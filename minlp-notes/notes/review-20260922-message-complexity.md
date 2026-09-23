# Independent review of the scalar indicator-message lower bound

Date: 2026-09-22. Reviewed files:
[research note](research-20260922-message-complexity.md) and
[exact checker](../code/research_20260922/check_message_complexity.py).
The reviewer did not edit those files.

**Assessment.** The stated mathematical claims survive this review. The
result is a representation lower bound, with the approximation and algorithmic
limitations stated correctly. A stronger construction is available: set every
coupling coefficient to the same fixed rational number. This removes tiny
input coefficients while preserving the exponential number of necessary
polynomial formulas. Section 3 gives the proof. The coordinator independently
rechecked its center separation and approximation argument.

## 1. Proof audit

For a fixed indicator vector, inactive coordinates must have error zero.
On the active coordinates, the original objective is exactly the squared
Euclidean norm of the control errors and recurrence residuals. The terminal
condition is their single linear constraint. Its coefficient vector has
squared norm

\[
D_z=\sum_i w_i^2+\sum_i w_i^2b_i^2z_i>0.
\]

The least-norm solution is the constraint vector multiplied by
\((t-t_z)/D_z\). Reconstructing states verifies the terminal condition and
shows that no other constraint was lost. This establishes the claimed
fixed-support formula, including the empty support and the one-period case.

Different centers give different unique zeros. Each zero has a neighborhood
where its quadratic alone minimizes, because there are finitely many other
strictly positive values there. The explicit \(h/3\) neighborhoods in the
original construction are also correct. At the left domain endpoint they
contain an ordinary open interval on their right.

The lower bound for arbitrary finite minima of polynomials is stronger than a
count of supports. A finite union of zero sets of nonzero univariate
polynomials cannot cover an open interval. Consequently every polynomial
representation must contain each locally active quadratic identically. This
argument does not assume the proposed representation came from support
enumeration. It also handles a finite piecewise polynomial representation on
intervals. It does not handle compact recursions, integer operations, or other
representations outside this class.

The matrix expansion and Gershgorin bounds are correct. Internal state rows
have at most four neighbors. The graph consists of triangles sharing state
vertices, with an initial pendant control edge, and has pathwidth and treewidth
two when there are at least two periods. The terminal conditioning is an
operation used to form a message. It is not an assertion that the graph after
terminal deletion has exactly the same width.

For the shifted all-indicator lift, the error vector is measured from
\((z,4\mathbf 1+s^z)\), where all \(s_i^z\ge0\). An inactive state
has error at most \(-4\), so the spectral lower bound yields

\[
H\ge n+[16(1-3\theta)-1]k\ge n+10.2k.
\]

The all-on candidate costs at most \(n+1\), including at both terminal
endpoints. Thus every optimal state indicator is on. The subtraction of four
then gives exactly the original scalar message plus \(n\). Linear
coefficient bounds remain valid for the one-period endpoint case.

The two-piece approximation in the original note is correct. Above the largest
center, the all-ones support has both the shortest nonnegative distance to the
parameter and the largest denominator. Below that center, nearest-grid-center
rounding gives the stated error. Deletion-only lower bounds do not imply lower
bounds for newly constructed approximate functions.

## 2. Independent finite checks

The existing command was run without alteration:

```text
python3 code/research_20260922/check_message_complexity.py
PASS: 724 exact support QPs, 124 centers, 248 neighborhood endpoints; n=1..5, theta=1/10,1/20
```

The checker assembles residual rows before solving their normal equations; it
does not use the proposed value formula to construct the quadratic programs.
Its handling of fixed terminal coordinates, inactive controls, and the
zero-dimensional one-period empty-support problem is correct.

Two additional targeted inline Python programs were run with `python3 -`.
They used `fractions.Fraction` and the existing rational Gaussian elimination
routine, but separately assembled the lifted residuals and the constant
coupling instances:

```text
PASS: 1360 exact lifted support QPs, n=1..4, two theta values, four terminal values; every inactive-state support costs more than n+1
PASS: 756 constant-coefficient support QPs; 1698 truncated-envelope checks; n=1..6, two theta values
```

The first program enumerated control supports and every feasible state support
with the terminal indicator on, at terminal offsets
\(0,1,1/2,\theta^n/2\), for \(\theta=1/10,1/20\). Its quadratic
programs used the original shifted residuals with inactive state variables
fixed at zero. The global minima equaled \(n+V_n(t)\), and every support
with an inactive state cost more than \(n+1\).

The second program checked the fixed-support formula for constant couplings
at zero, one, and each support's center. It checked distinct centers and the
approximation below for every retained suffix length, at all centers and the
additional parameters zero, one, and one half. These programs were finite
checks, not proofs of the general assertions. No project-wide tests, CI checks,
or Lean verification were performed.

## 3. Stronger construction with a fixed coefficient alphabet

In the original definition of \(V_n\), replace its coefficients by

\[
b_i=\theta\qquad(1\le i\le n),
\quad 0<\theta\le1/10\text{ fixed and rational}.
\]

The fixed-support derivation uses no special property of the original
\(b_i\), so now

\[
t_z=\sum_{i=1}^n\theta^{n-i+1}z_i,
\qquad
D_z=\sum_{i=1}^n\theta^{2(n-i)}
     +\sum_{i=1}^n\theta^{2(n-i+1)}z_i,
\qquad
q_z(t)=\frac{(t-t_z)^2}{D_z}.
\]

All centers lie in
\([0,\theta/(1-\theta)]\subset[0,1]\). They are pairwise distinct.
Indeed, write a difference of centers in increasing powers of \(\theta\)
and let \(j\) be the first nonzero coefficient. That coefficient is either
one or minus one, and the tail's absolute value is bounded by

