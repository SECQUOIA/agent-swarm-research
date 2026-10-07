# Significance of the pruned-grid and negative-inertia results

Update: the [frontier reassessment](frontier-significance.md) records the
reviewed Gaussian-like ambient QP and MIQP FPT theorems, sparse mixed
expected exact QP, anisotropic separable recourse, pure-integer quartics,
and the deterministic orthant certificate. It supersedes the ranking and
formerly open expected-work and continuous ambient-FPT questions below. Its status table
separates reviewed results from pending compositions.

Date: 2026-10-02. This is a fresh significance assessment, not another proof
review or a publication-priority determination. It reads the two current
theorems, their completed independent reviews, the
[min-marginal audit](../prior-art/minmarginal-prior.md), the
[convex-recourse audit](../prior-art/convex-recourse-prior.md), and the older
[program assessment](program-significance.md). A fresh independent agent
challenged the ranking and simpler algorithmic baselines. Literature
questions were routed to the existing literature agents; no new knowledge
base writer was created.

## Assessment

The program now has two substantial **conditioned exact-complexity
theorems**. The pruned-grid theorem is the stronger candidate for a distinct
algorithmic contribution. The negative-inertia theorem is the broader
continuous-QP companion, with a closer relationship to established spectral
branch and bound. Neither result yet demonstrates a major practical MINLP
advance.

The [pruned-coordinate-grid theorem](../new-direction/pruned-coordinate-grid.md)
proves exact rational mixed-integer box-QP optimization in
\(f(p,\kappa)\operatorname{poly}(I)\), where \(p\) is supplied bag size
and \(\kappa=\max\{1,L/g\}\) uses upper coordinate curvature of the
summed objective. Its approximation bound is polynomial in input length
and requested accuracy bits, with an exponent independent of \(p\).
There is no variable-occurrence parameter or full-bag norm parameter.

This achieves and strengthens the main open target in the older assessment.
That assessment's ranking, its description of shared-grid accuracy
exponents, and its occurrence-removal recommendation are now outdated.
The earlier affine regridding theorem remains a useful derivation, but
should no longer be the headline for rational box QP.

The [negative-inertia theorem](../new-direction/negative-inertia-qp.md)
proves exact rational continuous QP over any bounded rational polytope in
\(f(k,\max\{1,\nu/g\})\operatorname{poly}(I)\), where \(k\) is the
negative inertia and \(\nu=\max\{0,-\lambda_{\min}(A)\}\) measures
negative-curvature magnitude. Large positive curvature affects input and
preprocessing precision, but is not charged to this numerical parameter.
It has no graph
decomposition hypothesis. Its supplied-decomposition version only needs
growth toward one common optimal projected image, allowing a continuum
of original optimizers. The completed
[independent review](negative-inertia-qp-review.md) and the separately
reviewed rational normalization support this statement.

These are meaningful parameterized statements. Exact rational recovery
strengthens an approximation theorem, but does not by itself create a new
optimization method. The significance rests on the uniform input and
accuracy exponents and on the classes covered by useful parameter values.

## What appears substantive

For the pruned-grid result, the key step is the connection between a
discrete conditional bound and a continuous coordinate region. The
corrected-grid min-marginals at an interval's endpoints lower-bound every
original feasible point whose coordinate lies in that interval. Safe
filtering then preserves every optimizer, while global growth bounds the
entire retained coordinate hull relative to the next mesh scale. The next
grid has \(O(\sqrt\kappa\log(n+2))\) points per coordinate, independently
of how many accuracy refinements have occurred.

That last fact changes the complexity conclusion. A table factor involving
an accuracy-dependent quantity to the power \(p\) becomes a factor
involving \(\log(n+2)^p\), which can be absorbed into a parameter function
times an ordinary polynomial in \(n\). Capped unsuccessful conditioning
trials and the denominator invariant complete the uniform bit bound.
Finding a valid filtering mechanism that gives this contraction is the
clearest additional mathematical step in the current program.

Min-marginal computation, cost-based filtering, geometric grids, rational
reconstruction, and tree-decomposition DP are established tools. The
[source audit](../prior-art/minmarginal-prior.md) also documents adaptive
treewidth DP and min-marginal-guided grid refinement. The theorem should
therefore be described as a conditioning-dependent guarantee for their
certified combination, not as the invention of those mechanisms. The
conditional interval lemma is short once the rounding lower bound is
available; the stronger claim comes from the complete contraction and
complexity analysis.

