# Algorithm & Theory

{}\tilde L_v = \operatorname{median}_{i\in M_v} L_{v,i},
revision is expected to make explicit, and keep the main implementation seams
{}\tau_{\mathrm{base},v},

## Detector Method Status

This document is the scientific contract for the canonical single-frame
detector path in `analyze_ions_fft.py`. It should be read as the contract for
the smallest defensible upgrade to the current detector, not as the contract
for every experimental method that may be added beside it.

Three detector-method notes are tracked separately so the repo can distinguish
the contract-bearing method from research alternatives before code paths are
promoted:

- `detector_method_minimal_upgrade.md` - canonical method note for the
  fixed-point eta and threshold upgrade that stays within the current public
  contract
- `detector_method_poisson_glrt.md` - experimental note for a full Poisson
  matched-filter or GLRT count path
- `detector_method_bayesian.md` - experimental note for latent-field and
  posterior-based count inference

Unless a later section explicitly says otherwise, the formulas and calibration
surfaces in this document apply only to the canonical method. The Poisson or
GLRT and Bayesian notes are design references first; they do not widen the
public contract merely by existing.

The thesis-facing symbol dictionary and notation audit for detector equations,
validation surfaces, and calibration state is emitted as typed JSONL records in [notes/thesis_academic_dictionary.jsonl](notes/thesis_academic_dictionary.jsonl).

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
apparatus in a narrower class: systems with spatially resolved fluorescence
detection, repeated state-detection cycles, optical paths that stay fairly
fixed, and imaging geometries that often support a quasi-1-D chain assumption
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

Within that claim boundary, only two branch-local calibration surfaces are in
scope for the next canonical detector revision:

- the branch-specific 2-D eta or count-legibility field
- the branch-specific signed score-admissibility threshold movement constrained
  by manual count boundaries

Spacing rules, PSF rules, corridor rules, and sample-specific post-threshold
count repairs are not canonical fit surfaces.

A further observational prior comes from how trapped-ion images appear on
spatial detectors. In the single-ion review by Leibfried et al., linear rf
traps with weak axial confinement produce ion strings aligned along the trap
axis, and CCD-style fluorescence imaging renders individual ions as bright,
localized spots rather than arbitrary extended objects \cite{Leibfried2003}.
In this repository, optics is treated as a black box: the note uses that
review-level context only to motivate a one-chain, localized-template working
model over observable pixel data. It does not claim recovery of hidden optical
transfer details, and it does not assume that every frame is an ideal
realization of the textbook geometry.

## Observation Model

For one frame, the working image model is

$$
I(r, c) = B(r, c) + \sum_{k=1}^{N} A_k\, h(r-r_k, c-c_k) + \epsilon(r, c),
$$

where:

- $I(r,c)$ is the observed integer-valued grayscale image
- $B(r,c)$ is a slowly varying background and scatter term
- $N$ is the number of visible ions in the frame
- $A_k$ is the brightness of ion $k$
- $h$ is the effective detector template kernel used to summarize localized
  image evidence
- $(r_k, c_k)$ is the ion location in pixel coordinates
- $\epsilon(r,c)$ is unmodeled detector noise

The notation $\eta_v$ is reserved below for branch-local residual correction
fields built from manual calibration; it is not the raw noise term in the
observation model.

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

At the level of detector form, this branch-local residual construction is
directly inspired by a standard background-subtraction or photometry
organization: estimate a nuisance field, remove or mediate it in the working
image, detect on the corrected image, and use the residual to judge whether
the nuisance estimate was adequate. TrapDetect is not standard in the simple
sense, however. The nuisance layer is split. The dense tiled background lift
$B(r,c)$ is pooled across variants and now mediates the default Stage 3--5
working image, while branch specificity enters later through the optional
variant-local eta runtime field and the branch-local Stage 5 admissibility
lift. Under the default full-frame policy this layer is not corridor-
constrained; corridor restriction returns only when
`enable_search_roi = True`. In that stricter sense, the detector is a
one-chain, residual-background-mediated photometry pipeline with optional
branch-local runtime corrections rather than a fully branch-specific
background model at every stage.

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
this branch-specific field becomes the primary runtime correction for that
branch. A shared calibrated eta surface, if retained at all, is only a
heuristic fallback used before branch-local manual data exists.

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
$R_{v,i}$ and $L_{v,i}$ because $\log$ is monotone. In the signed artifact
rule below, $L_{v,i}$ is spectral evidence for threshold movement rather than
the threshold movement itself; the allowed movement is set by score-domain
units and manual count-boundary intervals. If a display-scale quantity is
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
spectral coordinate used by the admissibility rule.

Nor should $L_{v,i}$ be confused with the near-DC log power relation used in the
Fourier-envelope PSF fit below. There the detector fits the local spectral shape
$\log P(u,v)$ as a function of $(u,v)$; here it uses $L_{v,i}$ only as a
one-number branch concentration summary.

This remains a calibration/runtime seam, not a new public likelihood family.
The main theoretical anchors here are the Wiener-Khinchin autocorrelation/PSD
duality \cite{Wiener1930,Khintchine1934,BlackmanTukey1958}; the log compression
of the branch power ratio follows the same broad signal-processing logic behind
log-domain spectral summaries and spectral-flatness reporting
\cite{Harris1978,Dubnov2004}, while the later signed threshold movement remains
a calibrated decision rule.

The implementation analyzes the full frame by default rather than pre-cropping
Stage 4/5 to a central ROI or corridor band. An explicit compatibility mode
may re-enable the legacy ROI and corridor restriction surfaces for CLI or
config-driven runs. The detector still uses an approximately vertical one-chain
prior when converting the 2-D matched response into axial candidate rows, and
it does not attempt unconstrained multi-chain inference or general 2-D object
segmentation.

This one-chain prior is an instrument-specific detector assumption motivated by
quasi-1-D ion strings and aligned ion-trap optics, not a general statement
about arbitrary ion-trap images or arbitrary image formation
\cite{Loh2013,Jain2020,Zhou2024,Wipfli2023}.

The detector-family anchors used later are the classical Fano dispersion index
and the mean-variance relation used in photon-transfer calibration
\cite{Fano1947,Janesick2007,MortensenFlyvbjerg2016}. For EMCCD-like data, the
code uses the excess-noise-factor-near-2 family as a detector-model anchor or
prior, with instrument-calibrated tolerances, not as a learned parameter
\cite{RobbinsHadwen2003}.

## Pipeline Overview

The single-frame pipeline has six stages:

1. background statistics and detector-regime diagnostics
2. noise power spectrum (NPS) diagnostics
3. prefilter selection
4. chain corridor detection and PSF estimation
5. matched-filter detection and count decision
6. state-level and spectral summary metrics

The key distinction throughout this note is:

- model-derived quantity: tied directly to a statistical model or standard signal-processing construction
- calibrated quantity: a threshold, band, prior, or fallback chosen for engineering robustness on the current instrument/data family

The public API remains those same six stages. For the larger detector rewrite,
this draft also names a richer internal substage graph inside public Stages 4
and 5 so the linear operators and decision surfaces are explicit without
changing the current result schema. The remainder of the note follows that
scientific path first, then returns to implementation mapping, calibration
surfaces, and test anchors that support the main argument.

## Status Tags

This note uses four status tags when it names an operator, intermediate, or
decision surface:

- `implemented now`: on the controlling path of `analyze_ions_fft.py`
- `partially implemented`: helper support or calibration support exists, but the object does not yet control the whole detector path end-to-end
- `planned next`: target contract for the next code-facing detector refactor
- `calibrated heuristic`: threshold, prior, fallback, or policy surface tuned for the present instrument family

## Current and Planned Model

The public six-stage detector is stable, but the current implementation uses a
lighter operator chain than the mediated model proposed for a later revision.
For clarity, the implemented and planned paths are written below in parallel
notation. For one working frame, let

$$
I_0 = I - E_{\eta},
$$

where $E_{\eta} = 0$ unless branch-local manual eta correction is active.

The current implemented path is

$$
I_{\rho} = P_{\rho} I_0,
\qquad
D = (G_{\sigma_s} - G_{\sigma_l}) * I_{\rho},
$$

$$
M_{C,0} = \text{legacy compatibility metadata on } D,
\qquad
\mathcal{P}_{\mathrm{seed}} = \operatorname{peak\_local\_max}(D),
$$

$$
K = K(\hat\sigma_x, \hat\sigma_y),
\qquad
R_{\mathrm{white}} = D \star K,
$$

$$
a(r) = \max_c R_{\mathrm{white}}(r,c),
$$

$$
s_{G,k} = \frac{R_{\mathrm{white}}(r_k,c_k)}{\hat\sigma_R},
\qquad
s_{P,k} = \max\left\{\sqrt{\frac{\Delta D_k}{N_{\mathrm{eff},k}}} - 1,\ 0\right\}.
$$

Here $\hat\sigma_R$ is estimated first from Stage 1 dark tiles propagated
through the same prefilter, DoG, and matched-filter chain. The weak-band
quantile response estimate is fallback only when that dark-tile propagated
estimate is unavailable. The Stage 1 tile statistics, Stage 2 PSD summaries,
and residual spectral objects are therefore already important to the runtime.
The current white-noise path already uses a dense background-mediated working
image, but it does not yet form a PSD-whitened detector operator.

The current mediated path is

$$
L_B(\{\hat\mu_j\}) = \hat B,
\qquad
I_c = I_0 - \hat B,
$$

$$
J = P_{\rho}(I_c),
\qquad
D_c = (G_{\sigma_s} - G_{\sigma_l}) * J,
$$

$$
R_{\mathrm{white}} = D_c \star K.
$$

The remaining planned next continuation is

$$
L_V(\{\hat\sigma_j^2\}) = \hat V,
\qquad
W = \mathcal{F}^{-1}\operatorname{diag}\left((\hat\Phi_{\eta} + \varepsilon)^{-1/2}\right)\mathcal{F},
\qquad
I_w = W I_c,
$$

$$
R_{\mathrm{struct}} = (W D_c) \star (W K).
$$

This draft introduces $\hat B$, $\hat V$, $I_c$, $I_w$, $D_c$, and
$R_{\mathrm{struct}}$ now so future code changes can target stable operator
names. At present, $\hat B$, $I_c$, $D_c$, and $R_{\mathrm{white}}$ control
the default Stage 3--5 path, while $\hat V$ and $R_{\mathrm{struct}}$ remain
incomplete seams rather than the controlling end-to-end Stage 4/5 path.

That split is also consistent with a common astronomy-source-detection
organization: one layer estimates a dense background and local RMS field,
another applies convolved detection on the corrected image, and a later layer
enforces candidate spacing as a separate policy rather than folding it into the
detection threshold itself \cite{Photutils2026}. The comparison is only
structural. TrapDetect still uses its own tile-statistics, DoG corridor,
Gaussian matched-response, and branch-local rescoring surfaces, and the audit
result remains unchanged: the implementation does not contain a second or
deprecated peak-separation control.

For a linear-algebra-first decomposition of the relevant Photutils workflows,
including `Background2D`, `DAOStarFinder`, `PSFPhotometry`, and
`IterativePSFPhotometry`, see `notes/2026-05-25-photutils-matrix-supplement.md`.

