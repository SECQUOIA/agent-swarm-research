# Exact two-switch CIA worst case with equal mode totals

Status: developed 2026-09-04 and independently agent-reviewed; see `notes/review-cia-two-switch-equal-masses.md`. This file retains the earlier equal-total proof. The corresponding unrestricted-total two-switch problem is now resolved by [the exact two-switch theorem](cia-exact-two-switch-worst-case.md).

## Statement

Let n≥4, T>0, and let α:[0,T]→R^n be any measurable simplex-valued control satisfying

\[
 \int_0^T\alpha_i(t)\,dt=T/n\quad\text{for every i}.
\]

Then α has an integer control ω with at most two switches and cumulative error at most

\[
 E=T\max\left\{\frac1n,
 \frac1{n((n/(n-1))^3-1)}\right\}.
 \tag{1}
\]

This bound is the exact worst case over all α satisfying the equal-total condition. The constant relaxed control α_i(t)=1/n attains it. Thus constant uniform controls are worst-case in this class despite allowing arbitrary time-dependent redistribution of the same mode totals.

## A two-block reach lemma

Fix a threshold E>0 and a time L>0. Write A_i(t)=∫_0^t α_i(u)du for any measurable simplex-valued α. Let

\[
 R_i=\max\{t\in[0,L]:t-A_i(t)\le E\}.
\]

The maximum exists because t−A_i(t) is continuous and nondecreasing. If some R_i=L, a first block using mode i may reach L within negative discrepancy E.

Otherwise assume R_i<L for every i. Let x and y denote the largest and second largest R_i. For n≥3,

\[
 x+(n-2)y\ge nE,
 \qquad (n-1)x+y\ge\frac{n^2E}{n-1}. \tag{2}
\]

To prove the first inequality, choose p attaining x. At time y, every i≠p satisfies y−A_i(y)≥E, whereas A_p(y)≤A_p(x)=x−E. Summing all cumulative allocations at y gives

\[
 y=\sum_iA_i(y)\le(n-1)(y-E)+(x-E),
\]

which is the first inequality in (2). The second follows from x≥y and the identity

\[
 (n-1)x+y
 =\frac{n}{n-1}\,[x+(n-2)y]
 +\frac{n^2-3n+1}{n-1}(x-y).
\]

The last coefficient is positive for n≥3.

Consequently,

\[
 \max_{p\ne q}\{R_p+A_q(L)\}
 \ge\frac{nE}{n-1}+\frac Ln. \tag{3}
\]

Indeed, if all these pair values were strictly smaller than a number C, then choosing a mode p attaining x would give A_q(L)<C−x for q≠p and A_p(L)<C−y. Therefore

\[
 L=\sum_iA_i(L)<nC-[(n-1)x+y]
 \le nC-\frac{n^2E}{n-1}.
\]

It is impossible to choose C equal to the right-hand side of (3) while every pair is smaller, proving (3).

## Construction and proof of the theorem

Use E from (1), put r=n/(n−1), and define

\[
 L=T-T/n-E.
\]

For n≥4 this lies strictly between 0 and T. The defining inequality E≥T/[n(r^3−1)] is equivalent to

\[
 rE+L/n\ge L-E. \tag{4}
\]

All positive cumulative discrepancies are automatically at most T/n≤E because A_i(t)≤A_i(T)=T/n and cumulative integer occupations are nonnegative. It remains to control negative discrepancies at the ends of the selected blocks.

Form the reach times R_i on [0,L]. If R_p=L for some p, use p until L and any different mode afterward. The initial block's negative discrepancy is at most E, and the final block's negative discrepancy is T−L−T/n=E. Thus one switch already suffices in this case.

Otherwise, (3) and (4) supply distinct modes p,q with

\[
 R_p+A_q(L)\ge L-E.
\]

Select a third mode r_0 distinct from p and q, and put

\[
 t_1=\max\{0,L-A_q(L)-E\},\qquad t_2=L.
\]

Then t_1≤R_p and t_1≤L. Use p on [0,t_1), q on [t_1,L), and r_0 on [L,T]. The three negative discrepancies at their block endpoints are controlled respectively by

\[
 t_1-A_p(t_1)\le E,
 \qquad L-t_1-A_q(L)\le E,
 \qquad T-L-T/n=E.
\]

For each selected mode the discrepancy is nondecreasing before its block, nonincreasing during its block, and nondecreasing afterward. Thus these endpoint inequalities control every negative discrepancy. Together with the automatic positive bound they prove the upper bound for the complete trajectory, using at most two switches.

For the lower bound, the constant uniform input is within the equal-total class. The exact uniform-control theorem in [the main CIA result](cia-uniform-switching-obstruction.md) applies because n≥4 and s=2≤n−2, and its value is exactly (1). This proves sharpness. ∎

## Scope and implementation

The construction uses cumulative-integral evaluations and one-dimensional monotone inverse evaluations for the first-block reach times. For piecewise-constant relaxed data, each inverse can be obtained by scanning or searching its cumulative array. Finding the best ordered pair in (3) requires only the two largest reach values and the cumulative vector A(L): for each q, choose the largest R_p with p≠q.

This is an exact extremal theorem under equal total mode allocations. It does not prove that uniform inputs are worst-case with unrestricted mode totals. Moving both switches to grid endpoints is also not claimed here to preserve a half-grid error term; no such discrete corollary is used.
