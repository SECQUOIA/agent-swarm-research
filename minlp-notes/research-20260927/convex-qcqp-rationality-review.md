# Independent review: rationality for convex quadratic feasibility

The proposed irrational singleton, the obstruction to rational aggregation,
and the variant using three positive definite quadratic inequalities are
correct. The proposed lift also establishes rational feasible witnesses when
the PSD Hessians span at most one dimension. These arguments do not classify
the case of Hessian span two.

I checked these statements against the completed
[main note](convex-qcqp-rationality-boundary.md), including its mixed-integer
clause and its limits on the meaning of the aggregation obstruction.

## The irrational singleton

Let \(r=\sqrt[3]{2}\), \(p=(r,r^2)\), and
\[
q_1=x^2-y,\qquad q_2=y^2-2x,\qquad
q_3=(x-y)^2-2x-y+4.
\]
All three polynomials have rational coefficients and PSD Hessians of rank
one. They vanish at \(p\): the only less immediate substitution is
\[
q_3(p)=r^2-2r^3+r^4-2r-r^2+4=0.
\]

For the positive weights
\[
\lambda=(2r-1,r^2-1,1),
\]
direct expansion gives
\[
\sum_i\lambda_iq_i(z)
=(z-p)^\top M(z-p),\qquad
M=\begin{pmatrix}2r&-1\\-1&r^2\end{pmatrix}.
\]
Indeed, \(Mp=(r^2,r)\), \(p^\top Mp=4\), and
\(\det M=2r^3-1=3\). Thus \(M\) is positive definite. A feasible point
makes the aggregate nonpositive, so it must be \(p\). The unbounded-domain
system already has feasible set \(\{p\}\); no box constraints are needed.
Its affine hull contains no rational point.

The quadratic-part matrices of the three rows are linearly independent in
\(\operatorname{Sym}_2\), so the native Hessian span is exactly three.

## No nonzero rational aggregate is globally nonnegative

The claim holds even if the rational weights have arbitrary signs. Suppose
\(\alpha\in\mathbb Q^3\) and
\(g=\sum_i\alpha_iq_i\) is globally nonnegative. Since all rows vanish at
\(p\), this point is a global minimizer of \(g\), and hence
\(\nabla g(p)=0\). Its first gradient coordinate yields
\[
0=\tfrac12\partial_xg(p)
=(\alpha_1+\alpha_3)r-\alpha_3r^2-(\alpha_2+\alpha_3).
\]
The numbers \(1,r,r^2\) are linearly independent over \(\mathbb Q\), since
\(t^3-2\) is irreducible over \(\mathbb Q\). Consequently
\(\alpha_3=0\), \(\alpha_1+\alpha_3=0\), and
\(\alpha_2+\alpha_3=0\), so \(\alpha=0\).

Thus this example has a strictly positive algebraic aggregation certificate
but no nonzero rational nonnegative aggregation certificate. No claim about
all possible certificate systems follows from this particular obstruction.

## Three proper ellipsoids give the same singleton

Define
\[
R_i=3q_i+q_1+q_2+q_3\qquad(i=1,2,3).
\]
Writing a quadratic as \(z^\top B_i z+\text{affine}\), its quadratic-part
matrices are
\[
B_1=\begin{pmatrix}5&-1\\-1&2\end{pmatrix},\quad
B_2=\begin{pmatrix}2&-1\\-1&5\end{pmatrix},\quad
B_3=\begin{pmatrix}5&-4\\-4&5\end{pmatrix}.
\]
Each has determinant nine and a positive first diagonal entry. Hence every
\(R_i\) has a positive definite Hessian. Each set \(R_i\le0\) is a compact,
full-dimensional ellipsoid: its unique quadratic minimizer is rational,
whereas the irrational point \(p\) lies on its zero level. Thus its minimum
is strictly negative.

Completing the squares gives centers
\((13/18,29/18)\), \((26/9,7/9)\), and \((35/9,65/18)\). The minimum
values are \(-53/36\), \(-101/9\), and \(-449/36\), respectively, as
reported in the main note.

Set
\[
S=\sum_i\lambda_i=2r+r^2-1,\qquad
\eta_i=\frac{\lambda_i-S/6}{3}.
\]
Since \(\sum_i\eta_i=S/6\), the coefficient of \(q_i\) in
\(\sum_j\eta_jR_j\) is \(3\eta_i+S/6=\lambda_i\). Therefore
\[
\sum_i\eta_iR_i=\sum_i\lambda_iq_i=(z-p)^\top M(z-p).
\]

