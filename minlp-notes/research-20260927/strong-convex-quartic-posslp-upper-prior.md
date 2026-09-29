# Prior audit for exact strongly convex optimization and PosSLP

Date: 2026-09-28. This is a primary-literature and significance audit,
not the independent proof review of the upper bound.
The mathematical upper bound in
[the main note](strong-convex-quartic-posslp-upper.md), including its
polynomial-observable extension, has passed
[fresh independent proof review](strong-convex-quartic-posslp-upper-independent-review.md).
Publication priority is unestablished.

The [independent source and scope review](strong-convex-quartic-posslp-upper-prior-review.md)
passed after the recorded wording corrections. It does not replace
the separate mathematical proof review.

The Newton method, algebraic separation, compressed rational arithmetic,
and even the reduction to **one** PosSLP instance all have close,
explicit predecessors. The possible contribution is their application
to general unconstrained rational strongly convex quartics with a
supplied rational curvature lower bound, followed
by the matching lower bound for quartics with supplied strict rational
Hessian certificates. It should not be presented as a new method for
turning high-precision Newton iteration into an exact sign decision.

## 1. The target and the distinctions that matter

The input is an explicitly represented rational quartic
\(f\), a positive rational \(\mu\), and the promise
\(\nabla^2f\succeq\mu I\) on all of \(\mathbb R^n\).
For its unique minimizer \(p\), rational-threshold comparisons of
\(f(p)\) and of a coordinate \(p_j\) reduce in polynomial
time to one PosSLP instance per chosen predicate. The upper bound
also covers \(h(p)\) for a supplied rational polynomial \(h\)
of degree at most four. Equality and zero gaps are included.
The algorithm first prints a polynomial-bit rational starting point;
subsequent, much more accurate iterates are shared arithmetic circuits.

A supplied rational positive definite Gram matrix for the Hessian
biform makes a narrower input class polynomially checkable and gives
an explicit rational \(\mu>0\). Together with the separately
reviewed [lower bound](unconstrained-quartic-posslp-reduction.md),
the upper bound classifies strict and weak minimum order comparison
in that class as PosSLP-complete. The associated optimizer-coordinate lower bound
is in the [root-circuit reduction](posslp-certified-cubic-root-reduction.md).
Those order comparisons are also PosSLP-complete. Equality has the
proved upper bound; no matching equality hardness result is claimed.

The upper bound is unconstrained and requires a supplied
global strong-convexity bound. It does not establish PosSLP membership
for general exact SDP, all convex quartics, constrained polynomial
optimization, or arbitrary uniquely solvable polynomial systems.

## 2. The closest methodological predecessor already gives many-one completeness

