# Every prime at least five occurs as the exact SOS coefficient-field degree

Date: 2026-09-28. Status: construction, quantitative proof, and retained
exact checks passed a fresh independent adversarial review.
Publication priority is not established.

For every odd prime \(p\geq5\), there is an integer quartic in
\(n=(p+1)/2\) variables with minimum zero, global Hessian bound
\(\nabla^2F\succeq I\), and an integer positive definite Hessian
Gram matrix. For every real subfield \(E\subseteq\mathbb R\),

\[
 \boxed{F\text{ is SOS over }E
 \quad\Longleftrightarrow\quad
 F\text{ has a PSD polynomial Gram over }E
\quad\Longleftrightarrow\quad 2^{1/p}\in E.}       \tag{1}
\]

Polynomial Gram matrices here use the full monomial basis of degree at
most two.

The polynomial has \(O(p^2)\) monomials and \(O(\log p)\)-bit
integer coefficients. Its integer Hessian Gram also has
\(O(\log p)\)-bit entries. Both can be constructed in time polynomial
in \(p\). This is a bound in the number of output variables, not in
the bit length of a binary encoding of \(p\).

Thus strict rational SOS-convexity permits an arbitrarily large necessary
algebraic field for an SOS or polynomial Gram certificate of the exact
minimum. The smallest real coefficient field is precisely
\(\mathbb Q(2^{1/p})\), and the smallest number-field degree is
\(p\). This extends the [small three-variable example](ternary-rational-sos-convex-counterexample.md).
It does not establish hardness of exact optimization or a lower bound
for other certificate systems.

## The point and a coefficient obstruction

Write

\[
 p=2s+1,\qquad n=s+1\geq3,\qquad a=2^{1/p},
 \qquad b=(a^s,a^{s+1},\ldots,a^{2s}).                \tag{2}
\]

Use variables \(x_0,\ldots,x_s\). All coordinates of \(b\)
lie between one and two. The coordinate field is \(K=\mathbb Q(a)\):
indeed \(a=2/b_s\). Eisenstein's criterion gives degree \(p\).

For a polynomial \(P\), define

\[
                \Lambda(P)=[x_s]P+[x_0^2]P.        \tag{3}
\]

Suppose a quadratic \(q\) vanishes at \(b\), its coefficients
belong to a real field \(E\), and \(T^p-2\) is irreducible over
\(E\). Write its constant coefficient as \(d\), its linear
coefficients as \(v_i\), and its coefficient on \(x_0^2\) as
\(h_{00}\). Reduce \(q(b)\) modulo \(a^p-2\). The coefficient
of \(a^{2s}\) is exactly

\[
                          v_s+h_{00}=0.             \tag{4}
\]

To see this, products of coordinates have exponents between \(2s\)
and \(4s\). The only one congruent to \(2s\) modulo \(2s+1\)
is \(b_0^2\). Among linear and constant monomials, only \(x_s\)
has that exponent. Irreducibility makes these coefficient comparisons
valid over \(E\).

Consequently

\[
 \Lambda(q^2)=v_0^2+2d(v_s+h_{00})=v_0^2.            \tag{5}
\]

Let \(S\) be the rational space of vanishing quadratics whose
linear coefficient on \(x_0\) is zero. Squares from \(S\) have
\(\Lambda\)-value zero. The unused vanishing quadratic

\[
                         r=x_1x_s-2x_0             \tag{6}
\]

satisfies \(\Lambda(r^2)=4\). We will construct a strictly
SOS-convex rational SOS from \(S\), then subtract this square while
retaining strict convexity.

## An explicit positive definite exposing quadratic inside the space

Define the rational quadratics

\[
\begin{aligned}
 P_0&=x_0^2-x_s,&
 P_1&=x_s^2-2x_{s-1},&
 P_2&=x_0x_1-2,\\
 P_{i+2}&=x_i^2-x_{i-1}x_{i+1}
                       &&(1\leq i\leq s-1).
\end{aligned}                                             \tag{7}
\]

Every \(P_j\) belongs to \(S\). The condition \(s\geq2\)
is used for \(P_1\): its linear term must not involve \(x_0\).
Consider the real linear combination

\[
 E_*=2aP_0+a^2P_1-2P_2
       +\sum_{i=1}^{s-1}a^{2s-2i+2}P_{i+2}.          \tag{8}
\]

It is a positive definite quadratic centered at \(b\). The following
factorization proves this and gives quantitative bounds.

Let \(G\) be the \(n\times n\) symmetric tridiagonal matrix,
indexed by \(0,\ldots,s\), with

