# Review of unbounded common-range mixed-integer optimization

Date: 2026-09-28. Scope:
[common-range-unbounded-optimization.md](common-range-unbounded-optimization.md).
This reviewer did not develop the general convex semialgebraic value
theorem or the present composition. The reviewer previously contributed
repairs to the objective-excluded threshold argument. That dependency
subsequently received a separate fresh review, including exact output.
This review checks the new composition and its parameter accounting; it
does not replace the independent reviews of the general value theorem.

**Finding.** No substantive gap was found in the composition. Conditional
on the stated general semialgebraic value theorem and the reviewed
objective-excluded algorithms, the result is a full exact optimization
algorithm in \(f(k,\rho)N^C\), with an absolute input exponent.
It covers finite unattained infima and returns an exact optimizer when
one exists. The distinction between \(\rho\) and the continuous-block
common range, and the linear dependence on coefficient bit length, are
essential. A display typo in the integer-box formula was reported and
corrected by the author.

## 1. Projection retains the claimed parameter

Let \(K_*\) be the continuous directions annihilated by every full
native squared-residual Hessian. A rational basis gives
\(x=T_1u+T_0v\), with \(u\in\mathbb R^\rho\).
For every native polynomial, its \(vv\), \(uv\), and \(zv\)
quadratic terms vanish. All affine rows and cone right-side signs remain
affine. Thus the full fiber has the form

\[
                     Cv+p(z,u)\le0
\]

with constant rational matrix \(C\). The coefficient bit bounds of
this coordinate change are polynomial in the explicit input length,
with an absolute exponent.

Only requiring \(v\) to lie in the kernel of each \(xx\) block
would leave \(zv\) terms and a matrix depending on \(z\). The
unbounded theorem correctly uses \(K_*\). With full PSD constraint
Hessians, zero quadratic energy on \((0,v)\) implies the full Hessian
annihilates that vector, so \(\rho=r_x\). For indefinite squared
SOC Hessians this implication is unavailable.

The objective is not included in this kernel. In transformed variables
its \(vv\) matrix is constant PSD, its linear \(v\) coefficient is
affine in \((z,u)\), and its remaining part is quadratic. Arbitrary
objective rank therefore does not add quantified coordinates.

## 2. The recession branch and the finite-fiber charts

Write \(Q\) for the objective's \(vv\) Hessian and \(a_v\)
for its constant linear coefficient. Global PSD of the objective gives

\[
 Qd=0\quad\Longrightarrow\quad
 Q_0(0,T_0d)=0.
\]

Consequently the objective change along \(v+\lambda d\) is
\(\lambda a_v^Td\), independently of \((z,u)\), when \(Qd=0\).
The normalized linear system

\[
             Cd\le0,\qquad Qd=0,\qquad a_v^Td=-1
\]

has a solution exactly when the unnormalized strict descent system does.
If it has a solution, every nonempty fiber is unbounded below. Native
mixed-integer feasibility then correctly distinguishes an empty problem
from an unbounded one. A cone's affine sign condition must be among the
rows of \(C\); the manuscript retains it.

If the system is empty, the polyhedral QP dichotomy gives a finite
attained minimum in each nonempty real fiber. The reviewed full-active-face
Moore--Penrose argument then supplies a quadratic polynomial map
\(v_I(z,u)\) containing the minimum-norm optimizer of each fiber for
at least one chart. This remains valid with singular objective Hessians,
singular KKT matrices, and zero active multipliers.

The chart is retained only where its original constraints hold. Thus
every retained point is feasible, even if a pseudoinverse was evaluated
at an inconsistent stationarity right-hand side. Conversely, a
threshold-feasible fiber has an attained fiber minimum and one chart
contains that minimum. These two directions prove the exact epigraph
identity in the manuscript. Each chart has quadratic constraints and a
quartic objective value; the existential block has dimension \(\rho\).

Failure of the recession test does **not** prove global boundedness.
For example, with unrestricted integer \(z\) and real \(v\), the
PSD objective \((v-z)^2-z\) has a finite minimum \(-z\) in each
fiber but global infimum minus infinity. The later rational-threshold
test, not the fiber test, handles this case. The manuscript makes the
required distinction.

