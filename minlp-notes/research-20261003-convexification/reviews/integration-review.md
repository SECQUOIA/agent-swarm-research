# Independent original-row integration review

The implementation was cleared for the prospective campaign after the
supported model semantics, support conversion, actual inserted rows, and
saved-cut replay passed the checks below. This is internal review by agents
separate from implementation authors. It is not external peer review or
formal verification.

## Validity argument and binding

Every mode submits the same source model through the reviewed common builder.
The experimental separator keeps the original nonlinear rows. It selects
signed original sides `h_r(x) + d_r v <= b_r`, where `v` includes original
variables and, when needed, the common objective epigraph. A numerical LP
proposes nonnegative multipliers. The support kernel verifies the proposed
binary64 coefficients over a box justified by original affine implications
and optional original affine block rows. The row converter then eliminates
the selected nonlinear sides and compensates exactly for rounding the final
linear coefficients. Only global root cuts are submitted.

The independent replay reconstructs every nonlinear and affine row part from
the archived original expression trees and binary64 leaves. Saved feature
strings are compared with these reconstructions, never parsed or evaluated.
It separately checks objective sense, selected upper/lower sides, row
constants, side multipliers, original domain rows, and inferred bounds. The
support certificate is replayed against those independently reconstructed
inputs. Its digest binds the exact row-elimination certificate. The actual
inserted SCIP columns, coefficients, constant, bounds, and global scope must
then match the exported linear row.

The new metadata audit also rebuilds the submitted model without optimizing
it. It binds the source variables, objective epigraph, complete original-row
admission, exact affine implications, and source-domain guard records to the
archived original input. Guard equations and witness bounds are separately
derived from the real domain identities. This matters when a zero multiplier
or cancellation would otherwise erase a logarithm or reciprocal domain.

## Findings resolved before freeze

- Source-domain admission and native model construction had the issues
  documented in [model-review.md](model-review.md), including variable-power
  restrictions, pure constant rows, and row-side constant rounding. These
  were fixed and independently tested.
- The actual-row audit initially allowed two source variables to map to one
  transformed column. Such an aggregation identity is not part of the cut
  certificate. The audit now rejects duplicate transformed-column mappings,
  as well as missing nonzero columns and unproved fixed-variable substitutions.
- The actual upper-side test now explicitly requires an infinite SCIP upper
  side; a NaN cannot pass an inverted comparison.
- The prospective harness had four independent audit findings concerning
  binary domains, missing validation fields, setup-time charging, and partial
  cut logs. These were fixed before the experiment, as recorded in
  [experiment-review.md](experiment-review.md).

No unresolved model or added-cut correctness blocker remained at freeze.
Unsupported admission, bounded direction searches, and support-budget exits
remain explicit limitations. Failure to find a cut does not establish hull
membership.

## Targeted evidence before freeze

