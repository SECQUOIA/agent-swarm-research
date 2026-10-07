# Exact polynomial output after discovering an active face

Date: 2026-10-02. Complete restricted theorem with an explicit active-gradient
precision term. This removes the full-Hessian premise for strictly
complementary boundary optima, but does not remove the known precision
obstruction. Review and diagnostics are in [README.md](README.md).

## 1. Result and the additional parameter

Use the input model of the
[implicit convex-patch theorem](../../research-20261002/new-direction/implicit-convex-patch-certificate.md):
an explicit rational polynomial of fixed degree \(d\) on a bounded mixed
product box, a supplied factor-tree decomposition with bag size \(p\),
and a verified rational upper coordinate-curvature bound \(L>0\).
Input length \(I\) includes the decomposition and curvature certificate.
Preprocess fixed coordinates and inward-rounded native integer bounds.

Assume a unique optimizer \(a\) and unknown point growth

\[
 F(x)-F(a)\ge g\|x-a\|^2\quad(x\in X),\qquad
                    \kappa=\max\{1,L/g\}.                       \tag{1}
\]

Every continuous coordinate active at an original bound is assumed
**strictly complementary**: its inward derivative is positive. Let
\(\gamma>0\) be the smallest such inward derivative. If there are no
active continuous coordinates, the margin parameter below is set to one.

Compute a rational \(M\ge1\) bounding every absolute continuous-Hessian
row sum on the original continuous box hull, uniformly over the integer
coordinates. Fixed-degree coefficient bounds give one in polynomial work
and with polynomial bit length. Define, for analysis only,

\[
 B_\gamma=\left\lceil\log_2\max\{2,M/\gamma\}\right\rceil.       \tag{2}
\]

Neither \(a,g,\gamma\), nor \(B_\gamma\) is supplied.

**Theorem.** A deterministic algorithm constructs an exact implicit global
optimizer with a finite rational certificate in

\[
                    f_d(p,\kappa)\operatorname{poly}(I+B_\gamma)
                                                                    \tag{3}
\]

bit work. The output is a fixed integer assignment, a selected continuous
box face, and a certified strongly convex polynomial subproblem on a
rational box in that face. Its unique minimizer is a global optimizer of
the original problem. The certificate is sound without the growth and
strict-complementarity promises; those ensure termination and (3).

There is no assumption on the full continuous Hessian at \(a\). Once all
active continuous coordinates are fixed, the remaining principal Hessian
is at least \(2gI\): its coordinates are interior, so (1) applied in every
two-sided free direction gives this by a second-order limit. No quantitative
distance from these coordinates to their bounds is required for that
limit or for the theorem.

The \(B_\gamma\) term is material. It need not be polynomial in \(I\)
under fixed degree, width, and \(\kappa\). Thus (3) is not the stronger
\(f_d(p,\kappa)\operatorname{poly}(I)\) theorem for arbitrary boundary
optima requested in the general open problem.

## 2. Two verifiable face reductions

Suppose a rational retained box \(C\) is known to contain every original
optimizer and its integer coordinates have been fixed. Work on a copy
\(B\) of its continuous box. A coordinate can be fixed to an original
lower bound \(\ell_i\) when that bound is an endpoint of \(B_i\) and
\(\partial_iF\ge0\) throughout \(B\). Replacing that coordinate by
\(\ell_i\) cannot increase the objective. For an original upper bound,
use \(\partial_iF\le0\). Every reduction preserves the minimum over
the current box, since the clamped point remains in it. Several such
reductions may be applied sequentially with fresh certificates.

A weak sign proves preservation of **at least one** global optimizer,
not containment of every one. Accordingly, after such a reduction the
certificate states equality of the original and restricted minimum values.
If the sign is strict, every optimizer uses the selected bound. Under the
unique-optimizer promise all sound reductions preserve \(a\), including
weak ones, but the verifier need not trust that promise.

Here are explicit polynomial-time or parameterized sign tests.

1. Let \(c\) be the midpoint of the current face box and \(r\) its
   maximum half-width. The row-sum bound gives
   \(\partial_iF(x)\ge\partial_iF(c)-Mr\) and
   \(\partial_iF(x)\le\partial_iF(c)+Mr\). A strictly positive lower
   bound or strictly negative upper bound certifies elimination.
2. Optionally, expand each derivative factor in a tensor Bernstein basis
   on its current rational box. Sum the minimum coefficients for a lower
   bound and the maximum coefficients for an upper bound. These bounds
   certify weak signs as well. Each factor scope has size at most \(p\)
   and degree at most \(d-1\), so each expansion has at most
   \((d+1)^p\) entries; this is not an expansion over all variables.
   All coefficients are computed exactly. The basis is a nonnegative
   partition of unity, so the test is sound. It is a sufficient test and
   is not claimed complete for nonnegative polynomials.

