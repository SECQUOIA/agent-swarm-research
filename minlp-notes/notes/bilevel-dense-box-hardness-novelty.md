# Source audit: scalar-leader hardness with a strongly convex box QP follower

Date: 2026-09-05. Bounded primary-source audit of
[the promoted dense-follower theorem](../results/bilevel-scalar-leader-spd-box-np-completeness.md).
The full draft, including the affine-upper gadget, constant gap, and NP
membership argument, was read. Independent agents review its mathematics.

The subsequent [no-upper-constraints extension](bilevel-dense-box-no-upper-constraints-extension.md)
was also read. It puts clause shortfalls into additional boxed follower
coordinates and their linear penalty into the upper objective. The strongest
current scope therefore has no upper constraints except `x in [0,1]`;
every leader is feasible. References below to upper constraints describe
the earlier version or the general allowed class, not a requirement of
the strengthened reduction. The promoted statement removes the redundant
`q` coordinates: it uses `2n+m` followers `y,p,v` and upper objective
`2 sum y_i - 2 sum p_i + 2 sum v_a`. Its two independent mathematical
reviews approved the strengthened statement.

## Assessment

No exact matching hardness theorem was found with all the stated
restrictions: one scalar leader, a fixed follower unit box, a rational
positive definite quadratic follower Hessian, affine dependence of its
linear cost on the leader, and an affine leader objective with no upper
constraints except the leader interval. The always-feasible gap `OPT=0` versus
`OPT>=2` would give a useful sharp boundary for the repository's structured
follower tractability theorem.

However, scalar-leader bilevel hardness, constant-gap reductions, ternary
digit extraction, and exponentially complicated strongly convex response
paths have close antecedents. The claim must be the combined restriction
to a fixed-box strongly convex follower, with explicit polynomial-bit data.
The path visiting Boolean assignments is also implied by an older Lasso
construction after duality; it should not be claimed as the first such path.

## Closest bilevel hardness result

Sugishita and Carvalho,
[Complexity of bilevel linear programming with a single upper-level variable](https://arxiv.org/html/2510.21126v2)
(v2, March 2026), Theorem 2.1, proves NP-completeness with one upper
variable, all variables in the unit interval, and no upper constraints
beyond lower optimality. Its 3-SAT reduction has optimum `-1` in the
satisfiable case and `0` otherwise. Section 4 and its supporting lemmas
use clipped piecewise-linear digit functions, weighted lower objectives,
absolute deviations from one-half, and a common fractional point. These
are particularly close mechanisms to the candidate and deserve direct
credit. The source uses a linear follower with additional coupled linear
constraints, rather than a fixed-box strongly convex quadratic follower.

The candidate's fixed box and unique response therefore give a different
restriction. Its newest version also removes all upper constraints, matching
that aspect of Sugishita--Carvalho. The distinguishing strengthening is the
pure-box follower with a fixed positive definite Hessian and unique response,
not absence of upper constraints or a first scalar-leader constant gap.

## A Boolean-vertex box path follows from the Lasso precedent

Mairal and Yu,
[Complexity analysis of the Lasso regularization path](https://arxiv.org/pdf/1205.0079)
(2012), Proposition 2, equation (4), recursively adds sign patterns
`[eta,0]` and `[+/-eta,1]`. Their square triangular design is invertible.
Theorem 1 attains `(3^p+1)/2` path segments. The recursion implies every
full sign vector whose last coordinate is `+1` occurs. The following box-QP
consequence is an inference from their construction and standard duality,
not a theorem explicitly stated in that paper.

For Lasso data `(X,v)`, let `u=X^T(v-Xw)/lambda`. Its normalized dual is

```
min_{u in [-1,1]^p}
    (1/2)u^T(X^{-1}X^{-T})u - t(X^{-1}v)^T u,
t=1/lambda.
```

At a full-support primal sign pattern, the dual equals that exact sign
vector. Thus a fixed SPD box QP with one scalar cost parameter already
visits every Boolean assignment in its first `p-1` coordinates after an
affine box change. This does not by itself supply a polynomial-bit
hardness reduction: the recursive small parameter choices and the useful
parameter interval still need encoding bounds. The candidate's explicit
rational weights and witness parameters address that separate issue.

Gartner, Jaggi and Maria's
[An exponential lower bound on the complexity of regularization paths](https://jocg.org/index.php/jocg/article/view/2955)
(2012; preprint 2009) is another direct predecessor: its SVM path has
exponentially many distinct support sets. Exponential path length rules
out uniformly short complete path enumeration. It alone does not prove
NP-hardness of optimizing a specified leader objective over that path.

## Other nearby primary results

Ketkov and Prokopyev,
[On the complexity of bilevel linear and quadratic programs in fixed dimensions](https://arxiv.org/html/2511.15592v2)
(June 2026), studies fixed follower dimensions. Theorem 4 gives a positive
result for optimistic convex quadratic problems with fixed follower
variable count. Theorems 5 and 6 concern pessimistic convex followers with
fixed constraint count and optimistic nonconvex followers, respectively.
These do not cover the candidate's growing follower dimension and unique
fixed-box convex response. The candidate does not settle their remaining
fixed-follower-constraint question.

Bolte, Le, Pauwels and Vaiter,
[Geometric and computational hardness of bilevel programming](https://arxiv.org/html/2407.12372),
Theorems 2.18 and 2.20, represents piecewise polynomial functions through
convex polynomial followers on boxes, including bounded boxes for the
appropriate semicontinuous class. Those constructions allow general
polynomial objectives and do not impose the fixed SPD quadratic follower
restriction. Their general polynomial hardness should be distinguished
from the much narrower construction here.

Justin P. Koeln,
[Exact feedforward neural network representations of multi-parametric quadratic programs with applications to explicit MPC](https://www.sciencedirect.com/science/article/pii/S0005109826003638)
(2026), gives exact ReLU and clipped-ReLU representations of parametric
QP solutions, including symmetric box constraints. The primary publisher
abstract and introduction were accessible; the complete paid paper was
not reviewed. Its stated result converts QPs to networks, with an
exponential worst-case neuron bound. It does not state the candidate's
inverse gadget construction or bilevel hardness theorem.

## Recommended positioning and limits

The result would show that fixed leader dimension and a simple follower
feasible set are insufficient without control of the follower's quadratic
interaction structure. This is a useful boundary next to a polynomial
algorithm based on bounded block/aggregate dimensions. It should credit
the scalar coding and absolute-deviation mechanisms above while emphasizing
their implementation inside one fixed-box, strictly convex QP.

Strong convexity means a positive definite Hessian for each encoded
instance. The exponentially separated weights do not establish a uniform
condition-number bound or strong NP-hardness with bounded numerical data.
The intended hardness is ordinary polynomial-bit hardness. With a unique
follower response, optimistic and pessimistic response choices coincide.
The newest version realizes all clause penalties within the follower
response and consequently needs no leader coupling constraints.

Any constant-gap conclusion concerns exact follower optimality. An
approximately solved follower may erase tiny gradient margins, so the
hardness should not be extended to a relaxed-response model without an
additional quantitative proof. Likewise, a path-length lower bound alone
cannot replace the 3-SAT objective-gap argument.

## Search record

Searches combined scalar/single/one-dimensional leader, strongly or
strictly convex quadratic follower, fixed box, affine upper objective,
NP-hardness, parametric box QP, and regularization-path complexity. The
sources above were the closest checked matches. No source found states
the full combined restriction. This is a bounded no-match assessment,
not proof that an equivalent reduction is absent from all literature.
