# Canonical fields for fractions with one shared quadratic form

Date: 2026-09-28. Status: independent proof review. The canonical field
argument is valid when every numerator has a strictly positive multiple
of one full positive semidefinite quadratic form. An independent
subreview checked the common-gradient argument, the integer cross terms,
and the auxiliary-variable selector. Zero curvature multipliers require
a different statement; Section 6 gives an actual-optimum counterexample.

This note supplies encoding bounds and a rational-matrix description of
the optimal continuous fiber. Value computation, integer bounds, and
attainment algorithms are separate inputs.

## 1. Normalize the shared curvature

Write \(w=(z,x)\), with integer coordinates \(z\) and continuous
coordinates \(x\). Let the rational native feasible set \(F\) be closed
and convex, described by PSD quadratic or SOC constraints and affine
rows. Keep SOC right-hand-side signs when using squared polynomials.
Consider

\[
 \Phi(w)=\max_{1\le j\le m}
 \frac{\lambda_j B(w)+a_j^Tw+c_j}{d_j(w)},\qquad
 B(w)=\tfrac12w^TQw,\quad Q\succeq0,
 \quad\lambda_j>0,\quad d_j>0\text{ on }F.                \tag{1}
\]

All data, including the strictly positive multipliers, are rational and
explicitly encoded; \(m\ge1\). The rank of \(Q\) is unrestricted and
is excluded from the native range parameter. Divide the numerator and
denominator of ratio \(j\) by \(\lambda_j\). This leaves that ratio
unchanged, preserves denominator positivity, and increases encoding
length only polynomially. Henceforth use the normalized notation

\[
                     \Phi(w)=\max_j\frac{B(w)+a_j^Tw+c_j}{d_j(w)}.
                                                               \tag{2}
\]

Let \(H_i\) be the full native Hessians and set

\[
 L_* =\{h:H_i(0,h)=0\text{ for every }i\},\qquad
 L=L_*\cap\bigcap_j\ker d_{j,x}^T,
 \quad r=\operatorname{codim}L\le\rho+\ell,               \tag{3}
\]

where \(\rho=\operatorname{codim}L_*\), and \(\ell\) is the rank of
the denominator linear forms restricted to \(L_*\). Positive scaling
of each denominator does not change this rank. Fix a rational split
\(x=T_1u+T_0v\) with \(\operatorname{range}T_0=L\) and
\(u\in\mathbb R^r\). Rational linear algebra gives polynomial-bit
transformation matrices. This split can be fixed before integer
substitution.

Fix an integer assignment \(z=\bar z\), and include its bit length in
the current rational input length \(N\). Let \(\theta\) be a finite
lower bound for \(\Phi\) throughout this continuous fiber, and assume
that its \(\theta\)-sublevel is nonempty. Thus \(\theta\) is exactly
the attained continuous minimum in this fiber. Let its selected real
embedding have minimal-polynomial degree \(D\), coefficient bits \(H\),
and an isolating interval; put \(K=\mathbb Q(\theta)\).

The following conclusions hold for some effective functions and an
absolute constant \(C\). The projected optimal set has a unique
minimum-norm point \(u^*\). Its optimal fiber has a unique minimum-norm
point \(v^*\), and

\[
 \begin{split}
 [\mathbb Q(\theta,u^*):\mathbb Q]&\le f(r,D),\\
 K(u^*,v^*,B(w^*),Qw^*)&=K(u^*),\\
 \operatorname{encoding}(\theta,u^*,v^*,w^*,B(w^*),Qw^*)
      &\le f(r,D)(N+H+1)^C.                              \tag{4}
 \end{split}
\]

Encoding means one rational univariate representation, including the
selected value embedding. The same bound controls each coordinate's
primitive integer minimal-polynomial coefficient bits and a containing
box. The point is canonical for the fixed split, not necessarily for the
norm in the original coordinates.

## 2. The full shared gradient and quadratic value are constant

The continuous optimal set is

\[
 O=\{x:(\bar z,x)\in F,\quad
 h_j(\bar z,x):=B(\bar z,x)+a_j^T(\bar z,x)+c_j
                         -\theta d_j(\bar z,x)\le0\ \forall j\}.
                                                               \tag{5}
\]

It is nonempty, closed, and convex. For two of its points \(x,y\), put
\(\delta=(0,x-y)\). Each normalized residual satisfies

\[
 h_j(\bar z,(x+y)/2)
   =\tfrac12h_j(\bar z,x)+\tfrac12h_j(\bar z,y)
                         -\tfrac18\delta^TQ\delta.        \tag{6}
\]

