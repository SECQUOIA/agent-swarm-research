# Stage 2, round 1: independent review 05

Reviewer: reviewer05. Date: 2026-09-07.

## Snapshot and disposition

Reviewed frozen source: `process/snapshots/stage02-round01/`.
The SHA-256 of `SHA256.json` is
`b4c7f91913054ca4da83eac32ccaae2ac52412e605c468a63278172846d1f849`.
All seven listed source files independently matched their manifest hashes.
All source locations below refer to this snapshot.

I read the entire stage: both sections, the fixed-core appendix, main file,
bibliography, README, and coverage record. I checked the new proofs directly
and compared their scope with the canonical sources. I did not read another
reviewer's stage 2 report, coordinate findings, delegate, or edit manuscript
sources. Compilation and rendering used only my private copy under
`verification/reviewer05/stage02-round01/`.

**Recommendation: pass.** I found no major or minor issue requiring correction.
The support-tuple reconstruction, polynomial numerical-degree extension, and
constant-local-Hessian degree refinement are justified by the supplied proofs.
There are optional pagination improvements below; these are suitable for the
scheduled final layout pass and do not block this stage.

## Major findings

None found.

## Minor findings requiring correction

None found.

## Full mathematical review

### Local elimination and global comparison

Locations: `sections/02-exact-responses.tex`, lines 10–18, 42–142, 146–282.

The initial convex-fiber explanation is correct and useful: with the leader and
aggregate fixed, the remaining objective is strictly convex on a convex fiber,
so a global optimum is the unique fiber minimizer. This explains why many
follower coordinates do not require unrelated algebraic parameters.

The normal-cone argument supplies necessary multipliers at every local minimum
without Slater or independent active rows. The local problem has the correct
effective linear term, including aggregate and shared multiplier contributions.
The scalar clipping tests have the correct order and signs, cover singleton
intervals, and agree at branch boundaries.

The block proof handles redundant equalities by retaining all primal equality
tests while using an independent basis for stationarity. Its conic-support
reduction is valid modulo the equality row space: changing the sign of a
dependence provides a positive coefficient, the stated minimum step preserves
nonnegativity, and each iteration removes a supported generator. The surviving
rows give a nonsingular saddle-point matrix because the local Hessian is
positive definite. Squaring its determinant and multiplying the Cramer
numerator by the original determinant gives the stated positive-denominator
representation. Valid branches satisfy sufficient local KKT conditions and
therefore agree wherever they overlap.

The polynomial regime count follows from sign enumeration in a fixed ambient
dimension, not from a Cartesian product. Disconnected sign realizations do not
invalidate selection because all local decisions depend only on signs. The
shared consistency and complementarity equations reconstruct exactly feasible
stationary candidates. The numerator in equation (19) equals the original
follower objective times the positive squared common denominator.

The universal comparison in equation (21) is sufficient for globality because
every true global minimum is among the candidates and every candidate is
feasible. It therefore removes nonglobal stationary points and retains every
global tie. The upper regime predicate uses the same candidate regime; it does
not accidentally associate one response's upper value with another response's
follower value. Quantifier elimination may be applied once to the response
predicate before duplicating it, so growing regime or upper-row counts do not
silently create growing quantified dimension.

### Encoding, recovery, and constant algebraic degree

Locations: `sections/01-foundations.tex`, lines 206–292;
`sections/02-exact-responses.tex`, lines 199–234, 267–282, 474–510.

The substitution lemma and degree estimates remain valid under numerical degree
growth. The common denominator has degree linear in the number of selected
blocks, but its fixed number of variables keeps its expanded encoding
polynomial. The coefficient product estimate explicitly controls bit lengths.
Substituting arbitrary listed upper monomials introduces the additional degree
factor stated in Lemma 2.3. The joint optimality formula samples the leader,
candidate, and objective together; subsequent rational evaluation keeps every
follower coordinate in that field and avoids multiplying independent extension
degrees.

