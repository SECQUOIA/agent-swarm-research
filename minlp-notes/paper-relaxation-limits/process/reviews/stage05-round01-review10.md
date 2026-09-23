# Stage 5, round 1 — independent review 10

**Verdict: PASS.** No major or minor findings. The strengthened order-one lower transfer and the separate order-one upper certificate are valid under the stated oracle. The whole-stage proof and source review below is independent; the additional emphasis was the certificate contract across stages.

## Coverage

I read all 779 lines of the frozen Stage 5 manuscript under `process/snapshots/stage05-round01/`: `sections/13-xor-quadratic-hulls.tex` (333 lines), `sections/14-monomial-reformulations.tex` (228), and `sections/15-finite-certificates-affine.tex` (218). These are printed Sections 16–18. There are no new Stage 5 appendices. I checked the frozen `main.tex` inclusion order and the four relevant entries of its `references.bib`; I visually inspected frozen PDF pages 73–74, containing both upper certificates and the start of the affine boundary. No layout defect was apparent there.

Earlier dependencies read directly were the vertex representation and full certified-cover convention in `01-foundations.tex`; the charged reductions proposition and its proof in `09-cardinality-spatial.tex`; the oracle definition and cutoff/coupled-cut boundary in `10-cardinality-preordering.tex`; all of `11-coordinate-domains-lifts.tex`; and all of `12-relative-blocks-cuts.tex`. The earlier fractional-cardinality positivity results are contextual predecessors, not mathematical inputs to the XOR functional. I did not re-review unrelated bilinear, positive-polynomial, or structural chapters.

Process material read: `review-protocol.md`, `stage-05-review-assignment.md`, `stage-05-author-assignment.md`, the complete `stage-05-author.md` ledger, focus 10 in `stage05-reviewer-focus.json`, `order-one-monomial-refinement.md`, and the Stage 5 scope/notation/dependency rows of `scope-proposal.md`. I checked the source locators in `verification/stage05-primary-sources.json` against the files themselves, including SHA-256 equality for all four originals. I did not use the author's or earlier reviewers' PASS labels as proof, read other current-round reports, edit the manuscript, or delegate work.

All seven canonical/correction sources mapped by the ledger were read completely, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`.
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`.
- `notes/spatial-bb-affine-branching-barrier.md`.
- `notes/review-spatial-bb-beyond-clique.md`.
- `notes/review-spatial-bb-beyond-clique-second.md`.
- `notes/review-spatial-bb-bounded-monomial-lift.md`.
- `notes/review-spatial-bb-affine-branching-barrier.md`.

I read `../literature/AGENTS.md` before accessing primary originals. Primary-source access and scope:

- **Schoenebeck, author full version**, `https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf`, local `/tmp/minlp-relaxation-limits-sources/schoenebeck-full.pdf`. Read its entire 19-page extracted text, with close reconstruction of the random model, Definition 10, Theorems 11–12, Lemma 13 and its complete signed-character proof, and the appendix width argument. Visually inspected original printed pages 7, 8, 10, 11. The actual constant vector is unit length; the immediately following norm-zero sentence is a source typo and is not imported. The chosen gamma avoids the source's singular three-variable illustrative boundary. The manuscript's proof also supplies the equivalence-relation and general-polynomial Gram details explicitly.
- **Ahmadi–Dash–Hua–Stellato, arXiv 2605.28674v1**, local `../literature/papers/ahmadi2026-disjunctive-sum-of-squares/original.pdf`. Read the abstract and introduction/contribution statements, Definitions 1–2, Theorem 1, Sections 6.1–6.2 through the Algorithm 3 tolerance specification, and the closing discussion. Visually inspected printed page 32. Checked the actual region, SOS bound and scaled positive-tolerance conventions. I did not independently establish every theorem of this paper.
- **Beame et al., arXiv 1710.03219v3**, local `/tmp/stage05-author-sources/stabbing.pdf`. Read the abstract and introduction through Theorem 1 and the surrounding system definitions/comparison. Visually inspected PDF pages 3–4, printed 2–3. The original explicitly uses integer negation and states quasipolynomial-size Tseitin proofs. The bibliographic entry correctly identifies the 2023 inspected version and preliminary ITCS 2018 appearance.
- **Fleming et al., arXiv 2102.05019v2**, local `/tmp/stage05-author-sources/branch-cut.pdf`. Read the abstract and introduction through Theorems 1.1–1.4 and their accompanying explanations. Visually inspected PDF page 5, printed 4. Theorem 1.3 is a bound for CNF encodings; Theorem 1.4 is restricted to SP*. Both restrictions are preserved in the manuscript.

