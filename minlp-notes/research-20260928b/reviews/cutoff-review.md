# Adversarial review: objective-cutoff propagation and spatial branch-and-bound node complexity

Date: 2026-09-29. Scope: every numbered result, the tables and the literature
section of
[`../bb-complexity/cutoff-propagation/cutoff-propagation.md`](../bb-complexity/cutoff-propagation/cutoff-propagation.md)
("the note"). Context read: the program, the
[spatial review](spatial-bb-review.md) (Section 1.3, Fix 2) and Sections 1–4
and 8.3 of the
[constrained note](../bb-complexity/spatial-constrained/instance-dependent-node-complexity.md).
The reviewer did not write the note and did not edit it. Reviewer code and logs
are in [`cutoff/`](cutoff/). The propagator
[`cutoff/ifbbt.py`](cutoff/ifbbt.py), the instances and the branch-and-bound
code were written independently and do not import the author's code. Floating
point without outward rounding throughout: the computations illustrate, they do
not certify.

## Verdict

No counterexample to any numbered theorem, lemma, proposition or corollary was
found. Every proof was checked line by line, and each holds as stated or after
a local fix. The errors are in side remarks, in the summary's wording, and in
one step of the proof of Lemma 2.1:

- The summary says an interior nondegenerate minimizer needs
  `Theta(eps^(-1/2))` rounds "in the computed examples". This is false as
  stated. `nondeg1` in monomial form has an interior nondegenerate minimizer
  and needs 4–7 rounds.
- The proof of Lemma 2.1(b) says that consecutive runs "compose to one run".
  They do not, because each new run restarts from the forward box. The
  conclusion still holds, for a reason the note does not give (Section 2).
- Section 4 says the expanded `linediag` is "locally one-sided" at `(1, 0)`.
  It is not: the cube loss there is `8.01 r`.
- The note says setting (FS1) includes "every representation in Section 3".
  It does not include the shared-base representations `s`, `st`, `u` and
  `centered`.
- Smaller slips: a wrong monotonicity reason in the examples after
  Corollary 3.3, one reversed table cell, one percentage range, and the
  `eps`-range of the `kappa^(-1/2)` remark.

Theorem 3.1 is the note's main technical tool. Its final (endpoint) version is
correct. A new test uses general non-monotone polynomial unary nodes, which the
author's test did not cover. The endpoint formula and the fixed point agree on
200 of 200 instances, under two schedules and in chain form. A targeted example
shows that the endpoint rule decides the answer. The rejected full-range version
would be wrong on it.

The node counts reproduce exactly: 55 cells of Table 7.1 were re-run with
independent propagation and bounding code, and all match.

On novelty: the Section 1 facts are known, as the note says. Theorem 3.8 is the
known "exact bound, no cluster" principle (Du–Kearfott; Wechsung et al.)
applied to the propagation bound. None of the following were found in the
sources checked:

- Theorem 3.1;
- the one-term-width bound (Corollary 4.2);
- the round-count results;
- the surviving lower bounds (Theorems 5.1–5.5).

Two prior statements should be cited:

- Schichl–Markót–Neumaier's blanket claim that constraint propagation has
  overestimation order 1 and therefore clusters. The note refines it and, for
  one-sided representations, contradicts it.
- Benhamou et al. (1999), who call the exact characterization of HC4-revise's
  output an open problem.

| Claim | Verdict | Main point |
|---|---|---|
| Lemma 1.1, Lemma 1.2, Prop. 1.4 (model, `F_lo <= pi_D <= min_C f`, schedule independence) | correct; known | proved for "fair exact" runs only. HC4 uses partial revise steps and needs one more sentence (Section 1) |
| Lemma 2.1 (hybrid family, merged propagation frames) | correct after a proof fix | "runs compose to one run" is false; the conclusion follows from `Z* ⊆ Z0(Π_x Z*)`. Test: 57 merged pieces, 0 violations |
| Theorem 2.2 (transfer principle) | correct | |
| Prop. 2.3 (`f* + |f - f*|`) | correct, elementary | |
| Theorem 3.1 (fixed point of flat sums, endpoint formula) | correct | 200/200 new instances; targeted example separates it from the rejected version |
| Remark 3.2 (chains of sums) | correct | 200/200 chain representations agree |
| Cor. 3.3 (one-sided exactness) | correct | the reason given for `h_c` on `(-inf, 0)` is wrong; the conclusion holds |
| Remark 3.4, Cor. 3.5, Prop. 3.6, Examples 3.7 | correct | |
| Theorem 3.8 (`eps`-independent node count) | correct for the idealized algorithm | fixed-point propagation of nonempty nodes need not terminate; state the stopping rule |
| Prop. 3.9 (`>= (pi/8 - o(1)) a eps^(-1/2)` rounds) | correct for the stated HC4 schedule | recursion reproduced exactly; bound holds in 36/36 runs; observed `pi a eps^(-1/2)` |
| Prop. 3.10 (`O(log log 1/eps)` rounds) | correct | observed 3–4 rounds against a bound of 7–10 |
| Conjecture 3.11 | labelled conjecture | evidence for `line3` is overstated |
| Lemma 4.1, Cor. 4.2 (one-term width) | correct | (FS1) does not contain the shared-base forms, contrary to the text. 60 random multivariate tests, 0 violations |
| Example 4.3 (`x^2 - 2xy + y^2`) | correct | four boxes checked |
| Lemma 4.4 (first-order loss) | correct | "locally one-sided at `(1,0)`" is wrong |
| Theorem 5.1 (vertex localization under CND) | correct | 127 removals, 0 violations; a stronger localization is observed |
| Theorem 5.2 (relaxation lower bounds survive with `min(alpha, alpha_F)`) | correct | "nodes" needs a bound on phases per node; "every lower bound" means those using (V) on `N_theta` |
| Example 5.3 | correct | constants reproduced exactly |
| Theorem 5.4 (`log(1/eps)` survives at isolated minima) | correct | constants rechecked; the `kappa^(-1/2)` regime needs `eps << kappa rho0^2`, not `eps << kappa` |
| Strip sharpness after Theorem 5.4 | correct | reproduced |
| Theorem 5.5 (transversal curves) | correct | |
| Remark 5.6 | heuristic, correctly labelled open | |
| Section 6 table | mostly correct | one cell reversed; upper rates for propagation runs are numerical |
| Table 7.1 | reproduced | 55 cells identical with independent code |
| Summary, round-count sentence | false as stated | `nondeg1` monomial form: interior minimizer, 4–7 rounds |

