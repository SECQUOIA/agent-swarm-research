# Independent review of the unbounded continuous radius theorem

Date: 2026-09-27. Status: independent derivation and adversarial proof audit.
The main manuscript is [unbounded-hessian-span.md](unbounded-hessian-span.md).
This review was started from the proposed statement before that manuscript was
available; its complete first draft was subsequently read. No substantive
gap was found. It does not establish publication priority.

## Verdict and precise scope

The proposed radius argument is sound. Let a nonempty set `F` be defined by
rational affine equations and inequalities and rational quadratic inequalities
`q_i(x)<=0`, each with a positive-semidefinite Hessian. There are no supplied
coordinate bounds and no constraint qualification. If the total explicit
binary input length is `N>=2` and the native Hessian matrices span a vector
space of dimension `h`, then `F` contains a point satisfying

```
||x|| <= 2^{N^{O(h+1)}}.
```

The bound concerns a real feasible point. It does not assert that the point
is rational, that the entire feasible set is bounded, or that an exact
continuous optimizer has been constructed. As usual for an explicit input
model, the number of listed variables and rows is bounded by the input
length. Unused coordinates can be fixed to zero.

The proof strengthens the existing bounded value argument by choosing the
coercive squared-norm objective. The compactness needed in the proof comes
from an unknown feasible point; that point is not used in the coefficient
description. This distinction is the main issue to check.

## Independent proof audit

Because `F` is closed and nonempty, `min_{x in F} ||x||^2` attains its value
`theta`. Choose its minimizer `x*`. Coercivity is sufficient for attainment;
boundedness of `F` is unnecessary. Strict convexity also makes this minimizer
unique, although uniqueness is not needed for the value bound.

Delete every inequality that is strict at `x*`, and impose equality in the
active affine rows. The minimum norm remains `theta`: a point in the new
system with smaller norm would give a better point of the original system
on a sufficiently short segment starting at `x*`. This uses the finite
number of deleted rows, their strict slack, and convexity of every retained
quadratic and of the objective.

Choose a Hessian basis among the active quadratic rows. For every other
active row, subtract its rational linear combination of the basis rows.
The resulting affine polynomial vanishes at `x*`; impose that affine
equation. This additional restriction retains `x*` and therefore retains
the minimum value. The basis coefficients and the resulting affine
equations have polynomial bit length by rational determinant bounds.
No coordinate of `x*` appears in their coefficients.

After rational elimination write `x=x0+Vu`, with `V` having full column
rank. The restricted squared-norm objective is

```
f(u) = ||x0+Vu||^2,
Hessian f = 2 V^T V > 0.
```

Its coefficients have polynomial bit length. Every retained quadratic is
now a linear combination of at most `h` basis polynomials, as a whole
polynomial. In particular, its gradient has the same combination formula.
There is no need to perturb the objective or append a ball. If the affine
space has dimension zero, its rational point already has the required
bound.

For `0<epsilon<1`, replace the retained inequalities by `q_i(u)<=epsilon`
and minimize `f`. The original point `u*` is strictly feasible. The
feasible set is closed, and the objective is coercive in `u`, so a
minimizer exists. Every such minimizer satisfies

```
f(u_epsilon) <= f(u*) = theta.
```

This is a common compact sublevel set, although its radius is not yet
known numerically. Any accumulation point as `epsilon` tends to zero is
feasible for the reduced system. It follows that the relaxed values
converge to `theta`. The unknown sublevel bound is used only for this
existence argument, never as an input coefficient.

Slater's condition for each relaxed problem gives nonnegative KKT
multipliers. Express the aggregate native-gradient contribution by the
coefficient vectors in the Hessian basis. Conic Caratheodory reduction
then leaves at most `h` multipliers, using only rows that are active at
the current relaxed minimizer. This preserves stationarity and
complementarity. It is unnecessary to preserve the sum of the
multipliers: the proof uses stationarity and primal feasibility, not an
identity for the Lagrangian's constant term. This point matters because
the shifted polynomials `q_i-epsilon` need not share the original linear
dependences.

Along a sequence tending to zero, one support `J` occurs infinitely
often. Its stationarity matrix is

```
M = 2 V^T V + sum_{i in J} lambda_i Q_i > 0.
```

