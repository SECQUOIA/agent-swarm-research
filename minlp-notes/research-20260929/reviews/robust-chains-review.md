# Review of `theory-robust-lb/robust-chains.md`

Date: 2026-09-30. Independent, adversarial review. I did not write the note
or its scripts. All my scripts and logs are in
[`robust-chains-review-checks/`](robust-chains-review-checks/). I wrote the
code from scratch and did not import any of the note's modules.

Labels used below:

- **proved**: checked by hand, line by line;
- **exact**: checked in exact arithmetic (sympy, rationals, or an algebraic
  root evaluated to 30 digits);
- **float**: reproduced in floating point (HiGHS LPs, grids, local
  polishing), not interval-certified.

## Verdict

**Fixes needed.** I found no error in any proof. Theorem A.2, Theorem B.2,
Proposition C.2 and Theorem C.3 are correct as stated. I reproduced every
numerical table I re-ran with independent code (Section 6).

The problems are in how the results are summarized and scoped:

1. **The Part 1 headline is false without (H1).** The note says "Uniform
   chains with symmetric couplings: no lower bound that grows with `n`
   exists". It names the fixed balanced split among the classes covered.
   That holds only under (H1). I give a uniform chain
   `sum u(x_i) + b sum x_i x_{i+1}` with polynomial `u` that violates (H1).
   On it, every balanced-split cover at `eps < 0.0113` has at least `n/2`
   boxes for even `n`. The witness family was checked in exact arithmetic;
   the global optimality of the witnesses was checked in floating point
   (Section 3). Branch-and-bound counts there grow linearly for even `n`.
   Theorem A.2 itself is not affected.
2. **A solver-relevant relaxation escapes Theorem C.3.** The minimal-order
   sparse moment-SOS relaxation of the cubic chiral chain is exact at the
   root (order 2, pair cliques, linear box constraints). This is proved by
   the note's own identity (Section 1). The note should say so in "For
   solvers" and in Section 8. Factorable MINLP relaxations that share
   `x_i^2` are covered.
3. Several smaller inaccuracies and missing steps (Section 7):
   - an incorrect sentence about [R]'s classes;
   - an overstated scope for the volume-counting ceiling;
   - a misreported binding-term order;
   - leftover windows are not handled in Theorem C.3;
   - the base labelled "analytic" uses an LP gap;
   - loose ceilings.

I also offer two strengthenings (Section 4.3):

- the two-point family is optimal **in the continuum** for the per-bond LP
  (exact identity), not only on the grid;
- a fully analytic chiral base approaching 1.0093 per variable for long
  windows, better than the "1.0033 analytic", which depends on an LP value.

## 1. Relaxation class: what is covered and what escapes

Covered, as in [R, Lemmas 1.2–1.3]:

- per-factor envelopes, or anything weaker, for every per-node split of the
  class;
- per-node choice of the split, even with knowledge of `x*`;
- same-relaxation bound tightening at `2n` pieces per round.

For the chiral chain, class (a) is `P_2`, because `u_i = a t^2`. The cubic
bond term cannot be moved between factors except through univariate
functions [R, Lemma 1.1]. The note states all of this correctly.

**Factorable MINLP relaxations are covered.** A SCIP-, BARON- or
Couenne-style reformulation writes `x_i x_{i+1}^2` as `x_i w_{i+1}` with
the auxiliary `w_{i+1} = x_{i+1}^2`. That auxiliary is shared by the two
factors that contain `x_{i+1}`. This is the lifted view of [R, Section 1.3]
with shared lifts `{x, x^2}`, which equals `P_2`. McCormick on each factor
is weaker than the envelope. So Theorem C.3 applies to such solvers, as long
as they do not branch on auxiliary variables and use no cuts on three or
more variables (both excluded by [R]).

**Sparse moment-SOS relaxations escape it (proved).** Each bracket of
Proposition C.1 has the representation

```
(x+y)^2 (b/2 + (g/2)(y-x)) + (ev/2)(x^2+y^2)
  = [ (b/2 - g)(x+y)^2 + (ev/2)(x^2+y^2) ] + (g/2)(x+y)^2 (1+y) + (g/2)(x+y)^2 (1-x),
(a/2) t^2 ± (g/2) t^3 = ((a-g)/2) t^2 + (g/2) t^2 (1 ± t).
```

