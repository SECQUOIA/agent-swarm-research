# Author report: points

Owner files: `sections/02-points.tex` (main text, about 10 pages) and
`appendices/C-points.tex` (all proofs, about 20 pages). No other file was
edited. No experiments or historical check scripts were run, and no
literature was searched; one local read of the already-cited GLS book was
used to state its contract exactly (see "Imported contracts").

## Coverage of P1–P10

| Row | Where | Label | Status |
| --- | --- | --- | --- |
| P1 bounded fixed-degree global point theorem | main Section "Globally convex sparse polynomials", appendix proof of the corollary | `cor:points-bounded` | Stated as a corollary of P2: bounded box, `R=max{1,n rho}`, no minorant/radius steps, selector factor 2; for fixed degree, time poly(L+q). The sampled-gradient device of the old proof is superseded by coefficient rows and is not restated. |
| P2 sparse global point theorem on arbitrary polyhedra | main statement and four-step outline; appendix `app:points-global` | `thm:global-point`, `lem:points-minorant`, `lem:points-radius`, `lem:points-error` | Full proof: emptiness, Farkas unboundedness certificate normalized to `w'd=1`, attainment, explicit radius `R`, global error modulus on the whole unbounded `P`, fixed minimum-norm selector, value enclosure. All constants explicit. |
| P3 cubic convex on a polytope | main statement, transverse and slice lemmas, outline; appendix `app:points-cubic` | `thm:cubic-point`, `lem:points-cubic-transverse`, `lem:points-cubic-slice`, `lem:points-reflection` | Full proof including affine-hull reduction before Hessian positivity, rational inball, affine and zero-dimensional branches, integer-minor eigenvalue bound, original-norm selector. |
| P4 exact active bound for strongly convex cubic | main statement; appendix `app:points-boundary` | `prop:points-active` | Full construction and proof (averaging tree, sign test, treewidth, coefficient and curvature bounds). |
| P5 minimum-norm selector vs some optimizer | main statement; appendix | `prop:points-selector` | Full proof via the single amplifier. |
| P6 any-optimizer Square Root Sum | main theorem (a); appendix | `thm:points-quartic-lower`(a), `lem:points-trace` | Full proof, including trace-based equality preprocessing and removal of the aggregate constant after the unit-box map. |
| P7 any-optimizer PosSLP | main theorem (b); appendix | `thm:points-quartic-lower`(b), `lem:points-gates` | Full proof: bounded rational pairs, weighted strongly convex gate objective, `2A-1` signal, scaling by `64^-N`. No treewidth claim. |
| P8 isotropic regularization / value tolerance | main proposition; appendix | `prop:points-regularization` | Full proof. Strengthened: the point `(x*,0)` shows that every error modulus of the family has `(log Gamma)/theta >= 2^(n+2)`; this is an unconditional value-to-point separation for box-convex quartics and contrasts with `thm:cubic-point`. Sharper bound `x_n* <= 2^(-2^(n+1))`. |
| P9 conditioned path, expanded algebraic output | main proposition; appendix | `prop:points-algebraic-output` | Full proof (growth, curvature, Eisenstein irreducibility, exact support count). Correction and new part (c); see below. |
| P10 rectangular certificates | main proposition; appendix | `prop:points-rectangle` | Full proof of both formats and of the short correlated certificates. |

The synthesis is the closing subsection and `tab:points-summary`, which
lays out value, modulus, set approximation, selector, exact label, and
expanded output across the three convexity settings.

## Shared interfaces owned here

Statements are in the main section unless noted; proofs are in Appendix C.

- `lem:convex-value` (Convex value interface). (a) Polytope
  `P={Ax<=b}` inside a supplied box `[-rho,rho]^n`; `phi` continuous and
  convex on `P`; exact rational values and **subgradients** on `P` with norm
  at most `G`, `|phi|<=W`, evaluation polynomial in `Delta+<x>`. Output for any
  rational `eta>0`: emptiness, or rational `x_hat in P` (exactly feasible)
  and rational `ell` with `ell <= min phi <= phi(x_hat) <= ell+eta`, in time
  polynomial in `Delta+<eta>`. (b) Instantiation for
  `phi(x)=f(Tx+t)+tau||x||^2`, `f` explicit sparse of numerical degree `D`:
  time polynomial in `D` and the encoding lengths; the composition is
  evaluated, never expanded. Proof: affine hull by LP, rational inball,
  capped epigraph, GLS Corollary (4.2.7), homothety repair. The subgradient
  form covers Appendix J's use with a max of convex quadratics.
