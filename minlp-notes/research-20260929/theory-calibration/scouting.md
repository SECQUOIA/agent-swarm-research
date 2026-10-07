# Discrete calibrations for transcribed optimal-control problems: scouting and first-pass theory

Date: 2026-09-30. Workstream "theory-calibration" of the September 29
program. Status: **scouting note, reviewed, revised, rechecked and revised
again.** An independent review ([`../reviews/calibration-review.md`](../reviews/calibration-review.md),
checks in `../reviews/calibration-review-checks/`) found no false central
claim but one false sentence, missing hypotheses, missing citations and
overstated novelty; Section 10 lists the first revision. A recheck
([`../reviews/calibration-recheck.md`](../reviews/calibration-recheck.md))
found no mathematical error and listed minor fixes R1–R8 (scope, wording,
one citation detail, one numerical-agreement sentence); Section 11 lists the
second revision. A confirmation
([`../reviews/recheck-calibration-confirm.md`](../reviews/recheck-calibration-confirm.md))
found all eight fixes applied correctly and raised four minor wording
points; the root applied them on 2026-09-30 (Section 11.1, not
rechecked). Proofs are complete unless
a statement is labelled "sketch" or "conjecture". All computations
(Example 3.6, Section 5 checks) are floating-point illustrations, not
certified values. Literature entries
marked [v] were checked during this scouting (web page, abstract or local
library copy); [vr] marks entries checked by the reviewer; unmarked entries
are cited from memory and should be checked before reuse.

Cited repository notes:

- [O] open-instances report, [`../open-instances/open-instances-report.md`](../open-instances/open-instances-report.md)
  (dtoc5, lnts, camshape, optcdeg2, lukvle10);
- [W2] COPS report, [`../open-instances-wave2/cops/report.md`](../open-instances-wave2/cops/report.md)
  (chain, catmix);
- [K] consistency note, [`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md);
- [D] decomposition note, [`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md);
- [F] face-exact note, [`../theory-face-exact/face-exact-exponential.md`](../theory-face-exact/face-exact-exponential.md);
- [R] split-robust note, [`../theory-robust-lb/robust-lower-bound.md`](../theory-robust-lb/robust-lower-bound.md);
- [T7] open-theory list, item 7, [`../../literature/topics/open-theory-challenges.md`](../../literature/topics/open-theory-challenges.md).

## Summary

**Unifying notion.** For a transcribed problem
`min sum_t L_t(x_t,u_t) + Phi(x_N)`, `x_{t+1} = f_t(x_t,u_t)`, a *discrete
calibration* is a family of functions `S_t` of the state with stage
residuals `rho_t = L_t + S_{t+1} o f_t - S_t`. Every family gives the valid
bound `B(S) = inf S_0 + sum_t inf rho_t + inf (Phi - S_N)` (Lemma 2.1); a
calibration is a family with `B(S) = f*`. This is Krotov's sufficient
condition for discrete systems (1967), the Bellman inequality of
approximate dynamic programming, and the split relaxation of [K] on the
path of stages. **The notion is classical; its use as a certificate
language for these instances is the contribution.**

**The closed instances in this language (Section 2.4).**

| instance | class of `S_t` | exact windows | classical name |
|---|---|---|---|
| dtoc5 | affine (costates); residual jointly convex | none | discrete Mangasarian |
| lnts | affine for each fixed `h`; minimized Hamiltonian affine in the state | global parameter `h`, by monotonicity | discrete Arrow |
| optcdeg2 | affine on state enclosures | head block (monotone, corner) | Mangasarian fails where `lambda_t < 0` |
| lukvle10 | affine (pair Lagrangian) | 3-pair tail, 2-D interval B&B | fails at the end transient |
| chain | field: `S_k(z,v) = G(v) - v z + k c` | 2-D end window | discrete Weierstrass field of catenaries |
| catmix | concave, piecewise linear, positively homogeneous | none | DP with a concavity prior |
| camshape | comparison: affine calibrations of auxiliary LPs plus a min-plus DP | none | discrete Sturm comparison (disconjugacy) |

**First-pass theorems.**

