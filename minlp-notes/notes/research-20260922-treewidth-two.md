# Exact indicator quadratic optimization at bandwidth two

The reviewed version is now
[the result note](../results/indicator-quadratic-treewidth-two-hardness.md).
This development draft preserves the investigation before the final review
and exact support checks; its pending-status statements are historical.

Date: 2026-09-22. Status: research result with a complete elementary proof;
independent adversarial review and broader priority checks are still required.
The reduction was developed in the current research session. It is not a claim
that the general idea of encoding subset sums by continuous chains is new.

The main result is a sharp obstruction to extending exact tree algorithms using
only sparsity and conditioning: convex quadratic optimization with uncoupled
indicator variables is NP-hard already for a fixed family of bandwidth-two,
strictly diagonally dominant matrices arbitrarily close to the identity. Every
indicator has a strictly positive penalty. There are no other constraints.

The restriction concerns the Hessian support graph, not the graph of a dense
Schur complement after eliminating variables. Its graph is a chain of triangles
sharing individual vertices, with an initial pendant edge. It has maximum degree
four and treewidth and pathwidth two. The quadratic matrix is independent of the
SUBSET SUM numbers: only the linear and indicator costs encode those numbers.

A second construction below strengthens the result in a different direction:
all indicator penalties equal one and all linear coefficients are bounded by
nine. Its Hessian is still arbitrarily close to the identity and has the same
graph, but its small off-diagonal entries now encode the instance. This second
construction proves exact hardness, with a potentially exponentially small gap.

## Model and theorem

Consider rational data in

\[
 \min\{v^T K v+c^Tv+\lambda^Ty+c_0:
       v_j(1-y_j)=0,\quad v\in\mathbb R^N,
       y\in\{0,1\}^N\},                                      \tag{1}
\]

where \(K\succ0\) and every \(\lambda_j>0\). The continuous Hessian is \(2K\).
The constant \(c_0\) is included to expose a nonnegative residual formulation;
subtracting it from the decision threshold removes it from the input model.

**Theorem 1.** Fix any rational \(0<\theta\le1/10\). There is a family of
rational matrices \(K_{n,\theta}\), depending only on \(n\) and \(\theta\), such
that deciding whether the value of (1) is at most a given rational threshold is
NP-complete, even under all of the following restrictions:

1. \(N=2n\), the ordered matrix has bandwidth two, and its support graph has
   maximum degree four and treewidth and pathwidth two for \(n\ge2\).
2. All diagonal entries equal \(1+\theta^2\); off-diagonal entries belong to
   \(\{0,-\theta,\theta^2\}\).
3. \((1-3\theta)I\preceq K_{n,\theta}\preceq
   (1+3\theta+2\theta^2)I\).
4. Every continuous variable has its own binary indicator and positive penalty;
   no indicators are fixed, and there are no coupling constraints.

Write

\[
 \delta_\theta=
 \frac{\theta^2(1-\theta^2)}{1+\theta^4}>0.                  \tag{2}
\]

The reduction in the proof has the additional promise that its optimal value is
at most \(\delta_\theta/4\) or greater than \(\delta_\theta\). Consequently,
computing its optimal value with absolute error at most
\(\delta_\theta/4\) is NP-hard. The coefficients in this promise family can have
exponentially large magnitudes, but have polynomial binary encoding length.
This is not a strong NP-hardness claim.

**Corollary 2.** For every fixed \(\varepsilon>0\), exact optimization remains
NP-hard with a fixed family of rational unit-diagonal matrices satisfying

\[
 \|K-I\|_2\le\varepsilon,
\]

and with the graph restrictions and positive penalties in Theorem 1.
Thus requiring the Hessian condition number to be arbitrarily close to one
does not yield a general exact polynomial-time algorithm for bandwidth two.

## Reduction and proof

Take positive integers \(a_1,\ldots,a_n,B\) from SUBSET SUM, with \(n\ge2\).
Choose continuous variables \(x_i,s_i\), binary variables \(z_i,w_i\), and set

