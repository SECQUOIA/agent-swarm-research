# Independent first audit: one-resource bilevel approximation in accuracy bits

Date: 2026-09-05. Reviewer: `constant_rank_review`.

**Status: PASS.** I independently checked the complete proof in [the candidate](bilevel-one-resource-accuracy-bit-algorithm.md): exact leader feasibility, multiplier bounds, the signed balance identity, polynomial surrogate optimization, rational feasible leader recovery, all error constants, and encoding dependence. The reviewed scalar inverse lemma supplies the required approximation interface. The result is polynomial in rational input length, numerical maximum degree, and requested accuracy bits for fixed leader dimension. This report does not certify novelty or practical running time.

## Exact feasibility, unique response, and bounded multipliers

Each marginal is strictly increasing on the unit interval because it has nonnegative coefficients and at least one positive coefficient at positive degree. Its integral is strictly convex. The follower therefore has a unique minimizer on every nonempty resource slice, including boundary faces; a positive lower bound on the second derivative is unnecessary.

The box's image under the signed scalar resource row is exactly `[b_min,b_max]`. Convexity of the box and its two extremal Boolean vertices prove sufficiency as well as necessity. Thus the rational polytope `X'` describes feasible leaders exactly. It can be empty or lower dimensional. If all weights vanish, the extra condition is exactly `b(x)=0`, and the reviewed diagonal positive-marginal argument applies on that polytope. If the upper response coefficients all vanish, the exact LP shortcut is valid after this feasibility restriction.

For nonzero weights, the four threshold ratios per coordinate give correct global multiplier bounds. For `w_i>0`, the lower bound is no larger than `(ell_i^- - G_i)/w_i`, so the lower multiplier saturates the coordinate at one; the upper bound is at least `ell_i^+/w_i`, so it saturates at zero. For `w_i<0`, the lower bound is no larger than `ell_i^+/w_i`, giving response zero, while the upper bound is at least `(ell_i^- - G_i)/w_i`, giving response one. These inequalities include saturation equality. Since `G_i>0`, at least two collected ratios differ and `L<U`.

The box-Lagrangian response is continuous in leader and multiplier. Each term of its signed resource sum is nonincreasing in the multiplier. At the global endpoints the sums are exactly `b_max` and `b_min`, independently of the leader. The intermediate-value theorem therefore supplies a balancing multiplier for every feasible leader, including endpoint resource values. Lagrangian minimization then proves primal optimality directly; no constraint qualification or multiplier uniqueness is required. If a balancing interval is flat, every balancing response is still the same by strict convexity.

The continuity argument for the true response is valid. Any sequence of feasible leaders admits multipliers in one fixed compact interval. Every convergent multiplier subsequence produces a balanced limiting response, hence the unique optimum at the limiting leader. Applying this to arbitrary subsequences proves full response continuity. Therefore the upper objective attains its minimum on nonempty compact `X'`.

## Exact balance-to-response control

Fix a leader and a balancing multiplier. Increasing the multiplier decreases coordinates with positive weights and increases coordinates with negative weights. Multiplying each coordinate change by its resource weight therefore gives the same weak sign in every nonzero-weight coordinate. Decreasing the multiplier reverses all those signs together. Consequently

```
sum_i |w_i| |q_i(lambda)-z_i*| = |sum_i w_i q_i(lambda)-b|.
```

Zero-weight responses do not depend on the multiplier and contribute no difference, even if their upper objective coefficients are large. This proves the objective-error bound using `c_max/w_min` without any cancellation, derivative estimate, or strong-convexity constant. Saturated coordinates, flat multiplier intervals, and boundary resources all satisfy the same identity.

## Surrogate cells and optimization

I read the [positive polynomial inverse lemma](certified-positive-polynomial-inverse-approximation.md) and its [second full review](review-certified-positive-polynomial-inverse-approximation-second.md) to verify the import. It applies to exactly the nonnegative marginal coefficients stated here. It returns rational thresholds and branches, uniform response error `eta`, degree `O(log(1/eta))`, polynomial coefficient length, and `O(P^2 log(1/eta))` branches. Rational normalization by `G_i` and subsequent affine substitution preserve these bounds. No lower bound on positive marginal coefficients is assumed except through their rational encoding. This audit relies on the lemma's separately reviewed analytic and bit proof rather than treating an inverse-evaluation oracle as free.

The weighted tolerance has polynomial encoding. In particular `W`, `w_min`, `A`, and `C=c_max W/w_min` are rational combinations of polynomially many input numbers. Even when `w_min` is tiny or the weights have very different magnitudes, `log(1/eta)` remains polynomial in their encodings and `B`.

Normalizing the multiplier to `theta in [0,1]` makes every inverse argument affine in only `r+1` variables. The rational threshold arrangement therefore has polynomially many realizable cells for fixed `r`, including lower-dimensional cells. Weakening a nonempty relative cell's strict tests gives its closure: mixing a weakly feasible point with a point of the relative cell proves this assertion. Each chosen branch stays valid throughout that closure, including thresholds where adjacent approximants differ.

