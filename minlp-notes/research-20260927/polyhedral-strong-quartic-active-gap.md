# A supplied inactive-slack gap removes the active-face guess

Date: 2026-09-28. Status: proved and passed
[independent adversarial review](polyhedral-strong-quartic-active-gap-review.md).
No novelty claim is made.

The [general polyhedral oracle bound](polyhedral-strong-quartic-posslp-upper.md)
guesses an active support. A supplied lower bound on nonzero optimal
slacks makes the full active set recoverable by ordinary polynomial-bit
approximation. Exact value or coordinate comparison then uses one
PosSLP instance. This is a conditional refinement, not a deterministic
upper bound for the general constrained problem.

Let \(f,P=\{X:AX\le b\},\mu\) satisfy the assumptions of the
general note. In addition, supply \(\delta\in\mathbb Q_{>0}\) and
promise that, at the unique minimizer \(p_P\) for nonempty \(P\),
\[
 b_i-a_i^{\mathsf T}p_P=0
 \quad\text{or}\quad
 b_i-a_i^{\mathsf T}p_P\ge\delta
 \qquad\text{for every row }i.                         \tag{1}
\]
The bit length of \(\delta\) is part of the input. No lower bound
on a nonzero Lagrange multiplier is required.

**Proposition.** Under these promises, every exact value or minimizer
coordinate comparison in the general note has a deterministic
polynomial-time many-one reduction to PosSLP.

**Proof.** First check emptiness by rational LP. Empty inputs have a
constant truth value according to the requested comparison, and map
to a fixed yes or no PosSLP circuit. For nonempty inputs set
\[
 \sigma=\max\{1,\max_i\|a_i\|_1\},\qquad
 \varepsilon=\min\left\{1,
                   \frac{\mu\delta^2}{128\sigma^2}\right\}.
                                                               \tag{2}
\]
For no inequalities use \(\sigma=1\). All quantities have polynomial
bit length in the enlarged input.

The rational convex polynomial approximation algorithm of Slot,
Steurer, and Wiedmer,
[Hesse's Redemption, Corollary 1.2](https://arxiv.org/html/2511.03440v1),
returns an actual feasible rational point \(\tilde p\in P\) with
\(f(\tilde p)\le f(p_P)+\varepsilon\) in polynomial time.
Strong convexity and constrained first-order optimality give
\[
\begin{aligned}
 f(\tilde p)&\ge f(p_P)
   +\nabla f(p_P)^{\mathsf T}(\tilde p-p_P)
   +\frac\mu2\|\tilde p-p_P\|^2\\
 &\ge f(p_P)+\frac\mu2\|\tilde p-p_P\|^2.
\end{aligned}
\]
The nonnegative linear term is retained here because an optimum on
the boundary need not have zero ambient gradient. It follows that
\[
 \|\tilde p-p_P\|\le\frac{\delta}{8\sigma},\qquad
 |a_i^{\mathsf T}(\tilde p-p_P)|\le\frac\delta8.             \tag{3}
\]
Every truly active row has slack at \(\tilde p\) at most
\(\delta/8\); every inactive row has slack at least
\(7\delta/8\). Thus the full active set is exactly
\[
             S=\{i:b_i-a_i^{\mathsf T}\tilde p<\delta/2\}.
                                                               \tag{4}
\]
This set is computed by exact comparisons of polynomial-bit rationals.

Choose a rational row basis \(A_I\) of \(A_S\). The point
\(p_P\) lies in \(A_IX=b_I\), and the polyhedral normal-cone
condition puts \(\nabla f(p_P)\) in the row space of \(A_I\).
Hence \(p_P\) is stationary for the affine restriction. The
free-coordinate parameterization from the general note preserves
the curvature bound \(\mu\), so its unique unconstrained minimizer
is exactly \(p_P\).

Apply the companion unconstrained comparison theorem to this restricted
quartic and the desired value or coordinate observable. This constructs
one PosSLP instance. The zero-dimensional restriction is rational and
can instead map its directly computed truth value to a constant
instance. No oracle calls are used in the preceding active-set recovery.
\(\square\)

The selected row basis need not support nonnegative multipliers by
itself. That is harmless here: the entire active set has already been
identified, and its row space supplies restricted stationarity. The
positive-support certificate in the general NP oracle verifier is a
different choice with a different purpose.

The proposition covers redundant constraints, zero multipliers, and
lower-dimensional polyhedra. It does not assume strict complementarity
or ordinary Slater feasibility. However, the inactive-slack promise is
substantial and is not verified by this procedure. If the best useful
\(\delta\) has exponentially many printed bits, polynomial time in
the enlarged input is not polynomial time in the original instance.
The algebraic separation bound in the general argument does not
automatically provide a polynomial-bit \(\delta\).

This is a standard active-set identification implication once a gap
and the weak-optimization algorithm are supplied. Its role is to state
precisely one sufficient condition for removing nondeterminism. It is
not evidence that the unrestricted problem lies in deterministic
\(\mathrm P^{\mathrm{PosSLP}}\), and no practical solver speedup or
publication-priority claim is made.

The independent review reconstructed the error and slack bounds and
checked the row-space argument, including an example where a chosen
row basis requires a negative multiplier. No mathematical correction
was needed. No project-wide verification or CI inspection was performed.