- The first bracket on the right is a sum of squares when `g <= b/2`.
- The other terms are squares times linear box constraints, of degree 3.
- Exact check: `check1_exact.log`, item 4.

So `f_n` has a Putinar certificate supported on the pair cliques, of degree
at most 4. Sparse Lasserre of order 2 (Waki–Kim–Kojima–Muramatsu, SIAM J.
Optim. 17 (2006) 218–242, bibliographic level) is the lowest order that
accepts a cubic objective. It therefore certifies `f* = 0` at the root.
With the constraint `1 - x^2 >= 0` in place of linear bounds, the same
holds at order 2, using `1 + y = ((1+y)^2 + (1-y^2))/2`.

The note's remark that "adding `t^3` closes the chiral chain" is the
LP-side version of this. The note should state plainly that the standard
moment-SOS approach to a cubic polynomial objective is root-exact here. The
lower bound speaks to factorable MINLP relaxations, not to moment-SOS
solvers.

I found no other per-factor relaxation that defeats Theorem C.3.

## 2. Part 1: Proposition A.1 and Theorem A.2 (proved, no error)

**Proposition A.1 (proved).** All four items follow as written. The
interior factors are `phi`; the end factors are `phi + u/2`. The
alternating configuration gives `f*_n <= (n-1) m + max(u(a), u(c))`, using
the symmetry of `phi`. Item 4 is [R, Proposition 2.1] with `t = 0`.

**Theorem A.2 (proved), step by step.**

- **Step 1.** The chain `kappa sum (x_e - t)^2 <= sigma_k - min u/2 <= Delta_0`
  is correct. The pigeonhole index satisfies `j <= k-1`. Gluing needs at
  least one copy of `t` between the two end blocks, which `n >= 2k`
  guarantees. Then `psi(x_j, t) <= M (x_j - t)^2` gives
  `g*_n <= 2 sigma_k + eps/2`.
- **Step 2.** The boxes have diameter `sqrt(2) h`, the middle factors
  satisfy `psi >= 0`, and `N = ceil(8 sqrt(2) (k-1) L/eps)` gives the
  `eps/4` per block. Correct.
- **Step 3.** The `n < 2k` case is correct. One edge case: for `n = 2` the
  single factor is `phi + u(x_1)/2 + u(x_2)/2`, so `L` must also bound its
  Lipschitz constant. This is trivial to fix.
- Monotonicity in the class gives the final claim.

The size is astronomically large. For UD, `kappa ≈ 0.061`, `Delta_0 ≈ 0.029`
and `M ≈ 1.5` give `k ≈ 2.8/eps`. The note says this. The quasi-polynomial
version is correctly labelled a sketch.

## 3. Counterexample to the Part 1 headline outside (H1)

**Chain WALL.**

```
f_n = sum_i u(x_i) + b sum_i x_i x_{i+1}   on [-1,1]^n,
u(t) = 1.022 t + 0.189 t^2 + 1.774 t^3 + 1.086 t^4,   b = 0.962.
```

I found it by a random search (`check6_wall_search.py`, seeds 1 and 2). The
coupling is symmetric. The bond `phi` is minimized off the diagonal, at
`(-1, c)` and `(c, -1)`, where `c = 0.337723...` is the root of
`u'(c) = 2b` in `(-1, 1)`. So (H1) fails.

**Minimizers.** For even `n`, the grid DP (4001 points, then L-BFGS-B)
gives `f*_n` equal to the value of each of the `n/2` "wall" configurations
`x^(j)`, `j = 1, 3, ..., n-1`, to `1e-10`:

- `x^(j)` is in phase `(-1, c, -1, c, ...)` up to index `j`;
- it is in the shifted phase after `j`;
- its two `-1`'s are adjacent at bond `(j, j+1)`.

The wall positions are exactly degenerate, because `-1` is a bound and
there are no boundary layers. Status: **float** (`check7_wall.log`,
`check7_wall_roots.log`).

**Separation lemma.**

- Any box that contains `x^(j)` and `x^(k)`, `j < k`, also contains
  `x^(j+2)`. Hence it contains the pair box `Q_j` of `x^(j)` and `x^(j+2)`.
