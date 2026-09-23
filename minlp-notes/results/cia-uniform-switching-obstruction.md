# Uniform controls disprove the Sager–Zeile switching-budget conjecture

Status: proofs developed on 2026-09-04 and independently agent-reviewed; see `notes/review-cia.md`. The counterexample is exact and does not depend on optimization software. Novelty is provisional: targeted searches found the conjecture in the original article and Zeile's dissertation, but no subsequent resolution.

## Problem and published claim

Let a relaxed control have n nonnegative components summing to one on [0,T]. An admissible integer control selects exactly one component at each time and changes its selected component at most s times. The CIA error is

\[
 D(\alpha,\omega)=\max_i\sup_{0\le t\le T}\left|\int_0^t(\alpha_i(u)-\omega_i(u))\,du\right|.
\]

For a unit equidistant grid of N intervals, both controls are constant on each interval, T=N, and the supremum is the maximum over grid endpoints. A switch between consecutive intervals counts once; the initial activation does not count.

Sager and Zeile, *On mixed-integer optimal control with constrained total variation of the integer control*, Computational Optimization and Applications 78 (2021), 575–623, Conjecture 1, equation (7.6), assert that the worst-case discrete error equals

\[
 \begin{cases}
 T/(s+2)+\bar\Delta/2,&1\le s\le n-2,\\
 T/(2s+4-n)+\bar\Delta/2,&s>n-2,
 \end{cases}
\]

