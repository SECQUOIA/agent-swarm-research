# Coverage and stage interfaces

Inventory date: 2026-09-13. This is a paper-development record, not part of the
submission manuscript. Repository notes and agent reviews are evidence to be
re-examined, not mathematical references or external peer review.

The paper concerns global bounds for discrete choices under the actual selected
Gaussian covariance, together with locality theory and limitations that explain
those bounds. The original source-model correction and the later temporal
synthetic kinetic experiments are distinct studies. The latter do not reproduce
the published covariance or establish the original public CSV's sensitivity-generation provenance.

## Manuscript and review structure

The scientific manuscript has seven main sections: introduction; statistical
foundations; locality; approximation; certification; computation; and discussion
and conclusion. Supporting appendices contain the scope counterexamples, scalar
predecessor adaptation, represented-matroid proof, arithmetic, structured oracle,
robust witnesses, separator identities, and computational model details.

The corresponding source files are `sections/00-introduction.tex` through
`sections/06-discussion.tex` and the four files in `appendices/`. The portable
`supplement/` holds the data, witnesses, checkers and numerical producers.
The source-model extension now proves D and conventional A rankings exactly,
in addition to trace.

The staged development and five-reviewer gates are recorded in root-owned
`PROCESS.md` and the numbered reports. This coverage map records final scientific
locations and dispositions; it is not the live review-status tracker.

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

