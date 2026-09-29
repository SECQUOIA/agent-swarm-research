# A rational Hessian certificate for the irrational-zero quartic

Date: 2026-09-28. Status: exact symbolic verification and Lean verification
of the second directional derivative bound complete. This supplies a second proof of
global strong convexity for the polynomial in
[the construction](convex-quartic-irrational-zero.md). It proves the
slightly weaker bound $4096I$, while the analytic proof establishes
$4124I$. It does not replace or re-review the construction's literature
comparison or its zero-set argument.

## Claim and differentiated polynomial

Let

\[
 A=12599x^2-10000xy+7937y^2-15874x-12599y+20000,
 \qquad F=A^2+10000[(x^2-y)^2+(y^2-2x)^2].
\]

Then $\nabla^2F(x,y)\succeq4096I$ for every real $x,y$.
This follows from an explicit rational identity and positive integer
coefficients, without estimates involving $\sqrt[3]{2}$.

Direct differentiation gives

\[
\begin{aligned}
 H_{11}={}&1904937612x^2-1511880000xy-2399958312x\\
          &+599993052y^2-19204y+1511967752,\\
 H_{12}={}&-755940000x^2+1199986104xy-19204x\\
          &-476220000y^2-87752y-6948,\\
 H_{22}={}&599993052x^2-952440000xy-87752x\\
          &+756071628y^2-1199979156y+952449602.
\end{aligned}
\]

Here $H=\nabla^2F$. Define the directional gap

\[
 P(x,y,a,b)=a^2(H_{11}-4096)+2abH_{12}+b^2(H_{22}-4096).
\]

It suffices to prove $P\ge0$ for all real arguments.

## Integer sum-of-squares identity

Make the invertible rational change of coordinates

\[
 x=\frac{63}{50}+\frac X{100},\qquad
 y=\frac{1587}{1000}+\frac Y{100}.
\]

For arbitrary real $a,b,X,Y$, set

\[
\begin{aligned}
 v_0&=2a-2b, & v_1&=2b,\\
 v_2&=2Xa-Xb-Ya+Yb, & v_3&=2Xb+Ya-Yb,\\
 v_4&=2Ya-Yb, & v_5&=2Yb.
\end{aligned}
\]

Let $N$ be the following symmetric integer matrix, displayed by rows:

```text
 812297303152  102427849072   22618204800  -13093175680    5654551200    -130053040
 102427849072  262472489120   22618204800   -5643994880    1929960800   -3911932400
  22618204800   22618204800  761975044800   78611522400   39305761200   -2034439000
 -13093175680   -5643994880   78611522400  128114982000  -15939729800  -13708914300
   5654551200    1929960800   39305761200  -15939729800  112025966300   13144848050
   -130053040   -3911932400   -2034439000  -13708914300   13144848050  120298532375
```

Its strict diagonal-dominance margins are

\[
\begin{aligned}
(\delta_0,\ldots,\delta_5)
={}&(668373469360,125940547168,596786912600,\\
   &\qquad1117644940,36051115250,87368345585),\\
\delta_i={}&N_{ii}-\sum_{j\ne i}|N_{ij}|>0.
\end{aligned}
\]

The complete certificate is the polynomial identity

\[
\boxed{
\begin{aligned}
16000000\,P\left(\frac{63}{50}+\frac X{100},
                 \frac{1587}{1000}+\frac Y{100},a,b\right)
 &=v^{\mathsf T}Nv\\
 &=\sum_{i=0}^5\delta_i v_i^2
   +\sum_{0\le i<j\le5}|N_{ij}|
       \bigl(v_i+\operatorname{sign}(N_{ij})v_j\bigr)^2.
\end{aligned}}
\]

The second equality follows by expansion: every off-diagonal term is
$2N_{ij}v_iv_j$, and the coefficient of $v_i^2$ is
$\delta_i+\sum_{j\ne i}|N_{ij}|=N_{ii}$.
Every coefficient in the 21-square expression is a positive integer.
The first equality is an exact identity of rational polynomials; the
targeted checker expands and verifies it. Since the coordinate change
covers every real $(x,y)$, the identity proves the claimed Hessian bound.
The usual Hessian criterion therefore makes $F$ globally strongly
convex with parameter $4096$.

