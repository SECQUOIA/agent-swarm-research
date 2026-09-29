# Independent review of the quadratic-fractional value theorem

Date: 2026-09-28. Reviewed manuscript:
[common-range-quadratic-fractional.md](common-range-quadratic-fractional.md),
Sections 1--5 and the stated limits in Sections 6--7. The reviewer
reconstructed the argument from its outline before reading the finished
draft. A separately assigned reviewer independently attacked the QP fiber
dichotomy, singular charts, and real-right-hand-side attainment argument.
Neither reviewer developed the proposed value proof.

**Finding.** No gap was found in the value, classification, or conditional
integer-witness claims, subject to the explicitly imported one-PSD-cut
oracle and quasiconvex mixed-value theorem. The proposed composition
preserves an absolute polynomial input exponent. This review does not
establish the pending continuous optimizer theorem, publication priority,
or practical solver performance.

## 1. Assumptions that the proof actually uses

The full numerator Hessian must be PSD in both the retained and eliminated
coordinates, including the integer coordinates. PSD only in each
continuous fiber would not suffice. It would neither prove convexity of
the projected weak sublevels nor give the parameter-independent recession
test used below.

The native kernel must satisfy the cross-aware condition
\(H_i(0,v)=0\). A zero continuous diagonal block alone does not remove
integer-continuous products. The rotated cone with squared residual
\(4-4zx\) has zero \(xx\) Hessian block but a nonzero continuous
column in the full Hessian. Eliminating \(x\) using only the first
condition would produce a coefficient depending on \(z\), contrary to
the constant-matrix premise.

Finally, retaining the denominator direction is essential before testing
numerator recession. On \(v\ge0\), take

\[
                     P(v)=-v,\qquad d(v)=v+1.
\]

