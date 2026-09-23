# The one-block PSD product-ball lift has intrinsic barrier parameter \(b\)

Status: Proved; targeted literature screen complete; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High

## Result

Let \(W=[w_1\ \cdots\ w_b]\in\mathbb R^{s\times b}\), and consider the
relative-open affine PSD slice

\[
 \Omega_{s,b}:=\left\{(S,W)\in\mathbb S^b\times\mathbb R^{s\times b}:
 \operatorname{diag}S=\mathbf1,\quad
 \begin{pmatrix}S&W^T\\W&I_s\end{pmatrix}\succ0\right\}.       \tag{1}
\]

Equivalently, with

\[
                         D:=S-W^TW,
\]

the last condition is \(D\succ0\).  Let
\(\vartheta_{\rm opt}(\Omega_{s,b})\) be the infimum of the parameters of
all nondegenerate self-concordant barriers on this fixed slice.  The barrier
may couple every entry of \(S\) and \(W\); it need not be logarithmically
homogeneous, spectral, or separable.  Then, for every \(s,b\geq1\),

\[
                  \boxed{\vartheta_{\rm opt}(\Omega_{s,b})=b.}  \tag{2}
\]

The standard restricted PSD barrier already attains the optimum:

\[
 F_{\rm std}(S,W)
  =-\log\det\begin{pmatrix}S&W^T\\W&I_s\end{pmatrix}
  =-\log\det(S-W^TW).                                      \tag{3}
\]

Thus the order-\((s+b)\), one-factor column-packing lift of
\((B_2^s)^b\) has ambient PSD parameter \(s+b\), but its exact parameter
after affine restriction is \(b\), even when compared with arbitrary
coupled barriers on the slice.  This strengthens the earlier
standard-log-determinant statement.

The proof does not need \(b\leq s\).  In particular it covers \(b>s\), where
one cannot obtain the desired lower bound merely by placing all \(b\) columns
of \(W\) in mutually orthogonal directions of \(\mathbb R^s\).

## 1. A parameter-monotonicity lemma for bounded-fiber projections

The needed barrier-calculus fact is classical, but it is useful to isolate
its lower-bound consequence.

**Lemma 1 (bounded-fiber projection).**  Let \(\Omega\subset E\times H\) be
a relative-open convex domain, let \(C=\pi_E(\Omega)\), and suppose every
fiber

\[
                         \Omega_x:=\{y:(x,y)\in\Omega\}      \tag{4}
\]

is nonempty and bounded for \(x\in C\).  Assume affine hulls have been
eliminated, \(C\) contains no line, and \(F\) is a nondegenerate
\(\vartheta\)-self-concordant barrier on \(\Omega\).  Then

\[
                   \phi(x):=\min_{y\in\Omega_x}F(x,y)       \tag{5}
\]

is a nondegenerate \(\vartheta\)-self-concordant barrier on \(C\).
Consequently

\[
                         \vartheta_{\rm opt}(\Omega)
                  \geq \vartheta_{\rm opt}(C).             \tag{6}
\]

