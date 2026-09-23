# Stage 5, round 1 — corrections

Date: 2026-09-17. Implemented all three accepted minor findings from `stage5-r1-adjudication.md` in `sections/05-shortlist.tex` and reflected them in `evidence/stage5-portfolio.md`.

| Finding | Correction |
| --- | --- |
| 1. Undefined Ni/M | Defined Ni/M as Li's supported-Ni control without intentionally added W. Retained the 29.5% preleachate comparison against the 27.1% control and all limits on attribution. |
| 2. Ambiguous Pd/SSZ-13 comparison | Named both ST-CO-N2-O2 and ST-CO-O2, explained the former's extra N2 treatment between CO and O2, and specified applying the crossed NO/sulfur test to both. Preserved matched histories, inventories, and the application requirement. |
| 3. Unexplained extraction prediction | Removed “directional extraction prediction” and stated directly that mannose cannot be assumed to form an inactive reservoir. Retained the productive-feed evidence, epimerization caveat, possible inactive fraction, and exploratory hold. |

The entries remain brief. No bibliography, library, or closed-program chapter was edited.

Validation: `latexmk -pdf -interaction=nonstopmode -halt-on-error -cd manuscript/main.tex` passed and produced a 34-page PDF. Final LaTeX/BibTeX logs contain no warnings, errors, undefined references/citations, or overfull/underfull boxes. The four closed chapter SHA-256 hashes match their values before these corrections:

- Water: `34792454be1aa5930c992591ba95390a898726d0620dc8effbeee92d622f7a3c`
- Cyclic oxides: `1828b7b736451112b2a6ab80d03ac9725481cc5ad5d1962121de1dcf2c75b77f`
- Polymer: `806c7b23708b512411bd879c180841e34dee45a6ee599e147eedebfd30c96fd4`
- Silver: `644e433cee05c26deec1d06541f572105bcf44e9d7a2dd6f5f0784d63887ad00`

Ready for parent verification and Stage 5 closure. No further stage-specific reviewer round is required by the adjudication.
