# Opus whole-paper review, round 2

Date: 2026-10-05, about 20:45–21:45 UTC. Reviewer: Opus review sub-agent,
fresh round. This is not a continuation of the interim
`opus-wholepaper-r1.md`. Scope: the whole manuscript in
`paper-exact-arithmetic/`, all 97 inventory IDs, including Appendix L
(Q13–Q14). This file is the only file I wrote. I edited no manuscript,
bibliography or other evidence file.

## 1. Verdict

**I found no proof blocker and no unresolved source-contract defect.
One abstract sentence states the cone result without its scope and should
be qualified before submission (Finding 1, P2). Three minor presentation
items (P3) and one optional cleanup remain.**

- **Internal mathematics.** I read every section and appendix in its final
  form and reconstructed the proofs of every theorem family by hand, at the
  depth recorded in Section 4. I found no mathematical error, no missing
  hypothesis and no mismatch between a statement and its proof. Every
  high-risk item in the brief checks (Section 4.14).
- **Sources.** I did no literature research. The vetted literature report
  now records the contracts used by the riskiest new steps:
  - Basu 2014, Theorem 2.27 (fixed blocks);
  - Khachiyan–Porkolab, Theorem 1.1, with the quantified-block product in
    the exponent of the degree;
  - Lenstra 1983, Section 5;
  - Ben-Tal–Nemirovski, Theorem 1.1, and Kocuk 2021;
  - Kannan–Lenstra–Lovász, Theorem 1.19, and Serre, Proposition 3.3.5 and
    Theorem 3.4.4;
  - Eisenbud–Green–Harris, Theorem CB7, and Eisenbud–Harris 1987;
  - Renegar 1992, Part III, Theorem 1.1, and Luo–Zhang, Corollary 2;
  - Tarasov–Vyalyi, Theorems 3–4 (arXiv v1), and the Krick–Pardo–Sombra
    degree inequalities (noted as verified).

  Root's STATUS (21:32 UTC) reports that the remaining critical source
  checks passed and that the final literature report is still being
  written. Three clearances appear only in author and review records, not
  yet as rows of the vetted report:
  - Grigoriev–Pasechnik, Theorem 1.2;
  - Dedieu–Malajovich–Shub, Theorem 5.1;
  - Bombieri–Gubler.

  I treat this as an unfinished record, not an open defect (Section 8).
- **Readiness.** I do not yet call the manuscript submission-ready, for
  two reasons:
  1. the abstract sentence of Finding 1 should be fixed;
  2. the final literature record should be completed, so that the
     clearances above can be audited.

  Neither is a proof or source blocker. If both are done and no further
  mathematical text changes, this review has no remaining objection. This
  is an internal review, not external peer review.

## 2. Scope and method

I read the following:

- the brief, the conventions, the decisions (D1–D10; D3 superseded), both
  INTEGRATION records, STATUS and the final coverage audit;
- the latest literature review (21:32 UTC version, then its 21:37 UTC
  update);
- all authoring repair records;
- the author report for Appendix L;
- the full proof-family reviews and their second rounds: upper,
  reductions, heights, points, constraints, points-constraints,
  algebraic, fields, recourse, contrast, numerical (Opus R1 and R2),
  framing, readability, nonconvex, cones (R1 and R2) and integration (R1
  and R2);
- the interim `opus-wholepaper-r1.md` and `submission-package-r1.md`.

Manuscript read in full, in this order: abstract; Sections 00–11; then
Appendices C, A, D, E, G, H, I, L, J, K, B and F. Each main-text section
was read together with its proof appendix.

**Method.** I re-derived proofs by hand. That means:

- checking every displayed identity I could expand;
- recomputing constants and thresholds;
- tracing each imported contract to its statement in the paper;
- following each cross-appendix interface to the proof it relies on.

Printed finite certificates (large Gram matrices and their minors) were
spot-checked only (Section 9).

I ran no build, experiment, historical script, CAS, project-wide check or
CI inspection. Section 10 lists the read-only document checks I ran.

## 3. Changes made during this review

The manuscript changed several times while I was reading it. I rebuilt
each text I had read from my own earlier read outputs and diffed it
against the later file. I reread every change.

| File | Changed (UTC) | What changed | Assessment |
| --- | --- | --- | --- |
| `sections/00-introduction.tex` | 20:56, after my read | The scope paragraph (00:918–923) now limits the PosSLP/Square Root Sum hardness statement to continuous convex polynomial families. It also names Appendix L's strong NP-hardness with one constraint-Hessian direction. | Correct; matches the reductions at L:611–628. |
| `sections/08-fields.tex`, `sections/09-certificates.tex` | 20:47, before my read | I read the final versions. | Verified as part of the full read. |
| `appendices/J-quadratic-contrast.tex` | 21:05, before my read | I read the final version (`5d01e184…`) in full. | Section 4.11. |
| `appendices/L-further-arithmetic.tex` | 21:22 | L:198–199. The sentence citing Heintz 1983 (Lemma 2, Proposition 3) for the affine degree and projection facts was replaced by "These bounds use cumulative degree, so all components are charged." | Fine. The facts used remain cited to Krick–Pardo–Sombra §1.2.1, which STATUS reports was inspected. `Heintz1983` is now uncited. |
| `sections/06-algebraic.tex`, `appendices/E-algebraic.tex` | 21:25 | Citation and locator changes only. Harris 1992 → Eisenbud–Harris 1987 for minimal degree (06:552, E:1288–1289). E:1233 drops a Harris locator. (AG3) now cites only EGH Theorem CB7. | Imported statements unchanged. CB7 implies the reduced "all but one point" clause: take the residual to be one point, whose ideal sheaf has vanishing h¹ in nonnegative degree. Dropping CB5 therefore loses nothing, which matches the vetted EGH row. |
| `sections/abstract.tex` | 21:33 | The recourse sentence now says "the full selected optimizer of the tilted instance at every precision, correct on every draw". | Correct; matches Section 10. Resolves item 1 of the interim r1. |
| `references.bib`, `main.tex` | several times | Bibliography integration; PDF title; table-of-contents layout. | All references and citations resolve (Section 10). |

