# Prior-literature audit: ∃R-completeness of the pooling problem

Date: 2026-09-05. Status: novelty audit of `results/pooling-existential-theory-of-reals.md`
(Theorem 1, Corollaries 2 and 3). Not a proof audit.

## Verdict

**No matching result found in the sources searched; the ingredients are known.**

This is a bounded literature search, not proof of priority. Statements below
about absence refer to the searched sources and versions, not the entire
literature. The final closeout is recorded in
[the reconciliation audit](review-existential-reals-closeout.md).

- The search found no published or preprint source stating ∃R-hardness, ∃R-completeness, "not in NP unless
  NP = ∃R", or ∃R membership for the pooling problem, blending problems, or any bilinear
  network-flow problem. The ∃R compendium (arXiv:2407.18006) has no entry for pooling,
  blending, bilinear programming, QCQP, network flow, or power/gas/water flow; its
  optimization-flavoured entries are matrix/tensor rank problems (A16–A27) and Nash
  equilibria with constraints (GT1–GT22).
- What is known and must be credited (details below): (a) feasibility of a system of
  quadratic polynomials over a compact domain is ∃R-complete (Schaefer 2013, Lemma 3.9,
  unit ball; Schaefer–Štefankovič 2017, Corollary 4.4 plus remark); (b) the general
  quadratically constrained feasibility problem over a rational polyhedron, with or without
  a box, has been stated explicitly to be ∃R-complete in an OR paper (Poss, Kurtz, Goerigk,
  Henke, arXiv:2608.21574, Theorem 4, citing the compendium); (c) Bienstock–Verma 2019 raised
  NP membership of AC power-flow feasibility as unlikely because of irrational solutions and
  conjectured only an ε-version is in NP; (d) pooling optima with square roots are implicit
  in Haugland–Hendrix 2015, and "NMF requires irrationality" (Chistikov et al. 2017) plus
  Shitov's ∃R-completeness of NMF are the closest structured-bilinear analogues of
  Theorem 1 and Corollary 3.
- The reduction technique (ETR-INV gadgets realized by pool dilution, saturation forced by
  the objective, and inversion via a terminal quality equation) had no matching antecedent in the
  pooling or network-flow sources searched. ETR-INV has been used outside geometry (neural-network
  training, Bertschinger et al. NeurIPS 2023; Gram feasibility, arXiv:2603.19976), but not
  in flow networks. The inversion-by-quality trick is specific to blending.

## 1. Direct searches for the claim

| Query family | Where | Result |
|---|---|---|
| "pooling problem" + existential theory of the reals / ∃R / ETR | WebSearch, arXiv API (`all:"pooling problem" AND (existential OR "theory of the reals" OR ETR)`), Optimization Online site search for "existential theory of the reals" | 0 hits |
| "pooling problem" + "in NP" / NP membership / certificate / PSPACE / irrational / algebraic degree | WebSearch | only NP-hardness statements; no membership or irrationality statement |
| blending / bilinear / QCQP / network flow / power flow / gas / water + ∃R | WebSearch, arXiv API abstract search | only the sources in Section 2; no network-structured ∃R result |
| compendium text `/tmp/compendium.txt` | grep for pooling, blending, bilinear, quadratic program, quadratically constrained, QCQP, network flow, power flow, gas/water network | 0 hits for all |
| DBLP API | queries for "existential theory reals" with flow/quadratic/bilinear/pooling/power | service returned empty or HTTP 500; not a usable negative result |

Local KB (`literature/`): grep for "existential theory", "∃R", "ETR", "Schaefer", "Stefankovic",
"NP membership", "in NP" hits only unrelated packages (allender2009, koppe2012, basu*, loera2008,
odonnell2017, blanco2025, beck2023, ...). No pooling package mentions any of these terms.

## 2. What is already known (precise)

### (a) Quadratic feasibility over a compact domain is ∃R-complete