| Development and principal source notes | Manuscript location | Final scientific treatment |
|---|---|---|
| `measurement-source-audit`, `gated-information-bounds`, `gated-bound-independent-review` | Foundations, source-data experiment | Established selected-covariance correction (Liu 2016), Schur identity, sharp Kantorovich consequence and rank refinement; no new inequality or discovery of the mismatch claimed. Distinguish noise side information from actual responses. |
| `kinetics-selection-recheck`, `kinetics-independent-review`; `kinetics_selection_recheck.py`, `kinetics_trace_certificate.py`, input provenance | Computation source-model subsection and data supplement | All 2347 nonempty source-code-feasible schedules, 11 budgets and 33 criterion-budget comparisons; one trace choice changes with 3.1128% loss; D and conventional A choices agree exactly at all budgets. New independent full-covariance arithmetic verifies all 14,082 objective values and all 66 unique formula-specific optima. Same-time independent blocks, regularization, modality costs and code spacing are stated in `subsec:source-computation`. |
| `design-opportunities`, `measurement-implementation`, `markov-priority-audit`, `markov-theory-independent-review`, `path-oracle-independent-review`, `oa-solver-independent-review` | Locality introduction, implementation context | Exact noiseless complete-block Markov innovations and ordered-path hull are known through Lee–Gómez–Atamtürk. Forward/reverse equivalence telescopes even on fractional flows; singular-transition extension follows continuity. Cardinality layering/support duality is inherited machinery. |
| `markov-priority-audit` Section 7 | Locality background/scope appendix | Regular fully observed Markov likelihoods have additive expected gap Fisher information, including non-Gaussian and covariance-parameter examples under regularity. Established score orthogonality (Pagendam–Pollett; Baran et al.); not an extension of the finite-memory Gaussian fixed-covariance theorem without further hypotheses. |
| `noisy-markov-memory`, `noisy-markov-independent-review`, `noisy-markov-design-implementation`, block review | Locality main theorem and proof appendix | Genuine local Gaussian conditionals, explicit simultaneous relative precision bound over all selected subsets; calendar history differs from last-selected-count history. Scalar gain improvement and dimension-free noise-whitened full-block version. The contribution is the explicit bound plus design certificate, not Vecchia construction/filtering. |
| `noisy-markov-spacing`, `spacing-design-implementation`, spacing producer and integration reviews | Locality refined bound; certification DP | Stationary scalar covariance, innovation floor, finite-horizon distance-row pricing, minimum gap, compact feasible masks, edge cases L=0 and g>L. Additional history bits enforce spacing even when information memory is shorter. |
| `noisy-markov-far-pair-refinement`, `pair-refinements-independent-review` | Locality proof appendix and refined empirical certificate | Exact far-pair identity valid nonstationarily; stationary near-pair gain improvement requires stationarity. Retain reviewed nonstationary counterexample, do not extend bound beyond assumptions. |
| `integer-interval-scores`, integer and spacing integration reviews | Certification arithmetic appendix, supplement | Outward signed integer interval arc scores, validated innovation floor, ceiling loss/path length and exact integer pricing. Engineering consequence of interval arithmetic, no novelty claim. |
| `general-covariance-memory-bound`, `general-covariance-memory-independent-review`, `covariance-decay-priority-audit` | `thm:general-decay`, `cor:decay-metric`, `thm:trace-fptas` | Exponentially decaying off-diagonal blocks and a uniform lower eigenvalue suffice; diagonal blocks need no upper bound. Explicit constants independent of candidate/packet dimension; supplied rational metrics and variable packet dimensions. Section 8 dummy-block padding transfers suitable class-uniform full-calendar theorems to selected subsets, and block-diagonal normalization permits older bounded-spectrum estimates: neither subset uniformity nor unbounded original diagonal blocks alone establishes novelty. `subsec:locality-prior` proves both reductions and compares their hypotheses/constants. Classical inverse decay/regression localization credited; constants conservative. The source note's Section 6 weighted-trace FPTAS is included with packet and parameter dimension as input, under fixed decay and conditioning promises, rational inputs, and complete-packet exact-cardinality selection (optional mandatory/forbidden times); `thm:trace-fptas` states and proves the rational complexity result. |
| `partial-observation-memory-bound`, `partial-observation-independent-review` | Locality theorem and appendix | Fixed selectable packets observe input-sized latent states; process-noise floor, covariance contraction and normalized residual refinement. Does not permit arbitrary selectable channels. Exact coordinate-change checks. |
| `scalar-noisy-design-fptas`, `scalar-fptas-independent-review`, `scalar-gmrf-prior-reduction`, `scalar-gmrf-prior-independent-review` | Locality algorithm consequences and prior-art appendix | Scalar approximation algorithm retained; first scalar FPTAS novelty withdrawn because of focused-target reduction to Mahalanabis–Štefankovič. `app:scalar-prior` proves the adaptation and avoids the printed inverse/block-order issue with a singleton target bag. |
| `full-block-design-fptas`, `full-block-fptas-independent-review` | Locality approximation theorem | Weighted-trace FPTAS with both channel and parameter dimension as input under fixed rational contraction/noise promises, exact cardinality; complete packet selection essential. `prop:channel-hardness` supplies the individual-channel boundary. |
| `fixed-parameter-doptimal-fptas`, `doptimal-fptas-independent-review` | Spectral supporting appendix and D consequence | Fixed p, explicit rational PSD-edge DAG, singular prior allowed. Superseded and strengthened by the fully proved relative spectral-set result. High exponent and no practical algorithm implementation. |
| `dag-psd-approximation-set`, `psd-approximation-set-independent-review` | Spectral supporting appendix | Feasible relative matrix cover with exact kernel preservation; D/A/E and estimable-contrast consequences, all ranks, rational normalization and bit complexity. Complete standalone proof in `thm:dag-spectral-set`. Fixed information dimension essential. |
| `represented-matroid-psd-approximation-set`, `represented-matroid-psd-independent-review` | Separate supporting appendix | Explicit rational representation, input matroid rank, fixed p; exact profile detection/interpolation, owner-count enforcement, deletion and witness recovery. The Lean implementation uses an extra marker coordinate instead of constructing a contraction. This concerns additive PSD atoms, not general correlated subset information. Established Berstein et al. machinery credited. |
| `noisy-markov-fsai-priority-audit`, `kaminetz-webber2026-priority-audit`, `kaporin-metric-independent-check`, `vecchia-supermodularity-independent-review` | Locality literature comparison and short counterexample appendix | Fixed-pattern Vecchia optimality and inverse decay are prior art. Repeated-pair Kaporin metric scales with n while uniform spectral error does not. A global Gaussian KL bound already implies a relative precision and mean-Fisher sandwich (`noisy-markov-fsai-priority-audit`, Section 5); `app:locality-metrics` proves the eigenvalue implication and distinguishes the assumptions and horizon dependence. `app:pivot-supermodularity` confines its counterexample to the thesis; the distinct March 2026 paper makes no such claim. Historical factorization-inheritance/direct-sum proposal remains unproved and excluded as a theorem. |
| `noisy-markov-certificates`, `noisy-exact-independent-review`, solver reviews and `certify_noisy_markov.py` | Certification main theorem and exact supplement | Uniform sandwich transfers arbitrary-SPD log tangent and support prices to true selected covariance, with prior handled correctly; selected lower values and logs exact for rational inputs. Small exhaustive checks and larger certificates. |
| `spacing-certificates`, spacing certificate review, refined-spacing integration review | Certification refinement and computation | All spacing constraints included in integer pricing; initial/refined/interval certificates distinguished; saved refined kinetics certificate and time tradeoff. |
| `structured-dense-oracle`, its review, `covariance-dense-oracle`, covariance review | Comparator implementation appendix | Same Liu/virtual-noise relaxation, algebraic tridiagonal and covariance-filter/reverse-adjoint oracles in `app:dense-oracle`. The precision-space method can fail near unit correlation despite moderate covariance conditioning; the separately failed RTS residual-subtraction implementation is distinguished from the repaired reverse adjoint. No new relaxation/filtering claim. |
| `exact-dense-design-certificates`, dense certificate review, `kinetics-dense-certificate-review` | Certification comparator theorem and computation | Exact admissible-split check, feasible fractional lower value and tangent upper bound on continuous relaxation. Six synthetic and four kinetic cases. Fair comparison separates continuous solve error from relaxation gap. |
| `all-splits-separation`, all-splits review | Certification barrier theorem and computation | Pointwise split monotonicity, rational spectral witness and common fractional lower value for every admissible scalar split; includes boundary tuning. No universal barrier to all relaxations. |
| `diagonal-split-separation`, diagonal review | Certification barrier theorem and appendix | Fixed-selection convexity in diagonal split, SDP dual witness, exact >0.09254 chemical separation; survives pointwise split optimization and all affine upper tangents in family. Synthetic negative example retained; branching and other cuts outside scope. |
| `noisy-markov-kinetics-probe`, kinetic independent review | Computation nominal temporal study and model supplement | Four original-covariance log gaps below 0.001943; analytic sensitivities checked against independent ODE and high-precision matrix exponentials. Stipulated AR(1)+nugget errors and local log parameters; rate-swap ambiguity retained. |
| `block-snapshot-probe`, block-snapshot review | Computation full-packet limitations | Noncommuting/multichannel complete-packet examples, d=4 and d=16; greedy may choose identical schedule, dense bound can be tighter. Not general superiority. |
| `partial-observation-trace-probe`, partial trace probe/reviews, `partial-trace-certificates` | Computation partial-packet study; certificate supplement | Two latent drift modes, fixed scalar observation, trace with specified parameter scaling and prior; four exact relative gaps <0.0604%; dense numerical comparator faster but wider on these small examples. |
| `robust-kinetic-design`, `robust-design-certificates`, robust solver and certificate reviews, `robust-scenario-design-priority-audit` | Certification robust theorem and computation | One shared schedule over finite scenarios, known scenario covariances, raw vs standardized log criteria, invariant normalization, uncertainty intervals for individual optima. Maximin and standardized D-efficiency are established; no coverage of continuous uncertainty region. |
| `robust-dense-comparison`, robust dense review, `compare_robust_nominal.py`, `certify_robust_polish.py` | Computation robust matched comparison | Central-scenario schedules, greedy/exchange and dense relaxation; original winners mixed; 96-candidate polished exact standardized log gap 0.011487999119. Incumbent-generation costs, corrected local-optimum status and exact scenario-weight normalization are included. |
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

