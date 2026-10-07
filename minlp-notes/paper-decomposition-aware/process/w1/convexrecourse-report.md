# Cluster report: convex recourse and the negative-curvature target

Key: `convexrecourse`. Sources reviewed: `document/main.tex`; `document/extensions.tex` subsections "Negative curvature", "A complete reduction for certified affine convex recourse", the value-factor paragraph, and "Local pieces can preserve curvature cancellation"; the companion notes on affine convex recourse, affine-selector recognition, sparse convex value factors, piecewise curvature (with reviews), completion recourse notes, and `research-20261002/new-direction/negative-curvature-sparse.md`.

Outputs:

- `convexrecourse-proofs.tex`: self-contained statements and proofs. It compiles in a test wrapper with no errors or overfull boxes; the only undefined references are main-text labels and citations.
- `checks/convexrecourse_*.py`: exact-arithmetic checks, listed at the end.

## 1. Verdict

**Sound with fixes.** Every mathematical claim in the cluster survived a line-by-line re-derivation. No claim is false. The fixes fall into three groups:

- **Self-containedness.** The exact-output step for value factors, the recognition algorithm, and the conditional-moment witness defer essential proofs to companion notes. The fragment now proves all three.
- **Notation and wording.** These are minor.
- **Missing sharp statement.** The text calls the general negative-curvature bound "open" without saying whether the recourse route can reach it. It cannot in general (Proposition `prop:cr-limit`).

The three recourse results (direct value factors, global affine responses, piecewise responses) are now **one theorem** (`thm:cr`) with one curvature lemma.

## 2. Claim-by-claim verification

**(a) Convex-energy inequality and proximal envelope.** Both are correct.

- Convex energy: first-order optimality on the convex box gives F(x)−F* ≥ ½dᵀHd. Combining this with growth gives, for every c ≥ 0, F(x)−F* ≥ g/(2g+c)·dᵀ(H+cI)d. The text's c = 2ν case is one instance (`lem:cr-energy`). The inequality fails with integer variables, as the text says.
- Envelope: E_λ − (λ/2)‖·‖² is an infimum of affine functions, so it is concave, and E_λ has upper curvature λ in every direction (not just coordinate directions). The growth bound gλ/(2g+λ) comes from minimizing g‖x−x*‖² + (λ/2)‖x−w‖² over ℝⁿ. The condition λ > ν is needed only for strong convexity of each evaluation. The unconstrained Hessian λH(H+λI)⁻¹ is correct.

**(b) Affine recourse identity, growth transfer, reduced Hessian, residual width.**

- The identity f(y,v) − f(ȳ,v) = ½(y−ȳ)ᵀC(y−ȳ) + λᵀ(y−l) + μᵀ(u−y) is correct. It holds verbatim for polytopes Y = {Gy ≤ γ} as ½(y−ȳ)ᵀC(y−ȳ) + λᵀ(γ−Gy).
- Growth transfer to the metric I + ΣEᵀBᵀBE is correct. Growth with g > 0 already implies uniqueness, which gives y* = ȳ(z*).
- The reduced Hessian A + BᵀCB + BᵀD + DᵀB is correct. A sharper fact is new: under the certificate it equals **A − BᵀCB**. Complementarity is a polynomial identity on a full-dimensional set, so each row with a nonzero multiplier has G_kB = 0. Hence Bᵀ(CB+K) = 0 (`lem:leaf`(b)). This shows that recourse never increases the coordinate curvature, and it gives an energy formula (below).
- The residual-width statement is correct. Original width does not control it: a private variable attached to z₁,…,z_k in a star creates a k-clique.
- The ν-corollary is correct when ν > 0. The bracket ν ≤ β < 2ν takes polynomially many halvings because nonzero eigenvalues of a rational matrix are at least D₀^{−d}β₀^{1−d}. The algorithm never needs β.

**(c) Central-QP + LP recognition, including singular C.** Correct. Complete proof in `thm:cr-recog`.

