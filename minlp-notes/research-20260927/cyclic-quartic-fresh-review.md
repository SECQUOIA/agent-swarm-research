# Fresh review of the cyclic quartic construction

Date: 2026-09-28. Scope: an independent adversarial proof and cost audit of
[the cyclic construction](cyclic-quartic-exponential-degree.md), including
its import from [the rational Hessian certificate construction](sos-convex-quartic-realization.md).

No blocking mathematical defect was found. The construction establishes
the stated exponential degree, integer SOS quartic, global Hessian bound,
small coefficient sizes, and polynomial-time rational Hessian certificate.
The distinction between the number of variables and the number of
residuals is handled correctly. The output obstruction applies to the
specified minimal-polynomial coefficient-list formats; it does not apply
to all exact algebraic representations. Growth is exponential in the
dimension $n$, which should remain explicit when stating the output
consequence. This review does not establish publication priority, verify
the bibliographic comparisons, or audit the separate general upper bounds
on algebraic degree.

The draft uses $m=n+1$, $\sigma=(-1)^m$,
$d=(2^m-\sigma)/3$, $s_i=((-2)^i-1)/3$, and $p_i=2^{s_i/d}$.
The integer $d$ is positive and odd. The recurrence
$2s_i=s_{i+1}+s_{i+2}$ follows directly from the formula for $s_i$.
Before wrapping, $s_m=\sigma d$ and $s_{m+1}=-2\sigma d-1$.
Consequently the two wrap corrections are respectively $\sigma d$ and
$-\sigma d$, exactly as required by the two exceptional coefficients
in the residuals. The inequalities $|s_i|<d$ hold for $0\leq i<m$,
including the smallest case $n=2$.

Writing $a=2^{1/d}$ gives $p_1=a^{-1}$ and expresses every other
coordinate as an integer power of $a$. Eisenstein irreducibility of
$T^d-2$ therefore gives the exact field degree $d$, rather than merely
an upper bound. Since $d$ is odd, this particular polynomial has exactly
one real root. Odd degree by itself would not imply that property for a
general polynomial; here the explicit binomial does.

For the exposing quadratic, the normalization $X_i=x_i/p_i$ turns
$p_i^{-2}q_i$ into $X_i^2-X_{i+1}X_{i+2}$. Summing over the cycle gives

\[
 \sum_i p_i^{-2}q_i(x)
 =\frac12\sum_i(X_i-X_{i+1})^2.
\]

The condition $X_0=1$ forces every zero of this energy to be the stated
point. This proves uniqueness of the common real zero independently of
the later convexity argument. In particular, the proof does not silently
restrict to positive solutions of the binomial system.

For a vector $h$ with $h_0=0$, telescoping along the anchored path and
Cauchy--Schwarz give
$\|h\|^2\leq n^2\sum_i(h_i-h_{i+1})^2$. The difference operator has
norm at most two. Together with $1/2<p_i<2$, these inequalities give

\[
 \frac1{8n^2}I\preceq H_*\preceq8I
\]

with the factor $1/2$ in the energy included. There is no Hessian versus
quadratic-matrix factor error here: the Hessian of the energy is $2H_*$.

The homogeneous quadratic matrix $T_i$ consists of a diagonal entry
one and a disjoint off-diagonal block of norm at most one, with entries
removed when the fixed variable $x_0$ occurs. The three cyclic indices
are distinct even when $m=3$. Thus $\|T_i\|_2\leq1$. Each residual
gradient has at most three nonzero entries, each of absolute value less
than four, so $\|b_i\|_2<4\sqrt3<7<8$.

The full residual Jacobian is

\[
 J=\operatorname{diag}(p_i^2)(2I-S-S^2)ED_p^{-1}.
\]

The factorization $(2I+S)(I-S)$ is exact, and
$\|(2I+S)z\|\geq\|z\|$ follows from the reverse triangle
inequality and orthogonality of $S$. Applying the anchored path estimate
then gives the lower singular-value bound $1/(8n)$. This argument uses
all $m$ rows and does not assume that deleting one residual preserves
the same bound.

