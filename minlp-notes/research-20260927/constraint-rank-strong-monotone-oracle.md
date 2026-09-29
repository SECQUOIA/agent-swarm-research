# A constraint-rank algorithm for exact strongly monotone polynomial equilibria

Date: 2026-09-28. Status: proved and passed
[independent adversarial review](constraint-rank-strong-monotone-oracle-review.md),
including an additional fresh source and algorithm review.
Publication priority is unestablished.

The rank of the constraint normals, rather than the number of variables,
controls a randomized exact oracle algorithm. For a globally strongly
monotone rational cubic map over a rational polyhedron, the algorithm
uses expected \((r+1)^{O(r)}\operatorname{poly}(N)\) time with a
PosSLP oracle, where \(r\) is the constraint-matrix rank and \(N\)
is the explicit input length. The exponent of \(N\) is independent
of \(r\). Globally strongly convex quartic optimization is a special
case obtained by taking the gradient map.

The sampling method is classical Clarkson machinery for violator
spaces. The ingredient supplied here is an exact oracle implementation
for its small subproblems using the reviewed strongly monotone zero
theorem. This is a parameterized algorithmic consequence of that theorem,
not a new sampling method or an ordinary polynomial-time algorithm.

## 1. Inputs and outputs

Let \(T:\mathbb R^n\to\mathbb R^n\) be an explicit rational
polynomial map of degree at most three, with a supplied rational
\(\mu>0\) satisfying
\[
 \langle T(x)-T(y),x-y\rangle\ge\mu\|x-y\|^2
                        \qquad(x,y\in\mathbb R^n).       \tag{1}
\]
Let \(P=\{x:Ax\le b\}\), where \(A\in\mathbb Q^{m\times n}\)
and \(b\in\mathbb Q^m\) are explicit, and put
\(r=\operatorname{rank}A\). Given a rational polynomial \(h\)
of degree at most four, consider the unique solution \(p\), when
\(P\) is nonempty, of
\[
             p\in P,\qquad T(p)^{\mathsf T}(x-p)\ge0
                                    \quad(x\in P).      \tag{2}
\]
Existence and uniqueness for every nonempty rational polyhedron were
proved and independently reviewed in the
[constrained variational-inequality note](polyhedral-strong-monotone-vi-upper.md).

**Theorem.** There is a Las Vegas algorithm with a PosSLP oracle that
decides whether \(P\) is empty and, otherwise, answers any exact
order or equality comparison of \(h(p)\) with zero. Its expected
running time is
\[
                      (r+1)^{O(r)}N^C,                 \tag{3}
\]
for an absolute constant \(C\), with polynomial-length oracle
queries. Every returned answer is correct. Randomness affects the
running time, not the correctness of an answer.

The algorithm also outputs a polynomial-size exact representation of
\(p\): a rational affine chart \(p=\bar x+Zy_*\), together
with an explicit globally strongly monotone cubic map whose unique
real zero is \(y_*\). A zero-dimensional chart instead gives a
rational point. It does not print expanded algebraic coordinates.

The bare \(\mu\) formulation is a promise result. The verified
rational positive definite Jacobian Gram format in the
[zero theorem](strong-monotone-cubic-posslp-upper.md) gives a fully
checked input version, rejecting invalid certificates before other
branches. The coefficient encoding of \(h\) is included in \(N\).
No bound on the ambient dimension \(n\), beyond its explicit input
encoding, is imposed independently of \(N\).

For \(T=\nabla f\) with a globally strongly convex rational
quartic \(f\), take \(h=f-\tau\) for exact value comparison or
\(h=X_j-\tau\) for a coordinate. Empty-set value conventions can
be handled after rational feasibility checking. The theorem thus
provides (3) for those constrained optimization problems as well.

## 2. Feasibility and the violator mapping

First test feasibility of the full system \(Ax\le b\) by
ordinary rational LP. If it is infeasible, return immediately. This
step is important: every constraint subset used from now on is
feasible. No conventions about a variational inequality on an empty
set enter the sampling argument.

