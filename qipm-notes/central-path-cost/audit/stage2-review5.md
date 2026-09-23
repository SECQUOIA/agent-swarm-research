# Stage 2 independent review 5

Reviewed 2026-09-07. I read all four new manuscript files, both verification scripts, the integrated main file and relevant revised foundations, the bibliography, source map, literature ledger, and root's additional primary-source screen. I did not read other review reports or communicate with other reviewers. Temporary front matter and future-stage placeholders are excluded.

## Verdict

**No major mathematical issue identified in the intended Stage 2 theorems.** The sharp prefix result, scalar certificate, distribution laws, dyadic family, and discrete tube proof survive independent checking. Four minor scope/notation repairs are required below. In particular, two contextual assumptions need to be stated explicitly; the intended proofs already supply what is needed, so these do not require redevelopment of a theorem. No final priority or submission-readiness verdict is implied for the unfinished full paper.

## Required minor repairs

1. **State the conic projection hypothesis.** `sections/03a-distribution.tex:94–99` says that a conic central path with gap `nu/eta` inherits the displayed primal tail bound. The gap identity alone does not identify its primal projection with the standard spectral-barrier path used to prove that bound. Add that the conic path's projection is the path just analyzed, for example because the cone barrier restricts to the unit-scale spectral barrier up to an additive constant and the objective/parameter agree. Specify that primal length uses this restricted metric. The precise restriction contract already appears later in the residual-transfer paragraph and can be referenced. This matters: duplicating a slack inequality changes a restricted barrier and its central path while preserving a logarithmic-homogeneity gap identity. No central-path or metric equivalence follows merely from `gap=nu/eta`. I classify this as a minor narrative scope omission because it is outside the formal tail corollary and has an immediate intended restriction.

2. **Explicitly change the barrier in the unequal-scale subsection.** `sections/03b-discrete.tex`, subsection “Unequal scales can produce a larger discrete separation,” introduces alpha_i and immediately uses weighted radial coordinates. The section opening says *throughout this section* `F=sum_i b(x_i)`. Add at the subsection opening: “In this subsection replace the unit-scale barrier by `F_alpha(x)=sum_i alpha_i b(x_i)` on the product of r scalar intervals; all norms and distances refer to this barrier.” Without this override the displayed endpoint distance `H_0 sqrt(r)` is not the distance in the declared F metric. The intended weighted proof is correct and needs no mathematical change, but the metric must be explicit.

3. **Identify the support-direction sign in the LP section.** `sections/03b-discrete.tex:5–7` introduces objective `-sum_i w_i x_i`, whereas the earlier gap definition `g_c=h(c)-<c,x>` and central-coordinate formulas use the maximized direction `c=w`. The tube theorem subsequently writes `g_c` without specifying c. Say “minimize `-w^T x`, equivalently maximize the support direction `c=w` used in g_c.” This prevents a literal reading with `c=-w`, which would reverse the accurate face. The conic minimization convention later in the section can remain as written.

4. **Specify eta positive in the pointwise distribution inequality.** `sections/03a-distribution.tex:19–30` uses `Q_1(eta)/eta` without an explicit range. State that the pointwise bound holds for `eta>0` (or give its continuous extension at zero); the integral bound can still explicitly include `eta_0=0` as it does now. This is a boundary-notation correction only.

## Proof review

### Exact scale-order supremum and accuracy comparison

