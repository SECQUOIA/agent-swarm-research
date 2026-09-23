# LB-ESH: adversarial literature and contribution assessment

Search and assessment date: 2026-09-19. Scope: the construction in
[the method note](lbesh-20260912-method.md), its
[scout](scout-20260912-convex-gdp-algorithms.md), and the
[previous implementation review](review-20260912-lbesh.md). This is a primary-source
literature assessment, not an independent validation of the current implementation
or numerical results. No solver runs were performed for this assessment.

**Assessment:** the current construction is an implementation and cut-selection
policy within established perspective-cut outer approximation. Its affine cuts,
reduced NLPs, finite approximation argument, and single-tree organization do not
individually support a new algorithmic-framework claim. A credible contribution
could be a careful computational study establishing when original-space radial
separation is useful in a GDP solver. Strong publication readiness depends on
that evidence; a useful prototype alone does not establish it.

## Primary-source comparisons

The following records describe details actually inspected. Equations and page
numbers refer to the linked manuscript versions, which may differ from the
published numbering.

### Perspective cuts

Frangioni and Gentile, *Perspective cuts for a class of convex 0–1 mixed integer
programs*, Mathematical Programming 106 (2006), 225–236:
[publication record](https://arpi.unipi.it/handle/11568/104242),
[author manuscript](https://arpi.unipi.it/retrieve/e0d6c92d-3c45-fcf8-e053-d805fe0aa794/01MINLP.pdf).
Section 2, equations (5)–(8), gives the perspective subgradient
`[s, c + f(p/u) - s·(p/u)]`, the corresponding affine inequalities, and an
outer-approximation scheme separating fractional solutions. Thus evaluating a
base function at the disaggregated ratio and transforming the affine cut is
established. LB-ESH changes the point at which the base function is linearized;
it does not introduce a different family of valid inequalities. The paper's
on/off epigraph setting is narrower than a GDP front end, but applies to its
individual lifted disjunct rows.

Bestuzheva, Gleixner and Vigerske, *A Computational Study of Perspective Cuts*,
[2021 author manuscript](https://arxiv.org/pdf/2103.09573).
Section 3, Theorem 2, explicitly identifies transformed base-function gradient
cuts with perspective cuts. Section 4 describes their integration with SCIP's
nonlinear handlers and separation; it treats general constraints and also
nonconvex estimators. Consequently, “generate original-space affine cuts and
extend them to indicators” is already an implementation strategy, beyond the
original separable-objective motivation. A fair practical comparison must
identify whether SCIP detects the relevant on/off structure in the tested input;
its mere presence on a solver list does not settle that question.

### ESH and its relation to Kelley cuts

Kronqvist, Lundell and Westerlund, *The extended supporting hyperplane algorithm
for convex mixed-integer nonlinear programming*, JGO 64 (2016), 249–272:
[publisher](https://link.springer.com/article/10.1007/s10898-015-0322-3).
The publisher abstract and the author's [thesis, section 4.1](https://www.doria.fi/bitstream/handle/10024/160918/kronqvist_jan.pdf?sequence=2)
were available; the publisher's full article was not needed to infer additional
unread details. ESH's LP initialization, interior-point root searches, and MILP
refinement are already central features. The complete root-search construction
also appears in section 2.2 of the Kronqvist–Misener manuscript below.

Serrano, Schwarz and Gleixner, *On the relation between the extended supporting
hyperplane algorithm and Kelley's cutting plane algorithm*:
[author manuscript](https://arxiv.org/pdf/1905.08157),
[published article](https://link.springer.com/article/10.1007/s10898-020-00906-y).
Sections 4–5, Propositions 6–7 and Lemma 8, identify radial boundary separation
with Kelley separation of a gauge representation. This is a major qualification
to theoretical novelty: applying radial support to each disjunct remains a
specialization of a known oracle. Their discussion also distinguishes residuals
under equivalent constraint representations. Row residuals should therefore
not be treated as representation-independent measures of solution accuracy.

### ESH with disjunctive strengthening

Kronqvist and Misener, *A disjunctive cut strengthening technique for convex
MINLP*, Optimization and Engineering 22 (2021), 1315–1345:
[manuscript](https://optimization-online.org/wp-content/uploads/2020/08/7957.pdf),
[publisher](https://link.springer.com/article/10.1007/s11081-020-09551-6).
Sections 3–5 optimize a fixed cut normal over separate terms of an exclusive
selection disjunction. Equation (13) gives `alpha·x <= sum_i b_i y_i`, with
`b_i` from separate convex optimization problems; Algorithm 3 combines this
with ESH. Their `ST` and `MT` mean single/multiple *tightening*, not single/multiple
branch-and-bound trees. They explicitly avoid evaluating nonlinear perspectives.
LB-ESH instead maintains disaggregated variables and can choose different normals
at different term boundary points using line searches. Neither construction is
identical to the other, and no general finite-cut dominance follows. Their
section 6.1 compares strengthened ESH against ESH on hull formulations, making
“ESH plus disjunctions without epsilon perspectives” too broad a novelty claim.

### Convex GDP cutting planes

Trespalacios and Grossmann, *Cutting Plane Algorithm for Convex Generalized
Disjunctive Programs*, INFORMS Journal on Computing 28 (2016), 209–222:
[publication](https://pubsonline.informs.org/doi/10.1287/ijoc.2015.0669),
[author manuscript](https://egon.cheme.cmu.edu/Papers/Trespalacio_gdp_cutting_planes_v2.pdf).
Section 3 constructs a separation NLP over a hull formulation strengthened by
basic steps; projected separating cuts improve a big-M formulation. See the
system (2a)–(2n), Propositions 3.1–3.2 and Figure 3. Their target relaxation may
be stronger than the independent-disjunction hull used by LB-ESH because basic
steps intersect disjunctions before convexification. LB-ESH avoids those
projection NLPs and keeps a lifted polyhedral master. Its cheaper individual-row
oracle trades against potentially weaker information; it does not subsume the
basic-step method. The manuscript describes preprocessing before solving the
resulting MINLP and identifies branch-and-cut as a possible extension.

### Logic-based OA

Türkay and Grossmann, *Logic-based MINLP algorithms for the optimal synthesis
of process networks*, Computers & Chemical Engineering 20 (1996), 959–978:
[full author copy](https://cepac.cheme.cmu.edu/pasi2011/library/grossmann/MetinLogOACACE.pdf).
The LOA algorithm on journal pages 963–965 combines selected-structure NLPs,
a hull representation of the linearized disjunctive master, bounds, and
set-covering initialization. Steps 3–7 spell out the NLP/linearization/master
cycle. Consequently, reduced NLPs that omit inactive units, and hull-transforming
linearizations rather than nonlinear equations, are inherited features.
LB-ESH can generate separating cuts without solving an optimization subproblem
at each cut point; that is a distinction from classical LOA's cut-point policy,
not from all established OA or separation methods.

### Conic GDP and conic OA

Bernal Neira and Grossmann, *Convex mixed-integer nonlinear programs derived
from generalized disjunctive programming using cones*, Computational Optimization
and Applications 88 (2024), 251–312; preprint 2021:
[publisher](https://link.springer.com/article/10.1007/s10589-024-00557-9),
[manuscript](https://arxiv.org/pdf/2109.09657).
Section 3, Theorem 1 and formulation HR-Cone use
`A_ik v_ik - y_ik b_ik in K_ik`, with disaggregation and scaled bounds.
This is an exact perspective-free cone representation under the stated hull
hypotheses. Table 1 includes nonlinear forms beyond quadratics. Thus
“nonquadratic” does not imply “no exact conic hull.” General expression oracles
may be more convenient than supplying a cone representation, but convenience
needs concrete examples and measurements.

Coey, Lubin and Vielma, *Outer Approximation With Conic Certificates For
Mixed-Integer Convex Problems*:
[full manuscript](https://arxiv.org/pdf/1808.05290).
Sections 2–4 develop LP OA with dual-cone cuts, certificates, tolerances and
fractional separation. Sections 5.3.2–5.3.3 describe iterative and MIP-solver-driven
implementations; the latter uses lazy and heuristic callbacks in one tree.
Section 6.3.1 explicitly tests separation-only variants against variants using
continuous conic subproblems. Hence cheap separation, optional optimization
oracles, and single-tree integration are established alternatives. A GDP-specific
implementation may preserve structure more conveniently, but these ingredients
are not by themselves a new solution paradigm. Pajarito or an equivalent exact
conic OA baseline is relevant on cone-representable tests.

### The user's quadratic-hull paper

Gusev and Bernal Neira, *Exact Hull Reformulation for Quadratically Constrained
Generalized Disjunctive Programs*, **v2, revised 2026-03-17**:
[current record](https://arxiv.org/abs/2508.16093),
[versioned manuscript](https://arxiv.org/html/2508.16093v2).
Section 3.1 gives GEHR; section 3.2 gives **Conic Exact Hull Reformulation
(CEHR)**. Proposition 2 and equations (18)–(22) establish the exact lifted system

```
v'Qv <= t y,   t + c'v + d y <= 0,   t >= 0,
xL y <= v <= xU y,   0 <= y <= 1.
```

Section 3.2.2 supplies the factorized rotated-SOC form; Appendix C compares
algebraic representations and discusses solver recognition. CEHR is the directly
relevant quadratic baseline, with the same continuous perspective hull as the
limit of the proposed cuts. The initial assessment inspected v1 and discussed
its weaker S3 alternative; that historical observation **does not describe v2's
CEHR**. The current comparison must cite v2. Appendix B retains the polynomial
homogenization extension, so polynomial examples alone do not establish novelty.

### Recent work and search limits

Nguyen and Pulsipher, *Solution Methods for Infinite-Dimensional Generalized
Disjunctive Programming*, [2026 manuscript](https://arxiv.org/html/2608.27707v1),
sections 3.3–3.4, extends projection cutting planes and LOA to infinite-dimensional
models. It is relevant background for modern GDP algorithms, not evidence that
the finite-dimensional radial oracle was previously absent. Searches also
covered combinations of “extended supporting hyperplane,” “logic-based,”
“disjunctive,” “perspective,” “gauge,” and 2025/2026 dates. The practical overlap with current `discopt` source is assessed below; it is
not used as a peer-reviewed priority claim. This review found no primary source establishing
priority for precisely the complete current LB-ESH policy. That statement is
an unsuccessful search outcome, **not proof of novelty**.

### Practical implementation overlap: discopt

The [MIP-NLP documentation](https://kitchingroup.cheme.cmu.edu/discopt/mip_nlp.html)
distinguishes algebraic OA/ECP/ESH from GDP reformulation. GDP is first converted
with big-M, hull, or multiple big-M; the native logic-based OA route is separate.
The experimental SHOT profile selects ESH, root-search policies, and single-tree
or multi-tree execution, with ECP fallbacks recorded in traces. Therefore this
is a candidate **independent algebraic ESH implementation**, not documented
term-by-term radial separation of an exact polyhedral GDP hull.

Source inspection on 2026-09-19 pinned repository HEAD to
[`52df59d141a79a0e79ecf652d7ca1d3d45e34a2a`](https://github.com/jkitchin/discopt/tree/52df59d141a79a0e79ecf652d7ca1d3d45e34a2a).
The package [manifest](https://github.com/jkitchin/discopt/blob/52df59d141a79a0e79ecf652d7ca1d3d45e34a2a/pyproject.toml)
identifies `0.8.1.dev0`, Python >=3.12, Rust/maturin, JAX, NumPy, SciPy,
POUNCE, and HiGHS dependencies. It was not installed or executed in this review.

In [`oa.py`, `_add_esh_cuts`](https://github.com/jkitchin/discopt/blob/52df59d141a79a0e79ecf652d7ca1d3d45e34a2a/python/discopt/solvers/oa.py#L3420),
the oracle uses the full algebraic evaluator, invokes `rootsearch_from_store`
with `fixed_discrete=True`, then generates OA cuts at the returned support point.
It falls back to ECP if a compatible interior or converged root search is absent.
This differs from LB-ESH's separate disjunct interiors and fractional
`v_ik/y_ik` separation. The
[hull implementation](https://github.com/jkitchin/discopt/blob/52df59d141a79a0e79ecf652d7ca1d3d45e34a2a/python/discopt/_relax/gdp_reformulate.py#L1128)
uses the Furman–Sawaya–Grossmann epsilon perspective, default `eps=1e-8`,
for nonlinear rows; its generated model is not the exact lifted-cut master.

**Baseline suitability:** potentially useful as a supplementary algebraic
ESH-after-reformulation comparator, but not yet a validated experimental baseline
and not a substitute for ESH/ECP ablation in the identical master. A pilot must
pin the revision, disable direct quadratic routing when measuring ESH, verify
that traces record actual ESH cuts rather than only fallbacks, and check primal
feasibility and bound orientation independently. GDP expressions would require
native translation or prior Pyomo reformulation: the
[Pyomo bridge](https://github.com/jkitchin/discopt/blob/52df59d141a79a0e79ecf652d7ca1d3d45e34a2a/python/discopt/pyomo/solver.py#L157)
round-trips algebraic models through `.nl`, losing the original GDP layer.
Static inspection also finds that `_build_results` assigns the incumbent to
Pyomo's lower-bound field for minimization and the solver bound to the upper-bound
field (lines 235–266). This appears reversed; it is a source-level finding,
not an executed reproduction. Read native result fields or validate/fix the
adapter before using its reported bounds. No claim about release stability,
priority, correctness, or performance follows from this limited source review.

## Exact algebraic relationship and limits

The following calculations are this assessment's direct derivations, included
to make the comparison falsifiable. They are not proposed as novel results.

For a differentiable convex row `g(x) <= 0`, let
`F(v,y)=y g(v/y)` for `y>0`. At `(v,y)=(tau z,tau)`, `tau>0`,

```
grad_v F = grad g(z),
dF/dy = g(z) - grad g(z)·z.
```

Its OA inequality is precisely

```
grad g(z)·v + [g(z)-grad g(z)·z] y <= 0.
```

This is the LB-ESH affine transform. With `z=v_hat/y_hat`, it is the usual
perspective ECP cut at the current point. With `z` on the radial zero boundary,
it is a perspective OA cut at another point. Avoiding division when constructing
the affine coefficients does not make the cut family different. Bounded scaled
variables give `v=0` at `y=0`, so every such cut is valid there without epsilon.

A complete collection of ordinary tangents at every base point already enforces
`g(v/y)<=0` for `y>0`: choosing the tangent point `z=v/y` recovers that
inequality. Therefore the two cut policies do not have distinct limiting
relaxation strength simply because one uses boundary points.

“Supporting” also does not imply dominance over a point tangent with a different
normal. Consider `g(x)=x1²+x2²-1`, interior point `a=(0,1/2)`, and candidate
`p=(2,1/2)`. The radial boundary point is `z=(sqrt(3)/2,1/2)`. The ESH and ECP
halfspaces, respectively, are

```
(sqrt(3)/2) x1 + (1/2) x2 <= 1,
2 x1 + (1/2) x2 <= 21/8.
```

At `(0,3)` only the ECP inequality holds; at `(2,-2)` only the ESH inequality
holds. Both comparison points lie in `[-3,3]^2`, and both inequalities are valid
for the unit disk. Setting the indicator to one embeds the same counterexample
in GDP. A generic statement that LB-ESH cuts dominate ECP cuts is therefore false.

For fixed interior points, radial boundary cuts are unchanged up to positive
scaling by replacing `g` with `phi(g)`, where `phi` is differentiable, strictly
increasing, `phi(0)=0`, and `phi'(0)>0`. The boundary point is identical and the
normal is multiplied by `phi'(0)`. This is a useful implementation diagnostic,
not a fresh theoretical foundation: the established gauge interpretation already
explains it. The claim does not automatically cover numerically computed
interiors, row selection, stopping residuals, or finite root-search tolerances.

## Defensible thesis and decisive experiments

A defensible working title is **“Radial and point separation for perspective-cut
outer approximation of convex GDP: a computational study.”** The narrower
question is whether choosing a disjunct boundary point gives enough bound
improvement to pay for its initialization and function evaluations. The current
literature does not supply that answer for this implementation.

1. Compare ESH and ECP within an identical lifted master, initialization,
   incumbent policy, tolerances, and solver/thread configuration. Attribute
   differences to the oracle rather than to different software packages.
2. Include exact conic hulls for quadratic, exponential, and other supported
   cone-representable families. Compare to a conic OA method when making claims
   about avoiding repeated continuous optimization solves. If a full conic OA
   baseline is unavailable, state the scope limit.
3. Report bound improvement versus elapsed time, row/gradient evaluations,
   number of cuts, LP iterations, and continuous-subproblem work. Include
   interior-point construction and compilation costs in end-to-end timings.
   Equal cut-count and equal-time comparisons answer different questions;
   neither should stand in for the other.
4. Separate root relaxation quality from complete certified solve performance.
   Count feasibility-checked incumbents and proven bounds, with common timeouts
   and paired instance sets. Do not use reference-objective agreement alone
   as an optimality certificate.
5. Test controlled curvature, dimension, term count, small positive indicators,
   thin/lower-dimensional terms, and alternative equivalent row representations.
   Include public nonquadratic application families; invented favorable examples
   can diagnose a mechanism but cannot establish broad usefulness.
6. Predeclare the interpretation of a negative result. If ESH has no reliable
   advantage, retain the implementation and the limits it establishes. The
   conclusions should become a modest computational finding, not a claim that
   an inherently stronger relaxation was discovered.

No generic new oracle-policy theorem presently emerges from these ingredients.
Compactness-based finite termination is necessary correctness work but is close
to standard cutting-plane arguments. Quantifying a useful regime may be valuable,
but an assertion of better worst-case oracle complexity would require a new
proof and lower-bound comparison, not a reformulation of the existing packing
argument. Strong-publication readiness remains conditional on a substantive,
independently checked finding from the experiments or an additional theoretical
result with a genuine comparison to these predecessors.
