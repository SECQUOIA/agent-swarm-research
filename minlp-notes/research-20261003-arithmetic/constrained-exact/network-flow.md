# Exact arithmetic for separable strongly convex polynomial flows

Date: 2026-10-03. Status: proof supplied and independently reviewed; see
[network-flow-review.md](network-flow-review.md). Publication priority is not established.

**Result.** Exact value, coordinate, and fixed-degree polynomial-observable
comparison for a separable globally strongly convex quartic over a rational
network-flow polyhedron belongs to deterministic
\(\mathrm P^{\mathrm{PosSLP}}\). The graph, dimension, and constraint rank
are unrestricted. No lower bound on a nonzero optimal slack or multiplier is
assumed. The reduction uses polynomially many adaptive oracle calls, not one
many-one PosSLP instance.

This supplies one concrete extension beyond the low-constraint-rank result.
It does not resolve exact quartic comparison over arbitrary polyhedra.

## 1. Input and output

Let \(G=(V,E)\) be a directed graph, let \(A\) be its node-arc
incidence matrix, and let
\[
 P=\{x\in\mathbb R^E:Ax=b,\ \ell\le x\le u\}.
\]
The balance vector and finite capacity endpoints are rational. Endpoints
may also be infinite. Sections 2--4 initially assume finite endpoints;
Section 5 gives the polynomial-time reduction of the general case to that
case.
Parallel arcs, redundant node-balance equations, fixed arcs, and
lower-dimensional feasible sets are allowed. Let
\[
 f(x)=\sum_{e\in E}f_e(x_e),\qquad f_e\in\mathbb Q[t],
 \qquad \deg f_e\le4.
\]
The input supplies a rational \(\mu>0\) with the promise
\[
                  f_e''(t)\ge\mu\quad(t\in\mathbb R,e\in E).
\]
These univariate quadratic inequalities can also be verified in rational
polynomial time: a nonconstant quadratic \(at^2+bt+c\) is nonnegative
on the line exactly when \(a>0\) and \(4ac-b^2\ge0\), while the
constant case is immediate. Apply this test to \(f_e''-\mu\), treating
negative leading coefficient and nonconstant linear cases as invalid.
Thus supplied curvature can be checked here; no multivariate convexity
recognition promise is hidden in the graph structure.

When \(P\ne\varnothing\), coercivity, closedness, and strong convexity
give a unique minimizer \(p\). For any supplied rational polynomial \(h\) of fixed
degree, each of the six comparisons of \(h(p)\) with zero is decidable in
\(\mathrm P^{\mathrm{PosSLP}}\). Value and coordinate comparisons use
\(h=f-r\) and \(h=x_e-r\). Rational flow feasibility is checked first;
an empty feasible set is handled before any optimizer predicate. For value
comparisons one may use the convention \(\min\varnothing=+\infty\).

All polynomials use explicit rational coefficients. The total input length
includes the graph, bounds, balance vector, curvature bound, and observable.
The degree of \(h\) is fixed independently of the input dimension.

## 2. Exact quadratic flow solves with rational-circuit data

