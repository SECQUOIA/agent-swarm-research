# The pooling problem is complete for the existential theory of the reals

Date: 2026-09-05. Status: two independent proof audits passed with
corrections, all applied (see the status line at the end).

**Theorem 1.** The threshold decision version of the Pooling Problem
(Haugland's 2016 model, defined in Section 1) is complete for the
existential theory of the reals, `∃R`. Hardness holds under all of the
following restrictions:

- one quality attribute, with every source quality in `{0,1}`;
- lower and upper quality bounds at terminals (equivalently, two attributes
  with qualities in `{0,1}` and only upper bounds, see Section 6, item 1);
- no source–terminal arcs; every pool has in-degree at most two, every
  terminal in-degree at most two, every source out-degree at most two, and
  every unforced pool out-degree one;
- all flow lower bounds are zero; all node capacities are rational with
  numerators and denominators polynomially bounded in the instance size;
- arc costs lie in `{0,-1,-2}` and the profit threshold is rational.

**Corollary 2.** Unless `NP = ∃R`, the Pooling Problem is not in `NP`.
Since `∃R ⊆ PSPACE`, it is in `PSPACE`.

**Corollary 3 (algebraic degree).** For every irrational real algebraic
number `α` there is a pooling instance with rational data and rational
threshold that has exactly one threshold-feasible flow, and one designated
arc of that flow carries the value `(α - b)/a` for rationals `a ≠ 0`, `b`
fixed by the instance; this value has the same algebraic degree as `α`.
Moreover, that flow has all values in `Q(α)`, and no threshold-feasible flow
of the instance has all its values in a subfield of `R` not containing `α`.
In particular, pooling instances with rational data can have only irrational
optimal solutions, with flow values of arbitrarily high algebraic degree.

The membership statement is routine. The contribution is the hardness
reduction, which encodes the `∃R`-complete problem ETR-INV of Abrahamsen,
Adamaszek, and Miltzow into flow-conservation, capacity, and blending
constraints of a standard pooling network. To our knowledge, no `∃R`-hardness
result for the pooling problem, or for any structured blending network, has
been published; see Section 6.

## 1. Model and decision problem

We use the Pooling Problem exactly as defined by Haugland (2016, Section 2.1),
with the lower quality bounds that he explicitly includes.

A directed graph `D=(S,P,T,A)` has sources `S`, pools `P`, terminals `T`, and
arcs `A ⊆ (S×P) ∪ (P×T)`. Data: node capacities `b ∈ Q_+^{S∪P∪T}`, arc costs
`c ∈ Q^A`, one quality attribute with source qualities `q_s ∈ Q`, and
terminal quality bounds `ℓ_t ≤ u_t`. A flow `x ∈ R_+^A` must satisfy

```
sum_{p} x_{sp} ≤ b_s              (s ∈ S)
sum_{s} x_{sp} = sum_{t} x_{pt} ≤ b_p   (p ∈ P)
sum_{p} x_{pt} ≤ b_t              (t ∈ T).
```

Write `X_p = sum_t x_{pt}` for the throughput of pool `p`. A quality vector
`w ∈ R^P` is a quality vector of `x` if `w_p X_p = sum_s q_s x_{sp}` for every
pool `p`; when `X_p > 0` this determines `w_p` as the flow-weighted average of
incoming source qualities, and when `X_p = 0` the value `w_p` is arbitrary.
The flow is feasible if for some quality vector `w` and every terminal `t`

```
ℓ_t sum_p x_{pt} ≤ sum_p w_p x_{pt} ≤ u_t sum_p x_{pt}.
```

The profit of `x` is `-sum_a c_a x_a`. The decision problem POOL asks, given
rational data and a rational threshold `ζ`, whether a feasible flow with
profit at least `ζ` exists.

Two conventions are worth recording. First, the quality constraint at a
terminal is proportional to its actual inflow, not to its capacity. Second, a
pool with zero throughput has an unconstrained quality, but that quality only
multiplies zero flows, so it never affects feasibility.

## 2. The existential theory of the reals and ETR-INV

`∃R` is the class of decision problems that reduce in polynomial time to the
problem ETR of deciding whether an existentially quantified Boolean
combination of polynomial equations and inequalities with integer
coefficients has a real solution. It satisfies `NP ⊆ ∃R ⊆ PSPACE` (the
upper bound is Canny's).

**Definition (ETR-INV; Abrahamsen, Adamaszek, Miltzow 2018, Definition 5).**
An instance consists of real variables `x_1,…,x_n` and a set of equations,
each of one of the forms `x = 1`, `x + y = z`, `x·y = 1` with
`x,y,z ∈ {x_1,…,x_n}`. The question is whether the system has a solution
with every variable in `[1/2, 2]`.

**Theorem (Abrahamsen, Adamaszek, Miltzow 2018, Theorem 7).** ETR-INV is
`∃R`-complete.

For the reduction below we first replace every equation `x = 1` by
`x·x = 1`: within `[1/2,2]` the two are equivalent. So we may assume that
every equation is an addition `x + y = z` or an inversion `x·y = 1` (with
`x = y` allowed). Let `m` be the number of equations and write `Φ` for the
instance and `V(Φ) ⊆ [1/2,2]^n` for its solution set.

## 3. Membership in ∃R

Given a POOL instance, introduce real variables `x_a` (`a ∈ A`) and `w_p`
(`p ∈ P`). The conjunction of `x_a ≥ 0`, the capacity and conservation
constraints, the equations `w_p X_p = sum_s q_s x_{sp}`, the terminal
inequalities `ℓ_t X_t ≤ sum_p w_p x_{pt} ≤ u_t X_t` with `X_t = sum_p x_{pt}`,
and `-sum_a c_a x_a ≥ ζ` is a polynomial system of degree two whose size is
polynomial in the input. It has a real solution if and only if the POOL
instance is a yes-instance, because the equations for `w` are exactly the
definition of a quality vector, including the free value at pools with zero
throughput. Hence POOL is in `∃R`.

## 4. The reduction

Fix an ETR-INV instance `Φ` in the normalized form of Section 2. All arcs
carry cost `0` unless stated otherwise; costs are fixed globally in
Section 4.1. Every node created below is one of the following kinds.

- A **forced** node is a source, pool, or terminal whose capacity we intend
  to be attained exactly. The sets of forced sources, pools, and terminals
  are `S_F`, `P_F`, `T_F`.
- A **diluent source** is a source of quality `0` with capacity `B` (defined
  below), unforced, with a single outgoing arc.
- A **slack terminal** is an unforced terminal with capacity `B` and vacuous
  bounds `ℓ = 0`, `u = 1`, with a single incoming arc.
- A **vacuous** terminal has bounds `ℓ = 0`, `u = 1`.

Let `M` be the largest number of arcs from any single forced pool to
terminals other than its slack terminal, in the construction below. Such
arcs are the emission arcs of 4.3, the arcs `(P_x,t)` of the inversion
gadgets (4.5), and the arcs `(R̄_z,t)` of the addition gadgets (4.6). A
variable occurring in all `m` equations gives at most `2m` such arcs at
`R_v` (two per addition `v + v = z`), at most `m + 1` at `P_v`, at most `m`
at `R̄_v`, and one at `P̄_v`; hence `M ≤ 2m + 1`. Set

```
B := 2M + 3.
```

### 4.1 Forcing by the objective

Every arc `a = (u,v)` gets cost `c_a := -(number of forced groups containing a)`,
where the forced groups are: the set of arcs leaving a forced source, the set
of arcs leaving a forced pool, and the set of arcs entering a forced
terminal. An arc has two endpoints, so it lies in at most two groups and
`c_a ∈ {0,-1,-2}`. Put

```
ζ := sum_{s ∈ S_F} b_s + sum_{p ∈ P_F} b_p + sum_{t ∈ T_F} b_t.
```

**Lemma 4 (forcing).** For every flow `x` satisfying the capacity and
conservation constraints, the profit is
`sum_{s∈S_F} out(s) + sum_{p∈P_F} X_p + sum_{t∈T_F} in(t) ≤ ζ`, with
equality if and only if every forced source, pool, and terminal attains its
capacity.

*Proof.* The profit `-sum_a c_a x_a` counts each arc once per forced group
containing it, so it equals the displayed sum of group totals. Each group
total is bounded by the corresponding node capacity, so the profit is at most
`ζ`, with equality exactly when all bounds are tight. ∎

Consequently, a flow has profit at least `ζ` if and only if it is feasible
and every forced node is saturated. In the rest of the proof "saturated"
refers to this situation.

### 4.2 Variable gadget

For each variable `v` of `Φ` create a forced source `s_v` of quality `1` and
capacity `5/2`, and two forced pools `P_v` and `P̄_v` of capacity `B`, with
arcs `(s_v,P_v)` and `(s_v,P̄_v)`. Attach to each of `P_v`, `P̄_v` its own
diluent source and its own slack terminal.

In a saturated flow write `v := x_{s_v P_v}`; then `x_{s_v P̄_v} = 5/2 - v`.
Because `P_v` has throughput `B > 5/2`, its diluent inflow is `B - v ≥ 0`
and its quality is `w_{P_v} = v/B`; likewise `w_{P̄_v} = (5/2 - v)/B`.

### 4.3 Emission terminals and relays

An **emission** from a forced pool `Q` is the following structure: a forced
terminal `t` of capacity `2` with bounds `ℓ_t = u_t = 1/(2B)`, an arc
`(Q,t)`, a **relay pool** `p'` of capacity `2` with the single outgoing arc
`(p',t)`, and a forced **relay source** `s'` of quality `0` and capacity `2`
with the arc `(s',p')` and one further arc `(s',·)` whose head is specified by
the gadget that uses the emission. We say that `s'` **delivers** the emitted
value at quality `0`.

**Lemma 5 (emission).** Let `Q` be a forced pool whose incoming arcs are one
arc of quality `1` carrying flow `a` and one diluent arc. In every saturated
flow, the emission structure satisfies `a > 0`, `x_{Qt} = 1/a ≤ 2`, and the
delivering arc `(s',·)` carries flow `1/a`. Conversely, whenever
`a ∈ [1/2, 2]`, setting `x_{Qt} = 1/a`, `x_{p't} = x_{s'p'} = 2 - 1/a`, and
the delivering arc to `1/a` satisfies all constraints of the structure.

*Proof.* `Q` is saturated, so `X_Q = B > 0` and `w_Q = a/B`. The terminal
`t` is saturated with inflow `2`, so its quality constraint reads
`w_Q x_{Qt} + w_{p'} x_{p't} = 1/B`. The pool `p'` receives flow only from the
quality-`0` source `s'`, so either `x_{p't} = 0` or `w_{p'} = 0`; in both
cases `w_{p'} x_{p't} = 0`. Hence `a x_{Qt} = 1`, which forces `a > 0` and
`x_{Qt} = 1/a`; the capacity `2` of `t` gives `1/a ≤ 2`. Since the inflow of
`t` is exactly `2`, `x_{p't} = 2 - 1/a`, and because `p'` has one incoming
and one outgoing arc, `x_{s'p'} = 2 - 1/a`. The source `s'` is saturated at
`2` with exactly two arcs, so its other arc carries `1/a`. The converse
statement is a direct check: all flows are nonnegative because
`1/a ∈ [1/2,2]`, the terminal and source totals are exactly `2`, the relay
pool throughput `2 - 1/a ≤ 2` respects its capacity, and the quality
constraint at `t` holds with equality. ∎

A **quality flip** converts a delivered quality-`0` arc into a delivered
quality-`1` arc: route the delivering arc `(s',p_2)` into a pool `p_2` of
capacity `2` with the single outgoing arc `(p_2,t_2)` to a forced vacuous
terminal `t_2` of capacity `2`; add a pool `p_3` of capacity `2` with the
single arc `(p_3,t_2)`, fed by a forced source `s_3` of quality `1` and
capacity `2`, which has one further arc `(s_3,·)`. In a saturated flow
`x_{p_2 t_2} = x_{s' p_2}`, `x_{p_3 t_2} = 2 - x_{s' p_2}`, and the free arc of
`s_3` carries `x_{s'p_2}` again; the converse construction is immediate. The
quality of `p_2` and `p_3` is irrelevant because `t_2` is vacuous.

### 4.4 Inverse pools

For each variable `v` create forced pools `R_v` and `R̄_v` of capacity `B`,
each with its own diluent source and slack terminal. Take one emission from
`P_v`, apply a quality flip, and let its final delivering arc enter `R_v`.
Do the same from `P̄_v` into `R̄_v`.

In a saturated flow, Lemma 5 and the flip give: the quality-`1` inflow of
`R_v` is `1/v`, so `w_{R_v} = 1/(vB)`, and every emission from `R_v` carries
`x_{R_v t} = v` (apply Lemma 5 with `a = 1/v`). Likewise `R̄_v` has quality
`1/((5/2 - v)B)` and every emission from `R̄_v` carries `5/2 - v`. The
emissions used to feed `R_v` and `R̄_v` also enforce the range: Lemma 5 gives
`1/v ≤ 2` and `1/(5/2 - v) ≤ 2`, that is, `1/2 ≤ v ≤ 2`.

The diluent of `R_v` is `B - 1/v ≥ 0` because `B ≥ 5`.

### 4.5 Inversion gadget for `x·y = 1`

Create an emission from `R̄_y`, whose relay source delivers the value
`5/2 - y` at quality `0` into a pool `p_c` of capacity `5/2` with the single
outgoing arc `(p_c,t)`, where `t` is a new forced terminal of capacity `5/2`
with bounds `ℓ_t = u_t = 2/(5B)`. Add the arc `(P_x,t)`.

In a saturated flow: `x_{p_c t} = 5/2 - y` by Lemma 5 and the single-arc
relay pool; the inflow of `t` is `5/2`, so `x_{P_x t} = y`. The quality
constraint at `t` is `w_{P_x} y + w_{p_c}(5/2 - y) = (2/(5B))(5/2) = 1/B`.
As in Lemma 5 the second term vanishes, so `(x/B) y = 1/B`, that is,
`x·y = 1`. Conversely, if `x·y = 1` with `x,y ∈ [1/2,2]`, the assignment
`x_{P_x t} = y`, `x_{p_c t} = 5/2 - y` and the emission flows of Lemma 5
satisfy every constraint of the gadget. When `x = y` the gadget uses `R̄_x`
and `P_x` of the same variable; nothing changes.

### 4.6 Addition gadget for `x + y = z`

Create one emission from `R_x` and one from `R_y`; their relay sources deliver
`x` and `y` at quality `0` into a new pool `p_+` of capacity `4` with the
single outgoing arc `(p_+,t)`, where `t` is a new forced terminal of capacity
`5/2` with bounds `ℓ_t = u_t = 2/(5B)`. Add the arc `(R̄_z,t)`.

In a saturated flow: `p_+` receives `x + y ≥ 1` from quality-`0` sources
only, so `w_{p_+} = 0` and `x_{p_+ t} = x + y`. Since `t` is saturated,
`x_{R̄_z t} = 5/2 - x - y`. The quality constraint at `t` reads
`w_{R̄_z} x_{R̄_z t} = 1/B` with `w_{R̄_z} = 1/((5/2 - z)B)`, hence
`x_{R̄_z t} = 5/2 - z` and therefore `x + y = z`. Conversely, if
`x + y = z` with all three in `[1/2,2]`, then `x_{p_+ t} = x + y ≤ 4`,
`x_{R̄_z t} = 5/2 - z ∈ [1/2, 2]`, and the emission flows satisfy every
constraint. (Here the pool `p_+` plays the role of the diluent of an
emission from `R̄_z`; the arc `(R̄_z,t)` is counted as an emission of `R̄_z`
for the purpose of defining `M`.)

### 4.7 Slack and capacity bookkeeping

Every forced pool `Q ∈ {P_v, P̄_v, R_v, R̄_v}` has one quality-`1` inflow
`a ∈ [1/2,2]`, one diluent inflow `B - a ≥ 0` (within the diluent capacity
`B`), at most `M` arcs to non-slack terminals each carrying at most `2`
(emitted values, `y ≤ 2` on inversion arcs, `5/2 - z ≤ 2` on addition
arcs), and one slack arc. In the intended flow the slack arc carries
`B - (sum of those arc flows) ≥ B - 2M = 3 > 0`, within the slack capacity
`B`. Every forced pool is thus
saturated at `B`, and every emission terminal, relay source, flip terminal
and flip source is saturated at `2`; every variable source is saturated at
`5/2`; every inversion and addition terminal is saturated at `5/2`.

The pools `R_v` and `R̄_v` and the emissions feeding them are created for
every variable, whether or not a gadget uses them (Section 4.4), so the
range `[1/2,2]` is enforced for every variable.

### 4.8 Correctness

**Lemma 6.** `Φ` has a solution in `[1/2,2]^n` if and only if the
constructed POOL instance has a feasible flow with profit at least `ζ`.

*Proof.* (⇐) Let `x` be feasible with profit at least `ζ`. By Lemma 4 every
forced node is saturated. Define `v := x_{s_v P_v}` for each variable. Section
4.4 shows `v ∈ [1/2,2]`. Section 4.5 shows `x·y = 1` for every inversion
equation, and Section 4.6 shows `x + y = z` for every addition equation.
Hence `(v)_v ∈ V(Φ)`.

The (⇐) argument also shows that every arc flow of a saturated feasible
flow is a fixed rational function of `(v)_v` (relay, flip, emission, gadget,
diluent, and slack flows were each derived from `v` and constants), so
distinct saturated flows induce distinct points of `V(Φ)`.

(⇒) Let `(v)_v ∈ V(Φ)`. Assign `x_{s_v P_v} = v`, `x_{s_v P̄_v} = 5/2 - v`,
diluent inflows `B - a` at every forced pool with quality-`1` inflow `a`,
emission flows as in Lemma 5 (values `1/v`, `1/(5/2 - v)`, `v`, `5/2 - v`
respectively for `P_v`, `P̄_v`, `R_v`, `R̄_v`), flip flows as in Section 4.3,
gadget flows as in Sections 4.5 and 4.6, and slack flows as in Section 4.7.
Every quality-`1` inflow lies in `[1/2,2]`, every emitted value lies in
`[1/2,2]`, and every constraint was checked in the respective section. All
forced nodes are saturated, so the profit equals `ζ` by Lemma 4. ∎

### 4.9 Size and numbers

The instance has `O(n + m)` nodes and arcs, since each variable contributes a
constant number of nodes and each equation a constant number of emissions
and gadget nodes. Capacities lie in `{2, 5/2, 4, B}` with `B = 2M + 3 ≤ 4m + 5`;
bounds lie in `{0, 1, 1/(2B), 2/(5B)}`; qualities in `{0,1}`; costs in
`{0,-1,-2}`; and `ζ` is a sum of capacities. Every pool has in-degree at
most two (forced pools: one quality-`1` arc and one diluent arc; `p_+`: two
quality-`0` arcs; relay and flip pools: one arc). The construction is
computable in linear time. Together with Section 3 and the
`∃R`-completeness of ETR-INV, this proves Theorem 1. ∎

## 5. Proofs of the corollaries

*Corollary 2.* If POOL were in `NP`, then ETR-INV, which reduces to POOL in
polynomial time, would be in `NP`, and every problem in `∃R` would reduce to
it, giving `∃R ⊆ NP`. The upper bound is `∃R ⊆ PSPACE`. ∎

*Corollary 3.* Let `p ∈ Z[x]` be a nonzero polynomial with `p(α) = 0` and
let `[c,d]` be a rational interval in which `α` is the only root of `p`. The
ETR instance `Φ_α := {p(x) = 0, c ≤ x ≤ d}` has the compact solution set
`V(Φ_α) = {α}`. By Abrahamsen and Miltzow (2019, Theorem 1) there is an
ETR-INV instance `Ψ` such that `V(Ψ)` is rationally equivalent to `V(Φ_α)`
and is a linear extension of it: there are a coordinate projection `π` and
rationals `a`, `b` such that `x ↦ a·π(x) + b` is a bijection from `V(Ψ)`
onto `{α}`. Since `α` is irrational, `a ≠ 0` (otherwise `α = b ∈ Q`). Hence
`V(Ψ)` is a single point `x*` with `π(x*) = (α - b)/a`, and by rational
equivalence `x* ∈ Q(α)^n`. (Their Corollary 2 states the field
consequence.) Apply the reduction to `Ψ`. By Lemma 6 and its proof,
threshold-feasible flows correspond bijectively to points of `V(Ψ)`: every
flow value is a fixed rational function of the ETR-INV solution (`v`,
`5/2 - v`, `1/v`, `1/(5/2 - v)`, `2` or `B` minus such a value, `x + y`, or
a constant), and conversely the solution is read off as `v = x_{s_v P_v}`.
So the instance has exactly one threshold-feasible flow, its values lie in
`Q(α)`, and the arc `(s_{π}, P_{π})` of the projected variable carries
`(α - b)/a`, which has the same degree as `α`. Finally, any threshold-feasible
flow yields a point of `V(Ψ)` inside the field generated by the flow values,
and that field contains `α` because `a·π(x*) + b = α`. ∎

For a concrete example, the instance encoding `x + x = y`, `x·y = 1` has the
unique solution `x = 1/√2`, `y = √2`, and every threshold-feasible flow of the
corresponding pooling instance carries these irrational values (verified
numerically below).

## 6. Remarks, scope, and relation to prior work

1. **Upper bounds only.** Haugland (2016, Section 2.1) notes that
   a lower bound on an attribute is an upper bound on a negated attribute.
   With nonnegative data: add an attribute `k'` with source qualities
   `q'_s = 1 - q_s ∈ {0,1}` and terminal upper bounds `u'_t = 1 - ℓ_t`. For
   pools with positive throughput `w'_p = 1 - w_p`, and pools with zero
   throughput contribute nothing at terminals, so the new upper bound is
   equivalent to the old lower bound. Hence Theorem 1 also holds for the
   pooling problem with two attributes, qualities in `{0,1}`, and upper
   quality bounds only, which is the form used by Alfaki and Haugland (2013).
   Whether one attribute with upper bounds only suffices is not settled here.
2. **Models with direct source–terminal arcs** (bypasses), generalized pooling
   with pool–pool arcs, and formulations with flow lower bounds all contain
   the instances above as special cases, so hardness transfers to them. The
   objective is only used to force saturation of some nodes; with explicit
   lower bounds on node throughputs (source supply, pool throughput, and
   terminal demand) equal to the corresponding capacities at forced nodes,
   the same reduction gives `∃R`-completeness of the pure feasibility
   question with no objective.
3. **What the theorem does not say.** It does not concern approximation,
   fixed-parameter cases, or numerical tolerances: an `ε`-feasible,
   `ε`-optimal rational approximation has encoding length polynomial in the
   instance size and `log(1/ε)` for bounded rational instances with a feasible
   optimum, when all polynomial constraints may also be violated by `ε`.
   This follows by rounding an optimal flow and bounded pool qualities; it
   does not promise an exactly feasible rational flow. The theorem concerns
   exact decision with rational data. The repository's
   NP-membership statements for fixed-parameter subclasses (for example,
   `results/fixed-parameter-linear-fibers-np-membership.md`) are consistent
   with it and are now seen to be genuinely restricted: a general NP
   certificate would imply `NP = ∃R`.
4. **Prior work.** Strong NP-hardness of pooling is due to Alfaki and Haugland
   (2013) and Haugland (2016); no NP-membership statement for the general
   problem appears in that literature, and the compendium of `∃R`-complete
   problems (Schaefer, Cardinal, Miltzow 2024) contains no entry for pooling,
   blending, bilinear network flow, or quadratically constrained programming
   with network structure. The `∃R`-completeness of unstructured quadratic
   feasibility on a compact domain is classical (Schaefer 2013, Lemma 3.9,
   for the unit ball; Schaefer and Štefankovič 2017), and Poss, Kurtz,
   Goerigk, and Henke (arXiv:2608.21574, Theorem 4) state explicitly that
   quadratically constrained programming over a rational polyhedron, with
   or without a box, is `∃R`-complete. The contribution here is the encoding
   into the specific flow-times-proportion structure of pooling with
   constant-quality sources and a single attribute. Irrational optimal
   pooling solutions of degree two are implicit in an example of Haugland
   and Hendrix (2015); no arbitrary-algebraic-degree pooling counterpart to Corollary 3 was found
   in the literature search.
   Bienstock and Verma (2019, Section 1.3) raise the analogous NP-membership
   question for AC power flow feasibility; no `∃R` result for that problem
   is known to us. The nearest structured-bilinear analogues are the
   irrationality and `∃R`-completeness results for nonnegative matrix
   factorization (Chistikov, Kiefer, Marušić, Shirmohammadi, Worrell 2017;
   Shitov 2016). See `notes/pooling-existential-reals-novelty.md`.
5. **Bounded data and degrees (Theorem 1′).** Hardness in Theorem 1 also
   holds with every capacity in `{2, 5/2, 4, 7}`, every quality bound in
   `{0, 1, 1/14, 2/35}`, every node of in-degree at most two and out-degree
   at most three, and the threshold `ζ` equal to the sum of forced
   capacities; that is, with all numerical data except the threshold from a fixed finite
   set, in analogy with strong NP-hardness. Proof: replace the fan-out at forced
   pools by chains. For each variable `v` build the alternating chain
   `P_v → R_v → P_v^{(2)} → R_v^{(2)} → …`, where each link is an emission
   (Lemma 5) followed by a quality flip feeding the next forced pool, so the
   pools alternately have quality `v/B` and `1/(vB)`; and likewise
   `P̄_v → R̄_v → P̄_v^{(2)} → …` with qualities `(5/2 - v)/B` and
   `1/((5/2 - v)B)`; every chain pool has its own diluent source and slack
   terminal. Each pool of a chain has one arc to the next link and at most
   one gadget arc, so `M ≤ 2`, and we fix `B := 7` for every instance
   (Section 4 only needs `B ≥ 2M + 3`); each gadget occurrence takes the
   next free pool of the required kind, advancing the chain when necessary,
   which terminates within two links because the kinds alternate. The proofs of Lemmas 5–6 apply
   verbatim to every pool of a chain, since each has exactly one quality-`1`
   inflow with value `v`, `1/v`, `5/2 - v`, or `1/(5/2 - v)` and one diluent
   inflow; the range `[1/2,2]` is enforced because every chain is advanced
   at least once (each `P_v` and `P̄_v` emits). A variable with `k`
   occurrences needs at most `2k + 3` links of constant size, so the
   instance has `O(n + m)` nodes. Only the threshold `ζ`, a sum of
   capacities, grows with the instance; with node-throughput lower bounds
   (item 2) the objective and `ζ` disappear and every number is from the
   fixed set. This variant is implemented in
   `code/pooling_existential_reals/bounded_build_and_check.py`, which
   reports the data set and degrees of each instance and passed seven
   Gurobi checks, including a fan-out instance in which one variable has
   five occurrences. An independent audit of this item
   (`notes/review-pooling-existential-reals-bounded.md`) passed with minor
   corrections, all applied, including exact rational checks of the
   intended flow on seven systems and structural assertions on 300 random
   instances. The exact and structural audit is now saved as
   `code/pooling_existential_reals/check_bounded_exact.py`.
6. **Unresolved: one attribute with upper bounds only.** The present
   gadgets use exact quality pins, so deleting the lower bounds does not
   preserve the inversion and addition equations. The attempted extension
   using only an upper constraint on a positive product did not supply the
   missing reverse inequality. Miltzow and Schmiermann (TheoretiCS 2024;
   FOCS 2021 version, Section 1.2) discuss a related continuous-constraint
   problem with only the concave constraint `x·y ≤ 1` whose complexity was
   unresolved there. This analogy is not a reduction: arbitrary pooling
   constraints and substitutions have not been shown equivalent to that
   problem, and it does not rule out a different one-attribute construction.
   This direction is closed here as unresolved. A bounded pool count with
   fixed quality count is also outside this hardness statement: those
   instances are in `NP` by the repository's
   [linear-fiber certificate lemma](fixed-parameter-linear-fibers-np-membership.md),
   so `∃R`-hardness there would imply `NP = ∃R`. The
   [one-pool theorem](pooling-one-pool-bypass-existential-reals.md) instead
   uses bypass arcs and an unbounded number of attributes.

## 7. Verification record

`code/pooling_existential_reals/build_and_check.py` implements the
reduction as written (Haugland model, `w`-variables, forced nodes, costs,
`ζ`, diluent and slack capacities `B`, inverse pools for every variable)
and solves the resulting instances with Gurobi 13 (nonconvex QCQP,
tolerances `1e-9`), asserting a certified optimal status. Seven ETR-INV systems were checked, including the
satisfiable systems `x·x = 1`, `x + x = y, x·y = 1` (solution `1/√2`),
`x + y = z, x·z = 1, y·y = 1` (golden-ratio solution), two boundary systems
with values exactly `1/2` and `2`, and two unsatisfiable systems. In every
satisfiable case the optimal profit equals `ζ` and the recovered variable
values match the algebraic solution to six digits; in every unsatisfiable
case the optimal profit is strictly below `ζ` (by at least `0.15`). This is a
sanity check of the gadgets, not part of the proof.

## Sources

- M. Abrahamsen, A. Adamaszek, T. Miltzow, *The Art Gallery Problem is
  ∃R-complete*, STOC 2018 (arXiv:1704.06969; J. ACM 69(1), 2022). Definition 5
  (ETR-INV) and Theorem 7.
- M. Abrahamsen, T. Miltzow, *Dynamic Toolbox for ETRINV*, arXiv:1912.08674
  (2019). Theorem 1 and Corollary 2 (algebraic consequence).
- M. Schaefer, J. Cardinal, T. Miltzow, *The Existential Theory of the Reals
  as a Complexity Class: A Compendium*, arXiv:2407.18006 (2024). Entry (A1).
- M. Schaefer, *Realizability of graphs and linkages*, in Thirty Essays on
  Geometric Graph Theory, Springer 2013, Lemma 3.9.
- M. Schaefer, D. Štefankovič, *Fixed points, Nash equilibria, and the
  existential theory of the reals*, Theory Comput. Syst. 60 (2017) 172–193.
- T. Miltzow, R. F. Schmiermann, *On classifying continuous constraint
  satisfaction problems*, FOCS 2021; TheoretiCS 3 (2024), Art. 10
  (arXiv:2106.02397), Theorems 1.11 and 1.13 and Section 1.4.
- M. Poss, J. Kurtz, M. Goerigk, D. Henke, arXiv:2608.21574 (2026),
  Theorem 4 (`∃R`-completeness of quadratically constrained programs).
- D. Bienstock, A. Verma, *Strong NP-hardness of AC power flows feasibility*,
  Oper. Res. Lett. 47 (2019) 494–501, Section 1.3
  (local: `literature/papers/bienstock2019-strong-np-hardness-of-ac`).
- D. Haugland, E. M. T. Hendrix, *On a pooling problem with fixed network
  size*, ICCL 2015 (local: `literature/papers/haugland2015-on-a-pooling-problem-with`).
- J. Canny, *Some algebraic and geometric computations in PSPACE*, STOC 1988.
- D. Haugland, *The computational complexity of the pooling problem*,
  J. Global Optim. 64 (2016) 199–215, Section 2.1
  (local: `literature/papers/haugland2016-the-computational-complexity-of-the`).
- M. Alfaki, D. Haugland, *Strong formulations for the pooling problem*,
  J. Global Optim. 56 (2013) 897–916.

## Status

Draft by the root agent, 2026-09-05. Numerical gadget checks passed.
Independent proof audits: `notes/review-pooling-existential-reals-1.md`
(PASS WITH CORRECTIONS: the slack bound had omitted the inversion arcs in
`M`, with a Gurobi counterexample; corrected) and
`notes/review-pooling-existential-reals-2.md` (PASS WITH CORRECTIONS on the
revised text: irrational `α` in Corollary 3, explicit bijection sentence in
Lemma 6, code alignment; all applied). Novelty audit:
`notes/pooling-existential-reals-novelty.md` (new as a statement about
pooling; unstructured QCQP `∃R`-completeness credited).
