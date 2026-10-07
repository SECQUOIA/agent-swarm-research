# Consistency and scalar covering audit

## Scope and conclusion

I read `AGENTS.md`, `BRIEF.md`, both consistency and covering notes in full, and the definitions and relevant covering/certificate results in `decomposition-certificates.md` and `extension-adaptive.md`. I independently checked the analytical arguments. No experiment was rerun, no CI result was inspected, and no literature discovery or knowledge-base write was performed.

There is no fatal flaw in the separator-consistency theorem chain. Split duality, the one-separator band identity, the tree sandwich, graded exact splits, the bag-error bound, scalar concentration, and the scalar covering construction are sound with the explicit assumptions below. The notes also contain incomplete arguments and several overstated side claims; they must not be copied into a submission.

The coherent contribution is: affine certificates approximate restricted cost shifts; their consistency loss has an exact one-edge band interpretation; trees require one joint split; graded dynamic-programming splits recover margin-sensitive control; scalar concentration converts that control into a covering bound. This supports the constructive certificate paper without making its scalar ideal-relaxation theorem into a general certificate-size theorem.

## Source-claim inventory and inclusion decisions

Here C denotes `research-20260929/theory-consistency/consistency-relaxations.md`, H denotes `research-20260929/theory-decomposition/covering-upper-half.md`, D denotes `decomposition-certificates.md`, and E denotes `extension-adaptive.md`. These references are provenance, not scientific citations. The literature lead supplies external attribution.