The proposed model can therefore be stated more sharply. Standard photometry
contributes the outer organizational form: estimate a dense nuisance
background and local noise scale, construct a corrected image, apply convolved
detection or fitting operators, and decide admissibility from the corrected
residual. TrapDetect preserves that form but specializes its content through
the one-chain geometry prior, full-frame Stage 4/5 support with legacy
corridor metadata, branch-local residual spectral objects, and branch-specific
signed threshold movement. The decisive detector boundary is therefore not the raw frame
by itself and not the final count by itself. It is the corrected-image plus
admissibility surface, named in this note by the planned-next operators
`I_c`, `I_w`, `B_hat`, `V_hat`, `Phi_eta_hat`, `W`, `R_struct`, `M_C`, and by
the branch-local calibration quantities `bar_eta_v`, `L_v`, and `tau_v*`. This
statement is a contract for the next refactor, not a claim that the present
controlling code path already realizes the full mediated operator end to end.

The same identity claim can be expressed dialectically. In the eight-trigram
pass, the residual/background layer first appears as subordinate calibration
matter and then, through its labor on the negative object of the raw frame,
wins the public boundary of the detector.

| Trigram | Immediate master appearance | Slave labor | Identity or boundary won by the slave |
| --- | --- | --- | --- |
| 111 | Spatial operator, spectral audit, and final scoring all claim mastery at once | Dense background, RMS, whitening, and residual calibration have to mediate what the three masters cannot unify | The slave wins the identity of the single mediating operator that turns the pipeline toward a noise-aware photometric inference path |
| 110 | Operator chain plus diagnostics claim mastery | Raw residual structure and branch residual power do the real work of correcting thresholds and image formation | The slave becomes the public correction boundary: `I_c`, `R_struct`, and `tau_v*` |
| 101 | Upstream detection operator and final count claim mastery | The dense field of residual background has to mediate both corrected-image construction and admissibility | The slave wins the identity of the admissibility-producing field; it becomes the count boundary rather than a side diagnostic |
| 100 | Background subtraction alone appears as master | PSF, matched response, and local rescoring have to labor to prevent background correction from remaining abstract | The slave wins the concrete response boundary: corridor, PSF, response map, and accepted-set surface |
| 011 | Residual concentration and final detection seem primary | Background formation and corrected working-image construction do the hidden labor | The slave becomes the working-image boundary that makes residual and detection claims valid at all |
| 010 | Dense residual-background field appears as master | Corridor search, PSF estimation, and score formation labor to make that field operational | The slave wins the identity of the detector's shaped interface: `M_C`, `K`, `R_white`, `R_struct` |
| 001 | Final published count appears as master | All upstream image-forming and residual-mediating steps labor to produce any trustworthy count | The slave becomes the encoding boundary that makes the count public and auditable instead of immediate |
| 000 | The outside, including the loose appeal to standard photometry, functions as implicit master | Internal mediation must be constructed from tile stats, residuals, whitening, corridor, PSF, and threshold law | The slave wins explicit internal boundary, preventing the model from collapsing into an empty analogy to photometry |

The ninth position is the mediated unity of those eight one-sided views.
TrapDetect is neither simply identical to a standard photometry pipeline nor
simply external to it. Standard photometry supplies the outer form of the
detector: estimate nuisance background, subtract or whiten, detect sources,
refine or fit, and decide admissibility. TrapDetect keeps that form while
specializing it through branch-local calibration, one-chain corridor geometry,
residual spectral objects, and Stage 5 branch admissibility. Its real identity
is therefore a specialized photometric detector whose decisive boundary is
produced by residual-background labor rather than by the raw frame alone or by
the published count alone.

Peak-separation policy remains independent from thresholding throughout both
models. The controlling config key is `peak_min_distance`; the CLI alias
`--peak-distance` writes that same key rather than introducing a second spacing
parameter. The shipped default is the rounded one-fifth spacing rule measured
from manual matched-count frames with at least two ions, using the fitted-chain
`chain_line_projected_spacing_px` statistic rather than an optics model.

## Linear Algebra Ledger

| Object | Definition | Role | Status |
| --- | --- | --- | --- |
| $I_0$ | $I - E_{\eta,\mathrm{global}}$ | base frame after global eta preprocessing; branch-local eta fields may be applied later per Stage 5 variant | `implemented now` |
| $(\hat\mu_j, \hat\sigma_j^2)$ | sigma-clipped tile statistics on tile $T_j$ | Stage 1 background ensemble | `implemented now` |
| $\hat B$ | $L_B(\{\hat\mu_j\})$ | dense background lift from Stage 1 tiles | `implemented now` |
| $\hat V$ | $L_V(\{\hat\sigma_j^2\})$ | dense variance / RMS-like lift | `partially implemented` |
| $\hat\Phi_{\eta}$ | residual PSD / autocorrelation summary | structured-noise operator input | `partially implemented` |
| $P_{\rho}$ | regime-selected median, Gaussian, or identity prefilter on the corrected-image working surface | working-image operator | `implemented now` |
| $J$ | $P_{\rho}(I_c)$ | corrected-image prefiltered working surface | `implemented now` |
| $D_c$ | $(G_{\sigma_s} - G_{\sigma_l}) * P_{\rho}(I_c)$ | corrected-image DoG residual | `implemented now` |
| $K$ | Gaussian template built from $(\hat\sigma_x, \hat\sigma_y)$ or $\hat\sigma_{\mathrm{iso}}$ | Stage 5 response template | `implemented now` |
| $R_{\mathrm{white}}$ | $D_c \star K$ | current matched-response map | `implemented now` |
| $R_{\mathrm{struct}}$ | $(W D_c) \star (W K)$ | PSD-aware structured-noise response map | `planned next` |
| $M_C$ | legacy corridor-style metadata on the full-frame support | preserves result-schema reporting without restricting Stage 4/5 columns | `implemented now` |
| $a(r)$ | $\max_c R(r,c)$ | axial response profile used by `find_peaks` on the full response map | `implemented now` |
| $\hat A_{G,k}$ | $\arg\min_{A \ge 0} \lVert y_k - b_k\mathbf{1} - A t_k \rVert_2^2$ | local Gaussian amplitude model or reconstruction amplitude | `partially implemented` |
| $s_{P,k}$ | $\max\{\sqrt{\Delta D_k / N_{\mathrm{eff},k}} - 1, 0\}$ | candidate-local Poisson score | `implemented now` |
| $\tau_{\mathrm{base},v}$ | fitted artifact-owned score-domain threshold base, falling back to $\tau_{\mathrm{regime}}$ when no valid artifact exists | branch admissibility anchor | `partially implemented` |
| $\mathcal I_v=(\tau_{\mathrm{lo},v},\tau_{\mathrm{hi},v}]$ | learned manual count-boundary interval from accepted/rejected candidate scores | safe threshold interval | `partially implemented` |
| $\Delta\tau_v$ | signed fitted threshold movement clipped to $[-\Delta\tau_v^-, +\Delta\tau_v^+]$ and constrained by $\mathcal I_v$ | branch score-admissibility adjustment | `partially implemented` |
| $\tau_v^*$ | $\operatorname{clamp}_{\mathcal I_v}(\tau_{\mathrm{base},v}+\Delta\tau_v)$, or fallback threshold when no valid interval exists | branch acceptance threshold | `partially implemented` |

## Public Stages and Internal Substages

| Public stage | Internal substages used in this note | Status |
| --- | --- | --- |
| Stage 1. Background & noise regime | Stage 1a tiled sigma-clipped means / variances; Stage 1b dense background and RMS-like lifts | Stage 1a `implemented now`; Stage 1b `implemented now` for background and `partially implemented` for RMS-like lifting |
| Stage 2. Noise power spectrum | Stage 2a dark-tile PSD diagnostics; Stage 2b regime and noise-operator selection | `implemented now` |
| Stage 3. Prefilter | Stage 3a regime-driven prefilter selection; Stage 3b working-image construction | selection `implemented now`; corrected-image construction `implemented now` |
| Stage 4. Corridor & PSF estimation | Stage 4a full-frame DoG support with legacy corridor metadata; Stage 4b provisional peak seeding; Stage 4c PSF estimation and reconciliation | `implemented now` |
| Stage 5. Matched-filter detection | Stage 5a response-map generation; Stage 5b axial candidate extraction and spacing policy; Stage 5c local Gaussian / Poisson rescoring and thresholding | Stage 5a `implemented now` for white-noise response and `planned next` for PSD-aware response; Stage 5b and Stage 5c `implemented now` |
| Stage 6. State & spectral summary | Stage 6a accepted-set state metrics; Stage 6b corridor spectral audit; Stage 6c residual spectral audit for calibration | Stage 6a and Stage 6b `implemented now`; Stage 6c `partially implemented` as a calibration seam |

The stage-by-stage sections below follow this order. Each section states the
quantity produced at that stage, the role that quantity plays in the next part
of the detector, and the places where the present implementation still relies
on calibrated operational choices.

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

The targets $F=1$ and $F=2$ are standard detector-model anchors. The actual
tolerance bands used around them are still calibrated defaults. In the current
code,
those hard bands coexist with an internal soft-evidence layer whose widths are
tempered by the reported single-frame uncertainty rather than by multi-frame
pooling.

These Stage 1 summaries provide the detector's intensity-domain description of
the frame. Stage 2 adds the complementary frequency-domain description needed
to decide whether later filtering and scoring should treat the noise as white,
banded, or directionally structured.

## 2. Noise Power Spectrum Diagnostics

From the darkest tiles, the code computes a Hann-windowed averaged power
spectrum estimate \cite{BlackmanTukey1958,Harris1978}:

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

These are standard PSD-based diagnostics. The cutoffs that define "whiteish"
behavior are still calibrated thresholds.

### Single-Frame Uncertainty

The three NPS diagnostics are also reported with explicit standard errors
derived from the spread across the within-frame dark-tile ensemble. Each dark
tile yields an independent realization of whiteness, log spectral flatness, and
log directional anisotropy; the reported standard errors use a MAD-based
robust location standard error \cite{BeersFlynnGebhardt1990} on those
samples. These errors are aggregated into a downstream
`measurement_precision_score` that softens, but does not override, the hard
regime label.

Taken together, the Stage 1 and Stage 2 diagnostics describe both the scale
and the structure of the background noise. Stage 3 converts that diagnostic
picture into an explicit regime label and uses it to choose how the later
detector branches should interpret the image.

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
formal likelihood-ratio test. The targets are standard model anchors; the
relative tolerances are calibrated. The public label remains a hard compatibility
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

Given the detector-regime evidence above, the prefilter stage chooses one of
three actions:

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

This control-limit form is a standard binomial-tail approximation; for the
underlying binomial-proportion setting and the limits of simple
normal-approximation interval logic, see
\cite{Wilson1927,BrownCaiDasGupta2001}. The choices of $k$, $z$, kernel size,
and Gaussian blur width are calibrated engineering defaults.

