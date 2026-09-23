# Priority audit: Markov information paths and correlated experimental design

Date: 2026-09-12. Bounded primary-source audit by the design-opportunities
research agent. This note supersedes the novelty assessment in
[the initial opportunity note](research-20260912-design-opportunities.md).
It separates mathematical equivalence from publication-priority uncertainty.
The [independent review](research-20260912-markov-theory-independent-review.md)
checks the original mathematics; it did not perform this literature audit.

The central proposed information-graph hull is already known through a direct
linear image of Lee, Gómez, and Atamtürk's principal-inverse hull. The different
innovation direction does not change its fractional relaxation. Singular
transitions are a routine continuity extension, not a credible substantial
contribution. Count layering, path pricing, logdet support duality, and generic
Frank–Wolfe branch-and-bound also do not presently support a new theory claim.
Keep investigating the solver only if it can establish substantial useful
improvements, or if another nonroutine advance emerges.

## 1. Decisive primary source and source locations

Jisun Lee, Andrés Gómez, and Alper Atamtürk, *Convexification of multi-period
quadratic programs with indicators*: [arXiv:2412.17178](https://arxiv.org/abs/2412.17178)
(first posted 2024-12-22), published in *Mathematical Programming*,
[DOI 10.1007/s10107-026-02379-5](https://link.springer.com/article/10.1007/s10107-026-02379-5)
(2026-07-22). Both primary HTML versions and the 37-page preprint PDF were
inspected. The published numbering differs from the preprint.

Their scalar construction is in §3.2, equations (14), preprint Propositions
4–5; its block version is §3.3, equation (18), and Theorem 8 in the preprint
(Theorem 2 in the published version). It represents the convex hull of padded
selected-principal inverses using continuous ordered-path flows and binary
node visits. The published Proposition 6 gives binary-visit uniqueness.
The paper also supplies shortest-path optimization and conic reformulations
with side constraints. Its motivating objective is indicator quadratic
optimization rather than experimental design.

The following sections give our explicit mapping to the proposed model. They
are an equivalence analysis, not a newly claimed hull theorem.

## 2. Exact mapping for nonsingular transitions

Let a complete observed Gaussian error chain have block dimension `r`, marginal
covariances `P_i>0`, and transitions `e_j=Phi_ji e_i+eta_ji`. Suppose its
one-step transitions are nonsingular. Write `T_1=I` and `T_i` for the product
of transitions from time 1 to time `i`; then `Phi_ji=T_j T_i^{-1}`. Its full
covariance `R` has, for `i<=j`,

```text
R_ij = P_i Phi_ji^T = P_i T_i^{-T} T_j^T.
```

Set `U_i=P_i T_i^{-T}` and `V_i=T_i`. Then `R_ij=U_i V_j^T`, exactly the
block-factorizable class in the cited formulation. Positive definite initial
and innovation covariances ensure `R>0`. All selected block principal
submatrices are therefore positive definite.

Let `E_S` select the full blocks indexed by `S` and define the padded inverse
`K_S=E_S^T(R_SS)^{-1}E_S`. With stacked fixed mean sensitivities `F`, information
is `J(S)=J0+F^T K_S F`. Consequently the affine map

```text
(z,K) -> (z,J0+F^T K F)
```

takes `conv{(1_S,K_S)}` exactly to `conv{(1_S,J(S))}`. Affine maps commute with
finite convex combinations, giving both inclusions without an additional
assumption about the design criterion. This directly disproves priority for
the proposed information-graph hull. Independent chains use products of these
flow sets and summed information; adding installation or budget constraints
preserves integer exactness but does not create a new hull theorem.

## 3. Forward and reverse innovations give the same fractional formulation

The proposed model assigns a first-marginal information matrix to a source
arc, forward conditional information to each selected gap, and zero to a sink
arc. The prior formulation's padded inverse expansion uses reverse
conditional information and a final-marginal term. Here is a direct
comparison independent of factorization notation.

For `i<j`, let `C_ij=Cov(e_i,e_j)`, and define

```text
A_i = F_i^T P_i^{-1} F_i,
Phi_ji = C_ij^T P_i^{-1},
Omega_ji = P_j-C_ij^T P_i^{-1} C_ij,
B_ij = C_ij P_j^{-1},
V_ij = P_i-C_ij P_j^{-1} C_ij^T.

W_forward,ij = (F_j-Phi_ji F_i)^T Omega_ji^{-1}
               (F_j-Phi_ji F_i),
W_reverse,ij = (F_i-B_ij F_j)^T V_ij^{-1}
               (F_i-B_ij F_j).
```

Computing the two-observation information by either Schur complement gives

```text
A_i+W_forward,ij = W_reverse,ij+A_j,
W_reverse,ij-W_forward,ij = A_i-A_j.                 (A)
```

Under §2's factorization, `B_ij=U_i U_j^{-1}`, so the reverse expression is
the sensitivity congruence of the cited arc coefficient. Equation (A)
telescopes on an ordered path: forward source plus gap contributions equal
reverse gap plus sink contributions. It also telescopes on every fractional
flow because inflow equals outflow at each internal vertex. Thus the two
formulations yield identical information at every common flow, not just at
integer solutions. Reversing the innovation convention cannot strengthen
the existing relaxation.

## 4. Singular-transition boundary

The formulas in §3 use marginal and innovation inverses, never transition
inverses. They remain well defined when one-step transitions are singular,
provided initial and innovation covariances remain positive definite.

One should not apply the square-factor representation from §2 literally at
this boundary. If square `U_i,V_i` satisfy `U_i V_i^T>0`, both are nonsingular;
then every `U_i V_j^T` is nonsingular. A covariance with a zero cross block,
including independent observations, cannot have that representation. The
cited paper's broad discussion of inverse block-tridiagonal structure should
therefore be read with its factor and inverse assumptions in mind. Our
equivalence uses the explicit sufficient mapping in §2, not an unrestricted
interpretation of that discussion.

This boundary is still no substantial novelty opportunity. Perturb each
singular transition by a generic vanishing multiple of the identity so that
every perturbed transition is nonsingular; keep the initial and one-step
innovation covariances positive definite and fixed. The generated covariance
`R_epsilon` converges to `R`. There are finitely many subsets, and inversion is
continuous at each positive definite selected covariance. Therefore all graph
vertices `(1_S,K_S(epsilon))` converge to `(1_S,K_S)`. The underlying bounded
flow polytope is common to the perturbations, while its reverse coefficients
in §3 converge. Taking limits gives the same flow representation at singular
transitions. This is a direct continuity corollary, consistent with the exact
rational singular-transition check in the independent review.

## 5. The two dense correlated-design bounds are identical

[Pázman, Hainy, and Müller (2022)](https://arxiv.org/abs/2103.02989),
*A convex approach to optimum design of experiments with correlated
observations*, [DOI 10.1214/22-EJS2071](https://doi.org/10.1214/22-EJS2071),
is a direct D-optimal comparator. Its primary preprint §2.3–2.5 was read.
For a target of `k` points, it uses weights `0<=xi_i<=1/k`, `sum xi_i=1`,
with virtual variance `a(1/k-xi_i)/xi_i`. Set `z_i=k xi_i`. On positive
coordinates its covariance is

```text
R+a(diag(1/z)-I) = S+a diag(1/z),  S=R-aI>0.
```

Woodbury gives

```text
(S+a diag(1/z))^{-1}
 = S^{-1}-S^{-1}(S^{-1}+diag(z)/a)^{-1}S^{-1}.
```

After congruence by `F` and adding the same prior, this is exactly the Liu
scalar-split extension in equation (4) of the opportunity note. Continuity
extends the identity to zero coordinates. The paper uses a cutting-plane
bound and constructs integer designs through rounding/sampling. Thus the
dense OA baseline has a direct statistical-design interpretation, and the
strict rational example compares against this virtual-noise bound as well.
This is an algebraic equivalence found in the audit, not a claim of priority
for either source's result. [Liu et al.](https://arxiv.org/abs/1508.03690)
is the earlier source of the expression used in our implementation.

## 6. Older sampling work and algorithmic comparators

| Work and inspected material | Consequence |
| --- | --- |
| [Dette, Pepelyshev, and Zhigljavsky, arXiv:1501.01774v2](https://arxiv.org/pdf/1501.01774), 38 pages, §§1–3, Appendix B, and references; published DOI 10.1214/15-AOS1361 | Triangular covariance kernels, continuous-time BLUE and asymptotic signed/matrix-weighted designs are established. Its finite designs approximate those constructions. It does not supply the constrained path solver sought here. |
| Patan and Bogacka, [CSDA 2007, DOI 10.1016/j.csda.2007.05.030](https://doi.org/10.1016/j.csda.2007.05.030), metadata and abstract only | Chemical-kinetics measurement schedules with correlated multivariate errors are a close application predecessor. Full algorithm comparison remains unresolved. Authors are Maciej Patan and Barbara Bogacka. |
| Uciński and Atkinson, [SNDE 2004, DOI 10.2202/1558-3708.1217](https://doi.org/10.2202/1558-3708.1217), metadata/abstract and reference trace only | Another close chemical-kinetics predecessor and English account of the Brimkulov–Krug–Savanov procedure. Unread full text must not be classified as a globally exact algorithm. |
| Brimkulov, Krug, and Savanov, 1986 Russian book *Design of Experiments in Investigating Random Fields and Processes*, Nauka, Moscow; bibliographic trace only | Historical correlated-design algorithm. The original source remains unread. “Exact design” means discrete observations and does not itself mean globally certified optimization. |
| [Uciński, Measurement 2020](https://www.sciencedirect.com/science/article/pii/S0263224120304115), DOI 10.1016/j.measurement.2020.107873, primary abstract/introduction | Its correlated D-optimal criterion concerns the OLS estimator covariance. It uses majorization-minimization, simplicial decomposition, randomization, and exchange. It is related solver work, but a different estimator objective from the Fisher/BLUE model here. |
| Uciński, [A-optimal fast exchange, 2025](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5167525), DOI 10.1016/j.measurement.2025.117794, abstract only | Potential stronger correlated-design incumbent method; full algorithm and objective scope require reading before implementation or claims of dominance. |
| [Ahipaşaoğlu, Cipolla, and Gondzio, 2026 column generation](https://link.springer.com/article/10.1007/s12532-026-00326-1), primary §3.2–3.3 | Established logdet support generation, dual pricing, and integer-design approximation. Its columns are ordinary candidate design vectors. Our whole-path matrices change the pricing set; generic column generation is not a new mechanism. |
| [Hendrych, Besançon, and Pokutta, arXiv:2312.11200](https://arxiv.org/abs/2312.11200) | Frank–Wolfe branch-and-bound for mixed-integer experimental design is an essential algorithmic comparator, already identified in the original note. |
| [López-Fidalgo and Wong, 2026 review](https://www.annualreviews.org/content/journals/10.1146/annurev-statistics-042324-012947), DOI 10.1146/annurev-statistics-042324-012947, abstract/reference list | Useful current source map. Its broad comments about gaps in available algorithms do not establish novelty of a specific proposal. |

The Dette introduction names Brimkulov–Krug–Savanov but its inspected arXiv
reference list does not supply the book entry. The Pázman–Hainy–Müller primary
paper §3.1 instead gives a concrete bridge: its BKSF comparator uses an
approximate sensitivity exchange rule, and the original BKS rule compares
objective values directly. Its appendix describes BKSF. This makes a
greedy-only computational comparison too weak. The CSDA2007 full text was not
retrieved during this bounded audit, so tracing its own references remains
open rather than presumed complete.

The principal-inverse framework also predates Lee's path specialization:
[Wei, Atamtürk, Gómez, and Küçükyavuz](https://doi.org/10.1007/s10107-023-01982-0),
*On the convex hull of convex quadratic optimization problems with indicators*,
defines the general principal-inverse polytope and gives associated hull
representations. Its existing local full text and note were inspected at
`literature/papers/wei2023-on-the-convex-hull-of/`. No duplicate KB entry is
needed. This strengthens, rather than weakens, the priority disproof.

## 7. Unknown parameters and non-Gaussian models: useful scope, weak novelty

A regular fully observed Markov family's gap likelihood factors give additive
expected Fisher information. This requires Markov structure in a parameter
neighborhood, differentiation under the integral, and square-integrable scores.
Conditional scores have mean zero given prior observations; all cross terms
therefore vanish. The expected gap information depends on its two endpoints
and the fixed underlying model. It does not depend on which earlier points
were selected when sampling does not intervene on the process.

This reasoning is established statistical machinery. As a concrete earlier
example, [Pagendam and Pollett, *Locally optimal designs for the simple death
process*](https://people.smp.uq.edu.au/PhilipPollett/papers/LOptimal.pdf), §2,
factors the complete-observation likelihood and obtains a sum of gap Fisher
terms. [Baran, Szák-Kocsis, and Stehlík](https://arxiv.org/abs/1704.05719),
*D-optimal designs for complex Ornstein–Uhlenbeck processes*, DOI
10.1016/j.jspi.2017.12.006, studies mean and covariance-parameter design,
including gap-based information expressions. Neither a non-Gaussian label nor
unknown correlation parameters makes the additive identity new.

For implementation planning, an explicit full Gaussian Fisher arc can still
be useful. Let the gap conditional distribution be

```text
Y_j | Y_i ~ Normal(m_j+A(Y_i-m_i), Q),
Cov(Y_i)=P_i,
```

where all quantities may depend on the local parameter `theta`. For parameter
coordinates `a,b`, put `d_a=m_{j,a}-A m_{i,a}` and `A_a=partial A/partial theta_a`.
The expected gap Fisher entry is

```text
I_gap,ab = d_a^T Q^{-1} d_b
         + trace(Q^{-1} A_b P_i A_a^T)
         + (1/2) trace(Q^{-1} Q_a Q^{-1} Q_b).          (B)
```

To derive (B), differentiate the conditional mean with the observed `Y_i`
held fixed: the derivative is `d_a+A_a(Y_i-m_i)`. Apply the Gaussian
conditional Fisher formula and then average over `Y_i`; its centered mean
removes cross terms and its covariance is `P_i`. The covariance-score and
mean-score cross terms are zero for a normal conditional distribution. The
first-marginal Fisher term is the usual mean term plus
`trace(P_i^{-1} P_{i,a} P_i^{-1} P_{i,b})/2`. This is a derivation for future
verification, not an implemented or independently reviewed extension.

The resulting PSD matrices fit the same generic additive-path optimization
machinery. A useful implementation could jointly estimate kinetic and noise
parameters, but a publication claim would need an important unresolved design
problem and strong solver evidence. Merely substituting (B) into the path
lift is a routine extension.

Partial/noisy observations are a genuine harder boundary. The observed
process need not be Markov even when a latent state is Markov. The nugget
counterexample in the opportunity note proves the failure directly.
[Eshragh, Skerritt, Salvy, and McCallum, PLOS One 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0328707)
provides a concrete partially observed birth-process design problem and a
different Fisher computation; it is not solved by the proposed finite-memory
arc identity. No solution to this boundary is claimed here.

## 8. Search record and unresolved sources

All searches below were performed on 2026-09-12. The record is a bounded
query/source trail, not an exhaustive database search or evidence of absence.

| Query or source-tracing step | Outcome |
| --- | --- |
| `"principal submatrices" "inverse" "convex hull" "path"` and inspection of general inverse-hull work | Decisive Lee/Gómez/Atamtürk prior formulation; checked preprint and published §3–4. |
| `"Markov" "optimal design" "shortest path"` | Broad search produced mostly irrelevant MDP/path work; no priority inference drawn. |
| `"correlated" "experimental design" "dynamic programming" "convex hull"` | No additional decisive primary source; Lee already resolves the central claim. |
| `"optimal design" "whole designs" "column generation"`; direct 2026 column-generation reading | Ordinary logdet support generation is established; whole-path pricing is the application-specific component. |
| `"Optimum experimental designs for dynamic systems" "Patan" pdf` | Verified Patan/Bogacka metadata; no lawful full text recovered in this audit. |
| `"Brimkulov" "Krug" "Savanov" design 1986` plus Dette and current review references | Identified historical Russian book and the Uciński/Atkinson English account; original work unread. Related 1980 paper has conflicting secondary pagination and was not assigned guessed metadata. |
| `"Experimental design for time-dependent models with correlated observations" pdf` | Located 2004 article identifier and chemical-kinetics abstract; full text unresolved. |
| `"A convex approach to optimum design" correlated pdf` | Located arXiv:2103.02989; read the dense convex construction and showed equality with the Liu split. |
| `"D-optimal sensor selection in the presence of correlated measurement noise"` | Followed Pázman–Hainy–Müller's reference to Uciński2020; distinguished its OLS objective from Fisher information. Search also identified the 2025 fast A-optimal exchange source. |
| Dette full-text recovery | arXiv:1501.01774v2 PDF downloaded successfully to `/tmp/minlp-design-opportunities-20260912/dette2015.pdf`; existing KB entry was queued for promotion. |

All new relevant entries and full-text promotions were routed to the sole
literature-maintenance agent `/root/literature`, with parent notification.
That agent owns bibliographic validation, lawful retrieval, the KB, and the
missing-source report. This audit did not mutate the KB. Outstanding requests
include the Patan/Bogacka2007 and Uciński/Atkinson2004 full texts and the
Brimkulov–Krug–Savanov book. The 1980 BKS article was also requested with
conflicting bibliographic details flagged, together with Fedorov's 1996
*Design of spatial experiments: Model fitting and prediction* chapter,
*Handbook of Statistics* 13:515–553, which supplies the BKSF variant. The
Uciński2020 and 2025 sources were routed as well. Metadata inclusion remains appropriate even if
they cannot be retrieved. Lee's related 2025 thesis
[Multi-Period Quadratic Programs for Hybrid Affine Systems](https://escholarship.org/uc/item/8zs5p5d7)
was also routed as an openly accessible supporting source; its chapter on the
same hull should not be counted as a separate discovery.

The defensible current research claim is an implementation opportunity using
known hull machinery for an important correlated-design problem. The audit
has not found a new publishable theorem. That negative result should be
retained even if later experiments establish a valuable software contribution.
