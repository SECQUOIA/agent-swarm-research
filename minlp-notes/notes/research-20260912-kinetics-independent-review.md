Independent review, 2026-09-12. **The archived-input selection result is
reproduced.** The finite problem contains 2,347 nonempty schedules. Across the
eleven budgets and three criteria, only the $3,000 trace-information comparison
changes its winning selection. A separate rational calculation confirms every
trace winner and its uniqueness. I found no remaining substantive defect in the
reviewed recheck or trace certificate.

The $3,000 result is:

| Formula optimized | SCM installed | DCM samples | Marginal trace | Gated trace |
|---|---|---|---:|---:|
| Marginal selected covariance | B | C at 45 and 60 minutes | 83.0302958778916 | 108.080741408421 |
| Full-inverse gating | B | A at 7.5 and 22.5 minutes | 80.4457284983500 | 108.307086326390 |

Each design costs $3,000. The gated design loses approximately
`2.584567379541549`, or **3.1128003968% of the corrected optimum**, in true trace
information. Expressed with the gated design in the denominator, the corrected
design improves true trace by approximately 3.2128087194%. These percentages
answer different comparisons. The original opening of the
[recheck note](research-20260912-kinetics-selection-recheck.md) incorrectly used
the first percentage as an improvement over the gated design; I reported that
wording defect and verified its correction.

This review covers the
[recheck implementation](../code/research_20260912/kinetics_selection_recheck.py),
its [JSON](../code/research_20260912/kinetics-selection-recheck.json) and
[CSV](../code/research_20260912/kinetics-selection-recheck.csv), the
[trace certificate implementation](../code/research_20260912/kinetics_trace_certificate.py)
and [certificate](../code/research_20260912/kinetics-trace-certificate.json), and
the implementation claims in the
[source audit](research-20260912-measurement-source-audit.md). The author checkout
at `/tmp/minlp-measurement-source-audit-20260912/measurement-opt` was clean and
reported commit `430090e610446aab88328ce495ffb15b684c56c4`. I read its Python and
CSV files without importing author modules or deserializing stored results.

The source mapping and constraints passed the following checks.

| Item | Independent check and conclusion |
|---|---|
| CSV rows and parameters | The original and local CSV copies are byte-identical, with SHA-256 `54506ecb5606ea8900a99cb8490508bdd4b9a364aba4f26efe2676f9a7f6f3ca`. There are 24 rows and four parameter columns, `A1,A2,E1,E2`. The leading index column has labels 1–8, 10–17, and 19–26 and is excluded from the sensitivities. |
| Six-channel mapping | Source `SensitivityData.get_jac_list`, lines 199–223, selects source row `8*s+t` separately for each SCM and DCM species. Thus source channel-major row `8*c+t` has sensitivity `Q[8*(c % 3)+t]`. The recheck's time-major row `6*t+c` represents exactly that same observation. No index label is mistaken for a parameter or used as a row position. |
| Covariance | Source `kinetics_MO.py`, lines 69–110, halves cross-modality correlations. The mathematical result is `R6 = [[B,B/2],[B/2,B]]`, with `B = [[1,.1,.1],[.1,4,.5],[.1,.5,8]]`. Source `measure_optimize.py`, lines 723–737, correlates channels only at matching times. In source ordering the full matrix is `R6 ⊗ I8`; permuting to time-major ordering gives `I8 ⊗ R6`. |
| Positive definiteness and inverse | The full covariance's smallest computed eigenvalue was approximately `0.4978337623`. Its pseudoinverse and direct inverse differed by `2.27e-15` in relative Frobenius norm. The source's use of `pinv` therefore does not introduce a different statistical expression here. |
| SCM and DCM costs | One selected SCM installs a species for $2,000 and includes all eight observations. Each used DCM species incurs $200 once, plus $400 for each selected time. Source installation constraints, lines 1292–1321, force the installation indicator to equal the logical OR of that species' samples. The recheck correctly omits redundant installation decisions. |
| Modality exclusivity | Source pairs `[0,3]`, `[1,4]`, and `[2,5]` prohibit SCM and DCM installation for the same species. This is an installation restriction across the entire schedule. The recheck correctly forbids all manual samples of an installed SCM species. |
| Global spacing | Source forward windows, lines 1424–1454, sum samples over every DCM species while the time difference is strictly less than ten minutes. On this grid each window contains its starting time and the next time, where present. Therefore simultaneous samples of different species and samples at adjacent indices are both forbidden. Samples two indices apart are allowed. |
| Time labels | The nonzero CSV points are labeled 7.5, 15, …, 60 minutes, consistently with `Q_drop0.csv` and the source's `dynamic_time_dict`. A source detail is that the optimizer receives the full nine-point `linspace(0,60,9)` and uses its first eight entries for spacing, internally 0, 7.5, …, 52.5. This constant shift leaves all pairwise time differences and every feasibility result unchanged. |
| Sample caps and nonempty selection | Global spacing permits at most four DCM samples, so both stated caps of ten are redundant. Source lines 1190–1202 and 1344–1350 exclude the entirely empty selection. The recheck correctly includes pure SCM and pure DCM choices and excludes only the wholly empty design. |
| Budget and regularization | Budgets are upper bounds, with no requirement to spend the entire amount. The eleven values are $1,000 through $5,000 in $400 steps. Each information matrix includes `1e-4 I4`, as required by source lines 1180–1185 and `small_element_value = 0.0001`. Its trace contribution is exactly `4/10000` in the rational calculation. |

