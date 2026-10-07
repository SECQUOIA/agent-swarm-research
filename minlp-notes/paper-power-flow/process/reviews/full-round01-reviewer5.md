# Independent whole-manuscript review: reviewer 5

Verdict: **PASS subject to one minor boundary-case correction. No major issue found.**

I independently reviewed the complete frozen `full-round01` manuscript, including every theorem/proof, both appendices, introductory and concluding claims, references, reproducibility instructions, and coverage map. I did not read other full-round reports or edit manuscript inputs. All 22 snapshot hashes matched.

## Required correction

**Minor: preserve connectedness when the principal-window transfer receives the zero-variable source.** Location: `sections/04-structural.tex:196-199` (Lemma 5.3) and `:256-260` (Corollary 5.5), composed with `sections/03-ac.tex:315-340` (Corollary 4.9).

The zero-variable source has a singleton solution set in dimension zero. Lemma 5.3 maps it to one isolated pinned voltage-1, injection-0 bus; subdivision leaves that graph unchanged. The principal-window construction requires `n >= 2` and explicitly pads smaller networks with isolated buses. That padding produces a disconnected graph in this case, contrary to Corollary 5.5's instruction that the transfers change no graph and preserve all structural restrictions. Every construction starting with at least one arithmetic variable already has at least two buses after the connector step, so this is a trivial-input composition gap and does not undermine the hardness result.

A concise fix is to replace Lemma 5.3's zero-variable output by two pinned voltage-1, injection-0 buses joined by a unit-conductance edge. It still has a singleton feasible voltage set, uses the same finite alphabet, and satisfies every structural restriction. Subdivision then leaves at least two buses, and the principal transfer needs no isolated padding. Alternatively, handle this source explicitly in Corollary 5.5 using that two-bus network with `c_2 = 3/4`. I independently checked its zero active/reactive injections and cosine inequality. No new general theorem is needed.

## Mathematical assessment

The ordinary reduction correctly handles repeated variable names through distinct occurrences, unused variables, all inversion endpoint ranges, redundant free-injection intervals, size bounds, and unique rational extension. The generalized planar construction preserves transmitted bounds; local sum variables do not propagate through further crossovers. The disk-and-corridor argument and occurrence allocation support the claimed degree and planarity, including repeated ports. Connection and harmonic subdivision preserve the whole solution set. The sole composition omission is the trivial case identified above.

The AC proof consistently distinguishes real lifts from principal line angles. I checked the determinant signs, axis crossings, negative cosine limits, antipodal exclusion, fundamental-cycle sufficiency, and purely resistive energy identity. The one-sided reactive intervals, rectangular reference convention, winding examples, and shrinking positive windows have the stated scope. There is no inference from arbitrary principal-angle reactive balance to equal phases.

The self-contained arithmetic proof provides both directions and unique auxiliary values. Its small-signal scaling, shifted addition/product gates, reciprocal square identity, dyadic constants, and finite-type continuity argument give the required ranges without a circular dependence on the circuit size. Compact denominator bounds prove the basic-closed converse; the three-quadrant obstruction is valid. The finite-simplex nonface construction supports topological universality only, as claimed. Empty feasible sets and singleton algebraic sources are covered; the designated scalar-affine coordinate preserves the claimed number field. The manuscript does not import the false general Boolean rational-universality assertion from the earlier source.

The pointwise residual bounds, explicit tiny infeasible recurrence (including `k = 0`), compact epigraph application of the polynomial-minimum theorem, promise-certificate mesh, and reactive stability constants are consistent. Exact box membership is retained when residuals are relaxed. The separation comparison concerns the required residual accuracy, not an algorithm lower bound. The stability result correctly treats disconnected components and isolated buses separately. All eight legacy examples have the stated analytic outcomes.

I checked the primary dependency statements against the available primary texts and prior retrieved originals, including the exact ETR-INV formulation, the crossover restrictions, the polynomial-minimum hypotheses and scale, and the triangulation scope. The literature comparison keeps distinct models and preprint/journal numbering separate. Abstract and conclusion accurately summarize the proved results, including the qualification over the rationals and the absence of fixed finite cosine data for the shrinking-window model.

## Reproduction, coverage, and presentation

All four frozen exact suites passed independently with the documented counts. A fresh LaTeX/BibTeX build produced 28 pages without warnings, unresolved references, or overfull/underfull boxes. I inspected rendered pages covering the abstract, construction exposition, transfer/structural transition, arithmetic proof, verification appendix, and references; no layout defect required correction.

A fresh repository search found 18 relevant or incidentally matching result/note/code files. Every corresponding file was byte-identical in the other worktree. The coverage map accounts for the actual exact power-flow developments; the additional incidental matches concern different potential-flow or chance-constrained models and introduce no omitted theorem for this paper. Historical numerical evidence is accurately separated from exact proofs.

Artifacts are in `/workspace/minlp-notes/paper-power-flow/verification/reviewer5/full-round01/`, including the manifest receipt, four check logs, clean build and PDF, rendered pages, `worktree-coverage.json`, and `empty-source-composition.log`.

After the minor correction above, I consider the manuscript mathematically coherent, sufficiently explained for its intended research readership, and complete within its stated scope. I found no significant missing development that should delay completion. No optional improvement is being presented as a required correction.
