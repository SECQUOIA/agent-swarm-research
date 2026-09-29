# Independent prior audit: arithmetic of convex polynomial singletons

Date: 2026-09-28. This audit complements
[the main singleton prior audit](singleton-field-characterization-prior.md)
and [the three-ellipsoid audit](three-ellipsoid-degree-prior-audit.md).
Its emphasis is native polynomial descriptions and convex constraint
satisfaction, rather than spectrahedral constructions. The construction
under review is in [the unbounded-degree note](few-quadratic-unbounded-degree.md).

There is a direct published-preprint predecessor for an irrational singleton
defined by a globally convex rational polynomial: Slot, Steurer, and Wiedmer
give a univariate sextic with a unique cubic irrational zero. The inspected
sources do not establish the proposed general characterization together
with realization by three positive-definite quadratics. This is a bounded
source comparison, not evidence of priority. The necessity argument is
short and uses standard algebra; it could readily be known without being
indexed under the proposed terminology.

## Exact statement and the elementary part of the argument

Let

\[
S=\{x\in\mathbb R^n:f_i(x)\leq0\quad(1\leq i\leq m)\}=\{a\},
\qquad f_i\in\mathbb Q[x_1,\ldots,x_n].
\]

The argument below requires only that the individual sets
\(S_i=\{x:f_i(x)\leq0\}\) are convex. Globally convex defining
polynomials are sufficient, as are globally quasiconvex defining
polynomials. Mere convexity of their intersection is insufficient.

Write \(A=\{i:f_i(a)=0\}\). Then

\[
\bigcap_{i\in A}S_i=\{a\}.
\]

Indeed, if \(b\ne a\) belonged to every active sublevel set, every point
\((1-t)a+tb\), for \(0<t<1\), would satisfy the active inequalities.
Continuity and strictness of the finitely many inactive inequalities make
them hold for sufficiently small positive \(t\). This contradicts
uniqueness. In particular,

\[
\{x\in\mathbb R^n:f_i(x)=0\text{ for every }i\in A\}=\{a\}.
\tag{1}
\]

Thus the singleton is a real algebraic set over \(\mathbb Q\), not just
a semialgebraic set over \(\mathbb Q\). Its coordinates are algebraic:
for example, real quantifier elimination gives a rational univariate
semialgebraic description of each singleton coordinate projection, and
some nonzero polynomial in that description must vanish there.

Put \(K=\mathbb Q(a_1,\ldots,a_n)\). Every real embedding
\(\sigma:K\to\mathbb R\) preserves the active equations, so (1) gives
\(\sigma(a)=a\). Since the coordinates generate \(K\), this is the
identity embedding. Hence \(K\) has exactly one real embedding and has
odd degree over \(\mathbb Q\).

The coordinate claim needs one additional step. For any \(b\in K\), set
\(F=\mathbb Q(b)\). The degree \([K:F]\) is odd. For each real embedding
of \(F\), a primitive-element polynomial for \(K/F\), transported by
that embedding, has odd degree and therefore a real root. It follows that
each real embedding of \(F\) extends to one of \(K\). Consequently
\(F\) also has exactly one real embedding, so the minimal polynomial of
\(b\) has exactly one real root. This applies to every coordinate, not
only to a chosen primitive element.

For the weaker assumption that each zero sublevel set is convex, the
scalar converse is immediate: if \(p\in\mathbb Q[t]\) is irreducible
with exactly one real root \(\alpha\), then
\(p(t)^2\leq0\) defines the convex singleton \(\{\alpha\}\). This does
not make \(p^2\) a convex function. For example,
\(((t^3-2)^2)''=30t^4-24t\) is negative at \(t=1/2\).
The realization by three globally strictly convex quadratics is therefore
the substantive strengthening of this elementary representation.

These observations concern a coordinate occurring in some singleton
system, with ambient dimension allowed to grow. They do not say that every
such scalar singleton has a univariate quadratic description. Nor does a
unique optimizer over a larger feasible set automatically satisfy the
same conclusion: an irrational optimal value cannot simply be inserted
as a rational polynomial threshold.

## Direct native-polynomial predecessor