## 4. Reconstruction by theorem family

Each family lists its main results, its dependencies, and what I
re-derived. "Imported" means an external theorem used under a stated
contract (Section 8).

### 4.1 Models and output contracts (Section 01)

These definitions are used everywhere: explicit encoding, Hessian Grams,
the canonical quadratic-square Gram, rational circuits and root circuits,
the minimum-norm and fixed selectors, PosSLP and Las Vegas.

- Re-derived: the low-degree tensor (Killing) argument; the Gram
  congruence S=[[T,0],[c⊗T,T⊗T]]; and the conic-duality construction in
  `rem:models-socp`, where a 2×2 PSD block is equivalent to
  ‖(2b,a−c)‖≤a+c.
- The {x+y, x²/2} gate basis credited to Tarasov–Vyalyi in
  `rem:models-socp` is elementary to re-derive. It is now a vetted row
  (arXiv v1, Theorems 3–4). The bibliography entry notes that the theorem
  numbers refer to v1, which covers the locator at 00:802.

### 4.2 Values to points (Sections 02 and C)

Results: `thm:global-point` (exponent 1/D, effective constant),
`thm:cubic-point`, the quartic lower bounds, the regularization family,
the path family and the rectangle certificates. Dependencies: Slot–Steurer–
Wiedmer v1 structural facts, re-derived with constants; the GLS contracts
behind `lem:convex-value`.

Re-derived:

- the selector τ and log₂(1/τ);
- the interpolation constants and β_k;
- the Hoffman bound, the minorant and radius lemmas, and the Bregman error
  modulus;
- for the cubic theorem, 108ΛR₀² and τ=ε⁶/(1024R⁴Γ⁴);
- the amplifier identity
  d²/dt²[(θ+tπ)²(y+tς−γ)²]=2(θς+2(y−γ)π)²−6(y−γ)²π²;
- ‖P‖≤1/√2 for the averaging tree, the trace lemma, and the gate gap
  9/8−1/63;
- for the regularization family, x_n*≤14·28^{−2^n};
- for the path family, P_k(t+1)≡t^{2^k} mod 2 with constant −2
  (Eisenstein) and 2^{n−2}+1 nonzero terms;
- the rectangle constants 5/8, 11/32 and 135/256.

### 4.3 Exact upper bounds (Sections 03 and A)

Results: `lem:separation`, the Newton circuits, `thm:exact-upper`, the
monotone-map theorem with its non-gradient example, the slack gap, and
`thm:posslp-closure` (adaptive single-sign compiler). Imported: one-block
QE with coefficient-height control (Basu, vetted).

Re-derived:

- the shifted-comparison margins 3g/8 and 15g²/64;
- the non-gradient matrix Q₀ and its minors 3, 47/16, 43/16, 65/16;
- the warm start δ₀=μ⁵/(32Λ⁵) and the cut bound below −Λδ₀;
- the compressor bound εκ^S<1/4 and the identity B⁴=σ_{S+2}.

### 4.4 Lower reductions (Sections 04 and B)

Results: the cube-root compiler, `thm:reductions-root-language`, the
signed-root realization, the quaternion compiler and realization,
`thm:reductions-min-sign`, `thm:rational-optimizer`, the box baseline and
the sums proposition. Dependency: `lem:quartic-realization`.

Re-derived:

- the normalization; the small-signal boxes (radicand forms (a)–(c),
  (1±w)³ against 1±13w); and the analytic gadget bounds, including
  (16/9)·10⁶<2²⁴;
- signal arithmetic with Θ'=2³⁰Θ³ and log₂Θ_t=16·3^t−15;
- the schedule-order bookkeeping and the output inequality s_e²≤|s_o|/8;
- for the root-language upper bound: the conjugate bound Ξ, the
  separation 2^{−2^{6L}}, the Newton relative-error recursion and the
  propagation constants;
- |det J_i|=dα^{d−1} for the residual Jacobian; the tridiagonal T_α and
  its eigenvalue bound; the power-curve identity
  P_α=(t−α)(t^d−α^d); and the exact vanishing representation
  E_i^*=S_i−α_iT_i+Σχ_𝔪(α_i)R_{i,𝔪};
- the coupled-form rescaling: off-diagonal row sum ρ^{1/2}A=h₀/4;
- the quaternion identities, the generator iteration 6g′₁≤(6g₁)², and
  log₂Θ_t=(41·4^t−20)/3;
- the tilt Gram entries, the Frobenius bound √(12κ²+10)<8, and
  G*≥u₀²t/2;
- the box-baseline weights B=2(C+1).

### 4.5 Constraints, VI and integer search (Sections 05 and D)

Results: `thm:constraints-unambiguous` (UP^PosSLP∩coUP^PosSLP, including
degenerate polyhedra and strongly monotone cubic VIs), the rank Las Vegas
theorem, `thm:constraints-nonlinear` (2^{O(k)}L^C), the constrained Newton
transfer, boxes and flows, the binary corollary, and the mixed candidate
lists.

Re-derived:

- the partial minimum φ(u)=f(c̄+Du) and G(k)=2·4^{c₀k};
- the Newton transfer e_{j+1}≤e_j², and the star graph giving k=n−1;
- the binary-decision Gram Schur bound 3−32ε²N/ϱ≥3−2/25;
- the Jacobi-contraction admissible vector and the ≤2n-pivot homotopy;
- the artificial-arc potentials, including fixed arcs;
- the padding Gram 4τ−32nt/μ₀=4;
- the circuit LP and the normal-cone test.

