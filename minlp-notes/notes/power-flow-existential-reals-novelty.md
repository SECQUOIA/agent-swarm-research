# Prior-literature audit: ∃R-completeness of resistive and AC power-flow feasibility

Date: 2026-09-05. Status: novelty audit of the claim (1) feasibility of the resistive
("DC", constant-power-injection) model — V_i ∈ [VL_i, VU_i], V_i Σ_j g_ij (V_i − V_j) ∈ [PL_i, PU_i],
g_ij > 0 — is ∃R-complete; (2) AC power-flow feasibility (real and reactive injection bounds, voltage
magnitude bounds, real angle-difference limits ≤ π/2, or the separate
rectangular variant with bus-angle boxes relative to a reference) is ∃R-complete even with
purely resistive lines, zero reactive injections, maximum degree 3 and data from a fixed finite set;
hence not in NP unless NP = ∃R. Proof: ETR-INV gadgets in the resistive model plus an
energy/monotonicity argument that zero reactive injections force equal angles on resistive
lines under the stated real angle-difference bounds. Principal line differences alone
do not suffice on cycles; see the corrected result and its reviews A–C.
Not a proof audit. Reduction script: `code/power_flow_existential_reals/dc_resistive_build_and_check.py`.

## Verdict

**No matching result found in the sources searched (both parts); the ingredients and model are known.**

This is a bounded search, not proof of priority. All absence statements below
refer to the searched sources and versions. Its original scope preceded the
angle-semantics correction; the final theorem uses real angle differences
or the separate rectangular bus-angle-box variant. See
[the closeout audit](review-existential-reals-closeout.md).

- The search found no published or preprint source stating ∃R-hardness, ∃R-completeness, or "not in NP unless
  NP = ∃R" for AC power flow, AC-OPF, DC/resistive power flow with constant-power loads, or any
  Kirchhoff network with power constraints. The ∃R compendium (arXiv:2407.18006v1, text at
  `/tmp/compendium.txt`) has no entry for power, load flow, electrical networks, circuits (other
  than arithmetic circuits), Kirchhoff, voltage, or network flow. Web searches (2020–2026) for
  power flow + ∃R/ETR/PSPACE/"in NP" find only NP-hardness statements.
- What is known and must be credited:
  (a) AC feasibility is strongly NP-hard (Bienstock–Verma 2019, lossless model) and weakly NP-hard on
  trees (Lehmann–Grastien–Van Hentenryck 2016); Bienstock–Verma explicitly doubt NP membership
  because of irrational solutions and conjecture only an ε-version is in NP
  [[bienstock2019-strong-np-hardness-of-ac]] p.6. Verma's thesis (2009, Remark 5.1.6) already
  fights the irrationality issue inside the NP-hardness proof. The search did not locate an explicit AC-feasibility PSPACE/∃R classification.
  The rectangular membership observation is routine and is not a novelty claim.
  (b) The resistive model in claim (1) is exactly the "OPF in DC networks" model of Gan–Low 2014
  (IEEE TPS 29(6)), who state it is "non-convex and NP-hard in general", and it is Lavaei–Low
  2012's "resistive network with active loads" case. The standard citation "OPF is NP-hard even
  if the network is resistive and there are no reactive loads" is Lavaei–Low 2012, Appendix B,
  Case 2 — see (c). No searched source gives a complexity classification beyond NP-hardness for this model, and the
  DC-with-constant-power-loads literature (Bolognani–Zampieri, Simpson-Porco–Dörfler–Bullo,
  Barabanov et al., Matveev et al., Jeeninga–De Persis–van der Schaft) contains no complexity
  statement at all; Jeeninga et al. show the loads-only case (fixed source voltages, no voltage
  bounds at loads) is decided by an LMI, which bounds where hardness can come from (Section 2b).
  (c) The "resistive lines + zero reactive injections ⇒ real (in-phase) voltages" step was used
  by Lavaei–Low 2012 (Appendix B, Case 2) to reduce OPF with Im Y = 0, |V_k| = 1, Q_k^min =
  Q_k^max = 0 to a ±1 quadratic problem. Their version imposes no angle-difference limit and is
  not correct as stated (splay equilibria on rings satisfy Q ≡ 0 with unequal angles); the
  claim's argument with |θ_i − θ_j| ≤ π/2 is the sound form. The lossless analogue (zero real
  injections force equal angles inside the π/2-cohesive region, via the convex energy function
  Σ a_ij (1 − cos(θ_i − θ_j))) is standard in Dörfler–Chertkov–Bullo 2013 (PNAS) and
  Dörfler–Bullo; Molzahn–Lesieutre–DeMarco 2012 restrict attention to equal-angle solutions for
  zero injections in lossless systems.
  (d) ETR-INV (Abrahamsen–Adamaszek–Miltzow, variables in [1/2, 2], constraints x + y = z,
  x·y = 1) [[abrahamsen2022-the-art-gallery-problem-is]] p.11 and the Miltzow–Schmiermann
  continuous-CSP result (any curved equality plus addition is ∃R-complete; compendium Section 1.4,
  ref. [MS24]) are the general tools; the fixed-injection one-neighbour bus V_i(V_i − V_j) = c is a
  "curved constraint" in that sense. The network-specific gadget design (pinned unit-voltage buses
  giving linear relations, complement copies 5/2 − v, degree-3 copy chains, the inversion bus) has
  no matching antecedent found in this search.

