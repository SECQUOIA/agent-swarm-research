# Stage 2, round 1: independent review 1

Verdict: accept stage 2. No major or minor mathematical, correspondence, or
clarity issue identified in the reviewed stage. Deferred consequences,
applications, frontier results, and final source packaging are not part of
this verdict.

## Major findings

None.

## Minor findings

None.

## Mathematical review

1. **AHC and supporting hyperplanes.** The unbounded-level and strictly
   increasing divergent-sequence formulations are equivalent by the stated
   recursion. The open-hull separation argument correctly obtains a strict
   support inequality without assuming the ordinary hull is closed. The
   common-negative-direction argument gives midpoint feasibility uniformly
   across the finite constraint family. The homogeneous hyperplane exclusion
   handles `t=0` separately and dehomogenizes correctly for either sign of t.

2. **Hyperplane certificate.** Separation from the open negative orthant
   needs no closedness of the quadratic image. Its multiplier is nonzero,
   nonnegative, and has positive coordinate sum; both the sign argument and
   zero separation level are correct. Substitution of `t=(alpha dot x)/s`
   gives exactly the displayed sweep inequality.

3. **Closed coefficient cone.** The support-reduction proof accommodates
   signed dependencies and zero generators. Minimum-ratio subtraction keeps
   all active weights nonnegative and removes at least one. The independent
   subfamily cone is closed in its closed span, hence in the ambient space;
   the finite-union argument is valid. There is no unjustified appeal to
   closedness of an arbitrary image of a closed cone.

4. **Constant elimination and normalization.** Strict feasibility gives
   `c_k < L(A_k,b_k)` with L continuous and linear. Replacing c by that upper
   bound increases the sweep expression because its coefficient is a square.
   A zero nonconstant pair contradicts the original sweep at x=alpha.
   Thus positive pair normalization is legitimate, remains in the actual
   coefficient cone, and admits a norm-one convergent subsequence. The
   normalized b and L terms are bounded and multiplied by vanishing powers
   of `1/s_k`; their limits vanish for each fixed x. A single coefficient
   subsequence is enough for all x. Symmetry and pointwise nonnegativity give
   PSD, while cone membership recovers actual nonnegative weights. No bound
   on `c_k/rho_k` or on normalized weight vectors is needed.

5. **Easy implication and dimensions.** Both a nonzero PSD quadratic part
   and a nonzero purely affine slope make the aggregate unbounded above,
   yielding a proper convex negative sublevel set. The argument indeed
   needs neither feasibility nor AHC. The one-constraint discussion is
   consistent, and Dines gives the asserted two-constraint specialization.

6. **Quantitative alternative.** The distance bound for two closed cones
   uses a compact nonempty unit section, with the zero-cone case treated
   separately. The PSD distance identity and its minimum-eigenvalue bound
   have the correct Frobenius factor and positive-part qualification.
   Under triviality, a nonzero pair has a strictly negative eigenvalue
   bounded by `-kappa*rho/sqrt(n)`. Discarding the negative constant term
   and bounding the mixed term has the correct inequality direction and
   yields `s <= 2 sqrt(n)||alpha||/kappa`. The alternative simplex limit
   provides eventual negativity of the constant by strict feasibility,
   so that the proposition applies. The claimed dependency and limitations
   of kappa are appropriate.

## Formal correspondence

Read the actual `Model`, `Headline`, `SweepBounds`, `LimitCompactness`,
`Coefficients`, `Hyperplanes`, `EasyDirection`, and `ConeGeometry` sources,
and checked the declarations in `ConeClosed` and `DefinitionsSequence`
against the coverage map. The theorem's input data, strict feasible set,
ordinary `convexHull`, nonnegative nonzero weights, PSD matrix and nonconstant
pair match the manuscript. The headline has precisely nonemptiness and AHC;
the HHC specialization is derived from those definitions. Separation weights,
cone closedness, and the nonzero limit are proved rather than assumed.

The formal limit uses the negative of the continuous functional supplied as
`q_A(x0)+2 b dot x0`; this is the same L used in the manuscript. The
entrywise and product maximum norms differ from the manuscript's Euclidean
choices but do not affect finite-dimensional compactness or the conclusion.
The formal uniform-separation lemma has at least the stated manuscript
scope. The exclusion of the spectral quantitative calculation from formal
coverage is accurate. The formal section appropriately distinguishes
kernel replay from an independent implementation and avoids claiming that
other manuscript mathematics or literature assertions are certified.

The wrapper includes setting, proof, and formal account and is independently
buildable as a LaTeX document. `FORMAL-VERIFICATION.md` candidly records the
later obligation to package portable Lean sources; that obligation is not
misrepresented as already fulfilled.

## Checks actually run

- Read `process/stage02-author.md`, the complete certificate and formal
  sections, relevant setting/macros, the formal wrapper and its README,
  topic-27 coverage, and `process/stage02-root-formal-check.md`.
- Targeted source reads and declaration searches in the Lean modules named
  above. No current reviewer reports were read.
- Read the root verification manifest and checked all 11 listed current
  Lean source SHA-256 hashes against it with Python: all matched.
- Inspected the author snapshot's structure and the recorded author/root
  verification scope. I did not rerun the already successful Lean checks.
- `rg -n 'Warning|Overfull|Underfull|undefined'` on both final LaTeX logs:
  no matches. No redundant concurrent LaTeX build was run.

No source edits, external search, numerical experiments, project-wide
verification, or CI inspection were performed. This report is the only
file authored by this reviewer during the stage-2 review.
