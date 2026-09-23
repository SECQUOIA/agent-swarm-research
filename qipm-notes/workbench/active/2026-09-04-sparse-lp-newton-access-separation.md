# A sparse LP Newton-step separation between matrix and factor access

Status: Proved; independently audited; targeted literature screen completed  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the construction; moderate on apparent novelty

## Result

There is a three-variable, two-equality LP at an exact central point whose
Newton normal matrix has condition number \(\kappa\), for which constant-error
Newton-state preparation needs \(\Omega(\kappa)\) canonical queries when the
normal matrix is the primitive oracle, but \(\widetilde\Theta(\sqrt\kappa)\)
queries when its rectangular constraint factor is the primitive oracle.  The
same family transfers the complete normalized-shift hierarchy to a genuine LP
normal matrix.  The conclusion is intentionally access-model specific: a
digital sparse-entry oracle reveals the hidden scalar immediately.

Fix \(\rho>1\), a sufficiently small public \(\Delta>0\), and
\(t\in[\Delta,\rho\Delta]\).  Put

\[
 u_\pm=\frac{(1,\pm1)}{\sqrt2},\qquad
 q_+=\frac{(1,1,2)}{\sqrt6},
\]

\[
 v_0=\frac{(1,-1,0)}{\sqrt2},\qquad
 k=\frac{(1,1,-1)}{\sqrt3},
\]

and define

\[
 q_-=(\cos\theta)v_0+(\sin\theta)k,qquad
 \sin\theta=2\sqrt{2\Delta}.
\]

The pairs \(q_+,q_-\) and \(u_+,u_-\) are orthonormal, while

\[
 \langle q_-,\mathbf1\rangle
 =2\sqrt{2/3}\sqrt\Delta.
\]

Let

\[
 A_t=u_+q_+^T+\sqrt t\,u_-q_-^T.                            \tag{1}
\]

Then

\[
 A_tA_t^T=P_++tP_-=:H_t,qquad \kappa(H_t)=1/t,              \tag{2}
\]

where \(P_\pm=u_\pm u_\pm^T\).  For small enough \(\rho\Delta\),
all entries of \(A_t\) are bounded constants; its row and column degrees are
three and two.

Consider the LP

\[
 \min\ \mathbf1^Tx
 \quad\text{subject to}\quad
 A_tx=A_t\mathbf1,\qquad x\geq0.                            \tag{3}
\]

The point

\[
 x=s=\mathbf1,\qquad y=0
\]

is exactly on its primal--dual logarithmic central path at \(\mu=1\).
The feasible affine space is a line.  Its intersection with the orthant is a
nontrivial compact segment: a nonzero vector in \(\ker A_t\) is orthogonal to
the strictly positive vector \(q_+\), and therefore has both signs.  The
objective is nonconstant because \(\mathbf1\notin\operatorname{row}(A_t)\)
when \(\cos\theta\ne0\).  Thus this is not a zero-objective or unbounded
central-point gadget.

## Tight Newton-state access separation

At the center, the affine-scaling normal equation is

\[
 H_t\Delta y=A_t\mathbf1
 =a\left(u_++\sqrt{\Delta t}\,u_-\right),qquad
 a=2\sqrt{2/3},                                               \tag{4}
\]

Concretely, this is the usual predictor system
\(A_t\Delta x=0\),
\(A_t^T\Delta y+\Delta s=0\), and
\(\Delta x+\Delta s=-\mathbf1\), up to the immaterial simultaneous sign
convention for the direction.

and hence

\[
 \Delta y=a\left(u_++\sqrt{\Delta/t}\,u_-\right).           \tag{5}
\]

The normalized Newton states for the endpoint subfamily \(t=\Delta\) and
\(t=\rho\Delta\) have trace distance

\[
 d_{\rm tr}=\frac{\sqrt\rho-1}{\sqrt{2(\rho+1)}}.            \tag{6}
\]

Canonical rotation block encodings of \(H_t\) differ in operator norm by
\(O_\rho(\Delta)\).  Canonical state-preparation oracles for the normalized
right sides in (4) also differ by \(O_\rho(\Delta)\), because their hidden
coefficient is \(\sqrt{\Delta t}=\Theta(\Delta)\).  The standard hybrid
argument and (6) therefore give

\[
 Q_{H}=\Omega_\rho(1/\Delta)=\Omega_\rho(\kappa(H_t))         \tag{7}
\]

for constant-error preparation of this actual central Newton direction.