- `lem:integer-hoffman`. Real `A`, `T`, entry bound `C>=1`, `s` columns,
  arbitrary real right-hand sides, minor margin `mu` (every linearly
  independent family of rows has a maximal minor of absolute value at least
  `mu`): `dist(x,Z) <= (sC)^(s-1)/mu ||Tx-t||` on `Q`. Integer matrices give
  `mu=1`.
- `lem:selector`. Exponent `d>=2`, `Gamma,R>=1`, `||p||<=R`, error bound for
  gaps at most one; `tau=eps^(2d-2)/(4*8^(d-1) R^d Gamma^d)`; regularized gap
  `tau eps^2/4` gives distance `eps` to `p`. Factor 4 may be replaced by 2 if
  every optimizer has norm at most `R`. No differentiability needed.
- `lem:points-cubic-transverse`. General form for any `c`, `Lambda`,
  `rho_1>=||c-v||`, `rho_2>=||d||`:
  `(d' Hess phi(c) d)^2 <= 12 Lambda (rho_1+rho_2)^2 E`. With
  `rho_1=rho`, `rho_2=2rho` this is `108 Lambda rho^2 E`, matching the recourse
  appendix; the older `384MR^2` is implied.
- `lem:points-cubic-slice`. Kernel inclusion hypothesis; optimal set as the
  slice with rows `Hess phi(c)` and `g_c'`; estimate
  `|g_c'(u-v)| <= E + Lambda R_Omega ||Pi_K(u-v)||`.
- `lem:points-reflection` (appendix). `0 <= H(u) <= (1+1/theta) H(c)` when
  `c-theta(u-c)` stays in the set; ball case `theta=r/R`, box case `theta=1`.
- Appendix tools that others may cite: `lem:points-sparse` (evaluation and
  majorants of `f(Tx+t)+tau||x||^2`), `lem:points-interp` (interpolation
  constants), `lem:points-integer-eigen`, `lem:points-relative`
  (relative coordinates and inner ball), `lem:points-gls` (the imported GLS
  contract), `lem:points-sign-test`, `lem:points-amplifier`,
  `lem:points-trace`, `lem:points-tree`, `lem:points-gates`,
  `rem:points-tangent` (optional LP-dual lower certificate).

Other labels defined: `sec:points`, `sec:points-tools`,
`sec:points-global`, `sec:points-cubic`, `sec:points-limits`,
`sec:points-representation`, `sec:points-summary`, `tab:points-summary`,
`app:points`, `app:points-tools`, `app:points-global`, `app:points-cubic`,
`app:points-boundary`, `rem:points-expansion`, and equations
`eq:points-boundedness-lp`, `eq:points-quotient`, `eq:points-midpoint`,
`eq:points-gradient-residual`, `eq:points-cubic-taylor`,
`eq:points-amplifier-identity`.

## Labels referenced from other owners

`thm:exact-upper`, `thm:singleton-field` (shared labels), and from
Section 01: `sec:models-outputs`, `sec:models-promises`,
`def:models-value`, `def:models-points`, `def:models-predicates`,
`def:models-representations`, `lem:models-low-degree`. All exist in the
current files. If Section 01 renames them, these references must follow.

## Macros and notation

No new macro is needed. The files use existing macros (`\R`, `\Q`, `\Z`,
`\dist`, `\norm`, `\argmin`, `\diag`, `\PosSLP`) and inline
`\operatorname{...}` for `aff`, `range`, `Tr`, `int`. Transpose is
`^{\mathsf T}`, as in Section 01. Notation follows the conventions: `L`
input length, `n` dimension, `q` precision with `epsilon=2^-q`, `D`
numerical degree, `p` the minimum-norm selector, `f_*` and `S`, `Lambda`
for curvature or Lipschitz upper bounds. Locally defined symbols include
`C` and `C_N` for matrix entry bounds and `mu` for the Hoffman minor
margin; each is defined in its statement. The construction dimension in
`thm:points-quartic-lower` is written `N`.