\[
 A_i=a_i\theta^{-(n-i+1)},\qquad
 \mu=\frac{\delta_\theta}{4n},\qquad s_0=0.                \tag{3}
\]

The symbol \(s_0\) is a fixed boundary value, not a decision variable. Minimize

\[
\begin{split}
 F(x,s,z,w)={}&
 \sum_{i=1}^n\bigl(x_i^2-2A_ix_i+A_i^2z_i\bigr)\\
 &+\sum_{i=1}^n(s_i-\theta s_{i-1}-\theta x_i)^2
 +\theta^2(s_n-B)^2+\mu\sum_{i=1}^nw_i,                 \tag{4}
\end{split}
\]

subject only to

\[
 x_i(1-z_i)=0,\qquad s_i(1-w_i)=0,
 \qquad z_i,w_i\in\{0,1\}.                              \tag{5}
\]

Equation (4), rather than an expansion with bilinear \(x_i z_i\) terms, is the
actual convex quadratic objective. On feasible points its first summand equals
\((x_i-A_i z_i)^2\): when \(z_i=0\), (5) forces \(x_i=0\); when \(z_i=1\),
the equality is the usual square expansion. This identity must not be used
outside the indicator-feasible set. In particular, the construction has no
binary-dependent continuous Hessian.

All terms in this feasible-point residual representation are nonnegative, and
all indicator penalties \(A_i^2,\mu\) are positive.

### YES instances

If \(\sum_i a_i z_i=B\), set

\[
 x_i=A_i z_i,\qquad s_i=\theta s_{i-1}+\theta x_i,
 \qquad w_i=1.
\]

These choices satisfy (5), including when a state happens to be zero. Iteration
of the recurrence gives

\[
 s_n=\sum_{i=1}^n\theta^{n-i+1}A_i z_i
     =\sum_{i=1}^n a_i z_i=B.
\]

Every square vanishes, and \(F=n\mu=\delta_\theta/4\).
Some state indicators may instead be zero, so this is an upper bound on the
optimal value and need not be the exact YES value.

### NO instances and the uniform residual gap

For any feasible point, put

\[
 e_i=x_i-A_i z_i,\quad
 r_i=s_i-\theta s_{i-1}-\theta x_i,\quad
 t=s_n-B.
\]

The recurrence, without assuming any residual is zero, gives the exact identity

\[
 B-\sum_{i=1}^n a_i z_i
 =\sum_{i=1}^n\theta^{n-i+1}e_i
  +\sum_{i=1}^n\theta^{n-i}r_i-t.                       \tag{6}
\]

On a NO instance the left side is a nonzero integer, so its absolute value is
at least one. Apply Cauchy--Schwarz to the right side with residual vector
\((e,r,\theta t)\). Define

\[
 D_{n,\theta}=\theta^{-2}
 +(1+\theta^2)\sum_{j=0}^{n-1}\theta^{2j}.
\]

Then

\[
 1\le D_{n,\theta}
       \left(\sum_i e_i^2+\sum_i r_i^2+\theta^2t^2\right)
   \le D_{n,\theta}F.
\]

Since \(0<\theta<1\),

\[
 D_{n,\theta}
 <\theta^{-2}+\frac{1+\theta^2}{1-\theta^2}
 =\frac{1+\theta^4}{\theta^2(1-\theta^2)}
 =\delta_\theta^{-1}.
\]

Thus every feasible point of a NO instance satisfies
\(F\ge D_{n,\theta}^{-1}>\delta_\theta\). The distinction uses all feasible
continuous points, not merely the intended zero-residual representatives.
This rules out a possible loophole in which continuous adjustments repair the
terminal residual at negligible cost.

### Matrix structure and conditioning

Order the continuous variables as

\[
 v=(x_1,s_1,x_2,s_2,\ldots,x_n,s_n).
\]

The quadratic homogeneous part of (4) is

\[
 v^T K_{n,\theta}v
 =\sum_i x_i^2+
   \sum_i(s_i-\theta s_{i-1}-\theta x_i)^2+\theta^2s_n^2.
                                                               \tag{7}
\]

