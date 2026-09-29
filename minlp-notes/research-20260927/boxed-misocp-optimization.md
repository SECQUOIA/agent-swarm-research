# Exact affine optimization over SOCP systems with boxed integer variables

Date: 2026-09-28. Status: complete corollary proof; the
[independent review](boxed-misocp-optimization-review.md) and a separate
completion audit found no gap. This is a consequence of the reviewed continuous, value-encoding,
and optimizer-encoding results linked below. No separate novelty claim is
made for finite-union selection, algebraic recognition, or integer bisection.

Finite rational bounds on the integer variables extend the exact affine
SOCP optimization result to mixed-integer systems. For fixed squared-Hessian
span, an NP oracle suffices to classify the problem, recover its exact finite
infimum, decide attainment, and return an exact optimizer when one exists.
When the number of integer variables is also fixed, the algorithm is
deterministic polynomial time without an oracle.

## 1. Input and conclusion

Let \(z\in\mathbb Z^k\) lie in a supplied finite rational box \(B_z\),
let \(x\in\mathbb R^n\), and consider rational affine constraints and
SOC rows

\[
 \|A_{i,z}z+A_{i,x}x+b_i\|_2
      \le c_{i,z}^Tz+c_{i,x}^Tx+d_i\quad(1\le i\le m).       \tag{1}
\]

Write the resulting feasible set as \(F\), and minimize the rational
affine objective

\[
                         f(z,x)=a^Tz+u^Tx+v.                \tag{2}
\]

The continuous variables need not have a supplied box. Define

\[
 h=\dim_{\mathbb Q}\operatorname{span}
       \{2(A_{i,x}^TA_{i,x}-c_{i,x}c_{i,x}^T):1\le i\le m\}.
                                                               \tag{3}
\]

This is the span of the Hessians in the continuous variables after squaring
the cone rows. Retain all affine right-side sign conditions. No condition
on the quadratic blocks involving \(z\), or on their rank, is imposed.
The parameter refers to the supplied representation.

Let \(N\ge2\) be total binary input length. As in the
[continuous optimization note](continuous-socp-optimization.md), let
\(S\ge2\) bound structural size and \(\tau\ge1\) bound rational
coefficient bits, including the integer box. Empty integer intervals are
detected after rounding their endpoints to
\(L_i=\lceil\ell_i\rceil\), \(U_i=\lfloor u_i\rfloor\).

**Corollary.** For each fixed \(h\), the problem is in
\(\mathrm{FP}^{\mathrm{NP}}\): a deterministic polynomial-time
algorithm with an NP oracle reports exactly one of

- infeasible;
- unbounded below;
- finite infimum, not attained;
- finite minimum, attained.

In either finite case it returns the value as a primitive integer minimal
polynomial and a rational isolating interval. In the attained case it also
returns an integer vector \(z^*\) and an exact continuous optimizer in
one common algebraic field. The value degree, continuous common-field degree,
and total output length are \(N^{O(h+1)}\). All oracle queries have
polynomial length for fixed \(h\). For fixed \(k,h\), the entire
algorithm is deterministic polynomial time without an oracle.

The returned continuous point can be chosen to be the unique minimum-norm
optimizer within the selected integer fiber. No convexity or unique
minimum-norm point is claimed across the union of integer fibers. The case
\(k=0\) is exactly the continuous result. Empty continuous tuples are
handled as in that result.

## 2. Uniform algebraic bounds over all boxed assignments

For a fixed \(z\in B_z\cap\mathbb Z^k\), denote its continuous
fiber by \(F_z\), and let \(\theta_z=\inf_{x\in F_z}f(z,x)\)
when the fiber is nonempty. Every boxed integer coordinate has polynomial
bit length in the input. Substituting these coordinates changes structural
size by at most a fixed polynomial factor, and gives rational coefficient
bits at most

\[
                         (\tau+1)S^{O(1)}.                  \tag{4}
\]

The continuous Hessians are exactly those in (3). These bounds are uniform
over assignments and require no enumeration.

The [finite-infimum theorem](nonconvex-finite-infimum.md) therefore gives
uniform effective bounds

