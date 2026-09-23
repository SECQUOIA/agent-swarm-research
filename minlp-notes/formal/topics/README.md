This index separates each Lean verification topic from the corresponding paper.
A completed entry means its listed formal statements have passed the checks
recorded for that package; it does not mean every claim in the paper has been
formalized. Local work uses targeted checks; CI handles project-wide
verification. Do not run project-wide verification locally or check CI.

| Order | Topic | Proof namespace and directory | Status |
|---|---|---|---|
| 0 | Exact convex integer/binary counts, including monotone extension | `ExactCounts`, [`Formal`](../Formal) | Completed; [package](00-exact-counts/README.md), [coverage](../COVERAGE.md) |
| 1 | Switching control | `SwitchingControl`, [`Formal/SwitchingControl`](../Formal/SwitchingControl) | Verified; [record](01-switching-control/VERIFICATION.md) |
| 2 | Primitive FBBT lower bound | `FBBT`, [`Formal/FBBT`](../Formal/FBBT) | Verified; [record](02-fbbt/VERIFICATION.md) |
| 3 | Potential-flow certificates | `PotentialFlow`, [`Formal/PotentialFlow`](../Formal/PotentialFlow) | Verified; [record](03-potential-flow/VERIFICATION.md) |
| 4 | Cubic relaxation-gap witnesses | `CubicGap`, [`Formal/CubicGap`](../Formal/CubicGap) | Verified; [record](04-cubic-gaps/VERIFICATION.md) |
| 5 | Reciprocal-anchor hulls | `ReciprocalAnchor`, [`Formal/ReciprocalAnchor`](../Formal/ReciprocalAnchor) | Verified; [record](05-reciprocal-anchor/VERIFICATION.md) |
| 6 | Network–simplex hulls | `NetworkSimplex`, [`Formal/NetworkSimplex`](../Formal/NetworkSimplex) | Verified; [record](06-network-simplex/VERIFICATION.md) |
| 7 | Positive multilinear uniform-gap conjecture disproof | `MultilinearGap`, [`Formal/MultilinearGap`](../Formal/MultilinearGap) | Verified; [record](07-multilinear-disproof/VERIFICATION.md) |
| 8 | Exact finite multilinear hull-gap formula | `MultilinearGap`, [`Formal/MultilinearGap`](../Formal/MultilinearGap) | [Package](08-exact-multilinear/README.md); [verified](08-exact-multilinear/VERIFICATION.md) |
| 9 | Sharp multilinear degree and dimension growth | `MultilinearGap`, [`Formal/MultilinearGap`](../Formal/MultilinearGap) | [Package](09-sharp-multilinear/README.md); [verified](09-sharp-multilinear/VERIFICATION.md) |
| 10 | Complete mathematical coverage of the standalone multilinear paper | `MultilinearGap`, seven completion modules | [Package](10-multilinear-completion/README.md); [verified](10-multilinear-completion/VERIFICATION.md) |
| 11 | Complete focused cubic bounds and paper | `CubicGap`, thirteen completion modules | [Package](11-cubic-completion/README.md); [verified](11-cubic-completion/VERIFICATION.md) |
| 12 | Sharp marginal-floor multilinear gaps | `MultilinearGap`, `Formal/MultilinearGap` | [Package](12-marginal-floor/README.md); complete and verified |
| 13 | Many-leaf reciprocal-anchor hull | `ReciprocalAnchor.ManyLeaf`, `Formal/ReciprocalAnchor/Many*.lean` | [Package](13-many-leaf-reciprocal/README.md); complete, targeted checks passed |
| 14 | Certified MINLP mathematical soundness | `CertifiedMinlp`, `paper-certified-minlp/formal/CertifiedMinlp` | [Package](14-certified-minlp/README.md); complete, targeted checks passed |
| 15 | Flat-chain network–simplex threshold | `NetworkSimplex`, `Formal/NetworkSimplex` | [Package](15-flat-chain-threshold/README.md); complete |
| 16 | Deterministic potential-flow certificates | `PotentialFlow`, [`Formal/PotentialFlow`](../Formal/PotentialFlow) | [Package](16-potential-flow-certificates/README.md); complete, independently reviewed |
| 17 | Arbitrary-grid one-switch minimax and sharp grid transfer | `GridSwitching`, [`Formal/GridSwitching`](../Formal/GridSwitching) | [Package](17-grid-switching/README.md); complete, independently reviewed |
| 18 | Positive-box multilinear gap aspect-ratio bounds, finite-dimensional refinement and original-box transfer | `MultilinearGap`, [`Formal/MultilinearGap`](../Formal/MultilinearGap) | [Package](18-positive-box/README.md); complete, independently reviewed |
| 19 | Structural multilinear gaps: feedback, frequency two and incidence treewidth two | `MultilinearGap`, 66 structural modules | [Package](19-structural-multilinear/README.md); complete, independently reviewed |
| 20 | Scalar quadratic precision: sharp square law, rank/inertia laws and finite linear constructions | `QuadraticPrecision`, 57 modules | [Package](20-scalar-quadratic/README.md); complete, independently reviewed |
| 21 | DAG spectral approximation sets: original-input construction, singular ranges, size and bit-work bounds, criteria and conditional transfer | `DAGSpectral`, 124 modules | [Package](21-dag-spectral/README.md); complete, independently reviewed |
| 22 | Represented-matroid spectral approximation sets | `MatroidSpectral`, 65 modules | [Package](22-represented-matroid-spectral/README.md); complete, independently reviewed |
| 27 | Quadratic aggregation certificate equivalence, HHC specialization and supporting cone/hyperplane lemmas | `QuadraticAggregation`, 11 modules | [Package](27-quadratic-aggregation/README.md); complete, independently reviewed |
| 28 | Closed-system and Shor consequences, exact finite SDP characterization, and boundary examples | `QuadraticAggregation`, 10 new modules | [Package](28-quadratic-aggregation-consequences/README.md); complete, independently reviewed |
| 29 | Infinite aggregation: HHC, spectral goodness, indispensable strict rays, finite closed-hull obstruction | `InfiniteAggregation`, 18 modules | [Package](29-infinite-aggregation/README.md); complete, independently reviewed |
| 30 | Exact aggregation hulls, finite SDP lifts and weak-system hull equality | `InfiniteAggregation`, ten new modules | [Package](30-infinite-aggregation-hull/README.md); complete, independently reviewed |
| 31 | Finite aggregation accuracy, rational constructions and coefficient-size bounds | `InfiniteAggregation`, fifteen new modules | [Package](31-aggregation-accuracy/README.md); complete, independently reviewed |

The [recommended-topic sequence](../RECOMMENDED-TOPICS-PLAN.md) lists all later
topics and their order. Topics 00–22 are complete within their listed scopes;
topics 23–26 remain queued. Topic 27 was separately prioritized by the user
and is complete within its stated scope.

Each new topic has its own explanation, claim-to-theorem coverage table, and
verification record in its numbered folder. Topics in the canonical project
share the pinned Lean and Mathlib installation under `formal/`.
[Certified MINLP](../../paper-certified-minlp/formal/README.md) has a separate
formal project and its own checks, as do the standalone paper exports.
Each project's import and axiom audits cover its proof modules, including
private declarations. The topic records identify the checks performed;
completion does not imply that every extension received a new full-project
kernel replay.

`bash scripts/verify.sh` from `formal/` is the full-project CI/reproduction
entry point. It is not a local development requirement.
