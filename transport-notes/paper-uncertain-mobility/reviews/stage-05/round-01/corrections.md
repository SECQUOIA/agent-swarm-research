# Corrections: Stage 05, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the Stage 05 author. Date: 2026-09-07.

Input reviewed snapshot: `b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c`, preserved in [snapshot.json](snapshot.json). I read the [coordinator adjudication](adjudication.md) and [reviewer 1's report](reviewer-1.md). The adjudication accepts two overlapping groups of minor findings and identifies no major issue.

| Accepted findings | Corrected source locations | Correction and reasoning |
|---|---|---|
| R1-01, R4-01 | `sections/05-exact-observation.tex`, lines 252–262 | Replaced the claim of independent endpoint traces with independent component restrictions and no endpoint matching condition; explicitly noted that finite traces need not exist. Explained localization of bounded form functions by the vanishing-energy transitions, followed by form-norm truncation to obtain the result for arbitrary domain elements. |
| R1-02, R3-01, R4-02, R5-01, coordinator C-01 | Same section, lines 418–426 and 434 | Stated that the diffusion operator scales as r⁴. For an unamplified rescaled test, displayed the full integrated form with factor r⁵ and source with factor r. Changed the response-scale expression to r²/r⁵=r⁻³. The resulting estimate, theorem, policy, and constants are unchanged. |

Domain check: for a bounded function, the added derivative cost from a cutoff is bounded by its squared supremum times the transition energy; the original energy on shrinking transition intervals tends to zero by integrability. The L² and bounded-reaction errors also tend to zero. For the explicit piecewise positive weights, truncation errors have derivative energy on the sets where |v|>N and converge to zero by dominated convergence, as do their L² and reaction errors. Thus the argument uses component restrictions without presuming endpoint traces.

Scaling check: with ds=r dx, D=r⁶/(2B), and ∂s=r⁻¹∂x, the derivative integral has coefficient r⁵/(2B), while k=r⁴V gives reaction factor r⁵. The source has factor r, so its optimized quadratic quotient has factor r²/r⁵=r⁻³. SymPy independently checked these factor identities.

Verification:

- Forced the full LaTeX/BibTeX build with `latexmk -pdf -g -interaction=nonstopmode -halt-on-error -file-line-error main.tex` in the manuscript folder. It exited with status 0 and produced the 37-page PDF.
- Scanned the final `main.log`; no warnings, undefined-reference notices, or overfull/underfull boxes were present.
- Explicitly scanned the entire changed source for trailing whitespace and control bytes other than newlines, and checked its final newline. All checks passed, including for this untracked manuscript file.
- Compared all fifteen manifest-listed source hashes. Only the intended section differs. The reviewed manifest, all reports, and the author handoff remain unchanged; no later-stage file or historical source note was edited.

Corrected section SHA-256: `c8dc11388cc9be24070eed23dd970438abd43d74bc5956fff00f454bed1a5310`.

Editing is complete. Neither correction changed a substantive claim or exposed a major issue. Coordinator verification and a separate acceptance record remain required; this record does not accept Stage 05 or begin Stage 06.