The identity also gives a rational Gram certificate that
$F-2048(x^2+y^2)$ is SOS-convex: its directional Hessian is a sum of
positive rational multiples of squares of rational polynomials.
The original $F=A^2+[100(x^2-y)]^2+[100(y^2-2x)]^2$ is itself a rational
sum of squares. Thus explicit rational certificates of nonnegativity
and strong convexity coexist with the construction's irrational
unique zero. This is a consequence of the displayed identities,
not a separate novelty claim about SOS-convex polynomials.

## Independent Gram-matrix check

The certificate was first found in the monomial vector

\[
 w=(a,b,Xa,Xb,Ya,Yb)^{\mathsf T}.
\]

The integer matrix $M$ in
[the checker](check_convex_quartic_rational_sos.py) satisfies

\[
250000\,P\left(\frac{63}{50}+\frac X{100},
               \frac{1587}{1000}+\frac Y{100},a,b\right)
 =w^{\mathsf T}Mw.
\]

For clarity, the scalar here is $250000$, not $16000000$.
Let

\[
 U=\begin{pmatrix}
 1&-1&0&0&0&0\\
 0&1&0&0&0&0\\
 0&0&1&-1/2&-1/2&1/2\\
 0&0&0&1&1/2&-1/2\\
 0&0&0&0&1&-1/2\\
 0&0&0&0&0&1
 \end{pmatrix}.
\]

Then $v=2Uw$ and $U^{\mathsf T}NU=16M$, which explains the
factor $64$ between the two identities. The checker verifies these
matrix identities over the rationals. It additionally verifies that
all six leading principal minors of $M$ are positive and that an exact
$LDL^{\mathsf T}$ factorization has positive diagonal entries. These
are separate exact matrix checks of the same certificate; the
positive-square proof above does not require them.

## Discovery, verification, and limits

A numerical semidefinite program helped select a Gram matrix from its
three-parameter affine family. Rounding the three free parameters to
integers gave $M$. Rounding its triangular factor to half-integers
gave $U$. Numerical feasibility is not used in the proof, and no
numerical solver is needed to run the saved checker.

Command actually run:

```text
python research-20260927/check_convex_quartic_rational_sos.py
```

It passed the following targeted checks using SymPy exact arithmetic:

- Differentiate the original $F$ and verify the Gram identity.
- Verify the integer matrix $N$, its six positive margins, and its
  square decomposition for an arbitrary six-dimensional vector.
- Verify the complete 21-square identity in shifted coordinates and
  again after substituting $X=100x-126$, $Y=100y-1587/10$.
- Verify the six positive leading principal minors and positive exact
  $LDL^{\mathsf T}$ factorization of $M$.

The symbolic checker establishes identities and rational signs. The
conclusion for all real inputs follows from nonnegativity of squares
and the ordinary Hessian criterion. An independent exact rational
interpolation and elimination check of the original Gram certificate
is recorded in [the root audit](convex-quartic-root-audit.md).

The [Lean file](../formal/ConvexQuarticIrrationalZero.lean) separately
verifies the displayed 21-square identity by `ring` and its sign by
`positivity`. It also differentiates the original $F$ along arbitrary
affine lines twice. Its theorem `quartic_second_deriv_lower_bound`
therefore proves, for all real $x,y,a,b$,

\[
4096(a^2+b^2)\le
\left.\frac{d^2}{dt^2}F(x+ta,y+tb)\right|_{t=0}.
\]

The formalization author ran `lake env lean ConvexQuarticIrrationalZero.lean`
from `formal/`; it exited successfully without warnings, and the
reported axioms were only `propext`, `Classical.choice`, and `Quot.sound`.
The full scope and command are recorded in
[the verification record](convex-quartic-lean-verification.md).
This certificate's author subsequently read the formal definitions,
square coefficients, and derivative theorems for correspondence. The
Lean result covers the actual second derivative, not merely a separately
defined polynomial claimed to be a Hessian. The subsequent theorem
`quartic_convex` also verifies `ConvexOn ℝ Set.univ` on `ℝ × ℝ`
by the second-derivative criterion on affine lines. A named strong
convexity predicate and the stronger constant $4124$ are not formalized
here. No project-wide checks or CI checks were run for this addition.
