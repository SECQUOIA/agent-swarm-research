# Independent review: response-dependent upper constraints

Date: 2026-09-06. Verdict: **PASS for Sections 1–10; PASS for the additional
upper-constraint argument in Section 11, conditional on the separately reviewed
convex aggregate theorem; PASS for the polynomial-upper extension in Section
12.** No substantive mathematical error was found.

Reviewed [the candidate note](bilevel-reopened-response-constraints.md), the
[inherited accuracy-bit theorem](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md),
the aggregate recovery argument used by Section 11, and the author's exact
diagnostic script. This review independently reconstructed the new arguments;
it does not certify publication priority or implement the algebraic optimizer.

## 1. The response graph and rational recovery

The inherited construction is sufficient for the stated interface. A true KKT
lift has inverse approximation error at most `eta`, resource allowance `S eta`,
and complementarity allowance `k Lambda S eta`. An arbitrary candidate already
has doubled true residual allowances. Rounding inside its rational cell doubles
the polynomial residual allowances, making true residuals at most `3 S eta` and
`3 k Lambda S eta`. The inherited choice of `eta` with `tau=rho/2`, and
`eta<=rho/2`, therefore gives response error at most `rho` at both the algebraic
candidate and its rational recovery.

The rational point need not satisfy the nonlinear candidate conditions. This
is handled correctly: membership is preserved in the rational cell contained
in `X'`, while quantitative slack handles all nonlinear residuals. Additional
polynomial values can be controlled simultaneously by absolute derivative
coefficient bounds. Their degrees and bit lengths remain polynomial, and the
number of upper inequalities changes polynomial counts, not variable dimension.

The inverse approximations, fixed-dimensional algebraic optimization, and
rational simplex recovery are inherited dependencies, rather than newly proved
numerical routines. The review checked how the new proof uses their guarantees.

## 2. Outer and inner theorems

For the outer sets, `F_j<=A_j rho` includes every truly feasible lift. Thus
emptiness certifies true infeasibility. At a winner, rounding plus response
error gives `f_j(xhat)<=2 A_j rho+delta/4`, and objective comparison gives
`H(xhat)<=V(0)+2 A_0 rho+epsilon/4`. The prescribed tolerances imply the
claimed weaker inequalities. A returned outer point need not be truly feasible;
the statement explicitly preserves that distinction.

For the inner sets, `F_j<=-delta/2` includes every lift feasible at tightening
`delta`, since `A_j rho<=delta/8`. Rounding changes each polynomial constraint
by at most `delta/8`, and the response error contributes another `delta/8`.
The final point therefore has margin at least `delta/4`. This gives exact upper
feasibility, despite possibly irrational follower responses. Inner emptiness
implies `V(delta)=+infinity`, which is correctly distinguished from original
infeasibility. The objective comparison with `V(delta)` uses the same ledger.

The objective certificate has the correct signs. If `a_out` is the exact outer
surrogate optimum, then `a_out<=V(0)+A_0 rho_out` and
`h_out<=a_out+omega_out`. Consequently
`h_out-omega_out-A_0 rho_out<=V(0)`. Exact feasibility of the inner output and
its response estimate give `V(0)<=H(x_in)<=h_in+A_0 rho_in`.
The interval is valid even if the outer surrogate gives a severe underestimate.

As all tolerances vanish, any subsequence of outer outputs has a further
convergent subsequence in compact `X'`. Vanishing violation and response
continuity give exact upper feasibility at the limit. This rules out a limiting
outer value strictly below `V(0)`. True-feasible lifts provide the opposite
bound. No analogous inner convergence follows without right continuity of
`V(t)`, as the supplied example demonstrates.

## 3. Moduli and explicit sufficient conditions

The rational tightening
`t=sigma min(1/2,(epsilon/(2D))^q)` lies in `(0,sigma]` and makes the promised
tightening loss at most `epsilon/2`. Raising a rational to integer power `q`
has output length polynomial in numerical `q` and the rational input lengths.
This matches the explicit numerical-`q` complexity statement; it is not a
polynomial claim in `log(q)`.

For the response modulus, repair `z(x')` into the follower set at `x`, and
repair `z(x)` into the set at `x'`. The two repair costs are at most
`L K B_b h` each. The difference in linear incentives contributes at most
`B_ell h`, using coordinate differences at most one. The cost gap is at most
`T h`, and the existing Bregman lower bound gives response distance bounded by
`K B_b h+(T/mu)^(1/(P+1))h^(1/(P+1))`. For `0<=h<=1`, the rational constant
`C_z` in the note dominates this expression. All coefficients have polynomial
bit lengths, including the signed-marginal `mu`.

Convexity of the reduced upper rows, which is a substantive additional promise,
allows interpolation from an optimizer toward the strict anchor. The reduced
objective need not be convex; its Hölder modulus controls the resulting cost.
The independent-response service subclass is valid because a nonnegative
affine incentive composed with an increasing concave inverse and its upper
constant extension is concave. The exclusion of negative incentives is needed.

For reserve controls, uniform headroom at a common `s_safe` is sufficient even
when the reduced constraints are nonconvex in the remaining leader variables.
Interpolating only reserve leaves the follower response unchanged, maintains
membership in the convex reserve polytope, and costs at most
`||w||_1 t/sigma`. No sign condition on `R` is needed. The product leader set,
reserve-independent follower, fixed total leader dimension, and uniform margin
are all explicit. The conservative affine certificate can indeed be checked
by rational LP when the safe reserve is given rationally.

## 4. Negative examples

