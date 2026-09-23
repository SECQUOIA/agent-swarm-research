# Tight statistical prefactors for sparse inverse quadratic forms

Status: Proved; targeted literature screen completed; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the reductions; moderate on novelty of the full-SQ matrix
realization

## Main result

Let \(0<\epsilon\leq\epsilon _0\) for a sufficiently small universal
constant and let \(\kappa\geq4\).  There is a family of real, two-sparse SPD
matrices \(H_x\in\mathbb R^{2M\times2M}\), indexed by
\(x\in\{0,1\}^M\), and one public unit vector \(b\), such that

\[
 \kappa^{-1}I\preceq H_x\preceq I,
 \qquad \kappa(H_x)=\kappa,                                \tag{1}
\]

and estimating

\[
 q_x=b^TH_x^{-1}b                                          \tag{2}
\]

to relative error \(\epsilon\), with success probability at least \(2/3\),
requires

\[
 \boxed{\Omega\!\left(\min\left\{M,
            \frac{\kappa}{\epsilon^2}\right\}\right)}     \tag{3}
\]

randomized classical oracle queries.

There is also a sharp high-confidence form.  For failure probability
\(0<\zeta\leq1/10\), whenever
\[
 M\geq C\frac{\kappa}{\epsilon^2}\log\frac1\zeta,
\]
the lower bound strengthens to
\[
 \boxed{\Omega\!\left(
   \frac{\kappa}{\epsilon^2}\log\frac1\zeta
 \right).}                                                \tag{3a}
\]

The lower bound survives the strongest usual sampling-and-query interface
for the matrix: entry and sparse-location queries, row and column norm
queries, conditional squared-entry sampling, global squared-entry sampling,
and the Frobenius norm.  It also survives exact \(SQ(b)\).  All sampling
probabilities and all norms are public; only signs of off-diagonal entries
contain input bits.

Moreover, \(H_x\) is, up to the factor two, the exact barrier Hessian at the
public analytic center of a two-sparse box LP with the same full-SQ
simulation.  Thus (3) is a genuine local Newton-decrement lower bound, not
only an abstract SPD-oracle construction.

Consequently the \(O(\kappa\epsilon^{-2})\) statistical factor in the
companion dimension-independent Newton-decrement estimator is worst-case
optimal.  This statement is only about that polynomial factor.  It does not
prove that the full \(\kappa\epsilon^{-2}\) factor must multiply the
estimator's full-accuracy exponential local-walk cost.  The companion
[composition note](2026-09-04-inverse-quadratic-product-composition-obstruction.md)
does prove a weaker but genuine same-instance product
\(\epsilon^{-2}s^{\Omega(\sqrt\kappa)}\), and a continuous tradeoff between
that constant-contrast endpoint and the full-accuracy clock endpoint.

In the coherent quantum version of the same oracle model, if
\(M\geq C\kappa/\epsilon\), the family gives

\[
 \boxed{\Omega(\sqrt\kappa/\epsilon)}                     \tag{4}
\]

queries.  This is tight on the constructed public-eigenbasis commuting
family: quantum amplitude estimation gives
\(O(\sqrt\kappa/\epsilon)\) queries.  The companion
[coherent frontier note](2026-09-04-coherent-inverse-quadratic-frontier.md)
shows that a generic variable-time negative-power routine instead gives
\(\widetilde O(\alpha\kappa/\epsilon)\), and proves this optimal in the
plain black-box block-encoding model.  A fixed inverse-square-root QSVT
circuit followed by multiplicative amplitude estimation gives only
\(\widetilde O(\alpha\kappa^{3/2}/\epsilon)\).  Under exact sparse-value
access the black-box lower does not apply, so the gap between (4) and the
generic \(\widetilde O(d\kappa/\epsilon)\) sparse upper remains open.

## A two-by-two sign gadget with public SQ metadata

Put

\[
 a=\kappa^{-1},\qquad m=\frac{1+a}{2},\qquad
 h=\frac{1-a}{2},
\]

and, for \(z\in\{0,1\}\), define

