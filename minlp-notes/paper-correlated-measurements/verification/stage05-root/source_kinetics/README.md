# Exact public-kinetics rankings

This experiment independently reconstructs the acquired schedules from the
audited public code and evaluates all three information criteria in rational
arithmetic. It imports neither the original reanalysis nor third-party
optimization code and does not deserialize stored author selections.

The input is `kinetics_source_data/Q_drop0.csv` from
[dowlinglab/measurement-opt at commit 430090e](https://github.com/dowlinglab/measurement-opt/tree/430090e610446aab88328ce495ffb15b684c56c4).
Its SHA-256 is
`54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca`.
Prepare `kinetics_Q_drop0.csv` locally with `prepare_input.py`. The command
retrieves the pinned source URL and verifies the SHA-256 before writing the
input; a separately obtained copy can be supplied with `--from-file PATH`.
The local input is ignored by Git. The source URL and full commit are also
stored in the exact result. This provenance identifies the supplied numerical
table; it does not verify how its physical sensitivities were generated.

The 24 rows are species-major, eight times for each of A, B and C, with columns
A1, A2, E1 and E2. SCM and DCM use the same sensitivity rows. The six-response
same-time covariance is `[[B,B/2],[B/2,B]]`, where
`B=[[1,1/10,1/10],[1/10,4,1/2],[1/10,1/2,8]]`; distinct times are independent.
The information regularizer is `I4/10000`. Every input decimal, including tiny
nonzero sensitivity entries, is interpreted exactly as written.

SCM selects one species at all eight times for cost 2000. DCM costs 200 per
installed species plus 400 per sample; a species cannot use both modes.
At most one DCM sample is taken at a time, no consecutive candidate times
may both have a DCM sample, and there are at most four manual samples.
Times are 7.5, 15, ..., 60 minutes. Empty acquisition schedules are excluded.
Budgets are 1000, 1400, ..., 5000. Redundant installations with no acquired
sample are not separate acquisition schedules.

The time labels follow the intended dropped-zero convention: sample index `i`
is reported at `7.5(i+1)` minutes. In the pinned source, `kinetics_MO.py:207`
constructs `linspace(0,60,9)`, and lines 214–215 map its final eight entries
to 7.5, ..., 60. Line 275 passes the full nine-entry array to the optimizer;
`measure_optimize.py:1059–1064` uses its first eight entries for the spacing
map, producing 0, ..., 52.5 instead. This uniform shift leaves every pairwise
time difference, 10-minute exclusion window and feasible acquisition schedule
unchanged. The supplied sensitivity rows have the initial zero rows dropped;
we preserve their intended labels and all reported selections and objectives.

From this directory, run:

```sh
python prepare_input.py
python exact_rankings.py --output rankings-rerun.json
python check_rankings.py --record rankings-rerun.json --output rankings-rerun-check.json
```

The generator uses the Python standard library. The independent checker needs
SymPy (the recorded run used 1.14.0). The explicit output names above preserve the archived results and their manifest
hashes. The `--data`, `--output` and `--record` options support other new rerun
locations.
`check_rankings.py --winners` checks all ranking decisions and directly evaluates
the 51 distinct reported winners and runners-up; the default directly evaluates
**all 2,347 schedules** and was used for the archived validation.

`exact-rankings.json` contains every schedule's exact trace, determinant and
trace of inverse under both the marginal and gated information formulas, plus
every exact optimum set and runner-up margin. The generator uses two independent
schedule enumerations, rational local information, and principal cofactors for
the inverse trace. The checker instead assembles the full 48-response covariance
in mode/species/time order, directly inverts its selected submatrices, and
computes the inverse information matrix. It matches all 14,082 exact objective
values and rechecks all ranking decisions. Fractions, not floating tolerances,
determine every equality and ordering.

All 66 formula/criterion/budget optimum sets are singletons. Marginal and gated
choices agree in every D and conventional A comparison. The only changed choice
is the trace criterion at budget 3000: the marginal optimum selects SCM B and
DCM C at 45 and 60 minutes; gating selects SCM B and DCM A at 7.5 and 22.5
minutes. Its exact relative true-trace regret is
`2199814141231484373123939179832885522375657830969353821095757/70669938988094335150669123840613003115148437500000000000000000`,
approximately 0.031128003967883486. Determinant rankings establish D rankings
without computing logarithms. Conventional A minimizes the inverse trace;
the source's criterion called A instead maximizes the information trace.

The observed generator time was 3.0742 seconds before serialization, including
input, enumeration and matrix validation. The separate complete checker took
16.1405 seconds. These are individual validation runs, not a controlled timing
comparison with the published optimizer. Mathematical outputs reproduce exactly;
timings and file hashes incorporating timing fields naturally change on rerun.
