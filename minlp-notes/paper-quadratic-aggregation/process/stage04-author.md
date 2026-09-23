# Stage 4 author report

Date: 2026-09-22. Status: authored, ready for the required five independent
reviews. Earlier repository reviews were read as context, not accepted in
place of this manuscript's staged review. No subagents were used by this
author.

## Deliverables

- `sections/05-gram-hyperplanes.tex`: sharp HHC threshold for the full Gram
  map with one scalar square; exact hyperplane image; singular Gram-factor
  attainment; explicit pair-rotation proof of the real trace interval;
  credited classical squared-fidelity identity and boundary proof; repeated
  block corollary and exact scope.
- `sections/06-infinite-aggregation.tex`: the three-inequality example for
  every replication count r>=2; complete good cone; a continuum of
  indispensable strict rays; finite impossibility for nonstrict good
  aggregations; open and closed hull formulas and finite semidefinite lifts;
  equality with the hull of the original compact closed system; countable
  dense sufficiency only in the nonstrict case; original-variable quadratic
  impossibility for both strict and nonstrict conjunctions; precise literature
  comparisons and the failure of homogeneous PDLC/smoothness/common-zero
  hypotheses.
- `main.tex` includes these two sections. `references.bib` has the associated
  primary-source references, distinguishing numbered preprint locators from
  journal metadata. `supplement/check_infinite_aggregation.py` and its README
  give a portable standard-library exact checker.

## Mathematical investigation and development

The old dimension thresholds r>=3k and r>=k+2 are superseded by the sharp
r>=k theorem for the full map. Every endpoint and interior trace value is
actually attained, including singular matrices. The exceptional scalar
square case k=r=1 is HHC but does not obey the general image formula.
Explicit rotations replace an appeal to connected orthogonal components:
for odd k rotate all but the least-singular-value axis, reach a nonpositive
trace, and negate factors to fill the other half of the interval.

The squared-fidelity step uses its classical product-of-traces infimum,
not the invalid assertion that the square of a concave function is
automatically concave. Both positive semidefinite arguments are regularized
in the boundary proof. The universal matrix result is presented as a
structural HHC formulation, without a new matrix-inequality priority claim.

The full multiplier cone was derived before using any exact aggregation
theorem. Replication of a negative leading eigenvalue excludes every
nonconvex leading block from the good class. The unique-ray witnesses
prove uncountable strict necessity even if all other rays are retained.
The closed finite-family obstruction uses a new point outside the closed
hull, obtained by perturbing the off-diagonal Gram entry; the strict
boundary witness alone would not suffice.

The r=2 open hull uses the published BDS aggregation theorem with all
hypotheses explicitly checked and the inspected v2 number. A direct
two-point proof is retained for r>=3, together with a covariance proof of
necessity. The closed lift is proved closed by its explicit scalar formula,
not a general projection-closedness assertion. Mixing with the lifted
origin proves density; if the scalar remains 1/2, positive definiteness
allows its small increase. Compactness gives conv(T_r)=cl(conv(S_r)).

The root's proposed strengthening to arbitrary nonstrict quadratics was
independently validated and included. In the planar restriction, discard
identically zero polynomials only in the nonstrict case. A boundary arc
must be covered by zero sets of the remaining polynomials. The quartic's
irreducibility and the impossibility of vanishing on an arc are proved
using a nonsquare rational function, division in R(x)[y], and Gauss's
lemma. Real analyticity on a neighborhood of a compact parameter interval
then makes each nonzero quadratic's arc intersection finite. No claim
about arbitrary Boolean descriptions or lifted formulations is made.

## Literature and originality assessment

See `stage04-literature.md` and the consolidated literature record. The
newly inspected antecedents include Beck's 2009 global quadratic matrix
image theorems, in addition to Uhlmann's formula and rotation-image work.
The manuscript distinguishes the HHC/good-aggregation conjunction from
the older DMS infinite example by an explicit HHC counterexample and its
two negative leading eigenvalues. It distinguishes the DHW boxed equality
aggregation operation and the ball hypograph from this fixed-level hull.
Wang–Kılınç-Karzan's general QMP hull exactness already applies for r>=3.
No general first-infinite-aggregation, new SDP principle, or solver-speedup
claim is made. The narrow explicit-conjecture-resolution priority claim
uses “To the best of our knowledge.”

## Targeted verification actually run

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Passed; the integrated stage-4 manuscript has 25 pages. Final `main.log`
and `main.blg` were searched for Warning, Overfull, Underfull, and undefined:
no matches. Rendered PDF pages 13, 17, and 18 with `pdftoppm` and inspected
the displayed matrix formulas and quartic proof; no layout defect found.

From the repository root:

```sh
python3 paper-quadratic-aggregation/supplement/check_infinite_aggregation.py
```

Passed: 2,601 exact ray identities, six finite-family outside witnesses,
coordinate/interior slacks, and explicit prior-example image/inertia algebra.
After the root requested stronger regression value, trivial sampled
coefficient-sum checks were removed and the DMS midpoint test was rewritten
to compute the actual images and reconstruct the inconsistent squares and
product. The targeted checker was rerun after that change.

Finite checks do not prove HHC, infinite quantifiers, irreducibility, or
novelty. No project-wide verification, CI inspection, Lean build, or new
formal-certification claim was made. Concurrent formal supplement sections
and wrappers were preserved and remain outside this stage's scope.

## Next-stage boundary

Quantitative approximation/objective-specific exactness belong to stage 5;
the four-aggregation strict PDLC theorem to stage 6; full synthesis and
formal packaging to stage 7. They were not authored or implicitly accepted
here. The required five independent reviews of this completed stage remain
the coordinator's next step.
