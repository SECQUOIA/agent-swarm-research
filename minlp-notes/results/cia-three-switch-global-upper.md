# Three-switch CIA: exact small-mode values and a sharp asymptotic correction

Status: developed 2026-09-04 and [independently reviewed](../notes/review-cia-three-switch-global.md). This argument uses the independently reviewed three-distinct-mode prefix theorem and the three-switch heavy-mode lemma. It does not depend on a four-distinct-mode prefix theorem or computational certificates.

Let F_{n,3}(T) denote the continuous worst-case cumulative CIA error with at most three switches. For every n≥5,

\[
 \boxed{F_{n,3}(T)\le T\max\left\{\frac15,U_n\right\},\qquad
 U_n=\frac{n^4-7n^3+21n^2-29n+15}
 {n(2n-3)(2n^2-6n+5)}.} \tag{1}
\]

Consequently F_{n,3}(T)=T/5 for n=5,6,7,8,9,10,11. The first correction as n→∞ is exact:

\[
 F_{n,3}(T)=\frac T4-\frac{5T}{8n}+O(T/n^2).
\]

The lower witness for the small-mode values is the known omitted-mode construction. The matching upper bounds are supplied here.

## Avoiding a chosen final mode by distributing its relaxed allocation

Choose a mode q of largest total mass a=A_q(T). Write m=n−1. On the remaining modes define

\[
 \widehat\alpha_i(t)=\alpha_i(t)+\frac{\alpha_q(t)}m,
 \qquad i\ne q.
\]

These rates form an m-mode simplex-valued control, with cumulative allocations

\[
 \widehat A_i(t)=A_i(t)+A_q(t)/m.
\]

If a schedule using only these modes has negative discrepancy at most E'=E−a/m relative to the completed control, then relative to the original control its negative discrepancy is at most

\[
 E'+A_q(t)/m\le E.
\]

This observation uses the whole cumulative history, and therefore does not restart the rounding error at intermediate blocks.

By the [three-distinct-mode prefix theorem](cia-exact-two-switch-worst-case.md), if m≥4 and E'>0, three distinct modes different from q can reach any horizon of length at most

\[
 m E'\left[\left(\frac m{m-1}\right)^3-1\right]
 =c((n-1)E-a),
 \qquad c=\left(\frac{n-1}{n-2}\right)^3-1. \tag{2}
\]

Only negative discrepancy is asserted by this intermediate construction.

## Global upper bound

The case n=5 is already proved by the heavy-mode theorem and its all-light greedy corollary. Assume n≥6 in the remainder of this upper-bound argument.

Set E=T max{1/5,U_n}. If a mode has mass greater than E, the [three-switch heavy-mode theorem](cia-three-switch-heavy-mode.md) completes the proof.

Otherwise all mode totals are at most E. In particular a≤E, E'=E−a/(n−1)>0, and all positive discrepancies are automatically at most E. We have U_n<1/4 for n≥5, so E≤T/4. Thus

\[
 L=T-a-E\ge T-2E\ge T/2>0.
\]

Use (2) to obtain a three-block prefix avoiding q up to L, and then activate q on [L,T]. The prefix exists provided

\[
 c((n-1)E-a)\ge T-a-E,
\]

or equivalently

\[
 ((n-1)c+1)E+(1-c)a\ge T. \tag{3}
\]

For n≥6, 0<c<1. Since q has maximum mass, a≥T/n. Consequently (3) follows from

\[
 E\ge T\frac{n-1+c}{n((n-1)c+1)}=TU_n.
\]

The final q block has length T−L=a+E. Its largest negative discrepancy is its final discrepancy, equal to E. All previous modes retain their negative bounds after the prefix, and all positive bounds follow from their masses being at most E. There are at most four distinct activation blocks, proving (1).

For completeness, the algebraic upper bound used above is

\[
 \frac14-U_n=
 \frac{10n^3-56n^2+101n-60}
 {4n(2n-3)(2n^2-6n+5)}>0\qquad(n\ge5).
\]

The numerator, after writing n=5+h, is 10h³+94h²+291h+295, with all coefficients positive.

## Exact plateau and asymptotic gap

For n=5,...,11, direct exact evaluation gives

| n | U_n |
|---|---|
| 5 | 29/175 |
| 6 | 127/738 |
| 7 | 841/4697 |
| 8 | 1639/8840 |
| 9 | 971/5085 |
| 10 | 193/986 |
| 11 | 7561/37829 |

Every entry is below 1/5. Five successive distinct pure modes of duration T/5 give the matching lower bound, because any control with at most three switches omits one of them.

For sufficiently large n, the exact uniform-control lower bound is

\[
 L_n=\frac1{n((n/(n-1))^4-1)}.
\]

The difference between the upper coefficient and this lower coefficient is

\[
 U_n-L_n=
 \frac{6n^4-20n^3+21n^2-7n+1}
 {(2n-3)(2n-1)(2n^2-6n+5)(2n^2-2n+1)}.
\]

In particular,

\[
 \begin{aligned}
 U_n&=\frac14-\frac5{8n}+\frac{11}{16n^2}+O(n^{-3}),\\
 L_n&=\frac14-\frac5{8n}+\frac5{16n^2}+O(n^{-3}),\\
 U_n-L_n&=\frac3{8n^2}+O(n^{-3}).
 \end{aligned}
\]

The leading 1/4 alone is a known coarse-block rounding consequence. The matching coefficient −5/8 of the first mode-count correction is the refinement established here. This result leaves a gap of order T/n² at large n; it does not claim an exact finite-n formula there.


## Subsequent exact result

The [exact three-switch theorem](cia-exact-three-switch-worst-case.md) now closes the remaining finite-n gap, using an independently audited computer-assisted four-block reach theorem. The argument above remains an independently reviewed analytic upper bound and supplies the mode-completion step used in the arbitrary-block result.
