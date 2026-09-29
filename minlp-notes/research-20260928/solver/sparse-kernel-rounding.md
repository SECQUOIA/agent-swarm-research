# Sparse box certificates from consistent polynomial densities

Date: 2026-09-28. Research result with two independent proof reviews and
two prior-work audits. The proof below concerns the full local box
preordering, not the usual local quadratic module. Publication priority
remains unestablished.

## Candidate contribution and solver meaning

A sparse Schmüdgen moment relaxation on a junction tree can be rounded to
an actual probability distribution on the full box. The rounding first
turns every local pseudoexpectation into a nonnegative polynomial density.
The same polynomial kernel is used in every bag, so shared moments become
exactly equal shared marginal densities. Junction-tree gluing then produces
one global distribution. No local representing-measure assumption is needed.

For a fixed polynomial objective this gives error of order `r^-2` at moment
order `r`, with constants depending on local objective coefficients and the
largest bag size. This is stronger than the inspected published bound of
Korda, Magron and Ríos-Zertuche, Theorem 6, whose rate is
`r^(-2/(w+3))` for largest bag size `w`. However, Magron's July 2025
and February 2026 author presentations already publicly state the
inverse-square sparse preordering rate for two bags. Their difference
from the published theorem remains unresolved. **The rate itself must
not be described as first established here.**

The positive polynomial kernel and its dense convergence role are established
tools. This self-contained argument supplies compatible sparse moment
rounding, explicit constants, and finite extraction. Whether those details
add to the presentations' underlying argument remains to be checked.

The theorem provides sparse global lower bounds with an accuracy order
matching the established dense box preordering rate. It supplies no running
time claim for generic MINLP, no comparable result for arbitrary hard local
constraints, and no automatic conclusion for sparse Putinar relaxations.

## 1. Model and hierarchy

Let `B_1,...,B_t` be bags in a tree `T`, covering `{1,...,n}` and satisfying
the running-intersection property: bags containing any particular variable
form a connected subtree. Write `w=max_b |B_b| >= 1` and

\[
 f(x)=\sum_{b=1}^t f_b(x_{B_b}),\qquad x\in[-1,1]^n,
 \qquad f^*=\min_{[-1,1]^n} f.
\]

Each `f_b` is a real polynomial. Its tensor Chebyshev expansion is

\[
 f_b(x)=\sum_\alpha c_{b,\alpha}T_\alpha(x),\qquad
 T_\alpha(x)=\prod_{i\in B_b}T_{\alpha_i}(x_i).
\]

Let `d=max_b deg(f_b)` and choose an integer `r>=max(w,d)`. A feasible
order-`r` sparse preordering point consists of linear functionals

\[
 L_b:\mathbb R[x_{B_b}]_{\le2r}\longrightarrow\mathbb R
\]

such that `L_b(1)=1`, adjacent bags agree on all polynomials in their
intersection of total degree at most `2r`, and

\[
 L_b\left(q(x)^2\prod_{i\in I}(1-x_i^2)\right)\ge0
 \quad\text{if }I\subseteq B_b,\quad
 2\deg q+2|I|\le2r.                                      \tag{1}
\]

The relaxation value is

\[
 \rho_r=\inf_{(L_b)\text{ feasible}}\sum_b L_b(f_b).
\]

Point evaluation at any box point is feasible, so `rho_r<=f*`. Nothing in
the rounding proof assumes this infimum is attained or strong duality.

Define the explicit coefficient budget

\[
 A(f;B)=\sum_b\sum_\alpha |c_{b,\alpha}|
                              \sum_{i\in B_b}\alpha_i^2.  \tag{2}
\]

The decomposition into bag polynomials is part of this constant; constants
in the objective make zero contribution.

The sparse moment hierarchy is a finite semidefinite program. A feasible
moment point supplies a relaxation objective that may lie above or below
the true optimum; its objective alone is not a certified lower bound.
The optimum `rho_r`, or a feasible SOS dual certificate, supplies a lower
bound. The rounding statement applies to every feasible moment point.

