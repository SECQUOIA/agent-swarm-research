# Independent reader and editorial review

## Scope and verdict

This review assesses whether a journal reader can understand the statements,
their significance, the computational and output models, and the relation
between the main text and the proofs. It is not a new mathematical proof
audit, bibliography verification, or PDF layout inspection.

**Readability verdict: pass after the local repairs confirmed below.** No
mandatory editorial repair or material comprehension blocker remains in the
reviewed source. This verdict does not close the separately tracked
mathematical source-contract check in Appendix L or the final PDF inspection.

The manuscript has a coherent account of four outputs: values, points, exact
predicates, and exact descriptions or certificates. The introduction names a
central classification theorem, explains the ingredients needed to move
between these outputs, and connects the distinctions to exact optimization.
The models chapter makes the formats and convexity certificates explicit.
The technical chapters generally state both the positive result and its
limits before developing the construction. The discussion carries those
limits through to the proposed uses. I found no global comprehension
blocker and no reason to remove results or proofs because of the length.

Several local notation and scope ambiguities needed repair. They concern
which selector is hard, the ranges of summary claims, the meaning of a
certificate space, and interfaces in the recourse argument. The repairs
below preserve the results and the intended scope. I checked the actual
integrated wording rather than accepting planned changes.

## Material inspected

I read `evidence/BRIEF.md`, `evidence/INTEGRATION.md`, and the authoring
`CONVENTIONS.md`, `DECISIONS.md`, and `INTEGRATION.md`; `main.tex` and
`macros.tex`; the actual abstract and all main chapters 00–11; and the
opening guides of Appendices A–K. I subsequently read actual Appendix L
through its final scope discussion when it became available.

Representative difficult proof passages were also read for presentation:

- Appendix A: sign compilation, magnitude bounds, compression, and refinement.
- Appendix C: the global error modulus, coefficient rows, Bregman estimate,
  residual conversion, and optimal-slice argument.
- Appendix E: the finite residual and positive-dimensional base-locus routes
  to the sharp five-variable degree bound.
- Appendix H: finite radial order, including the imported positivity
  interface, sphere ring, ideal, states, and dehomogenization.
- Appendix I: accepted completion, rejection probability, same-selector
  fallback, work bound, and the value-certificate and quartic-boundary passages.
- Appendix J: recovery of one common field from approximation and the degree,
  height, recognition, and coordinate-extraction interfaces.
- Appendix L: the weak-quadratic model, sampling consequence, finite-infimum
  and attainment distinction, NP-oracle output, selected-field cone model,
  projection/radius/gap/rational-lift chain, common-field witness, and known
  threshold corollaries.

A read-only helper independently reviewed Chapters 05–10; its observations
were checked against the actual source before being reported. The review
used targeted text inspection only. No builds, mathematical scripts,
experiments, project-wide verification, CI inspection, source discovery,
or literature-KB mutation were performed.

## Structure, contribution statements, and prior work

The central theorem hierarchy is understandable. The quartic PosSLP
classification is identified as central; effective selector approximation,
constraints and integer selection, output length, coefficient fields,
certificate formats, and recourse are presented as distinct related results.
The summary table helps a reader locate the hypothesis, output, and formal
statement. The supporting appendices supply the longer arguments and state
external theorem contracts where those contracts matter.

The introduction distinguishes known convex-value approximation and known
error exponents from the effective constant and fixed-selector additions.
It does not claim novelty for ordinary sign compilation, Newton iteration,
classical positivity results, or established certificate formats. The
comparison with the convex-value paper specifies a version. The additions
in Appendix L are attributed to their sampling and fixed-dimensional
integer ingredients rather than presented as new nonconvex optimization
algorithms. I found no blanket priority claim or unsupported assertion of
novelty in the prose reviewed. Verification of the cited source contracts
and complete citation metadata belongs to the separate literature review.

The manuscript consistently distinguishes ordinary polynomial time,
PosSLP reduction, Las Vegas expected work, and parameterized time. It also
distinguishes convexity promises from checked certificates, equality upper
bounds from order completeness, and exponential dependence on dimension
from exponential dependence on total input length. The main chapters
separate Hessian Grams, polynomial Grams, moment/exposing matrices, and
coefficient fields. These distinctions are essential and should be retained.

The long proofs inspected usually explain their purpose before giving
their estimates and use named stages to expose dependencies. An expert
reader with the indicated algebraic or optimization background can follow
them without repository notes. I found no distracting account of agent
work, review history, or repository development in the manuscript prose,
and no pattern of empty promotional or formulaic language needing a broad
rewrite. Repetition of hypotheses in the overview and formal statements
helps navigation; no general compression recommendation follows from this
review.

## Local repairs confirmed in the source

1. **Chapter 02, the concluding selector comparison.** The hard output is
   now called “the minimum-norm selector at accuracy $1/4$,” and the next
   sentence says “Requiring minimum norm strengthens the output contract.”
   This preserves the fact that the easy selector in the example is also
   fixed across precisions.
2. **Chapter 05, the few-nonlinear-directions theorem and Appendix D.** The
   affine-chart offset is now `\bar c`; the separation constant remains
   `c_0`. This removes a change of meaning inside one proof.
3. **Appendix D, rational-circuit equality.** The opening now states that
   equality holds exactly when both strict-sign tests return false.
4. **Chapter 06, degree overview.** The summary now includes $n\ge3$ for
   $2^n-3$ and $n\ge4$ for $2^n-5$, matching the formal theorem.
