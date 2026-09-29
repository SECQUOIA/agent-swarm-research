# Recheck of the revised cutoff-propagation note

Date: 2026-09-29. Scope: the substantive revisions listed in Section 11 of
[`../bb-complexity/cutoff-propagation/cutoff-propagation.md`](../bb-complexity/cutoff-propagation/cutoff-propagation.md)
("the note"), made after the [first review](cutoff-review.md). The reviewer had
not seen the note before, did not write it, and did not edit it.

Code and logs are in [`cutoff-recheck/`](cutoff-recheck/). The propagator
[`iprop.py`](cutoff-recheck/iprop.py) and the instances
[`inst.py`](cutoff-recheck/inst.py) were written from scratch and import
neither the author's code nor the first reviewer's code. The author's
[`check_revision.py`](../bb-complexity/cutoff-propagation/check_revision.py)
was read, not reused. All computations use floating point without outward
rounding: they illustrate, they do not certify.

## Verdict

| Revision | Verdict | Main point |
|---|---|---|
| (1) Lemma 1.2(d) | correct | Proof checked. 329/329 converged fixed points satisfy `Z ⊆ Z0(Π_x Z)`. 37/346 one-round boxes do not, so the lemma has content. Nit: constant nodes |
| (1) Lemma 2.1(b), new proof | correct under two stated or implicit assumptions; both need fixing in the text | Restart enlargement is handled correctly. 0 violations in 20,750 start-box checks, 667 frame pieces and 853 emptied phases, including decreasing cutoffs, depth-3 inheritance and second phases. **Gap A:** the model allows constraint propagation inside runs; then (Π) fails (explicit counterexample). **Gap B:** the proof needs a nonincreasing incumbent, while Theorem 5.2 says "any ... incumbents"; using the smallest cutoff along the inheritance chain removes the need |
| (2) HC4 paragraph after Lemma 1.1 | correct | Each claim checked. HC4 and random orders of partial steps reach the same limit in 200/200 cases (max difference 8e-15) |
| (3) Remark 4.1a | correct, and more general than stated | Witness hull-consistent in 300/300 random shared-base DAGs; 750/750 checks on `s`, `st`, `u`, `centered`. Single use is **not** needed: 300/300 also for bases in which a variable occurs twice |
| (4) Proposition 5.1a | correct | Proof checked line by line. 0 violations in 909 removals under verified hypotheses. Adversarial search: the far face reaches 0.500 of the bound, so the constant is within a factor 2 of sharp |
| (5) Proposition 3.9 | correct for the stated HC4 schedule | Recursion reproduced to 4e-16. Bound holds in 84/84 runs, always at least 8 times below the observed count |
| (5) Restated round-count criterion | **false as stated**, including on the note's own data | `rot_kappa`/`st` and `line3`/`st` have a term stationary at the minimizer, with the minimizer at the end of that term's lifted range. They still need `5.92 eps^(-1/2)` rounds (Table 7.1: 55, 588, 5920, 59234). So does `x^2 - 2x + 1 + (x-1)^4` |
| (5) Conjecture 3.11, restated | hypothesis inconsistent with its cited examples | Example 3.7(d) and `line3`, cited as instances or evidence, do not satisfy "every term strictly monotone" |

No numbered theorem, lemma or proposition was found false. The problems are
in the round-count criterion that the revision introduced (Summary,
Section 3.3, Conjecture 3.11, Sections 7.2 and 11), and in two scope gaps of
Lemma 2.1. All three have short fixes (Section 6).

## 1. Lemma 1.2(d) and the proof of Lemma 2.1(b)

### Lemma 1.2(d)

The claim is that a hull-consistent `Z` satisfies `Z ⊆ Z0(Π_x Z)`. The proof
goes in topological order.
- Hull consistency of `E_k` makes the endpoints of `W_k` attained in
  `E_k ∩ Z`. They are therefore values of `op_k` on `Z_children`.
