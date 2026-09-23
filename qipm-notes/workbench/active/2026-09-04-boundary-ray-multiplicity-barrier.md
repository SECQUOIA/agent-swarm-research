# Boundary-ray multiplicity lower-bounds a restricted Lorentz barrier

Status: Proved; literature-screened; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

## Result

The standard Lorentz-product barrier can lose half of its ambient parameter
after affine restriction, but it cannot lose the logarithmic contribution of
a nonzero boundary ray.  This gives an exact restricted-barrier frontier for
the globally \(C^1\) full product-ball lifts studied in
[the top-class no-sharing theorem](2026-09-04-c1-euler-no-sharing-product-balls.md).

Let

\[
 Q_m=\{(t,u):t\geq\|u\|_2\},\qquad
 q_m(t,u)=t^2-\|u\|_2^2,
\]

and let an affine space \(\mathcal A\) meet the interior of
\(K=\prod_{i=1}^LQ_{m_i}\).  On
\(\Omega=\mathcal A\cap\operatorname{int}K\), restrict the standard product
barrier

\[
                 F(w)=-\sum_{i=1}^L\log q_{m_i}(w_i).       \tag{1}
\]

Suppose \(\bar w\in\mathcal A\cap K\) lies in the relative boundary of
\(\Omega\).  Let

\[
 J_1=\#\{i:\bar w_i\in\partial Q_{m_i}\setminus\{0\}\},
 \qquad
 J_0=\#\{i:\bar w_i=0\}.                                  \tag{2}
\]

Then every self-concordant-barrier parameter certified by (1) on \(\Omega\)
satisfies

\[
                         \boxed{\nu(F|_\Omega)\geq J_1+2J_0}. \tag{3}
\]

This is a lower bound for this particular restricted standard barrier, not
for arbitrary barriers on the projected feasible set.

For the grouped affine lift used below, a separate embedded-cube argument
now proves the same value for **every** possibly coupled self-concordant
barrier on that fixed slice; see
[Coupling cannot lower the barrier parameter of the grouped ball
slice](2026-09-04-coupled-barrier-grouped-ball-slice.md).  The distinction
in the preceding sentence remains necessary for an arbitrary affine lift:
diagonal duplication can create arbitrarily many nonzero boundary factors
without changing the intrinsic slice domain or its optimal barrier
parameter.

Now take

\[
                         C=(B_2^s)^k,\qquad s\geq3,\quad k\geq2, \tag{4}
\]

and an exact strictly feasible affine lift over Lorentz factors of dimensions
at most \(d\).  Assume that the lift admits globally labelled \(C^1\) primal
and polar factor selections on the full extreme slack operator.  If
\(3\leq d<s+1\), put

\[
                           h=\left\lceil{s\over d-2}\right\rceil. \tag{5}
\]

The top-class simultaneous-activity theorem below and (3) give

\[
                         \boxed{\nu(F|_\Omega)\geq kh}.      \tag{6}
\]

Separate grouped Lorentz lifts attain equality.  If \(d\geq s+1\), one
direct Lorentz factor per source ball attains, and (3) forces,

\[
                         \boxed{\nu(F|_\Omega)=k}.           \tag{7}
\]

Consequently the minimum parameter of the *restricted standard
Lorentz-product barrier*, within this globally selected \(C^1\) lift
class, is exactly

\[
 \boxed{
 \nu_{\rm std,slice}^{\min}=
 \begin{cases}
 k\lceil s/(d-2)\rceil,&3\leq d<s+1,\\
 k,&d\geq s+1.
 \end{cases}}                                               \tag{8}
\]

This is the slice analogue of the exact ambient parameter
\(2k\lceil s/(d-2)\rceil\) or \(2k\).  It shows that affine restriction can
halve the optimal standard-product certificate, but smooth switching cannot
make it smaller than one unit per necessary productive block.

## Boundary multiplicity lemma

Choose any \(w^\circ\in\Omega\) and consider the affine segment

\[
                  w(\tau)=(1-\tau)\bar w+\tau w^\circ,
                  \qquad 0<\tau\leq1.                       \tag{9}
\]

