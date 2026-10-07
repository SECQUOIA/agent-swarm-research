# Opus review of foundations and algorithms, round 1

## Scope and snapshot

This is a read-only review of `sections/foundations.tex` and
`sections/algorithms.tex`. Both files changed several times while I worked
(foundations at 01:32, 01:41 and 01:43 UTC; algorithms at 01:29 and 01:38
UTC). I re-read each new version in full and re-checked every finding
against the final snapshots below. Line numbers refer to these snapshots.

| File | SHA-256 of reviewed snapshot | Modified (UTC) |
| --- | --- | --- |
| `sections/foundations.tex` | `825ccbd5c15a5ef19cc06eb27a9d25112e446f57d32273a3d4f35ae51418d58b` | 2026-10-06 01:43:36 |
| `sections/algorithms.tex` | `8980d76a4a5af79fcedb2dfe77e5ca75ee4f67bfd4a62bce18060383918d2cff` | 2026-10-06 01:38:49 |

Review window: 2026-10-06 01:21 to 01:50 UTC. Both hashes were confirmed
unchanged when this report was written.

Not reviewed: the other sections and the integrated or compiled paper.
From other sections I read only the statements that these two sections
cite: in `certificates.tex`, Lemma `lem:reference-family`, the definitions
of relaxation-sound steps and witness pools, Theorem `thm:protected`, and
Propositions `prop:fixed-box`, `prop:join`, `prop:round-check`, and
`prop:current-round`, together with Example `ex:round-check` and Corollary
`cor:objective-ceiling`; in `local-rates.tex`, the statement of
Proposition `prop:two-variable-rate` and the citation for clipped
McCormick monotonicity.

## Verdict

At the final snapshot both sections are mathematically sound. All six
known objections and the later findings from `review-foundations-r1.md` are
resolved. Three items still need changes before submission:

1. **F1/A1 (material).** A construction determined by the box alone can
   violate monotonicity. The policy's own five-point tangent rows do so.
   The text says or implies the opposite in foundations lines 88–93 and
   gives an incomplete reason in algorithms lines 316–323 and 601–602. An
   exact counterexample and replacement text are below.
2. **A2 (material for a validity proof).** The floating-point primitives
   in algorithms lines 392–447 are defined only for finite arguments,
   although the passes apply them after overflow. The overflow sentence
   covers only one direction, and the arithmetic assumption is both
   stronger than needed (round-to-nearest) and not quite sufficient (it
   does not exclude flush-to-zero or denormals-are-zero). A complete
   replacement lemma and proof are below. The implementation is correct;
   only the written argument is incomplete.
3. **A8 (attribution).** `algorithms.tex` contains no citations, yet its
   safe dual bound, its outward row correction, and its exact LP
   verification with rational reconstruction are established techniques.
   Source requests are listed below.

F2 is a recommended original development. It shows that a greatest fixed
box exists without the closedness hypothesis, which makes item (ii) of
Section 2.4 and the inclusion chain more informative. The remaining
findings are minor. Once items 1–3 are fixed, I have no remaining
mathematical objection to these two sections.

## 1. Known objections at the final snapshot

| Objection | Status |
| --- | --- |
| `H_U ⊆ P ⊆ B_∞` for every fixed `P` | Resolved. Lines 365–369 state the two independent inclusions and give a correct counterexample (`φ_B≡0`, `H_U={0}`, fixed box `{1}`). The endpoint ceilings (372–375) need only `P ⊆ B_∞`. F2 gives a stronger correct chain. |
| Sublevel-hull proof must take hulls | Resolved. Lines 231–234 take the closed hull of `S ⊆ K_U(H_U) ⊆ H_U`. The proof uses neither face attainment by original points nor continuity of `f`. |
| Fair schedules need only order and containment | Resolved. Lemma `lem:sequential`(b)–(c), lines 158–187, uses the complete-block sandwich `T_U^{t_j}(B) ⊆ C_{t_j} ⊆ T_U^j(B)`. I checked the proof, including the empty-box convention (lines 131–132). See F7 for its last sentence. |
| Closedness needed only for fixedness | Resolved. Proposition `prop:fixed-limit` (286–302) uses `(closed-family)` only to show that `B_∞` is fixed. |
| Symmetry "defeats" OBBT | Resolved. Lines 244–249 now state the singleton obstruction, the bound `L(B_∞) ≤ L(H)`, and that tightening can still remove parts of the box outside the hull. |
| Nonfixed-limit example on all subboxes | Resolved. Lines 338–346 define `φ_B` on every `[r,s]` through `g(s)`. I checked validity, monotonicity, lower semicontinuity, `s_{k+1}-1/2=(s_k-1/2)/2`, `T_0(B_∞)=[0,1/8]`, and the failure of `(closed-family)` at `C_k=[0,s_k]`, `x_k=s_{k+1}→1/2`. |

