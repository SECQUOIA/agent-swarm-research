# Uniform rational bounds at the noncommutative-rank precision rate

Date: 2026-09-05. Status: independently verified candidate corollary;
publication priority unestablished. Both the construction and the uniform
lower estimate were reviewed in
[the independent audit](../notes/review-quadratic-ncrank-rational-construction.md).
This strengthens the constructive upper bound in
[the general quadratic-system theorem](quadratic-system-noncommutative-rank-complexity.md).
It adds an effective rational upper construction and a uniform rational
lower estimate without changing the arbitrary-real-data theorem's scope.

## Statement

Let `F=(f_1,...,f_m)` be a vector of quadratic polynomials with rational
coefficients on a rational bounded closed full-dimensional box
`B=product_i[l_i,u_i]`, where `l_i<u_i`. Let `s` denote the total
binary encoding length of these data, including dimensions. Let `r`
be the noncommutative rank of their symmetric Hessian pencil, as defined
over the complex free skew field in the main theorem.

There is a deterministic algorithm that, given these data and an integer
precision parameter `k>=0`, constructs a rational mixed-integer linear
graph relaxation containing every exact graph point and having coordinatewise
absolute output error at most `2^(-k)` on `B`. Its running time and
total output encoding length are bounded by `poly(s+k)`. Its binary
count satisfies

```
p <= (r/2) k + P(s),
```

for a universal polynomial `P`. No other integer coordinates are needed.
Moreover, for another universal polynomial `Q`, the minima in the main
theorem obey the uniform bounds

```
(r/2)k-Q(s) <= p_conv(2^(-k)) <= p_bin(2^(-k))
             <= (r/2)k+P(s).
```

Thus each minimum equals `(r/2)k` up to an additive polynomial in the
input encoding length, uniformly over rational instances and precisions.
Each coefficient has encoding length `poly(s)+O(k)`, and the number
of rows and variables is `poly(s)(k+poly(s)+1)`.

Consequently the optimal leading precision coefficient can be attained
algorithmically with rational coefficients and polynomial encoding size.
For a fixed rational instance the excess term is constant in `k`,
as in the original asymptotic theorem. This is a construction-time statement,
not a polynomial-time algorithm to optimize the resulting MILP.

The accuracy is specified as a dyadic target to make its input convention
unambiguous. For an arbitrary rational `ε in (0,1]`, first compute
`k=ceil(log2(1/ε))` by integer comparisons; the same result holds with
running time polynomial in `s`, the encoding length of `ε`, and `k`.
No claim is made that an arbitrarily long rational accuracy input can be
read in time depending only on `log(1/ε)`.

## Established algorithmic import

