# Independent review of unbounded mixed-integer quadratic optimization

Date: 2026-09-27. Status: review completed after one missing algorithmic
justification was supplied. No remaining gap was found in the attainment,
status classification, optimal integer-assignment, or optimal-value argument.
This is independent proof review, not formal verification or a priority claim.

The reviewed manuscript is
[mixed-integer-attainment-frontier.md](mixed-integer-attainment-frontier.md).
The reviewer did not develop its recession elimination or original-coordinate
witness argument. A fresh subreviewer independently checked Sections 3--4
and the relevant primary-source statements. The final exact continuous-vector
output has a separate dependency on
[exact-convex-optimizer-recovery.md](exact-convex-optimizer-recovery.md), which
is being reviewed separately; this note does not replace that review.

## Scope and verdict

The input has rational affine rows and globally positive-semidefinite
quadratic rows, including its convex quadratic objective. Integer and
continuous variables may both be unbounded. The parameters are the number
`k` of integer variables and the dimension `h` of the span of the constraint
Hessians restricted to the continuous variables. The objective Hessian is
excluded from `h`.

Subject to the explicitly linked feasibility, compressed-projection, and
continuous-value results, the manuscript establishes polynomial Turing
complexity for every fixed `k,h`. It does not establish an FPT bound, a
practical exponent, or an exactly rational continuous optimizer. The
qualitative finite-attainment proof does not require fixed `k,h`.

The draft originally cited a bounded-integer, unbounded-continuous
optimization reduction that was not actually stated in the linked notes.
The bounded MILP note had boxes on both types of variables, while the radius
note only transferred feasibility, integer-only objectives, and supplied
thresholds. A feasible-point radius does not preserve the minimum of an
unrelated continuous objective. The author independently noticed the same
missing step and added the threshold-specific argument in Section 5. I
reread that addition and found it sufficient. The correction is described
below.

## Rational recession elimination

For a nonempty sublevel of the feasible set, expanding each PSD quadratic
along a recession direction `d` first gives `d^T Q_i d=0`. PSD then gives
`Q_i d=0`, so the cross term vanishes and the remaining condition is the
linear inequality `a_i^T d<=0`. The affine equations give `E d=0`.
Including the objective row yields a rational polyhedral cone independent
of the numerical objective threshold.

A strictly negative objective slope in this cone gives a rational such
direction. Scaling its integer components to integers produces an objective
sequence tending to minus infinity from any mixed-integer feasible point.
The preliminary feasibility check is essential; the manuscript performs it.

If all objective slopes are zero, choosing a nonzero rational direction
allows exact dimension reduction. Every row has the form

```
r_i(y) + alpha_i t <= 0,    alpha_i <= 0.
```

Rows with negative slope can all be satisfied by one sufficiently large
`t`. This remains true if `t` must be integral, by rounding upward. Rows
with zero slope, affine equalities, and the objective are independent of
`t`. Thus the reduced system preserves all attained objective values, not
merely their closure or infimum.

For a direction with zero integer component, choosing a nonzero continuous
coordinate and restricting it to zero selects one representative on every
parallel line. Since retained rows are constant on such lines, their encoded
restrictions literally delete coefficients. No denominator from the
direction is introduced into the reduced rows.

For a direction with nonzero integer component, positive rational scaling
gives a primitive integer vector `p`. A unimodular completion `U` and the
shear `x=x'+d_x t` give a bijection of the mixed lattice. Restriction to
`t=0` substitutes only the remaining columns of `U` into the integer
variables; the continuous coordinates remain unchanged. Consequently full
PSD is preserved by congruence, and the span of the continuous Hessian
blocks cannot increase.

At most `k` eliminations need a unimodular change. Each has polynomial bit
growth in the current data. All other eliminations merely remove
coefficients. A fixed number of polynomial growth steps stays polynomial in
the original input length for fixed `k`; the number of intervening rational
LP calls is polynomial. This justifies the claimed effective reduction
without assuming a polynomial bound on naive back-substitution.

If the recession cone becomes zero, each nonempty objective sublevel is
closed and bounded, hence compact. Its intersection with the mixed lattice
is closed. A nonempty such intersection has a minimum, and points outside
that sublevel cannot improve it. This completes the attainment and status
classification argument.

One boundary example explains why repeated elimination is necessary.
Minimizing `-u` over `u^2<=v` is unbounded below, but every recession direction
of its sublevels has `d_u=0` and therefore zero objective slope. Eliminating
the harmless `v` direction drops the quadratic row and exposes the remaining
unbounded linear objective. The manuscript correctly tests reduced problems
and does not claim that every unbounded original problem has a strictly
decreasing original recession ray.

## Compact terminal projection and algebraic value

The small integer-witness theorem gives a terminal feasible integer
assignment of polynomial bit length for fixed `k,h`. Substituting any such
assignment has uniformly polynomial encoding size. The continuous-radius
theorem then gives a feasible representative of polynomial coordinate bit
magnitude. Bounding the rational objective on the resulting known coordinate
box supplies a computable polynomial-bit upper threshold `B`; constructing
the actual representative is unnecessary.

The terminal set `K=C intersect {q_0<=B}` is nonempty and compact. Its real
projection `Y` on the integer-coordinate positions is compact and convex.
Adding the objective threshold increases the continuous Hessian span by at
most one.

The compressed formula for `Y` has many charts but only three quantified
blocks. Projecting onto one coordinate places the other `k'-1` real
coordinates in the outer existential block:

```
exists (z_{-j}, R), for all t, exists lambda: chart predicates.
```

