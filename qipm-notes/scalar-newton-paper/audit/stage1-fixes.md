# Stage 1 corrections

All four accepted minor findings in `stage1-assessment.md` are resolved.
No theorem scope, complexity bound, or proof constant changed.

1. **Approximate sampling and coupling.** In `sections/03-classical.tex`,
   Proposition `prop:precision` now defines the estimator and implementation
   to return zero on sampled zero coordinates, imposes the arithmetic-error
   condition only on the support, and explicitly asserts existence of a
   coupling with an exact-oracle execution. Its proof identifies off-support
   samples as coupling disagreements. The sufficient coordinate-error
   condition immediately after the proof is explicitly restricted to nonzero
   coordinates. This resolves reviewer 1 item 1, reviewer 2 item 1, reviewer
   3 item 2, reviewer 4 item 3, and reviewer 5 item 1.
2. **Ideal randomness.** The cost-model paragraph of
   `sections/02-models.tex` now grants unit-cost independent uniform real
   draws and exact comparisons with computed probabilities. It explicitly
   excludes the finite-bit implementation of these choices from the ideal
   arithmetic bounds. This resolves reviewer 3 item 1 and reviewer 4 item 4.
3. **Kantorovich attribution.** Lemma `lem:kantorovich` now names the
   classical inequality, describes the displayed version as an equivalent
   form, and cites Lin (2013), equation (1.1). Its elementary proof and
   estimator-specific sharpness statement remain intact. The new `Lin2013`
   bibliography entry uses the normalized metadata of the local literature
   package, whose original equation was checked by the root reviewer.
   This resolves reviewer 1 item 2 and reviewer 4 item 2.
4. **Sampler antecedent.** The paragraph after
   Theorem `thm:solution-sampling` now attributes the sampler-to-sampler
   question specifically to Andoni--Krauthgamer--Pogrow, Section 1.4, and
   distinguishes that question from their main coordinate-estimation
   theorems. This addresses the accepted clarification from reviewer 4
   item 1 without adopting the unsupported suggestion that the antecedent
   was absent.

Validation:

- The existing diagnostic passed under
  `/home/sgusev/miniconda3/envs/qipm/bin/python
  scalar-newton-paper/scripts/verify_classical.py`. It checks polynomial
  residuals, complex and support-restricted moments, the sharp variance
  witness, the raw rejection law, and arithmetic-error transfer.
- `conda run -n qipm --live-stream make -C scalar-newton-paper` completed
  successfully, producing the seven-page staged PDF. The final LaTeX log
  contains no undefined references, undefined citations, or box warnings.
- No extra diagnostic was added: the correction defines a previously
  undefined branch and states the coupling already proved; a numerical
  encoding of a zero fallback would not add distinct mathematical confidence.

Verdict: the accepted Stage 1 findings are fully addressed; no new major or
minor issue was identified during the correction check.