Also resolved since earlier snapshots:

- The archived 0.705 factor was replaced by the exact one-dimensional
  example in lines 200–210, which I verified.
- The text now states that selective schedules inherit the lower
  enclosures `T_U^m(B) ⊆ C_m`.
- The local-rate summary is no longer phrased as a dichotomy.
- The node-incumbent caveat on `ε` was added.
- `algorithms.tex` now cites Lemma `lem:reference-family` instead of
  re-proving lifted order. It uses the same `y_k` and `Gz ≤ g` notation as
  `certificates.tex`.
- "Sidecar" is now defined at its first use (algorithms 287–288).

## 2. Findings in `foundations.tex`

### F1 (material). A construction determined by the box can violate monotonicity (lines 88–93)

The sentence "Monotonicity can fail when the construction depends on more
than the box" suggests that a construction determined by the box alone is
safe. It is not, and the paper's numerical policy is an example.

**Counterexample (exact).** Let `f(x)=x^2` with no constraints. On
`B=[ℓ,u]`, relax with the rows `y ≥ 2px-p^2` at the five points
`p_k=ℓ+k(u-ℓ)/4` (`k=0,…,4`) and the secant `y ≤ (ℓ+u)x-ℓu`, with objective
`v=y`. These are the policy's square rows without the retained pool. On
`B`, tangents are at most `x^2`, which is at most the secant, so

```
φ_B(x) = max_k (2 p_k x - p_k^2).
```

- `φ_{[-1,1]}(0)=0` (knot `p=0`), but `φ_{[-1/2,1]}(0)=-1/64`. The knots are
  `-1/2,-1/8,1/4,5/8,1`, and the best of them at `x=0` is `p=-1/8`. Hence
  `(eq:monotonicity)` fails.
- At `U=1/4 ≥ f^*=0`, the condition `2px-p^2 ≤ U` gives `x ≤ (p^2+U)/(2p)`
  for `p>0` and `x ≥ (p^2+U)/(2p)` for `p<0`. Therefore
  `T_U([-1,1])=[-1/2,1/2]` (knot `1/2`), whereas
  `T_U([-1/2,1])=[-1/2,41/80]` (knot `5/8`). Lemma `lem:order`(b) fails
  above the optimal value. The point `(x,y)=(41/80,1/4)` is feasible on
  the smaller box `[-1/2,1]`, where all five tangents hold and the secant
  value is `121/160`. On `[-1,1]`, the tangent at `1/2` requires
  `y ≥ 21/80 > 1/4`.

The family satisfies `(closed-family)`, because its knots depend
continuously on the endpoints. So closedness and monotonicity are
independent properties, and the closing sentence of lines 330–332 should
not be read as evidence of monotonicity.

**Replacement for lines 88–93.**

```latex
Monotonicity can fail even when the construction is determined by the box.
For example, relax $x^2$ on $[\ell,u]$ by the tangents $y\ge2px-p^2$ at the
five points $p=\ell+k(u-\ell)/4$, $k=0,\dots,4$, and the secant, with
objective $v=y$, as in the numerical policy of
Section~\ref{sec:algorithms-policy}. Then
$\phi_{[-1,1]}(0)=0>-1/64=\phi_{[-1/2,1]}(0)$, and at $U=1/4$ one has
$T_U([-1,1])=[-1/2,1/2]$ but $T_U([-1/2,1])=[-1/2,41/80]$: on the larger
box the tangent at $1/2$ excludes the point $(x,y)=(41/80,1/4)$.
Constructions that depend on more than the box need not be monotone
either. Cutting planes separated at earlier relaxation solutions and kept
in a pool depend on the search history, and rows dropped to save time, or a
relaxation that is solved only approximately, can produce a larger
feasible set on a smaller box. For such constructions the statements below
require a separate argument.
```

### F2 (recommended development). A greatest fixed box exists without `(closed-family)`

Item (ii) (lines 358–361) and Proposition `prop:fixed-limit` identify a
greatest fixed box only under `(closed-family)`. Monotonicity alone already
gives one, and it contains both `H_U` and every fixed box. This makes the
inclusions in lines 365–369 a single chain while keeping the observation
that `H_U` and a given `P` need not contain each other. The result is the
order-only, arbitrary-family form of Proposition `prop:join` in
`certificates.tex`.

