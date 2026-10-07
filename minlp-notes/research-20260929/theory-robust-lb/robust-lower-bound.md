# Split-robust lower bounds for single-tree spatial branch-and-bound on paths

Date: 2026-09-30. Workstream "theory-robust-lb" of the September 29 program.
Status: **reviewed, rechecked and confirmed; revised after each round.** An
independent review ([`../reviews/robust-lb-review.md`](../reviews/robust-lb-review.md))
confirmed the mathematics and asked for one numerical correction, literature
positioning and several sharper statements (Section 10.1). An independent
recheck of that revision
([`../reviews/robust-lb-recheck.md`](../reviews/robust-lb-recheck.md)) found
no mathematical error and asked for one citation fix and several narrower
wordings (Section 10.2). An independent confirmation of the second revision
([`../reviews/recheck-robust-lb-confirm.md`](../reviews/recheck-robust-lb-confirm.md))
found every fix applied and no mathematical error; it found one numerical
range that was wrong for odd degrees and a few wording points (Section 10.3).
The third revision was confirmed by
[`../reviews/robust-lb-confirm-r1.md`](../reviews/robust-lb-confirm-r1.md)
(no remaining problem). Proofs
are complete unless a step is marked "sketch". The constants in Theorem 4.3(2)–(3) and Section 6.5 are
computer-evaluated in double precision on grids (Section 4.3(b)); they are
not interval-certified. The analytic constant in Theorem 4.3(1) needs no
computation beyond arithmetic. Scripts and logs are in this directory
(Section 9).