For negative inertia, the substantive statement is a precise Turing bound
for an established low-dimensional global-optimization strategy. Global
growth confines surviving projected cells to a region whose radius is
proportional to the current mesh width. The number of cells per level
therefore depends on negative inertia and conditioning, while additional
accuracy costs additional levels. Rational normalization makes that
statement intrinsic to the Hessian's negative inertia rather than dependent
on an uncontrolled supplied factorization. Handling the exact kernel and
keeping a rational low-rank representation are necessary technical details.

The fixed-domain convex recourse formula and its growth transfer are useful
and correct. They avoid the false assumption that an equality-sliced value
function must have upper curvature. Nonetheless, square completion,
convex recourse, chord bounds, and branching in negative spectral directions
all have close precedents. The
[convex-recourse audit](../prior-art/convex-recourse-prior.md) identifies
Vavasis and Luo and coauthors as direct predecessors and Del Pia's rational
Jacobi work as a relevant arithmetic predecessor. I would present this
result as a growth-conditioned complexity analysis and arithmetic completion
of that established framework.

The distinction is not merely relative versus additive approximation. The
audit reports an additive guarantee for Luo and coauthors, with a displayed
\(\varepsilon^{-k/2}\)-type subdivision count, and an objective-range-relative
guarantee with polynomial \(1/\varepsilon\) dependence for Del Pia.
The present extra growth assumption changes the active-cell bound and
permits logarithmic accuracy dependence and exact recovery. A direct
analysis of the existing spectral algorithms under **the same growth
assumption** is therefore the most relevant comparison. Their published
unconditioned worst-case bounds alone do not establish a separation.

Neither audit identifies a source stating the exact combined guarantee.
That is an incomplete literature finding, not evidence that the theorem
is new. No priority claim follows from this assessment.

## The two results cover different structure

| Feature | Pruned coordinate grids | Negative inertia |
|---|---|---|
| Feasible domain | Continuous/integer product box | Continuous bounded rational polytope |
| Structural parameter | Supplied maximum bag size \(p\) | Number \(k\) of negative Hessian eigenvalues |
| Numerical parameter | Summed upper coordinate curvature \(L/g\) | Negative-curvature magnitude \(\nu/g\), or supplied projected ratio \(\alpha/g_T\) |
| Main computational tool | Exact finite-state junction-tree DP | Exact polynomial-time convex-QP recourse |
| Important additional scope | Arbitrarily many integer coordinates and large integer ranges | Dense interactions and coupled linear constraints |
| Nonunique-optimum scope | Main theorem assumes uniqueness; separate finite-mode corollary allows tied modes at one gridded vector | Projected theorem allows many original optima at one projected image |
| What is not supplied | General mixed linking constraints | An arbitrary mixed-integer residual oracle |

Neither theorem dominates the other. Bounded-width Hessians can have a
number of negative directions growing with dimension. A dense Hessian can
have one negative direction and unbounded interaction width. Upper
coordinate curvature and negative-curvature magnitude measure different
parts of the Hessian. Neither ratio dominates the other in general. These
are distinctions between structural parameters; such matrix
examples alone are not evidence of difficult optimization instances.

The finite-mode and projected variants are useful qualifications. They
avoid charging a small gap between tied discrete labels that share the
same optimized continuous or projected point. They do not automatically
handle several separated optimal projected points or mode-dependent
continuous feasibility.

## Restrictions that carry real difficulty

Global growth is a global separation condition. If a competing feasible
point is distance \(D\) from the optimum and has objective gap \(\Delta\),
then necessarily \(g\le\Delta/D^2\). Matrix nonsingularity, favorable
local curvature, generic uniqueness, and a small negative inertia do not
control such distant near ties. In the projected variant, the same
obstruction uses the distance between projected images.

The algorithms do not need the user to supply \(g\), and their accepted
certificates do not rely on trusting it. This is a useful separation of
correctness from the complexity promise. It does not turn an arbitrarily
small global \(g\) into a moderate running time. Multiplying the entire
objective by a positive constant scales curvature and growth together and
does not improve either ratio.