Each \(x_i\) has diagonal coefficient \(1+\theta^2\). A state \(s_i\),
\(i<n\), receives coefficient one from residual \(i\) and \(\theta^2\) from
residual \(i+1\). The last state receives its \(\theta^2\) contribution from
the terminal term, so its diagonal is the same. The nonzero off-diagonal entries
are

\[
 K_{x_i,s_i}=-\theta,\qquad
 K_{s_{i-1},s_i}=-\theta,\qquad
 K_{s_{i-1},x_i}=\theta^2\quad(i\ge2).                  \tag{8}
\]

The latter two entries are absent for \(i=1\). These are all off-diagonal
entries. They have index distance at most two in the stated ordering. The bags

\[
 \{x_1,s_1\},
 \{s_1,x_2,s_2\},\ldots,
 \{s_{n-1},x_n,s_n\}
\]

form a path decomposition of width two. A triangle is present when \(n\ge2\),
so treewidth and pathwidth are exactly two. The degree of an internal state is
four and all remaining degrees are smaller. The graph is chordal and a cactus;
its triangles share at most a single vertex. In particular, large separators
or large biconnected components are not needed for the reduction. Its balls have
at most \(4r+1\) vertices at integer graph radius \(r\), by the bandwidth bound.

Every absolute off-diagonal row sum is at most \(3\theta+\theta^2\).
Gershgorin's theorem for this symmetric matrix gives

\[
 1-3\theta\le\lambda_{\min}(K_{n,\theta})
 \le\lambda_{\max}(K_{n,\theta})
 \le1+3\theta+2\theta^2.                                \tag{9}
\]

In particular, \(K\) is strictly diagonally dominant and positive definite.
At \(\theta=1/10\), \(\kappa_2(K)\le66/35<1.886\).
For arbitrary fixed \(\theta\) tending to zero, the displayed condition bound
tends to one. Dividing the objective by \(1+\theta^2\) yields a unit-diagonal
quadratic matrix \(\bar K\) satisfying

\[
 \|\bar K-I\|_2
 \le\frac{3\theta+\theta^2}{1+\theta^2}\le4\theta.
\]

Choosing a fixed positive rational \(\theta\le\min\{1/10,\varepsilon/4\}\)
proves Corollary 2. The objective scaling also scales the threshold and gap by
the same known rational factor.

There is no conflict with tractability of matrices that can be made Stieltjes
by sign changes. Each triangle in (8) has a positive product of its three edge
signs. This product is invariant under independent variable sign changes, while
three negative off-diagonal entries would have negative product. Thus no sign
change makes all three edges of any such triangle nonpositive.

### Encoding length, attainment, and membership in NP

For fixed rational \(\theta=p/q\), every \(A_i\) has binary encoding length
\(O(\log a_i+n(\log p+\log q))\). Squaring these values and constructing the
other coefficients preserves polynomial encoding length. No variable bound or
large penalty multiplying the dynamic residuals is used. Every support-restricted
continuous quadratic is coercive by (9), hence attains its unique minimum.
The finite minimum over supports is therefore attained as well.

For membership in NP, a certificate gives the selected support. If \(J\) is
that support, the optimal continuous vector on it is
\(-\tfrac12K_{J,J}^{-1}c_J\). It is rational with polynomial encoding length,
and exact rational linear algebra verifies its value in polynomial time.
The support may include coordinates that optimize to zero; these are still
feasible, and all supports are permitted. The certificate does not require a
promise that each selected coordinate is nonzero. A support with value at most
the threshold exists exactly when (1) has value at most the threshold.

The gap proves additive approximation hardness: an estimate within
\(\delta_\theta/4\) is at most \(\delta_\theta/2\) on YES instances and exceeds
\(3\delta_\theta/4\) on NO instances. A threshold between these two values
decides SUBSET SUM.

## Bounded magnitudes do not restore exact tractability

