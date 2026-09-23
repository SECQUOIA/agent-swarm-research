# Stage 4: coordinator investigations

## Closing the multivariate optimized phase-loss bound

This develops the explicitly unresolved equality following equation (10) of `research/multiphase-reservoir-geometry.md`. It is a proposed proof for independent review, not an accepted theorem yet.

Let `p_N = sum_i w_i Normal(N e_i, N I_r)` for finitely many distinct fixed phase points in Euclidean dimension r, with fixed positive weights. Reweight by `exp(t_N dot E - kappa_N |E|^2/2)`. Assume `kappa_N N^(3/2) -> 0` and `kappa_N N^2 -> infinity`. Define a contact set F to be the set of all phase points nearest to some finite center c. Let `W_* = max_F sum_(i in F) w_i`. Then the proposed exact optimized limit is

`lim_N inf_t TV(p_N,q_(N,t)) = 1-W_*`.

The existing upper bound is sound: choose a center c realizing a maximizing contact set and `t_N=kappa_N N c`. With `s_N=1/(1+kappa_N N)` and `alpha_N=kappa_N N^2 s_N`, the transformed component means are `N s_N(e_i+t_N)`, covariance `N s_N I_r`, and weights proportional to `w_i exp(alpha_N[c dot e_i-|e_i|^2/2])`. Weights outside F vanish; on F they converge to the original conditional weights. Standardized component shifts vanish because `kappa_N N^(3/2)->0`, and covariance ratios tend to one. Hence the limiting TV is the missing target mass `1-sum_F w_i`.

For the lower bound, consider any field sequence and any subsequence along which its TV has a limit. Further subsequences suffice.

### 1. Fields bounded away from zero force TV to one

Write `u_N=t_N/|t_N|`, `H_N=max_i u_N dot e_i`, and `eta_N=N^(-1/4)`. Select a phase j attaining H_N. The logarithmic weight ratio of phase i to phase j is

`log(w_i/w_j)+N s_N |t_N|(u_N dot e_i-H_N) - alpha_N(|e_i|^2-|e_j|^2)/2`.

If `|t_N|>=epsilon>0` and `u_N dot e_i <= H_N-eta_N`, this tends uniformly to minus infinity: the negative magnitude is at least order `N^(3/4)`, whereas `alpha_N=o(sqrt N)`. Thus q gives probability tending to one to components with projection at least `H_N-eta_N`. Their scaled means obey

`u_N dot [s_N(e_i+t_N)]-H_N >= s_N|t_N|-(1-s_N)|H_N|-s_N eta_N >= epsilon/2`

for large N. Their projected standard deviations on the energy-density scale are at most `N^(-1/2)`. Consequently q lies with probability tending to one beyond the halfspace `u_N dot (E/N)>H_N+epsilon/4`, while p gives that halfspace vanishing mass. Therefore TV tends to one. The same inequalities cover unbounded field norms.

Since `1-W_*<1`, such sequences cannot improve the claimed optimum.

### 2. Small fields cannot move mass between macroscopic phase locations

It remains to consider `t_N->0`. Then every transformed component mean divided by N tends to its own e_i, and its variance divided by N^2 tends to zero. Pass to a subsequence along which all transformed weights converge to v_i; let I be their nonempty positive support. Choose disjoint fixed small macroscopic neighborhoods of all phase points. The union of neighborhoods indexed outside I has canonical probability tending to `sum_(i notin I) w_i` and q probability tending to zero. Hence

`liminf TV(p_N,q_N) >= 1-sum_(i in I) w_i`.

No control of standardized within-phase shifts is needed for this lower bound. If those shifts cause additional error, the bound only becomes less sharp for that particular field sequence.

### 3. Every surviving support is contained in a finite empty-sphere contact set

Set `z_N=N s_N t_N` and `c_N=z_N/alpha_N`. Fix i0 in I. For i in I, the exact weight-ratio formula implies

`c_N dot (e_i-e_i0) - (|e_i|^2-|e_i0|^2)/2 = O(1/alpha_N)`.

