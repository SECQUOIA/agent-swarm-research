# A finite reservoir can remove coexistence that field tuning cannot restore

Date: 2026-09-06. Status: independently reviewed exact Gaussian phase-mixture results. The optimized total-variation size thresholds remain novelty candidates after targeted open-literature review. The Gaussian reservoir, supporting-paraboloid geometry and exponential-family face limits are established. The candidate contribution is the precise distribution-level obstruction and its size scaling.

## Why the two-phase result does not automatically extend

Two separated canonical energy peaks can retain their relative weights after a finite reservoir's temperature is adjusted. Three energy peaks generally cannot: a temperature change supplies a linear bias in energy, while reservoir curvature produces a quadratic bias. An exact invariant of three phase probabilities makes that obstruction measurable.

This matters for deliberately designed coexistence, competing crystal polymorphs, and multicomponent finite systems. It does not assert that a generic single-component system has three phases coexisting over a finite temperature interval. The reference coexistence point and any interaction parameters needed to produce it are fixed; the adjustable controls below are explicitly specified.

## An exact three-phase theorem

Use dimensionless energy units and consider

\[
p_N(E)=w_-\varphi_N(E+N)+w_0\varphi_N(E)+w_+\varphi_N(E-N),
\quad w_i>0,\quad \sum_iw_i=1,
\]

where `varphi_N` is a centered Gaussian density of **variance** `N`. The three component means are `-N,0,N`, and their separation relative to the standard deviation diverges. Couple to a Gaussian reservoir:

\[
q_{N,t}(E)\propto p_N(E)\exp\{tE-\tfrac12\kappa_NE^2\},
\qquad \kappa_N\ge0.
\tag{1}
\]

Here `t` is freely tunable, representing the bath's inverse-temperature offset. For an ordinary thermal bath locally, `kappa=beta^2/c_B`, where `c_B=C_B/k_B`.

Complete the square. With

\[
\alpha_N=\frac{\kappa_NN^2}{1+\kappa_NN},\qquad
z_N=\frac{tN}{1+\kappa_NN},
\]

the transformed component variance is `N/(1+kappa_N N)`, their means are
`(N e_i+tN)/(1+kappa_N N)` for `e_i=-1,0,1`, and their weights are

\[
v_i=\frac{w_i\exp(z_Ne_i-\alpha_Ne_i^2/2)}
{\sum_jw_j\exp(z_Ne_j-\alpha_Ne_j^2/2)}.
\tag{2}
\]

The following ratio is **independent of the temperature adjustment**:

\[
\boxed{\frac{v_+v_-}{v_0^2}
=\frac{w_+w_-}{w_0^2}e^{-\alpha_N}.}
\tag{3}
\]

**Theorem.** There exists a sequence `t_N` such that
`TV(p_N,q_{N,t_N})->0` if and only if `kappa_N N^2->0`.

**Necessity.** Total-variation convergence of separated Gaussian mixtures forces the three nonvanishing target components to be matched in weight, width and center. A transformed component has standard deviation no larger than `sqrt(N)` and cannot cover two macroscopically separated target windows. The three ordered components must therefore match in order, and `v_i->w_i`. Equation (3) forces `alpha_N->0`. Since
`alpha_N=N (kappa_N N)/(1+kappa_N N)`, this is equivalent to `kappa_N N^2->0`.

**Sufficiency.** Take `t_N=0`. The condition makes all log weight changes tend to zero, makes the variance ratio tend to one, and makes each standardized mean shift `O(kappa_N N^(3/2))` tend to zero. Componentwise Gaussian convergence implies mixture total-variation convergence.

Thus the optimally tuned three-phase model needs `c_B>>N^2`, whereas the optimally tuned two-phase model needs only `c_B>>N^(3/2)`. The stronger requirement is caused by phase probabilities, not local thermal fluctuations.

## A regime where individual phase shapes are accurate but coexistence is lost

Assume

\[
\kappa_NN^{3/2}\to0,\qquad \kappa_NN^2\to\infty.
\tag{4}
\]

For adjustments `t_N=O(kappa_N N)`, within-phase widths and standardized mean shifts vanish. Nonetheless (3) tends to zero, so the three phase weights cannot all remain positive in the limit. In the equal-weight case,

\[
\boxed{\lim_{N\to\infty}\inf_t\operatorname{TV}(p_N,q_{N,t})=\tfrac13.}
\tag{5}
\]

