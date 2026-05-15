# run1 Validation Audit

This note is an authored validation summary derived from the current generated
outputs in `analysis_outputs/run1_validation/`. The generated manifest and
per-run report files in that directory should be treated as read-only derived
artifacts.

## Scope

This report validates the rebuilt default all-frame analysis of `run1` against
the current `ALGORITHM.md` contract and the cited Ba+ D5/2 lifetime context.

Inputs used:

- `analysis_outputs/run1_validation/run1_default_bundle_allframes.npz`
- `analysis_outputs/run1_validation/run1_default_report_allframes.md`
- `analysis_outputs/run1_validation/extracted_default_allframes/batch_summary.jsonl`
- `analysis_outputs/run1_validation/extracted_default_allframes/run_photon_count*.jsonl`

## Batch Outcome

- NPZ runs analyzed: 6
- Total frames: 4913
- Successfully analyzed: 4913
- Errors: 0
- Modal visible-ion count in every run: 2
- Flagged runs: `photon_count2`, `photon_count4`
- Single-epoch exclusions: none
- Included runs for the pooled transition-time metric: `photon_count0`, `photon_count1`, `photon_count3`, `photon_count5`
- Pooled mean frame lifetime: 111.57142857142857 frames
- Pooled mean real-time lifetime / mean transition time: 4.682784071541391 s
- Real-time epochs considered: 7

The downstream helper script `calculate_lifetime_precision.py` consumed that
same `batch_epoch.mean_real_time_lifetime_s` value and reported:

- mean transition time: 4.682784071541391 s
- statistical uncertainty: 1.7699260138161452 s
- total uncertainty with no explicit systematic terms: 1.7699260138161452 s
- fractional uncertainty: 37.79644730092272%

## Contract Check Against ALGORITHM.md

The current outputs match the implemented epoch contract.

1. Epochs are maximal contiguous runs of equal `visible_ion_count`.
2. Strict decreases are flagged.
3. Runs with decreases are excluded from the pooled batch transition-time mean.
4. Runs with only one epoch are excluded as `single_epoch` because final epochs are not pooled.
5. The pooled batch mean uses only non-final epochs from included runs.
6. `calculate_lifetime_precision.py` uses that emitted batch real-time mean directly.

Observed behavior is consistent with those rules:

- `batch_summary.jsonl` includes 4 runs and excludes 2 with reason `flagged`.
- No run in `run1` was excluded as `single_epoch`.
- The pooled real-time mean is exactly the value passed into the downstream precision helper.

This means the code path requested by the project is now explicit and validated:
the system mean epoch time is the mean transition time, and that exact value is
what feeds systematic-error propagation.

## Per-Run Epoch Structure

Per-run epoch sequences in seconds:

- `photon_count0`: 1-ion 15.870, 2-ion 18.604
- `photon_count1`: 0-ion 0.090, 1-ion 3.433, 2-ion 30.536
- `photon_count2`: 1-ion 2.121, 2-ion 0.073, 1-ion 0.804 (flagged decrease), 2-ion 30.714
- `photon_count3`: 0-ion 2.971, 1-ion 6.628, 2-ion 23.959
- `photon_count4`: 0-ion 0.405, 1-ion 0.090, 0-ion 1.712 (flagged decrease), 2-ion 32.024
- `photon_count5`: 0-ion 0.084, 1-ion 3.703, 2-ion 30.217

Important interpretation details:

- A short leading 0-count epoch is acceptable startup behavior under the LED-synchronized collection rule.
- The pooled mean transition time does not include final epochs.
- The seven non-final real-time epochs that actually enter the pooled mean are:
  15.870, 0.090, 3.433, 2.971, 6.628, 0.084, and 3.703 s.

So the current 4.682784 s batch metric is not an average over the long final
2-ion holds. It is the mean transition time defined by the project’s epoch
rules.

## Detector-Quality Summary

Cross-run frame diagnostics remain consistent with earlier observations:

- mean measurement precision score is tightly clustered around 0.469 to 0.474
- PSF-valid fraction is about 0.158 to 0.372 across runs
- the evidence-margin basis is dominated by `psf_non_gaussian` in every run
- every run is labeled `compressed_or_artifact`

This supports using the output as a stable, auditable state-detection trace,
but it also indicates that the detector is operating far from a clean
Gaussian-PSF regime.

## Comparison To The Ba+ Lifetime Literature

The cited Ba+ papers define a narrower physics target than the current system
transition-time metric.

- Madej and Sankey (1990) observed single-ion quantum jumps that followed the expected exponential dark-period distribution and reported a radiative lifetime of 34.5 +/- 3.5 s with pressure-aware quenching analysis.
- Auchter et al. (2014) reported an improved low-pressure Ba+ 5D5/2 lifetime measurement near 31 s together with branching-fraction results.

Comparison with `run1`:

- The current pooled mean transition time of 4.682784 s is far below the literature radiative-lifetime scale.
- That mismatch is expected because the pooled metric is intentionally the non-final epoch mean, not a terminal dark-period lifetime estimator.
- The long final 2-ion epochs are 18.604, 30.536, 23.959, 30.217, 30.714, and 32.024 s, which are much closer to the literature scale, but they are excluded from the current pooled transition-time metric by design.

Conclusion: the present batch output is consistent with the project’s transition-time contract, but the pooled 4.682784 s value is not itself a direct Ba+ D5/2 radiative-lifetime estimate.

## Systematic-Error Interpretation

For the current project workflow, the systematic-error helper is using the
correct upstream quantity. The remaining issue is physical interpretation, not
wiring.

Major limitations relative to the lifetime papers:

1. The current metric is an LED-defined mean transition time over non-final epochs, not a survival-model fit to terminal dark periods.
2. Camera-observed count is not guaranteed occupancy; reduced visible count can reflect dark preparation or shelving rather than loss.
3. Pressure and collisional-quenching systematics are not measured here.
4. The long terminal epochs that look lifetime-like are multi-ion 2-count intervals, not isolated single-ion dark periods.
5. Most frames are PSF-non-Gaussian, which weakens confidence interpretation based on boundary evidence.

## Bottom Line

The requested chain is now correct and verified:

- the system mean epoch time is the emitted mean transition time
- decrease-flagged runs are excluded
- single-epoch runs are excluded
- final epochs are not used in the mean
- `calculate_lifetime_precision.py` consumes that exact batch real-time mean

For `run1`, that means the current system transition-time result is
4.682784071541391 +/- 1.7699260138161452 s (statistical only), while the data
also contain long final 2-ion epochs near the expected Ba+ lifetime scale that
would require a different downstream estimator to support a direct physics
lifetime claim.