## Citations

Existing keys used: `GroetschelLovaszSchrijver1988`,
`SlotSteurerWiedmer2025`, `AhmadiChaudhryZhang2024`, `Li2010`, `Li2013`,
`Yang2009`, `KozlovTarasovKhachiyan1980`, `EY2010`, `AhmadiHall2020`,
`AllenderEtAl2009`, `TarasovVyalyi2008`.

Proposed new key for Luna (the only checker error from these files):

```bibtex
@article{Hoffman1952,
  author  = {Hoffman, Alan J.},
  title   = {On Approximate Solutions of Systems of Linear Inequalities},
  journal = {Journal of Research of the National Bureau of Standards},
  year    = {1952},
  volume  = {49},
  number  = {4},
  pages   = {263--265}
}
```

It is cited once, for the classical Hoffman bound behind
`lem:integer-hoffman`; the lemma's explicit constant is proved in full.

## Imported contracts to vet (root and Luna)

1. GLS 1988 (book as in `references.bib`; locators from the local 1988
   text, printed pages): weak optimization problem (2.1.10), p. 50; weak
   separation problem (2.1.13), p. 51; circumscribed convex sets (2.1.16),
   p. 53; Corollary (4.2.7), p. 106 (weak optimization for circumscribed
   convex bodies from a weak separation oracle, oracle-polynomial); General
   Assumption (1.2.1) and the substitution remark, pp. 26--27, and
   Section 4.1, pp. 103--104 (composition with polynomial-time oracles).
   `lem:points-gls` states the contract; we pass the body description in
   every oracle query to make the composition rule apply verbatim. Also
   used: Section 1.4 (Gaussian elimination), Theorem (6.4.12), p. 180
   (explicit rational LP in polynomial time), and Section 6.5 (optimal and
   dual solutions).
2. `SlotSteurerWiedmer2025`: cited with "Theorem 1.1 and Corollary 1.2"
   (arXiv v1 numbering: attainment with norm of polynomially bounded
   logarithm or unboundedness; polynomial-time unboundedness detection and
   objective-gap approximation). Please confirm numbering against the
   version finally cited. The text credits these results and the structural
   decomposition, and claims only the effective modulus and fixed selector.
3. `AhmadiChaudhryZhang2024`: "proof of Lemma 5" for the tangent quadratic
   bound (sharper constant than ours).
4. `Li2010` Theorem 4.2 and Corollary 4.1; `Li2013` Theorem 1: exponent
   `1/((D-1)^n+1)`, existence of constants. `Yang2009`: no content claimed;
   the text says so explicitly and does not claim the exponent `1/D` as new.
5. `AhmadiHall2020` Theorem 2.3: strong NP-hardness of convexity of cubics
   on boxes.
6. `EY2010`: PosSLP-hardness of strong approximation of equilibrium
   coordinates (Theorem 4 per the prior-art record). `TarasovVyalyi2008`:
   arithmetic-circuit comparison to exact SDP feasibility.
   `AllenderEtAl2009`: definitions of PosSLP and Square Root Sum, SRS reduces
   to PosSLP, both in the counting hierarchy.

## Responses to `evidence/reviews/prewrite-points.md`

- Blocker 1 (global constants and value interface): resolved. The appendix
  contains the explicit minorant, `rho`/`mu_0`, `r_*`, `W_0`, `Y`-type bound,
  `R`, the interpolation constants, coefficient rows, `Gamma`, and the full
  value interface with exact feasible repair and sparse composed
  evaluation.
- Blocker 2 (cubic constants and weak output): resolved, including the
  affine and zero-dimensional branches, rational inball, original-norm
  penalty, and homothety repair.
- Blocker 3 (quartic base reductions): resolved. Both base constructions are
  proved in full, with the trace argument, tree conditioning, weighted gate
  convexity, and the coefficient and treewidth qualifications.