Corollary 2.9 correctly assumes both fixed normals and constant local Hessians.
Their KKT inverses then have rational constant entries. Local responses become
polynomials in the fixed compressed coordinates of degree independent of the
number of blocks. Summing them and substituting fixed-degree upper data preserves
this degree independence. The number and bit lengths of polynomials may grow,
but those quantities do not enter the degree bound in the cited elimination
and sampling results. A fixed number of these operations therefore gives the
claimed uniform degree bound for a selected optimum, infimum, or attained
pessimistic leader/worst-response tuple. The result does not assert that every
optimal real point has bounded algebraic degree.

I rechecked the relevant primary statements in
`[[basu1996-on-the-combinatorial-and-algebraic]] p.3-4` (Theorem 1.3.1 and bit
bounds) and `p.27-28` (Section 3.1.3 and the degree of each univariate sample
representation). The original PDF formulas on pages 4 and 27 were visually
verified in my preceding stage 1 review; the same source and locators are used
here. In particular, the number of sample representations depends on polynomial
count, while the degree of each representation has the required dependence on
degree and ambient dimension.

### Attainment, moving ranks, and pessimism

Locations: `sections/02-exact-responses.tex`, lines 284–472.

The fixed-normal closed-graph proof correctly applies one instance-specific
Hoffman constant to the nonempty systems at the sequence of leaders. It produces
feasible comparison points converging to every feasible point in the limiting
fiber. Passing the optimality inequality to the limit proves closedness; bounded
boxes and weak continuous upper rows then give optimistic attainment.

For moving normals, enumerating all equality/inequality subsets covers changing
equality rank. Soundness requires only a nonsingular selected KKT system, all
primal rows, and nonnegative selected inequality multipliers. It does not require
the selected equality rows to span all equalities everywhere. Completeness
selects a full basis at the actual leader and reduces the remaining conic
support. The determinant guard is included before denominator clearing, including
the empty-basis case when rank drops.

The pessimistic predicate first excludes empty follower sets and then detects
any upper-row violation by a global optimum. Worst-response maximization uses
all global responses, as the defined convention requires. Compactness at each
fixed leader guarantees that worst response even when the leader-dependent graph
is not closed. Uniform boxes bound the objective, so a feasible problem has a
finite infimum. Equation (26) characterizes that infimum without assuming it is
attained; membership in the attainable-value set then decides attainment. Joint
sampling includes a worst response and does not require a separate algebraic
extension.

Both counterexamples check directly. For the moving equality `xz=0`, the
response jumps from zero to one at `x=0`, making the upper infimum zero and
unattained. In Example 2.8 the follower cost is nonnegative; for positive `x`
only zero minimizes it, while at zero the two endpoints minimize it. The stated
worst values, upper-feasibility distinction, and interior stationary value
`1/16` all follow.

### Low-rank rational specialization

Location: `sections/02-exact-responses.tex`, lines 512–557.

The supplied decomposition yields affine clipping thresholds in `(x,w)` even
when the small matrix `M` is indefinite. Positive definiteness of the full
Hessian makes the box KKT conditions sufficient and the follower unique. A
realizable affine sign cell has the stated closure, and clipping formulas agree
on that closure, so closing the cells introduces no false follower response.
The aggregate bounds make each LP bounded. Lower-dimensional cells, constant
thresholds, upper rows, and rational decoding are covered. The proof does not
assume a decomposition can be found or that a small coupling norm implies low
rank. I compared the statement and proof with
`notes/bilevel-fixed-rank-quadratic-corollary.md`.

### Fixed-core appendix and new support-tuple recovery

Locations: `appendices/a-fixed-core.tex`, lines 10–277.

Local vertex enumeration covers lower-dimensional polytopes and singletons:
the active normals at a vertex must span the ambient local space. The displayed
positive-denominator tests give correct feasibility and score comparisons.
The support family is polynomial in the number of local rows for fixed block
dimension. Including the objective as one more measurement correctly turns
exact objective-value feasibility into membership in the Minkowski sum.

Lemma A.2 handles empty blocks and proves both directions of support membership.
The nearest-point separation proof has the correct direction and strict
separation inequality. The closed full feasible set is uniformly bounded by the
supplied finite rational boxes, which justifies attainment despite moving local
normals. Polynomial numerical degree is sufficient throughout: local determinant
and comparison degrees are linear in `d*delta`, the product degrees grow only
linearly in block count, and all algebraic elimination uses a fixed dimension.

