# Exact standard-slice barrier frontier for capped Lorentz product-ball lifts

Status: Proved; independently hostile-audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High

## Result

Let

\[
 C=\prod_{a=1}^kB_2^{s_a},\qquad
 M=\prod_{a=1}^kS^{p_a},\qquad p_a=s_a-1\geq2.             \tag{1}
\]

Suppose \(C\) has a proper affine lift over a finite product of Lorentz
cones \(Q_{r_i+2}\), \(1\leq r_i\leq c\), with a relative Slater point.
Assume that the lift has a globally labelled \(C^1\) feasible sheet
\(X:M\to\prod_iQ_{r_i+2}\) and globally labelled \(C^1\) dual factor
selections for every extreme row

\[
                         1-x_a^Tz,\qquad z\in S^{p_a}.     \tag{2}
\]

Restrict the standard product barrier

\[
                         F(w)=-\sum_i\log\det_{Q_{r_i+2}}w_i              \tag{3}
\]

to the lift's affine slice.  For each source put

\[
 h_a=\begin{cases}
 1,&c\geq p_a,\\
 \lceil s_a/c\rceil,&c<p_a.
 \end{cases}                                               \tag{4}
\]

Then its self-concordant-barrier gradient parameter satisfies

\[
                  \boxed{\nu_{\rm std,slice}(F)\geq\sum_{a=1}^kh_a.}     \tag{5}
\]

This is exact over the stated regularity class.  Use one direct
\(Q_{p_a+2}\) factor when \(c\geq p_a\), and otherwise partition the
\(s_a\) Euclidean coordinates into
\(\lceil s_a/c\rceil\) groups of size at most \(c\).  The standard product
barrier of this direct/grouped lift, after its allocation equalities are
imposed, has parameter exactly \(\sum_ah_a\).

For homogeneous dimensions \(s_a=s\), this becomes

\[
 \inf\nu_{\rm std,slice}=
 \begin{cases}
 k\lceil s/(d-2)\rceil,&3\leq d<s+1,\\
 k,&d\geq s+1,
 \end{cases}                                               \tag{6}
\]

where \(d=c+2\) is the Lorentz dimension cap.  The conclusion concerns the
standard product log-determinant after affine restriction.  It does not
lower-bound an arbitrary custom barrier on a competing lifted domain.

## 1. Boundary determinant order

For \(x\in M\), let \(z_i(x)\in\{0,1,2\}\) be the Jordan nullity of the
\(i\)-th Lorentz component of \(X(x)\), and put

\[
                              Z(x)=\sum_i z_i(x).           \tag{7}
\]

Join \(X(x)\) to the relative Slater point by a feasible segment.  After a
Lorentz automorphism sends the interior endpoint to the Jordan unit, the
\(i\)-th determinant has a zero of exact order \(z_i(x)\).  Therefore the
one-variable restriction of (3) has

\[
 F(t)=-Z(x)\log t+O(1),\quad
 F'(t)=-{Z(x)\over t}+O(1),\quad
 F''(t)={Z(x)\over t^2}+O(1).                              \tag{8}
\]

