# Independent review of the native-Hessian-span value theorem

Date: 2026-09-27. Reviewer: `hessian_span_review`.

The compressed-KKT proof in
[the Hessian-span note](hessian-span-reduction.md) is correct under its
stated assumptions: explicit rational convex quadratics, a supplied finite
rational coordinate box, and a nonempty feasible set. No Slater condition is
needed for the value theorem. The objective must be convex for this proof;
its Hessian need not lie in the native Hessian span.

The claimed degree and coefficient-bit bound is
`L^{O(h+1)}`, where `h` is the dimension of the linear span of the native
constraint Hessians. The theorem bounds an algebraic optimal value. It does
not directly find the unknown active affine space or return an optimal
point. Exact feasibility decision follows from the value gap and the
relaxed-feasibility argument below. That implication is separate from the
algebraic-value proof.

This review began independently of the author. It supplied the alternative
compressed-KKT argument, including the use of active rows to obtain `h`
native multipliers and the fixed-support subsequence. The resulting proof
was subsequently reread in full. The root reviewer separately audited these
new steps; this document alone should not be described as a wholly
independent post hoc audit of a proof to which its author contributed.

**Active affine restriction.** Fix an original optimizer `x*`. Impose all
original affine equalities and all affine inequalities active there as
equalities, retain the active nonlinear inequalities, and delete the
inactive inequalities. A lower-value point of this system would give a
lower-value original feasible point on a short segment from `x*`: convexity
preserves the retained inequalities, while continuity and strict slack
preserve the finitely many deleted rows sufficiently near `x*`. The
objective improves on every nontrivial part of that segment by convexity.
Thus the optimal value is unchanged.

The resulting set need not contain the original feasible set: imposing an
active affine inequality as an equality is a restriction. Calling this a
reduced problem is more precise than calling it an enlarged problem. This
wording issue does not affect the segment proof.

Choose a rational Hessian basis among the retained nonlinear rows. For each
retained row, subtract its rational Hessian combination. The remainder is
an affine polynomial and vanishes at `x*`, because the rows used in this
identity are all active there. Imposing these affine remainders as
equalities preserves `x*` and therefore the optimal value. After rational
elimination, the whole retained polynomials, including affine and constant
parts, span a space of dimension at most `h`.

This last point is essential. A small Hessian span alone does not bound the
span of the gradients, because the original affine parts may vary in many
independent directions. The proof obtains the needed polynomial identities
only after restricting to an affine space containing the optimizer.

All equations of that affine space are rational. Their construction does
not substitute the possibly irrational coordinates of `x*`. Gaussian
elimination therefore gives polynomial-bit rational data. Free variables
can be original coordinates; the original box then bounds the retained
optimizer in those coordinates. The added ball is strict at it. A
zero-dimensional affine space is a rational point and must be handled
before introducing the determinant formulas.

**Regularization and sparse multipliers.** Relax every retained native
inequality to `q_i(u) <= epsilon`, relax the added ball by the same positive
amount, and add `epsilon ||u||^2` to the objective. The old optimizer is
strictly feasible. The ball gives a common compact bound for
`0 < epsilon < 1`. Slater and convexity give KKT multipliers, and the
regularized objective Hessian is positive definite.

Write `q_i = sum_j c_ij q_j` in the retained polynomial basis. At a
regularized optimum, discard zero multipliers and use only rows satisfying
`q_i = epsilon`. The native multiplier contribution depends on
`eta = sum_i lambda_i c_i` in a space of dimension at most `h`. Conic
Caratheodory compresses this vector to at most `h` of those same active
rows. The polynomial identities preserve their aggregate gradient.
Nonnegativity and complementarity survive because only active rows were
used. Keep the ball multiplier separately. This yields at most `h+1`
multiplier variables.

Neither nonnegative coefficients in a Hessian basis nor a small number of
extreme rays of the full Hessian cone is required. Arbitrarily chosen basis
rows cannot simply replace all inequalities. All retained primal
inequalities must remain in the determinant feasibility formula, including
the rows outside the sparse multiplier support.

