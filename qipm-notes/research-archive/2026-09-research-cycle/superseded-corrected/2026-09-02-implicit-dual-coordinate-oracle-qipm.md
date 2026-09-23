# Implicit dual-coordinate oracles for sparse QIPMs

Date: 2026-09-02

## Summary

The state-to-diagonal lower bound does not apply when the changing diagonal is
an affine function of a smaller explicit iterate.  For the dual logarithmic
barrier method, store only the dual vector \(y\in\mathbb R^m\) and compute

\[
  s_i(y)=c_i-a_i^Ty
\]

coherently from the static \(i\)-th column \(a_i\) of \(A\in\mathbb R^{m\times
n}\).  If the columns are sparse, a slack query, a reciprocal-slack block
encoding, and hence a block encoding of the changing normal matrix can all be
implemented without materializing or refreshing an \(n\)-vector.

This gives a trajectory-level representation theorem: after tomography of the
\(m\)-dimensional dual Newton direction, updating the representation costs
\(O(m)\) words rather than \(O(n)\) words, and every later diagonal query is
computed from the updated \(y\).  It is a stronger access model than an
amplitude state, but the extra information is produced naturally by the
dual-only algorithm.  It does not hide block-encoding normalization,
right-hand-side preparation, tomography, or conditioning.

The closest published comparator is Wu et al.'s quantum dual logarithmic
barrier method.  That analysis reports \(O(mn)\) classical arithmetic per
iteration and assumes QRAM for changing normal systems.  The result below is a
representation/oracle refinement: keep the block encoding of \(A\) static,
compute the changing slack factors on the fly, and never explicitly form
\(s\), \(\Delta s\), or \(AS^{-2}A^T\).

## 1. Model

Consider the primal--dual pair

\[
 \min\{c^Tx:Ax=b,\ x\geq0\},\qquad
 \max\{b^Ty:A^Ty+s=c,\ s\geq0\},
\]

where \(A\in\mathbb R^{m\times n}\).  Write \(a_i\) for column \(i\).
Assume:

1. a static coherent sparse-column oracle returns the at most \(d_c\) nonzero
   positions and \(B\)-bit values of \(a_i\), and a value oracle returns \(c_i\);
2. a static \((\alpha_A,a_A,\epsilon_A)\)-block encoding of \(A\) is available
   at cost \(C_A\) per use; its one-time construction cost \(C_{\rm build}(A)\)
   is charged separately;
3. the current \(B\)-bit dual vector \(y_t\) is stored in coherent read-only
   memory, whose construction or refresh costs \(C_y=\widetilde O(mB)\);
4. known safety bounds satisfy
   \(0<\underline s_t\leq s_i(y_t)\leq\overline s_t\) for every \(i\).

The static block encoding in item 2 can come from sparse access, a concise
input circuit, or a data structure.  Its normalization and build cost are
parameters, not free QRAM assumptions.

Concretely, coherent access to the explicit dual iterate means a reversible
oracle

\[
 O_{y,t}:|j,z\rangle\longmapsto |j,z\mathbin\oplus (y_t)_j\rangle.
\]

We denote its query cost by \(C_{y,\mathrm{read}}\).  With a coherent-RAM data
structure, a read may have polylogarithmic depth, but loading or changing all
\(m\) words still costs \(\Omega(mB)\) work; this note charges
\(\widetilde O(mB)\) at every iterate update.  Without coherent RAM, a
multiplexed reversible circuit can implement the same oracle, but its gate
count can be \(\Theta(mB)\) per read.  In that realization one must substitute
that larger value for \(C_{y,\mathrm{read}}\) in every slack-oracle call.  The
theorem therefore removes an \(n\)-coordinate refresh, not the cost of coherent
access to the retained \(m\)-vector.

## 2. Affine-image diagonal oracle

### Theorem 1 (implicit slack and reciprocal diagonal)

Under the model above, there is a coherent value oracle

\[
 O_{s,t}:|i,0\rangle\longmapsto |i,\widetilde s_i(y_t)\rangle
\]

with absolute error \(\eta_s\), using \(d_c\) sparse-column accesses and

\[
 \widetilde O\!\left(d_c B+d_c C_{y,\mathrm{read}}
              +\log(1/\eta_s)\right)
\]

gates.  Reversible reciprocal evaluation and a controlled rotation give a
block encoding of

\[
 D_t=\underline s_t S_t^{-1}
     =\operatorname{Diag}\!\left(\frac{\underline s_t}{s_i(y_t)}\right)
\]

with normalization one.  Equivalently it is a block encoding of (S_t^{-1})
with normalization \(1/\underline s_t\).  Its operator error is

\[
 O\!\left(\frac{\eta_s}{\underline s_t}
          +\epsilon_{\rm arith}\right).
\]

#### Proof