The open polyhedral question (P^PosSLP versus UP∩coUP) is kept open
consistently in Sections 00, 05 and 11.

### 4.6 Singletons, degrees and cyclic families (Sections 06 and E)

Results:

- `thm:singleton-field`: coordinates of rational convex singletons have
  exactly one real conjugate;
- the realization lemma and canonical-Gram covariance;
- the power-coordinate quartics;
- `thm:algebraic-cyclic`;
- the dimension and degree bounds, including the five-variable maximum
  21;
- the three-quadric corollary, the network bounds, and the univariate
  case.

Imported: (AG1)–(AG7) (Hartshorne, Fulton, EGH CB7, Eisenbud,
Eklund–Jost–Peterson, Eisenbud–Harris, adjunction).

Re-derived:

- the canonical Γ(g) blocks 2bb^T+4g₀T, Δ(b,T), Ξ(T), and the covariance
  contractions under Ψ_c;
- the bivariate identity
  7599q₁+2937q₂+5000q₃=12599x²−10000xy+7937y²−15874x−12599y+20000, the
  Hessian bound 4124, and the Gram entry 1511967752;
- the realization Schur bound;
- for power coordinates: σ, the discriminant, det J=P₁′(α)/κⁿ, and the
  converse k≥(d+1)/2;
- for the cyclic family:
  - d_n and e_i, the wrapped binomials, and E_m=ηd_n;
  - the J bounds and M₁=10⁶n⁵;
  - the condition number 65540n²<65600n²;
  - the length Θ(d_n²);
- the topological SOS-length argument;
- the network bounds: g≤2^{n−1}−1, and 3g≤2^m−(−1)^m in the Eulerian
  case;
- for the five-variable maximum:
  - the residual parity argument (2v≤ℓ≤2^{v−1} forces ℓ=8, contradicting
    odd ℓ);
  - every positive-base value e (32, 22, 10, 16, 18, 12, 20, 20, 16) is
    at least 10, so D≤22, and part (c) then gives D≤21;
- the univariate Markov step t(3+t)²=2^{−2k}.

### 4.7 Heights, moments and Gram size (Sections 07 and F)

Results: `thm:heights-witness`, `thm:rational-height`,
`thm:heights-moment`, `cor:heights-gram`, `thm:interior-gram` and
`thm:circuit-gram`.

Re-derived:

- the Taylor-Gram integrals (1/2, 1/3, 1/12 and the 1/36 remainder);
- the cube-chain residual Jacobian (diagonal-block determinant 3ξ²) and
  the exposer identity E_i=P_ξ+(ξ−x)(c−ξ³);
- the weight bound √45/32<0.21 and the margins ω_k/4≤H*≤5/2;
- the localization radius (2+√6)δ_k and the cubic denominator bound;
- the circle-chain exposer: E_j(P+u)=‖u_j‖²−2κ_j(t_{j−1}^Tu_{j−1})² and
  (3+4i)²≡3+4i (mod 5);
- the uniform trace bound W_n⪰I/(15(n+1)) (mean squares 1, 1/3, 4/45,
  1/9);
- the determinant-denominator lemma and the Ω(2^k/k³) interior-Gram bound;
- the moment counterexamples and Khachiyan-type blocks.

### 4.8 Coefficient fields and descent (Sections 08 and G)

Results:

- the least fields Q(2^{1/ℓ}) (prime family) and Q(2^{1/5^k}) (tower);
- the explicit ternary quartic and the non-attainment corollary;
- the field-specific relation spaces, product independence, the descent
  criterion, and the minimum dimension three for rational descent failure.

Re-derived:

- the φ_ℓ obstruction;
- for the ternary example: the relations at p⋆=(a⁴/2,a,a²/2), the φ⋆
  values, and the products x³y, x⁴, y³z, yz³, x³z;
- the yz³ obstruction in four variables;
- the prime-family constants N₀=2²⁰n⁸, 21233664n¹³ and ‖Γ(r)‖<17;
- the tower gate identity, ρ=2^{−13}, the baseline constants
  20736·78732<2³¹, and the slice vector (0,0,c₅,0,−c₃) giving −c₅²;
- the Galois-order argument, the interpolation determinants, the cyclic
  class count, and the descent theorem.

### 4.9 Certificates (Sections 09 and H)

Results: the multiplier and denominator identity, the membership
counterexample, radial multipliers, block separation, and the qualitative
finite radial order on rational sphere rings.

Re-derived:

- the full radial-finiteness proof:
  - the archimedean preordering;
  - algebraicity by derivations, and H∈J²;
  - the order unit and both pure-state cases;
  - the tangent forms and parity homogenization;
- the zero identity of the multiplier theorem;
- spot checks of the printed 15×15 N certificate: constant entry
  544=8·68 and x-coefficient −1152=8·(−144).

### 4.10 Recourse under core noise (Sections 10 and I)

Results: V1–V5 and RQ1–RQ4, `thm:recourse-cubic`,
`thm:recourse-convexified`, the joint corollary, the QP-height corollary,
the fiber proposition, `rem:recourse-quartic`, and the affine-power
convexifier.

Re-derived: the obstruction examples, the lattice test in both
directions, the recourse-selection τ, the cell oracle and its refinement
invariants, the simplex volume, the conjugate pushforward, the weak tail
(180k³)^k, the growth tail, the core work bound, the convexified error
bound, the face lemma, the margin probability and the rejection budget
1/(4Ξ).

### 4.11 Quadratic contrasts (Appendix J)

I read all 2,721 lines. Results and checks:

