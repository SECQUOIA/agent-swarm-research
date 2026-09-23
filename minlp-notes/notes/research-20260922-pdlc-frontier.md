# Candidate four-aggregation theorem for arbitrary strict PDLC systems

**Current result:** the simpler complete proof is in
[Four aggregations suffice for strict three-quadratic PDLC hulls](../results/four-aggregation-strict-pdlc.md).
It uses direct bounded inward perturbations, so the projective construction
below is now a superseded proof route. The polished upper bound holds in
every dimension; the sharpness verification covers `n>=3`.

Date: 2026-09-22. Status: research draft requiring independent adversarial
review. The proposed proof below is not yet a verified result. Its novelty
also requires comparison with Alex Dunbar's 2025 dissertation, whose relevant
statements were retrieved through indexed primary-source passages but whose
full PDF download returned HTTP 403.

## Proposed advance

Let `n >= 3`, let `Q1,Q2,Q3` be linearly independent real symmetric
`(n+1)`-square matrices, and put

```
f_i(x) = (x,1)^T Q_i (x,1),
S = {x : f_i(x)<0 for i=1,2,3}.
```

Assume `S` is nonempty and that a signed linear combination of the `Q_i` is
positive definite (PDLC). The candidate conclusion is that, whenever the
ordinary convex hull is proper, there are at most four nonzero nonnegative
multipliers `lambda^j` with

```
conv(S) = intersection_j {x : f_lambda^j(x)<0},
```

where every `Q_lambda^j` has exactly one negative eigenvalue and every
aggregation is good for the strict system. No boundedness, regularity of the
nonstrict feasible set, absence of points at infinity, or nonsingularity of
the original good aggregations is assumed.

The linearly independent case is the main setting of Blekherman–Dunbar.
A dependent triple should reduce to at most two extreme generators of its
pointed coefficient-matrix cone; that reduction is recorded separately below
and is not silently assumed in the proof.

The proof strategy uses the published Blekherman–Dunbar four-bound as an
input. Its proposed new content is a perturbation, projective-chart, and
strict-limit transfer that removes their geometric hypotheses for ordinary
strict hulls. If correct and not already present elsewhere, this would rule
out the six-aggregation possibility in BDS Conjecture 3.2 in its principal
three-independent-quadrics setting. The existing four-necessary example in
BDS would then make the upper bound sharp.

## Exact literature boundary

Sources examined on 2026-09-22:

1. Blekherman–Dey–Sun, *Aggregations of Quadratic Inequalities and Hidden
   Hyperplane Convexity*, SIAM J. Optim. 34(1), 2024. Local source:
   `literature/papers/blekherman2024-aggregations-of-quadratic-inequalities-and/fulltext.md`.
   Their Theorems 2.8 and 2.17 provide exact strict aggregation and the
   six-bound under PDLC for three quadratics and `n>=3`. Propositions 9.1,
   9.2, and 9.6 give PSD improvement, reduction to support two, and two
   endpoint multipliers per coordinate face.
