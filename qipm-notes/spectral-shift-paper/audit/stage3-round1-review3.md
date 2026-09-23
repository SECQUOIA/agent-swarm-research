# Stage 3, round 1: independent review 3

**Findings: 0 major, 0 minor.** No manuscript repair is requested.

Reviewed all of `sections/06-lp-application.tex`, its integration in
`main.tex`, the relevant bibliography entries, the complete September 4
`sparse-lp-newton-access-separation` source note, and `audit/stage3-author.md`.
No peer reports were read. The deferred introduction and presentation work
are outside this review. No manuscript files were edited.

## Compiler transfer and access distinctions

- **Zero-query coarse tier:** The public contraction
  `(1-m_rho delta)P_minus` has maximum error exactly `G_0 delta` over
  the hidden interval. A public unitary dilation is available without
  queries. Thus the displayed zero is correct, including at `K=G_0`.
  Below `G_0`, the positive-index lower hierarchy excludes that shortcut.
- **Singleton high band:** This family has high spectrum `{1}`, not an
  interval of positive width. Its public, fixed eigenspaces also supply
  more information than the general `c=1` model. The explanation of why
  its coarse cost is zero while the general singleton model has a
  nonzero constant cost is correct. No logarithmic coarse lower bound
  is transferred to this family.
- **Scalar reduction with a fixed high block:** Extending only the
  low-sector block to `R(sin tau)` gives a unitary for every real tau.
  The fixed `R(1)` block adds no trigonometric degree. Arbitrary public
  gates mixing sectors do not change the degree induction, and the
  designated low-sector matrix element remains contractive outside the
  correctness interval. Thus the low-continuum lower proofs apply to the
  fixed completion family without requiring arbitrary completions as
  inputs. Excluding `B_t` from the compiler contract is necessary for
  this proof and is stated explicitly.
- **Positive tiers and joint precision:** The existing upper
  constructions apply with `c=1`; the scalar reduction gives the
  corresponding lower bounds. In the high-accuracy regime,
  `log(delta/eta)=Theta_beta(log(1/eta))` follows from
  `eta<=delta^(1+beta)`. The conversion from delta to condition number
  is uniform because `1/t` lies between `1/(rho delta)` and `1/delta`.
  The finite-index, growing-index, vanishing-relative-error, and exact
  impossibility consequences retain their original hypotheses.
- **Two-query factor bypass:** In addition to the left-side QSVT
  interpretation, the projector identity verifies the claim directly:
  compressing `U_A(I-Pi_C)U_A^*` to the row space gives
  `I_R-A_t A_t^T`. A free block encoding of the public projector needs
  no oracle calls; surrounding it by `U_A^*` and `U_A` uses two.
  The column null vector is outside the output space and contributes
  no spurious row eigenvalue.
- **Known-parameter and digital bypasses:** If t is known, public
  projectors permit direct zero-query synthesis; with unknown
  projectors the earlier two-point polynomial still gives two queries.
  The displayed entries determine t uniquely. In particular the factor
  coefficient `(q_minus)_1` is positive, so its inversion is legitimate.
  Approximate digital access can resolve the parameter to fixed state
  error with precision chosen as a function of delta. The manuscript
  correctly separates that precision and arithmetic cost from query
  count. The normalization-two controlled-LCU construction uses one
  query and does not contradict the unit-normalized lower bounds.

## LP construction and state theorem

The vector triples are orthonormal. The singular values of A are one and
`sqrt(t)`, giving the stated rank, norm, normal matrix, and condition
number. The null direction has both signs because it is orthogonal to
the strictly positive `q_plus`, so intersecting its affine line with the
orthant gives a nontrivial compact segment. Its objective derivative is
`cos(theta)/sqrt(3)>0`. The stated primal-dual point satisfies feasibility,
strict positivity, and complementarity exactly.

The predictor signs are consistent: eliminating the slack direction gives
`Delta x=-1+A_t^T Delta y`, and primal feasibility then gives
`H_t Delta y=A_t 1`. The displayed right side and solution follow from
the two singular-vector overlaps. In particular the primal direction is
public and independent of t, whereas the dual direction depends on the
representation parameter. This limitation is explicitly acknowledged.

The full normal, rectangular, and right-side oracles have the stated
unitarity and completions. Withholding the right-side norm avoids a direct
classical disclosure of t. The endpoint target trace distance is exactly
`d_rho`. The per-query endpoint bounds are valid in the specified parameter
range, including the factor singular value `sqrt(t)<1/2`. The right-side
oracle difference is only `O_rho(delta)`; counting it in the hybrid sum
therefore preserves both lower bounds. Purification and partial trace
justify the same conclusion for the density-output task with measurements.

For the matching upper bounds, the preparation success probabilities are
`t^2` and t, respectively. The amplitude-estimation error, square-root
conversion in the normal model, clipping, and median repetition give
the claimed additive `O(epsilon_0 delta)` estimate. The derivative of the
target angle is at most `1/(4 delta)`, and averaging over failure events
gives total trace error less than `epsilon_0` without postselection.
The algorithms have bounded worst-case query counts and do not use `B_t`.
The pseudoinverse identity and support overlap `(8/9)(1+delta)` are also
correct; no generic solver theorem is needed for the sharp upper bounds.

## Source coverage and integration

Every mathematical component of the source note is covered: the central
LP, both state-access models, continuum compiler transfer, factor bypass,
joint law, and digital/normalization limitations. The manuscript improves
the source's logarithm-suppressed factor-state upper bound by an explicit
amplitude-estimation algorithm and corrects the source's unqualified
complete-staircase transfer at the coarse tier. The distinction between
state output and reusable coherent conversion is maintained throughout.

`main.tex` includes the new section after the joint-accuracy section. The
BHMT entry is present, and local primary-source text identifies Theorem 12
as the amplitude-estimation result with the stated success probability.
The cited Orsucci--Dunjko discussion supports the established factor and
normalized-complement background; this section does not claim those
general ideas as new. Inspection of the current LaTeX log found no warning,
undefined-reference, or overfull/underfull-box entries. I did not rebuild
or change generated manuscript artifacts.

## Independent numerical checks

Used `/home/sgusev/miniconda3/envs/qipm/bin/python` with installed NumPy;
no packages were installed. A separate diagnostic checked 27 instances
with rho in `{1.1,2,20}`, delta in `{1e-2,1e-4,1e-6}`, and t at both
endpoints and the midpoint. All satisfy the stated parameter restrictions.

Checked the factorization, normal equation, primal predictor feasibility,
predictor elimination identity, both full-unitary identities, the explicit
two-query projector compression, right-side preparation, objective
derivative, bounded entries, endpoint trace distances, and all three
endpoint oracle-distance bounds. The largest matrix/vector identity
residual was `1.19e-15`. These checks support the analytic verification;
they are not numerical proof certificates.