For the disconnected-feasibility example,
`g'(z)=3(z-1/6)^2+11/12>0`. Since `g([0,1])=[0,3/2]`, every allowed leader has
an unsaturated inverse response. Monotonicity gives
`z(x)<=x` exactly when `x^2(x-1/2)>=0`, so feasibility is
`{0} union [1/2,1]`. Every positive tightening excludes the isolated optimum.
Writing a tightened boundary parametrically as
`x=g(z), t=z^2(z-1/2)` with `z>1/2` shows explicitly that its global minimum
approaches `1/2`, whereas `V(0)=0`. Thus a strict feasible point and uniform
strong follower convexity do not ensure the needed value continuity.

For the rational-output obstruction, squaring `sqrt(x)=x+1/8` gives
`x^2-3x/4+1/64=0` with discriminant `1/2`. Both roots are positive and below
one, and the unsquared right side is positive; no extraneous roots occur.
Both leaders are irrational, so a general rational exact-feasible-output
theorem is impossible. These examples support the specific limitations stated,
without implying hardness for the margin-promised subclasses.

## 5. Aggregate composition

Section 11 correctly avoids evaluating a branch polynomial after rounding
across its nonlinear validity boundary. It compares the actual final response
to the valid polynomial at the original algebraic candidate using

```
||p(v*)-q(v*)||inf + ||q(v*)-q(vhat)||inf
  + ||q(vhat)-z(xhat)||inf <= 2eta+tau.
```

Adding the leader affine change yields (17). With `eta,tau,h<=kappa`, its row
error is at most `4A kappa`, which is at most each of `epsilon/4` and `delta/4`.
At a true lift only `A_j eta` is needed, so the outer and inner inclusion
arguments survive. The posterior interval correctly approximates the algebraic
surrogate winner directly, rather than evaluating a potentially invalid branch
at the rational output. Its outer lower bound subtracts the true-lift error;
its inner upper bound adds the final recovery error.

The aggregate two-repair modulus follows from two uniform objective-variation
terms `T_x h` and two repair terms `L K B_b h`; aggregate convexity preserves
the local-cost Bregman lower bound. This suffices for convex-anchor interpolation.
Reserve interpolation remains valid only when the complete aggregate follower
is independent of reserve. These are new composition checks, conditional on
the separate aggregate theorem's candidate and recovery guarantees.

Two minor boundary clarifications were requested and incorporated by the author: explicitly
handle `N=0` before minimum-over-coordinates constants, and do not invoke the
inherited `c=0` objective-only LP shortcut when upper constraints still depend
on the response. Neither affects the construction or substantive proofs.

## 6. Polynomial upper functions

The Section 12 extension was checked after its addition. For an explicit
monomial `a x^alpha z^beta`, the sum of absolute leader partial derivatives on
the enlarged box is at most `|a||alpha|_1 2^|beta|_1`; the corresponding
response derivative sum is bounded by `|a||beta|_1 2^|beta|_1`. Thus the supplied
`L_x,L_z` are valid (deliberately conservative) infinity-norm Lipschitz bounds.
The enlarged response domain includes all valid inverse-polynomial endpoints
and the line segments to true responses. This is essential when signs and odd
powers occur.

After inverse substitution the compressed variable count remains fixed and
total degree is at most `D_up max(1,d_p)`. The number of expanded monomials is
therefore polynomial in that degree for fixed dimension. Multiplication of
explicit monomials and coefficient arithmetic require polynomial time and bit
length in the stated **numerical** upper degree. Nothing here implies a sparse
binary-degree theorem. The replacement of response coefficient norms by
`L_z`, and leader coefficient norms by `L_x`, proves the exact same ledgers,
including the aggregate endpoint comparison and posterior interval.

The convex-anchor objective constant follows by splitting leader variation and
response variation. For reserve controls, convexity in reserve of each reduced
constraint is exactly what interpolation needs; an objective Lipschitz bound
replaces its former affine coefficient norm. These assumptions are stated as
promises and do not follow from follower convexity. The zero-follower case is
correctly qualified as fixed-dimensional polynomial optimization and recovery
with the same upper-margin restrictions, rather than an LP claim. Polynomial
objectives without upper response constraints do not need a tightening
assumption. In particular the bilinear tariff-revenue example is covered.

## 7. Independent exact diagnostics

The separate reviewer script
[response_constraints_review.py](../code/bilevel_reopened/response_constraints_review.py)
passed **10,091 exact rational cases**:

- 5,043 pairwise response and signed-objective modulus cases for two-variable
  quadratic followers with moving sum upper bounds, equalities, and lower
  bounds. Followers are solved by exact water filling, with variational
  inequalities separately checked against rational feasible competitors.
- 1,681 cases for a signed cubic marginal whose derivative vanishes at an
  interior point, checking the polynomial response modulus without root solving.
- 120 global tightening-value comparisons for a convex reduced service
  constraint and a nonconvex signed reduced objective with known exact optimum.
- 99 exact points on the tightened optimum curve in the disconnected example,
  showing convergence to the nonzero tightening gap.
- 648 adverse-sign combinations for the posterior interval, including tiny
  independent errors and arbitrarily poor outer surrogate lower values.
- 2,500 polynomial upper-function Lipschitz checks on the enlarged response
  box, with signed mixed monomials, responses outside `[0,1]`, and independent
  leader and response perturbations.

These checks are distinct from the author's tests. They support the proof
audit and do not certify the general quantifier-elimination implementation,
industrial practicality, or publication novelty.