Let \(M=1+B+\sum_i A_i\). Substitute \((x,s)=M(\widehat x,\widehat s)\) into
(4), then divide the objective by \(M^2\). The quadratic matrix is unchanged;
the amplitudes and target become \(A_i/M\) and \(B/M\), and the state penalty
becomes \(\mu/M^2\). All linear coefficients have absolute value at most two,
all indicator penalties are at most one, and the constant is at most one.
All data remain rational of polynomial encoding length. The YES/NO threshold
and gap become \(\delta_\theta/(4M^2)\) and \(\delta_\theta/M^2\).

Consequently, exact NP-hardness also holds with bounded coefficient magnitudes
and the same near-identity matrices. This does **not** give fixed-accuracy
hardness under that normalization: the gap can be exponentially small. The
state penalties can be correspondingly small, and exact support choices can
require many bits of precision.

Even the optimal continuous solutions in the normalized construction have
uniformly bounded coordinates. Setting every variable and indicator to zero
gives objective \(\theta^2(B/M)^2\le\theta^2\). At any optimum, nonnegativity
of the residual representation gives \(|e_i|\le\theta\),
\(|r_i|\le\theta\), hence \(|\widehat x_i|\le1+\theta\). The recurrence then
implies

\[
 |\widehat s_i|\le
 \frac{\theta(2+\theta)}{1-\theta}<1
 \quad(0<\theta\le1/10).
\]

Thus the difficulty is not explained merely by unbounded optimizing states.
It concerns exact distinctions, penalty scales, and signed interactions.

## Unit penalties and bounded coefficients

The following strengthening trades the fixed Hessian of Theorem 1 for unit
indicator penalties and bounded linear coefficients. The two constructions
should not be combined into an unsupported claim that the Hessian can remain
independent of the input while all penalties equal one.

**Theorem 3.** Fix a rational \(0<\theta\le1/10\). Exact optimization of (1)
is NP-hard even when every \(\lambda_j=1\), every \(|c_j|\le9\), the support
graph is the same bandwidth-two triangle chain as in Theorem 1, and

\[
 (1-3\theta)I\preceq K\preceq(1+3\theta+2\theta^2)I.
                                                               \tag{10}
\]

In particular, \(\|K-I\|_2\le3\theta+2\theta^2\le4\theta\). The corresponding
rational threshold decision problem is NP-complete. All nonconstant objective
coefficients are bounded by an absolute constant. The constant term and the
decision threshold have magnitude \(O(n)\). The construction uses rational
entries of polynomial encoding length; some nonzero entries can be exponentially
small. No uniform positive decision gap is claimed.

**Proof.** Restrict SUBSET SUM to positive integers with
\(0<B\le M:=\sum_i a_i\); instances outside this range are trivial and can be
handled separately. Put

\[
 b_i=\frac{a_i\theta^i}{M},\qquad
 T=\frac{B\theta^n}{M},\qquad D=4.
\]

Thus \(0<b_i\le\theta^i\le\theta\) and \(0<T\le\theta^n\le1\).
Introduce continuous variables \(x_i,t_i\) and their binary indicators
\(z_i,\zeta_i\). Set the fixed initial value \(t_0=D\). Minimize

\[
\begin{split}
 H={}&\sum_{i=1}^n(x_i^2-2x_i+z_i)\\
 &+\sum_{i=1}^n
    [t_i-\theta t_{i-1}-b_ix_i-D(1-\theta)]^2\\
 &+\theta^2(t_n-D-T)^2+\sum_{i=1}^n\zeta_i,             \tag{11}
\end{split}
\]

subject only to \(x_i(1-z_i)=t_i(1-\zeta_i)=0\) and binary indicators.
For \(i=1\), the dynamic residual is \(t_1-b_1x_1-D\), since \(t_0=D\).
This boundary adjustment is essential. Every indicator penalty in (11) is
exactly one. The first summand is \((x_i-z_i)^2\) on feasible points.

For a binary vector \(z\), define the nonnegative reference trajectory

\[
 s_0^z=0,\qquad s_i^z=\theta s_{i-1}^z+b_iz_i.
\]

It satisfies

