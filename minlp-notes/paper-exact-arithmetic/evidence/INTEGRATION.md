# Integration decisions and outstanding checks

## Scope

Use evidence/coverage-map.md as the 97-entry result inventory. All 97 entries are in scope. Core exact-comparison, singleton/output, SOS-field/certificate, value/point, and recourse families belong in the main chapters and Appendices A–I. Quadratic arithmetic and certificate benchmarks Q1–Q12 belong in Appendix J; Q7 is a brief classical caveat. Appendix L includes Q13–Q14: nonconvex few-Hessian common-field, finite-infimum and attainment interfaces, and algebraic-cone exact feasibility, threshold and witness interfaces. This corrects the earlier classification of those two arithmetic developments as peripheral. The supplementary independent-block singleton expanded-output obstruction is included in Appendix J. Older FBBT and potential-flow application packages are motivation, not new proof dependencies.

## Accepted analytic improvements

1. Canonical quadratic-square Hessian Grams transform exactly under translation. For rational sum-of-square constructions, compute the rational Gram from the square factors directly. The previous second approximation and rational projection are unnecessary where covariance applies. Retain a complete proof of covariance and positivity.
2. The cyclic zero's local Hessian condition number has an analytic O(n²) bound. It is a condition number at the optimizer, not a uniform smoothness statement on a neighborhood.
3. The structured box QP interface has a self-contained admissible-vector proof and a 2n-pivot homotopy proof. This makes the required arithmetic operation bound explicit.
4. The structured deterministic box and polynomial-flow exact Boolean predicates compile to one PosSLP instance by the uniform integer sign compiler. This is a reduction-format consequence, not ordinary polynomial-time optimization or a lower bound for every structural subclass. Las Vegas rank sampling remains separate.
5. The previously pending small-vanishing-space SOS descent criterion has a new complete independent proof audit. Its abstract hypotheses are the theorem; finite cyclic stationary-space diagnostics are not promoted to a universal application.

## Manuscript integration requirements

- Every claimed repository theorem has a full paper proof or a precise established external theorem with a vetted input/output contract.
- Make source representation, supplied structure, and the cost of checking it explicit.
- Keep Hessian Grams distinct from ordinary polynomial Grams; full positive definiteness distinct from tensor-restricted positivity; and real SOS distinct from rational polynomial SOS and rational-function SOS.
- Keep equality upper bounds distinct from order-comparison hardness.
- Keep dimension-exponential lower bounds distinct from exponential bounds in total binary input length.
- Expanded minimal-polynomial or rational-coordinate output bounds do not exclude shared circuits or all implicit formats.
- General arbitrary-polyhedron deterministic comparison, general degenerate quartic comparison, general all-PSD Gram size, higher-dimensional degree maxima, coupled cubic completion without additional structure, and quartic recourse are explicit future questions. No claimed theorem may rely on a solution to one.
- The literature comparison credits established Newton/sign approximation, convex value optimization, error bounds, algebraic sampling, SOS descent, exact SDP/SOCP hardness, fixed-dimensional integer methods, and classical degree/topology results. Novelty is stated only for verified additional guarantees or restrictions.
- Source comparisons with Hesse's Redemption are version-specific. Its proceedings version is now published, but access and exact theorem comparison are being reconciled by Luna.

## Review sequence

After integrating the Opus chapters and the Luna source report, run independent Sol reviews by theorem family and an Opus whole-paper review. Resolve every substantive finding in a response record, then request fresh bounded review rounds for changed or disputed claims. Compile and run only targeted document checks. Record actual outcomes; do not reuse historical experiment results as checks rerun here.

## First actual-manuscript checks

Upper, reductions, and heights Opus authoring tasks completed. Independent
Sol manuscript reviews are running in parallel. Early repairable findings:
restrict circuit-output summaries to proved rational outputs; replace
nonsquare-dimension square-root constants by rational upper bounds in the
slack-gap proof; qualify validation complexity over general inputs rather
than fixed example families; the sqrt(2) X_1^2 example has a PSD, not PD,
full-basis Gram. These findings await complete reviewer reports and repairs.

The initial scoped source checker ran while drafts were incomplete: 24 input
files, 553 labels, 1416 references, 98 cited works; it failed on 2 unfinished
input files, unresolved labels in those drafts, and bibliography keys awaiting
Luna reconciliation. This is a diagnostic, not final verification. No
experiments, project-wide checks, or CI checks were run.

