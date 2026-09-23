# Whole-manuscript review, round 1 — independent reviewer 2

**Verdict: no major issue found; one minor composition clarification required.** After that correction, I consider the manuscript mathematically coherent and complete within its stated scope, with a clear separation of exact complexity, rational and topological universality, and numerical guarantees. This is an internal full-paper review, not a guarantee about external peer review.

I reviewed the entire frozen manuscript, its cited dependencies and package, and rederived the theorem interfaces rather than treating earlier stage passes as sufficient. I did not read other whole-paper reports or edit manuscript inputs. All 22 manifest hashes were verified before and after review.

## Required minor correction

**Preserve connectedness in the trivial principal-window transfer.**

At `sections/04-structural.tex:256–260`, the proof of `cor:structural-ac` says the corresponding transfers change no graph. There is one exceptional input to handle explicitly: the structural construction sends an arithmetic system with no variables to a single voltage-one, injection-zero bus (`lem:connect`). The principal-window corollary requires `n >= 2`; its general proof permits adding isolated buses to reach that size (`sections/03-ac.tex:336–340`). Applying that padding literally here breaks the connectedness asserted by the structural corollary.

This does not invalidate hardness, since the exceptional source is a trivial yes instance. Close the proof with either of these concrete changes:

- Before the structural construction, ensure the source has a named variable, adding a new variable fixed to one by `tt=1` if necessary; this gives a unique extension and does not change feasibility.
- Handle the no-variable source directly by two voltage-one, zero-active-injection buses joined by one unit-conductance line, with zero reactive injections and `c_2=3/4`.

The latter graph is connected, simple, planar, bipartite, has degree one and infinite girth, and uses the permitted voltage/injection values. Every nontrivial output of the existing structural construction already has enough vertices, so no isolated padding is needed there. State this exception and qualify the “change no graph” sentence accordingly.

## Full mathematical assessment

I found no other major or minor defect after checking these parts and their composition:

- **Exact model and source.** Binary rational encoding, positive voltage bounds, independently permitted singleton injections/voltages, and ETR membership are explicit. Normalizing `x=1` to `xx=1` is sound on the bounded positive source interval. Repeated and unused variables, and empty networks, retain the intended solution sets.
- **Ordinary reduction.** Complement paths supply distinct occurrence ports with the stated degree and size bounds. Addition and inversion residual equations have the correct signs; division uses positive variables. The free interval is redundant over the full voltage box. Both reduction directions and unique rational extension hold, including repeated names and unused roots. The certificate consequence uses a uniform polynomial verifier rather than irrationality alone.
- **AC membership and transfer.** Complex-power signs, shunts, and rational-cosine magnitude variables are consistent. The determinant crossing rule handles both axes, unequal magnitudes, same-direction collinearity, obtuse short arcs, and reversal. The exclusion of antipodes at `c>-1` is used exactly where needed; `c=1` is harmless. Fundamental-cycle equations characterize real lifts, and their Boolean polynomial encoding has polynomial size. The zero-reactive energy identity requires real differences below pi, not merely principal windows. One-sided reactive intervals, the rational winding counterexamples, the shrinking-window transfer, and reference-fixed boxes have the stated distinct scopes.
- **Structural restrictions.** The explicit bounded crossover is a unique extension and preserves transmitted bounds. The widened electrical complement and inversion constants are correct. Incidence disks/corridors respect repeated ports and the inversion's two adjacent first-input strands. Free-injection connectors preserve old constraints and unique voltages. Harmonic subdivisions yield exactly the common current scaling, even path lengths, and the asserted girth lower bound. All restrictions survive simultaneously. The only interface issue is the trivial principal-window case above.
- **Repaired arithmetic and universality.** The appendix begins with a conjunctive globally evaluated circuit, so it does not inherit the source's inactive-branch failure. Scaling, exact dyadic constants, shifted coordinates, multiplication from squares, and squares from reciprocals are reversible and unique. All forward ranges can be chosen uniformly by the finite gate types, while every bounded reverse solution obeys the exact algebraic identities. Compact denominator bounds prove basic-closedness invariance. The leading-homogeneous-form argument excludes the three-quadrant set. Finite triangulation and nonface equations give the separate semialgebraic topological result. The rational coefficient field is retained throughout. A designated affine coordinate supplies the singleton field/degree theorem; field generation is not incorrectly inferred from topology or joint coordinate generation.
- **Residual and certificate results.** The pointwise copy-error accumulation and inversion constants yield the stated two-sided bound for the ordinary construction. The recurrence family is exactly infeasible but has the displayed rational almost-solution, all bounds, counts, and connectedness. Its residual is only an upper bound on the positive minimum. The compact connected epigraph satisfies the JPT theorem's integer-coefficient, degree, dimension, and compact-component hypotheses; the substitution and scale are correct. Dyadic rounding with interval clamping preserves exact voltage bounds and provides polynomial-size certificates only for the stated promise. The text does not claim a polynomial exact algorithm or solve the different lossless approximate-membership question.
- **Reactive stability.** Centering and the conductance Laplacian produce the stated spectral inequalities and constants. The active discrepancy is nonnegative, the rational weakened constants are valid, and the graph lower bound covers the two-bus case. Componentwise application and isolated-bus conventions avoid a zero-eigenvalue division. The combined ordinary-source residual coefficient `256n(n-1)^2` follows correctly.

