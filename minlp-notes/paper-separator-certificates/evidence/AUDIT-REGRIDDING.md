# Audit of constructive regridding and certified local solves

## Conclusion and scope

The constructive certificate theorem is mathematically sound under its stated continuous-box, quadratic-growth, smoothness, lower-model, and terminating-oracle assumptions. The aggregate drift and contraction estimates do not conceal a branching factor. All displayed numerical constants and the shell-incidence upper bounds check. The inexact extension correctly pays one local residual per selected bag, rather than one per solved leaf-cell pair. No topic-wide fatal flaw was found.

The paper needs three explicit clarifications. Remove every fixed original coordinate before shell construction, not only the completely singleton-domain case. Interpret the accuracy-in-bits statement only for positive approximation budgets. Keep known-parameter final size, parameter-search work, and the returned search trial's output guarantee separate. The original unknown-constant schedule is valid with its fixed-instance qualification; a total-operation budget without a separate stage cap gives a simpler, stronger accounting argument.

A concrete arithmetic realization closes part of the general-oracle scope. For explicit rational polynomials, midpoint Taylor affine lower models make every local problem an exactly solvable affine minimization on a rational box intersection. Rational endpoint reconstruction controls center denominators by a linear exponent in the stage. This yields a bit-work theorem with explicit numerical conditioning factors. It does not yield polynomial time in input length without a quantitative conditioning restriction.

This audit concerns the constructive separator certificate theorem and its finite-precision implementation. It does not re-prove the separate single-tree lower bounds, separation theorem, covering conjectures, or the nonlinear dynamics extension. Source notes were read directly; historical reviews were used as cross-checks, not as substitutes for source proofs. No computational experiment was rerun and no literature discovery was performed.

## Source map

The following references use the current source line numbers.

| Topic | Exact source |
|---|---|
| Tree decomposition, occurrence bound and assignment | `research-20260929/theory-decomposition/decomposition-certificates.md`, lines 176–211 |
| Lower-model and smoothness assumptions | Same file, lines 223–248 |
| Certificate definition, including closed touching pairs | Same file, lines 250–305, Definition 1.2 |
| Validity and exact DP unfolding | Same file, lines 306–379, Lemmas 1.3–1.5 |
| Original shell construction and slope telescope | Same file, lines 698–754, Lemmas 3.1–3.2 |
| Earlier existence theorem, contrasted with construction | Same file, lines 785–940, Theorem 3.4 and Remark 3.5 |
| Regridding assumptions and computational scope | `research-20261002/regridded-certificates/note.md`, lines 16–74 |
| Regridding constants and algorithm | Same file, lines 76–143 |
| Aggregate drift and grading | Same file, lines 145–217 |
| Current-center error | Same file, lines 219–265 |
| Contraction, stopping and box counts | Same file, lines 267–333 |
| Incidence and local-program counts | Same file, lines 335–395 |
| Unknown-constant schedule | Same file, lines 397–445 |
| Certified local solve, lower DP and backtracking | `research-20261002/regridded-certificates/inexact-oracles.md`, lines 35–140 |
| Slope and gradient errors | Same file, lines 142–221 |
| Inexact contraction and counts | Same file, lines 223–316 |
| Touching faces and rational reconstruction | Same file, lines 318–369 |

The current reviews read were `research-20261002/reviews/regridded-certificates-adversary.md`, `regridded-certificates-significance.md`, and `regridded-inexact-adversary.md`, together with the relevant original decomposition review. The full current regridding and inexact notes were checked, including the revised budget schedule and reconstruction text. The original certificate note was read, including its later corrections, computational qualifications and limitations.

## Assumptions that must remain visible

