# Independent proof review of the certified cubic-root PosSLP reduction

Date: 2026-09-28. Status: the frozen proof passes this mathematical
audit. No substantive defect was found. Wording clarifications are
listed below. Publication priority is outside this review's scope.

The reviewed source is
[the proposed reduction](posslp-certified-cubic-root-reduction.md), with
SHA256
4682289ee8f943feee2d3d4f5f96da9869d6071abe0078f16ef521178d4614a9.
This reviewer did not develop the construction. The audit independently
reconstructs its arithmetic gadgets, analytic constants, error bounds,
interval certificates, output size, and feasibility orientation. The
quartic synthesis itself is an imported result; its statement and
[existing independent review](signed-odd-root-circuit-review.md) were
read to check that its actual input and output guarantees apply.

## Analytic multiplication and gate syntax

Let \(A(z)=(1+3z)^{1/3}-1\), taking the analytic branch near zero.
Its derivative at zero is one. For \(S(z)=A(z^2)\),

\[
 A(z)=z+O(z^2),\qquad S(A(z))=z^2+O(z^3).
\]

Consequently \(H(z)=\{S(A(z))+S(A(-z))\}/2\) is exactly even
and has expansion \(z^2+O(z^4)\). Thus

\[
 P(x,y)=A\bigl((H(x+y)-H(x-y))/4\bigr)
\]

has \(xy\) coefficient one and vanishes identically when either input
is zero. These are identities of analytic functions, not just of their
lowest Taylor terms. Exact axis vanishing permits a relative error
bound even when input orders differ.

The nine-gate implementation is correct. Four gates produce
\(A(x+y),A(-x-y),A(x-y),A(-x+y)\); four more apply \(S\);
the last applies \(A\) to the signed sum divided by eight. The
factor one-half in \(H\) and one-quarter in \(P\) multiply.
Writing the four stored roots as \(\zeta_j=1+S(\cdot)\) gives
the last radicand

\[
 1+\tfrac38(\zeta_1+\zeta_2-\zeta_3-\zeta_4).
\]

For \(\xi=1+x\), the radicand for \(S(x)\) is
\(3\xi^2-6\xi+4\). Addition and subtraction radicands are affine.
Every raw gate therefore has the permitted form. No independent-root
product is hidden in the notation.

## Analytic constants

On \(|z|\le1/12\), the disk \(1+3z\) stays at distance at least
\(3/4\) from zero. The branch is analytic on a neighborhood, and

\[
 |A'(z)|\le(4/3)^{2/3}<2,\qquad
 |A''(z)|\le2(4/3)^{5/3}<4.
\]

Integration along a line segment gives \(|A(z)|\le2|z|\).
Real Taylor's formula gives \(|A(z)-z|\le2z^2\).
For \(|x|,|y|\le r=1/100\), the successive argument and image
bounds in the source are valid. In particular, the outer argument has
modulus at most \(0.0016\), and \(|P|\le0.0032<1\).
All compositions are analytic on a neighborhood of the closed
polydisk, so Cauchy's estimate bounds the coefficient of \(x^iy^j\)
by \(r^{-i-j}\).

Vanishing on the axes eliminates every term with \(i=0\) or \(j=0\);
subtracting \(xy\) eliminates the \(i=j=1\) term. For
\(s=|x|/r,t=|y|/r\le1/4\), the remaining coefficient sum is at most

\[
 \frac{|xy|}{r^2}\frac{s+t-st}{(1-s)(1-t)}
 \le\frac{16}{9r^3}|xy|(|x|+|y|)
 \le\frac{2}{r^3}|xy|(|x|+|y|).
\]

Thus \(K=2^{24}>2/r^3\) suffices. The bound includes zero inputs.

## Homogenization and finite errors

The numerator and denominator signals need not represent the integer
value exactly as a quotient. Their assigned orders and coefficients
suffice. In addition, the two temporary numerator products both have
order \(d_a+d_b\), as required by the addition estimate.
Multiplication adds the two orders directly. The initializer
\(A(\delta-\delta)=0\) is exact. A zero assigned coefficient does not
invalidate the remainder bound or later induction.

