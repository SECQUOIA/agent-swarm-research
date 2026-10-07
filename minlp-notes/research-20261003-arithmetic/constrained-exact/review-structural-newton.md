# Independent review of structural constrained Newton refinement

Date: 2026-10-03.

Status: passed independent proof reconstruction and actual-file audit after
one operation-count wording correction.
This review concerns the proposed exact-observable upper bound for globally
strongly convex rational fixed-degree polynomials on rational boxes whose
Hessians have a positive definite comparison matrix. Tridiagonal Hessians and
positive definite Z-matrices are concrete sufficient cases.

## Main mathematical checks

Let \(P\) be the box, \(p\) its unique minimizer, and \(x\in P\).
Write \(H=\nabla^2 f(x)\), and let \(y\) minimize the Taylor quadratic
over the same box. Its gradient at \(y\) is
\[
g_x(y)=\nabla f(x)+H(y-x).
\]
The two variational inequalities give
\[
\langle g_x(y),y-p\rangle\le0,
\qquad
\langle\nabla f(p),y-p\rangle\ge0.
\]
Writing
\[
r=\nabla f(x)+H(p-x)-\nabla f(p)
\]
therefore gives
\[
\mu\|y-p\|^2
\le \langle H(y-p),y-p\rangle
\le -\langle r,y-p\rangle.
\]
If the Hessian has Lipschitz constant \(L_H\) on the box, Taylor's
integral remainder yields
\[
\|y-p\|\le \frac{L_H}{2\mu}\|x-p\|^2.
\]
This proves the claimed quadratic convergence without identifying a face or
requiring strict complementarity. Both iterates stay feasible by construction,
so the Hessian bounds are needed only along segments in the box.

For \(K=\max\{1,L_H/(2\mu)\}\), an initial error at most
\(1/(2K)\) gives
\[
\|x_k-p\|\le K^{-1}2^{-2^k}.
\]
A feasible objective-gap approximation with error at most
\(\mu/(8K^2)\) provides that initial point. All requested accuracy bits
at this initial stage are polynomial in the explicit input length. This step
must remain separate from the circuit refinement: an ordinary bit algorithm
asked for doubly exponentially small final error would not prove the result.

## Exact quadratic subproblems and source check

