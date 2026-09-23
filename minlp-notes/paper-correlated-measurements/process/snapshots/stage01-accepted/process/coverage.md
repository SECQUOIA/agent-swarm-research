# Coverage and stage interfaces

Inventory date: 2026-09-13. This is a paper-development record, not part of the
submission manuscript. Repository notes and agent reviews are evidence to be
re-examined, not mathematical references or external peer review.

The paper concerns global bounds for discrete choices under the actual selected
Gaussian covariance, together with locality theory and limitations that explain
those bounds. The original source-model correction and the later temporal
synthetic kinetic experiments are distinct studies. The latter do not reproduce
the published covariance or resolve the archived sensitivity-generation provenance.

## Sequential writing plan

1. Foundations and source audit (current): `sections/01-foundations.tex`.
2. Locality: `sections/02-locality.tex`, with supporting proofs in an appendix.
   Exact Markov prior art, scalar/full-block/general covariance/partial-packet
   relative bounds, spacing and pair refinements.
3. Approximation guarantees: `sections/03-approximation.tex` and detailed
   supporting appendices. Weighted-trace schemes, scalar prior-art reduction,
   fixed-dimension spectral approximation sets and D/A/E/contrast consequences.
   Include the represented-matroid extension as a separate additive-information
   result, not a solver for arbitrary correlated matroid selection.
4. Relaxation and certification: `sections/04-certification.tex`, with exact
   arithmetic, virtual-noise equivalence/barriers, finite-scenario normalization,
   and separator-hierarchy proofs in main text or appendices.
5. Computational investigation: `sections/05-computation.tex` and a standalone
   supplement with model data, certificate witnesses, checkers and reproduction
   instructions. Verify source-model comparisons, sensitivities and archived
   bounds; develop matched grid/separator experiments and necessary corrections.
   Root proposes exact D and conventional A ranking certification of the public
   source problem in addition to its existing exact trace rankings.
6. Synthesis: introduction, abstract, contribution comparison, limitations,
   conclusion, bibliography reconciliation, figures/tables, reproducible package
   and final submission checks. This stage follows accepted stages 1–5.
7. Entire-manuscript five-reviewer gate, corrections by a separate agent, and
   repeated five-reviewer rounds after accepted major issues.

Every numbered author stage is followed by five independent reviewers, root
adjudication, a separate correction author if any issue is accepted, and a fresh
five-reviewer round after accepted major issues. All valid minor issues must be
resolved before the next writing stage. `PROCESS.md` is owned by root.

## Consistent notation

- `n`: number of candidate times/packets; `d_t`: acquired packet dimension;
  `d_tot`: number of scalar candidate responses; `p`: mean-parameter dimension.
- `S`: a feasible packet schedule in `calF`; matrix subscripts include all its
  scalar coordinates. For partial latent observation, observation matrices should
  use `H_t`; histories should use `mathcal H_t` to prevent a collision.
- `R`: known full observation covariance; `F`: nominal mean sensitivity;
  `I(S)=F_S^T R_SS^{-1}F_S`; `J(S)=J_0+I(S)`; `J_gate` for full-inverse gating.
- `J_0`: declared PSD prior/regularizer. Later log/Schur numerical certificates
  may impose SPD; every such strengthening must be explicit.
- `L`: calendar history length; `g`: minimum calendar sampling gap; `k`:
  cardinality; `Q_L(S)` for approximate precision and `J_L(S)` for corresponding
  information (avoid `Q` for both precision and a sensitivity matrix).
- `D_t`: local conditional covariance; `Z_t`: local innovation/residual;
  `delta_L`: uniform spectral error; `W`: weighted-trace criterion weight.
- `N` or `J_ref`: an arbitrary SPD tangent reference. Do not assume it is a
  feasible integer information matrix.
- `a` / `D=diag(a_i)`: scalar/diagonal virtual-noise split, distinct from
  sampling-gap `g` and local residual covariance `D_t`.
- `s=1,...,q`: scenario index; `b_s^*`: individual true scenario log optimum;
  `g_*`: worst standardized log information; efficiency exponent always `1/p`.
- `A`: anchor set in separator sections, with nuisance vector `U=X_A`;
  matrix letters for Schur blocks must be local and explicitly defined.
- `ell,U`: verified lower and upper log-objective bounds; a displayed decimal
  must be outward rounded if asserted as a certified bound.

## Substantive result map