## 1. Direct searches for the claim

| Query family | Where | Result |
|---|---|---|
| "power flow"/"load flow"/"optimal power flow"/AC-OPF + "existential theory of the reals", ∃R-complete, ETR-complete, ER-complete (2024–2026 restricted and unrestricted) | WebSearch | 0 hits; only NP-hardness (Bienstock–Verma, Lehmann et al.) |
| power flow + "not in NP", "irrational solutions", certificate, Tarski/Renegar/quantifier elimination, PSPACE | WebSearch | only Bienstock–Verma Section 1.3 and Bienstock–Muñoz's irrational-QCQP remark; no PSPACE/∃R placement |
| "existential theory of the reals" + electrical network / circuit / Kirchhoff / resistor network | WebSearch | 0 relevant hits (compendium, geometry, NN training only) |
| DC/resistive network + constant power loads + NP-hard / complexity / solvability | WebSearch, downloaded PDFs (Section 2b) | NP-hardness only via Lavaei–Low; solvability papers give conditions, not classes |
| compendium text `/tmp/compendium.txt` | grep: power flow, load flow, electric, voltage, Kirchhoff, circuit, network flow, energy grid | 0 hits (circuit hits are arithmetic circuits only) |
| arXiv API (`export.arxiv.org`) | several queries | no response from the sandbox; not a usable negative result |
| Optimization Online site search for "existential theory of the reals" | WebSearch | 0 hits |

Local KB: no package mentions ∃R/ETR together with power, grid or flow; `bienstock2019`,
`bienstock2018`, `lehmann2015` (a different Lehmann et al. paper, switching/FACTS), `kocuk2016`,
`aigner2023` contain only NP-hardness statements.

## 2. What is already known (precise)

### (a) NP-hardness and the NP-membership question for AC feasibility

- Bienstock–Verma, *Strong NP-hardness of AC power flows feasibility*, Oper. Res. Lett. 47 (2019)
  494–501 (arXiv:1512.07315). Model: lossless (zero resistance, reactance x_ij > 0), unit voltage
  magnitudes, phase-angle limits θ_ij^max < π/2, "unconstrained reactive power flows and
  injections" [[bienstock2019-strong-np-hardness-of-ac]] p.1. Reduction from one-in-three 3SAT;
  the reduction "encodes some irrational quantities". Section 1.3 "Membership in NP": "A
  straightforward proof of such a fact, if true, is unlikely, for the reason that in a feasible
  solution very likely the f_ij (and possibly even some of the θ_i) would be irrational values. We
  conjecture that an approximate version of system (1) where equation (1b) is replaced with
  |sin(θ_i − θ_j) − x_ij f_ij| ≤ ε ... belongs to NP." [[bienstock2019-strong-np-hardness-of-ac]] p.6.
  This is the only place in the power-flow literature where NP membership is discussed. The claim
  under audit answers the implicit question (conditionally) and covers a *different* model
  (resistive instead of lossless); both hardness results together show the two extreme line
  models are hard.
