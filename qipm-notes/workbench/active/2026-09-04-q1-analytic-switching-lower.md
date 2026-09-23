# Analytic continuation closes the exceptional PSD cap

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the proof; priority not established

## Result

Let \(s\geq3\), \(b\geq2\), and consider the exceptional real-PSD cap
\(R=s\) for the full extreme slack of \((B_2^s)^b\).  Assume the globally
labelled primal and dual PSD factors are real analytic.  Assume also that
the entire selected primal boundary family indexed by
\(M=(S^{s-1})^b\) belongs to the closure of the strictly feasible affine
slice carrying the restricted standard product log-determinant.  Then

\[
 \boxed{\displaystyle
   \left\lfloor\nu_{\rm std,slice}\right\rfloor\geq2b.}   \tag{1}
\]

The grouped Schur lift attains \(2b\), so the analytic optimum is exact.
This is a formulation/barrier theorem, not an iteration lower bound.

A later sequential range-compression theorem proves the same bound under
the weaker globally bi-\(C^1\) hypothesis.  The present proof is retained
because it exposes a different rigidity mechanism: a hypothetical
sub-\(2b\) analytic factorization would have to generate a fixed positive
batch of globally persistent projective labels in every round.

## 1. Analytic saturation-extraction lemma

At a simultaneous contact \(x\in M\), write

\[
 Z(x)=\sum_i\operatorname {nullity}X_i(x)
\]

and let \(D_d(x)\) be the total private dual-range dimension assigned to
row \(d\).  The determinant vanishing-order lemma and private-curvature
inequalities give

\[
 1\leq D_d(x),\qquad \sum_{d=1}^bD_d(x)\leq Z(x)
 \leq N:=\left\lfloor\nu_{\rm std,slice}\right\rfloor.   \tag{2}
\]

Suppose a current analytic factorization still represents the full ball
slack in row \(d\), and \(D_d=1\) on a nonempty connected common generic
rank stratum \(\Omega\).  Such strata exist by intersecting the open dense
maximal-rank loci of the finitely many analytic matrices \(X_i\) and all
PSD row-subset sums used to compute the private quotient dimensions.

Equality throughout the row-curvature chain forces one fixed current
label \(i_d\) such that, on \(\Omega\),

\[
 H_{i_d}^d=g_d,\qquad H_i^d=0\ (i\ne i_d),               \tag{3}
\]

and

\[
 r_{i_d}=s,\qquad
 \operatorname {rank}X_{i_d}=s-1,\qquad
 \operatorname {rank}Y_{i_d}^d=1.                       \tag{4}
\]

The curvature tensors are analytic, so (3) extends to connected \(M\).
The projection of \(\Omega\) to the \(d\)-th sphere is nonempty open.
Every \(2\)-by-\(2\) minor of the one-variable analytic matrix
\(Y_{i_d}^d\) therefore vanishes globally.  This matrix cannot vanish at
a point: a two-sided differentiable PSD map has zero derivative at a zero
value, which would make its mixed-curvature channel zero, contrary to
(3).  Hence its rank is one everywhere.  Complementarity and

\[
 \operatorname {rank}H_{i_d}^d
 \leq \operatorname {rank}X_{i_d}
       \operatorname {rank}Y_{i_d}^d
\]

force \(X_{i_d}\) to have rank \(s-1\) and nullity one everywhere.

Let \(L_d:S^{s-1}\to\mathbb {RP}^{s-1}\) be the projective dual range.
Its differential has full rank by (3), so it is the universal double
cover.  Locally write
\(Y_{i_d}^d(u)=\lambda_d(u)q_d(u)q_d(u)^T\), with
\(\lambda_d>0\).  The curvature identity is

\[
 \langle h,k\rangle
   =2\lambda_d(u)
      \left\langle dq_d(u)k,
       X_{i_d}(x)dq_d(u)h\right\rangle.                  \tag{5}
\]

Because \(dq_d:T_uS^{s-1}\to q_d(u)^\perp\) is an isomorphism, (5)
determines \(X_{i_d}|_{q_d(u)^\perp}\) from \(u=x_d\).  Its kernel is
\(\mathbb Rq_d(u)\), so the entire primal matrix depends only on \(x_d\).
Independent variation of the other coordinates and surjectivity of
\(L_d\) give

\[
                        Y_{i_d}^e\equiv0\qquad(e\ne d).  \tag{6}
\]

Thus saturation on one generic analytic stratum yields a globally
persistent, cylindrical, nullity-one projective label.  Labels extracted
from distinct rows are distinct.

## 2. Residual ranges have an independent transversal

Remove any \(k\) persistent labels.  Each removed row leaves a
nonnegative cylindrical residual \(F_d(u,v)\) with

\[
 F_d(u,u)=0,qquad F_d(u,\tau_d(u))>0,                   \tag{7}
\]

where \(\tau_d\) is the deck involution of \(L_d\).  Every unremoved row
still has its full slack \(1-u^Tv\), with the antipodal involution.  Call
the PSD factors left after deletion the current factors.

We use a strengthened intermediate conclusion of the audited
orientation-residual theorem.  The global current dual-range sets of any
collection of \(k\) residual rows admit an independent transversal.  If
not, Rado's theorem supplies a nonempty deficient subset of \(r\) rows
whose total dual-range span has dimension at most \(r-1\).  The block-span
bound makes its ordinary column rank at most

