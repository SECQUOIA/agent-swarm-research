# Independent integration review

The stable implementation passes the focused cross-caller checks in
[check_integration.py](check_integration.py). These checks exercise the interfaces
between the completed modules. They supplement the larger component reviews;
they are not a project-wide test run.

The recorded command is:

```sh
python3 -B research-20261002-decomposition/completion/reviews/integration/check_integration.py
```

The run passed:

- 12 exact-output runs, including zero-time results and independently computed
  exact optima for six small original models.
- 27 original-model recourse runs through grid, automatic, minimum-cut,
  submodular, and convex backends. The models include rational fixed
  coordinates, integer coordinates, nonunit bounds, a continuum of optima,
  and complete elimination to a constant problem.
- Three constrained runs using an equality fiber, nonconsecutive native
  labels, an empty separator, union filtering, and incomplete versus exact
  output.
- 15 membership checks against an endpoint certificate with free integer
  labels.
- 50 rejected model, point, and checker-budget mutations.

Every solver result crosses a JSON serialization roundtrip before replay.
The small reference optimizer independently enumerates original integer
labels and continuous faces, then solves the nonsingular face stationarity
systems with separate rational elimination. It does not use the shared LP,
QP, or finite-tree implementations. Exact answers match its values; all
incomplete intervals enclose them.

For the main pipeline cases, replay runs with the LP, convex-QP, and grid
optimization entry points replaced by functions that raise immediately.
Replay succeeds without invoking them. Outer certificates bind their
original model, reduced mathematical model, exact-output request, lifted
point, and objective. Standalone grid and TU certificates certify their
explicitly embedded instances; their verification APIs do not take an
external expected model. An application using those APIs must compare the
embedded input with its intended instance. The composed recourse verifier
performs that comparison for the grid certificates it consumes.

Two integration issues were found and fixed by the recourse owner:

1. The outer checker forwarded its table-state limit only to grid replay.
   It now also forwards the limit to convex-recourse replay. A deliberately
   insufficient outer limit is rejected by the retained regression.
2. An original-coordinate `warm_start` was forwarded unchanged after
   affine or fixed-coordinate elimination. The wrapper now validates the
   original point and projects it to the retained coordinates before
   calling the grid or exact-output solver. Both modes pass the regression.
   Other specialized backends currently ignore an optional warm start.

A temporary missing scalar-piece serializer was observed while its owner
was still editing the helper. The completed helper resolves that failure.
The convex backend's runtime dependency on
`completion/theory/piecewise-recourse/scalar_piecewise.py` was also reported
to the benchmark owner, who confirmed it is included in source snapshots.

[results.json](results.json) records the counts and source hashes used for
this run. The [additional workflow review](new-workflows-review.md) records
16 further JSON certificate roundtrips and 31 rejected model or proof
mutations. Those checks connect the polynomial, boundary-output, convex,
submodular, and original-index pipeline interfaces. They include a changing
three-piece stiff convex response and an irrational optimizer represented
by an exact implicit patch, with the optimization entry points disabled
during replay. The [saved results](new-workflows-results.json) include the
scalar helper's source hash.

The review found no remaining bound-soundness or original-model composition
defect in these exercised workflows. This is bounded implementation evidence,
not a proof of all possible inputs or a general performance result. The
documentation correctly separates abstract polynomial-time oracle arguments
from the actual capped simplex, face-search, and cutting-plane algorithms.
It does not claim that the remaining general width/conditioning and
optimal-set efficiency questions have been solved.

The second review pass read the continuation `README.md`, `PROGRAM.md`,
`completion/README.md`, and `solver/README.md`. It checked all 60 local links
in those four files; none was missing. It recommended making the unique
optimizer assumption explicit next to the core width-and-conditioning bound,
and linking the current integration review separately from the first
report's historical review. It found no stale claim that the unrestricted
negative-curvature, width-FPT constraint, or arbitrary optimal-set questions
were complete. The first report's 74 benchmark runs are clearly labeled as
historical evidence, with new source snapshots kept separately.

No project-wide verification or CI inspection was performed.
