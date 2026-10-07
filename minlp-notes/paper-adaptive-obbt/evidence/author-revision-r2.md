# Author revision, round 2: foundations, algorithms, and front matter

Lane: final Opus revision of the owned files below. This report records the
disposition of every finding in scope, the notes left for the root, and the
checks actually run. Ownership of all six files is released with this report.

## Files revised

Only these files were edited. No other lane's file, `main.tex`, or the
bibliography was changed.

| File | SHA-256 at release | Lines |
| --- | --- | --- |
| `abstract.tex` | `f75cb5164d64ebc45ae450352fab170a68e99c1199589cc9f369ca02ea4fea4d` | 26 |
| `sections/introduction.tex` | `e8ec10762d7a60e00877773204212f8ee8c5d2adf83f5b0464fac22511ec13d4` | 201 |
| `sections/related.tex` | `3ca85ac3dc8a001ce22b97511f490b82330ece6a3c297cc78c9428afc4dde7ed` | 129 |
| `sections/foundations.tex` | `f30184c925375bf1f37300ce465057216656d36aadfdb9bed0c5476d009bb10d` | 457 |
| `sections/algorithms.tex` | `6602c5c06bac913f3fcda24de91c7a017d3363cb1c759dd5c117b9cab85dec18` | 691 |
| `sections/discussion.tex` | `cb886311c5814ac3f8210f4a0f888a33df81015aaa7a7227ffbe5be99e392cda` | 145 |

The starting snapshots were the ones reviewed in
`review-opus-foundations-r1.md` and `review-integration-r1.md`
(foundations `825ccbd5…`, algorithms `8980d76a…`, abstract `bebd515e…`,
introduction `212a9cf8…`, related `8fd759b1…`, discussion `5da4f472…`).
No other writer changed these files during the revision.

New label: `lem:greatest-fixed` (foundations). No label was removed or
renamed; `prop:sidecar-validity` keeps its label although the word
"sidecar" no longer appears in the text.

## Dispositions: Opus foundations and algorithms review

