# Short rational instances with large algebraic degree

Date: 2026-09-27. Status: the source audit and the shifted secular-map
construction below have received independent review. A separate targeted
symbolic check is recorded at the end. The construction combines classical
covering-space and Hilbert irreducibility methods; no novelty claim is made
for those ingredients. The completed mathematical audit is recorded in
[the secular-map review](short-degree-secular-review.md).

The qualitative sharpness argument in
[the sharp-degree note](multihomogeneous-degree-sharpness.md) gives no
coefficient-size bound. That omission matters for a lower bound on the size
of an exact answer. A large algebraic degree by itself need not rule out a
fixed-parameter running time if the instance encoding is equally large.

**Short-instance theorem.** For every positive integers \(h,r\), there is a
rational strictly convex QCQP with \(hr\) variables and \(h\) convex
quadratic constraints such that:

- the feasible set is compact and has a strict feasible point;
- the constraint Hessian span has dimension exactly \(h\);
- the unique optimizer and its optimal value generate the same number
  field, of degree \((2r)^h\) over \(\mathbb Q\);
- the complete rational input has length \((hr)^{O(1)}\), with an absolute
  exponent.

The theorem is an existence statement with effective size bounds. It does
not give an efficient algorithm for finding the coefficients. Its degree
\((2r)^h\) is sufficient for the output-size consequence below; it does not
attain the sharper extremal formula in the companion note.

## 1. The group-sensitive specialization bound

Let \(P(T,Y)\in\mathbb Z[T,Y]\) be irreducible, with \(m=\deg_TP\ge1\),
\(d=\deg_YP\ge2\), coefficient height \(H\ge e^e\), and splitting group
\(G\) over \(\mathbb Q(T)\). Dèbes and Walkowiak, Theorem 3.3, bound the
number of reducible positive integral specializations up to \(B\) by

\[
 2^{165}m^{64}d^{148\operatorname{Hi}(P)}
 (\log H)^{19}B^{1/2}(\log B)^5.                         \tag{1}
\]

Their Section 4.1 gives
\(\operatorname{Hi}(P)\log d\le(\kappa+1)\log|G|\), for an absolute
constant \(\kappa\). Thus some irreducible specialization has

\[
 \log B=O\bigl(\log(m+2)+\log|G|+\log\log H\bigr).       \tag{2}
\]

The paper's Section 6.1 does not itself supply a uniform many-parameter
version. The construction below therefore uses one parameter from the
outset. [Dèbes–Walkowiak, primary PDF, Theorem 3.3 and Section 4.1](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/pierre_debes/A44-DebesWalkowiakHITBounds.pdf).

One can avoid the finite-group theorem quoted in their Section 4.1 if only
a polynomial bit bound is needed. Every subgroup of a group of order \(g\)
has at most \(\lfloor\log_2g\rfloor\) generators: adjoining an element
outside the subgroup already generated at least doubles its size. Hence
the number of subgroups is at most
\((1+\lfloor\log_2g\rfloor)g^{\lfloor\log_2g\rfloor}\). The sum of the
indices of all maximal proper subgroups is therefore at most
\(\exp(O((\log g)^2))\). This set covers all possible factorizations in
the definition of the Hilbert index. Substituting this elementary estimate
in (1) replaces \(\log|G|\) in (2) by \((\log|G|)^2\), which also suffices.

## 2. A small rational map with full symmetric monodromy

Choose positive integers \(b_i,d_i\), with the \(d_i\) distinct, and put

\[
 R(\lambda)=\sum_{i=1}^r\frac{b_i^2}{(\lambda+d_i)^2},
 \qquad A(\lambda)=\prod_{i=1}^r(\lambda+d_i).
\]

We first show that the integers can be chosen with \(O(\log(r+1))\) bits
so that all finite branch values of \(R:\mathbb P^1\to\mathbb P^1\)
are distinct and simply branched. The prescribed fiber over infinity
contains the \(r\) double poles. The finite branch values consist of zero,
coming from \(\lambda=\infty\), and the values at the roots of