The output of this stage is a regime-conditioned working image that suppresses
the most disruptive small-scale artifacts without discarding ion-scale
structure. That working image is then passed to the spatial localization stages.

## 5. Public Stage 4a: Full-Frame Bandpass Isolation

Using that working image, the first internal half of public Stage 4 operates on
the full frame. The current code forms a Difference-of-Gaussians bandpass image
from the background-corrected working image without a central ROI crop or a
column-band restriction:

$$
I_c = I_0 - \hat B,
\qquad
I_{\rho} = P_{\rho} I_c,
\qquad
D_c = (G_{\sigma_s} - G_{\sigma_l}) * I_{\rho}.
$$

Here $\sigma_s$ preserves ion-scale structure and $\sigma_l$ suppresses slow
background variation. In the current code path, Stage 3 constructs the dense
background-corrected working image $I_c$ from the Stage 1 tile lifts and routes
that corrected image into the DoG bandpass. When branch-local eta runtime
fields are enabled, Stage 5 variants rebuild this same corrected-image view
after subtracting the variant-specific eta surface.

This DoG construction is a common practical bandpass choice. The actual scales
remain calibrated to the current image family \cite{MarrHildreth1980}.

### Full-Frame Support and Legacy Metadata

Legacy corridor metadata are still emitted for compatibility with the existing
result schema. In the default runtime, PSF estimation and Stage 5 candidate
extraction are not restricted to a narrow column band, so provisional peaks for
PSF support are drawn from the full DoG surface. When explicit ROI mode is
enabled, the legacy search-window and corridor-width restrictions are applied
again.

## 6. Public Stage 4b: PSF Estimation

The matched filter requires a PSF estimate, and the current code resolves that
bootstrap dependency directly on the full DoG image in two steps:

1. detect provisional full-frame peaks on the DoG image
2. estimate the PSF from local patches around those provisional peaks

Before the local-width and Fourier-envelope fits, the code forms a provisional
seed set on the full DoG image:

$$
\mathcal{P}_{\mathrm{seed}}
=
\operatorname{peak\_local\_max}(D; d_{\min}, \tau_{\mathrm{seed}}, n_{\max}),
$$

where $d_{\min}$ is controlled by `peak_min_distance` and
$\tau_{\mathrm{seed}}$ is the Stage 4 absolute threshold derived from
`peak_threshold_sigma`. This seed spacing floor is independent of the later
count-decision threshold. The default $d_{\min}=7$ px is the rounded one-fifth
of the manual matched-count projected ion spacing measured on frames with at
least two ions; matched 0/1-ion frames are excluded from that geometry statistic.
The CLI alias `--peak-distance` writes the same `peak_min_distance` config key
rather than a second spacing control.

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

These are practical moment estimators for a localized positive source, though
they are not exact maximum-likelihood estimates; the pixelated-source
localization literature makes clear both why such estimators are useful and
where their efficiency limits sit relative to likelihood-based methods and
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

The local-moment and Fourier-envelope models are practical approximate
estimators. The consistency window, fit region, minimum point count, and
fallback anisotropy ratio are calibrated heuristics.

Stage 4 therefore produces two key geometric outputs: a full-frame bandpass
support together with compatibility metadata, and a PSF model for the expected
ion image. Stage 5 uses those outputs to construct response maps, seed
candidate rows, and convert local evidence into a count decision.

## 7. Public Stage 5a: Response-Map Generation and Candidate Seeding

With the Stage 4 full-frame support fixed and PSF widths $\sigma_x$ and $\sigma_y$ available, the
code constructs an anisotropic
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

The current response map is computed as FFT-based cross-correlation

$$
R_{\mathrm{white}} = D \star K.
$$

For additive white noise and a known template, the matched filter is the
classical optimal linear detector. In practice, the code uses this logic under
the regime checks above and reports the diagnostics so the user can judge when
the assumptions are strained \cite{Turin1960}.

The planned next structured-noise branch is

$$
R_{\mathrm{struct}} = (W D_c) \star (W K),
$$

but that PSD-aware response map is not yet the controlling Stage 5 path.

### Axial Candidate Generation

The runtime keeps the full matched-response map. Legacy corridor metadata may be
refreshed for reporting, but candidate generation is not restricted to a column
band. The code converts the 2-D response into a 1-D axial profile by taking the
strongest matched response on each row,

$$
a(r) = \max_c R_{\mathrm{white}}(r,c).
$$

The code then applies `scipy.signal.find_peaks` to $a(r)$ subject to a minimum
distance rule, a height rule, and a prominence rule. The controlling spacing
policy is still `peak_min_distance`, with the effective 1-D distance widened by
the current PSF width estimate when needed. The default spacing floor is anchored
to one fifth of the manual matched-count projected ion spacing, excluding 0/1-ion
matched frames from the geometry estimate. This is a candidate-extraction policy,
not the count threshold itself.

This stage is a candidate generator, not the final count decision. The peak
height/prominence/distance settings are calibrated heuristics that seed the
later auditable threshold rule.

The result is a candidate set rather than a final accepted set. Each candidate
then enters a local refinement stage that recomputes position, width, and
branch-specific evidence on the patch itself.

## 8. Public Stage 5b: Local Refinement and Candidate Scoring

For each candidate row peak, the code refines the strongest local column on the
full response surface,
extracts a local patch, and computes:

- sub-pixel centroid
- local widths
- integrated signal
- local background mean and noise scale
- matched-filter response and matched SNR

If $\sigma_R$ is the estimated background standard deviation of the matched
response, then the matched SNR is

$$
\operatorname{SNR}_{\mathrm{matched}} = \frac{R_{\mathrm{white}}(r_k, c_k)}{\hat\sigma_R}.
$$

The current primary response-noise estimate is the dark-tile propagated matched
response sigma. If $\{B_m\}_{m=1}^M$ are the Stage 1 dark tiles after the same
prefilter and DoG chain, then the primary estimate is

$$
\hat\sigma_{R,\mathrm{dark}} = \operatorname{robust\_std}\!\left(\bigcup_{m=1}^{M} (B_m \star K)\right).
$$

The runtime uses

$$
\hat\sigma_R =
\begin{cases}
\hat\sigma_{R,\mathrm{dark}}, & \text{if the dark-tile propagated estimate is finite and positive},\\
\hat\sigma_{R,\mathrm{weak}}, & \text{otherwise},
\end{cases}
$$

where $\hat\sigma_{R,\mathrm{weak}}$ is the weak-band response fallback derived
from low-response regions of the current ROI. The dark-tile rule is therefore
the primary operational estimate; the weak-band quantile path is fallback only.

For the Poisson variants, the candidate-local score is instead

$$
s_{P,k} = \max\left\{\sqrt{\frac{\Delta D_k}{N_{\mathrm{eff},k}}} - 1,\ 0\right\},
$$

so public Stage 5b already contains two local score families even though the
response map itself is still the Gaussian matched-filter map above.

Stage 5b therefore supplies the local evidence for each candidate, but it does
not yet publish the visible-ion count. That final step occurs only after the
branch scores are compared to a score-domain threshold and any branch-local
signed artifact movement.

## 9. Public Stage 5c: Count Decision and Margin Diagnostics

The final visible-ion count is the cardinality of the accepted candidate set.
The fallback acceptance rule is explicit, and its threshold is already
regime-aware before any manual-calibrated score-admissibility artifact is
applied. Let

$$
\tau_0 = \texttt{min\_accepted\_matched\_snr},
\qquad
\tau_{\mathrm{artifact}} = \texttt{compressed\_artifact\_min\_accepted\_matched\_snr},
\qquad
\tau_{\eta\text{-artifact}} = \texttt{eta\_corrected\_compressed\_artifact\_min\_accepted\_matched\_snr}.
$$

Then the implemented regime floor is

$$
\tau_{\mathrm{regime}} =
\begin{cases}
\tau_0, & \text{if } \ell \neq \texttt{compressed\_or\_artifact},\\
\max(\tau_0, \tau_{\mathrm{artifact}}), & \text{if } \ell = \texttt{compressed\_or\_artifact} \text{ and eta is not applied},\\
\max(\tau_0, \tau_{\mathrm{artifact}}, \tau_{\eta\text{-artifact}}), & \text{if } \ell = \texttt{compressed\_or\_artifact} \text{ and eta is applied}.
\end{cases}
$$

Without branch-local manual calibration, or when a calibrated artifact is
missing or invalid, the branch decision rule is

$$
\\text{accept candidate on branch } v \iff s_{v,k} \ge \\tau_{\mathrm{regime}},
$$

In branch-only manual calibration, the score-admissibility artifact owns the
threshold base and its allowed signed movement. The runtime regime threshold is
then a fallback anchor, not the calibrated truth. For each branch $v$, let the
current branch residual power summary be

$$
R_v^{\ast}
=
\frac{P_{\mathrm{peak},v}^{\ast}}{\max(P_{\mathrm{mean},v}^{\ast}, \varepsilon)},
\qquad
L_v^{\ast} = \log R_v^{\ast},
$$

and let the branch manual references include

$$
{}\tilde L_v = \operatorname{median}_{i\in M_v} L_{v,i},
\qquad
{}\tau_{\mathrm{base},v},
\qquad
\mathcal I_v = (\tau_{\mathrm{lo},v}, \tau_{\mathrm{hi},v}],
$$

where $\tau_{\mathrm{base},v}$ is the artifact-owned threshold base in the
correct score domain. The interval $\mathcal I_v$ is the manual count-boundary
constraint: $\tau_{\mathrm{lo},v}$ is the strongest score that should remain
rejected, and $\tau_{\mathrm{hi},v}$ is the weakest score that should remain
accepted. When both sides are finite, a valid threshold must satisfy
$\tau_{\mathrm{lo},v} < \tau \le \tau_{\mathrm{hi},v}$.

The accepted margin-to-threshold measurements $m_{v,i}$ remain useful audit
statistics, but the branch-local admissibility movement is now signed. The
resolved mathematical object is the per-row admissible threshold interval

$$
\mathcal I_i = (\tau_{\mathrm{lo},i}, \tau_{\mathrm{hi},i}],
$$

induced by the ranked candidate scores for row $i$. The calibrated threshold
law is then fit in score space as

$$
{}\tau_i = \tau_{\mathrm{base},v} + g_{\theta_v}(z_i),
\qquad
z_i = \bigl(L_i^{\ast}, \tilde L_v, \rho_i^{\ast}\bigr),
$$

with the fitting target that $\tau_i$ lies inside $\mathcal I_i$ rather than
matching a fabricated midpoint or a median threshold summary. The signed
movement reported at runtime is the derived quantity

$$
\Delta\tau_v = \operatorname{clip}
\left(
{}\tau_i - \tau_{\mathrm{base},v},
-\Delta\tau_v^-,
\Delta\tau_v^+
\right),
$$

where $\rho_i^{\ast}$ denotes any available current PSD-adequacy evidence, and
$\Delta\tau_v^-$ and $\Delta\tau_v^+$ are artifact-owned lower and upper
movement caps. Positive movement raises the threshold to repair overcounts;
negative movement lowers the threshold to repair undercounts.

The calibrated branch decision rule is then