| Finding | Disposition |
| --- | --- |
| F1 (material): box-determined construction can be nonmonotone | Fixed. Foundations now states that monotonicity can fail even for a construction determined by the box, with the exact five-tangent counterexample: `phi_[-1,1](0)=0 > -1/64 = phi_[-1/2,1](0)`, and at `U=1/4`, `T_U([-1,1])=[-1/2,1/2]` but `T_U([-1/2,1])=[-1/2,41/80]`, witnessed by `(41/80,1/4)`. It names these as the policy's square rows without the pool, notes that endpoint tangents alone (family (b)) are monotone, and keeps the history-dependent and inexact cases. |
| A1 (material): why future-round results do not apply to the policy | Fixed in the local-relaxation paragraph: two separate reasons, box-relative tangent points (with the counterexample, no history needed) and the shared pool, which restores earlier tangents only while it has room and whose later tangents can cut lifted points checked earlier. The pool rule is stated as in the source (`retained_tangents_per_square=25`; the five current points are offered at each callback while the set has fewer than 25 points). "What the policy uses from the theory" now says the relaxations are not monotone and that protected boxes cover only cutoffs at least their threshold. The minor third mechanism (outward rounding) is omitted, as the reviewer allowed. |
| A1 (definite LP count) | Adopted after a targeted recount: every model of the prospective cohort has 10 to 144 variables in product terms, so a complete round needs at least 20 LPs, more than the 12 per root callback, unless earlier bounds fixed variables. |
| A2 (material for validity proof) | Fixed. `pred`/`succ` are defined on the extended binary64 set as nextDown/nextUp, with `pred(+inf)=Omega`, `succ(-inf)=-Omega`. Lemma `lem:enclosure` now assumes faithful rounding and holds for every exact result, including infinities; its proof no longer uses round-to-nearest. Text states that every IEEE direction is faithful with gradual underflow, including overflow, that flush-to-zero and denormals-are-zero must be disabled, and that an active directed rounding mode is covered. The overflow paragraph proves that no `inf-inf` can arise in the first two steps (lower bounds and `pred` terms are never `+inf`; `succ` terms and upper bounds are never `-inf`), that infinite intermediates stay valid, and that the third step rejects nonfinite products and results. The final chain no longer uses monotonicity of `pred∘fl` (faithful rounding need not be monotone); it uses the exact minimizing vertex and monotonicity of `pred`. The text states that nonfinite multipliers are rejected, and that the first two enclosures are accumulated in one sweep, matching `dual_box_bound`. The arithmetic assumption is now "IEEE binary64 arithmetic with gradual underflow". |
| A3: trigger rationale | Fixed: for a monotone family a smaller box or cutoff shrinks the cutoff sets and can move supports; the policy's own relaxation is not monotone, so this motivates but does not justify the triggers; unprocessed directions at an unchanged node are not revisited; thresholds are heuristic. |
| A4: set `S` in the row correction | Fixed: product rows use the exact lifts of all points of `B`; original rows and the cutoff row use the exact lifts of the points of `B` that satisfy that row. |
| A5: dual bound conventions | Fixed: `mu=+inf` for an infeasible LP (proof notes the trivial case); validity is independent of multiplier accuracy and of the solver's sign convention, since the bound holds for every `y<=0`. |
| A6: closure discussion | Fixed: "states what the stopping certificate guarantees"; "valid bounds" (line 5); every run stops because `K` is finite but no finite budget guarantees *fixed*; an exact LP solver removes reconstruction failures but not iterate growth (Heron digits 1, 1, 2, 4, 8). Theorem `thm:closure`(b) now covers boxes outside `B_0` (the reference family is defined on every box) and uses cutoffs at least `U_W-hat = max_{z in W-hat} v(z) <= U`, the form useful under decreasing incumbents. |
| A7: admission versus counts | Fixed in algorithms: *admission* is the untimed cheap check; an *acting callback* passes admission and a trigger; the table row and the trigger paragraph use "acting callbacks". See root note 2 for `experiments.tex`. |
| A8: attribution in algorithms | Attribution sentences added without citation keys, per instruction; see root note 1. The existing key `gleixner2017-three-enhancements-for-optimization-based` is now cited for SCIP's LP-based OBBT. The row correction is presented as an elementary proposition; no unverified source is attributed. |
| F2 (development): greatest fixed box without closedness | Implemented as Lemma `lem:greatest-fixed`, proved from monotonicity alone (hull of any nonempty family of fixed boxes is fixed). `P_U` is the hull of all fixed boxes in `B_0`, with `P_U=∅` if there is none, as requested by the focused Sol recheck. The lemma states that every Jacobi iterate contains `P_U` and `H_U ⊆ P_U`. A short remark identifies it as the elementary case of Tarski's theorem (existing key `tarski1955fixpoint`), cross-references `prop:join` as the finite-certificate form instead of repeating its proof, and claims no fixed-point novelty. |
| F2 consequences | `prop:fixed-limit` now concludes `B_∞=P_U` under closedness. Example `ex:not-fixed` states `P_U=H_U={0}` (only fixed box) and that continuing from `B_∞` gives `[0,1/8],[0,1/32],…`, reaching `P_U` only as a second limit. Item (ii) and the chain `H_U ∪ P ⊆ P_U ⊆ B_∞ ⊆ B_k` replace the two separate inclusions; the example notes `P_U=B_∞=[-1,1]`; the summary notes that both are empty if an iterate is empty. |
| F3: vacuous clause | Removed (`T_U(B_∞) ⊆ B_∞`), replaced by the containment of `P_U`. |
| F4: closedness paragraph | Added the joint lower-semicontinuity sufficient condition with its proof, the joint continuity of family (a), the sentence that `(closed-family)` is downward continuity `T_U(∩C_k)=∩T_U(C_k)`, and the independence statement: the five-tangent family is closed but not monotone; `ex:not-fixed` is monotone but not closed. |
| F5: persistence cutoff | Fixed: "at cutoffs at least `U`", with a pointer that Section 5 lowers this to the largest relaxation value of the points. |
| F6 wording | Fixed: "three limits on further tightening"; "all boxes in `R^n`"; "only a better incumbent or branching shrinks". The optional generalization to closed `R(B)` with compact lifted sublevel sets was not adopted: no paper family needs it, and other sections state compact `R(B)` as their premise. |
| F7: proof of `lem:sequential`(c) | Replaced by the explicit cofinal-subsequence argument (`t_j >= j`, both sequences subsequences of the nested Jacobi iterates, nesting of `C_m`). |
| F8: attributions | Source checks belong to the literature lead. To avoid an implicit priority contrast, "observed … for cyclic sweeps, in a form that covers arbitrary fair schedules" became "studied by Caprara and Locatelli, stated here for every fair schedule … and for Jacobi rounds"; related work now says "restate their order arguments for Jacobi, sequential, and selective schedules". CLM credit for complete stalls is retained, as confirmed by the root. |
| Empty-box convention (focused Sol recheck) | Added beside `eq:operator`: `K_U(∅)=T_U(∅)=∅`. |
| Round-check alignment (certificates r2) | Step 2(d) now checks the `2n` complete lifted points, with every auxiliary coordinate, on `R_U(B')`, and returns the lifted pool `W-hat`. The text and the proof of `thm:closure`(b) apply `prop:round-check`(a) to these optima, which lie in `R_U(B)` and whose projections attain all endpoints; part (c) cites `prop:round-check`(b). Theorem (b) also states that the returned box is the greatest fixed box and the Jacobi limit (proof via `lem:greatest-fixed`). |