The macro count \(T\) is fixed before adding the parameter circuit.
An integer addition uses three product macros and one addition macro;
an integer multiplication uses two product macros. Sharing old outputs
prevents expression-tree expansion. Hence \(T\) is linear in the
unit-constant circuit size. Assigned orders have polynomial bit length
and need not be printed.

For \(B=B_{j-1}\ge2\), multiplication of two approximations of
orders \(a,b\ge1\) gives error at most
\(3B^2\delta^{a+b+1}\). Their actual sizes give additional error

\[
 K(4B^2\delta^{a+b})(2B\delta^a+2B\delta^b)
 \le16KB^3\delta^{a+b+1}.
\]

For addition of order \(d\ge1\), inherited error is at most
\(2B\delta^{d+1}\), and the input to \(A\) has modulus at most
\(4B\delta^d\). The new error is at most
\(32B^2\delta^{2d}\le32B^2\delta^{d+1}\).
Both cases fit \(B_j=64KB_{j-1}^3\), including coefficient bounds.
Old signals retain their bounds because the \(B_j\) increase.

The logarithms satisfy \(b_0=1,b_j=30+3b_{j-1}\), hence
\(b_j=16\cdot3^j-15\). The assumption
\(B_T\delta\le2^{-30}\) bounds every signal input by \(2^{-29}\),
so all analytic estimates used in the induction apply.
This does not assume small intermediate integer circuit values.

At the final numerator the error is at most
\(2^{-30}\delta^{d_o}\), and its prescribed coefficient is the
nonzero integer \(W=2V-1\). Its modulus is at least one.
The final signal therefore has the sign of \(W\), including when
earlier gates cancel exactly.

## Parameter size and interval certificates

For positive \(z\), \(0<S(z)\le z^2\). Starting from the printed
rational \(\delta_0=1000^{-(Q+3)}\), exactly \(q=2T+5\) gates
produce \(\delta_q\le\delta_0^{2^q}\).
The first radicand uses \(\delta_0\) as a rational constant, so there
is no additional gate for it. Since \(\delta_0<2^{-4}\),

\[
 \delta_q<2^{-4\cdot2^q},\qquad
 4\cdot2^q=128\cdot4^T>16\cdot3^T+30.
\]

This proves the needed error assumption. No positive lower bound on
\(\delta_q\) is required. The exponentially small value is represented
by a short root circuit, rather than printed as a rational constant.

There are at most \(q+9T\le Q\) raw gates. Their widths satisfy
\(w_i=1000^i\delta_0\le1000^{-3}\), and every predecessor has
width at most \(w_{i-1}\). Direct interval evaluation deviates from
the central radicand value one by at most:

- \(6w_{i-1}\) for addition and subtraction;
- \(12w_{i-1}+3w_{i-1}^2\le13w_{i-1}\) for an \(S\) gate;
- \(3w_{i-1}/2\) for a product's final gate.

The quadratic estimate uses positivity of the predecessor boxes and
combines the exact square interval with the negative linear term.
It is valid even when separate occurrences are treated independently.
Repeated predecessors or coefficient cancellation can only improve it.

For \(0<w_i\le1/3\),

\[
 (1-w_i)^3\le1-2w_i\le1-13w_{i-1},\qquad
 (1+w_i)^3\ge1+3w_i\ge1+13w_{i-1}.
\]

The first radicand \(1+3\delta_0^2\) lies between one and
\(1+3w_1\). Thus every box passes the exact signed interval test
without access to the true gate values.

Each endpoint and the first radicand have \(O(Q)\) bits; the other
raw coefficients have constant bit length. There are polynomially
many entries. Computing \(1000^{Q+3}\), expanding macros, and
printing these rationals take polynomial bit time. The large proof
constants \(B_j\) and tiny \(\delta_q\) never need dense output.

## Quartic transfer

Every raw degree is three, with retained powers one and two. The
positive rational boxes pass the exact input promise of the
[signed-root synthesis theorem](signed-odd-root-circuit-quartic.md).
Its normalization factor \(\kappa\) has polynomial bit length.
That theorem returns a nonnegative rational quartic as a sum of
rational quadratic squares, with unique zero at the normalized
circuit point. It also supplies a rational positive definite Hessian
Gram and \(\nabla^2F\succeq I\).

