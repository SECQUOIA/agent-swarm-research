# Expected exact sparse polynomial box optimization under linear noise

Date: 2026-10-02. Status: complete theorem that passed independent
completed-text reviews and targeted exact checks. The result extends the
[sparse mixed quadratic cell theorem](sparse-bag-cell-smoothed-miqp.md) to
explicit fixed-degree polynomial factors. Exact output is implicit; it does
not expand algebraic coordinates or the optimal value. Publication priority
and practical performance are not established.

## 1. Statement and output

Let `F_0=sum_B f_B` be an explicitly represented rational polynomial of
fixed degree at most `d>=1`, on a product `X` of bounded rational continuous
intervals and bounded native-integer intervals. Every factor scope is
contained in a supplied tree-decomposition bag, and the largest bag has
size `p`. Round integer bounds inward, detect empty domains, and substitute
fixed coordinates. With no remaining coordinates, evaluate directly.
Otherwise write

```
n=n_c+n_z,    w_i=u_i-ell_i>0,    W=sum_i w_i,    w_max=max_i w_i.
```

Supply rational `sigma>0` and `L>0` such that

```
partial_ii F_0(x) <= L    on the full continuous hull of X, for every i. (1)
```

Let `I` be the binary length of these base data. Such an `L` can also be
computed by rational monomial bounds; its numerical size then enters the
bound below. The optimization theorem takes (1) as a valid input premise. For an
independently checkable global proof record, derive `L` by the stated
monomial bound or supply a polynomial-time-verifiable proof of a sharper
bound, with its length and verification cost counted in `I`. No general
polynomial-inequality verification oracle is assumed.

There is a base-computed power of two `M`, with `log M=poly_d(I)`, for
which independent uniform draws

```
gamma_i in {-sigma+2sigma k/(M-1): k=0,...,M-1}                 (2)
```

admit an algorithm returning an exact global optimizer of
`F_gamma=F_0+gamma'x` on **every draw**, with expected bit work at most

```
C_0^p [4+(1+n/2)L w_max/(2sigma)]^p poly_d(I).                 (3)
```

Here `C_0` is absolute, and the polynomial exponent may depend on fixed
`d`. No growth constant, unique optimum, nondegeneracy, integer-dimension
bound, or negative-inertia bound is assumed in the input.

The output has two permitted exact forms. The usual branch returns fixed
integer values, fixed original continuous bounds, and a rational box `C`
on the remaining coordinates, with a verified positive Hessian modulus.
Its unique constrained minimizer is the specified global optimizer; a
polynomial KKT system or `argmin_C F_gamma` denotes it exactly. The value
is the objective evaluated at this unique point. The exceptional branch
returns a real-algebraic global optimizer and its value by an exact general
fallback. It permits ties and positive-dimensional optimal sets.

The compact patch descriptor has polynomial length in `I`, including the
sampling bits, and supplies arbitrary-precision point and value evaluation
in `poly_d(I+q)` bit work. The exceptional representation and its evaluation
may have exponential size and cost. Their expected contributions are
polynomial because the same-draw fallback is rare. The separate global
pruning/DP proof record can be large even on a successful patch draw; its
expected size and verification work obey (3), rather than a per-draw
polynomial bound. Evaluation uses the compact descriptor after its global
validity has been established. Thus the result does
not assert polynomial expanded algebraic degree or output length on every
draw.

For fixed bag size, (3) is polynomial under polynomial bounds on its
numerical width/noise ratio. It is not an FPT bound in `p`, nor a polynomial
bound in the binary encoding of integer widths alone. It solves the sampled
objective under the one finite law (2), without resampling failures.
Section 7 records the elementary certified approximation consequence for
the original objective; exact unperturbed optimization is not asserted.

## 2. Polynomial rounding preserves the sparse cell argument

Use the nested mixed cells, bag-cell whitelists, deduplicated corner rows,
and two-pass separator-key DP from Sections 2--3 of the
[mixed quadratic theorem](sparse-bag-cell-smoothed-miqp.md). Binarize the
decomposition first, preserving bag size. Let `s` be the least power-of-two
integer at least `max(1,w_max)`, and let `h_j=s 2^(-j)`.

Continuous cells are clipped intervals of width at most `h_j`. Integer
cells use integral endpoints while `h_j>=1`; at the first level `h_j<1`,
replace retained unit intervals by singleton endpoint cells. Integer cells
then remain points. Each coordinate cell has at most two children.

For a univariate function with second derivative at most `L`,
mean-preserving endpoint rounding gives

