# Packed PSD and grouped Lorentz lifts have identical reduced Newton oracles

Status: Proved; targeted literature screen completed; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High within the matched reduced-oracle, exact-fiber-centering,
and projected-state contract

## Result

Cross-source PSD column packing can reduce the number of cone factors, but
it cannot reduce quantum Newton-state generation complexity when both
formulations receive matched access to the reduced problem.

Fix \(C=(B_2^s)^b\), split each source ball into \(h\) nonempty coordinate
groups, and let \(H=bh\). Compare:

1. the grouped Lorentz/paraboloid lift with one factor per group; and
2. any PSD column packing of the same groups, with arbitrarily many groups
   and source balls sharing a PSD block.

After exact fiber centering, both restricted standard barriers marginalize
to the same function

\[
 \boxed{
 \bar F_h(x)=-h\sum_{a=1}^b\log(1-\|x_a\|^2)+bh\log h.}    \tag{1}
\]

Consequently, for every common objective, every common set of affine
constraints \(Ax=d\), every common projected iterate \(x\), and every
common path multiplier, their projected Newton/KKT matrix and right-hand
side are identical.

### Oracle-equivalence theorem

In the matched reduced-oracle model defined in Section 3, let
\(\mathsf{Q}_{\rm PSD}(\epsilon)\) and
\(\mathsf{Q}_{\rm Lor}(\epsilon)\) be the minimum bounded-error quantum
query complexities for preparing an \(\epsilon\)-approximation to the
normalized projected Newton state. Then

\[
 \boxed{\mathsf{Q}_{\rm PSD}(\epsilon)
       =\mathsf{Q}_{\rm Lor}(\epsilon).}                  \tag{2}
\]

The reductions preserve the matrix dimension, entry and state-preparation
oracles, block-encoding normalization \(\alpha\), spectrum, condition
number \(\kappa\), right-hand-side norm and overlap, and requested output
state. They use no approximation and no formulation-dependent oracle
queries.

The same statement holds for randomized or deterministic classical query
complexity. It also tensorizes over an adaptive sequence of reduced Newton
calls: any fiber-oblivious QIPM has the same oracle transcript and projected
state trajectory on the two formulations.

If the complete canonical oracle compiler is charged rather than supplied,
the two algorithms can use the same compiler from the common raw data.
Their oracle-construction gates, inter-query gates, workspace, and
measurements are then identical as well (up to an optional fixed public
coordinate relabeling). Thus (2) is an end-to-end state-generation
equivalence inside this model, not only a black-box query count.

Thus no end-to-end state-generation advantage can follow *solely* from
replacing \(H\) separate Lorentz factors by fewer cross-source PSD factors.
Any claimed advantage must use a different contract, such as free
packed-block state preparation, ambient lifted-state output, or a
formulation-specific preprocessing oracle. Those resources must be charged
and are not consequences of factor count.

This is an impossibility theorem for a precise access/output model, not a
claim that the two ambient conic formulations are computationally
equivalent under every encoding.

## 1. The two lifts

Index the coordinate groups by \(\gamma\), and let
\(\Gamma_a\) be the \(h\) groups belonging to source ball \(a\).
Write \(x_\gamma\) for the corresponding subvector.

The grouped Lorentz formulation, after the standard rotated-cone affine
reduction, is

\[
 q_\gamma=t_\gamma-\|x_\gamma\|^2>0,\qquad
 \sum_{\gamma\in\Gamma_a}t_\gamma=1,                     \tag{3}
\]

with restricted barrier

\[
                       F_{\rm Lor}(t,x)=-\sum_\gamma\log q_\gamma. \tag{4}
\]

For the packed PSD formulation, place arbitrary sets of columns in blocks
\(\ell\):

\[
 Z_\ell=
 \begin{pmatrix}S_\ell&W_\ell^T\\W_\ell&I_p\end{pmatrix}\succ0,
 \qquad D_\ell=S_\ell-W_\ell^TW_\ell\succ0,               \tag{5}
\]

and impose

\[
 \sum_{\gamma\in\Gamma_a}
       (S_{\ell(\gamma)})_{\gamma\gamma}=1.               \tag{6}
\]

