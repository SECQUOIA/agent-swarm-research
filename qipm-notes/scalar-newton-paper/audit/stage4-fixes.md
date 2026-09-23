# Stage 4 corrections

All four accepted minor groups in `stage4-assessment.md` are addressed.
No theorem, proof, parameter regime, or mathematical result was changed.

1. **Prior fixed-state access distinction.** Section 6 now explicitly
   credits Alase et al.'s fixed-computational-basis comparison: their
   block-query lower bound persists, while one exact-entry query suffices.
   The contribution here is stated as the matching condition-number
   dependence for the relative inverse form and a realization of that
   access distinction for this task. Checked the discussion after Theorem
   IV.13 and Appendix A in the [primary PDF](https://arxiv.org/pdf/2111.10485),
   PDF pages 17 and 22.

2. **Build dependencies and missing bibliography.** The Makefile now
   declares `main.bbl` as a target, makes the PDF depend on it, and requires
   both outputs for ordinary builds and packaging. Its recipe generates
   the auxiliary file and runs BibTeX; the PDF recipe runs three LaTeX
   passes. The third pass is needed in the reproduced missing-bibliography
   case to stabilize references after the citation widths change.
   In a temporary copy with an otherwise current PDF, deleting only
   `main.bbl` was repaired by ordinary `make`. The same deletion followed
   by `make package` also repaired the bibliography and produced a valid
   package. Both final logs were clean and `make -q` reported that the
   default target was current. The temporary ZIP had 24 files and matched
   its corresponding source files byte for byte.

3. **Visible full-version locators.** The bibliography's rendered `note`
   fields now link explicitly to CGJ `1804.01973v2`, Apers--Gribling
   `2311.03215v3`, and Montanaro--Shao `2311.06999v3`, retaining their
   publication records. The introduction now identifies CGJ Theorem 33
   as belonging to the full version. All three versioned identifiers are
   present in the regenerated `main.bbl`.

4. **Journal metadata.** Added volume, issue, and pages for
   Aaronson--Ambainis, *SIAM Journal on Computing* 47(3), 982--1038 (2018),
   and Apers--Gribling, *SIAM Journal on Computing* 55(1), 93--134 (2026).
   Independently checked the publisher's information panels for
   [Aaronson--Ambainis](https://epubs.siam.org/doi/abs/10.1137/15M1050902?journalCode=smjcat)
   and [Apers--Gribling](https://epubs.siam.org/doi/10.1137/25M1736098).

Validation used the `qipm` environment. A forced build and packaging pass
succeeded; the manuscript remains 59 pages. The final LaTeX log has no
warnings, undefined references or citations, or overfull/underfull boxes.
All five numerical diagnostic scripts passed, including the 152
structured-system identities. The submission ZIP was regenerated after
the final Makefile change. The stage workflow and source map were left
for root to update. The separate whole-manuscript review remains pending.