- Schaefer, *Realizability of graphs and linkages* (2013), Lemma 3.9: common-root feasibility
  for polynomials f_i : R^n → R, i ∈ [s], restricted to B^n(0,1) (the unit ball), is
  ∃R-complete even when every f_i has total degree at most 2.
  (https://ovid.cs.depaul.edu/documents/realizability.pdf, p.~22 of the preprint.) The domain in
  the lemma is the unit ball, not a box. The draft's Remark 4 says "quadratic feasibility over a
  box (Schaefer 2013, Lemma 3.9)"; correct this to "unit ball" or cite the compendium's phrasing.
- Schaefer–Štefankovič, *Fixed points, Nash equilibria, and the existential theory of the reals*,
  Theory Comput. Syst. 60 (2017), Corollary 4.4 establishes ∃R-completeness of QUAD and 4-FEAS.
  The subsequent discussion attributes the unit-ball restriction B^n(0,1) for common-zero
  feasibility of QUAD to [31, Lemma 3.9], using Corollary 4.4.
  (https://ovid.cs.depaul.edu/documents/Nash.pdf)
- Compendium arXiv:2407.18006, entry (A1) Feasibility reports ∃R-completeness with degree at
  most 2 on compact domains including the unit ball and [−1,1]^n, citing [Sch13, Lemma 3.9].
  Theorem 2.4 (Schaefer) gives ∃R-completeness for a single polynomial having a root in [−1,1]^n.
  Hansen 2019 (Theory Comput. Syst. 63) uses a quadratic-equation system whose solution is
  promised to belong to a polyhedron inside the standard simplex
  (compendium entry GT9/minmax; ref [Han19]).
- Related structured results: NMF is ∃R-complete (Shitov 2016, compendium A21, from (A1));
  tensor rank (Schaefer–Štefankovič 2018, Shitov 2016; A26); Affine Rank Minimization
  (arXiv:2602.14037, 2026); Constrained Nonnegative Gram Feasibility (arXiv:2603.19976, 2026, via
  ETR-AMI). All are bilinear/multilinear feasibility problems with sign or affine constraints; none
  is a flow problem.

### (b) General QCQP / bilinear feasibility stated as ∃R-complete

- Poss, Kurtz, Goerigk, Henke, *The complexity landscape of robust (integer) linear programming*,
  arXiv:2608.21574 (21 Aug 2026), Section 2: QP asks "∃z ∈ Z : zᵀQ_ℓ z ≤ 0, ∀ℓ ∈ [L]?" with Z a
  rational polyhedron; Bounded-QP additionally restricts z to the box [−R,R]^{n_z}.
  Theorem 4 ([35]) gives ∃R-completeness for QP and Bounded-QP, citing the compendium [35]
  without a proof. Theorem 5 ([32]) gives NP-completeness for Bounded-QMIP-Single and QMIP-Single
  (single quadratic constraint; the Vavasis/Del Pia–Dey–Molinaro line). This is the only OR-side
  source found that explicitly says QCQP feasibility is ∃R-complete; it is a citation of folklore,
  not a new proof, and says nothing about network structure or blending.
- Vavasis 1990 (*Quadratic programming is in NP*) and Del Pia–Dey–Molinaro 2017 (MIQP in NP) give
  NP membership only for one quadratic objective/constraint over linear constraints. Köppe 2012,
  *On the complexity of nonlinear mixed-integer optimization*, notes for integer variables that
  QCQP feasibility is NP-hard, with NP membership unresolved in that account
  [[koppe2012-on-the-complexity-of-nonlinear]] p.8. Bienstock–Muñoz 2018 give simple convex,
  quadratically constrained polynomial-optimization instances that have no feasible solution
  with entirely rational coordinates [[bienstock2018-lp-formulations-for-polynomial-optimization]] p.9.
  Bienstock, Del Pia, Hildebrand, *Complexity, exactness, and rationality in polynomial
  optimization* (arXiv:2011.08347; Math. Program.) study rational vs. irrational certificates for
  QCQP; they do not treat pooling or ∃R.

### (c) NP membership of pooling in the pooling literature

- Alfaki–Haugland 2013, Section 3 "Computational complexity": proves strong NP-hardness only
  [[alfaki2013-strong-formulations-for-the-pooling]] p.4 (Sect. 3 header at fulltext line 95). No
  NP membership or certificate statement.
- Haugland 2016 (J. Global Optim. 64) explains that each hardness argument uses a polynomial
  reduction from an NP-complete decision problem to the pooling decision problem, establishing
  NP-hardness
  [[haugland2016-the-computational-complexity-of-the]] p.7; conclusion states only NP-hardness
  (strong or weak) and leaves pseudo-polynomial solvability for |K|=1, |S|=|T|=2 open
  [[haugland2016-the-computational-complexity-of-the]] p.16. Section 2.1 confirms that lower
  quality bounds are included and reducible to upper bounds on a negated attribute
  [[haugland2016-the-computational-complexity-of-the]] p.4 (supports Remark 3 of the draft).
- Dey–Gupte 2015, Gupte et al. 2017, Boland–Kalinowski–Rigterink 2017 (both packages),
  Baltean-Lugojan–Misener 2018: fulltext greps for "in NP", "NP-complete", "certificate",
  "irrational", "existential" find no NP-membership statement (Dey–Gupte only has the
  inapproximability statement conditional on NP ⊆ BPP).
- Letsios et al. 2020 survey (arXiv:1909.12328, Table 1 and Section 3.1): lists only "P" and
  "NP-hard" rows for pooling subclasses; the words "NP-complete" or "in NP" never appear for
  pooling; no open question about NP membership is raised.
- The searched pooling sources did not explicitly raise the general decision problem’s NP-membership question.

### (d) Irrational optimal solutions of pooling / bilinear programs

- Haugland–Hendrix 2015, *On a pooling problem with fixed network size* (ICCL 2015, user-supplied
  package, `status: unread`): for atomic instances (2 sources, 2 terminals, 1 quality) the optimal
  y is of the form r_0 ± √r_1 with rational r_0, r_1. The paper warns that comparing the two
  irrational values directly has no bounded bit-operation cost [[haugland2015-on-a-pooling-problem-with]] p.350. So irrational (degree-2) pooling
  optima with rational data are implicit in the literature; arbitrary algebraic degree
  (Corollary 3) is not.
- Bienstock–Verma 2019 (AC power flow), Section 1.3 "Membership in NP", treats possible
  irrationality of feasible f_ij and possibly θ_i as an obstacle to a simple NP-membership
  argument. The authors conjecture NP membership for an approximate formulation. [[bienstock2019-strong-np-hardness-of-ac]] p.6. No
  ∃R statement; no later ∃R result for AC-OPF was found (WebSearch 2020–2026, compendium).
- Chistikov, Kiefer, Marušić, Shirmohammadi, Worrell, *Nonnegative matrix factorization requires
  irrationality*, SIAM J. Appl. Algebra Geom. 1(1) 2017, 285–307 (arXiv:1605.06848): rational
  matrices whose minimal NMF needs irrational factors. Analogue of Corollary 3 for a structured
  bilinear system; degree 2 only.
- Berthelsen–Hansen 2022 (compendium GT14): deciding existence of an irrational Nash equilibrium
  is ∃R-hard; another "irrationality is forced" precedent.
- Abrahamsen–Miltzow, *Dynamic toolbox for ETRINV*, arXiv:1912.08674: Definition 19 (ETR-INV with
  1/2 ≤ x_i ≤ 2, constraints x+y=z, x·y=1), Theorem 1 (∃R-complete, rationally equivalent to any
  compact ETR), Corollary 2 (for algebraic α, an instance solvable over Q[α] but not over any field
  missing α). Verified. This is the source of Corollary 3 and should stay cited.

### (e) Verified citation details in the draft

- Abrahamsen–Adamaszek–Miltzow, arXiv:1704.06969v4 (STOC 2018): Definition 5 (ETR-INV with
  equations x=1, x+y=z, x·y=1, variables in [1/2,2]) and Theorem 7 (ETR-INV is ∃R-complete) —
  numbering verified against the PDF. J. ACM 69(1) 2022 version may renumber; cite the arXiv/STOC
  numbering explicitly.
- Compendium citation (A1) is correct; the draft should also cite Theorem 2.4 and its
  qualified attribution of the first known proof to Schaefer [Sch13, Lemma 3.9].

## 3. Assessment

1. **Theorem 1 as a statement about pooling: a candidate new result.** No matching statement
   was found in the searched pooling, bilinear-programming, or ∃R sources. The
   nearest published statements are the folklore "QCQP feasibility is ∃R-complete" (Poss et al.
   2026, Theorem 4, from the compendium) and Schaefer's Lemma 3.9. Neither implies hardness for the
   pooling structure (constant source qualities, flow-weighted quality averaging, one attribute,
   qualities in {0,1}), so the result is not a corollary of known work. The draft's "no
   NP-membership statement for the general problem appears in that literature" is confirmed.
2. **Corollary 2: no matching pooling statement found**, but the phrasing should acknowledge that the same
   conditional non-membership holds for general QCQP feasibility and is folklore there.
3. **Corollary 3: partially known.** Square-root optima for pooling with rational data are
   implicit in Haugland–Hendrix 2015 (p.350); the "arbitrary algebraic degree" strengthening had no match in this search
   and rests on Abrahamsen–Miltzow Corollary 2. The result file should cite Haugland–Hendrix 2015
   for the degree-2 precedent, and Chistikov et al. 2017 as the analogous structured-bilinear
   irrationality result.
4. **Technique: no matching pooling/network construction found.** ETR-INV has been the standard source for
   ∃R reductions since 2018 (art gallery, neural-network training, curve straightening, Gram
   feasibility), so using it is not itself a contribution; the gadget design (dilution pools that
   turn a flow into a quality, saturation forced by the objective as in Haugland's reductions,
   inversion via a fixed-quality terminal) is where the novelty lies and should be presented as
   such. Hansen 2019's "quadratic system inside a polyhedron in the simplex" variant of Lemma 3.9
   is the closest technique for problems with normalization constraints and could be mentioned
   as an alternative route.
5. **Related ∃R results worth crediting** (none is a flow problem): NMF (Shitov 2016; Chistikov et
   al. 2017 for irrationality), tensor rank (Schaefer–Štefankovič 2018), Nash-equilibrium decision
   problems (Garg–Mehta–Vazirani–Yazdanbod 2018; Bilò–Mavronicolas 2021; Berthelsen–Hansen 2022),
   Arrow–Debreu market equilibria (Garg et al. 2017), linkage realizability (Kempe/Abbott/Schaefer)
   as the origin of "flows realize arithmetic" style universality. Bienstock–Verma 2019 should be
   cited as the closest operations-research precedent for questioning NP membership of a
   nonconvex network feasibility problem.

## 4. Sources the result file should cite (additions marked +)

- Abrahamsen, Adamaszek, Miltzow, STOC 2018 / arXiv:1704.06969, Definition 5, Theorem 7 (kept).
- Abrahamsen, Miltzow, arXiv:1912.08674, Definition 19, Theorem 1, Corollary 2 (kept; fix
  numbering of the definition if quoted).
- Schaefer, Cardinal, Miltzow, arXiv:2407.18006, entry (A1), Theorem 2.4, Section 2 (kept).
- Schaefer 2013, Lemma 3.9 — state "unit ball", not "box" (kept, corrected).
- + Schaefer, Štefankovič, Theory Comput. Syst. 60 (2017) 172–193, Corollary 4.4 and the remark
  following it (QUAD ∃R-complete, also in the unit ball).
- + Poss, Kurtz, Goerigk, Henke, arXiv:2608.21574 (2026), Section 2, Theorem 4 (explicit "QP and
  Bounded-QP are ∃R-complete" in the OR literature) and Theorem 5 (single-constraint NP-complete).
- + Vavasis, Inf. Process. Lett. 36 (1990) 73–77; Del Pia, Dey, Molinaro, Math. Program. 162
  (2017) (NP membership for single quadratic constraint, to contrast).
- + Bienstock, Verma, Oper. Res. Lett. 47 (2019) 494–501, Section 1.3 (NP membership of AC
  feasibility doubted; ε-version conjectured in NP). Local: `bienstock2019-strong-np-hardness-of-ac` p.6.
- + Haugland, Hendrix, ICCL 2015, LNCS 9335, 328–342 (square-root optima). Local:
  `haugland2015-on-a-pooling-problem-with` p.350 (user-supplied; package still `unread`, so a
  reader must set status before citing it in a result).
- + Chistikov, Kiefer, Marušić, Shirmohammadi, Worrell, SIAM J. Appl. Algebra Geom. 1 (2017)
  285–307; Shitov, *A universality theorem for nonnegative matrix factorizations*, arXiv:1606.09068
  (structured bilinear ∃R-completeness and forced irrationality).
- + Letsios et al., Comput. Chem. Eng. 132 (2020) 106599, Table 1 (survey lists only NP-hard/P
  rows; no membership statement).
- Haugland 2016 (kept; add p.4 for lower bounds, p.7 for the hardness-only remark).
- Alfaki, Haugland 2013 (kept).
- Canny 1988 (kept).

## 5. Gaps in this audit

- DBLP API was unavailable (empty/HTTP 500), so DBLP was not searched; arXiv API, Optimization
  Online, WebSearch, the compendium text, and the local KB were.
- Google Scholar was reached only through general web-search snippets.
- Journal versions of Abrahamsen–Adamaszek–Miltzow (J. ACM 2022) and of Abrahamsen–Miltzow were
  not checked for renumbering.