The minimum in (5) exists because the fiber is bounded and the barrier
diverges at its relative boundary; it is unique because the fiber Hessian is
positive definite.  For completeness, at the minimizer \(y(x)\), the first
order condition is \(F_y=0\).  For a direction \(h\), differentiating this
condition shows that \((h,y'(x)h)\) is the Hessian-minimizing lift:

\[
 D^2\phi(x)[h,h]
   =\min_k D^2F(x,y(x))[(h,k),(h,k)].                       \tag{7}
\]

The envelope identity gives

\[
                         D\phi(x)[h]=DF(x,y(x))[(h,k)]      \tag{8}
\]

for every feasible lift \(k\), and in particular for the minimizer in (7).
The gradient inequality for \(F\) therefore gives the same
\(\vartheta\)-gradient inequality for \(\phi\).  Along an affine line in
\(x\), differentiating (7) once makes the acceleration term vanish by the
Hessian orthogonality encoded in the differentiated stationarity condition.
Hence

\[
 D^3\phi(x)[h,h,h]
  =D^3F(x,y(x))[(h,y'(x)h)]^3,                              \tag{9}
\]

and the self-concordance inequality transfers using (7).  Smoothness follows
from the implicit-function theorem.  Barrier divergence and nondegeneracy
are part of the exact partial-minimization theorem under the hypotheses
above.

This is exactly Chares's Theorem 5.2.1, including linear equations whose
right-hand side depends on the retained variable.  The derivative display is
included to make clear that (6) does not reverse the projection inequality or
silently assume a separable barrier.

## 2. The PSD completion fibers are bounded

Projection of (1) onto \(W\) gives exactly

\[
                 C=\operatorname{int}(B_2^s)^b
                  =\{W:\|w_a\|_2<1\ (a\in[b])\}.          \tag{10}
\]

Indeed, \(D\succ0\) implies

\[
                         D_{aa}=1-\|w_a\|^2>0.             \tag{11}
\]

Conversely, for \(W\in C\), choosing

\[
 S=W^TW+\operatorname{Diag}(1-\|w_1\|^2,\ldots,
                                      1-\|w_b\|^2)         \tag{12}
\]

makes \(D\) positive diagonal.

For fixed \(W\), the change of variable \(S=D+W^TW\) identifies the fiber
with

\[
 \{D\in\mathbb S^b_{++}:D_{aa}=d_a:=1-\|w_a\|^2\}.        \tag{13}
\]

Positive semidefiniteness gives

\[
                         |D_{ac}|<\sqrt{d_ad_c}\leq1,       \tag{14}
\]

so every fiber is bounded.  After deleting the fixed diagonal entries of
\(S\), (1) is full-dimensional in its affine hull.  The target (10) is
bounded and contains no line.  Lemma 1 therefore applies to *every* coupled
self-concordant barrier on (1).

## 3. The projected product of balls has exact parameter \(b\)

The product barrier

\[
                         f_C(W)=-\sum_{a=1}^b
                                   \log(1-\|w_a\|^2)       \tag{15}
\]

is a \(b\)-self-concordant barrier.  For the reverse inequality, choose one
unit vector \(e_a\in\mathbb R^s\) for each source ball and restrict to

\[
                             w_a=t_ae_a.                   \tag{16}
\]

The intersection is the open \(b\)-cube \((-1,1)^b\), and every cube
boundary point used in the corner lower bound is a boundary point of the
product body.  Affine restriction and Nesterov--Nemirovskii's cube lower
bound give

\[
                         \vartheta_{\rm opt}(C)=b.          \tag{17}
\]

Now let \(F\) be any \(\vartheta\)-self-concordant barrier on (1).  Lemma 1
and (17) give \(\vartheta\geq b\).  On the other hand, (3) is a
\(b\)-self-concordant barrier: before imposing \(\operatorname{diag}S=1\),
the local gradient calculation for \(-\log\det(S-W^TW)\) gives squared dual
norm \(b\), and affine restriction cannot increase the parameter.  This
proves (2).

Notice the two different cube roles.  The cube proving (17) lives in the
*projected product of balls* and exists for every \(b,s\).  The lower bound is
then lifted back to (1) by parameter monotonicity under bounded-fiber
projection.  It is not necessary to exhibit a \(b\)-cube affine section of
the PSD completion variables, so there is no \(b\leq s\) restriction.

## 4. QIPM consequence and scope

For this fixed one-block formulation, replacing the standard restricted
log-determinant by a custom coupled self-concordant barrier cannot reduce
the barrier-parameter factor below \(\sqrt b\).  The standard short-step
guarantee is

\[
                     O\!\left(\sqrt b\log{\Delta\over\epsilon}\right). \tag{18}
\]

The standard barrier also has an explicit auxiliary center.  Partial
minimization over \(S\) sets

\[
                 D=\operatorname{Diag}(1-\|w_a\|^2)        \tag{19}
\]

and recovers (15), while the bordered exact Newton system has the forest
structure recorded in the PSD column-packing Newton note.  Thus an opaque
coupled barrier offers no parameter advantage and does not automatically
preserve the known sparse solve.

Equation (2) is a formulation-level barrier certificate, not a lower bound
on the actual number of iterations of every classical or quantum IPM.  It
does not cover non-self-concordant methods or rule out better long-step
behavior.  The projection lemma gives the universal floor \(b\) for any
bounded-fiber lift of the same product body, but it does not prove that a
particular small-order lift attains \(b\); the exact upper bound here uses the
specific one-block PSD barrier (3).

## Literature and novelty boundary

Exact partial minimization is established in Robert Chares,
*Cones and Interior-Point Algorithms for Structured Convex Optimization
Involving Powers and Exponentials* (PhD thesis, UCL, 2009), Theorem 5.2.1,
[open PDF](https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf).
Its assumptions explicitly include bounded fibers, and its conclusion
preserves the same self-concordant-barrier parameter.  Chares attributes a
more restricted precursor to Nesterov.

The cube lower bound is Proposition 2.3.6 of Nesterov and Nemirovskii,
*Interior-Point Polynomial Algorithms in Convex Programming* (SIAM, 1994),
[DOI 10.1137/1.9781611970791](https://doi.org/10.1137/1.9781611970791).
The ball barrier, affine restriction, and Schur-complement construction are
standard.

A targeted local and web search found the partial-minimization theorem and
general optimal-barrier results, but not the exact arbitrary-coupled value
for the one-block PSD completion slice (1), nor this use of projection
monotonicity to close the \(b>s\) case.  The potentially new contribution is
the exact synthesis (2) and its QIPM-facing comparison with the ambient PSD
parameter and sparse marginal Newton system.  Priority remains subject to
specialist review.

## Audit checklist

- [x] The domain is convex because (1) is an affine slice of a positive
  definite matrix cone.
- [x] Projection onto \(W\) is exactly the interior product of balls.
- [x] Every fixed-\(W\) completion fiber is nonempty and bounded.
- [x] Fixed diagonal entries are eliminated before invoking nondegeneracy.
- [x] Partial minimization preserves both self-concordance and the same
  gradient parameter.
- [x] The target cube has dimension \(b\) even when \(b>s\).
- [x] The lower and upper bounds use the same barrier normalization.
- [x] Independent hostile audit.

## Independent hostile audit

The auditor checked Chares's hypotheses after eliminating the fixed
diagonal of \(S\), including full dimensionality in the affine hull,
bounded completion fibers, nondegeneracy, smoothness of the minimizer, and
the direction of (6).  It independently verified (7)--(9), noting that the
vertical acceleration term in the third derivative vanishes by the
differentiated stationarity condition.

The audit also checked the construction for \(b>s\): the unit direction in
(16) belongs to a different product coordinate for each source ball and may
be reused, so no orthogonal family in \(\mathbb R^s\) is required.  Finally,
it recomputed the full-domain derivatives of (3).  After a shear sends the
base point to \((D,0)\),

\[
 dF[H,K]=-\operatorname{tr}(D^{-1}H),\qquad
 d^2F[(H,K)]^2=\operatorname{tr}(D^{-1}HD^{-1}H)
                    +2\operatorname{tr}(D^{-1}K^TK),       \tag{20}
\]

so the squared local dual norm is exactly \(b\) before affine restriction.
The only requested correction was to avoid describing the big-\(O\)
short-step guarantee (18) as a lower bound; that wording has been fixed.
