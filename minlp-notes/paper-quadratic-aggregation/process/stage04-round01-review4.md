# Stage 4, round 1: independent review 4

Date: 2026-09-22. I independently read both new sections, the exact checker
and README, author/literature/snapshot records, coverage update, and added
bibliography. I did not read another current report or edit manuscript sources.

## Verdict

Accept the present stage 4 mathematics. No major or minor correctness issue
identified. One immediate optional strengthening is given below; it is not
needed to make the current statements true. Accuracy, PDLC, and portable formal
integration remain outside this review.

## Arbitrary-quadratic obstruction: detailed audit

The planar substitution uses two orthogonal coordinates available already when
`r=2`. It gives `h=0`, so the hull formula is exactly the ball-coordinate bounds
together with `(1-x^2)(1-y^2) > 1/4`, or its nonstrict counterpart. Squaring
introduces no extraneous branch because both factors are constrained nonnegative.

The chosen graph arc has positive radicand strictly below one on an open
neighborhood of its compact parameter interval. The derivative of the defining
quartic in the y direction is nonzero along the arc, so both feasible and
infeasible planar points occur arbitrarily near every arc point.

The rational function `(3/4-x^2)/(1-x^2)` has distinct simple real zeros and
poles; no cancellation occurs. It is not a square in `R(x)`. Hence the monic
quadratic in y is irreducible over that field. If the remainder after division
of a proposed quadratic restriction has nonzero y coefficient, one may avoid
its finitely many poles/zeros on a subinterval and recover a rational square
root, a contradiction. If its y coefficient vanishes, identical vanishing
along the arc forces the constant remainder to vanish too.

The quartic is primitive over `R[x]`: its two nonzero y coefficients sum to
the nonzero constant `-1/4`, so they are coprime. Gauss's lemma validly carries
irreducibility and divisibility back to `R[x,y]`. A degree-four polynomial
cannot divide a nonzero polynomial of total degree at most two. Therefore no
nonzero quadratic restriction vanishes on an arc segment. Its composition
with the analytic graph extends past both endpoints of the compact interval;
infinitely many zeros there would give an interior accumulation point for
analytic continuation. The claimed finite-zero conclusion is justified.

For strict descriptions, origin feasibility rules out identically zero planar
restrictions. Continuity from feasible points makes every restriction nonpositive
on the boundary arc; exclusion of an arc point forces at least one to be zero.
For nonstrict descriptions, identically zero restrictions must instead be
discarded, exactly as the proof does. Finitely many remaining strict negatives
would persist on a planar neighborhood and contradict the boundary property.
The proof handles even the case with no remaining restrictions. Thus the
finite-cover contradiction works for both claimed formulations, without relying
on convexity, aggregation membership, or smoothness of the candidate quadratics.

### Optional strengthening

The strict part of Theorem `thm:no-finite-quadratics` actually excludes any
**countable** family of arbitrary quadratic inequalities. Exclusion of a boundary
point from an arbitrary strict intersection still requires at least one
restriction to attain zero there. Each nonzero restriction has finitely many
arc zeros, and a countable union of finite sets cannot cover the uncountable
arc. Thus every exact strict description by original-variable quadratics must
use uncountably many inequalities. This improves the existing arbitrary-quadratic
statement at essentially no proof cost and strengthens the parallel good-ray
result. The nonstrict conclusion should remain finite: its neighborhood
argument uses finiteness, and countable dense nonstrict aggregations suffice.
I flag this as an optional mathematical improvement rather than an error.

## Other proofs challenged

- The Gram-fiber factorization extends orthonormal rows in singular cases
  because `r>=k`. The rectangular SVD gives the stated maximum, including
  scalar and zero cases. Pair rotations attain the full trace interval for
  even k; for odd k>=3 the endpoint `2*s_min-M` is nonpositive, and negation
  fills the other half. The scalar square exception is correctly isolated.
- The fidelity Cauchy--Schwarz factors have the correct order. The positive
  definite equality witness satisfies `ZGZ=H`; regularizing both PSD inputs
  proves the boundary formula without assuming an attained infimum there.
  The infimum is linear in G for each fixed positive definite Z, so the
  separate-concavity conclusion is legitimate. This is not an invalid use of
  squaring a concave function.
- The exact hyperplane image is the hypograph of that concave function over
  the PSD cone. Its exceptional `(k,r)=(1,1)` line image and its `r<k` rank
  obstruction are both correct. The corollary preserves only linear output
  maps and does not silently add mixed `tX` terms.
- The repeated block inertia proves the exact good cone for `r>=2`.
  Nonzero PSD-block multipliers have a strictly negative scalar block and
  their convex strict inequalities hold on every finite convex combination.
- The Gram witnesses are positive definite uniformly over `[1,2]`; AM--GM
  yields equality on exactly the claimed positive ray. The finite closed-family
  obstruction correctly perturbs the Gram off-diagonal to produce an exterior
  point, rather than trying to exclude a closed-hull boundary point.
- The open hull invokes BDS only after checking all its dimensional and
  feasibility hypotheses. Cone generation, minimizing the ray expression,
  strict and nonstrict Schur complements, lift mixing, and compactness of
  `conv(T_r)` establish the two hull formulas. Projection closedness follows
  from the explicit scalar formula rather than an invalid general principle.
  Dense countable rays work for nonstrict inequalities, including p or q zero.
- The direct midpoint proof explicitly retains its `r>=3` restriction, while
  the HHC/BDS route covers r=2. The covariance necessity proof has the strict
  variance inequalities needed for its final strict bound.
- The DMS comparison computes the actual failed HHC image and the two negative
  leading eigenvalues. Homogeneous PDLC failure, determinant multiplicity,
  and a common projective zero are established algebraically for this example.

## Literature and reproducibility

I checked Beck 2009 Theorems 3.1/3.4 in the retrieved primary text and the
relevant BDS/BD theorem locators. The manuscript's distinctions match their
stated hypotheses. I also independently opened
[Wang--Kılınç-Karzan v2, Section 4.1](https://arxiv.org/html/2403.04752v2):
its replication-count criterion supports the cited r>=3 closed-hull comparison.
The record distinguishes classical matrix ingredients, inspected versions,
and bounded priority evidence. I found no unsupported broad novelty assertion.

The script uses rational Gram entries and verifies actual ray slacks,
finite-family perturbations, and the DMS image/inertia calculations. The
finite-family slack controls the perturbation with the correct factor two.
It accurately excludes HHC, irreducibility, infinite quantifiers, and novelty
from its checking claim. The supplement needs no external data.

## Targeted commands actually run

Source and literature reads used `cat`, `rg --files`, targeted `rg -n`, and
`sed -n` on the files identified above. From the paper directory:

```sh
python3 supplement/check_infinite_aggregation.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage04-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage04-review4/main.log /tmp/quadratic-stage04-review4/main.blg
```

The script passed 2,601 exact ray identities and six finite-family outside
witnesses plus its other stated algebra checks. The independent build passed
and produced 25 pages; final log and bibliography-log scans found no matches.
No project-wide test, CI inspection, formal rerun, or subagent was used.
