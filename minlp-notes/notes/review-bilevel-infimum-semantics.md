# Independent audit: compressed bilevel infima and pessimistic semantics

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the compressed-response infimum and semantics note](bilevel-compressed-response-infimum-semantics.md). Both corollaries follow from the previously audited response representation. The note correctly distinguishes exact semialgebraic optimization from unconditional attainment, and its two pessimistic counterexamples are valid.

## Polynomial shared normals

At every fixed leader, the follower constraints remain linear in the follower variables. Polyhedral KKT necessity therefore still holds even if the shared matrix loses rank or its normals change with the leader. The compressed resource multipliers have the same fixed dimension. In the scalar case the only rational-response denominators are the positive local quadratic coefficients; changing the shared matrix does not introduce a matrix inverse or require constant shared rank.

For fixed-dimensional blocks, only the shared resource normals vary. Local equality bases, independent local active subsets, and the invertible positive-definite block KKT systems remain as already proved. Polynomial shared-normal dependence enters the effective linear cost and shared feasibility equations and preserves polynomial degree and bit bounds in fixed compressed dimension.

The fixed-normal Hoffman continuity argument is no longer available. The example `xz=0` with follower cost `(z-1)^2` is correct: the response is zero for positive `x` and one at zero, so the optimistic upper value `x+z` has infimum zero without an optimizer. The candidate responds by computing the infimum and deciding attainment, rather than asserting closedness of the reaction graph.

A feasible problem still has bounded upper values. The leader set is compact, its polynomial follower bounds have a uniformly bounded union, and the upper polynomial is continuous on the resulting compact enclosing set. Attainment is unnecessary for boundedness. The attainable upper-value set is semialgebraic through the compressed response formula, so its finite infimum and whether that endpoint belongs to the set are exactly computable.

## Pessimistic convention

The stated convention requires all global follower optima to satisfy every upper constraint and evaluates the largest upper objective among those optima. The formulas implement precisely this convention:

- `T(x,eta)` includes upper objective values of all global follower optima, without filtering them by upper constraints.
- `Bad(x)` records the existence of any global follower optimum violating an upper weak inequality, using a strict positive violation.
- `D(x)` excludes empty follower response sets and excludes every bad leader.
- `Worst(x,eta)` requires both an attained response value `eta` and an upper bound on every value represented by `T`.

For a fixed feasible leader, the global follower optimum set is closed inside its compact feasible polyhedron. Therefore its worst upper objective is attained, validating the existence condition in `Worst`. This pointwise attainment does not imply that the leader infimum is attained.

Nonunique multiplier encodings do not affect the predicates, because they describe the same visible follower points and values. Multiple passing local regimes return the same follower vector at their common compressed coordinates, by the previously audited local uniqueness argument.

## Fixed-dimensional formula size and algebraic recovery

The number of copies of the globally optimal response predicate is fixed. Regime and upper-constraint alternatives reuse the same compressed variables; they do not need fresh quantified variables for every regime or constraint. One implementation may first eliminate the internal quantifiers of the response predicate once, then form the polynomial-size disjunctions. Alternatively, the shared response predicate can be factored outside those disjunctions. Either construction makes the stated fixed-total-variable bound explicit.

Applying the already checked fixed-dimensional real-algebraic algorithms gives a univariate description of the set of pessimistic attained objective values. If the admissible set is nonempty, this value set is nonempty and bounded. Its infimum is a finite algebraic endpoint, and exact endpoint membership decides attainment.

The proposed first-order infimum formula is correct: one clause says `eta0` is a lower bound; the other says there is a value below `eta0+epsilon` for every positive epsilon. For a nonempty bounded set these clauses characterize its infimum uniquely, whether or not it belongs to the set. Substituting a fixed-dimensional representation of the value set adds only a fixed number of variable copies.

