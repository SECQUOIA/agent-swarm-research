# Low-dimensional coupling and indicator quadratic optimization

Date: 2026-09-25. Status: exploratory synthesis and modest extensions, not a
proposed main contribution. The source audit found substantial prior overlap.
The mathematical statements below have exact finite checks; the independent
proof review is recorded at the end.

## Assessment

A small coupling rank is useful only with additional structure. For the
indicator quadratic model, the sign of a low-rank update matters even when the
continuous quadratic is positive definite in both cases. A negative update
admits a finite list of activation sets, including under matroid constraints.
A positive rank-one update already permits a SUBSET SUM encoding with unit
activation costs and uniformly bounded linear coefficients.

This distinction is a useful solver-design boundary, but the basic mechanism
is too close to established subset-selection results to justify making it the
main research direction. The matroid extension below is a reusable consequence
of the geometry, not evidence of a major original advance. No novelty claim is
made for fixed-rank tractability or positive-update hardness in general.

The repository's earlier
[bandwidth-two hardness result](../results/indicator-quadratic-treewidth-two-hardness.md)
restricts the support graph of the Hessian. The positive-update construction
here has a dense support graph and instead restricts its distance from a
diagonal matrix to rank one. Neither structural restriction implies the other.

## A fixed-rank algorithm with a matroid on the activation variables

Let \(D\) be a positive rational diagonal matrix, let
\(U\in\mathbb Q^{n\times r}\), and suppose
\(Q=D-UU^T\succ0\). The factorization is supplied as input. Let \(b,c\)
be rational vectors. Let \(\mathcal I\) be the independent sets of a matroid
on \([n]\), supplied by an independence oracle. Consider

\[
 \min\{x^TQx-2b^Tx+c^Tz:
     x_i(1-z_i)=0,\quad z\in\{0,1\}^n,
     \{i:z_i=1\}\in\mathcal I\}.                         \tag{1}
\]

The activation set may strictly contain the nonzero support of \(x\).
This distinction matters when some activation costs are negative.

**Proposition 1.** For fixed \(r\), problem (1) has an exact algorithm using
polynomially many rational operations, polynomial bit work, and polynomially
many calls to the independence oracle. It returns rational optimal \(x\)
and binary optimal \(z\). The exponent may depend on \(r\); no
fixed-parameter tractability bound is claimed. The same conclusion holds if
activation sets must be matroid bases.

**Proof.** Write \(u_i^T\) for row \(i\) of \(U\), and \(d_i=D_{ii}\).
The identity

\[
 -\|U^Tx\|^2=\min_{y\in\mathbb R^r}
       \{\|y\|^2-2y^TU^Tx\}
\]

is attained at \(y=U^Tx\). Conditional on \(y\) and an activation set
\(S\), minimizing over \(x\) gives

\[
 H_S(y)=\|y\|^2+\sum_{i\in S}h_i(y),\qquad
 h_i(y)=c_i-\frac{(b_i+u_i^Ty)^2}{d_i}.                  \tag{2}
\]

The minimizing active coordinate is \((b_i+u_i^Ty)/d_i\); every inactive
coordinate is zero. Thus (1) equals
\(\min_y\min_{S\in\mathcal I}H_S(y)\). This is an interchange of two
minima, not a minimax interchange or a duality assertion.

For fixed \(y\), a minimum-weight independent set for weights \(h_i(y)\)
is obtained by considering elements in increasing weight order, adding an
element when its weight is strictly negative and independence is preserved.
Use a fixed index order for ties. For matroid bases, use ordinary
minimum-weight basis greedy, without the sign restriction. The signs and
relative order of the \(h_i(y)\) therefore determine one optimal set.

Here is a rational construction that avoids algebraic sampling. Lift the
coordinates to

\[
 t=(y_j\ (1\le j\le r),\ y_jy_k\ (1\le j\le k\le r))
       \in\mathbb R^m,\qquad m=r+r(r+1)/2.
\]

Each \(h_i\) becomes a rational affine function \(\widehat h_i(t)\).
Enumerate every nonempty face of the arrangement of

\[
 \widehat h_i(t)=0,\qquad
 \widehat h_i(t)-\widehat h_j(t)=0\quad(i<j),             \tag{3}
\]

