# Global two-switch CIA bounds and exact values for four to six modes

Status: developed 2026-09-04 and independently agent-reviewed; see `notes/review-cia-two-switch-global.md`. The finite-n gap is subsequently closed by [the exact two-switch theorem](cia-exact-two-switch-worst-case.md); this file retains the separate earlier proof. All relaxed controls below may be arbitrary measurable simplex-valued functions. Their mode totals need not be equal.

Write F_{n,2}(T) for the worst-case minimum cumulative CIA error over n-mode relaxed controls on [0,T], when the integer control may switch at most twice. For n≥4,

\[
 F_{n,2}(T)\le
 T\max\left\{\frac14,
 \frac{(n-1)^3}{3n^3-3n^2-5n+4}\right\}.
 \tag{1}
\]

Consequently,

\[
 \boxed{F_{4,2}(T)=F_{5,2}(T)=F_{6,2}(T)=T/4.}
 \tag{2}
\]

For fixed two-switch budget and increasing mode count, this determines the first finite-mode correction exactly:

\[
 \boxed{F_{n,2}(T)=\frac T3-\frac{2T}{3n}+O(T/n^2).}
 \tag{3}
\]

The upper bound differs from the exact uniform-input lower bound by only O(T/n²). Equality with the uniform lower bound at each finite n is not claimed for arbitrary totals.

## A mode with large total allocation

**Lemma.** Let n≥3 and E≥T/4. If some mode has total relaxed allocation strictly greater than E, there is an integer control with at most two switches and error at most E.

**Proof.** Set A_i(t)=∫_0^t α_i and m_i=A_i(T). Because some m_i>E, necessarily E<T. At most three modes have totals greater than E.

First suppose the largest total m_q satisfies m_q≥T−2E. The other mode totals sum to at most 2E, so at most one of them is strictly greater than E. Select that mode as p if it exists, and otherwise any p≠q. Use p on [0,E) and q on [E,T]. All omitted totals are at most E. The exact one-switch error formula gives

\[
 D=\max\{\max_{i\notin\{p,q\}}m_i,\ E-A_p(E),\ T-m_q-E\}\le E.
\]

Now suppose the largest total is smaller than T−2E. Then every total is smaller than 2E because E≥T/4. Also E<T/3, since a total greater than E is still present, so the times E and 2E lie inside [0,T].

If there are at least two modes with totals greater than E, choose one of them, q, satisfying A_q(2E)≤E. Such a mode exists since the sum of all cumulative allocations at 2E equals 2E. Put every other mode with total greater than E into the first two blocks, [0,E) and [E,2E), filling an unused block when necessary with a mode distinct from both q and the other initial mode. Use q on [2E,T]. The first two selected modes have negative discrepancy at most E because their block lengths are E, and final positive discrepancy at most E because their totals are at most 2E. The final mode's positive discrepancy before activation is at most A_q(2E)≤E, and its final negative discrepancy is

\[
 T-2E-m_q<T-3E\le E.
\]

Every omitted mode has total at most E. Monotonicity on each mode's preactivation, activation, and postactivation portions therefore controls all intermediate discrepancies.

It remains to handle a unique mode h with total greater than E. If A_h(2E)≤E, put two different modes other than h on the first two blocks of length E and h last. The preceding verification applies.

If A_h(2E)>E, use h on [0,2E], and two other distinct modes on the remaining two blocks, each of length (T−2E)/2≤E. The initial mode's negative discrepancy is 2E−A_h(2E)<E, and its final positive discrepancy m_h−2E is negative. Each other mode has total at most E, so all its positive discrepancies are bounded by E; its negative discrepancy is at most its block length, also at most E. This completes the proof. ∎

## A bound using the third largest mode total

**Lemma.** Assume n≥3 and every mode total is at most E. Let m_(3) denote the third largest total and set r=n/(n−1). If

\[
 E\ge\frac{T-m_{(3)}}{1+r+r^2}, \tag{4}
\]

then a control with at most two switches and error at most E exists.

**Proof.** Put L=T−m_(3)−E. If L≤0, a mode among the three largest totals can be used constantly: its final negative discrepancy is at most T−m_(3)≤E and all omitted totals are at most E. Hence assume L>0; clearly L<T.

Define first-block reach times R_i=max{t∈[0,L]:t−A_i(t)≤E}. If some R_p=L, use p until L and choose as final mode an unused member of the three largest-total modes. This final mode has total at least m_(3), so its final negative discrepancy is at most T−L−m_(3)=E. All positive discrepancies are bounded by the mode totals, which are at most E.

