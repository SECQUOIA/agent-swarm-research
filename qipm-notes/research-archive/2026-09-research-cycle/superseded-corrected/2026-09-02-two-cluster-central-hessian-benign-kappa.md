# Two-cluster central-path Hessians: the benign side of the chord law

Date: 2026-09-02
Status: independently referee-audited twice, then corrected in-house
once more and literature-grounded (full history in the verification
record). Propositions 1 and 2 (the classical core) verified in full,
including adversarial numerics. The quantum corollary went through
three forms: the original polylog claim (refuted by the first audit),
a \(\sqrt\kappa\) tightness claim (verified as approximation
mathematics by the second audit but corrected in-house on
implementability), and the final Theorem Q below, grounded in
Orsucci--Dunjko and Somma--de Wolf. Companion and calibration to
2026-09-02-barrier-independent-conditioning-dichotomy.md; positive
counterpart: 2026-09-02-newton-rhs-spectral-alignment.md.

## Message (final form)

The chord law proves \(\kappa_{\rm red}=\Omega((D(g)/g)^2)\) for every
barrier. This note shows that the ill-conditioning of log-barrier
central-path Hessians on degenerate LPs is *structured* — the spectrum
lives in two intervals whose internal ratios are \(\mu\)-free instance
constants — and that structured ill-conditioning is benign for
**classical Krylov methods**: CG touches the spectrum only through
matvecs and never pays for off-spectrum behavior. The quantum half is
the surprise, and it sharpened twice under audit: implementable QSVT
polynomials must be bounded on all of \([-1,1]\), where the bottom
cluster sits at the *middle* — so with a plain block-encoding the
clustered solve still costs \(\widetilde\Theta(\kappa)\) (all
algorithms, by Orsucci--Dunjko, on hidden-structure instances), and
\(\widetilde\Theta(\sqrt\kappa)\) under factor access
(\(H=G^\dagger G\)), which is the natural model for IPM normal
equations. Clustering helps no quantum access model beyond what the
model already gives, while collapsing the classical cost to polylog —
a previously unwritten separation on the very systems QIPMs need. The
practical sting for path-following is limited, however: the on-path
Newton right-hand sides are spectrally aligned with the benign cluster
(see the companion RHS-alignment note).

## Proposition 1 (two-cluster structure)

Standard-form LP, compact \(P\), \(P^\circ\ne\emptyset\), log-barrier
central path with \(S=\sup_{0<\mu\le\bar\mu}\max_j s_j(\mu)<\infty\),
optimal-support partition \(B,N\) (Goldman--Tucker), and
\(\beta=\inf_{0<\mu\le\bar\mu}\min_{j\in B}x_j(\mu)>0\) (positive by
central-path convergence to the relative interior of the primal optimal
face). Let \(r=\operatorname{rank}(P_NZ)\) and let \(\sigma>0\) be the
smallest positive singular value of \(P_N Z\) (instance constants;
\(P_N\) the coordinate projection onto \(N\), \(Z\) an orthonormal basis
of \(\ker A\); also \(\inf_{0<\mu\le\bar\mu}\min_{i\in N}s_i(\mu)>0\) on
the tail by strict complementarity of the Goldman--Tucker limit, which
the "\(\mu\)-independent internal ratios" phrase uses). Then for \(0<\mu\le\bar\mu\) the spectrum of
\(H_\mu=Z^\top X(\mu)^{-2}Z\) satisfies: the top \(r\) eigenvalues lie in
\[
  \Big[\ \sigma^2\min_{i\in N}s_i(\mu)^2/\mu^2,\
  \ \max_{i\in N}s_i(\mu)^2/\mu^2+\beta^{-2}\ \Big],
\]
and the remaining \(\dim V-r\) eigenvalues lie in
\(\big[\,D_P^{-2},\ \beta^{-2}\,\big]\) (lower end by the chord-converse
argument of Theorem B: every unit \(h\in V\) has a boundary exit time at
most \(\operatorname{diam}P\)). Both intervals have \(\mu\)-independent
internal ratios; their separation grows as \(1/\mu^2\).