1. *Affine class.* The affine calibration bound is the Lagrangian dual of
   the dynamics rows. An exact one exists iff some multipliers make every
   stage residual globally minimal on the trajectory (the "only if" needs
   `f*` to be attained); with smooth interior data the multipliers must be
   the discrete costates (Theorem 3.1).
   Discrete Mangasarian and Arrow conditions follow (Theorem 3.2).
   **Mesh-uniform version (Theorem 3.3):** for Euler transcriptions the
   costate calibration is exact for all small `h` if the continuous
   Hamiltonian is convex near the costate path ("Mangasarian with
   margin"), or if the strict pointwise (sufficient) form of the
   Leitmann–Stalford condition (1971) holds together with local convexity
   near the optimal pair (automatic for interior optimal pairs). The
   non-strict condition is also necessary in the limit. Only the
   mesh-uniform perturbation statement was not found stated before; the
   Runge–Kutta extension is a sketch.
2. *Quadratic class.* Local quadratic calibrations exist iff the discrete
   second-order sufficient condition holds, iff the discrete Riccati
   recursion is well defined (no conjugate point) (Theorem 3.4; classical:
   Reid roundabout theorem). **Global version (Theorem 3.5):** with affine
   dynamics and a uniform, possibly indefinite, lower bound on the stage
   Hessians, a well-defined comparison Riccati recursion certifies every
   KKT point as the global minimizer. This is exactly a certificate that
   the problem is convex after the states are eliminated; the quadratic
   calibration is its dynamic-programming form. In a double-well example
   below the threshold (Example 3.6), the costate-affine gap is 2.81–2.86
   and the best affine gap is exactly `J + (1-h) a^2/(4b) - h w(x_0)`
   (about 0.67 for `a = 2`) at every `N`, while the quadratic calibration
   closes the gap to about `1e-15`. The example therefore shows that
   per-stage affine calibrations cannot see hidden convexity; it does not
   certify a genuinely nonconvex problem.
3. *Complexity.* Checking a calibration costs one small global
   minimization per stage plus one problem per exact window (Proposition
   3.7). With Theorems 3.3, 3.5 and 5.2 this is `O(N)` or `O(N log N)` for
   all small `h`. On the
   repository's path family, a calibration with `n - 1` two-variable bag
   checks is exact, while every single-tree certificate with termwise
   McCormick relaxations needs at least `0.57 (5/3)^n` members ([F],
   Theorem 1; [R]) (Corollary 3.8). This separation is relative to the
   relaxation class. **For ODE transcriptions no exponential single-tree
   lower bound is known**, and Houska–Chachuat give mesh-independent
   branch-and-bound run-time bounds under regularity assumptions.
4. *Failure modes.* On a singular stage an exact affine calibration forces
   the state gradient of the switching function to vanish (Proposition
   4.1); this rules out exact affine calibrations, and a positive gap
   would additionally need dual attainment. Under the assumptions of
   Corollary 4.3, near a regular switch with a state-dependent switching
   function the costate calibration fails on a time window of fixed
   duration, that is `Theta(1/h)` stages (Proposition 4.2,
   Corollary 4.3). Convex state constraints are harmless for Theorem 3.2;
   nonconvex ones and 2-D boundary pinches are not (Section 4). An exact
   window is a merged bag; its cost is the difficulty (Proposition 4.4).
5. *Transfer (the most substantive result not found stated before,
   Theorem 5.2).* Suppose the
   continuous problem has an exact, strict `C^4` calibration `S`: `r = 0`
   on an admissible optimal pair and quadratic growth of the
   Hamilton–Jacobi residual `r` in `(x,u)`, on a *compact* state enclosure
   and control set, with interior optimal controls. Suppose also that the
   Euler KKT points converge uniformly. Then for all small `h`
   `S^h_t(x) = S(t_t,x) + (p^h_t - S_x(t_t,x^h_t))^T x` is an **exact**
   discrete calibration. The discrete KKT point is then the unique global
   minimizer of the transcription, whatever the convexity of its stages.
   - Compactness is essential: with `U = R` a strict smooth calibration
     exists while every Euler transcription is unbounded below.
   - Strictness in `x` is essential: non-strict LQ fields can lose
     `Theta(h)` (for example `xdot = -2x + u`, `l = u^2/2`,
     `Phi = x^2/2`); they can be
     exact when a second-order defect has a favourable sign (for example
     `xdot = u`, `l = (u^2 + x^2)/2`), see Remark 5.2(d).
   - On a nonconvex test problem the transferred family is exact for
     `h <= 0.05`, while costate calibrations lose about 8.6.
   - Without the affine correction the loss is `O(h^2)` in the strict case
     when `e_h = O(h)` (Proposition 5.1 gives the `O(h)` upper bound).

**Novelty, honestly.**

- Items 1 and 2 are classical in substance: discrete maximum principle
  with convexity; Krotov; Leitmann–Stalford (1971), whose condition has
  the pointwise condition behind Theorem 3.3 as a sufficient form; Reid
  roundabout theorem; Hilscher–Zeidan.
- Theorem 3.5 is convexity of the condensed problem, which is known in
  substance; it is kept as a reading, not as a result.
- Only the mesh-uniform perturbation statement of Theorem 3.3 was not found
  stated before, and it is modest.
- Theorem 5.2 and Propositions 4.1–4.2 were not found stated before; all
  are elementary. Theorem 5.2 is the one with potential practical weight.

**Recommended next question (Section 7).** *Transfer at switching points:*
for bang-bang problems with finitely many regular switches and a strict
piecewise-smooth field calibration, do transferred calibrations stay exact
outside windows of a bounded number of stages (independent of `h`) around
each switch, so that the whole transcription is certified in
`O(N log N)` plus a constant number of fixed-dimension window problems? A
positive answer would give exact global certificates of linear size
(checked in `O(N log N)`) for large
transcribed bang-bang problems (optcdeg2 is the test case). An extension to
singular arcs would target catmix and the rocket instances, whose listed
dual bounds were found invalid.

## 0. Setting and notation

- Horizon `N`, stages `t = 0..N-1`, states `x_t in R^n`, controls
  `u_t in R^m`.
- Problem (P):
  `min J = sum_{t<N} L_t(x_t,u_t) + Phi(x_N)` subject to
  `x_{t+1} = f_t(x_t,u_t)`, `(x_t,u_t) in Omega_t`, `x_0 in X_0`,
  `x_N in X_N`.
- `Omega_t` is any set that contains `(x_t,u_t)` for every feasible point.
  It holds control bounds, mixed constraints and valid state enclosures
  (for example the interval enclosures of [O, Section 6.2]). `f*` is the
  optimal value.
- Continuous-time source problem, when relevant:
  `min int_0^T l(x,u) dt + Phi(x(T))`, `xdot = g(x,u)`, `u(t) in U`,
  `x(0) = xi`. Explicit Euler with `h = T/N`: `L_t = h l`, `f_t = x + h g`.
- Discrete Hamiltonian `H_t(x,u,p) = L_t(x,u) + p^T f_t(x,u)`; continuous
  Hamiltonian `H(x,u,p) = l(x,u) + p^T g(x,u)`.
- Value functions: cost-to-go `V_t(x)` (tail problem from `x` at time `t`)
  and cost-to-come `Gamma_t(x)` (cheapest feasible head that reaches `x`
  at time `t`). `inf_x (Gamma_t + V_t) = f*` for every `t`.

## 1. Literature

### 1.1 (a) Discrete-time sufficient conditions for global optimality

- **Verification functions for discrete systems.** Krotov, *Sufficient
  conditions for the optimality of discrete control systems*, Doklady AN
  SSSR 172(1), 1967, 18–21 [v]; Krotov, *Global Methods in Optimal Control
  Theory*, Dekker 1996. A Krotov function `phi(t,x)` turns (P) into
  independent stage minimizations of
  `R_t = L_t + phi(t+1, f_t) - phi(t,x)`, which is exactly Definition 2.2
  below. Later work generalizes it with monotone Lyapunov-type functions
  (Irkutsk school; mathnet search results [v]).
- **Bellman inequalities and the LP approach to DP.** Manne (1960); de
  Farias–Van Roy, *The linear programming approach to approximate dynamic
  programming*, Oper. Res. 51 (2003) (the one-sided `2 x` approximation
  bound reproduced in [K]); Lincoln–Rantzer, *Relaxing dynamic
  programming*, IEEE TAC 51 (2006); Wang–O'Donoghue–Boyd, *Approximate
  dynamic programming via iterated Bellman inequalities*, Int. J. Robust
  Nonlinear Control 25(10) (2015) 1472–1496 [v] (quadratic lower bounds on
  value functions from LMIs); Summers et al., *ADP via sum of squares
  programming*, ECC 2013, arXiv:1212.1269 [v].
- **Discrete maximum principle and Mangasarian/Arrow sufficiency.** The
  discrete maximum principle (global minimality of `H_t` in `u`) is *not*
  necessary without (directional) convexity: Halkin, SIAM J. Control 4
  (1966) 90–111; Holtzman, IEEE TAC 11 (1966) [v]. Tamminen, *Strong
  Lagrange duality and the maximum principle for nonlinear discrete time
  optimal control problems*, ESAIM COCV 25 (2019) A20 [v]: strong Lagrange
  duality under a generalized convexity condition, and a maximum principle
  in which the Lagrangian is minimized in both state and control; this is
  the global-minimality form used in Theorem 3.1. Mangasarian (SIAM J.
  Control 4, 1966) and Arrow (Arrow–Kurz 1970) sufficiency in continuous
  time [v, secondary]; discrete-time versions appear in economics texts
  (Sydsæter–Hammond–Seierstad–Strøm, *Further Mathematics for Economic
  Analysis*, 2nd ed. 2008, Ch. 12). The pointwise condition that the
  optimal pair minimizes the augmented Hamiltonian `H + psidot^T x` at
  every time is the pointwise (sufficient) form of the Leitmann–Stalford
  condition: Leitmann–Stalford, *A sufficiency theorem for optimal
  control*, JOTA 8(3) (1971) 169–174 (metadata checked on Crossref; the
  paywalled original was not read). The only restatement read,
  Goenka–Liu–Nguyen (Birmingham WP 20-25, 2020, footnote 26) [v], states
  the theorem with an *integral* hypothesis along admissible pairs. They
  state it for an infinite-horizon discounted maximization problem; in the
  minimization form used here the hypothesis reads
  `int [H(x,u,psi) - H(x*,u*,psi) + psidot^T (x - x*)] dt >= 0`, and a
  transversality condition is also assumed. The pointwise inequality is their Assumption
  6, used "in line with" Leitmann–Stalford; it implies the integral
  condition. This pointwise form underlies Theorem 3.3.
- **Discrete Jacobi, Riccati and Sturm theory.** Hartman, *Difference
  equations: disconjugacy, principal solutions, Green's functions, complete
  monotonicity*, TAMS 246 (1978) 1–30 [v] (sign of Green's functions ⇔
  disconjugacy: the mechanism of camshape). Bohner, *Linear Hamiltonian
  difference systems: disconjugacy and Jacobi-type conditions*, JMAA 199
  (1996) [v] (discrete Reid roundabout theorem: positive definiteness of a
  discrete quadratic functional ⇔ strengthened Jacobi condition ⇔ Riccati
  solution; the key is a discrete Picone identity). Ahlbrandt–Peterson,
  *Discrete Hamiltonian Systems*, Kluwer 1996; Kratz, *Quadratic
  Functionals in Variational Analysis and Control Theory*, 1995.
  Hilscher–Zeidan, *Second order sufficiency criteria for a discrete
  optimal control problem*, J. Difference Equ. Appl. 8 (2002) [v]
  (positivity of the second variation ⇔ no conjugate intervals ⇔ conjoined
  basis ⇔ Riccati, with control constraints and a normality assumption).
- **Discrete fields and discrete Hamilton–Jacobi theory.** Ohsawa–Bloch–Leok,
  *Discrete Hamilton–Jacobi theory*, SIAM J. Control Optim. 49(4) (2011)
  1829–1856 [v] (recovers the Bellman equation and the costate relation
  for discrete optimal control); Marsden–West, *Discrete mechanics and
  variational integrators*, Acta Numerica 2001; Ober-Blöbaum–Junge–Marsden,
  *Discrete mechanics and optimal control: an analysis*, ESAIM COCV 2011
  (arXiv:0810.1386 [v]). No discrete Weierstrass *sufficiency* theory for
  transcriptions was found; the chain lemma of [W2] had no prior found by
  its verifier either.

### 1.2 (b) Verification functions and occupation measures

- **Continuous-time verification and duality.** Carathéodory's "royal
  road"; Klötzler's duality (1979); Vinter, *Convex duality and nonlinear
  optimal control*, SIAM J. Control Optim. 31(2) (1993) 518–538 [v]: the
  optimal value equals the supremum over smooth subsolutions of the HJB
  inequality (the relaxed value when velocity sets are nonconvex); earlier
  Lewis–Vinter (1980), Rubio (1986), Fleming–Vermes (1989).
- **Quadratic Hamilton–Jacobi functions for local sufficiency.** Zeidan,
  *Sufficient conditions for the generalized problem of Bolza*, TAMS 275
  (1983) 561–586 [v] (the Jacobi condition as the existence of a canonical
  transformation to a locally concave–convex Hamiltonian); Maurer–Pickenhain,
  JOTA 86 (1995) 649–667 [v] (a quadratic function satisfying a
  Hamilton–Jacobi inequality as a direct sufficiency criterion).
- **Occupation measures and moment–SOS.** Lasserre–Henrion–Prieur–Trélat,
  *Nonlinear optimal control via occupation measures and LMI-relaxations*,
  SIAM J. Control Optim. 47 (2008) [v]: LMI hierarchy of lower bounds that
  converge to the value under convexity assumptions. Korda–Henrion–Jones,
  *Convergence rates of moment-sum-of-squares hierarchies for optimal
  control problems*, Systems Control Lett. 2017 (arXiv:1609.02762) [v]:
  polynomial subsolutions converge in `L1` at rate `O(1/log log d)`, also
  for the discrete-time counterparts. Henrion–Korda–Kružík–Rios-Zertuche,
  *Occupation measure relaxations in variational problems: the role of
  convexity*, SIAM J. Optim. 34 (2024) 1708–1731 [v]; Korda–Rios-Zertuche,
  *The gap between a variational problem and its occupation measure
  relaxation* (arXiv:2205.14132) [v].
- **Discrete-time versions.** Hernández-Lerma–Lasserre, *Discrete-Time
  Markov Control Processes* (1996) (LP formulation);
  Savorgnan–Lasserre–Diehl, *Discrete-time stochastic optimal control via
  occupation measures and moment relaxations*, CDC 2009 [v]. For trajectory
  optimization: Kang–Xu–Sarva–Liang–Yang, *Fast and certifiable trajectory
  optimization* (STROM), arXiv:2406.05846 (2024) [v]: sparse second-order
  Lasserre relaxations along the horizon chain, certified suboptimality
  below 1%, numerical rather than rigorous certificates.
- **Point for this note.** In discrete time the stage-measure LP with full
  test classes has *no* relaxation gap (consistent measures glue into a
  mixture of trajectories; [K, Theorem 1.1 and Example 1]). The continuous
  occupation-measure gap is a convexification effect that transcription
  removes. What remains in discrete time is only the choice of function
  class for `S_t`.

### 1.3 (c) Global dynamic optimization by branch-and-bound

- **Methods.** Esposito–Floudas (JOGO 2000); Papamichail–Adjiman (JOGO
  2002); Singer–Barton, *Global optimization with nonlinear ODEs* (JOGO
  2006) and *Bounding the solutions of parameter dependent nonlinear ODEs*
  (SISC 2006) [v, local]; Chachuat–Singer–Barton, *Global mixed-integer
  dynamic optimization* (AIChE J. 2005) [v, local] and the IECR 2006
  review; Lin–Stadtherr (2007) [v, local]; Scott–Stuber–Barton,
  generalized McCormick relaxations (JOGO 2011) [v, local];
  Scott–Barton (JOGO 2013); Sahlodin–Chachuat (2011);
  Harwood–Barton (2018) [v, local]; Wilhelm–Le–Stuber (2019) [v, local];
  Song–Khan (2021) [v, local]; Ye–Scott (2024, 2025) [v, local].
- **Complexity in the horizon.**
  - Schaber–Scott–Barton, JOGO 73 (2019) 113–151 [v]: second-order
    convergence of ODE relaxations, with prefactors that can grow over the
    time horizon (method-dependent).
  - Cluster effect: Du–Kearfott (1994); Wechsung–Schaber–Barton, *The
    cluster problem revisited*, JOGO 58 (2014).
  - Houska–Chachuat, *Branch-and-lift* (JOTA 162, 2014) and *Global
    optimization in Hilbert space* (Math. Program. 173, 2019) [v, Theorem 2
    and Example 6 read]: worst-case iteration bounds independent of the
    number of variables, `exp(O(eps^{-1/p} log(1/eps)))` for `p`-times
    differentiable minimizers and `exp(O(log^2(1/eps)))` for smooth ones,
    under Lipschitz and regularity assumptions.
  - Repository: exponential single-tree lower bounds on fixed-coupling
    path families ([F], [D], [R]); see Corollary 3.8 and its caveats. No
    lower bound in `N` for ODE transcriptions was found.
- **Discretization side.** Hager, *Runge–Kutta methods in optimal control
  and the transformed adjoint system*, Numer. Math. 87 (2000) 247–282 [v,
  Theorem 2.1 and Section 3 read]: under smoothness and coercivity, with
  `b_i > 0`, **`U = R^m`, a Mayer cost and a scheme of order `>= 2`** (so
  not Euler), discrete KKT points exist near the continuous solution and
  converge. The bound is for the Hamiltonian-minimizing control
  `u(x^h_k, psi^h_k)`, not for the stage controls (Hager's Remark 2.2). The
  KKT system can be rewritten with transformed costates `chi_j`. With
  control bounds: Hager's Theorem 7.2 (second-order schemes) and
  Dontchev–Hager–Veliov (SINUM 2000). For Euler with control constraints
  the `O(h)` `L^inf` estimate is Dontchev–Hager, SICON 31 (1993) 569–603;
  Dontchev–Hager, Math. Comp. 70 (2001) treats state constraints and gives
  `O(h^{2/3})` [vr]. Semi-Lagrangian HJB schemes:
  Capuzzo-Dolcetta (1983), Capuzzo-Dolcetta–Ishii (1984), Falcone–Ferretti
  (2014). Bang-bang second-order theory: Agrachev–Stefani–Zezza (SICON
  2002), Maurer–Osmolovskii (SICON 2004); Euler error bounds for bang-bang
  LQ: Alt–Baier–Gerdts–Lempio (2012). Singular arcs: Kelley's generalized
  Legendre–Clebsch condition, Goh transformation, Bell–Jacobson (1975).

**What the literature does not contain (as far as found).** A statement
that global optimality of fine transcriptions follows, with certificates
of linear size (checked in `O(N log N)`), from a continuous global sufficient condition; a discrete
Weierstrass field theory usable for rigorous certificates; lower bounds on
branch-and-bound effort in the horizon length for ODE transcriptions.

## 2. Discrete calibrations

### 2.1 Definition and validity

**Definition 2.1.** For functions `S_t : R^n -> R` (`t = 0..N`) define the
stage residuals and the bound

```
rho_t(x,u) = L_t(x,u) + S_{t+1}(f_t(x,u)) - S_t(x)      (t < N),
rho_N(x)   = Phi(x) - S_N(x),
B(S) = inf_{X_0} S_0 + sum_{t<N} inf_{Omega_t} rho_t + inf_{X_N} rho_N.
```

**Lemma 2.1 (validity).** `J(x,u) >= B(S)` for every feasible point.

*Proof.* Along a feasible trajectory the `S` terms telescope:
`J = S_0(x_0) + sum_t rho_t(x_t,u_t) + rho_N(x_N)`. Bound each term by its
infimum over a set that contains it. □

`B` is unchanged by `S_t -> S_t + c_t` (constants telescope). Shifting so
that `inf rho_t = 0` for `t < N` and `inf rho_N = 0` gives the
*subsolution form* `S_t(x) <= L_t(x,u) + S_{t+1}(f_t(x,u))` on `Omega_t`,
`S_N <= Phi`, and `B(S) = inf_{X_0} S_0`.

**Definition 2.2.** `S` is a *calibration* (an exact verification family)
if `B(S) = f*`. It is *exact on a trajectory* `(xbar, ubar)` if every
infimum in `B(S)` is attained at the trajectory.

This is Krotov's discrete sufficient condition and the deterministic,
finite-horizon Bellman inequality. The names "calibration" and "field" are
used below because the chain certificate is literally a discrete field of
extremals (Section 2.4).

### 2.2 Strong duality, max-closure, and the dual

**Lemma 2.2.**

1. (*Strong duality.*) If `Omega_t` are the exact projections of the
   feasible set and the tail values are finite on them, then `S_t = V_t`
   is a calibration.
2. (*Max-closure.*) If `S^1` and `S^2` are in subsolution form, so is
   `max(S^1, S^2)`.

*Proof.* 1: `V_t(x) <= L_t(x,u) + V_{t+1}(f_t(x,u))` is the dynamic
programming inequality, and `inf_{X_0} V_0 = f*`. 2: if
`S_t(x) = S^i_t(x)`, then
`S^i_t(x) <= L_t + S^i_{t+1}(f_t) <= L_t + S_{t+1}(f_t)`. □

**Dual.** With `S_t` restricted to linear spaces `Phi_t` (containing the
constants) and under [K, Theorem 1.1]'s hypotheses (compact stage sets,
continuous data and test functions, which also give attainment of the
minimum), [K, Theorem 1.1] on the path of stage bags gives:
`sup_{S in Phi} B(S)` equals the minimum of `sum_t int L_t dmu_t` over
stage measures `mu_t` on `Omega_t` whose push-forward by `f_t` and the
`x`-marginal of `mu_{t+1}` agree on `Phi_{t+1}`. These are discrete
occupation measures with moment-type consistency. With full classes they
glue into mixtures of trajectories, so the full-class value is `f*`: in
discrete time the only loss comes from the class.

### 2.3 Exact calibrations are band elements; the gap identity

Take `S` in subsolution form and exact (`inf_{X_0} S_0 = f*`, `x_0` fixed
for simplicity).

- Along any feasible tail from `x` at time `t`, telescoping gives
  `tail cost >= S_t(x)`, so `S_t <= V_t`.
- Along any feasible head from `x_0` to `x`, the subsolution inequalities
  give `S_0(x_0) <= head cost + S_t(x)`, so `S_t(x) >= f* - Gamma_t(x)`.

So every exact calibration satisfies `f* - Gamma_t <= S_t <= V_t`: it lies
in the **band** of [K] for the separator `x_t`, whose lower edge is set by
the cost-to-come and upper edge by the cost-to-go, and which is pinched at
the optimal states. Both edges are extended-valued: `V_t = +inf` where no
feasible tail exists and `Gamma_t = +inf` off the reachable set.

**Domain convention.** In `B(S)`, `S_{t+1}` is evaluated on
`f_t(Omega_t)`, which need not lie in the `x`-section `D_{t+1}` of
`Omega_{t+1}`. The separator domain of `S_t` is therefore
`D_t ∪ f_{t-1}(Omega_{t-1})`, and the band edges are `±inf` on parts of it.
[K] assumes one common box and bounded value functions, so its results
carry over as follows, not verbatim:

- **One separator** (all other stages exact DP): the gap of a class
  `Phi_t` is exactly `2 dist_inf(Phi_t, Band_t)`, provided `f*` is finite.
  The proof of [K, Theorem 2.1] uses only `sup(L - U) <= 0` (true because
  `f* = inf(V_t + Gamma_t)`) and clipping, and both work with extended
  values.
- **Whole horizon:** `2 max_t dist(Phi_t, Band_t) <= gap <= 2 inf_{psi exact} sum_t dist(psi_t, Phi_t)`
  ([K, Theorem 3.1]). On unbounded domains the upper bound is typically
  `+inf` (in Example 3.6 affine and quadratic band elements differ
  unboundedly); only the lower bound stays informative.
- **Per-separator band membership is necessary, not sufficient.** [K,
  Proposition 3.3] is a three-stage path where each band contains a
  constant but the constant class has gap 1. The review adds a smooth
  version with an interior optimum (check c5, rechecked here): on
  `[-1,1]^2`, bags `a = 10 s1^2`, `c = 10 s2^2`,
  `b = -5 exp(-|s - (0.8,0.8)|^2/0.01)`. Then `f* = 0` at the origin, the
  costate slopes are forced to 0 (Theorem 3.1(3)), and the constant 0 lies
  in both bands. Yet the costate family gives bound −5, a gap of 5: the dip
  of `b` is hidden in each one-sided value function by `a` or `c`. The
  joint exactness condition is Theorem 3.1(2).
- **Pinch regularity** ([K, Lemma 4.2]). This needs `V_t` and `Gamma_t` to
  be semiconcave near the pinch. [K, Lemma 4.1] proves semiconcavity only
  for product domains, and dynamics tie private variables to the
  separator (`Gamma_{t+1}` is an infimum over the fiber `f_t(x,u) = y`).
  So semiconcavity near the pinch is a **hypothesis** here. It holds
  locally in the smooth interior case, for example for Euler at small `h`
  (where `x -> x + h g(x,u)` is a diffeomorphism) with Lipschitz value
  functions and interior optimal controls. Under it, `V_t` and
  `f* - Gamma_t` are differentiable at an interior optimal state with a
  common gradient, the costate `p_t`. The affine calibration is then the
  tangent plane of the band at the pinch point and is second-order
  accurate there. That this tangent plane lies in each band is necessary
  for exactness of the affine class but, by the example above, not
  sufficient.
- **Riccati band (informal).** Near the pinch point the band is bounded by
  quadratics with Hessians `P^V_t` (the backward Riccati solution: Hessian
  of the cost-to-go of the accessory problem) and `-P^Gamma_t` (the forward
  Riccati solution). With the unperturbed solutions the residual Hessians
  are only positive semidefinite (zero Schur complement), so a strict
  local calibration needs the `eps`-perturbation of Theorem 3.4. The
  forward version is symmetric and not written out.

### 2.4 Dictionary: the closed instances as calibrations

Stage bags are `{x_t, u_t, x_{t+1}}`. For trapezoidal schemes with controls
at the nodes (lnts, chain, catmix) the separator is `(x_t, u_t)`; the
statements below adjust accordingly.

1. **dtoc5** ([O, Section 4]). Affine `S_t(y) = -lambda_{t-1} y` (costate
   slopes). The stage residual is a strictly convex quadratic in `(u,y)`
   because `lambda_t < 1/4`. This is Theorem 3.2 (Mangasarian) with free
   variables, so no enclosures are needed.
2. **lnts** ([O, Section 3]). For fixed `h` the dynamics are linear in the
   state, so the minimized Hamiltonian is affine in the state (Arrow). The
   per-stage minimization over `theta` has the closed form
   `-sqrt(w^2 + b^2)`. Here the calibration proves *infeasibility* of
   every `h <= h2` (a calibration of the zero-cost feasibility problem with
   `B(S) > 0`). The global separator `h` is handled by monotonicity, which
   acts as a one-dimensional exact window.
3. **optcdeg2** ([O, Section 6]). Affine `S_t` from costates, with stage
   minimization over the interval state enclosures. The `v`-terms
   `A_t v^2 + B_t v`, `A_t = 0.2 h lambda_t`, are concave where
   `lambda_t < 0`, so Mangasarian fails on the first 3092 and last 2710
   stages. In band terms, no affine function lies in the band there. The
   head window `t < 3080` is made exact: `S_t` for `t < 3080` is replaced by
   the head's value function with terminal cost `S_3080` (Proposition 4.4),
   evaluated by a coordinatewise-monotonicity argument (every reduced
   gradient positive over the reachable box, so the minimum is at the
   corner). The tail window was not closed (gap 6.1e-3).
4. **lukvle10** ([O, Section 7]). A recurrence without control and a free
   initial pair. The state is the pair `(x_j, x_{j+1})`; `S` is affine in
   it (the pair Lagrangian). The stage residuals are quadratic in
   `x_{j+1}` because the map is quadratic. They are nonconvex only at the
   end transient; a 3-pair exact window with 2-D interval branch-and-bound
   on the entry state closes the gap.
5. **chain** ([W2, Section 2]). State `(z_k, v_k)` (height of the polyline
   vertex and cumulative weight `v_k = V + sum_{j<k} lambda_j`). Summation
   by parts gives stage cost `(v_{k+1} z_{k+1} - v_k z_k) - V_k dz_k`, and
   the calibration lemma gives
   `S_k(z, v) = G_{H'}(v) - v z + k c`,
   `G(v) = (v sqrt(H'^2+v^2) + H'^2 asinh(v/H'))/2`, `c = 2 G(h/2)`. This is a
   discrete Hamilton–Jacobi function in the extended state (height,
   cumulative length). Its continuous counterpart
   `S(x,z,v) = G(v) - v z - H' x` solves the Hamilton–Jacobi equation of
   the catenary: with `s = sqrt(1+z'^2)`,
   `z s + S_z z' + S_v s = sqrt(H'^2+v^2) s - v z' >= H'` with equality at
   `z' = v/H'`, so `S_x + min(...) = 0`. The vertical costate `S_z = -v` is
   the cumulative weight: a *configuration-dependent* tension multiplier.
   The two field parameters `(V, H')` are chosen per box of the 2-D end
   window `(z_1, z_N)`. The fixed-multiplier (affine) length Lagrangian
   fails because the length row is effectively reverse-convex ([W2]).
6. **catmix** ([W2, Section 3]). Linear homogeneous dynamics
   `y_i = M(u_i) y_{i-1}` with `M >= 0` on the positive quadrant and linear
   terminal cost. The value functions are concave and positively
   homogeneous. Proposition 2.3 below shows that chord interpolants on rays
   are genuine calibrations when they are concave; the certificate of [W2]
   uses concavity of the *true* value functions instead (induction
   `W_i <= V_i`), which is equally valid.
7. **camshape** ([O, Section 5]). A comparison certificate rather than a
   stage calibration of (P):
   - the bound `u_j >= S_j` is the Lagrangian bound of the auxiliary LP
     `min u_j` over the linear rows `e_k(u) >= 0`, with multipliers equal
     to the Green's function weights `U_{j-1-k}(c/2)`; the Lagrangian is
     constant in `u`, so the bound is exact;
   - the multipliers must be nonnegative (inequality rows), and
     `U_m(c/2) >= 0` for `m <= n-1` is disconjugacy of the recurrence
     `z_{j+1} - c z_j + z_{j-1} = 0` on `[0, n]` (Hartman 1978). So the
     certificate's validity condition is a discrete Jacobi condition;
   - the objective is decreasing in each `u_j`, and a min-plus DP handles
     the slope rows exactly.

**Proposition 2.3 (concave chord calibrations).** Let `y_i = M_i(u) y_{i-1}`
with `M_i(u)` entrywise nonnegative for `u in U`, state cone
`K = R^2_+`, and rays `r_1, ..., r_J` ordered in `K` and spanning it. Let
`W_i` be positively homogeneous and linear on each cone
`cone(r_j, r_{j+1})`. If every `W_i` is concave on `K`, `W_N <= Phi` on `K`,
and `W_{i-1}(r_j) <= min_{u in U} W_i(M_i(u) r_j)` for all `j`, then `W` is
in subsolution form: `W_{i-1}(y) <= W_i(M_i(u) y)` for all `y in K`,
`u in U`.

*Proof.* Write `y = s r_j + t r_{j+1}` with `s, t >= 0`. Then
`W_{i-1}(y) = s W_{i-1}(r_j) + t W_{i-1}(r_{j+1}) <= s W_i(M r_j) + t W_i(M r_{j+1}) <= W_i(M y)`.
The last step is superadditivity (concavity plus positive homogeneity) and
linearity of `M_i(u)` in `y`. □

Computed ray values can be turned into a genuine calibration by replacing
them with the largest concave homogeneous function below them. This must
be done backward, stage by stage: lowering `W_i` can break
`W_{i-1}(r_j) <= W_i(M r_j)`, so `W_{i-1}` must be recomputed from the
lowered `W_i`. The loss accumulates over the stages and is bounded by the
concavity defects of the computed values.

**Function classes that occurred.** Affine (costates) — dtoc5, lnts,
optcdeg2, lukvle10, and the non-dynamic ex6_2_x and pricing050
certificates; field-type, affine in one state with a nonlinear coefficient
of another — chain; concave piecewise linear — catmix; comparison
(auxiliary affine calibrations with sign conditions) — camshape; full
class on a few separators (exact windows) — optcdeg2, lukvle10, chain,
lnts (in `h`). Quadratic (Riccati) calibrations were not needed by any
closed instance. The balanced split that solves the repository's path
family at the root ([R, Proposition 2.1]) is a calibration whose separator
functions are multiples of the unary terms (quadratic when `kappa = 0`).

## 3. First-pass theorems

### 3.1 Affine calibrations

**Theorem 3.1 (affine class).** Let `S_t(x) = p_t^T x`. Then:

1. `rho_t = H_t(x,u,p_{t+1}) - p_t^T x`, and `B(p)` is the Lagrangian dual
   function of (P) with the dynamics rows dualized (multiplier `p_{t+1}` on
   `f_t(x_t,u_t) - x_{t+1} = 0`) and the sets `Omega_t`, `X_0`, `X_N` kept.
   So `sup_p B(p)` is the Lagrangian dual bound.
2. If there are a feasible `(xbar, ubar)` and `p` such that
   `(xbar_t, ubar_t)` minimizes `rho_t` over `Omega_t` for every `t`,
   `xbar_0` minimizes `p_0^T x` over `X_0`, and `xbar_N` minimizes
   `Phi - p_N^T x` over `X_N`, then the affine family is exact and
   `(xbar, ubar)` is a global minimizer. Conversely, **if `f*` is
   attained**, every exact affine family has this property at every global
   minimizer. (Without attainment an exact family need not produce a
   trajectory that minimizes the residuals.)
3. Let `(xbar, ubar)` be a global minimizer (so `f*` is attained and the
   converse in 2 applies). If the data are `C^1`, `xbar_t` is interior to
   the `x`-section of `Omega_t` for `1 <= t <= N-1`, and `xbar_N` is
   interior to `X_N`, then the slopes of any exact affine calibration are
   the discrete costates: `p_t = grad_x L_t + (d_x f_t)^T p_{t+1}` at
   `(xbar_t, ubar_t)` for `1 <= t <= N-1`, and `p_N = grad Phi(xbar_N)`.
   These slopes are unique. With `x_0` fixed, `p_0` cancels from `B(p)` and
   is not determined. With terminal constraints `p_N` ranges over
   `grad Phi + N_{X_N}(xbar_N)`, as in optcdeg2 where one parameter is
   free.

*Proof.* 1: `J + sum_t p_{t+1}^T (f_t - x_{t+1}) = sum_{t<N} [H_t(x_t,u_t,p_{t+1}) - p_t^T x_t] + p_0^T x_0 + Phi(x_N) - p_N^T x_N`.
With `x_0` fixed the copy `x_0 in X_0` is immaterial; otherwise `B(p)` also
dualizes it against the `x`-section of `Omega_0`.
2: this is [K, Proposition 5.1(2)] on the path: at a feasible point the
residual sum equals `J`, and attained infima give `J(xbar) = B(p) <= f*`.
For the converse, at a global minimizer `x*` the residual sum equals
`f* = B(p)`, so every term sits at its infimum.
3: interior minimality of `rho_t` in `x` gives the adjoint equation. □

**Theorem 3.2 (discrete Mangasarian and Arrow conditions).** Let
`(xbar, ubar, p)` satisfy the KKT conditions of (P) in the form
`0 in grad_{(x,u)} H_t(xbar_t,ubar_t,p_{t+1}) - (p_t, 0) + N_{Omega_t}(xbar_t,ubar_t)`
and `0 in grad Phi(xbar_N) - p_N + N_{X_N}(xbar_N)`, with `x_0` fixed.

1. (*Mangasarian.*) If `Omega_t` and `X_N` are convex, `H_t(.,.,p_{t+1})`
   is convex on `Omega_t`, and `Phi` is convex on `X_N`, then
   `S_t = p_t^T x` is exact on the trajectory, which is globally optimal.
2. (*Arrow.*) Let `H^0_t(x,p) = inf {H_t(x,u,p) : (x,u) in Omega_t}`. If
   `ubar_t` attains it at `xbar_t`, and
   `H^0_t(x,p_{t+1}) >= H^0_t(xbar_t,p_{t+1}) + p_t^T (x - xbar_t)` on the
   `x`-section `D_t` of `Omega_t` (for example `H^0_t(.,p_{t+1})` convex and
   differentiable at `xbar_t` with gradient `p_t`), and the terminal
   condition of item 1 holds, the same conclusion follows.

*Proof.* 1: `rho_t` is convex on `Omega_t` and the KKT inclusion is its
first-order optimality condition at `(xbar_t,ubar_t)`. 2:
`rho_t(x,u) >= H^0_t(x,p_{t+1}) - p_t^T x >= H^0_t(xbar_t,p_{t+1}) - p_t^T xbar_t = rho_t(xbar_t,ubar_t)`.
Apply Theorem 3.1(2). □

dtoc5 is case 1 with `Omega_t = R^2`; lnts is case 2 with `H^0` affine in
the state. Convex pure state constraints `x_t in D` are covered by case 1:
their discrete multipliers are the normal-cone terms.

**Definition (pointwise Leitmann–Stalford condition; "SGM" below).** The
continuous problem satisfies it on `D x U` along `(x*, u*, psi)` if for
every `t`, `(x*(t), u*(t))` minimizes
`phi_t(x,u) = H(x,u,psi(t)) - grad_x H(x*(t),u*(t),psi(t))^T x` over `D x U`.
Along the adjoint equation this is pointwise minimality of the augmented
Hamiltonian `H + psidot^T x`: the pointwise (sufficient) form of the
Leitmann–Stalford condition (JOTA 8, 1971). The restatement read for this
note (Goenka–Liu–Nguyen, Section 1.1) assumes only the time integral of
this inequality along admissible pairs, together with a transversality
condition. The pointwise condition is
weaker than joint convexity of `H(.,.,psi(t))` (Mangasarian). The name SGM ("stage-wise
global Mangasarian") is kept below only as a label. *Strict SGM* adds
`phi_t(x,u) - phi_t(x*(t),u*(t)) >= c (|x - x*(t)|^2 + |u - u*(t)|^2)`. The
discrete global form of the condition (Theorem 3.1(2) with affine `S`) is
Tamminen's "Lagrangian minimized in state and control" and a special case
of Krotov's conditions. What Theorem 3.3 adds is only the mesh-uniform
perturbation statement.

**Theorem 3.3 (mesh-uniform exactness of costate calibrations; Euler).**
Assume:

- (A1) `D` and `U` are compact and convex, and `D` contains every state of
  every feasible point of the transcriptions (an enclosure); stage sets
  `Omega_t = D x U` (`{xi} x U` at `t = 0`);
- (A2) `l, g in C^2` near `D x U`; `Phi` convex and `C^1`; the continuous
  solution has `x*(t) in int D`;
- (A3) Euler KKT points `(x^h, u^h, p^h)` exist with
  `e_h = max_t (|x^h_t - x*(t_t)| + |u^h_t - u*(t_t)| + |p^h_{t+1} - psi(t_t)|) -> 0`
  (for example under the coercivity assumptions of Dontchev–Hager, SICON
  1993, which gives `O(h)` with control constraints; only `e_h -> 0` is
  used).

Then:

1. (*Convex case.*) If `H(.,.,p)` is convex on `D x U` for all `p` with
   `dist(p, psi([0,T])) <= delta`, then for all `h` with `e_h <= delta` the
   calibration `S_t = p^h_t^T x` is exact and `(x^h, u^h)` is a global
   minimizer of the transcription.
2. (*SGM case.*) If strict SGM holds and `H(.,.,p)` is convex on
   `B_{2 delta}((x*(t),u*(t))) ∩ (D x U)` for `|p - psi(t)| <= delta`, then
   the same conclusion holds for all sufficiently small `h`. The local
   convexity hypothesis is automatic when `x*(t)`, `u*(t)` are interior
   (strict SGM then gives `grad^2 H >= 2cI` at the optimal pair, and
   continuity does the rest). It is a real extra hypothesis when
   `u*(t) in ∂U`. In the SGM case the stage problems are in general
   nonconvex away from the optimal pair, so each costs a small global
   minimization, not a convex program.
3. (*Necessity.*) If the costate calibrations are exact on `(x^h, u^h)` for
   a sequence `h -> 0` along which (A3) holds, then SGM (non-strict) holds
   at every continuity point of `u*` (with one-sided limits otherwise).

*Proof.* The residual is
`rho_t(x,u) = h l + p_{t+1}^T (x + h g) - p_t^T x = h [H(x,u,p^h_{t+1}) - q^h_t^T x] =: h phi^h_t`,
with `q^h_t = (p^h_t - p^h_{t+1})/h = grad_x H(x^h_t,u^h_t,p^h_{t+1})` by the
discrete adjoint equation, and the `u`-part of the KKT conditions is
`0 in grad_u H + N_U`.

1. `phi^h_t` is convex on `D x U` and satisfies first-order optimality at
   `(x^h_t,u^h_t)`. The terminal residual `Phi - p^h_N^T x` is convex with
   `p^h_N = grad Phi(x^h_N)`. Apply Theorem 3.1(2).
2. With `G = max |g|`, `R_D = max_{x in D} |x|` and `L_H` a Lipschitz constant
   of `grad_x H`, `|phi^h_t - phi_{t_t}| <= K e_h` on `D x U` with
   `K = G + L_H R_D`. Also `|phi(x^h_t,u^h_t) - phi(x*(t_t),u*(t_t))| <= L e_h`.
   For `(x,u)` at distance `>= delta` from `(x^h_t,u^h_t)` and
   `e_h <= delta/2`, strict SGM gives
   `phi^h_t(x,u) - phi^h_t(x^h_t,u^h_t) >= c delta^2/4 - (2K + L) e_h > 0`
   for small `h`. On the ball of radius `delta` around `(x^h_t,u^h_t)`,
   which lies in `B_{2 delta}((x*,u*))`, `phi^h_t` is convex and first-order
   optimal at `(x^h_t,u^h_t)`, so it is minimal there on the convex set
   `ball ∩ (D x U)`. Together, `(x^h_t,u^h_t)` minimizes `phi^h_t` on
   `D x U`.
3. `phi^h_t -> phi_t` uniformly and the minimizers converge, so the limits
   are minimizers. □

A numerical sanity check by the review (check c1): in the double well of
Example 3.6 with `x_0 = 1.3`, the trajectory stays in
`|x| >= sqrt(a/(2b)) = 1` (`min x = 1.068`), where `w` equals its convex
envelope, so SGM holds. (This is the relevant region, not the smaller
concave region `|x| < 0.577`.) The costate-affine gap is `<= 2.2e-16` at
`N = 50, 200, 1000`, as item 2 predicts. With `x_0 = 0.3` SGM fails and the
gap is 2.8–2.9.

*Runge–Kutta and trapezoidal schemes (sketch).* The algebra is exact; the
convergence input is not supplied by the cited theorem.

- For an `s`-stage scheme with `b_i > 0`, dualize the stage equations
  `Y_i = x_k + h sum_j a_ij g(Y_j,U_j)` (multipliers `lambda_i`) and the
  update (multiplier `psi_{k+1}`). The coefficient of `x_k` vanishes
  identically by Hager's relation `psi_k = psi_{k+1} + sum_i lambda_i`. The
  Lagrangian separates into node terms
  `h b_i H(Y_i,U_i,chi_i) - lambda_i^T Y_i` with Hager's transformed
  costates `chi_i = psi_{k+1} + sum_j a_ji lambda_j / b_i`.
- So the proof of Theorem 3.3 goes through with `H` evaluated at `chi_i`,
  **provided the stage values `(Y_i, U_i, chi_i)` converge uniformly**.
- Hager's Theorem 2.1 does not supply this. It assumes `U = R^m`, a Mayer
  cost and order `>= 2`, and it bounds the Hamiltonian-minimizing control
  `u(x^h_k, psi^h_k)`, not the stage controls `U_i` (his Remark 2.2: those
  may converge more slowly). With control bounds, Hager's Theorem 7.2
  (second-order schemes) or Dontchev–Hager–Veliov (2000) are the relevant
  inputs; this link is not checked.
- For the trapezoidal rule with controls at the nodes (lnts, chain), the
  Lagrangian separates by node with `H` at the averaged costate
  `(p_t + p_{t+1})/2`.

### 3.2 Quadratic calibrations

Let the data be `C^2` and let `(xbar, ubar, p)` be a KKT point with `x_0`
fixed, `x_N` free, and no active constraints. Write `A_t = d_x f_t`,
`B_t = d_u f_t` and let `Q_t, E_t, R_t` be the `xx`, `xu`, `uu` blocks of
`grad^2 H_t(.,.,p_{t+1})` at `(xbar_t,ubar_t)`, with `Q_N = grad^2 Phi(xbar_N)`.
The accessory functional is

```
Q(xi, eta) = sum_{t<N} [xi_t; eta_t]^T [[Q_t, E_t], [E_t^T, R_t]] [xi_t; eta_t] + xi_N^T Q_N xi_N
on  {xi_0 = 0,  xi_{t+1} = A_t xi_t + B_t eta_t}.
```

**Theorem 3.4 (local quadratic calibrations; classical in substance).** The
following are equivalent:

1. `Q` is positive definite on its subspace (the discrete second-order
   sufficient condition);
2. the Riccati recursion `P_N = Q_N`,
   `P_t = Q_t + A_t^T P_{t+1} A_t - (E_t + A_t^T P_{t+1} B_t)(R_t + B_t^T P_{t+1} B_t)^{-1}(E_t + A_t^T P_{t+1} B_t)^T`
   is well defined with `R_t + B_t^T P_{t+1} B_t > 0` for `t = 0..N-1`;
3. there is a quadratic family
   `S_t(x) = c_t + p_t^T (x - xbar_t) + (1/2)(x - xbar_t)^T Ptilde_t (x - xbar_t)`
   whose residuals have zero gradient and positive definite Hessian at
   `(xbar_t, ubar_t)` (at `t = 0`: in `u`), with `grad^2 (Phi - S_N) > 0`.

Each implies that `xbar` is a strict local minimizer with quadratic growth,
certified on a neighbourhood by `S`.

*Proof.* (1 ⇒ 2) Positive definiteness of `Q` implies positive definiteness
of the tail functional from `t` on `{xi_t = 0}` (extend by zero before `t`).
So the tail minimum over `eta_t, ..., eta_{N-1}` is attained for every
`xi_t` and equals `xi_t^T P_t xi_t`. The recursion is the DP step, and
`R_t + B_t^T P_{t+1} B_t` is the Hessian in `eta_t` of the tail functional at
`xi_t = 0` after minimizing the later controls, hence positive definite.
(2 ⇒ 3) The data of 2 form an open set, so 2 also holds for the data
`Q_t - eps I`, `R_t - eps I`, `Q_N - eps I` for small `eps > 0`; let `Ptilde`
be that solution and `c_t` the trajectory's cost-to-go. The gradient of
`rho_t` at the trajectory is zero by the KKT conditions. Its Hessian is
`K_t = [[Q_t + A^T Ptilde_{t+1} A - Ptilde_t, E_t + A^T Ptilde_{t+1} B], [., R_t + B^T Ptilde_{t+1} B]]`.
`K_t - eps I` has a positive definite `uu` block and zero Schur complement,
so `K_t >= eps I`. Terminal: `grad^2(Phi - S_N) = eps I`.
(3 ⇒ 1) Telescoping gives
`J(x,u) - J(xbar,ubar) = sum_t [rho_t - rho_t(xbar_t,ubar_t)] + [rho_N - rho_N(xbar_N)] >= (eps/2) sum (|x_t - xbar_t|^2 + |u_t - ubar_t|^2) - o(.)`
near the trajectory: quadratic growth. For an equality-constrained NLP
with linearly independent constraint gradients (always true here: the
Jacobian contains `-I` in `x_{t+1}`), quadratic growth is equivalent to 1. □

Bohner (1996) and Hilscher–Zeidan (2002) prove the equivalence 1 ⇔ 2 (with
more general boundary conditions and control constraints); item 3 is its
calibration reading. As noted in Section 2.3, the backward Riccati solution
is the upper end of the local band; the forward recursion gives the lower
end and, symmetrically, another local calibration (not written out).

**Theorem 3.5 (global quadratic calibrations by LQ comparison).** Let
`f_t(x,u) = A_t x + B_t u + d_t` be affine, `Omega_t` and `X_N` convex, `x_0`
fixed, and suppose `grad^2 L_t >= M_t = [[Qh_t, Eh_t], [Eh_t^T, Rh_t]]` on
`Omega_t` and `grad^2 Phi >= Qh_N` on `X_N`, where `M_t` may be indefinite.
If the Riccati recursion of Theorem 3.4(2) with data `(A_t, B_t, M_t, Qh_N)`
is well defined with `Rh_t + B_t^T P_{t+1} B_t > 0`, then every KKT point
`(xbar, ubar, p)` of (P) (with normal cones) is a global minimizer, and
`S_t(x) = c_t + p_t^T (x - xbar_t) + (1/2)(x - xbar_t)^T P_t (x - xbar_t)` is
an exact calibration.

*Proof.* The dynamics are affine, so
`grad^2 rho_t = grad^2 L_t + [A B]^T P_{t+1} [A B] - diag(P_t, 0) >= M_t + [A B]^T P_{t+1} [A B] - diag(P_t, 0) >= 0`
by the Schur complement, as in Theorem 3.4. So `rho_t` is convex on
`Omega_t`, and the KKT inclusion is its first-order optimality condition
at the trajectory. The same holds for `Phi - S_N`, since `P_N = Qh_N`.
Apply Theorem 3.1(2), which holds for any family `S`. □

**What Theorem 3.5 is: convexity of the condensed problem.** With affine
dynamics the states are affine functions of the controls, the feasible set
in `u` is convex, and the reduced objective `J(u)` has Hessian
`sum_t z_t^T grad^2 L_t z_t + zeta_N^T grad^2 Phi zeta_N` along the (exact)
trajectory directions `z_t = (zeta_t, eta_t)`. This is at least the
comparison LQ form, which is positive definite iff the comparison Riccati
recursion is well defined with positive pivots (Theorem 3.4, 1 ⇔ 2, for the
data `(A, B, M, Qh_N)`). So the hypotheses of Theorem 3.5 are exactly a
certificate that the problem is strictly convex **after the states are
eliminated**. "Every KKT point is a global minimizer" is then immediate,
and the quadratic `S` is the dynamic-programming (Riccati-factorization)
form of that certificate. That Riccati pivots are positive iff the reduced
Hessian is positive definite is standard in structured QP and MPC practice
(Rao–Wright–Rawlings 1998; HPIPM, arXiv:2003.02547 [vr]). The theorem is
therefore a reading of a known fact, not a new result.

- *Check.* In the double well of Example 3.6 at `N = 50`, the critical `a`
  at which the unperturbed Riccati recursion first fails and the critical
  `a` at which the reduced-Hessian lower bound loses definiteness are both
  `2.5172880840743` (`revision_checks.py`, Part C; the review found
  agreement to `1e-10` for `N = 50 … 5000`, with values 2.51729, 2.47977,
  2.46987, 2.46789, tending to `pi^2/4 = 2.46740`).
- *Scope.* For affine dynamics this strictly extends Theorem 3.2(1): the
  stage Lagrangians may be nonconvex while the condensed problem is
  convex. For nonlinear `f_t`, an interval enclosure of `grad^2 rho_t` over
  the stage box that is positive semidefinite is a valid sufficient check
  (`O(1)` per stage). For Euler transcriptions of `xdot = A x + B u` the
  discrete Riccati recursion converges to the continuous one, so the
  condition becomes the continuous Jacobi condition for the comparison
  problem in the limit. At finite `N` the discrete threshold lies above the
  continuous one.

**Example 3.6 (affine versus quadratic; floating-point illustration).**
`min h sum_{t<N} (u_t^2 + w(x_t))`, `w(x) = -a x^2 + b x^4`,
`x_{t+1} = x_t + h u_t`, `x_0 = 0.3`, `x_N` free, all variables free,
`T = 1`, `b = 1`. Neither classical condition applies: `H = u^2 + w(x) + p u`
is not convex in `x`, and neither is `H^0 = w(x) - p^2/4`.

- *Best affine bound, exactly (for `|xi| <= sqrt(a/(2b))`, true for
  `xi = 0.3`).* The dual function at `p = 0` equals
  `h w(xi) - (1-h) a^2/(4b)`. No affine family does better. By weak duality
  against the per-stage convexified problem, every dual value is at most
  that problem's value. That value is attained by the constant path
  `x = xi`, because `vex w` is flat on `|x| <= sqrt(a/(2b))`. So the best
  affine gap tends to `a^2/(4b) + J*`, about 0.67 for `a = 2`.
- *Quadratic calibration.* `w'' >= -2a` gives `M_t = diag(-2ah, 2h)`. The
  comparison Riccati recursion is well defined iff `P_{t+1} > -2/h`. Its
  continuous limit `-Pdot = -2a - P^2/2`, `P(T) = 0`, has
  `P = -2 sqrt(a) tan(sqrt(a)(T - t))`, which blows up (a conjugate point)
  iff `a T^2 >= pi^2/4 = 2.467`.

Results (`doublewell_calibration.py`; `eps = 1e-3` perturbation of the
Riccati data; stage residuals re-minimized numerically from random
starts):

| `a` | `N` | `J` at the KKT point | costate-affine gap | best affine gap | quadratic gap |
|---|---|---|---|---|---|
| 2.0 | 50 | −0.3247046625 | 2.81 | 0.659 | 2e-16 |
| 2.0 | 200 | −0.3286393888 | 2.85 | 0.667 | 1e-15 |
| 2.0 | 1000 | −0.3296960631 | 2.86 | 0.669 | 3e-15 |
| 2.0 | 5000 | −0.3299077691 | 2.86 | 0.670 (closed form) | 2e-15 |
| 2.4 | 50 | −0.4645445383 | 3.99 | 0.951 | 1e-15 |
| 2.4 | 5000 | −0.4732113687 | 4.05 | 0.966 (closed form) | 5e-15 |
| 3.0 | 50–5000 | −0.7474 … −0.7632 | 6.04–6.12 | 1.46–1.49 | Riccati fails at `t/N = 0.080 … 0.093` |

- The smallest eigenvalue of the stage Hessian lower bounds divided by `h`
  is `1.000e-3 = eps` at every `N`, as the proof predicts.
- For `a = 3` the recursion fails at `t/N -> 0.093`, the continuous
  conjugate time `T - pi/(2 sqrt 3) = 0.0931`.
- L-BFGS on the dual function agrees with the closed form to 1.4e-5
  (`a = 2`) and 1e-8 (`a = 2.4`) at `N = 50` and stalls at larger `N`,
  because the dual function is nonsmooth. The table uses the closed form.

- The review reproduced every number bit for bit and with independent
  code. The rerun took 5 min 34 s single-threaded.

**Interpretation (revised).**

- By the paragraph after Theorem 3.5, for every `(a, N)` in the table
  where the Riccati recursion succeeds, the transcription is **convex after
  condensing**. Its KKT point is unique and global, and no calibration is
  needed to see this.
- The discrete threshold lies above `pi^2/4` at finite `N` (2.517 at
  `N = 50`), so "exact up to the conjugate point" holds only in the limit.
- What the example shows is that the *per-stage* affine class cannot see
  hidden convexity: its gap stays 2.81–2.86 (costate slopes, `a = 2`) and
  0.66–0.67 (best affine) at every `N`, while the quadratic class is exact.
- It does not show the certification of a genuinely nonconvex problem.
  That is done by the transfer example of Section 5 (Theorem 5.2 and
  Check 5.3).
- For `a = 3` the condensed problem is nonconvex along the comparison
  bound, and the quadratic class with the global curvature bound gives
  nothing. Whether the KKT point is still globally optimal is not decided
  here.

### 3.3 Complexity

**Proposition 3.7 (cost of checking a calibration).** Let `S` use classes
`Phi_t` on the stages outside disjoint windows `W_1, ..., W_r`, handled
exactly (Proposition 4.4). Checking `B(S)` costs `N` global minimizations of
`rho_t` over `Omega_t` (dimension `n + m`, or `n + m` plus the stage
variables of the scheme), plus one global problem per window, plus writing
`S` (`O(N dim Phi_t)` numbers, `O(N n^3)` for Riccati). With stage cost
`c_stage` and window costs `C_j` the total is `N c_stage + sum_j C_j`.

This is bookkeeping. The content lies in the existence statements:

- Theorem 3.3 gives `r = 0` for all `N >= N_0`, with `c_stage` = one
  `(n+m)`-dimensional convex program (or a closed form) in case (1) and a
  small nonconvex global minimization in the SGM case (2);
- Theorem 3.5 does the same with one Riccati sweep;
- Theorem 5.2 does the same with nonconvex but low-dimensional stage
  problems, each certifiable by interval branch-and-bound on shells with
  `O(log(1/h))` boxes (sketch), so `O(N log N)` in total.

**Corollary 3.8 (a separation on the repository's path family).** Let
`F_n(x) = sum_{i=1}^n (x_i^2 - kappa x_i^4) + b sum_{i<n} x_i x_{i+1}` on
`[-1,1]^n` with `kappa + |b| <= 1`, read as a transcription with state
`x_t` and control `u_t = x_{t+1}`.

1. The calibration whose separator functions are half the unary terms
   (the balanced split) is exact: each bag function is `>= 0 = F_n(0)`
   ([R, Proposition 2.1]). The certificate is `n - 1` two-variable bag
   minimizations.
2. For `b = 0.8`, `kappa <= 0.2`, `eps <= 1e-4`, every single-tree
   certificate that relaxes each bilinear term alone by McCormick needs at
   least `0.57 (5/3)^n` members (leaves plus tightening pieces), for any
   branching rule, any node-wise split of class (a), and bound tightening
   by the same relaxation ([F, Theorem 1]; split-robustness from [R,
   Summary item 2]).

*Proof.* Both items are the cited results, restated. □

**Caveats.**

- The separation is between exact per-bag minimization and termwise
  relaxation. [F, Theorem 1] also holds for the convex member `kappa = 0`,
  which a convexity-aware single-tree solver closes at the root, and
  SCIP's default PSD-minor cuts escape it.
- [D, Theorem 3.4] gives polynomial decomposition-certificate sizes on
  paths in general; calibrations are the special case with structured
  split classes and no separator cells.
- **Transcriptions of ODEs are not covered.** There the per-stage coupling
  is near the identity and the per-stage nonconvexity is `O(h)`. A naive
  volume argument gives nothing, because the near-optimal set is thin in
  the high-frequency directions (eigenvalues up to `4/h` of the discrete
  Laplacian). Whether termwise single-tree branch-and-bound needs
  `exp(Omega(N))` nodes on, say, dtoc5-type transcriptions is open. The
  MINLPLib gaps are empirical and were traced in [O] to unbounded
  variables and weak relaxations, not to proven branching growth.
- Houska–Chachuat's mesh-independent bounds show that exponential
  dependence on `N` is not inherent to branch-and-bound on control
  parametrizations. Their bounds are quasi-polynomial at best in `1/eps`;
  calibrations are exact, and their cost is linear in `N` and independent
  of `eps` beyond the stage checks.

## 4. What fails at singular arcs, switches and state constraints; exact windows

Throughout this section the data are control-affine on stage `t`:
`L_t = L^0_t(x) + L^1_t(x)^T u`, `f_t = f^0_t(x) + F_t(x) u`, so for affine
`S` the residual is affine in `u`:
`rho_t(x,u) = alpha_t(x) + sigma_t(x)^T u` with switching function
`sigma_t(x) = L^1_t(x) + F_t(x)^T p_{t+1}` (for Euler,
`sigma_t = h (l^1(x) + G(x)^T p_{t+1})`).

**Proposition 4.1 (singular stages obstruct affine calibrations).** Let
`Omega_t = D x U` with `U` full-dimensional, `ubar_t in int U`,
`xbar_t in int D`, and `C^1` data. If the affine family with slopes `p` is
exact on the trajectory, then `sigma_t(xbar_t) = 0` and
`grad_x sigma_t(xbar_t) = 0`.

*Proof.* `rho_t(xbar_t, .)` is affine on `U` and minimal at an interior
point, so `sigma_t(xbar_t) = 0`. Hence `rho_t(xbar_t, u) = min rho_t` for
every `u in U`, so `xbar_t` minimizes `rho_t(., u)` over `D` for every `u`,
and `grad_x rho_t(xbar_t, u) = 0`. Subtracting two such identities gives
`(grad_x sigma_t(xbar_t))^T (u - ubar_t) = 0` for all `u` in a ball, so the
Jacobian vanishes. □

*Consequence.* With `x_N` free the slopes are unique (Theorem 3.1(3)). If
`f*` is attained at `xbar` and `grad_x sigma_t(xbar_t) != 0` at one singular
stage, **no exact affine calibration exists**. The stronger statement that
the affine class has a positive gap (`sup_p B(p) < f*`) also needs the dual
supremum to be attained. That is not proved here: [K, Proposition 1.2]'s
attainment argument uses sums of directions that vanish identically, and
this fails with dynamics rows. Along a continuous singular arc `sigma = 0` and
`d sigma/dt = 0`, but the state gradient of `sigma` generically does not
vanish when the control enters the dynamics through a state-dependent
matrix `G(x)` or the cost has an `x u` term. That is the catmix situation
(bilinear dynamics); the prediction that a costate Lagrangian loses there
([W2, Section 4]) is now a theorem about exactness. The size of the gap is
not quantified. Counterexample to overreach: for
`min int x^2`, `xdot = u`, `|u| <= 1`, `sigma = p` does not depend on `x`,
and the affine class is exact (Mangasarian holds).

**Proposition 4.2 (switches with state-dependent switching functions).**
Let `m = 1`, `U = [u_lo, u_hi]`, `Delta = u_hi - u_lo`, `ubar_t = u_lo`, and
`xbar_t in int D` with `B(xbar_t, r) ⊂ D`. Suppose on this ball
`rho_t(x, u_lo) <= rho_t(xbar_t, u_lo) + (Lambda/2)|x - xbar_t|^2` and
`grad sigma_t` is `M_s`-Lipschitz. If the affine family is exact at stage
`t` and `s* = Delta |grad sigma_t(xbar_t)| / (Lambda + Delta M_s) <= r`, then

```
sigma_t(xbar_t) >= Delta |grad sigma_t(xbar_t)|^2 / (2 (Lambda + Delta M_s)).
```

*Proof.* Exactness gives, for `|d| <= r`,
`0 <= rho_t(xbar + d, u_hi) - rho_t(xbar, u_lo) <= (Lambda/2)|d|^2 + Delta [sigma_t(xbar) + grad sigma_t(xbar)^T d + (M_s/2)|d|^2]`.
Take `d = -s grad sigma / |grad sigma|` and minimize over `s`. □

*Mesh dependence.* For Euler, `rho_t = h rhotilde`, so `sigma`, `Lambda`,
`M_s` all carry a factor `h`, and so do `s*` and the threshold. The
condition reads
`sigmatilde(xbar_t) >= Delta |grad sigmatilde|^2 / (2(Lambdatilde + Delta Mtilde))`,
**independent of `h`**.

**Corollary 4.3 (switch windows have fixed duration; conditional).**
Assume, in addition to the hypotheses of Proposition 4.2 at the stages
concerned, with `Lambdatilde`, `Mtilde` and the ball radius `r >= s*`
holding uniformly over these stages and in `h`:

- (i) `|grad_x sigmatilde| >= g_0 > 0` near the switch;
- (ii) discrete states and costates converge uniformly near the switch, so
  that the discrete switching function along the discrete trajectory is
  `gamma |t - t_s| + o(1)`. For bang-bang problems this is
  Alt–Baier–Gerdts–Lempio or Veliov-type theory, not (A3);
- (iii) the discrete states are interior;
- (iv) the slopes are unique (Theorem 3.1(3)), so that the statement covers
  all affine calibrations, not only the costate one.

Then for small `h` every stage with
`|t - t_s| < Delta g_0^2 / (2 gamma (Lambdatilde + Delta Mtilde))` (minus
`o(1)`) violates exactness: a window of fixed *duration*, hence
`Theta(1/h)` stages.

*Proof.* Insert (ii) into the `h`-independent condition, and use (i) for
the right-hand side. □

optcdeg2's failing head window (3092 stages, ending at the switch) is
consistent with this, though its main cause there is the concavity in `v`
(Section 2.4). The loss comes from freezing the multiplier: the costate
calibration uses `p_{t+1}` at every state, whereas a field calibration uses
the state-dependent multiplier `S_x(t,x)`, and its residual is nonnegative
for both control values by construction (Sketch 5.4).

**State constraints.**

- *Convex pure state constraints* are harmless for Theorem 3.2: they enter
  as normal-cone terms of the discrete adjoint. For Theorem 3.3 this is
  **unproved**. Discrete multipliers `nu_t = O(1)` at junctions make
  `q_t = O(1/h)`. The extra term `nu_t^T x` is minimized at `x^h_t` over
  convex `D`, which helps. But a Leitmann–Stalford-type condition with
  measure multipliers, and the corresponding convergence theory (only
  `O(h^{2/3})` in `L^inf`, Dontchev–Hager 2001), would be needed.
- *Nonconvex state constraints* (obstacles) make `Omega_t` nonconvex.
  Mangasarian fails, but the stage problem stays low-dimensional, so exact
  per-stage minimization is still `O(1)`. Exactness needs the residual to
  be minimal at the trajectory over the nonconvex set.
- *Boundary pinch points.* When the optimal state lies on the boundary of
  the state domain, the band can have a kink in the normal direction ([K,
  Lemma 4.2, consequences]). In dimension `>= 2` a boundary pinch set can
  defeat affine splits at first order ([K, Proposition 5.4], the example
  with `L = max(0, x + y - 1)` and `U = min(x, y)`). Affine calibrations
  can therefore fail on boundary arcs of 2-D state constraints even with
  smooth data.

**Proposition 4.4 (exact windows).** For a window
`I = {a, ..., b-1}` let

```
beta_I = inf { sum_{t in I} L_t(x_t,u_t) + S_b(x_b) - S_a(x_a) : (x_t,u_t) in Omega_t, x_{t+1} = f_t(x_t,u_t), a <= t < b }.
```

Replacing `sum_{t in I} inf rho_t` by `beta_I` in `B(S)` gives a valid
bound that is at least as large. It equals the bound of the family in
which `S_t` for `a < t < b` is the window's value function with terminal
cost `S_b` (the DP split on the window). It is exact on the trajectory iff
the trajectory attains `beta_I` and the remaining infima.

*Proof.* The window's residuals telescope to the window objective, whose
infimum is at least the sum of the stage infima. The DP split attains the
window infimum by Lemma 2.2(1). □

A window is a merged bag ("full class" on its interior separators). With
states eliminated, its dimension is `n + m |I|` (entry state plus window
controls). Generic branch-and-bound on it is exponential in `|I|`. The
closed instances escaped this in three ways:

- monotonicity (optcdeg2 head, 3080 stages, no branching);
- no controls, so the window has dimension `n = 2` (lukvle10);
- a 2-D end window with per-box field parameters (chain).

Under the assumptions (i)–(iv) of Corollary 4.3, affine calibrations need
windows of fixed duration, that is `Theta(1/h)` stages, at switches with
state-dependent switching functions. At singular arcs, Proposition 4.1
gives the same count only if the discrete states and controls are
interior and
`grad_x sigma_t(xbar_t) != 0` at `Theta(1/h)` stages along the arc, and
the slopes are unique as in (iv). This needs convergence assumptions for
singular arcs that are not stated or proved here. **Where these
assumptions hold, window cost that does not grow with the number of
stages in the window is the central difficulty.**

**Sketch 4.5 (quadratic calibrations on singular arcs).** With quadratic
`S`, the residual is quadratic in `u` with Hessian `B_t^T P_{t+1} B_t`,
where `B_t = h G`. The Riccati pivot is then `h^2 G^T P G` and the
numerator `E_t + A^T P B = h (grad_x sigmatilde + P G) + O(h^2)`, so each
Riccati step changes `P` by `O(1)` unless `P G = -grad_x sigmatilde` to
leading order. Bounded quadratic calibrations along a singular arc
therefore require `P` to be pinned in the direction `G`, plus a sign
condition at the next order: the discrete trace of the Goh transformation
and of Kelley's generalized Legendre–Clebsch condition. Not worked out.

## 5. Transfer from continuous calibrations

**Proposition 5.1 (sampling: an `O(h)` upper bound on the loss).** Let
`S in C^{1,1}([0,T] x R^n)` with `Lip(grad_{(t,x)} S) <= M` satisfy the
Hamilton–Jacobi inequality `l(x,u) + S_t + S_x g(x,u) >= 0` on
`[0,T] x D x U` and `S(T,.) <= Phi`, and let `|g| <= G` on `D x U`. For the
Euler transcription with `Omega_t = D x U`, the family `S_t = S(t_t, .)` has
`rho_t >= -(M/2) h^2 (1 + G^2)`, so
`B(S) >= S(0, xi) - (M T/2)(1 + G^2) h`.

*Proof.* `S(t+h, x+hg) - S(t,x) >= h (S_t + S_x g) - (M/2) h^2 (1 + |g|^2)`
by the lower Taylor bound for functions with Lipschitz gradient. □

This is the calibration form of the `O(h)` consistency of semi-Lagrangian
HJB schemes. It is an upper bound on the loss. **In the strict setting of
Theorem 5.2 the uncorrected family loses only `O(h^2)` when `e_h = O(h)`**
(Remark 5.2(f)). The `O(h)` rate is attained for non-strict `S`: for the
LQ field of Remark 5.2(d) (`xdot = -2x + u`, `l = u^2/2`,
`Phi = x^2/2`, `x_0 = 1`, `U = [-5, 5]`), the uncorrected family
`S_t = V(t_t, .)` has gap/`h` = 2.25, 2.41, 2.49, 2.52, 2.54, 2.55, 2.55
for `N = 10 … 640` (`recheck_revision_checks.py`, Part C; the recheck's
`r2` part C gives the same values). Remark 5.2(d) itself measures the
*corrected* (transferred) family.

**Theorem 5.2 (transfer with an affine correction; Euler).** Assume:

- (T1) *Compactness.* `D` and `U` are compact and convex, and `D` contains
  every state of every feasible point of the transcriptions. `S in C^4` on
  `[0,T] x D'` for a neighbourhood `D'` of `D` containing `D + h_0 G B_1`.
  `g in C^2` near `D x U` and `Phi in C^2` near `D`. The running cost may
  depend on time, `l = l(t,x,u)`: it is continuous in `t` and `C^2` in
  `(x,u)` near `D x U`, with `(x,u)`-derivatives up to order 2 continuous
  in `(t,x,u)`. The Euler transcription uses `L_t = h l(t_t, x, u)`.
  (Check 5.3 uses a time-dependent `l`.)
- (T2) *Exact strict calibration.* `(x*, u*)` is admissible and
  continuous (`xdot* = g(x*, u*)`, `x*(0) = xi`), with `x*(t) in int D` and
  `u*(t) in int U`. With `r(t,x,u) = l(t,x,u) + S_t(t,x) + S_x(t,x) g(x,u)`:
  - `r(t, x*(t), u*(t)) = 0` for all `t`;
  - `r >= c (|x - x*(t)|^2 + |u - u*(t)|^2)` on `[0,T] x D x U`;
  - `Phi(x) - S(T,x) >= Phi(x*(T)) - S(T,x*(T)) + c |x - x*(T)|^2` on `D`.
- (T3) *Uniform convergence.* Euler KKT points `(x^h, u^h, p^h)` exist with
  `e_h = max_t (|x^h_t - x*(t_t)| + |u^h_t - u*(t_t)| + |p^h_t - psi(t_t)|) -> 0`,
  where `psi(t) = S_x(t, x*(t))`. No rate is needed.

Then there is `h_0 > 0` such that for all `h <= h_0` the family

```
S^h_t(x) = S(t_t, x) + a_t^T x,     a_t = p^h_t - S_x(t_t, x^h_t),
```

is an exact calibration of the transcription, and `(x^h, u^h)` is its
unique global minimizer.

*Proof.* Write `eta_h = e_h + h`.

1. *`psi` is the costate.* By (T2), `r(t, ., .) >= 0` vanishes at the
   interior point `(x*(t), u*(t))`. So `grad_{(x,u)} r = 0` there and
   `grad^2_{(x,u)} r >= 2c I`. Using `xdot* = g(x*, u*)`, `grad_x r = 0`
   reads `d/dt S_x(t, x*(t)) = -l_x - g_x^T S_x`: the adjoint equation. The
   terminal condition gives `S_x(T, x*(T)) = grad Phi(x*(T))`.
2. *Size of the correction.* By (T3), `a_t = O(e_h)`. Use the discrete
   adjoint `p_t - p_{t+1} = h (l_x + g_x^T p_{t+1})`, the Taylor expansion of
   `S_x` along `x^h_{t+1} = x^h_t + h g^h_t`, and the identity
   `S_xt + S_xx g = grad_x r - l_x - g_x^T S_x`. They give
   `a_{t+1} - a_t = -h g_x^T (p_{t+1} - S_x(t_t,x^h_t)) - h grad_x r(t_t,x^h_t,u^h_t) + O(h^2) = O(h eta_h)`,
   because both brackets are `O(eta_h)`.
3. *Residual.* With
   `R_2(x,u) = int_0^1 (1-s) D^2 S(t_t + s h, x + s h g)[(1,g),(1,g)] ds`
   (`C^2` in `(x,u)` because `S in C^4` and `g in C^2`),
   `rho_t(x,u) = h r(t_t,x,u) + h^2 R_2(x,u) + (a_{t+1} - a_t)^T (x - x^h_t) + h a_{t+1}^T (g(x,u) - g(x^h_t,u^h_t)) + const`.
4. *Far region.* Let `z = (x,u)`, `z^h = (x^h_t,u^h_t)`,
   `delta = |z - z^h|`. From (T2), step 2 and `r(z^h) = O(e_h^2)`,
   `rho_t(z) - rho_t(z^h) >= h [c (delta - e_h)_+^2 - C eta_h delta - C e_h^2]`.
   This is positive for `delta >= M_0 eta_h` with `M_0` large, uniformly in
   `t`.
5. *Near region.* For small `h`, `x^h_t` and `u^h_t` are interior, because
   `e_h -> 0` and the continuous `x*`, `u*` stay at a positive distance
   from the boundaries of `D` and `U` on `[0,T]`. For `delta < M_0 eta_h`:
   the gradient of `rho_t` at `z^h` vanishes by the discrete KKT conditions
   (for `x` because `grad S^h_t(x^h_t) = p^h_t`). On this ball, which
   shrinks to `z*(t)`,
   `rho_t(z) - rho_t(z^h) - grad rho_t(z^h)^T (z - z^h) >= h (c - o(1)) |z - z^h|^2`,
   from the second-order remainders of `h r`, `h^2 R_2` and the `a` terms.
   So `z^h` is the minimum on the ball.
6. *Terminal and initial stages* are handled the same way: the terminal
   residual has growth `c |x - x*(T)|^2` minus an `O(e_h)`-sloped term, and
   stage 0 has only `u`. Theorem 3.1(2) applies to the family `S^h`. Strict
   positivity away from `z^h` gives uniqueness. □

The review checked every step. The first revision replaced the `O(h)` rate
of the first version by uniform convergence and added the admissibility
and `r = 0` hypotheses that step 1 needs; the recheck rechecked every step.
With a time-dependent `l` the proof is unchanged. Step 1 holds pointwise
in `t`. In steps 2–6, `l` enters only at the grid times `t_t`. In step 2
the `l_x` terms of the discrete adjoint and of the identity for
`S_xt + S_xx g` are evaluated at the same point `(t_t, x^h_t, u^h_t)` and
cancel. Otherwise the proof uses only uniform bounds and the uniform
continuity of the `(x,u)`-Hessian of `l` on the compact set
`[0,T] x D x U`, which the joint continuity in (T1) provides.

**Remarks 5.2.**

- (a) *No convexity of the stages is used.* Global optimality of fine
  transcriptions follows from an exact strict *continuous* calibration plus
  uniform convergence of the discrete KKT points. The certificate is the
  continuous `S` corrected by an `O(e_h)` affine term per stage built from
  the discrete costates.
- (b) *(T2) implies the coercivity behind (T3).* Along linearized pairs
  `zeta = (xi, eta)` with `xi(0) = 0`, `xidot = g_x xi + g_u eta`, put
  `P(t) = S_xx(t, x*(t))`. Then `r_uu = H_uu`, `r_xu = H_xu + P g_u` and
  `r_xx = H_xx + P g_x + g_x^T P + Pdot`, with `H` at `psi`. Hence
  `zeta^T grad^2 r zeta = zeta^T grad^2 H zeta + d/dt (xi^T P xi)`. So the
  second variation
  `Q_H(xi, eta) = int zeta^T grad^2 H(t, z*, psi) zeta dt + xi(T)^T grad^2 Phi xi(T)`
  satisfies

  ```
  Q_H(xi, eta) = int zeta^T grad^2 r(t, z*) zeta dt + xi(T)^T grad^2 (Phi - S(T,.)) xi(T)
              >= 2c (||xi||^2_{L2} + ||eta||^2_{L2}) >= 2c ||eta||^2_{L2}.
  ```

  This identity was observed by the review. It is a pointwise algebraic
  identity for any number of states and controls (no optimality is used);
  the recheck verified it symbolically for `n = 2`, `m = 1`, and
  `recheck_revision_checks.py` (Part A4) for `n = 2`, `m = 2` with a
  time-dependent `l`. The inequality uses `grad^2 r(t, z*) >= 2c I` from
  step 1. This is the coercivity used by Dontchev–Hager (SICON 1993), which
  then supplies (T3) for Euler with interior controls (their remaining
  smoothness hypotheses were not checked in detail). Hager (2000,
  Theorem 2.1) does not cover Euler; see Section 3.1.
- (c) *Compactness of `U` is essential (review F11, rechecked).*
  - Take `min int_0^T (u^2/2 + x^6 + x^2) dt + Phi(x(T))`,
    `Phi(x) = x^2/2 - x^4/4`, `xdot = u`, `x(0) = 0`, `u in R`.
  - `S = -x^4/4` is a `C^inf` exact strict calibration on all of `R x R`:
    `r = (u - x^3)^2/2 + x^6/2 + x^2`, and the exact identity
    `r - (x^2 + u^2)/4 = (u/2 - x^3)^2 + 3x^2/4 >= 0` gives growth with
    `c = 1/4`. Also `Phi - S(T,.) = x^2/2`. The optimum is `0`, and
    `(x,u,p) = 0` is an exact discrete KKT point with `a_t = 0`.
  - Yet **for every `h` the Euler transcription is unbounded below**:
    staying at 0 and jumping to `X` in the last step costs
    `X^2/(2h) + X^2/2 - X^4/4` (the running `x^6` term is evaluated at the
    left endpoint). At `X = 1000` this is about `-2.5e11` for
    `h = 0.1, 0.01, 0.001`.
  - So on unbounded control sets a strict continuous calibration says
    nothing about the transcription; (T1) excludes this.
  - With `U = [-K, K]` (and `D = [-KT, KT]`) Theorem 5.2 applies, and the
    example shows how `h_0` depends on the size of `U` (observed by the
    recheck). The last-stage residual at `x = 0` is
    `h u^2/2 - h^4 u^4/4`, which is nonnegative on `U` iff `h^3 K^2 <= 2`.
    So `h_0 <= (2/K^2)^{1/3}`, which tends to 0 as `K` grows.
  - Example 3.6 (free `u`) is outside Theorem 5.2 as stated. It works
    because its comparison calibration is quadratic and `g` is affine.
  - An unbounded version needs a growth condition, for example
    `sup |D^2 S| (1 + |g|)^2 = o(r/h)` (the review's suggestion; not
    checked).
- (d) *Strictness in `x` is essential (review checks c3, c4; expansion
  rechecked).* A field of extremals has `r = 0` along every field
  trajectory, so it is not strict in `x`.
  - For scalar LQ, `xdot = alpha x + u`, `l = (u^2 + q x^2)/2`,
    `V = P x^2/2` with `Pdot = P^2 - 2 alpha P - q`: the transferred
    residual, minimized over `u`, has curvature `(F(P(t+h)) - P(t))/2` in
    `x`, where `F(P) = h q + (1 + alpha h)^2 P / (1 + hP)` is the discrete
    Riccati map.
  - A Taylor expansion gives
    `F(P(t+h)) - P(t) = h^2 (P - alpha)(alpha P + q) + O(h^3)`
    (recheck `r1`; `recheck_revision_checks.py`, Part A1). For `q = 0`
    this is `h^2 alpha P (P - alpha)`: negative for `alpha < 0 < P` and for
    `0 < P < alpha`. For `alpha = q = 0` and `Phi = phi_T x^2/2`,
    `phi_T > 0`, the defect is exactly zero (`P = 1/(1/phi_T + T - t)`).
  - Where the coefficient is negative, a bounded `D` of fixed width costs
    `Theta(h^2)` per stage and `Theta(h)` in total. The review measured
    field gaps 0.191, 0.102, 0.053, 0.027, 0.013, 0.0067 for
    `N = 10 … 320` (`alpha = -2`, `q = 0`, `Phi = x^2/2`; reproduced to
    `2e-13` by Part C). If instead `F(P(t+h)) >= P(t)` at every stage, the
    stage residuals are convex and stationary at the interior trajectory,
    so the transferred field family is exact. The measured exact case
    (review checks c3, c4) is `alpha = 0`, `q = 1`, `Phi = 0`
    (`l = (u^2 + x^2)/2`), whose coefficient is `+P >= 0`; it lies outside
    the `q = 0` family.
- (e) *Tilting fixes non-strictness, at a price in `h_0`.* Tilt a field
  value function `V` to `S = V - e(t) |x - x*(t)|^2`, with
  `e(t) = eps e^{-lambda t}` and `d = x - x*(t)`. The added residual is
  `e(t)[lambda |d|^2 - 2 d^T (g - g*)]`, where `g* = g(x*(t), u*(t))`.
  - *General claim (sketch; verified only for scalar LQ).* Suppose the
    field control `u_f(t,x)` is Lipschitz with constant `L_f`,
    `V(T,.) = Phi`, and the strengthened Weierstrass condition
    `r_V >= c_W |u - u_f(t,x)|^2` holds on `D x U`, with
    `u*(t) = u_f(t, x*(t))`. Put `v = u - u_f(t,x)` and bound
    `d^T (g - g*) <= L_1 |d|^2 + L_2 |d| |v|`, where `L_1` is a one-sided
    Lipschitz constant of the closed-loop field `x -> g(x, u_f(t,x))` and
    `L_2` a Lipschitz constant of `g` in `u`. Young's inequality gives
    `r_S >= (c_W/2) |v|^2 + e(t) (lambda - 2 L_1 - 2 e(t) L_2^2 / c_W) |d|^2`.
    Since `|u - u*(t)| <= |v| + L_f |d|`, this is strict in `(x,u)` once
    `lambda > 2 L_1 + 2 eps L_2^2 / c_W`, with a constant proportional to
    `min(c_W, e(T))` for fixed `lambda` and `L_f`. The terminal residual is
    `e(T) |d|^2`. (For scalar LQ, `L_1 = alpha - P`, `L_2 = 1`,
    `c_W = 1/2`, so this sketch gives a slightly conservative version of
    the exact threshold below.)
  - For scalar LQ, `xdot = alpha x + u`, the exact threshold is
    `lambda > 2 alpha - 2P + 2 e(t)` for all `t` (review; the recheck
    confirmed the determinant). The terminal strictness constant is
    exactly `e(T) = eps e^{-lambda T}`.
  - *`h_0` versus the strictness constant `c`, in general.* The proof's
    constants give only `h_0` of order `c^2` (recheck R2): the far region
    needs `delta >= M_0 eta_h` with `M_0 ~ C/c`, the near region needs
    `grad^2 r >= c` on a ball of radius about `(C/c) eta_h`, and with a
    Lipschitz `grad^2 r` (for example `l, g in C^3`) this forces
    `eta_h <~ c^2`. Whether `h_0` is linear in `c` beyond quadratic
    residuals is open.
  - *Scalar LQ: `h_0` is linear in `c = e(T)` (formal leading-order
    derivation, and measured).* The stage residuals are exactly quadratic, so the
    transferred family is exact iff `F(s_{t+1}) >= s_t` at every stage
    `t >= 1`, where `s = P - 2e` is the tilted curvature (this is the 2 x 2
    Schur-complement test; it assumes an interior discrete trajectory and
    `1 + h s > 0`, both true here). Expanding (Part A2),
    `F(s(t+h)) - s(t) = 4 h e (lambda/2 - alpha + P - e) + h^2 K + O(h^2 e + h^3)`
    with `K = (P - alpha)(alpha P + q)` the field defect of (d). When
    `K(T) < 0` and the binding stage is near `t = T`, where `e` is
    smallest, the leading-order prediction is
    `h_0 ≈ 4 e(T) m(T) / |K(T)|`, `m = lambda/2 - alpha + P - e`: linear in
    `c`, with a prefactor that grows linearly in `lambda`. Measured
    `h_0 / (eps e^{-lambda T})` (Part B: `h_0 = T/N` at the largest inexact
    `N`, located by bisection; exact at every larger grid `N` up to
    `4e5`):

    | problem | `lambda` | `eps = 0.5` | `0.1` | `0.02` | prediction (`eps -> 0`) |
    |---|---|---|---|---|---|
    | `alpha = -2, q = 0, Phi = x^2/2` | 1 | exact for all `N >= 4` | 3.40 | 2.47 | 2.33 |
    | | 2 | exact for all `N >= 4` | 3.08 | 2.74 | 2.67 |
    | | 4 | 3.90 | 3.43 | 3.35 | 3.33 |
    | | 8 | 4.69 | 4.67 | 4.67 | 4.67 |
    | `alpha = 1, q = 1, Phi = 0` | 4 | 4.55 | 4.11 | 4.02 | 4.00 |
    | | 6 | 8.40 | 8.07 | 8.01 | 8.00 |
    | | 8 | 12.14 | 12.02 | 12.01 | 12.00 |

    The `eps -> 0` predictions are `(lambda + 6)/3` and `2 lambda - 4`.
    The measured values are 1.0002–1.47 times the prediction evaluated
    at the given `eps`, and the ratio tends to 1 as `eps e^{-lambda T}`
    decreases. So for scalar LQ, when `K(T) < 0` and the binding stage is
    near `T`, `h_0 ≈ C(lambda) eps e^{-lambda T}`. This
    is an observation for scalar LQ, not a general statement. The recheck's
    table (`r2` part B, 160-point geometric grid in `N`) gives the same
    picture with slightly larger ratios, 2.6–12.7, because its grid is
    coarser.
  - So `lambda` should be just above the threshold, not large.
  - Review check c4b: the tilted family is exact (gap `<= 7e-14` at
    `N = 40 … 2560`) with `lambda = 1` (`alpha = -2`) and `lambda = 4`
    (`alpha = 1`), while the untilted gap stays `Theta(h)`. With
    `lambda = 8` it is not yet exact at `N = 320` (gap 1.6e-3).
  - Explicit constants are therefore essential for practical use.
  - Comparison-LQ calibrations as in Example 3.6 are strict when the
    Riccati data are perturbed by `eps`.
- (f) *Uncorrected sampling loses `O(h^2)` in the strict case.* Along the
  discrete trajectory, telescoping gives
  `J^h - B(S^unc) = sum_t [rho^unc_t(z^h_t) - min rho^unc_t] + [same at N]`.
  - The uncorrected residual's gradient at `z^h_t` is minus the gradient of
    the `a` terms, which is `O(h eta_h)`, against curvature about `ch`. That
    costs `O(h eta_h^2)` per stage, and the far region is handled as in
    step 4.
  - The terminal gradient is `a_N = O(e_h)`, which costs `O(e_h^2)`.
  - So the loss is `O(eta_h^2)`, that is `O(h^2)` when `e_h = O(h)`.
- (g) *Scope.* The theorem covers `x_N` free and no state or terminal
  constraints (`D` is an enclosure), with interior optimal controls. With
  a floating-point KKT point, the certificate gives `f* >= J - tiny`, not
  exact equality. The Runge–Kutta version (transformed costates, Section
  3.1) is not written out and needs uniform convergence of the stage
  values.
- (h) *Rigorous checking (sketch).* Per stage the margin is at least
  `h c delta^2 / 2` at distance `delta >= M_0 eta_h`. Interval
  branch-and-bound on geometric shells around `z^h`, with boxes of width
  proportional to their distance, then needs `O(log(1/eta_h))` boxes per
  stage in fixed dimension `n + m` ([K, Corollary 5.5] and [D, Lemma 3.1]
  use the same shells). Total `O(N log N)` when `e_h = O(h)`.

**Check 5.3 (a genuinely nonconvex transcription).** The review
constructed, and `revision_checks.py` (Part B) re-implemented
independently, the following example.

- `S = sin(2x + t) + 0.3 x^3`, `x*(t) = 0.2 + 0.4 sin 2t`,
  `u* = 0.8 cos 2t` (admissible for `xdot = u`, `x(0) = 0.2`), `T = 1`,
  `U = [-2, 2]`, `D = [-1.8, 2.2]`.
- `r = (u - u*)^2 (1 + 0.5 sin 5x) + (x - x*)^2 (1.2 + sin 4(x - x*))`,
  which is nonconvex, `>= 0.2 |z - z*|^2`, and `0` on `(x*, u*)`.
- `l = r - S_t - S_x u` (time-dependent) and
  `Phi = S(T,.) + (x - x*(T))^2 (1 + 0.3 sin 7x)`.

Every stage residual was minimized globally on a 1601 × 801 grid over
`D x U`, followed by bounded local polish. Gaps `J^h - B`:

| `N` | 5 | 10 | 20 | 40 | 80 | 160 |
|---|---|---|---|---|---|---|
| transferred family (Theorem 5.2) | 0.084 (review) | 0.0021 | 6e-16 | 1e-15 | 3e-15 | 7e-15 (review) |
| uncorrected sampling | 0.098 (review) | 0.0237 | 0.0061 | 0.00157 | 0.00040 | 0.00010 (review) |
| costate-affine | 8.66 (review) | 8.77 | 8.71 | 8.66 | 8.63 | 8.62 (review) |

- My numbers (`N = 10 … 80`) agree with the review's to `2e-11` for the
  transferred and uncorrected rows, and to `1.5e-9` for the costate-affine
  row (differences 1.2e-11, 1.6e-10, 1.46e-9, 1.49e-9 for
  `N = 10, 20, 40, 80`; `recheck_revision_checks.py`, Part D). The
  recheck's third implementation agrees with mine to `4e-14`
  (transferred and uncorrected, except its transferred value at
  `N = 10`, which is `1.05e-6` lower because its local polish stopped
  short) and to `3.3e-10` (costate-affine).
- The discrete controls are interior, and the maximal state error is about
  `0.85 h`.
- The review measured `max|a_{t+1} - a_t|/h^2` = 5.29 at `N = 5` and
  5.54–5.65 for `N = 10 … 160`: bounded in `N`, as step 2 predicts.

So the transferred calibration certifies a nonconvex transcription exactly
for `h <= 0.05`, while costate calibrations lose about 8.6 at every `N`, and
uncorrected sampling loses `O(h^2)`. Here `h_0` lies in `(0.05, 0.1)`.

**Sketch 5.4 (bang-bang: field calibrations localize switch failures).**
Let the control enter affinely, with a box `U` and a bang-bang optimum with
finitely many regular switches. Let `S` be a strict field calibration in
`x` whose residual is `r = r_0(t,x) + sigma(t,x) u`, with `sigma` the field's
switching function (vanishing on the switching surface, not only on the
trajectory).

- Away from switches `|sigma(t, x^h_t)| >= gamma |t - t_s|`, and the stage
  minimization in `u` has a linear margin `h gamma |t - t_s| |Delta u|`
  against the `O(h eta_h)|Delta u|` remainders of the transfer proof.
- That margin wins unless `|t - t_s| <= C eta_h / gamma`: **a window of
  `O(1)` stages** when `e_h = O(h)`, not `Theta(1/h)` as for costate
  calibrations (Corollary 4.3).
- Each window is a global problem in `n + m W` variables with `W = O(1)`.
- Not proved: the discrete switching structure (one fractional control per
  switch), uniform estimates for the window problem, growth in `x` near
  the switching surface, and the compactness and strictness requirements of
  Remarks 5.2(c)–(e) in this setting.

## 6. Significance and novelty

**Classical in substance.**

- The notion of discrete calibration: Krotov functions (1967), Bellman
  inequalities and the LP approach to DP, cost-shifting splits of
  graphical models ([K, Section 8]).
- Theorems 3.1–3.2: the discrete maximum principle with convexity, strong
  Lagrange duality (Tamminen 2019), and economics textbook sufficiency.
- The pointwise condition behind Theorem 3.3: the pointwise (sufficient)
  form of the Leitmann–Stalford condition (1971).
- Theorem 3.4: the discrete Reid roundabout theorem (Bohner 1996;
  Hilscher–Zeidan 2002; Ahlbrandt–Peterson 1996).
- Theorem 3.5: convexity of the condensed problem, certified by a Riccati
  factorization of the reduced-Hessian lower bound (standard in structured
  QP and MPC). It is kept as a reading, not a result.
- The band picture: [K]'s results with the forward and backward value
  functions of DP.
- camshape's mechanism: discrete Sturm comparison and disconjugacy
  (Hartman 1978).

**Not found stated before; elementary; modest novelty.**

- Theorem 3.3: only the mesh-uniform perturbation statement (costate
  calibrations of Euler transcriptions are exact for all small `h` under the
  strict pointwise form of the Leitmann–Stalford condition, and the
  non-strict pointwise form is necessary in the limit).
- Propositions 4.1–4.2 and Corollary 4.3: exactness obstructions at
  singular and switching stages, and the fixed duration of the switch
  window.
- The instance dictionary and Proposition 2.3.

**Not found stated before; elementary; potential practical weight:
Theorem 5.2.**

- Known discretization theory proves that discrete KKT points are strict
  *local* minimizers near the continuous solution. Theorem 5.2 upgrades
  this to *global* optimality of the transcription, with an explicit
  certificate of linear size (checked in `O(N log N)`), when the continuous problem has an exact strict
  calibration on compact state and control sets, the optimal controls are
  interior, and the discrete KKT points converge uniformly (T3).
- The review's search found no such statement. Its search covered Krotov
  and the Irkutsk discrete theory, Hager and Dontchev–Hager,
  Malanowski–Büskens–Maurer-type discrete sufficient conditions (all
  local), and discrete Hamilton–Jacobi theory. The closest text,
  Abhijeet et al., *Convexity in optimal control problems*
  (arXiv:2404.08621, 2024), proves no transfer.
- The proof is short: a Taylor expansion plus stability of a strict
  minimum. It is the missing link that [T7] asks for between continuous
  global theory and rigorous certificates for large transcribed models,
  but only in the smooth, interior, compact case.
- Two caveats limit its practical weight. Strict smooth global
  calibrations are rare outside constructed or LQ-like cases, and `h_0`
  can be small (Remark 5.2(e)).

**Limits.**

- Everything here certifies the *transcribed* problem. [T7]'s
  compositional certificate also needs discretization error bounds, which
  are a separate matter.
- Theorem 5.2 needs an exact strict continuous calibration on compact sets.
  Such functions are known analytically for classical problems (tilted
  fields of extremals, perturbed LQ comparison) but must otherwise be
  computed. Moment–SOS gives only approximate subsolutions
  (`O(1/log log d)` in `L1`). An approximate `S` still yields a rigorous
  certificate, with a gap of about the defect times `T`, because validity
  comes from the discrete stage checks, not from `S`.
- Bang-bang, singular arcs and active state constraints are outside
  Theorem 5.2. These are exactly the features of the instances that
  needed windows (optcdeg2, catmix) or are still open (rocket).
- No lower bound in `N` for branch-and-bound on ODE transcriptions exists,
  so "exponential versus linear" is proved only on fixed-coupling families
  and only relative to termwise relaxations.

## 7. Recommended next question and attack plan

*Follow-up (root, 2026-09-30):* for the Euler transcription with one
regular switch, under the hypotheses of the bang-bang note's Theorem 4.1
plus an exact terminal term, this question is answered in
[`../theory-bangbang/window-exactness.md`](../theory-bangbang/window-exactness.md):
yes when the switch self-curvature `kappa_tau = b(x*(tau))^T w` is
nonnegative, no when it is negative (on grids whose KKT point has a
fractional stage, within transferred `C²` calibrations and, for LQ data,
within quadratic families with the discrete costate slopes; see that note's
Consequence paragraph). Runge–Kutta transcriptions and several switches
were not treated.

**Question (transfer at switches).** Consider a control-affine problem
with box controls whose solution is bang-bang with finitely many regular
switches (strict bang-bang second-order conditions in the sense of
Agrachev–Stefani–Zezza or Maurer–Osmolovskii), and which has an exact,
strict piecewise-`C^3` field calibration on a compact state enclosure
(strict in `x`, strict in `u` away from the switching surfaces). For its
Euler and Runge–Kutta (`b_i > 0`) transcriptions, are there `h_0` and `W`
independent of `h` such that for all `h <= h_0` an exact discrete
calibration exists that equals the transferred field calibration of
Theorem 5.2 outside windows of at most `W` stages around each switching
time, each window being a global problem in at most `n + m W` variables?

**Why this one.** A positive answer gives exact global certificates for
arbitrarily fine transcriptions of bang-bang problems at cost
`O(N log N) + (#switches) C(n + m W, eps)`. That capability does not exist
today:

- costate calibrations need `Theta(1/h)`-stage windows under the
  assumptions of Corollary 4.3;
- generic branch-and-bound has no proven mesh-independent exact
  guarantee;
- Theorem 5.2 handles the smooth part, and Check 5.3 shows it working on a
  nonconvex problem.

It also isolates the remaining difficulty (the discrete structure at
junctions) in a finite-dimensional local problem. optcdeg2's unresolved
tail (gap 6.1e-3) is a concrete test.

**Alternatives considered.**

- *Branch-and-bound lower bounds in `N` for ODE transcriptions.* An
  interesting negative result, but no capability, and the naive volume
  argument already fails (Corollary 3.8, caveats).
- *Sparse moment–SOS along the horizon.* Known rates are slow and the
  certificates numerical (STROM).
- *Singular arcs first.* Harder (Sketch 4.5). Best attempted after
  switches, with catmix as ground truth (its exact 1-D DP is available).

**Attack plan.**

1. *Finish the smooth case.*
   - Write Theorem 5.2 for Runge–Kutta with `b_i > 0` via Hager's
     transformed adjoint, including uniform convergence of the stage
     values.
   - Make the constants explicit, in particular how `h_0` depends on the
     strictness constant `c` (Remark 5.2(e): for tilted scalar LQ fields
     `h_0 ≈ C(lambda) eps e^{-lambda T}`, linear in `c`, was observed and
     obtained by a formal leading-order derivation; the general proof gives
     only order `c^2`).
   - State an unbounded-control version under a growth condition
     (Remark 5.2(c)).
   - Implement an a posteriori checker: given any candidate `S` (analytic
     or numerical) and a discrete KKT point, build `S^h` and certify the
     stage minima by interval branch-and-bound on shells.
   - Targeted test: the nonconvex example of Check 5.3, with interval
     arithmetic.
2. *Local analysis at a regular switch.* Use Alt–Baier–Gerdts–Lempio-type
   error bounds to fix the discrete switching structure (at most one
   fractional control per switch for small `h`). Derive the window size `W`
   from the margin comparison of Sketch 5.4, and prove that the window
   problem is well conditioned uniformly in `h`.
3. *Test problems.*
   - A bang-bang toy with an explicit field (for example a double
     integrator with a quadratic state cost and one switch).
   - optcdeg2: compute a strict field calibration on its 2-D state
     enclosure (HJB grid plus tilting). Rigor is not needed for `S`
     itself, since the discrete checks are rigorous. Apply the transferred
     calibration to the tail window that is still open.
4. *Band quantification.* Express windows as full-class separators and
   bound their number and length by band widths near junctions ([K,
   Theorem 3.1]). Check whether the `O(1)`-stage claim matches the
   measured band on optcdeg2.
5. *Then singular arcs:* catmix (verify the prediction of Proposition 4.1
   on its singular band numerically), then the Goddard-rocket instances.

## 8. Status of the statements

| item | content | status |
|---|---|---|
| Lemma 2.1 | validity of `B(S)` | proved |
| Lemma 2.2 | strong duality; max-closure | proved |
| Section 2.3 | exact calibrations lie in the band; gap identities | band membership proved; one-separator identity carries over with extended values (review F1); pinch regularity is a hypothesis; band membership not sufficient (counterexample) |
| Proposition 2.3 | concave chord calibrations | proved |
| Theorem 3.1 | affine class: Lagrangian dual, exactness, slopes | proved; converse of (2) needs attainment of `f*`; (3) is stated at a global minimizer (`p_0` free when `x_0` is fixed) |
| Theorem 3.2 | discrete Mangasarian and Arrow | proved (classical) |
| Theorem 3.3 | mesh-uniform exactness (Euler); necessity | proved given (A3); the condition is the pointwise (sufficient) form of the Leitmann–Stalford condition (the restatement read uses an integral hypothesis); RK and trapezoid a sketch |
| Theorem 3.4 | local quadratic calibrations ⇔ Riccati ⇔ SOSC | proved (classical) |
| Theorem 3.5 | global quadratic calibrations by LQ comparison | proved; equals convexity of the condensed problem (known in substance) |
| Example 3.6 | affine versus quadratic, double well | floating-point illustration, reproduced by the review; a hidden-convexity example |
| Proposition 3.7, Corollary 3.8 | cost; separation on the path family | bookkeeping; imported |
| Proposition 4.1 | singular obstruction | proved (no exact affine calibration); positive gap needs dual attainment |
| Proposition 4.2, Corollary 4.3 | switch obstruction; fixed-duration window | inequality proved; corollary conditional on stated assumptions (constants uniform over the stages); the `Theta(1/h)` count at singular arcs needs convergence assumptions not stated here |
| Proposition 4.4 | exact windows | proved |
| Sketches 4.5, 5.4 | quadratic on singular arcs; bang-bang windows | sketches |
| Proposition 5.1 | sampling: `O(h)` upper bound on the loss | proved; `O(h^2)` in the strict case when `e_h = O(h)` (Remark 5.2(f)); `Theta(h)` attained by a non-strict LQ field (floating point) |
| Theorem 5.2 | transfer with affine correction (Euler) | proved given (T3), after review fixes (admissibility, `r = 0`, compactness, uniform convergence); rechecked; time-dependent `l(t,x,u)` allowed |
| Remarks 5.2(c)–(e) | compactness and strictness are needed; tilting | (c) proved (exact identity); (d) defect `h^2 (P - alpha)(alpha P + q)` derived and checked symbolically; (e) scalar LQ threshold proved, `h_0` linear in `eps e^{-lambda T}` for scalar LQ by a formal leading-order derivation, and measured; general tilting claim a sketch; general `h_0` only of order `c^2` |
| Check 5.3 | nonconvex transfer example | floating point; the author's and the review's implementations agree to `2e-11` (transferred, uncorrected) and `1.5e-9` (costate-affine); the recheck's third implementation agrees except one `1e-6` local-polish shortfall at `N = 10` |

## 9. Commands run and files

Targeted checks only; no project-wide verification and no CI inspection.

- `python3 doublewell_calibration.py` in this directory (`OMP_NUM_THREADS=1`)
  → `logs/doublewell_calibration.json`, `logs/doublewell_calibration.log`.
  The review's rerun took 5 min 34 s single-threaded (the first version of
  this note said "about 1 minute", which was wrong).
- Revision: `OMP_NUM_THREADS=4 python3 revision_checks.py` →
  `logs/revision_checks.json`, `logs/revision_checks.log` (1 min 30 s).
  - Part A: the compactness counterexample.
  - Part B: an independent re-implementation of the nonconvex transfer
    example.
  - Part C: the critical `a` of the Riccati recursion versus the
    reduced-Hessian lower bound.
- Revision: the band counterexample (review c5) was re-evaluated inline
  (`python3 -c ...`, no files written): `f* = 0`, both bands contain 0, and
  the costate bound is −5.
- Second revision: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 recheck_revision_checks.py`
  → `logs/recheck_revision_checks.json`, `logs/recheck_revision_checks.log`
  (6.6 s, single-threaded). Parts A1–A4 (symbolic), B (tilted LQ `h_0`),
  C (uncorrected LQ field loss), D (Check 5.3 agreement, read from the
  three implementations' logs).
- Second revision, literature: Crossref lookup of doi 10.1007/BF00932465;
  the Goenka–Liu–Nguyen PDF was converted with `pdftotext` in `/tmp` and
  read at footnote 26 and Assumption 6; one web search for a
  Seierstad–Sydsæter treatment of the Leitmann–Stalford condition (none
  found, so the pointer was dropped).
- The review's own checks are in `../reviews/calibration-review-checks/`;
  they were read, not rerun.
- Literature: web searches and fetches listed in Section 1 (marked [v]);
  Hager (2000) and Houska–Chachuat (2019) PDFs were converted with
  `pdftotext` in `/tmp` and read at the cited theorems; local library
  entries under `literature/papers/` were checked for existence and scope.
  Entries marked [vr] were checked by the reviewer.

Files in `research-20260929/theory-calibration/`:

- `scouting.md` (this note);
- `doublewell_calibration.py` (Example 3.6);
- `revision_checks.py` (revision checks A–C);
- `recheck_revision_checks.py` (second-revision checks A–D);
- `logs/doublewell_calibration.{json,log}`, `logs/revision_checks.{json,log}`,
  `logs/recheck_revision_checks.{json,log}`.

## 10. Revision after review

The review ([`../reviews/calibration-review.md`](../reviews/calibration-review.md))
found no false central claim. Changes, keyed to its findings, are listed
below as made in the first revision; where Section 11 refines an item
(Leitmann–Stalford wording, Remarks 5.2(b), (d), (e)), Section 11 takes
precedence.

1. **Band carry-over (F1–F3).** Section 2.3 now states the separator
   domain and the extended-valued band edges, and says which of [K]'s
   results carry over (the one-separator identity with finite `f*`; the
   whole-horizon upper bound only on bounded domains). Pinch regularity is
   a stated hypothesis. The false sentence ("exactness of the affine class
   is whether this tangent plane stays inside the band") is removed. It is
   replaced by "necessary, not sufficient", with the review's counterexample
   (gap 5), rechecked. The Riccati-band bullet notes the need for the
   `eps`-perturbation.
2. **Affine class (F4–F7).**
   - Theorem 3.1(2): the converse needs attainment of `f*`.
   - The SGM condition is identified as the pointwise Leitmann–Stalford
     condition (JOTA 1971) and cited. Only the mesh-uniform statement is
     claimed.
   - Theorem 3.3: the local-convexity hypothesis is explained (automatic in
     the interior); necessity holds at continuity points of `u*`; only
     `e_h -> 0` is used; the review's `x_0 = 1.3` sanity check is added.
   - The Runge–Kutta remark is labelled a sketch, with the scope of Hager's
     Theorem 2.1 stated (`U = R^m`, Mayer cost, order `>= 2`, bounds the
     Hamiltonian-minimizing control, not the stage controls).
   - Section 1.3 is corrected likewise: Dontchev–Hager 1993 for Euler with
     control constraints; the 2001 paper for state constraints,
     `O(h^{2/3})`.
3. **Theorem 3.5 (F8).** It is now stated to be exactly a certificate of
   convexity of the problem after eliminating states. The Riccati
   recursion and the reduced Hessian fail at the same `a` (rechecked at
   `N = 50`: both 2.5172880840743). Its novelty claim is dropped.
4. **Example 3.6 (F8, F15).** It is reinterpreted as a hidden-convexity
   example (the per-stage affine class cannot see condensed convexity), not
   a certification of a nonconvex problem. The costate gap now reads
   2.81–2.86. The condition `|xi| <= sqrt(a/(2b))` is added to the closed
   form. The finite-`N` threshold is noted to lie above `pi^2/4`. The
   script docstring now says Example 3.6.
5. **Failure modes (F4, F17, F18).** The consequence of Proposition 4.1 now
   says "no exact affine calibration". A positive gap would need dual
   attainment, which is not proved. The `Theta(1/h)`-stage conclusion is
   Corollary 4.3, with its four assumptions stated. "Convex state
   constraints are harmless" is restricted to Theorem 3.2; for Theorem 3.3
   it is unproved.
6. **Transfer theorem (F10–F14).**
   - Hypothesis (T2) now requires `(x*, u*)` to be admissible with `r = 0`
     on it, which step 1 needs.
   - Compactness of `D` and `U` is explicit in (T1), with the review's
     counterexample (`U = R`, strict calibration, Euler transcription
     unbounded below for every `h`), rechecked. Example 3.6 is noted to be
     outside the theorem as stated.
   - The `O(h)` rate in (T3) is replaced by uniform convergence (proof
     redone with `eta_h = e_h + h`).
   - Remark (b): strictness implies the Dontchev–Hager coercivity
     (identity rechecked for scalar states).
   - Remark (d): strictness in `x` is necessary; non-strict LQ fields lose
     `Theta(h)`, with the defect `h^2 alpha P (P - alpha)` derived here.
   - Remark (e): the tilt needs `lambda` above a threshold, and `h_0` scales
     like `eps e^{-lambda T}`.
   - Remark (f): uncorrected sampling loses `O(h^2)` in the strict case
     (when `e_h = O(h)`; see Section 11, R6).
   - Check 5.3: the review's nonconvex example is re-implemented
     independently: exact for `h <= 0.05`, while costate calibrations lose
     about 8.6.
7. **Novelty (Section 6 and Summary).** Theorems 3.3 and 3.5 are no longer
   claimed as new beyond the mesh-uniform statement of 3.3. Theorem 5.2 and
   Propositions 4.1–4.2 are "not found stated before; elementary".
8. **Minor.**
   - Proposition 3.7: in the SGM case the stage problems are nonconvex
     (F9).
   - Proposition 2.3 remark: concave minorants must be taken backward,
     stage by stage (F16).
   - Section 2.2: the dual's attainment needs [K, Theorem 1.1]'s
     hypotheses.
   - The runtime statement is corrected.

This revision was rechecked in
[`../reviews/calibration-recheck.md`](../reviews/calibration-recheck.md);
Section 11 lists the resulting changes.

## 11. Revision after review (second round: recheck R1–R8)

The recheck found no mathematical error; its verdict was "fixes needed",
for minor items. I verified each item myself before changing the text. The
checks are in `recheck_revision_checks.py` (Parts A–D, 6.6 s,
single-threaded) unless stated otherwise. No theorem changed.

1. **R1 (Leitmann–Stalford citation).** Verified: Crossref gives
   G. Leitmann, H. Stalford, *A sufficiency theorem for optimal control*,
   JOTA 8(3) (1971) 169–174. I read Goenka–Liu–Nguyen (WP 20-25, 2020).
   Footnote 26 restates the theorem with an integral hypothesis along
   admissible pairs plus a transversality condition. The pointwise
   augmented-Hamiltonian inequality is their Assumption 6, which implies
   the integral condition. (Their reference list gives the title as "A
   sufficiency condition …"; the Crossref title is used here.) Changes:
   Section 1.1, the Definition before Theorem 3.3, Summary item 1, the
   Novelty list, Section 6 and the Section 8 row now say "pointwise
   (sufficient) form of the Leitmann–Stalford condition", and Section 1.1
   states the integral form. The Seierstad–Sydsæter pointer was cited from
   memory; one search found only their own sufficiency theorem (IER 1977),
   so the pointer is dropped. The original paper was not read.
2. **R2 (scope of `h_0 ~ eps e^{-lambda T}`).** Verified:
   - The proof's constants give `h_0` of order `c^2` (far region
     `M_0 ~ C/c`; near-region convexity on a ball of radius `~(C/c) eta_h`
     with a Lipschitz Hessian).
   - For scalar LQ I derived the leading-order threshold
     `h_0 ≈ 4 e(T) m(T)/|K(T)|` (Part A2 checks the `O(h)` term
     symbolically). I measured `h_0` by bisection (Part B), using the exact
     test `F(s_{t+1}) >= s_t`, which is equivalent to PSD stage Hessians,
     with closed-form Riccati solutions. The measured ratios are 2.47–12.14
     and approach the predictions `(lambda+6)/3` and `2 lambda - 4`. The
     recheck's 2.6–12.7 comes from a coarser grid.

   Changes: Remark 5.2(e) now separates three things. The general tilting
   claim is labelled a sketch, with a short Young-inequality argument. The
   general `h_0` is of order `c^2` from the proof. The linear scaling is
   stated only for scalar LQ, with the new table. The attack plan item is
   reworded to match.
3. **R3 (Section 4 closing paragraph).** Verified: the paragraph stated the
   `Theta(1/h)` window count unconditionally. It now cites Corollary 4.3
   and its assumptions (i)–(iv). It says that at singular arcs the count
   needs interior discrete controls with `grad_x sigma_t != 0` at
   `Theta(1/h)` stages, which requires convergence assumptions not stated
   here. Corollary 4.3 now also says that its constants hold uniformly over
   the stages and in `h` (recheck Section 7).
4. **R4 (Check 5.3 agreement).** Verified from the three logs (Part D).
   The author–review differences are at most `1.9e-11` (transferred,
   uncorrected) and 1.46e-9, 1.49e-9 (costate-affine, `N = 40, 80`). The
   sentence now gives both figures and the comparison with the recheck's
   implementation. The `max|a_{t+1} - a_t|/h^2` sentence now quotes the
   measured range (5.29 at `N = 5`, 5.54–5.65 for `N >= 10`) instead of
   "≈ 5.6 at every `N`".
5. **R5 (Remark 5.2(d)).** Verified by hand and symbolically (Part A1): the
   `O(h^2)` coefficient is `(P - alpha)(alpha P + q)`, and it is exactly
   zero for `alpha = q = 0`. The review's measured exact case (c3, c4) is
   `alpha = 0`, `q = 1`, `Phi = 0`, outside the `q = 0` formula. Changes:
   Remark (d) gives the general-`q` defect and describes the measured exact
   case correctly. The Summary says non-strict LQ fields "can" lose
   `Theta(h)`.
6. **R6 (`e_h = O(h)` and the cross-reference).** Verified: Remark (f)
   needs `e_h = O(h)` for `O(h^2)`. The Summary and the Section 8 row now
   state this condition. Part C recomputes the uncorrected LQ field family
   with an own stage minimizer (exact minimization in `u`, then over the
   piecewise-quadratic function of `x`). gap/`h` = 2.25 … 2.55 for
   `N = 10 … 640`, equal to the recheck's `r2` part C to `2e-13`; the
   transferred field gaps equal the review's c4 to `2e-13`. The comment
   after Proposition 5.1 now cites these numbers and says that Remark
   5.2(d) measures the corrected family.
7. **R7 (novelty leftovers).** "is new" (Summary item 1, Novelty list) and
   "most substantive new result" (Summary item 5) now say "not found stated
   before". The Section 6 sentence on Theorem 5.2 now names all its
   hypotheses: compact sets, interior optimal controls and (T3).
8. **R8 (time-dependent `l`) and optional items.**
   - (T1)/(T2) now allow `l(t,x,u)`: continuous in `t`, `C^2` in `(x,u)`,
     with `(x,u)`-derivatives up to order 2 jointly continuous, and
     `L_t = h l(t_t, x, u)`. I rechecked the proof. In step 2 the `l_x`
     terms are evaluated at the same point and cancel, and elsewhere only
     uniform bounds and uniform continuity are used. A note after the proof
     says so.
   - Step 5 now says why `x^h_t`, `u^h_t` are interior for small `h`.
   - Remark (b): "for scalar states" is dropped. The identity is algebraic
     for any `n`, `m`; I checked it by hand in vector form and
     symbolically for `n = 2`, `m = 2` with a time-dependent `l` (Part A4).
     `r_xx` is written as `H_xx + P g_x + g_x^T P + Pdot`, and the stronger
     bound `Q_H >= 2c(||xi||^2 + ||eta||^2)` is stated.
   - Remark (c): the grid ratio 0.255 is replaced by the exact identity
     `r - (x^2+u^2)/4 = (u/2 - x^3)^2 + 3x^2/4` (Part A3). The recheck's
     bound `h_0 <= (2/K^2)^{1/3}` for `U = [-K, K]` is added, with the
     last-stage residual `h u^2/2 - h^4 u^4/4` checked symbolically.
   - Section 3.1 sanity check: "outside the concave region" is replaced by
     `|x| >= sqrt(a/(2b)) = 1`, where `w` equals its convex envelope. That
     is the region where SGM holds; the concave region is `|x| < 0.577`.
   - Theorem 3.1(3) now assumes that `(xbar, ubar)` is a global minimizer,
     restricts the adjoint formula to `1 <= t <= N-1`, and says that `p_0`
     is not determined when `x_0` is fixed.
   - Not changed: the recheck's remark that `r = 0` on the optimal pair is
     a normalization (only minimality of `r(t,.)` at `z*(t)` matters). The
     stated hypothesis is correct as written.

### 11.1 Root edits after the confirmation (2026-09-30)

The confirmation
([`../reviews/recheck-calibration-confirm.md`](../reviews/recheck-calibration-confirm.md))
found R1–R8 and the optional items applied correctly and raised four minor
wording points (its Section 3). Each was checked against the text before it
was changed. No statement or number changes.

1. **Summary item 4.** The fixed-duration window is now stated as the
   conditional conclusion of Corollary 4.3: "Under the assumptions of
   Corollary 4.3, ... fails on a time window of fixed duration, that is
   `Theta(1/h)` stages".
2. **Section 4, closing paragraph.** For singular arcs, Proposition 4.1 also
   needs interior discrete states; the sentence now says "the discrete
   states and controls are interior".
3. **Remark 5.2(e), scalar LQ.** "Derived to leading order" became "formal
   leading-order derivation" (also in the status table), and the sentence
   giving `h_0 ≈ C(lambda) eps e^{-lambda T}` now carries its conditions
   (`K(T) < 0`, binding stage near `T`).
4. **Optional points.** "Linear-cost certificate" became "certificate of
   linear size (checked in `O(N log N)`)" in the three places; Section 10,
   item 6 now says "when `e_h = O(h)`"; the Definition before Theorem 3.3
   mentions the transversality condition of the GLN restatement.
5. **Header.** It cites the confirmation.
6. **Attack plan, Section 7 (closing audit, 2026-09-30).** Item 3 above
   missed one place: the attack plan's reference to Remark 5.2(e) still said
   "derived to leading order". It now says "obtained by a formal
   leading-order derivation".

## Sources (web)

- Krotov 1967: https://www.mathnet.ru/eng/dan32784
- Hilscher–Zeidan 2002: https://www.math.muni.cz/~hilscher/Abstracts/a_suffopt.html
- Bohner 1996: https://scholarsmine.mst.edu/math_stat_facwork/483
- Hartman 1978: https://www.ams.org/tran/1978-246-00/S0002-9947-1978-0515528-6/
- Zeidan 1983: https://www.ams.org/tran/1983-275-02/S0002-9947-1983-0682718-3/
- Maurer–Pickenhain 1995: https://link.springer.com/article/10.1007/BF02192163
- Leitmann–Stalford 1971 (Crossref metadata; original not read): https://doi.org/10.1007/BF00932465
- Goenka–Liu–Nguyen, WP 20-25 (2020), restatement in footnote 26 (integral hypothesis) and Assumption 6 (pointwise form) [v]: https://repec.cal.bham.ac.uk/pdf/20-25.pdf
- Tamminen 2019: https://numdam.org/articles/10.1051/cocv/2018012/
- Ohsawa–Bloch–Leok 2011: https://arxiv.org/abs/0911.2258
- Lasserre–Henrion–Prieur–Trélat 2008: https://arxiv.org/abs/math/0703377
- Korda–Henrion–Jones 2017: https://arxiv.org/abs/1609.02762
- Henrion–Korda–Kružík–Rios-Zertuche 2024: https://arxiv.org/abs/2303.02434
- Korda–Rios-Zertuche: https://arxiv.org/abs/2205.14132
- Savorgnan–Lasserre–Diehl 2009: https://api.openalex.org/works/doi:10.1109%2FCDC.2009.5399899
- Wang–O'Donoghue–Boyd 2015: https://stanford.edu/~boyd/papers/adp_iter_bellman.html
- Summers et al. 2013: https://arxiv.org/abs/1212.1269
- Kang et al. 2024 (STROM): https://arxiv.org/abs/2406.05846
- Houska–Chachuat 2019: https://optimization-online.org/wp-content/uploads/2016/08/5581.pdf
- Houska–Chachuat 2014: https://faculty.sist.shanghaitech.edu.cn/faculty/boris/branchAndLift.html
- Schaber–Scott–Barton 2019: https://dspace.mit.edu/handle/1721.1/131526
- Hager 2000: https://people.clas.ufl.edu/hager/files/rk.pdf
- Dontchev–Hager 2001 [vr]: https://www.ams.org/mcom/2001-70-233/S0025-5718-00-01184-4/
- HPIPM (Riccati and reduced Hessian) [vr]: https://arxiv.org/abs/2003.02547
- Abhijeet et al. 2024 [vr]: https://arxiv.org/abs/2404.08621
- Ober-Blöbaum–Junge–Marsden: https://arxiv.org/abs/0810.1386
- Halkin 1966 / Holtzman 1966 (cited via): https://www.numdam.org/item/RO_1975__9_3_75_0/