1. The domain is a continuous product of compact intervals. All fixed coordinates are removed first. Coupled constraints and lattice feasibility do not follow from this proof.
2. The supplied finite rooted tree satisfies running intersection and covers every coordinate and factor scope. Each factor is assigned once. Put `p=max_t |V_t|`, `q=max_{t!=r}|S_t|`, and `k=max_i |T_i|`. In general `q<=p`; the sharper `q<=p-1` needs the no-contained-child convention. Do not merge bags silently, since that may change `M` and the model-error constant.
3. Quadratic growth is global: `F(x)-f*>=g||x-x*||^2` for one minimizer `x*` and `g>0`. It implies uniqueness. A locally positive Hessian alone does not supply a useful global lower bound on `g`; a remote point of gap `delta` and distance `D` forces `g<=delta/D^2`.
4. Bag objectives have `M`-Lipschitz gradients on their boxes. Boundary gradients are well-defined; the original neighborhood-`C^1` assumption is sufficient. The proof uses bag smoothness, not smooth value functions.
5. Each leaf model is a continuous convex lower function with `0<=a_t(v)-m_{t,B}(v)<=A width(B)^2/4` throughout `B`. The original per-factor `(U^q)` hypothesis implies this with `A=alpha' max_t A_t`. Vertex exactness is unnecessary for regridding.
6. Exact local oracles return a value and an attaining point on every nonempty compact box intersection, including faces. Convexity without lower semicontinuity on the boundary does not by itself ensure attainment. The explicit continuity assumption repairs the original Definition 1.2/Lemma 1.5's unqualified minimum notation.
7. General counted work treats bag value/gradient evaluation and local convex optimization as oracle operations and excludes their internal cost. The input representation, model generation and number of factors or polynomial terms are additional implementation costs.
8. Inexact lower bounds, feasible points and objective upper values must satisfy certified inequalities. Tolerance-feasible primal output or an uncertified solver objective is insufficient.

The auxiliary claim in the original certificate source at lines 740–742, identifying a slope at an “interior nondegenerate” point with a derivative of a subtree value function, requires that the point actually solve the relevant subtree problem and that the envelope hypotheses hold. It is not needed for this paper. The scientific slope definition should remain the explicit subtree sum of bag gradients, proved useful by the algebraic telescope.

## Independent derivation of drift and grading

For a configuration, let `x_i=z_i^{top(i)}`, `b_t=width(B_t)`, `d_t=width(D_t)`,

\[
Q=\sum_t b_t^2+\sum_{t\ne r}d_t^2,
\qquad E=\sum_t\|z^t-x_{V_t}\|^2,
\qquad R=\|x-c\|.
\]

On an occurrence-tree edge for coordinate `i`, a point of `D_t intersect (B_parent)_St` connects the child copy to the parent copy. Therefore

\[
|z_i^t-z_i^{p(t)}|\le b_{p(t)}+d_t.
\]

The parent copy need not belong to `D_t`, and no equality of separator copies is assumed. This is exactly the weak compatibility in the certificate definition.

For one coordinate, build the path-incidence matrix with one row per occurrence, and columns for occurrence-bag widths and occurrence-edge cell widths. A row at depth `a` has `2a` entries equal to one. Its squared operator norm is bounded by its squared Frobenius norm,

\[
2\sum_{t\in T_i}\operatorname{depth}_i(t)
\le |T_i|(|T_i|-1)\le k(k-1).
\]

A topological ordering proves the depth sum bound, since the vertex in position `a` has depth at most `a-1`. Summing over coordinates counts a bag width at most `|V_t|` times and a separator width at most `|S_t|` times. Hence

\[
E\le k(k-1)\left(\sum_t |V_t|b_t^2+\sum_{t\ne r}|S_t|d_t^2\right)
\le C_0Q,\qquad C_0=k(k-1)p.
\]

Branching may repeat columns across rows but cannot defeat the Frobenius estimate. Bounded occurrence is essential; it is not implied by bounded width.

Shell grading gives

\[
b_t\le h+\theta\|x_{V_t}-c_{V_t}\|+\theta\|z^t-x_{V_t}\|,
\]

and the same inequality holds for each cell with vectors restricted to its separator. Coordinate `i` belongs to `m_i` bags and exactly `m_i-1` separators. A copy error is zero outside the bag's own separator. Consequently the center-difference sum is at most `(2k-1)R^2`, and the copy-error sum is exactly `2E`. With at most `2N-1` boxes,

\[
Q\le6Nh^2+3(2k-1)\theta^2R^2+6\theta^2E.
\]