```
E f(Y) <= f(x)+(L/2) Var(Y).
```

Apply this inequality sequentially in all coordinates. Bound (1) holds
throughout every intermediate line segment, even for a coordinate whose
original domain is integral. Independence preserves each coordinate's
conditional mean. Consequently, rounding any feasible mixed point to its
cell corners gives

```
E F_gamma(Y) <= F_gamma(x)+E_j,       E_j=n L h_j^2/8.          (4)
```

Integer coordinates already on grid nodes do not move and contribute no
variance. This argument replaces the quadratic cancellation of cross
terms; no multiaffinity or convexity of the polynomial is required. Shared
nested partitions preserve every bag whitelist under the rounding, also
when one particular bag cell is specified.

Let `m_j` be the exact allowed-grid minimum, `U_j` the best feasible value
seen, and `m_B(v)` the exact bag-row min-marginal. For a candidate bag cell
`C`, define

```
q_C=min_{v a corner of C} m_B(v),       LB_C=q_C-E_j.           (5)
```

Retain exactly cells with `LB_C<=U_j`. Inductively every original global
optimizer remains in the physical domain of the retained whitelists,
because fixed-cell rounding proves the lower bound. Moreover,

```
f* <= U_j <= m_j <= f*+E_j,
F_gamma(y)=q_C <= f*+2E_j                                     (6)
```

for some globally consistent feasible grid witness `y` for each retained
cell. This remains true for nonunique optima and for every finite-noise
draw. The DP evaluates explicit rational polynomial factors exactly and
uses minima keyed on separator tuples, not products of neighboring table
lists.

## 3. Conditional semiconcavity gives the same expected cell count

Condition on the noise outside a bag `B`. Define on its full real box

```
V_B(v)=min_{x_out in the original mixed outside domain}
       [F_0(v,x_out)+gamma_out'x_out].                        (7)
```

The outside feasible set is fixed independently of `v`. For every outside
point and coordinate `i in B`, subtracting `L v_i^2/2` leaves a concave
function of `v_i`; taking the infimum preserves concavity. Thus `V_B` is
coordinatewise `L`-semiconcave and is independent of the entire bag noise.

Every retained-cell witness corner satisfies

```
V_B(v)+gamma_B'v <= min_{v' in the original mixed bag domain}
                         [V_B(v')+gamma_B'v']+2E_j.           (8)
```

Let `a_i,j=h_j` for continuous coordinates and `a_i,j=max(1,h_j)` for
integer coordinates. At a regular coordinate node, comparisons with both
feasible neighbors a distance `a_i,j` away confine `gamma_i` to an interval
of length at most

```
L a_i,j+4E_j/a_i,j.                                          (9)
```

For a fixed bag tuple, these intervals depend on the conditioned outside
noise and the tuple, not on other in-bag noise. At most three coordinate
nodes are exceptional; there are at most `w_i/a_i,j` regular nodes. The
finite-law interval bound `length/(2sigma)+1/M`, followed by independent
multiplication, therefore gives

```
E[number of full-grid bag tuples satisfying (8)]
 <= product_(i in B)
 [3+Lw_i/(2sigma)(1+n h_j^2/(2a_i,j^2))+w_i/(M a_i,j)].        (10)
```

If `j<=J` and `M>=2^J`, this is at most

```
H_B=product_(i in B)[4+(1+n/2)Lw_i/(2sigma)].                 (11)
```

Indeed `w_i/(M a_i,j)<=s/(M h_j)=2^j/M<=1`.

Each corner belongs to at most `2^p` cells; each retained cell has at most
`2^p` children with at most `2^p` corners. The expected row and cell work
per level is consequently `C_0^p sum_B H_B`, with polynomial arithmetic
and dictionary overhead. This counts deterministic full-grid tuples only
in the analysis. The actual algorithm generates the sparse lists. It does
not condition the perturbation law on earlier pruning decisions.

## 4. Sound exact closure on a rational convex patch

Compute rational bounds on the original continuous hull

```
M_1 >= max{1, max_i sum_k sup |partial_ik F_0|},
T   >= max{1, max_i sum_jk sup |partial_ijk F_0|}.             (12)
```

Termwise monomial bounds suffice and have polynomial encoding length for
fixed `d`. Their magnitudes affect the cutoff logarithm, not (11).

Intersect the coordinate projection hulls of all retained bags containing
each coordinate. Their product `Q_j` contains every original global
optimizer. Fix an integer coordinate only when this intersected hull is a
singleton. For continuous coordinates use the rational midpoint `c` of
the current hull and `r=max_i (u_i(Q_j)-ell_i(Q_j))/2`. The interval

