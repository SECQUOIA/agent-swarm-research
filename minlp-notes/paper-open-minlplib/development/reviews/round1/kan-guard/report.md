# Guarded KAN path-(I) replay

**Every reported KAN lower bound is confirmed by the guarded path-(I) replay. All six searches completed with no open boxes.**

The change closes issue 1 of `../sol-math-supp2.md`: the original `minquad`
assumed that halving a binary64 curvature was exact, and used an unrounded
vertex-location test with heuristic padding. The counterexample is real,
but the complete guarded replays encounter neither inexact halving nor any
other guard failure. Every replay returns exactly the archived rigorous-exp
bound, including `kan_r5_h1_n3 = -262.8642258941303`.

## Change and scope

Only the copied [kan_bnb_rigexp.py](kan_bnb_rigexp.py) was changed. The
original dossier verifier and the paper remain untouched by this task.
All repository writes are confined to this review folder. The diff is
[kan_bnb_rigexp.diff](kan_bnb_rigexp.diff).

Each broadcast scalar entry checks finite inputs, ordered intervals,
`sl <= 0 <= sh`, exact halving by `2*(0.5*m) == m`, finite raw and
outward-rounded intermediates, and a positive vertex denominator. This
includes intermediates of ignored `np.where` branches. Failed entries are
minimized with exact `Fraction` arithmetic and converted downward to
binary64. Negative rational overflow returns `-inf`; positive overflow
returns the largest finite binary64. Nonfinite or reversed input intervals
return `-inf`. An ordered displacement interval that does not contain zero
uses exact rational minimization rather than the fast path.

The convex-vertex test now intersects `[sl,sh]` with a one-ulp outward
enclosure of `-g/m`. It cannot omit an admissible exact vertex. It no longer
uses the former `1e-9` / `1e-300` heuristic padding. The endpoint and vertex
value formulas retain their outward rounding. Counters record every vector
invocation, scalar entry, guard failure and fallback, and are included in
the final JSON. The module description was corrected to identify the
rigorous certifying exponential and distinguish the heuristic library exp.

An AST comparison removes only the module description, `minquad`, its
fallback/counter definition, and the result's `minquad_stats` field. The
remaining syntax trees are identical. Thus the decoder, exponential,
other bounding formulas, local search, pruning, splitting, incumbent
certification, tolerance and final bound formula were not changed.

## Proof

The full argument is [minquad-proof.md](minquad-proof.md). For fixed `s`,
the expression is affine in `g`, so minimization reduces to the two endpoint
slopes. For each slope, the quadratic minimum is at a displacement endpoint
or an admissible convex vertex. The exact-halving guard makes `half_m = m/2`
an exact identity. The sign-aware outward endpoint computations are below
the corresponding exact values, including underflow. The vertex value is
bounded below by an upward-rounded nonnegative numerator divided by a
positive downward-rounded denominator, followed by negation. The outward
vertex-location enclosure cannot miss an admissible vertex; including an
extra unconstrained vertex only lowers the bound. On guard failure, exact
rational endpoint/vertex minimization and checked downward conversion give
the bound directly.

This establishes the claimed lower bound for every finite binary64 input
with ordered slope and displacement intervals and `sl <= 0 <= sh`. The
fallback extends it to finite ordered intervals wholly on either side of
zero. Invalid inputs produce `-inf`. The proof relies on correct binary64
rounding with gradual underflow, `nextafter`, comparisons, exact Python
integer/rational arithmetic, and correctly rounded rational conversion;
normality of `m` is not an assumed substitute for the exact-halving check.

## Targeted tests

[test_minquad.py](test_minquad.py) executes definitions extracted from
`/tmp` source copies. Its independent rational oracle selects the upper
slope on the negative displacement half and the lower slope on the positive
half, then minimizes each quadratic exactly. It does not call the fallback
as its reference. Seed: `20261004`.

All **72,240** random and adversarial rational comparisons
passed; 63,106 returned finite bounds and the rest
returned valid `-inf` bounds after negative overflow.

| Input class | Exact comparisons |
|---|---:|
| ordinary | 20,000 |
| random binary64 | 20,000 |
| subnormal | 5,000 |
| boundary grid | 10,240 |
| vertex boundary | 15,000 |
| zero width | 1,000 |
| unsigned interval | 1,000 |

Additional passing checks cover all 32 combinations of signed-zero scalar
inputs, scalar/array broadcasting, empty arrays, 17 nonfinite or reversed
input cases, and four conversion probes (positive and negative overflow,
the maximum finite result, and exact cancellation). The referee probe
`t = 2^-1074`, `gl = gh = 0`, `m = -t`, `sl = -3`, `sh = 3` returns `-5*t`,
which is below the exact minimum `-9*t/2`; the copied original returns the
unsafe `-3*t`.

