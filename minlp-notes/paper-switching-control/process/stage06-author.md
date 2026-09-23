# Stage 6 author handoff

Status: author draft complete; no claim of stage acceptance. The required five
independent reviews and root adjudication follow this handoff. No subagents
were used by the author. Work was confined to paper-switching-control; no
original repository result, literature package, or reference artifact was edited.

## Manuscript and organization

The paper is now a complete56-page article with abstract, introduction,
related-work comparison, proof roadmap and synopsis table; all accepted
mathematics; reproducible computations; a closing research-scope discussion;
an appendix; and13 bibliography entries. Added manuscript files are
sections/00-introduction.tex,12-computations.tex,13-discussion.tex and
14-higher-reach.tex. Two standalone PDF figures and four generated experiment
tables plus timing macros are included. main.tex adds graphicx and the new
sections. README is now a consolidated build/verification/data guide rather
than accumulated stage scaffolding.

Before/after change map:

1. Every accepted section01–06 and08–11 is byte-for-byte unchanged relative to
   process/snapshots/stage05-accepted. This includes every mathematical proof,
   structural counterexample, source correction, algorithm contract and coarsening
   result from the accepted draft.
2. Old07 was split at its second section heading. Its first section remains in
   07-predecessors-and-frontier.tex. Its entire second section is verbatim in
   14-higher-reach.tex, now AppendixA after the closing discussion.
3. The first part of07 has one addition: the explicitly attributed classical
   comparison equation eq:classical-small-mode and its short cell-averaging
   proof. Removing that paragraph and concatenating07 and14 reproduces the
   original07 EXACTLY. process/stage06-preservation.json records the equality,
   unchanged filenames, old SHA-256, and the exact added paragraph. No existing
   result was silently removed or changed by the reorganization.
4. Introduction, abstract, computation and discussion are new authoring. The
   manuscript has no internal acceptance/stage-history prose. Process history
   remains separate. process/claim-coverage.md is now the definitive result/
   development map; its former candidate history is preserved unchanged in
   stage06-coverage-before.md. stage06-repo-inventory.txt records the CIA files
   used in the coverage audit.

## Further mathematical/application development

- The primary Zeile–Robuschi–Sager Corollary1 supplies the classical unrestricted
  grid bound(2n−3)/(2n−2)*h. Applying it on k equal cells and using exact cell
  averaging proves F_n,k−1 <=(2n−3)T/((2n−2)k). This is clearly attributed,
  independent of the new sharper fixed-budget results, and does not transfer
  the source's unrestricted-grid tightness to a hard-budget equality.
- The quantized public profile has an exact continuous one-switch optimum
  4721469/2500000=1.8885876 at that same switching time, mode2→3 under the
  manuscript's one-based labels. All six ordered-pair affine crossings are
  evaluated exactly, followed by independent direct evaluation at every fine
  input knot and the switch. Full fine-grid optimum remains1889/1000 and its
  exact gap1031/2500000 is below h/2. Root independently obtained the same
  values using a separate integer/rational implementation.
- The uniform n3,T1,s2 continuous comparison1/6 is proved directly in the text;
  the k<n uniform theorem is not incorrectly invoked at k=n. Every displayed
  coarse convergence value is corroborated by a separate labeled-word/boundary
  enumeration, not merely a rerun of the same optimizer.

The declared open questions are the same independent research directions:
general five-block reach and exact higher-budget minimax, exact F3,3, a general
floor-history switch law, the unused largest-heavy adjacent-repeat strengthening,
and constraint-aware transfer beyond the proved dwell/transition scope. The
paper does not present them as missing proof steps. State/objective/control-loop
application claims are not inferred from discrepancy alone.

## Experiments and reproducibility

verification/stage06/experiments.py freshly retrieves the pinned public CSV and
checks SHA-2561ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883.
The normalization and largest-remainder quantization are exact and documented.
Their error bounds are separate: normalization<4.959e−7 per rate;
quantization<1e−6 per rate; cumulative perturbation<12e−6 relative to the
normalized source. No unnormalized column is silently treated as simplex input.

