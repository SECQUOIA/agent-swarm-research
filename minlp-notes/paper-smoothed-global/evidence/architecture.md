# Paper architecture: smoothed exact global optimization beyond convexity

Date: 2026-10-05. Author: principal Opus writing agent. This file proposes
the manuscript's structure, its unifying proof mechanism, the assignment
of developments (IDs from `inventory.md`) to sections, notation additions,
and a cut plan. It is a planning record, not submission text.

It has been reconciled with the root's `integration-decisions.md`,
`integration-contract.md`, `notation.md` (ownership and label prefixes),
`reviews/root-model-early.md`, and Sol's prewriting audits
(`reviews/prewrite-lowrank-sol.md`, `prewrite-sparse-sol.md`,
`prewrite-recourse-sol.md`, `prewrite-two-inertia-sol.md`). Where this file
and a root file differ, the root file governs; differences are listed as
requests in Section 9.

## 1. Thesis

A fixed rational objective `F_0` is perturbed once by a random linear term
`gamma^T x`. The coordinates of `gamma` come from a finite rational law
that is computed from the base instance before sampling. The paper asks
when the **sampled** instance can be solved **exactly on every draw** in
expected polynomial (or fixed-parameter) bit time, without growth,
uniqueness or nondegeneracy promises.

The answer is one mechanism with three structural routes, plus one
contrasting regime:

* **Route A, few negative directions.** Nonconvexity lies in a
  `k`-dimensional factor (negative inertia or a supplied low-rank concave
  part). Search the `k` Fenchel coordinates; solve convex (mixed-integer)
  recourse exactly.
* **Route B, sparse interactions.** The interaction graph has a tree
  decomposition with bags of size `p`. Search bag cells with exact sparse
  dynamic programming on the whole instance.
* **Route C, a small core with tractable recourse.** Fixing `k` core
  coordinates leaves a recourse problem that is solvable exactly or with
  certified bounds under coordinate restrictions: box-stable QP, convex
  polynomial, native-integer, totally unimodular or network-flow recourse.
  In the strongest results only the core is perturbed.
* **Route D, strong noise (contrast).** No width or core parameter. Large
  noise pins most coordinates; the remaining random components are solved
  exactly.

Proved limitations explain which restrictions are intrinsic to the
mechanisms and which are not.

Draft contribution sentence: *for each route we give an algorithm that is
correct on every draw of one base-chosen finite rational law and whose
expected bit work is polynomial in the input length and in explicit
numerical curvature/width/noise ratios, for fixed structural parameters.
The bounds are FPT in Route A (aligned and Gaussian-like noise) and Route C,
and fixed-width polynomial (XP) in Route B, where a proved barrier shows
that the dimension power is intrinsic to the retention rule used.*

## 2. The unified mechanism

The root's `integration-contract.md` states the paper's one explanation:
curvature-corrected refinement preserves global optimizers; independent
linear noise bounds expected retained states; exact closure finishes the
sampled problem; a base-selected finite law pays for an exact fallback on
the same draw. The five obligations below make that explanation precise
and are written once in the counting chapter.