- `Q_j` fixes every coordinate except `j+1` and `j+2`, which range over
  `[-1, c]`.
- On `Q_j` the family below is mean-consistent, so it is feasible for the
  fixed balanced split with per-factor envelopes (`P_1` relative to the
  balanced base split). Its value is `f(x^(j)) - 0.0113433`:
  - on `(x_j, x_{j+1})`: `delta(-1, s)`;
  - on `(x_{j+1}, x_{j+2})`: `al delta(-1, c) + (1-al) delta(c, -1)`;
  - on `(x_{j+2}, x_{j+3})`: `be delta(-1, -1) + (1-be) delta(s, -1)`;
  - point masses elsewhere;
  - `s = 0.233524`, `al = 0.07789`, `be = 0.91553`.
- Status: **exact**. `check8b_wall_exact.py` uses the algebraic `c` and
  rational `s`, matches the means exactly, and evaluates the value to 30
  digits. The interior case differs from `n = 4` only by constants.

**Consequence.** For every even `n >= 4` and every `eps < 0.0113`, every
balanced-split cover of WALL has at least `n/2` members. By [R, Lemma 1.3],
a run without tightening rounds needs at least `n/2` leaves. This is a lower
bound that grows with `n` (linearly) for the fixed balanced split on a
uniform chain with a symmetric coupling. The witness family is exact; the
optimality of the witnesses is floating point.

Supporting floating-point data (`check7_wall.log`, `check7_wall_roots.log`):

- **Pair boxes.** All pair boxes for `n = 4..12` have fooling values
  `f* - 0.01132` (15 of 15 pairs at `n = 12`).
- **Balanced-split root gap.** Even `n = 4..14`:
  `0.0205, 0.0410, ..., 0.1231`. Odd `n`: 0. This is consistent with
  Proposition A.1, whose cap here is `phi(-1,-1) - m = 0.30`.
- **B&B leaves, balanced split, `eps = 1e-4`, even `n = 4..16`:**
  - spread rule: 3, 5, 7, 9, 11, 13, 15 (that is, `n - 1`);
  - bisection: 4, 7, 10, 13, 16, 19, 22;
  - odd `n`: 1 leaf.
- **Class (a)** (with `u` in the class) is root-exact for every `n` here:
  0 of the pairs are separated. So this example does not contradict any
  class-(a) claim.

**What this means for the note.**

- The bold item 1 of the Summary must say "under (H1)". The same applies to
  the author's summary ("no split-robust lower bound that grows with `n`
  exists").
- The bullet "This includes the fixed balanced split itself" is true only
  under (H1).
- The remark "Otherwise the optimum contains a domain wall whose position
  is nearly free" is not always true. For `u = t^2 + 1.5 t`, `b = 1.2`, the
  even-`n` frustration sits at a chain end: there are two mirror minimizers
  and no bulk wall (`check6_wall_explore.log`). This negative result is
  informative: walls can be pinned at the ends or free in the bulk.
- My counterexample has degenerate, boundary minimizers. It says nothing
  about chains with a unique, nondegenerate, interior minimizer outside
  (H1).

## 4. Part 3: chiral chain (proved, no error; two strengthenings)

### 4.1 Propositions C.1 and C.4 (exact)

- Both identities hold for `m = 1, 2, 3, 4`. The note checked
  `m = 1, 2, 3`.
- The telescoping formula for `n = 5` is correct.
- The end brackets are correct, and so is
  `f_n = sum W + (a/2)(x_1^2 + x_n^2)`.
- The bracket bound `b/2 - g m >= 0` and `S_m <= m` are correct.
- The Hessian eigenvalue claim is correct.
- C.4(2): the convex-hull and Carathéodory argument is correct. The law
  `(p, -p)` is `P_{2m}`-consistent because the odd moments up to `2m - 1`
  vanish.

### 4.2 Proposition C.2 and Theorem C.3 (proved)

**Two-point family (exact).** At `(0.6, 0.3, 0.05)` and `(0.6, 0.3, 0.1)`,
in rationals:

- the marginals of `p` and `-p` agree in moments 0–2 and differ in the
  third moment (`∓35/144`, `∓2/9`);
- `E W = -5/96` and `-1/30`;
- the end term is `a q = 13/48` and `7/30`.

