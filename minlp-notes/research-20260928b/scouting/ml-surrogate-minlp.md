# Scouting report: optimization over trained ML models embedded in MINLPs (`ml-surrogate-minlp`)

Date: 2026-09-28. Author: scout agent. Status: first pass. The theorems in Section 3
are proved here for the first time as far as this search could tell. They have not had
an independent review, and a focused prior-art audit is still needed (Section 2 and
Section 5). Scratch code and outputs are in
[`ml-surrogate-minlp/`](ml-surrogate-minlp/).

## Bottom line

- **Proved theory is dense for single units, thin beyond them.** For one neuron,
  or one max-of-affine unit, over a box or a continuous product of simplices, the
  hull is known, with fast separation (Anderson et al. 2020; Tjandraatmadja et al.
  2020). The repository's ridge-envelope theorem covers any continuous activation.
  Beyond one unit, the literature has:
  - approximate multi-neuron hulls (PRIMA, WraLU, WraAct);
  - incompleteness results for layerwise hull relaxations (Mao–Zhang–Vechev, ICLR
    2026);
  - hardness results for exact verification and Lipschitz computation.

  I found no extension-complexity bound for layer hulls. I also found no theorem on
  branch-and-bound (BaB) tree size for verification beyond exact-bound counting of
  activation patterns.
- **First-pass results (Section 3).** All are short proofs that reuse known
  extended-formulation, CSP and graph facts.
  - **Theorem A:** the hull of one ReLU layer over a box has extension complexity
    2^{Ω(n)}, even with nonnegative weights and fan-in at most 2. With bounded-degree
    graphs this is 2^{Ω(k/log k)} for k neurons. Hence no layer has a
    polynomial-size sharp or ideal MIP formulation.
  - **Theorem C:** for a fixed one-hidden-layer network, every LP relaxation with
    fewer than 2^{n^{c}} inequalities has worst-case ratio at least 2−ε. The
    single-neuron hulls already reach ratio 2, while an O(n²) SDP reaches 1/0.878.
  - **Theorem D:** a BaB method that branches on pairs of inputs needs 2^{Ω(n)}
    nodes to certify a bound better than about twice the optimum. This holds even
    when every node relaxation contains the exact hulls of all neuron groups
    spanning fewer inputs than the graph's girth. On the same instances the SDP
    root bound is within 1+O(1/√d) of the optimum.
  - **Theorem B:** layers whose fan-in-2 neurons form a simple forest have an exact
    O(n(n+u)²)-size extended formulation, where u is the number of one-input
    neurons.
  - **Remark A2:** a single neuron with binary inputs has the knapsack polytope as
    a face.
- **Best open question:** extend Theorem D beyond local relaxations and local
  branching, to Sherali–Adams level n^{Ω(1)}, global cuts and general hyperplane
  branching. The companion positive question is when SDP-bounded BaB is provably
  small.
- **Recommendation: 5/10.** A short, correct "barrier" paper is highly feasible.
  Its originality depends on a prior-art audit, and it brings no new solver
  capability. The open extension has higher significance but is much harder.

## 1. Frontier map

Notation. B is an input box, normalized to [0,1]^n when convenient. A layer
F(x) = (σ(w_j·x + b_j))_{j≤k} has graph hull H(F) = conv{(x, F(x)) : x ∈ B}.
xc(P) is the extension complexity of P: the least number of inequalities of any
polyhedron that projects onto P.

### 1.1 Single units: hulls and separation (settled)

- **ReLU over a box.** Anderson, Huchette, Ma, Tjandraatmadja and Vielma, *Math.
  Program.* 183 (2020), arXiv 1811.01988; the extracted text of §1.2 and §5 was
  checked.
  - The non-extended ideal formulation of ReLU(w·x+b) over a box has an exponential
    family of inequalities indexed by (I, h). Every inequality is facet-defining
    under mild conditions, and a most violated one is found in O(n) time
    (Propositions 12–13).
  - For the maximum of d>2 affine functions over a box, (24)+(25) is a hereditarily
    sharp formulation with efficient separation (Propositions 10–11). It is ideal
    for d=2 (Corollary 4).
  - Over a *continuous* product of simplices ("one-hot" inputs), Corollary 5 gives
    an ideal formulation with O(Σ p_i) separation. Integrality of the inputs is not
    part of that hull (see Remark A2 below).
- **Projected hull and the "barrier".** Tjandraatmadja et al., NeurIPS 2020, arXiv
  2006.14076 (extracted text checked). They give the projected hull in (x, y)
  space, with linear-time separation, used in OptC2V/FastC2V. This bypasses the
  single-neuron barrier of Salman et al. (NeurIPS 2019, arXiv 1902.08722; abstract
  checked) by using the multivariate input box.
- **Smooth activations.** Carrasco and Muñoz, *Math. Program.* 2026
  (`carrasco2026-tightening-convex-relaxations-of-trained`; local note read) treat
  convex or S-shaped activations with the STFE property over a box, via a
  recursive formula. The repository theorem in
  `research-20260922/ridge-envelopes/theory.md` covers every continuous σ(a·x+b)
  over a box, using a convex-order and Lovász-extension dual. Its neural-network
  experiment (`nn-experiment/report.md`) found valid cuts that did not pay off in
  solve time.
- **Intermediate formulations.** Kronqvist, Misener and Tsay give P-split
  formulations (`kronqvist2026-p-split-formulations-a-class`, local note read; the
  NeurIPS 2021 partition-based version is cited in the survey below). This is a
  per-neuron hierarchy from big-M to the convex hull. The repository documented a
  flaw in its Theorem 6.

### 1.2 Multi-neuron relaxations (heuristic or approximate hulls; no size theory)