| Obligation | Content | Shared lemmas |
| --- | --- | --- |
| (O1) Semiconcave search | A search space (factor coordinates, bag tuples or core) carries a value function that is coordinatewise `L`-semiconcave (or block/full-Hessian semiconcave) and receives an independent linear tilt from the noise after conditioning on the remaining noise. Nested dyadic meshes, corrected-corner lower bounds, pruning against the incumbent: every optimizer is retained, and each retained cell has a witness within `2E_j` (`4E_j` with certified approximate values). | F1, F12; route-specific oracles |
| (O2) Expected count | Local neighbor comparisons confine each interior coordinate's noise to a fixed interval of length `L h + 4E/h`; independence gives a level-uniform expected count. Adaptive lists are dominated by a deterministic full-grid count. Variants: dependent factor noise (volume lemma), Gaussian weighting, directional counts on simplex faces and order chambers, endpoint transport for binaries. | F2, A3, F14, B6, B8 |
| (O3) Sound closure | A deterministic certificate that, when it passes, yields the exact output on that draw: critical-region containment, best-other-label gap, scalar regions, gradient-sign or LP-exposure face fixing plus a Hessian-modulus test, residual excluded-region containment, competing-label exclusion, an optimal-face certificate for TU/flow recourse, or an objective-value lattice. | route chapters |
| (O4) Good event and finite law | Closure passes by a base-only level `J` outside an event of probability `<= 1/(2B)`: growth tail, active-margin tail, label isolation, fixed-hyperplane tubes, or algebraic tubes. Each continuous estimate transfers to the finite law by bounding the interval components of every axis section. | F3-F8, F13, F5 |
| (O5) Exact completion of exceptional draws | Usually a same-draw fallback with cost `B poly(I + b)`, where `B` depends only on base data, so the grid size is chosen after `B`. Two results need no fallback: the objective lattice of A9 makes the terminal gap exact, and Route D solves its components exactly on every draw. | F9, F10, F15 |

**Template theorem (F16, counting chapter).** Suppose a refinement search
runs through levels `0,...,J`, with `J` computed from base data; every
accepted closure certificate is exact on every draw; the expected work of
each level is at most `Theta (I+1)^c`; the probability that no certificate
is accepted by level `J` is at most `1/B`; and the fallback costs at most
`B (I+b+1)^c`. Then the algorithm is exact on every draw and its expected
bit work is at most `(J+1) Theta (I+1)^c + (I+b+1)^c`.

The proof is one line. Its value is the **precision order** it forces,
which the counting chapter states once and every theorem follows:
fallback budget `B` (base-only) -> `rho = 1/(4B)` -> thresholds (`g_0`,
`tau`, tube radius `delta`, value margin `mu_0`) -> cutoff `J` -> grid size
`M >= max{2^J, C_tail/rho, K/rho, ...}` -> one draw. No earlier quantity
depends on the sampled coefficients.

## 3. The routes in one table

| | Route A | Route B | Route C | Route D |
| --- | --- | --- | --- | --- |
| Structural parameter | `k` = factor rows (negative inertia after normalization); `n_z` for MIQP | `p` = bag size | `k` = core size | `Delta` = max primal degree |
| Search space and value | `a in R^k`, `W(a) = min_x F(x) + (alpha/2)||a - Tx||^2` | bag tuples, conditional value over the original outside domain | core `v in [0,1]^k`, `V(v) = min_z F(v,z)` on a residual domain independent of `v` | none |
| Corner oracle | exact convex QP / convex MIQP / scalar recourse | exact sparse min-marginal DP (certified approximate for implicit graphs) | exact box-stable recourse, certified approximate recourse, exact integer/TU/flow recourse | none |
| Count | aligned, uniform-ambient (volume lemma), Gaussian-weighted | `prod [4 + (1+n/2) L w_i/(2 sigma)]` per bag, domain variants | `[3 + (1+k/2) L/(2 sigma)]^k` (exact), `[3 + (1+k) L/(2 sigma)]^k` (certified) | component tail `sum a_i q_i/(1 - 4 Delta beta)` |
| Closure | critical region (+ label gap; scalar regions; lattice) | face fixing + PSD / convex-patch test | excluded region + patch; competing label + small-core solve; optimal-face certificate | strict monotonicity pinning |
| Good event | noise away from fixed hyperplanes; no integer near-tie | growth `>= g_0`, active margins `> tau` | growth (full or projected), margins, algebraic tubes | none needed |
| Exceptional draws | active-face / label enumeration (rational); none for A9 | face enumeration (QP); lexicographic two-block fallback | face or label enumeration; lexicographic fallback | none (exact component solves) |
| Output | exact rational | rational (QP) / implicit convex patch / charted graph patch | rational / patch / integer label + shared-root small-core algebraic | rational / one algebraic representation per component |
| Bound type | FPT (aligned, Gaussian-like); `n^{O(k)}` (uniform ambient) | XP in `p` (barrier X1) | FPT in `k` and `L/sigma`; three sampling-bit regimes | polynomial under a strong-noise condition |