- The common central gradient is classical (Mangasarian 1988).
- Necessity rests on one fact: an affine function that is nonnegative on Π and vanishes at an interior point vanishes identically. Applied to the primal bounds and the one-signed gradients, it forces the pattern (K_l, K_u, J).
- Sufficiency is box KKT with multipliers Γ_i on K_l and −Γ_i on K_u.
- The LP uses affine Farkas multipliers for a polytope Π, or absolute-value auxiliaries for a box.
- Exact checks (`convexrecourse_recognition.py`) compared the central-pattern LP with brute force over all 3^r global patterns on 5,000 random instances with r ≤ 3, many with singular C. They agreed on every instance: 2,358 accepted, 2,642 rejected. Every accepted selector passed exact pointwise KKT at five parameter values (11,795 checks). Two random singular instances plus the (y₁+y₂−z)² example show that fixing an arbitrary central active set would fail.

**(d) Value factors: concavity, curvature, bit complexity, exact output.**

- Concavity and curvature are correct: φ_t is an infimum of affine functions of v.
- The bit argument is correct. Each table entry is a sum, over one selected assignment, of at most |𝒜|+T+n values of polynomial size. No common denominator across active sets is needed (`lem:cr-bits`).
- The exact-output step is correct but was unproved in the paper. Main-text `lem:height` covers boxes only. `lem:cr-height` proves the polytope version: minimal face, H positive definite on the face tangent space by uniqueness, a nonsingular saddle matrix, then Hadamard and Cramer, giving denominator ≤ (2nβ²)ⁿ. The bound depends only on the continuous Hessian block and the constraint matrix, so it is uniform over the integer assignments. Reconstruction and acceptance are re-proved in `thm:cr`(iii).

**(e) Piecewise curvature, the f_M example, and the ladders.**

- Proposition `prop:piecewisecurvature` is correct. The step from "finitely many closed leaves" to "finitely many quadratic segments on a line" needs the covering argument now written out in `prop:vf-curv`. The downward-jump argument then closes the proof.
- New: the bound is **exact**. The certified σ_j = min_r(B_rᵀCB_r)_jj is the largest valid cancellation for that factor and does not depend on the certificate (`prop:vf-curv`(c)).
- New: a finite certificate always exists, for singular C too, via KKT pattern polyhedra, triangulation and the hyperplane arrangement (`prop:cert-exist`). Its size may be exponential.
- f_M: all three responses, values, gradient signs and piece curvatures 8, 0, 2M/(M+1) were checked exactly for five values of M (905 points), together with BᵀCB = 2M, 2M+8, 2(M+2)²/(M+1). Certified curvature is 8; the direct value is 2M+8.
- Three-piece ladder: the identity z²+f_M−1/20 = t²+Mr²+s²+u/5 was checked symbolically. Negative inertia is exactly m and 2 ≤ ν ≤ √5. The growth constant can be **improved from 1/36 to 1/12**, because w = r−s−t gives w² ≤ 3(r²+s²+t²); this was checked at 1,800 exact points. L ≤ 41/4.
- One-leaf ladder (u,v,y ∈ [0,1]): growth 1/3 (checked at 4,500 points), L ≤ 9/4, inertia m.

**(f) Open target.** See section 5.

## 3. Issues and fixes