```latex
\begin{lemma}[Greatest fixed box]\label{lem:greatest-fixed}
Let $\mathcal P$ be a nonempty family of fixed boxes of $T_U$ contained in
$B_0$. Then $Q=\hull\bigcup_{P\in\mathcal P}P$ is a fixed box. Hence, if
$T_U$ has a fixed box in $B_0$, the hull $P_U$ of all fixed boxes in $B_0$
is the greatest fixed box in $B_0$. It satisfies $P_U\subseteq B_\infty$,
and $H_U\subseteq P_U$ whenever $H_U\ne\emptyset$.
\end{lemma}
\begin{proof}
Each $P\in\mathcal P$ satisfies $P\subseteq Q\subseteq B_0$, so
Lemma~\ref{lem:order}(b) gives $P=T_U(P)\subseteq T_U(Q)$. The closed box
$T_U(Q)$ therefore contains $Q$, and Lemma~\ref{lem:order}(a) gives
$T_U(Q)=Q$. Apply this to the family of all fixed boxes in $B_0$. The
inclusion $P_U\subseteq B_\infty$ is Lemma~\ref{lem:fixed-persist}, and
$H_U$ is fixed by Lemma~\ref{lem:sublevel-hull}.
\end{proof}
```

Consequential edits:

- **Proposition `prop:fixed-limit`.** Conclude "Then `B_∞` is a fixed box,
  hence `B_∞=P_U`."
- **Optional remark with citation.** Subboxes of `B_0`, together with `∅`,
  form a complete lattice under inclusion, and `T_U` is monotone on it.
  `P_U` is its greatest fixed point in the sense of Knaster and Tarski (the
  bibliography already contains `tarski1955fixpoint`). `(closed-family)`
  is the downward continuity, `T_U(⋂C_k)=⋂T_U(C_k)`, under which the
  Jacobi sequence reaches this fixed point after countably many rounds.
  I checked this continuity: the subsequence argument of the existing
  proof gives the nontrivial inclusion.
- **Example `ex:not-fixed`.** Add "Here `P_U={0}`. Continuing from `B_∞`
  gives `[0,1/8]`, `[0,1/32]`, …, which reaches `P_U` only as the limit of
  a second infinite sequence." Transfinite iteration is classical; see the
  source requests.
- **Item (ii), lines 358–361.** Replace the last clause with "the greatest
  of them, `P_U`, contains `H_U` and every other fixed box in `B_0`, and
  equals the limit `B_∞` under `(closed-family)`".
- **Lines 365–369.** Use "These objects satisfy `H_U ∪ P ⊆ P_U ⊆ B_∞ ⊆ B_k`
  for every fixed box `P ⊆ B_0`, although `H_U` and `P` need not contain
  each other." Keep the example and add "and there `P_U=B_∞=[-1,1]`".

### F3 (minor). Vacuous clause in Proposition `prop:fixed-limit` (lines 289–290; proof 305–306)

`T_U(B_∞) ⊆ B_∞` holds for every box by Lemma `lem:order`(a), so the
clause and its proof sentence say nothing about `B_∞`. Delete them, or
replace them with the inclusion `P_U ⊆ B_∞` from F2.

### F4 (minor). Closedness paragraph (lines 323–332)

- **A general sufficient condition.** `(closed-family)` holds whenever
  `(x,ℓ,u) ↦ φ_{[ℓ,u]}(x)` is lower semicontinuous on `{ℓ ≤ x ≤ u}`.
  Proof: if `C_k ↓ C`, `x_k ∈ K_U(C_k)`, and `x_k → x`, then `x ∈ C` and
  `φ_C(x) ≤ liminf φ_{C_k}(x_k) ≤ U`. The lifted argument in the text is
  the special case of a compact `Z`. Family (a) (termwise McCormick with
  exact convex terms) is covered directly, because its projected objective
  is jointly continuous.
- **Independence from monotonicity.** Add one sentence saying that the
  five-point tangent family of F1 is closed but not monotone.

### F5 (minor). The persistence summary omits the cutoff condition (lines 279–284)

"bound the total movement of every endpoint under all later rounds of the
same relaxation family" holds only at cutoffs not below `U`. More
precisely, it holds at cutoffs not below the largest relaxation value of
the witnesses, which is the threshold in `certificates.tex`. Branch and
bound lowers the cutoff, so add "at cutoffs not below `U`".

### F6 (minor wording)

- **Line 5.** "the three objects that limit further tightening": item (iii)
  is a rate, not an object. Use "three limits on further tightening", which
  also matches the subsection title.