For every j, boundedness above of v_(j,N) and a positive lower bound for v_(i0,N) imply

`c_N dot (e_j-e_i0) - (|e_j|^2-|e_i0|^2)/2 <= O(1/alpha_N)`.

The constants can be chosen uniformly over this finite set. These are approximate solutions, with errors tending to zero, of a fixed finite system of linear equalities and inequalities. This implies exact feasibility, even if c_N diverges. One short justification uses Farkas' lemma after replacing each equality by two inequalities: if `A c <= b` were infeasible, there would exist `y>=0` with `A^T y=0` and `b dot y<0`; multiplying the approximate inequalities by y and letting their errors vanish contradicts this.

Thus a finite c exists with equality for I and the nearest-point inequalities for all phase points. Equivalently all i in I minimize `|e_i-c|^2`; I is contained in its full contact set F. Therefore `sum_I w_i <= W_*`, and the lower bound is at least `1-W_*`.

Applying the argument to nearly minimizing fields (within 1/N of the infimum) proves the optimized limit, without assuming minimizers exist. It also controls unbounded centers c_N and any successive selection among faces. In one dimension with three ordered phase points, the maximal contact sets are the adjacent pairs, recovering the previously proved missing-outer-phase formula.

The empty-sphere geometry and exponential-family closure mechanisms are established. The claimed addition here is the exact optimized full-TV consequence in the specified asymptotic Gaussian model. Literature priority is separate from this proof.

A numerical phase-weight check used the four square corners `(-1,-1),(-1,1),(1,1),(1,-1)` and its center, with weights `(0.10,0.20,0.30,0.15,0.25)`. Exhaustive subset linear-feasibility checks give maximal contact mass 0.75, attained by the top two corners and center, with sphere center `(0,1)`. Numerical minimization of the finite phase-weight TV at alpha 10, 30, and 100 gives `0.24999999794`, `0.25`, and `0.25`, consistent with the predicted limit. This checks only finite phase scores, not the full microscopic Gaussian TV or global numerical optimality; the proof above supplies the lower bound.

## Physical boundary under positive phase moments

The Stage 2 proof can supply a stronger application of the existing finite-capacity boundary calculation, without continuous microscopic densities. These deductions remain subject to the Stage 4 independent review.

For the short-range model in dimension d>2, the cutoff-free window has width eta/L, while a fixed standardized moment uses a displacement of order 1/sqrt(N). Every fixed multiple of the latter lies in the former for all sufficiently large N. The restricted log-partition second derivative is bounded by CN, and its first derivative at coexistence differs from the extensive phase center by O(sqrt(N)). Integrating gives a uniform bound on every fixed exponential moment of the standardized bond count. The already proved Hoeffding/Cauchy–Schwarz transfer supplies every fixed exponential moment of the actual standardized spin energy within each positive contour phase.

Those contour-conditioned energy laws have the same weak limits as the midpoint spin phases. The existing small exponential moment makes assigning a contour-phase configuration to the opposite midpoint phase exponentially unlikely on scale sqrt(N); the positive tunneling remainder also vanishes. The distinct macroscopic centers and positive phase weights therefore identify the limiting conditional laws.

At c_N/N^(3/2)->gamma>0, the secant-calibrated log weight tends on phase windows to b_i z, with b_-=b=-b_+ and b=beta^2 ell/(2 gamma). Global concavity gives the phasewise tangent bound `h_N(E) <= h_N'(e_i)(E-e_i)`, and `sqrt(N) h_N'(e_i)->b_i`. A standardized exponential moment at a coefficient strictly larger than b gives uniform integrability of these weights and of the absolute likelihood difference. Thus weak phase convergence suffices for the limiting phase weights, exponential fluctuation tilts, and full microscopic TV integral. The exceptional mass is controlled by its probability times the maximal bath gain, whose logarithm is `beta^2 ell^2 sqrt(N)/(8 gamma)+o(sqrt(N))`.