I read [Pang and Han, *Some Strongly Polynomially Solvable Convex Quadratic
Programs with Bounded Variables*](https://optimization-online.org/wp-content/uploads/2021/12/arxiv.pdf),
Algorithm I and Proposition 2.1, together with its comparison-matrix discussion.
Their bounded-variable algorithm uses at most \(2n\) pivots when supplied a
positive vector \(v\) satisfying
\(H_{JJ}^{-1}v_J\ge0\) for every principal subset \(J\).
The source explicitly allows degeneracy. Its operations are rational linear
algebra and sign comparisons, including ratio tests.

For an SPD Z-matrix, every principal inverse is nonnegative, so
\(v=\mathbf 1\) suffices. For the comparison matrix
\[
B_{ii}=H_{ii},\qquad B_{ij}=-|H_{ij}|\quad(i\ne j),
\]
when \(B\) is positive definite, the source gives the construction
\[
d=B^{-1}\mathbf1,
\qquad v=\tfrac12(H+B)d.
\]
Here \(d>0\), and positivity of \(v\) is also immediate from
\(v=\mathbf1+\tfrac12(H-B)d\).

For tridiagonal \(H\), recursively assigning signs on the path gives a
diagonal sign matrix \(S\) with \(B=SHS\). Zero off-diagonal entries
cause no difficulty. Thus \(B\) is positive definite whenever \(H\)
is. The identical argument works for any forest as the off-diagonal support
graph, as included in the final draft.

At every Newton step, the rational Hessian entries are represented by shared
arithmetic circuits. PosSLP decides all required signs, including those used
to form \(B\). Every principal matrix solved by the pivot procedure is
positive definite, so its rational elimination has nonzero pivots. Each
arithmetic operation adds only a constant number of numerator/denominator
circuit gates. Division does not require expansion of any integer. A
polynomial number of subproblem operations and Newton steps therefore gives
a deterministic polynomial-time PosSLP-oracle computation.

## Separation and exact output

A simple uniform separation argument uses the box KKT formula itself:
\[
\begin{gathered}
l\le x\le u,\quad \lambda^-,\lambda^+\ge0,\\
\nabla f(x)-\lambda^-+\lambda^+=0,\\
\lambda_i^-(x_i-l_i)=0,\quad
\lambda_i^+(u_i-x_i)=0,\quad z=h(x).
\end{gathered}
\]
The existential projection to \(z\) is precisely the singleton
\(\{h(p)\}\). The number of variables is linear in dimension; all
polynomial degrees are fixed and coefficient bit lengths are polynomial in
the original input. Thus the same one-block quantifier-elimination bound
used in the reviewed unconstrained theorem provides a computable bound
\[
h(p)=0\quad\text{or}\quad |h(p)|\ge 2^{-2^{a(I)}}
\]
for an effective polynomial \(a\). This avoids any need to know the
active face before refinement. Alternatively, restricting to the actual
active box face gives a singleton real stationary locus by global strong
convexity and supplies the same uniform bound; the unknown face is used only
to justify the bound, not enumerated by the algorithm.

A polynomial-bit Lipschitz bound for the explicit fixed-degree observable
and polynomially many constrained Newton steps reduce its approximation
error below one quarter of this gap. Comparing the resulting circuit value
with plus and minus half the gap decides its exact sign, including zero.
The gap itself has a polynomial-size repeated-squaring representation.

Coordinate slacks are admissible observables. Testing them gives the full
active-bound mask, including active bounds with zero multipliers. This does
not print expanded algebraic coordinates of the optimizer and does not turn
the complete adaptive computation into a single PosSLP instance.

## Targeted verification

I ran a Python/SymPy diagnostic using exact rationals and random
seed 103. It generated tridiagonal SPD matrices \(H=LDL^{\mathsf T}\),
with signed bidiagonal \(L\), in dimensions two through six. It checked
the comparison-vector condition on all 714 nonempty principal subsets of
the generated instances. A transcription of the source's pivot algorithm
then solved 90 bounded quadratic programs. Every output passed exact primal
feasibility and bound KKT sign checks, and every pivot count was at most
\(2n\). Cases included zero linear costs and boundary minimizers with zero
multipliers, as well as unrestricted integer linear terms.

The diagnostic was first run inline, then saved without changing its cases as
[check_structural_newton_review.py](check_structural_newton_review.py).
The persisted command actually run was:

```text
python3 research-20261003-arithmetic/constrained-exact/check_structural_newton_review.py
```

The program printed:

```text
PASS: 90 exact bounded-QP KKT checks; 714 exact principal n-step checks; all pivot counts <=2n; boundary zero-multiplier cases included
PASS: four exact quartic Newton steps satisfy the squared error bound; the true optimizer has an active lower bound with zero multiplier, while every computed iterate is interior
```

The second check differentiates
\(f(x)=\tfrac12\|x-p\|^2+((x_1-p_1)-(x_2-p_2))^4\),
with \(p=(0,1/2)\), symbolically and verifies its Hessian is
\(I+12((x_1-p_1)-(x_2-p_2))^2aa^{\mathsf T}\),
\(a=(1,-1)\). On \([0,1]^2\), the rational bound \(L_H=144\)
is valid, and \(\mu=1\). Starting at \((1/512,1/2)\), it checks four
exact constrained Newton steps against the squared form of the error
estimate. The active lower bound at the true optimizer has zero multiplier;
all four computed iterates are strictly interior. This directly exercises
the composition without assuming eventual active-set identification.

These finite checks test the source interface and degeneracy handling; the
complexity statement follows from the arguments above and the cited
quadratic-program theorem. No project-wide checks or CI inspection were
performed.

## Scope and limitations

The structural Hessian condition is a promise unless separately certified.
The argument does not establish how to recognize it over the whole box in
polynomial time. Fixed coordinates can be eliminated before optimization;
empty boxes and boxes reduced to a point are immediate rational cases.

The result supplies a new deterministic oracle upper bound for the stated
structural subclass. It leaves the unrestricted constrained problem open.
This review verifies the mathematical construction and source interface;
it does not establish publication priority.

## Actual-file audit

I read the complete [theorem draft](structural-newton.md) and
[source record](primary-sources.md). The draft's KKT-based separation,
fraction-circuit simulation, error thresholds, and unbounded-box radius all
match the proof requirements above. The fixed-degree extension is valid;
the relevant polynomial bounds may depend on the fixed degree. The exact
implicit optimizer description uses stationarity within the affine hull of
the active face, which is sufficient by global strong convexity.

One wording correction was necessary in the general transfer principle:
requiring an operation bound to depend on a numerical parameter whose
logarithm is polynomial in input length is insufficient. The operation
count must itself be polynomial in input length, for example polynomial in
the logarithms of any such parameters. A bound polynomial in their values
could be exponential. This does not affect the Pang--Han application,
whose operation count is polynomial in dimension.

I checked that the final draft makes this correction. I also checked its
added forest-support theorem and explicit comparison-matrix-positive-
definiteness corollary. Both use the same verified matrix construction.
The cap on the warm-start objective tolerance preserves every error bound.
No substantive mathematical issue remains in the stated promise theorem.
