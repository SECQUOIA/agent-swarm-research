# Stage 2, round 1, reviewer 05

**Verdict: PASS.** I found no major or minor defect in the assigned Stage 2 results. In particular, the exact dyadic hull formula is attained by an actual law on the original variables, and the coefficient-removal argument controls all clone vertices simultaneously. The finite cubic certificates establish the stated exact values without a numerical solver.

## Coverage

The manuscript reviewed was the frozen input under `process/snapshots/stage02-round01/`:

- `sections/02-universal-positive.tex` in full;
- `sections/03-cubic-equal-means.tex` in full;
- `sections/appendix-positive-couplings.tex` in full;
- `sections/appendix-cubic-certificates.tex` in full, including its printed checker;
- `main.tex`, `macros.tex`, `references.bib`, and `sections/01-foundations.tex`, with fresh verification of the vertex-law, common-upper, deficiency, easy-term independence, continuity, and nonnegative-box-transfer dependencies.

I read the review protocol, Stage 2 review and author assignments, author ledger, and every Stage 2 scope row. I read all ten canonical Stage 2 result notes: `positive-multilinear-gap`, `positive-multilinear-degree-upper-bound`, `positive-multilinear-sharp-degree-growth`, `positive-multilinear-second-order-upper`, `positive-multilinear-coefficient-removal`, `positive-cubic-gap`, `positive-cubic-analytic-family`, `positive-cubic-two-level-family`, `positive-cubic-rounding-upper-bound`, and `positive-multilinear-equal-marginals`, all under repository `results/`. I inspected the relevant prior correction records, particularly the exact nested-partition attainment, analytic Bernstein slack improvement, two-level rational variant and 32/52-variable additions, coefficient sampling quantifiers, and tuned harmonic cutoff. Old audit verdicts were not treated as proof. No other current-round report was read, no subagent was used, and no manuscript file was edited.

The Stage 1 finite-signing appendix is accepted background and has no new dependency in these positive results; I did not independently replay it. Later-stage spatial and structural results are outside this review.

After reading `literature/AGENTS.md`, I checked these primary sources:

- Luedtke–Namazifar–Linderoth: local original PDF and extracted text; Conjecture 1 on author-manuscript p.22 was independently rendered and visually inspected. Its positive-coefficient and nonnegative-box scope matches the dyadic counterexample. I also inspected the local text of the common-upper results and positive bilinear theorem used as background.
- Sherali (1997): local original PDF, direct `pdftotext -layout` extraction of printed pp.252–255, and a visual check of equation (13) on p.252. The displayed whole-cube elementary-symmetric formula and Theorem 3 agree with the manuscript. The local primary text identifies the complete degree-d polynomial and the restriction 2 <= d <= n.
- Hoeffding (1963): inspected the available primary-PDF page image at `/tmp/stage02-hoeffding-p5.png`, printed p.16, Theorem 2 and equation (2.6). Its independent bounded-variable assumption and exponent yield the manuscript's two-tail specialization. The manuscript separately proves the needed concentration inequality.

No required primary statement was inaccessible. These checks establish attribution of the stated tools and conjecture, not absence of prior positive-gap counterexamples throughout the literature.

## Findings

None requiring repair. The following are affirmative proof checks, not inferred findings from passing scripts.

## Independent verification

### Dyadic construction, attainment, and counts

At level j, there are 2^j distinct supports, each consisting of its own level anchor and a block of 2^(L-j) leaves. Thus the support count is 2^(L+1)-2, degree is 2^(L-1)+1, and occurrence count is L*2^L+2^(L+1)-2. The minimum mean of each term is 2^(-j), and its Frechet lower value is zero because its leaf-failure sum is exactly the anchor mean. Common-threshold rounding therefore gives both T and the full concave envelope equal to L.

The count surrogate is an upper relaxation for arbitrary level partitions: disjointness within a level gives N_j <= min(2^j,R). For any fixed law of R, selecting upper tails maximizes each anchor contribution, and the common quantile construction makes all those selections feasible simultaneously. This step imposes no false independence constraint on the anchors.

For every l and nonnegative r, capping the first l-s terms and retaining the last s linear terms proves the affine bound S_l(r) <= sr+F_l(s). Its integrated intercept is (L-s)/2^s. For q=s,s+1, direct summation gives E R^(q)=(L-q+2)/2^q. The displayed convex mixture has mean failure count exactly one, and both component profiles lie at equality points of the same affine bound. In particular, the l=s case uses r=0 or 2; the capped terms do not introduce an unaccounted error at that boundary. At a shared cutoff the difference of the two candidate hull formulas is zero because B_(s+1)=1.

