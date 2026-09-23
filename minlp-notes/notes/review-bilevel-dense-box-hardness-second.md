# Second independent audit of scalar-leader dense-box hardness

Date: 2026-09-05. Reviewer: `binary_formulation_review`.

**Verdict: PASS, with the joint-convexity clarification incorporated by the
author.** I independently checked
[the construction](bilevel-dense-box-hardness-investigation.md), including the
exact Boolean responses, auxiliary feedback, constant objective gap, rational
encoding, and NP membership. Joint convexity applies to the sum-of-squares
objective with its leader-only quadratic term retained. The normalized
objective obtained by deleting that term has identical follower responses but
need not be jointly convex.

## Every Boolean vector remains an exact follower response

The displayed ternary leader satisfies `0<x_b<1`: its largest possible value
is `1-1/(2*3^n)` and its smallest is `1/(2*3^n)`. Substitution into the base
residual gives exactly the displayed remaining-digit expression.

When `b_i=0`, the maximum possible contribution from later bits gives residual
`1/(2*3^(n-i))`, while the minimum later contribution gives residual at most
one. When `b_i=1`, the corresponding residual lies between minus one and
`-1/(2*3^(n-i))`. Thus the required derivative sign has a strictly positive
margin before accounting for later residuals.

Dividing the later-coordinate contribution by `w_i` gives the bound
`6 rho/(1-3 rho)`. Since `rho=1/(100*3^n)` and `n>=1`, this is strictly below
`1/(10*3^n)`. The direct residual magnitude is at least
`3/(2*3^n)`. Hence its signed derivative exceeds `w_i/3^n`, as claimed.
The lower-triangular base residual matrix has determinant one, so its positively
weighted Gram matrix is positive definite. Box KKT conditions are sufficient
and the encoded Boolean point is the unique base response.

Conditional on any `y in [0,1]^n`, the auxiliary minimizers are exactly the
two clipping formulas. The identity `p_i+q_i=|2y_i-1|` follows for the entire
interval, including `y_i=1/2`. Although the auxiliaries affect the optimum in
`y`, conditional minimization in `p,q` remains necessary at every full optimum.

At a Boolean vector, the extra derivative in coordinate `y_i` is `-2 eta`
at zero and `+2 eta` at one. This opposes the base margin but is smaller in
magnitude, because `2 eta=2 rho w_n<w_n/3^n<=w_i/3^n`. The auxiliary endpoint
derivative signs also hold; some are zero, which is allowed by box KKT.
Thus every Boolean response survives the feedback exactly.

The full residual Jacobian in `(y,p,q)` has diagonal blocks `L,I,I` and is
invertible. Positive weights give a positive definite follower Hessian that is
independent of the leader. The additional rows do not introduce lower-level
constraints: the complete feasible follower region is still the unit box.

## Joint convexity and the normalization distinction

Every residual in the unnormalized construction is affine in `(x,y,p,q)`.
Its positive weighted square is jointly convex, and their sum is jointly
convex. This proves the advertised stronger restriction when the leader-only
quadratic term is retained.

Deleting that term gives the normalized lower expression with Hessian in
`(x,z)` of the form `[[0,d^T],[d,Q]]`. If `d` is nonzero, this matrix is not
positive semidefinite: its quadratic form can be made negative by a suitable
choice of the scalar coordinate. Consequently, the normalized expression is
not itself the jointly convex representation. The author explicitly corrected
this distinction during review. Both representations induce exactly the same
follower map and the same bilevel problem.

## Feasibility, gap, and attainment

At `x=1/2`, all base coordinates equal one half and both auxiliary vectors
are zero. The geometric-series identity in the draft makes every residual
zero. The follower objective is a sum of nonnegative squares, so this is its
unique minimizer. Every three-literal clause inequality then has left-hand
side `3/2`; the constructed instances are always feasible.

At any follower response, the upper objective is exactly
`2 sum_i min(y_i,1-y_i)`, so it is nonnegative. A satisfying Boolean vector
has an encoded feasible leader and objective zero.