\[
\sum_{k=j+1}^{n}\theta^k
<\frac{\theta^{j+1}}{1-\theta}<\theta^j.
\]

The leading term cannot cancel. Therefore every support has a unique zero
inside the fixed parameter domain, and every exact finite minimum of
polynomials requires at least \(2^n\) distinct polynomials. This is the same
polynomial-identity proof, now with no shrinking input coefficients.

The Hessian has entries only among

\[
0,\quad 1,\quad 1+\theta^2,\quad -\theta,\quad\theta^2,
\]

and satisfies the original spectral bounds. The original linear coefficients
are zero and minus two, and every control penalty is one. The shifted state
construction also retains unit penalties and bounded linear coefficients from
a fixed finite rational set. Its only growing expanded coefficient is the
irrelevant objective constant, of order \(n\). The sparse residual description
contains \(O(n)\) terms with constant-size numerical coefficients. This
does not identify the number of terms with the exact total binary encoding
length, which also records indices and the horizon.

The center separation proof gives strict positivity, not a numerical stability
guarantee. Increasing the horizon still creates exponentially small differences
between some centers. The strengthening removes tiny data coefficients, not
fine resolution from the exact output.

### Approximation still has size independent of the horizon

Let \(m\le n\), and retain only supports with
\(z_1=\cdots=z_{n-m}=0\). Call their lower envelope \(V_{n,m}\).
It has at most \(2^m\) quadratics. For an arbitrary support \(z\), let
\(z'\) be the retained support obtained by deleting those first bits. Then

\[
0\le t_z-t_{z'}\le
\delta_m:=\frac{\theta^{m+1}}{1-\theta},
\qquad
0\le D_z-D_{z'}\le
\beta_m:=\frac{\theta^{2m+2}}{1-\theta^2}.
\]

Both denominators are at least one. Both centers and the parameter lie in
\([0,1]\), so

\[
\left|(t-t_{z'})^2-(t-t_z)^2\right|\le2\delta_m.
\]

Splitting the difference of the two quotients therefore gives
\(q_{z'}(t)-q_z(t)\le2\delta_m+\beta_m\). Choosing an optimal support
for the full envelope and using the fact that the retained supports are a
subset yields

\[
0\le V_{n,m}(t)-V_n(t)
\le\frac{2\theta^{m+1}}{1-\theta}
  +\frac{\theta^{2m+2}}{1-\theta^2}
\qquad(0\le t\le1).
\]

The denominator's base term is still the full-horizon
\(\sum_i\theta^{2(n-i)}\); it must not be replaced by its last \(m\)
terms. At fixed positive accuracy, choose \(m\) independently of \(n\),
or retain all supports if \(n<m\). This establishes a polynomial bound in
inverse accuracy for fixed \(\theta\), despite exponential exact complexity.
The original two-piece approximation should not be transferred to this
constant-coefficient family: its centers do not all shrink into
\([0,\theta^n]\).

## 4. Prior results and significance

The following primary sources were independently inspected during the review.

- [Bhathena, Fattahi, Gómez, Küçükyavuz, trees, arXiv v1](https://arxiv.org/html/2404.08178v1)
  gives an exact quadratic-time tree algorithm. Its graph assumptions differ
  from the triangle chain here. A lower bound for storing an entire conditional
  message is also different from a lower bound for finding one optimum.
- [The same authors, structured graphs, arXiv v1](https://arxiv.org/html/2603.02103v1),
  Definition 5 and Theorem 1, condition exact complexity on a margin controlling
  nearby support values. The definition uses the local value at a zero bag,
  with specified support equivalence classes. Equal minima at different
  nonzero terminal values do not by themselves evaluate that parameter.
  The note correctly avoids claiming an explicit margin lower bound without
  making this identification.
- [Lee, Gómez, Atamtürk, July 2026](https://link.springer.com/article/10.1007/s10107-026-02379-5),
  Definition 1 and Proposition 8, treats factorizable matrices whose inverses
  are block tridiagonal. Eliminating free internal states here gives
  \(I+uu^T/W\), with all \(u_i>0\), whose inverse has every off-diagonal
  entry nonzero. For \(n\ge3\), it is not scalar factorizable under any
  permutation. This verifies the note's direct scalar comparison. It does
  not rule out every possible extended or block reformulation.
- [Kuric, Ahmetspahic, Pock, 2024](https://epubs.siam.org/doi/10.1137/23M1556915)
  already studies exponential complexity of nonconvex piecewise quadratic
  continuous messages. This is a close conceptual antecedent, not a result
  to dismiss because its initial formulation looks different.

In fact, eliminating one local control in this construction gives the
two-well transition cost

\[
\min_{x,z:\,x(1-z)=0}
\{x^2-2x+z+(r-bx)^2\}
=\min\left\{r^2,\frac{(r-b)^2}{1+b^2}\right\},
\qquad r=s_i-\theta s_{i-1}.
\]

Thus the message is also a succession of operations on familiar two-well
quadratic costs. This reinforces the need to claim only the restricted
construction and the simultaneous restrictions it meets. General exponential
growth of quadratic message representations is established background.

The constant-coefficient version is a useful, elementary companion to the
hardness result: stable scalar recurrences, a matrix uniformly close to the
identity, bounded graph width, bounded coefficients, and unit penalties do
not control exact polynomial message size. It supplies an explicit instance
on which exact dominance pruning cannot reduce the number of formulas. It
does not establish hard optimization of that instance, an extension-complexity
lower bound, or difficult approximation at fixed accuracy. Exact novelty of
the simultaneous restrictions remains provisional; the searches and source
comparisons do not establish priority.
