# Stage 2, round 1, reviewer 02

**Verdict: MINOR.** I found no defect affecting a Stage 2 theorem, certificate, scope claim, or attribution. One strict comparison in an appendix sentence should be weakened to a non-strict comparison. The proof already uses the valid subsequent bound, so no mathematical result changes.

## Coverage

I read the frozen files under `process/snapshots/stage02-round01/`: `main.tex`, `macros.tex`, `references.bib`, all of `sections/02-universal-positive.tex`, `sections/03-cubic-equal-means.tex`, `sections/appendix-positive-couplings.tex`, `sections/appendix-cubic-certificates.tex`, and `sections/01-foundations.tex`. I checked the shared vertex-law, positive upper-envelope, deficiency, independence, continuity, and nonnegative-box-transfer proofs directly. The signed-bilinear portion is accepted background; the Stage 2 arguments create no new dependence on its finite-signing computation, so I did not repeat that enumeration or reopen its signing appendix.

I read `process/review-protocol.md`, both Stage 2 assignments, `process/stage-02-author.md`, and the Stage 2 scope rows and dependency instructions in `process/scope-proposal.md`. I read these canonical result files in full, relative to the repository root:

- `results/positive-multilinear-gap.md`;
- `results/positive-multilinear-degree-upper-bound.md`;
- `results/positive-multilinear-sharp-degree-growth.md`;
- `results/positive-multilinear-second-order-upper.md`;
- `results/positive-multilinear-coefficient-removal.md`;
- `results/positive-cubic-gap.md`;
- `results/positive-cubic-analytic-family.md`;
- `results/positive-cubic-two-level-family.md`;
- `results/positive-cubic-rounding-upper-bound.md`;
- `results/positive-multilinear-equal-marginals.md`.

I inspected the linked earlier audit records for corrections and checked the relevant correction arguments: the distinction between dense and sparse count models, nested realization, optimized rather than original harmonic cutoff, Bernstein slack, the second rational two-level variant, and coefficient-removal quantifiers. Those records' verdicts were not used as proof. I did not read another current-round report, edit manuscript files, or delegate work.

After reading `literature/AGENTS.md`, I directly checked these primary sources:

- Luedtke–Namazifar–Linderoth's local author-manuscript original: equations (7)–(8) and Theorems 4–5 on pp.8–9, positive bilinear Theorem 8 on p.15, and Conjecture 1 on p.22. I visually checked the conjecture in the original PDF. It does ask for the uniform positive-coefficient, nonnegative-box comparison that the dyadic sequence disproves.
- Sherali's local original: equation (13), Theorem 3, and its proof on printed pp.252–255 (PDF pp.8–11). I visually checked the displayed formula and theorem on pp.252–253. The binomial coefficient, constant term, and index range in `eq:sherali-symmetric` agree with the source after replacing its degree `m` by `d`.
- Hoeffding's original already available at `/tmp/stage02-hoeffding.pdf`: direct visual inspection of printed p.16/PDF p.5, Theorem 2 and equation (2.6), using its rendered page. Its independent bounded-variable hypothesis gives the manuscript's two-tail sum inequality after rescaling the source's sample mean. This is direct original-page inspection, not reliance on a secondary quotation. I did not need a new download.

No required Stage 2 primary source was inaccessible. I did not repeat the broader novelty search or the primary-source audits of unrelated accepted signed results.

## Findings

**S02R01-R02-01 — MINOR: replace one strict comparison by “at most.”**

Location: frozen `sections/appendix-positive-couplings.tex:19–20`, proof of `prop:arbitrary-dyadic`, sentence beginning “The interval ... contributes less than”.

The contribution on `0<t<=delta` can equal `delta * sum_{j=1}^L 2^j`. Take the admissible nonincreasing quantile `r(t)=m` for `0<t<=1/m=delta` and zero otherwise. Its integral is one. All anchors are selected throughout this interval, so the integrand there is exactly `sum_j 2^j`. This also corresponds to a feasible binary law: all leaves fail on this event and none fail otherwise, giving every leaf failure mean `1/m`.

The valid chain is “contributes **at most** `delta * sum_j 2^j < 2`.” The final strict bound by two is correct because `delta * sum_j 2^j = 2-2/m`. The displayed bound `H<=2+...` and the proposition are unaffected. Repair only the words “less than” to “at most.”

## Independent verification