## 4. Chapter plan, mapped to the root's ownership and label prefixes

The root's `notation.md` assigns four Opus blocks and label prefixes
`model:`, `count:`, `qp:`, `sp:`, `con:`, `rec:`, `int:`, `lim:`. The plan
below follows that assignment. Page estimates are rough (single column).

### Front matter (owner 4; `model:`)

**Abstract and Section 1, Introduction (6-7 pp.).** Model and why the
finite rational law belongs to the theorem (Turing input, atoms, no
resampling); main-results table (Section 5 below); the common mechanism in
one page; precise relation to prior and sibling work (classical
ingredients: Renegar elimination, Basu-Lerario tubes, GLS weak
optimization, exact convex QP and MIQP oracles, Hochbaum-Shanthikumar,
parametric-QP critical regions and Ding's reduction, Lee-Phạm genericity,
Beier-Vöcking and Röglin-Vöcking isolation, Kelner-Nikolova low-rank
smoothing; sibling manuscripts cited as unpublished companions without
private paths); uses and limits. IDs: summary; F18; X8.

**Section 2, Model and contracts (`model:`, 5-6 pp.).** Input model
(certificate encodings in `I`, verification work in running time;
correctness promises distinguished from complexity assumptions); noise
laws N1-N6 with `sigma` as scale (half-width for grids, standard deviation
of the Gaussian proxy, not the Gaussian-like support radius); the meaning
of every draw and expected bit work; output contracts OC1-OC6, compact
descriptor versus global proof record, charted graph descriptors;
parameters and numerical ratios; original-objective regret (F18) with its
representation and calibration caveats (inventory §6 item 23); the
perturbation models overlap in special cases but their guarantees do not
transfer automatically. IDs: F18.

### Block 1 (owner 1; `count:` and `qp:`)

**Section 3, Counting and finite-noise foundations (`count:`, 12-14 pp.).**
3.1 Template theorem and precision order (F16).
3.2 Semiconcave search: rounding and corrected corners (F1; correlated
simplex and order variants stated here, proved where used), nested
meshes, retained-witness invariant, localization (F12).
3.3 Local-comparison counts (F2); conditioning principle; deterministic
dominating counts for adaptive lists.
3.4 Tails: growth tail (F3), active margins (F7, stated once for general
domain formulas), label isolation (F8).
3.5 Finite laws: section-count transfer (F5); section bounds from finite
candidate sets (F4) and two-block elimination on semialgebraic mixed
domains (F6, stated once); algebraic tubes with jitter (F13); the finite
Gaussian-like law and weighted lattice count (F14).
3.6 Exact completion: rational face/label enumeration (F9); lexicographic
two-block fallback on general compact domains (F10).
3.7 Evaluating implicit convex patches (F11; boxes, relative polytopes).
IDs: F1-F14, F16, F17. Overlap: core-noise analogues of F5, F6, F10 and a
projected-growth tail appear in the exact-arithmetic companion; F1's
deterministic form appears in the decomposition companion.

**Section 4, Few negative directions: exact quadratic closure (`qp:`,
13-15 pp.).**
4.1 Fenchel lift, rational normalization and the attaining-witness
inequality (A0; kernel inclusion dropped for supplied factors, root
decision 4). The deterministic conditioned theorem appears as contrast and
as the input to 4.2.
4.2 The two-inertia proposition (A1) with Sol's explicit derivation of
the `Z^{k/2}` exponent, its uniform-grid statement, the optional
Gaussian-like variant, and its `k > 2` limit (X9). Root decision 2.
4.3 Theorem A: critical-region closure under aligned (A2), uniform ambient
(A3) and Gaussian-like ambient (A4) noise; Gaussian-like is the principal
statement (Sol low-rank audit §10).
4.4 Theorem A-MIQP: best-other-label gap with uniform (A5) and
Gaussian-like (A6) ambient noise; corner-label example X11; aligned noise
does not isolate labels (inventory §6 item 22).
4.5 Theorem A-sep: separable mixed recourse (A7) and its anisotropic
Gaussian-like form (A8); rational-breakpoint example X12.
4.6 The fine law matters: example X10.
IDs: A0-A8, X9-X12. Proofs in Appendices A (foundations) and B (Route A).