## Late integration pass (2026-10-05)

All original Opus authoring tasks completed. Sol round-two reviews passed the principal chapter proof chains. The independent Opus numerical review passed the mathematical proofs and requested precise attribution and comparison-scope changes. Those are assigned to the numerical repair writer.

Claude API rate limits stopped late framing repair, numerical repair, Appendix L writing and whole-paper review tasks. The user explicitly permits Sol fallback in that event; fresh Sol agents now own each of those scopes. This does not count the failed whole-paper Opus task as a completed review. A fresh Sol integration reviewer reconstructs the global interfaces, and actual Appendix L will receive independent proof reviews.

Luna verified GLS Theorem 3.2.1's acceptance at the queried current center, Remark 3.2.33's fixed-core cut contract, and Lemma 3.2.8's rounded encoding. EY2010 Lemma 5's bounded positive ordered circuit contract was also verified. Hesse comparison uses the inspected arXiv v1; the 2026 proceedings full text was not retrieved. Tutte1948 Theorem 3.6 is a valid directed matrix-tree source; its loopless contract is extended in the paper by explicit diagonal cancellation of loops.

Root corrected the Section 02 table caption to charge numerical degree D in the global-convex column. Root corrected Section 09's prime-denominator corollary to charge the binary length of arbitrary supplied c, rather than transfer the original family construction time polynomial in ell alone. These are output-contract repairs, not changes to the mathematical examples. Fresh changed-scope reviewers verify both.

The 20:40 scoped document diagnostic found 115 distinct cited keys, the expected not-yet-included Appendix L reference, and 69 bibliography keys awaiting the completed Luna lane consolidation. No other source-closure, label, or unfinished-text issue was found. This is not the final manuscript check.

## Critical KP formula grouping gate

The first Luna relay incorrectly omitted quantified-block dimensions from the KP witness bound. Root and the Appendix L writer independently rejected that with a repeated-square ray. A second relay placed the dimension factor outside the exponent of d. The cone reviewer rejected that form with a stronger variable-degree example: a convex singleton obtained by m repeated d-th powers has integer witness length d^(m-1), with one free integer coordinate, degree d and constant coefficient height. A bound polynomial in d with exponent independent of m cannot suffice. Luna is rereading the exact printed superscript grouping. This supersedes the preliminary relay quoted in the Opus final-review brief.

The paper needs atom-count independence with charged compressed block dimensions, never independence of quantified dimensions. A robust alternative is fixed-block quantifier elimination first, as a description-size argument only, followed by the quantifier-free KP witness bound. Appendix L remains open until the exact source contract and proof are repaired and independently rechecked. The nonconvex Q13 proof review passed; this gate concerns the cone Q14 witness-radius import.

## Resolution and final editorial pass

Luna magnified the original KP formula and confirmed the entire quantified-block product belongs in the exponent of d, as the counterexamples required. Appendix L now adopts the simpler weaker import: fixed-block quantifier elimination first, using per-atom degree and coefficient-height bounds independent of atom count, followed by the quantifier-free atom-count-independent KP witness bound. The resulting conservative radius exponent is unchanged. A fresh cone changed-scope review verifies the actual replacement.

The independent reader review passed after 17 local clarity corrections. They include threshold/range precision, chart-offset versus separation-constant notation, the exact Boolean equality test, the minimum in the interior-Gram determinant estimate, signed decomposition terminology, relation spaces versus certificate cones, scale and multiplier wording, and explicit core-face/free-coordinate/regularization/output explanations. None removes a result or replaces a proof with a historical check.

The 20:50 scoped document diagnostic covered 27 input files, 658 labels, 1765 references and 120 distinct cited works. Its only six errors are pending new Appendix L bibliography records. All source closure, labels, references, and unfinished-text checks passed. Root integrated 70 additional vetted records (119 available), preserving corrected existing author metadata and bibliographic version notes; the explicit comparison of existing metadata found only the retained Azam name, TeX accents and Chua series field, plus nonsemantic chunk comments. This remains an interim diagnostic, not final verification.

The user reported Claude limits reset. A NEW Opus whole-paper review round was commissioned with the full brief, previous findings/responses, all97 scope, actual Appendix L and source gate instructions. The earlier rate-limited task is not counted as a completed review.