Under `12C_0 theta^2<=1`, absorb the last term to obtain

\[
Q\le12Nh^2+12k\theta^2R^2.
\]

For `k=1`, all separators are empty and `E=0`; no division by a zero constant is needed. Empty bags/separators can use their single zero-dimensional cell and slope.

## Current-center error and contraction

Set

\[
B_0=MC_0/2+A/4,\quad \eta=g/20,\quad
C=12B_0+6kC_0M^2/\eta,\quad B=\max\{p,2C/g\}.
\]

The slope telescope gives the exact identity

\[
\Phi=F(x)+\sum_t\bigl[a_t(z^t)-a_t(x_{V_t})-
\nabla a_t(c_{V_t})\cdot(z^t-x_{V_t})\bigr]-\sum_t\operatorname{err}_t.
\]

Taylor's estimate at `x_{V_t}`, followed by the gradient difference between `x_{V_t}` and `c_{V_t}`, bounds each bracket in absolute value by

\[
M\|x_{V_t}-c_{V_t}\|\|z^t-x_{V_t}\|+(M/2)\|z^t-x_{V_t}\|^2.
\]

Thus

\[
|F(x)-\Phi|\le M\sqrt{kC_0}R\sqrt Q+B_0Q.
\]

Substituting the grading estimate gives

\[
\sqrt{12kC_0}M\sqrt N hR+
\bigl(\sqrt{12}k\sqrt{C_0}M\theta+12kB_0\theta^2\bigr)R^2
+12B_0Nh^2.
\]

Young's inequality pays `eta R^2/2+6kC_0M^2 Nh^2/eta` for the mixed term. The two remaining theta restrictions pay at most `eta R^2/2`. Hence `|F(x)-Phi|<=eta R^2+CNh^2`. There is no omitted boundary first-order term; cancellation works at the actual center before any stationarity statement.

A consistent configuration at `x*` has relaxed value at most `f*`. Therefore the minimizing configuration satisfies `Phi=LB_j<=f*`. Quadratic growth and the squared triangle inequality give

\[
e_j\le e_{j-1}/9+(10C/(9g))Nh_j^2.
\]

Since `h_{j-1}=2h_j`, `B>=2C/g` closes the induction. At stage zero `e_{-1}<=n s_0^2<=pN h_0^2<=BNh_0^2`; the stage-zero coefficient is even smaller than the later coefficient. For later stages the center difference is at most `10BNh_j^2`, and at stage zero it is at most `4BNh_0^2`. The incumbent includes the current point, so

\[
0\le\mathrm{UB}-\mathrm{LB}_j
\le(gB/2+C)Nh_j^2\le gBNh_j^2.
\]

The stated horizon `J=max(0,ceil(log_2(s_0 sqrt(gBN/eps))))` follows. No upper quadratic-growth bound, monotone sequence of lower bounds, or uniqueness of a minimizing configuration is used. The next center must remain the newly reconstructed point; substituting the retained best incumbent into an inequality for that new point would be unjustified.

## Shell construction, touching faces and all counts

The source shell construction is correct on a nondegenerate domain. Central cubes have side `h`. Level `ell>=1` uses grid side `theta 2^{ell-1}h` on the outer cube of radius `2^ell h`; the inner cube boundary aligns with the grid because `1/theta` is an integer. Retained cubes lie at distance at least `2^{ell-1}h`. Clipping decreases width and increases distance. After clipping, dropping empty-interior pieces preserves boundary coverage because every boundary point is a limit of interior points off the finitely many grid hyperplanes, and a retained closed box contains a convergent subsequence.

Repair for partially fixed domains: substitute each fixed original coordinate in all factors, remove it from every bag and separator, and delete or keep empty bags consistently. Then running intersection remains valid, no dimension increases, and the restricted smoothness and growth hypotheses hold on the reduced coordinates. If no coordinates remain, certified evaluation solves the problem. Merely dropping degenerate intersections before this reduction can discard the whole domain.

Let `m=4/theta`. At stage `j`, each partition has `j+1` levels and at most `m^d` boxes per level in dimension `d`. Therefore final boxes are at most `2Nm^p(J+1)` and all freshly created boxes are at most `Nm^p(J+1)(J+2)`.

