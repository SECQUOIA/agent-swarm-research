# Relative-value parity lower bound and barriers to linear-size residual amplification

Date: 2026-09-02

## Summary

This note records one strengthening of the signed-path LP and two limitations on
trying to obtain constant-relative-\(\ell_2\)-residual hardness with only
\(O(N)\) variables.

1. A harmless reweighting makes the two possible optimal values \(3/4\) and
   \(5/4\). Thus even a constant-relative approximation of a positive,
   constant-size optimal value needs \(\Omega(N)\) coefficient queries. The
   objective has constant Euclidean norm, the LP remains bounded and strictly
   primal-dual feasible, and its reduced central-path Hessian still has condition
   number one.
2. Within the parallel-path amplification used in Theorem 3 of
   `2026-09-02-parity-amplified-primal-state-lower-bound.md`, constant
   \(\ell_2\)-residual soundness forces \(\Omega(N)\) length-\(N\) path copies.
   The resulting quadratic size is therefore intrinsic to that architecture,
   not merely an artifact of its proof constants.
3. A long-range two-coordinate shortcut that is valid on every signed path must
   itself contain an interval parity in its coefficient ratio. Such a row cannot
   be simulated with \(O(1)\) queries to the original sign oracle. This blocks the
   most direct attempt to replace the parallel paths by a linear-size expander.

The last two statements are architecture-specific. They do **not** prove that
every bounded-degree real-linear parity gadget with constant residual soundness
has quadratic size.

## 1. Constant-relative optimal-value hardness

Let

\[
 \sigma_1,\ldots,\sigma_N\in\{-1,+1\},\qquad
 p_0=1,\quad p_i=\prod_{k=1}^i\sigma_k,
\]

and introduce \(u_i,v_i\ge0\), \(d_i=u_i-v_i\), and
\(q_i=u_i+v_i\) for \(0\le i\le N\). Set

\[
 w=\frac1{N+1},\qquad \alpha=\frac14,
\]

and consider

\[
\begin{aligned}
 \min_{u,v\ge0}\quad &
 w\sum_{i=0}^N(u_i+v_i)+\alpha(u_N-v_N),\\
 \text{subject to}\quad &d_0=1,\\
 &d_i-\sigma_i d_{i-1}=0\qquad(1\le i\le N).
\end{aligned}                                                    \tag{1}
\]

The support, right-hand side, and objective are independent of the hidden signs.
Every row has at most four nonzeros and every column at most two. All matrix
coefficients have magnitude one. Moreover,

\[
 \|b\|_2=1,
 \qquad
 \|c\|_2^2=2(N+1)w^2+2\alpha^2
            =\frac{2}{N+1}+\frac18=O(1).                \tag{2}
\]

The coefficient \(w\) requires only \(O(\log N)\) bits and is not hidden input.

### Theorem 1 (coarse multiplicative value approximation is parity-hard)

In the coherent fixed-position sparse coefficient-oracle model, estimating the
optimal value of (1) to relative error \(\epsilon<1/4\), with bounded
success probability, requires \(\Omega(N)\) coefficient queries. This remains
true although (1) is bounded and strictly primal-dual feasible, has a unique
nondegenerate strictly complementary optimum, and has a condition-one reduced
primal logarithmic-barrier Hessian at every point of its central path.

Equivalently, even distinguishing the promises

\[
 \operatorname{OPT}=\frac34
 \quad\hbox{and}\quad
 \operatorname{OPT}=\frac54                                      \tag{3}
\]

needs \(\Omega(N)\) queries. If an algorithm returns an exactly feasible point
rather than a value estimate, the much weaker guarantee

\[
 c^Tx\le\frac32\operatorname{OPT}                                \tag{4}
\]

already suffices for the same reduction.

#### Proof

The triangular signed-difference constraints force \(d_i=p_i\). Hence

\[
 u_i=\frac{q_i+p_i}{2},\qquad
 v_i=\frac{q_i-p_i}{2},\qquad q_i\ge1.                    \tag{5}
\]

On this affine space the objective is

\[
 w\sum_{i=0}^Nq_i+\alpha p_N.                              \tag{6}
\]

Its unique minimum has every \(q_i=1\), and consequently

\[
 \operatorname{OPT}=w(N+1)+\alpha p_N=1+\frac14p_N.       \tag{7}
\]

A relative-error interval of radius \(\epsilon\) around \(3/4\) is disjoint
from the corresponding interval around \(5/4\) whenever \(\epsilon<1/4\).
Thus a relative value estimator computes \(p_N\). For (4), when \(p_N=-1\)
the returned objective is at most \(9/8\), whereas when \(p_N=+1\) every
feasible objective is at least \(5/4\). A fixed threshold distinguishes the
two cases.