Ivanyos, Qiao, and Subrahmanyam, *Constructive non-commutative rank
computation is in deterministic polynomial time*, Theorem 1.5 in the
[2018 full manuscript](https://arxiv.org/pdf/1512.03531), gives a
deterministic algorithm producing a maximal shrunk subspace over the
base field. Over the rationals, it explicitly bounds all intermediate
and final data by a polynomial in input size. Lemma 5.3 states invariance
of noncommutative rank under field extension. Thus rational Hessians have
a rational maximal shrunk subspace with the same deficiency as over
the complex numbers. These are established algebraic algorithms; no
new rank algorithm is proposed here.

The conference version is also openly available as
[ITCS 2017, Theorem 7](https://drops.dagstuhl.de/storage/00lipics/lipics-vol067-itcs2017/LIPIcs.ITCS.2017.55/LIPIcs.ITCS.2017.55.pdf).
Using merely a polynomial arithmetic-operation count would not suffice:
the rational bit-complexity assertion in the full theorem is essential.
A naive implementation of repeated Wong-sequence operations can cause
coefficient growth and is not what is invoked.

## Rational bases preserve the required quadratic sparsity

Compute a rational basis of the Hessian span by exact elimination and
apply the imported algorithm. It gives a rational subspace `U` with

```
V=sum_j H_j U,
dim U-dim V=n-r.
```

When `r=n`, one may instead use `U=V={0}`. When `r=0`, all
Hessians vanish and the exact affine graph has an immediate rational
continuous linear formulation; no further construction is needed.

Compute rational bases of

```
Z=U intersect V^perp,
W=V intersect U^perp,
R=(Z+W)^perp.
```

These operations require only rational linear algebra. For example,
if matrices `U_b,V_b` contain basis columns, a basis for `Z` is
obtained from the image under `U_b` of
`ker(V_b^T U_b)`. The analogous formula gives `W`, and a
nullspace computation gives `R`.

The spaces `Z,W,R` are mutually orthogonal, but their chosen bases
need not be orthonormal. Put those basis columns into an invertible
rational matrix `T=[Z_b W_b R_b]`. Symmetry still gives
`H_j Z subset W`. Therefore

```
T^T H_j T =
[ 0    B_j   0   ]
[ B_j^T C_j  D_j ]
[ 0    D_j^T E_j ].
```

Indeed, a vector in `Z` is mapped by every Hessian into `W`,
which is orthogonal to both `Z` and `R`. Orthonormalization was
never needed for these zero blocks. This avoids introducing square roots
or algebraic coefficients.

The projection-adjoint argument in the main theorem is a statement about
the spaces themselves, so it continues to give

```
dim Z-dim W=n-r,
2 dim W+dim R=r.
```

All these basis matrices and `T^(-1)` have polynomial encoding length.
For completeness, exact solutions, nullspaces, and inverses of rational
matrices of polynomial dimensions and entry height have polynomial height:
clear denominators and use the determinant bounds for square subsystems,
or fraction-free elimination. Only a fixed number of these linear-algebra
stages follows the imported algorithm, with polynomial-size outputs at
each stage.

## Rational enclosing box and normalized coefficients

Write `v=T^(-1)x`. The exact interval bounds of each linear coordinate
on the original box can be computed without a general optimization oracle:

```
ell_i = sum_j min{(T^(-1))_ij l_j, (T^(-1))_ij u_j},
u'_i  = sum_j max{(T^(-1))_ij l_j, (T^(-1))_ij u_j}.
```

Every interval width `d_i=u'_i-ell_i` is positive: the corresponding
row of an invertible matrix is nonzero, and every original interval has
positive width. Set

```
v=ell+diag(d)y,   y in [0,1]^n,
x=c+Ay,
c=T ell,    A=T diag(d).
```

The enclosing box may be larger than the image of `B`. Retain the
original bounds `l<=c+Ay<=u` and the affine coordinate identities
in the final formulation. Their coefficients are rational of polynomial
height. Positive diagonal scaling and translation preserve all the
quadratic zero blocks.

Expand each transformed polynomial as

```
f_j(c+Ay) = affine_j(y) + sum_(i<=t) c_(j,it) y_i y_t.
```

The Hessian is `A^T H_j A`; distinct-index coefficients are its
off-diagonal entries and square coefficients are half its diagonal
entries. Exact rational arithmetic computes this expansion with
polynomial encoding length.

Define the positive rational number

```
C=max_j sum_(i<=t) |c_(j,it)|.
```

For `r>0`, `C>0`. Its binary encoding length is polynomial in
`s`; in particular `log2(max{1,C})<=poly(s)`.
This controls the precision overhead caused by the coordinate change,
including potentially narrow original boxes and ill-conditioned rational
basis matrices.

## Exact dyadic depths and binary count

Let

```
b=max{0, ceil(log2(C/4))},
K=k+b.
```

The integer `b` is computed exactly by comparing the numerator and
denominator of `C/4` with powers of two. No floating-point logarithm
or conditioning assumption is needed. It satisfies `b<=poly(s)`.

Give each coordinate in `Z` depth zero, each coordinate in `W`
depth `K`, and each coordinate in `R` depth `ceil(K/2)`.
Write the corresponding dyadic prefix and residual as

```
y_i=A_i+rho_i,
A_i=sum_(l=1,...,L_i) 2^(-l) beta_(i,l),
beta_(i,l) in {0,1},  0<=rho_i<=h_i=2^(-L_i).
```

Every nonzero quadratic monomial has either a `W` endpoint or two
`R` endpoints, so `h_i h_t<=2^(-K)`. The main theorem's exact
binary-continuous prefix products and residual McCormick or square
triangle give coordinatewise error at most

```
C 2^(-K)/4 <= 2^(-k).
```

These encodings contain the exact graph and do not discretize the
continuous inputs themselves: the residual variables retain all input
values. A square uses the same residual construction as in the main proof.

The binary count is

```
p=dim(W) K+dim(R) ceil(K/2)
 <= (r/2) K+dim(R)/2
 <= (r/2) k+(r/2)b+n/2.
```

Since `n<=s` and `b<=poly(s)`, this is the asserted bound
with a universal polynomial additive term.

There are at most `n(n+1)/2` required monomials. Each product requires
only `O(L_i+L_t+1)` rows and continuous auxiliaries, and the final
output equations use at most `O(mn^2)` coefficients. The bits
`2^(-l)`, residual widths, and their products have encoding length
`O(K+1)`. Combining them with the fixed transformed rational
coefficients yields individual encoding length `poly(s)+O(k)`,
and total formulation length and construction time `poly(s+k)`.

## A uniform quantitative rational lower bound

Assume `r>0`. Let `D` be a positive common denominator for every Hessian
entry. It may be chosen as the product of the denominators of the original
quadratic coefficients: forming a Hessian only doubles square coefficients
and copies distinct-index coefficients. Let

```
E=product_i [den(l_i) den(u_i)],
```

where all rational endpoints are in reduced form with positive denominators.
Under the ordinary binary encoding convention,
`log2 D<=s` and `log2 E<=s`. The products can have large magnitudes but
have polynomial binary length and are computed by exact integer arithmetic.

The main theorem's Hermitian principal-submatrix argument supplies a
coordinate set `I` of size `r` such that the real symmetric tuple
`G_j=H_j[I,I]` has full noncommutative rank. This restriction does not
change any retained Hessian coefficient, so every `A_j=D G_j` is integral.
Multiplication of every matrix by the same nonzero scalar preserves full
noncommutative rank. The completely positive operator

```
T_A(P)=sum_j A_j P A_j^*,
```

is rank non-decreasing. The established integral capacity bound is

```
cap(T_A) >= r^(-2r).
```

This is Theorem 2.18 of
[Garg, Gurvits, Oliveira, and Wigderson, *Operator Scaling: Theory and Applications*](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
The theorem applies to unnormalized integral Kraus operators and requires
no bound on their entry magnitudes. It is the quantitative import needed
here; compactness of the permanent argument alone would not provide this
explicit input-size estimate.

For the original restricted operator `T_G`, one has `T_G=D^(-2)T_A`.
The determinant is in dimension `r`; thus, directly from the definition,

```
kappa=cap(T_G)=D^(-2r) cap(T_A)
             >= D^(-2r) r^(-2r).
```

The exponent is `2r`, not `2`: capacity is the determinant ratio, not
its `r`th root.

Fix all coordinates outside `I` at any interior values. The volume of
the resulting input box is

```
V_I=product_(i in I) (u_i-l_i) >= E^(-1).
```

Indeed, if `l_i=a_i/b_i` and `u_i=c_i/d_i`, then the positive width is
`(c_i b_i-a_i d_i)/(b_i d_i)>=1/(b_i d_i)`. Including denominator
factors from the other coordinates can only decrease the reciprocal.
The fixed values change only affine terms, so their encoding is irrelevant
to the lower bound; rational midpoints can be used if desired.

The main theorem's finite bound gives, for any admissible convex lift
with `p` unrestricted integer coordinates,

```
epsilon >= [sqrt(r kappa^(1/r)/m) V_I^(2/r)
            /(4(r+2) omega_r^(2/r))] 2^(-2p/r).
```

Since the unit ball is contained in `[-1,1]^r`,
`omega_r^(2/r)<=4`. Substitution of the preceding estimates yields

```
epsilon >= [1/(16 D (r+2) sqrt(mr) E^(2/r))] 2^(-2p/r).
```

At `epsilon=2^(-k)`, this is the explicit uniform lower bound

```
p >= (r/2)k -(r/2)log2 D -log2 E
              -(r/2)log2[16(r+2)sqrt(mr)].
```

All terms subtracted from `(r/2)k` are bounded by a universal polynomial
in `s`; more specifically their size is
`O(r s+r log(mr+2)+s)`. This proves the claimed `Q(s)` bound for
arbitrary convex lifts and therefore for binary linear lifts. Rank zero
remains the exact affine case with both minima zero.

The principal coordinate restriction can also be found in polynomial time
if it is wanted as part of the certificate. Starting with the full index
set, test coordinate deletions with a deterministic rational nc-rank
algorithm. While the order exceeds `r`, the current Hermitian pencil has
an invertible principal submatrix of order `r`, so some deletion preserves
rank `r`. Repeating at most `n-r` times, with at most `n` tests per stage,
finds such a restriction. The lower bound itself only needs its existence.


## What this strengthens

The unrestricted real-data theorem establishes the optimal leading
integer dimension but does not promise an efficiently encoded change of
coordinates. This corollary establishes that rational input data admit
a deterministic polynomial-bit construction attaining that leading
coefficient. The only substantial algorithmic import is the existing
constructive noncommutative-rank theorem. The integral operator-capacity
bound additionally makes the lower estimate uniform up to polynomial
input-size overhead, even against arbitrary real convex lifts.

The result does not provide small numerical coefficient magnitudes
independent of input height, a strongly polynomial implementation, or a
polynomial-time MILP optimizer. Exponential coefficient magnitudes with
polynomial binary encoding are allowed. Uniformity depends on bounding
the rational encoding length; it does not extend to unrestricted real
coefficients with no encoding or height constraint.
