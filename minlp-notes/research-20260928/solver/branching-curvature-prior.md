# Curvature and convex-cover results: completed bounded literature audit

Date: 2026-09-28. This audit closes the literature-comparison task for the
[curvature atlas](branching-curvature-atlas.md) and
[degeneracy barrier](branching-degeneracy-barrier.md). It does not establish
publication priority. No equivalent theorem was identified in the primary
statements examined below, but the search was bounded rather than exhaustive.

The upper theorem combines established quadratic convexification and
negative-coordinate subdivision with a compactness argument. The barrier
combines established radial-well packing and convex-cover incompatibility
with a fixed, globally C² construction containing all accuracy scales.
These ingredients must not be presented as newly discovered methods.
The retained mathematical distinction is the contrast between strict
positive complementary curvature and a bound on negative inertia alone.

## Statements being compared

The approximation model is the vertical sandwich

```
epi_D f subset union_(i=1)^N C_i subset epi_D(f-epsilon),
```

with arbitrary convex pieces `C_i`, including convex projections of
continuous lifts. The atlas proves, for a fixed C² function on a compact
convex domain, `N = O_(f,D)(epsilon^(-k/2))` when at least `n-k` Hessian
eigenvalues are strictly positive everywhere. A strictly negative
`k`-dimensional slice gives the matching lower exponent.

The barrier gives one fixed C² function in every dimension `n>=2`, with
bounded Hessian and at most one negative eigenvalue everywhere, for which
the limiting logarithmic exponent of `N` is `n/2`. These are geometric
piece counts. They are not uniform bit-complexity bounds, minimum-cover
algorithms, or unrestricted optimization lower bounds.

## Closest upper-bound antecedents