Paths below are relative to repository root. `notes/` items begin with
`research-20260912-`; this prefix is omitted in the table for readability.

| Development and principal source notes | Planned location | Status and required treatment |
|---|---|---|
| `measurement-source-audit`, `gated-information-bounds`, `gated-bound-independent-review` | Foundations, source-data experiment | Established selected-covariance correction (Liu 2016), Schur identity, sharp Kantorovich consequence and rank refinement; no new inequality or discovery of the mismatch claimed. Distinguish noise side information from actual responses. |
| `kinetics-selection-recheck`, `kinetics-independent-review`; `kinetics_selection_recheck.py`, `kinetics_trace_certificate.py`, input provenance | Computation source-model subsection and data supplement | All 2347 nonempty source-code-feasible schedules, 11 budgets and 33 criterion-budget comparisons; one trace choice changes with 3.1128% loss, source D and conventional A choices agreed numerically. Existing exact arithmetic proves all trace rankings; exact D/A extension to be attempted in stage 5. Same-time independent blocks, regularization and code spacing must be stated. |
| `design-opportunities`, `measurement-implementation`, `markov-priority-audit`, `markov-theory-independent-review`, `path-oracle-independent-review`, `oa-solver-independent-review` | Locality introduction, implementation context | Exact noiseless complete-block Markov innovations and ordered-path hull are known through Lee–Gómez–Atamtürk. Forward/reverse equivalence telescopes even on fractional flows; singular-transition extension follows continuity. Cardinality layering/support duality is inherited machinery. |
| `markov-priority-audit` Section 7 | Locality background/scope appendix | Regular fully observed Markov likelihoods have additive expected gap Fisher information, including non-Gaussian and covariance-parameter examples under regularity. Established score orthogonality (Pagendam–Pollett; Baran et al.); not an extension of the finite-memory Gaussian fixed-covariance theorem without further hypotheses. |
| `noisy-markov-memory`, `noisy-markov-independent-review`, `noisy-markov-design-implementation`, block review | Locality main theorem and proof appendix | Genuine local Gaussian conditionals, explicit simultaneous relative precision bound over all selected subsets; calendar history differs from last-selected-count history. Scalar gain improvement and dimension-free noise-whitened full-block version. Candidate contribution is explicit bound plus design certificate, not Vecchia construction/filtering. |
| `noisy-markov-spacing`, `spacing-design-implementation`, spacing producer and integration reviews | Locality refined bound; certification DP | Stationary scalar covariance, innovation floor, finite-horizon distance-row pricing, minimum gap, compact feasible masks, edge cases L=0 and g>L. Additional history bits enforce spacing even when information memory is shorter. |
| `noisy-markov-far-pair-refinement`, `pair-refinements-independent-review` | Locality proof appendix and refined empirical certificate | Exact far-pair identity valid nonstationarily; stationary near-pair gain improvement requires stationarity. Retain reviewed nonstationary counterexample, do not extend bound beyond assumptions. |
| `integer-interval-scores`, integer and spacing integration reviews | Certification arithmetic appendix, supplement | Outward signed integer interval arc scores, validated innovation floor, ceiling loss/path length and exact integer pricing. Engineering consequence of interval arithmetic, no novelty claim. |
| `general-covariance-memory-bound`, `general-covariance-memory-independent-review`, `covariance-decay-priority-audit` | Locality theorem and appendix; approximation stage (Section 6 scheme) | Exponentially decaying off-diagonal blocks and a uniform lower eigenvalue suffice; diagonal blocks need no upper bound. Explicit constants independent of candidate/packet dimension; supplied rational metrics and variable packet dimensions. Section 8 dummy-block padding transfers suitable class-uniform full-calendar theorems to selected subsets, and block-diagonal normalization permits older bounded-spectrum estimates: neither subset uniformity nor unbounded original diagonal blocks alone establishes novelty. Stage 2 must explain these reductions and compare the actual hypotheses/constants. Classical inverse decay/regression localization credited; constants conservative. Section 6 inherits a weighted-trace FPTAS with packet and parameter dimension as input, under fixed decay and conditioning promises, rational inputs, and complete-packet exact-cardinality selection (optional mandatory/forbidden times); Stage 3 must state and verify it. |
| `partial-observation-memory-bound`, `partial-observation-independent-review` | Locality theorem and appendix | Fixed selectable packets observe input-sized latent states; process-noise floor, covariance contraction and normalized residual refinement. Does not permit arbitrary selectable channels. Exact coordinate-change checks. |
| `scalar-noisy-design-fptas`, `scalar-fptas-independent-review`, `scalar-gmrf-prior-reduction`, `scalar-gmrf-prior-independent-review` | Locality algorithm consequences and prior-art appendix | Scalar approximation algorithm retained; first scalar FPTAS novelty withdrawn because of focused-target reduction to Mahalanabis–Štefankovič. Explain proof adaptation and printed inverse/block-order issue with singleton target bag avoidance rather than citing an unqualified existing theorem. |
| `full-block-design-fptas`, `full-block-fptas-independent-review` | Locality approximation theorem | Weighted-trace FPTAS with both channel and parameter dimension as input under fixed rational contraction/noise promises, exact cardinality; complete packet selection essential. Include individual-channel hardness boundary. |
| `fixed-parameter-doptimal-fptas`, `doptimal-fptas-independent-review` | Spectral supporting appendix and D consequence | Fixed p, explicit rational PSD-edge DAG, singular prior allowed. Superseded/strengthened by relative spectral-set result; do not duplicate proofs unnecessarily. High exponent and no practical algorithm implementation. |
| `dag-psd-approximation-set`, `psd-approximation-set-independent-review` | Spectral supporting appendix | Feasible relative matrix cover with exact kernel preservation; D/A/E and estimable-contrast consequences, all ranks, rational normalization and bit complexity. Include complete proof, not agent-review citations. Fixed information dimension essential. |
| `represented-matroid-psd-approximation-set`, `represented-matroid-psd-independent-review` | Separate supporting appendix | Explicit rational representation, input matroid rank, fixed p; exact profile detection/interpolation, contraction/deletion and witness recovery. This concerns additive PSD atoms, not general correlated subset information. Established Berstein et al. machinery credited. |
| `noisy-markov-fsai-priority-audit`, `kaminetz-webber2026-priority-audit`, `kaporin-metric-independent-check`, `vecchia-supermodularity-independent-review` | Locality literature comparison and short counterexample appendix | Fixed-pattern Vecchia optimality and inverse decay are prior art. Repeated-pair Kaporin metric scales with n while uniform spectral error does not. A global Gaussian KL bound already implies a relative precision and mean-Fisher sandwich (`noisy-markov-fsai-priority-audit`, Section 5); Stage 2 must give the short eigenvalue argument and distinguish assumptions, constants, calendar window and horizon dependence, not assert a categorical KL/Fisher separation. Thesis counterexample must not be attributed to March 2026 paper, which makes no such supermodularity claim. Historical factorization-inheritance/direct-sum proposal remains unproved and excluded as a theorem. |
| `noisy-markov-certificates`, `noisy-exact-independent-review`, solver reviews and `certify_noisy_markov.py` | Certification main theorem and exact supplement | Uniform sandwich transfers arbitrary-SPD log tangent and support prices to true selected covariance, with prior handled correctly; selected lower values and logs exact for rational inputs. Small exhaustive checks and larger certificates. |
| `spacing-certificates`, spacing certificate review, refined-spacing integration review | Certification refinement and computation | All spacing constraints included in integer pricing; initial/refined/interval certificates distinguished; saved refined kinetics certificate and time tradeoff. |
| `structured-dense-oracle`, its review, `covariance-dense-oracle`, covariance review | Comparator implementation appendix | Same Liu/virtual-noise relaxation, algebraic tridiagonal and covariance filtering/RTS reverse derivative oracles. Prior precision-space method fails near unit correlation despite moderate covariance conditioning; repaired covariance oracle needed. No new relaxation/filtering claim. |
| `exact-dense-design-certificates`, dense certificate review, `kinetics-dense-certificate-review` | Certification comparator theorem and computation | Exact admissible-split check, feasible fractional lower value and tangent upper bound on continuous relaxation. Six synthetic and four kinetic cases. Fair comparison separates continuous solve error from relaxation gap. |
| `all-splits-separation`, all-splits review | Certification barrier theorem and computation | Pointwise split monotonicity, rational spectral witness and common fractional lower value for every admissible scalar split; includes boundary tuning. No universal barrier to all relaxations. |
| `diagonal-split-separation`, diagonal review | Certification barrier theorem and appendix | Fixed-selection convexity in diagonal split, SDP dual witness, exact >0.09254 chemical separation; survives pointwise split optimization and all affine upper tangents in family. Synthetic negative example retained; branching and other cuts outside scope. |
| `noisy-markov-kinetics-probe`, kinetic independent review | Computation nominal temporal study and model supplement | Four original-covariance log gaps below 0.001943; analytic sensitivities checked against independent ODE and high-precision matrix exponentials. Stipulated AR(1)+nugget errors and local log parameters; rate-swap ambiguity retained. |
| `block-snapshot-probe`, block-snapshot review | Computation full-packet limitations | Noncommuting/multichannel complete-packet examples, d=4 and d=16; greedy may choose identical schedule, dense bound can be tighter. Not general superiority. |
| `partial-observation-trace-probe`, partial trace probe/reviews, `partial-trace-certificates` | Computation partial-packet study; certificate supplement | Two latent drift modes, fixed scalar observation, trace with specified parameter scaling and prior; four exact relative gaps <0.0604%; dense numerical comparator faster but wider on these small examples. |
| `robust-kinetic-design`, `robust-design-certificates`, robust solver and certificate reviews, `robust-scenario-design-priority-audit` | Certification robust theorem and computation | One shared schedule over finite scenarios, known scenario covariances, raw vs standardized log criteria, invariant normalization, uncertainty intervals for individual optima. Maximin and standardized D-efficiency are established; no coverage of continuous uncertainty region. |
| `robust-dense-comparison`, robust dense review, `compare_robust_nominal.py`, `certify_robust_polish.py` | Computation robust matched comparison | Central-scenario schedules, greedy/exchange and dense relaxation; original winners mixed; 96-candidate polished exact standardized log gap 0.011487999119. Include incumbent-generation costs, local-optimum status correction and scenario-weight normalization repair. |
| `fixed-physical-grid-benchmark`, fixed-grid review, `fixed_physical_grid_refined_transfer.py` | Computation scaling study | Fixed physical horizon/covariance and k=16, grids n=48/96/192; target 0.01 missed on finer grids. Empty support-price timeouts reported as failure; 96 smaller-window diagnostic separate from primary budgeted runs. No claim exponential time is necessary. |
| `latent-separator-design`, theory review, `latent-separator-priority-audit` | Certification separator hierarchy theorem and proof | Exact anchor Gaussian conditional block decomposition, nuisance Schur criterion, nested anchor removal tightens fractional mixture bounds, stationary implementation. Full proof of cross-representation comparison; arbitrary shifted partitions not ordered. Generic Schur/conic/mixture/disjunctive grouping machinery known. |
| `latent-separator-implementation`, implementation review, `latent-separator-certificates`, certificate review | Computation hierarchy and exact supplement | Arbitrary rational nuisance witnesses, block-pattern pricing and exact certificate; five archived rational certificates. At n=192 best gap 0.157284408207 still misses 0.01; b=16 total cost exceeds 30 s despite solve alone fitting. Exponential block-pattern cost and growing nuisance dimension explicit. |
| `contribution-map`, `closeout`, `completion-audit`, `impact-assessment`, research logs and literature reports | Introduction/synthesis and internal reconciliation | Superseding status and empirical limitations, not external scientific citations. Several earlier missing-source claims are stale after Sep13 literature promotions. |

## Explicit exclusions

The following adjacent developments are excluded from scientific claims in this
paper: `ode-prototype`, `validated-polynomial-tubes`, `rational-flow`, their
reviews and scripts, `ode_support_experiment.py`, `polynomial_tubes.py`, and
`rational_affine_flow.py`, `extended_rpd.py`, and their implementation/review
artifacts concern relaxation/validated propagation for dynamic
optimization, not selecting observations from a supplied Gaussian covariance.
They have neither an integrated design certificate nor a demonstrated design
advantage. Excluding them does not exclude the independent ODE sensitivity
validation used by the kinetic measurement experiments.

The storage-balance/perspective investigation (`energy-opportunities`, storage
review and `storage_balance_perspective_gap.py`) and quadratic-conflict example
(`algorithm-opportunities` nonmeasurement portions,
`verify_quadratic_conflict_example.py`) have different feasible objects and
objectives. They are not measurement-design developments. General certified-MINLP,
LB-ESH/GDP, pooling, power-flow, and network papers are outside this topic.

The historical FSAI factorization-inheritance proposal is unproved and cannot be
promoted to a theorem. Failed runs, rejected novelty claims, and counterexamples
are retained as limitations/attribution corrections where relevant; they are not
hidden and are not described as unfinished positive results.
