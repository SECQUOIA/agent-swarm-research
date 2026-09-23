# Exact continuous CIA worst case with three switches

Status: developed 2026-09-04 and [independently reviewed](../notes/review-cia-exact-three-switch-transfer.md), with an additional full proof review by root. The all-n four-block prefix argument is computer-assisted: its exact finite rational and symbolic polynomial certificates have a [separate independent audit](../notes/review-cia-general-four-block.md). The heavy-mode and transfer arguments are analytic.

For every n≥5, the continuous worst-case cumulative CIA error with at most three integer-mode switches is

\[
 \boxed{F_{n,3}(T)=T\max\left\{\frac15,
 \frac1{n((n/(n-1))^4-1)}\right\}.} \tag{1}
\]

Thus F_{n,3}(T)=T/5 for n=5,...,11, and uniform relaxed controls are worst-case for every n≥12.

## Exact transfer from the one-sided prefix theorem

Set

\[
 E=T\max\left\{\frac15,
 \frac1{n((n/(n-1))^4-1)}\right\}.
\]

For any measurable relaxed control α:[0,T]→Δ_n, let m_i=∫_0^Tα_i(t)dt.

If some m_i>E, then T≤5E and the [three-switch heavy-mode theorem](cia-three-switch-heavy-mode.md) constructs a schedule with at most three switches and full error at most E.

Otherwise every m_i≤E. Every positive discrepancy A_i(t)−W_i(t) is then automatically at most E. The [general four-distinct-mode prefix theorem](cia-general-four-block-reach.md) constructs at most four distinct activation blocks reaching

\[
 \min\{T,nE((n/(n-1))^4-1)\}=T
\]

and controls every negative discrepancy W_i(t)−A_i(t) by E. Therefore its full error is also at most E. This proves the upper bound.

For the lower bound T/5, choose five successive distinct pure relaxed modes, each of duration T/5. Any integer control with at most three switches uses at most four distinct modes and omits one of these five, giving final discrepancy T/5.

The uniform relaxed input α_i=1/n has the exact value

\[
 T\max\left\{\frac1n,
 \frac1{n((n/(n-1))^4-1)}\right\}
\]

with at most three switches, by the [uniform switching theorem](cia-uniform-switching-obstruction.md). Since 1/n≤1/5 when n≥5, these two lower witnesses together match E. ∎

## Transition and asymptotics

The uniform coefficient is at least 1/5 exactly when

\[
 P(n)=n^4-14n^3+26n^2-19n+5\ge0.
\]

Direct substitution gives P(n)<0 for n=5,...,11. Writing n=12+h gives

\[
 P(12+h)=h^4+34h^3+386h^2+1469h+65>0
 \qquad(h\ge0).
\]

Hence the transition is between n=11 and n=12. In particular,

\[
 F_{n,3}(T)=\frac T4-\frac{5T}{8n}+\frac{5T}{16n^2}
 +O(T/n^3).
\]

The known omitted-mode construction and the exact uniform recurrence provide the lower bounds. The substantive upper-bound ingredients are the four-block reach inequality and the three-switch heavy-mode construction. The reach proof is computer-assisted: its finite exact rational and symbolic polynomial certificates are documented with the theorem. The transfer and heavy-mode parts are analytic.
