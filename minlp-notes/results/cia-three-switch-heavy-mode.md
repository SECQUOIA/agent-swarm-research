# Three-switch CIA bound when a mode has large total mass

Status: developed 2026-09-04 and [independently reviewed](../notes/review-cia-three-switch-heavy.md). This lemma concerns the full, two-sided cumulative discrepancy. It does not depend on the separately proved four-distinct-mode reach theorem. The later [universal heavy-mode theorem](cia-universal-heavy-mode-rounding.md) gives a shorter argument for every switch budget.

Let α:[0,T]→Δ_n be measurable, A_i(t)=∫_0^t α_i(u)du, and m_i=A_i(T). For an integer control ω, write W_i(t)=∫_0^t ω_i(u)du. The error is max_i sup_t |A_i(t)−W_i(t)|.

**Theorem.** Suppose n≥4, E>0, T≤5E, and at least one m_i>E. Then a control with at most three switches has error at most E.

The condition on a mode total is essential for large n: the exact uniform lower bound can exceed T/5. If a four-distinct-mode one-sided reach bound at the uniform threshold is established for n≥5, this theorem would provide the remaining heavy-mode step in an exact three-switch worst-case formula. No such prefix bound is assumed here.

## Reduction and discrepancy checks

Extend α from T to 5E, if necessary, by assigning the added time to any one mode. A mode whose original mass exceeds E still has that property after extension. A valid four-block schedule on the extended horizon restricts to a schedule with at most four blocks on the original horizon, preserving its error bound. Scaling time by E reduces the proof to E=1 and T=5.

For a mode selected exactly once, on a block [b,b+ℓ], its positive discrepancy is bounded by max{A_i(b),m_i−ℓ}, and its negative discrepancy is bounded by max{0,ℓ−A_i(b+ℓ)}. This follows from monotonicity of A_i before and after service and monotonicity of t−A_i(t) during service. A light mode means one with total m_i≤1. An unselected light mode automatically satisfies the error bound.

For a heavy mode i, define the latest level-one time

\[
 d_i=\max\{t\in[0,5]:A_i(t)\le1\}.
\]

Continuity gives 1≤d_i<5 and A_i(d_i)=1. Before d_i its allocation is at most 1, and after d_i it is greater than 1. The use of the latest level time handles flat portions without any strict-monotonicity assumption.

## Case 1: a mass is at least 3

Choose q with m_q≥3. The remaining masses sum to at most 2, so at most one other mode is heavy. Choose p to be that mode if it exists, and otherwise choose any mode different from q. Use p on [0,1] and q on [1,5].

For p, positive discrepancy is bounded by max{0,m_p−1}≤1 and negative discrepancy by 1−A_p(1)≤1. For q, positive discrepancy is bounded by A_q(1)≤1, and negative discrepancy by max{0,4−m_q}≤1. Every omitted mode is light. This case uses one switch.

## Case 2: at most one mass exceeds 2, and every mass is below 3

Choose q to be the unique mode of mass greater than 2 if it exists, and otherwise choose any heavy mode. Thus 1<m_q<3 and m_i≤2 for every i≠q.

There are at most four heavy modes, because their masses sum to 5. Select three distinct modes different from q that contain every other heavy mode, filling unused positions with arbitrary light modes. This is possible because n≥4. Give each selected light mode the artificial deadline 5, and each selected heavy mode its deadline d_i. Arrange these three modes in nondecreasing deadline order.

Choose an integer j∈{0,1,2,3} such that

\[
 j\le d_q\le j+2.
\]

For example, j=min{3,max{0,ceil(d_q)−2}} works. Place q on [j,j+2]. Place the other three selected modes, in their deadline order, on the unit slots whose start times are

\[
 0,1,\ldots,j-1,\quad j+2,j+3,\ldots,4.
\]

There are exactly three such slots, and the resulting schedule has four blocks.

We verify that every selected heavy mode starts by its deadline. Number the three modes in deadline order as i_1,i_2,i_3. If a mode is in a slot preceding q, its start time is ℓ−1 for its index ℓ. If its deadline were less than ℓ−1, then all first ℓ modes would be heavy and would each have allocation greater than 1 at time ℓ−1. Their total allocation would exceed ℓ, contradicting total allocation ℓ−1.

For a slot following q, its start time is ℓ+1, and ℓ≥j+1. If its deadline were less than ℓ+1, all first ℓ modes would have allocation greater than 1 there. Also d_q≤j+2≤ℓ+1, so A_q(ℓ+1)≥1. Their combined allocation would exceed ℓ+1, again a contradiction. Selected light modes have deadline 5 and do not cause a violation.

