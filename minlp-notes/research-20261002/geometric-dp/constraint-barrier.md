# Why local affine constraints change the problem

Date: 2026-10-02. Status: complete supporting reduction, independently
checked. This uses the standard SUBSET SUM encoding. It is a
limitation of the proposed product-domain extension, not a claim of a new
hardness mechanism or strong NP-hardness.

## Claim and scope

The geometric-grid theorem cannot extend to arbitrary local affine
constraints with runtime polynomial in binary input size, the ratio
\(L/c\), and \(\log(1/\varepsilon)\), even at treewidth two, unless
\(\mathrm P=\mathrm{NP}\).

This remains true for nonempty mixed binary/continuous problems with all
variables in \([0,1]\), affine objective and constraints, a unique global
optimizer, and the explicit global quadratic-growth constant
\(c=1/(2n+3)\). The upper coordinate-curvature bound may be supplied as
\(L=1\), so \(L/c=O(n)\). Objective coefficients have polynomial binary
encoding length but exponential magnitude. That distinction matters.

## Construction

Start with SUBSET SUM data consisting of positive integers
\(a_1,\ldots,a_n\) and target \(B>0\). Assume \(a_i\le B\); larger
items cannot participate and can be removed. Add a dummy item \(a_0=B\).

Use binary variables \(x_0,\ldots,x_n\) and continuous running sums
\(y_0,\ldots,y_{n+1}\in[0,1]\). Impose

\[
 y_0=0,\qquad y_{n+1}=1,\qquad
 y_{i+1}=y_i+(a_i/B)x_i\quad(i=0,\ldots,n).                       \tag{1}
\]

Minimize

\[
 F(x,y)=2^{n+1}x_0+\sum_{i=1}^n2^{i-1}x_i.                      \tag{2}
\]

Every constraint in (1) belongs to bag
\(V_i=\{y_i,x_i,y_{i+1}\}\). In the path
\(V_0,V_1,\ldots,V_n\), successive bags intersect in the one variable
\(y_{i+1}\). Each running-sum variable belongs to at most two bags, and
each binary variable to one. This is a supplied tree decomposition of width
at most two. Fixing the two endpoint running sums can only reduce its width.

The instance has polynomial binary encoding length. In (1), the nonconstant
coefficients have magnitude at most one and rational encodings of size
\(O(\log B)\). The largest objective coefficient has \(n+2\) bits, and
all objective coefficients together have \(O(n^2)\) bits.

## Feasibility and what the optimum decides

Summing (1) gives

\[
 Bx_0+\sum_{i=1}^n a_i x_i=B.                                   \tag{3}
\]

The dummy selection \(x_0=1\), \(x_i=0\) for \(i\ge1\) is always
feasible: its running sums are zero initially and one thereafter. Positivity
of the real item weights implies that it is the only feasible selection
with \(x_0=1\).

A selection with \(x_0=0\) is feasible exactly when its real items solve
the original SUBSET SUM instance. For any such selection, the successive
partial sums lie between zero and the final total \(B\), because the
weights are positive. Thus the running-sum bounds in (1) exclude no genuine
subset solution, regardless of item order.

The dummy objective is \(2^{n+1}\). Every real-item selection has objective
at most \(2^n-1\). Consequently the optimum selects a real subset if and
only if the SUBSET SUM answer is yes.

For every binary selection the equalities determine \(y\) uniquely. The
binary positional weights in (2) assign distinct integer values to distinct
real-item selections; the dummy value is distinct from all of them. Hence
every feasible point has a distinct integer objective value, and the global
optimizer \(z^*=(x^*,y^*)\) is unique.

## Curvature and global quadratic growth

The full vector \(z=(x,y)\), including fixed endpoint coordinates, has
\(2n+3\) coordinates in \([0,1]\). Thus

\[
 \|z-z^*\|_2^2\le2n+3.
\]

At any feasible point other than \(z^*\), distinct integral objective
values give \(F(z)-F(z^*)\ge1\). At the optimizer both sides below vanish.
Therefore the explicit global bound is

\[
 F(z)-F(z^*)\ge\frac{1}{2n+3}\|z-z^*\|_2^2
       \qquad\text{for every feasible }z.                       \tag{4}
\]

The continuous extension of (2) is affine. Every second derivative is zero,
so its upper coordinate curvature is zero; the supplied positive upper bound
\(L=1\) is valid. Thus (4) has \(L/c=2n+3\), polynomial in the instance
size. The curvature and growth constants need not be discovered by a solver:
the reduction supplies them.

The same construction also defeats the more permissive hybrid interpretation
in which the binary variables are fully enumerated and growth is required
only in the gridded continuous variables. Inequality (4) implies
\(F(x,y)-f^*\ge\|y-y^*\|^2/(2n+3)\). Each bag has only one binary state
variable of domain size two. The obstruction comes from the affine coupling
constraints, not from compressing a large integer domain or requiring growth
in a metric on the discrete states.

## Complexity consequence

An algorithm returning a feasible point within absolute error
\(\varepsilon=1/4\) must return the exact optimal feasible point here:
all suboptimal feasible values exceed the optimum by at least one. Reading
its \(x_0\) decides SUBSET SUM. An approximate optimal value with a certified
absolute error of \(1/4\) also distinguishes the cases, because every yes
instance has value at most \(2^n-1\), while every no instance has value
\(2^{n+1}\).

Accordingly, a runtime polynomial in input size, \(L/c\), and
\(\log(1/\varepsilon)\) at this fixed width would solve SUBSET SUM in
polynomial time. The example rules out that general extension unless
\(\mathrm P=\mathrm{NP}\).

## What this does and does not explain

The product-domain proof independently rounds coordinates while preserving
their means. Here independently rounding running sums and binary selections
generally violates (1). Small treewidth and quadratic growth do not repair
that loss of feasibility. A constrained extension therefore needs additional
structure, a valid constrained-rounding argument, or a complexity parameter
that becomes large on this family.

This is a weak NP-hardness reduction from SUBSET SUM. It does not exclude
pseudopolynomial algorithms in \(B\); the usual subset-sum dynamic program
has that kind of dependence. Bounds on coefficient *magnitudes* do not
remove the precision carried by the normalized rational weights \(a_i/B\).

The objective coefficients and gradient magnitudes are exponentially large.
Their binary encodings are short, and upper curvature is still zero. Thus
the reduction specifically excludes a bound that omits such magnitudes or
counts only their binary encoding lengths. It does not exclude bounds that
depend polynomially on objective coefficient magnitudes, gradient magnitudes,
inverse numerical separations, or other quantities exponential on this
family. Normalizing (2) to bounded coefficients correspondingly scales down
the objective gap, the supplied growth constant, and the absolute accuracy
needed to distinguish the two cases.

No claim is made that this reduction is original. Its purpose is to record
precisely why the product-domain hypothesis cannot simply be removed from
the proposed algorithmic theorem.

## Targeted verification

An independent agent checked the reduction, encoding lengths, full and
projected growth bounds, and the stated limitations. A standalone inline
Python command, `python3 - <<'PY'`, enumerated all item lists with one through
four items and targets one through five, taking each item in `1,...,B`.
Using exact rational arithmetic, it checked feasibility, uniqueness of
objective values, the decision equivalence, and (4) on every feasible
selection. All 1,274 instances passed. The same command checked this note
for unexpected control characters. No project-wide or CI checks were run.