\[
 D\le S^{O(h+1)},\qquad H\le(\tau+1)S^{O(h+1)}             \tag{5}
\]

for degree and coefficient bits of every finite \(\theta_z\).
The [minimum-norm optimizer theorem](nonconvex-attainment-and-optimizer.md)
likewise gives a uniform radius

\[
              R=2^{(\tau+1)S^{C(h+1)}}\ge1                 \tag{6}
\]

for a sufficiently large effective absolute \(C\), containing a
minimum-norm optimizer of every fiber whose infimum is attained. It also
gives its common-field degree \(S^{O(h+1)}\) and coordinate heights
\((\tau+1)S^{O(h+1)}\).

There are finitely many boxed integer assignments. If the overall problem
is feasible and bounded below, then

\[
                 \theta:=\inf_F f
                     =\min_{z:F_z\ne\varnothing}\theta_z.  \tag{7}
\]

Consequently the global finite infimum equals one of the slice values and
has the bounds (5). No product of the slice polynomials and no count of the
integer assignments enters this conclusion. Likewise, the global objective
is unbounded below exactly when at least one nonempty fiber is unbounded
below. Finiteness of the integer box is essential to both assertions.

## 3. Threshold decisions recover the global value

For each rational \(t\), the threshold system
\(F\cap\{f\le t\}\) adds only an affine row and leaves (3)
unchanged. The [SOCP projection theorem](socp-hessian-span-frontier.md)
reduces its feasibility to a rational MILP with exactly the original
\(k\) integer variables, including when no continuous box is supplied.

For fixed \(h\), this gives an NP feasibility language with polynomial
certificate length. An NP oracle decides the threshold queries when \(k\)
is part of the input. For fixed \(k,h\), the same reduction followed by
the fixed-integer-dimension MILP algorithm decides them in deterministic
polynomial time. The oracle changes with this complexity regime; no
polynomial-time solution of variable-dimension MILP is assumed.

First query feasibility of \(F\). If nonempty, use (5) to compute
\(M=2^{H+2}\) strictly larger in magnitude than every possible finite
\(\theta\). Feasibility of \(F\cap\{f\le-M-1\}\) is then
equivalent to unboundedness below. Otherwise bisect
\([-M-1,M+1]\) with the rational threshold oracle and recover the exact
finite value by the reviewed recognition procedure in the continuous note.
An infeasible query exactly at an unattained infimum preserves the enclosing
interval, just as in the continuous case.

The number of queries, their coefficient bits, and the recognition work are
polynomial for fixed \(h\). More precisely, the bounds have the form
\((\tau+1)^{O(1)}S^{O(h+1)}\) before the cost of the NP oracle.
The coefficient-sensitive projection construction retains this form:
threshold precision changes coefficient bits and leaves the native SOCP
structure polynomial in \(S\). Internal LP or MILP lift variables never
become input variables of a later algebraic bound. No enumeration of fibers
is used in the algorithm.

## 4. A compact mixed domain detects attainment

In the finite case, take \(R\) from (6) and form

\[
                       D=F\cap\{x\in[-R,R]^n\}.            \tag{8}
\]

The integer coordinates remain in their supplied box. Thus \(D\) is a
finite union of compact continuous fibers and is itself compact. If it is
empty, no original optimizer exists. Otherwise use Section 3 to compute
its exact minimum \(\beta\), which is attained, and decide

\[
           \theta\text{ is attained on }F
                         \quad\Longleftrightarrow\quad
                               \beta=\theta.                \tag{9}
\]

If the original problem attains \(\theta\) in some fiber, that fiber's
minimum-norm optimizer is inside (8) by (6), giving the forward implication.
The reverse implication is compact attainment in \(D\). Some other
fibers can have the same finite infimum without attaining it; (9) does not
require them to attain it.

The comparison in (9) uses exact algebraic root comparison. All optimization
and feasibility inputs remain rational. Adding (8) contributes only affine
rows, so structural size remains polynomial in \(S\), while maximum
coefficient bits become \((\tau+1)S^{O(h+1)}\). Reapplying the
coefficient-sensitive bounds preserves this form instead of composing
the exponent in \(h\) with itself.