Consequently \(F\le0\) restricts the variables to that zero. There,

\[
 X_{o,1}\ge\kappa
 \iff \xi_o\ge1
 \iff \xi_o>1
 \iff 2V-1>0
 \iff V>0.
\]

The weak-to-strict step is valid because the sign argument excludes
\(\xi_o=1\). This is a deterministic polynomial-time many-one
reduction, using the already reviewed synthesis theorem.
There is no unproved arithmetic separation assumption.

The result concerns exact empty-or-singleton feasibility. It does not
supply Slater points or a weak-feasibility gap. It does not establish
NP-hardness of PosSLP or hardness of approximate minimization. No
decision-hardness conclusion is inferred merely from output degree.

## Additional fixed-cube optimization consequence

During the audit, the authors proposed the following extension outside
the frozen file. It also passes independent mathematical checking.

Let \(w=\max_iw_i<1/3\). Then
\(\kappa=1/(1-w)<2\), and every normalized root obeys

\[
 0<\kappa\xi_i\le\frac{1+w}{1-w}<2.
\]

Both retained coordinates therefore belong to \((0,4)\).
The sharper displayed bound is needed; \(\kappa<2\) alone would
not imply the bound on squared coordinates.

For the designated first-power coordinate \(o\), set

\[
 X_o=\kappa+(8-\kappa)Y_o,\qquad
 X_j=8Y_j\quad(j\ne o).
\]

The image of \([0,1]^N\) contains the unique global zero of \(F\)
exactly when \(\xi_o>1\). A positive instance places that zero
strictly inside the box. A negative instance excludes it. Since \(F\)
is nonnegative and the cube is compact,

\[
 \min_{Y\in[0,1]^N}F(X(Y))=0
 \quad\Longleftrightarrow\quad V>0,
\]

and the minimum is strictly positive otherwise.
The optimization domain is always a fixed cube with the rational
strictly feasible point \((1/2,\ldots,1/2)\).

The affine diagonal \(D\) has entries eight except for
\(8-\kappa>6\). The transformed Hessian is at least
\(D^{\mathsf T}D\succeq36I\). Polynomial SOS is preserved by affine
substitution. For the full Hessian Gram, the old basis transforms by
the invertible rational linear map

\[
 (v,Y\otimes v)\longmapsto
 (Dv,(DY+b)\otimes Dv).
\]

Its diagonal blocks are \(D\) and \(D\otimes D\); the translation
only adds a lower-left block. Congruence therefore preserves positive
definiteness and rationality. The affine composition, dense quartic
coefficients, and transformed Gram all retain polynomial bit size.
This proves exact optimum-threshold hardness on a fixed compact domain.
It supplies no lower bound on the positive minimum in negative instances.

## Clarifications and verification record

These are wording improvements, not mathematical corrections:

- State explicitly that \(T\) counts arithmetic macros before the
  parameter generator is added, making the construction noncircular.
- Call \(3\xi^2-6\xi+4\) a squaring-simulation gate or \(S\) gate,
  rather than a square-root simulation gate.
- State explicitly that \(F\) is nonnegative, using the imported
  theorem's rational polynomial SOS.

Targeted checks were reading the frozen proof and the imported theorem
and review, and verifying the frozen SHA256 with the shell checksum
utility. The inequalities above were rederived symbolically by the
reviewer. No floating-point experiment, computer-algebra calculation,
Lean proof, or project-wide test is claimed here.
An attempted additional narrow-agent audit was unavailable because
the agent thread limit had been reached.
The independently authored computational checker and the separate
literature audit have distinct scopes and do not replace this proof.

## Reconciliation of the amended source

The amended source has SHA256
6545a3d03ee47a18b20c93de4ed31757571ee97bf9581bdfb8aaa6fac83bb475.
Its explicit macro count, squaring-gate terminology, and nonnegativity
statement incorporate the suggested clarifications. Its added cube
optimization section agrees with the independently checked extension
above, including the sharper normalized-coordinate bound, Hessian
congruence, compactness argument, and distinction between the cube's
Slater point and degenerate threshold feasibility. These changes pass
the scoped reconciliation. The analytic construction and constants
were unchanged. The new prior-comparison paragraph remains assigned
to the separate literature audit.