under 1 ≤ s ≤ N−2 and n>2. The claim is present in both the local preprint and the final published article. [Published article](https://doi.org/10.1007/s10589-020-00244-5); [open final PDF](https://www.econstor.eu/bitstream/10419/288496/1/s10589-020-00244-5.pdf). Local source: `literature/papers/sager2020-on-mixed-integer-optimal-control/original.pdf`, Conjecture 1, preprint p.27. Definition 10 specifies switches between consecutive intervals.

## An exact counterexample

Take n=5, N=T=45, s=1, and a_{i,j}=1/5 for every component and interval. Every schedule with at most one switch consists of one mode p for k intervals and a different mode q for 45−k intervals, with 0≤k≤45. Constant schedules are included by k=0 or k=45. At least three modes are never selected.

For a never-selected mode, the final error is 9. For mode p, the cumulative discrepancy decreases to −4k/5 at the switch and then increases to 9−k. For mode q, it increases to k/5 at the switch and then decreases to k−36 at the final time. Therefore

\[
 D(k)=\max\{9,4k/5,36-k\}.
\]

To verify the simplification, k/5≤9; |9−k|≤max(9,4k/5) for 0≤k≤45; and |k−36|≤max(9,36−k). The two nonconstant displayed terms intersect at k=20, where both equal 16. For k≤20 the last term is at least 16, and for k≥20 the middle term is at least 16. Thus the optimal CIA error is exactly **16**.

The conjectured worst-case value is 45/3+1/2=31/2=15.5. Since this particular relaxed control has minimum error 16, the conjecture is false even when interpreted only as an upper bound.

Repeating the construction on N=45m intervals, with the same five uniform components and one allowed switch, gives exact error 16m, whereas the conjectured value is 15m+1/2. Consequently the discrepancy persists at fixed horizon as the grid is refined: the continuous value is 16T/45, strictly greater than T/3.

## Exact continuous error for uniform controls and few switches

**Theorem.** Let n≥2, 0≤s≤n−2, and α_i(t)=1/n. Set r=n/(n−1). The minimum continuous CIA error with at most s switches is

\[
 E_{n,s}(T)=T\max\left\{\frac1n,\frac1{n(r^{s+1}-1)}\right\}.
\]

**Proof of the lower bound.** A schedule with m≤s+1 constant blocks leaves at least one mode unused, so its error E is at least T/n. Let 0=t_0≤t_1≤⋯≤t_m=T be its block endpoints. The occupation of the mode selected on block j by time t_j is at least t_j−t_{j−1}, even if that mode was also used earlier. Its negative discrepancy bound therefore implies

\[
 (t_j-t_{j-1})-t_j/n\le E,
 \qquad t_j\le r t_{j-1}+rE.
\]

Iteration yields T≤nE(r^m−1)≤nE(r^{s+1}−1), proving the second lower bound.

**Proof of attainment.** Put m=s+1 and

\[
 E_0=\frac{T}{n(r^m-1)},\qquad
 t_j=T\frac{r^j-1}{r^m-1},\quad j=0,\ldots,m.
\]

Use a different mode on each of these m blocks. For a selected mode, discrepancy increases from 0 to t_{j−1}/n before its block; decreases during its block; and increases after its block. At its block endpoint its discrepancy is

\[
 t_j/n-(t_j-t_{j-1})=-E_0.
\]

Its preactivation and final discrepancies are at most T/n, and after activation they never fall below −E_0. An unused mode has discrepancy t/n≤T/n. Thus the constructed schedule has error at most max(T/n,E_0), completing the proof. ∎

The theorem allows repeated modes in the lower bound; distinct modes are a consequence of the construction, not an assumption imposed on competitors.

For s=1 this specializes to

\[
 E_{n,1}(T)=T\max\{1/n,(n-1)^2/[n(2n-1)]\}.
\]

For n≥5, this exceeds T/3. More generally, for every fixed s≥1,

\[
 \lim_{n\to\infty} E_{n,s}(T)=T/(s+1)>T/(s+2).
\]

Thus the published first-branch continuous target is obstructed for every fixed switch budget once enough modes are available. This is a lower bound on the full worst-case CIA error; it does not assert that uniform controls are worst-case.

## Exact discrete error by a scalar recurrence

**Theorem.** On N unit intervals, under the same assumptions n≥2 and 0≤s≤n−2, define for integers K≥N

\[
 b_0(K)=0,\qquad
 b_{j+1}(K)=\left\lfloor\frac{n b_j(K)+K}{n-1}\right\rfloor.
\]

Let K* be the least integer K≥N with b_{s+1}(K)≥N. Then the optimal CIA error for a_{i,j}=1/n is K*/n.

**Proof.** Every grid-endpoint discrepancy is a multiple of 1/n. The unused-mode argument requires K=nE≥N. For any schedule with error≤K/n, the same block-end calculation as above gives t_j≤b_j(K), proving necessity (extra zero-length blocks may be appended to reach s+1 indices).

Conversely, choose t_j=min(N,b_j(K)), stop when N is first reached, and assign a distinct mode to each positive-length block. The reachability condition forces b_1≥1: otherwise all iterates would be zero. Hence K≥n−1, and each recurrence step increases b_j by at least one. The condition defining b_j ensures the discrepancy at each selected mode's block endpoint is at least −K/n. Before that block, after that block, and for all unselected modes, positive discrepancies are at most N/n≤K/n. Discrepancy is monotone on each segment of a mode's trajectory, so all negative discrepancies are controlled by its block endpoint. The schedule uses at most s+1 blocks, proving sufficiency. ∎

The monotone integer predicate supports binary search in K∈[N,N(n−1)]. No MILP or enumeration is needed. Continuous attainment and the recurrence also show

\[
 E_{n,s}(N)\le E^{\mathrm{grid}}_{n,s}(N)< E_{n,s}(N)+(n-1)/n.
\]

For the upper bound, set K=ceil(n E_{n,s}(N))+n−2. For every integer b, the next discrete iterate equals ceil((n b+ceil(n E_{n,s}(N)))/(n−1)), which is at least r b+r E_{n,s}(N). Hence the integer recurrence dominates the continuous recurrence, reaches N in at most s+1 steps, and certifies error at most K/n. The inequality K/n<E_{n,s}(N)+(n−1)/n gives the asserted strict bound.

## Significance and limits

The example concerns switching-limited process operating modes, such as equipment activation, reactor modes, or adsorption cycles. It shows that time spent among many relaxed modes can force an error larger than a bound inferred from a small number of bang-bang blocks. The uniform-control theorem supplies an exact benchmark family and a dimension-dependent obstruction for any proposed universal rounding guarantee.

This is a correction and an explicit family, not yet a complete characterization of worst-case CIA rounding. The uniform family alone does not characterize arbitrary relaxed controls. The final section below resolves the complete continuous one-switch case. The complete continuous [two-switch](cia-exact-two-switch-worst-case.md) and [three-switch](cia-exact-three-switch-worst-case.md) cases are now resolved separately. The [arbitrary-switch theorem](cia-arbitrary-switch-global-bound.md) gives a general exact plateau and sharp first correction; exact higher-budget values beyond that scope and general budgets s≥n−1 remain open.

## Exact worst-case continuous error with one switch

**Theorem (full worst case, one switch).** For every n≥3 and T>0,

\[
 \sup_{\alpha}\min_{\omega:\,\#\mathrm{switches}\le1}D(\alpha,\omega)
 =H_n(T):=T\max\left\{\frac13,\frac{(n-1)^2}{n(2n-1)}\right\}.
\]

The supremum ranges over all measurable simplex-valued relaxed controls. It is attained. For n=3 or 4, three consecutive pure-mode blocks of length T/3 attain it. For n≥5, the uniform relaxed control attains it.

**Proof.** Scaling time reduces to T=1. Write A_i(t)=∫_0^t α_i(u)du and m_i=A_i(1). For distinct modes p,q, choose p up to time τ and q afterward. Monotonicity of each discrepancy before, during, and after activation shows that its exact error is

\[
 \max\left\{\max_{i\notin\{p,q\}}m_i,\quad
 \tau-A_p(\tau),\quad1-m_q-\tau\right\}.
 \tag{1}
\]

Indeed, the omitted modes increase to their totals. The negative discrepancy of p is largest at τ. Its final positive discrepancy m_p−τ is at most 1−m_q−τ. The positive discrepancy of q at τ is at most τ−A_p(τ), and its final negative discrepancy is 1−m_q−τ. This accounts for every extremum.

Set E=H_n(1). In particular 1/3≤E<1/2. If some m_q≥E, there is at most one mode other than q with total strictly greater than E. Select p to include that mode if it exists, and otherwise choose any p≠q. All omitted totals are at most E. Set τ=max(0,1−m_q−E). Then τ≤max(0,1−2E)≤E, and (1) is at most E.

It remains to consider m_i<E for every i. Let q have the largest total and r the second largest. Define

\[
 t_q=1-m_q-E>0,\qquad t_r=1-m_r-E\ge t_q,
 \qquad h_i=1-m_i-2E.
\]

Both times belong to [0,1]. If every schedule p→q, p≠q, switching at t_q, and the schedule q→r switching at t_r had error strictly greater than E, equation (1) would imply

\[
 A_p(t_q)<h_q\quad(p\ne q),\qquad
 A_q(t_q)\le A_q(t_r)<h_r.
\]

Summing all n inequalities and using Σ_i A_i(t_q)=t_q yields

\[
 (2n-1)E<n-1-(n-2)m_q-m_r.
\]

But m_q≥1/n and m_r≥(1−m_q)/(n−1). Since n≥3, these imply

\[
 (n-2)m_q+m_r\ge(n-1)/n,
\]

and consequently

\[
 (2n-1)E<(n-1)^2/n,
\]

contradicting the definition of E. Thus one of the displayed schedules attains error at most E.

For the lower bounds, a relaxed control consisting of three consecutive distinct pure-mode blocks, each of length 1/3, leaves one of those modes unselected by every one-switch schedule and forces error at least 1/3. The uniform-control theorem supplies the lower bound (n−1)^2/[n(2n−1)]. Together with the upper bound, these establish equality and attainment. ∎

**Constructive consequence.** The proof produces a schedule after evaluating the totals and cumulative controls at at most two times. In the case with no total at least E, try the initial mode p≠q maximizing A_p(t_q); if it does not work, the schedule q→r at t_r must work. The number of mode comparisons is O(n), beyond the cost of integrating α.

**Corrected discrete upper bound.** For an arbitrary grid with maximum interval length Δbar, every discretized relaxed control admits a grid-aligned one-switch schedule with error at most

\[
 H_n(T)+\bar\Delta/2.
\]

Apply the continuous theorem to the piecewise-constant relaxed control and move the sole switching time to a closest grid endpoint. Each component's cumulative integer occupation changes by at most the time displacement, which is at most Δbar/2. No additional switch is created. The leading coefficient H_n(T)/T is best possible uniformly over increasingly fine grids, by the continuous lower-bound examples and convergence of these grid bounds.

This resolves the complete continuous one-switch problem, including the precise mode-count transition: T/3 for n=3,4; (n−1)^2 T/[n(2n−1)] for n≥5. It replaces the first branch of the conjecture in the one-switch case while retaining the half-grid rounding term as an upper bound. It does not claim that this finite-grid upper bound is attained for every N.

## Exact three-interval worst case and a smaller counterexample

**Theorem.** On three unit intervals, with n≥3 modes and at most one switch, the full worst-case discrete CIA error is

\[
 \max_a\min_w D(a,w)=2-3/n.
\]

**Proof.** For arbitrary relaxed data let m_i=Σ_{j=1}^3 a_{i,j}. Choose q with the largest total and p with the second largest. Use the schedule (p,q,q). Every other total is at most 1, since the third largest of nonnegative totals summing to 3 is at most 1. The discrepancy on the first interval is at most 1 in every component. At time 2, both selected modes have count 1 and relaxed cumulative values between 0 and 2, so their errors are at most 1; the omitted components have errors at most 1 throughout. At time 3, mode p has total at most 3/2 and count 1, giving error at most 1. Mode q has total m_q∈[3/n,3] and count 2, so its error is at most max(1,2−3/n)=2−3/n. This proves the upper bound.

For uniform relaxed data a_{i,j}=1/n, every schedule with at most one switch uses at most two modes. At least one mode therefore occupies at least two of the three intervals, giving final negative discrepancy at least 2−3/n. This proves the lower bound. ∎

Taking n=7 gives an instance with only 21 identical relaxed entries, all equal to 1/7. Its exact error is 11/7, while the published conjecture gives 3/3+1/2=3/2. The inequality 11/7>3/2 disproves the conjecture at N=3, the smallest grid size its assumptions permit. This small witness complements the five-mode family above, which demonstrates the failure under arbitrarily fine discretization at fixed horizon.