The grounded determinant assertion also has a direct derivation. The
nonzero eigenvalues of $2I-S-S^2$ are
$(2+\omega^j)(1-\omega^j)$ for $1\leq j<m$. Their product divided
by $m$ is any principal grounded cofactor, since both nullspaces are
spanned by the all-ones vector. Now
$\prod_{j=1}^{m-1}(1-\omega^j)=m$ and
$\prod_{j=1}^{m-1}(2+\omega^j)=(2^m-(-1)^m)/3$. The cofactor is
therefore $d$. This algebraic verification does not settle a source's
rooted-tree counting convention.

The weight errors $|z_i/Q-p_i^{-2}|\leq1/Q$ give
$\|\ell\|\leq8m/Q=\varepsilon/4$ and
$\|H-H_*\|\leq m/Q=\varepsilon/32$. Hence the claimed
$\mu I\preceq H\preceq LI$, with $\mu=1/(16n^2)$ and $L=9$,
holds. Every residual still vanishes exactly at $p$: rounding occurs
only in a linear combination of rational polynomials already vanishing
there. No approximate root is substituted into the output polynomial.

The integer scaling is exact. Each $2q_i$ is integral,
$A=2\sum_i z_iq_i$ is integral, and
$2Q/M=64mM$ is an even integer. Thus the displayed $m+1=n+2$
square factors are integer quadratics and their sum of squares is
$4Q^2\Phi$.

The cubic Hessian bound
$12\|b\|\|T\|\|u\|$ follows by differentiating
$2(b^{\mathsf T}u)(u^{\mathsf T}Tu)$: its three matrix terms have
norm bounds $4\|b\|\|T\|\|u\|$ each. Summing gives the claimed
$12\varepsilon D\|u\|$ with $D=L+8m$. The quartic Hessian lower
bound retains the contribution
$-4\varepsilon m\|u\|^2I$ from the possibly indefinite $T_i$.
The draft does not incorrectly assume their squares are convex.

All three parameter inequalities hold. In particular,

\[
 \frac{\nu^2\mu^2}{36nD^2}
 =\frac1{589824n^7D^2}
 \geq\frac1{170459136n^9}
 \geq\frac1{10^{12}n^{10}}=\varepsilon.
\]

Completing the scalar square subtracts exactly
$18\varepsilon^2D^2/\mu^2$. The resulting lower bound
$(3/2)\varepsilon\nu^2 I$ is conservative and valid. After scaling,
it becomes $96m^2M^2/n^2 I$, which exceeds $I$.

The imported Hessian Gram identity remains valid with $m=n+1$
residuals. In that identity the number of variables determines the
$n\times n^2$ cross block and its Frobenius estimate
$6\sqrt n\,\|b\|\|T\|$. The number of residuals appears only
when summing their contributions. Thus the correct bounds are

\[
 C\succeq2\varepsilon\nu^2I,\qquad
 R\succeq(4\mu^2-4\varepsilon m)I\succeq2\mu^2I,
 \qquad \|B\|\leq6\sqrt n\,\varepsilon(L+8m).
\]

These are the bounds used in the cyclic draft. The Schur-complement
subtraction is $18n\varepsilon^2D^2/\mu^2$, so its extra factor
is the dimension $n$, not the residual count $m$. The last parameter
inequality was chosen correctly to retain a positive Schur complement.

One can make the polynomial conditioning claim explicit. Let

\[
 q=2\mu^2=\frac1{128n^4},\qquad
 s=\frac32\varepsilon\nu^2=\frac3{128M^2n^2},\qquad
 B_0=6n\varepsilon D.
\]