\[
 G_{ii}=a^{2s-2i},\qquad
 G_{i,i+1}=G_{i+1,i}=\tfrac12 a^{2s-2i-1}.           \tag{9}
\]

Set

\[
 L(x)=(x_1-ax_0,\ldots,x_s-ax_{s-1},2-ax_s)^{\mathsf T}.
\]

Expansion, using \(a^{2s+1}=2\), gives

\[
                             E_*=L^{\mathsf T}GL.    \tag{10}
\]

For an additional check on the vanishing relations,

\[
 E_*(t^s,t^{s+1},\ldots,t^{2s})
       =(t^p-2)(a^2t^{p-2}-2).                       \tag{11}
\]

The latter identity can also be derived from
\(L(t^s,\ldots,t^{2s})=t^s(t-a)(1,t,\ldots,t^s)^{\mathsf T}
+(2-t^p)e_s\). It is not necessary to infer membership in a real
extension of a rational ideal: the explicit expression (8) already
places \(E_*\) in the real span of \(S\).

Write \(G=D_aTD_a\), where
\(D_a=\operatorname{diag}(a^s,a^{s-1},\ldots,1)\), and \(T\)
has diagonal one and adjacent entries \(1/2\). Its eigenvalues are
\(1+\cos(k\pi/(n+1))\), \(1\leq k\leq n\). Thus

\[
 \frac1{2n^2}I\preceq G\preceq4I.                  \tag{12}
\]

Here \(1-\cos(\pi/(n+1))\geq2/(n+1)^2\), and the entries
of \(D_a\) are between one and \(\sqrt2\). In centered
coordinates, \(L(b+u)=Bu\), with
\(B=-aI+U\), where \(U\) has ones on the upper adjacent diagonal.
The finite geometric series for \(B^{-1}\) gives
\(\|B^{-1}\|\leq n\), while \(\|B\|<3\). Consequently

\[
 E_*(b+u)=u^{\mathsf T}H_*u,
 \qquad \frac1{2n^4}I\preceq H_*\preceq36I.         \tag{13}
\]

Each \(P_j\) has quadratic-part norm at most one and gradient norm
at \(b\) at most eight. These bounds include the squared-coordinate
terms; no individual quadratic square is being assumed convex.

## Regular residual equations from the same restricted space

Use the \(n=s+1\) quadratics

\[
 R_0=x_0^2-x_s,\qquad R_1=x_0x_1-2,\qquad
 R_i=x_0x_i-x_1x_{i-1}\quad(2\leq i\leq s).         \tag{14}
\]

They all belong to \(S\). Their common real zero is \(b\):
\(R_1=0\) makes \(x_0\ne0\); setting \(t=x_1/x_0\), the
recurrences give \(x_i=x_0t^i\). Then \(R_0=0\) gives
\(x_0=t^s\), and \(R_1=0\) gives \(t^{2s+1}=2\).

The Jacobian is quantitatively nonsingular there. For a direction
\(u\), put \(h_i=u_i/b_i\). Divide the derivative rows by their
positive monomial values, which lie between one and four. The resulting
linear map is

\[
 \rho_0=2h_0-h_s,\qquad \rho_1=h_0+h_1,\qquad
 \rho_i=h_0+h_i-h_1-h_{i-1}\quad(2\leq i\leq s).
\]

If \(d=h_1-h_0\), then

\[
\begin{aligned}
 h_0&=\frac{\rho_0+s\rho_1+\sum_{i=2}^s\rho_i}{2s+1},\\
 d&=\frac{\rho_1-2\rho_0-2\sum_{i=2}^s\rho_i}{2s+1},\\
 h_i&=h_0+i d+\sum_{j=2}^i\rho_j.
\end{aligned}                                             \tag{15}
\]

The coefficient norms in the first two equations give
\(|h_0|\leq\|\rho\|\) and
\(|d|\leq\|\rho\|/\sqrt s\). Cauchy--Schwarz in the last
equation yields \(\|h\|\leq3n\|\rho\|\). Since the
coordinates of \(b\) are at most two, the Jacobian \(J\) satisfies

\[
                     \sigma_{\min}(J)\geq\frac1{6n}
                                      \geq\nu:=\frac1{8n}.  \tag{16}
\]

Every residual has quadratic-part norm at most one and gradient norm
at \(b\) at most eight.

## The integer output and its size

Choose

\[
 N=2^{20}n^8,\qquad \varepsilon=N^{-2},\qquad
                         D=64(n+1)N^2.             \tag{17}
\]

