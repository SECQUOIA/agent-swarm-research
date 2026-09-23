# Independent review: Stage 00, round 01, reviewer 3

Reviewer: `paper_reviewer_3`. Date: 2026-09-07.

I inspected the scaffold, plan, notation ledger, claim inventory, author handoff, review templates, review ledger, and build record. I did not read other reviewers' reports or coordinate findings. This is a preparation-stage review, not certification of proofs explicitly assigned to later stages.

Reviewed substantive infrastructure hashes (SHA-256):

- `PLAN.md`: `943457d6888a441c054a0e23b5c3dc69ac0bc6262e71387dc1cf9aca81cdb14a`
- `claims-map.md`: `aae5c9883aa3de7c81b5a916a76f9c9ea7634ce3ddc93a39597f7663fa8342f6`
- `notation.md`: `6fbcb755c8306fa62f40554696864fe766268b6115d661d3f98be1c9f2d1739b`
- `main.tex`: `11f0cd99bd54159fbceec18943ecb3abbf2a5e33c72ff46782189dcc135b5c13`
- `preamble.tex`: `69757a0786a132d9f837548aadfe1bd55e7503acb870508d66234e2d74e54572`
- `sections/00-status.tex`: `14fae1d9eaf46dfdae00c2722feed48b67f24a5d25f358c3586bdac2260702c2`

## Checks performed

The scope correctly distinguishes quenched disorder moments from particle-displacement moments, recognizes the finite-bulk ergodicity/form obligations, and does not interpret local whole-line inverses as stationary probability systems. Fixed per-observation budgets and noiseless bins are distinguished from average-budget or arbitrary noisy-sensing models. The two unfinished variational limits are assigned substantive development rather than relabeled as established.

I independently checked the dimensions in `claims-map.md:13`: tangential diffusivity has units length squared/time, its wall integral has units length cubed/time, and the integrated inverse response has units length times time. Therefore `J_phys=(ell_ref/k_ref)J'` is correct. Also `KV^2/Z` has units length/time squared in a two-dimensional cross-section, giving dispersion units length squared/time after multiplication by J. The local placement expression `a^(-4/5)m^(-1/5)` has the same response units. The harmonic coefficient given in L1 is consistent with the alternative gamma expression through the gamma reflection identity. These checks do not establish localization or policy-transfer theorems.

The workflow explicitly implements one stage author, five independent reviewers, coordinator adjudication, a different correction agent, another five-reviewer round after any valid major issue, correction of remaining valid minor issues, sequential stage acceptance, and the same process for the complete manuscript. Its snapshot rule prevents merging reviews of different drafts. Actual compliance beyond this initial author/review round remains to be recorded as work proceeds.

## Findings

### R3-01 — Minor: make the zero axial wall-drift assumption explicit

Location: `claims-map.md:7–9,19`; `notation.md:12–14`; Stage 1 scope in `PLAN.md`.

The mean `V=integral_Omega u/(A+KP)` and response prefactor `KV^2/Z` assume zero mean longitudinal velocity in the adsorbed state. Constant affinity by itself does not imply this: with wall drift w(s), the mean includes `K integral_Gamma w`, and the scalar constant-source reduction changes. Tangential wall mobility and possible axial Brownian diffusion do not supply this missing drift assumption. The ledger currently names no wall drift, but absence of a symbol is insufficient to define the physical scope.

Remedy: explicitly state that adsorbed particles have zero longitudinal advective drift, while any axial molecular diffusion is treated separately. Also describe reversibility as a property of the cross-sectional exchange/diffusion process, rather than the longitudinally advected process as a whole. I classify this as minor at the scaffold stage because the actual model derivation is explicitly reserved for Stage 1; it must not survive into the theorem assumptions.

### R3-02 — Minor: define the canonical ensemble in the inventory itself

Location: `claims-map.md:24–42`; `notation.md:10,18,30`.

The inventory repeatedly refers to the “cosine ensemble” and uses its density and bin width, but does not actually state its rate formula or probability law. These determine every displayed sharp coefficient. A reader currently needs to follow a source-note link to recover them.

Remedy: add a short canonical-model declaration, in dimensionless variables, such as `s in R/(2pi Z)`, `k_c(s)=(c+cos s)^2`, `c uniform on [-2,2]`, with c sampled once and fixed during transport. Identify the equal-bin partition as the partition of this offset interval. This is a scope-definition improvement, not a request to write later proofs prematurely.

### R3-03 — Minor: reserved notation conflicts with the Gaussian counterexample

Location: `notation.md:8` versus `claims-map.md:31`.

The ledger reserves A exclusively for bulk area, but L4 uses A and B for Gaussian amplitudes. This directly conflicts with the purpose of a stable notation ledger, and B is additionally the beta-function glyph elsewhere.

Remedy: use different amplitude names, for example independent standard Gaussian variables `xi_1, xi_2`, in the counterexample and its lower bound. Reserve A for area as planned.

## Overall assessment

No major issue found in Stage 0. The structure is appropriately cautious and comprehensive for the specified paper, and the sequential plan is compliant with the user's requested review process. Correct the three valid minor scope/notation issues before accepting this stage. No broader mathematical validity, numerical accuracy, or novelty conclusion is supplied by this scaffold review.
