# Unit-normalized shift on a two-interval promise

Status: Proved for fixed-QSVT transforms; constants and parity obstruction checked  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High  

## Question

Let \(0<\delta\ll1\), fixed \(\rho>1\), and fixed \(c>0\), with
\(\rho\delta<c\).  Given a unit-normalized block encoding of a PSD
contraction \(H\) promised to have

\[
 \operatorname{spec}(H)\subseteq[\delta,\rho\delta]\cup[c,1],
\]

how many plain-block queries suffice to produce a unit-normalized encoding of
\(I-H\) to error \(\eta=\Theta(\delta)\)?  The answer depends on the constant
hidden in \(\Theta(\delta)\), and parity matters essentially.

## The affine threshold

Define

\[
 E_\rho:=\inf_{a,b\in\mathbb R}
 \max_{1\le v\le\rho^2}|\sqrt v-(a v+b)|
 =\frac{(\rho-1)^2}{8(\rho+1)}.
\]

The minimax affine polynomial has

\[
 a=\frac1{\rho+1},\qquad
 b=\frac{\rho}{\rho+1}+E_\rho.
\]

Indeed, the error of the secant-slope line equioscillates at \(v=1\),
\(v=(\rho+1)^2/4\), and \(v=\rho^2\).  The endpoint errors are
\(-E_\rho\) and the interior error is \(E_\rho\).

## Theorem (square-root upper bound above the affine threshold)

Fix \(\rho>1,c>0\), and \(\gamma>0\).  For all sufficiently small
\(\delta\), there is an even real polynomial \(p_\delta\) such that

\[
 |p_\delta(x)|\le1\quad(-1\le x\le1),
\]

\[
 \sup_{x\in[\delta,\rho\delta]\cup[c,1]}
 |p_\delta(x)-(1-x)|
 \le (E_\rho+\gamma)\delta,
\]

and

\[
 \deg p_\delta=O_{\rho,c,\gamma}(\delta^{-1/2}).
\]

Consequently standard QSVT gives a unit-normalized shifted block encoding
with \(O(\delta^{-1/2})\) queries.  In particular, for \(\rho=2\),

\[
 E_2=\frac1{24}<\frac1{16},
\]

so error \(\eta=\delta/16\) is achievable with
\(O_c(\delta^{-1/2})\) queries (for sufficiently small \(\delta\)).  Together
with the existing arbitrary-algorithm \(\Omega(\delta^{-1/2})\) bound from
the scalar pair \(\delta,2\delta\), this is tight in that regime.

Here “standard QSVT” uses the real-polynomial form of Gilyén--Su--Low--Wiebe,
Corollary 18: every real, bounded, definite-parity polynomial is obtained as
the real part of a QSP polynomial, and a control qubit coherently combines
the \(+\Phi\) and \(-\Phi\) phase sequences.  Thus no unproved claim that
\(p_\delta\) itself satisfies the stronger single-sequence complex-QSP
completion conditions is being made, and the extra control qubit causes no
normalization loss.

### Explicit construction

Work in \(u=x^2\).  For an integer \(m\ge2\), define the normalized endpoint
Fejer kernel

\[
 F_m(u):=\frac{1-T_m(1-2u)}{2m^2u},\qquad F_m(0):=1.
\]

It is a polynomial of degree \(m-1\), and, writing \(1-2u=\cos\theta\),

\[
 F_m(u)=\frac{\sin^2(m\theta/2)}{m^2\sin^2(\theta/2)}.
\]

Thus \(0\le F_m\le1\) on \([0,1]\), while

\[
 F_m(u)\le\frac1{m^2u}\quad(u>0),\qquad
 F_m(u)=1-\frac{m^2-1}{3}u+O(m^4u^2).
\]

Use \(W_m=F_m^2\).  Choose \(m\) to be the nearest integer satisfying

\[
 \frac{2(m^2-1)\delta}{3}=a=\frac1{\rho+1}.
\]

Integer rounding perturbs the left side by only \(O_\rho(\sqrt\delta)\).
Hence, uniformly for \(v\in[1,\rho^2]\),

\[
 1-W_m(\delta^2v)=a\delta v+O_\rho(\delta^{3/2}).
\]

We also need a bounded polynomial that handles the upper interval but is
negligible at the lower interval.  Put \(z=1-u\), and expand

\[
 \frac{1-\sqrt{1-z}}{1-z}=\sum_{k\ge1}d_kz^k.
\]

The coefficients satisfy \(0<d_k\le1\): the coefficients of
\(1-\sqrt{1-z}\) are positive and sum to one, and \(d_k\) are their partial
sums.  Define

\[
 S_K(u):=u\sum_{k=1}^K d_k(1-u)^k.
\]

Then, on all of \([0,1]\),

\[
 0\le S_K(u)\le1-\sqrt u\le1,
\]

and

\[
 0\le(1-\sqrt u)-S_K(u)\le(1-u)^{K+1}.
\]

