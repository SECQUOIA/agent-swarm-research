# Stage 6 corrections

The separate correction author read the coordinator's first-round assessment
and all five complete reviewer reports. All five accepted minor corrections
are complete; no accepted issue remains pending.

1. The discussion now attributes reuse of a gated global upper bound to the
   unconditional information ordering, with a reference to Proposition 2.1.
   A separate sentence gives the condition-dependent comparison its proper
   role of bounding possible efficiency loss.
2. The discussion cites Bansal and Xu's growing-dimension A/E-design hardness
   for additive rank-one information under partition constraints, even with
   invertible feasible information matrices. It states the direct consequence
   ruling out polynomial approximation factors in that dimension unless P=NP,
   and explains consistency with the fixed-dimensional cover. The citation
   concerns A/E criteria, with no extension to weighted trace. The correction
   author independently inspected the primary v1 full text, Theorem 1.1, the
   entire reduction and inverse proof, and the final encoding-length argument;
   the primary abstract page confirms 5 August 2026. The new bibliography entry
   and literature record identify that version. The bibliography now has 58
   entries, all cited. Earlier author-stage counts remain historical records;
   the literature record explicitly distinguishes its earlier freeze from the
   present count.
3. The discussion now separates complete-packet and fixed-covariance promises
   for the temporal schemes from fixed information dimension and explicit
   rational feasibility representation for the abstract additive cover. Its
   grid-refinement and correlated-history matroid boundaries are retained.
4. The introduction uses plural verbs for Hainy et al.: “prove” and “develop.”
5. The introduction uses “consequences for estimable contrasts,” and the
   discussion uses “result for represented matroids.” These remove the
   source-newline spaces inside the former compound expressions.

## Verification

The final forced build completed successfully:

```text
latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The final PDF has 66 pages. Its final log has no warnings, undefined references,
overfull boxes or underfull boxes. The new reference uses the descriptive
publication field “Preprint, arXiv:2608.05468v1”; this also avoids an underfull
line encountered in the first build of that entry. The final transcript is
`/tmp/stage06-corrections-build.log`; the persistent final LaTeX log is
`build/main.log`.

Independent source checks found 204 unique labels, no unresolved references,
58 unique bibliography keys, all 58 cited, and no missing citation keys.
PDF text inspection confirmed the corrected plural verbs, unconditional
ordering attribution, separate assumptions, scoped A/E hardness statement,
and both replacement phrases. Neither broken compound remains in the PDF
text. No scientific computation was rerun because no executable mathematics,
model array or numerical witness changed.

SHA-256 comparison against all 204 first-round frozen files found exactly four
changed files: the introduction, discussion, bibliography and literature log.
All other 200 frozen files are byte-identical. Both supplement manifests still
validate: 159 archived files and 11 new-source files. This correction report
is the only additional source file. No accepted proof, data, executable,
snapshot, PROCESS.md, original repository source or unrelated paper was edited.
