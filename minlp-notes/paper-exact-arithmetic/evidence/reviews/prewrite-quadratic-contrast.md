# Prewriting audit: quadratic arithmetic and representation contrasts

Date: 2026-10-05. Internal analytic review of coverage entries Q1–Q7 and
the optional corank-one, number-field QP, rational infeasibility, and
coefficient-precision comparisons. No browsing, literature discovery,
experiment, or mathematical script rerun was performed. No source note or
manuscript was edited.

## Verdict and integration decisions

No incorrect mathematical claim was found in the reviewed final sources.
Their boundary theorems can enter the comparison appendix with the
contracts below. One source has a typesetting defect: the negative
one-half term in equation (3) of `two-span-rationality-frontier.md` contains
a malformed command. Typeset it as \(-\tfrac12\) in the manuscript.

Use \(L\) for total binary input length, \(n\) for continuous dimension,
and \(h\) for native constraint Hessian span. The objective Hessian is
excluded from \(h\). If the root requires a generic structural symbol
\(k\), define \(k=h\) in this appendix; do not confuse it with integer
dimension or the number of constraints. Count full matrices and all
coefficients in \(L\). Distinguish these models explicitly:

- Native PSD quadratic rows have Hessians \(Q_i\succeq0\). Squared SOC
  rows can have indefinite Hessians, even when the cone-defined set is
  convex. The rational-output threshold concerns the native PSD model.
- Constraint Hessian span controls algebraic degree; it is different from
  common Hessian range, number of nonlinear rows, or the span of polynomial
  Hessian fields for quartics.
- A joint field representation, separate actual-coordinate minimal
  polynomials, an ordinary sparse coefficient list, and an implicit
  equation or arithmetic circuit are distinct outputs.
- Continuous span after fixing integer variables does not control the
  size of an integer assignment or replace the full native span in a
  mixed-integer reduction.

