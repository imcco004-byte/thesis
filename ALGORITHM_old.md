# Algorithm & Theory

This note documents the single-frame analysis implemented in `analyze_ions_fft.py`.
It is intentionally narrower than a paper: it explains the statistical model,
the signal-processing steps, and the calibrated heuristics that the current
pipeline uses, without claiming more derivation than the code actually supports.

The goal is twofold:

1. make the present implementation scientifically legible
2. provide a stable base for future paper writing and later retuning work

## Scope

This document covers the single-frame path exposed by `analyze_array()` and
`analyze_path()`. Batch tools reuse this result structure but are not derived
here except where they report the same per-frame metrics.

Uncertainty estimates on Fano and mean-variance quantities are computed from
tiles within the current frame. Batch tools may summarize those per-frame
uncertainties later, but no multi-frame pooling is part of the single-frame
scientific claim documented here.

The present downstream use case is a Ba+ $5D_{5/2}$ metastable-state lifetime
experiment. In that setting, the camera-observed visible-ion count can change
because ions are shelved dark during LED-assisted acquisition, not only because
trap occupancy changed. That bright-versus-dark distinction is the standard
electron-shelving measurement picture reviewed for single trapped ions, where a
Ba$^+$ ion can remain trapped while its fluorescence disappears until the
shelved state decays
\cite{Leibfried2003,Madej1990,Gurell2007,Auchter2014,Mohanty2015}.

The motivating experimental family is trapped-ion and trapped-molecular-ion
apparatus with spatially resolved fluorescence detection, stable quasi-1-D ion
configurations, repeated state-detection cycles, and fixed optical paths
rather than unconstrained microscopy scenes
\cite{Leibfried2003,Loh2013,Jain2020,Zhou2024,Wipfli2023}.

## Claim Boundary

The current single-frame claim surface is deliberately limited to image-local
outputs:

- visible-ion count
- accepted-ion centroid and spacing estimates
- PSF width or shape estimates
- per-frame noise parameters
- per-frame confidence and uncertainty diagnostics

Quantities such as `decision_margin`, `evidence_margin`, and
`measurement_precision_score` are detector-confidence diagnostics. They are not
apparatus-physics observables and they do not by themselves justify collision,
blackbody, or leakage-light corrections.

This note therefore does not claim that one frame can directly recover a
radiative lifetime or infer external apparatus systematics from image
statistics alone. Those terms remain downstream, explicit-input quantities as
described in `systematic_error.md`.

A further physical prior comes from how trapped-ion images are formed on
spatial detectors. In the single-ion review by Leibfried et al., linear rf
traps with weak axial confinement produce ion strings aligned along the trap
axis, and CCD-style fluorescence imaging renders individual ions as bright,
optics-limited spots rather than arbitrary extended objects
\cite{Leibfried2003}. The present note uses that review-level context only to
motivate a localized-PSF, one-chain working model; it does not assume that
every frame is an ideal realization of the textbook geometry.

## Observation Model

For one frame, the working image model is

$$
I(r, c) = B(r, c) + \sum_{k=1}^{N} A_k\, h(r-r_k, c-c_k) + \eta(r, c),
$$

where:

- $I(r,c)$ is the observed integer-valued grayscale image
- $B(r,c)$ is a slowly varying background and scatter term
- $N$ is the number of visible ions in the frame
- $A_k$ is the brightness of ion $k$
- $h$ is the effective point-spread function (PSF)
- $(r_k, c_k)$ is the ion location in pixel coordinates
- $\eta(r,c)$ is detector noise

For calibration and eta-runtime work, the implementation also forms the
reconstructed signal field

$$
S(r, c) = \sum_{k=1}^{N} A_k\, h(r-r_k, c-c_k)
$$

and the residual field

$$
r(r, c) = I(r, c) - B(r, c) - S(r, c).
$$

For branch-only manual calibration, this residual is not pooled across the four
public Stage 5 variants. Let

$$
\mathcal{V} = \{
\\text{anisotropic\_gaussian},\\
\\text{symmetric\_gaussian},\\
\\text{anisotropic\_poisson},\\
\\text{symmetric\_poisson}
\}.
$$

For each variant $v \in \mathcal{V}$, the detector forms a branch-specific
reconstruction

$$
S_v(r,c) = \sum_{k=1}^{N_v} A_{v,k}\, h_v(r-r_{v,k}, c-c_{v,k})
$$

and branch-specific residual

$$
r_v(r,c) = I(r,c) - B(r,c) - S_v(r,c).
$$

The manual calibration set is also branch-specific. For each variant $v$, let
$M_v$ be the set of manually scored frames for which that same variant matches
the manual visible-ion count. No calibrated quantity in `manual_calibrated`
mode is pooled across variants.

Two branch-indexed corrections are then derived from $\{r_{v,i}\}_{i \in M_v}$.

First, the branch count-legibility field is the branch residual mean

$$
\bar\eta_v(r,c)
=
\frac{1}{n_v(r,c)}
\sum_{i\in M_v} r_{v,i}(r,c),
\qquad
n_v(r,c)
=
\sum_{i\in M_v} \mathbf{1}_{\mathrm{covered},i}(r,c),
$$

followed by the same Wiener-Khinchin-style structured autocorrelation
projection used elsewhere in the detector. The runtime branch field is then
coherence-gated by $|\bar\eta_v| / \mathrm{SE}_v$ when branch variance
estimates are available and capped for stability. After manual data exists,
this branch-specific field replaces any shared calibrated eta surface. A shared
surface, if retained at all, is only a heuristic pre-manual fallback.

Second, the branch score-admissibility correction uses the branch residual
power spectrum

$$
Q_{v,i}(\omega) = \mathcal{P}[r_{v,i}](\omega)
$$

and the derived branch scalars

$$
P_{\mathrm{mean},v,i} = \operatorname{mean}_{\omega} Q_{v,i}(\omega),
\qquad
P_{\mathrm{peak},v,i} = \max_{\omega} Q_{v,i}(\omega),
$$

$$
R_{v,i}
=
\frac{P_{\mathrm{peak},v,i}}{\max(P_{\mathrm{mean},v,i}, \varepsilon)},
\qquad
L_{v,i} = \log R_{v,i}.
$$

Here $R_{v,i}$ is the branch linear excess-power ratio and $L_{v,i}$ is the
same quantity on an additive scale. The ordering of variants is identical under
$R_{v,i}$ and $L_{v,i}$ because $\log$ is monotone, but the additive log form is
the more natural variable for threshold lifts. If a display-scale quantity is
needed later, it should be derived as

$$
D_{v,i} = 10 \log_{10} R_{v,i},
$$

not used as the canonical runtime parameter.

This branch peak-to-mean ratio is intentionally not the same object as spectral
flatness. Spectral flatness uses the geometric-mean to arithmetic-mean power
ratio and decreases toward $0$ for peaky spectra; by contrast, $R_{v,i}$ rises
above $1$ and $L_{v,i}$ rises above $0$ when residual power concentrates into a
small set of spectral bins. This makes $R_{v,i}$ the physically transparent
multiplicative excess-power quantity and $L_{v,i}$ the formula-first additive
threshold-lift quantity.

Nor should $L_{v,i}$ be confused with the near-DC log power relation used in the
Fourier-envelope PSF fit below. There the detector fits the local spectral shape
$\log P(u,v)$ as a function of $(u,v)$; here it uses $L_{v,i}$ only as a
one-number branch concentration summary.

This remains a calibration/runtime seam, not a new public likelihood family.
The classical anchor is the Wiener-Khinchin autocorrelation/PSD duality
\cite{Wiener1930,Khintchine1934,BlackmanTukey1958}; the log compression of the
branch power ratio follows the same signal-processing logic that motivates
log-domain spectral summaries and spectral-flatness reporting
\cite{Harris1978,Dubnov2004}.

