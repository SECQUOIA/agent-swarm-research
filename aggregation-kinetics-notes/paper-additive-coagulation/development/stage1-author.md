# Stage 1 author record

Status: five independent manuscript reviews complete; accepted minor corrections implemented by a separate revision agent. Coordinator verification is complete; stage 1 is accepted. Date: 2026-09-07. See `reviews/stage1-round1/assessment.md` and `stage1-revision.md`.

## Deliverables

- `main.tex` and `references.bib`: plain article scaffold, shared notation, real primary references, no invented author or affiliation.
- `sections/model.tex`: measurable daughter kernel, finite-count mass-conserving weak solution, explicit sampling conventions, controlled clocks, sufficient well-posed solution class.
- `sections/fractional-moments.tex`: full sharp pair inequality proof, bounded-test passage, controlled normalized fractional-moment decay, critical weak limits, moving windows, robust nonstationarity criterion, and explicit limits of sharpness claims.
- `appendices/wellposedness.tex`: self-contained construction and stability proof.
- `Makefile`, `.gitignore`, `README.md`, and `development/COVERAGE.md`: build and stage/claim coverage records.

No later-stage mathematical section, abstract, introduction, or discussion has been drafted. They will be integrated after their assigned author/review cycles.

## Mathematical development beyond the notes

The previous existence note only constructed selfsimilar daughter laws by narrow compactness, assumed a finite second initial moment, and did not prove nonlinear uniqueness. The new appendix proves existence and uniqueness for arbitrary jointly measurable time- and parent-dependent daughter kernels under the same initial second-moment hypothesis, in the class with locally bounded second moments.

The crucial stability argument is for `w(x)=1+x`. For the difference `d=n-v` and mean background `mu=(n+v)/2`, retain its direct loss `a d` and majorize the signed cross loss by a positive kernel. The exact weighted cancellation is

`P* w(y) - a(y) w(y) = lambda [mbar + 2 M2bar + y(Nbar + 2 mbar)] + sigma`.

This requires only locally bounded second background moments. A direct Hahn-sign derivative in measure space would be unsafe for measurable moving daughter atoms. Instead, the appendix solves the loss by an integrating factor, forms a positive majorant `z >= |d|`, and uses its exact integrated weighted loss balance. The negative loss of `z` bounds that of `|d|`, giving Gronwall without a Banach-space derivative. All potentially unbounded gain/loss integrals are finite under the second-moment assumptions; the majorant's integrated loss is finite by Tonelli and the scalar killed-survival identity.

Existence first uses bounded coagulation kernels with finite third initial moment. Uniform second- and third-moment bounds give a weighted-variation cutoff error of order `1/r`. The stability estimate then gives a Cauchy sequence. Finally finite-third-moment truncations of finite-second-moment initial data converge by the same estimate with a uniform second-moment coefficient. Weighted-variation passage handles merely Borel daughter kernels directly and preserves mass without a boundary compactness argument.

This method closes the particular parent-kernel and uniqueness gaps needed here. It does not assert that the second moment is necessary, nor uniqueness among every possible finite-first-moment solution. The estimates outside the appendix retain their weaker conditional solution assumptions.

## Corrections and interpretation choices

- The daughter condition is concentration on `(0,x)`, written as zero measure of its complement. Topological support contained strictly in that open interval would accidentally exclude ordinary densities reaching arbitrarily close to the parent size.
- The identities hold for all `(t,x)`, after permissible choices at a common null set of times. This avoids exceptional sets depending on a moving parent population.
- Expected count two and conserved expected mass need not describe a complementary binary event. The deterministic framework allows the full expected-measure class; finite-particle stages must impose realizability explicitly.
- Total variation distance for probabilities is the supremum over sets, while the signed-measure variation norm has no factor one half.
- All sizes use one fixed reference unit, including logarithms and polynomial weights.
- “Sharp” applies to uniform instantaneous coefficients and prefactor-one bounds. It does not claim sharp late-time front speeds or sharp downstream coupling constants.
- A total-variation overlap consequence of normalized fractional decay is included explicitly; it follows from `min(1,q) <= q^p`.

## Sources examined

The author read the existing model, controlled, general log-coupling, critical moment, exact last-event, inverse-preparation, and consolidated report notes, and used the relevant existing review record to identify boundaries. The coverage map lists all later-stage result sources and independent reviews.

Primary pages/PDFs inspected for the foundations bibliography:

- Eduardo Cepeda, *Well-posedness for a coagulation multiple-fragmentation equation*, Differential and Integral Equations 27 (2014), 105–136; [arXiv version](https://arxiv.org/abs/1301.1934). The additive constant-selection setting with fixed relative-fragment laws satisfying its dislocation hypotheses is within its homogeneous-like framework. It is not cited as directly covering arbitrary measurable parent dependence or time controls.
- M. Deaconu, N. Fournier, E. Tanré, *A pure jump Markov process associated with Smoluchowski's coagulation equation*, Annals of Probability 30 (2002), 1763–1796; [author PDF](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). Cited for established mass-sampling representations in pure coagulation, not as proof of the present fragmentation theorem.

## Build

`make` completed successfully with PDFLaTeX/BibTeX and generated `main.pdf` (10 pages). The final log was checked for unresolved references/citations, LaTeX errors, and overfull boxes. The PDF is an intentionally incomplete stage draft; successful compilation is not mathematical verification.

## Questions the five reviewers should stress-test

1. The weak integrating-factor comparison, especially its use of the positive majorant's loss and absence of a Bochner derivative.
2. Cutoff construction, moment bounds, forcing estimates, and both weighted-variation limits.
3. The distinction between conditional finite-count/finite-mass estimates and the proved finite-second-moment existence/uniqueness class.
4. The sharp fractional pair calculus proof and the bounded-concave-truncation domination.
5. The daughter-law scope, probability-distance convention, and precise critical weak convergence statements.