To lift the count construction, the first j bits of a reversed L-bit label are the reversals of the residue modulo 2^j. Consequently the first R reversed labels hit exactly min(2^j,R) level-j blocks simultaneously. An XOR shift permutes each level partition, preserving those counts. For any fixed leaf, exactly R of the 2^L shifts move it into a failure set of size R. Thus conditional failure probability is R/2^L and unconditional failure probability is 1/2^L, as required. This verifies exact attainment in the original polynomial, not merely in its surrogate.

The arbitrary-partition logarithmic argument is independently valid: its Jensen step uses the measure r(t)dt/M_0 and integrates 1/t only on the positive-r support, bounded by (L-1)log 2. The zero-mass case is handled. The dense predecessor's count LP has both realization directions, since a uniform failed subset and conditional anchor probabilities z_jr/p_r realize any feasible LP point. It is not incorrectly identified with the sparse hull formula. Padding preserves the exact face values and distinct supports; moving all means into the interior uses continuity only, and the increased occurrence count is acknowledged.

### Global upper laws and asymptotics

The dyadic scale laws, threshold law, harmonic law, endpoint law O, and cubic law B all preserve the entire marginal vector. In particular, integrating the harmonic kernel gives p[1+log(h_p/p)]/A_p=p, including a saturated cutoff h_p=1. The p=0 convention removes the logarithmic singularity. Low coordinates and the 1/2 classification are consistent across the relevant case splits.

The dyadic tail lemma follows from continuity of the cumulative integral and monotonicity of N(s), and selecting a power of two loses at most a factor two. There are exactly K scale laws, so the mixture denominator K+1 is correct.

For the harmonic full curve, inactivity during the integration interval entails p_j<t/M; hence at most eta*t of the failure mass is omitted. The anchor succeeds throughout that interval. The resulting integral lower bound holds also at z=1 by nonnegativity. Strict decrease of J(z)-z proves existence and uniqueness of the crossing; the convex tangent gives the stated scalar-optimal mixture, with the appropriate limited optimality claim. The final inverse-guarantee mixture with independence gives 1/zeta+2/c_0.

The Lambert calculation retains valid signs in the quadratic integral. For A=w-1/(2w), w>=1 gives A>=1/2 and a positive denominator; the displayed logarithmic comparison proves J(A/Lambda)>=A/Lambda. The tuned cutoff Lambda=N+log N, eta=1/N changes the upper denominator to log N-log log N+o(1). The fixed eta=1 appendix correctly retains the constant -1 and the reciprocal correction: its cubic Taylor remainder is at most 1/(12 alpha^2), and the omitted endpoint terms are o(alpha^(-2)). Neither argument establishes a second-order lower bound on the true supremum. The original finite constant and the distinct older leading-constant mixture are also proved with valid nonempty integration intervals and weights.

The largest admissible dyadic degree and dimension differ from an arbitrary allowance by bounded factors, sufficient to preserve the logarithmic leading constant. Unused-coordinate padding preserves the full gaps. The global-law quantifiers support simultaneous Frechet interpolation without an envelope-evaluation algorithm claim. Positive expansion transfers every degree upper bound in the required direction T_original <= T_expanded, with H unchanged.

### Clones and finite unit supports

Distinct original supports cannot collide under homogenization because padding coordinates are new. After cloning, each degree-d support supplies m^d distinct supports using one clone from each of d different original groups; supports from different original groups remain distinguishable. Homogeneity is what makes the common scaling m^d valid.

An arbitrary clone law induces random group averages q. Conditional independent rounding of the original coordinates preserves f(q) by multiaffinity and preserves all original means. Conversely, copying each original Bernoulli coordinate to its entire group embeds every original law. These two maps prove equality of the complete feasible expectation intervals and both envelopes. Clone independence is never assumed.

The concentration union covers all 2^(nm) vertices plus the separate termwise-gap event. Reusing the same retention indicators across events does not invalidate a union bound. With fixed original n,s,d and K^2>sn log(2)/2, the failure probability tends to zero and t/m^d tends to zero for d>=2. Uniform vertex error implies each envelope error is at most t; the hull-gap error is at most 2t. Positive limiting hull gap then justifies ratio convergence.

