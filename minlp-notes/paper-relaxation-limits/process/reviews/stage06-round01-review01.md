# Stage 6, round 1: independent review 01

**Verdict: PASS.** I found no demonstrable major or minor defect. This verdict concerns the frozen integrated manuscript and the claims it actually makes; it does not settle its stated open problems or replace the separate final review loop.

## Coverage

I reviewed `process/snapshots/stage06-round01`. Its 111-page `main.pdf` has independently checked SHA256 `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read the frozen review protocol, Stage 6 review and author assignments, complete Stage 6 author record, scope proposal, and claim-coverage ledger. I read the entire manuscript source, including proofs, appendices, bibliography, abstract, introduction, roadmap, and synthesis. The exact manuscript files are `main.tex`, `macros.tex`, `references.bib`, and all the following files under frozen `sections/`:

- `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`.
- `07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`.
- `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`.
- `appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`.
- `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

The full-paper reading included the dependency chains underlying the new comparisons, rather than treating earlier acceptance as proof. I consulted frozen author verification records and existing primary-source locator notes to identify checks and originals. I did not read another current-round review. I did not edit the manuscript or snapshot or delegate work.

I read `literature/AGENTS.md` before local originals. The following are direct primary-source checks. A PDF page is a one-based page in the file, unless a printed page is explicitly named. Local slugs below refer to `/workspace/minlp-notes/literature/papers/<slug>/original.pdf`; temporary filenames refer to `/tmp/minlp-relaxation-limits-sources/`. This is a record of selected passages, not a claim to have read every cited source in full.