The source dependencies are used within their verified scopes. In particular, the false general Boolean universality assertion is demonstrated and replaced by a self-contained restricted proof; the planar crossover's bounded-witness statement is not mistaken for full solution-set preservation; triangulation is used only topologically; and the polynomial-minimum theorem is applied to the required compact connected set. Version-specific theorem references remain explicit. The literature comparison distinguishes physical DC, lossless fixed-magnitude AC, tree/star hardness, fixed-source demand sets, convex-relaxation conditions, and scaled approximation.

## Completeness, structure, and reproducibility

The introduction states the strongest simultaneous restriction and gives a useful proof map. The detailed models precede the results using them. The separate structural, algebraic, and numerical sections have coherent interfaces, and the appendices keep the longer arithmetic identities and finite checks available without interrupting the main reduction. The conclusion does not overstate the principal-angle or numerical conclusions.

All eight legacy arithmetic examples are present. I independently checked their six feasible exact profiles symbolically and their interval bounds; the two infeasibility arguments are immediate consequences of the displayed equations. Historical solver output is clearly distinguished from exact evidence. The claimed exact-check counts reproduce.

The source inventory covers the core result, all three power-flow audits, closeout/novelty notes, both code files, the shared arithmetic dependency, and the numerical examples. An independent filename search and the two-worktree listing found no omitted power-flow development. The previously checked identical core files in the second worktree remain accounted for, and broader potential-flow manuscripts are correctly identified as a different topic.

The README now specifies Python 3.10 or newer and the correct lower-bound-on-girth claim. The package builds with standard tools and the exact suites need no licensed solver. I found no unresolved citation, labeling, or layout defect. Rendered pages 22, 25, and 27 are legible, including the stability proof, dense arithmetic gate identities, and eight-example table.

## Evidence retained

Under `verification/reviewer2/full-round01/`:

- `resistive.log`, `ac.log`, `developments.log`, `arithmetic.log`: fresh successful runs of all four frozen exact suites.
- `check_boundary_composition.py`, `boundary-composition.log`: independent exact check of the proposed connected two-bus exceptional image and symbolic checks of all six feasible legacy profiles. These support the stated correction without changing manuscript code.
- `build.log`, `build/main.pdf`, `build/main.txt`: clean independent 28-page build and extracted text. The final log contains no unresolved-reference/citation or overfull/underfull warnings.
- `page22.png`, `page25.png`, `page27.png`: reviewer-owned renderings inspected for readability.

The connectedness clarification is the only correction requested by this full-paper review.