- Differentiation of the scalar central equation gives `dx/ds=x(1-x^2)/(1+x^2)` and `v^2=1-(1+exp(2s))^(-1/2)` with the stated normalization. The integrable tail bounds justify both `H(s)=s+kappa+o(1)` and a uniform finite error when replacing a translated velocity by a step function.
- The weighted prefix decomposition has the correct coefficients `d_i=sqrt(S_i)-sqrt(S_{i-1})`. Weighted Cauchy–Schwarz gives exactly `Gamma^2=sum d_i^2/alpha_i`. Central spectra remain coordered within a factor, including signed Jordan eigenvalues, so the earlier endpoint-distance equality is applicable to arbitrary central subarcs.
- The sharpness construction has strictly decreasing `c_i=d_i/alpha_i`, hence strictly ordered activation thresholds. Its endpoint distance is `M Gamma`; the step-profile arc is `M Gamma^2+O_alpha(1)`. The uniform sigmoid-to-step integral error is independent of M. The resulting supremum is correct for the prescribed ordered scale vector; it does not assert an unattainable finite maximizer.
- `d_i^2/alpha_i=tanh(log(S_i/S_{i-1})/4)` for i>=2. Strict concavity gives the scale frontier and equality condition. For adjacent a<=b, `(S+a)(S+b)>=S(S+a+b)` is exactly the comparison needed to make the increasing-scale order more balanced in the two logarithmic increments; the exchange proof is valid. The S=0 case is correctly handled separately.
- The same-accuracy KKT comparison has the correct multiplier factor: at eta=lambda/2, `p(y_i^c)=y_i^*p'(y_i^*)`. Monotonicity makes this center accurate, and the first accurate center is coordinatewise earlier. The paper correctly distinguishes the sharp scalar constant from an unproved sharp product arclength constant.

### Scalar rational certificate

- The v transform, Y, A, and P identities check by direct differentiation. The displayed W is the inverse P-coordinate of `Y(v)A(v)`. Both endpoint ratios tend to one; strict convexity makes the interior ratio exceed one, proving finite attainment.
- Independently deriving the elasticity identity gives `dE/dlog y=E-K`, with `E=Y/v`. The bound K<1 follows from the displayed B derivative comparison. The D upper envelope, E>2 implication x>4/5, monotonicity of G, and K<107/200 all have the required inequality directions.
- Integrating the elasticity inequality yields the stated h_1 and h_k, with the correct coefficients of log(a), E, and k. The minimum location 50/19 and every rational logarithm bound agree with the appendix.
- The lower certificate uses positive series tails and squared positive radicals correctly. Its two inequalities imply `P(w_0)<Y(v_0)A(v_0)` and `Y(w_0)>a_0Y(v_0)`, the required strict witness. There is no reliance on a numerical stationary-point search or presumed uniqueness.

### Distribution, decay, and lower certificates

- The Q1 and Q2 constants follow from the stable scalar identities. The zero-parameter integral is convergent. The piecewise antiderivative differentiates to `sqrt(m+B eta^2)/eta`.
- The tail corollary properly separates the early interval from eta>=1 and uses the global bound `v^2<=z^2/2`. The nuclear-tail sharpening uses `min(z^2,1)<=z`, giving speed at most sqrt(2m). All stated head/tail factors agree with the proof.
- Both geometric and polynomial decay results explicitly impose the rank needed for the lower certificate. Their tail-integral upper bounds remain uniform in larger finite truncations. The polynomial upper length has no extra logarithm, because the square root of active rank grows as eta^(1/(2b)).
- Removing the determinant factor two by exact allocation is valid. The inverse-square-root logarithmic-coordinate example really defeats the stronger certificate: its logarithmic optimum diverges as c sqrt(log r), while `e^c sqrt(er)/B_r` eventually falls below one. Weights are decreasing and their total exceeds epsilon, so the example satisfies the allocation theorem's nontriviality range.
- The compressed logdet Hessian comparison follows from convexity of the negative logdet Schur-complement remainder. The compressed gradient parameter is m. The Hadamard/objective-error argument handles off-frame matrix endpoints. The direct allocation proof makes the Jordan/product statement independent of this matrix-only compression explanation.

### Dyadic finite-input and neighborhood arguments

