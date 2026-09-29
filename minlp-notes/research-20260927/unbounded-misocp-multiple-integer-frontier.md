# Unbounded MISOCP optimization through bounded rational linear forms

Date: 2026-09-28. Status: complete proof;
[independent adversarial review](multiple-integer-bounded-forms-review.md)
found no remaining gap in the fixed-parameter polynomial result or its
coefficient-sensitive generalization. The argument uses the reviewed compressed projection
formula and exact feasibility algorithm from
[unbounded MISOCP feasibility](unbounded-misocp-frontier.md). Novelty has
not been established. The geometric ingredients are classical; the proposed
addition is their use to bound a possibly unattained mixed-integer infimum
of a continuous objective.

The central observation is that the rational linear forms bounded on a
convex objective sublevel do not depend on the sublevel. If none exist,
and the projected domain is full-dimensional, the integer and continuous
infima agree. Otherwise a bounded integer linear combination can be fixed
without changing the integer infimum. Repeating this reduction leaves a
continuous semialgebraic infimum. This avoids describing integer escape
sequences or assuming a rational recession direction.

## 1. Input and proposed result

Let \(F\subseteq\mathbb R^k\times\mathbb R^n\) be the closed convex
set described by rational affine rows and rational second-order cone rows

\[
 \|A_i(z,x)+b_i\|_2\le c_i^T(z,x)+d_i.
\]

Let \(f(z,x)\) be rational affine. Set

\[
 h=\dim_{\mathbb Q}\operatorname{span}
 \{2(A_{ix}^TA_{ix}-c_{ix}c_{ix}^T):i\},\qquad
 \theta=\inf\{f(z,x):(z,x)\in F,\ z\in\mathbb Z^k\}.
 \tag{1}
\]

The original SOC sign conditions are retained when squared residuals are
used. No bounds, Slater condition, attainment assumption, or rational
continuous feasible point are imposed. Write \(N\ge2\) for explicit
binary input size.

**MISOCP theorem.** There is an effective function \(E(k,h)\) such
that every finite \(\theta\) has an integer annihilator of degree and
coefficient bit length at most \(N^{E(k,h)}\). Consequently, for fixed
\(k,h\), there is a polynomial-time Turing algorithm that:

1. classifies the problem as infeasible, unbounded below, or having finite
   infimum;
2. returns a minimal polynomial and isolating interval for every finite
   infimum, including an unattained one;
3. decides attainment and, when attained, returns an optimal integer
   assignment and an exact algebraic continuous optimizer.

The proof below establishes an effective fixed-parameter polynomial
exponent. It does not claim an FPT bound \(g(k,h)N^C\), nor the sharper
linear dependence of that exponent on \(h\) obtained in some continuous
results. Improving the parameter dependence is a separate question.

## 2. Algebraic bounds used in the proof

The compressed projection theorem gives a formula for

\[
 E=\{(z,t):\exists x\ ((z,x)\in F, f(z,x)\le t)\}
 \tag{2}
\]

with quantifier blocks of sizes \(1,1,h+1\). Its atomic degrees and
coefficient bit lengths are \(N^{O(1)}\). Adding the affine threshold row
does not increase \(h\). The Boolean matrix can contain exponentially
many atoms. It is used to prove bounds, not constructed by the algorithm.

The same statement permits arbitrary additional rational affine rows in
\((z,x)\). Rational affine changes of only the integer coordinates
preserve the original continuous Hessians and hence \(h\).

We use the following standard consequences of quantitative real
quantifier elimination and algebraic sampling. These are the
degree/height statements in Khachiyan--Porkolab (2000), Proposition 2.1,
Proposition 2.2, and Corollary 2.3, based on the cited work of Basu and
coauthors. Their degree and individual coefficient bounds are independent
of the number of atoms. Their running times are not independent of it.

**Bound convention.** A first-order formula obtained from a fixed number
(depending on \(k,h\)) of copies of (2), with at most a number of new
real variables depending on \(k,h\), has the following bounds:

* every finite endpoint of its one-dimensional solution set has an
  annihilator of degree and coefficient bit length \(N^{O_{k,h}(1)}\);
* every nonempty solution set has an algebraic sample in one number field
  with degree and coordinate representation length
  \(N^{O_{k,h}(1)}\).

