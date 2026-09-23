# Independent review: lift semantics and parity

Reviewed `Model.lean`, `Parity.lean`, `IntervalLower.lean`,
`LinearSystem.lean`, and `BinaryModel.lean` on 2026-09-20. The reviewer did not
implement these files. No correctness issue was found in these modules.

The convex model permits an arbitrary convex carrier in finite-dimensional
real space. Its integer coordinates range over all of `ℤ`, and its auxiliary
continuous dimension is arbitrary and finite. It assumes neither closedness
nor measurability of the carrier. The represented set existentially projects
actual feasible witnesses. Graph soundness includes membership in the original
input domain. Epigraph and hypograph containment quantify over every output in
the respective unbounded direction, without an extra truncation.

The parity code uses Euclidean remainder modulo two, whose nonnegativity is
proved for arbitrary signed integers. The midpoint witness is the integer
quotient of the sum by two. Its exact real embedding follows from equal
remainders; boundedness or nonnegativity of the indices is not assumed.
Raw contacts cover the domain by choosing a graph witness at each input.
Their closures lie in the compact domain. The proof closes the product of each
raw contact with itself inside a closed pair relation, so arbitrary points of
the closed contact retain the same midpoint error. This avoids assuming
measurability of raw contacts or that their lifted witnesses converge.

The square lower bound uses exactly `N+1` distinct grid inputs with `N=2^p`.
Pigeonhole supplies two distinct inputs of equal parity. Their separation is
at least `1/N`, including `p=0`; the quadratic midpoint identity gives
`eps >= 4^(-p)/4`. The square hypograph and concave-product epigraph versions
use the correct opposite error signs. The logarithmic equivalence assumes
`eps>0` and uses the natural ceiling, which implements the maximum with zero.
It includes equality thresholds and coarse accuracies. These modules establish
the lower bound and ceiling equivalence; attaining formulations and equality
of count minima require the construction modules.

`LinearSystem` stores a finite family of real affine inequalities, rather than
an arbitrary convex set relabeled as linear. Its preimage keeps the same
number of rows; append adds the exact row counts. Equalities can be represented
by opposite inequalities. `BinaryLinearLift` uses this actual finite system
and requires its continuous feasible set to imply the binary-coordinate bounds.
Its represented set additionally requires binary codes. The proved equality
with its associated unrestricted-integer lift establishes both directions:
every binary code has an integer witness, and every integer witness lies in
`[0,1]` and therefore is zero or one. Thus transferring lower bounds preserves
the actual number of discrete coordinates and does not weaken either model.

Targeted verification run from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.QuadraticPrecision.Model Formal.QuadraticPrecision.Parity Formal.QuadraticPrecision.IntervalLower Formal.QuadraticPrecision.LinearSystem Formal.QuadraticPrecision.BinaryModel
```

Result: passed. This was a targeted build of the listed modules and their
imported dependencies, not a project-wide verification or a CI check. Final
kernel replay and axiom auditing are recorded separately by the topic audit.

Coverage reviewed here: M1, M2, S1, the lower/ceiling portion of S3, and the
convex/binary model interfaces. M3's actual affine transformations, the
attaining upper constructions, higher-dimensional geometric bounds, and
asymptotic assembly were not part of this review.
