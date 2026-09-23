# Coherent inverse quadratic forms: the block-encoding frontier

Status: Proved; independently audited and targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the upper bound and fixed-transform obstruction; high on
the black-box hybrid lower, subject to the stated oracle-model boundary  

## Result

Let \(H\) be Hermitian positive definite,

\[
  \kappa^{-1}I\preceq H\preceq I,
\]

and let \(U_H\) be a controlled \((\alpha,a,\delta_{\rm in})\) block
encoding of \(H\).  Suppose \(U_b\) prepares the normalized state

\[
  |b\rangle=b/\|b\|,
\]

and that \(\|b\|\) is known.  For \(0<\epsilon\leq1/4\), variable-time
amplitude estimation applied to the negative power \(c=1/2\) gives a
relative estimate of

\[
  Q=b^*H^{-1}b
\]

with constant success probability using

\[
 \boxed{
  \widetilde O\!\left(
    \frac{\alpha\kappa}{\epsilon}
  \right)}                                               \tag{1}
\]

queries to \(U_H,U_H^\dagger\).  Keeping state preparation explicit, the
gate/query cost supplied by Theorem 33 of
[Chakraborty--Gilyén--Jeffery](https://arxiv.org/abs/1804.01973) is

\[
 O\!\left(
 \frac{\log^3\kappa}{\epsilon}
 \left[
   \alpha\kappa(T_H+a)\log^2\!\frac{\kappa}{\epsilon}
   +\sqrt\kappa\,T_b
 \right]
 \log\!\frac{\log\kappa}{\zeta}
 \right),                                                \tag{2}
\]

for failure probability at most \(\zeta\), up to harmless changes inside
the logarithms.  Their stated sufficient input-encoding accuracy, after
setting \(c=1/2\), is

\[
 \delta_{\rm in}
 =o\!\left(
 \frac{\epsilon}{\kappa\log^3(\kappa/\epsilon)}
 \right).                                                \tag{3}
\]

Thus a standard \(d\)-sparse block encoding with
\(\alpha\leq d\|H\|_{\max}\leq d\) gives

\[
 \widetilde O(d\kappa/\epsilon)                          \tag{4}
\]

sparse-oracle queries, plus the displayed state-preparation term.  More
generally one should retain the actual available normalization \(\alpha\),
rather than replace it by \(d\).

The dependence in (1) is optimal, up to polylogarithmic factors, in the **plain
black-box block-encoding model**:

\[
 \boxed{
  Q_{\rm BE}(\alpha,\kappa,\epsilon)
  =\widetilde\Theta(\alpha\kappa/\epsilon),
 }                                                        \tag{5}
\]

where \(\widetilde\Theta\) means an exact
\(\Omega(\alpha\kappa/\epsilon)\) lower bound and an upper bound with only
polylogarithmic overhead.

The lower bound already uses diagonal three-dimensional SPD matrices and a
public basis vector.  It does **not** transfer to an exact sparse-entry
value oracle, because one such value query reveals the varying diagonal
entry.  Under exact sparse access, the current generic gap is instead

\[
 \Omega(\sqrt\kappa/\epsilon)
 \ \leq\ Q_{\rm sparse}\ \leq\
 \widetilde O(d\kappa/\epsilon),                          \tag{6}
\]

where the lower bound is the full-SQ sign-block approximate-counting family.

## Why the inverse square root is the right observable

Put

\[
 R=\|H^{-1/2}|b\rangle\|,
 \qquad q=\langle b|H^{-1}|b\rangle=R^2.
\]

The negative-power routine with \(c=1/2\) outputs a number \(\Gamma\) such
that

\[
 1-\eta\leq\Gamma/R\leq1+\eta.
\]

Taking \(\eta=\epsilon/3\) gives

\[
 (1-\epsilon)q\leq\Gamma^2\leq(1+\epsilon)q
\]

for \(\epsilon\leq1\).  Multiplication by the known \(\|b\|^2\) recovers
\(Q\).  For a Newton system, this is exactly the squared Newton decrement
when \(H\) is the local Hessian and \(b\) is the local gradient/residual.

The improvement over one fixed QSVT circuit is the variable stopping time.
The algorithm resolves different dyadic spectral bands to different
precisions and applies variable-time amplitude estimation to the resulting
inverse-square-root success branch.  It is not legitimate to multiply the
worst spectral-resolution time by the worst inverse-root postselection
factor; doing so loses a factor \(\sqrt\kappa\).

## The tempting fixed-QSVT composition loses \(\sqrt\kappa\)

A useful baseline is a normalized inverse-root block encoding

\[
 B\simeq \frac{H^{-1/2}}{2\sqrt\kappa}.
\]

Applied to \(|b\rangle\), its success probability is

\[
 p=\|B|b\rangle\|^2
   =\frac{q}{4\kappa}
   \in\left[\frac1{4\kappa},\frac14\right].              \tag{7}
\]

The usual amplitude-estimation guarantee

\[
 |\widehat p-p|
 \leq O(\sqrt p/M+M^{-2})
\]

therefore gives a relative estimate with
\(M=O(1/(\epsilon\sqrt p))=O(\sqrt\kappa/\epsilon)\) calls
to the inverse-root circuit.  A uniform top-block error
\(O(\epsilon/\sqrt\kappa)\) is enough: if
\(\|\widetilde B-B\|\leq\xi\), then

\[
 |\|\widetilde B b\|^2-\|Bb\|^2|
 \leq2\xi\sqrt p+\xi^2.
\]

However, producing this one globally bounded transform costs
\(\widetilde O(\alpha\kappa)\) block queries.  The resulting fixed-circuit
bound is only

\[
 \widetilde O(\alpha\kappa^{3/2}/\epsilon).               \tag{8}
\]

This corrects the still more conservative direct-inverse/matrix-element
composition, which pays another square-root factor.

### Global boundedness forces the linear transform degree

The \(\widetilde O(\alpha\kappa)\) cost in (8) cannot be replaced by a
Chebyshev-looking \(\widetilde O(\sqrt{\alpha\kappa})\) degree while keeping
one unitary polynomial transform.  Let \(P\) be any real or complex degree-
\(n\) polynomial with

\[
 |P(x)|\leq1\qquad(-1\leq x\leq1)
\]

that approximates

\[
 f(x)=\frac1{2\sqrt{\alpha\kappa x}}
\]

to error at most \(1/32\) at the two signal values

\[
 x_1=\frac1{\alpha\kappa},\qquad
 x_2=\frac4{\alpha\kappa}.
\]

For \(\kappa\geq8\), the real part of \(P\) changes by a positive constant
over an interval of length \(3/(\alpha\kappa)\).  The mean-value theorem and
the interior Bernstein inequality imply

\[
 \Omega(\alpha\kappa)
 \leq |(\operatorname{Re}P)'(\xi)|
 \leq \frac{n}{\sqrt{1-\xi^2}}
 =O(n),                                                   \tag{9}
\]

so \(n=\Omega(\alpha\kappa)\).

This is an interior-point obstruction, not the endpoint Markov scale.  An
ordinary Chebyshev approximation on the physical positive interval can have
degree \(O(\sqrt\kappa\log(1/\eta))\), but it becomes too large on the rest
of the QSVT signal interval.  The unitary implementation requires global
boundedness.

Ordinary one-sequence QSVT also imposes definite parity.  The arbitrary-
parity construction in Gilyén--Su--Low--Wiebe combines the even and odd
parts coherently with constant overhead, and
[generalized QSP](https://arxiv.org/abs/2308.01501) removes the same
restriction directly.  Neither changes \(|P|\leq1\) on the full signal
interval, so neither evades (9).  Parity is therefore not the source of the
linear \(\alpha\kappa\) degree.  In the Laurent-polynomial parameterization
used by generalized QSP, the two signal phases
\(\arccos x_1,\arccos x_2\) are separated by
\(\Theta(1/(\alpha\kappa))\).  The trigonometric Bernstein inequality
\(\|F'\|_\infty\leq n\|F\|_\infty\) gives the same
\(\Omega(\alpha\kappa)\) degree bound directly.  This obstruction is scoped
to one bounded polynomial/Laurent-polynomial transform.  It is not a lower
bound for variable-time, rational, or postselected algorithms.

## Matching black-box lower bound

Fix \(0<\epsilon\leq1/16\), \(\kappa\geq4\), and \(\alpha\geq1\).  Define

\[
 H_z=\operatorname{diag}\!\left(
 \frac1\kappa,
 \frac{2(1+4\epsilon z)}\kappa,
 1
 \right),\qquad z\in\{0,1\},                             \tag{10}
\]

and \(b=e_2\).  Both matrices have condition number exactly \(\kappa\), and

\[
 q_0=\frac\kappa2,
 \qquad
 q_1=\frac{\kappa}{2(1+4\epsilon)}.                       \tag{11}
\]

Their relative-\(\epsilon\) output intervals are disjoint because

\[
 (1-\epsilon)(1+4\epsilon)>1+\epsilon.
\]

For a Hermitian contraction \(A\), use the canonical exact completion

\[
 W(A)=
 \begin{pmatrix}
 A&\sqrt{I-A^2}\\
 \sqrt{I-A^2}&-A
 \end{pmatrix}.                                          \tag{12}
\]

Then \(U_z=W(H_z/\alpha)\) is an exact controlled
\((\alpha,1,0)\) block encoding of \(H_z\).  The two unitaries differ only
on the varying scalar block.  Since that scalar remains below \(2/3\), the
map \(x\mapsto\sqrt{1-x^2}\) has bounded derivative there, and hence

\[
 \|U_0-U_1\|=O\!\left(\frac\epsilon{\alpha\kappa}\right). \tag{13}
\]

The standard hybrid argument bounds the distance between the final states
of every \(T\)-query adaptive algorithm by
\(T\|U_0-U_1\|\).  Constant-bias distinction of the disjoint intervals in
(11) therefore requires

\[
 T=\Omega(\alpha\kappa/\epsilon),                         \tag{14}
\]

proving the lower half of (5).  Controlled queries and inverse queries have
the same norm difference, so granting them does not weaken the argument.

The matrices in (10) happen to be one-sparse, but (14) is emphatically an
oracle-completion lower bound.  If the interface returns a diagonal value
as a classical bit string, the second diagonal query distinguishes the two
instances immediately.  This is why (14) and the sparse/full-SQ counting
lower bound answer different questions.

## Relation to the commuting counting lower

The sign-block family in the companion
[polyfactor note](2026-09-04-inverse-quadratic-polyfactor-lower.md) has
public eigenvalues \(\{1/\kappa,1\}\); hidden signs only decide which known
eigenspace receives the input mass.  It has the tight coherent law

\[
 \Theta(\sqrt\kappa/\epsilon)
\]

because it reduces exactly to approximate counting.  The lower bound (14)
uses a different obstruction: the relevant eigenvalue itself is unknown to
relative precision \(\Theta(\epsilon)\), and a normalized block encoding
changes by only \(\Theta(\epsilon/(\alpha\kappa))\).  Thus there is no
contradiction:

- public spectral values / commuting counting: \(\Theta(\sqrt\kappa/\epsilon)\);
- generic black-box block encoding: \(\widetilde\Theta(\alpha\kappa/\epsilon)\);
- exact sparse-value access: still between these two laws, with the upper
  normalization specialized to \(\alpha\leq d\).

## Literature boundary and novelty assessment

The upper bound is not new as a negative-power primitive.  It is the direct
\(c=1/2\) specialization of Theorem 33 in
[Chakraborty--Gilyén--Jeffery](https://arxiv.org/abs/1804.01973), whose
variable-time amplitude-estimation theorem explicitly estimates
\(\|H^{-c}|b\rangle\|\) multiplicatively.  Squaring that estimate gives the
inverse quadratic form.  The online *Quantum Algorithms for Data Analysis*
notes state an \(O(\mu(A)\kappa(A)/\epsilon)\) inverse-quadratic routine, but
their proof sketch obscures this norm-estimation route; Theorem 33 supplies
the clean oracle-level justification.

[Brassard--Høyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055)
supplies the amplitude-estimation error law used in the fixed-transform
comparison.  Gilyén--Su--Low--Wiebe supply the arbitrary-parity polynomial
eigenvalue transformation and globally bounded negative-power
approximants.  Generalized QSP removes polynomial-family restrictions but
retains the unitary boundedness that drives (9).

The apparently new contribution here is the exact frontier statement (5)
for relative inverse quadratic forms, including the elementary
three-dimensional completion lower bound, and its explicit separation from
the stronger sparse-entry oracle.  A targeted search found no prior theorem
stating this matching 
\(\widetilde\Theta(\alpha\kappa/\epsilon)\) law for the scalar inverse
quadratic observable.  This is an apparent-novelty claim, not a priority
guarantee.

## Scope

- Equation (5) is a query theorem for black-box block encodings, not an
  end-to-end gate theorem for loading a sparse matrix.
- Equation (4) is an upper bound under sparse access.  Its matching lower is
  not proved in that stronger oracle model.
- The theorem estimates one positive quadratic observable.  Bilinear forms
  can cancel and do not inherit a relative guarantee without an overlap
  promise.
- The result is local when interpreted as a Newton decrement.  It does not
  include the number of IPM iterations, changing-Hessian maintenance, or
  classical output of a Newton direction.
