# Stage 4 author record

Author: `stage4_spectra_author`. Completed 2026-09-07. The five independent
reviews found no major issues. The distinct correction agent addressed
the accepted minor findings; see `stage4-corrections.md`.
This record is not manuscript prose.

## Delivered files

- `sections/08-lp-spectra.tex`: LP cluster dimensions for every fixed
  finite-parameter barrier; fixed-face-tangent identification; canonical
  O(g²) and general O(g) weak-projector estimates; exact Newton forcing;
  conditional restricted-solve residual identity; globally verified sharp
  oscillatory barrier and residual-versus-direction counterexample.
- `sections/09-clustered-solves.tex`: complete Chebyshev construction and
  exact-arithmetic CG energy-error bound; quantum normalization, polynomial
  boundedness, RHS, output, and worst-case-versus-fixed-instance boundaries.
- `sections/10-formulation-scope.tex`: fixed coordinate exponent invariance;
  ambient Hessian Schur identity and augmented congruence; explicit Lorentz
  boost; metric length and correctly scaled objective sensitivity; finite-ν
  assumption boundary with a fully proved inverse-power example.
- `main.tex` includes these sections. Four verified bibliography entries added.
- `development/stage4_verify.py`, its saved JSON output, build log, and PDF
  text extraction record the author checks. These are internal checks, not
  the Stage 5 reproducibility package.

The introduction, abstract, numerical section, and full-paper synthesis
remain the explicitly assigned Stage 5 work. No other repository folder was
modified. In particular `central-path-cost` is unrelated and untouched.

## Proof checks and developments

1. The maximal optimal support B gives exactly the face tangent T, rather
   than just a subspace contained in it. The argument explicitly uses both
   feasible displacement signs at an optimal point to force zero objective
   increment. The weak cluster has dimension f = dim Φ, including f = 0 at
   degenerate singleton optima.
2. The logarithmic hard term has kernel T and a uniformly positive scaled
   restriction to T-perp, by classical positive endpoint slacks. The soft
   term is bounded. Weyl/minimax plus Dikin lower bounds prove all scales.
   Equal-gap Loewner comparison then transfers every ordered scale.
3. Canonical projector convergence is proved by applying the inverse hard
   operator on T-perp to H_N Q = Q Λ_w − H_B Q. No endpoint differentiability
   is assumed. General convergence uses only the quadratic-form bound
   H_F >= a g^-2 P_(T-perp), hence O(g) rather than O(g²).
4. The Newton RHS is r (not the LP equality vector b). At an exact center it
   is a scalar multiple of c_V. For approximate centers the manuscript
   explicitly refrains from treating the actual centering residual as the
   same forcing. The geometry/spectral result itself does extend to uniform
   observed-gap centrality residuals below one.
5. Oscillatory example: differentiation gives ψ_xy = cos(log y)/y,
   ψ_yy = −x(sin(log y)+cos(log y))/y², and
   ψ_yyy = x(3 sin(log y)+cos(log y))/y³. Relative to H0, the gradient,
   quadratic, and cubic bounds are respectively 2, 3, 7. Scaling by four
   gives standard differential self-concordance and gradient parameter
   4(2+2ε)²/(1−3ε) < 20. Boundary divergence is preserved by the bounded
   perturbation. This is a global domain proof, not a path-only test.
6. At the exact subsequence, H/4 = [[2, ε/g], [ε/g, g^-2+(1−g)^-2]].
   Its weak eigenvalue tends to 2−ε², not 2. The weak RHS norm is ~εg;
   the weak solution norm is ~εg/[4(2−ε²)], and the strong solution norm
   is ~g²/4. Consequently the discarded-mode relative residual tends to
   zero while the relative Euclidean direction error tends to one.
   The same barrier's central path oscillates on its optimal face and has
   no single endpoint, without invalidating the projector theorem.
7. The CG polynomial growth bound was simplified: its lower-interval
   Chebyshev factor has roots θ_j within that interval, so the product
   formula bounds upper-interval growth by Λ^m. This avoids a separate
   denominator estimate. The stated degree uses log(4Λ), covers degenerate
   one-point intervals, and bounds exact H-energy error. No old numerical
   iteration-count claims were copied.
8. The Schur formula uses the ambient Hessian B explicitly. The reduced
   H_F acts on ker A and cannot be inserted in A H_F^-1 A^T. The full KKT
   matrix changes by congruence, not spectral equivalence.
9. The cross-objective paragraph includes D_(c_V) x = −H_F^-1/μ. The
   sinusoidal example only separates uniformly bounded pointwise spectra
   from derivatives with respect to an unrestricted external parameter;
   its data derivatives grow too. It does not claim unbounded sensitivity
   per unit objective perturbation under a uniform Hessian lower bound.
