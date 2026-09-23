# Stage 4, round 1, independent review 11

**Verdict: PASS.** No major or minor finding. The frozen Stage 4 claims are correct under their stated region, oracle, degree, objective-agreement and tolerance assumptions. In particular, the endpoint-interpolation improvement removes the order loss for the defined coordinatewise graph lifts, and the relative extension handles global square multipliers correctly.

## Coverage

Reviewed the frozen `process/snapshots/stage04-round01/` versions of:

- `sections/09-cardinality-spatial.tex`, in full;
- `sections/10-cardinality-preordering.tex`, in full;
- `sections/11-coordinate-domains-lifts.tex`, in full;
- `sections/12-relative-blocks-cuts.tex`, in full;
- `sections/01-foundations.tex`, in full, particularly `subsec:certificate-model` and the multiaffine endpoint principle;
- `main.tex`, `macros.tex`, the Stage 4 bibliography entries, manifest and recorded build evidence.

There is no separate Stage 4 appendix. These four sections supply their own mathematical proofs and do not use the substantive earlier positive-gap or complexity theorems. I did not repeat the external-source audits of those unused earlier results.

Read `process/review-protocol.md`, `process/stage-04-review-assignment.md`, `process/stage-04-author-assignment.md`, the complete `process/stage-04-author.md` ledger, all Stage 4 rows of `process/scope-proposal.md`, and `process/univariate-lift-refinement.md`. Read all six repository source files listed below. I also read the earlier correction/audit notes `notes/review-spatial-bb-lower-bound.md`, `notes/review-spatial-bb-second.md`, `notes/review-spatial-bb-sdp-rlt.md`, `notes/review-spatial-bb-higher-sos.md`, `notes/review-spatial-bb-product-domain.md`, and `notes/review-spatial-bb-relative-gap.md`, and the literature-comparison/source-access records. These historical notes were used to locate corrections and refinements, not as mathematical premises. No other report from this review round was read.

The coverage check found no missing Stage 4 scope row:

| Source, relative to repository root unless stated | Frozen coverage checked |
| --- | --- |
| `results/spatial-bb-exponential-lower-bound.md` | `eq:cardinality-problem` through `prop:charged-tolerance`: optimum, arbitrary coordinate splits, overlapping covers, chord domination and formulation equivalences, exact positive-tolerance tree counts, the sharper exact midpoint leaf count, small feasibility tolerance and second-order chord error. |
| `results/spatial-bb-sdp-rlt-exponential-lower-bound.md` | `eq:sdp-model`, `eq:box-rlt`, `lem:sdp-witness`, `thm:sdp-cover`, and original-space affine-product closure. Full matrix and repeated indices are retained. The formerly open spatial SDP question is explicitly resolved for this model. |
| `results/spatial-bb-higher-sos-exponential-lower-bound.md` | `lem:fractional-positive`, `lem:assignment-localizer`, `thm:preordering-cover`, `cor:unique-cardinality`, and `eq:increasing-allocation`: homogeneous reduction, positive Gram decomposition, conditioning and degree bounds, noninteger negative-product obstruction, perturbation, unique optimizer, absolute-gap transfer and its relative limitation. |
| `results/spatial-bb-product-domain-exponential-lower-bound.md` | `thm:product-domain-cover`, the exact removed-set charging paragraph, and `prop:literal-lift`: arbitrary nonempty coordinate sets, every permitted local polynomial condition, global multipliers, and the distinct literal-substitution argument. |
| Paper-local `process/univariate-lift-refinement.md` | `thm:local-graph-lift` and its relative consequence: full-interval finite auxiliary functions, retained originals, affine balances, full-graph objective agreement, degree-preserving interpolation, all local conditions, and explicit exclusions. |
| `results/spatial-bb-relative-gap-exponential-lower-bound.md` | `lem:tensor-preordering`, `thm:relative-cover`, `prop:relative-asymmetry`, the explicit example, and component-certificate discussion: global total-degree positivity, light/heavy block split, exact exponent, squared-index coefficients and decomposition limit. |
| `notes/spatial-bb-known-clique-cut.md` | `prop:clique-escape`: primary Padberg attribution, continuous-graph validity, exact base and perturbed root bounds, increasing costs and one cut per relative block. |

