# Supporting result: exact quantum crossover for tall sparse LPs

Date: 2026-09-02

## Main result

This note gives a correct exact-output wrapper for the tall-LP quantum
interior-point method of Apers and Gribling.  The wrapper preserves sublinear
dependence on the number of constraints.  It is a supporting QIPM corollary,
not a best-known exact tall-LP algorithm: subsequent auditing found stronger
published exact oracle algorithms and a stronger quantum Clarkson method.  The
only apparently unstated part is coherent recovery of the binding rows from an
already available accurate feasible IPM point.

Consider the integer linear program

\[
  \min_{z\in\mathbb R^d} c^\top z
  \quad\text{subject to}\quad Az\geq b,
  \qquad A\in\mathbb Z^{n\times d},
\tag{1}
\]

with

\[
 |a_{ij}|,|b_i|,|c_j|\leq H=2^\ell.
\]

Assume the hypotheses needed by the underlying tall-LP QIPM: the feasible
region is bounded and full dimensional and a suitable initial interior point is
available.  In addition, assume that (1) has a unique, nondegenerate, strictly
complementary optimum \(z^*\).  Its active set \(I\) then has \(|I|=d\),
\(A_I\) is nonsingular, and the unique optimal dual multiplier is supported on
\(I\):

\[
 z^*=A_I^{-1}b_I,
 \qquad
 \lambda_I^*=A_I^{-\top}c>0.
\]

Let

\[
 \lambda=\min_{i\in I}\lambda_i^*,
 \qquad
 \gamma=\min_{j\notin I}(a_j^\top z^*-b_j),
\]

and define

\[
 R=\max_j\|a_j\|_2,
 \qquad
 K=\|A_I^{-1}\|_{1\to2}.
\]

### Localization lemma

If \(z\) is feasible and has objective error

\[
 G=c^\top z-c^\top z^*,
\]

then

\[
 G=(\lambda_I^*)^\top(A_Iz-b_I),
\]

where every entry of \(A_Iz-b_I\) is nonnegative.  Therefore

\[
 \|A_I(z-z^*)\|_1\leq G/\lambda,
 \qquad
 \|z-z^*\|_2\leq KG/\lambda.
\tag{2}
\]

It follows that

\[
 a_i^\top z-b_i\leq G/\lambda \quad (i\in I)
\tag{3}
\]

and

\[
 a_j^\top z-b_j
 \geq \gamma-RKG/\lambda \quad (j\notin I).
\tag{4}
\]

Thus a sufficiently accurate feasible point separates all binding from all
nonbinding rows.

## Universal bit bound independent of \(n\)

The important point for tall LPs is that the required accuracy depends on the
dimension \(d\) and coefficient bit length \(\ell\), not on the total number
\(n\) of rows.

Let \(r\) be the maximum row sparsity and set

\[
 D=(\sqrt r H)^d,
 \qquad
 R_{\max}=\sqrt r H,
 \qquad
 K_{\max}=\sqrt d\,(\sqrt r H)^{d-1},
\tag{5}
\]

where the last power is interpreted as one when \(d=1\), and

\[
 M=\max(1,R_{\max}K_{\max}).
\]

Sparse-row Hadamard bounds give \(|\det A_I|\leq D\).  Because \(A_I,b_I,c\)
are integral, Cramer's rule gives

\[
 \lambda\geq D^{-1},
 \qquad
 \gamma\geq D^{-1}.
\tag{6}
\]

The cofactor formula gives \(K\leq K_{\max}\), and trivially
\(R\leq R_{\max}\).

Ask the approximate QIPM for a feasible \(\widetilde z\) with

\[
 c^\top\widetilde z-\operatorname{OPT}
 \leq
 E:=\frac{1}{8D^2M}.
\tag{7}
\]

Substituting (5)--(7) into (3)--(4) gives the explicit separation

\[
 a_i^\top\widetilde z-b_i\leq\frac{1}{8D}\quad(i\in I),
\tag{8}
\]

\[
 a_j^\top\widetilde z-b_j\geq\frac{7}{8D}\quad(j\notin I).
\tag{9}
\]

Hence evaluation to additive error at most \(1/(8D)\), followed by thresholding
at \(1/(2D)\), is an exact membership predicate for \(I\).  The required
precision is

