# Deterministic potential-flow certificates: verification record

Status: complete. Every check recorded here was run locally from `formal/`, and
each figure below is labelled with the run it belongs to: the original package
checks of 2026-09-20, the CC35 rationality correction, the CC33+CC35 re-run, the
rounded-asymptotics follow-up, or a re-run made while correcting this file.
Figures that belong to an earlier run are marked **historical** where they appear,
not only in a later section. Project-wide verification is CI's responsibility and
was **not** run locally; no CI status or log was inspected. Nothing here asserts
an unobserved CI result.

The package contains twelve proof modules. Line counts below are **historical**:
they describe the original package at commit `e04cd29d`, before the rationality
and rounded-asymptotic follow-ups. Two of them were wrong and are corrected:
`TwoPath.lean` was recorded as 805 lines and `TwoPathComparison.lean` as 1253,
against 727 and 1213 in that commit. The 1253 figure is the count after the later
CC35 rational-witness follow-up; 805 matches no commit in the history, where
`TwoPath.lean` goes 727 then 765. The other ten rows were exact. All twelve
figures were re-checked with
`git show e04cd29d:formal/Formal/PotentialFlow/<file> | wc -l`.

| Module | Original lines | Obligations |
|---|---|---|
| `Bregman.lean` | 263 | CC01-CC05, CC07-CC09 |
| `Bisection.lean` | 472 | CC06 |
| `Scenario.lean` | 400 | CC10-CC13 |
| `Support.lean` | 327 | CC14-CC18, CC20 |
| `SupportComplete.lean` | 1171 | CC19, CC21 |
| `Curvature.lean` | 192 | CC22-CC24 |
| `Laplacian.lean` | 705 | CC25-CC30 |
| `FieldDuality.lean` | 208 | ordered-field solvability engine for CC25, CC29 |
| `TwoPath.lean` | 727 | CC31-CC33 |
| `TwoPathComparison.lean` | 1213 | CC34-CC38 |
| `DyadicRoot.lean` | 243 | CC39 |
| `CertResults.lean` | 397 | CC40 |

## Original package checks

| Check | Result |
|---|---|
| Targeted module builds, `lake build --wfail` | PASS: all twelve, zero errors and zero warnings |
| Coexistence: the twelve modules imported together | PASS: no conflicting declarations |
| Import coverage, `python3 scripts/check_imports.py` | PASS: **historical figure** — all 394 proof modules imported by `Formal.lean`, the count at the commits where this check ran. Later topics have expanded the import registry; this historical count is not a current registry count |
| Axiom audit over every `Formal.PotentialFlow` declaration, including private helpers | PASS: 949 declarations at this run. **This row previously cited 962**, which is the count from the later CC33+CC35 re-run, so it contradicted the log it points to. The four audit runs are 949 (original), 957 (CC35 rationality correction), 962 (CC33+CC35 re-run) and 977 (rounded-asymptotics follow-up); 977 is also what a re-run gives today |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay, `LEAN_NUM_THREADS=1 lake env leanchecker` per module | PASS: all twelve |
| `#print axioms` on the headline theorems added to `Verify.lean` | PASS: 30 declarations at this run, standard axioms only. **This row previously cited 31.** `Verify.lean` carried 30 `PotentialFlow` prints at commit `e04cd29d`; the 31st, `TwoPath.exists_integral_dualLower`, arrived with the CC33 rational-witness follow-up. It carries 31 today |
| Independent review | PASS: four reviewers, no blocking or significant defect. The first three covered CC01-CC39; CC40 was reviewed later, having fallen outside all three groups. See [REVIEW.md](REVIEW.md) |

The [run log](verification/run.log) records the invocations and their output. It
is a retained record of an executed run and is not rewritten, so one slip in it
is reconciled here instead: it describes "the 30 `#print axioms` lines" and then
reports "31 declarations". The 30 is right for that run, as the commit contents
above show; the reported 31 does not match the 30 lines the same sentence
describes.
The audit itself is [`verification/AuditPotentialFlow.lean`](verification/AuditPotentialFlow.lean);
it is the project audit of `Verify.lean` restricted to potential-flow modules, so
it covers module-owned private and auxiliary declarations, not only the public API.
Reproduce it with:

```sh
lake env lean topics/16-potential-flow-certificates/verification/AuditPotentialFlow.lean
```

`Verify.lean` now carries thirty-one `#print axioms` lines for this package's
headline theorems — thirty at the original run, plus
`TwoPath.exists_integral_dualLower` from the CC33 follow-up — so the project-wide
CI audit covers them.

## CC35 rationality correction

The follow-up correction adds `TwoPath.exists_rat_dualPotential` and
`TwoPath.exists_rational_dual_data`. The latter proves that all five parts of the
two attaining dual witnesses are casts of rational data when `eps` is rational.
Their cast equalities identify them with the witnesses in the existing root-test
and attainment theorems.

The following targeted commands were run from `formal/` on 2026-09-20:

```sh
lake build --wfail Formal.PotentialFlow.TwoPathComparison
lake env lean topics/16-potential-flow-certificates/verification/AuditPotentialFlow.lean
LEAN_NUM_THREADS=1 lake env leanchecker Formal.PotentialFlow.TwoPathComparison
```

All passed: the final build had no errors or warnings, the audit covered 957
potential-flow declarations with standard axioms only, and kernel replay exited
successfully. An initial development build found two unresolved cast goals;
splitting on the path condition resolved them before these final checks.
`git diff --check` also passed. No project-wide checks or CI inspection were run
for this correction. The original check results above remain a historical record.

## What the proofs do and do not use

There is no `sorry`, no custom `axiom`, no `native_decide`, no `partial def` and
no `@[implemented_by]` in any of the twelve modules. The decidable rational
checks of CC40 and the sanity checks of CC06 and CC39 are discharged by ordinary
kernel evaluation (`decide +kernel`), not by native compilation, so their
evaluation is checked by the kernel like any other proof.

Kernel replay uses the installed Lean kernel and the pinned imported Mathlib
base. It is not an independently implemented proof assistant, and it is not a
fresh replay of all of Mathlib. Lean 4.33.1 and Mathlib v4.33.1 remain pinned
and are shared with the existing project.

## Scope of the guarantee

Verification applies to the definitions recorded in [COVERAGE.md](COVERAGE.md)
and to no others. In particular it does not establish novelty, bibliographic
priority, external peer review, or physical validity, and it does not verify any
numerical producer, conic solver or JSON parser. The exclusions frozen in
[CLAIMS.md](CLAIMS.md) — the original-uncertainty-instance mapping, the
spanning-tree conservation repair, machine-level bit-complexity claims, and the
effective-resistance restatement — remain outside the package and are not
verified. Following topic 3, the verified content of the constructive claims is
their correctness, termination and exact accuracy or size recursions; no counted
bit-cost model is claimed.

One defect was found and fixed during integration: `Curvature.lean` and
`Laplacian.lean` both declared `Network.sum_goal_eq_sum_residual`, which made
them un-importable together. The curvature lemma was renamed
`sum_goal_eq_sum_residual_of_feasible`, and the coexistence check above was added
so the condition cannot recur silently.

## CC36–CC37 rounded-asymptotics correction

The new perturbation lemmas preserve both width limits under `o(eps)` endpoint
and root errors. The Laplacian statement recomputes the curvature sum from the
perturbed endpoints. An independent source review confirmed correspondence with
the manuscript's conditional rounded-output extension.

The following commands passed on 2026-09-20 from `formal/`, with
`$HOME/.elan/bin` on `PATH` and `LEAN_NUM_THREADS=1`:

```sh
lake build --wfail Formal.PotentialFlow.TwoPathComparison
lake env lean topics/16-potential-flow-certificates/verification/AuditPotentialFlow.lean
lake env leanchecker Formal.PotentialFlow.TwoPathComparison
```

The build exited 0 without warnings; the audit covered 977 potential-flow
declarations with standard axioms only; kernel replay exited 0. Commands and
output are retained in [verification/rounding-followup.log](verification/rounding-followup.log).
No project-wide verification or CI inspection was performed. Earlier results
above remain historical.

## Documentation correction, 2026-09-20

An audit of this package's prose found scope wording to correct or clarify in
[COVERAGE.md](COVERAGE.md), including its CC40 row, wrong numeric records in this
file, and a duplicated coverage row. No Lean declaration or proof changed; the
edits affect documentation, including the module comment in `CertResults.lean`. The
CC40 review that had been missing was also run; both are described in
[REVIEW.md](REVIEW.md).

Two targeted commands were run from `formal/` for this correction, with
`$HOME/.elan/bin` on `PATH`:

```sh
lake env lean topics/16-potential-flow-certificates/verification/AuditPotentialFlow.lean
git show e04cd29d:formal/Formal/PotentialFlow/<module>.lean | wc -l
```

The audit exited 0 and reported 977 potential-flow declarations with standard
axioms only, matching the rounded-asymptotics follow-up above. The `git show`
counts are the source of the corrected line-count table. The CC36 counterexample
recorded in [COVERAGE.md](COVERAGE.md) was checked with `lake env lean` on a
scratch file outside the repository. No build, kernel replay, project-wide check
or CI inspection was run for this correction; the earlier results above remain
historical.

## Follow-up source review of the documentation correction

A read-only comparison with the Lean signatures and the two-path source example
identified further wording changes: `gap_zero_sound` needs `C.gap = 0` in
addition to acceptance; CC36 inherits unit coefficients and positive trial
values from its example; and CC26's zero-energy witness is checked inside the
proof even though the exported conclusion states only an inequality. The module
comment and coverage/review records now make these distinctions explicit.

After these comment and documentation edits, the following targeted command was
run from the repository root and passed:

```sh
git diff --check -- formal/Formal/PotentialFlow/CertResults.lean formal/topics/16-potential-flow-certificates
```

No build, axiom audit, kernel replay, project-wide verification or CI inspection
was run for this follow-up. Earlier execution results above remain historical.