- That image is an interval, because a continuous image of a box is
  connected and, by the domain assumption, the children's intervals lie in
  forward images.
- By induction the children's intervals lie in those of `Z0(Π_x Z)`, and one
  forward operation is its exact image.

The proof is correct.

Nit: the lemma is stated for "every hull-consistent box". Constant nodes have
no elementary constraint, so a box that widens a constant's interval can be
hull-consistent without lying in `Z0(Π_x Z)`. Every use in the note has
`Z ⊆ Z0(B_0)`, where constants are points. Adding "`Z ⊆ Z0(X0)`" or "constants
fixed" closes this.

Test ([`check_merge.py`](cutoff-recheck/check_merge.py), part B): 329
converged nonempty fixed points on 9 instance/representation pairs, 0
violations. As a control, boxes taken after one HC4 round, which are not
hull-consistent, violate the inclusion in 37 of 346 cases. The backward pass
tightens `x` after the forward pass, so the lemma is not vacuous.

### The first review's point: restarts enlarge lifted intervals

Reproduced independently (part A). On `-3x^2 + 2x^2 + 2x^2` over `[-1, 1]`
with cutoff `-0.01`, the run ends with the first square node in
`[0.00333, 1]`. `Z0` of the unchanged x-box resets it to `[0, 1]`. The new
proof handles this correctly. It never needs the restart box to lie inside the
previous box. It needs only `D ⊆ Z0(B_i)`, which follows from `Π_x D ⊆ B_i`,
Lemma 1.2(d) and the monotonicity of `Z0`. Enlargement is irrelevant to that.

### The new proof, step by step

- *Smallest cutoff of the phase.* `D = Z*(B_0, c_min)` is hull-consistent for
  every larger cutoff, so Lemma 1.1(b) keeps it through each run. Correct. The
  choice matters: with the largest cutoff of the phase, 47 of 91 frame pieces
  are not certified (part C, control).
- *Restarts within a phase.* Correct, as above.
- *Children started from parent bounds.* Correct by induction:
  `Y ⊇ Z*(B_p, c_p) ⊇ Z*(B_p, c) ⊇ Z*(B_0, c) = D`. This uses `c <= c_p`
  (Lemma 1.2(b)) and `B_0 ⊆ B_p` (Lemma 1.2(a)). R-rel shrinks between the
  parent's phase and the split do no harm, since only `B_0 ⊆ B_p` is used.
- *Pieces and leaves.* `Z*(S, c) ⊆ D` gives `Π_x Z*(S, c) ⊆ B_f`, so
  `pi_D(S, y) > c` for `y ∈ S \ B_f`. An emptied phase has `D = ∅`. Both are
  correct.

Two start boxes are covered by the argument but not by the bullets: a later
run of the phase restarted from `Y ∩ Z0(B_i)`, and a second phase at the same
node started from that node's earlier lifted box. One sentence covers every
case: "every start box is `Z0` of the current x-box intersected with final
lifted boxes of earlier runs at this node or its ancestors, and each of these
contains `D`."

Test (part C): 9 instance/representation pairs, 80 random depth-3 trees each.
The setup was:
- 11,321 phases of 1–4 runs;
- restarts from `Z0(B_i)`, from `Z0(B_i) ∩` the previous lifted box, or from
  inherited bounds;
- the random partial-step order in 30 % of runs;
- 2,207 phases in which the cutoff decreased;
- 7,725 inherited starts and 2,465 second phases after R-rel-like shrinks.

The results were:
- `D` lay inside the start box in 20,750 of 20,750 runs;
- 667 of 667 frame pieces were certified;
- 853 emptied phases all had `D = ∅`.

The author's test (part B of `check_revision.py`) had a single cutoff per
phase, one level of inheritance, and only restarts from `Z0`.

### Gap A: constraint propagation inside runs

Section 2 lets a phase use runs "with cutoffs `c = UBD - eps` (and possibly
propagation of the constraints)". The proof uses Lemma 1.1(b), which covers
only revise steps of the objective graph and the cutoff. `D = Z*(B_0, c)` is
not hull-consistent for constraint revises, and Lemma 2.1(b) then fails.

