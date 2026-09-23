# Sequential range compression closes the real PSD one-channel residue

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the proof; priority not established

## Result

Let

\[
                         M=(S^{s-1})^b,
             \qquad s\geq3,\quad b\geq1.
\]

Suppose the full labelled product-ball slack has a finite globally
bi-\(C^1\) real-PSD factorization

\[
  1-x_d^Tz=\sum_{i=1}^L
       \operatorname {tr}\bigl(X_i(x)Y_i^d(z)\bigr),
 \quad
 X_i(x),Y_i^d(z)\in\mathbb S_+^{r_i},
 \quad r_i\leq s,                                      \tag{1}
\]

for every \(x\in M\), \(d\in[b]\), and \(z\in S^{s-1}\).  Then there is a
simultaneous contact \(u=(u_1,\ldots,u_b)\in M\) such that

\[
 \boxed{
   \sum_{i=1}^L\dim\left(
       \sum_{d=1}^b\operatorname {Ran}Y_i^d(u_d)
                         \right)\geq2b.}                 \tag{2}
\]

Diagonal complementarity puts the inner subspace in \(\ker X_i(u)\).
Consequently

\[
             \boxed{\sum_i\operatorname {nullity}X_i(u)\geq2b.}       \tag{3}
\]

This closes the remaining real-PSD one-channel case \(q=1,s=R\geq3\)
without assuming that a saturated row or label persists.  Source and label
switching cannot evade (2), because ranges already forced into the primal
kernels may be quotiented out before the next source row is processed.

If the selected tuple belongs to the closure of a strictly feasible affine
slice carrying the restricted standard product log-determinant, the usual
determinant vanishing-order argument gives

\[
                         \nu_{\rm std,slice}\geq2b.       \tag{4}
\]

The grouped Schur lift uses two coordinate groups per source and attains
\(2b\).  Thus, within the globally bi-\(C^1\) standard-slice class,

\[
       \boxed{\nu_{\rm std,slice}^{\min}=2b
                 \qquad(s=R\geq3).}                     \tag{5}
\]

Equation (2) is the stronger statement: it is a factorization theorem and
does not require Slater regularity or a barrier.

## 1. The one-ball contact-range lemma

The induction uses the following local-to-global consequence of the
audited real sole-factor obstruction.

> **Lemma 1.**  Let \(s\geq3\), and suppose
> \[
>  1-u^Tv=\sum_{i=1}^N\operatorname {tr}(A_i(u)B_i(v)),
>  \qquad A_i,B_i:S^{s-1}\longrightarrow\mathbb S_+^{n_i},
>  \qquad n_i\leq s,                                    \tag{6}
> \]
> is globally bi-\(C^1\).  Then some \(v\in S^{s-1}\) satisfies
> \[
>                         \sum_i\operatorname {rank}B_i(v)\geq2.      \tag{7}
> \]

Suppose instead that the rank sum in (7) is at most one everywhere.  It
cannot be zero: evaluating (6) at \(u=-v\) shows that at least one
\(B_i(v)\) is nonzero.  Hence the rank sum is exactly one for every \(v\).
The nonzero loci

\[
                       O_i=\{v:B_i(v)\ne0\}               \tag{8}
\]

are pairwise disjoint open sets that cover the connected sphere.  Each is
also closed, because its complement is the union of the other \(O_j\).
Thus exactly one label, say \(i_*\), is nonzero globally; it has rank one,
and every other dual factor vanishes identically.

At diagonal contact, positivity gives
\(A_{i_*}(u)B_{i_*}(u)=0\).  The mixed contact Hessian of (6) is the
rank-\((s-1)\) sphere metric.  The standard PSD cross-block rank bound gives

\[
 s-1\leq\operatorname {rank}A_{i_*}(u)
                \operatorname {rank}B_{i_*}(u)
       =\operatorname {rank}A_{i_*}(u)\leq n_{i_*}-1\leq s-1.        \tag{9}
\]

Equality holds throughout: \(n_{i_*}=s\), the complementary ranks are
\((s-1,1)\), and the rank-one support phase
\(S^{s-1}\to\mathbb{RP}^{s-1}\) is a local diffeomorphism.  Hence it is
the universal double cover.  This is exactly the real sole-factor equality
excluded by the independently audited even-quadratic theorem: the full
slack and absence of residual terms force the rank-\((s-1)\) sheet to be
an affine PSD pencil; differentiating its homogenized determinant recovers
the sphere coordinate as an even quadratic function of a kernel-vector
lift, contradicting the two sheets of the cover.  This contradiction
proves Lemma 1.

