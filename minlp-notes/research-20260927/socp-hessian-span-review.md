# Adversarial review of the SOCP Hessian-span reduction

Date: 2026-09-27. The complete draft
[socp-hessian-span-frontier.md](socp-hessian-span-frontier.md), Sections 1--8,
was read independently after the initial outline review. Verdict: the SOCP
reduction is sound conditional on the
nonconvex small-point and bounded-value theorems in
[nonconvex-hessian-span-frontier.md](nonconvex-hessian-span-frontier.md).
Those theorems have separate reviewers; this review does not independently
certify their entire elimination argument. Two qualifications were requested
and accepted: a derived box changes the continuous feasible set, and composing
the currently stated bounds gives a quadratic exponent in the span parameter
for inputs without continuous bounds. The full-text review also requested
explicit inclusion of a supplied continuous box in the definition of the
feasible set, and a qualification that optional equality elimination retain
the original integer coordinates and any induced compatibility rows. These
corrections have been made and independently rechecked in the main draft.
They clarify the statements; the gap and cone-lift proofs already keep the
boxes and affine rows. The revised literature paragraph also explicitly
excludes novelty for one-cone polynomial-time feasibility. No remaining gap
was found in the conditional SOCP reduction. Priority is not established.

Subsequent refinement: the independently reviewed
[coefficient-sensitive supplement](socp-coefficient-sensitive-review.md)
now justifies \(N^{O(h+1)}\) also without supplied continuous bounds.
The coarser \(N^{O((h+1)^2)}\) composition below remains a valid bound
from the original theorem statements; the later improvement uses an
additional height estimate and different explicit radius and tolerance
choices. The original review is retained to show why that extra accounting
was necessary.

## Reviewed claim and parameter

The input consists of rational affine constraints and rational SOC rows

\[
 \|A_iw+b_i\|_2\le t_i(w),\qquad t_i(w)=c_i^Tw+d_i.
\]

Define the rational quadratic polynomials

\[
 q_i(w)=\|A_iw+b_i\|_2^2-t_i(w)^2.
\]

The original SOC row is equivalent to the pair \(q_i(w)\le0\),
\(t_i(w)\ge0\). The Hessian of \(q_i\) is
\(2(A_i^TA_i-c_ic_i^T)\); it may be indefinite even though the cone
constraint defines a convex set. Consequently the earlier value theorem
for convex quadratic polynomials alone does not justify this extension.

For continuous input, \(h\) is the span dimension of these full Hessians.
For \(w=(z,x)\), where \(z\) is integer, use their \(xx\) blocks.
Expanding the rational data has polynomial encoding overhead. The parameter
concerns the supplied representation; it is not asserted to be an invariant
of the represented convex set.

## Exactness on a supplied finite box

Suppose first that all original variables have explicit finite rational
bounds. Put every affine row, both signs of each affine equality, the rows
\(-t_i\), and the polynomials \(q_i\) into a maximum violation function
\(v\), together with zero. For an integer assignment \(z\) within its
bounds, set

\[
 \alpha_z=\min_{x\in B_x}v(z,x).
\]

The epigraph formulation is a nonempty boxed QCQP: give its epigraph
variable a rational upper bound obtained by summing absolute coefficients
over the box. Its objective is linear, and its constraint Hessian span is
at most \(h\). The bounded-value theorem therefore gives a uniform effective
gap

\[
 \alpha_z=0\quad\hbox{or}\quad
 \alpha_z\ge\Delta=2^{-N^{C(h+1)}}.                 \tag{1}
\]

Here \(N\) is original total explicit input length and \(C\) is a
sufficiently large absolute constant. All bounded integer assignments have
polynomial bit length, so their substituted slice data have polynomial
length uniformly; no enumeration of assignments is involved. Appending the
epigraph variable adds a zero Hessian row and column.

Let a rational \(T\ge1\) bound \(|t_i(w)|\) for every row over the
full input box. For example, sum the absolute affine coefficients times
the coordinate magnitude bounds. Use the rational cone lift reviewed in
[socp-rational-lift-source.md](socp-rational-lift-source.md) with

\[
 \eta=\Delta/(8T^2).
\]

Retain all affine constraints exactly. Every point projected from a lifted
row satisfies \(t_i\ge0\) and
\(\|A_iw+b_i\|_2\le(1+\eta)t_i\). Since \(0<\eta\le1\),

\[
 q_i(w)\le(2\eta+\eta^2)t_i(w)^2
       \le3\eta T^2=3\Delta/8<\Delta.             \tag{2}
\]

Thus any integer assignment admitted by the lifted linear system has
\(\alpha_z<\Delta\). Equation (1) implies \(\alpha_z=0\), and
compactness supplies an exactly feasible original continuous point.
Conversely, every original feasible point lifts because the approximation
contains the exact cone. This proves equality of integer projections.

