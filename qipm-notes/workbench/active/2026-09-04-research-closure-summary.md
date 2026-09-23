# Research closure summary: sparse QIPM and conic-IPM frontier

Status: Closed research cycle
Closed: 2026-09-04
Paper status: Not incorporated
Priority status: Targeted literature screening found no direct collisions for
the candidate syntheses below, but this is not an exhaustive novelty opinion

## What is complete

This note closes the active research cycle.  The proof threads developed at
the end of the cycle are either proved and audited, explicitly scoped as
candidate syntheses after a targeted literature screen, or listed below as
open problems.  There is no remaining proof step silently assumed by a
headline theorem.

### 1. Sparse box LP: primal geometry does not capture dual completion

The [primal--dual completion
theorem](2026-09-04-sparse-box-primal-dual-completion-tax.md) gives one
two-sparse-row box LP family for which:

- the shortest arbitrary feasible primal path from the analytic center to
  an \(\epsilon\)-accurate point has length
  \(\Theta_R(r\sqrt{\log r})\);
- the shortest restricted primal central path has length
  \(\Theta_R(r\log r)\); and
- the minimum combined movement over strictly feasible primal--dual paths
  reaching duality gap at most \(2\epsilon\) is
  \(\Theta_R(r^{3/2})\): every such path pays the matching lower bound,
  while a central route supplies the upper bound.

For ordinary input length \(L=\Theta(r^2)\), these are respectively
\(\Theta(\sqrt{L\log L})\), \(\Theta(\sqrt L\log L)\), and
\(\Theta(L^{3/4})\), up to fixed-radius constants.  The last separation is
a dual-slack completion cost, not a primal centrality effect.  The theorem
was independently hostile-audited and literature-screened.  Its scope is
bounded local movement in the stated barriers, not unrestricted QIPM
runtime.

### 2. Exact-optimal coupled cube barriers still pay the centrality tax

The [hyperoctahedral barrier
family](2026-09-04-exact-optimal-hyperoctahedral-box-barrier-tax.md)
\[
 F_{\lambda,c}(x)
 =-\sum_i\log(1-x_i^2)-\lambda\log(c-\|x\|^2),
 \qquad \lambda\geq1,\quad c-r\geq4\lambda,
\]
is fully signed-permutation invariant, genuinely dense-coupled, and has
the exact cube-optimal parameter \(\nu=r\).  It nevertheless has the full
\(\Gamma_r=\Theta(\sqrt{\log r})\) same-endpoint central-path tax.  Taking
\(c=r+4\lambda\) makes the generic sum certificate \(r+\lambda\) overcount
the exact parameter by an arbitrarily large additive amount.

The [facet-regular stability
theorem](2026-09-04-facet-regular-coupling-box-centrality-tax.md) proves
that the same tax survives for every \(F=U+G\) whose convex coupling has
bounded gradient and Hessian on a full signed facet collar.  Within this
decomposition, escaping the proof requires singular coupling on every
relevant full collar.

The [dyadic discrete
companion](2026-09-04-exact-optimal-hyperoctahedral-box-discrete-tax.md)
uses \(O(r)\)-bit dyadic weights and tolerance.  From the analytic center,
every bounded-forward-Dikin sequence in a fixed metric tube, or in a fixed
Newton-decrement neighborhood below \(1/2\), needs
\(\Omega_{R,\Delta}(r\log r)\) chords even with arbitrary and backward
central labels.  A noncentral comparison path needs only
\(O_{R,\Delta}(r\sqrt{\log r})\) chords.  All three results passed
independent hostile audits.

### 3. Universal scalar-barrier and spectral-interval constants

The [sharp separable
theorem](2026-09-04-sharp-separable-centrality-tax.md) proves the
\(\Gamma_r\) endpoint tax, including a fully dyadic discrete form, for
every fixed normalized scalar one-self-concordant interval barrier.  Its
profile-uniform same-accuracy comparison is
\[
 L_{\rm CP}(\epsilon)
 \leq C_{\rm sc}\Gamma_r L_{\rm opt}(\epsilon),
 \qquad C_{\rm sc}<2,\qquad C_{\rm sc}\approx1.831856423.
\]
The constant is exact for the relaxed differential-envelope problem at the
profile-independent safe scale \(\log2\); it is not claimed globally sharp
for the fixed-smooth-profile minimax.

