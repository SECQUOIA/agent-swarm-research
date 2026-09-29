# A maximum of ratios with one shared PSD curvature matrix

Date: 2026-09-28. Status: complete proof. A fresh independent
[field and canonical-point review](common-range-shared-curvature-fractional-field-review.md)
and a separate [full value and algorithm review](common-range-shared-curvature-fractional-root-review.md)
found no unresolved gap; the author independently read both reviews.
No novelty claim is made. This extends the reviewed
[single quadratic numerator theorem](common-range-quadratic-fractional.md);
that theorem remains the established baseline.

Many fractional objectives can share one unrestricted PSD Hessian while
their affine numerator terms and positive affine denominators vary.
After introducing one common quadratic epigraph coordinate, a rational
threshold still contains only one unrestricted PSD quadratic row.
The objective count enters the input size, rather than the structural
parameter.

## 1. Model and theorem

Use the rational closed convex native PSD/SOC model in the single
quadratic-numerator theorem, with \(w=(z,x)\), \(z\in\mathbb Z^k\),
unbounded integer and continuous domains, and native cross-aware kernel
\[
 K_*=\{v:H_i(0,v)=0\text{ for every native Hessian }H_i\},
 \qquad \rho=\operatorname{codim}K_*.
\]
The native quadratic Hessians are full PSD; squared SOC Hessians may be
indefinite, with their affine cone signs retained.

Let \(Q\succeq0\) be rational and let \(m\ge1\). Consider
\[
 \inf_{(z,x)\in F,\ z\in\mathbb Z^k}
       \max_{1\le j\le m}
       \frac{\lambda_j B(w)+\widehat a_j^Tw+\widehat c_j}
            {\widehat d_j(w)},\qquad
                  B(w)=\tfrac12w^TQw,                    \tag{1}
\]
where every \(\lambda_j>0\) is rational and every rational affine
\(\widehat d_j\) is positive on all real points of \(F\).
The matrix \(Q\) has arbitrary rank and is excluded from \(\rho\).
The total explicit bit length is \(N\).

Divide numerator and denominator of ratio \(j\) by \(\lambda_j\).
The normalized objective is
\[
             \max_j\frac{B(w)+a_j^Tw+c_j}{d_j(w)}.          \tag{2}
\]
Normalization is rational with polynomial encoding growth and preserves
the rank of the denominator gradients restricted to \(K_*\). Denote
this rank by \(\ell\), and retain all those directions:
\[
 K'=K_*\cap\bigcap_j\ker d_{j,x}^T,\qquad
 x=T_1u+T_0v,\qquad r=\dim u\le\rho+\ell.                 \tag{3}
\]

**Complete theorem.** There are a computable function \(f\)
and absolute constant \(C\) giving exact optimization in
\(f(k,\rho,\ell)N^C\) bit operations: infeasibility, unboundedness
below, exact finite algebraic value, attainment, and an integer and
continuous optimizer when attained. A finite value and a canonical
attained optimizer have degree bounded by a function of
\((k,\rho,\ell)\) and representation length
\(f(k,\rho,\ell)N^C\). No dependence on \(m\) is hidden in the
parameter function; \(m\) is part of \(N\).

This is not a claim for several unrelated unrestricted PSD numerator
Hessians. Section 7 records why zero curvature coefficients also need
another argument.

## 2. One PSD threshold row

Introduce a continuous scalar \(\eta\). At a rational threshold \(t\),
the original maximum is at most \(t\) exactly when
\[
 \begin{split}
 w&\in F,\qquad z\in\mathbb Z^k,\\
 \eta+a_j^Tw+c_j&\le t\,d_j(w)\quad(1\le j\le m),\\
                         B(w)-\eta&\le0.
 \end{split}                                               \tag{4}
\]
If the original threshold holds, choose \(\eta=B(w)\).
Conversely the inequalities in (4) imply every original threshold.
For fixed rational \(t\), every new row except the last is affine.
The last is one PSD quadratic row with Hessian \(\operatorname{diag}(Q,0)\).
The [one-PSD-cut theorem](common-range-optimization.md) therefore gives
an exact threshold algorithm FPT in \((k,\rho)\). The auxiliary
coordinate has zero native Hessian column. The numerator curvature
remains excluded from the native parameter.

## 3. Exact quartic epigraph charts and finite-value bounds

After the rational split (3), the native rows are
\(Cv\le b(z,u)\), with constant rational \(C\) and quadratic \(b\).
Every \(d_j\) depends only on \((z,u)\). For free \((z,u,t)\),
the first two row families in (4) become
\[
             \widehat C y\le\widehat b(z,u,t),\qquad
                         y=(v,\eta),                      \tag{5}
\]
where \(\widehat C\) is constant rational and
\(\widehat b\) has degree at most two. Define the full PSD quadratic
objective
\[
                      \Phi(z,u,v,\eta)=B(z,x)-\eta.         \tag{6}
\]