```
partial_i F_gamma(c) + [-M_1 r,M_1 r]                         (13)
```

contains the gradient on the hull. A strictly positive interval forces the
original lower bound at every optimizer; a strictly negative one forces
the original upper bound. This uses the original-box first-order condition
within each fixed integer slice. It is not applied to integer coordinates.
Recorded equalities may be intersected into the hull before further tests,
since all optimizers satisfy them.

Once every integer coordinate is fixed, substitute its value and all
forced continuous bounds. On the remaining continuous box `C`, remove
singleton coordinates and take its midpoint `c` and radius `r` as above.
Given a positive rational trial modulus `g_0`, test by exact rational linear
algebra whether

```
H_CC(c)-(T r+g_0) I is positive definite.                    (14)
```

The third-derivative row-sum bound implies
`||H_CC(x)-H_CC(c)||_2<=T r` throughout `C`. Hence (14) certifies
`H_CC(x)>=g_0 I` on `C`. The box contains every original optimizer, so its
unique constrained minimizer is globally optimal for the original mixed
problem. This is a local patch closure: the Hessian need not be positive
on the entire original face. With no remaining coordinates, simply return
the fixed feasible point and its exact rational value.

The global proof record retains the pruning and fixing steps. The compact
patch descriptor records the substitutions, rational box, objective,
modulus, and rational matrix test. Equivalently, the unique primal point is described by its box KKT
system with nonnegative lower/upper multipliers. The positive Hessian bound
makes this exact implicit representation unambiguous. The certificate's
soundness uses no unverified growth or margin promise.

For stopping analysis only, suppose the sampled problem has point growth
at least `g_0` at its unique optimizer `a`, and every active continuous
coordinate has absolute gradient greater than `tau`. Set

```
A=2+nL/g_0.                                                  (15)
```

By (6), witnesses lie within Euclidean distance
`h_j sqrt(nL/g_0)/2` of `a`; retained cells and their coordinate hulls lie
within coordinatewise distance `A h_j`. If

```
h_j <= min{1/(4A), tau/(4M_1 A), g_0/(4T A)},                 (16)
```

then `h_j<1`, and integer cells are singleton values within `1/4` of the
optimal integer label. Thus all integer hulls are the correct singleton.
Since `a` lies in the hull, its midpoint is at distance at most `r` from
`a` in the infinity norm. The enclosure (13) differs from the gradient at
`a` by at most `2M_1 r<=tau/2`, so every active continuous coordinate is
forced correctly.

The remaining original continuous coordinates are interior at `a`.
Two-sided Taylor expansion of point growth gives

```
H_CC(a) >= 2g_0 I.                                          (17)
```

The matrix in (14) is at least `(g_0-2Tr)I >= (g_0/2)I`, so closure
succeeds by (16). No positive full Hessian at a boundary optimizer is
assumed: eliminating active coordinates is what justifies (17).

## 5. One finite law and a rare exact fallback

Use the [polynomial finite-noise tail theorem](polynomial-finite-noise-tails.md).
For the point-growth modulus `g_*`, with `g_*=0` on nonunique draws, that
result supplies a base-computable integer `C_tail=2^{poly_d(I)}` such that
for every threshold `epsilon>0` the same law (2) satisfies

```
Pr{g_*<epsilon} <= W epsilon/sigma+2n C_tail/M.               (18)
```

Its two-block real quantifier-elimination bound is independent of the
threshold and all coefficient heights. Integer membership is a finite
disjunction; its number of atoms can be exponential, but its logarithm is
polynomial in `I`. General doubly exponential cylindrical decomposition
would not suffice for the sampling conclusion here.

Let `R_z=product_(i integer)(w_i+1)` and

```
K=max{1,n_c 3^n_c R_z max(1,d-1)^n_c}.                       (19)
```

The same tail note proves the unconditional intersection bound

```
Pr{g_*>0 and some active continuous gradient has magnitude <=tau}
 <= K(tau/sigma+1/M).                                        (20)
```

Conditioning on all noise except that coordinate's coefficient leaves the
free stationary equations of every integer slice and original continuous
face unchanged. Positive point growth makes their relevant free Hessian
positive definite. Their nonsingular complex roots number at most
`max(1,d-1)^k` by Bezout, even if other singular components have positive
dimension. Each root imposes an interval of length `2tau` on the remaining
noise. This does not condition the law on a good-growth event.