No required original was inaccessible. These are direct checks of the locally available specified versions, not an exhaustive literature search or priority certification. Text extraction used `pdftotext` and visual rendering used `pdftoppm`; attempts to use Python `fitz` found that optional module unavailable, with no resulting access limitation.

## Findings

None. In particular, the full-box moment hull, the continuous feasible graph, and the pseudoexpectation's graph equations remain distinct throughout. No stronger closure or free deletion is silently used.

## Independent verification

### Certificate validity, discarded regions and infima

For every true feasible point in a node, evaluation at that point is a normalized functional satisfying all granted localizers, local equalities, moment-hull membership and, in the lifted setting, all graph equations. Thus each infimum is a valid lower bound. A true graph point cannot be ruled infeasible by this oracle. Conversely, an empty functional set has infimum positive infinity as specified; the lower proof constructs a feasible functional whenever a node contains a Boolean graph witness, so no witness-bearing node can exploit that convention.

The lower bounds use one feasible functional to bound the infimum from above. The upper bounds constrain every feasible functional before passing to the infimum. Neither direction assumes an optimizer of the moment problem exists. Actual convex-hull membership on nonclosed coordinate products requires finite convex combinations, and the constructed Boolean realizing laws are finite and supported in those products. The compact-box separation assertion does not falsely extend to nonclosed domains.

The unlifted witnesses are feasible because XOR clauses are costs, not feasibility equations. Lifted witnesses are true continuous graph points, with distinct original coordinates retained. Covers must include every such point. The paragraph after `thm:xor-transfer`, the general cover definition, and the earlier charged-reduction proposition agree: deleting feasible points by an objective deduction requires certified regions in the count. Pure feasibility deletion removes no graph witnesses. No leaf-only lower bound after uncharged objective propagation follows or is claimed.

Stage 4's coordinatewise graph-block oracle is not imported into Stage 5. The latter grants univariate coordinate inequalities, all continuous graph identities, and the full coordinate-box quadratic hull. In particular it does not grant arbitrary valid coupled inequalities, inequalities using an objective cutoff, or arbitrary products/localizers of box-valid quadratic cuts. The continuous polynomial identity `Phi(h(x))=F(x)` is stronger than Boolean or optimum-only agreement, as the theorem requires.

### Unlifted transfer and signed source

For a witness-containing region, fixing excluded endpoints deterministically and retaining the untouched marginal is legitimate without conditioning. If the original generator-degree sum is a and the square multiplier degree is d, then a+2d<=2r. After endpoint expansion the indicator has degree at most a, and its product with the substituted multiplier has degree at most a+d<=2r. Its square therefore lies within source degree 4r. Repeated factors, opposite signs, arbitrary univariate endpoint values, coupled multipliers and local equalities all obey that budget. The actual original quadratic law can be marginalized and fixed to give exactly every new mean and cross moment.

Clause pseudo-costs lie in [0,1] by positivity of `(1 +/- chi_A)^2`, with degree at most six. At most Delta|R| costs change. Hence a certified region satisfies |R|>=mT*/Delta, has witness fraction 2^(-|R|), and the union bound gives the stated cover count. Overlapping covers and nonintegral thresholds cause no difficulty.