## 1. The model (Section 1)

**Lemma 1.1.** Monotonicity of `rho_E` is correct, including the case
`E ∩ Z = ∅`. Part (a) needs `rho_E(Zh)` to be a box containing every
hull-consistent `D`, which holds.

Part (c), continuity from above, is correct. It uses that `E` is closed. The
model ensures this by requiring each unary function to be continuous on a
closed domain, so `log` and `sqrt` must be restricted to closed domains, as the
note does.

**Gap: HC4 is not a "fair exact run".** Lemma 1.1(c) and the "exactly when"
part of Proposition 1.4(b) are proved for runs whose every step is an exact
revise `rho_E`. HC4, as in `fbbt.py` and in the reviewer's code, uses partial
steps: a forward step updates the parent only, and a backward step updates the
children only. The conclusion still holds, but the note must say why:

- each partial step is monotone and continuous from above, by the same
  argument;
- a box fixed by the forward and backward steps of `E_k` is fixed by `rho_E`.
  The projection onto the parent is `W_k ∩ op(Z_children) = W_k`, because the
  forward step already gives `W_k ⊆ op(Z_children)`.

So HC4 run to convergence reaches `Z*`, and the numerical "fix" mode computes
`pi_D`. This is one sentence to add.

**Schedule independence.** Propositions 1.4(a)–(c) are correct, and the
statement is the standard one. The reviewer's HC4 and a random chaotic schedule
(exact revises in a random order each round) gave the same empty/nonempty
verdict in all 400 propagations of the Theorem 3.1 test. The chaotic schedule
needs more rounds, for example `4.2/sqrt(eps)` against `3.14/sqrt(eps)` for
`(s-1)^2` ([`logs/sanity.log`](cutoff/logs/sanity.log)).

**Prior work.** The greatest-fixed-point and confluence facts are in
Benhamou, Goualard, Granvilliers and Puget (1999): "the algorithm is confluent:
the output is independent of the reinvocation order of constraints". They are
also in Bordeaux, Hamadi and Vardi (2007) and in Belotti et al. (2012), whose
p.10 quotation the reviewer confirmed in the local text. The note already calls
these facts standard.

## 2. Hybrid certificates (Section 2)

**Lemma 2.1, proof fix.** Part (b) begins: "Several consecutive runs compose
to one run, so Lemma 1.1(b) gives `Π_x Z*(B_0, c) ⊆ B_f`." A second run
restarts from `Z0(B_1)`. That box can be larger than the lifted box at the end
of the first run in the coordinates of operation nodes, so the restart is not
a step `rho(Z) ⊆ Z`.

Concrete case: `x^2` written as `-3x^2 + 2x^2 + 2x^2` on `[-1, 1]` with cutoff
`-0.01`. The first run ends with the first square in `[0.00333, 1]` and the
x-box unchanged. `Z0` of that x-box resets it to `[0, 1]`
([`logs/endpoint_example.log`](cutoff/logs/endpoint_example.log)).

The conclusion survives. A hull-consistent box `Z` satisfies
`Z ⊆ Z0(Π_x Z)`: each node interval lies in the image of its children's
intervals, and induction in topological order gives the claim.

- So `Π_x Z*(B_0, c) ⊆ B_1` implies `Z*(B_0, c) ⊆ Z0(B_1)`, and Lemma 1.1(b)
  applies to the second run.
- If the cutoff decreases within a phase, use the smallest cutoff: `Z*` for
  that cutoff is hull-consistent for all the larger ones.
- The same argument covers solvers that start a child node from the parent's
  lifted bounds intersected with the child box, because that start box
  contains `Z*(child, c)`.

Test ([`cutoff/merge_check.py`](cutoff/merge_check.py)). Two runs of 1–3
rounds each, with a restart from the forward box between them, on boxes around
optimal points, cutoffs in `[-1e-3, 0.3]` and six instance/representation
pairs. For each of the 57 frame pieces `S`, the fixed point `Z*(S, c)` projects
into `B_f`: 0 violations.

