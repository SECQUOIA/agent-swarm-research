# Independent Stage 3 review 2

## Verdict

**No major issue found.** The normalized scalar theorem, relaxed-envelope formula and unique maximizer, smooth nonmonotone construction, canonical examples, facet argument, exact parameter proofs, radial upper comparison, and uniform radial discrete separation withstand independent analytical review. The two minor findings below concern the explicit regularity of the relaxed admissible class and the rank range of the final example. Neither changes the developed main theorem or its constants.

Read every new Stage 3 section and appendix, the extended scalar appendix and certificate, both relevant scripts, main-file integration, bibliography, source map, and literature ledger. Did not read other reviewers' reports or communicate with them. Did not edit the manuscript. Inspected the existing final build log rather than running a competing build; it has no warnings, undefined citations/references, or overfull/underfull boxes.

## Required minor repairs

### MINOR 1 — Specify local absolute continuity in the relaxed scalar-envelope class

Location: `sections/appendix-barrier-profiles.tex`, Proposition `prop:scalar-envelope`, especially lines 21–28 and the exactness paragraph at the end of its proof.

The main proposition begins with `p in C^2`, which is sufficient for every integration in its upper-bound proof. Its separate exactness claim refers to the “relaxed almost-everywhere constraints” on upsilon without specifying the admissible regularity class. Almost-everywhere differential inequalities alone, even for a continuous function, do not imply their integrated comparison bounds. The intended relaxed class must require upsilon to be locally absolutely continuous. The construction at the end already has this regularity.

Concrete reason: let C be the standard Cantor function on [0,1], extended by zero to the left and one to the right, and choose small h>0 and L>0. The continuous function

`upsilon(y)=1-exp(-y-L C((y-h)/h))`

has upsilon(0)=0, 0<upsilon(y)<1 for y>0, and derivative `upsilon'=1-upsilon` almost everywhere. Nevertheless at y=2h it can greatly exceed `exp(2h)-1`, contradicting the integrated envelope used in the proof. Its singular increase is precisely what local absolute continuity rules out. Starting the Cantor change at h preserves the ordinary near-zero behavior, so this is not merely a zero-endpoint artifact.

Suggested fix: state explicitly that the relaxed admissible functions are locally absolutely continuous on `[0,infinity)`, with upsilon(0)=0, `0<upsilon(y)<=1` for y>0, and the differential inequalities holding almost everywhere. The original C2-derived profile and the proposed piecewise differentiable extremizer both belong to this class. No new argument is needed.

### MINOR 2 — State r>=2 in the vertex-singular example

Location: `sections/04a-coupled-barriers.tex`, Example `ex:vertex-singular`, lines 410–420.

The example uses `n=r-1` and `Gamma_(r-1)`, and its proof requires at least one charged coordinate in addition to the unused coordinate. The condition r>=2 appears in the earlier dense/radial theorem but is not a section-wide hypothesis. At r=1, Gamma_0 is undefined and the displayed n-coordinate construction has no charged coordinate.

Suggested fix: start with “For r>=2, consider the boundary choice ...”. This also removes “earlier”, which currently refers to a choice not introduced earlier in the standalone manuscript. The exact parameter statement itself remains true at r=1, but its separate treatment is unnecessary here.

## Main mathematical checks

### Normalized scalar theorem and necessary multiplier conditions

I re-derived

`v_f'=v_f(1-v_f f'''/(2(f'')^(3/2))) >= v_f(1-v_f)`.

Positive-branch normalization supplies 0<v_f<=1, so the limit is one and the positive tail is integrable. Integrability at the analytic center follows directly from the finite scalar metric integral. Thus the step-profile replacement genuinely works for each fixed f, with constants allowed to depend on f and r. Integrating `x'(t)=exp(-t)v_f(t)^2` proves the finite right endpoint and the correct gap tail.

