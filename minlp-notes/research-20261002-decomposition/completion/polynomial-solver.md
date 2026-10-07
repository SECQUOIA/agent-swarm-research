# Explicit polynomial solver

The fixed-degree polynomial extension now has a reusable exact-arithmetic
implementation. It accepts continuous and native integer box variables,
rational polynomial factors in the monomial basis, and a supplied or
heuristically generated tree decomposition. It produces an independently
replayable objective bound and complete domain-filtering history.

- Implementation: [`polynomial_grid.py`](../solver/polynomial_grid.py).
- Independent replay: [`verify_polynomial.py`](../solver/verify_polynomial.py).
- Tests: [`test_polynomial_grid.py`](../solver/test_polynomial_grid.py).
- Independent review: [`polynomial-review.md`](polynomial-review.md).
- Automatic exact boundary output: [`polynomial-boundary.md`](polynomial-boundary.md).

## Model and use

`PolynomialFactor(scope, terms)` represents a sum of monomials. Each term is
`(coefficient, powers)`, and powers follow the listed scope order. Coefficients
and bounds are integers, rational strings, or Python `Fraction`s; floating-point
coefficients are rejected. Exponents are nonnegative integers. Repeated
monomials are combined exactly. Constant factors have empty scope.

`PolynomialBox(bounds, factors, integers=(), bags=None, edges=None)` validates
the domain and factor coverage. Omitting both decomposition arguments invokes
the shared deterministic scope-based decomposition heuristic; this supplies an
upper bound on width, not a minimum-width claim.

For example, from the `solver/` directory:

```python
from fractions import Fraction as F
from polynomial_grid import PolynomialBox, PolynomialFactor, solve
from verify_polynomial import verify_polynomial

# (x²-1/4)²+(y-x)², whose minimum is 0 at (+/-1/2,+/-1/2).
p = PolynomialBox([(-1, 1), (-1, 1)], [
    PolynomialFactor((0,), [(1, (4,)), (F(-1, 2), (2,)), (F(1, 16), (0,))]),
    PolynomialFactor((0, 1), [(1, (2, 0)), (-2, (1, 1)), (1, (0, 2))]),
])
proof = solve(p, epsilon=F(1, 100), time_limit=10, max_table_states=100000)
checked = verify_polynomial(proof, expected_problem=p)
```

`to_dict()` / `from_dict()` define the JSON model format. The command-line
interfaces read and write these exact rational artifacts:

```sh
python polynomial_grid.py model.json proof.json --epsilon 1/1000 --time-limit 10
python verify_polynomial.py proof.json
```

The replay API accepts `expected_problem=p` to bind a proof to an externally
supplied model. Without it, the statement checked is the model embedded in
the certificate. An optional `check` callback lets a caller interrupt replay.
The model also exposes exact evaluation, gradients, Hessians, and arbitrary
repeated derivative interval bounds. The boundary adapter uses those APIs.

## What the certificate proves

Every global coordinate curvature cap is derived, not supplied by the caller.
The producer differentiates each factor twice and computes a rational interval
for each resulting monomial on the original box. Summing interval bounds gives
`partial_ii F(x) <= L_i`, with `L_i >= 0`. The certificate records the original
box, derivative intervals, and caps. The checker independently reproduces them
using direct falling-factorial monomial differentiation and interval products.
Intervals crossing zero use the parity of each power.

At a grid node `v`, coordinate `i` receives correction
`L_i * ell_i(v)^2 / 8`, where `ell_i(v)` is the largest adjacent cell length.
Native integer cells of length one have no feasible interior labels and incur
zero correction. Sequential coordinate interpolation proves that the minimum
of the corrected grid objective is a lower bound on the continuous/mixed
problem. When `L_i=0`, the objective is concave in that coordinate with all
others fixed, so endpoints suffice.

Factors are assigned once to covering bags. The producer uses the shared
[`finite_dp.py`](../solver/finite_dp.py) for the grid minimum, witness, all unary
minimum margins, and all directed tree messages. It uses the QP solver's
coordinate-grid geometry. The polynomial-specific code owns factor evaluation,
curvature derivation, and its certificate history.