Apply any successful test, substitute the fixed coordinate, and scan again.
At most \(n\) substitutions occur per copy of a retained box. No search
over active sets or user-supplied face is needed. The optional Bernstein
test can certify a sign before a tiny true margin is numerically resolved;
the termination proof uses only the first test.

After the reductions, attempt the exact midpoint-Hessian/third-derivative
patch check of the predecessor on the remaining coordinates. If no
coordinates remain, the retained point is already an exact rational
optimizer. If the patch check succeeds, its unique constrained minimizer
has the original global value by containment followed by the recorded
minimum-preserving reductions.

The finite certificate need not prove uniqueness in the **original** box
when a weak reduction was used. It proves a unique optimizer in the selected
face and its original global optimality. This distinction affects the output
claim but not the requested construction of one exact optimizer.

## 3. Explicit search without a supplied margin

For each integer \(\mu\ge2\), define

\[
 K_\mu=4^\mu,\qquad \theta_\mu=2^{-\mu},\qquad
                         \tau_\mu=L/(4K_\mu).                   \tag{4}
\]

One trial runs the polynomial corrected-grid/min-marginal pruning algorithm
on the original box with grading \(\theta_\mu\), including the
individual-integer-label filter of the predecessor. It refines indefinitely
until a patch succeeds or its usual coordinate-label cap is exceeded.
Check the cap while generating labels, before allocating a larger bag
table. A cap failure ends that trial unsuccessfully.

After each stage with singleton integer coordinates, make a copy of the
retained box and perform Section 2's reductions. On the resulting face,
compute the midpoint restricted Hessian \(H_B(c)\) and use the rational
third-derivative bound \(T\ge1\) from the predecessor. Test by exact
linear algebra that

\[
                  H_B(c)-(Tr+\tau_\mu)I\succ0.                 \tag{5}
\]

The bound \(T\) may be taken over the original box and all continuous
coordinates; restriction only reduces the needed row sum. If (5) fails,
discard the copy and continue the original pruning trial. Thus no
unproved growth assertion or heuristic active-set choice enters a future
global pruning decision.

Trials must be interleaved so a large precision requirement does not force
exponentially finer grading. Use a deterministic time-bounded dovetail:
in phase \(q=2,3,\ldots\), run each trial \(2\le\mu\le q\),
from its start if desired, for at most \(2^{q-\mu}\) elementary bit
steps. Accept the first verified patch. Total allotted work through phase
\(q\) is \(O(2^q)\). Universal simulation and scheduling can be
implemented with polynomial overhead in the logarithm of this bound,
which is absorbed below. Restarting trials makes a particularly direct
finite schedule; their previous partial states need not be retained.

This is a complete algorithm. It does not wait forever at an unsuitable
conditioning guess or escalate \(K_\mu\) once per failed precision
stage. The latter schedule would lose (3) when \(\gamma\) is tiny.

## 4. Termination and bit complexity

Let \(\mu_*\) be the first trial with \(K_{\mu_*}\ge8\kappa\).
Then \(K_{\mu_*}\le32\kappa\), including the initial-trial case.
The existing pruning theorem keeps every optimizer, respects the label cap,
and after stage \(j\), with \(h_j=s_0 2^{-j}\), bounds every
continuous half-width by

\[
                     r\le5\sqrt{n\kappa}\,h_j.                 \tag{6}
\]

Its integer-label filter fixes all integer coordinates once
\(h_j\le1/(10\sqrt{n\kappa})\). These claims use point growth for
their analysis; the recorded pruning remains sound independently.

At an active continuous coordinate, its original bound remains an endpoint
of every retained box containing \(a\). If

\[
 r\le\gamma/(4M),\qquad r\le L/(8K_{\mu_*}T),                 \tag{7}
\]

then the first sign test fixes that coordinate. For a lower-active one,
\(\partial_iF(c)-Mr\ge\gamma-2Mr\ge\gamma/2>0\);
upper-active coordinates have the reversed inequality. Substitutions
preserve \(a\) and cannot enlarge \(r\), so all active coordinates
are removed in the scan.

For the remaining free block, \(H_B(a)\succeq2gI\), hence

\[
 H_B(c)-(Tr+\tau_{\mu_*})I
 \succeq(2g-2Tr-\tau_{\mu_*})I\succ0.                         \tag{8}
\]

