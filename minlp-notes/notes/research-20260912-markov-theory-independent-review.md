# Independent mathematical review of the Markov design proposal

Date: 2026-09-12. Reviewed file:
[research-20260912-design-opportunities.md](research-20260912-design-opportunities.md).
This review checks the mathematics from first principles. It does not audit the
implementation, establish priority, or independently check the literature.

The principal mathematical claims are correct under the stated model. No
counterexample was found to the block innovation identity, binary-visit
exactness, information-graph hull, correctly scoped dominance statement, strict
rational example, count-layered hull, or information-mixture dual. The main
needed changes are explicit qualifications about constrained hulls, pricing
certificates, and the scope of Fisher information. These qualifications matter
if the note becomes a theorem statement or an algorithm description.

| Claim | Verdict | Qualification |
| --- | --- | --- |
| Block selected-observation information identity (1) | Correct | The complete observed block is Markov; covariance is fixed with respect to the estimated parameters; relevant covariances are positive definite. |
| Continuous arcs with binary visits give an exact formulation (2) | Correct | Use a simple ordered acyclic graph and full flow conservation. Extra selection constraints preserve binary exactness. |
| Network projection equals the information-graph hull (3) | Correct | This is the hull of graph-encoded designs, before arbitrary extra constraints are intersected. |
| Dominance over matrix-concave binary-exact extensions | Correct with the stated graph domain | Binary exactness must hold at every design used in the path decomposition, including designs excluded only by later side constraints. |
| Liu extension (4) is binary-exact and matrix-concave | Correct | The scalar split satisfies `0<a<lambda_min(R)`; block indicators are repeated over their coordinates. |
| Strict example and persistence over all scalar splits | Correct | The claimed rational values and the uniform lower bound are exact. This says nothing about additional valid cuts or other splitting families. |
| Exactly-`k` layered graph gives the corresponding information hull | Correct | Handle `k=0` and infeasible mandatory/count combinations separately. |
| Dual (5), trial bound (6), and count pricing | Correct | The permitted design set is nonempty and information is SPD. Pricing is exact, or is replaced by a proved upper bound on its maximum. |
| Binary mixture marginals identify a design | Correct | This identifies an incumbent; an upper-bound certificate is still needed to close the node. |
| Parametric Markov extension | Correct as a prospective theorem | Requires a regular Markov family in a parameter neighborhood and expected full Fisher information, with all covariance and transition derivatives included. |

## 1. Block innovation identity

Suppress the chain index. Write the complete observation as
`Y_j=mu_j(theta)+e_j`, with zero-mean Gaussian errors, fixed covariance, and
`F_j=d mu_j/d theta` at the nominal parameter. For a deterministic selected set
`S={i_1<...<i_k}`, define a block lower-bidiagonal matrix `T_S` with identity
diagonal blocks and subdiagonal blocks `-Phi_(i_l,i_(l-1))`.

The transformed error vector is

```text
T_S e_S = (e_i1, eta_(i2,i1), ..., eta_(ik,i_(k-1))).
```

These blocks are mutually independent. Each gap innovation is independent of
all errors up to its preceding selected time; all earlier transformed blocks
are functions of those errors. Thus

```text
T_S R_SS T_S^T = D_S
              = blockdiag(P_i1, Omega_(i2,i1), ..., Omega_(ik,i_(k-1))).
```

The matrix `T_S` is invertible without any assumption that the state
transitions are invertible. Therefore

```text
R_SS^(-1) = T_S^T D_S^(-1) T_S,
F_S^T R_SS^(-1) F_S = (T_S F_S)^T D_S^(-1) (T_S F_S).
```

The rows of `T_S F_S` are precisely the source sensitivity and the gap
sensitivities in the note. This proves (1), including the full matrix-valued
information identity, not just a determinant identity. The empty set gives
zero information. Independent chains add because their likelihood scores are
independent and have mean zero.

The assumptions deserve these precise readings:

- Gaussian pairwise conditional regressions alone are insufficient. The gap
  residual must be independent of the entire preceding observed history.
- Positive definite innovation covariances are sufficient; transitions can be
  singular, nonnormal, time-varying, and noncommuting.
- Nonlinear means are allowed, but the fixed sensitivity calculation is local
  information at the specified parameter value.
- Selection is fixed independently of the observed outcomes, and collecting
  an observation does not change the process dynamics. An adaptive sampling or
  intervention model requires a separate likelihood argument.
