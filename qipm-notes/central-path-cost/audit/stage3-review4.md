# Stage 3 independent review 4

**Verdict: no major issues found.** The new radial upper bounds and uniform dyadic sequence comparison have valid proofs, and the scalar envelope, nonmonotone construction, exact parameter calculations, and maximizer localization are consistent. One minor regularity clarification is needed in the definition of the relaxed envelope class.

I reviewed all of `sections/04-barrier-dependence.tex`, `sections/04a-coupled-barriers.tex`, `sections/appendix-barrier-profiles.tex`, the new localization subsection in `sections/appendix-scalar-certificate.tex`, both changed/new verification scripts, bibliography additions, and the relevant earlier interfaces and literature audit. I did not read other review reports, communicate with other reviewers, or edit the manuscript. Pending front matter and Stage 4 are outside this review.

## Valid minor issue

**Specify local absolute continuity for the relaxed envelope class.** Location: `sections/appendix-barrier-profiles.tex:21–28`, the statement that `C(a)` is the exact envelope under the relaxed almost-everywhere constraints on `upsilon`.

The main assertion for `p in C^2` is unaffected: its `upsilon=p/p'` is continuously differentiable. But a class specified only by initial values and almost-everywhere differential inequalities need not permit integration of those inequalities. A continuous singular perturbation illustrates the gap in a literal reading: with a nondecreasing Cantor-type function `C` supported away from zero, `u(y)=1-e^{-y}-epsilon e^{-y}C(y)` can remain positive and at most one and obey `u'=1-u` almost everywhere, while violating `u(y)>=1-e^{-y}`. The relaxed-envelope derivation uses precisely that latter integrated bound.

**Repair:** explicitly say that the relaxed admissible functions `upsilon` are locally absolutely continuous on `[0,infinity)`, with the displayed inequalities holding almost everywhere for `y>0`. The proposed piecewise differentiable extremizers already belong to this class. No formula, constant, witness, or smooth-barrier theorem changes.

## Proof audit

### Normalized scalar class and exact relaxed envelope

- The normalization gives `0<v_f<=1` and `v_f'>=v_f(1-v_f)`. The argument for the unit positive-tail limit, exponential integrability of `1-v_f`, and integrability of the negative tail is valid. Thus the fixed-profile sharpness construction is justified without varying the profile with dimension.
- `x'(t)=e^{-t}v_f(t)^2` proves the right endpoint is finite. The support target and its approximation schedules therefore have a well-defined finite support value even though boundedness of the original interval was not separately assumed.
- The general target allocation is not assumed convex. Compactness in the metric coordinates gives existence; the first-order perturbation excludes zero coordinates; a nonzero constraint gradient permits the necessary multiplier equations at a global minimizer. The factor-two convention is harmless because the multiplier is freely named. The safe-scale comparison leads to the correct central parameter `lambda/log(2)`.
- Independently derived the two envelope time formulas by integrating `1/min(1,(1+u)e^q-1)`. The branch condition and the direction of substitution `u>=1-e^{-a}` are correct. Both branch denominators are positive in their stated ranges.
- The strict bound below two is supported by the displayed concavity/polynomial arguments. The endpoint limits and one interior value above the left endpoint limit prove attained maximality. The first branch has `a B'-B>0`; the second has strictly negative `B''`, so the unique-zero/unique-maximum argument is valid.
- The extremizing relaxed profile attains the minimizing prehistory and maximizing future velocity required by the calculation. The separate envelope proving that `log(2)` is the largest safe scale is correctly distinguished from it. The manuscript makes no unsupported smooth-profile minimax claim.

### Nonmonotone construction, fixed-profile sequences, spectral transfer

- `f_A''=P_A^2` and `|f_A'''|/(f_A'')^(3/2)=2|P_A'|/P_A<2` follow directly from `X_A'=1/P_A`. The construction has a finite interval, an analytic center, full gradient range, and divergence at both endpoints.
- The parameter bounds `A^2/9<nu_A<=(A+1)^2` hold on the whole interval, including the exponential tails. In particular the parameter really diverges in the sharpness limit.
- The disjoint translated windows provide the claimed total length, and the terminal-coordinate logarithmic bound controls every endpoint coordinate. Taking `A` to infinity at fixed `r,delta,B`, then decreasing `delta`, yields the exact supremum `sqrt(r)` with the quantifiers in the statement.
- The fixed-profile dyadic proof uses only constants depending on the fixed profile, shifts all thresholds by the same amount, and preserves the parameter gap of order `r^(2/3)` needed by the growing-tube proof. Actual objective accuracy forces the terminal label; no monotonicity of the labels is used.
- The polynomial approximation proof of the trace-separable Hessian formula has enough derivative control. Positive objectives use the positive branch; the evenness hypothesis for rectangular matrices ensures the Hermitian dilation gives the claimed singular-value metric. The text explicitly does not infer spectral self-concordance from scalar self-concordance.

