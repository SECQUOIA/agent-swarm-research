# Positive cubic gap investigation

Date: 2026-09-04. Follow-up to the sharp asymptotic multilinear result.

The later [focused cubic paper and Lean package](../paper-cubic-gap/README.md) certifies 1610000/743033≤R(3)≤31/12. Its [coverage map](../formal/topics/11-cubic-completion/COVERAGE.md) distinguishes these completed proofs from the exploratory searches and separate written results recorded below.

## Outcome so far

The hypothesis R(3)=2 is false. `results/positive-cubic-gap.md` gives an exact 24-variable certificate with ratio 6601/3225>2 and an 18-variable certificate with ratio 20891/10411>2. Both use strictly positive integer coefficients on their monomials and coordinate values 1/4,1/2,3/4. A padding argument gives a purely cubic 25-variable example at a strictly interior point with certified ratio at least 165025/80947>2.

The root agent supplied a common left/right endpoint-orientation coupling giving R(3)≤8/3. Its more general degree-d bound is (d−1)/(1−2^{-(d−1)}). This is asymptotically weaker than the sharp harmonic result, but useful at small degree. The exact R(3) and exact finite-dimensional cubic worst ratios remain open.

## Search methodology

`cubic_coefficient_search.py` restricts the universal coupling LP to all monomials of degrees two and three. At fixed marginals, finite minimax duality optimizes over all nonnegative monomial coefficients simultaneously. Samples through dimension12 gave ratios below two, but the strongest profiles repeatedly used three coordinate values near (u,1/2,1−u), with u near1/4. This suggested a grouped symmetry reduction rather than a larger exponential-state search.

`cubic_symmetric_search.py` divides the variables into three groups of equal size m and prescribes groupwise constant marginals. Permuting coordinates within groups preserves all constraints. A symmetrized coupling is described exactly by its success counts (A,B,C)∈{0,...,m}³. Given these counts, the conditional expectation of a monomial selecting k_i distinct coordinates from group i is

\[
\prod_i\frac{\binom{A_i}{k_i}}{\binom m{k_i}}.
\]

There are only six degree-two orbit types and ten degree-three orbit types. The coefficient-optimization LP therefore has (m+1)³ count states and16 monomial constraints, instead of2^{3m} binary states. Its dual gives a positive polynomial whose coefficient is constant within each orbit. The reduction is exact for finite m; it is not a continuous moment approximation.

At group marginals (1/4,1/2,3/4), the numerical optimized ratios were approximately:

| Group size m | Variables | Best orbit-symmetric ratio found |
|---:|---:|---:|
| 4 | 12 | 1.93394 |
| 5 | 15 | 1.97938 |
| 6 | 18 | 2.01182 |
| 8 | 24 | 2.04935 |
| 16 | 48 | 2.11250 |
| 32 | 96 | 2.14436 |
| 64 | 192 | 2.16060 |

These floating-point values guide discovery; the main result uses simpler integer coefficients and exact certificates. The optimizer consistently uses only six orbit types: high³, middle·high², middle², low·high, low·middle, and low².

`cubic_integer_certificate.py` searched small integer coefficients near this pattern, solved the count-state envelope LP, reconstructed a rational dual affine minorant, and checked it exactly on every count state. The 24-variable example has coefficients (2,3,13,12,8,7) in the listed orbit order. The 18-variable example has coefficients (2,3,9,10,7,7).

`verify_cubic_bounds.py` is the final certificate replay. It uses only Python integers, rational arithmetic, and exhaustive count states; it invokes no numerical solver. It checks all dual inequalities, all probabilities and count means, primal–dual equality, and the resulting gaps. Its output is preserved in `verify_cubic_bounds.log`.

## Failed universal factor-two coupling

A natural candidate puts each coordinate's minority event in the common interval [0,2p_i], with conditional probability1/2, independently given the common uniform threshold. This gives exactly half of each bilinear term's gap. It also gives at least half for cubic terms with two or three low coordinates. It fails on three high coordinates: when all three failure marginals equal p≤1/3, their union has probability7p/4, giving hull deficiency3p/4, whereas the term-by-term gap is2p. The ratio for this particular coupling is8/3. This disproves only that proposed coupling, not a factor-two theorem; the grouped exact examples then independently disprove the theorem itself.

A single low anchor with a bilinear star on high leaves plus all high-leaf triples appears unable to exceed two in the rare-event exchangeable limit. A third marginal level at1/2 and interactions among its variables supply the additional conflict in the successful construction. This last structural observation is a research heuristic, not a proved characterization.

## Next directions

