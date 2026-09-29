# Independent review of the three-ellipsoid degree construction

Date: 2026-09-28. Scope: the proof and coefficient bounds in
[the construction note](few-quadratic-unbounded-degree.md), including its
general one-real-root proposition and its polynomial-time binomial
specialization. This reviewer did not develop the construction. A fresh
subreviewer separately checked the affine spectral gap and rational
triangle step. No mathematical defect was found in the version reviewed.
The rational projection formula was independently derived during review
and communicated to the author.

The construction proves that three rational strictly convex quadratic
inequalities can have a unique feasible point whose coordinate field has
arbitrarily large degree. For the odd binomials `T^d-2`, it is constructive
with polynomial input length. This is a witness-degree result, not a
decision-time lower bound.

The general existence proof is sound. An irreducible rational polynomial
in characteristic zero has distinct roots. If it has exactly one real
root `alpha`, the real vector `v(alpha)` and the real and imaginary parts
of one vector from each nonreal conjugate pair form a real basis. This
follows from the invertibility of the complex Vandermonde matrix and the
invertible conversion between each conjugate pair and its real and
imaginary parts. Defining a symmetric bilinear form to have matrix
`diag(0,1,1,...,1,1)` in that basis means applying a congruence, and
produces a PSD form with kernel `R v(alpha)`.

For a conjugate vector `v(beta)=a+i b`, its quadratic value is
`a^T B_* a - b^T B_* b + 2i a^T B_* b = 1-1+0 = 0`.
This calculation uses a symmetric bilinear form, not a Hermitian form.
Vanishing at every distinct root implies divisibility by the defining
polynomial, so `B_*` belongs to the real solution space of the rational
remainder equations. Rational points are dense in this linear space.
Positivity on the fixed real subspace `U` survives a sufficiently small
rational perturbation in that space.

The companion-matrix orientation is correct: its superdiagonal entries
are one, its last row is the negative coefficient vector, and
`C v(beta)=beta v(beta)`. The span `U` of the nonreal real/imaginary
vectors is invariant under `C`. The restriction of `C-alpha I` to `U`
is invertible, while its kernel is the real eigenline. Thus its image is
exactly `U`. Positivity of `B` on this image proves

\[
 R=(C-\alpha I)^T B(C-\alpha I)\succeq0,
 \qquad \ker R=\mathbb Rv(\alpha).
\]

There is no need for `B` itself to be PSD. In fact, a nonzero rational
PSD matrix could not serve here: its zero quadratic value at `v(alpha)`
would imply `B v(alpha)=0`, and rational linear independence of
`1,alpha,...,alpha^(d-1)` would then force every row of `B` to be zero.
The construction correctly asks only for positivity on `U`.

The three rational coefficient matrices satisfy
`v(alpha)^T Q_j v(alpha)=0`. They generally do not satisfy
`Q_j v(alpha)=0`; the note uses the correct scalar identity. The
restriction of `R` to `H={z:z_0=0}` is positive definite because its
one-dimensional kernel does not meet `H` nontrivially. A sufficiently
small rational triangle in the plane `lambda_0=1`, containing
`(1,alpha,alpha^2)` in its relative interior, therefore gives three
rational quadratics with positive-definite affine Hessians.

Their positive barycentric combination is `z(x)^T R z(x)`. If all three
rows are nonpositive, that combination must be zero. The PSD kernel
condition and the fixed first coordinate `z_0=1` force
`z(x)=v(alpha)`. Conversely all three rows vanish there. This proves
the singleton claim, including attainment. Every individual quadratic
has a rational minimizer, obtained by solving its rational positive-
definite linear stationarity system. Its minimum is strictly negative:
otherwise its zero at the irrational point would make that point its
rational minimizer. Each individual sublevel is consequently a bounded,
full-dimensional ellipsoid. The joint system has no strict feasible
point; the proof does not claim one.