Let \(H=\{1,\ldots,m\}\). For every subset \(G\subseteq H\),
write
\[
 P_G=\{x:a_i^{\mathsf T}x\le b_i\text{ for }i\in G\},
 \qquad p_G=\text{the unique solution of }\operatorname{VI}(T,P_G).
\]
Define
\[
                    V(G)=\{i\in H:a_i^{\mathsf T}p_G>b_i\}.
                                                               \tag{4}
\]
The ground set contains row indices, so repeated inequalities remain
well-defined distinct elements.

The pair \((H,V)\) is a **violator space**: it has consistency
\(G\cap V(G)=\varnothing\), and locality
\[
 F\subseteq G,\quad G\cap V(F)=\varnothing
                  \quad\Longrightarrow\quad V(G)=V(F). \tag{5}
\]
Consistency is immediate. For locality, the hypothesis says that
\(p_F\) is feasible for \(P_G\). Since \(P_G\subseteq P_F\),
its variational inequality on \(P_F\) remains true for all points
of \(P_G\). Uniqueness therefore gives \(p_G=p_F\), proving
(5). A scalar objective and an ordering of solution values are not
needed. This matters for a nonpotential monotone map.

A basis of \(G\) means an inclusion-minimal \(B\subseteq G\)
such that \(V(B)=V(G)\). The **combinatorial dimension** is the
maximum size of a basis over all subsets. These are the definitions
in Gärtner, Matoušek, Rüst, and Škovroň,
[Violator Spaces: Structure and Algorithms](https://arxiv.org/pdf/cs/0606087v3),
Definitions 6--7 and 19. The minimality requirement concerns all subsets,
not just the final full instance.

## 3. Every basis has at most \(r\) rows

Fix any \(G\). At \(p_G\), the same short-feasible-segment and
Farkas argument as in the reviewed VI note gives
\[
             -T(p_G)=\sum_{i\in I}\lambda_i a_i,
 \qquad \lambda_i>0,\qquad a_i^{\mathsf T}p_G=b_i,       \tag{6}
\]
where \(I\subseteq G\) is a linearly independent set of active
normals, of size at most \(r\). To obtain independence, choose a
nonnegative conic representation with minimal positive support. If
its normals are dependent, subtract a scalar multiple of a dependence
until one positive coefficient becomes zero without making another
negative. This preserves the represented vector and contradicts
minimality. The empty support is allowed if \(T(p_G)=0\).

For every \(x\in P_I\), (6) gives
\[
 T(p_G)^{\mathsf T}(x-p_G)
           =-\sum_{i\in I}\lambda_i
                     a_i^{\mathsf T}(x-p_G)\ge0.
\]
Thus \(p_G\) solves the variational inequality using only the rows
\(I\). Uniqueness gives \(p_I=p_G\), hence \(V(I)=V(G)\).

This proves a bound on **every** minimal basis, not merely existence
of some small determining set. Apply the argument to a basis \(B\)
itself: there is \(I\subseteq B\) of size at most \(r\) with
\(V(I)=V(B)\). Minimality forces \(I=B\). Therefore the
combinatorial dimension is at most \(r\). In fact each basis is
linearly independent, although the algorithm below does not rely on
receiving a basis in advance.

The full feasibility precheck is what permits this \(r\) bound
without an extra infeasibility-basis case. If \(r=0\), all normals
are zero. Full feasibility implies that every row is automatically
satisfied, so \(P=\mathbb R^n\). The reviewed zero theorem solves
that case directly. Assume \(r\ge1\) from now on.

## 4. An exact primitive on at most \(r\) rows

The sampling algorithm will require the following primitive only
when \(|G|\le r\): given \(G\subseteq H\) and \(j\notin G\),
decide whether \(j\in V(G)\). The set \(G\) need not already
be a basis.

Enumerate all subsets \(I\subseteq G\), in a fixed order, and
discard those with dependent normals. There are at most \(2^r\)
subsets. For each remaining \(I\), parameterize
\(A_Ix=b_I\) as
\[
                 x=\bar x+Zy,\qquad Z^{\mathsf T}Z\succeq I.
                                                               \tag{7}
\]
Use free original coordinates, so \(Z\) contains an identity
row block. Rational elimination produces this chart with polynomial
bit length. Define
\[
             U_I(y)=Z^{\mathsf T}T(\bar x+Zy).          \tag{8}
\]
As in the reviewed VI proof, (1) and (7) imply global strong
monotonicity of \(U_I\) with modulus at least \(\mu\).
Let \(y_I\) be its unique zero and \(p_I=\bar x+Zy_I\).
These are represented implicitly; there is no need to print an
algebraic number. If \(I\) has rank \(n\), use the rational
solution of its equations directly.

For nonempty \(I\), put
\[
 \Lambda_I(y)=-(A_IA_I^{\mathsf T})^{-1}
                         A_I T(\bar x+Zy).              \tag{9}
\]
This is an explicit rational polynomial vector of degree at most
three and polynomial coefficient bit length. Check
\[
 \begin{aligned}
 b_i-a_i^{\mathsf T}p_I&\ge0 &&(i\in G),\\
 \Lambda_I(y_I)&\ge0,\\
 T(p_I)+A_I^{\mathsf T}\Lambda_I(y_I)&=0.
 \end{aligned}                                                   \tag{10}
\]
For empty \(I\), the multiplier vector is empty and the last
test means \(T(p_I)=0\). The stationarity residual is implied
by (8), but explicitly checking it avoids any implicit inference in
the verifier. Every scalar test in (10) is an explicit polynomial
observable of degree at most three at the zero of \(U_I\).
The reviewed zero theorem decides it with a constant number of
PosSLP queries. All query circuits have length polynomial in \(N\).

If (10) passes, feasibility, nonnegative multipliers, and the active
equations prove the variational inequality on \(P_G\) directly.
Thus \(p_I=p_G\). At least one subset passes, by the independent
support (6). Keep the first passing subset and chart. The primitive
then compares \(a_j^{\mathsf T}p_I-b_j\) with zero, using one
explicit linear observable. Its deterministic oracle running time
is at most \(2^r N^{C_0}\), for a fixed constant \(C_0\).

This subroutine can also return the chart and zero map for \(p_G\).
It uses no nondeterministic guesses, no approximate feasibility tests,
and no LP with an algebraic objective. Its dependencies are only the
reviewed zero theorem, rational linear algebra, and the elementary
conic-support argument. The more elaborate unambiguous-mask LP
verifier is not needed for this small-subproblem algorithm.

## 5. The primary sampling theorem and the bit model

Gärtner and coauthors, [the same primary paper](https://arxiv.org/pdf/cs/0606087v3),
Primitive 22 and Theorem 27, prove that a basis of a violator space
with \(m\) elements and combinatorial dimension at most \(r\)
can be found with an expected
\[
                         O(rm+r^{O(r)})                 \tag{11}
\]
violation tests. Their Sections 4.2--4.5, including the pseudocode
for both Clarkson stages, were read directly.

The size of the first argument to each primitive matters here.
In the two sampling stages, queries have first argument a returned
basis \(C\), so its size is at most \(r\). In the exhaustive
base case, the algorithm enumerates candidate subsets \(B\) of
size at most \(r\), and tests only \(V(B)\) or
\(V(B\setminus\{b\})\). It never needs the expensive primitive
on a large sampled set directly. The sampled sets can have
\(O(r^2)\) elements, but their bases are found through these
small-argument tests. The first Clarkson stage can draw larger
samples; those are processed by the second stage and still never
become large first arguments to the primitive. Thus the
implementation in Section 4 covers
every required call. Supplying the known upper bound \(r\) on
the combinatorial dimension suffices for the sampling analysis.

All oracle answers are exact. Clarkson's procedure stops only when
its basis has no violated rows of the relevant input set. Hence the
algorithm is Las Vegas. It returns a basis \(B\) of \(H\).
Since \(V(H)=\varnothing\), its solution \(p_B\) satisfies
all rows of \(H\). Its variational inequality on \(P_B\)
then also holds on \(P\), so \(p_B=p\). Run the small
subproblem routine on \(B\) once more to obtain the output
representation and perform the final observable comparison.

Combining (11) with the primitive cost gives (3), because the
\(2^r\) factor is absorbed by \((r+1)^{O(r)}\), and
\(m\le N\). Each individual oracle query and returned chart
still has polynomial encoding length in \(N\), independently
of how many samples are drawn.

The random sampling does not require explicit expansion of large
multisets. The second Clarkson stage stores multiplicities as binary
integers and doubles them on successful updates. The proof of its
Lemma 25 bounds the number of successful nonterminal reweightings
separately in each invocation of that stage by \(O(r\log m)\);
unsuccessful draws do not change weights.
Thus weight bit lengths are polynomial. Uniform sampling of a
specified number of copies can be performed by bounded-length random
integer draws and prefix sums, temporarily decrementing counts for
sampling without replacement. Before the exhaustive basis subroutine,
identify duplicate sampled copies with their original row indices:
multiplicity affects sampling probability, but does not change the
polyhedron or its VI solution. Rejection sampling for a uniform
integer uses expected constant trials. The first stage uses ordinary
subset sampling. The associated rational, integer, and random-bit
overhead is polynomial per counted sampling operation. This makes
the expected oracle-operation bound an expected bit-time bound of
the form (3), rather than a real-RAM claim with hidden number sizes.

## 6. What this establishes and what it does not

For fixed constraint-normal rank, exact equilibrium observables are
computable in expected polynomial time with a PosSLP oracle, while
the ambient polynomial dimension may grow. The dependence on the
rank is separated from the exponent of the input length. This is
stronger in that parameter than enumerating all \(m^{O(r)}\)
candidate supports. It is useful when many inequalities depend on
only a few linear combinations of the variables. Whether a particular
application has that structure and usable strong-monotonicity data
requires separate analysis.

The parameter is not the number of active constraints at the final
solution. Clarkson's dimension bound concerns bases of every
subproblem. A small final active support alone does not justify
replacing \(r\) by its size in the runtime bound. A box with one
independent coordinate bound per variable usually has rank \(n\),
so the theorem does not make general box-constrained instances
polynomial-time oracle problems.

The oracle remains material even at rank zero: the unconstrained
class already contains the reviewed PosSLP-hard gradient examples.
No ordinary fixed-parameter algorithm without the oracle is proved.
Nor does the theorem give a deterministic fixed-parameter algorithm,
a single PosSLP instance, or a polynomial bound independent of
\(r\). The output representation deliberately avoids an expanded
algebraic witness, whose size can be large.

Classical convex programs were already important applications of
LP-type algorithms, and the primary violator-space paper also treats
nonpotential complementarity settings. The present statement does
not claim that uniqueness, the support bound, or Clarkson sampling
is new. Its contribution is the explicit exact PosSLP primitive for
this polynomial class and the resulting constraint-rank bound.
No source examined so far establishes the same full input-and-oracle
statement, but the search is not exhaustive and publication priority
remains unestablished.

## 7. Verification status

The independent reviewer reconstructed locality without a potential,
the every-basis rank bound, feasibility, the support primitive, output,
and parameter dependence. An additional fresh reviewer audited the
primary sampling source, all primitive argument sizes, and the binary
sampling and weight bounds. No substantive defect was found. The final
revision clarifies the two stages' different sample sizes, duplicate
copies, and the scope of the update bound, and repairs one math display.

The author ran
`python3 research-20260927/check_constraint_rank_violator.py`, and
the independent reviewer read and reran the checker successfully.
It verifies 128 exact VI subproblems, 702 locality implications, and
all 11 minimal bases for two systems with constraint ranks one and
two in three ambient variables. The examples use nonsymmetric strongly
monotone affine maps and include redundant and zero rows. Their largest
bases have sizes one and two respectively. These finite checks support
the locality and every-basis arguments; they do not implement Clarkson
sampling or establish its expected runtime. No project-wide checks or
CI inspection were performed.
