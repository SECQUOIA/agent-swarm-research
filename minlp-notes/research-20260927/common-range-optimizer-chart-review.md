# Independent review: polynomial charts for conditional convex quadratic optimization

Date: 2026-09-28.

**Verdict.** The proposed chart lemma is correct. It gives a finite family
of rational polynomial maps of degree at most two that contains the
minimum Euclidean norm optimizer of every nonempty, bounded-below
fiber. A chart needs a basis of **all** active row normals, and the
multipliers on that basis are unrestricted in sign. The formula for the
global infimum requires every nonempty fiber to be bounded below, or a
separate treatment of unbounded fibers.

This is an independent proof and boundary check of the chart lemma. It
does not establish novelty or verify the subsequent real-algebraic
complexity bounds that might use the charts. A second reviewer,
`chart_linear_algebra`, independently checked the kernel, consistency,
minimum-norm argument, and rational coefficient bounds.

## Precise statement

Let \(u\in\mathbb R^r\), \(v\in\mathbb R^n\), and

\[
 P_u=\{v:Cv+p(u)\le0\},
 \qquad
 f(u,v)=\tfrac12v^THv+q(u)^Tv+a(u),
\]

where \(C,H\) are constant rational matrices, \(H\succeq0\), \(q\) is
rational affine, and \(p,a\) are rational polynomials of degree at most
two. For every subset \(I\) of linearly independent rows of \(C\),
including the empty subset, form

\[
 M_I=\begin{pmatrix}H&C_I^T\\C_I&0\end{pmatrix},
 \qquad
 v_I(u)=\operatorname{primal}\left[
 M_I^+\binom{-q(u)}{-p_I(u)}\right].
\]

Here \(M_I^+\) is the Moore--Penrose inverse in the ordinary Euclidean
inner product. It is a constant rational matrix.

If \(P_u\ne\varnothing\) and \(f(u,\cdot)\) is bounded below on \(P_u\),
then its unique minimum Euclidean norm optimizer is \(v_I(u)\) for at
least one such \(I\). Each \(v_I\) has degree at most two and rational
coefficient encoding length polynomial in the original dense input
length, uniformly over \(I\).

Set

\[
 D_I=\{u:Cv_I(u)+p(u)\le0\},\qquad F_I(u)=f(u,v_I(u)).
\]

The domain \(D_I\) is described by quadratic inequalities, and \(F_I\)
has degree at most four. At every nonempty, bounded-below fiber,

\[
 \min_{v\in P_u} f(u,v)
   =\min_{I:\,u\in D_I} F_I(u).
\]

No consistency, stationarity, or multiplier sign conditions need to be
added to \(D_I\) for this equality. The crucial facts are that every
retained point is feasible and that one chart contains an optimizer.

## Proof, including singular and degenerate cases

