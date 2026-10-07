# A constant-base polynomial component solver through joint critical limits

Date: 2026-10-02. Status: deterministic component construction with a
[fresh independent completed-text review](../reviews/polynomial-component-primitive-limit-review.md)
finding no substantive gap, and targeted exact diagnostics passing.
No index or priority claim. The complete strong-field composition is
outside this note.

The [earlier constructive fallback](polynomial-exact-fallback-construction.md)
uses separate coordinate limit polynomials and then pairs all their roots.
That loses a constant-base exponential bound in component dimension. The
construction below instead recovers all coordinates from one scalar root,
using a characteristic polynomial and its directional derivatives. It
does not assume generic linear perturbations or a radical stationary ideal.

## 1. Component interface

Fix a total degree bound `d`. Let `f` be an explicitly represented rational
polynomial on a nonempty bounded closed rational continuous box of dimension `k`.
Let `H` denote the input encoding length, including any sampled rational
linear coefficients. The deterministic bound is

\[
                       c_d^k\operatorname{poly}_d(H+1)
 \tag{1}
\]

bit operations for an exact global optimizer and value. The exponent of
the input polynomial is independent of `k`. The same representation permits
point and value refinement, and feasible rational approximations with a
certified value gap, in `c_d^k poly_d(H+q+1)` work for `q` accuracy bits.

An output consists of one real root `alpha` of a rational univariate
polynomial, its rational isolating interval, and rational polynomials
`r_i` such that the optimizer coordinates are `r_i(alpha)`. Fixed face
coordinates are recorded directly. The value can be `f(r(alpha))` or
a separately isolated root of its resultant polynomial. Expanded minimal
polynomials are not required.

For a mixed component, enumerate its native-integer labels first. If it
has `k_c` continuous coordinates and integer label counts `N_i`, the
resulting work is

\[
       c_d^{k_c}\left(\prod_{i\text{ integer}}N_i\right)
                         \operatorname{poly}_d(H+1).
 \tag{2}
\]

Substituting integer labels and rational bounds preserves fixed degree
and polynomial coefficient length. The proof below concerns one such
continuous problem. It handles every rational objective, including ties,
empty stationary faces, and positive-dimensional minimizer sets.

## 2. A finite flat deformation on each face

Enumerate the `3^k` lower/free/upper continuous faces. A vertex is already
a feasible candidate. On a face with `r>0` free variables, restrict the
objective and choose a fixed even `D>d`, putting `a=D-1`. For symbolic
`epsilon>0`, use

\[
               f_\varepsilon(x)=f(x)+\varepsilon\sum_i x_i^D.
 \tag{3}
\]

Let `z=1/epsilon`. The free stationary equations become

\[
            x_i^a+(z/D)\partial_i f(x)=0,
                       \qquad i=1,\ldots,r.
 \tag{4}
\]

For a degree-first monomial order their leading monomials are the coprime
powers `x_i^a`. The product criterion therefore makes these equations a
Groebner basis. Over `Q(z)`, and after every finite specialization of `z`,
the quotient has basis

\[
 \mathcal M=\{x_1^{e_1}\cdots x_r^{e_r}:0\le e_i<a\},
                         N=a^r.
 \tag{5}
\]

Its ideal may be nonradical. Its constant quotient dimension, rather
than radicality, is what is used below. Let `M_i(z)` be the multiplication
matrix of `x_i`. Its entries are polynomials in `z` with rational
coefficients.

For a coefficient vector `lambda`, put

\[
 M_\lambda(z)=\sum_i\lambda_iM_i(z),\qquad
 \chi_\lambda(z,T)=\det(TI-M_\lambda(z)).
 \tag{6}
\]

Also compute the independent coefficient derivatives

\[
 q_{\lambda,i}(z,T)=
 -\left.\frac{\partial}{\partial u}
       \det(TI-M_\lambda(z)-uM_i(z))\right|_{u=0}.
 \tag{7}
\]

