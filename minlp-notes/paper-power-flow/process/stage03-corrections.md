# Stage 3, round 1 corrections

Completed by the separate correction agent after reading the root assessment,
root repair guidance, all five independent reports, original Toolbox proof
and gate displays, reviewer-1 diagnostics, and the cached primary Ohmoto–Shiota
triangulation paper. Ready for a fresh frozen five-reviewer round; not accepted.

## Accepted major M1: repaired

- Section 05 now proves the sharp characterization: among compact
  semialgebraic sets over Q, precisely the basic closed sets are rationally
  equivalent to RPF voltage sets. All simultaneous graph restrictions survive.
- Necessity is proved by compact lower bounds on forward and composed inverse
  denominators and positive denominator clearing. The explicit compact
  three-quadrant obstruction has a self-contained leading-form proof.
- General compact semialgebraic topology survives through finite triangulation
  and the basic closed rational standard-simplex realization using nonface
  equations. The map is semialgebraic, with no rationality or polynomial-size
  triangulation claim. Ohmoto–Shiota v2, p.2, Theorem 1.1 and Section 1.2 were
  checked in the cached primary source; its bibliography entry was added.
- Appendix A proves the restricted arithmetic lemma independently. Unique
  polynomial circuit evaluation is followed by a sufficiently small dyadic
  scaling and an explicit halving chain. The fixed delta is encoded with
  `(1+delta)+(1-delta)=2` and midpoint constants. Shifted addition/product,
  multiplication from squares, and squares from reciprocals are explicit,
  with analytic identities. Continuity at strictly interior base values gives
  all range choices without the source's defective range lemma or center list.
  Both map directions, uniqueness, and designated affine recovery are proved.
  No arbitrary-scaling complexity bound is asserted.
- The singleton algebraic-degree theorem now depends on this proved lemma;
  its designated-coordinate field conclusion and structural claims survive.
- The appendix explains the source's inactive-branch failure precisely and
  distinguishes preserving existence from preserving a rational bijection.
- Abstract, README, bibliography, and coverage were updated. Accepted sections
  01–03 and the structural section were not edited.

## Accepted minor m1: corrected

The residual proof describes D's one complemented x copy of weight two and
one complemented y copy of weight one. The epsilon + 3 delta estimate and all
subsequent constants are unchanged.

## Actual verification

- New standard-library `checks/check_arithmetic_exact.py` passed: 1,681
  composed multiplication/reciprocal profiles; a full scaled/shifted disk
  circuit with 332 variables and 330 actual final addition/inversion equations
  on 49 valid, 72 outside, and 49 inconsistent profiles; nine dyadic constant
  chains including k=0; and 35 standard-simplex support profiles. Every final
  equation and bound is checked. Log:
  `verification/stage03-corrections-arithmetic.log`.
- All three existing exact checkers passed. Logs:
  `verification/stage03-corrections-resistive.log`,
  `verification/stage03-corrections-ac.log`, and
  `verification/stage03-corrections-developments.log`.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`
  succeeds with a 24-page PDF and no final warnings, undefined references or
  citations, or overfull/underfull boxes. Log:
  `verification/stage03-corrections-build.log`.
- The dense appendix gate page was rendered and visually inspected; equations
  are legible without clipping or overlap. Artifact:
  `verification/stage03-corrections-page22.png`. Extracted layout:
  `verification/stage03-corrections-layout.txt`.
- Fresh original-PDF Toolbox pp.6–8 extraction is saved at
  `verification/stage03-corrections-toolbox-p6-8.txt`; the printed Boolean
  substitutions and claimed projection bijection match the counterexample.

Finite checks support the analytic proofs; they do not certify universality,
compactness/continuity, triangulation, or the sharp obstruction. No accepted
finding remains unresolved in this correction version. The required repeat
five-reviewer round must still be adjudicated by the root.