The verifier reconstructs local tables and checks every directed Bellman
identity. It checks the attaining grid witness, every unary margin, each
feasible incumbent, and every pruning decision without calling the optimizer
or shared DP optimizer.

Continuous filtering keeps cells whose endpoint margin minimum does not
exceed the incumbent. Integer filtering keeps passing grid labels plus the
integer interiors of retained gaps of length at least two; unit gaps contribute
no extra labels. This distinction lets the retained integer hull become a
singleton. The certificate's final `retained_bounds` contains **every original
global optimizer**. Thus the history is suitable for the separate exact
boundary adapter. When a restarted trial is interrupted, replay exposes the
last completed domain, not the unfinished trial's working domain.

## Output and guarantees

- `certified`: the reported rational upper and lower bounds differ by at most
  the requested `epsilon`.
- `exact`: the upper and lower bounds coincide and the reported feasible
  rational point is a global optimizer.
- `stage_limit`, `table_limit`, or `time_limit`: the saved completed history
  still proves the reported bounds; the requested gap may remain unresolved.

The default decreasing-slope conditioning trials implement the existing
fixed-degree corrected-grid algorithm. Under its unique-optimum quadratic
growth assumptions, supplied-width and conditioning bounds give the theorem's
parameterized approximation guarantee. Certificate validity itself requires
neither uniqueness nor a supplied growth constant. Alternative uniform and
adaptive grids support diagnostics and exact native integer completion.

For native integer variables and fixed rational continuous coordinates, the
solver substitutes the fixed values into each monomial and computes the common
coefficient denominator `D`. Every feasible objective value then belongs to
`(1/D) Z`. A strict certified gap smaller than `1/D` proves the incumbent exact
without requiring a zero grid correction. The `integer_lattice` certificate
records `D` and the lower bound before exactification; replay independently
recomputes both and checks the strict separation. Varying continuous coordinates
cannot use this rule.

Sufficiently fine native integer grids also have only unit gaps and zero
correction, giving exact output directly. Large domains can exceed the explicit
table budget. These stopping rules do not provide an unconditional
polynomial-time integer optimization result.

The grid routine alone does not implement general exact algebraic output for
continuous polynomials. The separate boundary adapter returns a finite exact
implicit descriptor when its global containment, derivative signs, and
restricted strong-convexity tests succeed; its scope is recorded separately.

## Validation

From `research-20261002-decomposition/solver`:

```sh
python -m unittest test_polynomial_grid.py -v
python -m unittest test_polynomial_review.py -v
```

The implementation suite passed **11 tests**. It covers a coupled quartic
chain with two known global optima, brute-force agreement for sparse DP and
all margins, exact degree-six native integer output, mixed integer singleton
filtering, a concave cubic endpoint reduction, constant/fixed factors, invalid
models, incomplete-run replay, a replay callback, and rejection of altered
curvature, messages, domains, and exactness claims.

The independent review suite passed **11 tests**, with 24 random quartic finite
DP comparisons, 1,326 exact derivative/interval comparisons, ten dense
coordinatewise-concave endpoint comparisons, integer enumeration, shifted
skipped-integer-label retention, flat optimal-set preservation, a forced
interrupted restart, exact coefficient-lattice separation after fixed rational
substitution, equality-gap rejection, and malformed proof rejection. Its review records the
individual counts and scope. These are targeted local checks; no project-wide
verification or CI inspection was run.

## Limits

Monomial interval bounds can be conservative when terms cancel. They provide
a rigorous default without an external interval package or a claimed optimal
curvature estimate. Factor tables remain exponential in the decomposition bag
size. Exact rational arithmetic can consume substantial memory.

The parser accepts arbitrary polynomial degree. The fixed-degree theorem
must not be applied as a polynomial-time bound when exponents are part of
unbounded-degree input. Input evaluation, differentiation, interval setup,
and individual integer/rational arithmetic operations are atomic. The time
budget is cooperative during grid and table work, not a hard subprocess
wall-clock or memory limit. Nonfinite time-limit values are rejected.