The immutable source files are
[`kinetics_MO.py`](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/kinetics_MO.py),
[`measure_optimize.py`](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/measure_optimize.py),
and
[`greybox_generalize.py`](https://github.com/dowlinglab/measurement-opt/blob/430090e610446aab88328ce495ffb15b684c56c4/greybox_generalize.py).
These comparisons used the local files at that commit.

For completeness, choosing `s` SCM species and `q` manual samples gives
`binom(3,s) binom(9-q,q) (3-s)^q` schedules. The second factor counts
nonadjacent subsets of eight times. Summing over `s=0,…,3` and `q=0,…,4`, then
removing the empty schedule, gives 2,347. There are 20 feasible same-time channel
patterns, including the empty time pattern. For an independent computational
check, I enumerated four manual states per time, imposed the source's actual
forward windows, and separately enumerated three binary SCM installation
decisions. This uses neither the recheck's combinations generator nor its
pattern generator. It produced 2,347 unique schedules and these budget counts:

| Budget | Feasible schedules |
|---:|---:|
| 1,000 | 87 |
| 1,400 | 273 |
| 1,800 | 768 |
| 2,200 | 1,161 |
| 2,600 | 1,209 |
| 3,000 | 1,335 |
| 3,400 | 1,581 |
| 3,800 | 1,971 |
| 4,200 | 2,184 |
| 4,600 | 2,208 |
| 5,000 | 2,271 |

I constructed the full 48-by-48 covariance by explicit source-order channel and
time indices and evaluated every schedule directly. For selected observations
`U`, the marginal matrix is
`1e-4 I4 + F_U.T @ inverse(Sigma_UU) @ F_U`; the gated matrix instead uses
`inverse(Sigma)_UU`. Both retain the SCM/DCM cross terms at matching times. This
also independently checks that the recheck's block sum does not drop those
terms or invent correlations between different times.

The three criteria have the correct directions: maximize trace information,
maximize natural log determinant, and minimize trace of inverse information.
Source lines 1562–1567 maximize trace under the name A-optimality and maximize
the grey-box log determinant for D-optimality. The grey box calls NumPy
`slogdet`, so the natural-log interpretation is correct. Conventional
A-optimality is the additional inverse-trace comparison. It must remain
distinguished from the source's trace criterion.

All 33 independently computed comparisons matched the reported selected
schedules and regret. At the reported selections, maximum relative discrepancies
across the independently evaluated criteria, normalized by
`max(1, abs(reported value))`, were `6.01e-16` for trace, `7.38e-13` for log
determinant, and `7.97e-12` for inverse trace. The JSON and all 33 CSV rows agreed
on the checked objective fields and complete selected schedules. Rerunning both
reviewed implementations reproduced their JSON contents after excluding timing
fields, and reproduced the CSV byte for byte.

Regret is evaluated using the marginal criterion at the gated optimum. For a
maximized criterion it is the marginal optimum minus that achieved value; for
inverse trace it is that achieved value minus the marginal minimum. The code's
sign conversion implements both correctly. For D-optimality, a log-determinant
regret `delta` corresponds to determinant efficiency `exp(-delta)` and
four-parameter D-efficiency `exp(-delta/4)`. These quantities are computed in
the correct direction. Relative trace and inverse-trace regrets use the
marginal optimum as denominator.

Every numerical optimum is a singleton under the stated tolerance
`1e-9 * max(1, abs(best objective))`. The smallest observed best-to-runner-up gap
under that same normalization, across budgets and both formulas, was about
`2.09e-3` for trace, `6.44e-4` for log determinant, and `1.38e-6` for inverse
trace. The selected designs are consequently not artifacts of the declared
tie tolerance. The best and worst true scores over gated ties coincide. All
eleven D-optimal and all eleven conventional A-optimal selections agree under
the two formulas. Those non-trace ranking checks use floating point; they do
not constitute exact or interval certificates.

I separately checked the trace certificate with SymPy rational arithmetic,
using my own schedule set, exact CSV decimal strings, and the rational code
covariance. The calculation used `trace(precision * (F * F.T))`, with exact
matrix inverses, rather than importing the certificate's Fraction elimination
or trace routine. Across all eleven budgets it matched every exact winning
trace, runner-up trace, winning margin, regret, relative regret, and reported
inflation ratio. Every exact trace optimum was unique. At $3,000 the marginal
winner exceeds its runner-up by approximately `0.19956149867429615`; the gated
winner exceeds its runner-up by approximately `0.22634491796872505`. Its exact
marginal trace regret is

```text
2199814141231484373123939179832885522375657830969353821095757
/ 851134375000000000000000000000000000000000000000000000000000
```

The exact statement concerns the rational interpretation of the stored decimal
sensitivities and covariance. It does not establish exact physical
sensitivities, or reproduce every floating-point rounding step in the original
covariance construction. Both the dense floating-point and independent exact
calculations support the reported decision change.

The review does not resolve the sensitivity generator, experiment settings, or
parameter scaling that produced the CSV. It preserves the supplied coordinates
and the source's numerical regularization; trace and inverse trace depend on
those choices. It compares independently optimized choices using the archived
inputs and implemented constraints. No author optimization solver was run, no
stored author selections were deserialized, and no claim is made that the
authors' archived or published selections have been identified. I did not
re-audit the manuscript versions or the printed SI table; this numerical review
uses the symmetric code covariance and the documented source-audit distinction.
Nothing here extends the result to every correlated-noise instance or to a
different interpretation of the sampling constraints.

The temporary independent review programs are
`/tmp/kinetics_independent_review_20260912.py` and
`/tmp/kinetics_independent_exact_review_20260912.py`. Their results are preserved
for this session in
`/tmp/kinetics-independent-review-results-20260912.json` and
`/tmp/kinetics-independent-exact-review-results-20260912.json`. They ran with
NumPy 2.5.3 using:

```sh
uv run --project code/research_20260912 python \
  /tmp/kinetics_independent_review_20260912.py
uv run --project code/research_20260912 python \
  /tmp/kinetics_independent_exact_review_20260912.py
```

The exact review additionally compares fresh rerun artifacts named in its
source. The durable recheck and certificate reproduction commands are in the
main recheck note. Reviewed artifact SHA-256 values are:

```text
kinetics_selection_recheck.py
  1a742839926d2c0f4b47a98676a1d87958247d16d7e296a1573766b27f52277e
kinetics-selection-recheck.json
  33d45ea362f2739e950ca10f4109c3dd45662460230ee47c10102ada74cb31e2
kinetics-selection-recheck.csv
  651b99165ae1bfc54352bad3429e32d7936ac480ef11f6602bf7481db439c58b
kinetics_trace_certificate.py
  f328495032eef3a1fbd49fbd90d618bb35037291b09277e2debb60228f4d3b5b
kinetics-trace-certificate.json
  30f6ec627ea879118853a741c87d4c8e11899139b9df17e2b63c5edef2ef8b7c
```

No author files or literature KB files were edited, and no KB checks were run.
