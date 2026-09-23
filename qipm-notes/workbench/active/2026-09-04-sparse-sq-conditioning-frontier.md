# Dimension-independent sparse-SQ sampling and a tight conditioning frontier

Status: Proved; independently audited and literature-screened  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on theorems; moderate-to-high on apparent novelty of the joint frontier  

## Main result

Let \(A\in\mathbb R^{N\times N}\) be invertible, with at most \(d\) nonzeros
per row and column, public spectral bounds

\[
 \|A\|_2\leq1,\qquad \sigma_{\min}(A)\geq\kappa^{-1},
\]

row-and-column sparse-location/value access, and \(SQ(b)\) for a nonzero
right-hand side.  For \(0<\epsilon\leq1/2\), there is a classical algorithm
that samples from the exact squared-coordinate distribution of a vector
\(\widetilde x\) satisfying

\[
 \|\widetilde x-A^{-1}b\|_2
 \leq\epsilon\|A^{-1}b\|_2
\]

in ideal real arithmetic, using expected

\[
 \boxed{
 \exp\!\left(
 O\bigl(\kappa\log d\log(1/\epsilon)\bigr)
 \right)}
                                                               \tag{1}
\]

queries and arithmetic operations, up to polynomial factors in \(\kappa\).
The same construction gives coordinate queries to \(\widetilde x\).
Its complexity is independent of \(N\).

If \(A\succ0\), the sharper bound is

\[
 \boxed{
 \exp\!\left(
 O\bigl(\sqrt\kappa\log d\log(1/\epsilon)\bigr)
 \right).}                                                     \tag{2}
\]

Consequently, for fixed \(d\geq2\) and fixed \(\epsilon\), every
\(N^c\) classical lower bound that survives this sparse-location plus
\(SQ(b)\) access requires

\[
 \kappa=\Omega(\log N)
\]

in the general case and

\[
 \boxed{\kappa=\Omega(\log^2N)}
\]

for SPD systems.

These exponents are optimal in the joint dependence on conditioning,
sparsity, and precision, up to constants in the exponent and polynomial
factors, under the solution-distribution contract stated below.

## Chebyshev local inverse

For the general case, put \(B=A^TA\), \(a=\kappa^{-2}\), and

\[
 r_m(\lambda)=
 \frac{T_m((1+a-2\lambda)/(1-a))}
      {T_m((1+a)/(1-a))}.
\]

Then \(r_m(0)=1\) and

\[
 \|r_m\|_{[a,1]}
 \leq2\left(\frac{\kappa-1}{\kappa+1}\right)^m.
\]

Hence

\[
 q_{m-1}(\lambda)=\frac{1-r_m(\lambda)}{\lambda}
\]

is a polynomial, and \(m=O(\kappa\log(1/\epsilon))\) makes the last norm at
most \(\epsilon\).  Define

\[
 P=q_{m-1}(A^TA)A^T.
\]

For \(b=Ax\),

\[
 Pb-x=-r_m(A^TA)x,
\]

so \(\widetilde x=Pb\) has the required relative error without an extra
condition factor.  The singular values of \(P\) are

\[
 \frac{|1-r_m(\sigma^2)|}{\sigma},
\]

and therefore

\[
 1-\epsilon\leq\sigma_{\min}(P),\qquad
 \sigma_{\max}(P)\leq(1+\epsilon)\kappa,\qquad
 \kappa(P)\leq3\kappa.                                       \tag{3}
\]

The case \(\kappa=1\) uses \(P=A^T\).

For \(A\succ0\), apply the same residual directly on
\([\kappa^{-1},1]\).  It satisfies

\[
 \|r_m\|
 \leq2\left(
 \frac{\sqrt\kappa-1}{\sqrt\kappa+1}
 \right)^m,
\]

so \(m=O(\sqrt\kappa\log(1/\epsilon))\) and
\(P=q_{m-1}(A)\).  Its eigenvalues lie in
\([1-\epsilon,\kappa(1+\epsilon)]\).

Every row and column of these polynomial operators is supported in an
alternating sparse-graph neighborhood.  A complete row or column can be
materialized by enumerating at most

\[
 W=d^{O(m)}
\]

walks and aggregating equal endpoints.  Both row and column degree
assumptions are essential.

## Exact sparse matrix-vector rejection sampler

Let \(P\) be an invertible matrix with at most \(R\) nonzeros per row and
column, singular values in \([a_P,b_P]\), and explicit sparse access.  For
\(v\) with \(SQ(v)\), define

