# TrapDetect

TrapDetect analyzes trapped-ion images. It estimates how many ions are visible,
localizes accepted ions, and reports confidence and diagnostic information for
single frames, image sequences, and `.npz` camera archives.

The single-frame public claim surface is limited to image-local outputs:
visible-ion count, accepted-ion position and spacing, localized template or
noise estimates, and per-frame confidence diagnostics. TrapDetect does not claim that one frame
directly yields a radiative lifetime or that image statistics alone recover
collision, blackbody, or leakage-light corrections.

The repository includes example NPZ data in `run1/`. For the detector model,
black-box template assumptions, and stage-by-stage math, see [algorithm.md](algorithm.md).

## Documentation Map

These four documents are the maintained answer surface for the project:

| Question | Start here |
| -------- | ---------- |
| How do I install, run, validate, or inspect outputs? | [README.md](README.md) |
| What does the detector claim, mathematically and scientifically? | [algorithm.md](algorithm.md) |
| How do modules, data, artifacts, and risks connect? | [notes/project_architecture_mermaid.md](notes/project_architecture_mermaid.md) |
| What does a symbol, validation boundary, or thesis audit term mean? | [notes/thesis_academic_dictionary.jsonl](notes/thesis_academic_dictionary.jsonl) |

## Install

```text
python -m pip install numpy scipy scikit-image imageio
```

Optional:

- `pytest` to run the test suite
- `joblib` for the default CPU Joblib scheduler backend in `run_npz_batch.py`; use `--cpu-scheduler-backend executor` only when you intentionally want the legacy executor path
- `matplotlib` for custom plotting
- `psutil` to inspect process-usable CPU affinity and available RAM for batch-policy decisions
- `threadpoolctl` to clamp nested BLAS/OpenMP thread counts inside batch workers
- `nvidia-ml-py` for explicit VRAM admission checks when using the optional GPU lane
- `cupy` to offload the dense FFT/filter stages after a run is admitted to the GPU lane

If you use Jupyter, select a kernel with the same packages installed.

## Quick Start

### Jupyter

```python
from pathlib import Path
from run_npz_batch import run

batch = run(Path("run1/photon_count0.npz"), frames_per_file=1, max_workers=1)
print(batch["runs"]["photon_count0"]["summary"]["modal_ion_count"])
```

### Command line

```text
python run_npz_batch.py -a --auto-bundle run1/photon_count0.npz
```

This analyzes the archive and writes an auto-named NPZ bundle. To inspect the
bundle as readable JSONL:

```text
python extract_npz_json.py trapdetect_results_*.npz out/
```

See the later Jupyter and CLI sections for bundle details, JSONL schema notes,
and larger workflows.

All filenames in examples below (`out/`, `run1_bundle.npz`, `frame.jsonl`,
etc.) are placeholders — substitute whatever paths you want.

## Choose Your Workflow

| Situation | Use this API or CLI | Main output |
| --------- | ------------------- | ----------- |
| One frame already in memory or one image on disk | `analyze_ions_fft.analyze_array()` / `analyze_path()` or `analyze_ions_fft.py` | One frame result `dict` |
| Several ordinary image files | `run_batch()` or `analyze_batch.py` | Batch `dict` with per-run reducers (`frames`, `series_stats`, `state_matrix`) |
| One `.npz` archive or a directory of archives | `run()` or `run_npz_batch.py` | Top-level batch `dict` with multi-run aggregation, bundle writing, and parallel loading/analysis |
| A bundle `.npz` you want to inspect or export | `extract_npz_json()` or `extract_npz_json.py` | Readable JSONL files, `batch_summary.jsonl`, and typed variant audit rows |
| Manual-review-driven detector calibration, starting from either an existing review CSV or a newly selected review-image set | `tools/manual_review/export_flagged_review_frames.py` -> `tools/manual_data/rebuild_manual_test_data.py` or default auto-rebuild -> `tools/manual_detector_update.py` | Review PNGs, `manual_count_template.csv`, detector-update dataset NPZ, per-variant calibration artifacts, override JSONL, and update report |

For manual review, the intended operator chain is:

`tools/manual_review/export_flagged_review_frames.py` -> edit `manual_count_template.csv` -> rebuild or auto-rebuild detector-update dataset -> `tools/manual_detector_update.py`

The mainline mediation chain is:

`analyze_ions_fft.py` -> `analyze_batch.py` -> `run_npz_batch.py` -> `extract_npz_json.py` / `calculate_lifetime_precision.py`

Large-job parallelization, memory budgeting, and scratch-flow management remain concentrated in `run_npz_batch.py`.

For library imports, prefer the root modules that now own the runtime surface:

- `analyze_ions_fft`, `working_image`, `stage4`, `stage5`, and `stage6` for single-frame detector entrypoints and staged helpers
- `runner`, `orchestration`, `frame_staging`, `npz_frames`, `bundle_io`, `scratch_io`, and `snr_variant_jsonl` for batch orchestration helpers
- `manual_count_paths`, `manual_review_contract`, and `npz_frame_access` for manual-review and frame-access helpers

The root scripts and modules are now the canonical public entrypoints for both CLI and library use.

For the canonical single-frame runtime, Stage 3--5 operate on a dense
background-corrected full-frame working image by default. Legacy ROI
restriction and Gaussian warning-count repairs remain explicit compatibility
gates rather than canonical defaults.

## Use From Jupyter

### Single frame

Use `analyze_array()` when you already have one frame loaded in memory.

```python
import numpy as np
from analyze_ions_fft import analyze_array

with np.load("run1/photon_count0.npz", allow_pickle=True) as data:
        frame0 = data["camera_images"][0]

result = analyze_array(frame0, source_name="photon_count0/frame_000")
print(result["state"]["visible_ion_count"])
print(len(result["detections"]))
```

If your frame is already on disk as an image file, use `analyze_path()` instead.

### Image sequence

Use `run_batch()` for several ordinary image files.

```python
from analyze_batch import run_batch

batch = run_batch(["frame_000.png", "frame_001.png", "frame_002.png"], max_workers=4)
print(batch["series_stats"]["modal_ion_count"])
print(batch["frames"][0]["state"]["visible_ion_count"])
```

### NPZ archive or archive directory