In metric coordinates, `p_f'=sqrt(f'')` and `p_f''=f'''/(2f'')`, giving exactly the differential conditions used in the appendix. The allocation proof correctly uses compactness and necessary conditions at a global minimizer, without asserting convexity or uniqueness of a general allocation. The zero-coordinate perturbation has a linear objective-norm improvement against a quadratic cost. Its necessary multiplier equation is `y_i p_f'(y_i)=lambda w_i` after absorbing the factor two. The safe-scale comparison then yields a coordinatewise accurate central point at lambda/log(2). No convexity of p_f is needed.

The fixed-profile dyadic extension retains a common shifted activation threshold, actual endpoint accuracy, the correct first-accurate window up to an f-dependent constant, and an initial-progress bound from the fixed-profile prefix theorem. Its constants are appropriately not uniform over all scalar f.

### Relaxed envelope and its unique maximizer

After imposing the minor explicit regularity condition above, the differential comparison produces the exact maximal continuation `min(1,(1+u)e^q-1)`. Integrating its reciprocal gives both branches of C(a), with the correct branch condition and switch derivatives. Both time bounds decrease with u, so substituting the lower attainable u=1-exp(-a) has the right direction.

The small-a limit is 1/log(2), the large-a limit is one, and the exhibited interior value exceeds both. I checked the polynomial lower bound proving C(a)<2, including its positive minimum `(16-5 sqrt(10))/3`. On the first branch B''>0 and B(0)=0 imply aB'-B>0. On the second branch the displayed Taylor estimate proves B''<0 on its entire domain. Consequently aB'-B has exactly one zero after the switch. This establishes uniqueness of the maximizing a for C_SC; it does not imply or require uniqueness for c_star.

The reconstructed extremizing upsilon is locally absolutely continuous and piecewise differentiable, and attains the relaxed inequalities at the chosen a. The text correctly limits exactness to this relaxed problem at the fixed safe scale. It makes no unjustified sharp minimax claim for smooth product barriers.

### Smooth nonmonotone construction

The definitions give `f_A''(X_A(y))=P_A(y)^2` and scalar self-concordance ratio `2|P_A'|/P_A<2`. The finite endpoints, full gradient range, analytic center, and two-sided barrier divergence follow from the given integrals and the limits V_A(y)->+/-1. The parameter bounds A^2/9<nu_A<=(A+1)^2 are valid.

The middle metric interval has logarithmic width tending to a fixed constant. Therefore fixed separated weight translates yield r disjoint windows, each contributing `(1-2 delta)A` length, while the endpoint norm is at most `sqrt(r)[A+log(3A)+Br]`. Taking the limits in the stated order gives sqrt(r). The growing scalar parameter is explicit, avoiding a false contradiction with the normalized theorem or parameter-dependent prior bounds.

### Canonical and spectral cases

The polar-volume calculation gives U up to an additive constant. The entropic conjugate factorizes by Fubini and separability. Its exact scalar gradient parameter is `theta^2 a''(theta)=1-(theta/sinh(theta))^2`, with supremum one. The cited n-self-concordance theorem supplies the property needed in dimension one.

The general spectral Hessian follows from the polynomial trace calculus and uniform approximation of f''; divided differences converge by their integral formula. Positivity of the off-frame coefficients establishes ambient contraction before the common-frame path is exhibited. The rectangular dilation's two copies of f/2 have the correct normalization. The explicit warning against inferring arbitrary spectral-lift self-concordance from scalar self-concordance is necessary and correct.

### Facet collar and optimal-parameter couplings

The full-collar hypothesis is used correctly: one-dimensional convexity bounds partial_1 G even before entering the collar, so sufficiently large first objective forcing guarantees entry. Restricted inverse quadratic forms give the prefix-speed lower bound. Bounded added gradient and Hessian imply the asymptotic unit speed in activated coordinates. The competing path has only a bounded added length because its physical total variation is bounded inside the collar. Choosing the actual terminal objective gap transfers the endpoint lower ratio to the target-set ratio; strict central objective monotonicity justifies “first accurate”.