- **Approximate multi-neuron hulls.** These compute hulls over groups of neurons in
  pre-activation space.
  - k-ReLU: Singh et al., NeurIPS 2019.
  - PRIMA: Müller et al., POPL 2022, arXiv 2103.03638.
  - WraLU: POPL 2024, doi 10.1145/3632917; reports about 50% fewer constraints
    than PRIMA.
  - WraAct: OOPSLA 2025, doi 10.1145/3763086.
  - Partial multi-neuron relaxation: arXiv 2605.30155 (abstract checked;
    heuristic subsets).
  - MN-BaB: arXiv 2205.00263.
  - Roth's primer: arXiv 2106.03099.

  These were checked through abstracts and search snippets only. None proves
  size or complexity bounds for exact hulls.
- **Mao, Zhang and Vechev, ICLR 2026, arXiv 2410.06816** (HTML checked).
  - 𝒫₁ is the layerwise full-layer hull relaxation; 𝒫_r uses r-layer hulls.
  - Theorems 3.3 and 4.2: these relaxations are incomplete with arbitrarily large
    error, for multi-layer networks.
  - Theorem 5.1: they become complete if the network is widened with neurons that
    copy the inputs.
  - Proposition 5.6 bounds *exact-bound* partition complexity:
    #Partition(BaB(multi-neuron)) ≤ #activation patterns ≤ #Partition(BaB(single-neuron)).
  - The paper has no NP-hardness, extension-complexity or approximation-ratio
    statement.
- **Expressivity.** Baader, Müller, Mao and Vechev, arXiv 2311.04015 (abstract):
  single-neuron relaxations cannot precisely analyze networks for multivariate
  convex monotone CPWL functions.
- **Azuma, Kim and Yamashita, arXiv 2607.20013 (July 2026; abstract).** Order-2
  block-sparse SOS is tight for one-layer verification when the input-sharing graph
  is a matching and a "regular rank-one" condition holds. A two-unit hull is two
  one-unit hulls coupled through a shared scalar.
- **Survey.** Huchette, Muñoz, Serra and Tsay, arXiv 2305.00241 v4 (extracted text,
  §4.2.2–4.4 checked).
  - Composing locally ideal formulations is not ideal.
  - The full network needs exponentially many disjuncts.
  - "The analysis of polyhedral formulations for multiple neurons simultaneously
    quickly becomes intractable, and is beyond the scope of this survey."

### 1.3 Complexity of optimizing or verifying trained networks

- **Classical hardness.** Katz et al. (Reluplex, CAV 2017) and Sälzer–Lange (2021)
  show verification is NP-complete. These were not re-checked; they are standard.
- **Froese, Grillo and Skutella, COLT 2025, arXiv 2405.19805** (abstract).
  Verification is coNP-hard. Unless P=NP, no constant-factor polynomial-time
  approximation exists for the maximum of a ReLU network. Injectivity is
  coNP-complete, and for one hidden layer it is fixed-parameter tractable in the
  input dimension.
- **Parameterized and precision frontier (local notes read).**
  - `stargalla2026-parameterized-hardness-of-zonotope-containment`: two-layer
    positivity is W[1]-hard in d, with an ETH n^{Ω(d)} bound, and W[ℓ] for depth
    ℓ+1.
  - `stargalla2026-parameterized-complexity-of-lp-lipschitz` and
    `wang2026-lp-norm-maximization-over-zonotopes`: ℓ_p zonotope and ICNN
    Lipschitz computation is W[1]-hard.
  - `jayawardhana2026-convex-networks-remain-hard-to`: the Euclidean ICNN
    Lipschitz constant is NP- and W[1]-hard.
  - `skutella2025-open-problem-fixed-parameter-tractability`,
    `skorupinski2026-nearly-tight-bounds-for-zonotope` and
    `li2026-apx-hardness-of-computing-lipschitz` are related.

  Every one of these notes records that the paper proves no MICP-size or
  BaB-tree-size result.
- **Hertrich and Loho, arXiv 2411.03006** (abstract). xc(P) lower-bounds the size of
  any monotone or input-convex network that optimizes over P; virtual extension
  complexity (vxc) does the same for general networks. This is the reverse
  direction from network to polytope. No bound on hulls of network graphs is
  given.

### 1.4 Branch and bound for verification

- **Methods.** β-CROWN (arXiv 2103.06624, abstract) encodes split constraints and
  "generally produces better bounds than typical LP verifiers with neuron split
  constraints". Related methods, checked via abstracts or snippets:
  - GCP-CROWN, arXiv 2208.05740 (general cuts);
  - BICCOS, arXiv 2501.00200 (BaB-inferred cuts);
  - MN-BaB;
  - E-Globe, arXiv 2602.05068 (ε-global BaB, tight upper bounds);
  - OBBT trade-offs, arXiv 2312.16699 (cited in repository scouting).
- **Gap.** None gives tree-size lower bounds. The only size statement found is
  Proposition 5.6 of Mao–Zhang–Vechev (exact bounds).

### 1.5 Tree ensembles and Gaussian-process surrogates

- **Tree ensembles.**
  - Mišić, *Oper. Res.* 2020, arXiv 1705.10883 (snippet): mixed-integer
    formulation, NP-hardness, and a relaxation tighter than linearization.
  - Kim, Richard and Tawarmalani, "A reciprocity between tree ensemble optimization
    and multilinear optimization", *Oper. Res.*, doi 10.1287/opre.2022.0150
    (snippet): a polynomial reduction in both directions to multilinear
    optimization over products of simplices, and ideal formulations for single
    trees.
  - ENTMOOT (arXiv 2003.04774) and Mistry et al. (2021) are computational
    frameworks.

  Consequence: tree-ensemble hull questions reduce to multilinear-polytope theory,
  which the repository has developed extensively. I did not pursue them.
