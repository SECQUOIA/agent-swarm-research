# Stage 7, round 1, independent reviewer 3

Decision: clean. No major or minor correction is requested within the formal-verification and portable-supplement scope reviewed here.

## Material reviewed

I read the main formal overview, `FORMAL-VERIFICATION.md`, the standalone formal supplement wrapper and its five formal accounts, portable-project README and build metadata, `verify.py`, the fresh verification manifest and logs, and the audit ownership implementation. I independently inspected the central source interfaces and definitions in the certificate, good-cone, exact-hull, and approximation packages, including `Model`, `Headline`, `Good`, `HullCore`, `Hull`, `AccuracyModel`, and `Accuracy`. I also checked the package coverage records and local Markdown source links.

## Findings

- The counts agree: 64 owned modules and 909 owned declarations, partitioned as 11/178, 10/158, 18/248, 10/93, and 15/232. Five additional local support modules are supplied and correctly distinguished from owned modules individually replayed by the runner.
- Every input fingerprint in the fresh portable verification manifest matches the current file. The five audit logs record the expected successful counts. All 64 kernel replay logs are present and empty, consistent with successful replay; the build log ends with successful completion. These are topic-specific checks, and the prose correctly avoids describing them as project-wide verification or independent-kernel verification.
- The axiom audit identifies declarations by their owning modules and applies `Lean.collectAxioms` transitively. It rejects axioms outside `propext`, `Classical.choice`, and `Quot.sound`. The runner checks the audit partition against the owned-module list and checks source/build/audit fingerprints before and after the run.
- The core theorem's formal hypotheses are strict nonemptiness and actual AHC/HHC. The separation weights and coefficient-cone limit are proved, not external premises. The feasible-set, aggregation, and nontrivial-certificate definitions agree with the mathematical account.
- The example's good predicate uses actual homogeneous negative inertia and validity on the ordinary convex hull. Its formal classification is not a surrogate definition. The direct two-point hull construction works for every r≥2 and uses the weighted perpendicular direction stated in the new manuscript, including r=2.
- The approximation model explicitly transports all 2r coordinates into Euclidean space, defines actual extended Hausdorff distance, and takes the infimum over arbitrary finite good families of the stated budget. The text correctly distinguishes the proved lower constant 1/2000 from the paper's stronger sqrt(2)/2000 and the old weaker logarithmic constant. It likewise distinguishes the formal signed-coordinate SDP test from the paper's shorter trace/vector test.
- The main scope statement explicitly excludes the general Gram theorem, arbitrary-quadratic and countable-weak statements, four-bound, many-row appendix, application, single-objective exactness, stronger constant, and literature priority. The detailed accounts make the relevant package boundaries clear. No claim of formal verification of the whole manuscript is made.
- The portable Lean source import closure contains every local `Formal.*` import. No local Markdown source link in the supplied audits is broken. The final main and detailed-supplement LaTeX logs contain no warning or undefined-reference lines. The detailed supplement repeats the setting and core proof and states the later systems directly, so it is understandable without external repository notes.

## Checks performed

Read-only Python checks recomputed every SHA256 recorded in the portable verification manifest, counted the owned/support modules and replay logs, checked every local Lean import, checked local audit Markdown targets, and inspected build/audit/LaTeX logs. No expensive proof rerun, manuscript mutation, project-wide check, or CI inspection was performed by this reviewer.
