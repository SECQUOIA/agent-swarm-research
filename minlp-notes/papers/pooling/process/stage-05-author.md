# Stage 5 author record

Author: `/root/stage05_author`. Stage: `sections/05-contract-algorithms.tex`. This is the sole-author development and self-check record, not an independent review verdict. All Stage 5 manuscript labels use the `s5:` prefix. Root owns the forced complete-manuscript build, independent finite checks, review dispatch, and adjudication.

## Scope and manuscript organization

The draft gives full proofs of all five canonical Stage 5 results and the substantive supporting investigations. All 16 Stage 5 coverage rows now have explicit manuscript destinations. Promotion pointers are identified as such; distinct general theorems and certificate guarantees are retained separately.

1. `s5:quasipoly-path` proves the general one-parameter planar-path projection theorem. `s5:strip` separately proves polynomial affine-strip elimination on paths and trees and the fixed total cycle-rank consequence.
2. `s5:fixed-products` proves fixed-outlet optimization with unbounded feeds and arbitrary quality count and rank, using exact source and nonreceiving-product contracts.
3. `s5:conservation`, `s5:cuts`, and `s5:quadratic-field` prove fully contracted scalar/rank-one feasibility and the common quadratic-field witness guarantee. `s5:fixed-boundary` retains the boundary projection dependency. `s5:capacity-counterexample` gives the complete physical example showing why a restrictive common bound cannot be omitted.
4. `s5:quality-chart`, `s5:fixed-rank`, and `s5:arbitrary-exceptions` give the scalar, fixed-rank, and arbitrary-rank exception algorithms, including the complete vector chart construction and the exceptional-only fraction branch.
5. `s5:clamp`, `s5:box-base`, and `s5:restrictive-capacity` prove the common-capacity extension. `s5:throughput-optimization` adds exact minimum/maximum throughput and a linear pool-processing cost as a further completed consequence.
6. `s5:two-vector-theorem` proves arbitrary-topology feasibility for two full source-quality vectors with variable source supplies. `s5:two-vector-extensions` explicitly retains exact supplies and additional outlet resource rows with signed coefficients and nonnegative right-hand side.

The section uses the accepted stage notation, with the explicit local abbreviation `C_i = lambda_i` and exact supplies/demands `a_i,b_j`. Standard revenues are distinguished from the projected quality residual in the exception proof by `R_j^{econ}`. No accepted section was edited.

## Mathematical verification during authorship

### Parameterized relations

I reconstructed the Fourier–Motzkin elimination step with both same-child and cross-child pairs. Signs of augmented minors determine feasibility and omitted-row validity at all candidate vertices, including lower-dimensional bounded fibers. Empty sign cells are explicitly stored as the constant contradiction `0 <= -1`, preventing their candidate lists from accumulating. This addresses root's request to make the empty-cell row recurrence explicit without needing a separate Helly invocation.

Balanced depth gives polynomial row count, degree, and height at each cell and a quasipolynomial total cell count. The overlay recurrence uses the sum of breakpoint counts only in one parameter. Singleton cells retain symbolic polynomial rows evaluated at the same parameter. The feasibility conclusion includes a final minor refinement when the path has one relation. Original LP basis determinants, rather than an unsupported repeated-inversion assertion, justify polynomial common-field witness encoding.

For strips, I checked both signs of every gain and the identity converting bounds to differences. The sufficiency construction `y_i = min_j(U_j + d(j,i))` satisfies every lower and upper bound and every directed adjacent inequality. A zero gain contributes an interval at its original head and disconnects the preceding state. Arbitrary tree orientations require reciprocal gain factors when traversed against their original direction. Forest elimination plus at most two retained endpoints per deleted edge gives the fixed total cycle-rank result. Dense accumulated objectives and generic planar relations remain excluded. Infimum and attainment are distinguished; finite state bounds alone do not ensure compact parameter domains.

### Fixed outlets and conservation

I checked every local intake substitution, including absent feed arcs. Exact nonreceiving-product mass and vector-quality equations imply both affine boundary identities for every lifted path assignment. Detached bypass components may still feed the pool; their freedom does not change these identities. The retained dimension is at most `4r`, and arbitrary attributes add rows rather than concentration variables. At zero throughput, nonnegative intakes vanish and their vector mass is zero. At positive throughput, outlet fractions reproduce the actual pool quality mass. Standard economics, outlet costs, and pool-processing cost use only the retained coordinates. Arbitrary intake or bypass costs do not follow from this proof.

The exact-quality negative control is included in the text. Treating a nonreceiving product's quality upper bound as an exact quality would make its conserved mass substitution false.

### Signed cuts and quadratic witnesses

