# Joint sharp dependence on dimension, degree, incidence width, and interiority

Date: 2026-09-04. Status: full proof independently audited; no unresolved mathematical issue identified. This combines the separately reviewed degree, dimension, incidence-width, and marginal-floor results. No separate priority claim is made for this synthesis.

Let C(n,d,k,δ) be the supremum of the positive multilinear termwise-to-hull gap
ratio under all of the following restrictions:

- The domain is a unit cube of dimension at most n.
- Every nonlinear term has degree at most d.
- The original support incidence graph has treewidth at most k.
- Every coordinate of the evaluation point is at least δ.

Only points with positive hull gap are included. Here n,d,k are positive integers,
n,d>=2, and 0<δ<=1/2. Put

```
q = min{n,d,1/δ},
φ(q) = ln q / ln ln q,
r = min{k,φ(q)}.
```

Restrict to q>=exp(e), where φ is increasing. The asymptotic statement below
concerns r tending to infinity within this range. The parameters may vary
jointly in any way subject to that condition; it forces both q and k to tend
to infinity. Then

```
C(n,d,k,δ) ~ min{k, ln q / ln ln q}.                       (1)
```

The leading constant is one. The same statement holds if the evaluation point
must lie in the two-sided strip `[δ,1-δ]` in every coordinate. It also holds if
treewidth is replaced by incidence degeneracy or by the minimum possible maximum
outdegree of an incidence orientation.

## Upper bound

The separately reviewed results give the following bounds:

```
by dimension n:       (1+o(1)) φ(n),
by degree d:          (1+o(1)) φ(d),
by marginal floor δ:  (1+o(1)) φ(1/δ),
by incidence width k: k+o(k).
```

See [dimension and degree](positive-multilinear-gap.md),
[the marginal floor](positive-multilinear-marginal-floor-gap.md), and
[incidence sparsity](positive-multilinear-incidence-sharp-growth.md).

Taking the applicable bound corresponding to the smallest of n,d,1/δ gives
`(1+o(1))φ(q)`. Combining it with the width bound gives the right-hand side of
(1). This conclusion is uniform along every joint parameter sequence with
r→∞: then q→∞ and k→∞, so the relative errors in both selected bounds vanish.
The same argument applies to degeneracy and orientation. Restricting means to
an interior strip can only reduce the supremum.

## One lower family meets all restrictions simultaneously

Set

```
L = floor(min{k,φ(q)}),
b = floor((q/2)^(1/L)),
m = b^L.
```

For sufficiently large q and r these are well-defined integers with L>=2 and
b>=L. Indeed, L<=φ(q) implies

```
b >= (q/2)^(1/φ(q)) - 1 = (1-o(1)) ln q,
L/b <= (1+o(1))/ln ln q -> 0.                             (2)
```

Use the reviewed variable-radix construction with L levels and radix b:

```
p(a,z) = Σ_(j=1)^L Σ_(B in P_j) a_j product_(i in B) z_i,
a_j=b^-j,       z_i=1-b^-L,
```

where P_j partitions the m leaves into b^j nested equal blocks. It has unit
coefficients, at most 2m monomials, and the exact gap ratio

```
L/[1+(L-1)/b].                                           (3)
```

All the imposed restrictions hold:

- Its dimension is m+L<=q/2+φ(q)<=q<=n for all sufficiently large q.
- Its maximum degree is m/b+1<=m+1<=q<=d.
- Its incidence treewidth is exactly L<=k. Its degeneracy and minimum maximum
  orientation outdegree are no larger than its treewidth.
- Its smallest anchor mean is 1/m>=2/q>=δ. Its largest anchor mean is at most
  1/2. Every leaf has failure mean 1/m>=δ and success mean at least 1/2.
  Thus all means lie in `[δ,1-δ]`.

The exact gap and treewidth are proved in
[the incidence-growth theorem](positive-multilinear-incidence-sharp-growth.md).
By (2), the denominator in (3) tends to one. Also L/r→1 because r→∞.
Consequently (3) is `(1-o(1))r`, proving the matching lower bound and (1).

This proof uses a single simultaneous construction. Taking the minimum of
separate sharp upper bounds alone would not establish joint sharpness.

## Scope

The conclusion is a joint asymptotic as r→∞. It does not determine exact values
when treewidth or another controlling parameter remains fixed. The
[treewidth-two constant](positive-multilinear-treewidth-two-exact.md) is determined
by a separate theorem. The claim with an incidence
restriction concerns unit cubes and zero-lower-bound boxes after scaling; the
general positive-lower-bound expansion need not preserve incidence width.

Dimension and degree are upper limits, so the lower construction may use fewer
variables or a smaller degree than their stated limits. The unit-coefficient
and two-sided-strip restrictions are already met by the same lower family.

The [independent review](../notes/review-multilinear-joint-gap-growth.md)
checks the joint limiting quantifiers, uniform floor estimates, and every
restriction on the same lower construction. The four separate input theorems
retain their own proof audits and literature qualifications.
