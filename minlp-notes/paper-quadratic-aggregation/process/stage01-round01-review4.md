# Stage 1, round 1: independent review 4

Date: 2026-09-22. Scope: foundations, literature, inventory, and LaTeX
scaffold. I did not read another review or alter manuscript sources. Missing
later sections, abstract, and final packaging are intentional at this stage.

## Verdict

The present manuscript foundations have two minor issues and no major
mathematical, citation, novelty, or build issue. An end-of-review inventory
update reveals a major coverage issue described below; accept the stage only
after that inventory and scope correction.

The original conjecture is represented correctly, including nonemptiness,
ordinary rather than closed convex hull, and the equivalence between a
nonconstant aggregation and the displayed `(A_lambda,b_lambda)` condition.
The exclusion of the zero multiplier is adequately carried by that condition.
The HHC definition agrees with the cited version. The elementary implication
from HHC to ordinary hidden convexity has the correct dimension restriction.
The definition of good aggregation and the assumptions attached to the cited
hull theorem agree with BDS arXiv v2. The distinction between globally convex
aggregations and good aggregations is particularly useful for the later work.

The coverage map accounts for the canonical note and the corrective audit.
Candidate new investigations and the Kojima--Tuncel issue are explicitly
unaccepted later-stage work, so I have not treated them as established results
or as present-stage proof gaps. The literature record appropriately distinguishes
inspected versions, abstracts, access limitations, and bounded novelty searches.

## Major inventory issue discovered at review completion

The coordinator alerted me to concurrently appearing topic sources:
`notes/research-20260922-aggregation-frontier.md` and
`formal/topics/27-quadratic-aggregation/`. I independently listed the latter
and read the opening 100 lines of the former. The note claims a new HHC
construction and an affirmative resolution of BDS Conjecture 3.1; it explicitly
requires further independent mathematical and novelty review. Therefore the
coverage map's present blanket exclusion of finite-aggregation questions is
no longer adequate for the user's all-relevant-developments scope.

Fix: add both sources to the inventory, distinguish the candidate results from
verified ones, and add their separate author/reviewer development stage to
`PROCESS.md`. Revise the blanket Conjecture 3.1 exclusion pending that stage.
No main-proof writing or validation of the frontier conjecture is required
inside the present foundations stage. I have not certified the candidate proof.

## Minor issues and precise fixes

1. `sections/01-setting.tex:105-106`: the diagonal-case attribution does not
   retain the `n >= 2` restriction in BDS v2 Theorem 2.12, while the current
   paper begins with `n,m >= 1`. This does not make the elementary diagonal
   characterization false for `n=1`, but the source locator should accurately
   describe the theorem it cites. Insert “for $n\geq2$” into the sentence, or
   explicitly label the `n=1` extension as elementary if it is needed later.

2. `sections/01-setting.tex:126-129`: identify the matrices subject to DMS's
   positive definite linear combination assumption. Both `A_i` and `Q_i`
   are already defined and their distinction matters to the planned results.
   Replace the loose phrase by “under a positive definite linear combination
   assumption on the homogenized matrices $Q_1,Q_2,Q_3$, together with
   the dimension and hull assumptions in their theorem,” or state those
   assumptions explicitly. The current narrative is a summary rather than
   an imported theorem, so I classify this as clarity/precision, not a major
   unsupported theorem claim.

## Independent source checks

- Compared the manuscript against `/tmp/quadratic-paper-literature/bdsv2.txt`
  at Definition 2.1, good-aggregation notation, Theorems 2.9 and 2.12,
  Proposition 2.14, and Conjecture 3.3.
- Inspected the repository's DMS journal extraction, particularly its
  introduction, PDLC discussion, and Theorem 2.4 context. This supports the
  manuscript's distinction between real linear combinations and nonnegative
  aggregations and its modest historical account of Yildiran.
- Independently searched the web for `"Yildiran" "Convex hull of two quadratic
  constraints" "nonempty"` and `"Conjecture 3.3" "hidden hyperplane convexity"`.
  The primary author-hosted BDS and DMS PDFs appeared. The author-uploaded
  Yildiran preprint text also corroborated the strict-inequality convention
  and at-most-two-aggregations summary. No later resolution was identified
  by these searches; this is not evidence of exhaustive publication priority.
  Sources: https://www2.isye.gatech.edu/~sdey30/HHC.pdf and
  https://www2.isye.gatech.edu/~sdey30/AggQuadratics.pdf.

## Targeted commands actually run

Repository reads used `rg --files`, `cat`, `nl -ba`, and targeted `rg -n` and
`sed -n` on the files named above and the stage records. Build, from
`paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage01-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage01-review4/main.log
```

The independent temporary-directory build passed and produced three pages.
The final log search returned no matches (normal `rg` exit status 1 for no
matches). The generated bibliography prints the supplied DOIs and version
locators. No project-wide check, CI inspection, numerical experiment, or
subagent was used.
