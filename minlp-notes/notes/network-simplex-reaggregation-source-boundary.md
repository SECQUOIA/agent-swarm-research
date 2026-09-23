# Boundary of shared-matrix hull reaggregation

Date: 2026-09-07. Status: elementary counterexample checked locally and passed
[independent review](review-network-simplex-reaggregation-source-boundary.md).
This is a source-use correction, not a claim of a
new disjunctive-programming theorem.

## Source inspected

Lee and Bernal Neira, “Mixed-Integer Reaggregated Hull Reformulation of Special
Structured Generalized Linear Disjunctive Programs,” open preprint
[arXiv:2601.11782](https://arxiv.org/abs/2601.11782), corresponding to
DOI 10.1021/acs.iecr.5c03172. The local original PDF's printed page 9 was
visually inspected. The relevant local locator is
[[lee2025-mixed-integer-reaggregated-hull-reformulation]] p.9.

Theorem 2.2's displayed first inequality has a per-disjunct right side without
a sum. The subsequent derivation and (RHR) instead use the intended aggregate
system

\[
Ax\le\sum_j\lambda_j b_j,\qquad \lambda\ge0,\quad\sum_j\lambda_j=1.
\tag{R}
\]

The surrounding text describes common left-hand coefficients and nonempty
polyhedra and asserts exactness. The proof refers to Jeroslow and Blair for
additional sufficient/necessary conditions but does not spell them out in the
displayed theorem. The following example concerns (R), so it does not rely on
the apparent missing-sum typesetting problem.

## Counterexample to common A alone

Let

\[
A=\begin{pmatrix}-1\\1\\2\end{pmatrix},\qquad
b_1=\begin{pmatrix}0\\1\\100\end{pmatrix},\qquad
b_2=\begin{pmatrix}0\\100\\2\end{pmatrix}.
\]

For j=1,2 define P_j={x in R: Ax<=b_j}. Both polytopes are [0,1]:
the second row imposes x<=1 in P_1 and the third imposes x<=1 in P_2.
Consequently their union hull is [0,1]. Their Cayley hull is
[0,1] times the two-state simplex.

At lambda_1=lambda_2=1/2, system (R) becomes

\[
x\ge0,\qquad x\le101/2,\qquad 2x\le51.
\]

Thus x=2 satisfies (R) and is outside even the projected union hull. A common
loose global bound 0<=x<=100 does not repair the counterexample. If one first
derives and adds the tight global upper bound x<=1, this particular example
disappears, but the displayed assumptions do not require that extra step.

The example uses redundant parallel rows deliberately: common A does not
ensure common active inequalities or compatible decompositions. It establishes
only that common A and nonemptiness are insufficient. It does not assert that
the source's specific scheduling/packing reformulations or experiments are
wrong.

## Independent primary corroboration

Kis and Horváth,
[“Ideal, non-extended formulations for disjunctive constraints admitting a network representation”](https://link.springer.com/article/10.1007/s10107-021-01652-z),
§2, equation (7) and its following paragraph, explicitly distinguishes (R)
from the true union hull and says that the reverse inclusion fails in general.
It cites Jeroslow's sufficient conditions, Blair's necessary and sufficient
conditions, and later extensions. This supports the limited boundary above.
The original Jeroslow and Blair full papers were not retrieved in this pass;
no theorem-level attribution beyond that openly readable comparison is made.

## Consequence for the repository

The local Lee–Bernal Neira paper summary currently paraphrases common-A
reaggregation as unconditionally exact. It should not be relied on in that
form. The archive was left unchanged; this note records the correction and its
evidence separately.

The network–simplex residual-state merger uses the stronger and elementary
identity

\[
\lambda P+\mu P=(\lambda+\mu)P\qquad(\lambda,\mu\ge0),
\]

for a single convex P. Its proof is immediate from convexity in one direction
and choosing the same point in both summands in the other. It remains exact,
including zero weights. State slices modified by observed product values need
not be homothetic and must remain separate unless another valid argument
permits their merger.
