# Author report: conditional and integer recourse (round 1)

Author: Opus principal author for the recourse block. Date: 2026-10-05.
Files written (and only these): `sections/07-recourse.tex`,
`sections/08-integer.tex`, `appendices/E-recourse.tex`,
`appendices/F-integer.tex`, and this report. No experiment was rerun, no
literature search was made, nothing was committed, no task was delegated,
and no other author's file or historical note was edited.

## 1. What the block contains

Section 7 (`sec:rec`) presents conditional recourse as the mechanism that
reduces the effective nonconvex dimension to a supplied core: the
conditional value keeps upper coordinate curvature when residual
feasibility does not depend on the core, so the corrected-corner search and
the local count run in dimension `k`. Closure needs separate global
certificates (excluded residual slabs, then sign and Hessian tests). It
states three exact theorems and one corollary:

| Label | Content | Noise | `log2 M` | Expected work | Ordinary output |
| --- | --- | --- | --- | --- | --- |
| `thm:rec:qp` | quadratic, box-stable exact recourse | ambient | `poly(I)` | `8^k Q_ex poly(I)` | rational |
| `cor:rec:forest` | residual forest (feedback vertex set core) | ambient | `poly(I)` | same | rational |
| `thm:rec:poly` | fixed degree, box-stable certified recourse (e.g. certified residual convexity) | ambient | `poly_d(I)` | `8^k Q_ap poly_d(I)` | implicit patch |
| `thm:rec:core-only` | fixed degree, certified residual modulus `mu` | core-only | `poly_d(I)` | `8^k Q_ap poly_d(I)` | implicit patch |

with `Q_ex=[3+(1+k/2)L/(2 sigma)]^k` and `Q_ap=[3+(1+k)L/(2 sigma)]^k`
(`eq:rec:Q`). Supporting statements: `def:rec:instance`, `lem:rec:value`,
`ex:rec:feasibility`, `ex:rec:star`, `prop:rec:search`, `lem:rec:exclusion`,
`lem:rec:closure`, `def:rec:qp-oracle`, `def:rec:cert-oracle`,
`lem:rec:convex-oracle`, `prop:rec:rank`, `prop:rec:tube`,
`prop:rec:release`, `rem:rec:interior`, `ex:rec:fiber`, `ex:rec:weak`,
`ex:rec:two-sided`.

Section 8 (`sec:int`) covers integer labels, core-only flow/TU recourse,
strong-noise random components, and the low-rank lattice theorem:

| Label | Content | Noise | `log2 M` | Expected work | Output (every draw) |
| --- | --- | --- | --- | --- | --- |
| `thm:int:solver` | deterministic constant-base box solver, common-root output | none | none | `c_d^k poly_d(H)` | algebraic |
| `thm:int:native` | native integer recourse, competing-label certificate | ambient | `poly_d(I)` | `[8^k Q_ex + c_d^k] poly_d(I)` | label + algebraic core, length `c_d^k poly_d(I)` |
| `cor:int:native-implicit` | same, implicit core patch | ambient | `poly_d(I)` | `8^k Q_ex poly_d(I)` | label + patch |
| `thm:int:flow-interior` | convex integer flows, all optimal cores interior | core-only | `poly_d(I)` | `[8^k Q_ex + c_d^k] poly_d(I)` | flow + algebraic core |
| `thm:int:face` | deterministic optimal-face certificate | none | none | exact tests | certificate |
| `thm:int:flow-boundary` | convex integer flows, arbitrary core faces | core-only | `f_d(k) poly_d(I)` | `f_d(k) Q_ex poly_d(I)` | flow + algebraic core |
| `cor:int:bilinear` | bilinear coupling | core-only | `poly_d(I)` | `[8^k Q_ex + c_d^k] poly_d(I)` | flow + algebraic core |
| `thm:int:tu`, `cor:int:tu-ineq` | totally unimodular equalities/inequalities | core-only | as for flows | as for flows | label + algebraic core |
| `thm:int:strong-field` | strong fields, random components, mixed boxes | ambient, strong | any | `poly_d(I+log M)[1+sum a_i q_i/(1-4 Delta_+ beta)]` | component output |
| `thm:int:lowrank` | separable integer quartics minus low-rank concave part | aligned | `poly(I)` | `8^k H_rat poly(I)` | rational, no fallback |