**Theorem C.3, item 1.** The window equals the `k`-chain for `P_2`, because
`x^2` is in the class and the pinned bond `W(0, y) = (a/2) y^2` is the end
term. For `P_1`, the pinned-window value can only be smaller than the
`k`-chain value. So using `k`-chain values is conservative. Transport needs
affine invariance of `P_d`, which holds. The bound `Lambda_j` is correct.

**Theorem C.3, item 2: missing step on leftover windows.** When `n + 1` is
not a multiple of `k + 1`, the leftover variables form shorter windows.
The proof needs `Phi_r(mu) <= 1` for them.

- In item 1, transport gives this analytically.
- In item 2, `mu = 2.112` violates `2 mu Lambda <= 1`, so this step is
  missing. I checked it: `Phi_r(2.13) <= 1` for every `r <= 6`, by the same
  core and point-mass bound (**float**, `check3_bounds_P2_k7.log`). So the
  stated bound holds.
- The note should add this sentence, or restrict item 2 to
  `n + 1 ≡ 0 mod (k+1)`. If `s = 1` leftover variable remains, pinning the
  end index `n` is allowed; Lemma B.1's proof works unchanged.

### 4.3 Strengthenings (exact)

**(i) The per-bond value is exact in the continuum.** Put
`c1 = -(g-ev)(3g+ev)/(8g)`, `s = x+y` and `d = x-y`. Then

```
W(x,y) + c1 (x - y) + g_inf = g (d/2 + 1)(d/2 - q)^2 + s^2 (b/2 + ev/4 - g d/8)    (sympy: identity)
```

and the right side is at least 0 on `[-1,1]^2` whenever `g <= 2b + ev`.
Consequences:

- The per-bond `P_1` and `P_2` values equal `-(g-ev)^2/(4g)` exactly. The
  two-point family is optimal over all measures, not only on the grid. The
  linear shift explains why `P_1` and `P_2` coincide per bond.
- With the split `r_i = -c1 x_i`, the root gaps of `P_1` and `P_2` satisfy
  `(n-1) g_inf - a q <= Gamma_n <= (n-1) g_inf + c1^2/a`. Here
  `c1^2/a = 0.0151`. Both tables of Section 4.2 lie in this band. So the
  slope `g_inf` is proved for both classes.

**(ii) A fully analytic base.**

- `max |∂_x W| = max |∂_y W| = a + b + g/2` on `[-1,1]^2` when `g <= b/2`
  (proved by checking the linear-in-one-variable maxima). So `Lambda = 2.8`
  is provable, not only "exact".
- With the proved gap `(k-1) g_inf - a q`, the analytic base per variable
  is `exp(((k-1) g_inf - a q)/(2 (2a+2b+g)(k+1)))`. That is:
  - 1.0009 at `k = 7`;
  - 1.0061 at `k = 20`;
  - 1.0080 at `k = 50`;
  - tending to `exp(g_inf/5.6) = 1.0093`.
- The note's "1.0033 analytic" at `k = 7` uses the LP gap 0.1477. That is
  legitimate, and the note says "using the LP-computed window gap". But the
  fully proved base is better for long windows and needs no LP. The author's
  summary line "1.0033 analytic" should carry the same qualification.

## 5. Part 2: Lemma B.1 and Theorem B.2 (proved, no error)

- **Lemma B.1.** Each factor has at most one pinned index, by
  non-adjacency. Combined families are consistent at the pinned indices
  (`delta` marginals) and at the window indices by construction.
- **Theorem B.2.** The `delta`-slab measure, the Lipschitz dependence of
  `V_W` on `p` (only the integrands depend on `p`), and the summation are
  all correct.
- **Gap transport.** The bound `|T t - t| <= 2(1 - rho)` and the bound
  `rho exp(a(1 - rho)) <= 1` for `a <= 1` are correct.
- **Remark "symmetric uniform chains give nothing here".** Correct.

## 6. Numerics reproduced with independent code

My bound code (`cg.py`, and `cg4.py` for quartic factors) uses column
generation. Its factor minimization is exact in `y`, gridded in `x` (97
points) and refined by bounded Brent. This differs from the note's
resultant method. Self-tests against `1201^2` grids over 300 random cubic,
quartic or piecewise factors: maximum excess `9e-16` (`check2_roots_chiral.log`,
`test_cg4.log`).

