# Adversarial review: growth under random linear perturbations

Date: 2026-10-02.

Scope: the compact-domain growth argument and its rational-grid extension for
quadratic objectives on continuous boxes, mixed boxes, and bounded continuous
rational polytopes. The
[main draft](../new-direction/smoothed-linear-growth.md) was read and checked
against the arguments below. This review checks correctness and scope; it
makes no novelty claim.

## Verdict

The compact-domain argument is valid for a continuous objective on a nonempty
compact set in `[-R,R]^n`, with `R > 0`, and independent perturbation coordinates
whose densities are bounded by `phi`. The claimed constant
`g = rho/(48 n^2 phi R)` is safe. For continuous uniform perturbations in
`[-sigma,sigma]`, this becomes `g = rho sigma/(24 n^2 R)`.

The rational-grid extension for continuous and mixed box quadratic programming
is also valid with
the component count and sampling convention given below. Its safe constant is
`g = rho sigma/(48 n^2 R)`. These are global quadratic-growth bounds for the
**perturbed objective**, on an event of probability at least `1-rho`.

The argument does not establish an expected-runtime bound. A work bound valid
on an event of probability `1-rho` remains a high-probability statement unless
the work on the complementary event is separately controlled.

## Compact-domain proof details

Fix all perturbation coordinates except coordinate `i`. Let `u(t)` be the
largest coordinate `i` among minimizers at scalar tilt `t`. Compactness gives
existence. Comparing optimality inequalities at two tilts proves that `u` is
nonincreasing, and its total variation is at most `2R`.

Compact optimizer subsequences show that `u` is left-continuous. Its right
limit at `t` is the smallest coordinate `i` among minimizers at `t`. Thus finite
anchored maximal slope

`M(t) = sup_{s != t} |u(s)-u(t)| / |s-t|`

excludes a spread in coordinate `i` among minimizers. If this holds in every
coordinate, the minimizer is unique.

The response is jointly upper semicontinuous in all perturbation coordinates:
limits of optimizing points remain optimizing, and their coordinate values
cannot exceed the maximum at the limiting parameter. In particular it is
Borel measurable. Left continuity allows the supremum defining `M` to be
taken over rational `s`, by approximating each real `s` from below. For a fixed
rational `s`, define the quotient as zero when `s=t`. This gives a countable
Borel supremum and justifies conditional integration and the union bound.

### An elementary weak bound, including atoms

Let `mu` be the finite positive measure satisfying
`mu([a,b)) = u(a)-u(b)` for `a < b`. Its mass is at most `2R`.
If `M(t)>K`, a closed segment joining `t` and a witness `s` has mass greater
than `K` times its length. Enlarge the segment slightly to an open interval
with the same strict inequality. Let `O` be the union of all open intervals
whose mass exceeds `K` times their length.

For any compact subset of `O`, choose a finite interval subcover. Repeatedly
retain a longest remaining interval and discard all intervals intersecting
it. The retained open intervals are disjoint, and every discarded interval
lies in the triple dilation of its retained interval. Therefore the compact
subset has length at most `3 mu(ℝ)/K`. Inner regularity gives

`Leb{M>K} <= Leb(O) <= 6R/K`.

The proposed weaker bound `12R/K` is consequently safe. Using open intervals
in the selection avoids counting an endpoint atom twice. This proof covers
arbitrary scalar tilts, jumps, and unbounded support of the perturbation law.

### Growth inequality

On the event that all coordinate maximal slopes are at most `K`, let `x*` be
the unique minimizer and fix a competitor `x`. For a coordinate difference
`d = x_i-x*_i != 0`, use
`h = -sign(d) |d|/(2K)`. Choose an optimizer `y` at the shifted tilt whose
coordinate is the maximum response `u(b_i+h)`. This choice makes
`|y_i-x*_i| <= K|h|` immediate; it is enough to choose this one optimizer.
Optimality gives

`F_b(x)-F_b(x*) >= h(y_i-x_i) >= d^2/(4K)`.

Choosing the largest coordinate difference gives global Euclidean quadratic
growth with constant `1/(4nK)`. Conditional density bounds and the safe weak
constant give failure probability at most `12n phi R/K`. Setting
`K = 12n phi R/rho` proves the claimed compact-domain result.

## Finite-grid box-QP extension

Let `F = 3^n` and `B = (F+1)^2`. With all other tilt coordinates fixed, the
maximum-coordinate optimizer response has at most `B` affine pieces.