2. Blekherman–Dunbar, *A Topological Approach to Simple Descriptions of
   Convex Hulls of Sets Defined by Three Quadrics*, SIAM J. Applied Algebra
   and Geometry 9(2), 2025, 310–342,
   [arXiv full text](https://arxiv.org/html/2405.18282v1),
   [published text](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full).
   Theorem 1.4 assumes PDLC, nonempty interior, `C=cl(int C)`, and no points
   at infinity for the nonstrict set `C`. It gives its closed hull using at
   most four permissible good aggregations. The exact section-8 proofs were
   inspected, including Propositions 8.6 and 8.10.
3. Alex Dunbar, *Leveraging Algebraic and Geometric Structures in
   Optimization*, Emory dissertation, Summer 2025,
   [record](https://etd.library.emory.edu/concern/etds/vq27zq10w),
   [PDF](https://etd.library.emory.edu/downloads/2j62s637x?locale=en).
   Indexed PDF passages explicitly state Theorem 5.0.5 with PDLC,
   `C=cl(int C)`, and nonempty interior, omitting the no-infinity condition.
   The indexed proof on page 124 cites Propositions 5.3.11–5.3.13, then
   separates the cases `n=1`, `n=2`, and `n>=3` using spectral-curve geometry.
   This is stronger than the published theorem's statement. The surrounding
   text still contrasts it with the conjecture about strict inequalities;
   it does not itself assert the full strict result considered here.
   Full-PDF inspection remains outstanding; search excerpts alone do not
   establish the complete assumptions or validity of the stronger theorem.

There is already a simple four-bound in a large subclass: if the PSD
multiplier cone contains a vector with any positive coordinate, the argument
of BD Proposition 8.6 eliminates the opposite coordinate face. Together with
BDS's strict support-two theorem it applies without the closed-set regularity
or infinity conditions. This is an extension of an existing proof, not the
main research contribution. The difficult coefficient geometry has the
entire PSD multiplier cone contained in the nonpositive orthant.

## Lemma A: finitely many bad inward levels

For a continuous semialgebraic function `h` on a compact semialgebraic set
`M`, there are only finitely many values at which `h` has a local minimum
(relative to `M`). Consequently, except at finitely many levels `c`,

```
{z in M : h(z)<=c} = cl_M {z in M : h(z)<c}.
```

Proof. The set of local minimizers is semialgebraic by quantifier
elimination. If its image under `h` contained an interval, semialgebraic
selection and piecewise continuity would give a continuous selection `z(c)`
on a nonempty open subinterval with `h(z(c))=c`, every `z(c)` a local
minimizer. Taking nearby smaller `c` contradicts the local-minimum property
at an interior point. A semialgebraic subset of the line with no interval is
finite. For the consequence, any point at level `c` not approachable from
below has a neighborhood on which `h>=c`, making `c` a local-minimum value.
Points strictly below `c` are already in the strict sublevel. The opposite
closure inclusion follows from continuity.

Apply this to the unit sphere and

```
h(z)=max_i z^T Q_i z.
```

For all but finitely many `epsilon>0`, the homogeneous nonstrict system

```
z^T (Q_i+epsilon I) z <= 0, i=1,2,3,
```

is the closure of its strict counterpart, away from zero and also at zero
when strict feasibility holds. The sphere condition is exactly
`h(z)<=-epsilon`. This is a generic-level statement, not a claim that every
positive perturbation is regular.

## Lemma B: a good cone survives inward perturbation

Suppose `lambda0>=0`, `lambda0!=0`, is good for the original strict system.
Normalize `sum_i lambda0_i=1`, and let `Q0=Q_lambda0`. It has exactly one
negative eigenvalue, since it is negative at every lifted feasible point.
The homogeneous strict sublevel `{z:z^TQ0z<0}` has two antipodal convex
components, including when `Q0` is singular. Goodness implies all lifted
points `(x,1)`, `x in S`, belong to one component `D+`: the lifted convex
hull is connected and lies in the strict sublevel.

For sufficiently small `epsilon>0`,

```
Q_i^epsilon=Q_i+epsilon I,
Q0^epsilon=Q0+epsilon I
```

has inertia `(n positive, 1 negative)`. Its two strict negative cones lie in
the original two components, one in each, because its negative sublevel is
a subset of the old one and its two components are antipodal. Orient the
new component `D_epsilon+` to lie in `D+`.

Let `S_epsilon={x:f_i(x)+epsilon(||x||²+1)<0 for all i}`. Then
`S_epsilon subset S`, and every lifted point of `S_epsilon` is in
`D_epsilon+`. Thus `lambda0` is also strict-good for `S_epsilon`.
Nonemptiness holds for all sufficiently small epsilon by fixing one point of
`S`. PDLC and linear independence persist under sufficiently small matrix
perturbations. Finally every fixed finite subset of `S` is contained in all
sufficiently small `S_epsilon`.

## Lemma C: the projective chart introduces no strict feasible points

Fix a small epsilon as above. Let `a_epsilon` be a negative eigenvector of
`Q0^epsilon`, oriented so that `l(z)=a_epsilon^Tz>0` on
`D_epsilon+`. Because `Q0^epsilon` is nonsingular with one negative
eigenvalue, `l` is strictly positive on the closure of that component away
from zero. Its restriction to `ker(l)` is positive definite.

Set

```
F_epsilon = {z : z^T Q_i^epsilon z<0 for every i}.
```

Then

```
F_epsilon intersect {l>0} subset {t>0},
F_epsilon intersect {l<0} subset {t<0},
```

where `t=z_(n+1)` is the original affine-chart coordinate.

Indeed, a point in the first set with `t<0` has antipode with `t>0`.
After division by its positive `t`, that antipode is a lifted feasible point
of `S_epsilon`, hence lies in `D_epsilon+`. But the original point already
lies in `D_epsilon+`, contradicting antipodality. A strict feasible point
with `l>0,t=0` would, by openness, give such a point with `t<0`. The second
inclusion follows by antipodality.

Consequently the chart `l=1` gives exactly a projective image `T_epsilon`
of `S_epsilon`. Both sets use all three strict inequalities; no additional
component-selection inequality is added to their descriptions.

The nonstrict three-inequality set `C_epsilon` in the chart `l=1` has no
points at infinity: any vector in `ker(l)` satisfying all three nonstrict
forms must satisfy `z^TQ0^epsilon z<=0`, hence is zero. It is bounded because
it lies in the bounded ellipsoid `z^TQ0^epsilon z<=0,l(z)=1`.
For generic epsilon from Lemma A it equals `cl(T_epsilon)`, and therefore
`C_epsilon=cl(int C_epsilon)` with nonempty interior. The matrices in this
chart are obtained by an invertible congruence, preserving PDLC,
independence, and aggregation inertia.

## Lemma D: strictification and global pullback

Apply BD Theorem 1.4 to `C_epsilon`. It gives at most four homogeneous
aggregations `p_j(z)=z^TQ_lambda^j_epsilon^epsilon z` such that in the
chart `l=1`,

```
cl(conv T_epsilon) = intersection_j {p_j<=0}.
```

Discard every aggregate polynomial that is globally nonpositive on this
chart. Such an inequality is redundant. A quadratic polynomial `p` that is
not globally nonpositive cannot have `p=0` at an interior point of
`{p<=0}`: that point would be a local maximum at zero, so its Hessian would
be negative semidefinite, its gradient zero, and its global maximum zero.
Hence for the remaining finitely many inequalities,

```
conv(T_epsilon) = intersection_j {p_j<0} in the chart l=1.
```

Here `T_epsilon` is nonempty and open, so its hull is open and equals the
interior of its closed hull. The identity for interiors of finite
intersections is valid because all sets contain the nonempty open hull:
strict satisfaction gives an interior point; an interior point of the
intersection is an interior point of each sublevel. At least one aggregate
remains because the closed hull is bounded. Each remaining multiplier is
nonzero and permissible, and the displayed identity makes it strict-good.

Let `G_epsilon={z:p_j(z)<0 for every remaining j}`. There is no nonzero
`z in G_epsilon` with `l(z)=0`: openness would produce points of
`G_epsilon` with arbitrarily small nonzero positive `l`, whose rescalings
to `l=1` are unbounded, contrary to boundedness of `conv(T_epsilon)`.
Thus

```
G_epsilon intersect {l>0} = cone_positive(conv(T_epsilon)),
G_epsilon intersect {l<0} = -cone_positive(conv(T_epsilon)).
```

Every point of `conv(T_epsilon)` has `t>0` by Lemma C and linearity of
`t`. Taking the section `t=1` therefore eliminates the negative cone. A
projective map whose denominator is positive preserves convex hulls:
equivalently, the positive conical hull of the lifts is independent of the
choice of its positive affine section. It follows that in the original
coordinates,

```
conv(S_epsilon) = {x:p_j(x,1)<0 for every remaining j}.
```

This establishes the global equality, including points outside the domain
where a projective formula with a positive denominator was initially
introduced. Omitting this step would leave a real gap.

## Lemma E: bounded-cardinality strict aggregation survives the limit

Take generic `epsilon_k downarrow 0` small enough for all preceding steps.
For each `k`, use the four-bound representation of `conv(S_epsilon_k)`.
Duplicate an existing multiplier if necessary to have exactly four, and
normalize each by `sum_i lambda_(k,j),i=1`. Pass to a common subsequence
such that `lambda_(k,j)->lambda_j` for all four indices.

Every limit lies in the nonnegative simplex and is nonzero.
The matrices

```
M_(k,j)=sum_i lambda_(k,j),i Q_i + epsilon_k I
```

converge to `M_j=Q_lambda_j`. The set of matrices with at most one
negative eigenvalue is closed, and `f_lambda_j(x0)<0` at any fixed
`x0 in S`. Thus each limit has exactly one negative eigenvalue.

It remains essential to prove *strict* goodness; nonstrict validity alone
would be insufficient. Choose unit negative eigenvectors `v_(k,j)` of
`M_(k,j)`, oriented to have positive scalar product with `(x0,1)`.
After subselection they converge to a unit negative eigenvector `v_j` of
`M_j`. For each fixed `x in S`, both `x` and `x0` eventually belong to
`S_epsilon_k`. The strict-good property of the kth aggregation implies
that their lifts are in the same negative-cone component, so

```
v_(k,j)^T(x,1)>0.
```

Taking limits gives `v_j^T(x,1)>=0`. But `f_lambda_j(x)<0` because all
three original constraints are strict and the limit multiplier is in the
simplex. A vector on the hyperplane perpendicular to the unique negative
eigenvector cannot have negative quadratic value. Therefore the scalar
product is strictly positive. All lifts of `S` lie in a single convex
component of `{z:z^TM_jz<0}`. Consequently `lambda_j` is strict-good for
`S`, and its inequality holds strictly throughout `conv(S)`.

Conversely, if `x` strictly satisfies all four limiting inequalities, then
by convergence it strictly satisfies all four kth inequalities for all
large `k`. Hence `x in conv(S_epsilon_k) subset conv(S)`. We obtain

```
conv(S) = intersection_(j=1)^4 {x:f_lambda_j(x)<0}.
```

No interchange between closure and convex hull is used in this final step.
The proof relies on fixed-cardinality compactness *and* the negative-cone
orientation argument; ordinary pointwise limits of closed inequality
representations would not suffice.

## Dependent triples and low dimensions

If `S` is strictly feasible, evaluation at a fixed lifted point of `S`
is strictly negative on every nonzero nonnegative combination of the
`Q_i`. Thus their finitely generated cone is pointed. If its dimension is
at most two it has at most two extreme rays, each represented by an original
constraint. All remaining original inequalities are nonnegative combinations
of these, so the original strict feasible set equals the system of at most
two extreme-generator inequalities. This geometric reduction is elementary.
For two quadratics, HHC follows from Dines' theorem on the joint range of
two quadratic forms, applied on each linear hyperplane. BDS Theorem 2.17
with `m=2` then gives at most `m²-m=2` good aggregations: its condition on
every triple is vacuous. Alternatively, the explicit two-dimensional-span
paragraph in BDS Section 2.5 gives this same extreme-ray reduction and cites
Yıldıran (2009), Theorem 1. The at-most-two result was also checked against
the openly readable author text of that paper, whose setting is strict
quadratic inequalities. Thus the proposed at-most-four conclusion extends
to dependent triples for `n>=3`. A one-dimensional cone reduces to one
inequality, or to two duplicated copies to apply the same theorem.

The BDS strict theorem used to obtain the initial good aggregation is stated
for `n>=3`. No unsupported claim for dimensions one and two is included.

## Verification and significance boundaries

This is presently a proof draft, not an independently verified theorem.
No numerical experiment could establish its quantified chart or limit
claims. Independent review should specifically challenge:

- whether all strict feasible points use the same Lorentz component;
- regularity of generic inward levels on the sphere;
- whether chart pullback reintroduces points at infinity or an antipodal
  component;
- strictification after deleting redundant globally nonpositive quadratics;
- closure of strict goodness in the varying feasible-set limit;
- the exact hypotheses of the published four-bound input;
- whether the dissertation or other primary work already contains this
  transfer or the full strict four-bound.

Only targeted literature inspection has been performed so far. No repository
wide verification or CI inspection was run.

If validated, the capability is an exact constant-size direct quadratic
aggregation description for every strict three-quadratic PDLC hull in the
stated dimension range. This improves structural understanding and caps the
number of essential inequalities; the proof does not provide an efficient
algorithm for discovering the four limit multipliers or establish a solver
speedup. The projective perturbation mechanism may be reusable for other
finite convexification bounds, but that is an open direction rather than a
proved general theorem here.

### First independent review and a shorter thesis-dependent route

Reviewer `review_pdlc_transfer` independently checked Lemmas A–E and reported
no gap, specifically confirming the negative-eigenvector limit and global
chart pullback arguments. The reviewer also checked the dependent-case
source reduction above. This is evidence of correctness, not a certificate
of novelty or a substitute for further review.

If Dunbar's dissertation Theorem 5.0.5 is valid under precisely its indexed
statement (without any no-infinity hypothesis), a shorter proof is possible:
use generic inward **constant** shifts `f_i+epsilon`, apply its regular
closed-set four-bound, strictify, and apply Lemma E. The generic-level
argument for `h=max_i f_i` on `R^n` does not require compactness; finiteness
of local-minimum values still follows from semialgebraicity. The signed
PDLC matrix perturbation is then `epsilon (sum_i theta_i) e_t e_t^T`, which
also preserves positive definiteness for small epsilon. The full
dissertation needs inspection before this alternative can be used.
The present published-source proof deliberately establishes bounded
projective regularizations and does not depend on that stronger statement.

## Later simplification: the projective step is unnecessary

After the full proof above was written and reviewed, a simpler route emerged.
If `conv(S)` is proper, no nonzero direction `d` can satisfy
`d^T A_i d<0` for every original quadratic. Otherwise, for every point `x`,
`x+td` and `x-td` both belong to `S` for all sufficiently large `t`, which
would imply `x in conv(S)` and hence `conv(S)=R^n`.

Consequently **every** positive uniform homogeneous perturbation
`Q_i+epsilon I` has no points at infinity in the original chart: a nonzero
`d` satisfying `d^T(A_i+epsilon I)d<=0` for all `i` would give exactly the
forbidden strict negative direction for the original system. Thus the
projective chart, initial good aggregation, and Lorentz perturbation
arguments are unnecessary for this application.

Generic regularity can also be obtained without semialgebraic theory.
For any continuous `h` on a space with a countable base, every bad level
`c` for the equality `{h<=c}=cl{h<c}` equals `inf_B h` for some member `B`
of that base. There are only countably many exceptional levels. Apply this
to `h(x)=max_i f_i(x)/(1+||x||²)` on `R^n` and choose negative levels
`-epsilon_k` increasing to zero. The nonstrict perturbations are regular,
bounded, and have no points at infinity. PDLC persists, so the published
BD four-bound applies directly. Strictification and the orientation limit
lemma complete the proof.

The earlier projective proof is retained as useful historical work and as a
check of the stronger intermediate facts, but the polished result should use
this simpler route. This also removes the need for an external strict
aggregation theorem to obtain an initial good multiplier in the independent
case.
