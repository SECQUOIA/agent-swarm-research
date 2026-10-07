# Independent review of the regridded quadratic bit bound

Date: 2026-10-02. Status: passes mathematical review; no substantive
correction required. This review covers
[`regridded-qp-bit.md`](../geometric-dp/regridded-qp-bit.md), including its
polynomial approximation extension and unknown-growth exact algorithm.

Reviewer provenance: fresh adversarial-review agent
`/root/geometric_checks/qp_bit_adversary`, assigned independently by
`/root/geometric_checks`. The parent confirmed the explicit invocation
settings `model='gpt-6-astra'`, `reasoning_effort='high'`, and
`fork_turns='none'`. This records spawn provenance, not an independently
verified runtime-model identity. The reviewer checked the derivation before
reading the completed draft.

Sources inspected were the proposed note, the aggregate regridding proof,
the original certificate definitions and shell construction, and the
rational-height and reconstruction argument in `exact-box-qp.md`. No
external literature was consulted. This is a correctness review, not a
novelty assessment.

## Verdict and scope

The argument establishes a uniform polynomial input and accuracy exponent,
with all dimension, occurrence, and conditioning dependence outside that
exponent. Its parameter is the full bag Hessian bound divided by global
quadratic growth, together with bag size and coordinate occurrence. It
does not establish FPT in width alone or the same conclusion under a
coordinate upper-curvature bound.

The important specialization is valid: affine local objectives over box
intersections have exact corner minimizers. Choosing endpoints also for
zero coefficients is necessary for the stated lattice invariant. No
unaccounted nonlinear optimization oracle remains.

## Lower models and aggregate contraction

For a quadratic bag with Hessian `H` and `v=z-m_B`, the model error is

```
a_t(z)-ell_t,B(z) = (1/2) v^T H v + Mp W_B^2/8.
```

The assumptions give `|v^T H v| <= M p W_B^2/4`, proving exactly the
claimed interval `[0,Mp W_B^2/4]`. A bound only on positive curvature
would not prove underestimation. The draft correctly uses a two-sided
operator-norm bound.

This model need not be exact at a box vertex, so it does not satisfy the
older pointwise `(U^q)` condition. The draft explicitly substitutes the
uniform bag-width error. That substitution is sufficient: certificate
validity uses underestimation, and the aggregate proof uses only
`sum err_t <= (A0/4) sum W_Bt^2`, with `A0=pM` here. The rest of the
telescoping, copy-drift, and contraction arguments is unchanged.

Replacing the unknown growth constant by `min(g,M)` preserves growth and
the stated `kappa=max(1,M/g)`. It also keeps the upper bound on the stage
count controlled by input magnitudes and the parameters.

The numerical constants pass. The three sufficient inverse-mesh bounds
are bounded respectively by

```
4k sqrt(p),
278 k^2 sqrt(p) kappa,
27 k^(3/2) sqrt(p kappa).
```

For the third bound, square it and use
`240 k kappa (2C0+p) <= 720 k^3 p kappa < 27^2 k^3 p kappa`.
For the second, `80 sqrt(12)<278`. Thus the chosen inverse between
`1024 k^2 p kappa` and `2048 k^2 p kappa` suffices.
The displayed bound `B<=259 k^3 p kappa^2` is conservative; the same
estimates give `B<=258 k^3 p kappa^2`.

## Denominators, message size, and uniform bit cost

The lattice proof matches the actual shell construction. Shell increments
at stage `j` have denominator dividing `A_j=D 2^(j+mu)`. The previous
center's denominator divides `A_(j-1)`, hence `A_j`; clipping and box
intersection only select existing coordinates. Exact affine minimization
and consistency extraction again select coordinates. They never divide
by an affine coefficient.

The proposed common value denominator

```
T_j = 8 D A_j^2 = 8 D^3 2^(2(j+mu))
```

is sufficient without an omitted midpoint factor:

- Quadratic midpoint values divide `4 D A_j^2`.
- A midpoint gradient dotted with a corner-minus-midpoint divides
  `4 D A_j^2`.