The implementation assumes one approximately vertical ion chain inside a
restricted central region of the frame. It does not attempt full 2-D object
segmentation or multi-chain inference.

This one-chain prior is a trap-geometry assumption motivated by quasi-1-D ion
strings and aligned ion-trap optics, not a general claim about arbitrary image
formation \cite{Loh2013,Jain2020,Zhou2024,Wipfli2023}.

The detector-family anchors used later are the classical Fano dispersion index
and the mean-variance relation used in photon-transfer calibration
\cite{Fano1947,Janesick2007,MortensenFlyvbjerg2016}. For EMCCD-like data,
the code uses the excess-noise-factor-near-2 family as a detector-model anchor,
not as a learned parameter \cite{RobbinsHadwen2003}.

## Pipeline Overview

The single-frame pipeline has six stages:

1. background statistics and detector-regime diagnostics
2. noise power spectrum (NPS) diagnostics
3. prefilter selection
4. chain corridor detection and PSF estimation
5. matched-filter detection and count decision
6. state-level and spectral summary metrics

The key distinction throughout this note is:

- principled quantity: tied directly to a statistical model or standard signal-processing construction
- calibrated quantity: a threshold, band, prior, or fallback chosen for engineering robustness on the current instrument/data family

## 1. Background Statistics

The image is partitioned into non-overlapping tiles. For each tile, the code
computes a sigma-clipped mean and variance:

$$
(\hat\mu_j, \hat\sigma_j^2) = \operatorname{SigmaClip}(T_j; k_\sigma, n_{\mathrm{iter}}).
$$

This provides robust local background summaries that suppress hot pixels and
other impulsive outliers before detector-regime inference is attempted. The use
of robust location/scale estimation is standard; the exact clip radius and
iteration count remain engineering choices \cite{BeersFlynnGebhardt1990}.

The local Fano factor is then

$$
F_j = \frac{\hat\sigma_j^2}{\max(\hat\mu_j, \varepsilon)}.
$$

From the dimmer tiles, the pipeline reports a representative frame-level Fano
factor and fits a mean-variance relation

$$
\hat\sigma_j^2 \approx a\, \hat\mu_j + b.
$$

A quadratic extension in $\hat\mu_j$ is not part of the current contract.
On the present manual-review and synthetic detector anchors, it gives only
small in-sample $R^2$ gains while usually worsening small-sample AICc once the
extra coefficient is penalized, so the documented implementation remains linear.

The code also reports single-frame uncertainty for these quantities. The
frame-level Fano uncertainty is estimated from the spread of dim-tile Fano
samples within the same frame, and the slope/intercept uncertainties are taken
from the regression on that same tile ensemble. This keeps the estimator
single-frame even when later batch tooling summarizes many per-frame outputs
\cite{Fano1947,Janesick2007,MortensenFlyvbjerg2016}.

Interpretation:

- $F \approx 1$ and $a \approx 1$ are consistent with Poisson-like photon counting
- $F \approx 2$ and $a \approx 2$ are consistent with EMCCD-like excess noise
- substantially larger values indicate over-dispersion, structured background, quantization, or other non-Poisson effects

The targets $F=1$ and $F=2$ are principled detector-model anchors. The actual
tolerance bands used around them are calibrated defaults. In the current code,
those hard bands coexist with an internal soft-evidence layer whose widths are
tempered by the reported single-frame uncertainty rather than by multi-frame
pooling.

## 2. Noise Power Spectrum Diagnostics

From the darkest tiles, the code computes a Hann-windowed average power
spectrum \cite{BlackmanTukey1958,Harris1978}:

$$
P(u,v) = \frac{1}{M} \sum_{m=1}^{M} \left| \mathcal{F}\left[w \cdot (T_m - \bar T_m)\right](u,v) \right|^2.
$$

This supports three compact diagnostics.

### Whiteness Ratio

Low-frequency and high-frequency annuli are averaged and compared:

$$
R_{\mathrm{white}} = \frac{\langle P \rangle_{\mathrm{low}}}{\langle P \rangle_{\mathrm{high}}}.
$$

Values near $1$ indicate approximately white spatial noise.

### Spectral Flatness

The code computes

$$
\operatorname{SF} = \frac{\exp\left(\langle \log P \rangle\right)}{\langle P \rangle},
$$

which equals $1$ for a perfectly flat spectrum and drops below $1$ as power
concentrates into bands or peaks \cite{Dubnov2004}.

### Directional Anisotropy

Second moments of the PSD about the Fourier origin provide a coarse anisotropy
ratio. This checks whether the noise has a preferred direction, such as banding
or readout structure.

These constructions are principled. The cutoffs that define "whiteish" behavior
are calibrated thresholds.

### Single-Frame Uncertainty

The three NPS diagnostics are also reported with explicit standard errors
derived from the spread across the within-frame dark-tile ensemble. Each dark
tile yields an independent realization of whiteness, log spectral flatness, and
log directional anisotropy; the reported standard errors use a MAD-based
robust location standard error \cite{BeersFlynnGebhardt1990} on those
samples. These errors are aggregated into a downstream
`measurement_precision_score` that softens, but does not override, the hard
regime label.

## 3. Regime Classification

The detector-regime classifier combines Fano behavior, kurtosis, and NPS
whiteness to assign a label used later by the prefilter stage.

The implemented flags correspond to the following informal decision logic:

- `poissonish`: Fano factor lies close to the Poisson target
- `emccd_like`: Fano factor lies closer to the EMCCD target
- `over_dispersed`: Fano factor is materially above the EMCCD family
- `tails_ok`: darkest-patch kurtosis is not excessively heavy-tailed
- `whiteish`: the NPS is sufficiently flat across coarse low/high bands

This is a model-informed decision tree, not a learned classifier and not a
formal likelihood-ratio test. The targets are principled; the relative
tolerances are calibrated. The public label remains a hard compatibility
projection, while the internal detector-family evidence carries the single-frame
uncertainty from the Fano and mean-variance estimates.

### Regime-Driven Noise Model Selection

The regime label is also used downstream when the matched-filter detections are
rescored. The implementation always evaluates four SNR/count variants for each
frame:

- `anisotropic_gaussian`
- `anisotropic_poisson`
- `symmetric_gaussian`
- `symmetric_poisson`

The selected noise model is a hard gate:

- if `regime_label == "photon_counting"`, the primary exported noise model is Poisson
- otherwise, the primary exported noise model is Gaussian

The selected template family still comes from the PSF/template policy, so the
public `selected_snr_variant` is the selected template family crossed with that
regime-driven noise-model choice.

There is no separate "Poisson PSF" kernel in the current implementation.
The two spatial templates are still the Gaussian PSF families estimated in
Stage 6:

At the observation-model level, Gaussian-noise and Poisson-counting images are
indeed fundamentally different. If the expected image is

$$
\lambda(r,c) = B(r,c) + A\,h(r-r_0,c-c_0),
$$

then an additive-Gaussian working model treats the residual
$I(r,c)-\lambda(r,c)$ as approximately normal, whereas an ideal photon-counting
model uses the Poisson likelihood

$$
p\bigl(I\mid \lambda\bigr)
= \prod_{r,c}
\frac{\lambda(r,c)^{I(r,c)} e^{-\lambda(r,c)}}{I(r,c)!},
$$

or equivalently the negative log-likelihood, up to constants independent of
$\lambda$,

$$
-\log p\bigl(I\mid \lambda\bigr)
= \sum_{r,c}\left[\lambda(r,c) - I(r,c)\log \lambda(r,c)\right] + \text{const}.
$$

