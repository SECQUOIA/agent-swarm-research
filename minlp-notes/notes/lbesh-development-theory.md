# LB-ESH: mathematical contracts and quantitative separation results

Date: 2026-09-19. Author development note; independent review pending.
This note replaces the convergence and LP-exit claims in
[the original method note](lbesh-20260912-method.md) where they differ.
It develops the mathematical algorithm, not a claim that the floating-point
prototype satisfies every oracle assumption below.

## Scope, assumptions, and established results

Consider minimization with a linear objective after any epigraph lift,
global affine and convex inequality rows, bounded integer variables, and
finitely many exclusive disjunctions. For each disjunct let

\[
 S_{ik}=\{x\in C:B_{ik}x\le d_{ik},\quad
                         g_{ikj}(x)\le0\ (j\in J_{ik})\},
\]

where the original continuous domain \(C\) is a compact convex box. Variables
fixed in advance can be eliminated. Every nonlinear row is finite and convex
on an open convex neighborhood of \(C\), and the gradients used on \(C\)
have a finite bound \(L_r\). Continuous differentiability on a neighborhood
is a sufficient condition. Using a direct bound on gradients avoids assuming
that a Lipschitz constant *on a lower-dimensional box* bounds every ambient
gradient component. Write \(D=\operatorname{diam}(C)\),
\(R=\max_{x\in C}\|x\|\), and \(F_r=\max_{x\in C}|g_r(x)|\).
Rows with zero gradient bound are constant and are handled directly.

Hull copies satisfy \(x=\sum_k\nu_{ik}\),
\(\sum_k\lambda_{ik}=1\), \(\lambda_{ik}\ge0\), and
\(\lambda_{ik}x^L\le\nu_{ik}\le\lambda_{ik}x^U\).
Thus \(p_{ik}=\nu_{ik}/\lambda_{ik}\in C\) when \(\lambda_{ik}>0\), and
\(\nu_{ik}=0\) when \(\lambda_{ik}=0\). At integral indicators, exactly
the selected disjunct has \(\nu_{ik}=x\). Several disjunctions give the
intersection of their individual hull relaxations; that intersection need
not be the convex hull of the GDP feasible set.

