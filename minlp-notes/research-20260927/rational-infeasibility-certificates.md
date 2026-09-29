# Rational infeasibility certificates for convex quadratic systems

Date: 2026-09-27. Status: complete proof;
[independent adversarial review](rational-infeasibility-review.md) found
no mathematical gap after a characteristic-polynomial wording correction.
A [separate primary-source audit](rational-infeasibility-prior-review.md)
confirmed the prior alternatives and independently developed the stronger
encoding lower bound below. Publication priority remains unestablished.
This is a certificate refinement of the Hessian-span
results, not a new theorem of alternatives or a new complexity classification.

An infeasible rational system of native convex quadratic inequalities admits
a positive quadratic aggregate with rational coefficients and rational
multipliers. At fixed Hessian-span dimension, the entire certificate has
polynomial binary length. Checking it requires only rational arithmetic and
positive semidefiniteness of the rational input matrices. Algebraic numbers
are needed in the size proof, but not in the final certificate.

## 1. Statement and certificate format

Consider an infeasible system

\[
 f_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i\le0
                       \quad(i=1,\ldots,m),\qquad x\in\mathbb R^n,
                                                               \tag{1}
\]

with rational data and \(Q_i\succeq0\). Include every affine
inequality as a zero-Hessian row and every affine equality as two opposite
rows. Let \(N\ge2\) be the explicit binary input length, and let

\[
                 h=\dim_{\mathbb Q}\operatorname{span}\{Q_i\}.
\]

**Theorem.** There are rational weights \(w_i\ge0\) with
\(\sum_iw_i=1\), at most \(n+1\) of them positive, a rational vector
\(z\), and a positive rational number \(\gamma\) such that

\[
 \sum_iw_if_i(x)=\gamma+\tfrac12(x-z)^TH(x-z),
 \qquad H=\sum_iw_iQ_i\succeq0.                    \tag{2}
\]

The total bit length of these objects is \(N^{O(h+1)}\). In particular,
for fixed `h` this is a polynomial-size rational certificate of infeasibility.
It is checked in polynomial time in the input and certificate lengths.

More explicitly, a verifier forms

\[
 H=\sum_iw_iQ_i,\qquad b=\sum_iw_ia_i,\qquad c=\sum_iw_ic_i,
\]

and checks

\[
 w\ge0,\quad\sum_iw_i=1,\quad Hz=-b,\quad
              \gamma=c+\tfrac12b^Tz>0.             \tag{3}
\]

The rational identity (2) follows by expansion. The input PSD assumptions
imply \(H\succeq0\); they can themselves be checked by exact rational
linear algebra. A feasible point would make the left side of (2)
nonpositive and the right side positive.

The theorem concerns existence and encoding size. Once a common-field
positive aggregate is supplied, the conversion below constructs the rational
certificate in time polynomial in its encoding and the displayed bounds.
This note does not separately prove a polynomial-time procedure for
extracting those initial aggregate multipliers from a primal optimum.
The already established fixed-`h` decision algorithm is not needed by the
verifier.

## 2. A positive aggregate of controlled algebraic height

Treating affine rows as part of (1) lets us use the infeasibility argument
from [the algebraic certificate note](algebraic-primal-dual-certificates.md)
with no separate polyhedral constraints. The epigraph problem

\[
 \alpha=\min\{t:f_i(x)-t\le0\text{ for every }i\}              \tag{4}
\]

has a finite, nonnegative infimum. Its objective and native Hessians are
positive semidefinite. Classical convex quadratic attainment gives a
minimizer, and infeasibility of (1) forces \(\alpha>0\). The
epigraph has strict feasibility, since `t` can be increased at any fixed
`x`. Convex KKT therefore supplies weights with

\[
 w_i^*\ge0,\quad\sum_iw_i^*=1,\quad
 \sum_iw_i^*\nabla f_i(\bar x)=0,\quad
 w_i^*(f_i(\bar x)-\alpha)=0.                       \tag{5}
\]

Choose the canonical minimum-norm epigraph optimizer
\((\bar x,\alpha)\), and choose a basic solution of its active multiplier
system. The latter has `n+1` equations, including normalization. Thus
at most \(n+1\) weights are positive, and every weight belongs to
\(K=\mathbb Q(\bar x,\alpha)\). The previously proved field and
height bounds give

\[
 [K:\mathbb Q]\le
 \mathcal B(n+1,h):=\max_{0\le s\le\min(h,n+1)}2^s\binom{n+1}{s},
 \qquad H(w_i^*),H(\alpha)\le N^{O(h+1)},           \tag{6}
\]

where `H` on numbers denotes absolute logarithmic Weil height. The field
degree uses [the sharp degree refinement](multihomogeneous-span-degree.md);
the coefficient-height bound uses
[ordered perturbations](ordered-perturbation-optimizer.md) and the basic
multiplier argument already reviewed in the certificate note.

