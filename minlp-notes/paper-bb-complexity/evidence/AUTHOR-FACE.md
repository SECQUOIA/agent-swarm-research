# Box-face and RLCT chapter evidence

Status: complete mathematical draft saved on 2026-10-05. The root assigned
this Sol fallback after the writing-model limit. Ownership is restricted
to `sections/face-exact.tex`, `appendices/face-proofs.tex`, and this report.
The root confirmed that McCormick matching, transversality, centroid,
fractional-cover, and aligned-certificate tools belong to the geometry
author, and that the decomposition comparison belongs to its separate
author. None of those proofs is duplicated here.

## Main statements and their scope

| Manuscript label | Statement and hypotheses | Complete proof |
|---|---|---|
| `face:thm:characterization` | Unconstrained positive-width compact box; C1,1 objective; fixed strictly positive coefficients alpha_i; f+sum alpha_i x_i^2 convex; exact separable alphaBB oracle. N_cover, N_rect, N_tree, and total dyadic nodes are each comparable, with fixed-instance constants, to 1+sum of all positive-dimensional root-face integrals. The full root box is included. | `app:face:lower-bound`, `app:face:projection`, `app:face:characterization` |
| `face:eq:lower-explicit` | Weighted per-face cover bound d^(d/2)sqrt(prod_{free i} alpha_i)/pi^d times I_F. Also valid for measurable owned parts satisfying pointwise validity. | `face:eq:one-box-integral` and the following summation |
| `face:rem:gap-scope` | Extension from exact alphaBB to a positive lower scalar quadratic gap and a vertex-vanishing pointwise upper gap; owned event lower bounds retain their specified event/evaluation cost, without implying a raw valid-box cover. | Same per-box integration and packing proof; upper uses the witness consequence of the upper error only |
| `face:lem:analytic-integral` | Nonzero nonnegative analytic restriction with a zero, and supplied Laplace asymptotic. All three regimes and exact leading integral constants: lambda<a, lambda=a, lambda>a. | Main text, gamma-transform/Tonelli, dominated convergence, direct logarithmic integral comparison, monotone convergence |
| `face:cor:analytic-rate` | Analytic f near D. Maximum over positive-dimensional faces of the corresponding rates. Positive-minimum faces and identically-zero faces are distinct elementary cases. | Main text after the rate definition |
| `face:prop:full-box` | Full-box integral suffices if every minimizer is interior, or if m is nonnegative on a fixed neighborhood beyond D with Lipschitz gradient there. | Main text for interior case; `app:face:full-box` for external nonnegativity |
| `face:cor:interior` | Analytic interior minimizers: lambda<=n/2; equality iff every Hessian is positive definite; then finitely many minima, theta=1, logarithmic rate, explicit leading integral constant. | Main text, null-direction anisotropic sublevel and elementary local Laplace proof |
| `face:ex:quartic` | Isolated x^4 minimum has eps^(-1/4) complexity under the specified positive-gap oracle despite zero-dimensional optimal set. | Direct integral rescaling |
| `face:ex:product` | x^2y^2 gives eps^(-1/2)log(1/eps), with RLCT (1/2,2). | Exact sublevel area, exact zeta function, direct regularized-integral evaluation |
| `face:ex:boundary` | Four-dimensional x(1-x)+y^4+z^4+w^4 on the specified cube: full integral gives eps^(-1/4), but x=0 face gives and governs eps^(-3/4). | Direct Laplace factorization and classification of all other proper faces |

The upper construction uses a fixed optimal incumbent and counts ideal
certification after its discovery. The three spatial certificate minima
are separate quantities. A dyadic tree has fixed branching degree and a
binary realization; its total nodes are compared to leaf minima through
these constructions rather than identified with them. Strictly positive
gap coefficients are substantive: zero correction for a convex objective
can make the root exact.

## Source and proof map

The main mathematical source is
`research-20260929/rlct/rlct-node-complexity.md`, revised through the
2026-09-30 root wording edits. Its source hash at authoring was
`b97b76ede580b4054349d689fe9e94cc6927bd11fecba9cbc0a4c9417b57ea7a`.