All three new weights are strictly positive. Their numerators are
\[
18\eta_1=10r-r^2-5,\qquad
18\eta_2=5r^2-2r-5,\qquad
18\eta_3=7-2r-r^2.
\]
The bounds \(5/4<r<4/3\) follow by cubing. On this interval the first two
numerators increase, while the third decreases. Their respective lower
bounds, obtained at the appropriate endpoints, are
\(95/16\), \(5/16\), and \(23/9\). Thus the same positive definite
aggregate proves
\[
\bigcap_{i=1}^3\{R_i\le0\}=\{p\}.
\]

The row transformation is \(3I+\mathbf1\mathbf1^\top\), which has
eigenvalues \(6,3,3\) and is invertible over \(\mathbb Q\). The Hessian
span remains three. The obstruction to nonzero rational globally
nonnegative aggregates also transfers to these rows.

## Hessian span at most one admits rational feasible witnesses

If all Hessians vanish, the feasible set is a rational polyhedron. Otherwise,
suppose their span has dimension one and choose a nonzero input Hessian
\(Q\succeq0\). Every quadratic row can be written
\[
q_i(x)=\gamma_i\tfrac12x^\top Qx+a_i^\top x+c_i,
\qquad \gamma_i\in\mathbb Q_{\ge0}.
\]
The scalar is rational because it is the ratio of corresponding rational
matrix entries, using any nonzero entry of \(Q\). It is nonnegative because
both the row Hessian and \(Q\) are PSD and \(Q\ne0\).

Introduce one real variable \(t\) and impose
\[
\tfrac12x^\top Qx-t\le0,\qquad
\gamma_i t+a_i^\top x+c_i\le0\quad\text{for every }i,
\]
along with the original affine rows. For every original feasible \(x\),
choosing \(t=\tfrac12x^\top Qx\) gives a lifted feasible point. Conversely,
\(\gamma_i\ge0\) implies that every lifted feasible point projects to an
original feasible point. The lift preserves rationality in both directions.

This is one rational quadratic inequality plus rational affine constraints.
The polynomial-size rational feasible-witness theorem for one quadratic
inequality therefore applies. The lift has polynomial encoding size: it adds
one variable and one quadratic row, and the scalars \(\gamma_i\) are ratios
of input entries. Hence every nonempty instance in this PSD span-one class
has a rational feasible point of polynomial encoding length.

The mixed-integer clause in the main note is also valid. When the **full**
input Hessians are PSD and span at most one dimension, the same lift retains
every original integrality restriction and makes only the new variable
\(t\) continuous. Del Pia, Dey, and Molinaro's theorem applies directly and
gives a feasible witness of polynomial encoding length with the required
integer coordinates. The span-zero case is included by treating the affine
system as having one redundant quadratic inequality. A bound only on the
continuous Hessian blocks would not give the displayed full-polynomial
decomposition, so that weaker premise does not support this reduction.

For the source claim, I checked Theorem 1 and Section 2.2, Theorem 3, of
[Del Pia, Dey, and Molinaro, *Mixed-integer quadratic programming is in
NP*](https://arxiv.org/abs/1407.4798), using the
[local extracted text](nonconvex-prior-sources/del-pia-dey-molinaro-2014.txt).
Section 2.2 explicitly identifies the continuous case and attributes it to
Vavasis. The mixed-integer theorem also covers the continuous conclusion by
adding one integer variable fixed to zero, if a positive integer-variable
count is required by the theorem's notation. I did not independently read
Vavasis's 1990 paper in this review.

The main note's Proposition 2 deliberately states only the nonnegative-weight
case; its proof is valid. Its conclusion about an exposing aggregate with
minimum zero is appropriately limited. It does not rule out rational
infeasibility certificates with a positive margin, or rational descriptions
of algebraic certificates. I did not repeat the main note's prior-art
search, and this review makes no publication-priority claim.

These are existence and encoding-length statements for feasible witnesses.
They do not assert rationality of every feasible point or of an arbitrary
optimization problem's optimizer. The span-three counterexample and the
span-one theorem leave span two unresolved by this review.

## Targeted verification

I ran one inline `python - <<'PY' ... PY` command using SymPy. It reduced
polynomial identities modulo \(r^3-2\) and checked the three original
residuals, the completed-square identity, \(\det M=3\), all three new
quadratic-part matrices and determinants, the transformed aggregation
weights, the three endpoint bounds, and the rational-gradient coefficients.
All assertions passed. The positivity arguments and the span-one lift were
also checked directly above. No project-wide verification or CI inspection
was performed.
