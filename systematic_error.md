# Systematic Error

This note reuses the systematic-error section headings from the prior Ba+ lifetime papers in `Paper_reference_markdown/PhysRevA.97.032508 (2).md` and `Paper_reference_markdown/PhysRevA.101.062515 (1).md`, then repopulates those headings with the current TrapDetect contract from `ALGORITHM.md`, `README.md`, `calculate_lifetime_precision.py`, `run1_precision.jsonl`, `notes/run1_validation_audit.md`, and `notes/calculate_lifetime_precision_critique.md`.

## Claim Boundary And Current Status

- TrapDetect's central lifetime-like number is the batch `mean_real_time_lifetime_s` carried under the `batch_transition_lifetime` contract: the arithmetic mean of cumulative safe-prefix transition samples from camera-observed visible-count states after the `decrease_flag` cutoff gate is applied.
- `ALGORITHM.md` and `README.md` both state that this is a downstream transition-time precision summary, not a hidden refit of radiative lifetime physics.
- The current calculator deliberately splits systematics into two classes. External physical terms remain explicit inputs: `collision_quenching`, `blackbody_radiation`, and `leakage_light_deshelving`. Internal camera-diagnostic terms default from emitted batch diagnostics: `detection_error_bound`, `ion_heating_false_dark`, and `timing_window_bias`.
- Bundle v8 and extracted JSONL now preserve full four-variant SNR audit payloads downstream, including per-frame comparison rows and batch-level `snr_variant_batch_summary` rows. That widens the observable audit surface, but not the claim surface.
- The critique note in `notes/calculate_lifetime_precision_critique.md` sharpens that boundary: SNR-grounded confidence terms should contract or expand with the data, but pressure, blackbody, and leakage-light physics should not be invented from image diagnostics.
- The current mediation chain is therefore explicit: `analyze_ions_fft.py` produces detector variants, `analyze_batch.py` owns per-run reduction, `run_npz_batch.py` aggregates and writes the bundle, and only `extract_npz_json.py` / `calculate_lifetime_precision.py` consume the downstream contract. Parallel loading and memory management stay in the orchestrator and do not change the systematic model.
- The current `run1_precision.jsonl` example follows that rule. It emits only the three internal terms, marks them as `origin = snr_derived`, and explicitly lists `collision_quenching`, `blackbody_radiation`, and `leakage_light_deshelving` as still missing from the physics budget.
- The authored `notes/run1_validation_audit.md` shows why this distinction matters. In the `run1` example the retained statistic is a gated transition-time observable built from cumulative safe-prefix samples, while excluded terminal holds can still cluster near the literature lifetime scale. The current estimator is therefore physically narrower than a direct `5D5/2` radiative-lifetime fit.

## Explicit Refusals

- TrapDetect does not claim that a single frame directly yields the radiative lifetime of `Ba+ 5D5/2`.
- TrapDetect does not derive `collision_quenching`, `blackbody_radiation`, or `leakage_light_deshelving` from image SNR, margins, or other detector-confidence statistics.
- TrapDetect does not treat `measurement_precision_score`, `decision_margin`, or `evidence_margin` as substitutes for apparatus telemetry or dedicated control measurements.
- TrapDetect does not use Bayesian or other downstream post-processing as a substitute for missing detector-core evidence or missing explicit physical inputs.

## PhysRevA.97.032508 (2018): V. SYSTEMATIC EFFECTS

This paper is the closest structural match to TrapDetect's present use case because it treats long-lived `Ba+ 5D5/2` measurements as a sum of additive decay-rate contributions, then checks specific slow processes one by one.

### A. Background gas collisions

- The literature treats background-gas collisions as a real, pressure-dependent shortening of the observed lifetime. In PhysRevA.97.032508, collisional quenching is the dominant systematic and is handled by pressure scans plus extrapolation to zero pressure.
- `ALGORITHM.md` and `notes/run1_validation_audit.md` both keep the present repository on the other side of that boundary. The camera pipeline measures visible-count epochs and frame diagnostics, but it does not measure pressure, residual-gas composition, or collisional cross sections.
- `calculate_lifetime_precision.py` therefore keeps `collision_quenching` on the explicit physical-input path. Users may provide a decay-rate correction and/or decay-rate uncertainty, but the code will not derive collision physics from SNR or margin statistics.
- The current `run1_precision.jsonl` output is therefore correct to leave this term absent and to classify the physics budget as incomplete.

#### 1. Quenching

