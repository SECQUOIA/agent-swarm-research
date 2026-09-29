# Independent audit of quasiconvex transitions and value bounds

Date: 2026-09-28. Scope: Sections 1–5 and 7 of
[the quasiconvex value manuscript](quasiconvex-mixed-value-frontier.md).
This reviewer did not develop the argument. The review finds no substantive
gap in the finite-value theorem, coefficient-sensitive bounds, or the
restricted attained-integer corollary. The parent reviewer separately
checks fractional optimizer recovery. This note does not establish
novelty or independently audit the compressed SOC projection theorem.

## Primary inputs checked

I read the primary statements in Khachiyan and Porkolab,
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf):
Theorem 1.1, Propositions 2.1–2.2, and Corollary 2.3, printed pages
208 and 211–212. They allow Boolean formulas and strict inequalities.
The integer witness theorem requires convexity; real elimination and
sampling do not. Individual degree and coefficient bounds omit the atom
count, although the algorithms depend on it. The sample representation
uses one field with a common rational denominator, and its logarithmic
height is linear in the input coefficient bit bound.

For the geometric step, I checked Theorem 2 and Corollary 17 in
[Basu, Conforti, Cornuejols, and Zambelli](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf).
They provide maximal lattice-free containment and the polytope plus
rational linear-space structure used by the manuscript. Full dimension
excludes the alternative of an irrational affine hyperplane.

## Transition levels and endpoint conventions

The two nested families determine the actual spaces, not merely their
dimensions: inclusion and equality of finite dimensions imply equality.
The bounded-form dimension predicates each have at most one finite
boundary. The affine-dimension predicates, including dimension at least
zero, do the same. The last predicate accounts for empty sublevels.
Consequently there are at most \(2k+1\) relevant levels. A truth change
at a boundary itself causes no problem: the argument asserts constancy
only on open complementary intervals, and handles an optimum at a
boundary separately.

The count is sharp for these two invariants. In \(\mathbb R^k\), let

\[
 B_j=[-1,1]^j\times\{0\}^{k-j}\quad(0\le j\le k),
 \qquad
 U_j=\mathbb R^j\times[-1,1]^{k-j}\quad(1\le j\le k).
\]

Define the upward rational semialgebraic set

\[
 E=\bigcup_{j=0}^k B_j\times[j,\infty)
   \;\cup\;\bigcup_{j=1}^k U_j\times[k+j,\infty).
\]

All strict sublevels are nested convex sets. Their affine dimension
changes from \(-1\) through \(0,\ldots,k\) at levels
\(0,\ldots,k\); the bounded-form dimension subsequently drops from
\(k\) to zero at levels \(k+1,\ldots,2k\). There are exactly
\(2k+1\) distinct transition levels. This observation supports the
bookkeeping; it is not needed for the value theorem.

## The cap does not assume a bound for the unknown value

When the right endpoint \(\beta\) of the relevant interval is finite,
the strict slice \(C_\beta\) is convex and has an integer point.
It is described using a selected algebraic \(\beta\), whose bound
comes from the transition predicates. The integer witness theorem then
gives a small integer fiber, and algebraic sampling supplies a feasible
level \(s_0<\beta\) in that fiber. Necessarily \(s_0\ge\theta\).
Thus separation between \(s_0\) and \(\beta\), rather than between
\(\theta\) and \(\beta\), produces the rational cap.

The common-field sample can include the variable selecting \(\beta\).
Even separate algebraic representations would suffice: separation for
their product polynomial retains a logarithmic-height bound linear in
\(H+1\). For an infinite right endpoint, the total projection is the
nested union of convex strict slices. Sampling after its small integer
witness gives the required finite cap directly.

A concrete test is

\[
 E=\{(z,t):z\ge1/2,\ t(1+z)\ge z\}.
\]

Its epigraph is not convex, but every strict sublevel is an interval.
The transition levels are \(1/3\) and \(1\), and the integer optimum
is \(\theta=1/2\). Thus the optimum lies strictly inside a transition
interval with a finite right endpoint. Choosing the integer fiber
\(z=1\), sampled level \(s_0=2/3\), and cap \(U=3/4\) illustrates
the construction without using joint convexity.

## Descent, fields, and precision

In the lower-dimensional case, expand a jointly sampled affine equation
in one rational field basis. Every integer point satisfies all resulting
rational equations. At least one has a nonzero normal. Integer
consistency follows from the cap witness; no assumption that the whole
real affine hull is rational is needed. For example,
\(y=\sqrt2x+\sqrt2-1\) gives the two rational equations
\(x=-1\) and \(y=-1\) on rational points.

In the full-dimensional case, choose any level below the optimum in the
same transition interval. Its closure is lattice-free because its
interior equals the original convex set's interior. Integer points on
the closure's boundary are harmless. Maximal lattice-free containment
supplies a nonzero bounded rational form, contradicting the hypothesized
absence of such forms. This is an existence argument: that auxiliary
level need not have controlled algebraic encoding.

The rational-part construction can be implemented in the sampled field
using determinant equations, polynomial reduction, and rational kernel
computation. Determinant sizes and polynomial reduction counts depend
polynomially on field degree, and linearly on input logarithmic height.
Thus they preserve \((H+1)d^{O_k(1)}\). The finite range of the chosen
form bounds the integer right-hand side. Among finitely many right-hand
sides, one retains an infimizing subsequence, even when no optimizer
exists.

An integer affine parametrization retains convex strict slices and the
same infimum. Carrying the original atoms through the substitution
preserves their degree and adds a quantity linear in the parametrization
bit length to their coefficient bits. At most \(k\) repetitions give
the claimed bound. In dimension zero the finite value is a nonemptiness
transition, including when the vertical fiber is open.

## Attained witnesses and the Pell boundary

Convexity of the weak optimal slice is an actual additional condition.
The identity with the intersection of strict slices above a level uses
closed vertical fibers, not closedness of the whole set. Once the weak
optimal slice is convex, the controlled value representation and the
integer witness theorem apply to that slice.

The Pell example correctly defeats a polynomial witness bound under
strict-sublevel convexity alone. Dividing a positive norm-one unit by
powers of \(3+2\sqrt2\) preserves integral coefficients and leaves a
unit in \([1,3+2\sqrt2)\); its nonnegative second coefficient is less
than two, forcing the remaining unit to be one. For odd indices,
\(y_n\equiv2\pmod4\). Together with odd \(x_n\) and
\(y_{2n}=2x_ny_n\), this proves
\(v_2(y_n)=v_2(n)+1\). The resulting lower bound on the index and
the strict inequality \(x_n>2^{2n-1}\) give the stated binary length.

## Targeted checks and limits

An inline Python command using exact fractions and SymPy checked the
nonconvex epigraph example, its rational cap, and the affine-field
expansion above. Exact integer repeated squaring checked Pell indices
\(n=2^{a-1}\), \(1\le a\le13\), including indices beyond the
earlier run: the norm identity, exact two-adic valuation, and binary
length lower bound all passed through \(n=4096\).

These computations check distinct examples and arithmetic identities.
They do not replace the infinite proofs, prove novelty, or test an
optimization implementation. No project-wide verification or CI
inspection was performed.
