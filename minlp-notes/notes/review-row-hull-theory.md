# Independent review: theory of `results/row-hull-separable-concave.md`

Date: 2026-09-21. Reviewer: independent adversarial review agent. Scope: the
mathematical statements, their proofs, hypotheses and the literature
positioning. The computational claims were not reviewed. No existing file was
changed. Scripts are in `code/row_hull/review/`; they were written from the
statements in the note and do not import the author's code.

## Overall verdict

The core results (Proposition 1, Theorem 2, Theorem 2(b), the tilted flow cover
correspondence, Propositions 3–6) are correct. I found no counterexample to any
hull claim in 385 exact-versus-LP comparisons. There is **one wrong statement
as written** (Theorem 2(c) omits the bounds `0 <= z_i <= w y_i`, and they are
not implied), **one false universal claim** ("weaker otherwise" after
Proposition 3), and a list of missing conventions and hypotheses. The novelty
paragraph misses one source that must be checked before "to our knowledge new"
is kept (Kim, Tawarmalani, Richard 2022).

## (a) Verdict per statement

| Statement | Verdict |
|---|---|
| Setting and normalization | correct with fixes (E3, E4, E8) |
| Proposition 1 | correct. `Q` is a polyhedron, so no closure is needed (see G1) |
| Theorem 2, (RH) and (EF), `r = 0` case, `delta_i = 0` items | correct. State `0 <= k <= n-1` |
| Total unimodularity argument in Theorem 2 | correct |
| "Linear description", `O(n)` separation, interpretation | correct |
| Theorem 2(b), both senses | correct |
| Theorem 2(c) statement | **wrong as written**; correct after adding `0 <= z_i <= w y_i` (E1) |
| Theorem 2(c) proof (TU claim, elimination) | correct |
| Flow cover derivation after 2(c) | correct |
| "The same elimination with Theorem 2(b) handles `<=` rows" | correct (verified numerically), but it is an unproved remark; give the formula |
| Tilted flow cover correspondence (display, `(F, T_1, T_2)`, `|C| = k+1`) | correct; can be strengthened (E5) |
| "strict subfamily" | correct; a clean exact witness is given below |
| Proposition 3 | correct with fix (convention for `delta_i = 0`; E6). Hypothesis is necessary and sufficient |
| Lattice corollary | correct for `w_i >= g`; exclude `w_i = 0` (E7) |
| "is the hull for equal widths and is weaker otherwise" | **wrong as a universal claim** (E2) |
| Proposition 4 | correct, both directions |
| Proposition 5 | correct with fixes (`rho_i = sup`, infeasible LP; E8, E9). Interval merging argument correct, also with end-point jumps |
| Proposition 6 | every number verified; the objective is never stated (E10) |
| Shapley–Folkman paragraph | count "at most `m`" correct, also for degenerate solutions and inequality rows; the gap bound needs stated hypotheses (E11) |
| Novelty and Literature | overclaims in three places (section (d)) |

## (b) Errors, gaps and ambiguities, with corrections

### E1. Theorem 2(c) omits `0 <= z_i <= w y_i`, and the closed form does not imply it (error)

The theorem says `conv(X^y)` "is given by `y <= 1`, `tau >= 0`, the row and"
the min-inequality. With `n = 4`, `k = 1`, `w = 1`, `r = 1/2`, `delta_i = 1/4`:

```
z = (1/2, 1/2, 3/5, -1/10),  y = (1,1,1,1),  tau = (100,100,100,100)
```

satisfies the row (`sum z = 3/2`), `y <= 1`, `tau >= 0`, and the min-sum is
`1 + 1 + 4/5 - 1/5 = 13/5 >= 1`, but `z_4 < 0`, so the point is not in
`conv(X^y)`. The proof is fine: the extended form implies `z_i >= r zeta_i >= 0`
and `z_i <= w Y_i - (w-r) zeta_i <= w Y_i`; the loss happens when the existence
of `zeta` is rewritten as "sum of the `m_i` is at least one" without the
condition `m_i >= 0`. Theorem 2 handles this correctly by writing `z in X`.

