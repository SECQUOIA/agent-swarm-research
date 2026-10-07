# W4 review M-recourse: mathematics of Section 7 and Appendices C, D

Scope: `sections/recourse.tex`, `recourse-valuefn.tex`, `recourse-local.tex`,
`recourse-convex.tex`, `recourse-cuts.tex`, `recourse-mixed.tex`,
`recourse-balanced.tex`, `appendix-recourse-convex.tex`,
`appendix-recourse-cuts.tex`, with the results of Sections 3-6 that they cite
(Def 3.1/3.2, Prop 4.2, Lemma 4.3, Prop 4.5, Thm 4.7, Lemmas 5.4/5.5,
Thm 5.9, Lemma 6.3, Cor 6.4, Prop 6.6, Lemma 6.8, Thm 6.9, Thm 6.14). Numbers below follow
`/tmp/dpaper/out/main.aux` (Section 7 is pp. 31-44, App. C pp. 101-108,
App. D pp. 109-111).

## Verdict

I re-derived every statement and proof in the assigned files and found no
error that invalidates a theorem, lemma or proposition. The proofs of Lemma
7.1, Theorems 7.2, 7.4, 7.10, 7.12, 7.17, 7.20, 7.26, Lemmas 7.3, 7.8, 7.25,
C.5, D.1, Propositions 7.5, 7.9, 7.13, 7.16, 7.21, C.1, C.3, D.3, D.4,
Corollaries C.7, C.8, 7.27 and Theorem D.2 are complete and correct. The
examples (7.22, C.2, C.9, C.10, C.11) are numerically right. Exact-arithmetic
checks (below) confirm all formulas of Proposition 7.5, Example C.9,
Proposition 7.13 and the ladder C.10, and confirm on random instances the cut
identity, the threshold-encoded minimum cut, CORE's invariants, the height
bound of Lemma D.1, the exact-output pipeline of Theorem D.2 and the
submodularity of D.3(c). The remaining problems are five minor ones: three
sentences that overstate what is proved (a subsection title, a remark in
7.1, and the comparison in Theorem 7.10(iv)), a missing remark on
termination of the exact procedure of Theorem 7.10(iii) without growth, and
an imprecise robustness sentence in Theorem 7.17. The earlier w2 findings on
these files (R2 M1-M5, m1-m19) are fixed in the current text.

## Findings

### M-recourse-1 (minor) Theorem 7.10(iv): the comparison holds only for the Euclidean condition number

Location: `sections/recourse-convex.tex:207-209` (statement (iv)), with
`:197-206` (iii) and `sections/recourse-valuefn.tex:85-91` (Thm 7.2(b)).

Problem. (iv) says "Thus the parameter never exceeds the one obtained by
keeping the private variables as ordinary coordinates." The proof
(`:249-252`) compares the Euclidean numbers kappa(L^+, g_V) and
kappa(L_F, g_F). But the approximation theorem for the problem with the
private variables kept (Theorem 5.9(b)) is stated with the weighted number
kappa-bar, which can be much smaller than kappa. Theorems 7.2(b) and 7.10(iii)
use only the Euclidean kappa_V.

Counterexample to the broader reading. Take no private block (r = 0), or a
block that does not couple, and F_0(v) = 100 v_1^2 + v_2^2 on [-1,1]^2.
Then L^+ = 200, g = 1, kappa_V = 200, so Theorem 7.10(iii) gives
f(p,200) 200^C (I+q+1)^C. The same problem has weighted growth with
gamma = 1/2 (F = (1/2)(200 v_1^2 + 2 v_2^2)), so kappa-bar = 2 and Theorem
5.9(b) gives f(p,2)(I+q+1)^5. So "the parameter never exceeds" is false if
"the parameter" means the parameter of the respective approximation theorem.

The stronger statement is true and costs one line. Weighted growth is
inherited: if F - OPT >= gamma sum_{i in P} L_i^F (x_i - x_i^*)^2 and
L_i^+ <= max{(H_0)_ii, 0} = L_i^F for i in K (Theorem 7.10(iv)), then
V(v) - OPT = F(v, y(v)) - OPT >= gamma sum_{i in K} L_i^+ (v_i - v_i^*)^2,
so kappa-bar_V <= kappa-bar_F. Appendix C.1(b) uses only weighted growth of
V (it first converts point growth to weighted growth), so Theorem 7.2(b)
holds verbatim with kappa-bar_V in place of kappa_V.