For the binomial specialization, all quantitative steps also check out.
With `alpha=2^(1/d)` and `D=diag(1,alpha,...,alpha^(d-1))`, let
`P=I-11^T/d`. Then `B_*=D^(-1) P D^(-1)` is PSD with kernel
`R v(alpha)`. At a nontrivial `d`th root of unity `zeta`, the normalized
vector is `(1,zeta,...,zeta^(d-1))`. Both the sum of its entries and
the sum of their squares vanish because `d` is odd. This proves the
remainder identity. Oddness is essential here: at `zeta=-1` in even
dimension the sum of the squares does not vanish.

If `S` is cyclic shift, `C=alpha D S D^(-1)`. Hence
`U=D 1^perp`. For `u=Dw` with `w` orthogonal to `1`,
`u^T B_* u=||w||^2 >= ||u||^2/4`, since every diagonal entry of `D`
lies in `[1,2)`. Also `||B_*||_2 <= 1`. Thus an operator-norm
perturbation of at most `1/8` retains a lower bound `1/8` on `U`.
The note obtains this operator bound from a Frobenius bound, which is
valid. An entrywise error of `1/8` by itself would not suffice.

The rational projection is especially well controlled. For each residue
`r`, the matrix `E_r` has exactly the entries specified by reduction of
`T^(i+j)` modulo `T^d-2`. Using the full Frobenius inner product
automatically counts the symmetric off-diagonal entries twice, as the
quadratic form requires. Its support is disjoint from every other
`E_s`, and

\[
 \|E_r\|_F^2=(r+1)+4(d-r-1),\qquad
 d\leq\|E_r\|_F^2<4d.
\]

The displayed formula is therefore the exact orthogonal projection onto
the rational remainder kernel. It preserves symmetry, fixes `B_*`, and
contracts Frobenius error. There is no ill-conditioned basis inversion.
If the preliminary rounding uses a common dyadic denominator `M`, each
final entry is modified by only one projection term. Its denominator
divides `M ||E_r||_F^2`; it does not accumulate a product over all `d`
rows. Taking `M` polynomial in `d` gives `O(log d)` bits per entry,
including numerators. Approximating `alpha` to a suitable inverse-
polynomial error and evaluating its powers and reciprocals provides the
required rounded matrix in polynomial time. The sensitivity from powers
up to `2d-2` costs only another `O(log d)` precision bits.

On the affine direction space, write `y=(C-alpha I)z` with `z_0=0`.
The first `d-1` equations yield
`z_j=sum_(i<j) alpha^(j-1-i) y_i`. Every coefficient has magnitude
less than two. Cauchy--Schwarz and summation therefore give
`||z|| <= 2d ||y||`. Combining this with the lower bound on `B|U`
gives exactly the stated conservative margin

\[
 z^T Rz\geq\frac1{32d^2}\|z\|^2\qquad(z\in H).
\]

The coefficient bounds follow from `||C||_2=2` and `||B||_2<=9/8`:
`||Q_0||_2<=9/2`, `||Q_1||_2<=9/2`, and `||Q_2||_2<=9/8`.
For parameter errors at most `r=1/(1024d^2)`, the operator perturbation
is at most `45r/8`, strictly less than `1/(32d^2)`. Positive
definiteness is preserved with room to spare.

The note's particular triangle also works. Relative to its rational
center `c`, put `u=alpha-c_1`, `v=alpha^2-c_2`. Its vertices are
`(r/2,0)`, `(-r/2,r/2)`, and `(-r/2,-r/2)`. The barycentric weights
of `(u,v)` are

\[
 \frac12+\frac ur,\qquad
 \frac14-\frac{u}{2r}+\frac vr,\qquad
 \frac14-\frac{u}{2r}-\frac vr.
\]

When `|u|,|v|<=r/16`, they are bounded below by `7/16`, `5/32`,
and `5/32`, respectively. The triangle is nondegenerate, the target
lies strictly inside, and each vertex lies within maximum distance
`9r/16<r` of the target. Rational approximation of the center and the
displayed rational offsets have `O(log d)`-bit representations. Combining
the three rational coefficient matrices involves only a bounded number
of terms per entry, so the final coefficients also have `O(log d)`
bits. In particular the weaker polynomial-length claim in the note is
fully justified; a dense encoding has size `O(d^2 log d)`.