## Stage 2 written coverage and final locations

The following labels are actual manuscript locations.
All proofs are standalone and cite primary literature for attribution rather than
repository notes. The map above records the source-development provenance.

| Covered source development | Actual manuscript labels and disposition |
|---|---|
| Exact noiseless complete-block Markov information, prior hull mapping, forward/reverse fractional equivalence, singular-transition boundary | `subsec:exact-markov`, `eq:exact-markov-arcs`, `eq:forward-reverse`; explicitly inherited Lee–Gómez–Atamtürk / Wei et al. machinery. |
| Markov score orthogonality, non-Gaussian and covariance-parameter gap information | `app:markov-scope`, `eq:general-markov-fisher`; regularity hypotheses and complete derivation, with no extension of finite-history covariance-parameter guarantees. |
| True local conditionals, calendar histories, residual overlaps, precision/information transfer, PSD priors | `subsec:local-conditionals`, `lem:residual-transfer`, `lem:local-row`, `eq:prior-aware-local`. Common proof replaces duplicated scalar/block/general calculations. |
| Scalar noisy Markov base/gain bound, full-grid innovation floor, stationary fixed point, degenerate dynamics | `thm:scalar-locality`, `eq:scalar-refined-delta`, `eq:gain-delta`, `eq:full-grid-floor`. Signed/nonstationary and zero process-noise scope explicit. |
| Full observed blocks in noise metric | `thm:block-locality`, `eq:block-promises`; no dimension factor and no commutativity assumption. Author-stage development strengthens the archived gain-only constant to the scalar sharp-far form by transporting `Cov(X'_s,Z'_s)=Pi_s^-` through the later fresh history. Archived gain-only bound retained as a valid weaker version. |
| Exact far identity and stationary near-factor refinement; prohibited nonstationary extension | `eq:old-scalar-identity`, `eq:far-scalar-identity`, `app:locality-boundaries`; exact three-time `-1/20` witness and invalid proposed `1/32` bound. |
| Stationary minimum gap, rational finite-iteration innovation floor, pair majorants, finite-horizon row-support DP | `prop:spacing-locality`, `eq:spacing-floor`, `eq:spacing-pair-majorant`, `eq:spacing-row-dp`, `eq:spacing-delta`; old and refined pair versions distinguished. |
| Feasible mask count, cooldown when information history is shorter than spacing, exact count and support graph | `subsec:calendar-graph`, `eq:calendar-arc`, `eq:separated-mask-count`; covers L=0, g>L and at-most-singleton edge cases. General side constraints do not automatically preserve the continuous hull. |
| General covariance lower floor/off-diagonal decay, all explicit constants and weighted-conjugation proof | `thm:general-decay`, `eq:decay-constants`, `eq:conjugated-inverse`, `eq:decay-delta`; variable packet dimensions, large diagonal blocks and conservative numerical windows included. |
| Supplied rational block metrics and direct covariance-decay partial-observation corollary | `cor:decay-metric`, `eq:metric-decay-promises`, end of `subsec:general-decay`; metrics are SPD block coordinate metrics, not an unproved arbitrary calendar-distance extension. |
| Partial observation, singular initial/state covariance, covariance transport, Euclidean and intrinsic/normalized bounds | `thm:partial-locality`, `cor:partial-euclidean`, `eq:transport`, `eq:partial-normalized-delta`, `eq:partial-unnormalized`; full range-factorization proof handles unequal fresh histories and avoids all latent covariance inverses. |
| Random-intercept no-decay counterexample; calendar vs last-selected memory and grid refinement boundary | `eq:random-intercept-boundary`, `subsec:calendar-graph`; fixed-window horizon error not bounded at unit contraction. |
| Prior reductions and precise locality/FSAI/Baxter comparison | `subsec:locality-prior`, `eq:diagonal-priority-reduction`; independent dummy-block padding and diagonal normalization proved; no blanket subset-uniformity or unbounded-diagonal novelty claim. Unproved historical direct-sum route explicitly unused. |
| Global KL implies relative precision/Fisher; repeated-pair Kaporin scaling | `app:locality-metrics`, `eq:kl-relative-identity`, `eq:kaporin-pairs`; roots and congruence proved, dimension-root normalization distinguished. |
| Thesis pivot supermodularity and wrong marginal identity; fixed-order convergence counterexample | `app:pivot-supermodularity`, `eq:pivot-witness`, `eq:pivot-supermodularity-slack`; exact precisions and determinant ratios, convention-dependent final bound carefully separated. No attribution to March 2026 Kaminetz–Webber paper. |