Its block sizes are at most `k',1,max(1,h+1)`. Moving `z_{-j}` inside the
universal tolerance quantifier would be invalid; the manuscript does not do
so. The free set is a nonempty compact interval, possibly a singleton.

The original
[Khachiyan--Porkolab paper](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Proposition 2.1 on printed page 211, explicitly bounds output polynomial
degrees and coefficient bit lengths independently of the number of atomic
predicates. Predicate count affects formula size and elimination runtime.
Here quantifier elimination supplies a size bound only; the algorithm never
constructs the large formula. Thus the chart count does not invalidate the
claimed endpoint bound.

After identically zero atoms are removed, every interval endpoint must be a
root of some remaining nonzero polynomial. Otherwise all signs are locally
constant and the endpoint is not a boundary point. This includes singleton
intervals. If output coefficients have at most `H` bits, an upper Cauchy
bound such as `2^(H+1)` bounds all endpoints. For fixed `k,h`, the logarithm
of this bound is polynomial in the input length.

Some terminal optimal integer assignment therefore has polynomial bit
length. The continuous value theorem applies after fixing it and gives an
annihilator of the common terminal and original optimum with polynomial
degree and coefficient bit length. Exact recession projection, already
proved separately, is what transfers the value back to the original system.

## Original-coordinate optimal integer witness

The existence of a small terminal integer assignment does not by itself
bound the original assignment obtained by sequential lifting. The manuscript
correctly avoids that inference.

Let the optimal value `v` have an integer annihilator of degree at most `D`
and coefficient bit length at most `H`, both polynomial for fixed parameters.
Square-free reduction and real-root separation give a dyadic interval
isolating the selected root with bit length polynomial in `D,H`. The root
magnitude bound is polynomial in bits too. For example a conservative
`O(D(H+D+log D))` bit bound suffices after polynomial height growth in
square-free reduction.

Adjoin a real threshold `T`, its annihilator equation, and this isolating
interval to the compressed projection formula for `q_0<=T`. The threshold
changes constant terms in the parameter-dependent affine restrictions;
it does not create extra continuous Hessian directions beyond the objective
row. The prefix becomes

```
exists (T, R), for all t, exists lambda: polynomial predicates.
```

The final free-variable set is precisely
`{z: exists x, (z,x) in C, q_0(z,x)<=v}`. It is convex by joint convexity
and contains an integer point by the independently established attainment
argument. The isolated-root predicates need not themselves define a convex
set in all quantified variables. Only convexity of the resulting free `z`
set is needed.

Khachiyan--Porkolab Theorem 1.1 on printed page 208 permits arbitrary Boolean
formulas and bounds an optimal integer point from the atom degree, coefficient
bits, free dimension, and quantified block sizes. Its bound does not depend
on predicate count. Adding an integer coordinate fixed to zero converts
feasibility to its stated optimization problem, exactly as the source
explains immediately before the theorem. Applying that result gives the
claimed polynomial-bit original optimal integer assignment.

There is no circular computation of `v`: this application uses existence of
an annihilator and isolating interval with uniform size bounds. Those bounds
give a conservative witness box even when neither polynomial nor interval
has yet been computed. The actual optimization algorithm subsequently works
inside that box.

## The repaired bounded-integer optimization step

After the original integer coordinates are boxed, every nonempty integer
fiber has a finite attained continuous optimum. Global boundedness below
has already been established. Uniform substitution size and the unbounded
continuous value theorem give common degree, coefficient, and magnitude
bounds for all fiber optima.

The resultant argument from the bounded optimization note gives a common
positive separation between distinct fiber optimum values, whose inverse
has polynomial logarithm for fixed parameters. The number of possible
integer assignments need not be polynomial: the argument bounds all pairwise
differences by their algebraic degree and height, without enumerating them.

Bisection begins with a strictly lower endpoint and an upper endpoint at
which a feasible assignment exists. Each threshold inequality is added
before invoking the continuous-radius theorem. Thus the resulting continuous
box preserves feasibility of that specific threshold in every bounded
integer fiber. The bounded MILP reduction is applicable to each such boxed
query, even though the radius can change between thresholds.

Once the interval width is smaller than the uniform separation, any integer
assignment feasible at the upper endpoint has globally minimal fiber value.
A strictly larger fiber value would differ from the true minimum by at least
the separation, contradicting the bracket width. This proves the optimal
integer-assignment conclusion without relying on the separate exact-vector
recovery theorem. Fixing that assignment permits the reviewed continuous
value algorithm to return the exact algebraic optimum.

## Verification and limits

This review read the entire primary manuscript and the relevant projection,
continuous-radius, continuous-value, and bounded optimization dependencies.
The primary Khachiyan--Porkolab PDF was inspected directly, including the
precise coefficient-sensitive and integer-witness statements. A fresh
subreviewer independently checked the endpoint and isolated-threshold steps
against the same primary source and found no gap.

The targeted source commands were `rg`, `sed`, and `pdftotext -layout` on
the named manuscripts and the repository's Khachiyan--Porkolab PDF. The PDF
was also opened at its linked public source. A local inline Python check
of this new review's newline, trailing whitespace, control characters, and
relative Markdown links passed. No numerical test, Lean proof, project-wide
verification, or CI inspection was performed.

The exact continuous-vector construction is a separate proof obligation.
Literature priority and the optimality of the parameter dependence are not
established by this audit. The strongest supported conclusion of this review
is that the stated complexity argument, with its corrected threshold step
and explicitly named dependencies, has no identified mathematical gap.