| Source | Mathematically substantive claim | Assessment and decision |
|---|---|---|
| C §0 | Bounded splits telescope; edge value functions define ordered bands and nonnegative margins | Correct on product domains with running intersection. Include definitions. |
| C Thm 1.1 | Restricted split duality for weak-star compact convex normalized bag functionals | Correct. Require nonempty bag sets; if consistency is infeasible, the value is +infinity, with no assertion of an attained feasible minimum. Include as credited background. |
| C Thm 1.1 examples | Full separator measures glue; polynomial test classes give sparse moment consistency | Correct with the stated positivity/compactness assumptions. Include measure interpretation only; omit independent SOS development. |
| C Thm 1.1 examples | Quadratic box generators bound truncated moments; linear generators alone can leave second moments unbounded at order one | Correct. Omit from main paper as unrelated hierarchy detail. |
| C Thm 1.1 examples | Every polynomial bag representation on a tree is a polynomial separator split | Correct by leaf elimination; degree is preserved. Omit independent SOS development. |
| C Prop 1.2 | Finite-dimensional continuous split classes attain their exact-bag supremum | Correct, after quotienting the constants. Include if needed for affine exactness; proof below. |
| C Prop 1.3(1) | The infimum of a bag equals that of its convex envelope | Correct. For arbitrary bounded data use the closed convex envelope and infima. Include. |
| C Prop 1.3(2) | Joint closed bag envelopes with class Phi equal the split bound for Phi + Aff | Continuous case correct. Discontinuous source proof is a sketch and its hull operation does not preserve affine dependence on the split. Replace by the complete closed-graph-hull proof below. |
| C Prop 1.3(3), Prop 5.1(1) | Affine splits equal the joint bag-envelope relaxation | Correct consequence. Include. |
| C Prop 1.4 | Other bag relaxations add split-dependent bag errors | Correct inequality, not an additive equality for the optimized gap. Include the stronger graded bag-error theorem instead. |
| C Thm 2.1 | One-edge gap equals twice the distance from the class to its exact-split band | Correct, including clipping and constant balancing. Include. |
| C Cor 2.2(1) | Zero gap iff distance to band is zero; finite-dimensional continuous classes meet the band | Correct; attainment uses finite dimensionality and boundedness of the band. Include only the direct exactness interpretation. |
| C Cor 2.2(2) | Zero-width bands give ordinary uniform approximation error | Correct. Mention briefly, without importing separate approximation-rate papers. |
| C Cor 2.2(3) | Bounds using distances to U and L and maximum band width | Correct: for a split bracket a+b and maximum width W, the oscillation of phi-U (and phi-L) is at most a+b+W. Center by a constant. Omit as redundant. |
| C Cor 2.2(4) | A restricted separator subdomain gives a lower bracket | Correct; the local bracket may be negative unless that subdomain contains a pinch. Omit. |
| C Cor 2.2(5) | A moment-matching pair of separator laws gives the dual band gap | Correct for continuous data by compact duality. Include measure duality, not an additional theorem. |
| C Prop 2.3 | Independent cell pieces give the maximum cell bracket; constants have bracket sup L - inf U | Correct. Cells must form a single-valued partition, or use continuous pieces and closed-cell suprema. Include. |
| C Thm 3.1 | Tree lower maximum and upper sum over one joint exact split | Correct. Include. |
| C Prop 3.2(1) | Every exact split component belongs to the original edge band up to a constant | Correct by summing exact bag inequalities on each side. Include as interpretation if space permits. |
| C Prop 3.2(2) | Sequential selection of band elements preserves the optimum | Statement correct for bounded data; source proof incorrectly invokes an attained pinch. Repair with a minimizing sequence, below. Omit sequential algorithm from main text. |
| C Prop 3.3 | Each original band can contain a constant while the joint constant-class gap is one | Correct explicit multilinear example. Replace in main text by H Prop 4, which already obstructs affine classes with smooth quadratic data. |
| C Prop 3.3 extension | Both constant-class edge distances can be positive while their sum is below the joint gap | Correct for the stated multilinear family. Omit duplicate counterexample. |
| C §3, T1 | The tree sum bound is attained for the separable middle bag; coupling approaches the maximum bound; finite coupling remains strictly above it | Correct analytic arguments, including attainment of the split optimum for strictness. Omit the long approximation example. Numerical attainment counts are illustrations only. |
| C §3 | Bagwise perturbation quantity Q remains only an upper bound | Correct. Omit numerical comparisons. |
| C Cor 3.4 | Reduced-band sequential brackets sum to an upper bound | Correct. Its value functions are global quantities; it is not a local algorithmic oracle. Omit as an alternative route. |
| C Cor 3.4 discussion | Semiconcavity carries through elimination for disjoint incident separator coordinates; quadratic growth need not | Correct with infimum-based definitions. Omit alternative-route details. |
| C Lem 4.1 | Uniform separator semiconcavity passes to side value functions on boxes | Correct because an infimum of concave functions is concave and private domains are independent of the separator. Include in scalar appendix assumptions. |
| C Lem 4.2 | Interior pinches have a common derivative and quadratic affine approximation | Correct. Proof compares arbitrary super- and subgradients. Optional brief interpretation; scalar concentration supplies what the appendix needs. |
| C Lem 4.2 discussion | Affine band elements always exist locally at boundary pinches | False as written: U=L=s^2 on [0,1] is a zero-width band with no affine element on any neighborhood of 0. Delete. Approximation and exact insertion are different claims. |
| C Prop 4.3 | A global C^{1,1} band element with a quantitative constant | Explicitly incomplete. The extension estimate misses quadratic terms and bounded-function localization is absent. Exclude; no result here depends on it. |
| C Prop 5.1(2)--(3) | Affine exactness iff all shifted bags have one common global minimizer; interior slopes equal copy multipliers | Correct given finite-dimensional attainment. Include the exactness interpretation only if useful; the certificate construction already defines the slopes. |
| C Prop 5.1(4) | An affine function fits a one-edge band iff cav L <= vex U | Correct for finite continuous box data by convex separation. Omit as redundant. |
| C Prop 5.2 | Piecewise constants require order epsilon^{-1/2} cells near a nonzero multiplier and quadratically opening pinch | Correct; negative slopes reverse endpoint roles. Omit because D already supplies the certificate-model contrast. |
| C Prop 5.4(a) | Scalar affine-cell bracket is at most ((M_L+M_U)/2) r^2 - min w | Correct chord sandwich. Include only if needed to contrast one edge with a tree. |
| C Prop 5.4(b) | A tangent at an interior pinch bounds any cell by distance squared to that pinch | Correct, but it is not a diameter-squared bound for arbitrary cells. Omit. |
| C Prop 5.4(c) | A C^{1,1} side gives a quadratic affine-cell bracket in any dimension | Correct Taylor argument. Omit unnecessary alternate hypothesis. |
| C Prop 5.4 example | The convex/concave sandwich fails in dimension two, with affine gap 1/2 | Correct; complete proof below. Use only as a scope limitation, never as a proved higher-dimensional covering result. |
| C Cor 5.5 | One-edge affine shell count logarithmic in epsilon under quadratic margin growth; higher dimensions require smoothness near pinch | Correct under its explicit local smoothness and cube-containment assumptions. The latter is implicit and should be made explicit. Omit because regridding gives the paper's actual certificate construction. |
| C Prop 5.5 | Analytic and C^{1,1} band elements give polynomial approximation rates | Correct modulo the cited approximation results and scaling of the box in the Jackson constant. Omit independent p-refinement topic. |
| C Prop 5.6 | A positive-width kinked pinch still costs Omega(1/n) in degree-n polynomials | Correct. In the proof handle n=1 and delta=0 by the divided-difference contradiction before dividing by n-1 or delta. Omit independent p-refinement topic. |
| C §5.4 | Positive-width kink has the same asymptotic Bernstein constant as zero width | Conjecture, not established by the data or heuristic. Exclude. |
| C §5.4 | Curvature-jump bands with 0<c<1 contain no polynomial; upper n^{-2} rate; matching lower rate | Noninsertion and upper rate correct. Matching lower rate only numerical. Exclude lower-rate assertion and omit this tangent. |
| C Cor 5.7 | Polynomial band distance O(n^{-2}) follows from a separate sparse preordering theorem | Correct as a corollary of that prior theorem, not an independent explanation. Omit to avoid duplicating the sparse-SOS manuscript. |
| C Prop 5.8(a)--(b) | Aligned analytic pieces give exponential coefficient rate; dyadic unaligned breakpoint gives root-exponential rate | Correct under analytic extension across each breakpoint. Bernstein ellipse inclusion and coefficient counting check. Omit hp topic. |
| C §5.5 | Algebraic singularities give a geometric-mesh root-exponential rate | Not proved in this source. Exclude. |
| C Prop 5.9 | Incident separator partitions multiply bag subproblems; polynomial blocks grow with degree | Product is an upper bound in general, equality for independent coordinate blocks and full product coverage. Counts of coefficients alone are not runtime. Include this limitation in prose only. |
| C §§6--7 | Adaptive solver rules, open-instance interpretations, numerical rates and improvement factors | Heuristic or illustrative, not certified continuum results. Exclude. A finer-grid evaluation is an estimate, not a certified continuum upper bound. |
| H F1--F2 | Bag margin W_t equals g_t+w_t and dominates each incident separator margin | Correct on product domains with running intersection. Include in graded proof. |
| H Lem 0 | Split gap is exactly the supremum of reduced separator deficits minus global margin | Correct for genuinely single-valued bounded bag functions and splits. Omit because the graded proof is shorter and avoids reduced-message machinery. |
| H Thm 1(a)--(c) | Graded exact splits, discount 1/(2n), sliver-distance and cellwise bounds | Correct for any rooting, branching and separator dimension. Include. |
| H Remark 1.1 | L is itself an exact reversed-root split on a path | Requires the original root to be a path endpoint. False for a path rooted at its middle. Omit. |
| H Thm 1' | Discount 1/(3n+1) controls separator and bag errors together | Correct. Include with bounded errors and exact definition of W_t. |
| H Lem 1' | Leafwise sufficient bound with closed-cell pieces and leaf-dependent errors | Correct pointwise algebra. Do not equate it without further argument to the paper's all-touching certificate model. Omit as a separate certificate theorem. |
| H Prop 1.3 | Every uniformly discounted perturbation bound forces 2c sum w_e <= m | Correct using an attained optimizer and alternating-depth signs. Include optional sharpness remark, with continuum family below. |
| H Prop 1.3 discussion | Two alternating perturbations characterize the largest possible discount | Correct if ratios with zero denominator are omitted (or defined as +infinity) and vacuous zero-objective cases are handled. Omit technical optimization of the discount. |
| H Lem 2 | Scalar slope variation <= 4w(c)/h+4Mh, plus chord-oscillation bound | Correct. Include full proof in scalar appendix. |
| H Lem 2 sharpness | For any prescribed fixed interval I the supremum equals 4W/h+4Mh | Overstated if read this way. Universal constants are sharp, realized on I=[c-h,c+h]; the same supremum need not hold on a larger fixed I. Qualify or omit sharpness. |
| H Thm 3 | Dyadic scalar covering upper bound with (8n+2) logarithmic factor | Correct. Add n>=1, epsilon>0, positive valid M_e,G_e, and nondegenerate intervals. Include a fully proved sharper-constant version if desired. |
| H sharper-rule remark | Constants (4n+2) follow from h=4nr and sharp concentration | Correct; all proof steps are available. Upgrade the sketch to a complete theorem, without experimental claims. |
| H Cor 3.2 | Bracket-driven dyadic refinement coarsens the explicit rule and inherits its count | Correct induction on dyadic levels. Include. |
| H Cor 3.3 | Scalar covering numbers are bounded by a gap-coordinate certificate leaf count | Correct under the stated positive gap weights and S_t subset K_t. Omit because this introduces independent certificate lower-bound assumptions and does not establish a two-sided characterization. |
| H Prop 4 | Original scalar bands contain zero but the joint affine gap equals beta | Correct smooth quadratic example. Include as the main obstruction. |
| H Prop 4 discussion | Reduced value is concave near zero, convex outside; reduced band width can vanish at kappa=2beta | Correct closed forms and qualifications. Omit beyond the main example. |
| H Prop 5 | Touching-only aligned certificates equal fixed-slope leafwise split optimization after intercept normalization | Correct for that explicitly modified certificate convention, not an equality for D's all-touching definition. Keep out of the paper's theorem chain. Normalization proof can be made precise as below. |
| H Prop 5 sufficient condition | Cell refinement plus balanced slopes and discounted leaf errors proves epsilon | Correct for the aligned touching-only model. Slopes are essential to the sufficient condition. Omit independent model variant. |
| H §6 size sketch | Alignment requires at least the product of incident cell counts | False when separators overlap or repeat coordinates. Use common refinements for each distinct coordinate; a product over all incident edges is only an upper bound. Delete this lower assertion. |
| H §6 exact criterion | The single-valued reduced-deficit criterion directly applies to multivalued leafwise boundary data | Not without a boundary-state extension. Keep the sufficient Lem 1' bound only, or label edge states by (cell,value), as below. |
| H §6 | Combining dyadic per-level admissible allocations gives error <=2(epsilon+m) | Correct elementary case analysis. It does not realize those allocations by certificate leaves. Omit allocation tangent. |
| H §§6,9 | Full certificate upper half in reading R1; higher-dimensional affine covering; naive B.4 on trees | Open. No supported theorem may assert any of these. |
| D Lem 1.1, Obs 4.2 | DP nonnegative margin identity and unrestricted exact splitting | Correct; reuse with provenance, not as a novelty claim. Root's model section owns foundational DP/certificate arguments. |
| D Def 1.2, Lems 1.3--1.5 | All-touching certificate validity, chain inequality and unfolding | Definitions distinguish the actual certificate model from scalar ideal split classes. Preserve this distinction. |
| D Thm 2.5; E B.1,B.3--B.6 | Gap-coordinate coverings, pointwise allocations, dimension losses and one-edge upper bound | Relevant background only. The scalar appendix uses near-optimal projections, not a claimed complete characterization of certificate size. Independent allocation proofs belong to their own appendix/companion manuscript. |

