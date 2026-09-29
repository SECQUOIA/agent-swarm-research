# Topic 33 verification record

Date: 2026-09-29. Scope: the six modules `Formal.CompetitiveBranching.Model`,
`Lemmas`, `Counting`, `Theorem1`, `Competitive` and `Pruning`. All checks
below are targeted checks, run locally from `formal/` with the pinned
Lean 4.33.1 and Mathlib. The final run of each check came after the last
source edit, which deleted the unused definition `LeavesValid` from
`Model.lean` after the [statement review](reviews/statement-review.md).
That edit rebuilt all six modules. Checks 1–4 were rerun after it; the
earlier run audited 171 declarations. The difference of four is
`LeavesValid` and the auxiliary declarations Lean generated for it.

## Commands and outcomes

1. Warning-free build of the six modules:

   ```sh
   LEAN_NUM_THREADS=1 lake build --wfail \
     Formal.CompetitiveBranching.Model Formal.CompetitiveBranching.Lemmas \
     Formal.CompetitiveBranching.Counting Formal.CompetitiveBranching.Theorem1 \
     Formal.CompetitiveBranching.Competitive Formal.CompetitiveBranching.Pruning
   ```

   Exit status 0: `Build completed successfully (8711 jobs).` All six modules
   were rebuilt, with no warnings.

2. Axiom audit of every declaration owned by the six modules, including
   private and auxiliary declarations:

   ```sh
   LEAN_NUM_THREADS=1 lake env lean \
     topics/33-competitive-branching/verification/AuditCompetitiveBranching.lean
   ```

   Exit status 0. The audit fails on any axiom other than `propext`,
   `Classical.choice` and `Quot.sound`, including `sorryAx`. Output:

   ```text
   PASS: audited 167 topic-33 declarations across 6 modules.
   'CompetitiveBranching.internal_le' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.size_le' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.count_interval_le_three' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.count_first_interval_le_one' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.count_last_interval_le_one' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.count_breakpoint_le_one' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.eq_leaf_of_certificate_one' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.key_left' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.key_right' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.size_add_three_le' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.size_lt_four_mul' depends on axioms: [propext, Classical.choice, Quot.sound]
   'CompetitiveBranching.theorem1' depends on axioms: [propext, Classical.choice, Quot.sound]
   ```

   The same file prints the statements of `internal_le`, `size_le`,
   `theorem1` and `size_lt_four_mul` with `#check`.

3. Kernel replay of each module:

   ```sh
   for mod in Model Lemmas Counting Theorem1 Competitive Pruning; do
     LEAN_NUM_THREADS=1 lake env leanchecker Formal.CompetitiveBranching.$mod
   done
   ```

   All six exited with status 0 and printed nothing. The replay uses the
   pinned Lean kernel; it does not rebuild dependencies from source.

4. Source and root-import checks:

   ```sh
   grep -nE "\bsorry\b|^\s*axiom\b|admit" Formal/CompetitiveBranching/*.lean
   grep -c "^import Formal.CompetitiveBranching\." Formal.lean
   ```

   The first found no match (exit status 1). The second printed `6`: the root
   `Formal.lean` imports all six modules, as `scripts/check_imports.py`
   requires.

During development, each module was also elaborated with
`lake env lean Formal/CompetitiveBranching/<Module>.lean`. The independent
[statement review](reviews/statement-review.md) records its own reruns of
these checks on the earlier sources.

## Not run

No project-wide verification was run: not `scripts/verify.sh`,
`scripts/check_imports.py`, `lake build` of the root `Formal` library,
`Verify.lean`, or `lake env leanchecker -v Formal`. CI status and logs were
not inspected. CI performs the project-wide checks.
