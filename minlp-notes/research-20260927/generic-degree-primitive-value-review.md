# Independent review: a generic QCQP value generates its KKT field

Date: 2026-09-27. This review concerns the proposed sharpness argument for
`s` active quadratic constraints in `n` variables. It checks the field and
specialization steps independently. It does not claim a new generic KKT
count or establish novelty of the primitive-value observation.

The argument is valid with independent coefficient parameters, a common
parameter denominator, and Hilbert specialization inside the convex open
region. None of those qualifications should be omitted.

## The universal incidence

Write

\[
q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,\qquad 0\le i\le s,
\]

where the upper-triangular entries of the symmetric matrices, the linear
coefficients, and the constants are independent parameters over `Q`. Let
`K` be their rational function field. The incidence equations are

\[
q_i(x)=0\quad(1\le i\le s),\qquad
Q_0x+a_0+\sum_{i=1}^s\lambda_i(Q_ix+a_i)=0.
\]

Over the polynomial ring in all parameters, these equations solve explicitly
for `c_1,...,c_s` and `a_0`. The incidence coordinate ring is therefore a
polynomial ring in the remaining parameters, `x`, and `lambda`. In
particular, it is integral. This verifies that the incidence has one
function field, rather than an unexplained choice of a component.

The generic count

\[
[L:K]=D=2^s\binom ns
\]

is the classical quadratic specialization of Nie and Ranestad's generic
degree theorem, for `0 <= s <= n`. Its use here assumes the usual generic
finite, reduced KKT fiber. The source and its scope are recorded in the
[multihomogeneous prior audit](multihomogeneous-degree-prior.md).

## Derivatives recover all primal coordinates

Put `beta=q_0(x)` in `L`. For each `j`, let `D_j` be the derivation of `K`
that differentiates with respect to the independent parameter `a_{0,j}`
and fixes every other coefficient parameter. Characteristic zero gives a
unique extension to the finite algebraic extension `L`.

Differentiating the active constraints gives

\[
\nabla q_i(x)^T D_jx=0\qquad(1\le i\le s).
\]

The objective has the explicit coefficient derivative `x_j`. Consequently,

\[
D_j\beta=x_j+\nabla q_0(x)^TD_jx=x_j,
\]

where the last equality uses stationarity and the preceding identities.

Every derivation of `K` extends to `K(beta)` and remains in that field. More
explicitly, if `P(Y)` is the monic minimal polynomial of `beta` over `K`,
then