For the first statement, eliminate all variables except the endpoint
coordinate. At an endpoint at least one nonzero resulting polynomial
vanishes: otherwise all polynomial signs are constant nearby and the
Boolean formula cannot change truth value. For the second, choose a
nonempty sign condition in the quantifier-free formula and apply the
sample-point bound. These arguments do not sum coefficient lengths over
the potentially very large atom collection.

Strict sublevels can be described without changing the original quadratic
system: \(f<t\) is equivalent to
\(\exists s<t\ ((z,s)\in E)\). Thus an extra real variable suffices.
Negating a formula or putting it under a new universal quantifier changes
the quantifier blocks by a quantity depending only on \(k,h\).

### 2.1 A rational part of a semialgebraic linear space

Suppose a real linear space \(V\subseteq\mathbb R^k\) has such a
formula. There is a rational basis of

\[
 V_{\mathbb Q}:=\operatorname{span}_{\mathbb R}(V\cap\mathbb Q^k)
 \tag{3}
\]

whose coefficients have \(N^{O_{k,h}(1)}\) bits.

To prove this, let \(r=\dim V\). The formula asserting that
\(v_1,\ldots,v_r\in V\) and
\(\det((v_i^Tv_j)_{ij})>0\) has a sample in a common number field
\(K\) of controlled degree and height. These vectors form a real basis
of \(V\). Linear algebra over \(K\) gives a matrix \(M\) with
\(V=\ker_{\mathbb R}M\). Expand the entries of \(M\) in the power
basis of a primitive element of \(K\). For rational \(a\), the
equation \(Ma=0\) is equivalent to the resulting collection of rational
linear equations. Its rational kernel is exactly \(V\cap\mathbb Q^k\).
Rational Gaussian elimination and determinant bounds give a rational
basis of polynomial bit length in the already bounded representations.
The case \(r=0\) is immediate. This is an existence and height argument;
the expensive sample computation is not a step of the final algorithm.

### 2.2 General convex semialgebraic value theorem

The argument applies more generally to a nonempty convex set
\(E\subseteq\mathbb R^k\times\mathbb R\) that is upward closed in
its last coordinate: \((z,t)\in E\) and \(s\ge t\) imply
\((z,s)\in E\). Neither closedness nor attainment is required.
Suppose \(E\) has a quantifier-free Boolean description by integer
polynomial atoms of degree at most \(d\ge2\), whose individual
coefficient bit lengths are at most \(H\ge1\). The number \(m\)
of atoms is arbitrary. Assume \(E\cap(\mathbb Z^k\times\mathbb R)\)
is nonempty and put

\[
          \theta_E=\inf\{t:(z,t)\in E,\ z\in\mathbb Z^k\}.
 \tag{3a}
\]

**General value theorem.** For some effective function \(G(k)\), every
finite \(\theta_E\) has an integer minimal polynomial of degree at
most \(d^{G(k)}\) and coefficient bit length at most

\[
                         (H+1)d^{G(k)}.
 \tag{3b}
\]

These bounds are independent of \(m\). If the infimum is attained,
some optimal integer vector has bit length at most
\((H+1)d^{G(k)}\), after increasing \(G\) if necessary.

Here is the coefficient-sensitive accounting for the geometric proof in
Sections 3--4. For general \(E\), define
\(C_U=\{z:\exists t<U\ ((z,t)\in E)\}\).

1. An initial rational cap \(U\) with at most
   \((H+1)d^{O((k+1)^4)}\) bits is available without knowing the
   value. Upward closure implies \(E\cap\mathbb Z^{k+1}\ne\varnothing\).
   Apply Khachiyan--Porkolab's integer witness theorem directly in
   dimension \(k+1\), obtaining an integer pair \((z_0,t_0)\in E\)
   of that size, and use \(U=t_0+1\).
2. Every formula used for a bounded-form space, a joint basis, or an
   affine equation uses at most a number of variables depending only on
   \(k\). Its atom degree is bounded by \(\max\{d,O(k)\}\).
   Quantifier elimination and a common-field sample therefore have
   degree \(d^{O_k(1)}\) and bit length
   \((H+1)d^{O_k(1)}\). The sampling algorithm's running time may
   depend on \(m\); the degree and height conclusions do not.
