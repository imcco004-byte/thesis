# TrapDetect

TrapDetect analyzes trapped-ion images. It estimates how many ions are visible,
localizes accepted ions, and reports confidence and diagnostic information for
single frames, image sequences, and `.npz` camera archives.

The single-frame public claim surface is limited to image-local outputs:
visible-ion count, accepted-ion position and spacing, PSF or noise estimates,
and per-frame confidence diagnostics. TrapDetect does not claim that one frame
directly yields a radiative lifetime or that image statistics alone recover
collision, blackbody, or leakage-light corrections.

The repository includes example NPZ data in `run1/`. For the detector model,
PSF assumptions, and stage-by-stage math, see [ALGORITHM.md](ALGORITHM.md).

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
| One frame already in memory or one image on disk | `analyze_array()` / `analyze_path()` or `analyze_ions_fft.py` | One frame result `dict` |
| Several ordinary image files | `run_batch()` or `analyze_batch.py` | Batch `dict` with per-run reducers (`frames`, `series_stats`, `state_matrix`) |
| One `.npz` archive or a directory of archives | `run()` or `run_npz_batch.py` | Top-level batch `dict` with multi-run aggregation, bundle writing, and parallel loading/analysis |
| A bundle `.npz` you want to inspect or export | `extract_npz_json()` or `extract_npz_json.py` | Readable JSONL files, `batch_summary.jsonl`, and typed variant audit rows |

The mainline mediation chain is:

`analyze_ions_fft.py` -> `analyze_batch.py` -> `run_npz_batch.py` -> `extract_npz_json.py` / `calculate_lifetime_precision.py`

Large-job parallelization, memory budgeting, and scratch-flow management remain concentrated in `run_npz_batch.py`.

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
the raw camera archive such as `run1/photon_count0.npz`.

```text
python calculate_lifetime_precision.py input.npz --jsonl-out run1_precision.jsonl
```

If you already have extracted JSONL, that still works too:

```text
python calculate_lifetime_precision.py out/batch_summary.jsonl --jsonl-out run1_precision.jsonl
```

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
python create_validation_note.py "run1 validation audit" \
    --source analysis_outputs/run1_validation/run1_default_report_allframes.md \
    --source analysis_outputs/run1_validation/extracted_default_allframes/batch_summary.jsonl
```

The helper always resolves the file inside `notes/` and rejects path-like note
names so generated and authored artifacts stay separate.

## Utility Tools

Non-pipeline utility scripts now live under `tools/` so the repo root stays
reserved for the main analysis chain and public entrypoints.

- `tools/manual_review_session.py`: prepare a reviewer-facing JSONL session,
    generate a companion markdown packet, and apply completed review sessions
    back into a manual-review CSV plus rebuilt dataset artifacts.
- `tools/manual_detector_update.py`: build a manual-review-backed eta artifact
    and a reversible detector override config JSONL.
- `tools/manual_data/`: manual-review rebuild, inspection, and smoke-check tools
    for the canonical `tests/test_data.npz` artifact.
- `tools/manual_review/`: CSV/manifest comparison and summary probes for the
    manual-review audit inputs.
- Root entrypoints such as `analyze_ions_fft.py`, `analyze_batch.py`,
    `run_npz_batch.py`, `extract_npz_json.py`, `create_validation_note.py`, and
    `calculate_lifetime_precision.py` remain unchanged.

Rebuild the canonical manual-review dataset from the on-disk CSV and manifests:

```text
python tools/manual_data/rebuild_manual_test_data.py --format npz
```

If you want to trust CSV content piped from the current editor buffer instead of
the on-disk review CSV, pipe it to the same tool. The stdin path takes priority
over `--review-csv`:

```text
Get-Content manual_counts/psf_calibration_45.csv | python tools/manual_data/rebuild_manual_test_data.py --format jsonl --output analysis_outputs/manual_review_psf_calibration_25/manual_test_data.jsonl
```

Run the manual-review batch smoke check from its new location:

```text
python tools/manual_data/focused_check.py
```

Print a quick summary of the canonical manual-review NPZ:

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
| `analyze_batch.py` | Per-run reduction for ordinary image files and reducer ownership layer |
| `run_npz_batch.py` | Multi-run `.npz` orchestration, bundle writing, and parallel resource control |
| `extract_npz_json.py` | Convert bundle `.npz` files to readable JSONL, including v7 variant rows |
| `run1/` | Example NPZ input data |
| `tests/` | Automated test suite |

## More Detail

- [ALGORITHM.md](ALGORITHM.md) explains the detector model, PSF assumptions,
    heuristics, and decision metrics in more depth.
- The tests in `tests/` are a good source of small, verified usage examples.

## Iterative Detector Update Pipeline

The iterative manual-review pipeline is intentionally local and reversible.
`tools/manual_detector_update.py` produces a bundle-backed eta artifact plus a
JSONL override file, and `run_npz_batch.py --config ...` applies that override
to one batch invocation only. This does not mutate the default detector config
in `analyze_ions_fft.py` or `run_npz_batch.py`.

The review loop is centered on an editable CSV template plus a generated
markdown packet. `prepare` exports review images, writes
`manual_count_template.csv`, keeps `review_session.jsonl` as an audit copy, and
generates `review_session.md`. `apply` reads the completed CSV template and
rebuilds the manual-review dataset artifacts directly.

Prepare a per-run JSONL session with the default 20-sample review count:

```text
python tools/manual_review_session.py prepare \
    --input-dir analysis_outputs \
    --glob "run1_default_full_photon_count*.jsonl"
