# October 2026 rewrite: review and validation record

Baseline: `a0b2eebe`. The user asked for a rewrite of the manuscript for
clear structure and plain language, a better account of prior work,
significance and potential impact, and correction of any verified scientific
issue. The mathematical results, proofs and assumptions of the baseline are
kept; the changes below are presentation, verified corrections and a few
small additions. These were internal reviews by research agents, not
external peer review.

## Process

1. **Pre-rewrite review.** Six section reviewers re-derived every statement
   in Sections 2–7 and the appendix. A citation reviewer checked every
   prior-work statement and the bibliography against the sources. A context
   search identified application and foundational literature. Two readers
   (an expert referee and a decomposition practitioner) assessed clarity and
   structure. Every substantive finding was verified independently: three
   verifiers for major findings (majority rule), one for minor findings.
   Eleven minor findings survived and one was rejected. No finding affected
   a theorem. All sixteen proposed citations were verified against the
   sources; fifteen are used.
2. **Rewrite.** Section writers followed a common brief with a fixed outline,
   notation table, terminology and an explicit list of allowed content
   changes. The lead integrated and tightened the text.
3. **Post-rewrite review.** Seven checkers compared each rewritten file with
   the baseline for lost content, unapproved claims and errors, and
   re-derived all new mathematics. A citation checker re-checked every
   citation. Two fresh readers assessed clarity, repetition and
   significance. Of 73 findings, 47 survived verification and 26 were
   rejected. The three major ones concerned summaries, not proofs: the
   abstract stated finite exactness for mixed-integer convex problems
   without its hypotheses and omitted the quadratic scope of the upper
   bounds, and a discussion lesson attributed a large least penalty to
   every nearly feasible improving assignment, which holds only for the
   zero-multiplier threshold unless a cheap point with an opposite residual
   exists. All 47 were corrected.
4. **Final check.** Three fresh readers re-checked the whole manuscript
   against the formal results, one verifier checked the statements added in
   the last pass, and one checker compared these records with the compiled
   manuscript. Sections 2–5 and Appendix B produced no findings. Ten
   findings survived verification, all corrected. The abstract now states
   the affine linking equalities and the convex objectives and affine
   residual maps that the upper bounds and the perturbation theorem need.
   Example 7.6 now proves that the order `K/epsilon` is also necessary for
   the grid sample, through a finite-grid quantile bound. The remaining
   fixes concern wording in the introduction and these records.

## Corrections to the baseline manuscript

- Theorems 4.2 and 5.1 now state that one coefficient works for both the
  infinity norm and the one-norm (the baseline said "either").
- The Basu–Roy locators were swapped: Theorem 3 is the bounded-component
  radius and Theorem 4 the component-meeting radius. The extra
  `bit(N!)` term is located in the proof of their Theorem 2.
- The symmetric variant's accuracy statement now requires `0 <= epsilon < 1`.
- The stable-set coNP statement now takes the integer threshold as input;
  for each fixed threshold the test is polynomial.
- Section 7.5: the baseline recipe "use `epsilon p_0` in the construction"
  is invalid because refining the grid can lower its feasibility
  probability. It is replaced by a transfer bound from continuous to grid
  feasibility, `Pr{G feasible} >= p_0 - 2mK/q`, and a recipe with
  `epsilon p_0/2` that gives conditional failure probability below
  `epsilon`.
- Bhardwaj et al. are described with the hypotheses of their theorems
  (bounded integer variables for MIQPs; boundedness or a recession
  condition for convex objectives).
- Corollary 5.4 no longer credits its whole `k = 0` case to prior work; the
  prior results cover native constraints linear in all variables.
- Bibliographic metadata were corrected (issue numbers, DOIs, the published
  venue of the Basu survey, series of two books).

## Additions

- Remark 3.5: a seed `a_1 >= 2^{-t}` gives `Omega(N 2^n)` bits, so the
  worst case of Theorem 4.2 is `N 2^{Theta(n)}`; the same family needs
  `Omega(N 2^k)` bits against `N^{O(k+1)}`.
- Section 3.4: the lower bound holds for every penalty function with at most
  linear growth near zero, including the squared penalty.
- Section 2: the relation of the thresholds to the exact penalty
  representations of Rockafellar–Wets (Example 11.58, Definition 11.60,
  Theorem 11.61, Example 11.62(b)), checked against the book text.
- Section 6: a formal calibration definition; Theorem 6.4(b) for the
  zero-multiplier threshold; Remarks 6.5–6.9 (two-sided and constant
  factors, factors `2^{N^{1-epsilon}}`, rescaling, weak hardness, and
  factor-two calibration with an exactness oracle).
- Introduction: where exact norm penalties are used and why the size of the
  coefficient matters, with verified citations; a results table; concrete
  magnitudes for the chain; organized related work. Discussion: lessons for
  choosing penalties, scope, and open questions.

## Not adopted

- The `|V|^{1-epsilon}` inapproximability of the stable-set family. It is a
  direct consequence of known hardness of approximating the stability
  number, but it would need new citations and adds nothing to the binary-box
  result. The text says only that this family is used for strong
  NP-hardness of exact computation.
- Moving the tail examples and the Gaussian variant to appendices.
- The Füllner–Sun–Rebennack 2024 preprint, Han–Mangasarian 1979 and
  Pietrzykowski 1969. The first is only a preprint and the motivation is
  covered by verified published sources; the content of the other two was
  not verified.

## Verification limits

The numbering of Theorems 28.2 (existence of a Kuhn–Tucker vector under a
Slater condition on the non-affine inequalities) and 28.3 (Kuhn–Tucker
conditions) of Rockafellar's *Convex Analysis* was not confirmed from an
accessible copy. These are the standard locators for these results. As in
earlier stages, the cited general algebraic and Gaussian theorems were not
re-derived. No literature search establishes priority.

## Targeted checks run by the lead

Run from `paper-exact-penalties/` on October 1, 2026:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: success,
  no LaTeX warnings, undefined references or overfull boxes in `main.log`.
- `python3 -B verification/check_lower_bound.py`: PASS, including 24 new
  seed-variant cases.
- `python3 -B verification/check_upper_bound.py`: PASS (unchanged script).
- `python3 -B verification/check_calibration_perturbation.py`: PASS,
  including 55 new grid feasibility-transfer cases and 12 new grid-quantile
  cases.

No project-wide verification was run, CI was not inspected, and Lean was
not rerun. CI handles project-wide verification.