- **Degree.** `thm:qc-degree` gives [K(p):K]≤𝓑(n,k), with the Bézout
  count [U^dT^s](U+T)^d(2U)^s=2^s·C(d,s).
  - `lem:qc-parameter`: E≠0 by the implicit-function branch, and the
    Cayley–Hamilton identity extends to exceptional parameters.
  - `lem:qc-ordered-limits`: the lowest-order δ and then ε coefficients
    pass to the limit. This holds even if a specialization vanishes
    identically.
- **Height.** `lem:qc-elimination`:
  - the deformation λ_i^{a+1} gives a Gröbner basis by coprime leading
    monomials;
  - each multiplication-matrix entry has norm at most C_v^{T+1};
  - ℋ_κ vanishes along each real root branch by the left-eigenvector
    factorization det=β^T(wA−Γ−ζ)Ψ, with ζ^κ dividing Ψ;
  - W₀=𝔷(T+1)E+log𝔷!+𝔷log3.
- **`thm:qc-height`.**
  - G_j=Δ²(r_j−δ), and the Jacobian −Δ²G^TM^{−1}G is negative definite;
  - the norm bounds give E≤(2d+2)H_𝒮+2log((d+1)!)+2d log(s+2);
  - the Fujiwara and product-formula height bound for roots.
- **Radius, gap and decision.** `cor:qc-radius` and `prop:qc-decision`
  (the gap 2^{−L^{O(k+1)}} separates the decisions at η/3 and η/2).
- **Sharpness.** `thm:qc-sharp`:
  - the incidence variety is a graph, so ℒ=𝕂(x);
  - the derivation ∂_{a₀ⱼ}β=x_j gives 𝕂(β)=ℒ;
  - the seed point is valid, the substitution t=t₀+1/u is birational, and
    the thin-set density argument holds;
  - padding with slack PD rows reaches span k.
- **Span two and span three.**
  - `lem:qc-tangency`: the partial-fraction signs and root count force t₀
    to be a double root, and gcd(𝒩,𝒩′) is linear. Checked on the ball
    example −(τ−1)²/(τ+1) with uncancelled numerator −16(τ+1)²(τ−1)².
  - `prop:qc-two-rows` and `thm:qc-span-two`, Steps 1–5: the extreme-ray
    lift, margin decisions, bisection, and at most two curved restrictions.
  - `prop:qc-span-three`: weights λ=(2r−1,r²−1,1) with determinant
    2r³−1=3; the mixed weights 18ω_i bounded below by 95/16, 5/16 and
    23/9; and rational aggregates impossible because 1, r, r² are
    independent over Q.
- **Spectrahedra.**
  - `thm:qc-pencil`: real spectrum and double root; the size-2d
    construction 𝓛_ϱ=V^T·diag((α_j−x)/(α_j−ϱ))·V, with determinant
    det(G)²μ²/(μ(ϱ₋)μ(ϱ₊)).
  - `thm:qc-corank-one`: one real embedding through σ(v)=v; the converse
    uses the companion matrix and B∈ℒ, positive definite on U.
- **Long expanded outputs.**
  - `prop:qc-block`: S≡T^{2r} (mod ℓ) by the double-root comparison;
    v_ℓ(S(0))=1 by (1−rκ²)/ℓ≡1+m; the value valuation (r+1)/(2r) from
    the e=r+1 term.
  - `lem:qc-split`, using Hensel's lemma.
  - `thm:qc-blocks`(a)–(e), with the weight condition 1≤ω₁≤…≤ω_k and its
    k=2 necessity example.
  - The explicit weight, the translation lemma, and `thm:qc-sparse`.
  - `lem:qc-kummer` and `prop:qc-binomial-block`:
    - the form of B_* vanishes at the eigenvectors;
    - the projection constants D_r=r+1+a²(d−r−1);
    - ε₀=1/(100a⁵d²) and barycentric weights above 1/4;
    - Hessian independence through the cosine relation.
  - `cor:qc-feasible-output`: the mixing weights η_i=τ_i−1/11 and the
    alternating signs of the minimal polynomial.
  - `prop:qc-quartic`: x⁴−4ϖx+3ϖα=(x−α)²((x+α)²+2α²).
- **Recovery and certificates.**
  - `thm:qc-recovery`: the moment-curve primitive element, norm
    polynomials, and the derivative formula
    β_i=−∂_Sℛ_i(0,α)/𝔪′(α). The Q(√2) caution is correct.
  - `lem:qc-sign`.
  - `lem:qc-sound` and `thm:qc-certificate` (at most k exposing records;
    the chain example needs all k).
  - `thm:qc-rational-infeasibility`: rounding inside 𝒲, and the margin
    perturbation bound (M+2M²/η+M³/η²)ε.
  - `prop:qc-infeasibility-lower`(a)–(c).
- **Number-field QP and Pell.**
  - `thm:qc-number-field-qp`:
    - the pseudoinverse 𝒜^{−1}𝓜𝒜^{−1} holds for any kernel basis Z;
    - the Hoffman form and the optimal-set description;
    - the parameter chain ends with ‖y−p‖≤τ/16+√3τ/4<τ;
    - the classification is correct.
  - `prop:qc-pell`: |V|<4 in the fundamental domain, and v₅(B_j)=v₅(j).

### 4.12 Boundaries (Appendix K)

Re-derived:

- `prop:bnd-zero-hessian`: D³f(p)=0, and the null set of 𝒬 is invariant
  under translation along its zeros.
- `prop:bnd-newton`: the Hessian determinant 24x²(2x²+x+1)+4y²(24x²−6x+1)
  +48y⁴, the exact N(0,τ), h(1/2)=1/4, and 𝒯_y=(5/8)τ.
- `prop:bnd-kernel`: the Schur bound (2|t|−1)²≥0 and the kernel (0,a,1).
- `prop:bnd-nullvector`: eigenvalues x and x±√2.
- `prop:bnd-fixed-gap` and `prop:bnd-robust-root`: the degree +1 via the
  Jacobian D_k x^{D_k−1}, and the cycle has treewidth two.