Proof: split \(H_\mu=A_\mu+B_\mu\) with
\(A_\mu=Z^\top P_NX_N^{-2}P_NZ\) (PSD, rank \(r\), nonzero eigenvalues in
\([\sigma^2\min s_i^2/\mu^2,\ \max s_i^2/\mu^2]\)) and
\(\|B_\mu\|\le\beta^{-2}\); apply Weyl's inequalities. \(\square\)

Consistency checks: at a nondegenerate vertex \(r=\dim V\) (if
\(h\in\ker A\) has \(h_N=0\) then \(A_Bh_B=0\) and the basis matrix is
nonsingular, so \(h=0\); hence \(P_NZ\) has full column rank), the bottom
cluster is empty, recovering \(\kappa=O(1)\); with \(\dim\Phi\ge1\) the
bottom cluster is nonempty, recovering the chord-law \(\Theta(1/\mu^2)\)
gap between clusters. Multi-scale generalizations cluster the same way
with more windows: the audit measured the singularity-degree-2 SDP
witness (\(\min X_{22}\), \(\operatorname{tr}X=1\), \(X_{33}=X_{12}\))
and found **four** windows with per-decade-exact exponents
\(\mu^{-1/2},\mu^{-1},\mu^{-3/2},\mu^{-2}\) and \(\mu\)-free prefactors
(no \(O(1)\) window — consistent with the unique optimum emptying the
bottom cluster), correcting an earlier "three scales" guess in a prior
draft of this note.

## Proposition 2 (structured ill-conditioning is Krylov-benign)

Let \(H\succ0\) have spectrum contained in
\([a_1,b_1]\cup[a_2,b_2]\) with \(\rho_i=b_i/a_i\) and
\(\Lambda=b_2/a_1\) (\(=\Theta(1/\mu^2)\) above). Then for every
\(\varepsilon\), there is a residual polynomial \(q\) with \(q(0)=1\),
\(|q|\le\varepsilon\) on the spectrum, of degree
\[
  m\ =\ O\!\big(\sqrt{\rho_1}\,\sqrt{\rho_2}\,
  \log(\Lambda)\log(1/\varepsilon)+\sqrt{\rho_2}\log(1/\varepsilon)\big)
  \ =\ O_{\rho}\!\big(\log(\Lambda/\varepsilon)\log(1/\varepsilon)\big),
\]
hence CG reaches relative \(H\)-norm error \(\varepsilon\) in that many
iterations — polylogarithmic in \(\kappa=\Lambda\) (note
\(\kappa=b_2/a_1=\Lambda\) exactly), not \(\sqrt\kappa\). (Degenerate
case \(b_1=a_1\): treat cluster 1 as the point \(\{a_1\}\); the
Chebyshev factor degenerates gracefully to \(1-x/a_1\).)

Construction (elementary, avoids two-interval potential theory): let
\(p_2\) be the degree-\(d_2=\lceil\sqrt{\rho_2}\rceil\) shifted-Chebyshev
residual for \([a_2,b_2]\), normalized \(p_2(0)=1\); then
\(|p_2|\le2e^{-2d_2/\sqrt{\rho_2}}\le1/2\) on \([a_2,b_2]\) and
\(|p_2|\le1\) on \([0,a_2]\) by monotonicity. Let \(r_1\) be the
degree-\(m_1=O(\sqrt{\rho_1}\log(1/\varepsilon))\) Chebyshev residual for
\([a_1,b_1]\); on \([a_2,b_2]\) it can grow, but at most like
\(|r_1|\le(4\Lambda)^{m_1}\). Take
\(q=r_1\cdot p_2^{\,j}\) with
\(j=\lceil m_1\log_2(4\Lambda)+\log_2(1/\varepsilon)\rceil\): on cluster
1, \(|q|\le\varepsilon\cdot1\); on cluster 2,
\(|q|\le(4\Lambda)^{m_1}2^{-j}\le\varepsilon\); \(q(0)=1\). Total degree
\(m_1+jd_2\) as claimed. CG optimality over polynomials of equal degree
finishes the argument. \(\square\)

