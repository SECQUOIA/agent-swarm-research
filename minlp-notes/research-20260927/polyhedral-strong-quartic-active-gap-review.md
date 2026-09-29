# Independent review of the supplied inactive-slack-gap refinement

Date: 2026-09-28. Status: the frozen proof passes independent review.
No mathematical correction is needed. This is an elementary conditional
result, with no publication-priority claim.

The reviewed [note](polyhedral-strong-quartic-active-gap.md) has SHA256
f1f2d85704b98a59639e812bcb44b6ee6d2363e9e40b74e142c6a64558b9b63f.
This reviewer did not develop the construction and separately reviewed
both the unconstrained observable theorem and the general polyhedral
oracle argument on which it depends.

## Approximation identifies the complete active set

The lower bound \(\delta>0\) is a promise on every nonzero slack at
the actual constrained minimizer. Its rational encoding is part of the
input. The quantity
\(\sigma=\max(1,\max_i\|a_i\|_1)\) is rational and computable
in polynomial bit time, without computing any square root.

The cited convex approximation theorem returns an actual feasible
rational point \(\tilde p\), not merely a point close to the
polyhedron. At a constrained optimum \(p\), differentiability and
convexity of \(P\) imply
\(\nabla f(p)^{\mathsf T}(\tilde p-p)\ge0\).
Thus strong convexity gives

\[
 \frac{\mu}{2}\|\tilde p-p\|^2
 \le f(\tilde p)-f(p)
 \le\varepsilon
 \le\frac{\mu\delta^2}{128\sigma^2}.
\]

This proves \(\|\tilde p-p\|\le\delta/(8\sigma)\).
Since \(\|a_i\|_2\le\|a_i\|_1\le\sigma\), every slack
changes by at most \(\delta/8\). Active slacks at \(\tilde p\)
lie in \([0,\delta/8]\), using actual feasibility; inactive slacks
are at least \(7\delta/8\). Therefore the exact rational test

\[
 b_i-a_i^{\mathsf T}\tilde p<\delta/2
\]

recovers precisely all active rows. Its threshold cannot meet a
slack on a promised input. The minimum with one in the choice of
\(\varepsilon\) does not change any inequality.

## Row-space restriction needs no multiplier margin

Every active equation holds at \(p\). Dependencies among active
normals consequently induce the same dependencies among their
right-hand sides. A row basis therefore gives a consistent affine
restriction containing \(p\).

The polyhedral normal-cone condition places \(\nabla f(p)\) in
the row space of all active normals, hence in that of the selected
basis. Restricted stationarity follows. The identity-block nullspace
chart preserves the curvature lower bound, so this stationary point
is the unique unconstrained minimizer of the restriction.

There is no requirement that the basis preserve a nonnegative
multiplier representation. For example, minimize \((x-1)^2\) over
\(x\le0,-x\le0\). The optimum is \(x=0\). Choosing only the normal
\(-1\) as a row basis would require multiplier \(-2\) in
\(f'(0)+(-1)\lambda=0\), but its affine equation still fixes the
correct minimizer. This confirms why a multiplier-sign test is
unnecessary in this conditional construction, despite being needed
in the general guessed-support verifier.

The argument handles redundant rows, zero normals, zero multipliers,
and polyhedra with no ordinary interior. It imposes no strict
complementarity assumption.

## Reduction size and scope

The approximate point has polynomial bit length in the enlarged input,
including \(\delta\). All active-set tests and row-basis calculations
are ordinary polynomial-time rational operations. Affine substitution
preserves fixed degree and polynomial bit size. The final value or
coordinate predicate is therefore compiled to one PosSLP instance by
the reviewed observable theorem.

For empty \(P\), the requested predicate is decided directly under
the conventions in the general note. A zero-dimensional restriction
is a rational point and is also handled directly. Both cases may
output a constant yes or no PosSLP instance.

The procedure does not verify the inactive-slack promise. Even with a
checked Hessian certificate, that additional condition remains a
promise. If a useful \(\delta\) needs many printed bits, the runtime
bound is polynomial in that enlarged input, not in an earlier shorter
description. Algebraic separation alone does not provide a
polynomial-bit slack gap. The manuscript states these limitations
correctly and does not claim a deterministic result for all
constrained quartics.

This review rederived every displayed inequality and the row-space
argument. No further computation was needed beyond the independently
run boundary checks recorded in the
[general polyhedral review](polyhedral-strong-quartic-posslp-upper-review.md).
No Lean formalization, project-wide verification, or CI inspection was
performed.

The final status-and-verification version has SHA256
eb2bf4e5cf51072543f14f9b5c968fcddac5e27a0808578a65ae1ce6bc1b34e7.
Its reviewed status and verification account agree with the audit above.
These updates pass scoped reconciliation; no mathematical argument
changed.