\[
 c_j^2=\sum_i|P_{ij}|^2,\qquad
 S_i=\sum_j|P_{ij}v_j|^2.
\]

One trial does the following:

1. sample \(j\) with probability \(|v_j|^2/\|v\|^2\);
2. accept \(j\) with probability \(c_j^2/b_P^2\);
3. sample \(i\) from column \(j\) with probability
   \(|P_{ij}|^2/c_j^2\);
4. compute \(y_i=(Pv)_i\) and \(S_i\) from sparse row \(i\), and accept with
   probability \(|y_i|^2/(RS_i)\).

Cauchy--Schwarz makes the last probability at most one.  The probability
that a raw trial outputs index \(i\) is

\[
 \frac{|y_i|^2}{R b_P^2\|v\|^2}.
\]

Thus the conditional output is exactly
\(|y_i|^2/\|y\|^2\), and the expected number of trials is

\[
 \frac{R b_P^2\|v\|^2}{\|Pv\|^2}
 \leq R\kappa(P)^2.                                          \tag{4}
\]

Each trial materializes one row and column.  Combining (3), (4), and the
walk enumeration gives

\[
 O(W^2\kappa^2)
\]

work, which proves (1) and (2).  The factor \(R\) in (4) can be necessary:
a normalized dense Hadamard block has condition one and second-stage
acceptance exactly \(1/R\).

## Output and precision boundary

The theorem supplies a coordinate oracle and solution-distribution sampler.
It does not supply an exact norm oracle for \(Pb\).  The norm can be
multiplicatively estimated from the total rejection rate in
\(O(R\kappa(P)^2\gamma^{-2}\log(1/\delta_f))\) trials for relative error
\(\gamma\) and failure probability \(\delta_f\).  Exact norm evaluation can
require \(\Omega(N)\) queries even for a diagonal condition-two matrix.

Likewise, literal exact sampling assumes ideal real arithmetic.  Finite
precision gives a total-variation approximation and requires the usual
bit-complexity accounting.  No claim is made for strong coordinate error
relative to \(\|x\|_\infty\).

## Tight SPD witness from Grønlund--Larsen

The SPD conditioning threshold is attained.  In the explicit v5
Grønlund--Larsen Forrelation family, publicly scale the symmetric hard matrix
\(M\) by \(\bar M=M/(1+\gamma)\), where \(\gamma=e^{-1/T}\), and set

\[
 B=\bar M^2,\qquad b=\bar M e_1.
\]

Then

\[
 B\succ0,\qquad \deg(B)\leq5,\qquad
 B^{-1}b=\bar M^{-1}e_1.
\]

The public scalar does not change normalized sampling or relative error.
Sparse access to \(B\) and \(SQ(b)\) is simulated with constant overhead by
enumerating two-hop neighborhoods.

For this explicit family, even full \(SQ(B)\) is simulable with constant
overhead.  The matrix has the form

\[
 M=\begin{pmatrix}0&A\\A^\dagger&0\end{pmatrix},
\qquad A=I-\gamma U,
\]

so

\[
 B=\frac1{(1+\gamma)^2}
 \operatorname{Diag}(C,C),\qquad
 C=(1+\gamma^2)I-\gamma(U+U^\dagger).
\]

The three terms occupy disjoint clock blocks, and all row and column norms
are equal and public.  Conditional sampling uses only a constant number of
hidden-input queries.  Moreover \(U\) is unitarily equivalent to a
\(3T\)-cycle shift, so

\[
 \kappa(M)=\Theta(T)=\Theta(\log N),\qquad
 \boxed{\kappa(B)=\Theta(\log^2N).}
\]

The original \(\Omega(N^{1-1/k})\) constant-precision SQ sampling lower bound
therefore survives on a five-sparse SPD system exactly at the threshold
allowed by (2), up to constants.  This gives a tight conditioning phase
boundary, not merely an upper bound.

## Matching joint conditioning--sparsity--precision lower bound

The upper exponents in (1)--(2) are also attained as functions of all three
parameters.  Let \(K\geq3\), let \(q=2^r\), and set

\[
 \alpha_K=\log\frac{K+1}{K-1},\qquad
 \ell=\frac{\log(1/\zeta)}{6\alpha_K}+O(1).                  \tag{5}
\]