- The root penalty: min(a,b)≤a^{1−θ}b^θ gives 4B_φ𝔢^ϖ. Its limits are
  checked in (a)–(d).

### 4.13 Nonconvex quadratic and algebraic-cone arithmetic (Appendix L)

I read all of L, at the version reviewed by cones-r2, and reread the
21:22 change.

**Q13 (nonconvex quadratic systems).**

- The minimal-face lemma. The ellipse example checks:
  −3x²+16x−12 takes the values 9 and 37/4, and deleting the inactive row
  exposes value 1.
- `thm:ncq-feasible` credits only Grigoriev–Pasechnik's Theorem 1.2 and
  explicitly does not import their Theorem 1.5.
- The generic KKT example: λ_i=−1−1/(2u_i) and GM^{−1}G^T=diag(−4u_i³).
- The bordered Jacobian −Δ²GM^{−1}G^T, and the perturbation and
  common-field lemmas.
- `thm:ncq-infimum`:
  - the inner perturbation limit is taken before the outer
    regularization limit;
  - the unknown auxiliary box becomes inactive eventually;
  - attainment holds with bounded least-norm points;
  - the nonunique and unattained examples check.
- `thm:ncq-oracle` (bisection and verifier) and the hardness rows.

**Q14 (algebraic cone systems).**

- The projection formula, in both directions:
  - all charts carry guards;
  - one common finite grid is used, with the grid point selected per z;
  - the radius R is fixed outside the universal block.
- The blocks (2,1,h+1). I composed the QE-first radius independently from
  the contracts now in the vetted report:

  > d′=L^{O(h+1)}, b′=L^{O((h+1)(t+1))},
  > b′(d′)^{O((t+1)⁴)}≤L^{C(h+1)(t+1)⁴}.

  The fixed-zero coordinate makes every feasible integer point optimal,
  including for a nonclosed Y. The repeated-d-th-power example no longer
  conflicts with this bound.
- The rational Lorentz lift:
  - the triples (120,119,169) and k_j=2^{j−2}+2;
  - θ₂=θ₁/2 exactly, and folding needs θ_j≥θ_{j−1}/2;
  - (1+ε/(2k))^k≤1+ε.
- The rounding bound, including the case t_i<0:

  > q_i≤48εT²+18Tη=66Δ/256<Δ/2.

- The final rational MILP solved by Lenstra §5.
- `thm:cone-witness`:
  - the norm query ‖(2x,r−1)‖≤r+1 has Hessian 8I;
  - coordinate bisection gives 3τ/4;
  - the √2/√3 example has absolute degree four.
- The threshold and fractional corollaries: residual 4−4ds and sign
  d+s≥0.

**Interfaces.** L reuses J's `lem:qc-heights`, `eq:qc-minpoly-height`,
`lem:qc-elimination` (which needs `lem:qc-ordered-limits`),
`thm:qc-kll`, `thm:qc-recovery` and `lem:qc-sign`. I checked every one of
these in J (Section 4.11). L applies no native-PSD theorem of J to the
indefinite squared cone rows.

### 4.14 High-risk items named in the brief

| Item | Where | Status |
| --- | --- | --- |
| Canonical Gram and translation covariance | 06, E | Reconstructed; holds. |
| Cyclic family (degree, condition number, length) | 06, E | Reconstructed; holds. |
| Five-variable degree 21 | E | Reconstructed. Imports (AG3)–(AG7) as recorded. |
| Minimum dimension 3 for rational descent failure | 08, G | Reconstructed; holds. |
| Field-specific relation spaces | 08, G | Reconstructed. The general real-field PSD Gram is kept distinct from SOS over that field. |
| Radial finiteness on rational sphere rings | 09, H | Full proof reconstructed; holds. |
| Recourse chain V1–V5, RQ1–RQ4 | 10, I | Reconstructed; holds. |
| Adaptive O(S²) compiler | 03, A | Reconstructed. Does not derandomize Las Vegas algorithms or combine multi-bit outputs into one bit. |
| Open arbitrary-polyhedron case | 05, D, 11 | Kept open consistently; UP∩coUP proved. |
| Monotone-map and VI interfaces | 03, A, 05, D | Reconstructed. The non-gradient example's minors check. |
| Distinct output models | 01, 02, 06, 07, J, L | Format-specific throughout. Rational circuits are never claimed to output irrational objects. |

## 5. Findings

### Finding 1 (P2, abstract scope): the cone sentence omits its fixed parameters

**Location.** `sections/abstract.tex:30–33`: "Further results bound
common-field algebraic witnesses for nonconvex quadratic constraints with
few independent Hessians and extend exact cone feasibility to explicitly
represented algebraic data."

**Problem.** `thm:cone-feasibility` and `thm:cone-witness` give
polynomial time only for fixed integer dimension t and fixed span h of
the continuous Hessians of the squared cone residuals. The exponent
depends on t and h. Without that qualifier, a reader can take the clause
as general exact cone feasibility for algebraic data. But the paper
itself proves that exact second-order cone feasibility is PosSLP-hard
(`rem:models-socp`, cited at 00:806–808). A polynomial-time algorithm
uniform in h would therefore put PosSLP in P. The word "extend" also
implies a prior result that the abstract never states. The introduction
(00:405–419), the discussion (11:55–63, 11:144–155) and L's opening state
the scope correctly; only the abstract is affected.

**Repair.** For example:

> Further results bound common-field algebraic witnesses for nonconvex
> quadratic constraints with few independent Hessians, and give
> polynomial-time exact feasibility and witness algorithms for
> second-order cone systems with fixed integer dimension and few
> independent continuous Hessians, also when the data lie in one
> explicitly represented real number field.