| # | Severity | Location | Issue | Fix (verified) |
|---|---|---|---|---|
| 1 | major | extensions.tex, value-factor paragraph ("Exact recovery uses height bounds for the original rational QP on a bounded polytope… The companion proof establishes the full bit and height argument") | The paper proves height bounds only for boxes (`lem:height`), so exact output for value factors has no proof in the paper. | `lem:cr-height` (polytope height, uniform over integer labels) plus the reconstruction argument in `thm:cr`(iii). |
| 2 | major | extensions.tex, recognition paragraph ("The companion gives the full recognition proof") | Only necessity is sketched. Sufficiency, the multiplier certificate and the LP encoding are missing. | `thm:cr-recog` with full proof, for a box or any full-dimensional polytope of parameters. |
| 3 | major | extensions.tex, conditional-moment witness ("The companion supplies the complete construction and checks, including global McCormick inequalities") | The proof is not in the paper. The McCormick claim is unproved here. | `prop:cr-moment` proves the identity, growth 1/22, ν = 2, the moments, the value 3/32 and the covariance completion; all were also checked exactly. Drop the McCormick sentence or prove it separately. |
| 4 | minor | extensions.tex, "Any globally affine feasible selector fixes these coordinates…" | It must be an *optimal* selector; feasibility alone forces nothing. | Wording fixed in `thm:cr-recog`. |
| 5 | minor | extensions.tex, notation | D is both the coupling matrix and the correction sum D(y); A is both the retained block and 𝒜; the notes use u for both a bound and a multiplier. | Coupling K_t; all retained-only terms in q₀; private polytope G_ty ≤ γ_t; multipliers λ. |
| 6 | minor | `prop:piecewisecurvature` proof | The finite segment structure on a coordinate line is asserted, not proved. Boundary lines need care. | Covering argument in `prop:vf-curv`(b). |
| 7 | minor | ladder in extensions.tex and the piecewise note | g = 1/36 is valid but loose. | g = 1/12 (`prop:cr-ladder`). |
| 8 | minor | affine note (14), if imported | Diagonal rescaling changes the integer lattice. | `cor:cr-affine`(b) is restricted to continuous coordinates. |
| 9 | minor | "When L_red ≤ C₀β, for a checked rational ν ≤ β < 2ν…" | Needs ν > 0. The polynomial halving count needs an eigenvalue separation bound that is not in the paper. | `cor:cr-nu` includes the bound and notes the algorithm never uses β. |
| 10 | minor | extensions.tex "Negative curvature", "Two existing identities…"; "The companion…" | References to repository history and companions. | Removed in the fragment. |
| 11 | minor (scope) | "General changing active faces… require further structure; a general negative-curvature-only bound is still open." | Correct but unsharpened. The corollary's hypothesis L ≤ C₀ν can fail for every admissible recourse choice. | `prop:cr-limit` and `rem:cr-unstable`. |

No critical issue was found.

## 4. Classical versus new, and placement

Closest prior work:

- Multiparametric QP critical regions and affine responses: Bemporad–Morari–Dua–Pistikopoulos 2002 (bib); Tøndel–Johansen–Bemporad 2003 (local KB).
- Convex parametric piecewise-quadratic programs with set-valued solution maps and region traversal: Patrinos–Sarimveis 2011 (local KB).
- Constancy of the gradient on the solution set of a convex program: Mangasarian 1988, *Oper. Res. Lett.* 7(1), February 1988. The bibliographic data were checked by web search; the page numbers were not.
- Exact convex QP: Kozlov–Tarasov–Khachiyan (bib). Exact LP: Grötschel–Lovász–Schrijver (bib).
- Del Pia–Khajavirad 2026 split variables into nonpositive-diagonal endpoint variables and positive-diagonal continuous components (Q_C ⪰ 0 is one sufficient case), with low-rank coupling (their Theorem 4 and Corollary 1, local KB). This is the closest structural precedent for "convex part eliminated, combinatorial part retained". Our retained part may be a nonconvex continuous or mixed problem, handled by the conditioned grid.
- Their forest dynamic program uses concave piecewise-quadratic value functions with concave kinks, which is close in spirit to `prop:vf-curv`.

| Result (label in fragment) | Status | Recommendation | Reason |
|---|---|---|---|
| `thm:cr` Certified convex recourse (unified) | New composition; the ingredients are classical | **main** | Turns three scattered results into one statement with one parameter. It is the paper's "conditional recourse" for convex blocks. |
| `lem:leaf` KKT identity, Hessian −BᵀCB, energy formula | Identity classical; the simplification and the energy reading are elementary and not stated in the sources | **main** | Short. It explains when cancellation happens and drives the limits. |
| `prop:vf-curv` value-factor curvature with exactness | Concavity classical; exactness new in this framing | **main** | Core lemma; shows piecewise certificates lose nothing. |
| `prop:cert-exist` finite certificates exist | Folklore-level, in the spirit of mp-QP / piecewise linear-quadratic theory | **appendix** | Completes the picture; size unbounded. |
| `lem:cr-growth` growth transfer | Elementary | **main** (one paragraph) | Needed. |
| `lem:cr-bits`, `lem:cr-height` | Standard techniques | **appendix** | Needed for self-containedness. |
| `cor:cr-affine` affine condensation with metric and pullback | Elementary | **main** for (a); **remark** for (b) | (b) is a small refinement, valid only for continuous coordinates. |
| `cor:cr-nu` ν-regime and the β bracket | Elementary | **remark** | The algorithm does not need it. |
| `thm:cr-recog` recognition of affine selectors | Ingredients classical; whole-box recognition with singular C not found in the literature searched | **main** (proof may go to an appendix) | Clean polynomial-time algorithm; removes supplied maps. |
| `ex:cr-fm` three pieces | Example | **main** | Smallest illustration of cancellation across active sets. |
| `prop:cr-ladder` three-piece ladder; `rem:cr-oneleaf` | Examples | **appendix** (ladder); **drop or one sentence** (one-leaf) | Parameter separation with growing negative inertia; the ladder subsumes the one-leaf case. |
| `prop:cr-limit` obstruction | **New** | **main** (limits section) | Directly answers "exactly when"; matches the paper's "structural limits" theme. |
| `rem:cr-unstable` instability | New, elementary | **main remark** | Shows the cancellation is fragile under tiny private linear terms. |
| `lem:cr-energy`, `lem:cr-envelope` | Elementary; Moreau envelopes classical | **remark** | Motivation for the open target, not results. |
| `prop:cr-moment` local-moment witness | New, interface-specific | **appendix** (or drop if space is short) | Refutes one relaxation interface only; it must not be presented as a hardness result. |

