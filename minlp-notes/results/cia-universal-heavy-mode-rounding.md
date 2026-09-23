# A universal heavy-mode CIA bound by adjacent-repeat rounding

Status: developed 2026-09-04 and [independently reviewed](../notes/review-cia-universal-heavy-mode.md). The central argument is analytic. The earlier exact-flow searches suggested the statement but are not used in its proof.

Let α:[0,T]→Δ_n be measurable, let A_i(t)=∫_0^tα_i(u)du, and let W_i(t)=∫_0^tω_i(u)du for an integer control. The full cumulative error is max_i sup_t |A_i(t)−W_i(t)|.

**Theorem.** Let s≥0 be an integer and E>0. If T≤(s+2)E and some mode has terminal mass A_i(T)>E, then there is an integer control with at most s switches and full cumulative error at most E.

No restriction on n relative to s is needed. The theorem concerns profiles with a heavy mode; it does not by itself settle worst-case profiles whose every terminal mass is at most E.

## An integer-prefix rounding with a repeated mode

First normalize the interval length to one and consider an integer horizon M≥2. Average α over its M unit intervals, and let a_i,j denote those averages. Their column sums are one. Standard integral-flow rounding gives a one-hot word w_1,...,w_M whose occupation counts N_i(k) satisfy

\[
 \lfloor A_i(k)\rfloor\le N_i(k)\le\lceil A_i(k)\rceil
 \qquad(1\le k\le M). \tag{1}
\]

For clarity, the integral network has a supply-one node for each time slot. That node can send its unit to any mode's chain at that time. The chain edge after time k carries cumulative occupation and has lower capacity floor(A_i(k)) and upper capacity ceil(A_i(k)). The final edge enters a common sink. The original fractional allocations give a feasible flow. The bounded network-flow polytope has integral vertices because all capacities and supplies are integral.

If A_h(M)>1 for a mode h, maximize its final chain flow over this polytope. The maximum is at least the original fractional value A_h(M)>1. An integral optimum therefore sends at least two units to h. Thus there exists a rounding satisfying (1) in which some mode occurs at least twice.

At grid endpoints, (1) gives error at most 1. Within a unit interval, the selected mode's error W_i−A_i is nondecreasing, and every unselected mode's error is nonincreasing. Therefore the same error bound holds throughout the original measurable profile, not only for its interval averages.

## Reordering the first repeated-mode prefix

**Lemma.** Any error-one integer word on unit intervals that has a repeated mode can be replaced by another error-one word with at least one equal adjacent pair.

**Proof.** If the word already has an equal adjacent pair, retain it. Otherwise let r be the position of its first repeated mode, denoted q. On the prefix [0,r], q is selected twice, each of the other r−2 selected modes is selected once, and every remaining mode is omitted. The existing error bound at r implies

\[
 1\le A_q(r)\le3,\qquad
 A_i(r)\le2\text{ for every other selected mode},\qquad
 A_i(r)\le1\text{ for every omitted mode}. \tag{2}
\]

We reorder exactly this prefix multiset, keeping q twice and every other selected mode once.

Define d_q=max{t∈[0,r]:A_q(t)≤1}. When A_q(r)=1, this is r. Otherwise continuity gives A_q(d_q)=1. In both cases 1≤d_q≤r, A_q(t)≤1 for t≤d_q, and A_q(t)≥1 for t≥d_q.

Choose an integer j∈{0,...,r−2} with j≤d_q≤j+2; for example

\[
 j=\min\{r-2,\max\{0,\lceil d_q\rceil-2\}\}.
\]

Give q the double-length block [j,j+2]. For every other selected mode i, give it deadline d_i=max{t≤r:A_i(t)≤1} if A_i(r)>1, and artificial deadline r otherwise. Sort the r−2 other selected modes in nondecreasing deadline order, and place them on the unit slots whose start times are

\[
 0,1,\ldots,j-1,\quad j+2,j+3,\ldots,r-1. \tag{3}
\]

Each selected heavy mode starts by its deadline. To verify this, let ℓ be its index among the sorted modes. If its slot precedes q, its start is ℓ−1. A deadline below ℓ−1 would mean that the first ℓ sorted modes each have allocation greater than 1 at time ℓ−1, contradicting total allocation ℓ−1.

If its slot follows q, its start is ℓ+1, with ℓ≥j+1. A deadline below ℓ+1 would mean those first ℓ modes each have allocation greater than 1 there. Since d_q≤j+2≤ℓ+1, q has allocation at least 1 there as well. Their combined allocation would exceed ℓ+1, again a contradiction. Modes with artificial deadline r cannot violate either condition.