There are real sparse systems with full matrix-SQ access and SQ access to a
public-basis right-hand side such that every classical relative-\(\zeta\)
solution-distribution sampler needs

\[
 \boxed{
 Q=\Omega\!\left(\frac{\zeta q^{\ell/2}}{r\ell}\right).}    \tag{6}
\]

The general symmetric system has condition number exactly \(K\) and sparsity
at most \(q+1\).  The SPD system has condition number exactly \(K^2\) and
sparsity at most \(2q+1\).  Therefore, writing \(s\) for row/column sparsity,
(6) gives

\[
 Q=\exp(\Omega(K\log s))                                    \tag{7}
\]

at fixed sufficiently small precision.  Whenever \(K\log s\) exceeds a
universal constant, its precision-sensitive form is

\[
 Q=\exp\!\left(
 \Omega(K\log s\log(1/\zeta))
 \right),                                                   \tag{8}
\]

and the SPD exponent is obtained by substituting \(K=\sqrt\kappa\).
The fully explicit version, which remains valid outside that regime, is

\[
 \log Q\geq
 \left(\frac{\log q}{12\alpha_K}-1\right)\log(1/\zeta)
 -O(\log q+\log(r\ell)).                                    \tag{9}
\]

### Cyclic-clock construction

Take the block-Hadamard 2-Forrelation circuit on \(\ell\) blocks of \(r\)
qubits, with forward, final-state holding, and reverse clock segments of total
period \(3T\).  Its real orthogonal clock transition \(U\) obeys
\(U^{3T}=I\), is \(q\)-sparse, and is gauge-equivalent to a cyclic shift.
Set

\[
 \gamma=\frac{K-1}{K+1},\qquad A=I-\gamma U.                \tag{10}
\]

After even clock padding, the symmetric dilation

\[
 C=\frac1{1+\gamma}
 \begin{pmatrix}0&A\\A^T&0\end{pmatrix}                   \tag{11}
\]

has condition number exactly \(K\).  A cleaner SPD instance is

\[
 B=\frac{A^TA}{(1+\gamma)^2},\qquad
 b=\frac{A^Te}{(1+\gamma)^2},                               \tag{12}
\]

for a public basis vector \(e\).  Then

\[
 B^{-1}b=A^{-1}e,qquad \kappa(B)=K^2,
\]

and

\[
 B=\frac{(1+\gamma^2)I-\gamma(U+U^T)}{(1+\gamma)^2}.         \tag{13}
\]

The diagonal, forward, and reverse supports in (13) are disjoint clock
supports; their row and column norms are uniform and public.  Thus full
\(SQ(B)\), as well as \(SQ(b)\), is simulated with constant hidden-input
query overhead.

The inverse is the exact finite history state

\[
 A^{-1}e=\frac1{1-\gamma^{3T}}
 \sum_{t=0}^{3T-1}\gamma^tU^te.                             \tag{14}
\]

Its final-state holding segment has normalized mass

\[
 p=\frac{z}{1+z+z^2},\qquad z=\gamma^{2T}.                  \tag{15}
\]

Choosing \(T\) nearest
\(\log(1/\zeta)/(2\alpha_K)\) makes \(p=\Theta(\zeta)\).
A relative-\(\zeta\) vector perturbation changes the normalized projected
plateau state by only \(O(\sqrt\zeta)\).  After
\(O(1/\zeta)\) raw samples, its conditional measurement still solves the
2-Forrelation promise.  The classical query lower bound for that promise gives
(6).

The ambient dimension here is

\[
 N=\Theta(Tq^\ell),
\]

so the lower exponent is in \(\log s\), not in \(\log N\).  This distinction
is essential.

For vanishing \(\zeta\), the theorem assumes that each invocation's overall
output law is the squared-coordinate law of some relative-\(\zeta\) solution,
or an equivalent flagged/Las-Vegas guarantee (failure \(O(\zeta)\) also
suffices).  An unflagged constant-probability failure component could swamp
the rare \(\Theta(\zeta)\) plateau.  The fixed-precision lower bound does not
have this issue.

## Prior art and QIPM consequence

