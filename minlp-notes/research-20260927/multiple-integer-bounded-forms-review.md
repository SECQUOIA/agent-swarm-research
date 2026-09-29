# Review of the bounded-form reduction for unbounded conic optimization

Date: 2026-09-28. This is an independent adversarial review of
[the multiple-integer reduction](unbounded-misocp-multiple-integer-frontier.md).
I read its full Sections 1–9 after first reviewing the proposed argument.
No remaining gap was found in its fixed-parameter polynomial degree and
bit-height bound or its exact optimization reduction, conditional on the
separately reviewed compressed-projection, feasibility, and attained-fiber
inputs. The two repairs below are incorporated in the manuscript.
This review makes no novelty claim.

## 1. The qualitative argument

Let \(S\subseteq\mathbb R^k\times\mathbb R^n\) be convex and let
\(f\) be affine. Put

\[
 C_t=\{z:\exists x\ (z,x)\in S,\ f(z,x)<t\},\qquad
 \alpha=\inf_S f,\qquad
 \theta=\inf_{S\cap(\mathbb Z^k\times\mathbb R^n)}f.
\]

Assume that the mixed-integer set is nonempty and \(\theta\) is finite.
For a nonempty set \(C\), write

\[
 A(C)=\{a\in\mathbb R^k:\sup_{z\in C}|a^Tz|<\infty\}.
\]

This is a real linear space. Its definition requires boundedness in both
directions; one-sided boundedness would not define a linear space.

**Level independence.** If \(\alpha<t_1<t_2<\infty\), then
\(A(C_{t_1})=A(C_{t_2})\). Choose an anchor \((z_0,x_0)\in S\)
with \(f(z_0,x_0)<t_1\). A fixed \(\lambda\in(0,1)\) can be chosen
so that

\[
 (1-\lambda)f(z_0,x_0)+\lambda t_2<t_1.
\]

Convexity maps every point of \(C_{t_2}\) into \(C_{t_1}\) by
\(z\mapsto(1-\lambda)z_0+\lambda z\). A bound for a linear form
on the latter set therefore gives a bound on the former. The reverse
inclusion follows from nesting. This works also when \(\alpha=-\infty\).

**No rational bounded form.** Suppose the projected domain is
full-dimensional and \(A(C_t)\cap\mathbb Q^k=\{0\}\). Then
\(\theta=\alpha\). Indeed, every \(C_a\), \(a>\alpha\), is
full-dimensional: mix one point below level \(a\) with finitely many
projected domain points spanning the ambient space, using sufficiently
small positive mixing weights. If \(\alpha<a<\theta\), then \(C_a\)
has no integer point. Since
\(\operatorname{int}\overline{C_a}=\operatorname{int}C_a\), its
closure is lattice-free. It lies in a maximal lattice-free set
\(B=P+L\), where \(P\) is a polytope and \(L\) is a proper rational
linear space. Any nonzero rational vector in \(L^\perp\) defines a
bounded linear form on \(B\), contradicting level independence.

