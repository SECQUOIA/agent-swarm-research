# Stage 3 corrections

Correction author: `/root/stage03_corrections`. Date: 19 September 2026.

Status: all eight accepted minor groups are corrected and verified. The five review reports and lead disposition were read before correction. No major finding was identified in that review round, and no new scientific defect emerged during these corrections. The lead's acceptance remains separate from this author report. No Stage 4 narrative or packaging was authored.

## Itemized closure

1. **Monotonicity domain.** The model appendix now states that all allocation laws are nondecreasing on `[0,10/11]` and convex and continuously differentiable on an open neighborhood. The finite epigraph-bound argument still uses only the former interval. No equations, model bounds or data changed.
2. **Two-dimensional diagnostic design.** The empirical oracle subsection explicitly defines `q(x)=x^T Q x-1`, the transformed row `exp(a q(x))-1`, and `a in {1,2,4,8,16,32}`. This matches `lbesh_oracle_diagnostic.py`, including its 896-cut count.
3. **Effective master and conic settings.** The design distinguishes overall targets from the prototype's inner `MIPGap=1e-6` and `MIPGapAbs=1e-8`, verified against `lbesh/solver.py:98–99`. It states the conic adapter's `FeasibilityTol=IntFeasTol=1e-8` alongside `NonConvex=0`, verified against `lbesh_research/conic.py:358–361`. Matched ESH/ECP settings remain explicit.
4. **Continuous-reference settings.** The design now supplies one thread, 300 seconds, 300 iterations, and `1e-9` absolute-gap, relative-gap and feasibility targets, checked against `lbesh_research/conic_reference.py:140–151`. The text distinguishes these from benchmark limits.
5. **Objective comparison tolerance.** A labeled equation defines `T(w)=1e-6+1e-4 max(1,abs(w))` at the comparison witness objective. The text gives both minimizing and maximizing bound contradictions and explains incompatibility of an infeasibility report with a validated feasible witness. The enumeration paragraph explicitly uses `abs(f-f_ref)<=T(f_ref)`. These statements match `lbesh_study_analysis.py:245–259`, `lbesh_results_independent_audit.py:121–131` and `analysis_v1/derive_ablations_references.py:60–65`.
6. **Diagnostic timer boundary.** The text excludes imports and creation of the counted function/oracle objects, and includes per-call row/container construction and Python bookkeeping. The timer placements and `call_cut` implementation were inspected directly in `lbesh_oracle_diagnostic.py:66–100,121–131`.
7. **Figure annotations.** The generator supplies small opaque white backgrounds to the value labels in both cost-tradeoff panels. The dashed unity line remains visible except behind labels; rendered numbers are unobstructed. All outputs were regenerated with the specified repository virtual environment, and a consecutive regeneration produced byte-identical results.
8. **Analytic ECP target.** The empirical ellipsoid paragraph explicitly compares ECP constants with their own analytic ECP constants and explains that these generally differ from supporting constants. This follows the separate `analytical_cut_constant_error` and `support_constant_error` fields in `lbesh_oracle_diagnostic.py:133–150`.

## Targeted checks actually run

From the repository root:

```bash
code/minlp_solver_lab/.venv/bin/python paper-lbesh/scripts/regenerate.py
python paper-lbesh/scripts/check_evidence.py
```

Both succeeded. Regeneration produced 17 tables, both PDF figures and the full 1,464-record CSV. The narrow evidence checker passed narrative arithmetic, all batch outcomes, paired work, repetitions, LP exits, references, oracle counts and exact reconstruction of all 51 parameter streams.

An inline standard-library Python check hashed all 21 generated outputs, invoked `code/minlp_solver_lab/.venv/bin/python paper-lbesh/scripts/regenerate.py` once more with `subprocess.run(..., check=True)`, and compared hashes afterward. All 21 were byte-identical. The hashes and result are saved in `evidence/stage03-correction-regeneration.json`.

From `paper-lbesh`:

```bash
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex \
  > process/stage03-corrections-build.log 2>&1
pdftotext -layout main.pdf process/stage03-corrections-rendered.txt
```

The clean build succeeded, producing 37 pages. The final log contains no undefined references/citations, warnings or overfull boxes. The existing harmless bibliography URL underfull box remains. The additional settings/tolerance text changes pagination from the author's 36-page snapshot. The rendered text contains each new definition and clarification.

From the repository root:

```bash
pdftoppm -singlefile -scale-to 1800 -png \
  paper-lbesh/figures/cost_tradeoff.pdf \
  paper-lbesh/evidence/stage03-corrected-cost-tradeoff
```

I inspected the resulting PNG with `view_image`. All value labels are readable, the dashed unity line does not cross their glyphs, and neither panel has clipping. The statistical values and axis ranges are unchanged.

A final inline SHA-256 check compared the 47 files in the author's source fingerprint with the corrected files. Exactly six files changed: the four section files named above, `scripts/regenerate.py`, and `figures/cost_tradeoff.pdf`. All other frozen manuscript/data/table/figure inputs in that snapshot are identical. All 17 original evidence inputs listed in `data/provenance.json` also retain their recorded hashes. The corrected 47-file snapshot is `process/stage03-corrections-source-sha256.json`.

All commands succeeded on their first invocation during this correction pass. No solver performance runs, raw-witness revalidation, broad tests, project-wide checks or CI inspections were performed. Accepted Stage 2 theory and all research sources/data were preserved. This is the source-frozen handoff for lead inspection and Stage 3 acceptance.