[Andoni--Krauthgamer--Pogrow](https://arxiv.org/abs/1809.02995) explicitly
posed \(\ell_2\)-sampling from \(A^{-1}b\), given an \(\ell_2\)-sampler for
\(b\), as an open variant; their SPD results use a stronger single-coordinate
error contract.  [Gharibian--Le Gall](https://arxiv.org/abs/2111.09079)
already give
dimension-independent, degree-exponential classical simulation of sparse
polynomial matrix transforms for scalar overlaps.
[Montanaro--Shao](https://arxiv.org/abs/2311.06999) prove qualitatively
matching exponential-in-degree lower bounds for matrix-entry estimation.
The cyclic-clock proof above adapts their block-Hadamard/Forrelation mechanism,
but their theorem concerns matrix-entry estimation rather than
solution-distribution sampling.  Neither source states the sampler, the joint
matching SQ lower bound, or the conditioning-necessity theorem above.  The
result is also consistent with the
[Grønlund--Larsen](https://arxiv.org/abs/2411.02087) lower bound and shows why
their growing condition number is necessary.

The withdrawn Zuo--Li manuscript, arXiv:2307.06627v2, claimed a generic
\(\widetilde O(d\kappa\log(1/\epsilon))\) sparse quantum-inspired solver
and an even stronger SPD result, but its withdrawal explicitly states that
the relevant theorems are incorrect.  Independently, its contraction step
infers
\(G^TG\preceq\beta I\) from the spectral radius of a nonnormal companion
matrix \(G\); for their own vector \(e_1\),
\(\|Ge_1\|^2\geq1>\beta\).  It is not reliable prior art for this theorem.

Applied to QIPMs, (1)--(2) give a sharp exclusion rule.  A constant-degree,
constant-conditioned sparse Newton system with an SQ-preparable right-hand
side cannot support any dimension-polynomial quantum advantage for
solution-state sampling under matched sparse/SQ access.  The one-cone SOCP
separation in the companion note escapes only at the logarithmic
conditioning threshold, and its squared SPD version sits at the sharp
\(\log^2N\) threshold.

The scalar-output boundary is sharper still.  The companion
[Newton-decrement estimator](2026-09-04-sparse-sq-newton-decrement-upper.md)
applies the SPD residual above directly to \(b^*H^{-1}b\), samples coordinates
from \(SQ(b)\), and uses positivity plus the Kantorovich inequality to obtain
relative variance \(O(\kappa)\).  It estimates the decrement in
dimension-independent time

\[
 \exp\!\left(
 O(\sqrt\kappa\log(d+1)\log(1/\epsilon))
 \right)
\]

up to polynomial factors.  The matching
[full-SQ inverse-quadratic lower](2026-09-04-sparse-sq-inverse-quadratic-lower.md)
affine-shifts the Montanaro--Shao clock, uses the exact approximate degree of
the normalized reciprocal, and polarizes a hard inverse entry into two
positive quadratic forms.  A sparse public block Cholesky factor realizes
the same matrix as an exact box-LP analytic-center Hessian.  It matches the
displayed exponential dependence for the full constant-to-high-accuracy
range.  The parameterized SOCP decrement theorem independently supplies a
one-cone structural realization, with its narrower high-accuracy parameter
match.  Unlike the sampler theorem, the scalar upper never builds sampling
access to the inverse solution.

The polynomial factor is also sharp in isolation.  The companion
[sign-block lower bound](2026-09-04-inverse-quadratic-polyfactor-lower.md)
uses two-sparse SPD blocks with public full-SQ metadata to prove
\[
 \Omega\!\left(\min\{N,\kappa/\epsilon^2\}\right)
\]
randomized queries for relative inverse-quadratic estimation.  For coherent
queries, the same commuting family has tight high-dimensional complexity
\(\Theta(\sqrt\kappa/\epsilon)\) by approximate counting and amplitude
estimation.  The
[coherent inverse-quadratic frontier](2026-09-04-coherent-inverse-quadratic-frontier.md)
uses the \(c=1/2\) variable-time negative-power norm estimator to give the
generic block-encoding upper
\(\widetilde O(\alpha\kappa/\epsilon)\), and a canonical-completion hybrid
proves that this is optimal for plain black-box block access.  For exact
sparse-value access that hybrid instance is revealed by one entry query, so
the generic sparse upper \(\widetilde O(d\kappa/\epsilon)\) and the commuting
lower remain separated.  None of these results establishes a product of the
full \(\kappa\epsilon^{-2}\) factor and the full-accuracy exponential
local-walk factor on one family.  Distributional block averaging does give
the weaker same-instance product
\(\epsilon^{-2}s^{\Omega(\sqrt\kappa)}\), with an interpolating tradeoff.