Use `run()` when your data is stored in `.npz` camera archives. It accepts
either a single `.npz` file or a directory containing many `photon_count*.npz`
archives.

```python
from pathlib import Path
from run_npz_batch import run

batch = run(Path("run1"), max_workers=1)
print(list(batch["runs"].keys()))

run0 = batch["runs"]["photon_count0"]
print(run0["summary"]["modal_ion_count"])
print(run0["position_matrix"]["x_px"].shape)
```

Use the batch CLI with `--detector-module` when you want the same archive flow
to run through an alternate single-frame detector module, for example the
experimental float32 path:

```text
python run_npz_batch.py --detector-module analyze_ions_fft_float32 --stage5-selected-noise-only --auto-bundle run1
```

### Bundle extraction

After creating a bundle `.npz`, use `extract_npz_json()` to write readable JSONL
files and a batch-level summary.

```python
from extract_npz_json import extract_npz_json

result = extract_npz_json(
    "your_bundle.npz",
    "out",
    overwrite=True,
    summary_only=True,
)
print(result["batch_summary"])
```

## Use From the Command Line

### Single frame (CLI)

```text
python analyze_ions_fft.py --jsonl frame.jsonl frame_a.png
```

Use this when you want one JSONL result for one image file. The output
filename (`frame.jsonl`) is a placeholder.

### Image sequence (CLI)

```text
python analyze_batch.py --jsonl sequence.jsonl --images frame_000.png frame_001.png frame_002.png
```

Or pass a text file with one path per line:

```text
python analyze_batch.py --jsonl sequence.jsonl test_sequence.txt
```

### NPZ archive or archive directory (CLI)

Analyze one archive; auto-name the bundle:

```text
python run_npz_batch.py -a --auto-bundle run1/photon_count0.npz
```

The intended default batch workflow is bundle-first: the initial
`run_npz_batch.py` command writes a frame-stats-only NPZ bundle, and any JSONL
extraction or run/batch reductions happen afterwards in separate commands.

Extract readable JSONL after the bundle has been written:

```text
python extract_npz_json.py your_frame_stats_bundle.npz out/
```

Add deferred run-level and batch-level reductions afterwards:

```text
python run_npz_batch.py --reduce-existing-bundle your_frame_stats_bundle.npz --with-run-stats --with-batch-stats --bundle-npz your_derived_stats_bundle.npz
```

Analyze a directory of archives with the default all-frame configuration, the
default Joblib CPU scheduler, and preserved bundle-only scratch so the batch
can be resumed later:

```text
python run_npz_batch.py --auto-bundle --keep-temp C:\Users\isaia\Desktop\run1
```

Pure bundle runs now use bundle-only scratch automatically. When you request
only the bundle output (`--auto-bundle`, `--bundle-npz`, or the implicit
default bundle path) and do not also ask for `--jsonl` or `--xy-matrix`,
TrapDetect keeps lightweight finalized per-run sidecars plus bundle/meta
sidecars and omits raw `frames__*.npz` scratch payloads. With `--keep-temp`,
that scratch stays under a stable `.trapdetect-resume/<signature>/` directory
near the input source, and a later `--resume` run can reuse completed runs
without restaging raw frames. Use `--scratch-dir PATH` when you want the
scratch tree somewhere else.

If you also need a JSONL manifest, request it explicitly; that switches the
scratch flow back to the full mode because the extra sidecars still need the
frame-backed data:

```text
python run_npz_batch.py --bundle-npz run1_bundle.npz -j run1.jsonl C:\Users\isaia\Desktop\run1
```

TrapDetect now auto-materializes a durable cleaned-image dataset under
`cleaned_integer_images/` next to the raw source when it first analyzes raw
`photon_count*.npz` input. The cleaned dataset stores only the analysis-facing
fields, rewrites `camera_images` into a numeric cleaned NPZ, prefers `uint8`
for nonnegative `0..255` camera data and widens only when the observed range
requires it, and reuses that permanent copy on later runs so loader startup no
longer depends on the raw object-array path. To keep the one-time cleaning pass
fast, cleaned `uint8` archives are written without ZIP compression; wider dtypes
continue to use the compressed writer. Batch runs now do that cleaning in a
bounded pre-clean stage before analysis starts, then analyze only against the
prepared cleaned data.

If you want to build that durable cleaned dataset ahead of time, use the
separate cleaning utility:

```text
python tools/manual_data/materialize_cleaned_integer_images.py run1
```

If you want to benchmark the cleaned-archive path directly, use:

```text
python tools/manual_data/benchmark_cleaned_npy_vs_npz.py run1
```

On Windows, add `--inhibit-sleep` for long runs when you also want the CLI to
make a best-effort request that the machine stay awake while preserving the
scratch files:

```text
python run_npz_batch.py --auto-bundle --inhibit-sleep C:\Users\isaia\Desktop\run1
```

If scratch is preserved in this mode and you did not override `--scratch-dir`,
TrapDetect relocates it next to the written bundle in a visible sibling folder
named after that bundle, for example
`trapdetect_results_2026-05-15_at08h51m47s_rt00h12m03s_100npz.scratch/` next
to the matching auto-named `.npz` bundle.

The default batch configuration already analyzes all frames. The default CPU
path uses the Joblib scheduler backend: TrapDetect stages one run, lets Joblib
auto-batch per-frame work, derives CPU worker width and loader width
automatically, and keeps the deprecated GPU lane disabled unless you
explicitly pass `--gpu-device ...`. Use `-f N` only when you intentionally
want sampling. For NPZ loading, the current RAM-based auto cap is
intentionally simple:
available memory at or below 2 GiB forces one loader, available memory at or
below 8 GiB caps the loader pool at two, and higher-memory hosts stay on a
small bounded window of at most four concurrent loaders. When you need an
apples-to-apples benchmark, pin both `--workers` and `--npz-workers` instead
of comparing auto-derived modes.

The chunked frame-pool path is now legacy and only matters when you explicitly
opt into `--cpu-scheduler-backend executor`. In that legacy executor mode,
`--frame-pool-chunk-mode single` keeps one staged shard per run, `half` keeps
at most two, `quarter` keeps up to four, and `auto` falls back to the finer
byte-sized sharding behavior from the internal 64 MiB cap:

```text
python run_npz_batch.py --cpu-scheduler-backend executor --frame-pool-chunk-mode single --auto-bundle C:\Users\isaia\Desktop\run1
```

For large exact CPU batches, the default Joblib runtime derives its process-
pool width from process-usable logical CPUs, current affinity, available RAM,
and loaded BLAS/OpenMP threadpools, then clamps nested numeric libraries
inside each worker automatically. In most cases, leave `--workers`,
`--worker-inner-threads`, and `--fft-workers` unset:

```text
python run_npz_batch.py --auto-bundle C:\Users\isaia\Desktop\run1
```

Use explicit worker and thread flags only when you need a fixed benchmark or a
reproducible manual override. `analyze_batch.py` exposes the same
`--worker-inner-threads` and `--fft-workers` flags for image-path batches.

The optional GPU lane is run-level and conservative: a run is staged once,
assigned to the GPU only when the sampled free VRAM exceeds the estimated
float64 working set plus reserved headroom, and otherwise stays on the CPU
pool. Enable it with `--gpu-device auto` to pick the best CUDA-visible device,
or pass a stable selector such as a CUDA ordinal, UUID, PCI bus ID, or exact
device name:

```text
python run_npz_batch.py --bundle-npz run1_bundle.npz \
    --gpu-device auto --gpu-headroom-frac 0.25 --gpu-min-headroom-mib 256 \
    run1
```

The GPU scheduler is also explicit. The default `--gpu-scheduler spill`
submits an admitted run to the GPU only when the single GPU lane is idle and
otherwise spills that run back to the CPU pool. Experimental `queue-one`,
`queue-two`, and `queue-all` modes keep admitted runs waiting for the GPU
instead of spilling immediately. Current measured `run3` benchmarks in
`analysis_outputs/run3_first20_gpu_scheduler_benchmark.json` and
`analysis_outputs/run3_first10_fixed_policy_gpu_scheduler_benchmark.json`
showed those queued modes were substantially slower and changed summary
digests relative to the default spill baseline, so keep `spill` for production
analysis and use the queued modes only for targeted GPU investigations.

On mixed integrated/discrete Windows systems, `--gpu-device auto` resolves
against CUDA-visible devices rather than the OS display adapter numbering, so
it prefers the discrete NVIDIA adapter when that is the only CUDA target. The
batch metadata records both the requested selector and the resolved device
identity (`device_id`, UUID, PCI bus ID, and name).

If CUDA, CuPy, or NVML is unavailable, TrapDetect leaves the run on the CPU
lane and records that decision in the batch metadata instead of failing open.

For controlled runtime comparisons, use `tools/manual_data/benchmark_npz_batch_modes.py`.
It records wall time, effective worker policy, GPU scheduler telemetry, and a
summary digest so output drift is visible alongside performance changes. Pin
both worker widths when you want a scheduler-only comparison; otherwise the
auto loader policy can change between modes and confound the result. The same
tool records the requested and effective `frame_pool_chunk_mode` for legacy
executor comparisons, so you can do chunk-policy comparisons with the same
JSON report. Named presets include
`cpu-auto-single`, `cpu-auto-half`, `cpu-auto-quarter`, `cpu-auto-auto`, and
`hybrid-auto-quarter`:

```text
python tools/manual_data/benchmark_npz_batch_modes.py \
    --max-files 10 \
    --mode hybrid-auto \
    --mode hybrid-queue-one \
    --mode hybrid-queue-two \
    --mode hybrid-queue-all \
    --override-workers 16 \
    --override-npz-workers 2 \
    --json-out analysis_outputs/run1_first10_fixed_policy_gpu_scheduler_benchmark.json \
    run1
```

Use `--auto-bundle` when you want an auto-named output; use
`--bundle-npz PATH` to choose the filename yourself. The two flags are
mutually exclusive. `run_npz_batch.py` accepts exactly one positional
input path, and the examples here put it last so you can reuse the option
prefix and swap sources without rewriting the rest of the command. Auto-named
bundles now include the calendar date, military clock time, measured runtime,
and run count, for example
`trapdetect_results_2026-05-11_at15h42m08s_rt00h21m22s_100npz.npz`.

Advanced NPZ utilities that used to live in standalone helper scripts now
live under `run_npz_batch.py` too:

```text
python run_npz_batch.py -n 7 \
    --snr-variant-jsonl analysis_outputs/run1_first7_snr_variant_counts.jsonl \
    run1
```

```text
python run_npz_batch.py \
    --snr-variant-compact analysis_outputs/run1_first7_snr_variant_count_compact.jsonl \
    analysis_outputs/run1_first7_snr_variant_counts.jsonl
```

### Bundle extraction (CLI)

Extract readable per-run JSONL files from a bundle:

```text
python extract_npz_json.py run1_bundle.npz out/
```

Write only the batch-level summary file:

```text
python extract_npz_json.py --summary_only run1_bundle.npz out/
```

For supported bundles, that batch-level extraction is now the report surface as
well: `batch_summary.jsonl` includes typed lifetime report rows such as
`lifetime_mode_summary`, `lifetime_mode_comparison`, `lifetime_mode_selection`,
`lifetime_mode_diagnostics`, `lifetime_mode_histogram`, and
`lifetime_mode_fit_state`, and the extractor also writes companion
`lifetime_report.json` and `lifetime_report.md` files in the same output
directory.

The extractor accepts either `--out-dir PATH` or a trailing `OUT_DIR`
positional argument. It also accepts both `--summary-only` and
`--summary_only`.

### Lifetime precision (CLI)

Compute the batch transition-time precision directly from the batch bundle
`.npz` written by `run_npz_batch.py`, or from the top-level manifest JSONL or
the extracted `batch_summary.jsonl`. The default path is the bundle itself, so
you can point the calculator straight at `input.npz` without running the
extractor first. The CLI emits grouped, row-oriented JSONL to stdout and can
also write it to a `.jsonl` file. Large sections are distributed across
multiple row types, but each row keeps directly related fields together: one
row per observational metric, one self-contained row per component, and a few
grouped lifetime-summary rows instead of one monolithic nested payload.

