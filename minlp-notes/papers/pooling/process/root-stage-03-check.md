# Root stage 3 investigation

Stage 2 is closed. Root is independently checking the restricted-hardness stage while its sole author writes.

## Coverage recovery: weighted integer capacities

`notes/pooling-all-degrees-two-investigation.md`, lines189–222, develops a weighted integer-capacity extension of pure-mode normalization and identifies the unit-capacity family with a two-edges-per-color bipartite rainbow matching problem. This substantive development was not explicit in the initial coverage-table row; the row is now corrected and the author was told to retain the full proof.

The original restriction to nonnegative rational mode rewards appears unnecessary. In every feasible zero-bound point, positive restrictive-output flow `s` forces dirty intake `d=0`. Normalization then preserves `s` and `d` separately: if `s>0` retain clean-to-restrictive flow `s`; otherwise retain dirty-to-lax flow `d`. For costs producing `-alpha*s-beta*d`, this preserves cost for any signed rational `alpha,beta`. Given one allowed mode per pool, the capacitated bipartite flow polytope is integral for integer source/product/pool capacities; arbitrary rational edge weights do not change integrality. Its optimal integral solution weakly improves the normalized fractional objective. Thus this small strengthening is sound independently of nonnegative rewards. It does not establish integrality for arbitrary physical arc costs or convexity of the full pooling set. The author was asked to check this independently before inclusion.

## Initial mathematical reads

Read the complete orientation/degree-three result, all-four-degrees result, positive-tolerance proof, two-pool/two-output reduction, and represented positive-product FPTAS. The main identities and model scopes are coherent so far. In particular the tolerance cleanup loses at most `2n(eta+delta/eta)` and uses approximation gaps rather than an integral optimum identity at positive tolerance; the FPTAS requires the given polytope/function representation and `a>=1,b>=0`. Primary-source arithmetic and later copy-circuit proofs remain under investigation.

## Matsui source intermediate bound and its repair

Root read METR95-13's full extracted proof and viewed original PDF pp.3–4. Theorem 2.1 states a bound for any positive integer `p` that is false: set `n=5`, `p=2`, every `x_i=1/2`, every diagonal `y_ii=1/2`, and every off-diagonal `y_ij=0`, with `epsilon=1/4`. All source constraints (3) hold, but `Y-X^2=682-961=-279`, whereas the claimed lower bound is `-99/2`. The problematic step drops a factor `p^(2k-2)` without first checking the sign of the bracket. This is a defect in the inspected preprint's intermediate general statement, not a refutation of its large-parameter NP-hardness theorem or an assertion about an uninspected final journal correction.

The needed special case has a direct repair. At a rational vertex, every fractional coordinate lies in `[h,1-h]` with `h=(n^3)^(-n^3)` by a coarse integer determinant bound. Let `k` be the largest fractional index; McCormick rows make every term involving a larger (binary) index exact. Dropping nonnegative lower-index y terms gives

`Y-X^2 >= p^(2k-1) [p*x_k*(1-x_k) - (k^2-1)] >= p^(2k-1) [p*h/2 - n^2]`.

For `p=n^(n^4)` and `n>=5`, `p*h=n^(n^3*(n-3))>=n^3`, so the bracket is at least `n^3/2-n^2>1`. Thus the gap is strictly greater than `p`. Concavity of `Y-X^2` extends the bound from vertices to all feasible points of a no instance. A binary yes witness instead has gap zero. The downstream identity is

`UV-K=(Y-p)^2+4p^(4n)(Y-X^2-p)`.

For a binary yes point, `Y=X^2`, `X<=n*p^n`, and `(Y-p)^2<=n^4*p^(4n)+p^2<4p^(4n+1)`, giving `UV<K`; a no point has `Y-X^2>p`, giving `UV>K`. Both factors are positive because `V>=2p^(4n)-p-2n*p^(3n)>0`. All expanded coefficients have polynomial binary length. The author independently accepted and is writing this corrected source lemma. No general small-p claim is retained.

## Cubic edge-colored source

Read Section 5(A) and viewed original PDF p.26 of Chlebik–Chlebikova's author manuscript. It explicitly supplies the proper edge three-coloring of its three-regular graph and preserves the independent-set approximation gap; the construction does not merely promise colorability. This supports the precise source class used by the unit-capacity pooling reduction. Printed manuscript page locators must not be mistaken for final journal page numbers.

## Concrete positive-tolerance loss of integral optimality