### Finding 2 (P3, reproducibility): unpublished rank computations are mentioned as evidence

**Locations.**

- `sections/08-fields.tex:752–754`: "Exact rank computations for n=2 and
  4≤n≤16 are consistent with equality; they are recorded diagnostics,
  not part of any proof here."
- `sections/00-introduction.tex:569–571`: "the recorded finite rank
  computations do not establish that assertion."

**Problem.** Both sentences say clearly that these computations prove
nothing, so nothing is wrong mathematically. But a referee cannot check
or reproduce computations that are neither described nor supplied, and
"recorded" points to project records that will not ship with the paper.

**Repair.** Either delete the two sentences, or state exactly what was
computed and supply the data as supplementary material. "What was
computed" means: the rational rank of the product map from pairs of
degree-two relations to the stationary quartics at each cyclic point,
for which n, and with what software.

### Finding 3 (P3, wording): unclear "it"

**Location.** `sections/00-introduction.tex:205–207`: "adding a dummy
core to the box-convex quartic reductions above would turn it into a Las
Vegas algorithm …".

**Problem.** "it" has no clear antecedent.

**Repair.** Match `rem:recourse-quartic`:

> For residual quartics no full-point guarantee of this form is expected:
> such a guarantee, applied after adding a dummy core to the box-convex
> quartic reductions above, would give a Las Vegas algorithm with
> expected polynomial running time for Square Root Sum and for PosSLP
> (Remark~\ref{rem:recourse-quartic}).

### Finding 4 (P3, positioning): relate the polynomial-time cone theorem to the paper's own SOCP hardness

**Location.** Appendix L's opening (L:8–12), or 00:405–419.

**Problem.** A reader who has seen `rem:models-socp` will ask how
ordinary polynomial time is possible for second-order cone feasibility.
The answer is that the hard gate systems have Hessian span h growing with
the instance. Nothing in the text says so.

**Repair.** One sentence, for example: "Without a bound on h, exact
second-order cone feasibility is PosSLP-hard (Remark~\ref{rem:models-socp}),
because the gate systems there have span growing with the input. The
running time therefore cannot be polynomial uniformly in h unless PosSLP
is in P."

### Optional cleanup (not a finding)

- **Uncited bibliography entries.** Six entries are uncited: `Balaji2016`,
  `FultonLazarsfeld1982`, `Heintz1983` (uncited since the 21:22 L
  change), `JeronimoPerrucciTsigaridas2013`, `Joye2026` and
  `NieRanestadSturmfels2010`. They do not print, because `main.tex` uses
  `plainnat` without `\nocite{*}`. Removing them would keep
  `references.bib` matched to the paper.
- **Notation.** The interim r1 also listed overloads of L, Λ, N and k.
  I found none that changes a statement's meaning; each is locally
  defined. "Appendix L" and the input length L share a letter. Renaming
  either is optional.

## 6. Previous findings and author responses

I did not reopen any concern that earlier rounds marked resolved. I
checked each against the current text.

**Integration R1 (four contract repairs).** All present:

- 02:734–735 charges L, D, q in the global column and L, q in the
  fixed-degree columns.
- 02:495–496 names the minimum-norm selector at accuracy 1/4.
- 09:193–200 transfers the prime-family conclusions and charges the
  binary length of c.
- G:254–258 separates rational from integer scales.

**Integration R2.** The 00 scope repair is present and correct
(Section 3).

**Numerical review (Opus R1 and R2), repair-numerical-r1.** The
attribution and scope repairs are present. Their mathematics was
reconstructed again here.

**Framing R1 and its repair.**

- The abstract hypotheses, core-curvature wording and the
  Slot–Steurer–Wiedmer encoding premise are present (00:44–51).
- Every Hesse comparison is tied to arXiv 2511.03440v1. The bibliography
  entry is the v1 eprint, and no proceedings claim is made.

**Readability R1 (17 reader corrections).** Present. Examples: the chart
vector c̄ versus c₀; the minimum in the interior-Gram Rayleigh quotient;
signed decomposition; the explicit free coordinates in recourse.

**Heights R2.** The optional wording item is resolved at 07:873–880.

**Contrast R1 → repair → R2.** I re-derived:

- the weight hypothesis and k=2 necessity example in `thm:qc-blocks`(d);
- the rational constants and ℭ in `thm:qc-number-field-qp`;
- K's elimination statements and Basu–Mohammad-Nezhad degree floor;
- the two-format input lengths with k>3C.

**Points/constraints/algebraic R1 → repair → R2.** The repaired passages
are present: fixed arcs, isolated nodes, the algebraic-point remark,
`rem:algebraic-curvature`, and the root-circuit definitions.

**Recourse R1 → repair → R2.** Present: the rational Γ majorants, ⟨η⟩
accounting, the affine-hull reduction before Kozlov–Tarasov–Khachiyan,
and the lattice input in [0,1]^r.

**Nonconvex R1 (Q13).** The zero-dimensional chart correction is present
(L proof of `thm:ncq-feasible`).

**Cones R1, Finding 5 → QE-first repair → Cones R2.** Resolved. I
recomposed the bound independently (Section 4.13). The vetted report now
records Khachiyan–Porkolab with the block product in the exponent of the
degree.

**Interim `opus-wholepaper-r1.md` (21:20 UTC).** Item by item:

1. Abstract recourse sentence: fixed in the 21:33 abstract.
2. "Classification … including equality": 03:445–447 now says equality
   has only the upper bound.
3. Allender et al. "reduction": 03:530–533 and 02:448–451 now say
   P^PosSLP by Turing reduction, and the many-one form comes from
   `thm:posslp-closure`(b).
