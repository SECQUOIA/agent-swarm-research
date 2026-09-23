# Exact convex envelopes of one monomial are hard on narrow positive boxes

Date: 2026-09-04.

Status: the reduction, NP-completeness proof, graph-hull membership, fixed-ratio-type
corollary, and rank-one MOT / dual-oracle implications passed
[independent review](../notes/review-positive-box-single-monomial-hardness.md).
This is a tractability
boundary for the common-aspect-ratio results, not a claimed new complexity theorem
until a dedicated prior-literature comparison is complete.

## Decision problem and scope

The input consists of rational upper bounds `u_i>1` and a rational threshold `q`.
Let

```
m(x)=∏_{i=1}^n x_i,
B=∏_{i=1}^n[1,u_i],
xbar_i=(1+u_i)/2.
```

The decision problem asks whether `vex_B m(xbar)≤q`.

**Theorem.** This decision problem is NP-complete even when `1<u_i≤2` for every
coordinate. More strongly, for any fixed rational `η>0`, it remains NP-complete
under the restriction `1<u_i≤1+η`. Hence exact evaluation is NP-hard for one
unit-coefficient monomial, at the midpoint of a box with strictly positive lower
bounds, even when all box aspect ratios are arbitrarily close to one.

This result concerns a family of input boxes **contained in** `[1,2]^n`, or in
`[1,1+η]^n`; it does not concern the single common-aspect-ratio box `[1,2]^n` itself.
The reduction is from the weakly NP-complete PARTITION problem and establishes
ordinary NP-hardness. It
does not establish strong NP-hardness, hardness at fixed additive accuracy, or a
constant-factor approximation barrier. There is only one nonlinear factor, so its
variable frequency is one and its termwise relaxation is tautologically exact.
The difficulty is computing that single factor's exact envelope.

## Reduction from PARTITION

Start with positive integers `a_1,…,a_n` and write `A=Σ_i a_i`. We may assume `A`
is even: doubling all integers makes the total even and preserves whether there
is a subset summing to one half of the total. Choose an integer `K≥1` and set

```
ε=1/(16 K A³),
u_i=1+εa_i.
```

In particular,

```
1<u_i≤1+εA=1+1/(16 K A²)<2.
```

The normalized box variables are `x_i=1+εa_i z_i`. The prescribed physical
midpoint corresponds to `E Z_i=1/2` for every binary variable `Z_i`. Multiaffinity
implies that the envelope value is the minimum expected vertex product over all
such binary distributions.

For a binary vector `z`, put `S(z)=Σ_i a_i z_i`. Expanding the product gives

```
∏_i(1+εa_i z_i)
 =1+εS(z)+(ε²/2)[S(z)²−Σ_i a_i² z_i]+R(z).             (1)
```

All terms in `R` have degree at least three and nonnegative coefficients. The
elementary symmetric sum of degree `k` in the nonnegative numbers `a_i z_i` is
at most `A^k`. Since `εA≤1/16`,

```
0≤R(z)≤Σ_{k≥3}(εA)^k
       =(εA)³/(1−εA)
       ≤2ε³A³=ε²/(8K)≤ε²/8.                         (2)
```

For every admissible distribution, `E S=A/2`. Therefore (1) yields the exact
expectation identity

```
E m(X)=b+(ε²/2) Var(S)+E R(Z),
b=1+εA/2+ε²[A²/8−(1/4)Σ_i a_i²].                    (3)
```

If a partition exists, choose a corresponding binary vector `z*` with
`S(z*)=A/2`. The equal mixture of `z*` and its complement has all coordinate means
`1/2`, and `S=A/2` deterministically. Equations (2)–(3) imply

```
YES:  vex_B m(xbar)≤b+ε²/8.                           (4)
```

If no partition exists, every binary state has integer `S` distinct from the
integer `A/2`, so `(S−A/2)²≥1`. Every admissible distribution then has
`Var(S)≥1`. The nonnegative remainder in (3) implies

```
NO:   vex_B m(xbar)≥b+ε²/2.                           (5)
```

Equivalently, the NO case has the explicit affine lower certificate in normalized
coordinates

```
L(z)=1−ε²A²/8+ε²/2
     +Σ_i [εa_i+(ε²/2)(Aa_i−a_i²)]z_i.
```

At every binary vertex,
`m(1+εa⊙z)−L(z)=(ε²/2)[(S(z)−A/2)²−1]+R(z)≥0`, and
`L(1/2,…,1/2)=b+ε²/2`. Multiaffine interpolation extends this affine lower bound
throughout the box. This is the dual form of the variance argument.

Thus the rational threshold

```
q=b+ε²/4
```

distinguishes the two cases. The upper bounds, midpoint, and threshold have encoding
length polynomial in the binary input length: `log A` is polynomial in that input
length, and the formulas use a fixed number of powers and rational operations.
Taking `K=1` proves the restriction to boxes contained in `[1,2]^n`. For a fixed
rational `η>0`, choose a fixed integer `K` with `1/(16K)≤η`; the same reduction
then has `u_i≤1+η` throughout. This proves NP-hardness. ∎