The use of the full slack in Lemma 1 is essential.  The projective kernel
\(\tfrac12(1-(u^Tv)^2)\) does have a single order-\(s\) rank-one dual
factor; it is the missing orientation term in \(1-u^Tv\) that rules out
(6) with only one contact-range dimension.

## 2. Quotienting previously fixed contact ranges

We choose \(u_1,\ldots,u_b\) successively.  Suppose
\(u_1,\ldots,u_{d-1}\) have been chosen and define, in each PSD block,

\[
 W_i^{d-1}=\sum_{e<d}\operatorname {Ran}Y_i^e(u_e),
 \qquad
 P_i^{d-1}=\text{orthogonal projection onto }(W_i^{d-1})^\perp.       \tag{10}
\]

Fix arbitrary values of the as-yet unchosen primal coordinates.  For a
variable \(u\in S^{s-1}\), write

\[
 x^{(d)}(u)=(u_1,\ldots,u_{d-1},u,
                  \bar u_{d+1},\ldots,\bar u_b).          \tag{11}
\]

For every \(e<d\), row-\(e\) diagonal contact and nonnegativity of the PSD
summands give

\[
 X_i(x^{(d)}(u))Y_i^e(u_e)=0
 \quad\text{for every }i\text{ and every }u.              \tag{12}
\]

Thus \(W_i^{d-1}\subseteq\ker X_i(x^{(d)}(u))\).  In the orthogonal
decomposition \(W_i^{d-1}\oplus(W_i^{d-1})^\perp\), set

\[
 \begin{aligned}
 A_i^{(d)}(u)
   &=X_i(x^{(d)}(u))|_{(W_i^{d-1})^\perp},\\
 B_i^{(d)}(v)
   &=(P_i^{d-1}Y_i^d(v)P_i^{d-1})|_{(W_i^{d-1})^\perp}.
 \end{aligned}                                           \tag{13}
\]

These are globally \(C^1\), positive semidefinite, and have orders at most
\(s\).  Because (12) makes \(X_i= P_i^{d-1}X_iP_i^{d-1}\) on the slice,
cyclicity of trace shows that (1) becomes the exact one-ball factorization

\[
        1-u^Tv=\sum_i\operatorname {tr}
                    \bigl(A_i^{(d)}(u)B_i^{(d)}(v)\bigr). \tag{14}
\]

Lemma 1 therefore supplies a choice \(u_d\) with

\[
                       \sum_i\operatorname {rank}B_i^{(d)}(u_d)\geq2.
                                                               \tag{15}
\]

## 3. Every row adds two new kernel dimensions

Update

\[
 W_i^d=W_i^{d-1}+\operatorname {Ran}Y_i^d(u_d).           \tag{16}
\]

For a positive-semidefinite matrix \(Y=CC^T\) and an orthogonal projection
\(P=P_{W^\perp}\),

\[
 \begin{aligned}
 \operatorname {rank}(PYP)
   &=\operatorname {rank}(PC)
     =\dim P(\operatorname {Ran}Y)\\
   &=\dim(W+\operatorname {Ran}Y)-\dim W.                 \tag{17}
 \end{aligned}
\]

Applying (17) blockwise to (13), (15), and (16) gives

\[
          \sum_i\bigl(\dim W_i^d-\dim W_i^{d-1}\bigr)
             =\sum_i\operatorname {rank}B_i^{(d)}(u_d)
             \geq2.                                      \tag{18}
\]

Starting from \(W_i^0=0\), induction yields

\[
                            \sum_i\dim W_i^b\geq2b.       \tag{19}
\]

At the final simultaneous contact \(u=(u_1,\ldots,u_b)\), diagonal
complementarity for every row gives

\[
      W_i^b=\sum_d\operatorname {Ran}Y_i^d(u_d)
                         \subseteq\ker X_i(u).            \tag{20}
\]

Equations (19)--(20) prove (2)--(3).  Notice that future coordinates may be
changed after a row is processed: (12) holds for *all* remaining-coordinate
values, so every previously accumulated range remains in the kernel.

