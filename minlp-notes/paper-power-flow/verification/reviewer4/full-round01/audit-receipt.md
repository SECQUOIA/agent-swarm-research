# Final whole-manuscript audit receipt

Frozen input: `paper-power-flow/process/snapshots/full-round01`.
All 22 manifest hashes verified before review. The clean forced build used an
absolute output directory under this reviewer directory. The resulting PDF
has 28 pages; its final LaTeX log has no warning, undefined reference/citation,
overfull box, or underfull box. Pages 6, 13, 23, 25, and 27 were rendered and
visually inspected: the inversion table/diagram, crossover, appendix transition,
long arithmetic displays, and eight-example table are legible and unclipped.
The complete extracted PDF text was checked against the source structure.

All four frozen exact suites completed with exit code zero; their separate
logs contain the actual counts. The independent `check_gate_intervals.py`
adds a full-interval range certificate: delta=1/1024 keeps 64 propagated
auxiliary intervals strictly inside (1/2,2), with positive reciprocal
denominators, for all small inputs in [-delta,delta]. The nonnegativity
witness includes its allowed endpoint 1/2. These interval calculations do not
replace the separately audited algebraic identities and inverse recovery.

Primary-source checks were made against actual archived originals for the
ETR-INV definition/completeness (archived Art Gallery page 11), the polynomial
minimum bound (Jeronimo–Perrucci–Tsigaridas page 2), and the exact BM full-version
header (page 1). Extracted evidence is in the adjacent text files. The JPT
application has a compact connected epigraph, integer coefficients after
positive denominator clearing, degree bound 2, dimension n+1, and 4n+2
constraints; its nonzero-minimum bound specializes to the printed formula.

The primary [Ohmoto–Shiota version](https://arxiv.org/html/1505.03970v2),
Theorem 1.1 and Section 1.2, supplies semialgebraic triangulation and finite
complexes for compact sets; it does not supply rational equivalence. The
primary [Dobbins et al. article](https://pmc.ncbi.nlm.nih.gov/articles/PMC10244296/)
was reopened for the arithmetic-crossover attribution. The three equations
and their bounded unique extension were independently audited in the paper.

The eight relevant source files listed in the root's worktree inventory were
independently rehashed and compared to their actual counterparts in the other
worktree; all remain byte-identical (`worktree-check.json`). The coverage map
accounts for the original two power-flow theorems, complexity and algebraic
corollaries, angle corrections, quantitative/numerical evidence, and shared
arithmetic dependency. No additional in-scope result was found omitted.
