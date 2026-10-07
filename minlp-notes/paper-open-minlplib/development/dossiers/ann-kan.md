# Dossier: ann_cumene_tanh and the six KAN instances (family key `ann-kan`)

Prepared 2026-10-04 for the paper on certificates for open MINLPLib instances
(target: Mathematical Programming Computation). Paths without a prefix are
relative to `research-20260929/` (written R/ in the task). The authoritative
numbers are those of `open-instances-summary.md` and
`publication/integration/gap-values.json`; Section 5 rechecks them. Nothing
under R/ or literature/ was edited. All checks of this dossier ran in
disposable copies under `/tmp/annkan_dossier/` and `/tmp/annkan_dossier2/`
with at most two processes. The check scripts and their logs are saved in
`paper-open-minlplib/development/dossiers/ann-kan-checks/` (Section 8.1).

This version completes and corrects a draft left by an interrupted agent.
Corrections to that draft: the KAN rigorous-exp rerun (Section 8.3) is now
complete; the sign of the constant in the KAN scaling row is fixed
(Section 1.2); the statement that the local knowledge base has no affine
arithmetic or Taylor model source is withdrawn (Section 7); new issues
I12–I17 are added (Section 8.4).

## 0. Short version

| result | status | what it rests on |
|---|---|---|
| ann_cumene_tanh: every exactly feasible point of the OSIL model has objective ≥ L\* = −7447080719734483·2⁻⁴¹ = −3386.540229136918696895… (display −3386.5403) | computer-assisted proof; two independent bounding codes on one box partition; independently re-certified | IEEE binary64 arithmetic; correctness of either bounding code; coverage of the input box by the branch-and-bound leaves (by construction, numerically checked) |
| ann_cumene_tanh: an exactly feasible point with objective in [−3379.982394071771548095722619880929, −3379.982394071771548095722619880928] | proved; the independent review used exact rational interval arithmetic only | exact rational arithmetic |
| ann_cumene_tanh gap | ≤ 6.5579 absolute; ≤ 0.195% of \|primal\| (≤ 0.194% of \|dual\|); not closed | the two rows above |
| KAN (six models): the OSIL models have no real feasible point | proved by exact certificates; reconfirmed here with separate code | exact rational arithmetic; correct reading of the OSIL decimals |
| KAN: the minima of the relaxation R and of R_P (= OSIL model minus the partition-of-unity rows) lie in [L, U] with U − L ≤ 2.42e-8 (kan_r5_h1_n3) and ≤ 1.08e-10 (the other five) | computer-assisted; the authors' bound L is confirmed by an independent branch and bound | IEEE binary64; correctness of either of two codes (Section 3.2.4). The independent code originally assumed numpy's exp accurate to 4 ulp; this dossier reran it with a rigorous exp: same bounds for five instances, 3.2e-12 lower (still above L) for kan_r5_h1_n3 (Section 8.3) |
| KAN: points of R_P attaining U | proved; independent review in exact rational interval arithmetic | exact rational arithmetic |

No finding of this dossier invalidates a claimed number. The corrections
concern stated assumptions (one missing, two removable), the object to which
the KAN claim refers, a harmless shortcut in both ANN tanh enclosures,
reproducibility, and wording (Section 8.4).

---

## 1. Instances and models

### 1.1 ann_cumene_tanh

