# Eccentricity-profile preconditioning for sparse SOCP Newton systems

Status: Proved; independently audited; targeted literature screen complete  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High in exact arithmetic; finite-precision stability requires the
product-form qualification below  

## Result

A large Lorentz block can make an SOCP normal matrix dense even when the
underlying scalar base matrix has treewidth zero.  Its entire departure from
the sparse base nevertheless has signed rank at most two.  This observation
admits an adaptive extension to arbitrarily many Lorentz blocks.

Fix a threshold \(\theta\geq1\).  Treat exactly only the blocks whose current
radial eccentricity exceeds \(\theta\), and replace every other inverse
barrier Hessian by its scalar middle eigenvalue.  If \(b_\theta\) blocks are
treated exactly, then:

1. the resulting preconditioner differs from a sparse base by rank at most
   \(2b_\theta\);
2. the preconditioned condition number is at most \(\theta^2\), independently
   of the maximum eccentricity, the number of other cones, and all cone
   dimensions; and
3. if the sparse base normal graph has treewidth \(\tau\), one Newton solve has
   near-linear classical work when \(\tau,\theta,b_\theta\) are small.

Thus a few arbitrarily eccentric, arbitrarily high-dimensional Lorentz blocks
cannot by themselves create a polynomial Newton-solve advantage for a
full-output QIPM under matched access.  The theorem closes the large-cone gap
left open by the generic bounded-treewidth replacement theorem.

## Lorentz block identity

For \(x_\ell=(t_\ell,z_\ell)\in\operatorname{int}Q_{n_\ell}\), put

\[
 r_\ell=\|z_\ell\|_2,\qquad
 s_\ell=t_\ell^2-r_\ell^2,\qquad
 d_\ell={s_\ell\over2},\qquad
 \chi_\ell={t_\ell+r_\ell\over t_\ell-r_\ell}.
 \tag{1}
\]

When \(r_\ell>0\), define

\[
 u_{\ell,\pm}={1\over\sqrt2}(1,\ \pm z_\ell/r_\ell).
\]

For the standard barrier
\(F_\ell(x)=-\log(t^2-\|z\|_2^2)\), direct inversion gives

\[
 H_\ell^{-1}
 =d_\ell I
  +r_\ell(t_\ell+r_\ell)u_{\ell,+}u_{\ell,+}^T
  -r_\ell(t_\ell-r_\ell)u_{\ell,-}u_{\ell,-}^T.       \tag{2}
\]

The three eigenvalue ratios relative to \(d_\ell I\) are

\[
 \chi_\ell,\quad 1\ \text{(with multiplicity \(n_\ell-2\))},
 \quad\chi_\ell^{-1}.                                    \tag{3}
\]

At \(r_\ell=0\), equation (2) is interpreted as
\(H_\ell^{-1}=d_\ell I\) and \(\chi_\ell=1\).

Let \(A=[A_1\ \cdots\ A_L]\in\mathbb R^{m\times n}\) have full row
rank, with columns partitioned by the Lorentz blocks.  Define the exact and
base normal matrices

\[
 N=\sum_{\ell=1}^L A_\ell H_\ell^{-1}A_\ell^T,
 \qquad
 S=\sum_{\ell=1}^L d_\ell A_\ell A_\ell^T.              \tag{4}
\]

Both are positive definite.  Equation (3) immediately gives

\[
 \chi_{\max}^{-1}S\preceq N\preceq\chi_{\max}S,          \tag{5}
\]

but using \(S\) alone still pays for the single worst block.  The next
theorem removes that maximum.

## Adaptive outlier theorem

Let

\[
 B_\theta=\{\ell:\chi_\ell>\theta\},\qquad
 b_\theta=|B_\theta|,
\]

and define

\[
 P_\theta=
 \sum_{\ell\in B_\theta}A_\ell H_\ell^{-1}A_\ell^T
 +\sum_{\ell\notin B_\theta}d_\ell A_\ell A_\ell^T.    \tag{6}
\]

### Theorem 1 (eccentricity-profile preconditioning)

For every \(\theta\geq1\),

\[
 \boxed{
 \theta^{-1}P_\theta\preceq N\preceq\theta P_\theta,
 \qquad
 \kappa_2(P_\theta^{-1/2}NP_\theta^{-1/2})\leq\theta^2.
 }                                                        \tag{7}
\]

Moreover,

\[
 P_\theta=S+UCU^T,\qquad
 \operatorname{rank}(UCU^T)\leq2b_\theta.                  \tag{8}
\]

