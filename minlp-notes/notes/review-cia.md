# Independent agent review of the uniform-control CIA obstruction

Date: 2026-09-04. Review target:
[`results/cia-uniform-switching-obstruction.md`](../results/cia-uniform-switching-obstruction.md).
This is an independent agent review, not external peer review.

**Verdict:** The five-mode counterexample is correct and contradicts Conjecture 1 in the
final published Sager–Zeile article. The general continuous formula, discrete recurrence,
and strict additive discretization bound are also correct. One sentence in the discrete
sufficiency proof needed correction; the author repaired it, and the final wording was checked. Novelty of the
counterexample relative to later work remains subject to the separate literature search.

## Check against the published problem

The primary article is Sager and Zeile, *On mixed-integer optimal control with constrained
total variation of the integer control*, Computational Optimization and Applications 78
(2021), 575–623, [DOI](https://doi.org/10.1007/s10589-020-00244-5).
The local preprint records the conjecture at
[[sager2020-on-mixed-integer-optimal-control]] p.27. Its problem definitions are at
[[sager2020-on-mixed-integer-optimal-control]] p.3-5.

I independently read the final article's extracted definitions and rendered the final
PDF's printed page 615 (PDF page 42 including the repository cover) to inspect Conjecture 1,
equation (7.6). The conjecture is present in the final publication, with the stated first
branch `T/(s+2)+Δbar/2` when `s≤n−2`; its assumptions are `1≤s≤N−2`, `n>2`.
There is no requirement `n≤s+2` that would exclude five modes with one switch.

The relevant conventions match the proposed counterexample:

- Definition 1, printed page 578, normalizes total variation by one-half the sum of
  component variations. A change from one selected mode to another therefore costs
  one switch, not two. Remark 1, printed page 579, explains this factor.
- Definition 5, printed page 580, permits every relaxed column in the simplex.
  The uniform column `(1/5,...,1/5)` is admissible. Definition 7 takes arbitrary such
  relaxed data; it does not require bang-bang relaxed trajectories.
- Definition 7 and constraint (3.4), printed pages 580–581, minimize the maximum
  absolute cumulative deviation over all components and interval endpoints. This is
  exactly the discrepancy being computed here. For piecewise constant controls,
  each component's integral is affine inside an interval, so interior points cannot
  produce a larger absolute deviation than both endpoints.
- The paper counts changes between active intervals. Its Definition 10 starts the
  switch definition at interval `j≥2`, and its optimization over the initial active
  mode confirms that the initial activation is not a charged switch. The discrete
  TV display has a notational `j=1` boundary ambiguity for `w_{i,0}`; this does not
  change the intended convention. Even charging an extra initial activation would
  only restrict schedules and cannot rescue the proposed upper bound.
- The uniform relaxed trajectory is constant, hence its relaxed total variation is
  zero if that additional restriction were imposed.

The example uses `n=5`, `s=1`, `N=45`, `T=45`, and `Δbar=1`. Thus all numerical
assumptions hold: `1≤1≤43`, `5>2`, and `1≤5−2`.

## Independent proof covering every one-switch schedule

By symmetry, any nonconstant schedule with at most one switch selects one mode on
`[0,τ)` and another on `[τ,T]`, where `0≤τ≤T`. Allowing `τ=0,T` also includes
constant schedules. At least one of the `n≥3` modes is never selected.

For `α_i=1/n`, the first selected mode has discrepancy `−(n−1)τ/n` at the switch and
`T/n−τ` at the horizon. The second selected mode has discrepancy `τ/n` at the switch
and `τ−(n−1)T/n` at the horizon. Unused modes have final discrepancy `T/n`.
All paths are monotone between these events, giving

```
D(τ) = max{T/n, (n−1)τ/n, (n−1)T/n−τ}.
```

The omitted absolute-value terms are bounded by the displayed terms, including when
`τ=0,T`. Balancing the increasing and decreasing terms gives
`τ*=(n−1)T/(2n−1)` and value `(n−1)²T/[n(2n−1)]`, so the exact minimum is

```
T max{1/n, (n−1)²/[n(2n−1)]}.
```

For `n=5,T=45`, `τ*=20` is a grid point and the value is 16. In discrete notation,
`D(k)=max{9,4k/5,36−k}`. If `k≤20`, the last term is at least 16; if `k≥20`, the
middle term is at least 16. A 20-interval first block followed by a 25-interval second
block attains 16. Constants have discrepancy 36.

The conjectured value is `45/3+1/2=31/2`, strictly below 16. This disproves even the
upper-bound interpretation of the conjecture; it does not rely on whether its equality
could already fail through a smaller worst-case value.

## Independent proof check for arbitrary few-switch budgets

Let `m=s+1<n` and `r=n/(n−1)`. Every admissible schedule has at most `m` positive
blocks, so at least one mode is unused and `E≥T/n`.

At the end `t_j` of a block starting at `t_{j−1}`, its selected mode has accumulated
occupation at least `t_j−t_{j−1}`. Repeated use of that mode can only increase this
occupation. The negative discrepancy bound gives

```
t_j ≤ r t_{j−1} + rE.
```

Iteration yields `T≤nE(r^m−1)`, including schedules with fewer blocks. Hence
`E≥max{T/n,T/[n(r^m−1)]}`. This argument does not assume distinct modes.

For attainment, assign distinct modes to blocks ending at
`t_j=T(r^j−1)/(r^m−1)`. Their discrepancies at their own block endpoints all equal
`−T/[n(r^m−1)]`. Before activation and at the horizon, positive discrepancies are
at most `T/n`; after activation no negative discrepancy is lower than the endpoint
value. Unused modes attain `T/n`. This proves the formula exactly.

For every fixed `s`, its second coefficient tends to `1/(s+1)` as `n→∞`, exceeding
the conjectured first-branch continuous coefficient `1/(s+2)`. These are lower bounds
on the full worst-case problem, not a proof that uniform data are worst-case.

## Discrete recurrence and discretization bound

On a unit grid, the discrepancy is a multiple of `1/n`. Write its proposed bound as
`K/n`, where `K` is integer. The unused-mode condition gives `K≥N`. The same block
inequality gives

```
t_j ≤ floor((n t_{j−1}+K)/(n−1)).
```

Thus, starting at `b_0=0`, the recurrence
`b_{j+1}=floor((n b_j+K)/(n−1))` gives a necessary reachability condition
`b_m≥N`. It is sufficient: take block ends `min(N,b_j)` until reaching `N` and use
distinct modes. Every negative extreme is controlled at its block endpoint; every
positive discrepancy is at most `N/n≤K/n`.

The original draft said `K≥N≥1` alone makes every step increase by at least one.
That sentence is false for, e.g., `n=5,N=1,K=1`, where all iterates are zero. The
repair is immediate: if `b_1=0`, every iterate is zero, so a successful reachability
predicate forces `b_1≥1`, equivalently `K≥n−1`. Under that condition every iterate
increases by at least one. The theorem and construction therefore remain valid.

Let `Ec` denote the continuous optimum. Set `A=ceil(nEc)` and `K=A+n−2`. For an
integer `b`,

```
floor((n b+K)/(n−1)) = ceil((n b+A)/(n−1))
                      ≥ n b/(n−1) + n Ec/(n−1).
```

The discrete recurrence dominates the continuous recurrence with error `Ec`, so it
reaches `N` by block `m`. Moreover `K≥N` and
`K/n−Ec < (n−1)/n`, proving the claimed strict upper bound. The continuous lower
bound follows because grid controls are a subset of continuous controls. This proof
does not assume that independent rounding of switching times preserves discrepancy.

## Exact computational cross-checks

Independent enumeration using integer discrepancy numerators, with no optimization
solver, checked all 885 schedules for `n=5,N=45,s≤1`: five constant schedules and
`5·4·44=880` nonconstant schedules. The exact optimum was 16. All 20 optimal schedules
have switch position 20, one for each ordered pair of distinct modes. The simplification
`D(k)=max{9,4k/5,36−k}` matched the full prefix calculation for every schedule.

A second independent enumeration checked all admissible schedules for `n=2,...,6`,
`N=1,...,7`, and all `s=0,...,n−2`. Across 105 parameter cases and 127,078 schedules,
the scalar recurrence exactly matched the minimum integer discrepancy numerator.
Every case also satisfied the strict additive bound, evaluated with exact rational
arithmetic. This includes small-horizon cases that exposed the proof-sentence issue.

## Further review: exact continuous worst-case with one switch

The author subsequently proposed a stronger result. I checked it independently for
arbitrary measurable simplex-valued relaxed controls, including controls that are not
uniform or piecewise constant. For `n≥3`, the full continuous worst-case discrepancy
with at most one switch is exactly

```
H_n(T) = T max{1/3, (n−1)²/[n(2n−1)]}.
```

This section is a separate review of that stronger statement. It does not modify the
already verified five-mode counterexample or assume that uniform controls are always
worst-case. Uniform data attain the maximum for `n≥5`; three equal consecutive pure-mode
blocks attain it for `n=3,4`.

Normalize `T=1`. Write `A_i(t)=∫_0^t α_i(u)du` and `m_i=A_i(1)`, so
`Σ_i A_i(t)=t`, `Σ_i m_i=1`, and every `A_i` is nondecreasing and 1-Lipschitz.
For the schedule selecting mode `p` until `τ` and distinct mode `q` afterwards, define
`R_pq=max_{i∉{p,q}} m_i`. Direct endpoint analysis gives the exact expression

```
D_pq(τ) = max{R_pq, τ−A_p(τ), 1−m_q−τ}.             (A)
```

To check that nothing is missing, the first mode's largest negative discrepancy is
`τ−A_p(τ)` and its possible positive final discrepancy is
`m_p−τ≤1−m_q−τ`. The second mode's largest positive preactivation discrepancy is
`A_q(τ)≤τ−A_p(τ)` and its possible negative final discrepancy is `1−m_q−τ`.
Every omitted mode has nonnegative discrepancy increasing to its total mass. Each
selected mode is monotone on either side of the switch, so there are no further extrema.
The expression also handles `τ=0,1` and thereby constant schedules.

For a target `E`, the term `τ−A_p(τ)` is nondecreasing and the third term in (A)
is decreasing. Therefore the earliest possible switch that meets the third bound is

```
τ_q = max{0,1−m_q−E}.
```

A schedule with ordered pair `(p,q)` and discrepancy at most `E` exists if and only if

```
R_pq ≤ E,              A_p(τ_q) ≥ τ_q−E.             (B)
```

Set `E=max{1/3,(n−1)²/[n(2n−1)]}`. Choose `q` with largest total mass and `r` with
second largest total mass.

If `m_q≥E`, at most two masses can be strictly greater than `E`, since `E≥1/3`.
Choose `p` to cover the other such mode if it exists. Then all omitted masses are
at most `E`, while `τ_q≤1−2E≤E`. Since `A_p(τ_q)≥0`, condition (B) holds.

Otherwise all masses are less than `E`, so every pair satisfies the omitted-mode
condition. Suppose, for contradiction, that no one-switch schedule achieves `E`.
Here `τ_q=1−m_q−E>0`; put `h_q=1−m_q−2E` and define `τ_r,h_r` analogously.
Failure of every `p→q`, with `p≠q`, gives

```
A_p(τ_q) < h_q  for every p≠q.
```

Failure of `q→r` gives `A_q(τ_r)<h_r`. Since `m_q≥m_r`, we have `τ_q≤τ_r`, hence
`A_q(τ_q)<h_r`. Summing all components at `τ_q` gives

```
1−m_q−E < (n−1)(1−m_q−2E)+(1−m_r−2E),
(2n−1)E < n−1−(n−2)m_q−m_r.                         (C)
```

The largest and second largest masses obey
`m_q≥1/n` and `m_r≥(1−m_q)/(n−1)`. Because
`(n−2)−1/(n−1)>0` for `n≥3`, these imply

```
(n−2)m_q+m_r ≥ (n−1)/n.
```

Thus (C) implies `(2n−1)E<(n−1)²/n`, contradicting the definition of `E`.
This proves the upper bound for all relaxed controls.

For the matching lower bounds, three consecutive equal pure-mode blocks force error
at least `1/3`: a schedule using at most two modes omits one of the three modes with
mass `1/3`. The previously reviewed uniform-control formula forces error at least
`(n−1)²/[n(2n−1)]`. Taking the larger proves the stated worst-case equality.

The proof is constructive. In the all-small-mass case it suffices to check the `n−1`
candidates `p→q` at `τ_q`, followed, if needed, by `q→r` at `τ_r`. Thus it needs
only the vector `A(τ_q)` and the scalar `A_q(τ_r)` after computing and sorting the
total masses; finding the two largest masses is itself linear in `n`. This is a
worst-case guarantee, not a claim that these candidates solve every instance optimally.

For piecewise constant relaxed data on an arbitrary grid, moving the constructed
single switch to its nearest grid point changes each cumulative component integral
by at most `Δbar/2`. Therefore the corrected discrete universal upper bound is
`H_n(T)+Δbar/2`. This gives an upper bound, not an equality for the discrete worst-case
value. With only one switch, there is no accumulation of rounding errors from several
switching times. At fixed horizon, the discrepancy between the continuous and discrete
worst-case values can therefore be controlled from above by this half-grid term.

An exact-rational computational cross-check generated 800 nonuniform relaxed trajectories
with seven equal intervals, `n=3,...,10`, and integer column weights from 0 through 9
normalized to sum to one (random seed 4084). For every candidate considered by the above
construction, formula (A) matched an independent full component evaluation at every grid
endpoint and at the switch. In every instance, one of the stated candidates attained
discrepancy at most `H_n(1)`. This check supports the algebra but is not used in its proof.

Final-text check: the full one-switch theorem and its constructive and grid consequences
were read in the result file after insertion and agree with this independent review.
The discrete recurrence proof now contains the corrected reachability argument.

## Second independent review: equal-total two-switch theorem

The final text of
[`results/cia-two-switch-equal-masses.md`](../results/cia-two-switch-equal-masses.md)
was reviewed separately from the first review in
[`review-cia-two-switch-equal-masses.md`](review-cia-two-switch-equal-masses.md).
The theorem and proof are correct for `n≥4`, arbitrary measurable simplex-valued
controls, and equal terminal allocation `T/n` to every mode. This second review
found no mathematical issue.

I independently checked the following potentially delicate points:

- The cumulative allocation is absolutely continuous, and `t−A_i(t)` is continuous
  and nondecreasing. Its threshold sublevel set is a closed initial interval. If
  its maximal endpoint `R_i` is less than `L`, continuity gives exact equality
  `A_i(R_i)=R_i−E`, including when the function has flat portions.
- For the two largest reaches `x≥y`, summing allocations at `y` gives
  `x+(n−2)y≥nE`. The stated identity then proves
  `(n−1)x+y≥n²E/(n−1)` because `n²−3n+1>0` for `n≥3`.
- Writing `M=max_{p≠q}(R_p+A_q(L))`, summation against the largest and second
  largest reaches directly gives
  `nM≥L+(n−1)x+y`. Thus the pair guarantee is valid without an assumption about
  independence or simultaneous attainability of different reach times.
- With `L=(n−1)T/n−E`, condition
  `nE/(n−1)+L/n≥L−E` is exactly
  `E≥(n−1)^3 T/[n(3n²−3n+1)]`, which is the stated geometric coefficient.
- Equal terminal masses make every positive discrepancy at most `T/n≤E`.
  Choosing three distinct modes prevents earlier occupation of the second and
  third modes. Their negative extremes therefore occur at their own block ends
  and are exactly the quantities bounded in the proof. A zero-length first block
  causes no difficulty and only reduces the switch count.
- The uniform lower bound applies because two switches permit at most three
  blocks and `n≥4`, exactly the range of the previously verified formula.

This confirms the restricted-class extremal theorem. It does not settle the
unrestricted-terminal-mass two-switch minimax problem or any finite-grid correction.