When attainment holds, combining this property with `Worst` and an explicit compressed response realizing the value provides simultaneous algebraic recovery. Fixed-dimensional sampling places the leader, worst-case response encoding, and infimum in one polynomial-degree extension. Rational evaluation of the remaining follower coordinates in that extension preserves polynomial total output length. The optimistic corollary follows by the same construction with optimistic attainable values.

## Nonattainment and nonclosed robust admissibility

For `f(x,z)=z^2(1-z)^2+xz` on the unit square, positive `x` has unique follower optimum zero because every positive `z` makes `xz>0`. At zero, the two and only follower optima are zero and one. With `F=x+z`, the pessimistic value is `x` at positive leaders and one at zero. Its infimum zero is unattained. The decomposition into positive local quadratic coefficient one and the displayed nonconvex aggregate polynomial is exact, so the example lies inside the fixed-normal structural class.

Adding `z<=1/2` as a robust upper constraint excludes zero but admits every positive leader. Thus the robust admissible leader set is not closed. Under optimistic semantics, zero remains feasible through its response zero. These examples support precisely the stated limitations and do not contradict the original optimistic fixed-normal attainment theorem.

The corollaries preserve the existing restrictions on local response structure, block dimension, and degree encoding. This audit verifies the deductions and semantic definitions; it does not certify their novelty independently of the author's literature review.

## Delta audit: polynomial local normals and changing equality rank

**PASS for the enlarged local-normal scope.** I independently reviewed [the moving-local-normal note](bilevel-moving-local-normal-extension.md) and reread its integration into Section 1 of [the result](../results/bilevel-compressed-response-infimum-semantics.md). The preceding audit covered shared-normal changes; the following argument validates the additional local-normal changes now included in the theorem.

Enumerating all equality/inequality row subsets with combined size at most the fixed local dimension gives polynomially many candidate systems. A subset need not form a basis at every leader. The explicit nonzero-determinant guard selects exactly the leaders where its local constraint rows are independent: positive definiteness proves sufficiency for invertibility, and a row dependence supplies a nonzero multiplier vector in the KKT matrix kernel, proving necessity.

Each branch uses its squared determinant as denominator and includes a strict positivity guard before denominator clearing. Every original equality and inequality remains a feasibility test. Nonnegative multipliers on the selected inequalities, with zero multipliers on omitted rows, give valid sufficient local KKT conditions. Thus soundness does not require the selected equality subset to span all equality rows.

For completeness at a particular leader, choose an actual basis of its equality row space and reduce the active conic normal representation modulo that space to independent generators. This gives one enumerated pair with a nonsingular KKT system and valid multipliers. At a rank drop a different subset, possibly the empty equality subset, supplies the representation. If zero equality normals acquire inconsistent nonzero right-hand sides, the retained full feasibility tests reject all branches.

The determinant guards are part of the jointly enumerated sign conditions. Therefore no branch is used at a pole, and branch validity is constant within each regime. Overlapping valid branches return the same unique local minimizer. First-valid-branch selection still avoids the Cartesian product of block choices. Determinants and cleared tests have polynomial degree and bit size because local dimension is fixed; common denominator products and all global quantifier formulas remain polynomial in fixed compressed dimension.

Near rank changes, multipliers may diverge and the reaction graph may fail to be closed. Neither phenomenon invalidates pointwise representation or algebraic sampling. The theorem retains the correct infimum-and-attainment-decision conclusion, while the original fixed-normal theorem retains its separate unconditional optimistic attainment guarantee.

I ran `code/bilevel_response/check_response_boundaries.py`; its exact guarded moving-normal branch and nonglobal KKT exclusion checks passed. The integrated result's enlarged scope is consistent with the independently verified branch proof. No correction was needed.

Final sign wording checked after the other reviewer flagged it: the cone contains the **negative** local objective gradient. The author corrected this wording in both notes and both integrated results. The stationarity matrices and nonnegative inequality-multiplier tests already used the correct sign; the correction does not change the algorithm or this PASS conclusion.