Counterexample (part D). Take `f = -3x^2 + 2x^2 + 2x^2` on `X0 = [-1, 1]`, with
`F = {x >= 0.5}`, so `f* = 0.25`. The cutoff is `f* - 10^-3`, and
`g = 0.5 - x <= 0` is propagated in the same run. The run empties the root in
24 rounds, so `[-1, 1]` is a propagation leaf.
- Objective propagation alone removes nothing at this cutoff. Indeed
  `pi_D([-1,1], y) = Phi([-1,1]) = -1` for every `y`, so (Π) fails at the
  feasible point `y = 0.75`.
- (V) also fails there for `alpha > 0.717`, for example alphaBB with
  `alpha = 1`: `m + eps = 0.3135` against `q_C = 0.4375`.

Fix: either drop the parenthetical, so that constraint propagation becomes
separate (R-inf) rounds on x-boxes, or define `pi` on the graph that includes
the constraint nodes with their bounds. With the second option, Lemmas 1.1,
1.2(d) and the proof go through unchanged. Section 5 has `F = X0`, so nothing
downstream is affected. I could not tell whether the parenthetical predates
the revision, since the note is untracked. The first review did not mention
it.

### Gap B: the incumbent must not increase

The proof says the parent's cutoffs are at least `c` "because the incumbent
never increases". The node model is taken from the constrained note, whose
Lemma 2.1 allows "any incumbent values `UBD >= f*` (changing over time)".
Theorem 5.2 says "any ... incumbents" (note, line 1055). If a later cutoff is
larger than the parent's, the inherited box need not contain `D`.

Test (part E): 40 trees per instance with cutoffs that move up and down, and
children always starting from inherited bounds.
- With the phase's smallest cutoff, `D` was outside a start box 3,214 times,
  and 121 of 272 frame pieces were not certified.
- With the smallest cutoff along the inheritance chain (the current phase,
  plus every phase whose lifted box is inherited), there were 0 failures.

Since all cutoffs are at least `f* - eps`, (Π) still follows. Fix: use that
chain minimum in the proof, or state in Section 2 that `UBD` is nonincreasing
and drop "any incumbents" from Theorem 5.2. The first fix is the same length
and needs no assumption.

## 2. HC4 paragraph after Lemma 1.1

Each claim holds:
- The forward step `W_k := W_k ∩ op_k(Z_children)` is a run step. The
  projection of `E_k ∩ Z` onto the parent is exactly that set, and it is an
  interval by the domain assumption. The children are unchanged and contain
  their projections.
- The backward step, which updates children only, is a run step. Sequential
  updates of the two factors of a product are two such steps.
- Both steps are monotone. Both are continuous from above, for the same
  reason as in Lemma 1.1(c): the continuous image of a decreasing sequence of
  compact sets is the intersection of the images.
- A box fixed by both steps of `E_k` is fixed by `rho_{E_k}`: the parent's
  projection is `W_k ∩ op_k(...) = W_k`.
- The limit of a fair run is therefore hull-consistent and lies in `Z0(C)`.
  So it lies in `Z*` by (a), contains `Z*` by (b), and equals `Z*`.

Emptiness in finitely many steps follows by compactness. "Computes `pi_D` up to
its stopping tolerance" is informal but harmless.

Tests ([`check_hc4.py`](cutoff-recheck/check_hc4.py)):
- HC4 order against a random order of partial steps, on 200 random boxes and
  cutoffs over 8 representations. The verdict and the limit box agree in
  200/200 cases, with a largest difference of `8e-15`.
- 35 random 1D flat sums with repeated non-monotone monomials. The bisection
  value of `pi_D` is never above the grid minimum of the endpoint formula of
  Theorem 3.1(b); the largest excess is `2.2e-14`.

## 3. Remark 4.1a (shared single-use bases)

