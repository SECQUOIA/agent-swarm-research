# Stage 2 author record

Date: 2026-09-07. Scope: exact scalar and block responses, global comparison,
attainment and pessimistic semantics, supplied low-rank specialization, and
supporting fixed-core polyhedral elimination. Stage 2 is an author draft pending
five independent reviews. No stage 3 work was authored or delegated.

## Manuscript changes

- `sections/02-exact-responses.tex` gives the full exact quadratic-block theorem,
  with scalar clipping as its explanatory specialization. It proves local active
  normal support reduction, guarded rational formulas, polynomial global regimes,
  polynomial expanded degree/encoding, global comparison, exact common-field
  recovery, and fixed-normal optimistic attainment.
- The same section proves moving-normal compression with rank-changing equality
  bases, exact optimistic and pessimistic infimum/attainment algorithms, universal
  upper feasibility, worst-response recovery, and the supplied diagonal-plus-fixed-
  rank rational LP corollary. Explicit examples exhibit moving-normal optimistic
  nonattainment, fixed-normal pessimistic nonattainment, true ties, and rejection
  of a nonglobal stationary follower point.
- `appendices/a-fixed-core.tex` gives the complete fixed-core polyhedral theorem,
  vertex/support construction, Minkowski membership proof, optimum sampling, and
  constructive recovery of every original block.
- `main.tex` now includes stage 2 and the fixed-core appendix after the future
  main-section inputs. Later appendices have a clear insertion point. Existing
  foundation prose and the accepted snapshot were not modified.
- `references.bib` adds verified Adler–Beling metadata; its algebraic LP result is
  cited as an alternative method, not needed as an algorithmic black box by the
  final appendix proof.
- `process/coverage.md` maps every stage 2 obligation to manuscript labels and
  retains all stage 3–7 obligations, including the corrected curvature-boundary
  row added during stage 1 review. README identifies the current draft accurately.

## Developments beyond transcription

### Common support tuples replace algebraic LP recovery

Root proposed a more constructive recovery route, which the author verified and
proved in `lem:core-recovery`. The original support-regime enumeration produces
polynomially many complete tuples of local vertices. At the sampled optimum core,
keep every tuple whose selected formulas are defined and blockwise feasible.
The original direction/sign region need not still be realizable at that core.
The retained aggregate sums lie inside the true Minkowski sum and collectively
achieve its support in every direction. Equality of all supports proves that
their convex hull is the full aggregate/objective image.

A standard Carathéodory support reduction then yields at most k+2 tuples, since
the objective is appended to k linking measurements. Enumerating affinely
independent subsets and solving fixed-size systems over the already sampled
field returns nonnegative common weights. Applying these same weights in every
block reconstructs a feasible original tuple with the exact optimum objective.
All bit/degree bounds remain polynomial and no new field is adjoined.

This removes a substantial external arithmetic dependency: no growing-dimensional
algebraic-coefficient LP needs to be solved. The proof explicitly limits convex
combinations to polyhedral feasibility and affine measurements. It never mixes
nonconvex follower optima to invent response choices.

### Numerical degree need not be fixed in the polyhedral theorem

The source fixed-core theorem fixes degree. The appendix proves the more uniform
bound polynomial in (L, delta) for fixed core, local block, and linking dimensions.
Local determinant/score tests have O(d delta) degree and global products have
O((B+1)d delta) degree; expansion is in a fixed number of variables. Their dense
sizes and coefficient bit lengths are polynomial. Fixed-dimensional sign
construction, QE, sampling, and the new reconstruction preserve those bounds.
The statement becomes polynomial in L under the paper's degree-encoding rule.

### Constant local Hessians bound algebraic degree independently of N

Root also identified a useful arithmetic refinement, proved as
`cor:constant-hessian-degree`. If local normals and local Q matrices are constant,
local KKT denominators are rational constants. Each response branch is polynomial
in compressed coordinates of degree O(delta), regardless of the follower count.
Candidate and substituted upper polynomials then have degree O(delta^2), independent
of row and block counts. The degree bounds in Basu–Pollack–Roy's QE and sampling
algorithms depend on degrees/dimensions, not the number of polynomials. Therefore
fixed structural dimensions and fixed delta give a constant bound on the common
field degree of an optimistic optimizer/value, and on pessimistic infima and
attained leader/worst-response outputs. Their total encoding lengths still grow
polynomially with the input. This refinement is not extended to moving local
normals or leader-dependent Q matrices.

## Proof obligations explicitly checked

- Fixing x and w leaves a compact strictly convex quadratic fiber problem. This
  explains the geometric compression, while the construction still uses shared
  multipliers and a separate global comparison.
- Local KKT necessity follows from the polyhedral tangent/normal alternative and
  requires neither Slater nor linear independence. The conic support reduction
  works modulo the equality row space, including redundant equalities.
- All branch validity predicates include original local rows and multiplier
  signs. Moving matrices additionally require nonzero determinants; all equality
  subsets up to local dimension are enumerated, so rank changes are covered.
