# Unbounded mixed-integer optimization at small common Hessian range

Date: 2026-09-28. Status: complete composition proof with an
[independent review](common-range-unbounded-optimization-review.md).
It combines two separately reviewed results from this research batch.
Publication priority is unestablished.

The objective-excluded common-range algorithm extends to integer variables
without supplied bounds. The additional ingredient is a coefficient-sensitive
bound for finite mixed-integer infima of convex semialgebraic epigraphs.
That bound includes unattained infima, so no rational recession direction or
attainment assumption is required.

## 1. Statement

Let \(C\subseteq\mathbb R^k\times\mathbb R^n\) be specified by
rational affine rows and either native jointly convex quadratic inequalities
or rational second-order cone inequalities. For a cone row use the squared
residual Hessian \(H_i\) and retain its affine right-hand-side sign.
Define

\[
 K_* = \{v\in\mathbb R^n:H_i(0,v)=0\text{ for every native row}\},
 \qquad \rho=n-\dim K_*.
\]

Consider a rational jointly convex quadratic objective

\[
 q_0(z,x)=\tfrac12(z,x)^TQ_0(z,x)+a_0^T(z,x)+c_0,
 \qquad Q_0\succeq0,
\]

whose Hessian is **excluded** from \(\rho\). Let \(N\ge2\) be the
explicit binary input length.

**Theorem.** An algorithm running in \(f(k,\rho)N^C\) bit operations,
for a computable \(f\) and absolute \(C\), classifies the mixed-integer
problem as infeasible, unbounded below, or having a finite infimum. It
returns the exact algebraic value of a finite infimum, decides attainment,
and returns an optimal integer assignment and an exact algebraic continuous
optimizer whenever the infimum is attained. A finite value has degree at
most \(f(k,\rho)\) and coefficient bit length at most
\(f(k,\rho)N^C\). In the attained case, some exact optimal point has
an algebraic representation of that size.

For native PSD constraint Hessians, \(\rho\) equals the common range
dimension \(r_x\) of the continuous Hessian blocks. For squared SOC
Hessians this equality can fail; the full-kernel condition above removes
integer-continuous cross terms. The theorem does not assert an analogous
unbounded result with only \(r_x\) for arbitrary SOC data.

## 2. The two inputs to the composition

[The objective-excluded common-range theorem](common-range-optimization.md)
provides the following, with absolute input exponents:

- Exact feasibility at every rational objective threshold in
  \(f(k,\rho)N^C\) time, without integer bounds.
- With a supplied integer box, exact value recovery, attainment
  classification, and optimal-point recovery in \(f(k,r_x)N^C\) time.
- An implicit quartic epigraph representation after eliminating the
  continuous directions in \(K_*\), as detailed below.

[The general convex semialgebraic value theorem](unbounded-misocp-multiple-integer-frontier.md),
Section 2.2, states the following. Let \(E\subseteq\mathbb R^k\times
\mathbb R\) be convex and upward closed in its last coordinate, described
by a quantifier-free Boolean formula with atom degree at most \(d\ge2\)
and individual coefficient bit length at most \(H\). The number of atoms
is unrestricted. If \(E\cap(\mathbb Z^k\times\mathbb R)\) is
nonempty, every finite last-coordinate infimum has degree at most
\(d^{G(k)}\) and coefficient bit length at most

\[
                       (H+1)d^{G(k)}.              \tag{1}
\]

If the infimum is attained, some optimal integer vector has the same type
of bit bound. Neither closedness nor attainment is assumed in the finite
value statement. The proof uses bounded rational linear forms on convex
sublevels and dimension reduction through rational affine integer lattices.
Its coefficient bound is linear in \(H+1\); a bound \(H^{G(k)}\)
would not suffice for the FPT conclusion here.

This general value theorem is a result of the present batch, not an
established result being attributed to Khachiyan--Porkolab. Its literature
comparison, proof, and independent reviews are in the linked note. Its
uses of lattice-free geometry, algebraic sampling, and the classical
integer-witness theorem are separately identified there.

## 3. A quartic epigraph with only \(\rho\) quantified variables