**Scope.** The model allows relaxation-based reductions only on x-boxes and
axis-parallel splits in x. Real solvers also:

- tighten bounds of auxiliary (lifted) variables by OBBT or reduced costs, and
  then run FBBT from those bounds;
- in some configurations, branch on auxiliary variables.

Points removed in that interleaved way are certified by neither (V) nor (Π).
"Every hybrid run" in Theorem 5.2 therefore means every run of the Section 2
model. The comparison with SCIP in Section 7.4 should say so.

**Theorem 2.2** is correct. The certified set
`{y ∈ C : pi_D(C, y) > c}` equals `C` minus the box `Π_x Z*(C, c)`. It is
therefore measurable, which the integral bound needs.

**Proposition 2.3** is correct and elementary. It needs `abs` among the unary
functions, which the model allows. It also needs `f` to be factorable, which
the Kolmogorov–Arnold theorem gives for continuous `f`.

## 3. Exact propagation (Section 3)

### 3.1 Theorem 3.1

**Proof.**

- Part (a) uses hull consistency constraint by constraint. The endpoints of
  `Z'_k` lie in the closed set `{z : phi_j(z) ∈ P_j}`, so
  `t_j(sigma), t_j(tau) ∈ T_j`. The endpoints of `P_j` are attained, so
  `T_j ⊆ t_j(Z'_k)`. The root step is then direct. Shared non-variable bases
  cause no problem, because each constraint is used separately.
- Part (b), the witness, is correct. I checked each projection:
  - onto `x_k` both endpoints survive, since `t_j` at the endpoints lies in
    `[m_j, h_j]`;
  - onto `p_j` the result is `t_j(U'_k) ∩ [m_j, h_j] = [m_j, h_j]`;
  - onto the root, every value of term `j` extends with the other terms at
    their minima;
  - the root endpoints are attained, because
    `b + sum m_j <= Phi(U') <= c`.
- `Phi` is continuous in the endpoints, so the minimum exists.

**Tests** ([`cutoff/t31_check.py`](cutoff/t31_check.py),
[`logs/t31_check.log`](cutoff/logs/t31_check.log)). The instances are 120
univariate and 80 bivariate flat separable sums. The terms are general
polynomial unary nodes of degree 2–5, with interior maxima and minima, plus
power nodes and at most one linear term per variable. The boxes are random.

- `min_U' Phi` is computed with exact term minima (critical points), a
  sub-interval grid, and Nelder–Mead.
- At `c = min Phi + 1e-6 scale` the fixed point is nonempty in 200/200
  instances, under both HC4 and the chaotic schedule.
- At `c = min Phi - 1e-6 scale` it is empty in 192. In the other 8, all
  bivariate, the fixed box has `Phi = c` to `1e-9`. So the reviewer's minimizer
  missed the true minimum, which is what (a) requires.
- (a) holds at every fixed box: `Phi(Z') - c <= 9e-10`.
- The chain-of-binary-sums representations give the same verdicts in 200/200
  instances (Remark 3.2).
- (a) with a shared base `s = x - y`: 71 nonempty fixed boxes, all with
  `Phi <= c` ([`logs/rounds_check.log`](cutoff/logs/rounds_check.log)).

**Power of the random test.** The minimum over sub-boxes of the rejected
full-range formula differs from that of the endpoint formula in only 4 of the
200 instances ([`logs/discr_check.log`](cutoff/logs/discr_check.log)). Random
tests of the "empty below the minimum" type therefore rarely separate the two
formulas.

A targeted instance does ([`logs/endpoint_example.log`](cutoff/logs/endpoint_example.log)).
Write `x^2` as `-3x^2 + 2x^2 + 2x^2`, three separate power nodes, on
`C = [-1, 1]`.

- The endpoint formula gives `Phi([-a, a]) = -3a^2 + max(0, 2a^2, 2a^2) = -a^2`,
  so `pi_D(C) = -1`.
- The full-range formula gives a minimum of 0 over sub-boxes, that is, exact
  propagation.
- Bisection with the reviewer's propagator gives `pi_D([-1,1]) = -1.0`,
  `pi_D([-0.1, 0.1]) = -0.01` and `pi_D([-0.1, 0.3]) = -0.03`. These match the
  endpoint formula exactly.
- The fixed box keeps `x ∈ [-1, 1]` while the concave term's square node drops
  the values near 0. This is the mechanism the note describes.

The single-term `x^2` has `pi_D = 0`. The example makes the note's point that
the representation, not `f`, decides exactness. It would be a useful addition.

### 3.2 Corollary 3.3 to Examples 3.7

- **Corollary 3.3** is correct. One example is misjustified: for
  `h_c(s) = s^4 + (c-2)s^2 - 2cs + (1+c)` on `(-inf, 0)`, "only `s^4`
  decreases" is false. Both `s^4` and `-2cs` decrease, and `(c-2)s^2` is the
  only increasing term. Intervals there are still one-sided, with
  `j0 = (c-2)s^2` and `e` the right endpoint. The reviewer checked
  `pi_D = min h` on three intervals in `s < 0`
  ([`logs/loss_check.log`](cutoff/logs/loss_check.log), item 7).
