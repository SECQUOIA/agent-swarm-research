# Noncommutative rank determines integer precision for quadratic systems

Date: 2026-09-05. Status: independently reviewed; see
`notes/review-quadratic-noncommutative-rank.md`. Publication priority is unestablished. The algebraic
rank and capacity theorems used below are established results.

## Statement and scope

Let `B` be a bounded closed full-dimensional box in `R^n`, and let

```
F=(f_1,...,f_m),   f_j(x)=(1/2)x^T H_j x+a_j^T x+b_j,
H_j real symmetric,   m>=1.
```

A graph relaxation contains every `(x,F(x))`, `x in B`, and admits only
points with `|w_j-f_j(x)|<=ε` for all outputs and all admitted `x in B`.
It may be represented as the projection of
`K intersect (R^(n+m+d) times Z^p)`, where `K` is an arbitrary convex
set in a finite-dimensional real space. Neither closure of `K` nor
boundedness of its integer coordinates is required. Let `p_conv(ε)`
be the least such integer dimension. Let `p_bin(ε)` be the least number
of binaries in a linear extended formulation with the same properties.

Form the pencil `L(t)=sum_j t_j H_j`, with freely noncommuting variables,
and let `r` be its rank over the complex free skew field. This is the
noncommutative rank of the Hessian space. The word "noncommutative"
refers to this algebraic invariant, not to the real optimization variables.

**Theorem.** For each fixed `F,B`, as `ε` decreases to zero,

```
p_conv(ε) = (r/2) log2(1/ε)+O_(F,B)(1),
p_bin(ε)  = (r/2) log2(1/ε)+O_(F,B)(1).
```

The binary upper construction has `O_(F,B,n,m)(1+log(1/ε))` variables
and rows. Its coefficients may be arbitrary real numbers. This is a
formulation-size and integer-dimension theorem, not a polynomial-time
bit-complexity claim for finding or encoding its coordinate change for
arbitrary real data. For rational data, the independently reviewed
`quadratic-ncrank-rational-construction.md` supplies a deterministic
polynomial-bit construction and a uniform precision rate with polynomial
input-size overhead.
If `r=0`, all Hessians vanish and both minima are exactly zero.

The full graph on a full-dimensional box is essential to this statement.
Additional equations that restrict the input domain can change the answer.
The theorem measures auxiliary integer coordinates, independently of any
original discrete decisions in an optimization model.

## Established algebra used in the proof

Write `A(U)=sum_j H_j U` for a complex subspace `U`. The shrunk-subspace
characterization is

```
n-r = max_(U subset C^n) [dim U-dim A(U)].                 (1)
```

For a square complex tuple with full noncommutative rank, the completely
positive map `T(P)=sum_j H_j P H_j*` has positive capacity

```
cap(T)=inf_(P Hermitian positive definite) det T(P)/det P > 0. (2)
```

