# Scout report: open-problem sweep, 2024–2026

Area: `open-problem-sweep`. Date: 2026-09-28. Scratch files:
[open-problem-sweep/](open-problem-sweep/).

**Main finding.** Open problems stated in recent MINLP-related papers are
plentiful, but few are both important for solvers and tractable within
weeks outside topics already developed locally or owned by parallel
scouts. The best quick, verifiable target settles an explicit conjecture:
separating split inequalities for integer quadratic programs is NP-hard.
Burer and Letchford conjectured this, and de Meijer et al. restated it as
open in March 2026. This scout's first-pass reduction proves NP-hardness
even for positive definite input; it still needs independent review and a
lattice-literature priority check. The most substantial candidate is Del
Pia and Khajavirad's treewidth-hardness Statements 1–4. First-pass work
shows why the obvious reduction fails, identifies a natural test family,
and gives a possible repair route.

Throughout, "open" means that no resolution turned up in the searches
recorded in §1.3. An unsuccessful search does not establish novelty or
openness.

---

## 0. Ranked list

Scores run from 1 to 5:

- **I** (importance): value to MINLP solvers or major applications.
- **T** (tractability): expected progress by a strong theory team within
  weeks.
- **V** (verifiability): whether proofs are checkable, computations
  possible, or the result is Lean-formalizable.

Rank follows I×T×V, with ties broken by importance and then by overlap
with local work. Status reflects the checks in §1.3. Quotes marked (✓)
were checked against the primary text by this scout. The others were
extracted from full text by delegated sub-sweeps within this scout and
were not re-read here.

