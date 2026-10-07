# Discovering a nonunique optimum through a diagonal certificate

Date: 2026-10-02. This is a complete algorithm for a restricted certificate
class. It combines existing candidate generation and an independent global
test. The diagonal certificate itself is classical; no priority claim is
made. Review and exact diagnostics are recorded in [README.md](README.md).

## 1. Result

Let

\[
 F(x)=\tfrac12x^THx+b^Tx+c,\qquad x\in X=[\ell,u],
 \qquad H=H^T\in\mathbb Q^{n\times n}.
\]

All variables in this theorem are continuous. Substitute fixed coordinates
and reject empty boxes first. Supply a factor-tree decomposition of bag size
at most \(p\) and a rational \(L>0\) with \(H_{ii}\le L\). Let \(I\)
be their total rational encoding length. No optimizer, optimal set, or growth
constant is supplied.

For a feasible box KKT point \(s\), form the nonnegative diagonal matrix
\(D(s)\) by

\[
 d_i(s)=
 \begin{cases}
 2\partial_iF(s)/(u_i-\ell_i),&s_i=\ell_i,\\
 -2\partial_iF(s)/(u_i-\ell_i),&s_i=u_i,\\
 0,&\ell_i<s_i<u_i.
 \end{cases}                                                   \tag{1}
\]

Box KKT means zero interior gradients, nonnegative gradients at lower
bounds, and nonpositive gradients at upper bounds. Consider the class of
instances for which **at least one global optimizer** satisfies

\[
                         H+D(s)\succeq0.                        \tag{2}
\]

The promise is membership in this certificate class, not knowledge of a
particular certificate. Convex box QPs belong to it. It also contains
indefinite QPs with tilted optimal faces and disconnected optimal sets.

Let \(S=\arg\min_XF\). For any valid, unknown \(g>0\) satisfying

\[
       F(x)-f^*\ge g\operatorname{dist}(x,S)^2\quad(x\in X),
       \qquad \kappa=\max\{1,L/g\},                             \tag{3}
\]

there is an algorithm returning an exact rational optimizer, its exact
value, and an independently checkable description of the **entire** optimal
set in \(f(p,\kappa)\operatorname{poly}(I)\) bit work. The polynomial
exponent is absolute. A finite verifier does not trust either (2) as a
promise or (3): it checks rational box KKT and positive semidefiniteness.

Some positive set-growth constant exists for every bounded rational box QP;
the [previous proximal theorem](../../research-20261002/new-direction/proximal-growth-grid.md)
records the application of Luo and Sturm's classical quadratic error bound.
Existence does not give a useful numerical bound, and this theorem does not
compute or certify \(g\).

## 2. Soundness and completeness of the acceptance test

For every box KKT point \(s\), direct quadratic expansion gives

\[
 F(x)-F(s)=\tfrac12(x-s)^T(H+D(s))(x-s)
       +\tfrac12\sum_i d_i(s)(x_i-\ell_i)(u_i-x_i).               \tag{4}
\]

To verify the linear part, at a lower bound the gradient of the right-hand
side at \(s\) is \(d_i(u_i-\ell_i)/2\); at an upper bound it is its
negative; at an interior coordinate it is zero. The quadratic Hessian is
\(H+D-D=H\), and both sides vanish at \(s\). This proves the identity.

If (2) passes, all terms in (4) are nonnegative on \(X\). Thus \(s\)
is globally optimal independently of how it was found. Exact rational
PSD elimination, permitting zero pivots, verifies (2) in polynomial bit
time. A verifier must check zero-pivot off-diagonal entries as well; strict
positive-definite LDL alone is insufficient for the flat cases here.

Crucially, if the test passes at one optimum \(s\), it passes at **every**
optimum \(t\), with the identical diagonal matrix. Indeed, equality in
(4) gives

\[
 (H+D(s))(t-s)=0,\qquad
 d_i(s)(t_i-\ell_i)(u_i-t_i)=0.                                 \tag{5}
\]

For \(d_i(s)>0\), \(t_i\) is an endpoint. Also
\(\nabla F(t)=\nabla F(s)-D(s)(t-s)\). If that coordinate changes to
the other endpoint, its gradient changes from \(d_i(u_i-\ell_i)/2\)
to its negative, or conversely, and (1) still returns the same \(d_i\).
For \(d_i(s)=0\), both gradients are zero and (1) returns zero at either
an interior point or an endpoint. Hence \(D(t)=D(s)\). The argument does
not require either optimum to be isolated or rational.

This invariance is essential: the candidate algorithm may approach any
optimal component. Existence of an unrelated certificate at only one
distinguished optimizer would not justify the stopping theorem below.

## 3. Algorithm with untrusted conditioning guesses

The existing [proximal grid algorithm](../../research-20261002/new-direction/proximal-growth-grid.md)
has an explicit finite stage budget and grid-size bound for a supplied
\(K\ge1\). Its sound interpretation as a global interval requires
growth \(L/K\), but its grids and arithmetic can be computed even when
that guess is false. Its fresh boxes always contain their feasible centers.
No step requires an unverified oracle for global optimization.

Use the arithmetic height constants \(D,H_0,\tau\) of the
[exact recovery lemma](../../research-20261002/new-direction/proximal-exact-recovery.md),
computed from the original rational QP, with
\(\tau=1/(4nDH_0)\). The name \(H_0\) here denotes that lemma's
integer determinant bound, not the Hessian \(H\).

For \(K=1,2,4,8,\ldots\), perform the following finite trial.

1. Choose the largest dyadic
   \(\varepsilon\le\min\{1,L\tau^2/(4K)\}\).
   Run the proximal grid algorithm for its full explicit stage budget
   \(J\), the first integer for which
   \(Ln s_0^2 4^{-J}/2\le\varepsilon\), or zero if it already holds.
   Here \(s_0\) is the maximum original interval width. Do not regard its
   reported lower bound as independently valid.