Its restricted standard barrier is

\[
                     F_{\rm PSD}(S,x)=-\sum_\ell\log\det D_\ell. \tag{7}
\]

For fixed \(x\), Hadamard's determinant inequality and AM--GM give the
unique fiber minimizers

\[
 q_\gamma=d_\gamma={\rho_a\over h},\qquad
 \rho_a=1-\|x_a\|^2,\qquad \gamma\in\Gamma_a,             \tag{8}
\]

with every \(D_\ell\) diagonal. Substitution in either (4) or (7) proves
(1). This identity is exact and forgets the PSD packing layout.

## 2. The Newton systems are identical before final Schur elimination

The equality of marginal Hessians already proves the projected claim.
There is also a more informative identity at the bordered-system level.

For the Lorentz formulation put

\[
       u_\gamma=\delta x_\gamma,\qquad
       r_\gamma=\delta t_\gamma-2x_\gamma^Tu_\gamma.       \tag{9}
\]

At the fiber center (8), the barrier Hessian quadratic is

\[
 Q_{\rm Lor}(r,u)
   =\sum_\gamma {r_\gamma^2\over d_\gamma^2}
       +2\sum_\gamma{\|u_\gamma\|^2\over d_\gamma},        \tag{10}
\]

and the allocation tangent equations are

\[
 \sum_{\gamma\in\Gamma_a}
       (r_\gamma+2x_\gamma^Tu_\gamma)=0.                  \tag{11}
\]

For a PSD block direction \((A_\ell,U_\ell)=(\delta
S_\ell,\delta W_\ell)\), use the invertible direction congruence

\[
       B_\ell=A_\ell-W_\ell^TU_\ell-U_\ell^TW_\ell.        \tag{12}
\]

At diagonal \(D_\ell\),

\[
 d^2F_{\rm PSD}
 =\sum_\ell\left[
   \operatorname{tr}(D_\ell^{-1}B_\ell D_\ell^{-1}B_\ell)
       +2\operatorname{tr}(D_\ell^{-1}U_\ell^TU_\ell)
             \right].                                    \tag{13}
\]

Every off-diagonal entry of \(B_\ell\) is an independent positive
quadratic mode with zero objective and equality right-hand side. Remove
these modes and identify

\[
               r_\gamma=(B_{\ell(\gamma)})_{\gamma\gamma},
 \qquad u_\gamma=(U_{\ell(\gamma)})_\gamma.               \tag{14}
\]

Equations (13) and (6) become exactly (10) and (11). Sparse affine
constraints \(Ax=d\) add the same rows in the \(u\)-coordinates.
Barrier gradients and a common linear objective also give the same linear
term. Therefore the active residual-coordinate KKT systems agree entry for
entry.

More precisely, after a permutation of residual coordinates, the complete
centered PSD system has the direct-sum form

\[
 {\cal K}_{\rm PSD}^{\rm res}
    ={\cal K}_{\rm Lor}^{\rm res}\oplus D_{\rm off},
 \qquad
 b_{\rm PSD}^{\rm res}=(b_{\rm Lor}^{\rm res},0),          \tag{14a}
\]

where \(D_{\rm off}\) is positive diagonal, with one entry proportional to
\(2/(d_\gamma d_\delta)\) for every off-diagonal residual
\((B_\ell)_{\gamma\delta}\). Hence the normalized PSD solution in these
canonical residual coordinates is exactly the Lorentz solution padded by
zeros. For the direct, unscaled matrices,

\[
 \|{\cal K}_{\rm PSD}^{\rm res}\|
    \geq\|{\cal K}_{\rm Lor}^{\rm res}\|,\qquad
 \sigma_{\min}({\cal K}_{\rm PSD}^{\rm res})
    \leq\sigma_{\min}({\cal K}_{\rm Lor}^{\rm res}),       \tag{14b}
\]

so the extra PSD modes cannot improve the ordinary spectral condition
number. They can be dropped exactly because their right-hand side is zero.
This statement uses the residual coordinates (12); it is not a spectral
claim in the original \(\delta S\) coordinates, where the congruence need
not be orthogonal.

Eliminating \(r\) and the allocation multipliers gives the common marginal
Hessian