*Correction.* "Then `conv(X^y)` is given by `0 <= z_i <= w y_i`, `y <= 1`,
`tau >= 0`, the row and ...". With that fix the statement passed all tests
(objective coefficients of `y` of both signs, so the claim "the indicator of an
unused arc is free" is also confirmed).

### E2. "The inequality is the hull for equal widths and is weaker otherwise" is false

Counterexample with unequal widths: `n = 2`, `w = (1, 2)`, `B = 3/2`,
`gamma_2(z) = z(2 - z)`. `X` is nondegenerate, its vertices are `(0, 3/2)` and
`(1, 1/2)`, item 1 is never interior, `a_2 = 1/2`, `b_2 = 3/2`,
`gamma_2(a_2) = gamma_2(b_2) = 3/4`. Proposition 3 gives `tau_2 >= 3/4` on `X`,
which is exactly `Q`.

*Correction.* "The inequality is the hull for equal widths and is in general
not the hull otherwise."

### E3. Hypotheses missing from the setting

- `X` must be nonempty: `0 <= B <= sum_i w_i`. For Theorem 2 this is
  `0 <= k <= n - 1`. (Theorem 2(b) stays correct for `k >= n`, where the
  inequality is void, but this is not said.)
- Items with `a_i = 0` are not part of the row set; items with `l_i = u_i`
  (`w_i = 0`) have no chord. Say that both are excluded (or carry `gamma = 0`)
  and that Theorem 2 needs `w > 0`.
- The formula for `B` after normalization is not given
  (`B = b - sum_{a_i>0} a_i l_i - sum_{a_i<0} a_i u_i`). Negative coefficients
  are otherwise handled correctly; Proposition 6 row 2 is a correct instance.
- `f_i(l_i) != 0` is harmless because only the chord gap is used. One sentence
  would prevent the question (Lim et al. assume `f_i(0) = 0`).

### E4. "lower semicontinuous" is redundant

A finite concave function on `[0, w_i]` is continuous inside and can only jump
*down* at an end point, which is lower semicontinuous automatically. Nothing in
the proofs uses semicontinuity: Proposition 1 only uses Jensen's inequality and
values at vertices. Replace by "concave and finite on the closed interval
(this allows a downward jump at an end point, as for a fixed charge)".

### E5. The tilted flow cover correspondence is stronger than stated

Lim et al. work with the row `sum x <= d`, not an equality. Their (17) at
`z = 1`, multiplied by `w / (r (w - r))`, is *identically* the selection
`(F, T_1 = N\C, T_2 = C\F)` of the **Theorem 2(b)** inequality
`sum_i m_i >= (sum_i z_i - k w)/r`; the row is not used. The note's route
("after using the equality row") is also correct. Suggest stating both,
because the `<=` version is the one that matches their set.

I re-derived the specialization independently. System (7) with
`(a_1,b_1,a_2,b_2,l,u) = (1, mu - u_i, 0, 0, 0, u_i)` and `f_i = c_i x +
gamma_i` gives `lambda^z = 0`, `lambda^x + c_i lambda^t = mu/u_i`,
`lambda^t = - mu m_i / (u_i gamma_i(m_i))`, `m_i = u_i - mu`. Substituting in
(17) with `N^- = C^- = {}` gives the display in the note for general `u_i`
(by hand), and the sympy script confirms the display and both identities for
equal capacities. Covers with `|C| >= k+2` have `mu >= w`, so `M^+` is empty and
nothing is tilted; hence `|C| = k + 1` is the only case. Their Theorem 6 needs
`N^- != {}` and does not add inequalities here.

A cleaner witness for strictness than "6 of 30 random trials": `n = 3`,
`k = 1`, `w = 1`, `r = 1/2`, `delta_i = 1/4`, objective `sum_i tau_i/delta_i`.
The hull value is `1`. The point `z = (1/2,1/2,1/2)`, `tau = 0` satisfies every
selection with `|F| + |T_2| = 2`, so the cover subfamily gives `0`. The missing
inequality is the selection `F = N`.

### E6. Proposition 3: convention for `delta_i = 0`

`delta_i = min{gamma_i(a_i), gamma_i(b_i)}` is zero only if `gamma_i = 0`
identically (a nonnegative concave function that vanishes at an interior point
vanishes everywhere), but then `tau_i/delta_i` is undefined. Add "the third
entry is omitted when `delta_i = 0`" as in Theorem 2.

The nondegeneracy hypothesis is both needed and enough. If a subset sum equals
`B`, the corresponding vertex has every `z_i in {0, w_i}` and `tau = 0`, so
every term of the sum is zero and the inequality fails. In 109 random
degenerate instances it failed every time; in 291 nondegenerate ones it never
failed. Leaving out never-interior items is correct and is the strongest
choice (their terms would be nonnegative). Concavity on `[a_i, b_i]` is used
correctly; since `0 < a_i` and `b_i < w_i`, an end-point jump of `gamma_i`
plays no role. It would help to say that `a_i, b_i` may be any valid bounds,
not only the exact extremes (the proof covers this).

### E7. Lattice corollary

Correct. An interior value is `B - w(S) = (q - s) g + r`, which is congruent to
`r` modulo `g`, lies in `(0, w_j)`, and therefore in `[r, w_j - g + r]`. For
`w_i = g` the interval is the single point `r`, which is fine (this is the
equal-width case). For `w_i = 0` the formula gives `b_i < 0`; such items are
never interior and must be left out. Nondegeneracy holds automatically and
could be stated. Verified on 300 random lattices.

### E8. `rho_i = max gamma_i` need not exist

For a fixed charge, `gamma_i(z) = c (1 - z/w)` for `z > 0` and `gamma_i(0) = 0`;
the supremum `c` is not attained. Write `rho_i = sup gamma_i` (also in the
Shapley–Folkman paragraph).

### E9. Proposition 5, membership program

"`(z^, tau^) in Q` iff the program has value zero" needs the convention that an
infeasible program does not have value zero: the program is infeasible for
`z^` outside `X`, and for `tau^_i < 0` when `rho_i = 0`. The validity proof of
the cut is correct. Degenerate vertices have several representations
`(S, j, r)`; all give the same `phi`, so the minimum over all `(S, j)` with
`r in [0, w_j]` is the right quantity.

The interval-merging argument is correct, including fixed-charge jumps: for any
concave `h` on `[p, q]`, `h(x) >= min{h(p), h(q)}` for `x in (p, q)`, with no
continuity needed. Two implementation conditions should be stated because the
argument depends on them: a merged interval must be *clipped* to `[0, w_j]`
(not discarded when it sticks out), and the clipped end point `0` or `w_j` must
be evaluated with the true value `gamma_j = 0`, not with the one-sided limit.
My own implementation of the scheme with these two rules never exceeded the
exact minimum in 300 random instances with `K` between 1 and 4.

"Separation is therefore NP-hard as well" relies on the polynomial equivalence
of optimization and separation; one clause would make this explicit.

### E10. Proposition 6 does not state the objective

"The relaxation bound is 0" and "the optimal value is 1/2" refer to
`min sum_i tau_i` (equivalently `min sum_i x_i(1 - x_i)`), which is never
written. All numbers are right: the rows give `x_3 = 1/2`, `x_1 + x_2 = 3/2`;
the feasible set is the segment between `(1,1/2,1/2)` and `(1/2,1,1/2)`; the
objective on it is `-2 x_1^2 + 3 x_1 - 1/2` with value `1/2` at both ends; row 2
normalizes to `z_1 + z_2 + z_3 = 2` with `z_3 = 1 - x_3`, so both rows have
`r = 0`; the aggregated rows have `w = 2`, `r = 1`, `delta = 1/4` and give
`tau_3 >= 1/4` and `tau_1 + tau_2 >= 1/4` (selection `F = {1,2}`), bound `1/2`.
The summary's wording "a positive gap everywhere" is unclear; say "the
intersection of the row hulls gives bound 0 while the optimum is 1/2".

### E11. Shapley–Folkman paragraph

The count is right in the generality claimed. A basic solution of the
relaxation in `(x, t)` needs `2n` independent active constraints among `m`
rows, `n` chord rows and the bounds of `x`; if `p` chord rows are inactive, at
least `n + p - m` variables `x_i` are at a bound, so at most `m - p <= m` are
interior. This covers degenerate bases (fewer interior variables) and
inequality rows (slack variables are basic variables, which only lowers the
count of interior `x_i`). `m` must count *all* rows other than bounds and chord
constraints.

The *gap* bound needs hypotheses the paragraph does not state: the concave
terms enter only the objective, with unit (or stated) weights; there are no
integrality constraints, so that the relaxation's `x` is feasible; and `rho_i`
is a supremum. If `t_i` appears in other constraints, `(x*, f(x*))` need not be
feasible and the bound fails.

### G1. Closedness of `Q`

No closure is needed, and the note could say so: by Proposition 1, `Q` is the
sum of a polytope and a polyhedral cone, hence a polyhedron, even when
`gamma_i` is discontinuous at an end point. The proof's "other inclusion is
clear" is true: each `(v, gamma(v)) + d` with `d >= 0` is in the set, and their
convex hull is the right-hand side.

### G2. "`Q` is a valid relaxation of any model that contains the row ..."

Accurate for `t_i >= f_i(x_i)` and `t_i = f_i(x_i)`, for any subset of terms
(missing terms are items with `gamma = 0`), and with relaxed integer variables.
It is not accurate, and should not be read as applying, when the model contains
`t_i <= f_i(x_i)` only. For a term that the model uses only through
`t_i >= f_i`, nothing is lost; for equality terms the cuts are valid but the
hull of the graph is smaller than `Q` (Dey–Kocuk's two-sided setting). The note
says this in the Literature section; it belongs next to the claim.

### G3. Summary sentence "at most one term can be away from its chord ... and that one must be"

True only when `X` is nondegenerate (`r != 0` in the equal-width case) and
`gamma_j(r) > 0`. The summary states it without a condition.

## (c) What the scripts checked

All commands were run from `code/row_hull/review/`, single-threaded, with
`PY="uv run --project /workspace/minlp-notes/code/minlp_solver_lab python"`.

1. `OMP_NUM_THREADS=1 nice -n 10 $PY check_theorem2.py` (21 s).
   Generators come from brute-force enumeration of the row polytope written
   from its definition (not from the theorem's list of vertices). For each
   instance the support function `min c.z (+ d.y) + omega.tau`, `omega >= 0`,
   is computed exactly (fractions) over the generators and by a HiGHS LP over
   the claimed description: the extended form for all `n`, and the closed form
   as all `3^n` selections for `n <= 4`. The closed form is also evaluated
   exactly at every generator. Instances: `n = 2..6`; `k in {0, 1, n//2, n-1}`;
   `r/w in {1/1000, 1/3, 1/2, 7/10, 999/1000}`; rational `w`; items with
   `delta_i = 0` and all `delta = 0`; senses `=`, `<=`, `>=` (Theorem 2, 2(b));
   indicators with `=` and `<=` for `n <= 5` (Theorem 2(c) and the closing
   remark). 12 directions per instance: random, with many zero components,
   pure `tau` directions with 0/1 weights, pure `z` directions, and `y` costs of
   both signs. Outcome: `instances checked: 385; all support functions agree;
   worst abs LP-vs-exact difference 1.35e-13`. The script also prints the exact
   E1 counterexample to the literal statement of Theorem 2(c).
   Limitation: the LP side is floating point (tolerance `1e-7` relative); the
   vertex side is exact.
2. `OMP_NUM_THREADS=1 nice -n 10 $PY check_props.py` (4 s), exact arithmetic
   except two small LPs.
   - Proposition 3 with unequal integer widths and half-integer `B`, gap
     functions quadratic, tent, fixed-charge (jump) and zero:
     `{'nondeg_ok': 291, 'nondeg_bad': 0, 'deg_ok': 0, 'deg_bad': 109}`.
   - Lattice corollary, 300 instances: 0 vertex values outside
     `[r, w_i - g + r]`.
   - E2 counterexample printed.
   - Proposition 4, 300 instances: 0 mismatches between "min = 0" and
     "a subset sums to `B`".
   - Proposition 5 interval merging (my implementation, `K` in 1..4, jumps
     included): bound exceeded the exact minimum in 0 of 300 instances.
   - Proposition 6: rows imply `x_3 = 1/2`, `x_2 = 3/2 - x_1`; objective on the
     segment `-2 x1^2 + 3 x1 - 1/2`, end values `1/2`, `1/2`; bound with
     aggregated row hulls `0.5`; bound with original row hulls `0.0`.
   - Shapley–Folkman count on 60 random LPs with mixed `=`/`<=` rows (dual
     simplex): interior variables never exceeded `m`.
3. `OMP_NUM_THREADS=1 nice -n 10 $PY check_lll.py` (2 s). Sympy, `n = 5`,
   `k = 2`, `C = {0,1,2}`, `F = {0,1}`, symbolic `w, r, x, tau, gamma_i(m_i)`,
   chord slopes: solves system (7), builds (17) at `z = 1`; differences
   "(17) minus the note's display", "2(b) selection minus `w/(r(w-r))` (17)"
   and "Theorem 2 selection minus `w/(r(w-r))` (17) on the row" are all `0`.
   The symbolic check uses equal capacities; the general-capacity display was
   checked by hand only. Part 2 prints the strictness witness of E5:
   `exact over vertices 1 | all selections 1.0 | cover subfamily only 0.0`.

Not checked: the author's test file, the separation code, all computational
claims, and the correspondence against Lim et al.'s code (the note says the
same).

## (d) Overclaiming and unclear wording

1. **"Closed form for equal widths (Theorem 2, to our knowledge new)".** The
   Literature section does not mention Kim, Tawarmalani and Richard,
   *Convexification of permutation-invariant sets and an application to sparse
   PCA*, Math. Oper. Res. 47 (2022), arXiv 1910.02573. They convexify
   permutation-invariant sets and envelopes of permutation-invariant functions
   over hypercubes with congruent bounds. With equal widths and identical
   `gamma_i`, the set behind `Q` is permutation-invariant, so their machinery
   may already give Theorem 2 for that case. Item-dependent `gamma_i` break the
   invariance, so the general statement probably remains outside their scope,
   but I did not read the paper and this must be checked before the claim is
   kept. Also worth checking: Tawarmalani, Richard and Chung (2010) on
   orthogonal disjunctions (the case `k = 0` is an orthogonal disjunction, and
   (RH) then reduces to the classical simplex envelope `tau_i >= delta_i z_i/r`),
   and Tawarmalani, Richard, Xiong (2013) on envelopes via polyhedral
   subdivisions.
2. **"No complete description" for Lim et al.** Their Theorems 2–3 are complete
   descriptions of the single-term sets. Say "no complete description of the
   flow set".
3. **"and the remaining facets of the constant-capacity equality set"** (after
   2(c)) is a consequence of the theorem, not an independent finding, and
   (RH) selections include many non-facets; "contains all facets" is accurate,
   "the remaining facets" suggests a classification that the note does not give.
4. **"the root relaxation is exact, while every spatial branch-and-bound ...
   needs `2^Omega(n)` nodes"**: correct for the family as defined in the
   lower-bound note (`sum x_i = k + 1/2`), but the comparison should say that
   the lower bound is for term-wise relaxations with branching only.
5. **"For one row the row hull closes it completely"**: true as a statement
   about `Q`, but for general widths `Q` is NP-hard to separate (Proposition 4),
   and the closed form of Proposition 3 does not close it. The sentence reads
   as a computational claim.
6. **Summary numbers** (60–90%, 300 s to 10–60 s) are stated as results, while
   the section "Computational results" says "Summary to be completed from the
   final tables". Either fill in the section or mark the summary numbers as
   preliminary.
7. **Moré and Vavasis (1991)** do state NP-hardness of the concave knapsack
   problem in the paper named (confirmed from the abstract); the attribution is
   acceptable. Dey–Kocuk Proposition 1 is indeed a subset-sum reduction with
   `min sum (x_j - y_j)`; it is stated for `kappa > 1`.
8. The status line still says "Independent review: pending".

Sources for (d): [Kim, Tawarmalani, Richard, arXiv 1910.02573](https://arxiv.org/abs/1910.02573);
[Math. Oper. Res. version](https://pubsonline.informs.org/doi/10.1287/moor.2021.1219);
[Moré and Vavasis 1991](https://link.springer.com/content/pdf/10.1007/BF01588800.pdf).