2. Take the last feasible grid point \(y\). Select an original bound
   whenever a coordinate of \(y\) is within \(\tau\) of that bound.
   Solve the rational linear feasibility problem consisting of those
   selected bounds, the original box, and zero gradient equations in the
   remaining free coordinates. If infeasible, reject this trial.
3. Obtain any rational feasible solution \(s\) of this LP, with the usual
   polynomial bit-size LP output guarantee. Check all original box KKT
   conditions, form (1), and check (2). Accept **only** if these checks pass.

If no coordinates remain after preprocessing, their fixed point is already
the exact output. No rational reconstruction of a guessed global objective
interval is required: the accepted value is the exact evaluation \(F(s)\).

Every acceptance is sound by (4), including acceptance during an invalid
conditioning trial. At the first \(K\ge\kappa\), which has
\(K\le2\kappa\), the proximal theorem guarantees a global gap at most
\(\varepsilon\). Consequently

\[
 \operatorname{dist}(y,S)^2\le K\varepsilon/L\le\tau^2/4.
\]

The exact recovery lemma makes the selected-face LP feasible and **every**
feasible solution globally optimal. Section 2 then makes the diagonal test
pass, regardless of which optimal component that LP returns. Thus the
algorithm terminates by this trial on the claimed class.

The number of grid labels and stages in a trial is bounded by the supplied
\(K\) even when its growth guess is false: labels depend on the explicitly
bounded fresh-box radius and the chosen grading ratio; the stage budget is
imposed directly. The proximal rational-denominator argument is likewise
algebraic, not conditional on growth. Each trial therefore costs
\(f_0(p,K)\operatorname{poly}(I+\log K)\). Summing through
\(K\le2\kappa\) gives the asserted bound. The LP uses original
coefficients and selected bound indices, so its rational output has
polynomial length in \(I\); grid-point denominators do not enter its
equations. All final certificates consequently have polynomial length in
\(I\), although discovering them uses the stated parameters.

Outside this certificate class, the procedure may never accept. It is not
a decision procedure for class membership or a general unknown-growth
algorithm for arbitrary optimal sets. No failed trial certifies
nonmembership. A practical implementation needs an explicit work limit and
must report inconclusive termination when that limit is reached.

## 4. A compact exact description of every optimizer

For the accepted point \(s\), (4) proves the equivalence

\[
 x\in S\quad\Longleftrightarrow\quad
 \begin{cases}
 \ell\le x\le u,\\
 (H+D)(x-s)=0,\\
 d_i(x_i-\ell_i)(u_i-x_i)=0&\text{for every }i.
 \end{cases}                                                    \tag{6}
\]

For a PSD matrix, zero quadratic form is equivalent to membership in its
kernel. Thus no square-root coefficients occur in (6). This is a short
system of rational linear and quadratic equalities, with endpoint
alternatives kept implicit. It neither enumerates the connected components
nor expands a union of polytopes. The algorithm returns one rational
optimizer explicitly in addition to this full-set descriptor.

For example, on \([0,1]^3\),

\[
 F(x,y,t)=(x-y+t/2)^2+\tfrac18t(1-t)
\]

has the two optimal segments
\(\{(v,v,0):0\le v\le1\}\) and
\(\{(v,v+1/2,1):0\le v\le1/2\}\). Its diagonal is
\(D=\operatorname{diag}(0,0,1/4)\), while \(H+D\) is the rank-one
matrix \(2(1,-1,1/2)(1,-1,1/2)^T\). All Hessian diagonals are positive,
so coordinatewise concavity does not explain this case. Copies already
yield exponentially many components; the connected construction in the
[earlier audit](../../research-20261002/new-direction/unknown-growth-certificate-audit.md),
Section 5, supplies a fixed-width connected example in the same class.

The exact full-set descriptor does not establish a uniform polynomial-time
algorithm for projecting onto \(S\), counting its components, or answering
every quantified query about it. Those are separate tasks.

## 5. Prior comparison and scope

The maximal diagonal identity, including its invariance across optimizers,
is already established in
[flat-direction-certificates.md, Section 5](../../research-20261002/new-direction/flat-direction-certificates.md).
It is a diagonal Lagrangian sufficient condition for global quadratic
optimality, not a new certificate principle. The earlier proximal theorem
supplies a complete candidate algorithm under a trusted growth bound, and
the exact recovery lemma supplies a rational optimizer from distance to an
arbitrary optimal set. Neither alone makes an invalid guessed global bound
safe to accept.

An exact external comparator is Li, Wu, and Quan,
[Global optimality conditions for nonconvex minimization problems with quadratic constraints](https://link.springer.com/article/10.1186/s13660-015-0776-3),
Corollary 2, equation (14). Their box multiplier conditions have
\(\nabla F(s)+\operatorname{diag}(\lambda)(2s-\ell-u)=0\) and
\(H+2\operatorname{diag}(\lambda)\succeq0\), exactly the
certificate above with \(D=2\operatorname{diag}(\lambda)\).
The certificate class is thus an established Lagrangian exactness class;
this note does not claim a newly discovered tractable class in isolation.

The additional result is their complete combination: finite untrusted
growth trials, an acceptance test valid under every guess, proof that every
possible exact optimum passes on the promised class, and a compact
description of all optimizers. The continuous-variable restriction is
material: interior native-integer optima need not have zero gradient, so
(1)--(4) cannot be applied to arbitrary mixed-box KKT candidates unchanged.
The [endpoint result](endpoint-optimal-set.md) separately covers mixed
boxes in a different class.
