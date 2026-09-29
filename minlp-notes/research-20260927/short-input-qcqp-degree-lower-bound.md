# Short rational convex QCQPs with multiplicative algebraic degree

Date: 2026-09-27. Status: proof checked in stages. A reviewer supplied the
constant-term simplification and value-valuation proof; fresh reviewers
then checked those arguments, field composition, constructive weighting,
and the positive definite constraint refinement.
The proposed contribution is an explicit arithmetic construction
with coefficient-size control. The generic degree formula, Eisenstein's
criterion, Hensel lifting, and the primitive-element argument are classical.

The generic sharpness result in
[the degree sharpness note](multihomogeneous-degree-sharpness.md) does not
bound the size of a rational specialization. The separate
[effective Hilbert construction](sharp-degree-effective-hilbert-audit.md)
already proves polynomial-size existence with degree \((2r)^h\) for all
block dimensions \(r\). The construction here gives a direct arithmetic
alternative, with fully computable coefficients, for certain block
dimensions. It does not strengthen that existence theorem.

Here a direct construction gives
one strictly convex trust-region problem of degree \(2r\), for
\(r=p-1\) and any prime \(p\equiv1\pmod4\). Congruences then make the fields
of several blocks linearly disjoint, using coefficients of short binary
length. The optimizer field has the product of the block degrees. A positive
rational weighting of the objectives, also of short binary length, gives an
optimal value of the same degree.

**Constructive theorem.** Given increasing primes
\(p_1,\ldots,p_h\equiv1\pmod4\), put
\(n=\sum_i(p_i-1)\) and \(P_{\max}=p_h\). One can construct a rational
QCQP in \(n\) variables, in time polynomial in \(n\) and \(h\), with:

- \(h\) positive definite constraint Hessians spanning a space of
  dimension exactly \(h\);
- a positive definite objective Hessian, compact feasible set, and strict
  feasibility;
- a unique optimizer \(x^*\) and value \(v\) satisfying
  \(\mathbb Q(x^*)=\mathbb Q(v)\) and
  \[
  [\mathbb Q(v):\mathbb Q]=\prod_{i=1}^h2(p_i-1);
  \]
- coefficient bit lengths
  \(O((hP_{\max}^4+h^2P_{\max}^3)\log P_{\max})\).

The construction combines (12), (17), and (20). The constants in this
coefficient estimate are conservative. A smaller coefficient bound,
\(O(h^2\log P_{\max})\), holds by an existence argument in Section 4.

No hardness of approximate optimization follows. These problems separate
into ordinary trust-region problems before the optional Hessian mixing.
The conclusion concerns the size of an
expanded algebraic output, and distinguishes that output from a compact sum
of algebraic numbers.

## 1. One block

Let \(p\equiv1\pmod4\) be prime, let \(r=p-1\), and choose
\(\kappa\in\{1,\ldots,p-1\}\) with \(\kappa^2\equiv-1\pmod p\).
Let \(K>0\) be an integer satisfying

\[
K\equiv\kappa\pmod{p^2}.
\]

Consider the rational QCQP

\[
\min_{x\in\mathbb R^r}
 f(x)=\frac12\sum_{j=1}^r jx_j^2-K\sum_{j=1}^r jx_j,
 \qquad \sum_{j=1}^r x_j^2\le1.                    \tag{1}
\]

Its objective Hessian is positive definite, its feasible set is compact, and
zero is strictly feasible. The unconstrained minimizer has every coordinate
equal to \(K\), so it lies outside the unit ball. Consequently the unique
optimizer is

\[
x_j^*=\frac{Kj}{j+\lambda},\qquad
\sum_{j=1}^r\frac{K^2j^2}{(j+\lambda)^2}=1,       \tag{2}
\]

where \(\lambda>0\) is unique: the left side of (2) is strictly decreasing
on \(\lambda\ge0\), starts at \(rK^2>1\), and tends to zero. The multiplier
uses the Lagrangian \(f+\frac\lambda2(\|x\|^2-1)\).

Define integer polynomials

\[
F(T)=\prod_{j=1}^r(T+j),\qquad
F_j(T)=\frac{F(T)}{T+j},\qquad
P(T)=F(T)^2-K^2\sum_{j=1}^r j^2F_j(T)^2.          \tag{3}
\]

