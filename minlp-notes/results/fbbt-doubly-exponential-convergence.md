# Doubly exponential iteration counts for primitive bilinear FBBT

Status: candidate result, passed [independent mathematical review](../notes/review-fbbt.md) (2026-09-04); the primitive-iteration theorem has a [completed Lean verification record](../formal/topics/02-fbbt/VERIFICATION.md) (2026-09-11). This is a companion to [the FBBT complexity result](fbbt-monotone-system-hardness.md), whose hardness reduction is outside that formalization. Its proof is elementary, and its novelty has not yet been established.

## Statement and algorithm scope

For each integer `n>=1`, there is a feasible continuous system with exactly `4n+4` variables and defining equations, initial box `[0,1]^(4n+4)`, and affine or bilinear defining equations with coefficients in `{0,1/2,1}`, for which standard primitive FBBT requires at least

`2^(2^n-1)`

applications of one affine constraint before its designated lower bound reaches `1/2`. This bound holds for every finite prefix of every update schedule. Under every fair schedule, both endpoint vectors converge to the unique feasible point, whose designated coordinate is `1`; no finite primitive run attains that lower endpoint exactly.

Here a primitive update computes the interval hull for a single affine equality or a single nonnegative product equality and intersects it with the current box. A schedule is fair if every equation is selected infinitely often, with no bound on the delay between visits. Fairness is needed for the limiting-box conclusion, not for the finite-prefix bound. Symbolic substitution, equation aggregation, LP-based fixed-point acceleration, and stronger global contractors are outside this iteration-count claim. The nonlinear defining-equation dependency graph is acyclic; its only feedback component has two variables, and is linear once its upstream variables are fixed.

The model-size assertion counts its constant-size coefficients and equations. If indexed variable names are counted as binary strings, the ordinary encoding size is `O(n log n)`; the explicit lower bound in terms of `n` is the precise statement.

## Construction

Use an acyclic paired-product circuit to define

`b=2^(-2^n)`, `c=1-b`.

Start with `b_0=c_0=1/2`. For `i=1,...,n`, define

`h_i=b_(i-1)`,

`b_i=b_(i-1)*h_i`,

`v_i=b_(i-1)*c_(i-1)`,

`c_i=c_(i-1)+v_i`.

Induction gives `b_i=b_(i-1)^2` and `c_i=1-b_i`, so all these variables have unique values in the unit interval. Put `b=b_n`, `c=c_n`, and add

`w=c*z`, `z=b+w`.

There are two initial variables and equations, four per squaring stage, and two feedback variables and equations, for a total of `4n+4` of each. Every equation has at most three variable names. All products have distinct names. The acyclic circuit has a unique value. The final two equations imply `z=b+c*z`, hence `z=1` and `w=c`, since `b=1-c>0`. Thus the whole system has a unique feasible point.

Under a fair schedule, the least-fixed-point lemma in the companion result gives convergence of all lower endpoints to that point. Upper convergence needs a separate argument. Fair primitive updates fix the two initial constants and then every upstream variable in acyclic order after finitely many updates. Soundness and the initial unit box keep `u_z=1` throughout. Once the upstream variables are fixed, the next product update gives `u_w=c`. Thus the upper endpoints also converge to the feasible point, and the limiting box is a singleton.

## Iteration lower bound

Give the algorithm additional information by initializing every acyclic variable to its exact value. Leave `z,w` initially in `[0,1]`. Primitive interval-hull updates are monotone with respect to box inclusion, so this stronger initialization can only increase lower bounds compared with the original initialization under the same update schedule. A lower bound on its iteration count therefore also applies to the original initialization.

Write `l_z,l_w` for the two lower bounds. Throughout the stronger run,

`0<=l_w<=c*l_z`, `0<=l_z<=1`.

Initially this holds. A product-constraint update replaces `l_w` by `c*l_z` at most, and its reverse update `l_z>=l_w/c` cannot increase `l_z`. For the affine constraint, reverse propagation can set `l_w>=l_z-b`, which is no larger than `c*l_z`, because

