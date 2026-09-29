# Field bounds for a convex quadratic fractional optimizer

Date: 2026-09-28. Status: independent proof review. The canonical optimal
point has the field and height bounds stated below. The argument uses one
quadratic-programming chart and classical coefficient-sensitive quantifier
elimination. A separate review checked the optional sharper perturbation
argument in Section 6. This is an encoding result, not an optimization
algorithm or a novelty claim.

## 1. Assumptions and conclusion

Let \(F\subseteq\mathbb R^n\) be a closed convex set given by rational
native convex quadratic inequalities or rational SOC rows, together with
rational affine rows. Keep the right-hand-side sign of every SOC row when
using its squared polynomial. Let \(H_i\) be the native quadratic Hessians,
and let

\[
 q_0(x)=\tfrac12x^TQ_0x+a_0^Tx+c_0,\qquad Q_0\succeq0,
 \qquad d(x)=d_x^Tx+d_c>0\quad(x\in F).
\]

The rational input has total length \(N\ge2\). The objective Hessian
\(Q_0\), whose rank is unrestricted, is excluded from the native common
range. Put

\[
 L_0=\bigcap_i\ker H_i,\qquad
 L=L_0\cap\ker d_x^T,\qquad
 r=\operatorname{codim}L\le\operatorname{codim}L_0+1.
\]

Assume the finite value \(\theta=\min_F q_0/d\) is attained. Its supplied
exact description has primitive irreducible integer polynomial degree
\(D\), coefficient bit length \(H\), and an isolating interval selecting
the intended real embedding of \(K=\mathbb Q(\theta)\).

Fix a rational invertible split \(x=T_1u+T_0v\), where
\(u\in\mathbb R^r\) and \(\operatorname{range}T_0=L\), obtained by
rational linear algebra with polynomial-bit entries. Define \(u^*\) as
the minimum-norm point of the projected optimal set. In its fiber, define
\(v^*\) as the minimum-norm optimal point. These choices exist and are
unique. They refer to these fixed coordinates, rather than the norm in
the original coordinates.

There are effective functions \(A,B\) and an absolute constant \(C\)
such that

\[
 \begin{split}
 [\mathbb Q(\theta,u^*,v^*):\mathbb Q]&\le A(r,D),\\
 K(u^*,v^*)&=K(u^*),\\
 \operatorname{heightbits}(u_j^*),
 \operatorname{heightbits}(v_j^*),
 \operatorname{heightbits}(x_j^*)&\le B(r,D)(N+H+1)^C.
 \end{split}                                                     \tag{1}
\]

Here heightbits means the maximum coefficient bit length of the primitive
integer minimal polynomial. The tuple \((\theta,u^*,v^*,x^*)\), and the
raw numerator gradient \(Q_0x^*+a_0\), has a common rational univariate
representation of total length bounded by the same form. A computable
rational box of that logarithmic size contains this selected point.
Section 6 strengthens the first line to \(D5^{2r}\), but this sharper
constant is unnecessary when \(D\) is already a parameter.

## 2. The projected optimal set is closed

After the split, the native constraints and numerator have the form

\[
 Cv\le b(u),\qquad d=d_0(u),\qquad
 q_0(u,v)=\tfrac12v^TAv+(Bu+b_0)^Tv+a(u),\quad A\succeq0.
                                                               \tag{2}
\]

