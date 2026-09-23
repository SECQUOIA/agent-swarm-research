# Stage 2, round 1 — independent review 02

**Verdict: accept after one minor attribution correction.** I found no major mathematical or encoding defect in the frozen stage. The new support-tuple recovery and constant-local-Hessian degree corollary are supported by their proofs. The geometric algorithmic predecessor of the appendix should be cited explicitly.

## Snapshot, scope, and independence

I read the entire snapshot `process/snapshots/stage02-round01`: `main.tex`, both sections, the fixed-core appendix, bibliography, README, and coverage map. The manifest digest is `b4c7f91913054ca4da83eac32ccaae2ac52412e605c468a63278172846d1f849`; all seven file hashes match. All manuscript locators below refer to that snapshot.

I did not read other stage 2 review reports, coordinate findings, delegate, or edit manuscript sources. Verification artifacts are confined to `verification/reviewer02/stage02-round01`. I followed the previously read `literature/AGENTS.md` and changed no literature files. The accepted foundations were reread for integration; the deferred stages are not treated as missing material in this review.

## Actionable finding

### R02-S02-01 — minor: cite the direct Minkowski-sum algorithmic predecessors

**Locator:** `appendices/a-fixed-core.tex:84–101`, `182–212`, and especially the attribution paragraph at `268–274`; `references.bib`.

The appendix credits “established tools” in general and cites Adler–Beling for an alternative recovery route, but does not identify the established fixed-dimensional Minkowski-sum algorithms behind compatible support choices. The shared-direction selection is more specific than a generic invocation of convexity or Carathéodory’s theorem. A reader should be able to distinguish this known construction from its uniform extension over the polynomially varying core and from the explicit recovery presented here.

