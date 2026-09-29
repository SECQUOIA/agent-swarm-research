# Independent review of integer-coordinate optimization

Date: 2026-09-27. Status: symbolic proof review completed. No
remaining gap was found in the integer-objective corollary in
[unbounded-integer-frontier.md](unbounded-integer-frontier.md). A second fresh
reviewer independently checked the cutoff argument and its boundary cases,
with the same conclusion. The initial assignment was an independent review
of its linear-objective case; neither reviewer devised that case. During
review, this reviewer proposed the extension to convex quadratic objectives
depending only on the integer variables. The parent reviewer and the second
reviewer independently checked that extension. Its proof is recorded below
with this provenance, rather than presented as an independent discovery by
this reviewer. This is evidence from adversarial review, not formal
verification or a priority claim.

## Scope and dependencies

The reviewed objective is rational, convex quadratic, and depends only on
the integer variables. The linear case `c^T z` is considered first below.
The original constraints are rational affine rows and jointly
convex quadratic inequalities; there are `k` integer variables and the
continuous Hessian blocks have matrix-span dimension `h`. No variable
bounds are assumed.

This review takes the preceding exact feasibility theorem and its compressed
projection formula as established dependencies. It independently checks the
new use of an optimal-point bound, the unboundedness test, the encoding
lengths, and recovery of an optimal integer assignment. It does not repeat
the earlier projection or MILP proofs.

## Proof audit

Write `c=a/L`, where `L` is a positive integer and `a` is an integer vector.
One can use the product of the input denominators for `L`; its bit length
is at most their total bit length. Every entry of `a` therefore also has
polynomial bit length. The input size `N` must include the objective data,
as the draft expressly requires.

Adjoin an integer coordinate `w` and the equation `w=a^T z`. The resulting
real projection is the graph of a linear function over the original convex
projection, so it is convex. Adding that equation to the compressed formula
does not change its quantified block sizes or its continuous Hessian span.
Its individual degrees and coefficient lengths remain polynomial in `N`.

