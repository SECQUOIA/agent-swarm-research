# Independent review of numerical claims in the document

Reviewed the primary and historical numerical claims in `document/evidence.tex`
and this topic's `README.md`, `PROGRAM.md`, `CLOSEOUT.md`, and `VERIFICATION.md`.
The completed matched repair results were checked in a final pass against the
independent repair audit and raw records. This is an internal consistency
review, not a new experiment.

No numerical discrepancy was found. The review checked:

- Historical counts against the retained first-campaign records, summary and
  replay: 316 records; 24 selected and 20 admitted application models; 19 solves
  for baseline/control and 18 for cut modes; 1,073 versus 323 candidate LPs;
  5.59 versus 3.05 callback seconds; synthetic solves 12 versus 13; 1,082 replayed
  cuts, 270 checked incumbents, and eight unknown model/cut logs.
- Primary protocol and population counts against the independently reconstructed
  selection and schedule: 422 eligible models in strata 85/208/129, 30 selected,
  282 jobs in phases 90/30/39/105/18, and the stated time limits and tolerances.
- Completion and numerical outcomes against archived primary records: 1,338.6
  seconds outer campaign time; status counts 106 optimal, 74 gap limit, 31 time
  limit, 67 node limit, and four errors; 25 of 30 solves in every mode; cut totals
  0/38/10 across 0/7/3 cases; integration totals 170.57/187.02/187.12 seconds.
- Work and coverage against the independent coverage audit: candidate LPs
  186/66, support calls 138/51, callback times 27.63/27.00, discovery times
  24.41/24.63, 28 callback/discovery runs, 12 discoveries without supported
  blocks, 156 possibly overlapping blocks, 63 auto-eligible blocks, and 186
  declined source sides.
- Paired comparisons against the independent primary metric audit, including
  full, root-only, and six seed-one repeat cases. Additional inspection verifies
  the same 25 solved model identities in all modes. The same five unsolved
  models received no added cuts; each cut mode has zero better, one tied, and
  four worse bounds there. The two improved full-run bounds occur on models
  already solved by baseline. The `graphpart_clique-40` example has final
  bounds 438 versus 392 as reported.
- The constructed root mechanism against its raw records: both cut modes add
  two cuts on `simplex_quadratic_vector` and report an optimal bound
  `-0.5000000199754353`; baseline reports a node-limit bound
  `-0.5002737396971283`. The report correctly labels these numerical values
  and distinguishes the exact optimum `-1/2` from approximate solver output.
- Original-model and certificate coverage against the separate audits:
  123 recorded/replayed cuts, 156 archived hashes, 278 complete model records,
  271 numerical incumbent checks, 14 rejected tampering controls, and four
  unknown cut logs. The document correctly distinguishes the diagnostic
  execution errors from importer rejection.
- Seven historical model admissions against `numerics/model-admission.json`;
  40 independent polytope diagnostics and 21 separation tests against their
  component review records. The 250-test/eight-subtest and focused
  81-test/three-subtest counts are the primary agent's documented executions;
  this review did not repeat or add their overlapping test counts.
- The matched repair section against the independent 75-record audit and final
  replay: groups 8/7/9/1, solved counts per mode 4/4/0/1, all-cut totals
  12/10/11/3, auto-cut totals 3/0/3/0, 42 recorded and replayed cuts, 67 checked
  incumbents, 103 archived hashes, no unknown logs, and 14 rejected tampering
  controls. Solved model identities coincide between modes within each group.
  Full selected holdout integration totals round to 123.91/124.86/124.82
  seconds. The only worse diagnostic bound is on `waterno2_06` in both cut
  modes. Root and repeat comparisons all tie. Combined counts 165 cuts and
  338 incumbent checks preserve the four original unknown logs separately.
- Repair soft-budget diagnostics against raw measurements: six discovery
  overruns all mark incomplete discovery; the maximum discovery excess is
  3.617737 milliseconds and the maximum callback excess is 29.529274
  milliseconds. The maximum total-budget excess is 23.611235 milliseconds.
  These remain observed soft-budget excesses, not hard timing guarantees.

The recommendation to retain native baseline is consistent with the evidence:
equal application solved sets, unfavorable timing, and no improved bounds on
the common unsolved cases do not establish a benefit for default activation.
The document preserves the original frozen outcomes and treats the selected
repair cohort separately; it does not substitute corrected measurements into
the prospective table or claim that missing logs represent zero cuts.

One wording issue was sent to the owners and resolved: `PROGRAM.md` attributed earlier
losses to graph-auxiliary reformulation as an established cause. The historical
application control solves 19 models, like baseline, while both cut modes solve
18. These counts do not isolate that causal explanation. The recommended
wording simply identifies the earlier use of duplicate graph auxiliaries.
The owner changed this to "used in the earlier approach," which was verified
in the current file. No primary numerical-claim discrepancy remains open.

A final rounding correction was sent to the report owner and resolved: the maximum total
soft-budget excess rounds to 23.611 milliseconds at three decimals. Reporting
23.612 milliseconds is valid only as an explicitly upward-rounded upper bound.
The current `document/evidence.tex` reports 23.611 milliseconds. No numerical
claim or primary-versus-repair boundary issue remains open in the reviewed
document or root completion files.

The review used read-only archive extraction and the existing independent
audits. It ran no optimizer, new benchmark, project-wide tests, or CI checks.
