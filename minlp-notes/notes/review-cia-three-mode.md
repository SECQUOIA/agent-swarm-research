# Independent review: exact finite-grid CIA results

Date: 2026-09-04. Reviewed files:
[`cia-exact-three-mode-one-switch.md`](../results/cia-exact-three-mode-one-switch.md)
and the final three-interval section of
[`cia-uniform-switching-obstruction.md`](../results/cia-uniform-switching-obstruction.md).
This is an independent agent review, not external peer review.

**Verdict:** Both new formulas are mathematically correct under the stated convention
of at most one switch and free initial activation. The proofs cover arbitrary relaxed
simplex columns and all integer schedules, including constants. No correction to either
statement or proof is required. Novelty relative to later literature is a separate question.
The previous continuous theorem and five-mode counterexample remain independently
verified in [`review-cia.md`](review-cia.md).

## Exact three-mode formula

For `N≥2`, the claimed worst-case value is

```
F_3(3k)=k,
F_3(3k+1)=k+1/2  (k≥1),
F_3(3k+2)=k+3/4  (k≥0).
```

For `N=1`, choosing the component of largest relaxed value gives error at most `2/3`,
and the uniform relaxed column attains it. Thus the stated separate value is correct.

The schedule error identity used by the proof is exact. Write `A_i(t)` for cumulative
relaxed allocation and `m_i=A_i(N)`. If distinct modes `p,q` are selected before and
after integer switch time `τ`, with third mode `h` omitted, then

```
D(p,q,τ)=max{m_h,τ−A_p(τ),N−m_q−τ}.                 (1)
```

For completeness, the first selected component decreases until the switch and then
increases. Its negative extreme is `τ−A_p(τ)`; its positive final value is at most
`N−m_q−τ`. The second selected component increases until the switch and decreases
afterwards. Its positive switch value is at most `τ−A_p(τ)`; its negative final
value is `N−m_q−τ`. The omitted component is nondecreasing with final value `m_h`.
This accounts for every prefix. The identity also handles `τ=0,N`, hence constant
schedules. It does not require the relaxed data to be constant in time.

For `N=3k`, let `q` have largest total and `p` second largest, and switch at `k`.
Then `m_h≤k`, `k−A_p(k)≤k`, and `N−m_q−k≤k`. The upper bound follows.
Equal totals `k` force every schedule to omit a mass of `k`, giving sharpness.

## Check of the two other residues

Set `L=k+1`, and set `E=k+1/2` for `N=3k+1` or `E=k+3/4` for `N=3k+2`.
The six inequalities used by the author have the following nonnegative slacks:

| Inequality | Slack for `N=3k+1` | Slack for `N=3k+2` |
|---|---:|---:|
| `E≥N/3` | `1/6` | `1/12` |
| `2E≥N−L` | `1` | `1/2` |
| `4E≥N+L` | `0` | `0` |
| `E+L≥2N/3` | `5/6` | `5/12` |
| `3E≥2L` | `k−1/2` | `k+1/4` |
| `3E+k+2L≥2N` | `3/2` | `1/4` |

Thus all hold in exactly the asserted ranges. In particular the `k=0` case in
`N=3k+2` is valid; the excluded `N=1` case would violate `3E≥2L` with `E=1/2`.

Because `3E≥N`, there cannot be three totals strictly greater than `E`.
If exactly two are greater, choose these modes. Their cumulative sum at `L` is
at least `L−m_h>L−N+2E≥2(L−E)`. At least one can therefore be the first selected
mode with `A_p(L)≥L−E`. The omitted mass is below `E`, and the second selected
mode has final negative error below `N−E−L≤E`. Equation (1) proves the claim.

Otherwise, at most one total exceeds `E`. Let `q` have largest total and `r` second
largest. Every pair `p→q`, and the pair `q→r`, omits a mass at most `E`.

If `m_q≥N−E−k`, switch from `r` to `q` at `k`. Its first negative error is at most
`k≤E`, and its final negative error is at most `E`.

Otherwise `m_q<N−E−k`. At switch time `L`, every pair `p→q` already has final
negative error at most `E`, because `m_q≥N/3` and `E+L≥2N/3`. If either potential
first mode has cumulative allocation at least `L−E`, that pair works.

If both other cumulative allocations are strictly less than `L−E`, then
`A_q(L)>2E−L≥L−E`. Moreover,