\[
 B_z=
 \begin{pmatrix}
  m&(-1)^z h\\
  (-1)^z h&m
 \end{pmatrix}.                                           \tag{5}
\]

Every block has eigenvalues \(a,1\).  Its support, entry magnitudes, row and
column squared norms \(m^2+h^2\), and Frobenius norm are independent of
\(z\).  Let

\[
 H_x=\bigoplus_{j=1}^M B_{x_j},\qquad
 b=\frac1{\sqrt M}\bigoplus_{j=1}^M
       \frac{(1,1)^T}{\sqrt2}.                            \tag{6}
\]

The vector \(b\) is public and has a trivial exact SQ implementation.
Writing \(w=|x|\), the plus vector in block \(j\) has eigenvalue \(1\) when
\(x_j=0\) and eigenvalue \(a\) when \(x_j=1\).  Therefore

\[
 q_x=1+(\kappa-1)\frac{w}{M}.                             \tag{7}
\]

An entry-value query to \(H_x\) uses at most one query to \(x_j\).
Conversely, all norm and squared-magnitude sampling operations can be
implemented without querying \(x\); if a sampled value is requested, one
bit query supplies its sign.  Hence any algorithm using the full matrix SQ
interface yields, with at most constant overhead, a bit-query algorithm for
the Hamming-weight statistic (7).  This is why the construction uses sign
blocks rather than a diagonal matrix: for the naive diagonal construction,
the exact Frobenius norm would reveal the Hamming weight.

For the quantum statement, “coherent full SQ” means the canonical reversible
lifts of these same operations.  The sparse-location, norm, and sampling
unitaries are fixed public circuits.  A reversible matrix-value query uses
one standard bit query to write the sign and then uncomputes its workspace.
Thus every coherent matrix/SQ query has a constant-query simulation from the
standard bit oracle.  The lower bound does not grant an unspecified unitary
completion that is allowed to encode additional information about \(x\).

## Exact sparse box-LP realization

Let

\[
 u=\frac{1+\sqrt a}{2},\qquad v=\frac{1-\sqrt a}{2},
\qquad
 C_z=\begin{pmatrix}u&(-1)^zv\\(-1)^zv&u\end{pmatrix}.       \tag{7a}
\]

Then \(C_z^2=B_z\).  Put \(C_x=\bigoplus_j C_{x_j}\) and consider

\[
 \max_y\ \eta b^Ty
 \qquad\text{subject to}\qquad
 -\mathbf1\leq C_xy\leq\mathbf1,                            \tag{7b}
\]

where, for example, the public choice \(\eta=1/(4\sqrt\kappa)\) puts every
instance in a uniform small-decrement neighborhood.  Its paired logarithmic barrier is
\(\phi(y)=-\sum_i\log(1-(C_xy)_i^2)\).  At the exact public analytic center
\(y=0\),

\[
 \nabla^2\phi(0)=2C_x^TC_x=2H_x,\qquad
 \Lambda_\eta^2=\frac{\eta^2}{2}\,b^TH_x^{-1}b.             \tag{7c}
\]

Indeed \(b^TH_x^{-1}b\leq\kappa\), so this choice gives
\(\Lambda_\eta^2\leq1/32\).

Every row and column of \(C_x\) has two nonzeros.  As for \(H_x\), all
supports, magnitudes, norms, and squared-entry sampling distributions are
public; only an off-diagonal sign queries \(x_j\).  Relative estimation of
the squared decrement in (7c) is therefore exactly the task already shown
hard.  The box barrier has ambient parameter \(\Theta(M)\), so this is a
local scalar diagnostic lower bound rather than an iteration-count lower
bound.

## Classical lower bound

We use the standard weight-distinguishing lemma.  If
\(1\leq t\leq M/4\), \(1\leq\Delta\leq t/4\), and an input is promised to
have Hamming weight either \(t\) or \(t+\Delta\), its randomized query
complexity is

\[
 \Omega\!\left(\min\left\{M,
              \frac{tM}{\Delta^2}\right\}\right).         \tag{8}
\]