Fix (minimal). Replace the second sentence of (iv) by: "Thus
kappa(L^+, g) never exceeds the Euclidean condition number kappa(L, g) of F
with the private variables kept as ordinary coordinates." Optional
strengthening: state Theorem 7.2(b) and Theorem 7.10(iii) under weighted
growth of V with kappa-bar_V, and add to (iv): "and V inherits weighted
growth from F with kappa-bar_V <= kappa-bar_F, because L_i^+ <= L_i^F."

### M-recourse-2 (minor) Section 7.1 overstates what Section 7.3 achieves

Location: `sections/recourse-valuefn.tex:48-50`: "Section 7.3 evaluates V
exactly and bounds its curvature by quantities that do not see such stiff
convex terms".

Problem. The certified curvature can contain the full stiffness. Remark C.11
(M(y-w)^2 + eps y: sigma = 0, L_v = 2M for every eps > 0) and Proposition
7.13 (L_K/g_K >= M for every admissible K) show this. The sentence
contradicts the paper's own limits.

Fix: "Section 7.3 evaluates V exactly and certifies curvature bounds that can
cancel such stiff convex terms (Theorem 7.10), though not always
(Proposition 7.13);". (Optionally also `recourse-convex.tex:5-6`: "depends
only on the coordinate curvature of the reduced objective" -> "depends only
on the coordinate curvature and the growth of the reduced objective".)

### M-recourse-3 (minor) Title of Section 7.2 claims a necessity that is not proved

Location: `sections/recourse-local.tex:1`: "Local corrections need exact
recourse".

Problem. Theorem 7.4 shows that a bag-local allowance is valid with exact or
certified approximate recourse (eps_or > 0 is allowed), and Proposition C.1
even allows uncertified values with small error oscillation. Proposition 7.5
refutes one alternative only: grid min-marginals with a constant allowance.
No result shows that exact recourse is necessary. The w2 review (R2 m8)
removed the same necessity claim from the body text; the title still makes
it.

