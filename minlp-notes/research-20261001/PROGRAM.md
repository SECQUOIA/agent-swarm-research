# October 1 continuation: cutting planes for nonconvex quadratic programs

Date: 2026-10-01; closed 2026-10-04. All eleven streams are finished.
The final results, review states, errata and publication recommendations are
in the [closing record](CLOSEOUT.md). The user asked to finish the recommended work and its
extensions for one topic: cutting planes for nonconvex quadratic programs,
covering separation limits and the best choice of cut. Other topics are out of
scope.

## Starting results

1. Optimal intersection cuts from maximal quadratic-free sets:
   [note](../research-20260928b/sfree/optimal-intersection-cuts.md),
   [code](../research-20260928b/sfree/code), and
   [review](../research-20260928b/reviews/sfree-review.md).
2. Exact separation of split inequalities for integer QP is strongly
   NP-complete: [note](../research-20260928b/side-results/split-separation-np-complete.md).
3. A three-variable family of cube quadratic cuts, with a compact SDP that
   enforces it: [counterexample](../research-20260925/three-positive-disjoint-counterexample.md),
   [family](../research-20260925/three-positive-family-sdp.md), and
   [assessment](../research-20260925/publication-quadratic-assessment.md).

In SCIP 10.0, quadratic intersection cuts are off by default
(`nlhdlr/quadratic/useintersectioncuts = FALSE`;
`nlhdlr/quadratic/usestrengthening = FALSE`, checked through PySCIPOpt 6.2.1).
Results about choosing these cuts matter to solvers only if a better choice
makes them worth enabling, or clearly better when they are enabled.

## Work streams

| Directory | Question |
| --- | --- |
| `scip-rule-fidelity/` | Does the Python model of SCIP's set choice match the cuts SCIP generates? How far are SCIP's actual cuts below the corner bound on real instances? |
| `scip-set-selection/` | Inside SCIP: does a better choice of set make intersection cuts pay off? |
| `multiround/` | Why does the best-orbit rule fall behind over several rounds? Which multi-round rule works? Does the cutting loop converge? |
| `minor-sets/` | Does the tangent-edge obstruction also occur for the sets SCIP uses for implied minors (signature (2,2))? |
| `ratio-bound/` | Is the worst-case ratio of the orbit family to the corner bound bounded below under a nondegeneracy condition? |
| `orbit-closure/` | Is the closure of the orbit family's cuts exact for bilinear constraints? The [original BP experiment was stopped incomplete](orbit-closure/CLOSEOUT.md) on October 2; the finished [note](orbit-closure/note.md) proves its claim analytically and gives closure counterexamples. A separate Proposition 16 (B) certificate remains optional and incomplete. |
| `intersection-literature/` | A web-based priority and context audit for the intersection-cut results. |
| `split-practice/` | Ranks of SDP optima on benchmarks, practicality of exact separation at fixed rank, and newer literature. |
| `binary-separation/` | Status of separation for the binary analogue (rounded psd, hypermetric, gap-1); attempt it if it is open. |
| `three-var-computation/` | Does the selective family help beyond existing relaxations, at lower cost than the exact lift for each triple? |
| `three-var-completeness/` | Do the symmetry copies complete the description? What happens with four positive variables? |

Each stream has an author, an independent reviewer, and, when fixes are
needed, revisions and confirmation checks, for up to four rounds. The
[closing record](CLOSEOUT.md) distinguishes independent reviews from final
fixes checked by the coordinating agent. For `scip-set-selection`, independent
[review round 3](scip-set-selection/reviews/review-r3.md) verified the r2
revision; its optional O1–O3 wording fixes are now applied and not re-reviewed.
"Reviewed" means checked by a research agent that did not write the
material. It is not journal peer review. An unsuccessful literature search
does not establish novelty. Only targeted checks are run; CI handles
project-wide verification. Program files were included in repository commits made outside this program
(e.g. `d91d8d98b`, `f785387a8`, `b59ed1b83`); the program itself makes no commits.
This history was checked with `git log --oneline -- research-20261001 | head`.
