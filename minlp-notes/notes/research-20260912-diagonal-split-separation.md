# Comparing all diagonal virtual-noise splits

**Status: [accepted by fresh independent review](research-20260912-diagonal-split-independent-review.md) within the stated scope. No novelty claim for the convexity, SDP duality, or formulation.** A fixed feasible selection point gives a certified lower bound on every admissible diagonal-split continuous relaxation. For the existing 48-candidate fast-kinetics case, that lower bound exceeds the calendar-memory certificate's upper bound on the integer optimum by more than 0.09254 in log determinant. The same separation persists when the split is optimized separately at each selection point and when globally valid affine upper supports from different splits are combined.

The first synthetic case also provides a useful negative result: the same construction at its saved scalar-relaxation optimizer does not separate all diagonal splits. That does not decide whether a different selection point, or a stronger minimax computation, would establish separation.

## Fixed-selection convexity and an all-split bound

Let \(R\succ0\) be the observation covariance, \(J_0\succ0\) the prior information, and \(F\) the sensitivity matrix. An admissible diagonal split satisfies

\[
D=\operatorname{diag}(a),\qquad a>0,\qquad R-D\succeq0.
\]

Fix any feasible continuous selection vector \(z\in[0,1]^n\), \(\sum_i z_i=k\). On the rows \(T=\{i:z_i>0\}\), write \(h_i=(1-z_i)/z_i\) and

\[
S(a)=R_{TT}+\operatorname{diag}(h_i a_i:i\in T),\qquad
\phi_z(a)=\log\det\{J_0+F_T^TS(a)^{-1}F_T\}.
\]

Every positive \(a\) makes this point value well defined, whether or not \(R-D\succeq0\). The latter condition is required for the competing relaxation's admissible split, not for the tangent reference used below.

The determinant lemma gives

\[
\phi_z(a)=\log\det J_0+\log\det(S+C)-\log\det S,
\qquad C=F_TJ_0^{-1}F_T^T\succeq0.
\]

