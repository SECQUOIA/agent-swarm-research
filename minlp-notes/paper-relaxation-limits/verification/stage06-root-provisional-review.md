# Stage6 coordinator provisional proof reading

This is ongoing independent reading during sole authoring, not acceptance. The integrated text and author ledger will be frozen only after completion, then receive15full-stage reviews.

## Point-packing appendix

Read full draft at SHA 872f052a1ab44004350a100523c450009dfa445d08069b5c1651532170752cb9. Independently reconstructed the RLT pair bounds, all six group-pair distances for both constructions, diagonal secants and off-diagonal McCormick feasibility, variance/averaging SDP upper, block-projection covariance PSD and dimension scaling. k=2 boundary attains the required1/2; k-1=floor((n-1)/4) and all n restrictions are correct. Reopened Khajavirad2404.03091v1 original HTML to recheck model/citation context. No mathematical defect found in this draft. Existing root exact151032RLT checks provide finite evidence, not the PSD proof.

The Beach locator question is resolved as two different packages; the exact intended71-page v1 remains unchanged. See stage06-additional-primary-checks.md for current paths/hashes and corrected record.


## Scaling appendix

Read full draft SHA 2690b9ce64e1a0c4c53e46b3526f247a927a6dad05ef67abf7133f106d77e3c7. Reconstructed two-endpoint interpolation, fixed-T multiplicities, zero-weight conic recession argument, all16lower/upper S-comparisons giving the projected bilinear system (including ell=0), both cost counterexamples, exact extensive-only size-biased/product-weight perspective proof, finite diagnostic-cost rectangularity via closed fibres, integral-count convex decomposition without IDP, and Shapley diameter/Lipschitz limits. No mathematical defect found. Asked author to restate nonempty compact E_j in the integral-count subsection as a local hypothesis clarification. The final source-dependent-scale example is correct: (2,4) differs from chord value5.


## P-split appendix

Read full in-progress draft SHA cedcd34bb58c1b1f3afb95124b6902988ab66b009d3ffff875aa692692ac709e. Reconstructed retained-box/higher-dimensional counterexamples, fixed-c auxiliary-hull sufficiency, downward projection, transverse grouping, exact Hausdorff derivative and limit, irrational and rational coordinate comparisons with exactly transformed domains, arbitrary auxiliary-only witness domination, and aligned exact-image/SOC repair.

Two authoring issues sent to sole author before completion/freezing: (P1) directional-repair proposition must explicitly assume R contains the full true feasible set, not merely the two selected points, to conclude strict hull containment; canonical wording calls it a valid relaxation. (P2) truncated disjuncts have flat box-facet boundaries, so call their defining quadratics strictly convex rather than calling the sets strictly convex. P1 affects the standalone theorem hypothesis and is required; P2 corrects a mathematical terminology error. The remaining proof calculations check. These are pre-freeze authoring corrections, not results of the yet-unstarted formal Stage6 fifteen-reviewer round.

Root checked both P-split corrections in the live text: full-set validity now explicit, and strict convexity correctly describes the defining quadratics. The scaling count subsection also explicitly restores nonempty compact unit types. These pre-freeze authoring issues are resolved.


## Correlation face and global lift-size appendix

Read full draft SHA 6fdeff3ed133581353a4b6bad60062fc7397de35b421218dbbb6c489bafa7ab9. Reconstructed trace-face equality, paired face/inverse, exposure inequality, generator rounding bounds u<=6SD,v<=8SD,h<=SB+8SD, the4SB+58SD+5|S-m| estimate, constants136m+10 and184m+6, zero atom and finite convex combinations. Verified exact penalty, l1 block map norms and nonpolyhedral K2 curve argument.

Checked inherited fixed-block constants and Lorentz dimension convention against mapped canonical source (primary Fawzi/LRS inputs were inspected in earlier root source audits). For approximate LP, coefficient norm1 yields fixed-dilation2 sandwich. For PSD, f_k+theta remains[0,1], mean>=(6k)^-1, strict negative delta=1/(16k²), k^(-23/4) prefactor and k^(13/2) denominator all match. The minimal-face strict-feasibility reduction and nonnegative offset supply a q+1 factorization without assuming a proper original lift. Choosing odd k comparable to small a(m/logm)^(2/13) gives the asserted growth. J's l1 norm<=m gives A_m epsilon. No mathematical defect found.

Asked author to include explicitly the mapped approximate-SOCP consequence: at fine accuracy total cone dimension is superpolynomial by conversion to total PSD order. It must not be upgraded to the exponential exact-SOCP conclusion.


## Primitive FBBT appendix

Read the full appendix and reconstructed the least-fixed-point fairness argument, positive/negative circuit normalization, acyclic complements, detector roots, gap amplifier, rational feasible-point count and directed SCC sizes. Rechecked the stronger initialization under the same schedule, both simultaneous primitive hull updates, the lower-bound invariant and exact count K >= 2^(2^n-1). No core mathematical defect found. Requested explicit contraction for additional sound updates and a short derivation identifying the classical Kleene consequence as our inference from displayed Newton examples. Both are now included and the complete revised appendix was reread. The e_0(k)>=1/(k+1) induction and repeated-square-root bound are correct. PosSLP, fixed-point approximation, local stationarity and primitive iteration remain distinct.

## Integrated narrative and integer-precision comparison

Read main.tex in full (abstract, introduction, roadmap, input order), Sections16 and17, and the entire integer-precision appendix. Reconstructed square midpoint diameter and sharp secant/tangent error, scalar-product area integral, closed parity-class cover, edge-width bound20 epsilon, anisotropic fractional-cover program and shared-bit residual expansion. These statements count integer coordinates or binaries, not spatial certificates. Primary midpoint lemma and the exact intended Beach preprint version were independently inspected in the source record. Checked the added approximate SOC consequence: conversion to PSD order at most twice total Lorentz dimension proves only the approximate superpolynomial conclusion. No mathematical defect found in these additions. Narrative distinguishes the positive-envelope family from signed XOR, exact versus approximate resources, inherited classical inputs, and explicitly open problems.


## Provisional layout and coverage checks

Viewed rendered pages 1, 4, 77, 95, 98, 104 and108 of the111-page integrated draft (PDF hash fd01bf4f313e230f887ca56b678bd814580d69c142c06dc0bb2f67591496bb66). All inspected displays, table columns, headings and reference text are legible and unclipped. This is a sample of the current draft, not a claim to have visually inspected every final page. Sent a clarification making the abstract's coordinatewise graph transfer explicitly refer to the cardinality family, and an epsilon>0 domain clarification for the integer-comparison opening. Formal Stage6 review remains pending.

Read the entire cumulative coverage ledger, including the previously truncated middle in a separate complete read. Automated path/label comparison found no nonexistent mapped source or label; one search-audit record needed an explicit status mapping and was sent to the author. These lexical checks do not establish mathematical coverage by themselves.


## Author package completed and frozen

Read the full final author record, README, PROCESS and source-validation JSON. Verified all14 recorded original PDF hashes and all build-input/PDF hashes against current files. Independently reran the integration checker after reading it in full: all three exact scaling polytopes,168 signed-slack cases, rotation identities,308 labels and21 accepted-file comparisons pass. The abstract family qualifier, epsilon>0 and search-audit mapping are present. No pre-freeze authoring issue remains unresolved. Frozen Stage6 round1 PDF is343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916,111pages, no reported warnings. Separate review-context documents are preserved with hashes alongside the manuscript snapshot. This completes the authoring gate only;15independent full-stage reviews now begin.
