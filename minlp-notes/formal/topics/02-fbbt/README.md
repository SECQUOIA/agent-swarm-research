This package verifies the doubly exponential primitive-FBBT iteration theorem in
[the result note](../../../results/fbbt-doubly-exponential-convergence.md) and
[the appendix](../../../paper-relaxation-limits/sections/appendix-fbbt.tex).

The input has exactly `4n + 4` variables and defining equations, using only
copies, addition, multiplication, and the constant `1/2`. Starting every
variable in `[0,1]`, every sequence of exact bidirectional primitive interval
hulls needs at least `2^(2^n - 1)` applications of `z = b_n + w` before the
lower bound on `z` can reach `1/2`. This finite-prefix bound does not require
fairness. Under every fair schedule, both endpoint vectors converge to the
unique feasible point, whose `z` coordinate is `1`.

Here “fair” means that every equation is selected again after every finite
time. There is no bound on the delay. Each primitive contracts the current
box using one equation's exact interval hull; symbolic substitution,
equation aggregation, and global acceleration are different algorithms.

The main declaration is `FBBT.doubly_exponential_fbbt` in
[`Results.lean`](../../Formal/FBBT/Results.lean). `PrimitiveRun.singleton_limit`
proves the complete limiting box is a singleton. `canonical_slow_run` gives
an explicit fair schedule and actual exact-hull run, in addition to the
universal theorem over all permitted runs.

Proofs are in [`Formal/FBBT`](../../Formal/FBBT). See [COVERAGE.md](COVERAGE.md)
for the claim map and `VERIFICATION.md` for the final check record.
