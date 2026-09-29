# Independent review: a strict three-vertex indicator moment gap

Date: 2026-09-25.

## Verdict and scope

The claimed gap is correct for unrestricted real continuous variables with binary on/off indicators. The relaxation optimum is exactly (3/2), while the closed convex hull epigraph value is exactly (1+1/\sqrt3), at

\[
 x=(0,1,0),\qquad z=(1,1/2,1/2).
\]

The strict difference is (1/\sqrt3-1/2>0). Both optima are attained. The result concerns the stated shared first-and-second-moment formulation. It does not prove that every compact formulation for indicator quadratics on trees fails, or that polynomial-size exact formulations cannot exist.

This review independently derives the relaxation lower bound, the hull formula, and a full-space valid affine inequality certifying the hull lower bound. It also checks an explicit convex combination attaining the hull value. No literature search or novelty assessment was performed in this proof review.

## Set and relaxation being reviewed

Let

\[
 Q=\begin{pmatrix}3&1&1\\1&1&0\\1&0&1\end{pmatrix},\qquad
 K=\{(x,z,t):x\in\mathbb R^3,\ z\in\{0,1\}^3,
 \ x_j=0\text{ if }z_j=0,\ t\ge x^\top Qx\}.
\]

The leading principal minors of (Q) are (3,2,1), so (Q\succ0). Its interaction graph is the two-edge star with center 0. Fix (z_0=1), (x_0=0), (x_1=1), (x_2=0), and (z_1=z_2=1/2).

The proposed relaxation uses

\[
 M=\begin{pmatrix}1&0\\0&r\end{pmatrix},\qquad
 M_i=\begin{pmatrix}1/2&s_i\\s_i&r_i\end{pmatrix},\qquad
 0\preceq M_i\preceq M\quad(i=1,2),
\]

and minimizes

\[
 L=3r+2(1+s_1)^2+2s_2^2-r_1-r_2.
\]

These constraints give a valid lower relaxation. For a distribution over original feasible points, write (Y=X_0), (A_i=\{Z_i=1\}), (r=\mathbb E Y^2), (s_i=\mathbb E[Y1_{A_i}]), and (r_i=\mathbb E[Y^2 1_{A_i}]). The matrices are the total and selected moment matrices, so both (M_i\succeq0) and (M-M_i\succeq0) hold. Moreover,

\[
 X^\top QX=3Y^2+\sum_{i=1}^2
 \bigl((X_i+Y)^2-Y^2\bigr)1_{A_i}.
\]

Conditional Cauchy--Schwarz gives

\[
 \mathbb E[(X_i+Y)^2 1_{A_i}]
 \ge \frac{(x_i+s_i)^2}{z_i}.
\]

Thus the expression being optimized is valid; the gap is not caused by an incorrect square completion or indicator placement.

## Exact relaxation optimum

The two matrix inequalities imply

\[
 r_i\ge2s_i^2,\qquad r-r_i\ge2s_i^2,
 \qquad r\ge4s_i^2.
\]

Consequently,

\[
\begin{aligned}
 L&\ge r+2+4s_1+4s_1^2+4s_2^2\\
  &\ge\frac32+8(s_1+1/4)^2+4s_2^2
  \ge\frac32.
\end{aligned}
\]

An exact nonnegative-slack identity is

\[
\begin{aligned}
 L-\frac32={}&(r-2s_1^2-r_1)+(r-2s_2^2-r_2)
 +(r-4s_1^2)\\
 &+8(s_1+1/4)^2+4s_2^2.
\end{aligned}
\]

Equality is attained at

\[
 r=1/4,\quad
 M_1=\begin{pmatrix}1/2&-1/4\\-1/4&1/8\end{pmatrix},
 \quad
 M_2=\begin{pmatrix}1/2&0\\0&1/4\end{pmatrix}.
\]

Here (M_1) and (M-M_1) have determinant zero and positive diagonal entries; (M_2) and (M-M_2=\operatorname{diag}(1/2,0)) are positive semidefinite. Substitution gives (L=3/2).

## Hull lower bound valid even after taking closure

Put (a=1/\sqrt3) and (u=(1,1+a,0)^\top). For a binary support (S\subseteq\{0,1,2\}), let (H_S) be the inverse of the principal matrix (Q_{SS}), embedded into a (3\times3) matrix with zeros outside (S\times S); put (H_\varnothing=0).

For every (x) supported on (S), completing the square gives

\[
 x^\top Qx\ge2u^\top x-u^\top H_Su.
\]

The four center-active supports give the following exact values:

| ((z_1,z_2)) | (u^\top H_Su) |
|---|---:|
| ((0,0)) | (1/3) |
| ((1,0)) | (3/2+2a) |
| ((0,1)) | (1/2) |
| ((1,1)) | (5/3+2a) |

These values equal (1/3+(7/6+2a)z_1+z_2/6). When (z_0=0), the value is ((4/3+2a)z_1), since the two leaf coordinates have diagonal quadratic form. It follows for all eight supports that

\[
 u^\top H_Su\le
 \frac{1+z_0+z_2}{6}+\left(\frac76+2a\right)z_1.
\]

Indeed, for (z_0=0), the difference between the right and left sides is ((1+z_2-z_1)/6\ge0); for (z_0=1), it is zero. Therefore the affine inequality

\[
 \boxed{\quad t\ge
 2x_0+2(1+a)x_1-
 \frac{1+z_0+z_2}{6}
 -\left(\frac76+2a\right)z_1 \quad}
\]

is valid for (K), and hence for its closed convex hull. At the reviewed point it gives (t\ge1+a). This full-space inequality directly rules out a closure loophole involving sequences with (z_0\uparrow1).