\[
 \log(1/E)=O(d(\ell+\log d)),
\tag{10}
\]

which is independent of \(n\).  This is sharper for the tall-oracle setting
than using the total input length, which contains \(\Theta(n)\) coefficients.

## Quantum crossover algorithm

1. Run the Apers--Gribling QIPM with target (7).  Its output is an explicit
   feasible \(d\)-vector \(\widetilde z\).
2. Given coherent row access, reversibly compute
   \(a_i^\top\widetilde z-b_i\) to the precision in (8)--(9).  Quantum marked
   item enumeration recovers the exactly \(d\) rows below threshold using
   \(\widetilde O(\sqrt{nd})\) row queries.
3. Read those rows and solve
   \[
   A_I z^*=b_I,
   \qquad
   A_I^\top\lambda_I^*=c
   \]
   by exact rational arithmetic.
4. Check nonsingularity and \(\lambda_I^*>0\) classically.  Use Grover search
   over all rows to look for a violated inequality
   \(a_j^\top z^*<b_j\).  If no violation is found, with amplified failure
   probability \(\delta\), the returned pair is an exact primal--dual KKT
   certificate.

Under the promise, the candidate passes.  Random failure in the approximate
QIPM, enumeration, or verification can be handled by repetition.

## Complexity

Let \(Q_{AG}(n,d,r,E)\) and \(T_{AG}(n,d,r,E)\) denote the row-query and gate
complexities of the chosen Apers--Gribling barrier, for row sparsity \(r\).
The exact wrapper has

\[
 Q_{\rm exact}
 =Q_{AG}(n,d,r,E)
  +\widetilde O(\sqrt{nd}+d+\sqrt n)
\tag{11}
\]

row queries and

\[
 T_{\rm exact}
 =T_{AG}(n,d,r,E)
  +\widetilde O\!\left(
      r\sqrt{nd}\,\operatorname{poly}(d,\ell)
      +\operatorname{ExactSolve}(d,\ell)
    \right).
\tag{12}
\]

In the row-query convention of Apers and Gribling, one query returns an entire
sparse row; the factor \(r\) belongs in the gate ledger, not the row-query
ledger.  Before expanding its hidden precision dependence, their theorem gives

\[
 \widetilde O(n^{3/4}d^{5/4})
\]

row queries for the volumetric barrier or

\[
 \widetilde O(\sqrt n\,d^5)
\]

for the Lewis-weight barrier.  A conservative substitution should be written
as \(\sqrt n\operatorname{poly}(d,\ell,\log n)\), rather than claiming that
every displayed \(d\)-exponent survives expansion of the suppressed factors.
Since (10) has no \(n\)-dependence, the exact crossover does preserve the
sublinear-in-\(n\) exponents.  It outputs \(z^*\),
the \(d\) active row indices, and \(\lambda_I^*\), all as exact rationals.

Writing \(B=\Theta(d(\ell+\log r))\) for the identification precision, a
literal extra \(B\)-factor would make the volumetric bound sublinear when
\(n\gg d^5B^4\), and the Lewis-weight bound sublinear when
\(n\gg d^{10}B^2\).  These are sufficient regimes, not optimized boundaries.

The \(\widetilde O(\sqrt{nd})\) enumeration cost is optimal in the abstract
membership-oracle model for listing \(d\) marked items.  This does not by itself
prove that every exact-primal-output LP algorithm needs that cost; it proves
tightness of the crossover module and of the explicit sparse-certificate
contract.  In fact, the same order is necessary even for exact primal output.
Split \(n=dq\) one-sparse lower-bound rows into \(d\) blocks, one per scalar
variable.  In each block exactly one hidden lower bound has value
\(v_j\in\{1,2\}\), while the others have value zero; add the known upper bound
\(z_j\leq3\) and minimize \(\sum_jz_j\).  The unique nondegenerate strictly
complementary optimum is \(z_j^*=v_j\).  Recovering the exact primal vector
solves \(d\) independent search/value problems, giving
\(\Omega(d\sqrt q)=\Omega(\sqrt{nd})\) quantum row queries by direct sum, while
a randomized classical algorithm needs \(\Omega(n)\).  Thus the crossover
overhead has the optimal \(n,d\) query scaling on the promised problem class.