Those are not the same statistical model. The present implementation does not
claim to solve the exact Poisson likelihood. Instead it factorizes the problem
into:

- a spatial PSF template $h$, represented here by anisotropic or symmetric Gaussian kernels
- a detector-noise branch, represented here by Gaussian or Poisson-style response normalization

That factorization is a pragmatic approximation common in photon-limited PSF
estimation and localization workflows, where the optical blur model remains
Gaussian-like while the count statistics are treated separately
\cite{Fano1947,Janesick2007,Thompson2002,Ober2004,Mortensen2010}.

$$
K_{\mathrm{aniso}}(x,y;\sigma_x,\sigma_y)
= Z_{\mathrm{aniso}}^{-1}
\exp\!\left[-\frac{1}{2}\left(\frac{x^2}{\sigma_x^2} + \frac{y^2}{\sigma_y^2}\right)\right],
$$

$$
K_{\mathrm{sym}}(x,y;\sigma_{\mathrm{iso}})
= Z_{\mathrm{sym}}^{-1}
\exp\!\left[-\frac{x^2+y^2}{2\sigma_{\mathrm{iso}}^2}\right],
\qquad
\sigma_{\mathrm{iso}} = \sqrt{\sigma_x\sigma_y},
$$

with $Z_{\mathrm{aniso}}$ and $Z_{\mathrm{sym}}$ chosen so the discrete kernel
has unit $L^2$ norm. This keeps the spatial model aligned with the standard
elliptical-Gaussian working approximation used for photon-limited point-source
images, while allowing the detector to preserve anisotropy when the Stage 6
width estimates support it \cite{Thompson2002,Ober2004,Mortensen2010}.

The Poisson branch now changes the candidate-local decision statistic itself,
not only the noise normalization. The corridor search and provisional peak
generation are still seeded by the matched-filter response, but each refined
candidate is rescored on a local raw-image patch by a Poisson count model. For
one refined candidate patch $Y_k$ with candidate-local background mean
$\mu_{\mathrm{local},k}$ and a unit-sum PSF patch $p_k$ built from the selected
template family, the null and alternative expected counts are

Here the Gaussian kernels above use $(x,y)$ as template coordinates, but the
Poisson likelihood is evaluated over the discrete pixels of the refined patch,
so $(r,c)$ are patch-local row and column indices on that support.
$Y_k(r,c)$ is the observed raw-image count at that pixel, $p_k(r,c)$ is the
selected unit-sum PSF patch on the same support, $\mu_{\mathrm{local},k}$ is
the candidate-local background mean, and $A_k$ is the nonnegative candidate
amplitude.

$$
\lambda_{0,k}(r,c) = \mu_{\mathrm{local},k},
\qquad
\lambda_{1,k}(r,c; A_k) = \mu_{\mathrm{local},k} + A_k\,p_k(r,c),
$$

with $A_k \ge 0$ fitted by minimizing the Poisson negative log-likelihood (or
equivalently the Cash statistic up to constants independent of the model)
\cite{Cash1979,Donath2022}:

$$
C(\lambda \mid Y_k) = \sum_{r,c}\left[\lambda(r,c) - Y_k(r,c)\log\lambda(r,c)\right].
$$

The candidate-local deviance improvement is then

$$
\Delta D_k = 2\left[C\left(\lambda_{0,k}\mid Y_k\right) - C\left(\lambda_{1,k}(\hat A_k)\mid Y_k\right)\right],
$$

and the implementation maps that improvement onto an SNR-like score by
normalizing with the effective PSF support

$$
N_{\mathrm{eff},k} = \left(\sum_{r,c} p_k(r,c)^2\right)^{-1},
$$

$$
S_{\mathrm{poisson},k} = \max\left\{\sqrt{\frac{\Delta D_k}{N_{\mathrm{eff},k}}} - 1,\ 0\right\}.
$$

The subtract-1 centering term is an engineering correction for the finite-patch
null baseline; it keeps pure-background patches near zero while preserving the
same hard threshold interface used by the rest of Stage 5. This is therefore a
candidate-local Poisson likelihood detector, not a full-image Richardson-Lucy or
Bayesian deconvolution pipeline \cite{Cash1979,Donath2022}.

For the anisotropic-Poisson variant specifically, the PSF patch $p_k$ is built
from $K_{\mathrm{aniso}}$ and the candidate score is

$$
\mathrm{score}_{\mathrm{aniso,poisson},k} = S_{\mathrm{poisson},k}.
$$

The symmetric-Poisson branch is identical except that $K_{\mathrm{sym}}$ is used
in place of $K_{\mathrm{aniso}}$ when forming $p_k$. The Gaussian branch keeps the
classical matched-filter statistic

$$
\mathrm{SNR}_{\mathrm{gaussian}} = \frac{r}{\sigma_{\mathrm{gaussian}}}.
$$

So the current four-variant surface is a Cartesian product of

- spatial model: anisotropic or symmetric Gaussian optical PSF
- decision statistic: Gaussian matched SNR or centered local Poisson score

Even when one variant is chosen as the primary result, all four variant
summaries are still exported in `snr_variants`. This is why later review and
batch tools can inspect Gaussian-versus-Poisson disagreements without rerunning
the detector.

## 4. Prefilter Selection

The prefilter stage chooses one of three actions:

1. median filter for impulsive or heavy-tailed noise \cite{HuangYangTang1979}
2. small Gaussian blur for clean, white-ish Poisson or EMCCD regimes
3. no prefilter when structured background is better handled by the later bandpass

The hot-pixel control limit uses a Gaussian-tail exceedance model. If a pixel
is declared "hot" when it exceeds the darkest-patch mean by $k$ standard
deviations, then the expected one-sided exceedance probability is

$$
p_k = \Pr(Z > k), \qquad Z \sim \mathcal N(0,1).
$$

For $n$ pixels, the code uses a binomial-style upper control limit

$$
p_k + z\, \sqrt{\frac{p_k(1-p_k)}{n}}.
$$

This control-limit form is a principled binomial-tail approximation; for the
underlying binomial-proportion setting and the limits of simple
normal-approximation interval logic, see
\cite{Wilson1927,BrownCaiDasGupta2001}. The choices of $k$, $z$, kernel size,
and Gaussian blur width are calibrated engineering defaults.

## 5. Corridor Detection and Bandpass Isolation

The chain is assumed to lie in a restricted central search region. Within that
ROI, the code forms a Difference-of-Gaussians bandpass image

$$
I_{\mathrm{DoG}} = G_{\sigma_s} * I - G_{\sigma_l} * I,
$$

where $\sigma_s$ preserves ion-scale structure and $\sigma_l$ suppresses slow
background variation.

This is a standard bandpass construction. The actual scales are calibrated to
the current image family \cite{MarrHildreth1980}.

### Corridor Score

For each column inside the ROI, the code sums the top $k$ non-negative pixels:

$$
S(c) = \sum_{i=1}^{k} x_{(i)}(c),
$$

where $x_{(i)}(c)$ are the $k$ largest positive values in column $c$ after
sorting. The score is then lightly smoothed in 1-D and maximized over column.

This is not the unique optimal estimator of chain position. It is a sparse,
engineering proxy designed to favor narrow columns containing several bright
ion-like features instead of broad diffuse scatter. The idea is motivated by
the imaging geometry; the exact `column_topk` and corridor half-width are
calibrated heuristics.

For quasi-1-D trapped-ion strings, this kind of narrow-corridor search is
operationally useful because the bright features are expected to cluster along a
single trap axis even when per-ion amplitudes vary. That geometry matches the
linear-trap picture in which ions line up along the axis and appear on spatial
fluorescence imagers as separated bright dots whose apparent width is set
mainly by the optics
\cite{Leibfried2003,Jain2020,Zhou2024,Wipfli2023}.