**Zhang and Xia, 2024, and the Vavasis quadratic antecedent.**
The [open primary paper](https://cot.mathres.org/issues/COT202419.pdf),
Sections 1–3 and Theorem 2.1, treats a quadratic objective over a bounded
region given by convex quadratic inequalities, with a Slater point.
Approximation is relative to the objective's range. Subdivision of the
negative coordinates yields the familiar half-negative-inertia exponent;
the paper attributes the quadratic-programming scheme to Vavasis,
[*Approximation algorithms for indefinite quadratic programming*](https://doi.org/10.1007/BF01581085)
(1992). The atlas instead gives additive vertical error for smooth
nonquadratic functions, using finitely many locally chosen subspaces.
It offers no uniform bound on their construction cost or number.
The 1992 full text was not obtained in this closure pass; the earlier
repository audit examined an open precursor and this detailed reproduction.

**Skjäl, Westerlund, Misener, and Floudas, 2012.**
[*A Generalization of the Classical αBB Convex Underestimation via
Diagonal and Nondiagonal Quadratic Terms*](https://users.abo.fi/twesterl/selected-publications/5.%20JOTA-AS-TW-RM-CF-2012.pdf),
Sections 2 and 4–5, Theorems 4.1–4.3 and 5.1, constructs convex
underestimators of C² functions using interval-Hessian bounds,
quadratic perturbations, and affine corrections. It allows nondiagonal
perturbations and optimizes a bound on the maximum error.
Thus neither general smooth quadratic convexification nor nondiagonal
Hessian corrections are new here. The inspected results do not state a
rank-`k` local-cover theorem under strict real `k`-convexity or its
accuracy-dependent piece count. The atlas's projected chord correction
is a local spectral specialization of this established methodology.

## Equivalent curvature terminology and approximation results

**Pawlaschyk, 2015 and 2025.**
The [2015 dissertation](https://d-nb.info/1081429941/34), Theorem 2.4.3,
identifies C² real `q`-convexity with at most `q` negative Hessian
eigenvalues, and strict real `q`-convexity with at most `q` nonpositive
ones. Definition 2.6.5, Theorem 2.6.7, and Corollary 2.6.8 concern
approximation by real `q`-convex functions with corners, locally finite
maxima of smooth real `q`-convex functions.

The primary preprint
[*On rigid q-plurisubharmonic functions and q-pseudoconvex tube domains
in Cⁿ*](https://arxiv.org/html/2510.05009v1) (2025), Theorem 2.8,
restates both inertia characterizations; Corollary 3.9 and Theorem 3.11
give regularization and corners approximation. These statements retain
real `q`-convexity of the approximants, rather than producing convex
epigraph disjuncts. They supply no tolerance-dependent piece count.
In this terminology, the atlas assumes strict real `k`-convexity; the
barrier shows that real `1`-convexity alone allows the ambient exponent.

**Bungart, 1990.**
[*Piecewise smooth approximations to q-plurisubharmonic
functions*](https://msp.org/pjm/1990/142-2/pjm-v142-n2-p02-s.pdf),
Theorem 5.3 and Corollary 5.4, are the earlier approximation antecedents
cited by Pawlaschyk. They give approximation by piecewise smooth
`q`-plurisubharmonic functions on complex domains. Theorem 5.3 uses
strictness; Corollary 5.4 treats continuous functions without it.
The local finite maxima and complex Levi-form setting must not be
confused with a finite union of real convex epigraph pieces. The inspected
statements do not supply either rate under audit.

## Closest lower-bound and formulation antecedents

**Ma, Chen, Jin, Flammarion, and Jordan, 2019.**
[*Sampling Can Be Faster Than Optimization*](https://arxiv.org/pdf/1811.08413),
Theorem 2 and Appendix C.1, use a hidden radial well among packed balls
to obtain a derivative-oracle optimization lower bound with exponent
`n/2`. Equation (45) uses an increasing radial profile inside the well;
nonnegative tangential curvature follows by radial differentiation.
That inertia observation is our reading of the construction, not a
stated hypothesis of their theorem. The objective there has Lipschitz
gradient and depends on the requested tolerance. The repository barrier
uses one globally C² objective at all sufficiently small tolerances and
bounds every convex epigraph cover. The well-packing mechanism itself
is established prior work.

**Cibulka, Korbelář, Kynčl, Mészáros, Stolař, and Valtr, 2015.**
[*On three measures of non-convexity*](https://arxiv.org/pdf/1410.0407),
introduction and Theorems 2–4, studies invisibility graphs: two points
are adjacent when their connecting segment leaves the set. Clique size
is a lower bound on the number of convex sets covering the set.
The barrier's selected well-center graph points are an invisibility
clique in `epi_D(f-epsilon)` that any admissible cover must contain.
Consequently its segment-incompatibility lemma is an application of a
classical principle. The examined results do not impose Hessian inertia
or provide the fixed smooth, all-scales construction.

**Lubin, Vielma, and Zadik.**
[*Mixed-integer convex representability*](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
Proposition 4.2, characterizes binary mixed-integer convex representability
through finite unions of projections of closed convex sets. Definition
4.2 and Lemma 4.1 use pairwise midpoint exclusion to lower-bound the
number of unrestricted integer variables. The barrier instead proves
exclusion somewhere on each connecting segment. This bounds convex
pieces and binary assignments, but does not establish the midpoint
condition needed for the general-integer conclusion. The framework is
prior work; the smooth construction and its rate are separate claims.

## Nearby uses of “approximate convex cover” and “relaxation complexity”

Werner, Amice, Marcucci, Rus, and Tedrake,
[*Approximating Robot Configuration Spaces with few Convex Sets using
Clique Covers of Visibility Graphs*](https://groups.csail.mit.edu/robotics-center/public_papers/Werner23.pdf)
(2023 preprint; ICRA 2024), Section III.A, Definition 1, asks for convex
subsets covering a specified fraction of free-space volume. This is
inner approximation with allowed uncovered volume, unlike the vertical
outer sandwich here. Its visibility formulation confirms the relevant
terminology but does not imply a Hessian-dependent exponent.

An independent parallel audit also examined these primary sources:

- Averkov, Hojny, and Schymura,
  [*Computational aspects of relaxation complexity: possibilities and
  limitations*](https://pure.tue.nl/ws/portalfiles/portal/277790121/s10107_021_01754_8.pdf),
  Section 2.2: hiding sets lower-bound the number of inequalities in
  polyhedra preserving specified lattice points. This is a related
  incompatibility device, but a different complexity measure.
- Abrahamsen,
  [*Covering Polygons is Even Harder*](https://arxiv.org/pdf/2106.02335),
  Theorem 1: minimum exact convex polygon covering has an
  existential-theory-of-the-reals hardness result. This does not prove
  hardness of constructing the particular nonoptimal atlas cover.
- Geschke and Kojman,
  [*Convexity numbers of closed sets in Rⁿ*](https://www.math.uni-hamburg.de/forschung/bereiche/dm/personen/geschke-stefan/pdf/papers/n-conv5.pdf):
  exact convex covers and cardinal invariants, rather than smooth
  approximation exponents.

## Scope and final assessment

Searches included combinations of `real q-convex`, `strict real
q-convex`, `negative eigenvalues`, `Hessian inertia`, `nonconvex rank`,
`local curvature`, `alphaBB`, `nondiagonal convex underestimation`,
`convex epigraph cover`, `approximate convex cover`, `convexity number`,
`invisibility graph`, `hiding set`, and `mixed-integer convex
representability`. Named references in the most relevant results were
followed to the primary sources listed above. Search snippets and
secondary summaries were used as leads, not as theorem evidence.

The independent parallel review agreed that the well incompatibility
argument is classical and checked the distinction between binary
disjuncts and unrestricted integer variables. I independently reopened
the Cibulka and Lubin–Vielma–Zadik texts and checked the cited definitions
and statements. The prior proof reviews remain the evidence for the
mathematical results; this audit is not another proof verification.
The parallel reviewer also read the completed audit and found its
convex-cover source descriptions and qualified assessment accurate.
That final read did not independently verify the αBB, Pawlaschyk,
Bungart, or Werner source readings.

The appropriate classification is a proved geometric extension and a
proved explicit obstruction, both with qualified originality. The
combined comparison may be useful for deciding when local curvature
can justify fewer convex relaxations. The existing proofs do not
establish practical speedup, a uniform solver complexity theorem, or
publication priority. This bounded audit is complete; those limitations
are recorded rather than converted into additional research tasks.

The targeted command `python -` with an inline `pathlib`/`re` script
checked the three curvature Markdown files for trailing whitespace,
final newlines, and existing local Markdown targets after the update:
all three files and all 12 local targets passed. No theorem was changed,
no new computational experiment was run, and no project-wide verification
or CI inspection was performed.