For the signed moment lemma, a PSD unit-diagonal matrix with entries 0 or signs gives signed parallel-vector classes; distinct classes are orthogonal. Fixing the class of the constant vector to one, with independent fair signs on the others, realizes both means and second moments, including deterministic and anticorrelated coordinates.

For the width construction, derivable signs are consistent because opposite signs resolve to the empty contradiction. On supports of size at most floor(w/2), the symmetric-difference relation is transitive since the resulting difference has size at most w. Class orientations yield `y_(I triangle J)` as a Gram entry. This proves positivity for arbitrary square polynomials, not only functions of a single small variable set. Moments of odd top degree are defined directly by derivability; no impossible split of an odd w into two floor(w/2) supports is assumed. Width w therefore supports the stated degree w functional, and source requirements 4r<=w and 4rD<=w are correct.

The source parameters k=3, d=8, delta=gamma=1/4, epsilon_src=0 give positive linear width and a positive denominator 1/4. The source random model uses distinct variables per sampled clause, with replacement between clauses. Independent literal signs induce the manuscript's independent uniform parity signs.

### Random family, constants and asymptotics

For any fixed assignment, violations have distribution Bin(8n,1/2). The exponential-moment argument with t=1 gives exp(-n), and the assignment union bound gives exp(-(1-log 2)n)=o(1). For each original occurrence count, differentiating `(1-p+pt)^(8n)` at t=2, p=3/n, gives `E[D_i 2^D_i]=48(1+3/n)^(8n-1)`. Summing the tail estimate and applying Markov yields the deletion failure bound below 1/8 without independence among degrees. Its intersection with the two high-probability events is nonempty for every sufficiently large n.

After deletion, m>=7n, Delta<=64, and at least n violations remain for every assignment. Multiaffine endpoint minimization transfers OPT>=n/m>=1/8 to the continuous cube. Removing clauses preserves the one source functional, hence all admissible lower orders simultaneously. Absolute tolerance 1/16 and relative tolerance 1/2 both demand target at least 1/16 even with the best incumbent; worse incumbents cannot weaken these targets. The resulting exponents are 7n/1024 and 7n/(1024D).

The derivative and Hessian estimates count one first derivative and two mixed second derivatives per incident clause, each of magnitude at most 1/(2m). Symmetry gives the asserted spectral bound Delta/m.

### Monomial lower bound and order one

Literal pullback maps lifted degree k to original degree at most Dk. Local endpoint expansions produce products of parity indicators, idempotent even with repeated, overlapping, dependent or contradictory supports. For a+2d<=2r their indicator-times-multiplier degree is at most D(a+d)<=2rD; its square is available through 4rD. All allowed multiplied continuous graph identities vanish literally after pullback, at degree at most 2rD.

A lifted linear square pulls back to square-polynomial degree at most D, and each quadratic matrix entry is a signed character moment of degree at most 2D. The signed realization lemma applies; a restricted Boolean coordinate has endpoint mean and is fixed almost surely. The resulting full-box law need not be on the graph.

Objective pullback is exact after deterministic substitution. The affected-clause argument needs square-polynomial degree at most three; rD>=2 gives 2rD>=4. Thus the written lifted proof has no hidden r>=2 premise. For r=1,D=3 the linear objective and quadratic graph equations are available, and width 12 suffices. The original cubic objective still requires r>=2.

A consistent restricted parity matrix of rank q has exactly 2^(n-q) solutions. Selecting basis rows from its own rows gives the same support union C: a column absent from the basis is absent from the whole span. Therefore |C|<=Dq, including arbitrarily repeated supports and unrestricted finite auxiliary count. Combining this with the objective loss proves the count. The pair-plus-clause formulation is exactly equivalent on the continuous cube, uses 2m equations and N=n+2m<=17n, and gives exponent 7n/3072>=7N/52224. The polynomial-region necessity D=Omega(n/log n) is restricted to 4rD<=an and to polynomial growth in original n; no stronger statement in inflated N appears.

