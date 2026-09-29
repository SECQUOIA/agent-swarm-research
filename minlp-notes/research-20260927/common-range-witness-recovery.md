# Exact feasible witnesses at small common Hessian range

Date: 2026-09-28. Status: complete proof with
[independent adversarial review](common-range-witness-review.md).
This note extends the decision result in
[the common-range feasibility theorem](common-range-fpt-frontier.md).
The low-dimensional algebraic bounds and the recognition machinery are
established methods. The candidate contribution is their combination with
that exact feasibility oracle to recover a full feasible point in fixed-
parameter time. Priority for this combination has not been established.

## 1. Statement and the point that is recovered

Consider a rational convex quadratic system, or a rational second-order
cone system, of total binary encoding length \(N\). Affine rows and
equalities are unrestricted. For a cone row, use its squared polynomial
and retain the sign of its right-hand side. Let \(H_i\) be these native
quadratic Hessians and put

\[
 K=\bigcap_i\ker H_i,\qquad r=\operatorname{codim}K.
\]

The squared cone Hessians may be indefinite. As in the decision theorem,
the convex cone representation is needed by the algorithm.

**Recovery theorem.** Exact feasibility and the recovery of a feasible
real algebraic point take \(2^{O(r)}N^C\) bit operations, with an absolute
constant \(C\). If the system is feasible, the algorithm returns a
primitive integer irreducible polynomial \(P\), a rational isolating
interval for one real root \(\alpha\), and rational coordinate
polynomials \(b_j\) such that

\[
 x_j=b_j(\alpha),\qquad \deg b_j<\deg P.
\]

The degree of the common field is \(2^{O(r)}\), and the total output
length is \(2^{O(r)}N^C\). There is no Slater, boundedness, or rational
feasible-point assumption.

Choose a rational invertible coordinate transformation

\[
 x=T_1u+T_0v,
 \qquad u\in\mathbb R^r,
 \qquad \operatorname{range}T_0=K.                 \tag{1}
\]

Fix this transformation, computed by rational linear algebra. The point
returned below is specified by first minimizing \(\|u\|_2^2\) over the
projection of the feasible set and then minimizing \(\|v\|_2^2\) in
that fiber. These two unique choices specify the same point for every
requested approximation accuracy. This point depends on the chosen
coordinates; the theorem does not identify it with the minimum-norm point
in the original coordinates.

If \(r=0\), all squared rows are affine. Together with the retained
cone signs, they give a rational polyhedron, so ordinary rational LP
already returns a rational feasible point. The remainder assumes
\(r\ge1\).

For mixed-integer models, first recover a feasible integer assignment by
the decision theorem and then apply this result to its continuous fiber.
With a supplied integer box, this gives \(f(k,r_x)N^C\) recovery time.
Without one, it gives \(f(k,\rho)N^C\), with the cross-aware common-kernel
parameter \(\rho\) defined in the decision theorem. After substitution,
the continuous common range is at most the corresponding parameter.
This corollary concerns feasible witnesses, not optimal points.

## 2. The implicit projection is closed

In the coordinates (1), the polynomial and affine rows are

\[
 Cv\le b(u),                                        \tag{2}
\]

where \(C\) is a constant rational matrix and each entry of \(b\) is
a rational polynomial of degree at most two. All these explicit data
have polynomial encoding length. Farkas' lemma describes the projection
as

\[
 U=\{u:P_j(u)\le0\quad(1\le j\le S)\}.              \tag{3}
\]

After positive denominator clearing in each row, the \(P_j\) are integer
quadratics of coefficient bit length \(\tau\le N^{O(1)}\), and
\(\log(S+1)\le N^{O(1)}\). The minor argument establishing these bounds
is in Section 2 of the decision note. The algorithm never enumerates this
possibly exponential family.

Equation (3) proves that \(U\) is closed. Its convexity follows from the
original convex representation. If nonempty, it therefore has a unique
point

\[
 u^*=\operatorname*{argmin}_{u\in U}\|u\|_2^2.        \tag{4}
\]

Closedness here uses the constant matrix in (2). General linear projections
of closed convex sets need not be closed.

## 3. A classical low-dimensional arithmetic bound

We need the following bound in which the number of implicit rows enters
through its logarithm.

