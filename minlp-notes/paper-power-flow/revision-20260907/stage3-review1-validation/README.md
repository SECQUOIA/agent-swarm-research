# Exact Feasibility of Resistive and AC Power Networks

This paper proves existential-real completeness for exact resistive
power-flow feasibility under simultaneous connectedness, planarity,
bipartiteness, maximum degree three, unit conductance, and any prescribed
fixed lower bound on girth. Its solution-preserving construction yields
rational and topological universality. Separate bounded-degree, fixed-data
networks have doubly exponentially small infeasibility residuals. The paper
also gives AC hardness transfers, a quadratic encoding of real angle lifts,
and quantitative certification and reactive-stability bounds.

The model allows independent positive voltage intervals and signed injection
intervals, including simultaneous singletons. AC results distinguish real
bus angles, principal line angles, and reference-fixed bus-angle boxes.
Rational equivalence is restricted to compact basic closed sets over the
rationals. Approximate certificates require the specified gap promise.

## Build the manuscript

Run these commands from this directory, using a LaTeX distribution with
`latexmk`, BibTeX, TikZ, and the packages listed in `main.tex`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The result is `build/main.pdf`. The complete source consists of `main.tex`,
`macros.tex`, `references.bib`, `sections/`, and `appendices/`; no external
repository files or images are needed. Author metadata is left blank.

## Run the exact checks

Python 3.10 or newer is sufficient. All four deterministic programs use
only the Python standard library and require no optimization solver or
external data. Run from this directory:

```bash
python3 checks/check_resistive_exact.py
python3 checks/check_ac_exact.py
python3 checks/check_developments_exact.py
python3 checks/check_arithmetic_exact.py
```

Run Python without `-O` or `-OO` and with `PYTHONOPTIMIZE` unset, because
the checkers use assertions. Under these settings, each program reports its
results and exits successfully only if all checks pass.
`check_developments_exact.py` imports the resistive checker from the
same `checks/` directory; keep the four files together.

The verification appendix explains the coverage:

- Resistive: 12,751 voltage profiles, including 606 source solutions, repeated
  variable names, graph/data restrictions, and residual identities.
- AC: 2,112 short-arc pairs, 14,784 cosine tests, 177,168 winding cycles,
  648 complex-power sign checks, and 4,166 graph/crossing cases comparing
  vertex shifts with an independent enumeration of all simple cycles.
- Structural and quantitative: generalized gadgets, connectors, harmonic
  subdivisions, 360 perturbed profiles, infeasible recurrences through
  index 10, and 100 spectral/Lipschitz samples.
- Arithmetic: 1,681 multiplication/reciprocal profiles, a complete
  332-variable disk circuit, nine constant-chain configurations, and
  35 simplex support profiles.

These finite checks support the mathematical proofs; they do not establish
quantified theorems by sampling. The appendix also resolves eight small
feasible or infeasible instances analytically.

## Submission files

`submission.zip` contains only the manuscript sources, bibliography, four
checkers, and this README. It can be extracted and built independently.
The compiled PDF is supplied separately as `build/main.pdf`.