- An independent previous experiment contributes its information. Treating a
  prior as a fixed positive definite information matrix is an explicit design
  convention; the calculation is not automatically a fully Bayesian
  parameter-integrated design criterion.

An exact rational check independently constructed a nonstationary two-state
chain of length four with three mean parameters. Its transitions included

```text
A_2 = [[1, 1/3], [0, 1/2]],
A_3 = [[0, 1],   [0, 1/4]],
A_4 = [[1/2, 0], [-1/3, 1]].
```

The middle transition is singular. Starting from
`P_1=[[2,1/2],[1/2,1]]`, with independent SPD innovations
`Q_2=[[1,1/4],[1/4,2]]`, `Q_3=[[2,-1/3],[-1/3,1]]`, and
`Q_4=diag(1,3)`, all 15 nonempty subsets gave exactly equal rational matrices
by selected dense inversion and by (1). No production oracle was used.

## 2. Binary visits and the information-graph hull

A nonnegative unit flow on the ordered DAG decomposes into source-to-sink
paths with weights summing to one. At every candidate `j`, the flow-defined
visit value is the weighted average of the paths' zero-one visit indicators.
If that average is zero or one, every path of positive weight has that same
indicator. When all visits are binary, every positive-weight path has the
same visit set. The increasing order fixes the path uniquely.

This establishes the asserted continuous-arc exactness. Deleting arcs or
vertices can remove that path, making the selection infeasible, but cannot
create a second path with the same visit set. Parallel arcs with different
weights, cycles, or unrelated state-expanded graphs would need a fresh
argument; they are absent from the stated construction.

The same decomposition proves the hull identity: the linear image of the
unit-flow polytope under `(y -> (z,J))` is exactly the convex hull of the
individual path images. For several chains, take the product distribution of
their path decompositions; it produces a convex combination of complete
multi-chain designs with the same visits and summed information. A fixed
prior is an affine translation.

Minimum gaps can be enforced by deleting forbidden successive-visit arcs.
For a mandatory candidate `m`, every arc crossing from an index below `m` to
an index above `m` must be deleted, treating source and sink as outside the
candidate range. In particular the empty path must be deleted when any visit
is mandatory. These rules are sufficient in an ordered graph.

With `J0` SPD, maximizing the concave function `logdet` of affine information
over the continuous flow constraints is a convex optimization problem, in
the conventional concave-maximization sense. Adding the selection and
installation binaries gives an exact convex MINLP. The stated selection
binary count excludes any separately introduced installation binaries.

If `J0` is merely PSD, the formulation remains meaningful with an explicit
SPD logdet domain, or with `logdet=-infinity` on singular PSD matrices. It
then needs at least one feasible SPD design for a finite useful objective.

## 3. Exact scope of dominance

Let `D` be the graph-encoded binary designs before later side constraints,
and let `J_rel` be Loewner-concave on `conv(D)` and exact at every element of
`D`. For any graph flow decomposition,

```text
J_rel(sum_P lambda_P chi(P))
    >= sum_P lambda_P J_rel(chi(P))
     = sum_P lambda_P J(P).
```

Adding a common prior preserves the order. Any Loewner-increasing criterion
therefore gives a path bound no greater than the competing bound, provided
the competing feasible set contains the corresponding `(z,u)` point. The
same linear constraints in `(z,u)` can be imposed on both sides because they
do not alter this pointwise inequality. If information is represented by a
matrix hypograph, require the criterion's domain as well as `X<=J_mix`.

This argument is valid for every matrix-concave binary-exact extension on
that domain. It is a general Jensen argument for a finite information graph;
the special value of the Markov assumption is the compact flow
representation of that graph's hull.

Do not strengthen the assertion to every extension that is exact only on
the *finally constrained* binary designs while retaining an unlayered flow
intersection. The following counterexample gives the distinction exactly.
Take two scalar observations with unit variance, correlation `1/2`,
sensitivities `(1,-1)`, prior `1`, and exactly one visit. Each singleton has
added information `1`, while the pair has added information `4`:

```text
(1,-1) [[1,1/2],[1/2,1]]^(-1) (1,-1)^T = 4.
```

An equal mixture of the empty and full paths has expected count one and
added information `2`. Consequently the unlayered hull intersected with
the count equation has optimum `log(3)`, whereas the singleton hull and
integer problem have optimum `log(2)`. The constant full-information
extension `J_rel(z)=2` is matrix-concave and binary-exact on the final
singleton-design polytope. It does not dominate that unlayered intersection
because it is not binary-exact at the empty and full paths used by its
decomposition. This does not refute the note's graph-domain theorem; it
shows why that domain must remain explicit.

