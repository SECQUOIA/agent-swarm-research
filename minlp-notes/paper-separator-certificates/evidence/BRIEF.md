# Manuscript brief

The user requests a coherent, self-contained, submission-quality anonymous journal paper on constructive separator certificates. The central contribution is constructing affine separator certificates through regridding on arbitrary tree decompositions, together with the separator-consistency theory, certified inexact solves, stable nonlinear dynamics, and finite-precision output. Critically check all mathematics and develop necessary repairs; do not rerun computational experiments. Any evidence of a topic-wide fatal flaw must be documented and reported.

All literature research must use GPT Luna with max reasoning. A single reusable literature lead owns the knowledge base through the supplied lit skill at /workspace/local-home/repo/skills/literature/SKILL.md. Other authors/reviewers do no literature discovery or KB writes.

Canonical sources:
- research-20260929/theory-decomposition/decomposition-certificates.md
- research-20260929/theory-decomposition/extension-adaptive.md
- research-20260929/theory-decomposition/adaptive-matching.md
- research-20260929/theory-decomposition/covering-upper-half.md
- research-20260929/theory-consistency/consistency-relaxations.md
- research-20261002/regridded-certificates/note.md
- research-20261002/regridded-certificates/inexact-oracles.md
- research-20261002/tree-localization/counterexample.md
- research-20261002/new-direction/nonlinear-dynamics.md
- research-20261002/new-direction/nonlinear-dynamics-bit.md

Related existing manuscripts: paper-bb-complexity (certificate existence/size), paper-decomposition-aware (coordinate-grid algorithms/recourse), paper-sparse-sos (quantitative hierarchies), paper-certified-support-cuts (support and gluing), paper-open-minlplib (application-specific split certificates). Reuse foundational results with explicit provenance; do not duplicate entire independent manuscripts.

Write plain, precise mathematical prose with complete proofs, careful computational accounting and explicit structural assumptions. Prefer the simplest sound argument. No invented novelty or practical speedup claims. No author data, dates, internal research history, agent mentions, status labels, repo paths or review mechanics in the scientific manuscript. Preserve these only in evidence files. Use only targeted manuscript checks; do not inspect CI or run project-wide verification.

Root owns main.tex, macros.tex, introduction, conclusion, integration and packaging. Authors own assigned section/proof files. Reviewers write only their assigned evidence report; they may develop proof repairs there for author/root integration.