discarding constant equations while remembering their fixed signs. The
number of faces is \(n^{O(m)}\). One rational enumeration procedure inserts
hyperplanes successively and tests the negative, zero, and positive
extensions of each existing face. Strict feasibility is tested by giving
all strict inequalities a common slack \(\delta\in[0,1]\) and maximizing
\(\delta\) by rational linear programming. A positive optimum is equivalent
to feasibility of the strict system. In fixed dimension, the polynomial
number of faces and rational LP bounds give polynomial bit time and rational
relative-interior samples. Include lower-dimensional faces: an optimal parameter
can lie exactly on a tie or a zero-weight locus. Each face fixes every sign
and comparison in (3), so its sample determines a greedy activation set.
It is harmless that most sampled \(t\) need not be monomials of any \(y\).
They add feasible candidate sets rather than remove any.

For each candidate \(S\), solve the original quadratic with that activation
set:

\[
 x_S=Q_{SS}^{-1}b_S,\qquad x_{[n]\setminus S}=0,
 \qquad V_S=\sum_{i\in S}c_i-b_S^TQ_{SS}^{-1}b_S.       \tag{4}
\]

The empty set has value zero. Positive definiteness makes every principal
system invertible and every such solution globally optimal for its fixed set.
Rational linear algebra and comparisons in (4) have polynomial bit complexity.

To prove that the list includes a globally optimal activation set, take an
optimal pair \((x^*,S^*)\) of (1); it exists because the finite collection of
positive-definite quadratic subproblems all attain their minima. Set
\(y^*=U^Tx^*\). The lifted point of \(y^*\) belongs to an enumerated face.
Its candidate \(T\) is a minimum-weight independent set at \(y^*\), giving
\(H_T(y^*)\le H_{S^*}(y^*)=V^*\). On the other hand,
\(V_T=\min_yH_T(y)\) is the value of a feasible activation set for the
original problem. Consequently

\[
 V^*\le V_T\le H_T(y^*)\le V^*.
\]

The candidate is optimal. For \(r=0\), (2) consists of constant weights and
one greedy call suffices. This completes the proof. \(\square\)

The algorithm need not constrain the fixed-set minimizer in (4) to the face
that produced it. Its feasibility in the original problem and the preceding
inequality chain are sufficient. This observation removes a semialgebraic
optimization step.

Direct enumeration of realizable sign conditions of the quadratics in
\(\mathbb R^r\) could improve the dimension dependence. That improvement is
not needed for the stated polynomial result and is not analyzed here.

## Positive rank one with unit activation costs

**Proposition 2.** Fix any integer \(k\ge2\). Deciding whether the optimum
is at most a supplied threshold in the uncoupled-indicator quadratic model is
NP-complete even on a family with

\[
 Q=I+uu^T,
 \quad u_i>0,
 \quad c_i=1,
 \quad 1<b_i\le1+\frac1{k^2n},
 \quad \|Q-I\|_2\le\frac1{k^2n}.                       \tag{5}
\]

There are no cardinality or other constraints on the indicators. The same
hardness construction works if every continuous variable is also required to
belong to \([0,2]\). These are exact, weak hardness claims.

**Proof.** Take positive SUBSET SUM weights \(a_i\), let
\(A=\max_i a_i\), and assume \(0<B\le\sum_i a_i\le nA\), excluding
trivial instances. Set \(\tau=1/(knA)\). Under the indicator constraints,
consider the convex quadratic objective

\[
 F(x,z)=\sum_i(x_i^2-2x_i+z_i)
             +\tau^2(a^Tx-B)^2.                        \tag{6}
\]

On indicator-feasible points, its first sum equals
\(\sum_i(x_i-z_i)^2\). In particular \(F\ge0\), and \(F=0\) holds
exactly when \(x=z\) is a subset summing to \(B\). Expansion of (6) gives
the claimed model with

\[
 u=\tau a,\qquad b_i=1+\tau^2Ba_i,\qquad c_i=1,
 \qquad\text{constant }\tau^2B^2.
\]

The constant is removed by changing the decision threshold. The bounds in
(5) follow from
\(\tau^2\sum_i a_i^2\le1/(k^2n)\) and
\(\tau^2Ba_i\le1/(k^2n)\). The Hessian of the objective is \(2Q\).

