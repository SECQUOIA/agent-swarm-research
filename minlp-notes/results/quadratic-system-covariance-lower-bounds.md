# Quadratic systems: a covariance certificate and a counterexample to scalar rank

Date: 2026-09-05. Status: independently reviewed; see `notes/review-quadratic-vector-cross-product.md`.
The underlying matrix spaces and covariance tools are established.
The proposed result is a formulation-dimension bound for simultaneous
quadratic approximation. Publication priority is unestablished.

## Main result

Let `B subset R^n` be a bounded full-dimensional box of volume `V>0`,
and let `F=(f_1,...,f_m)` have quadratic coordinates

```
f_j(x)=(1/2)x^T H_j x+a_j^T x+b_j,   H_j=H_j^T.
```

A relaxation must contain the entire graph of `F` on `B`. Its error is
at most `ε>0` if every admitted `(x,w)`, `x in B`, obeys
`|w_j-f_j(x)|<=ε` for each output. Let `p_conv(ε)` be the minimum number
of unrestricted integer coordinates in an arbitrary finite-dimensional
convex lift. Let `p_bin(ε)` be the minimum number of binaries in a
linear lift. Continuous dimension and coefficients are unrestricted.

**Theorem 1 (sum-of-squares certificate).** Suppose that, for some
`c>0`,

```
sum_(j=1,...,m) H_j² = c I_n.
```

Then

```
p_conv(ε) = (n/2) log2(1/ε)+O_(F,B)(1),
p_bin(ε)  = (n/2) log2(1/ε)+O_(F,B)(1).
```

More explicitly, every admissible convex lift with `p` integer
coordinates satisfies

```
ε >= [sqrt(c n/m) V^(2/n) / (4(n+2) omega_n^(2/n))]
      * 2^(-2p/n),
```

where `omega_n` is the volume of the unit Euclidean ball. The upper
bound has a linear binary formulation of size
`O_(F,B,n,m)(log(1/ε))` for each fixed system and box.

**Theorem 2 (scalar rank is insufficient).** Consider the three outputs

```
F(x,y) = x cross y
       = (x_2 y_3-x_3 y_2,
          x_3 y_1-x_1 y_3,
          x_1 y_2-x_2 y_1),
x,y in [0,1]^3.
```

Every nonzero scalar linear combination of the three Hessians has
rank four. Nevertheless,

```
p_conv(ε)=p_bin(ε)=3 log2(1/ε)+O(1)
```

in the sense that both minima have that asymptotic expansion. Thus
half the maximum rank in the Hessian span, which is two here, does
not determine the precision coefficient for simultaneous outputs.
The coefficient for this system is three.

## Covariance inequality

Let compact `S subset R^n` have positive volume. Translate its centroid
to zero and let `X,Y` be independent uniform points in `S`. Their
covariance `Sigma` is positive definite: otherwise a nonzero linear
functional would vanish almost everywhere on `S`, contradicting
positive volume.

Suppose `q_j(v)=(1/2)v^T H_j v` obeys

```
|q_j(s-t)|<=delta_j   for all s,t in S.
```

For `A_j=X^T H_j X`, `B_j=Y^T H_j Y`, and `C_j=X^T H_j Y`, centering and
independence give

```
E[q_j(X-Y)²]
 = (1/2)E[A_j²]+(1/2)(E[A_j])²+E[C_j²]
 >= tr(H_j Sigma H_j Sigma).
```

Indeed, the mixed expectations involving `A_j C_j` and `B_j C_j`
vanish, and `E[C_j²]=tr(H_j Sigma H_j Sigma)`. Therefore

```
sum_j tr(H_j Sigma H_j Sigma) <= sum_j delta_j².
```

Now assume `sum_j H_j²=cI_n`. Diagonalize
`Sigma=U diag(lambda_1,...,lambda_n) U^T` with all `lambda_i>0`, and
write `K_j=U^T H_j U`. Define

