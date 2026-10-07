# Independent review of extension benchmark evidence

The final eleven-case run passes the independent artifact/reference audit and
all ten retained certificates pass a fresh bounded replay. No required correction
was found. The audit launches no optimization backend. Its machine-readable
result is [audit.json](audit.json). The earlier ten-case evidence remains in
`../archive/pre_lattice/`; its separate artifact/reference audit is preserved in
[pre_lattice_reference_audit.json](pre_lattice_reference_audit.json).

## Reference checks

The QP reference implementation in `corpus.py` enumerates every integer label
and every continuous stationary face. Skipping a singular free Hessian is sound:
choose a global optimizer in the relative interior of an optimal face of minimum
dimension. On this face the gradient vanishes and the Hessian is positive
semidefinite. A nonzero null direction could be followed at constant objective
until a boundary is reached, contradicting the minimum choice. Hence some global
optimizer is either a vertex or a stationary point with nonsingular free Hessian.

`check_artifacts.py` independently recomputes the four QP references by a
different, smaller enumeration. All integer coordinates in these inputs and the
other designated residual coordinates are coordinatewise concave, so an optimum
exists at their endpoints. Once these endpoints are fixed, at most two continuous
coordinates remain, with a positive-definite Hessian. Explicit one- and
two-variable stationary equations on their faces suffice. This confirms:

| Input | Exact minimum | Feasible candidates in independent audit |
| --- | --- | --- |
| Fresh signed mixed QP, six variables | `−509/105` | 138 |
| Mixed two-cut example | `0` | 12 |
| Same example with cut cap | `0` | 12 |
| Unbalanced signed triangle | `−1/2` | 8 |

The six-variable witness is `(2,1,1,0,1/84,5/28)`. This audit shares no reference
routine or optimization backend with the benchmark runner. The corpus's larger
full-face reference counts 591 feasible stationary candidates on that input.
The two-cut certificate uses two greedy bases with weights `1/2` and `1/2`; it
therefore exercises a nontrivial mixture. The signed triangle really is outside
the sign-flip class: multiplying the three required inequalities
`s_i s_j = −1` around the triangle would imply `1 = −1`.

The integer polynomial has `x∈{−3,…,6}`, `y∈{−2,…,7}`, and a continuous
coordinate fixed to `t=1/3`, with objective
`(t²/2)(−3−3y+3y²+7x−2xy−5x²)`. Instead of repeating the corpus's exhaustive
100-label enumeration, the independent audit uses concavity in `x` to reduce
to endpoints `−3` and `6`, then tests the nearest integers to the conditional
continuous minimizer `y=(3+2x)/6`. These four candidates prove the exact minimum
`−53/6`, attained at `(6,2,1/3)` and `(6,3,1/3)`. Substituting the fixed rational
coordinate makes every feasible value a multiple of `1/18`. The retained
certificate has raw lower bound `−71/8` and upper bound `−53/6`, a positive gap
of `1/24<1/18`, so it genuinely exercises the lattice stopping rule rather than
merely observing a preexisting zero gap. The fresh replay checks that rule.

For polynomial inputs, the audit independently expands the stated identities
and checks every coefficient and domain:

- `(x−1/3)^4` on `[0,1]` has minimum zero and no positive quadratic-growth
  constant. Its value divided by squared distance to the optimum tends to zero.
- `(x²−2)²+(y−x)²+(z−1)²` on `[1,2]²×{0,1,2}` has minimum zero at
  `(√2,√2,1)`. The capped input is exactly the same polynomial and domain.
- `(x²−1/2)²+y+xy²` on `[0,1]²` has minimum zero at `(1/√2,0)`.
- `(x−1/4)²+y−y²` on `[0,1]×[0,1/2]` has minimum zero at `(1/4,0)`;
  the `y` term is nonnegative throughout the given interval.
- `(x²−1/2)²` on `[-1,1]` has two irrational minimizers. The inconclusive
  bounded search is not counted as an exact-output certificate.

## Evidence and scope

The final audit checks all 25 frozen source/input/reference hashes, every
loaded repository-module hash, every saved result and checker record, compressed
certificate hashes, original objective/domain binding, feasible incumbent values,
reference enclosure, exact statuses, requested gaps, unchanged capped inputs,
status totals, timing arithmetic, and process resource records.

The final eleven configurations have **seven requested outputs** (three exact
values and four other certified outputs), **ten valid certificates**, two cap
statuses, one unsupported status, and one inconclusive search. These counts
measure different things. A valid bound certificate does
not turn a resource limit or unsupported backend into a solved instance. A
boundary patch is an exact implicit optimizer description; it is not a returned
rational optimizer or a numerical zero-gap assertion.

Worker source confirms sequential execution, one numerical thread, a two-second
cooperative solver budget, five-second subprocess wall limits, and a 512 MiB
address-space cap. Exact references are built before timed solver execution.
`solve_seconds` includes backend imports performed inside that phase; the
separate load/decomposition phase and full subprocess wall time remain
available. Checker time is measured separately. These single, small runs support
correctness diagnostics, not solver competitiveness, statistical speedups, or
scalability claims.

Targeted command actually run from the repository root, successfully:

```sh
python research-20261002-decomposition/completion/benchmarks/extensions/review/check_artifacts.py
```

It launched no optimizer. It first ran the independent artifact/reference
audit in one bounded worker, then replayed existing proofs sequentially in bounded
frozen checker workers. No project-wide tests or CI inspection were performed.