For a fixed activation set \(S\), write
\(a(S)=\sum_{i\in S}a_i\). Direct completion of squares gives

\[
 x_i=1+\frac{\tau^2a_i(B-a(S))}
                    {1+\tau^2\sum_{j\in S}a_j^2}
 \quad(i\in S),
 \qquad
 F_S=\frac{\tau^2(B-a(S))^2}
                    {1+\tau^2\sum_{j\in S}a_j^2}.       \tag{7}
\]

Since \(|B-a(S)|\le nA\), each active coordinate differs from one by
at most \(1/(k^2n)\), hence belongs to \([3/4,5/4]\). Thus adding the
box \([0,2]^n\) leaves all fixed-set optima unchanged. On a NO instance,
every support has

\[
 F_S\ge\frac{\tau^2}{1+1/(k^2n)}>0.                    \tag{8}
\]

The reduction has polynomial binary encoding length. A proposed activation
set is a polynomial certificate because (7) can be evaluated exactly in
rational arithmetic. More generally, for the unboxed model (4), with the
positive-update \(Q\), certifies the fixed-set value. This proves the stated
decision hardness and membership. \(\square\)

The decisive gap in (8) can be exponentially small in the input bit length.
This proof does not rule out efficient useful additive approximation. It
also does not establish strong NP-hardness or hardness for a fixed positive
additive tolerance. Good conditioning of the continuous quadratic alone
does not resolve exact activation decisions.

There is a concrete pseudopolynomial algorithm for this constructed family.
For each attainable integer sum \(s=\sum_{i\in S}a_i\), retain only the
largest attainable \(t=\sum_{i\in S}a_i^2\). Formula (7) decreases in \(t\)
when \(s\) is fixed. A standard include-or-exclude dynamic program computes
these maxima with \(O(n\sum_i a_i)\) updates; exact rational comparison of
the resulting values recovers an optimum. This supports the limited
complexity interpretation of the construction.

## Literature comparison and priority limits

The following primary sources were examined on 2026-09-25. Failure to locate
an exact match is not evidence of novelty.

