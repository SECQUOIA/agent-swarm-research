# SCIP node counts against the predicted tolerance exponents

Date: 2026-09-28. Status: empirical evidence from one solver version,
computed in floating point. It is not a proof and not a certified count.
Scope: the rates in
[scout Sections 3.6–3.7](../../scouting/spatial-bb-theory.md) and the
[review's](../../reviews/spatial-bb-review.md) caveat that objective-cutoff
propagation can escape the lower bounds.

## Summary

The predicted exponents hold in SCIP 10.0.2 when its search matches the
theory's model: best-first node order, incumbent `f*` from the start, and
pruning by bound. Fitted slopes of `log10(nodes)` against `log10(1/eps)` under
that setting (`model`) are:

| Prediction | Instances | Predicted slope | Fitted slope (`model`) | Per-decade node factor (predicted) |
|---|---|---|---|---|
| isolated nondegenerate minimum, `Theta(log(1/eps))` | iso2, iso2c, iso3, iso4 | 0 (linear in `log(1/eps)`) | 0.06–0.10; 9, 10, 40, 92 nodes per decade | additive |
| `p = 1` optimal set | linediag2, lineaxis2, ring2, mccdiag2, conexp2 | 1/2 | 0.50–0.52 | 2.7–4.0 (3.16) |
| `p = 2` optimal set | sphere3, plane3, conexp4 | 1 | 1.01–1.05 (2–3 decades only) | 9.0–11.1 (10) |
| growth `q = (2,4)` / `(4)` | qflat2a / qflat1 | 1/4 | 0.27 / 0.31 (bisection: 0.24 / 0.25) | qflat2a: 1.8–2.1 (1.78) |
| growth `q = (4,4)`, `(2,4,4)` | qflat2b, qflat3 | 1/2 | 0.49–0.51 | 2.8–3.3 (3.16) |
| McCormick, optimal segment transversal to the axes | mccdiag2 | 1/2 for every rule | 0.50–0.52 (default, LP-point and best-first settings: 0.49–0.59) | |
| McCormick, optimal segment aligned with an axis | mccaxis2 | depends on the rule | LP-point branching: 3 nodes for every eps; x1-only bisection: `log`; bisection on both variables: 0.49–0.62 | |

On the seven instances where the Theorem B lower bound applies, no SCIP run
had fewer final leaves than the bound. The smallest ratio of leaves to
bound was 1.59 (qflat1).

Default SCIP departs from the predictions in five ways. Each has an
identified cause:

1. **Isolated minima: the count stops depending on eps.** Below eps between
   1e-4 and 1e-6, default SCIP exhausts the tree (status `optimal`) with a
   fixed node count: 95 for iso2 (from 1e-6) and 341 for iso3 (from 1e-4).
   The cause is plunging in the default node selector. It dives along the
   path to the minimizer, past the depth that eps requires. The dive stops
   only when the box's relaxation gap is below the incumbent's feasibility
   error, about 1e-9. This is consistent with Theorem B, whose bound for
   iso2 at eps = 1e-7 is only 4.3 leaves. With best-first order the count
   grows linearly in `log(1/eps)` again.
2. **Short-window slopes below 1/2 for `p = 1`.** On linediag2 and
   lineaxis2, default SCIP's tail slope over `1e-4..1e-6` is 0.33–0.36. Its
   wide-window slope is 0.46–0.53. The cause is the default node order.
   SCIP's `limits/absgap` is a global stopping test, not a node-pruning rule,
   so the default selector (best estimate with plunging) also processes
   nodes whose bound is already within eps. The excess over `model` shrinks
   as eps falls (factor 3.6, 2.2 and 1.7 at 1e-4, 1e-5 and 1e-6). `model`
   also supplies the incumbent and turns heuristics off; these three changes
   were not separated. The default runs do have an incumbent at `f* -
   9.4e-10`, found by heuristics.
3. **Cutoff propagation, as the review predicted.** On the review's
   instance (isofbbt2, `t^2 - 2t^4` in 2D), default SCIP needs 15 nodes for
   every eps from 1e-2 to 1e-7. Removing cutoff reductions
   (`misc/allowweakdualreds = False`) gives 37. Best-first order without
   propagation grows slowly, from 23 to 35 nodes. SCIP's relaxation of this
   instance does not satisfy (G_alpha) near the minimizer: the secant gap of
   `-2x^4` is `O(w^4)`. So this is not an escape from a proved bound.
   - Removing cutoff reductions changed no `p >= 1` exponent except on the
     face-exact McCormick instance mccaxis2. This matches the Theorem D
     argument: with `UBD >= f*`, a cutoff cannot remove optimal points.
   - On the face-exact McCormick instance, cutoff FBBT shrinks `x1` around
     the optimal segment. It keeps default SCIP at 5 nodes down to
     eps = 3e-6.
4. **Relaxation strengthening that (G_alpha) does not model.** Three
   reformulations make the relaxation exact on the optimal set:
   - *Shared auxiliary variables.* In condisk2 (`min -x1^2-x2^2` on the unit
     disk) the objective and constraint share the `x_i^2` expression nodes,
     so the LP bounds the objective by `w1 + w2 <= 1`. Every setting solves
     it in 1 node.
   - *Shared nodes plus FBBT.* When the disk is written as a norm
     (condisk2soc), FBBT bounds the shared sum, again giving 1 node.
     Switching off nonlinear propagation restores slope 0.54–0.57.
   - *Unexpanded square.* Writing the ring as an unexpanded square
     (`expr/pow/expandmaxexponent = 1`) exposes the convex outer function;
     ring2 then takes 1 node instead of growing like `eps^(-1/2)`.
5. **Variable-lock presolve (`constraints/nonlinear/checkvarlocks = t`).**
   The objective of mccaxis2 is linear in `x2`, and `x2` appears in only one
   constraint. SCIP changes `x2` to binary and solves the instance in 1
   node. The McCormick runs use `checkvarlocks = d`.

The McCormick predictions of scout Section 3.7 hold in SCIP when the
branching rule is controlled:

- LP-point branching (`branching/midpull = 0`) finds the 2-leaf certificate
  on the aligned instance: 3 nodes for every eps.
- x1-only bisection grows like `log(1/eps)` (5 to 45 nodes over six
  decades).
- Bisection on both variables grows like `eps^(-1/2)`.
- On the transversal instance, no setting beats `eps^(-1/2)`.

`cons_nonlinear` ignores variable branching priorities for its own
branching. x1-only branching needed `constraints/nonlinear/branching/external
= True`, which hands candidates to SCIP's generic branching rules.

## 1. Predictions tested

Relaxations with gap at least `alpha * sum_i (y_i-l_i)(u_i-y_i)` (the
(G_alpha) hypothesis) give certificate sizes of order
`integral (f - f* + eps)^(-n/2)`. This yields:

- `Theta(log(1/eps))` at isolated nondegenerate minima;
- `Theta(eps^(-p/2))` for a `p`-dimensional optimal set (Theorem D; this
  also holds with constraints);
- `eps^(-(n/2 - sum_i 1/q_i))` for growth `sum_i |t_i|^(q_i)`.

McCormick relaxations are exact on box faces, so the rate depends on how
the optimal set sits relative to the coordinate hyperplanes (scout 3.7).
The review adds that interval propagation of the objective cutoff uses
information other than the relaxation and can escape the Theorem B bound.

Only coordinates that the relaxation gap involves count as branched
coordinates. By the low-rank remark, the relevant dimension is that of the
optimal set of the value function in those coordinates. conexp2 and conexp4
test this: their gap involves only the log variables.

## 2. Setup

### 2.1 Software

- SCIP 10.0.2 (optimized, 8-byte precision), with SoPlex 8.0.2 as LP solver
  and Ipopt as NLP solver.
- PySCIPOpt 6.2.1, Python 3.13.11, Linux 6.18 (WSL2), x86_64. These are
  recorded in [`results/meta.json`](results/meta.json).
- Runs were single-threaded, with at most 4 in parallel. The total SCIP
  solving time over 2134 runs was 1.76 CPU hours. Other processes loaded the
  machine, which affects times but not counts.
- Re-running five runs reproduced the node and LP iteration counts exactly
  ([`results/determinism_check.log`](results/determinism_check.log)).

### 2.2 Formulation and tolerances

Each instance is `min t` subject to `f(x) - t <= 0`, plus any constraints,
over a box. It is written as a CIP file ([`cip/`](cip/)). CIP input fixes
the expression form: PySCIPOpt's `Expr` would expand `(x1-x2)^4` into
monomials.

Every run sets the following:

| Parameter | Value | Reason |
|---|---|---|
| `limits/absgap` | eps | the theory's absolute tolerance |
| `limits/gap` | 0 | no relative gap |
| `numerics/feastol` | 1e-9 | the default 1e-6 caps the achievable gap; see below |
| `numerics/epsilon`, `numerics/sumepsilon`, `numerics/dualfeastol` | 1e-12, 1e-10, 1e-9 | keep the default ratios to feastol |
| `limits/nodes`, `limits/time` | 100000, 120 s | a sequence stops after its first limit hit; no run hit the time limit |
| `randomization/randomseedshift` | 0 | |

**Why feastol matters.** SCIP accepts points that violate `f(x) <= t` by up
to feastol, so the incumbent can lie up to feastol below `f*`. With the
default feastol of 1e-6 on linediag2, eps = 1e-6 and eps = 1e-8 both end
with status `optimal`, 38766 nodes and primal bound `f* - 9.99e-7`. The
tolerance, not eps, then sets the count. With feastol 1e-9 the counts keep
growing (13751 at 1e-4 and 66001 at 1e-6), and feastol 1e-10 gives similar
counts (12801 and 66331). The probe is in
[`results/tolerance_probe.log`](results/tolerance_probe.log). The sweep
uses eps from 1e-1 to 1e-7 in half-decade steps. The smallest eps is
therefore 100 times the feastol.

**How SCIP applies eps.** In SCIP, `limits/absgap` stops the solve when
primal minus dual bound is at most eps. Nodes are pruned only when their
lower bound reaches the incumbent value. Under best-first order with
incumbent `f*`, the processed nodes are exactly those whose lower bound is
below `f* - eps` (up to ties), which is the theory's model. Under the default selector
(best estimate with plunging) SCIP also processes nodes that are already
within eps.

### 2.3 Settings

Defaults referred to below are: `branching/midpull` 0.75,
`branching/midpullreldomtrig` 0.5 and `branching/clamp` 0.2; the node
selector `estimate` with plunging; `propagating/obbt/freq` 0 (root only);
`expr/pow/expandmaxexponent` 2; and `constraints/nonlinear/checkvarlocks` t.

| Setting | Changes from default |
|---|---|
| `default` | none |
| `nopresolve` | `setPresolve(OFF)` |
| `noprop` | `propagating/{dualfix,genvbounds,nlobbt,obbt,probing,pseudoobj,redcost,rootredcost,symmetry,vbounds}/freq = -1`; `constraints/{nonlinear,linear,varbound}/propfreq = -1`. Presolving still runs. |
| `nocutoffprop` | `propagating/{pseudoobj,rootredcost,redcost,genvbounds}/freq = -1`. Tree search only: pseudoobj presolving still uses the cutoff. |
| `noweakdual` | `misc/allowweakdualreds = False`. This removes all cutoff-based reductions, including those in presolve. |
| `nonlprop` | `constraints/nonlinear/propfreq = -1` |
| `obbtoff`, `obbtall` | `propagating/obbt/freq` = -1, or 1 (every node) |
| `lppoint` | `branching/midpull = 0`: branch at the LP value, clamped to 20–80% of the domain |
| `midpoint` | `branching/midpull = 1`, `branching/midpullreldomtrig = 0` |
| `widestbisect` | `midpoint` plus `constraints/nonlinear/branching/domainweight = 1` and `{violweight,dualweight,pscostweight,vartypeweight} = 0` |
| `model` | `nodeselection/bfs/stdpriority = 1e6`, `nodeselection/bfs/{min,max}plungedepth = 0`, heuristics off, known optimum added before solving (`x*`, `t = f(x*) + 1e-15`) |
| `modelnoprop` | `model` plus `noprop` |
| `toy` | `model` plus `noprop`, `widestbisect` and presolve off (closest to the scout's toy code) |
| `noexpand` | `expr/pow/expandmaxexponent = 1` |
| `withlocks` | `constraints/nonlinear/checkvarlocks = t` (SCIP's default; mccaxis2 otherwise uses `d`) |
| `smallstreps` | `numerics/boundstreps = 1e-6` |
| `xprio`, `xpriomidpoint`, `xpriolppoint`, `xpriotoy` | `chgVarBranchPriority(x1, 10)` plus the named setting |
| `exttoy`, `xprioexttoy` | `toy` without the widest weights, plus `constraints/nonlinear/branching/external = True`; the second adds x1 priority |

### 2.4 Fits

"Nodes" is `SCIPgetNNodes`, the number of processed nodes; LP iterations
and times are also recorded. Each node may solve several LPs, because of
outer-approximation rounds. Two slopes are fitted, both by least squares
of `log10(nodes)` on `log10(1/eps)`:

- the **tail slope** uses the (up to) 5 smallest eps that are at most 1e-3
  and did not hit a limit;
- the **wide slope** uses every such run with eps at most 1e-2.

"Nodes/decade" is the least-squares slope of the node count itself (not its
logarithm) over the tail window. It is the rate for logarithmic growth. A
node count marked `*` below means status `optimal`: the tree was exhausted.

## 3. Instances

All optimal values are exact by construction, as follows:

- `h_c(s) = (s-1)^2((s+1)^2 + c) >= 0`, with a unique nondegenerate zero at
  `s = 1`. SCIP relaxes its concave part `-(2-c)s^2` by secants.
- `g4_d(y) = (y+d)^4 + (y-d)^4 - 12 d^2 y^2 - 2 d^4`, which is identically
  `2y^4`. SCIP sees two convex quartics and a secant-relaxed `-12 d^2 y^2`.
- `z_d(y) = g4_d(y) - 2y^4`, which is identically 0 (a "hidden zero").
  SCIP does not detect this.

[`instances.py`](instances.py) checks each instance: `f(x*) - f*` is at most
2.2e-16 in 40-digit arithmetic, and no grid point lies below `f*`
([`results/instances_check.log`](results/instances_check.log)). Boxes are
asymmetric, so the minimizers are not at dyadic positions and the problems
have no symmetry. The one exception is condisk2 after presolve (below).

| Instance | n | Objective (constraint) | Optimal set, p | SCIP relaxation (from [`transformed/`](transformed/) and nonlinear-handler statistics) |
|---|---|---|---|---|
| iso2, iso3, iso4 | 2–4 | `sum_i h_{c_i}(x_i)`, `c = .5, .7, .6, .8` | `x = 1`, p = 0 | `x_i^4` by tangents, `-(2-c_i)x_i^2` by secants: (G_alpha) with alpha_i = 1.5, 1.3, 1.4, 1.2 |
| iso2c | 2 | iso2 + `0.5 (x1-x2)^4` | `x = 1`, 0 | as iso2, plus a convex coupling term |
| isofbbt2 | 2 | `x1^2 - 2x1^4 + x2^2 - 1.5x2^4` | `x = 0`, 0 | the review's `nondeg1`; the secant gap of `-x^4` is `O(w^4)` at 0, so (G_alpha) fails there |
| linediag2 | 2 | `h_{.5}(x1 - x2)` | segment `x1 - x2 = 1`, 1 | `(x1-x2)^4` kept as a power of a sum; `-1.5(x1-x2)^2` expanded into secants of `x1^2`, `x2^2` and McCormick of `x1 x2`; alpha = 1.5 |
| lineaxis2 | 2 | `h_{.5}(x1) + z_{.375}(x2)` | segment `x1 = 1`, 1 (aligned with an axis) | secants of `-1.6875 x2^2` and `-2x2^4`; alpha = (1.5, 1.6875) |
| ring2 | 2 | `(x1^2 + x2^2 - 1)^2` | unit circle, 1 | expanded to `x1^4+x2^4+2x1^2x2^2-2x1^2-2x2^2+1`; signomial and bilinear handlers |
| mccaxis2 | 2 | `2abs(x1-a) - (x1-a)(x2-b)`, `a = 1/3`, `b = sqrt2-1`, on `[0,1]^2` | `x1 = a`, 1 (aligned) | scout 3.7: `abs` exact, McCormick of `x1 x2` |
| mccdiag2 | 2 | `2abs(x1-x2-a) - (x1-x2-a)(x2-b)` | `x1 - x2 = a`, 1 (transversal) | McCormick of `x1 x2`, convex `x2^2` |
| sphere3 | 3 | `(x1^2 + x2^2 + x3^2 - 1)^2` on a box around `(1,0,0)` | sphere cap, 2 | as ring2 |
| plane3 | 3 | `h_{.5}(x1 + x2 - x3)` | plane, 2 | as linediag2 |
| qflat1 | 1 | `g4_{.375}(x1)` | `x = 0`, growth `q = (4)` | secant alpha = 1.6875 |
| qflat2a, qflat2b, qflat3 | 2, 2, 3 | `h(x1) + g4(x2)`; `g4(x1) + g4(x2)`; `h(x1) + g4(x2) + g4(x3)` | points; `q = (2,4)`, `(4,4)`, `(2,4,4)` | secants in every coordinate |
| conexp2 | 2 | `log(x2) - x1` s.t. `exp(x1) <= x2` | curve `x2 = exp(x1)` on the active constraint, 1 | secant of `log` (gap only in `x2`), `exp` by tangents |
| conexp4 | 4 | two copies of conexp2 | product of two curves, 2 | gap in `x3`, `x4` |
| condisk2 | 2 | `-x1^2 - x2^2` s.t. `x1^2 + x2^2 <= 1` | unit circle, 1 | shares `x_i^2` with the constraint; presolve tightens the box to `[-1,1]^2` and adds a symmetry constraint `x2 <= x1` |
| condisk2soc | 2 | same, constraint `(x1^2 + x2^2)^0.5 <= 1` | unit circle, 1 | same sharing; the norm is handled by the default handler |

**Relaxation check.** With presolve, propagation, OBBT and heuristics off,
SCIP's root bound equals an independently computed secant/McCormick bound
to within 1e-9 on qflat1, iso2, lineaxis2 and qflat2a. On linediag2 it is
9.5e-5 lower. So SCIP's relaxation is no stronger than the secant scheme
the (G_alpha) constants assume
([`results/relax_check.log`](results/relax_check.log)).

## 4. Results

All counts and fits are in [`results/summary.md`](results/summary.md),
generated from the raw runs in [`results/runs.jsonl`](results/runs.jsonl).
That file has one compact JSON object per run: status, nodes, LP iterations,
time, bounds, bound minus `f*`, domain reductions by component, leaves and
SoPlex warnings. The tables below are excerpts. `>N` marks a node-limit hit.

### 4.1 Isolated nondegenerate minima

| Instance | Setting | 1e-1 | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 | Nodes/decade |
|---|---|---|---|---|---|---|---|---|---|
| iso2 | default | 21 | 51 | 51 | 71 | 93 | 95* | 95* | 1 |
| iso2 | midpoint | 41 | 137* | 137* | 137* | 137* | 137* | 137* | 0 |
| iso2 | model | 15 | 25 | 33 | 45 | 55 | 63 | 75 | 9 |
| iso2 | modelnoprop | 23 | 35 | 49 | 55 | 73 | 79 | 93 | 9 |
| iso2 | toy | 55 | 65 | 81 | 93 | 101 | 117 | 157 | 28 |
| iso3 | default | 61 | 161 | 331 | 341* | 341* | 341* | 341* | 0 |
| iso3 | model | 57 | 91 | 119 | 149 | 183 | 209 | 259 | 40 |
| iso4 | default | 197 | 441 | 671 | 1191 | 2301 | 2921 | 3431 | 522 |
| iso4 | model | 173 | 265 | 349 | 437 | 519 | 613 | 699 | 92 |

The `Theta(log(1/eps))` prediction holds under best-first order: the
growth is additive, and the log-log slope falls towards 0. The rate grows
with `n` (9, 40 and 92 nodes per decade), as the exponential-in-`n`
prefactor predicts. The data do not test that constant.

Default SCIP saturates. In the `midpoint` run on iso2, the maximum depth is
34 already at eps = 1e-2. The incumbent is `f* - 9e-10`, so a node is pruned
only when its secant gap `sum_i alpha_i w_i^2/4` is below about 9e-10. That
needs widths of about 3.5e-5, which is `log2(4.2/3.5e-5)`, about 17
bisections in each of the 2 coordinates: depth 34, as observed. The count is
then set by feastol, not eps.

### 4.2 One- and two-dimensional optimal sets

| Instance | Setting | 1e-1 | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 | Tail / wide slope |
|---|---|---|---|---|---|---|---|---|---|
| linediag2 | default | 97 | 741 | 3291 | 13751 | 25731 | 65701 | | 0.33 / 0.46 |
| linediag2 | model | 89 | 359 | 1115 | 3805 | 11893 | 38073 | >100000 | 0.50 / 0.51 |
| linediag2 | obbtall | 69 | 193 | 961 | 4891 | 19521 | 43201 | | 0.48 / 0.59 |
| lineaxis2 | default | 267 | 788 | 3611 | 16541 | 35801 | >100000 | | 0.36 / 0.53 |
| lineaxis2 | model | 227 | 651 | 2427 | 7871 | 24349 | 88601 | | 0.52 / 0.51 |
| ring2 | default | 95 | 471 | 1761 | 5181 | 18291 | 56151 | | 0.52 / 0.52 |
| ring2 | model | 99 | 353 | 1155 | 3769 | 11857 | 37439 | >100000 | 0.50 / 0.51 |
| ring2 | noexpand | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0 |
| sphere3 | model | 79 | 747 | 7475 | 76699 | limit at 3e-5 | | | 1.01 / 1.01 |
| plane3 | model | 271 | 2857 | 31789 | limit at 3e-4 | | | | – / 1.05 |

- **`p = 1`.** Under `model` the per-decade factors are 2.9–4.0 on linediag2,
  lineaxis2 and ring2; the prediction is `sqrt(10) = 3.16`. On these three
  instances, 35 of the 39 sequences (all settings except `noexpand`) have a
  wide slope between 0.43 and 0.60. The exceptions are:
  - widest bisection under the default selector (0.63–0.66), whose counts
    at 1e-3 are 4–5 times the default's and which reached the node limit
    just below 1e-4;
  - `midpoint` on linediag2 (0.39), whose counts are irregular.
- **Alignment.** lineaxis2 (segment aligned with an axis) and linediag2
  (diagonal segment) have the same exponent, as predicted for (G_alpha)
  relaxations.
- **`p = 2`.** Per-decade factors are 9.5–10.3 (sphere3) and 10.5–11.1
  (plane3), against a predicted 10. Only 2–3 decades fit under the node
  limit.
- **ring2 without expansion.** With `expandmaxexponent = 1`, SCIP keeps
  `(w - 1)^2` with `w = x1^2 + x2^2` as a convex function of an auxiliary
  variable. The root bound is then 0 = `f*`, and 1 node suffices.

### 4.3 Flat quartic directions

| Instance (pred.) | default | noprop | model | modelnoprop | toy |
|---|---|---|---|---|---|
| qflat1 (0.25) | 0.36 / 0.34 | 0.27 / 0.29 | 0.31 / 0.33 | – | 0.25 / 0.24 |
| qflat2a (0.25) | 0.18 / 0.30 | 0.14 / 0.21 | 0.27 / 0.28 | 0.25 / 0.25 | 0.24 / 0.23 |
| qflat2b (0.5) | 0.54 / 0.52 | 0.50 / 0.50 | 0.51 / 0.49 | – | 0.53 / 0.61 |
| qflat3 (0.5) | 0.50 / 0.50 | 0.50 / 0.49 | 0.50 / 0.49 | – | limit at 1e-3 |

Entries are tail / wide slopes. The exponent `n/2 - sum_i 1/q_i` holds.
Under `model`, the qflat2a counts grow by factors of 1.8–2.1 per decade
(predicted 1.78).

On qflat1, bisection (`toy`) matches 1/4. SCIP's own branching point gives
0.31–0.36, and its ratio of leaves to the Theorem B bound rises from 1.6
to 3.7 over six decades. Under bisection the ratio stays between 3.3 and
5.0. This fits Theorem C, which is stated for bisection. Whether SCIP's
LP-point-biased rule loses a slowly growing factor, such as a log, was not
resolved.

The default counts on qflat2a are irregular: 109, 381, 501, 931, 1358.

### 4.4 McCormick (face-exact) instances

| Instance | Setting | 1e-1 | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 |
|---|---|---|---|---|---|---|---|---|
| mccaxis2 | withlocks (SCIP default) | 1* | 1* | 1* | 1* | 1* | 1* | 1* |
| mccaxis2 | default (locks off) | 1 | 3 | 5 | 5 | 5 | 211 | 1041 |
| mccaxis2 | lppoint | 1 | 3* | 3* | 3* | 3* | 3* | 3* |
| mccaxis2 | obbtoff | 3* | 3* | 3* | 3* | 3* | 3* | 3* |
| mccaxis2 | noweakdual | 3 | 21 | 61 | 221 | 221 | 401 | 9711 |
| mccaxis2 | xprioexttoy (x1-only bisection) | 5 | 11 | 17 | 25 | 31 | 37 | 45 |
| mccaxis2 | exttoy (bisection, both variables) | 7 | 27 | 91 | 379 | 1017 | 2803 | 10469 |
| mccaxis2 | toy (widest bisection) | 5 | 17 | 59 | 367 | 1363 | 4677 | 21191 |
| mccdiag2 | default | 3 | 11 | 33 | 121 | 328 | 1504 | 4776 |
| mccdiag2 | lppoint | 3 | 11 | 33 | 125 | 319 | 1516 | 4702 |
| mccdiag2 | model | 3 | 11 | 31 | 119 | 319 | 1025 | 3505 |
| mccdiag2 | toy | 5 | 19 | 73 | 405 | 1377 | 4793 | 18351 |

**Aligned segment (mccaxis2).** The scout's three regimes appear:

- The 2-leaf certificate, found by LP-point branching (by scout 3.7, the LP
  minimizer has `x1 = a`): 3 nodes.
- x1-only bisection: logarithmic growth, about 7 nodes per decade.
- Bisection on both variables: slopes of 0.49–0.50 (`exttoy`) and
  0.58–0.62 (`toy`).

Default SCIP falls between these regimes, for reasons of its own:

- With root OBBT off (`obbtoff`), the default branching point also finds
  the 3-node certificate; with root OBBT on it does not. How OBBT changes
  the root LP solution was not checked.
- Cutoff FBBT on `2|x1-a| - (x1-a)(x2-b) <= UBD` shrinks the `x1` range
  around `a`. By an interval-arithmetic estimate (not measured), each round
  multiplies the width by about `max|x2-b|/2 ≈ 0.3`. Without cutoff
  reductions (`noweakdual`), the count rises from 5 to 61 at eps = 1e-3.
- The shrinking stalls. After 5 nodes the dual bound is `f* - 2.4e-6`, so
  the count jumps once eps falls below that. Neither `numerics/boundstreps = 1e-6` nor
  `constraints/nonlinear/maxproprounds = 100` or 1000 removes the stall
  ([`results/maxproprounds_check.log`](results/maxproprounds_check.log)).
  Its cause was not identified.

Branching priorities alone had no effect: `xprio` gives exactly the
`default` counts and `xpriotoy` exactly the `toy` counts.

**Transversal segment (mccdiag2).** The best-first settings and the default
and LP-point rules give slopes of 0.49–0.59. The propagation, OBBT and
`smallstreps` variants give 0.48–0.66. No setting finds an `O(1)`
certificate, which matches the argument that any
McCormick-pruned box can cover only `O(eps^(1/2))` of the diagonal.
`midpoint` and `widestbisect` under the default selector jump between 1e-4
and 1e-5 (281 to 5101), so their tail slopes (0.23–0.28) are not
meaningful.

### 4.5 Constrained instances

| Instance | Setting | 1e-1 | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 | Tail / wide slope |
|---|---|---|---|---|---|---|---|---|---|
| conexp2 | default | 7 | 21 | 63 | 229 | 736 | 2728 | 9768 | 0.55 / 0.54 |
| conexp2 | model | 7 | 21 | 63 | 229 | 709 | 2047 | 7359 | 0.51 / 0.50 |
| conexp4 | model | 43 | 387 | 3709 | 40381 | limit at 3e-5 | | | 1.04 / 1.01 |
| condisk2 | every setting | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0 |
| condisk2soc | default, model, nocutoffprop | 1* | 1* | 1* | 1* | 1* | 1* | 1* | 0 |
| condisk2soc | noweakdual | 3* | 3* | 3* | 3* | 3* | 3* | 3* | 0 |
| condisk2soc | nonlprop | 31 | 226 | 1021 | 3018 | 13281 | 46041 | >100000 | 0.54 / 0.57 |
| condisk2soc | noprop | 41 | 321 | 1151 | 4991 | 17311 | 53700 | >100000 | 0.49 / 0.55 |

- **conexp.** The optimal curve lies on an active curved constraint, and the
  gap involves only the log variable. All 13 settings give 0.50–0.55 for
  conexp2. conexp4 gives 0.97–1.04, except 0.90 for `toy` over only three
  points. So Theorem D's exponent holds with a gap in one coordinate, provided the optimal set is transversal to that
  coordinate's level sets. This agrees with the low-rank remark: the value
  function in the branched coordinates has a `p`-dimensional optimal set.
- **condisk2.** Hypothesis (G_alpha) fails on the optimal set. SCIP's
  extended formulation gives the objective's `x_i^2` and the constraint's
  `x_i^2` the same auxiliary variables `w_i`. The LP then contains
  `w1 + w2 <= 1` together with the objective `-(w1 + w2)`, so the projected
  relaxation is exact on the circle.
- **condisk2soc.** Here the constraint gives `w1 + w2 <= 1` only after FBBT
  bounds the auxiliary variable of the shared sum. Turning off nonlinear
  propagation restores slope 0.5. The objective cutoff is not involved:
  `nocutoffprop` still gives 1 node.

### 4.6 Effect of individual SCIP components

| Component | Effect on counts | Effect on exponent |
|---|---|---|
| Presolve (`nopresolve`) | identical node and LP-iteration counts on all 9 core instances | none |
| Propagation (`noprop`, `noweakdual`, `nocutoffprop`) | for `p >= 1`, `noprop` changes counts by a factor of 0.84–1.55 on most instances, 1.9–4.5 on mccdiag2, and 3.5 at a single eps on lineaxis2 | none for `p >= 1`; removes the eps-independence on isofbbt2 and mccaxis2; condisk2soc changes from 1 node to slope 0.5 (`noprop`, `nonlprop`) |
| OBBT at every node (`obbtall`) | 1.5–3.4 times fewer nodes at 1e-3 (linediag2 961 vs 3291; ring2 1113 vs 1761; iso2 31 vs 51) | none (0.48–0.66 for `p = 1`); consistent with Lemma 0's corollary for same-relaxation OBBT |
| Root OBBT off (`obbtoff`) | equal to default, except mccaxis2 (3 nodes) | none |
| Branching point | midpoint or widest bisection gives 1.5–5 times more nodes than the default at 1e-3; LP-point counts are 0.3–2.8 times the default's, and 3 nodes on mccaxis2 | none under best-first order; irregular jumps under the default selector |
| Node selection and incumbent (`model` vs `default`) | removes plunging overhead and saturation | recovers `log` growth for isolated minima and clean `p/2` slopes |
| Expression expansion (`noexpand`) | ring2: 1 node | the relaxation class changes |
| Variable-lock presolve (`withlocks`) | mccaxis2: 1 node (`x2` becomes binary) | the problem changes |

**Which switch removes cutoff reductions.** `propagating/pseudoobj/freq =
-1` alone does not: pseudoobj's presolve callback still passes a
presolve-time incumbent through the nonlinear FBBT. On isofbbt2 at 1e-5:

- `nocutoffprop` gives 15 nodes;
- adding presolve off gives 37, and adding heuristics off gives 41;
- `noweakdual` gives 37;
- `misc/allowstrongdualreds = False` has no effect.

See [`results/switch_probe.log`](results/switch_probe.log).

### 4.7 Theorem B check

Theorem B's bound, `(n/pi^2)^(n/2) prod_i alpha_i^(1/2) integral (f - f* +
eps)^(-n/2)`, was computed by quadrature
([`thm_bounds.py`](thm_bounds.py), [`results/thm_bounds.json`](results/thm_bounds.json)).
It applies to seven instances whose SCIP relaxation has the (G_alpha) form
with known `alpha_i`.

Final leaves are the open nodes at termination plus the processed leaves.
Across all settings and eps, their ratio to the bound is at least 1.59. For
`model` the ratio is nearly constant over six decades:

| Instance | Ratio range (`model`) |
|---|---|
| iso2 | 6.8–9.8 |
| linediag2 | 15.9–23.7 |
| lineaxis2 | 27.9–40.7 |
| qflat2a | 7.4–9.4 |
| qflat2b | 6.2–9.7 |

Theorem C proves this constant-factor behaviour for bisection. Here it also
holds for SCIP's default branching point, which is not bisection.

Cutoff propagation never pushed a (G_alpha) instance below the bound. We
also did not construct a (G_alpha) instance on which cutoff FBBT is tight at
a nondegenerate minimizer. Heuristically, in SCIP's canonical form the two
properties seem hard to combine:

- SCIP merges equal monomials and expands squares of sums. So a concave
  term `-c x_i^2` centred at a minimizer at 0 is merged with the other
  `x_i^2` terms. The minimizer is then nondegenerate with a secant gap only
  if non-centred terms, such as `(x_i + d)^4`, supply the curvature.
- Non-centred terms, and monomials around a minimizer away from 0, have
  interval enclosures of first-order width. That is too loose for the
  cutoff to shrink boxes.

This is an observation, not a proof.

## 5. Floating-point and tolerance artifacts

- **Incumbents below `f*`.** With feastol 1e-9, heuristic incumbents lie up
  to 1e-9 below `f*` on unconstrained instances. On constrained instances
  the gap reaches 5.5e-9, because the constraint is also violated by up to
  1e-9. This is at most 5.5% of the smallest eps. No lower bound exceeded
  `f*` by more than 1e-15, where 1e-15 is the offset in the supplied known
  solution.
- **Exhausted trees.** Status `optimal` at small eps (420 of 2134 runs)
  means SCIP exhausted the tree at the feasibility-tolerance scale. Counts
  in those runs do not depend on eps; see 4.1.
- **Optimal points cut off.** When the incumbent is below `f*`, cutoff FBBT
  can declare boxes that contain optimal points infeasible. On mccaxis2
  (default) at eps of 1e-6 and smaller, this produced 20–137 "infeasible"
  leaves.
- **SoPlex tolerances.** SoPlex refuses LP tolerances below 1e-10 and says
  so. These messages appeared in 219 runs, at most 33456 times in one run.
  `constraints/nonlinear/tightenlpfeastol` requests the smaller tolerances.
- **Limits and failures.** No run hit the time limit, so all censoring is
  by the deterministic node limit. There were no errors and no restarts.

## 6. Files, commands and checks

All paths are relative to `research-20260928b/bb-complexity/solver-validation/`.

| File | Content |
|---|---|
| [`instances.py`](instances.py) | instance definitions, CIP writer, 40-digit evaluation, and a sanity check when run directly |
| [`run_one.py`](run_one.py) | one run: `python3 run_one.py INSTANCE SETTING EPS [--trans FILE]`; defines all settings |
| [`sweep.py`](sweep.py) | eps sweeps with 4 workers; `--phase2` runs the follow-up tasks |
| [`analyze.py`](analyze.py) | tables, fits, Theorem B ratios and numerical checks |
| [`thm_bounds.py`](thm_bounds.py), [`relax_check.py`](relax_check.py), [`tolerance_probe.py`](tolerance_probe.py) | bound quadrature, root-relaxation check, feastol probe |
| [`cip/`](cip/), [`transformed/`](transformed/) | instance files, and SCIP's presolved problems (`mccaxis2.withlocks.cip` shows the binary `x2`) |
| [`results/runs.jsonl`](results/runs.jsonl) | all 2134 runs, raw |
| [`results/summary.md`](results/summary.md), [`results/runs_fits.json`](results/runs_fits.json) | full tables and fits |

Targeted commands run, from this directory. Earlier exploratory probes used
the same code and are superseded by these.

- `python3 instances.py`: sanity check, logged to `results/instances_check.log`.
- `python3 tolerance_probe.py` on linediag2 and ring2: logged to
  `results/tolerance_probe.log` (run as a scratch copy on identical
  instances).
- `python3 run_one.py <inst> default 1e-3 --trans transformed/<inst>.default.cip`
  for each instance.
- `python3 sweep.py results/runs.jsonl --workers 4`: main sweep, with the
  9 core instances under 12 settings, the 11 others under 4 settings, and
  3 extra pairs. The log is `results/sweep.log`.
- `python3 sweep.py results/runs.jsonl --workers 4 --phase2`: run three
  times as follow-up tasks were added, the last time with `--workers 2`.
  These cover `noweakdual` on the core instances, the x1-priority and
  external-branching variants, `smallstreps`, and the condisk2soc switches.
  The first invocation is logged in `results/sweep2.log`.
- `python3 thm_bounds.py > results/thm_bounds.json`
- `python3 relax_check.py`: logged to `results/relax_check.log`.
- `python3 analyze.py results/runs.jsonl > results/summary.md`
- Five re-runs through `run_one.py`: logged to
  `results/determinism_check.log`.
- Inline `run_one.run` calls for the cutoff switches and propagation
  rounds: `results/switch_probe.log` and `results/maxproprounds_check.log`.

These are empirical checks with one SCIP version and small instances.
Slopes are least-squares fits over 1.5–6 decades; only 2–3 decades were
reachable for `p = 2`. Under best-first order they agree with the predicted
exponents to within about ±0.05. The exception is qflat1 under `model`
(0.31–0.33 against 0.25; bisection gives 0.24–0.25). The fits do not prove
the rates. No project-wide checks were run, and CI was not inspected.
Nothing was committed.