The new recovery proof is complete. At the sampled core, filtering the globally
enumerated tuples only by local feasibility is safe: every retained aggregate
lies in the true Minkowski sum. For every direction, the actual sign condition
at that core selected a support-maximizing feasible tuple, which necessarily
survives the filter. The retained convex hull thus has exactly the same support
function and equals the whole image sum. This also explains why it is unnecessary
to solve an additional direction-realizability problem for every retained tuple.

Caratheodory reduction gives affinely independent lifted support with at most
`h+1 = k+2` tuples. Exhaustive enumeration of those fixed-size subsets is
polynomial. On a feasible independent subset, the weight solution is unique
and belongs to the already sampled field because its data and target do.
Checking all leftover equations and weight signs avoids accepting an inconsistent
subset. The same weights applied to every block preserve the aggregate; separate
block-dependent weights would not. Fixed-size determinant formulas control
weight bit lengths and avoid any growing-dimensional algebraic LP dependency.
The no-block case and bounded slack extension are handled expressly.

I compared the appendix with Sections 1–5 of
`results/fixed-core-block-polyhedral-optimization.md`. Its strengthened numerical
degree dependence and different recovery argument are proved in the manuscript
rather than inferred from the narrower source statement. Adler–Beling is used
only to credit the alternative algebraic LP route. Its description agrees with
the primary discussion in
`[[adler1994-polynomial-algorithms-for-linear-programming]] p.1-3`, including
dependence on the common extension degree. The title, venue, pages, and year
match the local primary source.

## Integration, inventory, and reader comprehension

The foundations now explicitly identify the optimistic classical positive
comparison and declare all polynomial coefficients, including `c_b`, rational;
my two stage 1 findings are resolved. The output-degree convention now expressly
uses `(L,delta)`. Approximate output semantics are separated from exact
infeasibility and attainment decisions. These changes are coherent with the new
exact section.

The coverage record maps each stage 2 source to an actual theorem, proof,
example, or corollary. The scalar proof is coherently subsumed in the block
argument with its own clipping explanation. Moving normals, pessimistic
semantics, low-rank LPs, common-field recovery, and the fixed-core appendix are
present. The new arithmetic and recovery refinements are identified as written
developments pending review. The zero/negative-curvature examples and full
arithmetic barriers remain explicitly assigned to later stages. I found no
stage 2 coverage omission.

The structure is understandable for optimization readers: it explains convex
fibers before multiplier elimination, distinguishes local KKT sufficiency from
global comparison, gives explicit nonattainment examples, and separates
polyhedral convex mixing from nonconvex follower responses. The final warning
against mixing tied nonconvex responses is mathematically necessary and retained.

## Build and visual verification

The README command completed successfully from the isolated snapshot copy:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

The clean build produced a 17-page PDF. The final log contains no warnings,
undefined citations or references, or overfull/underfull boxes. All 14 citation
keys resolve. I rendered and visually inspected every PDF page, including the
new formulas, appendix, and bibliography. No text or mathematics is clipped,
overlapping, or unreadable. The verification folder retains the command log,
final build logs, PDF, extracted text, all rendered pages, and `verification.json`.

## Limits and optional suggestions

This review checks the full current mathematical exposition; it does not
reimplement general real-algebraic elimination or independently certify all
theorems in cited literature. I did not run the author's support-recovery
diagnostic because the new claim was assessed directly from its full proof.
The README diagnostic path belongs to the live manuscript's author-verification
folder and is not included in the frozen manuscript snapshot; this does not
affect the self-contained mathematical proof or clean PDF build. Later stage
results and the final abstract are not claimed complete by this draft.

Optional final-layout improvements:

- The short statement of Lemma 1.1 is split across PDF pages 4–5. Keeping the
  statement together would make it easier to read.
- The Adler–Beling bibliography entry breaks between `https:` on page 16 and
  the remainder of its URL on page 17 (`references.bib`, `AdlerBeling1994`).
  Keep the item together or omit the redundant PDF URL, since its DOI is
  already supplied. Both parts are present and readable; this is pagination
  polish, not a citation failure.