The function \(S\mapsto\log\det(I+CS^{-1})\) is classically convex; see [Kim and Kim (2006)](https://arxiv.org/abs/cs/0611043) and [Kim (2015), Theorem 1 and Lemma 1](https://arxiv.org/abs/1509.00777). The 2015 full text was read for this investigation. For completeness, if \(A=S^{-1}\) and \(B=(S+C)^{-1}\), then \(A\succeq B\succeq0\), and the Hessian in a symmetric direction \(H\) is

\[
\operatorname{tr}(AHAH)-\operatorname{tr}(BHBH)\ge0,
\]

because
\(A\otimes A-B\otimes B=(A-B)\otimes A+B\otimes(A-B)\succeq0\).
Affine substitution proves convexity in \(a\). With \(V=S^{-1}F_T\), the gradient is

\[
g_i=-h_i V_iJ^{-1}V_i^T\le0\quad(i\in T),\qquad g_i=0\quad(i\notin T).
\]

For any positive reference \(a^0\), convexity gives
\(\phi_z(a)\ge\phi_z(a^0)+g^T(a-a^0)\). Set \(w=-g\ge0\). If a matrix \(Y\) satisfies

\[
Y\succeq0,\qquad \operatorname{diag}(Y)\ge w,
\]

then every admissible split satisfies

\[
w^Ta\le\operatorname{tr}(DY)\le\operatorname{tr}(RY).
\]

Consequently the explicit number

\[
L=\phi_z(a^0)-g^Ta^0-\operatorname{tr}(RY)
\tag{1}
\]

is a lower bound on \(\phi_z(a)\) for **every** admissible diagonal split. Since \(z\) is feasible, it also bounds each split's continuous optimum from below. This reasoning needs neither strong SDP duality nor an optimal numerical reference or dual solution.

## Pointwise split optimization and combined tangent cuts

Let \(\mathcal A\) denote the admissible diagonal splits, \(\mathcal Z=\{z\in[0,1]^n:\sum_i z_i=k\}\), and \(\varphi_D(z)=\phi_z(a)\) for \(D=\operatorname{diag}(a)\). The certificate uses one common feasible point \(z^0\), with \(\varphi_D(z^0)\ge L\) for every \(D\in\mathcal A\). Therefore

\[
\sup_{z\in\mathcal Z}\inf_{D\in\mathcal A}\varphi_D(z)
\;\ge\;\inf_{D\in\mathcal A}\varphi_D(z^0)
\;\ge\;L.
\]

Thus optimizing the diagonal split separately at every selection point cannot remove the certified gap. No minimax interchange or minimax theorem is needed.

More generally, let \(\ell\) be any globally valid affine upper support of an admissible split's concave selection objective, including its valid tangent cuts. Then \(\ell(z^0)\ge\varphi_D(z^0)\ge L\). Consequently \((z^0,t=L)\) satisfies the original selection constraints and the intersection of arbitrarily many inequalities \(t\le\ell(z)\), even when they come from different admissible splits. For the certified kinetic case, a root outer-approximation relaxation built only from these constraints must retain a gap of at least **0.09254441633288486** above the true integer optimum, using the exact rational value underlying that display. Branching, added selection constraints, or cuts outside this family can remove the witness and are outside this conclusion. The [fresh review](research-20260912-diagonal-split-independent-review.md) also accepted this corollary.

## Exact certificate implementation

[certify_diagonal_split.py](../code/research_20260912/certify_diagonal_split.py) is separate from the previously reviewed solver and certificate modules. It interprets the saved rational model data and selection weights exactly.

For the stationary scalar Markov covariance, it reuses the reviewed exact tridiagonal solver. Write the latent precision as \(M/c\), and let

\[
t_i=a_i^0(1-z_i)+rz_i>0,\qquad
\{M+c\operatorname{diag}(z_i/t_i)\}U=MF.
\]

Then

\[
J=J_0+F^T\operatorname{diag}(z_i/t_i)U,
\qquad
g_i=-\frac{z_i(1-z_i)}{t_i^2}U_iJ^{-1}U_i^T.
\]

These formulas handle zero selection weights without dividing by \(z_i\). The zero-latent, independent-observation, and one-candidate cases use direct diagonal formulas. All matrix entries and operations in this evaluation are rational.

A floating SDP solution only proposes a dual matrix. Its symmetric eigendecomposition proposes a factor, which is rounded to a rational matrix \(B\). The code constructs

\[
Y=BB^T+\operatorname{diag}(c_i),\qquad
c_i=\max\{0,-g_i-\sum_j B_{ij}^2\}.
\]

This proves PSD and diagonal domination by construction, regardless of floating eigenvalue errors. The exact trace \(\operatorname{tr}(RY)\), gradient intercept, and existing rational log-determinant enclosure then give (1). The reference split is rounded to positive rational coordinates. Its covariance-split feasibility is deliberately not assumed or required.

The saved certificate includes the rational reference, information, gradient, factor, diagonal correction, lower bound, exact model data, and hashes of the numerical proposal and matching memory certificate. The factor grid and reference grid both have spacing \(10^{-8}\). Output display values are rounded; the rational entries carry the proof.

## Bounded numerical investigation

The numerical proposal code is [diagonal_split_probe.py](../code/research_20260912/diagonal_split_probe.py). The initial logdet-LMI formulation uses Kim's representation with a small information-dimensional auxiliary matrix. Clarabel solved the synthetic case, but failed on the kinetic case. The saved reproducible probe instead uses SLSQP on the exact fixed-point objective, with eigenvalue constraints for \(R-D\succeq0\), followed by the linear dual SDP. Solver statuses and residuals are retained, and neither is used as proof.

| Case | Numerical fixed-point minimum | Numerical dual lower estimate | Memory upper bound | Exact all-diagonal lower bound |
|---|---:|---:|---:|---:|
| Synthetic, \(n=48\), seed 0 | 7.689273264 | 7.689273183 | 7.699350373 | Not generated |
| Fast kinetics, \(n=48\) | 15.043117915 | 15.043117986 | 14.950572423 | 15.043116839 |

The [kinetics certificate](../code/research_20260912/results/diagonal-split-kinetics-certificate.json) gives the exact rational separation whose displayed value is **0.09254441633288486**. Exact generation took 0.226 seconds on the shared machine; this excludes the numerical proposal, which took 1.56 seconds. These are single observed runs, with one BLAS thread. The result concerns relaxation bounds, not fully solved mixed-integer formulations, and only this one kinetic case was certified for arbitrary diagonal splits in this bounded probe.

The kinetic SLSQP proposal stopped with `More than 3*n iterations in LSQ subproblem`. Its minimum covariance-split eigenvalue was approximately \(-1.16\times10^{-10}\). The floating dual had a minimum eigenvalue around \(-1.42\times10^{-9}\), and its nominal lower estimate slightly exceeded the recomputed point value. These are reasons to use the exact reconstruction, not evidence against the reconstructed bound. The synthetic dual status was `optimal_inaccurate`; its negative separation is recorded only as a numerical failure of the chosen fixed-point witness.

For the synthetic case, minimizing at the saved scalar-optimal \(z\) is weaker than determining
\(\inf_D\sup_z\phi_z(D)\). The negative probe therefore does not show that an optimized diagonal relaxation is as strong as the memory bound.

## Exact two-candidate example

The earlier two-candidate example also separates every diagonal split. Let

\[
R=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad
F=\begin{pmatrix}1\\-1\end{pmatrix},\quad J_0=1,\quad k=1,
\quad z=(1/2,1/2).
\]

At \(a^0=(1,1)\), the information equals 2 and \(g=(-1/8,-1/8)\). Take

\[
Y=\frac18\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0.
\]

Its diagonal equals \(-g\), and \(-g^Ta^0=\operatorname{tr}(RY)=1/4\). Equation (1) gives \(L=\log2\). Every diagonal split's continuous optimum therefore exceeds the exact integer optimum \(\log(3/2)\) by at least \(\log(4/3)\). The split \(a^0\) lies on the allowed PSD boundary; the same lower bound holds if the competing formulation instead requires a strict covariance split. This elementary extension is an illustration, not an originality claim.

## Checks and reproduction

[verify_diagonal_split.py](../code/research_20260912/verify_diagonal_split.py), written by the implementing researcher, independently forms dense rational covariances and inverses. [The saved checks](../code/research_20260912/results/diagonal-split-validation.json) cover 96 exact point/gradient comparisons, 96 PSD factor and exact trace checks using deliberately indefinite numerical proposals, 96 high-precision evaluations of convex tangent inequalities, and the exact toy dual. The subsequent [fresh independent review](research-20260912-diagonal-split-independent-review.md) accepted the theory and implementation, independently replayed the complete saved diagonal and memory certificates, and verified their exact positive separation. Its separate checks also covered 102 comparisons against feasible diagonal splits and 16 malformed-input rejections.

The numerical probes used CVXPY 1.9.2, Clarabel 0.11.1, NumPy 2.5.3, and SciPy 1.18.1. Temporary `uv --with` dependencies leave the project's dependency files unchanged.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 --with cvxpy==1.9.2 --with clarabel==0.11.1 python code/research_20260912/diagonal_split_probe.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --project code/research_20260912 --with cvxpy==1.9.2 --with clarabel==0.11.1 python code/research_20260912/diagonal_split_probe.py --input code/research_20260912/results/dense-design-kinetics-n48-certificates.json --memory code/research_20260912/results/noisy-markov-kinetics-certificate-n48-fast.json --output code/research_20260912/results/diagonal-split-kinetics-probe.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_diagonal_split.py code/research_20260912/results/diagonal-split-kinetics-probe.json code/research_20260912/results/diagonal-split-kinetics-certificate.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/verify_diagonal_split.py
```

Both primary convexity sources and the 2019 publication associated with Kim's preprint were routed to the sole literature-ingestion agent. They should be cited as prior art for this proof ingredient.
