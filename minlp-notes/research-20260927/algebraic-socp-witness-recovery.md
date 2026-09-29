# Exact witnesses for cone systems over one real number field

Date: 2026-09-28. Status: proof and separate adversarial reviews completed;
no unresolved gap was found in the stated bounds. This extends the
[common-field feasibility theorem](algebraic-threshold-misocp.md).
It does not claim a new algebraic recognition method or number-field
elimination theorem.

Exact feasibility over an explicitly represented real number field can
return an original feasible point, even when that point lies in a proper
extension of the input field. The field degree is part of the input. The
algorithm keeps the original field fixed throughout its feasibility queries
and constructs one absolute field representation only at the end.

## 1. Input, output, and statement

Let

\[
 K=\mathbb Q(\alpha),\qquad p(\alpha)=0,\qquad a<\alpha<b,
\]

where \(p\in\mathbb Z[T]\) is primitive and irreducible of degree
\(D\), and rational nonroot endpoints isolate the selected real root.
Every input coefficient is explicitly represented as a rational polynomial
in \(\alpha\) of degree below \(D\). Write \(N\ge2\) for the
total explicit binary input length, including the dense field polynomial,
isolator, and all coefficient vectors. In particular \(D\le N\);
the degree need not be fixed.

Consider the closed convex set

\[
 C=\{x\in\mathbb R^n:Lx\le a_0,
       \ Ex=e,\quad \|A_ix+b_i\|_2\le c_i^Tx+d_i
                                      \ (1\le i\le m)\},     \tag{1}
\]

with all data in the selected real embedding of \(K\). A supplied
rational box, if present, is included among its affine rows. Put

\[
 h=\dim_K\operatorname{span}_K
             \{2(A_i^TA_i-c_ic_i^T):1\le i\le m\}.            \tag{2}
\]

The squared quadratic description always retains
\(c_i^Tx+d_i\ge0\). The matrices in (2) may be indefinite.
Their span over \(K\) equals their real matrix span at the selected
embedding, by the minor criterion for rank. It need not equal their span
over \(\mathbb Q\).

**Witness theorem.** For every fixed \(h\), a deterministic algorithm
running in \(N^{C_h}\) bit operations either reports infeasibility or
returns the unique minimum-Euclidean-norm point \(x_*\in C\). Its
output consists of a primitive integer irreducible polynomial \(P\), a
rational interval isolating a real root \(\beta\), and rational
polynomials \(b_0,b_1,\ldots,b_n\), reduced modulo \(P\), such that

\[
 \alpha=b_0(\beta),\qquad x_{*j}=b_j(\beta),\qquad
 \mathbb Q(\beta)=K(x_{*1},\ldots,x_{*n}).                    \tag{3}
\]

Here \(C_h\) is effective and may depend on \(h\), but not on
\(D\). There is no fixed-parameter runtime claim with an absolute
input exponent. The point has absolute common-field degree and total
encoding length \(N^{O(h+1)}\); the algorithmic runtime statement is
deliberately more conservative because printed radius and precision bits
enter later feasibility calls.

No bounds, Slater condition, full-dimensionality, rational point, or
\(K\)-rational point are assumed. In dimension zero, exact field sign
tests decide the scalar conditions and the output may retain the input
field with no point coordinates.

## 2. One canonical point has one controlled extension field

If \(C\ne\varnothing\), it is closed and convex. The squared norm
is coercive, so it has a minimizer; strict convexity gives uniqueness.
Denote that point by \(x_*\).

The scalar elimination and height bounds over \(K\) are already proved
in Section 2 of the common-field feasibility note. A separate joint-field
argument is needed: multiplying the degrees of all \(n\) coordinate
polynomials could be exponential in the ambient dimension. The following
construction supplies the required common point and common degree bound.

Choose a basis \(B_1,\ldots,B_h\) of (2) over \(K\), and lift the
quadratic description to

\[
 w=(x,y)\in\mathcal P,\qquad
 F_j(w)=\tfrac12x^TB_jx-y_j=0\quad(1\le j\le h),              \tag{4}
\]