The public study includes every budget0–3 on EACH gridM12,24,48, plus the fine
one-switch and continuous one-switch optima. Every coarse output is evaluated
at all original fine endpoints. A separate full labeled-word/boundary enumerator
corroborates allM12/M24 optima. M48 uses the proved exact subset algorithm;
root separately corroborated its values. All coarse grids nest12000, so the
reported strict/general certificates bound both continuous and fine-grid optima.
The actual stage05 coarsener separately reproduces M24,s2 and its(1,1.5]
certificate. The manuscript explains stronger one-switch half-mesh and exact
zero-switch cases and the input-perturbation interval expansion.

Exact public rows by increasing budget:

- M12:3.7771752,1.9999996,1.8540056,0.8540056.
- M24:3.7771752,1.9999996,1.5,0.5263358.
- M48:3.7771752,1.9999996,1.5,0.52633545.

results.json stores all rational outputs and timing samples;
derived_public.json stores exact coarse masses. The original CSV is not bundled.
The script accepts either explicit --fetch or a hash-checked --data file.
check_results.py validates all derived optima, archived schedule witnesses,
strict/clipped brackets, crossing-oracle cases, controlled instances and
uniform convergence offline. It clearly states that source integration/public
continuous crossings require rerunning with fine data; an archived summary
is not misrepresented as an independent source proof.

The deterministic controlled comparison uses matched grids, budgets, objectives
and rational arithmetic for subset DP and separate word enumeration. Uniform
scaling cases vary mode count and grid size separately at budget2. Timings are
fresh medians of three calls, with CPU/wall samples, machine and Python metadata,
explicit solver-only boundaries, and shared-host caveat. There is no claimed
performance ordering versus SCARP, pycombina, commercial MILP or the2025 method.

render_results.py regenerates exact-decimal tables and timing macros; --check
compares them without writing. Optional --figures uses Matplotlib to generate
PDF figures. The first figure labels the geometric ONE-SIDED uniform term,
not the full uniform-input error, and the introduction states correctly where
it exceeds the plateau. The second figure compares matched public grids and
the independently established uniform continuous oracle. All discrete-case
interpolation is described as a plotting convention.

## Sources and evidence

verification/stage06/source-record.md records fresh primary-source checks and
precise limits. It incorporates the retained final-source audits from stages4–5.
The2025 publisher's indexed introduction was available and explicitly states
loss of optimal substructure/general global optimality; direct access returned403
and the full final PDF was not audited. The text relies only on the checked
introduction-level statement. Classical prefix-flow/matching, CIA decomposition,
SCARP, dwell algorithms, switching-time enumeration, and state-error bounds
are credited. The bounded literature comparison makes no claim of exhaustive
priority or first invention of a generic method. No author was contacted.

## Completed validation

- Fresh full public-data reproduction succeeded, including all twelve coarse
  budget cases, all6 continuous pair crossings, fine endpoint evaluation,
  nine uniform convergence cases and their independent enumeration, coarsener
  crosscheck, seven scaling cases and three matched exact-method cases.
- verification/run_all.py succeeded in the manuscript directory. It runs all
  portable prior proof/certificate/algorithm suites, original-artifact integrity,
  stage6 offline checks, and non-writing generated-table checks.
- A standalone relocated bundle in process/stage06-relocated built with
  latexmk/BibTeX and passed the SAME complete offline suite without any
  dependency on the repository originals. Final-pass main.log and main.blg
  contain no undefined references/citations, overfull/underfull boxes or warnings.
  Earlier-pass rerun messages in aggregate build.log are ordinary LaTeX passes.
- Visual inspection covered added intro pages1–5, computation/discussion
  pages48–51, transferred appendix pages52–55, both figures and bibliography
  pages55–56. The source-data citation was shortened to avoid badly justified
  long tokens; full path/commit/hash remain in the source record. One orphan
  final discussion word was removed. Other proof-body content is unchanged.
- The three new standalone verification/generation entry points explicitly reject
  Python -O; this prevents skipped assertions or source-hash checks. Normal
  execution and negative -O entry tests pass.
- Byte-preservation audit described above succeeded. Immutable old snapshots
  and all30 original reference artifacts remain unchanged.

Working logs and rendered-page images are diagnostic artifacts, not proof
inputs. Stage6 now awaits its required independent review. The author stops
writes after delivering the handoff.