3. Linear algebra on at most \(k\) sampled vectors in one field has
   determinant sizes bounded in terms of \(k\) and the field degree.
   Each addition, multiplication, norm, and determinant increases bit
   lengths by at most a factor polynomial in the field degree and
   depending only on \(k\), plus a term independent of \(H\).
   Rationalizing the equations and clearing
   denominators therefore retain the form
   \((H+1)d^{O_k(1)}\). In particular this step does not raise
   \(H\) to a power depending on \(k\).
4. The finite range of a selected bounded rational form is obtained by
   eliminating at most \(k+1\) additional variables. Its endpoint
   height, the bit length of the chosen integer right-hand side, and
   the size of an affine integer lattice parametrization all have the
   same linear-in-\(H\) form. Standard determinant and Hermite-normal-form
   bounds suffice for the parametrization; the rank is at most \(k\).
5. Substitution \(z=z_0+Ty\) into an original polynomial preserves
   its degree \(d\). If the integer entries of \(z_0,T\) have
   at most \(L\) bits, the coefficient bit length grows by at most
   \(O(dkL+k\log(d+1))\), in addition to the original height.
   The extra term bounds the number of contributing monomials. It is
   linear in \(L\), hence linear in \(H+1\). Keep the transformed
   original atoms at each stage; do not use the intermediate
   quantifier-elimination output as a new geometric input.

At most \(k\) restrictions occur. The degree of the carried atoms
remains \(d\), while their coefficient bits remain
\((H+1)d^{O_k(1)}\). In the terminal case, eliminate at most \(k\)
coordinates to obtain the finite continuous endpoint. This proves
(3b), using exactly the geometric argument below. Minimal-polynomial
factor height bounds preserve the stated form.

For an attained value, append a real variable selecting \(\theta_E\)
by its minimal polynomial and a rational isolating interval, and
project \(E\) at that value onto its integer coordinates. Root
separation provides an isolating interval of bit length
\((H+1)d^{O_k(1)}\). The projected set is convex. Applying the
quantified version of the integer witness theorem gives the stated
optimal-vector bound. This argument is separate from the descent and
does not presume attainment when proving (3b).

Composing this general theorem with a bounded-block quantified
description gives corresponding bounds with the block-size dependence
from quantitative real quantifier elimination. This is the form used
for the compressed SOCP epigraph. It is also potentially useful when a
different representation controls degree independently of the total
input dimension. It supplies bounds, not an algorithm that constructs
an exponentially large description.

## 3. Convex sublevels and bounded linear forms

For \(t\in\mathbb R\), put

\[
 C_t=\{z:\exists x\ ((z,x)\in F,\ f(z,x)<t)\},\qquad
 \alpha=\inf_{(z,x)\in F}f(z,x).
 \tag{4}
\]

These sets are convex and nested. They need not be closed. Fix a rational
\(U>\theta\) for which \(C_U\cap\mathbb Z^k\ne\varnothing\).
Such a \(U\) with \(N^{O_{k,h}(1)}\) bits exists uniformly: the
unbounded integer witness bound and the continuous algebraic feasible
witness bound provide some feasible mixed-integer point with all
coordinate magnitudes at most \(2^{N^{O_{k,h}(1)}}\); a larger rational
upper bound on its affine objective works. This argument uses only
feasibility, not an unknown optimum.

Define

\[
 \mathcal B_t=\{a\in\mathbb R^k:
                  \sup_{z\in C_t}|a^Tz|<\infty\}.
 \tag{5}
\]

**Lemma 1.** For every \(t>\alpha\), \(\mathcal B_t\) is the same
real linear space \(\mathcal B\).

**Proof.** Closure under linear combinations follows from the triangle
inequality. Let \(\alpha<s<t\), and take a feasible point
\((z_0,x_0)\) with objective \(L<s\). Choose a fixed
\(0<\lambda<1\) with \((1-\lambda)L+\lambda t<s\).
For each \(z\in C_t\), choose a corresponding feasible \(x\).
Convexity gives
\((1-\lambda)z_0+\lambda z\in C_s\). Therefore a bound on
\(|a^Tz|\) over \(C_s\) gives a bound over \(C_t\), by dividing
by the same positive \(\lambda\). The reverse inclusion follows from
\(C_s\subseteq C_t\). This also works when \(\alpha=-\infty\).
\(\square\)