```
m_r ≥ (N−m_q)/2 > (E+k)/2 ≥ N−E−L.
```

The last inequality is equivalent to `3E+k+2L≥2N`, checked above. Therefore the
pair `q→r`, switching at `L`, works. The construction exhausts every possible case
for the relaxed totals and cumulative allocations. Equality cases cause no gap:
using strict `>E` for the mass classification leaves all omitted masses admissible,
and success tests use non-strict `≥L−E`.

## Matching inputs cover all competitors

For `N=3k+1`, the proposed input consists of `k` pure third-mode intervals, one
`(1/2,1/2,0)` interval, then `k` pure intervals for each large mode. Its length is
`3k+1`; both large-mode totals are `E=k+1/2`. At `L`, each has prefix `1/2=L−E`.
For `N=3k+2`, the input consists of `k` pure third-mode intervals, one
`(1/4,1/4,1/2)` interval, `k` pure intervals for each large mode, and one final
`(1/2,1/2,0)` interval. Its length is `3k+2`; both large-mode totals are
`E=k+3/4`, and their prefixes at `L` are `1/4=L−E`.

Any schedule omitting either large mode has error at least its total `E`. Any remaining
competitor must select exactly the two large modes, in either order. Because its switch
is at an integer, either `τ≤k` or `τ≥L=k+1`. In the first case the final negative
error is at least `N−E−k`, which equals `E` in the first residue and is `E+1/2` in
the second. In the second case the first mode's negative error is at least
`L−A_p(L)=E`, because `t−A_p(t)` is nondecreasing. Both orders satisfy the same
calculation. Constant schedules also omit a large mode. This proves the lower bound
against every competitor and establishes exactness.

The correction relative to `N/3` is respectively `0`, `1/6`, and `1/12`; the author's
arithmetic is correct. These exact values show that the conjectured additive half-grid
term is not an exact equality even in three modes. This is distinct from the stronger
seven-mode example below, which invalidates the proposed upper bound itself.

## Exact three-interval result for arbitrary mode count

For `N=3`, `n≥3`, the full worst-case value is `2−3/n`.
For arbitrary relaxed input, choose `q` with largest total and `p` with second largest,
and use `(p,q,q)`. All omitted totals are at most 1, since three totals greater than 1
cannot sum to 3. At the first prefix, every error is at most 1. At the second prefix,
both selected components have occupation 1 and relaxed cumulative value in `[0,2]`,
so their absolute errors are at most 1. At the final prefix, the first selected mode
has total at most `3/2` and occupation 1, giving error at most 1. The second has total
in `[3/n,3]` and occupation 2, giving error at most `max{1,2−3/n}=2−3/n`.
These observations also bound every omitted mode at every prefix.

Uniform relaxed data give the matching lower bound: every schedule with at most one
switch uses at most two modes, so some mode occupies at least two of the three intervals.
Its final negative error is at least `2−3/n`. Constants are included in this argument.

Thus `n=7,N=3,s=1` has exact value `11/7`, greater than the conjectured `3/2`.
The published condition `1≤s≤N−2` forces `N≥3`, so this counterexample has the
smallest permitted number of intervals. This does not claim that seven modes are the
smallest possible for a counterexample at every grid size; the five-mode family already
uses fewer modes with more intervals.

## Independent exact computational checks

A separate implementation used cumulative integer numerators for quarter-valued relaxed
columns, and evaluated every component at every prefix directly. It did not reuse the
schedule-error identity to evaluate constructed schedules.

- For all 54,225 relaxed arrays whose columns range over the 15 three-mode simplex
  points with coordinates in multiples of `1/4`, across `N=2,3,4`, the author's
  constructive upper-bound cases produced a schedule with at most one switch and
  error no greater than the stated exact bound.
- For each `N=2,...,100`, the proposed extremizer's error was minimized by enumerating
  all ordered pairs of distinct modes and all integer switch positions `0,...,N`.
  The resulting exact rational optimum agreed with the formula for every `N`.
- Independent enumeration of all seven-mode, three-interval schedules with at most
  one switch confirmed the exact uniform-input optimum `11/7`.

These checks support the symbolic proof and catch small-horizon edge cases. The
finite relaxed lattice enumeration is not used as a substitute for the universal
constructive upper-bound proof.