- Global regimes are realizable sign conditions, not a Cartesian product. They
  may be disconnected. Overlapping valid local formulas agree by strict convexity.
- Positive squared determinants prevent incorrect denominator sign clearing.
  The growing product degrees and coefficient lengths are counted explicitly.
- Every compared candidate is feasible, and every global minimum is a candidate.
  These two directions justify comparison of stationary candidate values without
  a false convexity or stationary-sufficiency assumption.
- Quantified response copies occur a fixed number of times. In particular the
  number of upper rows does not introduce one real-variable block per row.
- Fixed-normal compactness uses Hoffman only on nonempty follower fibers along
  the converging sequence. Moving normals preserve pointwise KKT but not that
  uniform repair argument; the counterexample exposes the failure.
- The pessimistic objective uses all optimal responses before upper filtering;
  existence and attainment are separate predicates. Infimum output and optimal
  leader/witness output are recovered jointly only when appropriate.
- LP-cell closures in the low-rank specialization are safe because clipping
  formulas agree on thresholds; the true follower Hessian is SPD even when the
  supplied small coupling matrix is indefinite.
- The polyhedral appendix covers lower-dimensional and singleton blocks, empty
  blocks, signed and vanishing determinants, lower-dimensional aggregate hulls,
  redundant barycentric equations, and the empty block family. Common weights,
  not independent weights per block, preserve the aggregate target.

## Primary source verification and attribution

Read `literature/AGENTS.md` and did not alter literature packages or redistribute
originals. Read the canonical exact scalar/block, moving-normal/semantics, low-rank,
and fixed-core proofs, rather than inheriting their historical PASS verdicts.

Basu–Pollack–Roy (1996) remains the established exact real algebraic dependency.
Direct primary text checked: Theorem 1.3.1 and surrounding bit model; Section
3.1.2's degree bound for each univariate representation; and Section 3.1.3's
sample-point construction (PDF pp.27–28). Root independently checked the last
point. It supports the independence of output degree from the polynomial count
used in the constant-Q corollary.

Adler–Beling, *Polynomial Algorithms for Linear Programming over the Algebraic
Numbers*, Algorithmica 12:436–457 (1994), DOI 10.1007/BF01188714, was checked using
the local primary package and the author-hosted original:
https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf.
Their abstract, extension-degree discussion, and Section 5 Remark 1 explicitly
track the common algebraic extension and outline the rational-machine version.
The final manuscript does not rely on that outline, since support-tuple recovery
uses only fixed-size algebraic linear systems.

Megiddo–Tamir's multiplier/block elimination and Hoffman's fixed-matrix error bound
are credited as established ingredients. The Carathéodory reduction and support
separation argument are given explicitly. No source note or agent review is cited
as mathematical authority, and no exhaustive priority claim is made.

## Actual verification

Records are in `verification/stage02-author/`.

| Command | Outcome and distinct purpose |
| --- | --- |
| `python code/bilevel_response/check_response_boundaries.py` from repository root | PASS. Guarded moving-normal branches, singular equality basis replacement, and rejection of a nonglobal quartic KKT point. Output retained in `response-boundaries.txt`. |
| `python code/fixed_core_blocks/check.py` from repository root | PASS. 1,971 exact support/denominator checks, independent SciPy LP comparisons, and degeneracy checks. Output retained in `fixed-core.txt`. This is not a QE implementation. |
| `python verification/stage02-author/check_support_recovery.py` from paper folder | PASS. 124 exact support-hull/reconstruction targets across 18 cases: all original Cartesian vertex images and interior targets, empty/singleton/collinear/duplicate/zero images, and recovery in Q(sqrt(2)). Output retained in `support-recovery.txt`. |
| `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` from paper folder | PASS. Combined draft is 17 pages; final log has no warnings, undefined citations/references, or overfull/underfull boxes. Build transcript retained in `build.txt`. |

The new diagnostic obtains support tuples from planar direction rays and their
pair sums, independently checks images of the full original Cartesian product,
and reconstructs interior aggregate targets with common barycentric weights.
It checks a risky new reconstruction contract, not the universal proof or general
sign enumeration. It uses exact SymPy arithmetic; SciPy tolerances belong only to
the older, separately identified LP comparisons.

The explicit output logs for the first two scripts reproduce their actual tool
outputs with command and exit code. No timing claims are made. `manifest.json`
records the final input/artifact hashes and command outcomes. During development
one combined shell command used the paper working directory with repository-relative
write paths; those writes failed before changing files and the command was rerun
with absolute paths. The final build and files are the ones recorded here.

## Remaining scope

All stage 2 assigned theorem/proof obligations are written. Detailed cubic
arithmetic, sparse-degree and curvature/hardness boundaries remain with stages
4/5; this section only includes their needed square-root-sum motivation. Robust
near-optimal compression, screening, approximation, and computational algorithms
remain their later stages. This draft is ready for five independent stage 2
reviews; no claim of accepted stage status or completed paper is made here.