## 3. Degree and coefficient bounds preserve FPT

The quartic epigraph has \(k+1\) free variables and \(\rho\)
quantified variables. Each atom has \(N^{C_0}\) coefficient bits
for an absolute \(C_0\). The chart count may be exponential.
The reviewed coefficient-sensitive Basu--Pollack--Roy statement yields
a quantifier-free description with

\[
       d\le F(k,\rho),\qquad
       H\le F(k,\rho)N^{C_0},
\]

independently of the number of atoms. Its running time is not being
used. When \(\rho=0\), the existing formula already has bounded
degree and requires no elimination.

Section 2.2 of
[the general value note](unbounded-misocp-multiple-integer-frontier.md)
then gives

\[
 \deg\theta\le d^{G(k)},\qquad
 \operatorname{bit}(P_\theta)\le(H+1)d^{G(k)}.
\]

Substitution gives parameter-only degree and coefficient bit bound
\(F_1(k,\rho)N^{C_0}\). The exponent \(G(k)\) applies to
\(d\), which already depends only on the parameters, not to \(N\)
or \(H\). Replacing the second bound by \(H^{G(k)}\) would not
justify the result. The general note explicitly proves the needed
linear-in-\(H+1\) form.

The epigraph is convex and upward closed because it is the projection
of the original convex objective epigraph. Individual quartic charts
need not be convex, and no argument applies the convex value theorem
to an individual chart. Closedness of the epigraph is not assumed.
Thus the general theorem's hypotheses hold in exactly the form used.

This review read the geometric descent and its coefficient accounting.
The correctness of that new general theorem remains a separate theorem
input with its own adversarial reviews; the composition is not another
proof of it. In particular, it is not being attributed to the classical
integer-witness theorem, whose optimized coordinate is integral.

## 4. Classification and exact values

After native feasibility is established, the polynomial coefficient bound
gives an effectively computable Cauchy bound \(M\) larger than the
absolute value of every finite infimum for this input. Feasibility at
\(q_0\le-M-1\) is equivalent to objective unboundedness. This uses
the integer problem's value bound and does not compare it with the
continuous relaxation.

In the finite case, exact rational-threshold decisions give nested
closed numerical enclosures. When a midpoint equals an unattained
infimum, the false threshold answer can set the lower endpoint to that
midpoint without excluding the infimum. Standard algebraic recognition
applies to the established degree and height bounds.

The required precision, number of calls, and rational threshold lengths
all have the form \(F_2(k,\rho)N^{C_1}\), with absolute \(C_1\).
An oracle cost \(F_3(k,\rho)L^{C_2}\), evaluated on input length
\(L\le F_2(k,\rho)N^{C_1}\), remains
\(F_4(k,\rho)N^{C_1C_2}\). Multiplying by the query count still
has an absolute input exponent. No exponentially large chart formula
or QE output is constructed in these steps.

## 5. Conditional integer bounds and attainment

For the recovered finite value \(\theta\), the real set

\[
 Y_*=\{z:\exists x\ ((z,x)\in C,\ q_0(z,x)\le\theta)\}
\]

is convex. It need not equal an optimal face of the continuous
relaxation, since that relaxation can have value below \(\theta\).
This is harmless: every *integer* vector in \(Y_*\) has a completion
of value exactly \(\theta\), by the definition of the mixed-integer
infimum. Integer nonemptiness of \(Y_*\) is therefore exactly
attainment.

Select \(\theta\) with its minimal polynomial and a closed rational
isolating interval. This introduces one additional quantified real
variable. Degree and quantified dimensions depend only on \((k,\rho)\);
coefficient bits remain \(F(k,\rho)N^C\). Root separation gives an
isolating interval with the same form of bit bound. The quantified
integer-witness theorem consequently gives an integer box with
\(F(k,\rho)N^C\) encoding length that contains an optimal integer
assignment whenever one exists. It is a conditional box, not a claim
that all good integer sequences remain bounded.

