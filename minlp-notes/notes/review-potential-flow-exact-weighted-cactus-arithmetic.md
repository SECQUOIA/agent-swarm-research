# Independent arithmetic and input-contract review of the exact cactus solver

Date: 2026-09-06. Reviewer: `review_goal_bounds`, separate from the implementer.

**Outcome:** the exact quadratic arithmetic, comparisons, interval enclosure,
and supported input contracts pass this review after the schema corrections
recorded below. The solver accepts already constructed independent cycle and
bridge blocks. **It does not parse a graph, recognize a cactus, derive offsets
from nominations, or derive edge weights from a node-potential objective.**
Those are caller obligations; passing a graph-shaped object is now rejected.

Reviewed implementation:
[exact_weighted_cactus.py](../code/potential_flow_mpd/exact_weighted_cactus.py).
The independent checks are in
[check_exact_weighted_cactus_arithmetic.py](../code/potential_flow_mpd/check_exact_weighted_cactus_arithmetic.py).
The separate `review_weighted` audit covers candidate completeness, capacity
feasibility, and exact resistance recovery. This note does not duplicate that
full optimization audit.

## Exact comparison across radical representations

For nonnegative rational d, the helper determines the sign of `a+b*sqrt(d)`.
When the rational and radical terms have opposite signs, comparing their
squared magnitudes gives

\[
 \operatorname{sgn}(a+b\sqrt d)
 =\operatorname{sgn}(a)\operatorname{sgn}(a^2-b^2d).
\]

The implementation treats zero terms and equal-sign terms first, so squaring
does not discard necessary sign information.

For comparison across two stored radicands, write the difference as
`U+V`, where `U=a+b*sqrt(d)` and `V=c*sqrt(e)`. If their signs differ, then

\[
 \operatorname{sgn}(U+V)
 =\operatorname{sgn}(U)\operatorname{sgn}(U^2-V^2),
\]

and `U^2-V^2=(a^2+b^2*d-c^2*e)+2*a*b*sqrt(d)`. This is precisely the second
single-radical comparison in the code. In particular, exact equality is
recognized even when two equivalent radical values use different radicands.
The proof does not assume distinct squarefree radicands or an actual field
extension of degree four.

Arithmetic operations remain within one stored radicand, or add/multiply a
rational. This is enough for each local candidate and its physical witness.
Addition or multiplication of two nonrational values with unequal stored
radicands is deliberately unsupported, even if those radicands generate the
same mathematical field. The error text now states that restriction accurately.
Cross-radicand comparison is supported. The global value remains a sum of
separately represented terms, with an interval; the code does not provide
exact threshold comparisons for arbitrary sums of radicals.

The interval routine chooses dyadic square-root brackets with extra precision
depending on the magnitude of the radical coefficient. The extra precision
ensures that multiplication by that coefficient preserves the requested
absolute width. Negative coefficients reverse the interval endpoints, as
handled in the code. The global routine allocates enough additional bits to
make the sum of local interval widths at most `2^-bits`.

## Independent cancellation and magnitude controls

The arithmetic tests use Pell identities, rather than approximate decimal
comparisons. The recurrence for `(1+sqrt(2))^n=p_n+q_n*sqrt(2)` gives
`p_n^2-2*q_n^2=(-1)^n`. Thus the sign of `p_n-q_n*sqrt(2)` is known exactly,
including at n=1000 where the relevant integers have hundreds of digits and
the difference is extremely small.

The tests include:

- Nearzero Pell differences, and the same differences after adding a common
  rational offset `10^400` to the two compared values.
- Two-radical nearcancellation with a nonzero rational part: compare
  `a+sqrt(2)` to `sqrt(a^2+2+2*a*p_n/q_n)` for positive rational a. Squaring
  shows its sign is the negative of the known Pell sign.
- Exactly equal values represented using `sqrt(d)` and `sqrt(d*k^2)`, followed
  by a rational perturbation `10^-300` that must be distinguished from equality.
- Positive and negative radical coefficients of magnitude `10^300` and
  `10^-300`, at requested precision 0, 1, 40, and 1000 bits. Inclusion is
  independently checked by squaring transformed interval endpoints.
- Rejection of negative radicands, unsupported nonrational cross-radicand
  arithmetic, and Boolean precision arguments.

All 88 exact cancellation/equality/interval controls pass. These tests exercise
the arithmetic used to choose local winners without trusting an approximate
comparison or a tolerance-based equality test.

## Supplied blocks and an explicit graph reconstruction

The test fixture supplies two coherently oriented triangle blocks sharing one
vertex, plus a bridge. It independently reconstructs a six-node cactus graph
from those blocks. For each coherent cycle, writing `x_e=q+t_e` gives the fixed
nomination vector `b=A*t`, since the cycle circulation lies in the kernel of A.
For its edge weights w, `c=A*w` gives `c^T*pi=w^T*A^T*pi`.

For both minimization and maximization, the checker reconstructs physical
flows, resistances, and edge potential drops from the returned results. It
checks the original graph conservation equations, reconstructs node potentials,
checks every potential drop, and verifies that the node objective equals the
sum of returned block objective terms. Separate radical components are retained
when adding contributions from independent cycles.

The tests also reverse each coherent cycle's arcs and reverse/negate its offset
and weight arrays. The optimum is unchanged. Adding a common rational constant
of order `10^100` to the offsets only changes the circulation coordinate, while
adding a common constant of order `10^90` to the edge weights adds a multiple
of the zero cycle-drop sum. Both exact invariances pass. These are checks of
the documented supplied-block formulas, not an implementation or verification
of a general graph-to-block converter.

Capacity checks confirm that a bridge's exact fixed flow satisfies a matching
zero-width interval and fails an upper bound smaller by `1/100`. The separate
optimization review covers cycle capacity faces and irrational circulations.

## Schema issues found and corrected

The first implementation silently ignored unknown top-level and bridge keys.
In particular, unsupported graph input could be interpreted as an empty block
problem and return `optimal`, while an unknown capacity key could be ignored.
The author corrected this: top-level and block schemas now reject unknown or
missing fields, check container types, require explicit block lists, and reject
floating-point/Boolean rational data and Boolean precision.

A second review observation was that an early infeasibility return could skip
invalid scalar data in later blocks. The author now records infeasibility and
processes the remaining blocks before returning. The JSON command-line parser
also rejects duplicate keys instead of silently taking the last value.

The final checker rejects 24 malformed objects, including invalid later blocks
after an earlier infeasible block, unknown capacity aliases, graph-shaped input,
missing/invalid arrays, inconsistent dimensions, nonpositive resistance bounds,
and unsupported objective senses. Explicit empty cycle or bridge lists remain
a valid zero-objective problem. Valid command-line input and duplicate-key
rejection are checked in ordinary and optimized Python.

## Reproduction and limits

Both commands pass with no site packages:

```sh
python -S code/potential_flow_mpd/check_exact_weighted_cactus_arithmetic.py
python -S -O code/potential_flow_mpd/check_exact_weighted_cactus_arithmetic.py
```

No arithmetic or supported-schema issue remains from this audit. Exactness
does not mean this is an untrusted optimality-certificate checker: it is an exact
solver with internal physical-witness checks, whose optimization algorithm has
separate mathematical and computational review. It also does not make an
arbitrary collection of supplied blocks into a verified decomposition of a
user's original graph. Publication and usage descriptions should preserve
these distinctions.