## 5. Select an attained optimal fiber and recover its point

Suppose (9) establishes attainment. For rational integer-coordinate
interval restrictions \(K\), use the following Boolean oracle: answer
no if \(D\cap K\) is empty; otherwise compute its exact minimum
\(\beta_K\) by Section 3 and answer yes exactly when
\(\beta_K=\theta\). Compactness gives

\[
       \beta_K=\theta
          \quad\Longleftrightarrow\quad
         D\cap K\text{ contains an original optimizer}.    \tag{10}
\]

Start with the integer intervals \([L_i,U_i]\). Bisect an interval with
more than one integer at
\(m_i=\lfloor(L_i+U_i)/2\rfloor\). Query the lower part
\([L_i,m_i]\) while retaining every current interval. If (10) answers
yes, keep it; otherwise keep \([m_i+1,U_i]\). These two disjoint integer
intervals cover the current one, so some optimal point is retained.
Continue until every coordinate is fixed, obtaining \(z^*\).

This takes
\(O(\sum_i\log(U_i-L_i+1))\) interval decisions, polynomial in
the endpoint bit lengths. Store only the current endpoints; a bisection
history does not add rows. At termination \(F_{z^*}\) has an attained
optimum equal to \(\theta\), witnessed within the box (8).

Substitute this integer vector into the original unboxed system and invoke
the [continuous exact optimization algorithm](continuous-socp-optimization.md)
once. It returns the exact minimum-norm optimizer of that fiber. The
substitution obeys (4), so its common-field degree and output length are
\(N^{O(h+1)}\). It uses no NP oracle. All earlier interval decisions
use the threshold oracle of Section 3 through exact value recovery. This
proves the stated \(\mathrm{FP}^{\mathrm{NP}}\) conclusion for fixed
\(h\), and deterministic polynomial time for fixed \(k,h\).
Each interval decision makes polynomially many queries to the same NP
feasibility oracle through a deterministic value calculation; no stronger
oracle is introduced by composing these subroutines.

## 6. Why an unboxed value comparison would fail

Consider \(z\in\{0,1\}\), \(x,y\ge0\), and

\[
             \|(2(1-z),x-y)\|_2\le x+y,
             \qquad \min x.                               \tag{11}
\]

The squared residual is \(4(1-z)^2-4xy\); its continuous Hessian
span is one. For \(z=0\), the infimum is zero but unattained, since
\(xy\ge1\). For \(z=1\), the minimum zero is attained at
\((x,y)=(0,0)\). The global minimum is therefore attained. An unboxed
slice-infimum test would incorrectly accept \(z=0\) as a fiber from
which to recover an optimizer. In the box \([-R,R]^2\), \(R\ge1\),
the \(z=0\) minimum is \(1/R>0\), while the \(z=1\) minimum
is zero. The compact test (10) chooses an attained optimal fiber.

The mixed feasible set need not be convex; each continuous fiber is convex.
Integer interval selection uses finite partitions and compact value
attainment, so it does not assume convexity of the mixed feasible set or of
its optimal set. This note makes
no claim for unbounded integer variables, nonlinear objectives, or practical
running times. Priority for optimization on the full class is not established
here; the [SOCP prior audit](socp-hessian-span-prior.md) also records older
sources for the \(h\le1\) feasibility and projection cases.

The author ran `python -` with a targeted inline script checking this note
and the continuous note for local links, paired math delimiters, trailing
whitespace, control characters, and final newlines. The same command used
SymPy to verify the residual and continuous Hessian in (11), the boundary
point \((z,x,y)=(0,1/R,R)\), the optimal point \((1,0,0)\), and
infeasibility of \(x=0\) in the \(z=0\) fiber. All checks passed.
These are document and example checks, not an implementation of the general
algorithm or a verification of its universal degree bounds.

The completed [independent review](boxed-misocp-optimization-review.md)
found no gap. A separate completion audit checked the saved proof, its
compact-query requirement, and the oracle composition, with the same result.
No project-wide checks or CI inspection were performed.
