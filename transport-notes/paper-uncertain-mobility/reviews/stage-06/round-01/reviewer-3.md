# Independent review: Stage 06, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Reviewed snapshot: `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`.

I recomputed SHA-256 for every file listed in the supplied manifest; all hashes matched. I reviewed the complete `sections/06-finite-precision.tex`, the author handoff, and the accepted scalar-form, singular-measure, interval-localization, and exact-observation prerequisites. I did not read other reviewer reports or coordinator checks, edit source files, or delegate work.

## Local value: arbitrary measures, attainment, and continuity

The local physical scaling gives mass `a ell^5=m` and response factor `1/(a ell)=a^(-4/5)m^(-1/5)`, with normalized center span `w/ell`. The test used for the exact large-width lower bound has amplitude eta^(1/2) and width eta^(-1/4). Its source and reaction both scale as eta^(1/4). Integrating its derivative kernel over center positions and dividing by the center width also gives eta^(1/4), multiplied by the profile derivative energy. Therefore the oscillator variational lower bound `C0 eta^(1/4)` is exact for every positive eta and covers arbitrary concentrated mobility.

The padded constant upper trial has oscillator length much smaller than its unit endpoint padding at large eta. Free-endpoint harmonic localization is uniform because the minimum distance from any possible center to either endpoint, in oscillator units, tends to infinity. The reciprocal exterior costs at most two. The resulting coefficient is C0. For bounded eta the same padded trial has uniform positive coercivity and gives the claimed finite upper bound.

The quadratic expanding-interval argument retains the correct slower source-tail bound L^(-1/2). Its local pointwise energy estimate has powers |x|^(-2) and |x|^(alpha/2-1); alpha<2 makes the limiting energy function bounded. This permits a remote cutoff even for unbounded integrable d, followed by compact weighted-derivative approximation. The interval endpoints may approach infinity at different rates, since all compact intervals are eventually included and both source tails have the same uniform bound. Locally uniform metric convergence suffices; no uniform convergence at moving endpoints is assumed.

The singular-measure removal construction applies to translated quadratic reactions, which remain bounded on each fixed test support. Compact-test lower semicontinuity is joint in vague mobility and center convergence. A common countable smooth core supplies measurability for Fatou. Attainment of the local infimum does not require tightness of the original sequence: after vague convergence and singular-mass removal, adding any missing mass as a density can only lower the response. This produces a unit-mass density with value at most the infimum, hence equality. The same argument applies with eta varying, proving lower semicontinuity.

For upper semicontinuity, the positive-tail regularization has an energy at least the original energy divided by 1+epsilon, giving the pointwise response comparison in the text. On compact center sets, shifting the quadratic potential perturbs the anchored form by a relative quantity tending to zero. The fixed regularized competitor therefore has a continuous averaged response and supplies the required limsup. No strict mass scaling, uniqueness, or unproved monotonicity in uncertainty width is used.

## Conditional liminf against adversarial designs

Reflection preserves each individual cosine rate, so it can be applied within any bin, including a bin not symmetric under c-to-minus-c. Symmetric competitors have exactly M/2 on each half-circle. Pushing the first half-circle's mass to the rescaled root coordinate and dividing by M/2 gives measures of mass one on expanding intervals; a vague limit can have smaller mass, which is allowed.

The local expansion of the unsquared rate is `eta_I v-x+O_K(ell_I x^2)`. With source amplitude `(a_I ell_I^2)^(-1)`, each source, reaction, and mobility energy has common factor `(a_I ell_I)^(-1)`. Reflection gives two copies with the same limiting measure. Thus the normalized liminf is precisely the local response at center eta_* v. It remains valid if mass concentrates at points, oscillates below the placement scale, or escapes to infinity in the rescaled coordinate. Singular removal and completion to mass one give the local lower value after Fatou. This avoids an interchange of a limiting optimizer with either the offset integral or the source-test supremum.

The upper construction also preserves the correct factor of two. Its exact coordinate satisfies `ds=ell_I w_I dx` and makes the potential exactly `a_I ell_I^2(x-eta_I v)^2`. Choosing mobility `a_I ell_I^4 w_I d` cancels the metric in the derivative energy, while source and reaction retain w_I. The half mass is `m integral w_I^2 d`, tending to m by dominated convergence. A single normalization restores exactly M. The weighted interval lemma controls the source response uniformly on compact center ranges, and all possible roots lie a fixed distance inside the selected physical neighborhoods, giving a bounded exterior contribution.

Uniformity over bins on a fixed compact offset set follows from these sequential arguments and continuity. A finite collection of regularized profiles suffices for any desired error on the compact center-span range. This is a finite-bin decision rule, not a measurable-selection assumption. Since there are finitely many bins at each M and Delta, the original decomposition into conditional infima is also justified even without a circle minimizer.

## Regular bins, crossing bins, and every relative rate

For regular bins, the possible-root width is of order `w=Delta/sqrt(t)` and the padding is `ell=(M/t)^(1/5)`. With `t>=C(Delta+M^(2/7))`, both w/sqrt(t) and ell/sqrt(t) are uniformly small for a sufficiently large fixed C. The constant patch mobility is comparable to `M/(w+ell)`, whose harmonic length is at most a constant times ell. Thus the endpoint margin is adequate even when the bin span is much shorter than the placement width.