To see why positive-definite free-face candidates suffice, start with an
optimizer maximizing coordinate `i`. Its free Hessian is positive semidefinite.
If singular, a kernel direction preserves the quadratic objective while
remaining in the face. Every such direction has zero coordinate `i`;
otherwise one sign would increase that coordinate and contradict maximality.
Move along a nonzero kernel direction to the boundary and repeat. This
terminates at a face with a positive-definite free Hessian, or a vertex.
Vertices are included as faces with no free variables.

Each such face has one affine stationary-point candidate in the scalar tilt,
a quadratic objective score, and a feasible parameter interval. There are at
most `2F` finite feasibility endpoints and `F(F-1)` roots of nonidentical
pairwise quadratic score differences. Identically equal scores require no
additional crossings: the score derivative is precisely the candidate's
coordinate `i`, so the selected-coordinate affine functions are identical.
There are at most `F^2+F+1 <= B` open cells. Left continuity extends each
formula to its right endpoint. Thus `B` counts affine pieces with their
appropriate endpoints; it must not be described as counting both open cells
and additional singleton breakpoint pieces.

### Number of bad-set components

Write the response using `m <= B` affine pieces. On an open piece where
`u(t)=a t+c`, the maximal slope is the maximum of `|a|` and at most
`2(m-1)` expressions

`|v-a t-c| / |e-t|`,

where `e` is a finite breakpoint and `v` is one of its two limiting response
values. For scalar `s` in any other affine piece, the absolute secant slope
has its supremum at an endpoint limit. Infinite endpoint limits are zero
because the response is bounded.

On the current open piece, the sign of `e-t` is fixed. Each displayed
expression exceeds `K` on a union of two strict affine inequalities, with at
most two threshold locations. The bad set consequently has at most `4m-3`
interval components within each open piece. Adding the at most `m-1`
breakpoints as possible singleton components gives at most
`4m^2-2m-1 <= 4B^2` components. This bound covers jumps and equality cases.

### Grid spacing and constants

Use `M >= 2` equally spaced **points**, including both endpoints of
`[-sigma,sigma]`. Their spacing is `2sigma/(M-1)`. A set of length `L` with
at most `C` interval components, including singleton components, contains
at most `L(M-1)/(2sigma)+C` grid points. Its sampling probability is therefore
at most `L/(2sigma)+C/M`. There is no multiplicative `M/(M-1)` loss with
this convention.

With independent coordinate samples, choose

`K = 12nR/(rho sigma)`, and `M >= 8nB^2/rho`.

The safe weak bound contributes at most `rho/(2n)` per coordinate, and the
component correction contributes at most `rho/(2n)`. A union bound gives
failure probability at most `rho` and growth constant
`rho sigma/(48n^2 R)`.

For rational input and rational `sigma`, take `M` to be a power of two above
the stated bound. Sampling is then exact using `log2 M` random bits per
coordinate, and each perturbation is rational with bit length
`O(bits(sigma)+n+log n+log(1/rho))`. The exponential candidate count is used
only to bound the required grid size; the proof does not call for enumerating
the faces. This is a finite-bit sampling result, not an efficient method for
finding the global minimizer.

## Mixed-box candidate and bit bounds

The draft's mixed-box extension is valid. For each integer assignment, apply
the candidate reduction to the continuous coordinates and their box faces.
The count becomes `F = 3^(n_c) product_j N_j`, where `N_j` is the number of
allowed values of integer coordinate `j`. Empty integer domains must be
rejected first, as the draft specifies.

For a tilt in a continuous coordinate, the continuous-face argument applies
unchanged. For a tilt in an integer coordinate, each fixed-assignment
candidate is constant in that parameter, and the derivative of its affine
score is its fixed integer coordinate. Thus the identical-score argument,
affine-piece bound, component count, and grid calculation all still apply.
Noise must be supplied independently in every coordinate, including the
integer coordinates.

Bounded rational box endpoints imply that each `log N_j`, and hence
`log F = n_c log 3 + sum_j log N_j`, is polynomial in the encoded input
length. The sampling index and rational perturbations consequently use
polynomially many bits. The integer assignments need not be enumerated for
this sampling construction. The metric in the growth inequality can include
both continuous and integer coordinates because its proof was already valid
on an arbitrary compact feasible set.