The primary text of [Khachiyan and Porkolab (2000), Theorem
1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
page 208, was checked directly. It bounds all coordinates of some optimal
integer point when minimizing the last coordinate over a convex set defined
by a first-order formula. The bound depends on the number of free variables,
quantified block sizes, polynomial degrees, and individual coefficient
lengths; it does not depend on the number of atomic predicates. This is
exactly the optimization form needed for the augmented projection.

The free integer dimension is now `k+1`. With quantified block sizes
`1,1,max(1,h)`, an effective choice

```
B = 2^ceil(N^{C(h+1)(k+2)^4})
```

is a conservative bound on the absolute values of all coordinates of some
optimal `(z,w)`, whenever an optimum exists. The extra slack in `k+2` is
harmless. The constant `C` is independent of whether the objective is
bounded. The possibly large chart count is not used as an input-size bound
for an algorithm that constructs those charts.

After original feasibility is established, the feasible objective values
`w` form a nonempty subset of the integers. If bounded below, that subset
has a least element, attained by some feasible integer assignment. This
argument needs neither compactness nor a rational continuous optimizer.
Consequently, in the bounded case the optimal-point theorem applies and
the minimum satisfies `w* >= -B`.

It follows that the original system with the additional affine inequality

```
a^T z <= -B-1
```

is feasible exactly when the objective is unbounded below. If the objective
is unbounded, every finite threshold is feasible. If it is bounded, the
displayed threshold lies strictly below the minimum. This test uses the
bound for the original augmented objective problem, computed before the
threshold is inserted. It does not assume a size bound for a point satisfying
every arbitrarily negative threshold.

The binary length of `B` is polynomial in `N` for fixed `k,h`. The cutoff
query is therefore an instance of polynomial length with unchanged
parameters. The already-proved feasibility algorithm can be applied to
that enlarged input in polynomial time. Its own internal witness bound can
be larger without causing circularity; composing these polynomial bounds
preserves polynomial time at fixed parameters.

For a finite optimum, imposing `||z||_infinity <= B` retains an optimal
assignment by the same optimal-point theorem. The continuous-radius and
bounded integer-projection results therefore justify the initial draft's MILP
optimization route. The MILP must preserve integer assignments, not the
original continuous feasible vectors: that is sufficient because the
objective uses only `z`.

There is also a shorter constructive finish. The finite optimal integer
value lies in `[-B,B]`. Binary search over integer thresholds
`a^T z <= t`, using the unbounded exact feasibility algorithm, finds its
least feasible threshold in `O(log B)` calls. The algorithm's feasible
integer assignment at that threshold is optimal. Dividing its integer
objective value by `L` gives the exact rational optimum. This alternative
uses no additional optimization theorem. The saved strengthened corollary
uses this bisection argument; the initial MILP route was also valid.

## Extension to convex quadratic objectives

Let the objective be a rational convex quadratic polynomial `f(z)`. Clear
the denominators of its actual monomial coefficients to obtain
`p(z)=L f(z)` with positive integer `L` and integer polynomial
coefficients. This includes the constant term and any factor `1/2` used in
a matrix representation. The data remain of polynomial length, and `p` is
integer-valued on every integer vector.

In place of the linear equality, use the integer epigraph coordinate

```
p(z) <= w,   w integer.
```

The row `p(z)-w<=0` is jointly convex in all variables because `p` is
convex and `w` occurs affinely. Its Hessian in the continuous variables is
zero, so the continuous Hessian span remains `h`. The augmented real
projection is convex and has the same compressed-formula degree and
coefficient bounds. The optimal-point theorem therefore supplies the same
form of bound `B` in dimension `k+1`.

For each original feasible integer assignment, `w=p(z)` is an admissible
integer epigraph value. Conversely, every epigraph value is at least
`p(z)`. Thus their minimum values agree, and an optimal epigraph pair has
`w=p(z)`. If the original objective is bounded below, the feasible values
of `p` form a nonempty lower-bounded subset of the integers, so both minima
are attained. The original objective is unbounded below exactly when the
integer epigraph objective is unbounded below.

The cutoff `p(z)<=-B-1` and every binary-search threshold `p(z)<=t` are
admissible convex quadratic rows with zero continuous Hessian. They leave
`h` unchanged and require no extra integer variable in the actual
feasibility calls. Their encoding lengths are polynomial for fixed `k,h`.
The preceding cutoff and bisection arguments therefore return an optimal
integer assignment and exact value `p(z)/L`, or correctly report
infeasibility or unboundedness below.

## Boundary cases and limitations

The expanded saved corollary was read in full. Its maintained bisection
bracket has infeasible lower endpoint `-B-1` and feasible upper endpoint
`B`. This handles the possibility that the optimum equals `-B`, and
termination at adjacent integer thresholds identifies the optimum exactly.

The zero objective causes no exception: its minimum epigraph value is zero
and the negative cutoff is infeasible. If `k=0`, the same reasoning applies
to any rational constant objective after ordinary continuous feasibility.
Large
rational objective coefficients are covered by including their encoding in
`N`. A rational additive objective constant is included when forming `p`.

The proof depends on discrete objective values. It does not extend by the
same argument to a linear objective involving continuous variables. It
returns an optimal integer assignment and a rational value, not an exactly
feasible rational continuous vector. The running time is polynomial for
fixed `k,h`; this does not establish fixed-parameter tractability with an
input-size exponent independent of those parameters.

This corollary combines the new structural feasibility result with an
established optimal-point theorem. Its independent originality was not
assessed here, and no general novelty claim follows from this review.

## Verification record

This was a mathematical proof and primary-source review. No numerical test
is needed to establish the discrete-attainment implication or the cutoff
equivalence, and none was represented as verifying the general theorem.
The targeted inline Python check of this file's final newline, trailing
whitespace, control characters, and local Markdown link passed. No Lean
proof, project-wide verification, or CI inspection was performed.
