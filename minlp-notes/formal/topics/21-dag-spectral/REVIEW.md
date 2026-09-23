# Topic 21 review

Independent reviewers checked the source obligations before implementation,
then reviewed the proof groups and their integration. Each report identifies
its own scope; a local pass does not certify the whole-algorithm cost bound.
The final original-input execution review and all source-frozen checks passed.

| Review | Scope |
|---|---|
| [Source inventory](SOURCE-REVIEW.md) | The 33 frozen obligations and explicit exclusions |
| [Factorization](reviews/factorization.md) | Actual rational LDL factors, singular pivots, owner labels |
| [Normalization](reviews/normalization.md) | Maximum-volume existence, rational maps, reconstruction and identity floor |
| [Normalization assembly](reviews/normalization-assembly.md) | Actual original-input factors and successful enumerated trial |
| [Rounding and perturbation](reviews/rounding-perturbation.md) | Signed floors, differing path lengths, exact coordinate and PSD bounds |
| [Profile DP](reviews/profile-dp.md) | Actual stored representatives, feasibility, completeness and state counts |
| [Path integration and transfer](reviews/path-integration-transfer.md) | Rational labels, trial approximation and conditional finite-memory transfer |
| [Cover headline](reviews/headline-cover.md) | Original-matrix producer, all-target sandwich, kernels, empty cases and exact cardinality |
| [Criteria](reviews/criteria.md) | D/E/A guarantees, singular costs, pseudoinverse order and reuse |
| [Arithmetic foundations](reviews/bit-foundations.md) | Rational widths and local arithmetic execution bounds |
| [DP bit costs](reviews/dp-bit-cost.md) | Integer profiles, dictionary scans, owner tests and representation charges |
| [Exact E computation](reviews/exact-criteria-computation.md) | Computed root separation, exact ties, complete comparator trace and path sums |
| [Rational pseudoinverse execution](reviews/rational-pseudoinverse-execution.md) | Rational inverse formula, estimability and execution coupling |
| [Topological input](reviews/topological-input.md) | Computed ordering, original edge identities and raw graph headline |
| [Topological materialization](reviews/topological-materialization.md) | Cached endpoints, graph equality and scan counts |
| [Preprocessing execution](reviews/cover-preprocessing-execution.md) | Cached original factors, normalization, storage and accessors |
| [Basis execution](reviews/basis-input-execution.md) | Sorted labels, source reads, copied coordinates and forced owners |
| [Criterion selectors](reviews/criterion-selectors.md) | Actual candidate scans, original path evaluations and guarantees |
| [Weighted criteria](reviews/weighted-criterion-semantics.md) | Zero weights, infinite costs and polynomial weighted path selection |
| [Whole cover execution](reviews/whole-cover-execution.md) | Original-input construction, all trials, dictionary and recovery work |
| [Cost-observer evaluation](reviews/cost-observer-evaluation.md) | Proved compiler equality avoiding a width-sized allocation in the observer |

The implementation reviews caught gaps in the connection between counted
operations and returned values, and in charges for owner tests and table
access. These are implementation-accounting issues, not counterexamples to
the source's spectral-cover theorem. Initial findings and subsequent repairs
are recorded in the corresponding reports.

The final [verification record](VERIFICATION.md) distinguishes targeted
Lean builds, declaration axiom checks, kernel replay and independent
execution examples. No project-wide checks or CI inspection are performed.
