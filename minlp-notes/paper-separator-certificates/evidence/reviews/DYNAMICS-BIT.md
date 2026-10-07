# Independent mathematical review: rational dynamics and compressed output

Reviewed the stable manuscript `sections/dynamics-bit.tex` against its actual
`sections/dynamics.tex`, `sections/model.tex`, and
`sections/regridding.tex` dependencies. This review used symbolic arguments,
not computational experiments or the original source-note proofs. No
literature discovery or knowledge-base operations were performed.

## Verdict

The finite-precision dynamics development is mathematically sound. No major
or moderate repair is needed. The full-box component-gradient bound at the
section start correctly supplies the ambient-center derivative condition
identified in the exact-real review. The author has also applied explicit
incumbent initialization in the exact-real theorem.

One optional precision edit: in the conditioned theorem's final statement
about a further state precision, write “rational requested precision
`tau > 0`.” The reference to its binary precision length otherwise already
implies an encoded rational request. This is not a defect in the bound.

## Independent checks

1. **Affine cost realization.** A full three-coordinate leaf midpoint has
   squared radius at most `p w_B^2 / 4`. The gradient-Lipschitz Taylor
   remainder is at most `Mp w_B^2 / 8`; subtracting that rational
   quantity yields a valid affine lower model with error at most
   `Mp w_B^2 / 4`. Thus `A=pM` is correct. Multipliers alter only the
   slopes; the affine cost model remains a model of the original cost.

2. **Local LP dimensions and completeness.** Intersecting a leaf with its
   own separator cell merges coordinate bounds, leaving at most six
   bounds plus two affine strip inequalities. The constant intercepts of
   child messages can be added after choosing a local minimizer. Every
   bounded nonempty rational polyhedron has a vertex, and active normals
   at any vertex span the ambient space. Otherwise a small positive and
   negative common null-direction displacement preserves every active
   equality and every inactive inequality, contradicting extremality.
   Therefore enumerating all independent triples among the at most eight
   constraint rows, at most 56, finds every possible needed vertex even
   when the domain has lower dimension. Exact rational inequality checks
   prove candidate feasibility. Absence of any candidate proves emptiness.
   Elimination of fixed coordinates and the zero-dimensional convention
   supply an equally valid alternative implementation.

3. **Contraction-based enclosures.** Given a state midpoint and radius,
   fixing the retained exact rational control and using `|partial_sigma
   phi| <= a` encloses the next exact state in the interval with center
   `phi(midpoint,control)` and radius `a r_t`. Outward dyadic rounding
   increases half-width by at most one mesh unit; clipping cannot increase
   half-width and cannot lose the true state under box invariance. The
   resulting `r_{t+1} <= a r_t + delta` gives `r_t <= delta/(1-a)`.
   This argument uses function evaluation at one rational midpoint and
   a derivative modulus, rather than an unjustified natural-interval
   contraction claim.

4. **Upper objective bound.** Along the segment from the exact feasible
   bag point to its state-midpoint counterpart, the component-gradient
   bound gives absolute cost error at most `G_b(r_t+r_{t+1})`. Adding
   the same quantity to the midpoint cost produces a valid upper bound.
   Its excess is at most twice the sum of those errors, hence at most
   `4G_b N delta/(1-a)`. The controls are exact and add no error. Adjacent
   states need not have independent enclosures. The selected mesh gives
   both the `omega N h_j^2` objective allowance and midpoint state error
   at most `h_{j+1}/4`.

5. **Reset centers.** The largest prescribed dyadic reset mesh has size
   at most `h_{j+1}/2`; rounding adds at most that quantity. Together with
   the state-enclosure error, every coordinate differs from the repaired
   feasible trajectory by at most `h_{j+1}`. Clipping is nonexpansive
   relative to a point in the interval. Since `2T+1 <= pN`, the squared
   reset error is at most `pN h_{j+1}^2`. Resetting every coordinate,
   including the initial state and controls, is necessary to keep stage
   centers independent of previous LP denominators; the text does so.

6. **Rounded-center recursion.** The arbitrary-center configuration
   bound from the dynamics section applies because the supplied full-box
   gradient bound controls all ambient reset centers. Decomposing
   `y_j-c_j` through the minimizer and the preceding repaired point gives
   `||y_j-c_j||^2 <= 3(e_j+e_{j-1}+pN h_j^2)`.
   Thus growth yields
   `e_j <= (3/17)e_{j-1} + (20C/g+3p)N h_j^2/17`.
   At stage zero the reference trajectory is only a proof device and need
   not be represented or evaluated. Induction is valid because
   `5 B_round >= 20C/g+3p`. The chosen constant
   `B_round=max(p,4(C+omega)/g+3p/5)` supplies this inequality and also
   `g B_round/4 >= C+omega+3gp/20`. The latter gives the stated upper-
   minus-lower gap, including the enclosure error. No shifted center is
   assumed feasible, and no optimality/stationarity equation is used.

