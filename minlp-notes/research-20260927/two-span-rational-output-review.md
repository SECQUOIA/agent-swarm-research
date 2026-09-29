# Review of rational feasible-point construction at span two

Date: 2026-09-28. Status: the complete proof in
[the rational-output note](two-span-rational-output.md) passes this
independent adversarial review. This review concerns deterministic
polynomial-time rational output, beyond the existence and size of rational
witnesses.

## Claim and dependencies

The intended input is a rational system of native PSD quadratic inequalities
whose Hessian matrix span has dimension at most two, with arbitrary rational
affine rows. The intended output is either infeasibility or a rational feasible
point, in polynomial Turing time. Variable bounds and strict feasibility are
not assumptions.

The algorithm is a corollary of two separate ingredients:

- The exact fixed-span continuous feasibility and optimization algorithms
  summarized in [the main results](hessian-span-main-results.md), which accept
  rational input and return exact status and value. Their proof does not use
  the proposed rational-output algorithm.
- The rational tangency theorem in
  [the two-span note](two-span-rationality-frontier.md), and the classical
  fixed-span small-point consequence of quadratic-map sampling recorded in
  [the prior-work audit](nonconvex-hessian-span-prior-audit.md). The latter
  bounds the strict-branch radius without assuming either a rational witness
  or an algorithm to construct one. The polynomial rational-witness theorem
  in the two-span note is an alternative size argument, not a necessary
  dependency of this algorithm.

This review checks how those dependencies imply rational output. It does not
independently reprove every exact-optimization dependency, establish
publication priority, or claim an implemented solver.

## Affine-face identification is necessary

The two-generator epigraph lift has polynomial encoding length and leaves
two PSD quadratic inequalities, denoted by \(q_1,q_2\), inside a rational
polyhedron \(P\). First decide feasibility. On a nonempty feasible set
\(F\), minimize each affine defining row \(a_j\), normalized as
\(a_j\le0\). The row is identically tight on \(F\) exactly when its
minimum is zero. A negative minimum and an unbounded-below result both mean
that the row is not identically tight. Explicit equalities are retained
throughout.

The equalities from the tight rows define the affine hull \(L\) of the
smallest face of \(P\) containing \(F\). To check this without relying
on a face representation theorem, choose, for each remaining row, a point
of \(F\) making that row strict. Their average is feasible and makes
every remaining row strict. If no rows remain, use any feasible point.
A neighborhood of the resulting point in \(L\)
therefore lies in \(P\). This proves that \(L\) is the required affine
space. Rational Gaussian elimination computes its chart with polynomial
coefficient bits.

One must perform this reduction before interpreting a zero common margin
as quadratic tangency. For example,

\[
 q_1(x,y)=x^2-1,\qquad q_2(x,y)=y^2-1,\qquad P=\{x\ge1\}
\]

has feasible set \(\{1\}\times[-1,1]\). A common positive margin for
all three inequalities is impossible. Nevertheless the two quadratics
have a common strict point in the original plane, and no nonzero
nonnegative combination is globally nonnegative there: evaluate at the
origin. The correct affine reduction gives \(L=\{x=1\}\), on which
\(q_1\) is identically zero. The zero-quadratic branch then applies.

## Positive margin and rational rounding

In rational coordinates on \(L\), maximize \(s\), subject to

\[
 0\le s\le1,\qquad q_i+s\le0,\qquad a_j+s\le0
\]

for the remaining affine rows. The new variable contributes no Hessian
direction, so the exact fixed-span optimization oracle still applies.

If the optimal margin is positive, its polynomial-size algebraic
representation permits the choice of a positive dyadic rational
\(\delta\) below it with polynomial bit length. Fix this same
\(\delta\) for every subsequent query. The system requiring slack at
least \(\delta\) is rational, nonempty, and still has Hessian span at
most two. The fixed-span algebraic small-point bound therefore ensures
that doubling boxes \([-R,R]^d\), starting at \(R=1\), find a
feasible box after polynomially many doublings. That argument requires
only a small real point, which may be algebraic. The polynomial
rational-witness theorem gives an alternative justification.

Coordinate bisection must preserve feasibility of the fixed
\(\delta\)-slack system, not merely the original zero-slack system.
When the lower half of the current coordinate interval is infeasible,
retain the upper half. Every retained box then contains a point of the
same slack system. There is no need for the different queries to share
one distinguished algebraic point.

For example, on the outer box \([-R,R]^d\), a valid infinity-norm
Lipschitz bound for
\(q(u)=\tfrac12u^TAu+b^Tu+c\) is

\[
 L_q=R\sum_{i,j}|A_{ij}|+\sum_i|b_i|.
\]

