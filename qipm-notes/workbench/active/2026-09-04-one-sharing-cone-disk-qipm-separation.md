# One sharing cone: easy quantum states, hard readout, and barrier-independent primal--dual movement

Status: Proved; independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High, conditional on the explicitly separated access and output
contracts below

## Main theorem

For every \(N\geq2\), one nonsymmetric cone
\[
 \mathcal H_{N,2}
 =\{(\tau,z_1,\ldots,z_N):\|z_i\|_2\leq\tau\text{ for all }i\}
                                                                    \tag{1}
\]
supports a sparse optimization family with all of the following properties
on the same formulation.

1. The objective and cone are public. Every hidden bit appears only in one
   disjoint two-sparse equality row. All row norms, singular values, column
   degrees, and squared-sampling probabilities are public.
2. For the explicit optimal barrier on (1), fixing \(\tau=1\) and eliminating
   the hidden equalities leaves a diagonal Newton system of condition at
   most four along the entire central path. Normalized projected optimizer,
   checkpoint central-point, and checkpoint predictor-Newton states use
   \(O(1)\) hidden-bit queries.
3. At constant additive accuracy, the optimum value and a finite-central-
   checkpoint scalar have exact query law
   \[
                    Q_2=\Theta(N),\qquad R_2=\Theta(N),               \tag{2}
   \]
   and a sufficiently accurate explicit projected solution also needs
   \(\Omega(N)\) quantum and randomized queries.
4. The ambient cone has exact intrinsic logarithmically homogeneous
   self-concordant barrier parameter
   \[
                    \nu_{\rm opt}(\mathcal H_{N,2})=N+1.              \tag{3}
   \]
   Therefore, for **every** ambient LHSC barrier, a product-metric
   bounded-Dikin method starting at an exact primal--dual central point of
   gap \(\Delta_0\) and ending at any strictly feasible primal--dual point
   of gap at most \(\epsilon\), where \(0<\epsilon<\Delta_0\), requires
   \[
       T\geq
       {\sqrt{(N+1)/2}\log(\Delta_0/\epsilon)
        \over m\log(1/(1-R))}                                        \tag{4}
   \]
   rounds if a round contains at most \(m\) chords of starting local norm
   at most \(R<1\).

The claims in items 2 and 3 use the displayed explicit barrier. Item 4 is
uniform over all ambient LHSC barriers, but does not assert that their
central or Newton states are easy. The simultaneous lower bounds combine
by a maximum, never by multiplication.

## 1. Public-objective, hidden-constraint instance

Let \(b\in\{0,1\}^N\), put \(\sigma_i=(-1)^{b_i}\), fix
\(\tau=1\), and impose
\[
                         y_i=\sigma_i x_i,\qquad i\in[N].              \tag{5}
\]
Use the entirely public objective
\[
  \operatorname*{minimize}\quad
  L(z)={1\over\sqrt{10}}\sum_{i=1}^N(x_i+3y_i).                       \tag{6}
\]
Thus every public two-coordinate objective block has norm one and the
global raw objective norm is \(\sqrt N\).

In the hidden orthonormal nullspace coordinate
\[
                 (x_i,y_i)={u_i\over\sqrt2}(1,\sigma_i),              \tag{7}
\]
the problem is
\[
 \min_{u\in[-1,1]^N}\sum_i\beta_i u_i,\qquad
 \beta_i=
 \begin{cases}
  2/\sqrt5,&b_i=0,\\
  -1/\sqrt5,&b_i=1.
 \end{cases}                                                         \tag{8}
\]
Writing \(w=|b|\), the unique optimum value is
\[
                  \operatorname{OPT}(b)
                    =-{2N\over\sqrt5}+{w\over\sqrt5}.                 \tag{9}
\]
An additive estimate with error below \(1/(2\sqrt5)\) determines \(w\)
exactly. Computing its parity proves (2); reading every equality sign gives
the matching upper bound.