10. The inverse-power boundary is verified directly. For −log y+η/y,
    the scalar SC inequality is (1+3t)² <= (1+2t)³. The rectangle center
    exists at each sufficiently small gap from μ = −1/F_y > 0, without
    invoking the earlier finite-ν path proposition. κ ~ηg^-3 and the
    gradient ratio ~η/(2g) prove that finite ν is essential.

## Prior work and source access

The local inventory, original Section 4, and the two active workbench
formulation/contact notes were read. The workbench conclusions were reduced
to the relevant proved matrix identities and scope statements; unrelated
cone factorization/topological constructions were not imported.

- Wright (1994), local primary full text: abstract and active-constraint
  setup, including the full-row-rank assumption on the active Jacobian;
  invariant-subspace discussion around Theorem 2.2. The new text uses a
  broad classical antecedent citation and does not identify this LP theorem
  with a differently scaled nonlinear barrier Hessian statement.
- The previously verified Adler--Monteiro/Güler/Halická endpoint results
  are used with the same hypotheses as Stage 3. No novelty is assigned to
  logarithmic endpoint convergence or the canonical two-scale splitting.
- Davis--Kahan is credited for the standard subspace perturbation mechanism;
  the actual projector estimate has a complete elementary proof here.
- Axelsson (1994) is a classical cluster-sensitive CG reference. No unchecked
  chapter locator is given; the entire needed polynomial estimate is proved.
- Gilyén--Su--Low--Wiebe (2019), local primary full text p.4, explicitly
  gives the globally bounded [-1,1] polynomial contract. Metadata checked
  against the primary CWI author-manuscript repository:
  https://ir.cwi.nl/pub/28780/ . DOI 10.1145/3313276.3316366, STOC,
  pp.193–204. No claim that any arbitrary CG residual polynomial meets QSVT
  parity, normalization, or boundedness requirements is made.
- Orsucci--Dunjko (2021), local primary full text §§2.3 and 3, especially
  Proposition 6, states Ω(min{κ,N}) rather than an unqualified Ω(κ) at fixed
  dimension. Its normalization/decomposition/overlap qualifications were
  also inspected in the introductory table and discussion. Primary metadata:
  https://arxiv.org/abs/2101.11868 and DOI 10.22331/q-2021-11-08-573.
  No generic factor-access square-root-κ algorithm is claimed.
- Apers--Gribling (2026), local primary full text abstract, introduction,
  and algorithm outline, checked against the publisher abstract and metadata:
  https://epubs.siam.org/doi/10.1137/25M1736098 . Published SIAM Journal on
  Computing 55(1), 93–134, February 2026. The manuscript cites the row-access,
  tall-LP, explicit-solution positive result qualitatively; it does not
  substitute our fixed-dimensional parameter regime into their complexity.
- Monteiro--da Silva (2026), primary arXiv HTML Definition 4.1 and Remark
  11.1, https://arxiv.org/html/2606.04348v1 . The sole attributed fact is
  the explicit finite-global-ν versus inverse-power distinction. The citation
  is version-specific and labeled preprint. No other theorem or iteration
  claim from that preprint is needed or endorsed.

The Stage 4 contribution is the derived all-barrier spectral statement and
sharp alignment refinement enabled by the main equal-gap theorem, together
with the explicit counterexample. Classical spectral perturbation and CG
estimates are not presented as newly invented techniques. Priority wording
for the whole manuscript is left to the Stage 5 literature synthesis.

## Validation

Command, from `conditioning-paper`:

```sh
/workspace/local-home/miniconda3/envs/qipm/bin/python development/stage4_verify.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The author check passes. It uses NumPy and standard-library Decimal, with
no package installation or external numerical data:

- 2,000 deterministic random local directions on the rectangle, including
  near-boundary points, satisfy the global inequalities; maximum sampled
  SC ratio 0.503268 and gradient parameter 8.04618. A finite-difference
  check of the independently differentiated cubic has maximum normalized
  discrepancy 5.06e-5; its deliberately modest tolerance accounts for
  float64 coordinate cancellation near y=1. These samples check formulas,
  not the universal proof.
- 80-digit Decimal evaluation through k=6 confirms weak eigenvalue 7.9996,
  weak RHS/g 0.01, weak solution/g 0.0012500625031251563, strong solution/g²
  0.25, and relative Euclidean error approaching one. Stable determinant
  division avoids cancellation in the small eigenvalue.
- The constructed residual polynomial is checked on 2,002 interval points
  for four cases: ordinary separated clusters, two singleton clusters,
  a large separation, and narrow almost-touching clusters. All sampled
  residual magnitudes are below 1e-8. Logarithmic evaluation avoids overflow
  of factors whose product remains small.
- The Lorentz boost gives ambient condition 625 at λ=0.2 and relative Schur
  discrepancy 1.07e-14 in an independent numerical matrix calculation.

The final Stage 4 build is 29 pages with no undefined references/citations,
LaTeX warnings, or overfull/underfull boxes. Two long displays were split
before completion. The author checked extracted PDF text for the new sections.