## Stage 3 written coverage and final locations

| Development | Actual manuscript disposition |
|---|---|
| Scalar/full-block weighted trace and growing sensitivity rank | `thm:trace-fptas`, `eq:complexity-envelope`, `eq:trace-approximation-ratio`; rational fixed promises, input-sized dimensions and explicit Turing proof. |
| General-covariance-decay and supplied-metric trace schemes | Item 3 of `thm:trace-fptas`, using Stage 2 constants; direct rational-coordinate computation avoids numerical whitening. |
| Intrinsic partial-packet scheme | Item 4 of `thm:trace-fptas`; new rational envelope replaces the square-root constant conservatively by s, with singular latent covariance inherited from accepted locality. |
| Minimum spacing with short information history | Proof of `thm:trace-fptas`; explicit cooldown/count/mask product, gap clamp to n+1, exact mandatory/forbidden/cardinality feasibility; polynomial even with input-sized gap. This is a developed strengthening of the original cardinality-only scheme, not a generic resource-budget extension. |
| Individual-channel hardness | `prop:channel-hardness`; cubic graph covariance I+A/12, condition number 5/3, scalar gap 1/9, isotropic noise and B0=1. Mohar primary complexity source credited; no first-hardness claim. |
| Scalar Mahalanabis–Stefankovic prior reduction | `app:scalar-prior`, `eq:gmrf-runtime`, `eq:gmrf-regularization`, `eq:gmrf-condition`; focused recurrence adaptation, singleton target bag avoids printed local inverse/block-order defect, normalization, regularization, width and objective conversion complete. No first scalar FPTAS claim; predecessor rounding model explicitly distinguished from our rational theorem. Cardinality-only padding scope retained. |
| Fixed-p determinant scheme and all-rank spectral strengthening | `thm:dag-spectral-set`, `lem:spectral-normalization`, `eq:spectral-cover`, `eq:dag-cover-size`; one common full normalization proof, all actual feasible paths, signed floor DP, exact ranges, all boundary cases and bit bounds. Determinant-only predecessor result is subsumed without duplicated proof. |
| D/E/conventional A/estimable contrasts; objective-independent reuse | `subsec:spectral-consequences`, `cor:true-spectral-cover`, `eq:true-spectral-cover`; determinant rather than multiplicative logdet, algebraic eigenvalue comparison, common-kernel inverse bounds, added common prior/congruence and true covariance transfer. |
| Rational represented matroids | `thm:matroid-spectral-set`, `app:matroid-proof`, `eq:matroid-owner-marker`, `eq:matroid-profile-polynomial`; rank-preserving restriction, forced-owner marker, full positive coefficient/interpolation/deletion proof and exact witnesses, cached Bird determinant evaluation, q input-sized and p fixed. Berstein algorithm credited; no oracle/finite-field/intersection/history-matroid generalization. |
| Spectral priority audit | `subsec:matroid-cover`; Pareto/profile predecessors, Brown PTAS normalization, Filova–Somogyi–Harman PSD atom reduction, covariance pruning, multiplicative lower envelopes, spectral coresets, projected vertices and fixed-decision-dimension distinctions. Specific combined cover novelty qualified. |