$$
\\text{accept candidate on branch } v \iff s_{v,k} \ge \\tau_v^{\ast},
\qquad
\\tau_v^{\ast}
=
\operatorname{clamp}_{\mathcal I_v}
\left(\tau_{\mathrm{base},v} + \Delta\tau_v\right),
$$

with the convention that missing or empty interval evidence falls back to the
score-domain threshold and conservative movement caps. This preserves the
public Stage 5 interface: the branch score family is unchanged, the threshold
remains explicit, and the second correction is not a shared post hoc penalty.
Gaussian and Poisson variants share this signed admissibility form; what differs
across variants is the branch score $s_{v,k}$, the score domain, and the
branch-local calibration artifact.

At the current implementation frontier, the runtime signed-threshold evaluator
is in place and the artifact schema can carry fitted interval data, but
canonical no-artifact runs still fall back to $\tau_{\mathrm{regime}}$. A bare
`analyze_array()` mismatch with no score reference applied is therefore
evidence about the fallback detector path, not yet evidence that the fitted
score-admissibility law itself is failing.

In that sense the Stage 5 signed threshold movement is the admissibility side
of the same residual-background model. Upstream, the detector tries to win a
corrected image by subtracting or mediating structured nuisance content.
Downstream, the detector lets the artifact move the count boundary only inside
the manual-count interval justified by accepted and rejected candidate scores.
This is why the branch-local movement belongs to the same photometry-inspired
organization as corrected-image construction while still remaining more
specialized than a standard pipeline. The admissibility law is
branch-conditioned, score-domain aware, and coupled to the residual spectral
object rather than derived from a generic global background model alone.

Within the selected noise-regime branch, Stage 5 may still apply an internal
accepted-set correction when the accepted many do not cohere as a stable one.
This includes accepted-set negation to zero or reduction to a smaller subset.
The public contract does not change: the reported count remains the cardinality
of the final accepted set after those branch-internal consistency checks.

The important scientific feature of the implementation is not that
$\tau_0 = 5.6$ is derived from first principles, but that the count decision is
auditable through the reported fallback floor, artifact threshold base, signed
threshold movement, manual-count interval, and reported margins.

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

Only after this acceptance step does the detector treat the surviving set as a
frame-level state and summarize it with state-level metrics. In that sense,
Stage 5 is the point at which image-local evidence becomes a published count
under an explicit decision rule.

## 10. Mode Tensor Contract For Generalized Stage 5

The canonical public result still has four Stage 5 variants:

$$
\mathcal V = \{\text{anisotropic\_gaussian},\text{symmetric\_gaussian},\text{anisotropic\_poisson},\text{symmetric\_poisson}\}.
$$

A generalized detector path adds a nested mode axis under each public variant
rather than adding new top-level variant keys. For each public variant
$v \in \mathcal V$, let $\mathcal M_v$ be the finite set of modes evaluated
under that variant. A mode is the tuple

$$
m = (v, O_m, q_m, C_m, p_m),
$$

where $O_m$ is the response operator, $q_m$ is the score selector, $C_m$ is the
calibration policy, and $p_m$ is the provenance record. The canonical mode is
the sole selected-count mode in the implemented runtime; nested experimental
modes are ledger-only unless a future selected-mode path passes explicit
provenance and calibration checks.

The corrected image for a mode is

$$
I_{c,m} = P_\rho\bigl(I - E_{\eta,m} - \hat B\bigr),
$$

with $E_{\eta,m}=E_{\eta,v}$ for branch-local count-legibility modes and
$E_{\eta,m}=E_{\eta,\mathrm{shared}}$ otherwise. The mode response map is

$$
R_m = O_m(I_{c,m}, h_v).
$$

For the canonical white matched response,

$$
R_m = D_{c,m} \star h_v.
$$

For a future structured-noise response, the same interface admits

$$
R_m = (W_m D_{c,m}) \star (W_m h_v).
$$

Candidate generation and acceptance remain distinct. Stage 5a produces a
candidate support from $R_m$; Stage 5b measures candidates; Stage 5c decides
admissibility. The candidate measurement tensor is

$$
X_{m,k,q},
$$

where $m$ indexes mode, $k$ indexes candidate, and $q$ indexes a named channel
such as matched response, Gaussian matched SNR, Poisson deviance score,
integrated SNR, candidate-support summed-excess SNR, local robust support SNR,
candidate-support mean-excess SNR, template-support excess density, template
normalized correlation, geometry support, or invalid-candidate status. Support
score channels use source-masked full-frame or full-ROI background location and
RMS estimates when valid; local annulus statistics remain emitted as diagnostics
and as the fallback when the source-masked RMS is unavailable.

Each mode chooses a scalar decision score by a selector vector $a_m$:

$$
s_{m,k} = a_m^T X_{m,k,:}.
$$

The accepted and rejected candidate sets are

$$
A_m = \{k : \operatorname{valid}_{m,k} \land s_{m,k} \ge \tau_m^*\},
$$

$$
B_m = P_m \setminus A_m.
$$

The threshold remains explicit:

$$
τ_m^* = \tau_{\mathrm{regime},m} + \Delta \tau_m.
$$

For canonical matched-score modes, existing branch score-admissibility artifacts
may supply $\Delta \tau_m$ only when the artifact score basis matches the mode
score basis. For experimental score modes, $\Delta \tau_m=0$ until the manual
detector update pipeline emits a mode-keyed calibration artifact with matching
`mode_id`, parent variant, and score basis.

Mode-local reconstruction is

$$
S_m(r,c)=\sum_{k\in A_m} A_{m,k}\,h_v(r-r_{m,k},c-c_{m,k}),
$$

and the mode residual is

$$
r_m(r,c)=I(r,c)-\hat B(r,c)-S_m(r,c).
$$

Manual calibration artifacts are functions of the manual-match residual family
$\{r_{m,i}\}_{i\in M_m}$ and record the optimized or manual detector
initialization config used to produce that family.

Dialectically, the visible count is the immediate master appearance: a scalar
claims to summarize the frame. The mode-indexed operator stack is the mediating
labor: corrected image, response map, candidate tensor, score selector,
residual reconstruction, and threshold motion. The raw frame and candidate
field are the negative object: they resist immediate counting through weak
extras, residual concentration, and branch disagreement. The public count is
therefore a mediated measure, not direct score-switch inference.

By default, Stage 6 selects the canonical mode of the selected public variant
and reports $N_{\mathrm{visible}}=|A_m|$. Nested experimental mode ledgers may
be emitted for audit and calibration, but they do not alter the selected count
unless an explicit experimental selected-mode config passes provenance and
calibration checks.

## 11. State-Level Metrics

For accepted ions with matched SNR values $s_1, \dots, s_N$, the code reports

$$
\rho_{\mathrm{rss}} = \sqrt{\sum_{k=1}^{N} s_k^2},
$$

along with the weakest-ion SNR, the mean ion SNR, and a spatial spacing metric
derived from the median separation between detected rows.

The root-sum-square summary is an engineering aggregate. It is not a posterior
probability or a sufficient statistic for every downstream task, but it is a
stable scalar summary of per-frame signal strength.

The code also fits a permanent image-local line-geometry statistic to the
accepted centroids.  For accepted centroid coordinates

$$
x_i = \begin{bmatrix} r_i \\ c_i \end{bmatrix},\qquad
X = \begin{bmatrix} x_1^T \\ \vdots \\ x_N^T \end{bmatrix},
$$

the detector drops nonfinite centroids, computes

$$
\mu = \frac{1}{N}\sum_{i=1}^{N} x_i,\qquad
X_c = X - \mathbf{1}\mu^T,
$$

and obtains the line direction from the centered SVD

$$
X_c = A\,\operatorname{diag}(\sigma_1,\sigma_2)\,V^T,
\qquad \sigma_1\ge\sigma_2\ge0,
\qquad u = V_{:,1}.
$$

The reported line is not slope-intercept form. It is

$$
\mathcal{L}=\{\mu + t u:t\in\mathbb{R}\},
$$

which solves the orthogonal total-least-squares problem

$$
\min_{\mu,\,u:\|u\|_2=1}
\sum_{i=1}^{N}\left\|(I-u u^T)(x_i-\mu)\right\|_2^2.
$$

With $n=[-u_c,u_r]^T$, the scalar diagnostics are

$$
t_i=u^T(x_i-\mu),\qquad
\rho_i=|n^T(x_i-\mu)|,
$$

the projected median nearest-neighbor spacing in sorted $t_i$, the projected
span, the RMS orthogonal residual, and

$$
\mathrm{linearity}=\frac{\sigma_1^2}{\max(\sigma_1^2+\sigma_2^2,\varepsilon)}.
$$

This statistic is a Stage 6 accepted-set summary. It does not alter Stage 5
variant selection, accepted/rejected partitioning, or the canonical detector-
update calibration surfaces.

At this point the detector has completed its single-frame task. The remaining
sections describe how those per-frame outputs are carried into a downstream
temporal interpretation, first through within-run epoch construction and then
through bundle-level lifetime summaries.

## 11. Spectral Chain Metric

The matched-filter response over the full Stage 5 support is Fourier
transformed and its
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

The batch layer (`run_npz_batch.py`) begins from the per-frame outputs above and
tracks how long the camera reports a given
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
is the camera-defined bright-versus-dark fluorescence level under the
acquisition conditions of the experiment: a Ba$^+$ ion can remain trapped while
its fluorescence drops during shelving and later returns when the metastable
state decays \cite{Leibfried2003}. The current contract is
therefore a contract for **camera-observed metastable-state epochs**: a strict
visible-count decrease is surfaced for review, but it is not by itself a claim
that an ion left the trap
\cite{Leibfried2003,Madej1990,Gurell2007,Auchter2014,Mohanty2015}.

The same distinction is explicit in the Ba$^+$ reshelving analysis used to
infer metastable-state branching. If $P_{\mathrm{sh}}$ is the initial shelving
probability, $P_{\mathrm{dec}}$ the decay probability during the wait interval,
$P_{\mathrm{re-sh}}$ the reshelving probability, $P_{\mathrm{seq-dec}}$ the
probability of a sequential $5D_{5/2}\to 5D_{3/2}\to 6S_{1/2}$ decay during
the wait, and $q$ the branching fraction from $5D_{5/2}$ to $6S_{1/2}$, then
the detected dark-state probability is

$$
P_{\mathrm{dark}}
=
P_{\mathrm{sh}}(1-P_{\mathrm{dec}})
+
P_{\mathrm{sh}} P_{\mathrm{dec}} q P_{\mathrm{re-sh}}
+
P_{\mathrm{sh}} P_{\mathrm{dec}} (1-q) P_{\mathrm{seq-dec}} P_{\mathrm{re-sh}},
$$

so

$$
q
=
\frac{
P_{\mathrm{dark}} - P_{\mathrm{sh}}\left[1-P_{\mathrm{dec}}\left(1-P_{\mathrm{re-sh}}P_{\mathrm{seq-dec}}\right)\right]
}{
P_{\mathrm{sh}} P_{\mathrm{dec}} P_{\mathrm{re-sh}} (1-P_{\mathrm{seq-dec}})
}.
$$

