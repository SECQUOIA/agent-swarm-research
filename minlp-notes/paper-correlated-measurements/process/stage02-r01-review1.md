# Stage 2 independent review 1

Scope: `sections/02-locality.tex` and `appendices/locality-scope.tex`, with the accepted foundations, macros, and Stage 2 coverage map as dependencies. Main focus: scalar and complete-block bounds, the strengthened far-pair estimate, and exact Markov path/principal-inverse equivalence. I did not read other reviewers' reports or modify the manuscript.

## Verdict and findings

**No MAJOR findings. No MINOR findings requiring correction.** The stage is mathematically coherent within its stated scope. I recommend acceptance of this stage, subject to the parent agent's assessment of the other independent reviews. This is not a claim of formal verification or an exhaustive literature novelty proof.

## Reconstructed arguments

- `sections/02-locality.tex:16–74`: the completely observed Markov information is exactly a sum of first-marginal and consecutive-gap matrices. For nonsingular transitions, choosing `U_i=P_i T_i^{-T}` and `V_i=T_i` gives the required block-factorizable covariance. The two-packet Schur identity gives the displayed forward/reverse potential difference. Summing it under flow conservation works for fractional flows as well as paths. The perturbation argument is legitimate because fixed positive initial and process covariances keep the limiting observation covariance and all nonempty gap covariances positive definite. The graph's flow polytope is finite and bounded independently of the perturbation. The text does not invert singular transitions.
- `sections/02-locality.tex:117–201`: the transfer lemma uses the equal spectra of `BB^T` and `B^TB`, so its factors are `1±delta`, as stated. Adding a positive-semidefinite prior preserves the claimed bounds without a positive prior floor. I recomputed the near geometric sum and the combination of generic far/near sums. The symmetric scalar matrix of block norms legitimately gives the operator-norm row bound even for unequal block dimensions.
- `sections/02-locality.tex:229–275`: the fresh scalar filter must start from an unconditional marginal, and the manuscript does this. For an excluded old observation the exact transported covariance includes the product of the actual local-history attenuation factors. For a far residual, the initial cross covariance is the earlier local prediction variance, rather than its innovation variance; measurement noise at the earlier endpoint is independent of the state. This establishes the sharper far identity. The stationary near improvement is used only where the target history is nonempty and hence has first gain exactly `P/(P+r)`.
- `sections/02-locality.tex:298–347`: whitening by each observation-noise covariance makes every complete-observation gain symmetric with norm at most `kappa`. All later transition/update products can be bounded by submultiplicativity; no commutativity is needed. Crucially, for a far pair all target-history observations occur after the earlier residual. Consequently the transported initial covariance really is `Pi_s^{-,s}`, whose norm is bounded by the unconditional marginal promise. The newly strengthened complete-block far bound is sound. The final block-orthogonal residual congruence correctly transports the normalized residual norm back to original coordinates.
- `sections/02-locality.tex:355–424`: a history for a selected target contains at most `floor(L/g)` observations. Replacing its gaps by `g` and filling missing observations yields a lower innovation-variance bound because the stationary Riccati gap map increases in both its input and the gap. The finite distance-pricing recurrence upper-bounds each row without claiming simultaneous attainability of all pair majorants.
- The general-decay proof, intrinsic partial-packet transport proof, graph construction, and prior-art reductions were also read for consistency. In particular, the weighted-conjugation proof does not need an upper diagonal bound; the partial-packet proof supplies the required range factorization when latent covariances are singular; and the graph retains a cooldown state when the information window is too short to enforce spacing.
- `appendices/locality-scope.tex`: differentiating the conditional Gaussian mean while holding the observed left endpoint fixed gives the stated derivative and all three expected gap-information terms. The random-intercept example rules out a horizon-uniform fixed-window bound without strict decay. The global KL implication and the dimension-dependent converse are correctly distinguished. The pivot-set counterexample is separated carefully from the March 2026 article and from the pivot-first greedy conclusion.

## Independent exact checks

I wrote and ran `verification/stage02-review1/check.py` using SymPy rational arithmetic, without importing manuscript producer or archived experiment code. Results are in `verification/stage02-review1/results.json`.

The test uses five two-dimensional latent packets with rational, noncommuting transitions, including one singular transition. It verifies transition contraction by exact 2-by-2 positive-semidefinite tests and constructs the covariance from a stationary latent covariance and positive process covariances.

- Exact far-pair transport identity: 160 selected-subset/window/pair cases.
- Exact sharper far-pair norm majorant, checked through a rational positive-semidefinite squared-norm inequality: the same 160 cases.
- Noiseless direct selected inverse versus forward path information: all 31 nonempty subsets.
- Forward/reverse two-packet information identity: 49 consecutive-pair occurrences across those paths.
- The nonstationary scalar covariance `-1/20` witness: exact verification.
- Random-intercept finite-window information formula: 54 horizon/window cases.

All checks passed. These are finite checks supplementing the reconstructed proofs, not substitutes for them.

## Primary-source checks

I read `literature/AGENTS.md` before using the local knowledge base. I checked the retrieved Lee–Gómez–Atamtürk published full text, especially the principal-inverse path formulation and its block extension in Section 3.3. I also extracted the original PDF pages 20–21 independently to verify the block path representation and published Theorem 2. This supports the manuscript's explicit attribution of the hull to prior work.

Vecchia's local original/extracted Section 3.1 does introduce the conditional-likelihood construction credited in the opening paragraph. Pagendam and Pollett's Section 2 explicitly uses the Markov gap likelihood and expected gap information for the death-process design example cited in the appendix. Finally, the thesis original PDF pages 12–14 contains the claimed marginal identity, Theorem 4.3, and equation (4.10); the manuscript's counterexample targets the actual displayed assertion. The distinct 2026 source uses the cited Kaporin definition and is not charged with that thesis assertion.

The remaining literature comparison is appropriately qualified. In particular the manuscript expressly declines a first-localization claim, explains dummy padding and diagonal normalization, and acknowledges that global Gaussian KL control already yields a relative precision/Fisher bound.
