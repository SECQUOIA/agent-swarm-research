# Stage 4A corrections

Implemented all three minor corrections accepted in `stage4a-assessment.md` after reading that assessment and independent review 1.

1. Corollary `proper-smooth-frontier` now explicitly requires an integer dimension cap `d >= 3`. Its formulas and proof are unchanged.
2. The topology appendix now states that the joint-cover theorem strengthens the abstract splitting restrictions **at capacity equality**. Equality of actual channel ranks is not substituted for this hypothesis.
3. The individual-channel normalization paragraph now explicitly requires positive capacity as well as rank equal to that capacity everywhere. This excludes zero-capacity channels, for which saturation alone does not exclude vertices.

Checked the nearby arguments against the joint-cover theorem: the corollary uses integer capacities; the comparison retains the distinction between ranks and capacities; and the individual normalization uses the theorem's positive-capacity argument to obtain nonzero complementary boundary factors. The following submersion propositions already require positive target dimension. No further inconsistency was found, and no scope was broadened.

Validation: `conda run -n qipm --live-stream make` completed successfully and produced the 55-page `main.pdf`. The build log is `audit/stage4a-corrections-build.log`. The final LaTeX log and bibliography log contain no warnings, unresolved references or citations, or overfull/underfull boxes. The only match for “Rerun” is the routine package description for `rerunfilecheck`.

Only the two specified section files and this correction record were edited as manuscript sources. Generated build outputs were refreshed. No later stage was marked complete.
