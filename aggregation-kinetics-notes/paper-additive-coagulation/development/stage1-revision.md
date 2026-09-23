# Stage 1 revision record

Date: 2026-09-07. Revision agent: `paper_revision_agent`, separate from the stage author and the five independent reviewers.

All corrections and reader aids accepted in `reviews/stage1-round1/assessment.md` are implemented. No accepted issue remains unresolved. At this revision handoff, coordinator verification and final stage acceptance were pending. The coordinator subsequently accepted stage 1; see `WORKFLOW.md` and `stage1-accepted-snapshot.json`.

## Accepted corrections

| ID | File and location | Exact change |
|---|---|---|
| S1-A1 | `appendices/wellposedness.tex`, setup preceding Lemma A.1 and stability application | Require joint measurability of the nonnegative loss and, for each finite positive `R,T`, an `L^1(0,T)` bound on `sup_{0<x<=R} a_s(x)` for almost every time. This replaces the weaker pointwise time-integrability assumption and the application-only qualification. The stability application now displays the admissible bound `lambda(t)(mbar(t)+R Nbar(t))+sigma(t)`. The existing localization proof applies directly. |
| S1-A2 | `sections/fractional-moments.tex`, Proposition 2.7 | Require joint measurability of the perturbed kernel and selection rate. Specify both substitutions in the bounded-Borel-test population balance, retain Definition 1.2's locally bounded count and conserved mass, and refer to the measurable daughter assumptions. Quantify the moment estimate by every `0<p<1`. |
| S1-A3 | `sections/model.tex`, count balance | State local absolute continuity of count, qualify its differential equation by almost every time, and state the explicit formula for every `t>=0`. |
| S1-A4 | `sections/model.tex`, Theorem 1.3 | Identify continuity in the weighted-variation norm `||.||_w` explicitly. |

## Accepted reader aids

- Define the integral pairing before its first use.
- Give setwise measurability explicitly in the solution definition.
- Explain that the factor one half counts unordered coagulation pairs once.
- In the monodisperse equal-split sharpness proof, justify continuity at zero of the moment-balance integrand using weighted-variation continuity, the product-weight bound on the coagulation integrand, and the equal-split fragmentation identity. This proves the asserted right derivative.
- Qualify the Cepeda comparison by fixed relative-fragment laws satisfying that work's dislocation hypotheses. Apply the same qualification in the author source record.

The author status and coverage record now report completed independent reviews and implemented minor corrections, while leaving coordinator verification pending. The revision changes no main claim and adds no later-stage material or priority claim. The original reviewer reports, assessment, and review snapshot remain unchanged.

## Verification

- `make` completed successfully with PDFLaTeX, BibTeX, and the prescribed subsequent PDFLaTeX passes. The final `main.pdf` has 10 pages (317,692 bytes).
- The final `main.log` and `main.blg` contain no unresolved references or citations, LaTeX errors, or overfull or underfull box warnings.
- `pdftotext -layout` and `pdfinfo` confirmed the generated artifact and readable count qualifications, perturbed-rate assumptions, and corrected comparison setup. The new passages were also checked against the accepted correction list.
- The first log-check pattern matched the ordinary `infwarerr` package description rather than a diagnostic. A corrected check excluded package metadata and passed. This was a check-pattern false positive; the build itself succeeded.

No second review round was run: the coordinator assessment requires verification of these minor corrections before the next stage.
