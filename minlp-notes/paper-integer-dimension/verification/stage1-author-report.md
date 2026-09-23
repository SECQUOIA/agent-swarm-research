# Stage 1 author report

The stage 1 mathematical draft is complete and ready for the prescribed fifteen-reviewer gate. No later-stage mathematical text was drafted. I did not delegate this drafting task.

## Files

- `sections/01-foundations.tex`: standalone mathematical draft, organized as four manuscript sections: representation/contact geometry; scalar rank/inertia; quadratic-system noncommutative rank; smooth maps and perspectives.
- `references.bib`: eleven references, with primary-version metadata and source distinctions. The journal author order for Lubin–Vielma–Zadik follows root's direct check, correcting the ordering in the local metadata note. Both Beach papers are recorded as the published 2024 versions.
- `coverage.md`: 43 canonical result files, 32 explicitly identified supporting developments or source comparisons, and 173 supporting note/audit files. Every canonical development is assigned to a stage. Superseded bounds, distinct proofs, algorithmic dependencies, counterexamples, and unresolved boundaries are identified.
- `verification/check_stage1_folding.py`: 455 numerical LP checks of the independently expanded continuous folding argument. All passed.
- This report.

The current integrated document compiles as an 18-page PDF. Root owns the final build and review snapshot. My last completed build before the final minor parity-mixture and bibliography additions had no warnings or overfull boxes; the one 15.8pt overflow in the rational-scope paragraph was repaired by rephrasing. A final rebuild follows this report.

## Mathematical coverage drafted

1. General convex lifts, finite but unrestricted continuous dimension, nonclosed convex sets, unbounded integer ranges, graph containment and vertical error. Distinct binary-linear minimum convention, affine transformations, restrictions, fixed-index convex sections, common-lift convex combinations, parity contacts and closure without measurability assumptions.
2. Exact logarithmic encoding of finite bounded polyhedral unions, with proof and common-recession extension.
3. Strong-curvature volume lower bound; exact square minimum; finite product bounds; width and area geometry; four-point obstruction to improving width constant to four; unequal graph-tolerance LP and fractional vertex cover; shared dyadic prefixes; exact bounded binary products; rational preprocessing.
4. Indefinite scalar contact-volume determinant lemma, explicit scalar-rank constants, compact signed-square construction; one-sided inertia, zero-binary compact positive-square epigraphs, exact one-sided product error for convex lifts, and linear-threshold qualification; logarithmic lower bound on LP epigraph row count.
5. Nc-rank algebraic imports with precise source identification, Hermitian principal compression, complex-to-real shrinking descent, symmetric coordinate structure, capacity and elementary Hall/permanent energy routes, fourth-moment identity, volume/covariance bound, finite nc-rank lower constant and matching compact binary upper. Explicit squared-Hessian certificate, cross-product rank gap and direct sums. A direct consequence connecting graph matrix-space rank to twice fractional cover is included.
6. Rational nc-rank construction and uniform precision statement, with explicit notice that its full bit-complexity proof belongs to stage 2.
7. Smooth local/global ranks; full local oscillatory estimate proof via TT*, integration by parts and Schur; real matrix-evaluation phase; arbitrary-contact volume bound; smooth anisotropic Taylor cells; fixed-degree polynomial prefix compiler; product and rank-deficient polynomial examples; reduction from circuit polynomial identity testing.
8. Constant scalar Hessian rank through partial Legendre charts and genuine polyhedral tubes; full boundary and compactness argument; Euclidean norm rotating-nullspace counterexample and angular illustration; unresolved rank-changing/vector scope.
9. Positive perspective row homogenization with no extra bits, exact binary-times-positive-scalar encoding, lower slicing transfer, rational-size preservation, quadratic-over-linear examples and ordinary-box version.

## Verification and additions beyond transcription