The following source dependency is the only special graph algorithm needed.
Végh's [2016 paper](https://doi.org/10.1137/140978296),
[author PDF](https://personal.lse.ac.uk/veghl/papers/vegh-quadratic.pdf),
Theorem 20 on printed page 1753, gives an exact strongly polynomial
algorithm for separable convex quadratic minimum-cost flow. For capacitated
instances it uses \(O(m^4\log m)\) elementary operations, where
\(m=|E|\). The computational model on page 1729 permits addition,
subtraction, multiplication, division, and comparisons. Section 2 on page
1735 reduces lower and upper capacities to nonnegative flows by adding one
node and one extra arc per original arc; auxiliary arcs may have zero cost.
Section 6.1, including the discussion immediately after Theorem 20, verifies
the quadratic implementation using rational linear systems and rational
parametric search. No root-extraction or integer-rounding oracle is needed. The
[independent review](network-flow-review.md) also supplies an explicit
rational-circuit bound for the source's high artificial-arc costs, so this
normalization does not inspect expanded coefficient encodings.

Consequently this algorithm can be simulated when its rational quadratic
coefficients are represented by shared arithmetic circuits. Keep every
computed number as a circuit. Simulate a numerical comparison by a PosSLP
query after converting rational circuits to integer numerator-denominator
circuits. Every permitted arithmetic operation adds only constantly many
gates. If equality is needed, use two strict comparisons. Every division
is defined along the source algorithm's valid execution path. A convenient
division rule preserving a positive denominator is
\[
 \frac{N_1/D_1}{N_2/D_2}
       =\frac{N_1D_2N_2}{D_1N_2^2}\quad(N_2\ne0).
\]
The operation count depends on graph size, not the expanded bit lengths of
the circuit values. Hence an exact quadratic-flow solve takes polynomial
time with a PosSLP oracle and returns shared rational circuits of polynomial
size. The ordinary bit-length guarantee in the source is not being used to
claim that the expanded outputs have polynomially many bits here.

The source's differential oracle is elementary for a quadratic arc cost:
the derivative of \(a_et^2+c_et\) is \(2a_et+c_e\). Its remaining
quadratic subroutines are covered by the inspected arithmetic model.
Feasibility is already known for each quadratic call below. A harmless
constant in an arc cost can be discarded.

## 3. Constrained Newton refinement

Use the [quadratic-subproblem transfer theorem](structural-newton.md).
For completeness, its decisive estimate and the graph specialization are
given here. At a feasible rational point \(x\), define
\[
 N(x)=\mathop{\rm argmin}_{y\in P}
 \left\{\nabla f(x)^T(y-x)
       +\tfrac12(y-x)^T\nabla^2f(x)(y-x)\right\}.
\]
The Hessian is diagonal. Omitting a constant, this subproblem has arc costs
\[
 q_{e,x}(y_e)
 =\tfrac12 f_e''(x_e)y_e^2
  +\bigl(f_e'(x_e)-f_e''(x_e)x_e\bigr)y_e.
\]
Every quadratic coefficient is positive, and its representation has only
constantly many new gates per arc. Thus Section 2 computes \(N(x)\)
exactly with polynomially many arithmetic gates and PosSLP calls.

Let \(M\) bound the Hessian Lipschitz constant on \(P\), and let
\(K=\max\{1,M/(2\mu)\}\). Such a rational \(M\) has polynomial
bit length: each third derivative is affine, and the supplied box bounds
control its magnitude. The constrained first-order conditions at
\(p\) and \(N(x)\), together with \(\nabla^2f(x)\succeq\mu I\),
give
\[
 \|N(x)-p\|\le\frac1\mu
   \|\nabla f(x)+\nabla^2f(x)(p-x)-\nabla f(p)\|
 \le\frac M{2\mu}\|x-p\|^2
 \le K\|x-p\|^2.                                      \tag{1}
\]
For the first inequality, put \(z=N(x)-p\), add the two variational
inequalities, and move the Taylor residual to the right-hand side.
This gives \(\mu\|z\|^2\le|z^T r|\), which yields the bound.
The segment from \(x\) to \(p\) lies in \(P\). The second inequality
is the integral Hessian-remainder estimate. No face-identification radius
appears in (1), including when optimal multipliers are zero.

Polynomial-time rational convex approximation supplies a feasible
\(x_0\) with
\[
 f(x_0)-f(p)\le\min\{1,\mu/(8K^2)\}.
\]
Strong convexity and constrained first-order optimality imply
\(\|x_0-p\|\le1/(2K)\). Only polynomially many accuracy bits are
requested at this preliminary stage. The weak-optimization dependency and
its exact-feasibility contract are recorded in
[the existing unconstrained theorem](../../research-20260927/strong-convex-quartic-posslp-upper.md)
and in the transfer theorem.

Iterating exact quadratic flow solves gives feasible rational-circuit
points \(x_k\) with
\[
                  \|x_k-p\|\le K^{-1}2^{-2^k}.           \tag{2}
\]
The number of stored gates and oracle calls is polynomial in input length
and \(k\), because the iterates retain their shared circuits.

## 4. Exact signs and feasible witnesses

The original rational instance has a singleton optimizer. Its KKT formula
uses a polynomial number of real variables and fixed-degree polynomial
equalities and inequalities. Node-balance multipliers may be unrestricted;
bound multipliers are nonnegative and complementary. These conditions are
necessary on a polyhedron, including lower-dimensional ones, and sufficient
by convexity. Adding \(s=h(x)\) gives a one-free-variable existential
formula whose real solution set is \(\{h(p)\}\).

The same real-algebraic separation argument used in the existing exact
comparison notes therefore supplies an effective polynomial \(a\) such
that
\[
 h(p)\ne0\ \Longrightarrow\ |h(p)|\ge
                 g:=2^{-2^{a(I)}}.
\]
The exponent bound concerns the original printed instance; it is not
recomputed from the expanded rational Newton iterates. On the supplied box,
\(\|\nabla h\|\) has a polynomial-bit upper bound. Thus polynomially
many iterations in (2) ensure
\[
                      |h(x_k)-h(p)|\le g/8.
\]
Construct \(g\) with repeated squaring and make the final sign query using
\(h(x_k)-g/2\) for strict positivity, \(h(x_k)+g/2\) for weak
positivity, or \(g^2/4-h(x_k)^2\) for equality. Negating the observable
or the predicate covers all other comparisons. This proves the theorem.

The feasible iterate has a useful additional interpretation. If
\(f(p)<r\), then the construction for \(h=f-r\) returns an exactly
feasible rational-circuit flow satisfying \(f(x_k)<r\). Its circuit is
polynomial in the original input size and is computed in
\(\mathrm P^{\mathrm{PosSLP}}\). No polynomial bound on its expanded
numerators and denominators is asserted. No rational witness is promised
when a non-strict threshold is attained only by an irrational optimum.

Disjoint union of two flow instances compares their exact optimal values:
minimize the sum of their objectives and use their difference as observable.
Use the minimum of their two curvature bounds. This adds no constraint-rank
restriction.

## 5. Scope and verification

Infinite endpoints do not change the conclusion. First obtain a rational
feasible flow \(q\) of polynomial encoding length by rational flow
feasibility, equivalently rational linear programming. Set
\[
                  R=1+2\|\nabla f(q)\|_1/\mu.
\]
This is a rational number of polynomial bit length. Since \(f(p)\le f(q)\),
global strong convexity gives
\[
 0\ge f(p)-f(q)\ge
  -\|\nabla f(q)\|_2\|p-q\|_2+
                       \tfrac\mu2\|p-q\|_2^2.
\]
Consequently \(\|p-q\|_2\le2\|\nabla f(q)\|_2/\mu<R\).
Intersect each original capacity interval with \([q_e-R,q_e+R]\).
The resulting bounded rational flow polytope is nonempty and retains
\(p\) as its unique minimizer. Its explicit encoding is polynomial.
The finite-endpoint theorem therefore applies without changing any exact
optimizer comparison.

The proof also applies to any fixed polynomial degree when global strong
convexity of every arc cost is supplied. The degree-four statement matches
the present topic. This is an upper bound for exact comparison, not a
strongly polynomial algorithm for computing irrational polynomial-flow
optimizers by ordinary arithmetic.

The graph structure enters through the exact quadratic subproblem solver.
Replacing the incidence equations and bounds by an arbitrary rational
polyhedron removes that verified dependency. General convex-QP bit
complexity, or an arithmetic bound depending on the expanded Hessian
encoding, does not justify the same circuit simulation.

The targeted check is:

```text
python3 research-20261003-arithmetic/constrained-exact/check_network_flow.py
```

It checks exact Taylor subproblem coefficients, feasible rational Newton
steps, and (1) on two parallel arcs with a balance equality, ordinary and
zero-multiplier boundary optima, and an optimum with tiny positive slack.
These examples check the formulas and boundary behavior; they do not prove
the uniform complexity theorem or implement Végh's algorithm. The source
operation model and the mathematical transfer argument supply those parts.
No project-wide verification or CI inspection is included.

The command above passed: six boundary cases and 42 exact rational Newton
steps. The source PDF was read for the stated dependency and its operation
model; downloaded copies are not required for the targeted check.
