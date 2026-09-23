# Exact Feasibility of Resistive and AC Power Networks

The manuscript proves existential-real completeness for exact resistive
power-flow feasibility under simultaneous connectedness, planarity,
bipartiteness, maximum degree three, unit conductance, and any prescribed
fixed lower bound on girth. It covers AC angle semantics and hardness
transfers; rational universality precisely for compact basic closed sets defined over the
rationals; arbitrary compact semialgebraic topology and algebraic voltages;
and quantitative residual and reactive-stability bounds.

The input allows independent positive voltage intervals and signed power
injection intervals, including singleton intervals. The AC results state
whether angles are consistent real bus angles, principal line angles, or
reference-fixed bus-angle boxes. Approximate certificate results use an
explicit gap promise and do not classify exact feasibility as NP.

Build from this directory with a LaTeX distribution providing `latexmk`,
BibTeX, TikZ, and the packages listed in `main.tex`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The PDF is [build/main.pdf](build/main.pdf); [main.tex](main.tex) is the entry
point. Mathematical sections are in `sections/`, the arithmetic proof and
verification supplement are in `appendices/`, and citations are in
[references.bib](references.bib). No author identity or journal template is
assumed.

Run the four deterministic exact-arithmetic suites with Python 3.10 or newer:

```bash
python3 checks/check_resistive_exact.py
python3 checks/check_ac_exact.py
python3 checks/check_developments_exact.py
python3 checks/check_arithmetic_exact.py
```

All checkers use only Python's standard library. They run without Gurobi or
another optimization solver. Their coverage is described in the manuscript's
verification appendix: 12,751 resistive profiles; 2,112 scaled short arcs and
177,168 winding cycles; generalized gadgets, subdivision and quantitative
checks; and 1,681 bounded arithmetic gate profiles plus full circuit and
simplex examples. These are finite checks supporting the proofs, not formal
certificates of quantified theorems.

The earlier solver experiments in the repository were not rerun. Their eight
source examples are resolved analytically in the verification appendix;
floating point solver bounds are not used as exact evidence. The earlier
exact winding checker was rerun, with its output retained in
[verification/root/legacy-winding.log](verification/root/legacy-winding.log).

The [source coverage map](process/coverage.md) accounts for relevant repository
notes, code, literature, and identical copies in the other worktree.
[PROCESS.md](PROCESS.md) records the required staged author/reviewer workflow;
`process/` contains author reports, independent reviews, root assessments,
and correction reports. Immutable reviewed-source snapshots are in `process/snapshots/`; execution
logs are in `verification/`. Internal reviews are not external peer review
or proof-assistant certification. Generated build files and diagnostic images
are excluded from version control.