The affine hull transform is established disjunctive programming. The
nonlinear-row cuts below are ordinary perspective outer-approximation cuts,
not a new cut family. [Frangioni and Gentile's perspective-cut work](https://arpi.unipi.it/handle/11568/104242)
is an essential precedent. [Kronqvist and Misener](https://link.springer.com/article/10.1007/s11081-020-09551-6)
already combine disjunctive cut strengthening with ESH and discuss avoiding
perspective-function numerical difficulties. [The ESH–Kelley relation](https://link.springer.com/article/10.1007/s10898-020-00906-y)
also rules out presenting the underlying boundary-cut idea as new. The
results below establish a transparent contract for this combination and
quantify choices in fractional separation; their novelty is not asserted.

## 1. Exact perspective identity and completeness

For a row \(g\), its tangent at \(z\in C\) is

\[
 \ell_z(x)=a_z^Tx+b_z,
 \qquad a_z=\nabla g(z),\quad b_z=g(z)-a_z^Tz.
\]

Convexity gives \(\ell_z(x)\le g(x)\). Consequently,

\[
 a_z^T\nu+b_z\lambda\le0                                      \tag{1}
\]

is valid for the lifted disjunct. This remains true if \(z\) is infeasible
or is only an approximate boundary point. At \(g(z)=0\), it is the usual
ESH supporting hyperplane. At \(z=p=\nu/\lambda\), it is the ECP cut.

For \(\lambda>0\), let \(G(\nu,\lambda)=\lambda g(\nu/\lambda)\).
At \((\lambda_0z,\lambda_0)\), \(\lambda_0>0\), differentiation gives

\[
 \nabla_\nu G=a_z,\qquad \partial_\lambda G=b_z.
\]

The tangent of \(G\) is exactly the left side of (1), because the constant
term cancels by positive homogeneity. Thus transforming a disjunct tangent
and differentiating the perspective give the same affine inequality.
The transform permits evaluating derivatives at the original bounded
point \(z\); it does not change the cut's mathematical strength.

For every \(p\in C\), \(g(p)=\sup_{z\in C}\ell_z(p)\): one inequality
is convexity and the other follows by choosing \(z=p\). Therefore all
cuts (1), together with scaled bounds and affine rows, describe exactly
the system of closed bounded-domain perspective inequalities for that
disjunct. At \(\lambda=0\), both the cuts and these inequalities admit
the inactive origin \(\nu=0\). Here the closure is taken for each
perspective function restricted to the scaled bounded domain; no claim
about an unrestricted recession domain is needed. If \(S_{ik}\) is
nonempty, the inactive origin is also in the closure of its positive-weight
feasible lift. If \(S_{ik}\) is empty, that latter closure is empty, while
the perspective-inequality system still admits the inactive origin.
Retaining that origin is the intended convention: an infeasible disjunct
must remain available at weight zero while other disjuncts are selected.
It is an infinite-cut identity, not a claim that one finite run constructs
a dense family of tangents.

For a finite polyhedral outer approximation
\(S_{ik}\subseteq P_{ik}\subseteq C\),
the Balas extended formulation projects to
\(\operatorname{conv}(\bigcup_kP_{ik})\). One direct proof is to divide
each positive-weight block by its weight for the forward inclusion, and
to use a convex combination for the reverse inclusion. Zero-weight blocks
vanish by boundedness. This argument establishes each disjunction's hull;
other global or logical rows are then intersected with that relaxation.

## 2. Uniform separation by ECP and ESH

Suppose \(g(p)=v>0\). ECP has \(\ell_p(p)=v\).
For ESH, suppose an anchor \(\bar x\in C\) satisfies
\(g(\bar x)\le-\delta\), \(\delta>0\). A common anchor for all rows
is convenient but not necessary for row-wise separation. On the segment
\(\bar x+t(p-\bar x)\), continuity and convexity give a boundary parameter
\(s\in(0,1)\) with \(z=\bar x+s(p-\bar x)\) and \(g(z)=0\).
The supporting inequality evaluated at \(\bar x\) yields

\[
 a_z^T(p-\bar x)\ge\delta/s.
\]

Hence the ESH tangent's violation at \(p\) is

\[
 \ell_z(p)=(1-s)a_z^T(p-\bar x)
 \ge(1-s)\delta/s
 \ge {\delta v\over LD}.                                      \tag{2}
\]

The last inequality uses \(s\le1\) and
\(v=g(p)-g(z)\le L\|p-z\|\le LD(1-s)\).
If \(D=0\), only one point exists and direct feasibility checking suffices.
An anchor is accepted only after evaluating its actual row values; the
status of an auxiliary NLP is not a certificate of strict feasibility.
Failure to find an anchor does not establish infeasibility and requires ECP
fallback. No Slater assumption is needed for ECP.

For either rule, \(\|a_z\|\le L\) and
\(|b_z|\le F+LR\), so a transformed normal has a uniform bound

\[
 K=\sqrt{L^2+(F+LR)^2}.                                        \tag{3}
\]

These formulas also hold for any chosen bounded subgradient of a finite
convex row: the supporting inequality at the anchor proves the radial
inequality for **every** such subgradient. The older review's suggestion
that one must choose a subgradient attaining the directional derivative is
unnecessary. The prototype still assumes differentiability.

## 3. Finite separation at integral master points

Fix \(\varepsilon>0\). Suppose every generated cut is retained, each
candidate satisfies the previously generated cuts, and an iteration with
any global or selected-disjunct nonlinear row exceeding \(\varepsilon\)
adds an ECP cut or the ESH cut above for at least one such row. The master
also enforces affine rows, bounds, logic, and integrality exactly. Then only
finitely many iterations can generate cuts before either there is no master
candidate or a candidate has all its relevant nonlinear rows at most
\(\varepsilon\). Inactive-disjunct rows are not included in this claim.

**Proof.** For a fixed row, ECP separates a violating point by more than
\(\varepsilon\), and ESH separates it by more than
\(\varepsilon\delta/(LD)\). A later candidate at which the same disjunct
is active must satisfy the old cut in original \(x\) coordinates. Cauchy–
Schwarz therefore separates the two candidate points by at least
\(\varepsilon/L\) for ECP or \(\varepsilon\delta/(L^2D)\) for ESH.
The same argument applies to a global row without an activity condition.
A compact box contains only finitely many points separated by any fixed
positive distance: cover it by finitely many balls of diameter smaller
than that distance. There are finitely many rows. Assign each unsuccessful
iteration one row for which a cut was added, and sum these finite bounds.
A violated positive constant row immediately eliminates its disjunct or
proves global infeasibility. This completes the argument. ∎

The proof does not require an optimal master candidate. If the master is
solved exactly to optimality, its objective is a lower bound on the true
GDP optimum. If it is solved inexactly, use the solver's valid objective
bound, not its incumbent objective, as the lower bound. Because every cut
is valid, both hull and finite-valid-big-M masters have this property.
The integral proof applies to either formulation.

An \(\varepsilon\)-feasible master point need not be exactly feasible and
does not by itself provide an exact feasible upper bound. A validated exact
incumbent of objective \(U\), together with a valid lower bound \(B\) and
\(U-B\le\eta\), certifies objective error at most \(\eta\). Finite
fixed-residual separation alone does not guarantee this gap closes.
Stopping by time, iteration count, failure to obtain an incumbent, or
stagnation must retain its actual reason.

## 4. Fractional separation with a residual certificate

Define the nonnegative bounded-domain perspective residual

\[
 r(\nu,\lambda)=
 \begin{cases}
 \lambda[g(\nu/\lambda)]_+,&\lambda>0,\\
 0,&(\nu,\lambda)=(0,0).
 \end{cases}                                                   \tag{4}
\]

Here \([a]_+=\max(a,0)\). This residual is continuous on the scaled
bounded domain, including zero weight, since \(r\le\lambda F\).

**Residual-calibrated separation theorem.** Fix \(\epsilon_p>0\).
At each fractional hull candidate, separate at least one row with
\(r>\epsilon_p\), using ECP or an ESH anchor of fixed margin. Use the
analogous positive tolerance for global rows. If all old cuts remain
satisfied, finitely many unsuccessful iterations suffice before all
perspective residuals and global residuals satisfy their tolerances, or
the relaxation is declared infeasible.

**Proof.** The ECP transformed cut is violated by exactly
\(\lambda g(p)=r>\epsilon_p\). By (2), the ESH transformed cut is
violated by more than \(\epsilon_p\delta/(LD)\). The normal bound (3)
is independent of \(\lambda\). Thus later candidate blocks satisfying
that cut are at a fixed positive distance from the cut-generating block
in \((\nu,\lambda)\) space. These blocks range over a compact set, so
the packing proof in Section 3 applies. Global rows are treated there. ∎

Let \(U_r\ge\max_{p\in C}[g_r(p)]_+\) be any finite, valid row upper
bound. One can safely skip a row without division whenever
\(\lambda U_r\le\epsilon_p\). If \(U_r>0\), any row requiring actual
separation then has \(\lambda>\epsilon_p/U_r\). This provides a
residual-derived threshold and a lower bound on the denominator, rather
than an unexplained fixed cutoff. Interval arithmetic or a known gradient
bound and a reference value can supply a conservative \(U_r\).
The theorem does not require that obtaining a tight bound be inexpensive.

With the existing rule that checks \(g_r(p)\le\varepsilon\) only when
\(\lambda\ge\tau\), a complete no-violation pass instead proves

\[
 r_r\le\max(\varepsilon,\tau U_r).                            \tag{5}
\]

For checked blocks use \(\lambda\le1\); for skipped blocks use
\(\lambda<\tau\). Thus a fixed \(0.05\) cutoff alone has no small
absolute residual guarantee if \(U_r\) is large. Rescaling a row also
rescales residual tolerances and \(U_r\); all reported tolerances must
state the row scaling. The retained-point separation proof with
\(\lambda\ge\tau>0\) is valid, using transformed margin at least
\(\tau\) times the unscaled margin and (3).

Every intermediate LP bound remains a lower bound on the intersected hull
relaxation. Only a completed no-violation pass supplies (4) or (5). A stall
or cap does not. The big-M fractional analogue has no such theorem:
the deactivation term can absorb the entire tangent violation.

## 5. Geometric error, convergence in value, and a missing regularity claim

There is a useful per-disjunction geometric bound. Suppose every retained
disjunct is nonempty and has an anchor \(\bar x_{ik}\) satisfying its
affine rows and every nonlinear row with margin at least \(\delta_{ik}>0\).
Let \(p_{ik}\) satisfy its affine rows and box, and define
\(v_{ik}=\max_j[g_{ikj}(p_{ik})]_+\). Convexity shows

\[
 q_{ik}={\delta_{ik}p_{ik}+v_{ik}\bar x_{ik}\over
                         \delta_{ik}+v_{ik}}\in S_{ik},
 \qquad
 \|q_{ik}-p_{ik}\|\le {D v_{ik}\over\delta_{ik}+v_{ik}}.         \tag{6}
\]

Indeed, each nonlinear value at the convex combination is at most
\((\delta_{ik}v_{ik}-v_{ik}\delta_{ik})/(\delta_{ik}+v_{ik})=0\),
and convex combinations preserve its affine rows and box. For any
unchecked block one may instead choose any feasible point of that block,
giving the coarser displacement bound \(D\). Therefore

\[
 \operatorname{dist}\left(x,\operatorname{conv}\bigcup_kS_{ik}\right)
 \le D\left[
 \sum_{k:\lambda_{ik}\ge\tau}
       {\lambda_{ik}\varepsilon\over\delta_{ik}+\varepsilon}
 +\sum_{k:\lambda_{ik}<\tau}\lambda_{ik}\right].                \tag{7}
\]

To prove (7), use \(x=\sum_k\lambda_{ik}p_{ik}\), form the feasible
hull point \(\sum_k\lambda_{ik}q_{ik}\), and apply the triangle
inequality and (6). If all weights are checked through (4), (6) also gives
the bound \(D\sum_k\epsilon_p/\delta_{ik}\). These are bounds for one
disjunction. The corrected points for different disjunctions need not
agree or satisfy global constraints or indicator-coupling logic.

In particular, individual disjunct Slater margins do **not** imply an
\(O(\varepsilon/\delta+\tau)\) error in the objective of the intersected
hull relaxation, contrary to suggestion S4 in the original review.
Consider \(0\le x,y\le1\), one disjunct row \(x^2-y\le0\), global
row \(y\le0\), and objective \(-x\). A disjunct anchor is \((0,1)\)
with margin one. The exact feasible set has \(x=y=0\), hence value zero;
the residual-\(\varepsilon\) point \((\sqrt\varepsilon,0)\) has value
\(-\sqrt\varepsilon\). No constant times \(\varepsilon\) bounds this
gap uniformly as \(\varepsilon\downarrow0\). Duplicate the disjunct
if an implementation requires at least two alternatives. A joint metric
error bound or suitable joint Slater/regularity assumption would be needed
for a linear objective-error bound.

A weaker value-convergence conclusion needs no such rate assumption.
Suppose compact master candidates satisfy the affine relaxation, their
global and perspective residuals tend to zero, and they are exact LP
optima of valid outer relaxations. Every cluster point is feasible for
the intersected hull relaxation by continuity of (4). Every master value
is at most its optimum \(v_H\), whereas every cluster objective is at
least \(v_H\). Compactness then shows all the master values converge to
\(v_H\). No rate follows. The same cluster argument with integral
indicators proves convergence to the GDP optimum when residual tolerances
tend to zero and master objectives are optimal. If the exact feasible set
is empty, such a compact sequence cannot exist. Approximate master solves
also suffice if their optimality errors tend to zero.

## 6. Epigraphs and compactness

For a continuous convex objective \(f(x)\), introduce \(t\ge f(x)\)
and minimize \(t\) plus any linear indicator cost. A finite box for
\(x\) does not itself bound \(t\); the compactness hypothesis must be
established rather than silently inherited. A tangent at \(x_0\) gives
a finite lower bound
\(m=\min_{x\in C}\{f(x_0)+\nabla f(x_0)^T(x-x_0)\}\).
A finite known \(M\ge\max_{x\in C}f(x)\) gives an optimization-equivalent
lift with \(m\le t\le M\), because every original feasible \(x\) can
be lifted with \(t=f(x)\). This upper bound removes unnecessary lifted
points but preserves an optimal lift for every original feasible point.
For example, a known Lipschitz bound gives
\(M=f(x_0)+L_fD\). The epigraph is assumed to appear only in its own
global row and the objective, not as an independently constrained original
decision variable.

Alternatively, a validated feasible incumbent and a total-objective cutoff,
together with bounded indicator costs, give an upper bound on \(t\).
Before such an incumbent exists this alternative supplies no bound.
Without explicit epigraph bounds one may prove a bounded-candidate property
from the actual master solves, but that needs its own argument; arbitrary
single-tree callback candidates are not covered merely because LP optima
would choose the smallest admissible \(t\).

The epigraph row can always use ECP. A reported incumbent objective must
be recomputed as \(f(x)\) plus original costs, rather than copied from an
epigraph variable that is feasible only to a nonlinear residual tolerance.

## 7. Single-tree correctness is an oracle contract

The single-tree algorithm uses the same globally valid cuts. Its correctness
requires the following solver/oracle properties; API use alone is not a proof.

1. The solver handles the finite mixed-integer linear master correctly,
   retains all lazy cuts for purposes of final feasibility, and eventually
   processes or fathoms every relevant node in the absence of limits.
   If a callback returns a candidate violating an old lazy cut, that cut is
   re-enforced before counting a new separation iteration. Fresh cuts in
   the packing argument are generated only at points satisfying all old
   cuts. Repeated callbacks for an unenforced old cut are a solver
   integration issue outside the packing argument; the solver must resolve
   those repetitions in finite time.
2. Every potentially accepted integer candidate is checked against all
   original global rows and the rows of its selected disjuncts. A violation
   above the chosen nonlinear tolerance produces a valid rejecting lazy
   cut with a uniform positive separation margin. Numerical inability to
   generate a rejecting cut is a failure status, not acceptance.
3. Submitted NLP heuristic points are checked for original feasibility,
   including bounds, affine rows, integrality, logic, and the original
   objective. A failed or locally infeasible NLP is not a certificate that
   an integer assignment is infeasible. An assignment is excluded only
   with a valid infeasibility proof. A feasible point needs no optimal NLP
   status to supply an upper bound.
4. A solver lower bound is interpreted with its documented numerical
   tolerances and the actual objective transformation. A valid exactly
   feasible upper bound \(U\) and a valid lower bound \(B\) with
   \(U-B\le\eta\) establish feasible \(\eta\)-optimality. Exact
   optimality requires zero gap in exact arithmetic; final master status
   alone establishes neither conclusion.
5. Optional fractional user-cut generation is disabled, capped at finitely
   many cuts, or satisfies the retained-cut and uniform-margin assumptions
   of Section 4 (or its fixed-positive-threshold variant). Unrestricted
   fractional cut generation, including repeated generation after cuts
   have been purged, is not covered by the finite-termination argument.

Under the exact-arithmetic versions of these contracts and the compactness
assumptions, Sections 2–3 bound the number of distinct nonlinear rejection
cuts. Contract 5 also bounds fractional cut generation. After those cuts,
finite MILP solution under contract 1 either proves
infeasibility or yields a point meeting the nonlinear tolerance. No global
NLP oracle is needed for this residual conclusion. Exactly feasible
\(\eta\)-optimality needs the upper/lower-bound condition in contract 4.
If the integration
instead accepts approximate incumbents, its result must expressly retain
that feasibility qualification; solving the master does not remove it.

This theorem is conditional on a complete branch-and-cut solver, not a
polynomial runtime bound. Optional fractional user cuts affect strength,
not the required integer-candidate validation.

## 8. Finite arithmetic and approximate boundary points

Exact tangents at approximate boundary points remain valid when the full
constant \(g(z)-\nabla g(z)^Tz\) is retained. Dropping \(g(z)\) is unsafe
when \(g(z)<0\): for \(g(x)=x^2-1\) and \(z=1/2\), the artificial
boundary cut \(x\le1/2\) excludes feasible points.

Validity does not ensure useful separation. A robust implementation checks
the actual transformed cut violation; if the ESH cut has insufficient
margin, it tries ECP. If neither is reliably rejecting, it reports the
numerical separation failure instead of claiming no violated nonlinear row.

A sufficient rigorous arithmetic model is explicit. Let an exact valid
cut on a compact domain be \(q^Ty\le d\), and suppose computed
\((\widetilde q,\widetilde d)\) satisfy a certified uniform error bound

\[
 |(\widetilde q^Ty-\widetilde d)-(q^Ty-d)|\le E
 \quad\hbox{for every domain point }y.
\]

Then \(\widetilde q^Ty\le\widetilde d+E\) is valid. If the exact
generating violation is at least \(\kappa\), its violation of the relaxed
computed cut is at least \(\kappa-2E\). If later candidates may violate
stored cuts by \(\rho\), a strictly positive margin requires
\(\kappa>2E+\rho\); a uniform coefficient bound then restores the packing
argument with that reduced margin. Nonlinear evaluations similarly require
error bounds before they can certify that a residual is below a tolerance.
This is a sufficient certified scheme, not a claim that ordinary double
precision gradients, Gurobi bounds, or Ipopt statuses provide interval
certificates. Ordinary numerical experiments should report maximum original
constraint residuals and objective gaps with the tolerances used.

## 9. ESH and ECP have no general cut dominance

For \(g(x,y)=x^2+y^2-1\), take violating point \(p=(2,0)\) and
strict anchor \(\bar x=(0,1)\cdot 0.9=(0,0.9)\). The line crosses
the unit circle at a point \(z=(z_x,z_y)\) with \(z_y>0\).
The ECP cut is \(x\le5/4\); the ESH cut is
\(z_xx+z_yy\le1\), where
\(z_x=(0.81+\sqrt{1.57})/2.405\) and \(z_y=0.9-0.45z_x\).
On the common box \([-2,2]^2\), the point \((1.2,1)\) satisfies ECP
but violates ESH, and \((1.3,-2)\) satisfies ESH but violates ECP.
Thus the two valid cuts are not generally ordered; benchmark conclusions
must compare their actual effects, not assert a universal ESH improvement.
If the anchor, boundary point, and violating point lie on a common radial
line for a Euclidean ball, the supporting cut does dominate the tangent at
the exterior point. That special geometry does not extend to arbitrary
anchors. Both statements persist after the hull transform by setting
\(\lambda=1\).

## 10. A representation-sensitivity diagnostic

Boundary cuts have a limited representation invariance that helps explain
when a separation policy might matter. Let \(g\) be a differentiable convex
row, and replace it by \(\widehat g=\phi\circ g\), where \(\phi\) is
convex, differentiable, strictly increasing on the relevant range,
\(\phi(0)=0\), and \(\phi'(0)>0\). The feasible set and every anchor's
strict-feasibility classification are unchanged, and the transformed row
remains convex. For a fixed anchor and exterior point, exact line search
finds the same boundary point \(z\). Its gradient is
\(\nabla\widehat g(z)=\phi'(0)\nabla g(z)\), so its ESH inequality is
the same halfspace, up to positive scaling. The hull transform preserves
this equality of halfspaces.

In contrast, at an exterior point \(p\) with \(v=g(p)>0\) and
\(\phi'(v)>0\), the transformed ECP inequality is

\[
 \nabla g(p)^T(x-p)\le-\phi(v)/\phi'(v),                        \tag{8}
\]

whereas the original ECP inequality has right side \(-v\). These are
not generally equal. A positive linear \(\phi\) is one case where they
are. The statement requires keeping the anchor fixed: an interior-point
optimization procedure can choose different anchors for different row
representations. It also assumes exact roots; residual-based approximate
line search and floating-point scaling need not be invariant.

A quantitative example is

\[
 \min\{-x:0\le x\le2,\quad
             g_a(x)=\exp(a(x-1))-1\le0\},\qquad a\ge2.
\]

Every instance has the identical feasible interval \([0,1]\), optimum
\(-1\), and strict anchor zero. With only the box initially, or after a
tangent at the anchor, the first master optimum is \(p_0=2\): the anchor
tangent has upper bound \((e^a-1)/a\ge2\). An exact ESH boundary cut
gives \(x\le1\) immediately. ECP at a master point \(p_k>1\) gives
the next master point

\[
 p_{k+1}=p_k-{1-\exp[-a(p_k-1)]\over a}.                       \tag{9}
\]

This follows by solving its affine tangent inequality for \(x\). The
new upper bound is smaller than the preceding one and remains above one,
because \(0<1-e^{-u}<u\) for \(u>0\). Thus previous tangents do not
alter (9). Each iteration decreases \(p_k\) by strictly less than
\(1/a\). To reach fixed geometric accuracy \(p_k\le1+\eta\),
\(0<\eta<1\), therefore requires

\[
 k>a(1-\eta).
\]

This is a lower bound on the number of master separation iterations,
not total runtime: ESH performs a line search, and its oracle work must
be counted. The ECP sequence nevertheless decreases to one, since any
larger limit would give a positive limiting decrement in (9).
The example is an exact-arithmetic diagnostic of representation
sensitivity, not a GDP-specific hardness result, a novel ESH principle,
or a representative application benchmark. Large \(a\) also creates
floating-point overflow and conditioning concerns that do not appear in
the exact derivation. Function-residual tolerances are not geometrically
comparable across \(a\), so empirical versions must stop by a common
distance/objective criterion and report evaluation costs.

## What these results support

The strongest supportable general statement is a perspective-OA algorithm
with a choice of boundary or exterior-point tangents, valid lower bounds,
finite fixed-tolerance separation under explicit compactness and solver
contracts, and residual-controlled fractional separation. The geometric
repair bound and the counterexample explain precisely why a useful hull
residual certificate is weaker than an objective-error certificate.
The results do not establish a new cut family, finite exact convergence,
a convergence rate for the intersected hull objective, or computational
superiority. Experimental benefit and novelty of the full implementation
require separate evidence.
