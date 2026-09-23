# Stage 4, round 1 — reviewer 07

Major findings: 0
Minor findings: 0

I found no concrete mathematical defect requiring correction in the frozen stage. This is a bounded review, not a guarantee of correctness, novelty or journal acceptance. My primary lens was the oracle graph formulation: the two spanners, positive scalarizations, explicit primal band, effective-coordinate rounding and affine restoration.

I read all 1,297 lines of `sections/04-vector.tex`, all of the abstract, introduction and conclusion, the task, lenses, process and review protocol, the bibliography and complete coverage inventory. I independently reconstructed the manuscript's proofs. I checked the current stage 1 definitions, parity and finite-disjunction lemmas; the stage 2 rational log-determinant allocation lemma and its repair; and the stage 3 scalar chord/packing lemma, indexed compiler, hybrid construction/count and Jensen superadditivity. Earlier stages had also been reviewed by me in their own rounds. This round is a full stage 4 review, not a new complete review of every proof in stages 1–3.

**Findings.** No MAJOR, MINOR or QUESTION findings identified. In particular, I found no missing hypothesis or incorrect error bound in `thm:vector-oracle-rank` or its separable extension.

**Detailed primary-lens checks.** At lines 340–358 the chord-subtracted image is the appropriate nonlinear subspace. The rational left inverse gives valid effective coordinates, and both displayed radii follow from elementary matrix-norm bounds. An exterior pulled-back separator cannot have zero normal because it would then contradict feasibility of zero. The effective body is symmetric but need not be unconditional; the proof does not assume otherwise.

At lines 376–486 I checked the rational spanner interface needed by the graph theorem. A lower bound on the seed determinant and bounds on feasible image entries give uniform cofactor bounds for all determinant-increasing bases. The objective norm bound is conservative and sufficient. Weak optimization followed by one fixed grid and one fixed central-ball repair gives exactly feasible vectors with additive objective loss at most one quarter. The repaired coordinates have common polynomial-bit denominators independent of exchange history. A returned coefficient exceeding two doubles the determinant; stopping implies the stated coefficient bound `9/4`, safely weakened to three. The positive-polar oracle returns either a valid separator or a certified nearby feasible point; it is never used as exact membership. Its inner ball, outer ball and independent feasible image seeds are explicit. Padding dimension one preserves the imported weak-optimization conclusion.

At lines 512–528, unconditionality permits restriction of polar duality to nonnegative directions when the chord-gap vector is nonnegative. Feasible nonnegative scalarization weights preserve convexity. Signed representation coefficients are harmless because the selected scalar gaps are nonnegative. Their sum cannot be affine at positive image rank: otherwise the independent projected scalarizations would annihilate the whole nonlinear image.

At lines 530–553, the second spanner provides both `B B_1 ⊂ C` and `C ⊂ B[-d,d]^r`. Therefore `P ⊂ K∩S ⊂ drP`. The finite proof uses exact bases with coefficient bounds one and refines from gap `2r` to `1/(2r)`, producing `8r²−1` cells. The symmetric `P/2` band both contains the graph and admits error in `P`. Only midpoint Jensen vectors are taken from the comparison lift, and these lie in `S`; no restriction on all errors of that lift is silently imposed.

At lines 555–576, the rational choices `c=d=3` and `tau=1/(36r)` give vector chord error in `13P/64`. Rounding each effective coordinate within `1/(16r L_B)` gives error in `P_0/16`, hence ambient error in `P/16`. Restoring `a+bx` exactly yields center error in `17P/64`. The explicit continuous band `w−y=VBu/(2r)`, `|u_i|≤1`, contains the exact graph and admits only `49P/64 ⊂ K`. Effective coordinates themselves need not be convex, and their rounding need not have a prescribed sign. Neither fact is used in the proof. The common index and interpolation weight preserve the original input. The cell-count factor `486·144=69984<2^17` gives the asserted count, including rank one. The affine rank-zero case is separate.

The same reasoning at lines 704–732 correctly uses one image and the same two spanners across every separable input block. Dividing coordinate-rounding tolerance by the number of active inputs before summation preserves the band guarantee. The product-packing comparison concerns the original vector lift, not independent scalar optima.

**Full-stage proof coverage.** I checked the following additional arguments and their boundary cases:

- Arbitrary-factor level cuts, plateau cases, interval-cover trimming, finite component/facet overlays and half-body bands. The common-grid order-statistic evaluator retains multiplicities and locates a containing source cell. Canonical fixed-depth mass bisection is ordered in the target even without monotone approximate values at distinct nodes. Reflected indices, fixed denominators, repeated endpoints and invalid codes are accounted for.
- Maximum-determinant original-output bases and rational factor-two determinant exchange; signed coefficients; box/facet rank counts; and the affine conclusion for rank-zero compact nonnegative-facet bodies. The weighted-l1 specialization correctly has one facet scalarization.
- Direct maximum-product allocation and its approximate supporting bound. Expansion at `(1−1/m)b+v/m` gives the factor seven, with `m=1` handled separately. The accepted allocation oracle returns an exactly feasible rational inscribed box, and the final model has explicit bands.
- The shared concatenated basis and all six separable finite/compiled comparisons. Jensen superadditivity gives the index-distance lower bound, and greedy deletion of the integer l1 ball gives the stated product-packing denominator. Local capacities `12P_i` and `5832P_i` include one-cell cases. The six count constants and the corresponding box, facet and effective-image error budgets are consistent.
- Separated positive-power layers, the signed-scalarization range construction, midpoint compatibility, oriented thirds violation, distinct residues and full binary-section lower bounds. The cap-set reduction also checks triples, and the direct three-witness argument checks repeated convexification inside an integer section. These results do not establish a growing binary/general-integer gap for this one-input family.
- Exact convex product counts. The three rational boxes contain their graph portions; the entire middle integer section has weights `(t,1−2t,t)` and remains valid. Oriented thirds combinations separate all ternary product contacts. The general-integer upper has linear size; the binary upper asserted here is finite and may have exponential continuous size. The hinge precursor and Bernstein stability mechanism survive as distinct arguments.
- The rational Bernstein triangular-wave family, the two-integer upper, peak/trough binary lower, degree/encoding bounds and convexity-piece comparison. The arbitrary polynomial overlay retains convex/concave/bracket metadata and uses directed rounding with the correct signs; all three band cases contain the exact graph and satisfy their stated error bound.
- The tilted-body construction, scalar projection lower bound and radius ratio forced by the second difference. The infinity/Euclidean conditioning bounds, simplex improvement and unconditional normalization have the stated finite scope. The nonsymmetric extension only uses the central inner ball and midpoint outer bound.
- Strict violation sets, their lattice-free integer projections, and the limits of union, Helly, Radon and product arguments. The one-input convex box question remains explicitly unresolved.