Then $s\leq q$ and
$B_0/q\leq13056\varepsilon n^6<1$. The block-square bound in the
imported argument gives a Gram eigenvalue at least $s/4$ before
translation. Using the rational bound $\|p\|\leq2n$, the inverse
translation matrix has norm at most $2+2n\leq3n$. Consequently the
unscaled Hessian biform in the original coordinates has a Gram matrix
with the explicit bound

\[
 M_x\succeq\beta I,\qquad
 \beta:=\frac1{1536M^2n^4}.
\]

Its matrix order is $N=n+n^2$. Approximating it in Frobenius norm
within $\beta/4$ and applying the imported coefficient projection
therefore gives an exact rational positive definite Gram matrix.
That projection is valid because each ordered matrix entry belongs to
exactly one coefficient constraint; the coefficient matrices have
disjoint supports. It is an orthogonal affine projection and cannot
increase the error from an exact Gram matrix. In particular, arbitrarily
large condition numbers for a general rational linear system are not
being ignored.

The entries of $M_x$ are polynomial expressions of degree at most two
in $p$. Their rational coefficients and their number are bounded by
polynomials in $n$: $H,T_i$ are fixed rational matrices, the translated
gradients are affine functions of $p$, and the translation matrix is
affine in $p$. Since $|p_i|<2$ and $\beta^{-1}$ is polynomial in
$n$, inverse-polynomial coordinate accuracy suffices. The exact
rational Gram matrix has polynomial size and can be verified in
polynomial bit time by exact rational elimination. No SDP oracle or
dense degree-$d$ algebraic-number representation is needed.

The approximation procedure also has the stated cost. The tail of the
logarithm series has the stronger bound

\[
 0<\log2-L_N
 <\frac{3}{4(2N+1)}9^{-N}<9^{-N}.
\]

Multiplication by $-2s_i/d$ increases the error by less than two.
Both exponential arguments remain in $[-2,2]$, where the derivative
is less than nine. The choice $9^N\geq256Q$ therefore gives an
exponential-value error below $1/(8Q)$ from this source. For $K\geq2$,
the ratio between consecutive absolute Taylor-tail terms is at most
$2/(K+2)\leq1/2$, proving the bound
$2^{K+2}/(K+1)!$. Adding a tail error at most $1/(8Q)$ and rounding
the rational approximation times $Q$ gives an error at most
$3/(4Q)<1/Q$. Ties can be resolved using rational arithmetic; no
comparison against an exact transcendental or algebraic rounding
boundary occurs.

The required $N$ and $K$ are $O(\log Q)=O(\log(n+1))$.
Although $d$ is exponentially large as a value, $d$ and $s_i$ have
$O(n)$ bits. For example, a common denominator for the truncated
exponential series is the argument denominator to the $K$th power
times $K!$. Its bit length is polynomial in $n$. Thus exact rational
evaluation of these finite series is a polynomial-time procedure.
The same reasoning applies to approximating the coordinates for the
Gram construction.

Finally, $|z_i|\leq4Q+1$, while $M$ and $Q$ have polynomial
magnitude. The main square factor has at most $2m$ terms; squaring it
and adding $m$ two-term residual squares gives $O(n^2)$ monomials.
Even the coarse bound obtained by summing the magnitudes of all
contributing products is polynomial in $n$. This establishes the
$O(\log(n+1))$ coefficient-bit bound for the output and its square
factors. Exponent vectors and monomial indexing require only polynomial
space and do not change the construction-time conclusion.

The original first coordinate has sparse primitive minimal polynomial
$2T^d-1$. Translating that coordinate by one gives the primitive
irreducible polynomial $2(T-1)^d-1$. Its constant coefficient is $-3$
and all other coefficients are signed twice a nonzero binomial
coefficient, so its ordinary monomial list has exactly $d+1$ terms.
The quartic translation costs only a constant factor in term count and
preserves integer SOS structure and the Hessian bound. This yields a
lower bound for dense output, and for ordinary sparse output of this
coordinate's minimal polynomial. It yields no corresponding lower bound
for a sparse polynomial describing an auxiliary primitive element with
rational coordinate maps, a shifted polynomial representation, a
circuit, or a rational-power expression. The draft's explicit
representation restrictions are therefore necessary and correct.