The exterior reciprocal cost `1/(t ell)` equals the harmonic scale based on ell alone and is therefore bounded by the padded-patch response. The additional `t^(-3/2)` term is smaller because ell/sqrt(t) is small. Expanding the fourth root of w+ell gives exactly the two powers `M^(-1/5)t^(-4/5)` and `M^(-1/4)Delta^(1/4)t^(-7/8)`.

For crossing bins, taking every bin meeting a fixed multiple of W enlarges the group by at most Delta, which is no larger than W. This is valid for folds at edges, inside cells, or on changing alignments. The fold patch radius is a sufficiently large fixed multiple of sqrt(W), and its mobility is comparable to `e=M/sqrt(W)`. The condition `W>=M^(2/7)` is exactly what gives `W>=c e^(1/3)`.

The central quartic response integrates to O(e^(-1/6)). The rootless local tail is of that same order. The separated-root side integrates to `O(e^(-1/4)W^(1/4))`, which absorbs the core because W is at least a constant times e^(1/3). These estimates also hold for the finite patch: compact scaled parameters have a uniformly coercive interval, and for separated roots the endpoints remain a fixed relative distance away. Rootless tails require only an upper reciprocal bound, not a false joint whole-line equivalent. The exterior patch and remaining rootless bins contribute `W^(-1/2)`, absorbed since `M^(1/4)W^(-7/8)<=1`.

The fold-group integrated bound `M^(-1/4)W^(3/8)` is uniformly lower order than the sum of the two main scales. Splitting the concave W power gives terms `M^(-1/7)` and `M^(-1/4)Delta^(3/8)`. Relative to their respective main scales they vanish as `M^(2/35)` and `Delta^(1/8)`. This checks all relative rates, including Delta much smaller than the fold layer, comparable to the placement scale, and much larger than it.

The coarse order lower certificate controls the averaged derivative kernel by `C/(Delta b^5)` at every spatial point. With `b=(M/Delta)^(1/4)`, multiplication by total mass M gives the same b^(-1) scale as source and reaction. A small fixed test amplitude makes the result positive. This supplies the lower bound without assigning mass to root arcs in advance. A fixed regular subset of bins has positive total probability; for fixed N, one positive-length regular subinterval suffices with N-dependent constants.

## Sharp intermediate and simultaneous coarse limits

On compact regular offset sets, the conditional limit is uniform and the local value continuous. Multiplication by each bin's probability Delta/4 yields the stated Riemann-sum density, including factors `2^(6/5)/4` and the local argument `2^(1/5)tau a^(-3/10)`. Nonnegative discarded bins give the liminf. For the upper bound, the omitted regular offsets are dominated by the integrable powers t^(-4/5) and t^(-7/8). Fold-group costs vanish after normalization: the two powers are M^(2/35) and, for bounded tau, O(M^(1/40)). Thus the limit remains valid at tau=0 and under changing bin alignment.

The coarse proof is separate from this finite-tau theorem, as it must be. On a compact regular offset set, `w=Delta/sqrt(a)[1+o(1)]`, `e=M/(2w)`, and the oscillator width b obeys b/w tending to zero. The paired source-minus-reaction term is `2z0(2I-U)`. Each root branch has conditional density `(1+o(1))/w`; the two spatial kernel supports remain disjoint. The maximum derivative kernel multiplied by the arbitrary mass `M=2ew` is at most `2z0 T[1+o(1)]`. This proves the unrestricted sharp conditional lower coefficient without assuming equal allocation by the competitor.

Padding each root arc by `p=sqrt(bw)` gives b much smaller than p and p much smaller than w. The mobility tends to e, both endpoint distances in harmonic units diverge, and the exterior reciprocal response divided by z0 is O(b/p), tending to zero. This gives conditional coefficient `2^(5/4)C0 a^(-7/8)`. Integrating with density 1/4 gives `2^(-3/4)C0 B(1/2,1/8)`. The omitted fold-group normalized cost is O(Delta^(1/8)), while the regular error has the same integrable t^(-7/8) envelope. The simultaneous coarse limit is therefore justified independently of the endpoint behavior of H.

The local large-eta equivalent in H yields the same coefficient, since `-4/5-(3/10)/4=-7/8` and `6/5+(1/5)/4-2=-3/4`. The mean/scalar physical comparison is uniform over observation laws by the accepted theorem and introduces no new restriction on these joint limits.

## Finding

### R3-01 — Minor: the cited equation is not the exact sine coordinate

Location: `sections/06-finite-precision.tex:448–450`.

The text refers to the “exact sine coordinate of” `eq:fold-scaling`. That equation in Section 02 defines the scaling of the generic quartic whole-line model; it does not define the exact sine coordinate. The exact sine substitution is supplied in the proof of `lem:cosine-uniform`. The mathematical argument here uses the correct substitution, so this is a cross-reference/exposition issue.

Remedy: state the substitution explicitly, for example `z=2 sin((s-s_j)/2)`, or refer to the proof of `lem:cosine-uniform` instead of the quartic scaling equation. The ensuing potential and metric statements need no change.

## Verdict

No major issue found. Correct the minor coordinate reference before acceptance. The local attained value, uniform conditional liminf and recovery, fold-crossing controls, exact finite-ratio crossover, and separate simultaneous coarse limit withstand the checks above. No local-profile uniqueness or numerical value of the new crossover has been certified by this review. The requested independent review sequence is being followed; final acceptance requires the coordinator's adjudication of all five reports.