Stage 3 mathematical development is fully written. Large-polynomial spectral
schemes are theoretical, with tiny exact proof tests, not an implemented
large-instance solver. The portable `supplement/checks/stage03.py` imports
explicitly included local audit helpers without invoking their historical output
routines or requiring the original repository.
The final subsection of `app:matroid-proof` also preserves the repository's
exact mixed-determinant cancellation, F2/Q independence, unattainable projected
integer profile, and growing-label-count oracle-model scope witnesses.

## Stage 4 written coverage and final locations

| Development | Actual manuscript disposition |
|---|---|
| Prior-aware finite-history global certificates | `thm:local-certificate`, `eq:local-certificate`, `subsec:local-certificates`; arbitrary SPD reference, true incumbent lower bound, weighted-trace variant including partial packets, exact path feasibility and whole-graph support. |
| Rational arithmetic and signed interval scoring | `app:certificate-arithmetic`, `eq:rational-log`, `app:integer-scores`, `eq:integer-arc-bound`; signed products/squares, positive variance floor, indefinite-weight clamp, distinct statistical/arithmetic floors, count/cooldown and path-length loss. General blocks use rational inverses, not an unproved entrywise inverse bound. |
| Dense Liu / virtual-noise scalar and diagonal family | `prop:vn`, `eq:vn-resolvent`, `eq:vn-covariance`, `eq:vn-gradient`; binary and zero-weight identities, PSD split boundary, Hainy Proposition3 equivalence and heteroscedastic modified-split mapping. |
| Exact continuous lower and upper bounds | `eq:vn-continuous-certificate`; rational split/gradient/support, upper tangent at any cube query, continuous lower bound only at feasible query, solve error separated from integrality gap. |
| Structured precision and repaired covariance oracle | `app:dense-oracle`, `eq:dense-tridiagonal`, `eq:split-tridiagonal-check`, `eq:dense-covariance-filter`, `eq:dense-reverse-adjoint`; complete algebra/adjoint proof, field-operation/storage counts, precision conditioning and initial RTS residual-subtraction failures distinguished. |
| Every scalar split, spectral limit | `eq:scalar-barrier` and exact tridiagonal nonpositive-pivot/general Rayleigh witnesses; inadmissible reference used only for its value. |
| Every diagonal split, pointwise optimization, all affine upper cuts | `prop:diagonal-barrier`, `eq:diagonal-barrier`, `eq:pointwise-split-barrier`, `eq:dual-repair`; full convexity/weak-duality proof, arbitrary positive reference, rational PSD repair, no minimax interchange. `ex:split-barrier` gives log(4/3) gap. Positive chemical and negative synthetic probes appear in `subsec:scalar-experiments`. |
| Raw/standardized finite-scenario bounds | `eq:robust-objectives`, `eq:robust-support`, `prop:robust-normalizers`, `eq:robust-certified-interval`; one common price, exact nonnegative simplex, correct optimal-normalizer interval directions, common feasible family, scale invariance and determinant-root efficiencies. |
| Robust spectral corollary | `cor:robust-fptas`, `eq:robust-cover-factor`, `app:robust-witnesses`; fixed qp, exact determinant comparisons, a-squared factor with sharp tie example, shared-versus-separate-price and common-mixture gap. |
| Exact latent representation and support certificate | `eq:separator-model`–`eq:separator-schur`, `eq:schur-variational`, `eq:separator-gradient`, `thm:separator-certificate`; SPD latent scope, correct nuisance prior, rank-p gradient, arbitrary W/G, count-constrained pattern DP, full-schedule hull rather than expected-count-only mixtures. |
| Nested-anchor hierarchy | `thm:separator-hierarchy`, `eq:separator-cross-identity`, `app:separator-hierarchy`, `eq:anchor-joint-quadratic`; all Gaussian prior cross terms and complete elimination proof, common-mixture Loewner ordering, strict hierarchy and rational empty-anchor hull-gap examples. Nonnested/unfinished numerical bounds not ordered. |
| Singleton baseline and bridges | Singleton subsection of `app:separator-hierarchy` proves actual diagonal VN equivalence, including singular R-D and zero weights; last unanchored point in b=1 convention explicit. `app:stationary-bridges`, `eq:bridge-loadings`, `eq:bridge-covariance`, `eq:bridge-transition`, `eq:anchor-prior-score` give signed endpoint/bridge/reset/sparse-prior formulas. |
| Prior comparison | Liu/Pazman/Hainy, Kim, Rybicki/Press, Särkkä/Svensson, Burclova/Pazman, Maus, Duarte/Sagnol/Wong, Wang/Yue, Chowdhary/Attia/Alexanderian, Sagnol/Harman, Harman/Trnovska, Filova/Somogyi/Harman, Alexanderian etal, Levine/How, Balas, Papageorgiou/Trespalacios credited. Only the precise nested Markov-anchor hierarchy receives a qualified novelty statement. |

