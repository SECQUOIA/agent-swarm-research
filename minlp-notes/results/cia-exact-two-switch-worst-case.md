# Exact continuous CIA worst case with two switches

Status: developed 2026-09-04 and independently agent-reviewed; see [root review](../notes/review-cia-exact-two-switch-root.md), [independent full review](../notes/review-cia-exact-two-switch-general.md), and [independent reach-proof review](../notes/review-cia-distinct-reach-general.md). This result closes the unrestricted-total two-switch problem for every n≥4. The central new step is an analytic distinct-mode reach bound; no computational certificate is used in the proof.

Let F_{n,2}(T) denote the supremum, over all measurable n-mode simplex-valued relaxed controls α on [0,T], of their minimum cumulative CIA error with at most two integer-mode switches. Then

\[
 \boxed{F_{n,2}(T)=T\max\left\{\frac14,
 \frac{(n-1)^3}{n(3n^2-3n+1)}\right\},\qquad n\ge4.}
 \tag{1}
\]

In particular F_{n,2}(T)=T/4 for n=4,5,6,7. Uniform relaxed controls are worst-case for every n≥8. Their mode-count expansion is therefore exact:

\[
 F_{n,2}(T)=\frac T3-\frac{2T}{3n}+\frac{2T}{9n^2}+O(T/n^3).
\]

## Distinct-mode reach theorem

Let A_i(t)=∫_0^t α_i(u)du, and F_i(t)=t−A_i(t). Each F_i is continuous and nondecreasing, and

\[
 \sum_iF_i(t)=(n-1)t.
\]

For an unused mode i, starting a block at time b and ending it at time t incurs negative discrepancy t−b−A_i(t). Thus an end time t is feasible at threshold E when F_i(t)≤b+E. Write its latest possible endpoint, on a horizon [0,L], as

\[
 \Phi_i(b)=\max\{t\in[0,L]:F_i(t)\le b+E\}.
\]

When 0≤b≤L this maximum exists and is at least b.

**Theorem.** For n≥4 and E>0, some sequence of at most three distinct modes reaches time

\[
 \min\{T,B_3\},\qquad
 B_3=nE\left[\left(\frac n{n-1}\right)^3-1\right],
\]

while keeping every selected mode's negative cumulative discrepancy at most E. Positive discrepancies are not constrained in this intermediate theorem.

**Proof.** Put r=n/(n−1), B_2=nE(r²−1), and L=min{T,B_3}. Suppose for contradiction that no sequence of at most three distinct modes reaches L. All reach times below are defined on [0,L].

Let R_i=Φ_i(0) be the first-block reaches. Let M_i be the largest reach of two distinct modes neither of which is i:

\[
 M_i=\max_{j,k\ne i,\ j\ne k}\Phi_k(R_j).
\]

Let M be the largest two-distinct-mode reach without an excluded mode. By the contradiction assumption, every R_i, M_i, and M is strictly smaller than L. Consequently F_i(R_i)=E. Moreover, if a pair (j,k) has reach at most a time u<L, then F_k(u)≥R_j+E. These statements follow from continuity, monotonicity, and the use of the latest feasible endpoint, including when a function has flat portions.

Sort the first-block reaches as x≥y≥z≥⋯. At time y, all modes other than one attaining x have cumulative allocation at most y−E, while the largest-reach mode has allocation at most x−E. Hence

\[
 x+(n-2)y\ge nE.
\]

Together with x≥y, this implies

\[
 (n-1)x+y\ge\frac{n^2E}{n-1}. \tag{2}
\]

One explicit identity proving this implication is

\[
 (n-1)x+y=
 \frac n{n-1}[x+(n-2)y]
 +\frac{n^2-3n+1}{n-1}(x-y),
\]

whose last coefficient is nonnegative for n≥3.

At time z, the two largest-reach modes have cumulative allocations at most x−E and y−E, and the other n−2 modes have allocations at most z−E. Therefore

\[
 x+y+(n-3)z\ge nE.
\]

Since x+y≥2z and n≥4,

\[
 (n-1)(x+y)+2z\ge\frac{2n^2E}{n-1}. \tag{3}
\]

Indeed, writing u=x+y gives the identity

\[
 (n-1)u+2z=
 \frac{2n}{n-1}[u+(n-3)z]
 +\frac{n^2-4n+1}{n-1}(u-2z),
\]

and the final coefficient is positive for n≥4.

For each mode i let x_i and y_i be the largest and second largest first-block reaches after excluding i. All pairs ending in i have reached no further than M, so

\[
 A_i(M)\le M-E-x_i.
\]

Summing these bounds gives

\[
 (n-1)M\ge nE+\sum_i x_i
 =nE+(n-1)x+y.
\]

By (2),

\[
 M\ge\frac{nE(2n-1)}{(n-1)^2}=B_2. \tag{4}
\]

Next fix i. At M_i, for every k≠i, the pair constraints imply

\[
 A_k(M_i)\le M_i-E-\max_{j\notin\{i,k\}}R_j.
\]

