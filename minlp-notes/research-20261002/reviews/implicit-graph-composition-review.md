# Independent review of the implicit-graph composition

Date: 2026-10-02. Verdict: passed for the stated global scalar-graph
premises and fixed-degree encoding. The coordinating researcher read the
complete [main theorem](../new-direction/smoothed-implicit-graph-constraints.md)
and [oracle proof](../new-direction/implicit-graph-oracle-interface.md),
independently of their authors, and rederived the interfaces below.
This is a mathematical review, not external peer review or a priority claim.

The model retains a product box in the anchor coordinates. Each dependent
coordinate is the unique scalar root throughout that box's real hull,
including between integer labels. The derivative floor applies throughout
its dependent interval. These global assumptions justify bisection,
implicit derivatives, and midpoint queries before integers are fixed.
Local root brackets alone would not justify the theorem. The final text
explicitly charges verification of supplied global certificates, or states
the result under valid premises. It does not supply a general polynomial
positivity algorithm.

Replacing a dependent variable by its retained support preserves running
intersection: its original occurrence subtree meets every relevant anchor
subtree in a constraint bag. The expanded scopes cover both objective
factors and dependent-coordinate noise. Conditioning on all dependent
noise leaves the original independent anchor coefficients intact. The
curvature and derivative bounds must hold uniformly before this
conditioning, as required in the theorem.

The approximate DP has the correct direction of error. If total lower-cost
error is at most `D<=E`, rounding gives `m^-<=f*+E`. Its attached implicit
feasible witness has upper bound `m^-+D`. Retention with `q_C^- - E<=U`
preserves every optimizer and supplies a single consistent witness of
true gap at most `2E+2D<=4E`. Thus the coefficient interval is
`La+8E/a`, giving the displayed `1+n` factor. No product of independently
selected block witnesses or conditioning on prior pruning is used.
Per-row precision and rational summation have polynomial bit overhead.

The closure test correctly includes both derivative approximation errors.
On the good event the gradient interval differs from the optimal gradient
by at most `2M_1 r+2 epsilon_g<=3 tau/4`. After original active bounds
and integer labels are fixed, two-sided retained directions give Hessian
at least `2g_0 I` at the optimizer. The accepted rational matrix test has
remaining slack at least `g_0-2Tr-2 epsilon_H>=g_0/4` at the cutoff.
The bounds concern the reduced Hessian, not the ambient objective Hessian.
No lower bound on inactive-coordinate slack is hidden in the argument.

The graph-assisted growth formula retains exactly two quantified blocks.
Its scalar-section complexity depends on degree and format, not on the
realized coefficient heights. For an original retained face, the
polynomial KKT system has `k+2m` variables. Invertibility of `q_y` makes
every tangent vector equal to `[I;-q_y^-1 q_u] du`. Its reduced Hessian
is positive definite at a positive-growth optimizer, so the bordered
Jacobian has no kernel. Only those nonsingular roots are counted;
other components may be positive dimensional. An active anchor's own
coefficient is absent from this face system and enters its derivative
with slope one. The finite-law margin bound therefore does not assume
independence after conditioning on good growth. The stated fixed degree
`D=max(2,d_F,max_j deg q_j)` safely bounds all KKT equations.

Exact fallback is applied to the original polynomial graph domain.
Replacing it by an explicitly encoded reduced polynomial would be wrong
because that reduced function can be algebraic. The two-block canonical
optimizer formulas instead retain the graph variables and preserve the
base-exponential, sampled-height-polynomial bound. Consequently the
sampling precision is chosen after a base-only cutoff, with no circular
dependence on sampled denominator sizes. Both failure terms are at most
`rho`, and the same-draw fallback costs are paid by `2rho B`.

For a successful patch, the approximate affine tangent with the
`beta diam_1(C)` correction is a valid rational lower plane. Its last
normal coordinate is `-1`, so rational normalization is safe. Failure to
separate proves the required vertical proximity to the epigraph. GLS
weak optimization still requires the documented erosion and feasibility
repair. The algebraic value at a clipped rational anchor is replaced by
a rational upper enclosure with half the requested error budget. This
gives a valid value interval and, through the chart Lipschitz bound,
physical-coordinate accuracy in polynomial precision cost.

The feasibility contract is accurate: a rational anchor plus its unique
root equations represents an exactly feasible physical point. Independently
rounded rational dependent coordinates need not be feasible. Successful
compact descriptions have polynomial size; the complete pruning record
has only the expected-size guarantee. Exact arbitrary threshold comparisons
are not silently inferred from the approximation oracle.

The comparison with the affine-state actuator reduction was clarified
during review. Its adjoint identity can preserve unary reduced scopes
despite a long forward dependency chain. It is a complementary reduction,
not evidence that arbitrary forward elimination preserves the main
theorem's bag-size bound.

This review used full proof reading and independent algebraic derivations.
It did not rerun the separate oracle or KKT diagnostics. Those checks and
the targeted nonlinear DP fixture, when complete, are recorded by their
authors. No project-wide verification or CI inspection was performed.