## Dispositions: full Opus review, owned scope

| Finding | Disposition |
| --- | --- |
| M2.1 contribution sentence | Replaced by "a prospective evaluation of an adaptive scheduling policy that uses only current-round screening and heuristic triggers, not the all-future certificates". |
| M2.2 evidence sentence | Now: the experiments show that the LP count is not a cost measure, and Section 10 shows why a width or remaining-tightening bound cannot by itself bound search time. |
| M3 structure | Not done here (root decision). The algorithms section remains the authoritative statement of what the policy implements; front matter keeps one statement each. See root note 4 for the floating-point appendix move. |
| M3.2 wrong cross-reference | Discussion now cites `prop:history` for identical histories. The same issue in `local-rates.tex` is root note 3. |
| m3 Starting paragraph | Fixed: a round cannot move endpoints of a fixed box, though its dual solutions can be useful (Gleixner et al.); in a strictly containing box the certificate bounds movement but proves no stall; symmetric minimizers only prevent collapse, tightening outside the hull can continue; results that guarantee movement (box threshold, stored dual bound below the endpoint, contraction conditions) are named, and none guarantees a shorter search. History result now cited as `ex:history` (moved to Appendix C by the root). |
| m4 "scales like" | Fixed: widths at most of order `sqrt(eps)` and gaps at most of order `eps`, attained in the two-variable model. |
| m5 `eps=0` certificate | Added to introduction and discussion: an optimal incumbent in the current box gives a protected singleton (`cor:original-points`), exact if the iterates converge to it (`ex:sharp-halving`); residual certificates otherwise. Discussion also cites `ex:critical-scalar` for non-exhaustive regimes. The local-rates passage is root note 3. |
| m7 threshold ambiguity | Fixed in introduction and discussion: the pool's face threshold marks expiry of the stored proof; the box can stay fixed down to `tau(P)`, about one round to compute. |
| m8 abstract stall sentence | Fixed ("Points of negative tangent-model value on every face of a box shape certify stalling at every sufficiently small scale"). |
| m12 precursor wording | Fixed: largest mean reductions in groups whose mean control time was a few seconds. |
| m14 "sidecar" | The root had already replaced it in effort and experiments; algorithms now uses "propagator time", "propagator time allowance", and "the propagator's timer". Only the invisible label remains. |

## Dispositions: Sol integration review and root precision items