Take a rational common bound \(L\ge1\) for every quadratic and
affine row, and let \(\eta=\min\{1,\delta/(2L)\}\). All their
bits are polynomial. If every final coordinate interval has width at
most \(2\eta\), its rational midpoint is within \(\eta\) in
infinity norm of a feasible point in that box. Every original row has
value at most \(-\delta+L\eta\le-\delta/2\). The rational chart
enforces all selected affine equalities exactly. The bisection count
includes the initial width \(2R\), and is polynomial in
\(\log R+\log L+\log(1/\delta)\).

Thus the strict branch needs only exact feasibility and value queries;
it need not request or round an algebraic feasible point.

## Zero margin and rational restrictions

The affine-face reduction guarantees a feasible point at which every
remaining affine row is strict. If the two quadratics had a common
strict point anywhere on \(L\), a sufficiently short segment toward
it from that feasible point would satisfy all remaining rows strictly.
Therefore zero margin implies the absence of a simultaneous strict
quadratic point on \(L\).

First test each individual quadratic for a global minimum of zero on
\(L\). For a PSD quadratic this uses rational linear algebra: solve
\(Au=-b\), and evaluate at a solution. If the equation is inconsistent,
the quadratic is unbounded below along a kernel direction. If a global
minimum of zero is found, replace the row by its rational gradient
equations and delete that quadratic row. Deletion is essential even if
the quadratic is identically zero and the gradient equations have rank
zero. Restriction preserves the feasible set and leaves one quadratic.

A remaining one-quadratic system can be handled by boxed rational convex
QP. Skip infeasible boxes and enlarge the box until its rational QP
minimum is at most zero. The classical one-quadratic short-witness
theorem bounds the number of doublings; exact convex QP returns a
rational minimizer. Alternatively, the same margin and restriction
argument can be repeated for the single remaining quadratic.

If neither individual quadratic has global minimum zero, the convex
alternative must use two positive weights. The tangency lemma provides
a positive rational \(t\) for which \(q_1+tq_2\) is globally
nonnegative and has minimum zero. Its construction is effective:

- On the common Hessian kernel, a nonzero linear coefficient determines
  \(t\) by a rational ratio.
- Otherwise pass to a rational complement and form the scalar Schur
  minimum \(f(t)\). After cancelling numerator and denominator, the
  tangency proof makes \(\gcd(N,N')\) linear for its nonzero reduced
  numerator \(N\). Its root is the required rational \(t\).
- If the scalar function is identically zero, \(t=1\) works. This
  case can already be excluded by the preceding individual minimum
  tests, but retaining the branch is harmless.

Cancellation is indispensable: the raw determinant can have additional
repeated roots at negative poles. The determinant and adjugate formulas
have degree \(O(d)\) and polynomial coefficient bits; rational
polynomial gcd and linear algebra therefore take polynomial time.
If the complement has dimension zero and the linear terms vanish on the
common kernel, both quadratics are constant. Their common zeros forced
by the positive-weight alternative make both constants zero, so taking
\(t=1\) is valid. This edge case cannot require a nontrivial inverse.

The gradient equations of \(q_1+tq_2\) define a rational affine
space containing every feasible point. On its direction space,

\[
 \ker(A_1+tA_2)=\ker A_1\cap\ker A_2,
\]

so both remaining quadratics become affine. Rational LP gives the
required rational point. This includes singular Hessians and the case
where the aggregate is identically zero.

## Scope of verification

The proof reconstruction above checks each branch, including affine
boundaries, zero Hessians, common-kernel linear terms, unbounded affine
objectives, and rational rounding at a fixed positive margin. The
polynomial bit claim uses only a constant number of affine restrictions;
the number of optimization queries is polynomial in the input size.

The complete candidate was read after the outline review. The author
then corrected the empty-average edge case and a literal tab replacing
the fraction command in the Schur formula; both corrections were
independently reread. The final width \(2\eta\), rather than the
more restrictive width initially suggested during review, is valid
because midpoint distance is at most half the interval width. The
quotient-dimension-zero branch also passes the check above.

A targeted Python check of this review's final newline, trailing
whitespace, control characters, and four local Markdown links passed.
The command used was:

```sh
python - <<'PY'
from pathlib import Path
import re
p = Path('research-20260927/two-span-rational-output-review.md')
s = p.read_text()
assert s.endswith('\n')
assert all(line == line.rstrip() for line in s.splitlines())
assert not any(ord(c) < 32 and c not in '\n\r' for c in s)
links = re.findall(r'\]\(([^)]+)\)', s)
local = [x.split('#', 1)[0] for x in links
         if not x.startswith(('http://', 'https://'))]
assert all((p.parent / x).exists() for x in local)
print(f'{len(local)} local links and document checks passed')
PY
```

The algorithmic claim should be presented as an output refinement of the
fixed-span exact algorithms, not as an independent proof of their
polynomial running time. Rational witness existence alone would not
justify the construction. No new prior-art search, project-wide checks,
CI inspection, or Lean formalization was performed in this review.
