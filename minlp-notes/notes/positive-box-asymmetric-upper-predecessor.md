# Sharp leading-order gap growth with the box aspect ratio

Date: 2026-09-04. Status: full upper-bound proof passed two fresh independent audits: `notes/review-positive-box-sharp-aspect-upper.md` and `notes/review-positive-box-sharp-second.md`. The matching lower construction has its own independent audit.

## Result

Let C_box(ρ) be the supremum of the term-by-term/convex-hull gap ratio over positive multilinear polynomials on strictly positive boxes whose coordinate aspect ratios are at most ρ. Dimension, degree, supports, coefficients and evaluation point are unrestricted. Then

\[
C_{\rm box}(\rho)\sim\rho\qquad(\rho\to\infty).
\tag{1}
\]

More explicitly, the [positive-box lower construction](../results/positive-multilinear-positive-box-lower.md) and the proof below give, for ρ≥64,

\[
\max\{2,\rho\}\le C_{\rm box}(\rho)
\le2+\frac{\rho+1}{1-3/\sqrt\rho}
=\rho+3\sqrt\rho+O(1).
\tag{2}
\]

For every smaller fixed ρ>1, finiteness follows from the independently audited [positive-box bound](../results/positive-multilinear-positive-box.md), including the bound 45/2 whenever all aspect ratios are at most four. Formula (2) does not determine the exact finite-ρ optimum.

## Parameters and two global laws

First work on [1,ρ]ⁿ. Write physical coordinates as xᵢ=1+t uᵢ, where t=ρ−1 and uᵢ∈[0,1]. Put

\[
\eta=1-1/\rho,\qquad
\delta=\rho^{-1/2}\le1/8,\qquad
b=\frac{\rho+1}{1-3\delta}.
\]

Let I be independent Bernoulli rounding of u. Let O be fair endpoint-orientation rounding: choose one uniform U on [0,1], then independently for each coordinate choose its success interval as [0,uᵢ] or [1−uᵢ,1]. Both laws preserve every individual marginal.

We prove, for every physical monomial,

\[
T\le bD_I+2D_O,
\tag{3}
\]

where T is its exact termwise gap, and D denotes its concave value minus its expected value under the indicated law. The mixture choosing I with probability b/(b+2) and O with probability 2/(b+2) then proves the upper bound in (2) after summation.

## An asymmetric low/high split

Classify a coordinate as low if uᵢ≤1−δ and high otherwise. For high coordinates put qᵢ=1−uᵢ<δ. For low coordinates retain uᵢ itself. Divide all values of the monomial by ρʰ, where h is its number of high coordinates. The normalized binary product is

\[
\prod_{\rm low}(1+tY_i)
\prod_{\rm high}(1-\eta F_i),
\]

where Yᵢ is a low success indicator and Fᵢ is a high failure indicator.

Let Q_L=Σlow uᵢ and Q_H=Σhigh qᵢ. Let C_L,C_H be the common-threshold concave values of the separate products and let

\[
P_L=\prod_{\rm low}(1+tu_i),\qquad
P_H=\prod_{\rm high}(1-\eta q_i)
\]

be their independent values. Empty-group products and C-values equal one. Define

\[
A=C_L-1-tQ_L,\quad B=C_H-1+\eta Q_H,
\quad D_{IL}=C_L-P_L,\quad D_{IH}=C_H-P_H.
\]

Under common-threshold rounding, low successes lie before 1−δ and high failures lie after 1−δ. They never overlap, except at irrelevant interval endpoints. Thus the normalized concave value of the full monomial is C=C_L+C_H−1, and

\[
D_I=D_{IL}+D_{IH}+J_I,
\qquad J_I=(P_L-1)(1-P_H).
\tag{4}
\]

Every term on the right is nonnegative.

The normalized convex value is V=φρ(Q_L−Q_H), where φρ is the piecewise linear interpolation of ρᵏ at integer k. This follows from the classical exact product envelope and integer-shift scaling; see the linked coarse-bound proof and its primary source. The two supporting lines at zero have slopes t and η. Consequently

\[
T=C-V\le A+B+t\eta\min(Q_L,Q_H).
\tag{5}
\]

## Bounds on within-group dispersion

Let a_L=maxlow uᵢ and a_H=maxhigh qᵢ, with an empty maximum equal to zero. The same integer-count inequalities as in the coarse proof give

\[
A\ge t^2(Q_L-a_L),\qquad
B\ge\eta^2(Q_H-a_H).
\tag{6}
\]

These estimates do not require the low marginals to be at most 1/2. For the low group, expand (1+t)ᴸ−1−tL and use binom(L,2)≥(L−1)₊ before integrating the common-threshold count. For the high group, use αᴴ−1+ηH≥η²(H−1)₊, with α=1−η.