The [exact polynomial-box fallback](polynomial-exact-fallback.md) supplies
an integer `B=2^{poly_d(I)}` and a fixed exponent `c_d` such that every
sampled input can be solved in

```
B (I+b+1)^c_d bit operations,    b=log_2 M,                   (21)
```

with an exact algebraic optimizer and value, even if minimizers tie or
form a continuum. It selects the lexicographically least global optimizer
by successive minimization over compact sets. Each coordinate, and the
value, has a singleton formula with two quantified blocks and one free
scalar. Renegar's bit-model elimination theorem followed by univariate
root isolation constructs the separate exact representations. The
coordinate formulas select the same canonical point. The polynomial
dependence on new coefficient bits is explicit; `B` depends only on the
base input. An independently checked
[constructive derivation](polynomial-exact-fallback-construction.md) also
proves this interface. Enlarge effective base polynomials so `B>=1`.

Choose, before drawing noise,

```
rho=1/(4B),    g_0=rho sigma/(2W),    tau=rho sigma/(2K).      (22)
```

Take the least `J>=0` satisfying (16) with `h_J=s2^(-J)`. Then choose the
least power of two

```
M >= max{2,2^J,4n C_tail/rho,2K/rho}.                        (23)
```

All logarithms in this construction are polynomial in `I`. There is no
precision circle: `B`, `C_tail`, `K`, `rho`, `g_0`, `tau`, and `J` are
fixed from the base data before `M`; only the polynomial factor in (21)
subsequently uses its bit length.

Equations (18) and (20) bound the two bad events by `rho` each. Therefore
closure succeeds by level `J` except on an event of probability at most
`2rho=1/(2B)`. If it has not succeeded, invoke (21) on this same draw.
The fallback terminates exactly even on tied or degenerate samples. Its
expected work and expected output size are polynomial in `I`.

## 6. Bit work and computational meaning of implicit output

There are polynomially many levels and bags. Sampled coefficients, uniform
grid coordinates, exact polynomial evaluations, DP sums, hull endpoints,
gradient intervals, and matrices in (14) all have polynomial encoding
length. Fixed degree is important for these estimates. Even the logarithm
of a complete level-grid table is polynomial in `I+J`, so sorting the
sparse generated rows adds only a polynomial factor to their count.
Summing (11) and adding the expected fallback proves (3).

For a successful patch, the [convex-patch evaluation lemma](convex-patch-evaluation.md)
checks the bit-model hypotheses of classical rational ellipsoid weak
optimization. In detail, bound `|F_gamma|<=V` on its rational box, and use
the compact epigraph

```
{(x,t): x in C, F_gamma(x)<=t<=V+2}.
```

It contains a ball about `(midpoint(C),V+1)` of radius `r_K`, the minimum
of `1/2` and the least positive half-width of `C`. Its enclosing radius and
inverse inner radius have polynomial encoding length. Polynomial value
and gradient evaluation provide rational separation, and the linear
objective `t` is globally 1-Lipschitz.

The bit-model weak-optimization theorem returns a point within `zeta` of
the epigraph, with objective compared against its `zeta`-erosion. The
evaluation lemma handles this contract explicitly. Homothety toward the
known epigraph center bounds the erosion cost by `(2V+1)zeta/r_K`.
Project the returned rational `x` onto `C`. For a rational bound
`G>=max(1,sup_C ||grad F_gamma||_2)`, the resulting feasible point `y`
and lower endpoint

```
a=t-[1+(2V+1)/r_K]zeta
```

satisfy `a<=f*<=F_gamma(y)` with interval width at most
`[G+2+(2V+1)/r_K]zeta`. Taking `zeta<=r_K/2` sufficiently small for
the requested gap uses only polynomially many precision bits. Thus the
required cost is polynomial in the compact patch encoding and requested
tolerance bits, even at boundary minimizers. This uses convex optimization
bit complexity, not a grid bound polynomial in the numerical ratio
`L/g_0`.

With `eta <= min{2^(-q), (g_0/2)2^(-2q)}`, strong convexity on the box
implies distance at most `2^(-q)` to its constrained optimizer. The feasible
value `U` gives the enclosure `[U-eta,U]`. Because `log(1/g_0)` and the
patch encoding are polynomial in `I`, these evaluations take
`poly_d(I+q)` bit work. On fallback draws, standard real-algebraic point
and value refinement costs `B' poly_d(I+b+q)` for a base singly exponential
`B'`; choose the budget `B` in (21) large enough also to dominate `B'`.
Their expected contribution is again polynomial. The fallback also
returns feasible rational approximants with a certified objective gap:
recover native integer labels exactly, clip continuous approximants to
the original box, and use a rational gradient bound and a separate value
enclosure to select sufficient precision. Section 6 of the fallback note
proves this within the same cost. No minimal polynomial, expanded
coordinates, or expanded exact value is required on usual draws.

