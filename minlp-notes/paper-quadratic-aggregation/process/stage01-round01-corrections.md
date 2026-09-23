# Stage 1, round 1: corrections

Read the coordinator assessment and all five independent reports. Every
accepted finding is addressed in the scope authorized by the coordinator.
No later-stage proof is newly asserted by these corrections.

## Accepted findings and corrections

- **Major inventory omission:** added the concurrent frontier note to
  `coverage.md`, with a separate row for each substantive candidate: general
  replicated-matrix HHC, the three-inequality instance, good-multiplier cone,
  uniquely active rays, finite and uncountable strict-description necessity,
  the open hull formula and direct midpoint derivation, closed-hull
  qualifications, PDLC obstruction, projective/spectral qualifications,
  symbolic checks, and distinction from extended conic formulations. All
  remain candidates pending stage 4 development and review.
- **Formal scope omission:** inventoried topic 27. It changed from in progress
  to reported completion during this correction turn. Read the updated
  README, frozen claims, source inventory, declaration coverage, review and
  verification records, manifest, contributed paper section, and the new
  canonical §3.4. Recorded a dated SHA-256 snapshot in
  `stage01-formal-source-snapshot.json`. The inventory reports the package's
  completion claim and check evidence without implying this paper stage
  reran Lean or independently certified the implementation.
- **Dimension attribution:** added BDS's original standing `n>=3, m>=2`
  conventions and distinguished the paper's smaller-dimensional extension.
  Restored `n>=2` in the diagonal Theorem 2.12 attribution.
- **DMS attribution:** specified positive-definite signed combinations of
  homogenized matrices `Q_1,Q_2,Q_3`, dimension `n>=3`, and a nonempty proper
  hull in the three-inequality result.
- **Older exploration:** after the coordinator's expanded coverage decision,
  mapped the proved conflict-repair construction and corrected example to a
  concise stage 3 appendix. Rows cover validity and tangents, the DD repair
  LP, exact margins, inequality/equality normalization, conditional rows,
  pure-bilinear and Shor limits, and exact checks. Excluded unrelated
  inexact OA/Benders and unimplemented experiment proposals; no algorithm
  novelty or performance claim is authorized.
- **Stage plan:** expanded PROCESS.md to six stages: foundations; Conjecture
  3.3 proof; consequences/examples/checks and application appendix; Conjecture
  3.1 frontier development with literature audit; synthesis/supplement/package;
  full-manuscript review. A fresh five-reviewer round remains required before
  stage 2 because the first round accepted a major issue.
- **Literature record:** removed the obsolete blanket Conjecture 3.1
  exclusion, added the published Blekherman–Dunbar eprint, Wang–Kılınç-Karzan,
  Beck, Dey–Han–Wang, Dunbar thesis and homepage leads, supplementary
  Yildiran/Sheriff access leads, and the application prior-work obligations.
  The record explicitly distinguishes independent primary-source inspections
  already performed from reports read only in the frontier note and future
  inspection obligations. No new external source claim is represented as
  independently verified by this correction turn.

## Concurrent contributed formal section

The formal contributor added `sections/90-formal-verification.tex` and an
input in `main.tex` during this turn. At the coordinator's express instruction,
removed only that input line so stage 1 remains a foundations build. The
section is preserved unchanged and its SHA-256 is in the snapshot. Stage 2
will integrate and independently review the shorter main proof and a bounded
formal account without duplicate proof exposition. The original quantitative
cone-separation lemma remains mapped as supporting mathematics.

## Targeted checks actually run

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The final build passed and produced three pages after deferring the formal
section. A targeted `rg -n 'Warning|Overfull|Underfull|undefined'
 paper-quadratic-aggregation/build/main.log` found no matches (exit status 1).
An earlier build during the concurrent input change passed with four pages;
that is superseded by the final foundations build. One editing script first
used a root-relative path while running from the paper directory and raised
FileNotFoundError before making any edit; rerunning it from the repository
root completed the intended literature corrections.

Other checks were targeted reads/searches and source hashing. No Lean check,
project-wide verification, CI inspection, or subagent was used. No file
outside the paper directory was modified. No stage 4 proof or new manuscript
novelty claim was written.