The [width-two hardness comparison](pruned-grid-hardness-sanity.md) makes
this point concrete: unique-optimum instances in the inspected reduction
have exponentially bad \(L/g\) despite bounded coefficients. The example
shows compatibility of that hardness result with the new theorem. It does
not establish that conditioning captures every possible source of hardness.
Similarly, the negative-inertia theorem does not contradict hardness with
one negative eigenvalue; its numerical parameter may be extremely large.

For an indefinite continuous quadratic on a full-dimensional feasible
region, an optimizer cannot be an interior local minimum: its Hessian
would have to be positive semidefinite. Useful examples must therefore
confront active-bound or active-constraint geometry. Adding a very large
linear term that makes one known vertex dominant gives an easy growth
certificate, but can also make the optimization elementary. Likewise,
planting a known common minimizer as the zero of nonnegative terms checks
the proof without showing a new useful regime.

The domain restrictions remain material. Product-box rounding does not
preserve a general equality, budget, indicator, or nonlinear constraint.
The negative-inertia route accepts general linear constraints because its
inner problem is continuous and convex. An arbitrary number of integer
variables in that inner problem can restore hard discrete optimization
even when the quadratic is convex. Calling that oracle convex does not
make it polynomial time.

The parameter functions can be large. Polynomially growing conditioning
may give polynomial time when structural dimension is fixed, but does not
give FPT in structural dimension alone. Conversely, a large theoretical
constant does not invalidate the uniform FPT theorem; it limits what can
be inferred about a practical solver.

## Solver capabilities actually established

Both proofs give global lower bounds, feasible witnesses, arbitrary
requested additive accuracy, and exact rational recovery in their stated
QP classes. The complexity exponents on input and accuracy bits are
uniform. These are stronger conclusions than an uncharged sequence of
real-valued optimization oracles. They are theoretical solver capabilities,
not performance measurements.

Global optimization to a tolerance is already a capability of established
global-optimization methods. The present results do not newly establish
that nonconvex QPs can be solved globally in principle. They establish
particular parameterized work bounds and exact finite-bit conclusions.

Implementation evidence is narrower than the theorem statements:

- The pruned-grid checker implements the two-pass DP, all min-marginals,
  interval filtering, and recentering. Its recorded checks cover nine
  instances and 70 stages. Selected grids are compared with exhaustive
  assignments. Unknown-growth trial caps, full rational reconstruction,
  and a standalone verifier for the pruning history are not implemented
  in that checker.
- The negative-inertia work now has a reusable small-instance branch-and-bound
  checker: five fixtures, ten runs, 416 auxiliary evaluations, and 428
  cells. It covers flat residual optima and premature reconstruction
  rejection, alongside the separate rational-normalization checks. Its
  convex oracle uses exhaustive active-face enumeration and its height
  bounds are fixture data. It therefore checks the outer algorithm but
  does not implement the general polynomial-time convex-QP oracle or
  general height computation. Ordinary floating-point solver output
  alone is not the exact oracle specified by the theorem.

No evidence yet establishes competitive wall time, memory, robustness,
or certificate size against a mature solver. A proof plus small mechanism
checks can support a complexity paper; it cannot support a broad practical
MINLP claim.

## Baselines that should control the claims

The appropriate baseline depends on the instance family:

1. Exact continuous forest-QP algorithms need no conditioning promise.
2. Ordinary finite-state bounded-width DP already handles binary or
   uniformly bounded domains.
3. Separate coordinate concavity makes endpoint DP exact.
4. Zero negative inertia is ordinary convex QP.
5. Separable components, a small enumerable discrete part, or obvious
   objective dominance can solve examples whose Hessian is nevertheless
   indefinite.
6. Existing spectral branch and bound should be assessed under the same
   growth promise, including its active-cell count, rather than only under
   a worst-case approximation bound that omits that promise.

The pruned-grid theorem is most compelling where coordinates genuinely
need interior resolution, the interaction graph has cycles, large integer
ranges or continuous decisions matter, and no simpler exact value-function
representation is available. The spectral result is most compelling where
the few negative directions are dense and coupled linear feasibility rules
out a product-box treatment. These descriptions identify useful test
targets; they do not assert that such a natural well-conditioned family
has already been demonstrated.

