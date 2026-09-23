# Independent review: variable-radix incidence lower bound

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed construction: variable-radix family proposed by `new_directions`.

## Verdict on the derivation

The construction and exact hull-gap formula are correct. With `ell≥2` levels
and integer radix `b≥ell`, it has term-by-term gap `ell` and exact hull gap

```
H=1+(ell−1)/b.
```

Its ratio therefore tends to `ell` as `b→∞`. The stated incidence orientation
has variable outdegree at most `ell` and factor outdegree one. Together with
the independently reviewed upper bound, this proves that the worst ratio for
maximum incidence outdegree at most `k` is asymptotic to `k` as `k→∞`.
The construction also proves exact sharpness of the ownership factor for the
restricted class with one low anchor per term and bounded high-variable frequency.
This is a mathematical audit, not a literature novelty determination.

## Construction and local gaps

Put `m=b^ell`. Index the leaves by strings of `ell` base-`b` digits. At level
`j=1,...,ell`, partition them by their first `j` digits into `b^j` blocks of size
`m/b^j`. Introduce a separate anchor `a_j` and include, with coefficient one,
the product of `a_j` and the leaves in each level-`j` block.

Evaluate at `a_j=b^(−j)` and leaf marginal `1−1/m`. Each term has concave-envelope
value `b^(−j)` and convex-envelope value

```
max(0,b^(−j)−(m/b^j)/m)=0.
```

Thus each level contributes one and the term-by-term gap is `ell`. A common
nested-threshold law attains every concave term envelope, so the full concave
envelope is also `ell`.

For a binary outcome, let `R` be the number of failed leaves and let `h_j` count
the level-`j` blocks hit by failures. Every feasible law has `ER=1` and
`EA_j=b^(−j)`. Exactly as in the dyadic proof,

```
H=max E Σ_j A_j h_j,
0≤h_j≤min(b^j,R).
```

The mean constraints and the relaxed count objective are sufficient here because
of the following simultaneous geometric realization.

## Digit reversal and uniform shifts

For an integer `R∈[0,m]`, take as failed leaves the digit reversals of
`0,1,...,R−1`, written with exactly `ell` base-`b` digits. At level `j`, their
first `j` digits are reversals of the original indices' last `j` digits. The
latter run through exactly `min(b^j,R)` residue classes. Therefore this set hits
exactly `min(b^j,R)` blocks at every level simultaneously.

Randomize the failed set by adding a uniform random digit string coordinatewise
modulo `b`, without carries. This translation permutes all level-`j` blocks,
preserves every hit count, and gives each fixed leaf failure probability `R/m`.
The argument works for every integer radix, not merely primes. After averaging
over `R`, every leaf has failure probability `1/m`.

Thus every joint law of the count and anchors can be realized by actual leaves
without loss in the relaxed objective. The sparse hull gap equals the relaxed
count maximum, rather than merely being bounded above by it.

## Quantile levels and an exact dual inequality

Rearrange each anchor to select the largest values of `R`, simultaneously using
one upper-tail quantile. The probability of a level with exactly the first `l`
anchors selected is

```
w_l=(b−1)b^(−l−1) for 0≤l<ell,
w_ell=b^(−ell).
```

The level utility is `S_l(r)=Σ_(j=1)^l min(b^j,r)`. For any integer `1≤s≤ell`,

```
S_l(r)≤s r+F_l(s),
F_l(s)=0                                      if l≤s,
F_l(s)=Σ_(j=1)^(l−s)b^j
      =[b^(l−s+1)−b]/(b−1)                  if l>s.
```

For `l≤s`, bound every term by `r`. For `l>s`, cap the first `l−s` terms and
bound the remaining `s` terms by `r`. The weighted geometric sum is exactly

```
Σ_l w_l F_l(s)=(ell−s)b^(−s).
```

Using `ER=1` gives the upper certificate

```
H≤s+(ell−s)/b^s.
```

In particular `s=1` gives `H≤1+(ell−1)/b` directly.

## Exact attainment by two count profiles

For `q=1,...,ell`, define an integer count on each quantile level by

```
R_l^(q)=0                         if l<q,
R_l^(q)=b^(l−q+1)                 if l≥q.
```

Its mean count is

```
B_q=Σ_l w_l R_l^(q)
   =[(ell−q)(b−1)+b]/b^q.
```

When `1≤s≤ell−1` and `B_(s+1)≤1≤B_s`, mix profiles `q=s` and `q=s+1` with respective probabilities

```
eta=(1−B_(s+1))/(B_s−B_(s+1)),   1−eta.
```

The denominator is positive and the weights lie in `[0,1]`. The mixture has
mean count one. Both profiles have the same anchor marginals, since in each
profile `A_j=1` precisely on levels `l≥j`, whose total probability is `b^(−j)`.

