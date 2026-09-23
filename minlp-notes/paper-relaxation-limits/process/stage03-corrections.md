# Stage 3 corrections after round 1

The separate correction agent implemented exactly the four accepted groups in
[the adjudication](stage03-round01-adjudication.md). The relevant findings in
reviews 03, 05, 06, 10, 11 and 12 were checked before editing. No new theorem,
constant, algorithm or proof mechanism was introduced.

| Group | Manuscript change | Validation |
| --- | --- | --- |
| A1 | In `sections/appendix-positive-box-predecessors.tex`, the asymmetric proof now explicitly resets `L(s)` to the low-success count and `H(s)` to the high-failure count. It defines `Q_L`, `Q_H`, integrates `C_L` over `[0,1-delta]` and `C_H` over `[0,delta]`, gives the corresponding independent products `P_L`, `P_H`, and restates `A`, `B`. | Checked the common-threshold decomposition and the unchanged dispersion, endpoint cross-term and two mass-regime arguments with the reset definitions. Exact rational checks described below passed. |
| A2 | In `sections/06-treewidth-two.tex`, Proposition 9.4 explicitly retains all constructed factor scopes, including zero-weight factors, for the exact incidence-treewidth claim. The following complete-graph example now specifies unit vertex weights. | For `K_2` with weights `(1,0)`, retaining both factor vertices gives the intended four-cycle and width two. The existing bag and minor proof applies unchanged. Unit weights give separate maximum `k+1` and global maximum one on `K_(k+1)`. |
| A3 | In `sections/appendix-structural-auxiliary.tex`, the exact-width `K_(2,m)` forest-coloring obstruction now assumes `m >= 2`. | A four-cycle gives the lower bound two; bags containing the two variable vertices and one factor give the upper bound. Private variables attach as leaves. The excluded `m=1` case is a tree. |
| A4 | In `sections/06-treewidth-two.tex`, the limits discussion retains the open question of partitioning width-two factors into two chordal-bipartite incidence classes, defined by excluding induced cycles of length at least six. It distinguishes that target from the proved all-cycle parity property, which permits induced eight-cycles, and marks the recorded 5,000-support experiment as finite evidence. | Read the closing discussion of the source investigation and its linked experiment record. The record ends with `{"total_checked": 5000, "counterexamples": 0}`. No search was replayed and no universal conclusion was inferred. |

The A4 source is
[`notes/multilinear-treewidth-two-investigation.md`](../../notes/multilinear-treewidth-two-investigation.md),
under “A possible balanced-matrix route.” Its linked
[`multilinear-chordal-bipartite-partition-search.jsonl`](../../notes/multilinear-chordal-bipartite-partition-search.jsonl)
has SHA-256
`fab016f391fcf3ef549fdbec3e307c4287f3353a244e95b401fb1fde4f0c879d`.
This is verification of the historical record and its stated scope, not a
fresh computational certification of its generated supports.

For A1, an ad hoc Python `Fraction` calculation at `rho=64`, `delta=1/8`
checked the empty vector and mean vectors `(3/4)`, `(3/4,3/4)`, `(15/16)`,
`(7/8,15/16)` and `(3/4,3/4,15/16,31/32)`. It directly integrated the full
normalized common-threshold product and both separate groups. Each case
satisfied `C=C_L+C_H-1`, the independent-deficiency decomposition,
`D_IL >= delta A`, and both dispersion inequalities. In the reported
singleton regression, `C_L=P_L=193/4`. In the two-coordinate regression,
`C_L=12289/4` and `P_L=37249/16`. These finite checks corroborate the local
definition repair; the existing written proof supplies the universal bound.

`python verification/build_and_check.py` completed with exit zero. Its
report records no warnings, no duplicate labels, and an exact match between
the printed Stage 2 checker and its source file. The PDF has 62 pages and
SHA-256 `78635ac0582055ae148862ba48123d264dacdc8079d935740188b484beddbd25`.

Rendered PDF pages 38, 39, 57, 59, 60 and 61 were inspected at a 1,500-pixel
maximum dimension. The retained-scope clause and unit-weight example on
page 38, open target on page 39, restricted forest example on page 57, and
reset asymmetric display on page 59 are readable and unclipped. Pages
60–61 confirm the continuation of the asymmetric proof and the following
fixed-mixture proof and reference transition. No layout repair was needed.
This inspection covers the affected passages and their continuations, not
every page of the cumulative manuscript.

Before editing, a SHA-256 baseline was captured outside the paper. All 198
baseline snapshot files and all 706 baseline files under the repository's
`notes/` directory remain identical. The six earlier accepted section files
(`01-foundations`, `02-universal-positive`, `03-cubic-equal-means`,
`appendix-finite-signings`, `appendix-positive-couplings`, and
`appendix-cubic-certificates`) and `macros.tex` also match
`process/snapshots/stage02-accepted/` byte for byte. All other live manuscript
sources, the bibliography and the verification scripts remain unchanged.
No literature files or other paper folders were edited.

Authored changes are limited to the three manuscript files named above and
this corrections record. The build regenerated `main.pdf`, `main.aux`,
`main.log`, `main.fdb_latexmk`, `verification/build-output.txt`,
`verification/build-report.json`, and `verification/manuscript.txt`.
The coordinator independently changed `verification/primary-source-checks.md`
and added `verification/potechin-source.json` during this pass; the coordinator
confirmed their ownership, and those files were left intact. Stage 3
acceptance remains the coordinator's next independent check. No later-stage
work was undertaken by this correction agent.
