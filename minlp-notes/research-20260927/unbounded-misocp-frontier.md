# Unbounded mixed-integer SOCP with few squared Hessian directions

Date: 2026-09-27. Status: proof and
[independent adversarial review](unbounded-misocp-review.md) completed;
no gap was found. The projection lemma below uses the reviewed genericity argument
from the [nonconvex certificate note](nonconvex-hessian-span-frontier.md).
The algorithm also depends on the separate
[bounded integer-projection result for SOCP](socp-hessian-span-frontier.md).
Novelty is not established.

The main consequence is exact feasibility of a rational mixed-integer
second-order cone system with no variable bounds, when the number of integer
variables and the span of the squared continuous Hessians are fixed. The
integer witness argument is valid more generally whenever the real projection
onto the integer coordinates is convex. An efficient feasibility algorithm
does not follow from that general witness statement alone.

## 1. Statements and parameters

Let \(w=(z,x)\in\mathbb R^k\times\mathbb R^n\). Consider a rational
system with affine equations, affine weak inequalities, and cone constraints

\[
 \|A_iw+b_i\|_2\le c_i^Tw+d_i,\qquad i=1,\ldots,m.       \tag{1}
\]

Write \(A_{ix}\) and \(c_{ix}\) for the columns and entries belonging
to \(x\). Define

\[
 h=\dim_{\mathbb Q}\operatorname{span}
    \{2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T):i=1,\ldots,m\}.
                                                               \tag{2}
\]

The matrices in (2) may be indefinite. They are the continuous Hessians
of the squared cone residuals

\[
 q_i(z,x)=\|A_i(z,x)+b_i\|_2^2-(c_i^T(z,x)+d_i)^2.
\]

Every cone row is equivalent to \(q_i\le0\) together with the affine
sign condition \(c_i^T(z,x)+d_i\ge0\). The sign condition is retained
throughout. The total explicit rational input length is \(N\ge2\).

**Unbounded MISOCP feasibility theorem.** For every fixed \(k,h\), exact
feasibility of (1) with \(z\in\mathbb Z^k\) is decidable in polynomial
Turing time. The algorithm returns a feasible integer assignment when one
exists. No input bounds, Slater condition, or rational continuous feasible
point are required. This is a polynomial-time result for fixed parameters,
not an FPT running-time claim.

The new ingredient for removing the integer bounds is the following statement.
It does not require second-order cones or positive-semidefinite Hessians.

**Convex-projection witness theorem.** Let

\[
 S=\{(z,x):L(z,x)\le0,\ E(z,x)=0,\ q_i(z,x)\le0\ (i\le m)\},
 \qquad Y=\{z:\exists x\ (z,x)\in S\},                         \tag{3}
\]

where all data are rational, the \(q_i\) have degree at most two, and
their continuous Hessians span dimension \(h\). Suppose \(Y\) is
convex. There is an effective absolute constant \(C\) such that

\[
 Y\cap\mathbb Z^k\ne\varnothing
 \ \Longrightarrow\quad
 \exists z^*\in Y\cap\mathbb Z^k:
 \log_2(2+\|z^*\|_\infty)
       \le N^{C(h+1)(k+1)^4}.                                  \tag{4}
\]

The continuous fibers in (3) may be nonconvex. Combining (4) with the
nonconvex algebraic witness bound gives polynomial-size algebraic feasibility
certificates for fixed \(k,h\), under the convex-projection promise. It
does not give a polynomial-time algorithm for arbitrary (3): even the
case \(k=0,h=1\) can encode Boolean feasibility through a nonconvex
quadratic inequality and affine rows.

## 2. A projection formula with few quantified variables

We prove a structural assertion without assuming convexity. The projection
\(Y\) in (3) has a first-order formula with quantifier block sizes

\[
                 1,\quad 1,\quad h+1,                         \tag{5}
\]

whose atomic integer polynomials have degree and individual coefficient
bit length \(N^{O(1)}\). The Boolean matrix can be very large. We use
the formula only to establish a witness bound, never as input to the final
feasibility algorithm.

### 2.1 Lift the continuous Hessian span