For an unsatisfiable formula, rounding any feasible response produces a
Boolean assignment with a false clause. The continuous value of each false
literal is the corresponding `min(y_i,1-y_i)`, including ties under the
specified rounding convention. The clause has three distinct variables;
therefore its sum is bounded above by the sum over all coordinates. Its
upper feasibility inequality forces that sum to be at least one. The upper
objective is consequently at least two. Distinctness is used here and is
stated explicitly.

The distinct-variable restriction of 3SAT causes no reduction gap. Repeated
literals can be simplified and tautological clauses removed. A two-literal
clause can be replaced by its two extensions with opposite signs of a fresh
third variable. A one-literal clause can be replaced by four clauses containing
all sign choices of two fresh variables. These preserve satisfiability and
have polynomial size.

The response map is continuous because its domain is a fixed compact box,
its objective is continuous, and its optimum is unique. Taking convergent
subsequences of follower minimizers and passing their objective comparisons
to the limit proves this directly. The feasible leader-response graph is
compact after imposing weak upper inequalities, and the upper objective
attains its minimum. There is no hidden infimum-versus-minimum exception.

An estimate with absolute error strictly below one distinguishes value zero
from value at least two by comparison with one. This proves the stated
approximation consequence. It does not imply hardness for approximate
follower responses, since the construction uses small lower-level margins.

## Rational encoding and NP membership

The coefficients `3^i` have `O(n)` bits, and the weights `rho^i` have
`O(n^2)` bits. Expanding the polynomially many affine squares creates only
polynomially many rational quadratic coefficients with polynomial bit
lengths. The encoded leader for a satisfying assignment is rational with
polynomial bit length. Ill conditioning does not invalidate these exact bit
bounds, but no favorable condition-number claim follows.

Upper variable coefficients lie in `{-1,0,1}`. After collecting a clause into
`Az<=b`, its right-hand side lies in `{-1,0,1,2}`; the upper objective has
constant `n`. Thus all nonobjective-constant upper data are uniformly bounded
integers. I flagged this distinction when the author tightened the original
wording about small integer coefficients.

For a general rational instance of the stated class, fix the lower/free/upper
status of every follower coordinate. The free principal submatrix of `Q` is
positive definite and invertible. Rational linear algebra expresses the free
coordinates affinely in the scalar leader, with polynomial coefficient bit
length. Fixed bound coordinates, free stationarity, endpoint gradient signs,
upper affine constraints, and the objective threshold define a closed rational
interval in `[0,1]`, possibly empty or a singleton. If it is nonempty, it has
a rational point of polynomial bit length. The resulting follower vector is
also rational with polynomial bit length.

A verifier checks the chosen point, box KKT signs, upper constraints, and
objective threshold using rational arithmetic. Positive definiteness makes
the follower KKT test sufficient. Allowing free coordinates at bounds uses
weak tests and includes degenerate status descriptions. This establishes NP
membership for the zero-threshold problem, completing NP-completeness with
the reduction.

## Checks and attribution

I inspected and ran
[the exact rational checker](../code/bilevel_response/check_dense_box_path.py).
It passed 510 full Boolean-response KKT checks for `n<=8`, four independently
expanded positive definite Hessian checks, and 129 feasible rational-grid
checks of the unsatisfiable-clause gap. These corroborate the algebra; the
general proof above supplies the unrestricted result.