For one bag/separator level pair in dimensions `d` and `q'`, compare the original grid sides, before clipping. If the bag side is smaller, each projected bag cube meets at most `3^{q'}` separator cubes, including endpoint contacts, so there are at most `3^{q'}m^d` incidences. If the separator side is smaller, each separator cube meets at most `3^{q'}` projected bag positions, each with at most `m^{d-q'}` private-coordinate fibers, again giving `3^{q'}m^d`. Clipping cannot add an intersection. This argument also covers the central grids; zero-dimensional separators have one cell.

Summing the `(j+1)^2` level pairs gives at most `N3^q m^p(j+1)^2` own-cell programs, including root leaf minima, and at most `(N-1)3^q m^p(j+1)^2` parent-child incidences. Summing stages gives the exact upper count

\[
N3^q m^p (J+1)(J+2)(2J+3)/6.
\]

An interval whose length is at most the other grid's spacing meets at most three closed grid intervals; this is where touching faces enter the factor `3^q`. They cannot simply be dropped from the exact configuration identity. Although the original validity remark allows an alternative formulation omitting certain touching tests, the constructive proof and implementation should use the stated closed intersections.

Enumerate level pairs by grid indices, charge to the finer bag grid or the separator grid plus fibers, and filter shell membership. The candidate count has the same incidence bound and costs `O(p)` coordinate work each. This avoids a hidden dense all-pairs scan. Bag gradients accumulate bottom-up in `O(Np)` arithmetic. Summed parent-leaf/child combinations are at most `(N-1)m^p(j+1)`, so affine child aggregation does not require a maximum-degree factor. The generic counted work is `O(pN3^q m^p(J+1)^3)` when bag evaluations are unit oracle calls.

This is an upper bound. The original source's discussions that infer a universal `Theta(log^2)` program count from finite numerical ratios should not be imported as a proved lower bound. The paper only needs the rigorous upper count.

## Certified inexact solves

For each actual local objective `q_t`, require a certified lower bound `ell_t`, a genuinely feasible point `z^t`, and a certified upper value `u_t` with

\[
\ell_t\le\min q_t\le q_t(z^t)\le u_t\le\ell_t+\delta_{t,j}.
\]

The incoming intercept is the minimum of these lower bounds. The child affine constant is the minimum compatible child intercept. Hence all local and child inequalities remain valid for arbitrary approximate slopes.

Along the selected backtracked choices, the selected local lower bound equals its incoming intercept, which in turn equals the parent leaf's selected child intercept; at the root it equals `LB`. Expanding the local objectives and canceling those intercepts gives the direct identity

\[
\widehat\Phi-\mathrm{LB}=\sum_t(q_t(z^t)-\ell_t).
\]

Every summand lies in `[0,delta_{t,j}]`. This proves that local gaps bounded by `d h_j^2` accumulate to at most `dNh_j^2`. Unselected problems affect which lower bound wins but never enter this residual sum. Inherited child constants are exact reported numbers and must not be paid a second time.

With `C_1=2p max(k-1,1)`, the edge-copy sum `H` satisfies `H<=C_1Q`: bound each edge coordinate by `b_parent+d_child`, square with factor two, and use `sum_child |S_child|<=(k-1)|V_parent|`. Thus slope error of aggregate norm `nu<=zeta sqrt(N)h_j` gives

\[
|\widehat\Phi-\Phi|\le\frac\eta4R^2+K_sNh_j^2,
\quad
K_s=\sqrt{12C_1}\,\zeta+12kC_1\zeta^2\theta^2/\eta.
\]

For gradient error vectors `e_t`, the coordinate subtree-sum matrix has squared Frobenius norm equal to the occurrence depth sum, at most `G=k(k-1)/2`. Hence `nu^2<=G sum_t ||e_t||^2`; per-bag error `gamma h_j` suffices with `zeta=sqrt(G)gamma`. Exact rational addition avoids a separate summation error; otherwise that error belongs in `nu`.