First consider its parameter-independent negative recession test.
Let \(Q_{vv}\) be the \(vv\) block of the transformed \(Q\), and
let \(a_{j,v}\) be the eliminated part of \(a_j\). It is
\[
 Ch\le0,\qquad Q_{vv}h=0,\qquad
                         a_{j,v}^Th\le-1\quad\forall j.   \tag{7}
\]
To derive (7), the kernel of the objective Hessian in \(y\) permits
directions \((h,\sigma)\) with \(Q_{vv}h=0\). Full PSD makes all
quadratic cross blocks kill \(h\), so the directional objective
coefficient is \(-\sigma\). The new affine rows require
\(\sigma+a_{j,v}^Th\le0\). A negative direction has
\(\sigma>0\), and scaling gives (7).

If (7) is feasible and the original mixed-integer model is feasible,
every ratio tends to \(-\infty\) along the corresponding feasible
ray: its denominator is constant, its quadratic part is constant,
and its normalized affine numerator decreases strictly. Thus the
maximum tends to \(-\infty\). Feasibility of (7) is a rational LP
question; original feasibility is checked before this classification.

If (7) has no solution, the reviewed constant-matrix QP lemma shows
that every nonempty fiber of (5) has a finite attained minimum of
\(\Phi\), including irrational parameter values. Its least-norm
minimizer belongs to one of finitely many rational polynomial charts
\[
                         y_I=y_I(z,u,t),\qquad \deg y_I\le2.
\]
Their constant KKT matrices have rational Moore--Penrose inverses of
polynomial coefficient bit length. Put
\[
 \begin{split}
 D_I&=\{(z,u,t):\widehat C y_I(z,u,t)\le\widehat b(z,u,t)\},\\
 G_I(z,u,t)&=\Phi(z,u,y_I(z,u,t)).
 \end{split}
\]
The atoms of \(D_I\) are quadratic and \(G_I\) is quartic.
The projected maximum-ratio epigraph is exactly
\[
 E=\{(z,t):\exists u\ \bigvee_I
                           [D_I(z,u,t)\wedge G_I(z,u,t)\le0]\}. \tag{8}
\]
A chart point is an actual feasible lift of (4); a feasible lift has
a fiber minimum no larger than its \(\Phi\), giving the reverse
inclusion. Stationarity guards for arbitrary chart points are unnecessary.

All individual coefficient bit lengths are \(N^{O(1)}\), with an
absolute exponent. The logarithm of the chart count is polynomial in
\(N\). The charts are used only for bounds, not enumerated.
Eliminating only \(u\) gives individual atom degree \(f(k,r)\)
and bit length \(f(k,r)N^C\), independent of the number of atoms.

At fixed real \(t\), the original threshold is
\[
              F\cap\bigcap_j\{B+a_j^Tw+c_j-t d_j\le0\}.
\]
Every row has PSD Hessian \(Q\). Hence each projected weak slice
of \(E\) is convex; strict slices are nested unions of these convex
sets. The [quasiconvex mixed-value theorem](quasiconvex-mixed-value-frontier.md)
gives parameter-only finite-value degree, height \(f(k,r)N^C\),
and the same conditional bit bound for an attaining integer vector.
Its linear dependence on the incoming coefficient height is essential.

The magnitude bound distinguishes \(-\infty\) from finite values
by one sufficiently negative rational threshold. Bisection and algebraic
recognition with (4) then recover the finite value in FPT time. This
also detects unboundedness not already detected by (7).

## 4. The actual optimal lift has constant shared quadratic value

Fix an integer assignment whose continuous optimum equals a finite
attained global mixed-integer value \(\theta\). The original optimal
set is
\[
 O=\{x:(z,x)\in F,\ B(z,x)+a_j^T(z,x)+c_j
                                \le\theta d_j(z,x)\ \forall j\}. \tag{9}
\]
It is closed and convex. Every point in it has maximum ratio exactly
\(\theta\). In the lift (4) at \(\theta\), one necessarily has
\(\eta=B(z,x)\): a strict inequality would make every original
ratio strictly smaller than \(\theta\). Thus every feasible lifted
optimal point has \(\Phi=0\), and every nonempty optimal fiber of
(5) has QP minimum zero.