- **Gaussian processes.** Schweidtmann et al., *Math. Prog. Comp.* 13 (2021), arXiv
  2005.10902 (abstract): reduced-space McCormick relaxations, envelopes of
  covariance and acquisition functions, and the MeLOn tool.
  - The multivariate envelope of one Gaussian bump over a box is not covered by the
    ridge theorem (it is a product, not a ridge).
  - Given the negative timing lesson of the repository's ridge-envelope experiment,
    I rated it low priority.
- **Other surrogate work.** Plate et al., arXiv 2609.31380 (Sept 2026, abstract),
  reduce the linear regions of a ReLU network empirically and report a 40–50%
  time reduction in superstructure optimization. Koeln 2026 (local) gives exact
  ReLU networks for mpQP solution maps.
- **Software.** OMLT, Gurobi Machine Learning and PySCIPOpt-ML were not re-checked
  in this pass.

### 1.6 Tools used below (checked)

- **Fiorini, Massar, Pokutta, Tiwary and de Wolf, JACM 2015, arXiv 1111.0837**
  (abstract): exponential xc for the cut, TSP and stable-set polytopes. Hence
  xc(COR(n)) = xc(BQP(K_n)) = 2^{Ω(n)}.
- **Göös, Jain and Watson, arXiv 1604.07062** (text checked, lines 108 and 346–371
  of the extraction): an explicit bounded-degree n-node graph with
  xc(STAB) = 2^{Ω(n/log n)}.
- **Kothari, Meka and Raghavendra, arXiv 1610.02704** (text checked: Definition 1.1,
  Theorem 1.2, Corollary 1.3). In the CLRS linearization framework, no LP relaxation
  with fewer than 2^{n^{c₃(ε)}} inequalities has MAX-CUT integrality gap below 2−ε.
  General extended formulations are covered.
- **Lee, Raghavendra and Steurer, arXiv 1411.6317** (abstract). Cut and stable-set
  polytopes need SDP lifts of dimension 2^{n^c}. For Max-CSPs, polynomial-size SDPs
  are no stronger than O(1)-degree SOS.
- **Pokutta and Van Vyve, ORL 2013** (`pokutta2013-a-note-on-the-extension`, local
  note read). Some knapsack polytopes have xc 2^{Ω(√n)}; the construction uses
  algebraically independent coefficients.

### 1.7 Sources examined (summary table)

| Source | How checked | What was checked |
|---|---|---|
| arXiv 1811.01988 (Anderson et al.) | full text (pdftotext) | contribution list, Prop. 10–13, Cor. 4–5, one-hot domain |
| arXiv 2006.14076 (Tjandraatmadja et al.) | full text | single-neuron hull, no multi-neuron hardness claims |
| arXiv 1811.08359 (IPCO version) | downloaded, not read | — |
| arXiv 2305.00241 v4 (survey) | full text | §4.2–4.4 statements on multi-neuron intractability |
| arXiv 2410.06816 (Mao–Zhang–Vechev) | HTML via fetch | definitions, Thm 3.3/4.2/5.1, Prop 5.6 |
| arXiv 2411.03006 (Hertrich–Loho) | abstract | xc/vxc lower bounds on network size |
| arXiv 2311.04015 (Baader et al.) | abstract | expressivity limits |
| arXiv 2607.20013 (Azuma–Kim–Yamashita) | abstract | matching input-sharing SOS tightness |
| arXiv 2605.30155, 2602.05068, 2609.31380 | abstracts | no complexity theorems |
| arXiv 2405.19805 (Froese–Grillo–Skutella) | abstract | coNP-hardness, inapproximability |
| arXiv 2103.06624 (β-CROWN) | abstract | relation to LP with splits |
| arXiv 2005.10902 (Schweidtmann et al.) | abstract | GP envelopes |
| arXiv 1111.0837, 1411.6317 | abstracts | xc / psd lift lower bounds |
| arXiv 1610.02704 (KMR), 1604.07062 (GJW) | full text (targeted) | exact theorem statements, bounded degree |
| PRIMA 2103.03638, WraLU, WraAct, 1902.08722, 2208.05740, 2501.00200, 2205.00263, 2106.03099, 1705.10883, opre.2022.0150, 2003.04774, 2512.24339, 2402.03625, 2410.22311, 2509.22849 | search snippets or abstracts | scope only (no size/complexity theory for exact multi-neuron hulls or BaB lower bounds) |
| Local notes: carrasco2026, jayawardhana2026, koeln2026, li2026, stargalla2026 ×2, skorupinski2026, wang2026, skutella2025, toh2026, kronqvist2026 P-split, pokutta2013 | `paper.md` notes read | claims and stated limits |
| Repository: `research-20260922/ridge-envelopes/{theory,novelty}.md`, `nn-experiment/report.md`, `research-20260922/scouting/{scout_brainstorm,brainstorm2-applications}.md`, `research-20260925/direction-audit.md`, `paper-integer-dimension/coverage.md` | read (relevant parts) | overlap and lessons (tree ensembles and NNs judged "crowded"; ridge cuts valid but slow) |

Search limitations: the session's web-search budget (200 calls) ran out partway
through this pass. After that I used arXiv API queries, which were partly
rate-limited, and direct page fetches. **An unsuccessful search does not establish
novelty.**

## 2. Open questions

Each question is precise. The evidence that it is open is that none of the sources
in §1 address it. That evidence is weak, especially for Q1(b) and Q2.

**Q1 (best). Branching complexity beyond local relaxations.** Let G be a d-regular
graph with max cut ≤ (1/2 + O(1/√d))|E|, for example a Ramanujan graph. Let

  f_G(x) = Σ_{ij∈E} (ReLU(x_i − x_j) + ReLU(x_j − x_i)) on [0,1]^n.

This is a two-layer ICNN with fan-in 2 and max f_G = maxcut(G). Theorem D below
settles the *local* case. Open:

- **(a)** Let every node relaxation contain the level-r Sherali–Adams closure of
  the standard MILP formulation, with r = n^{Ω(1)}, or contain arbitrary Gomory or
  MIR closures. Must every ReLU-splitting BaB tree that certifies
  f_G ≤ (1−ε)|E| still have 2^{n^{Ω(1)}} nodes?
- **(b)** Does the lower bound survive branching on general hyperplanes a·x ≤ β?
  This is a stabbing-planes-type proof system.
- **(c)** Positive side: for which classes of trained networks does BaB with
  spectrahedral (Shor/GW-type) node bounds provably need only polynomially many
  nodes for a (1+ε)-certificate? Froese–Grillo–Skutella rule out a general
  polynomial-time constant-factor method unless P=NP.

**Q2. Structure dichotomy for layer hulls.** Take layers of fan-in ≤ 2,
ReLU(a x_i + b x_j + c), over a box, with interaction multigraph G. Theorem A gives
exponential xc for dense and bounded-degree-expander G; Theorem B gives
polynomial-size EFs for simple forests. Is xc(H) ≤ poly(n, k)·f(tw(G))? The open
cases include simple graphs of treewidth 2 (cycles, ladders, series-parallel graphs)
and *multigraph* paths (two neurons on the same input pair). The Boolean-face
technique of Theorem A cannot give lower bounds there, because BQP(G) of a
bounded-treewidth graph has polynomial xc.

**Q3. Depth-dependent approximation barrier.** Sketch E below gives fixed-depth
families where every subexponential LP, and plausibly every polynomial-size SDP,
has ratio ≥ 2^k/(k+1) at depth about log₂ k. Which classes of networks with natural
weight bounds admit polynomial-size relaxations with ratio f(depth), and what is
the best f?

**Q4. Exact two-neuron hull over a box.** For two dense neurons sharing n inputs,
give an explicit facet description and a combinatorial (for example O(n log n))
separation algorithm, as Anderson et al. did for one neuron. A Balas LP already
gives polynomial separation, so this question is practical rather than
complexity-theoretic.

## 3. First-pass mathematics

### 3.1 Theorem A: layer hulls have exponential extension complexity

**Theorem A.** Let G = ([n], E) be a graph. Define the layer F_G on [0,1]^n by
y_ij = ReLU(x_i + x_j − 1) for ij ∈ E and u_i = ReLU(2x_i − 1) for i ∈ [n]. All
weights are nonnegative, fan-in is at most 2, and k = |E| + n. Then:

- the Boolean quadric polytope BQP(G) = conv{(v, (v_i v_j)_{ij∈E}) : v ∈ {0,1}^n}
  is affinely isomorphic to a face of H(F_G);
- STAB(G) is affinely isomorphic to a face of that face.

Hence xc(H(F_G)) ≥ xc(BQP(G)) ≥ xc(STAB(G)), and the same inequalities hold for
the minimum SDP-lift dimension.

*Proof.* Since 2ReLU(t) − t = |t|, the linear functional φ = Σ_i (2u_i − 2x_i + 1)
equals Σ_i |2x_i − 1| on the graph. So φ ≤ n on the graph, with equality exactly at
Boolean x. H is the convex hull of a compact set, so the face argmax_H φ is the
convex hull of the Boolean graph points (v, (v_i v_j), v). On this face u = x, so
dropping u is an affine bijection onto BQP(G). The inequality y ≥ 0 is valid, and
{y = 0} cuts out STAB(G). Faces of a polytope have extension complexity (and lift
dimension) at most that of the polytope. ∎

Instances:

- G = K_n gives xc ≥ 2^{Ω(n)} with k = C(n,2) + n (by FMPTW).
- The bounded-degree Göös–Jain–Watson graphs give xc ≥ 2^{Ω(n/log n)} =
  2^{Ω(k/log k)} with k = O(n).
- Lee–Raghavendra–Steurer rule out SDP lifts of dimension below 2^{n^c}.

The only general upper bound is Balas' extended formulation over the 2^k
activation patterns, of size O(2^k (n+k)). For fixed input dimension there is also
the vertex bound (number of arrangement vertices). So the exponential dependence
on the number of neurons is necessary up to a log factor.

**Corollary A1 (no compact exact layer formulations).** A sharp MIP formulation of
S = graph(F_G) is one whose LP relaxation projects onto conv(S); every ideal
formulation is sharp. Every such formulation has at least xc(H(F_G)) inequalities,
however many binary or auxiliary variables it uses. Per-neuron ideal formulations
have constant size here (fan-in ≤ 2), but no polynomial-size formulation can be
sharp for the layer.

**Remark A2 (integer inputs; knapsack face).** Take one neuron with binary inputs,
S = {(v, ReLU(a·v − β)) : v ∈ {0,1}^n}. Then {y = 0} ∩ conv(S) is the knapsack
polytope {v ∈ {0,1}^n : a·v ≤ β} (lifted by y = 0). The layer version is one
fan-in-n neuron plus the n unary neurons u_i over the box.

- Linear optimization over conv(S) is weakly NP-hard.
- By Pokutta–Van Vyve, xc(conv(S)) can be 2^{Ω(√n)}. Their coefficients are
  algebraically independent. A rational version should follow by aggregating
  their equalities with integer multipliers of polynomial bit length, but I did not
  check this.

This does not contradict Anderson et al.'s Corollary 5, whose simplices are
continuous. It matters for MINLPs whose network inputs are integer decisions: the
per-neuron "ideal" formulation is then not the hull of the mixed-integer set, even
for one neuron. The interaction hypergraph of this layer (one big edge plus
singletons) is Berge-acyclic, so Berge-acyclicity alone does not give tractability
once fan-in is unbounded.

**Computation (exp6).** For G = K_3 and K_4, the maximizers of φ over the exact
graph vertices are exactly the 2^n Boolean points.

