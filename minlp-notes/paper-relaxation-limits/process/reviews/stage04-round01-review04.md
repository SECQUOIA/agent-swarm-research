# Stage 4, round 1: independent review 04

**Verdict: PASS.** No major or minor defect found in the frozen Stage 4 claims. The no-order-loss coordinatewise graph-lift theorem and its relative-block extension are valid under their stated oracle and full-graph objective assumptions.

## Coverage

Reviewed snapshot: `process/snapshots/stage04-round01/`.

- Read all of `sections/09-cardinality-spatial.tex`, `sections/10-cardinality-preordering.tex`, `sections/11-coordinate-domains-lifts.tex`, and `sections/12-relative-blocks-cuts.tex`. No separate Stage 4 appendix is introduced.
- Read all of the shared `sections/01-foundations.tex`, including its spatial certificate definitions. The Stage 4 proofs use those definitions and elementary multiaffine endpoint arguments; they do not import an earlier positive-multilinear gap bound or signed-bilinear comparison as a premise. Read the five Stage 4 bibliography entries.
- Read `process/review-protocol.md`, both Stage 4 assignments, all seven Stage 4 rows in `process/scope-proposal.md`, the complete source-to-label and completion ledger in `process/stage-04-author.md`, and `process/univariate-lift-refinement.md`.
- Read all six canonical repository sources: `results/spatial-bb-exponential-lower-bound.md`, `results/spatial-bb-sdp-rlt-exponential-lower-bound.md`, `results/spatial-bb-higher-sos-exponential-lower-bound.md`, `results/spatial-bb-product-domain-exponential-lower-bound.md`, `results/spatial-bb-relative-gap-exponential-lower-bound.md`, and `notes/spatial-bb-known-clique-cut.md` (paths relative to the repository root).
- Read the relevant historical correction passages in `notes/review-spatial-bb-lower-bound.md`, and the later `review-spatial-bb-second.md`, `review-spatial-bb-sdp-rlt.md`, `review-spatial-bb-higher-sos.md`, `review-spatial-bb-product-domain.md`, and `review-spatial-bb-relative-gap.md`. Their verdicts were not used as proof. Also read `notes/spatial-bb-strengthening-novelty.md` and the relevant primary-source log entries. No other report from this review round was read.
- Read `literature/AGENTS.md` before local literature. Primary-source coverage and the Coniglio access limit are recorded below.

## Findings

None. No repair is required by this review. The following verification notes identify the assumptions and boundary cases on which this verdict depends.

## Independent verification

### Fractional optimum, covers, upper certificates, and tolerance

The balance-slice vertex characterization is correct for every stated `0 <= k <= n-1`, including `k=0`: any two fractional coordinates admit an opposite perturbation, and the half-integer balance forces the sole fractional vertex coordinate to equal `1/2`. Concavity therefore yields optimum `1/4`.

The chord identity, domination of arbitrary convex univariate underestimators, exact stated separable McCormick formulation, and minimal-alphaBB calculation all check out. Using an infimum for possibly discontinuous-at-endpoint convex underestimators correctly avoids an attainment assumption. Diagonal mixed RLT gives the chord domination for the stronger oracle.

For a contained witness, zero and unit coordinates contribute zero to the chord, and unrestricted endpoint-containing intervals have zero chords. Thus certification at a positive target forces `|R| > 2m T_*`. Uniform-subset avoidance gives two marginal bounds without independence; the reciprocal bound is their stated minimum. Neither overlap of regions nor arbitrary real split locations changes the union bound. Zero endpoint-class sizes give base one, impossible avoidance events give zero probability, and `q=0` gives the trivial bound without division.

The positive-tolerance construction really has four children created across the two successive binary splits at each surviving prefix. Summing gives `2^(n+2)-3` nodes and `2^(n+1)-1` leaves. At zero tolerance, the stopping counts are `k+1` highs and `n-k` lows. Pascal recursion gives `binomial(n+1,k+1)` leaves and the sharper complementary exponent `min{k+1,n-k}`. These stopping rules remain valid even if they continue into nodes already certifiable for some other reason.

