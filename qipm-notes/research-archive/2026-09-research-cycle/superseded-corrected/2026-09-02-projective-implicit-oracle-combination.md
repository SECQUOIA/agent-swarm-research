# Combining projective lazy refresh with implicit dual-coordinate oracles

Date: 2026-09-02

## Summary

Projective lazy refresh and the implicit dual-slack oracle compose more strongly
than a simple multiplication of their separate cost bounds.  If only \(R\)
classical Newton directions are extracted over a central-path tail, the whole
dual trajectory can be represented as an affine combination of those \(R\)
checkpoint vectors.  No \(m\)-vector update is needed at the intervening IPM
iterations, and no \(n\)-slack vector is ever formed.

An explicit tall, constant-column-sparse expander family makes every quantum
parameter benign: the directly split normal operator has constant
normalization and condition, the predictor RHS is explicit, constant
tomography accuracy suffices, and the projective constants are independent of
the number of duplicated inactive columns and of final precision.  This family
does **not** yield an honest quantum advantage over the best randomized
classical matrix-free method.  The scaling that keeps the block encoding
normalized makes the inactive normal contribution an average of bounded
terms, which can be sketched classically with a number of samples independent
of the tall dimension.

Making rare columns influential restores an \(n\)-dependent classical lower
bound, but it either increases the ordinary sparse block-encoding
normalization enough to erase the gain or reduces the quantum improvement to
Grover search for the exceptional columns.  Thus the natural combination is a
valid trajectory-compression theorem and a useful no-go result, not yet an
end-to-end QIPM speedup family.

## 1. Checkpoint-span representation theorem

Consider a dual-barrier path with explicit dual iterates

\[
 y_{t+1}=y_t+\lambda_t z_t,
 \qquad s_t=c-A^Ty_t.
\]

Suppose the projective lazy-refresh policy has checkpoint iterations
\(s_1,\ldots,s_R\).  Between checkpoints it uses only scalar multiples of the
last extracted direction.  Combining consecutive uses of the same direction
gives the exact representation

\[
 y_t=y_0+\sum_{r=1}^{R_t}\theta_{r,t}\widehat z_{s_r},
 \qquad R_t\le R,
\tag{1}
\]

where only the scalar coefficients \(\theta_{r,t}\) change at ordinary outer
iterations.

### Theorem 1 (projective checkpoint-span oracle)

Assume coherent read access to \(y_0\) and the extracted
\(m\)-vectors \(\widehat z_{s_r}\), each stored with \(B\) bits per entry.  If
the sparse columns of \(A\) have at most \(d_c\) entries, then:

1. a coordinate of \(y_t\) can be computed using \(R_t+1\) coherent vector
   reads and \(\widetilde O(R_tB)\) arithmetic gates;
2. a coordinate of \(s_t=c-A^Ty_t\) can be computed using
   \(O(d_cR_t)\) coherent vector reads and
   \(\widetilde O(d_cR_tB)\) arithmetic gates;
3. all vector loads over the path cost
   \(\widetilde O(RmB)\), while the \(T\) ordinary coefficient updates cost
   only \(\widetilde O(TB)\).

If the projective path theorem gives

\[
 R\le 1+\frac{2GV_{\rm proj}}{\eta},
\tag{2}
\]

then the changing-diagonal representation cost is

\[
 \widetilde O\!\left[
   mB\left(1+\frac{GV_{\rm proj}}{\eta}\right)+TB
 \right],
\tag{3}
\]

instead of \(\Theta(TmB)\) dual-vector writes or \(\Theta(TnB)\) slack-vector
writes.  On a finite projective tail, (3) is independent of final optimization
precision except for the scalar outer-loop term \(TB\).

#### Proof

Equation (1) follows by collecting all scalar steps made along each checkpoint
direction.  A query to coordinate \(j\) reads coordinate \(j\) of each stored
vector and evaluates the affine combination.  A slack query repeats this for
the at most \(d_c\) row indices in column \(a_i\), then computes
\(c_i-a_i^Ty_t\).  A checkpoint loads one new \(m\)-vector; a noncheckpoint
iteration changes only one coefficient.  Summing these costs and applying
(2) proves (3).

This theorem assumes that reuse of the approximate direction satisfies the
outer IPM's residual and feasibility contract.  The exact-central-path
projective theorem alone does not prove this for an oscillating inexact
trajectory.

### Scheduled versus tested refresh

If derivative bounds schedule the \(R\) checkpoints on a fixed additive
\(\mu\)-grid, no per-iteration residual test is needed.  An online policy must
also charge its residual tests.  A quantum norm/inner-product test can avoid a
classical \(\Theta(\operatorname{nnz}A)\) matvec, but its block-encoding calls,
state preparation, and additive error occur at all \(T\) iterations.  The
scheduled form is therefore the only version that automatically removes the
full tall-dimension cost over an arbitrarily long tail.