Adding the base error, slope perturbation and local residual gives coefficient `eta+eta/4=g/16` on `R^2`. If upper objective evaluation adds `omega Nh_j^2`, set `K=C+K_s+d+omega` and `B_in=max(p,8K/(3g))`. Then

\[
e_j\le e_{j-1}/7+(8K/(7g))Nh_j^2,
\qquad e_j\le B_{\rm in}Nh_j^2,
\]

and the actual certified gap is at most `(5gB_in/8+K)Nh_j^2<=gB_inNh_j^2`. The strict contraction margin is necessary with halved widths; allocating another full `eta R^2` would leave contraction `1/4`, which does not close a constant-times-`h_j^2` induction.

Touching domains are rational box intersections. Exact endpoint comparison decides emptiness and identifies fixed face coordinates, which must be fixed and eliminated before solving. Exact rational clipping certifies feasibility, but objective certification must occur after reconstruction. A supplied relative-box Lipschitz bound `L_q` gives transport error at most `L_q sqrt(p) tau` for coordinate displacement at most `tau`; starting from a certified half-budget and paying the other half after rounding is sound. Convexity and the width-squared model contract alone do not imply a supplied quantitative modulus.

The source's linearly growing bit-accuracy statement needs positive budgets. At zero local gap a rational minimizer may not exist: `(x^2-2)^2` is convex on `[1,2]` and uniquely minimized at `sqrt(2)`. Thus zero budgets require exact oracles with an appropriate exact representation. This is already compatible with the mathematical theorem's termination hypothesis but should be stated in the arithmetic prose.

## Simpler unknown-parameter search and its output

The original schedule budgets all counted operations and also caps stages by `r+lambda_eps`. It is correct, and its stated one-logarithm overhead uses fixed instance constants. The explicit stage cap is unnecessary.

Use rounds `r=1,2,...`; restart each `mu=1,...,r` from the fixed initial point with budget `2^r` counted operations and no separate stage limit. Stop at the first completed stage with a valid gap test. Let a sufficient run have a theoretical work upper bound `W>=max(2,2^{mu_*})`. At `R=ceil(log_2 W)`, the sufficient trial is present and has enough work. Total work is at most

\[
\sum_{r=1}^Rr2^r=(R-1)2^{R+1}+2\le2R2^R=O(W\log(2+W)).
\]

Every trial's gap test is sound regardless of whether its grading is sufficient for contraction. General oracle calls must terminate; their internal time remains excluded. The theoretical sufficient-run bound contains `m^p>=2^{mu_*}`, so the premise on `W` is available without a new numerical parameter.

The returned trial may have a different `mu` and stage than the sufficient comparison trial. It has an unconditional epsilon-gap guarantee and its actual partitions obey the actual shell formula. It is not justified to assign the known-parameter fine final-size bound to that trial by identifying it with the comparison run. A safe search output bound is `O(W)` boxes, because emission is charged to the returned trial's final budget; total search work is `O(W log W)`. This distinction is made in the authored section.

## Concrete rational polynomial realization

Let every bag objective be given by an explicit sparse list of rational monomials, of total degree at most a fixed `D`. Let `L` be total encoded input length, including the original box, initial rational center, tree, assignment, coefficients and rational epsilon. Let `S` be the total number of monomial records. Repeated equal monomials need not be aggregated. These representation assumptions are stronger than “a polynomial is evaluable” or an arithmetic-circuit representation, and are needed for the following proof.

### Computable smoothness and affine models

Put `R_0=max(1,max_i |L_i|,max_i |U_i|)`. For `D>=2`,

\[
M=D(D-1)R_0^{D-2}\max_t\sum_\alpha|c_{t,\alpha}|
\]

is a valid rational Hessian operator-norm upper bound: each row sum of absolute Hessian terms is bounded by this expression, and the Hessian is symmetric. For `D<=1`, take `M=0`. A tighter externally supplied certified rational bound can be used instead. Its encoding must be included in `L`. The computable bound has polynomial encoding length for fixed `D`, although its numerical magnitude can be exponential in `L`.

For midpoint `m_B` of a leaf, define

\[
\ell_{t,B}(v)=a_t(m_B)+\nabla a_t(m_B)\cdot(v-m_B)-Mp\width(B)^2/8.
\]

