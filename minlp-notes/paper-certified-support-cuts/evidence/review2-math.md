# Review round 2: mathematical correctness (lens R9-math)

Scope: every theorem, proposition, lemma, corollary, example and remark of Sections 2-6 and
Appendices A-E, re-derived line by line, plus the mathematical statements that Sections 7-8 use
(the path family, the glued pair-hull level, the block-closure bound of Part C4, budget arithmetic).
Page numbers refer to `development/draft-round2/main.pdf` (via `main.txt`, form-feed pages).

## Summary

No error was found that invalidates a theorem, proposition, example or headline claim. All exact
data in Sections 3-5 and the appendices were recomputed and are correct: the witness, the minimum
1/128, its unique minimizer and the cut of Proposition 3.1; the identity (7); the kappa = 3 measures
and the value 6103/16128; the binomial weights of Proposition 3.4; the re-splitting minima 3/4 and
-1/4 and Delta = 2/3 after Proposition 3.5; the envelope value -1/4 of Example 5.4; Example 5.7 and
the D = [0, 2] example; the Ben-Or tent identity; and the depth-two example of Remark 4.5. Exact LP
tests of Theorems 3.2(ii) and 3.3 found no mismatch, and the polynomials of Appendix C.1 were checked
exactly. The proofs of Theorems 4.1, 4.4, 5.2 and E.2, Propositions 3.5, 5.6 and 6.1, Lemmas E.1
and E.3, the ellipsoid variant, the encoding-length bounds of Appendices A and B, the coNP and
strong NP-hardness arguments, and the lower-bound reduction are correct as written. (A few
inequalities in Appendix B are loose, which is harmless.)

What a referee would still require:

- one **major** change: the introduction, Section 3.4 and the conclusions turn a three-variable
  result into a general claim about joint blocks. The claim is false for four-variable paths, which
  are inside the paper's own block class.
- several **minor** changes: an incomplete derivation of the Part C4 reference bound; a missing check
  of the coupling row for the glued pair-hull level; a hardness example that does not match the
  excluded class; an incomplete description of the implemented star oracle; necessity claims that
  the data contradict; and notation clashes.

---

## Findings

### M1 [major] "Representation, not strength" is proved only for three-variable paths, but stated for joint blocks in general

*Location.* `sections/01-introduction.tex:56-62` (contribution 1, p. 2);
`sections/03-composition.tex:287` and `:321-323` (Section 3.4, pp. 9-10);
`sections/09-conclusions.tex:6-13` (Section 9, p. 31).

*Issue.* Section 3.4 proves, correctly and through Burer-Natarajan-Willemsen (BNW) Theorem 1
(n <= 3), that on a three-variable path over a box the dense Shor relaxation with all McCormick
inequalities is exact. Three passages state more than this:
- introduction: "the advantage of joint blocks over their pairs is therefore one of representation";
- Section 3.4, first sentence of the paragraph: "The advantage of the joint block over its pairs does
  not extend to dense relaxations.";
- conclusions: "Second, the advantage of joint quadratic blocks over their pairs is one of
  representation. ... dense moment relaxations with products that are absent from the model close
  the same gaps".

BNW Theorem 1 holds only for n <= 3 (their full text, Theorem 1 and Example 4). Their
counterexample for n = 4 has a tridiagonal Hessian, so it is a **four-variable path**. A
four-variable box block lies within the separator's limits: four variables, quadratic, and
1 + 8 + 28 + 56 + 70 = 163 row subsets against the budget of 2,000 in Section 7.2. So the paper's
own oracle certifies the exact support cut of this block.

*Evidence.* `verification/R9_math_bnw_path4.py`, with Q = tridiag (diagonal 8, 25, 25, 8;
off-diagonals -14, -25, -14) and c = (12, 29, 0, 0) on [0,1]^4:
- exact minimum 0, attained only at x = 0 (face enumeration of Theorem 4.1 in rationals);
- dense SDP with McCormick inequalities on all 10 products and squares: -0.1220566;
- the same plus all triangle inequalities: -0.0001432;
- glued exact edge hulls (SDP + RLT per edge, exact on a 2-D box): -1.4544316;
- lin f at the dense optimum, which uses only x_i, x_i^2 and x_i x_{i+1}: -0.1220566.