```

Prepare a bundle-backed session from an existing admitted bundle NPZ:

```text
python tools/manual_review_session.py prepare --bundle-npz trapdetect_results_2026-05-07_at15h42m08s_rt00h21m22s_100npz.npz
```

When `--output-dir` is omitted, per-run prepare writes to
`analysis_outputs/manual_review_run1_last61/` and bundle prepare writes to
`analysis_outputs/manual_review_ground_truth/`.

Bundle-mode `prepare` uses a priority sampler instead of the older fixed
bucket export path. The rule cycle is:

- lowest SNR frame
- 2 frames adjacent to the same decrease event
- 2 frames adjacent to the same increase event
- 4 frames inside or adjacent to a decrease-followed-by-increase window
- 2 highest-ion-count frames
- 2 lowest-ion-count frames

The rule cycle repeats until the requested count is reached or the bundle runs
out of unused candidates. `--bundle-adjacency-window` controls the frame radius
used around decrease and increase anchors and around the recovery window.

Recommended review flow: open `manual_count_template.csv` with a table editor
such as Edit CSV, fill the manual count fields there, and then apply that CSV.

Apply a completed review CSV and rebuild both NPZ and JSONL dataset artifacts:

```text
python tools/manual_review_session.py apply analysis_outputs/manual_review_ground_truth/manual_count_template.csv
```

If you still want the older JSONL-driven path, `apply` also accepts
`review_session.jsonl` plus an optional `--review-csv PATH` output target.

Build a manual-review-backed detector override after the dataset has been
rebuilt:

```text
python tools/manual_detector_update.py --dataset-npz analysis_outputs/manual_review_ground_truth/manual_test_data.npz
```

That command also validates the override against the scored manual-review rows
and reports how many checked frames matched or mismatched the manual counts.

The detector override file is plain JSONL and can be passed to entrypoints that
support `--config`, for example:

```text
python analyze_ions_fft.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl frame.png
```

### Example Run1 Procedure

One concrete iterative pass using the admitted `run1/` bundles is:

1. Start from the first admitted bundle and prepare the review session.
2. Fill `manual_count_template.csv` in a table editor.
3. Apply the completed CSV to rebuild `manual_test_data.npz` and `manual_test_data.jsonl`.
4. Build the local detector override from that rebuilt dataset.
5. Rerun the full `run1/` detector pass with the local override only.
6. Compare the first pass and second pass lifetime summaries across the selected detector path and all 4 stored variants.

CLI example:

```text
python tools/manual_review_session.py prepare --bundle-npz manual_test_run1/run1_iteration_bundle.npz

python tools/manual_review_session.py apply analysis_outputs/manual_review_ground_truth/manual_count_template.csv

python tools/manual_detector_update.py --dataset-npz analysis_outputs/manual_review_ground_truth/manual_test_data.npz

python run_npz_batch.py --config analysis_outputs/manual_detector_update/manual_detector_override.jsonl --auto-bundle --keep-temp C:\Users\isaia\Desktop\run1