7. **Representation bounds.** The largest reciprocal-power-of-two mesh
   qualification prevents accidental choice of an unnecessarily tiny
   mesh. Reset centers have `O(I+j)` bits, and shell coordinates introduce
   at most `O(mu)` extra bits. At fixed arity and numerical degree,
   rational polynomial values and derivatives at these points have
   `O(b_j)` bits. Each adjoint recurrence step multiplies by a fresh
   `O(b_j)`-bit derivative and adds an `O(b_j)`-bit objective derivative,
   so length grows additively through the horizon to `O(T b_j)`.
   Fixed-size LP determinants and objective evaluations have length at
   most this order. A message is a sum of at most one selected local
   contribution per bag, at most `T` such `O(T b_j)`-bit rationals, so
   `O(T^2 b_j)` is a safe denominator/numerator bound. Taking minima
   only selects an existing rational sum; it does not multiply messages.
   This distinguishes the recurrence from exponential nonlinear state
   composition.

8. **Enclosure bit lengths.** The initial singleton and controls are
   bounded-length LP coordinates. Every later enclosure step evaluates
   the polynomial at a bounded-length midpoint and a retained rational
   control, then resets its endpoints to the selected dyadic precision
   or an input endpoint. Consequently nonlinear unrounded rational
   composition never occurs. The precision exponent is
   `O(I+j+log(1+G_b)+log(1/(1-a))+log(1+1/omega))`; all added scales
   have input-sized encodings. Summing rational objective values and
   radii through `T` stages remains polynomial in these lengths.

9. **Conservative rational constants.** For `C_0=6`, the inequalities
   `sqrt(C_0)<=3`, `sqrt(k)<=2`, and
   `sqrt(1+a^2+b^2)<=1+a+b` show that the displayed rational majorants
   dominate `L_q`, `rho`, and `D`. Replacing `D` by the majorant in
   the grading conditions and the derived error constants weakens the
   proof in a sound direction. Squaring the nonnegative square-root
   condition preserves equivalence. The supplied-growth stage estimate
   can be found by exact rational comparison, so square-root evaluation
   is not required by the finite-bit implementation.

10. **Conditioned work and output.** Exact LP basis computations replace
    each oracle call by constant-dimensional rational arithmetic, with
    polynomial costs at the established bit lengths. For the actual
    path separator dimension at most one, the factor `3^q` is a fixed
    constant. The work bound
    `N(4/theta)^3 (J+1)^3 poly(T,I,J,mu)` therefore follows from
    the actual incidence counts. With `omega=1` and `g<=1`, all
    numerical constants and the first sufficient reciprocal ratio are
    polynomially bounded by the stated conditioning bound `K`.
    The assertion is correctly about numerical conditioning, rather
    than a uniform polynomial in its binary encoding. A later arbitrarily
    tiny sufficient ratio would not satisfy the same conditioning-only
    bound; the text explicitly qualifies the polynomial statement to
    the first sufficient or conservative-test ratio.

11. **Compressed feasible output and its checker.** The retained rational
    initial state and controls, together with the original recurrence,
    define an exact feasible trajectory by the invariance promise.
    A rational upper bound belongs to those inputs, even if a later
    center is obtained by rounding different data. The incumbent stores
    the inputs associated with the least upper bound. The lower
    certificate checker can reproduce local LP enumerations, finite
    messages, and empty-state flags; the upper checker can reproduce
    contraction enclosures. Global derivative bounds and invariance
    remain explicitly supplied promises or separately verified facts.
    Growth is unnecessary to check certificate validity or the returned
    gap.

12. **Unknown-growth budgets.** Every grading trial uses valid original
    models and strips and accepts only a verified rational gap. The
    trial code uses none of `g`, `C`, `B_round`, or the stopping-stage
    estimate. For the smallest sufficient index, the displayed reciprocal
    threshold `R` is exactly the maximum obtained by solving the three
    grading inequalities, and `2^mu* <= 2R`. This bounds its index
    polynomially/logarithmically in numerical conditioning. A round with
    `r*=max(mu*,ceil(log_2 W*))` contains that trial and supplies its
    full elementary work budget. Summing all trial budgets gives at
    most `4r* max(2^mu*,W*)`; the permitted clock/simulation logarithmic
    overhead preserves polynomial bit complexity. Setup and completed
    output are explicitly charged. The first successful trial may have
    another ratio or stage, so the statement correctly bounds its output
    by total work and reserves the sharper fixed-ratio shell count for
    the sufficient run.

13. **Exponential-denominator example.** If
    `sigma_{t+1}=sigma_t^2/4` and `sigma_0=1/2`, writing
    `sigma_t=2^{-e_t}` gives `e_{t+1}=2e_t+2` and therefore
    `e_t=3*2^t-2`. On `[0,1]` the derivative bound is `1/2`, and
    the interval is invariant. The expanded denominator indeed has
    exponentially many bits despite contraction, establishing why
    compressed output is material.

## Final disposition

Both dynamics sections satisfy their stated mathematical promises. The
exact-real theorem and the polynomial finite-bit extension use distinct,
explicit computational and output representations. No computational
experiment is needed to support these proof-based conclusions.
