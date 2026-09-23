# Current topic coverage

Stages 1–8 are complete and accepted, including the separate five-reviewer whole-manuscript round.
The historical inventory and stage-by-stage mapping are preserved in
`coverage-through-stage06b.md`. The table below supersedes its pending-status
language and maps every relevant development to the current manuscript.

| Repository development | Manuscript destination and treatment |
|---|---|
| `results/quadratic-aggregation-trivial-hull-certificate.md`: definitions, HHC question, AHC, no negative leading direction, sweeping, nonzero limit, uniform-cone alternative | Sections 2–3, with complete coefficient-normalization proof and separately preserved spectral alternative |
| Same result: closed systems, exact SDP tests, Shor characterization | Section 4; improved 2n+1 exact objectives, unconditional Shor closure/whole-space proofs, explicit nonclosed projection examples including a compact original system |
| Same result and corrective reviews: stable convexity, HHC distinctions, closed feasibility failure, strip counterexample | Section 5; classical inputs credited and all examples exact; no floating-point zero decision or full-hull exactness claim |
| `notes/research-20260922-gram-hyperplane.md` and review | Section 6, sharp r≥k theorem, exact hyperplane images, singular cases, classical fidelity/rotation context |
| `results/infinite-quadratic-aggregation-hhc.md`, earlier frontier note and review | Section 7, actual r≥2 HHC, exact good cone, indispensable rays, arbitrary-quadratic obstructions, full strict/closed hulls and finite lifts |
| Later direct two-point development in formal topic 30 | Section 7 proof of the strict hull in every r≥2, without an external hull-theorem premise; replaces the earlier r≥3 midpoint-only supplement |
| `notes/research-20260922-aggregation-accuracy.md` and review | Section 8, dimension-independent inverse-square rate, finite-grid improved lower bound, rational meshes, objective-specific exactness, scientific figure and precise scope |
| `results/four-aggregation-strict-pdlc.md` and priority review | Section 9, all n≥1 compact inward transfer, strictification, negative-component limit, credited n≥3 sharpness, oriented SOC closure and failure of naive weak replacement |
| `notes/research-20260922-span-three-many.md` and review | Appendix B: known 2k bound, directional refinement, indispensable ellipsoid family and completed counterexample to the proposed general-cone two-bound |
| `notes/research-20260912-algorithm-opportunities.md` candidate 1 and corrected conflict example | Appendix A: proved diagonal-dominance repair LP, exact rational example, conditional-row/equality caveats; no unimplemented solver or performance claim |
| Formal topics 27–31 | Main Section 10 scope table; detailed and individual formal supplements; 64 modules/909 declarations plus 5 local dependencies in standalone pinned source project |
| Historical numerical scripts and experiment logs | Replaced where relevant by exact standalone checks; exploratory numerical trials are not proof or new empirical evidence |
| Bibliographic comparisons | Introduction plus detailed relevant sections; all source locators/version qualifications retained, including dissertation priority and Shor closure issue |

Earlier r≥3k Gram sufficiency and r≥6 infinite examples are superseded by
the sharp theorem and r≥2 construction. Earlier logarithmic lower constants
are superseded mathematically by the stronger finite-grid bound; the exact
formal constant remains distinguished. The unsupported arbitrary-cone
two-bound is disproved, not carried as an unresolved premise. An optimal
general many-ray count and efficient HHC/four-multiplier selection algorithms
are outside the proved scope, not requirements of the included theorems.

Unrelated quadratic precision, DAG, clustering, bilevel, treewidth, and
OA/Benders topics are excluded. Five local Lean modules from other namespaces
are copied solely as transitive proof dependencies, not as paper contributions.