Numerics (`notes/scripts/two_cluster_cg_check.py`; representative run,
\(n=40\) simplex-slice LP with a 2-coordinate inactive set, face
dimension 37): over \(\mu=10^{-2}\dots10^{-8}\), \(\kappa\) grows from
\(10^{1}\) to \(7\times10^{12}\) while the cluster count stays 2, the
intra-cluster ratios stay \(\le1.006\) (bottom) and converge to
\(4.004\) (top; \(2.44\) at \(\mu=10^{-2}\)), and CG solves random
right-hand sides to \(10^{-8}\) in 3--8 iterations (the drift from 3 to
8 at \(\mu=10^{-8}\) is float64 roundoff — 80-bit CG takes 6); the naive
\(\sqrt\kappa\) count at \(\mu=10^{-8}\) is \(\sim2.6\times10^{6}\)
iterations (audit-corrected figure).

## Theorem Q (gap-boundedness obstruction: QSVT cannot exploit clusters)

The original draft claimed Proposition 2's polynomial yields a
polylog-degree QSVT solve. The referee audit refuted this, and the truth
is a theorem in the opposite direction. Work in rescaled units
\(\|H\|=b_2=1\), spectrum \(\subseteq[1/\Lambda,\rho_1/\Lambda]\cup
[1/\rho_2,1]\), \(\Lambda=\kappa\)-scale.

1. **Admissibility.** A QSVT/QSP circuit implements only polynomials with
   \(|p|\le1\) on all of \([-1,1]\) — including the spectral gap and the
   near-zero segment, where no eigenvalue lives. Proposition 2's
   composite \(q\) attains \(\approx10^{85}\) inside the gap on the
   audit's test intervals: it is implementable by CG (which never
   evaluates it off the spectrum) but not by QSVT at any useful
   normalization.
