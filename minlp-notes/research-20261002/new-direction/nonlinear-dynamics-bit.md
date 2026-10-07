# Rational certificates and compressed trajectories for stable polynomial dynamics

Date: 2026-10-02. Status: independently checked precision extension of
[the stable nonlinear-dynamics theorem](nonlinear-dynamics.md).
The purpose is a Turing-model approximation algorithm,
not an expanded rational representation of every state in its trajectory.

## 1. Result and output contract

Consider the scalar dynamics and path factorization of the main note:

\[
 s_{t+1}=\phi_t(s_t,u_t),\quad t=0,\ldots,T-1,\qquad
 F=\sum_t a_t(s_t,u_t,s_{t+1}).
\]

Assume rational interval endpoints and rational polynomial maps and costs
of fixed numerical degree. Each map has two inputs and each cost has three.
Use the main note's box-invariance promise, contraction bound
\(|\partial_s\phi_t|\le a<1\), derivative bounds, and feasible-set
quadratic growth with constant \(g>0\). Supplied numerical bounds must be
valid; the algorithm does not discover or verify arbitrary stability,
invariance, or growth promises by itself.

The value of \(g\) need not be supplied. It is an instance-dependent rate
parameter in the proof. Section 8 gives an algorithm that searches grading
ratios under bit-operation budgets while using only the soundness-critical
bounds for its actual certificates.

There is a certified approximation algorithm with bit runtime polynomial in
the horizon, binary input size, the displayed conditioning parameters of the
main theorem, and \(\log(1/\varepsilon)\), at fixed local degree and
dimension. Its output consists of:

- Rational initial state and rational controls in their exact intervals.
- The original recurrence, which defines the exact feasible state trajectory
  from those rational inputs.
- Rational global lower and feasible-objective upper bounds whose difference
  is at most \(\varepsilon\).

The recurrence is part of the feasible-solution representation. The output
does **not** contain an expanded rational numerator and denominator for every
state. Certified state enclosures, at any requested finite precision, can
also be produced in polynomial bit work. This distinction is necessary:
repeated fixed-degree polynomial composition can make expanded rational state
values exponentially long.

The algorithm uses exact rational local LPs and exact rational gradients at
rational centers. It avoids arbitrary-real minimization or gradient oracles.
Only the repaired forward trajectory is evaluated through certified
enclosures. Every center coordinate is reset to controlled rational precision
before the next regridding stage.

## 2. Assumptions used for the bit claim

Write \(N=T\), \(p=3\), \(k=2\), and let \(s_0\) in constant formulas
denote the largest interval width, as in the main note. This width is distinct
from the initial-state variable. Let the rational input bounds include

\[
 |\partial_s\phi_t|\le a<1,\quad
 |\partial_u\phi_t|\le b,\quad
 \operatorname{Lip}(\nabla\phi_t)\le H,\quad
 \operatorname{Lip}(\nabla a_t)\le M.
\]

Choose a rational bound \(G_b\) on the magnitudes of all cost gradient
components on their full boxes. Such a bound can be obtained conservatively
from polynomial coefficients and interval magnitudes in polynomial bit work
at fixed degree. Put \(G=2G_b\). Then
\(|\partial_{s_j}F(c)|\le G\) for all ambient-box centers, including
infeasible ones.

Alternatively, the main note's bound \(G_{\rm feas}\) only on feasible
centers implies an ambient-box bound
\(G_{\rm feas}+2M\sqrt p\,s_0\), by comparing each of the at most two
incident bag gradients with any feasible point. A rational upper bound for
this expression suffices. Thus extending the allowable centers does not
introduce horizon dependence into this constant.

Conditioning includes \(1/(1-a)\), the objective first-derivative bound,
and the modified curvature used below. A bound using objective curvature
alone would omit the potentially large multipliers induced by affine
objective terms. The claim is polynomial in numerical conditioning
parameters, not uniformly polynomial in their binary encoding lengths.

If a rational growth lower bound is available, one can select a sufficient
grading ratio using rational arithmetic. With \(k=2,p=3,C_0=6\), replace
the main note's radical constants by

\[
 \overline L_q=1+a+b,\qquad
 \overline\rho=\frac{3(1+a+b)+(H/2)s_0}{1-a},\qquad
 \overline D=(3+2\overline\rho)^2.
\]

