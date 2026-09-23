# Stage07, round01: coordinator adjudication

Date: 2026-09-07. Reviewed snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`.

The coordinator read all five reports in full. Each reviewer verified the same 27 frozen files, independently derived the new trial comparisons and numerical factors, and checked saved feasible designs and discrete bounds. Their reports contain their own mathematical and numerical reasoning. The coordinator separately checked both new asymptotic consequences, independent dense/sparse formulations, saved numerical values, primary literature and all 54 PDF pages. No major issue was found. Earlier stage acceptance was not used as a substitute for checking dependencies.

## Decisions on every finding

| Finding | Decision | Required correction |
|---|---|---|
| Reviewer1 R1-07-1: mesh changes below optimization gaps | Valid minor | State that the eta=0 and eta=2 mesh comparisons show stability of returned objective values but do not separately resolve spatial error, since the differences lie below remaining optimization uncertainty. No additional optimization is required for this limited claim. |
| Reviewer2 M1, reviewer3 R3-01, reviewer5 R5-01: percentage rounding | One shared valid minor | Change 0.0159% to 0.0158%. The raw relative change is 0.00015841231081359375, so the corrected percentage follows directly. |
| Reviewer4: “unnormalized responses” | Valid minor | Replace with “unscaled ensemble moments.” The JSON stores aggregate moments after equal mobility-budget normalization; it does not store every individual offset response. |
| Coordinator: missing spaces in new audit prose | Valid minor | Correct missing spaces before numerals in Stage07 authored audit/README/plan/claim prose and the Stage07 build record, preserving identifiers, code, equations, versions and historical hashes. |

No submitted criticism is rejected. Reviewer2's incidental phrase “nonzero wall velocity scale” is inaccurate shorthand in the report, not a manuscript finding: the manuscript correctly assumes zero longitudinal wall advection and nonzero stationary mean speed V. The source must retain those actual assumptions. Original independent reports remain unchanged.

The asymptotic trial arguments are sound: the integrable unrounded mean profile dominates a factor tending to one times the normalized rounded profile; the critical distance and sine profiles agree to arbitrary relative accuracy on fixed-small retained fold neighborhoods, with all omitted contributions lower order. The circle finite-volume comparisons use equal discrete mass; the local tangent bound follows from exact convexity and is expressly limited to the finite-dimensional, finite-quadrature objective, with no interval-arithmetic claim. The literature positioning credits established tools and records access limits.

Assign the separate fixer to all four items. Once the coordinator verifies those corrections and a clean build, this stage can be accepted without a second Stage07 review round, since there is no valid major issue. The separately mandated five-reviewer whole-manuscript audit must then begin.
