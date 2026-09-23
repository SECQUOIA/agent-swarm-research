# Fine SDP approximations of the unit-capacity rank-one hull require superpolynomial size

Status (2026-09-04): the shifted-slack proof, quantitative formulas, and facial-reduction/duality argument passed independent audit; the underlying face-stability result also passed independent audit. The stronger fixed-error transfer through sign correlation matrices was proposed by the independent SDP reviewer and separately checked by the author. See [the independent audit](../notes/review-rank-one-approximate-sdp.md). Novelty remains provisional. This proof adapts an established pseudo-density lower-bound theorem to slightly shifted quadratic inequalities.

## Statement

Let

```
K_(2m) = conv{ W in R_+^(2m x 2m) : rank(W)<=1, We<=e, W^Te<=e },
A_m = m(184m+6).
```

All matrix l1 norms below are entrywise sums of absolute values. There are absolute constants `c>0` and `m_0` such that the following holds for `m>=m_0`.

If a convex set `Q` satisfies

```
K_(2m) subset Q subset K_(2m)+epsilon U_1,
epsilon <= 1/(2 A_m),
```

and `Q` has an exact semidefinite lift of PSD matrix order `q`, then

```
q >= exp( c (m/log m)^(2/13) ).
```

Thus a uniform additive l1 outer approximation with the displayed error of order `m^-2` cannot have a polynomial-size SDP lift. The lower bound applies nonuniformly, with arbitrary real coefficients. Multiple PSD blocks and scalar inequalities are counted by their total matrix order, by placing them in one block-diagonal PSD cone.

This is a positive-error bound at an explicit inverse-quadratic accuracy scale, not only an exact representation barrier. The constants are conservative. The logarithm in the exponent is retained so that the conclusion follows directly from the quantitative theorem used below without relying on sharper later refinements.

## Established input from the SDP lower-bound literature