These dominate \(L_q,\rho,D\). Put
\(\overline M=M+GH/(1-a)\), and use \(\overline D\) in \(B_0,C\)
and the grading conditions. The condition involving
\(\sqrt{12}\,k\sqrt{\overline D}\,\overline M\theta\) can be
checked by squaring its nonnegative sides. Repeatedly halving a dyadic
\(\theta\) until all rational inequalities hold avoids algebraic-number
arithmetic and changes only the conservative conditioning constants.
Likewise, the analytical stopping-stage bound can be computed by comparing
\(gB_{\rm round}Ns_0^2 4^{-J}\) with \(\varepsilon\), and enclosure
mesh widths can always be selected by rational comparisons. Without a
supplied growth lower bound, Section 8 replaces this ratio selection; the
algorithm stops on its computed certificate gap rather than on \(J\).

## 3. Infeasible centers preserve the adjoint cancellation

At any rational ambient-box center \(c\), define

\[
 d_j=\partial_{s_j}F(c),\quad A_t=\partial_s\phi_t(c_{s_t},c_{u_t}),
\]

\[
 \mu_{T-1}=-d_T,\qquad
 \mu_{t-1}=A_t\mu_t-d_t\quad(t=T-1,\ldots,1).
\]

With \(q_t=s_{t+1}-\phi_t(s_t,u_t)\) and
\(G_c=F+\sum_t\mu_tq_t\), direct differentiation gives

\[
 \partial_{s_j}G_c(c)=0\quad(j=1,\ldots,T).
\]

This algebra uses no equality \(q(c)=0\). If \(x\) is a consistent
configuration representative and \(y\) is its exact forward repair, they
share the initial state and every control. Therefore

\[
 \nabla G_c(c)^T(x-y)=0.                                       \tag{1}
\]

The multiplier bound \(|\mu_t|\le U=G/(1-a)\) holds at these centers.
All identities and error estimates in Sections 4--5 of the main note
therefore remain valid with this ambient-box \(G\).

In particular, keep the original objective lower models and use the adjusted
gradients only for the separator slopes. The main configuration identity
retains its multiplier residual term \(-\sum_t\mu_tq_t(z^t)\).
If one instead constructs a Taylor model of a full multiplier-adjusted
function, its constant value includes \(\sum_t\mu_tq_t(c)\), which
must not be dropped at an infeasible center.

## 4. Rational affine models and exact local LPs

No preexisting objective-relaxation oracle is needed. For a bag box \(B\)
of width \(w_B\), with full midpoint \(m_B\), use

\[
 \underline a_{t,B}(z)=a_t(m_B)+\nabla a_t(m_B)^T(z-m_B)
                                  -Mp w_B^2/8.                 \tag{2}
\]

Taylor's bound gives

\[
 0\le a_t(z)-\underline a_{t,B}(z)\le Mp w_B^2/4.
\]

Thus the main note's uniform width-squared contract holds with \(A_0=pM\).
The affine minorant does not generally vanish in error at box vertices.
The regridding proof here uses validity and the displayed uniform error
bound only; no literal vertex-vanishing \(U^q\) property is asserted.

For the graph use the original affine Taylor strip: at the input midpoint,

\[
 \ell_{t,B}(s,u)=\phi_t(m)+\nabla\phi_t(m)^T((s,u)-m),
 \qquad |s'-\ell_{t,B}(s,u)|\le H w_B^2/4.                      \tag{3}
\]

All coefficients in (2)--(3) are rational. The exact nonlinear graph in
\(B\) lies in (3), and every point in the strip has graph residual at most
\(H w_B^2/2\), exactly as required by the main repair estimate.

After intersecting the leaf with its own separator cell, the local domain
has at most six coordinate-bound inequalities and two strip inequalities.
The objective (2) plus separator slopes is affine. Child-message intercepts
are constants and can be added after solving. Thus every local task is an
LP with at most three variables and eight inequalities.

It can be solved exactly by enumerating linearly independent triples of
active rows, solving the corresponding rational linear systems, checking
all inequalities exactly, and selecting the least objective. A nonempty
bounded polyhedron has a vertex; at a vertex the active rows span the
ambient variable space. Hence finding no feasible candidate proves emptiness.
One may first eliminate coordinates fixed by intersecting box bounds.
This handles touching faces, exact affine graphs when \(H=0\), and
zero-dimensional local domains without numerical feasibility tolerances.