Fix: "Bag-local corrections and conditional recourse" (or "Local corrections
with exact or certified recourse").

### M-recourse-4 (minor) Exact output of Theorem 7.10(iii): termination without growth is not available and not stated

Location: `sections/recourse-convex.tex:202-206`;
`sections/appendix-recourse-convex.tex:359-369`.

Problem. The exact procedure of Theorem 7.10(iii) reconstructs each
continuous retained coordinate of the CT incumbent with denominator at most
Lambda_0. Without uniqueness this need not ever succeed: the incumbents may
approach a continuum of minimizers whose points have larger denominators, and
REC is not available because the slices are polytopes (w3 F67). So the
procedure has no termination guarantee without point growth. Theorem 6.14
(EX) and Theorem 7.2(c) do guarantee termination on every instance, and the
results table (`intro.tex:331-334`) lists Theorem 7.10 next to them, so a
reader may assume the same. The theorem itself is not wrong: it claims a
bound only under growth and validity without growth.

Fix: add to (iii) after "valid without growth or uniqueness": "Without point
growth of F the exact procedure is not guaranteed to stop; if every Y_t is a
box, Theorem 7.2(c) applies instead and EX stops on every instance."

### M-recourse-5 (minor) Theorem 7.17, last sentence: the subbox must keep integer endpoints

Location: `sections/recourse-cuts.tex:113-115`: "The same holds after the
residual box is replaced by a rational subbox, ...".

Problem. Lemma 7.15, on which the oracle rests, needs integer bounds for
integer residual coordinates. With a rational subbox such as [0, 1/2] for an
integer coordinate, the cut returns the endpoint 1/2, which is infeasible.
The sentence is also not used anywhere in the paper (`grep "rational
subbox"` finds only this line).

Fix: "by a rational subbox whose bounds are integers for integer
coordinates", or delete the sentence.

## Checked and found correct

* Lemma 7.1: (a) infimum of concave functions; finiteness from compactness
  and continuity; (b) V(v*) = OPT and the one-line growth transfer.
* Theorem 7.2 and App. C.1: (a) only Def 3.1, exact values and growth are
  used. (b) The operation count c(J+1)pI^2(60p sqrt(kappa_V))^p,
  J = O(P_L(I)+q), node length c(1+mu 2^mu)(P_L(I)+q+1) with
  1+mu 2^mu <= c' kappa_V for mu <= mu*, per-operation cost
  (c'' kappa_V (I+q+1))^{C'}; the exponents C and C_1 depend only on P and
  P_L, and constants are absorbed using I+q+1 >= 2. (c) Termination via
  Thm 6.9(b) applied to F at the lifted incumbent; bound via Thm 6.9(a) with
  q <= poly(I) + O(log kappa_V) from g >= L^V/kappa_V; the case L^V = 0.
* Lemma 7.3 (application of Prop 4.2(a) to V_B on one cell, integer
  coordinates with effective width 0) and Theorem 7.4(a)-(c), every
  inequality, including U <= F(x^{v°}) <= V_B(v°) + eps_or <= OPT + e +
  eps_or, the multilevel paragraph (lines 67-73) and Proposition C.1 with
  unknown delta_-, delta_+.
* Proposition 7.5 and its proof: (A) V(x) = (1 - mh^2/4)x^2 + omega_A x,
  unique minimizer, growth bound, U_G = 0, corner values
  (1-h)(mh^2/4-h-eps), +h^3, mh^2/4 - eps, the difference
  h(mh^2/4-eps)+h(1-h), the ratio limit (1-h)^{-1}; (B) Hessian, eigenvalues
  3 +- sqrt5 on span{e_x, m^{-1/2} 1}, g = (3-sqrt5)/2, kappa = 2(3+sqrt5),
  V^G(t) = 2t^2 - dh|t| + d^2h^2/4, U_G, the corner gaps and the lower bound
  dh/4 + 2h^2 - 1/2 for h <= 1/4. Example C.2 values 23/32, 27/32, 31/16,
  budgets 1/8 and 33/16, grid error m dist(x/4,G)^2.
* Definition 7.7 (BSP certificates) and the checking paragraph (Farkas form
  of affine inequalities on a polytope verified by LP duality).
* Lemma 7.8: the KKT identity (a); (b) G_s B = 0 on the support of lambda by
  the integral-domain argument, B^T Gamma = -B^T C B, Hessian -B^T C B.
  Formula (C.1) (eq:cv-energy) re-derived.
* Proposition 7.9 (a)-(c) and the appendix proof of (b) (covering of J by
  nondegenerate leaf intervals, jump of chi' equals jump of psi').
* Theorem 7.10 (i)-(iv): concavity along coordinate segments with possibly
  negative L_i, passage to L_i^+, endpoint DP for L^+ = 0, use of Thm 7.2,
  exact-output appendix proof (slices, Lemma C.5, continued fractions with
  1/(4 Lambda_0^2), threshold min{1/(2 Omega_0^2), g/(32 Lambda_0^4)}).
* Lemma C.5 (no uniqueness): maximal active set, the line argument that
  excludes d in W with Hd perp W, positive definiteness on W, nonsingular
  saddle matrix, row Hadamard bound (sqrt(2n') beta_H)^{2n'}, Cramer, value
  denominator 2 Delta Lambda_0^2.
* Theorem 7.12 and its proof: common central gradient, necessity for
  I_ell, I_u, I_0 (including the case "identically at a bound"),
  sufficiency via explicit multipliers, linearity of the Farkas system in
  (y_0, B, pi), the two examples after the proof.
* Proposition C.3 (KKT pattern polyhedra, triangulation, BSP refinement by
  facet hyperplanes, connectedness argument), Lemma C.4, Lemma C.6,
  Corollary C.7 (H_red = J^T Hess F J, rescaling), Corollary C.8 (halving
  test, eigenvalue lower bound Delta_H^{-d} nu0^{1-d}).
* Example C.9 (three pieces, KKT signs, B^T C B = 2M, 2M+8,
  2(M+2)^2/(M+1), piece second derivatives 8, 0, 2M/(M+1)); Proposition
  C.10 (expansion t^2 + M rho_1^2 + rho_2^2 + alpha_1/5, growth 1/12,
  inertia exactly m, 2 <= nu <= sqrt5, L^+ <= 41/4, g <= 33/16, ratio 123);
  Remark C.11.
* Proposition 7.13 and its proof: SOS bound with remainder xi_2^2/16,
  eigenvalues 4M and -1/2, admissible sets, y_c and x_c and the clipped
  pieces, F_M(2,2) = 3/2, rescaling argument, (4M - 1/2)/3 >= M.
* Lemma 7.14, Lemma 7.15, Proposition 7.16 (a) and (b), Theorem 7.17
  (weak duality certificate, Edmonds-Karp bit lengths).
* CORE (Algorithm 7.19), Theorem 7.20 (a)-(d), the stopping remark,
  Proposition 7.21 (|Q_j'| <= 2^k N_j, 8^k N_j queries, coordinate radius
  (h_j/2) sqrt(k kappa_K)), Example 7.22 (2^{jk/2} retained cells,
  U - lambda_j = e_j, Omega(eps^{-k/4}) queries).
* Lemma D.1 (Delta_K = Lambda_c Lambda_e^2 clears all coefficients of F_y,
  Omega_K independent of y, O(kI) bits) and Theorem D.2 (face enumeration
  contains the vertex of the stationary polytope, acceptance, J = O(I^2),
  complexity 8^k(1+sqrt(k kappa_K))^k poly(I)).
* Remark 7.23, Propositions D.3 and D.4 (lattice submodularity of the
  transformed quadratic, greedy vectors, Edmonds, LP and its dual,
  r_i = max{0, -abar_i}, basic solutions with <= m+1 orderings, checker).
* Lemma 7.25 and its proof (threshold encoding, bijection with
  nonincreasing vectors, pair coefficients H_ij delta delta <= 0, infinite
  arcs, arc count 3 sum k_i + 2 sum k_i k_j), Theorem 7.26 (a), (b) and the
  App. D.3 count (1 + nK_mu cuts per stage, nK_mu + 2 nodes,
  3nK_mu + n^2 K_mu^2 arcs, denominators), Corollary 7.27.
* Claims about Section 7 in the abstract, the introduction (lines 219-245)
  and the results table (lines 323-342) match the theorems, apart from the
  reading of Theorem 7.10 discussed in M-recourse-1.

## Checks run (targeted, exact arithmetic)

* `python3 -B process/w4/checks/M-recourse-local-convex.py` (new): ALL PASS
  (25 checks). Proposition 7.5(A) for (j,m,eps) in {(1,32,1/16),
  (1,17,1/32), (2,80,1/7), (3,400,1/3), (2,1000,1/2)}; 7.5(B) for
  (j,d) in {(2,8),(2,9),(2,20),(3,16),(3,40),(4,32)}; Example C.9 for
  M = 1, 3, 10 at 76 points each (KKT enumeration); Proposition 7.13 for
  M = 1, 2, 7 (growth on a 41x41 grid, clipped responses); Proposition C.10
  for m = 1, 2, 3, M = 1, 5 (OPT = m/20, growth 1/12 at 300 random points).
* `python3 -B process/w4/checks/M-recourse-cuts.py` (new): ALL PASS.
  Proposition 7.16(a) identity on all labels and max flow = min Phi (200
  random instances); Lemma 7.25 cut value and decoded minimizer = brute force
  and arc bound (150 random balanced quadratics with random grids and unary
  terms); Lemma D.1 denominators <= Omega_K (60 random cut-class instances,
  k = 1, 2, mixed residual); Theorem 7.20(b), (c) at every level and (d) at
  200 random feasible points per instance; Theorem D.2 pipeline with
  eps = Omega_K^{-2}/2 (23 instances where J is small enough); Proposition
  D.3(c) with a convex continuous part (150 instances).
* `python3 -B process/w3/checks/recA-cv-height.py` (rerun): PASS (3944
  instances, 1061 with several minimizers) for Lemma C.5.

No project-wide verification was run; CI was not consulted. No file in
`sections/`, `main.tex`, `macros.tex` or `references.bib` was edited.
