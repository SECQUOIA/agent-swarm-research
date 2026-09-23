# Stage 6: root investigation

Stage 6 began only after stage 5 closed with all accepted repairs checked. Sole author is `/root/stage06_author`. Root independently investigates proofs, sources and selected checks. This record is not a verdict on an unfinished manuscript.

## Initial full reads

Root read the physical degree-two price-response note, the full vertex-forcing note, the fixed-quality-alphabet note, the general parametric-path obstruction, the complete rank-one slab note, the fixed-interaction-rank cost result, and the convex-leaf arithmetic-barrier note.

- The physical descending path is affinely equivalent to the stated Klee–Minty cube. Standard output prices telescope to the dense right-flow objective with only the terminal price varying. The upper-only linear family uses an exact polyhedral repair bound and a uniform revenue bonus; this proof does not remove contracts from the nonlinear family.
- Reset outputs enforce equal adjacent signals while changing the supplying quality. In the nonlinear economics, the nonzero coefficient may sit on a reset duplicate, but its equality with the free signal preserves the telescoping objective. Two complete input qualities suffice for linear response; the active pool interface uses three.
- The pool interface has exact throughput one, quality `2-t`, and clean flow at least `t-t^2`. The new mass and upper-quality rows are correct; every other interface flow is affine in the path endpoint. The full graph has one undirected cycle and total input/output degrees at most two.
- The nonnegative telescoping factors vanish exactly at conditional endpoint patterns. Distinct patterns give distinct terminal values because lower/upper ranges are disjoint and their recursions invert. The perturbation's edge derivatives are strictly negative, and tangent-cone generation extends this to strict local optimality. The positive clean-flow cost transfers the property to the original physical feasible set.
- The parity argument applies to the complete optimal set, not its convex hull. Its matching integer-dimension upper construction may have exponential size. The exact LP hull has lower boundary equal to the affine vertex interpolation and upper boundary one; every hull vertex is physically feasible. This proves polynomial optimization over this particular nonlinear family and prevents an unwarranted hardness inference.
- The abstract slab reduction uses two sides of one dense aggregate, an exact zero threshold, and ordinary subset-sum encoding. Padding fixes local coefficients while preserving the endpoint certificate. It has no physical degree-two aggregate realization. The alternative parabolic exposing proof is a direct consequence of the same identity.
- The cost theorem's two projected boxes have fixed dimension for fixed interaction rank. A slice vertex lies on a box-image edge or original vertex; enumerating additional vertex-pair segments is sound because those segments remain feasible. Paired affine margin witnesses give `alpha*S+beta+gamma/S`, with at most one square root at an interior minimum. Zero-total continuity follows from the cost bound proportional to total mass. The fixed-attribute Lagrangian oracle has precisely the remaining margin/rank constraints and does not imply strong duality or tractability of the original constrained pool.
- Convex singleton leaves can encode independent square roots and one linking sum. This is a Square-Root Sum arithmetic barrier, not an NP-hardness assertion.

## Work in progress

The author handles primary shadow, parity, low-rank cost, and related local-optimum sources. Root is independently checking conic/network-simplex source scope. Root also fully read the correlation-face exact conic-lower-bound note: the normalized binary trace face, paired supports, affine inverse, exposure bound, conic-section transfer and nonpolyhedral caveat check algebraically. External lower-bound constants/versions still need source checks.

## Fresh finite checks

Root read each of the following existing scripts completely before execution. All runs exited successfully; their logs are under `verification/logs/`.

| Log | Exact finite evidence |
|---|---|
| `stage06-shadow.txt` | 8190 vertex/exposing-parameter checks and 8178 ordered breakpoints, through dimension 12. |
| `stage06-physical-penalty.txt` | 252 positive primal/dual certificates for original upper-only physical path rows, using the theoretical uniform penalty. |
| `stage06-fixed-alphabet.txt` | 252 original-network positive dual certificates, including relaxed reset contracts, two input qualities and upper bounds only. |
| `stage06-rank-one-slab.txt` | 2246 identity/interior/tangent checks, 661 subset-sum targets, 1016 padded endpoint identities and 661 fixed-coefficient targets. |
| `stage06-strict-local.txt` | 2044 distinct local-optimum values and 18432 negative directed-edge derivatives. |
| `stage06-rank-one-costs.txt` | 160 greedy-envelope versus exhaustive-pattern comparisons: 111 feasible and 49 infeasible; irrational, zero-only and singleton-total regressions. Both routes share the elementary total minimizer, so this principally tests candidate enumeration. |

