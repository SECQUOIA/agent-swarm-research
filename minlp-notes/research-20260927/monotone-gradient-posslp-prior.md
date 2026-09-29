# Further prior checks: monotone equations and gradient systems

Date: 2026-09-28. This supplements the
[exact-quartic upper-bound audit](strong-convex-quartic-posslp-upper-prior.md).
It records material scope comparisons from a broader search, not a
claim that all equivalent formulations have been excluded.

The [fresh source review](strong-convex-quartic-posslp-upper-prior-review.md)
checks the comparisons below. A separate
[independent audit](monotone-polynomial-posslp-prior-independent.md)
and its [source supplement](strong-monotone-exact-prior-supplement.md)
cover convex-optimization pseudogates, unique fixed points, finite SOS
convergence, polynomial variational inequalities, and condition-based
real-zero algorithms.

The alternative formulation that could subsume the quartic upper
bound is exact rational-threshold comparison at the unique zero of a
rational cubic map \(T\) satisfying
\[
 \langle T(x)-T(y),x-y\rangle\ge\mu\|x-y\|^2
 \qquad(x,y\in\mathbb R^n),
\]
with a supplied rational \(\mu>0\). For a quartic potential,
\(T=\nabla f\). Coordinatewise order preservation of a polynomial
map is a different use of the word monotone. Thus the probabilistic
polynomial-system results do not automatically cover this formulation.

## Material source comparisons

**A modern source for a moderate-precision initial point.**
Anagnostides, Farina, Sandholm, and Zhang,
[*A Polynomial-Time Algorithm for Variational Inequalities under the
Minty Condition*, arXiv:2504.03432v3](https://arxiv.org/pdf/2504.03432v3),
Theorems 1.5 and 4.7, gives an approximate Stampacchia VI solution in
time polynomial in dimension, \(\log(B/\epsilon)\), and
\(\log L\). Here \(B\) bounds the mapping, \(L\) is its
Lipschitz constant, and a compact convex domain has separation access.
Assumption 2.4 requires rational evaluation with polynomial encoding
length. Section 4.1 explicitly uses rounded rational ellipsoid data.
These are approximation results, not exact threshold or PosSLP
classification results.

Theorem 4.7 is stated for an isotropic domain. Its general affine
normalization should not silently be treated as an exact rational
operation: covariance normalization can introduce irrational entries.
A direct rational-domain argument, or a separately checked oracle
specialization, is preferable for a new bit-model proof. The source
also allows approximate value oracles in Appendix B; the caution
concerns instantiating the bit model, not the validity of its
approximation theorem. The source
attributes earlier strong-monotonicity ellipsoid work to Lüthi (1985)
and a broader approximation result to Magnanti--Perakis (1995).

The following is an elementary observation of this audit, rather than
an exact-decision theorem in that source. If a zero \(p\) lies in
the VI domain, then an \(\epsilon\)-SVI point \(x\) satisfies
\[
 \mu\|x-p\|^2
 \le\langle T(x)-T(p),x-p\rangle
 =\langle T(x),x-p\rangle\le\epsilon.
\]
Therefore a rigorously instantiated VI approximation theorem can give
a Newton starting point using only polynomial-bit accuracy. The
existence of a zero, its radius, the rational input model, and the
later exact comparison still require separate arguments.

**A polynomial-equilibrium claim that is explicitly approximate.**
Abolhassani, Bateni, Hajiaghayi, Mahini, and Sawant,
[*Network Cournot Competition*](https://arxiv.org/pdf/1405.1794),
uses strong convexity and strong monotonicity to obtain unique
equilibria. Its Theorem 10 explicitly outputs an approximate
complementarity solution with normalized complementarity gap at most
\(\epsilon\), with iteration bound
\(O(E^2\log(\mu_0/\epsilon))\). Thus the broad wording about
polynomial-time equilibrium computation in the introduction does not
supply an exact algebraic-coordinate decision theorem. The theorem
and its stated output criterion were read directly.

**General VI complexity does not impose the needed monotonicity.**
Kapron and Samieefar,
[*The Computational Complexity of Variational Inequalities and
Applications in Game Theory*, arXiv:2411.04392v1](https://arxiv.org/pdf/2411.04392v1),
formulates approximate VI and generalized VI search and proves
PPAD-completeness. The inspected introduction and problem formulations
concern approximation and do not give the globally strongly monotone
polynomial threshold classification. Section 6 expressly leaves exact
VI formulations for future work and conjectures a suitable
FIXP-completeness result. The usual equivalence between
convex minimization and a gradient VI is recorded in its Appendix C;
that equivalence alone supplies no new bit-complexity bound.

**Older geometric methods are leads, not exact-decision dependencies.**
Lüthi's
[*On the Solution of Variational Inequalities by the Ellipsoid
Method*](https://doi.org/10.1287/moor.10.3.515)
has a primary publisher abstract about convergence of the ellipsoid
method. Magnanti and Perakis's
[*A Unifying Geometric Solution Framework and Complexity Analysis for
Variational Inequalities*](https://dspace.mit.edu/entities/publication/25cd2edd-96c5-4f3c-8851-5ce571d7ba9e)
has a primary repository abstract stating near-optimal solutions in
polynomially many iterations. Full text was not obtained from those
primary endpoints in this follow-up. Neither abstract establishes an
exact sign theorem; no stronger conclusion about their full scope is
claimed here.

## Limits of the search

Queries additionally checked `strongly monotone polynomial systems`,
`unique real root`, `gradient`, `contraction`, `exact comparison`,
`PosSLP`, and `real computation`. The inspected results above did not
yield an equivalent exact classification. Unique fixed points,
FIXP representations, and compact arithmetic input require separate
comparison: uniqueness does not imply strong monotonicity, a fixed
point representation is not a short evaluation algorithm, and circuit
coefficients can hide arithmetic that explicit rational coefficients
cannot. The completed independent audit records those distinctions.

The many-one Newton/arithmetic-circuit predecessor remains
Etessami--Stewart--Yannakakis, Corollary C.8, already documented in the
main audit. This follow-up strengthens the record of assumptions; an
unsuccessful search still does not establish novelty.

Targeted checks: a `python -` check of final newlines, whitespace,
control characters, paired math delimiters, and local Markdown links
passed. `git diff --check -- research-20260927/monotone-gradient-posslp-prior.md`
also passed. No project-wide verification or CI inspection was run.