## Complete proof record and repairs

### 1. Model facts and exact full splitting

Let X be a finite product of compact intervals, and let a_t be bounded bag functions on a tree satisfying running intersection. Removing edge e partitions the bags into a child side A_e and the rest B_e. The variables exclusive to these two sides are disjoint once the separator s is fixed. Consequently

\[
f^*=\inf_s(U_e(s)+V_e(s)),\qquad
w_e=U_e+V_e-f^*\ge0,\qquad \inf_s w_e(s)=0.
\]

For bounded data, define U_t bottom up by infima. Put

\[
g_t=a_t+\sum_{u\in\mathrm{ch}(t)}U_u-U_t\quad(t\ne r),\qquad
g_r=a_r+\sum_{u\in\mathrm{ch}(r)}U_u-f^*.
\]

Each g_t is nonnegative, each nonroot bag has infimum zero, and the root shifted bag has infimum f*. This follows directly from the recursive definition, without selecting minimizers. Thus the split U is exact even for bounded discontinuous data. If the original data are continuous, compact product fibers also make U,V continuous and all original minima attained.

### 2. Duality and attainment

For nonempty weak-star compact convex M_t consisting of normalized bounded linear functionals on C(X_t), and continuous split classes Phi_e containing constants, the payoff

\[
Q((L_t),\phi)=\sum_tL_t(a_t)+\sum_e\bigl(L_{p(e)}(\phi_e)-L_{c(e)}(\phi_e)\bigr)
\]

