# Convex residuals and a small number of nonconvex linear directions

Date: 2026-10-02. Status: mathematical derivation, independently reviewed.
The coordinate result is a direct instance of the
[generic residual-oracle theorem](fan-exploration.md). The stronger
linear-direction result uses convex relaxations on slabs instead of
corner evaluations. These are structural and complexity deductions; no
novelty claim is made. Prior-art review is in progress.

## Exact convex residual optimization

Write a rational box quadratic as

\[
 F(x)=\tfrac12x^TAx+b^Tx+c,\qquad \ell\le x\le u.
\]

All boxes here are nonempty and compact; fixed coordinates can be
substituted out. Suppose a supplied coordinate set \(C\), of size
\(r\), leaves \(A_{RR}\succeq0\), where \(R\) is its complement.
For rational \(h=x_C\), the residual problem has objective

\[
 \tfrac12z^TA_{RR}z+(b_R+A_{RC}h)^Tz+
 \tfrac12h^TA_{CC}h+b_C^Th+c.
\]

It is a rational convex QP with polynomial encoding length in the
original input and \(h\). An exact rational optimizer and value can be
computed in polynomial bit time, including when the Hessian is singular
and the optimizer set contains a continuum. This uses the exact
Turing-model theorem of Kozlov, Tarasov, and Khachiyan, not a numerical
solver's stopping tolerance. The primary paper defines exact solution as
an exact rational value and an attaining point on page 1320, and constructs
the point in Section 6 on page 1323. Its integer-data formulation covers
rational inputs after denominator clearing, with polynomial bit growth.
[Primary paper](https://www.mathnet.ru/eng/zvmmf5189),
[full text](https://www.mathnet.ru/php/getFT.phtml?jrnid=zvmmf&option_lang=eng&paperid=5189&what=fullt).

The returned residual point also has a simple exact certificate. With
\(Q=A_{RR}\), \(d=b_R+A_{RC}h\), and \(y=Qz+d\), check
\(\ell_R\le z\le u_R\), and check that \(z_i\) minimizes
\(y_iw_i\) on its interval. These box KKT conditions imply, for every
residual feasible \(w\),

\[
 f(w)-f(z)=y^T(w-z)+\tfrac12(w-z)^TQ(w-z)\ge0.
\]

Consequently the generic core theorem gives exact optimization in
\(f(r,\max(1,L/g))\operatorname{poly}(I)\), where
\(L=\max(0,\max_{i\in C}A_{ii})\), provided the optimal core
\(h^*\) is unique and
\(F(x)-F^*\ge g\|x_C-h^*\|^2\). The algorithm does not need
\(g\) as input. Unique optimal core coordinates already imply that
some positive \(g\) exists, by the lemma in the generic theorem.
If \(L=0\), its exact \(2^r\)-corner algorithm needs no growth
assumption. Finding a smallest suitable \(C\) is not part of this claim.

This includes dense residual graphs. For example, let \(n=m^2\),
\(m\ge2\), and put all coordinates in \([0,1]\). The quadratic

\[
 F(h,z)=h^2+\|z\|^2+\frac{(\sum_i z_i)^2}{n}
                 +\frac{4h}{m}\sum_i z_i
\]

has a complete interaction graph. Deleting \(h\) leaves a positive
definite Hessian, whereas making the graph a forest requires deleting
\(n-1\) vertices. Its Hessian on the span of \(h\) and the normalized
all-ones residual direction is
\(\left(\begin{smallmatrix}2&4\\4&4\end{smallmatrix}\right)\),
so it is indefinite. Nevertheless \(F\ge h^2+\|z\|^2\), giving
unique optimum zero and growth constant one. This illustrates strict
structural coverage beyond a small graph feedback vertex set; the
explicit optimum makes it an illustration rather than a hard benchmark.

## Coordinate deletion and negative inertia are different parameters

Let \(k=n_-(A)\) count negative eigenvalues with multiplicity. If
deleting \(r\) coordinates leaves a PSD principal matrix, then
\(k\le r\): the negative eigenspace cannot intersect the residual
coordinate subspace nontrivially. There is no converse bound in terms
of \(k\) alone. For

\[
 A=I-\frac2n\mathbf1\mathbf1^T,
\]

there is exactly one negative eigenvalue. A principal matrix on \(s\)
coordinates is PSD exactly when \(s\le n/2\). Thus the smallest
coordinate deletion set has size \(\lceil n/2\rceil\).

A rotation to negative eigendirections does not preserve the corner
theorem. For a minimal example take \(x,y\in[0,1]\) and

\[
 F(x,y)=2xy+x+y,
 \qquad t=x-y,\quad z=x+y.
\]

The Hessian has eigenvalues \(2,-2\), and

\[
 F=-\tfrac12t^2+\tfrac12z^2+z,
 \qquad |t|\le z\le2-|t|.
\]

The residual optimum is \(z=|t|\), so its value is \(v(t)=|t|\).
The negative spectral coordinate has negative diagonal curvature, but
\(v\) has an upward kink and its unique minimum is at zero, not at
either endpoint of \([-1,1]\). It even satisfies projected quadratic
growth \(v(t)\ge t^2\). The failure comes from the changing residual
feasible set. It invalidates that proof, not all algorithms using linear
nonconvex directions.

## A stronger theorem using convex relaxations on slabs

Suppose a rational decomposition is supplied:

\[
 A=P-T^TDT,\qquad P\succeq0,\qquad
 D=\operatorname{diag}(d_1,\ldots,d_k)\succ0.
 \tag{1}
\]

Here \(T\) has \(k\) rows. Its rows need not be eigenvectors or
coordinate selectors. The encoding length \(I\) includes this
decomposition. Assume all optimizers share one value \(t^*=Tx^*\)
and, quantitatively,

\[
 F(x)-F^*\ge g\|Tx-t^*\|^2\quad(x\in[\ell,u]),\qquad g>0.
 \tag{2}
\]

Put \(d=\max_i d_i\), \(\kappa=\max(1,d/g)\). There is an
algorithm returning a feasible rational point and a certified gap at
most \(2^{-q}\) in

\[
 f(k,\kappa)(I+q+1)^K
 \tag{3}
\]

bit operations, with absolute \(K\). An exact optimizer and value
can be obtained in \(f_1(k,\kappa)(I+1)^{K_1}\). Neither algorithm
needs \(g\). For \(k=0\), solve the convex QP directly.

**Cell relaxation.** Compute the exact interval range of each row of
\(Tx\) over the original box and enclose the image in their product.
Rows with constant range can be substituted into the objective and
removed. For a cell \(B=\prod_i[a_i,b_i]\), use the feasible slab

\[
 X_B=\{x:\ell\le x\le u,\ a\le Tx\le b\}.
\]

Empty slabs can be recognized in polynomial time and discarded. On a
nonempty slab, minimize the convex quadratic

\[
 q_B(x)=\tfrac12x^TPx+b^Tx+c
       -\tfrac12\sum_i d_i[(a_i+b_i)(Tx)_i-a_ib_i].
 \tag{4}
\]

Let \(x_B\) be an exact minimizer and \(L_B=q_B(x_B)\). The
identity

\[
 F(x)-q_B(x)
 =\tfrac12\sum_i d_i((Tx)_i-a_i)(b_i-(Tx)_i)
 \in[0,\delta_B],\qquad
 \delta_B=\tfrac18\sum_i d_i(b_i-a_i)^2
 \tag{5}
\]

shows both that \(L_B\) is a valid lower bound and that its witness
\(x_B\) is original-feasible with \(F(x_B)\le L_B+\delta_B\).
The exact convex-QP theorem applies with the added rational slab
inequalities, including lower-dimensional slabs. This is the essential
replacement for the invalid corner argument.

**Refinement and packing.** Use the isotropic nested grid from the
generic theorem, with maximum side length \(h_j=s2^{-j}\) at level
\(j\). Keep the best feasible value \(U_j\) among all witnesses,
and retain only cells with \(L_B<U_j\). Refine retained cells.
The incumbent and the retained lower bounds give a certified interval;
discarded cells have lower bounds at least every later incumbent.
Put \(\delta_j=kd h_j^2/8\). If the optimum was not already found,
a cell containing an optimal point survives, and its witness gives

\[
 0\le U_j-F^*\le\delta_j.
 \tag{6}
\]

Every retained cell contains the projection \(t_B=Tx_B\), and

\[
 F(x_B)<F^*+2\delta_j,
 \qquad \|t_B-t^*\|<h_j\sqrt{kd/(4g)}.
 \tag{7}
\]

Thus every retained grid cell intersects a ball of that radius. The
number of cells is at most
\((\sqrt{k\kappa}+4)^k\); the constant four safely accounts for
closed endpoints and clipped terminal intervals. Each retained cell
has at most \(2^k\) children. Since
\(O(I+q+1)\) levels make \(\delta_j\le2^{-q}\), and every
relaxation has encoding length polynomial in \(I+j\), this proves
(3). Also \(U_j-L_B\le F(x_B)-L_B\le\delta_j\) for every
retained cell, so the reported interval itself has width at most
\(\delta_j\).

**Exact recovery.** Rational box-QP height bounds give polynomial-bit
denominator bounds \(V\) for \(F^*\) and \(R\) for every
coordinate of \(t^*\). For the latter, choose one polynomial-height
rational global optimizer and multiply by the supplied rational matrix
\(T\). Every optimizer has the same projection by assumption.
Isolate \(F^*\) once the certified interval has width less than
\(1/(2V^2)\). At subsequent levels, try rational reconstruction of
\(t^*\) within distance \(1/(4R^2)\) in each coordinate of the
incumbent projection. At most one denominator-\(\le R\) rational
lies in each such interval. Equation (2) and (6) make all coordinates
recoverable after \(\operatorname{poly}(I)+O(\log\kappa)\) levels.
For each candidate \(t\), solve the exact convex QP with \(Tx=t\),
where the negative term in (1) is constant. Accept only a feasible
solution with objective equal to the already isolated \(F^*\).
This acceptance test is sound even before the reconstruction succeeds.

## Unique optimal linear projections imply qualitative growth

The unique-core lemma extends from coordinate projections to any fixed
linear map \(T\) on a box. For each feasible \(t\), choose a
minimizer over \(\{x:\ell\le x\le u,Tx=t\}\) with the largest
possible number of bound coordinates. On its free coordinates \(J\),
the Hessian restricted to \(\ker T_J\) is positive definite. It is
PSD by second-order necessity. A null direction would have zero linear
and quadratic objective change and could be followed to another bound,
contradicting the choice of optimizer.

Fixing a bound pattern leaves an affine consistency condition on \(t\).
Choose a right inverse on \(\operatorname{range}(T_J)\) and a basis
for \(\ker T_J\). The restricted positive definite stationarity
equations give a unique affine candidate \(x_j(t)\). This includes
the zero-dimensional kernel case. Requiring that candidate to lie in
the box defines a compact polytope \(D_j\) in an affine subspace.
There are finitely many patterns and

\[
 v(t)=\min_{j:t\in D_j}F(x_j(t)).
\]

Each candidate value is quadratic and bounded below by \(F^*\).
If the optimal projection is unique, each piece attaining \(F^*\)
has unique minimizer \(t^*\). The unique-quadratic-minimum lemma
on a compact polytope proved in the generic core note supplies quadratic
growth on each such piece; the other pieces have a positive gap.
Taking the minimum of finitely many positive constants proves (2).
The algorithm does not enumerate these patterns. This existence result
does not bound the conditioning parameter by a small constant.

## Scope and remaining comparison

An exact rational congruence decomposition supplies (1) with
\(k=n_-(A)\), with polynomial encoding length, but its coefficients
can distort \(d/g\). Thus (3) by itself is a theorem for the supplied
representation. It is not yet an intrinsic statement that merely counts
negative eigenvalues. Under full-vector growth \(g_0\), a supplied
\(T\ne0\) gives projected growth at least
\(g_0/\|T\|_2^2\), hence a bound in
\(k,d\|T\|_2^2/g_0\).

The separate [rational spectral normalization](spectral-normalization.md)
constructs in polynomial bit time a rational \(n\)-by-\(k\) matrix
\(U\), where \(k=n_-(A)\), such that
\(\|U\|_2\le1\) and \(A+2HUU^T\succeq0\) for any supplied
positive rational \(H\ge\|A\|_2\). It uses exactly orthogonal
rational Jacobi rotations and an exact projection onto
\(\operatorname{range}(A)\), so singular Hessians are covered.
Set \(T=U^T\) and \(D=2H I\) in (1). With a unique full
optimizer and full-vector growth constant \(g_0\), (2) holds with
\(g=g_0\), since \(\|T\|_2\le1\). Consequently (3) and
exact recovery give the intrinsic bound

\[
 f\!\left(n_-(A),\max(1,H/g_0)\right)\operatorname{poly}(I+q+1)
\]

for certified approximation, and the corresponding bound without \(q\)
for exact optimization. Polynomial preprocessing includes the supplied
bound \(H\)'s bit length. A scalar upper bound within a constant
factor of the spectral norm can also be computed in polynomial bit time;
the displayed theorem only requires a valid supplied \(H\).
The normalization does not make a theorem depending on negative inertia
alone: quantitative growth remains essential to this running-time bound.

## Extension to a bounded rational polytope

The linear-direction theorem also holds with the box replaced by a
nonempty bounded rational polytope
\(X=\{x:Mx\le a\}\), including a lower-dimensional one. Its
inequality description is part of the input. Compute initial bounds on
each coordinate of \(Tx\) by exact linear programming over \(X\).
All subsequent slabs are rational polytopes, and (4)--(7), the packing
bound, and the exact convex residual solve remain unchanged. If every
cell is discarded, the incumbent is already exact and the algorithm
returns it.

For completeness, the rational-height requirement does not rely on box
geometry. Choose an optimizer in a face of \(X\) having the smallest
possible dimension. It lies in that face's relative interior, and the
Hessian restricted to the face's tangent space is positive definite.
Second-order necessity gives PSD; a null tangent direction would have
zero objective change until it reached a smaller face, since \(X\)
is bounded. The affine hull has a rational description using independent
input constraints. A rational particular point and rational tangent
basis therefore have polynomial encoding length. Solving the positive
definite stationary system gives a rational optimizer of polynomial
encoding length by determinant bounds. This also bounds the optimal
value and, after multiplication by rational \(T\), the optimal
projection. The face is used only to prove a height bound, not as an
algorithmic enumeration.

The qualitative projected-growth argument likewise extends: replace
bound patterns by faces of \(X\), and choose a minimal-dimensional
face meeting the slice optimizer set. The restricted Hessian on its
tangent space intersected with \(\ker T\) is positive definite.
Every face gives an affine stationary candidate on an affine consistency
space for \(t\), and its feasibility domain is a compact polytope.
The finite-piece argument then applies verbatim. In particular, a unique
full optimizer supplies positive full-vector quadratic growth, but that
qualitative fact alone does not give a small quantitative parameter.

This extension is a conditioned complexity result for classical
quadratic optimization with linear constraints. The convex chord
relaxation is a standard type of spatial branch-and-bound relaxation;
the point being assessed here is the explicit fixed-parameter bound
under projected growth, not the invention of that relaxation.

The standard one-negative-eigenvalue hardness result is a result for
quadratic programming with linear constraints. The publisher abstract
does not establish a box-only restriction, so it is not used here as a
box-QP hardness claim. Nor does it address this extra growth parameter.
[Pardalos and Vavasis, 1991](https://link.springer.com/article/10.1007/BF00120662).

## Verification

Independent mathematical review checked the convex oracle, the inertia
separation, the failure of spectral corner bounds, the slab relaxation,
and the extension of the qualitative growth lemma. The separate spectral
normalization note records its own construction and checks.

The command
`python research-20261002/new-direction/check_convex_modulator.py`
passed exact-rational checks using SymPy. Its two-variable slab example
uses a unique optimal projection lying at a nondyadic position in the
initial interval. Seven levels and thirteen convex slab solves passed
the relaxation identity, incumbent and lower-bound inequalities, and
projected-growth packing inequalities. It also checked the negative
inertia and exact coordinate-deletion threshold for dimensions 2 through
10, and the dense residual examples for \(m=2,3,4\). The small
diagnostic convex solver enumerates active faces; the theorem instead
uses a polynomial-time convex-QP oracle.

During development, the first temporary-checker run failed because an
empty right-hand side had zero columns; using a zero-by-one matrix fixed
the checker. The final scoped command above passed. No project-wide
checks or CI inspection were performed.

The scoped command
`git diff --check -- research-20261002/new-direction/convex-modulator-qp.md research-20261002/new-direction/check_convex_modulator.py`
passed. A targeted `python - <<'PY'` check also passed for trailing
whitespace, paired mathematical delimiters, and the three local links.
