# Independent review of the Hessian-span decision benchmark

Date: 2026-09-28. Scope: the reduction, degree-construction dependency,
precision example, and significance claims in
[the benchmark note](span-fpt-decision-frontier.md), together with
`check_span_fpt_benchmark.py`. This reviewer did not develop the benchmark.
A separate fresh reviewer checked the precision example and the proposed
gap-to-algorithm implication. The review found no mathematical defect in
the reduction or residual bound. Two wording corrections and two scope
clarifications are recorded below. This is a proof audit, not formal
verification or a novelty assessment.

The defensible result is a polynomial reduction from the selected sum of
strictly convex trust-region minima to compact native-PSD QCQP feasibility,
with Hessian span at most `k+1`. It does not establish parameterized
decision hardness or an FPT algorithm.

1. The secular normalization and selected value are correct. Positivity
   of every `d_ij` makes the objective strictly convex. If the unconstrained
   minimizer has norm at most one, the stated rational minimum applies,
   including the boundary case with multiplier zero. Otherwise at least
   one `b_ij` is nonzero, and
   `R_i'(T) = -2 sum_j b_ij^2/(T+d_ij)^3 < 0` on the nonnegative axis.
   Its endpoint values give the unique positive multiplier. Stationarity
   uses `lambda_i (||x_i||^2-1)/2`, exactly as stated. Substituting
   `d_ij*x_ij = b_ij-lambda_i*x_ij` and the active unit norm yields
   `beta_i = -(lambda_i + sum_j b_ij^2/(d_ij+lambda_i))/2`.
   Denominators cannot vanish at the selected positive root. Repeated
   diagonal entries and zero linear coefficients therefore do not cause
   an erroneous root selection; the unreduced polynomial is not the
   definition of the selected root.

2. The threshold reduction is exact. Separability gives the minimum
   `S = sum_i beta_i`, and each block minimum is attained uniquely.
   Hence the threshold system is feasible exactly when `S <= t`.
   Its budget Hessian is the positive diagonal matrix of all `d_ij`.
   The ball rows contribute at most `k` further Hessian directions, and
   copying the rational coefficients has polynomial cost. If a target
   algorithm costs `g(h) N^C`, the polynomial increase in input length
   and `h <= k+1` preserve FPT dependence on `k`.

   One literal correction is needed in the sentence calling the ball
   Hessians block identity matrices: they are **twice** the embedded
   block identity matrices. This factor does not affect the span or
   convexity. The check script already uses the correct Hessians.

3. Strict feasibility and the threshold boundary are handled correctly.
   When `t > S`, scaling every minimizing block by `1-epsilon`, with
   sufficiently small `0 < epsilon < 1`, makes every ball inequality
   strict and preserves the positive budget margin by continuity.
   When `t = S`, every feasible block must attain its own minimum, so the
   feasible set is the single product minimizer. This also covers blocks
   whose minimizers are interior. Equality with a rational threshold is
   a conditional case; the high-degree construction does not supply such
   equality instances. The compact domain and attainment claims do not
   depend on that construction.

   A second wording correction is advisable: the sentence saying that
   FPT feasibility gives an FPT algorithm “for (1)--(2) and its sum
   comparison” should say **for selected secular-sum comparison**.
   Read literally, the former wording might promise exact multiplier or
   value reconstruction. The reduction proves only a yes/no implication,
   and the choice of exact output representation matters elsewhere in
   the note.

4. The invocation of the
   [short-input construction](short-input-qcqp-degree-lower-bound.md)
   is legitimate. Its independent product-ball version, before the
   optional mixing of constraints, has precisely the required form.
   A positive weight `w_i` is absorbed by replacing the block diagonal
   and linear coefficients by `w_i d_ij` and `w_i b_ij`. The multiplier
   then scales by `w_i`, and the selected value becomes `w_i beta_i`.
   Positivity, rationality, and short coefficient lengths are preserved.
   Thus the source's primitive weighted sum supplies the degree product
   for the benchmark's unweighted sum of these rescaled block values.

   The source explicitly supplies short-input existence, rather than
   relying on generic algebraic degree. For fixed `k`, its
   `N = O_k(R^2 log R)` and degree `Omega_k(R^k)` contradict a dense
   minimal-polynomial output bound `g(k) N^C` by fixing `k > 2C` and
   letting `R` grow. A fixed rational threshold adds negligible length.
   The deterministic-weight version uses a larger absolute input
   exponent and gives the same conclusion by taking larger fixed `k`.
   Finding the existential short weight is unnecessary for an
   output-length lower bound. This review checked the dependency and
   parameter accounting; it did not rerun the source's full arithmetic
   proof or its verification suite.