The subsequently added local conditioning estimate is valid. At the
common zero the Hessian is
$2\ell\ell^{\mathsf T}+2\varepsilon J^{\mathsf T}J$.
Its smallest eigenvalue is at least $2\varepsilon\nu^2$, and its
largest is at most $2\varepsilon(\varepsilon+64m)$.
Since $\varepsilon\leq1$, the stated condition-number bound
$(1+64m)/\nu^2=O(n^3)$ follows. The claim is restricted correctly to
the minimizer.

The supporting formulation by $n+1$ full-dimensional rational
ellipsoids also passes. For $\tau=\mu/2$, $c_i=z_i/Q$,
$C=\sum_i c_i$, $W=\sum_iw_i$, and $R_i=G+\tau q_i$, the
quadratic matrix of $R_i$ is at least $(\mu/2)I$. The proposed weights

\[
 \lambda_i=\frac1\tau\left(w_i-\frac{Wc_i}{\tau+C}\right)
\]

satisfy $\sum_i\lambda_i=W/(\tau+C)$ and
$\tau\lambda_i+c_i\sum_j\lambda_j=w_i$. Hence their weighted
sum of the $R_i$ is exactly $G_*$. Also $c_i>0$, and

\[
 \tau(\tau+C)\lambda_i
 =\tau w_i+w_i(C-W)-W(c_i-w_i)
 \geq\frac\tau4-\frac{8m}{Q}>0.
\]

The positive combination proves that the intersection of the sublevels
is precisely $\{p\}$. Each $R_i$ has a rational unique minimizer
because its rational quadratic matrix is positive definite. That
minimizer cannot equal the irrational point $p$, so its minimum is
strictly below $R_i(p)=0$. Each individual sublevel is therefore a
bounded full-dimensional ellipsoid. Multiplication by the common
positive denominator $64n^2Q$ makes every $R_i$ integral, with
$O(\log(n+1))$ coefficient bits. The real coefficients $\lambda_i$
serve in the proof and are not asserted to be rational input data.

The failed repeated-squaring-chain argument is also correct under its
stated restriction $n\geq3$. Among sums of two elements of
$\{0,1,2,4,\ldots,2^{n-1}\}$, none is $2^n-1$. Reduction modulo
$T^{2^n-1}-2$ therefore gives no constant contribution from a
nonconstant quadratic monomial, forcing every rational quadratic
relation to have zero constant coefficient. At $n=2$, the sum
$1+2=3$ invalidates that argument, as the draft records.

The targeted command
`python research-20260927/check_cyclic_quartic_exponential_degree.py`
passed. It checks parameter bounds for $n=2,\ldots,80$, exact cyclic,
Jacobian and energy identities for $n=2,\ldots,12$, and certified
integer output for $n=2,\ldots,6$. Its output rows
$(n,d,\text{monomials},\text{maximum coefficient bits})$ were
$(2,3,15,118)$, $(3,5,31,131)$, $(4,11,50,139)$,
$(5,21,72,146)$, and $(6,43,98,151)$.

An additional targeted `python - <<'PY'` check independently constructed
the actual $n=2$ rational Hessian certificate. It used 120 rational
bisection steps for $2^{1/3}$, formed the translated block Gram matrix,
rounded its entries to denominator $2^{100}$, and projected onto the
exact rational coefficient equations for $\Phi$. The exact Hessian
biform identity passed, and all six leading principal minors were
strictly positive. The largest numerator or denominator required 161
bits. This concrete check supplements the universal conditioning proof;
it does not replace it. A targeted `python - <<'PY'` check of this review's
local links, display delimiters, trailing whitespace, and final newline
also passed. No project-wide verification or CI inspection was run.