Every sparse row or column query reveals at most one hidden sign and is simulated
coherently by \(O(1)\) standard sign-oracle queries. Bounded-error quantum parity
needs \(\Omega(N)\) sign queries, proving the lower bound.

For regularity, taking all \(q_i=2\) gives strict primal feasibility. The
equality matrix has full row rank and null space

\[
 \operatorname{null}(A)=
 \operatorname{span}\left\{
   \frac{e_{u_i}+e_{v_i}}{\sqrt2}:0\le i\le N
 \right\}.                                                \tag{8}
\]

Choose the positive dual slack \(s_{u_i}=s_{v_i}=w\) for every \(i\). Then
\(c-s=\alpha(e_{u_N}-e_{v_N})\), which is orthogonal to (8), and therefore lies
in \(\operatorname{range}(A^T)\). Hence a multiplier \(y\) exists with
\(A^Ty+s=c\), proving strict dual feasibility even though
\(c_{v_N}=w-\alpha\) is negative for large \(N\). The same triangular positive
column basis used for the unweighted signed-path LP proves nondegeneracy and
strict complementarity at the unique optimum.

Finally, on the feasible affine space the primal barrier is

\[
 \Phi_\mu(q)=
 \sum_{i=0}^N\left[
    wq_i-\mu\log\frac{q_i^2-1}{4}
 \right]+\alpha p_N.                                      \tag{9}
\]

All central coordinates are equal and solve

\[
 w=\frac{2\mu q}{q^2-1},
 \qquad
 q(\mu)=\frac{\mu}{w}+
         \sqrt{\left(\frac{\mu}{w}\right)^2+1}.          \tag{10}
\]

In the orthonormal basis (8), the reduced Hessian is a positive scalar multiple
of the identity. Its spectral condition number is one for every \(\mu>0\).
In particular, \(q=2\) at \(\mu=3w/4\). \(\square\)

### Interpretation and limitation

The earlier unweighted path has optimum \(N+1+\alpha p_N\), so constant
relative error swamps the parity gap unless one first subtracts the known
extensive term. The normalized objective in (1) removes that qualification:
the reported optimum itself is positive, \(\Theta(1)\), and separated by a
constant factor. This is a value-output lower bound, not a lower bound for every
decision version of LP; indeed, the constraints deliberately encode parity.

The result is a normalization strengthening rather than a new adversary method.
It should not be advertised as superseding stronger dimension-dependent LP query
lower bounds in other parameter regimes.

## 2. Why one path cannot tolerate constant \(\ell_2\) residual

Write \(z_i=p_i d_i\). The signed transition residual becomes

\[
 d_i-\sigma_i d_{i-1}=p_i(z_i-z_{i-1}).                   \tag{11}
\]

Set

\[
 z_i=1-\frac{2i}{N}.                                      \tag{12}
\]

Then the root is exact, the endpoint has the wrong sign, and all \(N\)
transition residuals have magnitude \(2/N\). Their total Euclidean norm is
\(2/\sqrt N\). Any number of input-independent exact copies of the endpoint can
therefore amplify the wrong value without increasing the residual. In the capped
pair formulation one may take \(h=1\), \(q=1\), and \(t=1\) at every vertex;
since \(|d_i|\le1\), all variables remain nonnegative and all cap and copy rows
are exact.

This is the path's small singular value in elementary form. Objective penalties
do not by themselves repair it under an approximate-feasibility output contract:
the free sums \(q_i\) can absorb many objective changes while the differences
drift. Any successful penalty argument must quantitatively couple objective gap
to these signed transition residuals rather than merely penalize the endpoint.

## 3. Quadratic size is necessary for replicated-path amplification

Consider the following restricted architecture. There are \(R\) copies of the
same length-\(N\) signed path, all rooted at the exact value \(d=1\); every copy
uses the same hidden sign \(\sigma_i\) at level \(i\). Arbitrary bounded-degree
input-independent copy trees and cap/reference variables may be attached before
and after the paths, as in Theorem 3 of
`2026-09-02-parity-amplified-primal-state-lower-bound.md`.

Allow the transition row at level \(i\) of copy \(r\) to be multiplied by an
arbitrary nonzero, input-independent weight \(\lambda_{r,i}\). Put

\[
 B=\max_{r,i}|\lambda_{r,i}|.
\]

### Proposition 2 (size--coefficient-scale tradeoff)