where \(C\) is diagonal with signs \(+1\) and \(-1\).  Preconditioned
conjugate gradients therefore obtains

\[
 \|y_k-y_*\|_N\leq\eta\|y_0-y_*\|_N                    \tag{9}
\]

in

\[
 k=O\!\left(\theta\log{2\over\eta}\right)              \tag{10}
\]

iterations.

### Proof

For every good block \(\ell\notin B_\theta\), equation (3) says

\[
 \theta^{-1}d_\ell I\preceq H_\ell^{-1}
 \preceq\theta d_\ell I.                                \tag{11}
\]

The bad-block contribution is identical in \(N\) and \(P_\theta\).  Since
it is positive semidefinite, summing (11) gives

\[
\begin{aligned}
 N
 &\succeq \sum_{\ell\in B_\theta}N_\ell
       +\theta^{-1}\sum_{\ell\notin B_\theta}S_\ell
 \succeq\theta^{-1}P_\theta,\\
 N
 &\preceq \sum_{\ell\in B_\theta}N_\ell
       +\theta\sum_{\ell\notin B_\theta}S_\ell
 \preceq\theta P_\theta.
\end{aligned}
\]

This proves (7).  Equation (2), applied only to the bad blocks, proves (8).
The usual CG energy bound

\[
 {\|y_k-y_*\|_N\over\|y_0-y_*\|_N}
 \leq2\left({\sqrt\kappa-1\over\sqrt\kappa+1}\right)^k
\]

and \(\sqrt\kappa\leq\theta\) prove (10). \(\square\)

The same Loewner comparison provides an a posteriori certificate.  For the
normal residual \(q_k=g-Ny_k\),

\[
 \|y_k-y_*\|_N^2=q_k^TN^{-1}q_k,
\]

while (7) implies

\[
 \theta^{-1}q_k^TP_\theta^{-1}q_k
 \leq q_k^TN^{-1}q_k
 \leq\theta q_k^TP_\theta^{-1}q_k.                       \tag{12}
\]

Thus the computable preconditioned residual controls the exact Newton energy
without converting through the raw Euclidean condition number.

## Sparse-treewidth implementation

Let the structural graph of \(S\) be the row-intersection graph of \(A\): two
equality rows are adjacent when their structural supports meet in a scalar
column.  Assume a width-\(\tau\) elimination order is supplied, and put
\(\bar\tau=\tau+1\).  Every scalar column support is a clique in this graph,
hence contains at most \(\bar\tau\)
rows.  It follows that \(S\) can be assembled in

\[
 O(\bar\tau\operatorname{nnz}A)
\]

arithmetic operations and factored in \(O(m\bar\tau^2)\) work with
\(O(m\bar\tau)\) storage.  Forming all block coefficients and the selected
rank corrections also costs \(O(n+\operatorname{nnz}A)\).

Write \(q\leq2b_\theta\) for the actual correction rank in (8).  In exact
arithmetic, the Woodbury identity gives

\[
 P_\theta^{-1}=S^{-1}-S^{-1}U
 (C^{-1}+U^TS^{-1}U)^{-1}U^TS^{-1}.                       \tag{13}
\]

The small core is nonsingular because \(S\) and \(P_\theta\) are positive
definite and \(C\) is nonsingular after zero correction columns are removed.
Dense storage of the transformed correction columns gives the conservative
setup bound

\[
 O\!\left(
 n+\bar\tau\operatorname{nnz}A+m\bar\tau^2
 +mb_\theta(\bar\tau+b_\theta)+b_\theta^3
 \right),                                                \tag{14}
\]

and one application of \(P_\theta^{-1}\) costs

\[
 O\!\left(m(\bar\tau+b_\theta)+b_\theta^2\right).        \tag{15}
\]

A matrix-free product by \(N\) costs
\(O(\operatorname{nnz}A+n)\): multiply by \(A^T\), apply (2) blockwise,
and multiply by \(A\).  Combining (10), (14), and (15) proves the one-system
work bound

\[
\boxed{
 O\!\left(
 n+\bar\tau\operatorname{nnz}A+m\bar\tau^2
 +mb_\theta(\bar\tau+b_\theta)+b_\theta^3
 +\theta\log{2\over\eta}
   [\operatorname{nnz}A+n+m(\bar\tau+b_\theta)+b_\theta^2]
 \right).
}                                                         \tag{16}
\]