\[
 C(\lambda)=\sum_i b_i^2\prod_{j\ne i}(\lambda+d_j)^3,
 \qquad R'=-2C/A^3.                                      \tag{3}
\]

The required open conditions hold for some positive real \(b_i,d_i\).
Here is an induction that checks this assertion rather than assuming a
generic rational map lies in this restricted family. For one pole there
is nothing to prove. Given a map with \(r-1\) poles, select a negative
real number \(a\), away from its poles, such that \(R'(a)\ne0\) and
\(R(a)\) is neither zero nor an existing finite branch value. Only finitely
many choices are forbidden. Add \(\varepsilon/(\lambda-a)^2\), with
\(\varepsilon>0\) small. The old simple critical points persist. Write
\(\varepsilon=t^3\), \(\lambda=a+tv\). The equation for a new critical
point becomes

\[
 v^3R'(a+tv)-2=0.
\]

At \(t=0\) it has three distinct nonzero roots. The implicit-function
theorem supplies three new simple critical points. Their critical values
have expansions

\[
 R(a)+\tfrac32tR'(a)v+O(t^2),
\]

with three distinct leading coefficients. They remain separate from one
another, from zero, and from all old critical values. Equation (3) has
degree \(3r-3\); the \(3r-6\) old and three new roots exhaust it. Also
\(R(\lambda)=(\sum b_i^2)\lambda^{-2}+O(\lambda^{-3})\) near infinity,
so the branch over zero remains simple.

This open condition has a polynomial witness of degree \(O(r^3)\) in
\((b,d)\). In detail, set

\[
 N(\lambda)=\sum_i b_i^2\prod_{j\ne i}(\lambda+d_j)^2,
 \quad
 Q(t)=\operatorname{Res}_{\lambda}(C,N-tA^2).
\]

Require distinct poles, nonzero residues, the correct leading coefficient
of \(C\), and
\(\operatorname{Disc}_{\lambda}C\ne0\),
\(Q(0)\ne0\), \(\operatorname{Disc}_tQ\ne0\).
The degree of \(Q\) in the parameters is at most \(12r^2-8r\), and
\(\deg_tQ=3r-3\). Discriminants therefore give the asserted \(O(r^3)\)
bound; harmless leading-coefficient factors can be included. The induction
proves that their product is not the zero polynomial. The elementary
polynomial grid lemma now supplies a point in
\(\{1,\ldots,O(r^3)\}^{2r}\) where it is nonzero. For \(r=1\), use
\(b_1=d_1=1\) directly.

The map has degree \(2r\), and its monodromy is transitive because its
source is connected. A loop about each finite branch value acts as a
transposition. These loops generate the entire monodromy group: the loop
about infinity is the inverse of their product. A transitive group generated
by transpositions is \(S_{2r}\). This last fact follows by forming a graph
whose edges are the generating transpositions; transitivity makes the graph
connected, and its edge transpositions generate the full symmetric group.
Thus the splitting field of \(R(\lambda)-T\) over
\(\overline{\mathbb Q}(T)\) has group \(S_{2r}\).

## 3. Independent blocks using one parameter

There are \(s=3r-2\) finite branch values, including zero. Set
\(K=(h-1)s^2\). Scale all \(b_i\) by one positive integer of
\(O(\log(h+1)+\log(r+1))\) bits so that \(R(0)>K+3\). Scaling preserves
all the branch properties just established. Choose integers

\[
 0\le a_1,\ldots,a_h\le K
\]

so that the finite branch sets of \(R(\lambda)=T+a_j\) are pairwise
disjoint. This is possible greedily: every earlier translate forbids at
most \(s^2\) values of the next shift, from the differences of two finite
branch values. Nonreal and nonintegral differences do not add integer
exclusions.

The splitting fields of these shifted maps are linearly disjoint over
\(\overline{\mathbb Q}(T)\). To prove this by induction, intersect the
next splitting field with the compositum of the preceding ones. Both are
Galois; a common subextension could ramify only where both extensions
ramify, hence only over infinity. In characteristic zero a nontrivial
connected cover of \(\mathbb P^1\) cannot branch only over infinity.
Indeed, for its degree \(e\), the ramification contribution of that fiber
is at most \(e-1\); Riemann–Hurwitz would give
\(2g-2\le-e-1\), forcing \(e=1\). Ramification does not appear at a new
place on taking a compositum of unramified extensions. This proves the
induction.

For the standard algebraic-geometric fact used here, see also the
characteristic-zero affine-line exercise following Riemann–Hurwitz in
[Vakil, *The Rising Sea*, Section 21.4](https://math.stanford.edu/~vakil/216blog/FOAGjul2724public.pdf).

Consequently the geometric splitting group is \((S_{2r})^h\). The
arithmetic group over \(\mathbb Q(T)\) contains this geometric group and
embeds in the same product, since each labeled block polynomial is rational.
It is therefore the same product, and the splitting fields are also
linearly disjoint over \(\mathbb Q(T)\).

## 4. A primitive optimal value

For \(1\le T\le2\), consider the separable QCQP

\[
 \begin{aligned}
 \min\quad&\sum_{j=1}^h\sum_{i=1}^r
       (d_i x_{ji}^2-2b_i x_{ji}),\\
 \text{subject to}\quad&\sum_{i=1}^r x_{ji}^2\le T+a_j,
          \qquad j=1,\ldots,h.
 \end{aligned}                                            \tag{4}
\]

The feasible set is a product of positive-radius balls, and zero is
strictly feasible. The objective Hessian is positive definite. Since
\(0<T+a_j<R(0)\), the unconstrained minimizer of every block is outside
its ball. Its positive multiplier \(\lambda_j\) is the unique positive
solution of \(R(\lambda_j)=T+a_j\), and

\[
 x_{ji}=\frac{b_i}{d_i+\lambda_j},
 \qquad
 \beta_j=-\sum_i\frac{b_i^2}{\lambda_j+d_i}
              -(T+a_j)\lambda_j.                         \tag{5}
\]

The same identities define the generic critical values in the function
fields. Differentiating (5) and using \(R(\lambda_j)=T+a_j\) gives
\(\beta_j'=-\lambda_j\). Every derivation of \(\mathbb Q(T)\) preserves
an algebraic intermediate field: implicit differentiation of the separable
minimal polynomial proves this. Hence
\(\mathbb Q(T,\beta_j)=\mathbb Q(T,\lambda_j)\), of degree \(2r\).

The unweighted sum \(\beta=\sum_j\beta_j\) generates the compositum of
these root fields. To see this, work in the product splitting field. If
\(g=(g_1,\ldots,g_h)\) fixes the sum, let
\(\delta_j=g_j\beta_j-\beta_j\). The equality
\(\delta_j=-\sum_{\ell\ne j}\delta_\ell\), and linear disjointness of
the splitting fields, imply \(\delta_j\in\mathbb Q(T)\). The automorphism
\(g_j\) fixes this difference, so iteration through its finite order gives
\(\delta_j=0\). The stabilizer of the sum is therefore the product of the
individual root stabilizers. Thus

\[
 [\mathbb Q(T,\beta):\mathbb Q(T)]=(2r)^h=:D.              \tag{6}
\]

This step avoids the incorrect inference that a sum of arbitrary
individually primitive elements must be primitive. The disjointness of
their **normal closures** is doing the work.

## 5. Coefficient bounds and rational specialization

The block-value polynomial can be bounded directly. Put
\(W(\lambda)=\sum_i b_i^2 A(\lambda)/(\lambda+d_i)\), and consider

\[
 H(t,Y)=\operatorname{Res}_{\lambda}
       (tA^2-N,(Y+\lambda t)A+W).                         \tag{7}
\]

Its degree in \(Y\) is \(2r\). Its leading coefficient is
\(t\operatorname{Res}_{\lambda}(tA^2-N,A)\): the second polynomial
has degree \(r+1\) in \(\lambda\), whereas its \(Y\)-coefficient
\(A\) has degree \(r\). The raw resultant is divisible by \(t\), since
both leading coefficients in \(\lambda\) vanish at \(t=0\), so the
homogeneous polynomials acquire a common root at infinity. Consequently
\(H/t\in\mathbb Z[t,Y]\) has leading coefficient
\(c=\operatorname{Res}_{\lambda}(tA^2-N,A)\), a nonzero integer
constant: evaluate \(tA^2-N\) at the roots \(-d_i\) of the monic
polynomial \(A\). Explicitly,
\(c=(-1)^r(\prod_i b_i^2)\prod_{i<j}(d_i-d_j)^4\ne0\).
Therefore a fixed nonzero integer multiple of every
\(\beta_j\) satisfies a monic polynomial over \(\mathbb Z[T]\).
The total degree of (7) is \(O(r^2)\), and its logarithmic coefficient
height is polynomial in \(r\) and \(\log(h+1)\). Dividing out \(t\)
does not increase either bound. These statements follow
from the Sylvester determinant, whose size and entry degrees are \(O(r)\).
The substitutions \(t=T+a_j\) preserve polynomial bounds.

Use the same integral scaling for all blocks, and write
\(\gamma_j=c\beta_j\), \(\gamma=\sum_j\gamma_j=c\beta\).
The minimal polynomial \(P(T,Y)\) of \(\gamma\) is monic and belongs to
\(\mathbb Z[T,Y]\). It has degree \(D\) in \(Y\), by (6). Its other
bounds can be obtained without constructing it:

\[
 \deg_TP\le D\,(hr)^{O(1)},\qquad
 \log H(P)\le D\,(hr)^{O(1)}.                            \tag{8}
\]

For completeness, each monic block polynomial has parameter degree at
most \(L=(hr)^{O(1)}\) and coefficient height at most
\(\exp((hr)^{O(1)})\). On the unit circle in \(T\), the elementary monic
root bound bounds every conjugate of every \(\gamma_j\) by
\(\exp((hr)^{O(1)})\). The elementary symmetric functions in the \(D\)
conjugates of their sum have the height estimate in (8), using Cauchy's
coefficient estimate on that circle. For large complex \(T\), the same
root bound gives growth \(O(|T|^L)\) for each conjugate. The coefficients
of \(P\), already known to be polynomials, consequently have degrees at
most \(DL\). This also proves the first estimate in (8).

The parameter degree is positive, as required in (1): on the optimizer
branch, \(\gamma'=-c\sum_j\lambda_j\ne0\). A minimal polynomial
independent of \(T\) would instead force \(\gamma'=0\).

Now substitute \(T=1+1/U\), clear powers of \(U\), and remove content.
This birational substitution preserves irreducibility over \(\mathbb Q(U)\)
and the splitting group. It leaves the logarithms of the degree bounds
and the double logarithm of the height bounded by \((hr)^{O(1)}\).
The group order is at most

\[
 ((2r)!)^h,\qquad \log|G|=O(hr\log(r+1)).
\]

Applying (1)–(2) supplies a positive integer \(u\) of \((hr)^{O(1)}\)
bits for which the specialized polynomial remains irreducible of degree
\(D\). There is no degree drop at a positive \(u\): before removing
content, the transformed leading coefficient is a power of \(U\), so its
content and its remaining leading coefficient also have only powers of
\(U\) as possible nonconstant factors.
The corresponding \(T=1+1/u\) lies in \((1,2]\), so all the
convexity and multiplier conditions for (4) hold. The nonzero rational
multiple \(c\beta\) of its true optimal value is a root of this irreducible
polynomial. Multiplication by \(c\in\mathbb Q^\times\) preserves the
generated field, so the optimal value has degree \(D\).

Every block optimizer is rational in \(\lambda_j\), and conversely
\(\lambda_j=b_i/x_{ji}-d_i\); the optimizer field therefore has degree
at most the product \((2r)^h\). It contains the optimal value, whose degree
equals that product, so both fields coincide. The \(h\) constraint
Hessians act on disjoint nonempty blocks and are linearly independent.
All coefficients and all matrix entries in a dense encoding of (4) have
total length \((hr)^{O(1)}\), as claimed.

The absolute exponent can be made explicit at this level of bookkeeping.
Write \(n=hr\). Then \(D=(2r)^h\le2^n\), so (8) and the birational
substitution give \(\log m,\log\log H=O(n)\). The elementary
subgroup-count estimate in Section 1 therefore gives
\(\log u=O(n^2\log^2(n+1))\). The original objective coefficients
need \(O(\log(n+1))\) bits; only the \(h\) right-hand sides use the long
denominator \(u\). Even a dense matrix encoding thus has length
\(O(n^3\log^2(n+1))\).

## 6. Consequence and limits

In an exact output format that writes a dense minimal polynomial for the
optimal value, no algorithm for convex QCQP can have running time
\(f(h)N^c\), for any function \(f\) and absolute constant \(c\), where
\(N\) is input length and \(h\) is the constraint Hessian-span dimension.
Indeed, the theorem gives \(N\le C(hr)^C\) for an absolute \(C\), while
that output has at least \((2r)^h+1\) coefficient positions. First choose
fixed \(h>Cc\), and then let \(r\) grow. This is an unconditional
**output-format** obstruction.

It does not rule out fixed-parameter feasibility or comparison algorithms,
approximation algorithms, or exact optimization with a more succinct
representation. Separate algebraic coordinates, a polynomial system, a
circuit, or a nested algebraic expression may be much shorter than a dense
primitive polynomial. No complexity-theoretic hardness assumption is used,
and no claim is made that finding the short instances is polynomial-time.

## 7. Other sources checked and verification

- Paredes–Sasyk, Theorem 1.1, gives a one-parameter exceptional-set estimate
  with a factor exponential in the polynomial degree. Directly using a
  degree-\((2r)^h\) polynomial therefore does not give the input-size bound
  needed above. Its group-preserving theorem also needs its degree
  dependence checked. [Primary paper](https://arxiv.org/abs/2202.10420).
- Cluckers and coauthors, Theorem 1.10, gives a many-parameter estimate
  whose displayed exponential degree factor and dimension-dependent
  constant do not directly provide the bound needed here. [Published
  paper](https://doi.org/10.1017/fms.2025.10096).
- An alternative route is a controlled restriction to an affine line.
  Kopparty–Saraf–Shpilka, Theorems 1.1–1.2, state a Kaltofen restriction
  theorem with a polynomial-degree obstruction for monic irreducible
  polynomials. It can be combined with the group-sensitive bound above,
  after bounding a primitive splitting-field polynomial. This alternative
  is not needed for the direct construction. [Author-hosted paper](https://www.math.utoronto.ca/swastik/pit-factor.pdf).

Independent reviewers checked the quoted specialization formulas,
the Morse-map induction, the grid degree bound, the branch-disjointness
argument, and primitivity of the unweighted value sum. One reviewer supplied
the latter simplification. Their review does not replace the proofs above.
The targeted symbolic check is documented in
[the check script](check_short_degree_secular.py). It checks small rational
maps and resultant identities; it does not establish the general
monodromy theorem or the effective Hilbert theorem. No project-wide or CI
verification was run for this note.

Commands actually run: `python research-20260927/check_short_degree_secular.py`
passed for \(r=1,2,3,4\). A targeted Python document check passed for the
two authored files, checking their three local links, final newlines,
trailing whitespace, and control characters.