**Lemma.** Suppose a nonempty closed convex set in \(\mathbb R^r\) is
defined by \(S\) integer quadratic weak inequalities, each of coefficient
bit length at most \(\tau\). Its minimum-norm point has common-field
degree at most \(3^{2r}\), and every coordinate has a primitive integer
minimal polynomial with coefficient bit length at most

\[
                  (\tau+\log(S+1)+1)2^{O(r)}.        \tag{5}
\]

The bound is deliberately conservative. The arithmetic principle is
already present in Jeronimo--Perrucci--Tsigaridas,
[*On the minimum of a polynomial function on a basic closed semialgebraic
set and applications*](https://arxiv.org/pdf/1112.0544): Proposition 10
bounds resultant coefficients using
\(\widetilde H=\max\{H,2r+2S\}\); Remark 11 treats coordinates of
minimizers; Theorem 12 treats an unbounded component whose minimizers form
a compact set. The same resultant argument permits a rational linear
form as output, giving a joint-field bound. These statements and their
proofs were inspected. The following separate derivation records exactly
the bound used here and its dependence on \(S\).

### 3.1 Small perturbation coefficients despite many rows

Use independent quadratic polynomials \(Q_0,Q_1,\ldots,Q_S\) and consider

\[
 f_{j,\varepsilon}=P_j+\varepsilon^2Q_j-\varepsilon,
 \qquad
 g_\varepsilon(u)=\|u\|_2^2+\varepsilon Q_0(u).       \tag{6}
\]

For a fixed set of at most \(r\) rows, the genericity lemma in
[the nonconvex certificate note, Section 4](nonconvex-hessian-span-frontier.md#4-a-quantitative-genericity-lemma)
provides proper algebraic bad sets for dependent active gradients and
singular bordered KKT matrices. For \(r+1\) rows it excludes a common
zero. In ambient dimension \(r\), their containing hypersurfaces have
degree \(G(r)=2^{\operatorname{poly}(r)}\), independently of \(S\).
Only the bordered determinant is needed here.

For each fixed nonzero \(\varepsilon\), the coefficient maps in (6)
onto the selected objective and constraint quadratics are surjective.
Substitution into each nonzero bad polynomial therefore remains nonzero
as a polynomial in \(\varepsilon\) and the coefficients of the \(Q_j\).
Choose one nonzero coefficient in its expansion in \(\varepsilon\).
The product of these chosen polynomials, over all relevant row sets, has
degree at most

\[
                     (S+1)^{r+1}G_1(r),
 \qquad G_1(r)=2^{\operatorname{poly}(r)}.            \tag{7}
\]

A nonzero polynomial of degree \(D\) cannot vanish on the entire grid
\(\{0,\ldots,D\}^m\), regardless of the number \(m\) of its variables.
Consequently all the \(Q_j\) can be chosen with integer coefficients of
bit length

\[
                         O(r\log(S+1))+\operatorname{poly}(r). \tag{8}
\]

The number of chosen polynomials can be exponential; this is an existence
argument used to bound heights. Neither this product nor the grid is part
of the recovery algorithm. For the selected coefficients, only finitely
many nonzero \(\varepsilon\) are exceptional, simultaneously for all
row sets.

### 3.2 An unknown box suffices for the existence proof

Choose any real \(R>\|u^*\|_\infty+1\). Minimize \(g_\varepsilon\)
on the hard box \([-R,R]^r\), subject to
\(f_{j,\varepsilon}\le0\). The point \(u^*\) is feasible for all
sufficiently small positive \(\varepsilon\), since its perturbation
term is quadratic in \(\varepsilon\) and the outward margin is linear.
Thus perturbed minimizers exist.

Any sequence of these minimizers as \(\varepsilon\downarrow0\) has a
convergent subsequence. Its limit belongs to \(U\), and comparison with
\(u^*\) shows that its norm is no larger. Uniqueness in (4) forces
every such limit to equal \(u^*\). Hence every minimizer lies strictly
inside the hard box once \(\varepsilon\) is sufficiently small.
Otherwise a sequence of boundary minimizers would have a boundary limit.
The unknown \(R\) therefore never enters the eventual KKT equations.

There are at most \(r\) active perturbed rows, their gradients are
independent, and the bordered KKT matrix is nonsingular. Passing to a
subsequence fixes the active set, of size \(s\le r\). The constraint
and stationarity equations form a square system in \((u,\lambda)\) of
at most \(2r\) variables, with degree at most two in those variables,
degree at most two in \(\varepsilon\), and coefficient
\(\ell_1\)-norm of bit length

\[
 \tau'=O(\tau+r\log(S+1))+\operatorname{poly}(r).     \tag{9}
\]

### 3.3 Eliminate the full KKT system

Apply the finite-quotient elimination lemma in
[the explicit separation note, Section 2](explicit-span-separation.md#2-an-elementary-elimination-lemma)
directly to this full system, with degree bound \(a=2\). For
\(q=r+s\le2r\) variables its quotient dimension is \(L=3^q\), and
the coefficient-bit bound is

\[
 L\bigl[\tau'(2(q+1)+1)+2+\lceil\log_2 L\rceil\bigr]. \tag{10}
\]

Take output \(A=1\), \(B=u_j\). The lemma bounds the degree and height
of an integer annihilator of the limit coordinate. It requires neither
bounded multipliers nor invertibility of the upper-left KKT block.
Taking an irreducible factor preserves (5), by the usual integer
factor-height bound.

Every rational linear combination of the coordinates can instead be used
as \(B\), without changing the degree bound \(L\). First the individual
coordinate conclusions establish algebraicity. The primitive element
theorem then supplies a rational linear combination generating their
joint field. Its degree is at most \(L\le3^{2r}\). This step avoids
multiplying individual coordinate-degree bounds. It finishes the lemma.

Applied to (3), the lemma gives

\[
 [\mathbb Q(u^*):\mathbb Q]\le2^{O(r)},\qquad
 \operatorname{heightbits}(u_j^*)\le2^{O(r)}N^C.     \tag{11}
\]

## 4. Approximate that one nonlinear point using rational queries

The effective meeting-radius bound in the decision theorem gives a
rational \(R\ge1\), with \(\operatorname{bit}R\le2^{O(r)}N^C\),
large enough that \(\|u^*\|_\infty\le R\). Increase a bound for one
feasible projected point by a factor of \(r\) if needed: the minimum
Euclidean norm is no larger than that point's norm.

For rational \(t\ge0\), append

\[
 \|u\|_2^2\le t
 \quad\Longleftrightarrow\quad
             \|(2u,t-1)\|_2\le t+1.                \tag{12}
\]

If the original variables are used, \(u=Lx\) for a rational matrix
\(L\) with kernel \(K\). The new Hessian is \(8L^TL\), which also
annihilates \(K\). Thus these queries do not increase the common range
dimension. Affine coordinate bounds on \(u\) also preserve it.
For a native PSD quadratic system, append the left side of (12) directly
as a PSD quadratic inequality; for an SOCP, use its displayed cone form.

Use exact rational feasibility queries to bisect
\(\nu=\min_U\|u\|_2^2\), initially between \(0\) and \(rR^2\).
Given a desired error \(\eta>0\), obtain a rational upper endpoint
\(t\) satisfying \(\nu\le t\le\nu+\eta^2/16\). The projection
inequality for the minimum-norm point gives

\[
 \|y-u^*\|_2^2\le\|y\|_2^2-\|u^*\|_2^2
                      \le\eta^2/16
 \quad(y\in U,\ \|y\|_2^2\le t).                  \tag{13}
\]

Starting from \([-R,R]^r\), bisect one coordinate interval at a time,
keeping a half exactly when the original system together with (12) and
all current coordinate bounds is feasible. Retain only the current
endpoints. The retained set stays nonempty. When every interval has
width below \(\eta/2\), its rational midpoint differs from \(u^*\)
in each coordinate by less than \(\eta\), by (13). For each new
accuracy request, restart with the original box; a retained box need
not contain \(u^*\) itself.

The query count and endpoint bit lengths are polynomial in
\(N,r,\operatorname{bit}R,\log(1/\eta)\). The coefficient-sensitive
form of the decision theorem gives total cost
\(2^{O(r)}(N+\log(1/\eta))^C\). Its proof treats added coefficient
bits polynomially with an absolute exponent; replacing that dependence
by a parameter-dependent exponent would not suffice.

## 5. Recover the affine fiber through rational quadratic programs

Let \(b^*=b(u^*)\), and define

\[
 F=\{v:Cv\le b^*\},\qquad
 v^*=\operatorname*{argmin}_{v\in F}\|v\|_2^2.       \tag{14}
\]

The fiber is nonempty and closed, so \(v^*\) exists uniquely. Its normal
cone is generated by active rational row normals. Choose linearly
independent active rows \(I\) spanning \(v^*\). Then

\[
 v^*=C_I^T(C_IC_I^T)^{-1}b_I^*.                     \tag{15}
\]

If \(v^*=0\), use the empty set. Rational minor bounds give polynomial
coefficient bit lengths for the matrix in (15), without enumerating its
possible row sets. Each coordinate of \(v^*\) is consequently a rational
quadratic polynomial in \(u^*\), with polynomial coefficient bit
length. It belongs to \(\mathbb Q(u^*)\).
If there are no \(v\) coordinates, the fiber recovery step is empty.

The same formula gives an effective magnitude bound \(\|v^*\|\le V\)
with \(\operatorname{bit}V\le2^{O(r)}N^C\). It also gives coordinate
minimal-polynomial heights of this size. For example, clear the leading
coefficients of the coordinate minimal polynomials in (11), making a
common multiple of the \(u_j^*\) integral. Apply (15), clear its
rational denominators and the square of this common multiple, and bound
all conjugates by the coordinate root
bounds. Taking a field norm produces an integer annihilator of degree
at most \([\mathbb Q(u^*):\mathbb Q]\) and coefficient bits
\(2^{O(r)}N^C\). This argument uses the joint field rather than a
product of coordinate fields.

It remains to approximate this particular \(v^*\) without an
algebraic-coefficient LP oracle. Approximate \(b^*\) rationally with
coordinate error at most \(\delta\), and put

\[
 \widehat b=\widetilde b+\delta\mathbf1,
 \qquad b^*\le\widehat b\le b^*+2\delta\mathbf1.     \tag{16}
\]

Polynomial evaluation on the known box for \(u^*\) requires only
\(O(\log(1/\delta)+\log R+N^{O(1)})\) accuracy bits in its
coordinates. Solve the rational convex QP

\[
 v_\delta=\operatorname*{argmin}\{\|v\|_2^2:Cv\le\widehat b\}. \tag{17}
\]

Classical exact rational convex QP is polynomial time; its output here
is rational. Since \(F\) is contained in the relaxed polyhedron,
\(\|v_\delta\|\le\|v^*\|\).

### 5.1 A uniform rational-matrix repair bound

There is an effective \(H_C\le2^{N^{O(1)}}\) such that, for every
nonempty fiber \(Cv\le b\) and every \(y\),

\[
 \operatorname{dist}(y,\{Cv\le b\})
                  \le H_C\|(Cy-b)_+\|_\infty.       \tag{18}
\]

This is Hoffman's bound, with a simple coefficient estimate. Let \(p\)
be the projection of \(y\) onto the fiber and put \(d=y-p\). By
conic Caratheodory, \(d=C_I^T\lambda\) for linearly independent active
rows and \(\lambda\ge0\). If the positive residual is at most
\(\epsilon\), then

\[
 \|d\|^2=\lambda^T(C_Iy-b_I)
 \le\epsilon\sqrt{|I|}\|\lambda\|
 \le\epsilon\sqrt{|I|}\,\sigma_{\min}(C_I)^{-1}\|d\|.
\]

Every nonzero rational minor has a denominator and numerator of
polynomial bit length. Determinant and matrix-norm bounds therefore give
one computable \(2^{N^{O(1)}}\) upper bound for the last factor,
uniformly over \(I\). Empty active sets give distance zero. No search
over active sets is needed to print a conservative \(H_C\).

Apply (18) to (17), obtaining \(w\in F\) with
\(\|w-v_\delta\|\le\zeta:=2H_C\delta\). The projection inequality
at \(v^*\), together with \(\|v_\delta\|\le\|v^*\|\le V\), gives

\[
 \begin{aligned}
 \|w-v^*\|^2
 &\le\|w\|^2-\|v^*\|^2
 \le2V\zeta+\zeta^2,\\
 \|v_\delta-v^*\|
 &\le\zeta+\sqrt{2V\zeta+\zeta^2}.                 \tag{19}
 \end{aligned}
\]

For \(0<\epsilon\le1\), choosing
\(\zeta\le\epsilon^2/[16(V+1)]\) makes the last quantity less than
\(\epsilon\). Thus a \(2^{-p}\) approximation to \(v^*\) requires
only \(O(p+\log V+\log H_C)\) bits in (16). This supplies the
required approximation oracle using rational data throughout.

## 6. Common-field recognition and verification

The tuple \((u^*,v^*)\) has joint-field degree \(2^{O(r)}\), coordinate
minimal-polynomial heights \(2^{O(r)}N^C\), and the certified
approximation procedures above. Apply
[common-field recovery from an approximation oracle](constructive-common-field-recovery.md).
Its Kannan--Lenstra--Lovasz recognition step and subsequent rational
interpolation have polynomial overhead in the dimension, degree, and
height bounds. Consequently their complete cost and output length are
\(2^{O(r)}N^C\).

Apply the rational transformation (1) inside this field. Since it is
invertible, the coordinates of \(x\) generate the same field as
\((u^*,v^*)\). Exact substitution and univariate sign determination
verify all original quadratic rows, affine rows, and cone right-hand-side
signs in polynomial time in this output length. Verification checks the
returned point against the original problem, independently of the
projected description used in the proof.

The algebraic recognition subroutine must use certified degree, height,
and precision bounds. A heuristic integer-relation search would not
establish this theorem. Likewise, a feasible point of the rational outer
LP alone need not satisfy the original cone system exactly.

## 7. Prior comparison, significance, and limits

The [common-range prior audit](common-range-fpt-prior.md) compares the
decision theorem with fixed-dimensional convex polynomial algorithms,
implicit convex programming, and exact mixed-integer convex quadratic
programming. Those comparisons remain necessary here. The additional
ingredients are classical: the low-dimensional critical-point arithmetic
bounds above, the polynomial-time exact rational QP theorem of
[Kozlov--Tarasov--Khachiyan](https://www.mathnet.ru/eng/zvmmf5189),
[Hoffman's linear error bound](https://nvlpubs.nist.gov/nistpubs/jres/049/4/V49.N04.A05.pdf),
and Kannan--Lenstra--Lovasz algebraic recognition. The primary Hoffman
paper and the relevant Jeronimo--Perrucci--Tsigaridas argument were read
for this note; the QP and recognition imports are also documented in the
linked earlier recovery notes.

The result closes a substantive decision-to-output gap: exact feasibility
can now return an original continuous point, even when every feasible
point is irrational. The integer variables and potentially many affine
continuous variables do not force a product of algebraic degrees. A
possible use is an exact certification layer for models depending
nonlinearly on a few continuous aggregate features. No practical speedup
or useful numerical precision estimate has been established.

This result does not contradict the matrix-span output lower bounds.
Common range is a different, stronger restriction on curvature, and its
dimension grows in those examples. Nor does feasible recovery by itself
give exact optimization or classify nonattainment of an objective.
Those require separate arguments.

The independent reviewer reconstructed the argument and then checked the
complete manuscript. That review found no substantive gap. The reviewer
contributed the inactive-box simplification and the primary-source
comparison; the review records this overlap. Two minor clarifications
were incorporated: native PSD norm queries remain PSD rows, and quadratic
evaluation uses the square of the common algebraic denominator.

The targeted command

```text
python research-20260927/check_common_range_witness.py
```

passed 91 exact outward-QP cases, spanning four active-set patterns. It
checks feasibility, norm monotonicity, the repair estimate, and the
projection inequality by exact symbolic arithmetic. Two further checks
show that the two-stage canonical point can differ from the original
minimum-norm point, and that an affine fiber can retain the nonlinear
coordinate's quadratic field. These examples test the recovery argument;
they do not verify the universal perturbation bounds, KLL, or the FPT
complexity theorem. No project-wide checks, CI inspection, or Lean
formalization were performed.

A targeted inline `python -` document check also passed for this note and
its review: 11 local links, paired math delimiters, whitespace, control
characters, and final newlines. These formatting checks do not establish
the mathematical claims.
