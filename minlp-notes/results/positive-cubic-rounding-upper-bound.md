# A 31/12 upper bound for positive cubic relaxation gaps

The [focused cubic paper and Lean package](../paper-cubic-gap/README.md)
collects the universal upper bound, fixed-mixture optimality, analytic lower
family, and exact finite witnesses. Its [coverage map](../paper-cubic-gap/formal/COVERAGE.md)
and [verification record](../paper-cubic-gap/formal/VERIFICATION.md) identify
the formal statements and completed checks.

Date: 2026-09-04. Status: full proof and fixed-mixture optimality independently audited; see `notes/review-positive-cubic-31-over-12.md`.

For every positive-coefficient multilinear polynomial f of degree at most three, on every finite nonnegative box,

\[
\operatorname{tbtgap}f(x)\le\frac{31}{12}\operatorname{chgap}f(x).
\]

The proof combines three distributions with the prescribed coordinate marginals. The same mixture works simultaneously for every bilinear and cubic monomial, independently of the coefficients and monomial supports. This improves the endpoint-orientation bound 8/3 documented in `positive-cubic-gap.md`.

## Reduction to binary distributions

First work on the unit cube and remove affine terms, which change neither gap. For a monomial with sorted coordinate marginals u≤v≤w, write

\[
T=u-\max(0,u+v+w-2)=\min(u,(1-v)+(1-w)).
\]

Zero-gap monomials need no estimate, since every deficiency is nonnegative. For a binary distribution with those marginals, its deficiency is u−E[X_1X_2X_3]. The concave envelope of a positive multilinear polynomial is the sum of its termwise concave envelopes, attained by the common-threshold coupling. Consequently it suffices to construct one distribution whose expected deficiency is at least 12T/31 for every monomial. Bilinear monomials are checked separately below.

## Three global distributions

Let O denote the endpoint-orientation distribution: draw U uniformly on [0,1], and independently for each coordinate choose with equal probability whether X_i is the indicator of [0,x_i] or [1−x_i,1]. Let I be independent Bernoulli rounding.

For B, classify coordinate i as low if x_i≤1/2 and high otherwise. Draw one common U uniformly on [0,1]. Set each low X_i=1[U≤x_i]. For each high coordinate, conditionally on U, independently set X_i=0 with probability 1/2 when U≤2(1−x_i), and with probability zero otherwise. Each failure probability is exactly 1−x_i, so every coordinate marginal is preserved.

Use the global mixture

\[
P=\frac{18}{31}O+\frac6{31}I+\frac7{31}B.
\tag{1}
\]

Write D_O,D_I,D_B for one monomial's deficiencies under the respective distributions.

## Cubic monomials with at least two low coordinates

Here u≤v≤1/2, so T=u. In O, an orientation of the second coordinate opposite to the first produces a deficiency of u, with probability 1/2. Thus D_O≥u/2. Also

\[
D_I=u(1-vw)\ge u/2.
\]

Since all deficiencies are nonnegative, (1) gives a deficiency of at least (18+6)u/(2·31)=12T/31.

## Cubic monomials with exactly one low coordinate

Put a=1−v and b=1−w, so a≥b≥0, and T=min(u,a+b). Direct integration gives

\[
\begin{aligned}
D_O&=\tfrac12\min(u,a)+\tfrac14\min(u,b),\\
D_B&=\tfrac12\min(u,2a)+\tfrac14\min(u,2b).
\end{aligned}
\]

The following elementary inequality supplies the result:

\[
18D_O+7D_B\ge12\min(u,a+b).
\tag{2}
\]

If u=0 it is immediate. Otherwise the cases are as follows.

- If a≤u/2, the left side is 16a+8b≥12(a+b).
- If b≥u/2, then D_O≥3u/8 and D_B=3u/4, so the left side is at least 12u.
- If b≤u/2≤a≤u, the left side is 9a+8b+7u/2. When a+b≤u, use 3a+4b≤7u/2 to obtain (2). When a+b≥u, use 9a+8b≥8u+a≥17u/2.
- If b≤u/2 and a≥u, the left side is 25u/2+8b≥12u.

