# Coordinator adjudication: Stage 01, Round 01

Coordinator: `/root`. Date: 2026-09-07. Reviewed snapshot: `64708f8c61e751a8447d7955def9a2929c159b2bfc457eae8e2baf1900497f31`.

All five independent reports are complete and were read in full. Each checked the mathematical claims, with independent calculations recorded. Reviewer 2 found no issue. The other reports identify three overlapping groups of minor issues. The coordinator independently inspected the section, checked the central derivations, built the PDF, and inspected rendered page 3; see the supplemental coordinator checks.

## Decisions

1. **Accept R1-01, R3-01, R4-01, R5-01 as one valid minor assumption clarification.** The optional molecular contribution needs a finite nonnegative bulk axial diffusivity and a nonnegative integrable wall axial diffusivity. These assumptions justify the stationary square-integrable Brownian integral. The central flow-only theorem does not use this optional term, and its isotropic example already has the required L1 condition, so the omission is minor rather than a defect in the main theorem. State the conditions near their introduction and explicitly connect finite stationary integrated diffusivity to the variance calculation. Retain the separate uniform-bound requirement in the final comparison remark.

2. **Accept R1-02, R4-02, R5-02 as one valid minor proof clarification.** Positive-spectrum inverse cutoffs alone do not see an atom at zero. The immediately preceding resolvent alternative is valid, and the stationary spectral derivation already includes this case, so the result is supported; nevertheless the advertised alternative self-contained proof must be complete. Add the kernel-projection trial with its zero energy and unbounded source pairing, then apply inverse cutoffs on the positive spectral subspace.

3. **Accept R4-03 as a valid minor explanation issue.** Closability determines which designs define physical dynamics. State its precise sequence criterion and a brief explanation of why it permits a unique closed form in L2. The later positive-floor proof already verifies that criterion, so no additional theorem is needed.

No criticism is rejected. No valid major issue was identified. The relevant claims and their boundaries remain M1–M4 as stated: stationary initialization, a connected one-dimensional wall, fixed positive bulk diffusivity and nonzero mean-speed prefactor, anchored bounded rates, and physical coefficients defined through their minimal closable forms. Nothing in this acceptance process establishes later singular asymptotics or novelty.

## Required correction and next decision

Assign all three groups to `/root/paper_stage_fixer`, who is distinct from the Stage 01 author. Preserve the frozen sources' manifest and all reports. The fixer must log exact changes and verification, run the build, and stop editing. The coordinator will inspect the edits, check the accepted snapshot, and record acceptance before Stage 02 begins. A repeat five-reviewer round is not required unless the correction exposes a major issue or changes a substantive claim.
