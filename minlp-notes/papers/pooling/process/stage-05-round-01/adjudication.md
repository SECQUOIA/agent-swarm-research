# Stage 5, round 1: root adjudication

Root read all 15 reports in full, including the small truncated portion of review01 in a separate read. Fourteen reports have no findings; review07 identifies one minor issue. No reviewer identifies a major issue. Root independently read the full frozen draft and canonical arguments, inspected the physical and algebraic mappings, and checked source passages and finite experiments as recorded in `root-stage-05-check.md`. Votes and test counts are not substitutes for those checks.

| Review | Verdict | Root disposition |
|---|---|---|
| 01 | No findings | Accept the scoped checks; no revision requested. |
| 02 | No findings | No manuscript revision. Reviewer corrected a malformed source link in the report at root's request. |
| 03 | No findings | No revision requested. |
| 04 | No findings | No revision requested. |
| 05 | No findings | No revision requested. |
| 06 | No findings | No revision requested. |
| 07 | One minor finding | Accept m1 below. |
| 08 | No findings | No revision requested. |
| 09 | No findings | No revision requested. |
| 10 | No findings | No revision requested, including the new throughput optimization proof. |
| 11 | No findings | No revision requested. |
| 12 | No findings | No revision requested. |
| 13 | No findings | All 16 coverage entries independently checked. |
| 14 | No findings | No revision requested. |
| 15 | No findings | No revision requested. |

## Accepted correction m1: exceptional products without pool outlets

At frozen lines 776–802, the exceptional-only branch counts actual allowed exceptional outlets but later uses product constraints and fractions with an ambiguous index set. Introduce an explicit set `J_E` of exceptional products with allowed outlets. Fractions and their simplex are indexed by `J_E`; put `v_j=theta_j=0` by convention at every other exceptional product. Explicitly retain demand and homogeneous quality requirements at **all** products in `E_J`, including bypass-only ones.

Root accepts the finding as minor. The theorem's hypotheses do not change, every necessary bypass coordinate is already retained, the canonical construction explicitly preserves all exceptional requirements, and no new projection or complexity argument is required. The ambiguous pronoun and undefined absent fraction should nevertheless be corrected: omitting such a product's requirements would be false. Review07's example, a product demanding at least two units but supplied by only a unit-capacity bypass, demonstrates this clearly. The correction makes that infeasibility explicit in the existing core without adding variables or changing the dimension bound.

Assign m1 to a separate repair agent. Root will inspect the exact diff, preservation of accepted sections and bibliography, and clean build before closing the stage. No major issue has been accepted, so another full-stage round is not required by the staged protocol. Stage 6 remains pending these checks. The complete paper will receive its own independent 15-reviewer loop.

## Closure after checked repair

Separate agent `/root/s05_minor_fixer` implemented m1. Root inspected both exact diff hunks and the complete repair record, independently verified the bypass-only product's contradictory demand/capacity rows, confirmed unchanged sections 01–04 and bibliography hashes, and inspected the final clean 73-page build. The revised section SHA-256 is `ccb69faa00989209af3be2b152ca721e51deedf3c2139ea8c3ec0fe87ff02aa5`. No accepted issue remains unresolved. Stage 5 closes after 15 full reviews and one separate repair pass; stage 6 may begin. The earlier frozen draft and all review reports remain preserved.
