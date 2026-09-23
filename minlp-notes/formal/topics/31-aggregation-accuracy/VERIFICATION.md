# Topic 31 verification record

Date: 2026-09-22. All ten frozen claims are covered by fifteen new Lean
modules. The package verifies actual Euclidean Hausdorff bounds, the
extended infimum, exact rational constructions and coefficient sizes,
the asymptotic rate, and constructive tolerance budgets.

From the repository root, this command passed:

```sh
python3 formal/topics/31-aggregation-accuracy/verification/run_checks.py
```

The runner performed only these targeted checks:

- `lake build --wfail` on the fifteen explicit targets in
  [modules.json](verification/modules.json): passed without warnings.
- `lake env lean topics/31-aggregation-accuracy/verification/AuditAggregation.lean`:
  passed for **232 owned declarations**, including private and generated
  declarations. Their transitive axiom dependencies are limited to
  `propext`, `Classical.choice`, and `Quot.sound`.
- `lake env leanchecker MODULE` for each of the fifteen modules:
  all exited zero. Empty replay logs indicate successful silent checks.
- Canonical root imports and before/after source fingerprints: passed.

See the [manifest](verification/manifest.json), [build log](verification/build.log),
[axiom log](verification/axioms.log), and `kernel-*.log` files. The pinned
toolchain is Lean 4.33.1, with one Lean worker. The axiom audit includes
dependencies transitively; replay does not rebuild every dependency.
Replay uses the pinned Lean kernel, not an independent implementation.
No project-wide verification or CI inspection was run.

The [independent reviews](REVIEW.md) found no unresolved issue. They checked
the genuine Euclidean transport, unbounded-error convention, arbitrary
good multipliers in the lower bound, all-point upper repair, exact integer
coefficient encoding, and finiteness before conversion from extended
reals. Tolerance sufficiency constructs a family rather than assuming
attainment of the infimum.

## Related paper and source

From `paper-quadratic-aggregation/`, this command passed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-aggregation-accuracy.tex
```

The final two-page supplement has no LaTeX warnings, overfull or underfull
boxes, undefined references, or duplicate labels. `pdftotext -layout` and
`pdfinfo` passed, and targeted text checks confirmed the Euclidean,
pigeonhole, binary-size and infimum discussion. The records are
[build output](verification/paper-build.log), [final log](verification/paper-final.log),
[text](verification/paper-text.txt), [PDF information](verification/paper-info.txt),
and [source/PDF hashes](verification/paper-sources.json).

The source note describes the verified alternatives to its original
Taylor and logarithmic-covering proofs. The latter alternative yields
the stronger lower constant `1/2000` and proves the advertised constant
as a consequence. The standalone supplement defines its original system
and multiplier cone and distinguishes the uniform approximation theorem
from the unverified single-objective discussion. It does not certify the
concurrently developed main manuscript or a numerical solver.

Final [documentation checks](verification/documentation-checks.txt) passed
for 457 local links across 35 related documents, all 64 Lean source
fingerprints across topics 27–31, both new paper manifests, and targeted
whitespace and `git diff --check` scans. The 25 new modules contain no
`sorry`, `native_decide`, or custom axiom declarations; the stronger
transitive axiom audits are recorded above.
