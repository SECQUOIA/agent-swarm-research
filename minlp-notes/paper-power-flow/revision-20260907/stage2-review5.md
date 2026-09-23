# Stage 2 independent review 5

## Verdict

No major issue and no required minor correction identified. I recommend accepting the Stage 2 mathematical changes and proceeding to the integration stage. In particular, the root-normalized real-vertex encoding is equivalent to the previous cycle equations and supports the stated linear formula counts.

This is an independent mathematical review, not a proof-assistant certificate or an exhaustive publication-priority search. I read the entire frozen manuscript, not just the changed AC passage, and did not consult the other new reviewer reports.

## Coverage and mathematical assessment

I read `main.tex`, `macros.tex`, all eight section files, both appendices, the bibliography, every line of all four supplementary Python checkers, and `stage2-author.md` in or associated with `stage2-snapshot`.

### Root-normalized AC encoding

The changed material in `sections/03-ac.tex:140–203` is correct.

- The sign convention is consistent throughout: an oriented edge goes from j to i, the determinant is Im(U_i conjugate(U_j)), and the crossing identity is delta_ij = alpha_i - alpha_j + 2 pi k_ij. Consequently the required potential equation is a_i - a_j = k_ij, with a plus sign in theta_i = alpha_i + 2 pi a_i.
- Root normalization removes only the additive freedom of the integer shifts. It does not claim that the represented root phasor has argument zero. The separate physical reference-angle convention can be satisfied by rotating a whole component, as the input model allows.
- Propagating from one zero root along a forest determines every a_i as an integer sum. Thus existential quantification over real a_i is sufficient; no integrality predicate is missing. Every non-tree equation holds exactly when the corresponding fundamental-cycle crossing sum vanishes.
- The crossing rule treats the positive and negative real axes correctly, including a branch cut endpoint. Its two nonzero branches are disjoint. The complement branch includes all remaining admissible cases. Positivity of the magnitude variables and c > -1 exclude zero and antipodal directions before this rule is used.
- The formula has four variables per vertex and one per edge. Each edge adds constantly many polynomial atoms and monomial occurrences; injection expressions contribute total size proportional to the incident-edge count. Rational denominators and variable indices require polynomial total bit length, which the theorem explicitly distinguishes from the linear structural counts. All polynomial degrees remain at most two.
- Empty graphs, isolated vertices, disconnected components, negative rational cosines, c = 1, and unequal magnitudes are covered by the proof. None of the later hardness arguments requires adding transcendental constants to this formula.

### Ordinary resistive reduction

I reconstructed the pinned-bus equations, the complement allocation, and the inversion elimination. At most two extensions per request gives the stated object counts; distinct requested occurrences avoid parallel edges and loops even when source names coincide. The degree bound and redundant free-injection bound apply throughout the full voltage box, which is essential for the reverse residual argument later. The inversion range follows from the unique interior minimum of 2x - 1 + 1/x and its endpoint maximum. Every source solution determines every bus voltage uniquely, including unused coordinates. The NP consequence is stated for arbitrary polynomial certificates, not merely rational voltage lists.

### Structural transformations

The arithmetic crossover is reversible with a unique local sum. Only that sum needs the larger interval. The electrical realization keeps original and wire root bounds while enlarging copies, so it does not introduce out-of-range arithmetic solutions. Inversion solutions still have both operands at most two. I traced the disk-and-corridor argument, including adjacent doubled strands, cyclic request order, and the repeated-name case. The inversion tree has three external leaves and no incompatible leaf-order restriction.

The connection argument uses only old buses with redundant injection bounds and sufficient degree capacity. It adds uniquely pinned voltages and preserves planarity by choosing exterior faces separately. Subdivision has uniquely affine internal voltages because they are positive and have zero injection. Endpoint currents are uniformly divided by 4L for both conductance types. Even path lengths give bipartiteness, and every resulting simple cycle contains at least three full old-edge paths. The fixed-girth quantifier is consistent with the finite alphabet and polynomial construction claims. The zero-variable exception and principal-angle transfer after subdivision are handled explicitly.

### Algebraic and topological results

The basic-closedness invariance proof is sound. One must bound away from zero both the forward denominators and the numerators obtained from substituted inverse denominators; the proof does precisely this. Compactness gives a common positive rational threshold. Requiring membership in T and the inverse identity then excludes all extraneous ambient points after even-power denominator clearing.

The three-quadrant argument is valid: the first nonzero homogeneous part of every active defining polynomial cannot have odd degree, and an excluded direction can be chosen away from the finitely many remaining zero sets. The triangulation argument gives a basic closed rational standard-simplex realization without asserting that the triangulation map is rational. The field-generation theorem correctly retains a single affine recovery coordinate, rather than relying only on joint generation by all voltages. The irrational, rational, empty-set, and arbitrary-degree cases are consistent.