There are at most \(\binom83=56\) candidate bases per unreduced task.
The main note's infeasibility flags and bottom-up message rules apply
unchanged. Exact rational backtracking gives a rational configuration and
rational controls and initial state for its forward repair.

## 5. Forward enclosure without expanding the trajectory

Let the rational initial state and controls obtained from backtracking be
fixed. Define the exact states semantically by the original recurrence.
Box invariance proves their feasibility.

At a forward step, suppose a certified interval for the exact current state
has rational midpoint \(m\) and radius \(r\). Evaluate
\(\phi_t(m,u_t)\) exactly as a rational number. The contraction bound
gives the next-state enclosure

\[
 [\phi_t(m,u_t)-ar,\ \phi_t(m,u_t)+ar].                          \tag{4}
\]

Round its endpoints outward to a dyadic mesh \(q>0\) and intersect with
the prescribed next-state interval. Intersection preserves containment by
box invariance. Its new radius obeys

\[
 r_{t+1}\le ar_t+q,\qquad r_0=0,
 \qquad r_t\le q/(1-a).                                       \tag{5}
\]

Ordinary natural interval evaluation of a polynomial is not a substitute
for (4): repeated occurrences of a state variable can inflate interval
widths even when the true derivative is bounded by \(a\).

Let \(m_t,r_t\) be the resulting state midpoints and radii. An objective
upper bound is the rational number

\[
 U_j=\sum_t a_t(m_t,u_t,m_{t+1})
                         +G_b\sum_t(r_t+r_{t+1}).               \tag{6}
\]

The same gradient bound gives

\[
 F(y_j)\le U_j\le F(y_j)+4G_bNq/(1-a).
\]

Fix any rational \(\omega>0\). Choosing
\(q\le\omega(1-a)h_j^2/(4\max\{1,G_b\})\) makes the upper-bound
error at most \(\omega Nh_j^2\). No independence between adjacent state
intervals is assumed; treating their uncertainties separately is a valid
upper bound.

## 6. Resetting the next center and its contraction

For the next stage, construct a rational center \(c_{j+1}\) approximating
the exact repaired trajectory \(y_j\), but not necessarily satisfying the
dynamics. Round **all** its coordinates, including continuous controls and
the initial state, to a prescribed dyadic mesh, then clip to their exact
intervals. Clipping cannot increase the distance from a feasible coordinate.

For example, also require \(q\le(1-a)h_{j+1}/4\) in (5), and round the
state midpoints and exact rational input coordinates to a dyadic mesh of
size at most \(h_{j+1}/2\). Their coordinate errors are then at most
\(h_{j+1}\), so

\[
 \|c_j-y_{j-1}\|^2\le pNh_j^2.                               \tag{7}
\]

The next center retains only these reset coordinates. The implicit feasible
incumbent retains its own rational controls and initial state separately.
Keeping exact LP coordinates in successive centers could otherwise create
a multiplying bit-length recurrence; resetting only dependent states is
insufficient.

Initialize at the rational box midpoint, whose bit length is \(O(I)\),
and use any implicit feasible reference trajectory for the proof. Since both lie in the box,
(7) holds at stage zero with \(h_0=s_0\). No exact expansion of that
initial trajectory is required.

Let \(C\) and the admissible grading ratio be those of the main theorem,
using \(G=2G_b\) and \(A_0=pM\). Its single-stage estimate now holds
at the possibly infeasible center:

\[
 F(y_j)-\operatorname{LB}_j\le(g/20)\|y_j-c_j\|^2+CNh_j^2.      \tag{8}
\]

Write \(e_j=\|y_j-x^*\|^2\). The three-vector inequality and (7) imply

\[
 \|y_j-c_j\|^2\le3(e_j+e_{j-1}+pNh_j^2).
\]

Since \(\operatorname{LB}_j\le f^*\), growth and (8) give

\[
 e_j\le\frac3{17}e_{j-1}
            +\frac{20C/g+3p}{17}Nh_j^2.                        \tag{9}
\]

Define