Choose a rational matrix basis \(B_1,\ldots,B_h\) and rational numbers
\(a_{ij}\) with \(\nabla^2_{xx}q_i=\sum_j a_{ij}B_j\).
Introduce \(y_j=\tfrac12x^TB_jx\), and set \(v=(x,y)\).
Then (3) is equivalent to

\[
 v\in P_z,\qquad F_j(v):=\tfrac12x^TB_jx-y_j=0
                       \quad(j=1,\ldots,h).                    \tag{6}
\]

Here \(P_z\) is a polyhedron in \(v\). Its row coefficients are
polynomials in \(z\) of degree at most one, and its constant terms
have degree at most two. This includes all original affine rows and the
affine replacements of every \(q_i\le0\). Computing a rational Hessian
basis increases encoding length only polynomially.

### 2.2 Rank charts for every possible active affine set

Choose any subset of the inequalities defining \(P_z\), make these
equalities, and retain every original affine equality. Write the resulting
system as

\[
                     B(z)v=b(z).                              \tag{7}
\]

For every choice of pivot rows and columns with a square minor
\(\rho(z)\), solve those pivot equations to obtain

\[
                     v=a(z)+V(z)u.                            \tag{8}
\]

The free rows of \(V\) form an identity matrix. The entries of \(a,V\)
are rational functions with common denominator \(\rho\). Add the guards

\[
       \rho(z)\ne0,\qquad B(z)a(z)=b(z),\qquad B(z)V(z)=0.      \tag{9}
\]

They assert that (8) parametrizes exactly the solution space of (7),
including all nonpivot equations. The rank-zero chart uses
\(\rho=1,a=0,V=I\). There are finitely many active sets and rank charts,
at most \(2^{N^{O(1)}}\). Determinant expansion bounds every rational
numerator degree and coefficient bit length by \(N^{O(1)}\), uniformly
over all choices.

For a zero-dimensional chart, include the direct disjunct asserting
\(a(z)\in P_z\), \(F_j(a(z))=0\) for every \(j\), and
\(\|a(z)\|^2\le R\). No multiplier variables are needed in this case.

### 2.3 One finite perturbation grid works for all real parameters

The subtle point is that a perturbation generic at one value of \(z\)
need not be generic at another. We do not choose a single perturbation for
all \(z\). Instead we construct a finite set of choices, the same set
for every \(z\), with polynomial-bit coefficients.

Let \(P_0,\ldots,P_h\) range over arbitrary quadratic polynomials in
the ambient variable \(v\). For \(\epsilon>0\), put

\[
 r_\epsilon(v)=\|v\|^2+\epsilon P_0(v),\qquad
 f_{j,\sigma,\epsilon}(v)
       =\sigma(F_j(v)+\epsilon^2P_j(v))-\epsilon,
       \quad\sigma\in\{-1,1\}.                                \tag{10}
\]

Fix any real \(z\). On each valid positive-dimensional chart (8),
restriction of an arbitrary ambient quadratic to the free coordinates
\(u\) is surjective onto the space of all quadratics in \(u\).
For fixed nonzero \(\epsilon\), this remains true of (10), jointly
for the objective and for any set of constraint indices with one orientation
per index.

The quantitative genericity lemma in the nonconvex certificate note gives,
for generic restricted quadratics, the following properties. All gradients
of active nonlinear rows are independent; more than \(\dim u\) such
rows have no common zero; and at every KKT solution the multiplier Hessian
is nonsingular. The bad coefficients lie in a proper hypersurface of degree
\(2^{N^{O(1)}}\). Its coefficient heights are immaterial here.

For each chart and oriented subset, pull this bad polynomial back through
(10) and (8). At the fixed \(z\), this is a nonzero polynomial in
\(\epsilon\) and the coefficients of the \(P_j\). Choose one nonzero
coefficient in its expansion in \(\epsilon\). The product of these
selected coefficient polynomials over all valid charts and oriented subsets
is nonzero, and its degree is at most

\[
                         D_0=2^{N^{O(1)}}.                     \tag{11}
\]