where \(\mathcal P\) is a polyhedron over \(K\) containing all
affine rows and cone signs. Its coefficients have polynomial explicit
encoding length. Let \(w_*\) be the unique lift of \(x_*\).

Choose an integer \(R\) strictly larger than every coordinate magnitude
of \(w_*\). This box is existential and is not inserted into the
coefficient bound. On \(\mathcal P\cap[-R,R]^{n+h}\), minimize

\[
 \|x\|^2+\varepsilon P_0(w),\qquad
        |F_j(w)+\varepsilon^2P_j(w)|\le\varepsilon,           \tag{5}
\]

where \(P_0,\ldots,P_h\) are generic rational quadratics of the
small coefficient size given by the existing nonconvex perturbation lemma.
The same integer-grid argument works for charts over \(K\): a nonzero
polynomial at the selected embedding cannot vanish on the entire grid.
Its degree bound is independent of coefficient magnitudes and rationality.

For sufficiently small positive \(\varepsilon\), \(w_*\) is
feasible for (5), so the compact problem has a minimizer. Every cluster
point of minimizing points is feasible for (4), and uniform convergence
of the objective on the fixed box gives squared norm at most
\(\|x_*\|^2\). Uniqueness therefore forces that cluster point to
be \(w_*\). In particular, all artificial box rows are inactive at
all minimizing points once \(\varepsilon\) is sufficiently small:
otherwise a boundary sequence would converge to an interior point while
remaining on the closed boundary.

Select one subsequence with a fixed active affine chart from the original
\(\mathcal P\) and a fixed oriented band support. Genericity gives
at most \(s\le h\) active nonlinear bands, independent gradients,
and nonsingular multiplier and bordered KKT matrices. The stationarity
elimination from the nonconvex proof gives a system in only \(s\)
multiplier variables and rational-function outputs for every original
coordinate. All outputs use this **same** selected sequence and point.
The unknown \(R\) no longer occurs in the system's coefficients.