is continuous affine in the compact product of bag sets and continuous linear in Phi equipped with its product uniform norm. Minimax gives sup_phi min_L Q = min_L sup_phi Q. The supremum of the linear mismatch is zero exactly when neighboring functionals agree on every separator test; otherwise scaling either sign makes it +infinity. A feasible family has an attained minimum by weak-star compactness. For probability measures the inner bag minimum is the pointwise minimum. Full continuous tests give equal separator marginals, and recursive conditional sampling glues the bag measures on the tree.

For finite-dimensional continuous split spaces and exact bag minima, attainment needs no extra constraint qualification. Quotient out constant edge functions. For a split direction d, define D_t=sum_children d_u-d_t, omitting d_t at the root. We have sum_t D_t(x)=0. Hence sum_t min D_t<=0. Equality forces every D_t constant: for every global x all nonnegative differences D_t(x)-min D_t sum to zero, and any bag point extends to a global box point. Leaf elimination then forces every d_e constant. On a unit sphere of the finite-dimensional quotient, continuity gives sum_t min D_t<=-kappa<0 uniformly. Since

\[
\sum_t\inf(a_t+D_t)\le\sum_t\sup a_t+\sum_t\inf D_t,
\]

the split objective tends to minus infinity with the quotient norm. Its continuity and bounded superlevel sets imply an attained maximum.