## Why this is not already implied by existing exact-QIPM claims

- Classical finite optimal-face and basis identification is old.  Ye's 1992
  finite-convergence paper develops an exact termination procedure, and modern
  crossover methods likewise recover a basis from an interior solution.
- Nannicini's quantum simplex work uses Grover-type routines for pricing and
  optimality after a basis is already available.  It does not recover the
  limiting IPM basis from a coarse tall-LP iterate.
- The 2025 "almost-exact" QIPM of Mohammadisiahroudi et al. invokes classical
  rounding after reaching exponentially small error but does not analyze the
  rounding cost.  Its bit length is the total dense input length and its
  framework is not sublinear in the number of rows.
- Apers and Gribling return an explicit feasible \(E\)-optimal point but do not
  state an exact rational crossover or exact primal--dual certificate.

## Strong collisions and resulting downgrade

- Objois and Vladu, *Adaptive Sparsification for Linear Programming*,
  arXiv:2510.08348, already give a quantum Clarkson algorithm returning an
  exact solution in \(\widetilde O(\sqrt n\,d^3)\) row queries, without the
  nondegeneracy promise used here.
- Dadush, Végh, and Zambelli, *On finding exact solutions of linear programs in
  the oracle model*, arXiv:2606.11820, return exact primal and sparse exact dual
  solutions from a polyhedral separation oracle.  Grover implementation of a
  violated-row oracle gives an immediate exact quantum row-query algorithm.
- Apers and Gribling's own cutting-plane appendix, combined with the same
  promise-specific crossover, has better \(d\)-dependence than either of their
  IPM bounds.

Therefore the theorem below should not be advertised as the first exact
quantum tall-LP algorithm, a best complexity result, or the main result of this
research cycle.

The narrow defensible claim is therefore:

> A coherent optimal-row crossover converts the tall-row-oracle QIPM into a
> bounded-error exact rational LP algorithm under unique nondegeneracy and
> strict complementarity, while preserving its sublinear dependence on the
> number of constraints.

The result is conditional on the structural promise.  Degenerate or
multiple-optimum LPs require optimal-face recovery rather than the simple
\(d\)-row theorem.  The gate bound must also charge reversible fixed-point
arithmetic and any setup used to access the explicit \(d\)-vector.
Apers and Gribling use unit-cost exact floating-point arithmetic; multiplying
their arithmetic count by a bit-multiplication cost is a conditional gate
ledger, not a finite-precision stability proof for their entire path.  Likewise,
explicitly loading all \(nr\) coefficients would erase sublinear wall time: the
theorem uses the same concise/coherent row-oracle model as the base algorithm.

## Primary sources checked

- Apers and Gribling, *Quantum speedups for linear programming via interior
  point methods*, arXiv:2311.03215, Theorem 1.1:
  https://arxiv.org/abs/2311.03215
- Y. Ye, *On the finite convergence of interior-point algorithms for linear
  programming*, Mathematical Programming 57 (1992), DOI:
  https://doi.org/10.1007/BF01581087
- Ge, Wang, Xiong, and Ye, *From an Interior Point to a Corner Point: Smart
  Crossover*, arXiv:2102.09420:
  https://arxiv.org/abs/2102.09420
- Nannicini, *Fast quantum subroutines for the simplex method*,
  arXiv:1910.10649:
  https://arxiv.org/abs/1910.10649
- Mohammadisiahroudi et al., *Optimal Scaling Quantum Interior Point Method for
  Linear Optimization*, arXiv:2512.04510:
  https://arxiv.org/abs/2512.04510
- Objois and Vladu, *Adaptive Sparsification for Linear Programming*,
  arXiv:2510.08348:
  https://arxiv.org/abs/2510.08348
- Dadush, Végh, and Zambelli, *On finding exact solutions of linear programs in
  the oracle model*, arXiv:2606.11820:
  https://arxiv.org/abs/2606.11820

Status: **proof complete at the query-complexity/composition level; apparently
unstated as an IPM crossover module, but superseded in overall exact-LP
complexity by the algorithms above.**  Retain as a useful supporting lemma, not
as an impactful headline result.
