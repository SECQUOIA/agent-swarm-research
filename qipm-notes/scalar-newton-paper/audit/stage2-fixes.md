# Stage 2 corrections

All seven accepted minor findings in `stage2-assessment.md` are resolved.
The corrections retain the intended parameter ranges and reductions; no
proved exponent or statistical factor changed. Work used the relocated
paper at `notes/scalar-newton-paper/`.

1. **Success, cost, and accuracy contracts.** The cost-model paragraph in
   `sections/02-models.tex` now states that classical and quantum lower
   bounds default to success at least two thirds on every promised input
   and worst-case query count. Explicit confidence and distributional
   expected-cost contracts override that default. In
   `sections/05-composition.tex`, Theorem `thm:path-product` explicitly
   requires relative error epsilon. This addresses reviewer 1 item 1,
   reviewer 2 item 1, reviewer 3 item 2, and reviewer 5 item 2.
2. **Coherent counting range.** Corollary `cor:coherent-counting` in
   `sections/04-lower-bounds.tex` explicitly requires kappa at least four
   and epsilon at most 1/128, in addition to its population bound. The
   preceding default supplies constant bounded error. This addresses
   reviewer 4 item 1 and reviewer 2's associated clarification.
3. **Every-oracle simulation.** Immediately before Proposition
   `prop:contrast`, `sections/05-composition.tex` defines an
   oracle-preserving realization by a uniform O(1)-hidden-query simulation
   of every granted sparse count/location/value, vector coordinate, norm,
   sampling, and constraint-factor request, with remaining data public.
   Both abstract compilers invoke this definition. The conditional compiler
   also explicitly retains identical public full-SQ metadata, as required
   for its direct sums. This addresses reviewer 1 item 2 and reviewer 4
   item 3.
4. **Nonconstant inner functions.** Both abstract compiler statements and
   the fixed-pair composition consequence now require nonconstant partial
   inner functions. Both fibers therefore exist when their distributions
   are invoked. This addresses reviewer 3 item 1.
5. **Rational sparsity base.** Proposition `prop:rational-clock` uses
   `max{4,(s-1)/8}` as its replacement base; the proof states both lower
   bounds on the chosen power-of-four gate size. This keeps the displayed
   lower bound informative at s=9. This addresses reviewer 1 item 3 and
   reviewer 5 item 1.
6. **Chebyshev definitions.** The witness proof defines first- and
   second-kind Chebyshev polynomials by their trigonometric identities and
   continuous endpoint extensions, and distinguishes scalar polynomial U_j
   from matrix clock gate U_t by argument and context. This addresses
   reviewer 4 item 2.
7. **Normalized generator test.** The rational-generator paragraph now
   tests `a |[(mI+h Jhat)^(-1)]_(i,j)| > 9 tau/10`, explicitly specifies
   the endpoints or second/penultimate queried vertices, and gives the
   positive-entry version after absorbing the known public endpoint sign.
   It identifies this quantity as a normalized reciprocal entry rather
   than an unnormalized inverse entry. This addresses reviewer 5 item 3.

## Audit correction

The lead assessment initially claimed the qualified coherent numerical
comparison was absent from the delivered TeX. Direct inspection found it
already present immediately before the statistical subsection in
`04-lower-bounds.tex`, including q_* and the noncancellation/high-accuracy
qualifications. The lead confirmed this and withdrew the absence claim.
The paragraph is retained. The assessment, author record, and source map
now accurately say that it preserves a qualification already present in
the source note, rather than repairing a new source error. Stage 3a will
integrate and check this existing paragraph within the coherent-access
comparison.

## Validation

- The qipm interpreter ran `checks/check_lower_identities.py`: all 25
  witness Jacobi realizations and 25 constant paths passed.
- The qipm interpreter ran `scripts/verify_classical.py`: all residual,
  support/complex moment, variance witness, rejection-law, and arithmetic
  transfer diagnostics passed.
- A clean forced build used `conda run -n qipm --live-stream make clean`
  followed by `make -B` in the paper directory. It produced the 20-page
  staged PDF. The final LaTeX and BibTeX logs have no warnings, undefined
  references or citations, or overfull/underfull boxes.

Verdict: every accepted Stage 2 correction is addressed. No new major or
minor issue was identified during this correction pass.