| # | Problem (short) | First 2024–26 statement (location) | Status | I | T | V | Overlap / note |
|---|---|---|---|---|---|---|---|
| 1 | Complexity of separating split inequalities for integer QP | de Meijer–Piccialli–Sotirov–Sudoso, [arXiv:2603.28979](https://arxiv.org/abs/2603.28979) §4 p.11 (✓); Burer–Letchford conjecture, restated by [Buchheim–Traversi](https://optimization-online.org/2013/07/3953/) pp.3, 8 (✓) | Open in literature; **NP-hardness proved in first pass here (§3.1)** | 3 | 5 | 5 | None |
| 2 | Dey–Kocuk Conjecture 2: pairwise 3×3 blocks match full PSD | [arXiv:2510.16595](https://arxiv.org/abs/2510.16595) §4.2.1 p.21, Concl. p.24 (✓) | Open; Conj. 1 resolved by [2605.15970](https://arxiv.org/abs/2605.15970) Prop 5.7 | 2 | 4 | 5 | Row hulls cite the paper; conjecture not pursued locally |
| 3 | Del Pia–Khajavirad Statements 1–4: treewidth hardness and extension complexity at bounded rank | [arXiv:2410.23045](https://arxiv.org/abs/2410.23045) end of §2.1 p.11, §2.2 pp.13–14 (✓) | Open even at constant rank | 3 | 3 | 4 | Adjacent to local multilinear work (hulls, not lower bounds) |
| 4 | Bounded IQP at inertia (1,1,n−2); noncopositivity with fixed negative index ≥ 2 | Ari–Hildebrand, [arXiv:2604.04851v2](https://arxiv.org/abs/2604.04851) §9 (✓) | Open | 3 | 3 | 4 | **Owned by `fixed-dimension-frontier`** |
| 5 | When continuous multipliers strengthen RLT (Hof–Walter Q12–15) | [arXiv:2511.13805](https://arxiv.org/abs/2511.13805) §6 (✓, local) | Open | 3 | 3 | 4 | None |
| 6 | Quadratic lift hull of a 2-D box with bounds on the product xy | Anstreicher–Burer–Park 2021 §5, restated in Zhang–Ouyang–Yang [arXiv:2608.16836](https://arxiv.org/abs/2608.16836) p.2 | Partially resolved: quadrant and a [1/2,2]² piece in 2608.16836 and [2608.26639](https://arxiv.org/abs/2608.26639) | 3 | 3 | 4 | Adjacent to McCormick (covered) |
| 7 | Exact convex representation of QP over m ≥ 3 balls | Burer, Math. Prog. 2024 ([arXiv:2303.01624](https://arxiv.org/abs/2303.01624)) abstract and conclusions; Sun–Kılınç-Karzan 2025 ([arXiv:2407.14992](https://arxiv.org/abs/2407.14992)) p.1 | Open; Burer's other two conjectures resolved by Sun–Kılınç-Karzan | 4 | 2 | 4 | None |
| 8 | Do relaxed second-order conditions strengthen SDP-RLT for general QP? | Yıldırım, JOGO 2026 ([arXiv:2506.09892](https://arxiv.org/abs/2506.09892)) §5 (✓, local) | Open; box QP analogue known (Burer–Chen) | 2 | 4 | 4 | None |
| 9 | Second semidefinite lifting exact for complex cut polytope CUT⁴∞ | Sinjorgo–Sotirov–Anjos, [arXiv:2402.04731](https://arxiv.org/abs/2402.04731) Conj. 1 | Open | 2 | 4 | 4 | None |
| 10 | sBB convergence for discontinuous piecewise-linear functions | Hübner–Gupte–Rebennack, IJOC 2026, pp.17, 34 (local) | Open | 2 | 4 | 4 | None |
| 11 | Optimal piece count for CPWL approximation of xy | Ploussard et al., [arXiv:2608.27312](https://arxiv.org/abs/2608.27312) Concl. p.21 (✓, local) | Partially resolved by sub-sweep lemma (unreviewed; priority unchecked) | 2 | 3 | 5 | Adjacent to local MIP-relaxation counts |
| 12 | Hildebrand–Göß Conj. 47 (boundary hyperplane cover, ball vs quadric) | [arXiv:2409.05308v2](https://arxiv.org/abs/2409.05308) §7.2 | **False as literally stated** (checked here, §2.4); corrected form open | 1 | 5 | 5 | None |
| 13 | Finite convergence of pure concavity-cut method with Konno's cut | Qu–Zeng–Lou, MPC 2025 ([arXiv:2302.05930](https://arxiv.org/abs/2302.05930)) §4.4 p.28 (✓, local) | Open (restates Horst–Tuy) | 2 | 3 | 4 | None |
| 14 | NP-hardness of minimal SOC representation of power cones (α-MCMGP) | Blanco–Martínez-Antón, SIOPT 2024 ([arXiv:2311.10470](https://arxiv.org/abs/2311.10470)) §4.1, Concl. | Open | 3 | 2 | 4 | None |
| 15 | Recognizing bounded nest-set gap/width; testing Boros's local boundedness | 2410.23045 §3.1–3.2; Boros, [arXiv:2607.08908](https://arxiv.org/abs/2607.08908) §3.2 | Open | 2 | 3 | 4 | Adjacent to multilinear |
| 16 | Must the IP value-function period grow doubly exponentially in m? | Ligthart, [arXiv:2606.30330v2](https://arxiv.org/abs/2606.30330) App. A | Open | 2 | 3 | 4 | Linear IP theory |
| 17 | (R,G)-finite generation of SOC(n) ∩ Zⁿ for n ≥ 11 | De Loera–Marsters–Xu–Zhang, [arXiv:2403.09927](https://arxiv.org/abs/2403.09927) v3 | Open | 2 | 3 | 4 | Possibly `micp-representability` |
| 18 | Necessary and sufficient SDP/DNN tightness on cycle patterns | Azuma–Kim–Yamashita, [arXiv:2607.16796](https://arxiv.org/abs/2607.16796) Concl. | Open | 2 | 3 | 4 | None |
| 19 | Convex hull of the Atamtürk–Gómez conic mixed 0–1 set | Du–Chen–Wei, [arXiv:2511.00452](https://arxiv.org/abs/2511.00452) p.1 | Open (low confidence) | 3 | 2 | 4 | Adjacent to indicator work |
| 20 | Is IQP FPT in (number of variables + number of constraints)? | Herrmann, [arXiv:2608.17818](https://arxiv.org/abs/2608.17818) §3 | Open | 3 | 2 | 4 | **Owned by `fixed-dimension-frontier`** |
| 21 | NP-hardness of robust bilevel selection (interval uncertainty) | Henke, [arXiv:2401.03951](https://arxiv.org/abs/2401.03951) §5; OWR 2023/35 | Open | 2 | 3 | 4 | Adjacent to bilevel |
| 22 | Duality gaps beyond i.i.d. blocks | Hübner, [arXiv:2503.02464](https://arxiv.org/abs/2503.02464) §5 | Open (loosely posed) | 2 | 3 | 4 | None |
| 23 | SOS rank of unweighted min-knapsack MK(q) | Kurpisz–Slot–Zaytsev, [arXiv:2605.00594](https://arxiv.org/abs/2605.00594) §1.1–1.2 | Partially resolved | 1 | 4 | 5 | None |
| 24 | SOS certificate degree for a quadratic nonnegative on two quadrics | Blekherman, OWR 2025/9 open problems, p.446 | Open, **ill-posed as recorded** (trivial P = 0) | 3 | 2 | 3 | None |
| 25 | Recovery threshold of the complete LP for rank-one Boolean tensor factorization | Del Pia–Khajavirad, MOR 2025 ([arXiv:2202.07053v3](https://arxiv.org/abs/2202.07053)) §1.4 | Open | 2 | 3 | 3 | None |
| 26 | Quantify DNN gaps from 5-vertex defect components in random StQP | Chen, [arXiv:2605.11456](https://arxiv.org/abs/2605.11456) §7.2 | Existence answered by a sub-sweep instance (not re-verified); quantification open | 1 | 4 | 4 | None |
| 27 | Tight iteration bounds for δ-relaxed polyblock outer approximation | Rashwan, [arXiv:2608.13694](https://arxiv.org/abs/2608.13694) Thm 2, Concl. (✓, local) | Open | 1 | 4 | 4 | None |
| 28 | Remove log n in separable convex IP with small dual treedepth | Hunkenschröder–Koutecký–Levin–Vu, [arXiv:2505.22212](https://arxiv.org/abs/2505.22212) open problems | Open | 2 | 2 | 3 | None |
| 29 | Subgradients of ODE relaxations without non-coincidence | Song–Khan, OMS 2024, §3.1 | Open | 2 | 2 | 3 | None |
| 30 | Minimal difference-of-convex decomposition of CPWL functions | Brandenburg, OWR 2025/12, Problem 1; [arXiv:2410.04907](https://arxiv.org/abs/2410.04907) | Open | 2 | 2 | 3 | None |
| 31 | Exact 2^{O(n)} algorithm for integer maximization over a Euclidean ball | Ari–Hildebrand, [arXiv:2609.15114](https://arxiv.org/abs/2609.15114) §8 | Open | 3 | 1 | 3 | Fixed-dimension adjacent |
| 32 | Complexity of unbalanced Procrustes | Chandrasekaran et al., [arXiv:2510.06112](https://arxiv.org/abs/2510.06112) §1.3 | Open | 2 | 1 | 3 | None |

Lower-priority open items, recorded briefly:

- Owned by other scouts: bit-oracle lower bounds for mixed-integer convex
  optimization (Basu–Kerger–Molinaro, [arXiv:2511.02082](https://arxiv.org/abs/2511.02082)
  §1.3; partly addressed by Kerger, [arXiv:2607.13335](https://arxiv.org/abs/2607.13335)),
  Oertel's conjecture (Cheng–Basu, [arXiv:2603.00286](https://arxiv.org/abs/2603.00286)),
  and "is integer cubic optimization in NP?" (Del Pia,
  [arXiv:2511.02983](https://arxiv.org/abs/2511.02983) v1 p.2).
- Hard real algebraic geometry: convex forms that are not SOS, with the
  smallest quartic dimension between 5 and 272 (Ahmadi–Blekherman–Parrilo,
  [arXiv:2404.14440](https://arxiv.org/abs/2404.14440) p.10); Putinar's
  theorem over ℚ (Baldi–Krick–Mourrain, [arXiv:2410.04845](https://arxiv.org/abs/2410.04845));
  components of two multi-affine zero sets (Basu–Perrucci, OWR 2025/9).
- SOS proof complexity: decidability of SoS-CSP (Bortolotti–Mastrolilli–Vargas,
  [arXiv:2504.17756](https://arxiv.org/abs/2504.17756)); bit size of
  symmetric SoS proofs with many constraints ([arXiv:2509.06928](https://arxiv.org/abs/2509.06928)).
- Ill-posed as literally stated: whether every nonnegative form has a
  disjunctive SOS proof (Ahmadi–Dash–Hua–Stellato,
  [arXiv:2605.28674](https://arxiv.org/abs/2605.28674) §7). Taking the
  disjunction D = {{p}} is trivial, so a sign-pattern restriction is needed.
- Not MINLP-specific: balanced independence number of the hypercube (OWR
  2024/50); Reinhardt perimeter for n = 2^s ≥ 16 (Mulansky–Potschka,
  [arXiv:2404.01841](https://arxiv.org/abs/2404.01841)); convex indegree
  objectives (Borsik–Madarasi, [arXiv:2509.06182](https://arxiv.org/abs/2509.06182)).

### 0.1 Exact statements of the ranked problems

Each entry summarizes the cited question, gives the relevant mathematical
conditions, and records the resolution check. Source prose is paraphrased.

1. **Split separation.** The paper 2603.28979 (p.11) identifies detection
   of violated cuts as the practical obstacle and leaves the complexity
   of split separation unresolved. Buchheim–Traversi (OO 2013/07/3953,
   p.3) likewise report no polynomial-time separation algorithm and
   endorse Burer–Letchford's conjecture of NP-hardness [8].
   - *Restatement.* Given a rational symmetric Y indexed 0..n with
     Y₀₀ = 1, decide whether some v ∈ ℤⁿ⁺¹ has
     ⟨v(v+e₀)ᵀ, Y⟩ = vᵀYv + vᵀYe₀ < 0.
   - *Check.* The 2026 paper still calls it unclear. Buchheim–Traversi's
     Theorem 5 handles only non-PSD Y. No resolution was found.
2. **Dey–Kocuk Conjecture 2.** The conjectured equality is
   S^κ_{P,R,s3} = S^κ_{P,R,S}.
   - *Restatement.* Take G = Δⁿ and κ > 1. PRs3 requires X ≥ 0, Xe = x,
     the linking constraints (5), and
     [[X_ii, X_ij, x_i], [X_ij, X_jj, x_j], [x_i, x_j, 1]] ⪰ 0 for all
     i < j. PRS instead requires [[X, x], [xᵀ, 1]] ⪰ 0. The conjecture
     says both have the same (x, y)-projection.
   - *Check.* Blekherman–Dey–Dunbar–Kocuk (2605.15970) prove Conjecture 1
     (PRS exact at κ = 2) and do not mention Conjecture 2.
3. **Del Pia–Khajavirad Statements.**
   - *Statement 2 (paraphrased).* Consider a family {G_k} that can be
     enumerated in polynomial time, with tw(G_k) = k for every k and
     rank r(k) bounded by a log-poly function of k. If an algorithm f
     solves every Problem BMO instance Λ_k on G_k within
     T(k)·poly(‖Λ_k‖), the assumption NP ⊄ BPP would force T(k)
     to grow faster than any polynomial in k.
   - *Statement 1* is the same for signed hypergraphs (Problem PBO).
   - *Statements 3–4* claim xc(PBP(H)) and xc(MP(G)) are at least
     2^{Ω(tw^δ + log n)} under log-poly rank.
   - The paper adds that even at constant rank, Statements 1 and 2
     remain open.
4. **Rank-2 indefinite IQP.** The questions concern parameterized
   complexity for bounded IQP with inertia (1,1,n−2), and for
   noncopositivity when the negative index is fixed and at least two.
   - *Restatement.* Is min{(aᵀx)(bᵀx) + cᵀx : x ∈ P ∩ ℤⁿ}, with P a
     polytope, FPT or W[1]-hard in n?
5. **Hof–Walter Question 12.** Characterize the choices of polyhedron
   P ⊆ ℝ^N and B ⊊ N for which R̃_B(P) ⊊ R_B(P). Here R̃_B also multiplies by
   continuous variables and their complements.
   - Q13 asks when RLT dominates the disjunctive hull of a complete
     assignment disjunction.
   - Q14 asks whether Corollary 11 is sufficient.
   - Q15 asks which disjunctions level-k RLT implies.
6. **Box with product bounds.** Describe
   conv{(x, y, x², xy, y²) : l ≤ (x,y) ≤ u, l_z ≤ xy ≤ u_z}.
7. **Balls.** The cited work reports no explicit tractable convex
   representation that is exact for m ≥ 3. For fixed m ≥ 3, give an
   explicit polynomial-size exact convex (for example disjunctive SDP)
   description of conv{(x, xxᵀ) : ‖x − c_i‖ ≤ ρ_i, i ≤ m}.
8. **Second-order conditions.** The authors propose examining the
   construction for general quadratic programs and testing whether
   it retains equivalence to the original SDP relaxation. Question: is
   there a QP with a finite SDP-RLT bound that strictly increases when
   relaxed second-order necessary conditions are added?
9. **CUT⁴∞.** Conjecture 1 asserts exactness of the second semidefinite
   lifting for CUT4∞: L(B₁) = CUT4∞.
10. **Discontinuous PLF sBB.** The authors report that their available
    branching rules do not establish asymptotic convergence for a
    non-l.s.c. PLF.
11. **xy pieces.** The authors conjecture that their function g_n is
    optimal in efficiency among CPWL approximations of the unit bilinear
    term, but leave that optimality claim unproved.
    - g_n has error 1/(16n²) and 2n(n+1) convex pieces.
    - A sub-sweep sketched an area lemma: a convex region K on which
      |xy − ℓ| ≤ ε for an affine ℓ has area at most 8ε. This gives a
      lower bound of 2n² pieces. The sketch is unreviewed, and the lemma
      may be classical (Pottmann et al. 2000; Atariah–Rote–Wintraecken).
12. **Conjecture 47.** The conjecture asserts that the condition in
    Lemma 46 is necessary as well as sufficient. See §2.4.
13. **Konno's cut.** The cited work leaves convergence unresolved when
    its stated conditions are omitted.
14. **α-MCMGP.** The proposed complexity classification is NP-hardness
    of α-MCMGP in general.
    The problem is the minimum number of 3-dimensional rotated
    second-order cones needed to represent x ≤ z^α. This is the
    sub-sweep's reported conjecture; this scout's local grep found only
    the further-research paragraph.

Items 15–32 are stated in the table in enough detail to be located; the
sub-sweep records behind them hold the verbatim quotes.

### 0.2 Resolved or closed in 2024–2026 (do not pursue)

| Former open question | Resolution |
|---|---|
| Polynomiality of (M)IQP in fixed dimension; bounded integer cubics | Ari–Hildebrand [2609.18266](https://arxiv.org/abs/2609.18266) (Sep 2026, unrefereed); Wei (Optimization Online, pure integer) |
| Is IQP FPT in n alone? | No: W[1]-hard, Herrmann [2608.17818](https://arxiv.org/abs/2608.17818) |
| MIQP approximation with fixed integer count and fixed negative eigenvalues | Del Pia [2607.29386](https://arxiv.org/abs/2607.29386) |
| Del Pia's thin-ray conjecture for integer cubic unboundedness | Proved in v2 of [2511.02983](https://arxiv.org/abs/2511.02983) |
| 4-block IP FPT (Eisenbrand–Rothvoss question) | [2609.23711](https://arxiv.org/abs/2609.23711), [2609.26746](https://arxiv.org/abs/2609.26746) |
| Koutecký IPEC 2025 separable-convex question | Ligthart [2606.30330](https://arxiv.org/abs/2606.30330) |
| Zonotope containment and ℓp maximization over zonotopes, FPT in d | W[1]-hard: [2509.22849](https://arxiv.org/abs/2509.22849), [2608.24865](https://arxiv.org/abs/2608.24865), [2608.15847](https://arxiv.org/abs/2608.15847) |
| Dey–Kocuk Conjecture 1 (DNN exact for separable StQP) | [2605.15970](https://arxiv.org/abs/2605.15970) Prop 5.7 (✓) |
| Burer's conjectures: lifted ball relaxation vs Kronecker RLT; redundancy of the Zhen et al. inequality | Sun–Kılınç-Karzan [2407.14992](https://arxiv.org/abs/2407.14992) (✓ local) |
| Delorme–Poljak: complexity of recognizing exact Max-Cut SDP, including unweighted graphs | NP-complete, Bhardwaj [2609.03508](https://arxiv.org/abs/2609.03508) (✓ local; single author, unrefereed). Two Mirka–Williamson questions are answered in a SIAM OP26 abstract (Gogoi–Bhardwaj–Narayanan) |
| Lasserre rank of Laurent's cropped hypercube | Cornuéjols–Patil–Wei [2609.27748](https://arxiv.org/abs/2609.27748) |
| de Klerk–Pasechnik conjecture | Baek–Vargas [2609.01010](https://arxiv.org/abs/2609.01010) (GPT-assisted, unrefereed) |
| Lee–Prakash–de Wolf–Yuen and Bienstock–Zuckerberg SoS-rank conjectures | Refuted (SIAM OP26 abstract MS253 in the local SIAM abstracts file `oh2026-convexification-of-a-class-of`) |
| Convex ternary quartics are SOS-convex | Ahmadi–Blekherman–Parrilo [2404.14440](https://arxiv.org/abs/2404.14440) |
| Nesterov's convex polynomial programming question | [2511.03440](https://arxiv.org/abs/2511.03440) (known locally) |
| Belotti's lower envelope on wedges for n > 2 | Yang–Zhang 2026 (local `zhang2026-flat-lower-envelopes-solve-bounded`) |
| MESP: does g-scaling improve the factorization (Γ) bound? (Fampa–Lee survey [2507.05066](https://arxiv.org/abs/2507.05066) §3.2, ✓) | No, for standard MESP: Shen–Kılınç-Karzan [2604.10363](https://arxiv.org/abs/2604.10363) Thm 3 (✓) |
| Xia's GTRS conjectures 5.6 and 5.10 | 5.6 confirmed, 5.10 disproved: [2409.01697](https://arxiv.org/abs/2409.01697) |
| Nonhomogeneous Calabi theorem and strict Finsler lemma for two quadratics | [2608.30571](https://arxiv.org/abs/2608.30571) (abstract only) |

---

## 1. Frontier map

### 1.1 Strongest relevant 2024–2026 results

| Result | Assumptions | Conclusion | Bearing on the list |
|---|---|---|---|
| Ari–Hildebrand 2609.18266 | Rational polyhedron, fixed dimension, quadratic objective; or bounded polytope with cubic objective | Exact polynomial-time optimization | Closes the classical fixed-dimension question; items 4 and 20 remain |
| Herrmann 2608.17818 | Integer QP, parameter = number of variables | W[1]-hard; uses O(k²N²) constraints | Leaves the parameter n + m open (item 20) |
| Blekherman–Dey–Dunbar–Kocuk 2605.15970 | Copositive A whose off-diagonal entries are nondecreasing in rows and columns | A is PSD + nonnegative (SPN); the DNN relaxation of separable StQP is exact | Base for item 2 (§3.2) |
| Del Pia–Khajavirad 2410.23045 | Polynomial-time enumerable families; log-poly rank; NP ⊄ BPP | Treewidth hardness for BQO and for PBO when all signed hypergraphs over G_k are allowed; xc ≥ 2^{Ω(tw^δ)} for some signing | Item 3; the single-hypergraph versions are open |
| Sun–Kılınç-Karzan 2407.14992 | QP with m balls | Burer's lifted relaxation dominates Kronecker RLT | Item 7 remains |
| Bhardwaj 2609.03508 | Max-Cut SDP, unweighted graphs | Recognizing exactness is NP-complete | Closes a 1993 question |
| Hof–Walter 2511.13805 | Polyhedra P ⊆ [0,1]^N, binary index set B | Geometric characterization of RLT closure points; RLT dominance over certain disjunctions | Item 5 |
| Buchheim–Traversi (OO 2013; Discrete Optim. 2015) | Any symmetric Y with Y₀₀ = 1 | Non-PSD Y: violated split found in polynomial time (Thm 5). PSD Y: separation is convex IQP | Item 1 |
| Shen–Kılınç-Karzan 2604.10363 | MESP with X = {x ∈ [0,1]^d : 1ᵀx = s} | Convex–concave structure of g-scaled Γ; g-scaling cannot improve Γ | MESP question closed |

### 1.2 Local-coverage and parallel-scout check

This scout read [open-theory-challenges](../../literature/topics/open-theory-challenges.md),
the [direction audit](../../research-20260925/direction-audit.md), the
[Sept 22 literature scout](../../research-20260922/scouting/scout_literature.md)
(its ten ranked questions and overlap table), and
[notes/open-problems-from-literature.md](../../notes/open-problems-from-literature.md).
Overlaps:

- Eigen-CG Conjecture 1 is already investigated locally and remains open
  ([research-20260922/eigen-cg](../../research-20260922/eigen-cg/investigation.md)).
- The Kannan–Barton clustering question, point packing (Anstreicher
  Conjecture 4), the Dey–Kocuk–Santana rank-one conjecture, Luedtke et
  al. Conjecture 1 and Geoffrion Property (P′) are all addressed locally.
- Items 4 and 20 belong to `fixed-dimension-frontier`. Oertel's
  conjecture and information complexity belong to `mi-centerpoints`.
  (R,G)-generation (item 17) may belong to `micp-representability`.
  Maximal quadratic-free sets belong to `s-free-intersection-cuts`.
- None of the top three ranked items is developed locally.

### 1.3 Sources examined and what was checked

This scout directly read or grepped the following:

- **Full text, relevant sections.** arXiv 2603.28979 (§4, split
  inequalities); Buchheim–Traversi OO 2013/07/3953 (pp.1–9, separation
  discussion and Theorem 5); 2510.16595 (§2, §3.2, §4.2.1, conclusion);
  2605.15970 (abstract, §5); 2410.23045 (§2.1–2.2 and statements);
  Fampa–Lee 2507.05066 (§3.2 open question); Shen–Kılınç-Karzan
  2604.10363 (§1, §5).
- **Local library.** Bhardwaj 2609.03508 (abstract, §4–5); Hof–Walter
  2511.13805 (§6); Yıldırım 2026 (§1, §5); Qu–Zeng–Lou (p.28);
  Ploussard 2608.27312 (conclusion); Rashwan 2608.13694; Belotti 2025
  and Yang–Zhang 2026; De Rosa–Khajavirad 2024; Elgersma 2024; Kelley
  2025; Hübner–Gupte–Rebennack 2026; Dey–Khajavirad 2025; Burer 2025;
  Sun 2025; Basu 2025; Del Pia 2025.
- **SIAM OP26 abstracts** (local `oh2026-convexification-of-a-class-of`),
  grepped for open or resolved statements: Max-Cut SDP exactness
  (MS337), SoS ranks on the hypercube (MS253), MESP scaling (MS308),
  convex polynomial programming (MS226), copositive stability number
  (MS131).
- **arXiv API.** "Voronoi relevant" and "Voronoi cell NP" queries, used
  for the split-separation priority check. No hardness paper was found;
  lattice results off arXiv were not reachable.

Delegated sub-sweeps run within this scout read the following. Each
recorded what was examined; statements not re-read by this scout are
unmarked in the table.

- **Integer programming with nonlinear objectives.**
  - Full text: Herrmann 2608.17818; 2609.15114; 2607.29386 (§1);
    2606.30330v2; 2609.23711; 2609.26746; 2505.22212; 2509.06182;
    2409.05308v2; 2511.02082v2; 2511.02983v2 (§1); 2604.04851 (§5–7, §9);
    2609.18266v2 (§1, Remark 7.10); Dagstuhl LIPIcs.IPEC.2025.1.
  - Abstract or grep only: 2602.06897, 2605.30602, 2411.15282,
    2501.00638, 2408.12183, 2603.00286, 2511.03440.
  - Local: Del Pia 2019 and 2025, Basu 2025, Verschae 2023 and 10 others.
- **QCQP and conic hulls.**
  - Full text or grep: 2605.11456, 1604.02172, 2510.16595, 2605.15970,
    2303.01624, 2608.26639, 2510.06112, 2511.00452, 2603.28979,
    2211.05645, 2608.30571, 2601.13511, 2409.01697, 2411.03103,
    2407.13407, 2602.14949, 2508.18435, 2501.09150, 2403.04752,
    2402.08827, 2502.15206, 2304.04174, 2608.03318, 2604.25033,
    2504.16330, 2303.18158, 2603.18215, 2502.13849, 2512.06437,
    2609.24661, 2305.16224, 2501.03698, 2509.23696, 2502.20133.
  - Local: about 25 papers, including Hof–Walter, Azuma 2026, Zadik 2024
    and Kılınç-Karzan 2025.
- **Global optimization and convex MINLP.**
  - Local full texts, about 70: Ploussard, Blanco (three papers),
    Dey–Kocuk, Hübner (two), Qu, Yıldırım, Rashwan, Song–Khan, Stargalla,
    Basu, Glaser, Cornuéjols, Dey–Xu, Murota–Tamura, Lefebvre, Burlacu,
    Lyu, Huchette, Vera, Casado, Kuchlbauer, Wei, Go, Halbig, Kronqvist.
  - arXiv pages: 2605.15970, 2510.02948, 2607.13335, 2406.00576,
    2604.23383, 2501.00638, 2501.11397, 2502.03288, 2604.04889,
    2602.06637, 2510.11497, 2406.12436, 2507.16496, 2308.04320.
  - About 20 arXiv title searches (outer approximation, Shapley–Folkman,
    surrogate duality, bound tightening, spatial branch, and others).
- **Polynomial and binary optimization.**
  - Full text: 1605.03019, 2609.27748, 2504.17756, 2509.06928,
    2404.14440, 2511.02983v1, 2507.12831v2, 2607.08908v2; Slot–Laurent
    2011.04027 (concluding section).
  - Abstract only: 12 further arXiv ids.
  - Semantic Scholar citation lists for 19 papers.
  - Local: Del Pia–Khajavirad (four papers), Hof–Walter, Kurpisz 2026,
    Baldi 2025, Ahmadi 2026, Baek 2026, Kunisky 2024.
- **Workshops and surveys.**
  - Full text of open-problem sections: OWR 2023/35 (MINLP "hatchery"),
    OWR 2024/50, OWR 2024/35, OWR 2025/9, OWR 2025/12; BIRS 25w5372
    report; Dagstuhl 25371; Randomstrasse101 2024 and 2025 (arXiv
    2504.20539, 2603.29571).
  - Full text of papers: 2402.04731, 2404.01841, 2401.03951, 2403.09927,
    2308.11153, 2606.21823, 2604.02968, 2409.07213, 2408.05942.
- **Search limits.** The shared WebSearch budget (200 calls) ran out
  during the sweep. Later checks used arXiv listings and the API, local
  full texts, and Semantic Scholar until rate-limited. INFORMS TutORials,
  Acta Numerica, and some paywalled journal versions were not reached.

---

## 2. Open questions that remain open (with evidence)

### 2.1 Split separation for integer QP (rank 1)

The question is stated above. The evidence that it is open:

- Letchford posed it in 2010, and Burer–Letchford conjectured
  NP-hardness (as cited by Buchheim–Traversi).
- Buchheim–Traversi give only the non-PSD case (Theorem 5).
- De Meijer et al. (March 2026, p.11) still call it unclear.
- An arXiv API search for Voronoi-cell membership hardness found no
  paper.

**Caution.** The core lattice step, "is 0 a closest lattice point to t?",
may be folklore in lattice complexity. §3.1 settles the MINLP question
only if the reduction survives review.

### 2.2 Dey–Kocuk Conjecture 2 (rank 2)

The conjecture is stated by its authors. Evidence that it remains open:

- The paper resolving Conjecture 1 does not mention it.
- A search of Kocuk's arXiv listing found nothing newer.

**Caution.** The authors note that PRs3 is computationally dominated by
PRS in their tests, which limits its direct solver value.

### 2.3 Del Pia–Khajavirad Statements 1–4 at constant rank (rank 3)

The authors leave these statements open even at constant rank. The
four citing papers found by the sub-sweep are all positive tractability
results.

### 2.4 Hildebrand–Göß Conjecture 47: false as stated

The sub-sweep's example was re-checked here.

- Let B be the unit ball and C = {x² + 4y² + 9z² ≤ 1}. Then C ⊆ B, and
  ∂B ∩ ∂C = {(±1, 0, 0)}, since 3y² + 8z² = 0 there. The plane y = 0
  covers this set, so a boundary hyperplane cover exists.
- g − α(‖·‖² − 1) has diagonal quadratic part (1−α, 4−α, 9−α). That part
  has rank at least 2 for every α, with signature (2,0), (1,1) or (0,2)
  at α = 1, 4, 9.
- The only candidate is α = 4, giving −3x² + 5z² + 3. A product of real
  affine forms h₁h₂ = (√5z − √3x + a)(√5z + √3x + b) needs a + b = 0 and
  b − a = 0 to cancel the linear terms, hence a = b = 0. Then the
  constant ab = 0 ≠ 3. So g has neither form in Lemma 46, and the "only
  if" direction fails.

The authors presumably intend nondegenerate intersections, such as
∂B ∩ ∂C of dimension n − 2. A corrected statement is a short exercise;
its value is low.

---

## 3. First-pass analyses of the top three

### 3.1 Rank 1: separating split inequalities is NP-hard

**Likely answer.** NP-hard, as Burer and Letchford conjectured, and
expected to be NP-complete for PSD input (membership not yet proved). Here the reduction is proved in outline, but it
has not been independently reviewed.

**Lemma A (lattice form, elementary).** Write Y = BᵀB with columns
B = [b₀, …, b_n]. Then

`q(v) := vᵀYv + vᵀYe₀ = ‖Bv + b₀/2‖² − ‖b₀/2‖²`.

A split inequality is violated exactly when some point of the lattice
Bℤⁿ⁺¹ lies strictly closer to −b₀/2 than 0 does. Both 0 and −b₀ lie at
distance ‖b₀‖/2 from −b₀/2.

**Lemma B (NP-hardness of CLOSER).** CLOSER asks: given a rational
lattice basis C and a target t, is there ℓ ∈ L(C) with ‖t − ℓ‖ < ‖t‖?
It is NP-hard, by reduction from subset sum (a ∈ ℤⁿ₊, s).

- Work in coordinates (sum, n parity coordinates, extra). Take basis
  vectors b_i = (M a_i, 2e_i, 0) and g = (M s, 𝟙, γ), where M ≥ 3 and γ
  is rational with n < γ² ≤ n + 8. Such a γ exists with polynomial size.
- Take the target t₀ = (M s, 𝟙, 0). For a lattice point
  P(x,k) = Σx_i b_i + k g,

  `‖t₀ − P‖² = M²((1−k)s − aᵀx)² + ‖(1−k)𝟙 − 2x‖² + k²γ²`.

- Case analysis:
  - k = 0: the value is at least n, with equality exactly when
    x ∈ {0,1}ⁿ and aᵀx = s. Otherwise it is at least n + 8 or at least
    n + M².
  - k even and nonzero: at least n + 4γ².
  - k odd: at least γ², with equality only at k = ±1 in special
    configurations.
- The point g itself (x = 0, k = 1) is at squared distance γ². So some
  lattice point is strictly closer to t₀ than g exactly when the subset
  sum instance is solvable.
- Translating by g gives t = t₀ − g = (0, 0, −γ) with the same lattice.

**Lemma C (embedding).** Given (C, t), choose a rational h with
8h² ≥ ‖t‖², for example h = ‖t‖₁. Set b₀ = (2t, 2h), b_j = (c_j, 0) and
Y = BᵀB/‖b₀‖².

- Then Y is rational, positive definite, and Y₀₀ = 1.
- Bv + b₀/2 = ((2v₀+1)t + ℓ, (2v₀+1)h) with ℓ ∈ L(C).
- If |2v₀+1| ≥ 3, the squared norm is at least 9h² ≥ ‖t‖² + h², so no
  violation.
- If |2v₀+1| = 1, violation means exactly ‖±t + ℓ‖ < ‖t‖.
- Hence a split is violated iff CLOSER(C, t) holds.

**Consequence (first pass).** Deciding whether a rational positive
definite Y with Y₀₀ = 1 violates some split inequality is NP-hard. In
the YES instances, the violated splits correspond exactly to subset-sum
solutions. Padding the instance so that every solution is large should
keep hardness under the promise that all bounded-support splits hold;
this refinement needs to be written out. Choosing h large also makes
|Y₀ᵢ| ≤ 1 and Y_ii ≤ 1, so Y can satisfy the basic box-SDP constraints.
Other RLT or triangle constraints are not controlled.

**Fixed rank (sketch).** Suppose Y ⪰ 0 has rank r.

- q is invariant under ker Y, which is a rational subspace.
- Let P be a rational r×(n+1) matrix with ker P = ker Y. Then
  Y = PᵀGP with G rational and positive definite, and Λ = Pℤⁿ⁺¹ is a
  lattice of rank r.
- Separation becomes a closest-vector problem in Λ under the form G,
  solvable in r^{O(r)}·poly time by Kannan's algorithm.
- So separation is FPT in rank(Y). The non-PSD case is already
  polynomial (Buchheim–Traversi Theorem 5).

**Computational check.** The script
[split_separation_check.py](open-problem-sweep/split_separation_check.py)
uses exact rational arithmetic on a = (3, 5, 7) and
s ∈ {4, 8, 9, 10, 11, 13, 15, 16}, brute-forcing v ∈ {−2..2}⁵.

- It finds a violated split exactly for the solvable s ∈ {8, 10, 15},
  each time with min q = −1/32.
- For the other s the minimum is 0, attained at v = −e₀.
- This is a sanity check of the construction, not a proof.

**Attack plan** (days to two weeks):

1. Write the full proof, including encoding sizes, strong NP-hardness
   (via an exact-cover CVP reduction), and NP membership for PSD Y. For
   the last, bound a minimal violating v through the lattice picture and
   a Hermite normal form preimage.
2. Settle the bounded-support promise version and the hardness of
   approximating the maximum violation (gap-CVP).
3. Complete the fixed-rank algorithm and give exact separation for
   bounded-coefficient families, for example v ∈ {−1,0,1}ⁿ⁺¹, which
   covers the families used in 2603.28979.
4. Formalize Lemmas A and C and the case analysis in Lean. They are
   elementary algebra over ℤ and ℚ.
5. Run a priority check in lattice-complexity sources (Voronoi-cell
   membership, relevant vectors, Micciancio–Goldwasser) before claiming
   more than "settles the MINLP conjecture".

**Main risk.** The lattice core is probably known in some form, so the
contribution is a short note resolving an explicit MINLP conjecture. Its
solver significance is modest: it justifies heuristic separation and
points to exact low-rank or bounded-support routines.

### 3.2 Rank 2: Dey–Kocuk Conjecture 2

**Likely answer.** True at κ = 2, and probably true in general.

- This scout's runs:
  [dey_kocuk_conj2_check.py](open-problem-sweep/dey_kocuk_conj2_check.py)
  on 60 random instances (n = 3–7, Clarabel) gave a largest gap of
  8.5e−9 for PRs3 and 3.5e−4 for PR.
- Hill climbing that maximized the PR gap found PR gaps of about 0.086
  (n = 5); PRs3 closed these to within 4e−9
  ([search_PR_n5.log](open-problem-sweep/search_PR_n5.log)).
- Hill climbing that maximized the PRs3 gap found at most 3.5e−8
  ([search_PRs3_n5.log](open-problem-sweep/search_PRs3_n5.log)).
- Sub-sweeps found a gap of at most 1.2e−7 on 160 instances at κ = 2,
  and PRs3 = PRS within 4.3e−7 at κ ∈ {1.5, 3}.

**Useful reformulation (κ = 2, derived here).**

- Eliminate x = Xe and use eᵀXe = 1. Each 3×3 block equals W_ijᵀXW_ij
  with W_ij = [e_i, e_j, e].
- The objective becomes ⟨A, X⟩ with A = Diag(β) + (αeᵀ + eαᵀ)/2.
- PRs3 is then min{⟨A,X⟩ : X ≥ 0, ⟨E,X⟩ = 1, W_ijᵀXW_ij ⪰ 0}.
  Slater's condition holds, so its dual is
  max{λ : A − λE − Σ W_ij Q_ij W_ijᵀ ≥ 0 entrywise, Q_ij ⪰ 0}.
- Given the resolved Conjecture 1, Conjecture 2 at κ = 2 is therefore
  equivalent to: for every (α, β), A − λ*E is a nonnegative matrix plus
  a sum of PSD matrices, each with range in some span{e_i, e_j, e}.
- Blekherman–Dey–Dunbar–Kocuk give an SPN decomposition (with an
  unrestricted PSD part), because a_ij = (α_i+α_j)/2 is ordered after
  sorting α.
- Pieces with range in span{e_i, e} alone give exactly PR, which is not
  exact (their Proposition 3). So the pair structure is essential.

**Technique.** Follow the inductive proof of their Theorem 3.1 and check
whether each PSD piece can be chosen supported on one span{e_i, e_j, e}.
Alternatively, construct the certificate directly from the KKT structure
of separable StQP (Bomze–Locatelli 2012). At most one index can be
interior with β_i < 0, which suggests pairing that index with each other
index. For κ ≠ 2, the linking constraints (5) couple y_j and X_jj
through power cones; a proof would compare projections, not SDP values.

**Main risk.** Low significance. The authors regard PRs3 as prohibitively
costly compared with PRS. A proof may add structural understanding of
conv(S²) without changing solver practice.

### 3.3 Rank 3: Del Pia–Khajavirad Statements at constant rank

**Reduction (proved here; elementary).** For a hypergraph G = (V, E) and
F ⊆ V, define the shadow G_F = {e ∖ F : e ∈ E, |e ∖ F| = 2} on V ∖ F.

- BQP(G_F) is a coordinate projection of the face {z_v = 1, v ∈ F} of
  MP(G). Hence xc(MP(G)) ≥ xc(BQP(G_F)) ≥ 2^{Ω(tw(G_F)^δ)}, by their
  Theorem 7.
- Algorithmically, BQO on G_F reduces to BMO on G: add unary terms −M on
  F and give every other edge coefficient zero.
- Their Corollary 4 is the case F = ∅.
- So Statements 2 and 4 would follow from a *shadow lemma*: for fixed
  rank r, max_F tw(G_F) ≥ tw(G)^c / f(r), with F computable in
  randomized polynomial time.

**Obstruction (proved here).** The shadow lemma is false already at
rank 3.

- Let C be a cubic graph. Define H_C with vertex set E(C) and
  hyperedges δ(x) for x ∈ V(C).
- The primal graph of H_C is the line graph L(C). So tw(H_C) =
  tw(L(C)) ≥ (tw(C)+1)/2 − 1 (Harvey–Wood), which is Θ(|V(C)|) for cubic expanders
  and Θ(k) for the k×k hexagonal grid. There L(C) is the Kagome lattice.
- Every vertex of H_C lies in exactly two hyperedges. So every shadow
  G_F has maximum degree at most 2, and tw(G_F) ≤ 2 for every F.
- The route through faces and forcing alone therefore cannot prove
  Statement 2 or 4.

**Repair route (sketch, unverified).**

- *Equality faces.* If δ(x) = {a, b, c} and c is fixed to 1, the face
  {z_{δ(x)} = z_a} ∩ {z_{δ(x)} = z_b} enforces z_a = z_b. It is a face
  because z_{δ(x)} ≤ z_a is valid. This builds "wires".
- *Branch vertices.* Keeping the cubic monomial at a branch vertex gives:
  MP(H_G) is a projection of a face of MP(H_C) whenever the cubic graph
  G is a suitably spaced topological minor of C. The same holds for the
  objective reduction from BMO on H_G to BMO on H_C.
- *A hard base problem.* Take G bipartite cubic with sides X and Y, reward
  R at X-vertices, penalty P > 3R at Y-vertices, and small edge costs.
  Then BMO on H_G is equivalent to minimum red–blue domination: choose
  T ⊆ X meeting every N(y).
- If red–blue domination is NP-hard on planar bipartite cubic graphs
  (plausible, unchecked), Statement 2 holds for the hexagonal family
  H_C. Every planar graph of maximum degree 3 embeds as a subdivision
  in a large hexagonal grid, so the embedding is deterministic and the
  conclusion would even hold under P ≠ NP.
- Statement 4 for these families would still need an *unconditional*
  extension-complexity argument, and face shadows cannot provide it.

**Concrete first test.** Is xc(MP(H_{hex_k})) = 2^{Ω(k^δ)}, where hex_k
is the k×k hexagonal grid?

**Likely answer.** Statement 2 is probably true, at least for these
families. Statement 4 is uncertain.

**Main risk.** A general proof must handle arbitrary bounded-rank
hypergraphs that mix shadow-rich parts with H_C-like parts. Signed
Statements 1 and 3 restrict which literals can be forced. An
unconditional extension-complexity bound for H_C families may need new
techniques. Small cases are testable: exact treewidth of shadows, and
brute-force BMO on H_G gadgets.

---

## 4. Significance

- **Proved (first pass, pending independent review):**
  - Split separation is NP-hard even for positive definite Y. This
    answers the Letchford / Burer–Letchford question as restated in
    2026.
  - Separation is FPT in rank(Y) (sketch).
  - The shadow lemma fails at rank 3, via H_C.
  - Hildebrand–Göß Conjecture 47 is false as literally stated.
- **Plausible:**
  - Integer-QP solvers are justified in using heuristic or
    bounded-support split separation. Exact separation at low-rank SDP
    points is possible.
  - A treewidth dichotomy holds for BMO at bounded rank, extended
    through wire/branch embeddings. This would guide which sparsity
    patterns decomposition-based binary polynomial solvers can exploit.
  - Pairwise 3×3 certificates suffice for separable StQP.
- **Speculative:** measurable solver speedups from any of these.
  - For the split cuts, practical value would require exact low-rank
    separation to be faster than the current convex-IQP separation.
  - For Statement 2, the result is a complexity boundary, not an
    algorithm.

---

## 5. Recommendation

**Score: 5/10** (significance × feasibility × originality), for the best
target found.

- Pursue the split-separation result first, as a short, checkable note.
  - Finish the proof, run a lattice-literature priority check, add the
    fixed-rank and bounded-support refinements, and formalize the
    identities in Lean.
  - This is a one- to two-week task with high confidence of a correct
    result. Its significance is modest and its lattice core may be
    folklore, so its value is resolving a named MINLP conjecture.
- Then invest in the Del Pia–Khajavirad Statement 2/4 program, starting
  with the hexagonal test family and a verified NP-hardness proof for
  red–blue domination on planar cubic bipartite graphs. It has higher
  risk and a higher ceiling (about 6/10 if it works).
- Treat Dey–Kocuk Conjecture 2 as an optional side proof: likely true,
  tractable, and of low solver value.
- The sweep did not find a new problem that is simultaneously high in
  solver importance, tractable in weeks, and outside local or
  parallel-scout coverage. Leading items 4 and 20 belong to
  `fixed-dimension-frontier`. Item 7 (m ≥ 3 balls) is important but
  unlikely to yield within weeks.

---

## Checks actually run

These are targeted checks only. No project-wide verification was run and
CI was not inspected.

- `python3 split_separation_check.py`, in the scratch folder: exact
  Fractions, a = (3,5,7), eight values of s, box v ∈ {−2..2}⁵. Output as
  in §3.1.
- `~/miniconda3/envs/minlp-notes/bin/python dey_kocuk_conj2_check.py 1`:
  60 random κ = 2 instances with Clarabel. Largest gaps: PR 3.5e−4,
  PRs3 8.5e−9, PRS 1.1e−8.
- `dey_kocuk_conj2_search.py 3 5 PR` and `… 4 5 PRs3`: hill climbing
  with 6 restarts × 60 steps, logs in the scratch folder.
- `dey_kocuk_dual_structure.py`: at the PR-gap instance, the
  interior-point dual has all ten blocks active. This is uninformative
  about sparsity.
- `pdftotext` extraction of 2603.28979, 2510.16595, 2605.15970,
  2410.23045, Buchheim–Traversi, 2507.05066 and 2604.10363, with the
  cited passages read.
- Sub-sweep numerical claims (Dey–Kocuk at κ ≠ 2, the StQP 5-path gap
  instance, the Ploussard area lemma) were not rerun here.