- Each A_i for i>=2 is uniformly Theta(r), so ordinary rational encoding uses Theta(r^2) bits. Rational summation before flooring can be performed with polynomial bit complexity; the proof does not substitute an exponent encoding or irrational input for this claim.
- The first-accuracy window follows from the scalar error bounds on all but O(sqrt(r)) final channels. Rounding changes thresholds by a uniformly bounded amount. The endpoint-distance harmonic sum and the coordinatewise accurate-allocation lower bound give matching Theta(r sqrt(log r)) orders.
- The central length lower bound handles accumulated flooring error by summation by parts, avoiding an erroneous O(r) sum of weighted individual errors. Its r log r leading contribution is correct.
- The growing-tube proof correctly bounds center-to-center distance by `C_r=2 delta_r-log(1-R)`. Clipping labels into [0,b] contracts each coordinate difference. For clipped u<=t, the first j channels give `Delta<=C_r/(v_0 sqrt(j))`; threshold spacing yields the claimed progress increment. Backtracking is covered by summing absolute increments.
- Actual final accuracy forces a large first coordinate; initial tube proximity bounds initial progress. The margin `T-b=Theta(r^(2/3))` dominates both log r and the allowed tube radius. The condition for diverging overhead follows from the correct `C_r sqrt(1+C_r)` denominator.
- The decrement lemma's segment integral gives `t<=lambda/(1-lambda)`, and the radius beta<1/2 is exactly what is needed for the logarithmic distance conversion. The conic residual pullback has the correct signs and requires only the explicitly stated restriction, AB=0, and B*c=-w. No dual-feasible shortcut is inferred.
- For spectral embeddings, trace inequalities imply a large leading singular value/eigenvalue at an accurate endpoint. Spectral contraction controls distances to labels and between labeled centers, so off-frame iterates do not invalidate the proof.
- In the intended weighted metric, every unequal-scale core has weighted coordinate gain Theta(H_0), uniformly for large U. A jump meeting three cores crosses the middle one fully and violates its center-distance allowance. At most two clipped gains are bounded by sqrt(2) C. The same-endpoint comparison and explicit parameter-crossing assumptions are consistent; they are not silently replaced by the equal-scale accuracy-forcing theorem.

## Executed checks and source review

Both supplied scripts passed with `/home/sgusev/miniconda3/envs/qipm/bin/python`, with no dependency installation. The rational script checked all exact margins and radical/series enclosures. The numerical script checked all 120 orders in each of 80 five-channel instances, sharpness convergence to Gamma=1.2748644298632108, and 401 scalar speed/error values. Its numerical nature is appropriately stated.

I additionally implemented a dyadic instance using exact Fraction sums and integer square-root ceilings, with r=512. Using stable scalar formulas and independent quadrature/root solving gave `s_epsilon-T=-0.00678403786423587`, endpoint distance `5798.766283293374`, central arc `8898.384502638977`, and ratio `1.5345306342619476`. A conservative cutoff J=63, below the exact floor(r^(2/3))=64, had minimum early gap `2.7725887222395613`. Across 2,000 random label pairs (seed 9915), the progress-increment upper bound had positive surplus, minimum approximately `0.00235450`. This is a diagnostic check, not a proof of the universal jump bound.

An independent computation of the stronger rank certificate with c=0.1 and epsilon=0.5 gave maximum untruncated certificate ratios 0.8891053, 0.8470052, and 0.8318239 at ranks 100, 1,000, and 10,000, respectively. Thus every positive-part term vanished in these examples while the logarithmic distance increased, as the proof predicts.

The final existing build log reports 20 pages and contains no warning, undefined reference/citation, or overfull/underfull-box message. I did not run a shared build while other reviewers might be building.

I read the Lorentz primary extraction, PDF pages 2–4, confirming the decreasing-rearrangement norm and triangle-property antecedent. The manuscript's limited attribution is appropriate; the central-path realization is not attributed to Lorentz. The earlier primary Nesterov–Todd/Nesterov–Nemirovski comparisons remain consistent with this stage. The root's expanded source screen and source map distinguish the future primal–dual prior result from present sharp standard-barrier claims. There is no broad unsupported first-result assertion in these sections. The promised full-manuscript priority synthesis remains a later responsibility.

The source map's Stage 2 topics are represented in the draft, including unequal scales, explicit input encoding, arbitrary labels, growing tubes, residual transfer, both decay laws, and the strengthened rank-certificate counterexample. I found no missing Stage 2 theorem promised by that map.
