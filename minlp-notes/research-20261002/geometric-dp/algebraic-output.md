# Exact algebraic output can be large even on a uniformly conditioned path

Date: 2026-10-02. Status: elementary construction checked by a fresh
independent mathematical reviewer. This is an output-format limitation,
not a point-oracle lower bound or a literature priority claim.

Bounded polynomial degree, path structure, and uniform conditioning do not
guarantee a short expanded algebraic representation of an exact optimizer.
The degree-four family below has a unique optimizer and uniform constants
for the [geometric-grid theorem](theorem.md), but the first optimizer
coordinate has an irreducible polynomial of exponential degree with
exponentially many nonzero coefficients. Exact output in a dense polynomial
format, or as an expanded sparse minimal polynomial, therefore takes
superpolynomial time merely to write.

This limitation depends on the output format. The same optimizer has a
short nested-square-root representation, and its exact objective value is
zero. The example does not rule out efficient exact algorithms using
compact symbolic outputs.

## 1. A degree-four path family

For \(n\ge2\), take \(X=[1,2]^n\) and

\[
F_n(x)=\sum_{i=1}^{n-1}(x_i^2-x_{i+1}-2)^2+(x_n-1)^2.
\tag{1}
\]

There are \(n\) constant-size factors, each with rational coefficients
of bounded bit length and total degree at most four. The interaction graph
is a path, with bags \(\{i,i+1\}\) and width one. The coefficient data
have \(O(n)\) bits; an ordinary factor list with binary variable indices
has \(O(n\log n)\) total encoding length.

Define

\[
a_n=1,\qquad a_i=\sqrt{a_{i+1}+2}\quad(i=n-1,\ldots,1),
\tag{2}
\]

using the positive square root. These values belong to \([1,2]\).
Every summand in (1) vanishes at \(a\), so \(F_n(a)=0\).
Conversely, a zero objective forces the terminal coordinate to be one and
then forces (2) successively. Thus \(a\) is the unique global optimizer.
The last coordinate is a boundary optimizer, which the grid theorem allows.

## 2. Uniform global growth and curvature

For any \(x\in X\), put \(e=x-a\) and let \(r\) be the residual
vector in (1):

\[
r_i=(x_i+a_i)e_i-e_{i+1}\quad(i<n),\qquad r_n=e_n.
\]

Let \(D\) be diagonal, with entries \(x_i+a_i\) for \(i<n\) and
last entry one. Let \(S\) have ones on its first superdiagonal and zero
elsewhere. Then

\[
r=D(I-P)e,\qquad P=D^{-1}S.
\]

Since \(x_i+a_i\ge2\), the weighted shift satisfies
\(\|P\|_2\le1/2\), while \(\|D^{-1}\|_2=1\).
The finite Neumann series for the nilpotent matrix \(P\) gives

\[
\|e\|_2
\le\|(I-P)^{-1}\|_2\|D^{-1}\|_2\|r\|_2
\le2\|r\|_2.
\]

Consequently the global quadratic-growth inequality holds with the
dimension-independent rational constant

\[
F_n(x)-F_n(a)=\|r\|_2^2\ge\tfrac14\|x-a\|_2^2.
\tag{3}
\]

For \(i<n\), the second derivative contributed by its outgoing factor is
\(12x_i^2-4x_{i+1}-8\), at most 36 on the box. An interior coordinate
has an additional second derivative of two from the preceding factor.
The terminal coordinate has total second derivative four. Thus

\[
\partial_{ii}F_n(x)\le38\qquad(x\in X)
\tag{4}
\]

for every coordinate and every dimension. This is the upper coordinate
curvature required by the grid theorem. Taking \(L=38\) and \(c=1/4\)
gives the uniform ratio \(L/c=152\).

## 3. Exponential algebraic degree and polynomial support

Put \(f(t)=t^2-2\), \(k=n-1\), and

\[
P_k(t)=f^{\circ k}(t)-1,
\qquad m=2^k.
\tag{5}
\]

The chain (2) gives \(P_k(a_1)=0\). The polynomial has degree \(m\).
It is irreducible over \(\mathbb Q\), as follows from Eisenstein's
criterion after translation.

Modulo two, \(f(t)\equiv t^2\), so

\[
P_k(t+1)\equiv(t+1)^{2^k}-1\equiv t^{2^k}\pmod2.
\]

