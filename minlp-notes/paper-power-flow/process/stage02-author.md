# Stage 2 author report

Status: complete draft ready for the required five independent reviews.
No stage-1 section or proof was edited. All edits are inside `paper-power-flow/`.

## Material written

`sections/03-ac.tex` supplies a complete AC input model, its rectangular
power equations, real-angle membership, equal-angle transfer, rational-data
winding counterexamples, a cycle-budget criterion and positive principal-window
hardness, and the rectangular bus-angle-box variant. Title, abstract,
README, bibliography, and coverage map reflect the written results.

The series sign convention was derived directly from `U conjugate(I)`, with
series admittance `g+ib` and bus shunt `h+it`. It gives
`P=h r²+sum[g(r²-H)-bD]`, `Q=-t r²+sum[-b(r²-H)-gD]`.
The model permits lossless lines for membership but uses positive conductances,
zero susceptances, and no shunts in hardness. No transformer generalization
is claimed. Angle limits apply to every line and are represented by exact
rational cosines, never approximations to angles in radians.

## Developments beyond transcription

1. Membership is extended to every rational cosine in `(-1,1]`. Positive
   magnitude variables make `H >= c r_i r_j` a valid unsquared polynomial
   test even when `c<0`. The determinant crossing test is independently
   proved using arguments in `[0,2pi)`, with negative- and positive-axis
   endpoints, coincident directions, and reversals treated in the proof.
   Antipodal directions are expressly excluded.
2. The real-lift criterion is proved using fundamental cycles. Its encoding
   uses only real quantified variables and Boolean combinations of polynomial
   comparisons. The polynomial-length accounting includes explicit cycles.
3. The principal-only obstruction is given with fully rational input data:
   for arbitrary fixed rational cosine below one, use rational positive active
   intervals containing the cycle power; for an explicit singleton example,
   the four-cycle has exactly P=2, Q=0, and c=0. Irrational cycle powers are
   not silently inserted into rational singleton intervals.
4. Every fundamental-cycle angle budget below `2pi` guarantees a real lift.
   Hence the strictly positive principal window with cosine `1-1/n²` supports
   the hardness transfer. Its encoding is polynomial and its cosine alphabet
   is explicitly not fixed. Padding to at least two buses uses the original
   magnitude and free-injection intervals.
5. All-zero reactive singleton intervals can be replaced by `[0,1]` without
   changing the hard feasible sets: purely resistive shunt-free networks have
   `sum Q_i=0`, so a common weak sign forces Q=0. The paper distinguishes this
   one-sided saturation from symmetric-tolerance robustness.
6. Bus-angle boxes include one reference per component. This fixes the
   rotational freedom and yields exactly the resistive voltage set in the
   rectangular coordinates, including isolated buses.

## Source checks and attribution

Read the relevant original result and reviews A/C, and the root's candidate
development note. Inspected the cached primary-source text of Dörfler et al.,
Eq. (1) and supplementary Lemma 2, and Lavaei--Low Appendix B Case 2.
The former is cited only for the oscillator equation and cohesive-angle
background; the manuscript does not import its printed global uniqueness
claim. The latter's discrete-phase reduction is not used in any proof or
claimed as an established equivalence. Full historical comparison belongs to
stage 4. Source retrieval provenance is already in `root-open-source-cache.json`.

## Verification performed

- `python3 checks/check_ac_exact.py`: PASS, exact rational arithmetic only.
  2,112 scaled non-antipodal pairs, including 768 arcs longer than pi/2;
  14,784 cosine comparisons; 177,168 cycles against a separately rotated cut,
  including 59,640 nonzero winding cycles; 648 direct complex-power expansions
  including positive/negative susceptance and shunts.
- Regressions include a long arc with unequal radii where the legacy
  `e_i+e_j` sign would be wrong, antipodal exclusion, the rational four-cycle,
  global reactive antisymmetry, and rational size-dependent cosine inputs.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`:
  PASS, 10 pages, no undefined references/citations or overfull/underfull boxes.
- Rendered and visually inspected page 7 containing the crossing formula,
  axis-case proof, cycle equation, and real-lift criterion; layout is legible.

Actual check and build outputs: `stage02-exact.log`, `stage02-build.log`.
The finite exact checks are regression evidence, not proofs of quantified
statements. The paper's analytic proofs carry those statements.

## Boundaries passed to later stages

No outstanding obligation is needed for the section's current theorems.
Stage 3 may add the proposed quantitative near-zero-Q estimate. Neither
symmetric positive-width reactive tolerance, a fixed positive principal-only
window for arbitrary-size graphs, nonzero-susceptance hardness, nor the
lossless fixed-magnitude complexity question is solved by this stage.
The paper does not assume that those broader research questions must be solved
for the stated exact-feasibility theorems to be complete.
