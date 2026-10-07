# Stage 4, round 1 — independent review 07

**Verdict: PASS.** No major or minor finding. The full assigned stage, including the new coordinatewise graph-lift theorem and its relative-block transfer, is correct under its stated oracle and cover assumptions.

## Coverage

Reviewed the frozen snapshot `process/snapshots/stage04-round01/`, specifically:

- `sections/09-cardinality-spatial.tex`, in full: optimum, arbitrary-split and cover count, chord domination and common formulations, both upper certificates, propagation charging, feasibility tolerance, quadratic chord error, full augmented SDP–RLT construction, and affine-product closure.
- `sections/10-cardinality-preordering.tex`, in full: normalization and degree conventions, classical moment formula, cardinality identities, homogeneous reduction, incidence Gram decomposition, assignment localizers, restriction/order threshold, endpoint regimes, perturbation, uniqueness, symmetry and increasing costs.
- `sections/11-coordinate-domains-lifts.tex`, in full: arbitrary product domains, every local polynomial constraint, endpoint interpolation, all lifted equality and localizer products, objective agreement, noncompact graphs, original-coordinate retention, and literal-substitution comparison.
- `sections/12-relative-blocks-cuts.tex`, in full: full tensor positivity under total degree, relative exponent and example, lifted extension with a coupled written objective, squared-index asymmetry, component certificates and clique cuts.
- `sections/01-foundations.tex`, including the graph-hull and spatial-certificate definitions; `macros.tex`; the Stage 4 inputs and bibliography entries in `main.tex` and `references.bib`. No theorem from Sections 02–08 or their appendices is a premise of the Stage 4 proofs. The Stage 4 arguments do not rely on the bilinear results also housed in the foundations file.

Read `process/review-protocol.md`, both Stage 4 assignments, all Stage 4 rows of `process/scope-proposal.md`, the complete author ledger `process/stage-04-author.md`, and `process/univariate-lift-refinement.md`. Read all six canonical repository sources mapped by the seven scope rows: the five `results/spatial-bb-*-exponential-lower-bound.md` files for the base, SDP–RLT, higher-SOS, product-domain and relative-gap results, and `notes/spatial-bb-known-clique-cut.md`.

Read the relevant historical correction/audit notes: `notes/review-spatial-bb-lower-bound.md`, `review-spatial-bb-second.md`, `review-spatial-bb-sdp-rlt.md`, `review-spatial-bb-higher-sos.md`, `review-spatial-bb-product-domain.md`, and `review-spatial-bb-relative-gap.md`. Also read `notes/spatial-bb-strengthening-novelty.md`, `verification/primary-source-checks.md`, and the Stage 4 author/source-validation records. These were used to identify corrections and source boundaries, not as proofs. No current-round peer report was read. No manuscript or shared verification file was edited.

The frozen manifest check independently matched all 59 existing manifest entries. The new theorem and surrounding oracle definitions on frozen PDF page 59 were visually inspected; the text and equations are readable.

Primary-source checks followed `literature/AGENTS.md`:

| Source | Directly checked material | Result and limit |
| --- | --- | --- |
| Jarre, 2018 author preprint | Local full text, particularly Sections 2–3; rendered original PDF page 4 | Confirms binary fixings and the max-cut SDP comparison. The manuscript makes a suitably limited predecessor statement. |
| Grigoriev, 2001 author manuscript | Local functional construction and Lemmas 1.3–1.4; rendered original PDF page 7 | Confirms the falling-factorial formula, normalization, cardinality identity and stronger classical square-positivity provenance. The subsequent full original positivity proof was not imported or audited; Stage 4 proves its own sufficient result. |
| Potechin, ITCS 2019 | Theorem 1, Example 18 and the knapsack parts of Theorem 44/Corollary 45; rendered original PDF page 8 | Confirms the moment formula and attribution to Grigoriev. No audit of the entire general symmetry machinery is claimed. |
| Padberg, 1989 | Local Lemma 2/equation (17), rendered original PDF page 11, printed page 149 | The original formula is exactly the cited cut with the full coordinate set and parameter k. The extracted text omits the formula, so the original was essential. The application needs validity, not the separate facet theorem. |
| Coniglio, anonymous review version | Fresh direct browser request to the exact review-PDF URL; shared source-access record | Fresh access returned OpenReview's browser-verification challenge. I did not bypass it or independently read the review appendix. Root's earlier reading is recorded in the shared log. The bibliography expressly identifies the review version and the unverified identity with the published version. This remains an external contextual-source limit, not a premise of the Stage 4 theorems. |

## Findings