Its leading coefficient is one. All other coefficients are divisible by
two. Its constant coefficient is exactly minus two, because
\(f(1)=-1\) and \(f(-1)=-1\), hence
\(P_k(1)=-2\) for every \(k\ge1\). Eisenstein's criterion at the
prime two proves irreducibility of \(P_k(t+1)\). Translation preserves
irreducibility, so \(P_k\) is the minimal polynomial of \(a_1\).
In particular,

\[
[\mathbb Q(a_1):\mathbb Q]=2^{n-1}.
\tag{6}
\]

The minimal polynomial also has many nonzero coefficients; it is not a
two-term polynomial hidden behind binary exponents. The iterate
\(f^{\circ k}\) has a nonzero coefficient at every even power from
\(t^m\) down to its constant term, with alternating signs in that order.
This follows by induction. It holds for \(t^2-2\). Squaring an iterate
preserves this alternating pattern because every contribution to a given
power has the same sign. Its squared constant term is four; subtracting
two leaves the nonzero constant two. The first iterate has constant minus
two, and every later iterate has constant two.

Subtracting one in (5) therefore leaves constant minus three when
\(k=1\), and constant one when \(k\ge2\). No coefficient vanishes.
Thus \(P_k\) has exactly

\[
m/2+1=2^{n-2}+1
\tag{7}
\]

nonzero monomials. For example, the first three minimal polynomials are
\(t^2-3\), \(t^4-4t^2+1\), and
\(t^8-8t^6+20t^4-16t^2+1\).

## 4. What the output lower bound does and does not say

Two output conventions have an immediate size obstruction:

- Any nonzero rational defining polynomial for \(a_1\) has degree at
  least \(2^{n-1}\). A dense coefficient vector for such a polynomial
  therefore has exponentially many entries, even if the polynomial is
  not minimal.
- An expanded monomial-list representation of the minimal polynomial has
  \(2^{n-2}+1\) nonzero terms. Allowing binary exponents in this list
  does not make the output polynomial in the input length.

Adding a root-isolating interval does not remove the mandatory polynomial
output. These bounds are exponential in \(n\) and superpolynomial in
the ordinary \(O(n\log n)\)-bit indexed input encoding. They rule out
a polynomial total runtime for algorithms required to produce these
particular exact optimizer representations.

The support argument concerns the minimal polynomial. It does not by
itself rule out a sparse higher-degree polynomial having the same root.
Nor does it apply to polynomial arithmetic circuits: (5) has an
\(O(n)\)-size repeated-squaring circuit. Equation (2) is an
\(O(n)\)-size radical circuit describing the entire optimizer with shared
subexpressions, and the factor equations themselves form a compact
triangular algebraic representation.

The optimum value is the rational number zero. Nonnegativity of the
squares and (2) give a short symbolic optimality certificate. Thus this is
not a lower bound for exact value computation, all exact certification,
or unrestricted symbolic exact optimization.

The distinction nevertheless matters when extending an exact algorithm
from rational quadratic data to higher-degree polynomial data. This
family satisfies fixed width, bounded degree, and uniform conditioning,
so the rational-polynomial approximation theorem gives polynomial runtime
in the input size and \(\log(1/\varepsilon)\) for certified approximate
solutions. An exact extension required to output dense defining polynomials
or expanded minimal polynomials cannot have the same kind of bound. A
compact exact output format would require a separate algorithm and
complexity analysis.

## 5. Why algebraic degree alone was not enough

The simpler chain on \([1/2,1]^n\),

\[
\sum_{i<n}(x_i^2-x_{i+1})^2+(x_n-1/2)^2,
\]

also has uniform conditioning and first-coordinate degree \(2^{n-1}\).
Its monic minimal polynomial is only \(t^{2^{n-1}}-1/2\), which is short
as a sparse polynomial with a binary exponent. That example suffices for a
dense-output warning but not for a sparse-minimal-polynomial warning.
The constant shift inside each residual in (1) gives the stronger support
statement (7) without relying on degree alone.

## 6. Verification status

The construction, growth estimate, curvature bound, irreducibility proof,
coefficient-support induction, and output-format qualifications received a
fresh independent mathematical review. The reviewer identified a broad
summary phrase and a minor minimal-polynomial normalization issue; both
were corrected. This is internal mathematical review, not external peer
review or a priority assessment. No executable checks, external literature
search, project-wide verification, or CI inspection were used.