\[
 \nabla^2\bar F_h(x)
 =\bigoplus_{a=1}^b
   \left[
     {2h\over\rho_a}I_s+{4h\over\rho_a^2}x_ax_a^T
   \right].                                               \tag{15}
\]

With additional affine constraints, the common projected KKT matrix is

\[
 {\cal K}_h(x)=
 \begin{pmatrix}
    \nabla^2\bar F_h(x)&A^T\\
    A&0
 \end{pmatrix}.                                           \tag{16}
\]

The equality is algebraic, not merely spectral: the two formulations
produce the same matrix and Newton residual in the same canonical
coordinates.

## 3. Matched reduced-oracle model

The public data are \(b,s\), the group partition, the desired numerical
precision, and the choice of PSD packing. Hidden or changing data consist
only of the common projected instance and iterate:

\[
                         {\cal D}=(A,d,c,x,\eta,y).         \tag{17}
\]

Here \(c\) is the objective, \(\eta\) is the path multiplier, and \(y\)
denotes any current affine multiplier used in the Newton residual.

A **matched reduced interface** supplies the same requested-precision
access to \({\cal D}\) for both formulations and then one or more of:

- entry/sparse access to the common matrix (16);
- a state-preparation oracle for its common right-hand side;
- an \((\alpha,a,\delta)\) block encoding of (16); or
- the analogous oracles for the common residual-coordinate system
  (10)--(11).

Canonical coordinate labels are projected scalar variables, affine
multipliers, and, when retained, the pairs \((a,\gamma)\) for residual
coordinates. A query returns a scalar or quantum state record, not an
entire variable-size cone factor for unit cost.

“Same” here means the same complete oracle unitary, including its action
outside the advertised input or ancilla subspace. Equality only of a
top-left encoded block or only of one prepared state is insufficient:
arbitrary unitary completions can leak formulation-dependent information.
Equivalently, both sides may use one fixed public canonical compiler from
the common raw-data oracle. In an adversarial-completion formulation, the
algorithm must work for every valid completion and the reduction couples
the two sides using the same completion.

The output contract is an \(\epsilon\)-accurate normalized state of the
projected Newton solution (with affine multipliers optionally retained):

\[
        {(\delta x,\delta y)\over\|(\delta x,\delta y)\|},
 \quad\text{or}\quad {\delta x\over\|\delta x\|}.           \tag{18}
\]

It does not ask for every packed PSD auxiliary direction.

One may instead request the complete solution in the canonical residual
coordinates of (14a). The two outputs then differ only by a fixed public
zero-padding isometry, and the diagonal block \(D_{\rm off}\) is public
once the common residuals are queried. The same two-way simulation holds.
This extension still does not cover the original \(\delta S\)-coordinate
state, whose reconstruction uses Gram products.

This model includes the normalization and success data that affect a
quantum linear solver. It prevents an artificial comparison in which one
oracle call returns a whole packed PSD block containing \(c\) columns but
one call on the Lorentz side returns only one column. If blockwise
state-preparation is desired, the matched Lorentz oracle may bundle the
same \(c\) column records into one public superblock.

For example, in the unconstrained case a concrete common compiler follows
directly from (15). Put \(r_a=\|x_a\|\). Each block is

\[
 (\nabla^2\bar F_h)_a
   ={2h\over\rho_a}I+
      {4hr_a^2\over\rho_a^2}
       |\widehat x_a\rangle\langle\widehat x_a|.           \tag{18a}
\]

Given coherent blockwise preparation of
\(|\widehat x_a\rangle\) and reversible access to \(\rho_a\), a standard
controlled LCU/projector construction block-encodes (18a) using \(O(1)\)
calls to those data oracles per encoding call. When \(r_a=0\), the
projector coefficient is zero and its state may be any public default.
If the global maximum is supplied as normalization metadata (or has been
precomputed and charged), the construction can use the exact normalization

\[
 \alpha_H=\|\nabla^2\bar F_h\|
   =2h\max_a{1+r_a^2\over\rho_a^2},                       \tag{18b}
\]

and the exact global condition number is