If \(\delta^TQ\delta>0\), every residual at the midpoint is strictly
negative. Each denominator is positive, so every ratio there is strictly
less than \(\theta\). There are finitely many ratios, making their
maximum strictly less than \(\theta\), a contradiction. Therefore
\(\delta^TQ\delta=0\), and the full condition \(Q\succeq0\) gives

\[
                  Q\delta=0.                            \tag{7}
\]

It follows that both the full vector \(g^*=Q(\bar z,x)\) and
\(B^*=B(\bar z,x)\) are constant on \(O\). Indeed, the two full
points differ by a vector in \(\ker Q\). This proves constancy without
assuming that the integer-continuous cross block vanishes. Each
unnormalized numerator gradient is also constant, being
\(\lambda_j g^*+a_j\) in the original notation. Ratio gradients need
not be constant.

The use of the full PSD matrix matters. Its block form implies
\(\ker Q_{xx}\subseteq\ker Q_{zx}\). Merely knowing that
\(Q_{xx}(x-y)=0\) would not, for a general non-PSD full matrix, imply
that the linear cross term \((Q_{xz}\bar z)^Tx\) is constant.

## 3. One auxiliary variable gives rational QP charts

At the fixed integer assignment, the native constraints have the form
\(Cv\le b(u)\), with constant rational \(C\) and quadratic rational
\(b\). All denominators depend only on \(u\). Introduce a scalar
\(\eta\) and use the affine rows

\[
 \eta+a_j^T(\bar z,T_1u+T_0v)+c_j
                           \le\theta d_j(\bar z,T_1u).   \tag{8}
\]

For every native-feasible \((u,v)\), sufficiently negative \(\eta\)
satisfies all these rows. Thus the lifted polyhedral fiber is nonempty
exactly when the native fiber is nonempty. On this polyhedron minimize
the convex quadratic

\[
               L_u(v,\eta)=B(\bar z,T_1u+T_0v)-\eta.       \tag{9}
\]

It is bounded below by zero. A negative value would imply, for every
\(j\),

\[
 B(\bar z,x)+a_j^T(\bar z,x)+c_j
     <\eta+a_j^T(\bar z,x)+c_j\le\theta d_j(\bar z,x),
\]

