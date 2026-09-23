# Independent audit of the correlation face in the rank-one flow hull

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed result: [A correlation-polytope face in the unit-capacity rank-one
hull](../results/rank-one-correlation-face-conic-lower-bounds.md), including
its complete proof, all three corollaries, and the nonpolyhedral caveat.

Verdict: the correlation-polytope construction is correct. It gives unconditional
lower bounds on exact conic lifts. The relevant SOCP size measure is total cone
dimension, not the number of cones of unrestricted dimension. A subsequent
strengthening, audited below, proves that the face is exposed.

## Construction and proof checked independently

Write

```
U_n = {W >= 0 : rank(W) <= 1, W1 <= 1, W^T1 <= 1},
K_n = conv(U_n).
```

All lower bounds are zero. The set `U_n` is compact: it is closed and each entry
lies in `[0,1]`. Therefore `K_n` is compact, and every point in it has a finite
convex decomposition into points of `U_n`. No closure or limiting-measure
assumption is needed.

For a nonzero atom, set `r=W1`, `c=W^T1`, and `S=1^TW1`. Rank one gives
`W=rc^T/S`, with `r,c in [0,1]^n` and `sum r=sum c=S>0`. Hence

```
trace(W) = sum_i r_i c_i / S <= sum_i r_i / S = 1.
```

Equality is especially restrictive. If `A={i:r_i>0}`, equality implies
`c_i=1` for every `i in A`. Consequently

```
S = sum_i c_i >= |A| >= sum_i r_i = S.
```

Both inequalities are equalities. Thus `r=c=1_A` and
`W=1_A1_A^T/|A|`. Conversely every such matrix for nonempty `A` attains trace
one. The zero matrix has trace zero. An average attaining trace one therefore
uses only these finitely many trace-one atoms. In particular

```
F_0 := K_n intersect {trace(W)=1}
     = conv{1_A1_A^T/|A| : empty != A subset [n]}.
```

Now let `n=2m`, where `m>=1`, and set

```
h(W) = sum_{i=1}^m W_{i,m+i},
F = K_{2m} intersect {trace(W)=1, h(W)=0, sum_{i,j} W_ij=m}.
```

All terms of `h` are nonnegative. A trace-one atom has `h=0` exactly when
its set `A` contains at most one member of each pair `{i,m+i}`. On those atoms,
`sum W=|A|<=m`. A convex combination with total sum `m` must therefore use
only sets with exactly one member of each pair. This proves

```
F = conv{a(x)a(x)^T/m : x in {0,1}^m},  a(x)=(x,1-x).
```

There is no invalid interchange of convexification and an arbitrary affine
section here: each equality is justified by an extremal linear value on the
previously restricted convex set. Specifically, `F_0` is an exposed face of
`K_{2m}`; setting `h=0` defines a face of `F_0`; setting total sum to `m`
defines a face of that face. Transitivity of faces implies that `F` is a face
of `K_{2m}`. Transitivity of *exposed* faces need not hold, so the stronger
word is not established by this argument.

The linear map `W -> X=m W_[m],[m]` maps `F` onto
`COR(m)=conv{xx^T:x in {0,1}^m}`. It is injective on `F`: writing `d=diag(X)`
and `e=1 in R^m`, its affine inverse is

```
W = (1/m) [ X          d e^T - X
            e d^T - X  ee^T - d e^T - e d^T + X ].
```

The identity holds on every vertex and therefore on every convex combination.
In particular, the claim is an affine isomorphism, not merely a projection.

## Lift transfer and precise bounds

Suppose `K_{2m}=pi(C intersect L)`, where `C` is the chosen product of cones,
`L` is affine, and `pi` is linear. Impose the three displayed equations on
`pi(Y)` inside `L`; this adds affine equations and changes no cone. Compose
the output map with `W -> m W_[m],[m]`. The resulting formulation is an exact
`C`-lift of `COR(m)`. Neither constructibility, rational coefficients,
optimization-oracle assumptions, nor strict feasibility is needed for this
direct set-theoretic transfer. In fact an arbitrary affine section would
suffice; the face property is additional information.