The historical corrections are present: the cover lower bound uses a **minimum**; exponential growth requires proportional witness parts/order headroom; arbitrary convex underestimators use an infimum; removed feasible slabs are charged; closed-slab certification is an explicit assumption; equality tolerance has the necessary small-tolerance range; integer/zero-weight moment boundaries are separate; and the degree range for the full preordering is distinguished from stronger square-only positivity. Retaining the literal `rD` proof alongside the stronger interpolation proof preserves a distinct argument rather than silently discarding it.

## Findings

None. No repair is requested.

## Independent verification

The following are independent derivations from the frozen statements. The finite checker described afterward is supplementary.

1. **Optimum, chords and cover count.** Two fractional coordinates allow an opposite feasible perturbation. Consequently each slice vertex has `k` ones and one half, giving penalty `1/4`. A convex underestimator lies below the endpoint chord even if it is not lower semicontinuous. The chord identity has error `(x-a)(b-x)`, bounded by `(b-a)^2/4`. At a containing witness, only restricted middle coordinates contribute, each less than `1/(2m)`. Thus certification at a positive target forces `|R|>2mT_*`.

   For any fixed endpoint-exclusion sets, containment implies both avoidance events. Bounding by the smaller of their marginal probabilities needs no independence. Since `|A|+|D|>=|R|`, the reciprocal uniform bound is the stated minimum of two bases raised to `q/2`. Witnesses are distinct even at `m=1`, the denominators remain positive, and `k=0`, `z=0` and `q=0` produce the claimed trivial endpoints. The union bound works for overlapping regions and arbitrary real split locations.

2. **Upper certificates and tolerance.** The low/upper/middle/high construction creates four nodes per surviving prefix: `1+4(2^n-1)=2^(n+2)-3` nodes and `2^(n+1)-1` leaves. The middle chord equals the target, while each final corner box has bound at least `(1-alpha)/2`. For the exact midpoint tree, the two stopping counts are `k+1` and `n-k`; Pascal recursion gives `binomial(n+1,k+1)` leaves and the exponent `min(k+1,n-k)`. No symmetry-in-`k` mistake remains.

   For `0<=delta<1/2`, every tolerated sum stays strictly between consecutive integers. Minimizing the vertex penalty over that interval gives `1/4-delta^2`. Exact-balance witnesses stay feasible, and the positive target is precisely `1/4-epsilon-delta^2`. At `delta>=1/2`, integer sums invalidate the unrestricted old formula; the manuscript excludes that case. The augmented-cover count is `(a+1)N`, with no claim that final boxes alone cover points removed by objective tightening.

3. **Full SDP–RLT.** With `c=t/s` and `d=t(t-1)/(s(s-1))`, the unrestricted covariance is
   `(c-d)(I-J/s)`, where `c-d=t(s-t)/(s(s-1))>=0`. Restricted covariance rows are zero, so the augmented matrix is PSD. The identity `c+(s-1)d=tc` verifies all balance rows. Distinct unrestricted pairs give `d`, `c-d`, `c-d`, and `(s-t)(s-t-1)/(s(s-1))`; repeated pairs give `c,0,0,1-c`. Every mixed restricted pair factors through a nonnegative deterministic slack, including singleton intervals. The objective is exactly `|M intersect R|p(1-p)`. The diagonal mixed RLT inequality also gives chord domination. At order one the listed preordering constraints give exactly this matrix system.

4. **Fractional moments and homogeneous positivity.** The cardinality recurrence is valid for squarefree degree at most `s-1`; the stated `2d-1` multiplier limit stays within it. The homogenizing denominator is positive under the lemma's hypotheses. The difference from each homogeneous replacement is the cardinality polynomial times a polynomial of degree at most `d-1` in the Boolean quotient. Multiplication by `P+H` requests degree at most `2d`, so replacing `P^2` by `H^2` is justified.

   For intersection size `ell`, the Gram-entry numerator factors as
   `(t)_(2d-ell)` times the falling-factorial Vandermonde sum with arguments `t-2d+ell` and `s-t`. Its value is `(t)_(2d-ell)(s-2d+ell)_ell`. Cancelling only the positive denominator `(s)_(2d)` gives the required entry; no potentially zero numerator is divided out. All incidence matrices are Gram matrices, and all displayed coefficients are nonnegative in the sufficient range. This proves positivity universally in that range without relying on numerical eigenvalues.