`l_z-b-c*l_z=b*(l_z-1)<=0`.

The forward affine update gives

`l_z(new)=max(l_z(old), b+l_w(old))<=b+c*l_z(old)`.

It also preserves `l_w<=c*l_z`, including when the interval hull updates both variables at once. To see the latter directly, the new lower bound on `w` is `max(l_w(old),l_z(old)-b)`, and both terms are at most `c*l_z(new)`.

The upper bounds cannot interfere with these formulas: the feasible point forces `u_z=1`, and `u_w` is either its initial value `1` or the tightened value `c`. After `K` affine-constraint applications, induction therefore gives

`l_z<=1-c^K=1-(1-b)^K<=K*b`.

Consequently `l_z>=1/2` requires `K>=1/(2b)=2^(2^n-1)`. This counts applications of a particular constraint, and hence also lower-bounds the total number of primitive constraint updates. Since `c>0`, the geometric bound is strictly below `1` for every finite `K`. The comparison with the original unit-box run transfers both conclusions to every finite prefix of every schedule, without fairness. □

The [exact-arithmetic audit script](../code/fbbt-hardness-check.py) also verifies the inequalities for 400 randomly scheduled primitive updates across four small instances.

The [Lean coverage map](../formal/topics/02-fbbt/COVERAGE.md) links the construction and exact counts, simultaneous bidirectional hulls, original unit-box comparison, arbitrary-schedule lower bound, and fair singleton limit to their formal declarations. The September 11 verification record reports kernel replay of all eight FBBT modules and an axiom audit. The binary serialization and `O(n log n)` encoding estimate, companion PosSLP-hardness reduction, publication novelty, and floating-point implementations are outside this formalization.

## Residual versus distance to the limiting box

At the stronger initial box, with the acyclic variables fixed exactly and `z,w` still in `[0,1]`, applying any one primitive update changes every endpoint by at most `b`, but the distance of `l_z` from its limit is `1`. This statement concerns the stronger initial box, not the original unit box. Thus an absolute per-update tolerance cannot certify proximity to the limiting bounds without accounting for numbers as small as `2^(-2^n)`, even though the model itself has only constant-size coefficients.

This does not imply that such a tolerance is unsuitable as a practical stopping rule. It shows that a theorem equating small local changes with certified small error in the ultimate box needs additional assumptions.

## Novelty boundary

Exponential and non-finite convergence of linear FBBT are established in Belotti, Cafieri, Lee, and Liberti, [*On feasibility based bounds tightening*](https://optimization-online.org/wp-content/uploads/2012/01/3325.pdf). The mechanism here combines the elementary slow recurrence `z<-b+(1-b)z` with a polynomial-size bilinear circuit for a doubly exponentially small positive number. The construction is not claimed to introduce either mechanism individually.

The potentially new statement is the explicit doubly exponential primitive-iteration lower bound for constant-coefficient bilinear input, including its small directed feedback component. The [dedicated source assessment](../notes/fbbt-novelty.md) is complete. It found no matching restricted contractor theorem, while crediting the established slow-iteration mechanisms; publication priority remains unconfirmed.

There is also close monotone-polynomial-system prior art. Esparza, Kiefer, and Luttenberger (SICOMP 2010, Section 7, Theorem 7.1), and Stewart, Etessami, and Yannakakis (JACM 2015, Section 4.1, equation (18)) study a chain of scalar quadratic components with square-root amplification of errors. Their established slow-Newton examples also imply doubly exponential first-bit convergence for ordinary Kleene iteration when combined with the scalar critical recurrence. Thus doubly exponential monotone iteration alone is not a sound novelty claim. The specific distinctions here are that the lower bound survives every ordering of the stated **bidirectional primitive interval-hull contractors**, and that it needs only **one feedback component, which becomes linear once the acyclic upstream values are fixed**. See the [Stewart–Etessami–Yannakakis author manuscript](https://homepages.inf.ed.ac.uk/kousha/final-jacm-cav13-jversion.pdf). These distinctions still need assessment for publication value.