For the standard interval barrier, the [exact scalar dilation
theorem](2026-09-04-exact-scalar-centrality-dilation.md) gives
\[
 c_\star=\sup_{y>0}{p^{-1}(yp'(y))\over y},\qquad
 {68743\over50000}<c_\star<{69\over50},
\]
with \(c_\star\approx1.37486420044\).  The theorem and rational enclosure
were audited and mechanically checked.  These constants feed the
[Jordan spectral-interval
theorem](2026-09-04-jordan-spectral-interval-distance-centrality-tax.md).

### 4. Exact selection-free exposed rank for fixed all-simple-EJA dictionaries

The [all-simple-EJA
frontier](2026-09-04-selection-free-symmetric-cone-exposed-rank-frontier.md)
fixes a finite repeatable dictionary of simple symmetric cones and optional
rays, sets
\[
 B=\max_i a_i(r_i-1),\qquad
 q=\left\lceil{s-1\over B}\right\rceil,
\]
with \(B>0\), and proves:

- exact selection-free minimum support-certificate rank \(q\);
- the same value generically on a dense open, full-measure support set;
- a field-independent Peirce-perspective lift attaining the bound,
  including the Albert value \(B=16\);
- bounded-Dikin movement minimax
  \(\Theta_\theta(\sqrt q)\); and
- exact restricted standard-barrier value \(q\) off the divisible seam,
  with the divisible value in \([q,q+1]\) before the rigidity refinements
  below.

The [same-instance query/readout
theorem](2026-09-04-symmetric-cone-exposed-rank-query-readout-boundary.md)
adds, on one divisible balanced-sign family, exact rank \(q\), exact
support-minor scale \(\Delta=1\), one-query signed amplitude-state
preparation under a charged public-magnitude contract, and
\(\Theta_\epsilon(s-1)\) raw queries for full explicit classical output at
fixed \(0<\epsilon<1/8\).  It also proves
\[
 \inf_{\mathcal L}\sup_v r_{\mathcal L}(v)=q,
 \qquad
 \sup_v\inf_{\mathcal L}r_{\mathcal L}(v)=1.
\]
The Albert statement uses 27 real coordinates in an ordinary complex
amplitude state and assumes neither octonionic amplitudes nor free Albert
arithmetic.  Both notes passed independent hostile audits.  Movement and
readout yield a maximum of lower bounds, never their product.

### 5. Arbitrary-factor wide-cap rigidity

The [Lorentz wide-cap
theorem](2026-09-04-arbitrary-factor-q2-lorentz-barrier-rigidity.md)
proves that if
\[
 s-1=q(d-2),\qquad q\geq2,\qquad d-2\geq q-1,
\]
then every bounded full-Slater lift by an arbitrary finite product of
Lorentz cones of dimension at most \(d\) and rays has
\(\nu_{\rm std,slice}\geq q+1\).  The grouped norm chain attains equality.
Together with the recession theorem, this closes all affine wide-cap
Lorentz lifts, including every quotient-two case.

The [Hermitian wide-cap
theorem](2026-09-04-arbitrary-factor-wide-cap-hermitian-barrier-rigidity.md)
proves the analogue over real, complex, and quaternionic PSD cones:
\[
 s-1=qB,\qquad B=a(R-1)\geq q-1
 \quad\Longrightarrow\quad
 \nu_{\rm std,slice}=q+1.
\]
It allows arbitrarily many factors of order at most \(R\) and arbitrary
rays.  Both proofs use a factor-count-independent face-codimension budget,
singleton compact boundary fibers, global active-label rigidity, and a
topological contradiction.  Both passed independent hostile audits; the
final review clarified that the proof uses actual two-sided feasible
directions, not the lineality of the ordinary tangent cone.

## Deliberately open problems

These are genuine boundaries, not unfinished proofs of the statements
above:

1. **Narrow-cap divisible Lorentz lifts.**  For
   \(s-1=q(d-2)\), the bounded cases \(d-2\leq q-2\) remain unresolved.
2. **Narrow-cap divisible Hermitian lifts.**  For \(s-1=qB\), the bounded
   projection-singular cases \(q\geq B+2\) remain unresolved.  The analogous
   all-EJA divisible standard-barrier frontier can still lie in
   \([q,q+1]\) outside the settled one-channel and wide-cap regimes.
3. **Arbitrary optimal cube barriers.**  The \(\Gamma_r\) tax is proved for
   scalar products and facet-regular convex couplings, not for every
   optimal, coupled, or hyperoctahedrally symmetric cube barrier.
4. **Globally sharp scalar comparison.**  \(C_{\rm sc}\) is sharp for the
   relaxed envelope, not yet for the fixed smooth scalar-barrier minimax.
   Uniqueness of the maximizer defining \(c_\star\) is also not needed and
   remains open.
5. **Unrestricted quantum complexity.**  None of the geometric movement
   theorems alone is an unrestricted QIPM query or runtime lower bound.
   A valid composition must charge formulation compilation, oracle access,
   state preparation, conditioning, success probability, and output, and
   may combine simultaneous lower bounds only when the model justifies it.

## Literature and audit boundary

The [targeted literature
ledger](2026-09-04-targeted-literature-screen-sparse-conic-qipm.md)
records the closest located primary sources and the conservative novelty
labels.  The strongest claims above are described as candidate syntheses
when their ingredients are classical but their exact conjunction was not
located.  Absence from that targeted screen does not establish priority.

The full derivation history and supersession chain remain in the
[frontier ledger](2026-09-04-sparse-qipm-frontier.md).  Intermediate
counterexamples and failed conjectures are retained there to prevent
accidental reuse.