A quadratic function bounded below on a nonempty polyhedron attains
its infimum by the classical Frank--Wolfe theorem. This theorem is
explicitly recalled in the introduction of
[Martinez-Legaz, Noll, and Sosa, *Minimization of quadratic functions on
convex sets without asymptotes*](https://www.math.univ-toulouse.fr/~noll/PAPERS/frank_and_wolfe.pdf).
Since \(H\succeq0\), the fiber optimizer set is nonempty, closed, and
convex. It therefore has a unique point \(v^*\) of minimum Euclidean
norm.

Let \(A\) be the set of all active constraint rows at \(v^*\), and
choose \(I\subseteq A\) whose rows form a basis for
\(\operatorname{row}(C_A)\). This also covers rank zero.

For every \(d\in\ker C_I=\ker C_A\), the points \(v^*+td\) are
feasible for all sufficiently small positive and negative \(t\).
Active rows stay at equality, while the finitely many inactive rows
have strictly positive slack. First-order optimality gives

\[
 (Hv^*+q(u))^Td=0\quad\text{for every }d\in\ker C_I.
\]

Consequently \(Hv^*+q(u)\in\operatorname{range}(C_I^T)\), and there is
a unique, possibly signed vector \(\lambda^*\) with

\[
 M_I\binom{v^*}{\lambda^*}
       =\binom{-q(u)}{-p_I(u)}.
\]

This proves consistency directly and requires neither Slater's
condition nor a constraint qualification.

The PSD assumption gives the exact kernel identity

\[
 \ker M_I=(\ker H\cap\ker C_I)\times\{0\}.
\]

Indeed, \(M_I(d,\mu)=0\) implies \(C_Id=0\) and

\[
 0=d^T(Hd+C_I^T\mu)=d^THd.
\]

Thus \(Hd=0\), and full row rank of \(C_I\) gives \(\mu=0\).
The converse is immediate.

For \(d\in\ker H\cap\ker C_I\), sufficiently small two-sided
feasible motions preserve the objective exactly:

\[
 f(u,v^*+td)-f(u,v^*)
  =t(Hv^*+q(u))^Td+\tfrac12t^2d^THd=0.
\]

Minimum norm among fiber optimizers therefore implies
\((v^*)^Td=0\). Hence \((v^*,\lambda^*)\) is perpendicular to
\(\ker M_I\). It is the unique minimum Euclidean norm solution of
the consistent symmetric system, so it is precisely the
Moore--Penrose solution. Taking its primal block proves the claim.

## Rationality, coefficient lengths, and chart count

The rationality of \(M_I^+\) does not require rational eigenvectors.
For any rational symmetric matrix \(M\), choose a rational basis
matrix \(Z\) of \(\ker M\). Put \(A=M+ZZ^T\). On
\((\ker M)^\perp\), \(A=M\) is nonsingular; on \(\ker M\),
\(A=ZZ^T\) is positive definite. These subspaces are invariant, and

\[
 M^+=A^{-1}MA^{-1}.
\]

For full-rank \(M\), use the empty basis and \(A=M\); for zero \(M\),
one can use \(Z=I\). Rational Gaussian elimination constructs \(Z\)
with polynomial coefficient bit lengths. Cramer's rule and determinant
bounds then give polynomial coefficient bit lengths for \(A^{-1}\)
and \(M^+\). All matrices have dimension at most twice the original
number of continuous variables, since \(|I|\le n\).

Multiplying by a polynomial vector of degree at most two preserves
that degree and polynomial coefficient encoding length. Substitution
into the original quadratic objective gives degree at most four,
again with polynomial coefficient encoding length. These estimates
are uniform over all \(I\), independent of numerical \(u\).

There are at most \(2^m\) independent row subsets when \(C\) has \(m\)
rows. Thus the number of charts can be exponential in the original
input length, although its logarithm and each chart's encoding length
are polynomial. The lemma alone does not supply a polynomial-time
algorithm that enumerates the charts.

## Necessary qualifications and exact examples

**All active normals matter.** Minimize \(v_1^2\) subject to
\(v_2\ge1\). The minimum-norm optimizer is \((0,1)\), but its sole
active constraint has zero KKT multiplier. The empty active-support
chart returns \((0,0)\), which is infeasible. Taking a basis of all
active rows returns \((0,1)\).

**Basis multipliers can be negative.** Minimize \(v\) subject to
\(v\le0\) and \(-v\le0\). The only feasible point is zero. If the
basis consists of the first row, its stationarity multiplier is
\(-1\). The full active set has a nonnegative multiplier
representation, but arbitrary row-basis compression need not preserve
nonnegativity.

**Unbounded fibers require separate treatment.** With no parameter,
minimize \(-v\) subject to \(v\ge0\). Both independent-row charts
return \(v=0\), while the original infimum is \(-\infty\). Therefore

\[
 \inf_{u,v:\,v\in P_u}f(u,v)=\min_I\inf_{u\in D_I}F_I(u)
\]

is justified when every nonempty fiber is bounded below. In
particular, it is justified whenever the original global infimum is
finite. It remains valid when the global infimum is \(-\infty\)
solely through a sequence of bounded-below fibers. It is not a
standalone test for unbounded fibers.

**The fourth degree is real.** For \(u\in\mathbb R\), minimize
\(v^2\) subject to \(v\ge u^2\). The fiber optimizer is \(v=u^2\),
and its objective is \(u^4\).

**PSD is essential to the stated pseudoinverse argument.** Let

\[
 H=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\quad
 q=\binom01,\quad v_1+v_2=1.
\]

Encode the equality by its two opposite inequalities. The objective
is constant on the feasible line, so the minimum-norm optimizer is
\((1/2,1/2)\). With the active basis \(C_I=(1,1)\), the primal block
of the KKT pseudoinverse solution is instead \((1/3,2/3)\). Here the
KKT kernel contains a nonzero multiplier component. This example
does not contradict the lemma, because \(H\) is indefinite.

**The norm refers to these coordinates.** After a nonorthogonal
rational change of variables \(x=T_1u+T_0v\), minimizing \(\|v\|\)
does not generally minimize \(\|x\|\). If the latter is required,
the chart can be adapted without increasing its degree. Put
\(G=T_0^TT_0\succ0\), \(h(u)=T_0^TT_1u\), and let \(Z\) span
\(\ker H\cap\ker C_I\). Replace \(v_I\) by

\[
 \widetilde v_I(u)=v_I(u)
 -Z(Z^TGZ)^{-1}Z^T\bigl(Gv_I(u)+h(u)\bigr).
\]

At the correct active-row chart, local optimality of the original
norm forces the weighted orthogonality condition that characterizes
this point. The correction has constant rational matrices and remains
polynomial of degree at most two. Use a zero correction when the
kernel is trivial.

## Targeted verification performed

Ran one inline `python` command using exact SymPy rational and
symbolic arithmetic. It checked five examples: a singular PSD chart
with dependent active rows and a free optimal direction, the need for
a zero-multiplier active row, a negative basis multiplier, an actual
quartic chart objective, and the indefinite-Hessian failure. The same
command checked \(A^{-1}MA^{-1}=M^+\) on the singular PSD example.
All assertions passed.

These checks verify the stated examples and matrix identities. The
general conclusions rest on the proof above. No project-wide checks,
CI inspection, numerical solver tests, or Lean proof were performed.
