# Independent review: a geometric convexity promise does not suffice

Date: 2026-09-28. Scope: the proposed Valiant–Vazirani boundary for exact
quadratic feasibility with one native Hessian direction. This review is
independent of the proposed proof's author.

## Verdict

The following conditional statement is correct.

> If a deterministic polynomial-time algorithm decides exact feasibility of
> rational quadratic systems whose **total feasible set is promised convex**,
> even when the native Hessians span a space of dimension exactly one, then
> \(\mathrm{RP}=\mathrm{NP}\).

The algorithm receives the quadratic description and the promise. It need not
receive a convex representation, a separation oracle, or a certificate of
convexity. The reduction does not establish hardness under any of those stronger
input requirements.

This is a direct consequence of the classical isolation reduction, combined
with an elementary quadratic encoding. It is a useful scope boundary, not a
new complexity mechanism or evidence of a substantial independent novelty
claim.

## Exact quadratic encoding

Let \(G\) be a CNF formula on \(N\geq 1\) variables. Introduce real variables
\(x\in\mathbb R^N\) and impose

\[
0\leq x_i\leq 1,\qquad
q(x):=\sum_{i=1}^N x_i(1-x_i)\leq 0.
\]

Each summand is nonnegative on the box. Thus \(q(x)\leq0\) holds there exactly
when every coordinate is Boolean. For each clause, impose the affine
inequality requiring the sum of its literal values to be at least one, with
literal values \(x_i\) and \(1-x_i\). The resulting real feasible set is
exactly the set of satisfying Boolean assignments of \(G\).

The only nonzero native Hessian is
\(\nabla^2q=-2I_N\), so its span has dimension exactly one. All coefficients
are rational, the description has polynomial size, and the box is explicit.
If necessary, a variable fixed to zero by an affine row ensures \(N\geq1\)
without changing the number of satisfying assignments.

A finite set is convex if and only if it is empty or a singleton. In
particular, zero- and one-solution formulas satisfy the promised convexity.
This step uses the whole feasible set's geometry; the native quadratic row is
concave and does not define a convex constraint.

## Independent isolation calculation

For completeness, the needed inverse-polynomial isolation probability can be
verified directly. Let \(S\subseteq\{0,1\}^n\) be the satisfying assignments of
an input formula, with \(s=|S|>0\). Choose \(k\) uniformly from
\(\{1,\ldots,n+1\}\), and choose a uniformly random affine map

\[
h(x)=Ax+b\in\mathbb F_2^k.
\]

For distinct Boolean vectors, their two hash values are independent and
uniform. Some available \(k\) satisfies
\(2s\leq 2^k<4s\). For this \(k\), write \(X=|S\cap h^{-1}(0)|\) and
\(t=s/2^k\). Then

\[
\mathbb E X=t,\qquad
\mathbb E[X(X-1)]=\frac{s(s-1)}{2^{2k}},\qquad
\frac14<t\leq\frac12.
\]

Since \(\mathbf 1_{X=1}\geq X-X(X-1)\) for every nonnegative integer \(X\),

\[
\Pr(X=1)\geq t-\frac{s(s-1)}{2^{2k}}
\geq t(1-t)\geq \frac18.
\]

Consequently a trial isolates one original satisfying assignment with
probability at least \(1/[8(n+1)]\). If the original formula is unsatisfiable,
every hash-constrained formula remains unsatisfiable.

To avoid any runtime convention for sampling a uniform integer from an
arbitrary range, one may instead try every \(k=1,\ldots,n+1\), using fresh
uniform binary matrices and vectors. This batch has isolation probability at
least \(1/8\); a constant number of independent batches suffices below.

Each parity equation can be expressed by a polynomial-size Boolean circuit.
Introduce variables for its gates and impose each gate's complete Boolean
equivalence, followed by its required output value. Every input assignment has
exactly one extension to the gate variables; therefore the CNF conversion
preserves the number of surviving assignments. A merely equisatisfiable
conversion would be insufficient here, because it could introduce multiple
extensions of the isolated input assignment.

The original Valiant–Vazirani paper supplies the same ingredients directly:
Theorem 1.1 and Corollary 1.2 address arbitrary completions of the zero/one
promise problem, and Lemma 2.1 supplies a polynomial CNF parity encoding with
a bijection of satisfying assignments. The author of the companion note
checked these statements in the original scan, pp. 87–88. This review checked
the reduction by the explicit calculation and gate-extension argument above.
Source: [Valiant and Vazirani, *NP is as easy as detecting unique solutions*
(1986)](https://www.cs.princeton.edu/courses/archive/fall05/cos528/handouts/NP_is_as.pdf).

## Behavior outside the promise and runtime

Run the proposed exact-feasibility algorithm on the quadratic encoding of
each hashed formula, and accept the original SAT instance if any run returns
feasible.

If the original formula is unsatisfiable, every constructed set is empty.
Every call therefore satisfies the convexity promise and must return
infeasible. False acceptance is impossible.

If the original formula is satisfiable, a trial produces a singleton with
probability at least \(1/[8(n+1)]\). On that trial the call satisfies the
promise and must return feasible. Calls corresponding to multiple satisfying
assignments may return arbitrary answers without invalidating this argument:
any acceptance still occurs on a satisfiable original formula. Repeating a
linear number of independent trials gives acceptance probability at least
one half.

If the assumed polynomial runtime guarantee applies only to promised inputs,
fix a polynomial bound witnessing that guarantee and stop each simulation at
that bound. Treat a timeout as rejection. All promised calls still complete,
so both the soundness and isolation arguments survive. The existence of the
polynomial bound suffices for this conditional complexity implication.

Thus SAT belongs to RP. Standard polynomial reductions imply
\(\mathrm{NP}\subseteq\mathrm{RP}\); the reverse inclusion follows by using
an accepting random string as an NP witness. Hence \(\mathrm{RP}=\mathrm{NP}\).

## Claims that this argument does not support

- It does not establish deterministic NP-hardness under a deterministic
  promise-preserving reduction, or the stronger implication
  \(\mathrm P=\mathrm{NP}\).
- It does not establish hardness when every nonempty feasible set must have
  nonempty interior, satisfy Slater's condition, or be supplied through a
  certified convex representation. The promised nonempty sets constructed
  here are singletons.
- It does not undermine polynomial algorithms for native PSD quadratics or
  explicit second-order-cone constraints. Those representations expose
  convexity that the present description hides.
- It does not depend on large algebraic output, high precision, unbounded
  domains, or irrational data. All feasible points in the reduction are
  Boolean and the common box is \([0,1]^N\).

## Verification record

This review checked the algebraic encoding, the pairwise-independent hashing
calculation, the unique-extension requirement, the one-sided error argument,
and runtime truncation. It also read the complete companion draft
[`convex-representation-boundary.md`](convex-representation-boundary.md) and
found no substantive gap in its final statement or proof. The proof is
discrete and exact; no numerical test or
Lean formalization was needed. A targeted Markdown check checked this file's
final newline and trailing whitespace. No project-wide check or CI check was
run. Literature checking here confirms the classical reduction used; it does
not establish that this particular reformulation has not appeared before.
