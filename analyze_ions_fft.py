"""FFT-based ion-chain analysis for single frames and short time series.

Pipeline Architecture
---------------------
The analysis is decomposed into six named stages, each of which can be called
independently for debugging or for paper-figure generation:

    Stage 1 – Background & noise regime    (``stage_background``)
    Stage 2 – Noise power spectrum          (``stage_nps``)
    Stage 3 – Prefilter selection & apply   (``stage_prefilter``)
    Stage 4 – Corridor & PSF estimation     (``stage_corridor_and_psf``)
    Stage 5 – Matched-filter detection      (``stage_detection``)
    Stage 6 – State & spectral summary      (``stage_state_summary``)

The top-level ``analyze_array()`` chains all six stages.  Each stage takes a
``PipelineState`` dataclass and returns it with additional fields populated.
This keeps internal numpy arrays (needed for time-series spectral cubes)
cleanly separated from the JSON-serializable output dict.

Design Decisions
----------------
1. The pipeline consumes integer-valued grayscale matrices (NPZ archives
   or raw camera output).
2. The corridor-detection step is intentionally run *twice*: once on the
   bandpass image (to locate the chain region for PSF estimation), and once on
   the matched-filter response (to refine the corridor with PSF-informed
   weighting).  This two-pass strategy avoids the bootstrap problem of needing
   a PSF to build the matched filter but needing the chain location to estimate
   the PSF.
3. The matched filter is implemented as FFT cross-correlation (not convolution)
   via ``scipy.signal.fftconvolve``.  For our symmetric Gaussian kernel the
   distinction is moot, but the code and docstrings now use the term
   "cross-correlation" to avoid confusion.
4. ``max_ions`` is capped at 20 (``N < 21``) per the current experimental
   requirement.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from contextlib import nullcontext
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence, cast

import imageio.v2 as imageio
import numpy as np
from scipy import fft, linalg, ndimage, optimize, signal, special, stats
from shared_utils import suppress_known_runtime_warnings
from skimage.feature import peak_local_max
from detector_primitives import (
    background_surface_from_tiles,
    background_rms_surface_from_tiles,
    border_background,
    candidate_measurement_defaults,
    candidate_measurements,
    effective_local_patch_radius,
    extract_patch,
    extract_patch_with_fallback,
    fit_detection_amplitudes,
    gaussian_kernel,
    local_background_stats,
    patch_moments,
    poisson_candidate_metrics,
    render_gaussian_component,
    render_gaussian_probability_patch,
    robust_std,
    select_psf_exemplars,
    source_masked_background_stats,
)
from pipeline_state import Stage3OperatorState as ParallelStage3OperatorState
import stage0_ops as parallel_stage0_ops
import stage4 as parallel_stage4
import stage5 as parallel_stage5
import stage5_modes
import stage6 as parallel_stage6
import working_image as parallel_working_image


def _prime_cuda_path_from_wheel_runtime() -> None:
    if os.environ.get("CUDA_PATH"):
        return
    for site_path in sys.path:
        candidate = Path(site_path) / "nvidia" / "cuda_runtime"
        if candidate.exists():
            os.environ["CUDA_PATH"] = str(candidate)
            return


_prime_cuda_path_from_wheel_runtime()
suppress_known_runtime_warnings()

try:
    import cupy as cp
    from cupyx.scipy import ndimage as cupy_ndimage, signal as cupy_signal
except ImportError:  # pragma: no cover - optional dependency
    cp = None
    cupy_ndimage = None
    cupy_signal = None


# ---------------------------------------------------------------------------
#  Numerical guard
# ---------------------------------------------------------------------------
EPS = 1e-12
_REPO_ROOT = Path(__file__).resolve().parent
_RUNTIME_FFT_WORKERS: int | None = None
_RUNTIME_EXECUTION_TARGET = "cpu"
_RUNTIME_GPU_DEVICE_ID = 0
_MANUAL_ETA_WORKER_KEY: tuple[str, str] | None = None
_MANUAL_ETA_WORKER_PACKAGE: dict[str, Any] | None = None
CONFIG_RELATIVE_PATH_KEYS = frozenset(
    {
        "calibration_path",
        "eta_score_admissibility_npz_path",
        "eta_variant_count_legibility_npz_path",
    }
)
DEFAULT_MANUAL_CALIBRATED_INVESTIGATION_ROOT = (
    _REPO_ROOT / "manual_calibrated_mode_presets"
)
MANUAL_CALIBRATED_MODE_PRESET_RELATIVE_CONFIGS: dict[str, Path] = {
    "manual_calibrated_canonical": Path(
        "manual_calibrated_canonical/manual_detector_override.jsonl"
    ),
    "mode_integrated_snr": Path(
        "mode_integrated_snr/manual_detector_override.jsonl"
    ),
    "mode_support_mean_excess_snr": Path(
        "mode_support_mean_excess_snr/manual_detector_override.jsonl"
    ),
    "mode_support_sum_snr": Path(
        "mode_support_sum_snr/manual_detector_override.jsonl"
    ),
    "mode_template_support_excess_density": Path(
        "mode_template_support_excess_density/manual_detector_override.jsonl"
    ),
}
MANUAL_CALIBRATED_MODE_PRESET_CHOICES = tuple(MANUAL_CALIBRATED_MODE_PRESET_RELATIVE_CONFIGS)


def configure_runtime_acceleration(
    *,
    fft_workers: int | None = None,
    execution_target: str = "cpu",
    gpu_device_id: int | None = None,
) -> dict[str, Any]:
    """Configure the execution backend for subsequent frame analyses in this process."""
    global _RUNTIME_FFT_WORKERS, _RUNTIME_EXECUTION_TARGET, _RUNTIME_GPU_DEVICE_ID

    _RUNTIME_FFT_WORKERS = None if fft_workers is None else max(1, int(fft_workers))
    normalized_target = str(execution_target).strip().lower()
    _RUNTIME_EXECUTION_TARGET = "gpu" if normalized_target == "gpu" and _gpu_backend_available() else "cpu"
    if gpu_device_id is not None:
        _RUNTIME_GPU_DEVICE_ID = max(0, int(gpu_device_id))
    return runtime_acceleration_metadata()


def resolve_manual_calibrated_mode_config(
    mode_name: str,
    investigation_root: str | Path | None = None,
) -> Path:
    """Resolve a named manual-calibrated preset to its accepted post-iteration config."""

    normalized_mode_name = str(mode_name).strip()
    if normalized_mode_name not in MANUAL_CALIBRATED_MODE_PRESET_RELATIVE_CONFIGS:
        raise KeyError(
            f"Unknown manual-calibrated mode preset {normalized_mode_name!r}. "
            f"Expected one of {MANUAL_CALIBRATED_MODE_PRESET_CHOICES}."
        )

    root_path = (
        DEFAULT_MANUAL_CALIBRATED_INVESTIGATION_ROOT
        if investigation_root is None
        else Path(investigation_root).expanduser()
    )
    if not root_path.is_absolute():
        root_path = (_REPO_ROOT / root_path).resolve(strict=False)

    config_path = root_path / MANUAL_CALIBRATED_MODE_PRESET_RELATIVE_CONFIGS[normalized_mode_name]
    if not config_path.exists():
        raise FileNotFoundError(
            "Manual-calibrated mode preset "
            f"{normalized_mode_name!r} expected config at {config_path}"
        )
    return config_path


def runtime_acceleration_metadata() -> dict[str, Any]:
    """Return a serializable snapshot of the configured execution backend."""
    gpu_enabled = _runtime_gpu_enabled()
    return {
        "execution_target": "gpu" if gpu_enabled else "cpu",
        "fft_workers": _RUNTIME_FFT_WORKERS,
        "gpu_backend": "cupy" if gpu_enabled else None,
        "gpu_device_id": int(_RUNTIME_GPU_DEVICE_ID) if gpu_enabled else None,
    }


def gpu_runtime_backend_available() -> bool:
    """Return whether the CuPy-based GPU execution backend is available."""
    return _gpu_backend_available()


def _gpu_backend_available() -> bool:
    return cp is not None and cupy_ndimage is not None and cupy_signal is not None


def _runtime_gpu_enabled() -> bool:
    return _RUNTIME_EXECUTION_TARGET == "gpu" and _gpu_backend_available()


def _require_cupy() -> Any:
    if cp is None:
        raise RuntimeError("CuPy backend is not available.")
    return cp


def _require_cupy_ndimage() -> Any:
    if cupy_ndimage is None:
        raise RuntimeError("CuPy ndimage backend is not available.")
    return cupy_ndimage


def _require_cupy_signal() -> Any:
    if cupy_signal is None:
        raise RuntimeError("CuPy signal backend is not available.")
    return cupy_signal


def _fft_runtime_context() -> Any:
    if _RUNTIME_FFT_WORKERS is None:
        return nullcontext()
    return fft.set_workers(_RUNTIME_FFT_WORKERS)


def _gpu_device_context() -> Any:
    if not _runtime_gpu_enabled():
        return nullcontext()
    return _require_cupy().cuda.Device(int(_RUNTIME_GPU_DEVICE_ID))


def _is_gpu_array(value: Any) -> bool:
    return cp is not None and isinstance(value, cp.ndarray)


def _as_accel_array(value: Any, *, dtype: Any = np.float64) -> Any:
    if not _runtime_gpu_enabled():
        return np.asarray(value, dtype=dtype)
    with _gpu_device_context():
        return _require_cupy().asarray(value, dtype=dtype)


def _to_host_array(value: Any) -> np.ndarray:
    if _is_gpu_array(value):
        return _require_cupy().asnumpy(value)
    return np.asarray(value)


def _fftshift_fft2_array(image: Any) -> Any:
    if _is_gpu_array(image):
        gpu_cp = _require_cupy()
        return gpu_cp.fft.fftshift(gpu_cp.fft.fft2(image))
    return fft.fftshift(fft.fft2(np.asarray(image)))


def _fftconvolve_array(image: Any, kernel: Any, *, mode: str) -> Any:
    if _is_gpu_array(image) or _is_gpu_array(kernel):
        with _gpu_device_context():
            gpu_cp = _require_cupy()
            gpu_signal = _require_cupy_signal()
            gpu_image = (
                image
                if _is_gpu_array(image)
                else gpu_cp.asarray(image, dtype=gpu_cp.float64)
            )
            gpu_kernel = (
                kernel
                if _is_gpu_array(kernel)
                else gpu_cp.asarray(kernel, dtype=gpu_cp.float64)
            )
            return gpu_signal.fftconvolve(gpu_image, gpu_kernel, mode=mode)
    return signal.fftconvolve(np.asarray(image), np.asarray(kernel), mode=mode)


def _gaussian_filter_array(image: Any, sigma: float | Sequence[float]) -> Any:
    if _is_gpu_array(image):
        return _require_cupy_ndimage().gaussian_filter(image, sigma=sigma)
    return ndimage.gaussian_filter(np.asarray(image), sigma=sigma)


def _gaussian_filter1d_array(
    values: Any,
    sigma: float,
    *,
    axis: int = -1,
) -> Any:
    if _is_gpu_array(values):
        return _require_cupy_ndimage().gaussian_filter1d(
            values,
            sigma=sigma,
            axis=axis,
        )
    return ndimage.gaussian_filter1d(np.asarray(values), sigma=sigma, axis=axis)


def _host_or_accel_array_op(
    *values: Any,
    cpu_op: Callable[..., Any],
    accel_op: Callable[..., Any],
    accel_dtype: Any = np.float64,
    **kwargs: Any,
) -> np.ndarray:
    if not _runtime_gpu_enabled():
        return np.asarray(cpu_op(*values, **kwargs))
    accel_values = tuple(_as_accel_array(value, dtype=accel_dtype) for value in values)
    return _to_host_array(accel_op(*accel_values, **kwargs))


def _fftshift_fft2(image: np.ndarray) -> np.ndarray:
    return _host_or_accel_array_op(
        image,
        cpu_op=lambda value: fft.fftshift(fft.fft2(value)),
        accel_op=_fftshift_fft2_array,
    )


def _fftconvolve(image: np.ndarray, kernel: np.ndarray, *, mode: str) -> np.ndarray:
    return _host_or_accel_array_op(
        image,
        kernel,
        cpu_op=lambda image_value, kernel_value, *, mode: signal.fftconvolve(
            image_value,
            kernel_value,
            mode=mode,
        ),
        accel_op=_fftconvolve_array,
        mode=mode,
    )


def _gaussian_filter(image: np.ndarray, sigma: float | Sequence[float]) -> np.ndarray:
    return _host_or_accel_array_op(
        image,
        cpu_op=lambda value, *, sigma: ndimage.gaussian_filter(value, sigma=sigma),
        accel_op=_gaussian_filter_array,
        sigma=sigma,
    )


def _gaussian_filter1d(
    values: np.ndarray,
    sigma: float,
    *,
    axis: int = -1,
) -> np.ndarray:
    return _host_or_accel_array_op(
        values,
        cpu_op=lambda value, *, sigma, axis: ndimage.gaussian_filter1d(
            value,
            sigma=sigma,
            axis=axis,
        ),
        accel_op=_gaussian_filter1d_array,
        sigma=sigma,
        axis=axis,
    )


def _relative_deviation_to_target(value: float, target: float) -> float:
    """Return the relative deviation from a named detector model target."""
    return abs(value - target) / max(abs(target), EPS)


def _clamp01(value: float) -> float:
    """Clamp a scalar to the closed interval [0, 1]."""
    if not np.isfinite(value):
        return 0.0
    return float(np.clip(value, 0.0, 1.0))


def _log_positive_mean_ratio(values: np.ndarray) -> float:
    """Return log(geometric mean / arithmetic mean) for positive samples."""
    positive = np.asarray(values, dtype=np.float64)
    positive = positive[np.isfinite(positive) & (positive > 0.0)]
    if positive.size == 0:
        return float("nan")
    arithmetic_mean = float(np.mean(positive))
    if not np.isfinite(arithmetic_mean) or arithmetic_mean <= 0.0:
        return float("nan")
    return float(np.mean(np.log(positive)) - np.log(arithmetic_mean))


def _log_power_peak_to_mean(value: float) -> float:
    """Return the natural-log transform of a positive peak-to-mean power ratio."""
    ratio = float(value)
    if not np.isfinite(ratio) or ratio <= 0.0:
        return float("nan")
    return float(np.log(ratio))


def _equivalent_isotropic_sigma(sigma_x: float, sigma_y: float) -> float:
    """Return the area-preserving isotropic sigma for an anisotropic Gaussian."""
    if not np.isfinite(sigma_x) or not np.isfinite(sigma_y):
        return float("nan")
    if sigma_x <= 0 or sigma_y <= 0:
        return float("nan")
    return float(np.sqrt(sigma_x * sigma_y))


def _soft_step_score(
    value: float,
    threshold: float,
    scale: float,
    *,
    direction: str = "above",
) -> float:
    """Return a smooth 0..1 transition score around a threshold."""
    if not np.isfinite(value):
        return 0.0
    z = (value - threshold) / max(abs(scale), EPS)
    if direction == "below":
        z = -z
    return float(special.expit(z))


def _soft_band_score(
    value: float,
    lower: float,
    upper: float,
    edge_scale: float,
) -> float:
    """Return a smooth membership score for a finite interval."""
    if not np.isfinite(value):
        return 0.0
    lo = min(lower, upper)
    hi = max(lower, upper)
    scale = max(abs(edge_scale), EPS)
    enter = _soft_step_score(value, lo, scale, direction="above")
    leave = _soft_step_score(value, hi, scale, direction="below")
    return _clamp01(enter * leave)


def _soft_target_score(value: float, target: float, scale: float) -> float:
    """Return a Gaussian-like closeness score to a target value."""
    if not np.isfinite(value):
        return 0.0
    z = (value - target) / max(abs(scale), EPS)
    return float(np.exp(-0.5 * z * z))


def _normalize_score_dict(scores: dict[str, float]) -> dict[str, float]:
    """Normalize a score mapping to a probability-like simplex."""
    clean = {
        key: max(float(value), 0.0) if np.isfinite(value) else 0.0
        for key, value in scores.items()
    }
    total = sum(clean.values())
    if total <= EPS:
        if not clean:
            return {}
        uniform = 1.0 / len(clean)
        return {key: uniform for key in clean}
    return {key: value / total for key, value in clean.items()}


def _robust_location_stderr(values: np.ndarray) -> float:
    """Estimate a robust standard error for a location statistic."""
    finite = np.asarray(values, dtype=np.float64)
    finite = finite[np.isfinite(finite)]
    if finite.size < 2:
        return float("nan")

    center = float(np.nanmedian(finite))
    mad = float(np.nanmedian(np.abs(finite - center)))
    robust_sigma = 1.4826 * mad
    if robust_sigma <= EPS:
        sample_sigma = float(np.nanstd(finite, ddof=1))
        robust_sigma = sample_sigma if np.isfinite(sample_sigma) else 0.0

    if robust_sigma <= EPS:
        return 0.0

    median_se_factor = 1.2533141373155001
    return float(median_se_factor * robust_sigma / np.sqrt(finite.size))


def hot_pixel_fraction_control_limit(
    patch_size: int,
    sigma_threshold: float,
    z_score: float,
) -> float:
    """Return a binomial control limit for the hot-pixel fraction.

    A pixel is counted as "hot" when it exceeds the darkest-patch mean by
    ``sigma_threshold`` standard deviations. Under a clean detector model the
    expected exceedance rate is the corresponding one-sided Gaussian tail
    probability, so the acceptable empirical fraction scales with both the
    patch size and the chosen sigma threshold.
    """
    tail_probability = float(stats.norm.sf(sigma_threshold))
    variance = tail_probability * max(1.0 - tail_probability, 0.0)
    std = float(np.sqrt(variance / max(int(patch_size), 1)))
    return min(1.0, tail_probability + z_score * std)


class InputDataError(ValueError):
    """Raised when input image data violates the integer-valued contract."""


# ---------------------------------------------------------------------------
#  Configuration
# ---------------------------------------------------------------------------
# Parameters are grouped by the pipeline stage they primarily affect.  The
# defaults intentionally mix principled detector-model anchors (for example the
# Fano targets F=1 and F=2) with calibrated engineering constants (for example
# corridor widths and acceptance thresholds).  See ALGORITHM.md for the
# stage-by-stage rationale and for which thresholds should be treated as
# heuristic priors rather than universal constants.

DEFAULT_CFG: dict[str, Any] = {
    # ── Stage 1: Tiled background diagnostics ──────────────────────────────
    # The image is partitioned into non-overlapping tiles of size
    # ``bg_block_shape``.  Each tile is sigma-clipped to produce a mean and
    # variance estimate that is robust to hot pixels and outliers.
    "bg_block_shape": (64, 64),         # (rows, cols) per tile
    "sigma_clip": 3,                    # clip threshold in units of sigma
    "sigma_clip_iters": 3,              # maximum clip iterations per tile
    "background_quantile": 7 / 20,      # fraction of dimmest tiles used for
                                        #   the mean–variance fit
    "dark_tile_count": 6,               # tiles kept for NPS estimation

    # ── Stage 2: Noise power spectrum ──────────────────────────────────────
    # (No dedicated parameters — the NPS is computed from the dark tiles
    # selected in Stage 1.)

    # ── Stage 2b: Noise regime classification ──────────────────────────────
    # These thresholds gate whether the CRLB formulas, matched-filter
    # normalization, and prefilter choices are physically justified.
    #
    # Fano factor interpretation:
    #   F ≈ 1  →  Poisson (photon-counting)
    #   F ≈ 2  →  EMCCD with excess noise factor F²=2
    #   F >> 2 →  over-dispersed (structured background, quantization)
    #
    # Mean-variance slope interpretation:
    #   a ≈ 1  →  photon-counting
    #   a ≈ 2  →  EMCCD
    #   a >> 2 →  over-dispersed or quantized
    "fano_poisson_tol": 1 / 2,          # |F-1|/1 < tol → "poissonish"
    "fano_emccd_tol": 1 / 2,            # |F-2|/2 < tol → "emccd_like"
    "kurtosis_max": 10,                 # excess kurtosis < max → "tails_ok"
    "whiteness_lo": 1 / 2,              # whiteness_ratio ∈ [lo, hi] →
    "whiteness_hi": 2,                  #   "whiteish"
    "sigma_min_px": 3 / 2,              # PSF σ > min → "psf_sampled" (Nyquist)
    "psf_r2_min": 7 / 10,               # FFT fit R² > min → "psf_gaussian"
    "psf_consistency_tol": 3 / 10,       # |FFT-local|/local < tol →
                                        #   "psf_consistent"

    # ── Stage 3: Prefilter decision ────────────────────────────────────────
    "prefilter_gaussian_sigma": 4 / 5,   # sigma for Gaussian prefilter [px]
    "median_size": 3,                   # kernel size for median prefilter
    "hot_pixel_sigma": 6,               # threshold for hot-pixel fraction
    "hot_pixel_fraction_floor": 1 / 1000,  # conservative floor for real-camera
                                        #   hot-pixel fraction gating
    "hot_pixel_tail_zscore": 5,         # binomial control-limit width for
                                        #   hot-pixel exceedance fraction

    # ── Stage 4: Stage 4/5 search-window policy ────────────────────────────
    #  Full-frame search is the default. Legacy ROI and corridor restriction
    #  can be re-enabled explicitly for compatibility-oriented runs.
    "enable_search_roi": False,
    "search_row_fraction": (3 / 20, 9 / 10),   # used only when ROI mode is enabled
    "search_col_fraction": (3 / 10, 7 / 10),   # used only when ROI mode is enabled

    #  4b) Difference-of-Gaussians bandpass.  ``dog_small_sigma`` preserves
    #      ion-scale features; ``dog_large_sigma`` removes slow scatter.
    "dog_small_sigma": 6 / 5,           # fine scale [px]
    "dog_large_sigma": 12,              # broad scale [px]

    #  4c) Corridor controls used only when ROI mode is enabled.
    "search_half_width": 30,            # corridor half-width [px]
    "column_topk": 20,                  # sparse column-score proxy

    #  4d) Preliminary peak finding (for PSF patches only).
    "peak_min_distance": 7,             # one fifth of manual matched-count
                                        #   projected ion spacing [px]
    "peak_threshold_sigma": 5 / 4,      # calibrated seed threshold above the
                                        #   median [sigma]
    "peak_prominence_sigma": 6 / 5,     # calibrated seed prominence [sigma]

    #  4e) Local PSF estimation patches.
    "local_patch_radius": 12,           # requested half-size of sub-patch
                                        #   [px]; capped at half the peak
                                        #   spacing floor to avoid blending
                                        #   adjacent ions into one PSF patch
    "psf_r_frac": 1 / 4,               # calibrated fraction of Fourier radius
                                        #   used in the log-envelope fit
    "psf_cN": 2,                        # power threshold relative to the NPS
                                        #   floor for FFT-fit bins
    "psf_min_points": 25,               # engineering safeguard: minimum valid
                                        #   spectral bins for the FFT fit
    "psf_template_family": "auto",     # "auto" chooses anisotropic in clean,
                                        #   Poisson/EMCCD-like regimes when
                                        #   per-frame anisotropy is supported,
                                        #   and symmetric otherwise; the other
                                        #   supported values are "anisotropic"
                                        #   and "symmetric"
    "psf_estimation_policy": "production",  # "production" keeps the
                                        #   detector's current fallback
                                        #   heuristics; "data_first" disables
                                        #   heuristic PSF fallbacks for setup-
                                        #   specific calibration passes
    "stage5_variant_noise_policy": "all",  # "all" keeps the full four-
                                        #   variant Stage 5 ledger; use
                                        #   "selected_noise_only" to evaluate
                                        #   only the regime-selected noise
                                        #   model across PSF families
    "eta_mode": "off",                # "off" leaves frames untouched;
                                        #   "manual_calibrated" enables the
                                        #   branch-local eta runtime fields and
                                        #   score-admissibility references
    "eta_score_admissibility_npz_path": None,
                                        # optional companion NPZ containing
                                        #   branch-indexed residual power,
                                        #   threshold, and admissibility
                                        #   reference observations
    "eta_variant_count_legibility_npz_path": None,
                                        # optional companion NPZ containing
                                        #   branch-indexed runtime eta fields
                                        #   derived from each variant's own
                                        #   manual-match residual frames
    "eta_max_abs_correction": 1.5,     # cap the runtime eta surface;
                                        #   larger corrections still tend to
                                        #   reintroduce ion-shaped structure
    "eta_runtime_min_coherence": 1.0,  # minimum |eta_mean| / SE retained in
                                        #   the structured eta projection when
                                        #   eta_std is available in the artifact
    "enable_gaussian_warning_count_corrections": False,
                                        # opt-in legacy switch for the
                                        #   manual-review-backed Gaussian
                                        #   count-repair rules; the canonical
                                        #   runtime leaves these out-of-scope
                                        #   repairs disabled unless explicitly
                                        #   re-enabled for compatibility work

    # ── Stage 5: Ion detection and acceptance ──────────────────────────────
    "max_ions": 20,                     # hard cap  (N < 21)
    "min_accepted_matched_snr": 5.6,    # calibrated count-decision threshold,
                                        #   not a universal likelihood-ratio
                                        #   constant
    "experimental_stage5_modes": (),    # optional nested Stage 5 mode ledgers;
                                        #   empty preserves the canonical four
                                        #   public variants and selected count
    "experimental_stage5_selected_mode": None,
                                        # optional mode_id from
                                        #   experimental_stage5_modes to
                                        #   promote into the public count;
                                        #   None preserves canonical counts
    "experimental_stage5_mode_calibration_npz_path": None,
                                        # optional mode-keyed calibration
                                        #   artifact; canonical score artifacts
                                        #   remain separate
    "experimental_stage5_mode_policy": "ledger_only",
                                        # experimental modes record nested
                                        #   ledgers by default and do not alter
                                        #   canonical count semantics
    "compressed_artifact_min_accepted_matched_snr": 6.0,
                                        # compressed/artifact backgrounds have
                                        #   a wider false-positive shoulder than
                                        #   the legacy 5.6 floor; require a
                                        #   slightly stronger matched-SNR margin
    "eta_corrected_compressed_artifact_min_accepted_matched_snr": 8.0,
                                        # eta-corrected artifact frames need a
                                        #   stricter floor so weak structured
                                        #   residuals do not survive as ions
    "candidate_width_max_ratio": 11 / 5, # local raw-patch widths are often
                                          #   broader than the matched-filter
                                          #   template, especially for close
                                          #   spacing and real-data blur;
                                          #   broader blobs beyond this ratio
                                          #   are still rejected

    # ── Stage 6: Spectral chain metrics ────────────────────────────────────
    "axial_frequency_band": 3 / 50,     # |u| band for vertical power [cyc/px]
    "temporal_laplace_s_values":        # real s-values for temporal Laplace
        (1 / 10, 1 / 4, 1 / 2, 1),
}


# ---------------------------------------------------------------------------
#  Pipeline state container
# ---------------------------------------------------------------------------
@dataclass
class PipelineState:
    """Mutable state vector for the staged single-frame analysis.

    The dataclass stores both the published observables (counts, SNR values,
    PSF widths, corridor location) and the transient numpy arrays required by
    later stages.  Only the scientifically reportable quantities are copied
    into the final JSON result; intermediate arrays remain here so they can be
    reused internally without polluting the serialized output.
    """

    # Input -------------------------------------------------------------------
    image: np.ndarray                       # original grayscale frame (float64)
    cfg: dict[str, Any]                     # merged configuration
    source_name: str = "array"
    eta_correction: dict[str, Any] = field(default_factory=dict)

    # Stage 1 – background ----------------------------------------------------
    background: dict[str, Any] = field(default_factory=dict)
    background_surface: np.ndarray | None = None
    background_rms_surface: np.ndarray | None = None

    # Stage 2 – NPS ------------------------------------------------------------
    nps: dict[str, Any] = field(default_factory=dict)

    # Stage 2b – regime classification -----------------------------------------
    regime: dict[str, Any] = field(default_factory=dict)

    # Stage 3 – prefilter ------------------------------------------------------
    prefilter_choice: dict[str, Any] = field(default_factory=dict)
    corrected_image: np.ndarray | None = None
    working_image: np.ndarray | None = None
    working_image_metadata: dict[str, Any] = field(default_factory=dict)
    filtered_image: np.ndarray | None = None

    # Stage 4 – corridor & PSF ------------------------------------------------
    roi_raw: np.ndarray | None = None
    roi_corrected: np.ndarray | None = None
    roi_bounds: tuple[int, int, int, int] = (0, 0, 0, 0)
    bandpass_roi: np.ndarray | None = None
    corridor: dict[str, Any] = field(default_factory=dict)
    psf: dict[str, Any] = field(default_factory=dict)

    # Stage 5 – detection ------------------------------------------------------
    response_roi: np.ndarray | None = None
    response_band: np.ndarray | None = None
    matched_kernel: np.ndarray | None = None
    axial_profile: np.ndarray | None = None
    row_peak_indices: np.ndarray | None = None
    response_noise_std: float = 0.0
    count_decision_threshold: float = 0.0
    detections: list[dict[str, Any]] = field(default_factory=list)
    rejected_detections: list[dict[str, Any]] = field(default_factory=list)
    accepted_detections_by_variant: dict[str, list[dict[str, Any]]] = field(
        default_factory=dict
    )
    rejected_detections_by_variant: dict[str, list[dict[str, Any]]] = field(
        default_factory=dict
    )
    snr_variants: dict[str, Any] = field(default_factory=dict)

    # Stage 6 – state summary --------------------------------------------------
    state: dict[str, Any] = field(default_factory=dict)
    spectral: dict[str, Any] = field(default_factory=dict)
    roi_power_spectrum: np.ndarray | None = None
    stage_timings_s: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class DetectionVariantSpec:
    """One Stage 5 template/noise combination."""

    name: str
    template_family: str
    noise_model: str
    sigma_x: float
    sigma_y: float


def _record_stage_timing(
    ps: PipelineState,
    stage_name: str,
    stage_fn: Any,
) -> None:
    """Run one pipeline stage and store its elapsed wall time in seconds."""
    started = time.perf_counter()
    stage_fn(ps)
    ps.stage_timings_s[stage_name] = time.perf_counter() - started


def _stage5_variant_specs(psf: dict[str, Any]) -> tuple[DetectionVariantSpec, ...]:
    """Return the four Stage 5 template/noise combinations in stable order."""
    template_shapes = (
        (
            "anisotropic",
            float(psf["sigma_x_used_anisotropic"]),
            float(psf["sigma_y_used_anisotropic"]),
        ),
        (
            "symmetric",
            float(psf["sigma_x_used_symmetric"]),
            float(psf["sigma_y_used_symmetric"]),
        ),
    )
    return tuple(
        DetectionVariantSpec(
            name=f"{template_family}_{noise_model}",
            template_family=template_family,
            noise_model=noise_model,
            sigma_x=sigma_x,
            sigma_y=sigma_y,
        )
        for template_family, sigma_x, sigma_y in template_shapes
        for noise_model in ("gaussian", "poisson")
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Utility helpers
# ═══════════════════════════════════════════════════════════════════════════


def _selected_stage5_noise_model(regime_label: str) -> str:
    return "poisson" if regime_label == "photon_counting" else "gaussian"


def _stage5_variant_noise_policy(cfg: Mapping[str, Any] | None) -> str:
    policy = "all" if cfg is None else str(cfg.get("stage5_variant_noise_policy", "all") or "all")
    normalized_policy = policy.strip().lower()
    return "selected_noise_only" if normalized_policy == "selected_noise_only" else "all"


def _stage5_variant_specs_for_cfg(
    psf: dict[str, Any],
    cfg: Mapping[str, Any] | None,
    regime_label: str,
) -> tuple[DetectionVariantSpec, ...]:
    variant_specs = _stage5_variant_specs(psf)
    if _stage5_variant_noise_policy(cfg) != "selected_noise_only":
        return variant_specs
    selected_noise_model = _selected_stage5_noise_model(regime_label)
    return tuple(
        spec for spec in variant_specs if spec.noise_model == selected_noise_model
    )

def ensure_integer_valued_image(
    image: np.ndarray,
    source_name: str = "array",
) -> np.ndarray:
    """Validate that an input image is finite and integer-valued.

    The acquisition model assumes that raw image samples are integer counts.
    Arrays stored as floating-point are accepted only when every value is
    exactly integral, in which case they are converted to ``int64`` before the
    pipeline promotes them to ``float64`` for FFTs and statistics.

    Parameters
    ----------
    image : np.ndarray
        Input grayscale or RGB image array.
    source_name : str
        Human-readable identifier used in error messages.

    Returns
    -------
    np.ndarray
        Integer-typed array preserving the input shape.

    Raises
    ------
    InputDataError
        If the array is non-finite or contains non-integer values.
    """
    arr = np.asarray(image)
    if arr.ndim not in (2, 3):
        raise InputDataError(
            f"{source_name}: expected a 2-D grayscale or 3-D RGB array, "
            f"got shape {arr.shape}."
        )
    if np.issubdtype(arr.dtype, np.bool_):
        raise InputDataError(
            f"{source_name}: boolean image arrays are not valid intensity data."
        )
    if np.issubdtype(arr.dtype, np.integer):
        return arr

    try:
        numeric = np.asarray(arr, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise InputDataError(
            f"{source_name}: image array must contain integer-valued samples; "
            f"dtype {arr.dtype} cannot be interpreted numerically."
        ) from exc

    if not np.all(np.isfinite(numeric)):
        raise InputDataError(
            f"{source_name}: image array must contain only finite values."
        )
    if not np.array_equal(numeric, np.rint(numeric)):
        raise InputDataError(
            f"{source_name}: image array must contain only integer-valued "
            "samples; non-integer values were detected."
        )
    return np.rint(numeric).astype(np.int64)

def load_grayscale_image(source: str | Path | np.ndarray) -> np.ndarray:
    """Load an image or accept an already in-memory grayscale matrix.

    Parameters
    ----------
    source : str, Path, or np.ndarray
        File path (PNG, TIFF, …) or a pre-loaded 2-D / 3-D
        integer-valued array.

    Returns
    -------
    np.ndarray
        2-D float64 array.  RGB inputs are averaged across channels.
    """
    if isinstance(source, np.ndarray):
        img = ensure_integer_valued_image(source, source_name="in-memory array")
    else:
        img = ensure_integer_valued_image(
            imageio.imread(source),
            source_name=str(source),
        )

    if img.ndim == 3:
        img = img.mean(axis=2, dtype=np.float64)

    return np.asarray(img, dtype=np.float64)


def sigma_clip_stats(
    values: np.ndarray,
    sigma: float,
    max_iters: int,
) -> tuple[float, float, int]:
    """Return sigma-clipped (mean, variance, surviving_count) for one tile.

    Sigma clipping prevents a few hot pixels or extreme outliers from
    dominating the noise estimate.  For a raw camera stream this is a
    conservative pre-processing step, not an assertion that sensor noise is
    Gaussian.

    Parameters
    ----------
    values : np.ndarray
        Flat or n-D array of intensities.
    sigma : float
        Clip radius in units of the current standard deviation.
    max_iters : int
        Maximum number of rejection passes.

    Returns
    -------
    mean : float
    variance : float
    count : int
        Number of surviving samples after clipping.
    """
    arr = np.asarray(values, dtype=np.float64).ravel()
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan"), float("nan"), 0

    for _ in range(max_iters):
        mean = arr.mean()
        std = arr.std(ddof=0)
        if std <= EPS:
            break
        keep = np.abs(arr - mean) <= sigma * std
        if keep.all():
            break
        arr = arr[keep]
        if arr.size == 0:
            return float("nan"), float("nan"), 0

    return float(arr.mean()), float(arr.var(ddof=0)), int(arr.size)


def shifted_frequency_grids(
    shape: tuple[int, int],
) -> tuple[np.ndarray, np.ndarray]:
    """Return 2-D frequency grids aligned with ``fft.fftshift``-ed spectra.

    Parameters
    ----------
    shape : (rows, cols)

    Returns
    -------
    u_grid, v_grid : np.ndarray
        Meshgrid arrays in cycles-per-pixel, DC-centered.
    """
    h, w = shape
    u = fft.fftshift(fft.fftfreq(w))
    v = fft.fftshift(fft.fftfreq(h))
    return np.meshgrid(u, v)


def _view_as_non_overlapping_blocks_2d(
    array: np.ndarray,
    block_shape: tuple[int, int],
) -> np.ndarray:
    """Return a 2-D non-overlapping block view for an exactly tiled array."""
    block_rows = int(block_shape[0])
    block_cols = int(block_shape[1])
    rows, cols = array.shape
    if rows % block_rows != 0 or cols % block_cols != 0:
        raise ValueError("block_shape must divide array shape exactly.")
    return array.reshape(
        rows // block_rows,
        block_rows,
        cols // block_cols,
        block_cols,
    ).swapaxes(1, 2)


@lru_cache(maxsize=64)
def _hann_window_2d(shape: tuple[int, int]) -> np.ndarray:
    """Return one cached separable 2-D Hann window for a patch shape."""
    win_r = np.hanning(shape[0])
    win_c = np.hanning(shape[1])
    return np.outer(win_r, win_c)


def _hann_fft2(patch: np.ndarray) -> np.ndarray:
    """Return the DC-centered complex FFT of a mean-subtracted, Hann-windowed patch.

    This is the single implementation of windowed 2-D FFT used by
    ``windowed_power_spectrum``, ``estimate_psf_fft``, and
    ``spectral_chain_metrics``.

    Parameters
    ----------
    patch : np.ndarray
        2-D intensity patch.

    Returns
    -------
    np.ndarray
        DC-centered complex spectrum, same shape as *patch*.
    """
    patch_f64 = np.asarray(patch, dtype=np.float64)
    patch0 = patch_f64 - patch_f64.mean()
    window = _hann_window_2d((int(patch_f64.shape[0]), int(patch_f64.shape[1])))
    return _fftshift_fft2(patch0 * window)


def windowed_power_spectrum(patch: np.ndarray) -> np.ndarray:
    """Compute a Hann-windowed 2-D power spectrum for one patch.

    Parameters
    ----------
    patch : np.ndarray
        2-D intensity patch.

    Returns
    -------
    np.ndarray
        DC-centered |FFT|² array, same shape as *patch*.
    """
    return np.abs(_hann_fft2(patch)) ** 2


def reconstruct_frame_components(
    image: np.ndarray,
    background: dict[str, Any],
    detections: Sequence[dict[str, Any]],
    sigma_x: float,
    sigma_y: float,
) -> dict[str, Any]:
    """Reconstruct ``B + sum_k A_k h_k`` and summarize the residual spectral object.

    The returned residual summary is the detector-core seam for the shared
    Wiener-Khinchin-style object used by eta calibration. It preserves the
    current Gaussian reconstruction path but makes the residual correlation and
    spectral summaries explicit instead of leaving eta and noise as unrelated
    downstream heuristics.
    """
    image_f64 = np.asarray(image, dtype=np.float64)
    background_surface = background_surface_from_tiles(background, image_f64.shape)
    amplitudes, ion_model = fit_detection_amplitudes(
        image_f64,
        background_surface,
        detections,
        sigma_x,
        sigma_y,
    )
    r_v = image_f64 - background_surface - ion_model
    residual_spectral_object = _estimate_residual_spectral_object(r_v)
    detections_with_amplitude = []
    for det, amplitude in zip(detections, amplitudes, strict=True):
        updated = dict(det)
        updated["fitted_amplitude"] = float(amplitude)
        detections_with_amplitude.append(updated)
    return {
        "background_surface": background_surface,
        "ion_model_surface": ion_model,
        "residual_eta": r_v,
        "residual_spectral_summary": _residual_spectral_summary(
            residual_spectral_object
        ),
        "detections_with_amplitude": detections_with_amplitude,
    }


def _residual_spectral_summary(
    spectral_object: dict[str, Any],
) -> dict[str, Any]:
    """Return scalar audit fields for one shared residual spectral object."""
    power_spectrum_peak_to_mean = float(
        spectral_object.get("power_spectrum_peak_to_mean", float("nan"))
    )
    return {
        "wiener_khinchin_method": str(
            spectral_object.get("wiener_khinchin_method", "none")
        ),
        "structured_projection_method": str(
            spectral_object.get("structured_projection_method", "identity_fallback")
        ),
        "structured_support_pixel_count": int(
            spectral_object.get("structured_support_pixel_count", 0)
        ),
        "structured_correlation_length_px": float(
            spectral_object.get("structured_correlation_length_px", float("nan"))
        ),
        "noise_correlation_length_px": float(
            spectral_object.get("noise_correlation_length_px", float("nan"))
        ),
        "center_variance": float(
            spectral_object.get("center_variance", float("nan"))
        ),
        "power_spectrum_mean": float(
            spectral_object.get("power_spectrum_mean", float("nan"))
        ),
        "power_spectrum_peak": float(
            spectral_object.get("power_spectrum_peak", float("nan"))
        ),
        "power_spectrum_peak_to_mean": power_spectrum_peak_to_mean,
        "log_power_spectrum_peak_to_mean": _log_power_peak_to_mean(
            power_spectrum_peak_to_mean
        ),
    }


def _build_residual_spectral_object(
    *,
    structured_projection_method: str = "identity_fallback",
    structured_kernel: np.ndarray | None = None,
    structured_support_pixel_count: int = 1,
    structured_correlation_length_px: float = 0.0,
    noise_correlation_length_px: float = 0.0,
    center_variance: float = float("nan"),
    power_spectrum_mean: float = float("nan"),
    power_spectrum_peak: float = float("nan"),
    power_spectrum_peak_to_mean: float = float("nan"),
) -> dict[str, Any]:
    kernel = (
        np.ones((1, 1), dtype=np.float64)
        if structured_kernel is None
        else np.asarray(structured_kernel, dtype=np.float64)
    )
    return {
        "wiener_khinchin_method": "fft_autocovariance_periodogram",
        "structured_projection_method": str(structured_projection_method),
        "structured_kernel": kernel,
        "structured_support_pixel_count": int(structured_support_pixel_count),
        "structured_correlation_length_px": float(structured_correlation_length_px),
        "noise_correlation_length_px": float(noise_correlation_length_px),
        "center_variance": float(center_variance),
        "power_spectrum_mean": float(power_spectrum_mean),
        "power_spectrum_peak": float(power_spectrum_peak),
        "power_spectrum_peak_to_mean": float(power_spectrum_peak_to_mean),
    }


def _estimate_residual_spectral_object(
    residual: np.ndarray,
    support_mask: np.ndarray | None = None,
) -> dict[str, Any]:
    """Estimate one shared residual spectral object via a Wiener-Khinchin-style pass.

    The structured projection remains the runtime eta kernel source, while the
    noise projection is summarized as a correlation length that can later inform
    Stage 5 without changing the current public detector contract.
    """
    residual_f64 = np.asarray(residual, dtype=np.float64)
    valid = np.isfinite(residual_f64)
    if support_mask is not None:
        valid &= np.asarray(support_mask, dtype=np.bool_)

    fallback_kernel = np.ones((1, 1), dtype=np.float64)
    fallback = _build_residual_spectral_object(structured_kernel=fallback_kernel)
    if not np.any(valid):
        return fallback

    centered = np.zeros_like(residual_f64, dtype=np.float64)
    residual_values = residual_f64[valid]
    centered[valid] = residual_values - float(np.mean(residual_values))
    coverage = valid.astype(np.float64)

    if _runtime_gpu_enabled():
        centered_accel = _as_accel_array(centered)
        coverage_accel = _as_accel_array(coverage)
        autocov_full = _to_host_array(
            _fftconvolve_array(
                centered_accel,
                centered_accel[::-1, ::-1],
                mode="full",
            )
        )
        overlap_full = _to_host_array(
            _fftconvolve_array(
                coverage_accel,
                coverage_accel[::-1, ::-1],
                mode="full",
            )
        )
        power_spectrum = _to_host_array(
            _require_cupy().abs(_fftshift_fft2_array(centered_accel)) ** 2
        )
    else:
        autocov_full = _fftconvolve(
            centered,
            centered[::-1, ::-1],
            mode="full",
        )
        overlap_full = _fftconvolve(
            coverage,
            coverage[::-1, ::-1],
            mode="full",
        )
        power_spectrum = np.abs(_fftshift_fft2(centered)) ** 2

    autocov = np.divide(
        autocov_full,
        np.maximum(overlap_full, EPS),
        out=np.zeros_like(autocov_full, dtype=np.float64),
        where=overlap_full > EPS,
    )

    finite_power = power_spectrum[np.isfinite(power_spectrum)]
    if finite_power.size:
        power_mean = float(np.mean(finite_power))
        power_peak = float(np.max(finite_power))
        power_peak_to_mean = float(power_peak / max(power_mean, EPS))
    else:
        power_mean = float("nan")
        power_peak = float("nan")
        power_peak_to_mean = float("nan")

    center_row = int(residual_f64.shape[0] - 1)
    center_col = int(residual_f64.shape[1] - 1)
    center_variance = float(autocov[center_row, center_col])
    if not np.isfinite(center_variance) or center_variance <= EPS:
        return _build_residual_spectral_object(
            structured_kernel=fallback_kernel,
            center_variance=center_variance,
            power_spectrum_mean=power_mean,
            power_spectrum_peak=power_peak,
            power_spectrum_peak_to_mean=power_peak_to_mean,
        )

    rho = np.divide(
        autocov,
        center_variance,
        out=np.zeros_like(autocov, dtype=np.float64),
        where=np.isfinite(autocov),
    )

    positive = (overlap_full > EPS) & np.isfinite(rho) & (rho > 0)
    labels, _ = cast(
        tuple[np.ndarray, int],
        ndimage.label(positive, structure=np.ones((3, 3), dtype=np.uint8)),
    )
    center_label = int(labels[center_row, center_col])
    if center_label <= 0:
        structured_kernel = fallback_kernel
        structured_support_pixel_count = 1
        structured_correlation_length_px = 0.0
        structured_projection_method = "identity_fallback"
    else:
        support = labels == center_label
        support_rows = np.any(support, axis=1)
        support_cols = np.any(support, axis=0)
        row_idx = np.flatnonzero(support_rows)
        col_idx = np.flatnonzero(support_cols)
        row0, row1 = int(row_idx[0]), int(row_idx[-1] + 1)
        col0, col1 = int(col_idx[0]), int(col_idx[-1] + 1)
        support_cropped = support[row0:row1, col0:col1]
        structured_kernel = np.zeros_like(rho[row0:row1, col0:col1], dtype=np.float64)
        structured_kernel[support_cropped] = rho[row0:row1, col0:col1][support_cropped]
        kernel_sum = float(np.sum(structured_kernel))
        if kernel_sum <= EPS:
            structured_kernel = fallback_kernel
            structured_support_pixel_count = 1
            structured_correlation_length_px = 0.0
            structured_projection_method = "identity_fallback"
        else:
            structured_kernel /= kernel_sum
            local_center_row = center_row - row0
            local_center_col = center_col - col0
            rr_local, cc_local = np.indices(structured_kernel.shape)
            structured_correlation_length_px = float(np.sqrt(np.sum(
                structured_kernel
                * ((rr_local - local_center_row) ** 2 + (cc_local - local_center_col) ** 2)
            )))
            structured_support_pixel_count = int(np.sum(support_cropped))
            structured_projection_method = "connected_positive_lobe"

    noise_weights = np.zeros_like(rho, dtype=np.float64)
    noise_mask = (overlap_full > EPS) & np.isfinite(rho)
    noise_weights[noise_mask] = np.abs(rho[noise_mask])
    noise_weight_sum = float(np.sum(noise_weights))
    if noise_weight_sum <= EPS:
        noise_correlation_length_px = 0.0
    else:
        noise_weights /= noise_weight_sum
        rr_full, cc_full = np.indices(noise_weights.shape)
        noise_correlation_length_px = float(np.sqrt(np.sum(
            noise_weights
            * ((rr_full - center_row) ** 2 + (cc_full - center_col) ** 2)
        )))

    return _build_residual_spectral_object(
        structured_projection_method=structured_projection_method,
        structured_kernel=structured_kernel,
        structured_support_pixel_count=structured_support_pixel_count,
        structured_correlation_length_px=structured_correlation_length_px,
        noise_correlation_length_px=noise_correlation_length_px,
        center_variance=center_variance,
        power_spectrum_mean=power_mean,
        power_spectrum_peak=power_peak,
        power_spectrum_peak_to_mean=power_peak_to_mean,
    )


def _eta_autocorrelation_kernel(
    eta_mean: np.ndarray,
    covered: np.ndarray,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return a normalized runtime kernel from the shared residual spectral object."""
    spectral_object = _estimate_residual_spectral_object(eta_mean, covered)
    structured_projection_method = str(
        spectral_object.get("structured_projection_method", "identity_fallback")
    )
    kernel = np.asarray(
        spectral_object.get("structured_kernel", np.ones((1, 1), dtype=np.float64)),
        dtype=np.float64,
    )
    return kernel, {
        "eta_structured_kernel": np.asarray(kernel, dtype=np.float64),
        "eta_structured_projection_method": structured_projection_method,
        "eta_runtime_method": (
            "autocorr_connected"
            if structured_projection_method == "connected_positive_lobe"
            else "autocorr_identity_fallback"
        ),
        "eta_runtime_autocorr_support_pixel_count": int(
            spectral_object.get("structured_support_pixel_count", 1)
        ),
        "eta_runtime_autocorr_radius_px": float(
            spectral_object.get("structured_correlation_length_px", 0.0)
        ),
        "eta_noise_correlation_length_px": float(
            spectral_object.get("noise_correlation_length_px", float("nan"))
        ),
        "eta_residual_spectral_method": str(
            spectral_object.get("wiener_khinchin_method", "none")
        ),
        "eta_residual_center_variance": float(
            spectral_object.get("center_variance", float("nan"))
        ),
        "eta_residual_power_spectrum_peak_to_mean": float(
            spectral_object.get("power_spectrum_peak_to_mean", float("nan"))
        ),
    }


