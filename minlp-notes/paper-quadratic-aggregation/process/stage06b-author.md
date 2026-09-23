# Stage 6b author report

Date: 2026-09-22. Status: complete author draft, ready for the required five
independent reviews. No subagents were used by this author. Stage 6's
accepted mathematical section and all concurrent formal files were preserved.

## Deliverable and independent investigation

`appendices/three-dimensional-span.tex` covers the newly discovered
many-constraint note and develops the coordinator's proposed counterexample
to its incomplete general-cone extension. It is a supporting appendix so
that the main narrative remains focused on the three conjecture questions.

The directional proposition gives at most `2|J_-(D)|` good cuts, where
the selected facets have negative evaluation on a positive definite
direction in the three-dimensional matrix span. The proof establishes
pointedness, the polygon section, equality of extreme-ray and facet counts,
preservation under deletion of redundant generators, and HHC via the
three-form theorem on each homogeneous hyperplane. It checks the exact
nonnegative-representation hypothesis of PSD improvement and explicitly
uses pair-support goodness with respect to the full original feasible set.
The conditional `2k-2` bound follows when the PSD cone in the span is not
contained in the negative coefficient cone. The unconditional `2k` bound
and the facet argument are credited to BDS, using **v2 Proposition 2.22**.

The centered ellipsoid example has a complete Vandermonde and boundary
witness proof. Exactly `k=m` original aggregation rays are necessary and
sufficient; every infinite strict description must also contain those rays.
For finite weak descriptions, the proof uses local strict slack and a
radial perturbation. It does not incorrectly extend ray indispensability
to infinite weak descriptions.

The new augmented example settles a specific proposed shortcut negatively.
Adding `-x1^2<0` and `-rho<0` changes the strict set but preserves its
ordinary hull by small generic midpoint perturbations. The weak set stays
unchanged. All `m` old rays remain exposed, the two added rays are extreme
by their zero constant coefficients, and the new cone has `k=m+2` rays.
An exact nonnegative combination produces the negative constant basis
matrix, so the cone contains the negative of the entire PSD cone in its
span. All old witness rays remain indispensable among *all* nonnegative
aggregation families, giving exact count `m=k-2`. The weak set is compact,
regular, has nonempty interior, and has no points at infinity. Thus a
general-cone analogue of BD's complementary-case **two-bound is false**,
even with its closed-set geometric hypotheses. This does not refute an
unconditional `2k-2` bound, which the paper does not assert.

No theorem in the appendix depends on an unfinished extension. The complete
unconditional theorem used is the prior `2k` upper bound; the directional
refinement and counterexample have fully stated, proved scopes. An optimal
general many-generator count is not claimed. The final remarks explain
why subsystem triangulation and arbitrary addition do not yield that count.

## Literature and scope

`stage06b-literature.md` records fresh primary-source inspection of the BDS
and BD preprints, the precise versioned locators, and search limits.
The appendix credits the prior facet geometry and does not claim a new
topological theorem or broad priority. The counterexample was independently
verified from `stage06b-root-development.md`, not accepted solely from its
finite numerical checks. No bibliography addition was needed.

The root's pre-freeze reading identified one grammatical issue, corrected
to “strictly feasible.” A preliminary build found an undefined `mathscr`
command; notation was simplified to standard `mathcal C_L` and
`mathcal P_L`, avoiding an additional LaTeX package. These authoring checks
do not replace the required five-reviewer stage.

## Targeted checks actually run

From the repository root:

```sh
python3 paper-quadratic-aggregation/supplement/check_three_dimensional_span.py
```

Passed after final script changes. The standalone standard-library script
checks the three-variable Vandermonde determinant, the ellipsoid witness
numerator, and the negative-cone relation as exact polynomial coefficient
identities. It also checks 1,235 rational witness evaluations for m=3,...,15
and strict signs of both added rows. The rational instances supplement
the manuscript's universal proof; no HHC, hull, facet, or priority claim
is inferred from samples.

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build/stage06b main.tex
```

Passed after the notation correction and final prose change. The final
stage PDF is `build/stage06b/main.pdf`, with build output in
`build/stage06b-author-build.log`. The author inspected the extracted
appendix text and rendered pages 34 and 36. The equations, theorem
statements, and page breaks were legible. Final log searches for Warning,
Overfull, Underfull, and undefined found no matches. UTF-8, terminal-newline,
and trailing-whitespace checks were included in the source snapshot step.

No project-wide verification, CI inspection, solver experiment, or Lean
rerun was performed. No external dependencies were installed.

## Handoff

Added the appendix, exact-check script, literature and author reports, and
snapshot. Updated the main input, supplement README, coverage/literature
records, and stage status. The five independent reviews must precede
acceptance. Synthesis, portable formal supplements, packaging, and
whole-manuscript review remain later stages.
