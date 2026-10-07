# Optimal diagonal scaling for a copositive residual

Date: 2026-10-02. Status: direct derivation with a
[fresh independent review](../reviews/jacobi-copositive-residual-review.md)
finding no substantive gap.
This identifies the exact scaling problem left after PSD and nonnegative
extraction. It does not give a tractable copositive-cone oracle or resolve
the [sparse negative-curvature target](negative-curvature-sparse.md).
No novelty claim or external literature comparison is made.

## Convention and normalized margin

Let `R` be a real symmetric strictly copositive matrix: `x'Rx>0` for
every nonzero `x>=0`. In particular, every diagonal entry `R_ii` is
strictly positive. Write

```
J=diag(R_11,...,R_nn),
g(R)=min_(x>=0, ||x||=1) x'Rx,
gamma(R)=min_(x>=0, x!=0) x'Rx/(x'Jx).
```

Strict copositivity and compactness give `g(R)>0` and `gamma(R)>0`.
Evaluation at coordinate axes gives `gamma(R)<=1`. Equivalently,

```
gamma(R)=max{tau: R-tau J is copositive}.
```

We use the quadratic convention `Q_R(x)=x'Rx`; its Hessian is `2R`.
For a positive diagonal matrix `D`, substitute `x=Dy`. The matrix in
`y` coordinates is `D R D`, not `D^(-1) R D^(-1)`. Its common upper
coordinate curvature and Euclidean orthant growth constant are

```
L(D R D)=2 max_i d_i^2 R_ii,       g(D R D).
```

The claims below concern the homogeneous orthant problem. A diagonal
change of coordinates can change box side lengths; it is not by itself
a complexity claim for a nonhomogeneous box-QP algorithm.

## Jacobi scaling is optimal

Among all positive diagonal congruences,

```
inf_D L(D R D)/g(D R D) = 2/gamma(R).                 (1)
```

The infimum is attained by Jacobi scaling

```
D*=J^(-1/2).
```

Indeed, `D* R D*` has unit diagonal, and changing variables in the
Rayleigh quotient gives `g(D* R D*)=gamma(R)`. Its ratio is therefore
the right side of (1).

To prove optimality, fix arbitrary `D` and put
`m=max_i d_i^2 R_ii>0` and `h=g(D R D)>0`. The definition of growth
is equivalent to copositivity of `R-h D^(-2)`. Also

```
D^(-2) >= J/m
```

entrywise on the diagonal. Adding the nonnegative diagonal matrix
`h(D^(-2)-J/m)` shows that `R-(h/m)J` is copositive. Thus
`gamma(R)>=h/m`, or `L(D R D)/g(D R D)=2m/h>=2/gamma(R)`.

Positive diagonal entries are necessary here. A zero diagonal already
precludes strict copositivity and positive Euclidean growth. The result
does not assert the same normalization for a boundary-copositive
residual with zero diagonal entries.

## Rational scaling with a constant-factor loss

Exact Jacobi factors may be irrational. If `R` is rational, choose
positive dyadic factors `d_i=2^(k_i)` satisfying

```
1 <= d_i^2 R_ii < 4.
```

Such exponents are found by exact rational comparisons. Their absolute
values, and the bit lengths of the factors and inverses, are bounded by
a constant times the encoding length of the corresponding positive
diagonal entries.

Since `R-gamma(R)J` is copositive, congruence gives

```
D R D >=_COP gamma(R) diag(d_i^2 R_ii) >=_COP gamma(R) I.
```

Here `>=_COP` means that the matrix difference is copositive. Hence
`g(D R D)>=gamma(R)` and `L(D R D)<=8`, giving

```
L(D R D)/g(D R D) <= 8/gamma(R).                      (2)
```

Thus rational dyadic scaling loses at most a factor four relative to
the optimal ratio. This statement presumes that the residual itself is
available with rational entries of controlled encoding length; it does
not supply such an extraction.

## Clipping large positive entries preserves the margin

Let `B` be copositive with unit diagonal, and define `C` by replacing
every off-diagonal entry above one by one. Then

```
g(C)=g(B),       diag(C)=I,       -1<=C_ij<=1.          (3)
```

Thus clipping is an entrywise nonnegative extraction with no loss of
normalized Euclidean growth. Applied after exact Jacobi scaling, it
preserves `gamma(R)` exactly. The lower entry bound follows by testing
copositivity on `e_i+e_j`.

For the margin claim, fix `x>=0`. Whenever a clipped edge has both
endpoint coordinates positive, move their total mass to one endpoint:
choose the first with probability `x_i/(x_i+x_j)` and the second with
the complementary probability. The mean vector is preserved. Since
`C_ii=C_jj=C_ij=1`, the contribution on those two coordinates is
`(x_i+x_j)^2`, constant along the transfer; every other term depending
on them is affine. Thus the conditional expected quadratic value is
unchanged. Each transfer reduces support size, so after at most `n-1`
transfers there is a random vector `Y` with no active clipped edge.
At every such outcome `Y'CY=Y'BY`. Conditional mean preservation and
convexity of squared norm give