The final test counters are 127 invocations and
72,300 scalar entries. There are
74 invocations with a guard failure and
29,185 failed entries, with exactly the same
fallback counts. Individual guard reasons overlap. They include 6,396
inexact halves and 24,507 nonfinite-intermediate entries. The denominator
positivity guard is mathematically unreachable on finite inputs and has
zero triggers; an initial harness assertion incorrectly demanded a trigger
for it and was corrected. No implementation change was needed for that
harness correction. Retained final results:
[test-minquad.log](test-minquad.log), [test-results.json](test-results.json).
Tests supplement the proof; they do not establish it by sampling.

## Six complete replays

| Instance | Guarded L_ver | Processed boxes | minquad calls | Scalar entries | Guard calls / entries | Fallback calls / entries |
|---|---:|---:|---:|---:|---:|---:|
| kan_r3_h1_n4 | `0.0027812371878503973` | 26,353 | 240 | 79,119 | 0 / 0 | 0 / 0 |
| kan_r3_h1_n5 | `-0.011042679449683842` | 22,301 | 234 | 66,963 | 0 / 0 | 0 / 0 |
| kan_r3_h1_n9 | `0.012963660028294303` | 42,633 | 264 | 127,959 | 0 / 0 | 0 / 0 |
| kan_r5_h1_n3 | `-262.8642258941303` | 1,648,095 | 4,175 | 8,240,575 | 0 / 0 | 0 / 0 |
| kan_r5_h1_n5 | `0.2725832539233757` | 709,937 | 1,910 | 3,549,785 | 0 / 0 | 0 / 0 |
| kan_r5_h1_n8 | `0.06932786057952356` | 615,673 | 1,675 | 3,078,465 | 0 / 0 | 0 / 0 |

`L_ver` strings are round-trip decimal representations identifying binary64
values; exact comparisons use the binary64 rational values rather than the
printed decimal strings.

Every run has `done = true`, `open = 0`, and zero counts for every individual
guard reason and for invalid inputs. The counters include local-search
candidate certification and all branch-and-bound evaluations. Calls are
vector invocations; scalar entries are the individual quadratic problems.
Every invocation with a failed entry and every failed entry would have been
counted once as both a guard event and a fallback.

| Instance | Paper L (display) | Margin above the paper exact stored L | Delta from prior rigexp L_ver |
|---|---:|---:|---:|
| kan_r3_h1_n4 | `0.002781237152581` | >= 0.0000000000352690268483 | exactly 0 |
| kan_r3_h1_n5 | `-0.01104267952179` | >= 0.0000000000720982041430 | exactly 0 |
| kan_r3_h1_n9 | `0.01296365996347` | >= 0.0000000000648195819935 | exactly 0 |
| kan_r5_h1_n3 | `-262.8642259093` | >= 0.0000000150911318996804 | exactly 0 |
| kan_r5_h1_n5 | `0.2725832538548` | >= 0.0000000000685284606838 | exactly 0 |
| kan_r5_h1_n8 | `0.06932786051052` | >= 0.0000000000689984458457 | exactly 0 |

These margin comparisons use `Fraction(L_ver)` and the exact stored `L`
from `paper-open-minlplib/data/numbers.json`, and separately check the
printed decimal `L` in `tables/tab-kan.tex`. Each printed decimal is at most
the stored exact `L`. All six guarded bounds are strictly greater than
both values. The displayed positive margins above were truncated downward
at 22 decimal places. Full exact margins and binary64 hexadecimal values
are retained in [comparison.json](comparison.json).

Every non-time field in the prior dossier JSON is identical to the replay,
including `processed`, `UB`, `ub_u`, `tol`, `lower_bound`, and completion
fields; the replay additionally contains counters. The archived rigexp logs
and their companion JSON files were also checked for equality. Therefore
all six guarded bounds are bit-identical to the previous **rigorous-exp**
bounds. The already documented comparison with the earlier library-exp
verifier remains unchanged: five bounds were bit-identical, while the
rigorous-exp `kan_r5_h1_n3` value is about `3.2e-12` lower. This task did not
rerun the earlier library-exp verifier.

## Execution, provenance and commands

All executable repository sources and OSIL inputs were copied to
`/tmp/kan-guard/` before execution or import. The replays ran in parallel,
with six worker processes pinned individually to CPUs `[0, 1, 2, 3, 4, 5]`.
OpenBLAS, OpenMP, MKL, NumExpr, vecLib and BLIS thread limits were one. After
the three r3 searches finished, further targeted checks ran without
exceeding the six-core limit. No project-wide verification, CI inspection
or commits were performed.

The environment was Python 3.13.11, NumPy
2.5.1, SciPy 1.18.0 and
mpmath 1.3.0. The random seed was zero, no extra
starts were supplied, third-order bounds were enabled, relative tolerance
was `4e-11`, and batch size was `1024`, matching the prior searches. The
wall-time limit was raised from `1800` to `7200` seconds to allow guards and
concurrent load; every search finished, so this limit did not cut off any
search. Search time is elapsed wall time, not a claimed CPU-time measurement.

