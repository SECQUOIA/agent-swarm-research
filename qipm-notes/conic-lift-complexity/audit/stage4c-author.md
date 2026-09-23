# Stage 4C author completion

Status: complete, integrated, and frozen for five independent reviews. No formal review is claimed by this author audit.

## Files

New main-text sections:
- `sections/10a-nonsymmetric-barriers.tex`
- `sections/10b-entropy-aggregation.tex`
- `sections/10c-conditioned-approximation.tex`
- `sections/10d-exact-compilers.tex`
- `sections/10e-projected-compilers.tex`

New appendices:
- `sections/10f-approximation-refinements.tex`
- `sections/10g-conditioning-counterexamples.tex`

Integration edits: `main.tex`, `bibliography.bib`, `audit/source-map.md`, `audit/workflow.md`; regenerated PDF and ordinary LaTeX auxiliary outputs. Detailed audits: `stage4c-barriers.md`, `stage4c-barriers.bib`, `stage4c-entropy-conditioning.md`, `stage4c-approximation.md`, `stage4c-compilers.md`, `stage4c-projected.md`; build log `stage4c-build.log`.

No reviewed earlier section was edited. No existing manuscript, workbench file, literature package, or `formal/` work was changed. All Python scripts used the project qipm interpreter.

## Work allocation and independent author examination

Four bounded author helpers developed disjoint nonsymmetric-barrier, approximation, exact-compiler, and projected-compiler files. This author developed the entropy and conditioning sections, integrated references, and read every new section and all helper audits. The root also made preliminary independent checks during writing. Those checks do not replace the user's required five formal reviews after author completion.

Fifteen complete original workbench notes are accounted for in the source-map stage disposition. Earlier reviewed results are referenced rather than copied. Long global approximation and conditioning extensions are appendices; there is one appendix boundary in main.tex.

## Substantive developments and corrections

1. The product-cosh epigraph factor count is strengthened from r-1 to r by retaining the full r-dimensional positive-curvature graph under a compact polyhedral truncation. No global selector assumption is imposed; arbitrary affine maps and free variables are allowed through the foundational reduction. The artificial truncation ray is not charged to the original product barrier.
2. The smooth near-complementarity approximation is sharpened by deleting the unnecessary alpha beta gamma error term. The global canonical projectors retain the sharper estimate and correctly supply continuous bundles. The finite-stencil theorem is separate.
3. Positive-output entropy aggregation's intrinsic parameter remains 2N+B even with zero columns, but the source's claimed exact exponential lift fails there. The corrected lift uses exponential cones only for active columns and two rays for every inactive input pair. The exact ambient parameter is 2N+n_++B. The elementary counterexample A=0, x=1,y=0,z=0 and a full finite-boundary-fiber proof are included.
4. All Hildebrand product lower bounds retain logarithmic homogeneity. For norm cones with p>2, dualize the whole product; scalar power cones use the positive branch after axial exchange. Characteristic-family necessary parameters are not promoted to universal optimal parameters, and differentiated asymptotics are proved through order three with an integrable dominator.
5. The classical optimal barrier problem is not purportedly resolved. Quantitative h(p)>2 proves an infimum gap; the elementary parameter-two classification alone proves only nonattainment. Explicit ansatz failures and finite-parameter oracle scope are fully developed conclusions.
6. Recourse compilation retains lineality equations and uses effective rank for ray counts. Canonical recourse requires strict positivity, and singular quadratic statistics are quotiented or augmented by X0 barriers. Gram and LP quantum reductions have actual published precision/access/initialization hypotheses.
7. Approximation-to-conditioning implications are explicitly delimited. Schur invariance does not imply raw KKT spectral invariance, and bounded pointwise IPM geometry does not control changing-label derivatives. Square-root interpolation requires its optimizing radius to fit; H=0 retains the infimum formula.
8. Simultaneous minima have a logarithmically amplified upper bound; no unsupported exact Theta query equality is asserted. Reusable quantum summaries have a joint operational reuse contract, not an assumption that one state can be consumed repeatedly.
9. A simpler one-sided KL example provides the source's constant-barrier versus oracle-access separation transparently. The corrected Umegaki divergence convention has its exact additional trace-Y term.

## Literature and novelty

The local literature is read-only. Each bounded audit lists actual primary sources and retrieval limitations. FS2023 is explicitly credited for the general compatibility and recession optimality machinery. He–Saunderson–Fawzi 2026 and Chen–Goulart 2025 are credited for positive-map entropy structure and sparse Hessians. Gouveia–Parrilo–Thomas 2015 is the comparator for approximate cone factorizations; the new conditions concern curved contacts and relative derivatives/increments. Vector-lattice and finite translation-space classifications, classical query primitives, and quadratic Schur barriers are attributed. No priority is inferred from a negative search.

The final published Apers–Gribling reference is SIAM J. Comput.55(1)(2026)93–134, DOI10.1137/25M1736098. Its published LP theorem is 1.3, not preprint theorem 1.1; Theorem3.1 is the Gram approximation result and Theorem6.1 gives the initialized implementation. These precise distinctions are recorded for later stages.

## Validation and scope

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completes. The final integrated manuscript has no undefined citations/references, duplicate labels or bibliography keys, or overfull/underfull warnings. Final page count is recorded in the build log and handoff.

The stage has no author TODOs or unproved claim used as a theorem. Exact nonsymmetric optimal parameters, unconstrained approximate lift classification, and a bridge from cross-label sensitivity to a fixed-formulation KKT lower bound are expressly outside the conclusions; they are not hidden premises. Stage5 movement, ledgers, active compilers and readout, final introduction/coverage/packaging, and the whole-manuscript review remain authorized root tasks.