Choose rational coordinates \(x=T_1u+T_0v\), with
\(u\in\mathbb R^\rho\) and columns of \(T_0\) spanning \(K_*\).
Every native row has the form

\[
                         Cv+p(z,u)\le0,            \tag{2}
\]

with constant rational \(C\) and quadratic \(p\). The objective is a
convex QP in \(v\), with constant PSD quadratic matrix \(Q\), affine
linear coefficient in \((z,u)\), and a quadratic constant term.

First test the rational linear recession system

\[
                  Cd\le0,\quad Qd=0,\quad a_v^Td=-1.          \tag{3}
\]

Here \(a_v\) is its constant linear coefficient. Joint PSD of the full
objective makes all parameter cross terms vanish on \(\ker Q\). If
(3) is feasible, every nonempty \((z,u)\) fiber has objective tending
to \(-\infty\). Therefore native mixed-integer feasibility immediately
settles the entire problem: it is either infeasible or unbounded below.

Otherwise every nonempty fiber QP has a finite attained minimum. The
constant-matrix charts in the objective-excluded theorem give degree-two
rational maps \(v_I(z,u)\). Put

\[
 D_I(z,u):\ Cv_I(z,u)+p(z,u)\le0,
 \qquad g_I(z,u)=q_0(z,T_1u+T_0v_I(z,u)).
\]

The rows in \(D_I\) are quadratic and \(g_I\) is quartic. Every
retained chart point is feasible, and one chart contains the minimum-norm
optimizer of every fiber. Consequently the epigraph projection is exactly

\[
 E=\{(z,t):\exists u\in\mathbb R^\rho\
                \bigvee_I[D_I(z,u)\wedge g_I(z,u)\le t]\}.     \tag{4}
\]

The chart family may be exponential. Each atom has polynomial coefficient
bit length, uniformly over charts. This is a description used for bounds,
not a formula the algorithm generates. The set \(E\) is convex and
upward closed because it projects the original convex objective epigraph.

Classical coefficient-sensitive quantifier elimination gives a quantifier-free
description of (4) with

\[
                 d\le f(k,\rho),\qquad
                 H\le f(k,\rho)N^{C_0}.           \tag{5}
\]

Only the per-atom degree and height bounds are used; they are independent
of the number of chart predicates. With \(\rho=0\), no elimination
is needed. The primary Basu--Pollack--Roy theorem and its coefficient
statement are documented in the objective-excluded note. Applying (1) to
(5) proves the claimed FPT algebraic bounds on every finite mixed-integer
infimum, including one approached only through unbounded integer sequences.

## 4. Exact value and unboundedness classification

Check native mixed-integer feasibility first. If the problem is nonempty,
the bounds just proved give a computable \(M\) with
\(\operatorname{bit}M\le f(k,\rho)N^C\) exceeding the absolute
value of every possible finite infimum. Exact rational-threshold
feasibility at \(q_0\le-M-1\) is therefore equivalent to objective
unboundedness below.

In the finite case, bisection with the unbounded threshold oracle gives
certified numerical enclosures for the infimum \(\theta\). Algebraic
recognition with the established degree and height bounds returns its
minimal polynomial and an isolating interval in FPT time. Equality at an
unattained threshold yields a false query but still leaves a valid closed
enclosure when that threshold becomes the lower numerical endpoint.

The number of calls and the bit length of every rational threshold are
\(f(k,\rho)N^C\). Each threshold oracle has an absolute input exponent.
Composing these bounds therefore retains an absolute input exponent;
neither quantifier elimination nor chart enumeration is executed.

## 5. Attainment and exact optimal-point recovery

If the finite infimum is attained, the optimal integer projection

\[
 Y_*=\{z:\exists x\ ((z,x)\in C, q_0(z,x)\le\theta)\}
\]

is convex and contains an integer point. Add to (4) a variable selecting
\(\theta\) by its minimal polynomial and a closed rational isolating
interval. The degree, coefficient height, and quantified dimensions all
have bounds depending on \((k,\rho)\) times an absolute polynomial in
\(N\). The classical Khachiyan--Porkolab integer-witness theorem thus
gives a uniform box