5. **Chapter 07, interior-Gram determinant explanation.** The minimum
   `m_k=\min h_k` and the Rayleigh quotient at a minimizer `a` replace the
   ambiguous reuse of `p`.
6. **Chapter 08, compact tower certificates.** The setup now calls the
   rational-weight expression a signed decomposition and identifies the
   coefficient of `r_{k,3}^2` as $-1$. It cannot be mistaken for the rational
   SOS whose existence the chapter excludes.
7. **Chapter 10, lattice application.** The text now applies the lemma to
   `a_F(\gamma)` after substituting certified endpoints, and includes the
   endpoint tests only for the provisionally free coordinates.
8. **Chapter 10, certified completion.** The theorem now defines `b` as an
   approximation in the certified face with endpoints imposed exactly and
   identifies the positive regularization parameter `\tau`.
9. **Chapter 10, output scope.** The conclusion now distinguishes exact
   internal core-face and margin certificates on accepted draws from the
   point/value approximation output, which does not supply all active labels.
10. **Appendix L, opening.** The reference to the physically preceding
    appendix was replaced by the intended explicit reference to Appendix J.
11. **Final framing of Appendix L.** The introduction's cone paragraph and
    table row, and both discussion uses, now specify the continuous Hessians
    of the squared cone residuals. The nonconvex quadratic summary retains
    its distinct constraint-Hessian definition. I checked the actual revised
    wording against Appendix L.
12. **Chapter 09, opening.** The positivity condition now identifies the
    homogeneous quadratic part of a quadratic in the square-factor span,
    allowing the affine terms required by the theorem. The word order also
    makes the span membership unambiguous.
13. **Chapter 09, short-denominator comparison.** The comparison now includes
    the corollary's scale range `\lambda\ge\lambda'_k`.
14. **Chapter 09, prescribed radial multipliers.** The opening now prescribes
    a hierarchy for a scaling family and states that no fixed order suffices;
    it no longer calls the varying quartic fixed.
15. **Chapter 09, block theorem.** The last item now explicitly concerns a
    positive semidefinite full Hessian Gram matrix.
16. **Chapter 10, finite-law transfer.** The constant `C` is now identified
    as the base-computable format bound from Appendix I, of size
    `2^{\poly(L)}`, independent of precision and sampled coefficient heights.
17. **Chapter 08, computed rational spaces.** The overview now names the
    rational quadratic relations, their product span, and the rational
    quartics with zero value and gradient. The subsection title and opening
    use the same terminology and identify the subsequent positive
    semidefinite test. They no longer call the full linear spaces
    certificate spaces.

## Final alignment and review limits

The abstract, introduction, models, and discussion have been checked against
actual Appendix L. Their output and complexity statements are aligned:
short nonconvex witnesses and NP-oracle output are distinct from ordinary
fixed-parameter cone algorithms; unattained finite infima do not promise a
feasible limiting point; nonunique nonconvex minimum-norm optimizers are
not called canonical; the mixed-integer cone witness is constructed in a
chosen continuous fiber; and threshold recovery uses a supplied exact value.

No unresolved journal-quality presentation repair remains from this review.
I do not recommend further changes merely to shorten the paper or vary its
terminology. Citation completion, the separately tracked Appendix L
Khachiyan–Porkolab radius source-contract repair, and final PDF inspection
remain separate integration tasks. The source-contract gate was reported by
the mathematical/literature reviewers; this reader review does not certify
its formula or treat it as a newly discovered readability defect.

## Source snapshot at final reader check

SHA-256 hashes below identify the actual integrated framing and locally
revised passages inspected. Appendix L was still awaiting the separately
tracked radius-source repair at this snapshot; a later mathematical repair
will change its hash.

```text
d4a8f2ff59b5037342a6acf11cc6faf80ee475c81bac1da4a0a80ae212a64859  sections/abstract.tex
0eae61605aca53bf38ba9b8ba845ec790a495ef55d2cc6d2d5c6d864a08e36a4  sections/00-introduction.tex
f1883295ee64b7b75e17d2c86d26202169f852741934095a4efcff718d900fb0  sections/01-models.tex
9255c3b578fbef9981d96873db3effe3a0f65345fcab796bbed3e16d1f88e010  sections/02-points.tex
0216cf2456eb982b40ea206dcb9f0fe4739eefd9b7b029d7b786b38a9599dc9e  sections/05-constraints.tex
b77ad09a3ad16a891f33eade8dc34cd3417a64cd3a88b8f565a1d5ee139469bb  sections/06-algebraic.tex
2cfaf3f0c8a4e6c144f3fb8b241bcdcba7a3683167c55adac4ea641a8090bbe1  sections/07-heights.tex
b05a1d5d0323344ce05eb679f4ac8651dca7cdea96360f5bdb549aeb46e4324e  sections/08-fields.tex
200313954066e5071cf3a25ec9d0f5c7a28e252b375297f2b9ec5a0515165c98  sections/09-certificates.tex
e38150a05d990980800c9e29724c6dcbe011932167b8331ff7ad88fffbe6b6b1  sections/10-recourse.tex
63252f4d6614dca06df90fa9476a6408ed6f8fb43eaeae9000ec77d0fec97440  sections/11-discussion.tex
3e7a43c5d884a915d99d0e9f46026d0d77ef1403ec04ab0157c4da03b194130e  appendices/D-constraints.tex
02b04f22e1a1b89380a06c55902dcefb37a8d766f1f26f7ed3e6bc322087f0f8  appendices/L-further-arithmetic.tex
```
