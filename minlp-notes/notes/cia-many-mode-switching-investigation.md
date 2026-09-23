# Many modes and a fixed switching budget

Investigated 2026-09-04 after the exact one-switch result. The dimension-free continuous minimax value is **T/(s+1)**. This follows from established rounding methods plus a simple uniform-control lower bound. It should be retained as a useful structural consequence, not presented as a major independent novelty claim. Independent verification is recorded in `notes/review-cia-many-mode.md`.

## Precise statement

For n≥1, T>0, and integer s≥0, write

\[
 F_{n,s}(T)=\sup_{\alpha}\min_{\omega:\#\mathrm{switches}\le s}
 \max_i\sup_{t\in[0,T]}\left|\int_0^t(\alpha_i-\omega_i)\right|,
\]

where α is any measurable simplex-valued control and ω selects one mode at every time. Then

\[
 F_{n,s}(T)\le T/(s+1),\qquad
 \sup_{n\ge1}F_{n,s}(T)=T/(s+1).
\]

The construction below in fact gives an error strictly smaller than T/(s+1) for every individual finite-mode relaxed input. The exact dimension-free supremum is approached as n tends to infinity.

## Direct upper bound with all cumulative errors preserved

Set m=s+1 and h=T/m. Partition [0,T] into m equal blocks I_j. Define the block averages

\[
 a_{i,j}=h^{-1}\int_{I_j}\alpha_i(t)\,dt,
 \qquad S_{i,k}=\sum_{j=1}^k a_{i,j}.
\]

Each column a_{·,j} lies in the simplex. There is a binary assignment y_{i,j}, with Σ_i y_{i,j}=1 for each j, satisfying simultaneously

\[
 \lfloor S_{i,k}\rfloor\le\sum_{j=1}^k y_{i,j}\le\lceil S_{i,k}\rceil
 \quad\text{for every i,k}. \tag{1}
\]

Here is a direct integral-flow proof. Introduce one supply node for each block j, with integer supply 1. It sends flow to nodes (i,j), one for each mode. Each mode has a chain

\[
 (i,1)\longrightarrow(i,2)\longrightarrow\cdots\longrightarrow(i,m)
 \longrightarrow\text{sink}.
\]

The outgoing chain arc from (i,k) has lower bound floor S_{i,k} and upper bound ceil S_{i,k}. A block-j supply arc to (i,j) has bounds 0 and 1. The sink demands m units. The fractional assignment a_{i,j}, with chain flows S_{i,k}, is feasible. All node supplies and arc bounds are integers, so the standard integrality theorem for network flows supplies an integer feasible flow. Its assignment arcs are y and its chain flows prove (1).

Choose mode i throughout I_j when y_{i,j}=1. There are at most m−1=s switches. At each block endpoint, (1) implies that every cumulative discrepancy has absolute value strictly smaller than h: an integer between floor S and ceil S differs from S by less than 1, including zero difference when S is integral.

Crucially, this endpoint control also handles arbitrary behavior inside the blocks. On a block where mode i is selected, its discrepancy derivative is α_i−1≤0 almost everywhere. Every other component has derivative α_i≥0. Each discrepancy is therefore monotone on that block, so its absolute value is bounded by its values at the two endpoints. This proves error<h everywhere on [0,T]. The proof does not independently restart rounding on each block; the chain constraints preserve all preceding errors.

The flow graph has O(n(s+1)) nodes and arcs. The existence statement requires only the block integrals; an algorithmic implementation presumes these are available or represented exactly. No numerical-oracle complexity claim is made for arbitrary measurable input functions.

## Matching dimension-free lower bound

Take uniform α_i=1/n. Any schedule with at most s switches has at most s+1 constant blocks; one of them has length L≥T/(s+1). If that block ends at time t and selects mode i, the occupation of i through time t is at least L. Thus its negative cumulative discrepancy is at least

\[
 L-t/n\ge T/(s+1)-T/n.
\]

This proves

\[
 F_{n,s}(T)\ge T/(s+1)-T/n.
\]

Letting n tend to infinity gives the matching lower bound on the supremum over n. The exact uniform-control formula in the main CIA result gives a sharper finite-n lower bound whenever s≤n−2:

\[
 F_{n,s}(T)\ge T\max\left\{1/n,
 \frac1{n((n/(n-1))^{s+1}-1)}\right\}.
\]

## Relationship to known results

The upper bound was already within reach of the cited CIA literature. Sager–Zeile, Corollary 6, prove the discrete bound

\[
 F^{\mathrm{grid}}_{n,s}(T)
 \le\frac{2n-3}{2n-2}\left(T/(s+1)+\bar\Delta\right),\qquad n>2.
\]

Their argument uses minimum-up-time rounding. [Published article](https://doi.org/10.1007/s10589-020-00244-5), Corollary 6; local preprint `literature/papers/sager2020-on-mixed-integer-optimal-control/original.pdf`, section 7. Its cited minimum-dwell-time result is verified in [Zeile–Robuschi–Sager](https://doi.org/10.1007/s10107-020-01533-x), Corollary 1 (printed page 669), which explicitly gives the sharp unrestricted CIA endpoint bound (2n−3)/(2n−2) times the grid spacing. Its grid-size condition N≥n−1 concerns attainment of the universal bound, not validity of the upper estimate.

Applying that unrestricted bound directly to the m=s+1 block averages above, followed by the same monotonicity argument inside each block, gives the stronger continuous estimate

\[
 F_{n,s}(T)\le\frac{2n-3}{2n-2}\frac{T}{s+1},\qquad n\ge3.
\]

Thus no passage to an infinitesimal grid is needed. The elementary integral-flow proof was supplied to establish the requested dimension-free bound independently of any unreviewed rounding algorithm.

The flow-rounding principle is classical. [Knuth, *Two-way rounding*](https://arxiv.org/abs/math/9504228), SIAM Journal on Discrete Mathematics 8 (1995), 281–290, uses network flows to control partial sums; related controlled matrix-rounding results also apply. The network above is given explicitly so the precise constraints used here do not depend on a loose analogy with two-way rounding.

## Historical finite-n target

The dimension-free coefficient is settled by the argument above. At this stage, the unresolved target was the sharp finite-n dependence for s≥2. The later sections record its resolution for two and three switches and its general first correction. For fixed s and large n, the exact uniform lower bound has expansion

\[
 \frac{T}{s+1}\left(1-\frac{s+2}{2n}+O(n^{-2})\right),
\]

while the known upper bound gives

\[
 \frac{T}{s+1}\left(1-\frac1{2n}+O(n^{-2})\right).
\]

For s=1, the exact theorem developed here matches the uniform lower expression once n≥5. Whether the uniform input is eventually worst-case for every fixed s, and hence determines the first finite-n correction, is a more substantial question than the dimension-free leading term. No result is claimed for that question here.


A first finite-n refinement is now developed in [the equal-total two-switch theorem](../results/cia-two-switch-equal-masses.md): uniform controls are worst-case among all measurable profiles with equal mode totals. The equal-total theorem has passed independent review. A subsequent [global upper bound](../results/cia-two-switch-global-upper.md) proves F_{n,2}(T)=T/4 for n=4,5,6 and the sharp first correction F_{n,2}(T)=T/3−2T/(3n)+O(T/n²) for arbitrary mode totals. At that intermediate stage, exact finite-n values at n≥7 remained open; the later exact two-switch theorem closes that gap.


## Computational searches for two-switch counterexamples

`code/cia_tv_conjecture/two_switch_search.py` implements a floating-point threshold-feasibility oracle in the regime where all mode totals are at most the tested error E and the two largest mode totals sum to less than T−2E. In this regime positive discrepancies are automatic and a schedule using only two distinct modes is impossible. Three distinct modes p,q,r are feasible exactly when R_p(E)+A_q(T−m_r−E)≥T−m_r−2E. The script searches temporal profiles for which every such inequality fails.

A full eight-mode, four-interval differential-evolution search made 51,177 objective evaluations; four additional six-interval searches with two internally identical groups (group sizes 1,2,3,4) made 21,783, 19,515, 21,783, and 21,783 evaluations. No input exceeding the uniform threshold was found. The best candidates were uniform inputs with slack numerically zero. These negative search outcomes provide no proof of uniform worst-case behavior. Search penalties exclude regimes not covered by this oracle; the global theorems above do not rely on these computations.

Exact-rational certificates separately checked 792 nonuniform equal-total profiles, 12 sharp uniform profiles, and 1,440 arbitrary-total profiles against the proved constructive bounds. The latter checks exercised all four heavy-mode branches as well as both branches of the final global construction. The proof reviews remain the primary mathematical verification.


## Exact two-switch resolution

The full unrestricted-total two-switch problem is now resolved for every n≥4 in [the exact two-switch theorem](../results/cia-exact-two-switch-worst-case.md):

F_{n,2}(T)=T max{1/4,(n−1)³/[n(3n²−3n+1)]}.

The proof establishes a general three-distinct-mode reach theorem and the exact one-sided discrepancy minimax. The maximizing-pair exclusion identity, first identified through independent finite event-order LP investigations, permits a fully analytic proof for every n≥4. Computational certificates are not used in the final argument. Root, `audit_rank_one`, and `review_fbbt` independently checked the completed proof. An exact-rational constructive check passed 480 arbitrary-total negative-reach cases, 480 full-error cases, and 12 sharp lower-bound constructions.

The boundary n=7 is therefore settled at T/4, and the uniform input is exactly worst-case at every n≥8. The next structural target is four or more distinct activation blocks, and then three or more allowed switches. The sufficient all-positive-error condition supplied by small mode totals must be kept separate from the one-sided reach problem.

## Three-switch progress and arbitrary block counts

The [three-switch heavy-mode theorem](../results/cia-three-switch-heavy-mode.md) now proves error at most T/5 whenever any mode has total mass greater than T/5. Its proof separates masses at thresholds 2T/5 and 3T/5 and uses a deadline order for one double-length block and three unit blocks. Independent exact-rational checks covered 1,859 profiles, including flat cumulative allocation segments; an independent reviewer also checked 873 heavy-mode profiles.

An elementary all-light greedy construction gives k distinct blocks reaching kE(n−k+1)/(n−k) when every terminal mass is at most E. Together with the heavy-mode theorem this already settles three-switch values through n=8. A more effective [mode-completion construction](../results/cia-three-switch-global-upper.md) avoids a largest-mass final mode by distributing its relaxed rate equally among the remaining modes. It independently settles n=5,...,11 and proves the sharp first asymptotic correction −5T/(8n). This analytic global upper remains useful even though a stronger exact result is now available from the independently verified four-block reach certificates.

The [exact three-switch formula](../results/cia-exact-three-switch-worst-case.md) combines that heavy-mode theorem with the [general four-block reach theorem](../results/cia-general-four-block-reach.md). Its reach dependency has an exact computer-assisted proof, with 179 finite rational cases and ten symbolic certificate families. The formula is T max{1/5,1/[n((n/(n−1))^4−1)]}. Final transfer-review status is maintained in the result file.

The same mode-completion idea also gives an [analytic bound for every k<n](../results/cia-arbitrary-block-one-sided-bound.md):

C_{n,k}=[n(n−1)+(n−k)(n−k−1)]/[nk(2n−k−1)].

This controls arbitrary-profile one-sided discrepancy and full discrepancy for every profile with equal terminal masses. For each fixed k it matches the first uniform-control correction, 1/k−(k+1)/(2kn), with an explicit gap of order 1/n². The construction was checked on 330 arbitrary and 66 equal-total exact-rational inputs, covering every k<n through n=12. Its independent proof-review status is maintained in the result file. No arbitrary-total two-sided formula for all k is claimed.

## A possible aggregate route beyond four blocks

The following reduction is algebraic; the required higher-order weighted inequality remains unproved. Let M^h be the maximum reach of h distinct modes, M_i^h the maximum such reach avoiding i, and M_{ij}^h the maximum avoiding i,j, with a common positive error threshold E. Under a contradiction assumption that no sequence of k distinct modes reaches a chosen horizon, all roots of orders below k are uncapped.

Monotonicity and endpoint inequalities give

(n−2)M_i^{k−1} ≥ nE + M_i^{k−2} + Σ_{j≠i}M_{ij}^{k−2} − M^{k−1}.

Choose a maximizing (k−1)-mode set S. Then M_i^{k−1}=M^{k−1} outside S. Consequently

Σ_iM_i^{k−1} ≥ [n−k+1−(k−1)/(n−2)]M^{k−1}
 +[(k−1)nE+H_S^{k−2}]/(n−2),

where H_S^{k−2}=Σ_{i∈S}[M_i^{k−2}+Σ_{j≠i}M_{ij}^{k−2}]. The coefficient of the global reach is nonnegative whenever n≥k+1.

Writing B_h=nE[(n/(n−1))^h−1], a sufficient next-step inequality is

H_S^{k−2} ≥ (k−1)nB_{k−2}.

Together with M^{k−1}≥B_{k−1}, it implies Σ_iM_i^{k−1}≥nB_{k−1}, and appending an unused final mode gives the desired k-block reach contradiction. The weighted inequality is proved here for the layers needed by k=3 and k=4. The first unresolved layer in this route is a weighted three-block inequality for four-element sets S, needed for k=5.

This reduction does not establish the higher-order inequality and does not settle the full two-sided problem with four or more switches. The required general heavy-mode argument is now proved below; only the higher-order one-sided inequality remains unproved.


## Final analytic reduction and closure

The [universal heavy-mode theorem](../results/cia-universal-heavy-mode-rounding.md) now applies to every switch budget. Its integral rounding and first-repeat prefix reordering proof is analytic and independently reviewed. It gives the exact identity F_{n,k−1}(T)=max{T/(k+1),G^-_{n,k}(T)} for 1≤k<n, where the one-sided minimax allows repeated modes.

Combining this with the explicit arbitrary-block coefficient gives the [full arbitrary-profile global bound](../results/cia-arbitrary-switch-global-bound.md), an exact plateau for k+1≤n≤k(k+1)/2, and the sharp first finite-mode correction for every fixed switch budget. These conclusions no longer require equal mode totals. Both dependencies and the final transfer have independent reviews.

The user requested that current work be finalized and stopped. The higher-order aggregate inequality above and the largest-mode adjacent-repeat strengthening are retained as explicitly unproved questions. No further investigation is active in this lane.