Supporting statements: `cor:int:mixed-solver`, `def:int:native`,
`prop:int:hs`, `lem:int:potentials`, `lem:int:proximity`. Proofs:
Appendix E (`app:rec`, 876 lines) and Appendix F (`app:int`, 996 lines).
In a scratch build with stubs for unwritten chapters, Section 7 occupies
pages 59-67, Section 8 pages 68-76, Appendix E pages 123-133, and
Appendix F pages 134-146.

Every theorem states the noise location and law (ambient, core-only,
aligned; `U_{sigma,M}` with a base-computed power of two `M`), the sampler
order (fallback factor, thresholds, level, grid), the output on ordinary
and exceptional draws, the numerical parameters that enter outside bit
length (`L/sigma`; `alpha w_i/sigma_i`; the strong-field `q_i`), the degree
and representation (explicit monomials, fixed `d`), and the status of each
premise (verified, certified, or promised, per `sec:model:input`).

## 2. Development-to-label map

Source paths are relative to `research-20261002/new-direction/`.

| Source development | Manuscript location | Treatment |
| --- | --- | --- |
| `local-error-recourse-interface.md` §1 (nonconvex star), §5 (positive definite star) | `ex:rec:star`, its paragraph after, proof in `app:rec:examples` | Included as the motivation for exact or certified conditional values; numbers rechecked exactly. Section 9 (`prop:lim:local`) reuses this example. |
| same, §2-3 (sufficient conditional interface, count (11)) | discussion around `prop:rec:search` | Not stated as a theorem: it is a sufficient interface, not an algorithm. |
| `smoothed-box-stable-recourse.md` | `def:rec:qp-oracle`, `thm:rec:qp`, `lem:rec:exclusion`, `lem:rec:closure`(a),(c), `cor:rec:forest`, `app:rec:main` | Included; closure test weakened to PSD for soundness (the good event gives `>= 2g_0`); fallback via `lem:sp:faces`. |
| `smoothed-polynomial-box-recourse.md` | `def:rec:cert-oracle`, `lem:rec:convex-oracle`, `thm:rec:poly`, `lem:rec:closure`(b), `lem:app:rec:stopping` | Included, including the `k=0` convention and the tangent certificate `eq:rec:tangent`. |
| `polynomial-recourse-rank-separation.md` | `prop:rec:rank` and the `t log t` remark, proved in `app:rec:main` | Included with its stated scope (fixed quadratic correctors only). |
| `core-only-noise-strong-recourse.md` | `rem:rec:interior`; growth lift `lem:app:rec:lift`(c); core-gradient tail `lem:app:rec:core-tails`(b) | Presented as the explanatory special case of the changing-face theorem, per Sol §3. |
| `core-only-noise-boundary-recourse.md` | `thm:rec:core-only`, `app:rec:core-only` | Included; constants of the source kept (`rho=1/(6B)`, `g_*`, `r`, `theta`, `nu`). |
| `core-noise-active-stratum-tube.md` | `prop:rec:tube`(a)-(c) | Included with full proof; exponent of the elimination format written as `a(N+1)^3` (source `a(N+1)^4`; both valid). |
| `small-residual-multiplier-curvature.md` | `prop:rec:release`, `ex:rec:two-sided` | Included; uses the sharper `B_3=K_3`. |
| `core-only-noise-rotating-fiber.md` (both variants) | `ex:rec:fiber` | Included, with the strictly convex variant stated explicitly. |
| tube note §6 example (18) | `ex:rec:weak` (coupled variant) | Included, plus the decoupled example with identically zero multiplier. |
| `smoothed-native-integer-recourse.md` | `def:int:native`, `thm:int:native`, `lem:int:label`, `lem:int:native-stop`, `prop:int:hs`, `lem:int:potentials` | Included with the current common-root completion. |
| `native-integer-recourse-implicit-closure.md` | `cor:int:native-implicit` | Included; old `A_d(k)` notation replaced by `c_d^k` (Sol §4). |
| `polynomial-component-primitive-limit.md` (the requested "joint critical-limit coordinate solver"; no file of the requested name exists) | `thm:int:solver`, `cor:int:mixed-solver`, `lem:int:quotient`, `lem:int:triangular`, `lem:int:leading`, `lem:int:recovery`, `lem:int:limits`, `lem:int:forms`, `lem:int:values`, `lem:int:cost` | Full proof written anew (see §3). No novelty claim (root decision 1). |
| `strong-field-component-polynomial.md` §7 | `lem:int:budget` | Included as an explicit loose ledger. |
| `strong-field-component-polynomial.md` §1-6, `strong-field-component-qp.md` | `thm:int:strong-field` | One theorem with the QP case (`a_i=3`, rational output) and the polynomial case (`a_i=c_d`, component output). |
| `smoothed-interior-core-flow.md` | `thm:int:flow-interior`, `def:int:charts` | Included; only original residual arcs are tested (source arcs only build the tree). |
| `core-only-flow-boundary-obstruction.md` | cited as `prop:lim:flow` (owned by Section 9) and summarized in `sec:int:flows` | Not duplicated, per the architecture's assignment of X6 to Section 9. |
| `flow-optimal-face-certificate.md` | `thm:int:face`, `lem:int:face-general`, `lem:int:proximity` | Included; unified with the TU case through multiplier maps. |
| `smoothed-boundary-core-flow.md` | `thm:int:flow-boundary`, `lem:int:margin`, `lem:int:normal` | Included with parameter-dependent sampling precision kept explicit. |
| `smoothed-bilinear-core-flow.md` | `cor:int:bilinear`, `lem:int:affine-margin` | Included. |
| `smoothed-core-tu-recourse.md` | `thm:int:tu`, `cor:int:tu-ineq`, `lem:int:tu-dual`, TU proof of `lem:int:proximity` | Included. |
| `smoothed-integer-low-rank.md` | `thm:int:lowrank` | Included; search and count now cited to the counting chapter. |