Taylor's remainder is bounded by `(M/2)||v-m_B||^2<=Mp width(B)^2/8`, so `0<=a_t(v)-ell_{t,B}(v)<=Mp width(B)^2/4`. These are valid continuous affine lower models with `A=Mp`. They do not need to satisfy the original vertex-vanishing `(U^q)` condition; the generalized bag contract was already permitted by the source at lines 23–33.

Every local DP objective is now affine on a rational box intersection. For a coefficient of nonnegative sign choose its lower interval endpoint; for a negative coefficient choose the upper endpoint. This gives an exact attaining minimum, including fixed face coordinates. Slopes and objective values are rational and computed exactly. There is no generic convex-solve oracle assumption in this subclass.

### Denominator invariant

Let `Q_0` be the least common multiple of the denominators of all original endpoints and the initial center. The denominator of `s_0` divides `Q_0`. At stage `j`, every unclipped shell endpoint is a previous center coordinate plus an integer multiple of `s_0 2^{-(j+mu)}`: this follows directly from the lower grid anchor `c_i-2^ell h_j` and step `2^{-mu}2^{ell-1}h_j`. Clipping selects original endpoints. Consequently, by induction, every stage-`j` endpoint and reconstructed center coordinate has denominator dividing `Q_0 2^{j+mu}`. Midpoints divide `Q_0 2^{j+mu+1}`. This linear exponent is the key repair against possible recursive denominator growth from arbitrary local minimizers.

Let `C_c` be the least common multiple of coefficient denominators, let `q_M` be the denominator of `M`, put `d=max(D,2)`, and set

\[
Z_j=8q_MC_c\bigl(Q_0 2^{j+mu+1}\bigr)^d.
\]

All midpoint model constants, current-center slopes, local endpoint objective values and DP intercepts have denominators dividing `Z_j`. Polynomial values and gradient-coordinate products have this property by degree counting; the correction term has a squared rational width and denominator factor eight. DP operations are additions and minima, so they preserve the same denominator. There is no fresh multiplication of child intercept denominators. A common scaled-integer representation makes this transparent.

### Magnitudes, bit work and certificate encoding

Put `C_tot=sum_{t,alpha}|c_{t,alpha}|`. On the original domain, `sum_t |a_t(v_t)|<=C_tot R_0^D` and `sum_t ||grad a_t(v_t)||_1<=D C_tot R_0^{D-1}`. Each gradient term can enter at most `k-1` separator slopes. Configuration values and incoming-intercept subtree values are therefore bounded in absolute value by a sum of the form

\[
C_{\rm tot}R_0^D+NMps_0^2/4+
kD C_{\rm tot}R_0^{D-1}(s_0+R_0).
\]

This upper bound has logarithm polynomial in the explicit input length for fixed `D`. Combining it with `log Z_j` gives entry length `O_D(L+j+mu+log N+log p)`. Intermediate affine coefficient sums have the same polynomial bit bound. Schoolbook exact integer arithmetic therefore supplies a polynomial bit cost per arithmetic operation; no real-oracle primitive remains.

A conservative total arithmetic count is

\[
O\bigl(\operatorname{poly}(p,D)(N+S)3^q(4/\theta)^p(J+1)^3\bigr),
\]

times a polynomial in `L+J+mu` for bit operations. Sparse exact polynomial evaluations and gradient evaluations supply the `S` factor. Input preprocessing computes the common denominators and Hessian bound in polynomial bit work. The fine factors may be improved, but a fully specified polynomial factor is sufficient for the paper's scope; it must not omit the term count.

The compact certificate stores leaves and cells, their rational endpoints, cell intercepts, common separator slopes, and one compatible child-intercept minimum per parent leaf and child edge. Summing degrees bounds those child constants by `(N-1)(4/theta)^p(J+1)`. Its encoded length is consequently

\[
O_D\bigl(pN(4/\theta)^p(J+1)(L+J+mu+\log N)\bigr).
\]

An independent verifier reconstructs each affine model and checks every local incidence by exact endpoint minimization; separate pair proof records are optional. If they are stored, their number follows the larger `N3^q(4/theta)^p(J+1)^2` final-incidence count.