- **Lines 38–40.** In "all subboxes of a larger domain box (for McCormick
  relaxations of polynomials, of `R^n`)", `R^n` is not a box. Write "(for
  McCormick relaxations of polynomials, all boxes in `R^n`)".
- **Line 357.** In "which only a better incumbent shrinks", branching also
  shrinks `H_U`, because `B_0` is the node box. Write "only a better
  incumbent or branching shrinks".
- **Lines 55–58 (optional generality).** A compact `R(B)` excludes epigraph
  lifts such as `y ≥ x^2` with `v=y`. All three conclusions (attainment,
  lower semicontinuity, and projection of sublevel sets) hold if `R(B)` is
  closed, `v` is continuous, and every lifted sublevel set
  `{z ∈ R(B): v(z) ≤ t}` is compact. Not needed for the paper's families.

### F7 (minor). Last sentence of the proof of Lemma `lem:sequential`(c) (lines 185–186)

"Both sides are nested sequences with the same intersection" is too terse
for the key step. Replace it with:

> Each block is nonempty, so `t_j ≥ j → ∞`. The sequences
> `(T_U^{t_j}(B))_j` and `(T_U^j(B))_j` are cofinal in the nested sequence
> `(T_U^k(B))_k`, so both have intersection `⋂_k T_U^k(B)`. The sandwich
> gives the same intersection for `(C_{t_j})_j`, which equals `⋂_m C_m`
> because `(C_m)` is nested.

### F8. Attribution claims that need source checks

These claims need checks by the literature lead: lines 6–11 (Caprara and
Locatelli on order independence; Belotti et al. on greatest fixed points
of FBBT), lines 189–192 ("observed … for cyclic sweeps … in a form that
covers arbitrary fair schedules"), and lines 239–244 (Caprara, Locatelli,
and Monaci: "lower limit", "two-variable class", and an example with no
bound movement although `H_U` is a point). If Caprara and Locatelli
already treat arbitrary orders or simultaneous updates, delete "in a form
that covers arbitrary fair schedules and Jacobi rounds".

## 3. Findings in `algorithms.tex`

### A1 (material). Why the future-round results do not apply to the policy (lines 316–323 and 601–602)

Both passages attribute the loss of lifted monotonicity to the
history-dependent pool. Two separate mechanisms operate, and the first
does not involve history at all:

1. **Box-relative tangent points.** The five points move with the box.
   Even without a pool, the construction violates projected and lifted
   monotonicity (F1, which uses exactly these rows).
2. **A capped, shared, growing pool.** It keeps only the first 25 points
   of each square, so tangents at earlier box-relative points can be
   missing on a later, smaller box. Conversely, tangents added after a box
   `P` was certified are rows of a later relaxation on a box `C ⊇ P` that
   were absent when the witnesses were checked on `P`, so they can cut
   those witnesses. Theorem `thm:protected` needs the witnesses to stay in
   the cutoff set of every later box.

A minor third mechanism, which need not appear in the paper: outward
rounding makes the stored rows depend on the box through rounding errors,
so nested exact rows need not give nested stored rows.

The same paragraph uses monotonicity of `T_U` as the reason for the
triggers (lines 542–545; see A3). Because the policy's relaxation is not
monotone, that reason cannot be stated as a property of this relaxation.

**Replacement for lines 318–323.**

```latex
The five tangent points move with the box, and the shared pool keeps only
the first 25 points of each square. Box-relative tangent points violate
monotonicity even without a pool: at $U=1/4$ they give
$T_U([-1,1])=[-1/2,1/2]$ but $T_U([-1/2,1])=[-1/2,41/80]$
(Section~\ref{sec:foundations}). The pool restores earlier tangents only
while it has room, and tangents it gains later can cut lifted points
certified on an earlier box. The relaxations of successive callbacks are
therefore neither a monotone family nor nested along the search, and the
future-round results do not apply to them.
```

**Replacement for the sentence at lines 601–602**, followed by a cutoff
sentence that is currently missing:

```latex
The policy's relaxations are not monotone. A protected box also certifies
only steps at cutoffs at least its threshold, whereas incumbent
improvements lower the cutoff during the search.
```

**Lines 605–607.** "which can exceed the per-callback allowance" can be
made definite. Every instance in the frozen October inputs has at least 10
variables in product terms; I counted 20 instances, with between 10 and
144 such variables. A full round over these variables therefore needs at
least 20 support LPs, above the root allowance of 12, unless presolve
fixes variables. The integration note on certificate cost still applies:
this is not a required cost for each proposed bound.

### A2 (material for a validity proof). Rounding primitives and overflow (lines 392–447)

