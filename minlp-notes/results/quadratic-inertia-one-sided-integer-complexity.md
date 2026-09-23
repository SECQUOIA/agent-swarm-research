# Quadratic epigraph approximation: integer dimension is half the negative inertia

Date: 2026-09-05. Status: independently reviewed; see
`notes/review-quadratic-inertia-one-sided.md`. Publication priority remains unestablished.
The signed-square upper construction is classical. The proposed point
is its optimal integer-dimension coefficient over all convex lifts.

## Main theorem

Let `B=product_i[l_i,u_i]` be a bounded box with nonzero side lengths,
and let

```
f(x)=(1/2)x^T H x+a^T x+b,   H=H^T.
```

Write `k_-=n_-(H)` and `k_+=n_+(H)` for the numbers of strictly negative
and strictly positive eigenvalues. For `ε>0`, an epigraph relaxation must
contain

```
epi_B(f)={(x,w):x in B, w>=f(x)}
```

and satisfy `w>=f(x)-ε` at every admitted point with `x in B`. Similarly,
a hypograph relaxation contains `hyp_B(f)` and satisfies `w<=f(x)+ε`.
There is no bound on the allowed output in the opposite direction.

Let `p_epi,conv(ε)` be the minimum integer dimension of any such epigraph
relaxation represented by an arbitrary finite-dimensional convex lift,
with unrestricted integer ranges and continuous auxiliary variables.
Let `p_epi,bin(ε)` be the minimum binary dimension when all lifted
constraints are linear. Define the corresponding hypograph minima in
the same way. Coefficients may be real.

**Theorem.** If `k_->0`, then

```
p_epi,conv(ε) = (k_-/2) log2(1/ε)+O_(H,B)(1),
p_epi,bin(ε)  = (k_-/2) log2(1/ε)+O_(H,B)(1).
```

If `k_-=0`, both epigraph minima equal zero for every positive accuracy;
the convex-lift minimum is zero even for exact representation. Replacing
`f` by `-f` gives

```
p_hyp,conv(ε) = (k_+/2) log2(1/ε)+O_(H,B)(1),
p_hyp,bin(ε)  = (k_+/2) log2(1/ε)+O_(H,B)(1)
```

when `k_+>0`, and both hypograph minima are zero for every positive
accuracy when `k_+=0`. The binary upper formulations use
`O_(H,B,n)(log(1/ε))` continuous variables and inequalities for fixed
`H,B`; their outputs are unbounded in the required epigraph/hypograph
direction.

Thus the graph, epigraph, and hypograph have leading coefficients
`rank(H)/2`, `k_-/2`, and `k_+/2`, respectively. The graph statement is
proved in `results/quadratic-rank-integer-complexity.md`.

## Lower bound on a negative-curvature slice

Assume `k=k_->0`. Choose an `n by k` matrix `T` with orthonormal columns
spanning the negative eigenspace. Then

```
T^T H T <= -m I_k
```

for some `m>0`. Pick a point `x_0` in the interior of `B`. For a
sufficiently small fixed `rho>0`, the entire parallelepiped
`x_0+T[-rho,rho]^k` lies in `B`: this follows from continuity of the
linear map and the positive distance from `x_0` to the box boundary.
Let `D=[-rho,rho]^k` and `g(t)=f(x_0+Tt)`. The quadratic `g` is
`m`-strongly concave on `D`.

Consider any convex lifted epigraph relaxation with `p` integer
coordinates. Restrict its original variables by `x=x_0+Tt`, `t in D`.
This preserves convexity of the lift and introduces no integers. Its
projection contains `epi_D(g)` and has the same one-sided error bound.

Group exact graph inputs `t` by parity of a feasible integer lift.
Two graph points `s,t` in the same parity class have a feasible midpoint
lift with integer coordinates. Its output is `[g(s)+g(t)]/2`, so

```
ε >= g((s+t)/2)-[g(s)+g(t)]/2 >= m ||s-t||²/8.
```

Take closures of the at most `2^p` classes in `D`; the pairwise bound
persists and the closures cover `D`. Each closed class has diameter at
most `sqrt(8ε/m)`, so the Euclidean isodiametric inequality gives volume
at most `omega_k (2ε/m)^(k/2)`. Therefore

```
volume(D) <= 2^p omega_k (2ε/m)^(k/2),
ε >= (m/2) [volume(D)/omega_k]^(2/k) 2^(-2p/k).
```

Taking logarithms yields the claimed lower coefficient. This argument
works for arbitrary convex lifts and unbounded integer coordinates;
closedness or measurability of the original parity classes is not
needed. The integer-parity mechanism is the published Midpoint Lemma:
[[lubin2022-mixed-integer-convex-representability]] p.11-12.

## Compact epigraph construction

Diagonalization and normalization on the box give