- Gao and Li, *A polynomial case of the cardinality-constrained quadratic
  optimization problem*, J. Global Optimization 56 (2013), 1441–1455;
  [2010 author manuscript](https://optimization-online.org/wp-content/uploads/2010/09/2721.pdf).
  The main algorithm assumes that the largest \(n-r\) eigenvalues coincide
  and uses an arrangement in \(r\) dimensions. Diagonal scaling puts
  \(D-UU^T\) in this structural class. Proposition 1 adds individual
  activation costs, oracle matroids, and a direct rational construction;
  it does not originate the tractability mechanism. Section 2.1 already uses
  a binary-enforcing sum of squares plus a linear-system residual under a
  cardinality constraint. Its one-row specialization is a close predecessor
  of Proposition 2. One sentence there writes an at-most-cardinality binary
  feasibility condition; equality at the displayed lower bound actually
  forces exactly that cardinality, so the zero vector is not a certificate.
- Del Pia, Dey and Weismantel, *Subset selection in sparse matrices*;
  [author manuscript](https://www2.isye.gatech.edu/~sdey30/SubsetSparse.pdf),
  Sections 2–4. They prove polynomial solvability for a block-diagonal design
  with fixed-size blocks and a fixed number of additional shared columns.
  Their diagonal case enumerates the ordering of affine absolute values to
  identify candidate supports. Eliminating a fixed number of unrestricted
  shared variables produces a negative low-rank Schur-complement update,
  making this a close structural predecessor. Their stated constraint is
  cardinality, rather than an oracle matroid with individual activation costs.
- Liu and Jiang, *Minimizing Sum of Truncated Convex Functions and Its
  Applications*; [author manuscript](https://arxiv.org/abs/1608.00236).
  Their low-dimensional piece-enumeration strategy is related. The gains in
  (2) are truncated concave quadratics plus a common quadratic, so the stated
  function class differs. The general strategy should not be claimed as new.
- Liu, Atamtürk, Gómez and Küçükyavuz, *Polyhedral analysis of quadratic
  optimization problems with Stieltjes matrices and indicators*;
  [primary article](https://link.springer.com/article/10.1007/s10107-025-02272-7).
  The same-sign linear-objective Stieltjes setting does not cover arbitrary
  signed data in Proposition 1. Its Proposition 6 hardness for an inverse
  matrix hull permits an arbitrary matrix objective; that is not the
  rank-one negative-semidefinite matrix objective obtained by eliminating
  \(x\) in (1). It therefore does not contradict Proposition 1.
- Hunkenschröder, Pokutta and Weismantel, *Minimizing a low-dimensional convex
  function over a high-dimensional cube*;
  [primary abstract](https://arxiv.org/abs/2204.05266), inspected as a separate
  direction screen. Its proximity approach depends on an integer projection
  matrix with bounded coefficients and specific convex-function assumptions.
  It does not give tractability based on projection dimension alone.
- Lee, Onn, Romanchuk and Weismantel, *The Quadratic Graver Cone, Quadratic
  Integer Minimization, and Extensions*;
  [primary abstract](https://arxiv.org/abs/1006.0773), inspected as a separate
  direction screen. It requires a supplied Graver basis and a suitable dual
  Graver cone condition. No extension of that condition was established here.

The last two entries are abstract-level screens, not complete theorem audits.
The literature reviewer independently found the Gao–Li overlap and reached
the same conservative significance assessment. The exact combination of
matroid activation and the supplied signed factorization was not located in
this bounded search. It remains a plausible modest extension, not a cleared
priority claim.

## Verification record and remaining questions

The targeted check was an inline `python` command using `fractions.Fraction`
and SymPy. It completed successfully on 2026-09-25 and checked:

- 852 positive-rank-one instances and 11,820 activation sets, with
  \(1\le n\le4\), weights in \(\{1,2,3\}\), every nontrivial target, and
  \(k=2\): exact stationary equations, the residual and value formulas in
  (7), the active-coordinate bounds, the SUBSET SUM equivalence, and (8).
- 40 signed rank-two examples on six variables with a partition matroid:
  exact enumeration of all feasible activation sets, followed by checking
  that greedy at \(y^*=U^Tx^*\) selects another globally optimal set.
  The random seed was `20260925`, with \(D=24I\), loading entries in
  \(\{-1,0,1\}\), linear coefficients in \(\{-4,\ldots,4\}\), and
  activation costs in \(\{-2,-1,0,1,2,3,4\}/7\).

These checks establish the formulas and optimal-parameter greedy implication
on the tested finite families. They do not implement arrangement enumeration,
prove arbitrary-dimension statements, or establish novelty. No project-wide
verification or CI inspection was performed. No Lean formalization was
attempted for this exploratory result.

The publication-readiness audit added the persistent, standard-library-only
checker [check_integer_structure.py](check_integer_structure.py). Running
`python research-20260925/check_integer_structure.py` passed all 852
positive-update instances and 11,820 support checks above, and also checked
the pseudopolynomial dynamic-programming value against exhaustive support
enumeration. Its deterministic signed rank-two sample contains 40 instances,
each tested with both independent-set and basis constraints for a partition
matroid, for 1,400 exact principal-system solves. This is reproducible finite
evidence for the formulas and the greedy-at-an-optimal-parameter implication;
it does not test the arrangement enumeration or establish its complexity.

Independent proof review: the agent `matroid_indicator_review` checked the
variational identity, matroid greedy rule, tie handling, monomial lifting,
rational bit complexity, and the positive-update construction. It separately
delegated the latter algebra to a fresh reviewer. The reviews accepted both
statements and emphasized the activation-set/support distinction, oracle
cost convention, inclusion of lower-dimensional faces, and fixed-rank rather
than FPT terminology. They also supplied the pseudopolynomial boundary just
recorded; its recurrence and monotonicity were rechecked directly here.

Potential useful follow-ups would need a stronger organizing idea: a
tractable mixed-sign coupling class larger than the negative-update class,
or an approximation guarantee that survives positive coupling without
depending on tiny exact gaps. Adding general knapsack constraints already
introduces ordinary discrete optimization hardness at rank zero. A
polynomial linear-optimization oracle by itself also does not justify the
matroid ordering argument; its optimal set need not depend only on the order
of individual weights. Any extension beyond matroids must address that
obstruction explicitly.