The proof is correct. Every node of a base gets its exact range over `U'`.
Each `p_j` gets `phi_j(Z'_k)`, and the root gets the interval of Lemma 4.1.
Every value of every interval below the root extends. The root step is as in
Theorem 3.1(b), because the root constraint treats the `p_j` coordinates as
independent.

**The single-use hypothesis is not needed**, in Remark 4.1a or in Lemma 4.1.
Give every non-root node the exact range of its expression over `U'`. Then
every elementary constraint below the root is hull-consistent: for any value
`w_a(x)` of a child, the point `x` gives values of the other child and of the
parent inside their intervals. The box lies in `Z0(C)` by the inclusion
property. Single use matters only in Corollary 4.2, where Moore's theorem
makes `F_lo(C) = b + sum_j min_C t_j`. So Lemma 4.1 holds for any DAG whose
root is a flat sum of distinct nodes `p_j`, with `Phi_full` computed from
exact term ranges. The remark's case analysis could be replaced by this one
sentence.

Tests ([`check_witness.py`](cutoff-recheck/check_witness.py)), with 2–3
variables, 1–3 bases and 1–4 power terms per base:
- *Single-use bases* (linear forms, `x_i x_j`, `x_i (x_j + 1)`), 300 cases:
  - the explicit witness lies in `Z0(C)` in 300/300 cases;
  - it is unchanged by every forward, backward and cutoff step in 300/300
    cases. In 13 cases this needed point sides widened by `1e-12`: they had
    emptied only through 1-ulp rounding, and every such case was checked;
  - the HC4 fixed point at `c = Phi_full(U')` keeps `U'` in 300/300 cases.
- *Bases that are not single-use* (`(x_i+x_j)(x_i-x_j)`, `x_i x_j + x_i`,
  `x_i - x_i^2`), 300 cases: the same, 300/300 in each check (32 widened).
- *The named representations* `linediag/s`, `rot1/st`, `line3/st`,
  `nondeg1/u` and `nondeg1s/centered`: `U'` was kept in 150/150 cases each.

## 4. Proposition 5.1a (two-sided localization)

Proof checked line by line:
- `min_{[0,delta]} phi_j <= phi_j(0) - delta phi_j'(0)^- + H_j delta^2/2` and
  `max - min <= delta |phi_j'(0)| + H_j delta^2` follow from Taylor's theorem
  with `|phi_j''| <= H_j` on `[0, delta]`, since `delta <= rho`.
- `sum_j phi_j'(0)^- - max_j |phi_j'(0)| = (D_i - d_i f)/2` is correct.
- The bound `K0 delta^2 <= delta D0'/4` uses `delta <= D0'/(4K0)`.
- `delta < 4(m+eps)/D0' < rho'` forces `delta = u_i - y_i`.
- The mirror segment gives `D_i + d_i f`.
- The two sides add to width below `8(m+eps)/D0'`.

The segments are boxes with degenerate sides, which Lemma 4.1 allows, and
they contain `y`. The statement is correct.

Tests ([`check_loc.py`](cutoff-recheck/check_loc.py)). The hypotheses were
verified per point, with `N = {y}`, `rho = 0.05`, `K0` sampled on the
segments, and only points with `m + eps < theta'` used. Two instances were
tested:
- `cnd1 = (s-1)^2 (s^2+1)` in monomial form. This is a 1D CND example, with
  term derivatives `4, -6, 4, -2` at `s = 1` and `D = 4`.
- Expanded `linediag`, on `t ∈ [0.2, 1.1]` of the line.

Results:
- *Random boxes:* 2,400 in total, with 668 and 241 removals of `y`. None had a
  face at or beyond `r = 4(m+eps)/D0'`. The largest ratio was 0.48.
- *Adversarial search:* all faces at `1e-4 r` except one, then bisection for
  the farthest removing face. The ratio is 0.481–0.500 over 60 faces (`cnd1`)
  and 0.495–0.499 over 32 faces (`linediag`).