So the single exact support cut lin f >= 0 of the four-variable block cuts off the dense optimum
by 0.122. The joint block is strictly stronger than the dense relaxation with all products. This
was found independently by the referee lens (`review2-referee.md`, F1), and this run confirms it.

*Fix.*
- Introduction: replace "A dense semidefinite relaxation ... the coordinates that the model already
  has." with: "On a three-variable path over a box, a dense semidefinite relaxation with the
  McCormick inequalities of the missing product is exact for every quadratic objective, by a theorem
  of \citet{BurerNatarajanWillemsen2025}; there the advantage of the joint block over its pairs is
  one of representation, which support cuts obtain in the coordinates that the model already has.
  On four-variable paths the dense relaxation is no longer exact, and the joint block is strictly
  stronger."
- Section 3.4, line 287: "On a three-variable path, the advantage of the joint block over its pairs
  does not extend to dense relaxations."
- Section 3.4, after line 323, add: "For four variables this fails: on the path of
  \citet[Example~4]{BurerNatarajanWillemsen2025} over $[0,1]^4$ the minimum is $0$, the dense
  relaxation with the McCormick inequalities of all products has value about $-0.122$, and the
  exact support cut of the four-variable block closes the gap."
- Conclusions: "Second, on three-variable paths the advantage of joint quadratic blocks over their
  pairs is one of representation: ... dense moment relaxations with the missing product close these
  gaps, and support cuts obtain the same strength in the model's own coordinates. For larger blocks
  the joint hull can be strictly stronger than such relaxations, as on the four-variable path of
  \citet[Example~4]{BurerNatarajanWillemsen2025}."

### M2 [minor] Part C4: the characterization of the best block-cut bound skips a step and leaves its premises implicit

*Location.* `sections/08e-path.tex:102-109` (Section 8.5, p. 28) and `:220-223` (p. 30);
`sections/B-tables.tex:171` (Table 12 caption, p. 55).

*Issue.* The text says that the best root bound obtainable from cuts on the blocks
"by Theorem 5.2 and Corollary 5.3 is min{sum_i vex phi_i(y_i) : sum_i y_i <= c, 0 <= y <= 1}".
Corollary 5.3 gives, for each block, the closure t_i >= vex Phi^(i)(x_i, y_i, z_i) over [0,1]^3. It
does not give the one-dimensional formula. Four points are missing.
1. *Partial minimization.* The formula needs
   min_{x,z} vex_{[0,1]^3} Phi^(i)(x,y,z) = vex_{[0,1]} phi_i(y), with phi_i = min_{x,z} Phi^(i).
   This holds because the projection of conv(epi Phi^(i)) onto (y, t) is the convex hull of the
   projection, but the paper does not say so.
2. *Block domain.* The block domain must be [0,1]^3. This holds because the coupling row involves
   other blocks and, since c >= 1 on all 20 instances, the bound step of Section 7.1 does not tighten
   y_i <= 1. If c < 1, the domain would shrink and the bound would change.
3. *Linear rows.* Combining the coupling row into aggregated cuts adds nothing (Section 5.1). This
   should be said.
4. *Wording.* "best root bound that cuts on the blocks can give" refers to the closure of the block
   cuts together with the linear rows, not to SCIP's whole root LP. Table 12 also uses
   "bound (ii)", a label that the text never defines.

The bound also equals the Lagrangian dual of the coupling row,
max_{mu >= 0} sum_i min_{0<=y<=1} (phi_i(y) + mu y) - mu c. This form is easier to state and to
check, and it explains why the bound is so often tight (one coupling row).

*Evidence.* `verification/R9_math_indep.py`, part N, computes the Lagrangian dual independently,
with exact rationals and a rigorous bracket (bisection on the supergradient, rational kink
candidates and tangent-line upper bound). For all 20 C4 instances it agrees with
`experiments/v4/c4-references.json`. Results:
- equality with the optimum on 13 of 20: the optimum lies in the bracket, and h at the archived
  exact multiplier equals the optimum exactly;
