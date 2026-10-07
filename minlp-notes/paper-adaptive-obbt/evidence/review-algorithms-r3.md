# Final algorithms review, round 3

## Verdict and scope

No unresolved mathematical, numerical-contract, or callback-definition issue
remains in scope. Findings A1–A7 of `review-opus-foundations-r1.md` are closed.
This focused review supplements `review-evidence-r2.md`; it does not reopen the
previously accepted experiment transcription or effort proofs.

Reviewed the released algorithms section, the floating-point block moved to
the numerical-validation appendix, the changed callback wording in experiments,
and `author-revision-r2.md`. Snapshot: **2026-10-06 02:28:52 UTC**. The three
manuscript hashes were confirmed unchanged after inspection.

| Source | SHA-256 |
| --- | --- |
| `sections/algorithms.tex` | `dfbf09c38202404ea77a30b3d8cd5068e842758bf3cf7aa9b02dc20924c4d327` |
| `appendices/numerical-validation.tex` | `dc58fdd51989e1b9b61010890d56c7ef52c606d1caaa4435ee4d24e3afd9bc85` |
| `sections/experiments.tex` | `facfe5d03aab6102d1fbbb994634d5f32e9b18fb36f78fb7781d9606ef48d391` |
| `evidence/author-revision-r2.md` | `2034b769fc58e2360770cfe3a62f44ccacb263eb09ab460057a7b40785807684` |
| October `campaign-01/source/adaptive_obbt.py` | `c6547934e544cd8bb8bf14ab2d0aa67702adc855e9d62a80e2660851a98c5e24` |
| October `theory/certified_driver.py` | `ba8048fe8cd990064973aee8d6f588067c8d977209ddd5bd44a6a31b705ce8f6` |

The last two paths are relative to `research-20261003-adaptive-obbt/`, with
`campaign-01` under `experiments/runs/`.

## Findings closed

| Finding | Released treatment |
| --- | --- |
| A1: moving tangent points and retained pool | Algorithms lines 337–350 separate box-relative nonmonotonicity from later pool growth. The exact five-tangent counterexample is correct. Lines 520 onward state that future-round guarantees require a different contract and a cutoff above the certificate threshold. |
| A2: floating-point enclosure | Appendix lines 83–161 define the extended predecessor/successor operations, prove one-step enclosure, handle both overflow signs, and reject nonfinite third-pass products or final bounds. See the independent reasoning below. |
| A3: triggers | Algorithms lines 466–474 restrict the monotonicity rationale to a monotone family, explicitly qualify its use for this policy, and identify unprocessed directions and heuristic thresholds. |
| A4: row-correction premise | Appendix lines 33–38 distinguish lifts of every point in the box for product rows from lifts satisfying the particular original or cutoff row. |
| A5: empty LP and multiplier convention | Appendix lines 51–81 use `mu=+infinity` when infeasible. Weak duality and the eliminated-bound-multiplier maximization are correct. Clipping makes validity independent of the reported multiplier sign convention; an unsuitable multiplier weakens the bound. |
| A6: closure and finite budget | Algorithms lines 166–215 and 246–256 correctly distinguish fixed status, finite stopping, and reconstruction failure. The reference-family extension supports the stated containing-box scope; the witness threshold is no greater than the supplied cutoff. Exact rational proposals remove reconstruction failure, while Heron denominator growth remains. |
| A7: admission and counts | Algorithms lines 445–465 define an acting callback as passing admission and a trigger. Limits count these visits, including visits that then encounter an unsupported box. The changed experiment wording agrees. |

## Overflow, reverse steps, and underflow

The first two passes preserve their enclosures by applying the one-step lemma
to each operation on the currently stored endpoints. Lower accumulators and
predecessor terms cannot be positive infinity; upper accumulators and successor
terms cannot be negative infinity. In the lower residual update, the subtracted
successor is never negative infinity; in the upper update, the subtracted
predecessor is never positive infinity. Thus the operations avoid undefined
infinity cancellation.

An overflow followed by an operation in the opposite direction remains safe.
If a lower enclosure of an exact partial sum `S` becomes finite `Omega`, then
`Omega <= S`; adding any finite reverse term preserves this inequality, and
the next predecessor step preserves it again. A negative-infinite lower
enclosure stays a lower enclosure. The upper-bound argument is symmetric.
The proof therefore does not require rejecting every intermediate overflow.

For an accepted third pass, all four vertex products are finite. The minimum
rounded product is no greater than the rounded product of an exact minimizing
vertex. Monotonicity of `pred` and the one-step lemma then give a lower
enclosure of that vertex product. This argument does **not** assume monotonicity
of faithful `fl`. Accumulation and the residual interval give the displayed
safe dual-bound chain. These operations and rejection points match the frozen
`dual_box_bound` source.

Gradual underflow and disabled flush-to-zero/denormals-are-zero modes are
explicit premises in both the appendix and the main-section summary. They
cover subnormal arithmetic and every IEEE rounding direction. This is a
conditional numerical-validity argument; the review did not establish or
claim an archival record of those runtime modes. The separate incumbent
feasibility premise and absence of exact certification for the native solve
remain clear.

## Callback correspondence and verification

In the frozen source, `state.record` and `S["calls"] += 1` occur only after
`reason` returns a trigger; the event is appended before the unsupported-box
check. No-trigger visits contribute elapsed time but produce no event. Thus
the acting-callback limits, the 48 unsupported events per arm, and the 404/741
recorded-callback denominators are consistent. Experiments lines 314–315 now
describe the approximately 17 ms figure as a quotient per recorded callback,
with timed no-trigger visits included in its numerator; it is not a measured
duration of each callback.

Commands actually run were read-only `sed`, `rg`, `cat`, `date`, and
`sha256sum`, followed by writing this report with `apply_patch`. No experiment,
solver, numerical routine, archived analyzer, build, test, project-wide check,
CI inspection, or literature search was run. Original evidence and manuscript
files were not edited.