### Block 2 (owner 2; `sp:` and `con:`)

**Section 5, Sparse polynomial optimization (`sp:`, 9-10 pp.).**
5.1 Bag-cell search, rounding through overlapping whitelists, separator-
key DP and the conditional count (B1).
5.2 Theorem B for fixed-degree polynomial factors on mixed boxes (B3), with
the quadratic specialization and rational output (B2); global proof trace
required (inventory §6 item 26).
5.3 The bridge to recourse: a certified conditional-recourse oracle would
replace `n` by `p` in the count (B10); the deterministic filter and the
bag-local counterexamples are in the decomposition companion (X2).
IDs: B1-B3, B10, X2. Proofs in Appendix C.

**Section 6, Constraint extensions (`con:`, 8-10 pp.).**
Theorem B-dom: explicit polynomial graphs (B4, charted output, rational
feasible approximants), implicit monotone graphs (B5, charted descriptor;
no rational feasible point in general), disjoint resource and probability
simplex blocks (B6), continuous and binary order polytopes in one theorem
with the transport count (B7, B8; root decision 3; weighted closure test),
affine-state actuator dynamics as an example (B9). Remarks: TU feasible
rounding and the fixed-polytope count at their proved scope (E7; root
decision 5); binary-before-exposure example X13.
IDs: B4-B9, X13, E7. Proofs in Appendix D.

### Block 3 (owner 3; `rec:` and `int:`)

**Section 7, Continuous conditional recourse (`rec:`, 8-10 pp.).**
7.1 Core search with exact or certified recourse; the excluded-region
certificate. Theorem C1: (a) exact box-stable QP recourse with rational
output (C1); (b) certified approximate recourse, e.g. convex residual
polynomials, with patch output (C3). Feedback-vertex-set corollary (C2);
rank-separation example (C4) attached to the residual-convex class only.
7.2 Core-only noise with uniformly strongly convex residuals, Theorem C3
(C8): growth lift, residual active-pattern tubes, small-multiplier release;
the rank-`k` convexifier remark (the gain is the original `L/sigma`);
examples X14; why merely convex residuals fail (X7, statement and pointer).
IDs: C1-C4, C8, X14. Proofs in Appendix E.

**Section 8, Native integers, TU and flow recourse, and strong noise
(`int:`, 12-14 pp.).**
8.1 The constant-base small-box solver (F15) as a reusable algebraic
interface (root decision 1; no novelty claim for its classical
mechanisms).
8.2 Theorem C2: native-integer recourse with all-coordinate noise (C5):
competing-label exclusion, whole-core completion; implicit variant (C6);
TU and network oracles (C7).
8.3 Theorem C4: core-only noise with separable convex integer recourse over
bounded TU systems, networks as an instance: the optimal-face certificate
(C10); (a) general convex costs with parameter-dependent sampling bits
(C11, C13); (b) bilinear coupling with polynomial sampling bits (C12, C13);
(c) the interior variant, proved for networks only (C9). The three
sampling regimes are stated in one table (root decision 7). Boundary
obstruction X6 motivates the face certificate.
8.4 Exactness by an objective lattice: Theorem A-int (A9), placed here
because its exact scalar integer recourse and fallback-free completion
belong with integer recourse; its Fenchel search is that of Section 4.
Deterministic baselines X16.
8.5 Strong noise without width, Theorem D (D1 QP, D2 polynomial with
structured output).
IDs: F15, C5-C7, C9-C13, A9, D1, D2, X6, X16. Proofs in Appendix F.