| Claim | Note | Reviewer | Status |
|---|---|---|---|
| Chiral root gaps, `P_1`/`P_2`/`P_3`, `n = 3..12` | table in Section 4.2 | identical to 6 decimals, both bracket ends | float |
| Per-bond values `5/96`, `1/30`; `P_3 = P_4 = 0` | Section 4.2 | same (241-point grid); continuum dual within `1e-5` | float; exact via 4.3(i) |
| C.4 per-bond values, `m = 2`: `P_3`/`P_4` = 0.0020, 0.0070 | Section 4.4 | 0.002041, 0.007040; continuum dual within `6e-6` | float |
| `gamma_7(theta)`, `theta = 0.2..1` | `chiral_bounds_P2.log` | identical to 5 decimals | float |
| Computed `Phi`, base per variable (`k = 7`) | 0.8314 at `mu = 2.112`; 1.0234 | 0.83139 at 2.112; 0.83083 at `mu = 2.13`; 1.0234 | float |
| Ceiling box (`k = 7`) | `mu0 = 4.079`; 1.078 | `V = 3.47796`, `mu0 = 4.080`; a local search finds `mu0 = 3.069`, ceiling 1.058 | float |
| UD root gaps (balanced, unsplit, class (a)) | Section 2.4 table | identical (e.g. 0.004854, 0.792459, 1.790667) | float |
| PROGRAM-like chains, balanced root-exact | `< 1e-9` | `<= 8e-8` (4 parameter sets, `n = 6, 10`) | float |
| UD B&B, balanced, spread | 11, then 10 for `n = 5..16` | 11, 10, 10, 10, 10, 10, 10 (`n = 4, 5, 6, 8, 10, 12, 16`); 10 at `1e-6` | float |
| UD B&B, balanced, bisect | 12, 14, 17, 23, 29, 35, 47 | identical | float |
| UD B&B, unsplit, `n = 3..7` | spread 8, 17, 27, 40, 55; bisect 15, 42, 47, 68, 102 | identical | float |
| Chiral `P_2` bisect, `n = 4..10` | 3, 8, 16, 38, 84, 190, 433 | identical | float |
| Chiral `P_2` spread, `n = 4..10` | 2, 4, 6, 14, 22, 44, 69 | 2, 4, 5, 15, 22, 42, 68 | float |
| Chiral `P_1` spread, `n = 4..9` | 6, 10, 32, 61, 159, 298 | 6, 10, 32, 61, 159, 297 | float |
| Chiral `P_1` bisect, `n = 4..7` | 32, 142, 455, 1,257 | identical | float |
| Chiral `P_3` | 1 leaf | 1 leaf (`n = 4, 6, 8`) | float |

The spread counts differ by at most 2 leaves, which is expected because the
rule reads a possibly non-unique LP solution. The note's statement that the
chiral counts were "not reproduced by independent code" can now be updated
for `n <= 10` (`P_2`) and `n <= 9` (`P_1`). I did not re-run:

- `n = 11, 12`;
- the `eps = 1e-6` chiral rows;
- the UD class-(a) rows;
- the random uniform search;
- the sparse-narrow runs.

## 7. Smaller issues

1. **Summary item 1, second bullet.** "Every split class considered in [R]
   contains the balanced split" is false. [R]'s `b_d` classes are taken
   relative to the gadget base split (its Theorem 4.3). [R] also considers
   the fixed unsplit split (its Section 2.1). Neither contains the balanced
   split when `u` is not a polynomial of degree at most `d`. The list that
   follows in the note (fixed balanced split, (a), (a0), `b_d` relative to
   the balanced base) is correct. Delete the sentence or restrict it.
2. **Summary "Meaningful base" paragraph.** It says volume-type counting
   "(tilted volume with windows, any reference product measure) is limited
   by corner boxes" and gives at most `exp(c · gap/curvature)`. Only
   Lebesgue reference measures were computed, and Section 5 says
   non-uniform measures "were not optimized". Remove "any reference product
   measure" from that claim, or label it a conjecture.
