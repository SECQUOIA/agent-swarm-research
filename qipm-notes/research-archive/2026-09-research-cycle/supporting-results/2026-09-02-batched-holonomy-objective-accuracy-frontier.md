# Batched holonomy SDPs: direct products and the scalar-accuracy frontier

Date: 2026-09-02

## Main point

Take \(G\) disjoint copies of the intrinsic trace-one triangle-holonomy SDP,
each driven by \(N\) private signs.  The total product SDP has

\[
                         L=33GN                                      \tag{1}
\]

constant-size PSD blocks, scalar row sparsity at most three, and scalar
column sparsity at most two.  The construction gives two different, sharp
batch lower bounds.

1. Returning all \(G\) component optimal values to additive error \(1/25\)
   takes \(\Theta(GN)=\Theta(L)\) raw queries.  Moreover, a published strong
   direct-product theorem implies that using only a sufficiently small
   constant fraction of \(GN\) queries makes the probability that all
   answers are correct exponentially small in \(G\).
2. The single scalar optimum obtained by averaging the \(G\) component
   objectives has the exact accuracy frontier
   \[
       \boxed{Q_\varepsilon
       =\Theta\!\left(N\min\{G,1/\varepsilon\}\right)
       =\Theta\!\left(\min\{L,N/\varepsilon\}\right)}          \tag{2}
   \]
   for \(0<\varepsilon\le1/100\), up to absolute constants and the harmless
   fixed factor 33 in \(L\).

For randomized classical algorithms the corresponding sharp law is

\[
 R_\varepsilon
 =\Theta\!\left(N\min\{G,1/\varepsilon^2\}\right)
 =\Theta\!\left(\min\{L,N/\varepsilon^2\}\right).             \tag{2a}
\]

Thus the family gives the standard quadratic quantum improvement in scalar
mean-estimation accuracy while retaining the full \(N\)-query cost of each
hidden holonomy bit.  The classical scan saturates at
\(\varepsilon=\Theta(G^{-1/2})\), whereas the quantum scan saturates only at
\(\varepsilon=\Theta(G^{-1})\).

Thus a scalar objective has a genuine phase transition.  Accuracy finer than
the \(1/G\) spacing of the component count forces a linear scan of the full
sparse input.  At constant accuracy, coherent approximate counting samples
the batch and removes the \(G\) factor.  This also explains why merely taking
a direct sum cannot prove a linear-total-size lower bound for a coarse scalar
output.

The lower bound in (2) follows from a useful parity-block symmetrization
lemma proved below.  It does not need a black-box composition theorem.

## 1. One component

For completeness, recall only the facts needed from
`2026-09-02-intrinsic-spectrum-trace-normalized-s3-parity.md`.
One component has \(P=33N\) blocks and input signs
\(\sigma_1,\ldots,\sigma_N\).  Put

\[
 h=\prod_{j=1}^N\sigma_j.
\]

After eliminating a degree-two signed congruence path and imposing the
public row \(\operatorname{tr}Z=1\), the component is exactly

\[
 \min_{Z\succeq0,\ \operatorname{tr}Z=1}
 \langle\overline C_h,Z\rangle,
 \qquad
 \overline C_h=3I+\frac1{10}(H_{12}+H_{23}+hH_{13}).           \tag{3}
\]

The two cost spectra and optimal values are

\[
 \begin{array}{c|c|c}
 h&\operatorname{spec}(\overline C_h)&v_h\\ \hline
 +1&\{16/5,29/10,29/10\}&29/10\\
 -1&\{31/10,31/10,14/5\}&14/5.
 \end{array}                                                   \tag{4}
\]

All local costs and right-hand sides are public.  Bit \(\sigma_j\) changes
only the two signed values in the \(12\) and \(13\) copy rows of edge \(j\).
Consequently one coherent fixed-position row or column query to the displayed
sparse constraint matrix is simulated with at most one query to one input
sign.

## 2. The disjoint batch

For \(g=1,\ldots,G\), let

\[
 \sigma_{g,1},\ldots,\sigma_{g,N}\in\{-1,+1\},\qquad
 h_g=\prod_{j=1}^N\sigma_{g,j},\qquad
 y_g=\frac{1+h_g}{2}\in\{0,1\}.              \tag{5}
\]

Take the Cartesian product of the \(G\) feasible spectrahedra.  There is one
public trace-one row per component and no equality row couples two
components.  Hence the batch remains strictly primal and dual feasible, has
\(L=33GN\) PSD blocks, and preserves scalar row sparsity three, column
sparsity two, and two input-dependent coefficient values per raw bit.

