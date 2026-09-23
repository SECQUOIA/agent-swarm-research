# Stage 4, round 1 — independent review 13

**Verdict: PASS.** No major or minor defect found in the assigned frozen Stage 4. The new coordinatewise graph-lift theorem and its global relative-tolerance extension are supported by complete proofs under their stated oracle assumptions. The theorem organization and inspected PDF presentation permit verification of those assumptions and proofs.

## Coverage

Reviewed snapshot: `process/snapshots/stage04-round01/`. All manuscript paths in this report refer to that snapshot unless otherwise specified.

Read in full:

- `sections/09-cardinality-spatial.tex` (printed Section 12).
- `sections/10-cardinality-preordering.tex` (Section 13).
- `sections/11-coordinate-domains-lifts.tex` (Section 14).
- `sections/12-relative-blocks-cuts.tex` (Section 15).
- `sections/01-foundations.tex`, particularly the vertex-law proof and the certificate, absolute-target, and relative-target definitions in `subsec:certificate-model`; `macros.tex`; the Stage 4 bibliography entries and input structure.

Stage 4 has no separate appendix. Its required moment, localizer, lift, tensor, and cut proofs are in these four sections. No other earlier-stage theorem is required as an unproved mathematical input to Stage 4: the fractional-cardinality optimum and the continuous multiaffine validity argument are proved here. Reading the foundations does not constitute a new primary-source audit of the unrelated accepted bilinear results.

Read the review protocol, Stage 4 review and author assignments, all Stage 4 scope rows in `process/scope-proposal.md`, and the complete author source-to-label ledger and completion record in `process/stage-04-author.md`. Read every canonical Stage 4 source:

- `results/spatial-bb-exponential-lower-bound.md`.
- `results/spatial-bb-sdp-rlt-exponential-lower-bound.md`.
- `results/spatial-bb-higher-sos-exponential-lower-bound.md`.
- `results/spatial-bb-product-domain-exponential-lower-bound.md`.
- `results/spatial-bb-relative-gap-exponential-lower-bound.md`.
- `notes/spatial-bb-known-clique-cut.md`.
- The paper-local `process/univariate-lift-refinement.md`.

The `results/` and `notes/` paths are relative to the enclosing repository. I inspected the relevant historical correction/audit notes `review-spatial-bb-lower-bound.md`, `review-spatial-bb-second.md`, `review-spatial-bb-sdp-rlt.md`, `review-spatial-bb-higher-sos.md`, `review-spatial-bb-product-domain.md`, and `review-spatial-bb-relative-gap.md`, and the bounded literature comparison `spatial-bb-strengthening-novelty.md`. Their verdicts were not premises of this review. I did not read another report from this review round, edit the manuscript, or use subagents.

I read `literature/AGENTS.md` before local literature. Primary-source checks were:

- [Jarre's August 4, 2018 preprint](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf), Sections 2–3 and the concluding scope limitation: binary variable fixing, the knapsack-to-max-cut transformation, and the stated SDP comparison. Local package `[[jarre2018-best-case-exponential-running-time]] p.2-5`. The manuscript uses this as a limited predecessor, not as an input proving its continuous cover theorem.
- Grigoriev's local author manuscript, functional construction and Lemmas 1.3–1.4, checked against a rendered original page 7: `[[grigoriev2001-complexity-of-positivstellensatz-proofs-for]] p.7`. The falling-factorial moments, normalization, cardinality recurrence, and classical square-positivity attribution agree. I did not independently audit the whole subsequent classical positivity proof; Stage 4 proves its own sufficient result.
- [Potechin's ITCS 2019 original](https://drops.dagstuhl.de/storage/00lipics/lipics-vol124-itcs2019/LIPIcs.ITCS.2019.61/LIPIcs.ITCS.2019.61.pdf), knapsack setup and Theorem 1, Example 18, and the knapsack parts of Theorem 44/Corollary 45 with the associated specialization: `[[potechin2019-sum-of-squares-lower-bounds]] p.3`, p.8, p.18. Example 18 was also checked visually against the original page. The moments are explicitly classical, and the manuscript does not claim the classical optimal square-positivity range as its own theorem.
- Padberg's local original, printed page 149/PDF page 11, Lemma 2, equation (17), checked visually: `[[padberg1989-the-boolean-quadric-polytope-some]] p.11`. With the whole coordinate set and parameter alpha=k, its inequality is exactly the manuscript cut after rearrangement and multiplication by two. No facet theorem is needed.
- Fresh access to the [Coniglio anonymous review PDF](https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf) returned an OpenReview browser-verification challenge. I did not bypass it and cannot independently certify that source's Appendix C. I read the coordinator's later successful-access record in `verification/primary-source-checks.md` and the author's access qualifications. The frozen bibliography explicitly identifies the review version and leaves identity with the published version unverified. This is a contextual-source access limit, not a missing premise in a Stage 4 proof.

## Findings

None. There are no required repair IDs.

In particular, I did not identify a reader-verification defect in the reuse of local parameters: the fractional moment parameter `t` and the later integral block parameter `t` are separately defined at the relevant section boundaries. The definitions consistently reserve `r` for half the available total degree, and the graph-lift discussion explicitly switches to lifted degree before stating its theorem.

## Independent verification

### Base objective, counting, upper certificates, and tolerance

The slice vertices have k ones, one half, and zeros elsewhere. Two interior coordinates admit an opposite feasible perturbation, whereas one interior coordinate is fixed by the balance. Concavity therefore proves the value 1/4, including k=0 and k=n−1.

The chord difference is `(x_i-a_i)(b_i-x_i)`. Convexity of any univariate underestimator bounds it above by the endpoint chord, even on degenerate intervals. The use of an infimum for a general underestimator correctly permits endpoint discontinuities. Substitution of y=1−x into both McCormick lower planes yields that same chord; the alphaBB second derivative is `2(alpha−1)`.

For a containing product region, its witness fraction is at most the smaller of the two endpoint-avoidance probabilities. Each avoidance probability is the appropriate without-replacement product and is bounded by a power of its marginal avoidance rate. Since one of |A| and |D| is at least |R|/2, taking the reciprocal produces **the minimum of the two reciprocal bases**, as in `lem:endpoint-count`. This handles overlapping covers, impossible avoidance, zero exclusion counts, and k=0 or z=0. The region restrictions do not depend on the selected contained witness.

At a witness, all zero/one coordinates and all unrestricted-coordinate chords vanish. The remaining penalty contribution is at most `|M∩R|p(1−p)`, with p=1/(2m). A positive target gives the strict restriction bound `|R|>m(1/2−2epsilon)`. All arbitrary real split locations are consequently covered.

The positive-tolerance upper tree adds four nodes for each surviving binary prefix. Summing gives `2^(n+2)−3` nodes and `2^(n+1)−1` leaves. The exact midpoint stopping counts start at `(k+1,n−k)`; Pascal's recurrence gives `binomial(n+1,k+1)`, with fixed exponent `min{k+1,n−k}`. The strict-target modification is available for positive tolerance. The quadratic error follows termwise from `(x-a)(b-x)≤(b-a)^2/4`.

A run with N processed nodes and at most a certified deletions per node supplies at most `(a+1)N` cover members. The text correctly requires a closed removed box to be certified before using it as such; the product-domain result later permits the exact removed coordinate set. For equality tolerance delta<1/2, the sum remains strictly between k and k+1, so minimizing the single fractional penalty over the allowed sum interval gives `1/4−delta^2`. The positive-target condition is precisely `epsilon+delta^2<1/4`; the manuscript does not extend that formula past an integer sum.

### SDP–RLT and the full preordering

For free coordinates, write c=t/s and d=t(t−1)/(s(s−1)). Direct subtraction gives

`X_UU−mu_U mu_U^T = [t(s−t)/(s(s−1))](I−J/s)`.

The other covariance rows and columns vanish. This proves full augmented PSD, including the deterministic restricted coordinates. The free row sum identity is `c+(s−1)d=tc`; adding restricted means gives Kc. Restricted rows give Kw_i. The four free off-diagonal slack products are `d,c−d,c−d,(s−t)(s−t−1)/(s(s−1))`; the repeated-index products are `c,0,0,1−c`. When either index is restricted, the expectation factors with a nonnegative deterministic slack. Thus diagonal cases and degenerate intervals are covered. The objective is exactly `|M∩R|p(1−p)`.

At r=1, affine-square positivity, all two-slack products, single slacks, and all balance-times-affine products give precisely the displayed SDP–RLT model. The diagonal mixed slack yields chord domination. Affine Farkas representations in original coordinates include a nonnegative constant, so their allowed products expand into granted slack terms and vanishing balance terms. This does not supply affine cuts in the quadratic lift.

For squarefree degree a≤2d−1, the moment recurrence gives `E[(sum u−t)u_S]=0` without invoking a moment with subset size beyond s. The homogeneous replacement has a strictly positive denominator; its difference from the original monomial is `(sum u−t)Q_S` with degree Q_S≤d−1 in the Boolean quotient. Multiplication by P+H requires only the proved multiplier degree 2d−1.

The incidence Gram expansion in (13.7) follows from falling-factorial Vandermonde. The calculation factors but never divides by `(t)_(2d−ell)`, so a zero numerator is harmless. Its coefficients are nonnegative under the stated two-sided sufficient range. This proves arbitrary square positivity, rather than only homogeneous monomial checks.

For assignment indicators, expansion gives the uncancelled moment `(t)_(a+|C|)(s−t)_b/(s)_(a+b+|C|)`. A nonconstant original square leaves at most 2r−2 assigned coordinates, making the indicator weight strictly positive. Conditioning is then legitimate. A constant or fully assigned square is handled without a zero-variable functional. Repetitions either collapse or conflict to zero. The remaining parameters obey `s−v≥2d` and both conditional cardinalities are at least 2d−1. This proves every granted global square localizer within its degree budget. The negative-slack-product example correctly distinguishes full-preordering feasibility from stronger classical moment-matrix positivity.

For `|R|<q_r`, integrality retains at least 2r−1 witness coordinates of each endpoint type. The separate r=1 dimension check is necessary and present. The constructed objective is strictly below the non-strict pruning target, even at R=empty. I recover

`q_r=min{k−2r+2,z−2r+2,m(1/2−2epsilon)}`.

The balanced positivity regime, linear-order exponential regime, epsilon=1/8 order cutoff, and trivial q_r≤0 statement are consistent. No zero threshold is divided by.

Strict concavity excludes every nonvertex minimizer of the perturbed problem. The exchange and mass-transfer arguments give the unique sorted optimizer and the separate linear-program minimum used by the escape cut. First moments are bounded by the granted node constraints. The eta estimate and `q_(r,eta)` follow, as does the explicit exponent n/32. Adding the conserved K preserves absolute gaps while generally changing relative gaps; the text makes this distinction explicit.

### Arbitrary local sets and the degree-free graph lift

On a restricted coordinate, actual witness membership makes every local inequality a nonnegative constant and every local equality zero. On an unrestricted coordinate, both endpoints belong to its actual set. Boolean reduction of a local polynomial is therefore its affine endpoint interpolation with nonnegative coefficients. Grouping repeated local factors produces nonnegative combinations of assignment indicators on at most the sum of their original degrees. Together with the unchanged square degree, this puts every expression within the assignment-localizer lemma. Closedness, connectedness, semialgebraicity, and a hull theorem are unnecessary.

The graph-lift substitution maps **every individual lifted variable** to an affine or constant polynomial. Consequently it preserves the total-degree bound for arbitrary globally coupled polynomials. Because original coordinates and affine balances remain present, every balance multiplier still fits degree 2r−1. For local inequalities and local equalities, endpoint values are evaluations at actual restricted graph tuples; the same assignment and Boolean-reduction argument proves all their products and allowed multipliers.

Every Boolean assignment after substitution is an actual point of the full product graph, including the fixed witness tuples. Hence any available full-graph polynomial identity vanishes after Boolean reduction, even if written with coupled variables. Full-graph objective agreement gives identical multilinear reductions of the substituted objective and the intended original quadratic objective. Both are within degree 2r. This proves objective agreement under the functional without asserting any false identity of a nonlinear function with its chord at continuous points.

Finite values on all of [0,1], exact preimages, retained originals, available objective degree, independent local restrictions, and exclusion of arbitrary coupled cuts are all explicit. The graph need not be compact, because the cover and attained optimum refer to the preserved original feasible problem. The literal polynomial substitution comparison also works: the equality-product degree is `1+D(2r−1)≤2rD`, and the full-graph polynomial objective identity extends from the cube. It is a coarser construction, not a contradictory order convention.

### Global relative certificate and escape cuts

For a global expression gP², each block localizing matrix indexed through degree d=deg P is available since `deg g_b+2d≤2r`. Tensoring those PSD matrices and selecting indices with **total** degree at most d yields exactly the required global localizing matrix. Entries discarded from the larger tensor are only auxiliary Gram entries and need not be globally defined moments. Equality products factor monomial by monomial. This validates the global oracle, including coupled squares and lifted block variables.

In a lightly restricted block the fractional functional is feasible by the endpoint count; in a heavily restricted block actual witness evaluation is feasible. Both penalty bounds are at most `|R_b|/(2q_0)`. Summation therefore gives `GK+sum_b|R_b|/(2q_0)+G eta`. Comparison with `(1−theta)C*` forces `sum_b|R_b|≥2q_0G tau`. Independent block witness selection and the coordinate product-region structure then yield the exact exponent `q_0G tau`. The example has `tau=17/128` and exponent `17n/384`.

The lifted extension does not require the **written** objective to be block separable: after the substitutions its Boolean reduction agrees with that of C on all remaining formal variables. The tensor functional respects those reductions. The stated no-loss result therefore survives the global relative oracle.

For asymmetry, a feasible-set permutation preserves the balance row space; the image of an entire block indicator must be an entire block indicator. Objective equality implies translation equivalence of the relevant coefficient lists. The first successive difference of each squared-index list distinguishes its block. No nontrivial block permutation survives, and distinct entries then exclude permutations within a fixed block. This proves the stated necessary symmetry exclusion modulo balances.

The clique polynomial is multiaffine and has Boolean values `(s−k)(s−k−1)≥0`; continuous validity follows by endpoint minimization. Combining the cut with equality products bounds the trace by k+1/4. The linear-cost minimum is attained at the same vertex, so the perturbed and shifted root bounds are exact. The k=0 direct argument is present. One cut per relative block, and separately reusable component certificates, explain why these are easy optimization problems despite their large certificates in the specified model.

### Supplemental exact checks and PDF inspection

Ran `python verification/reviewer13/stage04-round01/check_exact_tensor.py`. It uses exact rational arithmetic and symmetric elimination, explicitly checking that each zero pivot has a zero remaining row. It verified:

- A 7-by-7 full global order-one moment matrix for two blocks with `(s,t)=(3,3/2)`, exact rank 5, and 14 balance products.
- A 120-by-120 full global order-two moment matrix for two blocks with `(s,t)=(7,7/2)`, including repeated-power basis monomials, exact rank 77, and 1,360 balance products.
- Two 15-by-15 localizing matrices permitting arbitrary globally coupled affine squares: a repeated lower slack (rank 12), and a lower slack in one block times an upper slack in the other (rank 11).

Results are in `verification/reviewer13/stage04-round01/check_exact_tensor.json`. These are finite exact checks of the tensor moments and selected localizers, not a proof for all dimensions, all local polynomials, or all graph lifts. The universal conclusions above rest on the reconstructed proofs.

The frozen 80-page PDF has SHA-256 `acc8e083b7a3aa985d71e686a73d90405ea005928416a39e0bee05c338206339`. Independently matched all 20 recorded build input hashes and the PDF hash, checked 245 unique labels and no unresolved internal references, and read the frozen successful build report with no warnings. Evidence is in `frozen-consistency.json` under my verification directory. I did not recompile the snapshot or treat the author's successful build as a fresh reviewer build.

Visually inspected frozen PDF pages 47, 50, 53, 54, 56, 58–65. These include the stage transition, upper certificate, moment definition, homogenization/Gram decomposition, assignment localizer, perturbation theorem, local-domain and graph-lift statements, lift proof, tensor proof, relative theorem, symmetry argument, and clique-cut conclusion. Displayed formulas and references are readable; I found no clipping, overlap, or malformed theorem text. Natural page breaks sometimes split a proof, but its continuation remains clear. Renders and `pdf-audit.json` are confined to my assigned verification directory. An initial attempt using unavailable `fitz` failed before producing evidence; the successful renders used `pdftoppm`.

## Remaining limits

The Coniglio review appendix and published-version identity were not independently accessible to this reviewer. The full external Grigoriev and Potechin general positivity theories were not re-proved; the precise local attribution was checked, and Stage 4 supplies its own sufficient proof. No bounded search establishes priority.

The strongest achievable degree-versus-region tradeoff under other functionals, arbitrary coupled cuts, general branching coordinates, or elimination of original coordinates is outside these theorems. The report does not extrapolate from the finite exact checks or the inspected PDF pages. I found no unresolved mathematical dependency within the stated Stage 4 claims.