def build_runtime_eta_surface(
    eta_mean: np.ndarray,
    eta_count: np.ndarray,
    *,
    max_abs_correction: float,
    eta_std: np.ndarray | None = None,
    min_coherence: float = 0.0,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Return an autocorrelation-derived 2-D runtime eta surface and its support mask."""
    bar_eta_v = eta_mean
    n_v = eta_count
    covered = (n_v > 0) & np.isfinite(bar_eta_v)
    covered_bar_eta_v = np.where(covered, bar_eta_v, 0.0)
    kernel, runtime_info = _eta_autocorrelation_kernel(bar_eta_v, covered)

    if _runtime_gpu_enabled():
        filled_accel = _as_accel_array(covered_bar_eta_v)
        covered_accel = _as_accel_array(covered.astype(np.float64))
        kernel_accel = _as_accel_array(kernel)
        eta_smooth_num = _to_host_array(
            _fftconvolve_array(filled_accel, kernel_accel, mode="same")
        )
        eta_smooth_den = _to_host_array(
            _fftconvolve_array(covered_accel, kernel_accel, mode="same")
        )
    else:
        eta_smooth_num = _fftconvolve(covered_bar_eta_v, kernel, mode="same")
        eta_smooth_den = _fftconvolve(covered.astype(np.float64), kernel, mode="same")

    eta_v_runtime = np.divide(
        eta_smooth_num,
        np.maximum(eta_smooth_den, EPS),
        out=np.zeros_like(covered_bar_eta_v, dtype=np.float64),
        where=eta_smooth_den > EPS,
    )

    eta_runtime_mask = (
        covered
        & np.isfinite(eta_v_runtime)
        & (np.abs(eta_v_runtime) <= float(max_abs_correction))
    )
    coherence_kept_pixel_count = int(np.sum(eta_runtime_mask))
    if eta_std is not None and float(min_coherence) > 0.0:
        eta_std_v = np.asarray(eta_std, dtype=np.float64)
        eta_coherence_v = np.zeros_like(covered_bar_eta_v, dtype=np.float64)
        SE_v = np.full_like(covered_bar_eta_v, np.nan, dtype=np.float64)
        valid_SE_v = covered & np.isfinite(eta_std_v)
        SE_v[valid_SE_v] = eta_std_v[valid_SE_v] / np.sqrt(
            np.maximum(n_v[valid_SE_v], 1)
        )
        positive_SE_v = valid_SE_v & (SE_v > EPS)
        eta_coherence_v[positive_SE_v] = np.abs(bar_eta_v[positive_SE_v]) / SE_v[
            positive_SE_v
        ]
        infinite_coherence = valid_SE_v & (SE_v <= EPS) & (np.abs(bar_eta_v) > EPS)
        eta_coherence_v[infinite_coherence] = float("inf")
        eta_runtime_mask &= eta_coherence_v >= float(min_coherence)
        coherence_kept_pixel_count = int(np.sum(eta_runtime_mask))

    E_eta = np.zeros_like(covered_bar_eta_v, dtype=np.float64)
    E_eta[eta_runtime_mask] = eta_v_runtime[eta_runtime_mask]
    runtime_info["eta_runtime_min_coherence"] = float(min_coherence)
    runtime_info["eta_runtime_coherence_kept_pixel_count"] = coherence_kept_pixel_count
    return E_eta, eta_runtime_mask, runtime_info


def _finite_array_median(values: Any) -> float:
    """Return the median of finite values or NaN when none are available."""
    arr = np.asarray(values, dtype=np.float64)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return float("nan")
    return float(np.median(finite))


def _manual_eta_required_field(
    data: Any,
    field_name: str,
    *,
    artifact_path: Path,
) -> Any:
    if field_name not in data.files:
        raise InputDataError(
            f"Manual eta artifact {artifact_path} is missing required field {field_name}."
        )
    return data[field_name]


def _manual_eta_required_float(
    data: Any,
    field_name: str,
    *,
    artifact_path: Path,
) -> float:
    return float(
        np.asarray(
            _manual_eta_required_field(
                data,
                field_name,
                artifact_path=artifact_path,
            )
        ).item()
    )


def _manual_eta_required_int(
    data: Any,
    field_name: str,
    *,
    artifact_path: Path,
) -> int:
    return int(
        np.asarray(
            _manual_eta_required_field(
                data,
                field_name,
                artifact_path=artifact_path,
            )
        ).item()
    )


def _manual_eta_required_str(
    data: Any,
    field_name: str,
    *,
    artifact_path: Path,
) -> str:
    return str(
        np.asarray(
            _manual_eta_required_field(
                data,
                field_name,
                artifact_path=artifact_path,
            ),
            dtype=np.str_,
        ).item()
    )


def _manual_eta_optional_float(
    data: Any,
    field_name: str,
    *,
    default: float = float("nan"),
) -> float:
    if field_name not in data.files:
        return float(default)
    try:
        return float(np.asarray(data[field_name]).item())
    except (TypeError, ValueError):
        return float(default)


def _manual_eta_optional_str(
    data: Any,
    field_name: str,
    *,
    default: str = "",
) -> str:
    if field_name not in data.files:
        return str(default)
    try:
        return str(np.asarray(data[field_name], dtype=np.str_).item())
    except (TypeError, ValueError):
        return str(default)


def _manual_eta_runtime_sidecar_dir(
    artifact_path: Path,
    data: Any,
) -> Path:
    sidecar_dir_name = _manual_eta_required_str(
        data,
        "runtime_sidecar_dir_name",
        artifact_path=artifact_path,
    )
    return artifact_path.with_name(sidecar_dir_name)


def _load_manual_eta_sidecar_array(
    sidecar_path: Path,
    *,
    expected_dtype: Any,
    artifact_path: Path,
) -> np.ndarray:
    try:
        array = np.load(sidecar_path, allow_pickle=False, mmap_mode="r")
    except OSError as exc:
        raise InputDataError(
            f"Could not load manual eta sidecar {sidecar_path} referenced by {artifact_path}: {exc}"
        ) from exc

    expected = np.dtype(expected_dtype)
    if np.asarray(array).dtype != expected:
        raise InputDataError(
            f"Manual eta sidecar {sidecar_path} expected dtype {expected} but found {np.asarray(array).dtype}."
        )
    return array


def _build_score_admissibility_reference(
    *,
    variant_name: str,
    source_path: str | None,
    reference_applied: bool,
    reference_power_spectrum_peak_to_mean: float = float("nan"),
    reference_log_power_spectrum_peak_to_mean: float = float("nan"),
    reference_margin_to_threshold: float = float("nan"),
    reference_included_frame_count: int = 0,
    count_spectral_robust_lift_v1: dict[str, Any] | None = None,
    count_spectral_signed_threshold_v2: dict[str, Any] | None = None,
) -> dict[str, Any]:
    reference = {
        "reference_applied": bool(reference_applied),
        "source_path": source_path,
        "variant_name": variant_name,
        "reference_power_spectrum_peak_to_mean": float(
            reference_power_spectrum_peak_to_mean
        ),
        "reference_log_power_spectrum_peak_to_mean": float(
            reference_log_power_spectrum_peak_to_mean
        ),
        "reference_margin_to_threshold": float(reference_margin_to_threshold),
        "reference_included_frame_count": int(reference_included_frame_count),
    }
    if count_spectral_robust_lift_v1:
        reference["count_spectral_robust_lift_v1"] = dict(count_spectral_robust_lift_v1)
    if count_spectral_signed_threshold_v2:
        reference["count_spectral_signed_threshold_v2"] = dict(
            count_spectral_signed_threshold_v2
        )
    return reference


COUNT_SPECTRAL_ROBUST_LIFT_VERSION = "count_spectral_robust_lift_v1"
COUNT_SPECTRAL_SIGNED_THRESHOLD_VERSION = "count_spectral_signed_threshold_v2"


def _manual_eta_optional_count_spectral_robust_lift(
    data: Any,
    prefix: str,
) -> dict[str, Any] | None:
    version = _manual_eta_optional_str(
        data,
        f"{prefix}count_spectral_robust_lift_version",
    )
    if version != COUNT_SPECTRAL_ROBUST_LIFT_VERSION:
        return None
    return {
        "version": version,
        "score_key": _manual_eta_optional_str(data, f"{prefix}score_key"),
        "score_domain": _manual_eta_optional_str(data, f"{prefix}score_domain"),
        "lift_slope": _manual_eta_optional_float(data, f"{prefix}lift_slope"),
        "lift_cap": _manual_eta_optional_float(data, f"{prefix}lift_cap"),
        "safe_lift_ceiling": _manual_eta_optional_float(data, f"{prefix}safe_lift_ceiling"),
        "log_power_center": _manual_eta_optional_float(data, f"{prefix}log_power_center"),
        "log_power_scale": _manual_eta_optional_float(data, f"{prefix}log_power_scale"),
        "psd_adequacy_center": _manual_eta_optional_float(data, f"{prefix}psd_adequacy_center"),
        "psd_adequacy_scale": _manual_eta_optional_float(data, f"{prefix}psd_adequacy_scale"),
    }


def _manual_eta_optional_count_spectral_signed_threshold(
    data: Any,
    prefix: str,
) -> dict[str, Any] | None:
    version = _manual_eta_optional_str(
        data,
        f"{prefix}count_spectral_signed_threshold_version",
    )
    if version != COUNT_SPECTRAL_SIGNED_THRESHOLD_VERSION:
        return None
    return {
        "version": version,
        "score_key": _manual_eta_optional_str(data, f"{prefix}score_key"),
        "score_domain": _manual_eta_optional_str(data, f"{prefix}score_domain"),
        "signed_lift_slope": _manual_eta_optional_float(
            data,
            f"{prefix}signed_lift_slope",
        ),
        "artifact_decision_threshold_base": _manual_eta_optional_float(
            data,
            f"{prefix}artifact_decision_threshold_base",
        ),
        "delta_tau_lower_cap": _manual_eta_optional_float(
            data,
            f"{prefix}delta_tau_lower_cap",
        ),
        "delta_tau_upper_cap": _manual_eta_optional_float(
            data,
            f"{prefix}delta_tau_upper_cap",
        ),
        "log_power_center": _manual_eta_optional_float(data, f"{prefix}log_power_center"),
        "log_power_scale": _manual_eta_optional_float(data, f"{prefix}log_power_scale"),
        "psd_adequacy_center": _manual_eta_optional_float(
            data,
            f"{prefix}psd_adequacy_center",
        ),
        "psd_adequacy_scale": _manual_eta_optional_float(
            data,
            f"{prefix}psd_adequacy_scale",
        ),
        "threshold_interval_lower": _manual_eta_optional_float(
            data,
            f"{prefix}threshold_interval_lower",
        ),
        "threshold_interval_upper": _manual_eta_optional_float(
            data,
            f"{prefix}threshold_interval_upper",
        ),
        "signed_delta_policy": _manual_eta_optional_str(
            data,
            f"{prefix}signed_delta_policy",
            default="symmetric_frequency_difference",
        ),
    }


@lru_cache(maxsize=8)
def _load_manual_eta_package(
    score_npz_path: str,
    eta_npz_path: str,
) -> dict[str, Any]:
    """Load one cached manual-eta package with scalar references and memmapped sidecars."""
    score_path = Path(score_npz_path).expanduser()
    eta_path = Path(eta_npz_path).expanduser()
    try:
        with np.load(score_path, allow_pickle=False) as score_data, np.load(
            eta_path,
            allow_pickle=False,
        ) as eta_data:
            score_variant_names = tuple(
                str(name)
                for name in np.asarray(
                    score_data.get("variant_names", ()),
                    dtype=np.str_,
                )
            )
            eta_variant_names = tuple(
                str(name)
                for name in np.asarray(
                    eta_data.get("variant_names", ()),
                    dtype=np.str_,
                )
            )
            variant_names = tuple(
                dict.fromkeys((*eta_variant_names, *score_variant_names))
            )
            sidecar_dir = _manual_eta_runtime_sidecar_dir(eta_path, eta_data)
            package: dict[str, Any] = {
                "score_source_path": str(score_path),
                "eta_source_path": str(eta_path),
                "variant_names": variant_names,
                "variants": {},
            }
            for variant_name in variant_names:
                prefix = f"{variant_name}_"
                runtime_mean_file_name = _manual_eta_required_str(
                    eta_data,
                    f"{prefix}eta_runtime_mean_npy",
                    artifact_path=eta_path,
                )
                runtime_mask_file_name = _manual_eta_required_str(
                    eta_data,
                    f"{prefix}eta_runtime_mask_npy",
                    artifact_path=eta_path,
                )
                reference_log_power = _manual_eta_required_float(
                    score_data,
                    f"{prefix}reference_log_power_spectrum_peak_to_mean",
                    artifact_path=score_path,
                )
                signed_threshold = _manual_eta_optional_count_spectral_signed_threshold(
                    score_data,
                    prefix,
                )
                robust_lift = _manual_eta_optional_count_spectral_robust_lift(
                    score_data,
                    prefix,
                )
                if f"{prefix}reference_power_spectrum_peak_to_mean" in score_data.files:
                    reference_power = _manual_eta_required_float(
                        score_data,
                        f"{prefix}reference_power_spectrum_peak_to_mean",
                        artifact_path=score_path,
                    )
                else:
                    reference_power = (
                        float(np.exp(reference_log_power))
                        if np.isfinite(reference_log_power)
                        else float("nan")
                    )
                package["variants"][variant_name] = {
                    "variant_name": variant_name,
                    "score_source_path": str(score_path),
                    "eta_source_path": str(eta_path),
                    **_build_score_admissibility_reference(
                        variant_name=variant_name,
                        source_path=str(score_path),
                        reference_applied=bool(np.isfinite(reference_log_power)),
                        reference_power_spectrum_peak_to_mean=reference_power,
                        reference_log_power_spectrum_peak_to_mean=reference_log_power,
                        reference_margin_to_threshold=_manual_eta_required_float(
                            score_data,
                            f"{prefix}reference_margin_to_threshold",
                            artifact_path=score_path,
                        ),
                        reference_included_frame_count=_manual_eta_required_int(
                            score_data,
                            f"{prefix}reference_included_frame_count",
                            artifact_path=score_path,
                        ),
                        count_spectral_robust_lift_v1=robust_lift,
                        count_spectral_signed_threshold_v2=signed_threshold,
                    ),
                    "eta_runtime_mean": _load_manual_eta_sidecar_array(
                        sidecar_dir / runtime_mean_file_name,
                        expected_dtype=np.float64,
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_mask": _load_manual_eta_sidecar_array(
                        sidecar_dir / runtime_mask_file_name,
                        expected_dtype=np.bool_,
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_max_abs_correction": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_runtime_max_abs_correction",
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_method": _manual_eta_required_str(
                        eta_data,
                        f"{prefix}eta_runtime_method",
                        artifact_path=eta_path,
                    ),
                    "eta_structured_projection_method": _manual_eta_required_str(
                        eta_data,
                        f"{prefix}eta_structured_projection_method",
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_min_coherence": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_runtime_min_coherence",
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_autocorr_support_pixel_count": _manual_eta_required_int(
                        eta_data,
                        f"{prefix}eta_runtime_autocorr_support_pixel_count",
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_coherence_kept_pixel_count": _manual_eta_required_int(
                        eta_data,
                        f"{prefix}eta_runtime_coherence_kept_pixel_count",
                        artifact_path=eta_path,
                    ),
                    "eta_runtime_autocorr_radius_px": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_runtime_autocorr_radius_px",
                        artifact_path=eta_path,
                    ),
                    "eta_noise_correlation_length_px": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_noise_correlation_length_px",
                        artifact_path=eta_path,
                    ),
                    "eta_residual_spectral_method": _manual_eta_required_str(
                        eta_data,
                        f"{prefix}eta_residual_spectral_method",
                        artifact_path=eta_path,
                    ),
                    "eta_residual_center_variance": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_residual_center_variance",
                        artifact_path=eta_path,
                    ),
                    "eta_residual_power_spectrum_peak_to_mean": _manual_eta_required_float(
                        eta_data,
                        f"{prefix}eta_residual_power_spectrum_peak_to_mean",
                        artifact_path=eta_path,
                    ),
                }
    except OSError as exc:
        raise InputDataError(
            f"Could not load manual eta package score={score_path} runtime={eta_path}: {exc}"
        ) from exc
    return package


def _manual_eta_variant_record(
    cfg: dict[str, Any],
    variant_name: str,
) -> dict[str, Any] | None:
    score_path_value = cfg.get("eta_score_admissibility_npz_path")
    eta_path_value = cfg.get("eta_variant_count_legibility_npz_path")
    if score_path_value in (None, "") or eta_path_value in (None, ""):
        return None

    score_path = Path(str(score_path_value)).expanduser()
    eta_path = Path(str(eta_path_value)).expanduser()
    worker_key = (str(score_path), str(eta_path))
    if worker_key == _MANUAL_ETA_WORKER_KEY and _MANUAL_ETA_WORKER_PACKAGE is not None:
        package = _MANUAL_ETA_WORKER_PACKAGE
    else:
        package = _load_manual_eta_package(*worker_key)
    variant_payload = package["variants"].get(variant_name)
    if not isinstance(variant_payload, dict):
        raise InputDataError(
            f"Manual eta package score={score_path} runtime={eta_path} is missing required variant {variant_name}."
        )
    return variant_payload


def _manual_eta_artifact_paths_ready(cfg: dict[str, Any]) -> bool:
    score_path_value = cfg.get("eta_score_admissibility_npz_path")
    eta_path_value = cfg.get("eta_variant_count_legibility_npz_path")
    if score_path_value in (None, "") or eta_path_value in (None, ""):
        return False

    score_path = Path(str(score_path_value)).expanduser()
    eta_path = Path(str(eta_path_value)).expanduser()
    return score_path.is_file() and eta_path.is_file()


def _score_admissibility_reference_for_variant(
    cfg: dict[str, Any],
    variant_name: str,
    *,
    variant_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return branch-local log-power and margin references for threshold lifting."""
    score_path_value = cfg.get("eta_score_admissibility_npz_path")
    if score_path_value in (None, ""):
        return _build_score_admissibility_reference(
            variant_name=variant_name,
            source_path=None,
            reference_applied=False,
        )

    score_path = Path(str(score_path_value)).expanduser()
    if variant_payload is None:
        variant_payload = _manual_eta_variant_record(cfg, variant_name)
    if not isinstance(variant_payload, dict):
        return _build_score_admissibility_reference(
            variant_name=variant_name,
            source_path=str(score_path),
            reference_applied=False,
        )

    return _build_score_admissibility_reference(
        variant_name=variant_name,
        source_path=str(variant_payload["score_source_path"]),
        reference_applied=bool(variant_payload["reference_applied"]),
        reference_power_spectrum_peak_to_mean=float(
            variant_payload["reference_power_spectrum_peak_to_mean"]
        ),
        reference_log_power_spectrum_peak_to_mean=float(
            variant_payload["reference_log_power_spectrum_peak_to_mean"]
        ),
        reference_margin_to_threshold=float(
            variant_payload["reference_margin_to_threshold"]
        ),
        reference_included_frame_count=int(
            variant_payload["reference_included_frame_count"]
        ),
        count_spectral_robust_lift_v1=variant_payload.get(
            "count_spectral_robust_lift_v1"
        ),
        count_spectral_signed_threshold_v2=variant_payload.get(
            "count_spectral_signed_threshold_v2"
        ),
    )


def _finite_nonnegative(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(number) or number < 0.0:
        return None
    return float(number)


def _positive_finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(number) or number <= 0.0:
        return None
    return float(number)


def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(number):
        return None
    return float(number)


def _clamp_open_closed_interval(
    value: float,
    lower: float | None,
    upper: float | None,
) -> tuple[float, bool, bool]:
    if lower is None or upper is None:
        return float(value), False, False
    if not np.isfinite(lower) or not np.isfinite(upper) or upper <= lower:
        return float(value), False, False
    clamped = float(value)
    lower_open = float(np.nextafter(lower, np.inf))
    interval_applied = True
    was_clamped = False
    if clamped <= lower:
        clamped = lower_open
        was_clamped = True
    if clamped > upper:
        clamped = float(upper)
        was_clamped = True
    return float(clamped), bool(interval_applied), bool(was_clamped)


def _count_spectral_robust_lift_info(
    reference: dict[str, Any],
    residual_spectral_summary: dict[str, Any],
    current_log_power: float,
) -> dict[str, Any] | None:
    rule = reference.get("count_spectral_robust_lift_v1")
    if not isinstance(rule, dict):
        return None
    if str(rule.get("version", "")) != COUNT_SPECTRAL_ROBUST_LIFT_VERSION:
        return None

    log_power_scale = _positive_finite(rule.get("log_power_scale"))
    lift_slope = _finite_nonnegative(rule.get("lift_slope"))
    lift_cap = _finite_nonnegative(rule.get("lift_cap"))
    log_power_center = float(rule.get("log_power_center", float("nan")))
    if (
        log_power_scale is None
        or lift_slope is None
        or lift_cap is None
        or not np.isfinite(log_power_center)
        or not np.isfinite(current_log_power)
    ):
        return None

    z_power = max(0.0, (log_power_center - float(current_log_power)) / log_power_scale)
    z_psd = 0.0
    current_psd = residual_spectral_summary.get(
        "current_reference_psd_adequacy_score",
        residual_spectral_summary.get("reference_psd_adequacy_score", float("nan")),
    )
    psd_center = float(rule.get("psd_adequacy_center", float("nan")))
    psd_scale = _positive_finite(rule.get("psd_adequacy_scale"))
    try:
        current_psd_float = float(current_psd)
    except (TypeError, ValueError):
        current_psd_float = float("nan")
    if psd_scale is not None and np.isfinite(psd_center) and np.isfinite(current_psd_float):
        z_psd = max(0.0, (current_psd_float - psd_center) / psd_scale)

    z_frequency = max(z_power, z_psd)
    lift_uncapped = lift_slope * z_frequency
    lift_after_cap = min(lift_cap, lift_uncapped)
    safe_lift_ceiling = _finite_nonnegative(rule.get("safe_lift_ceiling"))
    if safe_lift_ceiling is not None:
        lift = min(lift_after_cap, safe_lift_ceiling)
    else:
        lift = lift_after_cap

    return {
        "score_admissibility_lift_rule_version": COUNT_SPECTRAL_ROBUST_LIFT_VERSION,
        "score_admissibility_lift_z_power": float(z_power),
        "score_admissibility_lift_z_psd": float(z_psd),
        "score_admissibility_lift_z_frequency": float(z_frequency),
        "score_admissibility_lift_uncapped": float(lift_uncapped),
        "score_admissibility_lift_cap": float(lift_cap),
        "score_admissibility_safe_lift_ceiling": (
            float(safe_lift_ceiling) if safe_lift_ceiling is not None else float("nan")
        ),
        "decision_threshold_lift": float(lift),
    }


def _count_spectral_signed_threshold_info(
    reference: dict[str, Any],
    residual_spectral_summary: dict[str, Any],
    current_log_power: float,
    tau_regime: float,
) -> dict[str, Any] | None:
    rule = reference.get("count_spectral_signed_threshold_v2")
    if not isinstance(rule, dict):
        return None
    if str(rule.get("version", "")) != COUNT_SPECTRAL_SIGNED_THRESHOLD_VERSION:
        return None

    tau_artifact_base = _finite_float(rule.get("artifact_decision_threshold_base"))
    tau_base = float(tau_regime if tau_artifact_base is None else tau_artifact_base)
    lower_cap = _finite_nonnegative(rule.get("delta_tau_lower_cap"))
    upper_cap = _finite_nonnegative(rule.get("delta_tau_upper_cap"))
    signed_lift_slope = _finite_nonnegative(rule.get("signed_lift_slope"))
    log_power_center = _finite_float(rule.get("log_power_center"))
    log_power_scale = _positive_finite(rule.get("log_power_scale"))
    if lower_cap is None or upper_cap is None or signed_lift_slope is None:
        return None

    z_power_raise = 0.0
    z_power_lower = 0.0
    if (
        log_power_center is not None
        and log_power_scale is not None
        and np.isfinite(current_log_power)
    ):
        z_power_raise = max(
            0.0,
            (log_power_center - float(current_log_power)) / log_power_scale,
        )
        z_power_lower = max(
            0.0,
            (float(current_log_power) - log_power_center) / log_power_scale,
        )

    current_psd = residual_spectral_summary.get(
        "current_reference_psd_adequacy_score",
        residual_spectral_summary.get("reference_psd_adequacy_score", float("nan")),
    )
    current_psd_float = _finite_float(current_psd)
    psd_center = _finite_float(rule.get("psd_adequacy_center"))
    psd_scale = _positive_finite(rule.get("psd_adequacy_scale"))
    z_psd_raise = 0.0
    z_psd_lower = 0.0
    if (
        current_psd_float is not None
        and psd_center is not None
        and psd_scale is not None
    ):
        z_psd_raise = max(0.0, (current_psd_float - psd_center) / psd_scale)
        z_psd_lower = max(0.0, (psd_center - current_psd_float) / psd_scale)

    z_raise = max(z_power_raise, z_psd_raise)
    z_lower = max(z_power_lower, z_psd_lower)
    delta_tau_raw = signed_lift_slope * (z_raise - z_lower)
    delta_tau_clipped = min(float(upper_cap), max(-float(lower_cap), delta_tau_raw))

    threshold_interval_lower = _finite_float(rule.get("threshold_interval_lower"))
    threshold_interval_upper = _finite_float(rule.get("threshold_interval_upper"))
    tau_candidate = tau_base + delta_tau_clipped
    tau_clamped, interval_applied, interval_clamped = _clamp_open_closed_interval(
        tau_candidate,
        threshold_interval_lower,
        threshold_interval_upper,
    )

    return {
        "score_admissibility_lift_rule_version": COUNT_SPECTRAL_SIGNED_THRESHOLD_VERSION,
        "score_admissibility_signed_delta_policy": str(
            rule.get("signed_delta_policy", "symmetric_frequency_difference")
            or "symmetric_frequency_difference"
        ),
        "score_admissibility_artifact_threshold_base": float(tau_base),
        "score_admissibility_fallback_threshold_base": float(tau_regime),
        "score_admissibility_delta_tau_lower_cap": float(lower_cap),
        "score_admissibility_delta_tau_upper_cap": float(upper_cap),
        "score_admissibility_threshold_interval_lower": (
            float(threshold_interval_lower)
            if threshold_interval_lower is not None
            else float("nan")
        ),
        "score_admissibility_threshold_interval_upper": (
            float(threshold_interval_upper)
            if threshold_interval_upper is not None
            else float("nan")
        ),
        "score_admissibility_signed_z_power_raise": float(z_power_raise),
        "score_admissibility_signed_z_power_lower": float(z_power_lower),
        "score_admissibility_signed_z_psd_raise": float(z_psd_raise),
        "score_admissibility_signed_z_psd_lower": float(z_psd_lower),
        "score_admissibility_signed_z_raise": float(z_raise),
        "score_admissibility_signed_z_lower": float(z_lower),
        "score_admissibility_signed_delta_raw": float(delta_tau_raw),
        "score_admissibility_interval_applied": bool(interval_applied),
        "score_admissibility_interval_clamped": bool(interval_clamped),
        "decision_threshold_base": float(tau_base),
        "decision_threshold_lift": float(delta_tau_clipped),
        "decision_threshold": float(tau_clamped),
    }


def _score_admissibility_threshold_info(
    cfg: dict[str, Any],
    variant_name: str,
    residual_spectral_summary: dict[str, Any],
    tau_regime: float,
    *,
    reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the branch-local threshold adjustment implied by the score artifact."""
    R_v_current = float(
        residual_spectral_summary.get("power_spectrum_peak_to_mean", float("nan"))
    )
    L_v_current = float(
        residual_spectral_summary.get(
            "log_power_spectrum_peak_to_mean",
            _log_power_peak_to_mean(R_v_current),
        )
    )
    if reference is None:
        reference = _score_admissibility_reference_for_variant(cfg, variant_name)
    delta_tau_v = 0.0
    threshold_base = float(tau_regime)
    robust_lift_info = None
    signed_threshold_info = _count_spectral_signed_threshold_info(
        reference,
        residual_spectral_summary,
        L_v_current,
        tau_regime,
    )
    if signed_threshold_info is not None:
        threshold_base = float(signed_threshold_info["decision_threshold_base"])
        delta_tau_v = float(signed_threshold_info["decision_threshold_lift"])
        tau_v_star = float(signed_threshold_info["decision_threshold"])
    elif reference["reference_applied"] and np.isfinite(L_v_current):
        robust_lift_info = _count_spectral_robust_lift_info(
            reference,
            residual_spectral_summary,
            L_v_current,
        )
        if robust_lift_info is None:
            L_v_star = float(reference["reference_log_power_spectrum_peak_to_mean"])
            delta_tau_v = max(
                0.0,
                L_v_star - L_v_current,
            )
        else:
            delta_tau_v = float(robust_lift_info["decision_threshold_lift"])
        tau_v_star = float(tau_regime + delta_tau_v)
    else:
        tau_v_star = float(threshold_base + delta_tau_v)

    info = {
        **reference,
        "current_power_spectrum_peak_to_mean": R_v_current,
        "current_log_power_spectrum_peak_to_mean": L_v_current,
        "decision_threshold_base": float(threshold_base),
        "decision_threshold_fallback_base": float(tau_regime),
        "decision_threshold_lift": float(delta_tau_v),
        "decision_threshold": tau_v_star,
    }
    if signed_threshold_info is not None:
        info.update(signed_threshold_info)
        info["decision_threshold"] = tau_v_star
    elif robust_lift_info is not None:
        info.update(robust_lift_info)
        info["decision_threshold"] = tau_v_star
    return info


def _score_admissibility_count_diagnostics(
    score_admissibility: dict[str, Any],
) -> dict[str, Any]:
    L_v_current = float(
        score_admissibility.get("current_log_power_spectrum_peak_to_mean", float("nan"))
    )
    R_v_current = float(
        score_admissibility.get(
            "current_power_spectrum_peak_to_mean",
            float(np.exp(L_v_current))
            if np.isfinite(L_v_current)
            else float("nan"),
        )
    )
    L_v_star = float(
        score_admissibility.get("reference_log_power_spectrum_peak_to_mean", float("nan"))
    )
    R_v_star = float(
        score_admissibility.get(
            "reference_power_spectrum_peak_to_mean",
            float(np.exp(L_v_star))
            if np.isfinite(L_v_star)
            else float("nan"),
        )
    )
    diagnostics = {
        "decision_threshold_base": float(
            score_admissibility["decision_threshold_base"]
        ),
        "decision_threshold_fallback_base": float(
            score_admissibility.get(
                "decision_threshold_fallback_base",
                score_admissibility["decision_threshold_base"],
            )
        ),
        "decision_threshold_lift": float(
            score_admissibility["decision_threshold_lift"]
        ),
        "score_admissibility_reference_applied": bool(
            score_admissibility["reference_applied"]
        ),
        "score_admissibility_current_power_spectrum_peak_to_mean": R_v_current,
        "score_admissibility_current_log_power_spectrum_peak_to_mean": L_v_current,
        "score_admissibility_reference_power_spectrum_peak_to_mean": R_v_star,
        "score_admissibility_reference_log_power_spectrum_peak_to_mean": L_v_star,
        "score_admissibility_reference_margin_to_threshold": float(
            score_admissibility["reference_margin_to_threshold"]
        ),
    }
    for key in (
        "score_admissibility_lift_rule_version",
        "score_admissibility_signed_delta_policy",
        "score_admissibility_artifact_threshold_base",
        "score_admissibility_fallback_threshold_base",
        "score_admissibility_delta_tau_lower_cap",
        "score_admissibility_delta_tau_upper_cap",
        "score_admissibility_threshold_interval_lower",
        "score_admissibility_threshold_interval_upper",
        "score_admissibility_signed_z_power_raise",
        "score_admissibility_signed_z_power_lower",
        "score_admissibility_signed_z_psd_raise",
        "score_admissibility_signed_z_psd_lower",
        "score_admissibility_signed_z_raise",
        "score_admissibility_signed_z_lower",
        "score_admissibility_signed_delta_raw",
        "score_admissibility_interval_applied",
        "score_admissibility_interval_clamped",
        "score_admissibility_lift_z_power",
        "score_admissibility_lift_z_psd",
        "score_admissibility_lift_z_frequency",
        "score_admissibility_lift_uncapped",
        "score_admissibility_lift_cap",
        "score_admissibility_safe_lift_ceiling",
    ):
        if key in score_admissibility:
            diagnostics[key] = score_admissibility[key]
    return diagnostics


def _require_manual_eta_artifact_path(
    cfg: dict[str, Any],
    field_name: str,
) -> Path:
    path_value = cfg.get(field_name)
    if path_value in (None, ""):
        raise InputDataError(
            f"eta_mode='manual_calibrated' requires {field_name}."
        )

    path = Path(str(path_value)).expanduser()
    if not path.is_file():
        raise InputDataError(
            f"eta_mode='manual_calibrated' requires existing {field_name}: {path}"
        )
    return path


def configure_manual_eta_worker_instructions(cfg: dict[str, Any] | None) -> None:
    """Install or clear one worker-global manual eta package for repeated frame analysis."""
    global _MANUAL_ETA_WORKER_KEY, _MANUAL_ETA_WORKER_PACKAGE

    normalized_cfg = cfg or {}
    if str(normalized_cfg.get("eta_mode", "off")).lower() != "manual_calibrated":
        _MANUAL_ETA_WORKER_KEY = None
        _MANUAL_ETA_WORKER_PACKAGE = None
        return

    score_path = _require_manual_eta_artifact_path(
        normalized_cfg,
        "eta_score_admissibility_npz_path",
    )
    eta_path = _require_manual_eta_artifact_path(
        normalized_cfg,
        "eta_variant_count_legibility_npz_path",
    )
    worker_key = (str(score_path), str(eta_path))
    _MANUAL_ETA_WORKER_KEY = worker_key
    _MANUAL_ETA_WORKER_PACKAGE = _load_manual_eta_package(*worker_key)


def _build_eta_metadata(
    *,
    eta_mode: str,
    eta_source_path: str | None,
    eta_runtime_min_coherence: float,
    eta_variant_name: str | None = None,
    eta_max_abs_correction: float | None = None,
    eta_runtime_surface_source: str | None = None,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "eta_mode": str(eta_mode),
        "eta_applied": False,
        "eta_source_path": eta_source_path,
        "eta_overlap_shape": [0, 0],
        "eta_covered_pixel_count": 0,
        "eta_runtime_method": "none",
        "eta_runtime_autocorr_support_pixel_count": 0,
        "eta_runtime_autocorr_radius_px": float("nan"),
        "eta_runtime_min_coherence": float(eta_runtime_min_coherence),
        "eta_runtime_coherence_kept_pixel_count": 0,
        "eta_noise_correlation_length_px": float("nan"),
        "eta_residual_spectral_method": "none",
        "eta_residual_center_variance": float("nan"),
        "eta_residual_power_spectrum_peak_to_mean": float("nan"),
    }
    if eta_variant_name is not None:
        metadata["eta_variant_name"] = eta_variant_name
    if eta_max_abs_correction is not None:
        metadata["eta_max_abs_correction"] = float(eta_max_abs_correction)
    if eta_runtime_surface_source is not None:
        metadata["eta_runtime_surface_source"] = eta_runtime_surface_source
    return metadata


def prepare_eta_correction(
    image_shape: tuple[int, int],
    cfg: dict[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return the eta-corrected surface to subtract and audit metadata."""
    eta_mode = str(cfg.get("eta_mode", "off")).lower()
    if eta_mode in {"off", "none", "disabled"}:
        return np.zeros(image_shape, dtype=np.float64), _build_eta_metadata(
            eta_mode="off",
            eta_source_path=None,
            eta_runtime_min_coherence=float("nan"),
        )

    if eta_mode != "manual_calibrated":
        raise InputDataError(
            f"Unsupported eta_mode {eta_mode!r}. Expected 'off' or 'manual_calibrated'."
        )

    variant_count_path = _require_manual_eta_artifact_path(
        cfg,
        "eta_variant_count_legibility_npz_path",
    )
    _require_manual_eta_artifact_path(
        cfg,
        "eta_score_admissibility_npz_path",
    )
    return np.zeros(image_shape, dtype=np.float64), _build_eta_metadata(
        eta_mode="manual_calibrated",
        eta_source_path=str(variant_count_path),
        eta_runtime_min_coherence=float(
            cfg.get("eta_runtime_min_coherence", float("nan"))
        ),
        eta_max_abs_correction=float(cfg.get("eta_max_abs_correction", 0.0)),
        eta_runtime_surface_source="branch_variant_count_legibility_pending",
    )


def _prepare_variant_count_legibility_correction(
    image_shape: tuple[int, int],
    cfg: dict[str, Any],
    variant_name: str,
    *,
    variant_payload: dict[str, Any] | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return one branch-local runtime eta surface and audit metadata."""
    path_value = cfg.get("eta_variant_count_legibility_npz_path")
    correction = np.zeros(image_shape, dtype=np.float64)
    if path_value in (None, ""):
        return correction, _build_eta_metadata(
            eta_mode=str(cfg.get("eta_mode", "off")).lower(),
            eta_source_path=None,
            eta_runtime_min_coherence=float("nan"),
            eta_variant_name=variant_name,
            eta_max_abs_correction=float(cfg.get("eta_max_abs_correction", 0.0)),
            eta_runtime_surface_source="none",
        )

    path = Path(str(path_value)).expanduser()
    if variant_payload is None:
        variant_payload = _manual_eta_variant_record(cfg, variant_name)
    metadata = _build_eta_metadata(
        eta_mode="manual_calibrated",
        eta_source_path=str(path),
        eta_runtime_min_coherence=float("nan"),
        eta_variant_name=variant_name,
        eta_max_abs_correction=float(cfg.get("eta_max_abs_correction", 0.0)),
        eta_runtime_surface_source="branch_variant_count_legibility_runtime_field",
    )
    if not isinstance(variant_payload, dict):
        return correction, metadata

    E_eta_payload = variant_payload.get("eta_runtime_mean")
    eta_runtime_mask_payload = variant_payload.get("eta_runtime_mask")
    if E_eta_payload is None or eta_runtime_mask_payload is None:
        return correction, metadata

    E_eta_f64 = np.asarray(E_eta_payload, dtype=np.float64)
    eta_runtime_mask_bool = np.asarray(eta_runtime_mask_payload, dtype=np.bool_)
    overlap_h = min(int(image_shape[0]), int(E_eta_f64.shape[0]))
    overlap_w = min(int(image_shape[1]), int(E_eta_f64.shape[1]))
    if overlap_h <= 0 or overlap_w <= 0:
        return correction, metadata

    eta_runtime_valid = (
        eta_runtime_mask_bool[:overlap_h, :overlap_w]
        & np.isfinite(E_eta_f64[:overlap_h, :overlap_w])
    )
    correction_overlap = correction[:overlap_h, :overlap_w]
    correction_overlap[eta_runtime_valid] = E_eta_f64[:overlap_h, :overlap_w][
        eta_runtime_valid
    ]
    metadata.update(
        {
            "eta_applied": bool(np.any(eta_runtime_valid)),
            "eta_overlap_shape": [int(overlap_h), int(overlap_w)],
            "eta_covered_pixel_count": int(np.sum(eta_runtime_valid)),
            "eta_max_abs_correction": float(
                variant_payload.get(
                    "eta_runtime_max_abs_correction",
                    cfg.get("eta_max_abs_correction", 0.0),
                )
            ),
            "eta_runtime_method": str(
                variant_payload.get("eta_runtime_method", "none")
            ),
            "eta_runtime_autocorr_support_pixel_count": int(
                variant_payload.get("eta_runtime_autocorr_support_pixel_count", 0)
            ),
            "eta_runtime_autocorr_radius_px": float(
                variant_payload.get("eta_runtime_autocorr_radius_px", float("nan"))
            ),
            "eta_runtime_min_coherence": float(
                variant_payload.get("eta_runtime_min_coherence", float("nan"))
            ),
            "eta_runtime_coherence_kept_pixel_count": int(
                variant_payload.get("eta_runtime_coherence_kept_pixel_count", 0)
            ),
            "eta_noise_correlation_length_px": float(
                variant_payload.get("eta_noise_correlation_length_px", float("nan"))
            ),
            "eta_residual_spectral_method": str(
                variant_payload.get("eta_residual_spectral_method", "none")
            ),
            "eta_residual_center_variance": float(
                variant_payload.get("eta_residual_center_variance", float("nan"))
            ),
            "eta_residual_power_spectrum_peak_to_mean": float(
                variant_payload.get(
                    "eta_residual_power_spectrum_peak_to_mean",
                    float("nan"),
                )
            ),
        }
    )
    return correction, metadata


def _variant_detection_inputs(
    ps: PipelineState,
    correction: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return branch-local image, ROI, and bandpass inputs for Stage 5."""
    assert ps.roi_raw is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."
    assert ps.bandpass_roi is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."

    correction_f64 = np.asarray(correction, dtype=np.float64)
    detection_image = np.asarray(ps.image, dtype=np.float64)
    if np.any(correction_f64):
        detection_image = detection_image - correction_f64

    working_views = _build_working_image_views(
        detection_image,
        ps.background,
        ps.prefilter_choice,
    )
    r0, r1, c0, c1 = ps.roi_bounds
    roi_raw = detection_image[r0:r1, c0:c1]
    bandpass_roi = compute_bandpass(
        working_views["filtered_image"][r0:r1, c0:c1],
        ps.cfg,
    )
    return detection_image, roi_raw, bandpass_roi


def _eta_correction_has_effective_signal(correction: np.ndarray) -> bool:
    return bool(np.any(np.asarray(correction, dtype=np.float64)))


def _build_working_image_views(
    image: np.ndarray,
    background: dict[str, Any],
    prefilter_choice: dict[str, Any],
) -> dict[str, Any]:
    """Build the corrected-image working views used by Stage 3-5."""
    image_f64 = np.asarray(image, dtype=np.float64)
    background_surface = background_surface_from_tiles(background, image_f64.shape)
    background_rms_surface = background_rms_surface_from_tiles(
        background,
        image_f64.shape,
    )
    corrected_image = image_f64 - background_surface
    filtered_image = apply_prefilter(corrected_image, prefilter_choice)
    return {
        "background_surface": background_surface,
        "background_rms_surface": background_rms_surface,
        "corrected_image": corrected_image,
        "filtered_image": filtered_image,
        "working_image": corrected_image,
        "metadata": {
            "background_correction_applied": True,
            "noise_operator": "identity",
            "working_image_basis": "background_corrected",
        },
    }


def _accepted_detection_signature(
    detections: Sequence[dict[str, Any]],
) -> tuple[tuple[float | None, float | None], ...]:
    signature: list[tuple[float | None, float | None]] = []
    for det in detections:
        row_value = det.get("row")
        col_value = det.get("col")
        signature.append(
            (
                None if row_value is None else float(row_value),
                None if col_value is None else float(col_value),
            )
        )
    signature.sort(key=lambda item: (item[0] is None, item[0], item[1] is None, item[1]))
    return tuple(signature)


def _reconstruction_summary_for_variant(
    reconstruction_cache: dict[
        tuple[int, float, float, tuple[tuple[float | None, float | None], ...]],
        dict[str, Any],
    ],
    detection_image: np.ndarray,
    background: dict[str, Any],
    accepted: Sequence[dict[str, Any]],
    *,
    sigma_x: float,
    sigma_y: float,
) -> dict[str, Any]:
    cache_key = (
        id(detection_image),
        float(sigma_x),
        float(sigma_y),
        _accepted_detection_signature(accepted),
    )
    reconstruction_summary = reconstruction_cache.get(cache_key)
    if reconstruction_summary is not None:
        return reconstruction_summary

    reconstruction = reconstruct_frame_components(
        detection_image,
        background,
        accepted,
        sigma_x=sigma_x,
        sigma_y=sigma_y,
    )
    reconstruction_summary = dict(reconstruction["residual_spectral_summary"])
    reconstruction_cache[cache_key] = reconstruction_summary
    return reconstruction_summary


def _background_reference_mean(
    background: dict[str, Any],
    image: np.ndarray,
) -> float:
    """Return a positive frame-level background reference for Poisson scaling."""
    reference = background.get("median_mean")
    if reference is None or not np.isfinite(reference) or reference <= 0:
        reference = float(np.median(image))
    return float(max(reference, EPS))


def _poisson_scaled_noise_std(
    gaussian_noise_std: float,
    local_background_mean: float,
    background_reference_mean: float,
) -> float:
    """Approximate matched-filter noise under a local Poisson model.

    The Gaussian baseline is already estimated from the darkest tiles after
    the same Stage 3-5 filtering chain. Local Poisson scaling may increase the
    noise floor in brighter backgrounds, but it should not make a dark
    candidate more permissive than that empirical baseline.
    """
    if not np.isfinite(gaussian_noise_std) or gaussian_noise_std <= EPS:
        return float("nan")
    if not np.isfinite(local_background_mean) or local_background_mean <= 0:
        return float("nan")
    if not np.isfinite(background_reference_mean) or background_reference_mean <= 0:
        return float("nan")
    effective_background_mean = max(
        float(local_background_mean),
        float(background_reference_mean),
    )
    return float(
        gaussian_noise_std
        * np.sqrt(effective_background_mean / max(background_reference_mean, EPS))
    )


def _effective_detection_threshold(
    cfg: dict[str, Any],
    regime_label: str,
    *,
    eta_applied: bool,
) -> float:
    """Return the matched-SNR threshold used for Stage 5 count acceptance."""
    tau_0 = float(cfg["min_accepted_matched_snr"])
    if regime_label != "compressed_or_artifact":
        return tau_0

    tau_regime = max(
        tau_0,
        float(cfg.get("compressed_artifact_min_accepted_matched_snr", tau_0)),
    )
    if eta_applied:
        tau_regime = max(
            tau_regime,
            float(
                cfg.get(
                    "eta_corrected_compressed_artifact_min_accepted_matched_snr",
                    tau_regime,
                )
            ),
        )
    return tau_regime


def _apply_detection_noise_model(
    detections: list[dict[str, Any]],
    noise_model: str,
    gaussian_noise_std: float,
    background_reference_mean: float,
) -> list[dict[str, Any]]:
    """Return candidate records with ``matched_snr`` rewritten for one noise model."""
    modeled: list[dict[str, Any]] = []
    for det in detections:
        updated = dict(det)
        matched_response = float(updated.get("matched_response", float("nan")))

        if noise_model == "poisson":
            modeled_noise_std = float("nan")
            updated["matched_score_basis"] = "poisson_deviance_sqrt"
            updated["matched_snr"] = float(
                updated.get("poisson_score", float("nan"))
            )
        else:
            modeled_noise_std = float(gaussian_noise_std)
            updated["matched_score_basis"] = "gaussian_matched_snr"
            updated["matched_snr"] = (
                float(matched_response / modeled_noise_std)
                if np.isfinite(matched_response) and modeled_noise_std > EPS
                else float("nan")
            )

        updated["matched_noise_model"] = noise_model
        updated["matched_noise_std"] = modeled_noise_std
        modeled.append(updated)
    return modeled


def _detection_variant_summary(
    variant_name: str,
    template_family: str,
    noise_model: str,
    sigma_x: float,
    sigma_y: float,
    gaussian_noise_std: float,
    corridor: dict[str, Any],
    accepted: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    tau_v_star: float,
) -> dict[str, Any]:
    """Summarize one template/noise variant without replacing the public detector."""
    accepted_snrs = [float(det["matched_snr"]) for det in accepted]
    rejected_snrs = [
        float(det["matched_snr"])
        for det in sorted(rejected, key=lambda item: item["row"])
        if np.isfinite(det.get("matched_snr", float("nan")))
    ]
    state = state_metrics(accepted)
    count_diagnostics = count_decision_metrics(
        accepted,
        rejected,
        tau_v_star,
    )
    count_diagnostics.update(
        manual_review_warning_metrics(
            visible_ion_count=int(state["visible_ion_count"]),
            weakest_ion_snr=float(state["weakest_ion_snr"]),
            nearest_boundary_margin=float(count_diagnostics["nearest_boundary_margin"]),
            sigma_x=float(sigma_x),
            sigma_y=float(sigma_y),
            axial_spacing_px_spatial=float(state["axial_spacing_px_spatial"]),
        )
    )
    manual_review_warning = bool(count_diagnostics["manual_review_warning"])
    manual_review_warning_reason = str(
        count_diagnostics["manual_review_warning_reason"]
    )
    return {
        "variant_name": variant_name,
        "template_family": template_family,
        "noise_model": noise_model,
        "score_basis": (
            "poisson_deviance_sqrt"
            if noise_model == "poisson"
            else "gaussian_matched_snr"
        ),
        "sigma_x": float(sigma_x),
        "sigma_y": float(sigma_y),
        "response_noise_std": float(gaussian_noise_std),
        "visible_ion_count": int(len(accepted)),
        "state": state,
        "count_diagnostics": count_diagnostics,
        "manual_review_warning": manual_review_warning,
        "manual_review_warning_reason": manual_review_warning_reason,
        "candidate_count_total": int(len(accepted) + len(rejected)),
        "accepted_matched_snrs": accepted_snrs,
        "rejected_matched_snrs": rejected_snrs,
        "chain_column": int(corridor["chain_col"]),
        "corridor_drift_px": int(corridor.get("corridor_drift_px", 0)),
    }


def _warning_reason_tokens(value: Any) -> set[str]:
    return {
        token.strip()
        for token in str(value).split(";")
        if token.strip()
    }


def _append_warning_reason(existing: Any, new_reason: str) -> str:
    reasons = [
        token.strip()
        for token in str(existing).split(";")
        if token.strip()
    ]
    if new_reason not in reasons:
        reasons.append(new_reason)
    return ";".join(reasons)


def _psf_width_band_match(
    sigma_x: float,
    sigma_y: float,
    *,
    lower: float = 6.85,
    upper: float = 7.2,
) -> bool:
    return bool(
        np.isfinite(sigma_x)
        and np.isfinite(sigma_y)
        and float(lower) <= float(sigma_x) <= float(upper)
        and float(lower) <= float(sigma_y) <= float(upper)
    )


def _relabel_accepted_detections(
    detections: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    relabeled = [dict(det) for det in sorted(detections, key=lambda item: item["row"])]
    for idx, det in enumerate(relabeled, start=1):
        det["label"] = f"ion_{idx:02d}"
        det["order_top_to_bottom"] = idx
    return relabeled


def _select_strongest_detections(
    detections: list[dict[str, Any]],
    keep_count: int,
) -> list[dict[str, Any]]:
    strongest = sorted(
        detections,
        key=lambda det: float(det.get("matched_snr", float("-inf"))),
        reverse=True,
    )[:keep_count]
    return _relabel_accepted_detections(strongest)


def _select_strong_relative_to_peak(
    detections: list[dict[str, Any]],
    *,
    relative_floor: float,
    absolute_floor: float,
) -> list[dict[str, Any]]:
    if not detections:
        return []

    strongest_snr = max(
        float(det.get("matched_snr", float("-inf")))
        for det in detections
    )
    snr_floor = max(float(absolute_floor), float(relative_floor) * strongest_snr)
    selected = [
        det
        for det in detections
        if float(det.get("matched_snr", float("-inf"))) >= snr_floor
    ]
    return _relabel_accepted_detections(selected)


def _select_strongest_detections_by_row_cluster(
    detections: list[dict[str, Any]],
    *,
    merge_gap_px: float,
) -> list[dict[str, Any]]:
    if not detections:
        return []

    ordered = sorted(detections, key=lambda det: float(det["row"]))
    clusters: list[list[dict[str, Any]]] = [[ordered[0]]]
    for det in ordered[1:]:
        if float(det["row"]) - float(clusters[-1][-1]["row"]) > float(merge_gap_px):
            clusters.append([det])
        else:
            clusters[-1].append(det)

    strongest_by_cluster = [
        max(
            cluster,
            key=lambda det: float(det.get("matched_snr", float("-inf"))),
        )
        for cluster in clusters
    ]
    return _relabel_accepted_detections(strongest_by_cluster)


def _apply_gaussian_warning_count_correction(
    accepted: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    variant_summary: dict[str, Any],
    regime_label: str,
    cfg: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Apply narrow manual-review-backed Gaussian count corrections.

    The widened scored ground-truth rows expose a narrow family of Gaussian
    overcounts in compressed-or-artifact frames. We correct only those local
    ambiguity patterns, keeping the warning public and leaving the global
    routing policy unchanged.
    """
    if str(variant_summary.get("noise_model", "")) != "gaussian":
        return accepted, variant_summary

    legacy_gaussian_warning_count_corrections_enabled = bool(
        (cfg or {}).get("enable_gaussian_warning_count_corrections", False)
    )

    if regime_label not in {"compressed_or_artifact", "over_dispersed"}:
        return accepted, variant_summary
    if not legacy_gaussian_warning_count_corrections_enabled:
        return accepted, variant_summary

    def refresh_context(
        current_accepted: list[dict[str, Any]],
        current_summary: dict[str, Any],
    ) -> dict[str, Any]:
        count_diagnostics = dict(current_summary.get("count_diagnostics", {}))
        score_admissibility = dict(current_summary.get("score_admissibility", {}))
        visible_ion_count = int(
            current_summary.get("visible_ion_count", len(current_accepted))
        )
        warning_tokens = _warning_reason_tokens(
            current_summary.get("manual_review_warning_reason", "")
        )
        sigma_x = float(current_summary.get("sigma_x", float("nan")))
        sigma_y = float(current_summary.get("sigma_y", float("nan")))
        state = current_summary.get("state", {})
        axial_spacing_px_spatial = float(
            state.get("axial_spacing_px_spatial", float("nan"))
        )
        weakest_accepted_snr = float(
            count_diagnostics.get("weakest_accepted_snr", float("nan"))
        )
        nearest_boundary_margin = float(
            count_diagnostics.get("nearest_boundary_margin", float("nan"))
        )
        accepted_snrs = [
            float(value)
            for value in current_summary.get("accepted_matched_snrs", [])
            if np.isfinite(value)
        ]
        rejected_snrs = sorted(
            (
                float(value)
                for value in current_summary.get("rejected_matched_snrs", [])
                if np.isfinite(value)
            ),
            reverse=True,
        )
        strongest_accepted_snr = (
            float(max(accepted_snrs)) if accepted_snrs else float("nan")
        )
        strongest_rejected_snr = float(
            count_diagnostics.get("strongest_rejected_snr", float("nan"))
        )
        second_strongest_rejected_snr = (
            float(rejected_snrs[1]) if len(rejected_snrs) >= 2 else float("nan")
        )
        delta_tau_v = float(
            score_admissibility.get("decision_threshold_lift", 0.0)
        )
        return {
            "count_diagnostics": count_diagnostics,
            "score_admissibility": score_admissibility,
            "visible_ion_count": visible_ion_count,
            "warning_tokens": warning_tokens,
            "sigma_x": sigma_x,
            "sigma_y": sigma_y,
            "width_band_match": _psf_width_band_match(
                sigma_x,
                sigma_y,
                upper=7.25,
            ),
            "wide_artifact_width_band_match": _psf_width_band_match(
                sigma_x,
                sigma_y,
                lower=6.75,
                upper=7.25,
            ),
            "axial_spacing_px_spatial": axial_spacing_px_spatial,
            "weakest_accepted_snr": weakest_accepted_snr,
            "nearest_boundary_margin": nearest_boundary_margin,
            "snr_outlier_flag": bool(count_diagnostics.get("snr_outlier_flag", False)),
            "strongest_accepted_snr": strongest_accepted_snr,
            "strongest_rejected_snr": strongest_rejected_snr,
            "second_strongest_rejected_snr": second_strongest_rejected_snr,
            "snr_minimum_to_next_ratio": float(
                count_diagnostics.get("snr_minimum_to_next_ratio", float("nan"))
            ),
            "snr_minimum_to_next_log_ratio": float(
                count_diagnostics.get("snr_minimum_to_next_log_ratio", float("nan"))
            ),
            "strongest_accepted_to_threshold_linear_ratio": float(
                count_diagnostics.get(
                    "strongest_accepted_to_threshold_linear_ratio",
                    float("nan"),
                )
            ),
            "strongest_accepted_to_threshold_log_ratio": float(
                count_diagnostics.get(
                    "strongest_accepted_to_threshold_log_ratio",
                    float("nan"),
                )
            ),
            "weakest_accepted_to_threshold_linear_ratio": float(
                count_diagnostics.get(
                    "weakest_accepted_to_threshold_linear_ratio",
                    float("nan"),
                )
            ),
            "weakest_accepted_to_threshold_log_ratio": float(
                count_diagnostics.get(
                    "weakest_accepted_to_threshold_log_ratio",
                    float("nan"),
                )
            ),
            "strongest_rejected_to_threshold_linear_ratio": float(
                count_diagnostics.get(
                    "strongest_rejected_to_threshold_linear_ratio",
                    float("nan"),
                )
            ),
            "strongest_rejected_to_threshold_log_ratio": float(
                count_diagnostics.get(
                    "strongest_rejected_to_threshold_log_ratio",
                    float("nan"),
                )
            ),
            "score_reference_applied": bool(
                score_admissibility.get("reference_applied", False)
            ),
            "delta_tau_v": delta_tau_v,
        }

    working_accepted = accepted
    working_summary = variant_summary
    current = refresh_context(working_accepted, working_summary)

    def apply_correction(
        corrected_accepted: list[dict[str, Any]],
        *,
        correction_reason: str,
        warning_reason: str,
        corrected_rejected: list[dict[str, Any]] | None = None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        corrected_summary = dict(working_summary)
        corrected_warning_reason = _append_warning_reason(
            working_summary.get("manual_review_warning_reason", ""),
            warning_reason,
        )
        corrected_state = state_metrics(corrected_accepted)
        tau_v_star = float(
            current["count_diagnostics"].get("decision_threshold", float("nan"))
        )
        corrected_count_diagnostics = count_decision_metrics(
            corrected_accepted,
            rejected if corrected_rejected is None else corrected_rejected,
            tau_v_star,
        )
        corrected_count_diagnostics["manual_review_warning"] = True
        corrected_count_diagnostics["manual_review_warning_reason"] = (
            corrected_warning_reason
        )
        corrected_count_diagnostics["count_correction_applied"] = True
        corrected_count_diagnostics["count_correction_reason"] = correction_reason
        corrected_count_diagnostics["pre_correction_visible_ion_count"] = (
            current["visible_ion_count"]
        )
        corrected_summary.update(
            {
                "visible_ion_count": int(len(corrected_accepted)),
                "state": corrected_state,
                "accepted_matched_snrs": [
                    float(det["matched_snr"]) for det in corrected_accepted
                ],
                "count_diagnostics": corrected_count_diagnostics,
                "manual_review_warning": True,
                "manual_review_warning_reason": corrected_warning_reason,
            }
        )
        return corrected_accepted, corrected_summary

    def promote_strongest_rejected(
        *,
        correction_reason: str,
        warning_reason: str,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        if not rejected:
            return working_accepted, working_summary
        promoted = sorted(
            rejected,
            key=lambda det: float(det.get("matched_snr", float("-inf"))),
            reverse=True,
        )[:1]
        promoted_ids = {id(det) for det in promoted}
        remaining_rejected = [det for det in rejected if id(det) not in promoted_ids]
        return apply_correction(
            _relabel_accepted_detections(promoted),
            correction_reason=correction_reason,
            warning_reason=warning_reason,
            corrected_rejected=remaining_rejected,
        )

    strongest_rejected_detection = (
        max(
            rejected,
            key=lambda det: float(det.get("matched_snr", float("-inf"))),
        )
        if rejected
        else None
    )
    strongest_rejected_profile_prominence = (
        float(
            strongest_rejected_detection.get(
                "profile_prominence",
                float("nan"),
            )
        )
        if strongest_rejected_detection is not None
        else float("nan")
    )

    if (
        current["visible_ion_count"] >= 2
        and len(working_accepted) >= 2
        and np.isfinite(current["weakest_accepted_to_threshold_linear_ratio"])
        and current["weakest_accepted_to_threshold_linear_ratio"] <= 1.05
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.2
        and np.isfinite(current["snr_minimum_to_next_ratio"])
        and current["snr_minimum_to_next_ratio"] <= 1.12
    ):
        return apply_correction(
            [],
            correction_reason=(
                "accepted_set_score_coherence_near_threshold_accepted_set_negation_to_zero"
            ),
            warning_reason=(
                "wide_spacing_two_ion_width_ambiguity"
                if "wide_spacing_two_ion_width_ambiguity" in current["warning_tokens"]
                else "accepted_set_score_coherence_ambiguity"
            ),
        )

    if (
        current["visible_ion_count"] == 2
        and len(working_accepted) >= 2
        and (
            not np.isfinite(current["strongest_rejected_snr"])
            or (
                np.isfinite(
                    current["count_diagnostics"].get(
                        "rejected_margin_to_threshold",
                        float("nan"),
                    )
                )
                and float(
                    current["count_diagnostics"].get(
                        "rejected_margin_to_threshold",
                        float("nan"),
                    )
                ) >= 2.5
            )
        )
        and np.isfinite(current["strongest_accepted_to_threshold_linear_ratio"])
        and current["strongest_accepted_to_threshold_linear_ratio"] <= 2.5
        and np.isfinite(current["weakest_accepted_to_threshold_linear_ratio"])
        and current["weakest_accepted_to_threshold_linear_ratio"] <= (13.0 / 6.0)
        and np.isfinite(current["snr_minimum_to_next_ratio"])
        and current["snr_minimum_to_next_ratio"] <= 1.12
    ):
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 1),
            correction_reason="accepted_set_score_coherence_strongest_single_detection",
            warning_reason=(
                "wide_spacing_two_ion_width_ambiguity"
                if "wide_spacing_two_ion_width_ambiguity" in current["warning_tokens"]
                else "accepted_set_score_coherence_ambiguity"
            ),
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        current["visible_ion_count"] == 2
        and len(working_accepted) >= 2
        and current["snr_outlier_flag"]
    ):
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 1),
            correction_reason="snr_outlier_strongest_single_detection",
            warning_reason="snr_outlier_count_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        current["visible_ion_count"] == 1
        and len(working_accepted) == 1
        and np.isfinite(current["weakest_accepted_to_threshold_linear_ratio"])
        and current["weakest_accepted_to_threshold_linear_ratio"] <= 1.2
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 1.25
    ):
        return apply_correction(
            [],
            correction_reason="accepted_set_threshold_coherence_singleton_negation_to_zero",
            warning_reason=(
                "low_snr_count_width_ambiguity"
                if "low_snr_count_width_ambiguity" in current["warning_tokens"]
                else "accepted_set_threshold_coherence_ambiguity"
            ),
        )

    if (
        current["visible_ion_count"] == 1
        and len(working_accepted) == 1
        and current["score_reference_applied"]
        and current["delta_tau_v"] >= 1.5
        and np.isfinite(current["weakest_accepted_to_threshold_linear_ratio"])
        and current["weakest_accepted_to_threshold_linear_ratio"] <= 1.75
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.65
    ):
        return apply_correction(
            [],
            correction_reason="accepted_set_threshold_reference_singleton_negation_to_zero",
            warning_reason=(
                "low_snr_count_width_ambiguity"
                if "low_snr_count_width_ambiguity" in current["warning_tokens"]
                else "accepted_set_threshold_coherence_ambiguity"
            ),
        )

    if (
        "wide_spacing_two_ion_width_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 2
        and len(working_accepted) >= 2
        and np.isfinite(current["strongest_accepted_to_threshold_linear_ratio"])
        and current["strongest_accepted_to_threshold_linear_ratio"] >= 2.5
        and np.isfinite(current["weakest_accepted_to_threshold_linear_ratio"])
        and current["weakest_accepted_to_threshold_linear_ratio"] <= 1.05
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.5
    ):
        return apply_correction(
            _select_strongest_detections(working_accepted, 1),
            correction_reason="wide_spacing_two_ion_width_ambiguity_strongest_single_detection",
            warning_reason="wide_spacing_two_ion_width_ambiguity",
        )

    alternating_multiplet_artifact = bool(
        not current["warning_tokens"]
        and 4 <= current["visible_ion_count"] <= 5
        and np.isfinite(current["sigma_x"])
        and np.isfinite(current["sigma_y"])
        and 6.35 <= current["sigma_x"] <= 7.0
        and 6.35 <= current["sigma_y"] <= 7.0
        and np.isfinite(current["axial_spacing_px_spatial"])
        and 45.0 <= current["axial_spacing_px_spatial"] <= 65.0
        and np.isfinite(current["strongest_accepted_snr"])
        and current["strongest_accepted_snr"] >= 100.0
    )
    if alternating_multiplet_artifact:
        alternating_strong = _select_strong_relative_to_peak(
            working_accepted,
            relative_floor=0.35,
            absolute_floor=40.0,
        )
        if len(alternating_strong) == 2:
            return apply_correction(
                alternating_strong,
                correction_reason="alternating_multiplet_count_ambiguity_strong_peaks_only",
                warning_reason="alternating_multiplet_count_ambiguity",
            )

    clustered_accepted = _select_strongest_detections_by_row_cluster(
        working_accepted,
        merge_gap_px=85.0,
    )
    if (
        len(clustered_accepted) < len(working_accepted)
        and current["visible_ion_count"] >= 2
        and "wide_spacing_two_ion_width_ambiguity" not in current["warning_tokens"]
        and np.isfinite(current["sigma_x"])
        and np.isfinite(current["sigma_y"])
        and 6.35 <= current["sigma_x"] <= 7.25
        and 6.35 <= current["sigma_y"] <= 7.25
    ):
        working_accepted, working_summary = apply_correction(
            clustered_accepted,
            correction_reason="row_cluster_count_ambiguity_strongest_per_cluster",
            warning_reason="row_cluster_count_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        "row_cluster_count_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 3
        and current["snr_outlier_flag"]
        and np.isfinite(current["axial_spacing_px_spatial"])
        and current["axial_spacing_px_spatial"] >= 90.0
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 7.5
    ):
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 2),
            correction_reason="row_cluster_count_ambiguity_strongest_two_detection",
            warning_reason="row_cluster_count_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        "row_cluster_count_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 2
        and len(working_accepted) >= 2
        and np.isfinite(current["axial_spacing_px_spatial"])
        and current["axial_spacing_px_spatial"] >= 150.0
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 10.0
    ):
        return apply_correction(
            _select_strongest_detections(working_accepted, 1),
            correction_reason="row_cluster_count_ambiguity_strongest_single_detection",
            warning_reason="row_cluster_count_ambiguity",
        )

    if (
        current["visible_ion_count"] == 0
        and not working_accepted
        and rejected
        and current["width_band_match"]
        and current["score_reference_applied"]
        and current["delta_tau_v"] >= 1.5
        and np.isfinite(current["strongest_rejected_snr"])
        and current["strongest_rejected_snr"] >= 8.0
        and np.isfinite(current["second_strongest_rejected_snr"])
        and (
            current["strongest_rejected_snr"]
            - current["second_strongest_rejected_snr"]
        ) >= 1.5
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 1.8
        and np.isfinite(strongest_rejected_profile_prominence)
        and strongest_rejected_profile_prominence >= 12.0
    ):
        return promote_strongest_rejected(
            correction_reason="manual_calibrated_dominant_singleton_recovery_from_rejected_peak",
            warning_reason="manual_calibrated_singleton_recovery_ambiguity",
        )

    if (
        current["visible_ion_count"] == 3
        and len(working_accepted) >= 3
        and current["width_band_match"]
        and np.isfinite(current["axial_spacing_px_spatial"])
        and 55.0 <= current["axial_spacing_px_spatial"] <= 80.0
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 9.0
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 2.2
        and np.isfinite(current["strongest_accepted_snr"])
        and current["strongest_accepted_snr"] <= 45.0
    ):
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 2),
            correction_reason="wide_spacing_two_ion_width_ambiguity_prepare_two_peak_set",
            warning_reason="wide_spacing_two_ion_width_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        "wide_spacing_two_ion_width_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 1
        and len(working_accepted) == 1
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 7.0
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.8
    ):
        return apply_correction(
            [],
            correction_reason="wide_spacing_two_ion_width_ambiguity_near_threshold_accepted_set_negation_to_zero",
            warning_reason="wide_spacing_two_ion_width_ambiguity",
        )

    low_snr_multiplet_negation_to_zero = bool(
        "low_snr_count_width_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] >= 2
        and len(working_accepted) >= 2
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 6.3
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.2
    )
    if low_snr_multiplet_negation_to_zero:
        return apply_correction(
            [],
            correction_reason="low_snr_count_width_ambiguity_near_threshold_accepted_set_negation_to_zero",
            warning_reason="low_snr_count_width_ambiguity",
        )

    low_snr_width_ambiguity = bool(
        current["width_band_match"]
        and 2 <= current["visible_ion_count"] <= 3
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 10.5
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 3.6
        and (
            not np.isfinite(current["axial_spacing_px_spatial"])
            or current["axial_spacing_px_spatial"] <= 50.0
        )
    )
    if low_snr_width_ambiguity and len(working_accepted) >= 2:
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 1),
            correction_reason="low_snr_count_width_ambiguity_strongest_single_detection",
            warning_reason="low_snr_count_width_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    if (
        "low_snr_count_width_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 1
        and len(working_accepted) == 1
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 8.5
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 1.25
    ):
        return apply_correction(
            [],
            correction_reason="low_snr_count_width_ambiguity_near_threshold_accepted_set_negation_to_zero",
            warning_reason="low_snr_count_width_ambiguity",
        )

    if (
        "low_snr_count_width_ambiguity" in current["warning_tokens"]
        and current["visible_ion_count"] == 1
        and len(working_accepted) == 1
        and current["score_reference_applied"]
        and current["delta_tau_v"] >= 1.5
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 10.5
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 0.65
    ):
        return apply_correction(
            [],
            correction_reason="manual_calibrated_low_snr_singleton_negation_to_zero",
            warning_reason="low_snr_count_width_ambiguity",
        )

    wide_spacing_three_ion = bool(
        current["visible_ion_count"] == 3
        and len(working_accepted) >= 3
        and np.isfinite(current["axial_spacing_px_spatial"])
        and 55.0 <= current["axial_spacing_px_spatial"] <= 70.0
        and np.isfinite(current["sigma_x"])
        and current["sigma_x"] < 6.75
        and np.isfinite(current["sigma_y"])
        and current["sigma_y"] < 6.75
    )
    if wide_spacing_three_ion:
        working_accepted, working_summary = apply_correction(
            _select_strongest_detections(working_accepted, 2),
            correction_reason="wide_spacing_three_ion_width_ambiguity_strongest_two_detection",
            warning_reason="wide_spacing_three_ion_width_ambiguity",
        )
        current = refresh_context(working_accepted, working_summary)

    wide_spacing_multi_peak_artifact = bool(
        current["visible_ion_count"] >= 2
        and len(working_accepted) >= 2
        and not current["warning_tokens"]
        and current["wide_artifact_width_band_match"]
        and np.isfinite(current["axial_spacing_px_spatial"])
        and 55.0 <= current["axial_spacing_px_spatial"] <= 400.0
        and np.isfinite(current["weakest_accepted_snr"])
        and current["weakest_accepted_snr"] <= 7.3
        and np.isfinite(current["nearest_boundary_margin"])
        and current["nearest_boundary_margin"] <= 1.2
        and np.isfinite(current["strongest_accepted_snr"])
        and current["strongest_accepted_snr"] <= 9.0
    )
    if wide_spacing_multi_peak_artifact:
        return apply_correction(
            [],
            correction_reason="wide_spacing_multi_peak_artifact_near_threshold_accepted_set_negation_to_zero",
            warning_reason="wide_spacing_multi_peak_artifact_ambiguity",
        )

    return working_accepted, working_summary


def _background_tile_response_noise_std(
    dark_tiles: list[np.ndarray] | None,
    prefilter_choice: dict[str, Any],
    sigma_x: float,
    sigma_y: float,
    cfg: dict[str, Any],
    kernel: np.ndarray | None = None,
    prepared_tiles: list[np.ndarray] | None = None,
) -> float:
    """Estimate matched-response noise from Stage 1 background-only tiles.

    Using the darkest background tiles avoids contaminating the Stage 5 noise
    estimate with real ion signal, which otherwise biases matched-SNR values
    downward as ion count or amplitude increases.
    """
    if not dark_tiles:
        return float("nan")

    response_samples: list[np.ndarray] = []
    if prepared_tiles is None:
        prepared_tiles = []
        for tile in dark_tiles:
            if tile is None or np.size(tile) == 0:
                continue
            prepared_tiles.append(
                _prepare_background_bandpass_tile(
                    np.asarray(tile, dtype=np.float64),
                    prefilter_choice,
                    cfg,
                )
            )

    for bandpass_tile in prepared_tiles:
        response_tile, _ = matched_filter_response(
            bandpass_tile,
            sigma_x,
            sigma_y,
            kernel=kernel,
        )
        if response_tile.size:
            response_samples.append(response_tile.ravel())

    if not response_samples:
        return float("nan")
    return robust_std(np.concatenate(response_samples))


def _prepare_background_bandpass_tile(
    tile: np.ndarray,
    prefilter_choice: dict[str, Any],
    cfg: dict[str, Any],
) -> np.ndarray:
    """Run one Stage 1 background tile through the corrected-image Stage 3/4 chain."""
    tile_f64 = np.asarray(tile, dtype=np.float64)
    centered_tile = tile_f64 - float(np.median(tile_f64))
    filtered_tile = apply_prefilter(centered_tile, prefilter_choice)
    return compute_bandpass(filtered_tile, cfg)


def _select_response_operator(
    regime: dict[str, Any],
    working_image_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the Stage 5 response-operator metadata for the current frame."""
    evidence = regime.get("evidence", {})
    structured_score = float(evidence.get("structured_score", 0.0))
    structured_candidate = bool(np.isfinite(structured_score) and structured_score >= 0.5)
    working_basis = str((working_image_metadata or {}).get("working_image_basis", "unknown"))
    return {
        "selected_response": "white",
        "structured_candidate": structured_candidate,
        "structured_response_available": False,
        "reason": "corrected_image_white_response",
        "working_image_basis": working_basis,
    }


def _build_response_maps(
    bandpass_roi: np.ndarray,
    sigma_x: float,
    sigma_y: float,
    *,
    kernel: np.ndarray | None = None,
    response_operator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build explicit Stage 5 response maps while keeping white response controlling."""
    white_response, matched_kernel = matched_filter_response(
        bandpass_roi,
        sigma_x,
        sigma_y,
        kernel=kernel,
    )
    operator_metadata = dict(response_operator or {})
    selected_response_name = str(
        operator_metadata.get("selected_response", "white")
    )
    return {
        "white_response": white_response,
        "selected_response": white_response,
        "selected_response_name": selected_response_name,
        "matched_kernel": matched_kernel,
        "metadata": operator_metadata,
    }


def _shape_variant_detection(
    ps: PipelineState,
    sigma_x: float,
    sigma_y: float,
    *,
    roi_raw: np.ndarray | None = None,
    bandpass_roi: np.ndarray | None = None,
    prepared_dark_tiles: list[np.ndarray] | None = None,
) -> dict[str, Any]:
    """Run the shared Stage 5 detection flow for one template shape family."""
    assert ps.bandpass_roi is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."
    assert ps.roi_raw is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."

    working_roi_raw = ps.roi_raw if roi_raw is None else np.asarray(roi_raw, dtype=np.float64)
    working_bandpass_roi = (
        ps.bandpass_roi
        if bandpass_roi is None
        else np.asarray(bandpass_roi, dtype=np.float64)
    )

    response_operator = _select_response_operator(
        ps.regime,
        ps.working_image_metadata,
    )
    response_maps = _build_response_maps(
        working_bandpass_roi,
        sigma_x,
        sigma_y,
        response_operator=response_operator,
    )
    response_roi = np.asarray(response_maps["selected_response"], dtype=np.float64)
    matched_kernel = np.asarray(response_maps["matched_kernel"], dtype=np.float64)

    pass1_col = ps.corridor.get("pass1_chain_col")
    corridor = detect_chain_corridor(response_roi, ps.roi_bounds, ps.cfg)
    if pass1_col is not None:
        drift = abs(corridor["chain_col"] - pass1_col)
        corridor["corridor_drift_px"] = int(drift)
        corridor["pass1_chain_col"] = int(pass1_col)
    corridor["response_operator"] = str(
        response_maps["metadata"].get("selected_response", "white")
    )

    bc0, bc1 = corridor["band_col_bounds_local"]
    response_band = response_roi[:, bc0:bc1]
    gaussian_noise_std = _background_tile_response_noise_std(
        ps.background.get("dark_tiles"),
        ps.prefilter_choice,
        sigma_x,
        sigma_y,
        ps.cfg,
        kernel=matched_kernel,
        prepared_tiles=prepared_dark_tiles,
    )
    if not np.isfinite(gaussian_noise_std) or gaussian_noise_std <= EPS:
        response_noise_values = response_roi[
            np.abs(working_bandpass_roi)
            <= np.quantile(np.abs(working_bandpass_roi), 13 / 20)
        ]
        gaussian_noise_std = robust_std(response_noise_values)

    row_peaks, axial_profile, row_properties = detect_ion_rows(
        response_band, sigma_y, ps.cfg
    )
    r0, _, c0, _ = ps.roi_bounds
    detections_all = refine_detections(
        working_roi_raw,
        response_band,
        row_peaks,
        row_properties,
        bc0,
        (r0, c0),
        gaussian_noise_std,
        sigma_x,
        sigma_y,
        ps.cfg,
    )
    return {
        "response_roi": response_roi,
        "response_band": response_band,
        "matched_kernel": matched_kernel,
        "response_operator_metadata": dict(response_maps["metadata"]),
        "corridor": corridor,
        "gaussian_noise_std": float(gaussian_noise_std),
        "axial_profile": axial_profile,
        "row_peaks": row_peaks,
        "detections_all": detections_all,
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 1 – Background & noise regime
# ═══════════════════════════════════════════════════════════════════════════

def tile_background_stats(
    image: np.ndarray,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Partition the frame into tiles and estimate per-tile noise statistics.

    Returns
    -------
    dict
        Contains:

        - ``means``, ``vars``, ``counts``: per-tile arrays.
        - ``fano_map``: local Fano factor = var / mean.
        - ``fano_factor``: median Fano factor over dim tiles.
        - ``mean_variance_slope``, ``mean_variance_intercept``,
          ``mean_variance_r2``: fitted var = a·mean + b relation.
                - ``uncertainty``: single-frame uncertainty from the tile ensemble
                    and regression fit.
        - ``dark_tiles``: list of the dimmest tile arrays for NPS.
        - ``darkest_patch_*``: higher-order statistics of the dimmest tile.
        - ``hot_pixel_fraction``: fraction of pixels >6σ in the dimmest tile.
    """
    bh, bw = cfg["bg_block_shape"]
    h, w = image.shape

    if h < 32 or w < 32:
        raise ValueError(
            f"Image is too small ({h}×{w} px) for background tile analysis; "
            "both dimensions must be at least 32 pixels."
        )

    # Adapt tile size so that at least 8 tiles span each image dimension, up
    # to the configured maximum.  A fixed 64-px tile on a narrow image (e.g.
    # 150 px wide) leaves only two tile columns, both of which can overlap the
    # ion-chain corridor, forcing noise to be sampled from signal-contaminated
    # regions.  Scaling the tile down ensures at least one tile column lies
    # entirely outside the corridor.  Minimum tile size is 32 px so the NPS
    # frequency grid remains usable.
    eff_bh = max(32, min(bh, h // 8))
    eff_bw = max(32, min(bw, w // 8))
    bh, bw = eff_bh, eff_bw

    h2, w2 = (h // bh) * bh, (w // bw) * bw
    tiles = _view_as_non_overlapping_blocks_2d(image[:h2, :w2], (bh, bw))
    grid_h, grid_w = tiles.shape[:2]

    means = np.full((grid_h, grid_w), np.nan, dtype=np.float64)
    vars_ = np.full((grid_h, grid_w), np.nan, dtype=np.float64)
    counts = np.zeros((grid_h, grid_w), dtype=np.int32)

    for row in range(grid_h):
        for col in range(grid_w):
            mean, var, count = sigma_clip_stats(
                tiles[row, col],
                sigma=cfg["sigma_clip"],
                max_iters=cfg["sigma_clip_iters"],
            )
            means[row, col] = mean
            vars_[row, col] = var
            counts[row, col] = count

    finite_mask = np.isfinite(means) & np.isfinite(vars_) & (means > EPS)
    if not np.any(finite_mask):
        raise ValueError(
            "No valid background tiles were found; "
            "image is too small or entirely invalid."
        )

    low_mask = means <= np.nanquantile(
        means[finite_mask], cfg["background_quantile"]
    )
    fit_mask = finite_mask & low_mask
    fit_x = means[fit_mask].ravel()
    fit_y = vars_[fit_mask].ravel()

    if fit_x.size >= 2 and np.ptp(fit_x) > EPS:
        regression = stats.linregress(fit_x, fit_y)
        slope = float(regression.slope)  # type: ignore[attr-defined]
        intercept = float(regression.intercept)  # type: ignore[attr-defined]
        mv_r2 = float(regression.rvalue ** 2)  # type: ignore[attr-defined]
        slope_stderr = float(regression.stderr)  # type: ignore[attr-defined]
        intercept_stderr = float(regression.intercept_stderr)  # type: ignore[attr-defined]
    else:
        slope, intercept, mv_r2 = float("nan"), float("nan"), float("nan")
        slope_stderr, intercept_stderr = float("nan"), float("nan")

    median_mean = float(np.nanmedian(means[finite_mask]))
    median_var = float(np.nanmedian(vars_[finite_mask]))
    fano_map = np.divide(
        vars_,
        np.maximum(means, EPS),
        out=np.full_like(vars_, np.nan),
        where=np.isfinite(vars_),
    )
    fano_samples = fano_map[fit_mask]
    fano_samples = fano_samples[np.isfinite(fano_samples)]
    fano_factor = (
        float(np.nanmedian(fano_samples))
        if fano_samples.size else float("nan")
    )
    fano_stderr = _robust_location_stderr(fano_samples)

    dark_tile_indices = np.argsort(means[finite_mask], axis=None)
    valid_rc = np.argwhere(finite_mask)
    dark_tiles: list[np.ndarray] = []
    darkest_positions: list[tuple[int, int]] = []
    for idx in dark_tile_indices[: cfg["dark_tile_count"]]:
        row, col = valid_rc[idx]
        dark_tiles.append(tiles[row, col].astype(np.float64))
        darkest_positions.append((int(row), int(col)))

    if not darkest_positions:
        raise ValueError(
            "No dark tiles were available for background diagnostics."
        )

    darkest_row, darkest_col = darkest_positions[0]
    darkest_patch = dark_tiles[0]
    patch_flat = darkest_patch.ravel()
    patch_mean = float(np.mean(patch_flat))
    patch_var = float(np.var(patch_flat))
    patch_std = float(np.sqrt(patch_var))
    if patch_std > EPS:
        patch_skew = float(stats.skew(patch_flat, bias=False))
        patch_kurt = float(stats.kurtosis(patch_flat, fisher=True, bias=False))
    else:
        # Skewness and kurtosis are undefined for a constant distribution
        # (the third/fourth central moments are zero but so is sigma³/⁴,
        # making the ratio 0/0 indeterminate).  NaN propagates correctly
        # through classify_noise_regime: NaN < kurtosis_max → False,
        # so tails_ok is conservatively set to False.
        patch_skew = float("nan")
        patch_kurt = float("nan")
    hot_pixel_fraction = float(
        np.mean(patch_flat > patch_mean + cfg["hot_pixel_sigma"] * max(patch_std, EPS))
    )

    return {
        "means": means,
        "vars": vars_,
        "counts": counts,
        "fano_map": fano_map,
        "median_mean": median_mean,
        "median_var": median_var,
        "median_std": float(np.sqrt(max(median_var, 0))),
        "fano_factor": fano_factor,
        "mean_variance_slope": float(slope),
        "mean_variance_intercept": float(intercept),
        "mean_variance_r2": float(mv_r2),
        "uncertainty": {
            "basis": "single_frame_tiles",
            "fit_tile_count": int(fit_x.size),
            "fano_sample_count": int(fano_samples.size),
            "fano_factor_stderr": float(fano_stderr),
            "mean_variance_slope_stderr": float(slope_stderr),
            "mean_variance_intercept_stderr": float(intercept_stderr),
        },
        "dark_tiles": dark_tiles,
        "darkest_patch": darkest_patch,
        "darkest_tile_position": darkest_positions[0],
        "darkest_patch_skewness": patch_skew,
        "darkest_patch_kurtosis": patch_kurt,
        "hot_pixel_fraction": hot_pixel_fraction,
        "trimmed_shape": (int(h2), int(w2)),
        "tile_shape": (int(bh), int(bw)),
        "dark_tile_grid_positions": darkest_positions,
        "darkest_patch_origin": (int(darkest_row * bh), int(darkest_col * bw)),
    }


def stage_background(ps: PipelineState) -> PipelineState:
    """Stage 1: compute tiled background statistics."""
    ps.background = tile_background_stats(ps.image, ps.cfg)
    return ps


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 2 – Noise power spectrum
# ═══════════════════════════════════════════════════════════════════════════

def nps_diagnostics(
    background_patches: Iterable[np.ndarray],
) -> dict[str, Any]:
    """Estimate a mean 2-D noise power spectrum and whiteness metrics.

    The NPS summaries are designed to be compact, interpretable, and sufficient
    to decide whether the background is approximately white (→ Gaussian
    prefilter) or structured/heavy-tailed (→ median prefilter or none).

    Returns
    -------
    dict
        - ``nps_floor``: scalar proxy for the spectral floor.
        - ``whiteness_ratio``: low-frequency power / high-frequency power.
          Values near 1 indicate spatially white noise.
        - ``spectral_flatness``: geometric mean / arithmetic mean of the
          spectrum.  Equals 1 for perfectly white noise.
        - ``directional_anisotropy``: ratio of the larger to smaller
          second moment of the PSD.  Equals 1 for isotropic noise.
    """
    spectra = [windowed_power_spectrum(patch) for patch in background_patches]
    mean_psd = np.mean(spectra, axis=0)
    h, w = mean_psd.shape
    cy, cx = h // 2, w // 2
    row_distance_sq = (np.arange(h, dtype=np.float64) - cy) ** 2
    col_distance_sq = (np.arange(w, dtype=np.float64) - cx) ** 2
    rr = np.sqrt(row_distance_sq[:, None] + col_distance_sq[None, :])
    rr_max = rr.max()

    valid = np.ones_like(mean_psd, dtype=bool)
    valid[cy, cx] = False
    low_mask = valid & (rr <= rr_max / 5)
    high_mask = valid & (rr >= 13 * rr_max / 20)

    positive = np.maximum(mean_psd[valid], EPS)
    low_power = float(np.mean(mean_psd[low_mask]))
    high_power = float(np.mean(mean_psd[high_mask]))
    log_spectral_flatness = _log_positive_mean_ratio(positive)
    spectral_flatness = float(np.exp(log_spectral_flatness))

    total_power = float(np.sum(mean_psd) - mean_psd[cy, cx])
    x_moment = float(
        np.sum(mean_psd * col_distance_sq[None, :]) / max(total_power, EPS)
    )
    y_moment = float(
        np.sum(mean_psd * row_distance_sq[:, None]) / max(total_power, EPS)
    )
    anisotropy = max(x_moment, y_moment) / max(min(x_moment, y_moment), EPS)

    # ── Per-tile diagnostic samples for single-frame uncertainty ──────────
    # Each tile gives an independent (within-frame) realization of the
    # whiteness / flatness / anisotropy diagnostics.  The spread across dark
    # tiles provides a robust single-frame standard error for each metric
    # without any multi-frame pooling.
    per_tile_whiteness: list[float] = []
    per_tile_log_flatness: list[float] = []
    per_tile_log_anisotropy: list[float] = []
    for spec in spectra:
        spec_valid = np.maximum(spec[valid], EPS)
        low_i = float(np.mean(spec[low_mask]))
        high_i = float(np.mean(spec[high_mask]))
        per_tile_whiteness.append(low_i / max(high_i, EPS))
        per_tile_log_flatness.append(_log_positive_mean_ratio(spec_valid))
        tp = float(np.sum(spec) - spec[cy, cx])
        xm = float(np.sum(spec * col_distance_sq[None, :]) / max(tp, EPS))
        ym = float(np.sum(spec * row_distance_sq[:, None]) / max(tp, EPS))
        aniso_i = max(xm, ym) / max(min(xm, ym), EPS)
        per_tile_log_anisotropy.append(float(np.log(max(aniso_i, EPS))))

    whiteness_stderr = _robust_location_stderr(
        np.asarray(per_tile_whiteness, dtype=np.float64)
    )
    log_flatness_stderr = _robust_location_stderr(
        np.asarray(per_tile_log_flatness, dtype=np.float64)
    )
    log_anisotropy_stderr = _robust_location_stderr(
        np.asarray(per_tile_log_anisotropy, dtype=np.float64)
    )

    return {
        "nps_floor": float(np.median(positive)),
        "whiteness_ratio": low_power / max(high_power, EPS),
        "spectral_flatness": spectral_flatness,
        "directional_anisotropy": float(anisotropy),
        "low_frequency_power": low_power,
        "high_frequency_power": high_power,
        "uncertainty": {
            "basis": "single_frame_dark_tiles",
            "tile_count": int(len(spectra)),
            "whiteness_ratio_stderr": float(whiteness_stderr),
            "log_spectral_flatness_stderr": float(log_flatness_stderr),
            "log_directional_anisotropy_stderr": float(log_anisotropy_stderr),
        },
    }


def stage_nps(ps: PipelineState) -> PipelineState:
    """Stage 2: compute noise power spectrum from darkest tiles."""
    ps.nps = nps_diagnostics(ps.background["dark_tiles"])
    ps.regime = classify_noise_regime(ps.background, ps.nps, ps.cfg)
    return ps


def classify_noise_regime(
    background: dict[str, Any],
    nps: dict[str, Any],
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Classify the noise regime from tiled statistics and the NPS.

    This produces a structured set of boolean flags and a human-readable
    regime label.  The flags are consumed by ``choose_prefilter`` and are
    also included in the JSON output so the user can see what regime the
    pipeline identified and whether CRLB / matched-filter assumptions are
    justified.

    Regime flags
    ------------
    poissonish
        Fano factor is close to 1 — consistent with photon-counting noise.
    emccd_like
        Fano factor is close to 2 — consistent with EMCCD excess noise
        factor F² = 2.
    over_dispersed
        Fano factor is well above 2 — likely quantization, structured
        background, or other non-Poisson process.
    tails_ok
        Excess kurtosis of the darkest patch is below the configured
        threshold — the noise distribution does not have heavy tails that
        would defeat a Gaussian-based matched filter.
    whiteish
        The 2-D noise power spectrum is approximately flat (white noise),
        meaning there is no significant spatial correlation or banding.
    mv_slope_physical
        The fitted mean–variance slope is in [0.5, 3.0], consistent with
        a photon-counting or EMCCD detector.  Values far outside this range
        indicate compression or digitization artifacts.

    Parameters
    ----------
    background : dict
        Output of ``tile_background_stats``.
    nps : dict
        Output of ``nps_diagnostics``.
    cfg : dict

    Returns
    -------
    dict
        ``flags`` (dict[str, bool]), ``fano_factor``, ``mv_slope``,
        ``kurtosis``, ``whiteness_ratio``, ``regime_label`` (str).
    """
    fano = background["fano_factor"]
    kurt = background["darkest_patch_kurtosis"]
    slope = background["mean_variance_slope"]
    whiteness = nps["whiteness_ratio"]
    flatness = nps["spectral_flatness"]
    background_uncertainty = background.get("uncertainty", {})
    fano_stderr = float(background_uncertainty.get("fano_factor_stderr", 0.0))
    slope_stderr = float(
        background_uncertainty.get("mean_variance_slope_stderr", 0.0)
    )
    if not np.isfinite(fano_stderr):
        fano_stderr = 0.0
    if not np.isfinite(slope_stderr):
        slope_stderr = 0.0
    anisotropy = float(nps.get("directional_anisotropy", 1.0))
    nps_uncertainty = nps.get("uncertainty", {})

    def _finite_or_zero(value: Any) -> float:
        try:
            v = float(value)
        except (TypeError, ValueError):
            return 0.0
        return v if np.isfinite(v) else 0.0

    whiteness_stderr = _finite_or_zero(
        nps_uncertainty.get("whiteness_ratio_stderr", 0.0)
    )
    log_flatness_stderr = _finite_or_zero(
        nps_uncertainty.get("log_spectral_flatness_stderr", 0.0)
    )
    log_anisotropy_stderr = _finite_or_zero(
        nps_uncertainty.get("log_directional_anisotropy_stderr", 0.0)
    )
    darkest_patch = background.get("darkest_patch")
    patch_size = int(np.size(darkest_patch)) if darkest_patch is not None else 1
    hot_pixel_fraction = float(background.get("hot_pixel_fraction", 0.0))

    poisson_rel = _relative_deviation_to_target(fano, 1.0)
    emccd_rel = _relative_deviation_to_target(fano, 2.0)
    poissonish = (
        poisson_rel < cfg["fano_poisson_tol"]
        and poisson_rel <= emccd_rel
    )
    emccd_like = (
        emccd_rel < cfg["fano_emccd_tol"]
        and emccd_rel < poisson_rel
    )
    over_dispersed = fano > 2.0 * (1.0 + cfg["fano_emccd_tol"])
    tails_ok = kurt < cfg["kurtosis_max"]
    whiteish = cfg["whiteness_lo"] <= whiteness <= cfg["whiteness_hi"]
    slope_poisson_rel = _relative_deviation_to_target(slope, 1.0)
    slope_emccd_rel = _relative_deviation_to_target(slope, 2.0)
    mv_slope_physical = (
        slope_poisson_rel < cfg["fano_poisson_tol"]
        or slope_emccd_rel < cfg["fano_emccd_tol"]
    )

    # Soft evidence is used internally by downstream stages so mixed or
    # boundary-case frames do not need to collapse to one hard regime label.
    whiteness_edge = max((cfg["whiteness_hi"] - cfg["whiteness_lo"]) / 6, 0.05)
    whiteish_score = _soft_band_score(
        whiteness,
        cfg["whiteness_lo"],
        cfg["whiteness_hi"],
        whiteness_edge,
    )
    flatness_score = _soft_step_score(flatness, 0.7, 0.1, direction="above")
    isotropy_score = _soft_step_score(anisotropy, 1.5, 0.2, direction="below")
    white_model_score = _clamp01(
        (whiteish_score + flatness_score + isotropy_score) / 3.0
    )
    structured_score = 1.0 - white_model_score

    tail_scale = max(cfg["kurtosis_max"] / 5, 1.0)
    tails_ok_score = _soft_step_score(
        kurt,
        cfg["kurtosis_max"],
        tail_scale,
        direction="below",
    )
    heavy_tail_score = 1.0 - tails_ok_score

    hot_pixel_limit = hot_pixel_fraction_control_limit(
        patch_size=patch_size,
        sigma_threshold=cfg["hot_pixel_sigma"],
        z_score=cfg["hot_pixel_tail_zscore"],
    )
    hot_pixel_limit = max(hot_pixel_limit, cfg["hot_pixel_fraction_floor"])
    hot_pixel_pressure = _soft_step_score(
        hot_pixel_fraction,
        hot_pixel_limit,
        hot_pixel_limit,
        direction="above",
    )

    fano_precision_score = _soft_step_score(
        fano_stderr,
        0.5 * cfg["fano_poisson_tol"],
        0.5 * cfg["fano_poisson_tol"],
        direction="below",
    )
    slope_precision_score = _soft_step_score(
        slope_stderr,
        0.5 * cfg["fano_poisson_tol"],
        0.5 * cfg["fano_poisson_tol"],
        direction="below",
    )
    whiteness_band = max(cfg["whiteness_hi"] - cfg["whiteness_lo"], EPS)
    whiteness_precision_score = _soft_step_score(
        whiteness_stderr,
        0.25 * whiteness_band,
        0.25 * whiteness_band,
        direction="below",
    )
    flatness_precision_score = _soft_step_score(
        log_flatness_stderr,
        0.25,
        0.25,
        direction="below",
    )
    anisotropy_precision_score = _soft_step_score(
        log_anisotropy_stderr,
        0.25,
        0.25,
        direction="below",
    )
    nps_precision_score = _clamp01(
        (
            whiteness_precision_score
            + flatness_precision_score
            + anisotropy_precision_score
        )
        / 3.0
    )
    measurement_precision_score = _clamp01(
        0.4 * fano_precision_score
        + 0.3 * slope_precision_score
        + 0.3 * nps_precision_score
    )
    measurement_uncertainty_score = 1.0 - measurement_precision_score

    poisson_fano_scale = max(cfg["fano_poisson_tol"], fano_stderr, EPS)
    poisson_slope_scale = max(cfg["fano_poisson_tol"], slope_stderr, EPS)

    poisson_fano_score = _soft_target_score(
        fano,
        1.0,
        poisson_fano_scale,
    )
    poisson_slope_score = _soft_target_score(
        slope,
        1.0,
        poisson_slope_scale,
    )
    photon_counting_raw = (
        np.sqrt(poisson_fano_score * poisson_slope_score)
        * white_model_score
        * tails_ok_score
    )

    emccd_fano_scale = max(2.0 * cfg["fano_emccd_tol"], fano_stderr, EPS)
    emccd_slope_scale = max(2.0 * cfg["fano_emccd_tol"], slope_stderr, EPS)
    emccd_fano_score = _soft_target_score(fano, 2.0, emccd_fano_scale)
    emccd_slope_score = _soft_target_score(slope, 2.0, emccd_slope_scale)
    emccd_raw = (
        np.sqrt(emccd_fano_score * emccd_slope_score)
        * max(white_model_score, 0.5 * flatness_score + 0.5 * isotropy_score)
        * tails_ok_score
    )

    over_fano_score = _soft_step_score(
        fano,
        2.0 * (1.0 + cfg["fano_emccd_tol"]),
        max(cfg["fano_emccd_tol"], fano_stderr, EPS),
        direction="above",
    )
    over_slope_score = _soft_step_score(
        slope,
        2.0 * (1.0 + cfg["fano_emccd_tol"]),
        max(cfg["fano_emccd_tol"], slope_stderr, EPS),
        direction="above",
    )
    over_dispersed_raw = (
        np.sqrt(over_fano_score * max(over_slope_score, 0.25))
        * max(structured_score, 0.25)
        * max(tails_ok_score, 0.25)
    )
    compressed_raw = (
        over_fano_score
        * max(heavy_tail_score, hot_pixel_pressure)
        * max(structured_score, 0.25)
    )

    family_raw = {
        "photon_counting": float(photon_counting_raw),
        "emccd": float(emccd_raw),
        "over_dispersed": float(over_dispersed_raw),
        "compressed_or_artifact": float(compressed_raw),
    }
    dominant_family = max(family_raw, key=lambda k: family_raw[k])
    sorted_family_scores = sorted(family_raw.values(), reverse=True)
    dominant_score = float(sorted_family_scores[0]) if sorted_family_scores else 0.0
    runner_up_score = float(sorted_family_scores[1]) if len(sorted_family_scores) > 1 else 0.0
    ambiguity_uncertainty_score = _clamp01(
        1.0 - dominant_score + 0.5 * runner_up_score
    )
    uncertainty_score = _clamp01(
        0.7 * ambiguity_uncertainty_score
        + 0.3 * measurement_uncertainty_score
    )
    family_scores = _normalize_score_dict(
        {
            **family_raw,
            "mixed": max(uncertainty_score, 0.0),
        }
    )

    # Human-readable summary
    if poissonish and tails_ok and whiteish:
        label = "photon_counting"
    elif emccd_like and tails_ok:
        label = "emccd"
    elif over_dispersed and not tails_ok:
        label = "compressed_or_artifact"
    elif over_dispersed:
        label = "over_dispersed"
    else:
        label = "mixed"

    flags = {
        "poissonish": bool(poissonish),
        "emccd_like": bool(emccd_like),
        "over_dispersed": bool(over_dispersed),
        "tails_ok": bool(tails_ok),
        "whiteish": bool(whiteish),
        "mv_slope_physical": bool(mv_slope_physical),
    }

    return {
        "flags": flags,
        "regime_label": label,
        "fano_factor": float(fano),
        "mean_variance_slope": float(slope),
        "darkest_patch_kurtosis": float(kurt),
        "whiteness_ratio": float(whiteness),
        "spectral_flatness": float(flatness),
        "evidence": {
            "detector_family_scores": family_scores,
            "dominant_detector_family": dominant_family,
            "dominant_score": dominant_score,
            "runner_up_score": runner_up_score,
            "uncertainty_score": uncertainty_score,
            "ambiguity_uncertainty_score": ambiguity_uncertainty_score,
            "measurement_uncertainty_score": measurement_uncertainty_score,
            "measurement_precision_score": measurement_precision_score,
            "measurement_precision_components": {
                "fano_precision": float(_clamp01(fano_precision_score)),
                "slope_precision": float(_clamp01(slope_precision_score)),
                "nps_precision": float(_clamp01(nps_precision_score)),
            },
            "uncertainty_basis": background_uncertainty.get(
                "basis",
                "single_frame_tiles",
            ),
            "fano_factor_stderr": float(fano_stderr),
            "mean_variance_slope_stderr": float(slope_stderr),
            "whiteness_ratio_stderr": float(whiteness_stderr),
            "log_spectral_flatness_stderr": float(log_flatness_stderr),
            "log_directional_anisotropy_stderr": float(log_anisotropy_stderr),
            "nps_precision_score": float(nps_precision_score),
            "whiteish_score": white_model_score,
            "structured_score": structured_score,
            "tails_ok_score": tails_ok_score,
            "heavy_tail_score": heavy_tail_score,
            "hot_pixel_pressure": hot_pixel_pressure,
            "hot_pixel_limit": float(hot_pixel_limit),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 3 – Prefilter
# ═══════════════════════════════════════════════════════════════════════════

def choose_prefilter(
    background: dict[str, Any],
    regime: dict[str, Any],
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Select the mildest spatial prefilter justified by the noise regime.

    The decision is driven by the formal regime flags from
    ``classify_noise_regime`` rather than ad-hoc threshold checks.  This
    ensures the prefilter responds correctly to different detector types:

    - **Photon-counting / EMCCD with clean tails and white noise**:
      a small Gaussian blur reduces pixel noise without biasing ion
      centroids beyond the CRLB floor.
    - **Heavy-tailed or impulsive noise** (hot pixels, outliers):
      a 3×3 median filter suppresses outliers that would otherwise
      dominate the matched-filter response.
    - **Over-dispersed but smooth**: no prefilter — the downstream
      DoG bandpass and matched filter handle separation better than
      a spatial blur that would smear ion-scale structure.

    Parameters
    ----------
    background : dict
        Output of ``tile_background_stats``.
    regime : dict
        Output of ``classify_noise_regime``.
    cfg : dict
        Configuration dict.

    Returns
    -------
    dict
        Keys: ``name`` (``"median3"`` | ``"gaussian"`` | ``"none"``),
        plus filter-specific parameters and a human-readable ``reason``.
    """
    hot_pixels = background["hot_pixel_fraction"]
    evidence = regime.get("evidence", {})
    family_scores = evidence.get("detector_family_scores", {})

    hot_pixel_limit = hot_pixel_fraction_control_limit(
        patch_size=background["darkest_patch"].size,
        sigma_threshold=cfg["hot_pixel_sigma"],
        z_score=cfg["hot_pixel_tail_zscore"],
    )
    hot_pixel_limit = max(hot_pixel_limit, cfg["hot_pixel_fraction_floor"])
    hot_pixel_pressure = evidence.get(
        "hot_pixel_pressure",
        _soft_step_score(
            hot_pixels,
            hot_pixel_limit,
            hot_pixel_limit,
            direction="above",
        ),
    )
    heavy_tail_score = evidence.get(
        "heavy_tail_score",
        0.0 if regime["flags"].get("tails_ok", False) else 1.0,
    )
    white_score = evidence.get(
        "whiteish_score",
        1.0 if regime["flags"].get("whiteish", False) else 0.0,
    )
    structured_score = evidence.get("structured_score", 1.0 - white_score)
    uncertainty_score = evidence.get(
        "uncertainty_score",
        1.0 if regime["regime_label"] == "mixed" else 0.0,
    )
    photon_score = family_scores.get(
        "photon_counting",
        1.0 if regime["flags"].get("poissonish", False) else 0.0,
    )
    emccd_score = family_scores.get(
        "emccd",
        1.0 if regime["flags"].get("emccd_like", False) else 0.0,
    )
    over_score = family_scores.get(
        "over_dispersed",
        1.0 if regime["flags"].get("over_dispersed", False) else 0.0,
    )
    compressed_score = family_scores.get(
        "compressed_or_artifact",
        1.0 if (regime["flags"].get("over_dispersed", False) and not regime["flags"].get("tails_ok", True)) else 0.0,
    )
    measurement_precision_score = evidence.get("measurement_precision_score", 1.0)
    measurement_uncertainty_score = evidence.get(
        "measurement_uncertainty_score",
        1.0 - measurement_precision_score,
    )
    clean_detector_score = max(photon_score, emccd_score)
    impulsive_score = max(heavy_tail_score, hot_pixel_pressure)

    candidate_scores = {
        "median3": _clamp01(
            0.65 * impulsive_score
            + 0.20 * uncertainty_score
            + 0.15 * max(compressed_score, 0.5 * structured_score)
        ),
        "gaussian": _clamp01(
            (
                0.45 * white_score
                + 0.35 * clean_detector_score
                + 0.20 * (1.0 - impulsive_score)
            )
            * (0.5 + 0.5 * measurement_precision_score)
        ),
        "none": _clamp01(
            0.40 * structured_score
            + 0.30 * max(over_score, 0.5 * compressed_score)
            + 0.15 * (1.0 - hot_pixel_pressure)
            + 0.15 * measurement_uncertainty_score
        ),
    }
    selected_name = max(candidate_scores, key=lambda k: candidate_scores[k])

    reasons = {
        "median3": (
            f"Adaptive prefilter scoring favored median suppression because "
            f"impulsive_score={impulsive_score:.2f}, hot_pixels={hot_pixels:.2e}, "
            f"kurtosis={regime['darkest_patch_kurtosis']:.2f}, "
            f"uncertainty={uncertainty_score:.2f}."
        ),
        "gaussian": (
            f"Adaptive prefilter scoring favored mild Gaussian denoising because "
            f"white_score={white_score:.2f}, clean_detector_score={clean_detector_score:.2f}, "
            f"impulsive_score={impulsive_score:.2f}."
        ),
        "none": (
            f"Adaptive prefilter scoring favored no spatial prefilter because "
            f"structured_score={structured_score:.2f}, over_dispersed_score={over_score:.2f}, "
            f"hot_pixel_pressure={hot_pixel_pressure:.2f}."
        ),
    }

    choice: dict[str, Any] = {
        "name": selected_name,
        "reason": reasons[selected_name],
        "score": float(candidate_scores[selected_name]),
        "candidate_scores": {
            key: float(value) for key, value in sorted(candidate_scores.items())
        },
    }
    if selected_name == "median3":
        choice["size"] = int(cfg["median_size"])
    elif selected_name == "gaussian":
        choice["sigma"] = cfg["prefilter_gaussian_sigma"]
    return choice


def apply_prefilter(
    image: np.ndarray,
    choice: dict[str, Any],
) -> np.ndarray:
    """Apply the spatial prefilter selected by ``choose_prefilter``.

    Parameters
    ----------
    image : np.ndarray
        Input image (unmodified).
    choice : dict
        Prefilter descriptor from ``choose_prefilter``.

    Returns
    -------
    np.ndarray
        Filtered image. When no prefilter is selected, this may alias ``image``.
    """
    name = choice["name"]
    if name == "median3":
        return ndimage.median_filter(image, size=int(choice.get("size", 3)))
    if name == "gaussian":
        return _gaussian_filter(image, sigma=float(choice["sigma"]))
    return np.asarray(image)


def stage_prefilter(ps: PipelineState) -> PipelineState:
    """Stage 3: choose and apply the prefilter.

    Uses the regime classification from Stage 2 to drive the decision.
    """
    ps.prefilter_choice = choose_prefilter(ps.background, ps.regime, ps.cfg)
    working_views = _build_working_image_views(
        ps.image,
        ps.background,
        ps.prefilter_choice,
    )
    ps.background_surface = working_views["background_surface"]
    ps.background_rms_surface = working_views["background_rms_surface"]
    ps.corrected_image = working_views["corrected_image"]
    ps.working_image = working_views["working_image"]
    ps.working_image_metadata = dict(working_views["metadata"])
    ps.filtered_image = working_views["filtered_image"]
    return ps


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 4 – Corridor search and PSF estimation
# ═══════════════════════════════════════════════════════════════════════════

def _search_roi_enabled(cfg: dict[str, Any]) -> bool:
    value = cfg.get("enable_search_roi", False)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def central_search_bounds(
    shape: tuple[int, int],
    cfg: dict[str, Any],
) -> tuple[int, int, int, int]:
    """Return Stage 4/5 bounds under the full-frame or explicit ROI policy."""
    rows, cols = shape
    if not _search_roi_enabled(cfg):
        return 0, rows, 0, cols

    rf0, rf1 = cfg["search_row_fraction"]
    cf0, cf1 = cfg["search_col_fraction"]
    r0 = max(0, int(round(rf0 * rows)))
    r1 = min(rows, int(round(rf1 * rows)))
    c0 = max(0, int(round(cf0 * cols)))
    c1 = min(cols, int(round(cf1 * cols)))
    return r0, r1, c0, c1


def compute_bandpass(
    image: np.ndarray,
    cfg: dict[str, Any],
) -> np.ndarray:
    """Compute a difference-of-Gaussians (DoG) bandpass image.

    Subtracting a heavily-blurred copy from a lightly-blurred copy removes
    low-spatial-frequency electrode scatter while preserving ion-scale
    structure.

    Parameters
    ----------
    image : np.ndarray
        Input (prefiltered or raw) image.
    cfg : dict
        Must contain ``dog_small_sigma`` and ``dog_large_sigma``.

    Returns
    -------
    np.ndarray
        Bandpass image (same shape as input).
    """
    if _runtime_gpu_enabled():
        accel_image = _as_accel_array(image)
        small = _gaussian_filter_array(accel_image, cfg["dog_small_sigma"])
        large = _gaussian_filter_array(accel_image, cfg["dog_large_sigma"])
        return _to_host_array(small - large)

    working_image = np.asarray(image, dtype=np.float64)
    small = np.empty_like(working_image, dtype=np.float64)
    large = np.empty_like(working_image, dtype=np.float64)
    ndimage.gaussian_filter(working_image, sigma=cfg["dog_small_sigma"], output=small)
    ndimage.gaussian_filter(working_image, sigma=cfg["dog_large_sigma"], output=large)
    np.subtract(small, large, out=small)
    return small


def detect_chain_corridor(
    image_2d: np.ndarray,
    roi_bounds: tuple[int, int, int, int],
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Return corridor metadata under the full-frame or explicit ROI policy.

    By default Stage 4/5 keep the full column support. When explicit ROI mode
    is enabled, this helper restores the legacy top-k column score and
    half-width corridor restriction.

    Parameters
    ----------
    image_2d : np.ndarray
        Bandpass image or matched-filter response within the Stage 4/5 bounds.
    roi_bounds : (r0, r1, c0, c1)
        Pixel bounds of the Stage 4/5 surface within the full frame.
    cfg : dict
        Retained for compatibility; no config value narrows the returned band.

    Returns
    -------
    dict
        ``chain_col`` (full-frame column), ``band_col_bounds_local``,
        ``band_col_bounds_full``, ``column_score``.
    """
    pos = np.maximum(np.asarray(image_2d, dtype=np.float64), 0.0)
    if pos.ndim != 2 or pos.shape[1] == 0:
        _, _, c0, _ = roi_bounds
        return {
            "local_chain_col": 0,
            "chain_col": int(c0),
            "band_col_bounds_local": (0, 0),
            "band_col_bounds_full": (c0, c0),
            "column_score": np.zeros(0, dtype=np.float64),
        }

    if _search_roi_enabled(cfg):
        topk = max(1, min(int(cfg["column_topk"]), pos.shape[0]))
        top_values = np.partition(pos, -topk, axis=0)[-topk:, :]
        col_score = _gaussian_filter1d(top_values.sum(axis=0), sigma=2)
    else:
        col_score = pos.sum(axis=0)

    local_col = int(np.argmax(col_score))
    _, _, c0, _ = roi_bounds
    full_col = c0 + local_col
    if _search_roi_enabled(cfg):
        half_width = int(cfg["search_half_width"])
        band_c0 = max(0, local_col - half_width)
        band_c1 = min(pos.shape[1], local_col + half_width + 1)
    else:
        band_c0 = 0
        band_c1 = int(pos.shape[1])

    return {
        "local_chain_col": local_col,
        "chain_col": full_col,
        "band_col_bounds_local": (band_c0, band_c1),
        "band_col_bounds_full": (c0 + band_c0, c0 + band_c1),
        "column_score": col_score,
    }


def preliminary_peak_candidates(
    bandpass_band: np.ndarray,
    cfg: dict[str, Any],
) -> list[tuple[int, int, float]]:
    """Find provisional bright spots used *only* for PSF estimation.

    These are not the final ion detections.  They provide sub-patches for
    measuring the local PSF shape before the matched filter is constructed.

    Parameters
    ----------
    bandpass_band : np.ndarray
        Bandpass image cropped to the corridor.
    cfg : dict

    Returns
    -------
    list of (row, col, value)
        Sorted brightest-first.
    """
    threshold = float(
        np.median(bandpass_band)
        + cfg["peak_threshold_sigma"] * robust_std(bandpass_band)
    )
    coords = peak_local_max(
        bandpass_band,
        min_distance=cfg["peak_min_distance"],
        threshold_abs=threshold,
        num_peaks=cfg["max_ions"] * 3,
        exclude_border=False,
    )
    peaks = [
        (int(row), int(col), float(bandpass_band[row, col]))
        for row, col in coords
    ]
    peaks.sort(key=lambda item: item[2], reverse=True)
    return peaks


def estimate_psf_fft(
    mean_patch: np.ndarray,
    nps_floor: float,
    cfg: dict[str, Any],
) -> dict[str, float]:
    """Estimate single-ion PSF widths from the Fourier envelope.

    For a Gaussian emitter the near-DC log power spectrum is approximately

        log P(u, v) ≈ c − 4π² (σ_x² u² + σ_y² v²)

    Weighted least squares is applied so the highest-SNR spectral bins near
    the origin dominate the fit.

    Parameters
    ----------
    mean_patch : np.ndarray
        Background-subtracted mean of several ion sub-patches.
    nps_floor : float
        Median spectral floor from Stage 2.
    cfg : dict

    Returns
    -------
    dict
        ``sigma_x_fft``, ``sigma_y_fft``, ``fft_r2``.
    """
    # Use the local mean-subtracted patch directly here. Unlike the NPS and
    # Stage 6 spectral summaries, this fit is trying to recover the Gaussian
    # envelope of a compact source patch; windowing the patch in real space
    # systematically narrows the inferred PSF on clean synthetic data.
    patch0 = mean_patch - mean_patch.mean()
    spectrum = _fftshift_fft2(patch0)
    power = np.abs(spectrum) ** 2 + EPS
    floor = (
        float(nps_floor)
        if np.isfinite(nps_floor) and nps_floor > 0
        else EPS
    )
    signal_power = np.maximum(power - floor, EPS)

    u_grid, v_grid = shifted_frequency_grids(mean_patch.shape)
    radius = np.sqrt(u_grid**2 + v_grid**2)
    mask = radius <= cfg["psf_r_frac"] * radius.max()
    mask &= power > cfg["psf_cN"] * floor

    if np.count_nonzero(mask) < cfg["psf_min_points"]:
        return {
            "sigma_x_fft": float("nan"),
            "sigma_y_fft": float("nan"),
            "fft_r2": float("nan"),
        }

    x1 = (u_grid[mask] ** 2).ravel()
    x2 = (v_grid[mask] ** 2).ravel()
    y = np.log(signal_power[mask]).ravel()
    design = np.column_stack([x1, x2, np.ones_like(x1)])
    weights = np.sqrt(
        np.maximum(
            signal_power[mask].ravel() / np.max(signal_power[mask]),
            EPS,
        )
    )
    design_w = design * weights[:, None]
    y_w = y * weights
    coeffs, _, _, _ = np.linalg.lstsq(design_w, y_w, rcond=None)
    ax, ay, _ = coeffs

    sigma_x_sq = -ax / (4 * np.pi ** 2) if ax < 0 else float("nan")
    sigma_y_sq = -ay / (4 * np.pi ** 2) if ay < 0 else float("nan")
    sigma_x = (
        float(np.sqrt(sigma_x_sq))
        if np.isfinite(sigma_x_sq) and sigma_x_sq > 0
        else float("nan")
    )
    sigma_y = (
        float(np.sqrt(sigma_y_sq))
        if np.isfinite(sigma_y_sq) and sigma_y_sq > 0
        else float("nan")
    )

    pred = design @ coeffs
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    fft_r2 = 1 - ss_res / max(ss_tot, EPS)

    return {
        "sigma_x_fft": sigma_x,
        "sigma_y_fft": sigma_y,
        "fft_r2": float(fft_r2),
    }


def _build_psf_result(
    *,
    sigma_x_used: float,
    sigma_y_used: float,
    sigma_x_local: float,
    sigma_y_local: float,
    sigma_x_fft: float,
    sigma_y_fft: float,
    fft_r2: float,
    candidate_patch_count: int,
    psf_heuristic_fallback_used: bool,
    psf_diagnostics: dict[str, Any],
    integrated_signal_median: float = float("nan"),
    sigma_x_used_anisotropic: float | None = None,
    sigma_y_used_anisotropic: float | None = None,
    sigma_x_used_symmetric: float | None = None,
    sigma_y_used_symmetric: float | None = None,
) -> dict[str, Any]:
    anisotropic_sx = (
        float(sigma_x_used)
        if sigma_x_used_anisotropic is None
        else float(sigma_x_used_anisotropic)
    )
    anisotropic_sy = (
        float(sigma_y_used)
        if sigma_y_used_anisotropic is None
        else float(sigma_y_used_anisotropic)
    )
    sigma_iso_used = _equivalent_isotropic_sigma(sigma_x_used, sigma_y_used)
    symmetric_sx = (
        sigma_iso_used
        if sigma_x_used_symmetric is None
        else float(sigma_x_used_symmetric)
    )
    symmetric_sy = (
        sigma_iso_used
        if sigma_y_used_symmetric is None
        else float(sigma_y_used_symmetric)
    )
    sigma_iso_local = _equivalent_isotropic_sigma(sigma_x_local, sigma_y_local)
    sigma_iso_fft = _equivalent_isotropic_sigma(sigma_x_fft, sigma_y_fft)
    anisotropy_ratio_fft = (
        float(sigma_y_fft / max(sigma_x_fft, EPS))
        if np.isfinite(sigma_x_fft) and np.isfinite(sigma_y_fft)
        else float("nan")
    )

    return {
        "sigma_x_used": float(sigma_x_used),
        "sigma_y_used": float(sigma_y_used),
        "sigma_x_used_anisotropic": anisotropic_sx,
        "sigma_y_used_anisotropic": anisotropic_sy,
        "sigma_x_used_symmetric": symmetric_sx,
        "sigma_y_used_symmetric": symmetric_sy,
        "sigma_x_local": float(sigma_x_local),
        "sigma_y_local": float(sigma_y_local),
        "sigma_x_fft": float(sigma_x_fft),
        "sigma_y_fft": float(sigma_y_fft),
        "sigma_iso_local": sigma_iso_local,
        "sigma_iso_fft": sigma_iso_fft,
        "sigma_iso_used": sigma_iso_used,
        "anisotropy_ratio_local": float(sigma_y_local / max(sigma_x_local, EPS)),
        "anisotropy_ratio_fft": anisotropy_ratio_fft,
        "anisotropy_ratio_used_anisotropic": float(
            anisotropic_sy / max(anisotropic_sx, EPS)
        ),
        "anisotropy_ratio_used_symmetric": float(
            symmetric_sy / max(symmetric_sx, EPS)
        ),
        "fft_r2": float(fft_r2),
        "candidate_patch_count": int(candidate_patch_count),
        "integrated_signal_median": float(integrated_signal_median),
        "psf_heuristic_fallback_used": bool(psf_heuristic_fallback_used),
        **psf_diagnostics,
    }


def estimate_psf(
    raw_roi: np.ndarray,
    candidate_peaks: list[tuple[int, int, float]],
    nps_floor: float,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Estimate a single-ion PSF from several bright candidate sub-patches.

    The ion chain as a whole is *not* a single Gaussian source, so the PSF
    cannot be estimated from the entire chain ROI.  Instead, the code averages
    small sub-patches around individual provisional peaks and then reconciles
    real-space second moments with the Fourier-envelope fit.

    Parameters
    ----------
    raw_roi : np.ndarray
        Raw (un-bandpassed) ROI image.
    candidate_peaks : list of (row, col, value)
        Provisional peaks from the bandpass corridor.
    nps_floor : float
        Spectral floor from Stage 2.
    cfg : dict

    Returns
    -------
    dict
        ``sigma_x_used``, ``sigma_y_used`` (the reconciled PSF widths),
        plus the individual local and FFT estimates for diagnostics.
    """
    psf_estimation_policy = str(cfg.get("psf_estimation_policy", "production")).lower()
    data_first_policy = psf_estimation_policy == "data_first"
    exemplar_support = select_psf_exemplars(raw_roi, candidate_peaks, cfg)
    selected_peaks = exemplar_support["selected_peaks"]
    radius = int(exemplar_support["effective_radius"])
    patches: list[np.ndarray] = []
    sx_vals: list[float] = []
    sy_vals: list[float] = []
    integrated_signals: list[float] = []

    for row, col, _ in selected_peaks:
        extracted = extract_patch(raw_roi, row, col, radius)
        if extracted is None:
            continue
        patch, _ = extracted
        moments = patch_moments(patch)
        if np.isfinite(moments["sigma_x"]) and np.isfinite(moments["sigma_y"]):
            patches.append(
                np.clip(patch - border_background(patch), 0, None)
            )
            sx_vals.append(moments["sigma_x"])
            sy_vals.append(moments["sigma_y"])
            integrated_signals.append(moments["integrated_signal"])

    fallback_sx = float(cfg["dog_small_sigma"])
    fallback_sy = float(cfg["dog_small_sigma"]) * 3 / 2
    fallback_iso = _equivalent_isotropic_sigma(fallback_sx, fallback_sy)
    exemplar_rows = [int(row) for row, _, _ in selected_peaks]
    exemplar_cols = [int(col) for _, col, _ in selected_peaks]
    psf_diagnostics = {
        "candidate_peak_count": int(exemplar_support["candidate_peak_count"]),
        "psf_exemplar_count": len(selected_peaks),
        "psf_patch_radius": radius,
        "psf_patch_radius_configured": int(exemplar_support["configured_radius"]),
        "psf_patch_radius_reason": str(exemplar_support["selection_reason"]),
        "psf_exemplar_rows": exemplar_rows,
        "psf_exemplar_cols": exemplar_cols,
        "psf_estimation_policy": psf_estimation_policy,
    }

    if not patches:
        if data_first_policy:
            return _build_psf_result(
                sigma_x_used=float("nan"),
                sigma_y_used=float("nan"),
                sigma_x_local=float("nan"),
                sigma_y_local=float("nan"),
                sigma_x_fft=float("nan"),
                sigma_y_fft=float("nan"),
                fft_r2=float("nan"),
                candidate_patch_count=0,
                psf_heuristic_fallback_used=False,
                psf_diagnostics=psf_diagnostics,
                sigma_x_used_anisotropic=float("nan"),
                sigma_y_used_anisotropic=float("nan"),
                sigma_x_used_symmetric=float("nan"),
                sigma_y_used_symmetric=float("nan"),
            )

        # No candidate patches survived extraction.  Fall back to the
        # DoG bandpass scales as a physically motivated prior: the PSF
        # must be narrower than the fine-scale Gaussian (otherwise the
        # bandpass would suppress ion features), so we use
        # dog_small_sigma as the axial width and scale by the typical
        # ion-trap PSF anisotropy ratio σ_y/σ_x ≈ 1.5 (axial extent
        # exceeds radial due to trap geometry).
        return _build_psf_result(
            sigma_x_used=fallback_sx,
            sigma_y_used=fallback_sy,
            sigma_x_local=float("nan"),
            sigma_y_local=float("nan"),
            sigma_x_fft=float("nan"),
            sigma_y_fft=float("nan"),
            fft_r2=float("nan"),
            candidate_patch_count=0,
            psf_heuristic_fallback_used=True,
            psf_diagnostics=psf_diagnostics,
            sigma_x_used_anisotropic=fallback_sx,
            sigma_y_used_anisotropic=fallback_sy,
            sigma_x_used_symmetric=fallback_iso,
            sigma_y_used_symmetric=fallback_iso,
        )

    mean_patch = np.mean(patches, axis=0)
    local_sx = float(np.median(sx_vals))
    local_sy = float(np.median(sy_vals))
    fft_est = estimate_psf_fft(mean_patch, nps_floor, cfg)

    if data_first_policy:
        finite_local = (
            np.isfinite(local_sx)
            and np.isfinite(local_sy)
            and local_sx > 0
            and local_sy > 0
        )
        finite_fft = (
            np.isfinite(fft_est["sigma_x_fft"])
            and np.isfinite(fft_est["sigma_y_fft"])
            and fft_est["sigma_x_fft"] > 0
            and fft_est["sigma_y_fft"] > 0
        )
        if finite_local:
            sx_used = local_sx
            sy_used = local_sy
        elif finite_fft:
            sx_used = float(fft_est["sigma_x_fft"])
            sy_used = float(fft_est["sigma_y_fft"])
        else:
            sx_used = float("nan")
            sy_used = float("nan")
        heuristic_fallback_used = False
    else:
        # When the preliminary-patch PSF is undersampled, it is typically being
        # driven by noise peaks rather than a stable ion image.  In that regime,
        # using the sub-pixel estimate as the matched-filter template creates a
        # spuriously sharp kernel and inflates false positives on synthetic
        # backgrounds.  Fall back to the same DoG-based prior used when no usable
        # patches survive extraction.
        sigma_min = float(cfg["sigma_min_px"])
        undersampled_local = (
            not np.isfinite(local_sx)
            or not np.isfinite(local_sy)
            or local_sx < sigma_min
            or local_sy < sigma_min
        )

        # Reconcile: average the two estimates when the FFT fit is plausible.
        sx_used = fallback_sx if undersampled_local else local_sx
        sy_used = fallback_sy if undersampled_local else local_sy
        if (
            not undersampled_local
            and np.isfinite(fft_est["sigma_x_fft"])
            and 1 / 2 <= fft_est["sigma_x_fft"] / max(local_sx, EPS) <= 2
        ):
            sx_used = (local_sx + fft_est["sigma_x_fft"]) / 2
        if (
            not undersampled_local
            and np.isfinite(fft_est["sigma_y_fft"])
            and 1 / 2 <= fft_est["sigma_y_fft"] / max(local_sy, EPS) <= 2
        ):
            sy_used = (local_sy + fft_est["sigma_y_fft"]) / 2
        heuristic_fallback_used = bool(undersampled_local)

    return _build_psf_result(
        sigma_x_used=sx_used,
        sigma_y_used=sy_used,
        sigma_x_local=local_sx,
        sigma_y_local=local_sy,
        sigma_x_fft=fft_est["sigma_x_fft"],
        sigma_y_fft=fft_est["sigma_y_fft"],
        fft_r2=fft_est["fft_r2"],
        candidate_patch_count=len(patches),
        psf_heuristic_fallback_used=heuristic_fallback_used,
        psf_diagnostics=psf_diagnostics,
        integrated_signal_median=float(np.median(integrated_signals)),
    )


def stage_corridor_and_psf(ps: PipelineState) -> PipelineState:
    """Stage 4: find the chain corridor and estimate the single-ion PSF.

    This is the first of the two corridor-detection passes.  The bandpass
    image is used here because the matched filter has not yet been
    constructed (it requires the PSF, which this stage estimates).

    Requires: stages 1–3 completed (``filtered_image`` and ``nps`` populated).
    """
    assert ps.filtered_image is not None, "Stage 4 requires stage 3 (prefilter) to run first."
    assert ps.corrected_image is not None, "Stage 4 requires stage 3 (working image) to run first."

    r0, r1, c0, c1 = central_search_bounds(ps.image.shape, ps.cfg)
    ps.roi_bounds = (r0, r1, c0, c1)
    ps.roi_raw = ps.image[r0:r1, c0:c1]
    ps.roi_corrected = ps.corrected_image[r0:r1, c0:c1]
    roi_filtered = ps.filtered_image[r0:r1, c0:c1]
    ps.bandpass_roi = compute_bandpass(roi_filtered, ps.cfg)

    # First corridor pass: locate chain column from the bandpass image
    corridor = detect_chain_corridor(ps.bandpass_roi, ps.roi_bounds, ps.cfg)
    ps.corridor = {"pass1_chain_col": corridor["chain_col"]}
    bc0, bc1 = corridor["band_col_bounds_local"]
    bandpass_band = ps.bandpass_roi[:, bc0:bc1]

    # Provisional peaks → PSF sub-patches
    preliminary = preliminary_peak_candidates(bandpass_band, ps.cfg)
    peaks_in_roi = [
        (row, col + bc0, value) for row, col, value in preliminary
    ]
    ps.psf = estimate_psf(
        ps.roi_raw, peaks_in_roi, ps.nps["nps_floor"], ps.cfg
    )

    template_policy = str(ps.cfg.get("psf_template_family", "auto")).lower()
    if template_policy not in {"auto", "anisotropic", "symmetric"}:
        template_policy = "auto"

    anisotropic_sx = ps.psf["sigma_x_used_anisotropic"]
    anisotropic_sy = ps.psf["sigma_y_used_anisotropic"]
    sigma_iso_used = ps.psf["sigma_iso_used"]
    regime_flags = ps.regime.get("flags", {})
    anisotropy_ratio_local = ps.psf.get("anisotropy_ratio_local", float("nan"))
    anisotropy_ratio_fft = ps.psf.get("anisotropy_ratio_fft", float("nan"))
    anisotropy_supported = (
        np.isfinite(anisotropy_ratio_local)
        and np.isfinite(anisotropy_ratio_fft)
        and abs(anisotropy_ratio_fft - anisotropy_ratio_local)
        / max(abs(anisotropy_ratio_local), EPS)
        < ps.cfg["psf_consistency_tol"]
    )

    if bool(regime_flags.get("poissonish", False)):
        regime_basis = "poissonish"
    elif bool(regime_flags.get("emccd_like", False)):
        regime_basis = "emccd_like"
    else:
        regime_basis = "structured_or_unknown"

    if template_policy == "anisotropic":
        template_family = "anisotropic"
        template_reason = "config_forced"
    elif template_policy == "symmetric":
        template_family = "symmetric"
        template_reason = "config_forced"
    elif regime_basis == "poissonish":
        if anisotropy_supported:
            template_family = "anisotropic"
            template_reason = "auto_poisson_anisotropy_supported"
        else:
            template_family = "symmetric"
            template_reason = "auto_poisson_symmetric_fallback"
    elif regime_basis == "emccd_like":
        if anisotropy_supported:
            template_family = "anisotropic"
            template_reason = "auto_emccd_anisotropy_supported"
        else:
            template_family = "symmetric"
            template_reason = "auto_emccd_symmetric_fallback"
    else:
        template_family = "symmetric"
        template_reason = "auto_structured_or_unknown_symmetric"

    if template_family == "symmetric" and np.isfinite(sigma_iso_used):
        ps.psf["sigma_x_used"] = sigma_iso_used
        ps.psf["sigma_y_used"] = sigma_iso_used
        ps.psf["anisotropy_ratio_used"] = 1.0
    else:
        ps.psf["sigma_x_used"] = anisotropic_sx
        ps.psf["sigma_y_used"] = anisotropic_sy
        ps.psf["anisotropy_ratio_used"] = float(
            anisotropic_sy / max(anisotropic_sx, EPS)
        )

    ps.psf["template_family_policy"] = template_policy
    ps.psf["template_family_selected"] = template_family
    ps.psf["template_family_reason"] = template_reason
    ps.psf["template_family_regime_basis"] = regime_basis
    ps.psf["anisotropy_supported"] = anisotropy_supported

    # PSF validity checks — the regime classification is extended here
    # so the JSON output shows whether CRLB assumptions hold.
    sx = ps.psf["sigma_x_used"]
    sy = ps.psf["sigma_y_used"]
    fft_r2 = ps.psf["fft_r2"]
    sigma_min = ps.cfg["sigma_min_px"]
    r2_min = ps.cfg["psf_r2_min"]
    consist_tol = ps.cfg["psf_consistency_tol"]

    psf_sampled = sx > sigma_min and sy > sigma_min
    psf_gaussian = np.isfinite(fft_r2) and fft_r2 > r2_min

    sx_fft = ps.psf["sigma_x_fft"]
    sy_fft = ps.psf["sigma_y_fft"]
    sx_local = ps.psf["sigma_x_local"]
    sy_local = ps.psf["sigma_y_local"]
    if (
        np.isfinite(sx_fft) and np.isfinite(sy_fft)
        and sx_local > EPS and sy_local > EPS
    ):
        rel_x = abs(sx_fft - sx_local) / sx_local
        rel_y = abs(sy_fft - sy_local) / sy_local
        psf_consistent = rel_x < consist_tol and rel_y < consist_tol
    else:
        psf_consistent = False

    ps.regime["flags"]["psf_sampled"] = bool(psf_sampled)
    ps.regime["flags"]["psf_gaussian"] = bool(psf_gaussian)
    ps.regime["flags"]["psf_consistent"] = bool(psf_consistent)

    return ps


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 5 – Matched-filter detection
# ═══════════════════════════════════════════════════════════════════════════

def matched_filter_response(
    bandpass_roi: np.ndarray,
    sigma_x: float,
    sigma_y: float,
    *,
    kernel: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the matched-filter (cross-correlation) response.

    The L2-normalized Gaussian kernel is cross-correlated with the bandpass
    image via ``scipy.signal.fftconvolve``.  Because the kernel is symmetric,
    ``fftconvolve(image, kernel)`` and ``correlate(image, kernel)`` produce
    identical results; the code passes the kernel directly (no flip) for
    clarity.

    Parameters
    ----------
    bandpass_roi : np.ndarray
        Difference-of-Gaussians bandpass image.
    sigma_x, sigma_y : float
        PSF widths from Stage 4.

    Returns
    -------
    (response, kernel) : (np.ndarray, np.ndarray)
    """
    kernel = gaussian_kernel(sigma_x, sigma_y) if kernel is None else np.asarray(kernel, dtype=np.float64)
    # Symmetric kernel → convolution == cross-correlation.
    response = _fftconvolve(bandpass_roi, kernel, mode="same")
    return response, kernel


def detect_ion_rows(
    response_band: np.ndarray,
    sigma_y: float,
    cfg: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Detect axial peaks in the 1-D matched-filter profile.

    The matched filter converts the 2-D search into a cleaner 1-D problem
    along the chain axis.  The minimum distance between peaks is scaled by
    the PSF width so adjacent ions are not double-counted.

    Parameters
    ----------
    response_band : np.ndarray
        Matched-filter response on the unrestricted Stage 5 search surface.
    sigma_y : float
        Axial PSF width [px].
    cfg : dict

    Returns
    -------
    peaks : np.ndarray
        Row indices of detected peaks.
    axial_profile : np.ndarray
        The 1-D profile used for peak finding.
    properties : dict
        ``scipy.signal.find_peaks`` property dict.
    """
    response_band = np.asarray(response_band, dtype=np.float64)
    if response_band.ndim != 2 or response_band.shape[1] == 0:
        axial_profile = np.zeros(response_band.shape[0], dtype=np.float64)
    else:
        # Stage 5 no longer narrows columns before row extraction, so the row
        # activation must preserve the strongest local evidence without a
        # corridor-width dilution penalty.
        axial_profile = _gaussian_filter1d(
            np.max(response_band, axis=1), sigma=1
        )
    profile_sigma = robust_std(axial_profile)
    height = float(
        np.median(axial_profile)
        + cfg["peak_threshold_sigma"] * profile_sigma
    )
    prominence = float(cfg["peak_prominence_sigma"] * profile_sigma)
    distance = int(max(cfg["peak_min_distance"], round(2 * max(sigma_y, 1))))
    peaks, properties = signal.find_peaks(
        axial_profile,
        height=height,
        distance=distance,
        prominence=prominence,
    )

    # Enforce the hard cap: keep only the tallest ``max_ions`` peaks.
    if peaks.size > cfg["max_ions"]:
        order = np.argsort(properties["peak_heights"])[::-1][: cfg["max_ions"]]
        peaks = peaks[order]
        for key, values in properties.items():
            properties[key] = values[order]
        sort_order = np.argsort(peaks)
        peaks = peaks[sort_order]
        for key, values in properties.items():
            properties[key] = values[sort_order]

    return peaks, axial_profile, properties


def refine_detections(
    raw_roi: np.ndarray,
    response_band: np.ndarray,
    row_peaks: np.ndarray,
    row_properties: dict[str, Any],
    band_col_offset: int,
    full_offsets: tuple[int, int],
    response_noise_std: float,
    expected_sigma_x: float | None = None,
    expected_sigma_y: float | None = None,
    cfg: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Refine coarse axial peaks into auditable candidate-ion records.

    For each row peak found in the matched-filter profile, the code searches
    for the locally maximal response inside the corridor, attempts a local
    patch extraction, and then measures centroid, width, and signal metrics.
    Candidates that cannot support a full local patch are retained with an
    explicit failure mode rather than being dropped silently; this preserves a
    complete audit trail for the final ion-count decision.

    Parameters
    ----------
    raw_roi : np.ndarray
        Un-bandpassed ROI.
    response_band : np.ndarray
        Matched-filter response in the corridor.
    row_peaks : np.ndarray
        Row indices from ``detect_ion_rows``.
    row_properties : dict
        Peak properties from ``detect_ion_rows``.
    band_col_offset : int
        Column offset of the corridor band within the ROI.
    full_offsets : (row_offset, col_offset)
        ROI origin in the full frame.
    response_noise_std : float
        Background sigma of the matched-filter response.
    expected_sigma_x, expected_sigma_y : float
        Template widths used for the current detection variant. Candidates
        that are much broader than these template widths are treated as
        diffuse background blobs rather than accepted ion candidates.
    cfg : dict

    Returns
    -------
    list of dict
        One entry per candidate row peak, with spatial labels and either a
        valid local refinement or an explicit rejection precursor.
    """
    cfg = {**DEFAULT_CFG, **(cfg or {})}
    roi_row_offset, roi_col_offset = full_offsets
    radius = effective_local_patch_radius(cfg, row_peaks)
    detections: list[dict[str, Any]] = []

    heights = row_properties.get(
        "peak_heights", np.full(row_peaks.shape, np.nan)
    )
    prominences = row_properties.get(
        "prominences", np.full(row_peaks.shape, np.nan)
    )
    max_width_ratio = float(cfg["candidate_width_max_ratio"])
    sigma_floor = float(cfg["sigma_min_px"])
    # The selected template can be intentionally symmetric or locally
    # undersharp, but the width-veto should never compare candidates against a
    # reference narrower than the detector's own DoG-based ion-shape prior.
    width_reference_x = max(
        float(expected_sigma_x)
        if expected_sigma_x is not None and np.isfinite(expected_sigma_x)
        else 0.0,
        float(cfg["dog_small_sigma"]),
        sigma_floor,
        EPS,
    )
    width_reference_y = max(
        float(expected_sigma_y)
        if expected_sigma_y is not None and np.isfinite(expected_sigma_y)
        else 0.0,
        float(cfg["dog_small_sigma"]) * 3 / 2,
        sigma_floor,
        EPS,
    )

    raw_roi_f64 = np.asarray(raw_roi, dtype=np.float64)
    response_band_f64 = np.asarray(response_band, dtype=np.float64)
    candidate_centers: list[tuple[float, float]] = []
    for peak_row in np.asarray(row_peaks, dtype=np.int64):
        if peak_row < 0 or peak_row >= response_band_f64.shape[0]:
            continue
        peak_col = band_col_offset + int(np.argmax(response_band_f64[peak_row]))
        candidate_centers.append((float(peak_row), float(peak_col)))
    source_mask_radius = max(
        radius,
        int(np.ceil(3.0 * max(width_reference_x, width_reference_y))),
    )
    full_roi_background = source_masked_background_stats(
        raw_roi_f64,
        candidate_centers,
        mask_radius=float(source_mask_radius),
    )

    for index, row_local in enumerate(row_peaks):
        col_local_in_band = int(np.argmax(response_band_f64[row_local]))
        col_local = band_col_offset + col_local_in_band
        matched_value = float(response_band_f64[row_local, col_local_in_band])
        matched_snr = (
            float(matched_value / response_noise_std)
            if response_noise_std > EPS else float("nan")
        )
        extracted = extract_patch_with_fallback(
            raw_roi,
            int(row_local),
            int(col_local),
            radius,
        )
        if extracted is None:
            detections.append({
                "row": float(roi_row_offset + row_local),
                "col": float(roi_col_offset + col_local),
                "matched_response": matched_value,
                "matched_snr": matched_snr,
                "poisson_score": float("nan"),
                "poisson_deviance_improvement": float("nan"),
                "poisson_amplitude_mle": float("nan"),
                "poisson_background_mean": float("nan"),
                "integrated_signal": float("nan"),
                "integrated_snr": float("nan"),
                "local_background_mean": float("nan"),
                "local_background_std": float("nan"),
                "sigma_x_local": float("nan"),
                "sigma_y_local": float("nan"),
                "profile_peak_height": (
                    float(heights[index]) if index < len(heights) else float("nan")
                ),
                "profile_prominence": (
                    float(prominences[index])
                    if index < len(prominences)
                    else float("nan")
                ),
                "requested_refinement_patch_radius": int(radius),
                "effective_refinement_patch_radius": None,
                **candidate_measurement_defaults(),
                "candidate_valid": False,
                "candidate_issue": "patch_out_of_bounds",
            })
            continue

        patch, (r0, r1, c0, c1), effective_radius = extracted
        moments = patch_moments(patch)
        centroid_x = moments["centroid_x"]
        centroid_y = moments["centroid_y"]
        sigma_x = moments["sigma_x"]
        sigma_y = moments["sigma_y"]
        total_signal = moments["integrated_signal"]
        full_row = roi_row_offset + r0 + centroid_y
        full_col = roi_col_offset + c0 + centroid_x
        bg_mean_local, bg_std_local = local_background_stats(
            raw_roi_f64, int(row_local), int(col_local), effective_radius
        )
        background_mean = float(full_roi_background.get("background_mean", float("nan")))
        background_std = float(full_roi_background.get("background_std", float("nan")))
        background_policy = str(full_roi_background.get("background_noise_policy", "source_masked_full_image_sigma_clipped"))
        background_fallback_reason = str(full_roi_background.get("background_fallback_reason", ""))
        if not np.isfinite(background_mean) or not np.isfinite(background_std) or background_std <= EPS:
            background_mean = float(bg_mean_local)
            background_std = float(bg_std_local)
            background_policy = "local_annulus_fallback"
            background_fallback_reason = background_fallback_reason or "invalid_source_masked_background_rms"
        noise_area = background_std * np.sqrt(patch.size)
        integrated_snr = (
            float(total_signal / noise_area)
            if background_std > EPS else float("nan")
        )
        selection_measurements = candidate_measurements(
            patch,
            centroid_x=float(centroid_x),
            centroid_y=float(centroid_y),
            sigma_x=(
                float(expected_sigma_x)
                if expected_sigma_x is not None and np.isfinite(expected_sigma_x)
                else float(sigma_x)
            ),
            sigma_y=(
                float(expected_sigma_y)
                if expected_sigma_y is not None and np.isfinite(expected_sigma_y)
                else float(sigma_y)
            ),
            background_mean=float(background_mean),
            background_std=float(background_std),
        )
        poisson_metrics = poisson_candidate_metrics(
            patch,
            float(bg_mean_local),
            float(centroid_x),
            float(centroid_y),
            float(expected_sigma_x)
            if expected_sigma_x is not None and np.isfinite(expected_sigma_x)
            else float("nan"),
            float(expected_sigma_y)
            if expected_sigma_y is not None and np.isfinite(expected_sigma_y)
            else float("nan"),
            float(total_signal),
        )
        width_ratio_x = float(sigma_x / width_reference_x)
        width_ratio_y = float(sigma_y / width_reference_y)
        candidate_valid = True
        candidate_issue = None
        if (
            not np.isfinite(sigma_x)
            or not np.isfinite(sigma_y)
            or sigma_x <= 0
            or sigma_y <= 0
        ):
            candidate_valid = False
            candidate_issue = "invalid_local_width"
        elif width_ratio_x > max_width_ratio or width_ratio_y > max_width_ratio:
            candidate_valid = False
            candidate_issue = "candidate_broader_than_template"

        detections.append({
            "row": full_row,
            "col": full_col,
            "matched_response": matched_value,
            "matched_snr": matched_snr,
            "poisson_score": float(poisson_metrics["poisson_score"]),
            "poisson_deviance_improvement": float(
                poisson_metrics["poisson_deviance_improvement"]
            ),
            "poisson_amplitude_mle": float(poisson_metrics["poisson_amplitude_mle"]),
            "poisson_background_mean": float(poisson_metrics["poisson_background_mean"]),
            "integrated_signal": float(total_signal),
            "integrated_snr": integrated_snr,
            "local_background_mean": float(bg_mean_local),
            "local_background_std": float(bg_std_local),
            "support_background_mean": float(background_mean),
            "support_background_std": float(background_std),
            "background_noise_policy": background_policy,
            "background_sample_count": int(full_roi_background.get("background_sample_count", 0)),
            "background_masked_fraction": float(full_roi_background.get("background_masked_fraction", float("nan"))),
            "background_fallback_reason": background_fallback_reason,
            "sigma_x_local": sigma_x,
            "sigma_y_local": sigma_y,
            "profile_peak_height": (
                float(heights[index]) if index < len(heights) else float("nan")
            ),
            "profile_prominence": (
                float(prominences[index])
                if index < len(prominences)
                else float("nan")
            ),
            "requested_refinement_patch_radius": int(radius),
            "effective_refinement_patch_radius": int(effective_radius),
            "candidate_width_ratio_x": width_ratio_x,
            "candidate_width_ratio_y": width_ratio_y,
                **selection_measurements,
            "candidate_valid": candidate_valid,
            "candidate_issue": candidate_issue,
        })

    broader_candidates = [
        det for det in detections
        if det.get("candidate_issue") == "candidate_broader_than_template"
        and np.isfinite(det.get("sigma_x_local", float("nan")))
        and np.isfinite(det.get("sigma_y_local", float("nan")))
        and float(det.get("sigma_x_local", 0.0)) > 0
        and float(det.get("sigma_y_local", 0.0)) > 0
    ]
    if broader_candidates:
        adapted_reference_x = max(
            width_reference_x,
            float(np.median([det["sigma_x_local"] for det in broader_candidates])),
        )
        adapted_reference_y = max(
            width_reference_y,
            float(np.median([det["sigma_y_local"] for det in broader_candidates])),
        )

        # If Stage 4 underfit the template width, keep Stage 5 auditable by
        # re-evaluating the veto against the coherent candidate-local widths
        # rather than forcing a zero-count outcome from an undersharp prior.
        for det in detections:
            sigma_x_local = float(det.get("sigma_x_local", float("nan")))
            sigma_y_local = float(det.get("sigma_y_local", float("nan")))
            if (
                not np.isfinite(sigma_x_local)
                or not np.isfinite(sigma_y_local)
                or sigma_x_local <= 0
                or sigma_y_local <= 0
            ):
                continue

            width_ratio_x = float(sigma_x_local / adapted_reference_x)
            width_ratio_y = float(sigma_y_local / adapted_reference_y)
            det["candidate_width_ratio_x"] = width_ratio_x
            det["candidate_width_ratio_y"] = width_ratio_y

            if det.get("candidate_issue") != "candidate_broader_than_template":
                continue
            if width_ratio_x <= max_width_ratio and width_ratio_y <= max_width_ratio:
                det["candidate_valid"] = True
                det["candidate_issue"] = None

    detections.sort(key=lambda item: item["row"])
    for idx, det in enumerate(detections, start=1):
        det["label"] = f"ion_{idx:02d}"
        det["order_top_to_bottom"] = idx
    return detections


SUPPORTED_SELECTION_SCORE_KEYS = stage5_modes.SUPPORTED_MODE_SCORE_KEYS

_SELECTION_SCORE_BASIS = stage5_modes.EXPERIMENTAL_SCORE_BASIS


def _selection_score_key(cfg: dict[str, Any]) -> str:
    raw_key = str(cfg.get("selection_score_key", "matched_snr")).strip() or "matched_snr"
    key = stage5_modes.canonicalize_score_key(raw_key)
    if not stage5_modes.score_key_supported(key):
        raise InputDataError(
            "Unsupported selection_score_key "
            f"{raw_key!r}; expected one of {SUPPORTED_SELECTION_SCORE_KEYS}."
        )
    return key


def _selection_score_threshold(
    cfg: dict[str, Any],
    default_threshold: float,
    *,
    score_key: str,
) -> float:
    if score_key == "matched_snr":
        return float(default_threshold)
    explicit = cfg.get("selection_score_threshold")
    if explicit is None:
        return float(default_threshold)
    try:
        threshold = float(explicit)
    except (TypeError, ValueError):
        return float(default_threshold)
    return float(threshold) if np.isfinite(threshold) else float(default_threshold)


def _selection_score_basis(score_key: str, noise_model: str) -> str:
    score_key = stage5_modes.canonicalize_score_key(score_key)
    if score_key == "matched_snr":
        return "poisson_deviance_sqrt" if noise_model == "poisson" else "gaussian_matched_snr"
    return _SELECTION_SCORE_BASIS[score_key]


def _selection_score_value(det: dict[str, Any], score_key: str) -> float:
    canonical_key = stage5_modes.canonicalize_score_key(score_key)
    for candidate_key in (
        canonical_key,
        *stage5_modes.deprecated_aliases_for_score_key(canonical_key),
    ):
        try:
            value = float(det.get(candidate_key, float("nan")))
        except (TypeError, ValueError):
            continue
        if np.isfinite(value):
            return value
    return float("nan")


def _experimental_selection_score_admissibility(
    threshold: float,
) -> dict[str, Any]:
    return {
        "decision_threshold": float(threshold),
        "decision_threshold_base": float(threshold),
        "decision_threshold_lift": 0.0,
        "reference_applied": False,
        "current_log_power_spectrum_peak_to_mean": float("nan"),
        "reference_log_power_spectrum_peak_to_mean": float("nan"),
        "reference_margin_to_threshold": float("nan"),
    }


def _experimental_mode_score_admissibility_matches_reference(
    mode: stage5_modes.Stage5ModeSpec,
    reference: Mapping[str, Any],
) -> tuple[bool, str]:
    if not bool(reference.get("reference_applied", False)):
        return True, ""

    declared_domain = ""
    for rule_key in (
        COUNT_SPECTRAL_SIGNED_THRESHOLD_VERSION,
        COUNT_SPECTRAL_ROBUST_LIFT_VERSION,
    ):
        rule = reference.get(rule_key)
        if isinstance(rule, Mapping):
            declared_domain = str(rule.get("score_domain", "") or "").strip()
            if declared_domain:
                break

    if declared_domain:
        return declared_domain == mode.score_domain, declared_domain

    return mode.score_domain == stage5_modes.SCORE_DOMAIN_SNR_LIKE, ""


def _threshold_change_requires_refilter(
    initial_threshold: float,
    final_threshold: float,
) -> bool:
    initial = float(initial_threshold)
    final = float(final_threshold)
    if not (np.isfinite(initial) and np.isfinite(final)):
        return False
    return not np.isclose(initial, final, rtol=1e-6, atol=1e-6)


def _experimental_mode_eta_cfg(
    cfg: dict[str, Any],
    mode: stage5_modes.Stage5ModeSpec,
) -> dict[str, Any]:
    mode_cfg = dict(cfg)
    if mode.score_admissibility_npz_path not in (None, ""):
        mode_cfg["eta_score_admissibility_npz_path"] = mode.score_admissibility_npz_path
    if mode.variant_count_legibility_npz_path not in (None, ""):
        mode_cfg["eta_variant_count_legibility_npz_path"] = mode.variant_count_legibility_npz_path
    return mode_cfg


def _promote_variant_public_mode(
    variant_summary: dict[str, Any],
    modes: dict[str, dict[str, Any]],
    selected_mode_id: str,
    selection_resolution: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected_mode = dict(modes[selected_mode_id])
    accepted = [dict(det) for det in selected_mode.get("accepted_detections") or []]
    rejected = [dict(det) for det in selected_mode.get("rejected_detections") or []]
    selected_state = state_metrics(accepted)

    score_key = str(selected_mode.get("score_key", "matched_snr") or "matched_snr")
    mode_count_diagnostics = dict(selected_mode.get("count_diagnostics") or {})
    decision_threshold = float(
        mode_count_diagnostics.get(
            "decision_threshold",
            (variant_summary.get("count_diagnostics") or {}).get(
                "decision_threshold",
                float("nan"),
            ),
        )
    )
    count_diagnostics = count_decision_metrics(
        accepted,
        rejected,
        decision_threshold,
        selection_score_key=score_key,
    )
    count_diagnostics.update(mode_count_diagnostics)
    count_diagnostics.setdefault("selection_score_key", score_key)
    count_diagnostics.setdefault("weakest_accepted_selection_score", count_diagnostics.get("weakest_accepted_score", float("nan")))
    count_diagnostics.setdefault("strongest_rejected_selection_score", count_diagnostics.get("strongest_rejected_score", float("nan")))
    count_diagnostics.setdefault("weakest_accepted_snr", count_diagnostics.get("weakest_accepted_score", float("nan")))
    count_diagnostics.setdefault("strongest_rejected_snr", count_diagnostics.get("strongest_rejected_score", float("nan")))
    count_diagnostics["selected_stage5_mode_id"] = str(selected_mode_id)
    count_diagnostics["selected_stage5_mode_score_key"] = score_key
    count_diagnostics["selected_stage5_mode_resolution"] = str(selection_resolution)
    count_diagnostics.update(
        manual_review_warning_metrics(
            visible_ion_count=int(selected_state["visible_ion_count"]),
            weakest_ion_snr=float(selected_state["weakest_ion_snr"]),
            nearest_boundary_margin=float(
                count_diagnostics.get("nearest_boundary_margin", float("nan"))
            ),
            sigma_x=float(variant_summary.get("sigma_x", float("nan"))),
            sigma_y=float(variant_summary.get("sigma_y", float("nan"))),
            axial_spacing_px_spatial=float(selected_state["axial_spacing_px_spatial"]),
        )
    )

    variant_summary["visible_ion_count"] = int(len(accepted))
    variant_summary["state"] = selected_state
    variant_summary["count_diagnostics"] = count_diagnostics
    variant_summary["manual_review_warning"] = bool(
        count_diagnostics.get("manual_review_warning", False)
    )
    variant_summary["manual_review_warning_reason"] = str(
        count_diagnostics.get("manual_review_warning_reason", "")
    )
    variant_summary["candidate_count_total"] = int(len(accepted) + len(rejected))
    variant_summary["accepted_matched_snrs"] = [
        float(det["matched_snr"])
        for det in accepted
        if np.isfinite(det.get("matched_snr", float("nan")))
    ]
    variant_summary["rejected_matched_snrs"] = [
        float(det["matched_snr"])
        for det in sorted(rejected, key=lambda item: item.get("row", 0.0))
        if np.isfinite(det.get("matched_snr", float("nan")))
    ]
    variant_summary["selected_stage5_mode"] = str(selected_mode_id)
    variant_summary["selected_stage5_mode_resolution"] = str(selection_resolution)
    if selected_mode.get("score_admissibility"):
        variant_summary["score_admissibility"] = dict(selected_mode["score_admissibility"])
    return accepted, rejected


def filter_detections(
    detections: list[dict[str, Any]],
    threshold: float,
    *,
    selection_score_key: str = "matched_snr",
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Partition candidate ions into accepted and rejected sets.

    The count decision is intentionally expressed as an explicit threshold on
    ``matched_snr`` rather than being folded into the 1-D peak finder.  This
    makes the model-order decision auditable: every row peak is either
    accepted, or it is preserved in the rejected list with a physically
    interpretable reason.

    Parameters
    ----------
    detections : list of dict
        All candidate ions from ``refine_detections``.
    threshold : float
        Matched-SNR threshold for Stage 5 acceptance.

    Returns
    -------
    (accepted, rejected) : (list[dict], list[dict])
    """
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for det in detections:
        if not det.get("candidate_valid", True):
            det = dict(det)
            det["rejection_reason"] = det.get(
                "candidate_issue", "candidate_refinement_failed"
            )
            det.pop("candidate_valid", None)
            det.pop("candidate_issue", None)
            rejected.append(det)
            continue
        selection_score = _selection_score_value(det, selection_score_key)
        if selection_score >= threshold:
            det = dict(det)
            det.pop("candidate_valid", None)
            det.pop("candidate_issue", None)
            accepted.append(det)
        else:
            det = dict(det)
            det.pop("candidate_valid", None)
            det.pop("candidate_issue", None)
            det["rejection_reason"] = f"{selection_score_key} < {threshold:.2f}"
            rejected.append(det)

    # Re-label after filtering so labels reflect final accepted order
    accepted.sort(key=lambda item: item["row"])
    for idx, det in enumerate(accepted, start=1):
        det["label"] = f"ion_{idx:02d}"
        det["order_top_to_bottom"] = idx

    return accepted, rejected


def count_decision_metrics(
    accepted: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    threshold: float,
    *,
    selection_score_key: str = "matched_snr",
) -> dict[str, Any]:
    """Quantify the exact margin by which the ion count is determined.

    The visible-ion count is the cardinality of the accepted set under the
    deterministic rule ``matched_snr >= threshold``.  This helper reports how
    far the nearest accepted and rejected candidates lie from the boundary so
    that downstream analysis can distinguish a well-separated count decision
    from one that is merely threshold-admissible.

    Parameters
    ----------
    accepted : list of dict
        Accepted candidate ions.
    rejected : list of dict
        Rejected candidate ions.
    threshold : float
        Acceptance threshold in the units of ``selection_score_key``.

    Returns
    -------
    dict
        Exact decision-boundary diagnostics.  Undefined quantities are
        returned as ``NaN`` and later serialized as JSON ``null``.
    """
    tau_v_star = float(threshold)
    accepted_snrs = np.array(
        [_selection_score_value(det, selection_score_key) for det in accepted],
        dtype=np.float64,
    )
    accepted_snrs_sorted = np.sort(accepted_snrs[np.isfinite(accepted_snrs)])

    # Partition rejections by reason. Candidates that failed refinement stay
    # separate from score-threshold rejections so they cannot distort the
    # decision boundary for the active selection statistic.
    snr_rejected: list[dict[str, Any]] = []
    refinement_failed: list[dict[str, Any]] = []
    snr_rejection_prefix = f"{selection_score_key} <"
    for det in rejected:
        reason = det.get("rejection_reason")
        if reason is None:
            if _selection_score_value(det, selection_score_key) < tau_v_star:
                snr_rejected.append(det)
            else:
                refinement_failed.append(det)
        else:
            reason_text = str(reason)
            if reason_text.startswith(snr_rejection_prefix) or f":{snr_rejection_prefix}" in reason_text:
                snr_rejected.append(det)
            else:
                refinement_failed.append(det)
            continue

    snr_rejected_snrs = np.array(
        [_selection_score_value(det, selection_score_key) for det in snr_rejected],
        dtype=np.float64,
    )

    weakest_accepted = (
        float(np.min(accepted_snrs))
        if accepted_snrs.size > 0 else float("nan")
    )
    next_weakest_accepted = (
        float(accepted_snrs_sorted[1])
        if accepted_snrs_sorted.size >= 2 else float("nan")
    )
    strongest_accepted = (
        float(np.max(accepted_snrs))
        if accepted_snrs.size > 0 else float("nan")
    )
    strongest_rejected = (
        float(np.max(snr_rejected_snrs))
        if snr_rejected_snrs.size > 0 else float("nan")
    )
    accepted_margin = (
        weakest_accepted - tau_v_star
        if np.isfinite(weakest_accepted) else float("nan")
    )
    rejected_margin = (
        tau_v_star - strongest_rejected
        if np.isfinite(strongest_rejected) else float("nan")
    )
    accepted_rejected_gap = (
        weakest_accepted - strongest_rejected
        if np.isfinite(weakest_accepted) and np.isfinite(strongest_rejected)
        else float("nan")
    )
    finite_margins = [
        margin for margin in (accepted_margin, rejected_margin)
        if np.isfinite(margin)
    ]
    nearest_boundary_margin = (
        float(min(finite_margins)) if finite_margins else float("nan")
    )
    boundary_defined = bool(finite_margins)
    snr_minimum_to_next_ratio = (
        next_weakest_accepted / weakest_accepted
        if np.isfinite(weakest_accepted)
        and np.isfinite(next_weakest_accepted)
        and weakest_accepted > 0
        else float("nan")
    )
    snr_minimum_to_next_log_ratio = (
        float(np.log(snr_minimum_to_next_ratio))
        if np.isfinite(snr_minimum_to_next_ratio)
        and snr_minimum_to_next_ratio > 0
        else float("nan")
    )
    strongest_accepted_to_threshold_linear_ratio = (
        strongest_accepted / tau_v_star
        if np.isfinite(strongest_accepted)
        and np.isfinite(tau_v_star)
        and tau_v_star > 0
        else float("nan")
    )
    strongest_accepted_to_threshold_log_ratio = (
        float(np.log(strongest_accepted_to_threshold_linear_ratio))
        if np.isfinite(strongest_accepted_to_threshold_linear_ratio)
        and strongest_accepted_to_threshold_linear_ratio > 0
        else float("nan")
    )
    weakest_accepted_to_threshold_linear_ratio = (
        weakest_accepted / tau_v_star
        if np.isfinite(weakest_accepted)
        and np.isfinite(tau_v_star)
        and tau_v_star > 0
        else float("nan")
    )
    weakest_accepted_to_threshold_log_ratio = (
        float(np.log(weakest_accepted_to_threshold_linear_ratio))
        if np.isfinite(weakest_accepted_to_threshold_linear_ratio)
        and weakest_accepted_to_threshold_linear_ratio > 0
        else float("nan")
    )
    strongest_rejected_to_threshold_linear_ratio = (
        strongest_rejected / tau_v_star
        if np.isfinite(strongest_rejected)
        and np.isfinite(tau_v_star)
        and tau_v_star > 0
        else float("nan")
    )
    strongest_rejected_to_threshold_log_ratio = (
        float(np.log(strongest_rejected_to_threshold_linear_ratio))
        if np.isfinite(strongest_rejected_to_threshold_linear_ratio)
        and strongest_rejected_to_threshold_linear_ratio > 0
        else float("nan")
    )
    snr_outlier_minimum_to_next_linear_ratio_threshold = 5.0
    snr_outlier_minimum_to_next_log_ratio_threshold = float(
        np.log(snr_outlier_minimum_to_next_linear_ratio_threshold)
    )
    snr_outlier_flag = bool(
        np.isfinite(weakest_accepted)
        and np.isfinite(next_weakest_accepted)
        and weakest_accepted
        < (
            next_weakest_accepted
            / snr_outlier_minimum_to_next_linear_ratio_threshold
        )
    )

    return {
        "decision_rule": f"{selection_score_key} >= threshold",
        "decision_threshold": tau_v_star,
        "selection_score_key": selection_score_key,
        "candidate_count_total": int(len(accepted) + len(rejected)),
        "accepted_count": int(len(accepted)),
        "rejected_count": int(len(rejected)),
        "snr_rejected_count": int(len(snr_rejected)),
        "refinement_failed_count": int(len(refinement_failed)),
        "strongest_accepted_snr": strongest_accepted,
        "weakest_accepted_snr": weakest_accepted,
        "strongest_rejected_snr": strongest_rejected,
        "strongest_accepted_selection_score": strongest_accepted,
        "weakest_accepted_selection_score": weakest_accepted,
        "strongest_rejected_selection_score": strongest_rejected,
        "accepted_margin_to_threshold": accepted_margin,
        "rejected_margin_to_threshold": rejected_margin,
        "accepted_rejected_gap": accepted_rejected_gap,
        "nearest_boundary_margin": nearest_boundary_margin,
        "boundary_defined": boundary_defined,
        "snr_outlier_flag": snr_outlier_flag,
        "snr_minimum_to_next_ratio": snr_minimum_to_next_ratio,
        "snr_minimum_to_next_log_ratio": snr_minimum_to_next_log_ratio,
        "strongest_accepted_to_threshold_linear_ratio": (
            strongest_accepted_to_threshold_linear_ratio
        ),
        "strongest_accepted_to_threshold_log_ratio": (
            strongest_accepted_to_threshold_log_ratio
        ),
        "weakest_accepted_to_threshold_linear_ratio": (
            weakest_accepted_to_threshold_linear_ratio
        ),
        "weakest_accepted_to_threshold_log_ratio": (
            weakest_accepted_to_threshold_log_ratio
        ),
        "strongest_rejected_to_threshold_linear_ratio": (
            strongest_rejected_to_threshold_linear_ratio
        ),
        "strongest_rejected_to_threshold_log_ratio": (
            strongest_rejected_to_threshold_log_ratio
        ),
        "snr_outlier_minimum_to_next_linear_ratio_threshold": (
            snr_outlier_minimum_to_next_linear_ratio_threshold
        ),
        "snr_outlier_minimum_to_next_log_ratio_threshold": (
            snr_outlier_minimum_to_next_log_ratio_threshold
        ),
    }


def manual_review_warning_metrics(
    *,
    visible_ion_count: int,
    weakest_ion_snr: float,
    nearest_boundary_margin: float,
    sigma_x: float,
    sigma_y: float,
    axial_spacing_px_spatial: float,
) -> dict[str, Any]:
    """Return detector-side warning flags for visually ambiguous count decisions."""
    width_band_match = _psf_width_band_match(sigma_x, sigma_y, lower=6.75, upper=7.3)
    low_snr_small_count = bool(
        width_band_match
        and 1 <= int(visible_ion_count) <= 3
        and np.isfinite(weakest_ion_snr)
        and float(weakest_ion_snr) <= 10.5
        and np.isfinite(nearest_boundary_margin)
        and float(nearest_boundary_margin) <= 1.35
        and (
            not np.isfinite(axial_spacing_px_spatial)
            or float(axial_spacing_px_spatial) <= 50.0
        )
    )
    wide_spacing_two_ion = bool(
        width_band_match
        and int(visible_ion_count) == 2
        and np.isfinite(axial_spacing_px_spatial)
        and 55.0 <= float(axial_spacing_px_spatial) <= 80.0
        and np.isfinite(sigma_x)
        and float(sigma_x) <= 7.05
        and np.isfinite(sigma_y)
        and float(sigma_y) <= 7.05
    )

    reasons: list[str] = []
    if low_snr_small_count:
        reasons.append("low_snr_count_width_ambiguity")
    if wide_spacing_two_ion:
        reasons.append("wide_spacing_two_ion_width_ambiguity")

    return {
        "manual_review_warning": bool(reasons),
        "manual_review_warning_reason": ";".join(reasons),
    }


def stage_detection(ps: PipelineState) -> PipelineState:
    """Stage 5: run matched-filter detection and refine ion positions.

    This is the second corridor-detection pass.  The first pass (Stage 4)
    used the raw bandpass image to locate preliminary peaks for PSF
    estimation.  Now that we have the PSF, we build the matched filter,
    re-detect the corridor on the matched-filter response (which has better
    contrast), and then find and refine individual ions.

    Requires: stage 4 completed (``bandpass_roi``, ``roi_raw``, ``psf``).
    """
    assert ps.bandpass_roi is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."
    assert ps.roi_raw is not None, "Stage 5 requires stage 4 (corridor/PSF) to run first."

    regime_label = str(ps.regime.get("regime_label", "mixed"))
    background_reference_mean = _background_reference_mean(ps.background, ps.image)
    variant_specs = _stage5_variant_specs_for_cfg(ps.psf, ps.cfg, regime_label)

    selected_noise_model = _selected_stage5_noise_model(regime_label)
    selected_variant_name = (
        f"{ps.psf['template_family_selected']}_{selected_noise_model}"
    )
    use_variant_count_legibility = (
        str(ps.cfg.get("eta_mode", "off")).lower() == "manual_calibrated"
        and ps.cfg.get("eta_variant_count_legibility_npz_path") not in (None, "")
    )
    variant_summaries: dict[str, Any] = {}
    accepted_by_variant: dict[str, list[dict[str, Any]]] = {}
    rejected_by_variant: dict[str, list[dict[str, Any]]] = {}
    shape_results_by_variant: dict[str, dict[str, Any]] = {}
    shared_shape_results_by_family: dict[str, dict[str, Any]] = {}
    base_detection_image = np.asarray(ps.image, dtype=np.float64)
    eta_artifacts_ready = _manual_eta_artifact_paths_ready(ps.cfg)
    reconstruction_cache: dict[
        tuple[int, float, float, tuple[tuple[float | None, float | None], ...]],
        dict[str, Any],
    ] = {}
    partition_cache: dict[
        tuple[int, str, float],
        tuple[tuple[int, ...], tuple[tuple[int, str], ...], tuple[int, ...]],
    ] = {}
    prepared_dark_tiles: list[np.ndarray] | None = None
    dark_tiles = ps.background.get("dark_tiles")
    if dark_tiles:
        prepared_dark_tiles = []
        for tile in dark_tiles:
            if tile is None or np.size(tile) == 0:
                continue
            prepared_dark_tiles.append(
                _prepare_background_bandpass_tile(
                    np.asarray(tile, dtype=np.float64),
                    ps.prefilter_choice,
                    ps.cfg,
                )
            )

    for spec in variant_specs:
        canonical_mode = stage5_modes.canonical_mode_for_variant(
            spec.name,
            spec.template_family,
            spec.noise_model,
        )
        variant_record = (
            _manual_eta_variant_record(ps.cfg, spec.name)
            if eta_artifacts_ready else None
        )
        variant_eta_metadata = dict(ps.eta_correction)
        detection_image = base_detection_image
        variant_roi_raw = ps.roi_raw
        variant_bandpass_roi = ps.bandpass_roi
        if use_variant_count_legibility:
            if variant_record is None:
                variant_eta_correction, variant_eta_metadata = (
                    _prepare_variant_count_legibility_correction(
                        ps.image.shape,
                        ps.cfg,
                        spec.name,
                    )
                )
            else:
                variant_eta_correction, variant_eta_metadata = (
                    _prepare_variant_count_legibility_correction(
                        ps.image.shape,
                        ps.cfg,
                        spec.name,
                        variant_payload=variant_record,
                    )
                )
            if _eta_correction_has_effective_signal(variant_eta_correction):
                detection_image, variant_roi_raw, variant_bandpass_roi = (
                    _variant_detection_inputs(ps, variant_eta_correction)
                )
                shape_result = _shape_variant_detection(
                    ps,
                    spec.sigma_x,
                    spec.sigma_y,
                    roi_raw=variant_roi_raw,
                    bandpass_roi=variant_bandpass_roi,
                    prepared_dark_tiles=prepared_dark_tiles,
                )
            else:
                shape_result = shared_shape_results_by_family.get(spec.template_family)
                if shape_result is None:
                    shape_result = _shape_variant_detection(
                        ps,
                        spec.sigma_x,
                        spec.sigma_y,
                        roi_raw=variant_roi_raw,
                        bandpass_roi=variant_bandpass_roi,
                        prepared_dark_tiles=prepared_dark_tiles,
                    )
                    shared_shape_results_by_family[spec.template_family] = shape_result
        else:
            shape_result = shared_shape_results_by_family.get(spec.template_family)
            if shape_result is None:
                shape_result = _shape_variant_detection(
                    ps,
                    spec.sigma_x,
                    spec.sigma_y,
                    roi_raw=variant_roi_raw,
                    bandpass_roi=variant_bandpass_roi,
                    prepared_dark_tiles=prepared_dark_tiles,
                )
                shared_shape_results_by_family[spec.template_family] = shape_result
        shape_results_by_variant[spec.name] = shape_result
        gaussian_noise_std = float(shape_result["gaussian_noise_std"])
        detections_modeled = _apply_detection_noise_model(
            shape_result["detections_all"],
            spec.noise_model,
            gaussian_noise_std,
            background_reference_mean,
        )
        tau_regime = _effective_detection_threshold(
            ps.cfg,
            regime_label,
            eta_applied=(
                bool(ps.eta_correction.get("eta_applied", False))
                or bool(variant_eta_metadata.get("eta_applied", False))
            ),
        )
        accepted, rejected = filter_detections(detections_modeled, tau_regime)
        if variant_record is None:
            score_reference = _score_admissibility_reference_for_variant(
                ps.cfg,
                spec.name,
            )
        else:
            score_reference = _score_admissibility_reference_for_variant(
                ps.cfg,
                spec.name,
                variant_payload=variant_record,
            )
        reconstruction_summary: dict[str, Any] = {}
        if score_reference["reference_applied"]:
            reconstruction_summary = _reconstruction_summary_for_variant(
                reconstruction_cache,
                detection_image,
                ps.background,
                accepted,
                sigma_x=spec.sigma_x,
                sigma_y=spec.sigma_y,
            )
        score_admissibility = _score_admissibility_threshold_info(
            ps.cfg,
            spec.name,
            reconstruction_summary,
            tau_regime,
            reference=score_reference,
        )
        tau_v_star = float(score_admissibility["decision_threshold"])
        if _threshold_change_requires_refilter(tau_regime, tau_v_star):
            accepted, rejected = filter_detections(detections_modeled, tau_v_star)
        variant_summary = _detection_variant_summary(
            spec.name,
            spec.template_family,
            spec.noise_model,
            spec.sigma_x,
            spec.sigma_y,
            gaussian_noise_std,
            shape_result["corridor"],
            accepted,
            rejected,
            tau_v_star,
        )
        variant_summary["eta_preprocessing"] = dict(variant_eta_metadata)
        variant_summary["score_admissibility"] = dict(score_admissibility)
        variant_summary["count_diagnostics"].update(
            _score_admissibility_count_diagnostics(score_admissibility)
        )
        accepted, variant_summary = _apply_gaussian_warning_count_correction(
            accepted,
            rejected,
            variant_summary,
            regime_label,
            ps.cfg,
        )
        modes = variant_summary.setdefault("modes", {})
        modes[canonical_mode.mode_id] = stage5_modes.mode_summary(
            canonical_mode,
            accepted,
            rejected,
            tau_v_star,
            calibration_path=ps.cfg.get("eta_score_admissibility_npz_path"),
            reference_applied=bool(score_admissibility.get("reference_applied", False)),
            selected_for_public_count=False,
            score_admissibility=score_admissibility,
        )
        for experimental_mode in stage5_modes.experimental_modes_from_cfg(
            ps.cfg,
            spec.name,
            spec.template_family,
            spec.noise_model,
        ):
            experimental_threshold_base = (
                float(experimental_mode.threshold)
                if experimental_mode.threshold is not None
                else float(tau_regime)
            )
            experimental_accepted, experimental_rejected = stage5_modes.partition_by_mode_cached(
                partition_cache,
                detections_modeled,
                experimental_threshold_base,
                experimental_mode,
            )
            experimental_score_admissibility = _experimental_selection_score_admissibility(
                experimental_threshold_base
            )
            experimental_threshold = float(experimental_threshold_base)
            if experimental_mode.score_admissibility_npz_path not in (None, ""):
                experimental_mode_cfg = _experimental_mode_eta_cfg(ps.cfg, experimental_mode)
                experimental_reference = _score_admissibility_reference_for_variant(
                    experimental_mode_cfg,
                    spec.name,
                )
                score_domain_matches, reference_score_domain = (
                    _experimental_mode_score_admissibility_matches_reference(
                        experimental_mode,
                        experimental_reference,
                    )
                )
                if score_domain_matches:
                    experimental_reconstruction_summary: dict[str, Any] = {}
                    if experimental_reference["reference_applied"]:
                        experimental_reconstruction_summary = _reconstruction_summary_for_variant(
                            reconstruction_cache,
                            detection_image,
                            ps.background,
                            experimental_accepted,
                            sigma_x=spec.sigma_x,
                            sigma_y=spec.sigma_y,
                        )
                    experimental_score_admissibility = _score_admissibility_threshold_info(
                        experimental_mode_cfg,
                        spec.name,
                        experimental_reconstruction_summary,
                        experimental_threshold_base,
                        reference=experimental_reference,
                    )
                    experimental_threshold = float(
                        experimental_score_admissibility["decision_threshold"]
                    )
                    if _threshold_change_requires_refilter(
                        experimental_threshold_base,
                        experimental_threshold,
                    ):
                        experimental_accepted, experimental_rejected = stage5_modes.partition_by_mode_cached(
                            partition_cache,
                            detections_modeled,
                            experimental_threshold,
                            experimental_mode,
                        )
                else:
                    experimental_score_admissibility = _experimental_selection_score_admissibility(
                        experimental_threshold_base
                    )
                    experimental_score_admissibility.update(
                        {
                            "score_admissibility_score_domain_guard_applied": True,
                            "score_admissibility_mode_score_domain": str(
                                experimental_mode.score_domain
                            ),
                            "score_admissibility_reference_score_domain": (
                                reference_score_domain
                            ),
                            "score_admissibility_reference_source_path": str(
                                experimental_reference.get("source_path", "") or ""
                            ),
                        }
                    )
            modes[experimental_mode.mode_id] = stage5_modes.mode_summary(
                experimental_mode,
                experimental_accepted,
                experimental_rejected,
                experimental_threshold,
                calibration_path=(
                    experimental_mode.score_admissibility_npz_path
                    or ps.cfg.get("experimental_stage5_mode_calibration_npz_path")
                ),
                reference_applied=bool(
                    experimental_score_admissibility.get("reference_applied", False)
                ),
                selected_for_public_count=False,
                score_admissibility=experimental_score_admissibility,
            )
            modes[experimental_mode.mode_id]["count_diagnostics"].update(
                _score_admissibility_count_diagnostics(experimental_score_admissibility)
            )
        public_mode_id, public_mode_resolution = stage5_modes.resolve_public_mode_id(
            ps.cfg,
            spec.name,
            modes,
        )
        for mode_id, mode_summary in modes.items():
            mode_summary["selected_for_public_count"] = mode_id == public_mode_id
        accepted, rejected = _promote_variant_public_mode(
            variant_summary,
            modes,
            public_mode_id,
            public_mode_resolution,
        )
        variant_summaries[spec.name] = variant_summary
        accepted_by_variant[spec.name] = accepted
        rejected_by_variant[spec.name] = rejected

    selected_variant = variant_summaries[selected_variant_name]
    selected_shape_result = shape_results_by_variant[selected_variant_name]
    ps.response_roi = selected_shape_result["response_roi"]
    ps.response_band = selected_shape_result["response_band"]
    ps.matched_kernel = selected_shape_result["matched_kernel"]
    ps.corridor = selected_shape_result["corridor"]
    ps.response_noise_std = float(selected_variant["response_noise_std"])
    ps.axial_profile = selected_shape_result["axial_profile"]
    ps.row_peak_indices = selected_shape_result["row_peaks"]
    ps.detections = accepted_by_variant[selected_variant_name]
    ps.rejected_detections = rejected_by_variant[selected_variant_name]
    ps.count_decision_threshold = float(
        selected_variant["count_diagnostics"].get("decision_threshold", 0.0)
    )

    ps.accepted_detections_by_variant = accepted_by_variant
    ps.rejected_detections_by_variant = rejected_by_variant
    ps.snr_variants = variant_summaries
    ps.psf["selected_snr_variant"] = selected_variant_name
    ps.psf["evaluated_snr_variants"] = [str(spec.name) for spec in variant_specs]
    ps.psf["stage5_variant_noise_policy"] = _stage5_variant_noise_policy(ps.cfg)
    if use_variant_count_legibility:
        ps.eta_correction = dict(selected_variant.get("eta_preprocessing", ps.eta_correction))
    return ps


# ═══════════════════════════════════════════════════════════════════════════
#  Stage 6 – State and spectral summary
# ═══════════════════════════════════════════════════════════════════════════

_LINE_GEOMETRY_METHOD = "orthogonal_tls_pca_svd"
_LINE_GEOMETRY_FLOAT_FIELDS = (
    "chain_line_row_center_px",
    "chain_line_col_center_px",
    "chain_line_dir_row",
    "chain_line_dir_col",
    "chain_line_normal_row",
    "chain_line_normal_col",
    "chain_line_angle_rad",
    "chain_line_total_scatter_px2",
    "chain_line_principal_scatter_px2",
    "chain_line_orth_scatter_px2",
    "chain_line_rms_orth_residual_px",
    "chain_line_max_orth_residual_px",
    "chain_line_linearity_ratio",
    "chain_line_orth_residual_fraction",
    "chain_line_projected_spacing_px",
    "chain_line_projected_spacing_cv",
    "chain_line_span_px",
)


def _undefined_line_geometry_metrics(
    status: str,
    *,
    n_input_points: int,
    n_points: int,
    n_dropped_nonfinite: int,
) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "chain_line_fit_defined": False,
        "chain_line_fit_status": status,
        "chain_line_fit_method": _LINE_GEOMETRY_METHOD,
        "chain_line_n_input_points": int(n_input_points),
        "chain_line_n_points": int(n_points),
        "chain_line_n_dropped_nonfinite": int(n_dropped_nonfinite),
    }
    metrics.update({name: float("nan") for name in _LINE_GEOMETRY_FLOAT_FIELDS})
    return metrics


def line_geometry_metrics(detections: list[dict[str, Any]]) -> dict[str, Any]:
    """Fit an orthogonal TLS line to accepted-ion centroids."""
    n_input_points = len(detections)
    if n_input_points == 0:
        return _undefined_line_geometry_metrics(
            "no_points",
            n_input_points=0,
            n_points=0,
            n_dropped_nonfinite=0,
        )

    points = np.asarray(
        [
            [det.get("row", float("nan")), det.get("col", float("nan"))]
            for det in detections
        ],
        dtype=np.float64,
    )
    finite_mask = np.isfinite(points).all(axis=1)
    points = points[finite_mask]
    n_points = int(points.shape[0])
    n_dropped_nonfinite = int(n_input_points - n_points)
    if n_points == 0:
        return _undefined_line_geometry_metrics(
            "no_points",
            n_input_points=n_input_points,
            n_points=0,
            n_dropped_nonfinite=n_dropped_nonfinite,
        )
    if n_points == 1:
        return _undefined_line_geometry_metrics(
            "insufficient_points",
            n_input_points=n_input_points,
            n_points=1,
            n_dropped_nonfinite=n_dropped_nonfinite,
        )

    center = np.asarray(np.mean(points, axis=0, dtype=np.float64), dtype=np.float64)
    centered = points - center
    scale = float(max(1.0, np.max(np.abs(points)), np.max(np.abs(centered))))
    float_eps = np.finfo(np.float64).eps
    scatter_eps = 64.0 * float_eps * max(n_points, 1) * scale * scale
    spacing_eps = 64.0 * float_eps * scale

    try:
        _, singular_values, vh = np.linalg.svd(centered, full_matrices=False)
    except np.linalg.LinAlgError:
        try:
            _, singular_values, vh = linalg.svd(
                centered,
                full_matrices=False,
                lapack_driver="gesvd",
            )
        except Exception:
            return _undefined_line_geometry_metrics(
                "svd_failed",
                n_input_points=n_input_points,
                n_points=n_points,
                n_dropped_nonfinite=n_dropped_nonfinite,
            )

    principal_scatter = float(singular_values[0] ** 2)
    orth_scatter = float(singular_values[1] ** 2)
    if orth_scatter <= scatter_eps:
        orth_scatter = 0.0
    total_scatter = float(principal_scatter + orth_scatter)
    if total_scatter <= scatter_eps:
        return _undefined_line_geometry_metrics(
            "degenerate_zero_scatter",
            n_input_points=n_input_points,
            n_points=n_points,
            n_dropped_nonfinite=n_dropped_nonfinite,
        )

    direction = np.asarray(vh[0], dtype=np.float64)
    direction_norm = float(np.linalg.norm(direction))
    if not np.isfinite(direction_norm) or direction_norm <= float_eps:
        return _undefined_line_geometry_metrics(
            "degenerate_zero_scatter",
            n_input_points=n_input_points,
            n_points=n_points,
            n_dropped_nonfinite=n_dropped_nonfinite,
        )
    direction = direction / direction_norm
    sign_axis = 1 if abs(float(direction[1])) >= abs(float(direction[0])) else 0
    if direction[sign_axis] < 0:
        direction = -direction

    normal = np.asarray([-direction[1], direction[0]], dtype=np.float64)
    projections = centered @ direction
    residuals = np.abs(centered @ normal)
    ordered_projections = np.sort(projections)
    projection_gaps = np.diff(ordered_projections)
    projected_spacing = float(np.median(projection_gaps))
    projected_span = float(ordered_projections[-1] - ordered_projections[0])
    gap_mean = float(np.mean(projection_gaps))
    projected_spacing_cv = (
        float(np.std(projection_gaps, ddof=0) / gap_mean)
        if gap_mean > spacing_eps else float("nan")
    )

    metrics: dict[str, Any] = {
        "chain_line_fit_defined": True,
        "chain_line_fit_status": "ok_two_point_exact" if n_points == 2 else "ok",
        "chain_line_fit_method": _LINE_GEOMETRY_METHOD,
        "chain_line_n_input_points": int(n_input_points),
        "chain_line_n_points": int(n_points),
        "chain_line_n_dropped_nonfinite": int(n_dropped_nonfinite),
        "chain_line_row_center_px": float(center[0]),
        "chain_line_col_center_px": float(center[1]),
        "chain_line_dir_row": float(direction[0]),
        "chain_line_dir_col": float(direction[1]),
        "chain_line_normal_row": float(normal[0]),
        "chain_line_normal_col": float(normal[1]),
        "chain_line_angle_rad": float(np.arctan2(direction[0], direction[1])),
        "chain_line_total_scatter_px2": total_scatter,
        "chain_line_principal_scatter_px2": principal_scatter,
        "chain_line_orth_scatter_px2": orth_scatter,
        "chain_line_rms_orth_residual_px": float(np.sqrt(max(orth_scatter, 0.0) / n_points)),
        "chain_line_max_orth_residual_px": float(np.max(residuals)),
        "chain_line_linearity_ratio": float(principal_scatter / total_scatter),
        "chain_line_orth_residual_fraction": float(orth_scatter / total_scatter),
        "chain_line_projected_spacing_px": projected_spacing,
        "chain_line_projected_spacing_cv": projected_spacing_cv,
        "chain_line_span_px": projected_span,
    }
    if not all(np.isfinite(float(metrics[name])) for name in _LINE_GEOMETRY_FLOAT_FIELDS):
        return _undefined_line_geometry_metrics(
            "nonfinite_output",
            n_input_points=n_input_points,
            n_points=n_points,
            n_dropped_nonfinite=n_dropped_nonfinite,
        )
    return metrics


def state_metrics(detections: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize the accepted-ion state for one frame.

    This function reports the observables associated with the accepted set of
    candidate ions.  The visible-ion count is therefore deterministic once the
    thresholded candidate partition has been performed.  The companion helper
    ``count_decision_metrics`` reports how far that partition lies from the
    decision boundary.

    Parameters
    ----------
    detections : list of dict
        Accepted ions.

    Returns
    -------
    dict
        ``visible_ion_count``, ``state_snr_rss``, ``weakest_ion_snr``,
        ``mean_ion_snr``, ``axial_spacing_px_spatial``.
    """
    line_metrics = line_geometry_metrics(detections)
    if not detections:
        return {
            "visible_ion_count": 0,
            "state_snr_rss": 0.0,
            "weakest_ion_snr": 0.0,
            "mean_ion_snr": 0.0,
            "axial_spacing_px_spatial": float("nan"),
            **line_metrics,
        }

    matched_snrs = np.array(
        [det["matched_snr"] for det in detections], dtype=np.float64
    )
    rows = np.array(
        [det["row"] for det in detections], dtype=np.float64
    )
    spacing = (
        float(np.median(np.diff(rows))) if len(rows) > 1 else float("nan")
    )

    return {
        "visible_ion_count": int(len(detections)),
        "state_snr_rss": float(np.sqrt(np.sum(matched_snrs**2))),
        "weakest_ion_snr": float(np.min(matched_snrs)),
        "mean_ion_snr": float(np.mean(matched_snrs)),
        "axial_spacing_px_spatial": spacing,
        **line_metrics,
    }


def spectral_chain_metrics(
    response_band: np.ndarray,
    cfg: dict[str, Any],
) -> dict[str, Any]:
    """Measure the axial comb signature in the 2-D Fourier plane.

    The ion chain is narrow transversely and comb-like axially.  Averaging
    the 2-D power over a narrow horizontal frequency band yields a 1-D
    vertical power profile whose dominant positive-frequency peak gives
    the spacing estimate in pixels.

    Parameters
    ----------
    response_band : np.ndarray
        Matched-filter response in the corridor.
    cfg : dict
        Must contain ``axial_frequency_band``.

    Returns
    -------
    dict
        ``axial_frequency_cpp``, ``spectral_spacing_px``,
        ``spectral_peak_power``, ``spectral_state_snr``,
        ``windowed_power`` (2-D array, consumed by Stage 6 for the
        spectral cube and then removed before serialization).
    """
    spectrum = _hann_fft2(response_band)
    power = np.abs(spectrum) ** 2
    u_axis = fft.fftshift(fft.fftfreq(response_band.shape[1]))
    col_band = np.abs(u_axis) <= cfg["axial_frequency_band"]
    vertical_power = power[:, col_band].mean(axis=1)
    v_axis = fft.fftshift(fft.fftfreq(response_band.shape[0]))
    min_freq = 2.0 / response_band.shape[0]
    pos_mask = v_axis > min_freq
    v_pos = v_axis[pos_mask]
    p_pos = vertical_power[pos_mask]

    if p_pos.size == 0:
        return {
            "axial_frequency_cpp": float("nan"),
            "spectral_spacing_px": float("nan"),
            "spectral_peak_power": float("nan"),
            "spectral_state_snr": float("nan"),
            "windowed_power": power,
        }

    peak_index = int(np.argmax(p_pos))
    dominant_frequency = float(v_pos[peak_index])
    noise_floor = float(np.median(p_pos))
    noise_sigma = robust_std(p_pos)
    spectral_peak_power = float(p_pos[peak_index])

    return {
        "axial_frequency_cpp": dominant_frequency,
        "spectral_spacing_px": (
            float(1 / dominant_frequency) if dominant_frequency > EPS
            else float("nan")
        ),
        "spectral_peak_power": spectral_peak_power,
        "spectral_state_snr": (
            float((spectral_peak_power - noise_floor) / noise_sigma)
            if noise_sigma > EPS else float("nan")
        ),
        "windowed_power": power,
    }


def stage_state_summary(ps: PipelineState) -> PipelineState:
    """Stage 6: compute state-level and spectral summary metrics.

    Requires: stage 5 completed (``response_band``, ``detections``).
    """
    assert ps.response_band is not None, "Stage 6 requires stage 5 (detection) to run first."

    ps.state = state_metrics(ps.detections)
    ps.spectral = spectral_chain_metrics(ps.response_band, ps.cfg)
    ps.roi_power_spectrum = ps.spectral.pop("windowed_power")

    selected_variant = ps.snr_variants.get(ps.psf.get("selected_snr_variant", ""))
    if selected_variant is not None:
        selected_variant["state"] = dict(ps.state)
        selected_variant["visible_ion_count"] = int(ps.state["visible_ion_count"])
    return ps


# ═══════════════════════════════════════════════════════════════════════════
#  Full pipeline
# ═══════════════════════════════════════════════════════════════════════════

def analyze_array_to_state(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
 ) -> PipelineState:
    """Run the six-stage pipeline and return the populated internal state."""
    if cfg is not None:
        unknown_keys = set(cfg) - set(DEFAULT_CFG)
        if unknown_keys:
            import warnings
            warnings.warn(
                f"Unknown configuration keys will be ignored: "
                f"{sorted(unknown_keys)}",
                stacklevel=2,
            )
    merged_cfg = dict(DEFAULT_CFG if cfg is None else {**DEFAULT_CFG, **cfg})
    image = load_grayscale_image(image)
    E_eta, eta_metadata = prepare_eta_correction(image.shape, merged_cfg)
    image = image - E_eta

    ps = PipelineState(
        image=image,
        cfg=merged_cfg,
        source_name=source_name,
        eta_correction=eta_metadata,
    )
    with _fft_runtime_context():
        _record_stage_timing(ps, "background", stage_background)
        _record_stage_timing(ps, "nps", stage_nps)
        _record_stage_timing(ps, "prefilter", stage_prefilter)
        _record_stage_timing(ps, "corridor_and_psf", stage_corridor_and_psf)
        _record_stage_timing(ps, "detection", stage_detection)
        _record_stage_timing(ps, "state_summary", stage_state_summary)
    return ps


def analyze_array_to_stage3_operator_state(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
) -> ParallelStage3OperatorState:
    """Build the root Stage 0-3 operator state for the staged path."""
    if cfg is not None:
        unknown_keys = set(cfg) - set(DEFAULT_CFG)
        if unknown_keys:
            warnings.warn(
                f"Unknown configuration keys will be ignored: {sorted(unknown_keys)}",
                stacklevel=2,
            )

    merged_cfg = parallel_working_image.merge_cfg(cfg)
    observed_image = load_grayscale_image(image)
    E_eta, eta_metadata = prepare_eta_correction(
        observed_image.shape,
        merged_cfg,
    )
    eta_corrected_image = observed_image - E_eta
    background = parallel_stage0_ops.tile_background_stats(eta_corrected_image, merged_cfg)
    nps = parallel_stage0_ops.nps_diagnostics(background["dark_tiles"])
    regime = parallel_stage0_ops.classify_noise_regime(background, nps, merged_cfg)
    prefilter_choice = parallel_stage0_ops.choose_prefilter(background, regime, merged_cfg)
    operators = parallel_working_image.build_working_image_operators(
        observed_image,
        merged_cfg,
        background,
        regime,
        prefilter_choice,
        eta_surface=E_eta,
        eta_metadata=eta_metadata,
    )
    return ParallelStage3OperatorState(
        source_name=source_name,
        image=observed_image,
        cfg=merged_cfg,
        eta_correction=eta_metadata,
        background=background,
        nps=nps,
        regime=regime,
        prefilter_choice=prefilter_choice,
        operators=operators,
    )


def analyze_path_to_stage3_operator_state(
    path: str | Path,
    cfg: dict[str, Any] | None = None,
) -> ParallelStage3OperatorState:
    """Load one frame from disk and build the Stage 0-3 operator state."""
    path_obj = Path(path)
    image = load_grayscale_image(path_obj)
    return analyze_array_to_stage3_operator_state(
        image,
        cfg=cfg,
        source_name=path_obj.name,
    )


def build_variant_stage3_operator_state(
    state: ParallelStage3OperatorState,
    correction: np.ndarray,
    correction_metadata: dict[str, Any] | None = None,
    *,
    variant_name: str | None = None,
    residual_spectral_summary: dict[str, Any] | None = None,
) -> ParallelStage3OperatorState:
    """Return a branch-local Stage 0-3 state without mutating the base state."""
    merged_metadata = dict(state.eta_correction)
    if correction_metadata is not None:
        merged_metadata.update(correction_metadata)
    operators = parallel_working_image.build_variant_working_image_operators(
        state.image,
        state.cfg,
        state.background,
        state.regime,
        state.prefilter_choice,
        correction=correction,
        correction_metadata=merged_metadata,
        residual_spectral_summary=residual_spectral_summary,
        variant_name=variant_name,
    )
    return replace(state, eta_correction=merged_metadata, operators=operators)


def analyze_array_to_stage4_state(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
):
    """Build the corrected-image Stage 4 state in the root detector."""
    stage3_state = analyze_array_to_stage3_operator_state(
        image,
        cfg=cfg,
        source_name=source_name,
    )
    return parallel_stage4.analyze_stage4_from_stage3_state(stage3_state)


def analyze_array_to_stage5_state(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
):
    """Build the corrected-image Stage 5 state in the root detector."""
    stage4_state = analyze_array_to_stage4_state(
        image,
        cfg=cfg,
        source_name=source_name,
    )
    return parallel_stage5.analyze_stage5_from_stage4_state(stage4_state)


def analyze_path_to_stage5_state(
    path: str | Path,
    cfg: dict[str, Any] | None = None,
):
    """Load one frame from disk and build the Stage 5 state."""
    path_obj = Path(path)
    image = load_grayscale_image(path_obj)
    return analyze_array_to_stage5_state(
        image,
        cfg=cfg,
        source_name=path_obj.name,
    )


def analyze_array_to_stage6_state(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
):
    """Build the corrected-image Stage 6 summary state in the root detector."""
    stage5_state = analyze_array_to_stage5_state(
        image,
        cfg=cfg,
        source_name=source_name,
    )
    return parallel_stage6.analyze_stage6_from_stage5_state(stage5_state)


def analyze_path_to_stage6_state(
    path: str | Path,
    cfg: dict[str, Any] | None = None,
):
    """Load one frame from disk and build the Stage 6 summary state."""
    path_obj = Path(path)
    image = load_grayscale_image(path_obj)
    return analyze_array_to_stage6_state(
        image,
        cfg=cfg,
        source_name=path_obj.name,
    )


def working_roi_inputs_from_state(
    state: ParallelStage3OperatorState,
    roi_bounds: tuple[int, int, int, int],
) -> dict[str, np.ndarray]:
    """Return ROI inputs from a Stage 0-3 operator state."""
    return parallel_working_image.working_image_inputs_for_bounds(state.operators, roi_bounds)


def analyze_array(
    image: np.ndarray,
    cfg: dict[str, Any] | None = None,
    source_name: str = "array",
    frame_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the staged Stage 0-6 analysis pipeline on one frame."""
    t0 = time.perf_counter()
    stage_timings_s: dict[str, float] = {}

    stage_started = time.perf_counter()
    stage3_state = analyze_array_to_stage3_operator_state(
        image,
        cfg=cfg,
        source_name=source_name,
    )
    stage_timings_s["background"] = 0.0
    stage_timings_s["nps"] = 0.0
    stage_timings_s["prefilter"] = time.perf_counter() - stage_started

    stage_started = time.perf_counter()
    stage4_state = parallel_stage4.analyze_stage4_from_stage3_state(stage3_state)
    stage_timings_s["corridor_and_psf"] = time.perf_counter() - stage_started

    stage_started = time.perf_counter()
    stage5_state = parallel_stage5.analyze_stage5_from_stage4_state(stage4_state)
    stage_timings_s["detection"] = time.perf_counter() - stage_started

    stage_started = time.perf_counter()
    stage6_state = parallel_stage6.analyze_stage6_from_stage5_state(stage5_state)
    stage_timings_s["state_summary"] = time.perf_counter() - stage_started

    return parallel_stage6.build_result_from_stage6_state(
        stage6_state,
        compute_time_s=time.perf_counter() - t0,
        stage_timings_s=stage_timings_s,
        frame_metadata=frame_metadata,
    )


def analyze_path(
    path: str | Path,
    cfg: dict[str, Any] | None = None,
    frame_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Convenience wrapper: load an image from disk and analyze it."""
    path = Path(path)
    image = load_grayscale_image(path)
    return analyze_array(
        image,
        cfg=cfg,
        source_name=path.name,
        frame_metadata=frame_metadata,
    )


# ═══════════════════════════════════════════════════════════════════════════
#  Time-series helpers
# ═══════════════════════════════════════════════════════════════════════════

def build_spectral_cube(results: list[dict[str, Any]]) -> np.ndarray:
    """Stack per-frame 2-D power spectra into a (T, H, W) cube.

    Parameters
    ----------
    results : list of dict
        Output of ``analyze_array`` for each frame.

    Returns
    -------
    np.ndarray
        3-D array indexed [time, freq_row, freq_col].

    Raises
    ------
    ValueError
        If the search-band shapes differ across frames.
    """
    cubes = [r["_internal"]["roi_power_spectrum"] for r in results]
    shapes = {c.shape for c in cubes}
    if len(shapes) != 1:
        raise ValueError(
            "All analyzed frames must share the same search-band shape "
            "to build a spectral cube."
        )
    return np.stack(cubes, axis=0)


def temporal_fft_cube(spectral_cube: np.ndarray) -> np.ndarray:
    """Temporal FFT along the time axis of the spectral cube.

    The input cube already contains 2-D power spectra (spatial-frequency
    domain), so only the time axis is transformed.

    Parameters
    ----------
    spectral_cube : np.ndarray
        (T, H, W) spectral cube.

    Returns
    -------
    np.ndarray
        DC-centered temporal FFT at each spatial-frequency point.
    """
    return fft.fftshift(fft.fft(spectral_cube, axis=0), axes=0)


def temporal_laplace_cube(
    spectral_cube: np.ndarray,
    dt: float,
    s_values: Iterable[float],
) -> np.ndarray:
    """Temporal Laplace transform for a list of real *s* values.

    Parameters
    ----------
    spectral_cube : np.ndarray
        (T, H, W) spectral cube.
    dt : float
        Time spacing between frames.
    s_values : iterable of float
        Laplace *s* parameters.

    Returns
    -------
    np.ndarray
        (len(s_values), H, W) array.
    """
    times = np.arange(spectral_cube.shape[0], dtype=np.float64) * float(dt)
    weights = np.exp(
        -np.outer(np.asarray(tuple(s_values), dtype=np.float64), times)
    )
    return np.tensordot(weights, spectral_cube, axes=(1, 0))


# ═══════════════════════════════════════════════════════════════════════════
#  Serialization
# ═══════════════════════════════════════════════════════════════════════════

def to_builtin(value: Any, _depth: int = 0) -> Any:
    """Recursively convert numpy-heavy outputs to JSON-serializable types.

    The ``_internal`` key (which holds numpy arrays for cross-frame
    composition) is stripped automatically.

    ``float('nan')`` and ``float('inf')`` are replaced with ``None``
    (JSON ``null``) to preserve the semantic distinction between "not
    measured / undefined" and a genuine zero.  For example,
    ``axial_spacing_px_spatial = null`` means spacing is undefined
    (single ion or no ions), whereas ``0.0`` would falsely imply a
    measured spacing of zero pixels.
    """
    if _depth > 100:
        return str(value)
    if isinstance(value, dict):
        return {
            key: to_builtin(val, _depth + 1)
            for key, val in value.items()
            if key != "_internal"
        }
    if isinstance(value, (list, tuple)):
        return [to_builtin(item, _depth + 1) for item in value]
    if isinstance(value, np.ndarray):
        return to_builtin(value.tolist())
    if isinstance(value, (np.floating, np.integer)):
        value = value.item()
    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
        return None
    return value


# ═══════════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════════

def print_summary(result: dict[str, Any]) -> None:
    """Print a compact human-readable summary for one analyzed frame."""
    state = result["state"]
    psf = result["psf"]
    background = result["background"]
    spectral = result["spectral"]
    count_diag = result["count_diagnostics"]
    print(f"\n=== {result['source']} ===")
    print(f"Compute time: {result['compute_time_s']:.4f} s")
    print(
        f"Visible ions: {state['visible_ion_count']} "
        f"/ {result['max_supported_ions']}"
    )
    print(f"State SNR (RSS of matched peaks): {state['state_snr_rss']:.2f}")
    print(f"Weakest ion matched SNR: {state['weakest_ion_snr']:.2f}")
    if np.isfinite(count_diag["nearest_boundary_margin"]):
        print(
            "Count decision margin [matched-SNR units]: "
            f"{count_diag['nearest_boundary_margin']:.2f}"
        )
    print(
        "PSF used (sigma_x, sigma_y) [px]: "
        f"({psf['sigma_x_used']:.2f}, {psf['sigma_y_used']:.2f})"
    )
    print(
        "Background diagnostics: "
        f"Fano={background['fano_factor']:.2f}, "
        f"MV slope={background['mean_variance_slope']:.2f}, "
        f"flatness={result['nps']['spectral_flatness']:.2f}"
    )
    if np.isfinite(spectral["spectral_spacing_px"]):
        print(
            "Spectral spacing estimate [px]: "
            f"{spectral['spectral_spacing_px']:.2f} "
            f"at {spectral['axial_frequency_cpp']:.4f} cyc/px"
        )
    if result["detections"]:
        print("Spatial labels (top to bottom):")
        for det in result["detections"]:
            print(
                f"  {det['label']}: row={det['row']:.2f}, "
                f"col={det['col']:.2f}, "
                f"matched_snr={det['matched_snr']:.2f}, "
                f"integrated_snr={det['integrated_snr']:.2f}"
            )
    else:
        print("Spatial labels: none detected.")
    if result["rejected_detections"]:
        print("Rejected candidates:")
        for det in result["rejected_detections"]:
            print(
                f"  row={det['row']:.2f}, col={det['col']:.2f}, "
                f"matched_snr={det['matched_snr']:.2f}, "
                f"reason={det['rejection_reason']}"
            )


def _resolve_config_relative_paths(value: Any, *, config_dir: Path) -> Any:
    if isinstance(value, dict):
        resolved: dict[str, Any] = {}
        for key, item in value.items():
            if key in CONFIG_RELATIVE_PATH_KEYS and isinstance(item, str) and item.strip():
                candidate = Path(item)
                resolved[key] = (
                    str(candidate)
                    if candidate.is_absolute()
                    else str((config_dir / candidate).resolve(strict=False))
                )
                continue
            resolved[key] = _resolve_config_relative_paths(item, config_dir=config_dir)
        return resolved
    if isinstance(value, list):
        return [_resolve_config_relative_paths(item, config_dir=config_dir) for item in value]
    return value


def load_config_file(path: str | Path) -> dict[str, Any]:
    """Load a JSONL configuration file and return it as a dict.

    The file must contain one JSON object per line. Blank lines and lines
    beginning with ``#`` are ignored. The first non-skipped line is parsed
    and returned; remaining lines are currently ignored.

    Parameters
    ----------
    path : str or Path
        Path to a ``.jsonl`` file whose first record keys match
        ``DEFAULT_CFG``.

    Returns
    -------
    dict
        Parsed configuration overrides.

    Raises
    ------
    SystemExit
        If the file cannot be read or parsed.
    """
    import sys

    path = Path(path)
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            obj = json.loads(stripped)
            if not isinstance(obj, dict):
                raise ValueError(
                    "first JSONL config record must be a JSON object"
                )
            return _migrate_legacy_selection_config(
                _resolve_config_relative_paths(obj, config_dir=path.parent)
            )
        return {}
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error loading config file {path}: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


def _migrate_legacy_selection_config(cfg: dict[str, Any]) -> dict[str, Any]:
    """Expose legacy selection-score JSON config as a ledger-only mode."""
    if "experimental_stage5_modes" in cfg or "selection_score_key" not in cfg:
        return cfg

    raw_score_key = str(cfg.get("selection_score_key", "") or "")
    if not raw_score_key:
        return cfg
    score_key = stage5_modes.canonicalize_score_key(raw_score_key)

    mode: dict[str, Any] = {
        "mode_id": f"config_{score_key}_ledger",
        "score_key": score_key,
        "ledger_only": True,
    }
    if "selection_score_threshold" in cfg:
        mode["threshold"] = cfg["selection_score_threshold"]

    migrated = dict(cfg)
    migrated["selection_score_key"] = score_key
    migrated["experimental_stage5_modes"] = [mode]
    return migrated


def apply_manual_calibrated_cli_overrides(
    cfg: dict[str, Any],
    args: argparse.Namespace,
) -> None:
    """Project explicit manual-calibrated CLI flags into detector config keys."""

    manual_calibrated_mode = getattr(args, "manual_calibrated_mode", None)
    manual_calibrated_investigation_root = getattr(
        args, "manual_calibrated_investigation_root", None
    )
    eta_mode = getattr(args, "eta_mode", None)
    score_npz_path = getattr(args, "eta_score_admissibility_npz_path", None)
    variant_npz_path = getattr(args, "eta_variant_count_legibility_npz_path", None)
    eta_max_abs_correction = getattr(args, "eta_max_abs_correction", None)
    eta_runtime_min_coherence = getattr(args, "eta_runtime_min_coherence", None)
    stage5_mode_id = getattr(args, "stage5_mode_id", None)
    stage5_score_key = getattr(args, "stage5_score_key", None)
    stage5_calibration_policy = getattr(args, "stage5_calibration_policy", None)
    stage5_threshold_source = getattr(args, "stage5_threshold_source", None)

    if manual_calibrated_mode is not None:
        preset_config_path = resolve_manual_calibrated_mode_config(
            manual_calibrated_mode,
            investigation_root=manual_calibrated_investigation_root,
        )
        cfg.update(load_config_file(preset_config_path))

    manual_artifacts_requested = (
        score_npz_path is not None or variant_npz_path is not None
    )
    if eta_mode is not None:
        cfg["eta_mode"] = str(eta_mode)
    elif manual_artifacts_requested:
        cfg["eta_mode"] = "manual_calibrated"

    if score_npz_path is not None:
        cfg["eta_score_admissibility_npz_path"] = str(score_npz_path)
    if variant_npz_path is not None:
        cfg["eta_variant_count_legibility_npz_path"] = str(variant_npz_path)
    if eta_max_abs_correction is not None:
        cfg["eta_max_abs_correction"] = float(eta_max_abs_correction)
    if eta_runtime_min_coherence is not None:
        cfg["eta_runtime_min_coherence"] = float(eta_runtime_min_coherence)

    if stage5_mode_id is None and stage5_score_key is None:
        return
    if stage5_mode_id is None or stage5_score_key is None:
        warnings.warn(
            "--stage5-mode-id and --stage5-score-key must be provided together; "
            "ignoring incomplete manual-calibrated Stage 5 mode overrides.",
            stacklevel=2,
        )
        return

    canonical_score_key = stage5_modes.canonicalize_score_key(stage5_score_key)
    manual_mode_cfg: dict[str, Any] = {
        "mode_id": str(stage5_mode_id),
        "score_key": canonical_score_key,
    }
    if stage5_calibration_policy is not None:
        manual_mode_cfg["calibration_policy"] = str(stage5_calibration_policy)
    elif manual_artifacts_requested:
        manual_mode_cfg["calibration_policy"] = stage5_modes.MODE_ARTIFACT_POLICY

    if stage5_threshold_source is not None:
        manual_mode_cfg["threshold_source"] = str(stage5_threshold_source)
    elif score_npz_path is not None:
        manual_mode_cfg["threshold_source"] = "manual_calibrated_mode_tau_v_star"

    if score_npz_path is not None:
        resolved_score_npz_path = str(score_npz_path)
        manual_mode_cfg["eta_score_admissibility_npz_path"] = resolved_score_npz_path
        manual_mode_cfg["calibration_path"] = resolved_score_npz_path
    if variant_npz_path is not None:
        manual_mode_cfg["eta_variant_count_legibility_npz_path"] = str(variant_npz_path)

    cfg["experimental_stage5_modes"] = [manual_mode_cfg]
    if getattr(args, "selected_stage5_mode", None) is None:
        cfg["experimental_stage5_selected_mode"] = str(stage5_mode_id)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Exposes the most commonly tuned configuration parameters as named flags
    so they can be adjusted without editing the source or writing a JSONL
    config file.  For full control, use ``--config`` with a JSONL file.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Count and label ions in trap images using "
            "FFT-based matched filtering."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s frame_a.png frame_b.png\n"
            "  %(prog)s *.png --jsonl frame_analysis.jsonl\n"
            "  %(prog)s *.png --max-ions 10 --min-snr 8.0\n"
            "  %(prog)s *.png --config analysis_config.jsonl --jsonl frame_analysis.jsonl\n"
            "  %(prog)s *.png --save-cube --dt 0.5 --jsonl frame_analysis.jsonl\n"
        ),
    )

    # ── Positional ──
    parser.add_argument(
        "images", nargs="+",
        help="Image paths to analyze.",
    )

    # ── Output ──
    out = parser.add_argument_group("output options")
    out.add_argument(
        "--jsonl", dest="jsonl_path", metavar="PATH",
        help="Write JSONL results to PATH.",
    )
    out.add_argument(
        "--save-cube", action="store_true",
        help=(
            "When multiple frames are given, save a spectral cube "
            "(.npz) alongside the JSONL output."
        ),
    )
    out.add_argument(
        "--dt", type=float, default=1, metavar="SEC",
        help="Time spacing between frames for --save-cube (default: 1.0).",
    )

    # ── Configuration overrides ──
    cfg = parser.add_argument_group(
        "detection parameters",
        "Override individual configuration values.  "
        "For full control, use --config with a JSONL file.",
    )
    cfg.add_argument(
        "--config", dest="config_file", metavar="JSONL",
        help="Load configuration overrides from a JSONL file.",
    )
    cfg.add_argument(
        "--manual-calibrated-mode",
        choices=MANUAL_CALIBRATED_MODE_PRESET_CHOICES,
        default=None,
        metavar="MODE",
        help=(
            "Load one accepted post-iteration manual-calibrated detector preset. "
            "This is a shortcut for the investigation override JSONLs."
        ),
    )
    cfg.add_argument(
        "--manual-calibrated-investigation-root",
        type=Path,
        default=None,
        metavar="PATH",
        help=(
            "Override the preset root used by --manual-calibrated-mode "
            f"(default: {DEFAULT_MANUAL_CALIBRATED_INVESTIGATION_ROOT})."
        ),
    )
    cfg.add_argument(
        "--max-ions", type=int, default=None, metavar="N",
        help=f"Maximum ion count (default: {DEFAULT_CFG['max_ions']}).",
    )
    cfg.add_argument(
        "--min-snr", type=float, default=None, metavar="S",
        help=(
            "Minimum matched-filter SNR to accept a candidate "
            f"(default: {DEFAULT_CFG['min_accepted_matched_snr']})."
        ),
    )
    cfg.add_argument(
        "--peak-distance", type=int, default=None, metavar="PX",
        help=(
            "Minimum axial separation between ions in pixels "
            f"(default: {DEFAULT_CFG['peak_min_distance']})."
        ),
    )
    cfg.add_argument(
        "--dog-small", type=float, default=None, metavar="σ",
        help=(
            "DoG bandpass small sigma "
            f"(default: {DEFAULT_CFG['dog_small_sigma']})."
        ),
    )
    cfg.add_argument(
        "--dog-large", type=float, default=None, metavar="σ",
        help=(
            "DoG bandpass large sigma "
            f"(default: {DEFAULT_CFG['dog_large_sigma']})."
        ),
    )
    cfg.add_argument(
        "--enable-search-roi",
        action="store_true",
        help=(
            "Explicitly re-enable legacy Stage 4/5 ROI and corridor restriction. "
            "Without this flag, search-window and corridor-width knobs do not narrow runtime behavior."
        ),
    )
    cfg.add_argument(
        "--search-rows", type=float, nargs=2, default=None,
        metavar=("LO", "HI"),
        help=(
            "Row fraction bounds for the Stage 4/5 search window when "
            "--enable-search-roi is set "
            f"(default: {DEFAULT_CFG['search_row_fraction']})."
        ),
    )
    cfg.add_argument(
        "--search-cols", type=float, nargs=2, default=None,
        metavar=("LO", "HI"),
        help=(
            "Column fraction bounds for the Stage 4/5 search window when "
            "--enable-search-roi is set "
            f"(default: {DEFAULT_CFG['search_col_fraction']})."
        ),
    )
    cfg.add_argument(
        "--corridor-width", type=int, default=None, metavar="PX",
        help=(
            "Half-width of the legacy chain corridor when --enable-search-roi is set "
            f"(default: {DEFAULT_CFG['search_half_width']})."
        ),
    )
    cfg.add_argument(
        "--selection-score",
        type=str,
        choices=stage5_modes.SUPPORTED_MODE_SCORE_KEYS,
        default=None,
        help=(
            "Deprecated compatibility flag. Records a ledger-only experimental "
            "Stage 5 mode and leaves the canonical selected count unchanged."
        ),
    )
    cfg.add_argument(
        "--selection-threshold",
        type=float,
        default=None,
        metavar="VALUE",
        help="Optional explicit threshold for the ledger-only --selection-score mode.",
    )
    cfg.add_argument(
        "--selected-stage5-mode",
        type=str,
        default=None,
        metavar="MODE_ID",
        help=(
            "Promote the named experimental Stage 5 mode into the public count. "
            "Omit this to keep canonical selected counts."
        ),
    )
    cfg.add_argument(
        "--stage5-selected-noise-only",
        action="store_true",
        help=(
            "Evaluate only the regime-selected Stage 5 noise model across the two "
            "PSF families instead of all four PSF/noise variants."
        ),
    )
    cfg.add_argument(
        "--eta-mode",
        choices=("off", "manual_calibrated"),
        default=None,
        metavar="MODE",
        help=(
            "Override eta runtime mode directly. Supplying artifact paths without "
            "this flag implicitly promotes eta_mode to manual_calibrated."
        ),
    )
    cfg.add_argument(
        "--eta-score-admissibility-npz",
        dest="eta_score_admissibility_npz_path",
        default=None,
        metavar="PATH",
        help="Path to the manual-calibrated score-admissibility NPZ artifact.",
    )
    cfg.add_argument(
        "--eta-variant-count-legibility-npz",
        dest="eta_variant_count_legibility_npz_path",
        default=None,
        metavar="PATH",
        help="Path to the manual-calibrated variant count-legibility NPZ artifact.",
    )
    cfg.add_argument(
        "--eta-max-abs-correction",
        type=float,
        default=None,
        metavar="VALUE",
        help=(
            "Override eta_max_abs_correction directly "
            f"(default: {DEFAULT_CFG['eta_max_abs_correction']})."
        ),
    )
    cfg.add_argument(
        "--eta-runtime-min-coherence",
        type=float,
        default=None,
        metavar="VALUE",
        help=(
            "Override eta_runtime_min_coherence directly "
            f"(default: {DEFAULT_CFG['eta_runtime_min_coherence']})."
        ),
    )
    cfg.add_argument(
        "--stage5-mode-id",
        type=str,
        default=None,
        metavar="MODE_ID",
        help=(
            "Define one explicit experimental Stage 5 mode from direct CLI flags. "
            "When used without --selected-stage5-mode, this mode is promoted into "
            "the public count."
        ),
    )
    cfg.add_argument(
        "--stage5-score-key",
        type=str,
        choices=stage5_modes.SUPPORTED_MODE_SCORE_KEYS,
        default=None,
        metavar="SCORE_KEY",
        help="Score key for --stage5-mode-id.",
    )
    cfg.add_argument(
        "--stage5-calibration-policy",
        type=str,
        default=None,
        metavar="POLICY",
        help=(
            "Optional calibration policy for --stage5-mode-id. If omitted and "
            "manual-calibrated artifact paths are supplied, defaults to mode_artifact."
        ),
    )
    cfg.add_argument(
        "--stage5-threshold-source",
        type=str,
        default=None,
        metavar="SOURCE",
        help=(
            "Optional threshold-source label for --stage5-mode-id. If omitted and "
            "a score-admissibility artifact is supplied, defaults to "
            "manual_calibrated_mode_tau_v_star."
        ),
    )

    args = parser.parse_args()
    if args.selection_threshold is not None and args.selection_score is None:
        parser.error("--selection-threshold requires --selection-score")
    if (args.stage5_mode_id is None) != (args.stage5_score_key is None):
        parser.error("--stage5-mode-id and --stage5-score-key must be provided together")
    if (
        args.manual_calibrated_investigation_root is not None
        and args.manual_calibrated_mode is None
    ):
        parser.error(
            "--manual-calibrated-investigation-root requires --manual-calibrated-mode"
        )
    if (
        args.selection_score is not None
        and (
            args.stage5_mode_id is not None
            or args.stage5_score_key is not None
            or args.stage5_calibration_policy is not None
            or args.stage5_threshold_source is not None
        )
    ):
        parser.error(
            "--selection-score cannot be combined with the explicit --stage5-* mode flags"
        )
    if (
        args.stage5_mode_id is None
        and (
            args.stage5_calibration_policy is not None
            or args.stage5_threshold_source is not None
        )
    ):
        parser.error(
            "--stage5-calibration-policy and --stage5-threshold-source require "
            "--stage5-mode-id/--stage5-score-key"
        )
    return args


def build_cfg_from_args(args: argparse.Namespace) -> dict[str, Any]:
    """Merge CLI flags and an optional JSONL config file into one dict.

    Priority (highest to lowest):
      1. Explicit CLI flags (``--max-ions``, ``--min-snr``, …)
      2. JSONL config file (``--config``)
      3. ``DEFAULT_CFG``

    Parameters
    ----------
    args : argparse.Namespace

    Returns
    -------
    dict
        Merged configuration.
    """
    cfg: dict[str, Any] = {}

    # Layer 1: JSONL config file
    if args.config_file:
        cfg.update(load_config_file(args.config_file))

    # Layer 2: explicit CLI flags override the config file
    if args.max_ions is not None:
        cfg["max_ions"] = args.max_ions
    if args.min_snr is not None:
        cfg["min_accepted_matched_snr"] = args.min_snr
    if args.peak_distance is not None:
        cfg["peak_min_distance"] = args.peak_distance
    if args.dog_small is not None:
        cfg["dog_small_sigma"] = args.dog_small
    if args.dog_large is not None:
        cfg["dog_large_sigma"] = args.dog_large
    if args.enable_search_roi:
        cfg["enable_search_roi"] = True
    if args.search_rows is not None:
        cfg["search_row_fraction"] = tuple(args.search_rows)
    if args.search_cols is not None:
        cfg["search_col_fraction"] = tuple(args.search_cols)
    if args.corridor_width is not None:
        cfg["search_half_width"] = args.corridor_width
    apply_manual_calibrated_cli_overrides(cfg, args)
    selection_score = getattr(args, "selection_score", None)
    selection_threshold = getattr(args, "selection_threshold", None)
    selected_stage5_mode = getattr(args, "selected_stage5_mode", None)
    if selection_score is not None:
        selection_score = stage5_modes.canonicalize_score_key(selection_score)
        experimental_mode: dict[str, Any] = {
            "mode_id": f"cli_{selection_score}_ledger",
            "score_key": selection_score,
            "ledger_only": True,
        }
        if selection_threshold is not None:
            experimental_mode["threshold"] = selection_threshold
        cfg["experimental_stage5_modes"] = [experimental_mode]
    elif selection_threshold is not None:
        warnings.warn(
            "--selection-threshold is ignored without --selection-score.",
            stacklevel=2,
        )
    if selected_stage5_mode is not None:
        cfg["experimental_stage5_selected_mode"] = str(selected_stage5_mode)
    if getattr(args, "stage5_selected_noise_only", False):
        cfg["stage5_variant_noise_policy"] = "selected_noise_only"

    return cfg


def main() -> None:
    """CLI entry point: parse arguments, analyze frames, emit output."""
    args = parse_args()
    cfg = build_cfg_from_args(args)

    try:
        results = [analyze_path(path, cfg=cfg or None) for path in args.images]
    except (InputDataError, FileNotFoundError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    for result in results:
        print_summary(result)

    if args.jsonl_path:
        output_path = Path(args.jsonl_path)
        frame_records = to_builtin(results)
        with open(output_path, "w", encoding="utf-8") as f:
            schema_line = {
                "type": "schema",
                "data": {
                    "writer": "analyze_ions_fft",
                    "schema_version": "trapdetect-frame-jsonl-v1",
                    "n_inputs": len(results),
                },
            }
            f.write(json.dumps(schema_line, default=str, allow_nan=False) + "\n")
            for frame in frame_records:
                frame_line = {"type": "frame", "data": frame}
                f.write(json.dumps(frame_line, default=str, allow_nan=False) + "\n")

        if args.save_cube and len(results) > 1:
            spectral_cube = build_spectral_cube(results)
            cube_path = output_path.with_suffix(".npz")
            np.savez_compressed(
                cube_path,
                spectral_cube=spectral_cube,
                temporal_fft=np.abs(temporal_fft_cube(spectral_cube)) ** 2,
                temporal_laplace=temporal_laplace_cube(
                    spectral_cube,
                    dt=args.dt,
                    s_values=DEFAULT_CFG["temporal_laplace_s_values"],
                ),
            )


if __name__ == "__main__":
    main()