If \(a\in\partial Q_m\setminus\{0\}\) and \(b\in\operatorname{int}Q_m\),
polarization of the Lorentz determinant gives

\[
 q_m((1-\tau)a+\tau b)
 =2\tau\langle Ja,b\rangle+O(\tau^2),                      \tag{10}
\]

where \(J(t,u)=(t,-u)\).  The leading coefficient is strictly positive:
\(Ja\) is a nonzero vector in the dual cone and has positive pairing with
the interior vector \(b\).  Hence

\[
             -\log q_m((1-\tau)a+\tau b)
             =-\log\tau+O(1).                              \tag{11}
\]

At the cone vertex,

\[
             -\log q_m(\tau b)=-2\log\tau-log q_m(b).     \tag{12}
\]

An interior component contributes \(O(1)\).  Summing (11)--(12) gives

\[
                 f(\tau):=F(w(\tau))
                 =-c\log\tau+O(1),
                 \qquad c=J_1+2J_0.                        \tag{13}
\]

Here the remainder is analytic at \(\tau=0\), so differentiation gives

\[
 f'(\tau)=-{c\over\tau}+O(1),\qquad
 f''(\tau)={c\over\tau^2}+O(1).                            \tag{14}
\]

A \(\nu\)-self-concordant barrier obeys the gradient inequality on every
line,

\[
                    |f'(\tau)|^2\leq\nu f''(\tau).          \tag{15}
\]

Taking \(\tau\downarrow0\) in (14)--(15) yields \(c\leq\nu\), proving
(3).  No transversality assumption on \(\mathcal A\) is needed because the
chosen segment and the quadratic Lorentz determinant give the exact
one-dimensional vanishing orders.

## From the top-class cover to simultaneous active rays

For the full extreme slack rows

\[
                         S_a(x,z)=1-x_a^Tz,                 \tag{16}
\]

put \(p=s-1\), \(c=d-2\), and let \(N_a(x)\) count the active contact Gram
channels for row \(a\).  At every \(x\), active label sets for different
rows are disjoint and \(N_a(x)\geq\lceil p/c\rceil\).

If \(c\nmid p\), this pointwise bound already equals
\(h=\lceil(p+1)/c\rceil\).  If \(p=tc\), the top-class proof shows that the
closed sets \(E_a=\{x:N_a(x)=t\}\) do not cover the contact product.  On an
exact-label stratum in \(E_a\), the \(t\) full-capacity phase maps form a
local diffeomorphism over a proper open subset of \(S^p\).  A cover by the
\(E_a\)'s would therefore kill the nonzero product of the sphere top classes
by the relative cup-product argument.  Thus in either case there is one

\[
                         x\in(S^{s-1})^k                    \tag{18}
\]

at which every row has at least \(h\) active channels.  Pointwise
row-disjointness makes these at least \(kh\) distinct labels.  Activity
means both contact factors are nonzero complementary boundary vectors, so
the selected primal tuple \(A(x)\) is a boundary point of the affine lift
with at least \(kh\) nonzero boundary components.  Applying (3) proves (6).
When \(c\geq p\), every row has at least one active channel at every point,
and the same argument gives the \(k\) rays needed for (7).

The only lift-level input beyond the factorization theorem is that the
chosen primal factor tuple belongs to the closure of the same strictly
feasible affine slice on which (1) is restricted.  This holds for the stated
selected affine-lift model and for all explicit constructions below.  A bare
slack factorization with no specified lift realization is not enough to
define \(F|_\Omega\).

## Matching grouped lift

For each source ball, partition its \(s\) coordinates into \(h\) nonempty
groups \(G\), each of size at most \(d-2\), and impose

\[
 \left({1+s_G\over2},{1-s_G\over2},x_G\right)\in Q_{|G|+2},
 \qquad \sum_Gs_G=1.                                      \tag{19}
\]

The Lorentz determinant in (19) is

\[
                              \Delta_G=s_G-\|x_G\|^2.      \tag{20}
\]