## 2. The theorem

**Theorem 1.** Set `m=floor(r/w)+1`. From every feasible sparse preordering
point `(L_b)` one can define a probability measure `nu` on `[-1,1]^n` with

\[
 \left|\int f\,d\nu-\sum_bL_b(f_b)\right|
       \le {3 A(f;B)\over2m^2+1}.                         \tag{3}
\]

Consequently,

\[
 0\le f^*-\rho_r\le {3A(f;B)\over2m^2+1}
                  \le {3w^2 A(f;B)\over2r^2}.           \tag{4}
\]

There exists a box point with objective at most the displayed local
pseudoexpectation objective plus the error in (3). Section 6 gives a
finite Chebyshev-grid version and deterministic extraction in an exact
arithmetic model. No rational-output or bit-complexity guarantee is claimed.

## 3. A fully explicit positive kernel

For `m>=2`, put

\[
 D_m(t)=\sum_{j=0}^{m-1}e^{ijt},\quad
 b_j=(m-|j|)_+,\quad
 a_k=\sum_{j\in\mathbb Z}b_jb_{j-k},\quad
 g_k={a_k\over a_0}.
\]

Here `b_j=0` when `|j|>=m`. Expanding `|D_m(t)|^4` gives

\[
 J_m(t):={|D_m(t)|^4\over a_0}
     =1+2\sum_{k=1}^{2m-2}g_k\cos(kt),\qquad
 a_0={2m^3+m\over3}.                                    \tag{5}
\]

The function `J_m` is nonnegative, even, and integrates to one against
`dt/(2pi)` on the circle. The coefficients `g_k` are nonnegative by their
convolution definition and at most one by Cauchy--Schwarz. Extend `g_k=0`
for `k>2m-2`. For every integer `k>=0`,

\[
 0\le1-g_k\le k^2(1-g_1)={3k^2\over2m^2+1}.             \tag{6}
\]

Indeed `g_k` is the expectation of `cos(kt)` under the nonnegative
probability density `J_m`, and
`1-cos(kt)<=k^2(1-cos(t))`. Moreover,

\[
 a_0-a_1=\tfrac12\sum_j(b_j-b_{j-1})^2=m,
\]

because there are exactly `2m` nonzero differences, all of magnitude one.

Let `mu` denote normalized arcsine measure on `[-1,1]`, and define

\[
 K_m(x,y)=1+2\sum_{k=1}^{2m-2}g_k T_k(x)T_k(y).           \tag{7}
\]

Writing `x=cos(theta)` and `y=cos(phi)`, the cosine addition identity gives

\[
 K_m(x,y)=\tfrac12\{J_m(\theta-\phi)+J_m(\theta+\phi)\}
          \ge0.                                        \tag{8}
\]

Orthogonality of Chebyshev polynomials gives

\[
 \int K_m(x,y)\,d\mu(y)=1,\qquad
 \int T_k(y)K_m(x,y)\,d\mu(y)=g_kT_k(x)                 \tag{9}
\]

for all `k>=0`. For `k` above the kernel degree the second integral and
`g_k` are both zero. All kernel coefficients are rational.

This is the classical squared-Fejér (Jackson-type) construction. The note
derives exactly the coefficients and estimates it uses; it does not claim
the kernel as new.

## 4. Positivity and consistency of the local densities

For each bag define

\[
 K_{m,b}(x,y)=\prod_{i\in B_b}K_m(x_i,y_i),\qquad
 h_b(y)=L_b\bigl(K_{m,b}(\cdot,y)\bigr).                \tag{10}
\]

For a fixed `y_i` the univariate polynomial `K_m(x_i,y_i)` is nonnegative
on `[-1,1]` and has degree at most `2(m-1)`. The classical univariate
interval positivity theorem supplies a representation