Root developed a small exact boundary example, supplied to the author for independent verification. On `K4`, use matching colors `E1={(0,1),(2,3)}`, `E2={(0,2),(1,3)}`, `E3={(0,3),(1,2)}` and the merged-lax all-degrees-exactly-two construction. For any `0<delta<=1/2`, let pools 0 and 3 take clean `1-delta` and dirty `delta`, each delivering one unit to its restrictive product. Let pool1 take one dirty unit and send it lax; pool2 is inactive. Every source and output capacity holds; the shared dirty input for 0 and 3 uses `2delta<=1`. The restrictive outputs have quality exactly `delta`. Profit is `3+2delta`.

Every integral flow at these unit capacities has each active pool using one pure unit, and each positive restrictive product can receive only one such unit. Since `delta<1`, that unit must be clean. Thus every integral point is also zero-tolerance feasible and its profit is at most `3=n/2+alpha(K4)`. Positive tolerance therefore destroys integral optimality on this same family for every `delta` in `(0,1/2]`, not merely in an abstract nonfacial example. This does not assert its exact nonintegral optimum.

`verification/check_positive_tolerance_boundary.py` checks all physical constraints and profits at 12 exact rational tolerances and exhaustively enumerates all 625 integral pool routing choices per tolerance. It passes. This supplements the general symbolic argument.

## Supplemental exact verification runs

- `verification/check_matsui_source_bound.py`: printed small-p counterexample, 237 rational McCormick cases for the corrected retained-factor bound, and the large-parameter bracket for n=5,...,12 all pass.
- Existing constant-data arithmetic checker: 1460 multiplier/signed-row cases and Matsui normalization at n5,6 pass; log `verification/logs/constant-data-arithmetic.txt`.
- Existing penalty estimate checker: 500 exact radial/error cases, 183 nontrivial repairs, and12 explicit Hoffman-constant bit bounds pass; log `verification/logs/penalty-bound-exact.txt`.

These checks have distinct scopes. No solver run with a moderate experimental penalty is used to certify the large theoretical penalty.

## Physical-network verification and initial draft read

Root read the complete stage-3 draft before reviewer dispatch. A forced build produced 40 pages with no final warnings. The physical checks completed successfully:

- `code/pooling_all_degrees_two/independent_review.py`: 46 graph/coloring instances and 5152 original-flow LP branches, including mixed intakes and waste. The negative control without quality disjunction gives four on K4 instead of three. These are floating-point LP checks with tolerance `1e-8`.
- `code/pooling_bypass_copy/independent_constant_data_review.py`: 40 physical two-feed circuit LPs and 40 contract-completion LPs, including 9 feasible and 31 infeasible reference cases. Fixed alphabets and degree restrictions are checked. A threshold-comparator negative control changes infeasibility to feasibility. Exact normalization bounds were also checked at n=5,...,8; LP comparisons are numerical.
- `code/pooling_bypass_copy/check_fixed_exception_hardness.py`: 16 original physical Gurobi feasibility models matched exact reference answers and checked the five-exception count, exact ordinary contracts, fixed palette, and input/output degrees. The nonlinear solver checks supplement the symbolic equivalence proof.

Logs are retained under `verification/logs/degree-two-branches.txt`, `constant-data-physical.txt`, and `five-exception-physical.txt`. These finite experiments do not establish the universal complexity claims.

## New independent reviewer checks retained

Reviewer 01 independently enumerated 1,026 SAT/orientation/subdivision examples and solved 88 complete physical endpoint-branch LP problems across both layer placements with and without pool capacities. The executed script is retained as `verification/check_stage03_orientation.py`; only a provenance/limitations docstring was added by root. Enumeration is exact; the LP comparisons use floating-point HiGHS.

Reviewer 02 independently compared 48 signed weighted, integer-capacity physical LP families against exhaustive integral modes, including repeated mode endpoints and restrictive or zero arc capacities. The executed script is retained as `verification/check_stage03_signed_modes.py`, with only a provenance/limitations docstring added. Its captured log is `verification/logs/stage03-signed-modes.txt`. LP comparisons use tolerance `1e-8`.

Reviewer 07 preserved `verification/check_stage03_reviewer07_gadgets.py`, which passed 162 exact rational full/half/coupling/averaging/splitting checks. These scripts were not rerun merely for storage. The initial reports record their commands and verification limits.

## First-round root adjudication and repair check

Root read all 15 reports and accepted one major missing upper-only quality hypothesis and four consolidated minor corrections. The detailed adjudication and separate repair record are retained. Root inspected the entire repaired source diff, verified the unchanged accepted section and bibliography hashes, and checked the clean 40-page build. The second-round snapshot is frozen at `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40`.

Root visually inspected the repaired theorem statements on PDF pages 23–24 and the end-of-section table and bibliography on pages 38–39 (the latter before the final scope repair). No clipping, unreadable equation, or table-layout defect was observed on those pages. A full final-document visual inspection remains required after all stages.