I reconstructed the outgoing-minus-incoming convention and the root-arc reduction to signed circulation. Both cut families and whole-component inequalities are necessary. Disconnected sets add over connected components. Paths, cycles, and isolated vertices have the claimed polynomial connected-subset inventory.

For every scalar output case I checked the exact algebra: distinct source qualities give a quadratic interval on one transformed arc; equal qualities give parameter conditions; one inlet gives an affine interval and node equality; zero inlets preserve the homogeneous residual and outlet bounds. Bounds are ordered using the actual fixed signs, and transformed flows are permitted to be negative. The all-candidate conjunction correctly realizes maximum lower and minimum upper bounds on cuts of size at most two. Singular source qualities are handled by the original physical LP. New isolated quadratic roots within nonsingular charts remain included.

The witness concentration is rational in a feasible open interval or a root of a rational quadratic at a boundary. Constant incidence matrices and a single division by each nonzero source scaling keep all flow coordinates in the same field. Rank-one affine compression preserves homogeneous zero-demand semantics and every flow bound. The explicit common-capacity counterexample computes `T = 1/[q(2-q)] >= 1` for qualities 0 and 2 and product qualities 1/2 and 3/2; capacity 3/4 therefore destroys otherwise valid local feasibility.

### Contract exceptions and arbitrary ambient quality

I checked the retained physical interface counts and the total mass and every quality equation in the core. Those global equations imply actual pool balance for every residual lift, including zero throughput.

The explicit direction family has polynomial size even when ambient dimension grows. Each nonsource vector excludes at most `K-1` members; coefficient bit lengths are polynomial. Source-vector branches are included only when the vector belongs to the selected affine space and its quality box. The chart lemma now explicitly includes the closed coordinate box spanned by allowed feed vectors in its statement. This corrects a statement/proof mismatch identified both in self-check and by root; no inactive quality outside that box is silently included. The final arbitrary-rank theorem covers inactive flows through its exceptional-only branch.

I expanded the extra coordinate equations independently. Their coefficients have the asserted affine/quadratic degrees after cancellation. Zero residual coefficients require the corresponding pure parameter equality; nonzero coefficients supply rational equality bounds with known denominator sign. Every quality equation is retained even for equal projected source qualities. Degree-two cuts use at most two rational candidates, so clearing only those denominators preserves constant degree. Strict nonzero chart conditions are not replaced by closures.

The active ordinary-product identity places pool quality in an affine space of dimension at most two. The exceptional-only branch instead uses conserved vector masses and outlet fractions, with core dimension at most `3|E_I| + 4|E_J|`. Both branches are sound and their union is complete. Standard economic profit is affine in retained external throughputs. A fixed set of extra cost arcs can be included by designating their external endpoints as additional exceptions while retaining original contracts. Arbitrary dense costs and restrictive common bounds remain outside this exception theorem.

### Common capacity and further throughput optimization

I checked the two binary dynamic-programming recurrences and their difference. Subtracting prefix unary sums makes every clamp state a member of a linear-size common list. Pairwise sign conditions fix every clamp, increment, and terminal choice. Cycles are solved by conditioning a first label and absorbing its incident edge into a unary term. The lemma applies to binary submodular energies, not generic bounded-treewidth continuous optimization.

The bounded-divergence base proof includes signed arc bounds, submodularity of the shifted nonnegative cut, product-lattice submodularity of box truncation, and normalization using nonemptiness. The reverse inclusion recovers both sides of the node box from singleton and complementary-set tests. I supplied the diminishing-increments proof of greedy feasibility and the telescoping support inequality for arbitrary signed costs and ties.

The common-capacity construction checks local nonemptiness before invoking support. Source reciprocal costs have fixed order on nonsingular source-quality intervals. Prefix-rank minimizations are quadratic binary path/cycle energies. Univariate refinements are a union of all breakpoint sets. The support functions have polynomial degree and coefficient height after a common known-sign denominator is introduced. Interpolation between two realized extremal divergence flows gives every feasible throughput in the required interval and stays in one represented algebraic field.

Root proposed exact throughput optimization as an additional consequence. I independently checked it and supplied `s5:throughput-optimization`: retain `(q,T)`, impose the support-derived interval inequalities, include singular LP throughput intervals, and project the actual-cell union. It equals the original compact attainable pair set. The extrema are attained and recoverable by the same flow interpolation. This adds a linear pool-processing objective while making no arbitrary arc-cost claim. The stronger class has polynomial-degree witnesses; no quadratic-field claim is extended to it.

### Two-vector convex feasibility