The maxima on the right sum over k≠i to (n−2)x_i+y_i. Using Σ_k A_k(M_i)=M_i and rearranging yields

\[
 A_i(M_i)\ge(n-1)E+(n-2)x_i+y_i-(n-2)M_i.
\]

Since M_i≤M and A_i is nondecreasing, combine this with A_i(M)≤M−E−x_i to obtain

\[
 (n-2)M_i\ge nE+(n-1)x_i+y_i-M. \tag{5}
\]

Choose a pair (p,q) attaining M. For every i outside this pair, the same pair is available in the definition of M_i, so M_i=M. Thus

\[
 \sum_iM_i=(n-2)M+M_p+M_q.
\]

The two excluded first-reach maxima satisfy x_p+x_q≥x+y, and both excluded second maxima are at least z. Summing (5) for p and q, then using (3), gives

\[
 \begin{aligned}
 \sum_iM_i
 &\ge\left(n-2-\frac2{n-2}\right)M
   +\frac{2nE+(n-1)(x+y)+2z}{n-2}\
 &\ge\left(n-2-\frac2{n-2}\right)M
   +\frac{2nE+2n^2E/(n-1)}{n-2}.
 \end{aligned}
\]

The coefficient of M is positive for n≥4. Substituting (4) and simplifying proves the aggregate bound

\[
 \sum_iM_i\ge nB_2. \tag{6}
\]

Finally, appending mode i to a maximizing pair that excludes i is a sequence of three distinct modes. The assumption that it cannot reach L implies the strict inequality F_i(L)>M_i+E. Sum this over i and use (6):

\[
 (n-1)L>\sum_iM_i+nE\ge nB_2+nE=(n-1)B_3.
\]

This contradicts L≤B_3 and proves the reach theorem. ∎

The proof also gives a finite constructive procedure. Compute first-block reaches and all ordered-pair reaches. For each candidate final mode, choose a maximizing pair excluding it and append that final mode. At least one such sequence reaches the target. The pair matrix requires n(n−1) reach evaluations; maxima excluding a mode can be obtained from a global maximizing pair plus at most two additional scans.

## Proof of the CIA worst-case formula

Let E equal the right-hand side of (1). If a mode has total greater than T/4, the heavy-mode lemma in [the global upper-bound result](cia-two-switch-global-upper.md) constructs a schedule with error at most T/4≤E. Its proof applies to arbitrary measurable controls and does not use the reach theorem above.

Otherwise every mode total is at most T/4≤E. All positive cumulative discrepancies are then automatically at most E, regardless of which modes are used. Apply the distinct-mode reach theorem at threshold E. Because

\[
 nE(r^3-1)\ge T,
\]

it reaches T using at most three distinct modes while controlling negative discrepancies. For a mode used on a single block, its largest negative discrepancy occurs at the end of that block; before and afterward the discrepancy is nondecreasing. Thus the reach inequalities control the full trajectory. This proves the upper bound in (1).

Four consecutive distinct pure-mode blocks of length T/4 force a lower bound T/4, because every two-switch schedule omits one of those four modes. The exact uniform-control theorem gives the lower bound

\[
 T/[n(r^3-1)] = T(n-1)^3/[n(3n^2-3n+1)].
\]

Both examples are admissible for n≥4. Their maximum matches the upper bound, proving (1).

For n=4,5,6,7 the uniform expression is at most T/4; for all n≥8 it is strictly greater. One can check this by the sign of n³−9n²+11n−4, which is negative at n=4,5,6,7 and positive and increasing for n≥8. The expansion in the introduction follows directly from the exact rational expression.

## Exact one-sided discrepancy minimax

The reach theorem also determines a simpler extremal quantity without any assumption on mode totals. Define the one-sided discrepancy

\[
 D^-(\alpha,\omega)=\max_i\sup_t\int_0^t[\omega_i(u)-\alpha_i(u)]\,du.
\]

For n≥4,

\[
 \sup_\alpha\min_{\omega:\#\mathrm{switches}\le2}D^-(\alpha,\omega)
 =\frac{T(n-1)^3}{n(3n^2-3n+1)}.
\]

The reach theorem proves the upper bound directly. For the uniform input, a schedule with block endpoints t_j and one-sided error E satisfies t_j≤r(t_{j−1}+E), even if a mode is repeated, because its occupation at the block endpoint is at least the current block length. Three iterations yield T≤nE(r³−1), proving the matching lower bound. Thus the uniform expression is the exact obstruction for negative discrepancies alone; the additional T/4 term in the two-sided theorem accounts for controls whose mass is spread over more modes than the schedule can select.

## Attribution and limitations

The proof's aggregate excluded-pair approach was suggested by independent event-order LP investigations of the n=4 reach problem. Those computations motivated the analytic inequality (6), but are not assumptions or verification requirements of this proof. The previous two-switch global bound remains a separate, independently reviewed argument; its finite-n gap is closed here.

The result concerns the continuous-time CIA problem. It does not assert an exact finite-grid worst-case formula or a half-grid perturbation bound for two rounded switching times. Novelty should be assessed with the existing CIA literature audit and the exact scope of the published conjecture.