With no extra flags, the calculator now derives the internal camera-diagnostic
systematics it can actually measure from the batch data: detection ambiguity,
near-threshold false-dark risk, and timing-boundary jitter. External physics
terms such as collision, blackbody, and leakage-light corrections still require
explicit inputs.

```text
python calculate_lifetime_precision.py input.npz
```

Here `input.npz` means the TrapDetect bundle created by `run_npz_batch.py`, not
the raw camera archive such as `run1/photon_count0.npz`. For bundle inputs the
default `auto` measurement mode now prefers an epoch-statistics estimate built
from cumulative non-final epoch transition times. If you want the older emitted
batch transition mean instead, pass `--measurement-mode batch_transition`. Two
explicit paper-inspired bundle modes are also available:
`--measurement-mode paper_weighted_brightening` for monotone cumulative bright
transitions and `--measurement-mode paper_k_interval_least_squares` for the
multi-state interval-rate fit. Three additional report-oriented bundle modes are
also available: `--measurement-mode paper_nonfinal_interval` for the pooled
non-final interval histogram, `--measurement-mode paper_segmented_brightening`
for contiguous brightening chains, and `--measurement-mode paper_segmented_darkening`
for contiguous darkening chains.

```text
python calculate_lifetime_precision.py input.npz --jsonl-out run1_precision.jsonl
```

If you already have extracted JSONL, that still works too:

```text
python calculate_lifetime_precision.py out/batch_summary.jsonl --jsonl-out run1_precision.jsonl
```

JSONL or manifest inputs still use the stored `batch_transition_lifetime`
summary because they do not carry the per-run epoch rows needed for the bundle
epoch toolset.

If you want to suppress one of the default SNR-grounded internal bounds, use
the corresponding opt-out flag:

```text
python calculate_lifetime_precision.py input.npz --no-snr-detection --no-snr-heating
```

Add explicit paper-grounded physical inputs such as collision or blackbody
rate corrections, leakage-light bounds, heating or detection fractional bounds,
and timing corrections.

```text
python calculate_lifetime_precision.py input.npz \
    --collision-rate-correction 0.0015 \
    --collision-rate-uncertainty 0.0005 \
    --blackbody-rate-correction 0.0002 \
    --leakage-rate-uncertainty 0.0003 \
    --heating-false-dark-fraction 0.01 \
    --timing-uncertainty 0.02 \
    --jsonl-out run1_precision.jsonl
```

Generic manual terms are still available with repeated `--systematic
NAME=SECONDS`, `--systematic-rate NAME=S_INV`, `--systematic-fraction
NAME=FRACTION`, `--rate-correction NAME=S_INV`, and `--lifetime-correction
NAME=SECONDS` flags.

Select specific runs:

```text
python extract_npz_json.py run1_bundle.npz -o out/ --run 0 --run 2
```

`--run` accepts a canonical name such as `photon_count0`, a group name such as
`run_photon_count0`, or a numeric index such as `0`.

## Authored Validation Notes

Keep authored validation notes separate from generated outputs.

- Generated artifacts belong under `analysis_outputs/`.
- Authored validation narratives belong under `notes/`.

Use the helper below to create a note stub in `notes/` without writing into the
generated-output tree:

```text
python tools/create_validation_note.py "run1 validation audit" \
    --source analysis_outputs/run1_validation/run1_default_report_allframes.md \
    --source analysis_outputs/run1_validation/extracted_default_allframes/batch_summary.jsonl
```

The helper always resolves the file inside `notes/` and rejects path-like note
names so generated and authored artifacts stay separate.

## Utility Tools

Non-pipeline utility scripts now live under `tools/` so the repo root stays
reserved for the main analysis chain and public entrypoints.

- `tools/manual_review_session.py`: historical/session-based review-session
    preparation and replay helper. The current detector-update corpus is rebuilt
    directly from `manual_count_template.csv` with `tools/manual_data/rebuild_manual_test_data.py`.
- `tools/manual_review/export_flagged_review_frames.py`: generate a bounded
    review-image set plus `manual_count_template.csv`, or rerender an existing
    review CSV with detector overlays and optional ledger-only Stage 5 modes.
- `tools/manual_detector_update.py`: primary manual-review calibration entrypoint.
    It consumes the detector-update dataset NPZ or the default auto-rebuilt
    corpus, emits branch-local score-admissibility plus variant-count-legibility
    artifacts for all four public variants, runs the canonical fixed-point
    validation loop, and runs one additional fixed-point subpass for each
    configured ledger-only Stage 5 selection mode.
- `tools/manual_mode_parity.py`: one-command live parity sweep for accepted
    named manual-calibrated presets against the detector-update corpus from
    `manual_count_template.csv`.
- `tools/manual_data/`: manual-review rebuild, inspection, and smoke-check tools
    for detector-update and legacy manual-review artifacts.
- `tools/manual_review/`: CSV/manifest comparison and summary probes for the
    manual-review audit inputs, including overlay rerenders for existing review
    CSVs and the generated review-image sets.
- `manual_calibrated_mode_presets/`: repo-local accepted post-fixed-point
    manual-calibrated preset bundle used by `--manual-calibrated-mode`.
- Root modules such as `analyze_ions_fft`, `runner`, `orchestration`,
    `manual_review_contract`, and `npz_frame_access` are the canonical import
    targets for new code.
- Public root CLIs such as `analyze_ions_fft.py`, `analyze_batch.py`,
    `run_npz_batch.py`, `extract_npz_json.py`, and
    `calculate_lifetime_precision.py` remain supported public entrypoints.
- `tools/create_validation_note.py` is the note-stub helper; it is no longer a
    root entrypoint.

Rebuild the current detector-update manual dataset from the root review CSV and
precleaned source archives:

```text
python tools/manual_data/rebuild_manual_test_data.py --format npz --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --output manual_review_detector_update/manual_test_data_from_manual_count_template.npz
```

Build the JSONL view of the same detector-update corpus:

```text
python tools/manual_data/rebuild_manual_test_data.py --format jsonl --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --output manual_review_detector_update/manual_test_data_from_manual_count_template.jsonl
```

If CSV content is piped from the current editor buffer, stdin takes priority
over `--review-csv`; keep the same `--source-npz-dir` and `--output` arguments.

