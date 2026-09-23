# Formal verification scope

The portable project is [supplement/lean](supplement/lean/README.md).
It contains 64 paper-owned Lean modules, 909 audited owned declarations,
five transitive local support modules, and pinned Lean 4.33.1/Mathlib
build metadata. No surrounding repository is required.

| Audit package | Modules | Declarations | Scope |
|---|---:|---:|---|
| 27 | 11 | 178 | Certificate theorem under AHC/HHC and its separation/cone foundations |
| 28 | 10 | 158 | Closed-system properness, Shor whole-space equivalences, signed-coordinate SDP tests, Dines and two boundary examples |
| 29 | 18 | 248 | Actual HHC for the two-ball example, exact good cone, uncountable strict rays, no finite weak good description |
| 30 | 10 | 93 | Exact strict/closed hulls, two-point decomposition for all r≥2, actual PD/PSD lifts, weak-system hull and all-good intersections |
| 31 | 15 | 232 | Euclidean approximation bounds/rate, explicit tolerance families and rational coefficient meshes |

Each package previously passed a warning-free explicit-module build,
transitive owned-declaration axiom audit and individual module kernel replay.
The core package was independently rerun during preparation of the paper.
The portable runner writes its own fresh results to
`supplement/lean/verification/`; those results are distinct from the
original package records. An absent output manifest is not a successful run.
All runs are topic-specific local checks, not project-wide or CI checks.

From the paper directory, build the detailed account with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build formal-supplement.tex
```

The individual `formal-verification.tex`, `formal-consequences.tex`,
`formal-infinite-aggregation.tex`, `formal-exact-hull.tex`, and
`formal-aggregation-accuracy.tex` wrappers remain independently buildable.
The main paper instead gives a concise combined scope statement.

Two differences from the paper are deliberate. Package 28 verifies
n(n+1)+2n signed-coordinate objectives, while the paper improves this to
2n+1 trace/vector objectives. Package 31 verifies lower constant 1/2000
(and the weaker original logarithmic constant), while the paper proves
sqrt(2)/2000. It verifies the same upper constant and inverse-square rate.
The approximation model explicitly uses the Euclidean norm in 2r coordinates.

The general sharp Gram theorem, arbitrary-quadratic obstruction, countable
dense weak sufficiency, stronger lower constant, strict PDLC four-bound,
many-row appendix, local-certificate application, single-objective duality,
and literature novelty claims are not verified by these packages. The
spectral alternative to the certificate proof is not fully formalized.
No numerical optimization solver is certified.

The only permitted transitive axioms are `propext`, `Classical.choice`,
and `Quot.sound`. Kernel replay uses Lean's own kernel and its imported
dependencies, not another proof assistant or a source replay of all of
Mathlib. The five extra local support modules are supplied so the package
is complete; they are imported but not individually replayed by the runner.