### The dense extension

Set `S=R-aI>0`. For a binary selection, let `E` select its observation
coordinates, so `diag(z)/a=E^T E/a`, with repeated indicators for full blocks.
Woodbury gives

```text
(S^(-1)+E^T E/a)^(-1)
    = S - S E^T (aI+E S E^T)^(-1) E S.
```

Substitution into (4) leaves
`J0+F^T E^T (E R E^T)^(-1) E F`, exactly the selected-observation
information. For the empty selection the added term is zero.

The map `z -> S^(-1)+diag(z)/a` is affine and SPD. Matrix inversion is
operator convex there. Congruence by `S^(-1)F` preserves matrix convexity,
and negating the result gives the asserted matrix concavity. Thus the
dominance application is valid for all scalar and full-block selections.

## 4. Strict rational example

Every arithmetic claim in Section 5 checks exactly. For its three-point
covariance, the information values without the prior are

| Selected set | Information |
| --- | ---: |
| Empty | 0 |
| Any singleton | 1 |
| `{1,2}` or `{2,3}` | `4/3` |
| `{1,3}` | `8/5` |
| `{1,2,3}` | `5/3` |

These values also follow directly from (1), because a gap of length `d`
adds `(1-2^(-d))/(1+2^(-d))<1`. Every mixture with expected count one has
added information at most one; a singleton attains it. Both the path bound
and integer optimum are `log(2)`.

At the symmetric fractional point, the dense extension's added information
has the exact expression

```text
q(a) = 1^T (R+2aI)^(-1) 1
     = (24a+5)/(16a^2+18a+3).
```

At `a=2/5`, this is `365/319`. The leading principal minors of `R-aI`
are exactly `3/5`, `11/100`, and `7/2000`, so Sylvester's criterion verifies
strict admissibility. Adding the prior gives `684/319`, and the difference
from the path objective is at least `log(342/319)>0`.

The exact eigenvalues of `R` are

```text
3/4, (9-sqrt(33))/8, (9+sqrt(33))/8.
```

The note's weaker Rayleigh bound `lambda_min(R)<=1/2` is sufficient.
Cauchy–Schwarz gives, uniformly over every admissible scalar `a`,

```text
q(a) >= (1^T 1)^2 / (1^T (R+2aI) 1)
     = 9/(11/2+6a)
     >= 18/17 > 1.
```

Thus even the infimum over admissible scalar splits leaves a uniform
objective gap of at least `log(35/34)>0`. The same lower bound survives
the limit as `a` approaches the admissible endpoint from below. No
assertion about diagonal/matrix splits or strengthened dense formulations
follows from this calculation.

## 5. Count layering and limits of the hull

For `1<=k<=n`, attach layer `ell` to the `ell`th visited candidate. A path
starts at layer one, moves only from `(ell,i)` to `(ell+1,j)` with `i<j`,
and reaches the sink only from layer `k`. Give its source and gap arcs
the original information matrices. Each path is then in one-to-one
correspondence with an admissible exactly-`k` selection. The same linear
projection proof yields its exact information-graph hull. Source/sink arcs
contribute `O(n)` arcs and the interlayer arcs contribute `O(kn^2)`.

The two-observation example in Section 3 verifies that layering can
strictly improve an unlayered count intersection. For `k=0`, use the empty
path alone if compatible with the required visits; for impossible counts
or mandatory sets, report infeasibility.

Even a layered information-graph hull can have a strict integer gap.
For two candidates with sensitivities `(2,0)` and `(0,2)`, one visit,
unit marginal variances, and prior `I_2`, the two design information
matrices are `diag(5,1)` and `diag(1,5)`. Each integer objective is
`log(5)`. Their equal information mixture is `3I_2`, with objective
`log(9)`. Its visit marginals are `(1/2,1/2)`.

This also demonstrates that the information-graph hull with a nonlinear
logdet hypograph is not the convex hull of the discrete logdet hypographs.
Additional linear budgets, installations, or synchronization constraints
intersecting a flow formulation need not preserve the hull of individually
feasible complete designs.

## 6. Information-mixture dual and pricing certificate

Assume the finite design set `K` is nonempty and every `J_P` is SPD. Then
`C=conv{J_P:P in K}` is compact and stays in the SPD cone. For SPD `H,J`,
apply `log(t)<=t-1` to the eigenvalues of `H^(1/2) J H^(1/2)` to obtain

