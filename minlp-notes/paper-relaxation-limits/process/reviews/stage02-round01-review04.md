# Stage 2, round 1, independent review 04

**Verdict: PASS.** I found no major or minor defect in the assigned frozen Stage 2 mathematics. The probability constructions preserve every coordinate mean in a single joint law. The exact finite certificates, limiting lower bounds, and universal upper guarantees have the stated scopes.

## Coverage

I read these frozen files under `process/snapshots/stage02-round01/` in full:

- `sections/02-universal-positive.tex`;
- `sections/03-cubic-equal-means.tex`;
- `sections/appendix-positive-couplings.tex`;
- `sections/appendix-cubic-certificates.tex`;
- `sections/01-foundations.tex`;
- `main.tex`, `macros.tex`, and `references.bib`.

I also read `process/review-protocol.md`, `process/stage-02-review-assignment.md`, `process/stage-02-author-assignment.md`, the author record and its entire coverage ledger, all Stage 2 scope rows, and the surrounding dependency and scope requirements in `process/scope-proposal.md`.

I read all ten canonical Stage 2 result files, rather than relying on the author ledger: `positive-multilinear-gap.md`, `positive-multilinear-degree-upper-bound.md`, `positive-multilinear-sharp-degree-growth.md`, `positive-multilinear-second-order-upper.md`, `positive-multilinear-coefficient-removal.md`, `positive-cubic-gap.md`, `positive-cubic-analytic-family.md`, `positive-cubic-two-level-family.md`, `positive-cubic-rounding-upper-bound.md`, and `positive-multilinear-equal-marginals.md` under `../results/`. Relevant older audit records were inspected for the sparse/dense correction, positive-box inequality, harmonic normalization and tuned cutoff, coefficient removal, all finite cubic witnesses, the positive Bernstein slack, both two-level parameterizations, the three-law mixture, and the classical equal-mean attribution. No current-round report was read.

The Stage 1 signing appendix was treated as previously accepted background. No Stage 2 argument requires its finite enumeration or the signed Schur-multiplier argument. I read the shared foundations, but did not reopen every primary source for those unrelated accepted results. Later stages and the planned final introduction/abstract integration were not treated as missing Stage 2 obligations.

I read `../literature/AGENTS.md` before using primary sources. Direct source checks were:

- Luedtke–Namazifar–Linderoth: local extracted text and original PDF p.22, including a rendered visual check of Conjecture 1. It concerns positive coefficients on nonnegative boxes and the term-by-term versus scalar hull gap, exactly the class contradicted here. I also inspected their common-upper statements and positive-expansion proof on pp.8–9. The manuscript correctly specifies the author-manuscript numbering. [Original author manuscript](https://jlinderoth.github.io/papers/Luedtke-Namazifar-Linderoth-12-TR.pdf).
- Sherali: original PDF pp.252–255, equation (13), Theorem 3 and its proof; visually checked equation (13) on p.252. The slope and intercept in `eq:sherali-symmetric` match the original after replacing its degree parameter by `d`. [Original paper](https://math.ac.vn/uploads/files/9701245.pdf).
- Hoeffding: directly retrieved the open original PDF and visually read printed p.16, Theorem 2 and equation (2.6). Applying the one-tail average bound to the sum, and then to its negative, gives the stated two-tail inequality with independent bounded summands. The manuscript also proves the required specialization. [Original paper](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).

No original needed for these three Stage 2 checks was inaccessible. Original source files and rendered source pages were kept outside the paper directory; no copyrighted original was copied into the deliverable.

## Findings

No findings requiring repair. In particular, the following distinctions in the frozen text are mathematically necessary and correctly maintained: exact sparse attainment requires nested partitions; dense count LP values belong to the dense model; original positive-box term gaps are bounded by expanded gaps; the analytic cubic endpoint is a supremum lower bound; the two-level family, unlike that analytic certificate, has a proved limit of its actual ratios; and mixture optimality is confined to the stated guarantee families.

## Independent verification

### 1. Foundations and full marginal preservation

The vertex representation follows by independently rounding a continuous point to endpoints, conditional on that point. This preserves every multiaffine value as well as its mean. Consequently the lower and upper envelopes optimize over the same complete mean-constrained law polytope. For positive coefficients, the single common-threshold law simultaneously attains every upper monomial envelope. Therefore

`H = max_P sum_e a_e E_P[X_anchor - product_e X]`

has the correct maximization direction. Each summand is a nonnegative indicator at every binary outcome. It is consequently valid to retain only the useful mixture component for a term without paying for contributions from other components.

The box transfer preserves the full hull gap by an affine bijection. For an original factor split by positive expansion, its lower envelope is at least the sum of expanded lower envelopes and its upper envelope is at most the sum of expanded upper envelopes. Thus `T_original <= T_expanded`. The proof never requires an equality of these term gaps or preservation of incidence structure.

### 2. Dyadic lower construction and alternate reductions

I verified the exact monomial and incidence counts, zero termwise lower values, and `cav f_L = T = L`. Upper-tail selection is simultaneously feasible for all anchors in the count surrogate: the anchor constraints impose only their singleton masses. The affine bound

`S_l(r) <= s r + F_l(s)`

comes from capping the first `l-s` terms and using slope `s` for the rest. Its integrated intercept is exactly `(L-s)2^(-s)`. The two resource profiles have means `B_s` and `B_(s+1)`; their stated convex mixture has mean one, valid weights, and integer counts no larger than `m`. Each profile lies on the same affine equality segment, including `l=s` with counts zero and two. At a cutoff tie, the difference between the adjacent formulas is `1-B_(s+1)=0`.

Bit reversal makes the first `R` failed labels occupy exactly `min(2^j,R)` level-j prefixes. A uniform XOR mask is a permutation of every partition and puts each fixed leaf in a size-R failure set under exactly R masks. This proves the individual conditional failure probability `R/m`; averaging gives the prescribed `1/m`. Thus the surrogate is attained by an original-coordinate law, not merely a count relaxation.

The arbitrary-partition estimate separately uses the geometric-sum bound and Jensen under `r(t)dt/M_0`. Removing zero-density points is legitimate, and the `M_0=0` case is explicit. The dense LP has both realization directions: uniform fixed-size failed subsets preserve each leaf mean, and conditional Bernoulli anchors realize every `z_jr/p_r`. The union bound for a random size-k subset gives the required comparison to the sparse surrogate. Homogeneous padding is exact at the face; continuity gives interior approximation. Its larger occurrence count is correctly stated.

The dyadic cutoff implies `s = log_2 L + O(1)`. Largest-admissible examples and unused coordinates transfer both lower asymptotics to all growing integer degrees and dimensions. No dimension is held fixed during this interpolation.

### 3. Dyadic and harmonic upper distributions

At dyadic scale B, `h=min(Bp,1)` satisfies `h>=p`, and conditional failure `p/h` over an interval of length h integrates to p. These are coordinatewise rules assigned once globally. The tail lemma is valid in both branches: if `S<=u`, monotonicity gives `sN(s)<=S`; if `S>u`, a continuous cumulative integral reaches u and supplies a prefix where the integrand equals N. There are exactly `1+floor(log_2(d-1))` allowed powers. The scale selected in the pointwise proof is used only to lower-bound the sum of those pre-existing global laws.

For harmonic rounding, `p<=h_p<=1` and `1<=A_p<=Lambda` imply valid probabilities. Splitting at p gives the exact normalization `integral q_p=p`, including saturated supports. The p=0 convention avoids undefined logarithms. Low coordinates are threshold indicators throughout, and ties at one-half are consistently low.

For a one-low term, the integration interval `[p_max,t_e]` lies inside the anchor-success interval. Inactivity means `p_j<t/M`, so at most `r t/M<=eta t` total failure mass is discarded. Active conditional probabilities sum to at least `(t_e-eta t)/(Lambda t)`. Conditional independence supplies the exponential union bound. These statements depend on the term only in the analysis; the law itself does not depend on its supports or anchor.

The scalar F decreases continuously from one, is positive in the open interval, and may equal zero at the right endpoint when eta=1. Thus `J(z)-z` has one root. The tangent mixture weights are positive and give `J(z)+az >= (1+a)zeta`. At the crossing every fixed combination of the two scalar curves equals zeta, proving exactly the stated scalar optimality. The final independence mixture has weights proportional to inverse guarantees and gives `1/(1/zeta+2/c_0)` for every term. All boundary and zero-gap cases avoid division by zero.

I separately checked the original finite constant 24, its integration interval and factors of two, and the older leading-constant mixture. For the latter, `b>=6` makes `b-3 log b>0`; the lower exponent is at most `1/b^2` on the selected interval even when the actual sum of conditional probabilities is larger. Integrating that lower exponent and assigning the stated inverse-guarantee weights gives the claimed leading constant.

### 4. Finite cutoff and asymptotic certificates

Direct integration gives

`integral_z^1 (1/v-eta)^2 dv = 1/z-1+2 eta log z+eta^2(1-z) <= 1/z`.

For `A=w-1/(2w)`, `w>=1` ensures `A>=1/2` and a positive final denominator. The difference

`A+log A+1/(2A)-(w+log w) = log(1-1/(2w^2))+1/(4Aw^2)`

is nonpositive, proving the Lambert certificate by the sign of `J(A/Lambda)-A/Lambda`. With `M=(d-1)N`, the defining logarithmic equation yields `w=log N-log log N+o(1)` and multiplication by `N/Lambda` changes this denominator by o(1).

For eta=1, the elementary finite cutoff is valid at `log Lambda=4` and thereafter. The linear/quadratic sandwich gives `alpha~log Lambda`. The integrated cubic remainder is at most `1/(12 alpha^2)`, while the endpoint/log terms are `O(log Lambda/Lambda)`. The mean value theorem then gives the reciprocal correction `alpha=w-1/(2w)+O(w^-2)`. None of these steps implies a second-order lower theorem for the actual supremum.

### 5. Cloning and uniform coefficient sampling

The clone proof establishes both directions of feasible expectation transfer. An arbitrary clone law produces random group averages q with `E q=x`; conditional independent rounding to original coordinates has expected objective f(q). Conversely an original law embeds by setting all clones in its group equal. This proves equality of entire expectation intervals, hence both envelope identities. It does not assume clone independence. Distinct original supports remain distinct after homogenization and cloning, and homogeneity gives exactly `s m^d` candidates.

The sampling variables are independent retention indicators. At every binary clone vertex their coefficient weights lie in `[0,1]`; the same is true of their fixed term-gap weights. The events need not be independent. The union bound covers all `2^(nm)` vertices plus the term-gap event. With `t=K m^((d+1)/2)`, its exponent is `m(n log 2-2K^2/s)+O(1)`, negative under the stated strict condition. Uniform vertex error controls each envelope by t through feasible expectations and the hull gap by 2t. Keeping the original instance fixed makes `t/m^d -> 0` for every d>=2.

The 25,000-variable numerical existence argument uses the correct five-error allowance in `T-2H`. Its remaining normalized margin is exactly `3987/4550>0`, and the logarithm of its failure bound is negative even with `log 2<1`. A successful sample is nonempty, and a nonempty positive nonlinear polynomial at an interior point has positive hull gap by comparison of independent and common-threshold expectations. No sampled support is claimed to have been constructed.

### 6. Cubic and equal-mean results

For endpoint orientation, the opposite-orientation exclusions are nested. The first selected sorted exclusion has probability `2^(-j)`, including ties, so the geometric expected maximum and the decreasing degree guarantee are valid.

For the cubic mixture, I checked all four one-low subcases, all-high terms, at least-two-low terms, and all three quadratic cases. In the all-high case the actual B union probability is `c+a/2+b/4`, so subtracting anchor failure leaves `a/2+b/4`. The independence inequality `u(a+b-ab)>=7t/16` follows from `ab<=(a+b)^2/4` and the two correct branches of `t=min(u,a+b)`. The three test configurations remain in their stated classes when limits are taken, and their weighted upper bounds cancel with weights `3/31,4/31,24/31`. This establishes only fixed-mixture termwise optimality.

The analytic scalar argument uses a positive-definite Hessian of determinant 248. On `c<=3/10`, the negative boundary derivative is the correct sign for a minimizer at a=1. On the other range, unrestricted quadratic elimination is a valid lower bound even if its stationary point is infeasible. All five exact Bernstein rows represent the eliminated quartics and have minimum coefficient `901/120000`. The count expansion, upper values and termwise lower values give the finite lower ratio with positive denominator. Its limiting certificate reduces to `1610000/743033`; the manuscript does not assert that this is the limit of the actual ratios.

For each finite three-group witness, the affine inequality covers every binary vertex because the objective depends only on counts. Conditional uniform subsets lift the attaining count law to every individual mean. Exact checks reproduce all three primal values and ratios. The 25-variable loss uses `Q<=1840` and only `E(1-Z)=1/1000`, so arbitrary padding dependence is allowed.

For both two-level parameter choices, the displayed sum-of-squares identity is exact and nonnegative on the full square. Their equality-atom laws give the prescribed two means. Conditional independent Bernoulli sampling from the scalar atoms preserves every coordinate mean and supplies the upper convex-envelope certificate with factor `1-1/m`. Coupled with the count correction bound, this proves convergence of actual ratios to `243/115` and `33/16`, respectively, and the retained m=20 and m=50 refinements. The m=16 affine bound is exact on all 289 count pairs and is attained by uniform counts (8,12). In the 52-variable example, the loss is bounded pointwise by `120 sum_k(1-z_k)` and therefore has expectation at most `12/5`, regardless of dependence. The 4,320 supports are distinct unit cubic supports.

For equal means, one adjacent-count uniform-subset law preserves the complete vector and has the displayed degree-d intersection probability for every subset simultaneously. Discrete convexity of `binom(K,d)` proves attainment for E_d; comparison to independence gives `q<=u^d<u`, ensuring positive denominators. Fixed-degree limits give the dimension-free supremum and convergence. Below `u/(1-u)`, the expression increases as `k/(u+...+u^k)`; above that point it decreases. This proves the stated floor/ceiling optimizer, including u<=1/2. Bernoulli's inequality gives two, approached by the even complete-graph example. The exact formulas remain confined to equal normalized unit-cube means.

### 7. Executed checks

I wrote and executed `verification/reviewer04/stage02-round01/check.py` using the repository's Python environment. Its output is `verification/reviewer04/stage02-round01/check.json`. It uses rational/integer arithmetic and symbolic polynomial identities, without a solver or floating-point feasibility tolerance.

The independent implementation checks actual O interval intersections and B conditional product integration for all 2,002 sorted quadratic/cubic tuples on the grid `{0,1/20,...,1}`, with separate singleton marginal checks. It checks dyadic resource profiles and cutoff ties for L=2,...,100, and every bit-reversal prefix count through L=8. It enumerates all `7^3+9^3+65^3` finite cubic count inequalities and their exact primal means, as well as the two-level residual minima. It reads the five Bernstein rows from the frozen manuscript itself, independently eliminates the two quadratics, and verifies both two-level identities and the reduced slack constant. It also checks the finite sampling margin and logarithm upper bound exactly. All checks passed.

The count enumerations are exhaustive certificates for the stated finite witnesses. The rational coupling grid and finite dyadic checks supplement the universal analytic proofs above; they do not establish continuous or all-dimension theorems on their own.

## Remaining limits

I did not independently compile or perform a page-by-page layout review of the frozen manuscript. I read its LaTeX definitions, statements, proofs, tables and printed checker. The independent checker verifies the finite mathematical claims without relying on a build or on the author's test statuses.

This review does not certify publication priority, absence of other literature, the exact value of R_3, globally optimal coupling choices, a matching second-order lower asymptotic, a small deterministic coefficient-removal construction, or any spatial-certificate consequence. Those questions are outside the proved Stage 2 claims or explicitly remain open. The accepted Stage 1 signing computation and its unrelated external norm inequalities were not independently recertified in this round.