## Current resolved gates (21:14 UTC)

The fresh cone review, its nested radius check, and the final integration review pass the actual QE-first Appendix L repair. The earlier KP gate paragraphs above describe the review history, not a current unresolved mathematical defect. All 97 developments are covered. All 125 bibliography records are integrated and all 120 cited keys resolve. The source check passes with 27 files, 658 labels, 1766 references and zero errors. The final typography build produces 322 pages without warnings. The bibliography has its own working contents anchor, editions print as words, and a smaller contents font removes a one-entry page. These last changes affect document layout and bibliography formatting only.

The remaining gates are the fresh Opus whole-paper review, Luna's final primary-source checklist, and final archive verification. Source-family, integration, readability and actual PDF layout checks have passed. No final submission-readiness claim is made before those remaining gates close.

## Final source and package gates (21:32 UTC)

All critical primary-source contracts passed. Source-only repairs now cite EGH1996 CB7 alone, cite the inspected Eisenbud–Harris1987 Proposition0/Theorem1/Lemma2.1 for minimal degree and quadratic curve ideals, remove an unread specific Harris definition locator, and remove the redundant unverified exact Heintz locator from the affine component/projection argument. The verified KPS2001 §1.2.1 and the printed argument suffice. No theorem statement or mathematical proof changed. Bibliography formatting preserves volume46part1 and the names Cayley–Bacharach and Pell. There are 126 bibliography records and 120 cited works.

The final 322-page PDF builds without warnings. The 30-file source archive passes CRC, byte-equality and inclusion checks. A fresh extracted-directory build passes without warnings and produces identical extracted typeset text to the repository PDF, including pagination. The source, coverage, layout, source-contract and packaging gates are closed. The fresh Opus whole-paper review is still running; final readiness and snapshot hashes await that result.


## Failed-review continuation cleanup and abstract precision

The failed Opus whole-paper round1 later had an automatic postterminal run
queued by nested-task callbacks. Its interim file is not a final review. Root
disposed stale task delivery and interrupted that later active run through
the supported thread-interruption tool; the distinct fresh round2 remains
active and owns the final Opus review. Other three rate-limited tasks have no
pending child runs and did not resume writing.

Root checked the interim's seven precision findings against the actual final
source. The equality/order distinction, Allender Turing attribution,
Slot–Steurer–Wiedmer encoding premise, AppendixL inclusion and interfaces,
Hesse AppendixC description, and reduction signal premise were already
repaired or covered by the completed reviews/source checks. Root made the
remaining abstract wording explicit: the random tilt returns the selected
optimizer of the tilted instance, correctly on every draw. This is a summary
clarification of the unchanged recourse theorem, not a new mathematical claim.
The previous archive/clean-build snapshot predates this last abstract edit;
root will refresh the final archive and comparison before delivery.


## Final closeout: 2026-10-05 22:33 UTC

The distinct Opus whole-paper R2 completed without a mathematical blocker.
Its four final presentation repairs pass both the independent Sol scope
review and the completed Opus R3. All 97 developments remain covered; no
uniform cyclic stationary-space equality or unpublished rank computation
is promoted to a theorem.

R3 closed the height–Mahler source record after checking its elementary
derivation. Its two remaining metadata items were repaired: GP/DMS entries
now print the exact inspected preprint versions and numberings, and Roman
numerals and eight named/acronym title fragments retain their case. Luna
records both journal texts as uninspected; the bibliography review accepts
the actual version notes and printed capitals. Its final refresh confirms
126 entries, 120 cited works and all 27 frozen TeX body hashes. No theorem
or proof changed after the accepted body snapshot.

The final PDF builds cleanly at 322 pages with empty author metadata. Final
bibliography pages and the accented-name correction were inspected. The
30-file archive passes integrity, source-byte equality and inclusion checks;
its clean build at /tmp/exact-paper-final-submission-cot9h0vp passes without
warnings. Its extracted PDF text matches /tmp/exact-paper-accepted-layout.txt
exactly. The final 32-file checksum manifest binds the sources, PDF and ZIP.
All recorded review, source, document and package gates are closed. No
computational experiment, mathematical script, CAS, project-wide check,
CI inspection, public submission, commit, PR or external message occurred.
