# Independent review of polynomial tubes and slab-dependent affine supports

Date: 2026-09-12. Reviewer: fresh subagent `polynomial_tube_review`.
Status: accepted within the exact polynomial and valid-metadata scope below.
No remaining validity defect was found. Two implementation improvements were
made by root during review: coordinatewise inflation and certificate metadata
checks. The reviewer did not edit the implementation or the literature knowledge
base. This review makes no originality or competitive-performance claim.

Reviewed components:

- [polynomial_tubes.py](../code/research_20260912/polynomial_tubes.py), SHA-256
  `d63671bbf406fe2494c4a17586d335d11e58948d7604cf284f4795b763c91348`;
- tube composition and `round_physical_supports` in
  [ode_support_experiment.py](../code/research_20260912/ode_support_experiment.py),
  SHA-256 `b7c71d171ab5c143ef3206b85002cba5bf08f8823d929165d3e8befdf499c137`;
- the proof in
  [validated-polynomial-tubes.md](research-20260912-validated-polynomial-tubes.md).

The independently reviewed
[support compiler](research-20260912-ode-theory-independent-review.md) and
[rational affine-flow integrator](research-20260912-rational-flow-independent-review.md)
remain separate prerequisites. This review checks their composition with the
new tubes and the new support-rounding step; it does not repeat their full
internal audits.

## Exact arithmetic and the one-step proof

The interval operations use `Fraction` throughout. Addition and negation are
exact. Multiplication takes the minimum and maximum of all four endpoint
products and therefore encloses every real product. Model dimensions and exact
scalar types are checked by `PolynomialModel`; interval construction rejects
reversed endpoints. Constants supplied as floats are rejected by the exact
arithmetic path. These restrictions do not make an arbitrary Python callable a
polynomial: the caller must supply a genuine polynomial expression using the
supported arithmetic. Branching or a custom function with different scalar
and interval behavior is outside the certificate contract.

On a slab, let `Y` contain the initial states and let the raw box `B` pass

\[
Y+[0,h]f^I(P,B)\subset\operatorname{int}B.
\]

Every individual polynomial ODE has a unique local solution. At a hypothetical
first boundary contact before time `h`, integration of its bounded derivative
places the state in the displayed strict interior, a contradiction. The image
is compactly inside `B`, and bounded derivatives exclude an obstruction to
continuation while the solution stays there. Thus the solution exists across
the whole slab and stays in `B`. A separate contraction-mapping test such as
`h*L < 1` is unnecessary for this first-exit argument.

It is essential that the RHS is evaluated on the raw candidate box during this
test. Using a contracted physical box to assert raw existence would require
an additional argument. The implementation contracts only after raw strict
inclusion has succeeded.

Once a contracted box `C` is established to contain the physical trajectory,

\[
x(t+h,p)\in Y+h f^I(P,C)
\]

follows from the integral of the derivative over the whole slab. This is a
slope enclosure using a validated tube, rather than a forward Euler step
without a remainder. The contracted tube need not satisfy strict inclusion:
a physical trajectory may lie on its nonnegativity or conservation boundary.

For each slab, the implementation records the initial box, raw box, raw RHS,
strict Picard image, contracted box and RHS, unrounded endpoint image, and
final endpoint. Consecutive records use exactly the previous endpoint as the
next initial box. These records expose the mathematical checks, although a
record alone does not authenticate the Python RHS or prove its physical
metadata.

## Physical and parameter-dependent invariant contraction

Intersection with a valid physical box preserves the trajectory. For a row

\[
\sum_k a_kx_k=b+\sum_rD_rp_r,
\]

the implementation forms an interval for the right-hand side, subtracts the
other coordinates, divides by the nonzero rational pivot, and intersects the
result with the current coordinate. Each update contains every physical state
that the previous box contained. Gauss–Seidel use of earlier updates remains
sound by induction; neither a fixed point nor a joint LP is required.

Allowing `b + D p` to depend on parameters is sound. Replacing its dependence
by an interval discards correlation but includes every relevant value.
Parameter/state correlation is not silently assumed independent in a way
that excludes a feasible value. Negative pivots are handled by exact interval
multiplication and therefore reverse endpoints correctly.

The initial affine state is first evaluated over the parameter box, then
contracted by the same physical metadata. Thus validity of that metadata is a
real assumption even before the first slab. The implementation detects an
empty intersection but cannot detect every false invariant or bound whose
intersection happens to remain nonempty. The error reports are appropriately
diagnostic; they are not certificates of process infeasibility.