Every unit-block mode therefore has positive discrepancy at most 1: its starting allocation is at most 1 and its final mass minus one is at most 1. Its negative discrepancy is at most its block length, which is 1. For q, A_q(j)≤1, m_q−2<1, and A_q(j+2)≥1, proving both discrepancy bounds. All omitted modes are light.

## Case 3: two masses exceed 2, and every mass is below 3

There can be only two such modes, say q and r. They are the only heavy modes because all remaining masses sum to less than 1. Order them so a=d_q≤b=d_r.

We have b≥2: otherwise both allocations at time 2 would exceed 1. We also have a<3. Indeed, if both deadlines were at least 3, then A_q(3)≤1 and A_r(3)≤1, while the remaining allocations sum to less than 1, contradicting their total 3. Finally b<4, because for either heavy mode i,

\[
 A_i(4)\ge m_i-1>1.
\]

Set τ=max{2,a}. These observations give 2≤τ≤3 and a≤τ≤b. Choose any light mode p, which exists since n≥4, and use the schedule

\[
 p\text{ on }[0,\tau-2],\qquad
 q\text{ on }[\tau-2,\tau],\qquad
 r\text{ on }[\tau,\tau+2],\qquad
 p\text{ on }[\tau+2,5].
\]

Delete any zero-length blocks. Mode q starts by a and ends at or after a. Mode r starts by b and ends at or after 4>b. Both receive length 2, and both final masses are below 3. The one-block discrepancy checks therefore give error at most 1 for q and r.

The two appearances of p have combined duration (τ−2)+(3−τ)=1. Hence W_p(t)≤1 and A_p(t)≤m_p<1 for all t, which bounds both discrepancy signs directly. Every other mode is light and omitted. There are at most four blocks.

The three cases are exhaustive, completing the proof. ∎

## An all-light greedy lemma and exact three-switch values

The heavy-mode theorem combines with the following elementary cumulative allocation argument.

**Lemma.** Suppose all mode totals satisfy m_i≤E. For any integer 1≤k<n, at most k distinct activation blocks can reach

\[
 \min\left\{T,\frac{k(n-k+1)}{n-k}E\right\}
\]

with both signs of cumulative error at most E up to the reached time.

**Proof.** Define t_0=0 and

\[
 t_j=\frac{j(n-j+1)}{n-j}E,\qquad 1\le j\le k.
\]

These times increase. Suppose j−1 distinct modes have been selected, and the current endpoint is t_{j−1}<T. At u=min{T,t_j}, the selected modes have cumulative allocation at most (j−1)E in total. Therefore one of the n−j+1 unused modes has

\[
 A_i(u)\ge\frac{u-(j-1)E}{n-j+1}.
\]

The identity

\[
 (n-j)t_j=(n-j+1)t_{j-1}+(n-2j+2)E
\]

and u≤t_j imply

\[
 \frac{u-(j-1)E}{n-j+1}\ge u-t_{j-1}-E.
\]

Thus activating that unused mode from t_{j−1} to u incurs negative discrepancy at most E. Any positive negative-discrepancy value is largest at the block endpoint, and the negative discrepancy decreases after the block; all earlier selected modes retain their bound. Every positive discrepancy is at most its mode's total mass, hence at most E. Stop if u=T, and otherwise continue. ∎

**Corollary.** For every n=5,6,7,8,

\[
 \boxed{F_{n,3}(T)=T/5.}
\]

The upper bound T/5 also holds for n=4.

**Proof.** Set E=T/5. If some mode mass exceeds E, apply the heavy-mode theorem. Otherwise use the all-light lemma with k=4. For 5≤n≤8,

\[
 \frac{4(n-3)}{n-4}E\ge5E=T.
\]

When n=4, at least one mass is at least T/4>E, so the heavy-mode theorem applies directly.

For n≥5, let the relaxed control take five distinct pure modes successively, each for time T/5, with all additional modes unused. Any integer control with at most three switches uses at most four distinct modes, so it omits one of these five modes. The omitted mode has final discrepancy T/5. This proves the matching lower bound. ∎

The lower witness is the familiar omitted-mode construction from the switching-budget literature; the new work here is the matching arbitrary-profile upper bound. The [subsequent global bound](cia-three-switch-global-upper.md) extends the exact plateau through n=11 and establishes the sharp first asymptotic correction. The [exact three-switch theorem](cia-exact-three-switch-worst-case.md) now also resolves n≥12 using the independently audited four-distinct-mode prefix theorem. That stronger dependency is not needed for the earlier corollary retained above.