The bounded-integer algorithm can be applied to this box without
increasing its structural parameter: \(r_x\le\rho\), and added
integer bounds are affine. If the restricted problem is empty, global
attainment is impossible. Otherwise its infimum \(\beta\) is
finite, since it is at least the finite global infimum and the
restricted set is nonempty. Global attainment holds precisely when
\(\beta=\theta\) and the restricted problem attains \(\beta\).
Both conditions are necessary: equality of infima alone would not
exclude an unattained continuous fiber infimum.

When both hold, the reviewed bounded-integer algorithm returns an
optimal integer assignment and invokes the continuous exact optimizer
algorithm in that rational fiber. Its field-degree and height bounds
remain parameter controlled. The rational-matrix affine completion in
the dependency avoids an unsupported generic LP over algebraic
coefficient matrices. Reading the output dependency revealed no new
loss of parameter control in this final call. The integer box's bit
length only changes the explicit input size by another FPT factor.

For a useful boundary example, impose integer \(z\ge1\) and

\[
                  \|(2,z-t)\|\le z+t,
\]

and minimize the real variable \(t\). This is equivalent to
\(zt\ge1\) with the retained sign, and its finite infimum zero is
unattained. Each integer fiber attains \(1/z\). Here \(r_x=0\)
but \(\rho=1\), because the squared residual has a nonzero
integer-continuous cross block. The example checks both distinctions:
finite-fiber attainment does not imply global attainment, and the
continuous-block kernel cannot replace the full-kernel parameter in the
zero-range attainment statement below. It does not rule out a different
FPT algorithm using the smaller parameter.

## 6. The zero-range discreteness boundary

The author proposed the additional consequence that \(\rho=0\)
rules out a finite unattained infimum. The reviewer reconstructed the
argument independently and found it valid.

With no retained nonlinear continuous coordinates, every finite fiber
minimum is some rational-polynomial chart value \(g_I(z)\). There
are finitely many charts, and their coefficient denominators are
constant in the integer vector \(z\). A common multiple \(D\)
of all these denominators therefore puts every attained fiber minimum
in \(D^{-1}\mathbb Z\). A finite global infimum excludes the
unbounded-fiber branch. Hence the nonempty collection of fiber minima
is bounded below and belongs to one fixed discrete grid; it has a
minimum. This value is attained in one integer fiber. Its chart point
is rational, since \(v_I(z)\) is rational at integral \(z\).

This proves attainment and existence of a rational optimizer at
\(\rho=0\), without bounding the bit length of the common multiple
over the potentially exponential chart family. It is a supporting
discreteness argument, not a separate FPT construction or a novelty claim.

## 7. Significance and verification scope

The composition extends the reviewed objective-excluded common-range
algorithm to unbounded integer variables and continuous objective values.
Del Pia's FPT theorem already covers a PSD quadratic objective over a
mixed-integer polyhedron. The proposed extension permits native nonlinear
constraints while keeping the explicit-input exponent absolute under the
additional common-range parameter. Its strongest new dependency is the
general finite mixed-integer value bound, including nonattainment, whose
prior-art comparison must remain separate and qualified.

The conclusion does not provide useful numerical tolerances, an efficient
implementation, short integer escape sequences, or a small parameter
factor. Publication priority is not established by the composition or by
the available searches.

The review read the complete composition, the general value theorem and
geometric proof, the current objective-excluded optimization algorithm,
the minimum-norm chart proof, the exact-output construction, and its fresh
review. It also rechecked the theorem-level interfaces against the
previously inspected coefficient-sensitive QE, integer-witness, and
one-quadratic algorithm imports. Targeted document checks are recorded
below. No project-wide verification, CI inspection, or formal proof was
performed. Numerical examples would not independently verify the
semialgebraic value theorem or the composition's asymptotic bit bounds.

A targeted inline `python -` check of this review passed: final newline,
trailing whitespace, control characters, paired math-delimiter counts,
and both local links. The final manuscript's corrected box display and
added zero-range boundary paragraphs were reread directly. No mathematical
test script was rerun, because the new work is a theorem composition and
does not change the previously tested identities or recovery procedures.