The cases include their shared boundaries and exhaust a≥b≥0. Independence has nonnegative deficiency, so (1) and (2) imply the desired bound.

## Cubic monomials with no low coordinate

Here u>1/2. Put c=1−u, a=1−v and b=1−w, so 1/2>c≥a≥b≥0. Under B, the failure union has probability

\[
c+\frac a2+\frac b4,
\]

obtained by integrating conditional union probabilities 7/8, 3/4 and 1/2 over the nested intervals of lengths 2b, 2(a−b) and 2(c−a). Therefore

\[
D_O=D_B=\frac a2+\frac b4
\ge\frac38(a+b)\ge\frac38 T.
\]

Independence provides the stronger bound

\[
D_I=u(a+b-ab)\ge\frac7{16}T.
\tag{3}
\]

To verify it, set s=a+b≤1 and use ab≤s²/4. If s≤u, then D_I/T≥u(1−s/4)≥u(1−u/4)≥7/16. If s≥u, then D_I/T≥s−s²/4≥u−u²/4≥7/16. The functions used are increasing on the relevant unit intervals, and u≥1/2.

The mixture deficiency is thus at least

\[
\frac{25}{31}\frac38T+\frac6{31}\frac7{16}T
=\frac{12}{31}T.
\]

## Bilinear monomials and boxes

For sorted bilinear marginals u≤v, T=min(u,1−v) and D_O=T/2.

If both coordinates are low, T=u and D_I=u(1−v)≥T/2. If exactly one is low, D_B=min(u,2(1−v))/2≥T/2. If both are high, D_B=T/2 and D_I=uT≥T/2. In the three cases the mixture deficiency is at least 12T/31, 25T/62, and T/2, respectively. Hence bilinear terms satisfy the same uniform 12/31 bound.

For a general nonnegative box, remove zero-width coordinates and scale the remaining coordinates to [0,1]. Every positive monomial expands into positive unit-cube monomials of degree at most three. The original term-by-term gap is at most the expanded term-by-term gap: concave envelopes are subadditive and convex envelopes are superadditive under summation. The full graph-hull gap is unchanged by the affine coordinate transformation. Applying the unit-cube result to the positive expansion proves the stated bound.

## Optimality within this three-distribution family

The weights in (1) are optimal among all fixed mixtures of O, I and B for a uniform guarantee over every bilinear and cubic monomial. This does not assert that 31/12 is the true worst cubic ratio.

Write the arbitrary weights as w,r,v, respectively, with w+r+v=1. Three marginal configurations bound any uniform deficiency fraction α.

- A bilinear term with marginals (u,1/2), where 0<u≤1/2, has normalized deficiencies (1/2,1/2,0). Hence α≤1/2−v/2.
- For a cubic term with marginals (ε,1−ε²,1−ε²), let ε decrease to zero. Its normalized deficiencies converge to (3/8,0,3/4). Hence α≤3/8+3v/8−3r/8.
- For a cubic term with marginals (u,1−u/2,1−u/2), let u decrease to 1/2 through values above 1/2. Its normalized deficiencies converge to (3/8,7/16,3/8). Hence α≤3/8+r/16.

Take the weighted average of these three upper bounds with weights 3/31, 4/31 and 24/31. The coefficients of r and v cancel, giving α≤12/31. The mixture (1) attains this value by the preceding proof. A stronger uniform termwise guarantee using fixed mixtures therefore requires a different coupling or a broader mixture family. This does not rule out a coefficient-aware or nontermwise analysis of the same distributions.

## Scope and verification

The proof is algebraic and does not depend on a numerical search. As a supplementary check, `code/multilinear_ratio/verify_cubic_rounding_upper.py` directly integrates the actual distributions in exact rational arithmetic for 546 bilinear/cubic marginal tuples, including cube and classification boundaries. Its `.log` records a complete pass; this finite check is not the proof of the continuous claim. The search in `code/multilinear_ratio/cubic_rounding_mixture_search.py` motivated consideration of these distributions, but its sampled bounds are not used. Novelty of the improved constant remains subject to a literature check. The exact worst cubic ratio is still undetermined.