- PhysRevA.97.032508 reports a linear quenching rate of `1.5(0.5) x 10^7 s^-1 / mbar` and subtracts the collisional decay-rate contribution before examining smaller effects.
- Madej and Sankey (1990), cited in `ALGORITHM.md`, are the earlier repository anchor for the same pressure-aware collisional-quenching logic.
- In TrapDetect, any quenching correction belongs in `--collision-rate-correction` or `--collision-rate-uncertainty`, with `origin = explicit_physical_input` rather than `snr_derived`.

#### 2. Fine-structure mixing

- PhysRevA.97.032508 also considers pressure-dependent `D5/2 <-> D3/2` mixing. In that experiment the continuous repumping scheme folds the mixing term into the same pressure-scaling collision budget.
- TrapDetect has no direct state-mixing model, repumping monitor, or pressure scan. For this repository, any analogous effect is best treated as part of the same external collision term rather than as a separate camera-derived systematic.

### B. Off-resonant scattering

- PhysRevA.97.032508 treats continuous laser light and shelving light as possible deshelving pathways, then checks whether the pressure-corrected decay rate depends on laser intensity or shelving rate.
- That logic maps naturally onto TrapDetect's `leakage_light_deshelving` component. The relevant quantity is a real decay-rate contribution from unwanted light, not an image-analysis confidence score.
- `README.md` explicitly says leakage-light corrections still require explicit physical inputs, and `calculate_lifetime_precision.py` only accepts `leakage_light_deshelving` as an explicit decay-rate uncertainty.
- The present repository has no optical-spectrum monitor, beam-extinction log, or per-run light-leak calibration. This term must therefore stay external.

#### 1. Laser light at 494 and 650 nm

- PhysRevA.97.032508 estimates the deshelving contribution from the 494 nm and 650 nm lasers to be negligible at the tested intensities, and additionally finds no significant intensity dependence in the pressure-corrected decay rate.
- PhysRevA.101.062515 arrives at the same practical conclusion through leakage tests and extinction arguments for several wavelengths.
- TrapDetect can cite that literature structure, but it cannot verify the same conclusion from image statistics alone. The correct repository action is still to keep any residual bound under the explicit `leakage_light_deshelving` term when apparatus measurements justify it.

#### 2. Light at 456 nm

- PhysRevA.97.032508 treats broadband 456 nm shelving light as a potential indirect deshelving path and concludes that the induced rate is negligible over the tested LED range.
- The repository already distinguishes this kind of optical-physics term from camera-confidence terms. SNR cannot establish a spectral-leak upper bound.
- If a future experiment characterizes the LED spectrum or filter leakage directly, that information should enter TrapDetect as an explicit leakage-light uncertainty rather than as a reweighted internal proxy.

### C. Stray electromagnetic fields

- PhysRevA.97.032508 separates blackbody radiation, static electric fields, and magnetic fields from collisional and optical processes because they modify the lifetime through known physical couplings, not through data-analysis ambiguity.
- TrapDetect preserves the same boundary for blackbody radiation. `calculate_lifetime_precision.py` exposes `blackbody_radiation` as an explicit decay-rate correction and/or uncertainty.
- The repository does not currently expose separate terms for Stark or Zeeman effects. If those become relevant, they belong either in the generic manual systematic channels or in future explicit named components, not in the SNR-derived defaults.

#### 1. Thermal radiation

- PhysRevA.97.032508 estimates blackbody-stimulated emission on the nearby `D5/2 - D3/2` transition and applies a small decay-rate correction, shortening the lifetime by about 0.1 s.
- `calculate_lifetime_precision.py` mirrors that literature structure directly: `blackbody_radiation` is an explicit additive decay-rate correction or uncertainty with `origin = explicit_physical_input`.
- The current `run1_precision.jsonl` file leaves this term missing, which is appropriate because no thermal-radiation correction was supplied.

#### 2. Stray electric fields

- PhysRevA.97.032508 treats dc Stark mixing from uncompensated stray fields as negligible at the observed field strengths.
- TrapDetect has no electric-field telemetry and no state-mixing forward model, so this effect is presently outside the named systematic set.
- If future apparatus documentation shows a non-negligible Stark contribution, it should be added as an explicit physical term rather than inferred from the image-derived measurement-precision score.

#### 3. Magnetic fields

- PhysRevA.97.032508 argues that the dc Zeeman effect does not alter the `5D5/2` lifetime in the same way because parity is preserved, so no correction is needed.
- The current repository likewise has no magnetic-field systematic component. This is acceptable so long as the experimental configuration remains in the same negligible-effect regime; otherwise it should be introduced as an explicit apparatus term.

