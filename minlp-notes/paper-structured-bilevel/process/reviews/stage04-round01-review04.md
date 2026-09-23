# Stage 4, round 1: independent review 04

Recommendation: accept after the two minor corrections below. I found no major defect. In particular, the new sharp response modulus has a valid active-pattern argument, an applicable noncompact component bound, and a polynomial-bit sufficient constant.

## Frozen source and scope

I verified all 11 files in `process/snapshots/stage04-round01/SHA256.json`; its digest is `4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`. All verification outputs are under `verification/reviewer04/stage04`, including `snapshot-check.txt`.

I read all of section 4 and appendices B/C, checked their integration with the accepted prerequisites, and inspected `main.tex`, README, bibliography, and coverage changes. I compared the coverage and assumptions against the five canonical accuracy results, the positive and signed inverse notes, and the signed-marginal and aggregate/polynomial-upper dependency addenda. I did not read other stage 4 review reports or root conclusions, edit manuscript source, or delegate. Historical PASS labels were not used as mathematical evidence.

## Required minor corrections

### M1. Include the nonlinear inverse-argument degree in the substitution bound

Location: `sections/04-accuracy.tex`, lines 538–540; compare the polynomial inverse arguments at lines 384–388.

The stated bound `D_up max{1,d_p}` is correct if `d_p` means the degree of the already-composed response polynomials `p_i(v)`. The text instead defines it as a bound on the inverse branches, which are univariate polynomials in their target argument. When the aggregate is nonlinear, composing such a branch with `a_i(v)` multiplies its degree by the argument degree.

A valid example is one follower with `g(z)=z`, `U=1`, `phi(w)=w^4/4`, incentive `ell(x)=x`, and upper objective `H=z`. The interior inverse branch is exactly the degree-one polynomial `h(a)=a`. Its compressed response is `p(x,w)=x-w^3`, of degree three. In normalized coordinates it is `x-(2t-1)^3`, still degree three. The branch has genuine candidate points: `w=z=1/4`, `x=17/64` gives exact consistency and an interior response. Thus this is not just an irrelevant polynomial outside the candidate construction. The displayed degree bound gives one for this example.

Remedy: define `d_p=max_i deg_v p_i(v)` after composition, or introduce `d_h` for the univariate inverse-branch degree and `d_a=max_i deg a_i`, and use `D_up max{1,d_h d_a}`. State that `d_a` is polynomially bounded by the aggregate's numerical degree. The overall polynomial-time conclusion remains valid; this is a correction to its explicit degree accounting. The independent diagnostic records the degree-one versus degree-three example.

### M2. Update the stage-status descriptions consistently

Locations: `process/coverage.md`, lines 94 and 107–110; `README.md`, opening paragraph, lines 3–6.

The coverage heading correctly says stage 3 is accepted, but its following status paragraph still says that draft awaits five independent reviewers. The README describes the draft through accepted stage 3 without identifying the now-included stage 4 author draft and two new appendices. The main file actually includes stage 4.

Remedy: replace the stale stage 3 pending-review sentence with its accepted status, and identify stage 4 as present and awaiting its review gate in the README opening. This concerns the development record, not a missing theorem or an objection to later-stage work.

## Detailed check of the new sharp modulus

Locations below refer to `appendices/c-quantitative-bounds.tex`.

**Changing affine right-hand sides, lines 189–204.** For two responses with the same actual active resource rows and lower/interior/upper box pattern, the difference `e` satisfies the complete active-row difference system. The minimum-norm row-space correction `d` obtained from an independent scaled basis therefore has the same active-row action. Dependent active rows are consistent because `e` itself solves them. The integer Gram/cofactor bound yields the stated infinity-norm estimate for `d`; box right-hand-side differences are zero. The correction need not be a feasible step, and the proof does not assume it is.

**KKT tangent cancellation, lines 206–224.** Both full optimal gradients belong to the common active-row span. Their difference is orthogonal to `e-d`. Separating the gradient change caused by the leader from the change in response gives the displayed bound