The quadratic chord-error bound follows termwise and bounds the difference of node optima by evaluation at a chord minimizer. The charged-cover proposition explicitly requires the discarded closed box to be certified; it does not silently assume closure preserves an open-slab certificate. Arbitrary product domains later permit charging the exact removed coordinate set. The enlarged balance slab has optimum `1/4-delta^2` precisely in the stated `0 <= delta < 1/2` range, and the witness proof applies when `epsilon+delta^2 < 1/4`. The old unrestricted tolerance and open-SDP prose have not been carried into the manuscript.

### Full SDP–RLT and affine closure

The unrestricted covariance is `t(s-t)/(s(s-1))` times `I-J/s`; all restricted covariance rows vanish. This proves the full augmented PSD condition, including deterministic and degenerate-coordinate cases. The unrestricted row identity is `c+(s-1)d=tc`. The four off-diagonal slack moments are `d`, `c-d`, `c-d`, and `(s-t)(s-t-1)/(s(s-1))`; repeated free indices give `c,0,0,1-c`. Restricted indices factor into deterministic and expected nonnegative slacks. Thus no diagonal RLT or mixed restricted/free condition is omitted.

At order one, the stated preordering is exactly this model. Affine Farkas representations require the nonnegative constant as well as box slacks and the balance multiple. Expanding allowed products yields only existing nonnegative moments and equality products within degree. This grants original-coordinate affine inequalities, not the lifted clique cut.

### Moment definition, homogenization, Gram decomposition, and localizers

The moment definition is a linear functional on the Boolean quotient; it is not claimed to be a measure or positive on all degrees. Every denominator `(s)_a` used for a subset satisfies `a <= s`. The cardinality recurrence uses multiplier degree at most `2d-1 <= s-1`, so its next moment is available.

For `|S|=a <= d`, the denominator `binomial(t-a,d-a)` is positive under `t >= 2d-1`, including `d=1,t=1`. In the quotient, the homogeneous numerator is `u_S binomial(sum u-a,d-a)`. Subtracting its value at `t` and dividing the polynomial difference by `sum u-t` produces a multiplier of degree at most `d-1`. Therefore replacing `P` by `H` uses the cardinality identity on `Q(P+H)` of degree at most `2d-1`; the proof does not require an unavailable degree `2d` multiplier.

For overlap `ell`, the Gram numerator is

`sum_j binomial(ell,j) (t)_(2d-j) (s-t)_j = (t)_(2d-ell) (s-2d+ell)_ell`.

This is falling-factorial Vandermonde. The proof factors but never divides by the potentially zero `(t)_(2d-ell)`. Dividing only by positive `(s)_(2d)` gives the claimed matrix entry. Every incidence matrix is a Gram matrix, and all coefficients are nonnegative under the sufficient two-sided range. This proves positivity beyond numerical evidence.

For disjoint assignment sets of sizes `a,b`, expansion of upper indicators gives the uncancelled moment `(t)_(a+c)(s-t)_b/(s)_(a+b+c)`. Repeated slacks reduce to the same assignment indicator, and conflicting slacks reduce to zero. If the square multiplier is nonconstant, `a+b <= 2r-2`, so the conditioning weight is strictly positive. The remaining square has degree `d` with `a+b+2d <= 2r`, giving all three hypotheses `s-a-b >= 2d`, `t-a >= 2d-1`, and `s-t-b >= 2d-1`. Constant squares, zero weights, and all-assigned cases require no division or zero-variable fractional functional. This covers arbitrary globally coupled squares.

The negative-indicator obstruction below the noninteger two-sided range is correct: `floor(t)+2` lower slacks produce exactly one negative numerator factor. Integer cardinalities are correctly separated. The manuscript does not claim that its sufficient moment-matrix range is the sharp classical one.