One proof applies Yao's principle to the uniform distributions on the two
Hamming spheres.  Until a constant fraction of the coordinates have been
queried, the transcript is sampling without replacement.  The chain rule
for relative entropy bounds the information per fresh query by
\(O(\Delta^2/(tM))\); if the displayed expression exceeds \(M\), the same
hypergeometric argument up to a fixed fraction of all coordinates gives an
\(\Omega(M)\) bound.  Pinsker's inequality then prevents constant-bias
distinguishing.  This is the variance-sensitive form of the usual classical
approximate-counting lower bound.

Take \(\epsilon _0=1/128\).  For
\(M\geq \kappa/(8\epsilon)\), put

\[
 t=\left\lfloor\frac{M}{\kappa}\right\rfloor,
 \qquad
 \Delta=\left\lceil 8\epsilon\frac{M}{\kappa}\right\rceil. \tag{9}
\]

To check the endpoint without suppressing rounding, write
\(u=M/\kappa\).  Then \(u\geq1/(8\epsilon)\), and
\[
 t\geq u-1,
 \qquad
 \Delta\leq8\epsilon u+1\leq (u-1)/4\leq t/4.
\]
The middle inequality follows from \(\epsilon\leq1/128\).  Also
\(t\leq M/4\), since \(\kappa\geq4\), so (8) applies.  If \(q_t\) and
\(q_{t+\Delta}\) are the two values in (7), then
\[
 q_t<2,
 \qquad
 q_{t+\Delta}-q_t
 =\frac{(\kappa-1)\Delta}{M}
 \geq8\epsilon\frac{\kappa-1}{\kappa}
 \geq6\epsilon.
\]
Thus \((1-\epsilon)q_{t+\Delta}>(1+\epsilon)q_t\): the two
relative-error output intervals are disjoint.  Substitution in (8) gives

\[
 \Omega\!\left(\min\left\{M,
              \frac{\kappa}{\epsilon^2}\right\}\right).   \tag{10}
\]

For \(M<\kappa/(8\epsilon)\), distinguish weights zero and one.  Here
\[
 q_1-q_0=\frac{\kappa-1}{M}
 >8\epsilon\frac{\kappa-1}{\kappa}\geq6\epsilon,
\]
so the same interval check applies.  Finding whether a uniformly hidden
marked coordinate exists costs \(\Omega(M)\) randomized queries, and in this
regime \(M<\kappa/\epsilon^2\).  This completes (3), including every
finite-\(M\) regime, up to universal constants and the inessential \(2M\)
versus \(M\) dimension convention.

The hard regime explaining the Kantorovich factor is transparent: a
\(\Theta(1/\kappa)\) fraction of the spectral mass has inverse eigenvalue
\(\kappa\), and the rest has inverse eigenvalue one.  The quadratic form is
constant scale, but its coefficient of variation is \(\Theta(\sqrt\kappa)\).

### High confidence

The logarithm in (3a) follows from a two-distribution version of the same
reduction.  Draw the hidden bits independently with the explicit choices
\[
 p_0=\frac1\kappa,\qquad
 p_1=\frac{1+16\epsilon}{\kappa}.                          \tag{10a}
\]
Let \(W_b\sim\operatorname{Bin}(M,p_b)\).  Multiplicative Chernoff bounds and
the displayed lower bound on \(M\) give, under either hypothesis,
\[
 \Pr\!\left[
  |W_b-Mp_b|>2\epsilon M/\kappa
 \right]
 \leq \exp(-\Omega(M\epsilon^2/\kappa))
 \leq O(\zeta).
\]
On these concentration events, the two weights differ by at least
\(12\epsilon M/\kappa\), so their values in (7) differ by at least
\(9\epsilon\), using \((\kappa-1)/\kappa\geq3/4\).  Both values are below
\(3\) for \(\epsilon\leq1/128\).  Hence their relative-\(\epsilon\) output
intervals are disjoint, with constant slack.

