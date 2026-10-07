# Exact arithmetic: source comparison and publication scope

Date: 2026-10-03. This is a focused primary-source recheck for the
arithmetic research synthesis. It does not replace proof review of the
repository's reductions. Publication priority remains unestablished.

The exact-arithmetic part already has a substantial literature audit.
In particular, the September 27 notes explicitly use and compare
*Hesse's Redemption*. The missing task was to connect that audit to the
point-approximation story, not to discover that source for the first time.

## What the exact quartic theorem says

The [upper-bound note](../../research-20260927/strong-convex-quartic-posslp-upper.md)
treats an explicitly represented rational quartic on all of
\(\mathbb R^n\), with a supplied positive rational \(\mu\) and the promise
\(\nabla^2f\succeq\mu I\) globally. For its unique minimizer \(p\), each
order or equality predicate on a supplied degree-at-most-four observable
\(h(p)\) reduces to one PosSLP instance. The reduction constructs a
polynomial-size arithmetic circuit, not an exponentially long printed
rational approximation.

The [lower-bound construction](../../research-20260927/posslp-certified-cubic-root-reduction.md)
and its [unconstrained perturbation](../../research-20260927/unconstrained-quartic-posslp-reduction.md)
give matching order-comparison hardness with a supplied positive definite
rational Hessian Gram. This is a polynomially checkable restricted input
format. The resulting completeness claim is for order comparisons;
equality has an upper bound, without a matching equality lower bound in
these notes. General polyhedral constraints are outside this
unconstrained classification.

## The Hesse comparison has no contradiction

The directly inspected version of Slot, Steurer and Wiedmer,
[*Hesse's Redemption*](https://arxiv.org/html/2511.03440v1), is v1.
Corollary 1.2 gives polynomial-time objective-gap approximation for a
globally convex rational polynomial over a rational polyhedron.
Table 1 leaves exact quartic threshold complexity and compact rational
witnesses unresolved in that version. Appendix C gives an irrational
quartic minimizer and a sextic zero sublevel without rational points.
Lemma C.3 concerns **univariate** convex quartics: a rational minimum
forces a rational minimizer.

The repository's
[quartic singleton realization](../../research-20260927/general-strongly-convex-quartic-singleton.md)
uses \(d-1\) variables for a degree-\(d\) algebraic number with exactly
one real conjugate. Taking an irreducible cubic therefore produces a
**bivariate** strongly convex quartic with minimum zero and an irrational
unique zero. Lemma C.3 does not apply. This answers the witness-existence
question left in the dated table for the multivariate class, conditional
on the repository proof being correct; it does not contradict a theorem
of that source or determine NP membership.

The [arXiv record](https://arxiv.org/abs/2511.03440) still lists only v1,
dated November 5, 2025, as checked on October 3, 2026. The proceedings
[publisher endpoint](https://dl.acm.org/doi/10.1145/3798129.3800760)
could not be read during this audit. Accordingly this comparison is
version-specific and does not assert the proceedings text is identical.

## Closest exact-decision precedents

Etessami, Stewart and Yannakakis,
[*Polynomial Time Algorithms for Multi-Type Branching Processes and
Stochastic Context-Free Grammars*](https://arxiv.org/pdf/1201.2374v2),
Appendix C, Corollary C.8, proves many-one PosSLP equivalence for strict
rational-threshold comparisons at coordinates of a probabilistic
polynomial system's least fixed point. Its proof already combines
polynomially many Newton steps, algebraic separation, determinant
circuits, repeated squaring and division elimination. Equality and
non-strict comparison are also decidable with a PosSLP oracle there.

That result is the closest inspected predecessor for the method.
Its coordinatewise monotone probabilistic maps are not the same input
class as globally strongly monotone gradient maps. In the latter,

\[
 (T(x)-T(y))^T(x-y)\geq\mu\|x-y\|^2.
\]

A theorem for one class does not transfer to the other from the shared
word “monotone.” The repository must credit the compressed-Newton
architecture and distinguish its target class and lower-bound
realization. Calling the general architecture new would be inaccurate.

Allender, Bürgisser, Kjeldgaard-Pedersen and Miltersen,
[*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
Proposition 1.1, identifies constant-free polynomial-time real
computation on Boolean inputs with \(\mathrm P^{\mathrm{PosSLP}}\).
Section 1.4 already discusses exponentially accurate square-root
approximations represented by short Newton circuits. The real-machine
simulation permits adaptive sign tests; it does not alone establish a
many-one reduction to a single final sign query.

Tarasov and Vyalyi,
[*Semidefinite Programming and Arithmetic Circuit Evaluation*](https://arxiv.org/pdf/cs/0512035v1),
Theorems 3 and 4, already reduce arithmetic-circuit order comparison to
exact semidefinite feasibility. Thus broad exact convex feasibility was
already PosSLP-hard. The additional restriction to an explicitly
expanded rational quartic, global strong convexity, a supplied strict
Hessian certificate and elementary or absent constraints is the material
comparison. Squaring arbitrary arithmetic residuals does not preserve
convexity and is not a substitute for the repository's realization.

Bürgisser and Jindal,
[*On the Hardness of PosSLP*](https://goravjindal.github.io/assets/pdf/posslpsoda2024.pdf),
Theorem 1.2, gives a consequence for NP under an additional conjecture
about computing polynomial radicals. Its result is conditional. The
repository's PosSLP-hardness consequently must not be described as an
unconditional NP-hardness theorem or an unconditional exclusion from P.
The succinct univariate polynomial encoding used in that work must also
be distinguished from the explicit fixed-degree quartic input here.

## What is established by this audit

The direct source checks support a precise publication claim: the
repository proposes a matching exact arithmetic classification for a
specified, verifiably strongly convex quartic class, using established
Newton-circuit techniques and a specialized convex realization. The
singleton constructions address an additional rational-witness boundary.
Approximate value computation, exact sign comparison, rational witness
existence and witness representation are different statements.

The existing
[monotone-map audit](../../research-20260927/monotone-gradient-posslp-prior.md)
and [independent broader audit](../../research-20260927/monotone-polynomial-posslp-prior-independent.md)
also compare variational inequalities, optimizer pseudogates and finite
SOS convergence. Those additional source comparisons were read from the
repository here; they were not all independently re-fetched in this
focused recheck. Finite exactness of a relaxation or representation at a
fixed point does not itself give a polynomial-time exact sign algorithm.

Searches combined exact convex quartics, PosSLP, irrational minimizers,
rational witnesses and strongly monotone polynomial equations. These
checks are finite and do not establish novelty by absence. In
particular, the inaccessible proceedings version and equivalent
formulations under other terminology remain literature limitations.

## Verification

The linked primary texts for the five comparisons above were opened,
and the specified theorem passages were read. A scoped Python check
verified this note's final newline, trailing whitespace and local
Markdown links. `git diff --check --
research-20261003-arithmetic/literature/exact-prior.md` passed. No
project-wide checks or CI inspection were run. These are document and
source-scope checks, not a fresh proof verification of the quartic
reductions.
