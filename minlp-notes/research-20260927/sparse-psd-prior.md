# Prior-art audit: sparse quadratic selection through PSD approximation

Date: 2026-09-27. Status: targeted literature audit, with a conditional
application derivation. This is not a novelty certificate or an independent
verification of the underlying PSD approximation-set algorithm.

The most promising claim now under consideration is a deterministic FPTAS
for maximizing

\[
g(S)=b_S^T(D_{SS}+U_SU_S^T)^{-1}b_S
\]

under one arbitrary nonnegative rational budget \(\sum_{i\in S}c_i\le C\),
optionally together with a cardinality bound. The number of columns of
\(U\) is fixed, \(D\) is positive diagonal, and input magnitudes and
condition numbers are unrestricted. The budget is to be satisfied exactly.
This is stronger and more interpretable than the original proposed
\(\epsilon B\) additive guarantee for minimizing
\(\lambda(S)-g(S)\), where \(B=\sum_i b_i^2/d_i\).

## 1. What is already in this repository

The proposed normalization and rounding mechanism is already developed in
[the September 12 DAG PSD approximation-set note](../notes/research-20260912-dag-psd-approximation-set.md).
It constructs, in polynomial bit time for fixed matrix dimension, feasible
path representatives satisfying

\[
(1-\eta)J(P)\preceq J(\widehat P)\preceq(1+\eta)J(P)
\]

for every feasible path. That note already handles singular ranges,
maximum-volume basis enumeration, rational normalization, owner forcing,
signed entry rounding, and common priors. Section 6 already includes
inverse-trace and contrast-variance objectives. Its references also already
discuss Brown–Laddha–Singh and Pareto dynamic programming. A
[represented-matroid extension](../notes/research-20260912-represented-matroid-psd-approximation-set.md)
also exists locally. These constructions must not be presented as new work
of September 27.

Replacing an arbitrary representative of a rounded DP state by its cheapest
representative is a small extension: future transitions add the same cost
to either representative. No new budget coordinate is needed. This is the
usual way to preserve one resource exactly while approximating other
quantities. The part worth documenting is its application to the Schur
complement expression for \(g\), its exact-budget consequence, and a precise
comparison against prior regression algorithms.

## 2. Algebraic scope of the application

Write \(u_i^T\) for row \(i\) of \(U\), and set

\[
K_S=\begin{pmatrix}I_r&0\\0&0\end{pmatrix}
 +\sum_{i\in S}\frac1{d_i}
 \begin{pmatrix}u_i\\b_i\end{pmatrix}
 \begin{pmatrix}u_i\\b_i\end{pmatrix}^{T}.
\]

If its blocks are \(K_S=\left(\begin{smallmatrix}H_S&h_S\\h_S^T&a_S\end{smallmatrix}\right)\),
Woodbury gives

\[
g(S)=a_S-h_S^TH_S^{-1}h_S
=\min_{z\in\mathbb R^r}(z,1)^TK_S(z,1).
\]

Consequently a two-sided relative PSD approximation of \(K_S\) gives the
same relative approximation of \(g(S)\), including \(g(S)=0\). If the
representative also costs no more than \(S\), a feasible optimum remains
represented within factor \(1-\eta\). This establishes the conditional
FPTAS deduction from the local PSD construction; it does not establish
priority for that deduction.

For penalties, \(0\le g(S)\le B\), so exact cost preservation and
\(g(\widehat S)\ge(1-\eta)g(S)\) imply additive error at most \(\eta B\).
Calling this a standard FPTAS is inappropriate without specifying the
nonstandard additive scale: \(\lambda(S)-g(S)\) can be negative or zero.

There is a separate relative minimization statement for genuine ridge least
squares. If \(b=Uy\), then

\[
\|y\|^2-g(S)
=y^T\left(I_r+\sum_{i\in S}u_iu_i^T/d_i\right)^{-1}y.
\]