The passes apply `pred` and `succ` to values that can be `±∞` after
overflow, but lines 394–396 define them only for finite numbers, and
Lemma `lem:enclosure` assumes `fl(s)` is finite. The overflow sentence
(431–434) treats only "an upward overflow followed by a downward step". The
symmetric case in `r̄_j` is missing: a downward overflow followed by
`succ` gives `-Ω`, which lies above the exact value. Round-to-nearest is
not needed; faithful rounding suffices. Gradual underflow is the essential
assumption, and it should explicitly exclude flush-to-zero (FTZ) and
denormals-are-zero (DAZ) modes. The implementation (`math.nextafter` with
`±inf`, rejection of nonfinite third-pass products and results) matches
the corrected argument below, which I checked against
`solver/adaptive_obbt.py::dual_box_bound`.

**Replacement for lines 392–412.**

```latex
The implementation clips the returned multipliers to $y=\min\{\tilde y,0\}$
and evaluates~\eqref{eq:dual-residual} with directed rounding. Let $\bar F$
be the binary64 numbers together with $\pm\infty$, let $\Omega$ be the
largest finite one, and let $\operatorname{pred}$ and $\operatorname{succ}$
be the IEEE~754 operations nextDown and nextUp on $\bar F$; thus
$\operatorname{pred}(+\infty)=\Omega$ and $\operatorname{succ}(-\infty)=-\Omega$.
For an operation with exact real result $s$, write $\operatorname{fl}(s)\in\bar F$
for the computed result.

\begin{lemma}[One-step enclosure]\label{lem:enclosure}
Suppose rounding is faithful: $\operatorname{fl}(s)=s$ if $s\in\bar F$, and
otherwise $\operatorname{fl}(s)$ is one of the two consecutive elements of
$\bar F$ that enclose $s$. Then
$\operatorname{pred}(\operatorname{fl}(s))\le s\le\operatorname{succ}(\operatorname{fl}(s))$
for every real $s$.
\end{lemma}

\begin{proof}
If $\operatorname{fl}(s)=s$ there is nothing to prove. Otherwise let
$s^-<s<s^+$ be the enclosing pair. If $\operatorname{fl}(s)=s^-$, then
$\operatorname{pred}(s^-)<s$ and $\operatorname{succ}(s^-)=s^+>s$; the case
$\operatorname{fl}(s)=s^+$ is symmetric.
\end{proof}

With gradual underflow, every IEEE~754 rounding direction is faithful,
including overflow to $\pm\infty$ or to $\pm\Omega$. Flush-to-zero and
denormals-are-zero modes are not, and the argument assumes that they are
disabled.
```

**Replacement for lines 431–434**, the overflow sentence after the three
passes:

```latex
In the first two passes, $\sigma$ and $\underline r_j$ are results of
$\operatorname{pred}$ and hence at most $\Omega$, and $\overline r_j$ is a
result of $\operatorname{succ}$ and hence at least $-\Omega$. No sum or
difference in these passes therefore has the form $\infty-\infty$. An
infinite intermediate value is $-\infty$ in a lower bound or $+\infty$ in
an upper bound, which remains valid. The third pass rejects any nonfinite
product and a nonfinite final value.
```

**Line 443.** Replace "ordinary binary64 arithmetic with round-to-nearest
and gradual underflow" with "IEEE binary64 arithmetic with gradual
underflow".

**Optional sentence.** This argument also covers a host solver that leaves
a directed rounding mode active, because faithfulness holds in every
rounding direction.

### A3 (minor to moderate). Trigger rationale (lines 542–545)

"Monotonicity of `T_U` in the box and in the cutoff … is the reason these
two events can create new tightening" overstates the logic. Monotonicity
says that a smaller box or cutoff gives a smaller `T_U`, which is why
re-solving can pay off. It does not show that nothing else can. Unprocessed
directions at an unchanged box are another source, and the policy
deliberately does not revisit them. As A1 shows, the policy's relaxation
is not monotone in any case. Suggested replacement:

```latex
For a monotone relaxation, a smaller box or a smaller cutoff shrinks the
cutoff set and can move supports that were optimal before; the policy
re-triggers only on these two events and does not revisit directions left
unprocessed at an unchanged node. The cutoff-dependent floors of
Section~\ref{sec:local-rates} motivate the incumbent trigger. The
thresholds are heuristic.
```

### A4 (minor). Applying the row correction (lines 357–359)

