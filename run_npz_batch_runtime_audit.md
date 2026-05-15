# run_npz_batch Runtime Audit

Date: 2026-05-05

This note records the latest scheduler audit for `run_npz_batch.py` so the
benchmark outcome is preserved in the repository instead of only in session
history.

## Scope

The audit focused on the `python run_npz_batch.py -a --auto-bundle <npz-dir>`
path, with emphasis on:

1. large-batch throughput on Windows
2. hybrid CPU/GPU scheduling behavior
3. resume-safe execution and benchmark repeatability

## Current Runtime Facts

1. CPU-auto remains the default execution policy.
2. The GPU lane is opt-in via `--gpu-device ...`.
3. The GPU scheduler default is `--gpu-scheduler spill`.
4. Auto NPZ loader width is currently capped from available memory as:
   1 loader when available memory is `<= 2 GiB`,
   2 loaders when available memory is `<= 8 GiB`,
   otherwise up to `len(npz_files)`.
5. Fixed-policy benchmark reruns should pin both `--workers` and
   `--npz-workers`, because auto loader selection can differ between modes and
   confound scheduler comparisons.

## Scheduler Variants Tested

The benchmark harness now supports these hybrid GPU scheduler variants:

1. `hybrid-auto` -> `gpu_scheduler_mode="spill"`
2. `hybrid-queue-one` -> `gpu_scheduler_mode="queue-one"`
3. `hybrid-queue-two` -> `gpu_scheduler_mode="queue-two"`
4. `hybrid-queue-all` -> `gpu_scheduler_mode="queue-all"`

The queued modes are investigative only. They are not recommended production
defaults.

## Measured Results

Artifacts:

1. `analysis_outputs/run3_first20_gpu_scheduler_benchmark.json`
2. `analysis_outputs/run3_first10_fixed_policy_gpu_scheduler_benchmark.json`

### First-20 comparison

The first-20 comparison showed:

1. `hybrid-auto` was fastest at `292.405 s`.
2. `hybrid-queue-two` was slower at `505.917 s`.
3. `hybrid-queue-one` and `hybrid-queue-all` were much slower at
   `1194.308 s` and `1253.880 s`.
4. The queued modes increased GPU usage, but they also changed summary digests
   relative to the spill baseline.

This run was useful, but not fully isolated, because auto loader selection did
not stay constant across all four modes.

### Fixed-policy first-10 comparison

The fixed-policy rerun pinned `--workers 16 --npz-workers 2` for all four
hybrid modes. That comparison isolated the scheduler itself.

Results:

1. `hybrid-auto`: `184.614 s`, `39.3 fps`, digest match.
2. `hybrid-queue-all`: `574.132 s`, digest mismatch.
3. `hybrid-queue-two`: `580.174 s`, digest mismatch.
4. `hybrid-queue-one`: `581.266 s`, digest mismatch.

Interpretation:

1. Forcing admitted runs to wait for the single GPU lane is currently a large
   wall-time regression.
2. The queued modes did not preserve the selected-summary output contract in
   these measured runs.
3. The current bottleneck is therefore not just GPU admission starvation.
4. The next credible optimization surface is the GPU analysis path itself,
   especially host-device transfers and synchronization inside
   `analyze_ions_fft.py`.

## Current Recommendation

For production batch analysis on this repository state:

1. keep `gpu_scheduler_mode="spill"`
2. use the queued modes only for targeted debugging or GPU-path experiments
3. prefer fixed-policy benchmark reruns before drawing conclusions from
   scheduler changes
