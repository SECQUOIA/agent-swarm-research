# Stage 2, round 1, independent review 10

**Verdict: PASS.** I found no major or minor defect requiring repair in the assigned frozen Stage 2 text. The universal and cubic arguments survive the counterexample checks described below. This verdict is based on the proofs and certificates, not the author ledger or prior audit verdicts.

## Coverage

I read the following files in `process/snapshots/stage02-round01/` in full:

- `sections/02-universal-positive.tex`;
- `sections/03-cubic-equal-means.tex`;
- `sections/appendix-positive-couplings.tex`;
- `sections/appendix-cubic-certificates.tex`;
- `sections/01-foundations.tex`;
- `main.tex`, `macros.tex`, and `references.bib`.

I read `process/review-protocol.md`, both Stage 2 assignments, `process/stage-02-author.md`, and the Stage 2 scope rows and dependency instructions in `process/scope-proposal.md`. The ledger matches the frozen claims, including the finite refinements and both older universal coupling proofs. The preliminary introduction/abstract are explicitly reserved for Stage 6 integration, so their current emphasis on Stage 1 is not a missing Stage 2 theorem.

I read all ten canonical Stage 2 result files under the repository's `results/`: `positive-multilinear-gap.md`, `positive-multilinear-degree-upper-bound.md`, `positive-multilinear-sharp-degree-growth.md`, `positive-multilinear-second-order-upper.md`, `positive-multilinear-coefficient-removal.md`, `positive-multilinear-equal-marginals.md`, `positive-cubic-gap.md`, `positive-cubic-analytic-family.md`, `positive-cubic-two-level-family.md`, and `positive-cubic-rounding-upper-bound.md`.

I also inspected their historical correction records: the two positive-multilinear lower reviews; both logarithmic-upper reviews; the first, second, and root sharp-upper reviews; `review-multilinear-second-order.md`; `review-multilinear-coefficient-removal.md`; and the cubic, analytic-cubic, two-level, cubic-31-over-12, and equal-marginal reviews. These are historical source corrections, not current-round reports. In particular, the manuscript correctly separates sparse and dense hull values, preserves the positive-expansion inequality direction, uses the strongest analytic slack, retains the alternate two-level family, and limits the mixture optimality claims.

The Stage 1 signing appendix is accepted background and has no new Stage 2 dependency; I did not reopen its exhaustive signing computation or the external Schur-multiplier sources. I did read the complete foundational text and reconstructed every positive-envelope lemma used in Stage 2.

Before primary-source use I read `../literature/AGENTS.md`. I directly checked:

- The local original and extracted Luedtke–Namazifar–Linderoth author manuscript, including a rendered image of printed p.22. Its Conjecture 1 has the positive-coefficient, nonnegative-box, uniform-constant scope used here. The attribution is to that version, without relying on a published-version conjecture number. I also checked its Theorems 4–5 in the extracted text against the common-upper background. [Author manuscript](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).
- Sherali's local extracted text and original PDF, printed pp.252–255. I visually checked equation (13) on p.252 and read the original PDF extraction of Theorem 3 and its proof. The manuscript's binomial slope and intercept agree after renaming the source's degree `m` to `d`. This is a whole-unit-cube result, and the equal-mean formulation is correctly attributed as a consequence. [Original paper](https://math.ac.vn/uploads/files/9701245.pdf).
- Hoeffding's open original PDF, downloaded only to `/tmp`, with direct visual inspection of printed p.16, Theorem 2, equation (2.6). Its independent bounded summands give the stated two-tail sum bound after rescaling the sample mean and applying the result to both signs. The manuscript also supplies a valid independent proof. [Original paper](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).

No copyrighted original was copied into the paper directory. No current-round review was read, and no manuscript was edited.

## Findings

None requiring correction. In particular, I found no missing hypothesis, reversed envelope inequality, invalid marginal law, unsupported finite exactness claim, or omitted required Stage 2 refinement. The following independent derivations record the substantive basis for this conclusion.

## Independent verification

### Universal lower construction and global upper laws

For the dyadic construction, I reconstructed the deficiency identity directly from the vertex objective: `f = sum_j A_j(2^j-N_j)` and `E R=1`, hence `H=max E sum_j A_j N_j`. The count surrogate is an upper relaxation for arbitrary partitions. Selecting upper quantile tails for all anchors is simultaneously feasible because their marginal constraints are separate; it does not impose an additional anchor consistency requirement.

The scalar resource bound has slope `s`: cap the first `l-s` terms and use `r` for the remaining `s`, obtaining `S_l(r)<=s r+2^(l-s+1)-2` for `l>s`. Its expected intercept is `(L-s)/2^s`. The two integer resource profiles have means `B_s` and `B_(s+1)`, so their displayed convex mixture has mean one. Both profiles lie on the same affine face, including `l=s` and cutoff equality. This proves the precise surrogate value, not merely its order.

