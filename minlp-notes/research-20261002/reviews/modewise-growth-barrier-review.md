# Independent review of the mode-wise growth barrier

Date: 2026-10-02. Reviewed
[the barrier note](../new-direction/modewise-growth-barrier.md), its linked
finite-state and projected-growth assumptions, and the local statement of
the continuous forest oracle. This is a mathematical review, not a novelty
assessment or a fresh audit of the external oracle source.

The reduction and its conclusions are sound. The author applied the one
requested correction: the comparison with `(7/3) F` is now non-strict,
so it also holds when `F=0`. There are no outstanding mathematical
corrections. The NO-instance gap and both hardness results are unchanged.

## Audit coverage

**Reduction and encoding.** Removing items above the positive target preserves
SUBSET SUM. Empty and one-item cases are trivial; restricting the hard family
to at least two retained items preserves the hardness conclusion for graphs
of treewidth exactly two. Each coefficient `a_i/(B 2^i)` has polynomial
encoding length, as do the expanded objective and the accuracy requested by
the decision reduction. A zero objective forces both the recurrence and
terminal equation, hence exactly the target subset sum. Conversely, the
recurrence trajectory is
`s_i = (sum_(j<=i) a_j z_j)/(B 2^i)`. It stays in the unit box, either by
the stated induction or by `s_i <= i/2^i <= 1/2`. Thus the box cannot exclude
a successful subset.

**Graph.** The stated bags satisfy the running-intersection property. Their
successive intersections are single state variables. For every `i>=2`,
the three cross terms in the recurrence square are nonzero and cannot cancel
with another factor, so they form an actual interaction triangle. The
terminal unary term requires no additional bag. The graph has width at most
two, and exactly two for `n>=2`.

**Gap and decision threshold.** The residual telescoping identity has the
correct sign. Its exact Cauchy--Schwarz multiplier is
`kappa_n = 1 + sum_(k=0)^(n-1) 4^(-k) = 7/3 - (4/3)4^(-n)`.
Thus `F >= delta(z)^2/kappa_n`. Integer subset sums give the stated
`Delta = (3/7)4^(-n)/B^2` lower bound on every NO instance. For a completely
explicit decision rule, request additive error `Delta/4` and compare a
guaranteed value estimate with `Delta/2`. A certified interval of width
`Delta/4` also separates the cases by its endpoints. A feasible objective
within `Delta/4` of optimum separates them in the same way. The requested
accuracy has polynomial encoding length. This proves weak NP-hardness and
the obstruction to a runtime polynomial in input length and
`log(1/epsilon)`; it makes no strong-hardness or inverse-accuracy claim.

**Curvature and constrained mode minima.** The shift-norm argument gives
`(1/2)||v|| <= ||Dv|| <= (3/2)||v||`, including `n=1`. Consequently the
state Hessian lies between `(1/2)I` and `(13/2)I`. At a constrained mode
minimizer, the gradient has nonnegative pairing with every feasible
displacement. The exact quadratic expansion therefore gives the stated
growth constant `1/4`, including boundary minima. The condition-number
bound thirteen follows. For the full Hessian,
`||[D,-C]||^2 <= ||D||^2 + ||C||^2`, so the bound seven is valid.
Convexity follows from the Gram representation. State diagonal entries are
`5/2` before the terminal state and four at that state; binary entries are
at most `1/2`. The claimed maximum diagonal curvature four is correct.

**Mode growth versus global growth.** The finite-state extension requires
a common optimal exposed vector, and the anchor theorem measures distance
to the projected global optimal set. Neither is supplied by independent
mode minima. In the two-item example, `B>=3` excludes every other zero
mode. Its projected optimal set is the singleton `(1/2,1/4)`. The displayed
competing recurrence point is feasible and gives exactly
`F/dist^2 = 1/(4B^2+1)`. It need not minimize its own mode: global growth
must hold at every feasible pair, so this one point suffices. The example
proves that a uniform mode growth constant does not provide a uniform
projected global growth constant. It does not assert the latter constant
is zero for a fixed instance.