**Primary evidence:** Gritzmann–Sturmfels, *Minkowski Addition of Polytopes: Computational Complexity and Applications to Gröbner Bases*, Algorithm 2.3.6 and Theorem 2.3.7, [[gritzmann1993-minkowski-addition-of-polytopes-computational]] p.13, enumerate a common arrangement of support directions and recover summand maximizers for each cell. Corollary 2.3.10 gives fixed-dimensional polynomial binary complexity, p.14. I inspected the extracted primary text and independently extracted those pages from the user-supplied original; I did not copy the original into the manuscript folder. Fukuda’s [author manuscript, Proposition 2.1 and Corollary 2.2, PDF pp.3–4](https://www.cs.mcgill.ca/~fukuda/download/paper/minksum030111.pdf) explicitly characterizes compatible summand faces and vertices through a common support direction and credits Gritzmann–Sturmfels. These are direct antecedents of the geometric step in this appendix.

**Actionable fix:** Add Gritzmann–Sturmfels (1993), and optionally Fukuda (2004), to the bibliography and cite them where compatible support choices are introduced or in the concluding attribution paragraph. Briefly identify the manuscript’s additional step as uniform sign enumeration over the varying core, followed by exact optimization and common-field reconstruction. Do not attribute the polynomially varying-core theorem itself to these fixed-polytope sources.

**Severity rationale:** The manuscript already calls the ingredients established, and its proof is complete. This is a traceable-attribution gap, not a false theorem or a finding that the full structural theorem is already present in those sources. No priority conclusion follows from the bounded source comparison.

## Mathematical findings: no correction required

### Exact quadratic-block compression

The proof at `sections/02-exact-responses.tex:42–309` correctly separates local strictly convex elimination from global nonconvex follower comparison.

- Polyhedral first-order necessity requires no Slater or active-row independence promise. The quotient-space support reduction preserves nonnegative inequality multipliers and produces independent active normals modulo an equality basis.
- The bordered KKT matrix is nonsingular under the stated positive definiteness and independent-row conditions. Squaring its determinant and multiplying the Cramer numerators preserves the solution and permits sign-safe denominator clearing.
- Testing every original local row handles redundant or inconsistent equalities. The valid branches agree because the effective local quadratic problem is strictly convex.
- Joint sign enumeration in fixed compressed dimension avoids an exponential product of local branch lists. Disconnected sign realizations do not invalidate branch selection, and zero signs are retained.
- The common response denominator and follower-value numerator have the stated polynomial degree and coefficient bounds. The substitution lemma controls arbitrary explicitly listed upper polynomials despite growing follower support. The objective equation uses an additional fixed coordinate.
- The global predicate compares feasible candidates with their actual follower values. Every global minimum has a KKT encoding, so comparing all candidates excludes nonglobal stationary points without assuming stationarity sufficient for the original nonconvex follower.
- Eliminating the response comparison once before further formulas prevents a growing number of upper rows or regimes from becoming a growing number of quantified variables. Joint sampling and rational decoding remain in one extension.
- The fixed-normal Hoffman argument proves the required closed graph on the actual feasible-leader domain, including instances with empty fibers elsewhere. Compactness then proves optimistic attainment.

The opening fiber interpretation is also correct: fixing an attainable aggregate leaves a strictly convex local sum on a convex fiber, so at most one global response can correspond to that aggregate for a fixed leader. It is not used to discard other aggregates or ties.

### Moving normals, semantics, and the LP specialization

The changing-rank construction at lines 317–358 correctly enumerates all equality/inequality subset pairs and guards the determinant. Soundness does not require the chosen equality subset to span every equality, because omitted multipliers can be zero and all primal rows are tested. Completeness chooses a true equality basis separately at each leader. The proof does not improperly reuse the fixed-normal continuity argument.

The optimistic moving-row example and fixed-normal pessimistic tie example have the claimed responses and unattained infima. The pessimistic formulas at lines 389–453 exclude empty followers, detect any upper violation over the entire global response set, compute the attained worst response at each feasible leader, and distinguish the leader infimum from an optimizer. A fixed number of elimination stages suffices.

The supplied low-rank corollary at lines 516–557 requires positive definiteness of the full Hessian while permitting an indefinite small matrix `M`; that is the correct distinction. Clipping consistency gives the complete box KKT conditions. Closing nonempty affine arrangement cells introduces no false response because the clipped formulas agree at thresholds. The aggregate bounds make each LP compact, and affine rational reconstruction gives a rational optimizer. The decomposition is explicitly supplied rather than computed.

### Constant-local-Hessian algebraic degree

The corollary at lines 474–510 is justified. Fixed normals and constant local Hessians make each KKT inverse rational and constant in the compressed coordinates. Summing arbitrarily many polynomial responses changes coefficient size, not degree. There is consequently no growing-degree denominator product, and substituted upper data have bounded degree when the numerical input degree is fixed.

I verified both external degree facts required for the conclusion, rather than inferring sample degree from quantifier elimination alone. Basu–Pollack–Roy Theorem 1.3.1 bounds the output polynomial degrees in terms of input degree and quantifier-block dimensions, independently of the number of input polynomials; [[basu1996-on-the-combinatorial-and-algebraic]] p.4, printed p.1005. Section 3.1.3 separately bounds the degree of each univariate sample representation in terms of degree and ambient dimension; p.27-28, printed pp.1028–1029. Original PDF images of the relevant theorem and sample construction were inspected and retained under verification. The fixed number of sequential eliminations and joint sampling therefore gives the claimed constant common-field degree, while coefficient bits and the total number of returned coordinates may grow polynomially.

### Fixed-core theorem and constructive recovery

The appendix’s numerical-degree extension is valid under its stated explicit polynomial encoding. Local determinants, feasibility tests, and score comparisons have degree `O(d delta)`. Global denominator products have degree `O((B+1)d delta)` in a fixed number of variables. Expanding them remains polynomial in numerical degree and input length; the proof does not claim polynomial time in sparse binary exponent length alone.

The support membership formula handles empty blocks correctly and is exact for nonempty compact convex Minkowski sums. The nearest-point separation argument supplies a complete proof of the reverse implication. Uniform finite rational block bounds ensure compactness even though local normals vary.

The new recovery argument at appendix lines 182–247 is sound. For every direction at the sampled core, its actual sign condition occurs in the globally constructed list. Its selected tuple survives the feasibility filter and attains the true support value. Extra tuples from sign conditions realizable only at other cores remain harmless because they are independently checked feasible at the sampled core. Thus the filtered aggregate hull equals the full image.

Carathéodory reduction supplies at most `h+1` affinely independent aggregate points. Enumerating such subsets has polynomial cost for fixed `h`. Each successful overdetermined system has a unique solution determined by independent rows, so its weights belong to the existing field. Checking the remaining equations and nonnegativity completes the construction. Applying those same weights to every block preserves both local convex feasibility and all linking/objective measurements. This is a convex combination of feasible polyhedral tuples; it does not mix a nonconvex follower’s response set. The no-block case and bounded slack-block extension are consistent.

Adler–Beling is correctly described as an alternative algebraic LP route with dependence on the common extension degree; see [[adler1994-polynomial-algorithms-for-linear-programming]] p.1-3 and the [author-hosted original](https://adler.ieor.berkeley.edu/ilans_pubs/lp_algebraic_1994.pdf). The manuscript does not assume polynomial complexity from separate coefficient degrees alone.

## Integration, coverage, and checks

The earlier review’s optimistic qualification and `(L, delta)` output wording are present in the foundations. The main theorem, moving-normal extension, pessimistic infimum theorem, rational LP specialization, and fixed-core appendix retain their distinct assumptions and output guarantees. Megiddo–Tamir remains credited for local multiplier arrangements, and the manuscript does not claim its polynomial global comparison as a consequence of convexity of the full follower.

I compared the written stage against the canonical fixed-core theorem’s Sections 1–5, the supplied low-rank corollary, the moving-normal note, the response-semantics result, and the relevant source-positioning notes. The coverage map identifies the new recovery and degree refinement, and retains the later-stage arithmetic and curvature boundaries. I found no omitted stage 2 proof obligation. The attribution finding above concerns a predecessor already identified in the repository source audit; it requires a primary citation in the paper, not another repository-note citation.

Verification completed in the isolated directory:

- All snapshot hashes match; see `hash-check.txt`.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../build main.tex` succeeded from the copied source directory. The final log has no warning, undefined reference/citation, overfull, or underfull diagnostic. See `build-command.log` and `build/main.log`.
- A separate label scan found no duplicate or missing labels; see `static-check.log`.
- Independently written `check_recovery.py` checks a triangle, a segment, and a singleton block with measurements in `Q(sqrt(2))`. Five selected support tuples span all six full-product images, and three common weights reconstruct an interior target with every block feasible in that same field. It also checks the moving-row determinant and the nonglobal quartic stationary midpoint. See `exact-check.log`. This is a small exact diagnostic, not an implementation or proof of general quantifier elimination.

## Limits of this review

The primary-source work checked the exact claims used here, with particular attention to both BPR degree bounds, the algebraic LP field assumption, and compatible Minkowski support choices. The Gritzmann–Sturmfels original is legitimately user-supplied and was read locally without redistribution. The Fukuda and Adler author copies were accessible online. The original-stage historical access limits for Liu–Spencer and Deng remain; the accepted broad comparisons do not require invented internal theorem locators. I did not exhaust all later literature or establish publication priority. Later-stage theorems and experiments remain outside this stage’s acceptance decision.