| Instance | Search seconds |
|---|---:|
| kan_r3_h1_n4 | 24.74 |
| kan_r3_h1_n5 | 22.71 |
| kan_r3_h1_n9 | 58.86 |
| kan_r5_h1_n3 | 1175.59 |
| kan_r5_h1_n5 | 744.42 |
| kan_r5_h1_n8 | 1005.18 |

The executed targeted commands were:

```text
python3 -m py_compile /tmp/kan-guard/checks/kan_bnb_rigexp.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -u /tmp/kan-guard/checks/test_minquad.py
python3 -u /tmp/kan-guard/run_replays.py
python3 /tmp/kan-guard/checks/compare_results.py --partial
python3 /tmp/kan-guard/checks/compare_results.py
```

The replay driver executed this command once per instance, with the CPU and
instance substituted and the manifest's environment:

```text
taskset -c <cpu> python3 -u /tmp/kan-guard/checks/kan_bnb_rigexp.py <instance> 4e-11 7200 1024
```

The driver is archived as [run_replays.py](run_replays.py), the exact
comparison as [compare_results.py](compare_results.py), source/dependency
and six input hashes as [replay-manifest.json](replay-manifest.json), and
worker exit codes as [replay-driver-results.json](replay-driver-results.json).
The copied guarded source SHA-256 is
`e5783a244eda1b24e0767a4c676931a4a5b995fcf6946407b34a783a18df57eb`. The original source
remains SHA-256
`82ca1dbd5def9b4bb2b701650e6961b53833f0074383dce20e509d7a86b29b33`.
The six full replay logs and output JSON files are under [logs](logs/).

To repeat this work, prepare an execution tree under `/tmp`, preserving the
relative paths of `research-20260929/reviews/wave3-verification/kan_decode.py`,
`research-20260929/reviews/open-instances-verification/osilx.py`,
`research-20260929/open-instances-wave3/kan/kan_iv.py`, and
`research-20260929/open-instances-wave2/small/ia.py`. Copy the six OSIL files
from `development/reviews/code/sol-kan-review/osil/` to `/tmp/kan-guard/osil/`.
Copy this guarded source, test, and comparison script to
`/tmp/kan-guard/checks/`, the original dossier source to
`checks/original_kan_bnb_rigexp.py`, and the replay driver to
`/tmp/kan-guard/run_replays.py`; create `checks/logs/`. The comparison also
reads copies of `paper-open-minlplib/data/numbers.json`,
`paper-open-minlplib/tables/tab-kan.tex`, and the prior dossier `.rigexp.log`
and `.bnb.json` files, placed in `/tmp/kan-guard/archive/` by basename. The driver sets `MINLPLIB_OSIL_ROOT` and `PYTHONPATH`
to those copied paths. Source paths here are relative to the repository
unless starting with `development/`, which is relative to
`paper-open-minlplib/`. Do not execute the scripts from the repository.

## Exact replacement text for the paper

Use the guarded artifact as the path-(I) implementation and add this
paragraph to the path-(I) arithmetic/trust-base discussion in
`sections/B9-ann-kan.tex`. The historical statement that only the
exponential changed belongs to the earlier rigorous-exp rerun; distinguish
this subsequent guarded replay rather than applying that AST-identity
statement to the new routine. The replacement is:

```latex
Path~(I) was subsequently replayed with a guarded quadratic lower-bound
routine. Every scalar quadratic calculation checks finite inputs and
intermediates, ordered intervals, signed displacements
$s_l\le0\le s_h$, and exact representability of $m/2$ by the test
$2\operatorname{fl}(m/2)=m$; the convex vertex location is enclosed by
outward rounding. If a check fails, the minimum over the endpoint slopes
and the displacement endpoints and admissible convex vertices is computed
in exact rational arithmetic and rounded down; nonfinite or reversed
interval data return $-\infty$. The endpoint and vertex formulas, together
with this fallback, give a lower bound even for subnormal inputs. All six
complete replays reproduced the archived rigorous-exponential values of
$\Lcert_{\mathrm{ver}}$, with no open boxes, no guard failures and no
fallbacks; each value strictly exceeds the reported $\Lcert$, comparing
the exact stored numbers. The trust base of path~(I) is
\cref{hyp:fp-ieee}, the correctness of the OSIL reader and exact decoder,
the interval and bounding implementation including these guards, the
rigorous exponential enclosure and its rationally checked constants,
the certified SiLU minimum constants, the exact rational positive-definite
Hessian check, and the box covering and pruning performed by the search.
The guards and replays close the arithmetic-domain gap in the quadratic
routine; they do not replace the correctness premise for the remaining
implementation or the components shared with path~(II). The exponential
enclosure, its interval core and the OSIL reader remain shared by the two
paths, so agreement does not remove those shared premises.
```

The fallback's Python exact arithmetic belongs to the routine's general
trust base; it was not exercised in any of these six searches. This work
repairs and proves `minquad` and replays path (I). It does not supply a new
line-by-line verification of the rest of the verifier, a NaN-safe replay of
path (II), or new primal certificates.