### Block 4 (owner 4; `lim:` and discussion)

**Section 9, Limitations (`lim:`, 6-8 pp.).** Proved obstructions, each
with its precise scope (none is a hardness theorem for the problem class):
global-error retention barrier (X1); ambient count-surrogate barrier (X3);
affine feasibility barrier and TU counting obstruction (X4);
parameterization obstructions (X5); single-flow boundary obstruction (X6,
proved here; Section 8 cites it); rotating fibers (X7); compatibility with
width-two hardness (X8); residual point-output barriers from the
exact-arithmetic companion (X15, cited).

**Section 10, Discussion and open problems (3-4 pp.).** FPT in width (X1,
B10); a sparse `nu/g` parameter; general affine or TU constraints (X4, E7);
exact output with merely convex residuals (X7, X15); dimension-free uniform
ambient counts (X3); sampled versus original objective; what an
implementation would need. Theory and worked examples only; no benchmark.

### Appendices (55-70 pp.)

* A (owner 1). Foundations: F3 (proximal and expanding-map proofs,
  sharpness), F4, F5, F6 and F7 for general domain formulas, F8, F9, F10,
  F11, F13 (Basu-Lerario input), F14.
* B (owner 1). Route A: normalization and the conditioned theorem (A0), A1
  and its Gaussian-like variant, critical-region extraction and the
  base-only Hessian bound (A2), volume lemma, section count and frame bound
  (A3), Gaussian budget loop (A4), label gap and mixed section count (A5,
  A6), scalar recourse and anisotropic normalization (A7, A8).
* C (owner 2). Sparse search and closure bookkeeping (B1-B3).
* D (owner 2). Constraint domains: graph substitution (B4, B9), certified
  approximate DP and bordered KKT (B5), simplex rounding, face counts, face
  tests and relative evaluator (B6), order transport, LP exposure, paired
  noise and weighted closure (B7, B8), TU rounding lemma (E7).
* E (owner 3). Continuous recourse: excluded region (C1), tangent
  certificates (C3), growth lift, three-block boundary formula and small
  multipliers (C8).
* F (owner 3). Integer recourse: F15 with its implementation ledger,
  competing labels and completion (C5, C6), intervals, proximity, chart
  images, value and affine margins, compact TU dual, circuits and slacks
  (C9-C13), lattice exactness (A9), strong-field proofs (D1, D2).
* G (owner 4). Limitation proofs too long for Section 9 (X1, X3, X4, X6,
  X7).

## 5. Main results (draft statements for the introduction table)

All theorems: one base-chosen finite law; exact output on every draw; no
growth, uniqueness or genericity promise; expected bit work as displayed;
polynomial exponents independent of the structural parameter. `C, C_0` are
absolute constants; `poly_d` has degree depending only on the fixed degree
`d`; `c_d` is the effective constant of F15.