## Membership in NP

At the normalized midpoint, the envelope distribution LP has equality rows
`1,z_1,…,z_n` and right-hand side `(1,1/2,…,1/2)`. It has an optimal basic feasible
solution with at most `n+1` positive weights. A certificate lists those binary
states and their rational probabilities. The states have polynomial total size;
the probabilities solve a nonsingular subsystem with 0/1 coefficients and
half-integer right-hand sides, so their numerators and denominators have
polynomial bit length by determinant bounds. Each vertex product also has
polynomial bit length because it is a product of at most `n` input rationals.

The verifier checks nonnegative probabilities, their total, every coordinate mean,
and the expected product bound using exact rational arithmetic. Therefore a YES
instance has a polynomially verifiable certificate, establishing NP membership
and hence the theorem's NP-completeness statement.

## Scalar graph-hull membership

The same reduction proves NP-completeness of deciding whether `(xbar,q)` belongs
to the convex hull of this single monomial's graph. At the midpoint, the common
comonotone upper law gives

```
C=cav_B m(xbar)=(1+∏_i u_i)/2.
```

Retaining its degree-two expansion yields
`C≥1+εA/2+(ε²/4)(A²−Σ_i a_i²)`, and hence

```
C−b≥ε²A²/8≥ε²/2>q−b,
```

because the doubled PARTITION input has `A≥2`. Therefore `q<C` in every reduced
instance, and graph-hull membership is equivalent to the lower-envelope threshold
test already proved hard. Membership is in NP: an exact convex combination of at
most `n+2` binary graph vertices suffices, with polynomial-bit rational probabilities
from a basic solution of the coordinate, value, and normalization equations.
This corollary has the same narrow-box and precision qualifications as the theorem.

## A fixed number of aspect-ratio types remains tractable

For one monomial on any rational strictly positive box `[l,u]`, suppose there are
at most `k` distinct ratios `r_j=u_i/l_i`. When `k` is fixed, exact envelope
evaluation is polynomial-time. This is an elementary enumeration consequence,
not a claimed new algorithm.

After `x_i=l_i[1+(r_j−1)z_i]` within ratio group `j`, the value at a binary vertex
depends only on the success counts `h_j` in these groups:

```
m(x)=(∏_i l_i) ∏_{j=1}^k r_j^{h_j}.
```

To separate the envelope distribution LP's dual, minimize this expression minus
`Σ_iπ_i z_i`. For fixed counts `(h_1,…,h_k)`, the product is fixed; the minimizing
choice selects the `h_j` largest dual coefficients in each group. Sort each group
once and use prefix sums, then enumerate the `∏_j(n_j+1)≤(n+1)^k` count tuples.
This gives an exact rational vertex oracle in `n^{O(k)}` time. The bounded-dual
argument in the [convex-cardinality theorem](convex-cardinality-frequency-two-gap.md)
then supplies polynomial-time envelope evaluation for fixed `k`. Fixed coordinates
are substituted first. The upper envelope remains directly computable by a common
threshold coupling.

Thus the hardness construction requires the allowed number of aspect-ratio types
to grow; closeness of the ratios to one by itself does not control exact complexity.

## What this does and does not separate

The [convex-cardinality frequency-two result](convex-cardinality-frequency-two-gap.md)
gives polynomial-time envelope evaluation when the positive monomial boxes have a
common aspect ratio within each connected component. Here the aspect ratios are
`1+εa_i`, with arbitrarily small variation but without exact equality. Exact
equality of the aspect ratios therefore marks a real computational restriction,
even before there is any interaction between different nonlinear factors.

The numerical separation in (4)–(5) is of order `ε²=1/(256K²A^6)`. This can be
exponentially small in the binary encoding length of PARTITION. Consequently the
proof does not rule out algorithms that approximate the envelope to fixed additive
accuracy, or algorithms whose running time depends polynomially on the numerical
value of `A`. It also makes no claim about gap-ratio approximation when local
envelopes are supplied by an oracle.

## Rank-one multimarginal optimal transport and an explicit published question

The same construction has a direct interpretation as multimarginal optimal
transport (MOT). Use `n` binary marginals, each uniform on its two states, and the
cost tensor

```
C = ⊗_{i=1}^n (1,1+εa_i),
C_z=∏_i(1+εa_i z_i).
```

This is a strictly positive rank-one tensor supplied in factored form; there is
no sparse correction. Its MOT value is exactly the midpoint envelope above.
Moreover, all tensor entries lie in `[1,16/15]`, since

```
Cmax=∏_i(1+εa_i)≤Σ_{k≥0}(εA)^k≤16/15.
```

