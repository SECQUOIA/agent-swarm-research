# Quantitative stability of the correlation face and approximate LP lower bounds

Status (2026-09-04): rounding estimate, exposing inequality, and approximate LP source transfer independently audited. The sharper outer-transfer estimate was proposed by the independent reviewer and separately checked by the author. See [the audit record](../notes/review-rank-one-stability.md). Constants are deliberately conservative.

## Setting

Use the unit-capacity rank-one hull and its correlation-polytope face from [the exact conic lower-bound result](rank-one-correlation-face-conic-lower-bounds.md):

```
K = K_(2m) = conv{ W>=0 : rank(W)<=1, We<=e, W^Te<=e },
F = { W in K : trace(W)=1, sum_i W_(i,m+i)=0, sum_ij W_ij=m }.
```

Throughout this note, `||W||_1=sum_ij |W_ij|` is the **entrywise** matrix norm, not the induced column-sum norm. For vectors it is the usual l1 norm. Define

```
T(W) = sum_ij W_ij,
D(W) = 1-trace(W),
B(W) = sum_(i=1)^m W_(i,m+i),
g(W) = m-T(W) + (2m+1) B(W) + (4m+1) D(W).
```

The independently checked exposing lemma proves

```
g(W) >= B(W)+D(W) >= 0 on K,      F={W in K:g(W)=0}.
```

The linear part of `g` has coefficient -`(4m+2)` on diagonal entries, `2m` on the selected cross-pair entries, and -1 elsewhere. Hence

```
|g(U)-g(V)| <= (4m+2) ||U-V||_1.
```

## Theorem 1: a global linear error bound

For every `W in K`,

```
dist_1(W,F) <= C_m g(W),     C_m = 136m+10.
```

**Proof.** First consider a nonzero rank-one generator `W=rc^T/S`, with `r,c in [0,1]^(2m)` and `sum r=sum c=S<=2m`. In this proof write `D=D(W)`, `B=B(W)`, and `g=g(W)`.

The exposing-lemma proof gives

```
||r-c||_1 <= 2SD.
```

Round each component of `r` to its nearest point in `{0,1}`, with either choice at 1/2, obtaining `a in {0,1}^(2m)`. Because `min(t,1-t)<=2t(1-t)` on `[0,1]`,

```
sum_i r_i(1-r_i)
 <= sum_i r_i(1-c_i) + ||r-c||_1
 <= 3SD,

u := ||r-a||_1 <= 6SD,
v := ||c-a||_1 <= 8SD.
```

Let `k=sum_i a_i`, and let `h` and `z` be the number of index pairs containing respectively two and zero ones in `a`. Then `k=m+h-z`. The elementary product estimate `|ab-cd|<=|a-c|+|b-d|` for variables in `[0,1]` gives

```
h = sum_i a_i a_(m+i)
 <= sum_i r_i r_(m+i) + ||r-a||_1
 <= SB + ||r-c||_1 + u
 <= SB + 8SD.
```

Make a paired binary vector `b` by removing one 1 from every full pair and adding one 1 to every empty pair. It has exactly one 1 in each pair, `sum b=m`, and

```
||a-b||_1 = h+z = 2h+m-k
 <= 2h + |m-S| + |S-k|
 <= 2SB + 22SD + |m-S|.
```

The matrix `V=bb^T/m` belongs to `F`. To compare `W` and `V` without dividing an error estimate by a possibly small `S`, set `b_tilde=(S/m)b`. The three nonnegative vectors `r,c,b_tilde` have total `S`. For nonnegative vectors, the entrywise l1 norm of an outer product is the product of their l1 norms. Therefore

```
||rc^T/S - b_tilde b_tilde^T/S||_1
 <= ||r-b_tilde||_1 + ||c-b_tilde||_1
 <= ||r-b||_1 + ||c-b||_1 + 2|S-m|,

||b_tilde b_tilde^T/S - bb^T/m||_1 = |S-m|.
```

Combining these estimates yields

```
||W-V||_1
 <= u+v + 2||a-b||_1 + 3|S-m|
 <= 4SB + 58SD + 5|S-m|.
```

From the definition of `g`,

```
|S-m| <= g + (2m+1)B + (4m+1)D.
```

Since `S<=2m` and `B+D<=g`,

```
||W-V||_1
 <= (18m+5)B + (136m+5)D + 5g
 <= (136m+10)g.
```

For `W=0`, choose any paired binary `b`. The distance to `bb^T/m` is `m`, whereas `g(0)=5m+1`, so the stated estimate also holds.

Finally, write an arbitrary `W in K` as a finite convex combination `sum_l lambda_l W_l` of generators. For each generator choose `V_l in F` as above. Then `V=sum_l lambda_l V_l in F`, and convexity of the norm and affinity of `g` give

```
||W-V||_1 <= sum_l lambda_l ||W_l-V_l||_1
           <= C_m sum_l lambda_l g(W_l) = C_m g(W).
```

This proves the theorem. QED.

This is an error bound inside `K`. Computing a generating decomposition of a general point of `K` is not claimed to be easy. For an individual rank-one matrix, however, the rounding procedure is explicit and takes linear work in the number of row/column indices once its marginal vectors are available.

## Corollary 1: an exact penalty for every linear objective

For any cost matrix `H`, any scalar `lambda > C_m ||H||_infinity`, and entrywise coefficient norm `||H||_infinity=max_ij |H_ij|`,

```
min_(W in K) { <H,W> + lambda g(W) } = min_(V in F) <H,V>.
```

Every minimizer of the penalized problem belongs to `F`.

**Proof.** For each `W`, Theorem 1 supplies `V in F` with distance at most `C_m g(W)`. Thus