| Theorem | Instance class | Noise | Expected bit work | Output |
| --- | --- | --- | --- | --- |
| A (a) | rational QP on a bounded rational polytope; supplied factor `H + alpha T^T T >= 0`, `||T|| <= 1`, `k` rows (normalization supplies one with `k = n_-(H)`) | aligned `T^T xi`, `xi` uniform grid | `C^k (1 + Theta_al)(I+1)^C`, `Theta_al = prod_i [3 + (1+2k) alpha w_i/(2 sigma)]` | exact rational |
| A (b) | same, `T` full row rank | ambient uniform grid | `C^k (1 + Theta_amb)(I+1)^C`; for the normalized factor `Theta_amb <= [2 + (1+2k)(2n + 2 nu sqrt(n) diam/sigma)]^k` | exact rational |
| A (c) | same, frame `c I <= TT^T <= I`, `c >= 1/2` | ambient Gaussian-like | `f(k, nu diam(P)/sigma) poly(I)`, absolute exponent | exact rational |
| A1 (prop.) | QP on a polytope, `n_-(H) <= 2` | ambient uniform (or Gaussian-like with enlarged accuracy) | `(I+1)^C (1 + nu W/sigma)` | exact rational |
| A-MIQP | rational QP on a bounded mixed polytope, `n_z` integer coordinates | ambient uniform / Gaussian-like | `f(n_z) C^k (1 + Theta_amb) poly(I)` / `f(n_z, k, 1 + nu diam(P)/sigma) poly(I)` | exact rational |
| A-sep | `sum_i phi_i(x_i) - (alpha/2)||Tx||^2`, convex piecewise quadratics with rational breakpoints, mixed product box, any `n_z` | aligned / ambient uniform / Gaussian-like | `C^k(1 + Theta_al) poly(I)` / `C^k(1 + Theta_amb) poly(I)` / `f(k, 1 + beta diam(X)/sigma) poly(I)`, `beta = alpha ||T||^2` | exact rational |
| B | fixed-degree polynomial factors on a mixed box, bag size `p`, `partial_ii F_0 <= L` on the hull | ambient uniform | `C_0^p [4 + (1+n/2) L w_max/(2 sigma)]^p poly_d(I)` | implicit convex patch (rational for QP) |
| B-dom | (i) explicit polynomial graphs; (ii) implicit monotone graphs; (iii) simplex blocks; (iv) continuous and binary order polytopes | ambient uniform | (i) bag size `p' <= max(1,k^D) p`, pullback `L'`; (ii) factor `(1+n)`, `p' <= p max(1,k)`; (iii) `C_0^p [4 + (2 + n/2) L max(1, w_max)/(2 sigma)]^p`; (iv) `C_0^p p_c!(p_c+1)[2 + 3 n_c Lambda/(4 sigma)]^{p_c}` (`p_c` continuous coordinates per bag; `p_c = p`, `n_c = n` for continuous orders) | charted patch / patch |
| C1 | unit-box core `k`, `L` on core diagonal; (a) exact box-stable QP recourse; (b) certified approximate recourse | ambient uniform | (a) `8^k [3 + (1+k/2) L/(2 sigma)]^k poly(I)`; (b) `8^k [3 + (1+k) L/(2 sigma)]^k poly_d(I)` | (a) rational; (b) patch |
| C2 | `[0,1]^k x Y`, `Y = {z in Z^r : Dz <= e, l <= z <= u}`, exact recourse under bound tightening | ambient uniform | `[8^k (3 + (1+k/2) L/(2 sigma))^k + c_d^k] poly_d(I)` | label + shared-root core, size `c_d^k poly_d(I)` every draw |
| C3 | core `k`, residual `H_RR >= mu I` (certified) | core only | `8^k [3 + (1+k) L/(2 sigma)]^k poly_d(I)` | patch |
| C4 | core `k`; separable convex integer recourse over a fixed bounded TU system (networks included) | core only | (a) `f_d(k) [3 + (1+k/2) L/(2 sigma)]^k poly_d(I)`, `log M <= f_d(k) poly_d(I)`; (b) bilinear: `[8^k (...)^k + c_d^k] poly_d(I)`, `log M = poly_d(I)`, `L` from `phi`; (c) networks with all optimal cores interior for every noise: as (b) for general convex arc costs | label + shared-root core |
| A-int | integer box, convex quartic `g_j` minus `(alpha/2)||Tx||^2`, `r` rows | aligned, per-row widths | `8^r Theta_rat P(I)`, no fallback | exact |
| D | mixed box QP (D1) and fixed-degree polynomials (D2) | strong uniform grid | `poly(I + log M)[1 + sum_i a_i q_i/(1 - 4 Delta beta)]` when `4 Delta beta < 1`; `a_i` = 3 (QP) or `c_d` (polynomial) for continuous coordinates, label count for integers | rational (D1) / per-component algebraic, symbolic value sum (D2) |

