# Stage 4, round 1 — reviewer 05

Major findings: 0

Minor findings: 0

## Assessment and scope

I found no concrete mathematical defect, material missing hypothesis, or substantive coverage omission in this snapshot. There are no numbered findings requiring repair. This is a bounded independent review, not a guarantee of correctness, novelty, or publication acceptance.

I read all 1,297 lines of `sections/04-vector.tex`, the complete abstract, introduction and conclusion, the bibliography, coverage inventory, task, lenses, process and review protocol. I compared the mathematical content with all ten canonical stage 4 result files and all eleven explicitly substantive stage 4 supporting files listed in `coverage.md`. This includes the earlier hinge/Bernstein stability mechanism, finite separable companion, direct product allocation, conditioning/simplex arguments, repeated-convexification obstruction, and unsuccessful lattice routes. I did not count a promoted pointer or a superseded numerical constant as an additional theorem obligation.

I reread the relevant accepted dependencies: stage 1's graph-sandwich definitions, affine invariance, parity contacts and finite disjunction; stage 2's rational logdet allocation and central repair; and stage 3's indexed compiler, monotone-curvature quantiles, dense hybrid and Jensen superadditivity. I checked the accepted stage 3 changes against the earlier reviewed version. Stage 4's abstract and synthesis agree with these dependencies and with the current vector claims. In particular, the one-input convex box constant-gap question remains open, and the paper distinguishes binary linear lifts from stronger lower bounds valid for arbitrary convex binary lifts.

The primary lens was the generic rational spanner. Existing audits were consulted after independently reconstructing the arguments and were not treated as evidence of correctness.

## Detailed spanner and oracle reconstruction

The argument in `lem:rational-spanner` at line 376 supplies the needed uniform rational implementation.

1. **Initial conditioning.** Feasible image coordinates are bounded by `A`. As long as exchanges increase the determinant, its magnitude remains at least the supplied nonzero seed determinant `Delta_0`. The cofactor bound therefore controls every inverse entry by `U`. For the row-coordinate objective `W B^{-1} e_i`, summing the absolute matrix entries bounds its one-norm by the stated `L`. The bounds depend only on original rational input and seeds, and their encoding length remains polynomial when rank varies. They need not be polynomially bounded in numerical value.

2. **Weak-optimization interface.** GLS Definition (5) compares the rational output's objective with all points of the exact body, while allowing Euclidean distance at most the requested tolerance. This is the convention used in the manuscript. Explicit inner and outer balls and a polynomial rational weak separator supply the hypotheses of Theorem (3.1). Padding a one-dimensional body by `[-1,1]` respects the source's dimension-at-least-two convention; projection preserves both guarantees.

3. **Exact feasibility.** With weak tolerance `d delta`, grid rounding adds at most another `d delta` in Euclidean norm. Thus the rounded point is within `epsilon = 2d delta` of the body. Writing the repaired point as a convex combination of a nearest feasible point and a point in the supplied central ball proves exact membership. This proof does not mistake weak membership for exact membership and does not require an exact support optimizer.

4. **Objective loss.** The rounded point is within `R_0 + 1` of the center. Its loss from weak optimization, rounding, and central repair is bounded by
   `d delta [1 + L + 2L(R_0+1)/sigma] <= 1/4`.
   This covers both signs of every representation-coordinate objective. At termination every exact feasible representation coefficient is consequently at most `2 + 1/4` in magnitude.

5. **Uniform encoding and termination.** The same dyadic grid and the same repair weights are used for every oracle output. Their numerators are uniformly bounded, and their coordinates have one fixed common denominator of polynomial bit length. Including the finitely many seed denominators preserves this property for all possible bases. Each accepted exchange more than doubles the absolute determinant, whose upper bound is `r! A^r`. The stated exchange count is polynomial, and every later inverse and objective has polynomial encoding. This supplies the missing ingredient that a merely per-call polynomial oracle guarantee would not establish by itself.

6. **Positive-polar use.** Central repair of a weak support maximizer over `K` gives an exactly feasible support point with the stated additive loss. A violated resulting support inequality separates the query from the whole positive polar. Otherwise division by `1+tau` certifies genuine proximity to a feasible polar point. Coordinate violations are separately detected. The positive central ball and the seeds `2 a_0 e_j` satisfy their support bounds; independent rows of `V` give independent seed images. This does not assume a strong separator for the polar. The effective primal body has the given rational radii, and an exterior pulled-back separator cannot vanish because zero is feasible.

## Whole-stage proof checks

