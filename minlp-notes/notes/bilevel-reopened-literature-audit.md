# Literature audit for the reopened bilevel work

Date: 2026-09-06. Scope: exact compressed responses, practical quadratic
specializations, response approximation, and near-optimal robust followers.
This is a bounded source comparison, not a proof review or a certification
of publication priority. No matching complete theorem was identified for
the near-optimal robustness extension described below.

The audit read `literature/AGENTS.md` first. Existing paper packages and
generated literature files were not modified. Newly retrieved open PDFs
were inspected in `/tmp`; their durable source URLs and locators are below.
Local package citations use the package's PDF-page markers. Other PDF
locators explicitly distinguish printed pages from PDF pages.

## Claim-by-claim assessment

| Repository claim or proposed extension | Closest checked antecedent | Assessment |
| --- | --- | --- |
| Exact global optimization with fixed leader/resource/aggregate dimensions and many positive quadratic local variables | Megiddo–Tamir (1993); Ketkov–Prokopyev (2026) | Clipping, multiplier cells, and fixed-dimensional algebraic processing are established. The candidate distinction is the complete structural global-response theorem, including nonconvex aggregate costs. |
| Diagonal-plus-fixed-rank quadratic box follower solved by cellwise LP | Classical parametric QP and separable resource-allocation cells | Keep the existing “attributed structural corollary” label. Implementing and certifying this specialization would supply practical evidence; ordinary active-set/path tracking is not itself novel. |
| Accuracy-bit global optimization of signed affine response objectives for polynomial resource allocation | Hochbaum–Shanthikumar (1990), Vigneron (2014), Bemporad–Filippi (2006) | These precedents do not supply the checked combined theorem. Logarithmic accuracy for a single convex allocation solve and approximate parametric policies must be credited. |
| Safe upper inequalities from a uniform response error and a margin | Besançon–Anjos–Brotcorne (2024), Proposition 4 and Corollary 1 | The basic Lipschitz margin principle is established. A new claim needs the structured global complexity guarantee, useful exact certificate, or a sharper verified statement. |
| Exact global design against all cost-near-optimal responses in the compressed class | Besançon–Anjos–Brotcorne (2024), Section 3; their 2021 complexity paper | The uncertainty semantics and per-row adversaries are established. The sources checked do not give polynomial-bit global optimization for fixed leader/resource/aggregate dimensions with growing follower dimension, especially nonconvex aggregate cost. This is the most promising new mathematical extension from this audit. |

## Near-optimal robustness: the closest sources