| Graph | Graph vertices | Facets of H | Facets of the face |
|---|---|---|---|
| K_3 | 27 | 72 | 16 = facets of BQP(K_3) |
| K_4 | 81 | 5424 | 56 = facets of BQP(K_4) ≅ CUT_5 |

### 3.2 Theorem C: an LP-relaxation barrier for one hidden layer, with an SDP contrast

**Theorem C.** Let D_n be the layer on [0,1]^n with neurons p_ij = ReLU(x_i − x_j)
and q_ij = ReLU(x_j − x_i) for i<j. For w ∈ Z_{≥0}^{C(n,2)}, the two-layer ICNN
f_w = Σ w_ij (p_ij + q_ij) = Σ w_ij |x_i − x_j| attains its maximum over the box at
a vertex, so max f_w = maxcut_w.

- **(a)** For every ε>0 there is c(ε)>0 with the following property. Let Q be any
  polyhedron in any dimension, with fewer than 2^{n^{c(ε)}} inequalities, whose
  projection contains H(D_n). Then for some w ∈ {0,1}^{C(n,2)},
  max_Q ⟨w, p+q⟩ ≥ (2−ε)·maxcut_w.
- **(b)** The intersection of the single-neuron hulls gives p_ij + q_ij ≤ 1, hence
  ratio ≤ Σw/maxcut_w ≤ 2 for every w.
- **(c)** The O(n²)-size spectrahedral relaxation
  R_SDP = {x ∈ B, p, q ≥ 0, ∃ Y ⪰ 0 with Y_ii = 1 and p_ij + q_ij ≤ (1 − Y_ij)/2}
  contains H(D_n) and has ratio ≤ 1/0.878.

*Proof.*

- (a) Use the KMR framework (Definition 1.1 and Corollary 1.3 of arXiv 1610.02704)
  with v_x = a lift in Q of the graph point at Boolean x and w_I = w on the p+q
  coordinates. Then ⟨w_I, v_x⟩ is the cut value.
- (b) The single-neuron hulls give p ≤ min(x_i, 1−x_j) and q ≤ min(x_j, 1−x_i).
- (c) Couple by thresholds: σ_i = sign(x_i − U) with U ~ Unif[0,1]. Then
  Y = E[σσᵀ] ⪰ 0 has Y_ij = 1 − 2|x_i − x_j|, so every graph point lies in R_SDP,
  and max_{R_SDP} ≤ GW SDP ≤ maxcut/0.878. ∎

So, in the worst case over output weights, per-neuron hulls are asymptotically
optimal among all subexponential LPs for this fixed architecture. This covers
PRIMA-type groups and any constant number of Sherali–Adams rounds. The same
architecture separates LPs from SDPs.

**Computation (exp9).**

| Instance | SDP root | Max cut | LP roots |
|---|---|---|---|
| K_n, n = 5–8 | 6.25, 9, 12.25, 16 | ⌊n²/4⌋ (6, 9, 12, 16) | triangle-relaxation LP C(n,2); with 3-input cuts 2C(n,2)/3 |
| Petersen graph | 12.5 | 12 | 15, with the triangle relaxation and with all exact 4-input hulls |

On K_n the SDP root equals n²/4, so it certifies ⌊n²/4⌋ after integer rounding.

### 3.3 Theorem D: branch-and-bound lower bounds (the main first-pass result)

**Setting.** G = ([n], E) has maximum degree Δ and girth g. f_G is as in Q1. A BaB
tree branches with constraints that each involve at most two input coordinates.
This covers ReLU splits x_i ≥ x_j / x_i ≤ x_j of the hidden neurons, input-domain
splits x_i ≤ c / x_i ≥ c, and mixtures of the two. Reg(ν) is the node region: the
box plus the branching constraints on the path.

**Local relaxation.** For r < g, Loc_r(ν) is the set of (x, y) with x ∈ Reg(ν) such
that, for every S ⊆ [n] with |S| ≤ r,

  (x_S, y_{E(S)}) ∈ conv{(z_S, F_S(z_S)) : z ∈ Reg(ν)}.

That is, Loc_r(ν) contains the exact hulls, over the node region, of all neuron
groups spanning at most r inputs. It includes, as special cases:

- exact modeling of neurons whose sign is fixed;
- triangle relaxations with optimal bounds;
- OBBT;
- the single-neuron hulls of Anderson et al.;
- any PRIMA-type group with at most r inputs.

A node bound counts as local if its relaxation contains Loc_r(ν).

**Lemma D.1.** max_{Loc_r(ν)} Σ_e (p_e + q_e) ≥ |E| − Δ|T(ν)|, where T(ν) is the
set of coordinates in the non-redundant branching constraints on the path.

*Proof.*

- Fix z* ∈ Reg(ν).
- For S with |S| ≤ r, define a random Z^S as follows. On T it equals z*. On
  S \ T, each connected component of G[S \ T], which is a tree because |S| < g,
  gets one of its two proper 2-colorings in {0,1}, uniformly and independently.
- Z^S ∈ Reg(ν), because the node constraints involve only coordinates in T.
- The single and edge marginals of Z^S do not depend on S:
  - a coordinate outside T is Bernoulli(1/2);
  - an edge inside S \ T is uniform on {(0,1), (1,0)};
  - an edge with one end in T has an independent Bernoulli(1/2) end and a fixed
    end.
- So the point (x̄, ȳ) of these marginal expectations lies in every group hull,
  that is, in Loc_r(ν).
- Its value is 1 per edge disjoint from T and 1/2 per edge with exactly one end in
  T, since E|z − Z| = 1/2 for z ∈ [0,1]. Hence the value is ≥ |E| − Δ|T|. ∎

**Theorem D.** Every BaB tree as above that certifies f_G ≤ θ has at least
2^{(|E|−θ)/(2Δ)} leaves.