The polynomial \(P\) is monic of degree \(2r\), and \(P(\lambda)=0\).

### 1.1. The secular polynomial is Eisenstein

Work first modulo \(p\). Then \(F(T)=T^r-1\) and \(K^2=-1\). We claim

\[
P(T)\equiv T^{2r}\pmod p.                       \tag{4}
\]

For completeness, put \(\alpha=-j\in\mathbb F_p^\times\). At this root
of \(F\),

\[
F_j(\alpha)=F'(\alpha)=r\alpha^{r-1}=-\alpha^{-1},
\]

so \(j^2F_j(\alpha)^2=1=\alpha^{2r}\). Also

\[
\frac{F_j'(\alpha)}{F_j(\alpha)}
 =\frac{F''(\alpha)}{2F'(\alpha)}
 =\frac{r-1}{2\alpha}
 =\frac r\alpha.
\]

Therefore \(P-T^{2r}\) and its derivative vanish at all \(r\) distinct roots
of \(F\). This difference has degree less than \(2r\), and hence is zero.
This proves (4).

The constant term has a simple closed form:

\[
P(0)=(r!)^2(1-rK^2).                              \tag{5}
\]

Write \(\kappa^2+1=kp\). Since \(1\le\kappa\le p-1\),
\(1\le k\le p-2\). Directly,

\[
\frac{1-(p-1)\kappa^2}{p}=1-(p-1)k\equiv1+k\not\equiv0\pmod p.
\]

The congruence \(K\equiv\kappa\pmod{p^2}\) preserves this valuation.
As \(p\nmid r!\), (5) gives \(v_p(P(0))=1\). Thus \(P\) is Eisenstein at
\(p\), and

\[
[\mathbb Q(\lambda):\mathbb Q]=2r.               \tag{6}
\]

Every optimizer coordinate is nonzero, belongs to \(\mathbb Q(\lambda)\),
and recovers the multiplier by \(\lambda=Kj/x_j^*-j\). In particular every
coordinate, as well as the joint optimizer field, has degree \(2r\).

### 1.2. The optimal value generates the same field

Let \(v=f(x^*)\) and \(\beta=2v\). Using the active norm constraint gives

\[
\beta=-\lambda-K^2\sum_{j=1}^r\frac{j^2}{j+\lambda}.
                                                               \tag{7}
\]

Extend the normalized \(p\)-adic valuation, with \(v_p(p)=1\), to a field
containing a root of \(P\). Since \(P\) is Eisenstein,

\[
v_p(\lambda)=\frac1{2r}.
\]

All \(j\in\{1,\ldots,r\}\) are \(p\)-adic units, so (7) has the
convergent expansion

\[
\beta=-K^2\sum_jj+(rK^2-1)\lambda
 +\sum_{m\ge2}(-1)^{m+1}K^2
       \left(\sum_j j^{1-m}\right)\lambda^m.     \tag{8}
\]

The constant coefficient has valuation exactly one because
\(\sum_jj=p(p-1)/2\). The coefficient of \(\lambda\) is divisible by \(p\).
For \(2\le m\le r\), the coefficient of \(\lambda^m\) is also divisible
by \(p\), by the sum of a nontrivial character of
\(\mathbb F_p^\times\). At \(m=r+1\), that character is trivial and the
coefficient is a unit. Every later coefficient is \(p\)-adically integral.
Thus the term with \(m=r+1\) has the unique smallest valuation, and

\[
v_p(\beta)=\frac{r+1}{2r}.                       \tag{9}
\]

Here \(r\) is even, so \(\gcd(r+1,2r)=1\). The reduced denominator of the
valuation of an algebraic number divides the ramification index of its
local field, which is at most its degree over \(\mathbb Q\). Equation (9)
therefore implies

\[
[\mathbb Q(v):\mathbb Q]\ge2r.
\]

The reverse inequality follows from (7) and (6), so

\[
\mathbb Q(v)=\mathbb Q(\lambda)=\mathbb Q(x^*),
\qquad [\mathbb Q(v):\mathbb Q]=2r.               \tag{10}
\]

Taking \(K=\kappa<p\) already gives the single-block construction with
\(O(\log p)\)-bit coefficients.

## 2. A splitting lemma for later primes

Suppose \(q>r\) is an odd prime and \(q\mid K\). Then the polynomial \(P\)
in (3) splits completely over \(\mathbb Q_q\).

Fix \(i\in\{1,\ldots,r\}\), put \(b_j=Kj\), and substitute

\[
T=-i+b_i u.
\]

The secular equation becomes

\[
H_i(u)=u^2-1-
 \sum_{j\ne i}\frac{b_j^2u^2}{(j-i+b_i u)^2}=0.  \tag{11}
\]

Multiply (11) by \(\prod_{j\ne i}(j-i+b_i u)^2\). This gives an integer
polynomial whose reduction modulo \(q\) is

\[
C_i(u^2-1),\qquad C_i=\prod_{j\ne i}(j-i)^2\ne0\pmod q.
\]

Both \(u=1\) and \(u=-1\) are simple roots modulo \(q\). Hensel's lemma
therefore gives roots \(u_+,u_-\in\mathbb Z_q\) in these residue classes.
All denominators in (11) are units, and \(u_\pm\ne0\). Thus

\[
T_{i,\pm}=-i+b_i u_\pm
\]

are roots of \(P\). The pair for one \(i\) is distinct because \(b_i\ne0\)
and \(u_+\ne u_-\). The pairs for different \(i\)'s have different residues
modulo \(q\). We have found \(2r\) distinct roots, proving the lemma.

The polynomial \(P\bmod q=F^2\) is not squarefree. Therefore it would be
incorrect to justify this splitting by a squarefree-reduction test. The
rescaling around each pole in (11) is essential.

## 3. Several blocks with independent fields

Choose increasing primes

\[
p_1<\cdots<p_h,\qquad p_i\equiv1\pmod4,
\]

and put \(r_i=p_i-1\). For each \(i\), select
\(1\le\kappa_i<p_i\) with \(\kappa_i^2\equiv-1\pmod{p_i}\).
Let

\[
L_i=\prod_{j>i}p_j,
\qquad 1\le t_i<p_i^2,
\qquad L_it_i\equiv1\pmod{p_i^2},
\qquad K_i=\kappa_iL_it_i.                       \tag{12}
\]

The empty product is one. For each block construct (1) with parameters
\((p_i,r_i,K_i)\), and denote its multiplier, value, and field by
\(\lambda_i,v_i,E_i=\mathbb Q(\lambda_i)=\mathbb Q(v_i)\).

Each \(P_i\) is Eisenstein at its own prime \(p_i\). For \(j<i\), we have
\(p_i>r_j\) and \(p_i\mid K_j\). By Section 2, \(P_j\) splits over
\(\mathbb Q_{p_i}\). Consequently the compositum of the earlier splitting
fields embeds in \(\mathbb Q_{p_i}\), and so does
\(E_1\cdots E_{i-1}\). Under such an embedding, \(P_i\) is still its
rational Eisenstein polynomial and is irreducible over
\(\mathbb Q_{p_i}\). It must therefore be irreducible over the embedded
earlier compositum. Induction gives

\[
[E_1\cdots E_h:\mathbb Q]
 =D:=\prod_{i=1}^h2r_i.                           \tag{13}
\]

This proves linear disjointness in the degree-product sense needed here.
Pairwise trivial intersections alone would not have justified (13).

Now take the product of the \(h\) unit balls and sum the objectives with
any strictly positive rational weights. Its unique optimizer consists of
the block optimizers, so its joint field has degree \(D\). Its \(h\)
constraint Hessians have disjoint nonempty diagonal supports and are
linearly independent. Thus the native constraint Hessian span is exactly
\(h\). The objective is positive definite, the feasible set is compact, and
zero satisfies every constraint strictly.

## 4. A short weighting whose value is primitive

Let \(E=E_1\cdots E_h\), which has degree \(D\), and recall that the
individual \(v_i\)'s generate \(E\). Distinct embeddings
\(\sigma,\tau:E\to\mathbb C\) differ on some \(v_i\), so

\[
\sum_{i=1}^h T^{i-1}\bigl(\sigma(v_i)-\tau(v_i)\bigr)
\]

is a nonzero polynomial of degree at most \(h-1\). There are at most
\(D(D-1)/2\) unordered pairs of embeddings. Therefore at most
\((h-1)D(D-1)/2\) integers cause any collision. Some integer

\[
1\le t\le1+\frac{(h-1)D(D-1)}2                  \tag{14}
\]

makes

\[
v=\sum_{i=1}^h t^{i-1}v_i
\]

have \(D\) distinct conjugates. In particular \(\mathbb Q(v)=E\).
Use the positive weights \(t^{i-1}\) in the QCQP objective. The optimizer
is unchanged, and its objective value now has degree \(D\).

Equation (14) proves existence of a short integer weight. It is not an
algorithm for finding such a weight in time polynomial in the QCQP input:
the degree \(D\), and the number of candidate weights, can be very large.
The block coefficients and block fields in Sections 1–3 are explicit;
this choice of primitive weighting is an existence statement with an
explicit bit bound. The next construction finds a larger weight directly.

### 4.1. A deterministic weight with polynomial bit length

The finite search can be avoided by an elementary root-separation bound.
Write \(P_{\max}=p_h\), \(K_{\max}=\max_iK_i\), and define integers

\[
C=4K_{\max}^2(P_{\max}+1)^{2P_{\max}+4},\qquad
s=3P_{\max}+1,\qquad d=2P_{\max},
\]

\[
H=s\bigl(\lceil\log_2s\rceil+\lceil\log_2C\rceil\bigr)+1,
\qquad
t=1+2^{(H+2)d^2+H+3}.                            \tag{17}
\]

Then the weighted optimal value \(\sum_i t^{i-1}v_i\) generates the full
field \(E\).

To prove this, consider the block value \(\beta_i=2v_i\). Suppressing the
block index, define

\[
A(T)=F(T),\qquad
B(T)=-TF(T)-K^2\sum_{j=1}^rj^2F_j(T),
\]

so that \(\beta=B(\lambda)/A(\lambda)\). The integer polynomial

\[
R(Y)=\operatorname{Res}_T(P(T),YA(T)-B(T))          \tag{18}
\]

has degree \(2r\) in \(Y\). Indeed \(P\) is monic, and
\(P(-j)=-K^2j^2F_j(-j)^2\ne0\), so the product formula for the resultant
has \(2r\) nonzero linear factors in \(Y\). By Section 1.2,
\(\deg_{\mathbb Q}\beta=2r\). Hence \(R\) is a nonzero integer multiple of
the primitive integer minimal polynomial of \(\beta\).

The coefficient \(\ell_1\)-norm of \(F\) is \(\prod_{j=1}^r(1+j)\).
The inequalities \(r<P_{\max}\), \(K\le K_{\max}\), and
\(\sum_jj^2\le P_{\max}^3\) therefore give

\[
\|P\|_1\le C,\qquad \|A\|_1+\|B\|_1\le C.
\]

The Sylvester determinant in (18) has size \(3r+1\le s\), and each entry
has coefficient norm at most \(C\), as a polynomial in \(Y\).
Consequently

\[
\|R\|_1\le s!C^s\le2^H.
\]

Dividing the integer content does not increase this bound for the primitive
minimal polynomial. Cauchy's bound gives modulus at most
\(M=2^{H+1}\) for every conjugate of every \(\beta_i\).

For any integer squarefree polynomial of degree \(d_i\le d\) and
coefficient height at most \(2^H\), its discriminant is a nonzero integer.
In the discriminant product, bound the leading coefficient by \(2^H\)
and every root difference except a chosen pair by \(2M\). This gives the
conservative separation bound

\[
|\alpha-\alpha'|\ge
\delta:=2^{-(H+2)d^2}                             \tag{19}
\]

for distinct conjugates of one \(\beta_i\). More explicitly, the reciprocal
bound from the product is
\((2^H)^{d_i-1}(2M)^{d_i(d_i-1)/2-1}\), which is at most
\(2^{(H+2)d^2}\).

Take distinct embeddings \(\sigma,\tau:E\to\mathbb C\), and let \(j\) be
the largest index where they differ on \(\beta_j\). The \(j\)-th term of
their weighted difference has modulus at least \(\delta t^{j-1}\).
The sum of all earlier terms has modulus at most

\[
2M\sum_{i<j}t^{i-1}<
\frac{2M}{t-1}t^{j-1}<\delta t^{j-1};
\]

if \(j=1\), there are no earlier terms. The last strict inequality follows
from (17). Thus the weighted sum separates every pair of embeddings and
generates \(E\). Multiplication by the rational number \(1/2\) gives the
same conclusion for the weighted sum of the \(v_i\)'s.

This weight is computable by integer arithmetic directly from the block
parameters. Its bit length satisfies

\[
\log t=
O\!\left(P_{\max}^4\log P_{\max}
       +hP_{\max}^3\log P_{\max}\right).
\]

The coefficient bit lengths after weighting are larger than those obtained
by (14), but remain polynomial in \(P_{\max}\) and \(h\), with an exponent
independent of \(h\).

## 5. Input size and the exponent in the span parameter

Write \(P=p_h\) and \(n=\sum_i r_i\). Formula (12) gives

\[
\log K_i=O(h\log P).
\]

Also \(\log D=O(h\log P)\), so (14) gives
\(\log(t^{i-1})=O(h^2\log P)\). Every coefficient of the weighted QCQP
therefore has \(O(h^2\log P)\) bits. In a conventional dense encoding of
the \(h+1\) quadratic forms, its total bit length is at most

\[
N=O\bigl((h+1)n^2\,[1+h^2\log P]\bigr),        \tag{15}
\]

with harmless additional index and dimension bits. Sparse encoding is
smaller. The arithmetic construction does not hide a coefficient whose
bit length grows like the degree product.

For example, choose the \(h\) primes in an interval \([R,2R]\). Then

\[
h(R-1)\le n<2hR,
\qquad D\ge[2(R-1)]^h\ge(n/(2h))^h\quad(R\ge2). \tag{16}
\]

For every fixed \(h\), arbitrarily large such intervals contain \(h\)
primes congruent to one modulo four, by the prime number theorem in
arithmetic progressions. More uniformly, the number of these primes in
\([R,2R]\) is asymptotic to \(R/(2\log R)\), so taking \(R\) sufficiently
large with \(h\le cR/\log R\) suffices for an absolute \(c>0\).

Equations (15)–(16) rule out a universal algebraic-degree upper bound of
the form \(f(h)N^C\), for any fixed constant \(C\) and arbitrary finite
function \(f\). Indeed, for fixed \(h>2C\) and arbitrarily large \(R\), the
lower bound grows as \(R^h\), while \(N^C=O_h(R^{2C}(\log R)^C)\).
The same conclusion holds for the length of a dense coefficient list for
the minimal polynomial of the optimal value.

The fully deterministic weight in (17) gives the same obstruction. For
fixed \(h\), its dense input length is \(O_h(R^6\log R)\), so choosing
\(h>6C\) and letting \(R\) grow again contradicts any proposed bound
\(f(h)N^C\). The sharper estimate (15) uses the shorter existential weight
from (14).

This is an output-representation obstruction. It does not rule out an
algorithm running in \(f(h)N^C\) time when its output is a compact sum of
separately represented algebraic numbers, nor does it establish a lower
bound for decision, comparison, or approximate optimization.

## 6. Every constraint can have a positive definite Hessian

The block constraints are convex but have zero curvature on the other
blocks. An explicit rational perturbation removes those zero directions
while preserving the optimizer and value. For \(h=1\) no change is needed.
Suppose \(h\ge2\), and write \(w_i=t^{i-1}\) for either positive weighting
above. Let

\[
L=K_{\max}P_{\max}^2,\qquad
\eta=\frac1{2h w_hL}.
\]

Replace the \(h\) unit-ball constraints by

\[
g_i(x)=\|x_i\|^2+\eta\sum_{j\ne i}\|x_j\|^2
             -1-\eta(h-1)\le0,\qquad 1\le i\le h. \tag{20}
\]

Every Hessian is positive definite. The row-mixing matrix
\(M=(1-\eta)I+\eta\mathbf1\mathbf1^T\) is invertible, so their span
still has dimension exactly \(h\). Zero remains strictly feasible, and
each individual quadratic sublevel is compact.

For the unweighted block multipliers, (2) gives the elementary bounds

\[
1<\lambda_i<K_i\sqrt{\sum_{j=1}^{r_i}j^2}<L.       \tag{21}
\]

For the lower bound, the secular sum at \(\lambda=1\) is at least
\(r_iK_i^2/4\ge4\): every \(\kappa_i\ge2\), and \(K_i\ge2\).
The upper bound follows by replacing \(j+\lambda_i\) in the denominator
by \(\lambda_i\).

At the original optimizer every block norm is one, so every constraint
in (20) is active. Set \(a_i=w_i\lambda_i\) and \(S=\sum_i a_i\).
The Lagrangian \(f+\frac12\sum_i\mu_i g_i\) is stationary there when
\(M\mu=a\). Explicitly,

\[
\mu_i=\frac{a_i-\eta S/[1+\eta(h-1)]}{1-\eta}>0,   \tag{22}
\]

because \(a_i>1\), while \(S<hw_hL\) implies \(\eta S<1/2\).
Thus the original optimizer satisfies the convex KKT conditions for
the modified QCQP. Strict convexity of its objective makes it the unique
optimizer. Its value and all algebraic degrees are unchanged.

The bit length of \(\eta\) is \(O(\log h+\log w_h+\log L)\), so this
modification preserves both polynomial input-size bounds. It changes the
feasible set; the KKT argument proves that the particular optimizer is
preserved, without asserting equality of feasible sets.

## 7. Prior results, scope, and verification

Nie and Ranestad's generic QCQP degree formula gives \(2^s\binom ns\)
for \(s\) generic active quadratics. In particular its one-constraint
specialization is \(2n\); that numerical degree is not new. The present
single-block construction realizes it with explicitly small integer
coefficients, and the congruences in (12) control how the block fields
combine. The companion effective Hilbert construction proves the same
output-size obstruction for unrestricted block dimensions. The additional
point here is direct coefficient generation using congruences and the
deterministic weighting (17). See
[their paper](https://arxiv.org/abs/0802.1233) and the
[generic sharpness comparison](multihomogeneous-degree-sharpness.md).

The secular equation and its degree-\(2n\) polynomial reduction are also
standard in trust-region methods. See equations (1.6), (2.5), and Section
3.2 of [Adachi–Iwata–Nakatsukasa–Takeda's author manuscript](https://people.maths.ox.ac.uk/nakatsukasa/publishedpdf/TRSrev2rev.pdf).
An independent source reviewer checked these passages and earlier
Forsythe–Golub material; the detailed comparisons and their limits are in
[the adversarial review](short-input-degree-adversarial-review.md).

Eisenstein irreducibility and total ramification are classical; a source
stating both is Theorem 3.7.6 of
[Mascot's algebraic number theory notes](https://www.maths.tcd.ie/~mascotn/teaching/2022/MAU34109/Poly.pdf).
The modular roots used in Section 2 are simple, so only the usual simple-root
form of Hensel's lemma is needed. The prime counting statement in Section 5
is the classical prime number theorem for arithmetic progressions, stated
in [Elkies's analytic number theory course notes](https://people.math.harvard.edu/~elkies/M229.26/index.html);
the displayed formula for fixed coprime modulus and residue was inspected.

Searches on 2026-09-27 combined “trust-region subproblem,” “algebraic degree,”
“secular polynomial,” “irreducible,” and “Eisenstein.” They did not locate
an equivalent explicit block construction. This limited unsuccessful
search does not establish novelty. A wider audit of arithmetic examples
for trust-region problems and algebraic optimization remains necessary
before making a publication novelty claim.

Independent proof checks are recorded in
[the secular construction review](secular-eisenstein-review.md) and
[the adversarial review](short-input-degree-adversarial-review.md).
The former documents both the reviewer's contributions and the subsequent
fresh checks. Its Section 5 checks the constructive weighting, which was
outside the latter review's scope.

The targeted command
`python research-20260927/check_secular_eisenstein.py` passed. It checks
the Eisenstein and value-series identities for primes \(5,13,17,29,37\),
an exact irreducible degree-eight value resultant, and five-digit Hensel
branches for three pairs in the CRT construction with primes \(5,13,17\).
These finite tests support the formulas; the general degree and
coefficient bounds rely on the displayed proofs. Targeted document checks
also passed for local links, math delimiters, whitespace, and control
characters. No project-wide verification, CI inspection, or Lean proof
was performed for this construction.