The following independent review commands passed:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_row_rounding_review.py
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_support_wrapper_review.py
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_replay_review.py
```

They passed five, three, and five tests respectively. The row tests establish
the exact worst rounding error by independent box-corner enumeration. The
wrapper tests use a three-variable equality simplex with exact support `1/3`,
an exact rational feature with an actual binary64 normal, and a zero-weight
feature with a pole. The replay tests run a real SCIP mechanism, reconstruct
its saved cuts from the original model, and reject 14 distinct corruptions.
They also check objective sense, unproved substitutions, and finite or NaN
upper bounds.

Separately, all 15 known-synthetic worker records and all 13 recorded cuts in
the preflight passed original-model replay. All 14 tamper controls were
rejected. The result is saved in [preflight-replay.json](preflight-replay.json).
The model reviewer passed 31 independent tests, and the polytope reviewer
passed 40 analytic, adversarial, and mutation diagnostics; their notes give
the commands and exact scope. No new holdout model was optimized before the
campaign freeze.

## Frozen source identities

| File | SHA256 |
| --- | --- |
| `solver/integration.py` | `5620d3f26473e56e0f0f0b086412508caa416bc190e207d85ea6c815db73e1be` |
| `solver/model.py` | `e4b13e50e0104ed2351b51840ac2a5c0154ad64a864ea257a91336af05638cbe` |
| `solver/bounds.py` | `51136605f4d26cb70b1d27348423a2a05fc26368e2a7b69e151598a70a4c3b35` |
| `solver/support.py` | `c260fb292db9f5cc59af2d3fd9ddde325f504088a2f83bfd8c0f649594c4d84c` |
| `solver/row_certificate.py` | `6917a78df65e0c7edc4dcf3fe695296fb6b9164c51d145f0b32f655fad6b2a9c` |
| `experiments/replay.py` | `b6e0fe49f87d6875aa3ce7b65acff3bd7586997cecd79af55104cf5c01582551` |
| `reviews/model_binding_audit.py` | `00e601bb928fdf8f4905c4ce60a37f383bd802cbe46c74ee82b54762d06d7e6e` |

The campaign's source manifest is authoritative for its snapshot. Complete
campaign and matched-repair replay are recorded below. Only topic-specific
local checks were run; no project-wide tests or CI status were inspected.

## Defensive changes after the campaign snapshot

The implementation author finished three defensive guards after the source
snapshot had already been captured. That intermediate integration file had SHA256
`9f5f791277166c01be07726c0268eb273d348f8e8a0abd8193e45a4a580a1572`.
Relative to the frozen `5620d3f...` version, it refuses a final cut right side
or actual lower side at SCIP's infinity sentinel, and catches an exception
while evaluating an optional heuristic exchange sample. No source model,
support theorem, exact rounding formula, or activation policy changed.

The frozen campaign remains unchanged. Its timings and solver outcomes apply
to the frozen version, not to a claim of identical execution of the later
live file. The independent [guard auditor](check_campaign_guards.py) checks
every recorded cut right side and actual row lower side against its recorded
SCIP infinity sentinel and lists worker errors separately. An affected row
would require an explicitly labeled corrected rerun; a missing worker log
cannot establish absence of an affected unrecorded row.

The first fresh-process snapshot replay passed 34 records and 31 cuts. The
separate initial guard audit passed 35 records and 31 cuts, with no worker
errors and a maximum absolute row-side/infinity ratio of `1e-20`. These are
pipeline checks, not the final campaign totals. Their saved results are
[campaign-partial-replay.json](campaign-partial-replay.json) and
[campaign-partial-guard-audit.json](campaign-partial-guard-audit.json).

## Failures found by the complete campaign and matched repair

The complete frozen campaign exposed a discovery robustness defect on the
large historical diagnostics `chp_partload` and `waterno2_06`. Constructing
every polynomial term over all original model variables exceeded SymPy's
recursion depth. Both cut modes failed on each model. Those four original
worker errors and unknown cut logs remain in the original records.

The correction constructs each polynomial over the variables actually
present in that term. Absent variables cannot change degree or coefficients.
Exact rational constants are handled directly; an unsupported transcendental
coefficient or a polynomial-construction recursion failure retains the whole
term in the nonlinear remainder. Thus the decomposition still sums to the
exact original expression. The independent replay needed the same sparse
generator correction for its separate parser. The checker frozen for the
repair campaign has SHA256
`83ab356a6c7e47f1a2ff064235452b0f4c9aa7eb92e9b125119554b0a166dbb4`.
At that point the replay suite passed six tests, including a 1,400-variable sparse
row, a large nonlinear product, and exact rational/transcendental remainders.

Discovery also ran past the existing separator allowance by performing
multiple symbolic operations without intervening time checks. The corrected
implementation checks that existing deadline between additive terms, source
rows, side admission, overlap grouping, selected-side scans, domain rows,
quadratic tests, and Hessian tests. An unfinished discovery throws away its
partial result, records `discovery_incomplete` and `budget_exhausted`, and
stops the experimental separator. It does not report zero eligible blocks
or a completed search. A single symbolic call is still nonpreemptive.
Independent controlled-clock execution confirmed that an unfinished
1,400-term decomposition exports no partial result. A real large-model probe
reported an explicit budget exit near one second.

The reviewed corrected integration has SHA256
`128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210`.
No support theorem, row-conversion formula, activation threshold, or budget
value changed. This version was separately frozen for a matched repair
supplement. The [independent selection](repair-selection.json) uses only a
recorded discovery overrun of the existing allowance or the identified
recursion error. It selects 25 model/phase/seed groups and all three modes
for each, giving 75 jobs. The original records' SHA256 is included. Objective
quality and corrected outcomes play no role in selection.

The supplement is a repair check on affected groups, not a replacement
prospective 30-model comparison. The two versions and their measurements
must remain separate.

## Complete original campaign replay

The following command ran in a fresh process against the verified original
campaign snapshot:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/replay.py research-20261003-convexification/experiments/campaign-v2 --output research-20261003-convexification/experiments/campaign-v2/replay.json
```