Even for a single ion, a dark-versus-bright camera outcome already mixes
shelving, decay, branching, and reshelving efficiencies. That is why the batch
epoch contract treats visible-count changes as fluorescence-state evidence
first, not as direct occupancy truth \cite{Auchter2014}.

This distinction matters for the statistical role of the epoch model. The epoch
layer does not replace the single-frame detector; it reorganizes per-frame
visible-count outputs into contiguous state segments that can later be pooled,
screened, and interpreted against the experimental lifetime literature.

For multi-ion continuous quantum-jump records, the interval model used in later
Ba$^+$ lifetime work writes the state-$k$ dwell rate as

$$
\tau_k^{-1} = k\tau_{D5/2}^{-1} + (n-k)\tau_S^{-1},
$$

where $k$ of $n$ monitored ions are shelved, $\tau_{D5/2}$ is the metastable
state lifetime, and $\tau_S$ is the shelving time. The same model writes the
observed lifetime on the rate axis as

$$
\tau_{D5/2}^{-1} = \tau_{D5/2,\mathrm{nat}}^{-1} + \sum_i \gamma_i,
$$

so pressure, off-resonant deshelving, blackbody stimulation, and related
apparatus terms enter additively as decay-rate corrections rather than as
hidden changes to ion occupancy. This is the reference model behind the
`paper_k_interval_least_squares` mode introduced below \cite{Dijck2018}.

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

Once the epoch layer has been built for each run, the batch layer forms a
single pooled mean transition lifetime for reporting. This step moves from
within-run state segmentation to across-run lifetime aggregation while still
preserving the rule that decrease events are interpreted conservatively.

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

For supported bundles, `extract_npz_json.py --summary-only` now promotes that
batch summary into a report surface. The emitted `batch_summary.jsonl` contains
typed lifetime-report rows for each bundle measurement mode together with
comparisons, selection diagnostics, histogram payloads, and k-state fit rows,
and the extractor writes companion `lifetime_report.json` and
`lifetime_report.md` artifacts beside the JSONL summary.

The result of this stage is still a descriptive transition-time summary rather
than a final physics estimate. The next section adds the explicit uncertainty
model and measurement-mode distinctions that are needed before the pooled
transition statistics can be discussed as lifetime estimates.

### Lifetime Precision From Epoch Statistics

For bundle inputs, the downstream helper script `calculate_lifetime_precision.py`
now defaults to an epoch-statistics estimate built directly from the stored
per-run epoch rows. The default bundle mode, `epoch_cumulative_nonfinal`, uses
the observed cumulative transition times over all finite non-final epochs within
each run as the lifetime samples and keeps the calculation in double precision
throughout. For extracted JSONL or manifest inputs, or when the user passes
`--measurement-mode batch_transition`, the helper falls back to the emitted
`batch_transition_lifetime.mean_real_time_lifetime_s` summary field. Five
additional bundle-only modes expose the reference-paper structures explicitly:
`paper_nonfinal_interval` pools the finite non-final interval durations in the
style of the paper interval histograms, `paper_weighted_brightening` keeps only
monotone `+1` bright-transition prefixes and averages their cumulative
transition times, `paper_segmented_brightening` keeps contiguous `+1`
brightening chains even after later resets, `paper_segmented_darkening` does the
same for contiguous `-1` darkening chains, and
`paper_k_interval_least_squares` groups one-step intervals by dark-count state
and fits the relation $\lambda_k = k R_{\downarrow} + (n-k) R_{\uparrow}$ on the
rate axis to recover $\tau_D$ and $\tau_S$ \cite{Dijck2018}.

If one run contributes finite non-final epoch durations
$e_{r,1}, e_{r,2}, \dots, e_{r,m_r}$, then the interval-style modes pool

$$
x_{r,j} = e_{r,j},
$$

while the cumulative modes pool

$$
c_{r,j} = \sum_{\ell=1}^{j} e_{r,\ell}.
$$

For adjacent retained epochs with visible-ion counts $n_{r,j}$, define the
count step

$$
\Delta n_{r,j} = n_{r,j+1} - n_{r,j}.
$$

`paper_weighted_brightening` keeps only the initial block with
$\Delta n_{r,j} = +1$ and pools the corresponding cumulative samples $c_{r,j}$;
`paper_segmented_brightening` pools those same cumulative samples over every
maximal contiguous $\Delta n_{r,j} = +1$ chain; and
`paper_segmented_darkening` does the analogous construction for maximal
$\Delta n_{r,j} = -1$ chains.

For the k-state least-squares mode, the source-paper rate model is

$$
\lambda_k = \tau_k^{-1} = k R_{\downarrow} + (n-k) R_{\uparrow}
= k\tau_D^{-1} + (n-k)\tau_S^{-1}.
$$

The 2018 Appendix A averaging-window correction for the observed state lifetime
$\tau_k^*(\Delta t)$ is

$$
\tau_k^*(\Delta t)=
\frac{
-\exp\!\left(\frac{\Delta t}{\tau_{k-1}}\right)p_{k\uparrow\downarrow}\tau_{k+1}
-\exp\!\left(\frac{\Delta t}{\tau_{k+1}}\right)p_{k\downarrow\uparrow}\tau_{k-1}
+\exp\!\left(\frac{\Delta t}{\tau_{k+1}}+\frac{\Delta t}{\tau_{k-1}}\right)
\left[\tau_k+p_{k\uparrow\downarrow}\tau_{k+1}+p_{k\downarrow\uparrow}\tau_{k-1}
-\Delta t\left(p_{k\uparrow\downarrow}+p_{k\downarrow\uparrow}-1\right)\right]
}{
\exp\!\left(\frac{\Delta t}{\tau_{k-1}}\right)p_{k\uparrow\downarrow}
+\exp\!\left(\frac{\Delta t}{\tau_{k+1}}\right)p_{k\downarrow\uparrow}
-\exp\!\left(\frac{\Delta t}{\tau_{k+1}}+\frac{\Delta t}{\tau_{k-1}}\right)
\left(p_{k\uparrow\downarrow}+p_{k\downarrow\uparrow}-1\right)
}.
$$

with

$$
p_{k\uparrow\downarrow} = p_{k\uparrow}p_{(k+1)\downarrow},
\qquad
p_{k\downarrow\uparrow} = p_{k\downarrow}p_{(k-1)\uparrow},
$$

$$
p_{k\downarrow} = \frac{kR_{\downarrow}}{kR_{\downarrow} + (n-k)R_{\uparrow}},
\qquad
p_{k\uparrow} = \frac{(n-k)R_{\uparrow}}{kR_{\downarrow} + (n-k)R_{\uparrow}}.
$$

The same appendix applies a finite-record correction on the rate axis before
solving for $\tau_D$ and $\tau_S$:

$$
\lambda_{k,\mathrm{corr}} = \left(\tau_k^*\right)^{-1} - T_{\mathrm{unint}}^{-1},
$$

where $T_{\mathrm{unint}}$ is the mean uninterrupted record duration for the
data set. This paper-derived correction layer is the reference model for the
k-state method; the simpler interval and cumulative modes above remain direct
summaries of the stored epoch durations.

The uncertainty calculation therefore sits one layer downstream from both the
single-frame detector and the epoch constructor. First the detector produces
per-frame visible-count and confidence outputs, then the epoch logic builds
camera-observed state segments, then the bundle layer forms transition-time
samples, and only then does the precision helper attach a statistical and
systematic uncertainty budget to the chosen lifetime summary.

With $N = \texttt{n_epochs_real_time_considered}$ for the selected measurement
mode and user-supplied absolute systematic terms $u_i$ in seconds, it reports

The mediation chain for that downstream use is now explicit: the detector in
`analyze_ions_fft.py` feeds per-run reduction in `analyze_batch.py`, the
multi-run orchestrator `run_npz_batch.py` publishes the bundle, and only then
do `extract_npz_json.py` and `calculate_lifetime_precision.py` consume the
selected-summary batch contract and the stored per-run epoch rows. The preserved
v8 variant payload is available for audit and review, but this pass
intentionally does not let disagreement between variants alter the lifetime
estimate.

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

## Owning Code Surfaces

The sections above describe the scientific path and the downstream reporting
contract. The table below records where those stages currently live in the code
so later detector revisions can land in the controlling abstractions rather
than in downstream summaries or batch wrappers.

| Internal surface | Current owners | Current contract | Next implementation target |
| --- | --- | --- | --- |
| Stage 1a tile statistics | `tile_background_stats()`, `stage_background()` | sigma-clipped tile means / variances, dim-tile ensemble, dark tiles | keep public outputs stable while exposing dense lifts explicitly |
| Stage 1b dense background lift | `background_surface_from_tiles()`, `reconstruct_frame_components()` | dense background mediates the default Stage 3-5 working image; dense RMS-like lift exists explicitly but is not yet the controlling response/noise operator | promote dense RMS-like lifts into explicit upstream response/noise operators |
| Stage 2a / 2b PSD and regime routing | `nps_diagnostics()`, `classify_noise_regime()` | dark-tile PSD summaries and regime evidence drive prefilter and branch choice | add explicit noise-operator selection without changing public regime labels |
| Stage 3 working image | `choose_prefilter()`, `apply_prefilter()`, `_variant_detection_inputs()` | prefilter is explicit; corrected-image routing is the default Stage 3-5 basis, with variant-local eta rebuilds when enabled | keep corrected-image routing while separating white-noise and PSD-aware operator paths |
| Stage 4a full-frame DoG support | `compute_bandpass()`, `detect_chain_corridor()` | full-frame DoG support with compatibility metadata on the current working image | keep the full-frame policy while feeding corrected-image residuals |
| Stage 4b seed and PSF estimation | `preliminary_peak_candidates()`, `estimate_psf()`, `estimate_psf_fft()` | provisional seeds and PSF reconciliation are already explicit | keep seed spacing policy independent from thresholding |
| Stage 5a response map | `matched_filter_response()`, `_shape_variant_detection()` | Gaussian matched-response map is controlling | split white-noise response from PSD-aware response generation |
| Stage 5b candidate extraction and scoring | `detect_ion_rows()`, `refine_detections()`, `_background_tile_response_noise_std()`, `_apply_detection_noise_model()` | 1-D axial extraction, dark-tile-primary Gaussian SNR, candidate-local Poisson score | preserve score families while making the response/noise operators explicit |
| Stage 5c thresholding and branch lifting | `_effective_detection_threshold()`, `_score_admissibility_threshold_info()`, `filter_detections()`, `stage_detection()` | regime floor and branch residual-power lift determine acceptance | keep the public count contract while separating response generation from local likelihood refinement |
| Stage 6 summaries and calibration seam | `state_metrics()`, `spectral_chain_metrics()`, `reconstruct_frame_components()`, `_estimate_residual_spectral_object()` | accepted-set summaries and residual spectral audits already exist | reuse residual spectral objects to support structured-noise operators upstream |

## Calibration Table

The current defaults mix true model anchors, error-budget controls, and
quantities whose real essence is not "calibration" at all but frame-mediation
state. The contract is clearer when those rows are split into the three buckets
below.

### First-Principles Anchors

