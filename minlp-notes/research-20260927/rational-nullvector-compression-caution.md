# A rational nullvector of one feasible matrix does not preserve rational feasibility

Date: 2026-09-28. Status: exact counterexample, independently reconstructed
by two agents. This is a caution about the hypotheses needed for a
facial restriction, not a new general obstruction theorem.

The online manuscript of Burgdorf, Klep, and Povh, printed pages
44--46, describes compression along a rational nullvector of a
singular feasible matrix. Its printed Theorem 1.81(ii) asserts
equivalence of rational feasibility before and after that compression.
Read with the stated preceding setup, the assertion needs an additional
hypothesis. The following example explains the issue.
[Inspected primary manuscript](https://igorklep.codeberg.page/files/Sosh_book_rev1_submitted.pdf).

Use the manuscript's Example 1.79 pencil
\[
 A(x)=
 \begin{pmatrix}2&x\\x&1\end{pmatrix}
 \mathbin{\oplus}
 \begin{pmatrix}x&1&0\\1&x&1\\0&1&x\end{pmatrix}.
 \tag{1}
\]
The first block is PSD exactly when \(|x|\le\sqrt2\); the second
has eigenvalues \(x-\sqrt2,x,x+\sqrt2\) and is PSD exactly when
\(x\ge\sqrt2\). Hence \(A(x)\succeq0\) exactly at \(x=\sqrt2\).

Now form the rational affine family of symmetric six-by-six matrices
\[
 X(t,x)=\operatorname{diag}\bigl(t,A(x)+tI_5\bigr).
 \tag{2}
\]
This can be expressed by rational affine equations on a matrix
variable, followed by a PSD constraint. It contains the rational
positive definite matrix \(X(2,0)\): its block eigenvalues are
\(2,4,3,2-\sqrt2,2,2+\sqrt2\).

The feasible matrix \(G_0=X(0,\sqrt2)\) has the rational nullvector
\(e_1\). Restricting the affine family to matrices that kill \(e_1\)
forces \(t=0\). Its remaining PSD constraint is \(A(x)\succeq0\),
which forces \(x=\sqrt2\). The restricted family is real feasible
but has no rational matrix, because its entries include \(x\).
Thus this compression removes all rational feasible points of a
rational SDP that originally has a rational strictly feasible point.

The defect is the difference between a nullvector of one selected
matrix and a common nullvector of the feasible set. A common rational
nullvector gives a rational change of basis that preserves every
feasible matrix, so it preserves rational feasibility. Selecting a
maximum-rank feasible matrix also suffices: if \(G_0,G\succeq0\),
then
\[
 \ker(G_0+G)=\ker G_0\cap\ker G.
\]
If some feasible \(G\) failed to kill a vector in \(\ker G_0\),
their midpoint would have larger rank than \(G_0\). Hence a
maximum-rank feasible matrix has precisely the common kernel.

This caution concerns the inspected manuscript wording, not every
use or implementation of its procedure. It does not contradict the
[moment arithmetic note](strict-hessian-moment-arithmetic.md):
that note identifies the common real kernel using an explicitly
maximum-rank Gram, and distinguishes rational-candidate restrictions
from restrictions preserving all real feasible Grams.

The primary setup and theorem were read independently after the
counterexample was proposed. The block determinants and eigenvalues
above were checked exactly on paper. No numerical SDP experiment,
Lean proof, project-wide check, or CI inspection was used.
