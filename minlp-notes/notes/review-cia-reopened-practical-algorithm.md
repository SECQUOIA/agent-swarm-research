# Independent review of the exact one-switch algorithm

Date: 2026-09-07. Reviewer: independent practical-algorithm review agent.

Reviewed [the algorithm note](cia-reopened-practical-algorithm.md),
[the implementation](../code/cia_reopened/rounding.py), and
[the author's checks](../code/cia_reopened/check_rounding.py).

## Mathematical conclusion

The three-term discrepancy identity, largest-total final-mode dominance,
three-candidate reduction, and O(nN) exact-arithmetic algorithm are correct.
The restrictions and arithmetic-versus-bit-complexity distinction are necessary
and adequately stated. This review does not establish literature priority.

For any mode, conservation and nondecreasing allocations imply that its
allocation increases by at most elapsed time. Thus active discrepancy decreases
and inactive discrepancy increases on each block, even when the relaxed control
varies inside an input interval. Endpoints therefore suffice. For initial p and
final q, the terms discarded by the displayed identity are controlled by its
retained terms: A_q(t) <= t-A_p(t) and m_p-t <= T-t-m_q.

Replacing final q by a largest-total eligible r removes r from the omitted
set and inserts q with m_q <= m_r. Both the omitted maximum and terminal
deficit cannot increase. With unrestricted final choices, all initial modes
outside the top two then share the same omitted maximum and final deficit;
maximizing their cumulative allocation selects a best one. Ties cause no
problem. Constants have error T-m_p. The implementation handles one and two
modes and a one-interval horizon separately or directly as required.

For the query consequence, if u>t then

    [2u-A_p(u)] - [2t-A_p(t)] >= u-t > 0.

Consequently a binary search for the crossing on the sorted eligible boundaries
is valid. Below the crossing the varying maximum decreases; above it, it is
nondecreasing. Taking the maximum with a constant omitted mass preserves the
claim that one neighboring boundary is optimal. Empty eligible sets require
only constants. O(n log N) additional queries assumes cumulative input and
sorted eligible boundaries already support random access; it is not a claim
about reading or preprocessing an arbitrary allocation table in that time.

## Independent numerical and edge-case verification

The separate [review script](../code/cia_reopened/check_rounding_review.py)
imports only the optimizer. It implements its own cumulative error evaluator,
enumerates all schedules, and separately implements binary search around each
initial mode's crossing. It passed **3,776** comparisons: exhaustive half-integral
three-mode/three-interval profiles with every permitted-boundary subset and
every fixed initial mode, plus rational nonuniform random profiles. Cases
include n=1, n=2, N=1, zero-total modes, ties, empty permitted sets, and duplicated
or unsorted valid boundaries. Ten malformed-input checks initially passed.

The author's script also passed its 530 comparisons and synthetic benchmark.
The latter returned 97301/200 at n=100, N=1000 in 0.285 seconds during this review.
These checks support correctness and prototype speed, not control performance.

## Public profile and precision audit

Downloaded the exact pinned CSV and reproduced its hash, n=3, N=12000, T=12,
optimal quantized discrepancy 1889/1000, and mode 1 to mode 2 at index 1889.
Runtime was 0.221 seconds in this run. The maximum normalization change was
4.9582e-7. The benchmark's direct endpoint enumeration agreed with the optimizer.

Largest-remainder quantization changes each normalized rate by strictly less
than 1e-6. Integrating that bound gives a uniform cumulative perturbation below
12e-6. The absolute discrepancy of each fixed schedule, and then the optimum
over the same schedule set, change by less than that amount. The returned
quantized-optimal schedule is consequently less than 24e-6 suboptimal for the
normalized decimal source. This last assertion concerns cumulative allocation
error only. No state, cost, feasibility, or original-control-task conclusion
follows without further analysis.

The [pinned example script](https://raw.githubusercontent.com/adbuerger/pycombina/6b073fe29984186dccfc7e2108bfba9692a6cc9c/examples/lotka_volterra_multimode.py)
actually takes stride 80 and data columns 4 onward: two weight columns on a
150-interval grid. The reviewed benchmark reads all three CSV weight columns
on the full grid. Both are legitimate inputs, but the benchmark must be described
as a new use of the published data, not the same original example with only its
switch budget changed.

## Issues reported for correction

1. The benchmark's independent p,q,i endpoint scan has O(n^3 N) operations,
   not the stated O(n^2 N). This affects the verifier description, not the
   optimizer's O(nN) guarantee or the three-mode numerical result.
2. The original example differs in selected columns and grid as described above.
3. Boundary validation originally converts the input to a set before checking
   element types. Inputs [1, True], [1, 1.0], and [1, Fraction(1)] therefore collapse
   to {1} and evade the integer-only check. Validation should inspect the input
   elements before deduplication. This has no effect on valid-input optimality.

All three issues were sent to the root agent; correction status is recorded
below when checked. There were no mathematical counterexamples in the audit.

**Correction verification:** the benchmark note and verifier comment now say
O(n^3 N); the benchmark description now identifies all three full-grid CSV
weight columns and distinguishes the example drivers. Boundary validation now
checks a list before constructing the set. Three independent regression checks
for the duplicate-type cases pass, bringing invalid-input checks to **13**.
All 3,776 one-switch/query comparisons still pass after these corrections.

## Review of the arbitrary-prefix completion and subset DP extensions

The new implementations `complete_with_one_block`, `optimal_block_assignment`,
and `optimal_few_switches` were also read independently. They implement correct
exact optimization for the models stated in their docstrings.

For a prefix ending at u, write E0 for its error, c_i for its service, and
r_i=m_i-c_i. Appending mode j gives exactly

    max(E0, max_{i != j} r_i, T-u-r_j).

An inactive mode's discrepancy increases from its value at u, whose absolute
value is bounded by E0, to r_i. Thus omitted negative residuals need no absolute
value: their negative discrepancy is already covered by E0. The active mode's
discrepancy decreases from its value at u to r_j-(T-u); its positive discrepancy
is already covered by E0. Replacing j by a larger residual in the eligible set
cannot increase the displayed expression. Excluding the previous mode when an
actual switch is required is valid; an empty prefix has no previous mode.

For prescribed k blocks, a schedule assigns each mode a subset of blocks,
possibly disconnected. Every mode's endpoint discrepancy depends only on its
own subset. The subsets must partition the block set, so a bottleneck subset
partition dynamic program is exact. Empty subsets correctly contribute the
mode's total mass. The implementation evaluates all k endpoints for each subset,
giving O(nk2^k) cost preparation. The submask recurrence uses O(n3^k) operations.
Its O(n2^k) traceback storage suffices to recover the labels, including repeats.

Enumerating all partitions into k=min(s+1,N) nonempty grid blocks covers every
schedule with at most s switches: fewer-switch schedules can be subdivided
without changing their labels. Every returned labeling also has at most k-1
actual switches. This proves the budget solver's reduction. The combinatorial
dependence on grid size remains a material limitation for large N and s.

The review script was extended with a separate reference enumeration of all
n^N interval schedules on 32 small rational instances. It passed:

- **194** prescribed partitions compared with all block labelings;
- **156** switch budgets compared with every admissible interval schedule;
- **2,097** arbitrary-prefix completions compared with every eligible suffix mode.

These include one mode, one interval, budgets larger than N, repeated labels,
negative residuals, an empty prefix, and a required switch with no eligible
mode. They do not substitute for the proofs above.

The completed extension text and its additional candidate-set lemma were then
read. The candidate-set exchange is valid: replacing a selected outside label
by an unused cheap label cannot increase the role cost, and an omitted top-total
label certifies that the newly omitted total is no larger than the old omitted
maximum. This requires fixed equality roles as stated.

Two further documentation points were sent to the author:

- One-switch working storage also contains O(N) boundary indices, so O(n+N)
  beyond the validated input is the direct implementation bound.
- Mode-specific dwell requirements do **not** inherently break the subset
  separation. For prescribed blocks, the maximal consecutive runs of the subset
  assigned to mode i determine all its activation durations. Declaring subsets
  violating i's dwell limits infeasible preserves the same recurrence. Per-mode
  activation counts, availability, or total service limits similarly belong to
  mode-local subset admissibility. General transition graphs do couple different
  mode labels and are a distinct restriction. The author is considering this
  practically useful extension; its implementation will need its own checks.

Coordinator closeout, 2026-09-07: the dwell extension was subsequently implemented
and passed the [separate fixed-budget review](review-cia-reopened-fixed-budget.md),
including 608 independent dwell comparisons. The paragraph above records the
earlier review stage; it does not designate an outstanding check.