The feasible set is not second-order-cone representable.  Projection onto
one root block gives the qutrit density spectrahedron
\(\mathcal D_3=\{Z\succeq0:\operatorname{tr}Z=1\}\).  If the batch had a
finite SOC lift, so would this projection; homogenizing a lift of
\(\mathcal D_3\) would give a finite SOC lift of
\(\operatorname{cone}(\mathcal D_3)=\mathbb S_+^3\), contradicting Fawzi's
theorem.

## 3. All component values: no batch amortization

Suppose a quantum algorithm returns numbers
\(\widehat v_1,\ldots,\widehat v_G\) such that

\[
             |\widehat v_g-v_{h_g}|\le\frac1{25}
             \quad\text{for every }g                           \tag{6}
\]

with joint success probability at least \(2/3\).  Thresholding each answer
at \(57/20\) recovers all \(h_g\).  Taking the product of the decoded signs
then computes

\[
                         \prod_{g=1}^Gh_g
                         =\prod_{g=1}^G\prod_{j=1}^N\sigma_{g,j},           \tag{7}
\]

the parity of all \(GN\) raw bits, with success at least \(2/3\).  Quantum
parity needs \(\Omega(GN)\) queries.  Reading every sign gives the matching
upper bound.  Therefore

\[
 \boxed{Q(\text{all component values})
             =\Theta(GN)=\Theta(L).}                            \tag{8}
\]

There is also a strong success tradeoff.  The strong direct-product theorem
of Lee and Roland implies that absolute constants \(a,b>0\) exist such that
any algorithm using at most \(aGN\) raw queries has probability at most
\(2^{-bG}\) of satisfying (6) for all \(G\) components.  This exponential
statement is inherited from the general query theorem; the new content here
is its sparse-SDP instantiation.

For a precise specialization, take \(f=\operatorname{PARITY}_N\), \(k=G\),
and \(\delta=3/4\) in Lee--Roland Theorem 1.1.  It gives

\[
 Q_{1-(3/4)^{G/2}}(f^{(G)})
 \ge \frac{G\log(9/8)}{8000}\,Q_{1/4}(f).                    \tag{8a}
\]

Since \(Q_{1/4}(\operatorname{PARITY}_N)=\Theta(N)\), fewer than an
absolute constant times \(GN\) queries gives joint success below
\((3/4)^{G/2}=2^{-\Omega(G)}\).  Thresholding outputs satisfying (6)
produces exactly the classical output vector required by \(f^{(G)}\), so this
application needs neither a state-generation extension nor an extra promise.

Equation (8) applies directly to preprocessing that must materialize a
reusable classical table of all component optima.  It does not apply to a
one-shot data structure that is asked for only one subsequently chosen
component, nor does it prohibit destructive quantum encodings from which not
all entries can be recovered.

## 4. One averaged scalar objective

Now give the batch the single scalar objective

\[
 \frac1G\sum_{g=1}^G
 \left[\frac1P\sum_{i=0}^{P-1}
       \langle C_{g,i},X_{g,i}\rangle\right].                  \tag{9}
\]

Separability and (4) give its exact optimum

\[
 V(\sigma)=\frac1G\sum_{g=1}^Gv_{h_g}
 =\frac{14}{5}+\frac1{10G}\sum_{g=1}^Gy_g.                    \tag{10}
\]

Thus additive-\(\varepsilon\) estimation of \(V\) is exactly additive-
\(10\varepsilon\) estimation of the mean of the \(G\) hidden parity bits.

### 4.1 Upper bound

An exact coherent oracle for \(h_g\), with \(g\) in superposition, can be
implemented using \(O(N)\) queries to the raw signs in group \(g\).  Standard
amplitude estimation then estimates \(G^{-1}\sum_gy_g\) to additive error
\(10\varepsilon\) with \(O(1/\varepsilon)\) calls to that parity oracle.  If
\(1/\varepsilon>G\), simply compute all \(G\) parities.  This proves

\[
 Q_\varepsilon(V)
 =O\!\left(N\min\{G,1/\varepsilon\}\right).                   \tag{11}
\]