\[
 K_m(x_i,y_i)=\sigma_{0,i}(x_i)
                         +(1-x_i^2)\sigma_{1,i}(x_i),   \tag{11}
\]

where `sigma_0,i` is a sum of squares of polynomials of degree at most
`m-1`, and `sigma_1,i` is a sum of squares of polynomials of degree at most
`m-2`. The representation need not vary polynomially in `y_i`; positivity
of `h_b(y)` is checked for each fixed `y`.

Multiplying (11) over a bag gives a preordering representation. Each term
has the form in (1) with

\[
 2\deg q+2|I|\le 2|B_b|(m-1)\le2w(m-1)\le2r.
\]

Thus `h_b(y)>=0`. Equation (9) shows that it integrates to `L_b(1)=1`
against `mu^{B_b}`. Hence

\[
 d\nu_b(y)=h_b(y)\,d\mu^{B_b}(y)                        \tag{12}
\]

is an actual probability measure.

If adjacent bags intersect in `S`, integrating `h_b` in `B_b\S` deletes
the corresponding kernel factors by (9). The remaining marginal density is

\[
 L_b\left(\prod_{i\in S}K_m(x_i,y_i)\right).            \tag{13}
\]

Its input total degree is at most `2|S|(m-1)<=2r`. Agreement of the shared
moments therefore makes (13) identical for both adjacent bags. The measures
`nu_b` have exactly consistent separator marginals.

The standard junction-tree gluing argument now produces a global probability
measure with these bag marginals. Explicitly, root the bag tree, sample the
root bag, and attach the variables introduced by each child using a regular
conditional distribution of its bag law given its separator. Compact
Euclidean boxes are standard Borel spaces, so these conditional distributions
exist. The running-intersection property ensures that the child only shares
already attached variables through its parent separator. Null separator
events may be assigned arbitrary conditional laws. Induction preserves all
bag marginals.

## 5. Objective error and proof of Theorem 1

First, for `|alpha|<=r`,

\[
 |L_b(T_\alpha)|\le1.                                  \tag{14}
\]

The identity

\[
 1-\prod_iT_{\alpha_i}(x_i)^2
  =\sum_i(1-x_i^2)U_{\alpha_i-1}(x_i)^2
                         \prod_{j<i}T_{\alpha_j}(x_j)^2 \tag{15}
\]

uses `1-T_k(x)^2=(1-x^2)U_{k-1}(x)^2`; zero indices contribute zero.
Every term has degree at most `2|alpha|<=2r`. Positivity (1) implies
`L_b(T_alpha^2)<=1`. The moment positivity with `I=emptyset` and
`L_b(1)=1` implies Cauchy--Schwarz,
`L_b(T_alpha)^2<=L_b(T_alpha^2)`, proving (14).

Using (9) and (10),

\[
 \int T_\alpha(y)\,d\nu_b(y)
       =\left(\prod_i g_{\alpha_i}\right)L_b(T_\alpha). \tag{16}
\]

Since each `g_k` lies in `[0,1]`, (6) gives

\[
 \left|1-\prod_i g_{\alpha_i}\right|
 \le\sum_i(1-g_{\alpha_i})
 \le{3\sum_i\alpha_i^2\over2m^2+1}.                    \tag{17}
\]

Expand `f_b` in Chebyshev polynomials, combine (14)--(17), and sum over
bags to obtain (3). The global law is box supported, so
`f*<=int f dnu`. Taking the infimum over feasible `(L_b)` gives the first
bound in (4). Since `m>r/w`, the second bound follows. The existence of a
point with objective at most the law's mean follows from compactness and
continuity. This completes the proof.

## 6. Finite rounding and a sparse certificate consequence

Let `d_infty=max_{b,alpha:c_balpha != 0} max_i alpha_i`, taking zero for
a constant objective, and set

