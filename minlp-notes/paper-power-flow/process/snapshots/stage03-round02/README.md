# Power-flow paper

The manuscript is being developed in the stages recorded in [PROCESS.md](PROCESS.md).
The current draft covers resistive and AC completeness, exact real-angle
winding constraints, bus-angle boxes, and positive principal-angle windows.
It also develops simultaneous planarity, connectedness, bipartiteness, unit
conductance and prescribed girth restrictions; rational universality precisely
for compact basic closed sets, topological universality for arbitrary compact
semialgebraic sets, and algebraic voltages; quantitative residual transfer and
reactive stability; approximate certificates for a gap promise; and matching
doubly exponential residual scales. Literature integration and the full-paper
review remain in the subsequent stages.

Build from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 checks/check_resistive_exact.py
python3 checks/check_ac_exact.py
python3 checks/check_developments_exact.py
python3 checks/check_arithmetic_exact.py
```

The PDF is `build/main.pdf`. All exact checkers use only Python's standard
library and do not import or run Gurobi. Numerical solver experiments in the
repository are separate evidence, not proofs. Stage reports and source coverage
are in `process/`.
