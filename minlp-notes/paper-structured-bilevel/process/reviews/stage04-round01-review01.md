# Independent review 01: stage 4, round 1

Recommendation: accept after one minor correction. I found no major mathematical or bit-complexity defect in this stage. The explicit degree estimate for substitution into an upper polynomial needs correction; the polynomial-time conclusion survives that correction.

## Reviewed material and integrity

I reviewed the frozen `process/snapshots/stage04-round01` source, including all of `sections/04-accuracy.tex`, `appendices/b-inverse-approximation.tex`, and `appendices/c-quantitative-bounds.tex`, the integration in `main.tex`, the bibliography, README, and coverage map. I checked the relevant accepted model, output, and fixed-dimensional elimination prerequisites from the earlier sections. The manifest digest is `4ef85d87d33a7c0860e735f7daa7311f1bc61f20b3ae6a36585f05ffe268befe`; all 11 listed file hashes match.

I did not read other stage 4 reviews or root conclusions, delegate any review work, or modify manuscript or snapshot files. All compilation and independent calculations used `verification/reviewer01/stage04`.

## Actionable finding

**Minor — include the degree of the inverse argument in the upper-substitution bound.** Location: `sections/04-accuracy.tex:538–540`, in `subsec:accuracy-polynomial-upper`, read together with the definition of `a_i(v)` at lines 384–387.

The text says that inverse branches of degree at most `d_p` produce an upper polynomial of degree at most `D_up max{1,d_p}` after substituting `z=p(v)`. In the aggregate model, a univariate inverse branch is composed with the polynomial argument `a_i(v)`. This argument need not be affine. Its degree must therefore enter this estimate.

A model satisfying the assumptions has one response coordinate, `g(z)=z`, `U=1`, `phi(w)=w^4/4`, and constant incentive `ell=1/2`. With `R=1`, an interior inverse branch is exactly the degree-one polynomial `h(a)=a`, but its pullback is `p(t)=1/2-(2t-1)^3`, of degree three. For the degree-one upper function `H=z`, substitution has degree three, whereas the displayed bound gives one. Restricting to the interior branch's validity set does not make this polynomial degree one.

Correction: define `d_a=max_i deg(a_i)` and replace the bound by `D_up max{1,d_p d_a}`; alternatively, explicitly define `d_p` here as the degree of the already composed polynomials `p_i(v)`. A safe argument bound in the present model is `d_a <= max{1,deg(phi)-1}`. The subsequent fixed-dimensional monomial count and coefficient-growth argument remain polynomial in the stated numerical degrees. This is a local accounting correction, not a counterexample to the global algorithm.

## Substantive mathematical assessment

### New sharp response modulus

I checked the full proof of `prop:accuracy-response-modulus`, not just the examples or the earlier weaker estimate.

The common-active-row correction in `eq:active-row-correction` is valid even with dependent active constraints. The actual response difference solves all active-row difference equations, so solving an independent row basis preserves the remaining equations. The integer Gram estimate bounds the selected correction with polynomial-bit data. Subtracting that correction leaves a vector tangent to every common active resource and box row. Both optimal gradients lie in the span of those rows, which gives the claimed cancellation without a constraint qualification or strict complementarity assumption.

Adding the two polynomial Bregman inequalities gives the required strong monotonicity of order `P+1`. The leader perturbation and gradient Lipschitz bounds then give the stated `1/P` estimate within a fixed active pattern. The case split at `||e||_infinity = D_b Delta` avoids division by a possibly vanishing response displacement. The rational upper bound for the resulting root constant is valid since leaders lie in the unit cube.

The globalization argument also checks out. The segment stays in the convex feasible leader projection. The KKT pattern description distinguishes inactive inequalities and interior box coordinates with strict inequalities, and bounded resource multipliers suffice. The degree count includes the complementarity products and the aggregate gradient. The lifts `p-u^2=0` and `p u^2-1=0` express weak and strict inequalities correctly. Their real algebraic sets may be unbounded, but the Milnor theorem used here applies to real affine algebraic sets and does not require compactness. The conservative variable and degree bounds cover the auxiliary variables and the final sum of squares.

Projection cannot increase the number of connected components. In one parameter, each projected component is an interval or point. Counting their endpoints gives a finite partition on whose open intervals one pattern applies; previously established response continuity supplies the endpoint estimates. Summing these estimates gives the advertised global constant. The proof uses the large pattern graph for counting only, so its exponential cardinality does not enter the running time of the algorithm that computes the constant. Its logarithm has the required polynomial bound. The example `z*(x)=x^(1/P)` proves sharpness, and the convex-anchor argument consequently supports the tightening exponent `P`.