\[
 N=m+\lfloor d_\infty/2\rfloor,\qquad
 \xi_j=\cos{(2j-1)\pi\over2N}\quad(1\le j\le N).       \tag{18}
\]

The normalized arcsine quadrature formula with these nodes and equal
weights `1/N` is exact for univariate polynomials of degree at most `2N-1`.
Since

\[
 2N-1\ge2(m-1)+d_\infty,
\]

tensor quadrature exactly integrates every bag density `h_b` and every
product `f_b h_b`. Define finite bag laws

\[
 p_b(j_{B_b})=N^{-|B_b|}h_b(\xi_{j_{B_b}}).              \tag{19}
\]

These are nonnegative, sum to one, and have matching separator marginals:
summation over a removed coordinate is exactly the corresponding arcsine
integral of its degree-`2(m-1)` polynomial. The same discrete junction-tree
gluing produces a law supported on `{xi_1,...,xi_N}^n` whose expected
objective equals the expectation in (3). Therefore

\[
 \min_{x\in\{\xi_1,\ldots,\xi_N\}^n}f(x)
       \le\sum_bL_b(f_b)+{3A(f;B)\over2m^2+1}.          \tag{20}
\]

Ordinary junction-tree dynamic programming computes this grid minimum
using `O(sum_b N^{|B_b|})` table entries and `O(t N^w)`
arithmetic/comparison work after the local objective tables have been
evaluated. The latter bound accounts for combining messages from all
children of a bag. A
minimizing assignment is recovered by storing conditional argmin entries.
The quadrature nodes are real algebraic; this is an exact-arithmetic count,
not a bit-complexity claim. Notably, this extraction need not construct the
densities or use the input pseudoexpectation explicitly: (20) proves that
the fixed-grid optimum bounds every feasible relaxation point's objective.

Chebyshev-grid approximation and finite-tree dynamic programming are
established methods. This consequence is a rounding interpretation of the
sparse SDP theorem, not a claim of a new general grid optimization method.

For completeness, the finite SDP has a strictly feasible primal point:
take the moments of product arcsine measure in every bag. For each local
preordering product and every nonzero square polynomial allowed in its
localizing matrix, the integral is strictly positive because the weight is
positive on the open box and a nonzero polynomial is not zero there almost
everywhere. These moments obey every consistency equality. The objective
is bounded by (14). Standard finite-dimensional SDP Slater duality gives
dual attainment and no gap. The dual is the sparse preordering certificate

\[
 f-\rho_r\in\sum_b
 \left\{\sum_{I\subseteq B_b}\sigma_{b,I}(x_{B_b})
                     \prod_{i\in I}(1-x_i^2):
       \deg\!\left(\sigma_{b,I}\prod_{i\in I}(1-x_i^2)\right)
                         \le2r\right\},                \tag{21}
\]

where the `sigma_b,I` are sums of squares. The bag consistency multipliers
cancel as polynomials when local identities are summed along the tree.
In particular, `f-f*+3A/(2m^2+1)` has such a certificate by adding a
nonnegative constant to (21). This is an existence result for real SOS
coefficients. Exact rational certificates and their sizes require separate
analysis.

## 7. Limits and verification status

The `2^w` local preordering products are part of the relaxation. Dropping
these products to retain only the ordinary box quadratic module requires
a different kernel positivity argument. No such transfer is claimed here.
The theorem is for the box alone; smoothing need not preserve extra local
constraints or prescribed integer values. The separately reviewed
[finite-state extension](mixed-discrete-extension.md) leaves discrete labels
unchanged under explicit labelled moment and separator consistency conditions.
It does not permit arbitrary label-dependent continuous domains.

The coefficient budget can be large relative to a differently normalized
objective, and the width factor in (4) has not been optimized. The numerical
relaxation cost and exact arithmetic costs of extraction remain open.
The core proof, finite rounding, and certificate consequence have received
[two](kernel-proof-review.md) independent [full reviews](proof-review.md).
Both reviews independently identified and corrected
the stated dynamic-programming work bound; the displayed conservative bound
includes the cost of combining child messages. The
[targeted check record](kernel-verification.md)
reports exact arithmetic tests and their limits.

