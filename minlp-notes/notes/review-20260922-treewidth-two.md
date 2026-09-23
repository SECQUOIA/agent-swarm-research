# Independent adversarial review: bandwidth-two indicator quadratics

Date: 2026-09-22. Reviewer: separate research agent, not an author of the
construction. Reviewed [the research note](research-20260922-treewidth-two.md)
and the common-penalty strengthening, including its final written Theorem 3.
This report records a mathematical review, not formal verification
or a proof of novelty.

## Verdict and boundaries

The first reduction is correct on independent examination. Its fixed Hessian,
spectral bounds, exact decision reduction, and constant absolute gap survive
the continuous adjustments that are the main potential loophole. The proposed
second reduction also works: a fixed positive translation forces the state
indicators on even when every indicator costs one. The latter construction
has instance-dependent Hessian entries and an exponentially small decision
gap. These are different strengths and must not be combined into one theorem
without an additional argument.

The structural conclusion is consequential for exact algorithms for this
particular model: positive definiteness, excellent conditioning, bounded
bandwidth, and even a chain of three-vertex blocks do not suffice. This is a
complexity boundary, not evidence that practical banded instances are hard or
that approximation algorithms fail. The underlying subset-sum accumulator is
old. Priority for the precise conjunction of restrictions remains unsettled.

Two wording corrections were communicated to the coordinator:

- State maximum degree **at most four**. At \(n=2\), the maximum degree is three; degree four first occurs
  at \(n=3\).
- In the translated construction, bounded objective data means bounded
  entries of \(K,c,\lambda\). The expanded additive constant grows with \(n\).
  It can be removed and transferred to the threshold, but is not itself
  uniformly bounded.

## Independent check of the first reduction

The feasible-point identity

\[
x_i^2-2A_ix_i+A_i^2z_i=(x_i-A_iz_i)^2
\]

requires the indicator constraint. It is correct for both binary choices and
does not introduce a binary-dependent Hessian. Setting an indicator to one
while its variable is zero is permitted; the YES construction legitimately
sets all state indicators to one, including zero states.

Unrolling the residual recurrence gives

\[
s_n=\sum_i a_iz_i+\sum_i\theta^{n-i+1}e_i
                    +\sum_i\theta^{n-i}r_i.
\]

Therefore the sign and every exponent in the note's residual identity are
correct. Weighted Cauchy--Schwarz uses the vector
\((e_1,\ldots,e_n,r_1,\ldots,r_n,\theta(s_n-B))\); its coefficient
vector has squared norm

\[
\theta^{-2}+\(1+\theta^2\)\frac{1-\theta^{2n}}{1-\theta^2}
 <\frac{1+\theta^4}{\theta^2(1-\theta^2)}.
\]

This proves the strict NO gap for all feasible continuous points. In
particular, the proof does not assume that minimizers lie exactly at the wells
or satisfy the chain equations exactly. Nonnegative state costs only strengthen
the NO bound. YES has value at most \(n\mu=\delta_\theta/4\), which is all
the reduction needs. The two approximation intervals are disjoint at the
claimed absolute error.

Direct expansion gives each diagonal \(1+\theta^2\). An internal state row
has absolute off-diagonal sum \(3\theta+\theta^2\); this is the largest
possible row sum. Thus the stated Gershgorin interval is correct. The last
terminal square is essential to the claim that **all** diagonals are equal;
without it the last state diagonal would be one. Scaling by \(1+\theta^2\)
gives rational unit diagonal and changes every objective threshold and gap by
the same factor. The constant-gap claim after scaling still holds because
\(\theta\) is fixed independently of the subset-sum instance.

The edge list gives the asserted path decomposition and bandwidth. Each
triangle has three nonzero edges for positive \(\theta\), so its treewidth
is not one. Triangles meet only in articulation vertices. Their positive
edge-sign product is invariant under variable sign changes and prevents
switching the whole matrix to nonpositive off-diagonal entries.

For fixed rational \(\theta=p/q\), the powers in \(A_i\) require only
polynomially many bits. Matrix inversion on a proposed support is exact
rational linear algebra with polynomial bit complexity. More explicitly,
clearing input denominators and applying determinant bounds to each principal
submatrix gives polynomial bit bounds for its inverse and minimizer. Coercivity
on each of the finitely many supports supplies attainment. Thus the
certificate argument is valid even when the optimized point has zero selected
coordinates. No generic real-number certificate is being assumed.