I checked full-vector affine normalization and positive-demand compatibility. Two distinct complete source vectors are not the same restriction as two attributes. The variable-supply proof retains scaled actual withdrawal and scaled actual intake, not only bypass variables. Exact products determine class consumption totals; the two class equations recover both global mass and actual pool mixing. The outlet identity holds for arbitrary bypass degrees, including an absent source class at an output. Outlet and common upper capacities share the same concave `q(1-q)` factor.

Replacing that factor by `q-r` gives an exact existential reduction with the sole convex condition `q^2-r <= 0`. Nonnegative capacity coefficients are essential. The closed polytope is bounded and rational. I checked the strict-interior LP and all three exact QP minimum cases: a positive minimum rejects; a zero minimum has one common quality among all minimizers; a negative minimum can be mixed with a rational interior-polytope point using the explicit polynomial-bit coefficient in the proof. Endpoint artifacts are handled only by the original physical LPs. Recovering every original flow divides by nonzero rational class factors and gives the stated polynomial rational witness.

The exact-source specialization is retained explicitly, as are outlet resource rows with arbitrary coefficient signs but nonnegative right-hand side. Positive outlet or common lower bounds have the opposite curvature and are excluded. Source procurement is variable in the stronger class; feasibility does not imply its optimization.

## Sources and attribution

Imported literature was read-only. Existing bibliography entries were reused unchanged. Three verified entries were appended, with all citations attached to the actual primitives used:

- Schrijver, *Combinatorial Optimization*, Part I, Corollary 11.2i, printed p.175, and Corollary 11.3a, p.176. Primary PDF: <https://www.lamsade.dauphine.fr/~cornaz/Enseignement/M2_MODO/DATA/A1.PDF>. The text explicitly permits real signed bounds; its incoming-minus-outgoing convention is opposite to the manuscript's divergence convention. The subsection proves the translation and connected-cut specialization.
- Shioura, Shakhlevich, and Strusevich (2013), Theorems 1–2 and equation (11), printed p.192. Primary PDF: <https://eprints.whiterose.ac.uk/id/eprint/78189/10/shakhlevich1.pdf>. The paper states the box rank formula and greedy rule for maximal vectors of a box-truncated submodular polyhedron. The manuscript proves the particular nonempty base-intersection specialization and normalization. No independent reading of earlier references credited there is claimed.
- Kozlov, Tarasov, and Khachiyan (1980), Russian original pp.1320–1323, including numbered paragraph 3 for rational optimal solutions and determinant bounds and paragraph 6 for optimizer recovery. Record: <https://www.mathnet.ru/eng/zvmmf5189>; primary PDF: <https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt>. The exact convex-QP primitive was checked in the full primary extracted text, not inferred only from its title or metadata. Root independently confirmed these locators and corrected an early informal message's paragraph number from 7 to 6.

I also checked the cited quantifier-elimination and sample-point passages in the local full text of Basu–Pollack–Roy (Theorem 1.3.1 and Sections 3.1.3–3.2) and the common-field rational-bit discussion in Adler–Beling (Section 5, Remark 1). The previously accepted planar path theorem is reused with its exact boundedness and field-lifting hypotheses. Existing Boland–Kalinowski–Rigterink and Baltean-Lugojan–Misener keys are reused for the bounded model comparison; no exhaustive priority claim is made.

Browser PDF screenshot requests returned references rather than viewable page images. Thus source verification here means primary extracted-text inspection, not visual page verification. An attempted shell download returned HTTP 403 and produced no source artifact. No third-party PDF or image is packaged in the manuscript tree. Root requested any future source downloads go under `/tmp/pooling-paper-sources`; none were needed afterward.

## Validation and limitations

Root read the canonical proofs and manuscript independently, ran the selected finite checks, and forced the full build. Its detailed evidence is in `process/root-stage-05-check.md` and the retained verification logs. The complete draft built to 73 pages with no final warnings. Root also ran the distinct 1,200-case exact affine-strip test after the first eight selected checks. I did not duplicate those routine runs. Their exact-versus-numerical limits remain explicit in root's record; they do not prove general symbolic complexity or replace these proofs.

This draft is ready for the required 15 complete independent reviews after freeze. It has not passed that new review round yet. No later-stage text was drafted, no reviewer was spawned by the author, and no historical PASS was treated as a mathematical premise.

Accepted sections 1–4 remain at their assigned SHA-256 hashes:

- `01-foundations.tex`: `e023daa9d8ceb445d931e193dce9d47ae1934e17ac13b54d4591710e3f8f76ae`
- `02-algebraic-complexity.tex`: `8abd1d862cc58d23ee4671f2610c02ca04c27390353ba023b442325565514e67`
- `03-restricted-hardness.tex`: `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40`
- `04-structural-algorithms.tex`: `88b1c181cde7f72b48535054de702a2ff4688a470633eb56e528c519974189de`
