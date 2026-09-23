# Complete manuscript, round 1 — corrections

Date: 2026-09-17. Implemented all eight consolidated minor findings from `full-r1-adjudication.md`. Changes are limited to the authorized clarifications, the new sequence map, navigation, and corresponding evidence notes. Experimental designs, source-access qualifications, calculations, and scope are preserved. No source-library file or workbook was copied or edited.

| Finding | Correction |
| --- | --- |
| 1. Water overview scope | The overview separates protection by late hydrophobic-polymer addition at one state/challenge from conditional prediction during a nearby reversible humidity pulse. It explicitly avoids implying a damage law across histories. The polymer is named in plain language before the later PDVB definition. |
| 2. Cyclic experiment map | Added a three-row table for ordinary steam/Ar cycling, the five-arm timing diagnostic, and usable policy blocks. Columns distinguish exposure, special-reset timing, and primary endpoint. Pre-reset operating output, post-reset recovery, and policy output before terminal analytical reset remain separate. The caption says “proposed” comparisons; the policy endpoint says ethylene per complete time without introducing an acceptance filter. No new arm or treatment is added. |
| 3. Priority terminology | Replaced “strongest reserve” with “second feasibility priority” for cyclic oxides, including the portfolio evidence note. The six brief reserve ideas remain distinct. |
| 4. Water data locator | Identified Fang's Source Data workbook, sheet “Figure 1,” and separate piecewise-linear interpolation of conversion and selectivity before integrating their product on the combined grid over 25–585 h. The article citation and existing evidence artifact locator provide traceability; no workbook is redistributed. |
| 5. Water feedback stability | Stated positive storage B>0 and the stable stationary-state condition G greater than the local source derivative, evaluated at that state, for the relaxation expression. |
| 6. Polymer component roles | Added W/silica metathesis and Na/alumina isomerization roles and their tandem chain-shortening function. The disputed initial activation of saturated PE and the cause of reuse loss remain unresolved. Checked Conk original PDF p.2. |
| 7. Ag chlorine background | Added gas-modifier deposition and competing removal, including alkane-mediated removal, and their effect on oxidation rates/selectivity. Retained material/condition dependence without a universal coverage or optimum. Checked Iyer and Bhan original PDF pp.1–2 and used the existing citation. |
| 8. References navigation | Added a phantom anchor and contents entry immediately before the bibliography. Contents and PDF outline now include References; the destination was verified against the bibliography start on final page 31. No page number is hard-coded. |

Validation completed:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -cd manuscript/main.tex` passed after the final wording refinements. The complete PDF is **34 pages**.
- Final LaTeX/BibTeX logs contain no warnings, errors, undefined citations/references, or overfull/underfull boxes.
- Inspected the rendered overview, the compact cyclic sequence table on page 12, and bibliography opening on page 31. Text and table fit without clipping. The parent also inspected the table and contents.
- Contents lists References on page 31. `mutool show` verifies the outline and contents link use `section*.12`; its destination points to page object `472 0 R`, which is PDF page 31, at the bibliography start.
- `python manuscript/evidence/check_water_output.py` reproduces reference 116.0351956682559 h, promoted 219.82661932044417 h, ratio 1.8944822564778319, and additive-mass ratio 1.8042688156931732. These remain the existing secondary output proxies, not new measurements.
- Added brief clarification records to the relevant evidence notes. Bibliographic entries and the shortlist are unchanged.

Ready for final parent verification and closure. No additional five-reviewer round is required by the adjudication unless verification reveals a major issue.