- **Remark 3.4** is correct under its hypothesis `t_j'(z0) ≠ 0`.
- **Corollary 3.5** is correct: the identity is algebra, and `G_k >= 0` under
  one-sidedness follows from `f_k(e) = h_{j0} + sum_{j≠j0} m_j`. The sentence
  "if all coordinates but one have zero forward excess, propagation is exact"
  also needs that coordinate to be one-sided. That is the context of the
  sentence, but it should be said.
- **Proposition 3.6** is correct.
- **Examples 3.7** are correct.
  - (a): `u >= 0` on the forward range.
  - (b): expanded `nondeg1s` is
    `-2y^4 + (8/3)y^3 - (1/3)y^2 - (10/27)y + 7/81`. On `y > 0` all four terms
    are monotone and only `(8/3)y^3` increases, so every sub-interval of
    `[0, 1]` is one-sided. This explains the one-node counts; the note states
    them without this reason.
  - (c), (d): if `C ⊆ {x - y > 1/2}`, the forward `s`-range excludes 0,
    because its lower end is attained at a vertex of `C`.
  - (e): the inequality `R_i^2 - sum_l k_l R_l^4 >= R_i^2(1 - nK R_i^2)` is
    right.

### 3.3 Theorem 3.8

The proof is correct. The potential `Psi` falls by at least 1 at each split of
a box wider than `w*`. Nodes of width at most `w*` are pruned: by propagation
if they lie in `R`, and otherwise by (U_tau) after any contraction. `delta`,
`R` and `w0` for the listed examples check out; for example
`h(1/2) = 0.6875` and `h' = (s-1)(2s+1)^2 <= 0` on `s <= 1`.

**Idealization.** "Fixed-point cutoff propagation at every node" does not
terminate in general on nodes whose fixed point is nonempty. Convergence can
be infinite (Lemma 1.1 and the note's own citation). The proof uses only two
things:

- nodes with empty fixed point are emptied, which takes finitely many rounds
  by Lemma 1.1(c);
- any contraction is allowed elsewhere.

The algorithm should therefore be stated as "propagate until empty, or until
some finite stopping rule", with the remark that the rounds needed are
unbounded as `eps -> 0` (Proposition 3.9). Du and Kearfott's Remark 1 is the
analogue for exact interval bounds, and the note cites it. Wechsung, Schaber
and Barton (2014) should also be cited: "When K is sufficiently small, i.e.,
K <= λ1/8, the cluster problem is completely absent (N = 1)" (local text,
p.8).

### 3.4 Round counts

**Proposition 3.9.** Correct for the HC4 schedule it states.

- The one-round recursion `y' = y - (y^2+eps)/(2a)`,
  `x' = sqrt(a^2 + 2ax - eps) - a` agrees with the reviewer's propagator to 12
  digits over 5 rounds.
- The squared inequality `(x^2+eps)(1 + 2x/a - (x^2+eps)/a^2) >= 0` is right.
- The nonemptiness conditions and the arctan step are right.

Runs for `a ∈ {1, 2}`, three start boxes and `eps = 1e-2..1e-7`: the proved
lower bound holds in all 36 runs, and `rounds · sqrt(eps)/a` tends to
`3.14 = pi` ([`logs/rounds_check.log`](cutoff/logs/rounds_check.log)). The
bound is a factor of 8 below the observed count, as the note says.

The proof is tied to one schedule. The summary's "a proved
`Omega(eps^(-1/2))`" should say "for HC4". A schedule-free version, counting
revise applications, looks straightforward but was not checked. The chaotic
schedule needs about `4.2/sqrt(eps)` rounds here.

**Proposition 3.10.** Correct. The reviewer observed 3–4 rounds for
`eps = 1e-2..1e-12`, against the bound of 7.05–9.84.

**Conjecture 3.11** is correctly labelled. The evidence overstates one case.
For `line3/st` with `R = 10`, the fitted exponent over `1e-1..1e-4` is 0.72,
against 0.54 without propagation. The counts are below and approaching the
propagation-free counts, so the exponent may agree asymptotically. Over the
tested range, however, it does not. Section 7.2's "the growth rate of the
propagation-free runs is unchanged" should exclude `line3`, or say
"approaches".

## 4. Witness lemma and first-order loss (Section 4)

- **Lemma 4.1** is correct. Inside a single-use term the arguments of each
  binary node are independent, so exact images give hull consistency. The
  root argument is as in Theorem 3.1(b).
- **Scope error.** Setting (FS1) says "so is every representation in
  Section 3". The shared-base representations `s` and `st` (the node `x - y`
  feeds `s^4`, `s^2` and `s`), `u` and `centered` are not single-use per term.
  The lemma extends to them when the shared bases are single-use expressions,
  but that is not what is proved. Nothing downstream depends on it: Sections
  4–5 are applied to expanded forms.
- **Corollary 4.2** is correct. Test on 60 random 2–3-variable monomial sums
  ([`logs/merge_check.log`](cutoff/logs/merge_check.log)): 0 violations of
  `pi_D <= F_lo + max width`, and 0 points of a random sub-box `U'` removed at
  `c = Phi_full(U')`.
- **Example 4.3** is correct. For the four boxes `[0.5,1.5]^2`,
  `[0.5,2]×[0.8,1.5]`, `[0.1,3]×[1,1.2]` and `[0.9,1.1]^2`:
  - `pi_D(C) = -1.125, -1.402, -0.428, -0.360`, each at most `-2a(b-a)`;
  - all diagonal points survive at `c = -2a(b-a)`;
  - on `[0.9,1.1]^2` the witness value is attained.
