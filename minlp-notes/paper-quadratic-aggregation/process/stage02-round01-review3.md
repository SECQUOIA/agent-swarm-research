# Stage 2, round 1: independent review 3

Date: 2026-09-22. Scope: the complete certificate theorem, both written
proof routes, mathematical coverage, assumption discipline, and the bounded
formal-verification account. Later-stage consequences and frontier results
are deliberately absent and were not required. I did not read other new
review reports, edit source, run global checks, inspect CI, or use subagents.

## Verdict

**Accept stage 2: no major or minor correction is required on this review.**
The main proof is complete, and the quantitative alternative is correct.
The formal account matches the inspected definitions and headline interfaces
without extending verification to the remaining manuscript.

## Mathematical review

1. **Exact assumptions and conclusion.** AHC's unbounded-level formulation
   is equivalent to the source's increasing-sequence formulation by the
   stated recursion. HHC implies AHC. The theorem uses finite positive
   dimensions, real symmetric data, strict nonemptiness, and AHC, with no
   hidden definiteness, image-closedness, rank, or Slater condition beyond
   the explicitly nonempty strict system. A nonzero coefficient pair
   automatically excludes the zero multiplier. The easy implication also
   holds if the strict system is empty, as correctly stated.

2. **Strict support and homogenization.** Openness of the ordinary hull
   follows from varying a positive-weight point in any finite convex
   combination. Separation gives a nonzero support normal, and openness
   makes the support inequality strict on the hull. The simultaneous
   strictly negative leading direction would express every target as a
   midpoint of feasible points. This correctly excludes the `t = 0` case
   of a swept hyperplane intersection. Dehomogenization divides by `t`
   through the `t²` identity, so no sign assumption on `t` is introduced.

3. **Hyperplane certificates.** The convex homogeneous image contains zero
   and misses the open negative orthant. Ordinary separation suffices:
   the separating functional is nonnegative because otherwise its values
   on that orthant are unbounded above. Its orthant supremum and its value
   at zero force the separating constant to zero. Normalization is legal
   because the weights are nonzero and nonnegative. The parameterization
   of the hyperplane requires and has `s != 0`. No closedness of the image
   is used.

4. **The actual coefficient cone is closed.** The finite-generator proof
   uses a dependence relation supported on the active generators, subtracts
   the maximal feasible positive multiple, and removes an active coefficient.
   It therefore reduces each conic representation to an independent
   subfamily. Each resulting cone is closed in its closed finite-dimensional
   span, and only finitely many such subfamilies exist. This avoids the
   false general rule that linear images of arbitrary closed cones are
   closed. Zero generators and the zero vector are covered.

5. **Constant elimination and normalization.** At a strict feasible point,
   the aggregate constant satisfies `c_k < L(A_k,b_k)`. Replacing `c_k`
   by that upper bound increases the sweep quadratic because the multiplier
   of `c_k` is a square. Nonnegativity is therefore preserved in exactly
   the needed direction. Before normalization, a zero coefficient pair
   would make `c_k < 0` and contradict the original sweep inequality at
   the nonzero support normal. The pair norm is consequently positive.

6. **The compactness passage.** Unit normalized coefficient pairs lie in
   the actual finite cone, whose unit section is compact. One subsequence
   converges in coefficient space to a norm-one pair. The cross term tends
   to zero, and the replacement constant term tends to zero because `L`
   is continuous and the sweep levels diverge. For every fixed vector the
   limiting quadratic value is nonnegative. The same coefficient limit
   works for all vectors; no invalid change of subsequence is made. Cone
   membership recovers genuine nonnegative original weights. Neither a
   limit of the weights nor boundedness of `c_k / rho_k` is needed.

7. **Easy implication and small cases.** A nonzero PSD quadratic part has
   a positive eigenvalue and gives an unbounded-above quadratic aggregate;
   a zero quadratic part with nonzero linear coefficient gives an
   unbounded-above affine aggregate. Their strict sublevel sets are proper
   and convex. The one-constraint discussion exhausts the possible leading
   forms, affine functions, and negative constants under strict feasibility.
   The two-form recovery is correctly identified as established theory.