For a fixed positive integer `d`, any lift over `(S_+^d)^r` therefore requires
`r=2^{Omega_d(m)}`. For `d=2` the explicit bound is
`r >= (9/7)^(m/2)/sqrt(7)`. These are the cone-block counts in Theorem 1 of
[Fawzi and Parrilo, *Exponential lower bounds on fixed-size psd rank and
semidefinite extension complexity*](https://arxiv.org/pdf/1311.2571), page 3.
Blocks of order at most `d` may be padded with zero rows and columns.

For an SOCP lift over Lorentz cones of dimensions `q_j`, counting scalar
nonnegative factors as dimension one, each factor has an exact representation
using at most `max(1,q_j-2)` copies of `S_+^2`. For dimensions one and two,
this follows by diagonal slices of a single PSD block; for dimension at least
three, use the chain of three-dimensional Lorentz cones. Thus total cone
dimension `D=sum_j q_j` satisfies

```
D >= (9/7)^(m/2)/sqrt(7).
```

The dimension reduction is also stated on page 3 of the same Fawzi–Parrilo
paper. It does not prove an exponential number of arbitrary-dimensional
Lorentz factors. It does prove an exponential number when the factors have
uniformly bounded dimension.

For an unrestricted PSD lift `C=S_+^r`, the order of the PSD matrix satisfies
`r >= 2^{Omega(m^{2/13})}`. This follows from Theorem 1.1 of
[Lee, Raghavendra and Steurer, *Lower bounds on the size of semidefinite
programming relaxations*](https://www.dsteurer.org/paper/sdpsize.pdf).
Here `r` means matrix order, not the number of scalar entries or affine
constraints. For a product of PSD cones of orders `r_j`, the corresponding
bound applies to `sum_j r_j` by placing the blocks on a single diagonal.

These are lower bounds for exact lifts. A transfer to approximate hulls
needs a separate quantitative argument; this audit establishes no such
transfer. They are unconditional existence bounds, so they strengthen a
conditional obstruction to efficiently constructible formulations.

The linear-programming consequence is less informative for the whole hull:
`K_n` is already nonpolyhedral for `n>=2`, so it has no finite polyhedral
lift. The substantive finite-lift conclusions concern SOCP and SDP.

## Checks and limits of this review

An exact-arithmetic enumeration of all subsets of `[2m]` for `m=1,...,6`
found respectively `2,4,8,16,32,64` surviving atoms, and verified every entry
of the affine inverse using Python `fractions.Fraction`. This checks the
indexing and scaling; the proof above establishes the unrestricted result.

The primary lower-bound papers were read directly on 2026-09-04. This audit
checks their applicability and the mathematical construction. It does not
establish novelty of the construction or exclude an equivalent result in
another area of the literature. The distinction must remain explicit in
publication claims.

The complete result file was subsequently read line by line. No mathematical
correction was needed. Its separate nonpolyhedral argument also checks out:
the simultaneous first-row and first-column saturation forces `r=c=(1,t)`
in dimension two, and the displayed graph has second derivative `2/q^3>0`.
The result correctly counts scalar inequality factors and does not overstate
the SOCP cone-count consequence. Its provisional novelty language is
appropriate to the evidence recorded.

## Subsequent explicit-exposure strengthening

The author subsequently supplied an explicit exposing functional. This also
passes independent audit. Write `T=sum W`, `D=1-trace(W)`, and
`B=sum_i W_(i,m+i)`. For a nonzero generating matrix with total `S`,

```
S <= m + sum_i r_i r_(m+i)
  <= m + S B + ||r-c||_1
  <= m + S B + 2 S D
  <= m + 2m B + 4m D.
```

The first inequality sums `a+b<=1+ab` for each complementary pair.
The second replaces the second factor by `c_(m+i)`, paying at most the
sum of absolute discrepancies on those coordinates. The third follows from
`|a-b|<=a(1-b)+b(1-a)` for `a,b in [0,1]`, summed over all coordinates;
the resulting right side is `2S-2r^Tc=2SD`. The final step uses `S<=2m`
and `B,D>=0`. The zero generating matrix satisfies the final inequality
directly. That final inequality is affine in `W` and hence survives taking
convex combinations.

Consequently the affine functional

```
g(W)=m-T+(2m+1)B+(4m+1)D
```

satisfies `g(W)>=B+D>=0` on `K_(2m)`. Equality holds exactly when
`D=B=0` and `T=m`, so `F_m={W in K_(2m):g(W)=0}` is exposed.
This is a separate proof; it does not rely on the invalid inference that a
face exposed inside an exposed face must be exposed in the original set.