Let \(I=\{i:w_i^*>0\}\), and keep only these rows. The aggregate

\[
 g_*(x)=\sum_{i\in I}w_i^*f_i(x)
\]

has global minimum \(\alpha>0\) at \(\bar x\). For any nonzero
\(\beta\in K\), absolute height gives
\(|\beta|\ge\exp(-[K:\mathbb Q]H(\beta))\) at the intended
real embedding. Consequently, for

\[
                  \omega=\min_{i\in I}w_i^*>0,
\]

there is an effective uniform bound

\[
                   \omega,\alpha\ge2^{-N^{O(h+1)}}.          \tag{7}
\]

If an aggregate with additional polyhedral normal multipliers is used
instead, include the corresponding affine rows among the `f_i` and divide
all weights and the positive margin by their positive total. Absolute
height preserves the same asymptotic bounds. Formulation (4) avoids that
extra normalization step.

## 3. Preserve the exact kernel equations while rounding

For weights that are strictly positive on `I`, positive semidefiniteness
implies

\[
 \ker\Bigl(\sum_{i\in I}w_iQ_i\Bigr)
              =\bigcap_{i\in I}\ker Q_i=:W.         \tag{8}
\]

Indeed, a vector has zero quadratic form in the weighted sum if and only
if it has zero quadratic form in every positively weighted PSD matrix.
The subspace `W` is rational and depends only on the support, not on the
positive weights. It has a rational basis of polynomial bit length in
`N`, obtained from the kernel of the rational matrix
\(Q=\sum_{i\in I}Q_i\).

Write \(b(w)=\sum_iw_ia_i\) and \(c(w)=\sum_iw_ic_i\). The
aggregate has finite minimum exactly when \(b(w)\perp W\). If this
orthogonality fails, its affine term decreases without bound on a kernel
line. If it holds, its restriction to \(W^\perp\) has positive
definite Hessian and hence an attained finite minimum.

Therefore round inside the rational affine space

\[
 \Lambda=\{w\in\mathbb R^I:\sum_iw_i=1,
                            b(w)\perp W\}.         \tag{9}
\]

It contains \(w^*\). Arbitrary independent rounding of the weights is
not sufficient: it may violate the exact equations in (9), making an
otherwise nearby quadratic unbounded below. Every rounding below preserves
(9) exactly and preserves the positive support.

All coefficients of (9) have polynomial bit length in `N`. Rational
Gaussian elimination gives

\[
                         w=w_0+Vu,                 \tag{10}
\]

where \(w_0,V\) have polynomial bit length and the entries of `u` can
be chosen to be a subset of the original weight coordinates. At \(w^*\),
these free coordinates lie in \([0,1]\). Rounding them to a dyadic
grid of mesh \(2^{-p}\) and then evaluating (10) gives a rational
\(\widehat w\in\Lambda\) with

\[
 \|\widehat w-w^*\|_1\le2^{\operatorname{poly}(N)-p},
 \qquad\operatorname{bits}(\widehat w)\le\operatorname{poly}(N)+O(p).
                                                               \tag{11}
\]

The statement includes the case of no free coordinates, where (10) is
already a rational singleton. The next section bounds how accurate this
rounding must be to preserve a positive global minimum.

## 4. A controlled neighborhood of positive aggregates

First suppose \(Q\ne0\), and let \(\rho>0\) be its smallest
positive eigenvalue. Since `Q` is a rational PSD matrix with polynomial
coefficient bits,

\[
                         \rho\ge2^{-\operatorname{poly}(N)}. \tag{12}
\]

One elementary proof clears a common denominator, notes that the product
of the positive eigenvalues is a positive coefficient of
\(\det(tI+Q)\) with a polynomial-bit rational denominator, and bounds the
other eigenvalues by the trace. Its logarithmic lower bound is polynomial
in the matrix dimension and coefficient bits; no choice of an irrational
eigenbasis is encoded.

Let \(V_0=W^\perp\), considered only as a Euclidean subspace, and put

\[
             \eta=\min(1,\omega\rho)
                         \ge2^{-N^{O(h+1)}}.         \tag{13}
\]

The Hessian \(H_*=\sum_iw_i^*Q_i\) obeys
\(H_*|_{V_0}\succeq\eta I\), since \(H_*\succeq\omega Q\).
If \(\|\widehat w-w^*\|_1\le\omega/2\), every retained weight
is at least \(\omega/2\), so
\(\widehat H|_{V_0}\succeq(\eta/2)I\) and its kernel is still
exactly `W`.

