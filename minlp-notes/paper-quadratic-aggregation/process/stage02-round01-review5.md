# Stage 2, round 1: independent review 5

Verdict: pass. No major or minor correction required. I found no mathematical
gap in the main theorem, the direct proof, or the quantitative alternative.
The formal account accurately limits what was checked. This verdict does not
extend to the later-stage consequences, applications, or frontier results.

## Mathematical review

Read the complete new certificate section independently of the formal-status
claim. The following potentially fragile steps are justified:

- AHC's arbitrarily-large-level definition gives a single increasing sequence
  tending to infinity, and HHC implies it in every stated positive dimension.
- A common strict negative leading direction gives feasible points on both
  sides of every candidate midpoint. Finiteness of the system supplies a
  common sufficiently large radius. The lemma does not make an incorrect
  recession-cone claim.
- The hull of the nonempty open system is open, and separation from an exterior
  point gives a nonzero supporting normal with strict inequality on the hull.
  The exclusion of sweeping hyperplanes handles t = 0 separately and uses
  t squared for either sign of nonzero t.
- Hyperplane-image separation needs no closedness: the negative orthant is
  open. Its unbounded coordinates force the separator weights nonnegative;
  zero in the image and the orthant supremum force separator level zero.
  Normalization is valid because the nonzero nonnegative vector has positive
  coordinate sum.
- The finite-cone proof correctly removes dependencies from active generators,
  including relations with coefficients of mixed signs. Independent-generator
  cones are closed in their closed spans; their finite union is closed. This
  does not rely on the false general assertion that linear images preserve
  closedness.
- Strict feasibility bounds the constant above by a fixed linear functional
  of the coefficient pair. Since its multiplier in the sweep inequality is
  a square, replacement by this upper bound has the correct inequality
  direction. The original inequality rules out a zero pair before division.
- The normalized pairs lie in a compact unit section of the actual cone.
  One coefficient subsequence suffices for every quadratic evaluation. The
  perturbations vanish on that subsequence without any lower bound on the
  pair norm or any bound on the original constant divided by that norm.
  Closedness recovers actual nonnegative weights for a nonzero PSD limit.
- Both easy-direction cases are proved, including a purely affine aggregate.
  This implication also holds for an empty strict system, as claimed.
- The uniform-separation lemma is valid for the stated closed, potentially
  nonconvex cones. Its compact-sphere and scaling argument includes the zero
  cone. The PSD-distance identity and min-eigenvalue estimate have the correct
  sign and square-root dimension factor.
- Under triviality of every PSD certificate, P intersects the PSD cylinder
  only at zero. With a negative aggregate constant, the eigenvector evaluation
  gives exactly s <= 2 sqrt(n) norm(alpha) / kappa. The simplex-limit argument
  makes the constants eventually negative using nonemptiness; it does not
  assume negativity prematurely. This completes the alternative contradiction.
- The remarks about one normal, one constraint, and two constraints are
  consistent with the theorem. No step silently requires n >= 3 or m >= 2.

The exposition provides the needed intermediate arguments rather than merely
referring to internal notes. The second proof is distinguishable by its
quantitative bound and is explicitly not advertised as an additional novelty.

## Formal scope and evidence

Read the formal section, stage author report, author snapshot, coordinator
check report, manifest, supplement wrapper, and packaging obligation. Spot
checked actual Lean semantics and interfaces in `Model.lean`,
`Headline.lean`, `LimitCompactness.lean`, `ConeClosed.lean`, and
`Coefficients.lean`. The strict feasible set, ordinary convex hull, real finite
coefficients, matrix symmetry, nontrivial certificate, HHC kernels, AHC levels,
and headline assumptions agree with the manuscript. The general limit lemma
returns a single norm-one point with every quadratic evaluation nonnegative;
the headline instantiates its closed-cone premises using proved properties.

The account expressly excludes the spectral quantitative alternative and all
later consequences from formal scope. It correctly distinguishes kernel replay
from an independently implemented proof assistant and defers portable-source
packaging to stage 5. The current mathematical paper builds without those
external Lean sources. I did not independently rerun Lean or audit every
declaration implementation, and do not imply that I did.

## Targeted checks actually run

- A Python SHA-256 comparison checked all 22 entries in
  `process/stage02-author-snapshot.json`: no missing files or mismatches.
- A Python scan of the saved main and supplement LaTeX logs found no warning,
  undefined-reference, or overfull/underfull messages; both saved builds report
  seven pages. I did not rerun LaTeX.
- Inspected the coordinator's saved manifest and axiom-audit output. The latter
  ends with `PASS: audited 178 topic-27 declarations across 11 modules.` All
  eleven named kernel-log files are present. Their successful outcomes are
  supported by the coordinator's completed runner record; mere file presence
  alone is not used as verification.
- No project-wide command, CI inspection, numerical experiment, subagent, or
  new literature-priority assertion was used. Did not read other stage 2
  reviewer reports or change manuscript sources.