## 2. A tall sparse family with uniformly controlled quantum parameters

Let \(B\) be the oriented incidence matrix of a fixed-degree balanced
bipartite expander on \(m\) vertices, as in
`stable-active-subspace-qipm.md`.  For every vertex \(i\) and
\(k\in[K]\), introduce variables \(u_{ik},v_{ik}\) with columns

\[
  K^{-1/2}e_i,\qquad -K^{-1/2}e_i,
\]

and costs \(a_{ik}\in[1,2]\).  Consider

\[
\begin{aligned}
 \min\quad &\sum_{i,k}a_{ik}(u_{ik}+v_{ik})\\
 \text{s.t.}\quad &Bx+K^{-1/2}\sum_{k=1}^K(u_{\cdot k}-v_{\cdot k})
                    =B\mathbf1,\\
 &x,u,v\ge0.
\end{aligned}
\tag{4}
\]

There are \(n=|E|+2mK=\Theta(mK)\) variables.  Every column has at most two
nonzeros.  The optimum has \(u^*=v^*=0\), \(y^*=0\), and an active optimal
face in the \(x\)-variables.  Strict primal and dual feasibility follow as in
the original expander witness.

The complexity comparison below is in a common random/coherent-query model
for the array \((a_{ik})\) and for the formula-defined sparse columns.  If the
\(\Theta(mK)\) costs are instead supplied as an explicit file that must first
be loaded into coherent memory, that one-time \(\Omega(nB)\) construction cost
must be charged and there is no sublinear end-to-end wall-clock claim.  The
classical sketch receives the same random-access oracle.

Along the central path, the inactive normal contribution is diagonal:

\[
 D_{ii}(y)=\frac1K\sum_{k=1}^K
 \left[
  \frac1{(a_{ik}-y_i/\sqrt K)^2}
  +\frac1{(a_{ik}+y_i/\sqrt K)^2}
 \right].
\tag{5}
\]

Here it is convenient to use the projectively equivalent scaled dual normal
matrix.  Exact complementarity gives

\[
 \mu H_{\rm dual}(\mu)
 =\mu AS^{-2}A^T
 =AS^{-1}XA^T
 =\mu^{-1}C_\mu+\mu D_\mu.
\]

Multiplication by the scalar \(\mu\) changes neither the Newton solution ray
nor a relative residual test.  Formula (5) is the \(D_\mu\) term in this
scaled decomposition.

For a sufficiently small fixed tail start \(\mu_0\), central-path regularity
keeps \(|y_i|/\sqrt K\le1/2\).  Consequently

\[
  c_D I\preceq D(y)\preceq C_DI
\tag{6}
\]

for numerical constants independent of \(m,K\), and all derivatives of (5)
with respect to \(y_i\) are uniformly bounded.  The expander gap gives the
corresponding uniform bounds for the active Laplacian on
\(U=\mathbf1^\perp\).  Applying the implicit-function theorem to the
equilibrated central equations therefore gives projective constants
\(B_{\rm proj},L_{\rm proj},G_{\rm proj}=O_m(1)\) with respect to \(K\) and the
final precision.  This notation is deliberate: the argument here proves
uniformity in the tall factor \(K\), but does not prove a dimension-free bound
in \(m\).  The constants may depend on \(m\), the expander gap, and the chosen
\(\mu_0\).

The direct split is important.  Encode the active constant-degree incidence
matrix separately.  The inactive matrix has row sparsity \(2K\), column
sparsity one, and maximum entry \(K^{-1/2}\), so a standard sparse-access
normalization is

\[
 \alpha_{A_N}=O(\sqrt{(2K)(1)}K^{-1/2})=O(1).
\tag{7}
\]

Since the inactive slacks stay in a constant interval, (7) yields an
\(O(1)\)-normalized block encoding of (5).  The active-subspace split from the
stable equilibration theorem therefore gives

\[
 \alpha_M\|M_\mu^{-1}\|=O(1).
\tag{8}
\]

For the exact central predictor, the RHS is the fixed vector
\(b=B\mathbf1\), whose state is prepared from the known bipartition with
constant overhead.  Thus the RHS preparation factor is \(O(1)\).  A fixed
relative normal-equation tolerance permits normalized-state tomography
accuracy \(\xi=\Theta(\eta)\), so one refresh uses
\(\widetilde O(m/\eta)\) controlled QLS state preparations.  Equations
(2), (6), and (8) make the total solve/readout count over the tail