Deliberately not included: `approximate-convex-recourse.md` (a
growth-conditional antecedent superseded by `thm:rec:poly`);
`polynomial-exact-fallback-construction.md` (superseded for component work
by the solver; the general fallback is `thm:count:fallback`, owned by the
counting author); core-only value-oracle notes (their output contract
belongs to the exact-arithmetic companion; see §5).

## 3. Corrections and new work relative to the sources

1. **Joint critical-limit solver: a complete proof without analytic
   Puiseux convergence.** The source argued with convergent branch
   expansions and a "locally constant leading power". The manuscript
   proof (`app:int:solver`) uses: the formal Puiseux field only for
   valuations (`lem:int:leading`); simultaneous triangularization of the
   commuting multiplication matrices to obtain joint eigenvalues that are
   common zeros, so Stickelberger's multiplicity theorem is not needed
   (`lem:int:triangular`); an elementary limit argument showing that limits
   of real critical points of the deformed face problems are among the
   bounded limits, using only the polynomial identity of
   `lem:int:leading` and Zariski density (`lem:int:limits`); and reality of a
   recovered limit read directly from the rational maps `B_i/A`
   (`lem:int:recovery`), with no conjugation argument. The identity
   `c_m = 0` for `m > kappa` is proved as a polynomial identity in the form
   coefficients, which justifies differentiating before specializing.
   Bad forms are handled by the explicit skip tests of step (3) and are
   harmless because every kept point lies in the box.
2. **Release of small multipliers.** The two-sided Taylor argument now
   handles the endpoint case `t* = eta` by a limit, and the multiplier
   Hessian bound uses `B_3 = K_3` with the row-sum justification in
   `eq:app:rec:hessvar`.