The attainment step also holds in the original polynomial. Reversal of the first `R` binary indices visits exactly `min(R,2^j)` level-`j` prefixes. XOR shifts preserve all partition hit counts and act transitively on the leaves; conditional on `R`, each leaf fails with probability `R/2^L`. Thus the anchor and leaf marginals are all satisfied together. The counts, degree, strict interiority, and all-integer asymptotic interpolation follow as stated.

For arbitrary partitions, the logarithmic sum estimate uses only the count surrogate. In Jensen's step, any zero-density part of the integral is removed, and `M log(1+B/M)` is increasing; this handles `M=0` by continuity. The dense count LP is exact in both directions because uniform failed subsets realize any feasible count law. Neither argument imports dense numerical values into the sparse model. Homogenization fixes the added coordinates on a face before continuity is used; it retains monomial count but increases occurrence count as acknowledged.

For harmonic rounding, splitting the integral at `p` proves exactly `integral q_p=p`, including saturation at `h_p=1`. The zero-failure convention avoids the logarithm at zero, and the global low/high classification handles ties at one-half. In the hard-term integration range `p_max<=t<=t_e`, an inactive coordinate contributes less than `t/M`; hence active mass is at least `t_e-eta*t`. Dividing by `Lambda*t` and using conditional independence proves the complete curve `J(z)`. All laws are defined on the whole marginal vector before examining a term.

I reconstructed the scalar mixture by differentiating `J`: `J'=-F`, with `F` strictly decreasing. The tangent at its unique crossing with `z` gives `J(z)+F(zeta)z >= (1+F(zeta))zeta`. The crossing proves only the stated optimum for these two scalar curves. Adding independence with inverse-guarantee weights is valid because all omitted deficiencies are nonnegative. The resulting coupling works for every support at once.

The finite Lambert calculation has the correct quadratic-integral sign: `integral_z^1(1/v-eta)^2 = 1/z-1+2 eta log z+eta^2(1-z)<=1/z`. For `A=w-1/(2w)`, the remaining expression is `log(1-1/(2w^2))+1/(4Aw^2)<=0` when `w>=1`. Thus the denominator is positive under the explicit hypothesis. With tuned cutoff, `Lambda=N+log N`, `eta=1/N`, and multiplication by `N/Lambda` changes the denominator by `o(1)`. The fixed-cutoff appendix correctly retains the constant `-1`; its integrated cubic remainder is at most `1/(12 alpha^2)`, yielding the reciprocal correction without making a second-order lower claim.

I separately checked the older dyadic-scale proof. Its largest-power selection is available even when `d-1` is not a power of two. The tail lemma follows from a prefix whose cumulative `N`-mass first reaches `u`, with `sN(s)` bounded by that mass. The original three-law harmonic finite bound and the earlier leading-constant mixture retain their own complete proofs: in the latter, `b>=6` makes `b-3 log b>0`, and only the lower exponent, not the actual conditional intensity, is required to be small.

Nonnegative-box transfer uses `T_original<=T_expanded` and equality of the full hull gap. It preserves degree and dimension, but does not preserve original factor structure; the manuscript uses the transfer only where those invariances suffice.

### Cloning, finite existence, and endpoint perturbations

The clone law sends every binary clone expectation to an original feasible expectation through conditional independent rounding of group averages. Setting each clone group equal to one original binary coordinate proves the converse. This is equality of feasible expectation intervals, so both envelopes scale exactly. Distinct original supports and clone labels prevent monomial collisions.

The random retention argument controls all `2^(nm)` vertices and the separate termwise-gap event. Independence between those events is unnecessary for the union bound. Uniform vertex error controls each envelope by `t`, hence `H` by `2t`; `t/m^d` vanishes with the original instance fixed. The prescribed strict inequality on `K^2` makes the exponential union bound vanish. All three restrictions—unit coefficients, degree exactly `d`, interior means—are therefore simultaneous, with unrestricted dimension.

For the finite cubic application, `2t^2/(464m^3)=m^3/23200`, the logarithmic failure bound is negative at `m=1000` even with `log 2<1`, and the error in `T-2H` is `5t`. The remaining normalized margin is exactly `3987/4550>0`. This proves the claimed existence without pretending a retained support has been produced.

### Cubic universal and lower certificates

In the orientation law, opposite orientations exclude nested intervals inside the minimum-mean anchor interval. The expected longest selected interval is `sum_j 2^(-j)a_(j)`. The sorted-sum inequality and the decreasing average of the geometric weights give the general endpoint factor and its cubic `8/3` specialization.

