# Encoding upper-bound review

The frozen target was the cumulative thirteen-page manuscript and its
supporting files. The increment was measured from `fd646f01`; the cumulative
baseline was `fe439d5c885e3efd7f9fc4b1392eaffca7cfcf6f`. Reviewers also inspected
the new untracked files. The raw external report is retained in
`evidence/reviews/stage2-claude.txt` relative to this paper folder.

| Independent review | Scope and outcome |
| --- | --- |
| Codex `s2_review_whole` | Complete manuscript, source comparisons, PDF and both checkers. No findings. |
| Codex `s2_review_general` | General upper bound, sparse certificates, reciprocal graph and primary Basu–Roy bounds. No findings. |
| Codex `s2_review_fixedcount` | Affine-face reduction, singular regularization, quantified limit, coefficient heights and multiplier recovery. No findings. |
| Codex `s2_review_algorithm_sources` | Conservative-output corollary and the precise scope of cited algebraic results. No findings. |
| Codex `s2_review_clarity_checks` | Cumulative clarity, PDF, references and symbolic checker. No findings. |
| Fresh Claude session | One Fable whole-target reviewer and three Opus reviewers for Section 4, Section 5 and cross-cutting consistency, followed by parent adjudication. No confirmed mathematical error; seven localized presentation or check-quality findings. |

The task lead checked and accepted the external findings: describe the two
parameter bounds as complementary; distinguish the objective bound from the
feasible-set symbol and the quantified free scalar from the primal optimum;
make polynomial counts and radius substitutions literal; describe the cited
Grigoriev–Pasechnik result as a few-quadratic result; retain the bounded-solution
qualification in the Kamminga–Rudolph comparison; compute the test objective
from its primal point and check its signed value and constraint expressions;
and clarify global slice convexity, residual notation and script names.
The separate local uses of other standard symbols do not require wholesale
renaming. These fixes do not change a theorem or its proof strategy.

The five Codex reviews and the external session were read-only. The external
session verified retained source statements and artifact hashes without
network access. The lead and author had separately checked the primary-source
records documented in `stage2-sources.md`. No review independently reproved
the internals of the cited general algebraic theorems. Finite symbolic checks
are not evidence for their universal bounds.

Because every accepted change is localized and directly verifiable, a full
repeat review is unnecessary under the build skill. The updated source and
checks are inspected directly, and the author records the targeted checker
and manuscript build in `stage2-validation.md`. No project-wide checks or CI
inspection are included.