- largest optimum - (ii) = 6.473e-4;
- c >= 1 on every instance;
- an independent exact branch and bound (Lagrangian bounds, branching on the choice of nearest
  pair) certifies the archived optima to 1e-20 (72 nodes in total).

`verification/R9_math_checks.py`, part G, checks the partial-minimization identity by LP on one copy
(max difference 2.3e-16). So the stated values are right; only the argument is incomplete.

*Fix.* Replace 08e-path.tex:103-109 ("and the best root bound that cuts ... functions
$\varphi_i$.") with:

"and the bound (ii) of the block closure, that is, of all aggregated cuts on the blocks
$(x_i,y_i,z_i)$ together with the linear rows. Each block has the single nonlinear row
$\Phi^{(i)}-t_i\le0$ and the domain $[0,1]^3$: the coupling row involves other blocks, and since
$c\ge1$ it implies no tighter bounds. By Theorem~\ref{thm:closure} and Corollary~\ref{cor:one-row}
its closure is $t_i\ge\operatorname{vex}\Phi^{(i)}(x_i,y_i,z_i)$. Minimizing over $x_i$ and $z_i$
commutes with convexification, because the projection of a convex hull is the convex hull of the
projection. With $\varphi_i(y)=\min_{x,z\in[0,1]}\Phi^{(i)}(x,y,z)=\dist(y,A_i)^2+\dist(y,C_i)^2$
this gives (ii) $=\min\{\sum_i\operatorname{vex}\varphi_i(y_i):\sum_iy_i\le c,\ 0\le y\le1\}$,
which is also the Lagrangian dual bound
$\max_{\mu\ge0}\sum_i\min_{0\le y\le1}(\varphi_i(y)+\mu y)-\mu c$ of the coupling row. We computed
it with exact convex envelopes and a rational bisection on $\mu$, to within $10^{-28}$."

At :220-221, replace "the best root bound that cuts on the blocks can give" with "the block-closure
bound (ii)". In the Table 12 caption, write "opt.$-$(ii): optimum minus the block-closure bound (ii)
of Section~\ref{sec:mechanism}".

### M3 [minor] "Glued exact pair hulls give the bound 0" also needs the coupling row to hold at the zero points

*Location.* `sections/08e-path.tex:85-87` (p. 28); Table 5, row "glued pair hulls", and its caption,
`:121-122` (p. 29).

*Issue.* Theorem 3.2 gives the glued bound 0 for each copy on its own. The instance also has the
coupling row sum_i y_i <= 0.8n, and the glued relaxation of the instance must satisfy it, with
m_{y_i} in place of y_i. The bound 0 holds because each zero point has m_{y_i} at the crossing of the
two chords, which lies between the points of A_i, so m_{y_i} <= 3/4. The paper does not say this.
Table 5 then reports "glued pair hulls" as "the analytic bound 0 of Theorem 3.2", which is the
instance bound only with this extra step.

*Evidence.* `verification/R9_math_checks.py`, part F: for all copies of seeds 0-9 and all n, the
chord intersection is interior to both chords, the largest m_y is 129/176, and
sum_i m_{y_i} <= 0.8n on all 40 instances.

*Fix.* At :85-87 write: "Glued exact pair hulls give the bound $0$ for every copy: the chords of
$A_i$ and $C_i$ cross at a point with $m_{y_i}\le\max A_i\le3/4$, so the zero points of all copies
together satisfy the coupling row, and the part of the gap that only the joint block closes is the
whole optimum."

### M4 [minor] The hardness example does not match the excluded class "rows that couple two leaves"

*Location.* `sections/04-quadratic.tex:108-112` (Section 4.2, p. 13).

*Issue.* The text excludes "rows that couple two leaves" and justifies this with
min sum_i x_i(1-x_i) subject to sum_i a_i x_i = b. That row couples *all* leaves, and subset sum is
only weakly NP-hard. The example therefore does not show that rows involving two leaves make the
problem hard. They do, even in the strong sense.

*Evidence.* `verification/R9_math_twoleaf.py`. For a graph G on n >= 3 vertices,
min sum_i (n x_i(1-x_i) - x_i) subject to x_i + x_j <= 1 (ij in E), 0 <= x <= 1, equals -alpha(G).
- The objective is concave, so a vertex is optimal.
- Vertices of the fractional stable-set polytope are half-integral.
- At a vertex with h halves and ones on a stable set O, the value is -|O| + h(n/4 - 1/2), which
  is > -alpha(G) if h >= 1.

The script checks this exactly on C5 (-2), the Petersen graph (-4) and 25 random graphs with
n <= 9.

*Fix.* "Rows that involve two or more leaves are excluded, because with them the problem is
strongly NP-hard already without a center and with two leaves per row: for a graph $G$ on $n\ge3$
vertices, $\min\sum_i(nx_i(1-x_i)-x_i)$ over $0\le x\le1$ and $x_i+x_j\le1$ ($ij\in E$) equals minus
the stability number of $G$, because the objective is concave and the vertices of this polytope are
half-integral \citep{NemhauserTrotter1974}; a single row over all leaves gives subset sum
\citep{Karp1972}, compare \citet{MoreVavasis1990}." (Add the Nemhauser-Trotter 1974 or Balinski
1965 reference.)