Run the manual-review batch smoke check from its new location:

```text
python tools/manual_data/focused_check.py
```

Print a quick summary of the legacy canonical manual-review NPZ used by older
tests:

```text
python tools/manual_review/summarize.py
```

## Understanding the Output

- `result["state"]["visible_ion_count"]`: final ion count for one frame. This
    is usually the first value to inspect.
- `result["detections"]`: accepted ions for that frame. Each detection includes
    fields such as `row`, `col`, and `matched_snr`.
- `batch["series_stats"]["modal_ion_count"]`: most common ion count across an
    image sequence.
- `run0["summary"]["modal_ion_count_candidates"]`: tied modal ion counts when the
    run has no unique mode. In that case `off_modal_frame_fraction` excludes all
    tied modal counts instead of arbitrarily picking one winner.
- `run0["summary"]`: per-archive rollup for an `.npz` run, including counts,
    diagnostics, and epoch summaries.
- `run0["position_matrix"]`: dense per-ion matrices such as `x_px` and `y_px`.
    Shapes are `(n_ions, n_frames)`.
- `run0["summary"]["ion_count_epochs"]`: contiguous stretches of frames with
    the same visible ion count. `decrease_flag` marks a drop in count when one is
    detected.
- `batch_summary.jsonl`: a JSONL summary file written by `extract_npz_json.py`
    with a `type="schema"` header row, one `type="batch_transition_lifetime"` row
    carrying fields such as `n_runs_included`, `included_runs`, `excluded_runs`,
    and `bundle_schema_version`, one `type="snr_variant_batch_summary"` row per
    variant when v8 batch-variant fields are present, plus per-run
    `type="included_run"` / `type="excluded_run"` rows.

### Confidence and diagnostic fields

`psf_valid` and `evidence_margin_basis` tell you whether the
`evidence_margin` is meaningful.

- If `evidence_margin_basis == "psf_valid"`, the selected per-frame template
    was usable for matched filtering and the evidence margin is interpretable.
- If the basis is `psf_undersampled` or `no_boundary`,
    `evidence_margin` may be unavailable. In Python results this can appear as
    `NaN`; in JSONL it becomes `null`. This is a diagnostic condition, not a
    crash.

`psf_valid` no longer means “FFT-confirmed Gaussian PSF”. It now means the
selected per-frame template was usable for the matched-filter detector. The
separate regime flags such as `psf_gaussian` still report whether the Fourier
envelope fit looked Gaussian-like.

### JSONL output

`run_npz_batch.py -j ...` writes optional typed JSON Lines sidecars (the
NPZ bundle remains the primary output). The first row is a `schema`
record, and later rows include records such as `meta`, `summary`,
`frame`, `epoch`, and `epoch_summary`. Output is strict-valid JSON:
non-finite floats are written as `null`, never bare `NaN` or `Infinity`.
Extractor `type: "epoch"` rows now keep the raw epoch lifetimes and also add
`transition_sample_retained`, `transition_frame_lifetime`, and when available
`transition_real_time_lifetime_s` so the cumulative safe-prefix transition
logic is visible after extraction.

### Bundle reduction before lifetime calculation

`run_npz_batch.py --auto-bundle` writes a frame-stats bundle by default.
`calculate_lifetime_precision.py` expects a derived bundle that already
contains run-level and batch-level transition statistics such as
`batch_transition_lifetime_*` fields.

Use one of these two supported paths:

Create the derived statistics when the bundle is written:

```text
python run_npz_batch.py --auto-bundle --with-run-stats --with-batch-stats run1/photon_count0.npz
```

Or post-reduce an existing frame-only bundle before running the lifetime tool:

```text
python run_npz_batch.py --reduce-existing-bundle your_bundle.npz --with-run-stats --with-batch-stats --bundle-npz your_bundle_derived_stats.npz
python calculate_lifetime_precision.py your_bundle_derived_stats.npz --measurement-mode auto --jsonl-out analysis_outputs/your_bundle_lifetime.jsonl
```

If you skip the reduction step, the lifetime tool will not find the derived
transition metrics it needs and will fail against a frame-only bundle.

## Requirements and Limits

- Input arrays must be grayscale, finite, and integer-valued at acquisition
    time. Boolean arrays are rejected.
- Every `.npz` used with `run_npz_batch.py` must contain a `camera_images`
    array.
- The pipeline assumes one approximately vertical ion chain in each frame.
- Ion labels are top-to-bottom ordinals within a frame. They are not
    cross-frame identity tracks.
- `run_npz_batch.py` analyzes all frames by default. Use `-f N` only when you
    intentionally want evenly spaced sampling.

## Testing

Run the full test suite:

```text
python -m pytest -q
```

Run the smoke path documented above:

```text
python run_npz_batch.py -a --auto-bundle run1/photon_count0.npz
```

## Project Files

| Path | Purpose |
| ---- | ------- |
| `analyze_ions_fft.py` | Single-frame detector and SNR-variant source of truth |
| `analyze_ions_fft_float32.py` | Experimental mixed-precision detector module that keeps the canonical result contract while routing heavy Stage 3/4/5 image kernels through float32 |
| `analyze_batch.py` | Per-run reduction for ordinary image files and reducer ownership layer |
| `run_npz_batch.py` | Multi-run `.npz` orchestration, bundle writing, and parallel resource control |
| `stage5_modes.py` | Stage 5 canonical/experimental mode specifications and nested ledger helpers |
| `extract_npz_json.py` | Convert bundle `.npz` files to readable JSONL, including v7 variant rows |
| `notes/project_architecture_mermaid.md` | Architecture diagrams, risk matrix, and document ownership map |
| `notes/thesis_academic_dictionary.jsonl` | Symbol dictionary, validation boundaries, and thesis audit rules |
| `run1/` | Example NPZ input data |
| `tests/` | Automated test suite |

## More Detail

- [algorithm.md](algorithm.md) explains the detector model, PSF assumptions,
    heuristics, and decision metrics in more depth.
- The tests in `tests/` are a good source of small, verified usage examples.

## Iterative Detector Update Pipeline

