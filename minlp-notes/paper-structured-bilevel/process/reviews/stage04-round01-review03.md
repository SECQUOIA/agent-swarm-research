# Stage 4, round 1 — independent review 03

Snapshot: `process/snapshots/stage04-round01`.
Manifest SHA256: `4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`.
The digest and all eleven listed file hashes were independently verified.

**Recommendation: accept after one minor documentation correction. No major mathematical defect found.**

I read the complete accuracy section, inverse appendix, quantitative appendix, and integration/coverage changes, including the new sharp response-modulus proof. I checked the accepted prerequisites where used; I did not read other stage 4 reports or root conclusions, delegate, change manuscript sources, or treat historical PASS records as verification. Later-stage boundaries and experiments are not current omissions.

## Actionable finding

### R03-1 — Minor: reconcile the stage-status prose

**Location:** frozen `process/coverage.md:107–110`, particularly “The draft awaits five independent reviewers,” immediately after the stage 3 location table. Related location: `README.md:4–6`.

**Evidence and reason:** The stage 3 heading at `process/coverage.md:94` says that stage is accepted after review and corrections, while its concluding paragraph still says it awaits reviewers. The README describes accepted stages 1–3 but does not identify the included pending stage 4 in its opening summary. `main.tex` already includes section 4 and appendices B/C, and the coverage inventory explicitly identifies stage 4 as the current pending gate.

**Fix:** Change the stage 3 concluding paragraph to accepted status, preserving the scope of its finite diagnostic logs. Update the README opening to say that the current draft contains accepted stages 1–3 and the stage 4 author draft with its two new appendices. Keep stage 4 explicitly pending review. No mathematical change is needed.

## Inverse approximation audit

**Locations:** `appendices/b-inverse-approximation.tex`, `lem:inverse-modulus`, `thm:inverse-approximation`, and `prop:positive-inverse`.

The interpolation proof gives a uniform increment bound without assuming nonnegative coefficients or strictly positive derivative. Monotonicity bounds all interpolation node values by the increment, and the endpoint comparison gives the displayed factor. Clipping does not invalidate the inverse modulus. Endpoint normalization only scales the target tolerance by the rational endpoint difference.

The critical-value construction includes real parts of all complex critical values, not only real critical values. Its fixed-three-variable description, finite cardinality, exact bracketing, and padding provide the required distance bound on complementary target gaps. The total padded length is smaller than the selected bad-interval tolerance, so constant approximations on merged components have the claimed response error even at interior derivative zeros.

The geometric panel construction has polynomially many rational panels. The rational response center has a rational target center within the required distance of the panel midpoint. The disk stays away from every complex critical value. Properness of the polynomial and local inversion justify a finite covering, and simple connectivity supplies a single inverse branch on the disk. The chosen branch agrees with the increasing real inverse on the relevant real segment. Thus Cauchy estimates are applied to an actual holomorphic inverse, rather than merely to a formal series.

I checked the Taylor recurrence and common-denominator induction. At order `n`, higher powers cannot contain the unknown `c_n`; products of previous coefficients have exactly the stated denominator exponents. Cauchy's magnitude bound together with polynomial denominator lengths controls numerator lengths. Truncated convolution avoids enumerating exponentially many compositions. The coefficient bounds and panel scaling therefore support polynomial bit cost, not merely a count of arithmetic operations.

The positive-coefficient specialization separately proves its stronger relative complex disk by coefficient majorization and Rouché's theorem. Its root bound, panel ratio, truncation degree, and `32 P^2 m` panel count check out. Nonnegativity is not imported into the general signed-marginal theorem. The diagonal power construction likewise has the stated numerical-power and accuracy-bit dependence.

## Projection, multipliers, growth, and response certificates

**Locations:** `appendices/c-quantitative-bounds.tex:9–131`; `sections/04-accuracy.tex`, `subsec:accuracy-one-resource` and `lem:accuracy-certificate`.

The resource projection has the correct lower-support sign. Central sign cones inside the nonnegative orthant are pointed, and their extreme rays are covered by the enumerated independent column/coordinate hyperplanes. Rank deficiency, zero columns, `k=0`, and the single-ray `k=1` case are addressed. This gives exact leader feasibility without approximating follower coordinates.

The integer Gram-matrix bounds are conservative but sufficient. Independent active-row representations exist without a constraint qualification; integer determinants give the denominator lower bound. The multiplier scaling is in the correct direction, and the same representation applied to a Euclidean projection proves the repair estimate. Large negative inactive slack is not treated as a positive violation.