```text
logdet J <= trace(HJ)-logdet H-p.
```

Equality holds exactly when `H=J^(-1)`. This proves weak duality and every
trial bound (6), even if the trial matrix `M` is not in `C`.

Let `J*` maximize logdet over `C`. Its feasible-direction first-order
condition is

```text
trace(J*^(-1)(J_P-J*)) <= 0  for every P in K.
```

Thus `max_P trace(J*^(-1)J_P)<=p`. The reverse inequality follows by
averaging a convex decomposition of `J*`, whose trace is exactly `p`.
Choosing `H=J*^(-1)` therefore attains equality in (5). No exchange of
an unjustified minimax order is needed.

The dual objective is convex: its support-function term is convex in `H`,
and `-logdet H` is convex. It has `p(p+1)/2` matrix coordinates, but
evaluating its support term still requires optimization over the complete
permitted design set. Small dual dimension alone does not establish a
small algorithmic cost.

For one chain with a fixed count, set
`c_0j=trace(H W_0j)` and `c_ij=trace(H W_ij)`. With forbidden arcs omitted,
the recurrence is

```text
d_1(j)   = c_0j, if its source arc is allowed; otherwise -infinity,
d_ell(j)= max over allowed i<j of [d_(ell-1)(i)+c_ij].
```

Maximize `d_k(j)` over allowed sink arcs and add the constant
`trace(H J0)`. This is `O(kn^2)` scalar work after computing the scores.
Required visits can be encoded by the same skip-arc deletions. The
source contribution, prior contribution, and infeasible states cannot be
omitted. The phrase “no integer optimization” should be replaced by
“no general-purpose mixed-integer solver”: longest-path pricing is itself
a discrete optimization problem.

Separate chain counts give separate pricing problems. A shared total
count can be priced by convolving per-chain count tables. Other coupled
constraints may destroy this decomposition. In (5), `K` must include all
such constraints if the asserted bound is the strongest information
mixture bound for the actual node. Pricing a superset of `K` still gives
a valid, possibly weaker upper bound.

For an algorithm, the following distinctions are necessary:

- An exact support maximum or a proved upper bound on that maximum makes
  (6) an upper bound. A merely feasible heuristic path provides a lower
  bound on the support maximum and cannot certify (6).
- If a maintained mixture `M` lies in `C`, then `logdet(M)` is a feasible
  value for the continuous mixture problem, and the Frank–Wolfe gap is
  `max_P trace(M^(-1)J_P)-p`. The mixture value is generally not an integer
  incumbent value.
- A mixture with all binary visit marginals has one common visit set,
  so it yields an actual information matrix for that selection. This
  alone does not prove node optimality; the upper bound must also close.
- If arbitrary installation variables have only been linearly relaxed,
  binary visits alone need not give an integer feasible installation
  decision. Either maintain mixtures of feasible complete designs, as
  the definition of `K` requires, or handle those binaries separately.
- The identities are exact mathematical certificates. Floating-point
  code still has its stated feasibility, inversion, and optimization
  tolerances; this review does not validate those tolerances.

An empty `K` is an infeasible node, handled before the dual. The note's
SPD-prior assumption conveniently supplies the SPD information premise.

## 7. Observation and parameter scope

The nugget-noise counterexample is correct. For `rho=1/2`, `tau^2=1`,
three observations, and constant scalar mean sensitivity, the covariance
is

```text
R = [[2,1/2,1/4], [1/2,2,1/2], [1/4,1/2,2]].
```

Its conditional covariance `Cov(e_1,e_3 | e_2)` is `1/8`. Dense inversion
gives information `17/16`; incorrectly treating adjacent pairwise
regressions as independent innovations gives `11/10`, an overstatement
of `3/80`.

This also gives a literal partial-coordinate counterexample. Start with
the full Markov state `(u_t,v_t)` and use the invertible coordinate change
`(u_t+v_t,u_t)`. The resulting two-dimensional state is Markov with SPD
innovations, but observing its first coordinate alone produces the
non-Markov nugget process. Full-block observation is a substantive
restriction.

Correlated old and new observations cannot generally be handled by adding
the old information while retaining the unchanged new-observation model.
Making the old observations mandatory is one exact joint-likelihood
construction. An explicitly derived conditional-likelihood construction
can also be valid, so “must be modeled as mandatory observations” is
stronger wording than mathematically necessary.

