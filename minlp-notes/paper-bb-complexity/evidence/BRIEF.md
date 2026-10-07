# Manuscript brief

The user requests a complete, self-contained paper on what determines the complexity of branch-and-bound, suitable in our judgment for submission to a reputable journal. Authors should remain blank. Cover the repository developments coherently, even if the manuscript is large. Write plain, precise prose for optimization experts, explain assumptions and mechanisms, and identify original contributions relative to inspected primary literature. Existing computational experiments may be trusted and must not be rerun. Mathematical results must be critically examined; repair errors and develop incomplete arguments needed for complete claims. Do not manufacture claims of solved open questions, novelty, or practical speedup. Open questions beyond the proved scope may remain explicitly open; core statements must have complete proofs.

Use Claude Opus for main writing, and independent Opus and GPT Sol reviewers. Sol may do supporting mathematical development. If Claude usage limits intervene, use Sol. All literature research must use GPT Luna at maximum reasoning. One reusable Luna agent owns the supplied $lit workflow and serialized literature additions. Writers and mathematical reviewers should use the evidence and citations supplied by that agent, and request further literature work through root rather than conduct their own literature searches.

Primary source families:
- /workspace/minlp-notes/research-20260928b/bb-complexity/ (SYNTHESIS.md, PROGRAM.md and topic notes, reviews, computations)
- /workspace/minlp-notes/research-20260929/rlct/rlct-node-complexity.md and reviews
- /workspace/minlp-notes/research-20260929/theory-single-tree/
- /workspace/minlp-notes/research-20260929/theory-decomposition/
- /workspace/minlp-notes/research-20260929/theory-consistency/
- /workspace/minlp-notes/research-20260929/computation/
- /workspace/minlp-notes/research-20260928b/closing-research-results.md
- /workspace/minlp-notes/research-20260929/closing-research-results.md

Relevant current papers for overlap: paper-relaxation-limits, paper-decomposition-aware, paper-open-minlplib, paper-adaptive-obbt, paper-sparse-indicator-quadratics. This manuscript should stand alone but attribute related results and avoid presenting overlap as a separate new discovery.

Only the new /workspace/minlp-notes/paper-bb-complexity/ directory is writable for manuscript work. The root README may receive a narrow link only after final integration if warranted. Preserve existing notes, experiments, manuscript folders, user work, and git state. Do not commit, run project-wide checks, inspect CI, or rerun experiments. Read AGENTS.md. Each agent owns disjoint assigned files; report cross-file requests to root. Keep internal process and review evidence out of submission sources.

Verification means proof review, source/evidence accounting, targeted mathematical identity checks when useful, and clean standalone LaTeX builds. Build and package the final paper and archival computational references. Maintain a claim coverage map that records hypotheses, proof location, literature comparison, experimental provenance, and review resolution.