For a deterministic adaptive decision tree, each previously unseen queried
bit is Bernoulli with parameter \(p_0\) or \(p_1\), regardless of the
adaptively selected coordinate, and
\[
 D_{\rm KL}(\operatorname{Ber}(p_0)\|
            \operatorname{Ber}(p_1))
 =O(\epsilon^2/\kappa).                                   \tag{10b}
\]
Repeated-coordinate queries give no new information.  The KL chain rule
therefore bounds the transcript divergence after \(T\) informative queries
by \(O(T\epsilon^2/\kappa)\).  On the other hand, composing a
relative-error estimator with the threshold between the two separated output
bands gives a test with error \(O(\zeta)\).  Binary data processing then
requires transcript divergence \(\Omega(\log(1/\zeta))\).  Hence the number
of matrix-value queries is
\[
 \Omega\!\left(
  \frac{\kappa}{\epsilon^2}\log\frac1\zeta
 \right).
\]
Yao's principle converts this distributional statement into the worst-case
query lower bound (3a).  The same reasoning covers the full-SQ interface:
all norm and squared-magnitude samples are public, and requesting a sampled
value exposes at most one Bernoulli bit, just like one addressed value query.
Thus the confidence logarithm in the companion median-of-means upper is
necessary as well, once the ambient population is large enough to support
that confidence.

## Quantum lower and matching commuting upper

Nayak and Wu's weight-decision theorem gives, for weights \(t\) and
\(t+\Delta\), quantum query complexity

\[
 \Omega\!\left(
   \sqrt{\frac{M}{\Delta}}+
   \frac{\sqrt{t(M-t)}}{\Delta}
 \right).                                                 \tag{11}
\]

With (9), and \(M\geq C\kappa/\epsilon\) for a sufficiently large universal
\(C\), the rounding in \(t\) and \(\Delta\) changes only constants and the
second term is \(\Omega(\sqrt\kappa/\epsilon)\), proving (4).  The first
term is \(\Theta(\sqrt{\kappa/\epsilon})\) and is smaller for
\(\epsilon\leq1\).  For smaller dimensions, the same construction gives the
more detailed finite-size weight-decision lower bounds; (4) is stated only
where the clean dimension-independent expression is valid.

For the matching upper on this commuting family, prepare the uniform block
index and compute from the queried sign a random variable
\(Y_j\in\{1,\kappa\}\).  A controlled rotation whose success probability is
\(Y_j/\kappa\) has mean

\[
 p=\frac{q_x}{\kappa}\geq\frac1\kappa.                   \tag{12}
\]

Multiplicative amplitude estimation estimates \(p\) relatively with

\[
 O\!\left(\frac1{\epsilon\sqrt p}\right)
 =O(\sqrt\kappa/\epsilon)                                \tag{13}
\]

coherent bit, matrix-value, and state-preparation queries.  Thus (11) is
not merely a lower-bound artifact: it is the exact worst-case
condition--accuracy law for this public-eigenbasis commuting family when
\(M\) is large enough.

## A fixed-circuit inverse-square-root baseline