The coordinate field has degree exactly `d`: it contains `alpha`, all
other coordinates are its powers, and `T^d-2` is Eisenstein at two.
This disproves a degree bound depending only on the number of these
convex quadratics or their Hessian-span dimension. The construction has
span at most three, which is all the proposition needs; its proof does
not need a separate universal span-equality argument. A single such
family still has degree only `n+1`, so it does not by itself rule out an
FPT witness algorithm with polynomial dependence on the ambient input,
and supplies no yes/no lower bound. Product-field or output-format
strengthenings require separate proofs. No literature or novelty claim
was audited here.

The proposed extension from two to an arbitrary prime radicand `ell`
also passes the quantitative audit. Now `1<=D_jj<ell`,
`B_*|U >= I/ell^2`, and the projection denominator is
`(r+1)+ell^2(d-r-1) <= d ell^2`. A Frobenius error of at most
`1/(8ell^2)` gives `B|U >= 7I/(8ell^2)` and `||B||<=33/32`.
The pinned-cycle estimate gives
`||(C-alpha I)z|| >= ||z||/(ell d)` on `H`, so the affine margin is
at least `7/(8ell^4 d^2)`. Here `||C||=ell`,
`||Q_1||<=33ell/16`, and `||Q_2||<=33/32`. The checker's triangle
with side parameter `1/(100ell^5 d^2)` has all vertices within twice
that parameter of the target, well inside the positive-definiteness
neighborhood. A common rounding grid of polynomial size in `d,ell`
again gives `O(log(d ell))` bits per coefficient. Its denominators may
have polynomial magnitude in `ell`; their binary lengths, and the bit
operation counts, are polynomial in `d` and `log ell`. Irreducibility
uses that the radicand is prime. This extension does not require a
different conceptual argument.

Targeted verification used an inline Python/SymPy script for
`d=3,5,7,9`. It constructed an exact dyadic lower approximation to
`2^(1/d)` using integer root extraction; rounded the real template with
a proved error bound; applied the rational Frobenius projection;
formed the displayed rational triangle; and checked every row's
vanishing modulo `T^d-2`. It verified positive definiteness using exact
positive leading principal minors and checked Hessian span three in
these four examples. All four cases passed. These finite checks support
the formulas; the general result follows from the argument audited
above. After inspecting
`check_few_quadratic_unbounded_degree.py`, a separate inline Python
command loaded it with `runpy.run_path` and called `check_block(5,3)`;
that prime-radicand extension passed. This initial review did not run its
extra degree-nine sum example. The subsequent product-field audit is
recorded below.
An inline Python document check passed for this review's local link,
display delimiters, final newline, whitespace, and control characters.
No project-wide verification or CI inspection was performed.

An integration review on the same date checked the completed block-output
corollaries. It also checked the final uniform-radicand triangle, which
replaces the initial symmetric triangle and constants discussed above.
The completed corollaries are correct. One triangle-weight mismatch was
identified during drafting and is resolved in the final construction.

The final triangle has vertices `c+(-e,-e)`, `c+(2e,-e)`, and
`c+(-e,2e)`, where `e=1/(100a^5 d^2)` and each coordinate of `c`
approximates the target within `e/16`. Its weights are
`1/3-(delta_1+delta_2)/(3e)`, `(1+delta_1/e)/3`, and
`(1+delta_2/e)/3`. They are bounded below by `7/24`, `5/16`, and
`5/16`, hence all exceed `1/4`. Every vertex is within `33e/16<3e`
of the target. The uniform affine spectral margin is at least
`1/(2a^4 d^2)`, and `3(4a+2)e` is strictly smaller. Thus the expanded
neighborhood preserves positive definiteness and supplies the stronger
weights used in mixing. The earlier symmetric triangle only guaranteed
`5/32`; substituting that weaker bound into the original claimed
`>1/8` mixing estimate would have been incorrect.