*Proof.* A redundant branching (one child empty) leaves the region unchanged;
contract it. After this, every feasible leaf needs |T| ≥ (|E|−θ)/Δ by Lemma D.1,
and every branching adds at most 2 coordinates. So every root-to-leaf path has at
least (|E|−θ)/(2Δ) non-redundant branchings, and the contracted tree contains a
complete binary tree of that depth. ∎

**Corollary D.2 (explicit separation).** Take non-bipartite d-regular LPS Ramanujan
graphs. Their girth is about (2/3) log_{d−1} n, and their max cut is
≤ (n/4)(d − λ_min) ≤ (1/2 + √(d−1)/d)|E| by the eigenvalue bound. The constant in
the girth bound should be re-checked against the LPS paper; the argument only needs
girth → ∞. Any local BaB with r < g needs ≥ 2^{εn/4} nodes to certify
f_G ≤ (1−ε)|E|. That bound is still about 2(1−ε)/(1+2/√d) times the optimum. The
root bound of R_SDP is at most the eigenvalue bound (1/2 + √(d−1)/d)|E|.

This is also a statement about MILP branch and bound on the standard neuron
formulations: branching on neuron binaries is ReLU splitting. It holds when the
LP is strengthened by any local cuts, but not by global cuts such as Gomory cuts.

**Theorem D′ (complete graph, triangle relaxations with exact bounds).** Consider
ReLU-splitting BaB on f_{K_n} whose node LP models resolved neurons exactly and
unresolved neurons by triangle relaxations with the exact bounds [−1, 1].

- **(i)** For odd n, certifying the exact value ⌊n²/4⌋ needs ≥ n! leaves.
- **(ii)** Certifying (1+δ)⌊n²/4⌋ with δ<1 needs ≥ 2^{n√((1−δ)/2) − O(1)} leaves.

*Proof.* At a node with closure poset P, the node LP equals
#incomparable pairs + max over up-sets U of P of #(comparable pairs split by U).
This holds for three reasons:

- incomparable pairs can take p + q = 1 at any x;
- comparable pairs are exact;
- a convex function is maximized over the order polytope at a 0/1 vertex.

For (i), suppose i and j are incomparable. Some linear extension of P places them
next to each other. Of the two middle cuts, of sizes (n±1)/2, at most one separates
them; the other gives LP ≥ ⌊n²/4⌋ + 1. So every leaf is a total order, and every
strict order cone must be covered, which gives n! leaves.

For (ii), every leaf needs ≥ C(n,2) − θ comparable pairs, and D arcs produce at
most C(D+1, 2) comparable pairs. Every node region contains the constant vectors,
so no child is ever infeasible. ∎

Theorem D′(i) is essentially an instance of Mao–Zhang–Vechev's exact-bound
activation-pattern count. Part (ii) and Theorem D do not follow from their
statement.

**Computations.**

- **exp4: ReLU-splitting BaB on K_n with triangle LPs (HiGHS).**

  | n | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|
  | leaves, exact certification | 6 | 22 | 120 | 660 | 5040 | 38064 |
  | leaves, δ = 0.25 | 6 | 8 | 66 | 202 | 886 | 4096 |

  For odd n the exact counts equal n!. The inequality LP(node) ≥ #unresolved held
  at every node. The n = 9 run was stopped, since it needs at least 9! leaves.
- **exp7: the same BaB with the valid 3-input cuts**
  d_ij + d_jk + d_ik ≤ 2 and d_ij ≤ d_ik + d_kj, where d = p + q.

  | n | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|
  | leaves | 10 | 48 | 212 | 1316 |

  Local cuts help a lot on K_n, whose girth is 3, but the counts still grow
  steeply.
- **exp8: Petersen graph (girth 5) with the exact hulls of all 205 four-vertex
  groups** (78 local types, 2040 exact facets, computed exactly). The root LP is
  15 = |E| against a max cut of 12. Across 300 random nodes there were 0
  violations of LP ≥ #unresolved. This confirms Lemma D.1 in the box-group case.

### 3.4 Lemma L: sign-compatible layers gain nothing in nonnegative directions

**Lemma L.** Suppose the weight vectors of a layer are sign-compatible: for some
s ∈ {±1}^n, s_i w_ji ≥ 0 for all i, j. Then, for every d ≥ 0 and every c, the
intersection of the single-neuron hulls attains max_{H} (d·y − c·x). So every facet
of the joint hull with a nonnegative y-part is implied by single-neuron facets.

*Proof.* Flip coordinates so that w ≥ 0. Each vertex function S ↦ ReLU(w_j(S) + b_j)
is then supermodular. The concave envelope over the box equals the Lovász
extension (TRX 2013, or the ridge theorem), and the Lovász extension is linear in
the set function. So conc(Σ d_j g_j) = Σ d_j conc(g_j). ∎

Consequences:

- Joint cuts can help only in mixed-sign or DC directions, for example y₂ ≤ y₁ when
  z₂ ≤ z₁ holds on the box.
- Theorem A is consistent with the lemma: its hard faces use −y directions.
- This proves the first bullet of item 7 in
  `research-20260922/scouting/scout_brainstorm.md`.

**Computation (exp1).** For random pairs with n = 2, sign-compatible pairs had
joint facets only with mixed-sign (y₁, y₂) coefficients (228 facets). Incompatible
pairs also had joint facets that bound y₁ + y₂ from above (95 of 95 instances).
Two examples:

- For ReLU(x₁+x₂) and ReLU(x₁−x₂) on [−1,1]², the hull is a 4-simplex with the
  single joint facet y₁ + y₂ ≤ x₁ + 1.
- For ReLU(x₁+x₂) and ReLU(2x₁+x₂−1) on [−1,1]², the joint facets are y₂ ≤ y₁ and
  2y₁ − y₂ ≤ x₂ + 1.