## 6. PSF Estimation

The matched filter requires a PSF estimate, but PSF estimation itself requires
a corridor location. The current code resolves this bootstrap dependency in two
steps:

1. detect a provisional corridor on the DoG image
2. estimate the PSF from local patches around provisional peaks

### Local Real-Space Estimate

For several bright provisional peaks, a local patch is background-subtracted and
its second moments are measured. For a patch $J$, the centroid and widths are

$$
\hat c_x = \frac{\sum x J(x,y)}{\sum J(x,y)},
\qquad
\hat c_y = \frac{\sum y J(x,y)}{\sum J(x,y)},
$$

$$
\hat\sigma_x^2 = \frac{\sum (x-\hat c_x)^2 J(x,y)}{\sum J(x,y)},
\qquad
\hat\sigma_y^2 = \frac{\sum (y-\hat c_y)^2 J(x,y)}{\sum J(x,y)}.
$$

These are principled moment estimators for a localized positive source, though
they are not exact maximum-likelihood estimates; the pixelated-source
localization literature makes clear both the usefulness and the efficiency
limits of such estimators relative to likelihood-based methods and
Cramer-Rao-style bounds \cite{Thompson2002,Ober2004,Mortensen2010}.

### Fourier-Envelope Estimate

For a Gaussian PSF, the log power spectrum near DC satisfies

$$
\log P(u,v) \approx c - 4\pi^2\left(\sigma_x^2 u^2 + \sigma_y^2 v^2\right).
$$

The code fits this model by weighted least squares on a near-origin region whose
power rises above the NPS floor. This makes the fit emphasize the highest-SNR
spectral bins.

### Reconciliation

If the local and Fourier estimates are broadly consistent, the code averages
them. Otherwise it falls back to the local estimate. If no usable patches
exist, the code uses the fine DoG scale and a fixed anisotropy ratio as a
fallback prior.

The local-moment and Fourier-envelope models are principled. The consistency
window, fit region, minimum point count, and fallback anisotropy ratio are
calibrated heuristics.

## 7. Matched Filter and Candidate Detection

With PSF widths $\sigma_x$ and $\sigma_y$, the code constructs an anisotropic
Gaussian kernel

$$
K(x,y) = Z^{-1}\exp\!\left[-\frac{1}{2}\left(\frac{x^2}{\sigma_x^2} + \frac{y^2}{\sigma_y^2}\right)\right]
$$

and normalizes it in $L^2$:

$$
\|K\|_2 = 1.
$$

When the template policy selects the symmetric family, the same construction is
used with a single isotropic width $\sigma_{\mathrm{iso}} = \sqrt{\sigma_x\sigma_y}$.
This is why the exported variant names are the Cartesian product of
{anisotropic, symmetric} and {gaussian, poisson}: the first word names the PSF
shape family, while the second names the noise model used to convert matched
response into SNR \cite{Thompson2002,Ober2004,Mortensen2010,Turin1960}.

The response is computed as FFT-based cross-correlation

$$
R = I_{\mathrm{DoG}} \star K.
$$

For additive white noise and a known template, the matched filter is the
classical optimal linear detector. In practice, the code uses this logic under
the regime checks above and reports the diagnostics so the user can judge when
the assumptions are strained \cite{Turin1960}.

The corridor is then re-estimated on the matched-filter response because the
response has higher contrast than the raw DoG image.

### Axial Candidate Generation

The response is averaged across corridor columns to produce a 1-D axial profile.
Peaks are found subject to minimum distance, height, and prominence rules.

This stage is a candidate generator, not the final count decision. The peak
height/prominence/distance settings are calibrated heuristics that seed the
later auditable threshold rule.

## 8. Local Refinement and SNR

For each candidate row peak, the code refines the column inside the corridor,
extracts a local patch, and computes:

- sub-pixel centroid
- local widths
- integrated signal
- local background mean and noise scale
- matched-filter response and matched SNR

If $\sigma_R$ is the estimated background standard deviation of the matched
response, then the matched SNR is

$$
\operatorname{SNR}_{\mathrm{matched}} = \frac{R(r_k, c_k)}{\sigma_R}.
$$

The response-noise estimate itself is taken from weak-bandpass regions so that
bright ions do not dominate the background estimate. That quantile-based mask is
an engineering choice, not a universal law.

## 9. Count Decision and Margin Diagnostics

The final visible-ion count is the cardinality of the accepted candidate set.
The base implemented acceptance rule is explicit:

$$
\\text{accept candidate on branch } v \iff s_{v,k} \ge \\tau_0,
$$

with base threshold $\tau_0 =$ `min_accepted_matched_snr`.

In branch-only manual calibration, the second correction acts as a mathematical
threshold lift rather than as a shared post hoc penalty. For each branch $v$,
let the current branch residual power summary be

$$
R_v^{\ast}
=
\frac{P_{\mathrm{peak},v}^{\ast}}{\max(P_{\mathrm{mean},v}^{\ast}, \varepsilon)},
\qquad
L_v^{\ast} = \log R_v^{\ast},
$$

and let the branch manual references be

$$
\\tilde L_v = \operatorname{median}_{i\in M_v} L_{v,i},
$$

The accepted margin-to-threshold measurements $m_{v,i}$ remain useful audit
statistics, but the first branch-local threshold-lift law should be additive
in the log-power deviation itself rather than multiplied by a second branch
scale. The recommended first branch-local law is

$$
\Delta \tau_v = \max(0, L_v^{\ast} - \tilde L_v),
$$

so the branch decision rule becomes

$$
\\text{accept candidate on branch } v \iff s_{v,k} \ge \\tau_v^{\ast},
\qquad
\\tau_v^{\ast} = \\tau_0 + \Delta \\tau_v.
$$

This preserves the public Stage 5 interface: the branch score family is
unchanged, the threshold remains explicit, and the second correction raises the
threshold only when the current branch residual power is more concentrated than
the manual-match branch reference. Because $L_v = \log R_v$ is already the
additive form of the multiplicative excess-power ratio, an additional margin
multiplier would be an external scaling rather than an immanent continuation of
the same contradiction. Gaussian and Poisson variants share this threshold-lift
form; what differs across variants is the branch score $s_{v,k}$ and the
branch spectral calibration reference.

Within the selected noise-regime branch, Stage 5 may still apply an internal
accepted-set correction when the accepted many do not cohere as a stable one.
This includes accepted-set negation to zero or reduction to a smaller subset.
The public contract does not change: the reported count remains the cardinality
of the final accepted set after those branch-internal consistency checks.

The important scientific feature of the implementation is not that
$\tau_0 = 5.6$ is derived from first principles, but that the count decision is
auditable through the reported base threshold, branch threshold lift, and
reported margins.

If the accepted and rejected branch-score sets are $A_v$ and $B_v$, the code reports

$$
m_{\mathrm{acc},v} = \min A_v - \tau_v^{\ast},
\qquad
m_{\mathrm{rej},v} = \tau_v^{\ast} - \max B_v,
$$

$$
g_v = \min A_v - \max B_v,
\qquad
m_{\mathrm{near},v} = \min\{m_{\mathrm{acc},v}, m_{\mathrm{rej},v}\},
$$

where finite. These diagnostics quantify how close the frame is to changing the
ion count under the current branch rule.

## 10. State-Level Metrics

For accepted ions with matched SNR values $s_1, \dots, s_N$, the code reports

$$
\rho_{\mathrm{rss}} = \sqrt{\sum_{k=1}^{N} s_k^2},
$$

