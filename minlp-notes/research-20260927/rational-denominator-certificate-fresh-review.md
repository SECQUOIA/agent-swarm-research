# Fresh review of the rational denominator certificate

Date: 2026-09-28. Verdict: the exact certificate passes independent review.
For the specified polynomial, the minimum total degree of a polynomial
common denominator in a rational-function SOS over \(\mathbb Q\) is exactly
two. The denominator \(R=1+x^2+y^2+z^2\) works and is positive everywhere.
This is a sharp certificate benchmark; this review makes no publication
priority claim.

The reviewed artifact is
[the quadratic-multiplier checker](check_ternary_rational_sos_quadratic_multiplier.py),
with SHA-256
`0fb76cb892fbc05c963fbad4764b0c8e383ef15838e36cf9216949789d0df4af`.
It defines \(r_0=2-2xy\), \(r_1=2x^2-2yz\),
\(r_2=2y^2-4z\), \(r_3=2z^2-x\), \(r_4=2xz-y\),
\(A=4r_0+5r_1+3r_2+9r_3\), and
\(F=A^2+\sum_{i=0}^3r_i^2-r_4^2\).
The earlier strong-convexity and unique-zero claims are outside this
review's verification scope. The denominator proof below needs only the
displayed \(F\), its zero at \(p=(a^4/2,a,a^2/2)\), where
\(a=2^{1/5}\), and its failure of polynomial SOS over \(\mathbb Q\).

I reconstructed \(F\), \(R\), and the fifteen basis polynomials independently
using sparse polynomial dictionaries and Python `Fraction` arithmetic.
Only the integer matrix \(N\) was read from the checker, through its syntax
tree; the independent calculation did not import or execute its definitions
of \(F\), its basis, or its verification routines. It obtained exactly

\[
                         b^{\mathsf T}Nb=8RF.
\]

The basis order agrees with the checker:

\[
\begin{aligned}
b=(&z^2-x/2,\ y^2-2z,\ xz-y/2,\ xy-1,\ x^2-yz,\\
   &z^3-y/4,\ yz^2-1/2,\ y^2z-x,\ y^3-2yz,\\
   &xz^2-yz/2,\ xyz-z,\ xy^2-y,\ x^2z-1/2,\ x^2y-x,\ x^3-z)^{\mathsf T}.
\end{aligned}
\]

The reconstructed \(F\) has degree four, 31 nonzero monomials, and maximum
absolute coefficient 448. The product \(RF\) has degree six and 78 nonzero
monomials. The first five entries of \(b\) have degree two; the remaining
ten have degree three. The largest absolute entry of \(N\) is 4240, and
the largest reduced denominator of an entry of the Gram matrix \(N/8\)
is exactly eight. The basis itself uses only denominators two and four.

To check strict positivity independently of the checker's rational LDL
factorization, I computed all leading principal determinants of \(N-8I\)
using fraction-free Bareiss elimination over the integers. Every exact
division was checked. In order, the determinants are

```text
4232
2041407
5839006240
5263436936513
8309698919905512
11480475166599386752
24140997007816543732224
9072065142124268516803584
1221674797258437785568657408
1569452470480427736351156994048
1967046692952416690050593546305536
844438887950283618215158211684597760
196739716166438745148196850208516079616
21440610749731697832005735132127356256256
497197930466744687768853864373192977547264
```

The matrix is symmetric. Sylvester's criterion therefore proves
\(N-8I\succ0\), and hence \(N/8\succ I\). This checks a strict rational
Gram certificate, with no floating-point tolerance.

I also checked the basis separately in \(\mathbb Q[a]/(a^5-2)\). A monomial
\(x^iy^jz^k\) evaluates to
\(2^{\lfloor(4i+j+2k)/5\rfloor-i-k}a^{(4i+j+2k)\bmod5}\).
All fifteen basis elements evaluate to zero. The evaluation matrix on
the twenty monomials of total degree at most three has rank five, and
the coefficient matrix of \(b\) has rank fifteen. Thus \(b\) is precisely
a basis of the rational space \(I_3\) of cubic-or-lower polynomials
vanishing at \(p\). This rank claim is not needed for the identity to be
an SOS certificate, but it is correct as stated.