- **Lemma 4.4** is correct: the Taylor remainder in the `l1` norm and the
  collection of terms check out.
  - The reviewer reproduced `D_i` and `L` independently: `D = 12, 2.352, 22`
    and `L = 24, 11.62, 76` at `t = 0.5, 0.2, 1`; `L = 8` for `iso2`, `rot0.1`
    and `rot1`.
  - Cube losses reproduce: `50.95 r`, `18.49 r`, `139.9 r`, `7.99 r`,
    `8.01 r`.
  - `L = 8` at `(1, 0)` holds for every `kappa`: `16 - 8` for
    `kappa <= 1/2`, and `18 - 10` at `kappa = 1`.
- **Error in "measured values".** "At `t = 0` the point `(1, 0)` has a zero
  coordinate, and the representation is locally one-sided." At `(1, 0)`,
  `D_1 = D_2 = 0` but `L = 8`. The reviewer's cube loss there is `8.01 r`
  ([`logs/loss_check.log`](cutoff/logs/loss_check.log)). So the expanded
  representation is not exact near `(1, 0)`: it has face-type loss (ND1
  without CND). Only the coordinate-segment witness loses nothing to first
  order.
- The CND discussion (two terms of each sign in each coordinate; quadratics in
  two variables never satisfy it) is correct.

## 5. Lower bounds that survive propagation (Section 5)

### Theorem 5.1

The proof is correct. The segment witness gives
`pi_D <= f(y) - D0 delta + K0 delta^2 <= f(y) - D0 delta/2`, which forces
`delta < rho*` and hence `delta = d_i^C(y)`. Then `a_i <= d_i w(C)` gives (V)
with `D0/(2 n w(C))`. The remark about boxes is right, because
`max_j sum_i <= sum_i max_j`.

**Tests** ([`logs/loc_check.log`](cutoff/logs/loc_check.log)).

- Setup: expanded `linediag`, 800 boxes around points `y = (t+1+u, t)` with
  `t ∈ [0.3, 1.1]` and `|u| <= 0.012` (so `m + eps < theta`). Face distances
  are log-uniform down to `1e-3 r`, with `r = 2(m+eps)/min_i D_i(y)`.
- `y` was removed 127 times, and every removal had `d_i^C(y) < r` in every
  coordinate. The largest ratio was 0.30.
- An earlier sampling with face distances of order `r` produced no removals at
  all: a removal needs a box much smaller than `r`
  ([`logs/loss_check.log`](cutoff/logs/loss_check.log), item 5).

**Observation: stronger localization.** In all 127 removals, both faces were
within `r` in every coordinate, not just the nearer one. The mechanism appears
to be one-sided segments `y + [0, delta] e_i`. They give
`Phi_full <= f(y) - delta (D_i - d_i f(y))/2 + O(delta^2)`, and the mirror
segment gives the same with `+ d_i f(y)`. So near stationary points, CND forces
the whole box to have width `O(m + eps)`. The reviewer did not write this out
as a proof. The note's weaker statement suffices for its purpose.

### Theorem 5.2

Correct as an application of Lemma 2.1, Theorem 2.2 and Theorem 5.1. Two
wording issues:

- "Every hybrid run needs `Omega(eps^(-p/2))` nodes" holds for `|P|`, that is
  leaves plus `2n` times the phases and rounds. It holds for nodes only under
  (c)'s assumption of at most one phase per node, or more generally a bounded
  number of phases per node.
- The summary says that when "the term gradients cancel without a dominant
  term ... every lower bound of the relaxation-gap theory survives". That is
  Theorem 5.2 under CND, and only for bounds that use (V) at points of
  `N_theta`. Under ND1 alone, only Theorems 5.4–5.5 hold.

**Example 5.3.** The reviewer recomputed
`D0 = 2.3520`, `K0 = 322.7`, `rho* = 0.00364`, `alpha_F = 0.1400` and
`theta = 4.29e-3`. The covering bounds `1.5, 4.25, 13.5, 42.25` also reproduce
([`logs/ex53_check.log`](cutoff/logs/ex53_check.log)).

### Theorem 5.4

The proof is correct. The reviewer checked each step:

- the cube witness;
- `|m(y) - m(y')| < (m+eps)/4`, and hence
  `(3/4)(m+eps) < M(z) < (5/4)(m+eps)`;
- the layer thickness `(8/3) M(z)/L0`;
- the sup-norm layer-cake integral `(n-1) 2^n rho0`, which is also right for
  `n = 2`;
- `K_F = (16 n (n-1) 2^n rho0/(3 L0))(5/4)^(n/2) gamma^(1-n/2)`;
- the final estimate
  `n 2^(n-1) (2 Gamma)^(-n/2) log(Gamma r1^2/eps)`.

Face-localization test (`iso2` and `rot0.1`, 800 boxes with one coordinate
thin at scale `eps`): `x*` or a nearby point was removed 125, 127, 10 and 6
times. There were 0 violations of `min_i d_i^C < 2(m+eps)/L0`
([`logs/loc_check.log`](cutoff/logs/loc_check.log)).