```
f(x)=affine(x)+sum_(j in P) c_j y_j²-sum_(j in N) d_j y_j²,
0<=y_j<=1,   c_j>0, d_j>0,
|P|=k_+, |N|=k_-.
```

The `y_j` are affine functions of `x`. This is the same normalized
signed-square decomposition used in the graph theorem. If `H=0`, the
epigraph is already a polyhedron and the theorem is immediate. Otherwise
put `A=sum_(j in P)c_j+sum_(j in N)d_j>0` and

```
L=max{0,ceil[(1/2)log2(A/(4ε))]}.
```

For each `j in P`, use the zero-binary folding epigraph relaxation
with `L+1` folds for `t_j>=y_j²`. It contains the entire
square epigraph, and every admitted point obeys

```
t_j>=y_j²-2^(-2L-4).
```

For each `j in N`, use the upper half of the depth-`L` binary sawtooth
relaxation for the square:

```
0<=y_j<=1,
g_0=y_j, g_l=G(g_(l-1)) encoded with L binaries,
t_j<=y_j-sum_(l=1,...,L)4^(-l) g_l.
```

Here `G(u)=min{2u,2(1-u)}` and its standard binary graph encoding is
linear. The interpolant upper bound contains the entire hypograph of
the square and gives

```
t_j<=y_j²+2^(-2L-2).
```

In particular, no lower bound on a negative-term `t_j` is required.
Finally impose the single linear inequality

```
w>=affine(x)+sum_(j in P)c_j t_j-sum_(j in N)d_j t_j.
```

For every admitted point with integral binaries the right-hand side is
at least

```
f(x)-sum_(j in P)c_j 2^(-2L-4)
    -sum_(j in N)d_j 2^(-2L-2)
>= f(x)-A 2^(-2L-2)
>= f(x)-ε.
```

Conversely, each point with `w>=f(x)` has a lift: choose all `t_j=y_j²`
and the corresponding sawtooth auxiliary variables. Increasing `w`
preserves feasibility, so the construction includes the complete
unbounded epigraph as required.

The only binaries are the `k_- L` binaries for negative square terms.
This proves the upper coefficient. Positive square terms need no
binaries, however many positive eigenvalues are present. With an
arbitrary convex lift one may alternatively model each positive square
epigraph exactly using the convex inequality `t_j>=y_j²`.

When `k_-=0`, the same LP epigraph construction achieves every positive
accuracy with zero binaries. The exact epigraph of `f` is convex, which
also proves the stated zero-integer exact convex representation.
The hypograph theorem follows by applying the entire argument to `-f`
and reversing the output coordinate.

## Exact convex-lift corollary for one product

For `f(x,y)=xy` on `[0,1]^2`, the smallest epigraph underestimation
error achievable with `p` unrestricted integer coordinates in an
arbitrary convex lift is exactly

```
E_epi,conv(p)=2^(-2p-2).
```

The same statement holds for hypograph overestimation. Consequently,
for every `ε>0`,

```
p_epi,conv(ε)=p_hyp,conv(ε)
            =max{0,ceil[(log2(1/ε)-2)/2]}.
```

Proof of the lower bound. Restrict to `x+y=1`, parametrized by
`x=t,y=1-t`, `0<=t<=1`. The function becomes `t(1-t)`, whose concavity
midpoint gap is `(s-t)²/4`. Closures of at most `2^p` parity classes
cover the interval, and one has diameter at least `2^(-p)`. Pairs in the original parity class approach that diameter, so their
feasible chord-midpoint errors have supremum at least `2^(-2p-2)`.
This proves the lower bound even when the convex lifted set is nonclosed.

For the matching upper bound, introduce

```
u=(x+y)/2,   v=(x-y+1)/2,
xy=u²-v²+v-1/4,
0<=u,v<=1.
```

Use the exact convex constraint `t_plus>=u²`, the depth-`p` binary
sawtooth hypograph `t_minus<=F_p(v)`, and

```
w>=t_plus-t_minus+v-1/4.
```

This contains the full epigraph and reaches below it by at most
`F_p(v)-v²<=2^(-2p-2)`. The error is attained by choosing `u=1/2` and
`v` at a midpoint of a depth-`p` dyadic interval; these values correspond
to the valid original point `(x,y)=(v,1-v)`. For the hypograph, the
transformation `(x,y,w) -> (x,1-y,x-w)` converts it to a product
epigraph and preserves one-sided error and integer dimension.

This exact statement permits the convex square epigraph constraint.
With purely linear lifted constraints, zero-binary positive-square
refinement approaches the same error with arbitrarily small positive
slack. No claim of exact finite-LP attainment at the threshold is made.
The broader linear-lift asymptotic theorem above is unaffected.

The comparison is consequential: approximating a product's whole graph
requires leading integer coefficient one, while its epigraph or
hypograph alone requires coefficient one half. The metric and represented
set must be specified when comparing formulation counts.