Approximate each of the \(n+1\) weights in (8) downward to the
grid \(D^{-1}\mathbb Z\), retaining the rational weight \(-2\)
exactly. Let \(A\) be \(D\) times the resulting quadratic.
Thus \(A\) has integer coefficients and belongs to \(S\).
The promised polynomial is the explicit expression

\[
 \boxed{F=A^2+(D/N)^2\sum_{i=0}^sR_i^2-r^2.}         \tag{18}
\]

The number \(D/N=64(n+1)N\) is an integer. All positive square
factors in (18) have zero linear coefficient on \(x_0\), and
every factor vanishes at \(b\). Therefore

\[
 F(b)=0,\quad \nabla F(b)=0,\quad \Lambda(F)=-4.     \tag{19}
\]

The weights in (8) have absolute value at most four. Hence each
coefficient of \(A\) is bounded by a polynomial in \(n\), since
\(D\) itself has polynomial magnitude. The expression for \(A\)
uses \(O(n)\) monomials. Equation (18) has \(O(n^2)\) monomials
and integer coefficients of polynomial magnitude, proving the claimed
\(O(\log n)\) bit bound.

The integer weights can be computed without an approximate equality
test. For a weight \(a^k=2^{k/p}\), find the largest integer \(z\)
such that \(z^p\leq 2^kD^p\). All exponents here satisfy
\(0\leq k\leq p+1\); the weight \(2a\) uses \(k=p+1\).
Binary search uses integers with \(O(p\log n)\) bits and
polynomially many bit operations. No expanded number-field computation
is required to construct \(F\).

## A quantitative full Hessian Gram proof

Write \(\bar A=A/D\). Equations (13), (17), and the bounds on
the \(P_j\) give

\[
 \bar A(b+u)=\ell^{\mathsf T}u+u^{\mathsf T}Hu,
 \quad \|\ell\|\leq\varepsilon/8,
 \quad mI\preceq H\preceq40I,
 \quad m:=\frac1{4n^4}.                              \tag{20}
\]

Indeed the coefficient approximation changes the gradient by at most
\(8(n+1)/D\) and the quadratic matrix by at most \((n+1)/D\).

Apply the [reviewed square-Gram lemma](sos-convex-quartic-realization.md)
to the rational SOS baseline

\[
                 G_0=\bar A^2+\varepsilon\sum_{i=0}^sR_i^2.
\]

Here \(L=40\), \(V=8\), and \(L+nV\leq24n\). The chosen
\(\varepsilon\) satisfies its three requirements

\[
 \varepsilon\leq1,\qquad
 \varepsilon\leq\frac{m^2}{2n},\qquad
 \varepsilon\leq\frac{\nu^2m^2}{36n(L+nV)^2}.       \tag{21}
\]

For the last inequality, the right side is at least
\(1/(21233664n^{13})\), whereas
\(\varepsilon=1/(2^{40}n^{16})\).

For clarity, the imported estimate applies to the entire Gram matrix
on \((v,u\otimes v)\), not just to its evaluations on such tensor
vectors. Its quadratic block is at least \(2m^2I\), its Schur
complement is at least \((3/2)\varepsilon\nu^2I\), and its
cross-block norm is at most \(6\sqrt n\varepsilon(L+nV)\).
The ratio of a convenient cross-block bound to \(2m^2\) is at most
\(1152n^{10}\varepsilon<1\). Completing the block square therefore
gives the following lower bound for the centered Gram \(M_0\):

\[
                         M_0\succeq\beta I,
 \qquad \beta:=\frac{\varepsilon}{256n^2}.           \tag{22}
\]

The canonical centered Gram \(M_r\) for the Hessian of \(r^2\)
has norm at most \(64n\). To check the estimate, its centered
gradient has norm less than four and its quadratic matrix has norm
\(1/2\) and squared Frobenius norm \(1/2\). The three Gram blocks
have norms bounded respectively by \(32\), \(12\sqrt n\), and
\(5\); their sum gives \(32+24\sqrt n+5\leq64n\).

It follows from (18) that a centered Hessian Gram for \(F\) satisfies

\[
 M_F=D^2M_0-M_r\succeq(D^2\beta-64n)I\succ I,
 \qquad D^2\beta=\frac{16(n+1)^2N^2}{n^2}.           \tag{23}
\]

Thus \(\nabla^2F\succeq I\) globally. Equations (19) and
strong convexity prove that the unique zero is \(b\), with
\(F(x)\geq\|x-b\|^2/2\).

## The canonical certificate is already integer

The final polynomial does not require rational approximation of an
algebraic Gram matrix. The square-Gram formula is exactly covariant
under translation.