The approximate-counting step is the standard amplitude-estimation algorithm
of G. Brassard, P. H\o yer, M. Mosca, and A. Tapp,
[*Quantum Amplitude Amplification and
Estimation*](https://arxiv.org/abs/quant-ph/0005055).  Only the realization
of one marked-item query by an \(N\)-sign parity computation is specific to
this construction.

### 4.2 Parity-block symmetrization lemma

The matching lower bound is not obtained by treating the \(h_g\) as free
oracle bits; the algorithm queries their \(GN\) constituents directly.  The
following lemma accounts for that access.

> **Lemma (degree division under parity blocks).**  Let a \(q\)-query quantum
> algorithm access \(\sigma\in\{-1,+1\}^{G\times N}\), and let
> \(p(\sigma)\) be the probability of any fixed final measurement event.
> Average this probability uniformly over raw inputs conditioned on the
> block parities \(h=(h_1,\ldots,h_G)\):
> \[
>       \overline p(h)=\mathbb E[p(\sigma)\mid
>                    \prod_j\sigma_{g,j}=h_g\text{ for every }g].          \tag{12}
> \]
> Then \(\overline p\) is a real multilinear polynomial in \(h\) of degree
> at most \(\lfloor2q/N\rfloor\).

**Proof.**  The polynomial method writes \(p(\sigma)\) as a real multilinear
polynomial of degree at most \(2q\).  Consider one of its sign monomials
\(\chi_S(\sigma)=\prod_{(g,j)\in S}\sigma_{g,j}\).  Conditional expectation
factors over groups.  Within group \(g\), uniform averaging subject to
\(\prod_j\sigma_{g,j}=h_g\) annihilates every character except the empty
character and the full \(N\)-bit character.  The former averages to one and
the latter to \(h_g\).  Therefore \(\chi_S\) either vanishes or becomes a
monomial in \(h\) whose degree is the number of groups for which \(S\)
contains all \(N\) bits.  That number is at most \(|S|/N\le2q/N\).  Averaging
all monomials proves the lemma. \(\square\)

### 4.3 Lower bound and phase transition

Let an estimator achieve additive objective error \(\varepsilon\) on every
raw input with probability at least \(2/3\), where
\(0<\varepsilon\le1/100\).  For all sufficiently large \(G\), choose two
Hamming weights \(\ell,\ell'\) centered around \(G/2\), with separation

\[
 \Delta=|\ell-\ell'|=
 \max\{1,\lceil21\varepsilon G\rceil\}.                       \tag{12a}
\]

Their optimal values differ by \(\Delta/(10G)>2\varepsilon\).  Thresholding
the estimate midway therefore gives a bounded-error acceptance polynomial
which distinguishes the two weights.  The finitely many smaller values of
\(G\) are absorbed into the constants, or handled directly by one parity
block.  After the conditional averaging in (12), the polynomial
distinguishes the same two Hamming weights of \(y=(1+h)/2\).

Theorem 1.1 of Nayak and Wu gives, for a polynomial distinguishing weights
\(\ell,\ell'\), a degree lower bound containing
\(\Omega(\sqrt{m(G-m)}/\Delta)\), where \(m\) is the one of the two weights
farther from \(G/2\).  Both selected weights are central, so this becomes

\[
                 \Omega\!\left(\min\{G,1/\varepsilon\}\right).            \tag{13}
\]

This is the finite-size saturation behind their Corollary 1.12 for additive
mean estimation.  The fixed conversion factor ten between objective and mean
error changes only the hidden constant.  Combining (13) with the
degree-division lemma gives

\[
 \left\lfloor\frac{2q}{N}\right\rfloor
 =\Omega\!\left(\min\{G,1/\varepsilon\}\right),
\]

which proves the lower half of (2).

There is also a general composition route to the same asymptotic lower bound.
The thresholded problem is the partial symmetric Boolean function separating
weights \(\ell\) and \(\ell'\), composed independently with \(G\) copies of
\(\operatorname{PARITY}_N\).  The negative-weight adversary bound
characterizes bounded-error quantum query complexity and obeys perfect block
composition; see A. Belovs and T. Lee,
[*The quantum query complexity of composition with a
relation*](https://arxiv.org/abs/2004.06439).  Combining that theorem with the
Nayak--Wu outer lower bound and
\(Q(\operatorname{PARITY}_N)=\Theta(N)\) also yields (2).  The elementary
conditional-Fourier proof in Section 4.2 usefully exposes the exact degree
division, but the composition principle itself is prior art.

Equivalently, in terms of total sparse size,

\[
 Q_\varepsilon(V)=
 \begin{cases}
  \Theta(N/\varepsilon),&\varepsilon=\Omega(1/G),\\
  \Theta(L),&\varepsilon=O(1/G).
 \end{cases}                                                   \tag{14}
\]

This is an end-to-end tightness statement, not merely a lower bound: coherent
approximate counting realizes the first branch and an explicit scan realizes
the second.

## 5. Randomized classical complexity

The quantum phase law has a matching classical counterpart with the usual
quadratic loss in accuracy.

### 5.1 Upper bound

Let \(s=\min\{G,\lceil c/\varepsilon^2\rceil\}\) for a sufficiently large
absolute constant \(c\).  Sample \(s\) component indices uniformly, without
replacement when \(s<G\).  For each sampled component, read its \(N\) signs
and compute its parity.  The empirical mean of the resulting \(y_g\)'s,
inserted into (10), has additive error at most \(\varepsilon\) with constant
success probability by the usual bounded-sampling estimate.  If \(s=G\),
the result is exact.  Hence

\[
 R_\varepsilon(V)
 =O\!\left(N\min\{G,1/\varepsilon^2\}\right).                 \tag{15}
\]

### 5.2 Exact adaptive simulation lemma

The lower bound must allow a raw algorithm to interleave its queries among
many parity blocks.  The following distributional simulation handles that
adaptivity exactly.

> **Lemma (a parity block charges \(N\) classical raw queries).**  Fix
> \(h\in\{-1,+1\}^G\).  In each group \(g\), draw the \(N\) raw signs
> uniformly conditioned on \(\prod_j\sigma_{g,j}=h_g\), independently among
> groups.  Any deterministic adaptive raw-sign decision tree making at most
> \(q\) queries can be simulated with exactly the same output distribution by
> a randomized decision tree that queries the parity-bit oracle \(h\) at most
> \(\lfloor q/N\rfloor\) times on every computation path.

**Proof.**  The simulator keeps the signs already exposed in each group.  A
first-time query while at least two signs in that group remain unseen is
answered by a fresh independent fair sign.  If the query asks for the last
unseen sign, the simulator queries \(h_g\) and returns the unique sign that
makes the product of all \(N\) signs equal to \(h_g\).  Repeated queries
return the stored answer.

This is exactly the uniform conditional distribution: every proper subset
of the \(N\) signs is uniform and independent of \(h_g\), while the last sign
is forced by the product.  The argument remains valid under arbitrary
adaptive interleaving because the groups are conditionally independent.
Every parity-oracle query corresponds to a distinct group in which all
\(N\) raw signs have been queried at least once.  These completed groups use
disjoint sets of \(N\) first-time raw queries, so their number is at most
\(\lfloor q/N\rfloor\) pathwise.  Queries to repeated coefficient
occurrences or to public coefficients can only increase the raw cost and do
not affect the bound. \(\square\)

The same statement holds for a randomized adaptive raw algorithm: first fix
its internal random seed, apply the lemma, and then include both that seed
and the simulator's fair signs in the induced randomized parity-bit tree.

### 5.3 Lower bound

Assume a randomized raw-query algorithm estimates \(V\) to additive error
\(\varepsilon\) with probability at least \(2/3\) on every raw input.  For
each fixed parity vector \(h\), it has the same guarantee after averaging
over raw strings conditioned on \(h\).  The simulation lemma therefore gives
a randomized decision tree that estimates the mean of the \(G\) bits
\(y_g=(1+h_g)/2\) to additive error \(10\varepsilon\), using at most
\(\lfloor q/N\rfloor\) parity-bit queries.

The classical randomized query complexity of additive mean estimation is

\[
 \Theta\!\left(\min\{G,1/\delta^2\}\right)                   \tag{16}
\]

at mean error \(\delta\).  For completeness, the upper bound is sampling.
For the lower bound, Yao's principle applied to uniformly random strings of
two nearby central Hamming weights reduces the task to distinguishing two
hypergeometric experiments.  With \(o(\min\{G,1/\delta^2\})\) inspected
positions their total variation distance is bounded away from one; this is
the standard finite-population Bernoulli-mean lower bound.  At
\(\delta=O(G^{-1/2})\), it saturates at \(\Omega(G)\).

Taking \(\delta=10\varepsilon\) and using the pathwise query bound yields

\[
 q=\Omega\!\left(N\min\{G,1/\varepsilon^2\}\right).          \tag{17}
\]

Together with (15), this proves (2a).  Comparing (2) and (2a) gives three
regimes:

\[
\begin{array}{c|c|c}
\text{accuracy}&Q_\varepsilon(V)&R_\varepsilon(V)\\ \hline
\varepsilon=\Omega(G^{-1/2})
 &\Theta(N/\varepsilon)&\Theta(N/\varepsilon^2)\\
G^{-1}=O(\varepsilon)=O(G^{-1/2})
 &\Theta(N/\varepsilon)&\Theta(NG)\\
\varepsilon=O(G^{-1})
 &\Theta(NG)&\Theta(NG).
\end{array}                                                   \tag{18}
\]

The endpoints overlap only by constant factors.  The middle regime is the
most pronounced separation: every randomized classical algorithm must scan
a constant fraction of the full sparse batch, while the quantum algorithm
still samples coherently across components.

In particular, at \(\varepsilon=\Theta(G^{-1/2})\),
\[
 Q_\varepsilon(V)=\Theta(N\sqrt G),\qquad
 R_\varepsilon(V)=\Theta(NG)=\Theta(L).                 \tag{18a}
\]
Since \(L=33NG\), the quantum bound is
\(\Theta(\sqrt{NL})\) up to the fixed factor \(\sqrt{33}\), while the
randomized classical bound is linear in the displayed sparse size.  This is
a dimension/accuracy specialization of the exact phase laws, not an
unqualified exponential advantage.

## 6. Parallel public-start Newton preprocessing

The batch has a matching QIPM interpretation.  With objective (9), take the
public point \(X_{g,i}=I/3\) and product-barrier parameter

\[
                             \mu=\frac1{GP}.                   \tag{19}
\]

The full ambient Hessian is \((9/(GP))I\), so the complete reduced Hessian
on the \(5G\)-dimensional feasible tangent is the same scalar identity.  All
unreduced Newton right-hand sides are public.  In physical root coordinates,
the \(g\)-th direction remains

\[
 \Delta Z_g=-\frac1{90}(H_{12}+H_{23}+h_gH_{13}).             \tag{20}
\]

Every undamped physical step has minimum eigenvalue at least \(14/45\).
Thus a preprocessor that returns classical descriptions of all root
directions with entrywise error less than \(1/200\) reveals every \(h_g\)
from the sign of the \(13\) entry.  It inherits (8) and the Lee--Roland
exponential success tradeoff despite exact reduced condition number one and
public unreduced residuals.

The error threshold is nonvacuous because the hard entry has magnitude
\(1/90>1/200\).  This corollary concerns simultaneous classical
materialization.  A single normalized global quantum direction state is a
compressed output and need not reveal all \(G\) parities; no \(\Omega(GN)\)
claim is made for one such state.

## 7. Scope and novelty

The direct-product and approximate-counting ingredients are prior art.  The
quantum polynomial method is due to Beals et al.,
[*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049).
The approximate-counting degree lower bound is Nayak and Wu,
[*The quantum query complexity of approximating the median and related
statistics*](https://arxiv.org/abs/quant-ph/9804066).  The exponential batch
tradeoff is Lee and Roland,
[*A strong direct product theorem for quantum query
complexity*](https://arxiv.org/abs/1104.4468).  The non-SOCP fact is Fawzi,
[*On representing the positive semidefinite cone using the second-order
cone*](https://arxiv.org/abs/1610.04901).

Perfect negative-adversary composition already covers the outer gap-counting
function composed with inner parity blocks, as explained after (13).
Consequently the degree-division lemma is a short construction-specific
proof, not a new general composition theorem.  Likewise, the
\(O(1/\varepsilon)\) mean-estimation branch is standard amplitude estimation,
and the exact \(2^{-\Omega(G)}\) success decay is a direct specialization of
Lee--Roland.

Boolean composition has also been embedded in an optimization value before.
Theorem 8.4 of S. Apers and S. Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215v3), embeds a
majority--OR--majority composition into an LP optimum and proves an
\(\Omega(\sqrt{nd}\,r)\) coefficient-query lower bound.  It does not give
the present parity-block accuracy curve, simultaneous component-output
theorem, non-SOCP holonomy geometry, or condition-one public Newton start;
but it means that block composition inside an optimization value is not
itself new.

The candidate new result is therefore only the sparse-QIPM synthesis: a non-SOCP,
trace-normalized, intrinsically spectral holonomy family for which both the
no-amortization vector theorem and the exact scalar accuracy frontier can be
proved, while the public-start reduced Newton Hessian is a scalar identity
and its unreduced residuals are public.  The adaptive conditional simulation
lemma additionally proves the matching randomized classical frontier without
assuming that a raw algorithm queries one parity block at a time.  In
particular, (14) and (18) give a precise
boundary on what direct-sum lower-bound amplification can and cannot prove
for a single scalar optimization output.

The theorem remains a raw-query result.  An oracle that supplies the block
parities, aggregated reduced gradients, or component optima has already
performed the hard composition.  The value lower bound is for the exact
displayed equalities; the path operator has small singular values, so no
constant-residual robustness is claimed.