Indeed, \(2Tr\le L/(4K_{\mu_*})\le g/4\) and
\(\tau_{\mu_*}\le g/4\). Thus (5) succeeds. Conditions (6)--(7)
require only
\(j=\operatorname{poly}(I)+O(\log\kappa+B_\gamma)\) stages.
Numerical magnitudes of \(M,T,L,s_0\) contribute their binary lengths,
not their numerical values, to this count.

At fixed degree the predecessor bounds every grid value and message by a
polynomial in input length, stage, and the parameter-dependent label count.
Each sign test and Hessian test adds
\(f_d(p)\operatorname{poly}(I+j+\mu_*K_{\rm grid})\) work.
Consequently trial \(\mu_*\) succeeds in
\(A=f_d(p,\kappa)\operatorname{poly}(I+B_\gamma)\) bit steps.
The dovetail reaches it by
\(q=\mu_*+\lceil\log_2\max\{1,A\}\rceil\), so total work is
at most \(O(2^{\mu_*}A)\), up to the stated polynomial simulation
overhead. Since \(2^{\mu_*}=O(\sqrt\kappa)\), this proves (3).

An earlier successful trial may have a much smaller certified patch
curvature. Do not infer an \(O(\kappa)\) conditioning bound for that
patch from (3). To evaluate its implicit optimizer to \(q\) bits with
the original parameter dependence, use the original problem's
[certified enclosure algorithm](../../research-20261002/new-direction/deterministic-boundary-output.md),
Section 1, whose point and value guarantees require only point growth.
It describes the same optimizer under (1), without trusting a curvature
bound for the accepted patch. If a feasible point on the selected face is
desired, clamp its fixed continuous coordinates to the certified bounds;
this cannot increase its Euclidean distance to \(a\). For certified
value bounds use the enclosure algorithm directly, or request additional
position accuracy using a rational gradient bound on the original box.
The evaluation cost is \(f_d(p,\kappa)\operatorname{poly}(I+q)\)
under the uniqueness/growth promise, plus reading the saved certificate.

The descriptor itself is also unambiguous without that promise: its
strongly convex KKT problem has a unique primal solution. General
approximation using that patch's own verified curvature remains possible;
only its favorable \(\kappa\)-dependent cost uses the original promise.

## 5. Examples and exact limitations

The earlier full-Hessian obstruction
\(G(x,y)=F_{\rm chain}(x)+y+x_ny^2\), with \(y\ge0\), is
immediately reduced by \(\partial_yG=1+2x_ny\ge1\). Its extremely
small full-Hessian eigenvalue never needs representation. The variant
\(F_{\rm chain}(x)+y(1-y)\) on \(0\le y\le1/2\) has a
negative full-Hessian entry \(-2\). Its Bernstein derivative
coefficients \(1,0\) certify weak monotonicity globally, select \(y=0\),
and leave the uniformly strongly convex chain. Thus discovery covers actual
indefinite boundary cases, not only a relabeling of positive full Hessians.

Strict complementarity still permits an extremely small margin. In the
[nearby-minimum construction](../../research-20261002/new-direction/deterministic-boundary-output.md),
the global optimum has active \(y=0\) with
\(\partial_yG(a,0)=3a_n/2>0\), where
\(a_n=2^{-(4\cdot2^n-2)}\), at fixed degree, bag size, and growth ratio.
Thus \(B_\gamma\) is exponential in chain length. The earlier
[rectangular sign obstruction](../../research-20261002/new-direction/implicit-optimum-precision-obstruction.md)
and nearby nonglobal local minimum remain intact. This theorem does not
claim that every instance incurs that cost; a correlated identity or a
different certificate can bypass it, as those notes demonstrate.

If some active derivative is zero, the automatic Bernstein reductions may
still succeed, or the remaining full Hessian may already pass (5). But no
general termination theorem is proved here for weakly complementary active
coordinates. A restricted Hessian alone is not an algorithm for discovering
their face. The general finite exact certificate under point growth alone
remains open.

## 6. Primary comparison

Interval derivatives, endpoint substitution, and monotonicity propagation
are established methods; see Araya, Trombettoni, and Neveu,
[Exploiting monotonicity in interval constraint propagation](https://www.lirmm.fr/~trombetton/publis/mohc_aaai_2010.pdf).
The predecessor's
[primary-source audit](../../research-20261002/prior-art/implicit-convex-patch-prior.md)
also compares rigorous interval search, alphaBB, and finite KKT branching.
This result adds the explicit automatic face-discovery schedule and its
margin-dependent bit bound to the existing sparse containment and exact
implicit convex-patch framework. It does not claim a new monotonicity rule,
active-set principle, or general boundary closure theorem.
