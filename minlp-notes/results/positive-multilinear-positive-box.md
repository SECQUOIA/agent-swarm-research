# Uniform multilinear gap bounds on fixed strictly positive boxes

Date: 2026-09-04. Status: full common-aspect proof, arbitrary-box extension, and constants independently audited; see `notes/review-positive-multilinear-fixed-positive-box.md`. The proof was developed jointly with the agent recording `notes/positive-box-independent-investigation.md`. Novelty remains subject to a dedicated literature screen.

## Result

The later [aspect-ratio-plus-two theorem](positive-multilinear-positive-box-sharp.md) proves the stronger bound `ρ+2` for every aspect ratio `ρ>1`, including four on `[1,2]^n`. The proof below is retained as an independently verified predecessor and a record of its separate low/high estimates.

Let f be any positive-coefficient multilinear polynomial on a box ∏ᵢ[ℓᵢ,rᵢ], where 0<ℓᵢ≤rᵢ. Put

\[
R=\max\left\{4,\max_i\frac{r_i}{\ell_i}\right\}.
\]

Then, at every point of the box,

\[
\operatorname{tbtgap}f(x)
\le\left(4R+6+\frac2R\right)\operatorname{chgap}f(x).
\tag{1}
\]

Dimension, degree, supports, positive coefficients, evaluation points, and variation among the individual coordinate intervals are unrestricted. In particular, on [1,2]ⁿ—and on every strictly positive box whose coordinate aspect ratios are at most four—the ratio is at most **45/2**.

The proof first establishes a common-aspect-ratio bound on [1,ρ]ⁿ. Put η=1−1/ρ and define

\[
K(\rho)=2(1+1/\rho)
+\max\left\{4(1+\rho),\frac8{\eta^3}\right\}.
\tag{2}
\]

The ratio on [1,ρ]ⁿ is at most K(ρ). Positive affine expansion then transfers the bound to arbitrary boxes with aspect ratios at most ρ. Using the ambient value R≥4 gives (1). No sharpness claim is made for these constants.

The product envelopes used in the proof are classical. Proposition 4.1 of Adams–Gupte–Xu explicitly gives the envelopes on [1,ρ]ᵈ, crediting Benson 2004 and Tawarmalani–Richard–Xiong 2013. The present assertion concerns the ratio for arbitrary positive sums of products. [Primary manuscript, printed page 22](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf).

## Exact local envelopes and two global distributions

Write each coordinate as xᵢ=1+(ρ−1)uᵢ, where uᵢ∈[0,1]. We round u to a binary vector Y and evaluate xᵢ=1+(ρ−1)Yᵢ. Every distribution considered preserves E Yᵢ=uᵢ.

For one monomial, with S=Σuᵢ, its convex envelope is φρ(S), where

\[
\phi_\rho(s)=\rho^{\lfloor s\rfloor}
[1+(\rho-1)(s-\lfloor s\rfloor)]
\]

is defined for all real s. This is the piecewise linear interpolation of ρᵏ at integer k. Its concave envelope is attained by common-threshold rounding Yᵢ=1[U≤uᵢ]. The same common-threshold law attains every positive monomial's concave envelope simultaneously.

Let I be independent Bernoulli rounding. Let O be endpoint-orientation rounding: draw one uniform U on [0,1], and independently for each coordinate choose, with equal probabilities, the success interval [0,uᵢ] or [1−uᵢ,1]. These are global distributions, defined without reference to a monomial.

For each monomial we will prove

\[
T\le a_\rho D_O+b_\rho D_I,\quad
a_\rho=2(1+1/\rho),\quad
b_\rho=\max\{4(1+\rho),8\eta^{-3}\},
\tag{3}
\]

where T is its termwise gap and D denotes its concave-envelope value minus its expectation under the stated law. Nonnegative affine terms have zero gap and can be omitted.

## Low and high coordinates

Put t=ρ−1 and α=1/ρ=1−η. Call coordinate i low if uᵢ≤1/2 and high otherwise. For a low coordinate put qᵢ=uᵢ; for a high coordinate put qᵢ=1−uᵢ. All q-values lie in [0,1/2]. Let h be the number of high coordinates in the monomial, and divide all its values and gaps by ρʰ for the rest of the local proof.

Let Q_L,Q_H be the sums of the low and high q-values. For s∈[0,1/2], let L(s),H(s) count low and high q-values at least s. All integrals below are over this interval. Define