In particular, if the input is scalar sparse and
\(\bar\tau,\theta,b_\theta=D^{o(1)}\), where \(D=m+n\), then (16) is
\(D^{1+o(1)}\log(1/\eta)\), even if some Lorentz blocks have dimension
\(\Theta(D)\), the exact normal matrix is dense, and its raw condition number
is arbitrarily large.

There is no need to choose \(\theta\) in advance.  Sort the eccentricities as

\[
 \chi_{(1)}\geq\cdots\geq\chi_{(L)},\qquad \chi_{(L+1)}=1.
\]

For each \(b\in\{0,\ldots,L\}\), keep the top \(b\) blocks exactly and set
\(\theta_b=\chi_{(b+1)}\).  The proof of Theorem 1 only requires every
untreated block to have eccentricity at most the threshold, so the resulting
solve has bound (16) with correction count \(b\) and
\(\theta=\theta_b\).  Minimizing that explicit expression over \(b\) gives an
order-statistic Pareto envelope: the cost is controlled by the best tradeoff
between correction rank and the first untreated eccentricity, not by
\(\chi_{(1)}\) alone.  Ties cause no problem; treating some threshold-equality
blocks exactly is optional, and the number \(|B_{\theta_b}|\) may be smaller
than \(b\).

The Woodbury formula is an arithmetic identity, not a stability guarantee for
signed near-cancelling updates.  In finite precision one should instead use a
stable product-form Cholesky implementation, or state explicit growth and
working-precision assumptions.  This is precisely the numerical issue treated
by [Goldfarb and Scheinberg](https://doi.org/10.1007/s10107-004-0556-1).

### A quasidefinite alternative to the signed Woodbury core

There is a direct sparse implementation that avoids explicitly inverting the
possibly cancelling small matrix in (13).  Absorb the magnitudes of the bad
blocks' positive and negative rank-one corrections into matrices \(U,V\), so

\[
 P_\theta=S+UU^T-VV^T.                                  \tag{16a}
\]

The intermediate downdate is still positive definite:

\[
 S-VV^T
 =\sum_{\ell\notin B_\theta}d_\ell A_\ell A_\ell^T
  +\sum_{\ell\in B_\theta}
   A_\ell\!\left(d_\ell I-r_\ell(t_\ell-r_\ell)
          u_{\ell,-}u_{\ell,-}^T\right)\!A_\ell^T
 \succ0.                                                 \tag{16b}
\]

Indeed, each matrix in parentheses has eigenvalue
\((t_\ell-r_\ell)^2/2>0\) on \(u_{\ell,-}\) and eigenvalue
\(d_\ell>0\) on its orthogonal complement; full row rank of \(A\) makes the
sum positive definite.  Consequently

\[
 \mathcal P_\theta=
 \begin{bmatrix}
 S&V&U\\ V^T&I&0\\ U^T&0&-I
 \end{bmatrix}                                           \tag{16c}
\]

is symmetric quasidefinite, and eliminating the two hub groups gives
\(P_\theta\).

Insert all at most \(2b_\theta\) hub vertices into every bag of the supplied
width-\(\tau\) decomposition of the graph of \(S\).  This covers every
hub--row edge and gives an expanded width at most
\(\tau+2b_\theta\).  Strong factorability of a symmetric quasidefinite matrix
then gives a pivot-free factorization in

\[
 O\!\left((m+b_\theta)(\bar\tau+2b_\theta)^2\right)       \tag{16d}
\]

arithmetic, with \(O((m+b_\theta)(\bar\tau+2b_\theta))\)
factor storage and triangular-solve work.  This is an alternative to the
Woodbury terms in (14)--(15), so the better of the two implementations may be
used in (16).  It removes a separate signed small-core inversion and exact
zero-pivot breakdown.  It still does not by itself prove a dimension-free
finite-precision bit bound; scaling, element growth, and refinement remain
part of that ledger.

## Exact relation to the primal Newton metric

Consider the equality-constrained Newton equations

\[
 H\Delta x+A^T\Delta y=r_d,\qquad A\Delta x=r_p.          \tag{17}
\]

Elimination yields

\[
 N\Delta y=AH^{-1}r_d-r_p,
 \qquad
 \Delta x=H^{-1}(r_d-A^T\Delta y).                        \tag{18}
\]

If \(e_y=\widehat{\Delta y}-\Delta y\), then the induced primal error is
\(e_x=-H^{-1}A^Te_y\), and therefore

\[
 \boxed{\|e_x\|_H^2=e_y^TNe_y=\|e_y\|_N^2.}              \tag{19}
\]

The PCG energy guarantee is exactly the local barrier-metric error of the
induced primal correction.  No factor \(\kappa_2(N)\) is lost in this
translation.

## A rank lower bound for this preconditioner class

The dependence on the number of eccentric blocks is not only an artifact of
the construction.

### Theorem 2 (the rank-two charge per outlier is worst-case sharp)

For every \(b\geq1\), \(\theta\geq1\), and \(\chi>\theta^2\), there is a
product of \(b\) genuine three-dimensional Lorentz blocks whose base normal
matrix is \(S=I_{3b}\), hence has treewidth zero, and whose exact normal
matrix has orthogonal eigenvectors

\[
 N u_{\ell,+}=\chi u_{\ell,+},\quad
 N u_{\ell,0}=u_{\ell,0},\quad
 N u_{\ell,-}=\chi^{-1}u_{\ell,-}.                       \tag{20}
\]

If \(P=I+R\succ0\), \(R=R^T\), and \(\operatorname{rank}R<2b\), then

\[
 \boxed{\kappa_2(P^{-1/2}NP^{-1/2})\geq\chi>\theta^2.}    \tag{21}
\]

Consequently any base-plus-low-rank preconditioner that guarantees condition
at most \(\theta^2\) on every profile needs rank at least \(2b\) on some
profile with \(b\) outliers.  The rank-\(2b\) construction (8) is therefore
worst-case rank-optimal.

### Proof

Choose each interior cone point so that \(d_\ell=1\) and its eccentricity is
\(\chi\); explicitly,

\[
 t_\ell+r_\ell=\sqrt{2\chi},\qquad
 t_\ell-r_\ell=\sqrt{2/\chi}.
\]

Take \(A=I_{3L}\).  Equations (3)--(4) give (20) and \(S=I\).

Let \(E_+\), \(E_0\), and \(E_-\) be the three \(b\)-dimensional eigenspaces
in (20), and let \(p\) and \(q\) be the positive and negative inertia of
\(R\).  If \(p<b\), the restriction of \(R\) to \(E_+\) is not positive
definite.  Hence some nonzero \(v\in E_+\) has \(v^TRv\leq0\), and

\[
 {v^TNv\over v^TPv}\geq\chi.                             \tag{22}
\]

Because \(\operatorname{rank}R<2b\), dimension counting also gives a nonzero
\(w\in\ker R\cap E_+^\perp\).  On \(E_0\oplus E_-\), \(N\preceq I\), so
the Rayleigh quotient at \(w\) is at most one.  Thus the generalized
condition number is at least \(\chi\).

If instead \(p\geq b\), then \(q<b\), since
\(p+q=\operatorname{rank}R<2b\).  The restriction of \(R\) to \(E_-\) is
not negative definite, so some nonzero \(v\in E_-\) has \(v^TRv\geq0\) and
generalized Rayleigh quotient at most \(\chi^{-1}\).  Dimension counting
gives a nonzero \(w\in\ker R\cap E_-^\perp\); on
\(E_+\oplus E_0\), \(N\succeq I\), so its quotient is at least one.  Again
the condition number is at least \(\chi\).  This proves (21). \(\square\)

There is also a profile-wise sharp statement for the stronger Loewner
contract in (7).  If \(b_\theta\) blocks have \(\chi_\ell>\theta\) and a
preconditioner \(P=I+R\) satisfies
\(\theta^{-1}P\preceq N\preceq\theta P\), restriction to the high and low
eigenspaces forces at least \(b_\theta\) positive and \(b_\theta\) negative
directions in the update.  Its rank is therefore at least
\(2b_\theta\), exactly matching (8).

The witness is a legitimate SOCP normal system, though it is intended as a
linear-algebra lower bound, not as an end-to-end optimization query lower
bound.

## Dense, ill-conditioned, width-zero example

The simplest instance makes the QIPM comparison vivid.  Take one Lorentz
block of dimension \(D\), \(A=I_D\), \(d=1\), and choose a dense radial
direction \(z/\|z\|\).  Then

\[
 S=I_D,\qquad
 N=I_D+a u_+u_+^T-c u_-u_-^T,qquad
 \kappa_2(N)=\chi^2.                                     \tag{23}
\]

The exact normal matrix is generically dense and \(\chi\) can be arbitrarily
large, yet \(b_1=1\) and a rank-two Woodbury or product-form solve takes
\(O(D)\) arithmetic.  Hence a QIPM runtime stated only through the raw
condition number and sparsity of the assembled exact normal matrix can be
arbitrarily pessimistic relative to the matched classical structured solve.

## QIPM consequence and scope

Suppose that along a \(T\)-step SOCP trajectory:

- the structural graph of every scalar base matrix \(S_t\) has a supplied
  width-\(\tau_t\) order;
- current cone coordinates and entries of \(A\) are classically evaluable at
  the precision charged to the quantum oracles;
- at thresholds \(\theta_t\), only \(b_t\) blocks are more eccentric; and
- the outer inexact-IPM theorem accepts the \(H_t\)-local/normal-energy error
  in (19), or the certified preconditioned-residual contract in (12); and
- the hybrid QIPM materializes the classical primal and multiplier updates
  before constructing the next Newton system.

Applying (16) at every iteration gives a classical trajectory with the same
accepted local-metric solve tolerances.  If
\(\tau_t+1,\theta_t,b_t=D^{o(1)}\), its total Newton work is
\(T D^{1+o(1)}\) up to accuracy logarithms.  The materialized hybrid updates
already require \(\Omega(TD)\) word operations.  Thus the QLSA replacement
cannot yield a polynomial total-work advantage on this profile class.

This conclusion does **not** cover quantum-state, sample, scalar-observable,
or implicit-iterate output.  It also does not give a finite-precision bit
bound without a stable update implementation, and it does not assert that
\(b_t\) remains small on every SOCP central path.  The energy and
\(P^{-1}\)-residual contracts above also must not be silently replaced by an
ordinary Euclidean or full-KKT residual: that conversion needs additional
spectral bounds and, in finite precision, a backward-error analysis.
The eccentricities and the base graph are representation-dependent as well:
a Lorentz automorphism can reduce a block eccentricity while transforming
the corresponding columns of \(A\), thereby changing entry access,
normalization, and sparsity.  The theorem is an algorithmic guarantee in the
fixed coordinates supplied to the solver, not a coordinate-invariant lower
bound or condition measure.

The theorem is complementary to the few-cone Lorentz SQ sampler.  That result
handles weak output with a cost exponential in a sparse-base polynomial
degree and assumes a fixed number of cones.  The present theorem allows an
arbitrary number and arbitrary dimensions of cones, uses a different
eccentricity-profile parameter, and proves near-linear **explicit** Newton
solves plus a matching low-rank obstruction.

It is also complementary to the
[latent-treewidth Lorentz theorem](2026-09-04-latent-treewidth-lorentz-newton-systems.md).
Let \(\mathcal C_{\rm prof}\) denote the best order-statistic bound obtained
by minimizing (16) over \(b\), and let

\[
 \mathcal C_{\rm latent}
 =O\!\left((n+m+L)(\tau_{\rm L}+1)^2\right).             \tag{23a}
\]

The same Newton system therefore has the unified exact-arithmetic envelope

\[
 \boxed{\mathcal C_{\rm Newton}
        \leq\min\{\mathcal C_{\rm prof},
                   \mathcal C_{\rm latent}\}.}          \tag{23b}
\]

The two arms cover different structure.  The profile arm allows large latent
treewidth when only a few blocks are eccentric; the latent-width arm allows
arbitrarily many eccentric blocks.  Subject to the same access and output
scope, a proposed polynomial QLSA speedup must evade both classical arms, not
merely exhibit a dense or ill-conditioned assembled normal matrix.

## Literature boundary

The block identity (2), sparse-plus-rank-two normal form, and product-form
factorization are classical; see the
[Alizadeh--Goldfarb SOCP survey](https://doi.org/10.1007/s10107-002-0339-5)
and [Goldfarb--Scheinberg](https://doi.org/10.1007/s10107-004-0556-1).
Existing implementations already distinguish large cones and handle their
dense rank corrections specially.  Kobayashi, Kim, and Kojima study how SOCP
formulations change Schur-complement sparsity and report a size threshold for
large-cone handling
[[JORSJ 51 (2008), 241--264](https://doi.org/10.15807/jorsj.51.241)].

A targeted search found no source proving the adaptive *eccentricity*
threshold (7), its treewidth-parametric cost (16), the low-rank necessity
theorem (21), or the resulting raw-condition-number mirage and matched-access
QIPM exclusion.  Those statements, rather than the rank-two algebra itself,
are the defensible apparent novelty.  Priority is not guaranteed.