I wrote and ran `verification/reviewer02/stage02-round01/check.py` with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`. It passed; exact values and residual lists are in `verification/reviewer02/stage02-round01/results.json`. The script uses integer/rational arithmetic and symbolic polynomial identities. Its finite loops are supporting evidence for the parameterized proofs, not substitutes for them.

### Dyadic construction and distinct predecessor arguments

The upper-tail exchange is valid simultaneously for every anchor because only its individual mass is prescribed. The surrogate is an upper bound on the maximized deficiency. For nested partitions, bit reversal makes its relaxation exact: the first `R` strings contain exactly `min(R,2^j)` distinct length-`j` prefixes, and XOR shifts act transitively on leaves while preserving all level partitions. Conditional failure mean is therefore `R/m` for each leaf, including `R=0,m`.

I checked the affine certificate's direction and equality intervals. Summing its intercepts gives `(L-s)/2^s`. The profile means are `B_q=(L-q+2)/2^q`, and the mixing weights are nonnegative, sum to one, and force `E R=1`. The endpoint `l=s` uses equality at counts zero and two. The script independently verifies the budgets, mixture values, all piecewise-linear breakpoints, and adjacent-cutoff equality for `L=2,...,64`, and every failure count and level in the prefix construction for `L=2,...,8`. The written prefix argument establishes arbitrary `L`.

The monomial and occurrence counts are `2^(L+1)-2` and `L2^L+2^(L+1)-2`. The largest degree is `2^(L-1)+1`; choosing the largest admissible `L` proves both all-integer asymptotics with leading constant one. Homogenization preserves the face values and monomial count, with the correctly stated larger occurrence count and interior approximation rather than interior equality.

For arbitrary partitions, the logarithmic pointwise estimate and Jensen argument have the correct inequality directions, including zero quantile mass. The first interval has the small wording issue above. The dense polynomial's union-bound comparison is valid, and its count LP has both realization directions: a uniform failed subset and conditionally sampled anchors recover all means and the specified objective. No dense LP value is substituted for the sparse hull value.

The older dyadic coupling preserves each failure probability as `h(p/h)=p`. Its scale selection is within the stated set because `N(s)<=d-1`, including `d=2`. The tail lemma correctly separates `S<=u` from `S>u`; continuity of the integral supplies the truncated mass-one interval in the latter case. Summing the `K` scale guarantees and adding independence gives `2(K+1)/c_0`.

### Harmonic constants, endpoints, and asymptotic directions

For every permitted real `M`, `h_p>=p`, `1<=A_p<=Lambda`, and the integral of `q_p` is exactly `p`. The explicit `p=0` rule covers the boundary. On the hard-term integration interval, inactive mass is at most `eta*t`, so active mass is at least `t_e-eta*t`. The conditional-union lower bound therefore has the stated exponent and sign. Zero gaps and `p_max>=t_e` are treated before divisions and give valid zero lower bounds.

The scalar guarantee `J` is convex with derivative `-F`; hence its tangent has the sign used in `J(z)+a z >= (1+a)zeta`. The mixture weights favor the appropriate reciprocal guarantee and normalize correctly. Evaluating both scalar curves at their crossing proves exactly the limited scalar-family optimality claim. Positive expansion is used in the safe direction `T_original<=T_expanded`, with equality of the full hull gap.

The quadratic integral is

`1/z-1+2 eta log(z)+eta^2(1-z) <= 1/z`.

The negative logarithm and `eta<=1` justify discarding the extra terms. At `A=w-1/(2w)`, the exact residual is

`log(1-1/(2w^2)) + 1/(4 A w^2) <= 0`

because `w>=1` gives `A>=1/2`. Thus `J(A/Lambda)>=A/Lambda`, so the root is **at least** `A/Lambda` and the reciprocal ratio certificate is an **upper** bound. The case `w<1` remains covered by the fixed-point theorem, without using this optional certificate.

The original finite `24 Lambda/(c_0 log Lambda)` bound retains a nonempty integration interval for `Lambda>=16`; its harmonic gain and equal-mixture factor are consistent. The older leading mixture has `b>=6`, `b-3 log b>0`, and the inverse-guarantee weights `1/h,a,2/c_0`. For the tuned cutoff, `Lambda=N+log N` and `eta=1/N`; the numerator adjustment is `O((log N)^2/N)=o(1)` in the denominator. This proves the displayed upper expansion with no matching lower assertion.

For the original cutoff, `ell>=4` makes `ell-log ell-2>1/2`. The reciprocal proof's integrated cubic remainder is bounded by `1/(12 alpha^2)`. The other terms are `O(log Lambda/Lambda)=o(alpha^-2)`, yielding `alpha=w-1/(2w)+O(w^-2)` by the stated mean-value argument. I found no missing constant or reversed inequality in these finite and asymptotic bounds.

### Cloning, sampling, and finite homogeneous bounds

The cloning argument proves equality of complete feasible expectation intervals: conditional independent original rounding realizes `f(q)` from any clone law; identical clones embed any original law. Homogeneity is what supplies the common scale `m^d`. Distinct supports remain distinct after cloning.

Uniform control is over all `2^(nm)` vertices plus the term-gap event. The exponent with `t=K m^((d+1)/2)` is `-2 K^2 m/s`; the strict threshold `K^2>sn log(2)/2` dominates the vertex count for the fixed original instance. Each envelope incurs error at most `t`, and `H` at most `2t`. The use of continuity and positive limiting hull gap is sufficient for convergence of ratios and makes no fixed-dimension claim.

The finite constants check exactly:

- quadratic coefficient sum `1840`; loss `1840/1000=46/25`; hull bound `3225/7+46/25=80947/175`; ratio bound `165025/80947`;
- `2(1/10)^2/464=1/23200`; at `m=1000`, even replacing `log 2` by one gives a negative failure-bound logarithm;
- `943-2(80947/175)=3131/175`; the sampling error is `t+2(2t)=5t`, leaving the positive margin `3131/2275-1/2` after normalization;
- `16*binom(16,2)+20*binom(16,2)=4320`; the explicit 52-variable loss is `120*20/1000=12/5`, giving `2160/(1072+12/5)=2700/1343`.

### Cubic certificates and two-level families

Independent full integer enumeration checked all `343+729+274625` three-group count states and all `289` two-group count states. Every affine minorant is valid; every listed primal probability is nonnegative; each law has the exact count mean; and each used atom is tight. Uniform conditional success subsets then establish every individual marginal, so these are complete finite envelope certificates rather than tests of a restricted dependence class.

The resulting exact `(cav, vex, H, T/H)` values are:

| Variables | Concave envelope | Convex envelope | Hull gap | Ratio |
|---:|---:|---:|---:|---:|
| 18 | `1647/4` | `2750/13` | `10411/52` | `20891/10411` |
| 24 | `971` | `3572/7` | `3225/7` | `6601/3225` |
| 192 | `587944` | `34172072/105` | `27562048/105` | `7443345/3445256` |
| 32 | `2160` | `1088` | `1072` | `135/67` |

I independently eliminated `(a,b)` from the analytic residual using differentiation and solved the unrestricted quadratic stationarity equations. Its Hessian determinant is `248`. On the first region, the boundary gradient has the correct sign: `(a-1)*partial_a h>=0`. The derivative at `c=3/10` is `-31/60`. The resulting quartics reproduce all five rows of the actual frozen Bernstein table after conversion from power coefficients; their 25 coefficients have minimum `901/120000`. This is a continuous certificate because each row's Bernstein basis is nonnegative and sums to one on its interval, and the intervals cover the full required range.

The normalized count expansion has negative correction at most `72/m`. The affine mean is `139/6`, and the six orbit contributions sum to the stated exact upper and termwise-gap formulas. Subtraction gives the upper hull denominator with `+135/(4m)+9/m^2-delta_*`. In particular,

`(161/4)/(223/12-901/120000) = 4830000/2229099 = 1610000/743033`.

The manuscript correctly treats this as a supremum lower bound, without asserting attainment of the affine minorant or convergence of the actual analytic-family ratios.

Both two-level sum-of-squares identities were checked exactly, including their equality atoms, weights, and means. For the main family, the finite correction is at most `9/(8m)`, giving `H_scaled<=115/216`; conditional independent sampling from the equality atoms gives the reverse lower bound `(115/216)(1-1/m)`. These opposite hull bounds give the displayed ratio interval and actual-ratio convergence to `243/115`. The alternate coefficients give scalar mean value `83/150`, correction `49/(50m)`, hull constant `32/75`, and ratio limit `33/16`. The retained finite values `4617/2300` and `1617/800` follow by substitution. The interior and all-means-above-one-half claims use continuity only where a strict finite margin is available.

### Cubic upper law and equal means

The endpoint-orientation deficiencies are the expected maximum of independent half-selected nested exclusion lengths. Their sorted-sum bound has factor `(1-2^-k)/k`, decreasing in `k`; this gives `8/3` at degree three.

I checked all low-coordinate classes of the three-law proof, including the four one-low cases and their shared boundaries. Their inequalities sum to `18D_O+7D_B>=12t`; independence's omitted contribution is nonnegative. For all-high cubics, the exact union integral gives `D_B=D_O=a/2+b/4`, and the independent fraction is at least `7/16`. The constants combine as `25*3/8+6*7/16=12`. The quadratic cases also reach at least `12/31`. The three optimality tests have the displayed exact or limiting normalized deficiencies, and weights `3/31,4/31,24/31` cancel both free mixture coefficients. This proves only the stated fixed-mixture termwise optimum.

For equal means, the adjacent-count law is feasible for all coordinates and degrees at once. Convexity of the interpolated sequence `binom(K,d)` proves the lower envelope for `E_d`; comparison with the binomial independent law gives `q<=u^d<u`, so all denominators are positive. Fixed-degree limits give the lower direction for the dimension-free supremum. The candidate expression increases below `u/(1-u)` and decreases above it, proving the floor/ceiling optimizer. Bernoulli's inequality gives the factor two in the correct direction; the even complete-graph ratio `2(n-1)/n` proves sharpness. The exact formulas remain confined to equal normalized unit-cube means.

## Remaining limits

The exact value of `R_3`, optimal finite degree constants, and a matching second-order lower asymptotic remain open as stated. This review does not certify literature priority or absence of a prior construction. The author's build report was not used as mathematical evidence, and I did not repeat a PDF build or the accepted Stage 1 signing enumeration. Those limits do not affect the Stage 2 proof checks above.
