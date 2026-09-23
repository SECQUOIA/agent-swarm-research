# Stage 2 author audit

Status: complete and ready for independent review, 2026-09-22.

I read all three source notes in full, the current model and fixed-accuracy
section, the root preparation audit, the literature audit, and the root's
new parity development. The results are integrated in main.tex. No subagents
were used.

## Source coverage: joint-accuracy-normalized-shift.md

- Exterior thresholds H_n, monotonicity, asymptotics, and the largest odd
  admissible index are stated in Section 4.1, with labels eq:Hn,
  eq:H-asymptotic, thm:joint-exterior, eq:nK.
- The all-circuit quantitative lower bound retains the sine Taylor target
  in the affine angle coordinate. It includes the negative extrapolation
  point, its sign justification, Bernstein remainders with constants inside
  growing powers, exterior Chebyshev, and the uniform comparison u_s/K.
  This comparison covers arbitrarily fast growth of log(1/K).
- The scalar oracle is used periodically for contractivity, while correctness
  is invoked only on the principal promised interval; no completion-blind
  dependence on sin(t) is presumed.
- The integrated-sign polynomial is constructed and proved contractive on
  the entire interval, with exact unit normalization. Its high-band error
  proof is independent of the low-band Taylor proof.
- The matched K<=delta^beta law and eta<=delta^(1+beta) full-complement law
  are proved with uniform constants (thm:joint-matched).
- The high-band irrelevance to lower bounds and full [delta,1] accuracy of
  the upper are explicit. General coherent/adaptive scope is inherited from
  the precise model, not an unstated extension to postselection.
- Fixed-order relation is captured by H_(2r)=G_r and the distinction between
  the uniform joint bounds and the complete fixed staircase. No universal
  novelty or fully optimal intermediate law is claimed.

## Source coverage: joint-accuracy-normalized-shift-lower.md

- Fejer--Riesz factorization and the analytic map A(exp(i arcsin x)) are
  proved/explained in lem:FR-remainder. The root pairing proof is recalled,
  and the relevant local GQSP proof is cited. The growth bound for A outside
  the disk follows directly from the maximum principle.
- Cauchy's geometric Taylor remainder is stated for arbitrary usable radius
  R. Squaring the Taylor polynomial gives a genuinely globally nonnegative
  polynomial, with the quantitative error obstruction.
- The finite-index margin theorem includes the r<=c_rho delta^(-1/2)
  hypothesis, the factor endpoint argument establishing T>=r+1, the
  adaptive-radius case, and the separate large T*delta case.
- The explicit all-r threshold lower estimate is obtained directly by
  evaluation of the exact threshold formula. The half-threshold hypothesis
  and its constants are stated explicitly.
- The fixed-radius branch rules out T<r+1 simultaneously for every r at
  sufficiently small delta. No artificial restriction on log(1/K) remains.
- The maximum-over-index formula, a conventional quantified exponential
  consequence, and the high-accuracy consequences are included. This proof
  is independent of the exterior-Taylor lower bound.
- The exact K=0 consequence is made explicit: no finite-query exact
  converter exists on the low continuum for sufficiently small delta.
- The QIPM implication is included at the correct access-contract level:
  dimension/sparsity do not remove the continuum lower bound, but finite
  known spectra and supplied complement access can do so. The concrete
  LP application belongs to the next stage.

## Source coverage: joint-accuracy-pinned-gate.md

- The growing threshold index theorem keeps the source hypothesis r->infinity
  and r=o(log(1/delta)), with a degree-independent leading constant.
- Explicit Chebyshev contacts and their angular spacing give the uniform
  quadratic slack. The Dirichlet-kernel power bound is proved directly by
  its average-of-exponentials representation.
- The gate is proved to be an even algebraic polynomial; its degree is
  explicitly at most 4(r+1)^2(r+2)(k-1). Its values are globally in [0,1].
- The low-band leakage/slack ratio tracks all powers, and the signed blend
  proves exact error G_r*delta, including threshold contacts.
- The source's tail estimates (17) and (22) hid an exponential-in-r
  factor. The manuscript corrects them to

      W <= min(1, 2(r+1)^2 * [2/(k|x|)]^(2r+4)).

  The factor 2^(2r+4) is explicitly retained. In the global tail, the
  linear term is bounded by C*r^2*2^(2r)/k=o(1); the polynomial term is
  bounded by C*r*[2*B_rho/(A*R0)]^(2r), controlled by one fixed large A.
- All three global regions are checked before asserting contractivity.
  Neither low/high approximation nor a mesh is used as a contractivity
  substitute.
- High-band analysis includes W itself, as well as W*delta*P; the source
  mainly displayed the latter. Both terms are shown o(G_r*delta), with
  exponential-in-r constants retained. The positive-series truncation and
  the degenerate high point c=1 are treated separately.