### Facet collar and exact-parameter couplings

- Convexity in the first coordinate and the full-collar gradient bound correctly force entry into the collar while other coordinates are unrestricted. This would not follow from a vertex-only hypothesis, and the distinction is explicit.
- The inverse-Hessian variational estimate and the asymptotic active-coordinate summands produce the central-arc lower bound. The transformed straight route from a fixed interior point stays in the collar; its extra curvature length is bounded by total Euclidean variation. This gives the required endpoint upper estimate.
- The same-accuracy conclusion is valid: strict monotonicity of the objective along the central path makes the selected terminal gap the first-accuracy gap, and the entire target set can only have smaller distance than that central endpoint.
- Checked the dense Sherman--Morrison calculation, all three estimates using the gradient slack `m`, and the numerical coefficient `17/32`. The quadratic preserves standard self-concordance.
- Checked the radial derivative formula and the scalar numerator/denominator difference proving the parameter bound. The directional limit along the positive diagonal gives parameter at least `r`, while the upper bound gives at most `r`. The uniform positivity of `c-||x||^2` permits the bounded-derivative argument.
- The singular-at-vertices example keeps its last coordinate small, making the coupling bounded along the relevant paths. Its effective `r-1`-coordinate construction and its separate `r+1` parameter are justified.

### New radial comparisons and uniform arbitrary-label sequence bound

- The global domination `D <= F'' <= (11/8)D` follows from `D>=2I`, `x^T D^{-1}x<=t/2`, and the two scalar maxima. It holds everywhere in the full cube, including paths outside the active subspace, uniformly in the allowed parameters.
- Differentiated stationarity gives the stated formula for `a'`. The bound `K<=t` is valid coordinatewise and yields `0<=a'<=1/4`.
- The estimates `7/10<=theta_i<=5/4` have the right signs and imply monotone coordinates. Ordered `v_i`, rather than an unproved ordering of the actual coupled speeds, is exactly what the prefix argument uses. This gives the prefactor `sqrt(11/8)*25/14` as stated.
- The same-accuracy proof uses the correct comparison `4z_i/5<=q_i<=z_i`, the parameter enlargement by `5/4`, and the inequality `H(s+log(a))<=a H(s)`. Applying the direct transformed-coordinate length bound avoids introducing an unjustified reverse bound on the coupled endpoint distance.
- The radial dyadic proof has constants uniform over `lambda,c` varying with rank. Its common velocity threshold, shifted early interval, actual terminal accuracy, and initial tube control are all sufficient. Global metric domination allows the clipping proof in the `rho` coordinates, so backward labels and the analytic-center label remain covered.
- The unrestricted route is feasible and accurate, and the global upper metric comparison bounds its length. The resulting growing-tube denominator and fixed-neighborhood separation are consistent with the earlier theorem.

### Every-maximizer localization

- The `h_1`/`h_k` endpoint tests exclude scalar ratios above the certified lower bound outside the stated elasticity interval. Their derivative signs and minimum location have the correct direction.
- `E=Y(v)/v` is strictly increasing, and the two rational `Y` bounds locate every possible maximizer in the claimed `v` interval. Positive squaring transfers it to the stated `x` interval. No uniqueness assertion is smuggled into this localization.
- Differentiating `P(W)=Y A` yields the displayed stationarity equation, including the factor `A(W)`.

## Independent verification and attribution

- Ran `verify_barrier_dependence.py` with the existing qipm interpreter. All 96 nested scalar center solves, parameter/metric/speed bounds, and three arc comparisons passed. Maximum relative finite-difference tangent error was approximately `1.22e-9`. The independently solved numerical envelope maximum was `a=0.6501143834529713`, `C=1.831856422983876`.
- Ran the extended `verify_scalar_certificate.py`. All exact arithmetic assertions passed, including every localization logarithm, `Y`-series tail, and squared-radical enclosure.
- These numerical checks support, and do not replace, the analytic proofs. The scalar localization script is an exact finite certificate.
- Read the local primary Chewi theorem/tensorization discussion and Castro--Cuesta Section 4.1, including the small diagonal regularization conclusion. The manuscript correctly credits the exact dimension bound, canonical factorization history, and parameter-preserving diagonal regularization. Its present claims concern the proved centrality comparisons and the explicitly coupled examples. No unsupported priority expansion was identified.
- The existing final build log reports 34 pages and no undefined references, warnings, or overfull boxes. No shared build was run during this review.

No additional mandatory minor issue was found. The proof order is coherent, and the distinction between fixed scalar profiles, relaxed scalar controls, arbitrary self-concordant profiles with growing parameter, and the explicitly coupled radial family is maintained.
