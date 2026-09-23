# Hostile audit of prefix rigidification

This note audits `2026-09-02-prefix-rigidified-condition-one-newton-hardness.md`.

## Verdict

The augmentation is correct in the stated raw coefficient-query model.  The
\(T\) public rows remove exactly the \(T\) small-height null modes, preserve the
hidden parity differences, and leave both the entire central-path reduced Hessian
and the infeasible-start reduced Newton coefficient exactly scalar in the raw
orthonormal null basis.  The robust approximate-feasibility lower bound and all LP
regularity properties survive.

The essential caveat is an access distinction: a scalar reduced coefficient does
not prepare the hidden reduced right-hand side, construct the affine feasibility
correction, or load the answer into original coordinates.  No condition claim is
made for the full KKT or equality-normal matrix.

## Rank, kernel, and sparsity

Before augmentation, the orthonormal null columns are

\[
 W_i=\sqrt{\frac23}
 \left(\frac12e_{u_i}+\frac12e_{v_i}-e_{t_i}\right).
\]

The rigidification row at prefix node \(i<T\) is

\[
 r_i=e_{u_i}+e_{v_i}-\frac54e_{h_i}.
\]

Its restriction to the old kernel is diagonal:

\[
 \langle r_i,W_j\rangle=\sqrt{\frac23}\,\delta_{ij}.       \tag{1}
\]

Thus the new rows are independent modulo the old row space and kill precisely
\(W_0,\ldots,W_{T-1}\).  Since the old nullity is \(P\),

\[
 \operatorname{rank}A'=3P+T,qquad
 \ker A'=\operatorname{span}\{W_i:i\ge T\}.                \tag{2}
\]

Each new row has three nonzeros and coefficient magnitude at most \(5/4\).  It
adds one incidence to an affected \(u,v,h\) column, raising the maximum column
count from three to four.  Row sparsity remains at most four.  The new support and
values are input-independent.

## Feasible set and regularity

The new row fixes only

\[
 q_i=\frac54H_i\qquad(i<T),                                \tag{3}
\]

while the signed propagation equations still fix
\(d_i=H_i\tau_i\).  It therefore does not reveal or constrain the hidden pair
orientation.  At a prefix optimum all four variables are positive, with pair
values \(9H_i/8,H_i/8\).  At each free optimum exactly three variables are
positive.  The total number of positive variables is

\[
 4T+3(P-T)=3P+T,
\]

matching the row rank.

Any null vector supported on these positive columns is, by (2),
\(\sum_{i\ge T}\alpha_iW_i\).  At free node \(i\), the coefficient on its zero
pair member is nonzero unless \(\alpha_i=0\).  Hence every coefficient vanishes,
and the positive columns form a basis.  Increasing a free \(q_i\) by
\(\epsilon\) activates the zero pair member by \(\epsilon/2\) and increases the
objective by \(w\epsilon\), so its reduced cost is \(2w>0\).  This verifies
primal and dual nondegeneracy and strict complementarity.

The displayed central point is strictly primal feasible.  With
\(s^1=\mu_1/x^1\), dual stationarity need only hold against the surviving kernel
(2).  Every surviving node has the common height \(H\), and the scalar
stationarity equation supplies exactly this condition.  Therefore
\(c-s^1\in\operatorname{range}(A'^T)\), giving a strictly positive dual-feasible
slack.  This verifies strict primal-dual feasibility without imposing an omitted
prefix stationarity equation.

## Exact conditioning

At every central parameter \(\mu>0\), all surviving nodes have the same height
\(H\), objective slope \(w\), scalar central coordinate, and local curvature.
Because the surviving \(W_i\)'s are orthonormal, the complete reduced Hessian is

\[
 W^T\nabla^2F_\mu(x(\mu))W=\lambda(\mu)I_{P-T}.             \tag{4}
\]

This proves raw orthonormal condition number one on the entire central path, not
merely at \(\mu_1\).

At the public start,

\[
 \frac{s_u^0}{x_u^0}=\frac{s_v^0}{x_v^0}
 =\frac4{9H_i^2},qquad
 \frac{s_t^0}{x_t^0}=\frac1{H_i^2}.
\]

The squared \(u,v,t\) components of \(W_i\) are \(1/6,1/6,2/3\), so

\[
 W_i^T(X^0)^{-1}S^0W_i
 =\frac{22}{27H_i^2}.                                     \tag{5}
\]

Only \(i\ge T\) survive and every such \(H_i=H\).  Hence the start reduced
coefficient is exactly

\[
 \frac{22}{27H^2}I_{P-T}.                                 \tag{6}
\]

This remains the correct reduced coefficient at an infeasible start: write the
primal correction as any particular solution of its feasibility equation plus
\(Wz\), then project the eliminated dual equation with \(W^T\).

The cross-term identities and endpoint equations in the source note then prove
the unique full Newton correction.  The augmentation changes neither the endpoint
nor the complementarity calculation; it only adds public primal equations that
the endpoint satisfies.

## Robust lower bound

All new right-hand-side entries are zero.  Therefore

\[
 \|b'\|_2=\|b\|_2=\sqrt2
\]

and the residual decomposes as

\[
 \|A'x-b'\|_2^2
 =\|Ax-b\|_2^2+
 \sum_{i<T}|q_i-\tfrac54h_i|^2.                            \tag{7}
\]

The augmented relative-residual promise implies the old promise with exactly the
same constant.  The base gain--plateau decoder consequently applies to every
admissible nonnegative vector without modification.  No right-hand-side norm
dilution occurs.

The \(16N\) output nodes all lie in the unmodified plateau, so the direction-state
signal and normalization estimate are unchanged.  A query to a new row is wholly
public, while a query to an old row exposes at most one hidden sign.  Thus the
coherent oracle simulation still uses at most one sign query per LP query, and
both state lower bounds remain \(\Omega(N)=\Omega(P)\).

## Interpretation

The construction genuinely escapes the centered-start incompatibility for the
unaugmented four-variable product: instead of trying to equalize small-height
curvatures, it removes those feasible directions using only \(O(\log N)\) public
equalities.  This retains linear size and bounded row and column degree.

Condition one describes the reduced coefficient matrix.  Forming a particular
correction for

\[
 A'\Delta x=b'-A'x^0,
\]

forming its reduced right-hand side, and loading or recovering the
original-variable state still depend on the hidden signs.  The result is therefore
an affine-loading/right-hand-side access separation, not a condition-number lower
bound for a supplied scalar QLS.

Direct numerical checks at \(N=2,4,8,16,32\) confirmed rank \(3P+T\),
\(A'W=0\), endpoint dual stationarity to floating-point precision, and equality
of every start reduced eigenvalue with \(22/(27H^2)\).

Status: **hostile algebraic audit passed.**