Crucially, the bound in (11) depends on the input dimensions and degrees,
not on the values or heights of the real specialized coefficients at \(z\).
The number of perturbation coefficients is polynomial in \(N\).
A nonzero polynomial of degree at most \(D_0\) cannot vanish on the
entire integer grid \(\{0,\ldots,\lceil D_0\rceil\}^p\).
Therefore the finite collection \(\mathcal G\) of perturbations with
coefficients in this grid contains, for every real \(z\), one choice
that is generic on all its valid charts for all sufficiently small positive
\(\epsilon\). Each grid coefficient has \(N^{O(1)}\) bits.

This is a pointwise existence statement using one common grid. The selected
grid point can depend on \(z\); no continuous or definable selection is
needed. The eventual formula includes every grid point as a Boolean
disjunct. The grid and its defining bad polynomials are not constructed by
the feasibility algorithm.

### 2.4 Eliminate primal variables by stationarity

Fix one grid point, chart of positive dimension \(d\), and oriented
subset \(J\) with \(s=|J|\le\min\{h,d\}\). Restrict (10) through
(8). With nonnegative multipliers \(\lambda\in\mathbb R^s\),
stationarity has the form

\[
 M(z,\epsilon,\lambda)u=-g(z,\epsilon,\lambda).               \tag{12}
\]

Both sides are rational in \(z\) and polynomial in
\((\epsilon,\lambda)\). On the guard \(\det M\ne0\), use the
adjugate formula to define

\[
 U=-M^{-1}g,\qquad V_*(z,\epsilon,\lambda)=a(z)+V(z)U.         \tag{13}
\]

There is a common polynomial denominator for all coordinates in (13).
Its nonvanishing is explicitly required. Its numerator and denominator
degrees and coefficient bit lengths are \(N^{O(1)}\). This follows
from a fixed number of determinant and polynomial substitutions of matrices
of size at most polynomial in \(N\). We use even powers of the common
denominator to clear inequalities; no sign of a pivot or determinant is
assumed.

The corresponding disjunct requires (9), \(\lambda\ge0\),
\(0<\epsilon<\delta\), the denominator guard, and

\[
 \|V_*\|^2\le R,\qquad V_*\in P_z,\qquad
 |F_j(V_*)+\epsilon^2P_j(V_*)|\le\epsilon\quad(j\le h),        \tag{14}
\]

as well as \(f_{j,\sigma,\epsilon}(V_*)=0\) for the selected
oriented rows. Stationarity is already built into (13). The equality checks
are included for clarity; the reverse implication below only uses (14).

### 2.5 Exact equivalence, including nonclosed projections

Pad multiplier tuples to length \(h\). Put all disjuncts, including
the zero-dimensional direct disjuncts, inside the prefix

\[
 \exists R>0\quad\forall\delta>0\quad
              \exists(\epsilon,\lambda)\in\mathbb R^{h+1}.    \tag{15}
\]

The unrestricted formal universal quantifier uses the implication from
\(\delta>0\). For a direct zero-dimensional disjunct the final tuple
is unused.

Suppose first that \(z\in Y\), and fix a feasible lift \(\bar v\)
in (6). Choose a good grid point for this \(z\). Minimize
\(r_\epsilon\) over

\[
 v\in P_z,\qquad |F_j(v)+\epsilon^2P_j(v)|\le\epsilon.
                                                               \tag{16}
\]

For all sufficiently small positive \(\epsilon\), the original
\(\bar v\) satisfies (16). The objective is uniformly coercive on
that tail, since it is the squared norm plus \(\epsilon\) times a
fixed quadratic. Thus global minimizers exist and, by comparison with
\(\bar v\), have uniformly bounded norms.

At each such minimizer, make all its active affine inequalities equations
and choose a valid chart. All other affine rows are locally strict. At most
one orientation of each band is active. Genericity gives independent active
nonlinear gradients, ordinary KKT multipliers, and nonsingular \(M\).
Therefore the minimizer appears in (13)--(14). Finitely many chart and
support choices allow a fixed one along an infinite sequence
\(\epsilon\downarrow0\). If a zero-dimensional chart occurs infinitely
often, its fixed point satisfies (6) by passage to the limit. In either
case one \(R\) makes (15) true for every \(\delta>0\).