Both profiles attain the scalar upper certificate at every level. For `l<s`
the count is zero; at `l=s`, the two counts are zero and `b`, and
`S_s(r)=sr` throughout `[0,b]`. For `l>s`, their counts are the two endpoints
`b^(l−s)` and `b^(l−s+1)`, exactly the interval where the capped first `l−s`
terms and linear last `s` terms make the upper certificate an equality.
The digit-reversal translation construction then makes this an actual binary
law with the required leaf and anchor means. Hence

```
H=s+(ell−s)/b^s
```

under the stated budget condition.

For `b≥ell≥2`, `B_1=ell−(ell−1)/b≥1` and
`B_2=[(ell−1)b−ell+2]/b²≤1`. Thus `s=1` applies and establishes the claimed
exact gap and ratio. No numerical optimization enters this proof.

## Orientation consequence and sharp ownership factor

Orient each leaf incidence toward its factor and each factor's anchor incidence
toward the anchor. Every leaf has outdegree `ell`, every anchor has outdegree
zero, and every factor has outdegree one. For maximum outdegree allowance
`k=ell`, the ratios approach `k` as the radix tends to infinity. The earlier
upper bound with `r=s=k` and the sharp degree substitute gives

```
R_orientation(k)≤k+O(log k/log log k).
```

Consequently `R_orientation(k)/k→1`.

All factors of the construction have exactly one low coordinate at the specified
point: anchors are at most `1/2` and, for `ell≥2`, leaves are strictly above
`1/2`. Each high leaf belongs to exactly `ell` factors. In the restricted class
with exactly one low anchor per term and high-variable frequency at most `r`,
the ownership construction alone gives ratio at most `r`; there is no outgoing
high gap and no easy-factor contribution. The present family with `ell=r`
approaches `r`. Thus that class has exact supremum `r` for `r≥2`. For `r=1`,
disjoint ownership gives exactness and the supremum is one.

## A further fixed-parameter lower bound

The same family admits a slightly better orientation when `ell≥3`. Orient each
deepest bilinear factor toward both its leaf and its anchor, giving it outdegree
two. Orient all other factor-to-anchor edges toward the anchor, and orient all
remaining leaf incidences toward their factors. Each leaf then has outdegree
`ell−1`, and the maximum outdegree is `ell−1`.

The graph also has degeneracy at most `ell−1`: delete the deepest bilinear factors,
which have degree two; then delete leaves, each of degree `ell−1`; the remainder
is a disjoint union of factor-anchor stars. Therefore, for each integer `k≥2`,
taking `ell=k+1` and letting `b→∞` gives

```
R_orientation(k)≥k+1,
R_degeneracy(k)≥k+1.
```

These are supremum lower bounds, not claims that the finite-radix ratio equals
`k+1`. They are compatible with the leading asymptotic constant one.
They should not automatically be transferred to treewidth: the construction's
treewidth is not shown to be `ell−1` by either an orientation or degeneracy order.

## Final written theorem and exact treewidth independently checked

I read the completed `results/positive-multilinear-incidence-sharp-growth.md`.
The exact gap proof, fixed-parameter supremum statements, orientation and
degeneracy constructions, upper comparison, and sharp high-variable-frequency
statement are correct. No unresolved mathematical issue was found.

The additional exact treewidth statement also checks independently. Eliminating
all leaves first fills only chains of nested factor nodes into cliques: two
factor nodes share a leaf precisely when their corresponding blocks are nested.
Each leaf has exactly `ell` such factor neighbors. Now eliminate factors in
descending order of level. When a level-`j` factor is removed, its remaining
neighbors are contained in its `j−1` strict ancestor factors and the anchors
from levels `j,...,ell`, at most `ell` vertices total. Eliminating a factor fills
edges among these ancestors and deeper anchors; it never connects unrelated
factor nodes. This invariant is preserved throughout the descending elimination.
Finally only the `ell` anchors remain. The resulting elimination width is at
most `ell`.

For the matching lower bound, fix a level-`ell−1` block. Its `b` leaves are
adjacent to all `ell−1` ancestral factor nodes. Contract each leaf's deepest
bilinear factor into that leaf; the resulting leaf is also adjacent to anchor
`a_ell`. These vertices contain a `K_(ell,b)` minor. When `b≥ell`, pair `ell−1`
distinct left vertices with distinct right vertices to form connected branch
sets, and take an unused vertex from each side as two further singleton branch
sets. Every pair of the resulting `ell+1` branch sets is adjacent, giving a
clique minor of size `ell+1`. Hence treewidth is at least `ell`.

Thus the construction has incidence treewidth exactly `ell`, not merely a
bounded-orientation certificate. Taking `ell=k`, `b→∞` proves `W(k)≥k` for the
supremum under treewidth at most `k`. Together with

```
W(k)≤D(k)≤P(k)≤k+min(k,B(k+1))+κ=k+o(k),
```

this establishes all three leading constants:

```
W(k)/k→1,    D(k)/k→1,    P(k)/k→1.
```

The stronger fixed-`k` lower bounds `D(k),P(k)≥k+1` remain consistent with this
conclusion. Their construction has treewidth `k+1`, so the draft correctly does
not assert the same fixed-`k` lower bound for `W(k)`.