After eliminating the public affine coordinates, (1) becomes

\[
                              -\sum_G\log\Delta_G.         \tag{21}
\]

Each summand is a one-self-concordant barrier on a paraboloid epigraph.
Products add parameters and affine restriction cannot increase them, so
(21) has parameter at most \(h\) on one ball and at most \(kh\) on (4).
At every product extreme every grouped cone component is nonzero: the
public equality \(u_G+v_G=1\) rules out the cone vertex.  Thus (3) gives
the reverse inequality, so the parameter is exactly \(kh\).  Taking one
group per source proves the large-cap equality (7).

The Hessian of (21) is diagonal plus one rank-one term per group.  Adding
one hub per term and one equality-row vertex per source ball gives a forest
of \(k\) trees and an exact \(O(ks)\) Newton solve.  Therefore a standard
short-step analysis gives the exact certificate

\[
 O\!\left(\sqrt{kh}\log{1\over\epsilon}\right)
 \quad\text{rounds},\qquad
 O\!\left(ks\sqrt{kh}\log{1\over\epsilon}\right)
 \quad\text{exact field operations}.                       \tag{22}
\]

These are upper bounds for this barrier and solver, not lower bounds on the
number of iterations taken by every IPM or QIPM.  Under matched access and
full classical iterate output, the linear tree solve also supplies a
same-round classical replacement for a quantum linear-system subroutine.

## Literature and novelty boundary

The gradient inequality (15), affine-restriction rule, and short-step
interpretation are part of the standard self-concordant-barrier calculus of
Nesterov and Nemirovskii; see Chapter 2 of
[*Interior-Point Polynomial Algorithms in Convex
Programming*](https://doi.org/10.1137/1.9781611970791.ch2).
The proof of (3) is an elementary application of the defining gradient
inequality for a self-concordant barrier.  It is related in spirit to the
classical result that a locally polyhedral vertex with \(j\) independent
active facets forces barrier parameter at least \(j\), but it counts
vanishing orders of the *specified restricted product barrier*, not local
facets of the projected domain.  No standalone novelty is claimed for this
one-dimensional lemma.

A targeted search did not locate the combination of boundary-ray
multiplicity with the \(C^1\) top-class full-slack theorem, nor the exact restricted
standard-barrier frontier (8).  The potentially new content is that
combination.  Priority remains subject to specialist review.

Scope is essential:

- (8) assumes a strictly feasible affine Lorentz-product lift with compatible
  globally selected \(C^1\) primal and polar factor sheets;
- it concerns the standard sum of Lorentz log-determinants after affine
  restriction; the companion cube theorem upgrades the grouped construction
  to arbitrary coupled slice barriers, but not every affine lift;
- the parameter is an iteration-complexity certificate, not an iteration
  lower bound; and
- finite-precision stability and data-access costs are separate questions.

## Independent hostile audit

The auditor independently expanded the Lorentz determinant on the segment
(9).  It verified that a nonzero boundary component has a strictly positive
linear coefficient by self-duality, a vertex has exact order two, and an
interior component has order zero.  Differentiating the resulting analytic
remainder gives (14), and the one-dimensional gradient inequality gives the
claimed lower bound without any transversality assumption.

For the product-ball application, a second audit checked the stronger
arbitrary-\(C^1\) upgrade.  When \(c\nmid p\), the pointwise activity count
already gives \(h\) rays for every row.  When \(p=tc\), the relative
top-class argument proves that the minimal-activity sets \(E_a\) cannot
cover, so one contact has at least \(t+1=h\) active channels for every row
simultaneously.  Pointwise row-disjointness makes the resulting \(kh\)
nonzero primal boundary components distinct.  No Baire or unique-
continuation step is needed.

The auditor also checked the matching grouped lift, the exact value (kh),
and the direct-block value \(k\).  It confirmed that the theorem needs an
actual strictly feasible affine lift whose selected boundary factors lie in
the closure of the same affine slice.  It does not follow from an abstract
slack factorization alone and does not extend to a custom or coupled slice
barrier.  No mathematical correction was required.
