# Stage 3 author record

Date: 2026-09-07. Author agent: `paper_author`. Status: authored and locally
checked; awaiting five independent reviews.

## Scope

Added `sections/03-structured-oracles.tex`, integrated it into `main.tex`,
and updated README. Added primary max-flow, transportation, and polynomial
augmenting-path references. Accepted Sections 1–4 were not changed.

The section covers all substantive claims of
`results/network-simplex-cycle-theta-hull.md` and
`results/network-simplex-parallel-path-hull.md`. Their independent second
reviews were read and their qualifications carried into the manuscript.

The progression is state domains, exact theta supports, planar Minkowski
closure, original-coordinate hulls, linear-arithmetic separation and recovery,
the joint-state obstruction, arbitrary parallel paths, transportation
sufficiency, and a flow-based oracle. The proof never applies the planar
edge argument to higher-dimensional sums.

## Proof development and scrutiny

- Theta coordinates use `h=s+t` and a separate arc sign `sigma`, avoiding
  collision with global state count `d` and the unmodified path signs used
  later in the parallel-path formulation.
- The five theta nonemptiness checks follow from intersection of attainable
  sum intervals. All six supports are proved to be attained, via interval
  elimination.
- Planar closure treats two-dimensional sums, segments, and points separately.
  A segment summand must have one of the permitted directions because its
  relative interior lies on a tight defining boundary. Facet directions of
  a two-dimensional sum follow from its exposed-face decomposition.
- Piecewise-affine conditions are converted into genuinely global linear
  inequalities by active branch selection. The proof tracks nonrepetition of
  product indices, including same-type cancellation and distinct states.
- Compact recovery includes an explicit feasible point rule for reflected
  suffix intersections. Empty suffixes and zero-weight defaults are covered.
  Dense output is charged separately from the compact computation bound.
- Transportation sufficiency derives nonnegative row demands from complement
  subsets; they are not silently assumed. The proof minimizes each column's
  cut side independently and converts the resulting inequality exactly back
  into the subset formula. Zero total demand works without an exception.
- The max-flow oracle separates negative row demands before building a
  capacity network. A minimum cut's row set yields a violated original-space
  subset cut even before column-side minimization is imposed.
- Rational polynomial bit complexity is attributed to a polynomial-time flow
  method; arbitrary Ford–Fulkerson augmentations are not claimed polynomial.
- Both oracle scopes allow arbitrary orientations and parallel arcs, with
  loops handled as independent cycles. They do not cover arbitrary nested
  series–parallel blocks or side constraints added before convexification.

The worked multi-state theta example uses absolute path flows `X_s,X_t` so
they cannot be mistaken for signed circulation deviations. Separate one-label
decompositions are given explicitly; the joint cut is violated by exactly
`1/3`. This illustrates established joint disaggregation rather than claiming
a new convexification principle.

## Literature checks

- Ford–Fulkerson, *Maximal Flow Through a Network*: primary PDF opened from
  Yale, and Cambridge's primary article/PDF record verified DOI
  `10.4153/CJM-1956-045-5`, Canadian Journal of Mathematics 8, 399–404 (1956).
- Ford–Fulkerson, *Solving the Transportation Problem*: primary INFORMS record
  verified Management Science 3(1), 24–32 (1956), DOI
  `10.1287/mnsc.3.1.24`.
- Edmonds–Karp, *Theoretical Improvements in Algorithmic Efficiency for
  Network Flow Problems*: indexed primary author-hosted PDF supplies the
  algorithm statement and Journal of the ACM 19(2), 248–264 (1972) metadata.
  DOI `10.1145/321694.321699` was cross-checked. A later direct PDF open
  returned HTTP 502; it is not recorded as a successful new download.
- Kis–Horváth Section 5.7 remains explicitly cited as the direct Cayley-hull
  transportation-projection predecessor. Gritzmann–Sturmfels supplies the
  classical geometric background.

No claim of new generic polynomial hull separation is made, and the
coefficient assertions concern a rational row scaling, not primitive integer
normalization or EC&R multiplier magnitudes.

## Checks run

From the repository root, using the `minlp-notes` Python environment:

```sh
python code/audit-network-positive-decomposition.py
python code/common-factor-network-positive-verify.py
python code/common-factor-parallel-paths-verify.py
```

Results:

- 400 exact theta decompositions, containing 1,860 state polygons, passed.
- 400 exact-formula versus numerical full-unmerged-LP classifications passed:
  193 feasible and 207 infeasible. Every accepted case also passed exact
  rational decomposition/refinement against the unmerged contracts.
- 300 exact subset-family versus numerical bounded-matrix-LP classifications
  passed: 207 feasible and 93 infeasible.

The LP comparisons are labeled numerical; they are not rational certificates
of every LP status. The earlier graph-to-cut implementation audits remain
available for Stage 6 and are not relabeled as newly executed here.

New standalone check, from the manuscript directory:

```sh
python verification/stage03-exact.py
```

This uses only Python's standard library. It independently enumerates pairwise
boundary intersections for 160 rational theta domains (53 nonempty), checks
feasibility and attainment of every tight support, and enumerates bounded
integer matrices for 100 integral transportation models (35 feasible).
It verifies every column-side cut minimization identity and includes 56 cases
with a negative row demand. The equivalence of real and integer feasibility
for those small integral transportation systems uses the standard flow
integrality property. It also verifies the joint-state `1/3` obstruction.
All checks passed; see `verification/stage03-exact.json`.

The complete manuscript builds with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The result is 20 pages, with no undefined references/citations, LaTeX warnings,
or box warnings. Build output and source hashes are retained in
`verification/stage03-build.txt` and `stage03-validation.json`.

## Remaining questions

No unresolved issue was identified within the retained cycle/theta and
parallel-path scopes. No broader topology is inferred from these formulas.
The final computational section will distinguish implementation timing and
certificate behavior from these arithmetic and existence results.