\[
 B_{\rm round}=\max\{p,\ 4(C+\omega)/g+3p/5\}.                \tag{10}
\]

Induction with \(h_{j-1}=2h_j\) gives
\(e_j\le B_{\rm round}Nh_j^2\). The initial error is at most
\(pNh_0^2\). The induction step closes because
\(12B_{\rm round}+20C/g+3p\le17B_{\rm round}\).

Maintain the least certified feasible upper bound (6). Adding its evaluation
error to (8), and using the distance bounds, gives

\[
 0\le\operatorname{UBD}-\operatorname{LB}_j
 \le[3gB_{\rm round}/4+3gp/20+C+\omega]Nh_j^2
 \le gB_{\rm round}Nh_j^2.                                    \tag{11}
\]

Thus the algorithm stops by

\[
 J=\max\{0,\lceil\log_2(s_0\sqrt{gB_{\rm round}N/\varepsilon})\rceil\}.
\]

No additional shrinkage of the original admissible \(\theta\) is needed.
The center-rounding argument retains a contraction factor \(3/17<1/4\).

## 7. Bit lengths and total work

Let \(I\) be the total binary input length, including rational bounds and
interval endpoints. Fix numerical polynomial degree and local dimension.
Let \(\theta=2^{-\mu}\), and use the fresh shell partitions of the main
theorem at \(h_j=s_0 2^{-j}\).

The reset centers have coordinate bit lengths \(O(I+j)\): each coordinate
is a prescribed dyadic rational or a clipped input endpoint. Fresh shell
endpoints have bit lengths \(O(I+j+\mu)\). They do not inherit the
previous local LP's arbitrary denominators.

Set \(B_j=O(I+j+\mu+\log(T+1))\). At rational points of this size,
fixed-degree, fixed-arity polynomial values and derivatives have
\(O(B_j)\)-bit rational representations. The backward adjoint recurrence
is affine in each previously computed multiplier, so bit lengths grow
additively across its \(T\) steps, giving \(O(TB_j)\) bits. This is
different from nonlinear forward composition.

The coefficients of each three-dimensional LP have polynomial bit length,
and its vertex determinants have polynomial bit length. The conservative
bound \(O(TB_j)\) suffices for local points and nonconstant local values.
Every DP message is a sum of at most \(T\) chosen local contributions;
taking minima selects such a sum. Messages are never multiplied by one
another. Reducing rational arithmetic therefore gives the conservative
message-size bound \(O(T^2B_j)\), independent of the number of grid tasks.

Forward enclosure uses a dyadic precision with

\[
 \log(1/q)=O\bigl(I+j+\log(1+G_b)+\log(1/(1-a))
                                      +\log(1+1/\omega)\bigr),
\]

with harmless positive-part conventions when a quantity exceeds one.
These scale terms already have polynomial binary encodings in the supplied
input. Exact polynomial evaluation followed by outward dyadic rounding
keeps all interval endpoints at this prescribed size. Objective sums in
(6) have polynomial bit length as well.

The main shell-incidence count gives
\(O(N3^w(4/\theta)^p(J+1)^3)\) local tasks, with \(p=3\).
Each now requires a constant number of rational LP basis solves and
polynomial-bit arithmetic. Gradient, adjoint, enclosure, and center-reset
work is polynomial in the same quantities. Therefore total bit runtime is

\[
 N(4/\theta)^3(J+1)^3\,
                  \operatorname{poly}(T,I,J,\mu),               \tag{12}
\]

where degree and local dimensions are fixed and the supplied scale bounds
are counted in \(I\). The admissible reciprocal grading ratio is polynomial
in the conditioning constants displayed in the main theorem; \(J\) depends
logarithmically on their scale and on \(1/\varepsilon\). This establishes
the stated conditioned Turing approximation theorem.

Exact LP basis enumeration also supplies a concrete way to check local lower
bounds and infeasibility. A checker verifies rational controls and initial
state, runs the enclosure recurrence for the upper bound, and checks the
finite lower-certificate recurrences. It must trust or separately verify the
supplied global derivative bounds and box-invariance assertion. The final
leaf-plus-cell count remains that of the main theorem; a full serialized
proof includes numeric entries and local checks, all covered by the
polynomial work bound rather than by the bare box count alone.

## 8. Unknown growth constants and bit-budget search