These are derivatives with respect to individual linear-form coefficients,
not derivatives with respect to the scalar index of the forms used next.

## 3. Enumerating forms without trusting a separation test

Consider the moment-curve forms

\[
 \lambda(t)=(1,t,t^2,\ldots,t^{r-1}),\qquad
 t=0,\ldots,Q-1,
 \quad Q=1+(r-1)\left(N+\binom N2\right).
 \tag{8}
\]

For each form, perform the following exact operations.

1. Let `K` be the degree in `z` of `chi_lambda`, and set
   `p(T)=[z^K]chi_lambda(z,T)`. If `p` is constant, skip this form.
2. If any `q_lambda,i` has degree in `z` exceeding `K`, skip the form.
   Otherwise put `b_i(T)=[z^K]q_lambda,i(z,T)`.
3. Let `G=gcd(p,p')`, `P=p/G`, and `A=p'/G`. If `G` does not divide
   some `b_i`, skip the form. Otherwise let `B_i=b_i/G`.
4. The polynomial `P` is squarefree up to a scalar and `gcd(A,P)=1`.
   Use the extended Euclidean algorithm to compute
   `r_i=B_i A^(-1) mod P`.
5. Isolate every real root `alpha` of `P`, evaluate the signs of
   `r_i(alpha)-ell_i` and `u_i-r_i(alpha)`, and retain the tuple only
   if it belongs to this closed face box. Include its fixed coordinates.

This procedure need not determine which form is good. A bad form may
fail a test or produce spurious reconstructed points. Every retained
point is nevertheless exactly feasible. Such extra candidates cannot
improve on the original true optimum. Completeness follows because at
least one enumerated form has the properties proved below.

## 4. Why one form recovers every finite critical limit

Over the algebraic closure of `Q(epsilon)`, list the geometric solutions
of (4), with their local algebra multiplicities. Their total multiplicity
is `N`. The standard algebraic Puiseux expansion theorem describes their
branches as `epsilon` tends to zero. No expansion is computed by the
algorithm; only its existence is used in this proof.

A bounded branch has a finite vector limit `v`. An unbounded branch has
a most negative exponent and a nonzero leading-pole vector `w`, so it
has the form `epsilon^(-s)(w+o(1))`, `s>0`, after zero entries are allowed
in `w`. There are at most `N` branches and at most `N` distinct bounded
limits. Choose a linear form that

- does not annihilate any such nonzero leading-pole vector; and
- separates every pair of distinct bounded vector limits.

For the moment curve (8), each forbidden condition is a nonzero polynomial
in `t` of degree at most `r-1`, even when the vectors are complex. There
are at most `N+binom(N,2)` conditions. Hence at least one of the `Q`
integer forms is good. For `r=1`, the single form suffices.

For a good form, a projected branch is bounded exactly when the original
vector branch is bounded. Multiplication matrices have these projected
coordinates as eigenvalues, repeated according to local multiplicity.
Consequently the leading coefficient as `z=1/epsilon` tends to infinity
has the factorization

\[
 p_\lambda(T)=C(\lambda)
       \prod_{v\text{ distinct finite limit}}
                       (T-\lambda^{\mathsf T}v)^{\mu_v},
                    \qquad C(\lambda)\ne0.
 \tag{9}
\]

Here `mu_v` collects the multiplicities of all bounded branches with
the same vector limit. The leading power `K` is locally constant as
`lambda` varies near a good form: every unbounded projection retains its
leading pole. The coefficients of `chi` and its derivatives are ordinary
polynomials in `z`; in particular the sum of the branch pole exponents
in this leading product is the integer `K`.

Differentiating before specializing the independent form coefficients
therefore gives