## 4. Consequences and scope

The proof does not stratify saturated-row sets and never selects a global
row-to-label matching.  It shows why such a matching is unnecessary.
Label switching can occur only inside the quotient left after earlier
contact ranges are removed, and Lemma 1 forces the next row to add at least
two new quotient dimensions regardless of that switching.

The factorization theorem needs finite global labelling and bi-\(C^1\)
regularity only through Lemma 1's real sole-factor exclusion.  The
compression and dimension induction themselves use continuity and PSD
positivity.  The order cap \(r_i\leq s\) is essential: with an order-
\((s+1)\) block, the ordinary Schur lift represents one ball with one
contact-range dimension.

For genuine finite affine PSD lifts, the later
[intrinsic certificate-fiber theorem](2026-09-04-affine-psd-sequential-compression-without-selections.md)
removes global selections entirely.  It compresses the compact convex
fibers of original row-support certificates, proves that every positive
weighted aggregate has rank at least \(2b\), and forces nullity at least
\(2b\) in every final lift fiber.  Thus the present smooth-factorization
statement remains useful for abstract factorizations, while its affine-lift
and standard-logdet conclusions are superseded by that stronger theorem.

The barrier equality (5) additionally assumes that the selected boundary
tuple is in the closure of the same Slater affine slice on which the
standard product log-determinant is restricted.  It says nothing about an
arbitrary coupled or custom barrier and is not an IPM/QIPM iteration lower
bound.  Its QIPM relevance is formulation-specific but exact: within this
standard capped-PSD dictionary, cross-source switching cannot lower the
restricted barrier quantity below the grouped-Schur value.

The sole-factor obstruction is proved in
[the Hermitian standard-slice frontier](2026-09-04-hermitian-psd-standard-slice-barrier-frontier.md#an-even-quadratic-obstruction-for-real-order-rgeq3),
with the order-three case independently expanded in
[the PSD3 saturation exclusion](2026-09-04-psd3-saturation-exclusion.md).
The private-dimension reduction and the formerly open \(q=1\) interval are
recorded in
[the private-curvature frontier](2026-09-04-psd-product-ball-private-curvature-frontier.md)
and
[the divisible top-class note](2026-09-04-psd-product-ball-divisible-topclass.md).

A targeted primary-source screen found a close methodological antecedent:
Theorem 2.10 of Fawzi, Gouveia, Parrilo, Robinson, and Thomas,
“Positive Semidefinite Rank”
([arXiv](https://arxiv.org/abs/1407.4095),
[publisher](https://doi.org/10.1007/s10107-015-0922-1)), proves the
block-triangular PSD-rank inequality by spanning ranges forced by a zero
block and compressing the remaining factors to the orthogonal complement.
Thus range compression is not new in isolation. No source was located for
the smooth **sequential contact selection** used here: each cylindrical
ball row is processed after quotienting previously chosen contact ranges,
and the one-ball full-slack obstruction forces two new dimensions at every
stage, yielding one simultaneous contact with the sharp \(2b\)
range/nullity. That product-ball factorization conclusion remains a
candidate derived theorem under its global labelling and bi-\(C^1\)
hypotheses; priority is not established.

## Independent hostile audit

The audit checked that rank sum at most one makes the nonzero dual label a
clopen choice on the connected sphere, so one fixed rank-one label carries
the entire one-ball slack.  Full mixed curvature then forces order exactly
\(s\) and complementary ranks \((s-1,1)\), matching the hypotheses of the
audited real sole-factor even-quadratic exclusion.

For the induction, every earlier contact range remains in the primal
kernel under all later-coordinate variations.  Orthogonal compression
therefore preserves the exact trace identity, global bi-\(C^1\) regularity,
positivity, and the order cap.  For arbitrary singular PSD \(Y=CC^T\),
\[
 \operatorname {rank}(PYP)=\operatorname {rank}(PC)
 =\dim(W+\operatorname {Ran}Y)-\dim W,
\]
so each application of the one-ball lemma adds at least two genuinely new
range dimensions.  Later coordinate choices cannot undo those fixed dual
ranges, and final simultaneous complementarity puts their direct blockwise
sums in the primal kernels.  The factorization conclusion (2)--(3) is
independent of Slater regularity; only the barrier consequence (4)--(5)
uses the common affine-slice closure.  No substantive correction was
needed.