contradicting the lower bound \(\Phi\ge\theta\). A bounded-below
convex quadratic over a nonempty polyhedron attains its minimum,
including for the real right-hand sides occurring here. The real-data
argument is recorded in
[the quadratic optimization note, Section 2](common-range-optimization.md#2-a-parametric-convex-qp-projection).

If \(u\) is the projection of an optimum, its minimum in (9) is zero.
Its QP optimizers are precisely the lifts of the original optimal points
in that fiber, with \(\eta=B(\bar z,x)\). In particular, a feasible
lift satisfying \(L_u\le0\) has equality and projects to an optimum.
By Section 2 every such \(\eta\) equals the same number \(B^*\), even
across different optimal \(u\). Consequently minimizing
\(\|(v,\eta)\|^2\) among these QP optimizers selects exactly the
minimum-norm original optimal \(v\).

Apply [the constant-matrix QP chart lemma](common-range-optimizer-witness.md#2-constant-matrix-quadratic-programming-charts)
to \(y=(v,\eta)\). The constraint matrix consists of native rows
\((C_i,0)\) and rows \((a_{j,x}^TT_0,1)\), all rational. Its
right-hand sides are rational polynomials of degree at most two jointly
in \((u,\theta)\). In particular, the term \(\theta d_j(u)\) never
multiplies \(v\). The objective Hessian is the constant rational matrix

\[
 \begin{pmatrix}T_0^TQ_{xx}T_0&0\\0&0\end{pmatrix}\succeq0,
\]

and its linear coefficient in \(y\) is affine rational in \(u\), with
last coordinate \(-1\). Thus every chart KKT matrix is constant rational,
independent of \(u\) and \(\theta\). Its Moore--Penrose inverse is
rational with polynomial-bit coefficients, including singular cases.

There are finitely many charts
\(y_I(u,t)=(v_I(u,t),\eta_I(u,t))\), each a rational polynomial map
of degree at most two jointly in \((u,t)\). One represents the
minimum-norm QP optimizer in every nonempty fiber. This use requires a
basis of all active row normals, including rows with zero multiplier,
as in the cited chart lemma.

Let \(D_I(u,t)\) mean that the chart output satisfies every lifted
polyhedral row, and define

\[
 G_I(u,t)=B(\bar z,T_1u+T_0v_I(u,t))-\eta_I(u,t),\qquad
 S_{I,\theta}=\{u:D_I(u,\theta),\ G_I(u,\theta)\le0\}.    \tag{10}
\]

The rows in \(D_I\) have degree at most two in \((u,t)\); \(G_I\)
has degree at most four. Every coefficient has polynomial bit length.
The exact identity

\[
                         \pi_u O=\bigcup_I S_{I,\theta}   \tag{11}
\]

follows by selecting the minimum-norm QP optimizer in each optimal fiber
and by the reverse feasibility implication after (9). No multiplier-sign
or stationarity-consistency guard is needed in the chart sets: an
admitted chart point is an actual feasible lift.

Equation (11) proves that \(\pi_u O\) is closed. It is convex as the
projection of \(O\), so its minimum-norm point \(u^*\) exists and is
unique. Choose the chart representing the minimum-norm QP optimizer above
this \(u^*\). By the constant-\(\eta\) argument, it represents
\((v^*,B^*)\). The point \(u^*\) is the unique minimum-norm point of
that one basic closed chart set, because the chart set contains \(u^*\)
and is contained in \(\pi_uO\).

## 4. Degree, height, and one common field

Use the selected chart from Section 3. Encode the intended \(\theta\)
by \(P_\theta(t)=0\) and a closed rational isolating interval. Root
separation permits interval endpoint bits polynomial in \(D+H\) for
this existence argument. The given isolator selects which root is meant.

For coordinate \(j\), append a scalar output \(s=u_j\) and describe
the unique norm minimizer by

\[
 \exists(u,t)\left[
 P_\theta(t)=0,\ t\in[a,b],\ D_I(u,t),\ G_I(u,t)\le0,\ s=u_j,
 \quad
 \forall u'\bigl[(D_I(u',t)\wedge G_I(u',t)\le0)
                 \Rightarrow\|u\|^2\le\|u'\|^2\bigr]
 \right].                                                \tag{12}
\]

It defines exactly \(\{u_j^*\}\). The quantifier blocks have dimensions
\(r+1\) and \(r\), there is one scalar free variable, and polynomial
degree is at most \(\max(4,D)\). Coefficient bits are bounded by
\(f(D)(N+H+1)^{C_0}\) with an absolute \(C_0\), clearing denominators
separately in each row.

The coefficient-sensitive quantifier-elimination theorem bounds each
output polynomial's degree by a function of these dimensions and degree,
and its coefficient bits by that function times the input bit bound.
These per-polynomial bounds are independent of predicate count. The
precise source is
[Basu--Pollack--Roy, Theorem 1.3.1](https://doi.org/10.1145/235809.235813)
and its well-behavedness condition, also stated in
[Basu's author survey, Theorem 2.27](https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf).
The source text was inspected for the preceding quadratic fractional
field review, whose [Section 3](common-range-quadratic-fractional-field-review.md#3-a-direct-bound-using-classical-quantifier-elimination)
gives the identical singleton argument.

A nonzero output polynomial must vanish at the singleton coordinate,
since otherwise every predicate sign would be locally constant. Thus
each retained coordinate has bounded degree and height of the form (4).
Multiplying those degree bounds across only \(r\) coordinates, and
including \(\theta\), gives a common field of degree \(f(r,D)\).
The selected \((v^*,B^*)=y_I(u^*,\theta)\) is a rational quadratic
polynomial map, and \(w^*\) and \(g^*=Qw^*\) are rational affine maps
of its outputs. They add no field extension.

Polynomial evaluation, Weil-height inequalities, and conversion from
Weil heights to integer minimal-polynomial heights preserve an absolute
input exponent. A primitive-element choice and trace-pairing linear
algebra give one rational univariate representation of the full tuple;
the details are in
[the quadratic fractional field review, Section 4](common-range-quadratic-fractional-field-review.md#4-the-fiber-and-gradient-add-no-extension).
The number of original coordinates and ratios only contributes an
absolute polynomial factor in the explicit input length. There is no
degree multiplication over them. If \(r=0\), the empty retained tuple
requires no QE: the chart map directly gives \((v^*,B^*)\in K^{n+1}\).

## 5. Rational optimal fibers and uniform conditional boxes

The common full gradient also gives a linear description of the optimal
fiber after fixing \(u^*\). Obtain any \(w_0\in K(u^*)^{k+n}\) with
\(Qw_0=g^*\) by rational row reduction, and put
\(B_0=\tfrac12w_0^TQw_0\). The particular integer coordinates of
\(w_0\) need not equal \(\bar z\). On \(Qw=g^*\), the difference
\(w-w_0\) lies in \(\ker Q\), hence \(B(w)=B_0=B^*\).
The original optimal fiber is exactly

\[
 \begin{split}
 &Cv\le b(u^*),\qquad Q(\bar z,T_1u^*+T_0v)=g^*,\\
 &a_j^T(\bar z,T_1u^*+T_0v)+c_j
                  \le\theta d_j(\bar z,T_1u^*)-B_0
                       \qquad(1\le j\le m).
 \end{split}                                               \tag{13}
\]

All coefficient matrices on \(v\) are rational. The algebraic data occur
only on right-hand sides, as degree-at-most-two polynomials in
\((\theta,u^*,g^*)\) with polynomial-bit rational coefficients. Thus
the rational-matrix approximation and minimum-norm QP completion method
used for a single quadratic fraction applies to this fiber. The common
gradient can be approximated using rational affine cuts once an
optimal-set value oracle is available. These observations do not supply
that oracle by themselves.

For mixed-integer attainment, let \(N_0\) be the original input length,
suppose the original global infimum is the known finite \(\theta\), and
consider every integer assignment with bit length at most \(M\).
Rational substitution has size polynomial in \(N_0+M\).
In each fiber, \(\Phi\ge\theta\). A nonempty
\(\theta\)-sublevel is therefore an attained optimal set of precisely
the kind used above. One computable bound

\[
                       \log_2 R\le f(r,D)(N_0+M+H+1)^C      \tag{14}
\]

contains its canonical point, uniformly over all those assignments.
Empty sublevels require no point. A supplied or separately proved bound
for some attaining integer assignment, together with (14), permits the
usual compact-box comparison with \(\theta\). That comparison uses the
actual global infimum; it does not require a canonical theorem for
arbitrary nonoptimal sublevels.

## 6. Boundaries and counterexamples

Strict positivity of every \(\lambda_j\) is substantive. The simple
example \(\max\{x^2,1\}\), with unit denominators and no native rows,
has minimum one on \([-1,1]\); the shared quadratic value and gradient
vary over the optimal set. A stronger example is

\[
                         \min_{v\in\mathbb R}\max\{(v-2)^2,2\}.
                                                               \tag{15}
\]

Its actual optimum is the rational number two, \(r=0\), and its
minimum-norm optimizer is \(2-\sqrt2\), outside the value field
\(\mathbb Q\). The constant numerator has multiplier zero. Thus even
the same-field canonical conclusion would fail if zero multipliers were
admitted without changing the statement.

At a nonoptimal threshold, positive multipliers do not rescue that
conclusion: the single ratio \((v-2)^2/1\) at threshold two has the
same minimum-norm sublevel point \(2-\sqrt2\), while \(r=0\) and the
threshold is rational. The proof of (9)'s nonnegative objective and the
transfer from minimum norm in \((v,\eta)\) to minimum norm in \(v\)
both use that \(\theta\) is a true lower bound.

Finally, full PSD cannot silently be replaced by PSD of the continuous
block alone in the constancy argument. Let

\[
 Q=\begin{pmatrix}2&1\\1&0\end{pmatrix},\qquad
 B(z,x)=z^2+zx,\qquad
 F=\{z=1,-1\le x\le1\},\qquad q=B-x-1,
 \quad d=1.                                               \tag{16}
\]

The continuous block is zero, and every point of this fixed fiber is
optimal with value zero. But \(B(1,x)=1+x\). Its original minimum-norm
point is \(x=0\), whereas minimizing \(x^2+\eta^2\) with
\(\eta=1+x\) gives \(x=-1/2\). The full matrix is indefinite, so
(16) is outside the stated theorem. It isolates the need to account for
integer cross terms when justifying the selector.

These counterexamples do not assert impossibility of other algorithms or
other canonical choices beyond the stated assumptions.

## 7. Verification record

The proof review checked positive normalization, the simultaneous strict
midpoint gap, the full-PSD cross-block implication, nonnegative and
attaining lifted QPs, rational constant chart matrices, closedness, the
same-field selector, and uniform conditional integer-fiber boxes. A
separate subreview reconstructed these points and supplied the
counterexamples in (15)--(16).

The final read of
[the main shared-curvature proof](common-range-shared-curvature-fractional.md)
also found no gap in its field and recovery steps, its conditional compact
attainment comparison, or its negative recession calculation. The imported
quasiconvex mixed-value theorem and the literature-priority question were
outside this fresh review's scope.

An inline `python -` command with SymPy checked positive normalization,
a constant rational KKT chart with a nonzero integer-continuous cross
term, and the quartic degree of its residual. Specifically, for
\(B(z,v)=(z+v)^2/2\), the active equations
\(v=u^2\) and \(\eta+v=\theta(u+2)\) produce
\((v,\eta)=(u^2,\theta(u+2)-u^2)\). The same command checked the
minimal polynomial of \(2-\sqrt2\), the norm selector in (16), and
a PSD cross-kernel identity. Every assertion passed. These examples
illustrate the argument; they do not prove the universal bounds.

A targeted inline `python -` document check tested this file's local
links, paired math delimiters, final newline, control characters, and
trailing whitespace. It passed. No project-wide verification or CI status
or logs were inspected.