Otherwise the two-block reach lemma from [the equal-total result](cia-two-switch-equal-masses.md) gives

\[
 \max_{p\ne q}\{R_p+A_q(L)\}\ge rE+L/n.
\]

Condition (4) is equivalent to rE+L/n≥L−E. Choose a pair attaining at least L−E and set

\[
 t_1=\max\{0,L-A_q(L)-E\}\le R_p.
\]

Use p until t_1, q until L, and then a member of the three largest-total modes distinct from both p and q. The initial and middle negative discrepancies are at most E by construction. The last mode's negative discrepancy is at most T−L−m_(3)=E. All positive discrepancies are at most their mode totals, hence at most E. The same monotonicity argument controls the full trajectory. ∎

## Derivation of the global bound

Normalize T=1 by scaling time. Put r=n/(n−1), S=1+r+r², and

\[
 E=\max\left\{\frac14,\frac{n-1}{(n-2)S+6}\right\}.
\]

Simplifying the second fraction gives (n−1)³/(3n³−3n²−5n+4), as in (1). In particular 1/4≤E<1/3 for n≥4.

If some mode total is greater than 1/4, apply the first lemma with threshold 1/4, giving a schedule with error at most 1/4≤E. Otherwise every mode total is at most 1/4≤E. Let a denote the largest total.

If a≥1−3E, choose a mode with this largest total as the final mode, starting at time 2E, and use any two other distinct modes for the first two blocks, each of length E. The first two negative discrepancies are at most their block lengths, E. The last negative discrepancy is 1−2E−a≤E. All positive discrepancies are at most the mode totals, hence at most E. Thus the desired schedule exists in this case.

It remains to consider a<1−3E. Since the two largest totals sum to at most 2a, the remaining n−2 totals sum to at least 1−2a. Each is no larger than the third largest total, so

\[
 m_{(3)}\ge\frac{1-2a}{n-2}>\frac{6E-1}{n-2}.
\]

The definition of E implies

\[
 E[(n-2)S+6]\ge n-1,
\]

or equivalently

\[
 ES\ge1-\frac{6E-1}{n-2}>1-m_{(3)}.
\]

The second lemma applies. This proves (1).

For n=4,5,6 the second expression in (1) equals 27/128, 64/279, and 125/514 respectively, all at most 1/4. Thus F_{n,2}(T)≤T/4 in these cases. Conversely, four consecutive pure-mode blocks of length T/4 force error at least T/4: every schedule with at most two switches selects at most three modes and omits one of the four modes with relaxed total T/4. This proves (2).

## Sharp first finite-mode correction

For n≥8, the uniform-control theorem supplies

\[
 \frac{T(n-1)^3}{n(3n^2-3n+1)}\le F_{n,2}(T)
 \le\frac{T(n-1)^3}{3n^3-3n^2-5n+4}.
\]

The difference between these explicit upper and lower bounds is

\[
 \frac{T(n-1)^3(6n-4)}
 {n(3n^2-3n+1)(3n^3-3n^2-5n+4)}
 =\frac{2T}{3n^2}+O(T/n^3).
\]

Both have the same first two asymptotic terms:

\[
 \frac{T(n-1)^3}{n(3n^2-3n+1)}
 =\frac T3-\frac{2T}{3n}+O(T/n^2),
\]

\[
 \frac{T(n-1)^3}{3n^3-3n^2-5n+4}
 =\frac T3-\frac{2T}{3n}+O(T/n^2).
\]

Squeezing proves (3). The known coarse-grid upper bound is [(2n−3)/(2n−2)]T/3=T/3−T/(6n)+O(T/n²); see [the many-mode investigation](../notes/cia-many-mode-switching-investigation.md) and its primary sources. The new result therefore determines a correction that the known upper bound could not identify.

## Gap left by this proof and its subsequent resolution

At n=7 this result gives F_{7,2}(T)≤216T/851, while the four-block lower construction gives T/4. At n≥8 the uniform-control lower bound dominates T/4. The argument does not decide whether uniform controls are worst-case at each sufficiently large finite n, but it confines any possible improvement over them to O(T/n²). For n≥8, any counterexample at the uniform threshold must have every mode total at most T/4, by the first lemma.


The later [exact two-switch theorem](cia-exact-two-switch-worst-case.md) proves F_{n,2}(T)=T max{1/4,(n−1)³/[n(3n²−3n+1)]} for every n≥4. Thus F_{7,2}(T)=T/4, and uniform controls are worst-case for every n≥8. The bounds and constructions in this file remain valid independently of that later argument.