## Additional audit: coordinate widths and continuous polytopes

Sections 10–11 of the main draft pass the additional audit. If `W` is the
largest coordinate range, subtracting each coordinate's midpoint places the
feasible set in `[-W/2,W/2]^n`. Linear perturbations acquire only an additive
constant; objective gaps and Euclidean distances do not change. Substituting
`R=W/2` therefore gives the rational-grid growth constant
`g0 = rho sigma/(24n^2 W)`, and the continuous uniform-noise constant is
`rho sigma/(12n^2 W)`. Removing constant coordinates handles `W=0` as the
singleton case. For integer coordinates the translation is a proof device,
as the draft explicitly states, and does not change the model's integrality
convention.

A polytope described by `m` supplied inequalities has at most `2^m` nonempty
faces: the inequalities tight throughout a face determine that face. This
argument allows redundant inequalities and lower-dimensional polytopes.
At an optimizer maximizing the selected coordinate, the smallest containing
face has a positive-semidefinite tangent Hessian and zero tangent gradient.
A null direction of the restricted Hessian preserves the quadratic objective
on its feasible segment. It must preserve the selected coordinate as well,
since otherwise one locally feasible sign would increase that coordinate.
Boundedness ensures the segment reaches a proper face. Repetition gives a
positive-definite tangent Hessian or a vertex.

Every face with positive-definite tangent Hessian consequently supplies one
affine stationary candidate in the scalar tilt. Its feasible parameter set
is an interval, its score is quadratic, and differentiating its score gives
the selected coordinate because the candidate derivative is tangent to the
face. Thus identical score polynomials again have identical response
coordinates. The previous piece and component bounds apply with `F=2^m`
and `B=(F+1)^2`. The required grid therefore has
`log2 M = O(m+log(n/rho))`, so both exact sampling and rational perturbation
encoding use polynomially many bits. Rational linear programs compute the
coordinate ranges with polynomial bit complexity. No face enumeration is
required by the sampler or by this counting argument.

The corollary substitutes the right conditioning parameter from the
[negative-inertia theorem](../new-direction/negative-inertia-qp.md):
`max{1, nu/g0} <= max{1, 24n^2 W nu/(rho sigma)}`. Linear perturbations do not
change negative inertia or `nu`. Although the theorem states its general
complexity using a parameter function, its displayed cell count is
polynomial in the conditioning parameter for fixed negative inertia `k`.
The number of refinement levels and the exact convex-QP arithmetic have
polynomial bit bounds. These details justify the draft's fixed-`k`
polynomial-work consequence when `W`, `nu`, `sigma^-1`, and `rho^-1` have
polynomial numerical bounds. Large positive curvature contributes to input
length and preprocessing precision rather than to this conditioning ratio.

This extension remains a high-probability result for the perturbed
continuous polytope QP. It neither bounds expected work nor supplies a
polynomial-time mixed-integer convex-QP oracle. The audit checked the
interface and explicit packing dependence of the previously reviewed
negative-inertia theorem; it did not repeat that theorem's internal proof.

## Draft reconciliation, limits, and verification

The main draft uses a centered-interval covering proof, giving the safe
constant `12R/K` directly. The stronger constant in this review is optional;
the draft's stated constants require no change. The draft also uses
monotonicity to reduce each component comparison to one affine inequality,
which is valid and improves the intermediate count without changing the
safe bound `4B^2`.

The draft correctly distinguishes high-probability work for the perturbed
objective from expected running time and exact recovery for the original
objective. Its solver consequence depends on the separately established
pruned-grid theorem, including that theorem's certificate validity outside
the growth event. This review checks the growth and sampling inputs to that
consequence; it does not re-prove the solver theorem.

The compact-domain theorem by itself does not imply a rational-grid result
for every continuous objective. Atoms can hit ties, and the box-QP argument
needs its finite affine-piece bound to control that risk. The mixed-box
count above supplies that bound for the mixed domain in the draft. More
general mixed-integer feasible sets require a separate argument.

The review used direct mathematical checks of the conditional-response,
covering, candidate, component, and spacing arguments. No executable test or
project-wide verification was run, and no CI status or logs were inspected.
The targeted whitespace command
`git diff --no-index --check /dev/null research-20261002/reviews/smoothed-linear-growth-adversary.md`
produced no whitespace diagnostics; its exit status was 1 because the new
file differs from `/dev/null`.