The matrix \(C\) is constant rational, and the entries of \(b\) and
\(a\) are rational quadratics. All transformed data have polynomial bit
length. On any nonempty fiber, \(d_0(u)>0\) is fixed and
\(q_0(u,v)\ge\theta d_0(u)\), so the fiber numerator is bounded below.
A convex quadratic bounded below on a nonempty polyhedron attains its
minimum, including with singular Hessian and irrational right-hand sides.
The argument in [the optimization note, Section 2](common-range-optimization.md#2-a-parametric-convex-qp-projection)
also proves this real-data version directly.

Use the rational polynomial maps \(v_I(u)\) from
[the optimizer chart lemma](common-range-optimizer-witness.md#2-constant-matrix-quadratic-programming-charts).
Each has degree at most two and polynomial coefficient bit length. Every
nonempty fiber's minimum-norm numerator optimizer is represented by one
such map. Define

\[
 D_I=\{u:Cv_I(u)\le b(u)\},\qquad
 g_I(u)=q_0(u,v_I(u)),\qquad
 S_{I,\theta}=\{u\in D_I:g_I(u)\le\theta d_0(u)\}.       \tag{3}
\]

The sets \(D_I\) use quadratic rows, and \(g_I\) has degree at most
four. Each \(S_{I,\theta}\) is basic closed over \(K\), with at most
the original number of rows plus one. The finite chart family satisfies

\[
 U_\theta=\pi_u\bigl(F\cap\{q_0-\theta d\le0\}\bigr)
             =\bigcup_I S_{I,\theta}.                    \tag{4}
\]

For the forward inclusion, minimize the numerator in the given fiber and
use its minimum-norm optimizer chart. The reverse inclusion follows from
actual feasibility of \((u,v_I(u))\); no stationarity-consistency or
multiplier-sign guard is needed in (3). At the global minimum, every
point in (3) has equality in its last inequality.

Equation (4) proves closedness of the projection as a finite union of
closed sets. The original sublevel is convex because \(Q_0\succeq0\)
and \(d\) is affine. Its projection is therefore convex. Attainment makes
it nonempty, so it has a unique minimum-norm point \(u^*\). This argument
does not assume that an arbitrary projection of a closed convex set is
closed.

At \(u^*\), ratio optimization and numerator optimization in the fiber
are identical. Thus \(v^*\) is the minimum-norm numerator optimizer there.
Choose a chart \(I_*\) representing that particular point. Then

\[
 u^*\in S_{I_*,\theta}\subseteq U_\theta,\qquad
 v^*=v_{I_*}(u^*).                                      \tag{5}
\]

The point \(u^*\) is the unique minimum-norm point of this one chart set:
any competitor would also be a competitor in \(U_\theta\). The chart set
itself need not be convex. Selecting an arbitrary chart through \(u^*\)
would provide an optimizer, but need not provide \(v^*\).

## 3. A direct bound using classical quantifier elimination

Write \(P_\theta\) for the primitive minimal polynomial. There exists a
closed rational interval \([a,b]\) containing only its selected real
root, with endpoint bit lengths bounded by an absolute polynomial in
\(D+H\). This follows from integer-polynomial root separation and Cauchy's
root bound. For an existence bound, a needlessly long supplied isolator
can be replaced by this shorter one; reading the supplied input still
costs its actual length.

Put

\[
 \Phi_I(u,t)\ \Longleftrightarrow\quad
       u\in D_I\ \wedge\ g_I(u)-t d_0(u)\le0.
\]

For each \(j\le r\), the formula

\[
 \exists(u,t)\left[
 \begin{array}{l}
 P_\theta(t)=0,\quad a\le t\le b,\quad \Phi_{I_*}(u,t),\quad z=u_j,\\
 \forall w\,[\Phi_{I_*}(w,t)\Rightarrow\|u\|^2\le\|w\|^2]
 \end{array}\right]                                    \tag{6}
\]

defines exactly the singleton \(\{u_j^*\}\). It has one scalar free
variable, quantified blocks of dimensions \(r+1\) and \(r\), degree
at most \(\max(4,D)\), and integer coefficient bit lengths at most
\(B_0(D)(N+H+1)^{C_0}\) after clearing each row's denominators separately.
The constant \(C_0\) is absolute. Only this one chart appears in (6).

The coefficient-sensitive quantifier-elimination theorem gives output
degrees depending only on block dimensions and input degree, and output
coefficient bits at most the input bit bound times a function of those
same quantities. Neither bound depends on the number of predicates; the
running time and output count do. This is the well-behavedness condition
and Theorem 1.3.1 of
[Basu--Pollack--Roy (1996)](https://doi.org/10.1145/235809.235813), stated
explicitly in [Basu's survey, Theorem 2.27](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
Both local source statements were inspected for this review.

At least one nonzero output polynomial vanishes at \(u_j^*\). Otherwise
every nonzero predicate would have locally constant sign, contradicting
that (6) defines a singleton. It follows that each coordinate has an
integer annihilator of degree at most \(A_0(r,D)\) and coefficient bits
at most \(B_1(r,D)(N+H+1)^{C_1}\).

Multiplying coordinate-degree bounds across only the \(r\) retained
coordinates gives

\[
 [\mathbb Q(\theta,u^*):\mathbb Q]\le D A_0(r,D)^r.        \tag{7}
\]

This is a function of \((r,D)\). No degree multiplication over the
original \(n\) coordinates occurs. Weil-height bounds for roots of the
annihilators, followed by the identity between minimal-polynomial Mahler
measure and Weil height, give the same form of minimal-polynomial bit
bound. This step does not assume that taking a factor decreases the
maximum coefficient.

## 4. The fiber and gradient add no extension

Equation (5) immediately gives \(v^*\in K(u^*)^{n-r}\), because
\(v_{I_*}\) is a rational degree-two polynomial map. Its rational
coefficients have polynomial bit length. Evaluation of these maps and of
the rational coordinate transformation preserves a bound
\(B(r,D)(N+H+1)^C\) with absolute \(C\). The number of ambient
coordinates contributes only an absolute polynomial factor in \(N\).

The raw numerator gradient is constant on the entire optimal set. Indeed,
write \(h=q_0-\theta d\). If \(x,y\) are optimal, their segment is
feasible, \(h\ge0\) on \(F\), and convexity gives \(h\le0\) on that
segment. The midpoint identity therefore gives

\[
 0=h((x+y)/2)
   =\tfrac12h(x)+\tfrac12h(y)-\tfrac18(x-y)^TQ_0(x-y).
\]

Positive semidefiniteness implies \(Q_0(x-y)=0\). Hence
\(g^*=Q_0x^*+a_0\) is this common gradient and belongs to \(K(u^*)^n\),
with the same height form. The gradient of the ratio itself need not be
constant, since its denominator can vary along the optimal set.

For a common representation, choose a primitive integer linear combination
of \((\theta,u^*)\) separating its finitely many field embeddings. The
coefficient sizes depend only on its field degree. Height bounds give a
short minimal polynomial for this primitive element. Scale it and each
coordinate separately to algebraic integers, then solve the trace-pairing
linear system in its power basis. Cauchy bounds on conjugates and Cramer's
rule bound all rational coordinate coefficients by the stated form. The
details are recorded in
[the affine fractional field review, Section 6](fractional-common-range-field-review.md#6-one-short-representation-that-includes-theta).
This proves the common representation assertion in (1), including
\(\theta\) and \(g^*\). Cauchy bounds supply a rational containing box.

When \(r=0\), the numerator is a rational convex QP over a rational
polyhedron and the denominator is constant. Its minimum-norm optimizer is
one rational chart value directly. There is no low-dimensional elimination
step.

## 5. Uniform conditional boxes and the limit at nonoptimal thresholds

Fix integer variables of bit length at most \(M\). Substitution gives
rational continuous data of length bounded by an absolute polynomial in
\(N+M\). Assume the retained continuous dimension is uniformly at most
\(r\), and denominators remain positive on every relevant feasible
fiber. If \(\theta\) is the finite global mixed-integer infimum, then
every feasible continuous point in every integer fiber satisfies
\(q_0-\theta d\ge0\). Consequently, whenever that fiber's
\(\theta\)-sublevel is nonempty, it is exactly that fiber's nonempty
optimal set. The preceding bound gives one uniform conditional radius

\[
                  \log_2 R\le B(r,D)(N+M+H+1)^C.          \tag{8}
\]

No optimal integer assignment needs to be known in order to print this
bound. Empty sublevels require no witness. An integer-coordinate bound
and an algorithm deciding attainment remain separate inputs.

The same small-chart-witness conclusion holds for any nonempty algebraic
sublevel if the numerator is bounded below on every nonempty retained
fiber. Equation (4) then holds for that threshold, its projected sublevel
is closed and convex, and one may select the minimum-norm numerator
optimizer over its canonical \(u\). That selected point is a sublevel
witness. It need not minimize \(\|v\|\) over the entire sublevel fiber.

This distinction is necessary. For \(F=\mathbb R\), \(d=1\),
\(q_0(v)=(v-2)^2\), and the nonoptimal rational threshold \(2\), one
has \(r=0\), but the minimum-norm sublevel point is \(2-\sqrt2\).
It is not in \(K=\mathbb Q\). The numerator optimizer \(v=2\) is a
rational sublevel witness. Nonoptimal equality levels can also be
nonconvex: in this example equality gives the two points
\(2\pm\sqrt2\). These counterexamples do not affect (8), where
\(\theta\) is the global mixed-integer infimum.

## 6. Optional sharper relative-degree bound

The following extension of the
[finite-quotient argument over a number field](algebraic-coefficient-span-precision.md#3-the-finite-quotient-lemma-over-k)
was checked separately. It proves

\[
                [K(u^*):K]\le5^{2r},\qquad
                [\mathbb Q(\theta,x^*):\mathbb Q]\le D5^{2r}.
                                                               \tag{9}
\]

It is enough to work with the single set \(S_{I_*,\theta}\), whose
norm minimizer is unique. Write its degree-at-most-four rows as
\(P_j(u)\le0\). Perturb them by

\[
 F_{j,\varepsilon}=P_j+\varepsilon^2Q_j-\varepsilon,
 \qquad f_\varepsilon=\|u\|^2+\varepsilon Q_0,
                                                               \tag{10}
\]

where each constraint perturbation \(Q_j\) is a generic integer quartic
and the objective perturbation \(Q_0\) is a generic integer quadratic.
For small positive \(\varepsilon\), the objective is uniformly coercive,
\(u^*\) survives every constraint, and global perturbed minimizers exist.
Comparison with \(u^*\) bounds them uniformly. Every cluster point is a
norm minimizer of the original set, hence is \(u^*\). No box is needed.

For each selected set of \(s\le r\) rows, the generic bad loci exclude
dependent active gradients and singular full bordered KKT matrices;
for \(r+1\) rows they exclude a simultaneous zero. The mixed quartic and
quadratic degrees cause no genericity obstruction. In the universal KKT
incidence, solve the constraint constants from feasibility and the
objective linear coefficients from stationarity. This incidence is an
affine space of dimension equal to coefficient-space dimension. Its
bordered determinant is nonzero at
\(F_i=u_i\), \(f_0=\sum_{j>s}u_j^2\), \(u=\lambda=0\), where it equals
\((-1)^s2^{r-s}\). Thus singular KKT incidences have proper projected
closure. The analogous gradient-dependence incidence uses a projective
multiplier and has dimension one less than coefficient space. Standard
degree bounds for these incidences depend only on \(r\).

For fixed nonzero \(\varepsilon\), the coefficient changes in (10) are
surjective onto precisely these constraint and objective spaces. The
finite integer-grid argument over \(K\), as in
[the affine fractional field review, Section 3](fractional-common-range-field-review.md#3-one-low-dimensional-perturbation-over-k),
therefore chooses perturbation coefficient bits at most
\(A_1(r)+O(r\log(m+2))\), where \(m\) is the native row count. Only
finitely many nonzero \(\varepsilon\) then fail genericity. This grid is
used for existence, not enumerated.

Pass to a sequence with one fixed active set of size \(s\le r\).
Its full KKT equations have \(q=r+s\le2r\) root variables and total
degree at most four: a multiplier times a constraint derivative has
degree at most \(1+3=4\). Each selected root is nonsingular, although
its multipliers may diverge as \(\varepsilon\) tends to zero. The
finite-quotient lemma uses \(a=4\), hence quotient dimension
\(5^q\le5^{2r}\). Apply it with output any coordinate, and then any
rational linear combination of the coordinates of this same limiting
point. A primitive such combination gives (9).

For heights, take the joint local coefficient norm of only the selected
at-most-\(r\) rows and the objective. There are a number of coefficients
depending only on \(r\); each original coefficient is \(a+b\theta\)
with rational \(a,b\) of polynomial bit length. Their joint logarithmic
height is at most
\(A_2(r)(N^{C_2}+H+\log(D+1)+1)\). The finite-quotient determinant and
coefficient-extraction bounds preserve linear dependence on this quantity.
Conversion from Weil height to integer minimal-polynomial coefficient bits
then yields the same absolute-exponent height bound as (1).

This argument concerns affine roots and their limits. It does not assert
that a homogenized KKT system has no roots at infinity; that assertion
can fail because of multiplier directions at infinity. No such assertion
is needed for the finite-quotient deformation.

## 7. Verification and scope

The review reconstructed the chart choice, closedness, singleton formula,
common-field completion, gradient identity, and uniform conditional box.
The final read of [the quadratic fractional witness draft](common-range-quadratic-fractional-witness.md)
also checked its canonical-level statement and Section 6's boxed attainment
argument: the global infimum is a lower bound in every integer fiber, so
every nonempty level to which its conditional radius is applied is optimal.
An independent subreview checked the quartic-constraint and
quadratic-objective genericity calculation, coercivity, and the rational
selector alternative. The primary
[Jeronimo--Perrucci--Tsigaridas paper](https://arxiv.org/pdf/1112.0544)
was consulted for comparison: its polynomial-minimum and coordinate
arguments use deformation and low-dimensional elimination. The present
proof does not attribute the relative number-field statement (9) directly
to that paper.

The result assumes denominator positivity, an attained finite continuous
minimum for the canonical optimizer, and preservation of native SOC signs.
It does not bound the minimum-norm point in the original coordinates,
decide attainment, construct the implicit chart, or prove a new FPT
algorithm. The supplied value degree and height must be bounded separately
for an optimization theorem.

An inline `python -` command with SymPy checked the quartic chart
\(v=u^2\) for objective \(v^2\), the minimal polynomial of
\(2-\sqrt2\), and the raw-gradient distinction for
\(q_0(x,y)=x^2+y+1\), \(d=y+2\), on \(x=1,y\ge0\). The ratio there
is identically one, its raw numerator gradient is \((2,1)\), and its
ratio gradient is \((2/(y+2),0)\). The command also checked all 27
bordered determinants for \(1\le r\le6\), \(0\le s\le r\).
These checks passed and illustrate the arguments; they are not proofs of
the general theorem.

A targeted inline `python -` document check tested this file's local
links, paired math delimiters, final newline, control characters, and
trailing whitespace. It passed. Only these targeted checks were run;
project-wide verification and CI status or logs were not inspected.
