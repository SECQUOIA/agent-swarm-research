# Sparse-Newton dequantization envelope for hybrid QIPMs

Status: Proved synthesis theorem  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on novelty  
Question: When does explicit direction tomography eliminate any polynomial
total-work advantage across sparse conic QIPMs?

## Dense-transcript compiler

At round \(t\), suppose a hybrid QIPM forms

\[
 K_td_t=r_t
\]

and materializes a dense classical direction satisfying

\[
 \|K_t\widehat d_t-r_t\|_2\leq\eta_t\|r_t\|_2.
\]

Assume the system is consistent, \(K_t\) has full column rank (in particular,
the intended square KKT system is nonsingular), the iteration starts from
\(d_0=0\), the outer proof accepts every direction with this contract, and
that
multiplication by \(K_t,K_t^T\), including evaluation of current entries,
costs \(M_t\). Classical CGLS/LSQR, without forming normal equations, obtains
the same contract in exact arithmetic using

\[
 \boxed{
 O\!\left(M_t\kappa_2(K_t)\log\frac2{\eta_t}\right)
 }
\]

work and \(O(\operatorname{nnz}K_t+D_t)\) storage. Indeed CG on
\(K_t^TK_td=K_t^Tr_t\) satisfies

\[
 \|K_td_k-r_t\|_2
 \leq2\left(\frac{\kappa_2(K_t)-1}{\kappa_2(K_t)+1}\right)^k\|r_t\|_2.
\]

Thus sparse, polylogarithmically conditioned systems are classically solvable
in \(D_t\operatorname{polylog}D_t\) work, while dense quantum readout already
costs \(\Omega(D_t)\) word writes. Summing over a fixed common path-following
schedule gives a trajectory-level no-polynomial-advantage result.

If an SPD system has a supplied elimination ordering of width \(w_t\), sparse
Cholesky instead costs \(O(D_tw_t^2)\) factorization and \(O(D_tw_t)\) per
solve. Hence the useful classical envelope is

\[
 \widetilde O\!\left(
 \min\{M_t\kappa_2(K_t),D_tw_t^2\}
 \right).
\]

The width arm needs a stable pivot-free formulation; indefinite KKT systems
and finite precision require explicit pivot and bit-growth qualifications.

## Conic scope

The theorem is cone-agnostic. For an uncondensed augmented system over
bounded-size cone blocks, bounded constraint incidence gives
\(\operatorname{nnz}K_t=O(D_t)\). It therefore covers LP, bounded-order SOC
and rotated-SOC products, fixed-size PSD blocks, exponential and power cones,
and sparse augmented nonsymmetric-cone formulations whenever their actual KKT
entries are classically evaluable. For chordal SDP, the relevant parameter is
the extended constraint-support width, not merely aggregate sparsity.

The result does not cover coherent/implicit iterates, scalar or few-observable
output, a quantum-only block encoding, dense Schur complements, a different
scaled residual norm, free QRAM/preconditioners, or parallel-depth claims.
Apers--Gribling's tall-LP algorithm also escapes: its gain is in quantum row
sampling/Hessian formation, not a QLS followed by dense direction tomography.

For compressed output, the later
[sparse-SQ conditioning theorem](2026-09-04-sparse-sq-conditioning-frontier.md)
gives a complementary and stronger boundary under row-and-column sparse
access: solution-distribution sampling is dimension-independent at fixed
sparsity, condition, and accuracy.  Polynomial sampling hardness therefore
requires at least logarithmic condition growth, or squared-logarithmic growth
for SPD systems.

## Novelty boundary

CGLS, Kaczmarz, sparse elimination, and the individual conic solvers are known.
A targeted search found no single sparse, cone-agnostic trajectory replacement
theorem with this matched residual and output contract. Its value is as an
apparently new exclusion criterion: a sparse QIPM must avoid dense classical
direction materialization and maintain an efficient nonlinear iterate oracle,
or its Newton module is classically replaceable in the well-conditioned or
small-width regimes.
