# Stage 2, round 1: independent review 3

## Verdict

No major issues found in the delivered lower-bound and composition sections. The distributional product uses the relevant primary composition theorem with the correct order of quantifiers; the stronger full statistical-times-exponential product is not claimed. Two minor statement clarifications are listed below.

I read both complete sections, the Stage 2 author record and source-map entries, and the relevant primary source passages. I did not read other review reports and made no manuscript edits.

## Numbered findings and repairs

1. **Minor: exclude constant inner functions when asserting the existence of two fiber distributions.** At `sections/05-composition.tex:81-88`, “for every partial Boolean inner function g, there are distributions mu_0, mu_1 on its two fibers” is false for a constant partial function: one fiber is empty. Ben-David–Blais explicitly assign zero Shaltiel-free complexity in that case. This does not affect the Forrelation applications or any nontrivial lower bound. **Repair:** say “for every nonconstant partial Boolean inner function g”; add the same harmless nonconstant assumption to the conditional and distributional compiler statements, or explicitly dispose of constant g as a trivial zero lower bound before invoking the two distributions.

2. **Minor: put the baseline success probability in every lower-bound theorem statement.** The clock theorem states success probability 2/3, but the statistical lower bound, conditional compiler, distributional scalar product, and high-accuracy path-product statements do not explicitly state it. Their proofs require a bounded-error estimator, and the distributional proof specifically amplifies an assumed baseline success probability. The coherent counting comparison likewise uses constant success probability only in its proof. **Repair:** write “with success probability at least 2/3” in these statements, or give one explicit convention near the start of Section 4 that every lower bound is for worst-case success at least 2/3 unless a different failure parameter is specified. Retain the high-confidence population restriction separately.

## Composition and primary-source verification

The cited local PDFs were checked directly with `pdftotext` under the qipm environment where extraction in the fulltext file omitted displayed formulas.

- `[[david2020-a-tight-composition-theorem-for]] p.16`: Definition 22 uses the **minimum** of the two expected query costs divided by squared Hellinger distance; Definition 23 maximizes this quantity over the two fiber distributions; Theorem 24 gives `sfR(g) = Omega(R(g))`. This is the stronger inner-distribution property needed here, rather than ordinary bounded-error distributional hardness alone.
- `[[david2020-a-tight-composition-theorem-for]] p.25-26`: Definitions 33–34 specify conditional independent copies and compR; the minimax observation permits an outer mixing distribution. The proof of Theorem 35 fixes a pair witnessing sfR before constructing the outer simulation. Equation (3) and the cost summation on p.26 establish the claimed fixed-pair lower bound. Thus choosing the scalar threshold from the expectations under that pair is legitimate, and does not change the pair after selecting the outer distribution. The source explicitly allows partial outer functions and expected query costs.
- `[[chakraborty2023-on-the-composition-of-randomized]] p.4 and p.11`: Theorem 2 permits partial outer and inner functions and gives the full product when the outer randomized complexity is linear in its arity. Observation 23 is indeed `noisyR(F) = Omega(R(F)^2/M)`. The manuscript invokes these results within their hypotheses.
- Montanaro–Shao, arXiv:2311.06999, Theorem 1.8 and Section 5.1, checked in the primary PDF extraction `/tmp/qipm-ms.txt`: the approximate-degree numerator, denominator, additive `tau/4` output error, weighted-clock construction, and the two-function Forrelation promise agree with the imported statement. The manuscript additionally proves the full-SQ simulation and LP transfer; it does not attribute those additions to the matrix-function theorem.

### Distributional scalar product

With `n >= 200`, the two outer weights lie in `[0.38M,0.62M]` and differ by `48 sqrt(M)`. Before a sufficiently small constant fraction of the bits are queried, both hypergeometric success probabilities remain uniformly bounded away from zero and one, and the per-query KL divergence is `O(1/M)`. Thus the central two-sphere function has `R(F)=Theta(M)`, uniformly in n. The corrected lower bound n>=200 matters; merely checking that both weights are integers in `[0,M]` would not suffice.

The Hoeffding event uses tolerance `6 Delta/sqrt(M)` for variables in `[-1,1]`; its failure is bounded by `2 exp(-18 Delta^2)`, less than 0.004 for `Delta >= 0.59`. The scalar mean separation is `S=48 Delta C/sqrt(M)`, so that tolerance is `S/8`. Also `S > 14 epsilon d`, while every realized scalar is below `3d`. Therefore the amplified estimator and concentration together give error below 1/3 for the fixed-distribution composed decision problem. Independence is only needed conditional on the outer string, and the proof conditions correctly.

### Conditional high-contrast compiler

For fixed absolute gamma, C1 and C2, the chosen `M=Theta(D/epsilon^2)`, `t=Theta(M/D)` and `Delta=Theta(epsilon M/D)` have `tM/Delta^2=Theta(M)`. For sufficiently small absolute epsilon the rounding constraints and `Delta<=t/4` hold uniformly for `D>=1`. The relative scalar intervals are separated by choosing C1 sufficiently large. Thus Theorem 2 applies. The subsequent narrow-level conditions correctly distinguish relative half-width from an absolute half-width measured against q1.

## Remaining mathematical checks

- Verified polarization constants, public spectral pads, the gauge identity, and hidden-input-independent norm/sampling tables. The claim is a hidden-query lower bound with free public preparation, and this limitation is explicit.
- Checked the box factor `B B^T=H`, its sparse transpose as a constraint factor, analytic-center uniqueness and decrement normalization. The factors use individual gates rather than cumulative circuit products.
- Checked the contraction-preserving dyadic rounding and resolvent bound: their product gives coefficient perturbation at most `3 tau/256`. The rational `3/5,4/5` polarization constant, LDL pivots, and four-square Gram realization are consistent. No polynomial preprocessing or bit-complexity claim is smuggled into that result.
- Checked the stopped hypergeometric proof, including the support-singularity safeguard and stopping probability. Checked both population regimes for the statistical lower bound, and the Bernoulli high-confidence argument with its explicit population threshold.
- Checked the coherent counting upper and lower scales and the stated canonical oracle-completion restriction.
- Checked the witness minimax phase, signed barycentric annihilation, spectral-measure realization of the second and penultimate coordinates, and partial-fraction calculation of the common diagonal. The resulting contrast is constant times c, not kappa times c.
- Checked constant-path endpoint formulas, the relation `n=3(ell+1)` to an actual growing Forrelation circuit, the high-accuracy regime, and the outer `Theta(kappa^2)` block count. The prefactor decreases admissible hard-circuit length at fixed accuracy, as the text now says.
- Checked cyclic dilution, the exact two-cluster inverse, and the Schur-complement condition-number lower bound. The condition-budget maximization is valid because its logarithm is convex in `sqrt(K0)`. These are correctly framed as limits of specified constructions, not general impossibility theorems.
- The source-map treatment of the separate winner-finding/small-success note is appropriate: no unsupported transfer to scalar averaging is made. Existing approximation and composition engines are attributed. Stage 2 does not contain an unsupported first-of-its-kind novelty assertion.

## Diagnostics

`/workspace/local-home/miniconda3/envs/qipm/bin/python scalar-newton-paper/checks/check_lower_identities.py` passes all 25 witness Jacobi realizations and 25 constant paths. This supplements the algebraic checks and is not used as their proof.
