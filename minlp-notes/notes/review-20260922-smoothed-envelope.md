# Review of the smoothed scalar-envelope candidate

Date: 2026-09-22. Independent adversarial review of a candidate supplied by
the research coordinator. This review proves a slightly stronger statement
and records the limits of the literature check. It does not certify novelty.

**Conclusion.** The proposed bound is correct. Counting only changes between
sampled winners leaves a small proof gap involving isolated ties. Counting
cells that contain any optimal tie repairs it. This also removes the proposed
semialgebraic assumption entirely. Midpoint sampling improves the constant.

## Precise statement and proof

Let \(Z\) be a nonempty subset of \(\{0,1\}^n\), let
\(I=[a,b]\) with \(T=b-a>0\), and let each deterministic function
\(q_z:I\to\mathbb R\) be \(L\)-Lipschitz. Let the random variables
\(\xi_1,\ldots,\xi_n\) be independent and have Lebesgue densities bounded
by \(\phi\). Define

\[
 F_z(t)=q_z(t)+\xi^Tz,\qquad V(t)=\min_{z\in Z}F_z(t).
\]

Let \(B\) be the set of parameter values in \((a,b)\) where the minimum
is attained by at least two distinct supports. Then

\[
 \mathbb E|B|\le 2n\phi LT.                              \tag{1}
\]

In particular \(B\) is finite almost surely. The number \(K\) of maximal
connected intervals on which the minimizing support is unique satisfies

\[
 \mathbb E K\le 1+2n\phi LT.                            \tag{2}
\]

Intervals are understood relative to \(I\), with tie points removed. The
same support can occupy two different intervals, and both are counted.
The original proposed bound \(1+4n\phi LT\) is therefore valid as well.

**Fixed-parameter isolation.** Fix \(t\), and put
\(c_z=q_z(t)\). Conditional on all noise coordinates except \(\xi_i\),
the best values in the two classes \(z_i=0\) and \(z_i=1\) have the form
\(A_i\) and \(B_i+\xi_i\). Both \(A_i,B_i\) are now fixed.
When either class is empty, ignore that coordinate. The event that their
values differ by at most \(\delta\) has conditional probability at most
\(2\phi\delta\).

Order all support values, including multiplicity. If the difference
\(\Delta(t)\) between the smallest two is at most \(\delta\), take
supports attaining those two values and a coordinate where they differ.
They attain the minima within their respective bit classes: a better
support in the runner-up's class would contradict its rank. Thus

\[
 \Pr\{\Delta(t)\le\delta\}\le 2n\phi\delta.            \tag{3}
\]

If there is only one support, interpret the gap as infinity. Letting
\(\delta\downarrow0\) proves that a fixed parameter has a unique
minimizer almost surely. Arbitrary deterministic support costs \(c_z\)
do not affect this conditioning argument.

**Cell bound.** Partition \(I\) into \(m\) equal closed cells of length
\(\eta=T/m\), and let \(C_m\) count cells containing a point of \(B\).
At the midpoint \(s\) of a cell, choose its unique minimizing support
\(z\). Suppose that \(t\) in this cell is a tie point. Some minimizing
support \(y\) at \(t\) differs from \(z\), and
\(F_y(t)-F_z(t)\le0\), whether or not \(z\) is itself optimal at \(t\).
Consequently

\[
 0\le F_y(s)-F_z(s)
 \le 2L|s-t|\le L\eta.
\]

Hence \(\Delta(s)\le L\eta\), and (3) gives

\[
 \mathbb E C_m\le m(2n\phi L\eta)=2n\phi LT.            \tag{4}
\]

This argument detects a tie even when the same branch wins on both sides.
It also detects several changes hidden inside one cell. Those cells will
separate at sufficiently fine resolution.

**Passage to the number of ties.** By (3), almost surely no endpoint or
midpoint of any of these countably many grids is a tie. On this probability
one event, every finite subset of \(B\) occupies distinct cells for all
sufficiently large \(m\). Therefore

\[
 |B|\le\liminf_{m\to\infty}C_m,
\]

where an infinite tie set gives an infinite right-hand side. Fatou's lemma
and (4) prove (1), including the assertion that \(B\) is finite almost
surely. On each component of \(I\setminus B\), the unique minimizing
support is locally constant, by continuity and finiteness of \(Z\), hence
constant. There are \(|B|+1\) components. This proves (2).

All relevant events are measurable. For example, the event that a closed
cell contains an optimal tie is a finite union over pairs of supports of
projections, over a compact parameter interval, of their joint equality
and optimality conditions. Equivalently it is the event that the minimum
gap over the cell is zero; the gap is a continuous function of the finite
vector of branch values. Tie points at deterministic cell boundaries have
probability zero, so using open or closed cells does not change (4).

Semialgebraicity is not used. In particular the theorem itself establishes
almost-sure finiteness even when unperturbed Lipschitz differences have
infinitely many zeros.

The constant \(2\) in (1) is optimal under these hypotheses. For \(n=1\),
take \(I=[0,T]\), \(L>0\),
\(q_0(t)=L(t-T/2)\), \(q_1(t)=-L(t-T/2)\), and
\(\xi_1\) uniform on \([-LT,LT]\). There is exactly one interior
crossing almost surely, at \(t=T/2+\xi_1/(2L)\). Its density bound is
\(\phi=1/(2LT)\), so \(\mathbb E|B|=1=2n\phi LT\).

## Application and limitations