For \(q(u)=d+b^{\mathsf T}u+u^{\mathsf T}Tu\), its canonical
Hessian Gram on \((v,u\otimes v)\) has blocks

\[
\begin{aligned}
 C&=2bb^{\mathsf T}+4dT,\\
 D(b,T)_{i,(k,j)}&=2b_kT_{ij}+4b_iT_{kj},\\
 Q(T)&=8\operatorname{vec}(T)\operatorname{vec}(T)^{\mathsf T}
                                      +4T\otimes T.
\end{aligned}                                             \tag{24}
\]

Let \(A_c=c\otimes I\). The identities

\[
\begin{aligned}
 A_c^{\mathsf T}Q(T)&=D(2Tc,T),\\
 A_c^{\mathsf T}Q(T)A_c
   &=8(Tc)(Tc)^{\mathsf T}+4(c^{\mathsf T}Tc)T,\\
 D(b,T)A_c+A_c^{\mathsf T}D(b,T)^{\mathsf T}
   &=4(b^{\mathsf T}c)T+4b(Tc)^{\mathsf T}+4(Tc)b^{\mathsf T}
\end{aligned}
\]

show that substituting \(u=x-c\) transforms (24), by the corresponding
Gram congruence, into the same formula with
\(b'=b-2Tc\) and \(d'=d-b^{\mathsf T}c+c^{\mathsf T}Tc\).
Linearity extends this fact to positive or negative linear combinations
of quadratic squares.

Apply this to (18). The positive definite centered Gram from (23)
transforms exactly into the canonical Gram computed from the integer
square factors at the rational center zero. For an integer quadratic,
\(d,b\) are integer and \(2T\) is integer. Each block in (24)
is consequently integer. The resulting original-coordinate Gram is
integer and positive definite, and its entry sizes are polynomial in
the coefficient magnitudes of the square factors. This proves the
claimed bit bound and provides a direct polynomial-time certificate
construction. Translation need not preserve the particular matrix
lower bound in (23); the global Hessian lower bound was already proved.
The positive definite quadratic block of the full Gram also makes the
leading quartic positive away from zero, by Euler's identity, so the
polynomial has degree exactly four.

This covariance observation simplifies this construction. The rational
affine-projection procedure in the cited general result remains valid;
no claim about arbitrary Gram parametrizations is being made.

## Proof of the exact coefficient-field characterization

Suppose \(E\subseteq\mathbb R\) and \(a\notin E\). Then
\(T^p-2\) is irreducible over \(E\). A proper monic factor of
degree \(j\), \(1\leq j<p\), would have constant coefficient
\((-1)^j a^j\zeta_p^k\). Its reality forces \(\zeta_p^k=1\),
because the only real \(p\)-th root of unity for odd \(p\) is one.
Thus \(a^j\in E\). Since \(p\) is prime, an integer Bézout
identity using \(a^p=2\) then gives \(a\in E\), a contradiction.

Any SOS representation of \(F\) over \(E\) would have quadratic
factors vanishing at \(b\). Equations (4)--(5) would imply
\(\Lambda(F)\geq0\), contradicting (19).

For a PSD polynomial Gram matrix, an additional argument avoids assuming
that PSD matrices factor over their coefficient field. Let \(m(x)\)
be the full vector of monomials of degree at most two, and suppose
\(F=m^{\mathsf T}Qm\), with \(Q\succeq0\) and entries in
\(E\). From \(F(b)=0\), positivity gives \(Qm(b)=0\).
Each row therefore defines a vanishing quadratic over \(E\), so (4)
implies, in particular,

\[
                         Q_{1,x_s}+Q_{1,x_0^2}=0.
\]

Here the subscripts identify monomials, and \(1\) means the constant
monomial. Extracting the two polynomial coefficients gives

\[
 \Lambda(F)=2Q_{1,x_s}+Q_{x_0,x_0}+2Q_{1,x_0^2}
           =Q_{x_0,x_0}\geq0,
\]

again a contradiction. This proves necessity for all PSD Gram ranks.

Conversely, a rational positive definite Hessian Gram can be factored
as a rational sum of squares by rational LDL decomposition and
four-square decompositions of its positive rational weights. Taylor
integration at \(b\in K^n\) then gives an SOS over \(K\).
Each squared Hessian factor becomes \(U(u)+tV(u)\), with
\(U,V\in K[u]\), and

\[
 \int_0^1(1-t)(U+tV)^2\,dt
       =2\bigl((U+V/3)/2\bigr)^2+(V/6)^2.            \tag{25}
\]