along with the weakest-ion SNR, the mean ion SNR, and a spatial spacing metric
derived from the median separation between detected rows.

The root-sum-square summary is an engineering aggregate. It is not a posterior
probability or a sufficient statistic for every downstream task, but it is a
stable scalar summary of per-frame signal strength.

## 11. Spectral Chain Metric

The matched-filter response inside the corridor is Fourier transformed and its
power is averaged over a narrow horizontal-frequency band. The dominant positive
vertical-frequency peak gives a spectral spacing estimate:

$$
f_{\mathrm{axial}} = \arg\max_{f>0} P_{\mathrm{vertical}}(f),
\qquad
\hat d_{\mathrm{spectral}} = \frac{1}{f_{\mathrm{axial}}}.
$$

The code also reports a spectral state SNR by comparing the dominant peak to a
robust noise floor within that 1-D profile.

This is a comb-signature heuristic rather than a full lattice-model fit. Its
motivation is the near-periodic axial structure expected from trapped-ion
strings and related ion-array platforms, not a claim that this exact spectral
summary is a canonical estimator \cite{Jain2020,Loh2013}.

## 12. Ion-Count Epoch Lifetimes

The batch layer (`run_npz_batch.py`) tracks how long the camera reports a given
visible-ion count within a single archive. An **epoch** is a maximal run of
consecutive frames — ordered by source frame label — sharing the same
`visible_ion_count`. For every epoch the pipeline records:

- `ion_count` — the per-frame visible-ion count during the epoch (or `null`
  for errored frames),
- `start_frame`, `end_frame` — the first and last source frame labels
  inside the epoch,
- `frame_lifetime` — the number of frames the count was held,
- `start_time_s`, `end_time_s`, `real_time_lifetime_s` — default wall-clock
  lifetime fields for the epoch. `end_time_s` remains the timestamp of the
  last observed frame in the epoch, while `real_time_lifetime_s` runs from the
  epoch start to the next epoch boundary when one exists; for the final epoch
  it falls back to `end_time_s - start_time_s`. Values are `NaN` when frame
  timestamps are unavailable,
- `errored` — `true` when the epoch corresponds to frames that failed
  analysis (no ion count is defined),
- `decrease_flag` — `true` when entering this epoch reduced the camera-observed
  visible-ion count relative to the previous non-errored epoch.

For the present Ba+ lifetime context, these epochs are not interpreted as
literal loading-or-loss segments. At the start of data collection, LED-driven
fluorescence and state preparation can make some or all trapped ions appear
dark to the camera, so the observed visible-ion count is a state-detection
observable rather than a guaranteed occupancy count. In the trapped-ion
electron-shelving picture reviewed by Leibfried et al., the measured quantity
is exactly this bright-versus-dark fluorescence level: a Ba$^+$ ion can remain
trapped while its fluorescence drops during shelving and later returns when
the metastable state decays \cite{Leibfried2003}. The current contract is
therefore a contract for **camera-observed metastable-state epochs**: a strict
visible-count decrease is surfaced for review, but it is not by itself a claim
that an ion left the trap
\cite{Leibfried2003,Madej1990,Gurell2007,Auchter2014,Mohanty2015}.
Transitions that involve an errored epoch on either side are never marked as
decrease events; the comparison waits for the next real count.

An `ion_count = 0` epoch is a valid trap state (empty trap) and is handled
by the same rules. Only a value-to-value decrease trips the flag.

A run with exactly one epoch means only that no visible-count transition was
detected across the analyzed frames.

This is an engineering heuristic, not a likelihood-ratio test: the pipeline
exposes every decrease transition so downstream review can decide whether a
decrease was physical (loss) or an upstream artifact (PSF drift, background
excursion). Aggregate outputs include `n_epochs`, `n_decrease_events`,
`max_frame_lifetime`, `mean_frame_lifetime`, `initial_ion_count`, and
`final_ion_count` in `summary["epoch_summary"]`, plus aligned bundle
arrays (`run__{name}__epoch_*`) and JSONL `type: "epoch"` /
`type: "epoch_summary"` records.

The motivating context is repeated monitoring of trapped-ion or
trapped-molecular-ion states over sustained apparatus runs, where state
preparation/detection, optical alignment, trap stability, and metastable-state
lifetime systematics matter alongside per-frame localization
\cite{Loh2013,Ni2014,Zhou2024,Wipfli2023,Madej1990,Gurell2007,Auchter2014,Mohanty2015}.

### Epoch Calculation Procedure (Implementation Contract)

The implementation in `run_npz_batch.py::compute_ion_count_epochs` follows
this deterministic procedure:

1. Build an ordered frame stream from per-frame digests and per-frame errors.
  Digest rows carry integer ion counts; error rows carry `ion_count = null`.
2. Sort by source frame label using trailing-integer order (for example,
  `frame_002 < frame_010 < frame_100`).
3. Scan the ordered stream and merge maximal contiguous runs with identical
  ion count into one epoch.
4. Emit per-epoch fields:
  `epoch_index`, `ion_count`, `start_frame`, `end_frame`,
  `frame_lifetime`, `errored`, `decrease_flag`.
5. Always emit `start_time_s`, `end_time_s`, and `real_time_lifetime_s`.
  `end_time_s` is the timestamp of the last observed frame in the epoch.
  `real_time_lifetime_s` uses the next epoch start time as the boundary when
  one exists, so non-final epochs are not shortened by one frame interval; the
  final epoch falls back to `end_time_s - start_time_s`. When frame timestamps
  are unavailable, these values are `NaN`.
6. Compute `decrease_flag` only for strict value-to-value decreases against the
  previous non-errored epoch. Errored epochs do not trigger decreases and do
  not reset the previous real count.
7. Produce summary fields:
  `n_epochs`, `n_decrease_events`, `decrease_transitions`,
  `max_frame_lifetime`, `mean_frame_lifetime`,
  `max_real_time_lifetime_s`, `mean_real_time_lifetime_s`,
  `total_real_time_s`, `initial_ion_count`, `final_ion_count`.

An `ion_count = 0` epoch is a valid state and is handled with the same
rules as all other integer counts.

### Verification Status (2026-04-24)

Epoch calculations are currently verified by test suites that exercise both
the direct algorithm and pipeline integration paths.

- `pytest -q tests/test_ion_epochs.py`: **25 passed**
- `pytest -q tests/test_e2e.py tests/test_e2e_real_data.py`: **24 passed**

These checks validate the contract above, including:

- epoch construction from contiguous equal-count runs,
- strict-decrease detection semantics,
- errored-epoch behavior across transitions,
- zero-ion validity,
- bundle and JSONL surfacing of epoch fields,
- batch decrease-aware prefix aggregation behavior.

### Batch-Level Transition Lifetime Pooling

For batch-level reporting, a single pooled mean transition lifetime is computed
across all runs one archive at a time; decrease flags are never computed across
archive boundaries. The per-epoch `decrease_flag` contract is unchanged: it is
only the cutoff marker that defines the safe prefix. For one run with no
decrease flags, the safe prefix is all non-final epochs. For one run with a
decrease, the safe prefix ends immediately before the epoch adjacent to the
first decrease. Concretely, if epoch $k$ is the first epoch with
`decrease_flag = true`, then the safe epochs are $0, \dots, k-2$.

Those safe epochs are not averaged directly. They are first converted into
cumulative transition samples. If the safe epoch durations are
$e_1, e_2, \dots, e_m$, then the emitted samples are

$$
e_1,\quad e_1 + e_2,\quad \dots,\quad e_1 + \cdots + e_m.
$$

