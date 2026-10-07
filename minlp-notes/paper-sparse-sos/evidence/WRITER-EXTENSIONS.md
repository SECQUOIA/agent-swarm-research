# Sections 8–9 writer record

Date: 2026-10-05. Sol fallback author, explicitly authorized by the user after the original Opus author encountered the Claude API rate limit. This file is process evidence, not submission text.

## Completed files

- `sections/08-extensions.tex`: polynomial-constraint rounding in both cones; global feasible repair; common concave Slater regime; local-versus-global counterexample; finite-state preorder and accepted ordinary-module extension; real labelled certificates after justified label pruning.
- `sections/09-certificates.tex`: unified full-basis rational Gram witness theorem; explicit diagonal certificate of one; rational moment outer bound; global coefficient right inverse; exact rounding/correction and denominator bound; checkable approximate-Gram conversion; rational gap budgets at both box rates.

All proofs are inline. No Appendix C is required. No placeholder or unfinished proof is present. No bibliography, shared macro, other writer's source, original research note, experiment, or unrelated file was changed.

## Binding sources and mathematical dependencies

Read `AGENTS.md`, `evidence/BRIEF.md`, `evidence/ARCHITECTURE.md`, `macros.tex`, Sections 2–4, `evidence/AUDIT-EXTENSIONS.md`, `evidence/reviews/developments-sol-r1.md`, and `evidence/LITERATURE-PRELIMINARY.md`.

Primary proof sources: `research-20260928/solver/general-constraints-kernel.md`, `mixed-discrete-extension.md`, and `rational-sparse-certificates.md`; targeted accompanying prior/review documents were read. The manuscript incorporates the independently accepted exact-density domination and label-mass-scaled correction developments from the audit and development review. No independent literature research was performed; all source requests went to root for the designated shared Luna researcher.

Section 8 depends on these existing manuscript interfaces:

- Section 2: junction trees, coefficient budgets, Chebyshev multiplication, degree-preserving interval positivity, mass-homogeneous Chebyshev moment bounds, PSD Cauchy–Schwarz, tree gluing, and the finite-SDP Slater theorem used for the separately justified pruned labelled SDP.
- Section 3: the Jackson kernel and its preordering certificate, exact normalization, diagonal multipliers, and compatible local density proof.
- Section 4: the SOS kernel and normalized signed kernel, residual product proof with its degree ledger, the common correction theorem, and the explicit fixed-width parameter choice.
- Section 6: `thm:affine-sharp` for the limited statement that power one is sharp over the broad global-linear-error class. Section 8 itself proves no new lower-bound example.

Section 9 depends on Section 2's **box-only** real dual attainment and Sections 3–4's cone-specific gap bounds solely to derive its real finite-cone membership promise. The rationalization proof itself needs no tree. It treats full monomial bases for the unlabelled box preordering or ordinary box module, with no additional polynomial-generator or labelled blocks.

## Proof choices and safeguards

The constrained model uses the global residual `V=sum(-g)_+^2` and global bound `dist_2(x,K)<=H V^(alpha/2)` on the whole box. Separate local error bounds are explicitly insufficient. The common Slater sufficient condition is proved by interpolation. Global repair is proved with finite nets and a weak limit rather than an unspecified efficient projection routine.

The constrained preordering includes `g` times every box-preordering product used by the kernel and reserves `d` source degrees, with `r>=max(2d,d+w)`. Its violation residual is evaluated only through degree `2d<=r`.

The constrained ordinary module reserves `r>=wD+2d`. Its divided-difference certificate stays in the ordinary module through degree `2deg(g)`, and its squared-displacement certificate uses degree `D+2`. The corrected density dominates `h/(1+Delta_w)`, with a nonnegative remainder of known mass. One exactly glued global law therefore has objective error `O(log^3 r/r^2)` and squared violation `O(log^2 r/r^2)`. Global repair yields `O((log r/r)^alpha)`. No constrained dual-attainment inference is made.

