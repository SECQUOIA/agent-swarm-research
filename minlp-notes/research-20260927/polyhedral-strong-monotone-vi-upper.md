# Exact observables of strongly monotone cubic variational inequalities

Date: 2026-09-28. Status: proved and passed
[fresh independent adversarial review](polyhedral-strong-monotone-vi-upper-review.md),
including additional focused reviews. The unambiguous polyhedral
dependency has also passed independent review. Publication priority
is unestablished.

The active-set construction also applies to polynomial maps that are
not gradients. It gives an unambiguous oracle upper bound for exact
observables of the unique solution of a strongly monotone cubic
variational inequality over a rational polyhedron. This is a scope
extension of the existing arguments, not a deterministic exact solver.

## 1. Definition and statement

Let \(T:\mathbb R^n\to\mathbb R^n\) be an explicit rational
polynomial map of degree at most three. Supply \(\mu\in\mathbb Q_{>0}\)
with the global promise
\[
 \langle T(x)-T(y),x-y\rangle\ge\mu\|x-y\|^2
                       \quad(x,y\in\mathbb R^n).         \tag{1}
\]
Let \(P=\{x:Ax\le b\}\) be an arbitrary explicit rational
polyhedron, and let \(h\in\mathbb Q[X]\) have degree at most
four. A solution of the variational inequality is a point \(p\in P\)
satisfying
\[
                   \langle T(p),x-p\rangle\ge0
                   \qquad(x\in P).                     \tag{2}
\]
When \(T=\nabla f\), condition (2) characterizes minimizers of
the differentiable convex function \(f\). General \(T\) need
not arise from any scalar objective.

**Theorem.** If \(P\ne\varnothing\), (2) has exactly one
solution. For each relation \(\bowtie\in\{<,\le,=,\ne,\ge,>\}\),
the language asserting that \(P\ne\varnothing\) and
\(h(p)\mathrel{\bowtie}0\) belongs to
\[
                 \mathrm{UP}^{\mathrm{PosSLP}}\cap
                 \mathrm{coUP}^{\mathrm{PosSLP}}.        \tag{3}
\]
With only a supplied \(\mu\), this is a promise statement.
The checked rational positive definite Jacobian Gram format of the
[strongly monotone zero theorem](strong-monotone-cubic-posslp-upper.md)
gives corresponding ordinary languages, with invalid certificates
rejected. This requires no Slater condition, multiplier gap, or
positive lower bound on nonzero slacks.

## 2. Existence on an arbitrary nonempty polyhedron

Choose any \(x_0\in P\). A rational such point can be obtained
by rational LP, although rationality is not needed for this existence
argument. Choose \(R>\|T(x_0)\|/\mu\) and let
\(K=P\cap\overline B(x_0,R)\). The continuous map
\[
                         x\longmapsto\Pi_K(x-T(x))
\]
maps the nonempty compact convex set \(K\) to itself. Brouwer's
fixed-point theorem, applied in its affine hull if needed, gives a
fixed point \(p\). The Euclidean projection characterization gives
\(\langle T(p),x-p\rangle\ge0\) for all \(x\in K\).

The point cannot lie on the artificial sphere. Indeed, if
\(\|p-x_0\|=R\), strong monotonicity gives
\[
 \langle T(p),p-x_0\rangle
 \ge\mu R^2+\langle T(x_0),p-x_0\rangle
 \ge\mu R^2-\|T(x_0)\|R>0,
\]
contradicting the variational inequality with \(x=x_0\).
Thus \(p\) lies strictly inside the ball. For each \(x\in P\),
a sufficiently short segment from \(p\) toward \(x\) lies in
\(K\). Applying the inequality on that segment and dividing by its
positive length proves (2) for every \(x\in P\).

If \(p,q\) both satisfy (2), summing their inequalities with test
points \(q,p\), respectively, gives
\(\langle T(p)-T(q),p-q\rangle\le0\). Equation (1) then
forces \(p=q\). This proves existence and uniqueness, including
unbounded or lower-dimensional polyhedra.