The batch mean is the arithmetic mean over those cumulative samples, computed
in both frame-count and real-time forms when the required time metadata are
finite. Runs with exactly one epoch are excluded as `single_epoch` because the
final epoch is never retained and would otherwise contribute no transition
sample. Runs with no safe retained epochs after the first-decrease rule are
excluded with reason `decrease_events`. Runs with no epochs at all are excluded
with reason `no_epochs`.

Excluded runs are listed with reason codes in the bundle scalars
`batch_transition_lifetime_{mean_frame_lifetime,mean_real_time_lifetime_s,n_runs_included,n_runs_excluded,n_epochs_considered,n_epochs_real_time_considered,included_runs,excluded_runs,excluded_reasons}`.
The same information is surfaced as a `type: "batch_transition_lifetime"`
JSONL record and — after extraction — in `batch_summary.jsonl` next to the
per-run JSONL files. Bundle v8 extends that batch summary with typed
`snr_variant_batch_summary` rows that preserve per-variant disagreement and
count/SNR aggregates for audit purposes, but those variant rows do not replace
the selected-summary batch metrics. This is an engineering aggregate, not a
likelihood estimate: it is only meaningful for downstream review of stable
camera-observed metastable-state segments that precede the first visible-count
decrease within each run. A short leading `ion_count = 0` startup epoch is a
valid camera-dark state under this contract and, when it lies inside the
retained safe prefix, contributes to the cumulative transition samples the same
way as any other retained non-final epoch. Risky detection warnings such as the
weakest-SNR disparity audit remain per-frame diagnostics and do not participate
in epoch exclusion.

### Lifetime Precision From Mean Transition Lifetime

The downstream helper script `calculate_lifetime_precision.py` uses the batch
summary field `mean_real_time_lifetime_s` from the
`batch_transition_lifetime` contract as the lifetime estimate $\hat\tau$ and
keeps the calculation in double precision throughout. With
$N = \texttt{n_epochs_real_time_considered}$ and user-supplied absolute
systematic terms $u_i$ in seconds, it reports

The mediation chain for that downstream use is now explicit: the detector in
`analyze_ions_fft.py` feeds per-run reduction in `analyze_batch.py`, the
multi-run orchestrator `run_npz_batch.py` publishes the bundle, and only then
do `extract_npz_json.py` and `calculate_lifetime_precision.py` consume the
selected-summary batch contract. The preserved v8 variant payload is available
for audit and review, but this pass intentionally does not let disagreement
between variants alter the lifetime estimate.

$$
u_{\mathrm{stat}} = \frac{\hat\tau}{\sqrt{N}}, \qquad
u_{\mathrm{sys}} = \sqrt{\sum_i u_i^2}, \qquad
u_{\mathrm{tot}} = \sqrt{u_{\mathrm{stat}}^2 + u_{\mathrm{sys}}^2}.
$$

This is intentionally a downstream uncertainty budget, not a new hidden-model
fit inside the detector pipeline. The central estimate comes directly from the
camera-observed batch mean transition time in seconds, computed from the same
epoch system above: safe pre-decrease epoch prefixes retained, the epoch
immediately preceding the first decrease excluded, single-epoch runs excluded,
and final epochs omitted. The result should be read as a precision summary for
the observed metastable-state sequence rather than a claim about true trap
occupancy in every frame
\cite{Madej1990,Gurell2007,Auchter2014,Mohanty2015}.

## Calibration Table

The current defaults mix statistical anchors with calibrated operational
constants. The table below is intended as an explicit contract for reviewers.

| Parameter | Default | Role | Status |
| --- | ---: | --- | --- |
| `bg_block_shape` | `(64, 64)` | tile size for robust local background statistics | engineering default |
| `sigma_clip` | `3` | outlier rejection radius | standard robust-statistics choice |
| `background_quantile` | `0.35` | dim-tile subset for mean-variance fit | calibrated safeguard |
| `dark_tile_count` | `6` | number of tiles used for NPS | engineering default |
| `fano_poisson_tol` | `0.5` | relative band around Poisson target | calibrated detector-family tolerance |
| `fano_emccd_tol` | `0.5` | relative band around EMCCD target | calibrated detector-family tolerance |
| `kurtosis_max` | `10` | heavy-tail cutoff for Gaussian-like assumptions | calibrated safeguard |
| `whiteness_lo`, `whiteness_hi` | `0.5`, `2.0` | acceptable whiteness band | calibrated safeguard |
| `prefilter_gaussian_sigma` | `0.8 px` | mild denoising blur | calibrated stability setting |
| `median_size` | `3` | impulsive-noise suppression | engineering default |
| `hot_pixel_sigma` | `6` | hot-pixel exceedance definition | calibrated safeguard |
| `hot_pixel_fraction_floor` | `0.001` | minimum allowed hot-pixel limit | engineering floor |
| `hot_pixel_tail_zscore` | `5` | width of exceedance control limit | calibrated safeguard |
| `search_row_fraction`, `search_col_fraction` | `(0.15, 0.9)`, `(0.3, 0.7)` | central ROI restriction | instrument/data prior |
| `dog_small_sigma`, `dog_large_sigma` | `1.2 px`, `12 px` | ion-scale bandpass | calibrated scale prior |
| `search_half_width` | `30 px` | corridor half-width | instrument/data prior |
| `column_topk` | `20` | sparse column score | calibrated heuristic |
| `peak_min_distance` | `12 px` | candidate separation floor | calibrated heuristic |
| `peak_threshold_sigma` | `1.25` | candidate seed threshold | calibrated heuristic |
| `peak_prominence_sigma` | `1.2` | candidate seed prominence | calibrated heuristic |
| `local_patch_radius` | `12 px` | local PSF/refinement support size | engineering default |
| `psf_r_frac` | `0.25` | Fourier-fit radius fraction | calibrated heuristic |
| `psf_cN` | `2` | power above NPS floor for Fourier fit | calibrated heuristic |
| `psf_min_points` | `25` | minimum bins for Fourier fit | engineering safeguard |
| `sigma_min_px` | `1.5 px` | sampling plausibility check | model-informed safeguard |
| `psf_r2_min` | `0.7` | Gaussian-fit plausibility check | calibrated safeguard |
| `psf_consistency_tol` | `0.3` | local-vs-FFT agreement window | calibrated safeguard |
| `eta_mode` | `"off"` / `"manual_calibrated"` | off or branch-only calibrated mode | constrained public contract |
| `eta_variant_count_legibility_npz_path` | `None` | branch-indexed count-legibility artifact carrying one structured runtime field per variant | calibration input |
| `eta_score_admissibility_npz_path` | `None` | branch-indexed score artifact carrying branch power summaries, linear power ratios, log power ratios, thresholds, and margins | calibration input |
| `eta_max_abs_correction` | `1.5` | runtime cap for the branch structured count-legibility projection | calibrated safeguard |
| `eta_runtime_min_coherence` | `1.0` | minimum per-pixel coherence ratio $\lvert\bar\eta_v\rvert / \mathrm{SE}_v$ retained in the branch count-legibility runtime mask when branch variance estimates are available | calibrated safeguard |
| `log_power_spectrum_peak_to_mean` | derived | canonical branch log-power quantity $L_v = \log(P_{\mathrm{peak},v} / \max(P_{\mathrm{mean},v}, \varepsilon))$ | derived branch calibration quantity |
| `max_ions` | `20` | hard experimental cap | experiment constraint |
| `min_accepted_matched_snr` | `5.6` | base Stage 5 threshold $\tau_0$ before any branch-local threshold lift | calibrated decision boundary |
| `axial_frequency_band` | `0.06 cyc/px` | spectral comb averaging band | calibrated heuristic |
| `evidence_margin` | derived | log-odds of chosen ion count over nearest alternative | reported diagnostic |
| `measurement_precision_score` | derived ∈ [0,1] | aggregated confidence from SNR, margin, and uncertainty | reported diagnostic |

