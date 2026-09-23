# Stage 6 — root independent reading and verification plan

Stage 5 is accepted; author implementation and computational work has begun.
The baseline requirements are in `process/computational-baseline-plan.md`.

## Independently checked baseline algebra

At a fixed query with two positive weights lambda and 1-lambda, disaggregation
can be written f and x-f on ANY bounded equality-flow network. First check the
original aggregate domain. Then Af=lambda*b and
max(0,x-(1-lambda)u)<=f<=min(x,lambda*u) are exactly the two states' balances
and capacities. An observation in the second state fixes f_e=x_e-z_e; a first
state observation fixes f_e=z_e. Multiple fixed values must agree and must stay
within the intersected bounds. Observations on zero-weight states must be zero.
A single positive state is checked directly. This is an elementary specialization
of the known hull, not a new convexification theorem. Numerical LP solutions
remain numerical evidence unless independently verified with rational witnesses.

For a globally merged optimization EF, let J be all labels appearing in any
observation. The retained weights are y_j for j in J and 1-sum_{j in J}y_j.
Every original y coordinate and its objective/fixed value remain in the model.
The x objective is copied onto every retained state flow; each z objective is
placed on its own retained observed flow. The homothetic merger proves exactness.
This baseline uses no graph block, path, cycle, or observation-rank elimination.

## Required code review boundaries

- The eliminated profile does not have sum(w_explicit)=t when the residual
  branch carries positive flow. Old anchored-total inverse bases cannot be
  reused without changing the mathematical problem. Interior-residual tests
  specifically exercise this distinction.
- Only observed labels should determine the exponential library dimension.
  Unused original weights and original simplex constraints remain relevant.
- Compact decomposition must retain one normalized merged default and recover
  unused labels proportionally; zero merged weight cannot be divided by.
- Both exceptional a=3 cuts must be exercised by the exact paper examples,
  with exact global validity and preserved violation after the balance repair.
- Baseline status failures are not infeasibility certificates. A floating-point
  state weight must not be discarded merely for being small and positive.
- Preserve exact-vs-numerical status distinctions and the general compressed
  implementation's failed-certificate states. Model matrix bytes are not peak
  memory and source-level row counts are not post-presolve sizes.

No implementation or runtime conclusion is accepted at this point.

## First implementation reading

Read the initial upgraded flat_chain.py in full. The active-label category map,
merged state expression, grouped recovery, lazy dense compatibility properties,
a=0 direct path, a=1/2 interval recovery, and unanchored inverse-basis recovery
are correct. The code emits the negative Farkas expression, so the bypass repair
sign is correspondingly reversed; selecting a first-arc coefficient equal to
half the bypass coefficient and subtracting that multiple of the gadget balance
repairs both signs correctly. No correctness defect identified in this draft.

Sent two implementation qualifications to the author: tuple normal construction
and hashing carries an extra dimension factor versus preindexed-mask theorem
costs; historical _profile_bases checks do not validate new _reduced_bases.

## Optimization structure checked independently

For fixed y and no coupling rows beyond the component hull, the objective is a
sum of independent state-network objectives. A per-state network-LP baseline is
therefore relevant. A budget on aggregate x breaks that separation; comparing
formulations after appending the same row measures H intersect that budget,
not a claim that convexification commutes with intersection. The root requested
one bounded illustration and an explicit scope statement.

The disjoint-label ablation has no globally absent state label. Its three
observed arcs in each six-arc theta block meet at least two distinct paths,
so every label has full observation rank two and the observed-eliminated model
should have no remaining state-cycle auxiliaries. This predicts a concrete
model-size check, not a runtime outcome.

## Strong baseline and experiment source reading

Read strong_baselines.py, test_strong_baselines.py, paper_stage06.py, and the
updated flat-chain tests in full. The globally merged EF retains all y columns,
including their objectives and coupled-row coefficients; the state-flow objective
and added aggregate rows map correctly. Exact zero detection and two-state
observation-bound intersection are sound. Numerical aggregate balance checks are
explicitly tolerance based, and solver failures raise instead of becoming
infeasibility claims. The fixed-y independent network baseline is restricted to
uncoupled objectives. The budget benchmark measures H intersect the budget.

The new test suite has 21 passing tests, including both three-label cut repairs,
unanchored recovery with positive residual profile, compact unobserved-label
merging, the four-label obstruction, arbitrary graph baseline agreement, and
nonzero original-y objectives. Existing independent path-hull and compressed
checks also pass. These are author-run logs inspected by the root; the upcoming
five reviews provide independent implementation validation.

Root added an independent cross-formulation check of the general extra-row
mapper: 30 random graph instances, free simplex coordinates, and three coupled
rows with nonzero x/y/z coefficients. All 60 full/globally-merged numerical
objective and row-feasibility comparisons agree with the independently assembled
observed-eliminated formulation. Evidence: verification/stage06-root/
check_coupled_rows.py and its log. This is numerical agreement, not an exact
optimality certificate.

## Manuscript reading

Read the complete initial sections/08-computation.tex and all five generated
table sources. Their central interpretation matches the recorded controls:
global merging explains much of the original sparse-case advantage, local
compression remains useful when all labels are globally present, observed
elimination can cost more to build, and the older long-boundary-chain speedup
disappears against elementary baseline improvements. Fixed-y objective-only
optimization is explicitly separable; the budget adds a coupling row only to
the exact component relaxation. The two-supplier network has the stated
parallel-path topology despite opposite path traversal directions.

Sent two pre-freeze local prose/TeX fixes to the author: literal ell instead of
\ell in transportation indices, and one-flow rather than two-flow substitution.
No substantive issue found in this initial reading. The 44-page build log is
clean. Final section and source hashes will be frozen before independent review.

## Frozen stage checks

After author completion and the stage06-round01 snapshot, independently verified
all 82 dependency hashes in stage06-validation.json; there are no mismatches.
The source/data freeze is intact. Rendered computational PDF pages39 and41
were visually inspected during final author cleanup: text, equations, and tables
were legible without clipping. An attempted later render coincided with the
author's PDF rebuild and saw an incomplete file; this is a concurrent-output
read, not a manuscript defect. Independent reviewers build private copies.

Root also re-read accepted sections01–07 in full across the current manuscript
preparation and prior stage checks. The compression, coordinate-section, support
geometry, and sharp fixed-label arguments remain coherent with the new code
scope. Full-manuscript coherence review still follows Stage7.

## Round1 major finding and corrected baseline reading

Root accepted reviewer5's missing fixed-y joint LP control as major after
reading its independent implementation. The separate correction agent's new
fixed-y branch was read in full: it uses only positive grouped state flows,
native scaled capacities, block balance rows, the fixed-y objective constant,
and correct substitution of arbitrary original x/y/z rows. Original-point
reconstruction restores zero observed states and every fixed y coordinate.
No algebraic defect was found. The official three-case rerun uses the archived
objective vectors, weights and exact budget rows; all optima agree and all
membership/cold data remain unchanged. Updated size and timing interpretation
correctly reports the stronger global baseline's advantage on the sparse and
budget cases and the retained local advantage on the all-labels control.

Read the strengthened grid guard and its13 private mutation outcomes; actual
data pass and all deliberate omissions, duplications, order/method/summary
corruptions fail. The shell probe extracted the PDF command and confirmed
correct continuation without rerunning the experiment. Sorting and inverse-
basis wording fixes are present. These root checks supplement, and do not
replace, the required second five-reviewer round.