```
<H,W> + lambda g(W)
 >= <H,V> + (lambda-C_m||H||_infinity)g(W).
```

The extra term is strictly positive when `W` is outside `F`, and vanishes on `F`. Compactness gives existence of minimizers. QED.

This corollary is a general objective-transfer statement. Separate, sharper penalties may give better numerical constants for particular combinatorial reductions.

## Theorem 2: outer-approximation transfer

Let `Q` be any convex set satisfying

```
K subset Q subset K + epsilon U_1,
```

where `U_1` is the entrywise l1 unit ball. Define the affine subspace

```
H_F = {W: D(W)=0, B(W)=0, T(W)=m}
```

and the projected slice

```
P_Q = { m Y_[m],[m] : Y in Q intersect H_F }.
```

Then

```
COR(m) subset P_Q subset COR(m) + A_m epsilon U_1,
A_m = m(184m+6).
```

If `Q` has a lift over a cone `C`, then `P_Q` has a lift over the same cone.

**Proof.** We retain a stronger intermediate estimate from Theorem 1's rounding proof. For each nonzero generator `W_l` with total `S_l`, it constructed `V_l in F` satisfying

```
||W_l-V_l||_1 <= 8m B(W_l)+116m D(W_l)+5|S_l-m|.
```

This also holds for the zero generator, whose distance to any paired atom is `m`. For a finite convex combination `W=sum_l lambda_l W_l`, the exposing-lemma bound gives

```
(S_l-m)_+ <= 2m B(W_l)+4m D(W_l).
```

Here the right side is nonnegative even when `S_l<=m`. Since `|t|=2t_+-t`,

```
sum_l lambda_l |S_l-m|
 <= 4m B(W)+8m D(W)+m-T(W).
```

Taking the same convex combination of the `V_l` therefore supplies `V in F` with

```
||W-V||_1 <= 28m B(W)+156m D(W)+5[m-T(W)].             (*)
```

The right side is nonnegative by this proof; the final bracket alone may have either sign.

Now take `Y in Q intersect H_F` and `W in K` with `||Y-W||_1<=epsilon`. Since `B(Y)=D(Y)=0` and `T(Y)=m`,

```
0<=B(W)<=epsilon,    0<=D(W)<=epsilon,    m-T(W)<=epsilon.
```

The affine functions in these three bounds have coefficient infinity norm one. Substituting into (*) gives `||W-V||_1<=(184m+5)epsilon`, so

```
||Y-V||_1 <= (184m+6)epsilon.
```

Extracting the principal block cannot increase the entrywise norm, and multiplication by `m` gives the stated factor `A_m`. The first inclusion follows from `F subset Q intersect H_F` and the exact-face theorem. The lift statement follows by adding the three affine equations and composing the output projection. QED.

A convex outer approximation need not be symmetric. The projected matrix `P_Q` may consequently contain nonsymmetric matrices; this does not affect the distance estimate or the valid-inequality argument below.

## Corollary 2: fine LP approximations require exponentially many inequalities

Let `Q_m` be a polyhedron with

```
K_(2m) subset Q_m subset K_(2m) + epsilon_m U_1,
epsilon_m <= 1/A_m.
```

Then every LP extended formulation of `Q_m` has `2^(Omega(m))` inequalities. This conclusion is unconditional and permits arbitrary real coefficients and arbitrary auxiliary dimension.

**Proof.** Theorem 2 gives a polyhedron `P_Q` with a lift using no more inequalities than the lift of `Q_m`, satisfying

```
COR(m) subset P_Q subset COR(m)+U_1.
```

For any `a in {0,1}^m`, the matrix `M_a=2diag(a)-aa^T` has entrywise coefficient norm at most one. The inequality `<M_a,X><=1` is valid for `COR(m)`, since its slack at `xx^T` is `(1-a^T x)^2`. Therefore every `X in P_Q` satisfies

```
<M_a,X> <= 2.
```

In the notation of Braun, Fiorini, Pokutta, and Steurer, define

```
Q_corr = {X: <2diag(a)-aa^T,X><=1 for all a in {0,1}^m}.
```

Then `COR(m) subset P_Q subset 2Q_corr`. Theorem 6(i) of [*Approximation Limits of Linear Programs (Beyond Hierarchies)*, PDF p.18](https://www.bayesianestimation.org/paper/approxlp.pdf) states that every polyhedron in this sandwich has extension complexity `2^(Omega(m))`. Apply it with the fixed dilation factor two. QED.

Since `A_m=Theta(m^2)`, this excludes polynomial-size LP lifts with uniform additive entrywise l1 error of order `m^-2` with the displayed constant. This concerns finite approximations of the nonpolyhedral hull, so it is stronger than merely observing that no finite LP can represent the hull exactly.

The same statement can be written in terms of a uniform additive objective gap: for a compact convex outer set, `Q subset K+epsilon U_1` is equivalent to

```
h_Q(H)-h_K(H) <= epsilon for every H with ||H||_infinity<=1,
```

where `h` is the support function. This equivalence follows directly from separation and the duality of the entrywise l1 and coefficient infinity norms.

## Limitations and next steps

The fine-LP corollary uses an established robust nonnegative-rank lower bound. It does not prove an approximate SOCP or SDP lower bound: the correlation inequalities used in that particular sandwich admit a small SDP lift, as the cited source itself explains in Section 4.3. A different slack family, such as the pseudo-density construction underlying the unrestricted SDP lower bound, is needed for that extension.

The new mathematical content proposed here is the polynomial quantitative face stability and its transfer to the continuous unit-capacity rank-one flow hull. The supplied constants have not been optimized. The exact and approximate results are provisional with respect to novelty until a broader literature audit is complete.