For the cover transfer, the integer restriction count below `k-2r+2` and `z-2r+2` retains `2r-1` coordinates of each endpoint class. The special `r=1` dimension argument is needed and supplied. The objective is strictly below the non-strict pruning target, including `R` empty. This establishes exactly the stated `q_r`, its zero-threshold convention, and the balanced order regimes. The perturbation bound follows from first moments in `[0,1]`; strict concavity and the exchange argument prove the unique optimizer. The extra linear-cost LP argument is sufficient for the later clique-cut conclusion. Adding conserved flow preserves absolute gaps but does not imply a fixed relative gap on a growing single block.

### Arbitrary product domains and coordinatewise graph lifts

For each unrestricted coordinate, both actual endpoints belong to the local set. Every local nonnegative polynomial therefore reduces to a nonnegative combination of its two endpoint indicators. After grouping repeated factors, each participating nonconstant coordinate consumes at least one original factor degree. The assignment-indicator lemma consequently applies with every permitted global square. A local equality reduces to zero and remains zero after every allowed global multiplier. This uses no compactness or hull assertion about arbitrary coordinate sets.

The graph-lift map sends every lifted variable to an affine polynomial in one Boolean coordinate, or to its actual deterministic witness value. It is an algebra homomorphism that cannot raise degree. Retained original coordinates keep the balance affine. Local graph inequalities have nonnegative values at the selected true graph tuples; local equalities vanish there. Thus exactly the same degree budget proves all lifted localizers and equality products. Full-product-graph identities, even coupled ones, also vanish on all substituted Boolean tuples.

Full-graph objective agreement is substantive: those tuples need not satisfy the balance. Agreement only on the feasible slice would not justify this proof. Under the actual assumption, uniqueness of multilinear reduction gives objective agreement through degree `2r`. Finite definition of every auxiliary on all of `[0,1]` preserves every witness and the original optimizer, even for discontinuous maps. Covers are correctly defined by preimages; no false compactness claim about the lifted graph is made. The proof constructs moments rather than asserting a continuous chord identity for an auxiliary function.

The literal polynomial substitution comparison correctly yields the weaker order `rD`: a balance times a lifted multiplier pulls back to degree at most `1+D(2r-1) <= 2rD`. The no-loss theorem does not assert invariance under arbitrary nonlinear reformulations, joint-coordinate auxiliaries, or coupled valid cuts.

### Global tensor, relative threshold, symmetry, and escape certificates

The block localizing matrix with indices through degree `d=deg P` is available because `deg g_b+2d <= 2r` in each block. Its tensor product is PSD. Restricting to index tuples of total degree at most `d` gives precisely the required global localizing matrix. The unused tensor entries need not be global moments; this causes no domain-of-definition gap. Equality products factor one global monomial at a time. This proof covers squares coupling every block and lifted variable.

Lightly restricted blocks use fractional moments, while heavily restricted blocks use the contained true witness. Both have penalty at most `|R_b|/(2q_0)`. The resulting objective upper bound rearranges against `(1-theta)C*` to give `sum_b |R_b| >= 2q_0 G tau`. Independent block witnesses and the endpoint count then give exactly `(3/2)^(q_0 G tau)`. The numerical example has `tau=17/128` and exponent `17n/384`. The `tau<=0` and fixed-order scope are explicit.

For the lifted extension, Boolean reduction after all block substitutions also handles a written objective coupling blocks, provided it agrees on the full graph. The factor functionals annihilate the remaining Boolean identities. There is no hidden written-separability requirement.

The affine-hull row-space argument forces any feasible-set-preserving permutation to map whole blocks to blocks. Sorted successive differences of the squared-index coefficients distinguish the blocks up to translation, and a finite distinct coefficient set cannot equal a nonzero translate of itself. This proves the claimed stronger symmetry exclusion modulo balances.

The clique polynomial is multiaffine and has Boolean value `(s-k)(s-k-1) >= 0`, proving continuous validity. Summed equality products and the cut give `trace X <= k+1/4`; the independent linear-cost LP bound gives exact perturbed root values. One cut per relative block suffices. The manuscript states both this escape and the short component-certificate escape, so the lower bound is not presented as inherent optimization hardness. Its final XOR motivation remains distinct from the earlier positive-multilinear gap family.