## Known Heuristic Surfaces

The current code exposes a mix of theory-backed standard methods and
deliberately calibrated engineering surfaces. Each surface below is tagged so
it is clear whether the rule follows from a standard result or from
instrument-specific tuning.

1. Tiled sigma-clipped local background statistics — **theory-backed**:
   robust location/scale estimation \cite{BeersFlynnGebhardt1990}.
   Calibrated part: clip radius and iteration count.
2. Fano and mean-variance targets ($F=1$, $a=1$; $F=2$, $a=2$) —
   **theory-backed**: photon-transfer / Fano model and EMCCD excess-noise
   model \cite{Fano1947,Janesick2007,MortensenFlyvbjerg2016,RobbinsHadwen2003}.
   Calibrated part: relative-deviation tolerances around the targets.
3. Hann-windowed averaged periodogram and spectral flatness —
   **theory-backed** \cite{BlackmanTukey1958,Harris1978,Dubnov2004}.
   Calibrated part: whiteness low/high annulus radii.
4. Single-frame uncertainty on Fano, mean-variance slope/intercept, and NPS
   whiteness/flatness/anisotropy — **theory-backed**: linear-regression
   standard errors \cite{Janesick2007} and MAD-based robust location SE
   \cite{BeersFlynnGebhardt1990}.
5. Regime-family soft scores (photon-counting, EMCCD, over-dispersed,
   compressed-or-artifact) — **theory-backed** in target location;
   **still-calibrated** in soft-score width and the hard-label projection.
6. Hot-pixel Gaussian-tail binomial control limit — **theory-backed**:
   one-sided Gaussian exceedance + binomial proportion control limit.
   Calibrated part: the sigma threshold $k$ and control-limit width $z$.
7. Gaussian prefilter with small $\sigma$ and $3\times3$ median filter —
   **theory-backed** as standard denoisers \cite{HuangYangTang1979}.
   Calibrated part: the prefilter-selection weights and the fallback to "none".
8. Difference-of-Gaussians bandpass and Gaussian matched filter —
   **theory-backed** \cite{MarrHildreth1980,Turin1960}.
   Calibrated part: DoG scales and PSF fallback anisotropy ratio.
9. Sparse top-$k$ corridor score — **still-calibrated**: engineering proxy for
   narrow-chain geometry, not a canonical estimator.
10. Provisional peak-finding thresholds (height, prominence, min distance) —
    **still-calibrated**: candidate generator only; feeds an auditable
    matched-SNR threshold.
11. PSF reconciliation window and no-patch fallback prior — **still-calibrated**.
12. Weak-band quantile mask for matched-response noise — **still-calibrated**.
13. Final Stage 5 base threshold $\tau_0$ —
  **still-calibrated decision boundary**. On Gaussian branches the score is
  matched SNR; on Poisson branches it is the centered local Poisson score
  above. An auxiliary confidence-weighted `evidence_margin` is reported for
  transparency but does not change the published count.
14. Branch residual spectral objects for count-legibility and score-admissibility —
  **theory-backed** in the Wiener-Khinchin autocorrelation / power-spectrum
  duality \cite{Wiener1930,Khintchine1934,BlackmanTukey1958};
  **still-calibrated** in the branch manual-match inclusion rule, the
  connected-support extraction, the per-pixel coherence gate, and the runtime
  absolute-correction cap used for the branch count-legibility field.
15. Branch power-ratio and log-power summaries — **theory-backed** as monotone
  summaries of periodogram concentration and log-domain dynamic-range
  compression \cite{Harris1978,Dubnov2004}; **still-calibrated** in the use of
  peak-to-mean residual power and the branch reference median used for the
  first additive threshold-lift law
  $\Delta\tau_v = \max(0, L_v^{\ast} - \tilde L_v)$.

These do not invalidate the method. They mark where future work can replace
calibrated operational rules with stronger detector-specific or probabilistic
models.

## References

The citations above use `\cite\{key\}` anchors tied to the BibTeX-style entries
below. Anchor keys match the in-text citations exactly.

