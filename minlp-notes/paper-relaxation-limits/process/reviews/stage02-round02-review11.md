# Stage 2, round 2 — independent review 11

**Verdict: PASS.** No major or minor finding. The earlier missing finite two-level development is now included with complete certificates and the correct within-family threshold.

## Coverage

I read the complete frozen files in `process/snapshots/stage02-round02/`:

- `sections/02-universal-positive.tex`
- `sections/03-cubic-equal-means.tex`
- `sections/appendix-positive-couplings.tex`
- `sections/appendix-cubic-certificates.tex`
- `sections/01-foundations.tex`, `main.tex`, `macros.tex`, and `references.bib`.

I checked the Stage 2 dependencies in the foundations afresh: vertex-law envelopes and continuity, monomial Fréchet bounds, common upper attainment, nonnegative deficiencies, the independence classes, nonnegative-box transfer, and the positive bilinear comparison. I read the remainder of the foundations for consistency. The previously accepted finite-signing appendix is not a new Stage 2 dependency and was not independently replayed here.

I read the round assignment, protocol, author assignment and record, all Stage 2 scope rows, round 1 adjudication, and separate correction record. I compared the manuscript against all ten canonical Stage 2 result files: `positive-multilinear-gap`, `positive-multilinear-degree-upper-bound`, `positive-multilinear-sharp-degree-growth`, `positive-multilinear-second-order-upper`, `positive-multilinear-coefficient-removal`, `positive-cubic-gap`, `positive-cubic-analytic-family`, `positive-cubic-two-level-family`, `positive-cubic-rounding-upper-bound`, and `positive-multilinear-equal-marginals` (all under `results/`, with `.md` extensions). I also read their historical mathematical review notes, including the smaller two-level refinement, alternate rational two-level parameters, analytic slack, reciprocal correction, and coefficient-removal finite bound. I read `notes/positive-cubic-gap-investigation.md` to distinguish proved developments from numerical proposals. I did not read another current-round report or edit manuscript files.

The following coverage distinctions were checked explicitly:

| Required development | Frozen coverage and conclusion |
| --- | --- |
| Sparse dyadic family and exact hull | `thm:dyadic-exact`: counts, cutoff ties, affine upper certificate, resource mixture, bit reversal and XOR realization are complete. |
| Distinct arbitrary-partition and dense arguments | `prop:arbitrary-dyadic`, `eq:dense-count-lp`: separate integral proof and exact dense count-LP realization retained; no dense numerical value is substituted for a sparse exact hull. |
| Older upper proofs | `prop:dyadic-degree`, `eq:original-harmonic-finite`, `eq:older-leading-mixture`: dyadic tail proof, original harmonic finite bound, and distinct leading-constant mixture retained. |
| Full harmonic refinement | `lem:harmonic-curve`, `thm:harmonic-fixed-point`, `app:reciprocal-cutoff`: complete cutoff curve, scalar mixture scope, Lambert certificate, tuned denominator, fixed-cutoff constant and reciprocal correction retained. |
| Cloning and finite unit-coefficient existence | `thm:coefficient-removal`, `eq:finite-25000-probability`, `eq:finite-25000-margin`: exact envelopes in both directions, uniform sampling error, and the nonconstructive finite bound are complete. |
| Three-group cubic certificates and variants | `prop:cubic-finite`, `eq:homogeneous-25`, cubic certificate appendix: exact 18/24/192-variable values and the separate 25-variable bound retained. |
| Analytic cubic family | `lem:cubic-scalar`, `thm:cubic-analytic`: all five Bernstein identities, uniform slack, strongest reduced limiting bound and explicit m=36 specialization retained. |
| Every two-level finite development | `thm:cubic-two-level`, `tab:two-level-small`, `app:two-level-variant`: m=4,8,12 exact values, m=16 exact value, m=20 bound, iff threshold, 52-variable unit example, and alternate 33/16 family with m=50 bound retained. |
| Cubic upper laws | `prop:endpoint-orientation`, `thm:cubic-upper`: full general-degree orientation proof, cubic and quadratic cases, and limited mixture optimality retained. |
| Equal means | `thm:equal-finite`, `cor:equal-infinite`: finite formula, degree restriction, attainment, dimension limit, degree optimizer and sharp factor two retained with classical attribution. |