- Integer rounding is handled by inequalities k>=k0 and k*delta<=2A*
  delta^(1/(2r)), avoiding an unnecessary hidden degree-dependent rounding
  expansion.
- The source query bound and exponent-one consequence are retained.

## Further development during this stage

The parent proposed these extensions; I independently checked the proofs
and integrated them with complete arguments.

1. The nonnegative EVEN threshold F_r gives an implicit optimal staircase
   for a single even transform, including threshold equality and possible
   plateaus. Attainment, positivity, convergence to zero, the lower Taylor
   limit, and the parity-preserving pinned upper are proved.
2. F_1=F_2=E_1: convexity of a globally nonnegative quadratic in y^2 gives
   the second equality by a chord argument. Consequently the even lower
   for K<E_1 improves from delta^(-3/4) to delta^(-5/6).
3. An explicit globally positive cubic in y^2 at rho=2 has error <1/32.
   This yields the matching even upper and upgrades the comparison to
   Theta(delta^(-5/6)), versus unrestricted Theta(delta^(-1/2)).
4. Odd transforms have matched Theta(delta^(-1)*log(1/delta)) at fixed K.
   The Taylor/exterior lower retains the logarithm; the upper uses a
   bounded sign polynomial minus x, divided by 1+tau, with a proof on
   both the transition region and its complement.
5. Combining the finite-margin lower at r-1 with the growing pinned upper
   gives the same delta exponent on both sides, with lower prefactor
   r*(G_(r-1)-K)^(1/r) and upper r^3. Away from the upper tier boundary,
   including exact lower thresholds K=G_r, the remaining ratio is O(r^2).
   This improves the source's undifferentiated subpolynomial-gap statement.

## Genuine remaining scope

The intermediate regime log(1/K)=o(log(1/delta)) has no proved uniform
multiplicative Theta law here. Away from upper tier boundaries the residual
factor is at most O(log(1/K)^2); very close approach to those boundaries
requires the displayed margin factor or an independent lower index. These
are stated as further questions, not omitted proof steps. The growing
pinned theorem does not assert its construction for r=Theta(log(1/delta));
the matched integrated-sign theorem already settles the high-accuracy
region. Explicit closed formulas for higher F_r are not asserted; the
implicit optimum and the concrete parity comparison are fully proved.

## Literature verification and attribution

- Read local Gilyen et al. extended text at Lemma 25: it states bounded odd
  sign approximation with the required degree and global bound. The
  construction cites this exact lemma.
- Read local Motlagh--Wiebe full text at Theorem 4 and its proof: the
  conjugate-reciprocal root argument and even unit-circle multiplicities
  support the Fejer--Riesz factorization explanation.
- Bos--Ma'u--Waldron exterior inequality, Proposition 2.1, was already
  directly checked by the root in audit/literature.md. Added its local
  metadata/DOI bibliography entry and cited the precise proposition;
  manuscript also gives the elementary proof in the fixed section.
- No novelty is claimed for these classical tools or for generic uniform
  amplification. A broader introduction/literature discussion remains
  a later writing stage.

## Reproducible diagnostics and build

Run:

    /home/sgusev/miniconda3/envs/qipm/bin/python scripts/joint_accuracy_diagnostics.py

from the manuscript directory (the script also works from another directory).
It writes thresholds.csv, pinned_kernels.csv, joint_diagnostics.pdf, and
joint_diagnostics.png under figures/stage2-diagnostics. Thresholds for rho=2,
r=1,...,32 come from the hyperbolic stationary equation, evaluated using a
stable cosh difference. The first G value agrees with the known quadratic
formula; the leading asymptotic ratio approaches one. Pinned diagnostics
use r=2,3,4 and delta=10^(-6r), with k*delta approximately 0.064. Sampled
normalized errors have maximum absolute value 1; sampled leakage/slack
ratios are approximately 6.85e-25, 1.94e-46, and 3.33e-74. Pin leakage is
zero to working precision. These are floating-point numerical checks, not
certificates. The script evaluates the signed error without subtracting
nearly equal values of q and 1-x. The figure was visually inspected.

The script uses installed NumPy, SciPy, and Matplotlib in qipm. No package
was installed. Arbitrary-precision mpmath is not installed, so the optional
diagnostics use the existing SciPy stack and make no interval-certification
claim.

Build command:

    conda run -n qipm --live-stream make all

The full LaTeX/BibTeX build succeeds. The final log has no undefined
references/citations, LaTeX warnings, or overfull/underfull boxes. Figures
are generated as standalone artifacts; their manuscript placement can be
decided during the planned presentation stage.