### D. Ion dynamics and interaction

- The literature treats ion heating and multi-ion interaction as mechanisms that can bias the observed dark-period duration without changing the underlying atomic lifetime. The physical lifetime stays the same, but apparent detection times can stretch if fluorescence recovery is delayed.
- This is the closest category to TrapDetect's internal SNR-derived systematics. The repository does not claim a first-principles thermodynamic model, but it does expose confidence observables that move when detection becomes ambiguous or near-threshold.
- In `run1_precision.jsonl`, `ion_heating_false_dark` is derived from the exact fraction of included bundle frames whose weakest accepted SNR falls below `1.2 * min_accepted_matched_snr`. For the current 100-archive example, that fraction is `0 / 3940 = 0`, so the propagated heating term is zero.
- The critique note is important here: this term is not an external physics guess. It is a conservative camera-diagnostic bound on false-dark risk when the accepted detections are close to threshold.

#### 1. Ion temperature

- PhysRevA.97.032508 excludes data with heating signatures such as unsharp fluorescence edges or disturbed EMCCD ion-crystal images, and otherwise finds no significant dependence on rf voltage or laser detuning.
- TrapDetect cannot watch the same experimental control surfaces directly, but `ALGORITHM.md` already exports several nearby diagnostics: weakest SNR, decision margin, evidence margin, undefined-margin fraction, and `measurement_precision_score`.
- In the current 100-archive example, the median `measurement_precision_score` is `0.46925116660585353`, which indicates stable but not especially clean data quality. This is consistent with the repository's choice to keep heating as a bounded diagnostic term rather than to claim it is physically absent.

#### 2. Ion-ion interactions

- PhysRevA.97.032508 checks for dependence on ion number and finds no significant change in the pressure-corrected decay rate between one-ion and multi-ion runs.
- `notes/run1_validation_audit.md` highlights a related present limitation: the long final epochs in `run1` are mostly multi-ion 2-count holds, not isolated single-ion dark periods.
- The current TrapDetect lifetime helper therefore uses the camera-observed epoch contract directly and does not reinterpret multi-ion visible-count holds as single-ion radiative lifetime measurements.

## PhysRevA.97.032508 (2018): APPENDIX A: LIFETIME EXTRACTION

The appendix headings matter because they show how the paper separates physics systematics from analysis bias. TrapDetect still lacks an equivalent dedicated bias study for any direct radiative-lifetime claim.

### 3. Data sets and analysis bias

- PhysRevA.97.032508 runs pseudorandom simulations matched to the data-taking conditions and finds a residual analysis bias of `-1.8 x 10^-4 s^-1`, attributed to finite time resolution, the lifetime estimator, and other analysis approximations. The paper corrects for that shift and keeps its magnitude as a systematic uncertainty.
- TrapDetect does not yet have an analogous end-to-end bias study for direct lifetime extraction. Its closest current safeguards are the emitted quality diagnostics and the explicit claim limitations in `run1_precision.jsonl`.
- That output currently lists three limitations that matter here: camera-observed visible count is not guaranteed occupancy, the non-final epoch mean is not a direct radiative lifetime, and the external physics systematics are incomplete.
- If the repository later grows a terminal-dark-period lifetime estimator, this appendix is the right model to copy: simulate the exact estimator, quantify its residual bias, then surface that bias as a first-class component.

## PhysRevA.101.062515 (2020): IV. SYSTEMATICS

This paper is valuable because it treats several small optical and detection systematics explicitly, then shows how to bound them with dedicated control experiments rather than with broad qualitative assurances.

### A. Finite pumping times

- PhysRevA.101.062515 concludes that finite pumping times are negligible because the relevant pumping durations exceed roughly 20 time constants, making pumping errors effectively vanishing on the reported scale.
- TrapDetect has no direct laser-pulse timing stream, so it does not model finite pumping times as a named component.
- The nearest current analogue is the internal `timing_window_bias` uncertainty, but that quantity means something narrower: it bounds frame-boundary ambiguity in the image-derived epoch timing, not optical-pumping incompleteness.

### B. Leakage pumping rates

- PhysRevA.101.062515 treats leakage pumping rates wavelength by wavelength and uses dedicated blocking and null tests to bound each one.
- In TrapDetect, all such leakage-light concerns collapse into the external `leakage_light_deshelving` component because the camera pipeline has no way to measure spectral extinction ratios or unwanted scattering rates.
- This is exactly the split endorsed by the critique note: leakage is a real apparatus systematic, not a camera-diagnostic proxy.