Lucas Slot, David Steurer, and Manuel Wiedmer,
[*Hesse's Redemption: Efficient Convex Polynomial Programming*](https://arxiv.org/html/2511.03440v1#A3),
arXiv:2511.03440v1, November 5, 2025, Appendix C:

- Example C.2 gives \(f(t)=(t^3+t+1)^2\). It has minimum zero at its
  unique irrational real zero. The displayed identity
  \(f''(t)=30t^4+6t^2+2(3t+1)^2\) proves global convexity.
- Lemma C.3 proves that a rational univariate convex quartic with rational
  minimum has a rational minimizer. Its proof uses divisibility by the
  minimizer's minimal polynomial and the uniqueness of the real critical
  point.
- Theorem 1.1 and Corollary 1.2 address convex polynomial minimization over
  polyhedra and approximate solutions. They do not give a general exact
  feasibility algorithm for several convex polynomial constraints.

This source already contains native convex polynomial irrational
singleton feasibility, and an arithmetic obstruction in small degree.
It does not state the full field-signature characterization, an
arbitrary-degree singleton family with three quadratics, or the planar
corank-one pencil construction. These are separate claims requiring
separate comparison.

## Convex constraint satisfaction and rational-point algorithms

Manuel Bodirsky, Peter Jonsson, and Timo von Oertzen,
[*Essential Convexity and Complexity of Semi-Algebraic Constraints*](https://arxiv.org/pdf/1210.0420),
Logical Methods in Computer Science 8(4), article 5 (2012), has a directly
relevant distinction in Section 6, printed pp. 23–24. Its problem
“Feasibility of Convex Polynomial Inequalities” assumes that every
individual polynomial inequality defines a convex set. It does not
require that the defining polynomials themselves be globally convex.
Section 6 distinguishes this input class from arbitrary convex
semialgebraic relations. Lemma 3.7 and Corollary 3.8 establish rational
points and their density for semilinear relations, not for arbitrary
semialgebraic relations. Theorem 4.6 characterizes essential convexity
using convex Horn definitions. None of these inspected results gives the
field characterization under review. In particular, their terminology
must not be silently identified with globally convex polynomial functions.

Mohab Safey El Din and Lihong Zhi,
[*Computing rational points in convex semi-algebraic sets and SOS decompositions*](https://arxiv.org/pdf/0910.2973),
INRIA Research Report 7045 (2009), studies convex sets defined by rational
semialgebraic formulas. Its rational-point algorithm returns a rational
point exactly when one exists; it does not assert that nonempty convex
sets in this input class always have rational points. The introduction
also discusses totally real descent for sums of squares. This is
arithmetic context for the question, but its input class permits
descriptions whose individual polynomial sublevels are not convex.
The abstract and introduction were inspected here; the full algorithm
was not independently audited in this pass.

The distinction can be seen without any spectral example. The rational
description

\[
(t^2-2)^2\leq0,\qquad -t\leq0
\]

defines the convex singleton \(\{\sqrt2\}\). The first individual
sublevel set is \(\{-\sqrt2,\sqrt2\}\), which is not convex.
Thus convexity of the represented set alone cannot yield the signature
restriction.

## A natural attempted reduction that does not settle the converse

Krzysztof Kurdyka and Stanisław Spodzieja,
[*Convexifying positive polynomials and sums of squares approximation*](https://arxiv.org/pdf/1507.06191),
Theorem 5.5 and Corollary 5.7 provide a tempting
route: multiplication by \((1+\lVert x\rVert^2)^N\) makes a polynomial
strictly convex under positivity and leading-form assumptions. The
relevant theorem requires the original polynomial to be strictly positive
on the convex closed domain. It therefore cannot be applied directly to
\(p^2\), which vanishes at the desired singleton. Their nonnegative
variant in Corollary 5.7 adds positive perturbations before multiplying;
that changes the zero set. These results do not, as stated, produce the
required zero-preserving globally convex rational description. No claim
is made here that such a description is impossible or cannot follow from
another convexification theorem.

## Assessment and verification

The necessity argument should be presented as an elementary arithmetic
observation unless a stronger historical claim receives further support.
The strongest construction claim to compare is the joint statement:
every permitted nonrational scalar is realized using three rational
positive-definite quadratics, with the stated ambient dimension; the
companion rational two-parameter pencil has a singleton feasible set and
corank one. Arbitrary irrational singleton examples, including the
native sextic above, do not establish that joint statement.

Primary material actually inspected: Hesse Appendix C and main theorem
statements; Bodirsky–Jonsson–von Oertzen Sections 3.2, 4 and 6;
Safey El Din–Zhi abstract and introduction; Kurdyka–Spodzieja introduction,
Theorem 5.5, and Corollary 5.7. Search routes included convex constraint satisfaction,
rational convex polynomial feasibility, algebraic conjugates of convex
minimizers, and polynomial convexification. A Jonsson–Thapper 2018 paper
was located through its authors' publication pages, but unsuccessful
full-text retrieval means it is not counted as fully inspected here.
Missing search results do not establish novelty.

Targeted local check actually run: an inline `python`/SymPy calculation
verified the displayed sextic second-derivative identity, irreducibility
of \(t^3+t+1\), and its count of exactly one real root. All three checks
passed. Also ran `git diff --check -- research-20260927/singleton-field-characterization-prior-independent.md`
without diagnostics; the new file was separately read back. No project-wide
checks or CI inspection were run.