| Source location | Manuscript use | Development or correction |
|---|---|---|
| Setting, Sections 2.1–2.2 | Intrinsic face RLCT and analytic integral regimes | Cite the primary Lin input supplied by Luna; prove gamma-transform evaluation in the manuscript; do not use an RLCT pair for an identically-zero face |
| Theorem 3.1 | Per-face arcsine lower bound | Give the simple weighted coefficient constant directly; handle degenerate intersections by zero intrinsic measure; include measurable owned-set form |
| Lemma 3.2 | Box-only face projection and relative fatness | Keep explicit available length-s steps; do not assert the unconstrained gradient inequality from nonnegativity only on a closed box |
| Theorem 3.3, Lemma 3.3a, Corollary 3.4 | Dyadic packing, vertex absorption, characterization | Use separate cover/partition/tree minima; use 8^n as a safe closed-grid packing constant; use log_+ throughout corner counting; retain finite counts instead of potentially negative nonoptimal-vertex logarithmic displays |
| Proposition 3.6 | Full-integral dominance under external nonnegativity | Give a complete intrinsic-volume packing and layer-cake proof; ensure cube side fits root box and descent step fits the fixed neighborhood |
| Theorem 4.1, Corollary 4.2 | All facewise analytic regimes and interior simplification | Critical regime has log^theta, not log^(theta−1); zero and positive faces separately stated |
| Lemma 2.4 | Interior equality iff nondegenerate | Complete null-direction volume estimate and local Gaussian rescaling argument |
| Example 4.3(a) | Substantive boundary counterexample | Use direct analytic Laplace factorization; no archived numerical quantities or experiment reruns needed |
| Section 5 product example | Singular crossing illustration | Supply exact zeta and direct integral formula, avoiding dependence on a Newton-polyhedron theorem |

The bb-complexity source family is accounted for through the full
`AUDIT-SPATIAL.md` map: root-face lower bounds are the unconstrained
coordinate-stratum arcsine case of the constrained geometry note. Event
ownership and run-cost statements remain owned by the certificate and
geometry author. McCormick results from the spatial-face-exact note are
also owned by that author and are explicitly distinguished in the final
paragraph of this chapter.

## Independent findings incorporated

Read and incorporated `BRIEF.md`, `AUTHORING-CONVENTIONS.md`,
`ARCHITECTURE-DECISION.md`, the full `AUDIT-SPATIAL.md`, the relevant
`ARCHITECTURE.md` scope/proof entries, `INCOMING-AUDITS.md`, and `ISSUES.md`.
The spatial audit hash was
`bc843fa7d9ed6247f2b8643ca327d3c814544fae0a07d4ed3212740425e103d4`.
The latest incoming-audit and literature-key files were reread after the
chapter was saved. `LITERATURE.md` and a dedicated final face review file
were not present at that inspection.

The source second recheck
`research-20260929/reviews/rlct-recheck2.md` was read. Its concrete verified
boundary example and vertex proof inform the chapter; no source numerical
claims are repeated. The manuscript also fixes the unsafe negative
intermediate logarithmic displays noted in the audit and fresh check.

A separate child mathematical check, `face_math_check`, independently
confirmed the projection/fatness proof, geometric-series summation,
corner absorption, and all three gamma-transform constants. It identified
the log_+ need for both optimal and nonoptimal vertex displays and warned
that box-only nonnegativity does not by itself imply
|grad m|^2<=2Mm at every interior point. Both points are addressed: the
chapter retains explicit step lengths, and its classical gradient bound
appears only in the externally nonnegative neighborhood proof.

The root's independent final face/decomposition reviewer reported no
substantive defect in the first saved chapter. Its optional clarification
about a corner witness on a far grid boundary was addressed directly:
the all-coordinate one-sided estimate applies with distances at most s,
because the opposite length-s steps fit when 2s<=s0. The latest appendix
contains that explicit argument; the reviewer has been notified of its
new hash.