These rows are fixed model anchors, hard compatibility gates, or experiment
constraints that do not need optical priors.

| Parameter | Default | Role | Contract reading |
| --- | ---: | --- | --- |
| `sigma_clip` | `3` | outlier rejection radius | standard robust-statistics choice |
| `eta_mode` | `"off"` / `"manual_calibrated"` | off or branch-only calibrated mode | constrained public contract |
| `enable_search_roi` | `False` | explicit opt-in for legacy Stage 4/5 ROI and corridor restriction | compatibility gate, not a canonical tuning surface |
| `enable_gaussian_warning_count_corrections` | `False` | opt-in legacy Gaussian post-threshold count-repair rules retained only for compatibility-oriented studies | legacy compatibility gate, not a canonical tuning surface |
| `max_ions` | `20` | hard experimental cap | experiment constraint |
| `fixed_point_max_iterations` | `3` | canonical solver cap for the detector-update outer loop | solver-policy default, not a detector surface |
| `fixed_point_reference_tolerance` | `1e-6` | absolute stability tolerance used when comparing branch reference summaries between successive detector-update iterations | solver-policy default, not a detector surface |

### α/q-Derived Controls

These rows are best understood as error-budget or quantile controls. The current
numeric defaults remain the shipped implementation values, but their proper
scientific interpretation is "derive from explicit $\alpha$ or $q$ targets"
rather than "treat as eternal magic constants."

| Parameter | Default | Role | Contract reading |
| --- | ---: | --- | --- |
| `background_quantile` | `0.35` | dim-tile subset for mean-variance fit | quantile control `q_bg`, not an optical prior |
| `fano_poisson_tol` | `0.5` | relative band around Poisson target | should be tied to a Poisson-family error budget around $F = 1$ |
| `fano_emccd_tol` | `0.5` | relative band around EMCCD target | should be tied to an EMCCD-family error budget around $F = 2$ |
| `kurtosis_max` | `10` | heavy-tail cutoff for Gaussian-like assumptions | tail-probability safeguard |
| `whiteness_lo`, `whiteness_hi` | `0.5`, `2.0` | acceptable whiteness band | should be a null interval for white PSD behavior |
| `hot_pixel_sigma` | `6` | hot-pixel exceedance definition | per-pixel tail threshold |
| `hot_pixel_fraction_floor` | `0.001` | minimum allowed hot-pixel limit | floor on the hot-pixel exceedance budget |
| `hot_pixel_tail_zscore` | `5` | width of exceedance control limit | familywise or binomial-tail safeguard |
| `peak_threshold_sigma` | `1.25` | candidate seed threshold | seed-stage exceedance control |
| `peak_prominence_sigma` | `1.2` | candidate seed prominence | seed-stage prominence control |
| `eta_max_abs_correction` | `1.5` | runtime cap for the branch structured count-legibility projection | runtime correction safeguard that should be justified by an explicit confidence budget |
| `eta_runtime_min_coherence` | `1.0` | minimum per-pixel coherence ratio $\lvert\bar\eta_v\rvert / \mathrm{SE}_v$ retained in the branch count-legibility runtime mask when branch variance estimates are available | coherence-significance gate |
| `min_accepted_matched_snr` | `5.6` | fallback Stage 5 threshold $\tau_0$ before any valid branch-local score-admissibility artifact is applied | base false-alarm control |
| `compressed_artifact_min_accepted_matched_snr` | `6.0` | stronger Stage 5 floor used when `regime_label == "compressed_or_artifact"` | regime-conditional false-alarm control |
| `eta_corrected_compressed_artifact_min_accepted_matched_snr` | `8.0` | stronger Stage 5 floor used when compressed-artifact routing and eta correction are both active | regime-and-correction conditional false-alarm control |

### Frame-Mediation State

These rows are better understood as the detector's frame-mediation state: the
internal operator-construction scales, branch artifacts, and derived detector
state used to build and audit the working image. Their essence is not "public
academic tuning knob" but "estimate from the frame, carry as branch state, or
hide as an implementation detail."

| Parameter | Default | Role | Contract reading |
| --- | ---: | --- | --- |
| `bg_block_shape` | `(64, 64)` | tile size for robust local background statistics | internal construction scale for the dense nuisance field |
| `dark_tile_count` | `6` | number of tiles used for NPS | internal sample-count choice for PSD estimation |
| `prefilter_gaussian_sigma` | `0.8 px` | mild denoising blur | internal prefilter construction scale |
| `median_size` | `3` | impulsive-noise suppression | internal prefilter construction scale |
| `search_row_fraction`, `search_col_fraction` | `(0.15, 0.9)`, `(0.3, 0.7)` | legacy search-window bounds used only when `enable_search_roi = True` | legacy frame-restriction state, not a canonical surface |
| `dog_small_sigma`, `dog_large_sigma` | `1.2 px`, `12 px` | ion-scale bandpass | internal operator-construction scales |
| `search_half_width` | `30 px` | corridor half-width used only when `enable_search_roi = True` | legacy corridor-construction state |
| `column_topk` | `20` | sparse column score used only when `enable_search_roi = True` | legacy candidate-construction state |
| `peak_min_distance` | `7 px` | one fifth of manual matched-count projected ion spacing, excluding 0/1-ion matched frames | internal chain-construction scale |
| `local_patch_radius` | `12 px` | local PSF/refinement support size | internal local-model support scale |
| `psf_r_frac` | `0.25` | Fourier-fit radius fraction | internal PSF-fit construction scale |
| `psf_cN` | `2` | power above NPS floor for Fourier fit | internal PSF-fit construction scale |
| `psf_min_points` | `25` | minimum bins for Fourier fit | internal fit-stability safeguard |
| `sigma_min_px` | `1.5 px` | sampling plausibility check | internal PSF plausibility safeguard |
| `psf_r2_min` | `0.7` | Gaussian-fit plausibility check | internal fit-quality safeguard |
| `psf_consistency_tol` | `0.3` | local-vs-FFT agreement window | internal cross-estimator coherence safeguard |
| `eta_variant_count_legibility_npz_path` | `None` | branch-indexed count-legibility artifact carrying one structured runtime field per variant | branch-local frame-mediation artifact |
| `eta_score_admissibility_npz_path` | `None` | branch-indexed score artifact carrying branch power summaries, linear power ratios, log power ratios, thresholds, and margins | branch-local frame-mediation artifact |
| `log_power_spectrum_peak_to_mean` | derived | canonical branch log-power quantity $L_v = \log(P_{\mathrm{peak},v} / \max(P_{\mathrm{mean},v}, \varepsilon))$ | derived branch state, not a free public knob |
| `axial_frequency_band` | `0.06 cyc/px` | spectral comb averaging band | internal spectral-summary construction scale |
| `evidence_margin` | derived | log-odds of chosen ion count over nearest alternative | reported detector state |
| `measurement_precision_score` | derived ∈ [0,1] | aggregated confidence from SNR, margin, and uncertainty | reported detector state |

## Canonical Detector-Update Outer Loop

The manual-review calibration used by `tools/manual_detector_update.py` is an
iterative outer solve, not a one-pass artifact build. Let

$$
 Y = \begin{bmatrix}
 y_1^\top \\
 \vdots \\
 y_n^\top
 \end{bmatrix} \in \mathbb{R}^{n \times p},
 \qquad
 z_{\mathrm{manual}} \in \mathbb{Z}^n
$$

stack the $n$ scored manual frames and their reviewed visible-count labels. In
the parameter dictionary immediately above, the canonical outer-loop symbols are
the following:

- `eta_score_admissibility_npz_path`: the persisted branch score block carrying
  the reference linear powers, reference log powers, thresholds, and margins.
- `eta_variant_count_legibility_npz_path`: the persisted branch eta block
  carrying the runtime eta field and runtime mask per variant.
- `log_power_spectrum_peak_to_mean`: the derived scalar summary that becomes the
  branch additive threshold reference $L_v$.
- `eta_max_abs_correction` and `eta_runtime_min_coherence`: the two mutable
  branch-calibration knobs that shape the runtime eta projection.
- `fixed_point_max_iterations` and `fixed_point_reference_tolerance`: the
  solver-policy defaults that bound the loop and define its stability test.

Let

$$
 Z^{(t)} \in \{0,1\}^{n \times |\mathcal{V}|}
$$

encode the row-wise one-hot branch membership over the public Stage 5 variants,
and for each $v \in \mathcal{V}$ let

$$
 I_v^{(t)} = \operatorname{diag}(Z^{(t)}_{:,v}) \in \{0,1\}^{n \times n},
 \qquad
 L_v^{(t)} \in \mathbb{R},
 \qquad
 E_v^{(t)} = \begin{bmatrix}
 \operatorname{vec}(\eta_v^{(t)}) \\
 \operatorname{vec}(M_v^{(t)})
 \end{bmatrix}
$$

where $L_v^{(t)}$ is the branch additive threshold reference reconstructed from
`eta_score_admissibility_npz_path` and tied to the derived
`log_power_spectrum_peak_to_mean` row, while $E_v^{(t)}$ is the branch
count-legibility block reconstructed from
`eta_variant_count_legibility_npz_path` and built under the runtime safeguards
`eta_max_abs_correction` and `eta_runtime_min_coherence`.

Assemble the branch parameter block as

$$
 L^{(t)} = \begin{bmatrix}
 L_v^{(t)}
 \end{bmatrix}_{v \in \mathcal{V}},
 \qquad
 E^{(t)} = \operatorname{blkdiag}\!\left(E_v^{(t)}\right)_{v \in \mathcal{V}},
 \qquad
   \Theta^{(t)} = \begin{bmatrix}
 E^{(t)} \\
 L^{(t)}
 \end{bmatrix}
$$

The deployed detector-update loop is then written most faithfully in the same
step order as the implementation.

Detector step:

$$
 Z^{(t+1)} = D\!\left(Y ; \Theta^{(t)}\right)
$$

Selected-count and strict-mismatch step:

$$
 \widehat z^{(t+1)} = C\!\left(Y ; \Theta^{(t)}\right),
 \qquad
 m^{(t+1)} = \widehat z^{(t+1)} - z_{\mathrm{manual}}
$$

Branch score-admissibility rebuild:

$$
 R^{(t+1)} = M_{\mathrm{score}}\!\left(Y, Z^{(t+1)}\right),
 \qquad
 L^{(t+1)} = \Pi_L R^{(t+1)}
$$

where $R^{(t+1)}$ is the stacked score-artifact block whose persisted fields are
written to `eta_score_admissibility_npz_path`, and $\Pi_L$ extracts the branch
reference vector composed of the per-variant reference linear powers and the
derived branch log-power summaries $L_v^{(t+1)}$.

Branch count-legibility rebuild:

$$
 E^{(t+1)} = M_{\eta}\!\left(
 Y,
 Z^{(t+1)};
 \eta_{\max},
 \kappa_{\min}
 \right)
$$

with
$$
 \eta_{\max} = \texttt{eta\_max\_abs\_correction},
 \qquad
 \kappa_{\min} = \texttt{eta\_runtime\_min\_coherence}
$$