The normalized construction preserves the Hessian but makes the decision gap
and some costs small. Its bounded-coordinate argument is valid: the all-zero
point supplies the claimed upper bound, and the residual norm bounds plus
the contracting recurrence bound each coordinate. None of this proves strong
NP-hardness or hardness at fixed normalized accuracy.

## Independent check of the common-penalty strengthening

Here take positive integers \(a_i\), \(0<B\le M=\sum_i a_i\),
\(b_i=a_i\theta^i/M\), \(T=B\theta^n/M\), and \(D=4\). The
restricted subset-sum problem remains NP-complete: instances outside the
range of possible positive sums can be recognized and mapped to a fixed NO
instance. Use the wells \(x_i^2-2x_i+z_i\), the first residual
\(t_1-D-b_1x_1\), later residuals
\(t_i-\theta t_{i-1}-b_ix_i-D(1-\theta)\), terminal square
\(\theta^2(t_n-D-T)^2\), and unit costs for all state indicators
\(\zeta_i\).

For a fixed binary vector \(z\), define the exact reference trajectory

\[
\bar t_i=D+\frac{\theta^i}{M}\sum_{j\le i}a_jz_j\ge D.
\]

Set \(e_i=x_i-z_i\), \(h_i=t_i-\bar t_i\), and \(h_0=0\). The wells
and dynamic residuals sum exactly to

\[
\sum_i e_i^2+\sum_i(h_i-\theta h_{i-1}-b_ie_i)^2.
\]

Its matrix \(K_0\), before adding the terminal quadratic, has diagonals
\(1+b_i^2\) for \(e_i\), \(1+\theta^2\) for \(h_i\), \(i<n\), and
one for \(h_n\). Since \(0<b_i\le\theta\), a state row has absolute
off-diagonal sum at most \(3\theta+\theta^2\), and an \(e_i\) row at
most \(\theta+\theta^2\). The last state row has sum at most
\(2\theta\). Consequently \(K_0\succeq(1-3\theta)I\). This proof
does not incorrectly borrow the terminal diagonal correction from the first
construction.

If exactly \(k\) state indicators are zero, the corresponding \(h_i\) equal
\(-\bar t_i\), so \(\sum_i h_i^2\ge D^2k\). Dropping the terminal
square gives the valid bound

\[
F\ge n+\big((1-3\theta)D^2-1\big)k.
\]

For \(\theta\le1/10\), the coefficient of \(k\) is at least \(10.2\).
By contrast, \(z=0,x=0,t_i=D,\zeta_i=1\) has objective
\(n+\theta^2T^2\le n+\theta^2\). Thus every optimizer has all state
indicators on. The translation forces activation without imposing a constraint
or adding a large penalty to a dynamic residual.

With all state indicators on, \(F\ge n\). Equality is possible exactly when
the wells and every residual vanish, which is equivalent to
\(\sum_i a_iz_i=B\). A NO instance cannot have infimum \(n\) without
attaining it, because the earlier coercivity argument applies. Alternatively,
the first reduction's weighted Cauchy--Schwarz bound gives the explicit
strict NO gap

\[
F>n+\delta_\theta\frac{\theta^{2n}}{M^2}
\]

when all states are on; the off-state lower bound is larger as well. This
also exposes why constant-cost hardness here does not yield a fixed absolute
approximation barrier with bounded linear coefficients.

The full Hessian has diagonals \(1+b_i^2\) and \(1+\theta^2\), and the
triangle edges are \(-b_i,-\theta,+\theta b_i\). It has the same graph
and the claimed uniform spectral interval. It approaches identity as
\(\theta\downarrow0\) without scaling the unit penalties. The entries
depend on the \(a_i\); the fixed-Hessian assertion from the first construction
must not be attached to this one. For an explicit linear coefficient bound,
write \(h_1=D\), \(h_i=D(1-\theta)\) for \(i>1\). The item coefficient
\(-2+2h_ib_i\) lies in \([-2,-1.2]\). An internal state coefficient
\(-2h_i+2\theta h_{i+1}\) has magnitude at most eight; the terminal
coefficient has magnitude at most
\(2D+2\theta^2(D+T)\le8.1<9\). This independently confirms the precise
\(|c_j|\le9\) claim in the final theorem. The additive constant is

