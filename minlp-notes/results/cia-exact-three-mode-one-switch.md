# Exact finite-grid CIA error with three modes and one switch

Status: developed 2026-09-04 and independently agent-reviewed; see `notes/review-cia-three-mode.md`. This complements the general continuous one-switch theorem in [the main CIA result](cia-uniform-switching-obstruction.md). Novelty remains provisional.

Let F_3(N) be the maximum, over all three-mode relaxed controls on N unit intervals, of their minimum CIA error using at most one switch. The initial activation is free. For N≥2,

\[
 F_3(N)=
 \begin{cases}
 k,&N=3k,\\
 k+\frac12,&N=3k+1,\\
 k+\frac34,&N=3k+2.
 \end{cases}
\]

The middle case has k≥1; the last case allows k=0. For completeness F_3(1)=2/3.

## Proof of the upper bound

Write A_i(t) for cumulative relaxed allocation through time t and m_i=A_i(N). A schedule using p through integer time τ and q afterward has exact error

\[
 \max\{m_h,\ \tau-A_p(\tau),\ N-m_q-\tau\},
 \tag{1}
\]

where h is the omitted third mode. This follows by checking the monotone pieces of each cumulative discrepancy; see the main CIA result for a complete derivation.

If N=3k, choose q with largest total, p with second largest total, and τ=k. Then m_h≤k, τ−A_p(τ)≤k, and N−m_q−τ≤k, proving F_3(3k)≤k.

For the remaining cases set L=k+1 and set E=k+1/2 when N=3k+1, or E=k+3/4 when N=3k+2. The following inequalities hold in both cases:

\[
 E\ge N/3,\quad N-L\le2E,\quad N+L\le4E,
 \quad E+L\ge2N/3,
 \quad3E\ge2L,\quad3E+k+2L\ge2N.
 \tag{2}
\]

The inequality 3E≥2L uses k≥1 in the N=3k+1 case; all the others also hold in the stated ranges.

There are at most two modes with totals greater than E. If there are exactly two, select those two modes. Their cumulative allocations at L sum to at least L−m_h>L−N+2E≥2(L−E), by (2). Thus one selected mode p satisfies A_p(L)≥L−E. Use it first and the other selected mode q afterward, switching at L. Equation (1) is at most E: the first negative error is controlled by the chosen cumulative allocation, the final negative error is N−m_q−L<N−E−L≤E, and the omitted mode has total below E.

Otherwise, there is at most one total greater than E. Let q have largest total and r second largest. Every schedule p→q, p≠q, and also q→r omits a mode with total at most E.

If m_q≥N−E−k, use p=r, q second, and τ=k. Both nonconstant terms in (1) are at most E because k≤E. Otherwise m_q<N−E−k. Since m_q≥N/3 and E+L≥2N/3, the final negative error of any p→q schedule switching at L is at most E. If some p≠q has A_p(L)≥L−E, that schedule works.

In the remaining case both other modes satisfy A_p(L)<L−E. Therefore A_q(L)>2E−L≥L−E, by (2). Also

\[
 m_r\ge\frac{N-m_q}{2}>\frac{E+k}{2}\ge N-E-L,
\]

where the final inequality follows from 3E+k+2L≥2N. Thus q→r, switching at L, controls both nonconstant terms of (1) by E. This proves the upper bound.

## Matching relaxed controls

When N=3k, give each mode total k, for example by using three consecutive pure-mode blocks of length k. Every one-switch schedule omits one mode and incurs error at least k.

For N=3k+1, label modes 1 and 2 as the two large modes. Use:

- k intervals of pure mode 3;
- one interval with allocations (1/2,1/2,0);
- k intervals of pure mode 1;
- k intervals of pure mode 2.

The two large modes have totals E=k+1/2. At time L=k+1, each has cumulative allocation 1/2=L−E. Any schedule omitting either incurs error at least E. If both are selected, a switch at τ≤k gives final negative error N−E−τ≥E. A switch at τ≥L gives negative discrepancy for the initial mode at least L−A_p(L)=E, since t−A_p(t) is nondecreasing. Thus every schedule has error at least E.

For N=3k+2 use:

- k intervals of pure mode 3;
- one interval with allocations (1/4,1/4,1/2);
- k intervals of pure mode 1;
- k intervals of pure mode 2;
- one interval with allocations (1/2,1/2,0).

Now the two large-mode totals are E=k+3/4 and their cumulative allocations at L are 1/4=L−E. The same argument applies: an omitted large mode incurs E; a switch at τ≤k gives final negative error at least N−E−k=k+5/4>E; and a switch at τ≥L gives initial-mode negative error at least E. This proves sharpness and the formula. ∎

Scaling every grid interval by Δ multiplies all displayed values by Δ. The formula illustrates that the half-grid term in the published conjecture is not an exact additive correction even for three modes: the actual correction to N/3 is 0, 1/6, or 1/12 depending on N modulo 3.