There is also one common full gradient \(g=Qw\) and one common
value of \(B(w)\) over this fixed-integer optimal set. For two optimal
points \(w,w'\), their midpoint is optimal. At least one ratio,
say \(j\), is active at the midpoint. Put
\(h_j=B+a_j^Tw+c_j-\theta d_j\). The exact quadratic identity gives
\[
 0=h_j((w+w')/2)
   =\tfrac12h_j(w)+\tfrac12h_j(w')
                     -\tfrac18(w-w')^TQ(w-w')
   \le-\tfrac18(w-w')^TQ(w-w')\le0.
\]
Positive semidefiniteness forces \(Q(w-w')=0\).
Consequently \(Qw\) is common and
\(w^TQw=(w')^TQw'\). Using the full \(Q\) includes all integer
cross terms. Constancy is asserted after fixing \(z\), not across
different optimal integer assignments.

## 5. Canonical field and uniform conditional box

The projected optimal set in \(u\) is the finite union of the
closed chart sets in (8) with \(z\) fixed and \(t=\theta\).
It is also convex as a projection of (9), so it has a unique
minimum-norm point \(u_*\). In its lifted optimal fiber select the
least-norm \((v_*,\eta_*)\). Section 4 makes \(\eta_*\) constant
on the whole optimal set, so this selection is equivalent to choosing
the least-norm optimal \(v_*\). The QP chart lemma gives
\[
                    (v_*,\eta_*)=y_{I_*}(z,u_*,\theta)
                                                               \tag{10}
\]
for some chart \(I_*\).

The point \(u_*\) uniquely minimizes its norm on that one chart's
closed quartic set: the set contains it and is contained in the
projected convex optimal set. The low-dimensional singleton formula
from the [single-numerator field proof](common-range-quadratic-fractional-field-review.md#3-a-direct-bound-using-classical-quantifier-elimination)
therefore bounds \((\theta,u_*)\) in one field of degree
\(f(r,\deg\theta)\) and height \(f(r,\deg\theta)(N+H)^C\),
where \(H\) is the representation length of \(\theta\).
Chart (10) is a degree-two rational polynomial in \((z,u,\theta)\),
so it adds no field extension. The same holds for \(g=Qw_*\).
No degree product over ambient coordinates is taken.

Substitution of every integer vector in the conditional attaining box
has uniformly FPT coefficient size. In any fiber with a point at
\(\theta\), that level is its actual attained optimum. Thus the
argument gives one computable rational box containing its specified
canonical point for every such integer assignment. No enumeration
of the integer box or charts is needed.
Discarding the auxiliary \(\eta\) coordinate from this box still
retains the specified original optimizer. The recovery queries below
box \((u,v)\) and use the original maximum-ratio objective;
\(\eta\) is needed only for the threshold lift and chart proof.

## 6. Attainment and exact recovery

Intersect the original model with the integer box and the full
transformed continuous box. The resulting mixed-integer set is compact.
The maximum of finitely many positive-denominator ratios is continuous,
so a nonempty boxed set has an attained minimum. This boxed value equals
\(\theta\) exactly when the original problem attains its infimum.
Integer bisection preserving that equality selects an optimal assignment.

Fix it. Every rational affine or \(u\)-norm cut inside the full box
is compact. Its exact maximum-ratio value equals \(\theta\) precisely
when it meets \(O\). This supplies an optimal-set oracle using only
rational problem inputs. Norm and coordinate bisection approximate
the same canonical \(u_*\); each precision request restarts from the
original box. The new norm row annihilates \(K'\), so the native
range remains at most \(r\). All denominator gradients annihilate
the resulting kernel.

Each coordinate of the common full gradient \(g=Q(z,x)\) is a
rational affine function of \(x\). Its constancy on \(O\) allows
ordinary rational scalar bisection with the same compact oracle.
Choose a fixed rational right inverse on the range of \(Q\), set
\(Qw_0=g\), and define \(B_0=\tfrac12w_0^TQw_0\). In the native
fiber over \(u_*\), the optimal set is exactly
\[
 Q(z,x)=g,\qquad
       a_j^T(z,x)+c_j\le\theta d_j(z,u_*)-B_0\quad\forall j.
                                                               \tag{11}
\]
The forward inclusion follows from Section 4. Conversely the gradient
equation fixes the quadratic part at \(B_0\), so all threshold
inequalities hold and the known global lower bound certifies optimality.

After substituting \(u_*\), all coefficient matrices on \(v\) in
(11) are rational and constant. Only the right-hand sides are algebraic.
The existing outward-rounding, rational minimum-norm QP, and Hoffman
argument approximates their least-norm point \(v_*\). Joint recovery
of \((\theta,u_*,g,v_*)\) yields one exact field representation.
Final substitution checks the native constraints, denominator signs,
and every threshold at the independently known optimum \(\theta\).

The field degree is parameter-only, all query and output bit lengths
are \(f(k,\rho,\ell)N^C\), and all subroutines have absolute input
exponents. Thus the value and output compositions have the stated
FPT form, using the quantitative dependencies cited above.

## 7. Positive domains, boundaries, and significance

An explicit domain \(F\cap\{d_j>0\ \forall j\}\) is handled by
one shared reciprocal coordinate \(s\) and the cones
\(\|(2,d_j-s)\|\le d_j+s\). The
[reviewed positive-domain lift](common-range-positive-domain-review.md)
preserves all objective values and attainment, increases native
codimension by at most \(\ell+1\), and makes every denominator
annihilate the new kernel. The matrix \(Q\) receives a zero
auxiliary row and column. The same parameter family therefore applies.

Strict positivity of every \(\lambda_j\) is used in Section 4.
If a term has zero curvature, it can determine the maximum while the
curved terms are slack. For example, \(\min_x\max\{x^2,1\}=1\)
has optimal set \([-1,1]\), on which \(Qx=2x\) is not constant.
Its shared epigraph coordinate need not equal \(x^2\). This example
does not disprove an FPT theorem with zero coefficients; it disproves
the output mechanism as stated. That extension remains open here.
The field reviewer found a stronger boundary:
\(\min_v\max\{(v-2)^2,2\}=2\) has native retained dimension zero
and rational value, but its minimum-norm optimizer \(2-\sqrt2\)
is irrational. Thus allowing a zero curvature coefficient breaks the
claimed same-field canonical conclusion at an actual optimal level.

The capability concerns worst-case normalization across many
scenarios with one common convex quadratic cost and scenario-dependent
affine terms and positive affine denominators. The shared-curvature
assumption is exact and concerns the input representation. No practical
speedup or solver implementation is demonstrated.

As an exact rank check, take \(M\ge1\), native constraints
\(\|(1,1)\|\le u\), \(v_i\ge u\), \(1\le w\le2\),
and \(t\ge1\), and objective
\[
 \max\left\{\frac{\sum_{i=1}^M v_i^2+u+s}{w},
             \frac{\sum_{i=1}^M v_i^2+u-s}{w}\right\}.
\]
Here \(\rho=1\), \(\ell=1\), and the shared numerator Hessian
has rank \(M\). The maximum equals
\((\sum_i v_i^2+u+|s|)/w\), so its minimum is
\(M+\sqrt2/2\), reached at \(u=v_i=\sqrt2\), \(w=2\),
and \(s=0\), with arbitrary \(t\ge1\). This exhibits an
irrational optimum and an unbounded optimal set at fixed parameters
while the excluded objective rank grows.

Classical fractional reformulation, parametric QP charts, and common
quadratic-gradient facts have substantial prior uses. The
[single-numerator prior audit](common-range-quadratic-fractional-prior.md)
credits the continuous polyhedral exact-value and attainment predecessor.
The maximum-of-ratios problem itself is classical generalized fractional
programming. The inspected publisher abstract of
[Crouzeix--Ferland (1991), *Algorithms for generalized fractional
programming*](https://doi.org/10.1007/BF01582887)
describes algorithm families, convergence, and numerical efficiency;
it was not a full-text comparison with an exact mixed-integer theorem.

[Amaral--Bomze (2019), *Nonconvex min--max fractional quadratic
problems under quadratic constraints: copositive relaxations*](https://link.springer.com/article/10.1007/s10898-019-00780-3)
directly studies multiple quadratic-over-affine ratios. Its Sections
1--3 allow unrelated indefinite numerator matrices on a compact
continuous domain and give a completely positive reformulation and
tractable lower bounds. Its wider nonconvex representation differs
from the exact parameterized algorithm proposed here. The introduction,
model assumptions (1.4)--(1.7), formulation (3.1)--(3.3), and conclusion
were inspected in the primary full text.

Searches covered shared/common Hessians, generalized fractional
programming, minimax quadratic fractional programs, and mixed-integer
fractional complexity. They also located
[Scott--Jefferson--Frenk (1998), *A duality theory for a class of
generalized fractional programs*](https://repub.eur.nl/pub/11535);
only its institutional abstract was inspected, which states a duality
result for quadratic-form/positive-concave ratios. No matching
shared-curvature mixed-integer complexity theorem was found in this
limited search. This is not evidence establishing publication priority;
a stronger prior audit remains useful.

An author-run inline Python command with exact SymPy arithmetic
checked this family for ranks \(1,2,7,12\), positive-weight
normalization, constancy of its optimal gradient and quadratic value,
the one-direction denominator refinement, the zero-curvature field
counterexample, and a quartic lifted chart with an integer cross term.
All assertions passed. These are selected algebraic and boundary checks,
not a verification of the universal complexity proof.

A targeted inline Python document check passed for the final note: eight local
links, final newline, trailing whitespace, control characters, and paired
math delimiters. The fresh field review independently checked the
canonical selector, full-gradient argument, integer cross terms, and
rational fiber, with a separate narrow subreview. The root investigator,
who did not develop this extension, separately reviewed the complete
value, recession, attainment, and recovery composition. No unresolved
gap was found under the stated assumptions and imported theorems.
No project-wide checks, CI inspection, or Lean formalization are asserted.