#### 1. Stray light at 455 nm

- PhysRevA.101.062515 reports high extinction at 455 nm and bounds unwanted pumping during the experiment window at a negligible level.
- TrapDetect should use this as a literature pattern only. If a future setup reproduces this control experiment, the resulting bound should be entered explicitly as leakage-light uncertainty.

#### 2. Stray light at 614 nm

- PhysRevA.101.062515 uses a dedicated lifetime-style leakage test with the 614 nm light unblocked but nominally switched off, and finds a rate consistent with zero within uncertainty.
- This is closely aligned with the repository's named `leakage_light_deshelving` component. It is exactly the kind of external control measurement that the current CLI is meant to accept.

#### 3. Stray light at 585 nm

- PhysRevA.101.062515 finds the 585 nm leakage rate negligible for the experiment times of interest.
- TrapDetect has no direct equivalent monitor. Any residual concern remains part of the same explicit leakage-light budget.

#### 4. Stray light at 650 nm

- PhysRevA.101.062515 identifies 650 nm leakage as more relevant to pumping out of `D3/2` than to the final detection step, but still quantifies the induced error on the reported observables.
- For TrapDetect, this again supports keeping wavelength-specific optical leakage outside the SNR-derived defaults and inside the explicit physical-input path.

#### 5. Stray light at 493 nm

- PhysRevA.101.062515 finds no shelving events in the dedicated control test and therefore treats this leakage path as negligible.
- The repository does not yet record an analogous apparatus check, so no such conclusion should be imported automatically into the current calculator.

### C. Collisions and detection errors

- PhysRevA.101.062515 is the direct literature anchor for separating bright-state and dark-state detection errors from the underlying atomic physics and for bounding them with control experiments.
- TrapDetect adapts that idea to the information it actually has. Instead of PMT/Bayesian state-detection controls, it uses emitted image-analysis diagnostics to build a conservative `detection_error_bound` when no explicit override is supplied.
- The implemented formula in `calculate_lifetime_precision.py` is `0.85 * undefined_margin_frame_fraction + 0.15 * (1 - measurement_precision_score_median)`, clamped to `[0, 1]`.
- In the current `run1_precision.jsonl` example this yields a fractional bound of `0.08277766761090945`, which propagates to `0.3400542607838382 s` on the current observed mean transition time. The metadata correctly tags this as `origin = snr_derived` and exposes the generating statistics under `source_statistics`.
- The same file shows why this term is currently the dominant internal systematic: `undefined_margin_frame_fraction = 0.003723932472691162`, `measurement_precision_score_median = 0.46925116660585353`, and the median quality score is far from the ideal limit of `1.0`.
- If the user supplies `--detection-error-fraction`, the same component remains in the budget but changes origin from `snr_derived` to `cli_override`.

## Repository-Specific Timing Bound

The literature sections above do not map one-to-one onto TrapDetect's frame-boundary timing term, so it is worth stating that term explicitly.

- `calculate_lifetime_precision.py` defines `timing_window_bias` uncertainty as `undefined_margin_frame_fraction * representative_frame_period_s` whenever those batch diagnostics are available.
- This is not a claim about optical pumping latency or atomic time dilation. It is a claim about the ambiguity introduced when the visible-count transition lies near a frame boundary or when the decision margin is undefined often enough to blur transition timing.
- In the current `run1_precision.jsonl` example, `representative_frame_period_s = 0.04242981772404164` and `undefined_margin_frame_fraction = 0.003723932472691162`, which produces a timing uncertainty of `0.00015800577603292568 s`.
- The repository cites PhysRevA.97.032508 and Mohanty (2015) for the general importance of timing-window analysis, but the implemented bound is explicitly camera-diagnostic and should not be confused with a full apparatus timing calibration.

## Bottom Line

- The prior literature supports a hard boundary between external apparatus physics and internal detection confidence. TrapDetect now follows that boundary explicitly.
- External paper-style inputs remain necessary for `collision_quenching`, `blackbody_radiation`, and `leakage_light_deshelving`.
- Internal confidence-driven terms are allowed to default from the emitted batch diagnostics, and the current implementation does so for `detection_error_bound`, `ion_heating_false_dark`, and `timing_window_bias`.
- The current repository still does not make a direct radiative-lifetime claim from the epoch mean. Any future document that tries to do so will need the missing external physics inputs plus a dedicated analysis-bias study of the kind illustrated in PhysRevA.97.032508 Appendix A.