Likewise, cross-correlated chains cannot be added as independent sources.
Combining synchronized complete measurements into a joint observed Markov
block is a valid remedy when its assumptions actually hold; merely
stacking asynchronous or partly observed latent states does not establish
the required observed Markov property.

### Parameter-dependent covariance and the prospective extension

For fixed deterministic observation times, suppose a Markov model has
dominated first marginal and gap-transition densities, differentiable in
a neighborhood of the nominal parameter, with differentiation permitted
under the integral and square-integrable scores. The Markov property must
hold in that parameter neighborhood, not just for the covariance at one
point. Write the selected likelihood as

```text
p_theta(y_i1) product_l p_theta(y_i_(l+1) | y_i_l).
```

Each transition score has conditional mean zero given the preceding
selected observations. It is therefore uncorrelated with every earlier
score. Expected full Fisher information is the sum of the initial score's
information and the expected transition-score outer products. Averaging
an arc term uses the unconditional marginal distribution at its preceding
time, which is independent of which other times were selected. Thus these
are precomputable source/arc matrices at the nominal parameter.

For a Gaussian family, an explicit correct arc formula helps prevent
accidentally reusing (1) when covariance is unknown. Let `theta_a` index a
parameter coordinate, `h_a=f_(j,a)-Phi_ji f_(i,a)`,
`Phi_a=partial_a Phi_ji`, and `Omega_a=partial_a Omega_ji`. Then

```text
W_ij[a,b]
 = h_a^T Omega^(-1) h_b
   + trace(Omega^(-1) Phi_b P_i Phi_a^T)
   + (1/2) trace(Omega^(-1) Omega_a Omega^(-1) Omega_b).
```

The source contribution is

```text
W_0j[a,b]
 = f_(j,a)^T P_j^(-1) f_(j,b)
   + (1/2) trace(P_j^(-1) P_(j,a) P_j^(-1) P_(j,b)).
```

These formulas use the derivative of the conditional mean at fixed
observed `y_i`, namely `h_a+Phi_a e_i`, and then average over `e_i`.
They reduce to (1) when covariance and transitions are parameter-free.
An independent exact rational two-state, two-parameter calculation, with
both parameters entering `P_i`, `Phi_ji`, and `Omega_ji`, matched these
terms against the full joint Gaussian covariance-derivative Fisher formula.
For example, a zero-mean scalar normal observation with variance
`exp(theta)` has Fisher information `1/2`, although its mean sensitivity
is zero; (1) alone would miss that information.

The additive statement concerns the full parameter information matrix.
Eliminating estimated nuisance parameters by a Schur complement generally
does not commute with summing source/arc matrices. For instance, two
independent observations with means `theta+eta` and `eta` each provide
zero effective information for `theta` after individually eliminating
`eta`, whereas their joint full information gives effective information
`1/2`. Retain nuisance coordinates in the additive information matrix,
or separately justify the resulting design criterion.

## 8. Reduction relevant to the separate priority review

The core hull is a direct linear image of a more general selected-inverse
graph. This is a mathematical reduction, not a literature finding in
this review. Let `E_j` select time block `j` from the full observation
vector and define the embedded selected inverse

```text
K(S)=E_S^T R_SS^(-1) E_S.
```

The same block innovation factorization gives

```text
K(S)
 = E_first^T P_first^(-1) E_first
   + sum_(successive i,j)
       (E_j-Phi_ji E_i)^T Omega_ji^(-1) (E_j-Phi_ji E_i).
```

The information is exactly `J0+F^T K(S)F`. Consequently, an existing exact
extended hull for `(chi(S),K(S))` immediately gives the claimed
information-graph hull by linear projection.

For invertible one-step transitions, write `T_j=A_j ... A_2` and `T_1=I`.
For `i<=j`,

```text
R_ij = P_i Phi_ji^T = (P_i T_i^(-T)) T_j^T.
```

Thus these Markov covariances have the usual triangular block-factorized
form. Singular transitions do not by themselves provide a persuasive
separation from a hull theorem stated for invertible factors: invertible
transitions can approximate them while initial and innovation covariances
stay SPD, and all finitely many selected inverses and innovation arc
matrices then converge. The precise assumptions and closure of a candidate
prior theorem still need checking by the separate literature reviewer.

Correctness of the present proofs therefore does not establish novelty.
Any claim that this information hull itself is new should wait for that
selected-inverse equivalence audit.
