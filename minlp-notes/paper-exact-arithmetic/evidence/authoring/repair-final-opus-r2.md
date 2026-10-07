# Response to Opus whole-paper review R2

The completed review `reviews/opus-wholepaper-r2.md` found no mathematical
blocker and requested four final presentation repairs. This response covers
those repairs only; no theorem or proof was changed.

1. **Abstract cone scope (P2).** The abstract now explicitly fixes the
   integer dimension and the dimension of the span of the continuous
   Hessians of the squared cone residuals. It names second-order cone
   systems over one explicitly represented real number field. The
   introduction and Appendix L already define that span over the input
   field and charge the field representation.
2. **Unpublished rank diagnostics (P3).** References to finite rank
   computations were removed from Sections 00 and 08. The all-dimension
   stationary-space equality remains open. The proved dimension and
   product-independence statements and the conditional descent theorem
   are unchanged. No result or development was dropped, and no experiment
   was rerun.
3. **Quartic recourse implication (P3).** The introduction now names the
   hypothetical full-point guarantee as the premise, states its Las Vegas
   consequence explicitly and points to `rem:recourse-quartic`.
4. **Cone result versus unrestricted hardness (P3).** The introduction
   now refers to `rem:models-socp`, explains that Hessian span can grow
   with circuit size in the gate constructions, and distinguishes that
   unrestricted family from the theorem fixing both t and h.

The six uncited bibliography records do not print and need no manuscript
change. Prior R1 precision repairs and proof-family reviews remain accepted
by R2. The source researcher consolidated the already-cleared
Grigoriev–Pasechnik sampling, Dedieu–Malajovich–Shub isolated-count and
Bombieri–Gubler height conventions in `evidence/literature-review.md`, with
honest status for the standard textbook imports. The BG row also records
the height–Mahler normalization used in L and its elementary Gauss-norm
derivation, without claiming inspection of the full textbook. Root read
the final rows;
the report's SHA-256 is
`2bb82f75647aeffc4d69aa9fc50e4e5e9911996f6ef6609484f3c261cada927b`.
This source-record completion changes no mathematical statement or proof
and makes no new priority claim.

The scoped document checker passes with 27 TeX files, 658 labels, 1768
cross-references and 120 cited works, with zero errors. The two added
references are the explicit recourse and SOCP hardness connections above.

## Changed-source SHA-256 snapshot

```
491f90e98658426866e4755c8b3b5f4d84d85569f02e083241d5f2cdd4a7cca8  sections/abstract.tex
32a473010509ff4930f8dfa4d67fd1f1efdf014723c23fba142967a388f17f92  sections/00-introduction.tex
1c3b8d8123348933fecdae6a5b6ed677ef6ffc46010782b0005999e925e121be  sections/08-fields.tex
```