The polynomial balance constraint is a closed condition in a compact rational cell. At any true optimal leader and balancing multiplier, uniform coordinate approximation gives `|T_Q|<=W eta`; hence some surrogate feasible set is nonempty. Signed upper coefficients give objective error at most `A eta` there. Exact optimization over all surrogate sets therefore yields the claimed upper comparison with the true optimum.

Quantifier accounting is correct. The formula defining a cell minimizer has only `2(r+1)` variables, regardless of the number of follower coordinates or constraints. The fixed-variable quantifier-elimination and sampling interface was checked against primary degree and coefficient-bit bounds in my [diagonal audit](review-bilevel-bounded-power-accuracy-bit-algorithm-second.md). It supplies a polynomial-degree rational univariate representation of the selected point. Comparing different cell values needs only pairwise algebraic comparisons and retention of the winner's own representation. It does not require a common field containing all cell values or all true follower inverse values.

## Rational recovery and complete error ledger

The distinction between the rational polytope `Q` and the polynomial balance set is essential and correct. The latter may contain no rational point. The recovery step preserves `Q` exactly and budgets an extra residual, which is sufficient for the final true response guarantee.

A bounded rational polytope in fixed dimension has polynomially many vertices of polynomial rational encoding, including when it is lower dimensional. Enumerating affinely independent subsets of at most `r+2` vertices finds a simplex containing the selected algebraic point. Its barycentric weights are rational affine functions of that point and remain in its polynomial-degree field. Flooring all but one weight and assigning the remainder to the last vertex preserves all exact cell equations and inequalities. A grid denominator of order `(r+1)/delta` suffices for infinity-distance at most `delta`; its bit length is polynomial. No lower bound on cell width or coordinatewise rounding is used.

For a polynomial on the unit cube, `max(1,sum |a_nu| |nu|)` bounds the sum of absolute partial derivatives. Thus the chosen `delta` ensures objective deterioration at most `epsilon/8` and polynomial balance deterioration at most `W eta`. Its encoding is polynomial even when `W eta` is extremely small. The recovered leader remains in `X'` and is therefore exactly follower-feasible. The auxiliary multiplier and approximate coordinate responses need not satisfy exact balance.

The final error chain checks as follows:

* The algebraic surrogate point has `|T_Q|<=W eta`; recovery gives `|T_Q(vhat)|<=2W eta`.
* Coordinate approximation contributes at most one further `W eta`, so the true box-Lagrangian response at `vhat` has balance residual at most `3W eta`.
* The exact residual identity bounds its upper response error relative to the true balanced optimum at the same leader by `3C eta`.
* Comparing the surrogate coordinates to that box-Lagrangian response adds `A eta`.
* Thus `|H(xhat)-H_Q(vhat)|<=(A+3C)eta`, and true leader suboptimality is at most `epsilon/8+(2A+3C)eta<=7epsilon/32`.

The optimum-value estimate is equally valid. Exact leader feasibility gives `H(xhat)>=OPT`, so the rational number `H_Q(vhat)` differs from `OPT` by an amount in `[-(A+3C)eta, A eta+epsilon/8]`. These endpoints have magnitudes at most `3epsilon/32` and `5epsilon/32`, respectively. Hence the displayed absolute-error guarantee follows without evaluating any true follower inverse at the output stage. Exact rational evaluation of `H_Q` at the rational recovered point has polynomial bit length.

## Complexity and edge cases

All quantified dimensions and arrangement exponents depend only on the fixed leader dimension. Degrees, branch counts, dense expansions in those fixed variables, rational matrix calculations, and precision lengths are polynomial in the input, numerical `P`, and `B`. Small resource weights or a large multiplier interval affect coefficient lengths and logarithmic precision; neither is used as an inverse numerical iteration bound. The proof is polynomial in numerical `P`, not in `log P` for arbitrary sparse powers.

The diagonal output-length obstruction embeds with a zero resource row. If a nonzero row is required, one can append an independent coordinate with nonzero resource coefficient, fix its resource value, and give it zero upper coefficient; the original hard rational leader output remains necessary. No additional common-field exact arithmetic claim follows. The argument does not extend automatically to leader-dependent resource coefficients, multiple resource rows, or extra response-dependent upper constraints.

## Exact supporting checks

I inspected and reran [the signed-balance checker](../code/bilevel_one_resource/check_signed_balance.py):

```
PASS: 7200 exact signed-balance/error certificates across 160 instances
```

The rational linear-marginal instances include mixed and zero weights, weight denominators `2^20`, global multiplier bounds, saturation, endpoint resources, and exact balance solutions. These checks exercise the new residual identity and objective transfer, not the full inverse approximation or real-algebraic optimizer.

I also reran [the rational recovery checker](../code/bilevel_bounded_power/check_rational_simplex_recovery.py), which passed twelve exact simplex recoveries, including lower-dimensional cells and accuracy requests up to 100 bits. Its exact algebraic-floor and feasibility checks support the inherited recovery step.

No unresolved mathematical or encoding issue remains in the stated one-resource model. The approximation is of the objective at an exactly feasible rational leader; it does not promise an exactly balanced rational follower vector.