\[
 \kappa_H=
 {\displaystyle\max_a{1+r_a^2\over\rho_a^2}
  \over
  \displaystyle\min_a{1\over\rho_a}}.                    \tag{18c}
\]

A standard inverse-state routine therefore has the conditional query
ledger

\[
       \widetilde O\!\left(
          \kappa_H\log(1/\epsilon_{\rm lin})\right),       \tag{18d}
\]

apart from right-hand-side preparation and the usual output-state success
factor. Without that metadata, any common certified upper bound can replace
\(\alpha_H\); finding a tighter bound is a common data-access cost. A
blockwise scalar preconditioner can replace \(\kappa_H\) by
\(\max_a(1+r_a^2)/\rho_a\), but applying and undoing that scaling, including
its success amplitude, must also be charged. Neither \(H\), the PSD packing
arity, nor the number of cone factors enters a single encoding call. If
block norms are not available coherently, both formulations must pay the
same norm-estimation or data-maintenance cost.

## 4. Proof of oracle equivalence

At a common data record (17), Sections 1--3 show that the complete
canonical oracle unitaries are identical bit for bit after the public
coordinate identification. A
query made by a PSD algorithm can therefore be forwarded to the Lorentz
oracle without modification, and conversely. All inter-query unitaries,
measurements, adaptivity, and stopping rules remain unchanged. The final
state (18) is the same vector in the same Hilbert space. This gives

\[
 \mathsf{Q}_{\rm PSD}(\epsilon)
 \leq\mathsf{Q}_{\rm Lor}(\epsilon)
 \quad\text{and}\quad
 \mathsf{Q}_{\rm Lor}(\epsilon)
 \leq\mathsf{Q}_{\rm PSD}(\epsilon),
\]

which proves (2).

Because (16) is the same matrix, every intrinsic linear-solver quantity is
also the same:

\[
 \dim{\cal K},\quad \|{\cal K}\|,\quad
 \sigma_{\min}({\cal K}),\quad \kappa({\cal K}),\quad
 \|b_{\rm Newt}\|,\quad
 {\|{\cal K}^{-1}b_{\rm Newt}\|\over\|b_{\rm Newt}\|}.     \tag{19}
\]

In particular, a block-encoding algorithm with a bound of the schematic
form

\[
 \widetilde O\!\left(
    \alpha\,\|{\cal K}^{-1}\|
       \log(1/\epsilon_{\rm lin})\right)                   \tag{20}
\]

has the same normalization, conditioning, precision, and success factors
on both sides when fed the matched encoding. When
\(\alpha=\|{\cal K}\|\), the spectral factor in (20) is \(\kappa\).
An implementation may choose a worse encoding for one formulation, but
that is not an intrinsic advantage of packing.

For an adaptive fiber-oblivious QIPM, argue inductively. The initial
projected record is common. If all prior query answers and measurements
agree, the algorithm selects the same next projected iterate and multiplier;
the next reduced oracles again agree by (15)--(16). Thus the complete
oracle transcript, number of Newton calls, and projected output-state law
are identical.

The identical canonical compiler described after (18) also gives the same
gate count and workspace. Conversely, any formulation-specific compiler
can be used unchanged by the simulation wrapper because its only
task-relevant output is the same complete oracle unitary. Thus charging
the compiler does not break the equivalence unless it is allowed to access
additional ambient formulation data, which is the different model in
Section 6.

## 5. Consequences for packing and cap choices

For fixed group width \(p\), \(h=\lceil s/p\rceil\). The PSD packing
arity \(c\), number of PSD blocks, and cross-source layout do not occur in
(1), (15), or (16). Hence

\[
 \boxed{
 \mathsf{Q}_{\rm packed\ PSD}(p,c)
  =\mathsf{Q}_{\rm unshared\ PSD}(p,1)
  =\mathsf{Q}_{\rm grouped\ Lorentz}(p)}
                                                               \tag{21}
\]

under the matched projected-state contract, for every admissible \(c\).
The equality covers a whole adaptive run, not only one isolated solve.

Under a PSD order cap \(R\), choosing \(c>1\) forces \(p\leq R-c<R-1\).
It therefore never lowers

\[
                 H_p=b\left\lceil{s\over p}\right\rceil.  \tag{22}
\]