For branches \(q_z(t)=(t-t_z)^2/D_z\) on \([0,1]\), if
\(D_z\ge1\) and \(0\le t_z\le1\), then \(|q_z'(t)|\le2\).
Thus \(\mathbb E K\le1+4n\phi\). Adding \(\xi^Tz\) is exactly
independent perturbation of the original indicator penalties: fixing
support commutes with adding a constant that depends only on that support.
Uniform noise on \([-\varepsilon,\varepsilon]\), with
\(0<\varepsilon\le1/2\), has \(\phi=1/(2\varepsilon)\) and keeps
unit baseline penalties positive.

The bound concerns the perturbed instance. It does not give exact solutions
of the unperturbed instance, and it does not show how to find all remaining
branches efficiently. A small output can still be expensive to identify.
Nor does it bound the binary encoding length of crossing locations under
arbitrary real-valued perturbations. It is not an exact Turing-time theorem.

The family and parameter domain must be fixed independently of the noise.
The noise must distinguish every pair of support labels; unperturbed bits,
dependent noise without a conditional density bound, or several distinct
branches with the same label require a different argument. Independence can
be replaced by the stated conditional density bound for each coordinate
given the others, but marginal density bounds alone do not suffice.

Uniformly bounded branch slopes on a bounded parameter interval are
essential to this proof. Indicator messages with support-dependent feasible
parameter domains need not satisfy the hypotheses. Higher-dimensional
parameters are not covered: cell counts scale differently and an interface
usually contains infinitely many points.

### Subtracting a common function can sharpen the estimate

One can first replace every \(q_z\) by \(q_z-g\), for any deterministic
common function \(g\). Winners and tie points do not change. Only the
Lipschitz constants of the relative branch costs matter.

For the main
[constant-coefficient construction](research-20260922-constant-data-messages.md),
put \(D_0=W_n\). Its centers satisfy
\(0\le c_z\le\theta/(1-\theta)\), and
\(0\le D_z-D_0\le\theta^2/(1-\theta^2)\). Subtracting
\(g(t)=t^2/D_0\) shows that every relative branch is Lipschitz with constant

\[
 L_{\rm rel}=\frac{2\theta}{1-\theta}
              +\frac{2\theta^2}{1-\theta^2}.
\]

Thus \(\mathbb E K\le1+2n\phi L_{\rm rel}\), which is
\(1+O(n\phi\theta)\) uniformly in the horizon. This is the principal
application. There is no exponentially vanishing factor in this estimate.

For the dyadic construction in the existing
[message-complexity note](research-20260922-message-complexity.md), write
\(A=\theta^n\), \(D_0=\sum_i\theta^{2(n-i)}\), and

\[
 d=\max_z(D_z-D_0)
   =\frac{\theta^{2n}}{(2^n-1)^2}\frac{4^n-1}{3}.
\]

The centers belong to \([0,A]\), and \(D_0\ge1\). Subtracting
\(g(t)=t^2/D_0\) gives

\[
 |(q_z-g)'(t)|
 \le 2t\frac{D_z-D_0}{D_zD_0}+\frac{2t_z}{D_z}
 \le2d+2A.
\]

Therefore \(\mathbb E K\le1+4n\phi(A+d)\), and the probability of any
optimal tie or support change is at most \(4n\phi(A+d)\). This estimate
tends to zero exponentially for fixed noise density. It applies to the
dyadic construction with centers in \([0,\theta^n]\); a different
constant-coefficient construction with centers in a fixed interval does
not inherit that exponential factor.

## Literature examined and significance

The isolation step is established background. Beier and Vöcking's
*Typical Properties of Winners and Losers in Discrete Optimization*
develops winner-gap estimates and smoothed complexity through rounding.
I inspected the openly available
[STOC 2004 version](https://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/BeierV.pdf)
(in particular Lemma 5) and checked the metadata of the
[2006 journal version](https://epubs.siam.org/doi/10.1137/S0097539705447268).
The journal's full text was not inspected. Roughgarden's
[2014 lecture 15, Section 5](https://www.timroughgarden.algorithmsilluminated.org/f14/l/l15.pdf)
explicitly gives the same two-sided coordinate-class conditioning proof
and constant \(2n\phi\delta\). Adding arbitrary deterministic support
offsets leaves that proof unchanged; this is not a new isolation lemma.

Beier, Röglin, Rösner, and Vöcking's
[*The smoothed number of Pareto-optimal solutions in bicriteria integer optimization*, Theorem 1](https://link.springer.com/article/10.1007/s10107-022-01885-6)
allows an arbitrary deterministic objective and one perturbed linear
objective, with a bound involving dimension, density bounds, and expected
absolute coefficient sizes. For binary sets this gives an established
polynomial bound on the entire Pareto set. It is closely related when
\(q_z(t)\) is affine in a common scalar parameter. The inspected statement
does not directly count repeated intervals for arbitrary nonlinear
Lipschitz branches.

Applegate, Archer, Johnson, Nikolova, Thorup, and Yang's
[*Wireless coverage prediction via parametric shortest paths*, Section 6](https://arxiv.org/html/1805.06420)
proves smoothed bounds for parametric shortest-path breakpoints by a
random-plane projection result attributed to Nikolova et al. (2006).
The perturbation is angular noise in two objective vectors, and the
underlying branch costs are affine in the scalar parameter. This is a
direct antecedent for smoothed parametric complexity, but its inspected
theorem is not the Lipschitz-branch statement proved above.

The new candidate should therefore be presented as a short transfer from
classical isolation to bounded-variation scalar parameter dependence, with
a concrete indicator-message consequence. The independent search did not
locate the exact general statement, but was not exhaustive and does not
establish priority. No claim of a new general smoothed-optimization
framework or an algorithmic speedup is justified by the present argument.

## Verification record

This review independently reconstructed the isolation, cell, and limit
arguments. The removal of semialgebraicity and the midpoint improvement
were derived during the review. No numerical experiments, Lean proof, or
project-wide verification were run. The claims concern general probability
and continuity arguments for which finite sampling would not materially
strengthen the proof.
