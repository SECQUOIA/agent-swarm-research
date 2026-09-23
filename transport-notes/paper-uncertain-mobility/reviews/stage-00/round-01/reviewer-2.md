# Independent review: stage 00, round 01, reviewer 2

Date: 2026-09-07. Independence: prepared without reading any other review report in this round or coordinating findings with other reviewers. No manuscript files were edited.

## Reviewed material and snapshot

Read the complete stage plan, claim inventory, notation ledger, README, LaTeX entry point/preamble/status section, review protocol and templates, author handoff, and build record. Inspected the underlying scalar-to-bulk transfer and finite-precision source arguments to test the dependency assignments; their earlier verification labels were not used as authority.

SHA-256 snapshot identifiers:

- `PLAN.md`: `943457d6888a441c054a0e23b5c3dc69ac0bc6262e71387dc1cf9aca81cdb14a`
- `claims-map.md`: `aae5c9883aa3de7c81b5a916a76f9c9ea7634ce3ddc93a39597f7663fa8342f6`
- `notation.md`: `6fbcb755c8306fa62f40554696864fe766268b6115d661d3f98be1c9f2d1739b`
- `main.tex`: `11f0cd99bd54159fbceec18943ecb3abbf2a5e33c72ff46782189dcc135b5c13`
- `preamble.tex`: `69757a0786a132d9f837548aadfe1bd55e7503acb870508d66234e2d74e54572`
- `README.md`: `45c774cf4dc86717b95529c93afc5a8999ceec45d95e30fc7f849724a747fae3`
- `reviews/README.md`: `156af753f118d69a8f9b2ac7d14e8beac9c2bc0a918e70d284e917a675dcd430`

## Checks performed

This stage is an audit scaffold, not a theorem manuscript. I checked that major open questions were assigned development rather than disguised as established statements, that proof prerequisites can be developed in the proposed order, that the proposed coefficients are internally consistent, and that the required author/five-reviewer/separate-fixer loop is faithfully specified.

Independent normalization checks:

1. For two symmetric ordinary roots with curvature `a=1-c²`, the constant-mobility contribution is `2 C0 a^(-3/4) ε^(-1/4)`. Averaging at density `1/4` and converting `dc=|sin s| ds` yields the subcritical design coefficient in D2, including its factor `2^(q-3)`. The allocation integral is `2 B((1-αq)/2,1/2)`.
2. Numerically recomputed `C0=4.647476009400967`, `Cpl=6.222823736019888`, `K1=18.386063650114284`, `Kobs=22.40462823074913`, `Kcrit=2.0223307639693906`, and `Kcoarse=25.723827388763294` from the displayed formulas. The decimal mean constants in O2 agree.
3. The supercritical balancing powers are coherent: fold radius `M^(1/7)`, response `M^(-3/7)`, and parameter width `M^(2/7)` give moment order `M^((2-3q)/7)`. Its intersection with `M^(-q/4)` is `q=8/5`; the critical allocation logarithm has power `1+q/4=7/5`. This scaling check is not a sharp-limit proof, and the plan correctly does not treat it as one.
4. The proposed X2 formula reproduces both endpoint constants algebraically. With `Fcenter(0)=Cpl`, the integral is `B(1/2,1/5)`. With the large-argument form `C0 η^(1/4)`, the integrand exponent is `-4/5-3/40=-7/8` and the factor is `2^(6/5+1/20)/4=2^(-3/4)`, producing P3. The plan correctly says these checks do not prove the interior limit.
5. The nondimensional conversions for D, M, and J are consistent with a one-dimensional wall and a reaction rate. The extra `ell_ref/k_ref` in the physical response is necessary and is present.
6. Stage 1 need not depend on the later oracle theorem: a root-centered bump of width `M^(1/5)` directly proves the observation-uniform lower bound needed in M4. The source argument supplies this route. The rest of the stated dependency order is coherent.

## Findings

### R2-01 — Minor: define the canonical ensemble explicitly in the scope inventory

Location: `claims-map.md`, scope paragraphs and L3/D2; `notation.md`, Jc row.

The inventory repeatedly refers to the “cosine ensemble” and specifies exact coefficients, but never directly states its complete definition: nondimensional `s∈R/(2πZ)`, `k_c(s)=(c+cos s)^2`, and `c` uniform on `[-2,2]`. The L3 verification column mentions density `1/4`, and the source notes contain the definition, but a scope/notation artifact should not require following links to identify the basic ensemble. In particular, the density and wall length determine all the displayed constants.

Remedy: add the canonical rate, domain, and probability law to the scope or notation ledger, and make clear that this definition applies to the exact constants D2–D3, O2, and P2–P3/X2. This is a small scaffold clarification, not a challenge to the formulas.

### R2-02 — Minor: record zero surface axial drift with the physical assumptions

Location: `claims-map.md:7–19`, especially M1; `notation.md`, u/V and axial diffusivity rows.

The candidate mean `V=∫Ωu/(A+KP)` and prefactor `χ=KV²/Z` assume zero axial advective drift in the surface state. Constant affinity alone does not imply this. With a nonzero surface drift w(s), the mean includes `K∫Γw`, and the surface source generally ceases to be the constant used here. The stage plan promises an explicit model later, so this is not a current false theorem, but this material assumption should be part of the scope now to prevent accidental broadening.

Remedy: explicitly state that adsorbed particles have zero axial advective velocity while any surface axial molecular diffusion is treated separately. Stage 1 should derive the model under that assumption.

### R2-03 — Minor: Gaussian coefficient notation conflicts with the ledger

Location: `claims-map.md:31` (L4), compared with `notation.md:8`.

The ledger reserves A exclusively for bulk area, but the Gaussian counterexample uses `g=A cos s+B sin s`. This is an actual inconsistency in the present artifacts, although it has no mathematical consequence.

Remedy: rename the two Gaussian amplitudes, for example `ξ1,ξ2`, and specify their independent standard-normal law in the L4 verification task. Keep A for cross-sectional area.

## Explicit future obligations, not current-stage defects

- Arbitrary L¹ designs, the smooth-test definition, physical closed forms, and measurable policies present genuine analytical difficulties. Stage 1 expressly owns them; there is no current claim that they have been resolved.
- Sharp supercritical localization and possible measure relaxation are unfinished. X1 and Stage 3 clearly identify the necessary liminf, recovery, tail, and mass-allocation arguments. Their absence from this scaffold is not an issue requiring a proof at Stage 0.
- The interior finite-precision crossover similarly remains a proposed formula, with uniform conditional localization expressly required in X2/Stage 6. No sharp equivalent is being claimed prematurely.
- Generic-fold orders are not generic-fold sharp coefficients. The inventory maintains that boundary.
- Literature searches and numerical reproduction have a clear later stage. No novelty claim or numerical certification is currently asserted in the LaTeX scaffold.

## Overall assessment

No major issue found in Stage 0. Accept after the three minor consistency/definition corrections above. This verdict approves the scope and workflow only; it does not certify the candidate theorems, future sharp limits, or novelty. The plan provides a sound basis for the requested sequential development and review.