The numerator tends to \(-\infty\), but the ratio has the finite,
unattained infimum \(-1\). After the manuscript's refinement
\(K'=K_*\cap\ker d_x^T\), this direction is retained, and the
recession test no longer incorrectly treats it as an eliminated fiber
direction. Every nonempty fiber then has a constant positive denominator.
Positivity is needed on the full real feasible set for the projected
convexity argument; positivity only on the mixed-integer points is a
different assumption.

## 2. Recession and attainment of the fiber QP

Write the full PSD Hessian in retained/eliminated blocks. If
\(Qh=0\) for its eliminated principal block, the padded vector
\((0,h)\) has zero quadratic form. For a PSD matrix, zero quadratic
form implies membership in its kernel. Thus every cross block also kills
\(h\), and the directional linear coefficient reduces to the constant
\(a_v^Th\). The system

\[
                     Ch\le0,\quad Qh=0,\quad a_v^Th<0
\]

is independent of the retained parameters. Its presence gives numerator
and ratio infimum \(-\infty\) in every nonempty fiber. The manuscript
correctly checks mixed-integer feasibility before concluding that the
whole problem is unbounded.

The converse also holds for irrational parameter values. To check the
attainment step, write \(v=Wy+Zs\), where the columns of \(Z\)
span \(\ker Q\). The quadratic term is positive definite in \(y\)
and absent in \(s\). The linear coefficient in \(s\) is constant.
Absence of the displayed negative recession direction makes the constant
dual set of this kernel LP nonempty. For a feasible \(y\), its finite
value is a maximum over finitely many dual vertices, hence a finite
maximum of affine functions of \(y\). One fixed feasible dual vector
supplies an affine lower bound. Constant-matrix Farkas elimination makes
the feasible \(y\)-domain closed. Adding the positive-definite quadratic
therefore gives a coercive, lower-semicontinuous objective on that domain.
Its minimum is attained, and the remaining kernel LP attains its value.
This argument uses real LP duality and does not require rational right-hand
sides.

The separate focused reviewer reconstructed the same argument. The
counterexample \(P(a,v)=av\) on \(v\ge0\) confirms why mere PSD
of the \(vv\) block would not give this dichotomy: recession would
depend on the sign of \(a\).

## 3. Singular charts and exact threshold projection

At the minimum-norm fiber minimizer, choose a linearly independent basis
of all active row normals. Every direction annihilated by those rows
allows sufficiently small feasible motion in both signs. First-order
optimality therefore supplies a multiplier, without a sign restriction
for the selected basis. For its symmetric KKT matrix,

\[
 \ker\begin{pmatrix}Q&C_I^T\\C_I&0\end{pmatrix}
       =(\ker Q\cap\ker C_I)\times\{0\}.
\]

PSD proves the first inclusion by multiplication by the primal kernel
vector, and row independence forces the multiplier component to vanish.
Motion along this kernel preserves both the objective and local
feasibility. Minimum norm makes the selected solution orthogonal to the
kernel, so the Moore--Penrose formula gives that solution exactly.
Using all active normals is necessary to include active rows with zero
objective multipliers.

An arbitrary chart may solve an inconsistent KKT right-hand side. This
does not create a false positive: its native feasibility predicate and
actual numerator value explicitly certify a feasible original point.
The chart covering a minimum supplies the reverse implication. Because
the denominator is constant and positive within the fiber, a numerator
minimizer also minimizes the ratio there. Thus the union in equation (9)
is exactly the ratio threshold projection.

Rational minors give polynomial coefficient bits for every constant KKT
pseudoinverse. The chart maps have degree at most two, native feasibility
substitutions have degree at most two, and numerator substitutions have
degree at most four. The product \(t d_0(z,u)\) has degree at most
two. There is no denominator depending on the retained parameters to
clear. The potentially exponential chart count affects construction
cost, but the algorithm never constructs this union.

## 4. Convex sublevels and the FPT exponent

At each fixed real threshold \(t\), the set before projection is

\[
                  F\cap\{P-td\le0\}.
\]

Its convexity follows from the full PSD numerator Hessian. Subtracting
an affine function does not change that Hessian. Negative numerators and
negative thresholds cause no exception. Projection preserves convexity;
strict sublevels are nested unions of weak sublevels. The generic
quasiconvex mixed-value theorem is therefore applicable even when the
joint projected epigraph is nonconvex or nonclosed. Convexity of the weak
optimal slice separately justifies its conditional integer-witness
corollary.

I checked the relevant coefficient distinction against the local primary
text of [Khachiyan--Porkolab (2000), Propositions 2.1--2.2 and
Corollary 2.3](../literature/papers/khachiyan2000-integer-optimization-on-convex-semialgebraic/fulltext.md).
The individual degree and coefficient-bit bounds do not carry the atom
count that appears in the algorithms' running times. This is the
distinction needed when the implicit chart family is exponential.
The present mixed-value theorem is a separate repository result; it is
not being attributed to that classical paper.

More explicitly, after eliminating \(r\le\rho+1\) continuous
coordinates, write the atom bounds as
\(d_E\le A(k,r)\) and \(H_E\le B(k,r)N^c\), with absolute
\(c\). The mixed-value bound has the form
\((H_E+1)d_E^{G(k)}\), so its coefficient height remains a parameter
function times \(N^c\). It is not a bound with exponent \(G(k)\)
on \(H_E\). Bisection and recognition then make a parameter function
times an absolute polynomial number of queries with similarly bounded
input length. Substituting those lengths into the one-PSD-cut oracle's
absolute polynomial exponent preserves FPT dependence on \((k,\rho)\).

The oracle sees \(P-td\) as its one distinguished PSD quadratic row,
whose Hessian is always \(Q_0\). No additional objective curvature is
silently included in the native parameter. Native PSD rows can be
converted to the stated rational SOC lift without changing their common
kernel or adding nonlinear auxiliary columns, so the mixed native model
is covered.

## 5. Classification and the positive-domain lift

After native mixed-integer feasibility and the optional fiber-recession
test, the finite-value bound supplies a magnitude bound \(M\). A
feasible threshold strictly below \(-M\) rules out a finite infimum.
Conversely, infimum \(-\infty\) makes every finite threshold feasible.
Weak threshold failure at an unattained value still gives a valid closed
bisection enclosure; value recognition does not require attainment.

The added cone

\[
                         \|(2,d-s)\|\le d+s
\]

implies \(ds\ge1\) and \(d+s\ge0\), hence \(d,s>0\).
For every original point with \(d>0\), taking \(s=1/d\)
gives a lifted point. Its squared residual is \(4-4ds\), whose
additional full Hessian has range contained in the span of the
denominator gradient and the new-coordinate direction. The increase in
the cross-aware continuous codimension is at most two. The numerator
remains PSD after adding its zero auxiliary column. This verifies the
claimed reduction from an explicitly open positive-denominator domain.

## 6. Exact checks and remaining scope

The targeted command

```text
python research-20260927/check_quadratic_fractional_value.py
```

passed. It checks exact symbolic identities for the denominator-recession
counterexample, the integer-continuous kernel distinction, PSD cross-block
annihilation, a singular KKT chart with a zero active multiplier, an
inconsistent but feasible chart, quartic numerator substitution, and an
irrational optimum with a rank-nine PSD numerator and affine native
constraints. The latter uses

\[
 \frac{s^2+1+\sum_i v_i^2}{s+1},\quad s\ge0,
 \qquad \theta=2\sqrt2-2,
\]

and the exact certificate
\(P-\theta(s+1)=(s-(\sqrt2-1))^2+\sum_i v_i^2\).
These calculations test examples, not the universal theorems or their
complexity bounds. No project-wide checks, CI inspection, or Lean proof
was used.

Section 6 correctly withholds exact continuous output. A short optimal
integer vector does not decide continuous attainment, and a minimum-norm
point in an arbitrary quadratic threshold fiber need not lie in the
coefficient field. The extra structure at the true global optimal ratio
must be used and reviewed separately. This review also makes no novelty
claim for quadratic-fractional programming, threshold reformulation, or
the polyhedral special case. The potentially useful advance is the
stated parameter dependence for the larger native model, conditional on
the new mixed-value theorem and the other reviewed inputs; its priority
requires the separate literature comparison.