It passed all **123 recorded cuts**, bound **278 original-model records**,
and rejected all **14 tamper controls** across the 282 scheduled records.
The four failed workers have unknown cut logs and are listed separately;
they are not successful replayed model records. The
[saved replay](../experiments/campaign-v2/replay.json) verifies all 156
archived source and input hashes.

The independent final [guard audit](campaign-guard-audit.json) checks all
123 recorded right sides and actual row lower sides. All are below SCIP's
infinity sentinel; the largest absolute-side/sentinel ratio is `8.5e-19`.
None of the four saved worker errors comes from heuristic exchange-sample
evaluation. These checks establish that the earlier defensive guards do not
change any recorded primary cut; missing logs remain unknown.

The independent metric audit reports 271 checked incumbents with no failed
original-model residual checks and no reference-bound conflicts. All three
modes solved 25 of the 30 new holdout models. Those numerical results do not
extend the component-level certification claim.

## Complete matched repair and final checker

The final offline checker was run in a fresh process against each campaign's
own verified support, bound, model, and row-conversion snapshot. The primary
command above and the following matched-repair command both exited with code
zero:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/experiments/replay.py research-20261003-convexification/experiments/repair-discovery-v1 --output research-20261003-convexification/experiments/repair-discovery-v1/replay.json
```

The [repair replay](../experiments/repair-discovery-v1/replay.json) passed all
**42 recorded cuts**, bound all **75 model records**, verified **103 archived
source and input hashes**, and rejected all **14 tamper controls**. There were
no worker errors, hard timeouts, or unknown cut logs. The independent metric
audit also passed all **67 returned-incumbent checks**, with no reference-bound
conflict. The [repair guard audit](repair-guard-audit.json) passed all 42
recorded rows; its largest absolute-side/SCIP-infinity ratio was
`3.000000000000002e-20`.

The selected full-run holdout subset solved 4/8 models in every mode, and the
selected diagnostics solved 4/7 in every mode. No corrected cut-mode final
bound improved over its matched baseline. Six runs had small remaining
discovery overshoots, all explicitly marked incomplete; the largest excess
was 0.003618 seconds. This agrees with the stated nonpreemptive-operation
limitation. The completed supplement resolves the observed execution defects
without establishing a general benefit for enabling these cuts.

The final checker additionally handles tamper controls for a valid empty
infeasibility row, such as `0 >= 1`, without assuming a first nonzero column.
An independent fixture derives that row from `x^2 <= -1` and the valid support
`x^2 >= 0`; its submitted-row record is a constructed fixture, not a claim that
SCIP generated it. This change affects only the offline review harness.
Its targeted command was:

```sh
code/minlp_solver_lab/.venv/bin/python research-20261003-convexification/reviews/test_replay_review.py
```

All **seven tests** passed in 1.882 seconds. This later run is distinct from
the earlier six-test execution and the primary agent's 81-test/three-subtest
focused run; their overlapping counts are not added.

Both final campaign replay results name checker SHA256
`10115390a428ca2eb7131d5ebf4a094260170ebe3146e491ad73b85526c4c146`.
The exact checker bytes are archived as [replay-final.py](replay-final.py),
with both result hashes in
[replay-final-provenance.json](replay-final-provenance.json). They can be used
in place of `experiments/replay.py` in the commands above. This checker version
is separate from the originally frozen `b6e0fe49...` and repair-frozen
`83ab356a...` offline scripts; neither solver snapshot was changed.

No unresolved original-model, recorded-cut, or matched-repair correctness
blocker remains within the supported scope. Across the two distinct cohorts,
165 recorded cuts passed replay and 338 returned incumbents passed numerical
checks. The four original unknown cut logs remain unknown.

## Certification boundary

Replay shares reviewed exact support, bound, and source-domain primitives
with the implementation. Its independence concerns source reconstruction,
logical composition, and separate analytic tests, not an independently
implemented arithmetic kernel. Python, SymPy, Arb where used, and the checked
submitted PySCIPOpt expression interface remain trusted dependencies.

The certificates cover recorded original-model inequalities. They do not
certify SCIP's later presolve, numerical feasibility tests, branch-and-bound
search, or reported primal and dual bounds. Missing worker cut logs are
unknown, and cannot be counted as zero cuts or as certified runs.