For the three-law mixture, I reconstructed `O` and `B` by interval integration rather than relying on the displayed deficiency formulas. With one low mean the four cases in `(a,b)` exhaust the domain. In the middle case the two needed inequalities are `3a+4b<=7u/2` below `a+b=u`, and `9a+8b>=17u/2` above it. For all-high means, subtracting anchor failure from the integrated failure union gives `a/2+b/4`; independence contributes at least `7t/16`. Quadratic terms are independently covered. The optimality test approaching `u=1/2` must approach from above, as explicitly stated, because `B` changes classification at that boundary. The three upper constraints average with weights `3/31,4/31,24/31` to cancel both free mixture variables and yield `12/31`, with exactly the limited optimality scope asserted.

For the analytic lower family, I solved the two linear stationarity equations for the `(a,b)` quadratic independently. Its Hessian determinant is 248. On `c<=3/10`, the boundary minimizer has zero `b` derivative and nonpositive `a` derivative, making the first-order convexity argument valid on the entire square. On the other region, the unrestricted minimum is a valid lower bound even if the stationary point lies outside the square. Fresh elimination gives precisely the two displayed quartics.

I expanded all five Bernstein rows exactly from those eliminated polynomials. Their common minimum coefficient is `901/120000`. The count identity's negative correction is at most `72/m`; taking an affine expectation at `(1/4,1/2,3/4)` yields `139/6+delta_*-72/m`. The upper and termwise corrections subtract to the stated denominator. The limiting certified lower is exactly `1610000/743033`; the text correctly does not claim convergence of actual ratios to that endpoint or attainment of the affine minorant.

All three finite cubic witnesses have matching affine count minorants and rational count laws. Conditional uniform subsets recover every original singleton marginal, so the count reduction covers arbitrary dependence. The frozen integer/rational checker was replayed and passed all `343+729+274625` inequalities, the primal mean/value checks, and all 289 two-level inequalities. Its output reproduces every table value. This is exact finite verification; the count-to-vertex and primal/dual arguments explain why it certifies the full envelope.

For the 25-variable variant the padding loss is at most `1840/1000`, with no assumption of independence from the old variables. For the explicit 52-variable polynomial, the loss is at most `120*(20/1000)=12/5`; its 4,320 supports are distinct cubic supports of coefficient one, and all lower term envelopes remain zero. These establish the claimed bounds without implying new exact hull values.

Both two-level identities were independently expanded. Their equality atoms have the asserted means and affine expectations. Conditional independent Bernoulli sampling of coordinates from the atoms multiplies the scalar expectation by `1-1/m`. This supplies the other inequality on the actual finite hull gap, proving actual-ratio convergence to `243/115` and, for the alternate family, `33/16`. The finite `m=20`, exact `m=16`, and alternate `m=50` certificates are all retained and correct.

### Equal means and independent check artifacts

The adjacent-count uniform-subset law is a single global law for every degree. Convexity of the interpolated binomial count sequence proves its optimality for each `E_d`. Comparing with independence gives `q<=u^d<u`, so all denominators are positive. Fixed-degree convergence gives the dimension-free supremum and the limit of the finite maxima; no exchange of an uncontrolled growing-degree limit is needed because the maximizing integer lies at a floor/ceiling neighbor of `u/(1-u)`. Bernoulli's inequality then gives two, with the complete graph showing sharpness.

Independent checker: `verification/reviewer10/stage02-round01/check_independent.py`. Results: `verification/reviewer10/stage02-round01/independent-results.json`.

- Exact rational integration of the actual `O` and `B` laws on 1,122 quadratic/cubic tuples with coordinates in `{0,1/16,...,1}`, plus singleton marginal checks. The minimum observed normalized mixture deficiency is exactly `12/31`.
- Exact dyadic resource inequalities for every integer count, every valid cutoff including ties, and simultaneous reversed-prefix counts for `L=2,...,9`.
- Exact symbolic elimination and all five Bernstein identities; both two-level identities and equality atoms.
- Exact positivity and strict factor-two checks for 5,244 equal-mean `(n,u,d)` instances.
- 120 floating quadrature checks of the actual harmonic conditional product law, including `d=2`, cutoff factors `1,1.25,5,30`, zero failure means, small failure scales, and saturated cutoffs. The corresponding scalar fixed points and applicable Lambert certificates were also checked numerically.

The checker and the frozen finite checker both completed successfully. Rational and symbolic checks are exact for their stated finite identities and cases. The harmonic computations are numerical sanity checks, not uniform or rigorous quadrature certificates. None of the finite searches substitutes for the preceding universal arguments.

## Remaining limits

This review does not establish literature priority or exclude all earlier sources. The three primary sources used for Stage 2 attribution were accessible; no central source was treated as inspected solely through a secondary citation. I did not conduct a new novelty search, revalidate unrelated Stage 1 external inputs, or rebuild and visually audit every page of the manuscript PDF.

Exact `R_3`, optimal finite-degree constants, a matching second-order lower asymptotic, small deterministic coefficient-removal constructions, and global optimality outside the specified coupling families remain open within this stage. The manuscript preserves those limits and makes no unsupported spatial-certificate consequence from these positive gap examples.