The barrier-gradient inequality
\(|F'(t)|^2\leq\nu_{\rm std,slice}F''(t)\) gives

\[
                         \nu_{\rm std,slice}\geq Z(x)
                         \quad\text{for every }x\in M.     \tag{9}
\]

Thus it remains only to show that \(Z(x)\geq\sum_ah_a\) somewhere.

## 2. Active contact channels are charged to nullity

At the contact row \(z=x_a\), mixed differentiation of the factorization
of (2) writes the positive-definite tangent metric on \(S^{p_a}\) as a sum
of positive-semidefinite Lorentz phase channels

\[
 H_i^a=\alpha_i\beta_i^a(Dq_i^a)^*Dq_i^a,\qquad
                              \operatorname{rank}H_i^a\leq r_i.          \tag{10}
\]

Call \(i\) active for \(a\) at \(x\) when \(H_i^a(x)\neq0\), and write
\(\ell_a(x)\) for the number of active labels.  Cylindrical
complementarity and strict convexity of a Lorentz cone imply pointwise
no-sharing:

\[
 H_i^a(x)\neq0\quad\Longrightarrow\quad H_i^b(x)=0
 \quad(b\neq a).                                           \tag{11}
\]

Every active channel has two nonzero complementary boundary factors.
Its primal factor therefore has Lorentz nullity one.  Distinct active
labels are distinct product factors, whereas inactive factors have
nonnegative nullity.  Hence

\[
              \sum_a\ell_a(x)\leq Z(x),\qquad
              \ell_a(x)\geq\left\lceil{p_a\over c}\right\rceil.          \tag{12}
\]

For \(c\geq p_a\), the right side is \(h_a=1\).  For \(c<p_a\), it equals
\(h_a\) unless \(c\mid p_a\), in which case it equals \(h_a-1\).

## 3. A nullity deficit would kill a nonzero top class

Let

\[
 D=\{a:c<p_a\text{ and }c\mid p_a\}.                       \tag{13}
\]

If \(D\) is empty, (12) gives \(Z(x)\geq\sum_ah_a\) at every point.
Suppose \(D\neq\varnothing\) and, contrary to the desired conclusion,

\[
                              Z(x)\leq\sum_ah_a-1
                              \quad\text{for every }x\in M.              \tag{14}
\]

Equations (12)--(14) imply that at every \(x\), at least one source
\(a\in D\) has exactly \(t_a=p_a/c\) active labels.  Thus the closed sets

\[
                         E_a=\{x:\ell_a(x)=t_a\},\qquad a\in D,           \tag{15}
\]

cover \(M\).  Partition each \(E_a\) into its finitely many clopen compact
strata \(E_{a,J}\) having the same exact active-label set \(J\).

On \(E_{a,J}\), rank \(p_a=t_ac\) with \(t_a\) channels of capacities at
most \(c\) forces every capacity to equal \(c\) and every partial rank
bound in (10) to be sharp.  On a neighborhood \(P_{a,J}\) of the compact
projection \(\pi_a(E_{a,J})\subset S^{p_a}\), the normalized dual phases
therefore give a local diffeomorphism

\[
                  Q_{a,J}:P_{a,J}\longrightarrow(S^c)^{t_a}.            \tag{16}
\]

The neighborhood is proper.  If it were the whole sphere, (16) would be a
finite covering.  For \(c=1\), the target has noncompact universal cover.
For \(c\geq2\), domain and target are simply connected, so the covering
would be a diffeomorphism, contradicting the target's nonzero intermediate
cohomology.  Thus

\[
                         H^{p_a}(P_{a,J};\mathbb Z)=0.      \tag{17}
\]

Choose pairwise disjoint neighborhoods
\(E_{a,J}\subset W_{a,J}\subset\pi_a^{-1}(P_{a,J})\), and put
\(U_a=\coprod_JW_{a,J}\).  If
\(u_a=\pi_a^*[S^{p_a}]\), then \(u_a|_{U_a}=0\).  Since the \(U_a\),
\(a\in D\), cover \(M\), the relative cup-product lemma gives

\[
                              \prod_{a\in D}u_a=0.          \tag{18}
\]

The Kunneth theorem says that this product is nonzero.  This contradiction
proves that some \(x\) has \(Z(x)\geq\sum_ah_a\), and (9) proves (5).

## 4. Exact direct/grouped barrier

For every small-cap source, use coordinate groups \(G\) and the standard
paraboloid Lorentz slice

\[
                        s_{a,G}\geq\|x_{a,G}\|^2,\qquad
                        \sum_Gs_{a,G}=1.                   \tag{19}
\]

After restriction, (3) is

\[
                  F_{\rm grp}
                  =-\sum_{a,G}\log(s_{a,G}-\|x_{a,G}\|^2).               \tag{20}
\]

Each summand has gradient parameter one, so imposing the independent
allocation equalities leaves parameter at most the number of factors,
\(\sum_ah_a\).  Exactness follows either from (5), or directly by
approaching a boundary point at which every displayed determinant tends
to zero.  A large-cap source uses
\(-\log(1-\|x_a\|^2)\), also with exact parameter one.  This proves
attainment in (5)--(6).

## Scope and relation to the other frontiers

The global \(C^1\) sheet assumption is essential to the topological step.
An arbitrary semialgebraic lift need only provide regular factor selections
on dense strata, and active labels can change across singular seams.  The
result is therefore a standard-slice frontier within a regular
factorization class, not an unconditional lower bound for every exact lift.

The contact channel, no-sharing, and proper-phase-neighborhood arguments
are proved and independently audited in
[A C1 cohomological no-sharing theorem for full product-ball Lorentz
factorizations](2026-09-04-c1-euler-no-sharing-product-balls.md).  Exact
determinant order along a Slater segment is the symmetric-cone argument in
[Exact standard-slice barrier frontier for capped symmetric-cone ball
lifts](2026-09-04-symmetric-cone-standard-slice-barrier-frontier.md).
The present combination is new to this note: it charges every active
contact label to a determinant zero and uses the phase-cover obstruction to
force all source-wise rounding premiums at one common boundary fiber.
The affine-restriction and gradient-parameter rules are part of the
classical framework of Nesterov and Nemirovskii,
[*Interior-Point Polynomial Algorithms in Convex
Programming*](https://doi.org/10.1137/1.9781611970791).  A targeted search
for standard restricted barriers together with Lorentz-product lifts,
product balls, and determinant boundary multiplicity found no statement of
(5)--(6).  Priority remains subject to specialist review.

An independent hostile audit passed the combination.  Activity makes both
contact factors nonzero complementary boundary vectors, so each pointwise
row-disjoint active label contributes one distinct unit of primal Jordan
nullity.  Vertex and interior components cannot be active and only add
nonnegative nullity.  The audit checked the deficit pigeonhole over the
heterogeneous set \(D\), the proper phase neighborhoods, and the relative
cup product of the nonzero subproduct \(\prod_{a\in D}u_a\).

It also checked the upper bound after all allocation equalities.  Each
restricted grouped determinant is
\(s_{a,G}-\|x_{a,G}\|^2\) and contributes parameter one; at a product
extreme all allocation inequalities are tight simultaneously.  Direct
large-cap ball barriers likewise have exact parameter one.  Thus the lower
and upper values in (5)--(6) match with the stated standard-slice scope.