For d>2, the exceptional surface cost N^((d-1)/d) dominates sqrt(N), so every fixed gamma>0 is allowed. In d=2 the current proof gives only a small exponential-moment coefficient eta and an exceptional bound C exp(-b_exc sqrt(N)). A sufficiently large fixed gamma satisfies both strict inequalities `beta^2 ell/(2 gamma)<eta` and `beta^2 ell^2/(8 gamma)<b_exc`. This yields a microscopic boundary theorem for sufficiently large gamma, without asserting it for every gamma or determining the microscopic small-gamma morphology.

The mean-field lattice-Gaussian bounds give every fixed standardized exponential moment, and the Gamma kinetic transform also permits every fixed coefficient for sufficiently large N. Hence the same positive-phase boundary argument applies at every fixed gamma. If desired, the pure-spin mean-field case can be covered using Gaussian probability measures with variance zero interpreted as a point mass; density-ratio formulas must not be used at that zero variance.

## Optimizing the physical boundary calibration

The existing optimized Gaussian crossover can also be completed for the physical power-law bath under the positive-phase boundary hypotheses. This is another proposed deduction for Stage 4 review.

Let c_N/N^(3/2)->gamma and assume the finite-tilt moment/exceptional bounds needed for the secant boundary theorem, with Gaussian phase variances v_i (zero may be allowed in measure notation). For each phase let G_i be its centered limiting Gaussian and let G_i^b be the exponentially tilted Gaussian, with mean b_i v_i and unchanged variance. Define

`F(r)= (1/2) sum_i || w_i G_i - r_i G_i^b ||_variation`, with `r_- = r`, `r_+=1-r`.

Then the proposed optimized physical limit is `min{ inf_(0<=r<=1) F(r), w_-, w_+ }`.

**All interior r are attainable.** A total-energy change d sqrt(N) relative to the secant choice produces a finite freely adjustable endpoint score difference, while preserving the limiting local slopes b_i. Hence it realizes every strictly positive limiting pair of phase weights. The same moment and exceptional bounds give the full-TV limit F(r). Continuity permits taking an infimum over the closed interval.

**The two phase-abandonment bounds are attainable.** Center the bath maximum at either phase energy. Since N<<c_N<<N^2, its globally bounded likelihood converges to one in that phase and zero in the other, so the full bath law approaches the corresponding canonical conditional phase law. The full-TV error tends to the missing phase weight. A positive auxiliary decomposition gives the same conclusion by concentration in disjoint macroscopic phase neighborhoods and projection.

**Every better candidate must lie in the finite secant-correction family.** Suppose a subsequence of arbitrary admissible calibrations has TV limit strictly below min(w_-,w_+). With normalized likelihood R_N, define the overlap contribution in phase i by `O_i,N=w_i,N E_i min(R_N,1)`. Since the phasewise losses are nonnegative and sum to TV (with an optional exceptional contribution), `O_i,N >= w_i,N-TV`; hence both overlaps stay positive. Tight phase windows capture all but arbitrarily small canonical phase mass. Points with R_N<epsilon contribute at most epsilon to overlap, and points with R_N>M have canonical mass at most 1/M because E R_N=1. Thus fixed finite window size and fixed epsilon,M allow selection of one feasible energy x_N=e_-+O(sqrt(N)) and y_N=e_++O(sqrt(N)) for which both normalized likelihoods lie in [epsilon,M]. Their log difference a_N is bounded.

Writing D_N=y_N-x_N, the exact endpoint identity is

`c_N log[(calE_N-x_N)/(calE_N-y_N)] = beta_N D_N-a_N`.

It solves to

`calE_N = x_N + D_N/[1-exp(-(beta_N D_N-a_N)/c_N)]`.

Here D_N is order N and c_N is order N^(3/2). A bounded a_N changes this expression from the exact secant calibration for x_N,y_N by O(c_N/D_N)=O(sqrt(N)). Moreover, uniformly for these endpoints,

`calE_sec(x,y)=c_N/beta_N+(x+y)/2+beta_N(y-x)^2/(12c_N)+O((y-x)^4/c_N^3)`.