### 3. Complete closed-envelope proof, including discontinuous splits

This repairs C Prop 1.3's sketch without taking a nonlinear lower-semicontinuous hull of a parameterized Lagrangian. Fix an arbitrary bounded split phi and write f_t=a_t^phi. Let

\[
K_t=\overline{\operatorname{conv}}\{(z,f_t(z)):z\in X_t\}\subset\mathbb R^{|V_t|+1}.
\]

Each K_t is compact. Its lower fiber boundary h_t(z)=min{v:(z,v) in K_t} is the closed convex envelope of f_t. Indeed h_t is lower semicontinuous and convex, is below f_t, and every lower semicontinuous convex minorant has a closed convex epigraph containing K_t. Also min_Kt(v+b(z))=inf_z(f_t(z)+b(z)) for every affine b, because a linear functional has the same infimum on a set and on its closed convex hull.

Minimize sum_t v_t over (z_t,v_t) in product K_t, enforcing equality of neighboring separator copies. Running intersection makes consistent copies equivalent to one global x; minimizing v_t fiberwise gives min_x sum_t h_t(x_Vt). Apply compact minimax to K and unrestricted affine separator multipliers. It yields

\[
\min_x\sum_t h_t(x_{V_t})
=\sup_{b\in\mathrm{Aff}}\sum_t\inf_{z\in X_t}(a_t^{\phi+b})(z).
\]

Take the supremum over phi to obtain rho(Phi+Aff). Taking Phi to be constants gives the affine-class envelope identity. The individual bag statement follows also because the constant inf f is a convex minorant and h<=f. This proof is complete for bounded discontinuous splits.

### 4. Band identity and cells

For one separator put L=f*-V. For phi define a=sup(phi-U), b=sup(L-phi). Then its gap is a+b. Since inf(U-L)=0, a+b>=0. Shifting phi by (b-a)/2 makes both suprema equal (a+b)/2. Clipping this shifted function into [L,U] produces a band function at uniform distance at most (a+b)/2. Therefore 2 dist(Phi,Band)<=gap(Phi).

Conversely, if psi is in the band then

\[
\sup(\phi-U)+\sup(L-\phi)\le\sup(\phi-\psi)+\sup(\psi-\phi)=\operatorname{osc}(\phi-\psi).
\]

Constants belong to Phi, so minimizing the oscillation is twice the uniform distance. This proves equality. If U,L and phi are continuous, clipping is continuous, so the band can be restricted to continuous functions in that version.

For independent cell pieces, every global bracket bounds each cell bracket below. Conversely choose a near-minimizing piece on each cell, and balance its two suprema by an independent constant shift. The global bracket is at most the largest chosen cell bracket. Taking limits gives gap=max_D g_D. Individual g_D may be negative; the full maximum is nonnegative because inf w=0. With continuous affine pieces, half-open cell conventions and closed-cell suprema agree by density of the cell interiors.

### 5. Tree sandwich and sequential bounded-data repair

For an exact split psi, let m_t=inf a_t^psi, so sum m_t=f*. If r_e=phi_e-psi_e has inf alpha_e and sup beta_e, then

\[
\inf a_t^\phi\ge m_t+\sum_{u\in\mathrm{ch}(t)}\alpha_u-\beta_t.
\]

Summing gives gap(Phi)<=sum_e osc(r_e). Optimizing each component and using constants gives the upper bound 2 inf_{psi exact} sum_e dist(psi_e,Phi_e), and taking psi=U gives its DP corollary. For the lower bound enlarge every class except one to all bounded functions. Exact DP splitting on each side, valid for bounded modified bags, collapses the two sides to U_e,V_e. The one-edge identity then gives gap(Phi)>=2 max_e dist(Phi_e,Band_e).

Every exact component is in its band up to a constant: sum the shifted bag inequalities on each side and translate by the sum of the child-side bag minima.

The sequential construction is also valid without an attained pinch. If L<=psi<=U, choose s_j with w(s_j)->0. Then

\[
0\le U(s_j)-\psi(s_j)\le w(s_j),\qquad
f^*\le V(s_j)+\psi(s_j)\le f^*+w(s_j).
\]