## 3. The active-set verifier

Use the same full active-mask certificate as in the
[unambiguous quartic note](polyhedral-strong-quartic-unambiguous-upper.md).
For a guessed subset \(S\) of constraint rows, choose a canonical
row basis \(I\) and the rational free-coordinate chart
\[
                 x=\bar x+Zy,\qquad A_Ix=b_I,\qquad
                 Z^{\mathsf T}Z\succeq I.               \tag{4}
\]
The chart has polynomial-bit coefficients. Define
\[
                 U_S(y)=Z^{\mathsf T}T(\bar x+Zy).       \tag{5}
\]
This is an explicit rational polynomial map of degree at most three.
For any \(y,z\),
\[
\begin{aligned}
 \langle U_S(y)-U_S(z),y-z\rangle
 &=\langle T(\bar x+Zy)-T(\bar x+Zz),Z(y-z)\rangle\\
 &\ge\mu\|Z(y-z)\|^2
 \ge\mu\|y-z\|^2.
\end{aligned}                                                   \tag{6}
\]
The reviewed strongly monotone zero theorem therefore supplies its
unique real zero \(y_S\), exact polynomial-observable comparisons
there, and the shared rational Newton circuit used in its proof.
Set \(p_S=\bar x+Zy_S\). A rank-\(n\) basis gives a
rational point instead and is handled by rational arithmetic and LP.

Check that the slacks at \(p_S\) vanish exactly on \(S\) and
are strictly positive off \(S\). Then check
\[
 T(p_S)^{\mathsf T}v\ge0
 \quad\text{for every }v\text{ with }A_Sv\le0,
                                      \ -1\le v_j\le1.  \tag{7}
\]
This test uses the rational LP and uniform vertex-observable gap
argument of Lemmas 1--2 in the unambiguous quartic note, replacing
the unconstrained minimizer of a gradient map with the unique zero
of \(U_S\). Its required properties all appear in the reviewed
monotone theorem: polynomial-bit rational initialization, quadratic
Newton convergence using only rational operations, a uniform
algebraic gap for fixed-degree explicit observables, and exact
PosSLP comparison. The vector observable here is
\(C(y)=T(\bar x+Zy)\), still explicit and cubic.

For specificity, choose a polynomial input-length bound \(M\) for
\(U_S,\mu,v^{\mathsf T}C\) over every vertex \(v\) of the
boxed tangent polytope. The rational-vertex determinant bound is
unchanged. Use the monotone theorem's bounds \(B=2^{30M}\) and
its fixed effective separation polynomial \(a(M)\), enlarged as
in that theorem. Its warm start and \(a(M)+2\) Newton steps give
error at most \(\gamma/8\) for all those observables, where
\(\gamma=2^{-2^{a(M)+1}}\) bounds every nonzero value away
from zero. Minimizing the resulting rational circuit cost, printing
an optimal rational vertex by its active equations, and checking its
true observable sign proves (7) in \(\mathrm P^{\mathrm{PosSLP}}\).
There is no LP with an unhandled algebraic objective and no expansion
of the high-precision Newton rationals.

**Soundness.** For every \(x\in P\), the direction \(x-p_S\)
satisfies the guessed active inequalities and scales into the box in
(7). Thus (7) implies (2). Uniqueness identifies \(p_S\) with
the actual solution \(p\).

**Completeness.** At the solution \(p\), every direction with
\(A_{S_*}v\le0\), where \(S_*\) is the full active set,
gives a short feasible segment. Hence \(T(p)^{\mathsf T}v\ge0\)
on that cone. Farkas' lemma puts \(-T(p)\) in the cone of the
active normals, so \(T(p)\) lies in their row space. Therefore
the coordinate of \(p\) in (4) solves (5), and the unique zero
theorem identifies it with \(y_{S_*}\). All tests pass.

