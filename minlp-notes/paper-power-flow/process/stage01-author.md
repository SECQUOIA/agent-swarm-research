# Stage 1 author report

Scope completed: foundations and the full resistive reduction. Files added are
`main.tex`, `macros.tex`, `references.bib`, `README.md`, sections 01–02,
`checks/check_resistive_exact.py`, and the coverage map. All edits are inside
`paper-power-flow/`. Root-owned stage status in `PROCESS.md` is unchanged.

## Mathematical development and checks

The exact input model specifies finite rational interval endpoints, strictly
positive voltage lower bounds, a simple undirected graph, signed net
injections, singleton intervals, and isolated buses. The physical distinction
from the linear AC DC approximation and the dissipation identity are explicit.
The decision class and conditional NP consequence use the Turing model and do
not infer nonmembership from irrationality alone.

The reduction was independently rederived before writing. Inversion uses
`v_I=x`, `v_W=2x-1+1/x`, and `y=v_W-2x+1`; the auxiliary range is
`[2 sqrt(2)-1,7/2]`. Every complement, addition, inversion, and auxiliary bus
has its complete original neighborhood stated in the proof, table, or figure.
The path allocation rule uses at most two extensions per request. All equations
request three distinct copies even when names repeat, giving at most `n+16m`
buses and `18m` lines, and no loops or parallel edges. Every named unused
variable retains one isolated bus, preserving its free source coordinate.

The uniform bound 85 is used in both the manuscript and its independent checker.
The bound 84 applies on the entire prescribed voltage box. This differs
deliberately from the legacy builder's degree-dependent bounds and makes the
fixed finite alphabet directly reproducible.

Lemma 2.2 and Proposition 2.3 explicitly preserve the solution set by a rational
homeomorphism, with inverse coordinate projection. This is the interface needed
for stage 3's self-contained universality/algebraic-degree consequences.

Primary dependency: the archived STOC/arXiv copy in
`literature/papers/abrahamsen2022-the-art-gallery-problem-is/`, p.11,
Definition 5 and Theorem 7. I read the fulltext passage and rendered/viewed
original PDF p.11 to verify the three displayed equation forms lost in text
extraction. The source uses repeated names and the interval `[1/2,2]` exactly
as required. `x=1` is replaced by `x*x=1` without changing the solution set.
The bibliography explicitly distinguishes the cited preprint numbering from
the 2022 journal version. Abrahamsen–Miltzow p.1–4 was read for complexity
conventions and the later rational-equivalence dependency. All original
power-flow reviews A/B/C and the closeout were consulted.

## Actual verification

`python3 checks/check_resistive_exact.py` completed successfully:

```
PASS: 12751 exact original-network profiles; 606 source solutions.
PASS: repeated/unused variables, empty instance, residual identities,
      distinct copies, simple graphs, degree <= 3, fixed data, size, and dissipation.
Finite exact checks support the proof; no numerical solver was used.
```

The checker uses only standard-library `Fraction` arithmetic. It constructs
the original graph independently of the legacy builder and computes every
original bus injection from all incident lines. It covers all 27 addition
name-identification patterns and all 9 inversion patterns on three names,
343 rational assignments per pattern, 101 reciprocal witnesses, a long fan-out
instance, 300 seeded mixed systems, and the empty instance. For arbitrary source
assignments it verifies exact residual identities at the original pinned buses,
so nonsolutions are checked too; it does not claim to solve arbitrary
infeasibility. Finite checks supplement the analytical proof.

The stage draft builds with `latexmk -pdf -interaction=nonstopmode
-halt-on-error -outdir=build main.tex`. The build and exact-check logs are
saved in `process/stage01-build.log` and `process/stage01-exact.log`.
The PDF has six pages; final log has no undefined citations/references or
overfull/underfull boxes. The bibliography and figure were also inspected in
the extracted PDF text. Full introduction and related literature are deliberately
reserved for stage 4, as root's stage plan specifies.

## Issues and interfaces reserved for later stages

No unresolved mathematical obligation was found in the stage-1 theorem.
Several later claims must be developed with care rather than transcribed:

1. Review C's optional extension of the test `e_i+e_j>0` from arcs at most
   `pi/2` to arcs less than `pi` uses an identity for equal magnitudes.
   It need not hold for unequal magnitudes. A full-range extension can instead
   normalize endpoints or introduce positive magnitude variables; the current
   stage makes no AC claim.
2. The novelty note's phrase that an LMI characterization is polynomially
   decidable "up to precision" is not an exact Turing-class proof. Describe
   the characterization with its assumptions; do not infer exact P.
3. Arbitrarily high degree for an individual coordinate requires the toolbox's
   affine coordinate projection, not rational field generation alone. Root
   has the exact rational-bijection interface now.
4. Root is independently developing edge-subdivision and planar-source leads
   for stage 3. None is included or assumed here.
5. Existing numerical AC spread upper bounds are tolerance-based checks, not
   proofs of exact angle equality. Stage 4 should separate them from the exact
   scripts and mathematical energy identity.

Ready for the required five independent stage-1 reviews. No reviewer was
spawned by the author.
