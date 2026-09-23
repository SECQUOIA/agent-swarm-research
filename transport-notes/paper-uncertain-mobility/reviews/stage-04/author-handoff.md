# Stage 04 author handoff

Status: author complete and ready for the coordinator to freeze the source and dispatch five independent reviewers. This is not stage acceptance. No later-stage work was started, no work was delegated, and the author has stopped editing manuscript sources.

## Files and scope

- `sections/04-generic-folds.tex`: new section, approximately five pages in the combined 30-page manuscript, proving claim G1.
- `main.tex`: includes Section04 after the accepted predetermined-design section.
- `notation.md`: adds generic-family density, values, and fold-distance notation. At the coordinator's request, its Stage03 constant status now points to that stage's acceptance.
- `claims-map.md`: records G1 as authored and awaiting review; changes X1's stale status to Stage03 accepted, without changing its mathematical content.
- `PLAN.md`: replaces the historical scaffold statement that no substantive stage was accepted with a link to the current review ledger.
- `reviews/stage-04/author-handoff.md`: this report.

The accepted Sections00–03, preamble, and bibliography were compared with the Stage03 accepted-snapshot hashes and remain byte-identical. No bibliography or literature package was modified.

## Development and verification

The section rederives the generic theorem from explicit sufficient assumptions, rather than importing the result from a repository note. The parameter density is named varpi to distinguish it from bulk concentration p; mobility normalization uses a_R, leaving A and Z with their established physical meanings.

1. The nonempty finite multiple-zero set consists of interior folds with nonzero gss and gc. Fold sites and fold parameters are each pairwise distinct. All other spatial zeros are simple. The density is bounded and positive almost everywhere on both sides near every fold. No positivity is required on unrelated regular parameter intervals.
2. A finite cover of the compact zero set, using fixed-sign gs at simple roots and fixed-sign gss at folds, proves a uniform root-count bound. The closed regular portion has a uniform slope bound. Compactness and exclusion of identically zero realizations prove uniform rate anchoring.
3. The fold coordinate is constructed explicitly: solve gs(z(c),c)=0, apply the second-order Taylor integral factor, and absorb its fixed-sign nonzero coefficient into the coordinate. The construction needs only a C2 coordinate, bounded Jacobians, a center shift of order parameter distance, and a nonzero derivative of the signed fold parameter. No high-regularity Morse theorem is invoked.
4. The zero curve c=C(u) has C'(sj)=0 and C''(sj)=-gss/gc, giving root-position probability proportional to r du. A sliding-bump quotient plus Tonelli and Jensen for a negative power proves the local bound r^(2-5q/4) m^(-q/4) for every positive q and every L1 field. Zero local mass is handled by shrinking tests. No coefficient regularity is assumed in the lower bound.
5. One fixed shell gives the subcritical lower order. Disjoint geometric spatial shells with disjoint parameter images share the total budget, producing the critical logarithm with exponent 7/5. A whole-budget fold bump of width M^(1/7), on a parameter window of width M^(2/7), gives the supercritical lower order.
6. The upper trial has exact mass M and grades distance to all known fold sites with exponent max(0,(6q-4)/(q+4)). The nonnegative exponent preserves a positive global floor, including at ordinary roots that are stationary in the parameter or happen to occupy another fold's site.
7. The response proof keeps ordinary-root and positive-potential contributions alongside the active fold contribution. It explains the uniform free-endpoint harmonic bound, the separated-root oscillator scale, the reciprocal-potential remainder, central quartic interval coercivity, and rootless bounds. The Taylor coefficients and scaled parameter in the central interval are explicit.
8. Integration checks every parameter contribution for every q>0. The endpoint exponent is positive below 8/5, zero at 8/5, and negative above. At q=2/3 the possible rootless logarithm is lower order. At q=8/5 the central/rootless terms contain one fewer logarithmic factor than the main term. Above 8/5 the regular-root term is lower order.
9. Uniform anchoring verifies the accepted physical transfer theorem. Since each optimized scalar order dominates the logarithmic bulk moment, the generic full-bulk optimum is asymptotic to chi^q times the scalar optimum at fixed positive bulk diffusivity and nonzero V. This does not assign a sharp numerical coefficient to the generic scalar order.

No unresolved mathematical gap is known to the author. The main independent-review targets are the compact regular-root partition, arbitrary-design shell averaging, the global lower floor protecting extra roots, and uniform central-window coercivity. Matching scales were checked analytically; a numerical experiment is unnecessary for this order theorem and none is claimed.

## Source and novelty boundaries

Read the accepted model/transfer, local-baseline, and predetermined-design sections, together with `notes/generic-kinetic-folds.md` and `notes/review-generic-kinetic-folds.md`. The latter are leads, not cited substitutes for the manuscript proof.

No new external citation is needed for the direct Taylor-coordinate construction. The section makes no novelty claim about normal forms, variational compliance, or the general selection of moment behavior by rare degeneracies. The coordinator's current-stage literature check of Berry–Keating–Schomerus (2000) is consistent with this scope; the complete primary-literature comparison remains Stage07.

The theorem does not extend to simultaneous or spatially coincident folds, singular/vanishing sampling density, higher-order degeneracies, uncertain fold sites, mobility caps, fixed spatial resolution, vanishing bulk diffusivity, or zero mean velocity. It does not assert a generic sharp coefficient, unique design, bounded bulk remainder, or convergence of every order-optimal trial.

## Build and source checks

Command, from the manuscript directory:

    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex

The combined manuscript builds to 30 pages. The final log contains no warnings, undefined references, overfull boxes, or underfull boxes. An initial draft had missing backslashes in several quad spacers and an invalid multi-label eqref; the author corrected these before handoff and checked explicitly for recurrence. Source checks cover the untracked changed files directly and report no trailing whitespace. The author visually inspected PDF page26, containing the generic geometry and normal-form proof; its equations and text are legible and within the margins.

The coordinator may now freeze the source and start the five-reviewer round.
