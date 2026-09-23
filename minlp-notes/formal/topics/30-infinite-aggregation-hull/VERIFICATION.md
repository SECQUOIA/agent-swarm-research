# Topic 30 verification record

Date: 2026-09-22. All eight frozen claims are covered by ten new Lean
modules. The exact hull, closure, weak-system hull, actual matrix lifts,
and all-good intersection identities hold for every `r≥2`.

The command run from the repository root was:

```sh
python3 formal/topics/30-infinite-aggregation-hull/verification/run_checks.py
```

It passed all of the following targeted checks:

- `lake build --wfail` on the ten explicit targets in
  [modules.json](verification/modules.json), without warnings.
- `lake env lean topics/30-infinite-aggregation-hull/verification/AuditAggregation.lean`:
  all **93 owned declarations** have transitive axiom dependencies limited
  to `propext`, `Classical.choice`, and `Quot.sound`.
- `lake env leanchecker MODULE` separately for each of the ten modules:
  all exited zero. Empty replay logs record successful silent checks.
- Canonical root imports and before/after source fingerprints: passed.

The [manifest](verification/manifest.json), [build log](verification/build.log),
[axiom log](verification/axioms.log), and `kernel-*.log` files preserve
the results. The pinned toolchain is Lean 4.33.1, with one Lean worker.
The axiom audit includes imported dependencies transitively; the targeted
module replays do not rebuild all dependencies. Replay uses the pinned
Lean kernel rather than an independently implemented checker.

The [semantic reviews](REVIEW.md) found no unresolved issue. In particular,
the direct two-point proof covers `r=2`, and the final statements do not
assume the BDS hull theorem or the hull equality they are proving.
No project-wide verification or CI inspection was run.

## Related paper

From `paper-quadratic-aggregation/`, this command passed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-exact-hull.tex
```

The two-page supplement has no final LaTeX warnings, overfull or underfull
boxes, undefined references, or duplicate labels. An initial overfull
paragraph was corrected. `pdftotext -layout`, `pdfinfo`, and targeted
extracted-text checks passed. The records are [build output](verification/paper-build.log),
[final log](verification/paper-final.log), [text](verification/paper-text.txt),
[PDF information](verification/paper-info.txt), and
[source/PDF hashes](verification/paper-sources.json).

The source note now gives the stronger direct two-point proof for all
`r≥2`, identifies the completed formal scope, and removes its stale blanket
statement that no Lean formalization exists. The separate supplement does
not certify the concurrently developed main manuscript or its other claims.

The supplement was rebuilt successfully after a concurrent update to the
shared LaTeX macros. Its final recorded inputs and PDF match the current
files. Topic-30 documentation checks covered 384 local links and all 49
then-completed source fingerprints across topics 27–30; targeted
`git diff --check` also passed.