- The curvature correction divides `8 D A_j^2`.
- Center-gradient slopes dotted with corners divide `D A_j^2`.
- Intercept recurrences add, subtract, and select minima; they introduce
  no new denominator.

Each subtree intercept is the value of one configuration on that subtree,
so it contains at most linearly many bag and edge terms. A slope is itself
a sum of input-gradient terms. Absolute magnitudes therefore grow by
polynomial factors in the number of bags, rather than by an exponential
recurrence. Numerator bit lengths remain polynomial as claimed. Reduced
rational arithmetic or integer arithmetic scaled to `T_j` both suffice.

The use of `3^p` correctly covers supplied decompositions with separators
of size `p`. Merging bags solely to get `3^(p-1)` could change the
curvature parameter, so retaining the supplied decomposition is sound.
The incidence count and corner work give a cubic stage-count dependence;
the polynomial degree does not grow with `p`. Even a dense incidence scan
would preserve the FPT conclusion, though not the sharper displayed count.

## Unknown growth and exact reconstruction

The schedule budgets actual bit operations and imposes no stage cap.
Through the first sufficient round its simulated work is
`O(r_* 2^r_*)`, where
`r_*=max(1,mu_*,ceil(log2 T_*))`. Both `2^mu_*` and the successful run's
bit work have the required parameter dependence. Uniform polynomial
simulation and scheduling overhead preserve an absolute input exponent.
This avoids introducing an uncontrolled factor `2^J`.

The rational-height argument applies to the aggregated rational quadratic.
The optimum value bound remains valid without uniqueness, which is what
makes acceptance independent of the growth promise. The coordinate bound
applies to the unique optimizer. The numbers `R,V` have polynomial binary
length and are never enumerated.

The exact-run target is sufficient. The third mesh restriction implies
`M theta^2 <= gbar/(240kp)`. Thus an incumbent reaching the target has
squared distance at most `1/(3840kp R^4)`, strictly smaller than the square
of the reconstruction radius `1/(4R^2)`. Each coordinate interval
therefore contains its true rational coordinate, and its length is too
small to contain two rationals with denominators at most `R`.

The objective interval likewise isolates its unique denominator-at-most-`V`
rational. Final feasibility and exact objective equality are essential and
are present. They also handle candidates reconstructed during an
inadmissible trial. Polynomial-time rational reconstruction and the
precision `O(I^2+mu)` fit the uniform FPT bit bound.

## Polynomial extension and resolved clarifications

The approximation extension is valid for explicitly represented rational
polynomial coefficients with charged numerical degree. Evaluation at a
stage midpoint has denominator dividing `D(2A_j)^d`; gradient-times-point
terms have the same bounded-degree structure. Combining the curvature
correction only requires raising this to at least degree two. Subsequent
intercept accumulation remains additive. With `dbar=max(d,2)`, the draft's
explicit common denominator
`D^(dbar+1) 2^(dbar(j+mu+1)+3)` covers both polynomial terms and the
curvature correction. Value bit lengths are
`O(dbar(I+j+mu+1))` up to input-polynomial terms. The draft requires fixed
degree or numerical degree bounded by a fixed polynomial in input length.
This preserves its three-parameter scope; no additional degree parameter
is asserted.

This does not prove a rational exact optimizer for higher-degree bags.
The draft correctly limits the extension to certified approximation.
The current draft explicitly specifies monomial-list encoding, excluding
compressed polynomial circuits with uncharged coefficient heights. It also
specifies that the dyadic-accuracy exponent `q` is a nonnegative integer.
Both requested clarifications are resolved.

The current draft also includes exact rational positive-semidefiniteness
checks on `MI-H_t` and `MI+H_t`, or a directly verifiable absolute-row-sum
bound, to validate the supplied quadratic bound `M`. This resolves the
certificate-checking clarification. Checking general polynomial Lipschitz
bounds remains a separate input promise in the extension. No requested
clarification remains unresolved.

## Verification record

This review used read-only source inspection and independent algebraic
derivation. No executable tests were run by this reviewer; the note's
separate local tests are not attributed to this review. The only file
created by this reviewer is this review. No project-wide verification,
CI inspection, or external search was performed.