A positive definite rational Gram matrix gives a sum of rational polynomial
squares. In detail, rational LDL factorization of \(N/8\) writes
\(RF=\sum_{i=1}^{15}d_i h_i^2\), where \(d_i\in\mathbb Q_{>0}\)
and \(h_i\in\mathbb Q[x,y,z]\) have degree at most three. For
\(d_i=p_i/q_i\), with positive integers \(p_i,q_i\), the four-square
theorem writes \(p_iq_i=\sum_{j=1}^4e_{ij}^2\). Therefore
\(d_i=\sum_{j=1}^4(e_{ij}/q_i)^2\). Absorbing these rational factors
gives \(RF=\sum_{k=1}^{m}q_k^2\) with \(m\le60\) and
\(\deg q_k\le3\). The rank-fifteen Gram matrix alone does not assert
an unweighted decomposition into fifteen rational squares.

Multiplying this identity by \(R=1^2+x^2+y^2+z^2\) gives

\[
 R^2F=\sum_{k=1}^{m}
       \bigl(q_k^2+(xq_k)^2+(yq_k)^2+(zq_k)^2\bigr).
\]

Consequently

\[
 F=\sum_{k=1}^{m}\left[
       \left(\frac{q_k}{R}\right)^2+
       \left(\frac{xq_k}{R}\right)^2+
       \left(\frac{yq_k}{R}\right)^2+
       \left(\frac{zq_k}{R}\right)^2\right].
\]

This is an SOS of at most 240 rational functions with coefficients in
\(\mathbb Q\), a common denominator of total degree two, and numerators
of total degree at most four. Since \(R\ge1\), every displayed rational
function is defined on all of \(\mathbb R^3\). The squared denominator
\(R^2\) has degree four, and \(R^2F\) has degree eight. These degrees
must be distinguished from the degree-two SOS multiplier \(R\): the
identity for \(RF\) by itself would give denominator \(\sqrt R\), which
is not the rational denominator being certified here. No minimum number
of squares is claimed.

For the lower bound, I independently checked the existing obstruction
to polynomial SOS over \(\mathbb Q\). Evaluation of the ten monomials
of degree at most two at \(p\) has rank five, and the five \(r_i\)
are independent and vanish at \(p\). They therefore form a basis of
the rational quadratic vanishing space. For
\(\Lambda(P)=2[z]P+4[y^2]P\), direct rational multiplication gives

\[
 \Lambda(r_ir_j)=4\,\mathbf 1_{i=j=4},
 \qquad \Lambda(F)=-4.
\]

In any polynomial SOS of the quartic \(F\), summands have degree at most
two because highest-degree real squares cannot cancel. Evaluation at
the real zero \(p\) forces every summand to vanish there. Thus a
rational polynomial SOS would give \(\Lambda(F)\ge0\), a contradiction.
The rank calculation uses the irreducibility of \(T^5-2\), which follows
from Eisenstein's criterion at two.

Now suppose \(F=\sum_j(u_j/d)^2\), with
\(u_j,d\in\mathbb Q[x,y,z]\), \(d\ne0\), and \(\deg d\le1\).
If \(d\) is constant, this is already a rational polynomial SOS.
Otherwise \(d\) is a nonconstant affine polynomial, whose real zero
set is a nonempty affine hyperplane. Clearing denominators gives the
polynomial identity \(d^2F=\sum_j u_j^2\). On that hyperplane the
left side vanishes, so every \(u_j\) vanishes there. Choose a variable
whose coefficient in \(d\) is nonzero. Division by \(d\) in that
variable leaves a remainder in the other two variables with rational
coefficients. The remainder vanishes at every real point of
\(\mathbb R^2\), so it is the zero polynomial. Hence \(d\) divides
every \(u_j\) over \(\mathbb Q\). Cancelling \(d^2\) again gives
a rational polynomial SOS for \(F\), a contradiction. This proves
minimality even if a proposed rational-function representation is
initially interpreted only away from its denominator's zeros. A
positive rational weighted SOS obeys the same argument.

The finite certificate consists of rational polynomial data, the integer
matrix, the coefficient identity, and positive integer determinants.
These give exact, finitely checkable evidence for the asserted rational
Gram representation. Rational LDL and the four-square theorem then
give the claimed rational-square representation with a finite explicit
bound on its number of summands. The checker does not print expanded
rational square factors, and this review does not claim that it does.
No numerical SDP output is required to verify the artifact.

The targeted commands actually run were
`python3 /tmp/degree_two_denominator_fresh_audit.py` (the independent
sparse-`Fraction`, quotient-field rank, obstruction, and integer-Bareiss
checks), `python3 research-20260927/check_ternary_rational_sos_quadratic_multiplier.py`
(the frozen checker), and
`sha256sum research-20260927/check_ternary_rational_sos_quadratic_multiplier.py`.
All passed. The independent temporary script was run again after adding
the quadratic obstruction check. No project-wide checks were run, and
CI status and logs were not inspected.
