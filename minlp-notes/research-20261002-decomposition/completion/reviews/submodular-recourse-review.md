# Independent review of mixed submodular recourse

The reviewed implementation is mathematically sound within its stated class.
I found no incorrect bound, exactness claim, endpoint reduction, or certificate
acceptance in the source inspection and targeted checks described below.
This is a review of the implementation and its certificate contract, not a
claim that its worst-case running time is polynomial.

Files reviewed:

- `solver/submodular_recourse.py`
- `solver/verify_submodular_recourse.py`
- The relevant exact LP, convex box-QP, rational model, and interval-bound
  routines in `solver/rational_optimization.py` and
  `solver/certified_grid.py`.
- `conditional-messages/mixed-submodular-recourse.md`.

## Mathematical checks

The recognition test correctly removes fixed coordinates, requires
nonpositive diagonal entries on the endpoint block, and rejects integer
coordinates in the remaining convex block. Effective native-integer bounds
are rounded before this step by `BoxQP`. The rational PSD test permits a
singular convex block. Sign propagation imposes precisely the condition that
every active off-diagonal coefficient becomes nonpositive after coordinate
reversal; interactions with fixed coordinates need no sign test.

The query construction correctly substitutes endpoint and fixed variables,
forms the remaining linear term, and keeps the original objective convention
`x'Ax/2+b'x+c`. Endpoint membership is interpreted consistently under negative
signs. Query-cache keys use sorted original coordinate indices, while greedy
vectors use the supplied endpoint-block order. These two representations are
consistent even when that order is not sorted.

Partial minimization of the transformed submodular objective over its product
convex box yields a submodular endpoint-value function. For each permutation,
its exact prefix differences therefore form a valid base vector. A convex
combination `w` gives the certified lower bound
`g(empty)+sum(min(0,w_i))`. This remains a valid bound when a resource limit
interrupts optimization.

The master LP minimizes an epigraph of the stored greedy affine pieces on
the unit box. Its first inequality multipliers are nonnegative and sum to
one, giving exactly the base mixture used in the proof. Sorting the master
point in decreasing coordinate order separates all greedy pieces. A
violated permutation cannot already be stored. If separation finds no
violation, the Lovasz value is a convex combination of the queried prefix
values. The feasible incumbent and master lower bound must then coincide.
Thus sufficient resource caps produce exact termination after at most the
number of endpoint permutations. This is a factorial cut bound. The
convex-QP oracle also has an exponential active-face fallback; neither this
cutting-plane implementation nor its QP fallback establishes the polynomial
runtime of the distinct oracle-LP construction in the theory note.

## Certificate and resource checks

The checker reconstructs the embedded exact model and optionally binds it to
the expected model. It recomputes the independent-factor lower bound rather
than trusting the solver. Its additional proof uses its own rational PSD
elimination, box feasibility, and coordinate KKT signs for every conditional
query. Those conditions suffice even for a singular convex block. Fixed
coordinates correctly require no KKT sign restriction.

Each mixture term must be a complete permutation, every chain value must
exist in the checked query table, weights must be positive and sum to one,
and the claimed lower bound must equal the strongest bound supported by the
embedded proof. The checker's proof does not call LP, QP, cutting-plane, or
submodular minimization routines. Exactness is accepted only for zero gap;
an epsilon claim also checks the requested output mode and tolerance.

An interrupted greedy chain may improve the feasible incumbent without
finishing a new base. Its partial query table does not invalidate the previous
base-mixture bound. Zero query, face, cut, or pivot budgets and an immediate
time limit produce valid partial bound certificates. Time and external checks
are cooperative, rather than hard process interruption. Performance counters
are descriptive metadata and are deliberately outside the mathematical
certificate contract.

## Targeted checks actually run

Two temporary inline Python diagnostics were executed from the repository
root with `python3 -B - <<'PY'`. Both imported only the relevant solver files;
neither ran project-wide verification or inspected CI.

The first diagnostic used random seed `88213` and passed:

- 120 exact comparisons with an independent oracle that enumerates three
  concave endpoint coordinates and minimizes the remaining scalar convex
  quadratic at its clipped rational stationary point. Cases had arbitrary
  sign reversals, rational coefficients, varying boxes, one extra fixed
  coordinate, and randomly selected native-integer endpoint coordinates.
  Half supplied the endpoint order `(2,0,1)`. All results survived JSON
  serialization and independent replay. The largest observed cut count was
  four.
- The two-base fixture from equation (17) of the theory note. Its exact
  certificate used two mixture terms and proved value zero.
- Eight explicit resource exits: cut caps zero and one; query caps zero,
  one, and two; face cap zero; pivot cap zero; and time limit zero. All
  returned valid resource-limit certificates on that fixture.
- Seven injected `BudgetExceeded` interruptions after check calls 1, 2, 5,
  10, 20, 40, and 80. Every returned certificate replayed.
- Rejection of 16 corrupted proofs, covering incorrect bounds, Boolean or
  duplicate labels, nonoptimal conditional points, duplicate queries,
  negative weights, incomplete or repeated permutations, invalid sign
  assignments, invalid partitions, missing mixture evidence, nonrational
  data, malformed nested values, and a changed final point. An expected-model
  mismatch was also rejected.

The second diagnostic used seed `9137` and passed:

- 60 exact comparisons with a signed two-dimensional singular PSD convex
  block and two concave coordinates, one native integer. The independent
  oracle enumerated endpoint labels and convex-box edges, then minimized
  each remaining scalar quadratic exactly. This is complete for the chosen
  rank-one PSD block because its objective is affine along the nullspace,
  so some minimizer lies on a proper box face. All 60 serialized certificates
  replayed.
- Separate pure-convex, pure-concave, and all-fixed cases, each solved and
  replayed exactly.
- An unsupported integer convex-block example, correctly returned as
  unsupported with a valid coarse interval certificate.

No source changes were needed as a result of this review. The implementation
author was asked to update the old theory note's diagnostic-only status and
link the new implementation while preserving the runtime distinction above.