To attain the upper side, choose `z_N=alpha_N/2`, or exactly `t_N=kappa_N N/2`. Then the zero and positive phases have equal exponential weights, while the negative phase has relative weight `exp(-alpha_N)`. The limiting law preserves the shapes of two adjacent phases with weights one half each, losing the third. Its distance from the equal three-phase reference tends to one third.

For the lower side, equation (3) implies that at least one transformed component weight tends to zero along every convergent subsequence. No two Gaussian components of standard deviation at most `sqrt(N)` can cover all three target windows with nonvanishing mass. Hence at least one target phase window, of limiting probability one third, is missed. This argument must be stated using expanding windows `|E-Ne_i|<=L_N sqrt(N)` with `L_N->infinity`, `L_N/sqrt(N)->0`, or a fixed-window limit followed by `L->infinity`. Arbitrary temperature sequences that move the remaining components away from target windows cannot improve the bound.

For unequal fixed weights, the same reasoning gives

\[
\lim\inf_t\operatorname{TV}(p_N,q_{N,t})
=\min(w_-,w_+).
\tag{6}
\]

The central and either outer phase can be retained together; both outer phases cannot survive without the center, because their geometric-mean weight is exponentially smaller than the center weight. A subleading change of `z_N` matches any desired conditional weights on the chosen adjacent pair; retaining the reference weights renormalized on that pair attains the missing outer-phase mass.

The independent reviewer confirmed (5)–(6), including arbitrary temperature sequences. Uniformly for `|t|<1/4`, one outer component weight is at most a constant times `exp(-alpha_N/2)`, and other components have exponentially small overlap with that outer target window. For `|t|>=1/4`, the outward extreme component dominates and moves beyond all target phase windows, giving TV tending to one. See the [full review](verification/multiphase-reservoir-review.md).

## Multivariate phase probabilities and reservoir geometry

Let the exchanged quantities form a vector `E in R^d`. To isolate the geometry, use common isotropic phase covariance:

\[
p_N(E)=\sum_{i=1}^k w_i\mathcal N(Ne_i,NI_d)(E),
\qquad e_i\ne e_j,
\]

and the same isotropic quadratic reservoir `exp(t dot E-kappa_N |E|^2/2)`. Completing squares gives

\[
v_i\propto w_i\exp(z\cdot e_i-\alpha|e_i|^2/2),
\quad z=\frac{Nt}{1+\kappa_NN},\quad
\alpha=\frac{\kappa_NN^2}{1+\kappa_NN}.
\tag{7}
\]

For any affine dependency `a_i` satisfying `sum_i a_i=0` and `sum_i a_i e_i=0`,

\[
\boxed{\sum_i a_i\log(v_i/w_i)
=-\frac\alpha2\sum_i a_i|e_i|^2.}
\tag{8}
\]

This family of invariants removes **all** adjustable conjugate fields. At nonvanishing `alpha`, exact phase-weight restoration `v_i=w_i` is possible if and only if there are `c in R^d` and a scalar `b` with

\[
|e_i|^2=2c\cdot e_i+b\quad\text{for all }i.
\tag{9}
\]

Equivalently, the distinct phase-density points lie on one sphere centered at `c`. Choosing `z=alpha c` then restores all phase weights exactly. Every affinely independent set of at most `d+1` points admits such a sphere; larger sets generally do not. Cospherical larger sets are an exception, so the number of phases alone is not the complete criterion.

