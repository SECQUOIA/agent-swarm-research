# Second independent review: response-dependent upper constraints

Date: 2026-09-07. Reviewer: independent subagent `nearoptimal_review1`, who did
not author the result. Disposition: **PASS**, conditional on the stated promises
and the separately reviewed inverse and convex-aggregate dependencies. No
substantive proof defect found in Theorems 1–2, Corollaries 3 and 5–7, the
posterior interval, or the negative examples.

Read the complete [response-constraint note](bilevel-reopened-response-constraints.md),
the complete [fixed-resource theorem](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md)
including its signed-polynomial extension, and the complete
[convex-aggregate theorem](bilevel-reopened-nonlinear-aggregate.md). This review
checks their composition directly; it does not replace the independent audits
of the polynomial-inverse approximation lemma or certify publication priority.

## Surrogate interface, outer and inner optimization

The response-surrogate interface extracted in Section 3 is supported by the
base theorem. Taking `tau=rho/2`, inverse error `eta<=rho/2`, and the original
residual restrictions gives the promised response error both at candidate points
and after rational recovery. At a rounded point, resource and complementarity
allowances each grow by the explicitly budgeted amount; transferring from the
polynomial response to the true clipped inverse yields the threefold allowances
in the base proof. These imply inverse-response error at most `tau`, and adding
the inverse-polynomial error gives at most `rho`. The true KKT lift is always
included. Rational recovery preserves the enclosing rational cell and exact
membership of the leader in `X'`, not arbitrary nonlinear candidate feasibility.

The additional upper-polynomial rounding requirements can be imposed together
with those residual requirements because there are polynomially many explicitly
encoded polynomials in fixed dimension. Their coefficient bounds give sufficient
rounding accuracy with polynomial bit length. Degenerate and lower-dimensional
rational cells are handled by the same rational-simplex recovery.

The outer ledger is correct: the true optimum has a candidate lift feasible for
`F_j<=A_j rho`, and the combined lift, rounding, and response errors yield
`2A_j rho+delta/4<=delta/2` and objective excess at most `epsilon/2`. Thus empty
outer candidates certify original infeasibility, whereas a returned point may
violate the original rows and is not a certificate of exact feasibility.

The inner ledger is also correct. Every leader feasible with tightening `delta`
has a candidate lift satisfying `F_j<=-delta/2`. At the recovered point,
`-delta/2+delta/8+A_j rho<=-delta/4`, which proves exact original upper feasibility.
Its objective comparison is against `V(delta)`; no unjustified comparison with
`V(0)` is inserted before a tightening modulus is supplied. Nonempty inner
candidates can yield a safe leader even when `V(delta)` is infinite. Empty inner
candidates certify only that the `delta`-tightened original problem is empty.

The shared-response dimension does not grow with the number of upper rows.
Rows are extra polynomials in the same compressed coordinates, so fixed-variable
real algebraic optimization remains polynomial in their total explicit input
size. No exact evaluation or comparison of a growing collection of independent
inverse radicals is used.

## Effective moduli and posterior bounds

The selected tightening

```
t=sigma min{1/2,(epsilon/(2D))^q}
```

satisfies `D(t/sigma)^(1/q)<=epsilon/2`, including when `epsilon/(2D)>1`.
Its rational bit length is polynomial in the encodings and numerical `q`; a
polynomial claim in the binary length of unrestricted `q` alone is not made.
Promise (M) forces nonempty tightened sets and supplies the missing objective
comparison. It is a substantive assumption and is not treated as an oracle the
algorithm can automatically verify.

The posterior interval is valid without trusting (M). If `m_out` is the exact
outer surrogate minimum, then

```
h_out-omega_out-A_0 rho_out <= m_out-A_0 rho_out <= V(0).
```

The inner recovered leader is exactly feasible, and its true objective is at
most `h_in+A_0 rho_in`. These give the asserted rational lower and upper bounds.
If both procedures return, the inner point itself supplies the needed original
feasibility premise. Outer convergence follows from compactness, response
continuity, vanishing row violations, and vanishing objective errors. Inner
convergence additionally needs `V(t)->V(0)`; the note states this distinction.

The explicit response modulus in Lemma 4 is sound. Two Hoffman repairs introduce
`2LKB_b h`; changing the affine incentive contributes at most `B_ell h` because
both response vectors are in the unit cube. Uniform polynomial convexity bounds
the displacement of the repaired point from the true optimum. Since
`h<=h^(1/(P+1))` and `a^(1/(P+1))<=max(1,a)`, the rational overestimate `C_z`
is valid even when `T=0`. Convex interpolation toward the supplied strict anchor
therefore proves the asserted tightening modulus without requiring objective
convexity. Convexity of the reduced rows is expressly an extra promise.

The reserve construction is valid without convexity of reduced feasibility in
the other leader coordinates. Reserves leave the complete follower problem
unchanged; interpolation toward a uniformly safe reserve transfers the margin
linearly and changes the affine objective by at most `||w||_1 t/sigma`. The
stronger proposed LP certificate is conservative but valid. An artificial slack
would change the modeled problem; the note explicitly excludes that interpretation.

## Convex aggregate composition and nonlinear branch crossings