Thus neither factorization nor integration requires an extension beyond
\(K\). If \(a\in E\), this representation and its PSD polynomial
Gram are defined over \(E\). This completes (1).

## Consequences, prior results, and limits

Every real number field supporting either exact certificate contains
\(K\), so its degree is divisible by \(p\). A finite tower of
quadratic extensions cannot suffice. The same point and Hessian
certificate also give rational SOS certificates for \(F+\eta\),
for every positive rational \(\eta\), by the
[positive-constant lemma](rational-sos-convex-descent.md). Rational SOS
lower bounds have supremum zero but do not attain it.

Excluding an arbitrarily prescribed coefficient field is already possible
without convexity. In particular, Scheiderer's Corollary 2.11 constructs,
for any prescribed real number field, a rational nonnegative ternary
quartic form without an SOS over that field.
[Published primary source](https://ems.press/content/serial-article-files/32129).
Excluding one chosen field differs from forcing an unbounded minimum
field degree. The [least-field literature comparison](exponential-sos-field-prior.md)
deduces from Scheiderer's norm construction that its quartic examples
admit some real SOS field of degree at most 24. It also compares generic
SDP algebraic degrees, arithmetic constraints on every feasible point,
and the distinction between Gram fields and SOS fields.
The distinction here is the simultaneous global strong convexity,
integer full Hessian Gram, small integer coefficients, and exact
description of every real field supporting either an SOS or a PSD Gram.
The [prior comparison for three variables](three-variable-rational-sos-descent-prior.md)
records further relevant descent and point-ideal results. Publication
priority for the family requires a separate literature assessment.

The field degree grows linearly with the number of variables in this
construction. This is not a superpolynomial certificate-size lower bound;
the necessary field itself has a short radical description. The result
concerns polynomial SOS and polynomial Gram certificates of the attained
value. It does not exclude rational certificates with denominators or
multipliers, alternative exact proof systems, or efficient approximate
optimization. A possible use is to test exact reconstruction procedures
and certificate formats against arithmetic requirements that persist
despite strict convexity and small integer input.

## Verification record

The symbolic construction, coefficient functional, Jacobian estimate,
Gram bounds, and translation covariance were checked independently by
the parent investigator. A [fresh adversarial review](arbitrary-prime-strict-sos-field-review.md)
by an agent uninvolved in the construction checked the universal proof,
all quantitative estimates, exact SOS and PSD Gram field characterization,
and construction complexity. It found no unresolved gap and independently
reran the retained checker. The author read that completed review; its
scope and conclusions agree with the proof above. A positive review is
evidence of correctness, not formal verification.

The retained [exact checker](check_arbitrary_prime_strict_sos_field.py)
was run with

```text
python research-20260927/check_arbitrary_prime_strict_sos_field.py
```

It passed the following targeted checks:

- A generic two-variable symbolic identity for the canonical Gram under
  translation. The dimension-independent identities are proved in (24).
- All displayed regularization and perturbation inequalities for
  \(n=3,\ldots,80\). These finite cases supplement the universal
  estimates in (20)--(23).
- For \(p=5,7\), exact construction of the integer weights and
  polynomial, identities (10)--(11), the scaled Jacobian factorization
  with determinant \(p\), algebraic zero and stationarity, and
  \(\Lambda(F)=-4\).
- For those same two primes, construction of the integer original-coordinate
  Hessian Gram, the fully differentiated polynomial identity, and an
  exact positive-pivot LDL factorization of that Gram minus the identity.

The resulting metadata were

| Prime | Variables | Monomials | Maximum coefficient bits | Maximum Gram-entry bits |
| --- | --- | --- | --- | --- |
| 5 | 3 | 31 | 152 | 153 |
| 7 | 4 | 50 | 165 | 167 |

The uniform constants deliberately give larger coefficients than the
separate small quintic example. The checker uses no numerical eigenvalue
or SDP calculation. It establishes the stated identities and signs for
the tested outputs; the arbitrary-prime, coefficient-size, and field
classification results use the universal proofs above.

Exploratory exact SymPy calculations verified (10)--(11) for
\(p=5,7,11,13\). The first attempt used a nonexistent `Poly.applyfunc`
method and did not complete; replacing it by polynomial remainder in
\(a\) gave passing checks. Those finite identities supplement the
universal algebra above. No project-wide verification or CI inspection
was performed.

Targeted inline Python checks passed the relative links, mathematical
delimiters, final newlines, trailing whitespace, and control characters
of this note, with the applicable text checks also applied to the retained
checker. The targeted `git diff --check --` command for those two files
returned no diagnostics. No Lean verification was used.