## 6. Dependency graph (proof order)

```
F1 -> F2 -> {A2, B1, C1}
F3 -> F4 -> {A1, B2, C1}          F3 + F6 -> F7 -> {B3, B5-B8, C3, C5, C8}
F5: every finite-law statement     F8 -> {A5, A6}
F9 -> {A1-A8, B2, C1, D1}          F10 -> {B3-B8, C3, C8; C5 fallback}
F11 -> {B3-B8, C3, C6, C8}         F13 -> {C8, C9, C11}
F14 -> {A4, A6, A8, A1 variant}    F15 -> {C5, C9, C11-C13, D2}
A0 -> {A1 (count), A2-A6 (normalization)}
A2 -> A3 -> A4;  A3 -> A5;  A4 + A5 -> A6;  A2 + A3 -> A7 -> A8;  A9 (F2, A0 lift)
B1 -> B2 -> B3 -> {B4, B5, B6, B7, B9};  B7 -> B8;  B10 (F2)
C1 -> C3 -> C8;  C1 -> C5 -> {C6, C9};  C7 -> {C5, C9, C10};  C10 -> C11 -> C12;  {C11, C12} -> C13
D1 -> D2
```

Writing order: Sections 2-3 and Appendix A first (their lemma statements
fix the interfaces), then Blocks 1-3 in parallel, then Section 9, then the
introduction.

## 7. Notation additions and clash resolutions

The root's `notation.md` is authoritative (`I`, `n`, `n_c`, `n_z`, `k`, `p`,
`d`, `L`, `alpha`, `nu`, `sigma`, `gamma`, `xi`, `M`, `h_j`, `J`, `E_j`,
`U_j`, `f^*`, `B`, `g_0`, `tau`). Proposed additions:

| Symbol | Meaning | Replaces in sources |
| --- | --- | --- |
| `H`, `c` | Hessian and linear coefficient of a quadratic `x^T H x/2 + c^T x + c_0` | `A`, `b` |
| `A x <= b` with `m` rows | linear constraints; `A` also for a TU matrix | `M x <= d`, `C x <= d`, `q` rows |
| `T` | supplied factor, `H + alpha T^T T >= 0`, `||T||_2 <= 1` | - |
| `beta` | `alpha ||T||_2^2` in the separable theorem; Route D's `q_i` and `beta` are local to Section 8.5 | - |
| `W(a)`, `V` | Fenchel value (Route A); conditional values in Routes B and C | `W_r`, `V_gamma` |
| `gamma^perp` | ambient-noise component in `ker T` | `r` |
| `G_M(sigma)` | grid `{-sigma + 2 sigma j/(M-1) : 0 <= j < M}` | - |
| `b` | bits of one sampled coefficient | - |
| `Lambda` | full Hessian upper bound (order domains) | `H` |
| `mu` | residual strong-convexity modulus | - |
| `G`, `M_2`, `M_3` | rational bounds on gradient one-norm, Hessian row sums, third-derivative row sums | `G`, `M_1`, `T` |
| `v`, `z`, `r` | core variables, residual variables, residual dimension (arcs for flows; `s` nodes) | - |
| `e_j` | core correction `k L h_j^2/8` (Route C), beside the global `E_j = n L h_j^2/8` | `B_j` |
| `Theta` | expected count factors | `H_B`, `H_amb`, `H_G`, `H_rat`, `Q` |
| `C_sec`, `C_tail` | section-component bounds | `C`, `D` |
| `bar H` | base-only bound on critical-piece Hessians | `H_0` |
| `N_z = prod (u_i - l_i + 1)` | number of integer label assignments | `R_Z`, `Z` |
| `p_c` | continuous coordinates per bag (binary order) | `q` |
| `c_d`; `f_d(k)`; `E_d(k)` | F15 constant; parameter factors of C11; analysis-only elimination format | `A_d(k)` (stale) |
| `Delta` | maximum primal degree (Route D) | - |
| `q` | only requested accuracy `2^{-q}` | `t` |