Suppose relative-residual soundness at threshold \(\eta\) is meant to rule out a
point at which every path endpoint has the sign opposite to \(p_N\). If the two
root anchors give \(\|b\|_2=\sqrt2\), then necessarily

\[
 RB^2\ge\frac{\eta^2N}{2}.                                \tag{13}
\]

Consequently, with uniformly bounded coefficients and any fixed constant
\(\eta>0\), this architecture requires \(R=\Omega(N)\) and
\(RN=\Omega(N^2)\) signed-path edges before endpoint amplification is counted.
Conversely, keeping only \(O(1)\) paths requires coefficient scale
\(B=\Omega(\sqrt N)\).

#### Proof

For path \(r\), define its series resistance

\[
 S_r=\sum_{i=1}^N\lambda_{r,i}^{-2}.
\]

Among all sequences with \(z_{r,0}=1\) and \(z_{r,N}=-1\), weighted
Cauchy--Schwarz gives

\[
 \min\sum_{i=1}^N
   \lambda_{r,i}^2(z_{r,i}-z_{r,i-1})^2
 =\frac4{S_r}.                                            \tag{14}
\]

Equality is attained by taking the increments proportional to
\(\lambda_{r,i}^{-2}\). This sequence stays in \([-1,1]\). Propagate its wrong
endpoint exactly through every attached copy tree, set all reference variables
exactly, and use \(q=1,t=1\). The cap rows and nonnegativity are satisfied. Since
\(S_r\ge N/B^2\), the resulting relative residual obeys

\[
 \frac{\|Ax-b\|_2^2}{\|b\|_2^2}
 =2\sum_{r=1}^R\frac1{S_r}
 \le\frac{2RB^2}{N}.                                      \tag{15}
\]

If \(RB^2<\eta^2N/2\), this wrong-endpoint point satisfies the promised residual
bound. Hence soundness requires (13). \(\square\)

The constants in a particular decoder proof can be improved, but doing so cannot
change this exponent at bounded coefficient scale: tolerating any fixed positive
relative residual still forces linearly many parallel copies in this architecture.
For a dimension \(P=\Theta(RN)\), the parity lower bound \(\Omega(N)\) is therefore
at most \(\Omega(\sqrt P)\) when robustness is obtained solely by path replication.
Row scaling avoids the quadratic dimension only by paying \(B=\Omega(\sqrt N)\),
which appears directly in sparse block-encoding normalization and numerical-scale
parameters; it is not a free improvement for a QLS-based QIPM.

### A tenfold improvement of the current residual constant

The proof of Theorem 3 in
`2026-09-02-parity-amplified-primal-state-lower-bound.md` does not need its stated
residual constant \(10^{-3}\). The same construction, stability lemma, and trace
distance \(1/400\) work with

\[
 \frac{\|Ax-b\|_2}{\|b\|_2}\le\frac1{100}.                \tag{16}
\]

Indeed, put \(E=\|Ax-b\|_2\le\sqrt2/100\). The inequalities already proved
there give

\[
 \|h\|_2\le(1+12E)\sqrt P,qquad
 \|q\|_2,\|t\|_2\le(2+25E)\sqrt P,
\]

and hence

\[
 \|x\|_2^2
 \le\bigl[2(2+25E)^2+(1+12E)^2\bigr]P
 <\frac{25}{2}P.                                         \tag{17}
\]

Writing \(S=16N^2\) and using \(P/S<33/16\), the signed leaf mass is at least

\[
\begin{aligned}
 \sum_{j\in S}\tau_jd_jq_j
 &\ge |S|-\sqrt{|S|}\|e\|_2-\|e\|_2\|q_S\|_2\\
 &\ge |S|\left[
  1-12E\left(1+(2+25E)\sqrt{33/16}\right)
 \right]
 >\frac14|S|.                                             \tag{18}
\end{aligned}
\]

The ideal amplitude-state decoder therefore has bias greater than

\[
 \frac{(|S|/4)}{2(25P/2)}
 >\frac4{825}>\frac1{250}.                                \tag{19}
\]

Trace distance \(1/400\) reduces a binary measurement's success probability by
at most \(1/400\), leaving a fixed positive bias. A fixed number of repetitions
then computes parity. Thus the robust theorem can state residual \(10^{-2}\)
without changing its construction or any asymptotic parameter. The largest
constant supported by these particular loose norm bounds is about \(0.013\) if
the trace-distance allowance is reduced accordingly; \(10^{-2}\) is a cleaner
statement with the existing \(1/400\) trace guarantee.