After computing an endpoint image, `_round_outward` uses exact floor and
ceiling on a rational grid. The lower endpoint moves down and the upper
endpoint moves up, including for negative numbers. Each move is less than
`1/denominator`. Physical/invariant contraction and intersection with the
already proved tube then preserve endpoint validity. Their order does not
create a circular proof.

## Inflation, failure, and precision limits

The positive margin is multiplied by the time step. It permits strict
inclusion for a singleton equilibrium without adding a fixed state-width
floor. Initially all radii are positive. After a failed attempt, the reviewed
implementation doubles only coordinates whose inclusion test fails; every
coordinate is rechecked after the RHS is reevaluated. A change in another
coordinate can therefore cause a previously successful coordinate to be
enlarged on a later attempt. No successful final test is inferred from an
earlier test.

The first version doubled every radius together. The independent polynomial
example

\[
\dot x=1,\quad\dot y=2x,\quad(x(0),y(0))=(0,0),
\quad (x(t),y(t))=(t,t^2)
\]

failed with 40 slabs on `[0,1]` under its default margin. Joint inflation kept
the unfavorable ratio between the initially nonzero and zero-rate coordinate
radii. Root changed the rule to coordinatewise inflation; the example now
passes with the original default settings. Both rules were sound when they
returned a certificate. This was a needless validation failure, not an
incorrect enclosure.

The cap still permits failure on a coarse mesh even when the physical solution
exists. For example, `x'=-x`, `x(0)=1`, has a bounded solution, yet a single slab
of length 2 fails this box-inclusion construction. A failed tube attempt must
not prune a branch as infeasible. `TubeFailure` reports the slab and final
attempt rather than returning a partial certificate. The independent check
also confirms explicit failure for `x'=x²`, `x(0)=1`, on a horizon reaching its
pole. That latter test uses a deliberately invalid global physical bound to
exercise failure; it is not an admissible model instance.

The note's width recurrence is correct for the actual interval expression.
On bounded boxes, write

\[
w(f^I(P,C))\le L_xw(C)+L_pw(P),\qquad
w(B_j)\le W_j+\nu h_j.
\]

The endpoint update then satisfies

\[
W_{j+1}\le(1+L_xh_j)W_j+L_ph_jw(P)+L_x\nu h_j^2+\delta_j.
\]

Contraction cannot enlarge any width. Summation and the discrete Gronwall
bound give the note's equation (9). The constants must bound the interval
expression, not just the derivative of a simplified real expression; `x-x`
is the elementary counterexample to the latter shortcut. Bounded seed rates
and a fixed inflation cap give a uniform finite `nu`, including with
coordinatewise doubling. Uniform continuity of the interval polynomial on
compact domains and the strictly positive rate margin also prove first-attempt
success for all sufficiently small steps.

A fixed endpoint denominator preserves validity but does **not** prove
convergence as the time step tends to zero. The following example is exact:

\[
\dot x=1/3,\quad x(0)=0,\quad K=[0,1],\quad T=1,
\]

with `inflation=0`, `margin=1/3`, and `grid_denominator=1`. For every number of
steps `N >= 2`, induction gives

\[
Y_j=[0,2j/(3N)],\qquad Y_N=[0,2/3].
\]

Indeed the radius is `2/(3N)`. The unrounded next endpoint has lower endpoint
`1/(3N)` and upper endpoint `(2j+1)/(3N)`. Rounding gives `[0,1]`, whose
intersection with the next raw tube yields the stated `Y_(j+1)`. Strict raw
inclusion holds at every step. The true final value is `1/3`, so the width
does not shrink. With rounding disabled, every endpoint is the exact singleton
`j/(3N)`. The script verifies both statements for `N=2,3,10,40,100`.

On a uniform grid, endpoint rounding adds less than `2/denominator` to each
component width per step. The sufficient precision condition is therefore
`h*denominator -> infinity`; denominator of order `h^-2` or larger retains
the first-order width bound. Separate support-slope and affine-flow rounding
also require precision control for claims about affine-cut convergence.
Their fixed precision does not affect the validity claim, and retaining the
convergent interval objective bound supplies the note's separate consistency
safeguard.

## Slab-dependent support composition and slope rounding