\[
D^2+(n-1)D^2(1-\theta)^2+\theta^2(D+T)^2,
\]

which explains the wording caveat above.

## Literature and novelty review

Primary sources inspected online on 2026-09-22:

- Lerner and Parr, [*Inference in Hybrid Networks: Theoretical Limits and
  Practical Algorithms*](https://arxiv.org/pdf/1301.2288), §3, Theorems 1–2
  and Corollary 3. Their reduction accumulates subset sums in a Gaussian
  chain with binary-dependent offsets. It establishes inference and discrete
  MAP hardness under simple graph structure. This is a close antecedent for
  the mechanism; the present zero-indicator formulation and spectral/penalty
  restrictions are additional work, not stated consequences of their theorem.
- Bhathena, Fattahi, Gómez, Küçükyavuz,
  [*A Parametric Approach for Solving Convex Quadratic Optimization with
  Indicators Over Trees*](https://arxiv.org/html/2404.08178v1), §3.1–3.4 and
  Theorem 3.2. The stated quadratic operation count supplies the strongest
  direct tree comparison. An arithmetic operation count alone does not prove
  a Turing-model polynomial bound; a sharp bit-complexity dichotomy would
  require an explicit rational-coefficient and breakpoint analysis.
- The same authors, [*Solving Convex Quadratic Optimization with Indicators
  Over Structured Graphs*](https://arxiv.org/html/2603.02103v1), §1.2,
  Definition 5 and Theorem 1. Their exact runtime explicitly depends on
  near-optimal local support multiplicity and margin, in addition to graph
  geometry and conditioning. The new family is compatible with that theorem.
  It does not by itself calculate their margin or prove that this specific
  parameter is necessary.
- Choi, Fattahi, Han, Gómez, Lozano, [*Convexification of Mixed-Integer
  Quadratic Optimization via Decision Diagrams*](https://arxiv.org/html/2608.22815v1),
  abstract and structural/approximation discussion. Exact tree and approximate
  sparse-graph constructions do not supply a general exact bandwidth-two
  algorithm. The note should give the author list accurately, starting with
  Choi rather than attributing it only to Gómez and coauthors.

Searches also tested the formulations “sparse approximation,” “sparse
regression,” “banded,” “near orthogonal,” “diagonally dominant,” and
“treewidth” with hardness terms. The publisher abstract for Çivril's
[*A note on the hardness of sparse approximation*](https://doi.org/10.1016/j.ipl.2013.04.014)
describes a cardinality-constrained approximation result and near-orthogonal
dictionary motivation. Only its abstract was inspected; this does not exclude
overlap in a full proof or later literature. No equivalence was established.

The defensible claim is therefore an explicit hardness result with carefully
specified simultaneous restrictions, and an unresolved priority question.
Absence from this search is not evidence of firstness. The result could support
a useful short theoretical paper if priority survives broader expert review;
this report cannot determine publication significance or historical novelty.

## Verification scope

This review independently rederived the identities, matrix entries, spectral
estimates, activation bound, graph decomposition, bit encoding, and support
certificate argument. It did not run a numerical enumeration, Lean, project-wide
tests, or CI. It also read
[check_treewidth_two.py](../code/research_20260922/check_treewidth_two.py):
the builder represents \(v^TQv-2h^Tv+\lambda^Ty+c_0\), constructs the
correct first translated residual, and solves \(Q_{JJ}v_J=h_J\) on each
support. The resulting value \(c_0+\lambda(J)-h_J^Tv_J\) is correct.
The coordinating researcher reported that its 24 rational instances and
3072 support QPs passed; this reviewer inspected its logic but did not rerun it.
The original coefficient assertion \(\max|h_j|\le10\) checked only
\(|c_j|\le20\), so the coordinator was advised to strengthen that assertion
to \(2\max|h_j|\le9\). The analytical bound above does not depend on that
sample assertion.

The targeted repository commands read the subject note and located
related literature files; the literature checks above used the cited primary
web sources. A separate support-enumeration experiment can detect finite-case
implementation errors, but cannot certify the all-dimension reduction or
novelty.