The general dyadic formula already determines its displayed canonical finite specializations. Floating-point dense values, exploratory cubic coefficient searches, and conjectural improved mixtures are not additional exact results. Later-stage scope additions are not Stage 2 omissions.

## Findings

None requiring correction.

The accepted round 1 coverage issue is resolved mathematically, not only in the ledger. The new table gives minorants at every count state, attainable fixed counts, exact lower and upper values, and exact ratios. Uniform subsets realize every coordinate mean. The ratios for m=4,8,12 are below two; m=16 gives 135/67; for all subsequent admissible m, the increasing bound `(243/115)(1-1/m)` is already above two at m=20. This proves exactly the stated iff assertion among positive multiples of four, without implying global minimum dimension.

The corrected arbitrary-partition proof now says the first interval contributes *at most* the geometric sum, defines `log_2^+`, and retains the zero-density convention. Both printed code blocks are present, in order, and match the executable exactly. I visually inspected frozen PDF pages 31–32; both blocks and the small-member table are complete and legible.

## Independent verification

The following are my derivations and checks, not reliance on prior PASS labels.

1. **Dyadic exactness.** The bound `S_l(r) <= sr + F_l(s)` follows by capping the first `l-s` terms and retaining the other s linear terms. Its weighted intercept is `(L-s)/2^s`. The two resource profiles have means `B_s` and `B_(s+1)`, so the stated mixture has mean one and is supported entirely at equality points. Prefix residues prove simultaneous hitting at every level; a uniform XOR shift assigns each leaf conditional failure probability `R/2^L`. This closes the geometry relaxation. I checked the resource identities and all allowed cutoff choices for L=2 through 25 in rational arithmetic, including equal-cutoff agreement. Every possible failure count and level was checked for prefix realization through L=9. The arbitrary-partition Jensen argument is independent of that realization. The dense LP's reverse construction also preserves all singleton means.

2. **Harmonic and older laws.** Splitting the harmonic integral at p gives exactly `[p+p log(h/p)]/A=p`. The zero-p convention and M=1 endpoint are valid. On the hard-term interval, inactive mass is at most `(d-1)t/M=eta*t`; all remaining probabilities have the required lower bound, yielding the full J curve. Its derivative is `J'=-F`, with F strictly decreasing and positive before one, so the fixed point and tangent mixture are valid even when eta=1 makes F(1)=0. The reciprocal mixture weights correctly equalize guarantees. Independently integrating the quadratic term gives `1/z-1+2 eta log z+eta^2(1-z) <= 1/z`. For `A=w-1/(2w)`, the residual reduces to `log(1-1/(2w^2))+1/(4Aw^2) <= 0` when w>=1. The tuned parameters are exactly `Lambda=N+log N`, `eta=1/N`; the numerator adjustment loses only `O((log N)^2/N)=o(1)`. For eta=1, the integrated cubic remainder is at most `1/(12 alpha^2)`, which supports the reciprocal expansion. I also checked the distinct tail lemma, dyadic scale count, original finite harmonic interval, and earlier inverse-guarantee weights. No finite numeric root check is being used as a universal proof.

3. **Cloning and sampling.** An arbitrary clone law yields random group averages, and conditional Bernoulli rounding maps its normalized objective expectation into the original feasible interval. Copying original variables into their clone groups proves the opposite inclusion. Distinct supports stay distinct after homogenization and cloning. The union bound covers all `2^(nm)` vertices and the separate term-gap event; independence between those events is unnecessary. Each envelope error is at most t and the hull error at most 2t. For fixed original data, `K^2>sn log(2)/2` controls the union, while `t/m^d -> 0` for d>=2. In the finite application, even replacing log(2) by one leaves a negative logarithmic failure bound, and the remaining normalized margin is exactly `3987/4550>0`.