The iterative manual-review pipeline is intentionally local and reversible.
`tools/manual_detector_update.py` is the primary operator entrypoint once you
have a review CSV. It produces bundle-backed calibration artifacts plus a JSONL
override file, and `run_npz_batch.py --config ...` applies that override to one
batch invocation only. This does not mutate the default detector config in
`analyze_ions_fft.py` or `run_npz_batch.py`.

Two starts are supported.

If you do not have a review CSV yet, first generate a review folder containing
selected review PNGs plus a template CSV. The `--limit` value is the requested
review-set size:

```text
python tools/manual_review/export_flagged_review_frames.py --bundle-npz your_bundle.npz --limit 120 --output-dir manual_review_detector_update/review_round_01
```

That writes `images/`, `review_manifest.jsonl`, and `manual_count_template.csv`
under the chosen output directory. If you already have a review CSV and want to
rerender those same rows with the current detector or with a ledger-only Stage 5
selection mode, use the same tool in `--review-csv` mode.

The current detector-update corpus is centered on the root
`manual_count_template.csv` and the precleaned NPZ source directory
`C:/Users/isaia/Desktop/run3_5926_precleaned`. Rebuild the detector-update NPZ
directly from those two inputs:

```text
python tools/manual_data/rebuild_manual_test_data.py --format npz --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --output manual_review_detector_update/manual_test_data_from_manual_count_template.npz
```

The rebuild helper now treats copied `manual_count_template.csv` files without
their own sibling manifests as detector-update CSVs too. That keeps saved
review-session copies on the same direct CSV-plus-precleaned-NPZ rebuild path
instead of falling back to the generic manifest-based manual-review builder.

If you keep the canonical review CSV at the repo root and use the default
detector-update dataset path, `tools/manual_detector_update.py` resolves that
dataset automatically and rebuilds it when the CSV or source NPZ directory has
changed. The shortest canonical command is therefore:

```text
python tools/manual_detector_update.py --fixed-point-verbose-log --trace-noise-window-log
```

Build the local detector override from that rebuilt dataset:

```text
python tools/manual_detector_update.py --dataset-npz manual_review_detector_update/manual_test_data_from_manual_count_template.npz --fixed-point-verbose-log --trace-noise-window-log
```

That command writes the update report and reversible override under
`analysis_outputs/manual_detector_update/` by default. The override is plain
JSONL and can be passed to entrypoints that support `--config`, for example:

```text
python analyze_ions_fft.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl frame.png
```

For the canonical detector module, that command runs an iterative fixed-point
calibration loop: validate against scored manual-review rows, rebuild the
branch eta and threshold artifacts from the resulting branch assignments, then
repeat until the strict mismatch set and branch artifact summaries stop moving
or the deterministic iteration cap is reached.

The implemented artifact scope is wider than the top-level selected count.
Every detector-update solve emits `score_admissibility` and
`variant_count_legibility` artifacts for all four public variants:

- `anisotropic_gaussian`
- `symmetric_gaussian`
- `anisotropic_poisson`
- `symmetric_poisson`

If the validation config also defines ledger-only experimental Stage 5 modes,
the tool runs one additional fixed-point subpass for each configured mode under
`analysis_outputs/manual_detector_update/_fp_modes/<mode_id>/`. Those mode
subpasses keep the four public variants intact, rebuild mode-local threshold
and eta artifacts against the selected mode, and then thread the resulting
artifact paths back into `manual_detector_override.jsonl` so later validation
or rerender commands can apply them without hand editing.

The generated `manual_detector_update.md` report is organized into artifact,
parameter-policy, calibration, validation, and fixed-point convergence
sections so the iteration history is explicit rather than implied.

The current fixed-point trace should be read as an audit artifact, not as proof
that canonical strict manual parity has already been achieved.

For the canonical minimal-upgrade path, only these calibration knobs are meant
to move:

- `eta_max_abs_correction`
- `eta_runtime_min_coherence`

The academic defaults used for canonical validation remain fixed:

- `search_row_fraction = [0.0, 1.0]`
- `search_col_fraction = [0.0, 1.0]`
- `search_half_width = 10000`
- `enable_gaussian_warning_count_corrections = False`

That fixed policy matches the shipped canonical runtime as well: the default
single-frame path already uses full-frame corrected-image Stage 3--5 routing,
and the legacy Gaussian warning-count repair path stays off unless a
compatibility-oriented run explicitly re-enables it.

`--validation-config` is therefore reserved for explicitly experimental runs,
for example when validating a noncanonical detector module. Canonical
detector-update runs reject nonacademic validation overrides rather than
silently merging them into the override file.

### Named Manual-Calibrated Presets

`analyze_ions_fft.py` and `run_npz_batch.py` now expose
`--manual-calibrated-mode` as a simple selector for accepted post-fixed-point
manual-calibrated presets. The default preset root is the repo-local
`manual_calibrated_mode_presets/` bundle, so these named presets no longer
depend on preserving a historical `analysis_outputs/...` investigation tree.

Example single-frame invocation:

```text
python analyze_ions_fft.py --manual-calibrated-mode mode_integrated_snr frame.png
```

Example batch invocation:

```text
python run_npz_batch.py --manual-calibrated-mode mode_integrated_snr --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned
```

The accepted named presets are:

- `manual_calibrated_canonical`
- `mode_integrated_snr`
- `mode_support_mean_excess_snr`
- `mode_support_sum_snr`
- `mode_template_support_excess_density`

On the current strict manual-count corpus derived from
`manual_count_template.csv` there are 113 strict scored frames. The live
parity results for these presets are:

- `manual_calibrated_canonical`: `111 / 113`
- `mode_integrated_snr`: `113 / 113`
- `mode_support_mean_excess_snr`: `111 / 113`
- `mode_support_sum_snr`: `113 / 113`
- `mode_template_support_excess_density`: `113 / 113`

The current candidates for future canonical-mode promotion are therefore:

- `mode_integrated_snr`
- `mode_support_sum_snr`
- `mode_template_support_excess_density`

This is a candidate set, not a claim that the shipped canonical default has
already changed. The ordinary canonical runtime still defaults to the current
canonical matched-SNR path unless one of these presets is selected explicitly.

Run the one-command live parity sweep for these named presets against the
detector-update corpus derived from `manual_count_template.csv`:

```text
python tools/manual_mode_parity.py
```