For each validated slab box `X_j`, the driver creates a model with that fixed
box, compiles affine minorants, and propagates their linear system. The signed
physical state `z=(x,-x)` satisfies the required inequality on that slab.
Continuity carries the comparison inequality across every known slab
boundary. There is no need to posit a single time-independent nonlinear RPD
field for the whole horizon.

The floating matrix exponential updates only the reference used to choose
valid pieces. It is not reused as the certified final state. The exact
linear-flow component separately bounds its coefficient error and shifts
the final affine functions downward. Neither the reference nor the affine
lower state has to remain within the physical tube.

The initial driver accepted a tube certificate with mismatched metadata or
time grid. The `run_case` path supplied matching data, but external reuse of
the helper could silently apply a tube on the wrong interval. Root added
checks for the horizon, step count and slab count, each slab start/duration,
parameter box, original physical box, affine initial coefficients, and all
invariant metadata. The independent script tests eleven such mismatches.
These checks prevent accidental reuse; the caller must still establish that
the certificate refers to the same RHS. An arbitrary callable's mathematical
identity cannot be inferred from these data fields.

The new slope-rounding operation is sound. Let an original affine row be

\[
r(p,z)=d+Ap+Bz,
\]

and let `Ahat,Bhat` be its nearest-grid slopes. With `z=(x,-x)`, the exact
maximum increase over `P × X` is

\[
E=\sum_k\max_{p_k\in P_k}(\widehat A_k-A_k)p_k
 +\sum_i\max_{x_i\in X_i}
 \big[(\widehat B_i-B_i)-(\widehat B_{n+i}-B_{n+i})\big]x_i.
\]

Every maximum is attained at an interval endpoint. Choosing the rounded
intercept no larger than `d-E` gives `rhat(p,(x,-x)) <= r(p,(x,-x))` throughout
the physical box. The implementation computes `E` exactly and floors the
intercept. `E` may be negative on a box excluding the origin; increasing the
intercept in that case is still justified by the same inequality.

Nearest-grid rounding of a nonnegative coefficient is nonnegative, so the
rounded state matrix stays Metzler. Although the rounded row need not bound
the full extended RPD field away from the physical manifold, it bounds the
physical derivative. If `ell'=Bhat*ell+Ahat*p+dhat`, then
`(z-ell)' >= Bhat*(z-ell)`, which proves the desired comparison without
evaluating the nonlinear inequality at `ell`. The driver's restricted
description is consequently the correct one.

## Independent evidence and reproducibility

The new standalone
[polynomial_tube_independent_checks.py](../code/research_20260912/polynomial_tube_independent_checks.py)
uses exact closed-form trajectories for nonlinear Riccati/decay ODEs,
an autonomous polynomial lift, and a three-state affine system with
parameter-dependent invariants and negative pivots. It also checks complete
tube-to-support-to-rational-flow composition, including coarse support
denominators 1 and 7. Run it with:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/polynomial_tube_independent_checks.py
```

The [saved exact-check report](../code/research_20260912/results/polynomial-tube-independent-review.json)
records source hashes and the following passing checks:

- 12,288 interval arithmetic corner checks;
- 4,158 outward-rounding checks, including negative values;
- 14,172 exact analytic trajectory/enclosure comparisons;
- 634 exact strict-inclusion coordinate checks;
- 25 invalid-input, coarse-grid failure, and metadata-mismatch checks;
- 640 end-to-end exact affine-bound comparisons with known physical solutions;
- 15,360 exact physical-manifold corner inequalities for slope rounding.

The original embedded diagnostics also passed on rerun: 300 strict-inclusion
slabs, 1,500 floating trajectory samples, an equilibrium, and an explicit
failure. The floating trajectory samples are diagnostics, not the certificate.

Finally, all eleven saved cases in `ode_singleton_tubes.json`,
`ode_quarter_tubes.json`, and `ode_rounded_tubes.json` were replayed. The
660 tube records and corresponding compiled affine supports match exactly,
and evaluation of the serialized final rational coefficients matches the
saved nominal values. The
[saved-record audit](../code/research_20260912/results/polynomial-tube-saved-record-audit.json)
identifies each case. This replay did not rerun the expensive final rational
linear integration for every stored case; that component has its separate
proof and independent review, and the new exact composition tests exercise it.

The code remains a restricted research prototype. It does not validate
arbitrary physical metadata, unknown switching times, nonsupported RHS
primitives, nonlinear objective incumbent feasibility, or a complete MINLP
branch-and-bound method. The reviewed results establish correct enclosures
and their supporting-flow composition, with the precision and failure limits
stated above.