The first-order witness predicts `2(m+eps)/(D_i ∓ d_i f)`, so the constant 4
cannot be improved beyond 2. The author's check reported a worst ratio of
0.37 from random sampling. That check also did not verify
`m + eps < theta'`, whereas this recheck does.

## 5. Round counts: Proposition 3.9, the restated criterion, Conjecture 3.11

### Proposition 3.9

Correct for the schedule stated.
- The one-round recursion `y' = y - (y^2+eps)/(2a)`,
  `x' = sqrt(a^2 + 2ax - eps) - a` matches the independent propagator to
  `4e-16` over 8 rounds.
- The squared inequality holds, and it holds trivially when `a + r < 0`.
- The nonemptiness conditions hold: `sigma' <= a + eps/(2a) <= tau'`, and
  `sigma^2 <= a^2 - eps` when `eps <= a^2`.
- The mean-value step `theta(z) - theta(z') <= 4 sqrt(eps)/a` holds, using
  `z' >= z/2` and the requirement `z <= a/4` at every round (the sequences are
  nonincreasing).

Test ([`check_rounds.py`](cutoff-recheck/check_rounds.py), part A): 84 runs,
with `a ∈ {0.5, 1, 2}`, four start boxes inside `a ± a/4` and
`eps = 1e-2..1e-8`. The bound holds in 84/84 runs, and the smallest ratio of
observed rounds to the bound is 8.00. On `[0.2, 2.2]` the observed
`rounds · sqrt(eps)` is 3.000, 3.130, 3.140, 3.141, tending to `pi`. A random
partial-step order needs `4.0–4.2/sqrt(eps)`.

### The restated criterion is contradicted

The revised Summary (lines 42–50) says that the round count is decided by
whether every term is strictly monotone at the minimizer. If some term is
stationary there, or the minimizer sits at the end of a lifted range, it
"needs a few rounds". Section 3.3 (lines 737–742) says the same "in the
examples". Section 11, item 1, says "all slow examples ... have nonzero
derivatives of every term there".

The note's own `st` representations refute this.
- In `rot_kappa`/`st` the term `kappa t^2`, with `t = x + y - 1`, has zero
  derivative at the minimizer `(1, 0)`. The minimizer is at the end `t^2 = 0`
  of its lifted range.
- The same holds for `(x_2 + x_3 - 1)^2` in `line3`/`st`.
- Yet Table 7.1 reports 55, 588, 5920 and 59234 rounds for `rot1`/`st`
  (`5.92 eps^(-1/2)`, the rate of `h_{1/2}`).

Independent reproduction (part B), rounds for `eps = 10^-2, 10^-4, 10^-6, 10^-8`:

| representation, box | stationary term at minimizer? | rounds |
|---|---|---|
| `s^2 - 2s + 1`, `[0.2, 2.2]` | no | 30, 313, 3140, 31414 |
| `t^2 - 2t^4` monomial | all terms | 4, 6, 6, 7 |
| `u - 2u^2`, `u = t^2` | lifted endpoint | 3, 4, 4, 4 |
| `x^2 - 2x + 1 + r^4`, `r = x - 1`, `[0.2, 2.2]` | yes (`r^4`, end of its range) | 30, 313, 3140, 31414 |
| `rot1`/`st`, root box | yes (`t^2`, end of its range) | 55, 588, 5920, 59234 |
| `rot1`/`st`, `[0.9,1.1] x [-0.1,0.1]` | yes | 49, 582, 5913, 59228 |
| `line3`/`st`, root box | yes | 55, 588, 5920, 59234 |

A stationary term that does not carry the cancellation changes nothing: the
fourth row is identical to the first. All the note's examples are consistent
with a per-base version, which is a heuristic and not proved here. Rounds grow
like `eps^(-1/2)` when some base has at least two terms whose nonzero
derivatives cancel at the minimizer (the situation of Remark 3.4). They stay
few when no base has such cancellation: all terms stationary (`t^2 - 2t^4`,
`nd2`), or the minimizer at a lifted endpoint where `f` grows linearly (`u`,
`centered`).