Section 11 uses the correct recovery interface from the aggregate theorem. The
candidate winner `v*` has valid inverse branches. Rational recovery preserves
only its enclosing rational polytope and may invalidate those branches.
The error comparison correctly follows

```
p(v*) -> q(v*) -> q(vhat) -> z(xhat),
```

with errors `eta`, `eta`, and `tau`, respectively. For affine upper data this
gives `||a_j||_1 h+||c_j||_1(2eta+tau)`. It does not evaluate the selected branch
polynomial at `vhat`. Imposing `h,eta,tau<=kappa` alongside the inherited residual
requirements is permissible and adds only polynomially many accuracy bits.
With `A` bounding both leader and response coefficients, the bound is at most
`4A kappa<=min(epsilon,delta)/4`.

True lifts have upper error at most `||c_j||_1 eta`. Consequently outer lifts,
inner tightened lifts, recovered feasibility, and objective comparisons have
the stated slack. The posterior bounds now use rational approximations to the
algebraic surrogate winner, rather than invalid branch evaluation at the rounded
point. Subtracting the approximation error and lift error gives the outer lower
bound; adding approximation error and the recovery bound gives the inner upper
bound.

The aggregate response modulus also composes correctly. Bounding objective
variation at fixed follower vector by `T_x h`, then making two feasible-fiber
repairs, gives cost loss at most `2(T_x+LKB_b)h`. Convex aggregate Bregman
divergence is nonnegative, so the existing local-cost modulus `mu` still controls
response displacement. Neither aggregate strong convexity nor invertibility of
a KKT matrix is introduced. The reserve corollary requires the aggregate cost,
as well as all other follower data, to be reserve-independent; this is explicit.

## Polynomial upper objectives and rows

Section 12 is a valid closure of the construction. On the enlarged response box
`[-1,2]^N`, summing the absolute partial derivatives gives

```
L_x=sum |a_(alpha,beta)| |alpha|_1 2^|beta|,
L_z=sum |a_(alpha,beta)| |beta|_1 2^|beta|.
```

The second constant is deliberately loose by a factor of two on nonconstant
response monomials, hence safe. The separate infinity-norm Lipschitz constants
remain valid for mixed signs, products across many follower coordinates, and
slightly out-of-box polynomial inverse values. Their logarithms are polynomial
in the explicit data and numerical upper degree. Zero constants for absent
variable groups or constant polynomials cause no division problem because all
precision ledgers take a maximum with one.

Substitution into an explicitly listed upper monomial raises its degree to at
most `D_up max(1,d_p)`. Expansion has polynomially many possible monomials because
the compressed ambient dimension stays fixed, irrespective of follower count.
Successive multiplication increases coefficient bit lengths polynomially in
numerical `D_up` and the supplied inverse-polynomial coefficient lengths. This
does not justify unrestricted sparse binary degrees, which the statement excludes.

For resource-only recovery the selected branch remains valid at `vhat`, so the
original polynomial-rounding argument and replacements `A_j=L_z(G_j)` suffice.
For aggregate recovery the valid comparison is instead

```
|G_j(xhat,z(xhat))-G_j(x*,p(v*))|
 <=L_x(G_j)h+L_z(G_j)(2eta+tau).
```

The leader and response line segments stay in the boxes on which the derivative
bounds hold. Thus nonlinear upper substitution does not reintroduce the invalid
`p(vhat)` evaluation. True-lift errors are `L_z eta`, and the existing outer,
inner, posterior, and convex-anchor ledgers transfer with the stated replacements.

The polynomial reserve extension requires convexity only as a function of the
reserve, with the complete follower unchanged. That convexity yields the margin
under interpolation, while `L_s(H)` bounds its objective cost. The objective need
not be affine or convex. These are explicit structural promises, not conclusions
drawn from lower-level convexity.

## Boundaries, zero cases, and verification

The two exact negative examples are correct. The strongly convex inverse model
has feasible set `{0} union [1/2,1]`, and positive tightening discards the isolated
global optimum despite another strictly feasible point. The square-root equality
has precisely the two irrational feasible leaders `3/8 +/- sqrt(2)/4`; squaring
introduces no extra root because both sides are nonnegative. Therefore a generic
Slater-only argument and unrestricted exact rational feasible output are invalid.

The note correctly distinguishes response-free and response-independent-objective
cases. With no follower variables the affine problem is an LP; polynomial upper
data instead require fixed-dimensional polynomial optimization and the same
margin qualifications for exact rational upper feasibility. A response-independent
objective cannot trigger the base LP shortcut when any upper row still depends
on the response. A constant objective causes no undefined precision constants.
With no upper rows, there is no tightening obstruction; arbitrary polynomial upper
objectives retain the original additive guarantee and exact membership in `X'`.
Upper polynomial equalities do not acquire an unjustified positive margin.

No duplicate diagnostic script was added: the existing
[exact checks](../code/bilevel_reopened/response_constraints_checks.py) already
test the negative examples, unrelated objective/constraint error scales, reserve
interpolation, and separate upper-polynomial Lipschitz bounds on the enlarged
response box. This review supplies the independent general proof verification
that those finite checks cannot provide.
The reviewer reran that script: all 4,553 exact diagnostic cases passed.

The result is ready for promotion after integration with the other independent
review and the explicitly conditional aggregate dependency. Practical solver
performance and unrestricted exact feasibility are not established or claimed.