For the 25,000-variable application, the allowance loses 5t in T-2H, leaving exactly 3987/4550 times m^3 as a positive margin. The coarse upper bound on the logarithm of the failure probability is already negative using log 2<1. The text correctly asserts finite existence without claiming to list a sample. Separately, the explicit 52-variable polynomial has 1920 supports of type UWW and 2400 of type UUz, all distinct and squarefree. The loss bound 120 times 20/1000=12/5 holds for arbitrary dependence on padding variables, giving the stated 2700/1343 ratio bound.

### Cubic primal/dual and analytic certificates

The three-group count reduction is exact because all vertex values depend only on group counts and a conditional uniform-subset law realizes every individual mean from a count law. I independently enumerated all 343+729+274625=275697 integer dual inequalities, checked every primal probability and mean, and recovered all listed exact ratios. The lower envelopes are respectively 2750/13, 3572/7, and 34172072/105. All supplied primal states are tight; no solver tolerance is involved. The 25-variable homogeneous bound follows from the pointwise quadratic loss bounded by 1840, and retains its exact upper and termwise values. The 289-state two-level certificate and the fixed-count attaining law establish the exact 32-variable ratio 135/67.

For the continuous three-group minorant, the positive-definite Hessian and boundary gradient sign establish the constrained minimum on c<=3/10. Unrestricted quadratic minimization on the remaining c interval gives a valid lower bound even if its minimizer leaves the square. I independently expanded all five Bernstein rows and recovered the common slack 901/120000. The finite-count correction is bounded by 72/m, and support counting gives the displayed upper and termwise formulas. The resulting limiting certificate reduces to 1610000/743033. The manuscript correctly avoids claiming actual ratio convergence or finite attainment for this analytic lower endpoint.

Both two-level polynomial identities expand exactly. Their equality atoms have the stated means and affine values. The finite count correction gives one envelope bound; conditional Bernoulli sampling from the equality atoms gives the other, without requiring the atom coordinates to be integer-grid counts. This proves actual ratio convergence to 243/115 and, for the alternate parameter choice, 33/16. The finite m=20 and m=50 bounds agree with their formulas.

The endpoint-orientation deficiency is exactly the expected largest selected nested exclusion, giving weights 2^(-j). The sorted-sum inequality and decreasing average justify the full degree constant. For the cubic 31/12 mixture I checked all low/high classes, all four one-low subcases, and the quadratic cases. The all-high independent estimate uses t>0 before division. The three exact/limiting obstruction configurations and their convex weights 3/31,4/31,24/31 cancel the mixture variables, proving optimality only among the specified fixed-mixture termwise guarantees.

### Equal means

The adjacent-count law gives all degree-d expectations q_(n,d) simultaneously. Discrete convexity of binomial(K,d) makes it minimizing for E_d; comparison with independent rounding gives q_(n,d)<=u^d<u, so all ratios are defined. This proves the finite maximum and its attainment. Fixed-degree limits, together with a finite maximizing degree, establish both the dimension-free supremum and the limit in n. Below u/(1-u), the relevant expression increases because it is the reciprocal of an average of a decreasing sequence; above that threshold it decreases. The floor/ceiling optimizer and Bernoulli factor-two inequality therefore follow. The unit-cube scope and classical attribution are explicit.

### Reproducible check artifact

`verification/reviewer05/stage02-round01/check.py` is an independent exact checker; `results.json` in the same directory records its successful output. It checks dyadic affine bounds for every integer failure count and all level indices for L=2,...,12, every reversed-prefix count in those sizes, XOR singleton counts exhaustively through L=6, the three finite cubic primal/dual certificates, the 289 two-level inequalities, explicit 52-variable support uniqueness, finite sampling margins, five Bernstein identities, and both two-level identities. It uses exact integers, rational numbers, and symbolic polynomial expansion. These finite checks supplement the universal arguments above and do not establish a universal theorem by sampling.

## Remaining limits

The exact finite-degree constants, global optimality of the cubic mixture bound, and a matching second-order lower asymptotic remain open as stated. Cloning does not preserve dimension or provide a small deterministic support. I did not generate the nonconstructive sampled polynomial, independently rebuild the PDF, or visually inspect every manuscript page. Primary-source checks were targeted to the Stage 2 dependencies; this review is not an exhaustive literature-priority search or a new audit of unrelated Stage 1 external inputs.