Cited notes: face-exact note
([`../theory-face-exact/face-exact-exponential.md`](../theory-face-exact/face-exact-exponential.md)),
decomposition note
([`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)),
and the constrained note [C]
([`../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`](../../research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md)).

## Summary

**Question.** The face-exact note (Theorem 2) and the decomposition note
(Corollary 2.1) prove exponential single-tree lower bounds for one fixed way
of splitting the objective into factors. Observation 4.2 of the
decomposition note shows that no lower bound holds for all splits. Is there
an exponential lower bound, on a path-structured problem with a unique
nondegenerate interior minimizer, that holds for every split in a natural
class a modeler or solver could use: (a) weighted splits of the unary terms
plus redistribution of quadratic (and linear) terms, or (b) redistribution
of polynomials of degree at most `d`?

**Answer: yes for both classes, on an explicit family, even if the split is
chosen per node and with knowledge of `x*`. The proved bases are small, the
family is built from three-variable gadgets, and for class (b) the family
must depend on `d`.**

**Significance, stated plainly.** This is a qualitative robustness result.
It shows that no split from a fixed finite-dimensional class, chosen per node
and even with knowledge of `x*`, avoids exponential growth. It has no
practical weight at realistic sizes: the analytic bound gives 1.35 leaves at
`n = 100` and 21 at `n = 1000`, the computed bound needs `n ≈ 275` to reach
`10^6`, and the counting method cannot exceed about 1.063 per variable at the
reference parameters (for class (a), 1.022–1.075 at the 19 other parameter
sets of the scan in Section 6.5). The
family is a direct sum of nearly independent three-variable gadgets joined
by links weaker than `1.4e-3`. The lower bound is a product
effect, not propagation along a path; with the links removed, a solver that
detects independent components avoids it. Lemma 1.2, the tool behind the
result, is known in substance (Section 1.5).

1. **Formalization (Section 1).** On a path every split is a redistribution
   of functions of one variable between the two factors that contain it
   (Lemma 1.1). A split class is a space `S_i` of such functions for each
   interior variable. With per-factor convex envelopes and the best split of
   the class chosen for each box, the node bound equals the minimum of
   `sum_e ∫ f_e dnu_e` over factor measures whose marginals agree on `S_i`
   (Lemma 1.2). Observation 4.2 is the case "all continuous functions":
   the marginals must be equal, and such measures glue on a path. Class (a)
   enforces agreement of `E x_i`, `E x_i^2`, `E u_i(x_i)`; class (b_d)
   agreement of the first `d` moments. Equivalently, the class fixes which
   univariate lifted variables are shared between neighbouring factors.
2. **What does not work (Section 2).**
   - The PROGRAM family (`kappa + |b| <= 1`, no linear terms) is solved at
     the root, with incumbent `f(0) = 0`, by the fixed balanced split with
     exact per-factor envelopes: every factor is nonnegative
     (Proposition 2.1). With the program's random
     linear terms, the balanced split needs 1–17 leaves and class (a) needs
     1 leaf up to `n = 8`. The 2.3–2.5 growth per variable of the review's
     toy runs came from alphaBB, not from the per-factor structure.
   - Near a nondegenerate `x*`, a weighted split makes every factor convex
     (face-exact note, Section 9.2), so any split-robust bound is free of
     `log(1/eps)`.
   - The proof of face-exact Theorem 2 (per-factor envelopes) uses chords
     centered at box centers, one per factor. Wherever the unary terms are
     quadratic, minimizing over class-(a) splits reduces such a bound to a
     single chord of `f`, which never exceeds `f(p) - f*` (Proposition 2.3).
     So that proof cannot be made split-robust. Face-exact Theorem 1
     (termwise McCormick) is not affected: every class-(a) split leaves the
     bilinear terms to McCormick and only adds nonnegative gaps, so its
     hypothesis (M_b) and its bound (for example `0.57 (5/3)^n` on the PROGRAM
     family) hold for every such split.
   - Concave unary terms alone create no gap: if every factor is concave in
     each variable on a box, the per-factor envelope bound equals the
     minimum of `f` over the box (Proposition 2.4). The candidate mechanism
     "unary terms concave away from `x*`" therefore does nothing inside the
     concave region.
3. **The mechanism that works (Section 3): shape incompatibility.** A
   three-variable gadget `x - y - z` with convex unary terms and bilinear
   couplings. The `x`-factor is cheapest when `y` is spread at `±t` (then
   `x` sits at a bound); the `z`-factor is cheapest when `y` is at `0` or
   `±1`. A class that shares only moments of `y` lets each factor use its own
   distribution of `y`. Five explicit points give a root gap
   `gamma = y1^2 (1-A)/A` (Proposition 3.2) for classes (a), (a0), (b2),
   (b3); 0.0761 for the reference parameters. For class (b_d) the gap is a
   polynomial-approximation problem in a band (Proposition 3.3): it lies
   between `2 E_d(L) - (eps_v + eta (1-y1)^2)` and `2 E_d(L)`, where `E_d(L)`
   is the best degree-`d` approximation error of the piecewise function `L`
   (of order `1/d^2`: about `0.095/d^2` to `0.18/d^2` for even
   `d = 2, 4, ..., 12` at `y1 = 0.38`; odd degrees add nothing,
   `E_{2k+1} = E_{2k}`). So, for each `d`, the gap is positive when
   `eps_v + eta (1-y1)^2 < 2 E_d(L)`; for fixed parameters it is zero for all
   large `d`. At the reference parameters class b10 already closes the gap
   exactly (rational certificate, Section 3.3).
4. **Theorem 4.3.** Chains of `G` gadgets (`n = 3G`, a path with weak links
   `delta`, unique nondegenerate interior minimizer `0`). For every
   single-tree run with per-factor envelopes (or anything weaker) and any
   per-node split from classes (a), (a0), (b2), (b3), leaves plus `2n` per
   tightening round number at least
   - `exp((gamma G - eps - delta (G-1))/Lambda)` (analytic; `1.003^n` for
     the reference parameters), and
   - `exp(-2.224 (eps + delta (G-1))) 1.1628^G`, about `1.052^n`
     (computer-evaluated).

   For class (b_d), with the base split stated in Theorem 4.3, the same holds
   with a gap `gamma_d`; computed bases per variable are 1.004–1.016
   (`d = 4`) and 1.0015–1.0044 (`d = 6`). Since `gamma_d <= 2 E_d(L)`, the
   base that Theorem 4.2 can prove for class (b_d) on this family is at most
   `exp(33.3 E_d(L)) = 1 + O(1/d^2)` per gadget, for every parameter choice.
   This limits the proof method, not the trees: class-b6 trees grow by 2.0
   per variable (item 6).
5. **Decomposition side (Section 5).** Theorem 3.4 of the decomposition note
   applies to the same family with the natural split: `O(n log(n/eps))`,
   with very large constants. With `delta = 0`, certifying each gadget
   separately with class-(a) bounds costs about 20–22 leaves per gadget. So
   the exponential separation survives every split in these classes on the
   single-tree side. The proved separation starts only near `n ≈ 850`
   (computer-evaluated base) or `n ≈ 15,000` (analytic base) against Theorem 3.4's
   constants, and near `n ≈ 140` or `3,300` against gadget bags.
6. **Numerics (Section 6).** Branch-and-bound with exact class-(a) node
   bounds (column generation; every pruned leaf carries a dual bound and
   every split box a primal fooling family; both consistency-checked (not
   certified) for class (a) with `G <= 2`) needs 20, 600 and
   12,336 leaves at `n = 3, 6, 9` (`eps = 1e-4`), about 2.85 per variable,
   and is nearly insensitive to `eps`. With the theorem's base split, class
   b4 needs 10, 172, 2,592 and class b6 needs 2, 16, 128 leaves (2.0 per
   variable). The fixed balanced split needs 88 and 7,372. The review
   reproduced every `delta = 0` count of classes (a), b4 and b6 (theorem's
   base split) with independent code, and the recheck reproduced those at
   `eps = 1e-4` with a third code. The `delta = 1e-3` and `delta = 0.1` rows
   were not reproduced independently.

**Open.** The gap between the proved base (1.05 per variable) and the
observed one (2.85), which needs a different counting argument (the present
one cannot exceed about 1.063 per variable at the reference parameters);
families without gadgets, in particular
uniform chains; strong couplings; classes whose degree grows with `n` or
`1/eps` (then the root can be exact); relaxations over cliques of three or
more variables.

## 1. Setting

### 1.1 Paths, factors and splits

- Root box `X0 = prod_i [L_i, U_i]`; objective
  `f(x) = sum_{e=1}^{n-1} f_e(x_e, x_{e+1})` with continuous factors;
  `f* = min_{X0} f`, `m = f - f*`.
- The families of this program have the form
  `f = sum_i u_i(x_i) + sum_e b_e x_e x_{e+1}` plus a base split of the
  `u_i` into the factors. The **balanced split** gives half of each interior
  `u_i` to each of its two factors and all of `u_1`, `u_n` to the end
  factors; the **unsplit** (PROGRAM) factorization gives `u_e` to factor
  `e`.

**Lemma 1.1 (every split on a path is a univariate redistribution).** If
`sum_e f_e = sum_e f'_e` on `X0`, where `f'_e` also depends only on
`(x_e, x_{e+1})`, then there are functions `r_1, ..., r_n` of one variable
with `r_1 = r_n = 0` such that `f'_e = f_e + r_{e+1}(x_{e+1}) - r_e(x_e)` for
every `e`.

*Proof.* Put `D_e = f'_e - f_e`, so `sum_e D_e = 0`. Fix `a in X0`.
`D_1(x_1, x_2) = -sum_{e>=2} D_e` does not depend on `x_1`, so
`D_1 = r_2(x_2)` with `r_2(t) = D_1(a_1, t)`. Suppose
`D_1 + ... + D_{k-1} = r_k(x_k)`. Then
`D_k(x_k, x_{k+1}) + r_k(x_k) = -sum_{e>k} D_e` does not depend on `x_k`;
call it `r_{k+1}(x_{k+1})`. So `D_k = r_{k+1} - r_k`. For `k = n-1` the
right side is `0`, so `r_n = 0`. □

In particular, a split whose factors differ from the base factors by
polynomials of degree at most `d` in the factor's two variables is a
redistribution of univariate polynomials of degree at most `d` (the `r_k`
built in the proof are such polynomials). Observation 4.2's split, restricted
to a path, is the redistribution of the value functions.

### 1.2 Split classes

**Definition.** A *split class* `S` assigns to each interior variable
`i in {2, ..., n-1}` a linear space `S_i` of continuous functions on
`[L_i, U_i]` that contains the affine functions. Its splits are
`f_e^r = f_e + r_{e+1} - r_e` with `r_i in S_i` (`r_1 = r_n = 0`).

- **(a)** `S_i = span{1, t, t^2, u_i}`: any weighting of `u_i` between its
  two factors, plus adding and subtracting `q_i t^2` and linear terms.
  **(a0)** `S_i = span{1, t, u_i}`: weights only.
- **(b_d)** `S_i = P_d` (polynomials of degree at most `d`), relative to a
  base split: by Lemma 1.1, all splits whose factors differ from the base
  factors by polynomials of degree at most `d`.
- **(full)** `S_i = C([L_i, U_i])`: all splits (Observation 4.2).

Linear redistribution is free: per-factor envelopes commute with adding
affine functions, and the added terms telescope. The envelope bound
optimizes it implicitly (Lemma 1.2).

### 1.3 The relaxation and its dual

For a box `A = prod [l_i, u_i]` write `A_e = [l_e, u_e] x [l_{e+1}, u_{e+1}]`.
For a split `r`,

```
F_A^r(x) = sum_e vex_{A_e} f_e^r (x_e, x_{e+1}),        LB_r(A) = min_A F_A^r,
LB_S(A)  = sup_{r in S} LB_r(A).
```

`LB_S(A)` is the bound when the solver picks the best split of the class for
each box, possibly knowing `x*`. A fixed split, or any per-factor relaxation
weaker than the envelope (McCormick, alphaBB, secants), gives a bound at most
`LB_S(A)`. So every lower bound on node counts proved for `LB_S` applies to
them.

**Lemma 1.2 (moment form).** Call a family `nu = (nu_e)` of probability
measures `nu_e` on `A_e` *S-consistent* if
`∫ phi dnu_{i-1}^{(i)} = ∫ phi dnu_i^{(i)}` for every interior `i` and
`phi in S_i`, where `nu^{(i)}` is the marginal on `x_i`. Then

```
LB_S(A) = sup_{r in S} sum_e min_{A_e} f_e^r = min { sum_e ∫ f_e dnu_e : nu S-consistent },
```

the minimum is attained, and the value does not depend on the base split as
long as base splits differ by elements of `S`.

*Proof.*
1. For a continuous `phi` on a box `B`,
   `vex_B phi(p) = min { ∫ phi dnu : nu in P(B), mean nu = p }`. The
   inequality `<=` is Jensen's for the convex minorant `vex_B phi`, and `>=`
   is Carathéodory's representation of the envelope by finitely many points.
   Hence `LB_r(A)` is the minimum over *mean-consistent* families of
   `L(nu, r) = sum_e ∫ f_e dnu_e + sum_i ∫ r_i d(nu_{i-1}^{(i)} - nu_i^{(i)})`.
2. The mean-consistent families form a convex weak*-compact set; `L` is affine
   and weak*-continuous in `nu` and affine in `r`. Sion's minimax theorem gives
   `sup_r min_nu L = min_nu sup_r L`, and `sup_r L(nu, r)` is
   `sum_e ∫ f_e dnu_e` if `nu` is S-consistent and `+inf` otherwise.
3. Dropping mean-consistency and taking `sup` over `r in S` gives the same
   value, because `S` contains the linear functions whose multipliers enforce
   mean-consistency; for fixed `r` the minimum over all families is
   `sum_e min_{A_e} f_e^r` (point masses). □

A consequence (noted by the review): the class bound equals
`sup_r sum_e min_{A_e} f_e^r`, so per-factor envelopes add nothing to the
best split followed by factor minima. The lower bounds below therefore also
cover solvers that bound each shifted factor by a constant (for example by
interval arithmetic) after optimizing the split. Lemma 1.2 is a restatement
of known duality (Section 1.5).

**Remarks.**

- *Observation 4.2.* With `S_i = C([L_i, U_i])`, consistent marginals are
  equal, and families with equal marginals on consecutive factors of a path
  glue to one measure on `A` (Markov-chain product). So `LB_full(A) =
  min_A f`. Any finite-dimensional `S_i` leaves room for different marginals
  with equal `S_i`-integrals; this room is the only source of gaps.
- *Lifted view.* `LB_S(A)` is the bound of the lifted relaxation that has, for
  each edge, the exact convex hull of
  `{(f_e(y), (phi(y_1))_{phi in S_e}, (phi(y_2))_{phi in S_{e+1}}) : y in A_e}`
  and shares the univariate coordinates between neighbouring edges (a point
  of the hull is a vector of integrals of a measure). Class (a) shares
  `x_i, x_i^2, u_i(x_i)`; class (b_d) shares `x_i^k`, `k <= d`. Relaxations
  with the same shared lifts but weaker edge sets have smaller bounds: for
  example McCormick, RLT and the `2x2` PSD cuts of SCIP's minor separator on
  a shared `x_i^2` variable, or the sparse Lasserre relaxation of order `r`
  with pair cliques for polynomial data (its PSD and localizing conditions
  hold for moments of true edge measures), which is dominated by `b_{2r}`.
  Degree-`d` sparse RLT (Sherali–Adams) with shared univariate monomials is
  dominated by `b_d` for the same reason.

### 1.4 Covers and branch-and-bound runs

**Definition.** A finite family `P` of boxes covering `X0` is an
*S-cover at tolerance `eps`* if `LB_S(C) >= f* - eps` for every `C in P`.
`N_S(eps)` is the least size of an S-cover.

**Lemma 1.3.** Consider a branch-and-bound run that terminates at tolerance
`eps`. At each node `B` it bounds with some split `r(B) in S` (any rule). It
may use any branching rule, split points and node order, incumbents
`UBD >= f*`, pruning by the node's own or an inherited bound, and rounds of
same-relaxation bound tightening: a round removes from the current box `B_k`
points `y` with `F^r_{B_k}(y) > UBD - eps` for some `r in S` (the `r` may
differ between points of the same round). Record children
instead of the parent when a parent's bound is the minimum of its children's.
Then the leaves together with the per-round frame pieces (at most `2n` per
round, [C, Lemma 2.1]) form an S-cover at tolerance `eps`. Hence
`#leaves + 2n #rounds >= N_S(eps)`.

*Proof.* The family covers `X0` by [C, Lemma 2.1(a)].
- Leaves. `LB_S` is monotone: on a smaller box fewer families are feasible in
  Lemma 1.2. A leaf `C` pruned by the bound of `A ⊇ C` satisfies
  `LB_S(C) >= LB_S(A) >= LB_{r(A)}(A) >= UBD - eps >= f* - eps`.
- Pieces. Let `Sp ⊆ B_k` be a frame piece of a round, and put
  `F = sup_{r in S} F^r_{B_k}`. Every removed point `y` satisfies
  `F(y) > UBD - eps`, whichever `r` removed it. `F` is convex (a supremum of
  convex functions) and finite on the box `B_k`:
  `F^0_{B_k} <= F <= f`, because `vex_{(B_k)_e} f_e^r <= f_e^r` and the
  `f_e^r` sum to `f`. The piece is closed, and its face shared with the kept
  box `B_{k+1}` may contain points that were not removed. Every other point of
  `Sp` was removed, so `F > UBD - eps` on a dense subset of `Sp`. `F` is
  upper semicontinuous on the box (a convex function is upper semicontinuous
  relative to any locally simplicial subset of its domain, such as a box;
  Rockafellar, *Convex Analysis*, Theorem 10.2, going back to Gale, Klee and
  Rockafellar 1968). So `F >= UBD - eps` on all of `Sp`. Now let `nu` be an
  S-consistent family on the factor boxes of `Sp`. Its common mean `z` lies
  in `Sp` (the means agree because `S` contains the affine functions). For
  every `r in S`,
  `sum_e ∫ f_e dnu_e = sum_e ∫ f_e^r dnu_e >= sum_e ∫ vex_{(B_k)_e} f_e^r dnu_e >= F^r_{B_k}(z)`
  by consistency and Jensen. Taking the supremum over `r` gives
  `sum_e ∫ f_e dnu_e >= F(z) >= UBD - eps`. So `LB_S(Sp) >= f* - eps`. A
  round that uses one `r` for all points is the special case
  `F^r_{B_k} <= F`. □

*Lifted relaxations with tightening.* The same proof covers a lifted
relaxation whose shared univariate lifts lie in `S` and whose edge sets
contain the moment vectors of true edge measures (Section 1.3), provided the
tightening rule is stated for that relaxation: a round removes points `y`
whose projected relaxation value `phi_{B_k}(y)` (the minimum of the lifted
relaxation with `x = y`) exceeds `UBD - eps`. `phi_{B_k}` is convex; if the
relaxation is feasible at every point of `B_k` and bounded below (for
example, because its lifted edge sets are bounded, as for McCormick, RLT or
moment relaxations on a box), `phi_{B_k}` is finite and hence upper
semicontinuous on the box (same theorem); and the moments of an S-consistent
family with mean `z` are feasible for the lifted relaxation at `x = z`, so its
value is at least `phi_{B_k}(z) >= UBD - eps`.

Not covered: cuts on three or more variables (for example on the aggregated
objective), convexity detection of `f` as a whole, lifted univariate
variables outside `S`, branching on lifted variables, and objective-cutoff
propagation.

### 1.5 Relation to prior work

Lemma 1.2 is known in substance; it is stated here in the form needed for
node counts. The references below were checked at the bibliographic level
(web search on 2026-09-30); the passages quoted for Cooper et al. were read in
the paper.

- *Affine `S` (per-factor envelopes of a fixed split).* The Lagrangian dual
  of a block-separable (copy) formulation equals the bound from the convex
  envelopes of the blocks. Falk (Oper. Res. 22 (1974) 410–413, "Sharper
  bounds on nonconvex programs") shows that the generalized-multiplier bound
  and the convex-envelope bound coincide for linearly constrained problems
  and for suitably separable ones. Dür and Horst (JOTA 95 (1997) 347–369)
  study this Lagrangian bound under partitioning in branch-and-bound, and
  Nowak (*Relaxation and Decomposition Methods for MINLP*, Birkhäuser 2005)
  treats block-separable reformulations and Lagrangian relaxation for MINLP.
  The review also cites an earlier paper, J. E. Falk, "Lagrange multipliers
  and nonconvex programs", SIAM J. Control 7(4) (1969) 534–545,
  doi 10.1137/0307039. Its bibliographic data were checked on Crossref; its
  content was not checked, so it is not used as a source here.
- *General `S`: reparametrization or cost shifting.* In discrete graphical
  models, equivalent transformations (Schlesinger, reviewed by Werner, IEEE
  TPAMI 29 (2007) 1165–1179), tree reweighting (Wainwright, Jaakkola and
  Willsky, IEEE TIT 51 (2005) 3697–3717) and dual decomposition (Sontag,
  Globerson and Jaakkola, "Introduction to dual decomposition for
  inference", in Sra, Nowozin and Wright (eds.), *Optimization for Machine
  Learning*, MIT Press 2011) maximize, over shifts of cost between factors,
  the sum of the factor minima. This maximum is the dual of the
  local-consistency LP relaxation, which is exact on trees (Wainwright and
  Jordan, Found. Trends Mach. Learn. 1 (2008) 1–305). The remark after
  Lemma 1.2 on Observation 4.2 is the continuous tree case of this fact.
- *Branch-and-bound with the best shift at each node.* In weighted CSP,
  Cooper, de Givry, Sánchez, Schiex, Zytnicki and Werner ("Soft arc
  consistency revisited", Artif. Intell. 174 (2010) 449–478) compute the
  optimal cost shift by an LP (OSAC, the dual of the LP relaxation, used in
  preprocessing) and approximate it by virtual arc consistency, "applied
  either during preprocessing or at every node of a search tree" (toulbar2).
  Ihler, Flerova, Dechter and Otten (UAI 2012) use cost shifting inside
  mini-bucket heuristics for branch-and-bound. These are the discrete
  ancestors of `LB_S` with a per-node split.
- *Consistency only on features.* Expectation-consistent inference (Opper and
  Winther, JMLR 6 (2005) 2177–2204) makes two tractable distributions agree
  on a set of moments; `LB_S` is the zero-temperature, optimization analogue
  with statistics `S_i`.
- *Sparse polynomial certificates.* The band criterion of Proposition 3.3
  (exactness iff the objective splits into nonnegative parts on the two
  cliques with a degree-`d` shift) is a two-clique instance of the
  structured-sparsity decomposition behind Lasserre's sparse hierarchy; see
  Grimm, Netzer and Schweighofer (Arch. Math. 89 (2007) 399–403) for a
  short proof of the sparse representation theorem.

*What is new here.* On a finite domain every function of one variable is a
finite vector, so discrete cost shifting already uses the full class, and
exactness on trees follows. On continuous domains a solver can shift only a
finite-dimensional class of functions, and that restriction is what creates
the gaps studied here. What this note adds is the use of the restricted-class
duality for node counts of spatial branch-and-bound: the monotone, per-node
form with bound tightening (Lemma 1.3), the negative results for per-factor
envelopes (Section 2), the five-point fooling and the band analysis of the
gadget (Section 3), and the split-robust product lower bound (Section 4). We
found no earlier rigorous spatial-B&B lower bound of this form; this is based
on the searches above and on the program's literature audit, not on a
systematic survey.

## 2. What cannot give split-robust bounds

### 2.1 The PROGRAM family is solved at the root

**Proposition 2.1.** Let `f = sum_i (x_i^2 - kappa x_i^4) + b sum_i x_i x_{i+1}`
on `[-1,1]^n` with `kappa in [0, 1]` and `|b| <= 1 - kappa`. With the balanced
split every factor is nonnegative on `[-1,1]^2` and vanishes at `0`. Hence
the balanced-split envelope bound of the root equals `f* = 0`, and the root is
pruned for every `eps >= 0` as soon as the incumbent satisfies
`UBD <= eps`, for example `UBD = f(0) = 0`.

*Proof.* On `[-1,1]`, `t^2 - kappa t^4 >= (1-kappa) t^2`. An interior factor is
at least `((1-kappa)/2)(x^2 + y^2) - |b||xy| >= (1 - kappa - |b|)|xy| >= 0`;
the end factors have an extra `(1-kappa) x^2/2`. So
`LB_r = min_x sum_e vex f_e >= sum_e min f_e = 0 = f(0)`. □

- The PROGRAM values `kappa = 0.1`, `b = 0.8` satisfy the condition. Up to
  equality it is the condition `kappa + b < 1` under which face-exact
  Lemma 1.1 proves that `x* = 0` is the unique minimizer.
- With the program's random linear terms the statement is not proved, but the
  numbers are similar (Section 6.2): 1 leaf for seed 0 and 1–17 leaves for
  seed 1 with the balanced split up to `n = 8`, and 1 leaf with class (a).
- The unsplit factorization, as in face-exact Theorem 2, needs 50, 190, 560
  and 1,464 leaves at `n = 3..6`.
- So the growth of 2.3–2.5 per variable that the decomposition review
  measured with the balanced split came from box-dependent alphaBB, which is
  much weaker than the per-factor envelope, and not from the factor structure.
  The open question of the synthesis is sharper than its motivating runs.

### 2.2 Near the minimizer

**Proposition 2.2 (face-exact note, Section 9.2).** If `∇^2 f(x*) ≻ 0` and
the `u_i` are `C^2` near `x*`, a class-(a0) split (weights only) makes every
factor strictly convex on a cube around `x*`. Boxes in that cube are exact,
so split-robust lower bounds cannot grow with `log(1/eps)`.

*Proof.* The diagonal entries `u_i''(x*_i)` of a positive definite matrix are
positive. Face-exact Lemma 9.1 (applied to `H - delta I`) splits them into
positive shares that make every `2x2` block positive definite; the weights
are the shares divided by `u_i''(x*_i)`, in `(0, 1)`. Continuity gives the
cube. □

### 2.3 Centered chords reduce to one chord

In the proofs of face-exact Theorems 1–2, the gap at a point `p` is bounded
below by chords symmetric about `p`, one per factor. For a split `r` let

```
Gamma_r(A, p) = sum_e sup { f_e^r(p_e) - (f_e^r(p_e + v) + f_e^r(p_e - v))/2 : p_e ± v in A_e }.
```

Then `f(p) - F^r_A(p) >= Gamma_r(A, p)`.

**Proposition 2.3.** Let `f = sum u_i + sum b_e x_e x_{e+1}` with every
`u_i` quadratic on `[l_i, u_i]`. Then, over class (a),

```
inf_r Gamma_r(A, p) = sup { f(p) - (f(p+v) + f(p-v))/2 : p ± v in A } <= f(p) - min_A f.
```

So a center-volume argument (face-exact Lemma 2.1) with such gap bounds
certifies nothing robustly: the admissibility inequality
`gap <= m(p) + eps` always holds.

*Proof.*
1. Let `D_i = u_i''` and `d_i = min(p_i - l_i, u_i - p_i)`. A class-(a) split
   changes the diagonals of the factor Hessians: factor `e` has Hessian
   `[[alpha_e, b_e], [b_e, beta_{e+1}]]` with `alpha_i + beta_i = D_i` for
   interior `i` (`alpha_1 = D_1`, `beta_n = D_n`), and every such pair is
   realized.
2. The chord defect of factor `e` along `v = (v_1, v_2)` is
   `-(alpha_e v_1^2 + 2 b_e v_1 v_2 + beta_{e+1} v_2^2)/2`, linear in
   `(s_1, s_2, t) = (v_1^2, v_2^2, v_1 v_2)`, which ranges in the compact
   convex set `K_e = {0 <= s_j <= d_j^2, |t| <= sqrt(s_1 s_2)}`.
3. So `inf_r Gamma_r <= inf_{alpha,beta} sum_e max_{K_e} (...) =
   max_{prod K_e} inf_{alpha,beta} (...)` by Sion's theorem. The inner
   infimum is `-inf` unless the two `s`-values of each interior variable
   agree, `s_{e-1,i} = s_{e,i} =: s_i`. It then equals
   `-(1/2) sum D_i s_i - sum b_e t_e <= -(1/2) sum D_i s_i + sum |b_e| sqrt(s_e s_{e+1})`.
4. Put `w_i = sqrt(s_i) in [0, d_i]` and choose signs `sigma_i` with
   `sigma_e sigma_{e+1} b_e <= 0` (possible on a path). Then `v = sigma ⊙ w`
   has `p ± v in A`, and the value is `f(p) - (f(p+v) + f(p-v))/2` because
   `f` is quadratic on `A`. This is at most `f(p) - min_A f`. Using the same
   `v` in every factor gives the reverse inequality. □

This is why face-exact Theorem 2's mechanism disappears under splits in every
region of constant unary curvature, not only near `x*`. A split-robust bound
for per-factor envelopes needs unary terms that are not quadratic on the
relevant boxes and fooling measures that are not symmetric two-point chords.

The proposition concerns per-factor envelopes only. Face-exact Theorem 1
(termwise McCormick) is invariant under class-(a) splits: each bilinear term
is still relaxed by McCormick alone, and the moved unary or quadratic pieces
are relaxed by their own underestimators, which add nonnegative gaps. So its
hypothesis (M_b) holds for every such split, and its bound applies
unchanged.

### 2.4 Edge-concave boxes are exact

**Proposition 2.4.** If for some split `r` every factor `f_e^r` is concave in
each of its two variables on `A_e`, then `LB_r(A) = min_A f`. In particular,
with the balanced split, every box on which all `u_i` are concave is exact.

*Proof.*
1. Every `p in A_e` is the mean of a distribution on the four vertices: split
   `p` along `x_e` onto the two edges `x_e = l_e, u_e`, then each edge point
   along `x_{e+1}`. Concavity along each direction gives
   `f_e^r(p) >= E f_e^r(vertex)`. So `g_e(p) = min {E f_e^r(V) : V vertex-valued, E V = p}`
   is a convex minorant of `f_e^r`, hence `g_e <= vex f_e^r`; Jensen gives the
   reverse. The envelope is vertex-polyhedral (compare Tardella 2004 and
   Meyer–Floudas 2005 for edge-concave functions).
2. So `LB_r(A)` is the minimum over families of vertex distributions `pi_e`
   with consistent means. A distribution on `{l_i, u_i}` is determined by its
   mean, so the marginals of `pi_{e-1}` and `pi_e` on `x_e` are equal. The
   product `pi(x) = pi_1(x_1, x_2) prod_{e>=2} pi_e(x_e, x_{e+1})/pi_e^{(e)}(x_e)`
   is a distribution on the vertices of `A` with these pair marginals. Hence
   `sum_e E_{pi_e} f_e^r = E_pi f >= min_A f`. □

So the task's candidate "unary terms concave for `|x_i| > r0`" produces no
gap on boxes inside the concave region; any gap needs a factor that is convex
in some variable on the box. The proposition does not rule out gaps on boxes
that straddle the convex core and the concave region. The construction below
uses only convex unary terms; its nonconvexity comes from the couplings.

## 3. The gadget

### 3.1 Definition and basic facts

Parameters `y1 in (0,1)`, `eta in (0,1)` and a valley parameter
`eps_v in (0, (1-eta)(1-y1)^2)`. (In the program's notation `eps` is the
tolerance; the valley parameter is written `eps_v`, and `epsf` in the
scripts.) Put

```
b = 2 y1,   b' = 2 eta + 2 (1-eta)(1-y1),   c = 1 + eta + eps_v,   z1 = 2 eta y1 / b',   k = 2 (1-eta) y1,
g(x, y, z) = y1^2 x^2 + b x y + c y^2 + u(z) + b' y z      on [-1,1]^3,
u(z) = b'^2 z^2/(4 eta)                     for |z| <= z1,
u(z) = (b'|z| + k)^2/4 - (1-eta) y1^2       for |z| >= z1.
```

`u` is even, convex and `C^{1,1}`: piecewise quadratic with curvature
`b'^2/(2 eta)` inside and `b'^2/2` outside. The factors are
`g_1(x, y) = y1^2 x^2 + b x y` and `g_2(y, z) = u(z) + b' y z`, and `c y^2` is
shared between them. Reference values: `(y1, eta, eps_v) = (0.38, 0.05, 0.02)`,
giving `b = 0.76`, `b' = 1.278`, `c = 1.07`, `z1 = 0.0297`.

**Lemma 3.1.** For `|y| <= 1`:

1. `min_{|x|<=1} g_1(x, y) = h1(y)`, with `h1(y) = -y^2` for `|y| <= y1` and
   `h1(y) = y1^2 - 2 y1 |y|` for `|y| >= y1`, attained at
   `x(y) = clip(-y/y1, -1, 1)`.
2. `min_{|z|<=1} g_2(y, z) = h2(y) = -eta y^2 - (1-eta)(|y| - y1)_+^2`,
   attained at `z(y) = h2'(y)/b' in [-1, 1]`.
3. `min_{x,z} g = K(y^2)` with `K(s) = eps_v s + eta (sqrt(s) - y1)_+^2`. So
   `g >= 0`, `0` is the unique minimizer, it is interior, and `∇^2 g(0) ≻ 0`
   (determinant `2 y1^2 b'^2 eps_v/eta`; smallest eigenvalue `0.005` for the
   reference values).
4. `g >= alpha (x^2 + z^2)` with `alpha = eps_v min(y1^2/4, b'^2/16)`.
5. `g` is convex on the slab `|z| < z1` and not convex at any point with
   `|z| > z1`.

*Proof.*
1. The quadratic in `x` is minimized at `-y/y1` if `|y| <= y1`, otherwise at
   `x = -sign(y)`.
2. `u'(z) = b'^2 z/(2 eta)` on `[-z1, z1]` and
   `u'(z) = sign(z) b'(b'|z| + k)/2` outside. For `|y| <= y1`,
   `z(y) = -2 eta y/b' in [-z1, z1]` and `u'(z(y)) = -b' y`, so `z(y)` is the
   minimizer of the convex function `u + b' y (.)`; the value is
   `eta y^2 - 2 eta y^2 = -eta y^2`. For `y > y1` (the case `y < -y1` is
   symmetric) `z(y) = -(2y - k)/b'`, which lies in `[-1, -z1]` because
   `b' + k = 2`; again `u'(z(y)) = -b' y`, and the value is
   `y^2 - (1-eta) y1^2 - y (2y - k) = h2(y)`.
3. `g = [g_1 - h1(y)] + [g_2 - h2(y)] + K(y^2)`, where
   `K(y^2) = h1 + h2 + c y^2` equals `eps_v y^2` for `|y| <= y1` and
   `eta(|y| - y1)^2 + eps_v y^2` otherwise. Both brackets are `>= 0` with
   equality only at `x = x(y)`, `z = z(y)`. The Hessian at `0` is
   `[[2 y1^2, b, 0], [b, 2c, b'], [0, b', b'^2/(2 eta)]]`, whose leading minors
   are `2 y1^2`, `4 y1^2 (c-1)` and `2 y1^2 b'^2 eps_v/eta`.
4. `g_1 - h1 >= y1^2 (x - x(y))^2` (strong convexity `2 y1^2` and optimality of
   `x(y)` on `[-1,1]`), and `g_2 - h2 >= (b'^2/4)(z - z(y))^2` (`u'' >= b'^2/2`).
   With `|x(y)| <= |y|/y1`, `|z(y)| <= 2|y|/b'` and `lambda = eps_v/2`:
   `y1^2 (x - x(y))^2 >= lambda (y1^2 x^2/2 - y^2)` and
   `(b'^2/4)(z - z(y))^2 >= lambda (b'^2 z^2/8 - y^2)`. Adding `K >= eps_v y^2`
   gives the claim.
5. Where `u''` exists, the Hessian is positive semidefinite iff
   `u'' >= b'^2/(2(c-1)) = b'^2/(2(eta + eps_v))`. This holds inside the slab
   and fails outside, because `eta + eps_v < 1`. □

All unary terms are convex. The objective is nonconvex outside the slab
`|z| <= z1` around `x*`, because `u` flattens while the couplings stay. This is
"nonconvexity away from `x*`", produced by curvature that drops rather than by
concave unary terms (compare Proposition 2.4).

### 3.2 The gap for classes (a), (a0), (b2), (b3)

Only `y` is shared by two factors. Its unary term `c y^2` is quadratic, so
class (a) and class (a0) give `S_y = P_2`, and class (b3) gives `S_y = P_3`.

**Proposition 3.2 (five-point fooling).** Let
`A = 1 + eps_v - (1-eta)(1-y1)^2`, `t* = y1/A` and `p = t*^2`. Then
`y1 < A < 1`, so `t* in (y1, 1]`. Define

- `nu_1` on `(x, y)`: mass `1/2` at `(-1, t*)` and at `(1, -t*)`;
- `nu_2` on `(y, z)`: mass `1 - p` at `(0, 0)` and mass `p/2` at `(1, -1)` and
  at `(-1, 1)`.

Both `y`-marginals are symmetric with second moment `p`, so they agree on
`P_3`. The value is

```
∫ g_1 dnu_1 + ∫ (c y^2 + g_2) dnu_2 = -gamma,        gamma = y1^2 (1 - A)/A.
```

Hence `LB_S([-1,1]^3) <= -gamma` for `S` in (a), (a0), (b2), (b3): the root
gap is at least `gamma`. For the reference values `gamma = 0.07612`. The
relaxation LP (Section 6) gives the same value, so the fooling is optimal in
these runs.

*Proof.* `A < 1` is the condition on `eps_v`; `A > y1` because
`(1-eta)(1-y1)^2 <= 1 - y1`. The marginals have mean `0`, third moment `0`
and second moment `p` (for `nu_2`: `p * 1`). Factor 1 at either atom:
`y1^2 - b t* = y1^2 - 2 y1 t*`. Factor 2: `u(1) = 1 - (1-eta) y1^2` since
`b' + k = 2`, so an outer atom contributes
`c + u(1) - b' = c + h2(1) = A`, and the total is `p A`. The sum is
`y1^2 - 2 y1 t* + A t*^2 = -y1^2 (1-A)/A`. The shares of `c y^2` may sit in
either factor, since `E y^2` agrees. □

Interpretation: with `k_j(s) = h_j(sqrt s)`, `k1` is convex in `s = y^2` (the
`x`-factor gains by spreading `y`, because `x` then sits at its bound and
`b x y` is linear in `|y|`), and `k2` is concave in `s` (the `z`-factor gains
by putting `y` at `0` or `±1`). A single value of `y` cannot do both. For a
sub-box `K = [-θx, θx] x [-θy, θy] x [-θz, θz]` the same construction gives
`LB_S(K) <= min_{p <= θy^2} [vex k1^K(p) + vex k2^K(p) + c p]`, with the
partial minima taken over `K` and envelopes on `[0, θy^2]` (used in
Section 4.3).

### 3.3 Class (b_d)

**Proposition 3.3 (band form).** For `d >= 2` put `L = -h1` and
`U = h2 + c y^2` on `[-1,1]`, so that `U - L = K(y^2) >= 0`. Then

```
gamma_d := -LB_{b_d}([-1,1]^3) = inf_{rho in P_d} [ max_{[-1,1]} (L - rho) + max_{[-1,1]} (rho - U) ].
```

Consequently:
1. `gamma_d >= 2 E_d(L) - (eps_v + eta (1-y1)^2)`, where
   `E_d(L) = min_{rho in P_d} ||L - rho||_inf > 0`;
2. for fixed parameters, `gamma_d = 0` for all large `d`;
3. `gamma_d <= 2 E_d(L)`, and `gamma_{2k+1} = gamma_{2k}`.

*Proof.* By Lemma 1.2 with `S_y = P_d` (and `c y^2` placed in factor 2),
`LB = sup_rho [min_{x,y} (g_1 + rho(y)) + min_{y,z} (c y^2 + g_2 - rho(y))]`
`= sup_rho [min (rho - L) + min (U - rho)]` by Lemma 3.1.
1. `max(rho - U) >= max(rho - L) - max(U - L)`, and
   `max(L - rho) + max(rho - L) = osc(L - rho) >= 2 E_d(L)` because `P_d`
   contains the constants. `max(U - L) = max_s K(s) = eps_v + eta(1-y1)^2`.
   `L` is not a polynomial (quadratic on `[-y1, y1]`, linear on `[y1, 1]`), so
   `E_d(L) > 0`.
2. `gbar = (L+U)/2` is even and equals `(1 + eps_v/2) y^2` near `0`, so
   `q(y) = (gbar(y) - gbar(0))/y^2` is continuous on `[-1,1]`. Take a polynomial
   `qt` with `|qt - q| <= eps_v/4` (Weierstrass). Then `rho = gbar(0) + y^2 qt`
   satisfies `|rho - gbar| <= eps_v y^2/4 < K(y^2)/2` for `y != 0`, so
   `L <= rho <= U` and `LB = 0` once `d >= deg rho`.
3. Take `rho` a best degree-`d` approximation of `L`. Then
   `max(L - rho) <= E_d(L)` and, since `U >= L`,
   `max(rho - U) <= max(rho - L) <= E_d(L)`. `L` and `U` are even, so
   replacing `rho` by its even part `(rho(y) + rho(-y))/2` does not increase
   either maximum; the best `rho` can be taken even, and odd degrees add
   nothing. □

Numbers (`y1 = 0.38`; grid-LP lower bounds on `E_d`, rounded down;
`logs/band_Ed.log`, `logs/revision3_checks.log`):
`E_2 >= 0.04508`, `E_4 >= 0.01009`, `E_6 >= 0.002634`, `E_8 >= 0.002536`,
`E_10 >= 0.001716`, `E_12 >= 0.000910`. The review bracketed these
two-sidedly to the 5 decimals it printed; the recheck's brackets and ours
(`revision3_checks.py`) have width at most about `1e-7`. So for even `d = 2, 4, ..., 12`, `d^2 E_d(L)` lies
between about 0.095 (`d = 6`) and 0.180 (`d = 2`). Odd degrees add nothing:
`L` is even, so, as in Proposition 3.3(3), a best approximation can be taken
even, and `E_{2k+1} = E_{2k}`. So for odd `d = 3, ..., 11` the product
`d^2 E_d` exceeds that of `d - 1`; it ranges from 0.13 to 0.41. With the reference
parameters (`eps_v + eta(1-y1)^2 = 0.0392`), the band LP and the relaxation
LP agree: `gamma_2 = gamma_3 = 0.07612`, `gamma_4 = gamma_5 = 0.00777`,
`gamma_6 = 0.00237`, `gamma_8 = gamma_9 = 0.00078`, and **`gamma_10 = 0`**:
class b10 closes the gadget's root gap, so it solves the reference chain with
`delta = 0` at the root (once `UBD <= eps`).

`gamma_10 = 0` is exact. The recheck
(`../reviews/robust-lb-recheck-checks/check_gamma.py`) gave an even
polynomial `rho = y^2 q(y)` of degree 10 with rational coefficients
(`q` has coefficients `1.002795549, 0.419528334, -3.338707087, 4.161904633,
-1.593496982` for `y^0, y^2, ..., y^8`). With `y1 = 19/50`, `eta = 1/20`,
`eps_v = 1/50`, none of `q - 1`, `1 + eps_v - q` (on `[0, y1]`),
`rho - L`, `U - rho` (on `[y1, 1]`) has a real root on its closed interval,
and each is positive at the midpoint. So `L <= rho <= U` on `[-1,1]` by
evenness, which gives `gamma_10 <= 0`; and `gamma_10 >= 0` because
`L(0) = U(0)`. We repeated the exact root counting with our own code
(`revision2_checks.py`, `logs/revision2_checks.log`). The earlier LP evidence
(band LP and relaxation LP, primal `0`, dual `-1.7e-11`;
`logs/band_check.log`, `logs/b10_gap.log`) agrees.

So `gamma_d` lies in `[2 E_d - 0.0392, 2 E_d]`; the lower end is vacuous at
`d = 4` here although `gamma_4 > 0`. For every `d` there are parameters with
`gamma_d > 0`: choose `eps_v + eta (1-y1)^2 < 2 E_d(L)`. Every fixed gadget
becomes exact for large `d`, so a construction that defeats class (b_d) must
depend on `d`, and by item 3 its gap is at most `2 E_d(L)`, which depends
only on `y1` and is `O(1/d^2)` uniformly in `y1` (`L'` is 2-Lipschitz for
every `y1`, so Jackson's theorem applies with a constant independent of
`y1`).

### 3.4 Where the escape of Observation 4.2 is excluded

- Observation 4.2's split for the gadget subtracts `h1(y)` from factor 1 and
  adds it to factor 2: factor 1 becomes `g_1 - h1(y) >= 0` and factor 2 becomes
  `c y^2 + g_2 + h1(y) >= K(y^2) >= 0`, both zero at `x*`. The proof of
  Proposition 3.3 works for any `S_y` that contains the constants: the root
  bound is `sup_{rho in S_y} [min (rho - L) + min (U - rho)]`. For a
  finite-dimensional `S_y`, where the supremum is attained, the class closes
  the root gap exactly when `S_y` contains a function in the band `[L, U]`
  (up to a constant). The band has width `K(y^2) <= eps_v + eta(1-y1)^2` and
  lies above `L = -h1`, whose second derivative jumps at `|y| = y1` (where `x`
  reaches its bound). `rho = L` itself is in the band, which is Observation
  4.2's split.
- Class (a) contains only quadratics in `y`. The best quadratic misses the band
  by at least `2 E_2(L) - 0.03922 > 0.0509` for the reference values; the actual
  gap is `0.0761`. In measure form, the five-point fooling agrees on
  `1, y, y^2, y^3` but gives `h1` different integrals.
- Class (b_d) contains degree-`d` polynomials. `E_d(L)` decays like
  `1/d^2` (a jump in `L''`), and Proposition 3.3(1) guarantees a gap when
  the band width `eps_v + eta(1-y1)^2` is below `2 E_d(L)`.
  At the reference parameters degree 10 already fits into the band
  (`gamma_10 = 0`).
- Knowing `x*` does not help: the restriction is the class, not information.

## 4. Product lower bound

### 4.1 Gadget chains

`F_G` on `[-1,1]^{3G}`, with variables ordered `x_1, y_1, z_1, x_2, ...`:

```
F_G = sum_{g=1}^G g(x_g, y_g, z_g) + delta sum_{g<G} z_g x_{g+1},     delta >= 0.
```

The factors are `(x_g, y_g)`, `(y_g, z_g)` and `(z_g, x_{g+1})`. The
interaction graph is the path (`delta > 0`) or a linear forest (`delta = 0`);
the treewidth is 1.

**Lemma 4.1.** If `0 <= delta < 2 alpha`, then
`F_G >= (1 - delta/(2 alpha)) sum_g g(x_g, y_g, z_g)`. So `0` is the unique
global minimizer, it is interior, `∇^2 F_G(0) ≻ 0`, and `F* = 0`.

*Proof.* `delta |z_g x_{g+1}| <= (delta/2)(z_g^2 + x_{g+1}^2)`, and each
`z_g` and `x_{g+1}` occurs in one connecting term; use Lemma 3.1(4). For the
Hessian: `F_G - (1 - delta/(2 alpha)) sum g >= 0` has value and gradient `0`
at `0`, so its Hessian there is positive semidefinite, and `sum g` has a
positive definite Hessian. □

For the reference values `2 alpha = 1.44e-3`. The range is not sharp. For
`delta = 0.1` the minimizer moves (numerically `F* = -0.060` at `G = 2` and
`-0.124` at `G = 3`), and the construction no longer applies.

### 4.2 Tilted volume

**Theorem 4.2.** Let `0 <= delta < 2 alpha` (so `F* = 0` by Lemma 4.1), let
`S` be any split class, and let the chain's base split keep all unary terms in
the gadget factors. For a box `B ⊆ [-1,1]^3` let
`V(B)` be the class bound of the three-variable gadget alone on `B`
(`f*` of the gadget is `0`), and let `Dhat(B) >= V(B)` be any upper bound. For
`mu > 0` put

```
Phi(mu) = sup_{B ⊆ [-1,1]^3} (vol(B)/8) exp(mu Dhat(B)).
```

Then every S-cover `P` of `[-1,1]^{3G}` at tolerance `eps` satisfies

```
|P| >= exp(-mu (eps + delta (G-1))) Phi(mu)^(-G).
```

*Proof.*
1. Let `C = prod_g C_g in P`. For each `g` take an optimal S-consistent family
   for `V(C_g)` (Lemma 1.2). For the connecting factor `(z_g, x_{g+1})` take the
   product of the `z_g`-marginal of gadget `g`'s second factor and the
   `x_{g+1}`-marginal of gadget `g+1`'s first factor. The combined family is
   S-consistent: at `y_g` by choice, and at `z_g`, `x_{g+1}` because the two
   marginals are identical. Its value is
   `sum_g V(C_g) + delta sum_g E z_g E x_{g+1} <= sum_g Dhat(C_g) + delta (G-1)`.
   Since `F* = 0` and `LB_S(C) >= -eps`, we get
   `sum_g Dhat(C_g) >= -eps - delta (G-1)`.
2. Hence `1 <= exp(mu (eps + delta (G-1)) + mu sum_g Dhat(C_g))`, and
   `vol(C)/8^G <= exp(mu (eps + delta (G-1))) prod_g (vol(C_g)/8) exp(mu Dhat(C_g)) <= exp(mu(eps + delta(G-1))) Phi(mu)^G`.
3. The members cover the cube, so `sum_{C in P} vol(C)/8^G >= 1`. □

This is the product analogue of the center-volume lemma: a box that is loose
in some gadgets (`Dhat < 0`) must be tight or far from the optimum in others,
and the exponential weight trades volume against gap.

### 4.3 Two ways to bound `Dhat`

**(a) Transport (analytic).** For a box `B = prod [l_j, u_j] ⊆ [-1,1]^3` with
relative sides `rho_j = (u_j - l_j)/2`, map the five-point fooling of
Proposition 3.2 by `T_j(t) = l_j + rho_j (t + 1)`. The images of the two
`y`-marginals still agree on `P_3`, because `T_y` is affine; so the image is
S-consistent for the classes of Proposition 3.2 (and for `b_d`, when a
`b_d`-fooling is transported). Since `|T_j t - t| <= 2(1 - rho_j)` and

```
Lambda_x = 2 y1^2 + 2 y1,    Lambda_y = 2 y1 + 2c + b',    Lambda_z = 2 b'
```

bound `|∂_j|` of the two factors (with `c y^2` in factor 1; `u'(1) = b'`), the
value moves by at most `sum_j 2 Lambda_j (1 - rho_j)`. So
`Dhat(B) = -gamma + sum_j 2 Lambda_j (1 - rho_j)` is valid, and

```
(vol(B)/8) exp(mu Dhat(B)) = exp(-mu gamma) prod_j rho_j exp(2 mu Lambda_j (1 - rho_j)) <= exp(-mu gamma)
```

whenever `2 mu Lambda_j <= 1` (`rho exp(a(1 - rho)) <= 1` on `[0,1]` for
`a <= 1`).

**(b) Cores and point masses (computed).** For nested cubes
`K_theta = [-theta, theta]^3`, use `Dhat(B) = -gamma(theta)` if `B ⊇ K_theta`
(symmetric fooling on `K_theta`, Section 3.2, and monotonicity), and
`Dhat(B) = min_B g` otherwise (a point mass). A box that contains `K_{theta_i}`
but not `K_{theta_{i+1}}` misses a slab in one coordinate, so
`vol/8 <= (1 + theta_{i+1})/2`. Therefore

```
Phi(mu) <= max { exp(-mu gamma(1)),  max_i ((1 + theta_{i+1})/2) exp(-mu gamma(theta_i)),  Psi(mu) },
Psi(mu)  = sup_{B not containing K_{theta_1}} (vol(B)/8) exp(mu min_B g).
```

`Psi` is bounded with the separable estimate
`min_B g <= min_{B_x} (y1^2 x^2 + b x y0) + c y0^2 + min_{B_z} (u + b' y0 z)`
for grid points `y0 in B_y`, with inner and outer grid intervals
(`gadget_bound.py`; details in its docstring). Interval minima over fine grid
points are upper bounds on the true minima, which is the safe direction. One
term goes the other way: for boxes with no grid point inside, the maximum of
a coupling function is taken over fine grid points and so is too small by
about the Lipschitz constant times the fine spacing, about `1e-3` in the
exponent. These terms are not binding, so the effect is cosmetic, but the
evaluation is a careful floating-point computation, not a rigorous
enclosure.

### 4.4 Main theorem

**Theorem 4.3.** Let `0 < eps_v < (1-eta)(1-y1)^2` and `0 <= delta < 2 alpha`,
and let `F_G` be the gadget chain (`n = 3G`). Consider single-tree
branch-and-bound as in Lemma 1.3, with per-factor convex envelopes (or any
weaker per-factor relaxation) and, at each node, any split from class (a),
(a0), (b2) or (b3), chosen per node and possibly with knowledge of `x*`. For
(b2), (b3) and (b_d) the classes are taken relative to the base split of
Theorem 4.2 (all unary terms in the gadget factors); this matters because
`u(z)` is not a polynomial. For (a) and (a0) the base split is irrelevant,
because `u_i in S_i`. Then:

1. (analytic)
   `#leaves + 2n #rounds >= exp((gamma G - eps - delta (G-1))/Lambda)`, where
   `gamma = y1^2 (1-A)/A` and `Lambda = 2 max(Lambda_x, Lambda_y, Lambda_z)`.
   For the reference values `gamma = 0.07612` and `Lambda = 8.356`, so the
   bound is `exp(-(eps + delta(G-1))/8.356) 1.00915^G`, about `1.003^n`.
2. (computer-evaluated) For the reference values,
   `#leaves + 2n #rounds >= exp(-2.224 (eps + delta (G-1))) 1.1628^G`,
   that is `1.0516` per variable for small `eps` and `delta = 0`.
3. (class b_d, `d >= 4`) Item 1 holds with `gamma_d` in place of `gamma`
   whenever `gamma_d > 0`, and for every `d` this is the case for suitable
   parameters (Proposition 3.3). Computed bases per variable: `d = 4`: 1.0036
   (reference), 1.0158 (`y1 = 0.3`, `eta = 0.005`, `eps_v = 0.002`); `d = 6`:
   1.0015 (reference), 1.0044 (`y1 = 0.5`, `eta = 0.005`, `eps_v = 0.002`).
   Since `gamma_d <= 2 E_d(L)` (Proposition 3.3(3)), the counting method
   cannot do much better:
   - *Every parameter choice.* On the box `[-1,-1/2]^3` every term of both
     factors is nonnegative (the couplings have positive coefficients and
     both arguments negative), so with the split `r = 0` each factor is at
     least its share of `c y^2`, and the shares add up to `c y^2 >= c/4`
     (take both shares nonnegative; this
     is no restriction, because `y^2` lies in every class considered here,
     and base splits that differ by elements of the class give the same
     bound, Lemma 1.2). Hence, for every such class,
     `V >= c/4 > 1/4` there and `(vol/8) exp(mu V) >= exp(mu/4)/64`, which is
     at least 1 once `mu >= 4 ln 64 ≈ 16.64`. For such `mu`, Theorem 4.2
     gives nothing. For smaller `mu`, the full cube gives
     `Phi(mu) >= exp(-mu gamma_d)`. So the base that Theorem 4.2 can prove
     for class (b_d) is at most `exp(16.64 gamma_d) <= exp(33.3 E_d(L))` per
     gadget, which is `1 + O(1/d^2)` uniformly in the parameters
     (Section 3.3).
   - *Reference parameters.* There the method needs `mu < 2.387`
     (Section 4.4), so any class-(b_d) base it gives is at most
     `exp(2.4 gamma_d) <= exp(4.8 E_d(L))` per gadget.
   - *`(y1, eta, eps_v) = (0.30, 0.005, 0.002)`.* The best corner box gives
     `mu < 2.378` (recheck; repeated in `logs/revision2_checks.log`), so the
     `d = 4` base there is at most `exp(2.4 · 2 E_4(L)/3) = 1.021` per
     variable (`E_4(L) = 0.01306` at `y1 = 0.3`), or 1.020 with the computed
     `gamma_4 = 0.0247`. The computed base is 1.0158.

   These caps concern only the bases Theorem 4.2 can prove, not the true
   tree sizes.

*Proof.* Lemma 1.3 reduces runs to S-covers. Theorem 4.2 with Section 4.3(a)
and `mu = 1/Lambda` gives item 1. Item 2 is Theorem 4.2 with Section 4.3(b),
evaluated with cores `theta in {0.46, 0.48, ..., 1}`, a grid of 101 points per
axis and the minimizing `mu` (`logs/bound_eval.log`). For item 3, the gadget
bound is attained by an S-consistent family (Lemma 1.2) with value
`-gamma_d`, and polynomial moment agreement is invariant under affine maps, so
Section 4.3(a) applies unchanged; the computed bases use Section 4.3(b) with
LP foolings on the cores (`logs/scan_bd.log`, `logs/bound_eval.log`). The
uniform cap in item 3 is proved in its first bullet; the other two caps use
the computer-evaluated corner-box thresholds `mu0` of Section 4.4 and
Section 6.5. □

**Remarks.**

- *Tolerance.* The bound has no `log(1/eps)` factor, as Proposition 2.2
  requires. It holds for every `eps` below a constant.
- *Flatness of the valley.* The smallest Hessian eigenvalue at `0` is `0.005`
  for `eps_v = 0.02`. The construction works for every
  `eps_v < (1-eta)(1-y1)^2 ≈ 0.365`. At `eps_v = 0.1` and `0.2` (smallest
  eigenvalues 0.023 and 0.044) the computed bases per variable are 1.0355 and
  1.0186 (`logs/scan_bd.log`, `logs/constants.log`). A flat valley helps but
  is not essential.
- *Smoothness.* `u` is `C^{1,1}` and smooth near `x*`. Mollifying `u` near
  `|z| = z1` changes `gamma` continuously and leaves `h2` unchanged near
  `y = 0`, so a `C^inf` version should work (sketch, not checked). A
  polynomial version, needed for the sparse-Lasserre remark of Section 1.3,
  would approximate `u` by a polynomial matching it to second order at `0`
  (sketch, not checked).
- *Where the constant is lost, and a ceiling.* Transport (item 1) charges
  every slightly shrunk box with the Lipschitz constant of the whole gadget.
  The core/point-mass bound (item 2) is limited by boxes that miss a thin
  slab of the smallest core (they contain `x*`, so their `Dhat` is at most
  `0`) and by small boxes in high corners of the cube. **At the reference
  parameters the tilted-volume method itself cannot give more than about
  1.063 per variable, even with exact gadget bounds** (review, check 4b).
  With `Dhat = V`, the full cube gives `Phi(mu) >= exp(-mu gamma)`. On the
  corner box `[-1,-0.48] x [-1,-0.873] x [-1,-0.813]` every term of both
  factors is nondecreasing in `|x|, |y|, |z|`, so both factor minima lie at
  the vertex nearest `0` and `V = min_B g = 2.7124` for every class (the
  class-(a) dual and primal bounds agree). There
  `(vol/8) exp(mu V) = 0.79, 1.037, 1.36` at `mu = 2.3, 2.4, 2.5`
  (`ceiling_check.py`, `logs/ceiling_check.log`); it reaches 1 at
  `mu0 = 2.387`. So every admissible `mu` is below `mu0`, and the base is at
  most `exp(mu0 gamma) = 1.1992` per gadget, 1.0624 per variable. The
  recheck's scan over corner boxes and our own continuous search
  (`logs/revision2_checks.log`) find essentially the same box
  (`mu0 = 2.3866`). The ceiling
  depends on the parameters: for class (a) at the 19 other parameter sets of
  the scan in Section 6.5, the best corner box gives 1.022–1.075 per
  variable. These are upper bounds on the method's ceiling at those
  parameters. The computed 1.0516
  is within about 1% of the reference ceiling, and the review's adversarial
  search puts the true
  `Phi(2.224)` in `[0.8443, 0.8600]`, against the computed `0.8600`. Closing
  the gap to the observed 2.85 per variable (Section 6.4) needs a different
  counting argument (a non-uniform reference measure, multiscale or
  tree-structured counting), not better per-box estimates.

## 5. The decomposition side

- **Theorem 3.4 of the decomposition note applies** to `F_G` with the natural
  split and the path decomposition (bags `{v_j, v_{j+1}}`, `w = 1`):
  - (QG): `F_G >= (1 - delta/(2 alpha)) sum g` and
    `g >= (1/2) min(alpha, eps_v) |(x, y, z)|^2` (Lemma 3.1), so
    `c_g = (1 - delta/(2 alpha)) min(alpha, eps_v)/2`;
  - (L^{1,1}): the factors are `C^{1,1}` with bounded Hessians;
  - (U^q_{alpha'}): factor 1 (with `c y^2`) is convex
    (`4 y1^2 (c-1) > 0`), so its envelope is exact; factor 2 and the connecting
    factor have Hessians bounded below, and the envelope is at least the
    alphaBB underestimator.

  So there is a decomposition certificate of size `O(n log(n/eps))` with
  constants that depend only on `(y1, eta, eps_v)`. The constants are very
  large: with `c_g ≈ 3.6e-4` and `M_a ≈ 16.4`, condition (T2) forces
  `theta = 2^-21`, so `(4/theta)^2 ≈ 7e13`, and the size bound is about
  `4e15 n` at `eps = 1e-4`.
- **For `delta = 0`** the gadgets are independent. Bags equal to the gadgets
  (width 2, empty separators), each certified at tolerance `eps/G`, give a
  certificate of size `sum_g N_gadget(eps/G)`: 20–22 leaves per gadget for
  `eps` between `1e-4` and `1e-6` (Section 6.4). These are **class-(a)**
  counts, the same class as on the single-tree side. Under the fixed natural
  split, factor 2 (`u(z) + b' y z`, Hessian determinant `-b'^2`) is nonconvex
  at `x*`, so a per-gadget tree with that split clusters at `x*` and needs
  more leaves.
- **Where the proved separation starts** (review's estimate, rechecked here
  by the arithmetic `1.0516^n = 4e15 n` and so on). Against Theorem 3.4's
  constants: near `n ≈ 850` with the computed base and `n ≈ 15,000` with the
  analytic base. Against gadget bags with `delta = 0` (about `7.3 n` leaves):
  near `n ≈ 140` and `n ≈ 3,300`.
- **Component detection.** For `delta = 0` the problem is separable, and any
  solver that detects independent components (for example SCIP's components
  presolver) splits it into gadgets and avoids the exponential. The weak
  links `delta > 0` exist to defeat this; they are too weak to change the
  counts (Section 6.4).
- **So the separation survives the split classes.** Against every per-node
  split of class (a), (a0), (b2) or (b3) on the single-tree side, the
  decomposition side needs only the fixed natural split:
  `N_single/N_dec >= c^n/(C n log(n/eps))` with `c = 1.003` (analytic) or
  `1.05` (computed). The decomposition wins because its separator cells
  localize `y`, and inside a small cell two distributions of `y` with equal
  moments differ little.

## 6. Numerical checks

All computations are double precision. Tolerance `eps = 1e-4` unless stated,
incumbent `f*` (0 for the chains, multi-start L-BFGS-B for the PROGRAM seeds),
widest-side bisection at midpoints.

### 6.1 Method and validation (`robust_bb.py`, `verify_leaves.py`, `verify_split.py`, `band_check.py`)

- The node bound `LB_S(B)` is computed by column generation on the moment form
  of Lemma 1.2. The primal LP over finitely many points per factor gives an
  explicit S-consistent family, whose value is an *upper* bound on `LB_S(B)`.
  The LP duals give a split `r in S`, and `sum_e min_{B_e} f_e^r` (exact
  minimization over each rectangle from critical points of the polynomial
  pieces, edges and corners) is a *lower* bound. A box is pruned when the lower
  bound reaches `f* - eps` and split when the upper bound is below it. Boxes
  where neither happened within 80 iterations are split and counted as
  "unresolved". Only the superseded balanced-split b6 run at `G = 3` has
  any (15).
- The chain runs use the base split of Theorem 4.2 (`base="gadget"` in
  `robust_bb.py`: all unary terms in the gadget factors, none in the
  connecting factors) unless stated otherwise. For class (a) the base split
  does not matter; for `b_d` it does, because `u(z)` is not a polynomial.
- Consistency checks for class (a), `G = 1, 2`:
  - for all 620 pruned leaves, the claimed factor minima were re-estimated
    (301 x 301 grid plus bounded L-BFGS-B); the claimed bound never exceeds the
    independent estimate by more than `2.8e-16`, and the shifted factors sum to
    `f` within `9e-16`;
  - for all 618 split boxes, the stored primal families have consistency
    residuals at most `1.2e-15`, weights summing to 1, and values below
    `f* - eps` (the closest by `2.2e-6`).

  The leaf check compares with an independent *estimate* of each factor
  minimum (grid plus local search), so it is a consistency check, not a
  certificate. Within the tolerances of the LP and the polynomial root
  finder, the counts are the exact tree sizes of widest-side bisection with
  the class bound. The review's independent reimplementation (reduction to
  measures on `y`, exact piecewise minimization) reproduced every
  `delta = 0` count of classes (a), b4 and b6 with the theorem's base split
  in Section 6.4 (class (a) at `eps = 1e-2, 1e-4, 1e-6`; b4 and b6 at
  `eps = 1e-4`; `G = 1, 2, 3`), with decision margins of at least `3.3e-5`
  (pruned boxes) and `1.4e-5` (split boxes) for class (a) at `eps = 1e-4`.
  The recheck's third implementation reproduced the `eps = 1e-4` counts, with
  no ambiguous boxes. Both use the `delta = 0` product structure, so the
  `delta = 1e-3` row (600, 12,330) and the `delta = 0.1` row (44, 108) were
  not reproduced independently.
- The relaxation LP, the band LP of Proposition 3.3 and the closed form of
  Proposition 3.2 agree to six digits (Sections 3.2–3.3).

### 6.2 PROGRAM family (`kappa = 0.1`, `b = 0.8`)

Leaves (`logs/bb_jobs1.log`):

| linear terms | relaxation | n = 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|
| `c = 0` | envelopes, balanced split | – | – | – | – | 1 |
| `c = 0` | envelopes, unsplit (face-exact Thm 2) | 50 | 190 | 560 | 1,464 | – |
| seed 0 | envelopes, balanced split | 1 | 1 | – | 1 | 1 |
| seed 0 | class (a) | – | – | – | 1 | 1 |
| seed 1 | envelopes, balanced split | 1 | 1 | – | 10 | 17 |
| seed 1 | class (a) | – | – | – | 1 | 1 |
| `c = 0` | alphaBB, balanced split (face-exact 9.3, decomposition review) | 24 | 64 | 162 | 404 | 2,476 |

Proposition 2.1 proves the first row for every `n`.

### 6.3 Gadget root gaps (reference parameters)

| class | env (balanced, fixed) | a, a0, b2, b3 | b4 | b5 | b6 | b8 |
|---|---|---|---|---|---|---|
| root gap | 0.1255 | 0.07612 | 0.00777 | 0.00777 | 0.00237 | 0.00078 |

### 6.4 Gadget chains: leaves under widest-side bisection

| class | base split | `eps` | `delta` | G = 1 (n = 3) | G = 2 (n = 6) | G = 3 (n = 9) | per variable, G = 2 → 3 |
|---|---|---|---|---|---|---|---|
| a | any | 1e-2 | 0 | 10 | 204 | 3,952 | 2.69 |
| a | any | 1e-4 | 0 | 20 | 600 | 12,336 | 2.74 |
| a | any | 1e-6 | 0 | 22 | 628 | 12,696 | 2.72 |
| a | any | 1e-4 | 1e-3 | – | 600 | 12,330 | 2.74 |
| b4 | theorem | 1e-4 | 0 | 10 | 172 | 2,592 | 2.47 |
| b6 | theorem | 1e-4 | 0 | 2 | 16 | 128 | 2.00 |
| b6 | balanced (a different class) | 1e-4 | 0 | 2 | 44 | 919 (15 unresolved) | – |
| env | balanced, fixed | 1e-4 | 0 | 88 | 7,372 | – | – |
| a, outside Lemma 4.1 | any | 1e-4 | 0.1 | – | 44 | 108 | 1.35 |

- Growth is exponential and almost independent of `eps`, as Theorem 4.3
  predicts: `12336^(1/9) = 2.85` per variable overall for class (a).
- The weak link `delta = 1e-3` changes nothing. With `delta = 0.1` the minimizer
  moves (`F* < 0`) and the counts are much smaller; Lemma 4.1 does not cover
  this case.
- Class b4 grows by 2.47 per variable (`G = 2 → 3`) and class b6 by 2.00,
  against 2.74 for class (a); the larger classes grow more slowly, in line with
  their smaller root gaps (0.0078 and 0.0024 against 0.0761).
- **Correction.** The first version reported b6 = 2, 44, 919 (15 unresolved)
  and said that b4 and b6 grow as fast as class (a). Those b6 runs used the
  balanced base split, which puts half of `u(z_g)` and half of `y1^2 x_{g+1}^2`
  into the connecting factor; polynomial shifts cannot move `u(z_g)/2` back,
  so that is a different class. The b4 counts happen to be the same under
  both base splits (`logs/bb_jobs1.log`, `logs/bb_jobs2.log`).

### 6.5 Proved bases (`logs/bound_eval.log`, `logs/scan_bd.log`, `logs/constants.log`)

| class | parameters `(y1, eta, eps_v)` | gap `gamma` | base per gadget | per variable | corner-box `mu0` | ceiling per variable |
|---|---|---|---|---|---|---|
| a (analytic, Thm 4.3(1)) | (0.38, 0.05, 0.02) | 0.0761 | 1.0092 | 1.0030 | 2.387 | 1.0624 |
| a (computed) | (0.38, 0.05, 0.02) | 0.0761 | 1.1628 | 1.0516 | 2.387 | 1.0624 |
| a (computed) | (0.38, 0.01, 0.005) | 0.0868 | 1.1825 | 1.0575 | 2.444 | 1.0733 |
| a (computed) | (0.38, 0.05, 0.1) | 0.0521 | 1.1103 | 1.0355 | 2.334 | 1.0414 |
| a (computed) | (0.38, 0.05, 0.2) | 0.0286 | 1.0567 | 1.0186 | 2.271 | 1.0219 |
| b4 (computed) | (0.38, 0.05, 0.02) | 0.0078 | 1.0109 | 1.0036 | 2.387 | 1.0062 |
| b4 (computed) | (0.30, 0.005, 0.002) | 0.0247 | 1.0480 | 1.0158 | 2.378 | 1.0198 |
| b6 (computed) | (0.38, 0.05, 0.02) | 0.0024 | 1.0044 | 1.0015 | 2.387 | 1.0019 |
| b6 (computed) | (0.50, 0.005, 0.002) | 0.0073 | 1.0134 | 1.0044 | 2.514 | 1.0062 |

The last two columns are the ceiling of Section 4.4 for each row: `mu0` is
the smallest `mu` at which some corner box `[-1,-a] x [-1,-b] x [-1,-c]` has
`(vol/8) exp(mu V) >= 1` (there `V = min_B g` for every class), and the
ceiling is `exp(mu0 gamma/3)`. They are floating-point evaluations
(`revision2_checks.py`, continuous multi-start search; the recheck's grid
scan gives the same `mu0` to 4 digits where both were run).

We also computed `mu0` for all 20 distinct parameter sets of
`logs/scan_bd.log`, with the same search (`revision3_checks.py`,
`logs/revision3_checks.log`, which lists each set with its `mu0`). For class
(a), the ceilings at the 19 sets other than the reference range from 1.022
at `(0.38, 0.05, 0.2)` to 1.075 at `(0.38, 0.005, 0.002)`. No class-(a) base
was computed at the latter set; the scan ran only b4 and b6 there. In all
26 rows of `logs/scan_bd.log`, the minimizing `mu` lies below the `mu0` of
its parameter set, by at least 0.110. The confirmation recheck's grid plus
L-BFGS-B search gives the same `mu0` to 4 digits for all 20 sets.

Observed: about 2.7–2.85 per variable for class (a), 2.5 for b4 and 2.0 for b6
(Section 6.4). The proved bases are lower bounds for *every* certificate, not
only for bisection, and the loss is in the counting step. At the reference
parameters that step cannot exceed about 1.063 per variable for class (a);
for the other rows the ceiling is in the last column (Section 4.4, last
remark).

### 6.6 How the gadget was found (`gadget_explore.py`, `logs/gadget_explore.log`)

Two polynomial designs were tried first: a quartic `u(z) = z^2/2 - beta z^4`
with bilinear couplings, and a coupling `-b' z y^2`. Both have class-(a) gaps
(up to 0.022 and 0.21), with `gap/Lambda <= 0.008`. The piecewise-quadratic
`u` realizes the complementary shapes exactly (`k1` convex, `k2` concave in
`y^2`, `K` nearly flat). Its `gap/Lambda ≈ 0.009` is similar, but its partial
minima have closed forms (Lemma 3.1), which gives the explicit fooling of
Proposition 3.2, the band analysis of Proposition 3.3 and the computed bound of
Section 4.3(b). The second polynomial design cannot defeat class (b4): its
`h2 = -(b'^2/4) y^4` is a polynomial, so agreement of the first four moments
makes the `z`-factor neutral and the relaxation exact at the gadget root. The
quartic design can keep small class-(b4) and (b6) gaps (0.0025 and 0.0006 for
`a = 6`, `b = 0.5`, `c = 0.9536`, `beta = 0.25`, `b' = 0.6`; none at `b8`), or
lose them already at `b4` (`a = 4`, `beta = 0.35`, `b' = 0.3`)
(`designQ_gaps.py`, `logs/designQ_gaps.log`).

## 7. Status

| Item | Content | Status |
|---|---|---|
| Lemma 1.1 | splits on a path are univariate redistributions | proved |
| Lemma 1.2 | class bound = S-consistent moment relaxation; lifted view | proved (Sion); known in substance (Section 1.5) |
| Lemma 1.3 | runs with per-node splits and tightening give S-covers | proved; closed tightening pieces handled by upper semicontinuity of `sup_r F^r_{B_k}`, so the `r` may vary per removed point (revisions 1 and 2) |
| Prop 2.1 | PROGRAM family (`kappa + abs(b) <= 1`, `c = 0`) solved at the root by the balanced split, incumbent `<= eps` | proved; seeds numerical |
| Prop 2.2 | weighted splits convexify near a nondegenerate `x*` | proved (face-exact 9.2) |
| Prop 2.3 | centered-chord bounds for per-factor envelopes reduce to one chord under class (a) where unaries are quadratic; face-exact Theorem 1 unaffected | proved |
| Prop 2.4 | edge-concave boxes are exact | proved |
| Lemma 3.1 | gadget: partial minima, unique nondegenerate interior minimizer, growth, convexity region | proved |
| Prop 3.2 | five-point fooling, root gap `y1^2(1-A)/A` for (a), (a0), (b2), (b3) | proved; equality observed by LP |
| Prop 3.3 | band form for (b_d); `2E_d(L) - width <= gamma_d <= 2E_d(L)`; odd degrees add nothing; exact for large `d` (`gamma_10 = 0` at the reference parameters) | proved; `E_d` by grid LP (valid lower bounds; bracketed by the review, the recheck and the third revision); `gamma_10 = 0` exact (rational certificate from the recheck; exact root counting repeated here) |
| Lemma 4.1 | chain minimizer for `delta < 2 alpha` | proved |
| Thm 4.2 | tilted-volume product bound | proved |
| Thm 4.3(1) | analytic bound `exp((gamma G - eps - delta(G-1))/Lambda)`, `1.003^n` | proved |
| Thm 4.3(2) | `1.1628^G`, about `1.052^n` | computer-evaluated (floating point); review's adversarial search: true `Phi` within 2% |
| Ceiling | Theorem 4.2's method gives at most about 1.063 per variable at the reference parameters; 1.022–1.075 (class (a)) at the 19 other parameter sets of the scan (Section 6.5) | corner-box value `V = min_B g` proved for every class; `mu0` and the ceilings computer-evaluated (review, recheck, confirmation recheck, and here) |
| Thm 4.3(3) | class (b_d) (theorem base split): existence for every `d`; bases for `d = 4, 6`; base provable by Theorem 4.2 at most `exp(33.3 E_d(L))` per gadget for all parameters | existence and the uniform cap proved; bases computed; says nothing about true tree sizes |
| Section 5 | decomposition side `O(n log(n/eps))` on the same family; proved separation from `n ≈ 850` (computer-evaluated base) or `15,000` (analytic) | proved by citing decomposition Thm 3.4 (hypotheses checked here and by the review); `delta = 0` case direct; crossovers are estimates |
| Remarks 4.4 | `C^inf` and polynomial versions | sketch |
| Section 6 | B&B counts, every node decision backed by a dual bound or a primal fooling family | computed; consistency checks for class (a), `G <= 2`; every `delta = 0` count of classes (a), b4, b6 (theorem base split) reproduced by the review's independent code, the `eps = 1e-4` ones also by the recheck's; `delta = 1e-3` and `0.1` rows not reproduced; b6 row corrected |

## 8. Limitations and open problems

- **No practical weight.** The result is qualitative. Proved: 1.003 per
  variable (analytic) and 1.05 (computed); 21 leaves at `n = 1000` from the
  analytic bound. Observed: about 2.85 for class (a). The loss is in the
  counting step, and exact gadget bounds on all sub-boxes cannot lift the
  tilted-volume method above about 1.063 per variable at the reference
  parameters (for class (a), 1.022–1.075 at the 19 other parameter sets of
  the scan; Sections 4.4, 6.5). A different counting argument would be
  needed.
- **Contrived family.** The family is a direct sum of three-variable gadgets
  joined by links below `1.4e-3`, with a piecewise-quadratic unary term and a
  nearly flat valley (the construction allows `eps_v` up to 0.36, at a
  smaller base). The lower bound is a product effect, not propagation along
  the path; for `delta = 0`, component detection removes it. We have no
  split-robust bound for uniform chains such as
  `sum u(x_i) + b sum x_i x_{i+1}`, and for the PROGRAM family there is
  nothing to prove (Proposition 2.1). The open question of the synthesis asks
  about the best cheap per-factor relaxations; this note answers it only for
  restricted split classes on a designed family. (*Root, 2026-10-01:*
  uniform chains are treated in [`robust-chains.md`](robust-chains.md): for
  symmetric couplings under a nondegeneracy hypothesis no split-robust bound
  growing with `n` exists for split classes that contain the balanced
  split (the unsplit factorization and `b_d` relative to the gadget base
  split of this note are not such classes), and a chiral chain gives a gadget-free
  split-robust exponential bound with similarly small bases.)
- **Strong coupling.** Lemma 4.1 needs `delta < 2 alpha` (`1.4e-3`). At
  `delta = 0.1` the minimizer moves and the counts drop (44, 108).
- **Class (b_d) needs `d`-dependent families.** For fixed data the class
  becomes exact at every gadget root for large `d` (Proposition 3.3(2));
  at the reference parameters `d = 10` suffices. For every parameter choice
  the gap is at most `2 E_d(L) = O(1/d^2)` (Proposition 3.3(3)). The
  same happens for any class whose degree grows with `n` or `1/eps`: then the
  root can be exact (compare the uniform-in-bags sparse Putinar rates of
  [`../../research-20260928/solver/sparse-putinar-exact-consistency.md`](../../research-20260928/solver/sparse-putinar-exact-consistency.md)).
  Whether some path family defeats every fixed `d` with a base independent of
  `d` is open. For the gadget chains, the base that Theorem 4.2 can prove
  tends to 1 as `d` grows (at most `exp(33.3 E_d(L))` per gadget for every
  parameter choice; Theorem 4.3(3)); whether their true tree sizes do is not
  known. Class-b6 trees grow by 2.0 per variable at the reference parameters.
- **Relaxation scope.** Covered: per-factor relaxations dominated by per-factor
  envelopes with shared univariate lifts in `S`, including per-edge PSD and RLT
  cuts on shared squares. Not covered: cuts on three or more variables,
  convexity detection of the whole objective, envelopes over the
  three-variable gadget blocks (exact here, since `g >= 0`), shared lifted
  univariate variables outside `S` (a shared lift for `h1(y)` would close the
  gadget's gap; shared lifts for `y^2` or `y^3` do not), and objective-cutoff
  propagation. For lifted relaxations with bound tightening, the tightening
  rule must be stated for that relaxation (Lemma 1.3).
- **Concave unaries.** Proposition 2.4 shows that boxes inside a concave region
  are exact. Whether concave unary terms away from `x*` can force gaps on boxes
  that straddle the convex core is not settled.
- **Numerics.** Only widest-side bisection and `n <= 9`. Every `delta = 0`
  count of classes (a), b4 and b6 (theorem's base split) was reproduced by the
  review's independent code, including `G = 3`, and the `eps = 1e-4` ones
  also by the recheck's. The `delta = 1e-3` and `delta = 0.1` rows were not
  reproduced independently. The computed constants are floating point, not
  interval arithmetic.
- **Downstream notes.** SYNTHESIS.md, Section 3 ("toy runs with the split
  factorization still grow 2.3–2.5 per variable") and face-exact Section 9.3
  (the open question for split envelopes) should cite Proposition 2.1: for
  `c = 0` the balanced split with exact envelopes solves the PROGRAM family at
  the root. This note does not edit them.
- **Review history.** Reviewed, revised, rechecked
  ([`../reviews/robust-lb-recheck.md`](../reviews/robust-lb-recheck.md): no
  mathematical error; one citation fix and several narrower wordings),
  revised again, and confirmed
  ([`../reviews/recheck-robust-lb-confirm.md`](../reviews/recheck-robust-lb-confirm.md):
  every fix applied, no mathematical error; one range wrong for odd `d` and
  a few wording points). The third revision (Section 10.3) has not been
  rechecked.

## 9. Files and commands

All commands were run from this directory with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`. They are targeted runs; no
project-wide checks were run, and no CI was consulted.

| File | Purpose |
|---|---|
| `robust_bb.py` | class bounds by column generation (Lemma 1.2), families (PROGRAM, gadget chains), B&B |
| `run_job.py`, `jobs1.txt` | one B&B job per line; `cat jobs1.txt \| xargs -P 30 -L 1 sh -c "timeout 7200 python3 run_job.py \$0 \$@"` → `logs/bb_jobs1.log` (first version; chain runs there used the balanced base split) |
| `jobs2.txt` | revision: b4, b6 and class-(a) chains with the theorem's base split (`gadget`), and one b6 run with the balanced split; same command → `logs/bb_jobs2.log` |
| `ceiling_check.py` | revision: the corner box behind the 1.063 ceiling; `python3 ceiling_check.py` → `logs/ceiling_check.log` |
| `b10_gap.py` | revision: relaxation LP for b8, b9, b10 at the gadget root; `python3 b10_gap.py` → `logs/b10_gap.log` |
| `verify_leaves.py`, `verify_split.py` | consistency checks (not certificates) of pruned leaves and split boxes; `python3 verify_leaves.py 1 a 1e-4`, `... 2 a 1e-4`, same for `verify_split.py` → `logs/verify_leaves.log` |
| `gadget_bound.py` | symmetric-fooling core gaps and the `Psi` bound (Section 4.3(b)) |
| `bound_eval.py` | Theorem 4.3(2)–(3) for the reference parameters; `python3 bound_eval.py 100` → `logs/bound_eval.log` |
| `scan_bd.py`, `jobs_scan2.txt` | parameter scan of computed bases; `cat jobs_scan2.txt \| xargs -P 8 -L 1 sh -c "python3 scan_bd.py \$0 \$@"`, plus `python3 scan_bd.py a 0.38 0.05 0.1` and `... 0.2` → `logs/scan_bd.log` |
| `constants.py` | closed-form constants, Theorem 4.3(1); `python3 constants.py` → `logs/constants.log` |
| `band_Ed.py`, `band_check.py` | `E_d(L)` lower bounds and the band form of Proposition 3.3 (revision: degrees 9, 10, 12 added) → `logs/band_Ed.log`, `logs/band_check.log` |
| `gadget_explore.py`, `designQ_gaps.py` | early design search and polynomial-design gaps (Section 6.6) → `logs/gadget_explore.log`, `logs/designQ_gaps.log` |
| `logs/program_balanced_factors.log` | grid check of Proposition 2.1 for the PROGRAM values |
| `revision2_checks.py` | second revision: exact root counting for the `gamma_10 = 0` certificate, corner-box `mu0` and ceilings for the Section 6.5 parameter sets, the uniform cap `V >= c/4` on `[-1,-1/2]^3`, `E_4(L)` at `y1 = 0.3`; `python3 revision2_checks.py > logs/revision2_checks.log` (about 1 minute) |
| `revision3_checks.py` | third revision: `E_d(L)` at `y1 = 0.38` for every `d = 2..12` (odd degrees included), corner-box `mu0` and class-(a) ceilings for all 20 parameter sets of `logs/scan_bd.log`, and the check that every minimizing `mu` there lies below `mu0`; `python3 revision3_checks.py > logs/revision3_checks.log` (about 3 seconds) |

## 10. Revision after review

### 10.1 First revision (after the review)

The review ([`../reviews/robust-lb-review.md`](../reviews/robust-lb-review.md),
checks in `../reviews/robust-lb-review-checks/`) confirmed every proof. Each
item below was checked by us before the text was changed.

1. **b6 row (review F1, required).** Rerun with the theorem's base split
   (`robust_bb.py` now has `base="gadget"`, the default for chains in
   `run_job.py`): b6 = 2, 16, 128 leaves, no unresolved boxes, the review's
   numbers. A rerun with the balanced split reproduces the old 44 at `G = 2`,
   which confirms the cause. b4 = 10, 172, 2,592 and class (a) = 600, 12,336
   (`G = 2, 3`) are unchanged under the theorem's base split
   (`logs/bb_jobs2.log`). Section 6.4 now states the base split of every row;
   the claim that b6 grows as fast as class (a) is replaced by the measured
   rates (2.00 against 2.74 per variable); the caveat about unresolved boxes is
   removed. Theorem 4.3 now states the base split for (b2), (b3) and (b_d)
   (review F2).
2. **Prior work (review F10, coordinator item 8).** New Section 1.5: Lemma 1.2
   is presented as a restatement of known duality (Falk 1974; Dür–Horst 1997;
   Nowak 2005; reparametrization and dual decomposition: Werner 2007,
   Wainwright–Jaakkola–Willsky 2005, Sontag–Globerson–Jaakkola 2011,
   Wainwright–Jordan 2008; per-node cost shifting in weighted-CSP
   branch-and-bound: Cooper et al. 2010, whose statement that VAC is applied
   "at every node of a search tree" we read in the paper; Ihler et al. 2012;
   Opper–Winther 2005; Grimm–Netzer–Schweighofer 2007). All were checked at the
   bibliographic level by web search. The review's Falk (1969) citation is
   not used as a source. (This revision said it "was not located"; that was
   wrong, and Section 10.2, item 1, corrects it.) The section states what is new: the
   restricted-class version on continuous domains and its use for node
   counts.
3. **`gamma_d` bounds (F3, coordinator item 3).** Proposition 3.3 gains item 3,
   `gamma_d <= 2 E_d(L)` and `gamma_{2k+1} = gamma_{2k}`, with proofs.
   `gamma_10 = 0` at the reference parameters was checked by the band LP
   (`band_check.py`, degrees up to 12) and by the relaxation LP (`b10_gap.py`:
   primal `0`, dual `-1.7e-11`). Sections 3.3, 3.4, 8, the Summary and
   Theorem 4.3(3) are updated.
4. **Ceiling (F4, coordinator item 6).** Section 4.4 and Section 8 now state that
   Theorem 4.2's method cannot exceed about 1.063 per variable on this gadget
   (at the reference parameters; Section 10.2, item 4),
   even with exact gadget bounds. We rechecked the review's corner box with the
   class-(a) dual bound: `V = 2.7124`, `(vol/8) exp(mu V) = 0.79, 1.04, 1.36` at
   `mu = 2.3, 2.4, 2.5` (`ceiling_check.py`). The sentence suggesting that exact
   gadget bounds might help was removed.
5. **Lemma 1.3 (F5, coordinator item 1).** Frame pieces are closed and share a
   face with the kept box. The proof now obtains `>= UBD - eps` on the closed
   piece from upper semicontinuity of convex functions on a box (Rockafellar,
   *Convex Analysis*, Theorem 10.2; checked by web search). A paragraph extends
   the argument to lifted relaxations with tightening, with the removal rule
   stated for that relaxation (F11).
6. **Proposition 2.1 (F6) and Proposition 2.3 (F7, coordinator item 2).**
   Proposition 2.1 states the incumbent requirement `UBD <= eps`. Proposition
   2.3 and the Summary now say that the impossibility concerns centered-chord
   proofs for per-factor envelopes (face-exact Theorem 2); face-exact
   Theorem 1 (termwise McCormick) is invariant under class-(a) splits.
7. **Section 5 (F8, coordinator item 5).** The 20–22 leaves per gadget are marked
   as class-(a) counts. The review's crossover estimates were rechecked by
   arithmetic (`theta = 2^-21` from (T2) with `c_g = 3.6e-4`, `M_a = 16.4`;
   size about `4e15 n`): `n ≈ 850` (computed base) and `15,000` (analytic
   base) against Theorem 3.4, `n ≈ 140` and `3,300` against gadget bags.
   Component detection for `delta = 0` is mentioned.
8. **Significance (coordinator item 7).** A plain statement after the answer in
   the Summary, and in Section 8: a qualitative robustness result with no
   practical weight at realistic `n`, built from nearly independent gadgets
   with links below `1.4e-3`.
9. **Wording (F9 and Section 4.3(b)).** "Certified" is replaced by "checked"
   for the leaf consistency check, and the `Psi` evaluation is described as a
   careful floating-point computation (one non-binding term is a fine-grid
   maximum). The review's independent reproduction of the class-(a), b4 and
   b6 counts, including `G = 3`, is recorded in Section 6.1 (it covers the
   `delta = 0` rows only; Section 10.2, item 3).
10. **Not changed here.** SYNTHESIS.md and the face-exact note should cite
    Proposition 2.1 (Section 8); editing them is outside this workstream.

Commands run for the revision (targeted; no project-wide checks, no CI):
`cat jobs2.txt | xargs -P 9 -L 1 sh -c "timeout 7200 python3 run_job.py $0 $@"`
(`logs/bb_jobs2.log`), `python3 band_check.py`, `python3 b10_gap.py`,
`python3 ceiling_check.py`.

### 10.2 Second revision (after the recheck)

The recheck ([`../reviews/robust-lb-recheck.md`](../reviews/robust-lb-recheck.md),
checks in `../reviews/robust-lb-recheck-checks/`) found no mathematical error.
It asked for one citation fix and several narrower wordings. We checked each
point before changing the text. No count or computed base changed; Lemma 1.3
was broadened and Theorem 4.3(3) gained a proved cap. (This sentence
originally read "No theorem, count or computed base changed"; Section 10.3,
item 3, corrects it.)

1. **Falk (1969) citation (R1, required).** A Crossref query for
   doi 10.1137/0307039 returns J. E. Falk, "Lagrange multipliers and
   nonconvex programs", SIAM J. Control 7(4) (1969) 534–545. So the first
   revision's "was not located" was wrong. Section 1.5 now gives the
   reference and says that its content was not checked and that it is not
   used as a source. Section 10.1, item 2, is annotated. We also re-read the
   Falk (1974) abstract on Crossref. It says the multiplier and
   convex-envelope bounds "are the same if the original problem has only
   linear constraints, or if the problem is separable with certain
   properties", which is how Section 1.5 uses it.
2. **Provable base versus tree growth (R6).** Summary item 4 and Section 8
   now say that the `1 + O(1/d^2)` statement concerns the base that
   Theorem 4.2 can prove, not the true tree sizes. They also note that
   class-b6 trees grow by 2.0 per variable. Section 8's "for the gadget
   chains it is false" is replaced by the recheck's suggested sentence.
   Theorem 4.3(3) now proves the cap for every parameter choice. On
   `[-1,-1/2]^3` all terms are nonnegative, so `V >= c/4 > 1/4` for every
   class, and `mu < 4 ln 64 ≈ 16.64`. Hence the base is at most
   `exp(16.64 gamma_d) <= exp(33.3 E_d(L))` per gadget. We checked the
   argument by hand and added one precision: the shares of `c y^2` can be
   taken nonnegative because `y^2` lies in every class considered. As an
   illustration only, `g(-1/2,-1/2,-1/2) - c/4 >= 0.755` over 20,000 random
   admissible parameter sets (`logs/revision2_checks.log`).
3. **Scope of the independent reproduction (R5).** We confirmed from the
   logs that the review's code
   (`../reviews/robust-lb-review-checks/logs/check3_bb.log`) covers only
   `delta = 0`: class (a) at `eps = 1e-2, 1e-4, 1e-6`, and b4 and b6 at
   `1e-4`. The recheck's code covers only `delta = 0` and `eps = 1e-4`. We
   narrowed the wording a little beyond the recheck's "all `delta = 0`
   counts". Neither review's own code computed the balanced-split rows (b6
   balanced; env balanced). The recheck reproduced b6 balanced `G = 2` = 44
   only by rerunning our code. The text now says "every `delta = 0` count
   of classes (a), b4 and b6 with the theorem's base split". It states that
   the `delta = 1e-3` and `delta = 0.1` rows were not reproduced
   (Summary 6, Sections 6.1, 7, 8; Section 10.1, item 9, annotated).
4. **The 1.063 ceiling holds at the reference parameters (R2).** We
   recomputed the corner-box threshold `mu0` with a different method: a
   continuous multi-start search over boxes `[-1,-a] x [-1,-b] x [-1,-c]`,
   where the recheck used a grid. We ran it for the recheck's six parameter
   sets and for the two further sets of Section 6.5 (`revision2_checks.py`).
   `mu0` agrees with the recheck to 4 digits (2.3866 against 2.3867 at the
   reference parameters). One set that the recheck did not try,
   `(0.38, 0.05, 0.2)` from Section 6.5, gives a lower cap, 1.0219 per
   variable. So the range at the other parameter sets is 1.022–1.073, not
   the recheck's 1.041–1.073. The Summary, Open, Section 4.4, Section 6.5
   (two new columns with `mu0` and the ceiling for every row), Section 7 and
   Section 8 now say "at the reference parameters" and give the range. In
   every row the computed base lies below its ceiling. Every minimizing
   `mu` in `logs/scan_bd.log` lies below the corresponding `mu0`. (At the
   time, `mu0` had been computed for only 8 of the 20 parameter sets in that
   log, so this sentence went beyond our evidence. Section 10.3, items 4
   and 6, check all 20 sets and replace the range by 1.022–1.075 for class (a).)
5. **Consistency checks (R7).** Summary item 6 now says that the leaf and
   split-box checks were done for class (a) with `G <= 2`, as
   `logs/verify_leaves.log` shows (`G = 1, 2`, `eps = 1e-4`). (It also said
   "independently", which overstated our own checks; Section 10.3, item 2,
   removes the word.)
6. **Lemma 1.3 (R3).** The statement now allows a different `r` for each
   removed point. The proof applies upper semicontinuity to
   `F = sup_{r in S} F^r_{B_k}`. This function is convex, and it is finite
   because `F^0_{B_k} <= F <= f`. The Jensen step holds for every `r` and so
   for the supremum. One `r` per round is the special case `F^r_{B_k} <= F`.
7. **Lifted relaxations (R4).** "Feasible at every point" is now "feasible
   at every point and bounded below". Bounded lifted edge sets are one
   sufficient condition. Without the lower bound, `phi_{B_k}` could be
   `-inf`, and Theorem 10.2 would not apply as stated.
8. **`gamma_10 = 0` is exact (optional).** Section 3.3 and the status table
   now cite the recheck's rational certificate `rho = y^2 q(y)`. We repeated
   the exact root counting with our own sympy code: the four defining
   polynomials have no real root on their closed intervals and are positive
   at the midpoints.
9. **`y1 = 0.3` cap (optional).** The "not checked" hedge in
   Theorem 4.3(3) is removed. Our search gives `mu0 = 2.3782` at
   `(0.30, 0.005, 0.002)`, and our grid LP gives `E_4(L) = 0.013056` at
   `y1 = 0.3` (the grid-LP lower bound and the fine-grid error of its
   polynomial agree to 6 digits; the recheck has 0.01306). This gives 1.0211 per variable
   with `2 E_4`, and 1.0198 with `gamma_4 = 0.0247`.
10. **Smaller wording (optional).** In Summary item 3, `E_d` is "of order
    `1/d^2`" with `E_d d^2` between 0.095 and 0.18 for `d = 2..12` (from
    the recheck's brackets; this range holds only for even `d`, and
    Section 10.3, item 1, corrects it), and the quantifiers now read "for each `d`,
    positive when `eps_v + eta(1-y1)^2 < 2 E_d(L)`". In Section 3.4, "narrower
    than about `E_d(L)`" is replaced by the sufficient condition "width below
    `2 E_d(L)`". Section 3.3 notes that `E_d(L) = O(1/d^2)` holds uniformly
    in `y1`. The Summary and the Section 5 status row say
    "computer-evaluated base". The header and Section 8 record the recheck.

Commands run for this revision (targeted, single-threaded; no project-wide
checks, no CI):
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 revision2_checks.py > logs/revision2_checks.log`
(about 1 minute), and two Crossref API queries
(`https://api.crossref.org/works/10.1137/0307039` and
`.../10.1287/opre.22.2.410`). No branch-and-bound run was repeated, because
no count changed. The Section 6.5 ceilings for the `b_d` rows use the rounded
gaps of Section 6.3 and `logs/scan_bd.log`.

### 10.3 Third revision (after the confirmation recheck)

The confirmation recheck
([`../reviews/recheck-robust-lb-confirm.md`](../reviews/recheck-robust-lb-confirm.md),
checks in `../reviews/recheck-robust-lb-confirm-checks/`) found every
requested fix applied and no mathematical error. It listed one wrong
numerical range, two wording points and four optional precisions. We
verified each point before changing the text. No theorem, proof, count or
computed base changed. One stated range widened slightly (item 4).

1. **Range of `d^2 E_d(L)` (confirmation 1).** `L` is even, so
   `E_{2k+1} = E_{2k}`, and the stated range 0.095–0.18 holds only for even
   `d`. Our full-basis grid LP (`revision3_checks.py`) gives `d^2 E_d` from
   0.0949 to 0.1803 for even `d = 2..12` and from 0.129 to 0.406 for odd
   `d = 3..11`. The lower bounds for `d = 2k+1` and `2k` agree to about
   `1e-8`, and the values
   match the confirmation's log. Summary item 3 and Section 3.3 now say "for
   even `d = 2, 4, ..., 12`" and state `E_{2k+1} = E_{2k}`. Section 10.2,
   item 10, is annotated. While checking this, we found that four of the six
   "lower bounds" listed in Section 3.3 had been rounded up (for example
   `E_2 >= 0.0451`, while the grid-LP value is 0.045084). They are now
   rounded down. For the same reason, Section 3.4's "at least
   `2 E_2(L) - 0.0392 = 0.051`" now reads "at least
   `2 E_2(L) - 0.03922 > 0.0509`" (the computed value is 0.05095).
2. **"Checked independently" (confirmation 2).** The leaf and split-box
   checks are our own scripts (`verify_leaves.py`, `verify_split.py`). They
   compare against a separate grid-plus-local-search estimate. Summary
   item 6 now says "both consistency-checked (not certified) for class (a)
   with `G <= 2`", and the Section 9 file table says "consistency checks
   (not certificates)" instead of "independent checks". Section 10.2,
   item 5, is annotated.
3. **Opening of Section 10.2 (confirmation 3).** The second revision
   broadened the statement of Lemma 1.3 (`r` may vary per removed point) and
   added a proved uniform cap to Theorem 4.3(3); see Section 10.2, items 6
   and 2. The opening sentence now says "No count or computed base changed;
   Lemma 1.3 was broadened and Theorem 4.3(3) gained a proved cap", with a
   note giving the old wording.
4. **Scope of the ceiling range (confirmation 4, optional).** The old range
   1.022–1.073 was the class-(a) ceiling at the seven non-reference sets
   where `mu0` had been computed. Instead of naming those seven sets, we
   computed `mu0` for all 20 distinct parameter sets of `logs/scan_bd.log`
   (`revision3_checks.py`, same Nelder–Mead search as `revision2_checks.py`).
   The class-(a) ceilings at the 19 non-reference sets range from 1.0219 to
   1.0752, with the maximum at `(0.38, 0.005, 0.002)`, as the confirmation
   found. For all 20 sets our `mu0` agrees with the confirmation's to 4
   digits. The Summary, Section 4.4, Section 6.5, the status table and
   Section 8 now say "for class (a), 1.022–1.075 at the 19 other parameter
   sets of the scan". Section 6.5 points to the log that lists the sets.
5. **Shares of `c y^2` in Theorem 4.3(3) (optional).** The text read as if
   each share were at least `c/4`. It now says that each factor is at least
   its share of `c y^2`, and that the shares add up to `c y^2 >= c/4`. The
   argument is unchanged: with nonnegative shares `s_1 + s_2 = 1` and
   `y^2 >= 1/4` on the box, the two factor minima sum to at least `c/4`.
6. **Bracket precision and the `mu < mu0` claim (optional).** The recheck's
   brackets for `E_4` and `E_8` have widths of `7e-8` and `5e-8`, and ours
   have widths up to `8e-8`. Section 3.3 now says that these brackets have
   "width at most about `1e-7`" instead of "agree to 8 digits". The review
   printed its brackets to 5 decimals only (`check5_props.log`), and the
   text now says so. The Section 10.2, item 4, claim
   that every minimizing `mu` in `logs/scan_bd.log` lies below its `mu0` was
   true but, at the time, supported for only 8 of the 20 parameter sets. It
   now holds on our own evidence for all 26 rows. The smallest margin is
   0.110 (b6 at `(0.30, 0.02, 0.002)`: `mu = 2.252`, `mu0 = 2.362`), as in
   the confirmation. Section 6.5 states this, and Section 10.2, item 4, is
   annotated.
7. **Header and Section 8.** Both now record the confirmation recheck and
   say that this third revision has not been rechecked.

The confirmation's optional remark on the balanced-split rows (listing them
with the unreproduced rows in Sections 6.1 and 8) was not applied. Those
sections already restrict the reproduction to "classes (a), b4 and b6 with
the theorem's base split", and Section 10.2, item 3, says explicitly that
neither review's own code ran the balanced-split rows.

Commands run for this revision (targeted, single-threaded; no project-wide
checks, no CI):
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 revision3_checks.py > logs/revision3_checks.log`
(about 3 seconds). We also read `../reviews/recheck-robust-lb-confirm-checks/logs/check_confirm.log`
and `../reviews/robust-lb-recheck-checks/logs/check_gamma.log` for comparison. No
branch-and-bound run was repeated, because no count changed.

*Root edit (2026-09-30, closing revision):* the header now records that
[`../reviews/robust-lb-confirm-r1.md`](../reviews/robust-lb-confirm-r1.md)
confirmed the third revision and found no remaining problem. No other text
changed.