Here `*` on numerical matrices is conjugate transpose. These imported
facts follow from the rank, shrinking, and operator-capacity results
presented by Garg, Gurvits, Oliveira, and Wigderson, *Operator Scaling:
Theory and Applications*, Theorems 1.4 and 1.17 and Section 2,
[open published paper](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
The capacity equivalence is due to Gurvits; it is used for arbitrary
fixed coefficients, without a quantitative rational encoding bound.

The complex free skew field has an involution fixing its free variables
and conjugating its scalars. It reverses products and sends an inverse
to the inverse of the adjoint. See Volčič, *Hilbert's 17th problem in
free skew fields*, Section 2.1,
[open published paper](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1).
Thus our pencil is Hermitian over this division ring.

## A full-rank principal restriction exists

**Lemma 1.** A Hermitian matrix of rank `r` over a division ring with
involution has an invertible principal submatrix of order `r`.

**Proof.** Induct on the matrix order. A nonzero diagonal entry is an
invertible one-by-one Hermitian pivot. If all diagonal entries vanish
but the matrix is nonzero, an off-diagonal entry `a!=0` gives the
invertible Hermitian principal pivot

```
D = [ 0  a  ],       D^(-1) = [ 0       (a*)^(-1) ].
    [ a* 0 ]                 [ a^(-1)   0        ]
```

After putting the pivot first, write the matrix as
`[D E; E* G]`. Its Schur complement `S=G-E*D^(-1)E` is Hermitian.
Block elimination over the division ring gives
`rank M=order(D)+rank S`. Induction supplies an invertible principal
submatrix `S[J,J]` of order `rank S`. The original principal submatrix
on the pivot indices together with `J` is invertible, because its Schur
complement is exactly `S[J,J]`. The zero matrix has the empty principal
submatrix. This proves the claim. ∎

Apply the lemma to `L`. There is an index set `I`, `|I|=r`, such that
`L[I,I]=sum_j t_j H_j[I,I]` has full noncommutative rank `r`. The
compressed Hessians are still real symmetric. Fixing every coordinate
outside `I` to an interior value of its interval leaves a full box
`B_I` of positive `r`-dimensional volume and exactly those Hessians.
The fixed-coordinate terms only alter affine terms. The compressed tuple has positive capacity by (2), or the positive
energy constant constructed below directly from (1).

## Positive capacity forces a volume bound

Work first in dimension `s>0` with real symmetric Hessians `G_j` and
positive complex capacity `κ`. For real positive definite `P`, (2)
implies `det T(P)>=κ det P`, with `T(P)=sum_j G_j P G_j`.

Let `S` be a compact set of positive volume satisfying

```
|(1/2)(x-y)^T G_j(x-y)|<=4ε     for every x,y in S and every j. (3)
```

Center a uniform random point `X` in `S`, take an independent copy `Y`,
and denote their positive definite covariance by `Σ`. Independence and
zero means give

```
E[((1/2)(X-Y)^T G_j(X-Y))²]
 = (1/2)E[(X^T G_j X)²]
   +(1/2)(E[X^T G_j X])² + tr(G_j Σ G_j Σ).
```

Consequently

```
tr(Σ T(Σ)) = sum_j tr(G_j Σ G_j Σ) <= 16m ε².              (4)
```

The following capacity-to-trace inequality is standard; GGOW Section
1.7 gives its stronger two-matrix variational form. Apply the
arithmetic-geometric mean inequality to the positive matrix `Σ^(1/2) T(Σ) Σ^(1/2)`. Capacity gives

```
tr(Σ T(Σ)) >= s [det Σ det T(Σ)]^(1/s)
             >= s κ^(1/s)(det Σ)^(2/s).                  (5)
```

The volume-covariance inequality is

```
vol_s(S)<=omega_s (s+2)^(s/2) sqrt(det Σ).
```

For completeness, whiten the centered set to covariance identity. Its
mean squared Euclidean norm is `s`. Among sets of a given volume a
centered ball minimizes the integral of squared norm, by exchanging
points outside the ball with missing points inside. A ball of radius
`R` has mean squared norm `sR²/(s+2)`. The whitened set therefore has
volume at most `omega_s(s+2)^(s/2)`, proving the inequality.
Combining it with (4) and (5) proves

```
vol_s(S) <= C_s ε^(s/2),
C_s=omega_s(s+2)^(s/2) [16m/(s κ^(1/s))]^(s/4).           (6)
```

Zero-volume sets satisfy (6) without the probabilistic argument.

## An elementary substitute for the capacity import

The existence of the energy constant in (5) can also be proved without
operator capacity. This independent argument was supplied during review.
Assume the tuple has full noncommutative rank, hence no real shrunk
subspace by (1). For every real orthogonal matrix `O`, define

```
W_ab(O)=sum_j ((O^T G_j O)_(ab))².
```

View its positive entries as edges in a bipartite graph between column
and row indices. If a column set `J` had fewer than `|J|` neighboring
rows, every matrix `O^T G_j O` would send the coordinate space on `J`
into that smaller row space. This would be a shrunk subspace. Hall's
matching theorem therefore gives a perfect matching, and the permanent
`per W(O)` is positive. It is a continuous function on the compact
orthogonal group. Consequently

```
μ=min_(O in O(s)) per W(O)>0.
```

Diagonalize `Σ=O diag(lambda) O^T`. One permutation `π` satisfies
`product_a W_(a,π(a))>=μ/s!`, since the permanent sums `s!` products.
All selected entries are positive. The arithmetic-geometric mean
inequality applied to those `s` terms gives

```
tr(Σ T(Σ)) = sum_(a,b) W_ab lambda_a lambda_b
 >= sum_a W_(a,π(a)) lambda_a lambda_(π(a))
 >= s (μ/s!)^(1/s) (det Σ)^(2/s).
```

Thus (6) and the ensuing lower proof hold with `κ=μ/s!`, even without
invoking (2). This constant need not equal the operator capacity. The
capacity expression remains a separate useful finite certificate.
Only the shrunk-subspace characterization is needed to obtain the
qualitative leading coefficient by this route.

## Parity gives the integer lower bound

For each parity vector `a in {0,1}^p`, let `S_a` consist of graph inputs
that have some feasible lifted graph point whose integer coordinates
have parity `a`. The `2^p` sets cover the input box. Two points in the
same set have feasible graph lifts with integer midpoint; convexity
therefore admits the midpoint of their visible graph points. The
quadratic midpoint identity gives

```
|(f_j(x)+f_j(y))/2-f_j((x+y)/2)|
 = |(1/8)(x-y)^T G_j(x-y)| <= ε.
```

This is (3). Taking each `S_a`'s closure in the compact box preserves
(3), gives compact measurable sets, and still covers the box. No
measurability of the original projection and no closure of `K` is
needed. This is a quantitative application of the established parity
method in Lubin, Vielma, and Zadik, *Mixed-integer convex
representability*, Lemma 4.1; see the local literature package
`literature/papers/lubin2022-mixed-integer-convex-representability/`.

Use the principal slice from Lemma 1 with `s=r`, volume `V_I`, and
compressed capacity `κ_I>0`. From (6),

```
V_I <= 2^p C_r ε^(r/2),
p >= (r/2)log2(1/ε)+log2(V_I/C_r).                         (7)
```

Equivalently, every admissible formulation obeys

```
ε >= [sqrt(r κ_I^(1/r)/m) V_I^(2/r)
      /(4(r+2)omega_r^(2/r))] 2^(-2p/r).
```

This lower bound applies to arbitrary convex lifts with unrestricted
integer ranges, and hence also to binary linear formulations.

## A real shrunk space can be chosen

Set `d=n-r`. An optimizer of (1) exists because deficiencies are integers
in a finite range. For complex subspaces define
`g(U)=dim U-dim A(U)`. The identities

```
A(U+V)=A(U)+A(V),       A(U intersect V) subset A(U) intersect A(V)
```

and the dimension formula imply supermodularity:

```
g(U+V)+g(U intersect V)>=g(U)+g(V).
```

Since the Hessians are real, `g(conjugate U)=g(U)`. If `g(U)=d`, both
`g(U+conjugate U)` and `g(U intersect conjugate U)` are at most `d`,
and supermodularity forces both to equal `d`. The sum is invariant
under conjugation and therefore is the complexification of a real
subspace `U_0`. Its image under the real Hessians is likewise the
complexification of `A(U_0)`. Complex and real dimensions agree for
these complexifications. Hence there are real spaces

```
U=U_0,    V=A(U_0),    dim U-dim V=d.                    (8)
```

This argument avoids any unstated real-versus-complex rank assumption.

## Symmetry turns shrinking into useful coordinates

**Lemma 2.** For real symmetric `H_j` and spaces as in (8), set

```
Z=U intersect V^perp,       W=V intersect U^perp.
```

Then `Z` and `W` are orthogonal, `dim Z-dim W=d`, and `H_j Z subset W`
for every output.

**Proof.** The restrictions `P_V:U->V` and `P_U:V->U` of orthogonal
projection are adjoints, so they have the same rank `t`. Their kernels
are `Z` and `W`. Thus `dim Z=dim U-t` and `dim W=dim V-t`, proving
the dimension identity. Orthogonality follows from `Z subset U` and
`W subset U^perp`. For `z in Z`, membership in `U` gives `H_j z in V`.
For every `u in U`, symmetry gives
`u^T H_j z=(H_j u)^T z=0`, since `H_j u in V` and `z in V^perp`.
Thus `H_j z in U^perp` as well, proving the claim. ∎

Complete orthonormal bases of `Z,W` by a basis of
`R=(Z+W)^perp`. In these coordinates every Hessian has block form

```
[ 0    B_j   0   ]
[ B_j^T C_j  D_j ]
[ 0    D_j^T E_j ].                                      (9)
```

Assign precision exponents zero to coordinates in `Z`, one to those
in `W`, and one half to those in `R`. Every nonzero quadratic monomial
in (9) has endpoint exponents whose sum is at least one, and

```
sum_i alpha_i = dim W+(1/2)dim R
              = (n-d)/2 = r/2.                          (10)
```

A square monomial uses twice its coordinate exponent. Coordinates
in `Z` have no squares or mutual products and do not couple to `R`.
This is why they can remain continuous at fixed precision.

## Compact binary construction with those exponents

Transform the original box by the orthogonal coordinate change and
enclose its image in a bounded box. Normalize that box to `[0,1]^n`
using diagonal positive scalings and a translation. Neither operation
creates any quadratic terms absent from (9). Retain the original
linear box constraints and the affine coordinate identities in the
lift. It suffices to approximate the transformed quadratics uniformly
on the larger box.

Write their quadratic terms as `sum_(i<=k) c_(j,ik) y_i y_k`, and let
`C=max_j sum_(i<=k)|c_(j,ik)|`. For `r>0`, `C>0`. Take

```
T=max{0, log2(C/(4ε))},
L_i=ceil(alpha_i T),     h_i=2^(-L_i),
y_i=A_i+rho_i,   A_i=sum_(l=1,...,L_i) 2^(-l) beta_(i,l),
beta_(i,l) binary,       0<=rho_i<=h_i.
```

Every `y_i in [0,1]` has such a representation, including `y_i=1`
by the all-one prefix and residual `h_i`. An empty sum when `L_i=0`
means `A_i=0` and `rho_i=y_i`.

For each distinct product use

```
y_i y_k = A_i y_k + rho_i A_k + rho_i rho_k.
```

Every prefix product is a linear combination of binary-times-bounded-
continuous products, which have exact four-row linear formulations.
Relax the residual product by its McCormick envelope on
`[0,h_i] times [0,h_k]`; its maximum absolute graph error is
`h_i h_k/4`. For squares use

```
y_i²=A_i y_i+rho_i A_i+rho_i²,
t>=0,    t>=2h_i rho_i-h_i²,    t<=h_i rho_i,
```

for the residual square. This triangle contains the square graph and
has maximum absolute graph error `h_i²/4`. The exact binary products
remain shared across outputs; there is one approximate value per
required monomial. Form each output by its affine part plus its
coefficient-weighted approximate monomials.

For each nonzero monomial, `alpha_i+alpha_k>=1`, so
`h_i h_k<=2^(-T)`. Therefore every output error is at most
`C 2^(-T)/4<=ε`. All exact graph points are contained by selecting
exact residual products or squares. The binary count satisfies

```
p=sum_i L_i <= (r/2)T+n
             = (r/2)log2(1/ε)+O_(F,B)(1).                (11)
```

The number of monomials is fixed. Each requires only a number of rows
and auxiliary variables proportional to the participating bit depths,
so the total formulation size is linear in `1+log(1/ε)` for fixed data.
Equations (7) and (11), together with `p_conv<=p_bin`, prove the theorem. ∎

## Consequences and novelty boundary

A single scalar quadratic has noncommutative rank equal to its usual
Hessian rank, recovering the scalar rank law. For the three components
of `x cross y` in six variables, the reviewed covariance certificate
`sum_j H_j²=2I_6` gives full noncommutative rank and coefficient three,
although every nonzero scalar combination has ordinary rank four.
Direct sums repeat this strict gap. Details and finite constants are
in `results/quadratic-system-covariance-lower-bounds.md`.

Noncommutative rank, operator scaling, shrunk subspaces, Hermitian
elimination, and the cross-product matrix space are established theory.
The candidate contribution is their connection to the exact leading
integer precision cost of an arbitrary real quadratic output system,
including a compact binary upper bound and an unrestricted convex-lift
lower bound. Searches so far have not located this connection in open
literature; that does not establish publication priority.

## Verification

The independent proof review is recorded in
`notes/review-quadratic-noncommutative-rank.md`. It checked the imported
rank characterization, complex-to-real descent, Hermitian principal
compression, both energy proofs, parity closure, finite constants, and
the compact binary construction.

`code/quadratic_rank/check_shrunk.py` checks 20 exact rational examples
obtained by nonorthogonal congruences: it verifies the symmetrized
subspace dimensions, all required zero Hessian blocks, and the sum of
precision exponents. All checks passed on 2026-09-05. The earlier
`check_vector.py` covers the fourth-moment identity and cross-product
example. These finite checks supplement the proofs.