For common covariance NI and symmetric positive-semidefinite curvature matrix B_N, Gaussian integration gives the effective metric M_N=B_N(I+NB_N)^(-1) and field z_N=N(I+NB_N)^(-1)t_N. The weight scores use z_N·e_i−N² e_i^T M_N e_i/2; even with isotropic phase covariance the effective metric, rather than raw B_N, must be retained. A positive-definite level set is an ellipsoid when nonempty and nondegenerate. In the semidefinite case a linear coefficient in the metric range gives an elliptic cylinder, a degenerate affine subspace, an empty set, or (for zero metric) the whole space as appropriate. A nonzero linear component in its nullspace can instead produce a paraboloid; for zero metric a nonzero linear term gives an affine hyperplane. The earlier unrestricted cylinder statement was too broad. Unequal phase covariances add phase-dependent terms and are not covered by (8). The precise statement is in the [paper's Gaussian appendix](../paper-finite-reservoirs/sections/gaussian-geometry.tex), label eq:anisotropic-effective-metric.

### Exact classification of full-distribution convergence

For at least two distinct fixed phase points, the preceding observations give a dichotomy in this isotropic common-covariance model:

\[
\exists t_N:\operatorname{TV}(p_N,q_{N,t_N})\to0
\quad\Longleftrightarrow\quad
\begin{cases}
\kappa_NN^{3/2}\to0,&\{e_i\}\text{ cospherical},\\
\kappa_NN^2\to0,&\{e_i\}\text{ not cospherical}.
\end{cases}
\tag{9a}
\]

For the cospherical case, choose `t_N=kappa_N N c`. Equation (9) fixes all weights exactly; component width ratios tend to one and standardized mean shifts are `kappa_N N^(3/2)(c-e_i)/(1+kappa_N N)`. Conversely, full-distribution matching forces width ratios to one and pairwise standardized mean shifts to zero. For any two distinct phase points their shift difference is proportional to `kappa_N N^(3/2)(e_i-e_j)`, giving necessity.

For the noncospherical case, linear algebra guarantees an affine dependency with `sum a_i |e_i|^2 != 0`. Full-distribution matching forces all phase-weight ratios to converge to their targets, so (8) forces `alpha_N->0`, equivalent to `kappa_N N^2->0`. Taking `t_N=0` then proves sufficiency, including the component shapes. The independent reviewer supplied a complete exclusion of phase permutations: a homothety mapping a finite set onto itself must preserve its diameter, hence have scale one, and preserve its centroid, hence have zero translation. Distinct points then match themselves.

The single-phase case is different: its mean can be aligned by tuning `t`, and the necessary scale is only `kappa_N N->0` to match its width. Thus the exact model has three distinct bath-size requirements: `N` for one phase, `N^(3/2)` for multiple cospherical phase points, and `N^2` for a noncospherical phase set. These statements concern total variation of complete distributions, not local-observable thermodynamic limits.

## Candidate phase selection picture

In regime (4), bounded choices `z/alpha=c` select the points minimizing `|e_i-c|^2`. The surviving phase sets are contact sets of empty spheres centered at `c`, hence faces of the Delaunay construction for the phase points. This is elementary paraboloid lifting geometry; the geometry itself is known.

For any such contact set `F`, the choice `t=kappa_N N c` leaves within-phase shapes asymptotically unchanged and gives limiting phase weights `w_i/sum_F w_j` on `F`, with zero elsewhere. Therefore

\[
\limsup_N\inf_t\operatorname{TV}(p_N,q_{N,t})
\le 1-\max_F\sum_{i\in F}w_i.
\tag{10}
\]

**Completed during manuscript development:** equality in (10) is proved for arbitrary field sequences in [the paper](../paper-finite-reservoirs/main.pdf), label thm:gaussian-phase-loss. Fields bounded away from zero move surviving components outside the target phase convex hull and force TV to one. For fields tending to zero, the positive limiting phase support satisfies approximate nearest-sphere equations; Farkas' lemma proves an exact finite-center contact set containing that support even when candidate centers diverge. This supplies the matching lower bound. The proof completed the five-reviewer Stage 4 cycle; see [the stage record](../paper-finite-reservoirs/WORKFLOW.md). The geometry itself remains established prior art.

## Physical and novelty limits

These are probability laws for entire finite-system states represented by phase peaks. They are not a statement about simultaneous spatial phase fractions in a sealed vessel. A spatially phase-separated configuration has an interfacial contribution, absent from the exact Gaussian mixture; a physical theorem needs the valley controls being developed separately.

The emerging literature on **designed super-Gibbs coexistence** is close. Thewes and Sollich (2025), *Ensemble inequivalence in the design of mixtures with super-Gibbs phase coexistence*, studies spatial phase selection by interfacial costs; its mechanism differs from the finite-reservoir probability reweighting considered here. Costeniuc, Ellis, Touchette and Turkington already characterize Gaussian ensembles by supporting parabolas/paraboloids. Edelsbrunner–Seidel gives the established Delaunay lifting geometry, and Csiszar–Matus analyzes exponential-family variation closures. These are substantive predecessors. The precise finite-N optimized-TV classification was not found in the checked sources; this is provisional evidence, not proof of novelty. See the [prior-art audit](verification/multiphase-reservoir-prior-art.md).

Deterministic quadrature in `verification/check_multiphase_reservoir.py` confirms the phase-loss limits. At `N=10^6`, `kappa=N^(-7/4)`, retaining the zero and positive phases gives TV `0.3333333333333` for equal weights and `0.1000000000000` for weights `(0.1,0.6,0.3)`. These are exact-mixture checks, not simulations of a molecular fluid.

Current continuation: the [LaTeX paper](../paper-finite-reservoirs/README.md) includes this classification, the completed optimum, and verified physical nonquadratic reservoir results. Unequal-covariance classifications are not asserted.