The exact-slack test forces every accepting mask to be \(S_*\).
There is exactly one valid optimality certificate. Append the
comparison of the explicit degree-at-most-four polynomial
\(h(\bar x+Zy_S)\), or its complement, to obtain the two
unambiguous machines. In the Gram-certificate format, invalid
certificates are handled first, by rejection in the original language
and acceptance in its complement. Next handle empty polyhedra
deterministically, still before guessing. This proves (3).
\(\square\)

## 4. Interpretation and limits

The theorem covers strongly monotone polynomial equilibrium equations
with polyhedral domain constraints, even when the Jacobian is
nonsymmetric and no potential function exists. This is a plausible
interface for exact questions in constrained equilibrium models.
It does not establish that any particular application has global
strong monotonicity or a readily available certificate, or that the
oracle construction is an efficient numerical solver.

For a concrete nonpotential example, put \(u=(x,y-1)^{\mathsf T}\),
\[
 T(x,y)=
 \begin{pmatrix}1&2\\-2&1\end{pmatrix}u
       +\|u\|^2u+\begin{pmatrix}-1\\0\end{pmatrix},
 \qquad P=\{(x,y):x\le0,\ y\ge0\}.
\]
For every \(v\in\mathbb R^2\),
\[
 v^{\mathsf T}J_Tv
   =\|v\|^2+\|u\|^2\|v\|^2+2(u^{\mathsf T}v)^2
   \ge\|v\|^2,
\]
so the global strong-monotonicity modulus is at least one. The
Jacobian satisfies \((J_T)_{12}-(J_T)_{21}=4\), excluding a
scalar potential. At \(p=(0,1)\), \(T(p)=(-1,0)\), and
the variational-inequality pairing is \(-x\ge0\) on \(P\).
The active restriction is \(x=0\); its remaining equation is
\((y-1)+(y-1)^3=0\). Thus the example has a unique constrained
solution while the ambient map is not a gradient.

The new existence argument is classical coercivity and projection.
The certificate argument is the same canonical active-set method as
for constrained convex quartics. The content added here is its precise
scope for constrained, nonpotential polynomial maps once the reviewed
strongly monotone zero theorem is available. The
[monotone source supplement](strong-monotone-exact-prior-supplement.md)
and [broader source audit](monotone-polynomial-posslp-prior-independent.md)
compare related variational-inequality, fixed-point, and algebraic
complexity results. Those comparisons do not establish priority for
this constrained extension. A dedicated wider search remains needed.

No deterministic \(\mathrm P^{\mathrm{PosSLP}}\) algorithm for
finding the active set is proved. No single PosSLP instance for the
general constrained problem is claimed. The global strong-monotonicity
assumption is essential to the present affine-restriction construction;
monotonicity solely on \(P\) does not justify applying the all-domain
zero theorem to arbitrary guessed affine spaces.

## 5. Verification record

The main independent review reconstructed the full extension and its
Newton/observable interface. Additional fresh reviews checked
constrained existence, affine restriction, full masks, and the
certificate and empty-input branches. No mathematical defect was
found. These reviews are linked above.

The main reviewer ran
`python research-20260927/check_polyhedral_monotone_vi_review.py`,
which passed an exact three-dimensional nonpotential cubic example,
a two-dimensional restriction retaining a nonzero skew Jacobian,
redundant and zero rows, and rejection of an incorrect feasible point
by a negative tangent pairing. A separate reviewer ran 191 masks and
42 tangent vertices across nine nonsymmetric affine cases. The review
records those checks and their limits. The author read the reviews
without duplicating their checks.

For the displayed two-dimensional example, the author and main reviewer
separately ran inline SymPy checks of the derivative identity, skew
Jacobian difference, value at \((0,1)\), and restricted equation.
An initial author assertion compared unsimplified expressions; after
explicit expansion, all exact identities passed. These finite examples
illustrate the nonpotential scope; they do not implement PosSLP or
prove the all-input complexity statement. No project-wide checks or
CI inspection were performed.