\[
 b_i(T)=-\partial_{\lambda_i}p_\lambda(T)
 =-C_i\prod_v(T-\lambda^{\mathsf T}v)^{\mu_v}
  +C\sum_v\mu_v v_i
    \frac{\prod_u(T-\lambda^{\mathsf T}u)^{\mu_u}}
                         {T-\lambda^{\mathsf T}v}.
 \tag{10}
\]

In particular, good forms pass both the degree and divisibility tests.
At `alpha=lambda'v`, divide (10) and `p'` by `G`. The term differentiating
`C` vanishes, and the remaining common nonzero factor cancels, giving

\[
                         B_i(\alpha)/A(\alpha)=v_i.
 \tag{11}
\]

The factor is nonzero because distinct vector limits have distinct
projections and the multiplicities are nonzero in characteristic zero.
Thus the construction recovers every bounded critical limit jointly.
If a projected root is real, separation and conjugation show that its
vector limit is real: a nonreal limit would have a distinct conjugate with
the same real projection. The method does not pair coordinates chosen
from unrelated algebraic branches.

There is an original global optimizer among these limits and the vertex
candidates. For a sequence of positive `epsilon` tending to zero, choose
a global box minimizer of (3). Compactness gives a convergent subsequence;
uniform convergence to `f` makes its limit an original global minimizer.
There are finitely many faces and algebraic branches, so a further
subsequence uses one face and one bounded stationary branch, unless its
face has dimension zero and is already enumerated. Its limit belongs to
the closed face. A good form for that face reconstructs it. Taking the
least original objective value among all retained feasible candidates
therefore returns an exact global optimizer on every input.

## 5. The matrix construction has constant-base exponential work

A naive reduction tree can have `s^{O(r)}` paths when `s` is the number
of input monomials. That is not the desired complexity. Instead memoize
the normal forms of every monomial of total degree at most

\[
                         R=r(a-1)+1.
 \tag{12}
\]

There are `binom(r+R,r)=c_d^r` such monomials. A reduction replaces a
factor `x_i^a` by `-(z/D)partial_i f`, lowering total degree by at least
one. Thus all needed recurrences use previously computed lower-degree
normal forms. Each has at most the input number of derivative monomials,
and every resulting vector has `N` entries. Its `z` degree is at most
`R`. With a common denominator for the input coefficients, its coefficient
bit lengths are polynomial in `H` and `r`: there are at most `R` reduction
steps along a path, and the logarithm of the number of paths is at most
`O(R log(s+1))`. Memoization avoids enumerating those paths.

Consequently all multiplication matrices have `c_d^r poly_d(H)`
construction cost, polynomial `z` degree in `r`, and polynomial rational
coefficient height. The integers `t` in (8) have `O(r+log r)` bits at
fixed degree; their powers have polynomial length in `r`. Forming
`M_lambda` does not change the height conclusion.

The determinants in (6)--(7) have size `N`, degree at most `N` in each
of `T,u`, and degree at most `RN` in `z`. Their coefficient bit lengths
are at most a polynomial in `N,H,r`. Exact multivariate interpolation
and rational determinant calculation, or fraction-free polynomial matrix
algorithms, compute them within such a polynomial bound. Only the three
variables `z,T,u` occur in this step; no dense polynomial in `r` independent
form coefficients is constructed. A derivative can be extracted as the
coefficient of `u` after interpolation. This is `c_d^r poly_d(H)` work
because every exponent of `N` is absolute.

There are `Q=O(rN^2)` forms, at most `N` real roots per form, and `r`
coordinate polynomials per root. Polynomial gcd, exact division, modular
inversion, root isolation, and signs at an isolated real root all have
bit work polynomial in their univariate degrees and coefficient lengths.
Their dimensions and heights above are `c_d^r poly_d(H)`. The candidate
count is `O(rN^3)`, still constant-base exponential. Summing over the
`3^k` original faces preserves (1).

## 6. Comparing values without an exponential Cartesian compositum