3. **Section 4.3, binding terms.** "followed by the point-mass term
   (0.8138)" is wrong. At `mu = 2.112`, four core terms exceed 0.8138:
   - `0.7 -> 0.75` and `0.8 -> 0.85`: 0.8284 each;
   - `0.65 -> 0.7`: 0.8201;
   - `0.85 -> 0.9`: 0.8190.

   See the note's own `checks_note.log`.
4. **Ceilings.** These are upper bounds on the method and are loose.
   - A short local search lowers the `k = 7` class-(a) ceiling from 1.078
     to 1.058 per variable (`mu0 = 3.07`).
   - "`mu0` stays near 3.5–4" is therefore not robust, and the large-`k`
     estimate `exp(4 · 0.052) ≈ 1.2` becomes about `exp(3.07 · 0.052) ≈ 1.17`.
   - The direction of the note's claims ("a better search can only lower
     these ceilings") is correct.
5. **Section 2.4, unsplit growth.** "grows by about 1.4 per variable over
   `n = 3..8`" is the last-step ratio. The average over `n = 3..8` is about
   1.57 (8 to 79 leaves with spread, 15 to 144 with bisection).
6. **Section 5, sparse-narrow covers.** The extrapolation `20^{n/3}` rests
   on one size (`n = 8`). There, the worst box is within `1e-7` of the
   tolerance. Larger `n` may need narrower intervals. The conclusion "not
   competitive" stands.
7. **Theorem C.3, item 1.** It could use `Lambda = 2a + 2b + g` (proved,
   Section 4.3(ii)) instead of `2a + 2b + 3g`.

## 8. Literature and novelty

- **Garibaldi and Thieullen.** Bibliographic data checked: Nonlinearity
  24(2) (2011) 563–611 (web search). The other citations agree with my
  recollection; I did not open them.
- **Sparse moment-SOS literature.** This is relevant to the escape in
  Section 1: Waki, Kim, Kojima and Muramatsu (2006), and Lasserre's
  sparse-hierarchy work. The note should cite it in that context.
- **Discrete-time auxiliary functions.** For the `P_d` analogy, the
  discrete-time SOS auxiliary-function framework may be closer than
  Tobasco–Goluskin–Doering. See, for example, Fantuzzi, Goluskin, Huang and
  Chernyshenko, "Bounds for deterministic and stochastic dynamical systems
  using sum-of-squares optimization" (SIAM J. Appl. Dyn. Syst., 2016). I
  checked this only at the level of a search snippet (Imperial repository);
  bibliographic details are not verified.
- **Novelty.** The note's claims are appropriately hedged. I found nothing
  that anticipates the chiral family or the pinning lemma. As always, an
  unsuccessful search does not establish novelty.

## 9. Commands run

All runs were from `reviews/robust-chains-review-checks/`, with
`OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`. They were targeted runs.
No project-wide checks were run, CI was not consulted, nothing was
committed, and the note was not edited.

| Command | Log |
|---|---|
| `python3 check1_exact.py` | `check1_exact.log` |
| `python3 check2_roots.py chiral`; `python3 check2_roots.py ud` | `check2_roots_chiral.log`, `check2_roots_ud.log` |
| `python3 check3_bounds.py 2 7` | `check3_bounds_P2_k7.log` |
| `cat jobs_bb.txt \| xargs -P 8 -L 1 sh -c 'timeout 5400 python3 check4_bb.py $0 $@'` | `check4_bb.log` |
| `python3 check5_bulk.py` | `check5_bulk.log` |
| `python3 check6_wall_explore.py 1.5 1.2`; `python3 check6_wall_search.py S` (`S = 1, 2`) | `check6_wall_explore.log`, `check6_wall_search_{1,2}.log` |
| `python3 test_cg4.py` | `test_cg4.log` |
| `python3 check7_wall.py roots`; `cat jobs_sep.txt jobs_wallbb.txt \| xargs -P 6 -L 1 sh -c 'timeout 5400 python3 check7_wall.py $0 $@'` | `check7_wall_roots.log`, `check7_wall.log` |
| `python3 check8_wall_family.py`; `python3 check8b_wall_exact.py` | `check8_wall_family.log`, `check8b_wall_exact.log` |
| `python3 check9_program_like.py` | `check9_program_like.log` |

Total compute was about 45 minutes of wall time. No single run took more
than about 9 minutes (chiral `P_2` bisect at `n = 10`: 493 s).
