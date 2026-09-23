# Exact zero-query radius for hidden-block state conversion

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorem; moderate on novelty  
Question: What exactly happens in the previously unresolved
\(p-\epsilon=o(k/G)\) state-conversion sliver?

## Minimax theorem

Use the target states from paper Section 8. Put \(r=k/G\):

\[
 \rho_S=\frac pk\sum_{g\in S}|g\rangle\!\langle g|\otimes\rho_W
 +\frac{1-p}{G-k}\sum_{g\notin S}|g\rangle\!\langle g|\otimes\rho_L,
\]

\[
 \rho_0=\frac1G\sum_g|g\rangle\!\langle g|\otimes\rho_L^0.
\]

The exact worst-case error achievable with zero input queries is

\[
 \boxed{
 R_0=\min_{\tau\in\mathcal D}
 \max\left\{
 D_{\rm tr}(\tau,\rho_L^0),
 \frac12\left[
 r\left\|\tau-\frac pr\rho_W\right\|_1
 +(1-r)\left\|\tau-\frac{1-p}{1-r}\rho_L\right\|_1
 \right]
 \right\}.
 }
\]

Therefore \(Q_\epsilon=0\) if and only if \(\epsilon\geq R_0\).

To prove it, dephase the label register and twirl any input-independent output
over all label permutations. Convexity cannot increase worst-case trace
distance, so an optimum has the form

\[
 \sigma_\tau=\frac1G\sum_g|g\rangle\!\langle g|\otimes\tau.
\]

Block-diagonal additivity of the trace norm gives the displayed distances to
\(\rho_0\) and every \(\rho_S\). Conversely every density operator \(\tau\)
defines such a zero-query output, proving equality.

## Exact special cases

If \(\rho_W=\rho_L=\rho_L^0\) and \(p\geq r\), then

\[
 R_0=p-r.
\]

Thus every requested excess winner probability
\(\delta=p-\epsilon\leq r\) is literally free.

If \(p=r\), \(\rho_L^0=\rho_L\), and \(r\leq1/2\), then

\[
 \boxed{R_0=rD_{\rm tr}(\rho_W,\rho_L).}
\]

The upper bound takes \(\tau=\rho_L\). For the lower bound, write
\(a=D(\tau,\rho_L)\), \(b=D(\tau,\rho_W)\). If \(a\geq rD(W,L)\) the first
term suffices. Otherwise the triangle inequality gives
\(b\geq D(W,L)-a\), and

\[
 rb+(1-r)a\geq rD(W,L)+(1-2r)a\geq rD(W,L).
\]

Consequently, when \(D(W,L)<1\) is fixed, every
\(\delta=p-\epsilon=o(r)\) is eventually in the zero-query region. For
orthogonal winner and loser states, \(R_0=r\), so every \(\delta>0\) leaves
that region. The previously unresolved sliver therefore cannot have a
universal winner-mass-only law; its boundary depends on full internal-state
geometry.

More generally, if \(\rho_W\perp\rho_L\), \(\rho_L^0=\rho_L\),
\(p\geq r\), and \(r\leq1/2\), direct minimization gives

\[
 R_0=
 \begin{cases}
 \dfrac{p(1-2r)+r^2}{1-r},&p\leq(1+r)/2,\\[6pt]
 \dfrac{p}{1+r},&p\geq(1+r)/2.
 \end{cases}
\]

An optimal center lies on the segment
\(\tau=t\rho_W+(1-t)\rho_L\); projecting onto the two orthogonal supports is
a CPTP retraction, so it cannot worsen the minimax problem.

## Optimized detuned-preparation upper bound

The public loser state can also be optimized rather than fixed to \(\rho_L\).
For \(m\in[r,p]\) and a density matrix \(\tau\), prepare winner mass \(m\),
winner internal state \(\rho_W\), and loser internal state \(\tau\). The exact
branch errors are

\[
 e_0(\tau)=D_{\rm tr}(\tau,\rho_L^0),
\]

\[
 e_k(m,\tau)=\frac{p-m}{2}
 +\frac12\|(1-m)\tau-(1-p)\rho_L\|_1.
\]

A rejection trial has acceptance probabilities

\[
 P_k=r/m,qquad P_0=\frac{r(1-m)}{m(1-r)}.
\]

Simultaneous fixed-point amplification therefore gives

\[
 Q_\epsilon\leq\widetilde O\!\left(
 Q(f)\inf_{\substack{r\leq m\leq p,\ \tau\in\mathcal D\\
 \max\{e_0(\tau),e_k(m,\tau)\}<\epsilon}}
 \sqrt{\frac{m(1-r)}{r(1-m)}}
 \right),
\]

with \(\widetilde O(Q(f)/\sqrt r)\) as the exact-branch fallback. This
strictly improves the paper's fixed-loser choice and replaces its coarse
internal-discrepancy split by a finite-dimensional optimization.

## Novelty boundary

Twirling and trace-norm block additivity are standard. A targeted search has
not yet found this exact hidden-block minimax radius. Its main value is to
replace the paper's qualitative zero-query caveat by an explicit finite-
dimensional convex optimization and sharp contrasting examples.
