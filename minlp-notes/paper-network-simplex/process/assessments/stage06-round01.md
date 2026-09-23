# Stage 6, round 1 — root adjudication

Read all five independent reports in full. Four reviewers found no major issue;
reviewer5 found a major omitted experimental control. The root accepts that
finding and four distinct minor issues. All must be corrected by a separate
agent before another complete five-reviewer round. Stage6 remains open.

## Accepted major

**R5-S06-01:** the optimization workloads fix all simplex weights, but the
full/global joint LP baselines still build variable-weight capacity rows and
retain fixed y columns. A direct fixed-weight disaggregation uses only positive
state flows, balances Af=lambda b, and native bounds 0<=f<=lambda u. All original
y objective terms become a constant, and their terms in additional rows move
to the right side. This is valid with an aggregate budget and avoids the many
solver calls of the independent-state comparator. Reviewer5's diagnostic
measurements materially change the original sparse-case comparison. The
baseline is mathematically correct as written, but insufficiently strengthened
for the practical interpretation. Official repeated measurements, model counts,
tables and discussion must be updated; do not substitute reviewer timings.

Preserve the current measured sources/data before changing them. Retain the
free-weight API and all original-coordinate objective/row semantics. Prefer a
direct fixed-weight branch of the existing full/global builder over another
duplicated public abstraction. Test exact zero weights, nonzero y objectives,
coupled x/y/z rows and reconstruction against independent vertex formulations.
Rerun the three official optimization cases with the unchanged five-run rotated
protocol, recording which membership data remain unchanged. The entire grid
may be rerun if simpler, but no expanded instance study is requested.

## Accepted minors

1. **S06R01-R1-F01, R2-S6-01, S06-R1-R3-01, R4-S06-01:** the LaTeX verbatim
   benchmark command has two literal continuation backslashes. Use one and
   verify the command extracted from the PDF/shell parsing.
2. **R2-S6-02:** qualify the implemented linear-in-L claim by the constructor's
   O(|O| log |O|) observation sorting. The mathematical grouped-input bound is
   unchanged, and the API documentation already discloses this overhead.
3. **S06R01-R1-F02:** distinguish sixteen-circuit separation at three labels
   from inverse-basis recovery, which begins at three, not above three. Update
   corresponding author-record prose without rewriting the historical record
   silently; explain the correction in the correction record.
4. **S06-R1-R3-02, R5-S06-02:** strengthen table validation to check unique flat
   grid keys, membership label counts, intended optimization names/order, and
   expected method coverage. The actual existing data are complete; only the
   claimed automated guard is too weak. Add meaningful private-mutation
   checks rejecting duplicate/missing cases and missing methods.

## Evidence and disposition

All five independently confirm the changed exact oracle and its sharp
three-label repairs, compact defaults, and residual-profile basis treatment.
All82 recorded hashes, all483 timing summaries and current complete case grid
match. Independent vertex-hull comparisons and exact witnesses/cuts passed.
Reviewer3 independently reproduced the full grid once, including all103
method/case sizes, statuses, objective values, cuts and the budget. None of that
removes the valid missing-control criticism. Numerical agreement is not an
exact optimality claim. The scientific baseline revision is major even though
the existing theorem proofs are unaffected.

After corrections, freeze Stage6 round2 and dispatch all five reviewers again.
Do not begin Stage7 before that round finds no major issue and all accepted
minor findings are resolved.
