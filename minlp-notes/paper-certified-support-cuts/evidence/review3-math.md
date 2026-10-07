# Review round 3: new and changed mathematics

Scope: the eight items (a)-(h) of the round-3 math lens. Sources are the current `sections/*.tex`;
page numbers refer to `main.pdf` and were read from `development/draft-round3/main.txt`.

## Summary

No item contains a mathematical error. Every number in the new Section 3.4 paragraph was
reproduced independently. The two-leaf hardness argument, the block-closure derivation, the glued
bound 0 with the coupling row, the Appendix A.4 examples and the Section 2 description of SCIP's
implicit-discreteness presolve are all correct. Five findings remain (all minor) plus two
suggestions:

- **F1:** the Shapley-Folkman remark in Section 8.5 reads Aubin-Ekeland correctly, but the bound
  is loose. On these instances it is 100 to 1000 times larger than the observed gaps, and on three
  instances it exceeds the optimum. It therefore does not explain why the block closure is close
  to the optimum.
- **F2:** two phrases in the new Section 3.4 paragraph are ambiguous or say more than the evidence.
- **F3:** the abstract does not qualify "dense semidefinite relaxations".
- **F4:** the hardness sentence in Section 4.2 is loosely worded.
- **F5:** Section 5.3 and Appendix D repeat each other almost verbatim.

## Checks run (targeted; no SCIP or Gurobi runs)