The runtime still includes the numerical factor `(4/theta)^p`, where an admissible ratio depends on `k,p,M/g` and `A/g=Mp/g`. Global quadratic growth is a promise, not a needed input for stopping: the actual lower certificate and exact feasible objective value provide the stop test. Unknown `g` is handled by the preceding total-bit-operation budget schedule, with overhead `O(T log(2+T))` relative to a theoretical sufficient-run bit-work upper bound `T>=2^{mu_*}`. This does not claim polynomial time in `L` alone. Such a conclusion requires an explicit quantitative restriction on those numerical factors and the stage horizon.

## Recommended self-contained theorem order

1. Define the product-box model and arbitrary rooted decomposition, with fixed-coordinate removal, actual `p,q,k`, and aggregate model contract.
2. Prove validity, exact finite DP/configuration unfolding, and the algebraic subtree-gradient telescope. Do not invoke value-function derivatives.
3. Construct shells explicitly; prove boundary coverage after clipping and the per-level dimension bounds.
4. Prove occurrence-matrix drift, grading absorption and uniform current-center error with all constants.
5. State and prove constructive contraction, certified stopping, final boxes and cumulative boxes.
6. Prove shell incidence enumeration and exact local-call/coordinate-work counts, using actual `q` and separate representation costs.
7. State the total-operation unknown-parameter search, distinguishing its output guarantee from the fine fixed-ratio final-size theorem.
8. Prove certified inexact lower DP, selected-residual identity, slope and gradient bounds, contraction, upper-evaluation budget, and exact face reconstruction. State the positive-budget precision caveat.
9. Give the explicit sparse rational polynomial affine-Taylor implementation with denominator, magnitude, bit-work and encoding proofs. Numerical conditioning remains a displayed parameter.

Authored manuscript files now follow this order: `sections/regridding.tex`, `sections/inexact.tex`, and `sections/arithmetic.tex`. The root author owns the foundational model lemmas and integration.

## Remaining limits and verification record

No mathematical gap remains in the audited constructive or certified-inexact theorem after these scope clarifications. General efficient certified convex oracles, mixed-integer reconstruction, coupled feasible sets, multiple minimizers and useful input-length bounds on the growth constant remain outside the result. The affine polynomial realization establishes one concrete implementation, rather than solving those broader oracle questions.

Checks actually used were targeted `cat`, `sed -n`, `nl -ba`, `rg -n`, and `wc -l` reads of the files listed above, together with independent algebraic derivation of every displayed constant and count. Narrow independent auditors cross-checked the inexact inequalities and rational polynomial realization. No experiment script, project-wide check, CI status, CI log or external literature search was used. Targeted TeX syntax checks, when run on the authored sections, are recorded in the completion note below; they are manuscript checks and provide no numerical evidence.

Completion checks: a temporary wrapper containing only the shared macros and `model.tex`, `regridding.tex`, `inexact.tex`, and `arithmetic.tex` was compiled twice with `pdflatex -interaction=nonstopmode -halt-on-error -output-directory /tmp/separator-regridding-check-8cdytfa6 /tmp/separator-regridding-check-8cdytfa6/regridding-check.tex`. The final builds passed, with no undefined references or overfull boxes. The targeted `git diff --check -- paper-separator-certificates/sections/regridding.tex paper-separator-certificates/sections/inexact.tex paper-separator-certificates/sections/arithmetic.tex paper-separator-certificates/evidence/AUDIT-REGRIDDING.md` command also passed. These checks were local section checks; no CI result is inferred.

Final integration clarifications: parent notation is `\pi(t)` throughout the authored sections, and the coefficient-denominator least common multiple in the arithmetic section is `C_den`, distinct from the analytic contraction constant `C`. The arithmetic checker computes the explicit Hessian majorant and verifies `M>=M_0`; using a smaller externally certified bound requires its separate proof and verification costs. The clock for the unknown-parameter bit schedule has constant amortized cost by binary countdown, so the claimed extra search logarithm does not conceal a further logarithm from checking a budget at every bit step.