**The `kappa^(-1/2)` remark.** The hypothesis `|d_i m| <= L0/8` on
`Q(x*, 2 rho0)` forces `rho0 <~ 1/(2(18 + 4 kappa)) ≈ 0.027`. `N_theta` is cut
off by this cube along the soft direction. The integral grows like
`2 pi (det H)^(-1/2) log(1/eps)` only once `eps << kappa rho0^2`, which is
about `7e-4 kappa`, not once `eps << kappa`. The scaling claim is right
asymptotically; the stated range is not.

### Strip sharpness, Theorem 5.5, Remark 5.6

- Strip sharpness is reproduced. For the `iso2` strip, `-pi_D/h = 7.955`,
  `7.996` and `8.000` at `h = 1e-2..1e-4`. For the `rot0.1` strip,
  `pi_D -> -0.85`.
- Theorem 5.5 is correct. Each coordinate is strictly monotone along `S`, so
  each slab meets `S` in one arc. The face-slab term `4n r_F/tau0` is
  conservative by a factor of 2.
- Remark 5.6 is heuristic and correctly labelled open.

## 6. Section 6 and the representation table

The dichotomy is stated accurately elsewhere in the note, and the
"box-likeness in x" paragraph is correct: the bounding-box volume ratio
`(2/pi)(sqrt(l1/l2) + sqrt(l2/l1))` checks out. Corrections to the table:

- In the `rot_kappa` row, the "no propagation" cell says "same, 2 fewer
  nodes". The propagation-free runs have 2 **more** nodes (73 against 71 at
  `1e-2`).
- `Theta(...)` in the expanded column combines a proved lower bound
  (Theorems 5.2 and 5.4) with an upper rate that is only observed for runs with
  propagation. The constrained note's bisection upper bounds are for trees
  without contraction. Contraction changes split points, and "propagation can
  only help" is not a theorem about tree size. The table and the summary should
  say "observed" for the upper side.
- The summary claims the one-sided representations need `O(1)` nodes. This is
  proved under Theorem 3.8's hypotheses and observed in the table.

**Summary, round-count sentence.** It says "an interior nondegenerate minimizer
needs `Theta(eps^(-1/2))` rounds to reach the fixed point in the computed
examples". `nondeg1` in monomial form (`t^2 - 2t^4`, terms `t^2` and `t^4`,
minimizer `t = 0` interior to `[-1/3, 2/3]`) needs 4, 5, 6, 6, 6, 7, 7 rounds.
Those are the note's own `rounds.log` counts, reproduced by the reviewer. The
distinction that matters is the one in Remark 3.4 and Proposition 3.10: whether
every term is strictly monotone at the minimizer, so that the minimizer is
interior to every term's range. Suggested wording: "a minimizer at which every
term is strictly monotone (interior to all lifted ranges)".

## 7. Computations (Section 7)

**Node counts, independent re-run** ([`cutoff/bbcheck.py`](cutoff/bbcheck.py),
[`logs/bbcheck.jsonl`](cutoff/logs/bbcheck.jsonl)). The node model is the
note's. The propagator is the reviewer's, with exact revises in the backward
pass. The alphaBB minimum is computed by bisection on the derivative in 1D and
by TNC plus a linearization bound in 2D and 3D. The author used L-BFGS-B.

All 55 cells match the note's Table 7.1 and `logs/tables.md` exactly:

- `nondeg1`: off 13/29/45/57; `u` and `mono` at the fixed point: 1.
- `h1`: off 11/17/23; `exp` with `R = 10`: 5/9/17; `R = 3`: 7/13/19; fixed
  point: 1, with 54/587/5919 rounds.
- `nondeg1s` `exp` with `R = 10`: 5/17/31.
- `nd2`: off 107/241/369; `mono` at the fixed point: 17.
- `iso2`: off 41/73; `exp` at the fixed point: 29/55.
- `rot0.1`: off 135/235; `exp` at the fixed point: 133/233; `st` at the fixed
  point: 1.
- `rot0.01`: 273/575 and 271/573.
- `linediag` at `1e-3`: off 1329, `exp` at the fixed point 1325, `s` with
  `R = 10` 1221, `R = 3` 1275, `s` at the fixed point 1 (also at `1e-6`).
- `line3` at `1e-2`: off 2235, `st` at the fixed point 1.

The column is `1e-2, 1e-4, 1e-6, 1e-8` where four values are given, and
`1e-2, 1e-4` where two are given. The whole run took 5 seconds on 6 workers.

**Representations and `alpha`.** The representations match `f` to `1.1e-13`
on 200 random points each ([`logs/sanity.log`](cutoff/logs/sanity.log)). Each
`alpha` is at least half the magnitude of the most negative Hessian eigenvalue
found on a grid of the root box
([`logs/alpha_check.log`](cutoff/logs/alpha_check.log)). The value is attained
exactly for `nondeg1`, `h1`, `linediag`, `iso2` and `rot`. It is `3.32` against
`4.5` used for `nd2`, and `2.68` against `3` for `line3`.

**Smaller misstatements.**

- Section 7.2 says propagation removes "4–30 % of the nodes on `iso2`". At
  `eps = 1e-1` the count drops from 31 to 19, which is 39 %. The range over
  the table is 4–39 %.
- Section 7.2 says bounded rounds leave the growth rate unchanged for
  `line3`. See Conjecture 3.11 above.