4. Missing Slot–Steurer–Wiedmer premise: present at 00:44–51.
5. Appendix L needed review: done by nonconvex-r1, cones-r1, cones-r2,
   integration-r2 and this review.
6. Source items:
   - The Slot–Steurer–Wiedmer Appendix C description is now consistent:
     Example C.2 is a sextic (00:822, 06:167, vetted report).
   - The Tarasov–Vyalyi basis contract is now a vetted row (Section 4.1).
7. `thm:reductions-min-sign` uses only u₀≠0 (04:470), which the
   compiler display supports.

## 7. Contributions, prior work, structure and readability

**Contributions.** The contribution statements are accurate and scoped:

- Each positive result names its hypotheses, encoding and output format.
- Hardness results are stated as reductions, not lower bounds.
- Order completeness is kept separate from equality.
- Dimension-exponential bounds are kept separate from bounds exponential
  in the input length.

Established ingredients are credited where they are used: Slot–Steurer–
Wiedmer (value approximation, norm bound), Allender et al. and
Etessami–Stewart–Yannakakis (the PosSLP bridge), Tarasov–Vyalyi,
Nie–Ranestad (the generic count), Grigoriev–Pasechnik (sampling),
Khachiyan–Porkolab, Lenstra, Ben-Tal–Nemirovski and Kocuk, KLL, and
Rouillier. In several places the paper explicitly disclaims novelty
(03:447, 07:422, 00:898–913).