All added variables are continuous. The lift's size is polynomial in
\(N+\log(1/\eta)\), hence \(N^{O(h+1)}\). With no integer
variables, rational LP feasibility decides existence exactly in this same
bound. A feasible LP solution need not itself be an exactly feasible
original continuous solution. With fixed integer dimension, the standard
fixed-integer-dimension MILP algorithm applies to the resulting formulation.

The global quadratic polynomials need not be convex. Convexity enters through
the given SOC representation and its lifted polyhedral outer approximation.
There is no use of an invalid gradient separator for an indefinite \(q_i\).

## Inputs without continuous bounds

The small-point theorem can be used before the gap theorem, without circularity.
For a nonempty continuous SOC system, its equivalent quadratic system has a
feasible point in a uniform rational box of radius
\(R=2^{N^{O(h+1)}}\). The radius proof requires no preexisting box.
For mixed-integer input, bounded integer coordinates have uniformly bounded
encoding length, so applying the same theorem after fixing \(z\) supplies
one radius that works for every feasible integer assignment.

The continuous Hessian block does not change under integer substitution:

\[
 \nabla^2_{xx}q_i(z,x)
 =2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T),
\]

independent of \(z\). Cross terms become affine terms in \(x\).
Affine restrictions or substitution of fixed coordinates cannot increase
the span dimension. Thus a common witness box is valid without guessing a
new span bound for each assignment.

This restriction preserves feasibility and the integer projection, but not
the entire continuous feasible set. For example, a nonnegative continuous
ray loses points after intersecting it with any finite box. The final MILP
outer-approximates the boxed restriction; it is not an outer approximation
containing every continuous solution of the original unbounded model.

There is a quantitative composition issue. The newly boxed input can have
length \(L=N^{O(h+1)}\). Applying the bounded theorem as stated gives

\[
 \log(1/\Delta)=L^{O(h+1)}=N^{O((h+1)^2)}.          \tag{3}
\]

Therefore \(N^{O((h+1)^2)}\) is the conservative unboxed construction
and decision bound justified by these statements. Polynomial time for
fixed \(h\) remains valid. Recovering \(N^{O(h+1)}\) requires a
separate height estimate whose dependence on input coefficient bit length
has an exponent independent of \(h\). That refinement is not proved by
silently substituting one total-input bound into another.

The added limitation example in the main note's Section 5 was independently
checked. The system \(\|(2,y)\|_2\le y\), \(y\ge0\), is
infeasible because squaring gives \(4+y^2\le y^2\). Its quadratic
residual is the constant four. Nevertheless, for every \(\epsilon>0\),
the explicit multiplicative norm relaxation admits \(y=2/\epsilon\):

\[
 (1+\epsilon)^2y^2-(4+y^2)=8/\epsilon>0.
\]

Thus a positive squared-residual gap alone does not control global relative
norm error on an unbounded domain. The example is stated for that norm
relaxation; it does not assert that every particular polyhedral cone lift
necessarily admits the same point. This supports the use of witness
truncation followed by a finite upper bound on the cone right sides.

## Cone apex and arithmetic source check