and where $M_{\eta}$ denotes the persisted branch eta rebuild written to
`eta_variant_count_legibility_npz_path`.

Parameter-block assembly step:

$$
 \Theta^{(t+1)} = \begin{bmatrix}
 E^{(t+1)} \\
 L^{(t+1)}
 \end{bmatrix}
$$

Prioritized strict-working-set screen:

The canonical loop starts with one blank-default full-corpus validation pass
before any manual eta package is built. That baseline accepted state defines
$m_{\mathrm{acc}}^{(0)}$, the first strict mismatch support, and the initial
guard and sentinel sets used by the later prioritized screen.

The canonical implementation does not ignore strict mismatches after a full
validation pass; it prioritizes them. Let the scored frame tensor and its
rowwise vectorization be

$$ \mathcal{Y} \in \mathbb{R}^{n \times H \times W}, \qquad Y = \operatorname{reshape}(\mathcal{Y}, n, p), \qquad p = HW $$

and let the accepted strict-mismatch vector after the previous accepted full
pass be $m_{\mathrm{acc}}^{(t)}$. Define the prioritized active set and its
selector matrix by

$$ A_m^{(t)} = \operatorname{supp}\!\left(m_{\mathrm{acc}}^{(t)}\right), \qquad A^{(t)} = A_m^{(t)} \cup G^{(t)} \cup U^{(t)}, \qquad P^{(t)} = \operatorname{Diag}\!\left(\mathbf{1}_{A^{(t)}}\right) $$

where $G^{(t)}$ is the strict guard set of threshold-moved or near-boundary
matches and $U^{(t)}$ is a small sentinel subset of currently stable strict
matches. The fast prioritized validation pass is then

$$ Y_A^{(t)} = P^{(t)} Y, \qquad Z_A^{(t+1)} = D\!\left(Y_A^{(t)} ; \Theta^{(t+1)}\right), \qquad \widehat z_A^{(t+1)} = C\!\left(Y_A^{(t)} ; \Theta^{(t+1)}\right) $$

with active mismatch vector

$$ m_A^{(t+1)} = \widehat z_A^{(t+1)} - P^{(t)} z_{\mathrm{manual}} $$

A candidate is promoted from this prioritized screen to an expensive full-corpus
confirmation pass only if the hard set improves and the guard set does not
regress:

$$ \alpha^{(t+1)} = \mathbf{1}\!\left\{\|m_A^{(t+1)}\|_0 < \|P^{(t)} m_{\mathrm{acc}}^{(t)}\|_0\right\} \cdot \mathbf{1}\!\left\{\operatorname{supp}\!\left(m_A^{(t+1)}\right) \cap G^{(t)} = \varnothing\right\} $$

This screen is a prioritization rule, not a mismatch waiver: every accepted
candidate is still validated on the full scored corpus.

Full-corpus confirmation and seed acceptance:

$$ Z_{\mathrm{full}}^{(t+1)} = D\!\left(Y ; \Theta^{(t+1)}\right), \qquad \widehat z_{\mathrm{full}}^{(t+1)} = C\!\left(Y ; \Theta^{(t+1)}\right), \qquad m_{\mathrm{full}}^{(t+1)} = \widehat z_{\mathrm{full}}^{(t+1)} - z_{\mathrm{manual}} $$

For each public branch variant $v \in \mathcal{V}$, let

$$ \kappa_v^{(t+1)} = \left\|m_{\mathrm{full},v}^{(t+1)}\right\|_0, \qquad \kappa^{(t+1)} = \left[\kappa_v^{(t+1)}\right]_{v \in \mathcal{V}} $$

For each variant $v$, let $\widetilde Q_{v,i}^{(t+1)}(\omega)$ be the
normalized residual periodogram of manual-match calibration frame $i$ on the
retained frequency-bin set $\Omega_{\mathrm{ret}}$, and let

$$
\overline Q_v^{(t+1)}(\omega)
=
\frac{1}{|M_v|}
\sum_{i \in M_v}
\widetilde Q_{v,i}^{(t+1)}(\omega)
$$

be the corresponding branch reference PSD. The exact-tie frequency criterion
is the aggregate retained-bin adequacy score

