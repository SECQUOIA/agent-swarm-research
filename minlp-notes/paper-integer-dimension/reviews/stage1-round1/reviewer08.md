Reviewer 08, stage1-round1. Primary lens: constant scalar Hessian rank, partial Legendre charts, polyhedral tubes, and finite covering.

Major findings: 0

Minor findings: 2

I found no false theorem or material proof gap in the completed stage. In particular, the constant-rank scalar upper bound supplies the needed control on each entire polyhedral tube, including points outside the chosen gradient-parameter cube. Its finite covering argument handles the boundary of the original box and uses the nonlinear charts only to select affine fibers. The final objects are actual polyhedra in the original coordinates. This assessment is limited to the checks described below and is not a claim of certainty or publication priority.

1. MINOR — Typographical error in the smooth Taylor bounds. Location: `sections/01-foundations.tex`, proof of `thm:smooth-ranks`, lines 974, 977, and 992. The expressions `C_0,2^{-T}` and `2C_0,2^{-T}` contain a literal comma between factors. This renders a comma in the displayed inequality and obscures the intended product. The reasoning clearly needs the ordinary products `C_0 2^{-T}` and `2C_0 2^{-T}`. Replace each literal comma by whitespace or `\,`. This is a notation defect, not a false estimate.

2. MINOR — The capacity import needs its own accurate source locator. Location: `sections/01-foundations.tex`, lines 529–542, the citation introducing `eq:shrunk`, `eq:evaluation`, and `eq:capacity`. GGOW Theorems 1.4 and 1.17 support the shrinking/rank and matrix-evaluation statements, but neither numbered theorem states the positive-capacity equivalence. I checked those statements in the cached published primary text. GGOW discusses positivity of capacity for a noncommutatively nonsingular pencil on printed page 237, credits Gurvits there, and defines and develops capacity in Section 2. The original repository result also cited Section 2 and explicitly credited Gurvits. Add that locator and attribution for the capacity assertion, rather than placing all three imports under the two theorem numbers. This is a source-locator/attribution weakness; the capacity fact itself is not challenged, and the manuscript also provides the independent Hall/permanent route to the qualitative lower exponent.

I read `PROCESS.md`, `reviews/PROTOCOL.md`, `reviews/STAGE1-TASK.md`, the assigned lens, the round snapshot, the complete 1,206-line `sections/01-foundations.tex`, `coverage.md`, `references.bib`, `macros.tex`, and `main.tex`. I compared the manuscript with all nine canonical stage-1 result files listed in the coverage table, including the original scalar constant-rank, smooth-map, perspective, scalar quadratic, inertia, bilinear graph, square/product, covariance, and noncommutative-rank proofs. I also read `notes/review-constant-hessian-rank-smooth-precision.md`, `notes/nonquadratic-integer-precision-investigation.md`, and `notes/mip-binary-lower-bound-extensions.md`. The existing audit was used to compare scope and obligations after reconstructing the manuscript argument, not as proof.

The independent mathematical checks covered parity classes with unrestricted integer indices and nonclosed lifts; closure and measurable contact-volume arguments; finite disjunctions and common recession cones; square/product constants and shared prefixes; the maximal-simplex determinant bound; one-sided inertia and unbounded epigraph outputs; Hermitian principal compression; real descent and the symmetric shrinking decomposition; covariance and Hall/permanent energy estimates; the local oscillatory estimate and tensor-power contact bound; global Hessian allocation and polynomial prefix compilation; and row homogenization for positive perspectives. I did not find another concrete defect in those arguments.

For the assigned lens, I explicitly checked the following obligations:

- A nonsingular principal Hessian block gives a locally invertible map `(u,v) -> (f_u(u,v),v)`. Constant rank makes the partial Legendre Schur complement vanish identically on the chart, so the inverse fibers are affine in `v`, and the stated affine function has both the correct value and gradient along the entire fiber.
- Compact nested parameter boxes give uniform Lipschitz and bounded-Hessian constants. A sufficiently small transverse neighborhood remains in the open smooth domain. Every Taylor segment used for a tube stays in this neighborhood. Thus the bound `MrL^2 h^2/2` applies to the whole tube without assuming that its points have nearby gradient parameters.
- The tube inequalities are linear because the central fiber is affine in `v`; boundedness follows from the compact `v` box and bounded transverse widths. Intersecting with the original box preserves polyhedrality. Empty intersections may be discarded.
- Each original box point, including a boundary point, lies in the interior of a smaller chart image. Compactness gives finitely many charts, with constants independent of accuracy. Their member counts add to `O(h^{-r})`. A Taylor error budget of `eps/2` and an affine band of radius `eps/2` give both graph containment and the required total error.
- Rank zero reduces to an affine function on the connected box. Rank equal to ambient dimension uses the zero-dimensional `v` parameter space and reduces to ordinary Taylor cells. The theorem correctly avoids claims about rank-changing singularities, general vector local-rank upper bounds, or rational compact compilation of arbitrary smooth charts.

I inspected the cached primary text of Nicola, Definition 1.1 and the following paragraph, which explicitly supports the constant-rank affine-gradient-fiber attribution. I also inspected Wolff, Theorem A and its proof on printed pages 50–51, and the relevant GGOW rank statements and capacity discussion. I did not perform a complete independent bibliography/novelty search, inspect every external reference, or audit the as-yet-unwritten stage-2 rational bit-complexity proof. That proof is explicitly deferred, so its absence is not counted as a stage-1 omission. I did not use the literature knowledge base, compile LaTeX, or rerun the repository's full numerical suites.

Executed checks: an inline SymPy check verified the rank-two indefinite example `f(x,y,t)=(x^2-y^2)/t` for `t != 0`, its affine Legendre fibers `x=tp/2, y=-tq/2`, and the exact transverse error `(du^2-dv^2)/t`. This exercises rotating null spaces without positive semidefiniteness. A second exact symbolic check verified the displayed four-variable polynomial Hessian at `(1,1,1,1)` and its rank three. Both passed. These finite symbolic checks supplement the general proof review.

The following SHA-256 hashes were computed from the reviewed files and all matched `reviews/stage1-round1/snapshot.json`:

| File, relative to `paper-integer-dimension/` | SHA-256 |
| --- | --- |
| `coverage.md` | `a5b675009a1c889bf93105e5b1121f2d5de5fac732d414c4b0b71563e1ce7727` |
| `macros.tex` | `3f613a2cf8ebf1bd4c6c84b531de0e74479e07a19ce7566961f1348384de7a3f` |
| `main.tex` | `cecaea518c089ff3beca3edf14ec879129f947f67ed01af7ef3602fb74ea571e` |
| `references.bib` | `bc7fbcf1dad163b2e1064e787760f7f76b88ba649c3f6657d3a46d9432a433da` |
| `sections/01-foundations.tex` | `075e0e998e9cf3e9bdf0830fde1822876ac272bb336eec5d10374425ace92e03` |