3. **Core-only projected-growth tail.** Obtained directly from
   `lem:count:finite-tails`(b), whose statement already perturbs a subset of
   variables of a reduced objective; no separate formula is needed. The
   core-gradient tail under core-only noise (`lem:app:rec:core-tails`(b)) is
   proved separately because `lem:count:finite-tails`(d) assumes ambient
   noise.
4. **Core search in two modes.** One proof covers exact and certified
   conditional values with the incumbent taken over the current level; the
   count is `thm:count:local` applied conditionally on residual noise.
   Correctness holds for every admissible oracle answer.
5. **Flows and TU in one argument.** `lem:int:face-general` states the face
   certificate for any polynomial multiplier map, and `lem:int:proximity` is
   proved once by conformal TU circuits, with networks as a special case.
6. **Interior flow test.** Only original residual arcs are tested; the
   chart family is the same as for the boundary theorem. This follows Sol's
   remark that artificial source-arc inequalities are unnecessary.
7. **Exceptional outputs** of `thm:rec:poly` and `thm:rec:core-only` are
   described as the root representations of `thm:count:fallback` (one
   canonical minimizer), not as common-root algebraic output.
8. **Fallback budgets made explicit**: `B=3^n` for the quadratic recourse
   theorem, `B=max{2, N_Z C_d c_d^k}` (or `N_Z 3^k`) for native labels.
9. **No duplication of other chapters**: corrected corners, local counts,
   meshes and the corrected-corner search are cited from the counting
   chapter; patch evaluation, quadratic face enumeration and the
   nonsingular-zero bound are cited from Appendix C (`lem:sp:gls`,
   `lem:sp:faces`, `lem:sp:bezout`); the flow obstruction is cited from
   Section 9 (`prop:lim:flow`).