\[
 0\le s_i^z
 =\frac{\theta^i}{M}\sum_{j=1}^i a_jz_j\le\theta^i,
 \qquad
 s_n^z=T\quad\Longleftrightarrow\quad\sum_i a_iz_i=B.
                                                               \tag{12}
\]

Let \(e=x-z\), \(d=t-D\mathbf1-s^z\), and let \(L\) be the strictly lower
shift matrix. Put \(R=I-\theta L\). The vector of dynamic residuals in (11)
is exactly

\[
 Rd-\operatorname{Diag}(b)e.
\]

The quadratic form

\[
 \|e\|_2^2+\|Rd-\operatorname{Diag}(b)e\|_2^2
 \ge(1-3\theta)(\|e\|_2^2+\|d\|_2^2)                 \tag{13}
\]

follows by Gershgorin. To check the bound directly, an \(e_i\) row has diagonal
\(1+b_i^2\) and off-diagonal absolute sum at most \((1+\theta)b_i\).
An internal \(d_i\) row has diagonal \(1+\theta^2\) and off-diagonal absolute
sum at most \(2\theta+b_i+\theta b_{i+1}\le3\theta+\theta^2\).
The last state row has diagonal one and off-diagonal sum at most
\(\theta+b_n\le2\theta\). Boundary rows have fewer entries. Each row therefore
has diagonal minus absolute off-diagonal sum at least \(1-3\theta\).
The terminal square in (11) is nonnegative and is not needed in (13).

Suppose \(k\) state indicators \(\zeta_i\) equal zero. The corresponding
\(t_i\) are zero, so \(d_i=-D-s_i^z\le-D\), and \(\|d\|_2^2\ge kD^2\).
Equations (11) and (13) imply

\[
 H\ge n-k+(1-3\theta)kD^2
   =n+\bigl((1-3\theta)D^2-1\bigr)k.                  \tag{14}
\]

For \(D=4\) and \(\theta\le1/10\), the coefficient of \(k\) exceeds one.
On the other hand, selecting \(z=0\), setting \(x=0\), taking every
\(\zeta_i=1\), and setting every \(t_i=D\) gives
\(H=n+\theta^2T^2<n+1\). Consequently every global optimum has all state
indicators equal to one. This conclusion is proved from the objective and
does not impose extra indicator constraints.

With those state indicators on, (11) is \(n\) plus a sum of squares. Its
minimum equals \(n\) if and only if every square vanishes. The first squares
give \(x=z\), the dynamic squares give \(t=D\mathbf1+s^z\), and the terminal
square then gives \(\sum_i a_i z_i=B\) by (12). Thus the decision threshold is
exactly \(n\). Attainment follows from the positive definite quadratic form
and the finite set of supports; hence on NO instances the minimum is strictly
larger than \(n\).

In the order \((x_1,t_1,\ldots,x_n,t_n)\), the homogeneous quadratic matrix
has diagonal \(1+b_i^2\) on \(x_i\), diagonal \(1+\theta^2\) on every state,
and off-diagonal entries

\[
 K_{x_i,t_i}=-b_i,\qquad
 K_{t_{i-1},t_i}=-\theta,\qquad
 K_{t_{i-1},x_i}=\theta b_i\quad(i\ge2).                \tag{15}
\]

The same row bounds give (10), strict diagonal dominance, and the claimed
graph. Every \(b_i>0\), so no triangle edge disappears. To verify the linear
coefficient bounds, write \(h_1=D\) and \(h_i=D(1-\theta)\) for \(i\ge2\).
The \(x_i\) coefficient is \(-2+2h_i b_i\), which has absolute value at most
two. The state coefficients are \(-2h_i+2\theta h_{i+1}\) for \(i<n\), and
\(-2h_n-2\theta^2(D+T)\) at \(n\). Their absolute values are less than nine.
The constant term is \(\sum_i h_i^2+\theta^2(D+T)^2\le16n+1/4\).
The numerator and denominator lengths of \(b_i,T\) are polynomial in the
SUBSET SUM input size. Membership in NP follows by the same support certificate
argument as Theorem 1. This proves the theorem.

