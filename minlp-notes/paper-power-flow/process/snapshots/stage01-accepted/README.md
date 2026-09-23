# Power-flow paper

The manuscript is being developed in the stages recorded in [PROCESS.md](PROCESS.md).
The current stage-1 draft covers exact resistive feasibility and its complete
bounded-degree reduction. Later stages add the AC model and the remaining
results before the full-paper review. The working title and abstract describe
only the results already written.

Build from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
python3 checks/check_resistive_exact.py
```

The PDF is `build/main.pdf`. The exact checker uses only Python's standard
library and does not import or run Gurobi. Numerical solver experiments in the
repository are separate evidence, not proofs. Stage reports and source coverage
are in `process/`.