With canonical factor access to \(A_t\), the two endpoint oracles differ by
\(\Theta_\rho(\sqrt\Delta)\), so the corresponding hybrid lower bound is
\(\Omega(1/\sqrt\Delta)\).  It is matched, up to logarithms, by applying a
rectangular QLSA to

\[
 \Delta y=(A_t^T)^+\mathbf1,
\]

whose singular-value condition number is \(1/\sqrt t\).  Standard QLSA upper
bounds and the matching two-hypothesis hybrid lower bounds consequently give
the tight oracle separation

\[
 \boxed{Q_H=\Theta(\kappa),\qquad
 Q_A=\widetilde\Theta(\sqrt\kappa)}                           \tag{8}
\]

for constant-error Newton-state output in the two canonical analog oracle
models.

## Transfer of the normalized-shift hierarchy

Suppose a reusable compiler is given the same canonical completion family of
unit-normalized plain-\(H_t\) oracles for every
\(t\in[\Delta,\rho\Delta]\), and must produce a unit-normalized block
encoding of \(I-H_t\) with operator error at most \(K\Delta\).  Restriction
to the \(u_-\) eigenspace is exactly the scalar interval-shift problem
\(t\mapsto1-t\).  Therefore, for
\(K<G_r(\rho)\),

\[
 Q_{\rm compiler}
 =\Omega_{r,\rho,K}
 \left(\Delta^{-(2r+1)/(2r+2)}\right),                       \tag{9}
\]

and error \(o(\Delta)\) forces

\[
 Q_{\rm compiler}=\Omega_{\rho,\varepsilon}
 (\Delta^{-1+\varepsilon})
\]

for every fixed \(\varepsilon>0\).

The growing-accuracy theorem in the companion joint-law note sharpens this
to an exact operational bound.  Let \(\epsilon\) denote the requested
absolute compiler error.  For every fixed \(\beta>0\), uniformly when
\(0<\epsilon\leq\Delta^{1+\beta}\),

\[
 \boxed{
 Q_{H,\rm compiler}(\Delta,\epsilon)
 =\Theta_{\rho,\beta}\!\left(
 \frac1\Delta\log\frac1\epsilon\right)
 =\Theta_{\rho,\beta}\!\left(
 \kappa\log\frac1\epsilon\right).}                         \tag{10}
\]

The lower bound still permits an arbitrary coherent converter and uses only
the continuum \(t\in[\Delta,\rho\Delta]\).  The matching upper bound is a
unit-bounded integrated-sign polynomial, implemented by generalized QSP.
By contrast, factor access implements \(I-A_tA_t^T\) exactly with the
degree-two polynomial \(1-s^2\).  Thus this exact-central sparse LP exhibits
a \(\Theta(\kappa\log(1/\epsilon))\)-versus-\(O(1)\) complement-compilation
separation between normal-matrix and factor access, in addition to the
\(\Theta(\kappa)\)-versus-\(\widetilde\Theta(\sqrt\kappa)\) Newton-state
separation in (8).

## What the theorem does not say

The separation is useful precisely because it isolates an access-model
choice that is often hidden in QIPM complexity statements.

- The primitive input for (7) is only the canonical analog \(H_t\) oracle
  together with the canonical normalized preparation oracle for (4).  Giving
  exact-value access to the full LP instance, including \(A_t\) or \(b_t\),
  changes the problem.

- Factor access bypasses normalized shifting: degree-two singular-value
  transformation with \(p(s)=1-s^2\) implements \(I-A_tA_t^T\) exactly.
- A normalization-two LCU block encoding of \(I-H_t\) also costs one query;
  a Newton solver need not request the unit-normalized reusable object in
  (9).
- A digital exact sparse-value query to (1) exposes \(\sqrt t\) in a known
  entry, so neither analog-oracle hybrid lower bound is an intrinsic
  sparse-input lower bound.

Thus (7)--(10) should be advertised as a sharp normal-matrix-versus-factor
access theorem on a genuine sparse LP Newton system, not as an unconditional
end-to-end sparse-QIPM lower bound.

Factor-assisted improvements for positive-definite quantum linear systems are
known; in particular,
[Orsucci--Dunjko](https://quantum-journal.org/papers/q-2021-11-08-573/)
study decompositions \(H=LL^\dagger\) that can reduce the condition-number
dependence.  Generic \(\Omega(\kappa)\) QLS lower bounds for direct matrix
access are also standard.  A targeted search found no prior theorem combining
the explicit exact-central sparse LP family, the tight
\(\kappa\)-versus-\(\sqrt\kappa\) canonical-oracle separation, and the full
normalized-shift staircase and joint-accuracy transfers.  That conjunction—not factor
preconditioning by itself—is the defensible apparent novelty.