Suppose a quantum algorithm is given an \((\alpha,a,0)\) block encoding of
\(H\), so its signal singular values lie in
\[
 \left[\frac1{\alpha\kappa},\frac1\alpha\right],
\]
and a unitary preparing \(|b\rangle\).  Corollary 67 of
[Gilyén--Su--Low--Wiebe](https://arxiv.org/abs/1806.01838), with
\(c=1/2\) and \(\delta=(\alpha\kappa)^{-1}\), supplies an even polynomial
approximating
\[
 g(x)=\frac12\sqrt{\frac{\delta}{x}}
\]
on \(x\in[\delta,1]\).  The polynomial is bounded by one on
\([-1,1]\), has the parity required for QSVT, and has
degree
\[
 D=O\!\left(\alpha\kappa
       \log\frac1{\eta}\right).                            \tag{14}
\]

On the spectrum of \(H/\alpha\), its ideal transform is
\[
 g(H/\alpha)=\frac1{2\sqrt\kappa}H^{-1/2}.
\]
Applying the transformed block encoding to \(|b\rangle\), the success
probability is therefore
\[
 p=\frac1{4\kappa}\langle b|H^{-1}|b\rangle
   =\frac{q}{4\kappa}\geq\frac1{4\kappa}.                  \tag{15}
\]

Choose operator-norm polynomial error
\(\eta=\Theta(\epsilon/\kappa)\).  The induced probability error is at most
\(2\eta+\eta^2=O(\epsilon/\kappa)\); with a sufficiently small hidden
constant, this is at most a constant fraction of \(\epsilon p\).
(The sharper state-norm estimate would permit
\(\eta=\Theta(\epsilon/\sqrt\kappa)\), but this changes only a logarithm.)
Multiplicative amplitude estimation uses
\[
 O\!\left(\frac1{\epsilon\sqrt p}\right)
 =O(\sqrt\kappa/\epsilon)                                 \tag{16}
\]
applications of the transformed state-preparation circuit.  Multiplying
(14) and (16) gives (4a), up to logarithmic factors and lower-order
state-preparation calls.

This is a deliberately elementary baseline.  It does not use variable-time
amplitude estimation.  The companion
[coherent frontier note](2026-09-04-coherent-inverse-quadratic-frontier.md)
specializes the negative-power variable-time theorem to \(c=1/2\), improving
this to \(\widetilde O(\alpha\kappa/\epsilon)\).

## Literature boundary

[Nayak--Wu](https://arxiv.org/abs/quant-ph/9804066) prove the symmetric
partial-function degree bound behind (11) and show that quantum approximate
counting matches it.  Classical bound (8) is the standard
sampling-without-replacement counterpart.  The use of these counting
theorems is not new.

[Brassard--Hoyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055)
give amplitude estimation and approximate counting, which imply (13).
[Li--Sra--Jegelka](https://proceedings.mlr.press/v48/lig16.html) study
matrix-inverse quadratic forms through Lanczos quadrature in the ordinary
matrix-vector model.  The open [quantum algorithms for data analysis
notes](https://quantumalgorithms.org/chap-toolbox.html) state an
\(O(\mu(A)\kappa(A)/\epsilon)\) inverse-quadratic routine in Lemma 5.7.
Their displayed proof does not transparently separate transform and
estimation costs.  The coherent frontier note gives a clean oracle-level
justification from Theorem 33 of
[Chakraborty--Gilyén--Jeffery](https://arxiv.org/abs/1804.01973):
specialize their variable-time negative-power norm estimator to \(c=1/2\),
then square the relative norm estimate.  Equations (14)--(16) remain useful
as the simpler fixed-QSVT comparison.

The apparently new point is the exact two-sparse sign-block embedding (5):
it turns the variance-sensitive approximate-counting lower bound into a
relative inverse-quadratic lower bound while keeping every norm and every
squared-magnitude sampling distribution public.  A targeted search found no
prior statement that the \(\kappa\epsilon^{-2}\) Kantorovich prefactor is
necessary for sparse-SPD inverse quadratic forms under full matrix SQ, but
this is evidence of apparent novelty rather than a priority guarantee.

## Scope

- The result applies directly to squared Newton decrements once \(H\) and
  \(b\) are supplied through the stated oracle contract, and (7b)--(7c)
  realize it as an exact box-LP analytic-center decrement.  It does not
  control a complete changing-Hessian IPM trajectory.
- Exact row norms or the Frobenius norm do not leak the answer.  This is
  stronger than a diagonal rare-eigenvalue construction.
- The classical theorem makes the polynomial statistical prefactor sharp,
  while the companion clock theorem makes the exponential local-evaluation
  dependence sharp.  Distributional block averaging forces an
  \(\epsilon^{-2}\) factor and a constant-accuracy clock factor on one
  instance.  A theorem forcing the full \(\kappa\epsilon^{-2}\) factor and
  the full-accuracy clock factor simultaneously remains open.
- The quantum lower bound applies to the generic problem through a commuting
  hard subfamily, but no matching upper is proved here for general
  noncommuting sparse matrices.  Claiming a
  \(\Theta(\sqrt\kappa/\epsilon)\) quantum theorem beyond the commuting
  subclass would require a new algorithm or a stronger lower bound.
