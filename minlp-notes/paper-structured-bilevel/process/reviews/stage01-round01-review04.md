# Stage 1, round 1: independent review 04

Recommendation: accept stage 1. I found no justified major or minor issue in the frozen stage. This recommendation covers the foundations and the completeness of the staged assignments; it does not certify the proofs assigned to later stages.

## Inspected source and independence

I inspected all five files in `process/snapshots/stage01-round01`: `main.tex`, `sections/01-foundations.tex`, `references.bib`, `README.md`, and `process/coverage.md`. The SHA-256 digest of `SHA256.json` is `2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`. Every listed file matched its manifest hash. The verification record is `verification/reviewer04/stage01-round01/snapshot-check.txt`.

I did not read other reports from this review round, delegate, or edit manuscript sources. I read `../literature/AGENTS.md` before consulting the literature packages and did not change generated literature files.

## Mathematical findings

- **Model and boundedness, foundations lines 89–133:** compactness of the leader set and continuity of the polynomial coordinate bounds do give uniform boundedness of the feasible follower union. Every nonempty fixed-leader feasible set is closed and bounded. Local positive definiteness is correctly distinguished from convexity of the full aggregate-coupled objective. Empty follower problems are permitted and handled explicitly.
- **Selection and feasibility, lines 135–190:** optimistic upper rows filter global follower responses, whereas pessimistic upper rows are universal over the complete response set. Infeasible leaders cannot pass by vacuous universal quantification. The compact fixed-leader response sets justify the stated adversarial maxima. Near-optimal responses are correctly defined by objective value rather than stationarity. The text does not assume leader attainment prematurely.
- **Encoding and output, lines 192–236:** the numerical degree parameter is explicit, with the necessary warning about sparse binary exponents. The common-field convention accounts for all recovered coordinates and distinguishes independently requested witnesses. The rational approximation guarantee refers to the true induced objective. XP-type dependence is not misrepresented as fixed-parameter tractability.
- **Algebraic tools, lines 240–252:** the claims use a fixed total number of real variables, rather than only fixed free dimension. The cited Basu–Pollack–Roy article actually contains Theorem 1.3.1 and Section 3.1.3, and its discussion supports quantifier elimination, realizable sign conditions, and univariate representations of samples.
- **Substitution lemma, lines 255–278:** the exponent `delta - |gamma|` is nonnegative; including the leader factor preserves the stated degree bound. Fixed dimension makes the expanded monomial count polynomial. Products of polynomially many rational factors also retain polynomial coefficient encoding length under the stated degree bound. Positive denominator clearing preserves signs. I additionally checked a mixed leader/follower polynomial symbolically and evaluated the sign identity at 25 rational points; this supplements the proof review rather than replacing it.
- **Hoffman bound, lines 280–293:** the constant is correctly uniform in right-hand sides for fixed normals, with nonemptiness stated. The text distinguishes an instance-wise existence argument from the quantitative bounds still owed by the approximation stage and does not extend uniformity to moving normals.

## Coverage and organization

The inventory includes all 14 `results/bilevel-*.md` files. A mechanical check found that all 72 explicitly backticked source paths or glob patterns resolve. More substantively, the coverage rows separately account for the supplied low-rank LP corollary; positive and signed monotone inverse lemmas; growing-leader vertex-integrity and parameterized boundaries; both the leader-interaction path and the Klee–Minty follower path; the affine-strip feasibility exception; and convex, nonconvex, and screening computations.

I compared the inventory with `notes/bilevel-paper-scope.md`, `notes/bilevel-response-complexity-map.md`, and the relevant closeout/status outlines. The staged order is meaningful: exact response compression precedes robustness, the accuracy stage explicitly closes its inverse and quantitative proof dependencies, and boundaries and computation have their own deliverables. The plan preserves unfavorable screening evidence, distinguishes independent fixed-price checks from a complete continuous-leader baseline, and does not promote diagnostic counts to formal verification. The fixed-core support-function framework and non-bilevel application exclusions are explicit.

The later abstract, integrated theorem overview, and future section inputs are intentionally assigned to later stages. Their absence is not a stage 1 defect. The eventual proofs and experiments must still meet their assigned coverage rows; mentioning them in this inventory is not evidence that they have been completed.

## Attribution and prose

The related-work prose makes the distinction between fixed follower dimension and fixed structural dimensions clear. Its scalar-leader linear hardness comparison retains coupled follower constraints. The description of Ketkov–Prokopyev does not silently extend their convex quadratic upper model, and the local/global distinction is explicit. The source positioning credits multiplier arrangements, algebraic computation, earlier approximation methods, and near-optimal robustness without using repository review reports as theorem authority.

I checked relevant passages in the local primary-source packages for Basu–Pollack–Roy, Ketkov–Prokopyev, Sugishita–Carvalho, and Megiddo–Tamir. The two version-specific preprint citations also match their official records: [Sugishita–Carvalho, version 2](https://arxiv.org/abs/2510.21126v2) and [Ketkov–Prokopyev, version 2](https://arxiv.org/abs/2511.15592v2). Publication prose is coherent and appropriately qualified for this foundation section. I have no optional wording preference that needs to become a correction requirement.

## Verification and limitations

The isolated copy at `verification/reviewer04/stage01-round01` builds with the README's `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` command. It produces a six-page PDF. The final log contains no warnings, undefined references, multiply defined labels, or overfull/underfull boxes. I also extracted and inspected the rendered text, including the bibliography. The build log is `isolated-build-command.log`, and the inventory/symbolic results are in `mathematics-and-inventory-check.json` in that directory.

One procedural limitation must be recorded: after copying the snapshot, I initially invoked `latexmk` from the manuscript root by mistake. That invocation exited successfully; I notified root, moved my command log to `initial-root-build-command.log` in the reviewer directory, and reran the full build from the isolated copy. I did not edit manuscript source files. The successful isolated build, rather than the accidental root invocation, is the build evidence for this review.

This was a review of the complete current stage, not a new audit of every future theorem's full source proof, every historical experiment, or every cited publication in full. No future theorem is accepted on the strength of this report. PDF layout checks used compiled text and TeX diagnostics rather than a page-by-page visual image audit.