A formula for \(\mathcal B=\mathcal B_U\) is

\[
 \exists R>0\ \forall z\in\mathbb R^k:
       \bigl(z\in C_U\ \Longrightarrow\ -R\le a^Tz\le R\bigr).
 \tag{6}
\]

Hence Section 2.1 supplies a polynomial-bit rational basis of
\(\mathcal B_{\mathbb Q}\).

**Lemma 2.** Suppose \(C_U\) is full-dimensional. If
\(\mathcal B\cap\mathbb Q^k=\{0\}\), then
\(\theta=\alpha\), with extended-real equality allowed.

**Proof.** Certainly \(\alpha\le\theta\). If strict inequality held,
choose \(\alpha<t<\theta\). The set \(C_t\) is nonempty and
full-dimensional. To see the second property, mix a point of objective
less than \(t\) with a sufficiently small fixed positive fraction of
an open ball in \(C_U\); the objectives of witnesses for that ball
are less than \(U\), so the same fraction works for every point of
the ball.

No point of \(C_t\) is integral. For a full-dimensional convex set,
\(\operatorname{int}\overline{C_t}=\operatorname{int}C_t\subseteq C_t\).
Thus \(\overline{C_t}\) is lattice-free, in the standard sense that its
interior has no integer point. The containment theorem of
Basu--Conforti--Cornuejols--Zambelli places it in a maximal lattice-free
convex set, which is full-dimensional because it contains \(C_t\).
Their complete formulation of Lovasz's theorem states that such a set has the form
\(P+L\), where \(P\) is a polytope and \(L\) is a proper rational
linear space. A nonzero rational vector in \(L^\perp\) is bounded in
absolute value on \(P+L\), hence on \(C_t\). Lemma 1 places it in
\(\mathcal B\), a contradiction. \(\square\)

The full-dimensional hypothesis is essential. An irrational line can
have no nonzero bounded rational linear form and contain only one integer
point. Section 4 handles this case before applying Lemma 2.

## 4. Dimension reduction and the finite-infimum bound

We prove the bound by induction on the current integer dimension. At
every stage the problem remains a rational SOC problem, the continuous
Hessian span is at most the original \(h\), the infimum remains the
same finite \(\theta<U\), and the current input length is
\(N^{O_{k,h}(1)}\). The rational cap \(U\) is retained throughout.
It is used to study sublevels, not to delete improving feasible points.

### 4.1 A projected sublevel with smaller affine dimension

If \(C_U\) is not full-dimensional in the current integer space,
there is a nonzero affine equation

\[
                     a^Tz=b\qquad(z\in C_U).
 \tag{7}
\]

The formula asserting \(a\ne0\) and (7) is another formula of the
type in Section 2. Sample \((a,b)\) in a common number field of
controlled degree and height. Expand all coefficients in its power
basis. For integral \(z\), (7) implies each resulting rational affine
equation. At least one has a nonzero normal. Clear denominators and
choose one such equation, written \(p^Tz=q\) with integer data of
\(N^{O_{k,h}(1)}\) bits.

Every mixed-integer point of objective less than \(U\) satisfies this
equation. Its integer solutions form a nonempty affine lattice, since
\(\theta<U\). Hermite or Smith normal form gives
\(z=z_0+Ty\), \(y\in\mathbb Z^{k-1}\), with polynomial-bit
integer \(z_0,T\); reducing further is also possible. Restrict to this
lattice. All sufficiently good points are retained, so the infimum
remains \(\theta\). Only integer coordinates were changed, so the
continuous Hessians are unchanged. Apply induction.

### 4.2 A full-dimensional sublevel with a bounded rational form

Suppose \(C_U\) is full-dimensional and
\(\mathcal B\cap\mathbb Q^k\ne\{0\}\). Section 2.1 gives a
nonzero integer \(a\in\mathcal B\) with polynomially bounded bit
length. The finite infimum and supremum of \(a^Tz\) on \(C_U\) have
annihilators of bounded degree and height: use the compressed formula
for \(C_U\), add a free value variable \(v=a^Tz\), and eliminate
the \(k\) coordinates \(z\). Section 2 then applies. A root bound
gives an integer \(B=2^{N^{O_{k,h}(1)}}\) with

