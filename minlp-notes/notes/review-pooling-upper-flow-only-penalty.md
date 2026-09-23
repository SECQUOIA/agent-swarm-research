# Independent review: exact penalty removes lower flow bounds

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the exact-penalty reduction passes, including its polynomial
encoding bound and production-cost variant.** This reviews
[the candidate](pooling-upper-flow-only-penalty-hardness.md). Its application
to the separately reviewed scalar-upper-quality cycles is also valid.

## Explicit error bound

For a nonempty closed polyhedron, the Euclidean projection exists even if
the polyhedron is unbounded. At the projection, the displacement belongs
to the cone of active row normals. A conic representation can be reduced
to linearly independent normals by adjusting nonnegative coefficients
along a dependence until one coefficient vanishes. Hence the matrix `B`
in the proof has independent integer rows and at most `N` rows.

Writing the displacement as `h=B^T lambda`, with `lambda>=0`, gives
`||h||_2^2 <= ||lambda||_1 eta`, because active-row displacement equals
the corresponding residual at the original point. Moreover,
`||lambda||_1 <= sqrt(N)||h||_2/sigma_min(B)`. Integer row independence
implies the positive integer `det(B B^T)>=1`. Since every singular value
is at most `NK`, the smallest is at least `(NK)^(-(r-1))`, and therefore
at least `(NK)^(-(N-1))`. The two Euclidean-to-one-norm factors yield
exactly `H=N(NK)^(N-1)`. The proof also covers lower-dimensional
polyhedra, equalities represented by opposite rows, and zero inactive
rows; such zero rows are never selected into the independent normal set.

I checked the primary
[Hoffman paper](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf),
Section 2, for the classical error-bound attribution. The displayed
coefficient-dependent estimate follows from the draft's direct proof;
it is not attributed verbatim to that source.

## Copy subsystem and radial repair

The copy subsystem contains direct gadget flows and actual pool intakes,
but excludes the anchor and primary output arcs. Its output-quality rows
are linear because gadget outputs receive direct input flows only. All
relaxed copy constraints therefore belong to a rational polyhedron.
The exact-contract subsystem is nonempty even when the source polytope
is empty: zero original intake signals and the corresponding complementary
and averaging signals fill every contract. Arc bounds make it bounded.

Retaining all upper bounds makes each contract deficit nonnegative. On
a physically feasible relaxed point, all noncontract inequality residuals
are zero. Clearing their denominators cannot change that fact. The
integer contract rows remain unscaled, so the maximum residual in the
full exact polyhedron is at most the sum of contract deficits. The error
bound thus controls the entire copy vector, and hence its intake vector,
by `H delta`. The integer coefficient bound and `H` have polynomial bit
length despite potentially large numerical values.

For an intake vector with `T=sum x` and `S=sum a_i x_i`, the primary
outlets are feasible exactly when `T<=2` and `S(T-1)-T<=0`. When `T<=1`,
send all pool flow to output 2. When `T>1`, send one unit there and the
remaining `T-1` to output 1; the necessary anchor amount is
`(S/T-1)(T-1)`, and the output capacity is equivalent to the displayed
inequality. This also confirms sufficiency and the anchor capacity.

The gradient bound `|dF/dx_i|<=3a_max+1` holds on the whole convex
nonnegative throughput-two simplex. Projection back to the exact copy
polytope may break outlet feasibility, but only by a controlled amount.
If the projected point violates it, its `T'>1` and `S'>1`. Radial scaling
to throughput `1+T'/S'` restores equality and removes mass exactly
`F(x')/S'`. Thus the repair never divides by a quantity near zero.
Homogeneous source rows survive scaling; the entire copy network can be
rebuilt from the scaled signals. This last step needs only the proved
copy projection property, so it applies equally to the closed-cycle model.

The intake reward changes by at most
`b_max(1+3a_max+1)H delta`, exactly the draft's `C`. For private-input
production rewards, the relaxed reward flow need not equal the intake.
The draft correctly bounds its change during projection in the full
copy vector, uses equality only at the repaired contract point, and
then applies radial rebuilding. The same constant is valid.

## Penalty and model scope

With `M=C+1`, the reward minus `M` times total deficit is strictly below
that of its exact-contract repair whenever the deficit is positive.
Adding the constant `B0=M sum e_j` expresses this as an ordinary linear
throughput objective. Every exact-contract point has zero deficit, so
the optimum is precisely `B0+OPT_contract`. All rows, coefficient bounds,
powers, objective coefficients, and the shifted decision threshold can
be computed with polynomially many bits. No optimal Hoffman constant,
projection point, or optimizer needs to be computed by the reduction.

Each source has at most one contract reward and each gadget output at
most one demand reward. Therefore the common production-cost shift
`D>=M+b_max` suffices. Adding the same unit output revenue cancels by
total mass conservation and leaves all input costs and output revenues
nonnegative. No arc, capacity, or quality specification is added by the
penalty. Every positive lower flow bound can be deleted. This gives
ordinary NP-completeness through the reviewed NP-membership result;
the large penalty prevents a strong-hardness inference.

I independently ran `check_upper_penalty.py --seed 47 --trials 8` and its
scalar-upper-quality version with seed 53 and eight trials. Each run
passed 16 original-network global solves, testing intake rewards and
private-input production rewards. Both negative controls have loose
profit 15 at zero penalty and exact-contract profit `15/2` at penalty
100, with restored deficits within numerical tolerance. Logs:

- [Original quality formulation](../code/pooling_bypass_copy/upper_penalty_independent_review_output.txt).
- [Scalar upper-only quality formulation](../code/pooling_bypass_copy/upper_quality_penalty_independent_review_output.txt).

These moderate-penalty experiments test the assembled physical models
and objective mechanism. They do not numerically validate the enormous
theoretical constant; its validity rests on the independent proof audit.