5. **All localizers and boundaries.** After Boolean reduction a slack product is either zero or an assignment indicator. Expanding upper slacks gives the uncancelled moment
   `(t)_(a+c)(s-t)_b/(s)_(a+b+c)`.
   If the original square polynomial is nonconstant, its degree budget forces `a+b<=2r-2`, making the indicator weight positive. Conditional moments then have parameters `s-a-b,t-a`, and satisfy all four required bounds: remaining dimension at least `2d`, both remaining cardinalities at least `2d-1`, and total degree at most `2r`. Constant squares, zero weights, repeated/conflicting factors and all-assigned coordinates are separately valid. Global dependence of the square causes no additional assumption.

   The integer restriction count retains at least `2r-1` endpoint witnesses of each kind exactly when `|R|` is below the first two entries of `q_r`. The proof checks `r=1` separately when establishing remaining dimension. The objective is strictly below the non-strict pruning target, including `R` empty. Positivity of `q_r` is distinguished from linear growth. For noninteger cardinality below the stated preordering boundary, `floor(t)+2` lower slacks have a negative moment; integer cardinality instead gives an actual distribution. The manuscript's comparison with classical square positivity is therefore sound.

6. **Product sets and the improved graph lift.** Endpoint and witness membership suffice; compactness or connectedness of the node sets is unused. Every local valid polynomial reduces to nonnegative endpoint coefficients. After grouping factors, the number of nonconstant Boolean coordinates is no larger than the sum of their original degrees, so assignment-indicator positivity respects the original budget even with repetitions. Every locally vanishing equality remains zero after an arbitrary allowed global multiplier.

   In a graph lift, each retained/auxiliary variable maps to an affine or constant polynomial. This is a degree-preserving algebra homomorphism before Boolean reduction. On every Boolean assignment it gives an actual full-graph tuple; at restricted coordinates it gives the actual witness tuple. Those facts prove every local equality, localizer, full-graph identity and available multiple. The original balance stays affine and has the same residual fractional cardinality. Full-graph objective agreement then gives identical Boolean reductions of the substituted lifted objective and the original quadratic objective, with both degrees at most `2r`. Thus the same objective estimate holds with order **r**. This does not claim that the interpolation is a continuous graph identity. Nonpolynomial functions are admissible because only their actual finite endpoint/witness values are used. Retaining originals, defining auxiliaries throughout `[0,1]`, requiring full-graph agreement and excluding coupled valid inequalities are material assumptions, all stated.

   In the distinct literal polynomial substitution proof, the balance product has degree at most `1+D(2r-1)<=2rD`, and the full-cube polynomial objective identity is legitimate. This verifies the coarser comparison separately.

7. **Relative tensor proof, asymmetry and escape.** For any allowed global localizer, each block matrix indexed by block monomials through square degree `d` is PSD. Their tensor product is PSD; its principal submatrix on tuples of total degree at most `d` is exactly the global localizing matrix. The unused tensor entries need not be globally available moments. Global equality products factor one monomial at a time. This proves positivity for squares coupling all blocks, also after local graph lifts.

   Light blocks use the fractional functional and heavy blocks true witness evaluation. Both have penalty at most `|R_b|/(2q_0)`. Subtracting `GK+G eta` from the relative target gives `sum_b |R_b|>=2q_0G tau`; independent block partitions and the union bound yield the displayed exponent. The example gives `tau=17/128` and exponent `17n/384`. The graph-lift objective argument remains valid even when its written polynomial couples blocks.

   Strict concavity forces a minimizing vertex, and ordered mass transfers uniquely minimize its linear cost over the whole balance slice. A coordinate permutation preserving the relative feasible set maps whole blocks to blocks because it preserves the normal row space. Objective equality on the slice forces translated coefficient lists. Squared-index successive differences distinguish the blocks, after which comparison of minima excludes a nonzero translation within a block. Distinctness alone would not establish this statement; the proof uses the stronger property correctly.

   The clique polynomial is multiaffine and has Boolean value `(s-k)(s-k-1)>=0`, so it is valid on the continuous graph. Balance products yield `sum_ij X_ij=K^2`; the cut bounds the trace by `k+1/4`. Adding the independently attained linear-program minimum proves perturbed root exactness, with no PSD requirement. The component certificate and known cut explicitly delimit the lower bound to its stated certificate system; the closing XOR motivation does not assert a positive multilinear spatial obstruction.

