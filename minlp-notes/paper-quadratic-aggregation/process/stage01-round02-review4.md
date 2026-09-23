# Stage 1, round 2: independent review 4

Date: 2026-09-22. Scope: corrected foundations, attribution, inventory, and
stage plan. I read the coordinator's round 1 assessment and correction report,
the current setting/scaffold, and updated coverage, literature, and formal
source snapshot records. I did not read another round 2 review or edit sources.

## Verdict

Accept stage 1. No remaining major or minor issue identified in its current
scope. This does not certify the deferred certificate proof, application,
formal interfaces, or frontier candidates.

## Corrections verified

- The diagonal-case attribution now expressly retains `n >= 2` from BDS v2
  Theorem 2.12.
- The original BDS standing dimensions `n >= 3, m >= 2` are now distinguished
  from the proposed smaller-dimensional extension. I checked these standing
  dimensions against Section 2.1 of `/tmp/quadratic-paper-literature/bdsv2.txt`.
- The DMS summary now identifies the homogenized matrices, signed real
  combination, dimension restriction, and nonempty proper hull. It no longer
  leaves readers to guess between `A_i` and `Q_i`.
- The frontier note is inventoried by substantive claim, including its general
  HHC construction, good-multiplier cone, finite/uncountable strict-description
  obstruction, open hull formula, direct midpoint proof, closed-hull variants,
  spectral qualifications, and conic-formulation limitation. These are clearly
  deferred candidates. The earlier blanket exclusion of Conjecture 3.1 has
  been replaced with a dedicated author/reviewer stage and literature audit.
- The formal package's reported status is accurately separated from independent
  verification by this paper process. Its main-proof scope and exclusions,
  source snapshot, shorter proof, and stage 2 integration are recorded. I read
  the current formal README, which corroborates the reported 12 obligations,
  11 modules, 178 declarations, and 11 kernel replays. I did not rerun Lean.
- The older application construction and corrected example are now mapped to
  a concise appendix with their normalization, activation, local/global,
  termwise/Shor, exact-margin, and bilinear qualifications. The unrelated
  OA/Benders exploration and proposed benchmarks are explicitly excluded.
- New external literature entries distinguish inspected primary sources from
  reports in a repository note and sources still to inspect. They do not
  prematurely establish novelty or transfer proof verification.
- `main.tex` still inputs only the foundations section. Deferring the formal
  section is consistent with the plan; missing later proofs are intentional.

## Targeted checks actually run

I used `cat`, `sed -n`, `rg --files`, and targeted `rg -n` to inspect the
records and manuscript above, the BDS standing dimensions, the frontier
headings, and the application note/review. One exploratory filename glob
`notes/algorithm-opportunities*` matched no file; I then read the exact
`notes/research-20260912-algorithm-opportunities.md` path from the inventory.

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage01-round02-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage01-round02-review4/main.log
```

Independent temporary-directory build passed and produced three pages.
The final log search found no matches. No project-wide test, CI check, Lean
build, numerical experiment, or subagent was used.