`2 mu ||e||^(P+1) <= N(A_z||e||+A_x Delta)D_b Delta + N A_x Delta ||e||`.

When `||e|| >= D_b Delta` and `||e||>0`, the term containing `Delta^2` is bounded by the additional `A_x Delta ||e||` term, and division gives exponent `1/P`. The zero-distance and smaller-distance cases are also covered. Replacing a positive constant's `P`th root by its maximum with one gives the stated rational `C_0`; `Delta<=1` follows from the leader cube. I independently tested the nonzero tangent correction for a quartic follower with a moving equality, including opposite redundant resource rows.

**Pattern description and lift, lines 226–249.** The actual pattern has three possibilities per box coordinate and two per resource row. The fixed-pattern graph can use at most `3N+4k+2` conditions: box status and gradient conditions, resource status, multiplier bounds, inactive multipliers, and segment bounds. Its gradient degree is at most `max{P,deg phi,2}` because `U,C` are constant and the endpoint segment is affine. The graph need not be expanded or constructed by the algorithm. The weak and strict lifts are exact existential equivalences. Adding at most one variable per inequality stays below `8(N+k+1)` variables; summing squared lifted equations has degree at most `2(d+2)`.

The reciprocal-square variables for strict inequalities can be unbounded near a boundary. This does not invalidate the cited bound. I checked [Milnor's original Theorem 2](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Milnor1.pdf), printed page 275, and the passage to the noncompact limit on printed page 278 against page images. The theorem covers real affine varieties, not merely compact smooth hypersurfaces. Its Betti bound gives the needed connected-component bound. Continuous projection cannot increase the number of connected components; properness of that projection is unnecessary for this claim.

**Segmentation, bit length, and sharpness, lines 251–272.** A finite union of interval/point components in the segment parameter has at most twice as many endpoints. Between successive endpoints a pattern present anywhere in that open interval is present throughout it. The same-pattern bound applies within that interval, and the previously proved continuity permits passage to its endpoints even if their active patterns differ. Summing over at most `2 Gamma+1` intervals yields the stated, deliberately coarse global constant. Its logarithm is polynomial because `log Gamma=O(N+k+(N+k)log(d+2))`. Computing the integer bound does not require constructing the potentially large pattern graphs. The example `z(x)=x^(1/P)` excludes every larger uniform Hölder exponent at zero.

**Anchor consequence, section 4 lines 722–746.** Convex interpolation toward the supplied strict anchor produces margin `t` and moves the leader at most `t/sigma`. Applying the sharp response modulus and the separate upper Lipschitz bounds gives the asserted tightening exponent `nu=P` and coefficient. Convexity of reduced constraints and the anchor margin remain explicit promises. The proof does not infer them from follower convexity or attempt an exact radical comparison to verify the anchor.

## Other mathematical and coverage findings

| Material | Review finding |
| --- | --- |
| Appendix B, lines 13–39 | The interpolation bound is valid for signed strictly increasing marginals, including flat derivative points. Clipping preserves the inverse-displacement implication. |
| Appendix B, lines 54–139 | The critical-value computation includes real parts of nonreal critical values. Padding, merged bad intervals, and geometric panels have the asserted precision/count bounds. The proper polynomial covering argument gives a holomorphic branch on the full disk and identifies it with the real inverse. |
| Appendix B, lines 141–196 | Rational response centers make the Taylor coefficients rational. The recurrence, denominator exponents, Cauchy tail, and intermediate convolution bounds give polynomial bit cost without enumerating compositions. Closed adjoining branches may disagree while both retain the error guarantee. |
| Appendix B, lines 199–257 | The positive-coefficient relative-disk estimate, Rouché comparison, dyadic panel count, and degree bound are justified. Positivity is confined to this specialization. |
| Appendix C, lines 9–99 | Orthant support tests and extreme-ray enumeration give the exact resource projection, including rank-deficient and zero-row cases. Integer Gram bounds give both bounded KKT multipliers and Hoffman repair without Slater assumptions. The repair proof includes the nonpositive box violations. |
| Appendix C, lines 101–175 | The signed Bregman bound follows from the inverse increment estimate in either displacement direction. The stronger positive-coefficient bound and both original `1/(P+1)` response moduli are justified. |
| Section 4, lines 86–186 | Barycentric rounding preserves rational-polytope membership, including lower-dimensional sets. The diagonal optimization ledger and explicit dyadic power construction give their stated margins. The two-power sparse-binary example proves a rational output-length obstruction. |
| Section 4, lines 188–271 | Signed/zero resource weights, endpoint multiplier bounds, equality feasibility, and the no-cancellation balance identity are correct. The `7 epsilon/32` leader and `5 epsilon/32` value ledgers cover recovery without exact auxiliary balance. |
| Section 4, lines 276–376 | Frozen-gradient comparison, feasibility repair, complementarity, and the convex aggregate mismatch yield the stated response certificate. Exact certificates have bounded multipliers. The stronger aggregate-only `1/P` mismatch bound is justified by retaining the response distance. |
| Section 4, lines 378–516 | Realizable sign patterns give a polynomial branch-vector list. Closed validity sets preserve every inverse error guarantee even when they enlarge nonlinear sign sets. Recovery stays in the base polytope and compares true clipped responses across possible branch changes. The transferred `4/5/4` residual ledger uses the necessary absolute bound on inactive negative slack. The separate resource-only `3/3` ledger is consistent. |
| Section 4, lines 518–584 | Apart from M1's degree wording, polynomial upper substitution and enlarged-box Lipschitz bounds preserve polynomial complexity and the true-response objective guarantee. Exact algebraic candidate comparisons do not combine all true response radicals. Empty-follower-dimension handling correctly remains polynomial optimization for nonlinear upper objectives. |
| Section 4, lines 594–789 | Outer, inner, posterior, and supplied-modulus guarantees have the right distinct meanings. Positive tightening is not silently imposed on exact upper equalities. Reserve controls are actual independent model controls with uniform headroom. The polynomial-upper and convex-aggregate extensions retain all feasibility qualifications. |
| Section 4, lines 791–838 | The disconnected tightening example, irrational-only feasible leaders, and exact square-root-sum comparison illustrate the claimed limits correctly. They do not contradict efficient approximation of the convex follower. |

The five canonical accuracy families and both inverse dependencies are substantively covered. The signed-marginal transfers, nonlinear-aggregate recovery addendum, arbitrary polynomial upper data, original modulus, and reserve/anchor qualifications all appear as proofs or explicit special cases. The main theorem combines the related accuracy families coherently rather than requiring duplicate theorem statements for every narrower source. Later exact-hardness boundaries and implementation experiments remain assigned to later stages and are not stage 4 omissions.

## Verification and limitations

The isolated build succeeds and produces a 45-page PDF. The final TeX log contains no warnings, undefined references, multiply defined labels, or overfull/underfull boxes. The shell search for warning strings returns no matches; its exit status does not indicate a failed build. Build logs and extracted text are retained in the reviewer directory.

I wrote and ran `check_review04.py` without importing author or historical reviewer code. Its JSON output records 624 exact signed/positive increment and Bregman checks; 21 moving-right-hand-side tangent cancellation cases; the explicit substitution-degree counterexample; strict-inequality lift and variable-count checks; a monotone cubic with nonreal critical values whose real part is `1/2`; seven exact Taylor coefficients with denominator and composition checks; and 20 sharpness identities. The Milnor PDF and checked page images are retained separately.

These finite checks supplement the proof audit. They do not implement general QE, certify asymptotic complexity experimentally, or establish publication priority for the sharp modulus. I did not rerun every historical diagnostic, read all newly cited publications in full, or visually inspect every compiled manuscript page. The report's acceptance recommendation remains subject to the two minor corrections and root's assessment with the other independent reviews.