Query the support and values of \(a_i\), query the corresponding entries of
\(y_t\), and reversibly accumulate \(c_i-a_i^Ty_t\).  The safety interval lets
one approximate \(z\mapsto\underline s_t/z\) uniformly and rotate an ancilla
with that amplitude.  Uncomputing the arithmetic gives the projected block
encoding.  The reciprocal is \(1/\underline s_t^2\)-Lipschitz on the safety
interval; after multiplying by \(\underline s_t\), an absolute slack error
\(\eta_s\) contributes \(O(\eta_s/\underline s_t)\) to the encoded operator.
There is no query to a state-preparation oracle for \(s\), so the
state-to-diagonal normalization--query lower bound is inapplicable.

### Corollary 2 (normal-matrix block encoding without diagonal refresh)

Let \(B_t=AS_t^{-1}\) and \(H_t=AS_t^{-2}A^T=B_tB_t^T\).  Standard products of
block encodings give normalizations

\[
 \alpha_{B,t}=\frac{\alpha_A}{\underline s_t},\qquad
 \alpha_{H,t}=\frac{\alpha_A^2}{\underline s_t^2}.
\]

Each use costs \(O(C_A+C_{s,t})\), up to logarithmic product overhead, where
\(C_{s,t}\) is the gate cost in Theorem 1.  Updating \(y_t\) changes the
diagonal oracle but does not rebuild the static encoding of \(A\).

The effective QLS parameter is not merely the spectral condition number:

\[
  \mathcal K_t:=\alpha_{H,t}\|H_t^{-1}\|.
\]

Any complexity statement must retain \(\mathcal K_t\), the block-encoding
errors, and the cost of (O_{s,t}).

## 3. Exact composition across dual-barrier iterations

The dual logarithmic-barrier Newton equations are

\[
 H_t\Delta y_t=\frac1{\mu_t}
       \left(b-\mu_t AS_t^{-1}e\right),
 \qquad
 \Delta s_t=-A^T\Delta y_t.
\]

The apparent dense slack update need never be performed.  If the tomography
output is the explicit \(m\)-vector \(\widetilde{\Delta y}_t\), set

\[
  y_{t+1}=y_t+\lambda_t\widetilde{\Delta y}_t.
\]

Then, identically,

\[
 c_i-a_i^Ty_{t+1}
 =s_i(y_t)-\lambda_t a_i^T\widetilde{\Delta y}_t.
\]

Thus the next slack oracle already contains the complete accumulated update.
There is no history-length factor and no checkpoint error.

The minimum-residual primal point used in the dual-barrier analysis also has
an implicit coordinate formula.  Since

\[
 x(s,\mu)=\arg\min_{Ax=b}\|\mu e-Sx\|_2,
\]

the Newton equation gives

\[
 x_i(s_t,\mu_t)
 =\frac{\mu_t}{s_i(y_t)}
  +\frac{\mu_t}{s_i(y_t)^2}a_i^T\Delta y_t.
\]

Once \(y_t\) and the latest \(m\)-dimensional direction are explicit, this is
another \(O(d_c)\)-access coordinate oracle.  An explicit \(n\)-vector output
still costs \(\Omega(n)\); the compressed output contract is the explicit dual
vector plus a primal coordinate oracle, selected observables, or a later
sparse-basis crossover.

### Theorem 3 (trajectory cost ledger)

Suppose iteration \(t\) prepares the Newton-direction state using a QLS
routine with

\[
 Q_{\rm solve,t}
 =\widetilde O(\Gamma_t\mathcal K_t)
\]

uses of the normal-matrix oracle, where \(\Gamma_t\) includes right-hand-side
preparation, amplitude amplification, solution-norm recovery, and failure
amplification.  Assume controlled access to the direction-state preparation
unitary and its inverse, a fixed real phase convention, and a separately
charged estimate of \(\|\Delta y_t\|_2\).  Let \(\xi_t\) denote the requested
\(\ell_2\) error for the *normalized* direction state.  The pure-state
tomography theorem of
van Apeldoorn, Cornelissen, Gily\'en, and Nannicini, *Quantum tomography using
state-preparation unitaries* (SODA 2023, arXiv:2207.08800), gives an
\(\xi_t\)-\(\ell_2\) classical description of an \(m\)-dimensional normalized
state using

\[
 R_t=\widetilde O(m/\xi_t)
\]

controlled calls to the preparation unitary and its inverse, with polylogarithmic
dependence on \(m\), \(1/\xi_t\), and failure probability hidden.  The same
paper proves a matching \(\widetilde\Omega(m/\xi_t)\) query lower bound.  This
bound concerns the normalized state; norm recovery, conversion to absolute
direction error, and resolving the physically required sign are included in
\(\Gamma_t\), not in \(R_t\).  Copy-only tomography would instead have
quadratic precision dependence and cannot be substituted into the displayed
ledger.  Under this coherent-access contract, a \(T\)-iteration implicit-oracle
implementation has query count

