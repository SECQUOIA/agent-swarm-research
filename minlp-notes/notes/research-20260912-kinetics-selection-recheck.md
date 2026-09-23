On the archived kinetics statistical inputs, correcting the selection covariance
changes one optimizer among the 33 comparisons made here. At budget $3,000,
the full-inverse gating optimizer loses 3.1128% of the optimal true trace
information under the corrected marginal likelihood. The D-optimal and
conventional A-optimal selections agree under
both formulas at every tested budget. Objective inflation remains present even
where the selected design agrees.

This is an independent exhaustive comparison of our optimizers on the supplied
numerical inputs and code constraints. It does **not** identify the authors'
archived selected designs, which were not deserialized, and does not regenerate
the physical experiment that produced the sensitivities. The statistical issue
and source locators are documented in the
[source audit](research-20260912-measurement-source-audit.md).

The input is the unmodified `kinetics_source_data/Q_drop0.csv` from author-repo
commit `430090e610446aab88328ce495ffb15b684c56c4`. The local
[data copy](../code/research_20260912/data/kinetics_Q_drop0.csv) and
[provenance record](../code/research_20260912/data/kinetics_Q_drop0.provenance.json)
preserve the immutable URL and SHA-256
`54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca`.
There are four parameter columns, eight times per species, and identical SCM/DCM
sensitivities for a species at a given time. The fixed same-time covariance is
the symmetric code covariance `R6 = [[B, B/2], [B/2, B]]`, where
`B = [[1,.1,.1],[.1,4,.5],[.1,.5,8]]`. Different times are independent.
The asymmetric entry in the printed SI table is not used.

The experiment has times 7.5, 15, …, 60 minutes. An SCM costs $2,000 and selects
all eight times for its species. A DCM costs $200 to install and $400 per sample.
The same species cannot use both modalities. The code's global ten-minute DCM
separation permits at most one manual sample at a time and forbids manual
samples at adjacent time indices, including samples of different species. Thus
at most four manual samples are possible; the stated per-species and total
manual caps of ten never bind. At least one measurement is selected. These are
the archived code constraints; other readings of the article's sampling rule
would define a different feasible set.

For each allowed same-time subset P, the code independently precomputes

\[
I_{t,P}^{\mathrm{marg}}=F_{t,P}^{\top}(R_6)_{PP}^{-1}F_{t,P},
\qquad
I_{t,P}^{\mathrm{gate}}=F_{t,P}^{\top}(R_6^{-1})_{PP}F_{t,P}.
\]

Both total information matrices add `0.0001 I`, matching the source's diagonal
regularization. This term affects low-budget rank-deficient designs and is
included in every reported criterion. It is not asserted to be independently
justified prior information. All calculations use the supplied parameter
coordinates and scaling. “Trace information” means maximizing `trace(J)`, called
A-optimality in the inspected source. Conventional A-optimality minimizes
`trace(inverse(J))`; it is an additional comparison here. D-optimality maximizes
the natural logarithm of `det(J)`.

There are 20 allowed same-time patterns after the modality and at-most-one-DCM
restrictions. For s SCM species and q manual samples, there are
`binom(3,s) binom(9-q,q) (3-s)^q` schedules, summed over s=0,…,3 and q=0,…,4.
The total is 2,348 including the empty design, or 2,347 source-feasible nonempty
designs before budget filtering. The algorithm evaluates every design under
both information rules and all three criteria once, then filters budgets
$1,000, $1,400, …, $5,000. No MIP or nonlinear optimizer is needed for this case.

The trace-information results are:

| Budget | Feasible designs | Corrected optimum | True information of gated optimizer | True loss |
|---:|---:|---:|---:|---:|
| $1,000 | 87 | 21.431331925 | 21.431331925 | 0 |
| $1,400 | 273 | 30.316097012 | 30.316097012 | 0 |
| $1,800 | 768 | 36.743426273 | 36.743426273 | 0 |
| $2,200 | 1,161 | 70.420288488 | 70.420288488 | 0 |
| $2,600 | 1,209 | 77.188090665 | 77.188090665 | 0 |
| $3,000 | 1,335 | 83.030295878 | 80.445728498 | 2.584567380 |
| $3,400 | 1,581 | 88.659442368 | 88.659442368 | 0 |
| $3,800 | 1,971 | 93.097825710 | 93.097825710 | 0 |
| $4,200 | 2,184 | 119.594969939 | 119.594969939 | 0 |
| $4,600 | 2,208 | 126.435087553 | 126.435087553 | 0 |
| $5,000 | 2,271 | 129.740997799 | 129.740997799 | 0 |

The changed $3,000 trace-information choice is fully specified below. An SCM
observes its species at all eight times; each design costs exactly $3,000.

