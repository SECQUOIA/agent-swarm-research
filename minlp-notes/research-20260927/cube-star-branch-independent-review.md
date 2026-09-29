# Independent review of the strict cube classification

Reviewed on 2026-09-27 by `/root/frontier_cube/four_star_route` against
[the classification note](cube-strict-extreme-classification.md) and the
[earlier family's exposed-ray proof](../research-20260925/three-positive-disjoint-counterexample.md).
No substantive defect was found in the stated restricted theorem. This is
an independent proof review, not a literature-priority assessment.

The strict hypotheses do the work claimed. A minimum in a face with at least
two free coordinates requires a positive semidefinite principal Hessian,
which a negative two-by-two principal determinant excludes. Thus checking
all edges and vertices certifies nonnegativity for every sufficiently small
perturbation that retains these strict Hessian conditions. The rank argument
does not overlook inward derivatives at edge contacts: even if a perturbation
changes such derivatives, a negative global minimum would still have to occur
on an edge or vertex.

At each interior edge zero, vanishing value and tangential derivative give
two homogeneous linear conditions on a perturbation. With at most four
contacts their common kernel has dimension at least two in the ten-dimensional
space of quadratics. The original polynomial lies in that kernel. An independent
element therefore gives two nonproportional feasible perturbations: contact
edge restrictions retain their squared factor and positive curvature, and
the finitely many other edges retain a strictly positive minimum. This proves
the claimed necessity of at least five contacts without assuming independence
of the contact equations.

The two elementary exclusions are valid. Three edges on one face force
the relevant mixed entry to be `d2*(2*h-d1)`, whose absolute value is strictly
less than `d1*d2`. For a three-edge star, the chord between two axis zeros
forces every square-correction coefficient to be nonnegative; the strict
minor assumption makes it positive. This excludes all other edge contacts.

I independently enumerated all graph automorphisms by testing permutations
of the eight vertices against the twelve literal edges in the note. This
gives 48 automorphisms and reproduces every one of the 24 listed orbit
representatives. The author's checker separately verifies each slack identity
and every forced-face disposition. The surviving six-cycle is correctly
treated as feasible and nonextreme: its recovered polynomial is an affine
square plus a positive multiple of the nonnegative triangle polynomial.
These two summands have different constant terms and cannot be proportional.

For the family orbit, I rederived the coefficient equations from the three
vertical tangencies. The bottom contacts imply `h < min(d1,d2)`, hence
`D = d1+d2-h > 0`. Positivity of the third contact parameter gives `D+k > 0`.
The chord and strict minor imply `k*(2*D+k) > 0`; together these exclude
`k < -2*D` and force `k > 0`. Its interior location gives `D+k < d3`.
The earlier proof that the five evaluations expose the family ray also
handles a zero coefficient multiplier and is valid under these restrictions.

The note appropriately limits completeness to extreme rays satisfying every
strict assumption. It does not classify vertex-contact or semidefinite-face
cases, nor prove that arbitrary strict-regime polynomials decompose into
extreme rays still in that regime. It therefore does not establish completeness
of the proposed cube relaxation.

Targeted commands actually run:

```sh
python research-20260927/check_cube_strict_extreme_classification.py
python research-20260927/check_cube_classification_review.py
```

Both passed. The second check independently reproduces the orbit table and
symbolically verifies the family and six-cycle contact values and tangential
derivatives. Neither check formalizes the local perturbation argument, proves
novelty, or covers the excluded regimes. No project-wide or CI checks were run.