Moving both endpoints by O(sqrt(N)) changes this expression by O(sqrt(N)). Therefore the original arbitrary total energy differs from the stated phase-center secant calibration by O(sqrt(N)). Pass to a further subsequence on which this scaled correction converges. The finite-correction boundary theorem now gives its limiting error F(r), which is at least inf F. This proves the lower bound: sequences whose error is not below min(w_i) already satisfy it.

Taking nearly minimizing calibrations proves the optimized limit without assuming a finite-N minimizer exists. For equal variances v and balanced weights, convexity of F and reflection symmetry minimize it at r=1/2, giving `min{2 Phi(b sqrt(v)/2)-1,1/2}`. The reflection argument alone treats the balanced case; the microscopic boundary hypotheses are used only where they have actually been proved (all fixed gamma in mean field and d>2; sufficiently large gamma in d=2).

The finite convex minimization is explicitly computable. Put `d_i=b sqrt(v_i)`. The phase-i contribution to its positive-part formula is

`r_i Phi(log(r_i/w_i)/d_i+d_i/2) - w_i Phi(log(r_i/w_i)/d_i-d_i/2)`.

At d_i=0 use `(r_i-w_i)_+`; at r_i=0 the contribution is zero by continuity. Summing these contributions gives F, since the total masses agree. For both d_i positive, its derivative with respect to r=r_- is

`Phi(log(r/w_-)/d_-+d_-/2) - Phi(log((1-r)/w_+)/d_++d_+/2)`.

It is strictly increasing and crosses zero once. The unique minimizer therefore solves equality of the two displayed Gaussian-CDF arguments. In particular, equal positive variances imply r=w_- even for unequal weights, so the optimized physical limit simplifies to `min{2 Phi(b sqrt(v)/2)-1,w_-,w_+}`. This extends the balanced special case in the preceding paragraph; it does not assert that retaining the original weights is optimal for unequal variances.

## Matrix geometry and barrier checks

The author proposed a directly physical version of the broader coexistence-compensation diagnostic. At the boundary, changing the secant-calibrated composite energy by `d sqrt(N)` changes the upper-minus-lower endpoint score by `beta^2 ell d/gamma+o(1)`, while leaving the limiting local slopes unchanged. The coordinator independently checked that choosing `d=beta^2 ell(v_- - v_+)/(8 gamma)` equalizes the two integrated Gaussian phase factors. Original phase probabilities are then restored asymptotically, while full TV tends to `sum_i w_i[2 Phi(b sqrt(v_i)/2)-1]`, with b as above. The maximal bath gain changes only by order one, so the same uniform-integrability and exceptional-mass hypotheses suffice. This does not claim exact finite-size weight restoration. It provides the relevant physical diagnostic without importing unrelated learned-potential parameters into this paper.

For a common isotropic Gaussian phase covariance NI and a matrix reservoir curvature B_N, the integrated phase scores use the effective matrix `M_N=B_N(I+N B_N)^(-1)`, rather than B_N itself. The field is transformed as well. At each finite N, weight restoration means that the effective quadratic score is affine on the phase point set. The author additionally identified a limitation in the old semidefinite-cylinder remark: a quadratic level set with a linear term in the nullspace direction can be a paraboloid. A cylinder description requires the linear coefficient to lie in the matrix range. The manuscript should give the exact affine-score condition and qualify its geometric special cases.

For the physical secant calibration, with `q=beta Delta/c`, the exact endpoint-normalized residual at fraction theta is

`h(e_-+theta Delta)=c[theta q+log(1-theta+theta exp(-q))]`.

At the midpoint this is exactly `c log cosh(q/2)`. Therefore the log-density barrier measured at the specified midpoint relative to either specified endpoint is lowered by that quantity. For c much larger than Delta, its leading term is `beta^2 Delta^2/(8c)`. The elementary two-regime bounds for log cosh show that, when Delta diverges and beta stays positive, vanishing absolute midpoint-barrier error is equivalent to `c >> Delta^2`. This identity says nothing about the location of displaced stationary points or a dynamical transition rate.