### M5 [minor] The implemented star oracle is described incompletely, and Section 7.2 attributes it to Theorem 4.4

*Location.* `sections/04-quadratic.tex:233-236` (p. 14); `sections/07-implementation.tex:110-113`
(Section 7.2, p. 22).

*Issue.*
- Section 4.2 says the implemented oracle "splits the center interval at all pairwise intersections
  of each leaf's bound lines and recomputes every leaf rule on every piece". Read literally, this is
  not a valid oracle. A convex leaf whose unconstrained minimizer v_i crosses L_i or U_i inside such
  a piece has the non-affine rule clip(v_i, L_i, U_i) there. That contradicts the certificate format
  ("the affine rule of every leaf on every piece").
- The code also splits each piece where v_i meets the active bound (convex leaves) and where
  alpha_i(L_i + U_i) + beta_i y + gamma_i changes sign (concave leaves). So the code is correct and
  the text is not.
- Section 7.2 says "only the star oracle of Theorem 4.4 can apply". The separator uses the simpler
  oracle, not the sweep of Theorem 4.4.

*Evidence.* `experiments/v4/snapshot/research-20261002-convexification/theory/quadratic_star.py`,
`_leaf_breakpoints` (lines 97-116) and `support_star` (lines 166-230).

*Fix.*
- 04-quadratic.tex:234-236: "it splits the center interval at all pairwise intersections of each
  leaf's bound lines and, inside each resulting interval, at the points where the unconstrained
  minimizer of a convex leaf meets a bound or a concave leaf changes its preferred endpoint, and
  then recomputes every leaf rule on every piece."
- 07-implementation.tex:110-111: "Otherwise only the star oracle can apply (the simpler
  implementation described at the end of Section~\ref{sec:star}, not the sweep of
  Theorem~\ref{thm:star})".

### M6 [minor] Necessity statements about the whole-row directions contradict the paper's own data

*Location.* `sections/01b-results.tex:14-17` (p. 3); `sections/09-conclusions.tex:30-33` (p. 32).

*Issue.* "showed that the separator closes the gap beyond that level only if it may add enough cuts
per block and tries the exact support of each whole row first", and "They did so only with the exact
support of each whole row as a first direction, enough cuts per block, and ...". These are logical
necessity claims. The data refute them in two ways:
- In C2, remainder directions with wide limits went above the pair-hull level on 7 of 20 instances
  (08e-path.tex:192-193 says so).
- In C4, remainder directions with wide limits closed medians of 0.93-0.98 and solved 20 of 20,
  the same count as the whole-row variant (Table 5).

This is the referee lens's F2. It is repeated here because it is a mathematical (logical)
misstatement.

*Fix.*
- 01b: "showed that enough cuts per block account for most of the closure, and that trying the exact
  support of each whole row first closes the rest when the coupling row does not bind; with a
  binding coupling row, both direction orders solved all instances."
- Conclusions: "They needed enough cuts per block; with a non-binding coupling row, the exact
  support of each whole row as a first direction closed the last part of the gap, and with a
  binding row the LP direction search found the sloped cuts that did the work."