2. **Markov no-go (audit's argument).** Any polynomial with \(q(0)=1\),
   \(|q(1/\Lambda)|\le\varepsilon\), and \(|q|\le M\) on \([0,1]\) has
   degree \(\ge\sqrt{(1-\varepsilon)\Lambda/(2M)}\): the unit drop over
   \([0,1/\Lambda]\) forces \(|q'|\ge(1-\varepsilon)\Lambda\) somewhere,
   while Markov caps \(|q'|\le2d^2M\). So a residual-style polynomial
   bounded on the interval pays \(\Omega(\sqrt{\Lambda/M})\): polylog
   degree forces subnormalization \(M=\widetilde\Omega(\Lambda)\).
3. **Bernstein branch no-go (cluster filtering does not escape).**
   Suppose one first filters the state to the bottom cluster (cheap: a
   step polynomial with \(\Theta(1)\) relative transition width at the
   inter-cluster threshold is bounded and of polylog degree) and then
   inverts there. In rescaled units \(y=\Lambda x\in[1,\rho_1]\), the
   inversion polynomial must satisfy \(|p|\le M\) on \([0,\Lambda]\) and
   approximate \(1/y\) on \([1,\rho_1]\) to relative accuracy
   \(\delta'\le1/8\), resolving the cluster's internal variation. For
   \(\rho_1\ge2\), \(p\) must then drop by at least
   \((1-\delta')-(1+\delta')/\rho_1\ge5/16\) across \([1,\rho_1]\), so
   \(|p'(\xi)|\ge5/(16\rho_1)\) for some \(\xi\in(1,\rho_1)\);
   Bernstein's inequality on \([0,\Lambda]\) caps
   \(|p'(\xi)|\le dM/\sqrt{\xi(\Lambda-\xi)}\le dM/\sqrt{\Lambda-\rho_1}\)
   (the product \(\xi(\Lambda-\xi)\) is minimized at the interval ends),
   giving, for \(\rho_1=o(\Lambda)\),
   \[
     d\cdot M\ \ge\ \frac{5\sqrt\Lambda}{32\,\rho_1}\,(1-o(1)):
   \]
   the degree--subnormalization product pays
   \(\Omega(\sqrt\kappa/\rho_1)\) even branch-wise (the argument applies
   to *any* single admissible polynomial relatively inverting the bottom
   cluster while bounded on \([0,\Lambda]\), composite
   filter\(\times\)inverter products included — audit's observation).
   The filter placement matters for the cheap half: the step transition
   must sit at the \(\Theta(1)\) end of the gap, where an absolute
   \(\Theta(1)\) transition width gives polylog degree; a step at the
   bottom-cluster scale would itself cost \(\widetilde\Theta(\Lambda/\rho_1)\).
   The one escape is a
   *scalar* bottom cluster (\(\rho_1\to1\) with only crude intra-cluster
   accuracy demanded): filter + multiply by a known constant is cheap —
   but Newton solves generically need constant relative accuracy across
   a bottom cluster of ratio \(\rho_1\ge2\)-type, where the obstruction
   binds.
4. **Implementability sharpens the no-go to \(\Theta(\kappa)\)
   (second-round self-audit correction).** Bounds 2--3 constrain
   polynomials bounded on \([0,\Lambda]\); item 1's admissibility is
   boundedness on \([-1,1]\), i.e. on \([-\Lambda,\Lambda]\) in
   \(y\)-units. For PSD \(H\) these classes differ decisively, because
   the bottom cluster sits near \(y=0\) — the **middle** of the
   admissible interval, where Bernstein gives no endpoint enhancement:
   any admissible \(p\) with \(|p|\le M\) on \([-\Lambda,\Lambda]\)
   separating \(y=1\) from \(y=2\)-type bottom-cluster structure needs
   \(|p'|\ge\Omega(1)\) at \(|y|=O(\rho_1)\ll\Lambda\), while
   \(|p'|\le dM/\Lambda\cdot\Lambda/\sqrt{\Lambda^2-y^2}\approx dM/\Lambda\)
   there, forcing
   \[
     d\cdot M\ =\ \Omega(\Lambda)\ =\ \Omega(\kappa).
   \]
   A Remez LP with the symmetric constraint confirms this exactly:
   minimal separating degree \(=(0.94\text{--}1.04)\cdot\Lambda\) across
   \(\Lambda=50\dots400\), versus \(1.7\sqrt\Lambda\) for the one-sided
   relaxation (`notes/scripts/qet_implementability_lp.py`). The earlier
   \(\sqrt\kappa\) claims of this note (a truncated-Laplace
   construction \((1-e^{-yT})/y\) and the one-sided tradeoff LP,
   `notes/scripts/qsvt_cluster_tradeoff_lp.py`) are correct *approximation*
   statements on \([0,\Lambda]\) but are **not QET-implementable**: the
   Laplace function explodes on \([-\Lambda,0)\), and its value
   \(T\neq0\) at \(y=0\) blocks the odd-extension trick that rescues
   Childs--Kothari--Somma's \(1/x\) (an odd target). Failed escapes,
   recorded: (a) parity/QSVT in \(u=\sigma^2\) has \(u=0\) as a genuine
   endpoint, but the quadratic map squeezes bottom-cluster features to
   scale \(1/\Lambda^2\), eating exactly the edge gain (degree
   \(\Theta(\Lambda)\) again); (b) the shift \(H\mapsto I-H\) moves the
   bottom cluster to the top **edge**, where \(1/\Lambda\)-features cost
   only \(\Theta(\sqrt\Lambda)\) — but constructing a
   *subnormalization-1* encoding of \(I-H\) from \(U_H\) is exactly a
   factor-2 uniform amplification whose faithful action within
   \(1/\Lambda\) of the new top edge appears to cost \(\Theta(\Lambda)\)
   itself; whether any exact-subnorm shift circumvents this is open and
   is now the sharpest open question here. Also open: adaptive schemes
   beyond fixed polynomials (variable-time amplitude amplification gives
   \(\widetilde O(\kappa)\) generally).

5. **Literature grounding (third-round sweep).** The corrected
   \(\Theta(\kappa)\) conclusion is not only a fixed-polynomial
   statement: Orsucci--Dunjko (arXiv:2101.11868, Props. 6--7) prove an
   **all-algorithms** \(\Omega(\min(\kappa,N))\) QLS lower bound in the
   block-encoding (and sparse-oracle) model on an instance whose
   spectrum is exactly two point clusters with hidden Grover structure
   inside the bottom one (needs \(N\ge\kappa^2\)); Somma--de Wolf
   (arXiv:2608.24493) prove eigenvalue discrimination at resolution
   \(\delta\) with a plain block-encoding costs \(\widetilde\Theta(1/\delta)\)
   — matching this note's symmetric-LP figure \(1.0\Lambda\) — and that
   the \(1/\sqrt\delta\) speedup exists precisely in the
   *spectral-amplification* model (access to \(G\) with \(H=G^\dagger
   G\)); Montanaro--Shao (arXiv:2311.06999, Thm 1.6) give \(\Omega(\kappa)\)
   for \(1/x\) in the sparse-oracle model. Zlokapa--Somma
   (arXiv:2404.03644) show low-energy promises do not help plain
   block-encodings — same phenomenon.
6. **Factor access redeems the one-sided class — and QIPMs have it.**
   A polynomial \(p(\lambda)\) bounded on \([0,1]\) only (the relaxed
   class of bounds 2--3 and the truncated-Laplace construction) equals
   the *even* polynomial \(q(\sigma)=p(\sigma^2)\), bounded on
   \([-1,1]\) by evenness — hence **implementable by QSVT on a
   block-encoding of a factor \(G\) with \(H=G^\dagger G\)**. Under
   factor access the \(\widetilde O(\sqrt\kappa)\) route is therefore
   real (and \(\widetilde\Theta(\sqrt\kappa)\) by Somma--de Wolf-type
   tightness; a \(u=\sigma^2\) edge-LP check shows clustering does not
   push below \(\sqrt\kappa\) there either). For IPM normal equations
   \(H=AD A^\top=(AD^{1/2})(AD^{1/2})^\top\) the factor is available
   directly from the data, so QIPM Newton solves naturally sit in the
   factor-access model — never square the condition number.

Consequences (corrected and final). The complete solve-cost table for
two-cluster Newton systems at \(\kappa=\Theta(1/\mu^2)\):
classical CG \(=\operatorname{polylog}(\kappa)\) matvecs; QSVT with
factor access \(=\widetilde\Theta(\sqrt\kappa)\); plain block-encoding,
fixed polynomials or (with hidden structure, \(N\ge\kappa^2\)) any
algorithm \(=\widetilde\Theta(\kappa)\). **Clustering helps the quantum
models not at all beyond what the access model already gives, while it
collapses the classical cost to polylog** — a separation that (per the
sweep) has not been written down before, although its quantum
ingredients are Orsucci--Dunjko's; the classical-side observation that
CG solves their hard instance in \(O(1)\) iterations appears to be new.
The off-spectrum-boundedness channel remains the mechanism, now
understood as an access-model statement: the \([0,\Lambda]\)-vs-
\([-\Lambda,\Lambda]\) constraint gap *is* the factor-vs-plain access
gap. \(\kappa\)-based QIPM resource estimates: pessimistic for hybrid
classical inner solvers on clustered instances; \(\sqrt\kappa\)-level
for factor-access QSVT (the right model for normal equations);
accurate for plain block-encoding solvers **on worst-case right-hand
sides** — but see 2026-09-02-newton-rhs-spectral-alignment.md: the
on-path Newton right-hand sides are spectrally aligned with the top
cluster (weak-mode fraction \(O(\mu^2)\)), so the path-following steps
themselves admit \(\kappa\)-free top-window solves under standard
inexact-Newton contracts; the obstruction binds off-path RHS and
weak-mode output contracts.

## Consequences and recommendations

1. Reconciliation (corrected): the chord-law conditioning floor is
   classically escapable on clustered spectra (CG), which is why
   classical inner solvers do not pay \(\mathrm{poly}(1/\mu)\) there —
   but Theorem Q shows the standard quantum polynomial route retains a
   \(\widetilde\Omega(\sqrt\kappa)\) degree--normalization cost even on
   those spectra. The repository's hardness program (loading, recovery,
   output) is thus joined by a fourth quantum-only interface:
   off-spectrum boundedness of implementable polynomials.
2. QIPM resource estimation: \(\kappa\)-scaled estimates are pessimistic
   for **hybrid schemes with classical iterative inner solvers** on
   clustered instances (orders of magnitude, per the CG numbers), but
   for QSVT-based solvers the \(\sqrt\kappa\)-scale cost is provably
   present in the single-polynomial model, so no such discount may be
   assumed. Checking cluster structure (cheap classically on small
   proxies) remains the right diagnostic — it now tells the classical
   and quantum routes apart.
3. Partially answered open item: natural sparse LPs with genuinely
   spread (non-clustered) central-Hessian spectra at practical depths
   do exist — Netlib adlittle exhibits a single 9-decade continuum
   (see 2026-09-02-netlib-conditioning-survey.md and
   notes/scripts/adlittle_spectrum_probe.py); the asymptotic two-cluster split
   is real but activates only past the float64 wall there. What remains
   open is a family whose spread is \(\mu\)-divergent (Proposition 1
   rules this out under its hypotheses), and the quantum question of
   item Q.4.

## Verification record

- Proposition 1 proof self-checked (Weyl splitting; the
  chord-converse lower end of the bottom cluster reuses Theorem B's
  argument verbatim).
- Proposition 2's composite polynomial checked for the three pointwise
  requirements (cluster 1, cluster 2, normalization at 0) including the
  growth accounting \((4\Lambda)^{m_1}\) of the Chebyshev factor off its
  interval; the \(\log\Lambda\) multiplicative loss versus the true
  two-interval minimax rate (Green-function asymptotics, cf.
  Axelsson-type clustered-CG bounds) is accepted for elementarity.
- Numerics: cluster count, frozen intra-ratios, and CG iteration counts
  over six decades of \(\mu\) (table above); singularity-degree-2 family
  shows the analogous multi-window structure (four windows, exponents
  \(1/2,1,3/2,2\), measured by the audit).
- Independent referee audit completed. Verdict: Propositions 1 and 2
  correct (the \(\sigma_r(DC)\ge\min d_i\cdot\sigma_r(C)\) step survived
  a 20{,}000-trial adversarial search — the single apparent violation
  was float64 SVD roundoff, resolved by exact rational arithmetic; the
  \((4\Lambda)^{m_1}\) growth bound confirmed including tight clusters;
  the composite polynomial verified end-to-end: degree 973 versus naive
  \(1.45\times10^5\) on \([1,4]\cup[10^8,4\times10^8]\)). The original
  QSVT corollary was found fatal: the composite polynomial reaches
  \(\approx10^{85}\) inside the spectral gap, violating QSVT
  admissibility, and the audit's Markov-brothers argument shows no
  polylog-degree admissible polynomial exists. This revision replaces it
  with Theorem Q (the audit's Markov no-go plus the Bernstein branch
  no-go added afterwards, self-checked but not yet externally audited),
  and applies the audit's other repairs: the corrected
  \(\sqrt\kappa\approx2.6\times10^6\) figure, the top-ratio convergence
  wording, \(\kappa=\Lambda\), the \(b_1=a_1\) degenerate case, the
  \(\inf s_i\) clause, the \(r=\dim V\) one-liner, and the four-window
  correction for the singularity-degree family.
- Third-round self-audit and literature sweep (after the external
  Theorem Q audit): a genuine implementability flaw in the then-current
  item 4 was found in-house — the truncated-Laplace polynomial and the
  one-sided tradeoff LP are bounded on \([0,\Lambda]\) but explode on
  \([-\Lambda,0)\) (the value \(T\neq0\) at \(0\) blocks the CKS odd
  extension), so they are not QET-implementable with a plain
  block-encoding; the external audit had verified their approximation
  mathematics, which stands, but not implementability. The symmetric-
  constraint LP (`notes/scripts/qet_implementability_lp.py`) shows the
  implementable minimal degree is \((0.94\text{--}1.04)\Lambda\), and
  the literature sweep found Orsucci--Dunjko's all-algorithms
  \(\Omega(\min(\kappa,N))\) on a two-cluster instance and
  Somma--de Wolf's \(\widetilde\Theta(1/\delta)\)-vs-factor-access
  dichotomy, which ground and complete the corrected items 4--6.
- A second external referee pass audited Theorem Q itself. Verdict:
  **sound with minor repairs**, both applied: the garbled
  "\(\cdot\sqrt{\rho_1}\)-scale" intermediate in the Bernstein step was
  deleted (the correct cap is \(dM/\sqrt{\Lambda-\rho_1}\)), and the
  drop constant was re-derived under an explicit relative-accuracy
  hypothesis \(\delta'\le1/8\) (drop \(\ge5/16\), final constant
  \(5/32\)); items 2 and 4 (Markov no-go; truncated-Laplace
  construction, including the quadrature/boundedness accounting and a
  cosmetic \(\log\rho_1\) for absolute-to-relative conversion) verified
  in full; the LP tradeoff numbers were independently reproduced,
  including the collapse points \(d=0.5\sqrt\Lambda\) and
  \(0.4\sqrt\Lambda\); the audit also strengthened generality (the
  branch no-go covers all fixed admissible polynomials, composite
  products included).