For the paper's bibliography: add `Mangasarian1988`. No other new keys are cited in the fragment. Not checked and not cited: Rockafellar–Wets on conjugates of piecewise linear-quadratic functions, Cannarsa–Sinestrari on semiconcavity, Moreau 1965.

The fragment references these main-text labels: `lem:round`, `prop:filter`, `lem:contraction`, `lem:localize`, `lem:states`, `thm:approx`, `lem:height`, `eq:semiconcavity`. The paper preamble must also define the `definition` and `example` environments.

## 5. Developments on the open questions

**(1) Unification: resolved.** In the convex recourse model with fixed private polytopes, define for each block and attachment coordinate the certified cancellation σ_{t,j} = min over leaves r of (B_rᵀC_tB_r)_jj, with σ = 0 when no certificate is given. The reduced objective then has coordinate curvature

L_i = (H₀)_ii − Σ_{t ∋ i} σ_{t,j(t,i)}.

The algorithm runs in f(p, max{1, L/g})·poly(S) for both approximation and exact output; certificates are valid without growth; and κ_rec ≤ κ_orig. The three earlier results are the special cases σ = 0, one leaf, and many leaves.

**(2) "Exactly when recourse reduces L/g to O(ν/g)": sharpened to an intrinsic criterion.**

- By `prop:vf-curv`(c), σ_{t,j} is the largest strong-concavity modulus of φ_t along e_j. It is certificate-independent and always finitely certifiable.
- By `lem:leaf`(c), on each piece σ equals −min over w in the free subspace of (wᵀCw + 2wᵀKe_j). This is the energy the response spends to follow a unit change of v_j, using only directions that keep every constraint with a positive multiplier active.
- So the route yields an O(ν/g) parameter **exactly when** (H₀)_ii − Σ_t σ_{t,j} ≤ C₀ν for all i, for some admissible choice of private blocks.
- The unconstrained Schur complement is the floor: no piece can cancel more than (K e_j)ᵀC⁺(K e_j) when K e_j lies in the range of C.

**(3) Obstruction: new (`prop:cr-limit`).** F_M = M(x−y)² − (x+y−2)²/8 + 2(y−1) on [0,2]×[1,3]:

- unique minimizer (1,1), growth 1/8, ν = 1/2, bag size 2;
- for every admissible retained set and every positive diagonal rescaling, L_R/g_R ≥ (4M−1/2)/3.

The cause is non-nested private and retained boxes: whichever variable is eliminated, its response clips on a full-dimensional set where the stiffness reappears. The parameter is defined on the original box. Tightening the box around the optimizer removes the clipped piece when y is retained, but not when x is retained, because then the stiff piece contains the minimizer. This is why localization is the natural next step. This proves the hypothesis L ≤ C₀ν is substantive and cannot be met by any choice of blocks or rescaling. Exact checks (`convexrecourse_obstruction.py`) cover the growth bound, eigenvalues, both clipped pieces and their curvature 2M−1/4, the concave interior piece, the value gap on the stiff piece, and the growth upper bounds.

**(4) Instability: new (`rem:cr-unstable`).** For M(y−u)² + εy, the certified cancellation drops from 2M at ε = 0 to 0 for every ε > 0, because the clipped piece [0, ε/2M] has the full curvature 2M. The Hessian, and hence ν, is unchanged. Thus the ladder families' uniform constants depend on exact zero private linear terms. The certified quantity is a maximum over pieces, however small the piece.