The unshared choice \(c=1,p_*=\min\{s,R-1\}\) weakly minimizes the
standard barrier certificate within the column-packing family. Balanced
\(p\approx c\approx R/2\) can dramatically reduce factor count while
leaving each reduced oracle call equivalent to the grouped formulation
and weakly increasing \(H_p\).

For the unconstrained product body, this comparison is even sharper.
At a fixed projected point,

\[
               \nabla^2\bar F_h=h\nabla^2\bar F_1,        \tag{23}
\]

so a global change in \(h\) does not change the condition number or the
normalized inverse state for an arbitrary fixed right-hand side. Along a
linear-objective central path, replacing \(\eta\) by
\(\zeta=\eta/h\) gives the same projected point for every \(h\). Thus
larger \(h\) changes the path metric and standard iteration certificate,
not the per-call normalized projected linear-system state at corresponding
scaled path points.

Combining (21)--(23), cross-source packing has no route to a reduced-state
QIPM advantage through factor count, block-encoding normalization,
conditioning, iteration count, or state dimension in this family. It may
still reduce ambient formulation storage or the number of cone-factor
labels, which are different resources.

## 6. What changes under other output or access contracts

The impossibility result deliberately stops at the boundary of its model.

1. **Full lifted state.** Reconstructing a packed PSD direction requires
   \[
        (\delta S_\ell)_{\rm off}
          =(W_\ell^T\delta W_\ell+\delta W_\ell^TW_\ell)_{\rm off}.
   \]
   The Lorentz lift has no analogous Gram output. These are different
   target states, so (2) does not compare them.
2. **Explicit classical output.** Both formulations need
   \(\Omega(bs)\) writes for all projected coordinates. Explicit packed
   PSD auxiliaries additionally require Gram entries. No state-only
   conclusion removes these costs.
3. **Raw ambient cone oracle.** An oracle for entries or state preparation
   of \(Z_\ell\) is not the oracle in Section 3. Its compilation from raw
   \(x\) may require inner products, normalization data, or a factored
   representation. A separate access theorem is needed.
4. **Free factor-bundled access.** Counting a variable-size factor as one
   query regardless of its information content can favor packing by
   definition. Bundling the same records on the Lorentz side removes that
   artifact.
5. **Off-center lifted iterates.** The identity uses exact fiber centers.
   Arbitrary ambient iterates can have nondiagonal \(D_\ell\), and their
   Newton systems need not agree. The companion
   [off-center quotient theorem](2026-09-04-off-center-psd-packing-schur-obstruction.md)
   derives their exact projected Hessian, gives a squared
   relative-eccentricity transfer, and exhibits an unbounded two-ball
   obstruction. A fiber-centered algorithm can recenter explicitly or
   work with (1). The companion [implicit recentering and access
   theorem](2026-09-04-implicit-psd-fiber-recentering-access.md) gives the
   exact linear-work and finite-precision compiler, and shows why its
   radial scale oracle is necessary rather than free.

The result therefore does not rule out a benefit for a carefully specified
ambient-state task. It says that such a benefit cannot be inferred from
fewer cone blocks once the actual reduced Newton operator and output are
matched.

## 7. Literature and novelty boundary

Quantum IPMs based on quantum linear-system subroutines explicitly depend
on Newton-system dimensions, conditioning, precision, access, and output
requirements; representative primary sources include Augustino et al.,
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://arxiv.org/abs/2112.06025), Kerenidis and Prakash,
[*A Quantum Interior Point Method for LPs and
SDPs*](https://arxiv.org/abs/1808.09266), and Kerenidis, Prakash, and
Szilágyi,
[*Quantum algorithms for Second-Order Cone Programming and Support Vector
Machines*](https://arxiv.org/abs/1908.06720).

A targeted search did not find the exact PSD--Lorentz marginal identity,
the residual-KKT equivalence, or the two-way matched-oracle impossibility
theorem (2). Novelty is plausible subject to specialist review.

The theorem is specific to the explicit column-packed Schur lift and exact
fiber centering. It is not a black-box equivalence of PSD and Lorentz cones,
and it makes no claim about arbitrary SDP or SOCP formulations.