| Item | Disposition |
| --- | --- |
| Integration 1 | "A round cannot move the endpoints"; protection versus fixedness of a containing box; minimizers prevent collapse only. |
| Integration 2 | Upper-bound wording; pool expiry versus fixedness in introduction and discussion. |
| Integration 3 | Discussion scope now restricts monotonicity to iteration, rate, and future-round results, names box-relative tangents and cut pools, and exempts current-round ceilings, validated dual bounds, and fixed-LP results. Observed histories: small changes certify nothing beyond nesting; an exact complete round with no change proves fixedness. |
| Integration 4 | Reuse "may be needed" only if discovery costs about a round; cheap certificates (exactly feasible incumbent singleton, optima of a completed exact round) named; the measured policy used neither kind. |
| `lambda in (r*,1)` | Introduction: for every `lambda in (r*,1)`, iterates from a sufficiently small box contract by `lambda` per round in a suitable gauge. |
| Two-variable rate domain | `0<|a|<2` added. |
| Stall cutoff | "every sufficiently small scale and every cutoff `U>=f*`" in introduction and discussion; foundations summary also says "sufficiently small". |
| Cluster threshold | Introduction and related: strict contraction condition with the same numerical threshold as nonstrict no-clustering conditions; related also says the scalar condition can fail although the iterates contract geometrically. |
| SCIP wording | "The SCIP implementation examined here". |
| Abstract length | 248 words (`wc -w` without the environment lines), down from 293. It keeps strict `r*<1` before the rate and floor claims, sufficiently small scales, `C^2` univariate factors, the specified-relaxation stall caveat, current-round-only policy scope, 20.9%, more propagator time, and no additional solve or demonstrated speedup. |
| Organization paragraph | Updated for the root's new appendices (`sec:parametric-proofs`, `sec:scheduling`). |

Earlier root repairs were preserved: strict `r*<1`, `C^2` factors, small
scales, singleton certificates, asymptotic convergence versus finite
termination, closedness for limit fixedness, no CLM "different mechanism"
claim, generic BM credit, Scott premises, no negative priority claims, and
the final-solve-savings wording.

## Notes for the root

1. **Citation insertion points.** Both sentences read correctly without a
   citation and contain no placeholder.
   - `algorithms.tex` lines 114–115, sentence "Checking floating-point
     proposals exactly after rational reconstruction is an established
     technique of exact linear programming." Append
     `~\cite{applegate2007-exact-solutions-to-linear-programming}`.
   - `algorithms.tex` lines 390–392 (sentence starting on line 390), "Bounds of this kind,
     evaluated with directed rounding, are an established way to obtain safe
     LP bounds from approximate dual solutions". Append
     `~\cite{neumaier2004-safe-bounds-in-linear-and}` before the semicolon.
   - Optional: the "Mathematical tools" paragraph of `related.tex` could add
     one sentence naming both techniques with the same two keys.
2. **`experiments.tex` callback wording.** Lines 275, 277, and 314–315 use
   "admitted" for callbacks that pass admission and a trigger. To match
   algorithms, use "acting callback(s)" (for example "allowed at most three
   acting callbacks", "trigger evaluations that started no acting callback",
   "per acting callback"). `effort.tex` uses admission only for the cheap
   test and the ledger, which is consistent.
3. **`local-rates.tex` (not owned).** No action needed: the current file
   already cites `prop:history` for shared histories (line 1289) and states
   the optimal-incumbent singleton in the `epsilon=0` passage
   (lines 1307–1310), matching the introduction and discussion.
4. **Floating-point validation appendix (full review M3).** The cleanest
   split in `algorithms.tex` is to keep the subsubsection heading and its
   first paragraph (lines 350–355), move everything from
   `\begin{proposition}[Outward row correction]` (line 357) through the
   paragraph ending "upstream of its import" (lines 357–510) to a new
   appendix, and keep the candidate paragraph "For a lower direction…"
   (line 512 onward), `prop:sidecar-validity`, and the cutoff paragraph in
   the main text. Replace the moved block by two or three sentences: each
   candidate is the dual bound of Proposition~\ref{prop:dual-residual},
   evaluated with directed rounding (Lemma~\ref{lem:enclosure}), for an LP
   whose rows are rounded outward (Proposition~\ref{prop:row-correction});
   the argument assumes IEEE binary64 arithmetic with gradual underflow and
   no flush-to-zero or denormals-are-zero mode. Keep the labels
   `prop:row-correction`, `eq:row-correction`, `prop:dual-residual`,
   `eq:dual-residual`, and `lem:enclosure` unchanged; `constraints.tex`
   cites `prop:dual-residual`, and the proof of `prop:sidecar-validity`
   cites `prop:row-correction`. The safe-bound attribution sentence of
   note 1 moves with the block; the exact-LP sentence stays at line 115.