- Verma, *Power grid security analysis: an optimization approach*, PhD thesis, Columbia 2009
  (open: http://www.columbia.edu/~dano/theses/verma.pdf). Chapter 5 proves Theorem 4.6.2
  (capacitated throughput maximization in the lossless nonlinear flow model is NP-hard) from
  one-in-three 3SAT with the "banana" network; Remark 5.1.6 (thesis pp. 142–144): "the two
  points where the curve crosses the horizontal line probably have irrational values, so we
  cannot express them exactly in the NP-completeness proof", fixed by a perturbation lemma. No
  membership discussion. (Chapter title says "NP-completeness proof" but only hardness is proved.)
- Lehmann, Grastien, Van Hentenryck, *AC-Feasibility on Tree Networks is NP-Hard*, IEEE TPS 31(1)
  2016, 798–801 (arXiv:1410.8253, downloaded and read). Model (Section II): polar; all voltage
  magnitudes fixed to 1; lines with conductance g ≥ 0 and susceptance b ≤ 0; fixed real and
  reactive demands P_i, Q_i at loads; generators with Σ p_ij ≥ 0 (no upper bound); angle-difference
  limit 0 < ∆ ≤ π/2; flows p_ij = g(1 − cos θ_ij) − b sin θ_ij, q_ij = −b(1 − cos θ_ij) − g sin θ_ij.
  Theorem 1: star networks with one load are NP-hard by reduction from Subset Sum (weak
  NP-hardness); the encoding "uses only rational numbers and finitely many real numbers
  constructed from rational numbers, sine, and cosine". Conclusion: the proof "relies on the
  existence of arbitrarily small bounds on voltage magnitudes ... and either generation bounds,
  capacity constraints, or a bound on phase angle differences". No membership discussion, no
  ∃R. Their model needs b ≠ 0 or g ≠ 0 with the ratio condition of Lemma 2; the lossy line (g > 0)
  with reactive demand is essential, unlike the claim's zero-reactive setting.
- Molzahn–Hiskens, *A Survey of Relaxations and Approximations of the Power Flow Equations*,
  FnT EES 4(1–2) 2019 (open: https://molzahn.github.io/pubs/molzahn_hiskens-fnt2019.pdf): cites
  only "[1] Bienstock–Verma, [2] Lehmann et al." for NP-hardness (pp. 2, 12, 20, 62, 107 of the
  PDF text); no membership or complexity-class discussion.
- Bienstock, Escobar, Gentile, Liberti, *Mathematical programming formulations for the AC-OPF*
  (4OR 2020 / Ann. Oper. Res. 2022; arXiv:2007.05334): "The ACOPF is NP-hard [12]"; nothing on
  membership or Tarski/PSPACE. Kocuk–Dey–Sun 2016 (arXiv:1504.06770): NP-hardness only.
- Bienstock–Muñoz 2018: "simple instances of PO (in fact convex, quadratically constrained
  problems) where all feasible solutions have irrational coordinates"
  [[bienstock2018-lp-formulations-for-polynomial-optimization]] p.9; PTAS for AC-OPF on bounded
  treewidth (Corollary 8). Consistent with the claim (approximate feasibility is easy on
  bounded treewidth; exact feasibility is ∃R-hard on degree-3 graphs of unbounded treewidth).
- The searches for "power flow" with Tarski, Renegar or PSPACE found no
  explicit upper-bound statement. This absence is not a novelty claim for
  the routine rectangular polynomial encoding.

### (b) The resistive model and DC power flow with constant-power loads

- Lavaei–Low, *Zero duality gap in optimal power flow problem*, IEEE TPS 27(1) 2012, 92–107
  (open: https://smart.caltech.edu/papers/zeroduality.pdf). Section "Resistive networks with
  active loads": "the OPF problem is NP-hard even if the network is resistive and there are no
  reactive loads. This situation, which corresponds to DC power distribution, is itself
  important". Appendix B, "NP-hardness of OPF problems", Case 2: Im{Y} = 0, |V_k| = 1,
  Q_k^min = Q_k^max = 0 for all generators, no line or angle limits (S^max = P^max = ∆V^max = ∞);
  they then write the OPF as min V^T Y V + Σ P_Dk s.t. V_k ∈ {−1, 1}, call this NP-hard "[33]"
  (a generic handbook citation; the problem is max-cut-like). Caveat: the step "Q ≡ 0 and Im Y = 0
  and |V| = 1 ⇒ V_k ∈ {±1}" is false without angle limits (a 3-cycle with unit conductances and
  angles 0, 2π/3, 4π/3 has Q_k = −Σ_j g sin(θ_k − θ_j) = 0 at every bus). Bienstock–Verma's
  stated purpose is to give "a rigorous proof" after this. So the *idea* of using zero reactive
  injections on a resistive network to force real voltages is Lavaei–Low's; the claim's
  energy/monotonicity argument with the ≤ π/2 angle limit is what makes it correct, and the
  claim's target (∃R, magnitudes in intervals rather than fixed) is different.
- Gan–Low, *Optimal power flow in direct current networks*, IEEE TPS 29(6) 2014, 2892–2904
  (open: https://smart.caltech.edu/papers/optimalflowjournal.pdf; equations are images, text
  read around them). Model: buses with real voltages, lines with admittance, Ohm's law, current
  balance, power balance p_i = V_i I_i, giving p_i = Σ_j y_ij V_i (V_i − V_j) (their (1)); substation
  bus 0 with fixed voltage; injection sets that are singletons (inelastic loads), two-point sets
  (on/off loads) or intervals [0, capacity] (generators); branch voltages within
  [V^min, V^max] (their (4a)–(4b)); line limits ignored. Abstract: "It is non-convex and NP-hard
  in general" (citing Lavaei–Low). This is the audited resistive model up to the choice of
  injection sets (the claim uses intervals, which include singletons); the claim should name it
  as the "DC network OPF"/"DC microgrid OPF" model and cite Gan–Low for its provenance and for the
  SOCP-exactness results (exact if voltage upper bounds do not bind, or uniform upper bounds and
  nonpositive injection lower bounds) — those tractable regimes are exactly the ones the gadgets
  violate (binding upper bounds, mixed-sign injections).
- Liu, Cui, Molzahn, Chen, Lu, *Optimal power flow in DC networks with robust feasibility and
  stability guarantees* (arXiv:1902.08163; IEEE TCNS): "there is no efficient solver with global
  optimality guarantee" for DN-OPF; NP-hardness via [9]/[27]; no class.
- Solvability literature for DC grids with constant-power loads (all downloaded, grepped for
  NP, polynomial time, complexity, tractable, decide, LMI, convex):
  - Bolognani–Zampieri, *On the existence and linear approximation of the power flow solution
    in power distribution networks*, IEEE TPS 31(1) 2016 (arXiv:1403.5031): sufficient
    existence condition by a fixed-point argument; no complexity.
  - Simpson-Porco, Dörfler, Bullo, *On resistive networks of constant power devices*, IEEE TCAS-II
    62(8) 2015 (arXiv:1503.04769): sufficient condition for all operating points to lie in a
    desirable set; no complexity (only "analytically intractable" in the informal sense).
  - Barabanov, Ortega, Griñó, Polyak, *On existence and stability of equilibria of LTI systems
    with constant power loads*, IEEE TCAS-I 63(1) 2016: necessary LMI condition, sufficient when
    a data-defined set is convex (single- and two-port systems); no complexity class.
  - Matveev, Machado, Ortega, Schiffer, Pyrkin, *On the existence and long-term stability of
    voltage equilibria in power systems with constant power loads*, IEEE TAC 65(11) 2020
    (arXiv:1809.08127): existence characterized via feasibility of the convex inequalities
    ⟨w_i⟩ + ⟨−b_i⟩/x_i − Σ_j a_ij x_j < 0 ("falls within the area of convex programming"), under
    Assumption 2.1 (a sign/monotonicity structure); no complexity class.
  - Jeeninga, De Persis, van der Schaft, *DC power grids with constant-power loads — Part I/II*
    (arXiv:2010.01076, arXiv:2011.09333; IEEE TAC 2023): for grids with fixed source voltages and
    constant-power loads (no voltage bounds at loads, no injection bounds at sources), the set F
    of feasible demand vectors is closed and convex (M4, Theorem 3.18) and feasibility is
    characterized by a necessary and sufficient LMI condition (M5, Theorem 3.22). Hence the
    loads-only, fixed-source-voltage DC problem is polynomially decidable (up to LMI precision),
    and the ∃R-hardness of claim (1) must and does come from voltage interval bounds on
    non-source buses combined with injection constraints (fixed injections at pinned buses and
    at the inversion bus, intervals elsewhere). The result file should state this boundary
    explicitly and cite Jeeninga et al.
  - Comănescu, *The steady states of isotone/antitone electric systems* (arXiv:2209.04208,
    2305.16268): monotone-operator existence/uniqueness; no complexity.
  None of these settles complexity in the sense of a class; they are consistent with the claim.
- Reference in the local KB: `lehmann2015-the-complexity-of-switching-and` (MPF with switching
  in the *linear* DC model) is a different model and does not overlap.

### (c) Precedents for "zero reactive injection on resistive lines forces equal angles"

- Lavaei–Low 2012, Appendix B Case 2 (above): same physical idea, no angle limit, incorrect as
  stated on cyclic networks. Should be credited as the origin of the trick and the standard
  source for "NP-hard even for resistive networks with no reactive loads".
- Lossless dual: Dörfler, Chertkov, Bullo, *Synchronization in complex oscillator networks and
  smart grids*, PNAS 110(6) 2013 (arXiv:1208.0045): the lossless power-flow equations
  ω_i = Σ_j a_ij sin(θ_i − θ_j) have at most one solution with |θ_i − θ_j| ≤ γ < π/2 on every edge,
  with the energy-landscape interpretation E(θ) = Σ a_ij (1 − cos(θ_i − θ_j)) − Σ ω_i θ_i
  (convex on the cohesive region). With ω = 0 the unique solution is θ ≡ const. The claim's
  reactive equations on resistive lines, Q_i = −Σ_j g_ij |V_i||V_j| sin(θ_i − θ_j) = 0, are exactly
  this system with weights a_ij = g_ij |V_i||V_j|, so the argument is a direct instance of the
  Dörfler–Bullo uniqueness argument (see also Dörfler–Bullo, *Synchronization in complex networks
  of phase oscillators: a survey*, Automatica 50 (2014); and Park, Zhang, Lavaei, Baldick,
  *Uniqueness of power flow solutions using monotonicity and network topology*, IEEE TCNS 2021,
  for monotonicity-based uniqueness with angle limits). Cite one of these rather than proving
  from scratch, but note the ≤ π/2 (non-strict) case needs the equality case of the convexity
  argument (sin is still monotone on [−π/2, π/2]; the potential is convex but not strictly on
  the boundary; connectedness with g_ij > 0 still gives equal angles).
- Molzahn, Lesieutre, DeMarco, *A sufficient condition for power flow insolvability with
  applications to voltage stability margins*, IEEE TPS 28(3) 2013 (arXiv:1204.6285, Section II-A):
  for a lossless system with zero injections "we restrict attention to candidate solutions in
  which all buses have the same voltage angle of zero" — existence direction only.
- Morton, *The admittance matrix and network solutions* (arXiv:2507.15331, Section on AC
  networks) and *Power flows with flat voltage profiles* (arXiv:2207.11963): classical
  observations that purely resistive AC networks with in-phase sources have in-phase voltages;
  expository, no bounds argument.
- No searched source states the claim's exact lemma ("in the full AC model with resistive lines, Q_i = 0
  at every bus and |θ_i − θ_j| ≤ π/2 on every line imply all angles equal, so the AC instance
  collapses to the resistive model"); it is a routine corollary of the Kuramoto uniqueness result.

### (d) ∃R toolbox precedents

- ETR-INV: Abrahamsen–Adamaszek–Miltzow, STOC 2018 / J. ACM 69(1) 2022, Definition 5 and Theorem 7
  [[abrahamsen2022-the-art-gallery-problem-is]] p.11; Abrahamsen–Miltzow, *Dynamic toolbox for
  ETRINV* (arXiv:1912.08674, local `abrahamsen2019-dynamic-toolbox-for-etrinv`), Theorem 1
  (rational equivalence to any compact ETR instance) — relevant if the result file also wants an
  "irrational/arbitrary algebraic degree solutions" corollary, as in
  `notes/pooling-existential-reals-novelty.md`.
- Miltzow–Schmiermann, *On classifying continuous constraint satisfaction problems* (FOCS 2021 /
  arXiv:2106.02397, compendium ref. [MS24]): CCSPs with addition and any "curved" equality
  constraint are ∃R-complete; the compendium (Section 1.4) summarizes it as "the inversion in
  ETR-INV can be replaced by virtually any curved function". The constraint V_i(V_i − V_j) = c of a
  fixed-injection one-neighbour bus is such a curved constraint, so a CCSP-based route exists;
  it does not by itself handle the network structure (each bus equation couples all neighbours,
  variables are voltages shared across gadgets, degree ≤ 3), which is what the gadget
  construction does. Mention as an alternative and as the general principle.
- Nearest structured ∃R results, none on networks: NMF (Shitov 2016), tensor rank, Nash
  equilibria, neural-network training (Bertschinger et al. 2023), Gram feasibility
  (arXiv:2603.19976); and the repository's own pooling result
  (`notes/pooling-existential-reals-novelty.md`, which records that Poss–Kurtz–Goerigk–Henke
  arXiv:2608.21574 state QCQP feasibility over a box is ∃R-complete as folklore).
- Compendium status: the copy at `/tmp/compendium.txt` is v1 (25 Jul 2024). A newer arXiv
  version may exist; re-grep it before submission, but the 2024–2026 web searches found no
  power-flow entry.

## 3. Assessment

1. **Claim (1), ∃R-completeness of the resistive/DC-network model: no matching result found.** The model is the
   Gan–Low 2014 DC-network OPF model and Lavaei–Low's resistive case, both of which say only
   "NP-hard". The constant-power-load solvability literature gives conditions and, for the
   loads-only fixed-source case, an LMI characterization (Jeeninga et al.), which the result
   file should cite as the tractable boundary. Membership in ∃R is immediate and should be
   stated with the compendium (A1) as the reference.
2. **Claim (2), ∃R-completeness of AC feasibility, with the stated restrictions: no matching result found.**
   Bienstock–Verma raised the NP-membership question (Section 1.3) and conjectured an ε-version
   is in NP; the claim gives a conditional NP-membership obstruction for the different,
   variable-magnitude resistive subclass used here; it does not resolve their
   lossless fixed-magnitude model. Credit Bienstock–Verma for the
   question and the irrationality observation, Verma 2009 Remark 5.1.6 for the earlier
   appearance of the irrationality obstacle, and Lehmann et al. 2016 for the tree-network
   (weak) hardness and for the observation that voltage bounds plus one of generation bounds /
   capacities / angle limits are needed. The "fixed finite data set" and "degree ≤ 3" features
   had no matching antecedent in the power-flow hardness sources searched (Bienstock–Verma use fixed constants
   but general graphs; Lehmann et al. use stars with data from Subset Sum).
3. **Equal-angle lemma: partially known.** Credit Lavaei–Low 2012 (Appendix B Case 2) for the
   resistive/zero-reactive trick and Dörfler–Chertkov–Bullo 2013 / Dörfler–Bullo 2014 for the
   uniqueness-in-the-π/2-region argument that makes it rigorous; note in the result file that
   Lavaei–Low's version omits the angle limit and fails on cycles, which is a small but useful
   correction to a widely cited remark.
4. **Technique: no matching construction found in the network sources searched.** ETR-INV and the CCSP "curved constraint" principle
   are the standard tools since 2018; the contribution is the gadget design (pinned buses as
   linear relations, complement copies, inversion bus) and the degree-3/finite-data control.
   Present it as such.
5. **Consequences worth stating with sources.** "Not in NP unless NP = ∃R" is the standard
   corollary (compendium Section 1); the analogous statement for QCQP feasibility is folklore
   (Poss et al. 2026, Theorem 4), so state the power-flow corollary for the precise model proved here, without
   claiming priority for all physical network models.

## 4. Sources the result file should cite

- Abrahamsen, Adamaszek, Miltzow, STOC 2018 / J. ACM 69(1) 2022, Definition 5, Theorem 7
  (ETR-INV). Local: `abrahamsen2022-the-art-gallery-problem-is` p.11.
- Schaefer, Cardinal, Miltzow, compendium arXiv:2407.18006, entry (A1) for membership, (L5) for
  ETR-INV, Section 1.4 for the curved-constraint remark; Miltzow–Schmiermann arXiv:2106.02397.
- Bienstock, Verma, Oper. Res. Lett. 47 (2019), Section 1 (model) and Section 1.3 (NP
  membership). Local: `bienstock2019-strong-np-hardness-of-ac` p.1, p.6.
- Lehmann, Grastien, Van Hentenryck, IEEE TPS 31(1) 2016 / arXiv:1410.8253, Section II (model),
  Theorem 1, Section IV.
- Verma, PhD thesis, Columbia 2009, Theorem 4.6.2, Remark 5.1.6.
- Lavaei, Low, IEEE TPS 27(1) 2012, Section on resistive networks and Appendix B Case 2.
- Gan, Low, IEEE TPS 29(6) 2014 (DC-network OPF model; SOCP exactness conditions).
- Jeeninga, De Persis, van der Schaft, arXiv:2010.01076 (Part I, M4–M5, Theorems 3.18, 3.22)
  and arXiv:2011.09333 (Part II) for the tractable loads-only boundary; optionally
  Bolognani–Zampieri 2016, Simpson-Porco–Dörfler–Bullo 2015, Barabanov et al. 2016, Matveev et
  al. 2020 as the solvability-condition literature.
- Dörfler, Chertkov, Bullo, PNAS 110(6) 2013 / arXiv:1208.0045 (uniqueness of cohesive
  solutions, energy function); Dörfler, Bullo, Automatica 50 (2014) survey.
- Bienstock, Muñoz, SIAM J. Optim. 28 (2018), Corollary 8 and the irrational-coordinates remark.
  Local: `bienstock2018-lp-formulations-for-polynomial-optimization` p.9.
- Molzahn, Hiskens, FnT EES 4 (2019) as the survey that records only NP-hardness.

## 5. Open-access sources worth ingesting (not ingested)

- Lehmann, Grastien, Van Hentenryck, arXiv:1410.8253 (PDF open; short, model needed verbatim).
- Lavaei, Low 2012, https://smart.caltech.edu/papers/zeroduality.pdf (author copy; Appendix B).
- Gan, Low 2014, https://smart.caltech.edu/papers/optimalflowjournal.pdf (author copy; equations
  are images, so `pdftotext` loses the model — verify against `original.pdf`).
- Verma 2009 thesis, http://www.columbia.edu/~dano/theses/verma.pdf (advisor's site; long).
- Jeeninga, De Persis, van der Schaft, arXiv:2010.01076 and arXiv:2011.09333.
- Dörfler, Chertkov, Bullo, arXiv:1208.0045 (PNAS preprint with SI).
- Molzahn, Hiskens 2019, https://molzahn.github.io/pubs/molzahn_hiskens-fnt2019.pdf (author copy).
- Miltzow, Schmiermann, arXiv:2106.02397.
- Lower priority: Simpson-Porco–Dörfler–Bullo arXiv:1503.04769; Matveev et al. arXiv:1809.08127;
  Bolognani–Zampieri arXiv:1403.5031; Molzahn–Lesieutre–DeMarco arXiv:1204.6285; Liu et al.
  arXiv:1902.08163.
- Not open: Barabanov et al. 2016 (IEEE TCAS-I; HAL record hal-02378521 has metadata only).

Downloaded working copies used for this audit are in `/tmp/pfaudit/` (not part of the KB).
