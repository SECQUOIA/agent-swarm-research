# Stage 5 correction record

Correction agent: `stage1_fixer`, distinct from the Stage 5 author.
Read all five Stage 5 reports and the coordinator's assessment. All
accepted findings were minor; the separate full-manuscript review remains
the next stage.

## Accepted findings and corrections

1. **R1/R2/R4/R5: LP scale count.** The abstract now says that a fixed
   barrier has *at most* two LP spectral scales, allowing the empty weak
   cluster at a unique optimum.
2. **R1: central-point terminology.** The numerical SDP description now
   refers to the exact central-point and stable quadratic-root formulas,
   avoiding confusion with the barrier's single analytic center.
3. **R1: simplex symbol.** Numerical prose, caption, and generated figure
   legend consistently use ϑ (`vartheta`). The reproduction README states
   that the unchanged internal CSV field `theta` denotes this parameter.
4. **R5: uniform residual hypothesis.** Both introductory uniformity
   summaries require bounded barrier parameters and centrality residuals
   bounded uniformly below one.
5. **Coordinator: CG interval ratios.** The numerical discussion identifies
   two and three as prescribed interval ratios before floating-point
   construction, without claiming exact spectral ratios for the rounded
   matrix used by CG and the reference solve.

## Validation

Ran the complete reproduction with the configured qipm Python:

```sh
make -C conditioning-paper reproduce PYTHON=/workspace/local-home/miniconda3/envs/qipm/bin/python
```

The Makefile fixes both BLAS thread counts to one. All reproduction checks
passed, including exact input certificates and numerical formula checks.
Compared the regenerated manifest with the previous manifest: only
`figures/simplex-plateau.pdf` and `repro/reproduce.py` changed hashes.
All 23 current manifest hashes independently match their files. Thus the
numerical rows, tables, other figures, and input data are unchanged.
The regenerated simplex figure was rendered and visually checked: its
ϑ legend is correct, legible, and unclipped.

Ran `make -C conditioning-paper clean` followed by
`make -C conditioning-paper`. The resulting manuscript has 36 pages.
The final LaTeX log contains no warnings, unresolved citations/references,
or overfull/underfull boxes. Build and reproduction logs are retained in
`/tmp/conditioning-stage5-correction-build.log` and
`/tmp/conditioning-stage5-correction-reproduction.log` for this session.

No original-paper, literature-corpus, or `central-path-cost/` files were
changed. All accepted minor corrections are complete.