The signed Bregman growth constant follows by integrating the increment lower bound over a half-interval. The nonnegative-coefficient improvement uses a separate monomial argument. The aggregate contributes a nonnegative Bregman term for each feasible leader, since all box images lie in its specified convexity box. No positive curvature lower bound is assumed.

For a single signed equality, all weighted response differences have the same sign as the dual parameter moves. Zero-weight coordinates do not change, so the exact balance-to-response identity and its use with signed upper coefficients are valid. The bounded multiplier interval covers endpoint resources, negative weights, and degenerate equality fibers. The zero-total-weight case correctly becomes a leader equality plus diagonal response problem.

In the general certificate, the frozen-gradient box variational inequality is compared with the actual feasible optimum, and aggregate-gradient mismatch is bounded with the stated row/column sums. Hoffman repair produces a feasible competitor before polynomial growth is used. The residual, complementarity, and aggregate errors yield the displayed `1/(P+1)` response estimate. Retaining the response distance in the mismatch term justifies the separate sharper `1/P` aggregate-only estimate. The proof does not assume the one-resource no-cancellation identity for multiple rows.

## Candidate completeness and rational recovery

**Locations:** `sections/04-accuracy.tex:379–517`, particularly `eq:accuracy-candidate` and `lem:accuracy-recovery`.

The nonlinear branch construction is sound. A common realizable sign condition selects branches in fixed dimension; the selected closed branch-interval validity conditions may enlarge that sign condition, but every added point retains the uniform approximation bounds. This avoids both an exponential Cartesian enumeration and an invalid assertion that weakening arbitrary nonlinear sign inequalities gives the topological closure.

Every true response has a lift with its true aggregate and a bounded multiplier. The polynomial allowances contain those lifts. Conversely, a candidate's true frozen response has the doubled residual allowances claimed in the text. All substitutions remain polynomial-size because the compressed dimension is fixed and numerical degrees are counted.

Rational recovery takes place in the exact base polytope, not in a possibly irrational nonlinear branch set. It compares true clipped inverses across branch boundaries and never evaluates an obsolete branch at the new point. The inverse modulus supplies enough argument precision. The complementarity transfer correctly includes the multiplier-change term multiplied by an absolute residual bound, which is essential for inactive rows with large negative slack. I checked the resulting `4 S eta`, `5 k Lambda S eta`, and `4 A_U eta` allowances and their use in the tolerance choice.

The interface compares `p(v*)` with the true response at the recovered leader, which is exactly what the later upper-polynomial Lipschitz bound uses. The resource-only variant can instead preserve its rational branch cell and budgets polynomial residual changes directly. The one-equality, resource-only, and general upper-objective ledgers all give the stated suboptimality and value-estimate bounds; they do not claim that an approximate follower is exactly resource feasible.

## New sharp leader-response modulus

**Location:** `appendices/c-quantitative-bounds.tex:134–272`, `prop:accuracy-response-modulus`.

I find the new `1/P` proof valid, including the globalization step.

1. For two responses with the same active resource rows and box pattern, an independent active-row basis gives a row-space correction `d` for the right-hand-side difference. The integer cofactor estimate bounds it by `K B_b Delta`. Dependent active rows are consistent because the actual response difference solves the complete active system.
2. Both optimal gradients belong to that common active-row span, so their difference is orthogonal to `e-d`. Adding the two fixed-leader Bregman inequalities and separating the change in the leader yields the displayed bound. When `||e||>=D_b Delta`, the quadratic-in-Delta term is absorbed into the linear response-distance term before division. The remaining case is already Lipschitz. The stated rational `C_0` overestimates the needed root constant and also handles zero `D_b` or zero leader-gradient variation.
3. Along a feasible leader segment, each box/resource pattern has a polynomial KKT description with bounded resource multipliers. The pattern description includes strict inactive slacks and strict interior bounds, so it tracks the actual active pattern rather than a relaxed collection of bases. Its degree is controlled by `max(P,deg phi,2)`, even though this high-dimensional description is used only for counting and is never expanded algorithmically.
4. The substitutions `p-u^2=0` and `p u^2-1=0` represent weak and strict inequalities exactly over the reals. The condition and variable counts fit the proposed `8(N+k+1)` bound, and summing squares gives degree at most `2(d+2)`. The component bound applies to the resulting possibly unbounded algebraic set. I verified the required affine real-variety statement directly in [Milnor, Theorem 2, printed page 275](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Milnor1.pdf). Continuous projection cannot increase the number of connected components.
5. Pattern-parameter components are intervals or points. Their endpoints give a finite segment partition on whose open pieces a chosen pattern persists. The same-pattern bound extends to endpoints by response continuity. Summing it over the pieces gives the stated global constant. Its numerical size may be exponential, but its logarithm is polynomial in the encoded data and numerical degree. The algorithm needs this bound, not an explicit list of high-dimensional patterns.