For the dense barrier I expanded the Sherman–Morrison expression and checked the estimates on A, B, and m. The upper correction is 17m/32, so its gradient parameter stays below r. For the radial barrier I checked the coordinate numerator/denominator polynomial and its monotonicity. Both parameter lower bounds follow from the explicit diagonal approach to the vertex. The parameter-preserving claims concern the full barrier parameter, not merely a coarse sum certificate.

### Uniform radial comparison and finite sequences

Independently re-derived the global Hessian sandwich. The diagonal perturbation costs at most D/4, and the rank-one perturbation at most D/8, giving the stated 11/8. The differentiated stationarity equation gives the stated formula for a'; the bound K<=t then implies a'<=1/4 uniformly. Thus each logarithmic effective-coordinate velocity theta_i lies in [7/10,5/4], while the auxiliary v_i remain ordered. This is sufficient for the prefix bound even though the actual y_i' need not be ordered. The endpoint coefficient is precisely sqrt(11/8)*(25/14).

For the accuracy comparison, q_i lies between (4/5)z_i and z_i; parameter dilation by 5/4 supplies an accurate radial center. The standard-profile inequality H(s+log(a))<=aH(s) gives the stated coordinate bound. Applying the direct norm bound from the proof, rather than replacing it by a needlessly weaker distance bound, yields exactly the printed same-accuracy prefactor.

The radial finite-sequence result is uniform even when lambda and c vary with r. All constants in the sandwich, threshold speed, and prefix argument are uniform. The shifted-threshold potential uses the same dyadic spacing and cutoff as Stage 2. Metric domination controls arbitrary iterates, coordinate monotonicity validates label clipping, actual accuracy forces the terminal label beyond the cutoff, and the initial tube supplies negligible initial progress. No forward-label assumption is hidden in the proof. The explicit transformed-coordinate route is measured in the actual coupled metric using the global upper sandwich.

### Every-c_star-maximizer localization

The new elasticity exclusions use a0=68743/50000, the correct switch at E=2, and the convex minimum of h_k. Their signs exclude every scalar ratio above a0 outside the stated elasticity interval. E=Y(v)/v is increasing, so the two rational Y enclosures imply the full interval for every maximizing v; monotonicity and rational squaring transfer it to x. The displayed stationary equation follows by differentiating P(W)=YA and using P'(v)=A(v)Y'(v). No unsupported stationary-point uniqueness is claimed.

## Verification and literature

Both scripts passed in `/workspace/local-home/miniconda3/envs/qipm/bin/python`, without package installation:

- `verify_scalar_certificate.py`: all exact rational series-tail, logarithm, radical, lower/upper, and every-maximizer localization checks passed.
- `verify_barrier_dependence.py`: all 96 independently solved radial centers passed parameter, Hessian, speed, and finite-difference checks; three central-arc checks passed. The largest tangent discrepancy was about 1.23e-9. Its independent scalar-envelope root calculation gave a=0.6501143834529713 and C_SC=1.831856422983876.

These numerical checks support rather than replace the analytical derivations above. The relaxed-envelope exactness and uniqueness are proved analytically; the c_star localization uses exact arithmetic.

Consulted the local Chewi primary text, including Theorem 2 and Section 4, and Castro–Cuesta Section 4.1. These support the specific canonical-barrier and diagonal-regularization attributions. Independently opened [the primary Lévy–Valeau–Akhavan–Rebeschini v3 text](https://arxiv.org/html/2510.24187v3), whose Section 6.1 gives the cube log-partition and gradient formulas and whose metadata agree with the bibliography. The manuscript accurately treats those formulas as prior specializations. The source-map Stage 3 developments are represented, and the new radial uniform upper bound is proved rather than inferred merely from metric comparability. I found no unsupported broad novelty claim in these stage-specific sections.