**SCIP comparison (Section 7.4).** The numbers match the other workstream's
[`results/summary.md`](../bb-complexity/solver-validation/results/summary.md):

- `linediag2` at `1e-6`: 65701 by default, 66661 with `noweakdual`;
- `ring2`: 56151 against 66991 with `nocutoffprop`, and 1 node with `noexpand`
  at every `eps`;
- `isofbbt2`: 15 against 37 with `noweakdual`.

The `maxproprounds` probe header says "default 10". Note that `nocutoffprop`
leaves `isofbbt2` at 15 nodes, and only `noweakdual` raises it. The note quotes
the setting that shows the effect, which is fine, but "switch off cutoff-based
reductions" covers two settings with different effects.

## 8. Corrections, consolidated

1. **Lemma 2.1(b), proof.** Replace "several consecutive runs compose to one
   run" with the argument that a hull-consistent box lies in `Z0` of its
   projection. Hence `Z*(B_0, c) ⊆ Z0(B_1)`, and each later run keeps it. Use
   the smallest cutoff of the phase. Add that start boxes inherited from a
   parent are covered.
2. **Lemma 1.1(c) / Proposition 1.4(b).** Add that HC4, whose steps are
   partial revises, also converges to `Z*`: its common fixed points are
   hull-consistent, and each step is continuous from above.
3. **Summary.** Qualify the round-count sentence as in Section 6 of this
   review. Replace "every lower bound ... survives" by the CND and ND1 split.
   Mark upper rates for runs with propagation as observed.
4. **Examples after Corollary 3.3.** On `(-inf, 0)`, the only increasing term
   of `h_c` is `(c-2)s^2`.
5. **Setting (FS1).** Delete "and so is every representation in Section 3",
   or extend Lemma 4.1 to single-use shared bases.
6. **Section 4, measured values.** At `(1, 0)` the expanded representation has
   `D_i = 0` and `L = 8`. There is a cube loss of `8 r` there, so it is not
   locally one-sided.
7. **Theorem 3.8.** State the propagation rule so the algorithm is finite, or
   call it idealized.
8. **Theorem 5.2.** Say "leaves plus phases", or assume a bounded number of
   phases per node, when concluding about nodes.
9. **Remark after Theorem 5.4.** Change `eps << kappa` to
   `eps << kappa rho0^2`.
10. **Section 6 table.** "2 fewer" should be "2 more", in the no-propagation
    column of the `rot_kappa` row.
11. **Section 7.2.** Change "4–30 %" to "4–39 %", and qualify `line3` with
    `R = 10`.
12. **Scope.** The `Omega(eps^(-1/2))` of Proposition 3.9 is for the HC4
    schedule. "Every hybrid run" excludes lifted-space OBBT interleaved with
    FBBT, and branching on auxiliaries.
13. **Literature.** Add the sources in Section 9 below.

## 9. Novelty

**Sources.** The note's local sources were used. A delegated reader also went
through the local full texts of Vu–Schichl–Sam-Haroud (2009), Chabert–Jaulin
(2009), Faltings (1994), Dlask–Werner (2024), Wechsung–Schaber–Barton (2014),
Kannan–Barton (2017), Du–Kearfott (1994), Araya et al. (2010), Schichl–Neumaier
(2005), Neumaier (2004), Belotti et al. (2012), Puranik–Sahinidis (2017) and
Borst et al. (2024).

The same reader fetched from the web Benhamou et al. (1999), Bordeaux–Hamadi–
Vardi (2007), Lhomme (1993), Chabert–Jaulin (CP 2009), Araya–Neveu–Trombettoni
(2011, occurrence grouping), and the preprints of Schichl–Neumaier (2004,
SIAM) and Schichl–Markót–Neumaier (2014). General web search was out of quota.

The reviewer confirmed the Wechsung, Du–Kearfott, Araya, Neumaier and Belotti
quotations in the local texts. The web-sourced quotations below come from the
delegated reader and were not re-checked by the reviewer.

**Known.**

- **Section 1** (greatest fixed point, confluence, schedule independence):
  Benhamou et al. (1999), Bordeaux et al. (2007), Belotti et al. (2012),
  Dlask–Werner (2024), and Puranik–Sahinidis (2017), citing Caprara–Locatelli.
  The note says this.
- **Theorem 3.8** is the "exact bound, no cluster" principle: Du–Kearfott
  (1994, Remark 1), Wechsung et al. (2014, `K <= lambda_1/8` gives `N = 1`)
  and Kannan–Barton (2017). What is new is applying it to the propagation
  bound `pi_D`, together with the conditions (Corollary 3.3, Proposition 3.6)
  under which `pi_D` is exact.
- **Proposition 2.3** and the representation dependence are folklore: DAG
  against tree in Schichl–Neumaier (2005) and Vu et al. (2009); occurrence
  grouping. Neumaier (2004, p.29) lists "min x − x s.t. x ∈ [0, 1]" as a
  pathological case.
- **Slow convergence** is known, as geometric rates (Neumaier 2004, p.42;
  Belotti et al. 2012), non-termination (Davis, via Faltings 1994), and
  hardness (Bordeaux et al. 2007). The tangency rate `Theta(eps^(-1/2))` of
  Proposition 3.9 and the doubly exponential rate of Proposition 3.10 were not
  found.

