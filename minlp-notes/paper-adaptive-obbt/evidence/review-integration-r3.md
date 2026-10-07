# Final source-integration review, round 3

Accepted for this focused integration scope. At the reviewed snapshot, the new prior-work paragraphs, contribution statements, and bibliography agree with the final bounded literature audit. No remaining material front-to-body or source-attribution mismatch was found. This closes the source-integration question left open in round 2; it does not replace the independent mathematical reviews or establish publication priority.

The snapshot was recorded at **2026-10-06 02:54:30 UTC**. I reviewed the final `evidence/literature-audit.md`, including all 37 reference dispositions and all 13 access or identity gaps, against the approved supplement, the paper bibliography, the introduction and related-work paragraphs, and the relevant discussion and body attribution passages. I also used the previous integration reports and revision responses. I did not repeat accepted proofs, perform independent literature searches, run experiments, build the manuscript, or inspect CI.

## Findings

The revised text credits repeated OBBT, incumbent cutoffs, generic McCormick convergence orders, recursive arithmetic and composition, and classical fixed-point, duality, and sensitivity arguments as established ingredients. Its stated contributions concern the specified OBBT maps, explicit shape-and-position-dependent second-order coefficients, finite certificates checked on their own rebuilt hulls, and sufficient contraction and stall conditions. These are appropriately qualified constructions and results, without a general priority or prior-absence claim.

The added predecessor paragraphs preserve the distinctions required by the audit:

- Puranik and Sahinidis provide the broader domain-reduction survey context. Coffrin and coauthors supply repeated FBBT context, explicitly distinguished from OBBT.
- Nagarajan and coauthors are credited with sequential OBBT/PBT repeated to a bound-change tolerance. The manuscript does not suggest that repeated OBBT or tolerance stopping was previously absent.
- The Belotti pair consists of the published 2010 chapter and the 2012 Optimization Online manuscript. The bibliography keeps the latter as a manuscript, and the prose does not describe it as a published 2012 article. Joint citation follows the audit's guidance because the 2010 chapter text was unavailable whereas the 2012 manuscript was read.
- The Sundar paragraph explicitly attributes rebuilding the quadratic-convex relaxation and the incumbent-cutoff variant to the consulted preprint. The proceedings entry retains its published metadata and identifies the consulted arXiv version 3, updated January 29, 2019. It does not imply that the unavailable proceedings text was inspected.
- The Taylor/McCormick–Taylor paragraph credits arithmetic, composition, and convergence-order analysis to the earlier work. Its distinction is the ordinary clipped McCormick coefficient and its use in the OBBT tangent map. The initial relative-clause ambiguity was corrected: only the latter models are described as combining a Taylor polynomial with a McCormick relaxation of its remainder. No material issue remains in that passage.

The generic citations to Bompadre–Mitsos 2012, Najman–Mitsos 2016, Robinson 1973, and Bompadre–Mitsos–Chachuat 2013 stay within the final audit's abstract or metadata support. They do not attribute unread detailed theorems, source constants, or negative content claims. The audit's remaining gaps, including unavailable or unidentified uncited predecessors, therefore remain disclosed limits on literature coverage rather than hidden support for a manuscript result. In particular, this acceptance does not clear an absolute novelty claim or certify the full contents of those sources.

The current summary of the face construction says **at most \(2n\) face optimizations**, consistent with the body theorem. This counts optimization problems and makes no wall-clock claim. The discussion also now conditions use of a completed round's face optima as a finite certificate on the rebuilt-row check. These statements retain the distinction between a current-round result and protection against future rebuilding.

## Bibliography and scope checks

The paper and approved supplement each contain 37 unique keys, with identical key sets. All citation keys in the reviewed introduction and related-work section resolve in the paper bibliography. The only entry-text differences from the supplement are protective title braces around `McCormick` and replacement of the Borrelli and Walker direct-PDF URLs by DOI URLs; they do not change the approved bibliographic identities. The added records and Sundar source-version note agree with the approved supplement.

An uncited Ryoo–Sahinidis 1996 title in the audit's gap list initially differed from the literature lead's final handoff. The root corrected it to the supplied verified title before the final hash pin. This bookkeeping correction did not change any manuscript claim or reference.

Checks actually performed were targeted file reads with `cat`, `nl`/`sed`, and `rg`, and Python reads for the key/entry comparison and SHA-256 identities. No source retrieval, computational campaign, build, project-wide verification, or CI check was performed for this review. The audit supplies the literature evidence; the accepted body reviews supply the proof assessment.

## Reviewed identities

Paths below are relative to `paper-adaptive-obbt`.

```text
cc6c2691c7eaf877c0e2e8b4ed945d10f29cd070008cd3828a8e53a06e15dbaa  references.bib
5ffcc29f326ad1b5a5d724b32acd7dbd276449accc4b2e77a541115ef51a0ac9  evidence/literature-references.bib
3a109aebf9c7c03959083abd6da9b0ba2438c283cbe8f213b0c24502807a9aa8  evidence/literature-audit.md
2b07d38eb0bbd5b50cada072ca29cbc6f58708a8385be1d07e5c17eb4379a666  sections/related.tex
564a50f6f73c647af6f568bd9912d6337993b71b31cce4acf3643fff9bd0d00b  sections/introduction.tex
57672aa74ee14a0533df7d75dfe80cc2079bc82b083c3330081f5e11aaefa5c3  sections/discussion.tex
ca8717986aad87156b02328832adbe13765b973ac98b9acfb3f779a26318e318  sections/cutoff.tex
f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d  sections/foundations.tex
de079f21574486bd3e0fa5f914d857279dc1a328b2c5bfda8f088a1337bfbd75  sections/local-rates.tex
dfbf09c38202404ea77a30b3d8cd5068e842758bf3cf7aa9b02dc20924c4d327  sections/algorithms.tex
dc58fdd51989e1b9b61010890d56c7ef52c606d1caaa4435ee4d24e3afd9bc85  appendices/numerical-validation.tex
```