Thus `u=p/Delta`, where `Delta=det M` and `p` is the appropriate adjugate
vector. Positivity follows for every nonnegative multiplier vector, not
only for the chosen certificates. After clearing denominators, impose
all retained primal inequalities, nonnegative multipliers,
complementarity on `J`, and the equation identifying the objective value
`w`. All solutions are global KKT minimizers of the relaxed convex
problem. Omitting inequalities outside `J` would invalidate this step;
the correct construction retains them.

The polynomial degree is `O(N)`, the number of rows is polynomial in
`N`, and coefficient bit lengths are polynomial in `N`. The variables
are `epsilon`, `w`, and at most `h` multipliers. The limit formula adds
one universal tolerance variable and has one free value variable. It
defines the singleton `{theta}` even if the multipliers diverge.
Bounded multipliers or a single support valid for every sufficiently
small `epsilon` are not required.

Coefficient-sensitive block quantifier elimination consequently gives
a nonzero integer polynomial `P` with `P(theta)=0`, degree
`N^{O(h+1)}`, and coefficient bit lengths `N^{O(h+1)}`. A polynomial in
a quantifier-free definition of a singleton must vanish there: otherwise
all nonzero polynomial signs would persist in a neighborhood. For
integer `P(t)=a_d t^d+...+a_0`, with `a_d!=0`, Cauchy's upper root bound
gives

```
theta <= 1 + max_{j<d} |a_j/a_d| <= 1 + max_j |a_j|.
```

Taking a square root yields the stated feasible-point radius. The case
`theta=0` is immediate. This uses an upper root bound, in contrast to
the reciprocal-root argument for positive value separation.

## A second proof of the radius using established sampling

After the same active affine restriction, the real algebraic set

```
Z = {u : q_j(u)=0 for every selected basis row j}
```

is nonempty, since it contains `u*`. Every point in `Z` satisfies all
retained inequalities, because every retained polynomial is a linear
combination of the basis polynomials. Hence its squared norm after the
affine map is at least `theta`.

[Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
Sampling in real algebraic sets*](https://arxiv.org/pdf/cs/0403008v3),
Theorem 1.2, applies to `p(Y)=sum_j Y_j^2` and the at most `h` basis
quadratics. It gives a sample in `Z` by a real univariate representation
whose degrees and coefficient bit lengths are `N^{O(h+1)}`. The theorem
does not assume that `Z` is bounded. Its definition of a univariate
representation gives coordinates `g_j(alpha)/g_0(alpha)`, where
`f(alpha)=0` and `f` and `g_0` are coprime.

For completeness, degree and height bounds for that representation do
bound the coordinate magnitudes, even though the denominator is
algebraic. If all degrees are at most `D` and coefficient bit lengths
at most `H`, then

```
R_j(Y) = resultant_T(f(T), g_0(T)Y-g_j(T))
```

is a nonzero integer polynomial vanishing at the represented coordinate.
It is nonzero because its leading coefficient in `Y` is the nonzero
resultant of `f` and `g_0`, up to the harmless leading-coefficient
convention. Its degree is at most `D`, and the Sylvester determinant
bounds coefficient bit lengths by `O(D(H+log(D+1)))`. The upper root
bound therefore gives `|g_j(alpha)/g_0(alpha)|<=2^{N^{O(h+1)}}`.
The rational affine map has polynomial-bit coefficients and preserves
this order of magnitude. If there are no basis rows, use `u=0`
directly.

The resulting point need not satisfy the original deleted inequalities.
This is harmless: its norm is an upper bound on the minimum norm of
the reduced problem, which equals the original minimum norm. Thus the
original minimizer obeys the same radius bound. This argument supplies
an independent route to the radius using established sampling, while
the compressed KKT argument additionally proves an annihilator bound
for the minimum squared norm itself. The sampling theorem alone is
not cited as an exact optimization theorem; the paper's Theorem 1.5
announces an optimization extension whose proof is deferred.

## Consequences and checks against overstatement

Adding the resulting rational box preserves feasibility. The bounded
exact-feasibility theorem therefore gives polynomial Turing-time decision
for every fixed `h`, without an input box. A safe black-box composition
of the displayed bounds is `N^{O((h+1)^2)}`. No claim about obtaining a
rational original feasible point follows.

For integer variables with explicit finite input bounds, substitution of
any integer assignment leaves slice coefficients of polynomial bit length,
uniformly over every assignment. Its continuous Hessian matrices remain
the `xx` blocks of the original quadratics. The radius theorem therefore
supplies one continuous box meeting every nonempty integer fiber. Appending
that box preserves the feasible integer projection. The existing MILP
construction then applies when the full original quadratics are jointly
convex. Slice convexity alone suffices for the radius argument but does
not justify that MILP construction.

The assertion is about preservation of feasibility of each fiber. The
new box need not contain every original point of a feasible fiber. For
objective-threshold decision, apply the radius argument to the system
with that threshold row included; the objective's continuous Hessian can
increase the span dimension by one. A box proved only for feasibility
must not silently be used to preserve arbitrary objective values.

No integer bound is removed by this reasoning. In particular, the
uniform-slice argument uses the polynomial bit length of each bounded
integer assignment. Substituting unrestricted integers does not have
that property.

The classical repeated-squaring example is a useful boundary check:
`x_1>=2`, `x_{i+1}>=x_i^2` forces
`x_n>=2^{2^{n-1}}`. Its `n-1` native Hessians are independent. Thus
convexity alone does not give a polynomial-bit radius in arbitrary
dimension, and the example does not contradict the fixed-span result.

## Source audit and novelty limits

[Basu and Roy, *Bounding the radii of balls meeting every connected
component of semi-algebraic sets*](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
Theorem 4 and Remark 1, give an explicit radius meeting all components
of a general polynomial sign system. Its asymptotic scale is
`2^{tau d^{O(n)}}`, with ambient dimension `n`, degree `d`, and coefficient
bit bound `tau`. The candidate's additional conclusion is a bound
controlled by the native Hessian matrix span for convex quadratic
systems; it is not the first general feasible-point radius theorem.

[Basu's 2014 survey](https://arxiv.org/abs/1409.1534), Theorem 2.27,
states the coefficient-sensitive block quantifier-elimination bound used
above: output integer bit lengths are linear in the input coefficient
bit bound, multiplied by the degree factor determined by the block
sizes. The locally stored primary text was read at
`research-20260925/publication-sources/basu-2014-author-survey.txt`.
Theorem 2.20 and Remark 2.21 also state the earlier general radius bound.

That linear bit-height dependence offers a sharper composition than
the conservative black-box `h^2` exponent: adding the radius box changes
coefficient bit lengths to `N^{O(h+1)}` while leaving dimensions, degree,
and row counts polynomial in the original `N`. Rational elimination and
determinant formation have a polynomial dependence on those bit lengths
with an absolute exponent. Applying Theorem 2.27 again therefore still
gives `N^{O(h+1)}` output bits. This refinement should be stated only
with the separated dimension/height bookkeeping; it does not follow by
substituting into an undifferentiated input-length bound alone.

[Bienstock, Del Pia, and Hildebrand, *Complexity, Exactness, and
Rationality in Polynomial Optimization*](https://arxiv.org/abs/2011.08347),
Introduction and Example 6.1, distinguish rational witnesses, exact
decision, and small approximate witnesses and record the convex
repeated-squaring obstruction. The local full text was inspected at
`literature/papers/bienstock2023-complexity-exactness-and-rationality-in/fulltext.md`.
Its discussion of few-quadratic algorithms explicitly warns that
arbitrarily many affine inequalities do not automatically fit those
algorithms. The candidate exploits convexity and a value-encoding proof
instead of enumerating affine active sets.

The targeted searches and inspected sources did not identify an equivalent
unbounded theorem stated in terms of the Hessian matrix span. This is
limited evidence, not a novelty certificate. The extension also shares
the main compressed-KKT mechanism of the bounded theorem and should be
presented as part of that contribution, not as an unrelated second advance.

## Verification record

The work in this review consisted of an independent derivation, a
symbolic audit of every proof step above, inspection of the relevant
bounded theorem, exact-feasibility manuscript, and complete unbounded
draft, and targeted reading of the named primary sources. The general
radius, QE, and few-quadratic sampling results were
read directly, not inferred from search snippets. Targeted web searches
covered small feasible points of convex quadratic systems, Hessian
span, and bounds for quadratic inequalities.

A targeted `python -` check of this review passed: final newline,
trailing whitespace, control characters, and its one local Markdown
link target. This was a document check, not a mathematical test or a
CI result.

No numerical calculation or Lean proof was used: neither would settle
the general quantifier-elimination and bit-complexity arguments by
testing instances. No project-wide verification or CI inspection was
performed.