The field-degree proof works for every odd `d`, including composite
values. Let the distinct prime radicands `a_i` avoid the prime divisors
of `d`. At the next prime `a_i`, each earlier field generated by a
radical is unramified because its defining integer polynomial has
discriminant `+/- d^d a_j^(d-1)`. The cyclotomic field
`F=Q(zeta_d)` is also unramified there. These implications use the
discriminant criterion and cyclotomic ramification theorem, verified by
the fresh subreviewer in
[MIT's number theory notes, Section 12.4 and Proposition 19.14](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf).
Unramified extensions remain unramified under compositum; this does not
assume the linear disjointness being proved. The needed local fact is
stated in
[Conrad's compositum handout, page 2](https://math.stanford.edu/~conrad/154Page/handouts/tamecomp.pdf).

At a prime ideal over `a_i` in either previous compositum, the normalized
discrete valuation consequently has `v(a_i)=1`. Eisenstein applied in
the localized DVR proves that adjoining `a_i^(1/d)` multiplies the
degree by `d`. The DVR version of Eisenstein is
[MIT Lemma 11.2](https://ocw.mit.edu/courses/18-785-number-theory-i-fall-2021/mit18_785f21_full_lec.pdf).
This proves both `[K:Q]=d^k` and `[F K:F]=d^k`. It uses neither
pairwise-intersection reasoning nor an assumption that `d` is prime.

The monomials `prod_i alpha_i^j_i`, with `0<=j_i<d`, are a tower
basis over `F`. The extension is the splitting field of the binomials
over `F`, hence Galois. Its automorphism group injects into the `d^k`
possible independent root-of-unity substitutions, and its order is
already `d^k`; every substitution therefore occurs. Distinct tuples
give distinct sums because the separate elements `alpha_i` are distinct
basis monomials. For `s=sum_i alpha_i`,

\[
 d^k=[F(s):F]\leq[\mathbb Q(s):\mathbb Q]
       \leq[K:\mathbb Q]=d^k.
\]

Thus `s` generates the whole coordinate field over `Q`, without a
generic primitive-element choice or an unbounded search for weights.

The exact span argument is also valid. A dependence between rational
Hessian matrices can be taken over `Q`. After converting through the
invertible triangle coefficient matrix, a relation among their affine
Hessians gives a rational quadratic form whose restriction to `z_0=1`
is affine. Its value at the full power-basis point is zero, so rational
linear independence of `1,alpha,...,alpha^(d-1)` makes the whole form
zero. Pair it with `v(beta_j)` and its complex conjugate. The factor
`v(beta_j)^T B v(conjugate(beta_j))` is strictly positive: it is the
sum of the positive quadratic values of the real and imaginary parts
in `U`. Dividing gives the displayed cosine relation. Two distinct
cosines force the middle coefficient to vanish when `d>=5`; the
irrationality of `alpha^2` then removes the others. For `d=3`, the
same relation is directly a cubic power-basis relation. Each block
therefore has span exactly three. Disjoint supports give exact span
`3k`, and the later invertible row mixing and coordinate congruence
preserve it. Irreducibility is essential for this exact-span argument;
the note restricts the assertion accordingly.

The specified affine change is unimodular in its linear part: replace
`x_11` by `R+sum_i x_i1`, keep all other coordinates, and recover
`x_11` by subtraction. Here `R=1+sum_i a_i` has short integer
encoding. Every conjugate of `s` has modulus at most
`sum_i a_i^(1/d)<sum_i a_i<R`. Every conjugate of the new first
coordinate thus has strictly positive real part. A real root contributes
a factor `X-r` with `r>0`; a conjugate pair contributes
`X^2-2 Re(z) X+|z|^2`. Each factor has strictly alternating nonzero
coefficients. Substituting `-X` and correcting the overall sign makes
every factor's coefficients positive. Their product has a positive
coefficient at every degree. This proves that the actual first
coordinate's minimal polynomial has exactly `d^k+1` nonzero terms.
The argument is constructive and does not use a generic translation.

For mixing, write `m=3k` and `M=I+epsilon 11^T`, with
`epsilon=1/(8k)`. Its eigenvalues are one and `1+m epsilon`, so it
is invertible. The Hessian of the sum of the block rows is positive
definite on the full space. Each mixed Hessian is therefore positive
definite. If `tau` collects the block weights, then `sum tau=k`,
and direct inversion gives

\[
 M^{-T}\tau=\tau-\frac{\varepsilon k}{1+3k\varepsilon}\boldsymbol1
           =\tau-\frac1{11}\boldsymbol1.
\]

Every new weight exceeds `1/4-1/11=7/44>1/8`. The old nonnegative
aggregate, whose only zero is the product point, is therefore a positive
combination of the mixed rows. This proves preservation of the singleton;
invertibility alone would not have proved equivalence of the inequality
systems. All rows still vanish at the singleton. Rational strict-convex
minimizers again show that each mixed ellipsoid has nonempty interior.

The fixed-`k` input estimate survives both operations. Before mixing,
each nonconstant matrix entry is supported on one block, so its sum
uses only three block rows. Mixing may sum `3k` rational constants
with different denominators, giving `O_k(log d)` bits when the
radicands and `k` are fixed. This is sufficient and is explicitly
distinguished from the single-block uniform coefficient bound. The
shear replaces only `x_11` by a sum of selected coordinates. Every
new quadratic coefficient is a sum of at most four old matrix entries;
the associated linear and constant transformations also preserve
`O_k(log d)` coefficient length. There are `3k` forms in
`k(d-1)` variables, so the dense encoding remains
`N=O_k(d^2 log d)` with an exponent independent of `k`.

Fixing `k>2C` and letting `d` grow through odd primes outside the fixed
radicand list makes `d^k+1` exceed `f(3k) N^C` for every fixed
exponent `C` and finite parameter factor. This proves the asserted
output obstruction for dense or ordinary sparse coefficient lists of
the actual coordinate minimal polynomials. It also gives the stated
degree obstruction for dense univariate representations of the whole
point. It does not prove a sparse-output obstruction for an arbitrary
different primitive generator, a nonminimal annihilating polynomial,
or a circuit representation. It gives no decision-time lower bound.
The completed manuscript keeps these output distinctions.

The subsequently added planar-pencil corollary is correct under the
stated irreducibility and unique-real-root assumptions. Put
`v=v(alpha)` and `w=Bv`. Rationality of `B` and independence of the
full power basis show `w!=0`: otherwise every rational row of `B`
would vanish coefficientwise, contradicting positivity on `U`.
If `C^T w` were a real scalar multiple `kappa w`, then `kappa`
would be a real eigenvalue, hence the unique real root `alpha`.
For every other right eigenvector `v(beta)`,
`(beta-alpha) w^T v(beta)=0`. Also `w^T v(alpha)=0` by the defining
remainder identity. The complete Vandermonde eigenbasis would force
`w=0`, a contradiction. Thus `w` and `C^T w` are independent.

For every real `s,t`, the quadratic value of
`Q_0+s Q_1+t Q_2` at `v` is zero. If that symmetric matrix is PSD,
it annihilates `v`. Direct multiplication yields

\[
 0=(\alpha-s)C^T w+(t-s\alpha)w.
\]

Independence gives `s=alpha` and `t=alpha^2`. The matrix at this
pair is the previously proved PSD matrix `R`, of corank one. This
proves the exact two-variable singleton spectrahedron assertion.
The proof needs neither a numerical eigenvector computation nor a
conditioning argument. It does not supply a decision-time lower bound.

This integration audit read the changed block and planar-pencil proof
sections and independently derived the displayed identities and bounds.
The fresh field subreviewer
checked the primary ramification sources linked above. The unchanged
base examples and degree-nine example were not rerun. A later section
characterizing possible real algebraic singleton coordinates is outside
this block-output audit. No project-wide verification or CI inspection
was performed.