Approximating this \(r\)-dimensional information matrix gives a relative
bound on residual-plus-ridge loss. Adding nonnegative activation costs
preserved from above gives a relative bound on the full positive objective.
This follows from the inverse-contrast consequence already in the local
note. The inverse formula itself is established sparse-ridge literature,
not a new identity.

The additive scale and relative residual scale differ materially. With
\(r=n=d_1=y=1\), \(u_1=b_1=M\), the full-support residual is
\(1/(1+M^2)\), whereas \(B=M^2\). An \(\epsilon B\) guarantee provides no
useful relative residual guarantee as \(M\) grows. Conversely, a relative
gain guarantee does not imply a relative residual guarantee when the
optimal gain nearly equals the response variance.

## 3. Closest external statements examined

### Das and Kempe: the same explained-variance objective

Das and Kempe, *Algorithms for Subset Selection in Linear Regression*,
STOC 2008, DOI `10.1145/1374376.1374384`,
[author PDF](https://david-kempe.com/publications/regression.pdf).
Sections 1–4 and Theorem 4.1 were examined. Their objective is the same
quadratic inverse gain, expressed as squared multiple correlation after
variance normalization. Theorem 4.1 gives an FPTAS for cardinality selection
with bounded covariance bandwidth; Section 4 assumes a polynomially bounded
condition number. Exact algorithms also cover tree covariance graphs and a
large known independent set. None of these structural assumptions is
implied by fixed rank of the dense off-diagonal factor \(UU^T\).

This is the strongest direct published FPTAS comparator found. The proposed
distinction is dense fixed-factor covariance, unrestricted conditioning,
and one exact binary-encoded budget. The search did not locate a theorem
already stating that combination. This absence does not prove novelty.

### Bienstock and Chen: the same Hessian class with indicators

Bienstock and Tongtong Chen, *Solving convex QPs with structured sparsity
under indicator conditions*, 2024,
[arXiv full text](https://arxiv.org/html/2411.11722v1).
Theorem 1.4 and Sections 2.1–2.2 were examined. Section 2.1 explicitly
uses PSD low rank plus diagonal covariance, introduces factor-link
equations, and applies bounded constraint-block treewidth. Theorem 1.4
returns a superoptimal solution satisfying combinatorial constraints while
allowing normalized mixed-integer constraint violations. Lemma 2.1 applies
this to sparse portfolios. Section 2.2 discusses repairing factor equations
and an additive objective guarantee for banded Hessians.

Their theorem is highly relevant; low rank plus diagonal tractability is
not an unexplored observation. It does not immediately state a relative
gain guarantee with exact arbitrary budget and bit complexity independent
of numerical conditioning. A reduction through approximate factor-link
equations needs a quantitative repair analysis; the read statements alone
do not settle whether such a reduction matches the proposed guarantee.

### Xie and Deng; Bertsimas and Van Parys: sparse ridge formulations

Xie and Deng, *Scalable Algorithms for the Sparse Ridge Regression*,
SIAM Journal on Optimization 30(4):3359–3386, 2020,
[open manuscript](https://optimization-online.org/wp-content/uploads/2018/06/6652.pdf),
studies cardinality-constrained squared loss plus positive ridge penalty.
Proposition 5 gives the binary inverse-information formulation, crediting
earlier work. Theorem 3's greedy ratio depends on data spectral quantities
and regularization. Theorem 5's randomized relative guarantee requires
sufficiently large regularization and permits a support-size excess of
\(\sqrt{3k\log(2/\alpha)}\), with failure probability \(\alpha\).
The source does not state a fixed-data-rank FPTAS with arbitrary positive
ridge strengths or feature costs.

Bertsimas and Van Parys, *Sparse High-Dimensional Regression: Exact Scalable
Algorithms and Phase Transitions*,
[2017 manuscript](https://arxiv.org/html/1709.10029), Section 2,
is a direct source for the convex binary inverse-information reformulation
and an exact cutting-plane algorithm. It does not supply the proposed
worst-case fixed-rank approximation complexity claim. These references
prevent presenting the ridge reduction or support elimination as new.

### Brown, Laddha, and Singh: fixed-dimensional spectral selection

Brown, Laddha, and Singh, *Fast algorithms for maximizing the minimum
eigenvalue in fixed dimension*, 2024,
[open journal PDF](https://par.nsf.gov/servlets/purl/10548928),
provides a randomized PTAS with running time
\(n^{O(d\log d/\epsilon^2)}\) under partition constraints and discusses
extensions to general matroids and monotone homogeneous concave matrix
criteria. Their conditioning method guesses and forces a subset, rescales,
and filters large vectors. These ingredients have clear prior ancestry.

The accuracy-dependent exponent differs from the proposed polynomial
dependence on \(1/\epsilon\) in fixed dimension. Partition/matroid constraints
also differ from an arbitrary exact knapsack budget. The local September
12 note already makes this comparison; the current application should
reference that audit rather than restart its novelty claim.

### Approximate Pareto and one-exact Pareto methods

Papadimitriou and Yannakakis, *On the approximability of trade-offs and
optimal access of Web sources*, FOCS 2000,
[primary conference paper](https://www.cs.purdue.edu/homes/yexiang/courses/18fall-cs590/papers/papadimitriou2000.pdf),
Theorems 1–2, establish polynomial-size approximate Pareto sets and
characterize efficient construction by a gap problem. This is foundational
ancestry for profile rounding; it does not automatically make signed
matrix-entry approximation preserve Loewner order or a Schur complement.

Herzel, Bazgan, Ruzika, Thielen, and Vanderpooten, *One-exact approximate
Pareto sets*, JGO 80:87–115, 2021,
[open paper](https://www.lamsade.dauphine.fr/~bazgan/Papers/JGO21.pdf),
studies sets that preserve one objective without deterioration and
approximate the remaining objectives. Efficient construction is
characterized through a suitable restricted auxiliary problem. This is
the appropriate terminology and precedent for exact budget preservation;
the PSD/Schur auxiliary algorithm is still a separate task.

The maximum-volume coordinate bound is also established machinery:
Awerbuch and Kleinberg's *Adaptive routing with end-to-end feedback:
Distributed learning and geometric approaches*,
[open manuscript](https://www.cs.cornell.edu/courses/cs683/2007sp/papers/OLSP.pdf),
Proposition 2.2, obtains a barycentric spanner by maximizing a determinant.
The replacement-column argument bounds all representation coefficients by
one. This elementary normalization argument should be attributed rather
than claimed as a separate new lemma.

Bökler, Chimani, and Jasper, *One-Exact Approximate Pareto Sets for APX-Hard
Multiobjective Problems*, ESA 2026,
[primary proceedings record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.112),
extends such frameworks using a relaxed restricted oracle. Its abstract
and proceedings description were examined, not its entire proof. It does
not by itself supply a matrix-order oracle for the present problem.

Mittal and Schulz, *An FPTAS for optimizing a class of low-rank functions
over a polytope*, Mathematical Programming 141:103–120, 2013,
[open manuscript](https://optimization-online.org/wp-content/uploads/2011/09/3152.pdf),
Theorem 3.3, assumes positive linear aggregates, an appropriate coordinate
monotonicity condition, and bounded multiplicative growth of the outer
function. Signed matrix entries and Schur-complement cancellation do not
automatically meet these assumptions. In addition, the basic theorem
optimizes over a continuous polytope; its discrete extreme-point extension
requires additional objective structure. A generic appeal to “low rank”
does not establish that this result subsumes the proposed application.

### Other results screened

[Atamtürk and Gómez's 2-by-2 convexifications paper](https://link.springer.com/article/10.1007/s10107-023-01924-w),
Proposition 2, gives NP-hardness for positive-cross-term convex indicator
quadratics through a rank-one-plus-identity construction. Thus exact
tractability cannot be assumed merely because the off-diagonal rank is one.
The result is compatible with an approximation scheme.

[Elbassioni and Nguyen's low cp-rank approximation schemes](https://arxiv.org/abs/1411.5050)
concern binary packing/covering problems with completely positive
decompositions. The factors are nonnegative, and the read statements do not
give the inverse-submatrix gain objective for arbitrary signed factors.
Only the relevant formulation and theorem statements were screened.

[Han, Li, and Li's 2026 convex-maximization framework](https://arxiv.org/html/2604.27427v1)
requires convex maximization with a comonotone feasible set. The lifted gain
\(g(K)\) here is concave in \(K\), being the infimum of linear forms. The
paper's fixed-rank convex-maximization statement therefore does not directly
apply. Its introduction and main modeling assumptions were examined.

[Paul and Drineas, *Feature Selection for Ridge Regression with Provable
Guarantees*](https://arxiv.org/abs/1506.05173), 2015, is a feature-sampling
and spectral-sparsification comparator. Its prediction-risk guarantees
relative to all features do not state optimization of the best affordable
support. Its abstract was read, with the distinction cross-checked by a
delegated literature reviewer.

[Cifuentes and Li, *Solving Sparsity Constrained PCA, Regression, and QCQP
via the Spartrahedron*](https://arxiv.org/html/2603.18215v1), 2026,
gives SDP approximation and exactness guarantees for sparse ridge
regression. A delegated reviewer checked Section 5: its relaxation-gap
bound and exactness regime are not a fixed-data-rank arbitrary-ridge FPTAS.
The exactness assumptions include full column rank and a signal/noise
regime. The root literature reviewer independently read the introduction
and modeling assumptions, but did not recheck the Section 5 proofs.

## 4. Contribution and significance assessment

The defensible candidate statement is narrow: fixed-factor covariance
permits a deterministic, condition-independent FPTAS for explained-variance
maximization with an exact arbitrary single budget, using the repository's
existing PSD approximation-set construction and cheapest-state retention.
No published equivalent was found in this audit. Further citation tracing
from Das–Kempe, Bienstock–Chen, and Xie–Deng remains worthwhile before any
priority claim.

This would be a useful structural tractability result for dense factor
models, noisy linear measurement selection, and ridge feature selection.
It does not establish statistical consistency, reliable feature recovery,
out-of-sample improvement, or a practical speedup. The polynomial exponent
in matrix dimension remains large. Relative gain can also be a weak
guarantee for a tiny residual, so gain and residual claims must stay
separate.

Against the user's request for advances beyond existing local work, this is
an application and exact-resource extension, not a new major approximation
mechanism. A standalone paper-level assessment should account for how much
of its theorem follows by a short transfer from the September 12 result.

## 5. Search and verification record

Searches included “subset selection low rank approximation scheme”,
“quadratic optimization indicator variables FPTAS”, “ridge regression
FPTAS”, “fixed rank best subset”, “budgeted sparse regression”, “regression
knapsack low rank”, “experimental design FPTAS”, “Loewner knapsack”, and
“one-exact approximate Pareto sets”. Additional searches screened PSD
rounding, spectral experimental design, and low cp-rank nonlinear programs.
Searches were performed on 2026-09-27. Search snippets were used to locate
sources; mathematical comparisons above use the linked primary sources,
with limited-read items identified explicitly.

The local DAG note and relevant sections of the primary PDFs were read.
Downloaded source PDFs and `pdftotext -layout` outputs are in
[`sources-sparse-psd/`](sources-sparse-psd/). Targeted commands used:
`rg` over the selected source texts, `sed` over the selected theorem
sections, Python `urllib.request.urlretrieve`, and `pdftotext -layout`.
All six retained PDF downloads and text extractions succeeded. An outdated
Optimization Online URL for the Han–Li–Li paper returned 404; the current
arXiv text was read instead.
A targeted Python documentation check passed: math delimiter counts are
balanced, and the source directory contains six retained PDFs. This check
does not validate mathematics or source interpretations.

No project-wide verification, CI inspection, numerical experiment, or Lean
run was performed for this literature audit. The displayed algebra was
checked directly; full algorithm correctness remains a separate review.