I also read the main theorem and relevant construction discussion of
[Sugishita–Carvalho](https://arxiv.org/html/2510.21126), which already establish
single-leader bilevel LP hardness using a ternary construction. The draft
correctly treats that work as an antecedent. This audit verifies the stated
pure-box strictly convex quadratic reduction and its gap; it does not claim
priority for single-leader hardness or all-Boolean parametric paths.

## Further audit: removing every upper constraint

I independently reviewed
[the clause-shortfall extension](bilevel-dense-box-no-upper-constraints-extension.md).
**PASS.** It strengthens the same theorem to an empty upper constraint list,
apart from the scalar leader interval. No correction was needed.

For `y` in the unit box, every clause literal sum satisfies `0<=ell_a(y)<=3`.
Conditional minimization of its added square therefore gives
`v_a=clip_[0,1](1-ell_a)=max(0,1-ell_a)`. The existing `p,q` conditional
formulas are unchanged. Consequently the new affine upper objective equals

```
2 D(y) + 2 sum_a max(0,1-ell_a(y)),
D(y)=sum_i min(y_i,1-y_i),
```

on every full follower response. This identity holds despite the influence of
the new squares on the base response `y`.

At any Boolean vector, a clause with zero, one, two, or three true literals
has its conditional auxiliary coordinate equal to one, zero, zero, or zero,
respectively. Its residual is correspondingly zero, zero, one, or two.
The new contribution to any base gradient has absolute value at most
`2m xi<2eta`, because each clause uses distinct variables and
`xi=eta/(m+1)`. Adding the earlier contribution gives total feedback strictly
below `4eta=w_n/(25*3^n)`, smaller than the proven base margin for every
coordinate. All Boolean assignments therefore retain their exact encoded
responses, not just satisfying assignments. Conditional auxiliary endpoint
KKT signs hold, and the enlarged residual matrix has diagonal blocks
`L,I,I,I`. Its positively weighted Gram matrix is positive definite.

For a satisfiable formula the corresponding Boolean response has zero
minority amounts and zero clause shortfalls, giving upper value zero.
For an unsatisfiable formula, round an arbitrary base vector and choose a
false clause. Its literal sum is bounded above by `D(y)`, so the upper
objective is at least

```
2 D(y) + 2 max(0,1-D(y)) >= 2.
```

This argument applies to every base vector in the cube satisfying the
conditional auxiliary identities. It does not need any upper clause
feasibility inequalities. Thus the objective gap survives their complete
removal.

The follower domain remains a constant compact unit box, and its objective
remains strictly convex in followers and jointly convex with the retained
leader-only term. Every leader is feasible, the unique response is
continuous, and the minimum is attained. Adding `m` variables and the weight
`eta/(m+1)` preserves polynomial rational encoding. The affine upper objective
now has variable coefficients in `{-1,0,2}` and constant `n`. The previous
active-status rational witness proof applies without change, establishing NP
membership for the strengthened class.

## Final integrated theorem: one auxiliary per base coordinate

I reread the complete promoted
[final theorem](../results/bilevel-scalar-leader-spd-box-np-completeness.md),
which removes the symmetric `q` coordinates. **PASS.** For every
`y_i in [0,1]`, the remaining conditional response
`p_i=max(0,2y_i-1)` satisfies `y_i-p_i=min(y_i,1-y_i)` exactly.
Thus the linear objective
`2 sum_i y_i-2 sum_i p_i+2 sum_a v_a` has the same minority-plus-shortfall
identity used in the gap proof, without an objective constant.

At a Boolean point, the remaining square contributes `-2eta` to a zero
base coordinate's derivative and zero to a one coordinate's derivative.
Its magnitude is at most the earlier bound. Clause feedback is unchanged,
so the combined bound below `4eta` remains valid. The residual Jacobian now
has diagonal blocks `L,I,I`; the positive definite Gram argument holds in
dimension `2n+m`. Every Boolean assignment retains its encoded response.
The absence of upper constraints, constant gap, polynomial encoding,
attainment, jointly convex retained-square representation, and rational
NP witnesses are all stated consistently in the integrated proof.

I also checked the optional approximation consequence in Section 8 of the
investigation. Adding one to the final upper objective gives an optimum
of one versus at least three, so an exactly feasible solution with ratio
strictly below three distinguishes the two cases. For `s=n+m`, the scaled
objective `1+2^s F` has polynomial encoding length and a no-instance value
at least `1+2^(s+1)`. Since the constructed input length is polynomial in
`s`, this eventually exceeds any fixed polynomial approximation guarantee
in that length. Finite exceptional sizes can be handled separately.
The claim is therefore valid for polynomial-time approximation algorithms
returning exactly bilevel-feasible solutions with the stated multiplicative
guarantees. It is a numerical-scaling corollary, as the note explicitly says;
it does not retain the main theorem's constant upper coefficients or give
a claim about approximate follower feasibility.
