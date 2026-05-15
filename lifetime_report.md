# Lifetime Report

Source bundle: trapdetect_results_2026-05-15_at14h22m56s_rt01h31m50s_500npz.npz
Bundle schema version: trapdetect-bundle-v9
Source path: C:/Users/isaia/Desktop/run3
Reported run count: 500

## Mode Summary

| Mode | Sample kind | Mean s | Median s | Samples | Runs in | Runs out | red. chi2 | tau_D s | tau_S s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| batch_transition | batch_transition_safe_prefix_cumulative | 13.0937 | NA | 557 | 480 | 20 | NA | NA | NA |
| epoch_cumulative_nonfinal | observed_cumulative_nonfinal_epoch_transition_time | 28.3755 | 28.5928 | 4802 | 481 | 19 | 146.006 | NA | NA |
| paper_nonfinal_interval | observed_nonfinal_epoch_interval_time | 3.99358 | 0.159017 | 4802 | 481 | 19 | 995.382 | NA | NA |
| paper_weighted_brightening | observed_cumulative_bright_transition_time | 13.1326 | 9.03772 | 535 | 467 | 33 | 1.69111 | NA | NA |
| paper_segmented_brightening | observed_segmented_bright_transition_time | 7.89768 | 3.18944 | 2230 | 481 | 19 | 15.8757 | NA | NA |
| paper_segmented_darkening | observed_segmented_dark_transition_time | 0.891694 | 0.141579 | 1980 | 471 | 29 | 1.12967e+13 | NA | NA |
| paper_k_interval_least_squares | paper_k_interval_weighted_least_squares_fit | 11.7129 | NA | 4210 | 481 | 19 | NA | 11.7129 | 10.6365 |

## Comparison Against Batch Transition

| Comparison mode | Reference mean s | Comparison mean s | Delta s | Ratio | Reference samples | Comparison samples |
| --- | --- | --- | --- | --- | --- | --- |
| epoch_cumulative_nonfinal | 13.0937 | 28.3755 | 15.2818 | 2.16711 | 557 | 4802 |
| paper_nonfinal_interval | 13.0937 | 3.99358 | -9.10008 | 0.305001 | 557 | 4802 |
| paper_weighted_brightening | 13.0937 | 13.1326 | 0.0389792 | 1.00298 | 557 | 535 |
| paper_segmented_brightening | 13.0937 | 7.89768 | -5.19598 | 0.603168 | 557 | 2230 |
| paper_segmented_darkening | 13.0937 | 0.891694 | -12.202 | 0.0681012 | 557 | 1980 |
| paper_k_interval_least_squares | 13.0937 | 11.7129 | -1.38081 | 0.894544 | 557 | 4210 |

## Distribution Diagnostics

| Mode | Sample count | Mean s | Median s | P10 s | P90 s | Std s | Raw interval mean s |
| --- | --- | --- | --- | --- | --- | --- | --- |
| batch_transition | NA | NA | NA | NA | NA | NA | NA |
| epoch_cumulative_nonfinal | 4802 | 28.3755 | 28.5928 | 6.21875 | 50.4707 | 15.8305 | 3.99358 |
| paper_nonfinal_interval | 4802 | 3.99358 | 0.159017 | 0.108383 | 14.2025 | 8.06448 | 3.99358 |
| paper_weighted_brightening | 535 | 13.1326 | 9.03772 | 1.35281 | 31.6247 | 12.4857 | 12.5576 |
| paper_segmented_brightening | 2230 | 7.89768 | 3.18944 | 0.122128 | 22.8136 | 10.3976 | 7.58401 |
| paper_segmented_darkening | 1980 | 0.891694 | 0.141579 | 0.105535 | 1.01466 | 3.19063 | 0.880195 |
| paper_k_interval_least_squares | 4210 | 4.43115 | 0.196039 | 0.10879 | 15.518 | 8.43693 | 4.43115 |

## Selection Diagnostics

