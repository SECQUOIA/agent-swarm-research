# Independent review of constrained-star support

I read the completed proof in `theory/README.md`, the full
`theory/quadratic_star.py` implementation, its polygon projection dependency,
and the existing star tests. I found no mathematical or implementation
correctness blocker. This review concerns the exact continuous support oracle
and the fixed-direction merge diagnostic; it does not establish publication
priority, completeness of direction search, or a solver speedup.

The additional diagnostic
[`check_star_pieces.py`](check_star_pieces.py) passed **88 cases**, including
one empty domain. It checked **786 entire center intervals** and **7,063 exact
comparisons** against feasible alternative leaf rules. Three deliberate
certificate mutations were rejected. The results and reviewed source hashes
are recorded in [`star-review-results.json`](star-review-results.json).

**Feasible projection.** Arbitrary rational center–leaf rows are handled
correctly. Dividing a row with a negative leaf coefficient gives a lower
affine bound; a positive coefficient gives an upper affine bound. Center-only
rows restrict the center directly, and an inconsistent constant row makes
the domain empty. For each leaf, the projection of its bounded polygon is a
closed interval, including possible singletons. Intersecting these intervals
with the common center interval is sufficient: once a center is chosen, all
leaves can be selected independently. Further projection iterations are
unnecessary under the stated row structure.

The review diagnostic checks the same conclusion using a different method.
It eliminates each scalar leaf by requiring every lower affine bound to be
at most every upper affine bound, then intersects the resulting scalar linear
inequalities. It calls no polygon projection routine. Its exact projected
interval matched every returned center interval, and its empty projection
matched the empty certificate.

**Conditional minimization and switches.** Positive leaf curvature requires
the unconstrained affine stationary rule clipped between the active bounds.
Zero or negative curvature requires an endpoint. The difference of endpoint
values factors into the nonnegative interval width times an affine expression
on an envelope regime. Thus all required switches are rational; solving a
general quadratic for endpoint ties is unnecessary. Identically tied
endpoints permit either choice. A zero-width interval and fixed variables
remain valid, including a fixed center. At a switch, both neighboring rules
are feasible and optimal by continuity, so minimizing their closed pieces
does not introduce invalid endpoint candidates.

To verify these statements against the actual output without reproducing the
producer's switch construction, the diagnostic checks each proposed affine
leaf rule throughout its entire reported interval. Affine row feasibility is
checked exactly at the interval bounds. For every original lower or upper
bound line, and for the unconstrained stationary line when curvature is
positive, it computes the center interval where that alternative is feasible.
This interval is obtained by substituting the alternative into all original
pair rows. On that interval it minimizes the quadratic difference between the
alternative's objective and the reported rule's objective. Every difference
is nonnegative.

At every center value a scalar quadratic has an optimal feasible endpoint or,
when convex, a feasible stationary point. Therefore these whole-interval
comparisons prove the reported rule conditionally optimal throughout each
checked piece, including ties and changing active bounds. This diagnostic is
stronger than testing a finite set of centers within the pieces. It also
checks partition coverage, aggregate polynomial identities, each piece's exact
minimum, the final minimum, and the feasibility and attained objective of
every reported minimizer. It uses its own arithmetic routines rather than the
producer's envelope, projection, or minimization helpers. It is a review
diagnostic, not a formally verified checker.

The corpus includes explicit crossing envelopes, positive/zero/negative leaf
curvatures, exact endpoint ties, center–leaf equalities, an empty projection,
a singleton projection, fixed leaves, a center without leaves, and 80
deterministically generated stars with arbitrary center indices. The separate
[`star-audit.md`](../theory/star-audit.md) compares global minima with full-space
face-stationarity enumeration; that independently developed check complements
this interval-level check.

**Complexity.** Let `s_i` count a leaf's original bound lines and let
`S=sum_i s_i`. The code examines at most quadratically many line intersections
per leaf, and uses a linear scan to identify active bounds on each resulting
interval. It adds only a constant number of conditional switches per such
interval. The merged partition has `O(sum_i s_i²)` pieces; direct evaluation
of all leaf rules on each piece costs `O(S)`. The stated conservative cubic
rational-operation bound therefore covers the support computation and the
polygon projections. Center-only rows do not break this bound.

The box specialization has only constantly many conditional switches per leaf
and `O(k²)` rational arithmetic work in its support phase. An end-to-end
operation count must also account for the explicit input representation and
serialization. Dense exponent tuples, zero monomial entries, and tuple sorting
need not take only quadratic elementary operations. This qualification was
sent to the author; the theorem's rational-arithmetic convention should be
retained when quoting the box bound.

Polynomial bit complexity is also justified here rather than inferred solely
from the arithmetic count. Bound lines and switches use a bounded number of
arithmetic operations on input coefficients. Aggregate quadratics sum only
polynomially many such terms; stationary points solve a single affine
equation. Rational numerators and denominators therefore have polynomial bit
length in the explicit input length. There is no repeated nonlinear
composition or recursively increasing degree across pieces.

**Merge gain and binding.** The common-minimizer equivalence is correct when
the assembled feasible set consists exactly of the simultaneous pair
memberships `(y,x_i) in P_i`. All center restrictions must be included there.
This assumption is now explicit in the note following review feedback. If an
additional center restriction were silently imposed only after computing the
individual pair minima, the stated equivalence could fail.

Under the explicit assumption, every pair objective is at least its own
minimum. Their sum attains the sum of minima exactly when their full
minimizing sets admit a common center. Otherwise compactness yields a strict
gap. The complete minimizing sets matter: their projected sets need not be
intervals, and comparing one selected minimizer from each pair would not
establish the condition. The reported merge gap is computed by exact support,
so the implementation does not make that erroneous shortcut. The gap is the
largest valid constant improvement for that fixed sum of normals, not a
prediction about other directions or runtime.

Replay reconstructs the canonical result against trusted mathematical input.
It shares the producer's algorithm; the note states this limit. The author
also clarified that binding is to normalized rational input, including the
omission of zero objective terms, rather than lexical identity of a model
file. External model-variable identities and the actual coefficients sent to
the solver remain the integration's responsibility.

The targeted command run from the repository root was:

```sh
python research-20261002-convexification/reviews/check_star_pieces.py > research-20261002-convexification/reviews/star-review-results.json
```

It completed successfully. The result records SHA-256 hashes of the reviewed
theory note, star implementation, and polygon implementation. No
project-wide verification or CI inspection was performed for this review.
