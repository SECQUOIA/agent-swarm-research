# Topic 21 verification

Date: 2026-09-21. **PASS.** The final source-frozen run completed successfully.
All 33 frozen claims are proved and independently reviewed within the
[stated scope](CLAIMS.md).

| Targeted check | Result |
|---|---|
| Explicit topic build, warnings treated as errors | Passed: 124 modules |
| All-owned-declaration axiom audit | Passed: 3,483 declarations |
| Preserved independent review clients | Passed: 20 clients |
| Individual kernel replay | Passed: all 124 modules |
| Source and verification-helper hashes unchanged during checks | Passed |
| Topic module discovery and canonical import coverage | Passed |

Run from `formal/`:

```sh
python3 topics/21-dag-spectral/verification/run_checks.py
```

The [runner](verification/run_checks.py) sets the pinned Elan toolchain on
`PATH` and `LEAN_NUM_THREADS=1`. It reads the exact
[124-module list](verification/modules.json), checks that it matches every
file in `Formal/DAGSpectral`, and checks each module's presence in the
canonical `Formal.lean` imports. It builds only those explicit targets with
`lake build --wfail`; it does not build the project root.

The [declaration audit](verification/AuditDAGSpectral.lean) examines every
declaration owned by those modules, including private and generated helpers.
It permits only `propext`, `Classical.choice`, and `Quot.sound`. The current
[audit log](verification/axioms.log) records 3,483 declarations. Production
proofs use no admitted declarations, custom axioms, or `native_decide`.

The runner also executes 20 preserved independent review clients with
warnings treated as errors, then calls `lake env leanchecker` separately for
each topic module. The clients check signed rounding, singular factors and
ranges, no-path and empty-path cases, exact eigenvalue ties, pseudoinverses,
weighted infinite costs, actual cache accesses, and the original-input cover.
Some review clients use native decision tests as supplementary runtime
assertions; those declarations are not imported by production modules or
used to prove any frozen claim.

The run records hashes of every topic source, the verification clients,
audit and runner, the toolchain and Lake manifest, and rejects changes during
verification. The [final manifest](verification/manifest.json) records the
completion time, exact module/client lists, toolchain and hashes.
Detailed review scopes and commands are linked from [REVIEW.md](REVIEW.md).

The independent whole-runner review passed all 14 execution assertions using
the default stack. Its positive-rank example initially exposed an expensive
cost-observer calculation: evaluating a loose width budget constructed a
list with that many entries. `primitiveBitCost_closed` proves equality to a
closed formula and supplies a verified compiler rewrite. Independent checks
compared 84 small cases against the original finite loops and evaluated a
width of `2^100`. The mathematical charge and its bound are unchanged.

The source theorem's scope is explicit: the costed core takes a graph with
verified topological indices, original rational PSD atoms and prior, and
rational accuracy. The separate raw-graph interface computes an ordering
and preserves the edge lists; its scan counts do not assert a full bit-cost
bound for Lean's topological-sort implementation. The cost model is
schoolbook arithmetic with explicit storage, access, dictionary and path-copy
charges, not a wall-clock bound for Lean's runtime. Finite-memory transfer
assumes the separately supplied uniform PSD sandwich. The stochastic graph
producer and represented-matroid topic 22 are excluded.

The two source notes, paper README, manuscript scope statement and spectral
section were updated to match these results. From `paper-correlated-measurements/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

This passed and regenerated the [66-page manuscript](../../../paper-correlated-measurements/build/main.pdf)
and its [build log](../../../paper-correlated-measurements/build/main.log), with
no LaTeX warnings, undefined references or overfull boxes. Pages 1 and 27,
containing the updated scope statements, were rendered and inspected.
[Paper build hashes](verification/paper-build.json) record the sources and PDF.
Historical paper snapshots and computational experiments were not changed.

Local Markdown links in the topic package and changed source documents were
checked. `git diff --check` passed. No project-wide verification was run, and
CI status and logs were not inspected.