### Exact finite checks and document checks

The new independent checker is `verification/reviewer11/stage04-round01/check_exact.py`; results are in `check_exact.json`. It uses only exact rational arithmetic:

- 210 Gram-entry samples through `d=7`, including zero-coefficient endpoints;
- a full 106-by-106 squarefree global order-two moment matrix for two seven-variable fractional blocks, proved PSD by rational symmetric elimination (rank 77);
- six 15-by-15 localizing matrices, including cross-block, repeated and conflicting slacks;
- 940 global balance products after Boolean reduction;
- all 19,321 assignment indicators through degree four on those fourteen variables;
- 49 negative-product checks outside the noninteger range;
- 6,400 endpoint-exclusion patterns in four small asymmetric witness systems;
- the exact relative-example arithmetic.

Boolean reduction spans every polynomial square of the specified degree for these moment matrices, including repeated powers. These finite checks do not prove the universal theorem, arbitrary local graph-lift validity, or publication priority.

All 59 manifest hashes matched. A read-only label check found no duplicate labels or unresolved local references. The frozen build report records a successful 80-page build with no warnings, and its PDF hash matches the reviewed PDF. I visually inspected the lifted theorem on frozen PDF page 59; the definition, degree condition and substitution are readable. I did not rerun a build that would write into the frozen snapshot. Evidence and primary-source renders are confined to `verification/reviewer11/stage04-round01/`.

## Primary sources and remaining limits

Read `literature/AGENTS.md` before local originals. Source access and attribution were checked as follows:

- [Jarre's August 2018 preprint](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf): read the local full text, including Sections 2–3, and visually checked original PDF page 4. It uses binary fixing and the max-cut SDP comparison. The manuscript's contextual sentence is supported; no precise source tree count is imported.
- [Grigoriev (2001)](https://doi.org/10.1007/s00037-001-8192-0): visually checked the local author-manuscript PDF page 7, the falling-factorial functional, Lemma 1.3 and Lemma 1.4. These verify the classical provenance and the distinction from the manuscript's sufficient Gram range. I did not claim a fresh audit of the complete stronger classical positivity proof; Stage 4 does not require it.
- [Potechin (2019)](https://doi.org/10.4230/LIPIcs.ITCS.2019.61): read Theorem 1, Example 18 and the knapsack statements/proof of Theorem 44 and Corollary 45; visually checked Example 18 on original page 61:8. It gives the same moment ratio and explicitly credits Grigoriev. The full general symmetry theorem is not used or independently audited here.
- [Padberg (1989)](https://doi.org/10.1007/BF01589101): visually checked local original PDF page 11, printed page 149, Lemma 2, equation (17). Its parameter range and formula give exactly the cited cut with `alpha=k`; the manuscript independently proves the continuous extension and the optional `k=0` boundary.
- [Coniglio's anonymous review version](https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf): my fresh browser attempt returned the OpenReview verification challenge, which was not bypassed. I read the coordinator's source-access record documenting its earlier successful reading of Assumption 1, Propositions 2–4 and Appendix C. I cannot independently confirm that source's full argument or identity with the published version. The bibliography expressly identifies the review version and the version limit. This contextual citation is not a premise of any Stage 4 theorem.

No mathematical dependency needed for the Stage 4 proofs remains unverified within the frozen manuscript. The external comparison is bounded: neither my checks nor the author's source ledger establish priority, and no such priority claim is made. Stronger coupled cuts, different branch coordinates, elimination of originals, or addition/reuse of component certificates require another model; the manuscript states these limits. The explicit families remain easy to optimize, as the text acknowledges.