**Not found; plausibly new.**

- **Theorem 3.1.** Benhamou et al. (1999, §4.1) write that "the exact
  characterization of the result provided by the execution of HC4revise is
  still an open problem" (a single revise). Araya et al. (2010, p.3) give
  `x^2 - 3x + y = 0` on `[4,10] × [-80,14]`, where HC4-revise gives no
  contraction.
  - The reviewer confirmed that the fixed point of the decomposed propagation
    also leaves `y ∈ [-80, 14]`, while the true hull is `[-70, -4]`
    ([`logs/araya_example.log`](cutoff/logs/araya_example.log)).
  - This is prior evidence of fixed-point dependency loss and should be cited.
  - Monotonicity-based exactness (Araya et al.; Chabert–Jaulin) differs from
    Corollary 3.3, which allows non-monotone `f` and gets exactness only at the
    fixed point of iterated propagation.
  - Collavizza–Delobel–Rueher (1999, "Comparing partial consistencies") and
    Hansen–Walster (2004) were not accessible. They are the most likely places
    for overlap.
- **Corollary 4.2 and Lemma 4.4.** The closest statement is
  Schichl–Markót–Neumaier (2014 preprint, §2) and Schichl–Neumaier (2004, §3):
  "constraint propagation techniques lead to overestimation of order k = 1,
  hence they suffer from the cluster effect", given without proof. The note
  proves this for flat sums with loss (first-order loss, Lemma 4.4). It shows
  the claim is false for one-sided representations: zero loss and no cluster
  (Corollary 3.3, Theorem 3.8). The note mentions only a repository paraphrase
  of this statement. It should cite the original and reconcile the two.
- **Lemma 2.1 (merging), Theorem 2.2 and Theorems 5.1–5.5.** No lower bound on
  node counts that survives propagation was found. The cluster analyses are
  upper bounds or worst-case counts, and they do not model domain reduction.
  Within the repository these are clean extensions of the constrained note's
  (V)-based arguments. The mathematical steps are short once the witness lemma
  is available.

As the note says, an unsuccessful search does not establish novelty.

## 10. What remains unchecked

- **Literature not examined.** Hansen–Walster (2004), Collavizza et al.
  (1999), Kearfott (1996), Ratschek–Rokne (1988), Messine (2004), Apt (1999),
  and the journal version of Schichl–Markót–Neumaier (2014).
- **Web-sourced quotations.** They were not re-verified by the reviewer.
- **Theorem 3.1 beyond polynomials.** Unary functions other than polynomials,
  such as `exp`, `log` and `abs`, were checked by proof only.
- **Not re-run.** The 3D sweeps (`iso3`; `line3` at `eps < 1e-2`; `line3/exp`),
  `linediag/exp` and `off` at `eps <= 1e-4`, and the author's own
  `check_formula.py` (replaced by the independent test). The author's
  statement that the rejected formula failed 9 of 18 cases cannot be checked,
  because its output was overwritten.
- **Schedule-free Proposition 3.9.** A version for any schedule, counting
  revise steps, was not worked out.
- **Stronger localization.** The two-sided localization under CND (Section 5
  of this review) is an observation plus a sketch, not a checked proof.
- **SCIP.** Not run. Only the other workstream's summary was compared.
- **Arithmetic.** Everything is floating point without outward rounding.
  Bisection estimates of `pi_D` treat a round limit as "nonempty", so they can
  only be low.

## Reviewer checks run

All from `research-20260928b/reviews/cutoff/` with `OMP_NUM_THREADS=1`, and at
most 6 worker processes. These are targeted checks only. No project-wide
checks were run, CI was not inspected, and nothing was committed. The note was
not edited.

- `python3 sanity.py > logs/sanity.log`: representations equal `f`; root round
  counts for `(s-1)^2` and `nondeg1` under HC4 and a chaotic schedule.
- `python3 t31_check.py > logs/t31_check.log` (8.5 min): Theorem 3.1 and
  Remark 3.2 on 200 instances with non-monotone unary nodes.
- `python3 discr_check.py > logs/discr_check.log`: how often the endpoint and
  full-range formulas differ (4/200).
- `python3 endpoint_example.py > logs/endpoint_example.log`: the
  `-3x^2 + 2x^2 + 2x^2` example.
- `python3 rounds_check.py > logs/rounds_check.log`: Propositions 3.9 and 3.10,
  and Theorem 3.1(a) with a shared base.
- `python3 loss_check.py > logs/loss_check.log`: Example 4.3; `D_i`, `L` and
  cube losses; strips; the first, powerless localization sampling; `h_c` on
  `s < 0`.
- `python3 loc_check.py > logs/loc_check.log`: localization tests for
  Theorems 5.1 and 5.4.
- `python3 ex53_check.py > logs/ex53_check.log`: Example 5.3 constants.
- `python3 merge_check.py > logs/merge_check.log`: merged frames (Lemma 2.1);
  Corollary 4.2 and Lemma 4.1 on random monomial sums.
- `python3 araya_example.py > logs/araya_example.log`: the fixed point for
  Araya et al.'s example.
- `python3 bbcheck.py 6 > logs/bbcheck.jsonl`: 55 cells of Table 7.1.
- Inline script `> logs/alpha_check.log`: `alpha` against the grid minimum
  Hessian eigenvalue.
