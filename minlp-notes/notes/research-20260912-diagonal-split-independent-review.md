# Independent review of the diagonal-split certificate

**Accepted within the stated scope.** A fresh reviewer found no mathematical or implementation defect in [the diagonal-split result](research-20260912-diagonal-split-separation.md). The saved fast-kinetics case has a certified lower bound of approximately **15.043116838985817** on every admissible diagonal-split continuous optimum. Its independently replayed memory upper bound is approximately **14.950572422652932**. The exact rational difference is positive and displays as **0.09254441633288486**. The JSON rational values, rather than these rounded displays, establish the strict inequality.

The result compares relaxation bounds for one fixed model and selection constraint. It also covers intersections of affine upper supports from different diagonal splits, as explained below. It does not establish a solver runtime advantage, dominance over other classes of valid inequalities, or a result about arbitrary nondiagonal splits. The mathematical ingredients are established convexity and weak semidefinite duality; this review makes no originality claim for them. In particular, the fixed-matrix convexity claim is explicitly covered by [Kim and Kim (2006)](https://arxiv.org/abs/cs/0611043) and [Kim (2015)](https://arxiv.org/abs/1509.00777). Both sources were already routed to the sole literature-ingestion agent by the author.

The quantifiers and inequality directions are correct. Fix a feasible selection point \(z\). Restricting to \(T=\{i:z_i>0\}\) makes the virtual covariance

\[
S(a)=R_{TT}+\operatorname{diag}\!\left(a_i\frac{1-z_i}{z_i}:i\in T\right)
\]

positive definite for every positive reference vector \(a\), including references that fail the competing relaxation's constraint \(R-\operatorname{diag}(a)\succeq0\). The determinant lemma expresses the fixed-point objective as a constant plus \(\log\det(S+C)-\log\det S\), with \(C\succeq0\). Its directional Hessian is nonnegative because \(A=S^{-1}\succeq B=(S+C)^{-1}\succeq0\) implies

\[
A\otimes A-B\otimes B=(A-B)\otimes A+B\otimes(A-B)\succeq0.
\]

Thus the affine tangent is a global lower support in \(a\). The derivative \(g_i\) is nonpositive, with exactly zero derivative when \(z_i=0\) or \(z_i=1\). Set \(w=-g\). For any \(Y\succeq0\) with \(\operatorname{diag}(Y)\ge w\), positivity of an admissible diagonal \(D=\operatorname{diag}(a)\) gives

\[
w^Ta\le\operatorname{tr}(DY)\le\operatorname{tr}(RY).
\]

Combining the inequalities proves the reported universal lower bound. Feasibility of the fixed \(z\) then bounds every split's maximized continuous objective from below, and hence also their infimum over admissible splits. Strong duality and numerical optimization success are unnecessary. The same conclusion applies when admissible splits require a strict covariance inequality, since that only reduces the split family.

There is also a stronger pointwise interpretation. Write \(\mathcal A\) for the admissible diagonal splits and \(\mathcal Z\) for the original capped simplex. The same saved \(z^0\in\mathcal Z\) satisfies \(\phi_D(z^0)\ge L\) for every \(D\in\mathcal A\). Consequently

\[
\sup_{z\in\mathcal Z}\inf_{D\in\mathcal A}\phi_D(z)
\;\ge\;\inf_{D\in\mathcal A}\phi_D(z^0)
\;\ge\;L.
\]

This requires no minimax interchange or minimax theorem. Every globally valid affine upper support \(\ell\) of any admissible split's concave selection objective satisfies \(\ell(z^0)\ge\phi_D(z^0)\ge L\). Thus the point \((z^0,t=L)\) satisfies the intersection of arbitrarily many such inequalities \(t\le\ell(z)\), even when they come from different diagonal splits. The exact positive separation therefore remains for the pointwise best all-diagonal virtual-noise envelope and for any relaxation consisting of the original selection constraints and those affine upper supports. Branching, further selection inequalities, or other types of cuts can remove this witness and are outside the conclusion. No production-code change is needed for this corollary.

The implementation's heteroscedastic virtual-noise formula agrees exactly with the dense active-row covariance inverse, including zero selection weights, independent observations, zero latent variance, a single candidate, signed correlations, and nondiagonal positive priors. Its rational factor construction \(Y=BB^T+\operatorname{diag}(c)\) proves PSD without relying on floating eigenvalue signs. The nonnegative correction proves the required diagonal inequalities exactly. Numerical references and eigendecompositions only propose these witnesses.

The separate [review driver](../code/research_20260912/review_diagonal_certificate_independent.py) uses dense rational covariance solves for information and gradients. It independently constructs finer rational logarithm enclosures and replays the memory certificate using dense local regressions and recursive pricing over explicit selected histories. It does not use the production tridiagonal information evaluator, gradient evaluator, logarithm routine, or memory pricing implementation as its reference calculations. [Saved results](../code/research_20260912/results/diagonal-split-independent-review.json) report:

- 96 exact information and gradient comparisons;
- 96 exact PSD-factor, diagonal-domination, and trace checks, including deliberately indefinite numerical proposals;
- 96 midpoint convexity checks using rational determinant inequalities;
- 102 comparisons of certified lower bounds against exact information at feasible diagonal splits;
- 16 malformed-input rejections;
- one complete saved diagonal certificate and matching memory certificate, with 256 dense conditional patterns, 10,495 priced arcs, and 94,207 recursive pricing states.

The saved model, selection vector, reference information, gradient, determinant, factor, correction, trace, lower bound, artifact hashes, and exact positive separation all match. The memory replay uses the previously reviewed relative-information theorem; it independently checks its numerical constant, innovation normalization, tangent matrix, integer price, logarithm direction, and incumbent value for this artifact. The complete run took about 5.09 seconds with one BLAS thread on the shared machine.

The two-candidate illustration also checks directly: for \(R=\left[\begin{smallmatrix}2&1\\1&2\end{smallmatrix}\right]\), \(F=(1,-1)^T\), prior 1, and one selected observation, the integer information is \(3/2\). At \(z=(1/2,1/2)\) and reference diagonal \((1,1)\), the information is 2 and the gradient is \((-1/8,-1/8)\). The proposed rank-one dual has trace pairing \(1/4\), exactly cancelling the tangent intercept correction. Its all-diagonal lower bound is therefore \(\log 2\), yielding the stated separation \(\log(4/3)\).

The reviewed production file hash is `46ef03e8ea406c87ae546ba0b90d75694d2b651c8c65f626b426d359d5dad71a`. The saved certificate hash is `40ac3cad244d8a997fcb3606b9c428e410aad2555cfceada6f107c95f05be109`. Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/review_diagonal_certificate_independent.py
```