\[
                     |a^Tz|<B\qquad(z\in C_U).
 \tag{8}
\]

It would be incorrect here to declare the original integer coordinates
continuous and apply a theorem parameterized by the full squared-Hessian
span. Cross terms can make that full span much larger than \(h\).
The compressed projection formula is what preserves the stated bound.

Choose a mixed-integer sequence with objective tending to \(\theta\)
and eventually less than \(U\). There are only finitely many possible
integer values of \(a^Tz\) in (8). One value \(b\) occurs along
a subsequence whose objective still tends to \(\theta\). Equivalently,
the minimum of the finitely many slice infima equals \(\theta\).
Thus the rational affine slice

\[
                            a^Tz=b
 \tag{9}
\]

has the same infimum, and \(b\) has polynomially many bits. Parametrize
its integer solutions as in Section 4.1 and apply induction.

This is an existence argument for a small slice. Enumerating its possible
right-hand sides is not part of the algorithm.

### 4.3 Terminal cases

If the integer dimension is zero, the value is a continuous
semialgebraic infimum. If \(C_U\) is full-dimensional and has no
nonzero bounded rational form, Lemma 2 identifies \(\theta\) with
the continuous infimum. In either case, eliminate the current integer
coordinates from the compressed epigraph formula (2). The finite
infimum is an endpoint of a one-dimensional semialgebraic set and has
the degree/height bound of Section 2.

There are at most the original \(k\) restrictions. At each restriction,
coefficient sizes, affine lattice bases, sample-point bounds, and endpoint
bounds grow by a polynomial whose exponent depends only on \(k,h\).
Composing at most \(k\) such bounds gives an effective exponent
\(E(k,h)\). This proves the proposed finite-infimum bound.

In particular, a finite infimum cannot be transcendental in this class.
This conclusion does not require finding, or giving an algebraic
parametrization of, an integer sequence approaching the value.

### 4.4 A qualitative consequence without semialgebraicity

The same geometric descent gives the following supporting statement.
For any convex upward set \(E\subseteq\mathbb R^k\times\mathbb R\)
with nonempty mixed-integer domain and finite mixed-integer infimum
\(\theta_E\), there is a rational affine space \(W\subseteq\mathbb R^k\)
containing an integer point such that

\[
                 \theta_E=\inf\{t:(z,t)\in E,\ z\in W\}.
 \tag{S}
\]

No encoding or computability conclusion follows for arbitrary convex
sets. To obtain the qualitative proof, choose any cap above a feasible
mixed-integer value. When a capped projection has smaller affine
dimension, replace it by the affine hull of its integer points; this
is a rational affine space of strictly smaller dimension and retains
all improving integer points. When it is full-dimensional, apply the
bounded-form dichotomy. A nonzero rational bounded form permits a
fixed integer slice along a minimizing subsequence; if none exists,
Lemma 2 identifies the current integer and continuous infima. Each
restriction decreases dimension, and compositions of rational affine
lattice restrictions remain rational. This proves (S).

Thus semialgebraicity is needed above to control the sizes of the
chosen slices and the final continuous value, not for the qualitative
existence of a slice. The statement does not assert equality with the
original continuous relaxation. No separate novelty claim is made.

## 5. Exact classification and value recovery

Use the existing exact unbounded MISOCP feasibility algorithm first.
For a nonempty instance, the bound just proved gives an explicit
\(M=2^{N^{O_{k,h}(1)}}\) such that every finite value satisfies
\(|\theta|<M\). Feasibility of the original problem with the
rational affine row \(f\le-M-1\) is therefore equivalent to
unboundedness below. This does not compare the integer problem with its
continuous relaxation.

In the finite case, rational threshold feasibility and bisection give
certified approximations to \(\theta\). The annihilator bounds and
the reviewed [algebraic recognition input](algebraic-recognition-source-review.md)
recover its minimal polynomial and a rational isolating interval in
polynomial time for fixed \(k,h\). If a midpoint equals an unattained
infimum, threshold feasibility is false; the enclosing interval remains
valid. Each query has the same \(k,h\), and only polynomially many
coefficient bits are introduced.