**Computation (exp2).** Facet counts for dense random pairs over [0,1]^n:

| n | 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| mean joint facets | 2.4 | 5.4 | 15.3 | 57.9 |
| mean single-neuron facets (sum of both) | 8.0 | 11.5 | 18.0 | 32.1 |

**Computation (exp5).** For random objectives and dense Gaussian pairs, n = 3–20,
the intersection of the two exact single-neuron hulls exceeds the exact pair hull
by 0.3–1.2% of the objective range on average. The median excess is 0 and the
maximum is 7–21%. So pair cuts matter only in specific directions, which bears on
Q4.

### 3.5 Theorem B: forest-structured layers have compact exact formulations

**Theorem B.** Let every neuron have fan-in ≤ 2, and let the fan-in-2 neurons form
a *simple* forest on [n]: at most one neuron per input pair, and no cycles. Let u
be the number of unary neurons. Then H(F) has an extended formulation with
O(n(2n+u)²) variables and constraints.

*Proof sketch.*

1. H(F) is the hull of the graph points at the vertices of the arrangement inside
   the box.
2. At such a vertex, each tight tree component has exactly one anchor: a box bound
   or a unary breakpoint. Each coordinate value is the anchor value propagated
   along the unique tree path, so coordinate i takes values in a set V_i with
   |V_i| ≤ 2n + u.
3. All grid points of ∏V_i lie in the box, so H(F) = conv{(v, F(v)) : v ∈ ∏V_i}.
4. This is a linear image of the pairwise marginal polytope of G with state spaces
   V_i. For forests that polytope equals the local polytope (junction-tree
   theorem). ∎

**Computation (exp3).** For random trees with n = 3–6, including unary neurons and
parallel neurons, every arrangement-vertex coordinate was in the predicted V_i.
Over 140 objectives, the local-marginal LP matched the exact maximum over the
graph to 1.8e−15.

**Obstacle.** With parallel neurons the value sets can grow exponentially. For
example, the tight neurons 2x_{i+1} − x_i = 0 and 2x_{i+1} − x_i − 1 = 0 produce all
dyadic values with i−1 bits. Cycles add "self-anchored" values. The random-weight
counts in exp3 stayed small (≤ 14) because random chains leave the box quickly, so
they say nothing about the worst case. This is Q2.

### 3.6 Sketch E: depth-dependent barrier (not checked in detail)

- **Construction.** Fix a k-ary predicate P whose satisfying set A supports a
  pairwise-independent distribution; Hadamard predicates have k = 2^r − 1 and
  |A| = k+1. Then
  f_P(x) = max(0, max_{a∈A} (1 − Σ_i |x_i − a_i|))
  is convex on the box, equals P at vertices, and is a maximum of |A|+1 affine
  functions. It therefore has a ReLU network of depth ⌈log₂(|A|+1)⌉ + O(1).
- **Network.** Place one subnetwork for each k-tuple and literal pattern (n^k 2^k of
  them); the output weights are the CSP instance. The maximum over the box equals
  the CSP optimum.
- **Lower bound.** Combining KMR Theorem 1.2 with Sherali–Adams gaps for
  pairwise-independent predicates (Benabbas–Georgiou–Magen–Tulsiani 2012), no LP of
  size 2^{n^{c}} beats ratio 2^k/(k+1) − ε.
- **Upper bound.** Exact per-subnetwork hulls, of constant size for fixed k, achieve
  2^k/(k+1).
- **SDPs.** Via LRS and SOS lower bounds from pairwise independence (Barak, Chan and
  Kothari 2015), polynomial-size SDPs should not do better either. I did not check
  the exact size parameters.
- **Reading.** The unavoidable ratio can grow doubly exponentially with depth, for
  fixed-depth, polynomial-width families. This addresses the brief's "approximation
  ratio as a function of depth" only through lower-bound families.

### 3.7 Attack plan for Q1, with difficulty and risk

1. **Global cuts and Sherali–Adams level n^{Ω(1)}.** Replace the girth argument by
   Charikar–Makarychev–Makarychev local-global Sherali–Adams solutions for max cut on
   high-girth or random graphs, which have gap 2−ε at level n^{γ(ε)}. Condition them
   on the ≤ 2D coordinates touched by the branching constraints. Conditioning on
   |T| coordinates costs |T| levels. The key lemma is that value drops only on
   edges near T; CMM's correlations decay with distance, which makes this
   plausible. Target: 2^{n^{Ω(1)}} nodes for SA-level-n^{γ} BaB.
   - Difficulty: high. Needs a careful reading of the CMM construction.
   - Risk: medium. The conditioning may disturb the local metric structure.
2. **General hyperplane branching.** Test whether Lemma D.1's "untouched
   coordinates stay uniform" idea survives dense branching hyperplanes, for example
   by random restrictions or a hyperplane-by-hyperplane potential argument. This is
   close to open stabbing-planes lower bounds, so the risk is high. A useful
   intermediate target is branching hyperplanes of bounded support s, where the
   bound becomes 2^{Ω(n/(sΔ))}.
3. **Positive side (c).** Prove polynomial node bounds for SDP-bounded BaB on
   structured two-layer ICNNs, for example when the output-weight graph has bounded
   threshold rank. Then test R_SDP-type Shor cuts in a MINLP solver on OMLT-style
   surrogate instances with difference or cut structure.
4. **Deliverable.**
   - Write Theorems A, C and D (with the explicit Ramanujan corollary) as a short
     note.
   - Run the prior-art audit: max-cut B&B with local relaxations on high-girth
     graphs; locality lower bounds for LP-based verification; stabbing-planes and
     Res(lin) literature.
   - Get an independent proof review.

Overall: the first-pass results are low-risk and high-feasibility. Item 1 is a
research-level extension with an uncertain timeline; my estimate is weeks to months.