The [finite-quotient height lemma over \(K\)](algebraic-coefficient-span-precision.md#3-the-finite-quotient-lemma-over-k)
then gives, for every fixed \(K\)-linear form \(\ell\) in the
coordinates, a nonzero polynomial over \(K\) annihilating
\(\ell(x_*)\), of degree at most

\[
                    L=(a_1+1)^s=N^{O(h+1)},                   \tag{6}
\]

where the reduced multiplier degree \(a_1=N^{O(1)}\). The degree
bound does not depend on the coefficients of \(\ell\). Applying
the primitive-element theorem to the finite extension generated by all
coordinates proves

\[
 [K(x_*):K]\le L,\qquad
 [\mathbb Q(\alpha,x_*):\mathbb Q]\le DL=N^{O(h+1)}.          \tag{7}
\]

This is a relative primitive-element argument on one fixed limit, not a
product of coordinate degree bounds. If the selected chart has dimension
zero, its point lies in \(K\) and (7) holds directly.

For individual coordinate outputs, the local coefficient-norm budget in
the common-field feasibility proof is \(N^{O(1)}\). Its finite-quotient
bound gives projective coefficient height \(N^{O(h+1)}\) over \(K\).
The product formula and Cauchy root bound imply the same form of absolute
logarithmic Weil-height bound for every coordinate. Its primitive integer
minimal polynomial has degree at most \(DL\) and coefficient bit length

\[
                            H=N^{O(h+1)}.                     \tag{8}
\]

These arithmetic bounds include the varying field degree in the explicit
input. They use determinant bounds and local heights, not a normal closure.
Other embeddings need not preserve convexity or the optimization problem;
they are used only to bound coefficients. The input generator \(\alpha\)
already has the corresponding degree and height bounds. The bounded
primitive-element and trace-pairing argument in
[the field review, Section 6](algebraic-socp-witness-field-review.md#6-one-short-absolute-representation-including-the-input-generator)
applied to (7)--(8) gives total length \(N^{O(h+1)}\) for (3).

## 3. An explicit box containing the canonical point

The coordinate annihilator bound (8) and Cauchy's root bound give a
computable rational integer \(B\ge1\) with

\[
 \operatorname{bit}B\le N^{O(h+1)},\qquad
                         x_*\in[-B,B]^n.                     \tag{9}
\]

The algorithm needs only the effective uniform height bound, not the
unknown coordinate polynomials, to print this box. First decide
feasibility by the established common-field algorithm. If feasible,
intersect (1) with (9). The result is compact and has the same unique
minimum-norm point. Thus there is no inference that a box meeting a
feasible set necessarily contains its minimum-norm point.

## 4. Approximation uses only the original field

Let \(\nu=\|x_*\|^2\). For a rational scalar \(t\ge0\), use

\[
 \|x\|^2\le t
 \quad\Longleftrightarrow\quad
                  \|(2x,t-1)\|_2\le t+1.                    \tag{10}
\]

The squared residual is \(4\|x\|^2-4t\), with Hessian \(8I\).
Each query therefore has span at most \(h+1\) over \(K\).
All new coefficients are rational. No field extension is introduced by
\(t\), and no square root of it is required.

For a requested accuracy \(p\ge1\), put \(\tau=2^{-p}\) and
restart from the original compact box. Bisect \([0,nB^2]\) for
\(\nu\), using exact common-field feasibility with (10), until a
feasible upper threshold \(u\) obeys
\(\nu\le u\le\nu+\tau^2/16\). The set

\[
              C_u=C\cap[-B,B]^n\cap\{\|x\|^2\le u\}
\]

is nonempty. For any \(y\in C\), the projection inequality at
\(x_*\) gives

\[
 \langle x_*,y-x_*\rangle\ge0,\qquad
 \|y-x_*\|^2\le\|y\|^2-\nu.
\]

Hence every point of \(C_u\) is within \(\tau/4\) of \(x_*\).
Bisect its coordinate intervals, retaining a lower closed half if the
exact feasibility oracle says yes and the upper closed half otherwise.
The two halves cover the previous interval, so nonemptiness persists.
Store only the current two endpoints in each coordinate. Stop when each
width is at most \(\tau\). The rational box midpoint then has
coordinate error at most \(3\tau/4<2^{-p}\) from \(x_*\).

A box retained for one accuracy request may exclude \(x_*\) itself.
Restarting from the original box for each request ensures approximation
to the same specified tuple. The number of queries and their encoding
lengths are polynomial in \(N\), \(\operatorname{bit}B\), and
\(p\). Every query retains the same input field \(K\), of degree
\(D\), and has only the extra Hessian in (10).

Independently refine the input isolator for \(\alpha\) to precision
\(2^{-p}\). Univariate root isolation and bisection have polynomial
bit cost in its dense degree, coefficient length, and requested precision.
Together these procedures give a certified approximation oracle for
the fixed tuple \((\alpha,x_*)\).

## 5. Absolute common-field reconstruction and verification

Apply [the constructive common-field recovery theorem](constructive-common-field-recovery.md)
to \((\alpha,x_*)\), using the absolute degree bound (7), coordinate
height bound (8), and the preceding approximation oracle. Its recognition
step is Kannan--Lenstra--Lovász; its primitive-element search and coordinate
interpolation have polynomial overhead in tuple length, degree, and height.
It therefore produces (3) without factorization over an unknown field.

Retaining \(\alpha\) as a coordinate is essential to this interface:
it embeds the input coefficient field in the output field and keeps the
selected real embedding. Recovering unrelated coordinate conjugates would
not give a valid input-to-output field map. Verify
\(p(b_0(\beta))=0\) and \(a<b_0(\beta)<b\). Then substitute
every original coefficient polynomial at \(b_0(\beta)\), reduce modulo
\(P\), and check all original affine rows, squared cone inequalities,
and cone signs by exact univariate algebraic arithmetic. This checks the
returned point against the original input system, not merely its rational
outer approximation.

All degree and height inputs to recognition are \(N^{O(h+1)}\), so
its requested accuracy is also \(N^{O(h+1)}\). The feasibility theorem
has polynomial bit complexity for fixed span and arbitrary dense field
degree. Substituting the printed box bits and recognition precision into
that theorem gives a polynomial in \(N\) with an effective exponent
depending only on \(h\). Multiplying by the polynomially many queries
preserves this form. This proves the stated \(N^{C_h}\) runtime.
There is no iteration of field extensions between oracle calls and no
assumption that \(D\) is constant.

## 6. Mixed-integer and algebraic optimal-level consequences

The common-field feasibility theorem returns a feasible integer assignment
\(z\) with polynomial bit length for fixed integer dimension \(k\)
and span \(h\). Substitute it in the original cone system and apply the
continuous theorem above. The field remains \(K\), the continuous
Hessians do not change, and the substituted encoding length remains
polynomial for fixed \(k,h\). Thus common-field MISOCP feasibility can
return an exact mixed-integer feasible point in polynomial time for fixed
\(k,h\), with dense field degree part of the input.

For a rational affine-fractional objective \(f(z,x)/d(z,x)\), suppose
an exact finite attained optimal ratio \(\theta\) is already known.
Its optimal level is the affine equation
\(f-\theta d=0\) over \(\mathbb Q(\theta)\). If the domain uses
the strict condition \(d>0\), represent it by one auxiliary continuous
variable \(s\) and the rational cone

\[
                    \|(2,d-s)\|_2\le d+s.                   \tag{11}
\]

This is equivalent to \(ds\ge1\) and \(d+s\ge0\), hence to
the existence of \(s>0\) with \(d>0\). The new squared residual
is \(4-4ds\), so it adds at most one Hessian direction. The augmented
system is closed. Applying the mixed-integer witness algorithm and
discarding \(s\) returns an original optimizer. This is a recovery
consequence conditional on a valid known value and attainment; it does
not prove a fractional-value encoding theorem.

A separate rational fractional-epigraph construction can also supply that
application. The common-field witness result is useful more generally and
is not presented as the only way to recover a fractional optimizer.

## 7. Prior comparison and limits

The [algebraic feasibility audit](algebraic-threshold-misocp-review.md)
and the rational [SOCP recovery note](socp-exact-witness-recovery.md)
identify the mathematical inputs. Direct elimination over a number field,
local-height estimates, minimum-norm selection, KLL recognition, and
primitive-element reconstruction are established tools. The contribution
here is the explicit decision-to-witness interface with a varying dense
input field, a common extension-field bound, and verification at the
selected real embedding. No independent publication novelty is asserted.

The output can lie outside the input field. For example, take
\(K=\mathbb Q(\sqrt2)\) with its positive embedding, impose
\(y=\sqrt2\), and impose

\[
             \|(\sqrt2,1)\|_2\le x,\qquad
             \|(x,\sqrt2x)\|_2\le3.
\]

These force \(x=\sqrt3\). The squared-Hessian span is one, while
the output field \(\mathbb Q(\sqrt2,\sqrt3)\) has degree four.
Thus requiring a witness in \(K\) would be false. The example also
illustrates why the input generator should be retained in (3).

This result provides an exact witness capability, not a numerical speedup
or a practical precision bound. The span restriction concerns the supplied
representation, and arbitrary nonconvex descriptions of convex sets are
outside the algorithm. Independently encoded algebraic coefficients without
a controlled common-field representation are also outside the input model.

## Verification record

The [field review](algebraic-socp-witness-field-review.md) and its
[independent audit](algebraic-socp-witness-field-independent.md) check the
one-limit argument, joint extension degree, local heights, primitive
element, and coordinate representation. The
[algorithm review](algebraic-socp-witness-recovery-review.md) checks fixed-field
queries, approximation of the same canonical point, recognition, selected
embedding, and both consequences. A further independent reviewer checked
the recovery interface. No unresolved gap was found. These reviews rely on
the linked perturbation and elimination lemmas and are not formal proofs.

The reviewers used exact inline SymPy calculations for proper extension
fields, their coordinate maps, the cone residuals, and embedding selection.
Those finite checks test the examples and representation mechanism, not
the universal degree, height, or complexity bounds. A targeted inline
Python document check covers final newlines, trailing whitespace, control
characters, paired math delimiters, and local Markdown links in this note
and its three reviews. No project-wide checks or CI inspection are used.