```bibtex
@article{Wiener1930,
  author  = {Wiener, Norbert},
  title   = {Generalized Harmonic Analysis},
  journal = {Acta Mathematica},
  volume  = {55},
  pages   = {117--258},
  year    = {1930},
  doi     = {10.1007/BF02546511}
}

@article{Khintchine1934,
  author  = {Khintchine, A.},
  title   = {Korrelationstheorie der station{"a}ren stochastischen Prozesse},
  journal = {Mathematische Annalen},
  volume  = {109},
  number  = {1},
  pages   = {604--615},
  year    = {1934},
  doi     = {10.1007/BF01449156}
}

@article{Chen2022,
  author  = {Chen, Yuanyuan and Chen, Lixiang},
  title   = {Quantum Wiener-Khinchin Theorem for Spectral-Domain Optical Coherence Tomography},
  journal = {Physical Review Applied},
  volume  = {18},
  pages   = {014077},
  year    = {2022},
  doi     = {10.1103/PhysRevApplied.18.014077}
}

@article{Fano1947,
  author  = {Fano, U.},
  title   = {Ionization Yield of Radiations. II. The Fluctuations of the Number of Ions},
  journal = {Physical Review},
  volume  = {72},
  pages   = {26--29},
  year    = {1947}
}

@article{Cash1979,
  author  = {Cash, W.},
  title   = {Parameter estimation in astronomy through application of the likelihood ratio},
  journal = {The Astrophysical Journal},
  volume  = {228},
  pages   = {939--947},
  year    = {1979},
  doi     = {10.1086/156922}
}

@book{Janesick2007,
  author    = {Janesick, J. R.},
  title     = {Photon Transfer: DN to $\lambda$},
  publisher = {SPIE Press},
  year      = {2007}
}

@article{MortensenFlyvbjerg2016,
  author  = {Mortensen, K. I. and Flyvbjerg, H.},
  title   = {Calibration-on-the-spot: How to calibrate an {EMCCD} camera from its images},
  journal = {Scientific Reports},
  volume  = {6},
  pages   = {28680},
  year    = {2016}
}

@article{RobbinsHadwen2003,
  author  = {Robbins, M. S. and Hadwen, B. J.},
  title   = {The noise performance of electron multiplying charge-coupled devices},
  journal = {IEEE Transactions on Electron Devices},
  volume  = {50},
  pages   = {1227--1232},
  year    = {2003}
}

@article{Donath2022,
  author  = {Donath, Axel and Siemiginowska, Aneta and Kashyap, Vinay and Burke, Douglas and Solipuram, Karthik Reddy and van Dyk, David},
  title   = {Pylira: deconvolution of images in the presence of Poisson noise},
  journal = {Proceedings of the Python in Science Conference},
  year    = {2022},
  doi     = {10.25080/majora-212e5952-00f}
}

@book{BlackmanTukey1958,
  author    = {Blackman, R. B. and Tukey, J. W.},
  title     = {The Measurement of Power Spectra},
  publisher = {Dover},
  year      = {1958}
}

@article{Harris1978,
  author  = {Harris, F. J.},
  title   = {On the Use of Windows for Harmonic Analysis with the Discrete Fourier Transform},
  journal = {Proceedings of the IEEE},
  volume  = {66},
  pages   = {51--83},
  year    = {1978}
}

@article{Dubnov2004,
  author  = {Dubnov, S.},
  title   = {Generalization of Spectral Flatness Measure for Non-{G}aussian Linear Processes},
  journal = {IEEE Signal Processing Letters},
  volume  = {11},
  pages   = {698--701},
  year    = {2004}
}

@article{HuangYangTang1979,
  author  = {Huang, T. S. and Yang, G. J. and Tang, G. Y.},
  title   = {A Fast Two-Dimensional Median Filtering Algorithm},
  journal = {IEEE Transactions on Acoustics, Speech, and Signal Processing},
  volume  = {27},
  pages   = {13--18},
  year    = {1979}
}

@article{MarrHildreth1980,
  author  = {Marr, D. and Hildreth, E.},
  title   = {Theory of Edge Detection},
  journal = {Proceedings of the Royal Society of London. Series B},
  volume  = {207},
  pages   = {187--217},
  year    = {1980}
}

@article{Turin1960,
  author  = {Turin, G. L.},
  title   = {An Introduction to Matched Filters},
  journal = {IRE Transactions on Information Theory},
  volume  = {6},
  pages   = {311--329},
  year    = {1960}
}

@article{BeersFlynnGebhardt1990,
  author  = {Beers, T. C. and Flynn, K. and Gebhardt, K.},
  title   = {Measures of Location and Scale for Velocities in Clusters of Galaxies: A Robust Approach},
  journal = {Astronomical Journal},
  volume  = {100},
  pages   = {32--46},
  year    = {1990}
}

@article{Wilson1927,
  author  = {Wilson, E. B.},
  title   = {Probable Inference, the Law of Succession, and Statistical Inference},
  journal = {Journal of the American Statistical Association},
  volume  = {22},
  pages   = {209--212},
  year    = {1927}
}

@article{BrownCaiDasGupta2001,
  author  = {Brown, L. D. and Cai, T. T. and DasGupta, A.},
  title   = {Interval Estimation for a Binomial Proportion},
  journal = {Statistical Science},
  volume  = {16},
  pages   = {101--133},
  year    = {2001}
}

@article{Thompson2002,
  author  = {Thompson, R. E. and Larson, D. R. and Webb, W. W.},
  title   = {Precise Nanometer Localization Analysis for Individual Fluorescent Probes},
  journal = {Biophysical Journal},
  volume  = {82},
  pages   = {2775--2783},
  year    = {2002}
}

@article{Ober2004,
  author  = {Ober, R. J. and Ram, S. and Ward, E. S.},
  title   = {Localization Accuracy in Single-Molecule Microscopy},
  journal = {Biophysical Journal},
  volume  = {86},
  pages   = {1185--1200},
  year    = {2004}
}

@article{Mortensen2010,
  author  = {Mortensen, K. I. and Churchman, L. S. and Spudich, J. A. and Flyvbjerg, H.},
  title   = {Optimized Localization Analysis for Single-Molecule Tracking and Super-Resolution Microscopy},
  journal = {Nature Methods},
  volume  = {7},
  pages   = {377--381},
  year    = {2010}
}

@article{Leibfried2003,
  author  = {Leibfried, D. and Blatt, R. and Monroe, C. and Wineland, D.},
  title   = {Quantum Dynamics of Single Trapped Ions},
  journal = {Reviews of Modern Physics},
  volume  = {75},
  pages   = {281--324},
  year    = {2003},
  doi     = {10.1103/RevModPhys.75.281}
}

@article{Loh2013,
  author  = {Loh, H. and Cossel, K. C. and Grau, M. C. and Ni, K.-K. and Meyer, E. R. and Bohn, J. L. and Ye, J. and Cornell, E. A.},
  title   = {Precision Spectroscopy of Polarized Molecules in an Ion Trap},
  journal = {Science},
  volume  = {342},
  pages   = {1220--1222},
  year    = {2013}
}

@article{Ni2014,
  author  = {Ni, K.-K. and Loh, H. and Grau, M. and Cossel, K. C. and Ye, J. and Cornell, E. A.},
  title   = {State-specific detection of trapped HfF+ by photodissociation},
  journal = {Journal of Molecular Spectroscopy},
  volume  = {300},
  pages   = {12--15},
  year    = {2014}
}

@article{Jain2020,
  author  = {Jain, S. and Alonso, J. and Grau, M. and Home, J. P.},
  title   = {Scalable Arrays of Micro-Penning Traps for Quantum Computing and Simulation},
  journal = {Physical Review X},
  volume  = {10},
  pages   = {031027},
  year    = {2020}
}

@article{Zhou2024,
  author  = {Zhou, Y. and Island, J. O. and Grau, M.},
  title   = {Quantum logic control and precision measurements of molecular ions in a ring trap: An approach for testing fundamental symmetries},
  journal = {Physical Review A},
  volume  = {109},
  pages   = {033107},
  year    = {2024}
}

@article{Wipfli2023,
  author  = {Wipfli, O. and Fernandes Passagem, H. and Fischer, C. and Grau, M. and Home, J. P.},
  title   = {Integration of a high finesse cryogenic build-up cavity with an ion trap},
  journal = {Review of Scientific Instruments},
  volume  = {94},
  pages   = {083204},
  year    = {2023}
}

@article{Madej1990,
  author  = {Madej, A. A. and Sankey, J. D.},
  title   = {Quantum jumps and the single trapped barium ion: Determination of collisional quenching rates for the 5d$^2$D$_{5/2}$ level},
  journal = {Physical Review A},
  volume  = {41},
  pages   = {2621--2630},
  year    = {1990},
  doi     = {10.1103/PhysRevA.41.2621}
}

@article{Gurell2007,
  author  = {Gurell, J. and Bi{\'e}mont, E. and Blagoev, K. and Fivet, V. and Lundin, P. and Mannervik, S. and Norlin, L.-O. and Quinet, P. and Rostohar, D. and Royen, P. and Schef, P.},
  title   = {Laser-Probing Measurements and Calculations of Lifetimes of the 5d$^2$D$_{3/2}$ and 5d$^2$D$_{5/2}$ Metastable Levels in {Ba II}},
  journal = {Physical Review A},
  volume  = {75},
  pages   = {052506},
  year    = {2007},
  doi     = {10.1103/PhysRevA.75.052506}
}

@article{Auchter2014,
  author  = {Auchter, Carolyn and Noel, Thomas W. and Hoffman, Matthew R. and Williams, Spencer R. and Blinov, Boris B.},
  title   = {Measurement of the branching fractions and lifetime of the 5D$_{5/2}$ level of {Ba}$^+$},
  journal = {Physical Review A},
  volume  = {90},
  pages   = {060501},
  year    = {2014},
  doi     = {10.1103/PhysRevA.90.060501}
}

@article{Mohanty2015,
  author  = {Mohanty, Amita and Dijck, Elwin A. and Nu{\~n}ez Portela, Mayerlin and Valappol, Nivedya and Grier, Andrew T. and Meijknecht, Thomas and Willmann, Lorenz and Jungmann, Klaus},
  title   = {Lifetime measurement of the 5d$^2$ D$_{5/2}$ state in {Ba}$^+$},
  journal = {Hyperfine Interactions},
  volume  = {233},
  pages   = {113--119},
  year    = {2015},
  doi     = {10.1007/s10751-015-1161-9}
}
```

## Existing Test Anchors

The repo already contains tests that support the main claims documented here:

- `tests/test_invariants.py` checks Poisson Fano behavior, mean-variance slope, NPS whiteness, flatness, anisotropy, and regime consistency
- `tests/test_crossval.py` checks local-vs-FFT PSF consistency and prefilter robustness
- `tests/test_unit.py` checks exact count-decision margin semantics
- `tests/test_synthetic.py` checks synthetic count, centroid, spacing, PSF, and localization-trend behavior inside the detector-core scope
- `tests/test_higher_validation.py` holds the deferred CRLB-style localization bound outside the detector-core acceptance gate

Those tests do not prove universal optimality. They do provide concrete anchors
for what the present implementation is claiming.