## 4. Significance

**Proved here (first pass, needs review):**

- **Layer-level exact formulations are impossible (Theorem A, A1).** No polynomial
  LP or SDP describes the hull of one ReLU layer, even with nonnegative, fan-in-2,
  small-integer weights. No polynomial sharp or ideal MIP formulation of a layer
  exists. This closes the "compact ideal layer formulation" direction and explains,
  in unconditional terms, why the literature stops at per-neuron ideality.
- **Multi-neuron LP cuts cannot fix worst cases (Theorem C).** For a fixed
  one-hidden-layer ICNN family, subexponential LP relaxations cannot beat the
  per-neuron ratio 2, while an O(n²) SDP achieves 1/0.878. This is a formal
  LP-versus-SDP separation for verification-type bounds.
- **Local BaB is exponential where the SDP root is nearly exact (Theorem D).** LP
  branch and bound with local branching and local relaxations needs 2^{Ω(n)} nodes
  on explicit two-layer ICNNs whose SDP root bound is within 1+O(1/√d) of the
  optimum. This applies to MILP B&B on standard neuron formulations strengthened
  only by local cuts, and to input-splitting BaB.
- **Forest layers have compact exact hulls (Theorem B).**
- **Integer inputs make single neurons knapsack-hard (Remark A2).** Relevant when
  network inputs are integer design decisions.

**Plausible:**

- Adding spectrahedral (Shor/GW-type) bounds to BaB for MINLPs with embedded ReLU
  networks can cut tree sizes exponentially on instances with pairwise-difference
  structure. Trained process surrogates rarely have that structure explicitly, and
  whether they exhibit it implicitly is unknown.
- Theorem B plus Lemma L could guide which neuron groups deserve exact multi-neuron
  cuts: tree-like interactions and mixed-sign directions.

**Speculative:**

- The Sherali–Adams and global-cut extension of Theorem D, which would give a
  near-universal statement about LP-based BaB for neural-network verification.
- Practical value of forest-structured exact formulations, for example
  1-D convolutions with kernel width 2 or sparse physics-informed layers.

**Still needed for practical value:**

- Measurements on real trained surrogates, for example OMLT or Gurobi-ML benchmark
  models: how often mixed-sign joint directions and SDP-exploitable structure occur.
- An implementation of SDP or eigenvalue bounds in a MINLP B&B for embedded
  networks.
- Evidence that SDP cost pays off. The repository's ridge-cut experiment is a
  warning that valid, tighter bounds can still lose on time.

## 5. Recommendation

**Score: 5/10** (significance 5, feasibility 8, originality 4–5).

Pursue this as a short barrier paper rather than as the main research direction:

1. Theorem A with Corollary A1 and Remark A2.
2. Theorem C with the SDP contrast.
3. Theorem D with the explicit Ramanujan corollary and the K_n n! bound.
4. Theorem B and Lemma L as the positive, structural side.

The proofs are short and were checked on small cases by exact computation. They
answer questions that the neural-network-verification and MINLP communities pose
informally, the "convex barrier" in particular, with unconditional,
formulation-independent statements. The main risks:

- **Originality.** Each theorem transfers a known extended-formulation, CSP-LP or
  locality argument. Experts may see them as folklore, and my search budget ran out
  before a targeted audit of max-cut B&B and stabbing-planes literature.
- **Solver impact.** It is mostly guidance: avoid compact exact layer
  formulations, and consider SDP bounds. No new solver capability is proven.

The best follow-on, Q1(a), extends Theorem D to Sherali–Adams levels n^{Ω(1)}. It
would raise significance substantially, but it is research-level and uncertain.

Q2–Q4 are lower priority. Tree-ensemble hulls reduce to the repository's
multilinear line, and Gaussian-process envelopes echo the negative ridge-cut timing
lesson.

## Appendix: commands run and scratch files

All commands were targeted scratch computations in
`research-20260928b/scouting/ml-surrogate-minlp/`. No project-wide checks were run
and no CI was inspected. pycddlib-standalone 3.0.0 was installed into `/tmp/pylibs`
for floating-point cddlib. Every facet used was re-derived and verified in exact
rational arithmetic in `hull_tools.py`.

| Script | Purpose | Output |
|---|---|---|
| `hull_tools.py` | exact arrangement vertices; cdd facets with exact re-derivation and verification | — |
| `exp1_two_relu_two_inputs.py` | facets of 2-ReLU/2-input hulls, sign-compatibility statistics | `exp1_output.txt` |
| `exp2_dense_pairs.py` | facet counts for 1 and 2 dense neurons, n = 2–5 | `exp2_output.txt` |
| `exp3_forest_ef.py` | Theorem B checks and value-set counts | `exp3_output.txt` |
| `exp4_bab_kn.py` | BaB with triangle LPs on K_n (run as `python3 exp4_bab_kn.py 9`; n = 9 stopped) | `exp4_output.txt` |
| `exp5_pair_gain.py` | single-hull versus pair-hull bound excess (Balas LPs) | `exp5_output.txt` |
| `exp6_face_bqp.py` | Theorem A face check (BQP facets 16 and 56) | `exp6_output.txt` |
| `exp7_bab_kn_triples.py` | BaB with 3-input cuts (run as `python3 -u exp7_bab_kn_triples.py 8`) | `exp7_output.txt` |
| `exp8_petersen_group_hulls.py` | Lemma D.1 check with exact 4-input group hulls | `exp8_output.txt` |
| `exp9_sdp_root.py` | GW/SDP root bounds (cvxpy with SCS) | `exp9_output.txt` |

The directory `src/` holds downloaded arXiv PDFs and their pdftotext extractions
(1811.01988, 1811.08359, 2006.14076, 2305.00241, 1610.02704, 1604.07062). They are
scratch copies, not literature packages.