Consequently exact MOT threshold evaluation is NP-complete already in this
restricted class. Unless `P=NP`, there is also no deterministic algorithm that
approximates its value to additive error `δ` in time polynomial in the rational
input length and `log(Cmax/δ)`. To see this, take `δ=ε²/32`: the approximation
intervals around (4) and (5) remain disjoint, and `log(1/δ)` is polynomial in the
PARTITION input length. The same conclusion for randomized bounded-error
algorithms requires the assumption `NP` is not contained in `BPP`.

The dual vertex oracle is hard even without using a general MOT-to-oracle
reduction. Choose rational dual coefficients

```
π_i=εa_i+(ε²/2)(Aa_i−a_i²),
d0=1−ε²A²/8.
```

Then the exact identity

```
C_z−Σ_iπ_i z_i=d0+(ε²/2)(S(z)−A/2)²+R(z)
```

implies that `MIN_C(π)=min_z(C_z−π·z)` is at most `d0+ε²/8` in a YES instance
and at least `d0+ε²/2` in a NO instance. The coefficients have polynomial bit
length. Thus exact `MIN`, and additive approximation with logarithmic dependence
on inverse accuracy, are NP-hard for this rank-one class as well. This does not
assert hardness of finding the smallest entry of a rank-one tensor without dual
weights: here that unweighted minimum is trivially one.

Altschuler and Boix-Adserà explicitly ask, after Theorem 7.4 in §7.2 of
*Polynomial-time algorithms for multimarginal optimal transport problems with
structure*, whether the constant-rank approximate oracle can have logarithmic
dependence on inverse accuracy, enabling exact `MIN` and MOT. The argument above
gives a negative answer under `P≠NP`, in the rational bit model, already for rank
one. Their Corollary 7.5 gives approximation with polynomial dependence on
`Cmax/δ`, which is compatible with this reduction.
[Published primary paper](https://link.springer.com/article/10.1007/s10107-022-01868-7),
[open PDF, p.55 of the PDF](https://d-nb.info/1271958090/34).

The published question was visually checked on PDF p.55. A focused search for
later resolutions did not locate one on 2026-09-04; that search is incomplete.
The claim here is that the proved reduction answers the question as written,
not that priority over all subsequent work has been established.

**Computation model.** These hardness conclusions use the standard rational bit
model. Section 2 of the cited paper assumes input bit lengths polynomial in its
dimensions. To meet that convention literally, if the original PARTITION input
has bit length `L`, append `O(L)` dummy binary tensor factors `(1,1)`, with uniform
marginals and zero dual potentials. They change neither the rank, cost range,
MOT value, nor oracle value, and make all input bit lengths polynomial in the
resulting number of marginals. The source also discusses arithmetic-operation
counts. This reduction does not prove a lower bound for an unrestricted
unit-cost arithmetic model that permits intermediates of unbounded bit length;
its consequence applies to polynomial-bit implementations.

The source match, padding, precision distinction, and direct oracle reduction
passed a [dedicated independent audit](../notes/review-rank-one-mot-precision.md).

## Literature status

- PARTITION is a classical NP-complete problem. Richard M. Karp, *Reducibility
  among Combinatorial Problems* (1972), states completeness of the listed problems
  on original p.94 and defines PARTITION as problem 20 on original p.97. Both pages
  were visually checked in the authorized reprint. Signed entries in that formulation
  can be replaced by their absolute values and zeros omitted, using the equivalent
  signed-sum formulation of PARTITION.
  [Open authorized reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf),
  [original article DOI](https://doi.org/10.1007/978-1-4684-2001-2_9).
- The envelope formulas on common-aspect-ratio boxes are classical; precise primary
  sources are collected in the linked convex-cardinality result. Those formulas
  do not apply to the unequal bounds in this reduction.
- Initial searches found many statements about general multilinear polynomials and
  general supermodular functions being hard to convexify, but did not yet locate a
  primary statement matching this single-monomial, positive-box, midpoint scope.
  That incomplete search is not evidence of publication novelty.
- In the local primary papers, Rikun states hardness for a general multilinear
  function on the unit cube, citing Crama; Sherali makes the same general-function
  statement. Their inspected hardness statements do not establish the single
  positive-monomial scope here. See
  [[rikun1997-a-convex-envelope-formula-for]] p.3 and
  [[sherali1997-convex-envelopes-of-multilinear-functions]] p.22.
- Altschuler and Boix-Adserà's separate *Hardness results for Multimarginal
  Optimal Transport problems*, §4, Propositions 4.1–4.2, rule out running times
  jointly polynomial in tensor rank and other parameters. Their construction
  uses growing rank; it does not supply the fixed-rank conclusion above.
  [Primary preprint](https://arxiv.org/html/2012.05398v1).

The independent verifier
[`code/audit_single_monomial_hardness.py`](../code/audit_single_monomial_hardness.py)
passed 120 exact rational tests, including 28 YES and 92 NO instances. It checked
12,420 binary-state remainder bounds, the explicit YES primal and NO affine-dual
certificates, and the direct tilted-MIN reduction with its `ε²/32` approximation
margin. No floating-point convex-envelope solver was used for these checks.