I verified the relevant primary statement directly in Milnor's original paper, Theorem 2, printed page 275, and checked the passage to arbitrary affine varieties in its proof: [On the Betti Numbers of Real Varieties](https://www.math.uchicago.edu/~shmuel/QuantCourse%20/Milnor,%20betti%20numbers%20of%20real%20varieties.pdf). A local copy and a viewed rendering of its first page are retained in the verification directory.

### Inverse approximation and bit complexity

I checked the general signed-marginal inverse construction through its complex-critical-value projection, padded bad intervals, rational panels, analytic inverse disks, rational response centers, Taylor recurrence, and denominator bounds. Projecting the real parts of all complex critical values is the appropriate obstruction set; restricting attention to real derivative zeros would not justify the analytic disks. Properness of the polynomial and the absence of critical values on the disk justify the inverse branch used in the coefficient estimates. The construction does not require a uniform positive real derivative.

The explicit denominator invariant and the analytic coefficient bound together control reduced rational coefficients and intermediate exact arithmetic. Their logarithms, panel counts, and truncation orders are polynomial in input bits, numerical degree, and accuracy bits. The positive-coefficient specialization uses its stronger assumption only where required for coefficient majorization and the relative inverse disk. The diagonal power construction keeps numerical-degree dependence separate from the sparse binary-exponent obstruction. The fixed-dimensional rational barycentric rounding argument preserves feasibility, including lower-dimensional faces.

### Resource certificates, nonlinear branch recovery, and global optimization

The exact resource projection and integer-Gram multiplier/repair constants cover signed rows, rank deficiency, equality faces, and zero resource dimension. The signed one-resource proof uses the weighted no-cancellation identity correctly; tiny nonzero weights affect required precision through their bit lengths. The Bregman lower bound is valid for signed polynomial coefficients under strict monotonicity, while the improved positive-coefficient constant is properly restricted.

The aggregate certificate accounts separately for primal resource residual, complementarity residual, and aggregate mismatch. It uses the true response to the frozen gradient and then repairs resource feasibility; it does not confuse frozen-gradient optimality with the coupled follower optimum. The nonlinear branch construction uses realizable sign patterns and closed branch validity sets, which may overlap or be disconnected. Its coverage argument does not require these sets to be polyhedral cells.

The recovery lemma rounds in the rational base polytope. It compares true inverse responses across a possible branch change and does not evaluate the old branch polynomial outside its validity interval. The complementarity ledger includes the potentially large negative inactive slack. The stated 4/5/4 residual allowances and the precision dependence are consistent with those estimates. The upper-function comparison uses the enlarged response box and the original algebraic candidate before rounding, so its validity survives branch changes. Apart from the local degree estimate identified above, the fixed-dimensional optimization and rational-output argument supports the global accuracy theorem.

### Upper constraints and scope

The outer theorem gives a bicriteria output and does not claim exact feasibility. The inner theorem gives exact safety relative to the tightened benchmark, and correctly limits what an empty inner approximation proves. The posterior gap, convergence qualifications, supplied tightening modulus, convex anchor, and reserve-control subclass preserve their distinct assumptions. The irrational-feasibility and isolated-optimum examples explain real limitations of rational exact-safe output and tightening. The independent upper-objective and zero-follower exceptions are handled explicitly.

I compared these developments with the canonical inverse, bounded-power, one-resource, fixed-resource, convex-aggregate, polynomial-upper, and response-constraint source developments and their coverage entries. I found no missing stage 4 dependency or unsupported strengthening other than the degree estimate above. Later structural, experimental, and final synthesis obligations remain outside this stage's acceptance decision.

## Verification and limits

The isolated `latexmk` build succeeded and produced a 45-page PDF. The build summary contains no undefined-reference, citation, multiply-defined-label, overfull, or underfull warnings. Hash results are in `hash-check.json`, and build results in `build-check.log` and `build-summary.json`.

The independent script `check_inverse_modulus.py` uses Lagrange inversion rather than the manuscript recurrence. It checks six inverse coefficients and their denominator divisibility for `z^3`, the signed polynomial `4z^3-6z^2+3z` with a flat interior derivative, and `(z+z^3)/2` with nonreal critical points. Nine exact rational target brackets check the resulting approximants. Three exact examples check common-pattern tangent cancellation and the associated monotonicity identity under the resource equation `z_1+z_2=x`. The script also confirms the upper-substitution counterexample above. Results are in `check_inverse_modulus.json` and `inverse-modulus-check.log`.

These finite calculations support specific algebraic steps; they are not an implementation of the general elimination, analytic inverse-covering, or global optimization algorithms. My acceptance assessment rests on the written proofs and their stated prerequisites. I did not rerun unrelated earlier-stage experiments or claim formal verification of the manuscript.