- **Refinement and common partitions:** The two endpoints of each strict concave-gap level give at most `2H-1` cells, including plateaus and repeated cuts. Finite interval covers can be trimmed by restriction. The deterministic mass-bisection tree orders its output by target even with nonmonotone approximate mass values at different nodes. Reflection reverses local indices. A product of polynomially many endpoint denominators and the largest dyadic denominator gives the common grid needed for exact numerator search. Multiplicity handles duplicates; positive-length merged cells lie in one source cell of every output. All outputs use the same input and interpolation weight.
- **Original-output and facet bases:** Maximum determinant gives coefficient bound one; rational exchanges give bound two. Selecting original convex functions preserves nonnegative basis gaps despite signed representation coefficients. Refinement yields the claimed `4r-1` and `8r-1` finite factors and the compiled constants 12 and 13. Facet rounding adds `K/16` to a `13K/32` chord gap; the half-body band gives containment and admitted error `31K/32`. Compactness and nonnegative weights justify the affine rank-zero case.
- **Direct unconditional allocation:** The exact product maximizer supplies the first-order sum bound `m`. Comparing an `e^{-1}` product approximation with `(1-1/m)b+v/m` gives the safe `7m` sum bound; the separate `m=1` argument is valid. Scaling the stage 2 allocation by `R` loses no feasible positive vector. The final inner box and normalized bands give `15/16` error and the stated compiled count.
- **Effective-image graph bands:** The positive-polar spanner controls nonnegative vector gaps, while the primal spanner gives `P subset K intersect S subset dr P`. These are separate uses with separate constants. The rational choices `c=d=3` and `tau=1/(36r)` put the gap in `13P/64`. Rounding the effective coordinates adds only `P/16`, preserving membership in `S` exactly. Restoring the affine part gives center error `17P/64`, and the explicit `P/2` band admits `49P/64`. The finite and compiled counts follow from the displayed refinement and scalar cell counts; no oracle constraint remains in the MILP.
- **Separable vector results:** One concatenated row basis or one shared effective image applies across every coordinate. Jensen superadditivity and deletion of an integer one-norm ball give the comparison against the original vector lift. The six per-coordinate count factors are bounded by `108r`, `180r`, `180r^2`, `87480r`, `157464r`, and `1277208r^2`, yielding constants 7, 8, 8, 17, 18 and 21. Coordinatewise error and rounding allowances sum within the stated common bands. Inactive coordinates and rank zero need no integers; mixed-coordinate nonlinear terms are explicitly excluded.
- **Positive-power obstructions:** The midpoint estimate is uniformly below `7/8`; each separately normalized signed scalarization has a two-rectangle upper construction. The oriented thirds error exceeds one and gives both modulo-three and binary-section lower bounds. Three zero-sum residues give a cap set, with the stated generating-function minimizer and finite prefactor. The direct three-witness proof handles arbitrary integer labels and then repeated convexification within the middle section. None of these arguments asserts a growing difference between the two minima for this family.
- **Exact convex and nonconvex separations:** I checked the degree-32 constants and all three integer sections, especially the entire mixed section with weights `(t,1-2t,t)`. Product contacts give the exact optimum counts; the binary upper is allowed exponential continuous size. The hinge precursor and its Bernstein thickening retain distinct valid mechanisms. For the nonconvex family, the Bernstein variance estimate gives uniform error, the period/orientation lift contains the graph, and separated peaks require distinct binary assignments. The degree bound and alternating-crossing argument support the logarithmic worst-case order without assuming the exact degree of the expansion.
- **Signed polynomial overlays:** Rational brackets of roots of the second derivative have small chord error on every subinterval. Sign-directed rounding and the three source-cell flags yield valid convex, concave, and bracket bands at merged cells, including repeated endpoints. The flags are computed Boolean wires and require no extra integer declarations. Count summation, fixed denominators and invalid-code exclusion fit the accepted indexed compiler.
- **Conditioning and open boundaries:** The tilted example preserves a narrow scalar difference while permitting a broad common output direction; its condition ratio grows at least as claimed. The box and sharper Euclidean simplex comparisons use the inner body for the final errors and the outer body only for midpoint bounds, so the nonsymmetric extension is justified. Unconditional normalization gives the inner crosspolytope. Strict violation projections are convex and integer-free, but their union need not be convex. The limitations concerning mixed Helly, integral Radon, products and oscillatory substitutions are accurately stated.

## Primary-source checks

I directly inspected GLS Definition (5), Theorem (3.1), and the polar/anti-blocker passages in the cached primary text. I also checked Plevrakis–Hazan Section 3.2, Lyu–Hicks–Huchette Section 3/Proposition 1, Kelly–Maulloo–Tan's proportional-fairness inequality, Ellenberg–Gijswijt Theorem 4, and Averkov–Weismantel Theorem 1.1. Their scope matches the use or predecessor credit here. The manuscript supplies the new graph and rational-interface arguments rather than attributing those conclusions to these imports.

The maximum-determinant and exchange attribution agrees with Section 2.3, Propositions 2.2 and 2.4 of the [Awerbuch–Kleinberg primary author manuscript](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf), which I opened directly. The present proof does not import that paper's initialization-specific oracle-call bound. I did not conduct a new exhaustive novelty search or verify all bibliography metadata independently. Hartman's historical attribution is not a consequential proof dependency: the needed bounded-second-derivative convexification is proved explicitly here.

## Executed checks and limitations

All five checks passed:

| Command under the repository root | Reported checks |
| --- | --- |
| `python code/quadratic_rank/check_rational_polar_spanner_second.py` | 16 generic systems, 93 exact repaired calls, 11 exchanges, 120 full-image vertex checks, 347 positive-polar cases |
| `python code/quadratic_rank/check_implicit_knot_overlay.py` | 2,304 ordered-search checks, 60 order statistics, 180 source-cell containments, 8 large-grid ranks, 99 directed bands |
| `python code/quadratic_rank/check_oracle_curvature_rank_bands.py` | 289 inner-parallelotope checks, 576 exact vector-chord comparisons, 9,216 band errors |
| `python code/quadratic_rank/check_separable_oracle_rank_precision.py` | 96 exact lattice-ball bounds, 1,536 coupled separable rounding/band checks |
| `python code/positive_vector_obstruction/check_box_gap_root.py` | 72 middle-slice vertices, 2,048 exact mixtures, 390 product contact-pair obstructions |

I inspected the spanner checker's scope: it uses a synthetic weak optimizer on rational boxes and tests exact repair, fixed denominators and exchange invariants. It does not implement GLS. These finite exact checks supplement the proofs; they do not implement or verify the complete oracle/quadrature/circuit/MILP pipeline. I did not run a shared LaTeX build, perform a page-by-page PDF review, or reread every historical audit in the dependency index. No manuscript, research or literature files were edited.

## Verified snapshot hashes

Every hash matched `reviews/stage4-round1/snapshot.json`. Paths are relative to `paper-integer-dimension`.

| File | SHA-256 |
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
