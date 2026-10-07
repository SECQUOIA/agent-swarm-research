# Changes after the campaign source freeze

The campaign began on 2026-10-03 at 04:29:09 UTC immediately after the
independent semantic and replay clearance. Its complete source snapshot is
retained in `campaign-v2/snapshot`, with hashes in
`campaign-v2/source-manifest.json`. Workers load that snapshot throughout the
campaign; concurrent live-file changes cannot affect later workers.

The frozen `solver/integration.py` begins with SHA256 `5620d3f`. The integration
owner subsequently completed three defensive changes in an intermediate file
with SHA256 `9f5f791277166c01be07726c0268eb273d348f8e8a0abd8193e45a4a580a1572`:

- Reject a converted cut right-hand side whose absolute value reaches SCIP's
  infinity threshold.
- Reject an actual inserted row left-hand side at that threshold.
- Catch arithmetic or value failures while evaluating a support minimizer for
  the optional sample exchange. A support certificate already obtained is not
  affected by this heuristic evaluation failure.

No model, activation policy, candidate coefficient, work limit or default
parameter changed. The reviewer instructed the campaign to continue with its
unaltered frozen implementation. The reviewer will inspect every recorded cut
against the infinity guard and all worker errors for the exchange failure
path. Until that audit is complete, no assertion is made that the changes are
inactive on the recorded cases. Results are measurements of the frozen
implementation, not a separate performance evaluation of the later live file.

All raw records remain. Any correctness-driven repeat must be documented
separately and must preserve the original result; no unfavorable result is
silently replaced.

The original campaign then exposed a separate correctness defect in the
prespecified large diagnostics `chp_partload` and `waterno2_06`: affine splitting
passed every source variable to SymPy's dense polynomial constructor. These
models have more than one thousand variables, so even sparse terms exceeded
the constructor's recursion depth. Both cut modes returned worker errors on
both models. Their absent cut logs retain unknown counts.

The owner repaired polynomial construction to use only the symbols appearing
in each term, with a matching independent replay fix and a regression using
1,400 source symbols. Exercising the repaired discovery on the actual models
also exposed a rational-domain conversion exception for a term with an exact
nonrational coefficient; such a term is now retained as nonlinear, as required
by the original split contract. The sparse-expression repair was then extended with the deadline checks below.
The subsequent budget audit also found discovery continuing past its existing
time allowance. The owner added deadline checks between discovery rows and
groups, retaining the same configured budget and policy. The supplement
therefore includes every original model/phase/seed group meeting the frozen
budget-violation or recursion-error criterion: 25 groups and 75 matched jobs.
See `repair-protocol.md` and `repair-plan.json`. It starts after all 282 original
jobs finish and after the repair passes model and replay review. It freezes
its own sources and retains all four original failures in the primary campaign.
`run_repair.py` implements that fixed plan; its output includes the explicit
amendment and source hashes.

The supplement froze the final reviewed integration
`128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210`
and independent replay
`83ab356a6c7e47f1a2ff064235452b0f4c9aa7eb92e9b125119554b0a166dbb4`.
The complete hashes and copied files are in
`repair-discovery-v1/source-manifest.json` and its `snapshot` directory.

The original replay passed all 123 recorded cuts while retaining four unknown
worker logs. The corrected replay passed all 42 recorded cuts with no unknown
logs. All recorded actual row left-hand sides also passed the SCIP-infinity
guard audit. These results certify the saved rows and their model bindings;
they do not establish performance equivalence between source versions.

The final offline checker used for both completed replays is archived as
`../reviews/replay-final.py`, SHA256
`10115390a428ca2eb7131d5ebf4a094260170ebe3146e491ad73b85526c4c146`.
Its provenance file records both result hashes. This later independent
checker is distinct from the checker copied into each measured source
snapshot; the frozen solver implementations were not changed.