\[
                              {s+1\over2}(r-1),           \tag{8}
\]

whereas Borsuk--Ulam and coordinate independence give
\(1+r(s-1)\).  This contradicts

\[
 2[1+r(s-1)]-(s+1)(r-1)=s+3+r(s-3)>0.                  \tag{9}
\]

Choose one independent dual-range vector per residual row.  Each vector
is a fixed linear combination of columns of the corresponding dual
matrices at the chosen source point.  Use the same combinations nearby
and select a nonzero \(k\)-by-\(k\) coordinate minor.  This minor is a
nonzero analytic function on the connected source-coordinate product, so
its nonvanishing locus is open dense.  Consequently, on a nonempty common
generic stratum,

\[
                     \dim W_{\rm res}\geq k,             \tag{10}
\]

where \(W_{\rm res}\) is the sum of current dual ranges of the already
extracted residual rows.  This conclusion does not use a nullity bound.

## 3. Bootstrap to all rows

Suppose for contradiction that \(N<2b\), and put

\[
                              j=2b-N>0.                  \tag{11}
\]

Assume \(k\) persistent labels have already been removed.  There are
\(f=b-k\) unremoved full-slack rows.  The removed labels each have nullity
one at every contact, so

\[
                              Z_{\rm cur}(x)\leq N-k.     \tag{12}
\]

Choose a common generic stratum on which (10) holds and all current
private dimensions \(D_e\) of the full rows are constant.  Work in the
block direct-sum dual space.  For every full row choose

\[
 P_e\subset U_e,\qquad
 U_e=P_e\oplus(U_e\cap U_{-e}),\qquad \dim P_e=D_e,       \tag{13}
\]

where \(U_{-e}\) is the sum of every other current row range, including
the residual rows.  Then

\[
                    W_{\rm res}\oplus\bigoplus_eP_e      \tag{14}
\]

is direct.  Indeed, in a relation \(w+\sum_ep_e=0\), solving for one
\(p_e\) puts it in both \(P_e\) and \(U_{-e}\), so \(p_e=0\).  Repeat
for every \(e\), then \(w=0\).

At simultaneous contact all spaces in (14) lie in the kernel of the
block-diagonal current primal matrix.  Equations (10), (12), and (14)
give

\[
 k+\sum_{e\ \operatorname{full}}D_e\leq Z_{\rm cur}\leq N-k,
 \qquad
 \sum_{e\ \operatorname{full}}D_e\leq N-2k.            \tag{15}
\]

Every full row has \(D_e\geq1\).  If \(n_1\) of the \(f\) full rows have
\(D_e=1\), then

\[
 N-2k\geq\sum_eD_e\geq n_1+2(f-n_1),
\]

and hence

\[
                           n_1\geq2f-(N-2k)=2b-N=j.       \tag{16}
\]

If fewer than \(j\) full rows remain, (16) is already a contradiction.
Otherwise Section 1 globalizes at least \(j\) new persistent labels.
Delete exactly \(j\) of them and repeat.  Equation (6) leaves every other
full row unchanged and prevents later deletions from altering old
residual rows.

The iteration increases \(k\) by the fixed positive integer \(j\).  It
cannot stop before all rows are extracted, by (16).  If all \(b\) rows
are extracted, the current factorization consists of \(b\) cylindrical
deck-separating residual rows and has nullity at most \(N-b<b\), contrary
to the orientation-residual theorem's nullity lower bound \(b\).  Thus
\(N<2b\) is impossible, proving (1).

## Scope and relation to the final frontier

Analyticity is used to choose common generic maximal-rank strata and to
continue saturated curvature identities and rank-one minors globally.
The proof should extend to a quasianalytic class with the corresponding
identity property, but no such extension is claimed here.

This continuation argument does not handle arbitrary globally \(C^1\)
switching.  The companion
[sequential range-compression theorem](2026-09-04-q1-sequential-range-compression-closure.md)
does: it successively quotients already fixed contact ranges and proves the
same \(2b\) result in the weaker bi-\(C^1\) class.

A targeted literature search has not found this analytic bootstrap, but
priority and novelty remain subject to specialist review.

## Independent hostile audit

The auditor verified that the orientation-residual proof yields an
independent transversal for every residual-row subcollection without a
nullity hypothesis.  Fixed column combinations realizing one transversal
give a nonzero analytic minor, so (10) holds on an open dense locus.

The audit also checked (14) blockwise.  Each private component in a
putative relation belongs both to its chosen complement and to the sum of
all other row spaces, hence vanishes.  All surviving spaces lie in the
current primal kernel.  This establishes (15), the invariant count (16),
and finite termination.  Finally, every new persistent label has zero
cross-row duals, so deletion preserves all old residuals and all other
full slacks.  No substantive correction was needed.

## Audit checklist

- Preserve the whole-boundary-family closure hypothesis when deriving
  \(Z(x)\leq N\) for every contact.
- Recheck the independent-transversal consequence without a nullity
  assumption and the analytic-minor step.
- Check that every private complement in (13) is relative to all other
  current rows, including the residual rows.
- Check the invariant batch size \(j=2b-N\) and finite termination.
- Preserve the global labels, real analyticity, cap \(R=s\), and
  restricted-standard-barrier scope.
