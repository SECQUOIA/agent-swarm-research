# Stage 2 correction pass

Implemented all nine minor corrections accepted in `stage2-round1-adjudication.md`. This was the separate correction pass following the five independent reviews. The theorem scopes, reduction mechanisms, and proof calculations are preserved.

| Accepted item | Change |
| --- | --- |
| 1. Bypass-degree comparison | The introduction to `s3:five-thm` now cites `s5:arbitrary-exceptions`, distinguishes bypass degree from total physical degree, and retains the fixed-exception, exact-ordinary-contract, and redundant-pool-bound conditions. It explicitly states that the preceding construction already has total output degree at most three. |
| 2. Positive concentration bound | Renamed `s3:tolerance` to “Positive strict-output concentration bounds” and adjusted the adjoining example title. The proof states that the concentration constraints hold exactly and does not permit arbitrary numerical residuals. |
| 3. Rational approximation output | Approximation recovery now explicitly uses binary rational feasible arc flows in the ordinary bit model, with output length bounded by running time. The positive-bound proof uses the equivalent exact rational test `d_v <= eta(a_v+d_v)` and handles empty pools separately. |
| 4. Weighted matching edges | `s3:weighted` identifies the clean-input/strict-output edge of weight alpha and dirty-input/lax-output edge of weight beta. Their common color is the pool, and the two edges per color have disjoint endpoints. |
| 5. Degree-one attribution | Added Haugland 2016 Proposition 3 at the degree-one LP paragraph, retaining the self-contained mass/quality argument. |
| 6. Final contract inventory | Added a compact table of all final external-node types, their exact or variable supply/demand/quality contracts, and physical degrees. It lists precisely the two conversion fillers, anchor, and two primary outputs as exceptions. The exclusion of unnecessary designated reporting ports remains explicit. |
| 7. Circuit convention | `s3:linear-circuits` now says “rational system of linear equations and weak inequalities.” |
| 8. Physical copy diagram | Added native TikZ full and half gadgets with physical arcs, assigned middle sources, open endpoint ports, complementary flow values, exact supplies/demands, upper qualities, and capacity conventions. Separate full/half zero-port cycles show distinct occurrences and actual zero-source arcs. The caption identifies the separate coupling equation and its distinct half occurrences. |
| 9. Single-flow prior work | Added Haugland 2019 Definition 2.2 and Proposition 3.1, printed p.96, near the pure-mode discussion, plus the bibliography entry. The text distinguishes imposed active-flow restrictions in that work from proved integral replacement in the present continuous family with simultaneous degree/data restrictions. |

Changed manuscript files:

- `papers/pooling/sections/03-restricted-hardness.tex`
- `papers/pooling/figures/full-half-copy.tex` (new native figure)
- `papers/pooling/bibliography.bib` (one new entry)

No other manuscript section or literature package was modified. Before editing, I read `literature/AGENTS.md`; the local Haugland 2016 Proposition 3 and Haugland 2019 Definition 2.2/Proposition 3.1 texts support the two citation changes. Root had independently verified the 2019 original PDF at PDF p.2, printed p.96.

Validation used an isolated source copy, including both figure files, in `checks/stage2-corrections-build/`. Running `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded and produced a 95-page PDF. Final source copies match the three edited manuscript files. The final TeX log has no errors, undefined references/citations, LaTeX warnings, or overfull boxes. It has eight underfull boxes elsewhere in the full-paper output. BibTeX reports the two existing empty-year warnings for `s6:boveroux2026` and `s6:lrs-full`; both entries are unchanged from the pre-correction bibliography. The new Haugland entry resolves correctly.

I rendered and inspected the copy figure on PDF p.39 and the final inventory on p.46. An initially tight pair of half-gadget flow labels was separated by placing endpoint labels on the outer sides of their respective arcs. The final figure has readable labels and separate full/half cycles; the inventory is legible and fits on one page. Root also inspected both renders and accepted them visually and mathematically. No duplicate mathematical tests were added for these exposition changes.

Evidence is in `checks/stage2-corrections/`: pre-edit files, `correction.diff`, `validation.json` with source hashes, extracted final PDF text, and `figure-page39.png` / `inventory-page46.png`. The isolated build retains its source, PDF, and logs. No accepted correction remains unresolved.