### M7 [minor] Notation clashes and statement inconsistencies

*Location and fix.*
- **delta.** delta is the distance in Theorem 3.2 and also denotes point masses in the kappa = 3
  example, in the same section (`03-composition.tex:217-218`, p. 8: "nu_A = 57/112 delta_{15/32}
  + ..."). Write "the measure with weights 57/112 and 55/112 at 15/32 and 57/32, ...", or use
  $\mathbb 1_{\{t\}}$ for point masses.
- **kappa.** kappa is the number of shared moments (Section 3.3, Appendix C.2), but kappa_A and
  kappa_C are the constants in the proof of Theorem 3.2 (`03-composition.tex:136-137`, p. 7) and in
  Appendix C.1 (`A-composition.tex:9-10`, p. 42). Rename the constants, e.g. to eta_A and eta_C.
- **alpha and gamma.** Appendix C.2 (`A-composition.tex:44-46`) names the measures alpha and gamma,
  while gamma is a scalar in Appendix C.1 (line 23) and alpha_i, gamma_i are coefficients in
  Sections 3.5 and 4.2. Rename the measures to mu_A and mu_C.
- **s.** In Appendix E, s is the number of vertices in Lemma E.3 and also the box side
  min{tau/rho, 1} in the ellipsoid variant (`A-separation.tex:149`, p. 47). Rename the side, e.g.
  to ell_0.
- **phi.** phi denotes the aggregated support value phi(a, lambda) (Section 5), the conditional leaf
  value phi_i (Section 4.2), the block function phi_i of Section 8.5, and phi_J (Appendix E).
  "vex phi_i" in Section 8.5 is therefore ambiguous. Rename the Section 8.5 function, e.g.
  $d_i(y)=\dist(y,A_i)^2+\dist(y,C_i)^2$.
- **alt.** alt(A, C) is undefined when both sets are empty, which Theorem 3.3 allows (both zero
  sets may be empty); Appendix C.2 assumes nonempty sets. Add "with $\operatorname{alt}=0$ if
  $A\cup C$ has at most one point" to the definition (`03-composition.tex:167-170`).
- **Abstract.** It states $O((m+k)\log(m+k))$ operations (`00-abstract.tex:11-12`), but
  Theorem 4.4 has $O(m_0+(m+k)\log(m+k))$. Add the $m_0$ term or "plus linear time for rows in the
  center alone".
- **Oracle points.** The oracle of Appendix E should return a rational point $p_c\in P\cap\Q^d$
  (`A-separation.tex:51-53`). Theorem E.2 asserts rational points, and the master LP is solved
  exactly.

### M8 [suggestion] "We know two reference values exactly" overstates how the C4 references were computed

*Location.* `sections/08e-path.tex:102-104` (p. 28).

*Issue.* The C4 records were computed as follows:
- bound (ii) by 100 bisection steps, with a multiplier bracket of 3.2e-30 and upper - lower =
  1.6e-29;
- the optimum certified by an "exact branch and bound ... tolerance 1/10^20";
- the reformulation is a "perspective MISOCP (binary per pair (s, t); w^2 <= r b)", not a
  quadratic program.

On these instances (ii) is rational, because no envelope segment from an interval end has an
irrational tangent point (R9_math_checks.py, part G). In general it can be irrational: a swap
between a clipped and an interior arc leads to a quadratic equation in mu.

*Evidence.* `experiments/v4/c4-references.json` (fields `bound_ii`, `optimum_certificate`,
`gurobi.attempts[].formulation`).

*Fix.* "For C4 we know two reference values to within $10^{-20}$: the optimum, from a convex
mixed-integer reformulation (a perspective formulation with one binary variable per choice of
nearest points) solved by Gurobi, re-solved exactly for the returned assignment and certified by an
exact branch and bound; and ..."

### M9 [suggestion] Small precision items in proofs and descriptions

- **Example 5.4.** `05-original.tex:172-174` (p. 17): "whose third moment is 0, not 1/4". The
  closure needs $\E u^3\ge1/4$ (from $-\E u^3\le-v_2$), not equality. Write "whose third moment
  $0$ is smaller than the required $1/4$".
- **Section 3.4.** `03-composition.tex:293-295` (p. 10): "what closes the gap must come from the RLT
  inequalities of the nonedge product $xz$". Within the dense moment relaxation, any closing
  constraint must constrain $p_{xz}$, but other families (for example triangle inequalities) also
  do. Write "must constrain the nonedge product $p_{xz}$, for example through its McCormick
  inequalities".
- **Section 4.2.** `04-quadratic.tex:97-98` (p. 12): "Section 3 shows that the blocks worth merging
  are often stars". Section 3 shows only that a three-variable path, a star with two leaves, can be
  worth merging. Write "The merged blocks of Section~\ref{sec:composition} are stars with two
  leaves; for stars with any number of leaves ...".
- **Section 2.** `02-setting.tex:157-160` (p. 5): SCIP's presolve "fixes a variable ... to one of its
  bounds, and makes it binary when its bounds are [0,1]". The step restricts such a variable to its
  two bound values; it does not fix it, as "makes it binary" in the same sentence shows. Write
  "restricts a variable ... to its bounds (some optimal solution has it at a bound), and makes it
  binary when its bounds are $[0,1]$".

---

## Statements checked and found correct (no change needed)

- **Proposition 2.1** (support description): compactness of $H_D$ and the strict separation step.
- **Proposition 3.1.**
  - Witness moments $(1/2,1/2,1/2,5/16,3/8)$ and $(1/2,4/5,5/16,4/5,1/2)$.
  - Minimum $1/128$, attained only at $(1,11/16,1)$, unique because $\omega>(a_2-a_1)^2$ makes
    $\Phi$ strictly concave in $x$ and $z$.
  - Cut (5): constant term $1/16$, right-hand side $-7/128$, violation $1/128$.
- **Theorem 3.2.**
  - (i): the midpoint argument.
  - (ii): the measure reformulation, the chord criterion, and the separated and nested polynomials
    of Appendix C.1, checked exactly on 800 random rational cases (K) and by LP on 120 cases with
    all four configurations (L, max deviation 5e-14).
  - The touching case gives 0.
  - The reduced Dey-Khajavirad objective is the case $\omega=(a_2-a_1)^2$ and has gap 1/128.
- **Theorem 3.3.**
  - Both directions: divided-difference weights, separating polynomial of degree alt (Appendix C.2).
  - The corollaries for $|A|+|C|\le\kappa+1$ and $=\kappa+2$.
  - LP test on 1,290 random $(A,C,\kappa)$ cases, no mismatch (M).
  - The kappa = 3 example: equal moments of orders 0-3, value $6103/16128$, minimum $1/2$.
- **Proposition 3.4.**
  - $x_j^2$ coefficients cancel; $A$ and $C$ are the even and odd integers.
  - Binomial weights match moments up to $\kappa$ for $\kappa\le14$.
  - The hypothesis $\kappa\le2^{r+1}-2$ is exactly what puts $\kappa+1$ in the $y$-range.
- **Section 3.4.**
  - Chordal completion (graph on $\{1,x,y,z\}$ minus $xz$ is chordal).
  - Identity (7), checked symbolically; $F_{ij}\ge0$.
  - Appendix C.3: uniqueness of $p_{xz}$, the two evaluations, violated McCormick inequality.
  - Complementation reduces every path objective to BNW's submodular case.
- **Proposition 3.5.** (i), and (ii) via Sion with compact product of pair hulls; the nested
  example (3/4, -1/4); the three-leaf example ($\Delta=2/3$).
- **Theorem 4.1 and Appendix A.**
  - Minimal-face argument; nonsingularity of $M_I$; dependent rows.
  - Counterexamples for unbounded $P$ and for the minimal-face choice.
  - Hadamard and Cramer bounds, including the scaling by $2^{-\alpha}$.
  - coNP membership and hardness; MAX CUT coefficients at most $n$.
- **Theorem 4.4 and Appendix B.**
  - Breakpoint counts: $s_i+2$ for convex leaves and $2s_i-3$ for concave leaves, so at most
    $2s_i$ per leaf and $2m+4k+1$ intervals.
  - Continuity of $V$, rationality of candidates, operation count.
  - Height bounds: $12\tau+4$ for breakpoints, $11\tau_i+7$ per leaf, $4C+36\tau+14$ for the
    minimum.
  - Ben-Or reduction: $r!$ components, tent identity, $\min V\ge-1$ iff $z\in W$.
- **Remark 4.5.** Conditional value $\min\{-1/8,-(1-t)^2/4\}$, switch at $1-\sqrt2/2$, $\min f=-3/8$
  at $(1,0,1/2)$.
- **Section 5.**
  - Proposition 5.1; the triangle example (point $(1/2,\dots,1/2)$ violates both inequalities).
  - Theorem 5.2: $K+Q$ closed, $\lambda\ge0$ from finiteness.
  - Corollary 5.3, including the equality case.
  - Product decomposition.
  - Example 5.4: tangent point $-1/2$, value $-1/4$, cut $v_1-v_2\ge0$.
  - Proposition 5.6: the $z_j=z+M^+\rho_j$ construction; Example 5.7.
  - Both inclusions of the hierarchy and the $D=[0,2]$ example.
- **Section 6.** Proposition 6.1 and conditions (C1)-(C4).
- **Appendix D.** Bernstein formula, partition certificate, chord lemma; the alphaBB remark is
  correct.
- **Appendix E.**
  - Lemma E.1: cone reduction, weak and strong duality, Lipschitz bound.
  - Theorem E.2: positive homogeneity forces $\|\bar c\|_\infty=1$; box packing gives
    $2r\lceil2\rho/(\epsilon-\theta)\rceil^{r-1}$; at most $r+1$ points; both outcome guarantees.
  - $\eta$-variant, ellipsoid variant (volume argument with $\epsilon=2\tau+\theta$).
  - Lemma E.3 and the grid fallback ($\theta+\rho/N\le(\epsilon+\theta)/2\le\epsilon$, and the
    within-tolerance certificate).
  - Irrational example.
- **Sections 7-8.**
  - Budget arithmetic: $N(15,4)=1941\le2000<N(16,4)=2517$ and $N(22,3)=1794$; the code counts
    two bound rows per variable.
  - Bound implication from rows, and the Rabinowitsch device.
  - Path family: every optimal $y_i$ is a midpoint $\le3/4$; the optimum is $\sum\delta_i^2/2$;
    each copy contributes $\ge1/8192$.
  - The $n$ cuts $t_i\ge\min\Phi^{(i)}$ give the optimum when the row does not bind.
  - C4: $c$ equals half the sum of the smallest minimizers, rounded down to $1/64$ (e.g. 123/64 for
    n10 s5), so the row binds.
  - $\sum_i\min\varphi_i$ is below SCIP's C4 root bound on 10 of 20 instances, matching "half" (O).

## Checks run (targeted, local; no project-wide tests, no CI, no SCIP or Gurobi solve)

All with `/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python`,
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`.

| Script | Content | Result |
|---|---|---|
| `verification/R9_math_checks.py` | exact checks A-J (Prop. 3.1, kappa=3 example, Prop. 3.4, Prop. 3.5 examples, identity (7), C3 chord intersections and coupling row, C4 Lagrangian value at archived multiplier and partial-minimization LP check, Examples 5.4/5.7 and D=[0,2], budget arithmetic, Ben-Or identity, Remark 4.5) | 25 of 25 pass |
| `verification/R9_math_indep.py` | K: App. C.1 polynomials (exact); L: Thm 3.2(ii) by LP; M: Thm 3.3 by LP; N: independent C4 bound (ii), equality count, max gap, archived optimum feasibility, exact B&B certification; O: "half" claim | 11 of 11 pass |
| `verification/R9_math_bnw_path4.py` | BNW Example 4 (four-variable path): exact minimum, dense SDP + all McCormick, + triangles, glued edge hulls (Clarabel) | values above; PASS |
| `verification/R9_math_twoleaf.py` | stable-set reduction for rows with two leaves (exact, 27 graphs) | PASS |

CI checks were not inspected or duplicated.