## 6. Attainment and an optimal point

Assume the exact finite \(\theta\) has been recovered. Its optimal
integer projection is

\[
 Y_* = \{z:\exists x\ ((z,x)\in F,\ f(z,x)\le\theta)\}.
 \tag{10}
\]

This real projection is convex. Use the compressed formula (2), with
one additional real variable \(t\), together with the minimal
polynomial and an isolating interval specifying \(t=\theta\).
The resulting formula defines exactly (10); it has a bounded number
of quantified variables depending on \(k,h\), and polynomial degree
and coefficient bounds. Khachiyan--Porkolab's integer witness theorem
therefore gives a universal
\(R_z=2^{N^{O_{k,h}(1)}}\) such that attainment, if it holds, occurs
at some \(z\in[-R_z,R_z]^k\cap\mathbb Z^k\).

For every such optimal assignment, its continuous fiber has rational
input of polynomial length and attains its rational affine objective.
The reviewed [attained-optimizer bound](nonconvex-attainment-and-optimizer.md)
therefore supplies some optimal continuous point in a uniform box
\([-R_x,R_x]^n\), with \(\log R_x=N^{O_{k,h}(1)}\).
This argument does not insert \(\theta\) as a coefficient of a
quadratic system: the fiber objective and constraints remain rational.

Intersect the original problem with both boxes. This compact
mixed-integer problem is either empty or has an attained minimum
\(\beta\). It has exact polynomial-time value recovery for fixed
\(k,h\): there are finitely many integer fibers, their value degree
and height bounds are uniform, and rational threshold feasibility gives
bisection and recognition. Hence the original infimum is attained if
and only if the boxed problem is nonempty and \(\beta=\theta\).

When equality holds, bisect each integer coordinate interval. For each
half, compute the exact boxed minimum and retain a half with value
\(\theta\). Compactness guarantees that a retained half contains an
optimizer. Polynomially many queries fix an optimal integer assignment.
The [continuous exact optimization algorithm](continuous-socp-optimization.md)
then returns an exact continuous optimizer in that rational fiber. Its
continuous Hessian span remains \(h\).

## 7. Examples and limits

The elementary problem

\[
 \inf\{(z_1-\tfrac12)^2+1/z_2:
                       z_1\in\mathbb Z,\ z_2\in\mathbb Z_{\ge1}\}
                         =\tfrac14
 \tag{11}
\]

has no optimizer and has continuous infimum zero. Its epigraph has a
rational SOC representation, using a square epigraph and a rotated cone
for the reciprocal. The form \(z_1\) is bounded on every finite
sublevel; fixing \(z_1=0\) or \(1\) reduces to a one-integer tail
whose continuous and integer infima agree. Thus the result cannot be
replaced by unconditional equality with the continuous infimum.

Conversely, bounding only the rational span of a recession cone is
insufficient. The lattice-free convex set

\[
       \{(z_1,z_2,z_3):0<z_1<1,\ z_3\ge z_2^2\}
\]

has recession cone generated by the positive \(z_3\) direction,
but its quotient by that direction is unbounded in \(z_2\). Bounded
linear forms capture the missing transverse bounded coordinate directly.

The theorem would supply exact termination and attainment decisions for
structured conic models without artificial variable bounds. It does not
provide a practical implementation, a small number of branch-and-bound
nodes, rational recession certificates, or simple integer escape curves.
The existing [irrational strip examples](socp-unboundedness-boundaries.md)
still exclude polynomial escape curves with rational coefficients.

A rational SOC example also demonstrates why the affine-dimension step
must be repeated. Let \(z_1,z_2\) be integral and \(t\) continuous,
and impose

\[
 \|(z_1,z_1)\|\le z_2,\qquad
 \|(z_2,z_2)\|\le2z_1,\qquad
 \|(2,z_1+1-t)\|\le z_1+1+t.
 \tag{12}
\]

The first two rows give \(z_2=\sqrt2z_1\) and \(z_1\ge0\);
the third gives \(t(z_1+1)\ge1\). The continuous infimum of \(t\)
is zero, whereas the only integer pair is \((0,0)\), with minimum
\(t=1\). On each sublevel above one the integer-coordinate projection
is an irrational ray. Its bounded-form space is the perpendicular
irrational line, whose rational part is zero. Applying Lemma 2 there
without Section 4.1 would be false. The continuous squared Hessians
in the sole continuous coordinate \(t\) are all zero, so this example
already has \(h=0\).