All commands were run with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` and
`/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`. The SDP solves use
CVXPY with Clarabel and SCS. They are continuous convex solves, not MINLP solver runs.

| Command | Result |
|---|---|
| `verification/M7_dense_fullgap.py` (existing) | path: SDP -0.1220566, rational point -0.122056; r=1: 0.5; r=2: rational point 1.85e-7; r=3: 7.99e-7 |
| `verification/R9_math_bnw_path4.py` (existing) | exact min 0 at x=0 only; dense -0.1220566; dense+triangles -0.0001432; glued edges -1.4544316; PASS |
| `verification/R10_math_checks.py` (new, this round) | all checks PASS (listed below) |
| one-off scripts (reading `experiments/v4/c4-references.json` and the generator `mechanism_c4.py` with bytecode writing disabled) | per-instance nonconvexity rho_i, coupling capacity c, bisection accuracy |
| `pdftotext` on `literature/papers/burer2025-on-the-semidefinite-representability-of/original.pdf`, pp. 2, 14, 43-44 | data of Example 4, Proposition 12 and the rational point |
| `grep` / `sed` on `/workspace/local-home/build-scip/scipoptsuite-10.0.3/scip/src/scip/cons_nonlinear.c` | `isSingleLockedCand`, `presolveSingleLockedVars`, parameter `checkvarlocks` |

`R10_math_checks.py` is independent of M7 and R9. It uses its own exact linear algebra
(Sylvester criterion with Bareiss determinants, not LDL^T), its own face enumeration, a second
SDP solver and a different interior point for rounding. It builds the full-gap objective from
the formula with sympy, and it computes the glued value through the Lagrangian dual of
Proposition 3.5(ii) with exact pair minima. Results:

- A1. The BNW Section 6.4 point x = (3/32, 3/16, 9/16, 3/4) with the X matrix from p. 43 of the
  local PDF has a positive definite moment matrix (exact). It satisfies all McCormick inequalities
  of all 10 products and squares, and its objective is exactly -109/1024.
- A2. The exact minimum over [0,1]^4 is 0, attained only at x = 0.
- A3. The dense SDP with all McCormick inequalities gives -0.1220566 with both Clarabel and SCS.
  BNW report -0.1220566 (Mosek).
- A4. Glued edge hulls: the SDP gives -1.4544316 (Clarabel and SCS). The exact Lagrangian lower
  bound is -1.454431581 and an exactly checked rational feasible point gives -1.454431392.
- B. Full gap, minimum 1/2 for r = 1, 2, 3. For r = 1 the dense value is 0.5 numerically, and the
  symbolic identity (eq:sdp-identity) gives the rigorous lower bound 1/2. For r = 2 and r = 3 the
  rational positive definite, McCormick-feasible points have values 2.5e-8 and 1.2e-7 (< 1e-6).
- C. Exact vertex enumeration on 81 graphs (all graphs with n = 3, 4; random graphs with n = 5, 6):
  every vertex is half-integral, its value is -|O| + h(n/4 - 1/2), and the minimum is -alpha(G).
- D. Section 8.5:
  - Part 4C4: c >= 87/64 on all 20 instances.
  - Chord crossings lie inside both segments with m_y <= 0.733 <= 3/4, and sum_i m_{y_i} <= 0.8n
    on all 40 instances (seeds 0-9).
  - optimum - block closure <= rho_max on every instance.
- E. Appendix A.4 example 1: pair minima 3/4 and -1/4, beta* = 1/2, Delta' = 0. Example 2:
  beta* = Delta = 2/3. The binomial weights of Proposition 3.4 have equal moments up to kappa
  (checked for kappa <= 14).

## Findings

### F1 [minor] The Shapley-Folkman remark does not explain the closeness it is cited for

- **Location.** `sections/08e-path.tex:194-197` (Section 8.5, p. 32).
- **Issue.** The text reads: "With a single coupling row, the block closure is close to the
  optimum for a known reason: by the Shapley--Folkman estimate of \citet{AubinEkeland1976}, the
  duality gap of a separable problem with one coupling constraint is at most twice the largest
  nonconvexity ... of a single block."
- **Is the reading correct?** Yes. Aubin-Ekeland bound the gap by min(m+1, n) rho(f_1) (as quoted
  by Udell and Boyd 2016, p. 7 of the local copy `literature/papers/udell2016-...`). With m = 1
  this is 2 rho_max. The box 0 <= y_i <= 1 belongs to the block domains.
- **The bound is not tight.** For one linear coupling row the gap is at most rho_max. Udell-Boyd
  (2016), Theorem 1, give this with m~ = 1, and a direct argument gives it too: at an optimum of
  the convexified problem, all blocks that lie strictly inside a segment of their envelope with the
  common slope -mu can be moved to the segment endpoints at constant cost and constant sum_i y_i,
  except one.
- **The bound does not explain the data.** On the 20 Part 4C4 instances, rho_max lies between
  0.035 and 0.216, so 2 rho_max lies between 0.071 and 0.432. The observed distance between the
  optimum and the block closure is at most 6.47e-4, and gap/rho_max <= 0.013. On three n = 10
  instances, 2 rho_max even exceeds the optimum itself:

  | instance | 2 rho_max | optimum |
  |---|---|---|
  | n10_s5 | 0.155 | 0.130 |
  | n10_s7 | 0.178 | 0.095 |
  | n10_s8 | 0.172 | 0.070 |

  The estimate shows only that the absolute gap does not grow with n. It does not show that the
  closure is close to the optimum on these instances.
- **Evidence.** `R10_math_checks.py`, part D: rho_i = max over y in [0,1] of
  (d_i - vex d_i), computed with a lower convex hull on the grid j/2^14. The per-instance table
  came from a one-off run of the same code.
- **Fix.** Replace "With a single coupling row, the block closure is close to the optimum for a
  known reason: ... of a single block." with:

  > With a single coupling row, the Shapley--Folkman estimate of \citet{AubinEkeland1976} bounds
  > the distance between the block closure and the optimum by twice the largest nonconvexity
  > $\max_y(d_i(y)-\operatorname{vex}d_i(y))$ of a single block, independently of $n$. On these
  > instances this bound lies between $0.07$ and $0.43$, far above the observed distances of at
  > most $6.5\cdot10^{-4}$, so it explains why the distance does not grow with $n$ but not why it
  > is this small.

  Optionally add: "for a linear coupling row the factor two can be dropped
  \citep[Theorem~1]{UdellBoyd2016}". If so, a bib entry is needed; the paper is in the local
  library.

### F2 [minor] Section 3.4, new paragraph: an ambiguous referent, and "much stronger" for four variables

- **Location.** `sections/03-composition.tex:343-354` (Section 3.4, p. 11).
- **Issue 1.** "the dense relaxation contains a rational point with objective value -109/1024
  [BNW, Sec. 6.4]; numerically its value is about -0.122". Grammatically, "its" can refer to the
  rational point, whose value is -109/1024, about -0.106. The number -0.122 is the optimal value
  of the relaxation (BNW, Table 6).
- **Issue 2.** "For blocks of four or more variables, joint support cuts can therefore be much
  stronger than dense first-level relaxations". The large gaps come from the instances with five
  and seven variables. On the four-variable path the dense relaxation misses 0.122 of a minimum
  0, and the objective coefficients reach 29, so "much" is supported only from five variables on.
- **Fully supported.**
  - The data of Example 4 (diagonal 8, 25, 25, 8; off-diagonal -14, -25, -14; c = (12, 29, 0, 0);
    tridiagonal, so a path).
  - The minimum 0, unique at x = 0.
  - BNW's rational point: Section 6.4, Proposition 12. It is feasible for BNW's relaxation (2),
    and BNW state, and our exact check confirms, that it also satisfies all lower McCormick
    inequalities. It therefore lies in the manuscript's "dense relaxation with the McCormick
    inequalities of all products".
  - The values -0.122 and -1.454.
  - The full-gap values: below 1e-6 for r = 2, 3, verified exactly as upper bounds by rational
    points; exactly 1/2 for r = 1 by the identity and BNW Theorem 1.
  - The padding argument behind "from four variables on".
- **Fix.** Replace "numerically its value is about $-0.122$, and that of the glued pair hulls of the
  three edges about $-1.454$." with:

  > the optimal value of the dense relaxation is about $-0.122$, and that of the glued pair hulls of
  > the three edges about $-1.454$.

  Replace the last sentence with:

  > For blocks of four or more variables, joint support cuts can therefore be strictly stronger
  > than dense first-level relaxations, not only more economical; on the full-gap instances with
  > five and seven variables, the dense relaxation recovers almost none of the minimum.

### F3 [minor] The abstract does not qualify "dense semidefinite relaxations"

- **Location.** `sections/00-abstract.tex:12-13` (p. 1).
- **Issue.** "from four variables on, joint blocks can be strictly stronger than dense
  semidefinite relaxations". The evidence (Section 3.4) concerns the dense first-level (Shor)
  relaxation with the McCormick inequalities of all products. Higher levels of dense moment
  relaxations are not covered, and Section 3.3 itself notes convergence as the number of moments
  grows. The introduction (`01-introduction.tex:64-67`), Section 3.4 (last sentence) and the
  conclusions (`09-conclusions.tex:13`) state the qualified version.
- **Fix.**

  > and from four variables on, joint blocks can be strictly stronger than the dense first-level
  > semidefinite relaxation with all McCormick inequalities.

### F4 [minor] Section 4.2, hardness sentence: "half-integral coordinates" and "that of a stable set"

- **Location.** `sections/04-quadratic.tex:116-118` (Section 4.2, p. 14).
- **Issue.** "at a vertex with $h\ge1$ half-integral coordinates the value exceeds that of a stable
  set by $h(n/4-1/2)>0$".
  - The integers 0 and 1 are half-integral too. The intended count is the number of coordinates
    equal to 1/2.
  - "that of a stable set" leaves open which stable set is meant. It is the stable set O of the
    coordinates equal to 1, with value -|O| >= -alpha(G).
- **The mathematics is correct.**
  - The objective is concave and integer-valued at stable sets.
  - The polytope's vertices are half-integral; adding x <= 1 does not change this.
  - The value at a vertex is -|O| + h(n/4 - 1/2).
  - The minimum is -alpha(G).
  - Coefficients are integers of size at most n, so the reduction from stable set gives strong
    NP-hardness.
- **Evidence.** `R10_math_checks.py`, part C: exact vertex enumeration on 81 graphs.
- **Fix.**

  > and at a vertex with $h\ge1$ coordinates equal to $\tfrac12$ the value exceeds the value
  > $-\abs O$ of the stable set $O$ of its coordinates equal to $1$ by $h(n/4-1/2)>0$.

### F5 [minor] Section 5.3 and Appendix D repeat each other

- **Location.** `sections/05-original.tex:185-203` (Section 5.3, p. 18);
  `sections/A-feasible-hull.tex:3-6, 33-50` (Appendix D, p. 49).
- **Issue.** Condensing Section 5.3 left the moved material in both places:
  - Appendix D opens with the same two sentences as Section 5.3 ("The closure $\mathcal C$ is a
    relaxation ... free direction in the affine parts").
  - It then repeats the example x^2 = 1/4 (Example D.2): "the point x = 1/4 is the mean of the
    measure with mass 3/4 at 0 and 1/4 at 1, which satisfies the row in expectation", "This is a
    Lagrangian duality gap", "It is closed by convexifying aggregated sets ... as in the
    aggregation closure of DeyMunozSerrano2022 ... by placing the row inside D, which changes the
    support problem; our implementation keeps nonlinear rows out of D so that the support problems
    stay in the classes of Section 4".
  - Section 5.3 presents this example in full but does not cite its label, although Section 5.2
    (`05-original.tex:133`) already refers to it as Example D.2.
- **Consistency.** Statements and labels agree:
  - Proposition D.1 (full row rank of the free columns) is a precise form of "every row has its own
    free direction".
  - Example D.2 matches the text.
  - The hierarchy and both strictness examples are correct. They were rechecked by hand: z <= 1/2
    at x = 1 on conv Sigma, and (1,1) lies in every conv Sigma_lambda and in C.
- **Fix.** Keep the discussion in one place. For example, replace `05-original.tex:191-201`
  ("For $D=[0,1]$ and the equality row ... classes of Section~\ref{sec:quadratic}.") with:

  > For the equality row $x^2=1/4$ on $D=[0,1]$, whose feasible set is $\{1/2\}$, even the complete
  > family of cuts accepts $x=1/4$ (Example~\ref{ex:quarter}); this is a Lagrangian duality gap,
  > not a failure of the direction search.

  Then delete the first paragraph of Appendix D (lines 3-6), or replace it with "This appendix
  proves the sufficient condition of Section~\ref{sec:feasible-hull} and the strictness claims."
  Keep the rest of Appendix D.

### F6 [suggestion] Appendix A.4, example 1: the re-splitting term contains a constant

- **Location.** `sections/A-composition.tex:100-101` (Appendix A.4, p. 47).
- **Issue.** Proposition 3.5(ii) re-splits with alpha_i y + gamma_i y^2 only. The example uses
  +-(1/2)(y - 3/2)^2, which also contains the constants +-9/8. These cancel and leave Delta'
  unchanged, so the conclusion stands, but the example lies formally outside the stated form.
- **Fix.** Either append "(the constants $\pm\tfrac98$ cancel and do not change $\Delta'$)", or write
  the re-splitting as

  > $q_1+\tfrac12y^2-\tfrac32y$ and $q_2-\tfrac12y^2+\tfrac32y$, with pair minima $-\tfrac38$ and
  > $\tfrac78$

  These values were verified: 3/4 - 9/8 = -3/8 and -1/4 + 9/8 = 7/8, with sum 1/2 = beta*.

### F7 [suggestion] Section 2: SCIP recognizes concavity syntactically

- **Location.** `sections/02-setting.tex:162-167` (Section 2.1, p. 6).
- **Issue.** The description is correct:
  - The conditions are finite bounds, no objective coefficient, a single constraint, and concave
    with an infinite left-hand side (convex with an infinite right-hand side).
  - The result is binary for bounds [0,1], and otherwise a bound disjunction. This matches the
    SCIP 8 report Section 4.2.7, Bestuzheva et al. 2025 Section 2.2.1, and the SCIP 10.0.3 source
    (`cons_nonlinear.c`, `isSingleLockedCand`, `presolveSingleLockedVars`). With the default
    `checkvarlocks = 't'`, SCIP makes [0,1] variables binary and adds a bound disjunction for other
    finite bounds. The round-2 writing note W16, which says the disjunction needs the non-default
    `'b'`, is mistaken.

  However, SCIP tests concavity only syntactically. The constraint must be a sum whose terms
  contain the variable only linearly in products or in even powers x^{2k} with a coefficient of
  the right sign. The text can be read as saying that SCIP detects every polynomial that is
  concave in the variable. For the path family the syntactic condition holds: x_i occurs in x_i^2
  with a negative coefficient and linearly in x_i y_i and x_i.
- **Fix (optional).** After "concave (convex) in it" insert "in a form that SCIP recognizes (the
  variable occurs only linearly or in even powers whose coefficients have the right sign)".

## Items verified, no change needed

- **(a) Section 3.4, new paragraph.** All numbers were reproduced; see A1-A4 and B above. The
  references to BNW Example 4 and Section 6.4 are accurate. The phrase "which we verified exactly"
  is accurate, because the exactness concerns the feasibility of the rational points, which are
  upper bounds. The claim "for r=1 it attains 1/2, as the theorem above predicts" is rigorous:
  - the identity (eq:sdp-identity) with A = {0,2}, C = {1,3}, omega = 4 gives the lower bound 1/2
    on the dense relaxation, and every term is nonnegative there;
  - complementing x and z makes the instance submodular, so BNW Theorem 1 applies.

  The wording issues are in F2 and F3.
- **(b) Two-leaf strong NP-hardness (Section 4.2).** Correct; see part C and F4 for wording.
- **(c) Block closure (Section 8.5).**
  - Each block (x_i, y_i, z_i) has the single nonlinear row Phi^(i) - t_i <= 0.
  - The domain is [0,1]^3: the coupling row involves other blocks, so it is not in D, and
    c >= 87/64 > 1 on all 20 instances, so it implies y_i <= c with no tightening.
  - Corollary 5.3 gives t_i >= vex Phi^(i).
  - Partial minimization commutes with convexification: the projection of conv(epi Phi^(i)) onto
    (y, t) is conv(epi d_i). conv(epi Phi^(i)) is closed, because it equals the compact
    conv(graph) plus a ray.
  - d_i = dist(y,A_i)^2 + dist(y,C_i)^2, because omega = 1 >= (a_2 - a_1)^2.
  - Equality with the Lagrangian dual of the coupling row holds by convex duality; y = 0 is a
    Slater point since c > 0.
  - The stated accuracy holds: the largest upper-minus-lower bracket is 1.26e-28 <= 2e-28.
  - The closure equals the optimum on 13 of 20 instances and lies at most 6.47e-4 below it on the
    others, as stated.
- **(d) Glued bound 0 with the coupling row.** For every copy of seeds 0-9 the chord crossing lies
  strictly inside both chords, with largest m_y = 129/176 = 0.733 <= 3/4. Hence
  sum_i m_{y_i} <= 0.75n < 0.8n, and the zero points of all copies together are feasible for the
  glued relaxation of the instance.
- **(e) Proposition 3.5(ii) attribution and Appendix A.4.**
  - Lagrangian decomposition with the moment coordinates (m_y, s_y) as copied variables is exactly
    the duality in the proof (Sion's theorem on the compact product of pair hulls). The reading
    "best split with an interface polynomial of degree two in y" matches (ii).
  - Example 1: Delta = 1/2, and Delta' = 0 for the stated re-splitting, which equals
    -p, +p with the nested-case polynomial p of Appendix A.1 (gamma = 1/2, t_0 = 3/2).
  - Example 2: the projections meet pairwise in {1}, {0} and {2} but have no common point, and
    Delta = 2/3.
  - The unstated weights omega do not matter, because only omega >= (a_2 - a_1)^2 is used. See F6
    for the constant.
- **(f) Section 5.3 and Appendix D.** Statements and labels are consistent; see F5 for the
  duplication.
- **(g) Shapley-Folkman.** "At most twice the largest nonconvexity" is a correct reading of
  Aubin-Ekeland for one coupling constraint, but it is not tight and does not explain the
  observations (F1).
- **(h) Section 2, implicit discreteness.** Correct as written; see F7 for an optional precision.

## Not used by this lens

`experiments/v5/runs/replay-partS5.log` was empty when this lens started (size 0, modified
2026-10-03 23:24). As instructed, I polled it every 60 s from 2026-10-03 23:59:52 to
2026-10-04 01:00:12. It was still empty at the end, and the replay process
(`replay_v5.py runs/partS5`, PID 169873) was still running. No check in this report depends on
the replay results.
