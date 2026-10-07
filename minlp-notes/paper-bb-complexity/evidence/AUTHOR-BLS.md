# BLS chapter source, proof, and integration record

Owned files are `sections/binary-least-squares.tex`,
`appendices/bls-proofs.tex`, and this report. The chapter is saved with
complete proofs of every selected nonstandard result. It follows the root's
Sol fallback authorization after the Claude usage limit.

## Evidence incorporated

- `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`,
  `INCOMING-AUDITS.md`, and `ISSUES.md` read before writing and reread at the
  finalization stage. The root integration decision governs the selected
  scope, rather than stale architecture proof-status entries.
- `AUDIT-DISCRETE.md`: complete Gaussian sign-orbit/NNLS development,
  including SO, NT, UN, C1, RI, exact Student density TD, exact coefficient
  mixture EM, and matching root threshold RT; BLS scope corrections and
  corrected ML-gap summation.
- `REVIEW-NNLS-R1.md`: complete core review and Section 8's separate exact
  coefficient-mixture/root-threshold review. Its explicit nonzero
  genericity conditions, distinction between orthant and box values,
  factor `2t` in mixture concentration, and exact `beta_N` expansion are
  included. The review's extension verdict is verified independently,
  superseding the stale “optional extension being reviewed” ledger text.
- Original mathematical source:
  `research-20260928b/bb-complexity/binary-least-squares/certification-thresholds.md`,
  model/conventions and Sections 1–4, with audited corrections. The chapter
  selects root exactness, ML comparison, cone/NNLS laws, C1, root inactivity,
  and hard certificate regimes; it does not copy the source's experiments,
  SDP comparison, midpoint-clique study, or heuristic extrapolations.
- Latest available `LITERATURE-KEYS.md` reread, including the primary-source
  distinction between the 2009 and 2014 square-system ML statements. At this
  stage `LITERATURE.md` is not yet present. The source identity and theorem
  scope messages received from root are used only for narrow attribution.

## Claim and proof map

| Manuscript label | Claim and hypotheses | Complete proof location | Source or comparison |
|---|---|---|---|
| `bls:model`, `bls:class-number` | Independent Gaussian design/noise; deterministic planted signs; `M>=N`; node oracle minimizes original quadratic on convex subsets of box. Class number is minimum arbitrary-convex-piece leaves and lower-bounds all permitted trees. | Main model discussion and elementary convex-hull argument | Source Section 0; lattice framework |
| `bls:ml` | Planted unique integer optimum if `beta_N rho_N >= (2+delta)log N`, fixed `delta>0`; uniform value-gap bound without recovery assumption. | `app:bls-ml-proof` | Source Theorem 2.2(a,c); fixed-margin square ML comparison to 2014 Hassibi et al. Lemma IV.2 |
| `bls:root-exactness` | Planted root minimizer probability exactly `2^-N`; global root exactness iff unique root minimizer is a vertex; explicit exponential upper bound. | `app:bls-root-exactness-proof` | Source Propositions/Theorems 1.1–1.2 |
| `bls:sign-orbit` | Sign-invariant event identity, full rank, explicit nonzero fixed-support regression coordinates and off-support residual products. Empty support residual is explicitly defined. | Main full deterministic KKT/sign-orbit proof | AUDIT-DISCRETE SO; REVIEW-NNLS Sections 1–2 |
| `bls:nnls-law` | Binomial support law; exact multivariate Student OLS density; selected positive coordinates distributed as its absolute values; maximum CDF; joint projection chi-square law. Requires independent isotropic Gaussian target, positive scales, and `n<=M`. | `app:bls-nnls-proofs`; concentration in `app:bls-beta-concentration` | AUDIT TD/EM and REVIEW Section 8; classical Gaussian cone law attributed to Hug–Schneider/McCoy–Tropp; Student regression law described as classical |
| `bls:nnls-tail` | Exact finite maximum coefficient bound `(n/2)q^(M-n+1)((1+q)/2)^(n-1)`. | Main full coordinate regression and binomial-sum proof | AUDIT NT; REVIEW Sections 2–3 |
| `bls:c1-threshold` | Fixed `rho=theta N`, `theta>0`, `M/N->beta>=1`; simultaneous upper-box inactivity; uniform wrong-fixing gap; threshold `theta_c=1/[4(2beta-1)]` with fixed margins. | Main full proof via NT and exact residual mixture; elementary bounds in `app:bls-probability-lemmas` | AUDIT UN/C1; REVIEW Sections 4–6; model-specific application of `lattice:path` |
| `bls:root-threshold` | Exact random cutoff `rho_box=(max u°(1))²/4`; root box value equals orthant iff `rho>=rho_box`, including equality. First-order ratio `rho_box/[log N/(2beta_N-1)]->1`. | Main scaling/uniqueness proof; `app:bls-root-threshold-proof` supplies full extreme-value/mixture limit proof | AUDIT RT; REVIEW Section 8 |
| `bls:root-inactivity-tail` | Finite sufficient inactivity bound; logarithmic expansion with exact `beta_N`. | Direct NT substitution; expansion in `app:bls-root-threshold-proof` | AUDIT RI; REVIEW Sections 1,7 |
| `bls:certificate-law` | `rho->infty`, `rho=o(N)`, `0<=epsilon<=rho`: logarithmic certificate size `Theta_beta((N/rho)log rho)`; fixed `rho>=rho0(beta)`: `Theta_{beta,rho}(N)`. Static order independent of data; optimal incumbent for the stated optimum certificate. | `app:bls-static-upper-proof`, `app:bls-overlap-entropy`, `app:bls-hard-lower-proof`; main explicitly absorbs logarithmic subtraction | Source Sections 4.1–4.3 and audited safe-range repair |