5. **Precursor relaxation.** `experiments.tex` line 27 correctly describes
   the precursor's five-point tangents. That relaxation is also box-relative
   and therefore not monotone in general (foundations counterexample). The
   experiments section makes no monotonicity claim about it, so no change
   is needed; this is recorded only for consistency of later edits.
6. **Discussion reference.** The discussion cites `ex:history`, which the
   root moved to Appendix~\ref{sec:scheduling}; the reference resolves.

## Remaining objections

None in the owned scope. All material and minor findings addressed to these
files are resolved or deliberately not adopted with the reason above
(optional F6 generalization; reviewer-optional third pool mechanism). Root
notes 1, 2, and 4 concern citation keys, `experiments.tex`, and an optional
structural move outside my ownership.

## Verification actually run

All checks were targeted. No computational experiment, solver, archived
analyzer, project-wide verification, CI status or log inspection, or
literature search was performed.

1. Read-only source inspection with `sed`, `grep`, and `cat`: the six owned
   files; the cited statements in `certificates.tex`, `cutoff.tex`,
   `residual.tex`, `local-rates.tex`, `constraints.tex`, `effort.tex`,
   `experiments.tex`, and the new appendices; all review and audit files
   named in the task; and the archived solver source
   `research-20261003-adaptive-obbt/solver/adaptive_obbt.py`
   (`dual_box_bound`, `Relaxation.__init__`, `TriggerState`, `propexec`,
   pool insertion) and `experiments/frozen/models.py` (`nlvars`).
2. `python3 -I -B /tmp/rev2-checks/exact_checks.py` with `fractions.Fraction`
   only: verified the knots for `[-1/2,1]`, `phi_[-1,1](0)=0`,
   `phi_[-1/2,1](0)=-1/64`, `T_{1/4}([-1,1])=[-1/2,1/2]`,
   `T_{1/4}([-1/2,1])=[-1/2,41/80]`, feasibility of `(41/80,1/4)` on
   `[-1/2,1]` (secant value `121/160`), violation `21/80>1/4` on `[-1,1]`,
   validity at 41 grid points on both boxes, the `ex:not-fixed` iterates
   `s_k-1/2=2^{-k-1}` and the continuation `1/8, 1/32, 1/128`, and the
   Heron iterates with denominator digit counts `1,1,2,4,8`. Output:
   `EXACT_CHECKS=ok`.
3. `python3 -I -B -` reading the 20 frozen model JSON files of the
   prospective cohort: variables in product terms per model, minimum 10,
   maximum 144 (matches the frozen `models.py` definition of `nlvars`).
4. Disposable builds in `/tmp/rev2-build-B8vAIp` and, after the final
   edits, `/tmp/rev2-build2-MLv3jx` (`pdflatex`, `bibtex`, `pdflatex`
   twice on a copy of the full source): 95 pages, exit 0, no errors, no
   undefined or multiply defined references, no overfull boxes; two
   underfull boxes occur in the bibliography only. Pages 1, 7–11, 64–69,
   and 80–81 of the first build were rendered with `pdftoppm` and
   inspected.
5. A label and citation scan of the six owned files against all manuscript
   labels and `references.bib`: no missing reference, no missing key, no
   unfinished-text marker, no duplicate label.
6. `python3 -I -B verification/check_sources.py` (read-only):
   `SOURCE_CHECK=ok: 18 TeX files, 243 labels, 29 citations`.

These are document and exact-arithmetic checks of the revised text; they are
distinct from the root's final build and from CI.