\[
            z\in[-R_z,R_z]^k,\qquad
            \operatorname{bit}R_z\le f(k,\rho)N^C,             \tag{6}
\]

that contains an optimal assignment whenever one exists. Equivalently,
the attained-witness conclusion in Section 2.2 of the general value note
already supplies this bound. It is conditional on attainment; it does not
presume that an infimum is attained.

Print (6) and run the bounded-integer value and attainment algorithm on
the original problem with that box. If it is empty, the original infimum
is unattained. Otherwise let its finite infimum be \(\beta\). The
original infimum is attained exactly when this bounded-integer problem
attains \(\beta\) and \(\beta=\theta\). Indeed, the box retains
some optimizer if one exists, and any boxed optimizer at value \(\theta\)
is an original optimizer.

In the affirmative case, the same bounded-integer algorithm returns an
optimal integer assignment and a continuous algebraic optimizer. Its
parameter satisfies \(r_x\le\rho\), and the bit length of (6) has
the required FPT form. Hence its running time and complete output length
also have the form \(f(k,\rho)N^C\).

## 6. What the result adds and does not add

For \(\rho=0\) and native PSD quadratic rows, the continuous part of
each constraint is affine, while integer-only quadratic terms may remain.
For fully affine constraints, Del Pia's established mixed-integer convex
quadratic programming theorem already gives FPT in \(k\), including
arbitrary objective rank. The candidate extension permits arbitrarily many
nonlinear constraint rows sharing a small continuous curvature subspace.

There is a simple attainment boundary at \(\rho=0\), also for SOC
rows. If the global infimum is finite, every nonempty integer fiber has
an attained QP minimum equal to one of the rational polynomial values
\(g_I(z)\). A common multiple \(D\) of the coefficients' denominators
over the finite chart family puts all these values in \(D^{-1}\mathbb Z\).
A nonempty subset of that grid bounded below has a minimum. Thus the
global finite value is attained, and the selected chart gives a rational
continuous optimizer. No bound on the size of this global common
denominator is asserted or needed. This is a classical discreteness
consequence of the charts, not a separate algorithm or novelty claim.

The distinction from \(r_x=0\) is real. Minimize \(x\) subject to
\(z\in\mathbb Z\), \(z\ge1\), and
\(\|(2,z-x)\|_2\le z+x\). The cone is equivalent here to
\(zx\ge1\), so the infimum is zero and unattained. Its squared
residual is \(4-4zx\): the continuous Hessian block is zero, but
\(\rho=1\). This separates the two attainment statements; it is
not a hardness counterexample to a possible stronger FPT algorithm.

The [prior audit](common-range-optimization-prior.md) and the objective note explain
the established ingredients and nearby algorithms. The common-range
parameter is a stronger structural restriction than Hessian matrix span;
the FPT conclusion sharpens dependence on that parameter and does not
dominate all of the broader fixed-span results. No unsuccessful search
establishes novelty.

This theorem could support exact certification for conic mixed-integer
models with few nonlinear continuous aggregate features and a general
quadratic cost, without artificial variable bounds. It gives no practical
runtime, useful precision constants, small branch-and-bound trees, or
simple integer sequences witnessing nonattainment. The large parameter
factors and the unimplemented algebraic-recognition steps remain barriers
to practical use.

## Verification record

This is a composition of independently reviewed projection, exact-oracle,
algebraic-recognition, and semialgebraic value bounds. The separate
composition review found no substantive gap. It checked the
objective-excluded parameter, linear coefficient-height dependence,
conditional attainment box, exact-output interface, and zero-range
attainment boundary. Its conclusion depends on the stated theorem inputs;
it does not replace their proofs or establish novelty.

A targeted inline `python -` check passed for this note and the base
objective-excluded note: 14 local links, paired math delimiters, trailing
whitespace, control characters, and final newlines. No
mathematical script was rerun for this theorem composition, which changes
none of the previously checked matrix identities. No project-wide
verification or CI inspection was used.