\[
 \widetilde O\!\left(
   \left(1+\frac{\mu_0}{\eta}\right)\frac{m}{\eta}
 \right),
\tag{9}
\]

independent of \(K\) and final precision.  The checkpoint-span oracle makes
the associated vector-load cost obey the same \(mR\) rather than \(mT\)
scaling.

Equation (9) is an honest parameter control statement.  It is not an honest
quantum speedup statement, for the reason below.

## 3. Classical randomized sketch obstruction

### Theorem 2 (bounded-average family has no tall-dimension advantage)

For family (4), fix any queried \(y\) in the safety interval and any
\(0<\varepsilon<1\).  For each vertex \(i\), sample

\[
 q=O\!\left(\varepsilon^{-2}\log(m/\delta)\right)
\]

indices uniformly from \([K]\) and replace (5) by the empirical average.
With probability at least \(1-\delta\), simultaneously for every \(i\),

\[
 \|\widehat D(y)-D(y)\|\le\varepsilon.
\tag{10}
\]

The sample and arithmetic cost is

\[
 O\!\left(m\varepsilon^{-2}\log(m/\delta)\right),
\tag{11}
\]

independent of \(K\) and hence of \(n=\Theta(mK)\).  Because the directly
equilibrated matrix and its inverse are uniformly bounded, (10) perturbs its
Newton direction by only \(O(\varepsilon)\) in relative norm.  The same
scheduled projective checkpoints and checkpoint-span representation can then
be used classically.

#### Proof

Every summand in (5) lies in a fixed bounded interval.  Scalar Hoeffding at
each vertex and a union bound prove (10)--(11).  Uniform invertibility and the
resolvent identity give the direction perturbation bound.

At constant IPM residual tolerance, (11) is
\(\widetilde O(m)\), matching the unavoidable \(\Omega(m)\) classical output
cost of checkpoint tomography.  Thus the quantum algorithm's independence of
the tall factor \(K\) is shared by the best randomized classical method.

The same issue extends beyond diagonal copies.  If a normal contribution is
an average of uniformly bounded rank-one terms with bounded leverage, a
classical matrix concentration sketch uses
\(\widetilde O(m/\varepsilon^2)\) samples (and at least \(m\) samples for a
full-rank spectral approximation).  At the constant accuracy used by an IPM,
the full \(m\)-coordinate quantum readout leaves no asymptotic tall-dimension
advantage.

## 4. Why rare influential columns do not repair this cleanly

To force a classical method to inspect \(K\) entries, one can hide a column
whose contribution to the normal matrix is \(\Theta(1)\).  In family (4), this
requires increasing its magnitude from \(K^{-1/2}\) to \(\Theta(1)\).  The
ordinary sparse-access normalization then changes from (7) to

\[
 \alpha_{A_N}=\Omega(\sqrt K),
 \qquad
 \alpha_{H_N}=\Omega(K).
\tag{12}
\]

Even if the true equilibrated normal matrix remains well-conditioned, a
black-box QLS solver pays the effective parameter
\(\alpha_{H_N}\|H_N^{-1}\|=\Omega(K)\), erasing the desired comparison with a
classical \(\Theta(K)\) scan.

A quantum algorithm can instead Grover-search for the exceptional columns in
\(O(\sqrt K)\) queries, store them explicitly, and then directly assemble a
constant-normalized operator.  That is a valid quadratic query improvement,
but its source is static unstructured-search preprocessing.  Once the marked
columns are known, both the quantum and classical solvers use the same
projective reuse.  It is not a new QIPM trajectory speedup.

More generally, a proposed hard family must avoid the following dichotomy:

1. **well-spread bounded contributions:** normalization and projective
   constants are benign, but classical randomized sketching removes the
   dependence on the tall dimension;
2. **rare influential contributions:** classical sketching becomes hard, but
   standard block-encoding normalization becomes large, or a separate Grover
   preprocessing step exposes the entire quantum gain.

## 5. Status

The checkpoint-span representation theorem is a rigorous useful positive
result.  It removes both per-iteration \(m\)-vector writes and \(n\)-diagonal
refreshes when the projective refresh count is finite.

The scaled-copy expander family rigorously controls the direct block-encoding
normalization, RHS preparation, tomography accuracy, and projective dependence
on tallness/final precision.  It fails the required classical comparison by
Theorem 2.  Therefore no honest end-to-end quantum advantage is claimed for
this family.

A successful next family would need a structured access model where a
constant-normalized quantum operator is available without also furnishing a
bounded-leverage classical sampling distribution, and where preprocessing is
not merely unstructured search.  No such explicit sparse LP family was found
in this cycle.