## The conditioning question and its quantitative follow-up

Can a natural, interacting family of growing size be shown to have a
quantitatively moderate global or projected growth ratio, without planting
its optimizer and without falling into the simpler classes above?

A strong answer would derive the conditioning bound from stated input
conditions that do not reveal the winning active face or mode assignment.
The family should keep the structural parameters controlled while the
number of interacting decisions grows. It should have non-obvious optimal
choices and allow an explicit comparison with the best applicable simpler
algorithm. This would show whether the current theorems identify a useful
tractable regime, rather than move the unresolved difficulty into an
uninterpreted numerical promise.

This is separate from checking that \(g>0\) exists for each individual
unique-optimum QP. It is also separate from verifying the answer without
knowing \(g\), which the current algorithms already do. The requested
advance is a meaningful quantitative family bound.

The parent's separable nonlinear plus low-rank concave interaction MINLP
extension is a sensible way to broaden the model while keeping a concrete
recourse oracle. It should keep the oracle's certified accuracy, feasible
witness representation, and discrete optimization cost explicit. But an
additional formal extension alone will not settle the conditioning question.
Even uniformly well-conditioned modewise problems can have distant nearly
tied global optima across modes.

The [linear-perturbation theorem](../new-direction/smoothed-linear-growth.md)
now supplies a reviewed answer in a random-input model. For independent
uniform linear noise of width \(2\sigma\), it gives an explicit global
growth bound with probability at least \(1-\rho\). For rational QPs,
a polynomial-bit rational noise grid gives

\[
g\ge\frac{\rho\sigma}{24n^2W},
\]

where \(W\) is the largest coordinate range. It applies to arbitrary
base quadratics on mixed boxes and continuous bounded rational polytopes;
no optimizer is planted and no winning face is supplied. Combined with
the two algorithms, it gives high-probability polynomial work at fixed
width or fixed negative inertia under the stated numerical scaling.

This directly addresses the principal interpretive weakness of an
unquantified growth promise. It also makes a distinction that the original
face-by-face approach obscured: a monotone optimizer-coordinate response
and a weak maximal-slope bound control distant competitors and local
flatness together. Exponentially many faces are used only to bound the
number of bad tilt intervals for rational discretization. Their logarithmic
count determines sampling bits; faces are not enumerated by the algorithm.

The [new source comparison](../prior-art/smoothed-linear-growth-prior.md)
already identifies qualitative generic quadratic growth under linear
perturbations and discrete randomized isolation as prior art. The possible
contribution is the explicit quantitative global modulus for continuous
domains and its finite-bit QP completion. Independent review and an
absence search still do not establish publication priority.

The new statement has important limits. It solves the perturbed objective.
Taking tiny noise to preserve an arbitrary original optimizer can destroy
the useful conditioning bound. Its runtime guarantee is high probability;
the available growth tail does not by itself bound the expectation of an
uncapped algorithm whose work is a higher inverse power of \(g\). Its
fixed-width or fixed-inertia corollary also needs numerically controlled
domain ranges, relevant curvature, noise scale, and failure probability.
Polynomial binary input size alone does not give that numerical control.

The most consequential remaining theoretical question is therefore whether
the high-probability result can be strengthened to an expected polynomial
work bound under a precisely specified perturbation model, or whether a
matching obstruction explains why this is too much to expect. That would
connect the conditioned algorithms to the usual expected-time notion of
smoothed complexity. It should not be claimed from the current tail bound.

The next validation should be small and targeted:
actual state or retained-cell counts against the most relevant baseline,
with the same certified tolerance and assumptions. A broad benchmark
campaign or more planted examples would not answer the central question.

## Work performed

This assessment used local source inspection, the existing completed proof
reviews, a delegated significance challenge, and messages to the existing
literature agents. The quantitative perturbation theorem was developed as
a separate follow-up, with its analytic reviews recorded in that artifact.
An inline `python3 - <<'PY'` document check passed for whitespace, paired
math delimiters, and all local links in this file and the perturbation note.
No executable optimization test, project-wide verification, CI inspection,
new external search by this assessor, or literature knowledge-base edit
was performed.