The finite pruning trace is used as the global-containment certificate.
The result is an expected exact optimization theorem with a meaningful
implicit output contract, not a claim that every instance has a small
algebraic certificate or that trace logging itself is a new certificate
principle.

## 7. An elementary original-objective certificate

For any sampled exact optimizer `a_gamma`, comparison with an original
optimizer gives `F_0(a_gamma)-min_X F_0<=sigma W`. More generally, suppose
the evaluator returns a feasible rational point `y` and perturbed lower
bound `a` with `F_gamma(y)-a<=delta`. The two rational numbers

```
a-max_(x in X) gamma'x,                 F_0(y)
```

bound the original optimum from below and above, with gap at most
`delta+sigma W`. The maximization of the linear term is an exact endpoint
calculation on the mixed box. Thus choosing `sigma=epsilon/(2W)` and
`delta=epsilon/2` yields an original-instance epsilon certificate on every
draw, with the expected work obtained by substitution into (3). This is a
simple solver-facing consequence. Its inverse-accuracy exponent can be
worse than a basic uniform-grid approximation bound, so it is not claimed
as an improvement over established approximation methods.

## Attribution, review, and verification

The [focused source comparison](../prior-art/sparse-smoothed-polynomial-prior.md)
distinguishes qualitative generic growth under linear tilts from the
quantitative finite-law tail, and separates classical real-algebraic and
convex optimization tools from this sparse expected-work composition.
Qualitative generic uniqueness and growth under continuous linear tilts
already cover these mixed product domains through classical semialgebraic
results. Neither that genericity nor exact implicit descriptions are
claimed as new principles. The count and sparse DP come from the quadratic
predecessor; the new proof obligations are polynomial finite-law control
and exact local convex-patch closure.

The [independent composition review](smoothed-sparse-polynomial-independent-review.md)
and [adversarial review](../reviews/smoothed-sparse-polynomial-review.md)
check rounding, counts, closure, the finite-law budget, and exact output.
The [finite-tail review](../reviews/polynomial-finite-noise-tails-review.md)
independently checks the actual polynomial tail artifact and the primary
quantifier-elimination statement. The
[fallback review](../reviews/polynomial-exact-fallback-review.md)
checks both exact all-draw constructions and their separate precision
costs. The convex evaluator's actual GLS weak-optimization contract and
rational feasibility repair were also independently checked. These are
mathematical reviews; they do not establish publication priority.

The targeted command actually run was

```
python3 -B research-20261002/new-direction/check_smoothed_sparse_polynomial.py
```

The [checker](check_smoothed_sparse_polynomial.py) passed six stages of a
mixed quartic path instance with bag size two (treewidth one). All 126 bag min-marginals matched
exhaustive allowed-grid minima; 27 retained witnesses met the error bound;
42 cells were removed while preserving the known optimizer. It checked 12
rounding atoms and 117 growth sample points. The algorithm fixed the
integer label and an active continuous bound, then verified a positive
Hessian on the remaining patch. The original full continuous Hessian is
indefinite throughout this example, so active-bound elimination matters.
A further 54 exact cases checked coordinate rounding for `x^2 y^2`, whose
rounding error cannot be justified by quadratic cross-term cancellation.
The [results](smoothed-sparse-polynomial-check-results.json) record these
finite checks.

The adversarial reviewer separately ran

```
python research-20261002/reviews/check_smoothed_polynomial_review.py
```

That [diagnostic](../reviews/check_smoothed_polynomial_review.py) passed
four exact probability/cutoff budgets, including 4,006 sampling bits, and
three finite laws with a tied endpoint atom that needs fallback. It also
checks the cell-count atomic correction, closure inequalities, and three
near-feasible epigraph repairs, including a box with 200-bit thin sides.

Scoped whitespace, fenced-block, and local-link checks passed, as did
`git diff --check` restricted to this note, its checker, and its results.
These checks do not implement the full finite-noise sampler, exact
algebraic fallback, or ellipsoid evaluator, and do not establish the
asymptotic expectation experimentally. No project-wide verification or
CI inspection was performed.