For a candidate root of `P`, its coordinates are all polynomials of the
same `alpha`. Form `V(T)=f(r_1(T),...,r_r(T))`, including fixed coordinates,
and clear its rational coefficient denominator. Its degree before reduction
is at most `d(N-1)` and its height is polynomial in the existing degree and
height bounds. Reducing modulo `P` is optional.

If `V=H_1/q_1` with nonzero integer `q_1`, the nonzero resultant

\[
                         \operatorname{Res}_T
                              (P(T),q_1 Z-H_1(T))
 \tag{13}
\]

has degree at most `N` in the value variable `Z`. Isolate its distinct
real roots and identify the candidate's value by refining its already
isolated `alpha`. Effective univariate root separation bounds make the
required precision polynomial in the degree and coefficient heights;
coincident value roots are first combined by squarefree reduction.
Alternatively, standard exact arithmetic at algebraic roots gives the
same comparisons. Comparing values from different candidates uses two
univariate representations of degree at most `N`, not `r` independent
coordinate extensions. Thus ties can be decided exactly in the required
bound, without indefinite interval refinement. For example, isolate the
squarefree product of the two value polynomials; equal values then have
the same root identifier.

After selection, root refinement and rational polynomial evaluation give
point and value enclosures with `q` extra bits in the same type of cost.
Clip continuous rational approximants to the original box and recover
integer labels exactly. A rational gradient bound on the box and the
separate exact-value enclosure supply a feasible rational point with any
requested certified objective gap. These bounds depend polynomially on
the additional coefficient and accuracy bits, rather than putting them
inside a dimension-dependent exponent.

For independent components, retain one such representation per component
and a sum of their exact value expressions. Expanding the sum into one
global minimal polynomial is unnecessary and can have exponential degree
even when every component is small. This structured output distinction
is necessary for an expected polynomial-work strong-field application.

## 7. Implication to check before a strong-field extension

The construction supplies the component-work bound needed by the
component-weight argument in [strong-field QP](strong-field-component-qp.md):
a degree-dependent constant `c_d` for each continuous coordinate and its
label count for each integer coordinate. A polynomial's derivative-range
enclosures can be computed by rational monomial bounds. Nonbad coordinates
are fixed by the same strict monotonicity tests, and components of the
original monomial interaction graph separate after substitution.

This route would require no generic-noise exception budget for component
algebra: the component solver itself is exact on every draw. The strong-noise
condition remains material, and expected output must use the structured
component representations just described. This section records the intended
interface, not a promotion or a completed smoothed theorem.

The proof uses classical finite quotient algebras, characteristic
polynomials, algebraic branch expansions, and exact univariate algorithms.
It should be compared with existing critical-point and rational-univariate
representation methods before any originality assessment. Missing source
requests are routed through the literature agent and sole ingester.

## 8. Targeted diagnostic

The exact-rational diagnostic
[check_polynomial_primitive_limit.py](check_polynomial_primitive_limit.py)
constructs the quotient multiplication matrices by memoized reductions
and verifies their defining relations. Its seven systems cover a nonradical
quotient, a positive-dimensional original stationary set, finite limits
coexisting with escaping branches, two distinct finite limits, an empty
finite stationary limit set, a repeated finite limit, and a genuinely
algebraic optimizer. It independently
computes the coefficient derivatives through the adjugate recurrence and
compares one with direct determinant differentiation. It also checks the
divisibility rejection needed for a pole-hiding projection, a bad form
that yields a harmless feasible spurious point, and a joint objective-value
resultant. The algebraic optimizer fixture includes the endpoints and
every free-face candidate in its exact comparison.

Command actually run: `python3 -B
research-20261002/new-direction/check_polynomial_primitive_limit.py`.
Result: seven systems, nine forms, eight recovered finite limits, and ten
exact matrix relations passed. These small fixtures supplement the proof;
they are not an implementation or a complexity benchmark of the full solver.
No project-wide checks or CI inspection were run.