| Mode | Excluded reasons | Initial count histogram | Peak count histogram |
| --- | --- | --- | --- |
| batch_transition | NA | NA | NA |
| epoch_cumulative_nonfinal | {"single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |
| paper_nonfinal_interval | {"single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |
| paper_weighted_brightening | {"decrease_before_valid_sample": 1, "multi_jump_transition": 13, "single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |
| paper_segmented_brightening | {"single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |
| paper_segmented_darkening | {"no_darkening_segments": 10, "single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |
| paper_k_interval_least_squares | {"single_epoch": 19} | {"0": 494, "1": 6} | {"0": 19, "1": 348, "2": 21, "3": 82, "4": 16, "5": 6, "6": 5, "7": 3} |

## K-Interval Fit States

| n_total | dark_count | Count | Mean interval s | Observed rate s^-1 | Fitted rate s^-1 |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1010 | 0.155106 | 6.44719 | 0.0940159 |
| 1 | 1 | 1021 | 12.9525 | 0.0772049 | 0.0853763 |
| 2 | 0 | 21 | 0.154816 | 6.45929 | 0.188032 |
| 2 | 1 | 71 | 3.37503 | 0.296294 | 0.179392 |
| 2 | 2 | 53 | 8.0256 | 0.124601 | 0.170753 |
| 3 | 0 | 226 | 4.69015 | 0.213213 | 0.282048 |
| 3 | 1 | 364 | 3.68161 | 0.27162 | 0.273408 |
| 3 | 2 | 206 | 2.42157 | 0.412955 | 0.264768 |
| 3 | 3 | 131 | 3.51456 | 0.284531 | 0.256129 |
| 4 | 0 | 15 | 0.129482 | 7.72307 | 0.376064 |
| 4 | 1 | 94 | 3.22654 | 0.30993 | 0.367424 |
| 4 | 2 | 133 | 1.04272 | 0.959028 | 0.358784 |
| 4 | 3 | 92 | 1.43765 | 0.695578 | 0.350145 |
| 4 | 4 | 50 | 1.73657 | 0.575848 | 0.341505 |
| 5 | 0 | 3 | 0.191117 | 5.2324 | 0.470079 |
| 5 | 1 | 14 | 0.123256 | 8.11318 | 0.46144 |
| 5 | 2 | 44 | 0.652621 | 1.53228 | 0.4528 |
| 5 | 3 | 73 | 1.37641 | 0.726526 | 0.444161 |
| 5 | 4 | 85 | 0.540198 | 1.85117 | 0.435521 |
| 5 | 5 | 44 | 1.69199 | 0.59102 | 0.426881 |
| 6 | 1 | 9 | 0.149576 | 6.68556 | 0.555456 |
| 6 | 2 | 64 | 0.150709 | 6.6353 | 0.546816 |
| 6 | 3 | 86 | 0.869201 | 1.15048 | 0.538177 |
| 6 | 4 | 41 | 0.9785 | 1.02197 | 0.529537 |
| 6 | 5 | 30 | 0.397478 | 2.51586 | 0.520897 |
| 6 | 6 | 23 | 2.79409 | 0.357899 | 0.512258 |
| 7 | 1 | 1 | 0.149072 | 6.70816 | 0.649472 |
| 7 | 2 | 7 | 0.183675 | 5.44439 | 0.640832 |
| 7 | 3 | 49 | 0.164369 | 6.08388 | 0.632192 |
| 7 | 4 | 72 | 0.525915 | 1.90145 | 0.623553 |
| 7 | 5 | 24 | 0.606238 | 1.64952 | 0.614913 |
| 7 | 6 | 27 | 0.577554 | 1.73144 | 0.606274 |
| 7 | 7 | 27 | 1.92401 | 0.519747 | 0.597634 |

## Figure Suite

The companion `lifetime_report.json` mirrors the complete bundle-backed suite used here.
It includes per-mode measurement summaries, comparisons against the batch transition baseline, selection diagnostics, histogram bin payloads, and the per-state rows for the k-interval least-squares fit.
The same structured rows are also emitted into `batch_summary.jsonl` as `lifetime_mode_summary`, `lifetime_mode_comparison`, `lifetime_mode_selection`, `lifetime_mode_diagnostics`, `lifetime_mode_histogram`, and `lifetime_mode_fit_state` records.