"S the set of exact lifts `(x,(x_ix_j))`, `x ∈ B`" is right for the product
rows. For an original row or the cutoff row, `S` must be the exact lifts
of the points of `B` that satisfy that row. Those rows have floating-point
coefficients, so only upward rounding of the right-hand side occurs and
the conclusion is unaffected. Suggested wording: "applies to each product
row with `S` the exact lifts of the points of `B`, and to each original or
cutoff row with `S` the exact lifts of the points of `B` satisfying it;
all lie in the LP's variable box."

### A5 (minor). Dual bound (lines 368–377 and 392)

- State `μ=+∞` for an infeasible LP; inequality `(eq:dual-residual)` then
  holds trivially.
- **Sign convention.** Validity does not depend on the solver's sign
  convention for multipliers. SciPy's HiGHS interface reports `∂μ/∂b ≤ 0`
  for rows `Az ≤ b` of a minimization, which matches `y ≤ 0`; I checked
  this against `certified_driver.py` and `dual_box_bound`. Under the
  opposite convention, clipping would discard the multipliers and weaken
  the bound, but would never invalidate it. One sentence makes this
  robustness explicit.

### A6 (minor). Closure discussion and Theorem `thm:closure`

- **Line 220.** "Part (b) is what the stopping certificate is worth" is
  informal. Use "Part (b) states what the stopping certificate
  guarantees".
- **Line 231.** "The procedure need not terminate in finitely many
  rounds" is inaccurate: every run stops, because `K` is finite. Write
  "No finite round budget guarantees status *fixed*: that status requires
  exact iterates that reach a fixed box, and the square examples below
  never do."
- **Lines 236–237.** An exact rational LP solver removes reconstruction
  failures but not growth in the size of the iterates. In Heron's
  iteration the number of digits roughly doubles each round. Add that
  clause.
- **Theorem (b), lines 167–169.** Theorem `thm:protected` is stated for
  boxes `C_0 ⊇ P` in `B_0`. Either add "in `B_0`", or note that the
  reference family is defined on all rational boxes, so `B_0` may be any
  box containing `C`.
- **Theorem (b), optional strengthening.** "uses cutoffs at least `U`" can
  be weakened to "at least `max_{z∈W} v(z)`", the pool threshold, which
  is at most `U`. This is the form useful under decreasing incumbents.
- **Line 5.** "bounds that are actually valid" should read "valid bounds".

### A7 (minor). "Admission" and "admitted callbacks" (lines 512 and 529–541)

The text defines *admission* as passing the cheap checks. The counters
called "admitted callbacks" (table and lines 536–538) count only visits
that pass admission **and** a trigger (`S["calls"]` and the per-node count
in `TriggerState`). A visit that passes admission but triggers nothing is
admitted under the first definition yet not counted. Rename the counters
"acting callbacks", or define "admitted callback" once as one that passes
both. `effort.tex` may use "admission" for cost admission, which makes the
clash worse.

### A8 (attribution). No citations in `algorithms.tex`

- **Proposition `prop:dual-residual` (368–390).** This is the classical
  safe LP bound, in which an inexact dual vector's residual is absorbed
  through finite variable bounds and evaluated with directed rounding.
- **Proposition `prop:row-correction` (332–359).** Outward rounding of
  relaxation rows with a right-hand-side correction over variable bounds
  is the standard safe-linearization technique.
- **Exact verification (105–119).** Checking floating-point LP proposals
  exactly after rational reconstruction is established in exact LP.
- **Lemma `lem:lp-certificate` (87–103).** Correctly introduced as weak
  duality; a textbook citation is optional.
- **SCIP's LP-based OBBT (283–284).** The bibliography already contains
  Gleixner et al. 2017.