Choose a rational \(M\ge1\) bounding every \(\|Q_i\|_2\),
\(\|a_i\|_2\), and \(|c_i|\), with \(\log M\le\operatorname{poly}(N)\).
Positive normalized weights give \(\|b(w)\|\le M\). For
\(\varepsilon=\|\widehat w-w^*\|_1\), the changes in the Hessian,
linear term, and constant have norms at most \(M\varepsilon\).
Their minimum values are

\[
 \nu(w)=c(w)-\tfrac12b(w)^T
                    (H(w)|_{V_0})^{-1}b(w).        \tag{14}
\]

Equation (9) places both linear terms in `V_0`. The identity for the
difference of two inverses gives

\[
 \|\widehat H^{-1}-H_*^{-1}\|_{V_0}
                \le 2M\varepsilon/\eta^2.
\]

Expanding the difference in (14), and using inverse norm bounds
\(1/\eta\) and \(2/\eta\), yields

\[
 |\nu(\widehat w)-\nu(w^*)|
 \le\left(M+\frac{2M^2}{\eta}+\frac{M^3}{\eta^2}\right)
                                     \varepsilon
 \le\frac{4M^3}{\eta^2}\varepsilon.                \tag{15}
\]

Thus it is enough to choose

\[
 \varepsilon\le
       \min\left(\frac\omega4,\frac{\alpha\eta^2}{16M^3}\right).
                                                               \tag{16}
\]

Then the support remains positive and
\(\nu(\widehat w)\ge3\alpha/4>0\). Equations (7), (12), and
(13) show that the reciprocal logarithm of the required accuracy is
\(N^{O(h+1)}\). Equation (11) achieves it with
\(p=N^{O(h+1)}\) and hence weights of the claimed bit length.

If \(Q=0\), every supported Hessian is zero, and (9) enforces
\(b(w)=0\) exactly. The aggregate is the constant \(c(w)\).
Its change is at most \(M\varepsilon\), so it suffices to choose
\(\varepsilon\le\min(\omega/4,\alpha/(4M))\). This includes
purely affine infeasibility and has the same bit bound.

## 5. Recover the rational center and verify the certificate

The rounded aggregate has rational coefficients \(\widehat H\),
\(\widehat b\), and \(\widehat c\), with coefficient bit lengths
\(N^{O(h+1)}\). Its kernel is `W` and \(\widehat b\perp W\).
The rational linear system

\[
                         \widehat H z=-\widehat b             \tag{17}
\]

is consistent. Choose a rational solution by Gaussian elimination, setting
free coordinates to zero. Cramer's rule bounds its bit length by a
polynomial in the matrix dimension and coefficient bits, hence still
\(N^{O(h+1)}\). In the all-affine case choose \(z=0\).
Set

\[
                    \gamma=\widehat c+\tfrac12\widehat b^Tz.
\]

This is the positive global minimum proved in Section 4 and is rational
with the same bit bound. Identity (2) follows exactly. These are all the
objects needed by the verifier; it does not receive or check the field
used in the existence proof, a kernel-rounding argument, a spectral bound,
or a Slater condition.

The proof also gives a polynomial conversion algorithm when the initial
positive aggregate is supplied in one isolated real field: compute its
positive support and the rational kernel, choose a sufficient precision
from field degree/height bounds, approximate its free weights, round them,
and solve (17). Exact field sign and approximation routines select the
positive support. A guard precision finer than the chosen dyadic mesh
ensures the error estimate even if a free coordinate is exactly a grid
midpoint. This conditional conversion is distinct from finding the initial
aggregate.

## 6. Exponential dependence on the span can be necessary

For \(h\ge1\), consider the infeasible system in \(h\) variables
\[
 f_0(x)=\tfrac12-x_1\le0,\qquad
 f_i(x)=x_i^2-x_{i+1}\le0\quad(1\le i<h),\qquad
 f_h(x)=x_h^2\le0.                                  \tag{18}
\]
The last row forces \(x_h=0\), and induction backwards forces
\(x_1=0\), contradicting the first row. Its quadratic Hessians are
independent diagonal matrices, so their span has dimension `h`. The
explicit dense input length is polynomial in `h`; the number of nonzero
coefficients is linear in `h`.

At the rational point \(y_i=2^{-2^{i-1}}\), every row except the last
vanishes and \(f_h(y)=2^{-2^h}\). Consequently every normalized
nonnegative aggregate with positive minimum \(\gamma\) satisfies
\[
 0<\gamma\le\sum_{i=0}^h w_i f_i(y)
                  =w_h2^{-2^h}\le2^{-2^h}.          \tag{19}
\]
If \(\gamma=p/q>0\) is recorded as an ordinary rational number,
then \(p\ge1\) and \(q\ge2^{2^h}\). The denominator alone needs
at least \(2^h+1\) binary digits. Thus polynomial bit length independent
of `h` is impossible for this normalized explicit certificate format.