None. No repair is required by this review. In particular, the earlier incorrect maximum in the witness count, unrestricted tolerance slogan, omitted intermediate tree nodes, final-leaves-only propagation claim, and stale open SDP statement have not reappeared in the frozen stage.

## Independent verification

The following are analytic reconstructions, separate from the finite checker.

1. **Optimum, chords, covers and upper bounds.** A slice vertex has k ones and one half coordinate; two fractional coordinates admit a feasible opposite perturbation. Thus concavity gives minimum 1/4. The chord difference is `(x-a)(b-x)`, and convexity of any underestimator bounds it by the endpoint chord, including degenerate intervals. At a contained witness only restricted middle coordinates contribute, with each contribution less than `1/(2m)`. The avoidance events for the zero and unit classes need not be independent: each gives a marginal upper bound, and their minimum suffices. Taking a reciprocal produces the stated minimum of exponential bases. The final union bound allows overlap. Empty endpoint classes and q=0 give the stated trivial cases.

   The three-interval construction creates four nodes per surviving prefix, hence `2^(n+2)-3` nodes and `2^(n+1)-1` leaves. The exact midpoint recurrence is `L(a,b)=L(a-1,b)+L(a,b-1)` with boundary value one, giving `binomial(n+1,k+1)` leaves. For feasibility tolerance the sum stays strictly between k and k+1 precisely in the stated small-tolerance regime; minimizing the remaining fractional penalty gives `1/4-delta^2`. Exact-balance witnesses remain feasible. Charging every certified discarded region gives at most `(a+1)N` cover members; there is no unsupported closure step for an open slab.

2. **All second moments.** The unrestricted covariance is exactly `(c-d)(I-J/s)`, with `c-d=t(s-t)/(s(s-1))`. Restricted rows have zero covariance. This verifies full augmented PSD, rather than a principal submatrix alone. Distinct free-index RLT expressions are `d`, `c-d`, `c-d`, and `(s-t)(s-t-1)/(s(s-1))`; repeated free indices give `c,0,0,1-c`. A restricted index factors out a nonnegative deterministic slack, including a singleton interval. The row sums give every equality product and the objective is precisely the restricted middle penalty. The order-one preordering is exactly this model. Affine Farkas representations on a nonempty, possibly degenerate, polytope include a nonnegative constant; expanding their products uses only existing moments and balance products.

3. **Higher-order positivity.** The cardinality recurrence uses subset size at most `2d-1 <= s-1`. Homogeneous replacement yields `P-H=eQ` in the Boolean quotient with `deg Q <= d-1`; multiplication by `P+H` therefore uses only permitted equality multipliers. The Gram-entry sum factors as `(t)_(2d-ell)(s-2d+ell)_ell`, without dividing by a potentially zero numerator. Its incidence matrices are Gram matrices and its coefficients are nonnegative in the stated range.

   Repeated/conflicting slack factors reduce to assignment indicators or zero. The uncancelled indicator moment is `(t)_(a+c)(s-t)_b/(s)_(a+b+c)`. A nonconstant square forces `a+b <= 2r-2`, making the conditioning weight strictly positive. After assignment, `v+2d <= 2r` proves all remaining dimension and two-sided cardinality hypotheses. Constant squares, zero weights and assignment of all variables require no undefined conditional functional. This verifies arbitrary global square polynomials. The negative-indicator example correctly explains the full-preordering boundary, independently of the stronger classical moment-matrix range.

   The integer implication `|R| < k-2r+2` leaves at least `2r-1` unit witness coordinates, and likewise for zeros. This is the source of the exact q_r formula. The r=1 remaining-dimension case is handled. The constructed objective is strictly below the non-strict pruning target, including R empty. The text distinguishes positive q_r from q_r linear in n.

4. **Graph lifts, the focus of this review.** Every auxiliary is a finite real number at every point of the full interval, so every original witness and optimizer has a true graph tuple. On a restricted coordinate the substitution is evaluation at that tuple; on an unrestricted coordinate every lifted variable is replaced by its affine endpoint interpolation. Thus lifted degree cannot increase, regardless of auxiliary polynomial degree or absence of a polynomial formula.

   Retaining x maps the original balance to the same affine cardinality relation. Each allowed balance multiplier retains degree at most `2r-1`. A local inequality has nonnegative values at the selected witness or at both actual endpoint tuples. Its Boolean reduction is a nonnegative endpoint-indicator combination. After grouping repeated local factors, each distinct nonconstant coordinate consumes at least one original lifted degree, so the indicator times the substituted global square stays within the assignment-localizer budget. A local equality reduces to zero, and multiplication by every allowed global polynomial preserves zero reduction. The same argument respects available full-product-graph polynomial identities.

   Full-graph agreement of the objective is used at Boolean assignments that need not satisfy the balance. It implies equality of the two multilinear reductions and hence equality of their moment values. Agreement only on the feasible graph would not justify this step; the manuscript explicitly requires the stronger assumption. This is a pullback of a functional, not a continuous identity between a nonlinear function and its chord. Exact preimages supply endpoint and witness membership even for disconnected or nonclosed restrictions. Neither graph compactness nor a hull theorem is used. The no-order-loss result is therefore valid as stated. Literal polynomial substitution independently gives the weaker rD result; its balance-product bound is `1+D(2r-1) <= 2rD`.