These attributions are needed to meet the brief ("do not portray classical
weak duality … as new"). Candidate sources are in Section 5.

## 4. Statements checked as correct

### Foundations

- **Lemma `lem:order` (a)–(c).** Correct.
- **Lemma `lem:sequential` (a)–(c).** Correct, including the empty-box
  convention.
- **One-dimensional example (200–210).** Checked the sequential map
  `(a,b) ↦ ((a+b)/4,(a+5b)/16)`, its validity conditions `b ≤ 3a` and
  `a ≤ 11b`, invariance of `b/a ∈ [7/12,3/4] ⊂ [1/2,1]`, and the
  eigenvalue `(9+√17)/32`. An exact iteration gives a final width ratio
  of `0.41009705080057`, against the eigenvalue `0.41009705080055`.
- **Lemma `lem:sublevel-hull`.** Correct.
- **Definition of fixed box and face characterization.** Correct, using
  compactness from lower semicontinuity.
- **Lemma `lem:fixed-persist`.** Correct.
- **Proposition `prop:fixed-limit`.** Correct apart from F3.
- **Lifted sufficient condition for `(closed-family)`.** Correct.
- **Example `ex:not-fixed`.** Correct.
- **Counterexample and endpoint ceilings in Section 2.4.** Correct.
- **Monotone constructions.** Lifted monotonicity implies projected
  monotonicity under a common objective. Constructions (a) and (b) are
  monotone. For the bilinear rows I checked the domination identity, and
  for squares the tangent and secant domination, including signed and
  degenerate intervals.

### Algorithms

- **Lemma `lem:lp-certificate`.** Correct, with all bound rows explicit.
- **Theorem `thm:closure` (a)–(e).** Correct given Theorem
  `thm:protected`, Proposition `prop:round-check`(b), Corollary
  `cor:objective-ceiling`, and Lemma `lem:fixed-persist`. I checked each
  part against `theory/certified_driver.py` and `theory/certificates.py`:
  - commit only after all `2n` exact replays;
  - rebuilt-row check of the old optima via `verify_protected_box`, which
    covers containment, rebuilt feasibility, exact face attainment, and
    pool value at most the cutoff;
  - an optional objective point that needs only feasibility and whose
    failure leaves the certificate unchanged;
  - `inconclusive` on a missing proposal or failed replay, discarding the
    partial round;
  - `unfinished` when the budget is exhausted;
  - prompt detection relying on rows that are a deterministic function of
    the box (`relaxation_rows`).
- **Example `ex:round-check`.** Checked independently.
- **Table `tab:closure-runs` and caption.** Every row matches
  `theory/remaining-benefit-driver-checks.json`, including 7, 4, 2, 10, 6,
  and 8 proposals, the boxes, the ceiling `-3`, and the failure reasons.
  The fourth-round failure in the upper direction is consistent with 8
  calls. The Heron values `5/4, 41/40, 3281/3280, 21523361/21523360` are
  exact. Reconstructing the double nearest to the fourth iterate with
  denominator bound `10^9` gives `667224190/667224159`. This illustrates
  the recorded failure mechanism.
- **Proposition `prop:row-correction`.** Correct. The statement about
  which coefficients need correction matches `Relaxation.add_row`: only
  the secant slope `ℓ_i+u_i` is inexact, `2p` and bound coefficients are
  already floating-point, and right-hand sides are rounded up exactly.
  Coefficient overflow raises `OverflowError`, which the callback treats
  as an unsupported relaxation.
- **Proposition `prop:dual-residual`.** Correct, including the bound
  multipliers `α_j=r_j^+` and `γ_j=r_j^-` and the use of
  `underline z ≤ overline z`.
- **Three passes and the final chain to `μ`.** Correct apart from A2.
  They match `dual_box_bound` step for step.
- **Proposition `prop:sidecar-validity`.** Correct, including the product
  intervals widened by one unit in the last place (`_down`/`_up` of the
  floating-point products, with `0` for squares whose interval contains
  `0`).
- **Cutoff paragraph.** Matches `_cutoff`: the absolute residual of
  `Problem.validation` covers rows, bounds, and integrality, the
  objective is computed exactly and rounded up, and the margin is
  `10^-6 max{1,|value|}`. The cancellation example is exact:
  `1e16+1` rounds to `1e16`.
- **Parameter table and policy rules.** All values match `Config`:
  admission and triggers in `TriggerState.reason`, score and ordering in
  `_candidate_order`, screening, the pilot (a single effective test, since
  the gain never decreases), the one-millisecond LP time floor, and
  deadline checks every 64 rows.

## 5. Source requests for the literature lead

I did not search for or check any of these sources. The specific
references are candidates from memory and must be verified before use.

1. **Caprara and Locatelli (2010), Math. Program. 125:123–137.** Confirm
   the form of their order-independence result (cyclic sweeps only,
   arbitrary orders, or simultaneous updates) and whether, and under what
   continuity, they prove that the limit is a fixed point. Needed for
   foundations lines 6–11 and 189–192.
2. **Caprara, Locatelli and Monaci (2016), Comput. Optim. Appl.
   64:513–533.** Confirm the term "lower limit" for `H_U`, the
   "two-variable class", and the example with no bound movement although
   `H_U` is a point. Needed for foundations lines 239–244.
3. **Belotti, Cafieri, Lee and Liberti.** Determine which paper
   establishes greatest fixed points of FBBT. Candidates are the 2010
   COCOA paper "Feasibility-based bounds tightening via fixed points" and
   the 2012 manuscript cited as `belotti2012fbbt`. Also check whether the
   `@misc` entry has a published version. Needed for foundations lines
   10–11.
4. **Fixed-point theory for F2.** Tarski (1955), already in the
   bibliography. Optionally, P. Cousot and R. Cousot, "Constructive
   versions of Tarski's fixed point theorems", Pacific J. Math. 82 (1979)
   43–57, for transfinite iteration.
5. **Safe LP bounds for A8 and Proposition `prop:dual-residual`.**
   A. Neumaier and O. Shcherbina, "Safe bounds in linear and mixed-integer
   linear programming", Math. Program. 99 (2004) 283–296; and C. Jansson,
   "Rigorous lower and upper bounds in linear programming", SIAM J.
   Optim. 14 (2004) 914–935.
6. **Safe linear relaxations for A8 and Proposition
   `prop:row-correction`.** G. Borradaile and P. Van Hentenryck, "Safe and
   tight linear estimators for global optimization", Math. Program. 102
   (2005) 495–517, or whatever source the lead finds closest to rounding
   coefficients with a right-hand-side correction over variable bounds.
7. **Exact LP verification and rational reconstruction (algorithms
   105–119).** D. Applegate, W. Cook, S. Dash and D. Espinoza, "Exact
   solutions to linear programming problems", Oper. Res. Lett. 35 (2007)
   693–699; A. Gleixner, D. Steffy and K. Wolter, "Iterative refinement
   for linear programming", INFORMS J. Comput. 28 (2016) 449–464; and
   W. Cook, T. Koch, D. Steffy and K. Wolter, "A hybrid branch-and-bound
   approach for exact rational mixed-integer programming", Math. Program.
   Comput. 5 (2013) 305–344.
8. **IEEE Std 754-2019.** For nextUp/nextDown and rounding-direction
   attributes (A2).

## 6. Verification actually performed

Reads (targeted `cat`, `sed -n`, `grep`):

- `AGENTS.md`, `evidence/BRIEF.md`, `evidence/INTEGRATION-NOTES.md`
  (twice, including the later reviewer-findings section), and
  `evidence/WRITING-TASKS.json`.
- `evidence/audit-rates.md`: the opening findings, the coverage table,
  common assumptions, interpretation, verification, and supplemental
  foundations sections.
- `evidence/audit-certificates.md`: sections 1–2, 5, and 7–9.
- `evidence/literature-audit.md`, `evidence/bibliography-aliases.json`,
  and the relevant `references.bib` entries.
- `evidence/review-foundations-r1.md`, read only after my own analysis was
  complete, to mark overlap.
- The two sections under review, each read in full several times with
  `cat -n`, with `sha256sum` and a `diff` against a private copy kept
  outside the repository.
- The cited statements in `certificates.tex` and `local-rates.tex`
  listed under Scope.
- Archived code and data under `research-20261003-adaptive-obbt/`:
  `theory/certified_driver.py`, `theory/certificates.py`,
  `theory/check_certified_driver.py`,
  `theory/remaining-benefit-driver-checks.json`, the fixture definitions in
  `theory/check_remaining_benefit.py`, `solver/adaptive_obbt.py` (all of
  it), `experiments/models.py` (`Problem.validation`), and an excerpt of
  `solver/test_adaptive_obbt.py`.

Two narrow commands were run:

1. `python3 -I -B -`, reading the frozen instance JSON files under
   `experiments/frozen/`, which counted variables occurring in product
   terms: 20 instances, minimum 10, maximum 144. No solver or model code
   was imported.
2. `python3 -I -B -` with an inline exact-arithmetic script using
   `fractions.Fraction` and `math`. Every assertion passed. It checked:
   - the five-point tangent counterexample of F1:
     `T_{1/4}([-1,1])=(-1/2,1/2)`, `T_{1/4}([-1/2,1])=(-1/2,41/80)`,
     feasibility of the witness on the smaller box, and
     `φ_{[-1,1]}(0)=0`, `φ_{[-1/2,1]}(0)=-1/64`;
   - the one-dimensional sequential example over 12 exact rounds, with
     its conditions, its ratio interval, and agreement of the width ratio
     with `(9+√17)/32`;
   - `math.nextafter` semantics at `±inf`, overflow of a binary64 product
     to `inf` without an exception, and `OverflowError` from
     `float(Fraction(10**400))`;
   - the fourth Heron iterate and its reconstruction from the nearest
     double.

   One printed diagnostic line in that script was malformed and is
   disregarded. All checks were assertions.

No numerical experiment, solver run, LaTeX build, project-wide check, or
CI-status or CI-log inspection was performed. No literature search was
performed. I wrote no repository file other than this report. The private
scratch copies of the two sections in `/tmp` were deleted after the final
hash check.