The abstract, introduction, result table and conclusion are consistent with those scopes and with the earlier accepted results. They distinguish numerical degree from binary exponent length, finite existence from polynomial rational construction, and integer count from encoding and optimization time. The synthesis does not present the growing-input convex product gap, the nonconvex family or the tilted-body family as a solution to the one-input convex box question.

**Canonical and supporting-source comparison.** I inspected the original texts for all ten canonical stage 4 results and all eleven explicitly substantive stage 4 supporting developments in `coverage.md`, comparing their statements, construction mechanisms and relevant proof passages with the manuscript. The oracle-curvature canonical result and rational-polar-spanner support were read in full and received the deepest source-level reconstruction. The finite separable, conditioning, tilted-body, hinge/lattice and three-witness supports were also checked directly. For other sources the comparison was targeted to statements and substantive mechanisms, not a new line-by-line audit of every historical proof or review note. The promoted nonconvex pointer adds no separate theorem. The alternative numerical constants in the earlier degree-32 investigation are superseded without losing a distinct mechanism. All ten canonical and eleven supporting developments have substantive manuscript locations; I found no omission.

For consequential classical imports I directly read the cached GLS 1981 Definition (5), Definition (6), body convention and Theorem (3.1). Its weak objective guarantee compares against every point of the exact body, as used here. I also read Ellenberg–Gijswijt Theorem 4 and its monomial-count specialization, and Averkov–Weismantel Theorem 1.1, equation (3). Their hypotheses and uses match the text. Root's source audit was consulted after the manuscript reconstruction as a source guide, not accepted as proof. I did not independently repeat every predecessor-priority search or re-read every cited paper; the barycentric-spanner, Bernstein, scalarization and explicit formulation steps used here were checked through their manuscript proofs.

**Executed checks and limitations.** I inspected and ran these existing exact checkers:

- `check_oracle_curvature_rank_bands.py`: 289 inner-parallelotope checks, 576 vector-chord comparisons and 9,216 band-error checks passed.
- `check_oracle_curvature_rank_mixed_coordinates.py`: 70 positive-polar representations and 9,216 signed effective-coordinate rounding/band checks passed.
- `check_rational_polar_spanner_second.py`: 16 generic systems, 93 exact repaired calls, 11 determinant exchanges, 120 full-image vertex bounds and 347 positive-polar cases passed.

An independent inline exact-integer/rational calculation checked 133 lattice-ball bounds for `1≤n≤7`, `1≤q≤19`, using the explicit count `sum_j 2^j binom(n,j) binom(qn,j)`, plus the two band-fraction identities and six count constants. All passed. These finite checks do not implement GLS or the complete graph compiler and do not prove the asymptotic claims. I did not run an MILP/SOCP solver, a shared LaTeX build or a fresh PDF layout review. No manuscript, bibliography, coverage, original research or other review report was edited.

**Frozen-file hashes.** All eleven SHA-256 values were checked against `reviews/stage4-round1/snapshot.json`; the final verification immediately before completing this report also matched.

| File relative to `paper-integer-dimension` | SHA-256 |
| --- | --- |
| `abstract.tex` | `db2b95f525fdfc786c9c24b46f41693892131a8103f249d27dbc012d53e323a3` |
| `coverage.md` | `d8b2ed835cfcdfac31b48197cd7a4da7c0e9bac0f73b2dfab6a3571d34a8e1cf` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `026577c84ea4f9c0ff19361708694be45ce88a5a4e911a9b902852f826d1ba9c` |
| `references.bib` | `60fd73a2eec8fd2bc999cf2c407c6a571c590b087786c78647cc1bb7a59a1693` |
| `sections/00-introduction.tex` | `6940bf7c1017d82a8ea00af76575aa88da76f2ef26290b4b3872fd0bba152b16` |
| `sections/01-foundations.tex` | `3108dc02b31b4812fe7fffb444e637a2c846e00268d750262e363dfdb1ded37e` |
| `sections/02-quadratic-finite.tex` | `0a81bba6f3635323663fb347f74face34c2aadb2ba0993b8a1d6465e9f8fdbd3` |
| `sections/03-scalar-nonlinear.tex` | `8e271531b4c705a1333b49f170b20e987359ed5e7d1b05866030bccb69040803` |
| `sections/04-vector.tex` | `d9369569aa0711c3652dcf28929ea4be5884c534f18e371038fbdfc7edb6252d` |
| `sections/05-conclusion.tex` | `2bfb1f16aaa317e5b49dd171ccd9648c7a320343f23ec13acbf6a38b1955ad6e` |