**Besançon, Anjos, and Brotcorne, _Robust bilevel optimization for near-optimal
lower-level solutions_, JGO 90:813–842 (2024).**
[Open final PDF](https://publications.polymtl.ca/65063/1/2024_Besancon_Robust_Bilevel_Optimization_Near-optimal_Lower-level.pdf),
[preprint](https://arxiv.org/abs/1908.04040).

Section 2 defines cost-near-optimal followers and robustness of upper
constraints. Proposition 4, printed pp.822–823 (PDF pp.11–12), and Corollary 1,
p.823, give sufficient feasibility through Lipschitz slack balls. Section 3,
pp.823–825 (PDF pp.12–14), equations (9)–(14), treats each affine upper row
through a convex adversarial subproblem and duality. Slater assumptions
matter to the stated equivalence; weak duality alone gives sufficiency.
The paper develops finite reformulations and computational methods, not
an input-polynomial global algorithm for the repository's fixed structural
parameters. The proposed fiber-minimum argument also allows structured
nonconvex follower costs and does not require strict feasibility of a
near-optimal sublevel set. Those are precise differences, not grounds to
claim that near-optimal robustness or rowwise adversaries are new.

**Besançon, Anjos, and Brotcorne, _Complexity of near-optimal robust versions
of multilevel optimization problems_, Optim. Lett. 15:2597–2610 (2021).**
[Publisher](https://doi.org/10.1007/s11590-021-01754-9),
[open inspected preprint](https://arxiv.org/pdf/2011.00824).

The inspected preprint has ten pages. Definition 1 on p.5 defines a
complexity class stable under objective substitution and an added linear
constraint. Lemma 1, pp.5–6, transfers this property to adversarial problems.
Theorem 1 on p.6 gives a second-polynomial-hierarchy-level membership result.
Theorem 2, pp.6–7, gives NP membership under the convex `P*[H]` assumptions
and compatible upper rows. These are conditional membership results,
not polynomial-time global optimization in the fixed-dimensional class
considered here. The source's arithmetic and certificate assumptions
should not silently be imported into a new exact real-algebraic theorem.
No diagonal/block-plus-aggregate or fixed-leader parameter theorem was
found. The independent linear case discussed in Section 2 is materially
different from a follower whose cost depends on the leader.

The final-paper Edinburgh download returned HTTP 403. The arXiv preprint
was retrieved successfully; the page locators above refer to that preprint,
not the final journal version.

## Existing exact and approximation antecedents

**Ketkov and Prokopyev (2026), _On the Complexity of Bilevel Linear and
Quadratic Programs in Fixed Dimensions_.** The inspected version is
[arXiv v2, 10 June 2026](https://arxiv.org/html/2511.15592v2).
Table 2 is on local PDF p.5; Theorem 4 on p.18 assumes fixed follower
variable count and convex quadratic upper/lower objectives. Theorem 5 on
p.21 concerns pessimistic convex quadratic models with fixed follower
constraint count. Theorem 6 on p.23 concerns nonconvex followers with fixed
follower variable and constraint counts. Leader dimension may grow in
those hardness results. They do not cover cost-near-optimal response sets.
The repo lets follower dimension and box-row count grow and fixes leader,
resource, and aggregate dimensions. This is a different parameterization;
it does not resolve their fixed-total-follower-constraint open case.
[[ketkov2026-on-the-complexity-of-bilevel]] p.5, p.18, p.21, p.23.

**Megiddo and Tamir (1993).** Section 4, local PDF pp.6–10, explicitly
constructs low-dimensional multiplier cells for fixed-dimensional local
quadratic blocks and a fixed number of shared constraints. Page 8 describes
all intersections of local cells and their polynomial count. The source is
single-level convex optimization. The scanned extraction is poor, so use
the [author original](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf)
for quotation-quality statements. Do not claim new multiplier clipping or
new low-dimensional arrangement machinery.
[[megiddo1993-linear-time-algorithms-for-some]] p.6-10.

**Gärtner, Giesen, Jaggi, and Welsch (2009), _A Combinatorial Algorithm to
Compute Regularization Paths_.** [Inspected open PDF](https://arxiv.org/pdf/0903.4856).
Section 2, PDF p.2, recalls piecewise-linear parameterized QP paths;
Section 3, pp.3–4, develops a criss-cross approach handling degeneracy.
The low-rank application involves the entire quadratic matrix, and the
paper is a path algorithm rather than a fixed-rank-plus-diagonal global
bilevel bit-complexity theorem. It is a useful implementation antecedent
and reminder that singularity/degeneracy handling predates this work.

**Bemporad and Filippi (2006), _An Algorithm for Approximate Multiparametric
Convex Programming_.** Proposition 3.1, local PDF p.6, gives a feasible
interpolated response for jointly convex constraints. Algorithm 4.1,
pp.11–12, supplies prescribed value-function tolerance. Theorem 4.1, p.13,
is polynomial in output size; it is not an input-polynomial accuracy-bit
theorem. This is an appropriate approximate-parametric baseline, with
care over whether the guarantee is for follower cost, follower coordinates,
or the separately signed leader objective.
[Author PDF](https://cse.lab.imtlucca.it/~bemporad/publications/papers/coap-mp_convex.pdf).
[[bemporad2006-an-algorithm-for-approximate-multiparametric]] p.6, p.11-13.

Hochbaum–Shanthikumar's logarithmic-accuracy convex allocation theorem and
Vigneron's algebraic-sum approximation were already compared carefully in
[the existing source assessment](bilevel-resource-accuracy-bit-novelty.md).
The present audit checked the local paper notes and selected text; it does
not repeat their complete technical reading. Nothing found changes the
existing distinction between inverse-accuracy schemes and the repository's
accuracy-bit global signed-response result.

## Source caution worth retaining

The 2024 robust-bilevel paper's Corollary 2, printed p.823, appears to reverse
the required margin inequality. This is visible in the original PDF, not
just OCR. If every deviation has distance at most `R`, the Lipschitz
argument requires slack **at least** `K R`.

A direct check is `y in [0,1]`, follower cost `f(y)=y^2`, exact response
`yhat=0`, near-optimal budget `delta=1`, and upper row `G(y)=y-1/4`.
Here `K=R=1`, so the printed condition `|G(yhat)| <= K R` holds, but `y=1`
is an allowed near-optimal response and violates the row. This observation
is a caution against importing that corollary, not a research contribution
or a criticism of the valid Proposition 4 margin principle.

## Recommended development and proof boundaries

The most useful extension from this audit is **exact structured
near-optimal robustness**. An elementary fiber equivalence motivates it:
for an affine response statistic `s=a^T y`, the existence of a follower
with that statistic and cost at most `v(x)+delta` is equivalent to the
minimum follower cost on the additional fiber `a^T y=s` being at most
`v(x)+delta`. The extra equality is one resource row, so the compressed
framework can plausibly represent the fiber minimum without retaining all
follower variables. This is a proposed route; the theorem needs its own
proof and independent review.

Important obligations are global, not merely stationary, fiber minima;
empty fibers; closed versus strict violation; budget zero; leader-dependent
fiber normals; and attainment. With arbitrarily many robust rows, eliminate
each row's fixed-dimensional adversarial formula before conjoining the
results. Quantifying an independent adversary vector for every row in one
formula would destroy the fixed-variable argument. A fixed-dimensional
vector of upper statistics can be handled together, but a growing vector
requires a separate analysis.

For approximate low-rank structure, ordinary strong-convexity perturbation
bounds and Lipschitz transfer are useful but unlikely to constitute a
strong novelty claim alone. A practical certificate should exploit the
supplied structure, distinguish global uniform bounds from candidate-only
checks, and report feasible-design and objective bounds for the original
model. Do not equate a small Hessian residual with preserved exact upper
feasibility without a margin or a verified original-model calculation.

## Search record and limits

Searches on 2026-09-06 included combinations of: `bilevel diagonal low rank`,
`quadratic fixed rank bilevel`, `parametric quadratic low-rank`, `separable
low rank quadratic programming parametric`, `near-optimal robust separable`,
`near-optimal bilevel fixed dimension`, `robust bilevel diagonal quadratic`,
`bilevel aggregate nonconvex polynomial time`, `response approximation
constraints margins`, and the exact titles of the primary sources above.
Search results in neural-network adaptation and inverse-Hessian
hypergradient approximations were screened as different uses of low rank.

Henke's July 2025 dissertation, _Computational Complexity of Robust Bilevel
Optimization Problems_, was downloaded from the [TU Dortmund repository](https://eldorado.tu-dortmund.de/server/api/core/bitstreams/6dca98eb-28cb-4d89-ba8d-e7e60c059f98/content).
Only its front matter and text searches were screened: searches for
near-optimality, separability, and fixed-dimensional quadratic structure did
not reveal a matching theorem. It was not fully read and is not cited as
proof of absence. The Jones–Morari approximate explicit MPC paper is a
useful lead, but its download was rate-limited, so no exact theorem claim
is based on that source here.

The audit supports a qualified statement that the checked openly accessible
literature did not supply the complete proposed structured robustness
complexity theorem. It does not establish first publication, industrial
scalability, or correctness of any new repository proof.

## Follow-up audit of the developed drafts

Updated: 2026-09-07. This extension inspected the drafts
[certified surrogate cells](bilevel-reopened-approximate-structure.md),
[convex polynomial aggregate coupling](bilevel-reopened-nonlinear-aggregate.md),
and [near-optimal robustness](bilevel-reopened-near-optimal-robustness.md).
The following are source comparisons of their actual statements. Mathematical
acceptance remains the responsibility of the separate proof reviews.

### Exact dense quadratic optimization after certified status screening

The strongest defensible distinction is the complete `M 3^t` exact global
algorithm, where `M` is the size of a supplied rational polyhedral surrogate
response cover and `t` counts statuses that cannot be certified throughout an
entire cover cell. It preserves the true dense follower and exact affine upper
constraints. Three existing principles need explicit attribution: nearby-model
safe screening, parameter-region analysis, and affine recovery from a fixed
QP active set. The proof combines these; none is new individually.

**Dantas and Gribonval, _Stable safe screening and structured dictionaries
for faster L1 regularization_ (2019).**
[Open v3 manuscript](https://arxiv.org/pdf/1812.06635v3),
[publication](https://doi.org/10.1109/TSP.2019.2919404).
This is a closer antecedent than generic safe screening. Section III, PDF
pp.4–5, develops screening from approximate dictionaries with bounded atom
errors. Remark 2 on p.5 explicitly requires safety for the original problem,
not its approximate version. Theorem 1 on p.5 gives a corrected GAP Safe
sphere using a dictionary-error bound; Section IV, pp.6–8, combines structured
approximations and a switch to more accurate/original dictionaries. This already
establishes that a structured surrogate can safely eliminate variables of an
original dense model. Its target is solving a Lasso problem, with parameter
grids discussed as an application. It does not state the candidate's uniform
polyhedral-cell status certificates or the resulting `M 3^t` exact global
bilevel algorithm. Claiming novelty simply for “surrogate plus safe screening”
would overstate the contribution.

**Liu, Zhao, Wang, and Ye, _Safe Screening with Variational Inequalities and
Its Application to Lasso_ (2014).**
[Open paper](https://proceedings.mlr.press/v32/liuc14.pdf).
Section 2.2, PDF p.3, uses two variational inequalities at different regularization
parameters to enclose a target response; Theorems 2–3 on pp.4–5 compute directional
bounds used for screening. The repository's ellipsoid/support construction has
this direct methodological antecedent. Its whole-cell maxima, rational sign
tests, and subsequent exact bilevel status enumeration are the added structure.

**Ndiaye, Fercoq, and Salmon, _Screening Rules and its Complexity for Active
Set Identification_ (2021).**
[Inspected open manuscript](https://arxiv.org/pdf/2009.02709).
Proposition 1 on PDF p.4 gives a general feature-screening rule; Proposition 4
on p.8 constructs safe regions from strong dual concavity; Proposition 8 on
p.13 bounds identification iterations under linear convergence and a separation
quantity. This establishes screening and complexity of identification, but its
iteration bound is not the candidate's exact global complexity parameter `t`.
The candidate correctly permits many certified free coordinates and does not
assume that weak perturbation alone gives a small ambiguous set.

**Yang et al., _A Safe Screening Rule with Bi-level Optimization of ν Support
Vector Machine_ (2024).**
[Inspected open manuscript](https://arxiv.org/pdf/2403.01769).
Theorem 1 on PDF p.11 derives a sphere from variational inequalities; Corollary 1
on p.12 gives directional support bounds. Section 3.2, p.13, equation (18),
introduces an auxiliary optimization over the displacement used to tighten
that sphere. Its “bi-level” terminology therefore concerns construction of a
screening rule for ν-SVM. It should not be mistaken for the candidate's exact
global leader optimization with an arbitrary affine objective and upper rows.
This source still directly precedes box-status screening from paired optimality
conditions.

**Arnström and Axehill, _A Unifying Complexity Certification Framework for
Active-Set Methods for Convex Quadratic Programming_ (2020).**
[Inspected v2 manuscript](https://arxiv.org/pdf/2003.07605v2).
Section IV, PDF pp.5–9, and Algorithm 2 on p.6 partition the parameter set
according to the working-set sequence of a QP method. Theorem 1 on p.7 gives
an affine-iterate formula after a constraint removal; the paper also discusses
nonaffine iterates and quadratic parameter-region boundaries. Thus uniform
parameter-region analysis and exact active-set complexity certification are
established. Its subject is the iteration behavior of a prescribed QP algorithm,
not the candidate's supplied-surrogate cover with an exponential factor only in
uncertified coordinate statuses.

**Vreugdenhil, Nguyen, Eftekhari, and Mohajerin Esfahani, _Principal Component
Hierarchy for Sparse Quadratic Programs_ (2021).**
[Open paper](https://proceedings.mlr.press/v139/vreugdenhil21a/vreugdenhil21a.pdf).
The model on PDF p.1 is a cardinality-constrained quadratic program with a
ridge term. Proposition 3.1 on p.4 supplies a low-rank min–max characterization;
Propositions 3.3 and 3.5 and Remark 3.4 on pp.5–6 develop algorithms and discuss
screening. This is a nearby use of spectral approximation, variable screening,
and global combinatorial structure. It does not state an exact parametric
box-response theorem or the candidate's cellwise ambiguity bound. No claim is
made here that its screening certificates are interchangeable with the new
ones; that would require a separate proof.

No identical `M 3^t` theorem was found in these inspected sources. Its likely
paper value is a **verifiable sufficient route to exact dense bilevel solutions**,
with candidate-dependent exponential complexity. It is not evidence of a
worst-case small `t` or of a speed advantage. Screening conservatism and the
cost of rational dense linear algebra need to remain visible in experiments.

### Convex nonlinear aggregates with accuracy-bit global optimization

The developed theorem fixes leader, aggregate, and resource dimensions while
allowing many strictly convex polynomial local costs. Its stronger point is
polynomial dependence on requested accuracy bits for a signed affine upper
objective, with an exactly feasible rational leader. It is not a new method
for one convex allocation problem, a new duality principle, or a general
polynomial-time algorithm for convex-follower bilevel optimization.

**Jeyakumar, Lasserre, Li, and Pham, _Convergent Semidefinite Programming
Relaxations for Global Bilevel Polynomial Optimization Problems_ (2016).**
[Inspected manuscript](https://arxiv.org/pdf/1506.02099),
[publication](https://doi.org/10.1137/15M1017922).
Theorem 2.3, PDF pp.5–6, establishes a Hölder estimate for polynomial lower-level
solution maps. Proposition 3.2 and Remark 3.3 on pp.9–10 explain the convex
reformulation and regularity requirements. Theorem 3.5 on p.12 gives convergence
of SDP lower bounds under the stated compactness, Slater, and nondegeneracy
assumptions; Theorem 4.7 on p.19 addresses the general polynomial setting.
These are global polynomial bilevel predecessors, but do not give the candidate's
fixed-aggregate accuracy-bit complexity and rational output theorem. The
candidate's normal-cone/repair argument also accommodates degenerate polyhedral
followers, including equalities encoded as pairs of inequalities.

**Ouattara and Aswani, _Duality Approach to Bilevel Programs with a Convex
Lower Level_.**
[Inspected manuscript](https://arxiv.org/pdf/1608.03260).
Section II-C on PDF p.2 states R1: strict follower feasibility for every leader.
Theorem 1 on p.3 analyzes the constrained dual; Proposition 4 on p.5 connects
local solutions of the reformulation; Section IV-C and Proposition 6 on p.6
study consistency under regularization. This is a direct antecedent for
convex-duality reformulation and approximation consistency. It does not supply
the fixed-dimensional branch construction, degree-dependent inverse modulus,
or polynomial accuracy-bit global guarantee claimed in the draft. Replacing
its regularity assumptions is meaningful only as part of that complete theorem.

**Vidal, Gribel, and Jaillet, _Separable Convex Optimization with Nested Lower
and Upper Constraints_.**
[Inspected manuscript](https://arxiv.org/pdf/1703.01484).
Section 3.2, PDF pp.19–20, discusses representability and precision. Section 3.3
on p.21 gives `O(n log(m) log(nB/epsilon))` operations for the continuous
nested-allocation problem and `O(n log m)` for linear/quadratic special cases.
This is explicit logarithmic-accuracy allocation work and must not be omitted
when discussing accuracy bits. Its objective is the allocation cost, not an
independently signed objective of the allocation response optimized globally
over leader decisions. Its operation-count statement also should not be
silently promoted to the candidate's fully specified rational bit model.

Together with the earlier Hochbaum–Shanthikumar, Vigneron, and
Bemporad–Filippi comparisons, these sources do not contain the new combined
convex-aggregate theorem. The natural contribution wording is:

> With fixed leader, aggregate, and resource dimensions, global additive
> optimization of an affine leader objective over the unique polynomial
> follower response is polynomial in input size, numerical degrees, and
> accuracy bits, with exactly feasible rational leader output, even without
> uniform strong convexity or strict follower feasibility.

This statement needs the complete model restrictions: densely encoded strictly
convex univariate local costs, convex polynomial aggregate cost, fixed
leader-independent aggregate/resource matrices, and no additional
response-dependent upper constraints. The technical extensions over the old
repo theorem are aggregate-mismatch control and rational recovery across
nonlinear branch boundaries. Neither generic approximate KKT sufficiency nor
fixed-dimensional semialgebraic optimization is claimed new.

### Final positioning of exact near-optimal robustness

The developed draft goes beyond the earlier affine-row proposal by permitting
polynomial upper criteria in a fixed number of criterion-specific measurements.
The measurement matrices may differ across arbitrarily many criteria. Compared
with the inspected 2021 and 2024 near-optimal robustness sources, a precise
candidate statement is:

> For fixed leader, local-block, aggregate, resource, and per-criterion
> measurement dimensions, exact robust feasibility, infimum, attainment,
> and algebraic adversarial witnesses can be computed in polynomial input
> bit time for cost-near-optimal followers. The follower dimension and number
> of independently measured upper criteria may grow, and aggregate follower
> costs may be nonconvex.

The comparison supports this narrow structural-composition claim, conditional
on proof acceptance. It does not support a new near-optimal response model,
a new general value-function projection principle, or a new theorem about
unrestricted dense polynomial upper criteria. Processing each criterion's
quantifiers separately is essential to the stated growing-row guarantee.
The convex fixed-normal attainment subclass is a useful consequence of
classical continuity and maximum-theorem arguments, not a separate novelty
claim on the present evidence.

The follow-up searches focused on `safe screening parametric quadratic
programming`, `safe screening approximate dictionary`, `safe screening region
parameter space`, `safe screening low rank`, and combinations of `bilevel`,
`aggregate`, `polynomial`, and `logarithmic accuracy`. All PDFs used for the
new detailed comparisons above were retrieved successfully and their cited
sections inspected. This was targeted follow-up rather than a repeat of the
completed initial searches.
