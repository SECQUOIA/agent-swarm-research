# Audit: continuous gate variables preserve binary inputs

Date: 2026-09-27. Status: independent proof review of the generic comparator
in [Applications and boundaries](hessian-span-applications-and-limits.md).
The argument is valid. It is an elementary consequence of standard circuit
simulation, not a new formulation theorem claimed by this research.

## Precise statement

Let a model have rational input data encoded by a bit string \(D\), and let
its original discrete decisions be \(z\in\{0,1\}^k\). Suppose a fixed
deterministic Turing machine decides whether the continuous fiber at
\((D,z)\) is feasible within time \(T(|D|+k)\), where \(T\) is a known
polynomial. Then one can construct in polynomial time a rational polyhedron
\(P_D\) with coordinates \((z,u)\), where every component of \(u\) is
continuous, such that

\[
 \{z\in\{0,1\}^k:\exists u\ (z,u)\in P_D\}
 =\{z\in\{0,1\}^k:\text{the original fiber is feasible}\}.
\]

The number of variables, inequalities and encoding bits is polynomial in
\(|D|+k\). No rational feasible point of the original continuous fiber is
needed.

## Proof and encoding details

A deterministic computation of \(T(n)\) steps has a Boolean circuit of
size \(O(T(n)^2)\): encode the successive machine configurations and
implement each local transition with a constant-size circuit. This
construction is explicit and takes polynomial time. Fix the input-data
bits to \(D\), leaving only the \(k\) binary decisions as free circuit
inputs. Machines that halt early can retain their acceptance state until
the prescribed last step. See
[Trevisan, CS254 Lecture 3, Theorem 5](https://lucatrevisan.wordpress.com/2010/04/25/cs254-lecture-3-boolean-circuits/)
for the tableau construction.

For each gate introduce one continuous output variable \(g\in[0,1]\).
Use the following inequalities or equality, with all input wires also in
\([0,1]\):

| Gate | Linear constraints in addition to the bounds |
| --- | --- |
| \(g=a\mathbin{\mathrm{AND}}b\) | \(g\le a,\ g\le b,\ g\ge a+b-1\) |
| \(g=a\mathbin{\mathrm{OR}}b\) | \(g\ge a,\ g\ge b,\ g\le a+b\) |
| \(g=\mathop{\mathrm{NOT}}a\) | \(g=1-a\) |

At binary input values these constraints force the unique correct binary
output. Induction in a topological ordering of the circuit therefore
forces every gate to its Boolean value whenever the original \(z\) is
binary. Requiring the final output to be one proves both directions of
the displayed equality.

Each gate uses a constant number of inequalities. Coefficients and right
hand sides can all be taken from \(\{-1,0,1\}\). If both inputs of an AND
or OR gate refer to the same wire, eliminate the redundant gate or insert
separate copy variables before writing its inequalities; otherwise
collecting repeated terms could produce a coefficient of two. Variable
indices require only logarithmically many bits, so the complete rational
description still has polynomial length.

## What the argument does and does not establish

This is exactness of the **binary projection**, not a linear description
of the convex hull of the feasible binary assignments. Gate constraints
need not remain exact when original inputs are fractional. There is no
conflict with lower bounds on linear extended formulations of such convex
hulls. Nor does the construction give a polynomial-time method for finding
an accepted binary input.

For a fixed Hessian-span bound, the established polynomial bit-time
continuous feasibility algorithm supplies the required fixed machine and
polynomial running-time bound. Accordingly, in purely binary applications,
the existence of a polynomial-size MILP with no additional integer
variables is already a consequence of continuous feasibility being in P.
The direct geometric formulation can still have structural value, but its
existence alone is not a separate complexity gain in this case.

For a bounded general integer coordinate, its binary digits are not
automatically forced to be binary by the integrality of that coordinate.
For example, \(z=b_0+2b_1=1\), with continuous \(b_0,b_1\in[0,1]\),
permits \((b_0,b_1)=(0,1/2)\). Therefore this proof does not establish the
corresponding result with general bounded integer inputs while preserving
the number of integer variables. It also does not recover a feasible
continuous point of the original nonlinear model.

## Verification scope

The review checked the circuit simulation's uniform construction, all
binary truth-table cases of the three gate formulations, induction over
the circuit, rational coefficient size, and the distinction between binary
projection and convex hull. No computation or project-wide checks were
needed for this elementary proof. The review is conditional on the stated
deterministic polynomial-time feasibility decider; it does not independently
verify that separate algorithm.
