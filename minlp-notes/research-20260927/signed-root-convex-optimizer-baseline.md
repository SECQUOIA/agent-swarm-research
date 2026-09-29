# A compact convex optimizer representation of certified root circuits

Date: 2026-09-28. Status: elementary baseline independently verified in
[the proof review](signed-root-convex-optimizer-review.md).
This is a scope comparison, not a novelty claim.

The [signed odd-root construction](signed-odd-root-circuit-quartic.md)
produces a unique feasible zero of one strongly convex quartic. Merely
representing the same values as the unique optimizer of a compact convex
program is easier. This note proves that distinction explicitly, even
with signed coefficients and access to predecessor powers.

Use the positive normalized root boxes and notation of that construction.
For each gate take variables \(X_i\) and \(Y_{i,e}\),
\(2\leq e\leq n_i\), with \(Y_{i,1}=X_i\). Impose their rational
boxes \(X_i\in[L_i,U_i]\) and
\(Y_{i,e}\in[L_i^e,U_i^e]\), and the inequalities

\[
 X_i^{d_i}\leq c_i+\sum_{j<i,e}a_{ije}Y_{j,e},
 \qquad X_i^e\leq Y_{i,e}\quad(2\leq e\leq n_i).
 \tag{1}
\]

These define a compact convex set. The powers are convex on the positive
boxes, and the radicands are affine in the optimization variables.
Their coefficients may have either sign. The input interval certificate
makes every radicand lie between \(L_i^{d_i}\) and \(U_i^{d_i}\)
for all preceding variables in their boxes. This remains valid when the
power variables do not equal the actual powers: interval evaluation used
their independent power boxes from the beginning.

Order the variables by gate, placing \(X_i\) first and then its
power variables. Orient each root variable positively and each power
variable negatively. Thus \(y_t=X_i\) or \(y_t=-Y_{i,e}\).
There are \(N\) variables, and the constraints have triangular form

\[
                    y_t\leq g_t(y_1,\ldots,y_{t-1})
 \tag{2}
\]

together with boxes. For a root, \(g_t\) is the positive odd root
of its affine radicand. For a power, it is \(-X_i^e\).
Every boundary value in (2) lies in its own box for every preceding
boxed prefix. Every feasible prefix can consequently be extended by
setting the following variables to these boundary values.

The recursive all-boundary point \(y^*\) is exactly the desired
circuit and its powers. It is a lexicographic maximum in this ordering,
but the following estimate replaces a lexicographic objective by one
ordinary rational linear objective.

## A finite weighted objective

Suppose more generally that each triangular boundary satisfies

\[
 |g_t(u)-g_t(v)|\leq C\sum_{j<t}|u_j-v_j|
 \tag{3}
\]

on its predecessor box, for some rational \(C\geq1\). For the
root circuit, \(C=NA^N\) suffices: the normalized radicands are at
least one, and the coordinate derivative of an odd root of an affine
radicand is bounded by the corresponding coefficient magnitude. The
power derivatives are at most \(eA^{e-1}\).

Set

\[
 B=2(C+1),\qquad W_t=B^{N-t}.
 \tag{4}
\]

Then \(y^*\) uniquely maximizes \(\sum_tW_ty_t\) over (2) and
the boxes. To prove this, take any feasible \(y\), and put

\[
 \delta_t=g_t(y_{<t})-y_t\geq0,
 \qquad e_t=y_t^*-y_t.
\]

The exact recursion and (3) imply

\[
 e_t=\delta_t+g_t(y_{<t}^*)-g_t(y_{<t}),
 \qquad |e_t|\leq\delta_t+C\sum_{j<t}|e_j|.
\]

Inductively,
\(\sum_{j<t}|e_j|\leq\sum_{j<t}(1+C)^{t-j-1}\delta_j\).
Therefore

\[
\begin{aligned}
 \sum_tW_te_t
 &\geq\sum_j\delta_j
       \left[W_j-C\sum_{t>j}W_t(1+C)^{t-j-1}\right]\\
 &\geq\frac1{C+1}\sum_jW_j\delta_j.
 \tag{5}
\end{aligned}
\]

For the last inequality divide the sum in brackets by \(W_j\)
and bound its geometric series by
\(C/[B-(C+1)]=C/(C+1)\). If every slack is zero, triangular
recursion forces \(y=y^*\). Otherwise the right side of (5) is
strictly positive. This proves uniqueness.

The weights have polynomial bit length because
\(\log W_t\leq N\log(2(C+1))\), and \(\log C\) is polynomial
in the certified circuit input. The compact convex polynomial program
(1) with the linear objective consequently has polynomial size and the
desired unique optimizer.

## What this comparison does and does not establish

The quartic realization adds an exact feasible singleton, uniform global
curvature, fixed polynomial degree, and explicit rational SOS and Hessian
certificates. The elementary optimizer representation above does not
supply those properties. Conversely, the quartic result should not be
described as the first way to place these circuit values in a compact
convex optimization model.

The proof gives a reduction, not a polynomial-time exact optimization
algorithm. A rational linear objective can have an irrational optimum,
and exact comparison remains an arithmetic issue. No PosSLP hardness,
NP-hardness, or novelty statement follows here. Nor is this a formulation
for arbitrary signed arithmetic circuits: the independently checkable
interval bounds and restricted root/power gate model are still required.

This is an elementary mathematical derivation. No numerical experiment
is needed for its universal weighted-recursion inequality. The independent
review reconstructed the inequality and checked the input model and
polynomial bit-size claim.