### Arithmetic appendix

I reconstructed the scaling circuit and all three layers of gates. Scaling both factors of a product, with a common auxiliary q = epsilon squared times z, preserves the original equation. The shifted multiplication equations force the intended unshifted product. The three-square identity produces ab, and the reciprocal gate has h = 1/[a(a+1/2)], giving the square output exactly. All displayed base gate values lie strictly inside [1/2,2], allowing a common sufficiently small dyadic neighborhood. The nonnegativity coordinate is the intended boundary exception. The converse uses algebraic identities and nonzero reciprocal denominators, not an unproved assertion that every candidate bounded solution was already near the base point. Compactness is used only for an existence choice of scaling; no polynomial-size claim is silently imported.

### Quantitative results and remaining AC claims

The reverse residual constant follows from at most 6m complement errors, the bound |h'| <= 2 on the actual inversion-bus interval, and the weighted copy errors at D. The forward extension has only the stated addition and D residuals. The recurrence family stays within the source box, is inconsistent at its last equation, and produces exactly one network violation, 1/(d_k+1). Its displayed residual is correctly distinguished from the minimum.

For separation, the epigraph is compact, nonempty, and connected via its full top face. Its dimension, 4n+2 constraints, coefficient clearing, and degree satisfy the imported minimum theorem. Substitution gives the displayed conservative bound and the claimed fixed-data doubly exponential scale. This result is not improperly extended to the planar residual construction.

The certificate proof rounds and clamps into exact rational voltage intervals, including singleton bounds. Its Lipschitz estimate and bit-size argument establish precisely the stated promise result. The reactive stability proof uses centered real angles, positive edge weights, the correct energy sign, and the conductance spectral gap. The rational constants yield 256 n(n-1)^2 eta^2 after substitution. The one-sided reactive extension is correctly presented as an exact saturation argument; symmetric tolerance hardness and fixed positive principal-window complexity are not claimed.

## Primary-source checks

I checked the following dependencies rather than relying on prior PASS labels:

- Local Art Gallery primary extraction: explicit bounded ETR-INV formulation, Definition 5, and Theorem 7. The interval is part of the source decision problem.
- Local Dynamic Toolbox primary extraction: Definition 4, Theorem 1, Lemma A's preprocessing and its claimed inverse, and the conjunction/gate material. The definition uses rational coordinate maps in both directions. The manuscript's inactive-branch example and basic-closedness obstruction are consistent with that definition and justify avoiding the broader claim.
- Published JPT source, `revision-20260907/sources/jeronimo-published.txt`: Theorem 1.1 requires dimension at least two, an even degree bound, bounded integer coefficients including the objective, and a compact connected component. The manuscript verifies all these conditions.
- Local Jafarpour et al. v4: Theorems 3.6 and 4.1. The existing potential/winding and within-cell uniqueness framework supports the manuscript's explicit credit; the new encoding is not advertised as a new winding theorem.
- Dobbins et al., [published Theorem 2.1 and proof](https://link.springer.com/article/10.1007/s00454-022-00381-0): the cited crossover equations and bounded-witness condition agree with the manuscript. The manuscript supplies the stronger explicit-bounds, solution-preserving argument it needs.
- Ohmoto–Shiota, [Theorem 1.1 and Section 1.2 in v2](https://arxiv.org/html/1505.03970v2): locally closed sets admit the stated semialgebraic triangulation, and compact sets use a finite complex. Compact input meets the local-closedness condition.

I did not reprove the deep imported ETR completeness, triangulation, or general polynomial-minimum theorems, nor independently repeat every Stage 1 literature search.

## Executed checks

I copied the four frozen programs into `revision-20260907/reviewer5-stage2/`, read them, and executed each there. All exited zero. The observed counts agree with the verification appendix: 12,751 resistive profiles; 2,112 scaled short-arc pairs, 177,168 cycles, and 4,166 graph/potential cases; 1,681 composed arithmetic gate profiles and the complete disk circuit; generalized crossover and inversion profiles, 360 perturbed networks, recurrence instances through k = 10, and rational spectral/Lipschitz samples.

These are fresh executions, but not independent implementations of every mathematical construction. The mathematical assessments above come from reconstructing the arguments; finite sampling is supporting evidence only. I did not rerun the historical optimization solver or treat its floating-point output as certification.

## Optional integration improvement

`appendices/verification.tex:109–117` retains historical solver results and repository-oriented language. For a standalone submission, I would consider moving that paragraph to the supplementary provenance notes and retaining the exact analytic examples in the paper. This is editorial preference, not a correctness defect: the current paragraph already identifies the numerical limitations, and Stage 3 is assigned submission packaging.

No correction or further Stage 2 mathematical development is required by this review.
