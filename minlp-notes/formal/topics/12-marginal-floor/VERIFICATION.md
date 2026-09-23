# Marginal-floor verification

Status: complete. All canonical checks passed on 2026-09-17.

The topic adds eleven proof modules to the canonical project. At this stage
the canonical root imports 171 proof modules. All new public and private
declarations are included in the project-wide transitive axiom audit.

| Check | Recorded result |
|---|---|
| Import coverage | PASS: all 171 proof modules |
| Existing generated certificate reproducibility | PASS: potential-flow example and cubic finite certificate |
| Warning-free integrated build | PASS |
| Transitive axiom audit | PASS: 15,240 project declarations |
| Kernel replay | PASS: all 171 proof modules and the root import |
| Independent semantic and claim review | PASS: all 32 obligations, including supporting facts |
| Dependency fingerprints | PASS: 38 proof sources and three pinned configuration files |
| Topic-local navigation | PASS: all local links resolve |
| Whitespace/error-marker source check | PASS |

The [run log](verification/run.log) records the actual full-project invocation.
[SHA256SUMS](verification/SHA256SUMS) records the dependency closure of all
eleven new modules and the pinned toolchain/dependency configuration. The
existing exact-family asymptotic cited as supporting mathematics in MF-24
also belongs to the checked canonical project; its earlier package retains
its own verification record.

From `formal/`, reproduce with:

```sh
bash scripts/verify.sh
sha256sum --check topics/12-marginal-floor/verification/SHA256SUMS
```

The project permits only `propext`, `Classical.choice`, and `Quot.sound`.
The audit checks module-owned declarations transitively, including private
helpers. Kernel replay uses the installed Lean kernel and rechecks project
declarations against the pinned imported dependency base; it is not an
independently implemented proof assistant or a fresh replay of all Mathlib.

The [coverage map](COVERAGE.md) and [independent review](REVIEW.md) establish
which mathematical statements these checks cover. Software experiments,
historical runtimes, novelty and publication priority are not formal claims.
The full verification command exited with status zero and the final kernel
replay PASS marker. At the user's request, work stops here; later topics remain
queued.