\[
D_j\beta=-\frac{(D_jP)(\beta)}{P'(\beta)}\in K(\beta).
\]

Separability makes the denominator nonzero. Uniqueness of extension makes
this derivative agree with the derivative computed in `L`. Thus
`x_j` belongs to `K(beta)` for every `j`.

The active-gradient matrix has generic column rank `s`: rank failure is
algebraic, and the real construction below supplies a full-rank incidence
point. Solving any nonsingular `s`-row subsystem of stationarity gives
`lambda` in `K(x)`. Since `beta` is a polynomial in `x` with coefficients
in `K`,

\[
L=K(x,\lambda)=K(x)=K(\beta).
\]

Therefore the generic objective value, the joint primal field, and the
entire KKT field all have degree `D` over the coefficient field.

The independent objective linear parameters are essential to this proof.
It does not assert the same primitive-element property for every fixed
coefficient family or every special instance.

## Specialization needs only parameter denominators

The power basis `1,beta,...,beta^(D-1)` expresses each `x_j` and each
`lambda_i` with coefficients in `K`. Choose one nonzero polynomial `H` in
the parameters clearing all those coefficients and all coefficients of
the minimal polynomial. Multiplying the identities by `H` gives polynomial
identities on the integral universal incidence. They consequently hold at
every incidence point after specialization, not merely at generic points.

Choose a rational coefficient specialization `p` with `H(p) != 0` for which
the specialized minimal polynomial remains irreducible of degree `D`.
Every specialized KKT point then has a value satisfying that polynomial,
so its value field has degree `D`. The specialized coordinate identities
give `Q(x,lambda) subseteq Q(beta)`, and the objective formula gives the
reverse inclusion for `Q(x)`. Hence

\[
[\mathbb Q(\beta):\mathbb Q]
=[\mathbb Q(x):\mathbb Q]
=[\mathbb Q(x,\lambda):\mathbb Q]=D.
\]

This reasoning avoids denominators that depend on the selected root.
Merely saying that generic rational-function identities can be specialized
would leave that point unproved.

## A full-dimensional convex open region

For `1 <= s <= n`, begin with

\[
Q_i=I\ (0\le i\le s),\quad
a_i=e_i,\quad c_i=0\ (1\le i\le s),\quad
a_0=-\sum_{i=1}^se_i.
\]

At `x=0`, all constraints are active and `lambda_i=1` satisfies
stationarity. The active gradients are `e_1,...,e_s`, and the Lagrangian
Hessian is `(s+1)I`. The square KKT Jacobian is nonsingular by its Schur
complement. The implicit function theorem therefore gives a KKT point
nearby for every coefficient tuple in a real open neighborhood. Shrinking
the neighborhood preserves positive definite Hessians, independent active
gradients, and strictly positive multipliers. The resulting primal point
is the unique global minimizer, by strict convexity and the sufficient
convex KKT conditions.

Strict feasibility is also present at the base point: take
`x=-eta sum_i e_i` with `0 < eta < 2/s`. It remains available in a smaller
neighborhood. Although the base constraint Hessians coincide, the nearby
tuples with linearly independent constraint Hessians form a nonempty
Zariski open subset. Thus the sharpness example can have native Hessian
span exactly `s`.

Hilbert irreducibility must be used in a form that reaches this real open
neighborhood. One can derive the needed density from standard integral
multivariate Hilbert irreducibility. Choose a rational coefficient tuple
`b` inside the neighborhood and substitute `p_i=b_i+1/t_i`. This is a
rational function field isomorphism and preserves irreducibility. Apply
integral Hilbert irreducibility while excluding the finitely many
hyperplanes `t_i=j`, `|j| <= M`, and the transformed denominator and leading
coefficient hypersurfaces. An integral specialization then has
`|t_i| > M`, so `p` is arbitrarily close to `b`. This is the precise
approximation requirement; bare existence of an irreducible rational
specialization would not be sufficient.

## Follow-up audit of the Hilbert irreducibility citation

The sharpness manuscript now cites Castillo and Dietmann,
[On Hilbert's Irreducibility Theorem](https://arxiv.org/pdf/1602.00314).
I independently read Theorem 1 and Corollary 2 on printed pages 1--2,
and the proof's treatment of exceptional specializations on pages 10--11.
The polynomial may have any number of parameter variables and need not be
monic. Corollary 2 bounds reducible integral specializations in a box by
`O(H^(r-1+gamma_G+epsilon))`. Section 5 separately bounds degree drops and
inseparable specializations by `O(H^(r-1))`, using the leading coefficient
and discriminant. These hypotheses support the citation.

For completeness, the application has the following exact details. After
the birational substitution, clear denominators in the minimal polynomial
and remove its content as a polynomial in `Y` over `Q[u]`. Then clear
rational numerical denominators and remove integer content. Gauss's lemma
makes the resulting primitive integer polynomial `f(u,Y)` irreducible; its
degree in `Y` remains `D`. Since `D>1` here, its Galois group is transitive
and every intransitive subgroup is proper. Thus `gamma_G <= 1/2`. Fixing
`epsilon=1/4` makes the number of reducible specializations `o(H^r)`.

Exclude the zero sets of the leading coefficient of `f`, its discriminant,
the transformed original parameter-denominator numerators, and all factors
`u_j-k` with integer `|k| <= M`. Each factor is nonzero as a polynomial;
the birational change cannot turn a nonzero parameter denominator into the
zero rational function. Their product has `O(H^(r-1))` integer zeros in
the box. Outside this union and the reducible specializations there remain
integer tuples for large `H`, since the box contains order `H^r` tuples.
The leading-coefficient exclusion explicitly preserves degree and ensures
that the primitive representative is a nonzero scalar multiple of the
specialized monic minimal polynomial. The denominator exclusions preserve
the coordinate recovery identities. Finally, `|u_j| > M` puts the rational
coefficient tuple in the required convex open neighborhood.

The case `D=1` is handled separately in the sharpness manuscript and does
not require the definition of `gamma_G` for a one-point action. No effective
coefficient bound for the final convex instance is asserted.

## Verification and limits

The review independently checked the incidence parametrization, extension
of coefficient derivations, stationarity cancellation, denominator
clearing, the real KKT Jacobian, and the convexity argument. It read the
local Nie--Ranestad source audit. A primary-source search also located
Dèbes's
[Density Results for Hilbert Subsets](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/pierre_debes/A27-HITDensity.pdf),
whose introduction states a stronger approximation result for Hilbert
subsets; that result is not needed in the proof above.

This is an existence argument for rational convex instances. It supplies
no coefficient-size bound and no explicit rational instance in arbitrary
dimension. The generic count is prior work. The sharpness claim still
depends on applying that count with exactly the coefficient space described
here, and it does not establish novelty of any broader Hessian-span theorem.
No numerical test, project-wide verification, or CI inspection was needed.
