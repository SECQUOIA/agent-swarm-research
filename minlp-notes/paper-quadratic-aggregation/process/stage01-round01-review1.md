# Stage 1, round 1: independent review 1

Verdict: acceptable foundations after two minor citation-precision edits.
No major issue found in the reviewed files. Main proofs and consequences
are deliberately absent and were not assessed as missing deliverables.
After this review was completed, the coordinator reported concurrent new
frontier notes and formal files omitted from the initial inventory. That
separate inventory finding still requires resolution; this verdict does not
override it or assess the new frontier results.

## Major findings

None.

## Minor findings

1. `sections/01-setting.tex:105–106`: the cited BDS v2 Theorem 2.12 is
   expressly stated for `n >= 2`, whereas the surrounding manuscript starts
   with `n >= 1`. The diagonal-case sentence does not preserve that source
   qualification. This does not undermine the mathematics (the one-variable
   diagonal case is elementary), but it slightly overstates the exact cited
   theorem. Add “for n >= 2” to the attribution, or separately explain the
   one-variable extension if later coverage needs it.

2. `sections/01-setting.tex:126–129`: specify that Dey–Muñoz–Serrano's
   positive definite linear combination is of the **homogeneous matrices
   Q_i**, and preferably state `n >= 3` and proper-hull context. Their
   Theorem 2.4 has those hypotheses. The present generic description is
   broadly accurate, but the object of the PDLC assumption is ambiguous
   precisely where this manuscript will later distinguish PDLC of the
   quadratic blocks A_i from PDLC of Q_i. Suggested wording: “For three
   quadratic inequalities in dimension n >= 3 with proper hull,
   Dey, Muñoz, and Serrano obtain an aggregation description when the
   homogeneous matrices Q_i admit a positive definite real linear
   combination.” Keep the existing clarification about signed coefficients.

## Positive checks and scope assessment

- Checked BDS arXiv v2 Definition 2.1, Proposition 2.14, Theorem 2.12,
  Theorem 2.9, Lemma 5.2, and Conjecture 3.3 against its extracted full text.
  Also rendered and visually inspected PDF page 14 to verify the conjecture's
  inequality signs. The manuscript's conjecture is equivalent: under strict
  feasibility every nonzero nonnegative constant aggregation is negative,
  and `(A_lambda,b_lambda) != (0,0)` itself excludes the zero multiplier.
- The definition of HHC, the distinction between homogeneous and ordinary
  quadratic parts, the meaning of ordinary hull, and the `d >= 3` argument
  for HHC implying hidden convexity are correct.
- The good-aggregation definition and the stated BDS hull-description
  assumptions agree with the primary source. The separation from globally
  convex certificates is clear and incorporates the corrective audit.
- The easy direction of the certificate equivalence is correct: a nonconstant
  convex quadratic is unbounded above in at least one direction, so its
  negative sublevel set is proper and convex.
- Read the local DMS full text at its introduction and Theorem 2.4, including
  its explicit comparison to Yildiran. The broad two- and three-constraint
  attribution is sound subject to the precision edits above.
- Checked Blekherman–Dunbar's available preprint at Theorem 1.4 and its
  explicit relation to BDS Conjecture 3.2. The literature record correctly
  distinguishes this from Conjecture 3.3.
- Read the canonical note's setting/summary and the September 22 audit's
  aggregation corrections. The coverage map captures the canonical note's
  mathematics and marks proposed new investigations as unaccepted until
  their later review. No unsupported priority assertion appears in the
  current manuscript. Access limits are candidly recorded.

## Supplementary source lead (not a required correction)

The browser can currently extract an author-uploaded accepted-manuscript
full text of Yildiran at
https://www.researchgate.net/publication/220386378_Convex_hull_of_two_quadratic_constraints_is_an_LMI_set .
It states the strict-inequality convention and the at-most-two-aggregation
claim explicitly. This provides a possible primary-text followup beyond
the publisher abstract. The literature record's earlier statement that full
text was not obtained at the authoring stage is a historical access statement,
not an error.

## Checks actually run

- Read `PROCESS.md`, author report, coverage and literature records, all
  current `.tex` files, and `references.bib`.
- Targeted `rg` and `sed` searches of BDS v2 and BD v1 full-text extracts
  and the local DMS `fulltext.md`.
- `pdftoppm -f 14 -singlefile -scale-to 1800 -png /tmp/quadratic-paper-literature/bdsv2.pdf /tmp/stage01-review1-bds-page14`,
  followed by image inspection.
- `rg -n 'Warning|Overfull|Underfull|undefined' paper-quadratic-aggregation/build/main.log`:
  no matches in the author's final build log. I did not rebuild concurrently
  with other reviewers.
- Online primary-source search for Yildiran's strict-system result; publisher
  abstract URL open failed, while the author-uploaded full text was accessible.

No project-wide verification, CI inspection, manuscript edits, or other
reviewer-report reads were performed.
