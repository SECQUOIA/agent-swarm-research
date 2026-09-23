# Whole-paper round 1: root adjudication

All fifteen reviewers completed independent reviews of every manuscript section and proof, the introduction, driver, bibliography and source index. Root read all fifteen reports in full. Fourteen report no findings; review13 reports one minor related-result coverage finding. Root accepts that finding after an independent proof check. Agreement counts do not establish mathematical truth.

| Reports | Reported outcome | Root disposition |
|---|---|---|
| 01–12 | No findings | No concrete correction to adjudicate; verification limits retained. |
| 13 | One minor finding | Accept M1 below. |
| 14–15 | No findings | No concrete correction to adjudicate; verification limits retained. |

## M1: zero-lower/unit-upper margin-block hardness

Accepted as minor. Section 6.7 gives general margin-block cost hardness and then discusses its unit-capacity hull, but omits the separate restriction proved in `results/rank-one-zero-lower-hardness.md`. Its scope is adjacent general matrix costs, so it does not invalidate a pooling theorem or require reproduction of an unrelated full proof. It is nevertheless a distinct developed restriction that belongs in the related-results account requested by the user.

Root checked the full saturated-margin repair and penalty proof and its use of the earlier biclique reduction. For total mass at least one, raising each distinguished margin at fixed total gives entrywise distance at most twice the sum of deficits. For smaller mass, the unit matrix at the distinguished entry satisfies the same bound. A cost penalty larger than twice the largest absolute entry therefore forces both margins to one, shifts the optimum by a known constant, and removes the positive lower bounds. Polynomially bounded integer costs and a negative threshold preserve strong hardness. The separate exact checker passed 2,000 rational examples; this supplements the proof only.

A separate repair agent must add a short statement that strong cost hardness persists with zero lower and unit upper margin bounds, using a negative threshold, cite the real note, and add its title/path/hash to the source index and coverage map. Preserve the existing distinction from standard additive physical economics. Use no invented author or public publication status. The current note hash is `26431afa15e32381c4aa342a0e8765ffaa5bb6cab1cb39ccbe6a2e013f7d70d0`.

No other finding is accepted. The source-only build, missing-section negative control, complete PDF layout inspection and source-integrity checks are recorded in `root-check.md` and `verification/whole-round01-root-validation.json`.

## Required next action

There are now 135 completed full reviews: 120 stage reviews and 15 whole-paper reviews. After separate repair and root verification, a fresh round of fifteen agents must review the complete revised paper. This repeat is required even though M1 is minor, under the agreed final whole-paper protocol. Completion remains pending a full round with no accepted findings and final artifact checks.

## Repair closure

Separate agent `/root/whole01_fixer` completed M1. Root read the repair record, validation and full exact diff, independently verified all four after-hashes and preservation of the other seven reviewed bundle files, and force-built the revised 91-page PDF without unresolved citations/references or overfull boxes. The corrected source is frozen under `snapshots/whole-round-02/`. M1 is resolved; the required fresh full-paper round may begin.