Clash resolutions requested from the root:

1. `B` is both the fallback work factor (root) and the standard bag symbol.
   Recommendation: keep `B` for the work factor and always write bags as
   `B_t` with an index, as the decomposition companion does.
2. `notation.md` allows `r` for input-inequality counts, but `r` is the
   residual dimension in Route C and the factor rank in A9. Recommendation:
   use `m` for inequality rows everywhere.
3. `q` is a precision, the per-bag continuous count of the source, and a
   face dimension in the tube lemma. Recommendation: `q` for precision
   only, `p_c` for the count, `s` or `dim K` for the face dimension.
4. `T` is the factor and the source's third-derivative bound.
   Recommendation: `M_3` for the latter.

## 8. Cut plan

### 8.1 Merges (one theorem, several parts)

* A2, A3, A4 -> Theorem A (three laws; Gaussian-like principal).
* A5, A6 -> Theorem A-MIQP. A7, A8 -> Theorem A-sep.
* B2, B3 -> Theorem B (quadratic case as part).
* B4-B8 -> Theorem B-dom; B7 and B8 in one order theorem with the transport
  count.
* C1, C3 -> Theorem C1 (exact versus certified recourse oracle).
* C9, C11, C12, C13 -> Theorem C4 for TU systems, networks as an instance,
  interior variant (networks only) as part (c).
* D1, D2 -> Theorem D.

### 8.2 Demotions

* A1 -> proposition (kept for its linear numerical dependence; not
  subsumed).
* B9, C4, F18, X16 -> examples or remarks. C2, C6, B10 -> corollaries.
* X9-X14 -> remarks next to the hypotheses they justify.
* X2, X15 and O1-O8 -> citations of the companions.

### 8.3 Exclusions

A10, D3 and E1-E10, except that E7 appears at its proved scope as a
supporting lemma or scope boundary (root decision 5).

### 8.4 Size

About 70-80 pp. main text and 55-70 pp. appendices. If the root later
needs a shorter paper, the least costly reductions are: move Theorem
B-dom (iii)-(iv) proofs and Theorem C4(a) entirely to appendices, compress
Section 9 to statements with appendix proofs, and shorten A1 to a remark
recorded in the coverage map as an intentionally omitted refinement.

## 9. Decisions recorded and open requests

Resolved by the root (`integration-decisions.md`): F15 and both strong-field
families are included (decision 1); A1 is kept with Sol's derivation
(decision 2); the transport count covers continuous orders (decision 3);
kernel inclusion is dropped for supplied factors (decision 4); TU rounding
only at proved scope (decision 5); charted graph outputs (decision 6);
three recourse sampling regimes (decision 7); honest overlap wording
without private paths (decision 8); no benchmark (decision 9).

Open requests to the root:

* The four notation clash resolutions in Section 7.
* Placement of A9 in Section 8 (`int:`) rather than Section 4 (`qp:`):
  Sol's recourse audit covered it, and its exactness mechanism is the
  integer lattice. If the root prefers `qp:`, only cross-references change.
* Whether Section 9 (owner 4) or the route chapters own the small
  hypothesis-justifying examples X10-X14; this plan keeps them in the route
  chapters and the proved obstructions in Section 9.

## 10. Verification priorities for Sol and Opus reviewers

Independent re-derivation priorities, from `inventory.md` §6: the general
non-box versions of F6, F7 and F10 that must be stated once; the ambient
volume lemma (A3); the mixed section count (A5); the Gaussian weighted sum
with a small frame constant (A4, A8); order transport and the weighted
closure test (B7, B8); simplex counts (B6); implicit DP error accounting
and the charted descriptor (B5); the flow value margin and identity
argument (C11); the compact TU dual (C13); the three-block boundary formula
and release constants (C8); F15 completeness; the area-formula step of F3.
Each theorem's budget order should be recomputed with the unified constants.