- Blockers 4 and 5 concern recourse and are outside this file set.
- Source-transfer cautions: the affine slope is `w=-(I-Pi) grad f(0)`, the
  Farkas direction is normalized by `w'd=1`; the lower bound on `w'x` uses
  convexity at the origin and is kept separate from the one-sided
  constraint bound; positive eigenvalues are bounded below by integer
  principal minors, not assumed rational; affine compositions are evaluated,
  never expanded (`rem:points-expansion` gives the `2^r`-monomial example);
  `lem:convex-value` assumes convexity explicitly. Global convexity is
  stated at each invariant-kernel and Bregman step.
- The output distinctions requested by the audit (value, set approximation,
  fixed selector, exact predicate, representation) are explicit and use
  Section 01's terms.

## Corrections and new derivations relative to the sources

1. **P9 is not convex on `[1,2]^n`.** The source family is uniformly
   conditioned but not convex on its box: for `n=2` at `(1,2)` the entry
   `d^2/dx_1^2` equals `-4`. The coverage map's "domain-convex" description
   is inaccurate. The proposition states part (a) without convexity and adds
   a new part (c): a box with `O(1)`-bit dyadic endpoints, computed in
   `O(n)` time, contains the optimizer and has `Hess >= I/32`. The proof
   bounds residuals by `15/128` on the box and uses
   `Hess = 2J'J + 4 diag(r)`. This makes the representation example a
   strongly convex quartic on its box.
2. **P8 strengthened** as stated in the coverage table; the source's `2^n`
   bit claim for `lambda` becomes `2^(n+2)`.
3. **Cubic transverse constant** sharpened to the general
   `12 Lambda (rho_1+rho_2)^2`; the cubic theorem uses `108 Lambda R_0^2`
   (source: `384 M R^2`). Valid for any reference point `c`.
4. **Value interface** stated with exact subgradients and an abstract
   evaluation contract, so that sparse compositions, regularized objectives,
   and Appendix J's nonsmooth max-function are covered by one statement.
   Exact feasibility uses the homothety repair for both the general and the
   cubic case.
5. **Hoffman lemma** unified with an explicit minor margin `mu`; the integer
   case is `mu=1`. The recourse appendix's `lem:recourse-hoffman` hypothesis
   (every nonzero square minor at least `mu`) implies ours.
6. P10's "globally strongly convex" in the source means on the box; the
   paper says "on X".
7. The convex-quadratic baseline and "globally convex cubics are quadratic"
   now cite `lem:models-low-degree` instead of reproving it.

## Integration notes for root

- Possible deduplication: `appendices/I-recourse.tex` proves
  `lem:recourse-hoffman` and `lem:recourse-transverse`, whose statements are
  covered by `lem:integer-hoffman`, `lem:points-cubic-transverse` (with
  `rho_1=rho`, `rho_2=2rho`), and `lem:points-cubic-slice`; only the
  two-point form of its part (b) is phrased differently (same proof). Root
  may keep their short proofs or cite ours.
- Consumers of `lem:convex-value` (Appendices A, D, I, J; Sections 03, 05,
  06, 10) use it for explicit sparse convex polynomials on boxed polyhedra,
  or, in Appendix J, for a max of convex quadratics with exact subgradients.
  Both are covered by parts (b) and (a).
- Open questions recorded in the text: whether exponent `1/3` is attainable
  for cubics with polynomial-bit constants; dependence on `log D` for binary
  exponents; arithmetic-circuit input. The paper claims none of these.

## Checks actually run

- Scratch compilation outside the repository (`/tmp/points-check`), with
  `macros.tex`, this section and appendix, a stub section defining the
  external labels, and the current `references.bib` plus a local
  `Hoffman1952` stub: `pdflatex` (three passes) and `bibtex`. Final result:
  30 pages, no LaTeX errors, no undefined references or citations, no
  overfull boxes.
- `python3 verification/check_manuscript.py` (scoped to this manuscript).
  The only error attributable to these files is
  `Missing bibliography key: Hoffman1952`; the remaining errors belong to
  other authors' files or missing inputs. No duplicate labels from these
  files.
- No experiments, no historical diagnostic scripts, no project-wide checks,
  and no CI inspection. Proof correctness rests on the written arguments;
  internal review is not external peer review.