Literature and targeted computational checks are recorded in companion
files. Project-wide checks and CI inspection are outside this task.

## 8. Prior-work comparison

The [independent prior audit](prior-independent.md) records the sources
examined, exact assumptions, and remaining priority uncertainty. The
[parallel source audit](kernel-prior.md) supplies a second comparison.
The main boundaries are these:

- [Korda, Magron and Ríos-Zertuche (2024/2025)](https://link.springer.com/article/10.1007/s10107-024-02071-6),
  Theorem 6, supplies the inspected sparse box-preordering rate
  `O(r^(-2/(w+3)))`. Its coordinatewise degree convention differs from our
  total-degree convention by width factors. Its sparse Jackson kernel and
  positivity facts are prior; our direct primal construction avoids its
  intermediate positive polynomial decomposition.
- [Laurent and Slot (2022/2023)](https://link.springer.com/article/10.1007/s11590-022-01922-5)
  already prove dense box-preordering rates of order `r^-2` with positive
  Chebyshev kernels. The claim here concerns preserving consistency of
  overlapping local truncated functionals.
- [Gamertsfelder and Mourrain (2025)](https://arxiv.org/html/2501.09385)
  obtain generalized-moment rates that include exponent two on boxes under
  an attained finitely supported dual assumption. The independent audit
  gives a width-two example without any exact polynomial separator dual.
  Our theorem makes no such dual-attainment assumption for the infinite
  marginal problem; Slater is used only for each finite SDP.
- [Catala, Hockmann, Kunis and Wageringel (2024)](https://link.springer.com/article/10.1007/s00365-024-09686-0),
  Remark 3.7, already identifies equal low-order moments with equal Jackson
  smoothing for actual measures. [Lasserre (2006)](https://doi.org/10.1137/05064504X)
  already supplies consistent-measure gluing in sparse optimization.
  Neither fact is claimed as new.
- [Piazzon and Vianello (2018)](https://www.math.unipd.it/~marcov/pdf/opticheb.pdf)
  give second-order Chebyshev-grid optimization bounds. Together with
  standard tree dynamic programming this limits the algorithmic novelty of
  Section 6: its role is an explicit comparison and rounding guarantee for
  this SDP hierarchy.
- [Gribling, de Klerk and Vera (2026)](https://arxiv.org/html/2605.31496)
  obtain a dense Putinar rate `O(log^3(r)/r^2)` using squared kernels with
  approximate normalization. That is a different cone. Exact mass
  preservation is essential to the separator argument here, so the theorem
  does not automatically transfer to their squared kernel or vice versa.

Magron's [*Sparse polynomial optimization*](https://homepages.laas.fr/vmagron/slides/lorentz25.pdf),
Lorentz Center, 7 July 2025, logical slide 23 of 44, already states
`O(d^-2)` for two overlapping local full preorderings with total-degree
truncation `2d`, attributing it to Korda, Ríos-Zertuche and Magron.
The same statement appears in
[*\(Non\)linear moment problems: theory and practice*](https://homepages.laas.fr/vmagron/nlmoment.pdf),
TENORS Learning Week 2, 16 February 2026, logical slide 35 of 90.
The independent audit inspected both rendered slides. Neither displayed
statement is dismissed as a typo: they are earlier public assertions of
the rate, despite the unexplained difference from the published theorem.
The slides mention a sparse Putinar rate without displaying its exponent.

These comparisons support a verified self-contained proof and rounding
construction, but not novelty of the inverse-square rate. The separately
reviewed [fixed quadratic lower bound](quadratic-sharpness.md) establishes
sharpness and has its own prior comparison. Publication priority of the
specific additions remains unestablished.
