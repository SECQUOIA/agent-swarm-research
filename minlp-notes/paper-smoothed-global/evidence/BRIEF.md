# Manuscript brief

The user requests one coherent, self-contained research paper on **Smoothed
exact global optimization beyond convexity**, suitable for submission to a
reputable journal. A long paper is acceptable. Authors remain unspecified.

The manuscript must cover the relevant developed results, explain their
importance and possible uses, state exact input and output contracts, and
compare precisely with prior work. All proofs must be examined critically.
Repair errors and complete necessary arguments within this topic. Do not
advertise conjectures or incomplete ideas as theorems. If a defect defeats
the entire subject and cannot be repaired, document it and stop authoring.

Use plain, precise language for optimization experts. Avoid promotional
phrases, inflated novelty, needless repetition, and development-history
narration. The paper must be readable without repository notes. Existing
computational evidence may be trusted; do not rerun experiments. Do not claim
new practical performance evidence for algorithms that remain theoretical.

Use Opus for principal writing, with Sol for mathematical development and
independent review in addition to Opus review. If Claude reaches a usage
limit, Sol may continue. All literature research must use GPT Luna at maximum
reasoning. One reusable Luna literature lead owns `$lit` ingestion and shared
KB updates; other agents request missing references through the root.

The source material is chiefly `research-20261002/new-direction/`, its
`prior-art/` and `reviews/`, and relevant antecedents in
`research-20260922/` and `research-20260927/`. Compare against the existing
exact-arithmetic, decomposition-aware, and sparse-indicator manuscripts to
identify overlap. Include overlap when needed for a complete proof chain,
and state clearly which contributions are original to this paper's topic.

Do not edit unrelated papers or their research notes. The root README and
adaptive-OBBT work were already modified when this task began. Avoid touching
them. Work inside `paper-smoothed-global/`, except serialized literature KB
maintenance by its owner. Do not commit or publish unless separately asked.

Only targeted manuscript checks and proof diagnostics are authorized locally.
Do not run project-wide verification or inspect CI. Preserve a coverage map,
author reports, independent reviews, adjudications, and a final verification
record outside the submission sources.
