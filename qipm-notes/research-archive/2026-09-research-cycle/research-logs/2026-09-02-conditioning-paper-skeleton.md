# Paper skeleton: the geometry of central-path conditioning

Date: 2026-09-02
Status: outline only; assembles the day's audited conditioning results
into a paper-shaped narrative. Source notes:
2026-09-02-barrier-independent-conditioning-dichotomy.md (chord law),
2026-09-02-two-cluster-central-hessian-benign-kappa.md (calibration).

## Proposed title

"The sublevel chord law: barrier-independent conditioning of interior
point central paths"

## Narrative arc

1. Question: quantum (and classical inexact) interior point methods pay
   for the condition number of Newton systems; the folklore
   \(\kappa=\Theta(1/\mu^2)\) is always derived for the logarithmic
   barrier. Could a different self-concordant barrier fix it? (No prior
   work answers this; the only all-barriers negative result, AGV STOC'22,
   is about iterations.)
2. Main law (Theorem A + universal \(\lambda_{\min}\) rigidity): at any
   central point with gap \(g\), for every \(\nu\)-SCB:
   \(\lambda_{\min}\asymp_\nu1/\ell(x)^2\) (two-sided, via Dikin
   containment for the lower half — note this half holds at *every*
   interior point, not just central ones — and asymmetric containment
   for the upper half), and \(\lambda_{\max}\ge\|\Pi_Vc\|^2/g^2\); hence
   \(\kappa\ge(D(g)\|\Pi_Vc\|/(2(\nu+2\sqrt\nu)g))^2\). The flat edge of
   the spectrum is geometry, not design.
3. Achievability (Theorem B): log/log-det have
   \(\lambda_{\max}\le S^2n^2/g^2\), so
   \(\kappa_{\rm can}\asymp(D(g)/g)^2\): the canonical barrier is a
   near-optimal barrier for conditioning, at every gap, on every
   instance.
4. The conditioning dictionary (Corollary C): error-bound/sharpness
   exponents become conditioning laws. LP unique optimum = weak sharp =
   \(\kappa=O(1)\) (degenerate vertices included); positive-dimensional
   face = \(\Theta(1/g^2)\) for every barrier; quadratic growth (generic
   unique SDP optimum, curved bodies) = \(\Theta(1/g)\); singularity
   degree \(d\) = \(\Omega(g^{2^{1-d}-2})\), with a proved-and-observed
   fractional law \(\Theta(\mu^{-3/2})\) at \(d=2\).
5. Calibration (companion note, audit-corrected): the ill-conditioning
   is two-clustered with \(\mu\)-free intra ratios, hence benign for
   **classical Krylov** (CG in 3--39 iterations at \(\kappa\) up to
   \(10^{13}\), toys and afiro) — but Theorem Q (final form) proves the
   quantum cost on clustered spectra is
   \(\widetilde\Theta(\kappa)\) for plain block-encodings (Markov/
   Bernstein no-gos + the Orsucci--Dunjko all-algorithms bound on their
   two-cluster instance) and \(\widetilde\Theta(\sqrt\kappa)\)
   under factor access (the natural model for IPM normal equations). This classical--quantum separation on the very
   Newton systems QIPMs must solve is arguably the paper's most
   surprising deliverable, and it reverses the naive resource-estimation
   advice for QSVT-based solvers while keeping it for hybrid classical
   inner solvers. Full-spectrum version: Theorem W pins every eigenvalue
   to sublevel chord widths (Gelfand/Bernstein sandwich).
6. Related work to cite and differentiate: M. Wright 1994/1998, FGW 2002
   (log barrier only); AGV 2022 (iterations, all barriers); Terlaky-group
   QIPM \(\kappa\) analyses (log barrier upper bounds); Apers--Gribling
   condition-free quantum IPMs (outside scope, must be scoped against);
   Burke--Ferris weak sharp minima; Sturm error bounds / singularity
   degree; Bubeck--Eldan, Lee--Yue (barrier constructions — none analyze
   central-path conditioning); Nesterov's containment theorems (proof
   ingredients).
6b. Positive counterpart (RHS alignment note, audited): on-path Newton
   right-hand sides are one universal vector \(Z^\top X^{-1}\mathbf1\)
   with weak-mode fraction \(O(\mu^2)\) (analytic-center annihilation
   + Davis--Kahan), so adaptive window-only solves track the entire
   path: end-to-end runs on afiro converge identically to exact solves
   (rel gap \(7.4\times10^{-10}\), same iteration count), while a
   naive gap-free window rule stalls — the algorithmic message is
   "full solve until the cluster gap opens, then drop the weak modes."
7. Open problems: degenerate-vertex middle constants; SDP
   characterization of \(D(g)\) growth in terms of facial structure
   beyond generic cases; spread-spectrum families where polynomial
   methods genuinely pay; extension of the near-optimality comparison to
   primal--dual scalings not of barrier-Hessian form.

## Additional results found after outlining

- Near-degeneracy plateau: for an LP with a \(\theta\)-nearly-optimal
  face, \(\kappa\) grows as \(\sim1/g^2\) until \(g\approx\theta\) and
  then freezes at \((4/3)\theta^{-2}\) (verified numerically at
  \(\theta=10^{-2},10^{-3}\)); the plateau height is the chord-law value
  and is computable from problem data. Practical: predicts/explains
  conditioning plateaus in QIPM experiments.
- Universal \(\lambda_{\min}\) rigidity: the chord converse
  \(\lambda_{\min}\ge1/\ell(x)^2\) holds for every barrier at every
  interior point via Dikin containment alone; only \(\lambda_{\max}\) is
  barrier-designable.

## Status of verification

All core claims audited or numerically verified as recorded in the source
notes. The chord-law-specific novelty sweep is complete: no prior
universal-over-barriers conditioning bound and no prior barrier
near-optimality claim were found; closest precedents to cite are
M. Wright (Math. Prog. 67, 1994) for the \(\Theta(1/\mu)\) barrier-Hessian
law at nondegenerate NLP optima (the inequality-constraint analog of the
SDP \(\Theta(1/\mu)\) observation) and Augustino et al. (arXiv:2112.06025,
§7) for the contrasting \(1/\mu^2\)-type primal-dual Schur bounds; the
proof-ingredients-are-textbook caveat (Dikin/asymmetric containment plus
\(\nabla F(x_\mu)=-c/\mu\)) should be stated prominently.