- Determine the exact value of R(3), or improve the audited upper bound 31/12.
- Refine the analytic three-group lower bound now certified in `results/positive-cubic-analytic-family.md`, or determine its exact limit.
- Characterize whether the six active orbit types are sufficient for the unrestricted cubic worst case. The current evidence establishes no such reduction.
- Reduce the number of variables or coefficient sizes while retaining a comfortable certified margin above two. Degree three is minimal by the known bilinear upper bound, but no minimum-dimension claim is made.
- Check specialized multilinear-polytope and probabilistic Fréchet literature for earlier degree-three examples or the endpoint-orientation upper bound before assigning novelty to either.

## Numerical certificate safeguard

A follow-up at 192 variables exposed a limitation of rationalizing floating-point dual multipliers directly: the resulting rational vector could be feasible but fail exact primal–dual equality. The certificate routine now solves the numerically active affine equations in exact rational arithmetic and then checks every count-state inequality and exact objective equality. Failed reconstruction is not evidence for a result. The smaller documented certificates also have separate pure-integer/rational replay code.

## Analytic family completed

The family in `results/positive-cubic-analytic-family.md` proves R(3)≥1610000/743033 by an affine minorant valid on the full normalized count cube [0,1]³. Convex elimination of two coordinates reduces the proof to quartic nonnegativity; five exact positive Bernstein expansions certify it with slack 901/120000. The finite multilinear family has positive integer coefficients whenever its group size is a positive multiple of nine. The refined lower certificates converge to 4830000/2229099=1610000/743033; convergence of the actual ratios is not asserted. Omitting the positive slack gives the simpler bound 483/223. Independent audit `notes/review-positive-cubic-analytic-family.md` passed, and the [completed Lean proof](../formal/Formal/CubicGap/AnalyticResults.lean) establishes the refined bound for the actual all-box supremum.

## Improved cubic upper bound and search limits

The three-distribution mixture in `results/positive-cubic-rounding-upper-bound.md` proves R(3)≤31/12. Its endpoint-orientation, independent, and low/high B=2 weights are 18/31, 6/31, and 7/31. A complete case analysis proves the global termwise guarantee. Three limiting marginal configurations show that 12/31 is the best possible uniform termwise fraction within this fixed mixture family. This optimality statement does not preclude a coefficient-aware analysis of those distributions.

A finite-grid LP over additional split thresholds and conditional-failure scales numerically reaches a ratio around 2.363. A four-component subset, adding split threshold 2/3 and scale 3, reaches about 2.546 on a boundary-enriched grid. Neither is a proved continuous bound. Earlier coarse grids overstated the quality of the three-component mixture because they missed limiting marginals at zero and immediately above the low/high split. Exact limiting examples exposed this artifact and led to the certified 31/12 bound. The exploratory script and logs retain these distinctions explicitly.

## Two marginal levels suffice

A separate search restricted all marginal values to at least 1/2 and found ratios above two with only two distinct marginal values. This led to the particularly simple family in `results/positive-cubic-two-level-family.md`: f_m=A E₂(W)+(5m/4)E₂(U), with marginals 1/2 and 3/4 and m divisible by four. Its actual ratios converge to 243/115, and a 40-variable member already has a certified lower bound above two. All individual termwise convex envelopes vanish at the evaluation point. A square-factor identity proves the global affine minorant, avoiding exhaustive enumeration.

The first parameter choice used marginals (1/2,4/5) and F(a,c)=ac²+(24/25)a². Its affine minorant was (41/25)a+(4/5)c−68/75, with residual (24/25)[a−(41−25c²)/48]²+(1−c)(5c−3)²(5c+11)/480. Equality atoms (1/3,1),(2/3,3/5) with equal weights give the matching scalar convex value 83/150. The finite family A E₂(W)+(24m/25)E₂(U) has ratios between (33/16)(1−1/m) and 33/16. This valid predecessor is retained here; the 243/115 choice is simpler and stronger.

Optimizing the same two-atom scalar family numerically suggests a ratio about 2.1137545 at marginals (1/2,3/4), with the interior c-coordinate about 0.64101861. This is only exploratory optimization and is not the asserted exact optimum of the two-level problem. The clean rational choice c=2/3 gives the certified 243/115.

## Equal marginals cannot give a ratio above two

The companion `results/positive-multilinear-equal-marginals.md` establishes the exact finite-dimensional worst ratio using a random subset with cardinality supported on the two integers adjacent to nu. Complete elementary symmetric polynomials attain the bound. The dimension-free value is at most two, sharply, so unequal normalized marginals are necessary; two values suffice by the new family. Sherali1997 already gives the underlying elementary-symmetric convex envelope explicitly (equation13, Theorem3), so the companion is labeled a classical consequence without a new-envelope claim. Its independent audit is complete.