Thus the eliminated leaf has infimum zero and the reduced problem has infimum f*. This replaces the source's unsupported use of equality at a pinch for bounded data.

### 6. Smooth affine obstruction

On [-1,1]^2 take root a_r=2 beta s_1^2, middle a_m=kappa(s_1-s_2)^2-beta s_2^2, and leaf a_l=2 beta s_2^2, with beta>0 and kappa>=2 beta. Then F>=0 and f*=0. The first band has

\[
U_1=\frac{\kappa\beta}{\kappa+\beta}s_1^2,\quad L_1=-2\beta s_1^2,
\]

and the second has U_2=2 beta s_2^2 and

\[
L_2=-\left(\frac{2\beta\kappa}{2\beta+\kappa}-\beta\right)s_2^2\le0.
\]

Both contain zero. For affine splits, remove telescoping constants and write phi_e=lambda_e s_e. The middle shifted bag at (s_1,s_2)=(1,1),(-1,-1) is -beta plus or minus (lambda_2-lambda_1), so its infimum is at most -beta-|lambda_2-lambda_1|. The root and leaf infima are at most zero by evaluation at zero. Therefore rho(Aff)<=-beta. The zero split attains -beta. The affine gap is beta despite zero original-band distances on both edges.

### 7. Graded splits and discounted errors

Let n=N-1>=1, b_t be the number of edges strictly inside sub(t), tau=1/(2n), theta_t=(2b_t+1)tau, and psi_t=U_t-theta_t w_t. Define W_t(z)=inf{F(x)-f*:x_Vt=z}. Product fibers imply W_t=g_t+w_t for nonroots, W_r=g_r, and W_t dominates every incident w.

For phi=psi+r, write epsilon_t=theta_t w_t-r_t. The bag deficit is

\[
D_t=\sup_z\left[\sum_{u\in\mathrm{ch}(t)}\epsilon_u-\epsilon_t-g_t\right]
\]

with no epsilon_t at the root. Sum D_t=gap(phi). On a nonroot bag its inside expression is

\[
\sum_u(-r_u-\tau w_u)+(r_t-\tau w_t)
+\sum_u(\theta_u+\tau)w_u+(1-\theta_t+\tau)w_t-W_t.
\]

All margin coefficients are nonnegative and sum to one because b_t=sum_u(b_u+1). Thus the last three terms are <=0. At the root sum_u(theta_u+tau)=1, giving the same conclusion. Taking separate suprema and summing proves

\[
\operatorname{gap}(\psi+r)\le\sum_e\{\sup(r_e-\tau w_e)+\sup(-r_e-\tau w_e)\}.
\]

Take r=0 to prove exactness. Since tau<=theta_t<=1-tau, the sliver |sigma-psi_t|<=tau w_t lies in the original band. The same oscillation and cell balancing arguments as above give the sliver-distance and worst-cell sum bounds.

For bag errors err_t>=0, take tau'=1/(3n+1), theta'_t=(3b_t+2)tau', and psi'_t=U_t-theta'_t w_t. Add err_t to each deficit and reserve tau'W_t for it. The remaining margin coefficients sum to 1-tau' in every bag, because theta'_t=sum_u(theta'_u+tau')+2tau' and sum_u(theta'_u+tau')=1-tau' at the root. The same inequality proves