**Binary forest corollary.** With `q_i` denoting the coefficient of
`z_i^2`, adding the displayed unary penalty makes that coefficient
`q_i-max(0,q_i)-1 <= -1`. Fixing all other variables leaves a strictly
concave univariate quadratic, even with arbitrary binary--binary and
binary--continuous cross terms. Replacing a fractional coordinate by a
minimizing endpoint preserves feasibility and cannot increase the
penalized objective. Repeating this step preserves all earlier endpoint
choices. Since the penalty vanishes at binary points, the continuous
penalized optimum equals the original mixed optimum. In fact strict
coordinate concavity already forces every exact continuous global optimum
to have binary coordinates. The rounding argument is nevertheless valid.
The penalties add no graph edges and have polynomial rational encoding
length. Exact endpoint comparisons and objective evaluation have polynomial
bit cost when the supplied optimizer has polynomial bit length.

The forest runtime conclusion relies on the exact rational polynomial-bit
continuous forest box-QP oracle stated in
[the feedback-vertex note](../new-direction/fan-exploration.md). This review
checks the reduction to that oracle, not its externally published proof.
No separate forest solver was run. The corollary concerns binary variables;
it does not establish the same statement for arbitrary integer intervals
or coupled constraints.

## Correction tracking

The original chain `delta(z)^2 <= kappa_n F < (7/3) F` is false at any
successful subset's zero-objective trajectory: it ends with `0 < 0`.
Replace its final `<` by `<=`, or state strictness only when `F>0`.
The coefficient inequality `kappa_n < 7/3` itself is correct. The author
was notified before the numerical checks. A final targeted source read
confirmed that the final `<` is now `<=` and that the note links this
review. There is no other requested mathematical correction.

## Targeted commands and results

Read-only commands used `cat AGENTS.md`, `find research-20261002 -name
AGENTS.md -print`, `rg --files`, `git status --short`, and targeted `cat`,
`rg -n`, `sed -n`, and `nl -ba` reads of the reviewed note, its linked
assumptions, the feedback-vertex note, the local prior-art note, and one
existing review for repository conventions. No additional nested
`AGENTS.md` was found. A final `sed -n` and `tail -16` read confirmed the
author's correction and review links; `wc -l` checked the review artifact.
`git diff --check -- research-20261002/reviews/modewise-growth-barrier-review.md`
returned no output, but the file is untracked, so that command does not
provide a whitespace check of its contents.

Two mathematical check commands actually ran as `python3 - <<'PY'`
invocations. Their bodies were not saved as test scripts; both exited
successfully. A third inline Python invocation using `pathlib.Path`
confirmed the review's final newline, absence of trailing whitespace,
removal of its pending marker, and the source's corrected inequality.

1. **Exact mode and gap checks.** Using `fractions.Fraction`,
   `itertools.product`, and `Random(26100219)`, generate three item tuples
   for each `n in {1,2,3,4}` and `B in {1,3,11,2^40+87}`. For all 360
   binary modes of these 48 instances, independently enumerate every
   active face of the state box and solve its rational stationary system.
   Verify the minimizing point's box KKT signs, the zero-value/subset-sum
   equivalence, recurrence feasibility, and the exact residual lower
   bound. Seventy modes have a boundary minimizer. All 18,648 state samples
   in `{0,1/2,1}^n` satisfy the telescoping identity, Cauchy--Schwarz bound,
   and growth bound relative to the independently obtained mode optimum.
   Also verify four displayed global-growth ratios for
   `B in {3,4,11,2^40+87}` and 475 strict endpoint comparisons for
   `q,c in {-7/3,-1,0,1/5,19/7}` at `t=k/20`, `1<=k<=19`.
   The final assertion confirms the zero-objective counterexample to the
   original strict inequality.
2. **Exact Hessian and graph checks.** For
   `n in {1,2,3,7,12}`, `B in {1,7,2^30+3}`, and
   `a_i=max(1,B-(i-1))`, construct the full rational Hessian directly from
   the residual matrix. Exact Schur-complement elimination verifies
   positive semidefiniteness of `H`, `7I-H`, `H_s-(1/2)I`, and
   `(13/2)I-H_s` in all fifteen cases. Also verify the maximum diagonal
   bound, that the proposed bags cover every nonzero interaction, and the
   existence of the second recurrence triangle when `n>=2`.

These checks support the algebra and boundary cases; the proofs above
establish the general claims. No external research, project-wide checks,
CI status checks, or CI log inspection were performed.
