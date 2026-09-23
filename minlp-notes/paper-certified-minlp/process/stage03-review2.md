# Stage 3 independent review 2

Reviewed 2026-09-13: all files in the standalone `formal/` source package, Section 5, the changed introduction, Stage 3 author report/manifest, and their correspondence with the accepted mathematical and implementation sections. Designated full Lean build reviewer. No shared manuscript, proof source, checker, or dependency files were changed.

**Verdict: no major or minor correction required.** The inspected formal statements match the manuscript's qualified scope, and independent verification passed. This is approval of Stage 3's focused theorem package, not a claim that the software checker or benchmark certificates have been verified in Lean.

## Independent build and provenance checks

I copied the entire formal source package to `/tmp/cert-minlp-stage03-review2-rb5blzpm/formal`, excluding `.lake`, created an empty project `.lake`, and linked only its dependency directory to the existing pinned dependency cache. I then ran the package's unmodified `bash scripts/verify.sh`. All project proof modules were compiled from source with no preexisting project build products. The independent log is at that temporary copy's `review2-run.log`.

The command exited with status zero and reported:

```text
PASS: all 3 proof modules are imported exactly once.
Built CertifiedMinlp.Coordinates
Built CertifiedMinlp.SafeCuts
Built CertifiedMinlp.Transfer
Built CertifiedMinlp
Build completed successfully (3010 jobs).
PASS: audited 95 project declarations; only propext, Classical.choice, Quot.sound are allowed.
replaying CertifiedMinlp.SafeCuts
replaying CertifiedMinlp.Coordinates
replaying CertifiedMinlp.Transfer
replaying CertifiedMinlp
PASS: build, axiom audit, module coverage, and kernel replay.
```

The four displayed principal theorem axiom lists contained exactly the permitted standard axioms. The recorded `verification/SHA256SUMS` passed independently. I also checked every one of the nine manifest dependency repositories: actual `HEAD` matched the pinned manifest revision and each working tree was clean. In particular, mathlib matched `0df444a360eaa60ab8c11dca51a86af692955474`.

This was a fresh compilation of the paper's proof modules using cached dependencies. It was not a fresh download or recompilation of mathlib, and it did not replay every mathlib declaration. Those are also the manuscript's stated limits.

## Proof integrity and audit coverage

- `CertifiedMinlp.lean` imports all three proof modules. `check_imports.py` compares its imports with every `.lean` file below the project module directory and rejects missing, duplicate, or unexpected imports.
- The axiom audit selects declaration ownership through the environment's module index and the `CertifiedMinlp` module prefix, not by the declaration's public namespace. Thus private and generated declarations belonging to those modules are covered. It traverses every selected declaration's transitive axioms and rejects anything outside `propext`, `Classical.choice`, and `Quot.sound`; the nonempty audit assertion prevents a vacuous pass.
- Manual inspection of all theorem sources found no added axiom, `sorry`, `admit`, native proof shortcut, unsafe declaration, external implementation hook, or environment mutation. The only project `run_cmd` is the diagnostic axiom audit in `Verify.lean`; it does not insert mathematical declarations.
- I inspected the installed Lean 4.33.1 `LeanChecker.lean` implementation. The supplied `leanchecker -v CertifiedMinlp` command discovers all compiled modules with that prefix, not just the declaration-free umbrella. It loads their exported/server/private parts and replays their declarations using the installed kernel. The independent log confirms all four project modules were replayed. Imported declarations remain the trusted dependency environment, exactly as Section 5 and the README explain.

## Mathematical correspondence

The coordinate definitions use rational bounds and explicit bounded/lower-bounded/upper-bounded/free constructors. Their membership and acceptance predicates match the rational enclosure table. The proofs establish the desired bound on the actual real residual at every admissible real coordinate. Free coordinates derive residual zero, fixed coordinates yield zero correction, and inconsistent bounded coordinates cannot meet the support membership premise.

`safe_affine_of_shift_bounds` performs the finite-sum residual algebra. `rational_enclosure_cut` obtains individual shift bounds from the coordinate theorem and the genuine enclosure premises before proving the underestimator. It does not assume the resulting affine inequality. The assumptions expose the support inequality and actual value/gradient enclosures, so the manuscript correctly excludes deriving support from convexity and evaluating intervals in software.

Generic transfer requires feasible embedding and objective equality; its epigraph specialization explicitly defines the master and constructs the graph point from base inclusion and valid cuts. The standalone proof does not pretend to verify parsing, affine propagation, integrality extraction, or LP/VIPR identity. The signed objective lemmas match the original minimization/maximization convention.

`incumbent_cutoff_lifting` proves the correct additional step from a bound inside a checked incumbent's weak cutoff to a bound on every feasible point. It assumes the restricted-set bound and does not claim to formalize the VIPR inference invariant. This matches Sections 3–4.

The primal infimum theorem first constructs a nonempty objective image and a bounded-below proof, then applies the conditional real infimum lemmas. The matching-witness theorem proves both equality to the lower bound and pointwise optimality. Empty feasible sets use the separate pointwise transfer convention and are not incorrectly represented by a real infimum equal to positive infinity.

## Manuscript assessment

Section 5 and the changed introduction accurately identify the proved mathematical interfaces and preserve the distinction between theorem verification and executable/artifact checking. The coverage table's stated premises and exclusions agree with the inspected declarations. No theorem is presented as a new general mathematical principle, and the comparison with earlier verified optimization work remains appropriately qualified.

No missing later experiment, artifact package, or final paper-wide check has been counted as a defect in this stage. Those remain the coordinator's separate stages.