The sharp QCQP degree formula is
\[
 \mathcal B(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns.
 \tag{1}
\]
It is not always \(2^h\binom nh\), and not always the support-size
\(h\) count. When \(n=h=3\), support two gives 12 and support three
gives 8. The canonical optimizer is the unique optimizer of least
Euclidean norm in the **original coordinates**. Arbitrary points of an
optimal face can be transcendental and are not covered.

The sources supply no ordinary decision or approximation lower bound from
large degree or large coefficient height. The explicit block and Pell
families have compact exact descriptions. All output impossibility claims
must name the required expanded format. The primal/dual certificate
theorem is a size and verification result, not a proved construction of
all exposing multipliers. Its verifier certifies global optimality, not
the minimum-norm selection.

The scope is arithmetic comparison and representation. This audit does
not authorize a full Hessian-span, SOCP, or nonconvex optimization survey.
External algebraic sampling, recognition, generic-degree, attainment, and
exact rational LP/QP contracts are listed for Luna verification at the end.
No unresolved local mathematical claim was found, conditional on those
stated established tools. The original inequalities and dimensional
assumptions must remain visible when those tools are cited.

## Q1: the sharp native-PSD rational-output threshold

Consider
\[
 F=P\cap\{q_i\le0:1\le i\le m\},\qquad
 q_i(x)=\tfrac12x^{\mathsf T}Q_ix+a_i^{\mathsf T}x+c_i,
 \quad Q_i\succeq0,
\]
where all data and the polyhedron \(P\) are rational. If \(h\le2\),
every nonempty \(F\) has a polynomial-size rational point, rational
points are dense in \(F\), and \(\operatorname{aff}F\) is rational.
A deterministic polynomial-time algorithm returns a rational feasible
point or reports emptiness, using the established fixed-span exact
feasibility/value algorithm and exact rational convex QP. There is no
boundedness, Slater, positive-definite-Hessian, or affine-hull promise.

### The tangency lemma, with its essential cancellation

For two rational convex quadratics suppose
\[
 q_1(p)=q_2(p)=0,\qquad q_1+t_0q_2\ge0
 \text{ globally},\qquad t_0>0.
 \tag{2}
\]
There is a positive rational multiplier with the same property and
polynomial bit length. Put \(W=\ker Q_1\cap\ker Q_2\). Stationarity
gives \((a_1+t_0a_2)\vert_W=0\). If these restricted linear forms
are not both zero, a rational basis vector recovers
\(t_0=-a_1^{\mathsf T}w/(a_2^{\mathsf T}w)\), so the multiplier is
already rational. Otherwise discard the rational common-kernel
directions. On a rational complement, \(Q_1+Q_2\succ0\), and
\[
 f(t)=\min_x(q_1+tq_2)
 =c_1+tc_2-\tfrac12(a_1+ta_2)^{\mathsf T}
                       (Q_1+tQ_2)^{-1}(a_1+ta_2)
 \in\mathbb Q(t).
\]
At \(t_0\), \(f(t_0)=f'(t_0)=0\); the derivative is \(q_2(p)\).
If \(f\equiv0\), choose \(t=1\). Otherwise diagonalize the two
PSD matrices by a real congruence, normalizing their diagonal pairs to
\((1-d_j,d_j)\), \(0\le d_j\le1\). Division of each scalar term
gives
\[
 f(t)=a+bt-ct^2-\sum_{j=1}^r\frac{\rho_j}{t-\sigma_j},
 \quad c\ge0,\quad\rho_j>0,\quad
 \sigma_1<\cdots<\sigma_r\le0.
 \tag{3}
\]
Combine equal poles and remove zero residues. These are exactly the
poles of the reduced rational function; the diagonalization is used only
to prove their signs.

The reduced numerator has degree at most \(r+1\) if \(c=0\), and
exactly \(r+2\) if \(c>0\). Between consecutive poles the function
goes from \(-\infty\) to \(+\infty\), giving \(r-1\) distinct
nonpositive zeros of odd multiplicity. If \(c>0\), another zero lies
to the left of the first pole. Together with the positive double zero,
these exhaust the degree bound. Thus every nonpositive zero is simple,
\(t_0\) is exactly double, and it is the only repeated complex root.
The case \(r=0\) follows directly from the quadratic polynomial; a
nonzero affine polynomial cannot have a double root. Therefore the gcd
of the reduced numerator and its derivative is linear over \(\mathbb Q\),
and \(t_0\) is rational.

Before cancellation a numerator is
\[
 2(c_1+tc_2)\det(Q_1+tQ_2)
 -(a_1+ta_2)^{\mathsf T}\operatorname{adj}(Q_1+tQ_2)(a_1+ta_2).
\]
Its degree and coefficient bits are polynomial in the input length, so
the rational root theorem gives the multiplier's polynomial bit bound.
The raw numerator can have spurious repeated nonpositive roots that
cancel against the determinant. Cancellation **must precede** the
derivative gcd. This is a substantive proof condition.

### Affine faces and the span lift

For two quadratic rows, take the smallest face \(P_0\) of \(P\)
containing \(F\), and a feasible point in \(\operatorname{ri}P_0\).
Such a point exists by averaging one feasible point strict in each
affine row that is not identically tight on \(F\). If a common strict
quadratic point exists in \(\operatorname{aff}P_0\), a sufficiently
short segment toward it gives strict quadratic and remaining affine
inequalities; rational density on the rational affine chart gives a
rational feasible point. Otherwise separate the convex open upper image
of \((q_1,q_2)\) from the negative orthant. The separating normal is
nonnegative, and feasibility forces the separating value to be zero.

If one multiplier is positive, that quadratic's global minimum on the
chart is zero, and its zero set is the rational affine solution space
of its gradient equations. Restrict to it, leaving one convex quadratic
and affine rows. Repeating the strict-point/zero-set argument gives
qualitative rationality; the one-quadratic small-witness theorem gives
polynomial length. If both multipliers are positive, use (2) to obtain
a rational positive multiplier. The aggregate's minimizer space is
rational, and both individual quadratics restrict to affine functions
there, because the aggregate kernel is their common kernel. Rational LP
then gives a point.

For general \(h=2\), the cone generated by the finitely many PSD
Hessians is a pointed two-dimensional cone with two extreme rays
generated by input matrices \(B_1,B_2\). Solve rationally
\(Q_i=\alpha_iB_1+\beta_iB_2\), with \(\alpha_i,\beta_i\ge0\).
The original system is the projection of
\[
 \tfrac12x^{\mathsf T}B_1x\le u_1,quad
 \tfrac12x^{\mathsf T}B_2x\le u_2,quad
 \alpha_i u_1+\beta_i u_2+a_i^{\mathsf T}x+c_i\le0,
 \quad x\in P.
 \tag{4}
\]
Nonnegative coefficients prove both directions of the projection
identity. This gives the two-row result with arbitrary affine rows.
The cases \(h=0,1\) use zero or one epigraph variable. Intersecting
with arbitrarily small rational boxes proves density; approximating an
affine basis by rational feasible points proves rationality of the hull.

### Constructive rational output

The algorithm can find the two cone rays by testing all independent
input pairs. After the lift, minimize each affine row over \(F\) to
detect rows identically tight on \(F\), and restrict to their rational
affine equations. On that chart maximize the common slack \(s\),
subject to \(q_i+s\le0\), every remaining affine row plus \(s\)
being nonpositive, and \(0\le s\le1\). It remains a span-two system.
Only the value or supremum and its sign are needed for this step.

If its value is positive, choose a positive polynomial-bit dyadic
\(\delta\) strictly below it. Keep the **same** closed
\(\delta\)-margin system throughout box doubling and coordinate
bisection. A fixed-span small-point theorem bounds the needed radius
by \(2^{L^{O(1)}}\). On the resulting box a quadratic Lipschitz
constant in the infinity norm is
\[
 R\sum_{i,j}|Q_{ij}|+\sum_i|a_i|.
\]
Bisect to width at most \(2\eta\), where
\(\eta\le\delta/(2M)\) and \(M\ge1\) is a common Lipschitz
bound. Exact feasibility queries retain a half-box meeting the fixed
margin system. Its rational midpoint is feasible for the original
system. Equality rows remain exact through the chart.

If the slack value is zero, first test each unconstrained quadratic
minimum by rational linear algebra. A zero minimum gives its rational
gradient-zero space and leaves one quadratic. Otherwise both exposing
weights are positive, so compute the rational tangency weight using
the common-kernel ratio or the reduced polynomial gcd above. On its
rational minimizer space, solve the remaining rational LP. The
one-quadratic branch doubles boxes and solves exact rational PSD QPs,
returning a rational minimizer once its value is nonpositive. The
classical one-quadratic witness bound limits this loop. The affine-face
restriction is required before the zero-margin alternative; without it,
a blocking affine boundary can masquerade as quadratic tangency.

The algorithm uses fixed-span value/decision, short-point, and exact QP
contracts; qualitative rational density alone does not prove its bit
complexity. A minimum-norm feasible point need not be rational: the
interval \((x-2)^2\le2\) contains 1 but has canonical point
\(2-\sqrt2\). The algorithm selects a point suitable for rational
output, rather than changing that canonical point's arithmetic.

## Q1 and Q6: explicit irrational and spectrahedral boundaries

For \(r=\sqrt[3]2\), let
\[
 q_1=x^2-y,\quad q_2=y^2-2x,\quad
 q_3=(x-y)^2-2x-y+4.
\]
Their rank-one PSD Hessians are independent. All vanish at
\(p=(r,r^2)\), and positive weights
\((2r-1,r^2-1,1)\) give
\[
 \sum_i\lambda_iq_i
 =(X-p)^{\mathsf T}
       \begin{pmatrix}2r&-1\\-1&r^2\end{pmatrix}(X-p).
 \tag{5}
\]
The determinant is three, so the feasible set is exactly \(\{p\}\).
This proves span three is the sharp rational-existence boundary. Three
positive definite ellipsoids also suffice: set
\(R_i=3q_i+q_1+q_2+q_3\). Their quadratic matrices are
\(\bigl(\begin{smallmatrix}5&-1\\-1&2\end{smallmatrix}\bigr)\),
\(\bigl(\begin{smallmatrix}2&-1\\-1&5\end{smallmatrix}\bigr)\), and
\(\bigl(\begin{smallmatrix}5&-4\\-4&5\end{smallmatrix}\bigr)\),
each with determinant nine and strictly negative minimum. With
\(S=\sum_i\lambda_i\), weights
\(\eta_i=(\lambda_i-S/6)/3>0\) reproduce (5).

There is no nonzero rational nonnegative aggregate globally
nonnegative for this system. At \(p\) it would have value and gradient
zero. Rationality and independence of \(1,r,r^2\) force its quadratic
and linear coefficients to vanish; the positive traces of the native
Hessians then force every nonnegative weight to be zero. The zero margin
is material: positive infeasibility aggregates can be rationalized, as
proved below.

For comparison, the rational SOC pair
\(\|(1,1)\|\le t\), \(\|(t,t)\|\le2\) forces \(t=\sqrt2\).
Its squared rows are \(2-t^2\le0\), \(2t^2-4\le0\), with the
right-hand-side sign conditions retained. One squared Hessian is
negative, so it is outside the native PSD theorem.

### One scalar affine rational PSD pencil

A rational symmetric pencil \(A+xB\), with no auxiliary scalar
variables, has feasible set \(\{\alpha\}\) exactly when \(\alpha\)
is totally real algebraic. The least matrix size is exactly
\(2d\), where \(d=\deg_{\mathbb Q}\alpha\).

Remove the rational common kernel of \(A,B\) by congruence. At the
feasible parameter let \(C=A+\alpha B\succeq0\). For nonreal \(z\),
a complex kernel vector of \(C+(z-\alpha)B\) would satisfy
\(v^*Cv+(z-\alpha)v^*Bv=0\). The two quadratic forms are real,
so \(v^*Bv=0\), then \(Cv=0\), then \(Bv=Av=0\), a
contradiction. Thus the reduced determinant is nonzero and real-rooted.
It vanishes at \(\alpha\), which proves algebraicity and total
reality. The feasible matrix is singular, or positivity would persist
on an interval.

That determinant has a double root at \(\alpha\). At corank at least
two its derivative vanishes by the adjugate formula. At corank one,
write a displacement in a kernel-adapted basis as
\[
 \begin{pmatrix}C_1+tE&tb\\tb^{\mathsf T}&t\beta\end{pmatrix}.
\]
If \(\beta\ne0\), a sufficiently small \(t\) of the proper sign
has positive Schur complement and is feasible, contradicting
uniqueness. Hence \(\beta=0\), and the derivative vanishes again.
The minimal polynomial's square divides the determinant; consequently
the matrix size is at least \(2d\).

For sufficiency, in \(K=\mathbb Q(\alpha)\) use the power-basis
multiplication matrix \(M\) and trace matrix
\(G_{ij}=\operatorname{Tr}_{K/\mathbb Q}(\alpha^{i+j})\).
If \(V\) is the real Vandermonde matrix of all conjugates, then
\(G=V^{\mathsf T}V\succ0\) and \(VM=\operatorname{diag}(\alpha_j)V\).
For rational \(r\) not a conjugate set
\[
 L_r(x)=G(M-xI)(M-rI)^{-1}
 =V^{\mathsf T}\operatorname{diag}
           \left(\frac{\alpha_j-x}{\alpha_j-r}\right)V.
\]
Choose rational isolating endpoints \(r_-<\alpha<r_+\), with no
other conjugate between them. Then
\(\operatorname{diag}(L_{r_-},L_{r_+})\succeq0\) exactly at
\(x=\alpha\). Its size is \(2d\), its corank is two, and its
determinant is \(\det(G)^2f(x)^2/[f(r_-)f(r_+)]\), including a
nonmonic minimal polynomial \(f\). Rational traces, inverses, and
determinant bounds give polynomial coefficient bit length in the
explicit polynomial and isolator. Auxiliary variables change the theorem.

### Optional corank-one classification

If a rational affine pencil \(A_0+\sum_i x_iA_i\) has singleton
feasible set \(\{p\}\) and corank one at \(p\), its coordinate
field has exactly one real embedding. Normalize an algebraic kernel
generator \(v\) to have one coordinate equal to one. A nonzero
\(v^{\mathsf T}A_iv\) would create a positive definite nearby matrix
by the same Schur argument, so all these rational quadratic forms,
including that of \(A_0\), vanish at \(v\). The system \(A(x)v=0\)
has unique real solution: any homogeneous parameter direction would
preserve the kernel and remain PSD for sufficiently small displacements
of both signs. Gaussian elimination therefore gives
\(\mathbb Q(p)=\mathbb Q(v)\). For any real embedding \(\sigma\)
of this field, put \(u=\sigma(v)\). The rational quadratic identities
give \(u^{\mathsf T}A(p)u=0\) at the **original** PSD matrix.
Thus \(u\) belongs to its one-dimensional kernel, and normalization
forces \(u=v\). The embedding is the given one. Do not infer that a
conjugate matrix remains PSD.

Conversely the power-basis construction in `few-quadratic-unbounded-degree.md`
realizes every field with one real embedding by a two-parameter singleton
corank-one pencil. Its key identity is
\(R=(C-\alpha I)^{\mathsf T}B(C-\alpha I)\), with kernel
\(\mathbb R(1,\alpha,\ldots,\alpha^{d-1})\), and \(B\) rational
positive definite on the nonreal eigenspace and satisfying
\(v(t)^{\mathsf T}Bv(t)\equiv0\) modulo the minimal polynomial.
Such a \(B\) exists by rational density in that rational linear space:
the real target gives zero on the real eigenvector and equal positive
values on the real and imaginary parts of each complex pair. Set
\(Q_0=C^{\mathsf T}BC\),
\(Q_1=-(C^{\mathsf T}B+BC)\), \(Q_2=B\), and \(w=Bv(\alpha)\).
Irreducibility makes \(w\ne0\), since otherwise every rational row
of \(B\) would vanish on the power basis. The vectors \(w,C^{\mathsf T}w\)
are independent: a real eigenvector dependence would have eigenvalue
\(\alpha\), and pairing with every other right eigenvector, and with
\(v(\alpha)\), forces \(w=0\). Every pencil member has zero quadratic
form at \(v(\alpha)\); PSD therefore forces its kernel equation
\((\alpha-s)C^{\mathsf T}w+(t-s\alpha)w=0\). Independence gives
\((s,t)=(\alpha,\alpha^2)\), and \(R\) proves feasibility there.
The rational case uses
\(\bigl(\begin{smallmatrix}1&x\\x&0\end{smallmatrix}\bigr)\).
Each coordinate subfield also has one real embedding: the total degree
is odd, and every real embedding of a subfield extends through an
odd-degree primitive polynomial. In one scalar variable, total reality
and one real embedding together imply rationality. Higher corank and
projections are outside this optional classification.

## Q2: exact degree and height at fixed constraint Hessian span

For a rational convex QCQP with nonempty feasible set and attained
finite minimum, its value and its canonical minimum-norm optimizer
generate a field of degree at most (1). Coordinate annihilators and
primitive minimal polynomials have coefficient bits \(L^{O(h+1)}\).
No Slater condition or zero-dimensional full complex KKT locus is needed.
The universal degree bound is sharp even for strictly feasible compact
instances with positive definite objective and constraint Hessians;
that sharpness statement gives no useful coefficient-size bound.

The local extension of the classical degree formula needs the following
proof steps. At the canonical optimizer retain active native rows,
turn active affine inequalities into equalities, and delete inactive
rows. Segment arguments preserve the lexicographic minimum of objective
and original-coordinate squared norm. For every retained native row
add the affine equality given by its difference from a rational linear
combination of a basis of the retained Hessians. These differences vanish
at the optimizer. In the resulting rational chart \(x=x_0+Vu\),
whole retained polynomials span at most \(h\) dimensions.

Minimize \(f+\varepsilon\|x_0+Vu\|^2\), first on rows
\(q_i\le\delta\) for fixed \(\varepsilon>0\), then take
\(\delta\downarrow0\), and finally \(\varepsilon\downarrow0\).
Inner convergence follows from coercivity and strict convexity. Outer
comparison with the canonical optimizer bounds the norms and makes
the objective gap tend to zero, so the limit is that same point.
These are ordered limits; arbitrary simultaneous parameter schedules
are not asserted.

At the strict inner problems choose a minimal positive multiplier
support. Its gradient columns are independent, and the whole-polynomial
span gives \(s\le\min(h,d)\), where \(d\le n\) is chart dimension.
Fix one support along nested subsequences before choosing a coordinate
or linear-combination output. Its full KKT system has bordered Jacobian
\(\bigl(\begin{smallmatrix}M&G\\G^{\mathsf T}&0\end{smallmatrix}\bigr)\),
where \(M\succ0\) and \(G\) has independent columns; the Schur
complement proves nonsingularity. Stationarity has bidegree at most
\((1,1)\) in primal and multiplier blocks; active equations have
bidegree \((2,0)\). The isolated-root multihomogeneous count is
\[
 [U^dT^s](U+T)^d(2U)^s=2^s\binom ds.
 \tag{6}
\]

Counting individual rational specializations is insufficient to bound
a limit's degree. Over the rational function field of the perturbation
parameters, localize the KKT algebra at the Jacobian determinant and
at an output denominator. All remaining roots are isolated reduced
points, so this is a finite reduced algebra of dimension at most (6).
Multiplication by the output has a characteristic polynomial of that
degree. Clearing parameter denominators gives one polynomial identity
valid at all generic regular roots. The implicit function theorem and
continuity extend it to exceptional regular specializations. The
localization is nonzero because any specialized regular root continues
on a real parameter neighborhood.

Take the first nonzero coefficient of the inner parameter, then the
outer parameter. The ordered finite limits give a nonzero rational
annihilator of degree at most (6). This holds for every rational
linear combination of coordinates using the same fixed support.
A primitive-element linear combination therefore bounds the **joint**
field degree, rather than only individual degrees. Its value belongs
to that field. Taking the maximum over supports gives (1), with a
maximizing index \(\min(h,\lfloor(2n+1)/3\rfloor)\), and
\(\mathcal B(n,h)\le3^n\).

The coefficient-height statement needs the separate finite-staircase
elimination and ordered-coefficient proof; the characteristic-polynomial
existence argument alone gives no height bound. Section on coefficient
precision below supplies its arithmetic mechanism. At \(h=0\) the
claim reduces to rational convex QP. For a fixed optimal integer fiber,
the degree bound applies independently of the assignment's magnitude,
but a uniform height bound still needs its encoding length.

Sharpness uses the integral universal KKT incidence, the classical
generic count (6), and Hilbert irreducibility inside a nonempty real
open set of strictly convex instances. The value is primitive because
differentiating it with respect to each independent objective linear
coefficient recovers the corresponding primal coordinate. A seed
\(Q_i=I+e_ie_i^{\mathsf T}, a_i=e_i,c_i=0\),
\(Q_0=I,a_0=-\sum_i e_i\), has optimizer zero and positive
multipliers one; its nonsingular KKT point persists on a real open set.
Rational specialization preserves irreducibility and avoids the finite
denominator exclusions. Additional independent PD Hessians can be added
as strictly slack rows to raise the span from the maximizing support to
the requested \(h\). Luna should verify the exact generic-degree and
integral multivariable Hilbert contracts; no effective short-input
specialization is inferred from this sharpness proof.

## Q3: direct short-input degree and sparse-output lower bounds

The explicit arithmetic block construction suffices for the output
comparison; invoking an effective Hilbert theorem is unnecessary.
For a prime \(p\equiv1\pmod4\), let \(r=p-1\), choose
\(1\le\kappa<p\) with \(\kappa^2\equiv-1\pmod p\), and an integer
\(K>0\) congruent to \(\kappa\pmod{p^2}\). Minimize
\[
 \tfrac12\sum_{j=1}^r jx_j^2-K\sum_{j=1}^r jx_j
 \quad\text{on }\sum_jx_j^2\le1.
\]
The unique optimizer is \(x_j=Kj/(j+\lambda)\), where the positive
\(\lambda\) uniquely solves \(\sum_jK^2j^2/(j+\lambda)^2=1\).
Set
\[
 F(T)=\prod_{j=1}^r(T+j),\quad F_j=F/(T+j),\quad
 P(T)=F(T)^2-K^2\sum_jj^2F_j(T)^2.
 \tag{7}
\]
Modulo \(p\), \(F=T^r-1\) and \(P=T^{2r}\). To verify the latter,
\(P-T^{2r}\) and its derivative vanish at all \(r\) nonzero
field elements, while its degree is below \(2r\). At \(\alpha=-j\),
\(F_j(\alpha)=-\alpha^{-1}\) and
\(F_j'(\alpha)/F_j(\alpha)=r/\alpha\), proving both vanishings.
Moreover
\(P(0)=(r!)^2(1-rK^2)\) has valuation one: if
\(\kappa^2+1=kp\), then \(1\le k\le p-2\) and
\([1-(p-1)\kappa^2]/p\equiv1+k\not\equiv0\pmod p\).
Thus (7) is Eisenstein and \(\deg\lambda=2r\). Every coordinate
recovers \(\lambda=Kj/x_j-j\).

The block value is primitive too. With \(\beta=2v\),
\[
 \beta=-\lambda-K^2\sum_j\frac{j^2}{j+\lambda}.
\]
In the normalized \(p\)-adic valuation, \(v_p(\lambda)=1/(2r)\).
Expansion in \(\lambda\) has constant valuation one; its linear
coefficient and coefficients of powers two through \(r\) are
divisible by \(p\); the coefficient of power \(r+1\) is a unit.
The finite-field sums \(\sum_jj^{1-m}\) prove these statements.
All later coefficients are integral, so the unique least valuation is
\(v_p(\beta)=(r+1)/(2r)\). Since \(r\) is even, that fraction is
reduced. Its denominator forces local ramification degree at least
\(2r\), so \(\mathbb Q(v)=\mathbb Q(\lambda)\).

For increasing primes \(p_i\equiv1\pmod4\), choose
\[
 L_i=\prod_{j>i}p_j,\quad L_it_i\equiv1\pmod{p_i^2},
 \quad1\le t_i<p_i^2,\quad K_i=\kappa_iL_it_i.
\]
Every earlier block polynomial splits over \(\mathbb Q_{p_i}\).
Indeed, when \(q>r\) divides \(K\), substitute
\(T=-j+Kj u\) in its secular equation; after clearing the other
unit denominators it reduces to a nonzero multiple of \(u^2-1\).
Its two simple roots lift by Hensel, giving two roots at each distinct
pole residue. The earlier splitting-field compositum therefore embeds
in \(\mathbb Q_{p_i}\), while the new polynomial is Eisenstein
there. Inductively the joint field degree is
\[
 D=\prod_{i=1}^h2(p_i-1),\qquad n=\sum_i(p_i-1).
 \tag{8}
\]
Pairwise trivial field intersections would not alone prove this product.
Squarefree reduction would not prove splitting: the reduction is a
square; the pole rescaling is required.

Positive rational weights preserve the block optimizers. A short
primitive value weight exists by embedding collisions: at most
\((h-1)D(D-1)/2\) integers fail for
\(\sum_i t^{i-1}v_i\), so choose
\(1\le t\le1+(h-1)D(D-1)/2\). This is an existence choice, with
\(O(h^2\log p_h)\)-bit coefficients. A deterministic larger weight
is also given in the source: conjugate bounds and an integer
discriminant separation bound make the last differing term dominate
all earlier ones. Its coefficient bound is
\(O((hp_h^4+h^2p_h^3)\log p_h)\). The direct source construction is
polynomial time in \(n,h\); the smaller weight is not claimed
polynomial-time discoverable.

All constraint Hessians can be PD. For weights \(w_i=t^{i-1}\), put
\(A=K_{\max}p_h^2\) and \(\eta=1/(2hw_hA)\), and replace the
block balls by
\[
 \|x_i\|^2+\eta\sum_{j\ne i}\|x_j\|^2
                        -1-\eta(h-1)\le0.
\]
Their mixing matrix \((1-\eta)I+\eta\mathbf1\mathbf1^{\mathsf T}\)
is invertible, so the span remains exactly \(h\). At the old
optimizer the new multipliers are
\[
 \mu_i=\frac{w_i\lambda_i-
       \eta\sum_jw_j\lambda_j/[1+\eta(h-1)]}{1-\eta}>0,
\]
using \(1<\lambda_i<A\). Convex KKT and strict objective convexity
preserve the unique optimizer and value. The feasible set is changed;
no equality of feasible sets is asserted.

For the existential short weighting, the dense input satisfies
\[
 L=O((h+1)n^2[1+h^2\log(p_h+1)]).
\]
For fixed \(h\), choose its primes in arbitrarily large intervals
\([R,2R]\). Then \(L=O_h(R^2\log R)\), whereas
\(D\ge[2(R-1)]^h\). A proposed bound \(f(h)L^C\) for dense
minimal-polynomial output fails by fixing \(h>2C\) and letting
\(R\) grow. For the deterministic larger weighting the input is
\(O_h(R^6\log R)\), and \(h>6C\) suffices. The prime-counting
dependency is only existence of arbitrarily many primes one modulo four
in such intervals, not a claim of a new prime algorithm.

### Ordinary sparse minimal polynomials are also large

For a degree-\(D\) polynomial \(P\), the coefficient of \(X^j\)
in \(P(X-t)\) is a nonzero polynomial in \(t\) of degree \(D-j\).
At most \(D(D+1)/2\) integers make any coefficient vanish. Some
\(0\le t\le D(D+1)/2\) makes all \(D+1\) coefficients nonzero.
Integer translation preserves irreducibility and primitive content.
An objective constant shift makes the actual value's minimal polynomial
dense. A short primitive linear combination of one coordinate from
each block can be made an **actual first input coordinate** by a
unimodular row shear, and another integer shift makes its minimal
polynomial dense too. The shear and its inverse preserve PD Hessians,
span, compactness, strict feasibility, and uniqueness. Their coefficients
have \(O(h^2\log(p_h+1))\) bits, preserving the short input bound.

This proves no \(f(h)L^C\) time bound for always printing ordinary
sparse minimal polynomials of the actual value, or separate minimal
polynomials for the actual input-coordinate optimizer. It does not
cover shifted bases, nonminimal sparse annihilating multiples, polynomial
circuits, another primitive generator with coordinate maps, field
towers, or implicit systems. The short shifts and primitive shear are
existence choices, which suffice for an output-length contradiction.

The independent feasible-output variant from
`few-quadratic-unbounded-degree.md` uses odd-degree prime binomial
singleton blocks. Its joint degree is \(d^k\), in dimension
\(n=k(d-1)\) and span \(h=3k\). Successive Eisenstein arguments
at distinct radicand primes, where the earlier fields are unramified,
prove the product degree. Over \(\mathbb Q(\zeta_d)\), independent
rotations and the monomial basis show the sum of radicals is primitive.
Replace a first input coordinate by \(R+\sum_i\alpha_i\), with
\(R=1+\sum_i a_i\). Every conjugate has positive real part, so real
linear and conjugate-pair quadratic factors all have strictly alternating
coefficients; their product has every coefficient nonzero. For fixed
\(k\) the input length is \(O_k(d^2\log d)\), yielding the same
no-FPT coefficient-list obstruction. This is a parallel feasible-output
construction, rather than a QCQP value example.

## Q4: a single quartic row does not inherit the quadratic bound

For distinct positive rational primes \(p_i\), minimize \(t\) subject
to
\[
 \sum_i(x_i^4-4p_ix_i)-t\le0,\quad
 1\le x_i\le p_i,\quad -3\sum_ip_i^2\le t\le0.
\]
There is one globally convex nonlinear row. Its unique optimizer has
\(x_i=p_i^{1/3}\) and value \(-3\sum_i p_i^{4/3}\). The identity
\[
 x^4-4px+3p^{4/3}
 =(x-p^{1/3})^2(x^2+2p^{1/3}x+3p^{2/3})
\]
proves uniqueness. The point \(x_i=3/2,t=-1\) is strictly feasible.
On the \(x\)-box the quartic's Hessian is at least \(12I\); the
epigraph polynomial itself has a zero \(t\)-curvature direction.

Over \(K=\mathbb Q(\zeta_3)\), the splitting-field group of the
prime cube roots embeds in \(\mathbb F_3^n\). If its image were a
proper subspace, a nontrivial monomial in the radicals would be fixed.
Its cube would be a rational prime product. Taking the norm
\(K\to\mathbb Q\) forces \(3\mid2a_i\) for every monomial
exponent \(a_i\in\{0,1,2\}\), a contradiction. Thus all independent
rotations occur; they prove linear independence of the radicals over
\(K\) and trivial stabilizer of any nonzero rational weighted sum.
The displayed value has degree exactly \(3^n\) over \(\mathbb Q\).
This proof includes the prime three.

The one row spans a one-dimensional family of polynomial Hessian
matrices, but its coefficient-matrix span and the span of its Hessian
values have dimension \(n\). Only the weaker row-count or field-family
interpretation is refuted. Its exact PSD quadratic lift introduces
\(x_i^2\le y_i\) and \(\sum_i y_i^2-4\sum_i p_ix_i\le t\);
the Hessian span is \(n+1\), consistent with the quadratic theorem.
Degree is exponential in dimension and superpolynomial under ordinary
expanded encodings; it is not uniformly exponential in total input
length. A short radical sum still describes the value. No comparison
hardness or small-gap claim follows from its degree.

## Q5: one-field primal, dual, and reduction certificates

For the rational convex QCQP above with finite optimum, let \(p\) be
its canonical optimizer. There exists a primal/dual certificate of
length \(L^{O(h+1)}\) in the single field
\(K=\mathbb Q(p)\), of degree at most (1). At most \(h\) curved
reduction records precede a final KKT record. An exposing record uses
at most \(n+1\) positive native and polyhedral multipliers together;
the final record uses at most \(n\). A deterministic verifier is
polynomial in input and certificate length. The theorem is existence
and verification; no algorithm for constructing the entire multiplier
sequence is proved by it.

Supply \(p\) in one isolated real field and check every original
constraint. Add all native tangents
\(\ell_i(x)=q_i(p)+\nabla q_i(p)^{\mathsf T}(x-p)\le0\) to the
original polyhedron; convexity ensures all feasible points remain.
For a current polyhedron \(A_jx\le b_j\), a reduction record satisfies
\[
 \lambda,\mu\ge0,\quad\sum_i\lambda_i=1,\quad
 \lambda_iq_i(p)=0,\quad\mu_r((A_jp)_r-(b_j)_r)=0,
 \quad\sum_i\lambda_i\nabla q_i(p)+A_j^{\mathsf T}\mu=0.
\]
Put \(H_j=\sum_i\lambda_iQ_i\),
\(v_j=\sum_i\lambda_i\nabla q_i(p)\), and add exact equations
\(H_j(x-p)=0\), \(v_j^{\mathsf T}(x-p)=0\). Indeed,
\[
 \sum_i\lambda_iq_i(x)
 =\tfrac12(x-p)^{\mathsf T}H_j(x-p)
      +\sum_r\mu_r((b_j)_r-(A_jx)_r),
\]
which is nonnegative on the current polyhedron and nonpositive on
original feasible points. Both nonnegative terms vanish there, proving
the records preserve **all** original feasible points. Complementarity
is necessary for this identity. The new section need not be a face of
the polyhedron in the elementary polyhedral sense.

The terminal nonnegative multipliers satisfy stationarity for the
objective, with the same complementarity. Their exact identity is
\[
 f(x)-f(p)=\tfrac12(x-p)^{\mathsf T}
                  (Q_0+\sum_i\lambda_iQ_i)(x-p)
       -\sum_i\lambda_iq_i(x)
       +\sum_r\mu_r((b_t)_r-(A_tx)_r).
 \tag{9}
\]
Every term is nonnegative on the original feasible set. This is the
complete optimality soundness argument; the verifier need not establish
Slater, minimal norm, a minimal face, or an actual span drop.

For existence, native rows whose restricted Hessian vanishes are already
affine and enforced by the added tangents. If the curved rows have a
relative strict point, KKT finishes. Otherwise a nonnegative convex
alternative gives a normalized aggregate minimized at \(p\) with value
zero. Polyhedral first-order optimality supplies the record above.
At minimum positive support its multiplier columns are independent,
so Cramer's rule yields a solution in \(K\), with support at most
\(n+1\). The restricted aggregate Hessian is a nonzero PSD positive
combination. Restriction to its kernel kills a nonzero element of the
native Hessian span, reducing that span dimension by at least one.
At most \(h\) such records are needed. Final basic stationarity gives
support at most \(n\).

Use absolute logarithmic heights throughout the \(h\) rounds:
\(H(ab)\le H(a)+H(b)\), \(H(a+b)\le H(a)+H(b)+\log2\), and
\(H(\det M)\le r^3B+\log(r!)\) for an \(r\)-square matrix with
entry heights at most \(B\). Each round costs a fixed polynomial
factor in \(L\); thus all heights remain \(L^{O(h+1)}\).
Convert to a primitive power basis only once. Vandermonde Cramer's rule
over all embeddings bounds rational coordinate coefficients by a
polynomial in field degree and element heights, with no normal-closure
degree factor. Exact polynomial arithmetic and signs at the one isolated
root verify the certificate. Separate coordinate isolators alone would
not provide this polynomial joint-checking contract.

### Constructive common-field recovery

Given a selected tuple \(\beta\), a joint-degree bound \(D\),
coordinate minimal-polynomial bit bound \(H\), and a certified
polynomial-cost approximation oracle for that same tuple, a deterministic
algorithm with overhead polynomial in \(n,D,H\) constructs a primitive
generator and all coordinate maps. KLL recognition is the established
external input. Search the \(O(nD^2)\) linear forms
\(\alpha_k=\sum_j k^{j-1}\beta_j\),
\(0\le k\le(n-1)D(D-1)/2\). Embedding collisions show one is
primitive; recognition of all candidates identifies the largest degree,
which is the actual joint degree \(d\).

For each coordinate recognize \(\alpha+s\beta_i\) for
\(s=0,\ldots,d\), with minimal polynomial \(p_s\) and degree
\(e_s\mid d\). Interpolate the polynomials
\(p_s(T)^{d/e_s}\), not the minimal polynomials themselves. These
are exactly the specializations of
\[
 R_i(S,T)=\operatorname{Norm}_{K(S)/\mathbb Q(S)}
                                  (T-\alpha-S\beta_i).
\]
The powers correct degree drops at exceptional samples. Differentiate
\(R_i(S,\alpha+S\beta_i)=0\) to obtain
\[
 \beta_i=-\frac{\partial_SR_i(0,\alpha)}{p'(\alpha)},
\]
and invert \(p'\) modulo the primitive minimal polynomial \(p\).
This produces all coordinate maps with rational polynomial arithmetic;
no number-field factorization or product of separate coordinate degrees
is used. Leading-coefficient clearing makes the input linear forms
integral, conjugate bounds control recognition heights, and ordinary
interpolation and determinant bounds control all subsequent bits.
Joint degree alone is insufficient without the selected-point oracle
and effective heights. This constructs primal output, not the exposing
multiplier sequence in (9).

## Optional rational infeasibility certificates

Every infeasible rational native PSD quadratic system, with affine rows
included as zero-Hessian rows, has rational nonnegative normalized
weights, at most \(n+1\) positive, a rational point \(z\), and rational
\(\gamma>0\) satisfying
\[
 \sum_iw_iq_i(x)=\gamma+\tfrac12(x-z)^{\mathsf T}H(x-z),
 \quad H=\sum_iw_iQ_i\succeq0.
 \tag{10}
\]
The total length is \(L^{O(h+1)}\). A rational verifier checks
\(w\ge0\), \(\sum_iw_i=1\), \(Hz=-\sum_iw_ia_i\), and
\(\gamma=\sum_iw_ic_i+\tfrac12(\sum_iw_ia_i)^{\mathsf T}z>0\).
The certificate is not a proof of integer infeasibility when the real
system is feasible.

The real positive aggregate is established prior. For the parameter-size
refinement, minimize \(\max_iq_i(x)\) by an epigraph. Classical native
convex quadratic attainment makes its value \(\alpha>0\), and strict
epigraph feasibility gives normalized KKT weights. A basic system uses
at most \(n+1\) positive weights, in the canonical epigraph optimizer's
field. Degree and height estimates bound its positive weights and
\(\alpha\) below by \(2^{-L^{O(h+1)}}\).

On its positive support \(I\), every positive combination has the
same rational kernel \(W=\bigcap_{i\in I}\ker Q_i\). Round the
weights **inside** the rational affine equations
\(\sum_iw_i=1\), \((\sum_iw_ia_i)\perp W\). Unrestricted
rounding can violate the second equation and make the aggregate
unbounded below. Rational free-coordinate elimination and dyadic
rounding preserve it exactly. If \(\omega\) is the least positive
weight and \(\rho\) is the least positive eigenvalue of
\(\sum_{i\in I}Q_i\), use \(\eta=\min(1,\omega\rho)\).
For coefficient norm bound \(M\ge1\), weight \(\ell_1\) error
\[
 \varepsilon\le\min\{\omega/4,\alpha\eta^2/(16M^3)\}
\]
preserves the support and makes the aggregate minimum at least
\(3\alpha/4\): the inverse-difference bound gives minimum change
at most \(4M^3\varepsilon/\eta^2\). Rational determinant bounds
give \(\rho\ge2^{-\operatorname{poly}(L)}\), so polynomially many
\(L^{O(h+1)}\) rounding bits suffice. In the all-affine case the
orthogonality equation fixes the aggregate linear term to zero; only
the positive constant must be preserved. Solve the final rational
stationarity equations to obtain \(z\) and \(\gamma\). This is a
polynomial conversion given the initial common-field aggregate;
extracting its original multipliers is a separate task.

The exponential span dependence is necessary for this explicit format.
The infeasible chain \(1/2-x_1\le0\),
\(x_i^2-x_{i+1}\le0\) for \(i<h\), \(x_h^2\le0\) has span
\(h\). At \(x_i=2^{-2^{i-1}}\), all but the last row vanish, so
every normalized positive aggregate margin is at most \(2^{-2^h}\).
Its rational denominator needs at least \(2^h+1\) bits. A scaling-
independent weight version uses the last row \(x_{h+1}\le0\) after
\(h\) squaring rows. With \(d=2^h\) and
\(x_i=t^{2^{i-1}}\), \(t=(1+1/d)/2\), positivity forces
\(\lambda_{h+1}/\lambda_0>2^{d-1}/(3d)\). These two weights alone
need \(\Omega(2^h)\) total bits under any common rescaling. The
chains have short symbolic infeasibility proofs, so no arbitrary-proof
or coNP lower bound is implied. Fixed Hessian span does not bound
aggregate support: a span-one family of \(n\) equal-radius balls
centered at the coordinate vectors can be infeasible with every proper
subfamily feasible, requiring all \(n\) rows in a positive aggregate.

## Optional number-field QP and coefficient precision

For one explicitly represented real number field \(K=\mathbb Q(\alpha)\)
of degree \(D\), rational \(Q\succeq0,C\), and \(b,c\in K\),
the QP \(\min\{x^{\mathsf T}Qx/2+c^{\mathsf T}x:Cx\le b\}\)
can be classified and its minimum-norm optimizer recovered in the
**original field** in polynomial time in the entire explicit input,
including dense field degree and coefficient representations. Independently
encoded algebraic coefficients with an uncontrolled compositum are outside
the statement. Existence of rational active charts alone is not an algorithm.

For a basis of all active normals, the canonical optimizer is the primal
part of
\[
 \begin{pmatrix}Q&C_I^{\mathsf T}\\C_I&0\end{pmatrix}^{+}
                         \binom{-c}{b_I}.
\]
The pseudoinverse is rational with uniformly polynomial bits. Its kernel
is \((\ker Q\cap\ker C_I)\times\{0\}\), and local feasible motions
show the canonical point is orthogonal to it. Basis multipliers may be
signed; these charts are not nonnegative KKT supports. Uniform determinant
and conjugate bounds give a polynomial-bit containing box and coordinate
heights, with no chart enumeration.

Rational normal matrices have a computable Hoffman bound
\(H_A\le2^{\operatorname{poly}(L)}\). The optimum set in that box is
\(\{x\in P:Qx=Qp,c^{\mathsf T}x=c^{\mathsf T}p\}\); its matrix
\((A,Q,-Q,c^{\mathsf T},-c^{\mathsf T})\) has a similarly bounded
Hoffman constant by algebraic norms of nonzero minors. Consequently
feasible objective gap \(\gamma\le1\) implies distance to the optimum
set at most \(T\sqrt\gamma\), with \(\log T\) polynomial in the
input. Round \(b\) outward by \(\varepsilon\), approximate \(c\)
to \(\varepsilon\), and solve the rational QP with norm penalty
\(\delta\|x\|^2/2\). For box norm bound \(U\), objective Lipschitz
bound \(M\), and \(W=2U+MH_A\), its output \(y\) satisfies
\[
 \|y-p\|\le e+\sqrt{2W\varepsilon/\delta+2Ue},\quad
 e=H_A\varepsilon+T\sqrt{W\varepsilon+\delta U^2/2}.
\]
For requested \(\tau\le1\), take
\(E=\tau^2/[16(U+1)]\),
\(\delta=E^2/[8T^2(U^2+1)]\), and
\[
 \varepsilon\le\min\{E/(2H_A),E^2/(16WT^2),
                                  \delta\tau^2/(32W)\}.
\]
The bound is below \(\tau\), with polynomial precision bits. Apply
common-field recognition to \((\alpha,p)\), then rationally convert
the resulting basis back to \(\alpha\). Norm regularization is
essential for approximating that fixed selector.

Affine feasibility over this model is reduced to a sufficiently fine
rational outer approximation on a conditional containing box: the
positive common-violation LP value, if nonzero, lies in \(K\) with a
uniform norm gap. Boundedness below is equivalent to feasibility of
\(Qv+C^{\mathsf T}\lambda=-c,\lambda\ge0\). Its failure separates
the closed polyhedral cone \(\operatorname{range}Q+\operatorname{cone}(C^{\mathsf T})\)
and supplies a direction \(Qh=0,Ch\le0,c^{\mathsf T}h<0\).
Its success gives a lower bound by completing the square. This removes
the feasibility and boundedness promises without an algebraic QP solver.

For coefficients in a field of degree \(D\), height at most \(B\),
and at most \(S\) variables, rows, and listed scalar coefficients,
the sharper span precision statement is
\[
 [K(\theta):K]\le(2n+1)^{\min(h,n)},\quad
 h_{\rm W}(\theta)\le(B+1)S^{c(h+1)},\quad
 \theta\ne0\Longrightarrow
 |\log|\theta||\le D(B+1)S^{c(h+1)}.
 \tag{11}
\]
Coordinate and joint-field analogues hold for the minimum-norm optimizer.
Convexity is required only at the chosen real embedding, and span is
over \(K\), equivalently over \(\mathbb R\) after that embedding.
The rational minimal polynomial has degree at most
\(D(2n+1)^{\min(h,n)}\) and coefficient bits of the final form in
(11), after increasing the absolute constant. The statement requires
finite attainment, and is a height bound rather than a field-operation
algorithm. It uses the older coarse degree count; no assertion that
this precision source itself states the sharper (1) is necessary.

Here is the arithmetic proof mechanism needed if this refinement is
included. After fixed-count affine restriction, the adjugate KKT
equations in \(s\le h\) multipliers have degree \(a=2d\), and
outputs are rational functions with nonzero determinant denominator at
the selected regular roots. Deform each equation to
\(G_i+\beta\lambda_i^{a+1}\). The pure leading monomials give a
staircase quotient of dimension \(J=(a+1)^s\). A basis monomial
times an output numerator or denominator has multiplier degree at
most \(T=a(s+1)\); each reduction decreases total degree. Multiplying
the multiplication matrices by \(\beta^T\) clears the reduction
denominators. For local polynomial norm bound \(C_v\), their
coefficient norms are at most \(C_v^{T+1}\).

The determinant
\(\det(w\beta^TM_A-\beta^TM_B-\zeta\beta^TI)\) is nonzero because
of its top \(\zeta\) coefficient. At archimedean places its norm is
at most \(J!3^JC_v^{J(T+1)}\); at finite places it is at most
\(C_v^{J(T+1)}\). Extract the first nonzero \(\zeta\) coefficient,
then the deformation coefficient, then the original parameters in the
required ordered-limit sequence. Selected-root nonsingularity and the
nonzero denominator preserve the selected output branch. Extraction
only selects coefficient subvectors and cannot increase local norms.
Thus a nonzero annihilator \(P\in K[w]\) has affine joint height
at most
\[
 W_0=J(T+1)E+\log(J!)+J\log3,
 \quad E=D^{-1}\sum_vn_v\log C_v
       \le(B+1)S^{O(1)}.
\]
Joint local norms avoid a factorial sum of separate global heights.
Cauchy's bound and the product formula give
\(h_{\rm W}(\theta)\le W_0+\log2\). For a nonzero output, remove
zero powers from \(P\), then apply Cauchy to \(P\) and its reversal.
Coefficient ratios belong to \(K\) and have height at most the
projective coefficient height, so their selected magnitudes are bounded
by \(\exp(DW_0)\). This gives
\(|\log|\theta||\le DW_0+\log2\), retaining a **linear** field-degree
factor. The argument does not require conjugate optimization problems
to be convex or a normal closure. Repeatedly encoding the primitive
element as a quantified variable would lose this precision refinement.

## Q7: two nonconvex integer variables and Pell height

For \(m\ge1\), minimize \(x\) on
\[
 x^2-5^{2m+1}y^2=1,\qquad x\ge2,y\ge1,
 \qquad x,y\in\mathbb Z.
\]
The explicit binary input length is \(\Theta(m)\), and continuous
Hessian span is zero. Its full quadratic Hessians, after expressing the
equality by two inequalities, are indefinite; it is outside native PSD
and convex mixed-integer results.

Put \(\alpha=9+4\sqrt5\) and
\(\alpha^j=X_j+B_j\sqrt5\). Every positive integral solution of
\(X^2-5B^2=1\) is a unique such power. To prove this special case,
divide a positive norm-one solution by a power of \(\alpha\) until
it lies in \([1,\alpha)\). The quotient remains integral in
\(\mathbb Z[\sqrt5]\), with coefficient \(0\le B<4\).
The possibilities 1,2,3 would require squares 6,21,46, so only the
identity remains. Also
\(B_j\equiv4j9^{j-1}\pmod5\), and
\[
 B_{5j}=5B_j(X_j^4+10X_j^2B_j^2+5B_j^4),
\]
whose parenthesis is one modulo five. Hence
\(v_5(B_j)=v_5(j)\). Feasibility requires \(5^m\mid B_j\), or
equivalently \(5^m\mid j\). The unique optimizer is
\((X_{5^m},B_{5^m}/5^m)\). Since
\(\alpha^j/2<X_j<\alpha^j\), its value and shortest feasible
witness need \(\Theta(5^m)=2^{\Theta(L)}\) bits; every feasible
witness has that lower bound, while others can be arbitrarily longer.
The value's minimal polynomial is linear and has the same coefficient
height obstruction. Repeated fifth powering gives an \(O(m)\)-gate
exact circuit. This is a classical output example, with no decision
hardness or NP nonmembership implication.

## External contracts for Luna to verify

These are existing external tools, not literature findings from this audit.

1. One-quadratic rational small witnesses with arbitrary rational affine
   rows, including the stated mixed-integer extension: Vavasis and
   Del Pia–Dey–Molinaro. The original Vavasis text was not retrieved in
   the source record; verify through a suitable primary statement.
2. Exact rational convex QP in polynomial Turing time, including exact
   optimizer/value recovery and empty/unbounded classification:
   Kozlov–Tarasov–Khachiyan. Ordinary convex-QP approximation alone is
   insufficient for the invoked contract.
3. Finite attainment of native convex quadratic optimization with
   polyhedral and convex quadratic constraints. The rational aggregate
   proof needs attained min-max value to exclude weak infeasibility;
   polyhedral Frank–Wolfe attainment alone is not its full contract.
4. Grigoriev–Pasechnik quadratic-map component sampling, with degree and
   coefficient bounds \(L^{O(r+1)}\) and indefinite auxiliary forms
   allowed. The span-two short strict-point proof introduces a third
   quadratic direction via \(sy\ge1\), preserving a positive margin.
5. Isolated-root multihomogeneous Bezout, including additional positive-
   dimensional components, and Nie–Ranestad's generic QCQP count and
   regularity. The general nongeneric proof here supplies its own
   parameter specialization and ordered-limit argument.
6. Integral multivariable Hilbert irreducibility with finite polynomial
   exclusions. It must meet a real convexity neighborhood; Zariski
   density alone is insufficient. The direct arithmetic block
   lower-bound proof does not need this contract.
7. KLL certified algebraic recognition from a degree bound, a coefficient
   height bound, and sufficiently accurate approximations to a specified
   real number, in polynomial cost in those parameters. Generic integer-
   relation heuristics do not meet this contract.
8. Polynomial univariate sign determination for a root selected by an
   isolating interval, including zeros and possibly reducible supplied
   defining polynomials. Verifiers must not trust a minimal-polynomial
   label or replace joint field consistency by unrelated root isolators.
9. Classical simple-root Hensel lifting, Eisenstein irreducibility and
   total ramification, basic discriminant/unramified-compositum facts,
   and primes one modulo four in arbitrarily large dyadic intervals.
10. Absolute/projective Weil heights, the product formula, ambient-field
    invariance, and primitive polynomial Mahler-height estimates. The
    local determinant and Cauchy arguments above derive the special
    bounds needed here. Hoffman and normal-cone/KKT alternatives are
    established geometry, with the particular scalar identities supplied
    explicitly in the proof.

Do not describe these boundary examples, generic counts, Pell phenomena,
trace forms, or RUR derivative mechanisms as new merely because a source
search found no equivalent statement. Distinct possible contributions are
the native span-two rational tangency extension, parameter-sensitive
certificate encoding, explicit small-coefficient degree products, and
their particular output-format consequences; priority remains a separate
literature question.

## Evidence and verification scope

Read the sixteen assigned notes, coverage Q1–Q7, and the linked active
restriction, ordered perturbation, generic sharpness, and constant-matrix
QP chart arguments needed to check their hypotheses. The mathematical
review reconstructed the formulas and quantified implications above.
Recorded finite diagnostics were not rerun or used as universal proofs.
Only scoped source reads and a document-only `python -` check of this
new review were performed. The check verified final newline, whitespace,
control characters, and balanced inline/display math delimiters, and
passed. No project-wide verification or CI inspection occurred.