## Attaining the hull lower bound

Let (b=\sqrt3). Use the following four original feasible points, all with (z_0=1), and choose their epigraph coordinates equal to their respective quadratic costs:

| Leaf indicator pattern | Probability | Continuous point ((X_0,X_1,X_2)) |
|---|---:|---|
| ((0,0)) | (b-3/2) | ((1/3,0,0)) |
| ((1,0)) | (2-b) | ((-b/6,1+b/2,0)) |
| ((0,1)) | (2-b) | ((1/2,0,-1/2)) |
| ((1,1)) | (b-3/2) | ((-b/3,1+2b/3,b/3)) |

All probabilities are positive and sum to one. Their continuous mean is ((0,1,0)), and each leaf indicator has mean (1/2). The quadratic costs are, in table order,

\[
 \frac13,\quad \frac32+\frac{2b}{3},\quad
 \frac12,\quad\frac53+\frac{2b}{3}.
\]

Their weighted mean is (1+b/3=1+a). Hence the lower bound is attained already in the ordinary convex hull. Together with the preceding valid inequality, this proves the stated closed convex hull value independently of the one-parameter calculation below.

## Review of the proposed one-parameter hull derivation

At the fixed leaf marginals, pattern probabilities must have the form

\[
 p_{00}=p_{11}=p,\qquad p_{10}=p_{01}=1/2-p,
 \qquad0\le p\le1/2.
\]

For fixed probabilities \(\lambda_S\), group all points with the same support and apply Jensen's inequality to the positive definite quadratic. The minimum expected cost with mean (x) is

\[
 \min\left\{\sum_{S:\lambda_S>0}
 \frac{v_S^\top Qv_S}{\lambda_S}:
 \sum_Sv_S=x,\ \operatorname{supp}(v_S)\subseteq S,
 \ v_S=0\text{ if }\lambda_S=0\right\}
 =x^\top\left(\sum_S\lambda_SH_S\right)^{-1}x.
\]

The equality follows by completing squares; with (W=\sum_S\lambda_SH_S\), the optimizer is (v_S=\lambda_SH_SW^{-1}x). On the present interval, (W\succ0): the supports with positive probability cover every coordinate, and each selected principal inverse is positive definite on its support.

Direct calculation gives exactly the proposed matrix

\[
 W(p)=\begin{pmatrix}
 p/3+1/2&-p/2-1/4&-p/2-1/4\\
 -p/2-1/4&p/2+3/4&p\\
 -p/2-1/4&p&p/2+3/4
 \end{pmatrix}.
\]

Its determinant is (-(2p-3)(2p+1)/16>0) on ([0,1/2]), and

\[
 f(p)=x^\top W(p)^{-1}x
 =\frac{4p^2-12p-15}{3(2p-3)(2p+1)}.
\]

Its derivative is

\[
 f'(p)=\frac{8(4p^2+12p-3)}
 {3(2p-3)^2(2p+1)^2}.
\]

The numerator polynomial is strictly increasing on ([0,1/2]), has its only zero there at (p=\sqrt3-3/2), and changes from negative to positive. Therefore this is the unique global minimizing probability, with (f(p)=1+1/\sqrt3). Both endpoints have value (5/3).

For completeness, the perspective representation does not conceal a nonclosed projection here. If (m>0) is the smallest eigenvalue of (Q), a bounded epigraph cost (T) implies

\[
 \|v_S\|^2\le \lambda_ST/m.
\]

Thus weighted means stay bounded and vanish when their weights tend to zero. The simplex of probabilities is compact, and quadratic perspectives are lower semicontinuous with the zero-weight convention above. Taking subsequences proves closedness of the projected epigraph. Alternatively, the explicit full-space lower inequality and attaining combination already settle closure at the point of interest.

## Why the shared moments fail

The relaxation optimizer cannot arise from one common distribution of the center variable. For the first leaf, the conditional center means are (-1/2) and (1/2), and the corresponding conditional second moments are both (1/4). Thus both conditional variances vanish, forcing the unconditional center distribution to put probability (1/2) at each of (-1/2,1/2).

For the second leaf, the inactive selected complement has moment matrix (M-M_2=\operatorname{diag}(1/2,0)). It requires probability at least (1/2) at center value zero. These requirements are incompatible. Each edge admits a separate measure with the prescribed center first and second moments; there is no common center measure realizing both edges.

This observation diagnoses the source of the failure. On its own, incompatibility of one lifted point would not prove a gap in the original coordinates. The two exact optimum calculations above provide that stronger conclusion.

## Assumptions and limitations

- The attaining combination uses negative continuous coordinates. If a model additionally requires nonnegative variables or finite bounds, its hull must be analyzed separately. The proof above asserts the exact value only for the explicitly defined free-variable set (K).
- The counterexample rules out exactness of the stated moment relaxation even on a three-vertex tree and with a positive definite objective. It does not establish complexity hardness or exclude richer formulations.
- The affine inequality is a separation certificate for this instance. No general algorithm or practical performance claim follows from this example alone.
- This review makes no originality claim. Comparisons with existing indicator-quadratic and moment-consistency formulations require separate literature review.

## Targeted verification

Run:

```text
python research-20260925/verify_tree_indicator_moment_gap.py
```

Result: passed, printing `PASS: exact support cut, W(p), hull witness, PSD witness, and relaxation certificate`.

The script uses exact SymPy arithmetic to check the support inverses and full-space cut on all eight binary patterns, the matrix and derivative formulas, the four-point hull witness, all four PSD constraints at the relaxation witness, and the relaxation's nonnegative-slack identity. It does not establish literature novelty, formalize the probability/closure argument in Lean, or test broader solver consequences. No project-wide verification or CI inspection was performed.