\[
 Q_{\rm path}
 =\widetilde O\!\left(
   \sum_{t<T}\frac{m}{\xi_t}\Gamma_t\mathcal K_t
 \right)
\]

and gate ledger

\[
 G_{\rm path}
 =C_{\rm build}(A)+
 \widetilde O\!\left[
 \sum_{t<T}\left{
   \frac{m}{\xi_t}\Gamma_t\mathcal K_t(C_A+C_{s,t})+mB
 \right}\right].
\]

There is no \(nT\) iterate-refresh term.  The \(mB\) term refreshes coherent
access to the tomography output.  Errors in tomography are exactly the
inexact dual-direction errors analyzed by the outer method; the representation
introduces only the separately budgeted slack-arithmetic error.

#### Right-hand-side warning

The parameter \(\Gamma_t\) can be large.  Applying a block encoding of
\(B_t=AS_t^{-1}\) to \(|e\rangle/\sqrt n\) has raw success amplitude

\[
 \frac{\|AS_t^{-1}e\|}{\alpha_{B,t}\sqrt n}.
\]

Moreover \(b-\mu_tAS_t^{-1}e\) becomes small near a centered iterate.  A direct
LCU state preparation can therefore suffer cancellation proportional to

\[
 \Gamma_{r,t}
 =\frac{\|b\|+\mu_t\alpha_{B,t}\sqrt n}
        {\|b-\mu_tAS_t^{-1}e\|}.
\]

One may instead form the \(m\)-dimensional residual by quantum mean estimation,
but that cost must replace, not be omitted from, \(\Gamma_t\).  The implicit
diagonal representation removes refresh cost; it does not solve RHS
preparation or conditioning.

## 4. Classical comparator and favorable regime

A classical matrix-free application of \(H_tv\) through all \(n\) sparse
columns costs \(\Theta(nd_c)\) arithmetic in the unstructured column-oracle
model.  Textbook CG therefore costs

\[
 \widetilde O(nd_c\sqrt{\kappa_t})
\]

per Newton solve, before outer iterations.  Ignoring common arithmetic factors,
the QLS/tomography route can be favorable only if

\[
 \frac{m}{\xi_t}\Gamma_t\mathcal K_t
 =o(n\sqrt{\kappa_t}).
\]

When the block encoding is near norm-normalized,
\(\mathcal K_t=\Theta(\kappa_t)\), this requires approximately

\[
  \frac{m\Gamma_t\sqrt{\kappa_t}}{\xi_t}=o(n).
\]

This is a conditional tall/sparse regime, not an unconditional quantum
speedup.  Classical solvers can use the same implicit slack representation;
the possible quantum gain is in querying the sum over many columns, not in the
affine representation itself.

## 5. Sparse-support and checkpoint alternatives

### Exact sparse update lists

If an algorithm is separately given a coherent list of the \(k_t\) nonzero
entries of every update, a dynamic dictionary can maintain a coordinate-value
oracle in \(\widetilde O(k_t)\) update work and polylogarithmic query time.  A
diagonal block encoding then follows from value-to-amplitude rotations and
escapes the state lower bound.

This is not a generic Newton-direction result.  Even with column-sparse \(A\),

\[
 \Delta s_i=-a_i^T\Delta y
\]

is generically nonzero for all \(i\).  Recovering the heavy support from an
amplitude state reintroduces search/tomography costs, and dropping small
coordinates without a weighted cumulative-error certificate can violate
positivity or the central neighborhood.

### Lazy checkpoints

With genuine coordinate-update oracles, storing a materialized checkpoint and
replaying \(L\) recent updates gives the generic ledger

\[
  C(L)=\widetilde O\!\left(\frac{T}{L}n
             +L\sum_{t<T}P_t\right),
\]

where \(P_t\) is the number of current-coordinate queries at iteration \(t\).
This can beat \(nT\) for some parameters, but it does not help when the updates
are supplied only as normalized states.  For dual slacks, the affine closure
\(s=c-A^Ty\) is strictly better: it summarizes the whole history in \(y\) and
needs no checkpoints.

## 6. Status and novelty boundary

The affine-image oracle theorem and its trajectory ledger are rigorous.  They
give a concrete escape from state-to-diagonal lifting and remove the changing
\(n\)-diagonal QRAM refresh assumed in some QLS-based dual QIPMs.

The dual logarithmic-barrier method itself is established prior art, and Apers
and Gribling already compute tall-LP slacks on demand in a different
spectral-sampling IPM.  The candidate new contribution is narrower: an
on-the-fly sparse block-encoding and implicit-output implementation of the
QLS-based dual barrier, with \(O(m)\) rather than \(O(n)\) representation updates
and with the full normalization/RHS/tomography ledger above.  A publishable
end-to-end speedup still requires a problem family controlling
\(\Gamma_t,\mathcal K_t,\xi_t\) and a finite-precision convergence proof.