A unit-block mode's negative discrepancy is at most its block length 1. Its positive discrepancy before activation is at most 1 by the deadline property; after activation it is at most A_i(r)−1≤1 by (2). For q, its starting allocation is at most 1, its allocation at the end of its length-two block is at least 1, and its terminal allocation minus its service is A_q(r)−2≤1. These facts bound both discrepancy signs by 1 throughout its prefix. Every omitted mode has total prefix allocation at most 1.

The reordered prefix therefore has error at most 1. Its occupation counts at r are exactly the original counts. Keeping the suffix unchanged preserves every later cumulative error. The two q slots are adjacent, proving the lemma. ∎

## Switch count and arbitrary horizons

Combining the integral rounding and the prefix reordering gives a word on M unit intervals with error at most 1 and at least one adjacent equality. It has at most M−2 switches.

For the theorem, extend the relaxed control from T to (s+2)E if necessary by allocating the added time to any one mode. A mode whose original mass exceeds E remains heavy. Scale time by E and apply the construction with M=s+2. It gives at most M−2=s switches and error at most E on the extended horizon. Restricting the schedule to [0,T] preserves both guarantees. ∎

## Exact reduction of the full minimax to its one-sided version

Let G^-_{n,k}(T) be the supremum, over all relaxed profiles, of their minimum one-sided error max_i sup_t(W_i(t)−A_i(t)) among integer controls with at most k activation blocks. Repeated modes are allowed in this definition. Let F_{n,k-1}(T) denote the corresponding full two-sided minimax with at most k−1 switches.

**Corollary.** For every 1≤k<n,

\[
 \boxed{F_{n,k-1}(T)=\max\left\{\frac{T}{k+1},G^-_{n,k}(T)\right\}.}
 \tag{4}
\]

**Proof.** If T=0, both sides vanish. Assume T>0 and put E=max{T/(k+1),G^-_{n,k}(T)}>0. For a given relaxed profile, if some terminal mass exceeds E, the universal heavy-mode theorem gives full error at most E with at most k−1 switches. If every terminal mass is at most E, select a one-sided minimizing schedule with at most k blocks. Its negative discrepancy is at most G^-_{n,k}(T)≤E, and its positive discrepancy is bounded by the terminal mode masses, hence by E.

A one-sided minimum exists for each profile. There are finitely many mode words of length k, and their ordered switch-time simplexes are compact. Zero-length blocks allow shorter schedules to be included. Occupation functions vary continuously in the switch times in the uniform norm, so their maximum one-sided discrepancy is continuous. Thus the preceding minimizing schedule is well-defined. Alternatively, the same upper argument can use E+ε and then let ε decrease to zero.

The reverse inequality F_{n,k-1}(T)≥G^-_{n,k}(T) follows because full error dominates one-sided error for every schedule. Also F_{n,k-1}(T)≥T/(k+1): when n≥k+1, k+1 successive distinct pure modes of duration T/(k+1) force any k-block integer schedule to omit a mode. These two lower bounds complete the proof. ∎

This identity does not assume that uniform controls are worst-case or that a one-sided optimum uses distinct modes. It gives an exact minimax reduction for every allowed block count k<n.

## Consequence for the remaining general switching problem

Let k=s+1 and n≥k+1. Suppose a universal one-sided k-distinct-mode reach theorem is established at the uniform-control threshold

\[
 E_0=\frac{T}{n((n/(n-1))^k-1)}.
\]

Then the exact full CIA worst case would be

\[
 F_{n,s}(T)=T\max\left\{\frac1{s+2},
 \frac1{n((n/(n-1))^{s+1}-1)}\right\}.
\]

Indeed, at the displayed threshold E, this theorem handles every profile with some mode mass greater than E. If all masses are at most E, positive discrepancies are automatic and the proposed one-sided reach theorem supplies the negative bound. The lower witnesses are the known s+2 omitted pure modes and the uniform relaxed profile.

Thus the full two-sided problem reduces to the one-sided distinct-mode reach problem. The universal heavy-mode theorem does not prove the latter beyond the block counts already established elsewhere in this repository.

## Relation to exploratory stronger statements

The proof selects the first mode that repeats in an appropriate rounding. It does not require that mode to have largest terminal mass. The largest-mode adjacent-repeat statement in `notes/cia-adjacent-repeat-investigation.md` remains unproved. The stronger statement allowing an arbitrary specified heavy mode is false, as documented there.


## Verification

The author implementation `code/cia_tv_conjecture/universal_heavy_certificate.py` checked 1,612 exact-rational inputs: 909 already had an adjacent repeat, and 703 exercised the first-repeat prefix reordering. A separate independent dynamic-programming implementation, `code/cia_tv_conjecture/audit_universal_heavy.py`, checked 1,415 cases, including endpoint masses 1 and 3 and interior allocation plateaus. The analytic proof remains the justification of the universal statement.