The asymmetric split supplies a different estimate for A:

\[
D_{IL}\ge\delta A.
\tag{7}
\]

Indeed, expand the low physical product into positive multilinear monomials in the normalized u-coordinates. Its concave value is the sum of the subset minima, while its independent value is the sum of the subset products. For every subset of degree at least two, its product is at most (1−δ) times its minimum marginal, because every other low marginal is at most 1−δ. The constant and affine subset terms cancel. Their remaining concave sum is exactly A, proving (7). This expansion is used only in the proof and need not be formed to sample either global law.

## The orientation cross term

We use only the nonnegativity of the separate-group orientation deficiencies. In particular, the symmetric-split estimate D_OL≥A/2 from the coarse proof is not used here.

Conditional on U=s or U=1−s, with 0≤s≤δ, each low variable has conditional physical expectation 1+(t/2)1[s≤uᵢ]. This follows from uᵢ≤1−δ: its two possible success intervals cover at most one of the two endpoints in question. Each high variable has conditional normalized expectation 1−(η/2)1[s≤qᵢ]. Outside these two end strips, the high conditional product equals one.

Conditional independence of the orientation choices therefore gives

\[
D_O=D_{OL}+D_{OH}+J_O\ge J_O,
\]

where

\[
J_O=2\int_0^\delta
\left(\prod_{\rm low}[1+(t/2)1\{s\le u_i\}]-1\right)
\left(1-\prod_{\rm high}[1-(\eta/2)1\{s\le q_i\}]\right)ds.
\]

Both bracketed factors are nonnegative. For an interval of length min(a_L,a_H), they are at least t/2 and η/2. Hence

\[
J_O\ge\frac{t\eta}{2}\min(a_L,a_H).
\tag{8}
\]

Combining (5), (6), and (8) yields

\[
T\le(1+1/\rho)A+(1+\rho)B+2J_O.
\tag{9}
\]

This is the cross-term estimate needed below.

## Small high-group failure mass

Suppose Q_H≤4δ. Let q=a_H and R=Q_H−q. Bonferroni's inequality and (6) imply

\[
\begin{aligned}
D_{IH}
&\ge B-\eta^2\sum_{i<j}q_iq_j\\
&\ge B-\eta^2(qR+R^2/2)\\
&\ge(1-q-R/2)B\ge(1-3\delta)B.
\end{aligned}
\tag{10}
\]

The final estimate uses q≤δ and R≤Q_H≤4δ. If R=0 the inequalities hold without division. From (7), (9), and (10),

\[
T\le\frac{1+1/\rho}{\delta}D_{IL}
+bD_{IH}+2D_O\le bD_I+2D_O.
\]

Here (1+1/ρ)/δ≤b for ρ≥64, and all components in (4) are nonnegative.

## Large high-group failure mass

Suppose Q_H≥4δ. Under common-threshold high failures, all failure events are confined to a set of probability a_H≤δ. Outside it the normalized high product equals one. Therefore

\[
C_H\ge1-\delta,\qquad
P_H\le e^{-\eta Q_H}\le e^{-4\eta\delta}\le1-2\delta.
\tag{11}
\]

For the final inequality, use e^{−z}≤1−z+z²/2 with z=4ηδ. Since η≥3/4 and δ≤1/8,

\[
4\eta-8\eta^2\delta\ge3-1=2.
\]

It follows that D_IH≥δ and 1−P_H≥2δ. Also P_L−1≥tQ_L, so J_I≥δtQ_L. Combine this with (7):

\[
D_I\ge\delta A+\delta+\delta tQ_L
=\delta C_L.
\]

Since C_H≤1 and V≥0, T≤C≤C_L. Thus T≤δ⁻¹D_I≤bD_I, proving (3) in this case as well.

## From local inequalities to the worst-case ratio

Undo each monomial's positive normalization and multiply (3) by its positive coefficient. The same I/O mixture applies to all terms. Common-threshold rounding attains the full concave envelope of a positive polynomial, so its hull gap is at least the summed deficiency under this mixture. This gives the upper bound b+2 on [1,ρ]ⁿ, including boundary and zero-gap cases.

For a box with smaller or unequal aspect ratios, the positive affine expansion from the coarse proof maps it bijectively from [1,ρ]ⁿ. The original termwise gap is at most the expanded termwise gap, and the full hull gap is invariant. The same bound therefore applies to every box in the definition of C_box(ρ).

The independently audited lower family has ratios tending to ρ for every fixed ρ>1. Combining that construction with b+2=ρ+3√ρ+O(1) proves (1). Neither argument claims that the exact finite-ρ constant is ρ or ρ+2.
