# Numerical contract for joint support cuts

The new support kernel certifies the actual finite binary64 coefficients sent
to the solver. It does not use the earlier univariate envelope code's safety
shift, the curve separator's assumed `libm` error bound, or endpoint values in
place of unresolved intervals. Historical experiments and their numerical
claims have not been rewritten.

## Supported model and public interface

For features `features = (f_0, ..., f_k)` and a domain

\[
D=\{x\in [l,u]:a_r^\top x\le b_r\text{ for each supplied row }r\},
\]

`certify_support(features, symbols, box, coefficients, ...)` returns a cut

\[
\sum_j c_j f_j(x)\ge\beta\qquad(x\in D).
\]

Coordinates of the original variables can be included as features. A solver
integration associates each feature with its corresponding original or
auxiliary variable. It must establish that each auxiliary represents that
feature and that each supplied row is valid on the cut's scope.

The arguments are stored SymPy expressions, symbols, numeric bounds,
coefficients, and rows of the form `(coefficient_tuple, rhs)` for `a*x <= rhs`.
Expression source strings are rejected. Integers and rational constants are
exact. A SymPy Float is interpreted as its exact stored binary value. Every
direction coefficient is first converted to the binary64 value that will be
exported; all later proof arithmetic uses that value's exact rational form.

The supported domains are:

- Rational polynomial curves in one variable and polynomial blocks in two
  variables, with bounded rational boxes and optional affine rows. The
  Bernstein tensor has at most 1,024 entries and degree at most 32 in each
  variable.
- Bivariate quadratic scalar support functions over rational polygons,
  including segments, singletons, and empty domains. An exact stationary-point
  oracle avoids subdivision.
- Multivariate quadratic stars: all mixed terms share one center, and every
  affine row contains at most one other variable. The exact star oracle
  accounts for all supplied rows and shares one center value across all
  leaves. General overlapping blocks or nonstar graphs are outside this
  implementation.
- One-variable elementary expressions built from rational constants, `pi`,
  `E`, addition, multiplication, integer powers, rational powers, `exp`, `log`,
  `sin`, `cos`, `sinh`, `cosh`, `tanh`, `atan`, and `Abs`. Their evaluation
  requires python-flint. Fractional powers use a nonnegative base; negative
  exponents require a strictly positive base. This interface does not infer a
  real odd-root interpretation for negative bases.

`SupportResult.status` is `complete`, `empty`, `incomplete`, or `unsupported`.
Only `complete` returns `cut`. The cut exposes `coefficients`, `rhs`
(`rhs_float` is an alias), and the exact dyadic `rhs_exact`. `witness` is a
JSON-compatible dictionary. `stats` records the method and work performed.
For exact polygon/star support, `stats.minimizer` and `stats.exact_support`
also contain exact rational strings; these remain available if an unattainable
separation target causes an `incomplete` result.

If `target` is supplied, even the exported, downward-rounded right-hand side
must be at least that target. Failure to reach it within the subdivision
budget returns `incomplete` with no cut and no partial witness. Without a
target, a finite conservative bound suffices. A failed separation attempt
never establishes membership in the convex hull. The optional exact
minimizers are useful for proposing additional samples, which the membership
checker reevaluates from the expected model.

## Exact polynomial bounds

The kernel first validates every feature expression tree as polynomial, then
combines the direction with exact rational coefficients. It transforms the
resulting polynomial to the unit box and calculates its tensor Bernstein
coefficients in rational arithmetic. Their minimum is a lower bound because
the Bernstein basis is nonnegative and sums to one on that box.

Each split bisects one coordinate at its exact rational midpoint. A leaf may
be excluded only when the exact minimum of a supplied affine row over its
whole box is **strictly greater** than that row's right-hand side. Equality
does not exclude a feasible boundary. An accepted witness contains a complete
binary split tree; its leaves either supply a valid bound or a row exclusion.
Consequently no part of the original domain can disappear from the proof.

The polygon and star fast paths supply exact rational support values and
their own complete certificates. Their proofs and restrictions are described
in the accompanying theory document. Final float conversion and full feature
binding still pass through the common support-cut wrapper.