Places to correct:
- Summary, lines 42–50, and item 3 (lines 80–84: "only `O(log log(1/eps))`
  when the minimizer sits at the end of a lifted range" should be limited to
  the lifted form of `t^2 - 2t^4`);
- Section 3.3, opening paragraph;
- Section 7.2, "Exact representations" and "Bounded rounds";
- Section 11, item 1.

### Conjecture 3.11, restated

The hypothesis "one-sided at a nondegenerate optimal set at which every term
is strictly monotone, as in Examples 3.7(b)–(d)" excludes 3.7(d)
(`rot_kappa`/`st`, and `line3`, which the example discusses), because of the
stationary `t^2` term. The evidence list and Section 7.2 still cite `line3`/`st`
with `R = 10` as a case of the conjecture. Either restate the hypothesis per
base, as above, so that 3.7(d) and `line3` are covered, or drop them from the
examples and the evidence. The conjecture itself was not tested beyond this;
it is correctly labelled as a conjecture.

## 6. Requested corrections, in order of importance

1. **Round-count criterion** (Summary, Section 3.3, Conjecture 3.11,
   Sections 7.2 and 11): the criterion is contradicted by `rot_kappa`/`st`
   and `line3`/`st` in Table 7.1, and by `x^2 - 2x + 1 + (x-1)^4`. Restate it
   per base, as a heuristic, and align Conjecture 3.11's hypothesis with its
   examples.
2. **Lemma 2.1, constraint propagation**: drop "(and possibly propagation of
   the constraints)" from Section 2, or define `pi` on the graph including the
   constraints (Section 1, Gap A).
3. **Lemma 2.1, incumbents**: use the smallest cutoff along the inheritance
   chain, or state that `UBD` is nonincreasing and adjust "any ...
   incumbents" in Theorem 5.2 (Gap B).
4. Minor:
   - one sentence covering all start boxes in the Lemma 2.1(b) proof;
   - constant nodes in Lemma 1.2(d);
   - the single-use hypothesis of Lemma 4.1 and Remark 4.1a can be dropped
     (Section 3);
   - Proposition 5.1a is sharp to within a factor 2.

## 7. Checks run

All from `research-20260928b/reviews/cutoff-recheck/` with `OMP_NUM_THREADS=1`
and one process. These are targeted checks only. No project-wide checks were
run, CI was not inspected, nothing was committed, and the note was not edited.

- `python3 sanity.py > logs/sanity.log`: 10 representations equal `f` to
  `6e-14`; `pi_D` of the endpoint example (`-1`, `-0.01`, `-0.03`, `0.04`);
  the Proposition 3.9 recursion.
- `python3 check_merge.py > logs/check_merge.log` (6 s): Lemma 1.2(d); merged
  phases and inheritance; nonincreasing versus arbitrary incumbents; the
  constraint counterexample.
- `python3 check_hc4.py > logs/check_hc4.log` (4 min): schedule independence;
  Theorem 3.1(b) cross-check.
- `python3 check_witness.py > logs/check_witness.log` (1 s): Remark 4.1a and
  its generalization.
- `python3 check_loc.py > logs/check_loc.log` (2 s): Proposition 5.1a.
- `python3 check_rounds.py > logs/check_rounds.log` (7 s): Proposition 3.9
  and the round-count criterion.

## 8. Not checked

- Parts of the note outside the Section 11 revisions, except where a revision
  relies on them (Lemma 1.1, Lemma 1.2(a)–(c), Theorem 3.1).
- The author's regression runs and Table 7.1, apart from the `rot1`/`st`,
  `line3`/`st`, `nondeg1` and `(s-1)^2` round counts, which reproduce exactly.
- Conjecture 3.11 under bounded rounds; no branch-and-bound runs were made.
- The literature additions of Section 11, item 7.