Restrict the sweep to one named preset and emit structured JSON instead of the
human-readable summary:

```text
python tools/manual_mode_parity.py --mode mode_integrated_snr --json
```

### Current Batch And Mode-Ledger Commands

Run the current detector-update override across a source archive directory. The
input path is last so the command can be reused with another directory:

```text
python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned
```

Run the full manual-count detector performance sweep when testing Stage 5 mode
selection. This builds the 120-row NPZ from
`C:\Users\isaia\Desktop\trapdetect\manual_count_template.csv`, configures all
eight supported selection/threshold modes, runs the manual detector update with
verbose fixed-point logging and the trace/noise-window log, then creates the
histogram report. The run is intentionally wide: the canonical pass and each
`_fp_modes/<mode_id>` pass still record the public SNR variants, so selection
modes multiply the amount of per-variant diagnostic output.

```powershell
Set-Location "C:\Users\isaia\Desktop\trapdetect"

$ReviewCsv = "C:\Users\isaia\Desktop\trapdetect\manual_count_template.csv"
$SourceNpzDir = "C:\Users\isaia\Desktop\run3_5926_precleaned"
$OutDir = "analysis_outputs\manual_detector_update_all_selection_methods_120csv_fixed"
$DatasetNpz = "manual_review_detector_update\manual_test_data_from_manual_count_template.npz"
$ValidationConfig = Join-Path $OutDir "all_selection_methods.validation.jsonl"
$TraceJsonl = Join-Path $OutDir "manual_detector_trace_noise_window.jsonl"
$HistogramDir = Join-Path $OutDir "histograms"

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Set-Content -Encoding ascii -Path $ValidationConfig -Value @'
{"experimental_stage5_modes":[{"mode_id":"matched_snr_manual_calibrated","score_key":"matched_snr","ledger_only":true},{"mode_id":"integrated_snr_manual_calibrated","score_key":"integrated_snr","threshold":5.6,"ledger_only":true},{"mode_id":"support_sum_snr_manual_calibrated","score_key":"support_sum_snr","ledger_only":true},{"mode_id":"local_support_sum_snr_robust_manual_calibrated","score_key":"local_support_sum_snr_robust","threshold":5.6,"ledger_only":true},{"mode_id":"support_mean_excess_snr_manual_calibrated","score_key":"support_mean_excess_snr","ledger_only":true},{"mode_id":"robust_peak_snr_manual_calibrated","score_key":"robust_peak_snr","ledger_only":true},{"mode_id":"template_support_excess_density_manual_calibrated","score_key":"template_support_excess_density","threshold":0.02,"ledger_only":true},{"mode_id":"template_ncc_score_manual_calibrated","score_key":"template_ncc_score","ledger_only":true}]}
'@

.\.venv\Scripts\python.exe tools/manual_data/rebuild_manual_test_data.py --format npz --review-csv $ReviewCsv --source-npz-dir $SourceNpzDir --output $DatasetNpz

.\.venv\Scripts\python.exe tools/manual_detector_update.py --dataset-npz $DatasetNpz --output-dir $OutDir --validation-config $ValidationConfig --fixed-point-verbose-log --trace-noise-window-log

.\.venv\Scripts\python.exe tools/manual_detector_trace_histograms.py $TraceJsonl --output-dir $HistogramDir
```

Primary outputs from that sweep are:

```text
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/manual_detector_override.jsonl
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/manual_detector_update_fixed_point_verbose.jsonl
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/manual_detector_trace_noise_window.jsonl
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/manual_detector_trace_noise_window.md
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/_fp_modes/<mode_id>/manual_detector_update_fixed_point_verbose.jsonl
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/histograms/manual_detector_trace_histograms.pdf
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/histograms/manual_detector_trace_histograms.md
analysis_outputs/manual_detector_update_all_selection_methods_120csv_fixed/histograms/data_wrangler_slope_and_stats.csv
```

The root trace/histogram above uses the final override's selected public mode.
To analyze each selection/threshold mode as the promoted public mode, run a
selected-mode trace and histogram pass per mode. This is the command to use for
the full SNR-variant by selection-mode performance matrix:

```powershell
Set-Location "C:\Users\isaia\Desktop\trapdetect"

$ReviewCsv = "C:\Users\isaia\Desktop\trapdetect\manual_count_template.csv"
$SourceNpzDir = "C:\Users\isaia\Desktop\run3_5926_precleaned"
$OutRoot = "analysis_outputs\manual_detector_update_selected_mode_matrix_120csv"
$DatasetNpz = "manual_review_detector_update\manual_test_data_from_manual_count_template.npz"

$Modes = @(
    @{ mode_id = "matched_snr_manual_calibrated"; score_key = "matched_snr" },
    @{ mode_id = "integrated_snr_manual_calibrated"; score_key = "integrated_snr"; threshold = 5.6 },
    @{ mode_id = "support_sum_snr_manual_calibrated"; score_key = "support_sum_snr" },
    @{ mode_id = "local_support_sum_snr_robust_manual_calibrated"; score_key = "local_support_sum_snr_robust"; threshold = 5.6 },
    @{ mode_id = "support_mean_excess_snr_manual_calibrated"; score_key = "support_mean_excess_snr" },
    @{ mode_id = "robust_peak_snr_manual_calibrated"; score_key = "robust_peak_snr" },
    @{ mode_id = "template_support_excess_density_manual_calibrated"; score_key = "template_support_excess_density"; threshold = 0.02 },
    @{ mode_id = "template_ncc_score_manual_calibrated"; score_key = "template_ncc_score" }
)

New-Item -ItemType Directory -Force -Path $OutRoot | Out-Null

.\.venv\Scripts\python.exe tools/manual_data/rebuild_manual_test_data.py --format npz --review-csv $ReviewCsv --source-npz-dir $SourceNpzDir --output $DatasetNpz

foreach ($Mode in $Modes) {
    $ModeOut = Join-Path $OutRoot $Mode.mode_id
    $ValidationConfig = Join-Path $ModeOut "selected_mode.validation.jsonl"
    $TraceJsonl = Join-Path $ModeOut "manual_detector_trace_noise_window.jsonl"
    $HistogramDir = Join-Path $ModeOut "histograms"

    New-Item -ItemType Directory -Force -Path $ModeOut | Out-Null

    $ModeSpec = [ordered]@{
        mode_id = $Mode.mode_id
        score_key = $Mode.score_key
        ledger_only = $true
    }
    if ($Mode.ContainsKey("threshold")) {
        $ModeSpec["threshold"] = [double]$Mode.threshold
    }

    $ModeConfig = [ordered]@{
        experimental_stage5_modes = @($ModeSpec)
        experimental_stage5_selected_mode = $Mode.mode_id
        experimental_stage5_mode_policy = "ledger_only"
    }
    $ModeConfig | ConvertTo-Json -Compress -Depth 6 | Set-Content -Encoding ascii -Path $ValidationConfig

    .\.venv\Scripts\python.exe tools/manual_detector_update.py --dataset-npz $DatasetNpz --output-dir $ModeOut --validation-config $ValidationConfig --fixed-point-verbose-log --trace-noise-window-log

    .\.venv\Scripts\python.exe tools/manual_detector_trace_histograms.py $TraceJsonl --output-dir $HistogramDir
}
```