\[
\begin{aligned}
C_L&=1+\int(\rho^{L(s)}-1)\,ds,
&P_L&=\prod_{\rm low}(1+tq_i),\\
C_H&=1+\int(\alpha^{H(s)}-1)\,ds,
&P_H&=\prod_{\rm high}(1-\eta q_i).
\end{aligned}
\]

Empty products and empty-group C-values equal one. Low successes and high failures occupy opposite ends of the common-threshold interval. Hence the normalized local concave value is C=C_L+C_H−1, while independent rounding has value P_LP_H. In particular,

\[
D_I=(C_L-P_L)+(C_H-P_H)+(P_L-1)(1-P_H).
\tag{4}
\]

All three terms are nonnegative. Denote the second term by D_IH and the last by J_I.

Set

\[
A=C_L-1-tQ_L,\qquad B=C_H-1+\eta Q_H.
\]

Both are nonnegative. Let q_L,q_H be the largest q-values in the two groups, setting either maximum to zero for an empty group. Then

\[
A\ge t^2(Q_L-q_L),\qquad
B\ge\eta^2(Q_H-q_H).
\tag{5}
\]

For the first inequality use (1+t)ᴸ−1−tL≥t²(L−1)₊. For the second, the integer function αᴴ−1+ηH is zero at H=1 and has increments η(1−αᴴ)≥η² for H≥1. Integrating gives (5).

## Orientation deficiency

Put b_L(s)=(1+t/2)^{L(s)} and b_H(s)=(1−η/2)^{H(s)}. Direct conditioning on U gives

\[
O=1+2\int(b_Lb_H-1),
\]

and therefore

\[
D_O=D_{OL}+D_{OH}+J_O,
\qquad J_O=2\int(b_L-1)(1-b_H),
\]

where D_OL and D_OH are the two separate-group orientation deficiencies. They are nonnegative. Moreover,

\[
D_O\ge\frac A2+J_O,
\qquad J_O\ge\frac{t\eta}{2}\min(q_L,q_H).
\tag{6}
\]

The first estimate follows by expanding powers:

\[
(1+t)^L-2(1+t/2)^L+1
\ge\tfrac12[(1+t)^L-1-tL].
\]

Every degree-j coefficient, j≥2, is multiplied on the left by 1−2^{1−j}≥1/2. Nonnegativity for the separate high group follows from convexity of z↦zᴴ at the midpoint of α and one. For the second estimate in (6), throughout an interval of length min(q_L,q_H), both counts are at least one, so b_L−1≥t/2 and 1−b_H≥η/2.

## Two high-group estimates

If Q_H≤1, then

\[
D_{IH}\ge B/4.
\tag{7}
\]

To verify this, let q=q_H and R=Q_H−q. Bonferroni's inequality gives

\[
P_H\le1-\eta Q_H+\eta^2\sum_{i<j}q_iq_j.
\]

The pair sum is at most qR+R²/2. By (5), B≥η²R. Consequently

\[
D_{IH}\ge B-\eta^2(qR+R^2/2)
\ge(1-q-R/2)B\ge B/4,
\]

because q≤1/2 and q+R≤1. This also covers R=0 without division.

If Q_H≥1, then

\[
D_{IH}\ge\eta^3/8.
\tag{8}
\]

For a proof, sort the high q-values in decreasing order. The formula for C_H assigns geometrically decreasing weights to them. Subject to their sum Q_H and upper bound 1/2, C_H is minimized by filling initial coordinates to 1/2 and then using at most one remaining fractional coordinate. Convexity of the interpolation of αᵏ implies

\[
C_H\ge\frac12+\frac12\alpha^{2Q_H},\qquad
P_H\le e^{-\eta Q_H}.
\]

The function g(Q)=1/2+α^{2Q}/2−e^{−ηQ} is nondecreasing for Q≥1. Indeed, −lnα≤η/α, and α^{2Q−1}≤e^{−ηQ} for Q≥1, so

\[
g'(Q)\ge\eta[e^{-\eta Q}-\alpha^{2Q-1}]\ge0.
\]

Finally,

\[
g(1)=1-\eta+\eta^2/2-e^{-\eta}
\ge\eta^3/6-\eta^4/24\ge\eta^3/8.
\]

The first inequality follows from the fourth-order Taylor upper bound for e^{−η}; here 0<η<1. This proves (8).

## Combining the estimates