8. **Quantitative alternative.** Closed cones meeting only at zero have
   positive distance on the compact unit section, without convexity. The
   PSD-cylinder distance is exactly the Frobenius norm of the negative
   eigenvalue part: diagonal truncation attains the lower bound, and the
   linear component is unchanged. The positive-part version of the minimum
   eigenvalue bound is valid for every symmetric matrix. Combining the
   bounds forces a negative eigenvalue at most `-kappa rho / sqrt(n)`.
   Evaluating the sweep inequality at its unit eigenvector and dropping
   the nonpositive constant term gives the stated level bound. In the
   alternative theorem completion, simplex compactness yields a nonzero
   multiplier limit; the all-trivial assumption and strict feasibility
   make its constant negative, so the level bound applies eventually and
   contradicts diverging levels. The zero coefficient cone causes no gap:
   existence of a sweep certificate with negative constant already rules
   out a zero coefficient pair.

The newer proof and the older quantitative route together preserve the
source developments within this stage. The one-normal remark accurately
describes what the proof actually needs and does not assert that convexity
on the limiting hyperplane alone suffices. The exposition explains the
steps that could otherwise conceal a gap, particularly closedness,
constant elimination, and the recovery of actual multipliers.

## Formal correspondence and limits

I inspected the actual `Model`, `DefinitionsSequence`, `Hyperplanes`,
`SweepBounds`, `Coefficients`, `LimitCompactness`, `Headline`, and
`ConeGeometry` declarations. `System` carries symmetry of the original
matrices; `feasible` is strict; `Certificate` requires nonnegative nonzero
weights, matrix PSD, and a nonzero quadratic or linear coefficient.
`proper_hull_iff_certificate` takes exactly strict nonemptiness and AHC.
Its HHC specialization introduces no extra premise.

The headline constructs unbounded hyperplane certificates from support,
AHC, and separation; it proves the nonzero-pair condition and constant
elimination; it supplies closedness and scaling of the actual coefficient
cone to the generic compactness lemma; and it recovers the original
aggregation weights and PSD using symmetry. These facts are not opaque
extra hypotheses of the headline. The formal use of equivalent maximum
norms does not change the mathematical content.

The written account correctly distinguishes the independently formalized
uniform cone lemma from the unformalized spectral distance calculation
and quantitative alternative. It also excludes all later consequences,
applications, examples, frontier claims, and novelty assertions. The
coordinator's completed targeted check supports the reported 11-module,
178-declaration and kernel-replay statement. I did not rerun those checks.
The permanent standalone source package remains an explicit stage-5
obligation; its absence is not a missing stage-2 theorem proof.

## Checks actually run and records read

- Read both current stage-2 sections and the author report, related
  canonical proof material, coverage/status records, the formal wrapper
  documentation, and the coordinator's independent formal-check report.
- Inspected the actual Lean declarations listed above for semantic
  correspondence. This was source review, not a second compilation or
  kernel check.
- Ran a targeted Python SHA-256 comparison against
  `process/stage02-author-snapshot.json`: all **22** recorded files match,
  including the stage-2 sources, eleven Lean files, relevant source records,
  formal-check manifest, and both PDFs.
- The same targeted script searched the existing final `main.log` and
  `formal-verification.log` for warnings, undefined references, and box
  diagnostics: zero matches in each. I did not independently rebuild or
  visually inspect the PDFs.
- An initial read used the nonexistent name `stage02-root-lean-check.md`;
  a targeted file search located and I read the actual
  `stage02-root-formal-check.md`. No file was changed by that failed read.
- No numerical experiment or new literature search was needed for the
  proof review; stage 1's versioned prior-work setting remains in force.
  No project-wide verification or CI checks were performed.
