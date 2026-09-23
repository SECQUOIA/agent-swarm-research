# Coordinator investigation

## Initial scope and sources

The existing repository has uncommitted LB-ESH development and evidence. Preserve those files. The completed frozen research bundle is `code/minlp_solver_lab/results/lbesh_development/publication_bundle_v1.tar.gz` (9,077 members, approximately 37 MB compressed). Its top-level paths are `AGENTS.md`, `README.md`, `code/`, and `notes/`; it includes the frozen source archive, raw runs, topic sources, environment pins, and legacy model sources. It can be delivered separately from a compact LaTeX source archive. Standalone relocation still needs verification during packaging.

The theory's principal qualifications are necessary: each separate disjunction hull differs from the full GDP hull; exact finite separation does not guarantee an exact feasible incumbent or objective gap; the implemented fractional cutoff differs from the residual-calibrated theorem; single-tree termination needs old-cut enforcement and control of fractional work; approximate boundary tangents must retain their full constant. The existing rowwise `_esh_cuts` implementation matches the rowwise mathematical construction, rather than a single root search over the maximum of rows.

The computational appendix must distinguish the pre-freeze continuous-reference pass, frozen primary runs, planned supplementary batches, and the two outcome-triggered follow-ups. No best-of pooling. The held-out controls are predeclared and untuned, not entirely unseen before the freeze.

The exact fixed weight cutoff needs care in the algorithm description: `_separate_point` defaults to `lamtol=1e-6` and `_lp_phase` calls that default; the optional fractional `MIPNODE` user-cut callback explicitly uses `lamtol=0.05`. Do not describe 0.05 as the initial LP phase's cutoff. Both are fixed numerical thresholds, distinct from the residual-calibrated mathematical proposal. The predicate skips `lambda <= lamtol`.

## Historical hardware evidence

The archived environment JSON records WSL2 Linux, 36 logical CPUs and Python 3.13.11. The development log records approximately 30 GiB RAM. Historical native solver logs identify the CPU as Intel Xeon w5-2565X; this is evidence from the experiment rather than inference from the current host. Examples:

- `main_generated_v1.jsonl.runs/48581c65ddd14947/gams.log`, line 45.
- `main_generated_v1.jsonl.runs/46b68d379557265f/gams.log`, line 45.
- `main_generated_v1.jsonl.runs/2578ea8681fdb650/gams.log`, line 45.

These paths are relative to `code/minlp_solver_lab/results/lbesh_development/`. Runs used one solver thread and at most six simultaneous workers; other machine work was present. Timings are end-to-end and the three schedules are not search-seed replications.