**(5) What failed and why.**

- I tried to replace the global constant by a *localized* one: either the maximum over pieces of local curvature/local growth, or curvature restricted to the sublevel set {V ≤ F* + Δ}. In the obstruction, retaining x gives an O(1) per-piece ratio. Retaining y puts the stiff piece where V ≥ 3/2 − O(1/M).
- So a localized analysis would handle that family. But the corrected-grid interpolation needs valid corrections on every cell visited in the first stages. With the global grading θ ~ κ^{-1/2}, those stages already cost poly(√M) states per coordinate.
- Cell-dependent corrections are valid (the rounding lemma only uses curvature on the current cell product, and a factor-wise version fits bag scopes). But I found no contraction or state-count argument that avoids paying for stiff cells before they are filtered. No theorem is claimed.
- A "tracked stiffness" sufficient condition follows from the energy formula but is essentially a restatement, so it was not added.

**Open questions, sharpened:**

1. **Localized parameter.** Is there a filtered-grid variant whose parameter is the maximum over linearity pieces of (local curvature)/(local growth), or curvature on the sublevel set {V ≤ F* + Δ} for some Δ = Θ(gap)? `prop:cr-limit` shows this is the minimum needed for recourse to approach ν/g.
2. **Choosing the private blocks.** Minimizing max_i L_i over admissible private partitions is a combinatorial problem of unknown complexity.
3. **Computing σ_{t,j}.** σ_{t,j} is intrinsic, but computing it may require enumerating critical regions. Is deciding σ_{t,j} ≥ s hard? Is there a polynomial certificate class between one leaf and a full partition, for example certifying only the minimizing piece?
4. **The general target f(p, ν/g)·poly(I)** remains open. Three method-level obstructions are now on record:
   - complete scalar messages are exponential (the unique-message family in the repository notes; not part of this cluster);
   - global recourse curvature (`prop:cr-limit`);
   - matched local separator moments (`prop:cr-moment`).

   None is a complexity lower bound.

## 6. Targeted checks actually run

All checks are in `paper-decomposition-aware/process/w1/checks/`, use exact `fractions.Fraction` (SymPy for symbolic identities), and were run individually with `python3 -B`. All passed. They are finite exact evidence; the proofs carry the general claims. No project-wide verification and no CI inspection were performed.

- `convexrecourse_value_factors.py`:
  - f_M: 905 value/response checks, 15 piece-curvature checks, 15 energy identities;
  - random positive definite blocks: 300 instances of Γ = −BᵀCB, 600 energy-formula checks, 600 exact second differences equal to Γ_jj, and 59,700 concavity second differences along lines crossing pieces (200 lines crossing pieces of different curvature);
  - ladder: symbolic identity (10) and 1,800 checks of growth 1/12.
- `convexrecourse_recognition.py`:
  - 5,000 random instances (r ≤ 3, often singular C) plus the two named examples;
  - exact Fourier–Motzkin LPs; central-pattern LP agreed with all-pattern brute force on every instance;
  - 11,795 pointwise KKT checks of accepted selectors.
- `convexrecourse_obstruction.py`:
  - symbolic PSD lower bound and eigenvalues;
  - 10,000 growth checks;
  - 2,010 reduced-value evaluations against brute force;
  - piece curvature, concave interior piece, 505 value-gap checks;
  - instability checks.
- `convexrecourse_oneleaf.py`: 4,500 growth checks for the one-leaf ladder; instability curvature.
- `convexrecourse_moment_witness.py`:
  - symbolic F_h identity; Hessian structure; moment matching of orders 1–3 (order 4 differs); relaxed value 3/32;
  - covariance completion; 6,000 checks of growth 1/22;
  - 61,740 grid checks of the convex-energy inequality (diagnostic: the growth constant is the grid ratio).
- LaTeX: the fragment compiled with `pdflatex` in a temporary wrapper (since removed). There were no errors and no overfull boxes; only main-text references and citations were undefined.

One check run was stopped and rerun: the first version of the recognition check was too slow because Fourier–Motzkin ran without eliminating equalities. Its background job was stopped, equality elimination was added, and the rerun finished in 18 s. No background jobs remain.