10. **Credit for classical mechanisms**: the solver paragraph credits the
    rational univariate representation and critical-point deformations and
    disclaims a new general algebraic complexity result (root decision 1 and
    the root's literature note).

No source result was found false. Sol's preliminary contracts are all
reflected: the solver has a full proof; component output keeps one root per
component and promises no sign test for sums; the three sampling-bit
regimes are kept separate; residual multipliers may vanish and strict
complementarity is never assumed; cost-only coupling with fixed residual
feasibility is a stated restriction, illustrated by `ex:rec:feasibility`;
oracle definitions require every residual subbox or tightened integer
interval.

## 4. Proof dependencies

- `thm:rec:qp`: `lem:rec:value` -> `eq:rec:corner` (`lem:count:rounding`) ->
  `prop:rec:search` (`thm:count:local`) -> `lem:rec:exclusion` ->
  `lem:rec:closure`(a),(c) -> `lem:app:rec:stopping` ->
  `thm:count:growth-tail`, `lem:count:finite-tails`(b),(d) -> fallback
  `lem:sp:faces` -> `lem:count:rare-fallback`(a); exact convex QP (KTK).
- `cor:rec:forest`: `thm:rec:qp` + Del Pia and Khajavirad, Theorem 1 and
  Lemma 19.
- `thm:rec:poly`: as above with `lem:rec:convex-oracle` (`lem:sp:gls` +
  tangent bound), `lem:rec:closure`(b), and fallback `thm:count:fallback`.
- `thm:rec:core-only`: `lem:app:rec:lift`, `lem:app:rec:core-tails`
  (`lem:count:finite-tails`(b), `lem:sp:bezout`), `prop:rec:tube`
  (Renegar's fixed-block elimination; Basu-Lerario tube; dimension theory
  of semialgebraic sets), `prop:rec:release`, and the `thm:rec:poly` chain.
- `thm:int:solver`: `lem:int:quotient` (Buchberger's first criterion),
  `lem:int:triangular` (simultaneous triangularization; Puiseux field
  algebraically closed), `lem:int:leading`, `lem:int:recovery`,
  `lem:int:limits`, `lem:int:forms`, `lem:int:values`, `lem:int:cost`,
  `lem:int:budget` (univariate algorithms).
- `thm:int:native`: `prop:rec:search`, `lem:int:label`,
  `lem:int:native-stop`, `thm:int:solver`, `cor:int:mixed-solver`,
  `lem:count:finite-tails`(b), `lem:count:rare-fallback`(a).
- `cor:int:native-implicit`: additionally `lem:rec:closure`,
  `lem:sp:bezout`, `lem:sp:gls`.
- `prop:int:hs`: Hochbaum-Shanthikumar Algorithm 4.2 and Theorem 4.3; exact
  LP extreme points (GLS).
- `thm:int:flow-interior`: `def:int:charts`, `lem:int:potentials`,
  `thm:int:solver`, Renegar format bound, grid tube from the proof of
  `prop:rec:tube`(c), `lem:count:finite-tails`(b), label fallback.
- `thm:int:face`: `lem:int:potentials`, `lem:int:proximity`,
  `lem:int:face-general`, `prop:int:hs`, `thm:int:solver`.
- `thm:int:flow-boundary`: `thm:int:face`, `lem:int:margin` (Renegar with
  coefficient heights; reciprocal Cauchy bound), `lem:int:normal`, tube,
  growth tail, label fallback. `cor:int:bilinear`: `lem:int:affine-margin`.
- `thm:int:tu`: `lem:int:tu-dual` (interpolation, TU integrality, LP
  duality, TU inverse entries), `lem:int:proximity`, `lem:int:face-general`.
- `thm:int:strong-field`: `cor:int:mixed-solver` or `lem:sp:faces`;
  connected-set counting proved in place.
- `thm:int:lowrank`: `thm:count:cells`, `def:count:mesh`,
  `cor:count:levels`, scalar convex integer recourse, objective lattice.

## 5. Interfaces with other chapters and items for the root

Labels used from other owners, all resolving in the current sources:
`thm:count:local`, `lem:count:rounding`, `thm:count:cells`,
`cor:count:levels`, `def:count:mesh`, `thm:count:growth-tail`,
`lem:count:finite-tails`, `thm:count:fallback`, `lem:count:rare-fallback`,
`sec:count`, `lem:sp:gls`, `lem:sp:bezout`, `lem:sp:faces`,
`prop:lim:flow`, `def:model:outputs` (items `implicit`, `algebraic`,
`component`), `def:model:perturbation`, `prop:model:regret`,
`eq:model:interval`, `sec:model:input`, `sec:model:algorithms`.
Section 9 already cites `ex:rec:star`, `ex:rec:feasibility`,
`ex:rec:fiber`, `prop:rec:rank`, `thm:rec:poly`, `thm:rec:core-only`.

Items requiring a root decision:

1. **`c_d` clash.** `thm:count:fallback` uses `c_d` as a polynomial
   exponent; this block uses `c_d` as the solver's constant base
   (`c_d^k`), as in all sources and Sol's audit. Suggest renaming the
   counting chapter's exponent (for example `e_d`).
2. **Algebraic output and fallback output.** `def:model:outputs`(c)
   requires one common root for all coordinates. `thm:count:fallback`
   returns separate root representations of the coordinates of one
   canonical minimizer. My theorems describe their exceptional outputs
   exactly that way. The model's sentence that fallback draws return
   "algebraic outputs" may need rewording, or `thm:count:fallback` may be
   described as its own format.
3. **Grid-law symbol.** The model writes `U_{sigma,M}`, the counting
   chapter `\mathcal U_{sigma,M}`. I followed the model.
4. **Citation keys.** I used literature-KB slugs, matching the counting
   chapter. The introduction cites `BasuLerario2023`, which differs from the
   KB slug `basu2023-hausdorff-approximations-and-volume-of` used here.
5. **Companion manuscript.** Per root decision 8, the overlap with the
   exact-arithmetic companion (see §6) should be stated where the
   introduction or discussion compares sibling work. My sections do not
   cite the companion.
6. **`lem:int:budget`.** Its proof relies on a stated per-call bound
   `A(l+2)^100` for fixed elementary routines (schoolbook arithmetic,
   Bareiss, interpolation, subresultants, Sturm sequences) without
   itemizing each routine. The bound is very loose, but a reviewer may ask
   for one sentence or citation per routine. The theorems need some explicit
   computable base `c_d` because it enters the noise law of
   `thm:int:strong-field` and the fallback factor `B` of the native and flow
   theorems; any proved smaller base can replace `2^{10000 D}`.

No macro additions are requested.

## 6. Overlap with the exact-arithmetic companion

The exact-arithmetic manuscript (`paper-exact-arithmetic`, Section 10 and
Appendix I) belongs to the same broader research program. It treats
core-only noise with Cauchy-name outputs for the optimal value and the
lexicographically least optimal core, on product boxes with residual
convexity and on coupled polytopes with a supplied convexifier; full
selected points under a convexifier or for residual-convex cubics; an
all-scale count `k^{O(k)}(1+kappa/sigma)^k`; block-elimination section
transfer; and an exact two-block fallback with a base-only factor.

Shared foundations, reproduced here self-containedly through the counting
chapter and Appendix E: conditional values with upper coordinate curvature
on fixed residual sets, corrected-corner cell bounds, growth tails and
finite-law transfer, and same-draw fallback with a base-only factor. The
new emphasis of this block is exact termination on every draw (rational,
implicit-patch, and common-root algebraic outputs) through excluded-slab
containment and competing-label or optimal-face certificates; native
integer recourse; core-only flow and TU recourse; strong-noise random
components; and the low-rank lattice theorem. The selectors differ: this
block promises no canonical (lexicographic or minimum-norm) selection.
`thm:rec:core-only` requires a uniform residual modulus, while the
companion's value/core theorem tolerates flat residual fibers; the
contracts are compatible but different.

## 7. Bibliographic identities used (for Luna and the root)

| Key | Identity | Use and locator to verify |
| --- | --- | --- |
| `basu2006-algorithms-in-real-algebraic-geometry` | Basu, Pollack, Roy, *Algorithms in Real Algebraic Geometry*, 2nd ed., Springer, 2006 | Semialgebraic sets with empty interior have lower dimension; semialgebraic maps do not raise dimension; the field of Puiseux series over an algebraically closed field of characteristic zero is algebraically closed; critical-point deformations; univariate isolation, sign determination, refinement. Exact theorem numbers to be supplied. |
| `basu2023-hausdorff-approximations-and-volume-of` | Basu, Lerario, Hausdorff approximations and volume of tubes of singular algebraic sets, *Math. Ann.* 387 (2023) 79-109 | Theorem 1.1 (tube bound with dimension bound). |
| `cox2015-ideals-varieties-and-algorithms` | Cox, Little, O'Shea, *Ideals, Varieties, and Algorithms*, 4th ed., Springer, 2015 | Buchberger's first criterion; standard monomials form a basis of the quotient. **Not in the KB; please ingest and give locators.** |
| `grotschel1988-geometric-algorithms-and-combinatorial-optimization` | Groetschel, Lovasz, Schrijver, *Geometric Algorithms and Combinatorial Optimization*, Springer, 1988 | Definition 2.1.10, Theorem 4.2.2, Corollary 4.2.7 (weak optimization); exact LP with an optimal vertex (locator to supply). |
| `hochbaum1990-convex-separable-optimization-is-not` | Hochbaum, Shanthikumar, Convex separable optimization is not much harder than linear optimization, *J. ACM* 37(4) (1990) 843-862 | Algorithm 4.2 and Theorem 4.3 (TU case, printed p. 858); requires optimal extreme-point LP solutions. |
| `horn2013-matrix-analysis` | Horn, Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013 | Simultaneous triangularization of commuting matrices (Theorem 2.3.3 in that edition, to verify). **Not in the KB; please ingest.** |
| `kozlov1980-the-polynomial-solvability-of-convex` | Kozlov, Tarasov, Khachiyan, The polynomial solvability of convex quadratic programming, *USSR Comput. Math. Math. Phys.* 20(5) (1980) 223-228 | Exact rational convex QP. |
| `mehlhorn2015-from-approximate-factorization-to-root` | Mehlhorn, Sagraloff, Wang, From approximate factorization to root isolation with application to cylindrical algebraic decomposition, *J. Symbolic Comput.* 66 (2015) | Polynomial-time root isolation and refinement (used together with BPR). |
| `pia2026-treewidth-and-the-complexity-of` | Del Pia, Khajavirad, Treewidth and the complexity of box-constrained quadratic programs, arXiv:2609.35595 (2026) | Theorem 1 (forest case, strongly polynomial, Turing model) and Lemma 19 (rational optimum of polynomial length); strong NP-hardness at treewidth two. |
| `renegar1992-on-the-computational-complexity-and` | Renegar, On the computational complexity and geometry of the first-order theory of the reals, Part III, *J. Symbolic Comput.* 13(3) (1992) 329-352 | Theorem 1.1 (format, degree, and coefficient-height bounds; printed p. 330), also restated as `thm:count:renegar`. |
| `rouillier1999-solving-zero-dimensional-systems-through` | Rouillier, Solving zero-dimensional systems through the rational univariate representation, *AAECC* 9 (1999) 433-461 | Credit for recovering coordinates from one univariate polynomial. |

The proofs use only these statements; no other external result is
assumed. Classical facts proved in place: Cauchy root bounds, TU inverse
entries and conformal circuits, connected-set counting, marginal-potential
flow optimality.

## 8. Checks actually run

All checks are local and targeted; none is a CI result and none reruns a
saved optimization experiment.

1. Scratch build. The paper sources were copied to `/tmp/rec-build`, empty
   stubs were added for chapters not yet written by other authors
   (`04-quadratic`, `06-constraints`, `10-discussion`, `B-quadratic`,
   `D-constraints`), and `pdflatex -interaction=nonstopmode main.tex` was
   run twice. Result: exit status 0, 153 pages, no LaTeX errors, no
   undefined references, no multiply defined labels, and, after fixes, no
   overfull boxes attributed to my four files. The only warnings from my
   files are undefined citations, because `references.bib` (root-owned)
   does not exist yet.
2. `python3 -I verification/check_sources.py` on the scratch copy. Result:
   only "Undefined citation" lines (43 keys across the paper, the bib file
   not yet existing); no unfinished-text, internal-path, environment, label,
   or reference errors.
3. Exact solver diagnostic `/tmp/rec-diag/solver_check.py` (SymPy),
   implementing steps (1)-(4) of `app:int:solver` literally, including the
   signs `chi_i = -d/du det(TI - X_lambda - u X_i)` and the degree and
   divisibility skips. For `y1^3-3y1+y2^2` (degree 3, `D=4`, `N=9`) every
   good form recovers exactly the two critical limits `(1,0)` and
   `(-1,0)`; the form `t=0` has lower `z`-degree (3 instead of 5), as the
   theory predicts for a form that annihilates a leading pole, and adds no
   spurious point. For `y1^2 y2`, whose critical set is positive
   dimensional, the only bounded limit recovered is `(0,0)`. The
   multiplication matrices commute. Result: pass.
4. Exact example diagnostic `/tmp/rec-diag/examples_check.py` (Fractions
   and SymPy): the star values `0, 23/32, 31/16`, min-marginal `23/32`,
   budgets `1/8` and `33/16`, and `V_h-V`; the positive definite star
   formulas for `d` in {8, 9, 16, 64}, including `q_C-U>=1/8` and the
   variation `-(d-1)h^2`, and the eigenvalues `3 +- sqrt5`; the corner
   distances `h/3, 2h/3` of `ex:rec:feasibility` for levels 1-24; the
   rank-separation gradients `4(e_i+1)`, `det(I+11^T)=m+1`, and the Euler
   identity `grad P^T (Hess P)^{-1} grad P = 4P/3`; the Hessian identities of
   both fiber examples; and the determinant in `ex:rec:two-sided`. Result:
   pass.

Diagnostics 3 and 4 support the stated formulas on small instances; the
general statements rest on the written proofs.