| Source | Directly checked passage and purpose |
| --- | --- |
| `luedtke2012-some-results-on-the-strength` | PDF 5–8, 22: unit-box recursive relaxation, vertex-law formulas, common positive upper envelope, and original conjectural scope. |
| `boland2017-bounding-the-gap-between-the` | PDF 3–5: signed bilinear bounds, cycle exactness, and cut identities. |
| `davidson2007-norms-of-schur-multipliers` | PDF 2–4, 6–7: real projective comparison and weighted density theorem; integer and fractional density are distinct. |
| `sherali1997-convex-envelopes-of-multilinear-functions` | PDF 8–9, printed 252–253: positive-box formula and Theorem 3. |
| `adams2018-error-bounds-for-monomial-convexification` | PDF 22: Proposition 4.1, common-aspect-ratio envelopes and its cited provenance. |
| `cornuejols-packing-covering.pdf` | PDF 78 and 84, printed 76 and 82: Theorems 6.5 and 6.13, including the distinction between Camion's criterion and balanced unit-right-hand-side integrality. |
| `hassin-tamir.pdf` | Visually read PDF 3, printed 381: Theorem 3.1 and terminal series/parallel constructions. |
| [Deza–Onn, Optimization over Degree Sequences of Graphs](https://arxiv.org/html/1908.09278v1) | Section 3, Theorem 1.2 and proof: convex degree costs reduce to matching through ordered marginal costs. |
| [Edmonds, Maximum Matching and a Polyhedron With 0,1-Vertices](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf) | PDF 1–2: weighted matching algorithm statement and matching-polytope theorem. |
| `gls1988.pdf` / corresponding extracted text | Printed 179–180: Theorem 6.4.9 and proof, with the well-described rational-polyhedron and oracle-polynomial qualifications. |
| `altschuler2023-polynomial-time-algorithms-for-multimarginal` | PDF 55: Theorem 7.4, Corollary 7.5, and the logarithmic-accuracy question. |
| `schoenebeck-full.pdf` | PDF 7–11: definitions, Theorems 11–12 and the local-vector construction used for the XOR dependency. |
| `anstreicher2009-semidefinite-programming-versus-the-reformulation` | PDF 12–13: the point-packing model and Conjecture 4. |
| [Khajavirad, Convex relaxations for the maximum separation problem](https://arxiv.org/html/2404.03091v1) | Propositions 1 and 3 and accompanying relaxations: the published point-packing values, symmetry restrictions, and RLT redundancy. |
| `balas1998-disjunctive-programming-properties-of-the` | PDF 5–7, printed 7–9: Theorem 2.1 and disjunctive-hull proof. |
| `wu2026-variable-aggregation-based-perspective-reformulation` | PDF 12: Lemma 3 and Theorem 3 statements. The deferred supplementary proof was not independently audited. |
| `starr1969.pdf` | PDF 12–13, printed 35–36: Shapley–Folkman lemma, corollary and proof. |
| `kronqvist2026-p-split-formulations-a-class` | PDF 4–6 and 15–16: Assumptions 1–4, Remark 1, actual formulation, Definition 4, Corollary 3, and Theorem 6 with proof. |
| `fawzi2013-exponential-lower-bounds-on-fixed` | PDF 3: Theorem 1, exact fixed-block lower bound and Lorentz-cone consequence. |
| `lrs-sdpsize.pdf` | PDF 23 and 32–34: Theorem 3.8 and equation (3.11), Theorem 5.3's pseudodensity proof, and Theorem 5.4. |
| `braun2013-approxlp.pdf` | PDF 18: the hard pair and Theorem 6(i), including its fixed dilation. |
| `ey-rmc.pdf` | PDF 26–28: Theorem 5.2 and the normalization, detection and amplification construction. |
| `belotti2012-on-feasibility-based-bounds-tightening` | PDF 1–2: scope of the linear-programming FBBT result. |
| `stewart2015-upper-bounds-for-newtons-method` | PDF 21–22: equation (18), the squaring construction, and Newton-method scope. |
| `esparza2010-computing-the-least-fixed-point` | PDF 34: equation (14), Theorem 7.1 and local proof. |
| `lubin2022-mixed-integer-convex-representability` | PDF 12: midpoint Lemma 4.1 and proof. |
| `beach2024-enhancements-of-discretization-approaches-for` | PDF 21 of the stored combined preprint: Section 5.1.1 and the sawtooth upper/lower error constants. |

Source limits are stated below. In particular, the table should not be read as an independent reproof of the full matching, ellipsoid, XOR, or extension-complexity literature.

## Findings

None. There are no major or minor finding IDs and no requested repairs.

## Independent verification

### Envelope foundations and every law construction

I reconstructed the vertex-law lemma by conditionally rounding each coordinate independently to its two box endpoints. Multiaffinity preserves the conditional objective and all means; the resulting finite marginal polytope is compact. Thus extrema, rather than merely infima and suprema, exist. The common threshold law attains every positive monomial's upper envelope simultaneously. The distinction between the graph hull gap and the specified termwise gap remains necessary throughout: affine addition preserves the former, and nonnegative expansion gives the stated one-sided comparison for the latter.

I checked the following law constructions, including their uses later in the paper:

- Independent, opposite-orientation and cubic baseline laws preserve deterministic coordinates and all intermediate means. The case splits at one half agree, and zero term deficiency needs no division by that deficiency. The three-law certificate proves its stated family guarantee; the paper does not mistake its optimal mixture for the unknown sharp cubic constant.
- The harmonic law has integral marginal `p`, including the separately defined `p=0` endpoint. The completion formula `q1=q0+(q-m)(1-q0)/(1-m)` remains in `[0,1]`, has the required integral, and is only used where its denominator is positive. Mixing the laws is global across terms.
- Ownership uses measurable circle unions with the required lengths, including zero lengths and coordinates without owned terms. Feedback conditioning retains nonnegative residual mass; zero-mass branches require no conditional law. Forest gluing has consistent shared-coordinate marginals. The odd-cycle matching/complement construction preserves the baseline marginals.
- Uniform adjacent-cardinality subsets give the prescribed coordinate means. In coefficient removal, the clone-all-equal law proves one envelope direction and conditional Bernoulli cloning proves the reverse; deterministic original coordinates cause no undefined conditional probability.
- The multiscale lower construction mixes adjacent radix profiles with capacity `M_q=((L-q)(b-1)+b)/b^q` to achieve expected size one. Uniform shifts make every leaf's failure marginal `1/m`. Digit reversal supplies the required nested-block coverage. The exact dyadic claim is kept separate from the simplified large-radix regime.
- Positive-box spreading retains the same ambient balanced orientation after deleting deterministic coordinates. The extremal transfer uses the global smallest and largest free means. Replacing that law with a newly balanced law on each support would change the opposite-pair probability and invalidate the argument; the manuscript does not do so. Order-zero and order-one deficiencies vanish, so the coefficient-regularity hypothesis is needed only from order two onward.
- Scale perspective attainment uses the size-biased distribution and the common operating variable exactly where required. The rectangularity counterexample respects the retained shared variable. Common-law statements are not silently extended to separate per-term distributions.

I wrote `verification/reviewer01/stage06-round01/check_laws.py` independently, using only exact rational arithmetic. Running `python3 verification/reviewer01/stage06-round01/check_laws.py` passed:

| Check | Exact finite coverage |
| --- | --- |
| Quadratic/cubic marginal preservation and `18 D_O + 6 D_I + 7 D_B >= 12 t` | 810 mean vectors, all coordinates on the eighth grid including 0 and 1. |
| Balanced ambient coefficient inequalities | 7,920 inequalities, ambient dimensions 2–5, means in `{0,1/2,1}`, every prefix restriction, and all checked coefficient orders including vanishing orders. |
| Radix capacities and mean-one mixtures | 55 profiles, bases 2–6 and depths 2–12. |

These finite checks exercise degeneracies and independently computed distributions. They do not prove the continuous inequalities or the universal radix geometry; those were checked by reading and reconstructing the arguments.

### Remaining proof dependencies

For signed bilinear gaps I checked the induced-cut characterization, polarization factors, density orientation argument, random-sign lower bound, and the transfer from the weighted Schur result. I separately executed the printed exhaustive signing program extracted from the frozen appendix; its values for orders 2–7 were `[1,2,4,4,5,8]`. This reproduces the supplied finite proof algorithm, rather than constituting a second independently designed enumeration.

For structural exactness I followed every case of the stronger one-sided terminal invariant in the series/parallel induction. The incidence argument uses the full Eulerian-submatrix condition where needed. The signed-factor example is not used to contradict positive-monomial exactness. The convex-degree matching reduction and dummy/parallel-edge degree-slab argument handle zero degree and endpoint slabs without changing the claimed model.

For cubic and equal-mean obstructions I checked the scalar Bernstein inequalities, two-level identities, and the admissible cardinality mixtures. I also ran the appendix's extracted finite cubic checkers in fresh Python namespaces. All claimed checks passed, including 275,697 three-group count states and 564 two-group states. The printed rational envelope values and ratios were reproduced. This is reproduction of the printed code, not a universal computational proof or an independent search for extremizers.

For the exact-complexity reduction I checked the quadratic remainder bound `epsilon^2/8`, the integral variance gap, rational input length, and the at-most-`n+1`-atom certificate. The conclusion distinguishes exact or logarithmic-accuracy hardness from fixed-error hardness. The rational-polytope condition needed for oracle equivalence is present.

For fractional cardinality I checked nonnegativity of `(t)_(2d-j)(s-t)_j/(s)_(2d)` over the stated range without canceling a potentially zero factor. Conditioning on an indicator is only normalized when its weight is positive; constants and `v=s` are covered separately. Tensor positivity uses an actual principal submatrix of the product moment matrix for total-degree coupled squares. Endpoint graph interpolation is affine in each formal Boolean coordinate, so it does not spend extra order under the paper's coordinatewise hypotheses.

For XOR I reconstructed the signed-character Gram transfer, deterministic substitution, and the explicit low-order cut law. The exact quadratic law is permitted to leave the algebraic graph because the relaxation uses the full coordinate-box hull. I checked the degree charges for the slack indicator square, including the `r=1`, `rD>=2` case. Rank bounds use support unions, so repeated factors do not increase the count. The bounded-incidence deletion inequalities `7n<=m<=8n`, maximum degree 64, and the resulting spatial constants agree. The order-one upper certificate uses graph equations in expectation and a valid quadratic box cut; it does not assume an unavailable cubic multiplier.

### Stage 6 comparisons

For point packing I checked the covariance projection, all five QQ/QH/QF/HH/HF entry types, and the resulting PSD certificates. The symmetry secants and block sizes are compatible with the stated `n>=5` range; collapsed side lengths cause no division by zero. The published values and the manuscript's explicit reconstructions agree.

For scale disjunctions I checked equal extreme scales, zero mixing weights, multiplicities, compactness at zero perspective weight, retained shared variables, and the rounding step. The proof separates unrestricted convexification from cost separation with a shared operating variable. The fixed-scale and rectangular cases have the hypotheses used in their attainment proofs.

For P-split I reconstructed the retained-box witness: its relevant vertices lie in the feasible balls and the displayed split lift is feasible. I checked the fixed-coordinate truncated-square minimization, the translated capsule projection, and the Hausdorff-distance maximization. The rational rotation is an exact coordinate change. The manuscript targets the universal theorem statement in the source, preserves the actual formulation, and states the additional feasible-set validity required by the directional repair.

For rank one I reconstructed the exposed correlation face, affine inverse, and rounding bounds. The estimate `||r-c||_1<=2 S D` leads to the stated `136m+10` error bound; the stronger section construction uses `184m+6`, and the projection factor is `m(184m+6)`. I checked the pseudodensity's negative margin, the `k^(-23/4)` prefactor and the scale `k` of order `(m/log m)^(2/13)`. Exact cone-size statements and approximate formulations use different hypotheses and are not converted into spatial leaf counts. The facial-reduction/factorization passage accounts for the extra scalar block.

For primitive FBBT I checked that every contraction retains the least fixed point, and that fairness alone yields finite-sweep domination without requiring a bounded delay. The PosSLP construction preserves complements and least-solution semantics; its amplifier separates value 1 from at most `1/8`. In the slow example, `l_w<=c l_z` is invariant, and each relevant affine update satisfies `l_z<=b+c l_z`. After `K` such updates the bound `l_z<=Kb` implies the stated doubly exponential update count. Exact upstream initialization only strengthens the comparator. This does not claim a lower bound for accelerated propagation or general solvers.

For the integer comparisons I checked midpoint parity classes, the closure/compactness step, the square-root diameter estimate, the product-region area `16 epsilon log 2`, and the width `20 epsilon`. The fractional vertex-cover coefficient follows with the stated precision convention. These arguments retain their own formulation and accuracy parameters.

### Integration and rendering

The abstract, scope ledger, theorem statements, appendices, and synthesis distinguish proved results from the remaining sharp constants and classification questions. I found no unsupported change from a restricted family to a universal theorem and no conversion between incompatible measures of difficulty.

A source-level reference check found 341 labels, no duplicate labels, no unresolved `ref`/`eqref`-family references, and no missing bibliography keys in the checked citation syntax. I visually inspected direct renders of PDF pages 1, 95, 104 and 107; text and displayed mathematics on those pages were readable without apparent clipping. The review artifacts are in `verification/reviewer01/stage06-round01/`.

## Remaining limits

- I read all manuscript source, but visually inspected only the four listed manuscript PDF pages. I did not run an independent LaTeX build or visually inspect all 111 rendered pages. The source-level label check is not a substitute for compilation.
- The independent rational checker covers finite grids and small dimensions. The larger finite signing and cubic checks reproduce the printed proof code. I did not rerun every exploratory computation or search in the repository, and none of these finite checks establishes a universal theorem.
- I checked selected original passages listed above, not every bibliography item or every proof in the long foundational sources. In particular, I did not independently audit the full sharp Khinchin proof, the full global LRS rank argument, the entire matching/ellipsoid algorithms, or Wu's deferred supplementary proof. Contextual attributions outside the listed passages have not all been traced through their original proofs. The manuscript explicitly cites these external inputs; this is a verification limit, not evidence that they are false.
- The sharp cubic constant, stronger feedback dependence, unequal-box classifications, and other questions explicitly left open remain open in this review. The tested family-optimality and restricted-model statements do not resolve them.
- This is an independent mathematical review, not formal verification. No defect was found after the stated reconstruction and falsification attempts; PASS should be read with the concrete coverage and limits above.
