# Final scope edits: bounded Sol review

Date: 2026-10-05. This is a report-only review of the four edits requested
after the completed Opus whole-paper R2. **Pass: all four findings are
resolved in the actual current text. No new mathematical or summary-scope
objection remains in this bounded review.** It does not re-review unchanged
proofs, certify novelty, or provide external peer-review approval.

I read Section 5 of evidence/reviews/opus-wholepaper-r2.md and its relevant
verdict, source and prior-review context. I read the actual revised abstract,
the affected introduction and fields passages, and the cited unchanged
model, recourse and Appendix L contracts. Two delegated read-only checks
separately examined the cone statements and the diagnostic/recourse edits;
both agreed with the dispositions below.

## Finding dispositions

1. **Abstract cone scope, Opus Finding 1 (P2): resolved.** At
   [abstract:32](/workspace/minlp-notes/paper-exact-arithmetic/sections/abstract.tex:32),
   the text now gives polynomial-time exact feasibility and witness recovery
   for second-order cone systems over one explicitly represented real number
   field only when both integer dimension and the continuous squared-cone
   residual Hessian-span dimension are fixed. This matches
   thm:cone-feasibility at L:672–678 and thm:cone-witness at L:992–1004.
   The formal field input includes a dense primitive polynomial, selected
   real-root isolator and charged power-basis data. Its span is over K;
   L:663–667 proves that this rank equals the real span rank at the selected
   embedding. Thus the abstract's ordinary span wording introduces no
   rational-span interpretation or succinct/unrelated-field encoding. It
   no longer reads as an unrestricted cone algorithm or asserts a uniform
   polynomial exponent in the two parameters.

2. **Unpublished cyclic rank diagnostics, Opus Finding 2 (P3): resolved.**
   The finite-computation references are absent from the affected 00/08
   sources. At [00:573](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:573),
   the proved dimension and product-independence results remain, and whether
   products exhaust the stationary quartics remains explicitly open. At
   [08:750](/workspace/minlp-notes/paper-exact-arithmetic/sections/08-fields.tex:750),
   the equality J_4^Q(p)=W^Q(p) is still open, followed by the correctly
   conditional descent consequence for any n>=4 where it holds.
   thm:fields-descent retains its dimension, stationary-space, baseline-SOS,
   global-convexity and positive-Hessian hypotheses; prop:fields-cyclic
   retains the relation basis and product-independence conclusion. No proved
   mathematical development or dependency was removed. This conclusion is
   local to the edited passages, not a rerun of the separate 97-row coverage
   audit.

3. **Quartic recourse antecedent, Opus Finding 3 (P3): resolved.** At
   [00:205](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:205),
   “such a guarantee” now clearly refers to the proposed full-point quartic
   guarantee. The implication matches rem:recourse-quartic at 10:574–585:
   adding one dummy core to a box-convex quartic leaves its residual
   minimizer unchanged by the tilt, with k=1 and core curvature Lambda=1.
   Fixing a positive constant tilt width and requesting point accuracy 1/4
   distinguishes the designated coordinates 0 and 1. The proposed bound
   would therefore give Las Vegas expected polynomial time for the source
   Square Root Sum and PosSLP problems. The sentence states this consequence;
   it does not infer an unconditional impossibility or solve quartic
   recourse. The actual cubic recourse theorem is unchanged.

4. **Cone algorithm versus unrestricted SOCP hardness, Opus Finding 4
   (P3): resolved.** At [00:421](/workspace/minlp-notes/paper-exact-arithmetic/sections/00-introduction.tex:421),
   the text names unrestricted-h SOCP PosSLP-hardness, says that h can grow
   in those gate constructions, and states that the new polynomial-time
   theorem fixes both t and h. This matches rem:models-socp at 01:453–481
   and the exact cone-span definition. For a squaring gate
   2x_i>=x_j^2, its Lorentz form has squared residual
   4x_j^2-8x_i and Hessian 8 e_j e_j^T. Distinct nonconstant predecessors
   give independent diagonal directions; a chain with m squaring gates
   already gives at least m-1 such directions in the primal subsystem.
   The source reduction's additional dual subsystem does not remove these
   existing directions. Thus “can grow” is supported directly by the
   printed construction without asserting that every circuit has large h.
   This explanation imports no new source theorem or stronger hardness
   model and preserves the explicit-field and fixed-parameter scopes.

## Reviewed snapshot

The hashes were refreshed after reading the actual repaired passages. The
model and recourse dependencies are unchanged from the earlier integration
review. The current L differs from that earlier snapshot by its subsequently
reviewed source-attribution update; only the relevant current statements
and input/span definitions were inspected in this bounded round.

```text
491f90e98658426866e4755c8b3b5f4d84d85569f02e083241d5f2cdd4a7cca8  sections/abstract.tex
32a473010509ff4930f8dfa4d67fd1f1efdf014723c23fba142967a388f17f92  sections/00-introduction.tex
1c3b8d8123348933fecdae6a5b6ed677ef6ffc46010782b0005999e925e121be  sections/08-fields.tex
f1883295ee64b7b75e17d2c86d26202169f852741934095a4efcff718d900fb0  sections/01-models.tex
e38150a05d990980800c9e29724c6dcbe011932167b8331ff7ad88fffbe6b6b1  sections/10-recourse.tex
6ba31da31c905495c68e575ea27c914efd82dae83b7796857d611530dafe0059  appendices/L-further-arithmetic.tex
2c80891cd1066932e70d88f6978d0e78df66a336468170c9842da98c9158e65a  evidence/reviews/opus-wholepaper-r2.md
```

## Targeted checks and limits

Actual checks were scoped cat, nl -ba/sed reads, rg scans of the edited
passages, and sha256sum of the named sources and report. The arithmetic
above was reconstructed by hand. A targeted wording scan confirmed the
removed finite-rank diagnostic references are absent from 00/08; its only
remaining matched n=2 text concerned an unrelated degree range.

I also refreshed only the bibliography status and postreview layout note
in integration-r2.md as separately requested. All six previously missing
L bibliography keys are present at the recorded refresh. J's two height
identities are unchanged on separate gathered rows, and References is added
to the contents. These are metadata and navigation/layout changes, not a
fresh proof review.

Both owned reports were checked with git diff --no-index --check /dev/null.
No whitespace diagnostic was printed; status 1 is the ordinary new-file
difference from /dev/null. No manuscript edits, source research, builds,
experiments, mathematical scripts, CAS, historical diagnostic reruns,
project-wide checks or CI inspection were performed. The literature record
and source consolidation remain in Luna's lane; the root's build and
submission-package checks are separate evidence. No result from those
lanes is claimed as a reviewer-run check here.