```
W_ab=sum_j (K_j)_(ab)².
```

These numbers are nonnegative and symmetric. Every row and column sum
is `c`, since
`sum_b W_ab=(sum_j K_j²)_(aa)=c`. Their total sum is `cn`. The weighted
arithmetic-geometric mean inequality, with weights `W_ab/(cn)`, gives

```
sum_j tr(H_j Sigma H_j Sigma)
 =sum_(a,b) W_ab lambda_a lambda_b
 >=cn exp(sum_(a,b) [W_ab/(cn)] log(lambda_a lambda_b))
 =cn (det Sigma)^(2/n).
```

Zero weights are simply omitted. Combining the two inequalities yields

```
det Sigma <= [(sum_j delta_j²)/(cn)]^(n/2).
```

The familiar volume-covariance inequality is

```
volume(S) <= omega_n (n+2)^(n/2) sqrt(det Sigma).
```

For a short proof, map the centered set by `Sigma^(-1/2)`. Its
covariance is identity, so its mean squared norm is `n`. Among sets
of a given volume, the centered ball minimizes the integral of squared
norm: moving volume from outside the ball to equal vacant volume
inside cannot increase that integral. A ball of radius `R` has mean
squared norm `nR²/(n+2)`. Thus the transformed set's volume is at most
`omega_n(n+2)^(n/2)`, proving the inequality after undoing the map.

Consequently,

```
volume(S) <= omega_n (n+2)^(n/2)
             [(sum_j delta_j²)/(cn)]^(n/4).
```

This proof is elementary and does not invoke operator scaling. Its
constant-marginal matrix identity is related to the normalization used
in that established theory.

## Applying integer parity

Suppose the relaxation is projected from a convex set in variables
`(x,w,u,z)`, with `z in Z^p`. Group exact graph inputs by the parity
class of any feasible integer lift. Two lifted graph points in the
same class have a feasible midpoint with integer coordinates. The
coordinatewise error condition implies

```
|q_j(s-t)|<=4ε
```

for every pair in that class and every `j`. Take the closure of each
class in `B`: the quadratic inequalities persist by continuity, and
the resulting at most `2^p` compact sets cover `B`. This step needs no
closedness or measurability of the original classes or projected lift.

A class of zero volume contributes nothing. Applying the preceding
covariance estimate to every positive-volume class gives

```
V <= 2^p omega_n (n+2)^(n/2)
          [16m ε²/(cn)]^(n/4).
```

Rearrangement is precisely the finite lower bound in Theorem 1.
Integer parity is the published Midpoint Lemma mechanism of Lubin,
Vielma, and Zadik; see
[[lubin2022-mixed-integer-convex-representability]] p.11-12.

## Compact upper construction

Normalize the original box to `[0,1]^n` by an affine change of variables.
Each transformed output is a weighted sum of square and distinct-index
bilinear monomials plus an affine function. Let `C>0` bound, for each
output, the sum of absolute coefficients of its quadratic monomials.

For every input coordinate use one shared depth-`L` binary expansion

```
x_i=A_i+r_i,
A_i=sum_(k=1,...,L)2^(-k) beta_ik,
0<=r_i<=h=2^(-L).
```

For each needed distinct-index product use the identity

```
x_i x_l=A_i x_l+r_i A_l+r_i r_l.
```

The first two terms are sums of binary-times-bounded-continuous
products and have exact linear encodings. Apply McCormick to the last
term, incurring error at most `h²/4`. For a square, use

```
x_i²=A_i x_i+r_i A_i+r_i².
```

Again the first two terms are exact binary products. The residual
square is relaxed by the three inequalities

```
t>=0,   t>=2h r_i-h²,   t<=h r_i.
```

On `0<=r_i<=h`, this contains its graph and has two-sided vertical
error at most `h²/4`. All outputs are assembled as their prescribed
linear combinations of the shared monomial variables.