Conversely suppose (15) holds at a fixed \(z\). If any witness uses a
zero-dimensional disjunct, it directly gives a feasible point. Otherwise
take \(\delta=1/\ell\) and the corresponding witnesses in (14).
Their points \(v_\ell\) have norm at most \(\sqrt R\), and
\(\epsilon_\ell\to0\). Pass to a convergent subsequence. The finite
grid \(\mathcal G\) has bounded coefficients, so each
\(P_j(v_\ell)\) is bounded, even if the grid point changes with
\(\ell\). Consequently (14) implies \(F_j(v_\ell)\to0\).
Every point satisfies all rows of the fixed closed polyhedron \(P_z\).
The limit therefore satisfies (6).

Thus (15) defines exactly \(Y\), not its closure. In particular, the
limit keeps \(z\) fixed. The existential bound \(R\) cannot depend on
\(\delta\); this is what excludes fiber points escaping to infinity.
All atomic polynomial degrees and coefficient bit lengths are
\(N^{O(1)}\), proving the structural assertion (5).

The affine case \(h=0\) also follows: no bands or perturbations are
needed, and a minimum-norm point of \(P_z\) is captured by an active
affine chart and its positive-definite norm Hessian. The unused final
variable pads the prefix to the displayed sizes.

Two exact examples show why the rank and boundedness precautions matter.
The system \(zx=0,\ x\ge1\), with the first equality written as two
opposite quadratic inequalities, has \(h=0\) and projection \(\{0\}\).
Keeping only generic-rank charts would lose its only feasible parameter.
Also, the system

\[
                  x^2\le0,\qquad 1-xy\le0,\qquad x+y\ge0
\]

is empty but has points \((x,y)=(1/t,t)\) whose maximum quadratic
violation tends to zero. The last two rows are equivalent to the SOC row
\(\|(2,x-y)\|_2\le x+y\). Thus the fixed radius in (15) is necessary
even for cone systems; vanishing residuals alone would certify a false
feasible fiber.

## 3. Applying the established integer-witness theorem