Finite-state separator equalities sum over every separator-label fiber, including absent fibers. The ordinary correction is `Delta_w*tau_{b,a}`, with one denominator and correction constant everywhere. Zero label mass implies the entire functional vanishes through degree `2r`, proved from PSD and the exponent split. Empty continuous bags use an empty tensor product. The all-discrete hierarchy is exact at order zero and explicitly overrides Section 2's standing `w>=1`, `r>=1` conventions, without using `r/w`. Label-dependent constants cancel, and the data-only error is distinguished from the family-dependent mass-weighted error.

Label pruning is justified by discrete mass gluing and whole-functional vanishing. A strictly positive distribution on all global permitted assignments, independent of product continuous measure, supplies primal Slater for retained blocks. Only the pruned SDP's attained real dual is claimed, as a labelled polynomial identity on the permitted assignment space.

For rational witnesses, positive finite-order real membership of `p-tau` is the prerequisite. The diagonal complement identity builds `H>=I/D_C`. Product-uniform rational moments give an explicit polynomial-bit outer bound. Monomial pivots in the empty-generator blocks give a global right inverse, including overlaps. The corrected denominator divides `2*lcm(2^B,input coefficient denominators)`, retaining the necessary extra factor of two. Exact coefficient matching and rational PSD checks independently verify any returned witness.

The ordinary rational majorant replaces the irrational square-root term by `2(D+1)*delta`, retaining the same asymptotic rate. Generic rational recovery and the ordinary cone restriction are attributed modestly to prior methods. The current text states polynomial-bit witness existence, conversion conditions, and verification only. It does **not** state unconditional polynomial-time construction: that remains dependent on Luna supplying an exact rational unknown-center strong-feasibility theorem. No original-input polynomial-time or practical solver claim is made.

## Citation dependencies sent to root

Provisional Section 8 keys: `tran2026-moment-sos-approximation`, `heijmans2026-degree-bounds`, and the existing `korda2025-convergence-rates-sparsity`. The first two identify the primary sources already retained in `general-constraints-prior.md`; Luna may replace them with canonical keys.

Section 9 uses the preliminary canonical keys `peyrl2008-computing-sum-of-squares-decompositions` and `davis2024-rational-dual-certificates-for-weighted`. Their exact metadata and source locators remain owned by Luna. The writer requested confirmation and the optional strong-feasibility source through root. No bibliography write or literature search occurred.

## Targeted validation actually run

The following command was run twice from `paper-sparse-sos`, with the second stdout redirected to `/tmp/extensions-writer-check.console`:

```text
pdflatex -interaction=nonstopmode -halt-on-error -jobname=extensions-writer-check -output-directory=/tmp '\documentclass[11pt]{article}\input{macros}\begin{document}\input{sections/02-setting}\input{sections/03-kernels}\input{sections/04-ordinary}\input{sections/08-extensions}\input{sections/09-certificates}\end{document}'
```

Both passes exited zero and produced the targeted 34-page PDF. After the second pass, all references internal to Sections 8–9 and their included Section 2–4 dependencies resolved. Excluded sharpness/recourse references and bibliography citations remained undefined as expected for this partial harness, which intentionally has no bibliography. Its one overfull box is in the inherited Section 4 constants display at line 77; no Section 8 or 9 overfull/underfull box or duplicate label was reported. This is a TeX integration check, not a mathematical theorem check or a full manuscript build.

Also run:

```text
rg -n 'Overfull|Underfull|undefined|multiply defined|Fatal|Error' /tmp/extensions-writer-check.log
 git diff --check -- paper-sparse-sos/sections/08-extensions.tex paper-sparse-sos/sections/09-certificates.tex
wc -l -w paper-sparse-sos/sections/08-extensions.tex paper-sparse-sos/sections/09-certificates.tex
```

The whitespace check exited zero. The draft count was 650 lines / 3,589 words in Section 8 and 337 lines / 1,935 words in Section 9 (987 lines / 5,524 words total). No experiment rerun, project-wide verification, CI inspection, or commit was performed. Historical research-checker records were read as evidence and were not represented as checks performed by this writer. Root will assign independent manuscript review of these drafts.
