# Rational log-product optimization over a separated convex body

Date: 2026-09-05. Status: supporting oracle lemma, independently reviewed twice.

This note supplies a polynomial-bit allocation oracle for a rational
matrix `C` and a convex set tested by separation. It is a direct use of
classical weak optimization with an explicit feasibility repair, not a
new general convex-optimization algorithm.

## Lemma

Let `C` be a rational `m` by `r` matrix, `r>=1`. Let `K subset R^m`
be closed and convex, with a rational strong separation oracle of
polynomial query and output complexity, and a known positive rational
radius `rho_0` such that `rho_0 B_2^m subset K`. Define

```
D=max{product_i p_i: 0<=p_i<=1, Cp in K}.
```

Given rational `0<nu<=1`, a deterministic polynomial-time algorithm
returns a positive rational feasible allocation `p` with

```
product_i p_i>=exp(-nu)D.                               (1)
```

The running time is polynomial in the matrix and oracle input encoding,
in the binary encoding of `rho_0`, and in the accuracy encoding. Neither
nonnegativity of `C` nor symmetry of `K` is needed for this oracle lemma.

## A bounded log-product hypograph with an explicit inner ball

Put `c=1+sum_ji |C_ji|`. Choose a dyadic `delta=2^(-b)<=1` with

```
delta r c<=rho_0/4.
```

Such `b>=0` is polynomially bounded in input length. The allocation
`delta 1` is feasible, so `D>=delta^r`. Every maximizing allocation
has `p_i>=delta^r`, since all other coordinates are at most one.
Define rational or integer constants

```
a=delta^r/4,
B=r(rb+2)+4,
p_0=(delta/2)1,
t_0=-r(b+1)-2,
sigma=min{delta/(16r),rho_0/(8c),1/4}.
```

Consider the compact convex body in `R^(r+1)`

```
Q={(p,t): a<=p_i<=1, Cp in K, -B<=t<=sum_i log p_i}.
```

Its maximum last coordinate is exactly `log D`; the lower bound on
`p_i` excludes no maximizer. Also

```
B_2((p_0,t_0),sigma) subset Q.
```

Indeed, `a<=delta/4`, so the coordinate margins around `p_0` exceed
`sigma`. The norm bound on `C p_0` is `rho_0/8`, and a perturbation of
norm at most `sigma` changes `Cp` by at most `c sigma<=rho_0/8`.
The point remains in the known ball inside `K`.

At `p_0`, the log product is `-r(b+1)ln2>=-r(b+1)=t_0+2`.
Throughout this ball the coordinates are at least `delta/4`, so the
log-product gradient norm is at most `4r/delta`. Its variation is at
most `1/4`, while the perturbation in `t` is at most `1/4`. Thus the
hypograph inequality remains strict. Finally, `t_0+B>=3`, so the lower
`t` bound holds. The body lies in a ball of radius `2(B+r+1)` centered
at `(p_0,t_0)`. Every constant has polynomial rational encoding.

## A weak separation oracle uses only rational linearization and logs

For a rational query `(p,t)` and positive rational tolerance `eta`, first
check the coordinate bounds `a<=p_i<=1` and `-B<=t<=0`; any violation
has a rational linear separator. Query the strong oracle at `Cp`.
If it is outside `K`, pull the separating inequality back through `C`.
The pulled-back normal cannot vanish on a violated inequality, because
`0 in K`. Strong separating normals can be divided by their nonzero
infinity norm to meet the norm-at-least-one convention of the source
below.

If these checks pass, evaluate `ell=sum_i log p_i` to an interval of
radius `tau=eta/2`, with rational midpoint `ell_hat`. If
`t>ell_hat+tau`, the rational inequality

```
t'<=ell_hat+tau+sum_i (p_i'-p_i)/p_i                    (2)
```

separates the query from `Q`. It is valid by concavity of the log
product, and its normal has Euclidean norm at least one because its
`t'` coefficient is one.

Otherwise `t<=ell+eta`, so lowering `t` to `min(t,ell)` gives a point
of `Q` within distance `eta`. This vertical correction does not violate
`-B`: every allowed `p` has `ell>=-r(rb+2)ln2>-B`.
Thus the oracle can certify weak membership in this case.

Logarithms of positive rationals bounded below by `a` can be evaluated
to the needed interval in polynomial time. The exact gradient entries
`1/p_i` and the tangent inequality coefficients have polynomial bit
length. This is a polynomial weak separation oracle for a convex body
with explicitly known inner and outer balls.

## Classical weak optimization and exact rational repair

Apply Grötschel, Lovász and Schrijver's
[weak separation--optimization equivalence](https://ir.cwi.nl/pub/10046/10046D.pdf),
Definition (5) on printed page 172 and Theorem (3.1) on page 177.
It returns a rational point `y=(p_y,t_y)` with distance at most `rho`
from `Q` and `t_y>=log D-rho`, for any positive rational `rho`, in
polynomial time in its binary encoding.

Choose

```
rho=nu sigma/[4(B+sigma+1)],
y_f=[sigma y+rho(p_0,t_0)]/(sigma+rho).                 (3)
```

This is an exactly feasible rational point of `Q`. To verify feasibility,
let `z in Q` satisfy `||y-z||<=rho`. Then (3) is the convex combination

```
y_f = [sigma/(sigma+rho)]z
       +[rho/(sigma+rho)] [(p_0,t_0)+(sigma/rho)(y-z)].
```

The second point belongs to the known radius-`sigma` ball in `Q`.
Therefore no exact nonlinear projection or irrational optimum is needed.

Since `(p_0,t_0)` is feasible and `log D<=0`, one has
`0<=log D-t_0<=B`. The repaired objective satisfies

```
log D-(y_f)_t <=rho+(rho/sigma)B<=nu.
```

Its first `r` coordinates form an exactly feasible rational allocation,
and `sum_i log (y_f)_i >=(y_f)_t>=log D-nu`. This proves (1).
All operations in the repair are exact rational arithmetic with
polynomial encoding length.

The checker `code/quadratic_rank/check_unconditional_allocation_repair.py`
passed 24 rational central-ball repairs at a known allocation optimum.
Coordinate bounds, convex-body feasibility, and objective bounds were
checked exactly; the log-hypograph inequalities were checked at 100-digit
precision. It does not implement the classical weak-optimization oracle.

Both the [first audit](review-positive-separable-unconditional-precision.md)
and [second audit](review-positive-separable-unconditional-precision-second.md)
passed this lemma, including the exact GLS convention, all explicit
radii, and rational feasibility repair.