Also \(S_K(u)\le Ku\), so it is \(O_\rho(K\delta^2)\) throughout the lower
cluster.  Take \(K=\Theta_c(\log(1/\delta))\) large enough that
\((1-c^2)^{K+1}\le\delta^2\).

Finally set \(A=1-b\delta\) and

\[
 P_\delta(u):=A W_m(u)+(1-W_m(u))S_K(u),qquad
 p_\delta(x):=P_\delta(x^2).
\]

For small \(\delta\), both \(A\) and \(S_K(u)\) lie in \([0,1]\), so
\(P_\delta\) is pointwise a convex combination and \(0\le P_\delta\le1\).
On \(u=\delta^2v\),

\[
 1-P_\delta(\delta^2v)
 =\delta(b+av)+O_{\rho,c}(\delta^{3/2}+\delta^2\log(1/\delta)).
\]

This gives the affine-threshold error on the lower cluster.  On \(u\ge c^2\),

\[
 W_m(u)\le\frac1{m^4u^2}=O_{\rho,c}(\delta^2),
\]

and therefore \(P_\delta(u)=1-\sqrt u+O_{\rho,c}(\delta^2)\).  Finally,

\[
 \deg p_\delta
 \le2\{2(m-1)+K+1\}=O_{\rho,c}(\delta^{-1/2}).
\]

The square on the Fejer kernel is useful: one unsquared kernel leaks
\(O(\delta)\) into the upper cluster with an inconvenient constant, whereas
the square makes this leakage \(O(\delta^2)\) without changing the asymptotic
degree or its first-order lower-cluster behavior.

## Obstruction below the affine threshold

The constant \(E_\rho\) is not an artifact of the construction.  Let
\(p(x)=P(x^2)\) be any even degree-\(2m\) polynomial bounded by one on
\([-1,1]\), and suppose

\[
 \sup_{x\in[\delta,\rho\delta]}|p(x)-(1-x)|\le\epsilon\delta.
\]

Taylor expansion at zero gives

\[
 \frac{1-P(\delta^2v)}\delta
 =\frac{1-P(0)}\delta-P'(0)\delta v+R(v).
\]

The second Markov inequality on ([0,1]) gives

\[
 \|P''\|_\infty\le \frac43m^2(m^2-1)<\frac43m^4,
\]

and hence, for \(1\le v\le\rho^2\),

\[
 |R(v)|\le\frac23m^4\rho^4\delta^3.
\]

The first two terms form an affine function of \(v\).  By the definition of
\(E_\rho\), necessarily

\[
 E_\rho\le\epsilon+\frac23m^4\rho^4\delta^3.
\]

Therefore, if \(\epsilon<E_\rho\),

\[
 \boxed{
 m\ge
 \left(\frac{3(E_\rho-\epsilon)}{2\rho^4}\right)^{1/4}
 \delta^{-3/4}.}
\]

In particular \(O(\delta^{-1/2})\) is impossible below the affine threshold,
even before imposing the upper-cluster condition.  More generally, Taylor's
theorem plus the \(k\)-th Markov inequality produces a hierarchy: if the
allowed relative error is below the best degree-\((k-1)\) approximation of
\(\sqrt v\) on \([1,\rho^2]\), then degree
\(\Omega(\delta^{-1+1/(2k)})\) is necessary.  This hierarchy is a lower-bound
observation here; matching constructions below the affine threshold have not
been proved in this note.

There is also the simpler universal even-parity lower bound.  Comparing
\(x=\delta\) and \(x=\rho\delta\), then applying the first Markov inequality
to \(P\), gives \(m=\Omega_{\rho,\epsilon}(\delta^{-1/2})\) whenever
\(2\epsilon<\rho-1\).

## Odd parity costs linearly

If \(p\) has odd parity, then \(p(0)=0\).  If it is bounded by one on
\([-1,1]\) and approximates \(1-x\) at \(x=\delta\) to error \(\eta\), the
mean-value theorem and Bernstein's inequality imply

\[
 \frac{1-\delta-\eta}{\delta}
 \le\max_{0\le x\le\delta}|p'(x)|
 \le\frac{\deg p}{\sqrt{1-\delta^2}}.
\]

Thus every odd-parity QSVT transform needs \(\Omega(\delta^{-1})\) degree.
The square-root construction must use even parity.  Since QSVT permits the
choice of degree parity, this is a design constraint, not a lower bound on all
QSVT implementations.

## Scope

The upper bound is an explicit fixed-QSVT construction and hence also an
upper bound for general converters.  The affine-threshold and odd-parity
obstructions concern a single QSVT polynomial.  The previously proved
\(\Omega(\delta^{-1/2})\) interval-promise lower bound applies to arbitrary
black-box converters.  No claim is made here that the stronger
\(\Omega(\delta^{-3/4})\) obstruction below \(E_\rho\) extends to adaptive
multi-ancilla converters.  That extension is instead supplied, with different
thresholds, by the
[adaptive lower hierarchy](2026-09-04-adaptive-normalized-shift-hierarchy.md);
the matching mixed-parity upper bounds are in the
[sharp staircase theorem](2026-09-04-normalized-shift-staircase.md).