\[
f^*-\widetilde\rho(\psi'+r)
\le\sum_e\{\sup(r_e-\tau'w_e)+\sup(-r_e-\tau'w_e)\}
+\sum_t\sup_z(\mathrm{err}_t-\tau'W_t).
\]

This is a sufficient consistency-and-bag-error bound. It counts neither oracle work nor actual certificate leaves.

### 8. Discount necessity and continuous sharpness family

Suppose an arbitrary split psi admits the preceding separator perturbation bound with c w_e for every bounded r. Then all |r_e|<=c w_e preserve exactness. At a global minimizer x*, every exact split's bag achieves its minimum at x*_Vt. Choose r_e=plus or minus c(-1)^{depth(child)}w_e. Both perturbations vanish at x*. In bag t the two perturbations have opposite signed sums of all incident margins. Hence

\[
a_t^\psi(z)-a_t^\psi(x^*_{V_t})\ge c\sum_{e\text{ incident to }t}w_e(z_{S_e}).
\]

Sum over bags at a consistent x to obtain m(x)>=2c sum_e w_e(x_Se).

The finite-grid source attains c=1/(2n). In the continuous box model use a path with root s_1^2, middle costs P(s_j-s_{j+1})^2, and leaf zero, all s_j in [-1,1]. The e-th edge has U_e=0 and V_e=P s_e^2/(P+e-1), by successively minimizing unconstrained quadratics (the minimizers stay between 0 and s_e, so lie in the box). At (s,...,s), m=s^2 and sum w_e=s^2 sum_e P/(P+e-1). Thus any uniform c must be <=1/(2 sum_e P/(P+e-1)), tending to 1/(2n) as P increases. This proves uniform optimality within smooth box instances without claiming exact finite-P attainment.

### 9. Scalar concentration, affine approximation and covering

Let U be M-semiconcave and L M-semiconvex, L<=U. Center quadratics at c and define the convex function

\[
v(s)=L(s)+\frac M2(s-c)^2-U(s)+\frac M2(s-c)^2.
\]

Then v<=M(s-c)^2 and v(c)=-w(c). The total slope variation of the corrected U and L on [c-h/2,c+h/2] is v'(c+h/2-)-v'(c-h/2+). Convex chord-slope bounds to the two outer endpoints c+-h, and v(c-h/2)+v(c+h/2)>=2v(c), give at most 4w(c)/h+4Mh.

For D of radius r, a convex function differs from its chord by at most r times its slope variation divided by two. A proof uses the two supporting-line inequalities at an interior point x: the chord defect is bounded by (x-a)(b-x)/(b-a) times the difference of the endpoint slopes, whose factor is at most (b-a)/4=r/2. Applying this to corrected U and L and adding the centered quadratic gives an affine l with

\[
\operatorname{osc}_D((1-\theta)U+\theta L-l)
\le\frac r2(\Delta_U(D)+\Delta_L(D))+\frac M2r^2.
\]

The sharper version of H Thm 3 is therefore complete, not a remaining sketch. A dyadic cell is interior when its distance to the outer interval boundary is >=4nr. Apply concentration at a minimizer of w in the cell with h=4nr. The cell is inside the inner concentration interval even if this minimizer is an endpoint. Its sliver bracket is bounded by

\[
B(D)=(8n+1/2)Mr^2-\frac{\min_Dw}{2n}.
\]

Near the outer boundary use Lipschitz one-sided slopes to get

\[
B(D)=2Gr+\frac52Mr^2-\frac{\min_Dw}{n}.
\]

Refine while B(D)>epsilon/n. Assume epsilon>0, M,G>0, and interval length ell>0; positive valid constants can always be enlarged from zero. The rules stop uniformly because their upper bounds tend to zero with r. The graded cell sum proves gap<=epsilon.

For an interior split at level j, r_j=ell 2^{-j-1}, the cell meets {w<=eta_j}, where eta_j=(16n^2+n)Mr_j^2-2epsilon>0. Its covering interval length 2sqrt((epsilon+eta_j)/M) is at most sqrt(16n^2+n) times its dyadic cell length. Since sqrt(16n^2+n)<4n+1, each covering interval meets at most 4n+2 closed dyadic cells. There are at most

\[
J=\max\left(0,\left\lceil\log_2\left(\ell\sqrt{\frac{(16n^2+n)M}{8\epsilon}}\right)\right\rceil\right)
\]

levels with eta_j>0. There are at most 2n boundary cells at each interval endpoint and at most

\[
J'=\max(0,\lceil\log_2(\ell/(2\varrho))\rceil),\qquad
\varrho=\min\left(\frac\epsilon{4nG},\sqrt{\frac\epsilon{5nM}}\right)
\]

levels with boundary splitting: for r<=varrho the two positive terms are each <=epsilon/(2n). Every binary split adds exactly one final cell. Hence

\[
|P_e|\le1+(4n+2)J_e\sup_{\eta\ge0}N_\infty(\pi_{S_e}E(\eta),2\sqrt{(\epsilon+\eta)/M_e})+4nJ'_e.
\]

The original H theorem follows with h=8nr, 64n^2+n, and factors 8n+2 and 8n instead. The bracket-driven rule only splits a cell when its bracket exceeds epsilon/n. Since that bracket is <=B(D), induction through the common dyadic tree shows it splits a subset of the explicit rule's cells; its count is no larger.

### 10. Sharpness qualification and dimensional scope

The constants (4,4) in concentration are universally sharp on the short domain I=[c-h,c+h]. Take a convex v flat at -W on |s-c|<=a=h/2-delta and linear outside, with slopes chosen to stay below M(s-c)^2. If W>0, for sufficiently small delta use slope (Mh^2+W)/(h/2+delta), reaching the parabola at h with slope at least 2Mh. If W=0 use the tangent slope 4Ma. Then the inner interval contains both kinks and total slope variation approaches 4W/h+4Mh. This does not prove sharpness on an arbitrary larger fixed I. Indeed for M=0 on [-H,H], H>h, the same convex chord argument using outer endpoints +-H gives a maximum at most 2W/(H-h/2), strictly below 4W/h; flat-then-linear examples approach it.

The two-dimensional band L=max(0,x+y-1), U=min(x,y) on [0,1]^2 has affine bracket 1/2. For the lower bound compare the mean-matching laws supported respectively on (0,0),(1,1) and (1,0),(0,1), each with weights 1/2. Their L and U expectations are 1/2 and 0. For the upper bound use l=(x+y)/2-1/4; both bracket suprema are 1/4. Smooth box data realize this band via child u x+(1-u)y and parent v(1-x-y), with u,v in [0,1]. Thus the scalar affine chord sandwich does not extend by the same argument to dimension two. Scaling the entire family gives an order-h affine bracket on size-h square domains; this alone is not a claim that a fixed instance has an order-h asymptotic mesh error. The manuscript should assert only the verified dimensional obstruction and the scalar scope of its covering theorem.

### 11. Certificate model and boundary-state cautions

The paper's certificate convention checks all intersecting cells, including touching pairs. H Prop 5 instead uses a touching-only convention that omits pairs whose interiors do not meet. Its equality with independent leafwise pieces therefore must not be presented as equality for the actual certificate model.

For that restricted aligned model, maximal-intercept normalization can be justified explicitly. Given arbitrary intercepts, let m_D be the infimum of a bag's shifted leafwise function on its own cell and m=min_D m_D. Increase each intercept by m_D-m: that bag's global infimum stays m while its parent additions increase pointwise, so the total bound cannot decrease. Then increase every intercept by m, a telescoping constant operation, making every cell infimum zero. Process upward. This yields feasible maximal intercepts and proves their optimality for fixed slopes. The slope-dependent sufficient condition follows by evaluating the bound at balanced intercepts before normalization.

For leaf-dependent errors and closed-cell pieces, an exact reduced-deficit identity needs cell labels. Replace each edge state s by (D,s), and define its reduced U by the infimum over child leaves carrying that label. Define c as the edge's infimum and delta=U-phi-c. Tree substitution then gives the exact supremum over compatible choices (x,B_t), where D_t(B_t)=D_t(B_parent), of sum leaf errors + sum labeled deltas - m(x). Compatible leaves exist even on boundaries: approach x by points off the finitely many cell and leaf faces, choose a constant-label subsequence, and use closedness. The simple unlabelled identity should be stated only for genuinely single-valued relaxed bag functions.

Finally, overlap invalidates the sketch's alignment lower bound. If root and two children all share one scalar s and both edges have the same k-cell partition, k root leaves suffice; k^2 are unnecessary. In general take the common refinement of all partitions on each distinct separator coordinate. Only independent coordinate groups force a product.

## Verification record

All source theorem proofs were checked analytically as described above. Files were read with `cat`, `sed`, and targeted `rg` searches. No source experiment, project-wide verification, or CI check was run. All source numerical values and novelty judgments remain outside this audit's mathematical evidence.

The parent subsequently assigned authorship of `sections/consistency.tex` and `appendices/scalar-covering.tex`. These files are complete. The main text uses chi for arbitrary splits, reserving the model's phi for subtree values; U is explicitly identified with that subtree value. It uses pi(t) for parents and n_T=N-1 for the edge count. The appendix upgrades the sharper scalar-rule sketch to a proved bound with factors 4n_T+2 and 4n_T. It also proves the value-function regularity assumptions from C^{1,1} bag data. The main text includes a complete bounded discontinuous closed-envelope argument, rather than the source's incomplete hull argument.

Targeted verification compiled a temporary wrapper containing only `sections/model.tex`, `sections/consistency.tex`, and `appendices/scalar-covering.tex`, using the actual shared `macros.tex`. The command was `pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=/tmp/minlp-consistency-check-iqaizho_ /tmp/minlp-consistency-check-iqaizho_/check.tex`, invoked from `paper-separator-certificates` through a Python subprocess wrapper. Initial passes found one overfull band-definition display, which was split; subsequent passes resolved references. The final targeted pass exited zero with no warnings, undefined references, overfull boxes or underfull boxes. The final output is a 14-page wrapper PDF. This is a module-level manuscript check, not a build of the complete paper.

External citation integration remains with the parent/literature lead: continuous pairwise local consistency and cost shifts (Wald--Globerson), compact minimax (Sion's one-space-compact corollary), and tree measure gluing background (readable Lasserre source). The mathematical statements have complete manuscript proofs and contain no unverified citation keys or novelty claims.
