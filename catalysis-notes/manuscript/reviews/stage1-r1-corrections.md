# Stage 1, round 1 — corrections

Date: 2026-09-17. Implemented all nine consolidated corrections accepted in `stage1-r1-adjudication.md`, after reading all five reviewer reports. No new major issue was identified. The chapter remains a proposal; none of its proposed experiments or validation results is represented as completed.

| Accepted issue | Change |
| --- | --- |
| 1. Operational conditioning endpoint (R1/R2/R5) | Experiment 1 now starts from the platform syngas atmosphere and specifies how the parent pilot chooses a duration beyond startup using rate/selectivity drift over a defined window. The complete feed, flow, temperature, pressure, and duration schedule is frozen before randomization. Pre-handling drift and retained-liquid observations are reported; stable function does not establish stationary water affinity. |
| 2. Whole-charge recovery and packing (R2) | Identical initial quartz dilution remains with every recovered charge. Repacking adds either the specified PDVB dose or its measured bulk volume of quartz to equal final bed volumes. No selective removal of initial diluent is assumed. Initial/final packing, heat/flow behavior, and solid/liquid recovery are included in the existing handling qualification. |
| 3. Scope of contribution (R1/R4/R5) | Opening and concluding claims now identify a controlled test at a defined catalyst state and disturbance, plus a conditional prediction within the calibrated range. The chapter no longer claims to locate an operating boundary. |
| 4. Two-pool reference and symbols (R3/R5) | Defined pool concentrations, capacities, conductances, common exchange rate constant, total water source, inlet concentration, and gas concentration. Wrote the steady pool-to-gas excess explicitly. The threefold change applies to that quantity; the total pool-to-inlet excess also contains the unchanged gas-to-inlet term. |
| 5. Absolute rates (R3) | Requires both pre-challenge and post-recovery absolute rates for every one of the four conditions, alongside retention and cumulative output. |
| 6. Consequential pulse validation (R4) | Chose output deficit over a fixed production horizon as the endpoint. Pulse duration must separate models consequentially on that endpoint, informing whether the humidity excursion fits an acceptable output budget. Explicitly notes that distinct time constants can give equal deficits through complete recovery. Independent charges, frozen predictions, and uncertainty requirements remain. |
| 7. Challenge and recovery source histories (R4) | Any parent checks used to reject a whole-bed reaction-water source explanation must bracket measured formulation-dependent challenge and recovery histories, including uncertainty. If this cannot be done, retain that explanation. Plateau-only bracketing is explicitly insufficient for post-recovery retention. |
| 8. Reaction and output context (R5) | Introduced cobalt Fischer–Tropsch conversion of syngas to hydrocarbons with water production, defined C5+ as hydrocarbons with at least five carbons, and introduced conversion and carbon-based selectivity before the proxy integral. |
| 9. Bibliographic locators and access distinctions (R1/R5) | Added Paterson volume 430 from the original PDF. Converted Hanssen to an edited-volume chapter entry with volume 109, pages 193–202, editors, book title, series, and publisher. Local original and publisher-indexed metadata checks are recorded in the evidence note. The Sengupta full-text access limitation remains unchanged. |

Both optional improvements were included without adding an experimental campaign: a short prior-art statement credits Fang 2022 additive removal, and the withheld-pulse test compares the functional prediction with a baseline built from inlet humidity, calibrated steady response, and apparatus delays using the same data.

Edited source files are `sections/01-water.tex`, `references.bib`, and `evidence/stage1-water.md`, plus this correction record. The source library and other repository sources were not edited.

Validation completed:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` in `manuscript/` passed and produced the updated eight-page `main.pdf`.
- Final LaTeX and BibTeX logs contain no warnings, undefined references/citations, errors, or overfull/underfull boxes. Extracted PDF text confirms the updated bibliography; rendered pages 4 and 7 were inspected for legibility and fit.
- `python manuscript/evidence/check_water_output.py` passed: reference 116.0351956682559 h; promoted 219.82661932044417 h; ratio 1.8944822564778319; ratio including 5% PDVB mass 1.8042688156931732. These remain source-series output proxies with the stated limitations.

The corrections are ready for parent verification and Stage 1 closure. No repeated reviewer round was needed under the adjudication.