5. The output and decision distinctions are maintained. The degree
   product obstructs a method required to produce a dense minimal
   polynomial before deciding. It does not obstruct selected-root
   comparison, circuits, separate number fields, or every exact
   representation. The note correctly refuses to infer an attained
   near-rational gap from a generic algebraic separation estimate.

   The sparse refinement needs its stated translation qualification:
   it makes the polynomial of `S+s` dense after a short rational
   objective shift. It does not automatically prove that the raw,
   zero-constant sum `S` defined in Section 1 has many nonzero minimal-
   polynomial coefficients. Adding an objective constant and changing
   the threshold accordingly preserves the decision problem, but a
   comparison algorithm can retain the shift separately. The current
   phrase “after a ... translation” is valid; an explicit sentence
   retaining this scope would prevent a stronger reading.

   The Square-Root Sum comparison is also consistent. For `k` integer
   radicands, the product over at most `2^k` conjugates gives an effective
   separation bound with `2^{O(k)} poly(N)` required bits. Equality is
   handled by that nonzero-gap bound. Rational linear objectives on unit
   balls can represent the radicals with polynomial input length: the
   binary expansion of an integer expresses it as at most twice its
   bit length many integer squares. Minimizing the corresponding linear
   form gives minus its square root. This concerns the stated broader
   linear-objective variant, since Section 1 requires positive quadratic
   coefficients.

6. The repeated-squaring example is a genuine residual-precision lower
   example. Its nonzero Hessians are `2 e_(i-1) e_(i-1)^T`, so their span
   has dimension exactly `h`; the equality and box rows are affine.
   Nonnegativity permits induction from `x_0=1/2` to
   `x_i >= 2^(-2^i)`, contradicting `x_h <= 0`. The residual objective
   is continuous on a nonempty compact domain. It has a positive
   minimum because a zero minimum would be a feasible point. The
   displayed exact chain gives the upper bound
   `alpha_h <= 2^(-2^h)`.

   Consequently `log_2(1/alpha_h) >= 2^h`, although the input length is
   polynomial in `h`. The very long denominators of the exhibited point
   are not input coefficients. This excludes a uniform polynomial
   precision bound for the specified residual-gap strategy. It does
   not exclude FPT precision or give a decision-time lower bound.
   Nor is this chain a precision lower example for the special
   product-ball benchmark: the note properly treats it as a different
   native-PSD family.

7. The proposed gap theorem would suffice for comparison, including
   equality, provided it is uniform and effective and `N` includes the
   rational threshold. A precise formulation is
   `S=t` or `|S-t| >= 2^(-L)`, where
   `L=ceil(g(k) N^C)`, `g` is computable, and `C` is absolute.
   Approximate each block value with error at most `2^(-L)/(8k)`.
   The total error is at most `2^(-L)/8`; an approximate difference
   of magnitude below `2^(-L)/2` identifies equality, and otherwise
   its sign is correct. This is more precise than “reciprocal
   logarithm,” which can be read in more than one way.

   The required block approximation has polynomial bit complexity.
   For a boundary block, set `B=max(1,sum_j |b_j|)` and bracket its
   multiplier in `[0,B]`; `R(B)<1`. Exact rational bisection applies.
   For the displayed value function `v(T)`,
   `|v'(T)| <= (1+R(0))/2` throughout the bracket. Both this bound and
   `B` have polynomial encoding length. Obtaining `P` accurate value
   bits therefore takes polynomial time in the input length and `P`,
   including rational arithmetic. Substitution of the hypothesized
   `L` gives an FPT comparison algorithm. This supplies the missing
   algorithmic detail; it does not prove the hypothesized gap bound.

The narrowing is useful as research organization, with limited theorem
content. The reduction itself is the standard threshold encoding of a
separable optimization problem. Its useful feature is the explicit
restricted family: positive diagonal objectives, selected monotone
secular roots, compact product balls, a precise strict-versus-boundary
dichotomy, and inherited short-input degree growth. It gives a concrete
subproblem on which to seek a better gap or certificate theorem. It is
neither a known hard source problem nor a proved equivalent formulation
of general Hessian-span feasibility. The note's statement that this is
not a proposed principal contribution is appropriate; the degree and
precision observations do not change that assessment.

The targeted mathematical check actually run was
`python research-20260927/check_span_fpt_benchmark.py`; it passed. The
script checks the exact secular and value identities for `d=(1,2)` and
`b=(1,1)`, quartic irreducibility, the displayed three-dimensional
Hessian span, PSD/PD conditions, and twelve exact squaring chains.
These are useful checks of formulas and parameter accounting. They do
not prove the general reduction, select the relevant root by themselves,
or establish a general gap or complexity theorem. The general claims
were checked from their displayed proofs. An inline Python check of this
review's local links, final newline, whitespace, and control characters
also passed. No project-wide verification or CI inspection was performed.