The source is Basu, Conforti, Cornuéjols and Zambelli,
[*Maximal lattice-free convex sets in linear subspaces*](https://arxiv.org/pdf/1701.06543),
Theorem 2(i), PDF page 2, and Corollary 20, PDF page 15. The former gives
the cylinder representation, and the latter gives maximal containment.
Both statements were inspected directly. Averkov's
[*A proof of Lovász's theorem on maximal lattice-free sets*](https://arxiv.org/pdf/1110.1014),
Theorem 1, independently states the rational-lineality conclusion for
full-dimensional maximal lattice-free sets.

**A rational bounded form gives a slice.** Fix \(U>\theta\) for which
the cap contains a mixed-integer feasible point. If a nonzero integer
vector \(a\) belongs to \(A(C_U)\), only finitely many integers
\(b=a^Tz\) occur below level \(U\). Along an integer-feasible sequence
whose objective values approach \(\theta\), one value \(b\) occurs
infinitely often. The slice \(a^Tz=b\) therefore retains the same
infimum. Only one form is needed at each step. A Smith or Hermite lattice
parametrization reduces the number of integer variables by one.

## 2. Necessary repairs

### 2.1 Check the affine dimension after every slice

Full dimension is essential. On the irrational line
\(z_2=\sqrt2 z_1\), the bounded-form space has no nonzero rational
vector, but the only integer point is the origin. A linear objective can
have continuous infimum \(-\infty\) and integer minimum zero.

Consequently, a slice cannot be followed immediately by the no-rational-form
argument. At every stage inspect the affine hull of the capped projected
domain. If it is proper, obtain a nonzero algebraic affine equation
\(a^Tz=b\) containing that domain. Put all coefficients in one number
field and expand in a rational basis. Every integer point satisfies each
resulting rational affine equation, and at least one equation has a nonzero
normal. Restrict the integer lattice by such an equation. This reduces the
integer dimension and preserves all integer points in the cap.

The author confirmed this preprocessing repair. Its coefficient bound must
be supplied by few-variable elimination and algebraic linear algebra, not
by assuming the original projected affine hull is rational.

### 2.2 Do not change which variables define the Hessian span

The existing continuous SOCP optimization theorem cannot be applied directly
after treating the integer variables as continuous. The span of the full
squared Hessians can be arbitrarily larger than the span of their continuous
blocks, even with one integer variable and continuous span zero.

For example, for \(j=1,\ldots,n\), impose the rational cones

\[
 \|(2,z-x_j)\|_2\le z+x_j.
\]

Their squared rows are \(4-4zx_j\). Every \(xx\)-Hessian is zero,
whereas their full Hessians are linearly independent. Thus the two spans
are respectively zero and \(n\).

The repair is to retain \(z\) among the few free or quantified variables
of the compressed projection formula. Eliminate those variables only in
that formula. This applies both when bounding \(a^Tz\) on the cap and
when bounding the finite continuous infimum at a terminal stage with
\(A(C_U)\cap\mathbb Q^k=\{0\}\). At most the fixed integer dimension
is added to the quantified variable count. The author was notified of
both uses of this repair.

## 3. Effective bounds and their limits

The coefficient-sensitive elimination input was checked directly in Basu's
[*Algorithms in Real Algebraic Geometry: A Survey*](https://arxiv.org/abs/1409.1534),
Theorem 2.27, also present in the repository's local text copy. Its bounds
for the degree and coefficient bit length of each output atom do not
depend on the number of input atoms. The size of the output formula does
depend on that number. No polynomial-time construction of the exponentially
large compressed formula or its elimination is justified by this observation.

I also inspected Khachiyan and Porkolab's
[*Integer Optimization on Convex Semialgebraic Sets*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
Propositions 2.1–2.2 and Corollary 2.3, printed pages 211–212. They explicitly
give common-field algebraic samples with degree and individual representation
bit bounds independent of atom count. The bit bound is linear in the input
coefficient bit bound. This validates the manuscript's simpler approach of
sampling several independent basis vectors together, rather than forming a
compositum from separately sampled vectors. Exact field linear algebra then
computes a defining matrix, and expansion in a power basis gives rational
equations for the rational part.

The bounded-form space has a first-order definition

\[
 a\in A(C_U)\quad\Longleftrightarrow\quad
 \exists R>0\ \forall z\bigl[z\in C_U\Rightarrow
                         -R\le a^Tz\le R\bigr].
\]

The affine-normal space has a similar definition using
\(a^Tz=b\). After inserting the compressed formula, only a number of
variables depending on \(k,h\) is quantified. Coefficient-sensitive
elimination therefore gives descriptions of these spaces with individual
degree and coefficient bit length polynomial in the original input for
fixed \(k,h\).

A separate independent subreview supplies an atom-count-independent bound
for the rational part of such a linear space. Normalize a coordinate chart
of the space to make each basis vector a singleton of a rational
semialgebraic formula. That point is an isolated real zero of the atoms
vanishing there. At most \(\binom{k+D}{k}\) original atoms span their
coefficient vectors, preserving degrees and heights. The isolated-real-root
bound in Hansen et al.,
[*Exact Algorithms for Solving Stochastic Games*](https://www.cs.au.dk/~arnsfelt/Papers/exactstochastic.pdf),
Theorem 23, PDF pages 19–20, bounds its algebraic coordinates. I independently
inspected that statement. Intersecting the conjugate complex linear spaces
and applying determinant height bounds then gives a rational basis of the
rational part with polynomial **bit length** at fixed dimension.
Absolute numerator or denominator magnitude is not asserted to be polynomial.
The full alternative proof is in
[the rational-part review](bounded-forms-rational-part-review.md).

For a bounded form with these rational coefficients, eliminate the
compressed definition of \(C_U\) together with \(s=a^Tz\). The
bounded image has finite endpoints, each a root of a nonzero univariate
output atom. Cauchy's bound gives a polynomial bit bound for all possible
integer values \(b\). Integer lattice restriction has polynomial encoding
cost in the equation data. Since the number of such restrictions is at
most the original \(k\), the fixed-parameter polynomial encoding bound
survives the induction.

At a terminal full-dimensional stage the integer and continuous infima
coincide. Eliminate the remaining integer coordinates, now used only as
real variables inside the compressed formula, to describe the achievable
objective values on the real relaxation. A finite endpoint is annihilated
by one nonzero output polynomial. At integer dimension zero the same
argument applies directly. This establishes the proposed finite-value
degree and bit-height mechanism, subject to the stated inputs.

The reduction is an existence argument for a uniform effective encoding
bound. A final algorithm can use that bound, rational-threshold feasibility,
bisection and algebraic recognition without constructing any of the
selected slices.

## 4. Attainment and recovery

The manuscript's Section 6 does not require the separate algebraic-threshold
feasibility algorithm. Once the finite value is known, its minimal polynomial
and isolating interval define that value inside a rational first-order
formula. The optimal integer projection is convex, so the classical integer
witness theorem bounds an optimal integer assignment whenever one exists.
At such an assignment, the continuous fiber and its objective are rational.
The attained-optimizer encoding theorem therefore gives a uniform box for
some optimal continuous point, without treating the value as an input
coefficient of that theorem.

Intersect the original set with both boxes. The intersection is compact,
so its minimum is attained whenever it is nonempty. It has the original
value exactly when the original infimum is attained. Uniform degree and
height bounds over the finitely many integer fibers, followed by the rational
threshold oracle and algebraic recognition, recover this boxed minimum.
The number of fibers is irrelevant to the bound for the selected minimum:
one fiber's annihilator suffices. Integer-coordinate bisection retains a
half-box whose exact minimum is the original value. After fixing the integer
assignment, the continuous optimization theorem applies to the rational
fiber with its original continuous Hessian span.

I checked these implications and found no circular dependence on attainment
or on an unknown optimizer radius. The argument does rely on the separate
attained-fiber encoding theorem, whose proof is outside this review.

## 5. Coefficient-sensitive general epigraph theorem

I subsequently read the added Section 2.2 and checked its general statement.
For a convex upward-closed set \(E\subseteq\mathbb R^k\times\mathbb R\)
defined by arbitrarily many integer polynomial atoms of degree at most
\(d\ge2\) and coefficient bit length at most \(H\), the proof gives a
finite mixed-integer infimum degree at most \(d^{G(k)}\) and minimal
polynomial coefficient bit length at most \((H+1)d^{G(k)}\), for an
effective function \(G\). No remaining gap was found in this refinement.

The following points preserve linear dependence on \(H\):

- Upward closure converts any mixed-integer feasible point into a fully
  integer point by increasing its last coordinate to an integer. The
  classical integer witness theorem therefore gives a bounded integer
  pair and an initial cap of bit length linear in \(H\).
- Common-field sampling bounds are linear in coefficient bit length.
  Determinant dimensions in field arithmetic depend on the field degree
  and integer dimension, not on \(H\). Rationalization and lattice
  parametrization therefore preserve that linear dependence.
- The carried description after a slice is the original polynomial family
  with an integer affine substitution. Its degree stays \(d\), and its
  coefficient bit growth is linear in the substitution's coefficient bit
  bound. The potentially larger-degree elimination output is not carried
  into the next induction stage.
- There are at most \(k\) slices. Root separation for the resulting minimal
  polynomial gives an isolating interval with the same linear-in-\(H\)
  form. The separate integer witness argument then bounds an optimal
  integer vector if attainment holds.

Independence from the number of atoms is an encoding conclusion. Neither
this proof nor the cited sampling algorithms run without reading a large
explicit formula. An efficient application still needs a separate oracle
or a compact representation whose operations avoid that formula.

## 6. Verification scope

The proof review checked level independence, maximal lattice-free
containment, rational recession structure, finite-slice preservation of the
infimum, both dimension issues, and the required coefficient accounting.
The rational-part lemma received a separate subreview. No priority claim
was checked or established.

A targeted inline SymPy calculation expanded the displayed cones and
checked their Hessians for \(n=1,\ldots,5\). All checks passed:
the continuous Hessian span is zero and the full Hessian span is \(n\).
This supports the concrete counterexample only; the general independence
is also immediate from the distinct \((z,x_j)\) matrix entries.
No project-wide checks or CI checks were run.