An explicit gap clarifies the role of precision. For all state indicators on,
let \(r\) denote the dynamic residual vector and \(u=t_n-D-T\). Then

\[
 \frac{\theta^n}{M}\left(B-\sum_i a_i z_i\right)
 =\sum_i\theta^{n-i}b_i e_i+\sum_i\theta^{n-i}r_i-u.
\]

Every NO instance therefore has

\[
 H-n\ge
 \frac{\theta^{2n}/M^2}
 {\theta^{2n}\sum_i a_i^2/M^2+
  \sum_{j=0}^{n-1}\theta^{2j}+\theta^{-2}}>0.             \tag{16}
\]

The optimum has all state indicators on by (14), so (16) applies to the global
optimum. It can be exponentially small even when all \(a_i\) are moderate.
The reduction does not show a polynomial lower bound on the gap or strong
NP-hardness. It establishes that arbitrarily weak rational interactions can
carry exact combinatorial information even with unit penalties and bounded
linear terms.

## Literature comparisons and priority boundary

The following sources were examined on 2026-09-22. An absence of the present
theorem in these sources is not a novelty proof.

| Source examined | Relevant established result | Comparison with this note |
| --- | --- | --- |
| Das and Kempe, *Algorithms for Subset Selection in Linear Regression*, STOC 2008, [author manuscript](https://david-kempe.com/publications/regression.pdf), Theorem 4.1 and §9 | Approximation for cardinality-constrained regression with bounded covariance bandwidth; exact algorithms for other graph structures; discusses extending tree methods to bounded treewidth. | An older, direct source for the algorithmic question. Their tree graph includes the response variable, while their bandwidth restriction concerns the covariates alone. The present theorems concern penalized selection and the continuous quadratic matrix, so they should not be described as resolving that entire question. No bandwidth-two hardness theorem was identified in the inspected text. |
| Del Pia, Dey, Weismantel, *Subset Selection in Sparse Matrices*, [2020 author manuscript](https://www2.isye.gatech.edu/~sdey30/SubsetSparse.pdf), introduction and main structural result | Polynomial-time subset selection when a design matrix consists of fixed-size diagonal blocks plus a fixed number of extra columns. | This restricts the design matrix, not just its Gram matrix. The sparse chain factors used here are not of that block-plus-fixed-columns type. The result therefore does not give a conflicting exact algorithm. |
| Bhathena, Fattahi, Gómez, Küçükyavuz, *A Parametric Approach for Solving Convex Quadratic Optimization with Indicators Over Trees*, [arXiv:2404.08178v1](https://arxiv.org/html/2404.08178v1), Theorem 3.2 and §1.2 | Exact \(O(N^2)\) arithmetic-time algorithm for positive definite Hessians supported on a tree; discusses path and Stieltjes algorithms. | The present pure-indicator model has the same basic unconstrained structure, but hardness already at treewidth two and arbitrary proximity to a diagonal matrix. The source does not state this hardness result. |
| Gómez, Han, Lozano, *Real-time solution of quadratic optimization problems with banded matrices and indicator variables*, [arXiv:2405.03051v1](https://arxiv.org/html/2405.03051v1), Theorem 1 | An additive approximation guarantee with runtime polynomial in dimension and \(\|d\|_\infty^2/\epsilon\), for fixed bandwidth and eigenvalue bounds. | The large-amplitude constant-gap construction has large \(\|d\|_\infty\); the bounded-amplitude construction has a small required \(\epsilon\). Neither contradicts the approximation theorem. The source discusses bandwidth greater than one but does not state the present hardness theorem. |
| Bhathena, Fattahi, Gómez, Küçükyavuz, *Solving Convex Quadratic Optimization with Indicators Over Structured Graphs*, [arXiv:2603.02103v1](https://arxiv.org/html/2603.02103v1), Definition 5, Theorem 1, Corollary 1 | Exact parametric algorithms under additional assumptions controlling the number of near-optimal local supports; complexity also depends on geometry, conditioning, and solution bounds. | Theorem 1 here rules out removing all numerical or support-separation dependence merely because bandwidth and condition number are small. It does not prove that their specific margin parameter alone is necessary, or evaluate that parameter on this family. |
| Gómez and coauthors, *Convexification of Mixed-Integer Quadratic Optimization via Decision Diagrams*, [arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1), §§7–8 and Proposition 9 | Structure-dependent exact diagrams, and approximation by neighborhood merging under spectral and volume-growth assumptions. | This gives stronger current positive theory than an unrestricted treewidth argument. The exact bandwidth-two obstruction and coefficient/precision distinction here remain compatible with its approximate guarantees. No equivalent hardness statement was identified in the inspected text. |
| Lerner and Parr, *Inference in Hybrid Networks: Theoretical Limits and Practical Algorithms*, UAI 2001, [§3, Theorems 1–2 and Corollary 3](https://arxiv.org/pdf/1301.2288) | SUBSET SUM is encoded in a chain of conditional Gaussian means; inference and finding the most likely discrete instantiation are hard even on simple hybrid graphical structures. | This is a substantive antecedent for the accumulation mechanism. Its model has switch-dependent Gaussian offsets and inference operations. It does not directly give the present uncoupled zero-indicator quadratic model with a fixed near-identity Hessian and positive separable penalties. A careful reduction comparison is needed before claiming conceptual originality. |
| Faenza, Muñoz, Pokutta, *New Limits of Treewidth-Based Tractability in Optimization*, Mathematical Programming 191 (2022), [local source](../literature/papers/faenza2022-new-limits-of-treewidth-based/fulltext.md), Theorem 3.6 | Limits for broad polynomial optimization families as intersection treewidth grows. | The present result fixes treewidth at two, imposes a positive definite quadratic objective, and uses only independent zero indicators. It is a different and substantially narrower hardness boundary, not a replacement for their general results. |

Searches included combinations of “quadratic optimization”, “indicator”,
“bandwidth 2”, “banded matrices”, “treewidth two”, “NP-hard”, “subset sum”,
“sparse regression”, and “switching linear Gaussian”. The most important
additional equivalence check was the older hybrid-inference chain reduction.
The result should provisionally be described as an explicit sharp structural
hardness theorem whose exact priority remains under investigation.

## Interpretation, limits, and next questions

The theorem gives a concrete boundary for exact solver design. A favorable
Hessian spectrum and a small graph separator do not by themselves bound the
complexity of support selection. This remains true when every local continuous
subproblem is extremely well-conditioned. Approximation, an appropriate margin,
or additional sign structure can still make useful algorithms possible.

The proof is deliberately narrow. It does not establish strong NP-hardness,
hardness at fixed normalized accuracy and bounded linear terms, or simultaneous
unit penalties and a Hessian independent of the input. It does not establish that typical
time-series instances are difficult. It also does not show hardness of the
particular second-difference or moving-average Hessian families used in
applications. Such claims would require new reductions or other evidence.

Possible consequential directions are: characterize the role of frustrated
triangles rather than general treewidth; identify a quantitative margin that
matches exact tractability and precision requirements; determine whether common
penalties and an input-independent Hessian together restore tractability; and compare its
parametric message complexity with current exact decision-diagram constructions.
These are open questions in this note, not established open problems in the
literature.

## Verification record

The proof above uses exact identities and Gershgorin bounds. The author of this
note independently checked the strengthened near-identity construction proposed
by the coordinating researcher, including the terminal diagonal correction,
the powers in (3) and (6), the positive state penalties, and the gap constant.
This is a cross-check during development, not a completed adversarial review.

The unit-penalty construction in Theorem 3 was also independently checked during
development: in particular, the first residual uses \(t_0=D\), the baseline
argument forces the state indicators on rather than assuming that behavior,
and the lower bound (13) does not need the terminal residual. Fresh independent
adversarial review has been requested by the coordinating researcher.

No targeted computational command has yet been run for this construction in
this note. The coordinating researcher is preparing an independent rational
support-enumeration check. No project-wide tests or CI checks were run. A
numerical check, when added, can challenge the formulas on finite instances;
it cannot establish the all-dimension hardness theorem or its novelty.