### Both upper certificates

For every epsilon>0, M=ceil(3/epsilon)>=1 and h=2/M<=2epsilon/3. The original cube grid has exactly M^n boxes, including M=1 for large epsilon. Clause oscillation is at most 3h/2. The eight-corner Bernstein identity is a degree-three nonnegative combination of coordinate-slack products; order two admits it. The graph transfer identity has a single degree-one multiplier on a quadratic equation, hence total degree three. It is valid in the order-two lifted oracle.

At order one, only the first two moments and the two graph equations are needed. On the whole box, the product discrepancy is at most 2h and the u-times-coordinate discrepancy at most h. The expectation bound on v is thus 3h; after multiplying by either clause sign and dividing by two the lower objective estimate loses at most 3h/2. The displayed q_e is a valid quadratic on the full box, and expanding `eq:order-one-cut-identity` cancels the u*x_k and a_k*u terms exactly. No cubic functional value or pointwise graph support is required. At epsilon=1/16, both constructions yield 48^n regions, which also reach relative target OPT/2 for OPT>=1/8.

An independent exact checker was written and run at `verification/reviewer10/stage05-round01/check_contracts.py`; results are in `check_contracts.json`. It verifies all degree-two graph identities for a deliberately nongraph four-atom law: x1=x2=0, x3 is a fair sign times 1/2, u is that sign, and independent v has mean 1/2. Thus E[u]=E[x1*x2]=0 and E[v]=E[u*x3]=1/2. Real-polynomial pullback of all 21 monomials of degree at most two shows that these two equations span the entire degree-two graph-identity space. Every atom is outside the graph, yet the law satisfies the full-box order-one oracle. For positive clause sign its objective is 1/4, whereas the true graph cost is identically 1/2 on the original node. This supplies a concrete adversarial check against silently replacing the box hull by the graph hull.

The checker also verifies the quadratic upper identity and full-box vertex inequality in 5,832 exact rational cases across 216 unequal or singleton original boxes and both clause signs; it checks the integer deletion bound and all displayed exponent constants. These are finite checks supplementing the universal proof. No floating-point result or finite experiment is used to prove the asymptotic XOR assertion.

### Affine boundary and comparisons

For uniform Boolean moments, E[S]=0 and E[S^2]=n are incompatible with a law on S>=0. The affine normalized coordinate equivalently violates z^2<=z. Symmetry leaves at least half the witnesses, including even-dimensional boundary mass.

For the second obstruction, t<r-1 and t<ceil(n/2) imply enough free coordinates to choose a+1 negative indicators if the fixed sum a>=0. Their degree is at most r-1, and their halfspace localizer has exact value -2^(-(a+1)). If a<0 the constant multiplier suffices. The r=1 conclusion is deliberately vacuous. This proves only the necessity for the specified substituted uniform construction.

The literature discussion preserves the distinctions actually checked in the originals: continuous simplicial/spherical covers with a prescribed scaled tolerance, integer-negation SP trees, CNF encoding size for finite-field CP refutations, and coefficient restrictions for SP* lower bounds. Perfect Boolean unsatisfiability gives only F>=1/m directly; multiaffinity transfers that bound to the cube but does not raise it to 1/16. No inspected source is used to claim a short fixed-gap continuous certificate or a lower bound for unrestricted affine branching.

## Remaining limits

I did not rerun a complete LaTeX build or all author checkers; I reviewed the frozen source, independently reconstructed every Stage 5 argument, ran the separate exact checker above, and inspected selected frozen PDF pages. The reported general theorem truth does not depend on those finite checks. The full paper's introduction/abstract integration belongs to the stated later stage.

The source width theorem remains an external asymptotic ingredient, checked directly in the specified full original and its appendix. The review does not prove priority, polynomial implementability of the exact quadratic-box-hull oracle, stronger coupled-cut closure, or fixed-gap bounds for unrestricted affine branch systems. These are accurately stated scope limits rather than defects.