| Formula optimized | SCM | DCM samples | Marginal trace | Gated trace |
|---|---|---|---:|---:|
| Correct marginal formula | B | C at 45 and 60 min | 83.0302958778916 | 108.080741408421 |
| Full-inverse gating | B | A at 7.5 and 22.5 min | 80.4457284983500 | 108.307086326390 |

The true trace loss is `2.584567379541568`, or `0.031128003967883705` of the
corrected optimum. Gating inflates trace by a factor `1.3017024722` at the
corrected design and `1.3463373177` at its own optimizer. This difference in
inflation reverses their ordering. The trace-optimal corrected design is not
asserted to be optimal for a different criterion such as determinant.

For all eleven D-optimal comparisons and all eleven conventional A-optimal
comparisons, the selected designs agree under the two information rules. Their
true selection regret is zero. At the D-optimal selections, gating inflates the
regularized determinant by factors from `1.8137` to `3.2523`, corresponding to
four-parameter D-information factors from `1.1605` to `1.3429`.

The full [JSON results](../code/research_20260912/kinetics-selection-recheck.json)
preserve every selected design, its cost, both evaluations of all three
criteria, inflation at both returned optima, and the best and worst true scores
over numerical gated-optimal ties. The
[CSV summary](../code/research_20260912/kinetics-selection-recheck.csv) contains all
33 comparisons. Every numerical optimum set is a singleton under the stated
tolerance `1e-9 * max(1, abs(best objective))`; consequently the reported best
and worst true values among those ties coincide.

The implementation is
[`kinetics_selection_recheck.py`](../code/research_20260912/kinetics_selection_recheck.py).
Reproduce it from the repository root with:

```sh
uv run --project code/research_20260912 python \
  code/research_20260912/kinetics_selection_recheck.py \
  --output code/research_20260912/kinetics-selection-recheck.json \
  --summary code/research_20260912/kinetics-selection-recheck.csv
```

An independent enumeration of the four possible manual states at each time
matched the schedule generator exactly. All 2,347 designs were checked against
dense submatrix calculations using the full 48-candidate covariance, for both
information rules. The maximum relative matrix discrepancy was `3.74e-16`, the
largest absolute log-determinant discrepancy was `9.30e-12`, and every gated
minus marginal matrix was positive semidefinite up to roundoff. These checks
test the implemented finite problem independently of the pattern sums.

The first complete sweep, including both independent checks, took approximately
0.31 seconds with NumPy 2.5.3. This establishes that exhaustive checking is
practical for this constrained instance; it is not a controlled runtime
comparison with the authors' software. Enumeration covers every feasible
design, but objective arithmetic and numerical tie detection in the primary JSON
results use floating point. The data's physical sensitivity-generation provenance remains
unresolved, and none of the results establish changes to every correlated-noise
benchmark or to the authors' stored selections.

An additional
[exact trace certificate](../code/research_20260912/kinetics-trace-certificate.json)
removes floating-point comparisons from the trace conclusions. Its
[independent arithmetic script](../code/research_20260912/kinetics_trace_certificate.py)
reads each archived CSV decimal string as a `Fraction`, constructs the rational
code covariance, inverts covariance blocks by rational Gauss-Jordan elimination,
and forms every trace coefficient exactly. It evaluates all 2,347 schedules
under both formulas and all eleven budgets, including the exact regularization
`4/10000` in each trace. A second enumeration again checks the feasible schedule
set. Decimal approximations in the certificate are display values and do not
determine rankings.

Every trace optimum is unique in exact arithmetic. The only optimizer change
remains at $3,000. At that budget the corrected winner, SCM-B with DCM-C at
45 and 60 minutes, exceeds its runner-up, SCM-B with DCM-C at 37.5 and 52.5
minutes, by exactly

```text
40790370329026134252313294029080809
/ 204400000000000000000000000000000000
```

which is approximately `0.19956149867429615`. The gated winner, SCM-B with
DCM-A at 7.5 and 22.5 minutes, exceeds its runner-up, the corrected winner,
under the gated objective by exactly

```text
107423298067956910413270175822536134960728787518627092294553
/ 474600000000000000000000000000000000000000000000000000000000
```

which is approximately `0.22634491796872505`. Its exact true trace regret is

```text
2199814141231484373123939179832885522375657830969353821095757
/ 851134375000000000000000000000000000000000000000000000000000
```

or approximately `2.584567379541549`. The exact relative regret is approximately
`0.031128003967883486`; its full fraction and every budget's exact winner,
runner-up margin, regret, and inflation ratios are preserved in the certificate.
This certifies the rational interpretation of the **as-stored numerical data**.
It does not establish that the underlying physical sensitivities are exact.
The rational sweep and enumeration check took about 0.25 seconds on this run.

Reproduce the exact trace certificate with:

```sh
uv run --project code/research_20260912 python \
  code/research_20260912/kinetics_trace_certificate.py \
  --output code/research_20260912/kinetics-trace-certificate.json
```