**Source and meaning.** Schweidtmann and Mitsos, "Deterministic global
optimization with artificial neural networks embedded", JOTA 180(3):925–948
(2019), arXiv:1801.07114v2, Section 5.4 (local copy
`literature/papers/schweidtmann2019-deterministic-global-optimization-with-artificial`).
The operating point of a cumene process (plug-flow reactor, two
rectification columns, flash, heat integration, recycles; Luyben's design)
is optimized on a hybrid model of 14 tanh multilayer perceptrons (MLPs)
that Schultz et al. trained on ASPEN Plus simulations. MINLPLib added the
instance on 2021-11-29 and cites the JOTA paper. The model is the paper's
full-space formulation ("794 variables, 789 equality and 1 inequality
constraints"), written with native tanh.

**Size and sense.** 794 continuous variables, 790 rows (789 equalities, one
inequality), no integer variables, minimization of `objvar` (the negative
total profit −P of the source).

**Decision variables and bounds.** Five inputs with finite boxes. The mapping
below matches the OSIL bounds to the bounds of the source (inferred from the
bounds, not from documentation):

| OSIL | bounds | source quantity |
|---|---|---|
| x723 | [360, 390] | reactor temperature T_reactor (°C) |
| x724 | [0.37, 1] | reflux ratio of column 1, RR_C1 |
| x725 | [1.31, 1.97] | reboiler duty of column 1, Q_reb,C1 (Gcal/h) |
| x726 | [0.85, 0.99] | distillate fraction of column 2, DF_C2 |
| x727 | [0.2, 1.2] | reflux ratio of column 2, RR_C2 |

The one inequality, row e789, is the product purity x772 ≥ 0.999.

**Structure that matters** (decoded and asserted by `open-instances-wave3/ann/ann_model.py`;
independently by the wave-3 verifier's `annv.decode`; re-run here on a copy):

- *Forward determination.* Starting from u = (x723,…,x727), 529 linear rows
  and 250 rows of the form x_v = tanh(x_s) determine 779 further variables in
  an acyclic order. 200 neurons have arguments that depend on the inputs
  only (tanh depth 1) and 50 have arguments that depend on outputs of
  depth-1 neurons (depth 2; recomputed here). The notes call these "first-"
  and "second-layer" neurons; whether a depth-2 neuron belongs to a second
  hidden layer or to an MLP fed by another MLP's outputs does not matter for
  any argument below. Each MLP maps normalized inputs through tanh neurons
  to denormalized outputs.
- *Ten remaining variables* (x754, x756, x787–x793, objvar) occur only in the
  rows e749, e750, e782–e788 and e790. All ten are free except objvar
  (bounds ±10²⁰):
  - e749: x753·x754 = x747·x748; e750: x754 + x755 + x756 + x778 = 1;
  - e782–e786: x746·x_w = Π_w for w = x787,…,x791, each Π_w a quadratic polynomial in determined variables;
  - e787: x765·x772 + x766·x792 = x760·x763; e788: x792 + x793 = 1;
  - e790: objvar = c₀ + Σ_{j∈J} a_j x_j + Σ_w c_w (x746·x_w) + c₉₂ (x766·x792) + c₉₃ (x766·x793),
    with c₀ = 10619.965999999999, six linear terms (x725, x737, x738, x739,
    x765, x770) and seven products (prices × component flows).
- *Bounds.* 728 variables have finite bounds: the 5 inputs, objvar, and 722
  determined variables. The 722 are 250 tanh outputs in [−1, 1] (never
  binding), 70 normalized MLP inputs in [−1, 1] (the training domain), 380
  with ±10⁶ and 22 with [−10⁹, 10⁶]. At the best known point two
  constraints are active: x772 ≥ 0.999 and the training-domain bound
  x647 ≥ −1 (with its copies x590, x701).

**Reduced model.** Let U ⊂ ℝ⁵ be the input box and x(u) the forward map.
Substituting the product identities x746·x_w = Π_w(x(u)),
x766·x792 = x760·x763 − x765·x772 and x766·x793 = x766 − x766·x792 (e788
multiplied by x766) into e790 gives an explicit function

  f(u) = c₀ + Σ_{j∈J} a_j x_j(u) + Σ_w c_w Π_w(x(u)) + c₉₂ (x760 x763 − x765 x772)(u) + c₉₃ (x766 − x760 x763 + x765 x772)(u).

f is a quadratic polynomial in the determined variables. The relaxation used
by every bound is

  R = { u ∈ U : ℓ_v ≤ x_v(u) ≤ υ_v for the 722 bounded determined variables v, x772(u) ≥ 0.999 }.

R drops e749, e750 and the solvability of the product rows (the dropped
variables are free and occur nowhere else) and the objvar bound ±10²⁰.
Lemma A.1 below shows that R contains the projection of the OSIL feasible
set and that the objective agrees, so min_R f ≤ OPT(OSIL). The two sets
differ only where a divisor x753, x746 or x766 vanishes with a nonzero
right-hand side.

**Provenance.** MINLPLib's `ann_cumene_exp` is the same problem with −tanh(v)
written as 2/(exp(2v)+1) − 1 and the row bounds shifted by exactly 1. This
was proved by exact comparison of the two OSIL files
(`publication/literature/network/checks/cumene_twin_exact.py`; independently
`publication/reviews/lit-network-r1/cumene_twin.py` and `cumene_twin_r2.py`):
variables, bounds, objective and all other coefficients are identical. Hence
every statement below about ann_cumene_tanh (dual bound and primal point)
holds verbatim for ann_cumene_exp. The OSIL file is sha256-identical to the
current MINLPLib file (status refresh 2026-10-02). The GAMS form was compared
with the OSIL form only numerically (rows equal at 50-digit sample points,
`publication/minlplib-status`), not exactly. The arXiv text (Table 4) and the
2021 dissertation (Table 2.8; local copy
`schweidtmann2021-global-optimization-of-processes-through`) report different
MAiNGO numbers for the same problem; the JOTA publisher table was not checked.

### 1.2 The six KAN instances

**Source and meaning.** Karia, Lastrucci and Schweidtmann, "Deterministic
global optimization over trained Kolmogorov Arnold networks", arXiv:2503.02807v1
(2025), supplement Zenodo 14961066 (local copies
`karia2025-deterministic-global-optimization-over-trained`,
`karia2025-karia-et-al-zenodo-default`). Each instance minimizes a trained
Kolmogorov–Arnold network (KAN) that is a surrogate of the Rosenbrock function
in 3 (r3) or 5 (r5) dimensions, f(x) = Σ_{i<d} [100(x_{i+1} − x_i²)² + (1 − x_i)²]
on [−2.048, 2.048]^d. MINLPLib added them on 2025-05-07. Each MINLPLib model
is the paper's "Default" formulation; the variable and row counts match the
Zenodo sheets exactly. Sanity check: mapped to the Rosenbrock domain
through each input's scaling row, the best point of kan_r5_h1_n8 is
x ≈ (1.006, 1.012, 1.024, 1.049, 1.103) and that of kan_r3_h1_n4 is
x ≈ (0.987, 0.974, 0.949), near the Rosenbrock minimizer (1,…,1)
(recomputed here). The three-neuron surrogate kan_r5_h1_n3 is poor: its
minimum −262.86 lies at x ≈ (0.51, 0.79, 0.64, 0.26, −0.77).

| instance | KAN | variables (binary) | rows | edges | knot intervals per edge | partition rows |
|---|---|---|---|---|---|---|
| kan_r3_h1_n4 | [3, 4, 1] | 1129 (288) | 1478 | 16 | 18 | 48 |
| kan_r3_h1_n5 | [3, 5, 1] | 1410 (360) | 1847 | 20 | 18 | 60 |
| kan_r3_h1_n9 | [3, 9, 1] | 2534 (648) | 3323 | 36 | 18 | 108 |
| kan_r5_h1_n3 | [5, 3, 1] | 838 (216) | 1121 | 18 | 12 | 54 |
| kan_r5_h1_n5 | [5, 5, 1] | 1392 (360) | 1867 | 30 | 12 | 90 |
| kan_r5_h1_n8 | [5, 8, 1] | 2223 (576) | 2986 | 48 | 12 | 144 |

All six minimize. Row classes of kan_r3_h1_n4 (verifier's decoder): 800
recursion, spline-sum and edge rows; 576 big-M; 48 partition; 16 one-hot; 16
SiLU; 13 copy; 5 sum; 3 scaling; 1 objective. In every instance, rows =
(definition rows) + (big-M rows, 2 per knot interval per edge) + (partition
rows, 3 per edge) + (one-hot rows, 1 per edge); e.g. 1478 = 838 + 576 + 48 + 16.

**The network.** With d inputs and n hidden neurons, every edge function is

  φ_e(z) = w^s_e S_e(z) + w^b_e silu(z),  S_e(z) = Σ_m c_{e,m} B_{e,m}(z),  silu(z) = z/(1 + e^{−z}),

a cubic B-spline on a uniform grid extended by three knots on each side
(r3: 12 grid intervals, 18 knot intervals; r5: 6 and 12). Hidden values
h_j = β_j + Σ_i φ_{ij}(u_i), output y = β₀ + Σ_j ψ_j(h_j) with ψ_j = φ_{(j,out)},
objective A·y + B with A = 970.2191877107767, B = 981.2776620620748 (r3) and
A = 1439.6298856740555, B = 1975.955959593862 (r5).

**MINLP encoding (Default formulation).** For each edge e with argument
variable z_e:

- binaries b_{e,1},…,b_{e,K} with one-hot row Σ_k b_{e,k} = 1;
- big-M rows c_k b_{e,k} − z_e ≤ M₁ and d_k b_{e,k} + z_e ≤ M₂, which force
  z_e ∈ I_{e,k} = [lo_{e,k}, hi_{e,k}] when b_{e,k} = 1 (the first lower and
  last upper rows carry no binary);
- Cox–de Boor rows, bilinear in binaries or lower-order bases and z_e, e.g.
  B_{m,1} = b_m(α_m + β_m z) + b_{m+1}(γ_m + δ_m z), and products B·z for
  degrees 2 and 3;
- partition-of-unity rows Σ_m B_{e,m,p} = 1 for p = 1, 2, 3;
- a spline-sum row, a SiLU row s_e = z_e/(1 + exp(−z_e)) and an edge row
  φ_e = w^s S_e + w^b s_e;
- copy rows (each edge has its own argument variable), scaling rows such as
  −x777 + 1.1796167609850992·x776 = −0.003910886333986257, i.e.
  x777 = 1.1796167609850992·x776 + 0.003910886333986257 with x777 ∈ [−2.048, 2.048]
  (x777 is the Rosenbrock coordinate), neuron-sum rows, the output row and
  the objective row.

**Why the partition rows are redundant in exact B-spline arithmetic.** For
exact cubic B-splines on the knots t₀ < … < t_K, Σ_m B_{m,p}(z) = 1 holds
identically for z ∈ [t_p, t_{K−p}], p = 1, 2, 3. The admissible arguments of
every edge lie in [t₃, t_{K−3}] (the input and hidden class boxes below are
this interval or a subinterval). So the partition rows are valid identities
of the exact network; they fail in the stored models only because the
recursion coefficients are 16-digit decimals (Proposition K.1). This is the
reason to state the KAN result for the model without them (R_P below).

**Determination.** With the inputs u and one knot interval k_e per edge fixed,
every equality row other than the partition rows can be solved for a single
unknown that enters linearly with a constant coefficient. So (u, k) determines
the whole point, and on a fixed interval each edge value is
φ_e(z; k) = w^s_e P_{e,k}(z) + w^b_e silu(z) with an exact rational cubic
P_{e,k} ("the model's piece").

**Boxes.** The *input class* Z_i is the intersection of the bounds of u_i,
its copies and its scaled copy; e.g. Z₂ = [−1.765937837439145, 1.6965037602019237]
for kan_r3_h1_n4 (own bounds of x1076: [−1.7755611391195993, 1.7043644849628665])
and Z₁ = [−1.7394724746200056, 1.7328417001798049] for the r5 models. The
*hidden class* H_j = [L_j, U_j] is the intersection of the bounds of h_j and
its layer-2 copy; it equals [t₃, t_{K−3}] of the layer-2 grid,
e.g. H₂ = [0.7032, 1.7346] for kan_r5_h1_n3 (the hidden variable alone has
[0.6661, 1.7346]).

**The two relaxations.**

- R (wave 3; verified): the OSIL model without the partition-of-unity rows
  and without the bounds on basis, spline, edge-output and output variables
  (and the inactive SiLU lower bound −0.278464596867598). It keeps the
  one-hot and big-M rows, the recursion, SiLU, edge, copy, scaling and sum
  rows, and the input- and hidden-class bounds. In reduced form,

  R = { (u, k) : u ∈ Z, z_e ∈ I_{e,k_e} for every edge e, h_j(u, k) ∈ H_j },  F(u, k) = A(β₀ + Σ_j ψ_j(h_j; k)) + B.

  Different edges of the same input have their own binaries, so in the
  overlap of two big-M intervals they may choose different pieces; R allows
  every such choice.
- R_P (proposed here): the OSIL model without the partition-of-unity rows
  only. Every point of R_P projects to a point (u, k) of R with the same
  objective (the one-hot, big-M and definition rows of R_P give k, z ∈ I_k
  and obj = F(u, k)), so min_R F ≤ min R_P. Section 8.4 (issue I4) explains
  why the paper can state the KAN result for R_P.

**Provenance and model issues.**

- The MINLPLib models are exact matches of the Default formulation of the
  source (counts in the Zenodo sheets). The source's SCIP runs used gap
  tolerance 0 and a 2-h limit; the 1e-6 feasibility tolerance is inferred
  from the logs, not stated in the paper.
- The coefficients are decimal roundings of the trained network. In exact
  arithmetic, the partition-of-unity rows are polynomial identities only up
  to residuals of order 10⁻¹⁷–10⁻¹⁵. This makes all six OSIL models infeasible
  (Proposition K.1). MINLPLib judges feasibility with tolerances, so its
  listed points remain legitimate in its own convention (they violate the
  partition rows by about 1e-15 and, for some points, other rows by up to
  9.0e-11).
- Big-M intervals of neighbouring knots overlap by up to 7e-16 or leave gaps
  up to 1.5e-15; all bounds below cover every admissible knot choice.
- The GAMS text was compared with the OSIL form only numerically (rows equal
  at 50-digit sample points, `publication/minlplib-status`). The exact
  infeasibility proof is for the OSIL decimals.

---

## 2. Listed status (MINLPLib pages fetched 2026-09-29; unchanged on 2026-10-02)

| instance | listed primal (point) | best listed dual (solver, date) | other listed duals | solved mark |
|---|---|---|---|---|
| ann_cumene_tanh | −3379.982394 (p1, infeas 2e-12, 2021-11-30) | none | none | open |
| (twin ann_cumene_exp) | −3379.982394 (p1, infeas 2e-10) | −3379.982394 (SCIP), −3379.982394 (LINDO), both 15 Feb 2022 | BARON −3379.985774 (31 Jul 2025), ANTIGONE −73920.54157 | — |
| kan_r3_h1_n4 | 0.00278124 (p1) | 0.0003908 (GUROBI, 2025-08-07) | SCIP 0.00030902, BARON −68.849874, XPRESS −69.02574609, ANTIGONE −216.8047332, LINDO −291.7075683 | open |
| kan_r3_h1_n5 | −0.01104268 (p2) | −0.01302849 (GUROBI) | SCIP −0.013472, LINDO −27.143612, BARON −41.707441, XPRESS −42.657827 | open |
| kan_r3_h1_n9 | 0.01296366 (p3) | 0.0081425 (GUROBI) | LINDO −95.113498, XPRESS −107.44524, SCIP −116.643412, BARON −192.886834 | open |
| kan_r5_h1_n3 | −262.3058993 (p2) | −789.740197 (GUROBI) | XPRESS −3447.844404, SCIP −5484.335905, BARON −23358.99071, SHOT −25573.03029 | open |
| kan_r5_h1_n5 | 0.27265451 (p2) | 0.26787523 (GUROBI) | SCIP −4.730063, BARON/LINDO/XPRESS −10.804775 | open |
| kan_r5_h1_n8 | 0.36062128 (p3) | −45.00462396 (GUROBI) | XPRESS −134.707683, LINDO −140.61921, SCIP −178.913917, BARON −185.911574 | open |

Sources: `open-instances-scout/fetched.csv`, `publication/minlplib-status/data/bounddates.json`
and `data/tables.md`, saved pages in `publication/literature/network/sources/minlplib_pages_20261001/`
(rechecked here). The BARON/LINDO/XPRESS value −10.804775 on kan_r5_h1_n5 is
close to the trivial bound A(β₀ + Σ_j min_{H_j} ψ_j) + B = −10.812 that
treats the hidden neurons as independent (wave-3 report, Section 2.4).

---

## 3. The certificates

### 3.1 ann_cumene_tanh: rigorous dual bound

**Idea in plain words.** All but ten of the 794 variables, and the objective,
are explicit functions of the five inputs. We split the 5-dimensional input
box into about 1.85 million sub-boxes. On each sub-box we write every
variable as an affine function of 255 symbols in [−1, 1] plus a small
remainder: five symbols for the inputs and one symbol for the linearization
error of each of the 250 tanh neurons, shared by all variables that depend
on that neuron (affine arithmetic). Shared symbols let linearization errors
cancel in the objective and in the constraints. The objective is then
bounded below by a weak-duality (Lagrangian) argument over the cube
[−1, 1]²⁵⁵, with multipliers on the bounds of R taken from any LP solver and
evaluated with outward rounding. A box is discarded if this bound exceeds
the target or if the constraints cannot hold on it.

**Lemma A.1 (reduction).** If x is an exactly feasible point of the OSIL
model, then u = (x723,…,x727) ∈ R, the determined coordinates of x equal x(u),
and objvar = f(u).

*Proof.* The forward rows have exactly one unknown each when processed in the
decoded order, and that unknown enters linearly with a nonzero constant
coefficient or, for tanh rows, as x_v = tanh(x_s); so the determined
coordinates of a feasible x equal x(u). The bounds of x restricted to the
determined variables and row e789 are the constraints of R. Rows e782–e786
give x746·x_w = Π_w(x(u)); e787 gives x766·x792 = x760x763 − x765x772; e788
multiplied by x766 gives x766·x793 = x766 − x766·x792. Substituting these
products into e790 yields objvar = f(u). (No division is used, so the lemma
holds also where x746 or x766 vanishes.) ∎

**Theorem A.2.** f(u) ≥ L\* := −7447080719734483·2⁻⁴¹ = −3386.540229136918696895… for every u ∈ R.
Consequently OPT(ann_cumene_tanh) = OPT(ann_cumene_exp) ≥ L\*.

The proof is computer-assisted. It has three parts: a covering of U by
boxes, a per-box inequality (Lemmas A.3–A.5) and its rigorous evaluation.

**Covering.** The branch and bound (`ann_tm.py`; run 1 = `ext_logs/ann_tm_v1_snapshot.py`
for 1800 s from U; run 2 = `ann_tm.py` with settings `sep-gradsmall`,
resumed from the 111,474 run-1 frontier boxes for 5400 s) starts from the
outward binary64 enclosure of U and processes boxes Q in three ways:
(a) Q is closed; (b) Q is bisected at a binary64 midpoint of one coordinate,
Q = Q′ ∪ Q″; (c) interval propagation shrinks Q to Q_red, and Q \ Q_red is
contained in the union of at most ten slab boxes S_i, so
Q = Q_red ∪ S₁ ∪ … ∪ S_m. By induction over the tree, U is contained in the
union of the leaves: 1,644,110 closed regions (closed boxes and slabs:
278,495 = 212,092 + 66,403 in run 1, 1,365,615 = 899,981 + 465,634 in run 2)
and the 208,223 final open boxes (`ext_logs/open_run2.npz`). The review
replayed both runs deterministically, reproduced every log line and both
saved frontiers bit for bit, extracted every closed region, and checked the
covering numerically: total volume equal to the start volume to 12 digits in
both runs, and 4000 random points each in exactly one region. These checks
test the implementation; the covering itself follows from (a)–(c).

**Lemma A.3 (affine forms with shared noise symbols).** Let
B = {m + diag(h)ξ : ξ ∈ [−1, 1]⁵} contain a leaf box. There are reals
C_v, vectors A_v ∈ ℝ²⁵⁵ and radii r_v ≥ 0, for every determined variable v
and for v = f, and for every u ∈ B a vector ξ(u) ∈ [−1, 1]²⁵⁵, such that

  |x_v(u) − C_v − A_v·ξ(u)| ≤ r_v  and  |f(u) − C_f − A_f·ξ(u)| ≤ r_f.

*Construction.* ξ_i(u) = (u_i − m_i)/h_i for i ≤ 5. A linear row
x_v = Σ_k w_k x_k + b gives C_v = Σ w_k C_k + b, A_v = Σ w_k A_k,
r_v = Σ |w_k| r_k. For tanh neuron n with argument x_s, the form of x_s gives
an interval [l_n, t_n] = [C_s − ‖A_s‖₁ − r_s, C_s + ‖A_s‖₁ + r_s] ⊇ {x_s(u) : u ∈ B};
Lemma A.5 gives α_n, β_n, δ_n with |tanh(s) − α_n s − β_n| ≤ δ_n on [l_n, t_n].
Put ξ_{5+n}(u) = (tanh(x_s(u)) − α_n x_s(u) − β_n)/δ_n ∈ [−1, 1] (ξ_{5+n} = 0
if δ_n = 0); then C_v = α_n C_s + β_n, A_v = α_n A_s + δ_n e_{5+n},
r_v = |α_n| r_s. This needs (A_s)_{5+n} = 0, which holds because neuron n is
not upstream of its own argument (asserted in both codes). For a product of
two forms, (C_p + A_p·ξ ± r_p)(C_q + A_q·ξ ± r_q) ⊆ C_pC_q + (C_pA_q + C_qA_p)·ξ
± (|C_p| r_q + |C_q| r_p + (‖A_p‖₁ + r_p)(‖A_q‖₁ + r_q)); the reviewer's code
uses the sharper split (A_p·ξ)(A_q·ξ) = ½Σ_i A_{p,i}A_{q,i} + N with
|N| ≤ ‖A_p‖₁‖A_q‖₁ − ½Σ_i |A_{p,i}A_{q,i}| (since ξ_i² ∈ [0, 1]). In floating
point, every computed C and A entry is a binary64 number, and a bound on
every rounding error is added to the radius. ∎

The point of the construction is that neuron n contributes the same symbol
ξ_{5+n} to every variable downstream of it. A per-variable remainder would add
the 250 linearization errors in absolute value; the shared symbol lets them
cancel. On boxes of relative width 0.001 near the optimum, the median gap
between the box bound and f\* fell from 2.06 (interval and mean-value forms
of wave 3) to 0.294 (one remainder per variable) and 0.0866 (shared symbols)
(`ann/extension.md`, Section 2.2).

**Lemma A.4 (weak duality over the cube).** Write the constraints of R as
σ_j (x_{v_j}(u) − b_j) ≥ 0, σ_j ∈ {+1, −1}. For every μ ∈ ℝ^J with μ ≥ 0 and
every u ∈ B ∩ R,

  f(u) ≥ Φ(μ) := C_f − r_f − Σ_j μ_j (σ_j (C_{v_j} − b_j) + r_{v_j}) − ‖A_f − Σ_j μ_j σ_j A_{v_j}‖₁.

If some μ ≥ 0 satisfies Σ_j μ_j (σ_j(C_{v_j} − b_j) + r_{v_j}) + ‖Σ_j μ_j σ_j A_{v_j}‖₁ < 0,
then B ∩ R = ∅.

*Proof.* By Lemma A.3, 0 ≤ σ_j(x_{v_j} − b_j) ≤ σ_j(C_{v_j} − b_j) + σ_j A_{v_j}·ξ + r_{v_j}
and f ≥ C_f + A_f·ξ − r_f. Subtracting the μ-weighted constraint terms gives
f ≥ C_f − r_f − Σ_j μ_j(σ_j(C_{v_j} − b_j) + r_{v_j}) + (A_f − Σ_j μ_j σ_j A_{v_j})·ξ ≥ Φ(μ),
since |ξ_i| ≤ 1. The second claim follows the same way from
0 ≤ Σ_j μ_j σ_j(x_{v_j} − b_j). ∎

Φ(μ) is a valid bound for every μ ≥ 0. So μ may come from any untrusted
solver (HiGHS in the review; enumeration of 3×3 vertex systems over the three
most violated "sides" in the authors' code); rigor comes only from
evaluating Φ(μ) with outward rounding. This is the safe-LP-bound principle of
Neumaier and Shcherbina (2004). Dropping constraints (the authors use only
sides with |b_j| < 10⁵ on non-tanh variables) only weakens the bound.

**Lemma A.5 (linear enclosure of tanh).** Let [l, t] be an interval and
α ∈ [0, 1]. Then g(s) = tanh(s) − αs is convex on (−∞, 0] and concave on
[0, ∞) (tanh″ = −2 tanh·sech²). On the convex piece, max g is attained at an
end point and g ≥ g(p) + g′(p)(s − p) for any p in the piece, whose minimum is
at an end point; symmetrically on the concave piece. If
α ≤ min(tanh′(l), tanh′(t)) = min_{[l,t]} tanh′ (sech² is unimodal), g is
nondecreasing and g([l, t]) = [g(l), g(t)]. Either way g([l, t]) ⊆ [g_min, g_max]
with g_min, g_max computed from finitely many values of tanh and tanh′; then
β = (g_min + g_max)/2 and δ = (g_max − g_min)/2. ∎

The reviewer's code uses a different valid argument: it splits [l, t] at 0
and near the stationary points ±s₀ of g, uses that g′ = sech² − α is monotone
on each piece within s ≤ 0 or s ≥ 0, places the extremes at end points where
g′ has a proven constant sign, and otherwise uses the crude enclosure
[tanh(a) − αb, tanh(b) − αa] (valid because α ≥ 0, which the code enforces by
clipping α to [0, 1]).

**Proof of Theorem A.2.** Let B be any leaf. The independent code
(`reviews/ann-extension-review-checks/annx.py`) computes the forms of Lemma A.3
without clipping, collects every bound of R that the affine range can violate,
obtains μ from an LP over all 255 symbols (elastic LP if infeasible), and
evaluates Φ(μ) in outward-rounded interval arithmetic. If Φ(μ) < L\* and B is
not proved empty, it bisects B along its relatively widest input and repeats
(at most 4000 nodes). For all 1,852,333 leaves the result was "f ≥ L\* on
B ∩ R" (one shot or after subdivision: 1,512 run-1 regions needed
subdivision, at most 223 nodes; 173 run-2 regions, at most 21 nodes; 5 open
boxes, at most 3 nodes). A NaN bound counts as "not proved" in this code
(`lb >= target` is false), so NaN cannot produce a false proof. With the
covering this gives f ≥ L\* on R. ∎

**Second, independent proof of the same leaves.** The authors' code closed
every closed region during the search with its own bound (`fbound_combo`:
the Lemma A.3 forms, also with one lumped remainder per variable, Lemma A.4
with up to three sides, the wave-3 interval passes on boxes wider than 1/16,
clipping that is valid at feasible points, and an objective cut that removes
only points with f > UB ≥ L\*). The final open boxes carry the authors' lower
bounds as keys, and the least key is L\*. The authors' certified value is
min(closed minimum, least open key, UB) = min(−3379.985488216472,
−3386.5402291369187, UB) = L\*. The independent reviewer read `ann_tm.py`,
`tm1.TM` and the wave-3 passes in full and found no rigor error. So every
leaf has two independent proofs, and L\* stays valid if either code is
correct (given the covering).

**What the computation checks, in what arithmetic, and what must be trusted.**

- Arithmetic: IEEE-754 binary64 in numpy/scipy, round to nearest, with
  directed steps by `np.nextafter`. The authors bound every rounding error
  by γ_n = nu/(1 − nu), u = 2⁻⁵³, valid for any summation order and with or
  without fused multiply-add, and inflate radii by (1 + γ_{2k+20}); the
  reviewer adds a relative slack τ = 10⁻¹² per operation (≥ 30× the γ_n of any
  sum used, n ≤ 260, applied to sums of absolute values, so cancellation is
  covered; it also covers the representation error of the decimal
  constants). Both assume the default floating-point environment (no
  flush-to-zero).
- Transcendentals: no libm result is trusted. tanh(s) = 1 − 2/(e^{2|s|} + 1)
  (sign-symmetric) with exp enclosed from +, −, ×, ÷ only. Authors:
  `kan_iv.iexp_pt_fast`, a 64-entry table of exp(j·ln2/64) computed with
  50-digit mpmath and widened by one ulp, a degree-8 Taylor polynomial on
  |r| ≤ 0.0055 with remainder ≤ 10⁻²⁵, and exact scaling by 2^k. Reviewer:
  own exp, argument reduction with an outward enclosure of ln 2, a
  degree-22 Taylor polynomial with remainder ≤ 10⁻³⁰. The mpmath-derived
  constants (both ln 2 enclosures and all 64 table entries) and the three
  remainder constants were rechecked here in exact rational arithmetic
  (`ann-kan-checks/check_constants.py`), so mpmath need not be trusted.
- Saturated tanh: both codes return the enclosure [1, 1] for tanh(z),
  z ≥ 300 (and [−1, −1] for z ≤ −300), which misses the true value by less
  than 2e^{−600} < 6·10⁻²⁶¹. Section 8.2 proves that the next outward-rounded
  operation always absorbs this; issue I12.
- Model reading: the reviewer's decoder (`annv.decode`, written by the wave-3
  verifier) and the authors' decoder agree on the input box, the 723
  constraint bounds, all 779 forward rows as exact rationals, and the
  objective (difference 3.3e-47 at 20 random points at 50 digits).
- Coverage: by construction (a)–(c), numerically checked as stated.
- Trusted code: `annx.py` (446 lines) was tested by its author only (5007 tanh
  points, 1304 linearization intervals including extreme ones, forward pass at
  21 points, 15,201 sampled feasible points in 250 boxes with 0 violations);
  `ann_tm.py` (1118 lines) was read in full by the reviewer. This dossier
  read the rounding, tanh, product, objective and dual-value parts of
  `annx.py` and found them correct (Section 8.2).

### 3.2 KAN: exact infeasibility of the OSIL models and enclosure of min R

#### 3.2.1 Exact infeasibility

**Proposition K.1.** None of the six OSIL models kan_r3_h1_n{4,5,9} and
kan_r5_h1_n{3,5,8} has a real point satisfying all its rows, bounds and
integrality requirements.

*Idea.* On each knot interval, the partition-of-unity rows of an edge become
polynomial identities in the edge argument z. With exact decimal coefficients
they fail by about 10⁻¹⁷–10⁻¹⁵, so they hold only at isolated z, or nowhere.
For one edge, no z in its feasible range satisfies all three rows on any
interval.

*Proof.* Fix the edge e\* listed below and a feasible point. The one-hot row
and binarity give a unique k with b_{e\*,k} = 1, and the big-M rows give
z ∈ I_{e\*,k}; the input-class bounds give z ∈ Z_i. With b = e_k, each
Cox–de Boor or product row of e\* (processed degree by degree) has exactly
one unknown variable, entering linearly with a nonzero constant coefficient,
so the basis variables equal polynomials B^{(k)}_{m,p}(z) with rational
coefficients, and the partition rows require
ρ^{(k)}_p(z) := Σ_m B^{(k)}_{m,p}(z) − 1 = 0 for p = 1, 2, 3. For every k with
I_{e\*,k} ∩ Z_i ≠ ∅, exact computation over ℚ shows that ρ^{(k)}_1, ρ^{(k)}_2,
ρ^{(k)}_3 have no common zero in I_{e\*,k} ∩ Z_i: either one of them has no
root there (Sturm count) or two of them have no common complex root
(nonzero resultant; equivalently, the gcd of the nonzero residuals is
constant). The rows involved belong to e\* alone, so the conclusion holds
whatever the other edges choose. ∎

| instance | edge e\* (input) | admissible pieces | complete single-edge certificates (verifier) |
|---|---|---|---|
| kan_r3_h1_n4 | x1076 (input 2) | 12 | 4 of 12 layer-1 edges (all edges of input 2) |
| kan_r3_h1_n5 | x1344 (input 2) | 12 | 5 of 15 |
| kan_r3_h1_n9 | x2416 (input 2) | 12 | 9 of 27 (and 1 of 9 layer-2) |
| kan_r5_h1_n3 | x776 (input 1) | 6 | 15 of 15 (and 2 of 3 layer-2) |
| kan_r5_h1_n5 | x1292 (input 1) | 6 | 25 of 25 (and 3 of 5) |
| kan_r5_h1_n8 | x2066 (input 1) | 6 | 40 of 40 (and 7 of 8) |

*Worked example* (kan_r5_h1_n3, edge x776, the knot interval selected by
binary b6, z ∈ [−0.585776, −0.004016]; the verifier's 0-based "piece 5").
With b6 = 1 the rows e48 and e49 give
x221 = −0.006902393224744528 − 1.718920732397047 z and
x222 = 1.0069023932247445 + 1.718920732397047 z; the other degree-1 bases
vanish. Hence ρ₁ ≡ x221 + x222 − 1 = −2.8·10⁻¹⁷ (exactly
1.0069023932247445 − 0.006902393224744528 − 1), a nonzero constant, and the
partition row e77 cannot hold. On the intervals of b6–b9, ρ₁ is a nonzero
constant; for b4 and b5 the degree-2 and degree-3 rows are needed (b4: ρ₁ ≡ ρ₂ ≡ 0
and ρ₃ has no root in the interval; b5: ρ₂ and ρ₃ have no common root). For
the r3 edges, the first admissible interval (b22 for x1076; the verifier's
piece 3) needs the scaled-copy bound (x1077 ∈ [−2.048, 2.048]): with the
argument's own bounds only, the degree-2 and degree-3 residuals of that
interval (rows e197, e198; both linear in z, coefficients about 3·10⁻¹⁵) are
proportional and vanish at the argument's own lower bound
z = −1.7755611391195993 (the boundary knot t₃); the scaled-copy bound gives
z ≥ −1.765937837439145 and excludes this root (Section 8.2).

#### 3.2.2 Statement of the enclosure

**Theorem K.2.** For each instance and the numbers L, U of Section 5,

  L ≤ min_R F ≤ min_{R_P} obj ≤ U.

The minima exist: for each of the finitely many knot choices k, the set
{u ∈ Z : z_e(u) ∈ I_{e,k_e}, h_j(u, k) ∈ H_j} is compact (h is continuous in u
for fixed k) and F is continuous on it. R_P is nonempty (Section 4.2), and
for each knot choice its points are the image of a compact set of inputs
under a continuous map, so min R_P is attained as well. *Proof.* (a) L ≤ min_R F is the
computer-assisted bound of Section 3.2.3. (b) U is the upper end of an
enclosure of the objective at a point of R_P (Section 4.2). (c) Every point of
R_P projects into R with the same objective (Section 1.2). ∎

**Corollary.** Every point of R_P, in particular every point that satisfies
all OSIL rows except the partition rows and all bounds and integrality
requirements, has objective ≥ L. The OSIL problem itself is infeasible
(Proposition K.1), so its optimal value is +∞ and every number is a vacuous
dual bound for it.

#### 3.2.3 The bound L ≤ min_R F

**Idea.** All variables are determined by the d inputs and the knot
intervals. A branch and bound over the input box Z (3 or 5 dimensions)
bounds F on each box for every admissible choice of knot intervals at once,
using interval enclosures and second- and third-order Taylor-type forms of
the composed network.

Two implementations exist.

**(I) Independent implementation, on the model's own pieces**
(`reviews/wave3-verification/kan_bnb.py`, 756 lines; own decoder
`kan_decode.py`). For a box B ⊆ Z, LB(B) is valid for all (u, k) ∈ R with
u ∈ B. It is the maximum of:

- LB1: natural interval enclosure with the hull over admissible pieces
  (Taylor ranges of each cubic piece intersected with mean-value forms) and
  h_j ∩ H_j;
- LB2: a second-order form ψ_j(h) ≥ ψ_j^{k₀}(ĥ_j) + D_j(h − ĥ_j) − pen_j around
  ĥ_j = h_j(centre) with a reference piece k₀, where D_j encloses ψ_j^{k₀}′ on
  hull(H_j, ĥ_j) (or, per neuron, ψ_j^{k₀}′(ĥ_j)(h − ĥ_j) + min(m_j, 0)(h − ĥ_j)²/2
  with m_j ≤ ψ_j^{k₀}″); pen_j bounds |P_k − P_{k₀}| exactly from knot-difference
  polynomials where arguments cross knots; the linear part splits into 1-D
  quadratics per input, minimized exactly;
- LB3: a third-order form V(c) + g·s + ½sᵀH_m s − g_r·r − ½rᵀ Rad r − penalties,
  where Rad bounds |H(ξ) − H_m| on the box, used only when H_m is positive
  definite, proved per box by an exact rational LDLᵀ, with ½gᵀH_m⁻¹g computed
  exactly.

Best-first search, bisection of the widest coordinate, a box discarded when
LB ≥ UB − tol (tol = 4·10⁻¹¹·max(1, |UB|)); final value
L_ver = min(UB − tol, min of open LB). This is valid whatever UB is: a point
in a discarded box has F ≥ UB_then − tol ≥ UB_final − tol ≥ L_ver. The
start box is the outward binary64 enclosure of Z; piece admissibility uses
outward enclosures of the big-M intervals.

**(II) Authors' implementation, through the ideal network**
(`open-instances-wave3/kan/kan_bb.py`, `kan_model.py`, `kan_iv.py`,
`open-instances-wave3/bbcore.py`). It bounds the exact C² cubic spline network
and subtracts an explicit perturbation term.

*Lemma K.3 (perturbation).* Let S̃_e be the exact C² cubic B-spline with the
decoded knots (t₀ = −M₁, t_k = lo_{e,k+1}, t_K = M₂) and the model's
coefficients c_{e,m}, and ψ̃_j, f̃ the corresponding ideal edge functions and
network. Let ε_e ≥ max over admissible k and z ∈ I_{e,k} ∩ (class box) of
|P_{e,k}(z) − S̃_e(z)|, computed exactly in rationals (Taylor shift and
Σ|c_k|w^k), η_j = Σ_i |w^s_{ij}| ε_{ij}, δ_j = |w^s_j| ε_j (layer 2), and
Lip_j ≥ max |ψ̃_j′| on [L_j − η_j, U_j + η_j] (4000-cell interval subdivision).
Then for every (u, k) ∈ R: |h_j − h̃_j(u)| ≤ η_j, h̃_j(u) ∈ [L_j − η_j, U_j + η_j],
and F(u, k) ≥ f̃(u) − Δ with Δ = |A| Σ_j (δ_j + Lip_j η_j).

*Proof.* The SiLU parts of the model and of the ideal edge coincide, so
|φ_{ij}(u_i; k) − φ̃_{ij}(u_i)| ≤ |w^s_{ij}| ε_{ij}, and summing over i gives the
bound on h_j. Then |ψ_{j}(h_j; k) − ψ̃_j(h̃_j)| ≤ |ψ_j(h_j; k) − ψ̃_j(h_j)| +
|ψ̃_j(h_j) − ψ̃_j(h̃_j)| ≤ δ_j + Lip_j η_j, because h_j ∈ H_j and the segment
between h_j and h̃_j lies in [L_j − η_j, U_j + η_j], where ψ̃_j is C¹ with
|ψ̃_j′| ≤ Lip_j. Multiply by |A| and sum. ∎

Hence min_R F ≥ min{ f̃(u) : u ∈ Z, h̃(u) ∈ [L − η, U + η] } − Δ ≥ LB_ideal − Δ.
Δ = 2.43e-11, 1.75e-11, 1.65e-11, 1.38e-10, 1.86e-11, 2.19e-11 (r3 n4/n5/n9,
r5 n3/n5/n8; `open-instances-wave3/logs/<name>.result.json`). LB_ideal comes
from a branch and bound with four forms (natural; mean value; affine-split
second order; third order with a Gershgorin test on VᵀH_cV, which preserves
inertia by congruence) and a monotonicity reduction on fully feasible boxes;
a box is discarded when lb ≥ UB − 10⁻¹⁰·max(1, |UB|) (`bbcore.py`: the
certified value is min(closed minimum, least open key, UB), valid whatever
UB is). The reported L is `dual_bound` ≤ LB_ideal − Δ (checked exactly here).
The tolerance explains why kan_r5_h1_n3 has the largest absolute gap:
10⁻¹⁰·262.9 = 2.6e-8.

**Relation of (I) and (II).** For all six instances L (authors) < L_ver
(independent), so (I) confirms (II):

| instance | L (authors, = summary dual) | L_ver (independent) | UB_ver | L_ver − L |
|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0027812371525814 | 0.0027812371878504 | 0.0027812372278504 | 3.5e-11 |
| kan_r3_h1_n5 | −0.011042679521782 | −0.011042679449684 | −0.011042679409684 | 7.2e-11 |
| kan_r3_h1_n9 | 0.012963659963475 | 0.012963660028294 | 0.012963660068294 | 6.5e-11 |
| kan_r5_h1_n3 | −262.86422590922 | −262.86422589412710 | −262.86422588361250 | 1.5e-8 |
| kan_r5_h1_n5 | 0.27258325385485 | 0.27258325392338 | 0.27258325396338 | 6.9e-11 |
| kan_r5_h1_n8 | 0.069327860510525 | 0.069327860579524 | 0.069327860619524 | 6.9e-11 |

Source: `reviews/wave3-verification/verification-report.md`, Section 1c, logs
`reviews/wave3-verification/logs/<name>.bnb_v2.{log,json}`; rerun with a
rigorous exp in Section 8.3 (identical L_ver for five instances; −262.8642258941303 for kan_r5_h1_n3).

Because L ≤ L_ver and L ≤ LB_ideal − Δ, the reported L is valid if either
implementation is correct. This is the main argument for reporting L rather
than the tighter L_ver (issue I13).

#### 3.2.4 What must be trusted

- (I) needs IEEE binary64 with one-ulp outward rounding by `nextafter`; the
  verifier's decoder (derived independently; its input and hidden boxes equal
  the authors' in exact arithmetic for r3_n4 and r5_n8); a lower bound of
  min silu (the verifier's `_zstar` uses mpmath intervals; checked here in
  rational arithmetic, Section 8.2); and, as run in wave 3, **numpy's exp
  accurate to within a relative 2⁻⁵⁰** (an empirical assumption: 0.58 ulp
  maximum error measured on 2·10⁵ points in [−8, 8]). This dossier reran (I)
  with numpy's exp replaced by the rigorous table exp of `kan_iv`
  (Section 8.3); the bounds are identical for five instances and 3.2e-12
  lower for kan_r5_h1_n3 (still 1.5e-8 above L), so the exp assumption is
  removed for path (I).
- (II) uses the rigorous exp of `kan_iv` (reviewed here, Section 8.2; its
  constants checked in rational arithmetic), but its ε, η, Lip values and its
  third-order form were not independently recomputed or reviewed. The
  verifier checked the logic of Δ.
- Neither KAN code was read line by line by a third party. (I) was tested by
  its author by soundness sampling on five of the six instances (not r3_n5;
  0 violations, smallest margin 1.2e-10). Agreement of two independently
  written codes, with L valid if either is correct, is the evidence
  (issue I13).

---

## 4. Exactly feasible primal points

### 4.1 ann_cumene_tanh

**Construction** (`publication/primal/water-ann-kan/code/fwd.py`, `nn_exact.py`;
point file `points/ann_cumene_tanh.point.json`).

- Inputs fixed at the rationals given by the 16-digit decimals of the wave-3
  point: x723 = 1854640286460337/(5·10¹²), x724 = 982921746111241/(1.25·10¹⁵),
  x725 = 1620252679906157/10¹⁵, x726 = 9494678019619749/10¹⁶,
  x727 = 734065236105183/10¹⁵ (≈ 370.92805729, 0.78633740, 1.62025268,
  0.94946780, 0.73406524).
- Every other variable is *defined* by one equality row in which it is the
  only unknown, appears linearly, and has a coefficient whose enclosure
  excludes 0. For e749 and e782–e787 the coefficients are x753, x746 and x766.
  All 789 equality rows are used, in an acyclic order. The real point x\*
  so defined satisfies every equality row exactly.
- Everything else is decided by outward enclosures of x\*: e789 holds with
  margin 9.979e-13; the bounds of all 728 bounded variables hold (x647 ≥ −1
  with margin 1.25e-12; the saturated neurons x650 = tanh(≈101.8) and
  x657 = tanh(≈−125.75) have enclosures that touch ±1, which still proves the
  non-strict bounds); no integer variables.

**Lemma P (forward existence).** If, with the inputs fixed at rationals, each
remaining variable is defined by a row in which it is the only unknown with a
nonzero coefficient, and the rows are used in an acyclic order, then the
defined real point satisfies all defining rows exactly. Existence is
constructive; only the nonzero coefficients, the unused rows and the bounds
need enclosures.

**Objective enclosure.** [−3379.982394071771548095722619880929,
−3379.982394071771548095722619880928] (outward 30-decimal rounding of the
stored enclosure; author, mpmath iv at 60 digits, width 1.0e-54; the JSON
stores 45-digit endpoints of width 1e-41). The independent review
(`publication/reviews/primal-water-ann-kan-r1/rev_nn.py`, own OSIL reader,
own rational interval arithmetic `rint.py` with a Taylor exp and Lagrange
remainder; no floating point, no mpmath) obtained width 2.8e-89 inside the
author's interval, the same 789 definition rows, and all rows and bounds
proved. The point is slightly better than MINLPLib's p1
(−3379.982394023530, row violation 8.2e-12). The 30- and 40-digit `.sol`
roundings are *not* exactly feasible; the JSON point (rational inputs plus
definitions) is the object of the proof.

### 4.2 KAN points of R_P

**Construction** (`nn_exact.py kan_*`, point files `points/kan_*.point.json`).

- Inputs fixed at the binary64 values of the wave-3 minimizers
  (`open-instances-wave3/logs/<name>.result.json`).
- For each edge, the binary of the first knot interval whose big-M rows hold
  for the whole enclosure of the argument is set to 1.
- The partition rows (equalities of continuous variables with all
  coefficients 1 and right-hand side 1; 3 per edge) are never used. Every
  other equality row defines one variable as in Lemma P: 838/1047/1883/617/1027/1642 rows
  (r3 n4/n5/n9, r5 n3/n5/n8). With the one-hot, big-M and partition rows this
  accounts for every row of each model (e.g. 838 + 16 + 576 + 48 = 1478).
- The one-hot rows hold exactly; layer-1 big-M rows hold exactly (rational
  arguments); layer-2 big-M rows hold by enclosures (smallest margin 1.4e-2 to
  6.5e-2 for r5, 7.3e-5 to 3.4e-3 for r3, so no knot ambiguity); **every OSIL
  variable bound holds, including those that R drops**; all binaries are 0/1.

So each point lies in R_P. At 60 digits the partition rows are violated
by 2.49e-15, 1.79e-16, 1.0e-15, 3.32e-16, 2.0e-16 and 5.81e-16 (r3 n4/n5/n9,
r5 n3/n5/n8); the other rows hold to ≤ 9.6e-42 at the interval midpoints
(author's 60-digit cross-check with the earlier reader). The independent review
proved the same with exact rational interval arithmetic and found its
enclosures (widths ≤ 3.2e-89) inside the author's.

---

## 5. Numbers table

Safe displays: duals rounded down, primal values rounded up (minimization);
gaps rounded up. "Exact" values are the binary64 numbers or rationals stored
in the cited files. Every value below was recomputed here with Fractions and
Decimal from the cited files (Section 8.1, item 2).

### 5.1 ann_cumene_tanh

| quantity | value | source |
|---|---|---|
| listed dual | none | MINLPLib page; `open-instances-scout/fetched.csv` |
| listed primal | −3379.982394 (p1) | MINLPLib page |
| our dual L\* | exact −7447080719734483/2⁴¹ = −3386.540229136918696895…; summary display **−3386.5403**; also valid as printed: −3386.5402291369187 | `ann/ext_logs/run2_resume_5400.log` (last lines); `reviews/ann-extension-review.md`; `primal/.../ann_cumene_tanh.point.json` (`dual_bound`) |
| our primal | enclosure upper end −3379.982394071771548095722619880928; summary display **−3379.9823940** | `publication/primal/water-ann-kan/points/ann_cumene_tanh.point.json` |
| absolute gap | 6.557835065147148799… → **≤ 6.5579** | recomputed here; point JSON `gap_upper` |
| relative gap | 1.940198e-3 of \|primal\| → **≤ 0.195%**; 1.936441e-3 of \|dual\| → ≤ 0.194% | `gap-values.json` entries "ann" and "ann dual" |
| wave-3 dual (historical) | −4024.4949777 (display −4024.495); gap 644.5126 = 19.07% of \|primal\| (summary display "≤ 20%"), 16.01% of \|dual\| (`gap-values.json`: 16.1%) | `open-instances-wave3/report.md`; `gap-values.json` |

### 5.2 KAN (claims concern R and R_P)

| instance | listed dual (GUROBI) | listed primal | our dual L (safe display) | our primal U (safe display) | gap U − L (rounded up) | relative to \|L\| |
|---|---|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0003908 | 0.00278124 | 0.002781237152581 | 0.002781237221442 | **≤ 6.9e-11** | 2.48e-8 |
| kan_r3_h1_n5 | −0.01302849 | −0.01104268 | −0.01104267952179 | −0.01104267941448 | **≤ 1.08e-10** | 9.72e-9 |
| kan_r3_h1_n9 | 0.0081425 | 0.01296366 | 0.01296365996347 | 0.01296366005304 | **≤ 9e-11** | 6.91e-9 |
| kan_r5_h1_n3 | −789.740197 | −262.3058993 | −262.8642259093 | −262.8642258850 | **≤ 2.42e-8** | 9.19e-11 |
| kan_r5_h1_n5 | 0.26787523 | 0.27265451 | 0.2725832538548 | 0.2725832539567 | **≤ 1.02e-10** | 3.73e-10 |
| kan_r5_h1_n8 | −45.00462396 | 0.36062128 | 0.06932786051052 | 0.06932786060620 | **≤ 9.6e-11** | 1.38e-9 |

Sources: L = `dual_bound` in `open-instances-wave3/logs/<name>.result.json`
(binary64; identical to `dual_bound` in the point JSON); U = `objective_hi`
in `publication/primal/water-ann-kan/points/<name>.point.json`; gaps in
`publication/integration/gap-values.json`. Recomputed here exactly from these
files: every gap equals the stored rational (`exact_upper`), every display
is an outward rounding, and `dual_bound ≤ LB_ideal − Δ` holds exactly. No
disagreement with the summary was found. The listed MINLPLib primal values
are tolerance-feasible OSIL points; our U values are exact points of R_P. For
r5 n3/n5/n8 our points improve the listed values by 0.558, 7.1e-5 and 0.291.
For the r3 instances, the listed points are no worse than ours: evaluated at
60 digits, the network at the listed inputs gives values 1.6e-14 (r3_n4),
2.9e-15 (r3_n5) and 2.1e-13 (r3_n9) below U (`reviews/wave3-verification/logs/kan_primal.log`;
issue I15). This does not affect the enclosure.

Optional tighter KAN gaps (if L_ver is reported instead of L; not
recommended, issue I13): U − L_ver ≤ 3.4e-11, 3.6e-11, 2.5e-11, 9.07e-9,
3.4e-11, 2.7e-11 (r3 n4/n5/n9, r5 n3/n5/n8; computed here exactly).

---

## 6. Verification record

| review | scope | what it checked | verdict |
|---|---|---|---|
| wave-3 verification (`reviews/wave3-verification/verification-report.md`), 2026-09-30 | KAN 1a–1e; ann Section 3 | KAN: own exact decoder; R; Δ logic (numbers not recomputed); own rigorous B&B on R for all six (numpy exp assumption); soundness sampling on 5 instances (0 violations, smallest margin 1.2e-10); 60-digit evaluation of the wave-3 points; **exact infeasibility of all six OSIL models** (Sturm counts and resultants; gcd root isolation in `kan_struct.py`). ANN: relaxation R, wave-3 bound per box (full run not repeated) | KAN verified, with the infeasibility correction; ann wave-3 bound verified with caveats |
| ANN extension review (`reviews/ann-extension-review.md`), 2026-09-30 | L\* = −3386.5402291369187 | deterministic replay of both runs (all log lines and both frontiers bit for bit); coverage (volume, 4000 points); own bound `annx.py` on all 1,644,110 closed regions and 208,223 open boxes; 15,201-point soundness sampling of both bounds; reading of the authors' code; primal and gap arithmetic; Section-5 diagnostics; literature | **verified**; minor wording issues, a recommended NaN guard (no NaN in 2.70 M evaluations) |
| primal review r1 (`publication/reviews/primal-water-ann-kan-review-r1.md`) | exact points for ann and six KAN | own OSIL reader; exact rational interval arithmetic (no floating point, no mpmath); forward definitions; all rows (except KAN partition rows) and all bounds; negative controls (7 rejected) | **verified**, minor issues addressed |
| network literature r1/r2 (`publication/reviews/lit-network-review-r{1,2}.md`) | provenance and prior results | cumene twin identity (exact); KAN source identification; 60-digit network values at SCIP's points (own reader, permutation test); SCIP 10 fixed-input runs | r1 issues (one major for ann: missed twin), resolved; r2 **verified** |
| integration r1/r2 (`publication/reviews/integration-review-r{1,2}.md`) | summary numbers | exact recomputation of every gap cell, including ann (4 percentages) and the six KAN cells | issues elsewhere; ann and KAN cells confirmed |
| this dossier | Sections 8.1–8.3 | independent infeasibility check (separate propagation code, one edge per instance); SiLU constants in rational arithmetic; review of the rigorous exp and exact check of its constants; rerun of the independent KAN B&B with a rigorous exp (all six); reading of `annx.py`'s rigorous parts; saturated-tanh analysis; exact recomputation of all gaps and displays | see Section 8 |

**Remaining assumptions.**

- ANN dual: IEEE binary64 round-to-nearest with `nextafter` and no
  flush-to-zero; correctness of either `annx.py` (tested by its author, rigor
  parts read here) or `ann_tm.py` (read in full by the reviewer); coverage
  implementation (replay). No A1/A2-type assumption (no libm exp, no
  unproved padding analysis); mpmath is not needed after this dossier's
  constant check.
- ANN primal: exact rational arithmetic only (review r1). The summary's
  "assumes mpmath iv" is the author's route and can be dropped (issue I3).
- KAN infeasibility: exact rational arithmetic and correct reading of the OSIL
  decimals (osilx; cross-checked by three readers).
- KAN dual: IEEE binary64 and correctness of either code (Section 3.2.4);
  after this dossier's rerun, no exp assumption for path (I).
- KAN primal: exact rational arithmetic only.

---

## 7. Relation to prior work

**ann_cumene_tanh.**

- Schweidtmann and Mitsos (arXiv:1801.07114v2, Table 4, Fig. 6; local copy
  `schweidtmann2019-deterministic-global-optimization-with-artificial`): no
  method converged in 10⁵ s. BARON 17.4.1 (full space, forms F1–F4) ended with
  absolute gap 10²⁰ and "does not improve its initial lower bound on the
  objective at all"; MAiNGO in reduced space ended with absolute gaps 10¹¹
  (F3), 8·10¹⁰ (envelope) and 10⁵ (envelope\*); F1, F2, F4 crashed. The 2021
  dissertation (`schweidtmann2021-global-optimization-of-processes-through`,
  Table 2.8) reports MAiNGO gaps 2930 (F3), 444 (envelope) and 328
  (envelope\*) instead; the JOTA table is unchecked. Either way the problem
  was not closed there. Their reduced-space formulation has the same five
  variables and one inequality as our reduction.
- MINLPLib lists no dual for ann_cumene_tanh, but the identical twin
  ann_cumene_exp has floating-point duals −3379.982394 (SCIP and LINDO,
  15 Feb 2022) equal to the displayed primal, and BARON −3379.985774
  (31 Jul 2025). So the problem is **partly known**: closed in floating point
  through the twin. Our bound is the first *rigorous* one found and is weaker
  than those floating-point claims.
- Izquierdo González et al. (Syst. Control Trans. 5, 2026) solve a different
  cumene ANN model globally.
- Mechanisms, with local copies where available: affine arithmetic
  (`stolfi2003-an-introduction-to-affine-arithmetic`) and its use in interval
  branch and bound (`figueiredo1997-fast-interval-branch-and-bound`, for
  unconstrained problems); Taylor models
  (`berz2009-rigorous-global-search-using-taylor`;
  `sahlodin2011-convex-concave-relaxations-of-parametric`); safe bounds from
  approximate LP multipliers (`neumaier2004-safe-bounds-in-linear-and`);
  interval branch and bound with constraint propagation
  (`neumaier2004-complete-search-in-continuous-global`, `vu2009-interval-propagation-and-search-on`,
  `schichl2005-interval-analysis-on-directed-acyclic`); reduced-space bounding
  of ANN-embedded problems (the source paper; `mitsos2009-mccormick-based-relaxations-of-algorithms`);
  convex relaxations of S-shaped activations (`carrasco2026-tightening-convex-relaxations-of-trained`).
  Zonotope (affine) domains are standard in neural-network verification
  (e.g. DeepZ); no such source is in the local knowledge base, so cite it only
  after checking. The combination used here (one noise symbol per neuron,
  constraint handling by a per-box LP dual evaluated in outward rounding, on a
  constrained problem with 250 neurons) is not claimed as new in method; the
  contribution is the certified bound for this instance.
- The remaining gap is a constrained cluster effect
  (`du1994-the-cluster-problem-in-multivariate`, `wechsung2014-the-cluster-problem-revisited`,
  `kannan2017-the-cluster-problem-in-constrained`): Kannan and Barton show
  that first-order convergent bounds can avoid clustering at a constrained
  minimizer when f grows linearly in feasible directions, but need second
  order otherwise. Here two constraints are active in five dimensions and f
  grows only quadratically on the 3-dimensional tangent space (reduced
  Hessian eigenvalues 39.5, 269.6 and 2.12·10⁵ in normalized coordinates;
  Lagrangian f − 58.51(x647 + 1) − 20891.4(x772 − 0.999)), and the affine
  bounds are first-order.

**KAN.**

- Karia, Lastrucci, Schweidtmann (arXiv:2503.02807v1; Zenodo 14961066): SCIP
  9.0.1 reported "optimal" values 1.08116412e-3 (r3_n4, 3459 s) and
  −1.30809959e-2 (r3_n5, 5038 s) for the Default formulation, and further,
  mutually different "optimal" values for other formulations. All lie
  **below** our certified min of R. At SCIP's reported inputs the network
  evaluates (60 digits) to 0.0028684784 and −0.0108512435. With the inputs
  fixed there, SCIP 10.0 returns "optimal" 0.0026959290 and −0.0113202912
  with row violations up to 9.3e-7 and 1.0e-6. The output scale A ≈ 970 turns
  row violations of about 10⁻⁶ into objective shifts of about 10⁻³. These are
  tolerance artifacts, not exact optima.
- r3_n9, r5_n3/n5/n8: all source runs hit the 7200 s limit; best duals
  −11.376, −1587.43, 0.18669, −122.67. For r5_n5 the ConvexHull run reports a
  primal value 0.2725188 below min R; the network at that input gives
  0.2729243.
- No other certificate for these networks was found (searches listed in the
  network literature report; the AIChE 2025 abstract of the source group was
  not obtained). Other KAN-optimization papers (Karia et al., ESCAPE 35,
  `karia2025-kolmogorov-arnold-networks-kans-as`; Li et al., arXiv:2604.03871)
  use different networks.
- Mechanisms: interval branch and bound in reduced space with second- and
  third-order forms (cf. Taylor models, `berz2009-rigorous-global-search-using-taylor`);
  exact real-algebraic certificates (Sturm sequences, resultants) for the
  infeasibility; monotonicity tests
  (`araya2010-exploiting-monotonicity-in-interval-constraint`).

---

## 8. Critical examination

### 8.1 Commands run for this dossier (targeted; disposable copies; no CI, no project-wide checks)

Copies under `/tmp/annkan_dossier/` and `/tmp/annkan_dossier2/`, with
`PYTHONDONTWRITEBYTECODE=1` and single-threaded BLAS; inputs are the cached
OSIL files and copies of `reviews/open-instances-verification/osilx.py`,
`open-instances-wave3/ann/ann_model.py`, `reviews/wave3-verification/{kan_decode,kan_bnb}.py`,
`open-instances-wave3/kan/kan_iv.py` (path insertion removed),
`open-instances-wave2/small/ia.py` and
`publication/reviews/primal-water-ann-kan-r1/rint.py` (all byte-identical to
the sources apart from the noted line). Scripts and logs are saved in
`paper-open-minlplib/development/dossiers/ann-kan-checks/`.

1. `ann_model.decode()` (copy): input box, row and bound classes, objective
   terms; plus an `osilx` read of the bounds of x746, x753, x754, x756, x766,
   x787–x793, objvar (all free except objvar ±10²⁰) and the count of 728
   bounded variables (Section 1.1).
2. Exact recomputation of L\*, the ANN gaps, the twin difference, and all six
   KAN gaps and displays from the point JSONs, `result.json`,
   `bnb_v2.json` and `gap-values.json` (Fractions/Decimal). All agree;
   `dual_bound ≤ LB_ideal − Δ` holds exactly for all six.
3. `kan_infeas_edge.py <instance> <edge>` (own propagation code; uses only the
   argument's own bounds): r5 n5/n8 — all 8 admissible pieces certified;
   r3 n4/n5/n9 — 13 of 14 (`kan_infeas_edge_roots.py kan_r3_h1_n4 x1076`:
   for b22 the residuals of rows e197 and e198 are proportional with common
   root z = −1.7755611391195993, the argument's own lower bound).
4. `kan_infeas_edge_class.py <instance> <edge>` (same, with the input-class
   box): r3 n4/n5/n9 — 12 of 12; r5_n3 — 6 of 6. With item 3, all six models
   are infeasible.
5. `silu_min_check.py` and `silu_verifier_consts.py`: the SiLU-minimizer
   brackets of both codes and the constants SILU_MIN_LO = −0.27846454276107413
   (authors) and SMIN_LO = −0.27846454276107474 (verifier) are valid lower
   bounds of min silu, proved with rational arithmetic (the review's
   `rint.exp_bounds`).
6. `check_constants.py`: exact rational checks that both ln 2 enclosures
   (`kan_iv.LN2`, `LN2_64`, and annx's construction) contain ln 2
   (series Σ 1/(k2^k) with tail bound), that all 64 table entries of
   `kan_iv` contain exp(j ln2/64) (Taylor bracket with remainder), and that
   the three Taylor remainder constants (10⁻²¹, 10⁻²⁵, 10⁻³⁰) are valid. All
   pass.
7. `kan_bnb_rigexp.py <instance> 4e-11 <limit> 1024` for all six instances:
   the verifier's branch and bound with `iexp` replaced by
   `kan_iv.iexp_pt_fast` (diff in `kan_bnb_rigexp.diff`; no numpy exp in any
   rigorous path; the remaining `np.exp` calls are in the float local search
   and the `--check-exp` test). Results in Section 8.3.
8. Reading (no execution) of the rigorous parts of `annx.py` (interval class,
   exp, tanh, `tanh_lin`, forward pass, objective, bound, `dual_value`,
   `prove`), of `ann_bb.tanh_pt` and `ann_tm.tanh_lin`, and of
   `kan_bb.Net.__init__` (ε, η, Lip, Δ).
9. Literature: dissertation Table 2.8 and arXiv Table 4 read in the local
   knowledge base.

### 8.2 Re-derivation and checks

**ANN reduction (Lemma A.1).** Re-derived from the decoded rows. Correct.
The claim "R drops only the solvability of the product rows" is right in the
sense that matters: no division enters f, so the lemma holds even where
x746 or x766 vanishes (enclosures [−194, 262] and [−18.1, 30.9] contain 0).

**ANN per-box inequality (Lemmas A.3–A.5).** Re-derived; matches the
reviewer's formula in `ann-extension-review.md`, Section 3.1. The authors'
`tanh_lin` was read: the convex/concave split, tangent bounds at an arbitrary
p, and the monotone case α ≤ min(tanh′(l), tanh′(t)) are all valid. The
clipping step replaces a form by a constant interval valid only at feasible
points; this is sound for lower bounds. The objective cut removes only points
with f > UB, and the final value is ≤ UB, so it is sound even if UB were not
attained.

**annx.py rounding (read here).** Linear rows: the radius update
Wa·r + τ(Wa·(|C| + S + r) + |b|), then ×(1 + τ) and one ulp up, covers the
propagated remainder, the rounding of C and of every A entry (bounded by
γ_k Σ|w|(|C| + S)), and the representation errors of w and b. tanh: the
update α r_z + τ(α|C_z| + |β| + α S_z) covers the rounding of αC_z + β and of
αA_z. Products: the ½D + N split and the τ terms are correct. Constraint
values q_j use the outward enclosure [b_lo, b_hi] of each exact bound.
`dual_value` evaluates Φ(μ) in outward interval arithmetic. NaN gives "not
proved". No error found.

**Saturated tanh (new; both codes).** `ann_bb.tanh_pt` (authors) and
`annx.itanh_pt` (reviewer) set lo = 1.0 − 1e-200 for |z| ≥ 300, which rounds
to 1.0, so the enclosure is [1, 1] (or [−1, −1]). The true value satisfies
1 − 2e^{−600} < tanh(z) < 1, so the enclosure misses it by ε < 6·10⁻²⁶¹.
The 60-digit reference used in the reviewer's test (`t_basic.py`, points
±350) also rounds to 1 and cannot detect this. *Proof that it is harmless.*
In both codes a point value T = [1, 1] is used only inside outward-rounded
interval operations: g = T − α·s and the crude T − α·b (linearization),
1 − T·T (derivative bounds), and w·T (natural interval pass, followed by
linear rows). (i) For T − p with T = [1, 1], z ≥ 300 and p = α·s ≥ 0 computed as an
outward interval [p_lo, p_hi]: each outward step rounds to nearest and then
moves one binary64 step outward, so it moves the end by at least a quarter
of a unit in the last place of the result (a half, except at a binade
boundary). Hence p_hi ≥ αs + ulp(αs)/4, and the computed lower end of
T − p is ≤ (1 − p_hi) − ulp(1 − p_hi)/4 (if 1 − p_hi = 0 only the first slack
is used). Since max(p, |1 − p|) ≥ 1/2, one of the two slacks is at least
2⁻⁵⁵ ≈ 2.8·10⁻¹⁷ ≫ ε, so the lower end is below the true
g = tanh(s) − αs > 1 − ε − αs. The upper end needs nothing (tanh(s) < 1).
The case z ≤ −300 is symmetric. (ii) 1 − T·T with
T·T = [1 − 2⁻⁵³, 1 + 2⁻⁵²] gives an interval containing [−2⁻⁵², 2⁻⁵³],
which contains the true sech²(z) ≤ 4e^{−600}. (iii) w·T is widened outward by
at least a quarter ulp of w, i.e. by ≥ 2⁻⁵⁵|w| ≫ ε|w|. So every derived enclosure is still valid
and the proofs stand. A released artifact should still use
`np.nextafter(1.0, 0.0)` as the lower end (issue I12). (The KAN SiLU code has
no such shortcut; its exp asserts |x| ≤ 700.)

**ANN covering.** Sound by construction; the numerical checks are checks of
the replay implementation, not the proof. Both codes start from the outward
binary64 enclosure of U (`M.lo0`, `M.hi0` built with `frac_iv`), so no sliver
of U is lost. One reproducibility gap: the reviewer's region lists and
per-region results lived in `/tmp/annrev/`, which no longer exists
(checked). Re-verification needs the replay (1805 s + 5220 s, one core) and
`verify_boxes.py` (360 + 1280 + 374 s on 4–5 processes).

**Rigorous exp (`kan_iv.py`).** Read in full. ln 2 is enclosed by comparing a
55-digit mpmath decimal exactly with doubles; j! is exact in binary64 for
j ≤ 22, so the inverse factorials are enclosed by one outward division; the
degree-18 remainder |r|¹⁹/19!·e^{|r|} ≤ 4.4e-26 ≤ 10⁻²¹ for |r| ≤ 0.36; the
table version uses |r| ≤ 0.0055 (ln 2/128 ≈ 0.0054), remainder ≤ 1.3e-26 ≤ 10⁻²⁵,
table entries from 50-digit values widened by one ulp, and exact
power-of-two scaling (k ≥ −1010 keeps results normal for |x| ≤ 700).
`ia.NI` rounds each +, −, ×, ÷ to nearest and widens by one ulp; this
encloses the exact result (also for subnormal results). Sound. The mpmath
constants and the remainder constants were checked in exact rationals
(Section 8.1, item 6), so the only trust left is binary64 arithmetic.

**SiLU minimum.** Both codes need a lower bound of min silu = −0.2784645427610738…
(at z\* = −1.2784645427610738…). Checked in exact rational arithmetic: on
the authors' bracket [−1.27846454277, −1.27846454275], silu′ < 0 at the left
end and > 0 at the right end, and the mean-value lower bound
−0.2784645427610738 is ≥ SILU_MIN_LO = −0.27846454276107413. The verifier's
constants, recomputed with its own `_zstar` code, are ZS_LO = −1.2784645427610748,
ZS_HI = −1.2784645427610726 and SMIN_LO = −0.27846454276107474; in rational
arithmetic silu′(ZS_LO) < 0 < silu′(ZS_HI) and the mean-value lower bound
−0.2784645427610738 is ≥ SMIN_LO. Both are valid. The mean-value step uses
|silu′| = σ|g| ≤ |g| with g(z) = 1 + z(1 − σ(z)); g′(z) = (1 − σ)(1 − zσ) > 0 for
z < 0, so |g| on the bracket is at most its larger end value. (Also
silu(z\*) = z\* + 1, since g(z\*) = 0 gives σ(z\*) = 1 + 1/z\*.)

**KAN Δ argument (Lemma K.3).** Re-derived and the code read
(`kan_bb.Net.__init__`); correct. The Lipschitz grid is
`linspace(hlo, hhi, 4001)`, whose end points are exactly the outward hidden
bounds, so the 4000 cells cover [L_j − η_j, U_j + η_j]. Two remarks: (i) the
segment argument needs both h_j and h̃_j in [L_j − η_j, U_j + η_j], which holds
because h_j ∈ H_j in R; (ii) Δ makes the authors' bound valid for R, not for
the ideal network; conversely, LB_ideal (not LB_ideal − Δ) is a lower bound
for the ideal network on the enlarged hidden boxes, which is what supports
statements about the exact-spline network (authors' code only).

**KAN infeasibility.** Reconfirmed with separate code (Section 8.1, items 3–4):
own parsing of the big-M rows and own polynomial propagation over ℚ, using
only the OSIL reader in common with the verifier. Common zeros of the three
residuals are the zeros of the gcd of the nonzero ones, so "gcd constant" or
"gcd root-free on I_k ∩ Z" is a complete test. The proof uses the
scaled-copy bounds for the r3 models (first admissible piece of x1076,
x1344, x2416). This is a fact about which constraints the proof needs, not a
gap. Not every edge has a certificate (r3: only the edges of input 2), but
one edge suffices.

**KAN branch-and-bound logic.** The final values of both codes are minima
over open boxes, recorded discarded bounds and UB − tol (or UB), which are
valid whatever UB is. Start boxes and piece admissibility use outward
enclosures. The verifier's L_ver uses `UB − tol`; its UB is also rigorously
R-feasible, but validity does not need that.

**Numbers.** Section 5 recomputed exactly; no disagreement. The summary's ANN
"≤ 0.195%" uses the primal denominator, as stated there; the extension note
and network literature report say 0.194% (dual denominator, or nearest
rounding). The wave-3 gap appears as 19% (SYNTHESIS), 19.1% (extension),
"≤ 20%" (summary) and 19.07% (exact).

### 8.3 Rerun of the independent KAN bound with a rigorous exp

`kan_bnb_rigexp.py` is `reviews/wave3-verification/kan_bnb.py` with one
function changed: `iexp(x)` returns [lower end of `kan_iv.iexp_pt_fast(x.lo)`,
upper end of `kan_iv.iexp_pt_fast(x.hi)`] (exp is increasing) instead of
numpy's exp widened by 2⁻⁵⁰. Same arguments as the wave-3 run
(`<name> 4e-11 <limit> 1024`); one process each, on a shared machine with
load about 9–13 (times are indicative).

| instance | L_ver, numpy exp (wave 3) | L_ver, rigorous exp (this rerun) | UB_ver (both, or wave 3 / rerun) | boxes wave 3 / rerun | time s wave 3 / rerun |
|---|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0027812371878503973 | 0.0027812371878503973 | 0.0027812372278503976 | 26,353 / 26,353 | 9 / 26 |
| kan_r3_h1_n5 | −0.011042679449683842 | −0.011042679449683842 | −0.01104267940968384 | 22,297 / 22,301 | 6 / 23 |
| kan_r3_h1_n9 | 0.012963660028294303 | 0.012963660028294303 | 0.012963660068294304 | 42,635 / 42,633 | 14 / 55 |
| kan_r5_h1_n3 | −262.8642258941271 | −262.8642258941303 | −262.8642258836125 / −262.8642258836157 | 1,648,095 / 1,648,095 | 266 / 1221 |
| kan_r5_h1_n5 | 0.2725832539233757 | 0.2725832539233757 | 0.27258325396337574 | 709,939 / 709,937 | 147 / 761 |
| kan_r5_h1_n8 | 0.06932786057952356 | 0.06932786057952356 | 0.06932786061952358 | 615,347 / 615,673 | 219 / 1188 |

All runs ended with no open boxes, so each final value is UB − tol
(rounded down). Five values are bit-identical. For kan_r5_h1_n3 the rigorous
exp gives a rigorous upper end UB at the same incumbent that is 3.2e-12
lower, so L_ver is 3.2e-12 lower (−262.8642258941303 = UB − 1.0514569035344627e-8);
it is still 1.509e-8 above L = −262.86422590922143, and U − L_ver ≤ 9.07e-9.
So L ≤ L_ver holds for all six instances with the rigorous exp. The box counts
differ slightly because the rigorous exp enclosures are a little wider or
narrower than numpy's ±2⁻⁵⁰ widening, which changes a few pruning decisions;
the final values are UB − tol, so they coincide wherever UB coincides (the
same incumbent point was found in all six runs).
Logs: `ann-kan-checks/logs/<name>.rigexp.log` and `<name>.bnb.json`.

### 8.4 Issues and resolutions

I1 (major, assumption missing from the summary; now resolved by computation).
The independent check of the KAN duals assumed numpy's exp accurate to a
relative 2⁻⁵⁰ (empirical). `open-instances-summary.md` and `READINESS.md` call
the KAN duals "independently verified" without this assumption, and the
authors' own path has unreviewed parts (ε/η/Lip numbers, third-order form).
*Resolution:* the rerun of Section 8.3 removes the assumption for L_ver,
which dominates L. Before citing it, have the one-function change reviewed
(one function and one import; `kan_bnb_rigexp.diff` has 17 lines) and archive `ann-kan-checks/` with the paper
artifact. If not adopted, state the assumption for KAN as for the eg_*
family.

I2 (minor, reproducibility). The ANN re-certification's region lists were
temporary and are gone. *Resolution:* regenerate with the review's
`replay.py` and `leaves.py` (about 2 h on one core) and archive the region
list (about 50 MB) or a compact split-decision encoding of the tree; rerun
`verify_boxes.py` (about 35 min on 4–5 processes) for the artifact.

I3 (minor, removable assumption). The summary and READINESS say the ANN and
KAN primal enclosures assume mpmath iv. Review r1 proved them with exact
rational interval arithmetic only. *Resolution:* state "proved in exact
rational interval arithmetic (independent review); confirmed with mpmath
intervals (author)".

I4 (minor, stronger and simpler statement available). The KAN points satisfy
every OSIL bound, so both min R and min R_P lie in [L, U]. R_P has a one-line
definition and drops only rows that are identities for exact B-splines on
the admissible domain (Section 1.2). *Resolution:* state the result for R_P,
"the OSIL model with its partition-of-unity rows removed", and mention R as
the set used by the dual bound. No computation needed.

I5 (minor, wording). Several documents call R "the intended network
(relaxation)" (`publication/reproduction/README.md`, `SYNTHESIS.md`,
`closing-research-results.md`, the network literature report). R contains
the network with the model's decimal pieces, which differs from the exact
C² spline network by at most Δ in the objective. *Resolution:* use "R" or
"R_P" with their definitions; say "exact-spline network" when that is meant,
and support claims about it only with LB_ideal.

I6 (minor, outdated statements in older notes). SYNTHESIS.md and
closing-research-results.md say the KAN relaxations are certified "to about
1e-10" and give ann_cumene_tanh "its first finite dual bound". *Resolution:*
use the summary: absolute gaps ≤ 2.42e-8 (kan_r5_h1_n3; 9.2e-11 relative)
and ≤ 1.08e-10 otherwise; "the first rigorous dual bound found" for
ann_cumene_tanh.

I7 (minor, display). The wave-3 ANN gap appears with four different
roundings. *Resolution:* omit the wave-3 bound from the paper or give
"19.07% (absolute 644.52)".

I8 (minor, tolerance semantics). L is not a valid bound for
tolerance-feasible OSIL points: relaxing the recursion rows by 10⁻⁶ can lower
the objective by about A·10⁻⁶ ≈ 10⁻³. *Resolution:* state this next to the
KAN result and in the discussion of the SCIP values.

I9 (minor, observation on the twin). Our exactly feasible point is also
feasible for ann_cumene_exp, with objective −3379.9823940717715…, which is
7.18e-8 below the displayed SCIP and LINDO duals −3379.982394. The display's
rounding slack is 5e-7, so in the audit's terms this is "invalid as listed"
(class (i-r)), explainable by page rounding; the underlying solver values
are unknown. The bound audit did not cover this twin. *Resolution:* at most
a footnote with the audit's (i-r) wording; do not claim a solver error.

I10 (minor, research). The ANN gap (0.195%) remains. *Resolution:* not
needed for the paper's claims. Closing it would need second-order bounds
near the active surface (second-order Taylor models for the second tanh
layer, or a certified local argument based on the second-order sufficient
condition at u\*), possibly neuron-argument branching. Cost unknown; a
research task.

I11 (minor, GAMS form). The KAN infeasibility and both ANN results are proved
for the OSIL decimals. The status track compared the .gms and OSIL forms of
these seven instances only at 50-digit sample points (its exact comparison
`exact_forms.py` covered other instances). No .gms file is cached locally.
*Resolution:* say "OSIL model"; optionally download the seven .gms files and
compare their decimals exactly with the OSIL rows (minutes), or run the edge
check on the GAMS rows.

I12 (minor, new; code hygiene, proved harmless). Both ANN tanh enclosures
return [1, 1] for |z| ≥ 300 (Section 8.2). The reviewer's code copied the
authors' idiom, so the two codes are not independent in this detail. The
deficit (< 6·10⁻²⁶¹) is absorbed by the next outward-rounded operation, as
proved in Section 8.2, so L\* stands. *Resolution:* include the short
argument in the paper's appendix (or a footnote) and change the constant to
`np.nextafter(1.0, 0.0)` in the released code. No rerun needed.

I13 (minor, new; disclosure). Neither KAN code was read line by line by a
third party; (I) was soundness-sampled by its author on five of six instances
(not r3_n5); (II) was reviewed only for the logic of Δ. The authoritative L
is valid if either code is correct, because L ≤ L_ver and L ≤ LB_ideal − Δ.
*Resolution:* report L (not the tighter L_ver, which rests on (I) alone) and
state the two-implementation argument. Optional: a third-party reading of
`kan_bnb.py` (756 lines; the LB2 penalty and the LB3 LDLᵀ test are the
delicate parts), about half a day; optional soundness sampling on r3_n5
(`kan_soundness.py`, minutes).

I14 (minor, new; removable assumption). The exp routines take ln 2 and the
64 table values from mpmath. *Resolution:* done here: exact rational checks
(`check_constants.py`) prove all these constants and the remainder bounds.
The paper can say the exp enclosures rely only on binary64 arithmetic.

I15 (minor, new; wording). For the r3 instances the listed MINLPLib inputs,
evaluated at 60 digits, give network values slightly below our U (by
1.6e-14, 2.9e-15, 2.1e-13). *Resolution:* do not call our r3 points "best
known"; claim primal improvements only for r5 n3/n5/n8. U remains a valid
upper end of the enclosure.

I16 (minor, new; literature). The draft said the local knowledge base has
no affine arithmetic or Taylor model source. It has
`stolfi2003-an-introduction-to-affine-arithmetic`,
`figueiredo1997-fast-interval-branch-and-bound` and
`berz2009-rigorous-global-search-using-taylor`. *Resolution:* cite them
(Section 7).

I17 (minor, new; correction of the draft). The draft wrote the scaling row as
x777 = 1.1796…·x776 − 0.00391…; the OSIL row is
−x777 + 1.1796167609850992·x776 = −0.003910886333986257, i.e. +0.00391….
Fixed in Section 1.2; the Rosenbrock coordinates quoted there were
recomputed with the correct sign.

Nothing found here invalidates a claimed result.

---

## 9. What the paper may claim and must not claim

**May claim (suggested wording).**

- ann_cumene_tanh: "Every exactly feasible point of the MINLPLib model
  ann_cumene_tanh has objective at least −3386.5403. An exactly feasible point
  with objective −3379.98239407177… exists. The remaining gap is at most
  6.558, i.e. 0.195% of the primal value. The lower bound comes from a
  computer-assisted branch and bound over the five inputs; every leaf was
  certified by two independently written implementations in outward-rounded
  binary64 arithmetic, with no trusted library transcendental." Add:
  "MINLPLib lists no dual bound for this model. To the best of our knowledge
  this is the first rigorous dual bound for it; the identical model
  ann_cumene_exp was closed in floating point by SCIP and LINDO, and our bound
  is weaker than those floating-point values."
- "Our bound and point apply verbatim to ann_cumene_exp, which differs only
  by the identity −tanh(v) = 2/(exp(2v) + 1) − 1 (verified exactly)."
- KAN: "In exact arithmetic, none of the six KAN models in MINLPLib has a
  feasible point: the decimal coefficients make the partition-of-unity rows
  of a single edge unsatisfiable on every admissible knot interval (exact
  certificates). These rows are identities for exact B-splines, so we certify
  the model without them, R_P. For each instance we enclose min R_P with
  absolute width at most 2.42·10⁻⁸ (kan_r5_h1_n3) and at most 1.08·10⁻¹⁰ for
  the others. The upper ends are attained by points that satisfy every other
  row and every bound exactly and violate the partition rows by at most
  2.5·10⁻¹⁵; for kan_r5_h1_n3, n5 and n8 they improve MINLPLib's listed
  primal values. The lower ends are confirmed by two independently written
  branch-and-bound codes."
- "The 'optimal' values reported for kan_r3_h1_n4 and kan_r3_h1_n5 in the
  source study lie below our certified lower bound of R; they are
  consequences of the solver's feasibility tolerance (row violations near
  10⁻⁶ scaled by A ≈ 970)."
- "To the best of our knowledge" is justified for: first rigorous dual for
  ann_cumene_tanh; first certified enclosures for the six KAN models without
  partition rows; the infeasibility observation.

**Must not claim.**

- That ann_cumene_tanh (or any KAN instance) is "closed" or "solved" in the
  OSIL sense. ann has a 0.195% gap; the KAN OSIL problems are infeasible.
- "First finite dual bound" for ann_cumene_tanh (the twin has finite FP
  duals), or that the problem was previously unsolved in any sense.
- That L is a dual bound for tolerance-feasible OSIL points, or that SCIP has
  a bug on the KAN models.
- A blanket "certified to 1e-10" for KAN (false for kan_r5_h1_n3 in absolute
  terms).
- That R is "the intended network" or "the trained KAN"; or that our KAN
  points are OSIL-feasible; or that our r3 KAN points are the best known.
- That the KAN dual bounds are free of assumptions beyond binary64
  arithmetic and code correctness, unless the rigorous-exp rerun
  (Section 8.3) is archived and its one-function change reviewed; otherwise state
  the numpy exp assumption for path (I) and the unreviewed parts of path (II).
- That either KAN code was independently reviewed line by line.
- That the ANN primal relies on mpmath (it does not; issue I3), or that the
  30/40-digit `.sol` files are exactly feasible.
- A performance comparison with MAiNGO/BARON/SCIP from these runs (shared
  machine, different settings).

---

## 10. Candidate figures and tables

1. **Table (ANN):** listed dual (none), twin FP duals, wave-3 rigorous bound,
   final bound, exact primal, gap (Section 5.1).
2. **Table (KAN):** listed dual and primal, L, U, U − L, relative gap, Δ,
   L_ver, boxes/time of both implementations (Sections 3.2.3, 5.2, 8.3), plus
   the SCIP "optimal" values from the source for n4/n5, marked below L.
3. **Figure (ANN convergence):** certified bound versus time for wave 3
   (−4024.49 at 3600 s) and the extension (−3540.38 at 318 s, −3455.2 at
   1069 s, −3426.92 at 1800 s, then −3398.22, −3394.39, −3388.60, −3386.54 at
   1800 + 2068/2732/4438/5401 s), with the primal value as a horizontal line
   (data in `ann/extension.md` Section 4 and the two logs).
4. **Figure (ANN tightness):** median box-bound gap versus box size for the
   wave-3 enclosure, one remainder per variable, and shared neuron symbols
   (`extension.md` table 2.2; `ext_logs/test_tm_{lumped,sep}.log`).
5. **Figure (ANN frontier):** projection of the final open boxes onto
   (x772 at the centre, f(centre) − UB), or onto the two least-curved
   directions of the reduced Hessian, showing the flat valley along
   x772 = 0.999 (data `ext_logs/open_run2.npz`; needs a plotting script run
   in a disposable copy).
6. **Box (KAN infeasibility):** the worked example of Section 3.2.1
   (kan_r5_h1_n3, edge x776, interval of b6: ρ₁ ≡ −2.8·10⁻¹⁷), with the table
   of certified edges.
7. **Figure (KAN tolerance artifact):** for kan_r3_h1_n4, the published SCIP
   value, its network value at SCIP's input, the SCIP 10 fixed-input value,
   and [L, U], on one axis.