Stage4's new self-contained `verification/stage04/check.py` imports only standard
Python and SymPy, not historical producer/certifier modules. Its 1,537 exact
checks cover literal resolvents, covariance/adjoint identities, binary log
tangents, dual repair, all-diagonal toy bounds, all tiny separator subsets,
signed bridges, interval scores and robust factors. No historical output was
overwritten. `sec:computation` and the portable supplement contain the numerical
tables, saved-certificate replays, and matched fresh studies.

## Stage 5 written coverage and final locations

| Development | Actual manuscript and supplement disposition |
|---|---|
| Public-source correction and all criterion rankings | `subsec:source-computation`; new `supplement/source_kinetics/` exact generator and independent full-covariance checker. All 2347 schedules, 14,082 exact objective equalities and 33 criterion-budget comparisons; all 66 formula-specific optima unique. D and conventional A agreement is now exact. |
| Six scalar synthetic and four kinetic certificates; fixed/all scalar splits | `subsec:scalar-experiments`, `tab:scalar-separations`; all ten common rational input models, exact true-design gaps, tightly bounded continuous solve error and all-scalar separations. Early timed OA results explicitly superseded for strength assessment, not hidden. |
| All-diagonal positive chemical / negative synthetic | `eq:kinetic-diagonal-separation`; unsuccessful proposals, rational dual repair, complete scoped barrier and separate proposal/certificate cost. Synthetic negative remains a failed fixed-point witness only. |
| Analytic kinetics and independent numerical sensitivities | `eq:computational-kinetics`, `eq:kinetic-sensitivity-row`, `app:computational-models`; independent 12-state balance/sensitivity ODE and 70-digit matrix exponential checks; finite decimal certification scope and rate-swap ambiguity retained. |
| Spacing, far-pair refinement and integer intervals | `subsec:packet-experiments`; original36.609s certificate,1e-8 interval loss,1.087s integrated timing,31,900arc comparison and refined .00972559 gap. Same incumbent; old/new records separate. |
| Complete-packet limitations and new block improvement | `subsec:packet-experiments`; d4/d16 numerical negatives and equal greedy designs; new Stage2 bound compared at the same promises; separate fresh n8,d3,56-schedule exact certificate in `supplement/results/fresh-all.json`. |
| Partial observation trace | `eq:two-mode-probe`, `subsec:packet-experiments`; four normalized exact relative gaps below .0604%, faster/wider numerical dense comparison, 96/late iteration cap, original weaker/L6 dispositions. |
| Finite-scenario robust original/polished/dense/nominal | `subsec:robust-experiments`, `tab:robust-certificates`; three exact intervals, all scenario/normalizer costs, separate dense-rounding polish, mixed earlier winners, returned-neighborhood status, corrected weights, continuous-region exclusion. |
| Fixed physical grid limits | `eq:fixed-physical-covariance`, `tab:physical-grid`; exact rational nesting, k16 fixed, primary first-price timeouts, separate96L12 diagnostic, numerical refined transfer, sufficient-not-necessary windows, softtime/workspace caveats. |
| Five separator certificates and all timings | `tab:separator-certificates`; exact endpoints, n192b16 accounted38.023s and missed .01 target, nonnested12/16 partitions, shared incumbents and exact arbitrary-witness scope. |
| New matched nested-anchor experiment | `subsec:nested-experiment`, `tab:nested-fresh`; common56 schedules, same exact optimum incumbent, four nested anchor sets,224 independent exact Schur identities, exact mixture lower/support upper intervals, dense and calendar comparison including δ≥1 failure; no expected-count-only relaxation substituted. |
| Portable self-contained supplement | `supplement/README.md`, `validate.py`, `replay_certificates.py`, `validate_models.py`, `fresh_experiments.py`, `reproduce.py`, dependencylock and159-file frozen manifest. No original-repo imports, /tmp checkout dependency, commercial verifier or third-party literature PDFs. |