[Khachiyan and Porkolab (2000), Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
applies to a convex set described by an arbitrary Boolean first-order
formula. If the atomic degrees are at most \(D\), coefficient bit
lengths at most \(L\), and quantified block sizes \(n_1,\ldots,n_\omega\),
the bit bound for an optimal integer point is

\[
             L D^{O(k^4)\prod_j O(n_j)}.                       \tag{17}
\]

The bound does not depend on the number of atomic predicates. Their sentence
immediately preceding the theorem reduces feasibility to optimization by
adjoining an integer coordinate fixed to zero. The theorem allows nonclosed
and lower-dimensional convex sets.

Apply (17) to (15), with this extra coordinate. Its degrees and coefficient
bit lengths are polynomial in \(N\), and its block-size product is
\(O(h+1)\). This gives (4). We do not apply their running-time theorem
to (15): that theorem depends on formula size, and our Boolean matrix can
be exponentially large. Only the size-independent witness bound is used.

The primary theorem and the feasibility reduction were checked in the local
full text, printed pages 207--208. The argument is the same established
integer-witness mechanism as in the
[PSD-Hessian version](unbounded-integer-frontier.md); the replacement here
is the compressed projection formula for indefinite quadratic fibers.

## 4. The unbounded MISOCP algorithm

The real set defined by (1) and the affine rows is convex. Its real projection
onto \(z\) is therefore convex, whether or not the projection is closed.
Its squared form satisfies (3), so (4) supplies a computable integer box
whose bounds have polynomial bit length for fixed \(k,h\). This box
retains at least one feasible integer assignment whenever one exists.

For every integer vector in that box, substitute \(z\) into the squared
system. Its input length is uniformly polynomial in the original length for
fixed \(k,h\). The nonconvex algebraic small-point bound supplies a
uniform continuous-coordinate box retaining a feasible point of every
nonempty fiber. This bound is valid for indefinite quadratics; it requires
neither a Slater point nor a rational feasible vector.

The two boxes reduce the problem to the bounded setting of the
[SOCP projection theorem](socp-hessian-span-frontier.md). That theorem uses
a positive lower bound on each infeasible fiber's minimum squared violation,
together with a rational lifted polyhedral outer approximation of the actual
Lorentz cones. The resulting rational MILP preserves exactly the feasible
original integer assignments inside the chosen box and introduces no new
integer variables. Fixed-integer-dimension MILP feasibility decides it and
returns an original feasible integer assignment.

Every step constructs data of polynomial length for fixed \(k,h\).
Composing the integer and continuous radius bounds can increase the exponent;
no sharp overall running-time exponent is claimed. The algorithm does not
enumerate the perturbation grid, active sets, or projection formula.

## 5. Prior work, significance, and limits

Khachiyan--Porkolab already gives exact integer optimization over convex
semialgebraic sets when the total free and quantified dimension is fixed.
A direct application to \(\exists x\ (z,x)\in S\) retains the entire
continuous dimension in the exponent. The contribution proposed here is its
combination with a projection formula whose quantified dimension depends
on Hessian span, followed by a polynomial-size SOC approximation reduction.
Neither the general integer-witness theorem nor rational approximation of
Lorentz cones is new.

The nonconvex small-point bound has also been identified as a consequence
of established few-quadratic component sampling, through a suitable face of
the lifted polyhedron. Its role here is a radius bound, not a separate
novelty claim. The bounded SOCP theorem's own literature comparison records
the exact scope of its scalar precision and rational approximation inputs.

[Blanco, Magron, and Martínez-Antón (2025), version 2](https://arxiv.org/html/2501.09828v2)
studies exact continuous cone feasibility and radius/discrepancy bounds.
Its displayed general bounds depend on ambient dimension or the number of
affine rows; Section 5 treats multiple cones. This is relevant exact-bit
prior work, but it does not state the unbounded mixed-integer Hessian-span
result above. Exact polynomial feasibility with just one cone also has an
elementary reduction to convex quadratic programming; that special case
must not be claimed as new.

[Hu (2026)](https://arxiv.org/abs/2609.06757) constructs polynomial-size
exact SOCP dual and alternative formulations, including weak infeasibility.
The paper explicitly distinguishes these formulation results from
polynomial-time solvability and polynomial coefficient-bit bounds. Its
abstract was examined here; detailed comparison belongs to the companion
SOCP prior audit. No priority claim follows from these searches.

The practical capability suggested by the theorem is exact preprocessing:
a class of unbounded conic MINLP feasibility problems can, in principle, be
reduced to a rational MILP with the original integer dimension. The proved
bound can be far too large for direct use. Useful instance-dependent radius
and violation bounds, numerical stability, and an efficient implementation
remain open. No computational speedup is established.

The following boundaries are essential.

- Convexity is needed for the projected integer witness theorem. The
  compressed formula itself does not make a nonconvex projection convex.
- Squared cone inequalities require the affine right-hand-side sign rows.
- The final box preserves nonemptiness of an unbounded integer projection,
  not every unbounded feasible assignment.
- The MILP's continuous coordinates need not themselves be feasible for
  the original cones. The claimed output here is an integer assignment
  with a nonempty original continuous fiber. The separate
  [SOCP recovery theorem](socp-exact-witness-recovery.md) now supplies an
  exact algebraic continuous witness after fixing that assignment.
- This note proves feasibility only. General SOCP linear objectives may
  have a finite unattained infimum, for example minimizing \(x\) over
  \(x,y\ge0,\ xy\ge1\). Attainment results for native PSD quadratics
  cannot be transferred to this conic setting. The
  [SOC unboundedness examples](socp-unboundedness-boundaries.md) give further
  limits on transferring native convex quadratic optimization arguments.
  The separate [integer-only objective corollary](integer-objective-misocp.md)
  uses discrete objective values to establish exact optimization in that
  restricted case.

## 6. Verification record

The proof was reconstructed from the genericity, rank-chart, and compact-limit
arguments, with explicit attention to specialization at arbitrary real
\(z\). A separate reviewer first reconstructed the proof independently,
then checked the manuscript line by line, including the uniform grid, prefix
equivalence, coefficient sizes, bounded-SOCP composition, and the exact
assumptions of Khachiyan--Porkolab. No gap was found.
No numerical experiment or Lean formalization is claimed; neither would
replace the parameter-uniform algebraic argument. An inline `python -`
command checked this note's local links, paired math delimiters, final newline,
trailing whitespace, and control characters; it passed. These are document
checks, not proof verification. No project-wide check or CI inspection was
performed.