The hidden equality matrix has disjoint rows
\((-\sigma_i,1)\). Hence
\[
                         EE^T=2I_N,                                  \tag{10}
\]
all row norms and singular values are \(\sqrt2\), every coordinate column
has degree one, and its ordinary squared-SQ sampling law is independent of
\(b\). An equality-row or equality-coefficient query costs one query to
\(b_i\); objective-coefficient queries are free because the objective is
public.
For coherent access, fix the canonical public preparation
\[
 {1\over\sqrt{2N}}\sum_i(-|i,x_i\rangle+|i,y_i\rangle)
\]
and phase only the \(x_i\) branch by \(\sigma_i\). This unitary and the
standard coherent bit oracle simulate one another with constant overhead.
Arbitrary hidden-dependent unitary completions are excluded.

Strict feasibility holds on both sides. The primal point
\(\tau=1,z_i=0\) satisfies (5) and lies in
\(\operatorname{int}\mathcal H_{N,2}\). To fix signs, use the dual
convention \(s=c-A^Tq\in\mathcal H_{N,2}^*\). Set the multipliers of
(5) to zero and the multiplier of \(\tau=1\) to \(-M\). The dual slack is
then
\[
 s=\left(M,{(1,3)\over\sqrt{10}},\ldots,
              {(1,3)\over\sqrt{10}}\right).
\]
The dual cone is
\(\mathcal H_{N,2}^*=\{(M,w_1,\ldots,w_N):
M\geq\sum_i\|w_i\|_2\}\), so any \(M>N\) is strictly dual feasible.

## 2. Explicit optimal barrier and finite checkpoint

An optimal ambient barrier is
\[
 F_{\mathcal H}(\tau,z)
 =-\sum_{i=1}^N\log(\tau^2-\|z_i\|_2^2)+(N-1)\log\tau.                \tag{11}
\]
It is the restriction of the classical spectral-norm-cone barrier. On the
fixed-scale slice \(\tau=1\), (11) becomes exactly
\[
                         \bar F(u)=-\sum_i\log(1-u_i^2),              \tag{12}
\]
whose affine-slice barrier parameter is \(N\).

At central multiplier \(\eta\), let
\[
 r(a)={a\over\sqrt{1+a^2}+1}.
\]
Equations (8) and (12) give
\[
 u_i(\eta)=
 \begin{cases}
  -r(2\eta/\sqrt5),&b_i=0,\\
  +r(\eta/\sqrt5),&b_i=1.
 \end{cases}                                                         \tag{13}
\]
Choose the public checkpoint \(\eta_0=2\sqrt5\). Then the two prototypes
are \(-r(4)\) and \(+r(2)\). The centered public-objective readout is
\[
\begin{aligned}
 S_b&:=L(z(\eta_0))+{2N\over\sqrt5}r(4)
       =w\Delta_{\rm cp},\\
 \Delta_{\rm cp}
   &={2r(4)-r(2)\over\sqrt5}
     ={\sqrt{17}-\sqrt5\over2\sqrt5}>0.                              \tag{14}
\end{aligned}
\]
Thus additive error below \(\Delta_{\rm cp}/2\) again determines \(w\)
and gives (2) at a finite, public central multiplier.

The scalar Hessian at the stationary point with effective force \(a\) is
\[
                  h(a)=\sqrt{1+a^2}\bigl(\sqrt{1+a^2}+1\bigr).        \tag{15}
\]
The equality-eliminated Newton Hessian is diagonal, and the ratio between
its two possible entries is \(h(4)/h(2)<4\). More generally the ratio is
at most four along the entire path because the two force magnitudes have
ratio two.

## 3. Easy projected states and hard classical output

At the checkpoint, the projected central vector has one of two public
amplitudes and signs in each coordinate:
\[
             u_i=-r(4)\quad(b_i=0),\qquad
             u_i=+r(2)\quad(b_i=1).                                  \tag{16}
\]
A uniform superposition over \(i\), one coherent query to \(b_i\), a
controlled rotation using the two public amplitudes, and postselection
prepare its normalized state. The success probability lies between two
positive constants independent of \(b,N\). Preparation is therefore
heralded-exact in \(O(1)\) expected queries and constant-error in \(O(1)\)
worst-case queries. Applying the one-query hidden basis change (7) gives
the normalized projected ambient \(z\)-state.