We use two results of Lee, Raghavendra, and Steurer in their [author-hosted manuscript, *Lower bounds on the size of semidefinite programming relaxations*](https://www.dsteurer.org/paper/sdpsize.pdf): Theorem 3.8, equation (3.11), PDF p.23, and Theorem 5.3, PDF p.32.

For an odd integer `k>=3`, define

```
f_k(z) = [ (sum_i z_i-k/2)^2 - 1/4 ] / k^2,
z in {0,1}^k.
```

Their pseudo-density construction supplies a function `D:{0,1}^k -> R` with

```
E D = 1,
||D||_infinity <= k^(3/2),
E D f_k = -1/(4k^2),
E D p^2 >= 0 for all polynomials p of degree <= k/2.
```

Expectations are uniform over the Boolean cube. Such a `D` is called a degree-`k` pseudo-density; it need not be nonnegative.

The quantitative consequence (3.11), obtained directly from the contrapositive of their Theorem 3.1, says that if `f:{0,1}^k->[0,1]` and a degree-`d` pseudo-density obeys `E D f < -delta`, then the matrix

```
M(S,x)=f(x_S),      S subset [m], |S|=k, x in {0,1}^m,
```

satisfies, for `m>=2k`,

```
rank_psd(M)
 >= [ c_0 delta m / (d k^2 ||D||_infinity log m) ]^(d/4)
    [ delta/||D||_infinity ]^(3/2) sqrt(E f),
```

where `c_0>0` is universal. This consequence needs the displayed pseudo-density hypothesis; it does not require knowing the exact sum-of-squares degree of `f`, which appears in the separate statement (3.10). The displayed source results are established inputs; their proofs are not claimed as new.

## Lemma 1: PSD lifts factor matrices of valid affine slacks

Suppose a nonempty convex set `R` has a lift over `S_+^q`, and finitely many affine functions `ell_s` are nonnegative on `R`. For any finitely many points `X_t in R`, the nonnegative matrix

```
M_st = ell_s(X_t)
```

has PSD rank at most `q+1`.

**Proof.** Write `R=pi(S_+^q intersect L)`, allowing an affine output map if desired. Restrict the lift to the smallest face of `S_+^q` containing its feasible set. Every face of the PSD cone is a PSD cone on a subspace, so this restriction has order `r<=q`; in that subspace the affine constraints admit a positive definite feasible matrix. This follows by taking a relative-interior point of the feasible set, or a finite convex combination spanning all feasible ranges.

For each `s`, minimize `ell_s(pi(Y))` over the restricted lift. The problem is strictly feasible and its optimal value is finite and nonnegative. Semidefinite conic duality therefore gives a dual optimum and an identity on the affine subspace of the form

```
ell_s(pi(Y)) = <B_s,Y> + tau_s,
B_s positive semidefinite,   tau_s>=0.
```

Choose a feasible lift `Y_t` for every `X_t`. Then

```
M_st = <diag(B_s,tau_s), diag(Y_t,1)>.
```

This is a PSD factorization of order `r+1<=q+1`. Facial reduction is used only as an existence argument, with no complexity or numerical regularity claim. QED.

## Lemma 2: fixed-accuracy sign-correlation approximations have large PSD lifts

Define the sign correlation polytope

```
SCOR(m) = conv{yy^T:y in {-1,1}^m}.
```

Let `R` be a convex set satisfying

```
SCOR(m) subset R subset SCOR(m)+eta U_1,
eta <= 1/2.
```

Then every PSD lift of `R` has order

```
q >= exp( c_1 (m/log m)^(2/13) )
```

for all sufficiently large `m`, where `c_1>0` is universal.

**Proof.** Fix an odd `k` with `3<=k<=m/2`. For each `k`-element subset `S` of `[m]`, define

```
L_S(Y) = [sum_(i,j in S)Y_ij-1]/(4k^2).
```

Index the sign vectors by `x in {0,1}^m` through `y=2x-e`. Then

```
L_S(yy^T) = [(sum_(i in S)y_i)^2-1]/(4k^2)
           = f_k(x_S).
```

Oddness of `k` implies `L_S>=0` on `SCOR(m)`. Every coefficient in its linear part is either zero or `1/(4k^2)`. Thus

```
L_S(Y) >= -eta/(4k^2)       for every Y in R.
```

Set `theta=eta/(4k^2)`. The affine functions `ell_S=L_S+theta` are nonnegative on `R`; their values at the sign outer products form the matrix

```
M(S,x)=f_k(x_S)+theta.
```

Lemma 1 gives `rank_psd(M)<=q+1`. Different binary vectors can index the same sign outer product, but repeated columns cause no problem for this factorization or for the established rank lower bound.

Since `eta<=1/2`,

```
0<=theta<=1/(8k^2),
E D(f_k+theta)=-1/(4k^2)+theta<=-1/(8k^2).
```

Here the pseudo-density remains a function of the original binary vector `x`; no change of its domain or degree is needed. The shifted function lies in `[0,1]` and has maximum less than `1/4`. Take `delta=1/(16k^2)` for the strict negative-expectation hypothesis. Its uniform mean satisfies

```
E(f_k+theta)>=E f_k=(k-1)/(4k^2)>=1/(6k).
```

The quantitative lower bound with `d=k` therefore gives universal constants `c_2,c_3>0` with

```
q+1 >= rank_psd(M)
     >= c_2 k^(-23/4)[c_3 m/(k^(13/2)log m)]^(k/4).       (1)
```

Choose odd `k` comparable to `a(m/log m)^(2/13)` for a sufficiently small universal `a>0`. For all sufficiently large `m`, it lies between three and `m/2`, and the bracketed base is at least 16. The right side of (1) is at least `c_2 k^(-23/4)2^k`, hence `exp(Omega(k))`. Absorbing the additive one proves the lemma. QED.

The use of sign coordinates is material. In binary coordinates, the centered-square slack has diagonal coefficient magnitude of order `1/k`; in sign coordinates all coefficients have magnitude `1/(4k^2)`. The latter permits a fixed error `eta` while preserving the negative pseudo-expectation.

## Proof of the main theorem

Let `H_F` be the affine subspace

```
H_F={W:trace W=1, sum_i W_(i,m+i)=0, sum_ij W_ij=m}.
```

Partition any `2m`-by-`2m` matrix into four `m`-by-`m` blocks and define the linear map

```
J(W)=m(W_11-W_12-W_21+W_22).
```

For an exact face atom `W=(x,e-x)(x,e-x)^T/m`,

```
J(W)=(2x-e)(2x-e)^T.
```

Consequently `J(F)=SCOR(m)`. Each source entry contributes to exactly one output entry, with coefficient `m` or `-m`; therefore

```
||J(U)-J(V)||_1<=m||U-V||_1.
```

The proof of the [quantitative face-transfer theorem](rank-one-correlation-face-stability.md) gives, for every `Y in Q intersect H_F`, a point `V in F` with

```
||Y-V||_1<=(184m+6)epsilon.
```

It follows that

```
R=J(Q intersect H_F)
```

satisfies `SCOR(m) subset R subset SCOR(m)+A_m epsilon U_1`. The argument uses the entire-matrix distance estimate before the principal-block projection in that theorem, so it applies to this different output map with the same norm bound.

Adding affine equations and composing the output map does not change the PSD cone in a lift of `Q`. The assumption `epsilon<=1/(2A_m)` implies `A_m epsilon<=1/2`. Lemma 2 now proves the result. QED.

## What this does and does not establish

The approximate lower bound differs from the exact-hull result: it allows a positive, explicitly inverse-polynomial outer error. It also differs from the approximate LP result: its proof uses the shifted centered-square slack family and pseudo-densities, not the unique-disjointness inequality family, which alone does not supply an unrestricted PSD lower bound.

The result concerns uniform additive error over the entire hull, equivalently all linear objectives with coefficient infinity norm at most one. It implies in particular that an error sequence `o(m^-2)` cannot have polynomial-size SDP lifts, but the displayed fixed constant at scale `m^-2` is stronger. It does not exclude good bounds for a restricted cost family, an objective-specific relaxation, or a weaker accuracy requirement. The proof gives no exponential lower bound in `m` for approximate SOCP lifts; embedding a product of Lorentz cones into a PSD cone transfers only the displayed superpolynomial bound on total cone size.

A targeted novelty search found no matching fine-SDP lower bound for this unit-capacity continuous rank-one flow hull. The robustness of the underlying correlation-polytope lower-bound method may be known; the proposed new contribution is its explicit application through the quantitative pooling-block face. Independent audit and a broader prior-art search remain necessary before publication claims.
