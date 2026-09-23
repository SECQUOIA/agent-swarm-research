# Stage 4, round 1: independent review 2

**Findings: 0 major, 0 minor.** No required repair found.

Reviewed the abstract, introduction, conclusion, reproducibility appendix,
overview figure and script, diagnostic script, README, Makefile, packaging
script/archive, bibliography, final source ledger, and author audit. I did
not read peer reports. Frozen manuscript and generated artifacts were not
modified; build and regeneration checks used a fresh extraction under
`/tmp/spectral-shift-review2-stage4-3uhgtay8`.

## Figure and numerical accuracy

- Inspected the overview image and its generating code. The left panel
  places transitions at numerical evaluations of the proved `G_r`, with
  filled markers on the cheaper tier and open markers on the excluded
  higher tier. The final visible segment ends before the next threshold.
  Exponent zero is correctly qualified in the caption to include the
  logarithmic coarse cost when `c<1`.
- The right panel's entire range is justified: `G_1(2)<1/32`, the sextic
  witness gives `F_3(2)<1/32`, and `F_1=F_2=1/24`. Thus unrestricted
  exponent `1/2`, the even jump from `1/2` to `5/6`, and odd exponent one
  apply throughout the displayed ranges. Equality markers are correct.
  The odd logarithmic factor is shown. Neither the plot nor caption
  presents the witness bound as the exact value of `F_3`.
- Regenerated both scripts in `qipm`. All three CSV files and both PNG
  previews were byte-identical to the frozen outputs. The overview
  reproduced `G_1=0.0211310131443375` and witness bound
  `0.020011288318253`; supplementary pinned diagnostics reproduced their
  reported values. These computations remain illustrations, not global
  feasibility certificates, as the appendix and README explicitly state.

## Reproduction and package checks

The supplied ZIP passes its CRC check, contains the expected 18 files,
has no absolute or parent-traversal paths, and every archived file matched
its frozen counterpart byte for byte. It includes all eight sections,
macros, bibliography database and generated bibliography, the required
figure PDF, all three scripts, README, and Makefile. Audit files, local
literature, previews, and build products are excluded.

From the fresh extraction I successfully ran:

```text
conda run -n qipm --live-stream make
conda run -n qipm --live-stream make figures
conda run -n qipm --live-stream make submission
```

Both builds produced 31-page PDFs with text identical to the frozen PDF.
Final LaTeX and BibTeX logs had no warnings, unresolved references, or
overfull/underfull boxes. The repackaged ZIP again passed its CRC check
and contained 18 files. The ordinary build invokes no Python; the bundled
figure and bibliography support the documented standalone workflow.
The Makefile retains those supplied resources when cleaning.

The installed Python, NumPy, SciPy, and Matplotlib versions match the
README exactly. Scripts resolve their input/output paths relative to
their locations, use no external data, and need no random seed.

## Presentation and mathematical consistency

The abstract and results overview preserve the proved distinctions:
positive fixed-accuracy tiers and their equalities; `c<1` versus `c=1`
coarse costs; single-transform parity restrictions; the positive-`K`
matched high-accuracy regime; and the unresolved intermediate
multiplicative optimum, including its boundary-margin factor. The
conclusion accurately identifies the remaining questions.

The LP summary keeps dual-state preparation separate from reusable
compilation, retains counted right-side access and the matrix-only
compiler contract, identifies the zero-query coarse exception, and
states that the primal predictor is public. No end-to-end LP or QIPM
lower bound is implied. The introduction also clarifies that subsequent
applications of the reusable circuit incur its oracle queries again.

Independently checked 100 unique labels and all reference targets;
all 18 bibliography entries are cited and all citation keys are defined.
The final ledger's explicit theorem numbers agree with the rebuilt
auxiliary file. Its corrections and strengthening agree with the
previously reviewed mathematics, including the even plateau and the
LP coarse-tier correction.

## Citation scope

Primary-source spot checks support the new framing and metadata,
including [Dong et al.](https://arxiv.org/abs/2608.30937),
[Somma–de Wolf](https://arxiv.org/abs/2608.24493),
[Laneve](https://quantum-journal.org/papers/q-2026-03-13-2025/),
[Sarkar–Yoder](https://arxiv.org/abs/2111.07182),
[King et al.](https://journals.aps.org/prl/abstract/10.1103/m3fj-m4rm),
[Haah](https://quantum-journal.org/papers/q-2019-10-07-190/), and
[Campos-Pinto et al.](https://epubs.siam.org/doi/10.1137/17M1131891).
The manuscript distinguishes its specific quantitative results from
prior synthesis, constrained approximation, and factor-access tools.
The qualified originality statement is appropriately bounded; this
review does not certify universal priority or literature completeness.
