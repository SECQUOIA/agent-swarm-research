# Independent review: spatial covers with the exact quadratic moment hull

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-beyond-clique-investigation.md`, including its
product-coordinate-domain extension and subsequent scaling remark.

**Verdict: PASS within the explicitly defined region-cover oracle model.**
The transfer, quadratic realization lemma, source-to-moment degree
conversion, random-instance/deletion argument, and product-domain extension
are correct. No substantive proof defect was found. The author added the
appropriate qualification for objective propagation and explicit source
parameters during review. Novelty remains a separate question.

## Transfer functional and full node preordering

For a node containing a Boolean witness, the restricted coordinates can
indeed be set to their witness signs regardless of their correlations
under the original pseudoexpectation. The operation is substitution
followed by marginalization, not conditional expectation. Its domain
contains every requested polynomial of degree at most `2r`.

After substitution, every restricted-coordinate slack is a nonnegative
constant. On each remaining coordinate, the slacks are `1+x_i` and
`1-x_i`. Boolean reduction of their product is zero if a conflicting
pair occurs, and otherwise is a positive constant times an assignment
indicator `I`. Repeated slack factors merely change that constant. If
the indicator uses `v` coordinates, then `v<=deg(g)`.

Write `d=deg(p)` for the original square multiplier. Substitution cannot
increase this degree. The Boolean identity

```
I p^2 = (I p)^2
```

is valid through degree `2(v+d)`, and

```
v+d <= deg(g)+d <= 2r-d <= 2r.
```

Thus its squared right-hand side is within degree `4r`, and the original
pseudoexpectation's PSD condition proves every required node preordering
inequality. This establishes positivity for all allowed products, not
only the moment matrix and individual slack localizers. The factor-two
loss between the node degree and the imported pseudoexpectation degree
is correctly charged.

Let `mu` realize the original first and second moments. Its marginal on
the unrestricted coordinates, combined with deterministic restricted
signs, is an actual distribution supported in the node. For restricted
and unrestricted indices its cross moments are respectively the
appropriate products of the fixed signs and unrestricted first moments,
which agree with substitution in the pseudoexpectation. Therefore the
entire degree-two moment vector, including diagonal and cross entries,
belongs to the exact node moment hull.

## Clause loss and cover counting

A clause avoiding restricted coordinates retains expectation zero for
its cost. Every other clause has expected cost in `[0,1]`. In fact a
touched clause leaves at most two unfixed variables; the realizing
degree-two distribution already proves this bound. The draft's stronger
argument using Boolean PSD through degree six also works because `r>=2`
and the imported degree is at least eight.

At most `Delta|R|` clauses touch a restricted coordinate, counting
repetitions and permitting overcounting. Hence

```
LB_r(B) <= L[F] <= Delta|R|/m.
```

A pruned node therefore requires `|R|>=mT/Delta`. Each such coordinate
permits at most one Boolean witness sign. A containing box has at most
`2^(n-|R|)` witnesses, so its fraction is at most `2^(-mT/Delta)`.
The reciprocal union bound proves the claimed cover size. No integrality
rounding problem arises when `mT/Delta` is noninteger.

The multiaffine objective attains a minimum at a cube vertex: holding
all other coordinates fixed, one can move a coordinate to an endpoint
without increasing its affine dependence. Repeating this for all
coordinates proves the equality of continuous and Boolean minima.
Every clause cost lies in `[0,1]` on the whole cube, as claimed.

## Exact realization of signed first and second moments

The augmented Boolean moment matrix has diagonal one and is PSD. Its
Gram vectors are unit vectors. An inner product of absolute value one
forces equality up to sign. This relation partitions the vectors into
signed classes; between distinct classes the inner product is zero,
because the only permitted entries are zero and signs.

Choose independent unbiased Boolean signs for the classes other than
the class containing the constant vector. Orient that class so the
constant vector has sign `+1`, and set its random variable to one.
Within every class, multiply by each coordinate's orientation sign.
The resulting actual distribution gives exactly the original means
and pair moments. This also covers coordinates of mean `+1` or `-1`,
and perfectly correlated or anticorrelated coordinates.

Supplementary exact checks generated 100 signed-class systems with nine
coordinates and up to four free classes. Enumeration of their Boolean
class assignments recovered every specified first and second moment
exactly. The proof, rather than these examples, establishes the lemma
for all dimensions.

## Verification of the imported source

The primary source was read directly, including Theorems 11–12, Lemma 13,
and its signed character-vector construction. Set `k=3`, density `d=8`,
`delta=1/4`, source exponent parameter `epsilon=0`, and `gamma=1/4`.
The density requirement is `d>=1+8 ln(2)<8`. Theorem 11 gives positive
linear resolution width with high probability. Lemma 13 maps width `w`
to level `w/2`; its signed basis vectors and product-consistency identity
give the required character moments. These statements are in
[Schoenebeck, full version, printed pages 7–11](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf).

More explicitly, index vectors by characters of support at most `w/2`.
For `|S|<=w`, assign its moment the derivable parity sign, or zero if
that parity is absent. For `|I|,|J|<=w/2`, product consistency gives
the moment of `I symmetric-difference J` as their Gram inner product.
Consequently the functional is PSD through squared degree `w`, with
all character moments zero or signs. Thus `4r<=w` suffices; equivalently,
Lasserre level `ell` gives polynomial degree `2ell`. Renaming the
positive linear-degree constant as `a` justifies `r<=an/4`.

Choosing `gamma=1/4` avoids the zero denominator produced by a literal
use of the source's informal `gamma=1/2` example when `k=3`. No such
singular parameter choice is needed for the candidate.

## Random sampling and occurrence deletion

For a fixed assignment, the independent uniform clause signs make its
violation count exactly `Binomial(8n,1/2)`, irrespective of dependencies
among sampled variable sets. Hoeffding bounds the probability of at
most `2n` violations by

```
exp(-2(2n)^2/(8n))=exp(-n).
```

The union bound over `2^n` assignments tends to zero because `ln(2)<1`.
Thus every assignment violates at least `2n` clauses with high probability.

Each original occurrence count has law `Binomial(8n,3/n)`. Independence
between the occurrence counts is not needed. The stated estimate is

```
E[D_i 1_(D_i>64)]
<= 2^(-64) E[D_i 2^D_i]
= 48(1+3/n)^(8n-1)/2^64
<= 48 exp(24)/2^64
< 6.9 * 10^(-8) < 1/8.
```

Linearity of expectation and Markov therefore bound the probability of
deleting more than `n` clauses by less than `1/8`. No concentration
or independence assertion about high-degree vertices is required.
The complement of that deletion event intersects both high-probability
events for every sufficiently large `n`.

On the intersection, retained clauses number between `7n` and `8n`,
every retained variable occurrence count is at most 64, and every
assignment violates at least `n` retained clauses. The normalized
minimum is therefore at least `n/m>=1/8`. Deleting constraints leaves
the same pseudoexpectation feasible and preserves all signed character
moments. The lower bound at target `1/16` is exactly
`2^(m/(16*64))>=2^(7n/1024)`. Both stated absolute and relative tolerances
require at least that target.

## Arbitrary coordinate sets

The appended product-domain extension is correct. If a coordinate set
contains both endpoints, every locally valid univariate polynomial has
nonnegative endpoint values. Its Boolean reduction is a nonnegative
combination of the two endpoint indicators. Expanding products gives
nonnegative coefficients times assignment indicators. Each involved
coordinate consumes at least one degree in the original nonconstant
factors, so the same degree-`4r` square argument applies. Deterministic
restricted coordinates satisfy every local inequality by witness
membership. Locally vanishing polynomial equalities, if included,
vanish under these substitutions as well.

The actual first/second-moment distribution is supported on Boolean
endpoints that belong to the coordinate sets, even when those sets are
disconnected or nonclosed. Thus it lies in the exact convex moment hull,
not merely its closure. For nonclosed sets, however, equivalence between
exact hull membership and all valid quadratic inequalities need not
hold: the inequalities describe the closed hull. The candidate states
that equivalence for compact boxes and does not need it for the extension.

## Scaling and essential oracle limits

The final derivative bounds are correct. Each clause incident to a
coordinate contributes at most `1/(2m)` to its gradient magnitude and
at most two mixed Hessian entries of magnitude `1/(2m)`. Therefore

```
||gradient F||_infinity <= Delta/(2m),
max_i sum_j |Hessian(F)_ij| <= Delta/m.
```

Symmetry of the Hessian bounds its spectral norm by the maximum absolute
row sum, giving `||Hessian(F)||_2<=64/(7n)` on the retained family.

Exact quadratic cuts are imposed as linear conditions on degree-two
moments. Their arbitrary products and SOS localizers are not granted;
the proof does not establish those stronger constraints. Arbitrary
valid cubic cuts could include the sought objective lower bound itself.
Coupled-coordinate branching and auxiliary reformulations also remain
outside the present model.

Finally, the counting theorem is about certified domains covering the
whole cube. A complete coordinate-split tree with no free feasible-region
deletions produces such a leaf cover. Objective propagation requires
including and charging discarded certified domains; a lower bound on
the count of final leaves alone would not follow after unrestricted
uncharged deletions. The author added this necessary qualification.

## Subsequent fixed-order upper certificate

The subsequently added `ceil(3/epsilon)^n` upper certificate also passes.
Each grid width is at most `2epsilon/3`; summing the three clause
derivative bounds of `1/2` gives clause variation at most `epsilon`.
The average of the separate clause minima is therefore at least
`OPT-epsilon`. Multiaffine Bernstein interpolation writes each clause
minus its minimum as a nonnegative sum of products of three normalized
box slacks, which the order-two preordering certifies. At tolerance
`1/16`, this gives `48^n` regions and also certifies relative gap `1/2`
because `OPT>=1/8`. The lifted transfer of this upper certificate is
audited in `notes/review-spatial-bb-bounded-monomial-lift.md`.
