# Independent review of product-domain and local auxiliary branching

Date: 2026-09-05. Reviewer: independent `spatial_sdp_review` agent.
Reviewed: `notes/spatial-bb-product-domain-investigation.md`.

**Verdict: PASS within the stated node-oracle model.** Arbitrary disconnected
coordinate sets, every valid univariate polynomial inequality, and local
polynomial auxiliary variables are handled correctly. The effective order
`rD` is sufficient. The argument does not assume that coordinate sets are
intervals or silently replace them by their convex hulls. No counterexample
or proof gap was found. Novelty has not been assessed in this review.

## Arbitrary coordinate sets

Fix a product domain containing one of the original witnesses. A coordinate
in `R` is evaluated deterministically at its witness value, which belongs
to its coordinate set. Every locally valid inequality is therefore
nonnegative there, and every locally valid equality is zero.

For a coordinate in `U`, both `0` and `1` belong to its set. In the Boolean
quotient, any univariate polynomial satisfies exactly

```
g(u_i) = g(0)(1-u_i)+g(1)u_i.
```

Local validity supplies `g(0),g(1)>=0`. This identity is algebraic; no
statement is made that the first moment itself lies in the possibly
disconnected set. The defined node oracle imposes polynomial moment
conditions, which is why evaluation of these conditions is the right
feasibility test.

After grouping all factors assigned to one coordinate, a product of local
inequalities reduces to

```
sum_{sigma in {0,1}^J} c_sigma
    prod_{i in J:sigma_i=1} u_i
    prod_{i in J:sigma_i=0} (1-u_i),
```

where every `c_sigma>=0`. Here `J` consists only of coordinates whose
factors have nonconstant Boolean reductions. Each such coordinate consumes
at least one degree in the original product, so

```
|J| <= sum_j deg(g_j).
```

Restricted-coordinate substitutions cannot increase the multiplier's
degree. Therefore each indicator times the resulting square satisfies
the degree budget in Lemma B of the reviewed higher-order theorem. The
nonnegative combination is consequently nonnegative under the proposed
functional. Constant factors and factors with identically zero Boolean
reduction cause no difficulty.

A locally vanishing equality has zero values at both Boolean endpoints
on `U`, and zero value at the deterministic witness coordinate on `R`.
Its substitution is thus zero in the Boolean quotient. Every product
with an allowed multiplier also evaluates to zero, including multipliers
coupling several coordinates.

The construction uses only endpoint membership and witness membership.
It needs no closedness, connectedness, semialgebraicity, finite component
count, or finite description of the coordinate sets. For nonclosed sets,
the polynomial oracle may also be unable to distinguish some closure
points; this only makes it weaker and does not affect the exhibited
functional or the lower bound.

## Equality, objective, and counting

The same restricted-coordinate count leaves enough unit and zero witness
coordinates to apply the reviewed fractional-cardinality moment lemmas.
The global equality and objective computations are unchanged. In
particular the functional's value is
`|M intersect R|p(1-p)`, so `|R|<q_r` precludes pruning.

Every witness contained in the product domain still satisfies
`Z intersect A=empty` and `H intersect D=empty`, because these are exact
endpoint-membership exclusions. Uniform-subset avoidance therefore gives
the same upper bound on the fraction of witnesses in one pruned domain.
The union bound applies to any cover, regardless of overlap or
disconnectedness. The perturbation estimate continues to hold because the
constructed first moments lie in `[0,1]`.

Branching on any single-coordinate function changes only one coordinate
set. Consequently the consequence for univariate term branching is valid
even for a nonpolynomial branching function, provided the node bound is
the stated original-variable polynomial oracle. Introducing polynomial
auxiliary variables changes the polynomial degree accounting and is
correctly treated separately.

## Polynomial auxiliary variables

Take `D` to be a positive integer degree bound, including the original
coordinate's degree one. Let `Phi` substitute every local auxiliary by
its defining polynomial in its single original coordinate. It is an
algebra homomorphism satisfying

```
deg(Phi(h)) <= D deg(h).
```

Thus an original-variable functional of degree `2rD` defines a lifted
functional on all polynomials of lifted degree at most `2r`.

For a lifted preordering expression `(prod_j g_j)p^2` with total degree
at most `2r`, its pullback is

```
(prod_j Phi(g_j)) Phi(p)^2,
sum_j deg(Phi(g_j))+2deg(Phi(p)) <= 2rD.
```

Each pulled-back generator is univariate because every generator involves
only a single coordinate's local block. It is nonnegative on the
corresponding projected set by its stated validity on the restricted
graph. It is therefore a generator permitted by the product-domain
oracle. All such inequalities, including the empty product and all
SOS multipliers, are satisfied. Locally valid equalities vanish after
the same Boolean/deterministic evaluation. Graph identities vanish
identically under substitution, whether or not the lifted order is
large enough to impose every such identity explicitly.

For the global equality `e=sum_i x_i-K`, a lifted multiplier of degree
at most `2r-1` pulls back to degree at most `D(2r-1)`. Since `Phi(e)=e`
still has degree one,

```
deg(e Phi(p)) <= 1+D(2r-1) <= 2rD.
```

The available original equality identities therefore suffice. This
checks the part of the argument where applying a blanket degree factor
without counting the equality separately could otherwise cause a gap.

The objective must be the intended original polynomial after exact
substitution, as stated in the candidate. Its evaluated value then agrees
with the earlier construction. Replacing order `r` by `rD` in the
reviewed bound gives the threshold

```
min(k-2rD+2,z-2rD+2,m(1/2-2epsilon)).
```

For quadratic auxiliary terms `D=2`, this is exactly
`min(k-4r+2,z-4r+2,m(1/2-2epsilon))`. Fixed lifted order gives an
exponential cover bound on the balanced family. No claim that hierarchy
order is invariant under nonlinear substitution is required.

## Scope that must remain explicit

The oracle is not an exact solver for coupled feasibility. Every valid
local inequality is allowed, but a globally valid coupled nonlinear
inequality is not automatically allowed. For example, after adding
`y_i=x_i(1-x_i)`, the affine lifted inequality `sum_i y_i>=1/4`
would solve the lower-bound problem at the root. It is outside the
listed local generators and cannot be introduced merely because its
lifted degree is one. The candidate correctly preserves this distinction.

Likewise, branching on a function jointly involving two original
coordinates generally destroys the product-domain description. Coupled
auxiliary graph definitions are outside the substitution argument because
their pulled-back local inequalities need not be univariate. Exact
feasibility pruning beyond the stated moment oracle is also outside the
certificate model.

Feasibility-based local reductions preserve the witness cover. For an
objective-based local reduction `S_i` to `T_i subset S_i`, the removed
part is itself the product with coordinate set `S_i minus T_i`; unlike
closed boxes, the present domain class can represent this set exactly.
It must still be certified and charged as a discarded domain. Final
leaves alone need not cover the original feasible set after such
reductions. These limitations are already stated appropriately in the
candidate.