Choose `L=max{0,ceil[(1/2)log2(C/(4ε))]}`. Then each output has error at
most `C h²/4<=ε`, using exactly `nL` binaries and `O(n²(L+1)+m n²)`
rows and continuous variables. Exact graph points lift by setting each
residual monomial to its true value. This upper construction applies
to every fixed quadratic system; the certificate proves when its
leading integer coefficient cannot be improved.

## Cross-product counterexample

For `a in R^3`, define the skew-symmetric matrix

```
A(a)=[ 0    a_3  -a_2
      -a_3  0     a_1
       a_2 -a_1   0  ].
```

It satisfies `x^T A(a)y=a dot (x cross y)`. Therefore the Hessian of
that scalar quadratic in variables `(x,y)` is

```
H(a)=[0 A(a); -A(a) 0].
```

For `a!=0`, the kernel of `A(a)` is the line spanned by `a`, and its
rank is two. This follows, for example, from
`A(a)^T A(a)=||a||² I-aa^T`. The block matrix `H(a)` consequently has
rank four. Thus the largest scalar Hessian rank in this three-dimensional
span is exactly four.

Let `H_j=H(e_j)`. Direct multiplication gives

```
sum_(j=1,...,3) H_j² = 2 I_6.
```

Theorem 1 applies with `n=6,m=3,c=2,V=1`, proving

```
ε >= [1/(16 omega_6^(1/3))] 2^(-p/3),
p>=3log2(1/ε)-log2(4096 omega_6),
omega_6=pi³/6.
```

The general compact upper uses six coordinates at half precision,
yielding `p<=3log2(1/ε)+O(1)`. Only six off-diagonal products are needed
for this particular system, and there are no square terms.

Any fixed scalar combination has rank four and, by the scalar rank
law, needs leading coefficient two. The simultaneous system needs
coefficient three. This difference rules out the maximum-scalar-rank
conjecture, including when formulation cells may use arbitrary convex
geometry and the integer ranges are unrestricted.

## Direct sums give an arbitrarily large coefficient gap

For `k` independent cross-product blocks there are `6k` input
coordinates and `3k` outputs. Extend each block Hessian by zeros to the
other blocks. Their squared sum is `2I_(6k)`, so Theorem 1 gives
precision coefficient `3k`. Every scalar combination is block diagonal,
with each block of rank at most four, and rank `4k` is attained when
all block coefficient vectors are nonzero. Thus the strongest scalar
rank coefficient is `2k`, leaving an additive gap `k` in the leading
coefficient. This is an immediate corollary of the reviewed-size
construction, not a claim that the underlying matrix-space rank gap
is new.

## Interpretation and limits

The outputs are the signed two-by-two minors of a two-by-three matrix.
Thus the example is a small quadratic-system obstruction relevant to
matrix and bilinear modeling; it does not depend on large dimensions
or pathological coefficients. It concerns the full graph of those
minors. Imposing only that all minors vanish produces a different,
lower-dimensional set, and this full-box graph lower bound cannot be
transferred to that set without a separate argument.

The certificate is sufficient, not claimed necessary. Common Hessian
kernel, maximum scalar rank, and the rank of the combined list of
Hessians are distinct quantities. No general characterization for all
quadratic systems is claimed here.

The alternating matrix space used above is classical bounded-rank
matrix theory. A recent primary discussion is Huang and Landsberg's *On linear spaces of matrices of bounded rank*, Section 2.1,
[open author manuscript](https://people.tamu.edu/~jml/HLLbnddrk5-22-25.pdf).
The search and derivation record is
`notes/quadratic-system-integer-complexity-investigation.md`.

## Verification

`code/quadratic_rank/check_vector.py` verifies the cross-product
Hessians, their squared sum, and the skew-matrix rank identity exactly
with symbolic arithmetic. It tests the covariance determinant energy
inequality on 15 exact positive definite matrices and separately checks
the centered fourth-moment identity for all three output Hessians. All
checks passed on 2026-09-05. General proofs remain the basis of the
claims.