There is also a cleaner simultaneous improvement of both error allowances. With
relative residual \(1/200\), one has \(E\le\sqrt2/200\), the same calculation gives
\(\|x\|_2^2<11P\) and signed leaf mass greater than \(3|S|/5\). The ideal bias is
then greater than

\[
 \frac{(3|S|/5)}{22P}>
 \frac{48}{3630}>\frac1{80}.
\]

Thus trace distance \(1/100\) still leaves constant bias. One may state either the
pair \((\eta,D_{\rm tr})=(1/100,1/400)\), which maximizes the clean residual
constant, or \((1/200,1/100)\), which improves both constants over the current
statement.

## 4. Long-range shortcut rows move parity into the oracle

One tempting alternative is to add a bounded-degree expander on the prefix
variables \(d_i\), hoping to give the constraint matrix a constant singular-value
gap. The following observation shows the oracle problem with that approach.

### Lemma 3 (interval-parity coefficient ratio)

Fix \(0\le i<j\le N\). Suppose a homogeneous two-coordinate row

\[
 a(\sigma)d_i+b(\sigma)d_j=0,                              \tag{20}
\]

with nonzero coefficients is valid for the exact signed-path solution
\(d_k=p_k\) for every input \(\sigma\). Then

\[
 -\frac{a(\sigma)}{b(\sigma)}
 =\frac{p_j}{p_i}
 =\prod_{k=i+1}^j\sigma_k.                                \tag{21}
\]

Thus one exact query returning both nonzero row values reveals the parity of the
\(j-i\) signs in that interval. Simulating such a row-value query from the raw
sign oracle requires \(\Omega(j-i)\) bounded-error quantum queries in general.

#### Proof

Substitute \(d_i=p_i\) and \(d_j=p_j\) into (20), divide by
\(b(\sigma)p_i\), and use \(p_j/p_i=\prod_{k=i+1}^j\sigma_k\). The query lower
bound is the standard quantum parity lower bound applied to that interval.
\(\square\)

The conclusion is invariant under arbitrary nonzero input-dependent rescaling of
the whole row, since only the ratio is used. It also applies to coherent whole-row
access. Therefore an expander made from long prefix-to-prefix equality rows does
not preserve the desired \(O(1)\)-query reduction from LP coefficients to raw
signs: it packages a long parity into one coefficient-oracle response.

The lemma does not exclude more elaborate gadgets with auxiliary variables and
rows involving three or more coordinates. Nor does it exclude changing the input
model and granting interval-parity coefficients directly. It identifies the exact
loophole that any claimed near-linear robust construction must close: it needs
constant residual soundness without either repeating \(\Theta(N)\) full paths or
hiding a long parity in a supposedly cheap coefficient query.

## Status

Theorem 1 and Lemma 3 are complete elementary reductions. Proposition 2 is a
lower bound only for the explicitly stated replicated-path architecture. Together
they explain why the current robust constant-relative-\(\ell_2\) theorem has
quadratic LP size and why the most obvious linear-size spectral-gap repair is not
valid in the raw coefficient-query model. A general linear-size bounded-degree
real-linear parity gadget with constant residual soundness remains open.

### Literature and novelty calibration

A targeted search on 2026-09-02 found established quantum LP lower bounds whose
optimal values encode Boolean functions. In particular, Apers--Gribling,
[*Quantum Speedups for Linear Programming via Interior Point
Methods*](https://doi.org/10.1137/23M1608569), Theorem 8.4, gives an additive-value
lower bound with stronger general dimension/sparsity dependence. Van Apeldoorn's
[*Quantum SDP-solvers: limits and
possibilities*](https://ir.cwi.nl/pub/29317/29317.pdf), Theorem 9.15, gives an
\(\Omega(n)\) constant-multiplicative lower bound for producing a solution of a
nonnegative LP, but explicitly does not obtain the same conclusion for
value-only output. Theorem 1 above is therefore useful because it puts a direct
multiplicative **value** gap into the already regular, bounded-degree,
condition-one signed-path family. It is not a new generic LP query lower-bound
technique, and its normalization may be considered too elementary to publish on
its own.

The search found no paper stating Proposition 2's exact
\(RB^2=\Omega(\eta^2N)\) size--row-scale tradeoff for a robust signed-parity LP
embedding, or Lemma 3's coefficient-oracle obstruction in this setting. Both are
simple once formulated and should be presented as supporting structural lemmas,
not as broad priority claims. Their main value is to delimit the current open
problem and prevent an invalid claimed improvement by row scaling or parity-laden
shortcut coefficients.