python analyze_variant_transition_bundle.py --pretty manual_test_run1/run1_iteration_bundle.npz trapdetect_results_2026-05-11_at19h11m25s_rt00h24m47s_100npz.npz --output manual_test_run1/variant_lifetime_report.txt
```

The fourth command uses the default Joblib CPU backend, auto-bundle output,
and preserved bundle-only scratch. In the example above, that rerun bundle is
`trapdetect_results_2026-05-11_at19h11m25s_rt00h24m47s_100npz.npz`. Replace the
second bundle path with the auto-named rerun bundle you want to compare.

The pretty report prints the selected path plus all 4 SNR variants with the
retained transition lifetime mean, median, and mode, the retained epoch count,
the number of included and excluded runs, and the summarized exclusion reasons.

If you already have reviewed CSVs from an earlier pass set and want to replay
that whole staged workflow against the current detector into a fresh folder,
the replay helper now supports three modes:

- `baseline`: generate one reusable baseline bundle
- `pass`: replay one saved reviewed session against an existing baseline bundle
- `replay-all`: rerun the baseline once, then replay every saved staged pass

For speed-sensitive benchmarking, generate the baseline once and reuse it for
later pass replays:

```text
python tools/manual_data/replay_manual_review_passes.py baseline --npz-source C:\Users\isaia\Desktop\run1 --output-dir manual_test_run1\replay_baseline --overwrite --benchmark
```

Then replay one saved pass directly without creating a wrapper directory:

```text
python tools/manual_data/replay_manual_review_passes.py pass --npz-source C:\Users\isaia\Desktop\run1 --session-dir manual_test_run1\review_session_pass3 --baseline-bundle manual_test_run1\replay_baseline\run1_iteration_bundle.npz --output-dir manual_test_run1\replay_pass3 --overwrite --benchmark
```

If you want the whole staged workflow in one command, keep using `replay-all`.
It reruns the baseline detector once, then applies each saved
`review_session*/manual_count_template.csv` cumulatively, rebuilds the
detector override in the new folder, reruns the batch, and writes one replay
comparison report at the end:

```text
python tools/manual_data/replay_manual_review_passes.py replay-all --npz-source C:\Users\isaia\Desktop\run1 --manual-review-dir manual_test_run1 --output-dir manual_test_run1\replay_current_detector --overwrite
```

If you only want the most complete reviewed CSV, not every intermediate pass,
add `--final-only`:

```text
python tools/manual_data/replay_manual_review_passes.py replay-all --npz-source C:\Users\isaia\Desktop\run1 --manual-review-dir manual_test_run1 --output-dir manual_test_run1\replay_current_detector_final --final-only --overwrite
```

Jupyter example:

```python
from pathlib import Path
import subprocess
import sys

from tools.manual_detector_update import build_manual_detector_update
from tools.manual_review_session import apply_review_session, prepare_review_session

first_bundle = Path("manual_test_run1/run1_iteration_bundle.npz")
review_dir = Path("analysis_outputs/manual_review_ground_truth")
run1_dir = Path(r"C:\Users\isaia\Desktop\run1")
# Replace this with the auto-named rerun bundle you want to compare.
second_bundle = Path("trapdetect_results_2026-05-11_at19h11m25s_rt00h24m47s_100npz.npz")
report_path = Path("manual_test_run1/variant_lifetime_report.txt")

session = prepare_review_session(bundle_npz=first_bundle, output_dir=review_dir)
session["template_csv_path"]
```

After you edit the CSV in a table editor, run the next cell:

```python
applied = apply_review_session(session["template_csv_path"])

update = build_manual_detector_update(
    dataset_npz_path=applied["dataset_npz_path"],
    validate_manual_counts=True,
)

subprocess.run(
    [
        sys.executable,
        "run_npz_batch.py",
        "--config",
        str(update["override_jsonl_path"]),
        "--auto-bundle",
        "--keep-temp",
        str(run1_dir),
    ],
    check=True,
)
```

Then save the pretty lifetime comparison report:

```python
subprocess.run(
    [
        sys.executable,
        "analyze_variant_transition_bundle.py",
        "--pretty",
        str(first_bundle),
        str(second_bundle),
        "--output",
        str(report_path),
    ],
    check=True,
)

report_path
```