The normalized convex envelope is V=φρ(Q_L−Q_H), because shifting the argument of φρ by the integer h multiplies its value by ρʰ. The left and right slopes at zero are η and t. Hence

\[
V\ge1+\max\{t(Q_L-Q_H),\eta(Q_L-Q_H)\}.
\]

Since t−η=tη, this gives

\[
T=C-V\le A+B+t\eta\min(Q_L,Q_H).
\tag{9}
\]

First suppose Q_H≤1. Inequality (5) yields

\[
\min(Q_L,Q_H)
\le\min(q_L,q_H)+A/t^2+B/\eta^2.
\]

Using (6), (7), and t/η=ρ, equation (9) implies

\[
\begin{aligned}
T&\le(1+1/\rho)A+(1+\rho)B+2J_O\\
&\le2(1+1/\rho)D_O+4(1+\rho)D_I.
\end{aligned}
\tag{10}
\]

Now suppose Q_H≥1. Since C_H≤1 and V≥0, T≤C_L=1+A+tQ_L. Also P_L−1≥tQ_L and P_H≤e^{−ηQ_H}, so

\[
J_I\ge tQ_L(1-e^{-\eta})\ge(t\eta/2)Q_L.
\]

Here 1−e^{−η}≥η/2 for 0<η<1. Apply (6) and (8) to obtain

\[
T\le2D_O+8\eta^{-3}D_{IH}+2\eta^{-1}J_I
\le2D_O+8\eta^{-3}D_I.
\tag{11}
\]

Equations (10) and (11) prove (3) in every case. No division by a gap is used, so zero gaps and boundary marginals are included.

## Summing the monomials

Choose O with probability aρ/(aρ+bρ) and I with probability bρ/(aρ+bρ). This one global law preserves all coordinate marginals. Undo each monomial's positive normalization ρʰ and multiply its inequality by its positive coefficient. Summing (3) shows that this law has full-polynomial deficiency at least tbtgap f/K(ρ).

Common-threshold rounding attains the full concave envelope, and minimizing over all binary distributions gives the full convex envelope. The hull gap is therefore at least the deficiency of the chosen law. This proves the common-aspect-ratio bound (2). In particular, using ρ=2 directly gives 67; the positive expansion below improves this to 45/2.

## Arbitrary positive boxes and the 45/2 bound

Remove coordinates with zero-width intervals, absorbing their fixed positive values into coefficients. For each remaining original coordinate zᵢ∈[ℓᵢ,rᵢ], choose an ambient R≥rᵢ/ℓᵢ and set

\[
s_i=\frac{r_i/\ell_i-1}{R-1}\in(0,1],\qquad
z_i=\ell_i[(1-s_i)+s_i x_i],\qquad x_i\in[1,R].
\]

This affine bijection maps the ambient box onto the original box. Every original positive monomial expands into positive monomials in the physical variables xᵢ; terms with a zero coefficient can be discarded. The full polynomial's graph-hull gap is invariant under this coordinate change.

For each original monomial, its concave envelope after expansion is at most the sum of the expanded monomials' concave envelopes, and its convex envelope is at least the sum of their convex envelopes. Hence the original termwise gap is at most the expanded termwise gap. Summing over original monomials and applying (2) to the expanded positive polynomial proves the same K(R) bound for the original box. This is a positive-expansion argument, not an inference from box inclusion alone.

Now take R=max{4,maxᵢ rᵢ/ℓᵢ}. Since η=1−1/R≥3/4,

\[
8\eta^{-3}\le\frac{512}{27}<20\le4(1+R).
\]

Thus K(R)=4R+6+2/R, proving (1). At R=4 this is 45/2. For example, the transfer from [1,2] to the ambient [1,4] uses z=(2+x)/3 coordinatewise and positive expansion of each physical monomial.

## A sharper constant from the same proof

The proof of (8) actually gives D_IH≥gρ, where

\[
g_\rho=1-\eta+\eta^2/2-e^{-\eta}>0.
\]

Because gρ≤1−e^{−η}, the same large-Q_H argument works with 1/gρ in place of 8η⁻³. Thus the stronger explicit bound

\[
2(1+1/\rho)+\max\{4(1+\rho),1/g_\rho\}
\]

also follows. The simpler expression (2) is enough for the 45/2 bound above. The asymptotic order of the best bound as ρ grows remains unresolved here; these formulas are O(ρ).