5. **Relative tensor transfer and perturbations.** Each block localizing matrix is PSD on block monomials through the global square degree d, since `deg(g_b)+2d <= 2r`. The tensor product is PSD, and its principal submatrix indexed by global total degree at most d is exactly the requested global localizing matrix. Unused tensor entries require no globally available high-degree moments. Equality products factor monomial by monomial. This covers squares coupling every block, also in lifted variables.

   Lightly restricted blocks use fractional moments; heavily restricted blocks use actual witness evaluation. Both have penalty at most `|R_b|/(2q_0)`. Summing and comparing with `(1-theta)C*` yields `sum |R_b| >= 2q_0 G tau`. Independent block sampling, together with the within-block marginal avoidance bounds, gives exponent `q_0 G tau`. The explicit arithmetic is `tau=17/128` and exponent `17n/384`. Boolean reduction also verifies a lifted objective written with cross-block terms, provided full-graph agreement holds.

   Strict concavity excludes nonvertex minimizers, and sorted positive coefficients uniquely minimize the linear objective over the entire slice by mass transfer. Unit first-moment bounds justify the perturbation estimate. A feasible-set-preserving permutation maps whole blocks to blocks through the balance row space; squared-index successive differences prevent translations between distinct block coefficient lists. Distinctness then excludes permutations within a block. This addresses objective equality modulo balances, rather than merely polynomial equality in ambient space.

6. **Escape and attribution.** The clique polynomial is multiaffine and equals `(s-k)(s-k-1)` at a Boolean vertex with s ones. It is therefore nonnegative on the full continuous cube. Equality products give total matrix sum K squared; the cut bounds the trace by `k+1/4`, giving penalty at least 1/4. The separate linear-program minimum is attained at the same optimizer, so the perturbed/increasing objectives and each relative block are also exact at the root. PSD is unnecessary for this deduction. These coupled cuts and reusable component certificates are properly outside the stated local-oracle/global-cover model. The text does not claim inherent optimization hardness or identify this family with the earlier positive multilinear examples.

An independent supplemental checker is saved at `verification/reviewer07/stage04-round01/check_review07.py`, with output `check_review07.json`. Running it with `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python` passed:

- 20 symbolic Gram-entry polynomial identities through d=5;
- 77 exact midpoint tree counts and 462 exact small-tolerance endpoint evaluations;
- an order-two graph construction with k=m=z=5, one middle coordinate fixed to 1/10, and the everywhere-finite nonpolynomial map `psi(0)=0`, `psi(x)=1/x` for x>0;
- 84 balance-times-monomial checks and 93 graph-equality products, using the valid cubic identity `x^2 y-x=0`;
- a coupled degree-four written objective differing from the original objective by a graph identity times another coordinate's auxiliary;
- 55 localizers with a square coupling all 15 local blocks, plus 715 repeated degree-four local products;
- 25 negative-indicator boundary probes and exact relative-example arithmetic.

All arithmetic in that checker is symbolic or rational. The selected unrestricted domains may be `{0,1} union (0,1/2)`, so the test also uses a nonclosed preimage and an unbounded graph. These finite tests support the stated degree and boundary calculations; they do not establish universal positivity or quantify over every polynomial constraint. Those conclusions come from the analytic proofs above. Source renders and the independent manifest result are stored only under the assigned verification directory.

## Remaining limits

Fresh Coniglio appendix access was unavailable as described above, and identity of its review and published versions remains unverified. No exhaustive priority search was performed. The full external proofs of Grigoriev's sharper positivity theorem and Potechin's general symmetry theorem were not audited because Stage 4 does not invoke them as mathematical premises. I did not rerun the cumulative LaTeX build or reproduce every author test; I verified frozen integrity, visually inspected the new theorem, and ran the independent exact checker described here.

Optimality of the order/region tradeoff for other functionals or stronger oracles remains outside this review. The paper explicitly excludes coupled auxiliary functions, arbitrary coupled cuts, elimination of the original affine balances, and exact optimization of the feasible graph. None of these limits leaves a required claim in the assigned stage unproved.