I independently read the source note and the relevant parts of Kocuk's
[open manuscript](https://optimization-online.org/wp-content/uploads/2019/12/7501.pdf),
including equations (1), (10), and (13) and Proposition 1. The source note's
repaired construction is valid. Its stopping rule \(J\ge2\),
\(\delta b_J\ge1\), avoids a nonpositive displayed stage count. Its
coefficient bound \(\max\{169,4/\delta+1\}\) includes the fixed
first triple. I checked the half-angle comparison, norm inequalities, and
tree composition directly. The homogeneous lift implies \(t=0\Rightarrow
u=0\); neither strict feasibility nor division by \(t\) is used.

The squared encoding must retain the nonnegative right-side condition.
For example, \(\|0\|_2\le-1\) is false while its squared residual
is \(-1\). Both the sign row in the violation function and the homogeneous
cone lift prevent this spurious branch. The estimate (2) uses an upper bound
on the right side, and has no lower-bound requirement near the apex.

I also independently checked the proposed irrational-singleton example
\(\|(1,1)\|_2\le x\), \(\|(x,x)\|_2\le2\). The first row
forces \(x\ge\sqrt2\), and the second forces \(|x|\le\sqrt2\),
so their common feasible set is \(\{\sqrt2\}\). The squared residuals
\(2-x^2\) and \(2x^2-4\) have Hessians \(-2\) and \(4\), hence
span dimension one. This is a valid two-cone rational input with no rational
continuous witness. It shows a qualitative boundary of the one-cone result;
it does not establish sharpness of the general algebraic size bounds.

## Prior results and significance boundary

Kocuk's Proposition 7 already constructs a rational polyhedral outer
approximation preserving every integer point of an intersection of balls
with integer centers and radii; the discussion also mentions integral
ellipsoids. Its proof uses the unit gap between distinct integer squared
norms. Neither rational SOC approximation nor exact integer preservation
alone is new here. The proposed addition is a uniform gap after minimizing
over arbitrarily many continuous variables, controlled by continuous
Hessian span.

Blanco, Magron, and Martínez-Antón,
[*On the Complexity of p-Order Cone Programs*](https://arxiv.org/abs/2501.09828),
Journal of Complexity 91 (2025), 101979, study exact feasibility, feasible
point radius bounds, and discrepancy without input boxes. I examined
Sections 4.1 and 5 in the open PDF. Their Theorem 5.2, for \(d\) SOC
blocks, \(m\) affine inequalities, \(n+d\) variables and integer
coefficient bit bound \(\tau\), gives

\[
 m[\min\{m,n\}+d]^{O(\min\{n+d,md^2\})}
\]

arithmetic operations on
\(\tau[\min\{m,n\}+d]^{O(\min\{n+d,md^2\})}\)-bit numbers.
Their formulation permits arbitrary affine dependencies by introducing
variables and equalities. This displayed bound is not polynomial merely
because \(d\) is fixed while \(m,n\) grow. Their single-cone Theorem
4.3 also retains an exponent depending on \(\min\{m,n\}\).
The proposed span-dependent result would improve these displayed bounds
for its class. This comparison is not an exhaustive priority determination.

In particular, the single-cone case should not be advertised as a new
polynomial-time consequence merely because that paper displays a larger
bound. There is an elementary reduction to exact rational convex quadratic
programming and LP. I independently checked the following argument. Write
the single row as \(\|Aw+b\|\le t=c^Tw+d\), with arbitrary rational
affine rows. The branch \(t=0\) is an LP because it requires \(Aw+b=0\).
For \(t>0\), put \(y=w/t\), \(s=1/t\). The affine constraints become
a rational polyhedron \(P\) with \(s\ge0\) and
\(c^Ty+ds=1\); the remaining condition is
\(\|Ay+bs\|^2\le1\), \(s>0\).

First check by LP that \(P\) has a point with \(s>0\). Minimize the
convex quadratic \(\|Ay+bs\|^2\) over \(P\) exactly. Its minimum
is attained when \(P\) is nonempty, by the quadratic-programming
attainment theorem, and an exact rational optimizer can be computed in
polynomial time by the classical
[Kozlov--Tarasov--Khachiyan algorithm](https://www.mathnet.ru/eng/zvmmf5189).
The original paper's pages 1320--1321 explicitly describe exact rational
value and optimizer recovery, attainment, and rational solution bounds.
A value greater than one
rejects. A value below one permits a sufficiently small convex combination
of an optimizer and any positive-\(s\) point of \(P\). At value one,
all optimizers have the same image \(Ay+bs=v^*\), by strict convexity
of the squared norm in its image. Thus their set is exactly the rational
polyhedron \(P\cap\{Ay+bs=v^*\}\); an LP decides whether it contains
a positive-\(s\) point. This checks the elementary route, not priority for
that route or for the fixed-span extension with many cones.

The recent preprint by Hao Hu,
[*An Exact Dual for Second-Order Cone Programming Using Only Lorentz-Cone
Constraints*](https://arxiv.org/abs/2609.06757), also warrants attention.
Its abstract explicitly distinguishes polynomial formulation size over
exact real data from polynomial-time solvability and rational certificate
bit bounds. Only that abstract was examined in this review; it is not used
as a proof ingredient or treated as an exhaustive comparison.

The main capability established conditionally is exact decision and exact
integer assignment preservation at fixed span, including singular feasible
sets and weakly infeasible unbounded inputs after witness truncation. It
does not imply that the formulation is practical: the constants in the
algebraic separation bound, the size of the lift, and numerical conditioning
remain to be assessed. It does not preserve the original continuous geometry
or an arbitrary continuous objective value in one fixed MILP.

## Targeted verification record

The two primary PDFs were downloaded with Python `urllib.request` to
`/tmp/socp-review-kocuk.pdf` and `/tmp/socp-review-porder.pdf`, then extracted
with `pdftotext -layout`. Targeted `rg -n` and `sed -n` reads examined the
sections identified above.
For the one-cone comparison, the original Russian
Kozlov--Tarasov--Khachiyan PDF was also opened through MathNet and its
exact-solution definition and rational optimizer argument were read on
printed pages 1320--1321. Its full algorithm was not reverified here.

An inline `python` script using `fractions.Fraction` and SymPy checked 80
Pythagorean triples, 78 coefficient growth inequalities, 248 rational tree
error factors, 100 stopping-rule/coefficient-bound cases, 15 fixed-integer
Hessian substitutions, and two symbolic identities. All passed. The first
run used structural equality for two differently expanded SymPy expressions;
that assertion was corrected to check that their expanded difference is zero,
and the complete script was rerun successfully. These checks establish only
the finite examples and identities, not the uniform algebraic value theorem.

Document checks: `git diff --check --
research-20260927/socp-hessian-span-review.md` and an inline Python whitespace,
control-character, and final-newline check. No Lean formalization,
project-wide verification, or CI inspection was performed.