Each selected-mode directory writes:

```text
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/manual_detector_update_fixed_point_verbose.jsonl
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/manual_detector_trace_noise_window.jsonl
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/manual_detector_trace_noise_window.md
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/histograms/manual_detector_trace_histograms.pdf
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/histograms/manual_detector_trace_histograms.md
analysis_outputs/manual_detector_update_selected_mode_matrix_120csv/<mode_id>/histograms/data_wrangler_slope_and_stats.csv
```

Add ledger-only Stage 5 score modes directly from the batch CLI. These commands
preserve the four public top-level `snr_variants`; the extra scores are nested
under each variant's `modes` ledger and do not replace the canonical count.
Deprecated `aperture_*` and `psf_region_*` score keys remain accepted as aliases
for older configs, but new commands should use support-based names.

```text
python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --selection-score matched_snr --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned

python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --selection-score integrated_snr --selection-threshold 5.6 --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned

python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --selection-score local_support_sum_snr_robust --selection-threshold 5.6 --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned

python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --selection-score template_support_excess_density --selection-threshold 0.02 --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned
```

To promote a configured mode into the public count, pass its mode id with
`--selected-stage5-mode`. For a CLI-created ledger mode, the mode id is
`cli_<score_key>_ledger`:

```text
python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --selection-score integrated_snr --selection-threshold 5.6 --selected-stage5-mode cli_integrated_snr_ledger --auto-bundle --keep-temp C:/Users/isaia/Desktop/run3_5926_precleaned
```

Regenerate manual-template review overlays for the same score modes without a
temporary config-generation script:

```text
python tools/manual_review/export_flagged_review_frames.py --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --detector-config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --output-dir analysis_outputs/selection_score_artifact_regenerated/manual_template_overlays_matched_snr --selection-score matched_snr

python tools/manual_review/export_flagged_review_frames.py --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --detector-config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --output-dir analysis_outputs/selection_score_artifact_regenerated/manual_template_overlays_integrated_snr --selection-score integrated_snr --selection-threshold 5.6

python tools/manual_review/export_flagged_review_frames.py --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --detector-config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --output-dir analysis_outputs/selection_score_artifact_regenerated/manual_template_overlays_local_support_sum_snr_robust --selection-score local_support_sum_snr_robust --selection-threshold 5.6

python tools/manual_review/export_flagged_review_frames.py --review-csv manual_count_template.csv --source-npz-dir C:/Users/isaia/Desktop/run3_5926_precleaned --detector-config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --output-dir analysis_outputs/selection_score_artifact_regenerated/manual_template_overlays_template_support_excess_density --selection-score template_support_excess_density --selection-threshold 0.02
```

Audit the manual oracle directly:

```text
python -m pytest -vv -ra --tb=long tests/test_manual_test_data.py::TestManualOracleAudit
```

The current corpus has 120 labeled rows: 113 strict-scored rows and 7
flagged-advisory rows. The oracle command is intentionally allowed to fail
informatively while strict parity is unresolved; current known examples include
`bundle_001`, `bundle_031`, and `bundle_092`, with patch-out context around
`bundle_030`, `bundle_059`, and `bundle_093`.

Historical Run1 review-session replay remains available when you intentionally
want to compare older staged pass sets against the current detector. The replay
helper supports three modes:

- `baseline`: generate one reusable baseline bundle
- `pass`: replay one saved reviewed session against an existing baseline bundle
- `replay-all`: rerun the baseline once, then replay every saved staged pass

For speed-sensitive benchmarking, generate the baseline once and reuse it for
later pass replays:

```text
python tools/manual_data/replay_manual_review_passes.py baseline --npz-source C:/Users/isaia/Desktop/run1 --output-dir manual_test_run1/replay_baseline --overwrite --benchmark
```

Then replay one saved pass directly without creating a wrapper directory:

```text
python tools/manual_data/replay_manual_review_passes.py pass --npz-source C:/Users/isaia/Desktop/run1 --session-dir manual_test_run1/review_session_pass3 --baseline-bundle manual_test_run1/replay_baseline/run1_iteration_bundle.npz --output-dir manual_test_run1/replay_pass3 --overwrite --benchmark
```

If you want the whole staged workflow in one command, keep using `replay-all`.
It reruns the baseline detector once, then applies each saved
`review_session*/manual_count_template.csv` cumulatively, rebuilds the
detector override in the new folder, reruns the batch, and writes one replay
comparison report at the end:

```text
python tools/manual_data/replay_manual_review_passes.py replay-all --npz-source C:/Users/isaia/Desktop/run1 --manual-review-dir manual_test_run1 --output-dir manual_test_run1/replay_current_detector --overwrite
```

If you only want the most complete reviewed CSV, not every intermediate pass,
add `--final-only`:

```text
python tools/manual_data/replay_manual_review_passes.py replay-all --npz-source C:/Users/isaia/Desktop/run1 --manual-review-dir manual_test_run1 --output-dir manual_test_run1/replay_current_detector_final --final-only --overwrite
```

For API-level automation, use the same commands as the contract and mirror the
small examples in `tests/` so manual parity failures remain visible.