There is also a lower bound on the weights themselves, independent of
normalization or an explicitly recorded margin. In \(h+1\) variables,
use the infeasible system
\[
 f_0=\tfrac12-x_1\le0,\qquad
 f_i=x_i^2-x_{i+1}\le0\quad(1\le i\le h),\qquad
 f_{h+1}=x_{h+1}\le0.                               \tag{20}
\]
Its Hessian span is `h`. Suppose \(g=\sum_{i=0}^{h+1}\lambda_i f_i\)
is strictly positive everywhere, with rational \(\lambda_i\ge0\).
Evaluation at zero forces \(\lambda_0>0\). Put \(d=2^h\) and
evaluate on \(x_i=t^{2^{i-1}}\) at \(t=(1+1/d)/2\). All the
intermediate rows vanish, while the first is \(-1/(2d)\) and the
last is \(2^{-d}(1+1/d)^d<3\cdot2^{-d}\). Hence
\[
              \frac{\lambda_{h+1}}{\lambda_0}
                         >\frac{2^{d-1}}{3d}.       \tag{21}
\]
Writing \(\lambda_0=p_0/q_0\) and
\(\lambda_{h+1}=p_1/q_1\) with positive integer numerators and
denominators gives
\(p_1q_0>2^{d-1}/(3d)\), since \(p_0q_1\ge1\).
Their binary encodings alone need at least \(d-O(\log d)=\Omega(2^h)\)
bits. Common scaling cannot avoid this ratio bound.

These are lower bounds for rational positive-aggregate certificates, not
for arbitrary infeasibility proofs, arithmetic circuits, or the complexity
class coNP. Both chains have short symbolic infeasibility proofs. The
examples show why the dependence on a structural parameter and the
certificate encoding must both be stated.

## 7. Prior results, significance, and limits

The existence of a real positive aggregate is an explicit special case of
[Jeyakumar--Li, Theorem 2.5](https://web.maths.unsw.edu.au/~gyli/papers/jl-zero-sum-final-18-07-13.pdf),
which applies to SOS-convex inequalities and bounds the degree of the SOS
remainder by the input polynomial degree. It already covers PSD quadratics.
The present proof does not claim that alternative as new. The
[certificate prior-art audit](algebraic-certificate-prior.md) records
that source and the broader exact-duality literature.

Safey El Din--Zhi's
[Theorem 1.1 on rational points in convex semialgebraic sets](https://arxiv.org/pdf/0910.2973)
gives rational point bit bounds controlled by the total number of variables
and polynomial degrees. It can be applied to an aggregate-certificate
spectrahedron once rational existence is known. Its parameter is not the
native Hessian span: the number of weights, or even the number of aggregate
Hessian and affine coefficients, may grow with the ambient dimension.
The fixed-span estimate here therefore still needs the margin and
kernel-preserving rounding argument.

The rationalization uses a special property of a positive combination of
native PSD Hessians: its kernel is the rational, support-dependent space
in (8). General rational semidefinite programs can lack rational separating
certificates, as discussed by
[Naldi--Sinn, Section 3.2](https://www.unilim.fr/pages_perso/simone.naldi/papers/2018_naldi_sinn.pdf).
Consequently, this proof cannot be transferred to arbitrary conic systems
by an assertion that real certificates can always be rounded. It preserves
the precise rational equations required for a finite quadratic minimum.

Rational density in (9) and continuity of the minimum already prove
rational-certificate existence without a coefficient bound. That short
argument is a supporting observation. The parameter-sensitive addition is
the \(N^{O(h+1)}\) binary-size bound, obtained by controlling the
positive support, curvature, and positive margin before rounding. The
current literature search does not establish priority for this combined
statement.

The certificate can make infeasibility checking substantially simpler than
repeating an exact algebraic optimization calculation: only rational
quadratic identities remain. It is not a rational feasibility certificate,
and it does not apply to a convex continuous relaxation that is feasible
but has no integer point. Practical extraction algorithms and numerical
size remain separate questions. Fixed-`h` feasibility is already in P by
the local main theorem, so no additional NP/coNP classification is claimed.

Verification consists of complete symbolic proof review, independent
rechecking of the explicit perturbation constants, and exact rational
checks of the two chain families. The reviews record their targeted
`python -` commands, checked dimensions, and limits. These computations
check examples; they do not certify the universal theorem. No numerical
experiment, Lean formalization, project-wide test, or CI inspection was
performed.

The author also ran `python -` with an inline document checker on this
note, its two reviews, and the three algebraic-certificate notes. All 22
local links, paired math delimiters, final newlines, control characters,
and trailing-whitespace checks passed. This was a targeted document check,
not a project-wide mathematical verification.
