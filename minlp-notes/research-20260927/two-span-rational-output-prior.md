# Prior audit for rational output at Hessian span two

Date: 2026-09-28. This is an independent, focused literature audit of the
proposed rational-output algorithm. It does not certify publication priority
or replace proof review.

The proposed output guarantee concerns a nonempty set defined by rational
native convex quadratic inequalities, with Hessian matrix span at most two,
and arbitrarily many rational affine rows. Both the number of variables and
the number of affine rows may grow. The intended output is an exactly feasible
rational vector, in polynomial bit complexity. The underlying existence and
short-witness result is in
[the rationality note](two-span-rationality-frontier.md).

The strongest general rational-output predecessor located is Safey El Din and
Zhi's algorithm for convex semialgebraic sets. Its published complexity does
not directly imply the proposed polynomial bound when the ambient dimension
grows. No inspected theorem directly subsumes the combination of two Hessian
directions, arbitrary affine rows, and polynomial-time rational output.
This limited search does not establish novelty.

## Sources and precise comparisons

1. **Safey El Din and Zhi, _Computing rational points in convex
   semi-algebraic sets and SOS decompositions_**, SIAM Journal on
   Optimization 20 (2010), 2876–2889,
   [open primary preprint](https://arxiv.org/pdf/0910.2973),
   [published DOI](https://doi.org/10.1137/090772459).
   Theorem 1.1, Corollary 1.2, and the affine restriction argument in
   Section 3 were inspected. For a convex set in dimension \(n\), defined
   by \(s\) rational polynomials of degree at most \(D\) and coefficient
   bit length \(\sigma\), Theorem 1.1 decides whether a rational point
   exists and returns one when possible, in
   \(\sigma^{O(1)}(sD)^{O(n^3)}\) bit operations. Its output bound is
   \(\sigma D^{O(n^3)}\). Corollary 1.2 covers quantified descriptions.
   Thus exact rational output, including lower-dimensional sets, is an
   established algorithmic task. Direct substitution of \(D=2\) does not
   make this bound polynomial in growing \(n\), even with two nonlinear
   constraints. Its affine restriction mechanism is also relevant prior
   methodology; it should not be presented as a new general principle.

2. **Bienstock, Del Pia, and Hildebrand, _Complexity, exactness, and
   rationality in polynomial optimization_**, Mathematical Programming
   197 (2023), 661–692,
   [open primary preprint](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf),
   [published DOI](https://doi.org/10.1007/s10107-022-01818-3).
   The introduction of the open preprint and the repository's published
   full text were inspected. The paper distinguishes Vavasis's short
   rational witness theorem for one quadratic inequality with affine
   rows from exact feasibility results for two quadratics and from
   fixed-number quadratic algorithms. It explicitly notes that the
   latter algorithms do not cover arbitrarily many affine inequalities
   plus two quadratic inequalities. Its rationality results do not state
   the native PSD span-two rational-output guarantee. The cited
   Vavasis–Zippel technical report was not separately retrieved in this
   audit, so its scope is recorded only as reported in this primary
   paper, not as an independently inspected theorem.

3. **Jia, Choi, Mourrain, and Wang, _An algebraic approach to continuous
   collision detection for ellipsoids_**, Computer Aided Geometric Design
   28 (2011), 164–176,
   [open primary paper](https://i.cs.hku.hk/~ykchoi/quadrics/CAGD_algebraic_ellipsoids.pdf).
   Sections 2–3 and Theorem 3.10 were inspected. These concern the
   characteristic polynomial of two ellipsoids in three-dimensional
   space, including the positive double root associated with external
   tangency and possible additional negative multiple roots. This is
   strong precedent for the determinant, repeated-root, and subresultant
   approach. The inspected statements do not assert rationality of the
   contact point for rational input in arbitrary dimension, or the
   extension to arbitrary affine rows. The repository's cancellation of
   the Schur-function denominator is a substantive distinction that
   must remain explicit in any comparison.

4. **Henrion, Naldi, and Safey El Din, _Exact algorithms for semidefinite
   programs with degenerate feasible set_**, 2018 manuscript,
   [author-hosted primary paper](https://perso.lip6.fr/Mohab.Safey/Articles/HeNaSa18.pdf).
   The abstract and Sections 1.1–1.2 were inspected. The authors remove
   genericity assumptions on the feasible spectrahedron, retain
   genericity assumptions on the linear objective, and return an
   algebraic representation. They give polynomial arithmetic complexity
   when either the number of variables or the matrix size is fixed.
   A usual SDP representation of two growing-dimensional quadratic
   inequalities fixes neither quantity. These stated bounds do not
   directly yield the proposed result, and algebraic output alone does
   not imply rational output.

## Why an arbitrary one-parameter SDP theorem is insufficient

One must not replace the special tangency argument by an assertion that a
nonempty rational one-variable spectrahedron has a rational point. The
following pencil gives an exact elementary counterexample:

\[
 A(t)=\operatorname{diag}\left(
 \begin{pmatrix}t&2\\2&2t\end{pmatrix},
 \begin{pmatrix}2&t\\t&1\end{pmatrix}\right).
\]

For its first block, positive semidefiniteness is equivalent to
\(t\ge0\) and \(2t^2-4\ge0\), hence \(t\ge\sqrt2\).
For its second block it is equivalent to \(2-t^2\ge0\), hence
\(|t|\le\sqrt2\). Therefore

\[
                       \{t:A(t)\succeq0\}=\{\sqrt2\}.
\]

This calculation is a boundary check, with no novelty claim. The rational
tangency lemma needs the special PSD structure of the two native Hessians,
which controls the poles and residues of their Schur function.

## Appropriate contribution statement

Conditional on complete verification of the output algorithm, its additional
content is a polynomial-time rational-output guarantee for this representation
class, based on the special span-two rationality theorem and exact fixed-span
optimization. It is not the first algorithm to compute rational points in
convex semialgebraic sets, the first use of affine restrictions for this task,
or the first determinant-based ellipsoid contact algorithm. The qualitative
rationality theorem remains the structural reason the output can always be
rational; a general algebraic output routine does not establish that fact.

The audit searched combinations of “two convex quadratic inequalities,”
“rational feasible point,” “rational solution,” “rational output,”
“ellipsoid tangency,” “contact point,” “one-dimensional spectrahedron,”
“one-parameter pencil,” and “rational points in convex semialgebraic sets.”
It also checked the primary references above under the different terminology
of exact SDP and collision detection. No claim is made that these searches
exhaust the relevant literature.

## Verification scope

This audit checked theorem statements and their parameter dependence. The
one-variable pencil counterexample was checked exactly from its two principal
determinants. It did not independently review the proposed algorithm's full
proof or execute project-wide checks.
