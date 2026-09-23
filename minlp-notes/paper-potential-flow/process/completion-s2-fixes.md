# S2 accepted correction

Date: 2026-09-10. Applied by a correction agent distinct from the S2 author after reading the lead adjudication and reviewer R3's full report.

## S2-C1 (minor; R3-1)

Corrected `complexity/sections/04-laws.tex` to attribute the polynomial number of nonlinear worst-case problems to robust-feasibility checking for a fixed design. The sentence now separately identifies the iterative adversarial design algorithm and retains the distinction between the number of subproblems and the cost of solving each. Corrected the corresponding source summaries in `completion-s2-author.md` and `completion-literature-screen.md`.

Independently checked the published article's abstract and Section 1, particularly the paragraphs before its contribution list: [Thürauf, Grübel, and Schmidt, *Adjustable robust nonlinear network design without controllable elements under load scenario uncertainties*](https://link.springer.com/article/10.1007/s10107-025-02207-2). They explicitly separate fixed-design feasibility from iterative adversarial design optimization.

No theorem, proof, algorithm, or complexity conclusion changed. This is the only accepted S2 correction; no mathematical issue was discovered during this correction pass.

## Verification

Invoked the existing `verification/build_and_check.py` function `build('complexity')` only. It ran `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` and returned exit code 0. The PDF exists. The final log has no errors, undefined references, undefined citations, duplicate labels, or overfull boxes.

Refreshed `completion-s2-build.json` with the returned diagnostics and all 13 exact input SHA-256 hashes. The corrected Section 04 hash is `32f63642338cc12271c3aff35c73fe1fbf7c36da61dcb4e9f3468a5f90096249`; the other 12 input hashes are unchanged from the reviewed S2 build record. No numerical reruns were needed for this prose-only correction.

No later stage, Paper B, staging operation, or commit was changed. Existing uncommitted work was preserved.