### Primary sources and computational evidence

- [Grigoriev's author manuscript](https://logic.pdmi.ras.ru/~grigorev/pub/square_knapsack_journal.pdf): directly inspected the local original PDF page 7, its falling-factorial functional, and Lemmas 1.3–1.4. The normalized Boolean-reduced moments and cardinality identity match. Local locator: `[[grigoriev2001-complexity-of-positivstellensatz-proofs-for]] p.7`. I did not audit the entire subsequent spectral positivity proof; Stage 4 supplies its own sufficient proof.
- [Potechin, ITCS 2019](https://drops.dagstuhl.de/storage/00lipics/lipics-vol124-itcs2019/LIPIcs.ITCS.2019.61/LIPIcs.ITCS.2019.61.pdf): read Theorem 1 and the knapsack parts of Example 18, Theorem 44, and Corollary 45; visually checked Example 18 on original PDF page 8. The moment ratio and attribution to Grigoriev are correct. Local locators: `[[potechin2019-sum-of-squares-lower-bounds]] p.3`, `p.8`, `p.18`. The full general symmetry machinery is not an imported premise.
- [Jarre's 2018 preprint](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf): read the six-page local text and accessed the primary PDF. Sections 2–3 support the narrowly worded binary-fixing/knapsack/max-cut-SDP predecessor comparison. Local locators: `[[jarre2018-best-case-exponential-running-time]] p.2-p.5`. No exact predecessor tree count is imported into Stage 4.
- Padberg: directly inspected local original PDF page 11, printed page 149, Lemma 2, equation (17). Taking the whole set and `alpha=k`, then changing sides and multiplying by two, gives the manuscript cut exactly. The formula is missing from extracted text, making original inspection necessary. Local locator: `[[padberg1989-the-boolean-quadric-polytope-some]] p.11`; [published source](https://doi.org/10.1007/BF01589101).
- [Coniglio review-version endpoint](https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf): this review's fresh browser access returned a verification challenge. I did not bypass it and cannot claim an independent full read. The coordinator's earlier successful extracted-text read is documented in `verification/primary-source-checks.md`; the manuscript and bibliography identify that exact review version and disclose unverified identity with publication. This is a contextual source-access limit, not an unproved mathematical premise of a Stage 4 theorem.

The independently written `verification/reviewer04/stage04-round01/check_exact.py` passed using exact arithmetic:

- 44 symbolic Gram-entry identities through `d=8`;
- 32,335 homogenization-times-monomial equalities in five integer and fractional boundary configurations through `d=3`;
- 71,591 direct assignment-indicator expansion identities, including zero weights and all-assigned cases;
- 2,974 allowed nonnegative indicator weights, checking strict positivity where nonconstant squares are allowed;
- 9,918 rational endpoint-avoidance bounds and the exact relative-example arithmetic.

Results are in `verification/reviewer04/stage04-round01/check_exact.json`. These finite checks support the formulas; the preceding algebraic review supports the universal claims.

I also read the frozen `verification/check_stage04_author.py` and replayed its functions with bytecode writing disabled and output redirected exclusively to my assigned directory. The replay reproduced 27 Gram identities, 48 boundary cases, nine lifted tensor cases, 774 equality checks, 360 localizer checks, and 1,792 clique/unique-optimizer vertex checks. Evidence: `verification/reviewer04/stage04-round01/frozen-author-replay.json`. This is reproduction of author evidence, separate from my independent checker. Source-page renders are also confined to the assigned verification directory. No manuscript, snapshot, or literature file was edited.

## Remaining limits

The Coniglio access limit above remains. No exhaustive priority search or audit of every theorem in the contextual sources is claimed. This review does not establish an optimal order-versus-region tradeoff for other functionals or stronger coupled oracles. Finite calculations do not establish universal positivity, and I did not independently rerun the cumulative LaTeX build. None of these limits invalidates the precisely scoped, self-contained Stage 4 proofs.
