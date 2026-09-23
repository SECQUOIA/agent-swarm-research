# Research opportunity: exact design under Markov measurement errors

Date: 2026-09-12. Status: known-hull application; practical advantage remains
unverified. The subsequent
[priority audit](research-20260912-markov-priority-audit.md) found direct prior
art: Lee, Gómez, and Atamtürk's principal-inverse hull is mapped linearly to
the information hull below. The original candidate novelty claim is withdrawn.
The proofs, strict illustrative comparison, and implementation opportunity are
retained. The
[independent mathematical review](research-20260912-markov-theory-independent-review.md)
checks these results and supplies the qualifications incorporated here.

The leading direction is an exact convex MINLP formulation and a compact
optimization oracle for measurement-time selection with fully observed
Gauss–Markov error blocks. Its useful distinction from ordinary D-optimal design
is that selecting a subset changes the relevant inverse covariance. Its useful
distinction from a general correlated-noise convex formulation is use of an
established exact information-graph convex hull with a provably stronger
relaxation. A substantial contribution would require meaningful computational
improvements or an additional nonroutine algorithmic advance on constrained
process-model examples. The hull, its innovation calculation, and generic
Frank–Wolfe/branch-and-bound machinery are not new contributions.

## 1. Motivation and closest competitors

Wang et al., *Measure This, Not That* (2024), connects this problem directly to
Bernal Neira's interests: measurement selection, convex MINLP, Pyomo/MindtPy,
reaction kinetics, and carbon-capture parameter estimation. Its public code is
[measurement-opt](https://github.com/dowlinglab/measurement-opt). The
[arXiv manuscript](https://arxiv.org/abs/2406.09557) specifies coefficients using
blocks of the full inverse error covariance and activates pairs of selected
measurements. There is an important interpretation question: true marginal
subset information uses the inverse of the selected covariance, which usually
differs from a selected block of the full inverse. A separate source/code audit
is checking this; do not present it as an established error in the published
article on the basis of this note alone.

The following are essential competing or limiting sources, routed to the single
literature-maintenance agent. Bibliographic inclusion and full-text reading
status are maintained there.

| Source | Consequence for this direction |
| --- | --- |
| [Lee, Gómez, and Atamtürk, multi-period quadratic programs with indicators](https://arxiv.org/abs/2412.17178), DOI 10.1007/s10107-026-02379-5 | Direct prior art: the continuous ordered-path lift of padded selected-principal inverses, including blocks and binary-visit uniqueness. Sections 3–4 below are its information-space application. |
| [Pázman, Hainy, and Müller, convex correlated design](https://arxiv.org/abs/2103.02989), DOI 10.1214/22-EJS2071 | Their virtual-noise D-optimal upper bound is the same scalar-split extension as (4), after rescaling their design weights. It supplies correlated-design benchmarks and an exchange heuristic comparator. |
| [Sagnol and Harman, exact D-optimal MISOCP](https://arxiv.org/abs/1307.4953) | Already handles arbitrary PSD elemental information blocks and linear design constraints. Replacing scalar observations by independent blocks is not a contribution. Its conic machinery can solve the proposed arc model. |
| [Li et al., D-optimal Data Fusion](https://arxiv.org/abs/2208.03589), DOI 10.1287/ijoc.2022.0235 | Existing exact convex formulations, submodular inequalities, probing/optimality cuts, and energy-system experiments defeat a proposal consisting only of stronger routine logdet cuts for additive independent observations. |
| [Liu et al., correlated measurement noise](https://arxiv.org/abs/1508.03690), DOI 10.1109/TSP.2016.2550005 | Gives an exact binary-dependent Fisher expression for arbitrary covariance and an SDP relaxation, plus greedy methods. This is the main formulation baseline, even though its numerical objective is A-optimality. Its matrix extension can also support D-optimality. |
| [Dette, Pepelyshev, and Zhigljavsky, correlated regression errors](https://pmc.ncbi.nlm.nih.gov/articles/PMC4914140/), DOI 10.1214/15-AOS1361 | Established correlated-design theory and triangular/Gauss–Markov covariance calculations must be credited. Initial source inspection concerns continuous-time/asymptotic constructions, not the finite constrained path MINLP claimed here. |
| [Optimum experimental designs for dynamic systems in the presence of correlated errors](https://doi.org/10.1016/j.csda.2007.05.030) | Especially close application: multivariate chemical kinetics and measurement-time scheduling under correlated errors. Indexed primary material describes a numerical approximate-design procedure; full-text algorithm comparison remains necessary. |
| [Hendrych, Besançon, and Pokutta, mixed-integer convex experimental design](https://arxiv.org/abs/2312.11200) | Boscia and its Frank–Wolfe branch-and-bound approach are algorithmic competitors. A custom branch-and-bound engine or ordinary Frank–Wolfe gap is not independently novel. |
| [A column generation approach to exact experimental design](https://doi.org/10.1007/s12532-026-00326-1) | A recent direct competitor for scalable exact-design algorithms. Need distinguish generation of Markov observation paths from generation of ordinary candidate experiments. |
| [Kumar and Magbool Jan, process sensor-network design](https://doi.org/10.1016/j.jprocont.2026.103718) | Recent exact MISDP process-engineering work. Its stated target is steady-state Kalman state-estimation sensor selection, which is different from static-parameter measurement-time selection. |

The publicly readable Liu author PDF was downloaded to
`/tmp/minlp-design-opportunities-20260912/liu2016.pdf`. Its equation (11) is the
exact correlated-noise extension used below. The original pages, not a search
snippet, support this comparison. The follow-up audit established an exact
Markov path-hull match in Lee, Gómez, and Atamtürk. Old optimal-sampling papers
remain relevant for benchmarking, not for rescuing the disproved hull-priority
claim.

## 2. Exact block model

There are independent chains `g=1,...,G`. Chain `g` has ordered candidate times
`1,...,n_g` and a full observation block of dimension `r_g` at each time. Fix a
nominal parameter vector of dimension `p`. Let `F_gj` be the `r_g` by `p` mean
sensitivity matrix. The observation error itself, not merely an unobserved
component of the error, is a Gaussian Markov chain with known covariance.

For each `i<j`, write the conditional model as

```text
e_gj = Phi_gji e_gi + eta_gji,
Cov(e_gi) = P_gi > 0,
Cov(eta_gji) = Omega_gji > 0.
```

Here `eta_gji` is independent of errors at and before `i`. In a time-varying
state-space representation, `Phi_gji` is the product of one-step transitions and
`Omega_gji` is the accumulated innovation covariance. Equivalently,
`Omega_gji = P_gj - Phi_gji P_gi Phi_gji^T`. The covariance parameters are fixed
for the principal theorem. The sensitivities can come from a nonlinear process
model; then this is a local Fisher-information design problem.

Define positive semidefinite information matrices

```text
W_g,0j = F_gj^T P_gj^{-1} F_gj,
H_g,ij = F_gj - Phi_gji F_gi,
W_g,ij = H_g,ij^T Omega_gji^{-1} H_g,ij.
```

For selected times `S_g={i_1<...<i_k}`, the exact marginal information is

```text
J_g(S_g) = W_g,0i_1 + sum_{ell=1}^{k-1} W_g,i_ell i_(ell+1),
J_g(empty) = 0.                                                   (1)
```

Proof: the selected error vector remains a Markov chain. Apply the invertible
block triangular transformation that retains its first observation and replaces
each later observation by its innovation relative to the preceding selected
observation. The transformed covariance is block diagonal with blocks
`P_gi_1` and `Omega_g,i_(ell+1),i_ell`. The transformed sensitivities are
`F_gi_1` and `H_g,i_ell i_(ell+1)`. Congruence invariance of generalized
least-squares information proves (1). Independence between chains makes their
information additive. A prior or previous *independent* dataset contributes a
fixed matrix `J0`.

The scalar stationary AR(1) specialization has `P_i=1`,
`Phi_ji=rho^(j-i)`, and `Omega_ji=1-rho^(2(j-i))`. This supplies a transparent
initial test case while allowing multivariate, nonstationary errors in the
theorem.

## 3. Exact formulation with continuous arcs

For one chain, create the ordered acyclic graph with source `0`, candidate
vertices `1,...,n`, and sink `n+1`. Include source-to-candidate, increasing
candidate-to-candidate, and candidate-to-sink arcs, plus the direct empty-path
arc. Give candidate-to-sink and empty arcs information zero; all other arc
matrices are defined above. Let `y_e>=0` be a unit source–sink flow and let
`z_j=sum_{e entering j} y_e`.

**Exactness theorem.** With `z` binary, the continuous arc variables describe
exactly the unique ordered path visiting the selected candidates. Therefore

```text
maximize logdet(J0 + sum_g sum_e W_ge y_ge)
subject to unit flow in every chain,
           z_gj = sum_{e entering j} y_ge,
           z_gj binary,
           A z + B u <= b,  u binary                            (2)
```

is an exact convex MINLP for any additional linear selection/installation
constraints. The matrix `J0` is assumed positive definite in the computational
version, so the logdet domain is never an issue. The formulation has
`sum_g n_g` selection binaries and `O(sum_g n_g^2)` continuous arcs. Binary arc
variables are unnecessary.

To prove uniqueness, decompose any unit acyclic flow into source–sink paths.
Every path with positive mixture weight must visit any vertex with `z_j=1`
and must avoid any vertex with `z_j=0`. An ordered graph has at most one path
with a prescribed visit set. Hence every path in the decomposition is the same.
This also proves correctness when some arcs are deleted.

Minimum gaps can be imposed by deleting arcs whose successive measurement
times are too close. Candidate availability is handled by deleting vertices.
Mandatory visits can be enforced by deleting arcs that skip any mandatory
candidate, with the analogous source and sink deletions. Installation costs use
`z_gj<=u_g`; multiple chains can share an installation variable. Global budgets,
per-chain sample caps, and synchronized restrictions can be ordinary linear
constraints. Arbitrary extra constraints do not preserve the continuous
convex-hull property below, but they do preserve binary exactness.

## 4. Information-graph hull and domination

Let `P_g` be the admissible ordered paths encoded by the graph, and `chi(P)` its
binary visit vector. Pure unit network flow decomposes into paths. Because the
visit and information maps are linear, its projection is exactly

```text
conv{ (chi(P), J_g(P)) : P in P_g }.                              (3)
```

The analogous result for multiple independent chains follows from a product
of their path decompositions. Adding a fixed prior preserves the identity.
This is the convex hull of the *information graph*, not automatically the
convex hull of its nonlinear logdet hypograph. Maximizing logdet over (3) can
favor a mixture of designs. This distinction is essential.

Suppose `J_rel(z)` is any Loewner-concave matrix extension on the convex hull
of the graph-encoded binary designs, and `J_rel(chi(P))=J(P)` at every such
path, including paths excluded only by later side constraints. Every feasible
fractional path point has some decomposition

```text
z = sum_P lambda_P chi(P),
J_mix = sum_P lambda_P J(P).
```

Matrix concavity gives `J_rel(z) >= J_mix` in the positive-semidefinite order.
Consequently any increasing information criterion, including logdet with a
positive definite prior, has a path-relaxation upper bound no larger than the
bound from `J_rel`. This comparison remains valid after adding the same linear
side constraints in the `z,u` variables, provided the competing feasible set
contains the corresponding point. For matrix hypograph formulations one may
allow `X<=J_mix`, retaining the criterion's domain; monotonicity gives the same
optimum. Exactness only on the finally constrained binary designs is
insufficient for this statement about an unlayered graph intersection. This
is a generic Jensen consequence of the known graph hull.

For the Liu extension, concatenate sensitivities into `F`, let full error
covariance be `R>0`, and choose `0<a<lambda_min(R)`. Write `S=R-aI`. Then

```text
J_Liu(z) = J0 + F^T S^{-1} F
           - F^T S^{-1}(S^{-1}+diag(z)/a)^{-1}S^{-1} F.          (4)
```

For block selection, each selection value is repeated for its observation
coordinates in `diag(z)`. Formula (4) matches every binary subset exactly.
The inverse map is matrix convex, so (4) is matrix concave. Thus (3) dominates
this established correlated-noise relaxation. Pázman, Hainy, and Müller's
virtual-noise covariance is `R+a(diag(1/z)-I)` for positive `z`, after setting
`z=k xi` for their exactly-`k` design measure. Woodbury identifies its information
with (4); continuity supplies zero-coordinate limits. This is a comparison of relaxations
for the same exact statistical problem, unlike comparing with the fixed-full-
inverse pair formula mentioned in Section 1.

## 5. A strict rational example illustrating the known hull

Use one scalar chain, three times, one unknown mean parameter, prior `J0=1`,
and sensitivities `F=(1,1,1)^T`. Set

```text
R = [[1, 1/2, 1/4], [1/2, 1, 1/2], [1/4, 1/2, 1]],
z_1+z_2+z_3=1.
```

For any nonempty selected subset, the scalar information is
`1+sum_(successive i,j) (1-2^{-(j-i)})/(1+2^{-(j-i)}) <= |S|`.
Thus all path mixtures with expected count one have added information at most
one, and singleton paths attain it. The path relaxation and integer optimum are
both `log(2)`. No count layering is needed for this example.

For (4) choose `a=2/5`. The leading principal minors of `R-aI` are
`3/5`, `11/100`, and `7/2000`, so this choice is strictly admissible. At
`z=(1/3,1/3,1/3)`, the added information is

```text
1^T (R + 2a I)^{-1} 1 = 365/319 > 1.
```

Hence the competing bound is at least `log(684/319)`, giving a strict gap of
at least `log(342/319)` above `log(2)`.

Optimizing the scalar `a` cannot eliminate strictness in this example.
The Rayleigh quotient of `(1,-1,0)` gives `lambda_min(R)<=1/2`, so every
admissible `a` satisfies `a<=1/2`. Cauchy–Schwarz in the metric `R+2aI` yields

```text
1^T(R+2aI)^{-1}1 >= 9/(11/2+6a) >= 18/17 > 1.
```

This last statement concerns scalar splitting only. It makes no claim about
all diagonal or matrix splitting strategies or additional valid cuts applied
to (4).

## 6. Count layering and a small-dimensional relaxation oracle

Intersecting (3) with `sum z=k` permits mixtures of paths with different
numbers of visits. An exactly-`k` layered graph instead uses vertices `(ell,j)`
for the `ell`th selected time, `ell=1,...,k`, with increasing-time arcs between
successive layers. Only layer `k` reaches the sink. It has `O(kn^2)` arcs and
projects to the exact information-graph hull over admissible exactly-`k`
selections. For `k=0`, use only the empty path when consistent with mandatory
visits; infeasible count/mandatory combinations have no path. Minimum gaps and mandatory/forbidden visits can be imposed in the
graph. This strengthens the unlayered relaxation with a count equation when
count mixing would help.

Let `K` be a nonempty finite set of permitted complete designs at a branch-and-bound
node, each with information `J_P>0` including the prior, and let
`C=conv{J_P:P in K}`. The strongest information-mixture bound has the dual

```text
max_(J in C) logdet J
 = min_(H>0) [ max_(P in K) trace(H J_P) - logdet H - p ].        (5)
```

For any `H>0`, the right expression is an upper bound by the elementary
variational inequality `logdet J<=trace(HJ)-logdet H-p`. Conversely let `J*`
maximize logdet on `C`. Concavity and first-order optimality give
`trace(J*^{-1}J_P)<=p` for every permitted path. Choosing `H=J*^{-1}`
attains the primal optimum and proves (5).

In particular, any positive definite trial matrix `M` gives the valid bound

```text
U(M)=logdet M-p+max_(P in K) trace(M^{-1}J_P).                    (6)
```

For one chain with exactly `k` visits, the maximum in (6) is a longest-path
dynamic program taking `O(kn^2)` scalar operations after arc scores are known.
It uses the same allowed arcs and required visits as the candidate problem.
No general-purpose mixed-integer solver or dense selected-covariance inverse is
required by this pricing step. Formula (5) has only `p(p+1)/2` continuous matrix variables,
regardless of the number of candidate times.

Independent chains with a fixed count in each chain price separately. A fixed
global count can be handled by convolution of per-chain count-value tables.
Arbitrary budgets or installations may require a resource-constrained path
oracle or Lagrangian relaxation; an ordinary unresource-constrained longest
path must not be asserted to optimize those constraints exactly. The support
maximum must be computed exactly or replaced by a proved upper bound to certify
(6). A heuristic feasible path alone gives a lower bound on that maximum and
cannot certify the node. Pricing a superset of `K` is valid but can weaken the
bound; an empty `K` is handled as infeasible before using the dual.

A fully corrective Frank–Wolfe method can maintain a mixture of path
information matrices and use (6) as its stopping certificate. Branch on a
fractional marginal visit. If all marginal visits are binary, every positive-
weight path mixture has that same selection, so its information is an actual
design's information. This supplies an incumbent, not automatic termination:
the upper-bound certificate must also close. Any installation binaries must
also be feasible, either because `K` comprises feasible complete designs or
because they are handled separately. This suggests a compact exact-design
branch-and-bound implementation. The information hull, Frank–Wolfe,
branch-and-bound, count layering, and path pricing mechanisms are established.
Only a demonstrated substantive solver improvement or additional nonroutine
advance could support a new contribution. Comparison with Boscia and the 2026
column-generation paper is required before making stronger claims.

## 7. Scope, negative results, and prospective extensions

The full observed error must be Markov. If `e_t=u_t+v_t`, where `u_t` is a
stationary unit-variance AR(1) process and `v_t` independent white noise of
variance `tau^2>0`, then

```text
Cov(e_1,e_3 | e_2)=rho^2-rho^2/(1+tau^2)>0  (rho != 0).
```

This common nugget-noise model therefore fails the first-order Markov
assumption. Using its adjacent selected pairs in (1) is generally wrong.
Likewise, observing arbitrary coordinates of a vector Markov error can hide
state and destroy the observed Markov property. Grouping all coordinates into
complete measurement blocks is an actual restriction, not a harmless notation.
Cross-correlated chains must be merged into a joint observed block, if that
block really is Markov. Previous observations correlated with new measurements
can be modeled as mandatory observations in their chain, or through a correctly
derived conditional likelihood; they cannot generally be treated as an
independent additive prior with the unchanged new-observation likelihood.

Covariance parameters need not be fixed in a broader theorem: for any regular,
fully observed parametric Markov process, selected-observation likelihoods
factor into a first marginal density and gap transition densities. Transition
scores have conditional mean zero, so their cross information terms vanish.
Expected Fisher information is again a sum of precomputable source and arc
matrices. Gaussian formulas then acquire covariance-derivative and transition-
derivative terms. This is a prospective extension, not the initial software
scope. It requires dominated differentiable densities, differentiation under
the integral, square-integrable scores, and a Markov family in a parameter
neighborhood. Sampling is deterministic and does not intervene on the process.
The expected full Fisher matrix must include all parameter derivatives;
observed information and a fixed-covariance mean approximation are different
objects. Established Markov-process sampling-design literature, including
[Locally optimal designs for the simple death process](https://people.smp.uq.edu.au/PhilipPollett/papers/LOptimal.pdf),
already uses likelihood factorization and additive expected information.
[D-optimal designs for complex Ornstein–Uhlenbeck processes](https://arxiv.org/abs/1704.05719)
already studies joint mean/covariance-parameter design. Neither the extension's
information identity nor its generic path lift supports a new contribution by
itself; the priority audit records this negative finding.

The exact hull concerns information matrices. It does not prove the integer
design problem polynomial-time solvable, nor that a count-layered matrix
relaxation is tight, nor that an arbitrary correlated-noise objective is
submodular in selected time points. Arc-additive PSD information does permit
known additive-design cuts in the arc variables, but this is an application of
existing cuts rather than a new submodularity result.

## 8. Verification, experiments, and decision criteria

A direct independent numerical check constructed random time-varying block
Markov covariances with block dimensions 1, 2, and 3, chain lengths 3, 4, and 5,
four parameter sensitivities, and seed `20260912`. All 159 nonempty subsets
were checked by both direct selected-covariance inversion and (1). Maximum
relative entry error was `6.09e-16`. SymPy independently returned the exact
rational values and positive principal minors in Section 5. These checks
support the algebra but do not establish runtime value. The later fresh-agent
[independent mathematical review](research-20260912-markov-theory-independent-review.md)
also verified the main statements, including an exact rational block example
with a singular transition; its qualifications are incorporated above.

The smallest useful implementation comparison should use the same solver,
selection variables, prior, sensitivities, covariance, budget, and stopping
tolerance for (i) path logdet OA and (ii) the exact dense extension (4) with
logdet OA. Optimize or sensibly choose the scalar splitting parameter; report
it. For blocks repeat the selection variable over all block coordinates.
Use direct selected-covariance evaluation of every reported incumbent. On
small instances enumerate all subsets to validate both exact formulations.

The substantive benchmark should use process sensitivities from an openly
available reaction-kinetics or carbon-capture example, with a clearly labeled
Markov error model rather than falsely attributing that error model to the
original data. Include scalar and multivariate chains, multiple independent
instruments, shared installation cost, global budgets, and minimum time gaps.
Report root bounds, achieved optimality gaps, runtime, nodes, cuts, and memory;
separate data preparation from solving. Compare count layering and the compact
path-mixture oracle where they fit. Include a greedy/exchange incumbent method;
being better than plain greedy alone is insufficient evidence for the exact
solver's advantage.

Continue only if the next phase survives these concrete failure criteria:

1. This theoretical failure criterion has occurred: a primary source already
   states the equivalent Markov principal-inverse path hull. The hull claim is
   withdrawn. Continue only for a substantial practical solver advance or new
   nonroutine result, with the existing hull credited.
2. Realistic process noise requires nugget or partial-block models and no
   defensible application remains for the exact model studied.
3. The arc model's quadratic storage dominates its stronger bound, while the
   compact path oracle provides no compensating advantage on important sizes.
4. A fairly tuned dense exact formulation or established conic/Frank–Wolfe
   implementation matches the proposed method across useful instances.
5. Improvements depend on nearly singular priors, unnormalized covariance
   splits, weak competing cuts, or unfair stopping rules.

The remaining candidate is a specialized solver applying the known hull to
constrained correlated design. Its value remains an empirical question. The
current work does not establish a new publishable theory result. Ordinary
independent-block D-optimal design is also strongly covered by prior work.