Every principal saved exact certificate is replayed (46 total). The source
rankings, proof fixtures, independent model validation and fresh block/nested
checks are separate, meaningful validation layers. Historical internal reviews
remain provenance rather than manuscript scientific citations. Large-exponent
spectral algorithms are explicitly theoretical and not benchmarked as practical
solvers. The integrated framing and package map are recorded below; review
completion is tracked separately in `PROCESS.md`.


## Stage 6 integration and final package map

| Material | Actual location and disposition |
|---|---|
| Standalone abstract and problem motivation | `sections/00-introduction.tex`, `sec:introduction`; selected-covariance target, discrete resource decisions, global certificate and efficiency interpretation. |
| Prior-work synthesis | `subsec:intro-prior`, `tab:prior-contributions`; inherited statistical/localization/conic/profile machinery and precise developed results. Detailed source-version limits remain in the bibliography and this process folder. |
| Contributions and assumption roadmap | `subsec:intro-results`; explicit locality constants and rational trace FPTAS, all-target two-sided PSD cover with exact ranges, split-family witnesses, finite-scenario certificates, nested changing-anchor hierarchy. Qualified priority claims retain the explicit representation restrictions. |
| Practical synthesis and limits | `sec:discussion`; continuous solve error versus locality error versus integrality, positive all-split separation, negative complete-packet/grid findings, full separator costs and finite-scenario scope. No universal solver dominance, physical validation, or giant-spectral-set benchmark claim. |
| Conclusion and data/code availability | `sections/06-discussion.tex`; complete scientific conclusion and accompanying-supplement availability without an invented public archive URL or authorship metadata. |
| Build and distribution guide | `README.md`; standalone manuscript source file set, clean rebuild command, independent supplement validation/reproduction guide and source-data provenance. `main.tex` has an anonymous author block and all sections integrated. |