4. **Finite cubic certificates.** I extracted and concatenated both verbatim blocks from the frozen appendix, compared them byte-for-byte with the frozen executable, and executed the extracted text. This checks 275,697 three-group count inequalities, all primal means and objectives, all ratios, and 564 two-group count inequalities. Every check passed. I independently checked why count distributions and uniform conditional subsets suffice for the original vertex envelope. The 25-variable padding loss is bounded without assuming independence from padding, and the 52-variable loss is `120*20/1000=12/5`, giving exactly the asserted ratio bound.

5. **Continuous cubic certificates.** Starting with the three-variable F and affine minorant, my script derives the boundary polynomial and unrestricted quadratic minimum, then expands every Bernstein row read from the actual frozen table. All five identities agree exactly. The least coefficient is `901/120000`; substitution gives `1610000/743033`. I checked the Hessian determinant and sign of the constrained boundary derivative by hand. Both two-level square-factor identities were independently expanded symbolically. The equality atoms have the required means, and conditional independent coordinate sampling makes the finite expected polynomial `(1-1/m)` times the scalar polynomial. This proves the actual two-level limiting ratios. The analytic three-group argument correctly claims only limiting lower certificates. The m=36 value without slack, `16985/8436`, was checked exactly.

6. **Cubic laws.** I checked all four one-low subcases, the all-high union integration, the independent lower fraction 7/16, and the separate quadratic cases. Independently of the manuscript's case formulas, my second script enumerates orientations and intersects endpoint intervals for O, and partitions the common-uniform interval at actual low thresholds and doubled high failure thresholds for B. Exact rational integration passes on 2,002 sorted quadratic/cubic tuples with denominator 20, six near-limit tuples, and 21 singleton marginal checks. The three optimality test configurations and their weighted cancellation give exactly 12/31. These finite checks supplement the complete case proof and do not establish global optimality of R_3.

7. **Equal means.** The adjacent-count law is common to all supports. Discrete convexity of `binom(K,d)` proves both its lower-envelope optimality for E_d and the upper bound on every positive polynomial's ratio. Comparison with independence supplies positive denominators. The expression increases up to `u/(1-u)` and decreases thereafter, giving the floor/ceiling optimizer; each maximizing degree is finite and its fixed-degree limit establishes convergence in dimension. My exact checks cover 17,955 finite rational candidates, including strict `q<u^d<u`, and compare the stated optimizing candidates against k=1 through 60. These checks passed and remain supplementary to the proof.

Artifacts are `verification/reviewer11/stage02-round02/check.py`, `check.log`, `couplings.py`, `couplings.log`, and the two inspected page renderings. The first script uses SymPy for exact polynomial identities; the extracted manuscript checker itself uses only Python's standard library. No floating-point solver or tolerance was used in these verification artifacts.

## Primary sources and remaining limits

I read `literature/AGENTS.md` before local source use. Directly inspecting text extracted from Luedtke–Namazifar–Linderoth's local original author PDF confirmed the vertex representation and Theorems 4–5 on p.8, the nonnegative-box argument on p.9, and Conjecture 1 on p.22. Its wording covers the positive nonnegative-box class used here. I did not independently inspect the published-version conjecture numbering; the frozen paper explicitly uses the author manuscript's numbering.

I inspected Sherali's local original PDF pp.252–253, equation (13) and Theorem 3. The entire-cube formula agrees with the manuscript, including the binomial coefficient, affine intercept and k range. The original is available at [Sherali's paper](https://math.ac.vn/uploads/files/9701245.pdf).

I opened the [Hoeffding primary PDF](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), downloaded an ephemeral copy under `/tmp`, and visually read printed p.16, Theorem 2 and equation (2.6). The independent bounded summands and squared range denominator agree with the manuscript's two-tail sum specialization. The paper also supplies its own proof. No primary source needed for these Stage 2 attribution checks was inaccessible, and no copyrighted original was copied into the paper directory.

I did not redo the entire prior Stage 1 external-source audit, formally verify the manuscript, or certify the absence of earlier positive-gap results in all literature. I inspected the frozen PDF's corrected certificate pages but did not rebuild the entire paper. The exact finite-degree constants, global R_3 optimum, a matching second-order lower bound, and stronger numerical mixture proposals remain unresolved; the frozen claims preserve those limits. No claim here converts an envelope-gap comparison into an algorithm for envelope evaluation or a spatial-certificate lower bound.
