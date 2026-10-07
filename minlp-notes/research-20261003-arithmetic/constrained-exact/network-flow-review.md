# Independent review of the polynomial-flow exact-comparison theorem

Date: 2026-10-03. Reviewed document: [network-flow.md](network-flow.md).

**Verdict:** no blocking mathematical defect found. The stated
`P^PosSLP` upper bound follows from the exact quadratic-flow dependency,
the constrained Newton estimate, and the effective algebraic separation
bound. It is a Turing reduction, and it does not settle arbitrary
polyhedral constraints or establish publication priority.

## Source dependency and compressed arithmetic

I inspected the [author PDF of Végh's 2016 paper](https://personal.lse.ac.uk/veghl/papers/vegh-quadratic.pdf),
especially the arithmetic model on printed page 1729, the capacity
reduction on page 1735, and Section 6.1 on pages 1751–1753. Theorem 20
states the exact capacitated quadratic-flow bound. The model permits only
elementary rational arithmetic and comparisons; its operation count is
independent of coefficient encoding length. Section 6.1 implements the
remaining oracles through rational linear systems and parametric search.
Zero quadratic coefficients are permitted, including the zero-cost
auxiliary arcs used for capacities. The source's separate rational
bit-length guarantee is unnecessary for the circuit simulation.

This is the right dependency. A merely polynomial bit-complexity result
for quadratic programming would not suffice once the Newton iterates
are represented by circuits. Here each source arithmetic operation adds
constantly many shared gates, and each numerical comparison uses
polynomially many PosSLP queries on circuits of polynomial size. An
adaptive branch does not require enumerating the source's decision tree:
only the execution path selected by the oracle answers is constructed.

The displayed positive-denominator division formula is correct. Its
denominator stays positive when the previous denominators are positive
and the source divisor is nonzero. The latter follows from following a
valid execution of the exact source algorithm. Initial binary rational
constants can be built with polynomially many integer-circuit gates.
Neither integer rounding nor expansion of circuit numerators is needed.

## Making the artificial-cost reduction explicit

The source also makes its working graph strongly connected with
artificial arcs of sufficiently high linear cost. The theorem can cite
the complete source algorithm as written. The following explicit bound
also removes any concern that this step might inspect expanded
coefficient lengths.

After replacing a capacity interval by its two-arc gadget, let `N` be
the number of gadget-graph nodes. Every original gadget flow lies in
`[0,u_e-l_e]`. Compute a rational-circuit bound `C>=1` on the absolute
derivative of every gadget cost on these intervals. For a quadratic,
the maximum of the two absolute endpoint derivatives suffices.

At an optimal feasible gadget flow, the residual graph with derivative
costs has no negative cycle. Add a temporary source with zero-cost arcs
to all nodes and take shortest-path distances `pi`. A shortest simple
path contains at most `N-1` gadget arcs, so

```
-(N-1) C <= pi_v <= 0.
```

These potentials satisfy the flow optimality inequalities, with equality
on positive-flow arcs. Add a new node `t`, set its potential to zero,
and give each artificial arc `vt` and `tv` linear cost

```
M = N C + 1.
```

Both artificial reduced costs are strictly positive at zero flow.
The original optimum, extended by zero artificial flow, therefore
satisfies the optimality conditions of the augmented convex problem.
Strict positivity also forces artificial flow to vanish in every
augmented optimum: the first-order convexity inequality gives a
strictly positive cost contribution for any positive artificial flow.
Thus this augmentation preserves the optimizer projected onto the
original arcs. It uses only polynomially many circuit operations and
comparisons. This is a proof of a usable bound; computing the unknown
optimal potentials is not part of the augmentation algorithm.

Empty instances are checked before this argument, as required by the
note. Isolated nodes and fixed arcs can be removed by ordinary rational
preprocessing. Equivalently, keep a polynomial bound in `|V|+|E|`
instead of using the source's normalized arc-only complexity notation.

## Newton convergence, feasibility, and exact signs

The Taylor quadratic has diagonal Hessian and linear coefficient

```
f'_e(x_e) - f''_e(x_e) x_e.
```

Hence the quadratic subproblem remains in the verified flow class at
every iterate. Its unique solution is rational for rational input,
including inputs held as circuits, and it satisfies the original
balance equations and capacity bounds exactly.

Adding the two constrained first-order inequalities gives

```
mu ||N(x)-p||^2
 <= [grad f(p)-grad f(x)-H_f(x)(p-x)]' [N(x)-p].
```

The Hessian remainder bound proves equation (1) of the reviewed note.
No active-face identification or positive lower bound on multipliers
enters this calculation. With the stated initial objective tolerance,
strong convexity yields `||x_0-p||<=1/(2K)`, and induction gives
`||x_k-p||<=K^(-1) 2^(-2^k)`. The initial weak-optimization call needs
only polynomially many accuracy bits and must return an exactly
feasible rational point; the cited convex approximation contract has
that requirement explicitly recorded in the transfer theorem.

The KKT projection is the singleton `{h(p)}` even on a lower-dimensional
flow polytope. Polyhedral normal-cone optimality does not require strict
feasibility, independent equality rows, or unique multipliers. Thus the
existing one-block elimination argument supplies a nonzero-value
separation bound in terms of the original explicit input. It is not a
bound in terms of expanded Newton iterates.

With observable error at most `g/8`, the three final strict-sign tests
can be made explicit as follows:

| Predicate | Strictly positive circuit expression |
| --- | --- |
| `h(p)>0` | `h(x_k)-g/2` |
| `h(p)>=0` | `h(x_k)+g/2` |
| `h(p)=0` | `g^2/4-h(x_k)^2` |

The separation alternative `h(p)=0` or `|h(p)|>=g` verifies every
row. Repeated squaring creates the small threshold using polynomially
many gates. This also validates the strictly feasible objective
witness claim when `f(p)<r`; it does not produce a rational optimizer
when the unique optimizer is irrational.

I also reviewed the added reduction for infinite capacity endpoints.
For a rational feasible flow `q`, coercivity gives existence of `p`,
and the strong-convexity inequality with `f(p)<=f(q)` gives
`||p-q||_2<=2||grad f(q)||_2/mu`. Thus the stated rational radius
`1+2||grad f(q)||_1/mu` strictly contains the optimizer. Rational linear
programming supplies `q` with polynomially many bits; fixed polynomial
degree makes the radius and resulting finite capacities have polynomial
encoding length. Intersecting the original capacities with this box
preserves the optimizer and the network-flow structure. This extension
does not require a new arithmetic primitive.

## Targeted verification and limits

Command run:

```text
python3 research-20261003-arithmetic/constrained-exact/check_network_flow.py
```

Result: passed six boundary cases and 42 exact rational Newton steps.
The cases include strict and zero-multiplier endpoint optima, an upper
capacity, and a tiny positive inactive slack. I also inspected the
checker: its optimality inequalities have the correct endpoint signs,
and its squared-error inequality is the square of the claimed
Euclidean estimate with `K=6`.

This test checks the local formulas, not the quadratic-flow algorithm
or the uniform complexity theorem. Those depend on the source theorem
and the mathematical argument above. No project-wide checks or CI
inspection were performed. This review is an internal mathematical
audit, not an external peer review or a literature-priority finding.