$$
\rho^{(t+1)}
=
\frac{1}{|\mathcal V'|}
\sum_{v \in \mathcal V'}
\frac{1}{|M_v|}
\sum_{i \in M_v}
\sum_{\omega \in \Omega_{\mathrm{ret}}}
\left[
\log \overline Q_v^{(t+1)}(\omega)
+
\frac{\widetilde Q_{v,i}^{(t+1)}(\omega)}{\overline Q_v^{(t+1)}(\omega)}
\right],
$$

where $\mathcal V' \subseteq \mathcal V$ is the set of variants with at least
one manual-match calibration frame. The accepted seed update is componentwise
across the four public variants, not aggregate-only. A full-corpus candidate is
accepted only if it does not regress any variant and either strictly improves
at least one variant or wins an exact-tie frequency-reference tie-break:

$$ \beta^{(t+1)} = \mathbf{1}\!\left\{\kappa^{(t+1)} \preceq \kappa_{\mathrm{acc}}^{(t)}\right\} \cdot \mathbf{1}\!\left\{\left(\exists v : \kappa_v^{(t+1)} < \kappa_{\mathrm{acc},v}^{(t)}\right) \;\lor\; \left(\kappa^{(t+1)} = \kappa_{\mathrm{acc}}^{(t)} \;\land\; \rho^{(t+1)} + \varepsilon_{\rho} < \rho_{\mathrm{acc}}^{(t)}\right)\right\} $$

$$ \Theta_{\mathrm{acc}}^{(t+1)} = \beta^{(t+1)} \Theta^{(t+1)} + \left(1 - \beta^{(t+1)}\right) \Theta_{\mathrm{acc}}^{(t)} $$

Here $\preceq$ is understood componentwise and $\varepsilon_{\rho}$ is the
small frequency-reference tie-break tolerance. The adequacy term never
overrides manual parity: it is consulted only when the full-corpus per-variant
mismatch vector is exactly unchanged.

Candidate rejection is also staged. If a proposal fails the prioritized screen
or the full-corpus seed-acceptance test, the solver rebuilds the same seed one
more time. If that retry still fails, the loop stops with a rejection report;
it does not search over ad hoc calibration-sample exclusions.

All stability checks are evaluated on the accepted full-corpus state
$\Theta_{\mathrm{acc}}^{(t)}$, not on the intermediate prioritized screen.

Stability-summary step:

$$
 s^{(t+1)} = \begin{bmatrix}
 \|m^{(t+1)}\|_0 \\
 \operatorname{supp}(m^{(t+1)}) \\
 \{\mathcal{I}_v^{(t+1)}\}_{v \in \mathcal{V}} \\
 \{P_{\mathrm{ref},v}^{(t+1)}\}_{v \in \mathcal{V}} \\
 \{L_v^{(t+1)}\}_{v \in \mathcal{V}} \\
 \{c_v^{(t+1)}\}_{v \in \mathcal{V}}
 \end{bmatrix}
$$

where $\mathcal{I}_v^{(t+1)}$ is the included calibration sample-ID set for
variant $v$, $P_{\mathrm{ref},v}^{(t+1)}$ is the branch reference linear power,
and $c_v^{(t+1)}$ is the variant runtime covered-pixel count.

The canonical minimal-upgrade loop stops on stability of the deployed contract
variables or on the solver cap:

$$
 s^{(t+1)} = s^{(t)}
$$

with the reference-summary comparisons understood componentwise as

$$
 \left|P_{\mathrm{ref},v}^{(t+1)} - P_{\mathrm{ref},v}^{(t)}\right|
 \leq \delta_{\mathrm{fp}},
 \qquad
 \left|L_v^{(t+1)} - L_v^{(t)}\right| \leq \delta_{\mathrm{fp}},
 \qquad
 \delta_{\mathrm{fp}} = \texttt{fixed\_point\_reference\_tolerance}
$$

for every $v \in \mathcal{V}$, together with unchanged strict mismatch count,
strict mismatch sample IDs, included calibration sample IDs, and covered-pixel
counts. If that stability test never passes, the loop stops after
`fixed_point_max_iterations` rebuilds.

Strict manual parity is not itself the break condition. It is the final success
outcome reported after the loop has either stopped stably or hit the iteration
cap:

$$ \mathcal{P}^{(t+1)} = \mathbf{1}\!\left\{m^{(t+1)} = 0\right\}, \qquad \texttt{converged} = \mathbf{1}\!\left\{\texttt{stopped\_on\_stability}\right\} \cdot \mathcal{P}^{(t+1)} $$

This is the canonical fixed-point interpretation for the repo. In optimization
language, it is closer to a generalized-EM or cyclic block-coordinate solve
than to a single closed-form estimator: one block updates branch assignments
with the deployed detector, one block rebuilds the branch score references, and
one block rebuilds the branch eta fields. The online EM overview in StatLect
and the coordinate-descent notes in Peng's *Advanced Statistical Computing*
describe this alternating-update structure explicitly; the detector-update loop
inherits that same iterative shape even though its practical convergence monitor
is detector-specific rather than a pure parameter norm.

With the prioritized strict-working-set screen, the canonical loop is more
precisely an alternating full-state solve with an active-set scheduler: hard
rows are revisited first to increase iteration throughput, but the accepted
state is still defined only by full-corpus detector validation.

That same distinction determines which parameters are allowed to move. The
canonical outer loop is meant to retune only the two branch-local calibration
surfaces named above. Detector-structure controls remain academically fixed so
the loop is identifying calibration fields for a stable detector, not
redefining the detector at each iteration.

Mutable canonical detector-update knobs:

- `eta_max_abs_correction`
- `eta_runtime_min_coherence`

Academically fixed defaults for canonical detector-update validation:

- `search_row_fraction = [0.0, 1.0]`
- `search_col_fraction = [0.0, 1.0]`
- `search_half_width = 10000`
- `enable_gaussian_warning_count_corrections = False`
- `fixed_point_max_iterations = 3` by default, with CLI override `--fixed-point-max-iterations`
- `fixed_point_reference_tolerance = 1e-6` by default, with CLI override `--fixed-point-reference-tolerance`

### Operator Realization And Mode Coverage

The operator-facing calibration corpus is the root `manual_count_template.csv`
paired with the precleaned source archive directory
`C:/Users/isaia/Desktop/run3_5926_precleaned`. If that CSV does not yet exist,
the review-image export path first writes a template CSV together with a chosen
number of review PNGs; the detector-update dataset NPZ is then rebuilt from the
completed CSV before the fixed-point solve is run.

At the artifact level, the implemented detector-update solve is not selected-count
only. Let the public branch set remain

$$
\mathcal V = \{\text{anisotropic\_gaussian},\text{symmetric\_gaussian},\text{anisotropic\_poisson},\text{symmetric\_poisson}\}
$$

and let $\mathcal U$ be the configured ledger-only experimental Stage 5 mode-ID
set. The canonical solve emits the per-variant artifact family

$$
\mathcal A_{\mathrm{can}} = \{(S_v, C_v) : v \in \mathcal V\},
$$

where $S_v$ is the score-admissibility artifact and $C_v$ is the branch
variant-count-legibility artifact for public variant $v$. For each configured
mode $u \in \mathcal U$, the implemented detector-update pipeline then runs one
additional mode-targeted fixed-point solve with the selected mode pinned to $u$:

$$
\mathcal A_u = \{(S_{u,v}, C_{u,v}) : v \in \mathcal V\}.
$$

Those mode-targeted solves do not widen the public variant set and do not turn
ledger-only modes into unconditional selected-count modes. They rebuild the
same two artifact families against the mode-local accepted-set and residual
surface, then persist the resulting paths back into the override record with
mode-local provenance (`calibration_policy = \texttt{mode\_artifact}` and
`threshold_source = \texttt{manual\_calibrated\_mode\_tau\_v\_star}`).

The implemented manual detector update is therefore a two-level solve:

1. one canonical fixed-point solve over all four public variants;
2. one additional fixed-point subpass for each configured ledger-only Stage 5 mode, again carrying all four public variants internally.

This is the contract that the docs mean by “artifact creation and optimization
apply to all selection modes and PSF/noise variants”: every solve remains
branch-local across the four public variants, and every configured selection
mode receives its own calibrated artifact pair rather than borrowing the
canonical threshold movement implicitly.

### Current Canonical-Promotion Candidates

The accepted post-fixed-point preset set is larger than the current promotion
candidate set. On the strict scored manual corpus derived from
`manual_count_template.csv`, three named presets presently satisfy full live
parity on all `113` scored rows:

- `mode_integrated_snr`
- `mode_support_sum_snr`
- `mode_template_support_excess_density`

This is a promotion frontier, not a declaration that the shipped canonical
selected-count path has already changed. The ordinary canonical runtime still
uses the current canonical matched-SNR selection path unless one of the named
manual-calibrated presets is requested explicitly.

## Method Design References

The URLs below were collected during the method-design research pass and are
the reference set for the three detector-method notes. They are intentionally
kept here so the canonical and experimental method docs point to the same
source list.

- Marco Taboga, *EM algorithm* (2021): <https://www.statlect.com/fundamentals-of-statistics/EM-algorithm>
- Roger D. Peng, *Advanced Statistical Computing*, Chapter 4, *The EM Algorithm*: <https://bookdown.org/rdpeng/advstatcomp/the-em-algorithm.html>
- Roger D. Peng, *Advanced Statistical Computing*, Section 3.5, *Coordinate Descent*: <https://bookdown.org/rdpeng/advstatcomp/coordinate-descent.html>
- Stephen J. Wright, *Coordinate Descent Algorithms* (2014/2015): <https://optimization-online.org/2014/12/4679/>
- Peter J. Denning, *The Working Set Model for Program Behavior* (1968): <https://denninginstitute.com/pjd/PUBS/WSModel_1968.pdf>
- Peter J. Denning, *Working Set Analytics* and related working-set publications: <https://denninginstitute.com/pjd/PUBS/Workingsets.html>
- Abhinav Shrivastava, Abhinav Gupta, Ross Girshick, *Training Region-Based Object Detectors With Online Hard Example Mining* (CVPR 2016): <https://openaccess.thecvf.com/content_cvpr_2016/html/Shrivastava_Training_Region-Based_Object_CVPR_2016_paper.html>
- PSD and autocorrelation duality: [Probability Course reference](https://www.probabilitycourse.com/chapter10/10_2_1_power_spectral_density.php)
- Colored-noise matched filtering review: [arXiv gr-qc/0509116](https://arxiv.org/abs/gr-qc/0509116)
- Photutils background guide: [Photutils background user guide](https://photutils.readthedocs.io/en/stable/user_guide/background.html)
- Photutils detection guide: [Photutils detection user guide](https://photutils.readthedocs.io/en/stable/user_guide/detection.html)
- Photutils PSF guide: [Photutils PSF user guide](https://photutils.readthedocs.io/en/stable/user_guide/psf.html)
- EM overview and fixed-point interpretation: [StatLect EM algorithm overview](https://www.statlect.com/fundamentals-of-statistics/EM-algorithm)
- Coordinate descent / backfitting overview: [Peng's Advanced Statistical Computing notes](https://bookdown.org/rdpeng/advstatcomp/coordinate-descent.html)
- Penalized spline smooth terms: [mgcv smooth terms reference](https://stat.ethz.ch/R-manual/R-devel/library/mgcv/html/smooth.terms.html)
- Latent Gaussian or GMRF spatial modeling with INLA: [Journal of Statistical Software article](https://www.jstatsoft.org/article/view/v063i19)
- Poisson likelihood and Cash statistic overview: [Sherpa statistics overview](https://cxc.cfa.harvard.edu/sherpa/statistics/)
- Poisson matched-filter detection theory: [arXiv 1709.01524](https://arxiv.org/abs/1709.01524)
- Poisson matched-filter false-alarm calibration: [arXiv 1801.02859](https://arxiv.org/abs/1801.02859)
- Spectral flatness reference: [librosa spectral flatness reference](https://librosa.org/doc/main/generated/librosa.feature.spectral_flatness.html)

## Known Heuristic Surfaces

The same surfaces read more cleanly when organized by the same vocabulary used
in the calibration table: first-principles anchors, $\alpha$/$q$-derived
controls, and frame-mediation state.

### First-Principles Anchors For Heuristic Surfaces

1. Tiled sigma-clipped local background statistics are grounded in robust
  location/scale estimation \cite{BeersFlynnGebhardt1990}; the detector's
  dense nuisance layer inherits that anchor even though some construction
  details remain implementation choices.
2. Fano and mean-variance target families ($F=1$, $a=1$; $F=2$, $a=2$) are
  theory-backed photon-transfer / Fano anchors for Poisson-like and EMCCD-like
  data \cite{Fano1947,Janesick2007,MortensenFlyvbjerg2016,RobbinsHadwen2003}.
3. Hann-windowed averaged periodograms, spectral flatness, and related NPS
  summaries are theory-backed PSD diagnostics
  \cite{BlackmanTukey1958,Harris1978,Dubnov2004}.
4. Single-frame uncertainty on Fano, mean-variance slope/intercept, and NPS
  whiteness/flatness/anisotropy is theory-backed by linear-regression standard
  errors \cite{Janesick2007} and MAD-based robust location SE
  \cite{BeersFlynnGebhardt1990}.
5. The Gaussian matched filter, candidate-local Poisson rescoring, and the
  Wiener-Khinchin residual spectral summaries used for branch audits are
  theory-backed score families rather than arbitrary engineering inventions
  \cite{MarrHildreth1980,Turin1960,Wiener1930,Khintchine1934,BlackmanTukey1958}.
6. Branch power-ratio and log-power summaries are theory-backed monotone
  summaries of residual-spectrum concentration and log-domain compression
  \cite{Harris1978,Dubnov2004}.

### $\alpha$/$q$-Derived Controls For Heuristic Surfaces

1. Relative-deviation bands around the Poisson and EMCCD targets are current
  detector-family tolerances; their scientific role is to represent an
  explicit error budget around the first-principles anchors rather than to act
  as immutable constants.
2. Whiteness intervals, regime-family soft-score widths, and the hard-label
  projection are current null-interval or quantile controls layered on top of
  the PSD and Fano anchors.
3. Hot-pixel Gaussian-tail limits are theory-backed in form, but the exceedance
  threshold $k$ and control-limit width $z$ are current tail-risk controls.
4. Provisional peak-finding thresholds (height, prominence, min distance) are
  current seed-stage exceedance controls; they feed an auditable Stage 5 score
  rather than define the final count directly.
5. Final Stage 5 regime floors are fallback decision boundaries. When a valid
  score-admissibility artifact is present, the artifact owns the score-domain
  threshold base and signed movement; the runtime floor from
  `min_accepted_matched_snr`,
  `compressed_artifact_min_accepted_matched_snr`, and
  `eta_corrected_compressed_artifact_min_accepted_matched_snr` remains the
  fallback anchor. On Gaussian branches the score is matched SNR; on Poisson
  branches it is the centered local Poisson score. An auxiliary
  confidence-weighted `evidence_margin` is reported for transparency but does
  not change the published count.
6. The branch manual-match inclusion rule, connected-support extraction,
  per-pixel coherence gate, runtime absolute-correction cap, and signed
  score-admissibility movement caps are also current significance or quantile
  controls rather than first-principles equalities.

### Frame-Mediation State For Heuristic Surfaces

1. Block geometry, dark-tile sampling, and dim-tile subset selection build the
  dense nuisance field and PSD estimators. Their essence is not "academic
  truth" but internal state construction for a given frame.
2. Gaussian and median prefilters, DoG scales, legacy ROI/corridor metadata,
  and sparse column logic are frame-mediation state used to construct the
  working image and candidate support. Legacy corridor metadata remains
  compatibility-only and no longer controls the default Stage 4/5 path.
3. PSF reconciliation windows, no-patch fallback priors, local support radii,
  and dark-tile propagated matched-response sigma are frame-mediation state
  used to stabilize response construction. The weak-band quantile response
  estimate remains fallback-only when the propagated dark-tile estimate is not
  available.
4. Branch residual spectral objects for count-legibility and
  score-admissibility, together with the branch eta and score-artifact
  packages, are frame-mediation state carried across calibration and runtime
  rather than public academic knobs.

This re-bucketing does not invalidate the method. It clarifies where the repo
already stands on first-principles ground, where the current implementation is
really carrying explicit error-budget controls, and where the code is simply
constructing the per-frame mediation state needed to make the detector
operational.

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

@software{Photutils2026,
  author  = {Bradley, Larry and others},
  title   = {Photutils},
  version = {3.0.0},
  year    = {2026},
  doi     = {10.5281/zenodo.596036},
  url     = {https://photutils.readthedocs.io/en/latest/}
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

@article{Dijck2018,
  author  = {Dijck, Elwin A. and Mohanty, Amita and Valappol, Nivedya and Nu{\~n}ez Portela, Mayerlin and Willmann, Lorenz and Jungmann, Klaus},
  title   = {Lifetime of the 5d$^2$D$_{5/2}$ level of $^{138}${Ba}$^+$ from quantum jumps with single and multiple {Ba}$^+$ ions},
  journal = {Physical Review A},
  volume  = {97},
  pages   = {032508},
  year    = {2018},
  doi     = {10.1103/PhysRevA.97.032508}
}
```

## Verification Anchors

The repository already contains tests that provide concrete verification
anchors for the main claims documented here:

- `tests/test_invariants.py` checks Poisson Fano behavior, mean-variance slope, NPS whiteness, flatness, anisotropy, and regime consistency
- `tests/test_crossval.py` checks local-vs-FFT PSF consistency and prefilter robustness
- `tests/test_unit.py` checks exact count-decision margin semantics
- `tests/test_synthetic.py` checks synthetic count, centroid, spacing, PSF, and localization-trend behavior inside the detector-core scope
- `tests/test_higher_validation.py` holds the deferred CRLB-style localization bound outside the detector-core acceptance gate

Those tests do not prove universal optimality. They do provide concrete anchors
for what the present implementation is claiming.