```
x'Cx=E[Y'BY]>=g(B) E||Y||^2>=g(B)||x||^2.
```

The last inequality uses `g(B)>=0`. Therefore `g(C)>=g(B)`. The
entrywise inequality `C<=B` gives the reverse inequality on the
nonnegative orthant. This proves (3), including boundary copositivity.
The finite random process is only a proof device.

There is a fully rational version for the dyadic scaling above. More
generally, suppose `B` is copositive and `B_ii<=a` for a positive
rational `a`. Cap its positive off-diagonal entries at `a`. At a capped
edge the coefficient governing curvature under mass transfer is
`B_ii+B_jj-2a<=0`. The quadratic is concave along that transfer, so
the expected endpoint value is at most its current value. The same
argument, now with `x'Cx>=E[Y'BY]`, proves exact preservation of `g(B)`.
The diagonal is unchanged.

In particular, dyadic scaling gives diagonal entries in `[1,4)`, so
capping at four leaves a rational residual with all entries in
`[-4,4]`, the same Euclidean growth constant, and the same diagonal
curvature. The lower entry bound follows from the two-coordinate
copositivity condition `B_ij>=-sqrt(B_ii B_jj)`. This bounded-entry
normal form does not bound its growth away from zero uniformly over
all original matrices; the residual-existence question remains.

## The exact extraction problem at a fixed threshold

Let `A` be the original symmetric matrix, and permit a decomposition

```
A=P+N+R,
P positive semidefinite,
N symmetric and entrywise nonnegative.
```

Both extracted forms are nonnegative on the nonnegative orthant.
For a fixed `tau in (0,1]`, the following statements are equivalent:

1. Such a decomposition has a strictly copositive residual that admits
   diagonal scaling with curvature/growth ratio at most `2/tau`.
2. The following fixed-threshold conic system is feasible:

```
A=P+N+R,
P >=_PSD 0,       N >= 0 entrywise,
R_ii > 0 for every i,
R-tau diag(R) >=_COP 0.                              (4)
```

Here `diag(R)` denotes its diagonal matrix. The last two conditions
already imply strict copositivity of `R`, since
`x'Rx>=tau sum_i R_ii x_i^2` for every `x>=0`. Equivalence follows
from (1) and the definition of `gamma(R)`.

For fixed `tau`, all matrix expressions in (4) are affine; the
constraints are membership in the PSD, entrywise nonnegative, and
copositive cones, together with strict linear diagonal inequalities.
There is no remaining nonlinear search over diagonal scalings. One may
add linear support restrictions on `R` to preserve a specified
interaction graph. Without those restrictions, a dense residual would
not automatically inherit the original treewidth. Sparsity requirements
on the extracted matrices, if desired, must also be stated explicitly.

Copositive feasibility is the unresolved part, not a routine tractable
conic program. Nor does (4) prove a bound on attainable `tau` in terms
of the original bag size, negative curvature, and Euclidean growth.
It gives an exact way to state that missing structural question.
A later algorithm would also need to find an appropriate decomposition
and control its encoding length.

## A useful composition property

There is a positive structural consequence for supplied local
extractions. Suppose a matrix is given as a sum of embedded bag matrices,

```
A=sum_t E_t' A_t E_t,
A_t=P_t+N_t+R_t,
P_t >=_PSD 0,       N_t >= 0,
R_t-tau diag(R_t) >=_COP 0,
(R_t)_ii > 0.
```

Here `E_t` selects the coordinates of bag `t`, every global coordinate
belongs to at least one bag, and the same `tau>0` works for every bag.
Then set `P=sum E_t'P_tE_t`, and similarly define `N,R`. The first two
matrices remain PSD and entrywise nonnegative, respectively. Moreover,

```
R-tau diag(R)
 =sum_t E_t'[R_t-tau diag(R_t)]E_t
```

is copositive, and every diagonal entry of `R` is positive. Thus the
global normalized residual margin is at least `tau`, independently of
how many bags contain a coordinate. All three assembled matrices are
supported on the union of the bag cliques.

Consequently a supplied decomposition into locally certifiable pieces
can combine without an occurrence penalty in this normalized margin.
The assumption is substantive: global strict copositivity and bounded
treewidth do not here imply that such local decompositions exist.
In particular, no claim that every width-two copositive matrix is SPN
is used or made.

## Verification and limits

The statements follow from the displayed cone inequalities. No numerical
tests, project-wide verification, or CI inspection were performed.
The independent review checked every stated implication, including
the clipping supermartingale. A designated literature scout is comparing
the normalization and block-decomposition ingredients with prior work.
The formulation separates three questions: existence of a well-conditioned
residual, finding its
extraction, and certifying it with a sparse algorithm. The proved results
are optimal scaling, rational approximation, margin-preserving clipping,
the fixed-threshold equivalence, and the stated composition implication.