## Proof simplifications and constants

The hard upper proof now uses the exact orthant residual mixture directly.
For a fixed static-order node with `K` wrong fixings, its independent
Gaussian target variance is `1+4rho K/N`; the residual is that variance
times a `chi-square(M-S)` variable with `S~Bin(N-d,1/2)`. Union bounding over
at most `(N+1)binom(N,K)` nodes gives the upper bound with explicit
deterministic margin

`eta_N=[log(e rho)/rho + log N/N + rho/N]^(1/8)`.

The main upper coefficient remains `1/[4(2beta-1)]`. This simplification
does not assert independence between nodes and does not cover adaptive
data-dependent variable orders.

The hard lower proof replaces the sharp Gaussian singular-value estimate
by an elementary `1/2`-net operator bound and avoids the source's decimal
barycenter constants. All auxiliary estimates are proved in the appendix.
With

`C_beta=2[sqrt(beta+1)+sqrt(2(log5+1))]`,
`p=Phi(-1)-Phi(-2)`,

the displayed valid lower constant is

`c_beta=beta p/[256 e² C_beta^4]`.

The fixed-SNR threshold is an explicit existence choice satisfying
`4log(1+exp(-0.07 beta rho0))<d_beta/2`,
`d_beta=beta p/[64 e² C_beta²]`, `rho0>=e`.
These are more conservative than the original source's `c_1≈1.8e-5` and
`rho0(1)=71`; those numerical constants and their finite-size claims are
not attached to this proof. The entropy proof uses an elementary
mode/Chebyshev binomial estimate `-log(8sqrt(k))`; the final loss is still
`-log(8N)` after floor accounting. A read-only mathematical subagent
independently checked the proposed conservative constants and the safe
regime deductions; final manuscript review is separate.

## Claim boundaries and exclusions

- A C1 failure is not a lower bound on tree size. The sharp threshold is
  stated only for fixed `theta` and fixed margins, not a shrinking critical
  window or the optimum over all possible linear-size trees.
- The C1 path application specifies the optimal incumbent for weak bounds,
  or exact best-bound selection and strict bounds when no initial optimal
  incumbent is present. Box least squares is exact at the surviving fixed
  binary singleton, and processing it evaluates the feasible vertex.
- Orthant value, box value, planted root minimizer, global vertex root
  exactness, rounding correctness, and ML recovery are explicitly distinct.
  The equality endpoint is retained. Positive `rho` is essential.
- No Hu–Lu decoder theorem is used as a simultaneous-node proof input.
- No blanket ML assertion is made for all order-`log N` signals. The
  theorem has the fixed boundary margin `(2+delta)log N`; lower certificate
  statements outside recovery use the actual OPT value gap.
- The matching hard law is not asserted throughout a finite interval
  `rho<=c' N`. The subtraction in the lower bound is explicitly retained
  and absorbed only in the two selected safe regimes.
- No universal algorithmic hardness, practical speedup, SDP square-system
  scaling theorem, or runtime bound follows from these node counts.
- No experiment is described as newly rerun or verified. The chapter
  has no numerical experiment dependency.

## Literature keys used

`hugSchneider2016RandomConicalTessellations`,
`mccoyTropp2014SteinerFormulas`,
`hassibiHansenDimakisAlshamaryXu2014OptimizedMCMC`, and
`huLu2020LimitingPoissonMIMO` are the only citation keys in the chapter.
The current bibliography contains all four. Attribution is limited to
the classical cone law, the corrected square ML sufficient comparison,
and the scope of the per-decoder Hu–Lu result. No unverified novelty claim
is made for the Gaussian cone law or Student density.

## Actual local verification and integration needs

Actual commands were scoped `pwd`, `rg --files`, `rg -n`, `cat`, `sed -n`,
and `wc -l` reads of the assigned sources, evidence, and lattice path lemma;
`sha256sum` recorded the two completed TeX files for the final reviewer.
`apply_patch` wrote only the three owned files. Mathematical checks were
proof reconstruction and independent read-only review, including degree
counts, sign/KKT conditions, Student normalization, finite mixture sums,
threshold algebra, Gaussian moments, entropy loss, and conservative net
constants. No experiment, code test, symbolic check, project-wide
verification, CI status/log inspection, or literature browsing was run.
Targeted TeX compilation is reserved for root integration as instructed.

Remaining integration needs are concrete: input both owned TeX files;
retain `lattice:path` with its singleton exactness/search hypotheses;
check the four citation keys against Luna's final bibliography/locators;
perform the integrated targeted TeX build; and incorporate the independent
final chapter review. No shared macro addition is needed.
