# Stage 2, round 1: independent review 4

Date: 2026-09-22. Scope: certificate theorem, both proof routes, and formal
semantic integration. I read the author report, current certificate/formal
sections, main/supplement wrappers, formal README, and the relevant actual
Lean sources. I did not read other current reviewer reports or edit sources.

## Verdict

Accept stage 2. No major or minor issue identified. The main argument is
self-contained and mathematically sound. The quantitative alternative is also
valid. The formal account accurately states the correspondence and its limits.
Later consequences, frontier results, and final packaging remain intentionally
outside this verdict.

## Main proof checks

1. The AHC definition has the required quantifier order: the good unbounded
   levels may depend on the normal. The displayed recursive construction
   proves the increasing-sequence equivalence. The proof only needs one normal
   supporting the hull, exactly as the later remark explains.
2. A common strict negative leading direction puts both sufficiently distant
   opposite translates of every point into the strict system. Finiteness of
   the family makes the common radius legitimate. The exclusion of `t=0`
   and the dehomogenization argument for either sign of `t` are both correct.
3. Openness of the ordinary convex hull is correctly justified. Separation
   from an exterior point yields a strict bound on that open set without
   assuming a closed hull or strong separation by positive distance.
4. Hyperplane-image separation needs only convexity of the image and openness
   of the negative orthant. The sign of the separator, level zero, and simplex
   normalization are correctly derived; no closed-image assumption is hidden.
5. Strict feasibility gives an upper bound on the constant, and its coefficient
   in the sweep inequality is a nonnegative square. Replacing it therefore
   preserves nonnegativity in the required direction. The coefficient pair is
   proved nonzero before division by its norm.
6. The finite-cone closedness proof handles dependent generators, negative
   relation coefficients, and the zero vector. It uses finite generation rather
   than a false universal closed-linear-image assertion.
7. The unit coefficient pairs have one convergent subsequence independent of
   the evaluation point. Continuity bounds the normalized linear functional;
   the perturbations vanish for each fixed point. The limit belongs to the
   actual cone, is nonzero, and has PSD quadratic part. Recovering weights
   through cone membership is sufficient; convergence of normalized weights
   or boundedness of the normalized constant is never assumed.
8. The easy direction correctly handles both a nonzero PSD quadratic part and
   a nonzero affine slope, including empty original feasible sets.

## Quantitative alternative

The angular separation lemma is correct for closed cones meeting only at zero,
without convexity. The distance formula leaves the vector component fixed and
truncates the negative matrix eigenvalues. Its bound uses the positive part of
the negative minimum eigenvalue, so it remains valid for PSD matrices too.

Under the no-nontrivial-certificate hypothesis, a nonzero coefficient pair has
minimum eigenvalue at most `-kappa*rho/sqrt(n)`. Evaluating along its unit
eigenvector, removing the nonpositive constant term, and bounding the cross
term yields exactly `s <= 2*sqrt(n)*norm(alpha)/kappa`. In the alternative
contradiction, simplex compactness supplies bounded coefficients and a nonzero
limit multiplier; strict feasibility then makes the limiting constant negative.
Thus the eventual hypothesis needed for the sweep bound is established rather
than assumed.

## Formal correspondence

I read the actual `Model`, `DefinitionsSequence`, `Headline`, `Hyperplanes`,
`SweepBounds`, `Coefficients`, `ConeClosed`, `LimitCompactness`, `ConeGeometry`,
`EasyDirection`, and `Recession` modules. The definitions and headline
interfaces have the intended strict feasibility, ordinary hull, nonnegative
nonzero weights, PSD quadratic part, and nonconstant aggregate. HHC uses all
nonzero-functional kernels; AHC matches the manuscript and its sequence
equivalence is proved. There is no extra definiteness, rank, separation-weight,
or cone-closedness premise in the headline.

The coefficient cone contains actual weights; its membership-to-certificate
conversion uses the stored matrix symmetry. Constant elimination and the
abstract compactness result have the required signs. The latter takes a closed
scaling-stable set as premises, and these premises are supplied by proved facts
about this particular coefficient cone. The norm convention uses the scoped
elementwise matrix norm and product maximum norm as stated.

I inspected the coordinator's independent check record and manifest. They
support the reported eleven-module check scope and pinned toolchain. I did not
repeat Lean compilation or kernel replay. The manuscript distinguishes these
checks from independent-kernel verification and excludes the spectral estimate,
quantitative alternative, later consequences, examples, applications, and
priority claims from its formal scope. The eventual portable-source packaging
obligation is explicit and appropriately deferred.

## Targeted checks actually run

Reads used `cat` on the files identified above and a targeted source search
for `sorry|admit|axiom|opaque` in the eleven-module directory. The only search
match was ordinary prose containing “admits,” not a proof placeholder.

From `paper-quadratic-aggregation/`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/quadratic-stage02-review4 main.tex
rg -n 'Warning|Overfull|Underfull|undefined' /tmp/quadratic-stage02-review4/main.log
```

The isolated-directory build passed, producing seven pages; the final log
search found no matches. The supplement wrapper reuses the same checked
sections and bibliography; I inspected it without an unnecessary second build.
No project-wide check, CI inspection, duplicate Lean run, or subagent was used.