The central predictor direction satisfies
\[
                     d_i=-{\beta_i\over h(\eta|\beta_i|)}.            \tag{17}
\]
At \(\eta_0\), these are again two nonzero public magnitudes with a
bit-controlled sign. The same construction prepares the normalized
projected predictor-Newton state in \(O(1)\) queries. This claim is for
the central predictor right-hand side; it is not a state-preparation
theorem for arbitrary Newton right-hand sides.

At the optimum \(u_i^*=-\operatorname{sign}\beta_i\), so its normalized
projected state is exactly one-query preparable. In contrast, an explicit
feasible point with total objective gap below \(1/\sqrt5\) has the correct
sign in every coordinate and reveals every \(b_i\). The same conclusion
holds for a checkpoint vector given to sufficiently small constant total
\(\ell_2\) error, because the two prototypes in (16) are a fixed positive
distance apart. Parity then gives \(\Omega(N)\) input queries for either
explicit-output contract.

These state claims concern the equality-eliminated coordinates, or their
image (7). They do not provide a free classical description of the hidden
nullspace basis, a free exact norm of a hidden projected vector, or an
easy full primal--dual central state.

## 4. Arbitrary-barrier primal--dual movement

Restricting (1) to \(z_i=\xi_i e\) for one fixed unit vector
\(e\in\mathbb R^2\) gives the \((N+1)\)-dimensional
\(\ell_\infty\)-epigraph cone. Hildebrand's sharp lower bound therefore
gives \(\nu\geq N+1\) for every LHSC barrier on (1), while (11) attains
equality. This proves (3).

For completeness, let \(G\) be any \(\nu\)-LHSC barrier on (1), let
\(G_*\) be its conjugate, and use the product metric of
\(\widehat G=G+G_*\). If \(z(t)\) is the exact primal--dual central path,
then
\[
       \langle x(t),s(t)\rangle={\nu\over t},\qquad
       \widehat G(z(t))=\nu\log t-\nu,\qquad
       \|\widehat G'(z)\|_{z,*}=\sqrt{2\nu}.                           \tag{18}
\]
The central point \(z(\nu/\epsilon)\) minimizes \(\widehat G\) over the
strictly feasible primal--dual gap-\(\epsilon\) sublevel set. Integrating
the gradient inequality along any ambient-interior path gives distance at
least
\[
                    \sqrt{\nu/2}\log(\Delta_0/\epsilon).              \tag{19}
\]
A chord of starting product-Dikin norm at most \(R<1\) has length at most
\(\log(1/(1-R))\), so (4) follows from \(\nu\geq N+1\). Intermediate
chords may violate the affine equalities.

At the same public multiplier \(\eta_0=2\sqrt5\), an arbitrary barrier has
starting gap \(\Delta_0=\nu/\eta_0\). Hence, whenever
\(\epsilon<(N+1)/\eta_0\),
\[
 T\geq
 {\sqrt{(N+1)/2}\log\!\bigl((N+1)/(\eta_0\epsilon)\bigr)
  \over m\log(1/(1-R))}.
                                                                    \tag{20}
\]
The substitution is monotone on this range: for
\(a=\eta_0\epsilon\), the derivative of
\(\sqrt\nu\log(\nu/a)\) has the sign of
\(1+\tfrac12\log(\nu/a)>0\). As \(N/\epsilon\to\infty\), the right-hand
side of (20) is
\(\Omega_{R,m}(\sqrt N\log(N/\epsilon))\). This asymptotic form is not
claimed uniformly as \(\epsilon\) approaches the starting gap.
The starting central point in (20) is the one defined by the chosen
barrier. Only for the explicit barrier (11) are the easy projected-state
and diagonal-Newton claims of Sections 2--3 asserted.

