# Stage 5: algorithms, transfer, and certified coarsening

Run from the paper directory or a relocated copy of it:

```sh
python verification/stage05/run_checks.py
```

Python 3 and its standard library suffice. Run without `-O`; the new entry
points reject disabled assertions, and the historical checkers use assertions.
The runner checks every original artifact against the provenance manifest,
runs four unchanged independent historical checkers and the new checks, then
writes local logs and `check-summary.json`. Snapshots omit logs; the summary
and every input needed to regenerate them are included. Run log-producing
commands on a working copy, not an immutable snapshot.

`coarsening.py` supplies the new exact coarsener. The input rows contain
integrated masses, interpreted as constant rates inside their input cells.
Nonaligned coarse endpoints are handled by exact integration. This assumption
matters: arbitrary rates inside a fine cell cannot be reconstructed from
that cell's masses alone. For a general measurable control, the manuscript
theorem instead assumes its actual coarse cumulative values are available.

```python
from fractions import Fraction as Q
from coarsening import certified_coarsen

answer = certified_coarsen(
    ((Q(1, 3), 0), (0, Q(2, 3))),
    (Q(1, 3), Q(2, 3)),
    switch_budget=1,
    epsilon=Q(1, 4),
)
print(answer.exact_error, answer.schedule)
print(answer.lower, answer.lower_strict, answer.upper)
```

For this import example, add `verification/stage05` to the Python path or
run from that directory. `cells=M` may replace `epsilon`; exactly one must
be supplied. Labels are zero-based. The schedule has one label per uniform
coarse cell and at most the requested number of actual changes. The exact
error concerns the supplied rational input. With the default zero tolerance,
`upper` is that exact schedule error. `lower_strict` distinguishes an open
lower endpoint from a closed endpoint after clipping a negative bound to zero.
If the unclipped lower endpoint equals zero, it remains strict.

The optional `cumulative_tolerance=delta` requires the caller to establish
that the original cumulative input differs from the supplied one by at most
delta in the uniform component norm. Then `upper` bounds the returned
schedule's error for the original input, and the interval bounds its
continuous optimum. The certificate width before clipping is `h+2*delta`.
The routine uses the general strict-width-h certificate uniformly; the
manuscript also proves stronger half-width certificates for one switch or
two modes and exactness for zero switches.

The coarse schedule is continuously feasible. It is feasible for a prescribed
fine switching grid only if its actual switching boundaries are allowed there;
the theorem's sufficient condition is nesting of the entire coarse grid.
No dwell or transition constraints are imposed by the coarsener. The archived
grid DP accepts minimum dwell times, but this does not make its constrained
optimum satisfy the unrestricted continuous certificate. The manuscript's
odd-grid dwell example proves that the failure can persist under refinement.

`check_new_results.py` checks 48 nonuniform input/budget cases by evaluating
every coarse word against the original input on the common refinement. It
also enumerates feasible words on a nested grid of twice the resolution and
checks the certificate interval. Further cases cover nonaligned exact masses,
both lower-endpoint conventions, epsilon rounding, invalid inputs, four
quantized-input bounds, and four dwell-refinement examples. These checks use
direct integration, not the tested cost recurrence, to evaluate schedules.

`continuous_exact.py` is a small-instance rational word/time-cell/vertex
enumerator, with separate full and one-sided objectives. It is deliberately
slow and complete: it enumerates all words, nondecreasing closed input cells
for switch times, and nonsingular sets of active inequalities for each bounded
LP. No numerical optimizer or rational reconstruction is used. Tests cover
nine analytically known optima, including switches on input boundaries,
an exactly reproduced input with a disconnected repeated mode,
constant schedules represented by repeated labels and zero-length blocks,
and the one-cell three-mode input with two switches. In the latter case,
the full optimum is 1/6 while the one-sided optimum is 8/57; thus confusing
the two objectives is detected. A separate degenerate polytope check confirms
the vertex method handles a lower-dimensional feasible set.

The four historical checkers add direct exhaustive comparisons for one switch,
crossing queries, prescribed subsets, fixed budgets, repeated modes, arbitrary
prefix completion, candidate labels, dwell feasibility, supported transfer,
and binary nonuniform transfer. Their exact counts and the nine continuous
solutions are recorded in `check-summary.json`. They support the printed
proofs; they do not substitute numerical testing for a universal theorem.

Build the manuscript with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`source-record.md` supplies primary-source locators and hashes. Source PDFs
are not redistributed. Application data and comparative computations belong
to the subsequent computational section.