## Qualified and excluded claims

- GEO-2 is resolved locally by distinct minima and cover-lower/tree-upper
  reasoning. No arbitrary partition is assumed to be a tree without
  refinement.
- FACE-1 is resolved with all positive-dimensional faces, equality's extra
  logarithm, positive-minimum and identically-zero cases.
- GEO-5 is respected: no half-dimensional rule is applied to an isolated
  degenerate minimum; x^4 is an explicit counterexample without quadratic
  growth.
- A general McCormick characterization is not claimed. This chapter's
  theorem uses a strictly positive vertex quadratic gap, which McCormick
  gaps need not satisfy.
- The critical-face non-governance question is unnecessary to the theorem
  and is not promoted from a sketch to a result.
- Newton-polyhedron generalities, reduced-rank learning-coefficient
  formulas, noisy two-regime conjectures, and higher-order relaxation
  extensions are not included in this focused chapter. No external
  coefficient formula is imported without an audited primary source.
- Integral leading constants are not claimed as exact limiting tree-count
  constants. Dimension-dependent constants need not be small.

## Literature dependency

The only current citation is `lin2017LearningCoefficient`, present in the
verified starter `references.bib`. Use is restricted to its compact
semianalytic Laplace/RLCT theorem, Section 2, Theorem 2.10, and the
boundary treatment confirmed by Luna's reading of Lemma 2.4. On each face,
the domain is intrinsic, compact, full-dimensional in its affine hull,
with affine analytic boundary inequalities and density one. The function
is nonnegative only on that domain; sign changes outside it cause no gap
in the cited application. All B&B conclusions and integral evaluations
have manuscript proofs.

No literature search or browsing was performed by this writer. No claim
of novelty is inferred from an unsuccessful search. The literature lead
may add historical context or an alphaBB-origin reference at integration;
that is not a mathematical dependency of the stated definition and proof.

## Targeted verification actually run

Read-only targeted commands included `cat AGENTS.md`; `rg --files
paper-bb-complexity`; `cat` and `sed -n` on the named conventions, audits,
source theorem sections, source second recheck, and starter bibliography;
`rg -n` on face/RLCT architecture entries and the two owned TeX files;
and `sha256sum` on the owned TeX files and core source/audit files.

One inline `python3 - <<'PY'` source check read only
`sections/face-exact.tex`, `appendices/face-proofs.tex`, and
`references.bib`. It checked balanced unescaped braces, nested
begin/end environments, duplicate labels, missing local references, and
missing cited bibliography keys. Result before the final prose-only
corner clarification: both files balanced, 43 unique labels, no missing
local reference, no duplicate label, and no missing citation key.
After the final corner clarification, a second scoped inline Python check
confirmed balanced braces, nested environments, unique labels, and
resolved local references in the final files, still with 43 labels.
The root will perform the targeted integrated LaTeX build.

No experiment, numerical computation script, project-wide verification,
CI inspection, or commit was performed. No CI result is asserted.

## Remaining integration requests

1. Build the integrated manuscript and review page layout. The two owned
   files use only the standard packages, environments, and macros from
   `macros.tex`; no shared macro addition is requested.
2. Retain the scope distinction in the framing: exact separable alphaBB is
   the main theorem model; `face:rem:gap-scope` states the broader
   positive-lower-gap/vertex-upper-error extension. McCormick has separate
   geometry theorems.
3. Link the owned-event remark to the final certificate-accounting label
   if useful. The remark currently uses prose and imposes no unresolved
   cross-label dependency.
4. Incorporate the final independent review status when its evidence
   record is saved. Current section hash:
   `ca5a8cd2b6092503a706f96fc35b721b8e6c51fb2f402bba7f7558ef4530ae5f`.
   Current appendix hash:
   `f10db89fc908a85a3e93d60f78558ba5050e9256e7f46fc6bfc5068ed350630e`.

There is no outstanding mathematical assumption or proof blocker in the
selected chapter.