The original multipliers can diverge as `epsilon` tends to zero. This is
harmless. The proof requires existence for each regularized problem, not a
bounded multiplier sequence. Compactness bounds the primal variables and
proves convergence of the regularized optimal values.

**Determinants and the scalar limit.** With the fixed sparse support, the
stationarity matrix is the sum of the convex objective Hessian,
`2 epsilon I`, and nonnegative multiples of convex constraint Hessians. It
is positive definite, including when every original Hessian is singular.
The adjugate reconstruction therefore has a strictly positive determinant.
Multiplying constraints by its square preserves their signs.

A certificate reconstructed from the polynomial formula satisfies primal
feasibility for every row, nonnegative multipliers, complementarity, and
stationarity. Convexity makes it a global optimum. This proves the reverse
direction of the formula; treating the determinant equations as only
necessary conditions would not suffice.

Choose regularization parameters tending to zero. There are finitely many
possible sparse supports, so one occurs along a subsequence tending to
zero. Its limit formula defines exactly the singleton containing the
unperturbed optimum. The support need not work for every sufficiently
small parameter. A universal scalar tolerance and the existential
regularization parameter, value, and multipliers give two blocks of sizes
`1` and at most `h+3`, with one free scalar.

I independently checked the degree and integer coefficient-height clauses
of [Basu's survey, Theorem 2.27](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf),
using the local source
`research-20260925/publication-sources/basu-2014-author-survey.txt`.
With these block sizes, degree `O(L)` and polynomial input coefficient
bits, both output degree and output coefficient bits are `L^{O(h+1)}`.
The source's coefficient-height statement is needed; an arithmetic
operation bound by itself would not prove this conclusion.

Denominator clearing deserves an explicit justification. There are only
polynomially many restricted input coefficients. Choose a common positive
denominator `D` for those coefficients, with polynomial bit length. The
determinant, adjugate, and constraint numerators have denominators dividing
`D^{O(d)}`. Clearing them therefore costs polynomially many bits, even
though the expanded determinant can have `L^{O(h+1)}` monomials. An
uncontrolled least common multiple over arbitrary output coefficients
would not be an adequate substitute for this argument.

After elimination, a singleton description must include a nonzero
polynomial vanishing at its point: otherwise all nonconstant signs would
remain unchanged in a neighborhood. Removing a factor of the indeterminate
and applying the reciprocal Cauchy root bound proves separation of a
nonzero value from zero. No rationality of that value is assumed.

The main proof does not depend on the deferred optimization theorem in
Grigoriev--Pasechnik or on the rank formula in Kamminga--Rudolph. Their
few-quadratic methods remain important prior results, but the direct proof
avoids the extra degeneration and row-deletion issues of that alternative
route. I have not independently reproved their general critical-point
machinery.

**The exact feasibility implication.** Here is a direct algorithmic bridge
that does not assume strict feasibility of the original system or an
approximate optimizer that is exactly feasible for it.

Put all native and affine row violations, including both signs of affine
equalities, in

```
v(x) = max(0, g_1(x), ..., g_M(x))
```

on the supplied rational box `B`. Eliminate coordinates whose lower and
upper bounds agree. If no free coordinates remain, evaluate the rows
directly. Otherwise `B` is full dimensional. Its center `c` and the
half-width lower bound

```
r_B = min_j (upper_j-lower_j)/2 > 0
```

are rational with polynomial bit length. Obtain rational bounds `M >= 1`
and `G >= 1` for all `|g_i|` and all Euclidean gradient norms on `B`.
Expanded rational quadratic input gives such bounds with polynomial bits.

The epigraph problem for `alpha = min_B v` is always nonempty after adding
a polynomial-bit upper bound for its epigraph coordinate. Its objective is
linear and its native Hessian span remains `h`. The value theorem supplies
an effective universal gap

```
alpha = 0  or  alpha >= Delta = 2^{-N^{C(h+1)}}
```

for a sufficiently large fixed constant `C`. Choose
`epsilon = Delta/2 <= 1/2` and consider

```
K_epsilon = {x in B : g_i(x) <= epsilon for every i}.
```

If the original system is infeasible, then `K_epsilon` is empty. If it is
feasible at `x*`, set

```
t = epsilon/(4M),
y = (1-t)x* + t c,
r = min(t r_B/2, epsilon/(4G)).
```

Convexity gives `g_i(y) <= t M = epsilon/4`. The distance of `y` from each
box face is at least `t r_B`. For every `z` with `||z-y|| <= r`, the
segment from `y` to `z` stays in `B`, and the gradient bound gives
`g_i(z) <= epsilon/4 + G r <= epsilon/2`. Thus a ball of the explicitly
bounded radius `r` lies in `K_epsilon`. The center `y` need not be known.
Both the outer radius and `log(1/r)` have size polynomial in
`N + log(1/Delta)`.

At a rational query point, first separate a violated box row if necessary.
Inside the box, a violated convex row gives the rational cut

```
gradient g_i(x) dot (z-x) <= epsilon - g_i(x) < 0.
```

The supporting-gradient inequality proves its validity for `K_epsilon`.
A zero gradient at a violated row proves that this sublevel set is empty.
These evaluations and cuts have polynomial bit complexity in the input
and query length.

A finite-precision ellipsoid feasibility method now distinguishes the two
promised cases: the relaxed body is empty, or it contains a ball of radius
at least `r`. It either finds a rational point in that body or obtains a
containing ellipsoid of volume smaller than such a ball. Only the former
case is compatible with original feasibility. Its bit running time is
polynomial in `N + log(1/Delta)`, hence `N^{O(h+1)}`. The unknown active
affine space in the value proof never has to be found by the decision
algorithm.

The precise finite-precision source is Groetschel, Lovasz and Schrijver,
[*Geometric Algorithms and Combinatorial Optimization* (1988)](https://www.zib.de/groetschel/pubnew/paper/groetschellovaszschrijver1988.pdf),
Theorem 3.2.1, printed pages 87--88. I independently read its statement,
the displayed algorithm, and its acceptance step in the downloaded text
`/tmp/penalty-gls1988.txt`. Definition 2.1.16 supplies the circumscribed-set
input convention. There is no supplied inner center in the theorem input.
The theorem returns an approximate member or a tiny-volume containing
ellipsoid in oracle-polynomial bit time. Its implementation takes the
membership branch only when the separator accepts a queried center. Our
separator accepts only actual members, so this particular invocation
returns an actual relaxed feasible point on that branch. Taking the volume
tolerance smaller than `(r/d)^d` makes the other branch impossible when
the promised ball exists. For dimension one, rational interval bisection
has the same conclusion; the zero-dimensional case was already handled.

I also independently reread the complete resulting
[exact-feasibility note](hessian-span-exact-feasibility.md), whose
normalization to the cube and slightly different constant factors give the
same proof. No substantive gap was found. Its bounded mixed-integer NP
consequence requires rational quadratic input, or an explicit promise that
fixing a polynomial-bit integer assignment leaves a polynomial-size
convex-quadratic instance. Convex continuous slices alone, for an
unspecified general representation, would not be enough. The author
incorporated this correction by specifying explicitly encoded rational
polynomials of total degree at most two and finite rational boxes.

The earlier [GLS paper (1981), Section 2 and Theorem 3.1](https://ir.cwi.nl/pub/10046/10046D.pdf)
was also read. The 1988 theorem is the more direct source because its input
does not require a known inner center. No ellipsoid implementation or
independent proof of the source's rounding estimates is supplied here.

**An exact irrational singleton in the stated class.** The distinction
between exact decision and a rational feasible output is real even for
three rank-one native Hessians. Let `t` be the positive real cube root of
`2`, and impose, on `[0,2]^2`,

```
q_1(x,y) = x^2-y <= 0,
q_2(x,y) = y^2-2x <= 0,
q_3(x,y) = (x-y)^2-y-2x+4 <= 0.
```

Each polynomial is convex with integer coefficients. Their Hessians have
rank one and span the three-dimensional space of symmetric two-by-two
matrices. All three rows vanish at `(t,t^2)`. The coefficients

```
t^2-t/2,  1-t/2,  t/2
```

are positive. Their weighted sum `p` has zero value and zero gradient at
`(t,t^2)`, and Hessian

```
[[2t^2, -t], [-t, 2]],    determinant = 3t^2 > 0.
```

Consequently `p >= 0` everywhere, with equality only at `(t,t^2)`.
Feasibility implies `p <= 0`, so the feasible set is exactly this irrational
singleton. This explicit example was derived during the review and is not
asserted to be novel. It avoids conflating convex quadratic polynomials
with general second-order-cone constraints: squaring a norm inequality can
produce an indefinite Hessian, which would be outside the theorem.

**Parameters and counterexamples to simpler explanations.** The bound is
not controlled by the maximum rank of a single native Hessian. The
square-root-sum comparison

```
sum_i sqrt(a_i) >= b
```

is equivalent to feasibility of `x_i^2 <= a_i`, `x_i >= 0`, and
`sum_i x_i >= b`, with explicit rational boxes. Every nonlinear row has
rank one, but their Hessian span has dimension equal to the number of
terms. Thus fixed `h` does not settle the unrestricted comparison problem.

For `h <= 2`, the pointed cone generated by PSD Hessians has at most two
extreme rays. Lifting a quadratic epigraph for each ray reduces the system
to at most two native nonlinear quadratics plus arbitrary affine rows.
That case already follows from the fixed-count result. The span theorem
first adds a substantially different family at `h=3`.

For example, for distinct rational `s`, the matrices

```
Q(s) = [[1,s],[s,s^2+1]] tensor I_d
```

are positive definite, have rank `2d`, and span a space of dimension three.
Every sampled matrix generates an exposed ray of the cone generated by the
samples: on the two-by-two coefficients, the functional

```
Q_22 - 2s Q_12 + (s^2-1) Q_11
```

takes value `(t-s)^2` at `Q(t)`. The number of cone generators is therefore
unbounded even though the span dimension is three. The main note uses an
equivalent diagonal moment-curve example. This rules out an explanation
that simply replaces all Hessians by `h` nonnegative generators.

**Prior comparison and significance.** I read the repository's fixed-count
proof and independent audits, Basu's coefficient-height theorem, the
Kamminga--Rudolph full version's stated QCQP scope, and the original GLS
ellipsoid source. The local fixed-count proof already provides the
regularization, determinant reconstruction, singleton elimination, and
penalty transfer. The new part in this argument is the rational active
affine restriction followed by compression in the native polynomial span.

Additional web queries on 2026-09-27 included combinations of “convex
quadratic,” “Hessian span,” “linear span,” “number of distinct Hessians,”
“same Hessian,” “independent quadratic forms,” and “rational feasible
point.” No matching general span-based encoding or exact-decision theorem
was identified. This is a limited search, not evidence of priority. Some
same-Hessian and few-constraint QCQP reformulations already exist; their
presence makes it especially important to distinguish the `h<=2` case
from arbitrary constraint cones in span three or more.

The value theorem and exact-decision consequence appear more consequential
than a sufficient-penalty bound alone. They identify a computable structural
parameter that controls exact precision despite many rows, high rank, and
failure of Slater. They do not yet provide practical penalty calibration,
an efficient method for recovering the algebraic optimizer, or measured
solver acceleration. The rational box is essential to the present proof;
unbounded input and unattained infima have not been covered.

**Targeted verification.** Ran

```
python research-20260927/check_hessian_span_review.py
```

All three checks passed. SymPy verified the irrational singleton's exact
vanishing and stationarity identities modulo `t^3-2`, the ranks and span of
its Hessians, the exposing identity for seven positive definite Hessians
in span three, and an exact compression of seven active multiplier
coefficients to three preserving the whole aggregate polynomial. These
checks challenge concrete algebra and distinguish linear span from conic
generation; they do not prove quantifier elimination, general conic
Caratheodory, or ellipsoid bit complexity. No Lean build, project-wide
verification, or CI inspection was performed.