## Scope for optimization

The theorem quantifies auxiliary integer dimension needed for a uniform
outer approximation of a quadratic epigraph over a full box. It directly
applies to preserving a quadratic objective through an epigraph variable,
or to a quadratic inequality when the whole epigraph block must be
approximated before additional physical constraints are imposed.
It does not prove that a particular optimization instance requires this
many integers: its feasible set may occupy only a smaller region, and
approximating its optimal value can be easier than approximating the
entire epigraph uniformly.

There is no contradiction with direct convex modeling when `H` is
positive semidefinite, or with algorithms exploiting a fixed number of
negative eigenvalues. The theorem supplies a universal formulation
lower bound in auxiliary integer dimension, not a new running-time
classification or a hardness claim for quadratic optimization.

## Literature and verification status

Signed-square decomposition, subdivision of the negative directions,
and linear underestimators are classical in global quadratic
optimization. A particularly recent primary comparison is Del Pia's
2026 [Rational Jacobi Rotations and the Complexity of Approximating Mixed Integer Quadratic Programming](https://arxiv.org/html/2607.29386v1).
Its Theorem 1 gives an approximation algorithm for fixed original
integer dimension and fixed negative inertia; Section 1 traces earlier
work of Vavasis and Del Pia. Those are algorithmic results in a rational
bit model, while this note concerns auxiliary dimension of a uniform
relaxation and allows real coefficients.

The exact leading coefficient for arbitrary convex lifted epigraph
relaxations was not found in the targeted searches completed for this
note. This remains qualified novelty evidence. The detailed search
record and independent proof audit are linked from
`notes/quadratic-inertia-one-sided-investigation.md`.

## Numerical verification

`code/quadratic_rank/check_one_sided.py` directly solves the zero-binary
square epigraph LP at depths zero through five and checks its error
against `2^(-2L-4)`. It also checks the opposite square hypograph error
`2^(-2L-2)` and the signed error allocation for `3u²-5v²`. All checks
passed on 2026-09-05; they support rather than replace the proof.


## Lean verification: topic 20

See the [coverage map](../formal/topics/20-scalar-quadratic/COVERAGE.md) and
[verification record](../formal/topics/20-scalar-quadratic/VERIFICATION.md)
for the declarations, independent reviews and final targeted checks. These
records supplement the historical checks above and cover scalar quadratic
results; they do not certify the whole paper or vector quadratic topic 26.

The sharp lower constant is also proved. The Lean development establishes the
Euclidean isodiametric inequality `volume(S) <= omega_d (D/2)^d` for arbitrary
compact sets of diameter at most `D`, including nonconvex sets. Its proof
maximizes a radial weighted measure over a compact family of bounded-diameter
sets and uses a strictly improving reflection polarization to exclude mass
outside the half-diameter ball. A sufficiently large finite cutoff transfers
a putative volume excess to a weighted-measure excess. This supplies the
actual unit-ball constant in the displayed `μ/2`
bound. The final theorem constructs the negative slice from the original
Hessian and box; it does not assume a supplied slice or isodiametric estimate.

The formal upper construction starts from the original Hessian and box. It
normalizes each nonzero spectral coordinate with a proved positive enclosing
radius, rather than assuming exact extrema. Negative squares use an actual
finite binary linear hypograph system. Positive squares use the continuous
folding system with `L` folds, whose error is `4^(-L)/4`. Using `L+1` folds
proves the stronger positive-square estimate displayed above, but is unnecessary
for the aggregate error `A 4^(-L)/4`.

The resulting epigraph uses exactly `k_- L` binary coordinates. It has at most
`r(3+2L)` real auxiliary coordinates and `2n+r(11+10L)+2` inequality rows,
where `r=rank(H)`. More precisely, the positive-square components use `L`
auxiliaries and `3L+3` rows each, while negative-square components use `2+2L`
auxiliaries and `11+10L` rows each; every component also contributes one stored
output coordinate. The original box contributes `2n` rows and the assembled
output contributes two rows, one of which is the harmless inequality `0<=0`.
Output reflection preserves these counts and gives the hypograph construction
with `k_+ L` binaries. The complete unbounded epigraph and hypograph are
contained, not only their graph boundaries.

The one-product result distinguishes exact convex attainment from linear
approximation. At each fixed `p`, an actual convex lift attains
`2^(-2p-2)`, and every convex integer lift has at least that error. For every
`δ>0`, an actual finite binary linear lift with the same `p` binaries has error
at most `2^(-2p-2)+δ`. Exact finite linear attainment at the threshold is not
claimed. The interval lower bound uses a finite grid and pigeonhole argument,
so it does not assume that a largest parity interval or worst-error witness
exists in a nonclosed lift.
