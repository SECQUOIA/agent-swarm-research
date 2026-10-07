# Certified support cuts for shared nonlinear expressions and quadratic blocks

Read [the integrated report](main.pdf) or its [LaTeX source](main.tex).
[COVERAGE.md](COVERAGE.md) maps each main claim to its proof, implementation,
saved evidence, and limitations. The overall scope is fixed by
[PROGRAM.md](../PROGRAM.md).

The report joins final-row numerical certification, checked activation
screening, exact quadratic support over row-constrained pairs and stars,
overlap limits, automatic SCIP integration, and comparative evidence. Its
mathematical components have substantial prior literature, credited in the
[source audit](../literature/README.md). The practical contribution is the
supported implementation and its explicit proof and model-binding contract.

The computational result is adverse for default activation: of 24 selected
held-out models, 20 pass the common importer; native baseline and the
reformulation control each solve 19, while both cut modes solve 18. Automatic
selection reduces separation work, but does not recover the lost solve. The
synthetic solved-count gain is already obtained without new cuts by the
reformulation control. See the [frozen results](../experiments/campaign-v1/results.md)
and [all recorded-cut replay](../experiments/campaign-v1/replay.json): 1,082
recorded rows pass, while eight worker errors have no model/cut log and are
excluded from successful replay coverage. This supports an optional research
component, not default use in a production solver.

The central limits are precise:

- A cut certificate proves the cut on its supplied domain; it does not certify
  SCIP's complete solve or final dual bound.
- Exact support for a chosen direction does not make the bounded numerical
  direction search complete.
- Exact pair hulls need not compose into the full simultaneous hull. The report
  gives a sharp rational obstruction and an implemented constrained-star remedy.
- Automatic activation and timing improvements require empirical assessment.
  Sampling microbenchmarks do not establish faster complete solves.
- Replay shares arithmetic routines with generation. Internal research-agent
  review is not an independently implemented checker, formal verification, or
  journal peer review.

Build only this report from the repository root:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  research-20261002-convexification/document/main.tex
```

The build uses the bibliography in `../literature/references.bib`. It needs no
project-wide verification and makes no claim about CI. Build output and the
local document checks are recorded in [VERIFICATION.md](VERIFICATION.md).