At the author's suggestion, root added `verification/check_interaction_rank_two.py`. It uses independent original margin-vertex enumeration as the reference for projected-box vertex-pair candidates on rational total slices. Numerical HiGHS proposes whether a projected corner is a vertex; every classification is accepted only after an exact rational exposing-vector or convex-combination certificate. Margin lifts, all bounds, totals and objective comparisons are exact. The first random fixture passed objective comparisons but failed a coverage assertion because it produced no redundant projected corner. Adding an explicit five-moving-generator case exercised that branch; this was a test-fixture correction, not a manuscript or theorem correction.

The final run passed 24 interaction-rank-two instances and 104 total slices, with 342 exposing certificates, 8 convex-combination certificates, 4 singleton boxes and 2 zero-total slices. It did not test an infeasible total interval in that sample. The log is `stage06-interaction-rank-two.txt`. Dependencies are NumPy, SciPy and SymPy. This checks the projected-candidate mechanism, not the full global stationary-point search or the asymptotic zonotope-enumeration algorithm. Finite checks supplement proofs and do not certify them.

## Draft and source checks before first review

Root read the complete introduction and Section 6. The first force build succeeded at 90 pages; the author is repairing table spacing before freeze. The primary price-response direction is now the telescoping direction, with revenues bounded by three and penalty `3*N^N+1`. The previous exact penalty scripts use the published smaller-price direction and penalty `2*N^N+1`; they do not separately test the new numerical coefficient. The same proved uniform repair argument supports it.

Root read the original-network `physical_vertex_forcing_check.py` and ran it successfully: 252 endpoint extensions recovered their unique path vertex and zero economic profit, and 18 interior terminal values had strictly negative best profit. These are floating-point LP checks of independently assembled physical rows, not exact global nonlinear certificates. The log is `verification/logs/stage06-physical-vertex-forcing.txt`.

The related network summaries match the canonical model and graph restrictions. Root checked the transportation embedding and parallel-path subset-cut proofs directly. De Loera and Onn's original published PDF confirms Theorem 1.1 and the layer-one injection in Section 3.3, printed page 816; DOI 10.1137/040610623. The compact disaggregated hull is compatible with original-coordinate universality and coefficient growth. General series–parallel graphs and slack-augmented inequality networks are not silently included.

Root checked the conic exact-face, stability and approximate-SDP canonical arguments algebraically, including the inverse-quadratic error threshold and the distinction between total SOC dimension and number of cones. Primary PDFs downloaded legitimately outside the manuscript folder confirm Fawzi–Parrilo arXiv:1311.2571v1 Theorem 1 and the SOC conversion (page 3 visually inspected), LRS author full version Theorem 3.8 equation (3.11), Theorem 5.3 and the exact 2/13 exponent, and BFPS author version Theorem 6 for fixed-factor approximate LP lifts. BFPS publisher metadata is Mathematics of Operations Research 40(3):756–772 (2015), DOI 10.1287/moor.2014.0694. The source-specific results do not alone imply the pooling-block approximation bounds; the separate stability and slack-transfer arguments are necessary and were read. No claim of new correlation-polytope lower bounds is made.

Source URLs: https://arxiv.org/pdf/1311.2571 ; https://www.dsteurer.org/paper/sdpsize.pdf ; https://www.bayesianestimation.org/paper/approxlp.pdf ; https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf .

After resumption, root verified the author freeze hashes and accepted earlier sections, then dispatched all 15 first-round reviewers. Rebuild succeeds at 90 pages with no undefined citations/references or overfull boxes. One mild underfull bibliography paragraph (badness 1205) remains; visual inspection of page 88 shows legible text within margins, so no repair is needed for that diagnostic. Intro table page 2 was visually inspected after ragged-right formatting. LRS equation (3.11) was additionally visually inspected on original PDF page 23. Static checks verify all labels and citation keys resolve.

Root read every round-1 report in full. Reviewer 03 supplied a distinct self-contained exact original-network reconstruction check, now preserved as `verification/check_stage06_physical_exact.py`, with its passing 4,482-case log. Root read the complete script: it assembles actual source/output totals, midpoint and interface quality masses, reset contracts, pool mass/quality balance, arc bounds and economics, then verifies the telescoping identity. Unlike the prior numerical interface LP check, it verifies rational feasible points directly; it does not enumerate all feasible points or solve the global nonlinear model. Reviewers 01 and 04 retain reproducible additional exact identity/edge checks within their reports.

Root visually inspected rendered stage pages 74–86 in contact sheets and found no clipping, overlaps or missing equations. Page 87 and the complete final document remain in the final visual-check scope. The 300 distinct repository paths in the coverage inventory all exist; no results/notes file matching the pooling filename family is absent from the inventory. This deterministic inventory check does not replace mathematical coverage review.