## 8. Prior results and novelty qualification

1. **Khachiyan--Porkolab (2000), *Integer Optimization on Convex
   Semialgebraic Sets*.** The local full text was inspected, particularly
   Proposition 2.1, Corollary 2.3, Theorems 3.1 and 3.4, and Corollary
   3.5. Their main optimized coordinate is integral. Their proofs already
   use algebraic sampling, rationalization of algebraic linear equations,
   rational lattice restrictions, recession spaces, and Kronecker
   approximation. Those methods and the small integer witness theorem
   are prior results. More precisely, Theorem 3.1(ii) already puts a
   full-dimensional lattice-free convex semialgebraic set in an
   integer-normal slab, with degree and height bounds. Its proof and
   the proof of Theorem 3.4 directly anticipate the lattice and
   lower-dimensional steps used here. The bounded-form space above permits choosing
   controlled slices from one rational cap, independently of the unknown
   continuous objective value. The proposed distinction is the bound for
   a finite, possibly unattained, mixed-integer value of a continuous
   objective. See the [primary paper](https://link.springer.com/content/pdf/10.1007/PL00009496.pdf).
2. **Lovasz's maximal lattice-free theorem.** The exact structural input
   is Theorem 2(i) in
   [Basu--Conforti--Cornuejols--Zambelli (2010), *Maximal lattice-free
   convex sets in linear subspaces*](https://personal.lse.ac.uk/zambelli/papers/lattice-free.pdf):
   a full-dimensional maximal lattice-free set in a rational ambient
   space is a polytope plus a rational linear space. The statement is
   used qualitatively, without a claimed coefficient bound for its
   facets. Its containment corollary gives a maximal lattice-free set
   containing every lattice-free convex set. Bounds in this note instead
   come from formula (6).
3. **Lubin--Vielma--Zadik, *Mixed-integer convex representability*.**
   [The primary preprint](https://arxiv.org/pdf/1706.05135),
   Sections 1.3 and 2.3, explicitly distinguishes rational coefficients
   from its stronger rationality condition on convex representations.
   Equations (1.4)--(1.5) encode an irrational strip using rational SOC
   data. Its structural periodicity and compact-representation results
   cannot be invoked merely because this note has rational SOC input.
4. **The current repository's feasibility and continuous optimization
   results.** These supply the compressed projection and the rational
   threshold oracle. The present reduction is the additional step needed
   for unbounded integer coordinates and a continuous objective; neither
   feasibility nor bounded-integer optimization alone gives the claimed
   finite-value height bound.

Additional searches included “mixed-integer semialgebraic infimum”,
“mixed integer algebraic optimal value convex”, and “bounded linear
forms convex integer optimization”. No equivalent theorem was identified
in the sources examined. This is not evidence of priority. In particular,
the general convex semialgebraic bounded-form reduction should be compared
with the full literature on mixed-integer convex duality and fixed-dimension
optimization before any novelty claim.

## 9. Verification status

An [independent reviewer](multiple-integer-bounded-forms-review.md)
checked the qualitative reduction, rational subspace bounds, induction,
nonclosed projections, use of old results, attainment, and the general
linear-in-coefficient-height theorem. No remaining gap was found,
conditional on the separate theorem inputs. An additional
[rational-part review](bounded-forms-rational-part-review.md) checked
the rational-subspace height step by a different argument.
The root agent independently checked level independence and identified
the lower-dimensional preprocessing and the need to use compressed
projection bounds when optimizing forms in the original integer
coordinates. Those points are included above.

The targeted command
`python research-20260927/check_multiple_integer_bounded_forms.py`
checks exact SOC residual identities, the irrational-ray continuous
Hessian span, and rational-part examples over a quadratic number field.
These examples check important failure boundaries; they do not prove
the general theorem. Local-link, newline, and whitespace checks were
also run on this manuscript. No project-wide tests or CI checks were run.
The final complexity
conclusion remains conditional on the separately reviewed compressed
projection and exact feasibility theorems.