The example `g(z)=z^P` establishes sharpness of the exponent. The anchor corollary correctly converts the modulus to tightening exponent `nu=P`; convexity of the reduced constraints and a strict anchor margin remain additional promises. The original `1/(P+1)` two-repair modulus is also proved independently and remains available.

## Upper semantics, exact feasibility, and boundary cases

**Locations:** `sections/04-accuracy.tex:519–838`.

The upper-polynomial constants bound separate leader and response variation on the enlarged response box. Sparse upper monomial lists are expanded only after substitution into fixed-dimensional compressed variables. Numerical upper degrees, including the exponential-sized coefficients represented by the factor `2^degree`, enter through their bit lengths and stated numerical-degree parameter.

The global theorem returns an exactly feasible rational leader and bounds the true induced objective. Its rational optimum estimate follows from the winning surrogate value and the recovery error, without exact summation of true inverse values. Continuity and compactness justify the minimum. The `N=0` branch correctly becomes fixed-dimensional polynomial optimization on the rational leader polytope, rather than being called an LP for nonlinear upper data.

The outer algorithm includes a lift of every truly upper-feasible leader, so emptiness certifies original infeasibility, while returned points may satisfy only relaxed rows. The inner algorithm's positive margin survives recovery and gives exact original upper feasibility. Its nonemptiness guarantee is relative to `V(delta)`, and emptiness does not decide original infeasibility. The posterior lower and upper bounds use their own approximation errors and require an actual inner point for original feasibility. The convergence statements retain the necessary tightening-value qualification.

The supplied-modulus algorithm uses the finite-value and modulus promises and does not purport to verify them. The strict-anchor and reserve-control corollaries give sufficient moduli under their explicit additional assumptions. A response-independent objective does not bypass response approximation when upper constraints still depend on the response. Response equalities, zero coefficients, and zero-dimensional followers are treated with the required distinctions.

The isolated-feasible-optimum and irrational-only-feasible-leader examples check out. The latter's two roots lie in the unit interval and satisfy the unsquared equality. The sparse-power example gives a rational-output length obstruction for its two-power objective; numerical power dependence is retained throughout. The exact radical-sum comparison example is presented as an arithmetic boundary, not as a proof of NP-hardness.

## Independent verification and limits

Artifacts are confined to `verification/reviewer03/stage04/`:

- `snapshot-check.json`: manifest digest and eleven file hashes.
- `check_accuracy.py`, `checks.json`: fresh code importing no author or reviewer implementation. It checks 78 exact increment inequalities and 169 exact Bregman inequalities for a signed marginal with an interior flat point; order-eight inverse Taylor reversion and its denominator invariant; common-active-row correction with a nonzero tangent component; sharp cubic flat-point scaling; a signed balance example with a zero weight; rational movement across a nonlinear inverse-branch boundary using the true inverse bound; the two exact-feasibility examples; and the pattern-lift variable-count estimate.
- `build/`, `build.log`: isolated latexmk build of the frozen manuscript. It produces 45 pages and the final log has no warnings, undefined citations/references, or overfull/underfull boxes. Initial-pass citation warnings in the combined transcript resolve on later passes.
- `milnor1964.pdf`, `milnor-page1.png`: the openly retrieved primary source and the page visually checked for the component theorem. Its PDF has no usable extracted text; the empty text extraction is not used as evidence.

An initial diagnostic assertion compared two equivalent unexpanded SymPy expressions structurally; I corrected the diagnostic to expand the derivative before comparison. The final exact checks pass. This was not a manuscript discrepancy.

The tests are finite checks of distinct contracts, not an implementation of the complete inverse-panel or quantifier-elimination algorithm. The universal analytic disk argument, bit bounds, active-pattern component count, and global error ledgers were assessed mathematically. I did not run the author's tests as independent evidence, implement general QE, repeat a comprehensive literature-priority search, or visually inspect every rendered page. Subject to the minor status correction above, I found the current proof dependencies complete within this stage's scope.