A scan for priority and filler phrasing ("the first to", "novel", "to our
knowledge", "remarkable", "crucial" and similar) found none.

**Importance and use.** The paper maps where exact arithmetic becomes
hard in convex polynomial optimization, across four outputs: values,
points, exact decisions, and exact descriptions and certificates. The
solver consequences in Section 11 are stated as consequences of the
theorems, not as claims about software.

**Structure.** The main text (00–11) gives every result with a proof
sketch or pointer. Appendices A–I give the full proofs, and J–L give
contrasts and extensions. The organization is coherent and the
cross-references resolve.

The paper is about 322 pages. That is permitted by the brief, but it
holds several papers' worth of material. A journal may ask for a long-form
venue or a split. Natural seams are:

1. complexity: 02–05 with A–D;
2. algebraic degree, heights, fields and certificates: 06–09 with E–H;
3. recourse: 10 with I;
4. contrasts and extensions: J–L.

**Readability.** The prose is plain and precise. Definitions come before
use, and each section opens with its point. Appendix L is the densest
part: the projection formula's guards, grid and blocks need careful
reading. The short roadmap before `app:cone-projection` helps. I found no
LLM-style filler or unsupported emphasis.

## 8. Source gates versus internal mathematics

The mathematics in my scope has no open internal step. The external
contracts it imports stand as follows at my snapshot, from the evidence
files. I did not check the sources myself.

| Contract | Used in | Recorded status |
| --- | --- | --- |
| Basu 2014 Thm 2.27, fixed blocks, pp.16–17 | L radius; one-block form in 03 | Row in vetted report |
| Khachiyan–Porkolab Thm 1.1, quantifier-free case | L radius | Row in vetted report |
| Lenstra 1983 §5 | L final MILP | Row in vetted report |
| Ben-Tal–Nemirovski Thm 1.1; Kocuk 2021 | L rational lift | Row in vetted report. The manuscript's own lift proof is complete. |
| KLL Thm 1.19 (exact threshold) | J `thm:qc-kll`; L recovery | Row in vetted report. Its threshold matches the manuscript's strict-inequality form. |
| Serre Prop 3.3.5 / Thm 3.4.4 | J `thm:qc-sharp` | Row in vetted report |
| EGH CB7; Eisenbud–Harris 1987 | E (AG3), (AG6) | Rows in vetted report |
| Renegar Part III Thm 1.1 | Recourse QE | Row in vetted report |
| Luo–Zhang Cor. 2 (1997 report) | J attainment | Row in vetted report |
| Tarasov–Vyalyi Thms 3–4 (arXiv v1) | 00:802, `rem:models-socp` | Row in vetted report; the bibliography note maps the theorem numbers to v1 |
| Krick–Pardo–Sombra §1.2.1 | L generic-degree lemma | Noted as verified in the vetted report (Heintz entry, 21:37 UTC); the Heintz attribution was removed |
| Grigoriev–Pasechnik Thm 1.2 (not Thm 1.5) | L `thm:ncq-feasible` | Reported confirmed by the literature lead (`authoring/further-arithmetic.md`); no row yet |
| Dedieu–Malajovich–Shub §5 Thm 5.1 | J `thm:qc-bezout` | Locator reported vetted (cones-r2); no row yet |
| Bombieri–Gubler | J, L heights | Conventions only; the needed inequalities are proved in J. No row yet. |
| Textbook contracts (Rockafellar, Neukirch, Davenport, Kozlov–Tarasov–Khachiyan, von zur Gathen–Gerhard, Hartshorne, Eisenbud 1995, Deimling, Hoffman) | J, K, I, E | Listed as pending in repair records. STATUS reports critical checks passed; no rows. |

These rows are a recording task for the literature lead. None changes a
proof in this review's scope.

## 9. Limitations

- **Sources.** I did no literature research and checked no source.
  Source status comes entirely from the vetted report and root's relays
  (Section 8).
- **Finite certificates.** Printed finite certificates were spot-checked,
  not fully verified: Γ_F, N_F, M⋆ minors, the 15×15 N certificate, and
  the H-tree data. Verifying them fully needs exact rational arithmetic,
  which this round did not run. The proofs that use them are otherwise
  complete.
- **Earlier context.** My reading of Sections 00–10 and Appendices A, C,
  D, E, G, H, I and L happened earlier in this session, before a context
  compaction. The hand checks recorded above come from that pass. I
  reconstructed those files from my own read outputs and confirmed by
  diff that every later change is the one listed in Section 3.
- **Moving files.** The manuscript changed during the review (Section 3).
  The hashes in Section 11 are the snapshot I finally verified. Any edit
  after them needs a changed-scope check.
- **Not peer review.** This review cannot guarantee acceptance or rule
  out issues an external referee may raise.

## 10. Targeted checks actually run

All checks were read-only and local. None is a CI result. No build,
compile, experiment, historical script, CAS or project-wide check was run.

- **Hash snapshots.** `sha256sum` on all manuscript sources at 20:46,
  21:12, 21:32 and 21:37 UTC, and again after writing this report.
- **Text recovery and diffs.** An inline Python script rebuilt each
  earlier file version I had read (00, 01, 06, 08, 09, E, L, and several
  evidence files) from my session's own read outputs. `diff` then
  compared each with the current file. On the unchanged 01, the rebuild
  differed only by one trailing empty line.
- **References and citations** (inline Python): 25 included TeX files
  (abstract, Sections 00–11, Appendices A–L), 658 labels with no
  duplicates, and 1,766 references with none unresolved. 120 distinct
  cited keys all resolve in `references.bib`, which has 126 entries and
  no duplicate keys; 6 entries are uncited.
- **Hygiene scan** (inline Python): no `TODO`, `FIXME`, `ROOT-CITE`,
  `LIT-REQUEST`, `??`, repository paths, agent names or comment lines in
  any manuscript source. `\begin`/`\end` counts balance in every file.
  No trailing whitespace, tabs or missing final newlines.
- **Wording scan** (inline Python): priority and filler phrasing, as in
  Section 7.
- **This report:** `git diff --no-index --check /dev/null` (result in
  Section 11).

## 11. Final SHA-256 snapshot

Manuscript sources as finally verified (21:37 UTC, rechecked after
writing):

```text
42d390dfbeba1fd2459f150f1ce52901c91420d45e8799dc2ae9ef00a1be3d2b  main.tex
1eb51a834c6285ec54212db5dffc0e85c7d0c59a131df32cd7741cc2a273ebf8  macros.tex
20dbe6573a5b4be6749c6c188a6adbfe3a123e21d7599d14a07ca1fd67e3f7a5  references.bib
2dce96e179d21f96ed1b240bf17e040803b440c88013e8cce2d41b34f96d9537  sections/abstract.tex
697822ed8c772532c85172845cce06742c6a07dd18591d393f8fa55a0506c96b  sections/00-introduction.tex
f1883295ee64b7b75e17d2c86d26202169f852741934095a4efcff718d900fb0  sections/01-models.tex
9255c3b578fbef9981d96873db3effe3a0f65345fcab796bbed3e16d1f88e010  sections/02-points.tex
0db409d6a3b1e406e5e882d51311fb2df15ec345b23bea4667d61eaf7f6c2ee5  sections/03-upper.tex
0673ebfc72cfd606b7ce7d3f35d6e027520fa59188f4540b5c657f69b7ebd50e  sections/04-reductions.tex
0216cf2456eb982b40ea206dcb9f0fe4739eefd9b7b029d7b786b38a9599dc9e  sections/05-constraints.tex
cec67b102b0aef0b3a03f1f00abb8ed79cd1dd128f2fac50a0c7d2190a8ea0bb  sections/06-algebraic.tex
2cfaf3f0c8a4e6c144f3fb8b241bcdcba7a3683167c55adac4ea641a8090bbe1  sections/07-heights.tex
b05a1d5d0323344ce05eb679f4ac8651dca7cdea96360f5bdb549aeb46e4324e  sections/08-fields.tex
200313954066e5071cf3a25ec9d0f5c7a28e252b375297f2b9ec5a0515165c98  sections/09-certificates.tex
e38150a05d990980800c9e29724c6dcbe011932167b8331ff7ad88fffbe6b6b1  sections/10-recourse.tex
63252f4d6614dca06df90fa9476a6408ed6f8fb43eaeae9000ec77d0fec97440  sections/11-discussion.tex
e0a65e32b8d02c2b30d29882c71c37d8f781388a73aa53bbc13dba9fbad5269d  appendices/A-upper.tex
1c78b5cd28b75854390eac3d8f48ffa6c623ecb7061f3bc4142375d70a692b94  appendices/B-reductions.tex
0469412f5fc0bb8a9122329e673a30690a2c6ddf9eb577f3844e7b39f04bde90  appendices/C-points.tex
3e7a43c5d884a915d99d0e9f46026d0d77ef1403ec04ab0157c4da03b194130e  appendices/D-constraints.tex
9fe8e892b59bccab190e7ba51eac50bb8c41faa97ca24bf7631c9a0484fa8b03  appendices/E-algebraic.tex
523e1364bd3cc09c05d4f79d889826a1d4b010ead6276e8c1e71629b85d021d3  appendices/F-heights.tex
0c4ddf55ba158ccd8c3857002eaea8805d15373d183f46b785777d50117cfeb1  appendices/G-fields.tex
37ca5a03d9cbb382b9ffe327ab6894e3b43664f9a2c9e405527a37fa47f1a7c5  appendices/H-certificates.tex
f4c21d1ad36fac74449315f3b4a20c4c1652e41e50797e657796c8b0e526d155  appendices/I-recourse.tex
5d01e18401f2fde9d3c2e62d0dde59784101b923ed84980b972266b15e01b3d9  appendices/J-quadratic-contrast.tex
ed88ea5a7c14d38370861141adb3a613a41f7e2cfd4fef42ef663af098568b82  appendices/K-boundaries.tex
6ba31da31c905495c68e575ea27c914efd82dae83b7796857d611530dafe0059  appendices/L-further-arithmetic.tex
```

Literature report read: `evidence/literature-review.md` as of 21:37 UTC.