## 5. Fixed-primal comparison and exact scope

For the explicit barrier (11), the fixed-scale restriction (12) also gives
a different, primal-only theorem. Starting at \(u=0\), objective gap at
most \(\epsilon\) forces
\[
 \prod_i(1-u_i^2)
 \leq\left({2\sqrt5\,\epsilon\over N}\right)^N,
\]
so every path in the fixed restricted metric has length at least
\[
                  \sqrt N\log{N\over2\sqrt5\,\epsilon}.               \tag{21}
\]
This reaches a primal accurate set but fixes the standard restricted
barrier. Equations (19)--(20) instead cover every ambient LHSC barrier but
use the primal--dual product metric, a central start, and a strictly
feasible primal--dual gap certificate. Neither statement implies the
other.

For fixed sufficiently small \(\epsilon\), this one formulation therefore
has the simultaneous ledger
\[
\begin{gathered}
 L=1,\qquad \dim\mathcal H_{N,2}=2N+1,\qquad
 \nu_{\rm ambient}^{\rm opt}=N+1,\qquad\nu_{\rm slice}=N,\\
 Q_{\rm projected\ state}=O(1),\qquad
 Q_{\rm scalar/full}=R_{\rm scalar/full}=\Theta(N),\\
 T_{\rm arbitrary\ LHSC,\ primal\text{-}dual}
   =\Omega_{R,m}(\sqrt N\log N).
\end{gathered}                                                       \tag{22}
\]
This means \(\max\{Q_{\rm readout},T_{\rm movement}\}\) under a model that
charges both resources. It never means their product.

The movement theorem is not an oracle-query or runtime lower bound. It
does not apply to unbounded local-norm jumps or to a quantum evolution not
represented by bounded product-Dikin chords. The query theorem does not
grant free norms of hidden projected data, arbitrary coherent-unitary
completions, a materialized hidden nullspace basis, or a compiled
central-iterate oracle. State, scalar, SQ, and full classical outputs are
distinct contracts.

## 6. Provenance and literature boundary

The hidden-equality query reduction and its approximate-counting extension
are proved in
[Product-disk central-readout query
hierarchy](2026-09-04-product-disk-central-readout-query-hierarchy.md).
The exact barrier (11) and \(\nu_{\rm opt}=N+1\) are proved in
[Bounded-face sharing sharp
models](2026-09-04-bounded-face-sharing-sharp-models.md).
The arbitrary-barrier product-metric theorem is extracted in
[Barrier-independent primal--dual bounded-Dikin lower
bounds](2026-09-04-barrier-independent-primal-dual-dikin-lower-bound.md).

The Nesterov--Todd primal--dual geometry is prior art and is not claimed as
new:

- Yu. E. Nesterov and M. J. Todd,
  [On the Riemannian Geometry Defined by Self-Concordant
  Barriers](https://doi.org/10.1007/s102080010032).
- R. Hildebrand,
  [A lower bound on the optimal self-concordance parameter of convex
  cones](https://optimization-online.org/2011/06/3068/).

The candidate contribution is the same-instance sparse-data synthesis and
its exact separation of factor count, ambient barrier choice, projected
state preparation, classical readout, and bounded primal--dual movement.
No open-literature source was found that states this combined result;
priority still requires specialist review.

## Independent hostile audit

The audit rederived the hidden orthonormal coordinate, objective signs,
exact Hamming-weight reduction, and both Slater points. It checked the
dual-cone convention above, the checkpoint separation constant, the
scalar Hessian formula and its factor-four condition bound, and the
constant-success state preparations for the checkpoint center, predictor,
and optimizer.

It also checked the arbitrary-LHSC product-metric argument against the
Nesterov--Todd gap and barrier-value identities, including the
\(\sqrt{\nu/2}\) distance constant and the strictly feasible endpoint-set
claim. Finally, it verified that the query, classical-output, and movement
statements are simultaneous maximum-type lower bounds; none are
multiplied.
