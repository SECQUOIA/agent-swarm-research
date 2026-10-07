# Manuscript brief

Write a complete, self-contained journal paper on quantitative sparse SOS hierarchies and large convex recourse blocks. Authors remain blank. The user permits a large paper and necessary mathematical development, requires critical proof verification, clear plain prose for optimization experts, precise prior-work comparisons and qualified novelty. Trust existing computational records; do not rerun experiments. If a fatal unrepairable error defeats a reasonable paper, document it and stop.

## Scope

Primary sources: /workspace/minlp-notes/research-20260928/closing-research-results.md and /workspace/minlp-notes/research-20260928/solver/. Central chain: sparse full-preordering kernels; ordinary-module O(log^3 R/R^2) exact-consistency transfer with coefficient normalization and no extra bag-count factor; fixed-domain private convex quadratic recourse; affine recourse O(1/r) and sharpness; regular projected multipliers restoring O(1/r^2); polynomial constraints with global error bounds; finite-state variables; rational certificates with slack; exact finite-order examples. Include supporting findings only if coherent. Curvature-based convex covers and unrelated algebra/control topics are outside scope.

The inverse-square sparse preordering rate was asserted in Magron July 2025 and February 2026 slides. Do not claim that rate as new. Dense ordinary-module kernels are prior. Distinguish private-degree-two and total-degree hierarchies, primal rounding and dual certificate attainment, ordinary quadratic modules and preorderings, exact moment consistency and measures, fixed-width constants and coefficient normalization. No general MINLP runtime or practical speedup is established.

## Team and workflow

Use Claude Opus for main writing. Use GPT Sol and Opus independent reviewers, with Sol supporting mathematical development. All literature research is assigned to one GPT Luna agent at max reasoning. Luna alone owns the supplied $lit skill /workspace/local-home/repo/skills/literature/SKILL.md and serial KB maintenance. Writers/reviewers use supplied research notes and Luna evidence rather than conduct literature searches; requests for sources go to root. Reviewers must repair or propose rigorous repairs for gaps and clearly separate established results from open extensions.

## Files and verification

Project: /workspace/minlp-notes. Manuscript: /workspace/minlp-notes/paper-sparse-sos. Only that new manuscript directory is writable for paper work; Luna may maintain /workspace/minlp-notes/literature under $lit. Preserve all existing source notes, other papers, user edits, and git state. Do not commit, run project-wide verification, inspect CI, or rerun computational experiments. Follow AGENTS.md. Use disjoint file ownership. Keep internal process and review evidence out of submission sources. Provide complete mathematical proofs, literature bibliography, clear examples and appropriate interpretation. Submission archive must build independently. Record actual targeted checks and their outcomes. No journal submission is authorized.