Etessami, Stewart, and Yannakakis,
[*Polynomial Time Algorithms for Multi-Type Branching Processes and
Stochastic Context-Free Grammars*, arXiv:1201.2374v2](https://arxiv.org/pdf/1201.2374v2),
Appendix C, **Corollary C.8**, proves polynomial-time many-one
equivalence with PosSLP for strict rational-threshold comparisons of
coordinates of the least fixed point of a probabilistic polynomial
system. The inspected version is dated February 2013; the appendix
states that this extension was absent from the STOC 2012 version.

Theorem C.4 supplies doubly exponential precision after polynomially
many Newton iterations. Lemma C.5 and Theorem C.7 combine algebraic
separation with an explicit precision choice. The proof of Corollary
C.8 represents Newton iterates by polynomial-size arithmetic circuits,
implements matrix inversion through determinants, clears divisions,
and performs one final sign comparison. Thus neither the circuit
representation nor the many-one strengthening is new here.

Their systems have nonnegative coefficients with each coefficient sum
at most one and a distinguished least fixed point in the unit cube.
This is not a statement about arbitrary gradient equations of strongly
convex polynomials. A reduction between those two input classes would
need proof; uniqueness alone does not supply it. This source is the
closest inspected precedent for the upper-bound architecture.

## 3. The broader numerical-complexity framework is older

Allender, Bürgisser, Kjeldgaard-Pedersen, and Miltersen,
[*On the Complexity of Numerical Analysis*](https://people.cs.rutgers.edu/~allender/papers/slp.pdf),
Proposition 1.1, identifies the Boolean part of constant-free
polynomial-time real computation with \(\mathrm P^{\mathrm{PosSLP}}\).
This allows adaptive oracle calls at branch tests; it does not by
itself give a many-one reduction to one PosSLP instance. Proposition
1.3 likewise states a polynomial-time Turing equivalence for its
numerical problem.

Section 1.4 explicitly credits Tiwari's 1992 work for polynomial-size
Newton circuits approximating square roots to exponential precision.
That attribution was read directly; Tiwari's original article was not
obtained in this audit. Section 3, before Theorem 3.9, discusses small
circuits for approximating algebraic functions. The theorem there
concerns a fixed constant, and its one advice bit should not be
confused with one oracle query for a varying optimization input.

These results explain why compressed arithmetic is the natural output
model. They do not supply uniform radius, conditioning, or Newton-basin
bounds for a growing-dimensional polynomial minimization instance.

Kung and Traub,
[*All Algebraic Functions Can Be Computed Fast*](https://www.eecs.harvard.edu/~htk/publication/1978-jacm-kung-traub.pdf),
Theorem 8.1, is an earlier Newton-method precedent: it bounds field
operations for computing expansion coefficients. The source separates
that cost model from coefficient growth and more general multivariate
extensions. It should not be cited as an exact bit-complexity theorem
for the present optimization problem.

## 4. Approximation and algebraic separation are established ingredients

Slot, Steurer, and Wiedmer,
[*Hesse's Redemption: Efficient Convex Polynomial Programming*,
arXiv:2511.03440v1](https://arxiv.org/html/2511.03440v1),
Corollary 1.2, provides the polynomial-time convex approximation used
for the initial point. Only ordinary polynomial-bit accuracy is
requested at that stage. Its Table 1 and Section 1.3 distinguish
approximation from exact threshold decision and list the latter's
convex-quartic complexity as unknown in that dated version.

This source is a convenient direct dependency, but its recent general
norm theorem is not essential to the conceptual strong-convexity
argument. Here the elementary bound
\(\|p\|\le\|\nabla f(0)\|/\mu\) already gives a rational
search radius. This explains why the radius question is easier in
the present class. This audit does not substitute a different
optimization theorem for Corollary 1.2. The extra work is the uniform
exact-decision analysis and its matching restricted lower bound,
not approximate optimization alone.

The inspected preprint and official STOC 2026 acceptance are documented
in the [lower-bound prior audit](posslp-convex-quartic-prior.md).
The final proceedings text was not obtained, so the dated table is
not evidence that a question remained unresolved in a later version.

For separation, Basu's author survey,
[*Algorithms in Real Algebraic Geometry: A Survey*](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf),
Theorem 2.16, gives the one-block quantifier-elimination bounds used
by the proof. Applying them to a singleton **real** projection avoids
assuming that the whole complex critical locus is finite. The
elimination is an analysis tool; the reduction need not execute it.

Hansen, Koucký, Lauritzen, Miltersen, and Tsigaridas,
[*Exact Algorithms for Solving Stochastic Games*](https://arxiv.org/pdf/1202.3898),
Theorem 23, is a further primary predecessor giving explicit degree,
height, and separation bounds for isolated real solutions. It is
also the source used in the probabilistic-system argument above.
The authors expressly distinguish isolated real roots from isolated
complex roots and describe their elimination techniques as standard.

One printed step in its proof, on page 23, applies Lemma 26 as if a
nonzero root obeyed \(|\gamma|>\|R\|_\infty^{-1}\); the
lemma states the weaker factor-2 bound. The stronger inequality is
false in general, as the positive root of \(t^2+3t-1\) shows.
This observation does not establish that the final conservative
theorem is false. It does mean that this audit does not endorse every
printed constant or replace the proof's separate Basu-based argument
with that dependency merely to obtain explicit constants.

## 5. The established classification and its significance

The combined result is exact PosSLP-completeness under
polynomial-time many-one reductions for
strict and weak unconstrained minimum-threshold and minimizer-coordinate comparisons
of a natural, verifiably strongly convex quartic class. The hard
instances already supply a rational positive definite Hessian Gram;
curvature recognition is not the source of difficulty. The upper
bound handles all inputs of that class and not just the specific
circuits used by the reduction. It additionally covers equality;
equality completeness is not asserted.

The upper-bound method is an adaptation of established tools. The
lower-bound realization under those polynomial and curvature
restrictions appears the more substantial construction. A complete
classification is stronger than either an arithmetic witness-size
obstruction or a one-sided hardness result. This ranking is a
significance assessment, not a priority claim.

An additional consequence is a polynomial-size rational
arithmetic-circuit point whenever the zero sublevel has
nonempty interior. It is compatible with the
[exponential expanded-witness lower bound](strict-convex-quartic-rational-witness-lower-bound.md):
sharing arithmetic subexpressions can be short even when printing
all numerators and denominators is long. It does not produce a
rational point in a singleton irrational zero sublevel.

For MINLP, the result isolates the exact arithmetic cost of a
continuous polynomial node bound even with certified global curvature.
It neither shows PosSLP is NP-hard or outside P nor supplies a practical
solver speedup. It also leaves constrained problems, weaker curvature,
and exact symbolic output costs outside this classification.

## 6. Search and review record

Searches combined `PosSLP`, `strongly convex`, `convex polynomial`,
`exact minimization`, `Newton`, `Boolean part`, `fixed point`, and
`algebraic separation`. The search also inspected references from the
probabilistic-system and numerical-complexity papers. Primary source
text was used for the substantive comparisons. Secondary search hits
were used only as leads.

The author and a fresh reviewer independently read the relevant
Etessami--Stewart--Yannakakis and numerical-complexity statements.
The reviewer additionally checked the Kung--Traub scope directly.
The author and the upper-bound author independently inspected the
Hansen separation passage. These checks establish source scope and
identify methodological precedent; they do not verify the new upper
proof or establish novelty by exclusion. Equivalent results under
other terminology, general theorems with an applicable specialization,
and later versions remain unresolved prior-work risks.

The [broader formulation check](monotone-gradient-posslp-prior.md)
and [independent audit](monotone-polynomial-posslp-prior-independent.md)
record follow-up searches under monotone polynomial equations,
variational inequalities, gradient systems, fixed-point representations,
and finite SOS convergence. They found additional methodological
precedents but no inspected theorem giving the full target statement.

Targeted document checks passed: a `python -` check of this note and
`strict-convex-quartic-witness-prior.md` verified trailing newlines,
absence of trailing whitespace and control characters, balanced inline
and display math delimiters, and all local Markdown links.
`git diff --check -- research-20260927/strong-convex-quartic-posslp-upper-prior.md research-20260927/strict-convex-quartic-witness-prior.md`
also passed. No project-wide verification or CI inspection was run.