I independently derived the determinant constants, covariance fourth-moment factors, capacity-to-volume exponents, real shrinking descent, symmetric zero-block allocation, endpoint coverage of prefixes, residual product error, local analytic phase mixed Hessian, and Legendre-fiber identities. The canonical proofs and their central audits were read for the stage 1 results. Root independently ran seven preexisting stage 1 checkers, all passing, and checked the nc-rank and perspective arguments.

The manuscript proves the square upper bound directly using residual decomposition, so exact optimality does not depend on taking the sawtooth error formula on faith. It also supplies a standalone continuous folding LP proof for the compact zero-binary square epigraph, replacing a black-box invocation. The added LP check directly optimizes over relaxed internal folding variables, rather than only evaluating the exact fold sequence. This tested 455 projected fibers at depths one through seven.

The TT* proof explicitly shrinks to a neighborhood where the mixed Hessian stays close to one fixed invertible matrix. This avoids the invalid inference that an average of invertible matrices is invertible. The constant-rank proof bounds error throughout each polyhedral tube, not merely on points with a selected gradient parameter. The manuscript keeps arbitrary finite integer mixtures separate from the much weaker parity-midpoint condition, which will support the later exact separation results.

No substantive stage 1 theorem was invalidated during drafting. I found and repaired local writing/LaTeX errors in the authored draft: a transient width-order typo while entering McCormick inequalities, three single-backslash align row terminators, and one overfull paragraph. These never changed the final mathematical statement. Root's author-order correction is incorporated in the bibliography.

## Source verification

Read `literature/AGENTS.md` and its knowledge-base conventions before literature use. Existing literature metadata, extracted texts, canonical notes and audits were used; no user-supplied literature was redistributed or modified.

Primary online texts were opened for GGOW (published 2020 paper), the IQS revised full manuscript, Volčič (arXiv full manuscript, matching 2021 journal record), Nicola (2008 manuscript) and Wolff's March 2002 notes. GGOW Theorems 1.4/1.17 and 2.18, IQS Theorem 1.5 and field-extension Lemma 5.3, and the free-field involution convention are the imported algebraic facts. Root also retrieved GGOW, Nicola and Wolff into the build source cache and checked their statements. The direct Hörmander PDF retrieval failed, but the publisher record confirms author, title, year, volume, pages 1–11 and DOI; Wolff's exact Theorem A and the complete proof supplied in the manuscript verify the analytic result used. No claim of having directly read the unavailable original full text is made. Boyd–Vandenberghe's official book page confirms the book and authors; perspective transfer itself is proved directly here.

Priority is not established by these checks. The text credits algebra, parity, McCormick/sawtooth, oscillatory analysis, affine fibers and perspective geometry as established ingredients. Final introduction and novelty comparisons remain stage 4/5 work.

## Explicit pending obligations and limits

- Equation `eq:rational-rate-preview` is a precise preview, not a completed stage 1 proof: stage 2 must give the rational basis-height, exact depth and uniform capacity lower-bound details. This is the only intentionally deferred proof of a displayed result in stage 1.
- Rank-changing scalar smooth maps and vector maps with unequal local/global ranks remain unresolved. These are stated as boundaries, not solved claims.
- Stage 2 grouped PSD error budgets may have unrestricted output directions. The stage 1 error-body definition is compact and full-dimensional; the later stage must explicitly extend the convention or quotient measured directions.
- Several source notes use `p_bin` for arbitrary convex binary lifts. The manuscript convention is binary **linear** lifts. Exact separation lower bounds should explicitly say they apply to the larger convex-binary class, then pair with their MILP upper constructions.
- The inventory identifies a previously easy-to-miss note-only finite theorem for separable continuous convex vector outputs and its facet version (`convex-separable-vector-finite-rank-precision.md`). It also records the unresolved one-input constant-gap question and failed lattice/Helly amplification routes. These must enter stage 4 with their proper scope.
- No external review, journal acceptance or absence of all possible errors is claimed. Fifteen independent reviews and the final whole-paper gate are still required.