The validity of every stage is independent of the growth constant and of
whether its grading ratio satisfies the convergence inequalities. Objective
minorants require the valid supplied \(M\); graph strips require \(H\).
Forward enclosures require the valid contraction bound \(a<1\), and
feasibility of the implicit repaired trajectory requires box invariance.
The objective upper bound uses \(G_b\). These soundness-critical promises
and bounds are not guessed. In contrast, \(g\) is used only in the rate
analysis.

Define trial \(\mu\ge1\) to run ratio \(\theta=2^{-\mu}\), starting
from the same rational box midpoint, through stages \(j=0,1,\ldots\).
It uses the rational Taylor LPs, exact adjoints, enclosure accuracy, and
center reset already specified. These computations use the known input
bounds, \(\omega\), and \(h_j\), but never \(g,C,B_{\rm round}\), or
the analytical stopping-stage bound. A trial stops only when its rational
upper and lower bounds differ by at most \(\varepsilon\).

For rounds \(r=1,2,\ldots\), restart each trial \(1\le\mu\le r\)
with a budget of \(2^r\) actual bit operations. Abort a trial before it
performs an operation exceeding the budget. Count all its setup, grid
generation, arithmetic, control logic, and output work inside this budget;
there is no unbudgeted preprocessing specific to the trial. There is no
separate stage cap. A time-bounded execution of the bit-level algorithm
implements this schedule even when interruption occurs within a rational
arithmetic routine.

Let \(\mu^*\) be any first sufficient dyadic ratio index, and let
\(W^*\ge1\) bound the bit work of its successful unbudgeted trial. The
preceding theorem makes \(W^*\) polynomial in horizon, input size,
conditioning, and \(\log(1/\varepsilon)\). The admissible ratio bounds
also make \(2^{\mu^*}\) polynomial in the conditioning parameters.
Every round

\[
 r^*\ge\max\{\mu^*,\lceil\log_2W^*\rceil\}
\]

contains and finishes that trial unless another trial has already returned
a valid certificate. Total simulated bit work through that round is at most

\[
 \sum_{r=1}^{r^*}r2^r\le2r^*2^{r^*}.
\]

Thus the unknown-growth algorithm has polynomial bit complexity in the same
parameters. The displayed allocation has a logarithmic scheduling overhead
relative to \(\max\{W^*,2^{\mu^*}\}\); budget counters and the
time-bounded simulation add at most a polynomial logarithmic overhead.
This is not a procedure for proving growth
or estimating its best constant. It is a sound certificate algorithm whose
termination and rate follow whenever the assumed positive growth constant
exists.

## 9. Limits and verification

Arbitrary convex or transcendental input oracles are outside this bit theorem.
Numerical degree must be fixed or otherwise included in arithmetic costs;
binary encoding of unbounded exponents is insufficient. Additional endpoint
or state constraints need a separate repair-invariance argument. Ordinary
floating-point feasibility tolerances are not substituted for the exact
rational LP and compressed-trajectory semantics.

The result depends on stability, feasible quadratic growth, and objective
first-derivative bounds. It does not contradict the width-two affine
constraint barrier. That reduction imposes a terminal target on its running
sum; forward repair from arbitrary retained controls need not meet that
target. It is therefore outside the box-invariant model considered here,
which permits every choice of initial state and controls in their prescribed
intervals. No claim is made that the required constants are easy to establish
on a general model.

A [fresh Astra review](../reviews/nonlinear-dynamics-bit-review.md)
independently checked arbitrary-center cancellation,
the need for contraction-aware interval propagation, complete coordinate
resetting, and polynomial adjoint/LP bit growth. It then checked the written
rounded-center constants, initialization, LP feasibility logic, and full bit
statement; no mathematical blocker was found. Its exact-rational inline
checks passed 80 cancellation and forward-enclosure cases at horizons
1, 2, 5, and 11; six degenerate LP cases; 27 choices of contraction constants;
and 81 dyadic-rounding and rational-clipping cases. It also checked the
written unknown-growth schedule and passed 144 exact schedule-arithmetic
cases. These were targeted
`python` checks, not a full solver implementation or performance study.
The two implementation clarifications it requested—an input-sized initial
center and all-rational bounds for radical constants—were applied.
No project-wide or CI verification was run.