Rigorous Bernstein affine bounds are established literature, including
[Garloff and Smith (2008)](https://www-home.htwg-konstanz.de/~garloff/rigorous.pdf).
This implementation's contribution is the particular model binding, final
coefficient recertification, replayable export, and solver integration.

## Elementary intervals and curvature

Rational interval addition, multiplication, division, and integer powers are
exact. Monotone transcendental functions are bounded by Arb evaluations at
their exact rational endpoints. Sine, cosine, and hyperbolic cosine use an
Arb enclosure of the entire input interval. Arb's `lower()` and `upper()`
endpoints are converted to exact dyadics through `man_exp()`; decimal output
and ordinary floating-point function evaluations are not used in the proof.
See the [python-flint Arb reference](https://python-flint.readthedocs.io/en/stable/arb.html)
and [Arb's arithmetic description](https://arxiv.org/abs/1611.02831).

Every original feature is evaluated and its domain checked on each retained
cell, including features with zero direction coefficient. Only then may the
kernel use cancellation in the combined scalar function
\(g=\sum_j c_j f_j\). It takes the maximum of the separate-feature interval
bound, the combined-function interval bound, and, where available, the
rigorous curvature bound

\[
\min\{\underline g(a),\underline g(b)\}
-\frac{(b-a)^2}{8}\max\{0,\overline{g''([a,b])}\}.
\]

The curvature expression is compiled once per direction. If it is
unsupported, undefined, or unbounded on a cell, the full-domain natural
interval bound remains available. No endpoint is substituted for a sliver.
For example, `sqrt(x)` and `x**(3/5)` are enclosed on `[0,1]` although their
derivatives are singular at zero. A tiny interval extending below zero is
rejected or remains incomplete.

The original model boundary matters: SymPy may simplify `x/x` to `1` before
this API sees it. A previously erased singularity cannot be recovered from
the constant `1`. A retained, unevaluated reciprocal product is checked at
zero and rejected. The integration must preserve the original parser's
domain semantics or explicitly restrict its claim to the mathematical
expression supplied to the checker.

## Final rounding and replay

Let \(L\) be the exact rational global lower bound. The kernel takes the
nearest binary64 value and, when it exceeds \(L\), its immediate predecessor.
Thus the emitted finite \(\beta\) satisfies
\(\operatorname{Fraction}(\beta)\le L\). Overflow produces no cut. This
rounding is performed after all final direction coefficients have been
converted to their exported binary64 values. It is not sufficient to round a
previously certified rational direction and reuse its old bound.

`replay_support(features, symbols, box, coefficients, rows, witness)` accepts
the **expected** model, not a model asserted by the certificate. It checks:

1. The typed feature trees, exact bounds and rows, and hexadecimal float
   coefficients match that model.
2. Every split has exactly two children covering its parent's box, and every
   excluded leaf has an exact affine-row contradiction.
3. Every retained leaf's lower bound is no greater than a newly computed
   Bernstein or Arb bound, or the exact polygon/star certificate replays.
4. The stored global bound is no greater than every retained leaf bound, and
   the exact dyadic value of the exported right-hand side is no greater than
   the global bound.

The checker never evaluates expression text supplied by a witness. Generation
and replay share arithmetic routines, so this is an independently executable
replay pass, not a separately implemented arithmetic library or a formally
verified checker. Its trusted base includes Python's rational arithmetic,
the expression walker, the exact oracle implementations, and, for elementary
functions, python-flint/FLINT. It certifies a row's mathematical validity; it
does not certify SCIP's entire solve, feasibility tolerances, internal row
transformations, or the original model-to-auxiliary translation by itself.

## Targeted verification and environment

The focused tests cover interior minima, clipped polynomial domains, exact
float coefficient conversion, downward rounding, forged right-hand sides,
forged leaf bounds, omitted branches, incorrect row exclusions, model-binding
mutations, empty domains, unsupported graphs, zero-weight undefined features,
unevaluated reciprocal cancellation, tiny invalid endpoint slivers, singular
derivative endpoints, large trigonometric arguments, and exact graph samples.

The following command was run from the repository root:

```sh
PYTHONPATH=research-20261002-convexification \
  /tmp/minlp-convexification-env/bin/python -m pytest -q \
  research-20261002-convexification/solver/test_certified.py
```

Result: **29 tests passed**. This is a local targeted result, not a CI result.
No project-wide verification or CI inspection was performed for this kernel.

The temporary environment was created explicitly with:

```sh
uv venv /tmp/minlp-convexification-env
uv pip install --python /tmp/minlp-convexification-env/bin/python \
  sympy python-flint pytest numpy scipy
```

Resolved versions for this check were Python 3.14.6, SymPy 1.14.0,
python-flint 0.9.0, pytest 9.1.1, NumPy 2.5.3, and SciPy 1.18.1. The support
kernel itself does not require NumPy, SciPy, or a solver. Polynomial support
and replay do not require python-flint. No library installs occur inside the
checker.

## Remaining limitations

Exact rational arithmetic and proof replay add cost. Certificates retain
the subdivision tree and can become large. Strict domain validation can be
inconclusive when interval dependence obscures a valid expression's domain;
subdivision budgets then produce no cut. The general polynomial path is a
bounded refinement method, not a polynomial-time exact hull algorithm.
Elementary expressions have only one free variable. Wider nonstar coupling,
general nonlinear domain constraints, complex branches, arbitrary special
functions, and automatic preservation of domains already erased by an
external symbolic parser are not supported.
