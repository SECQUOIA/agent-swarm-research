# Reopened general-switch investigation: propagating exact small-block results

Date: 2026-09-07. Status: analytic derivation, exact coefficient checks, and
[independent review](review-cia-reopened-general-reach.md) complete, including the
unclipped transfer refinement and the negative relaxation certificate. This note does **not** prove the arbitrary-block
uniform-input conjecture. It records a useful consequence of combining existing
results that was absent from the earlier general bound.

The first derivation below retains a conservative clipped seed. The later
unclipped refinement is stronger and is the final bound presented in the
[result statement](../results/cia-seeded-arbitrary-switch-bound.md).

## A stronger upper bound for every larger block budget

Let `k` be the allowed activation-block count, `n>k>=4`, and put

\[
 m=n-k+4,\qquad
 \theta_{n,k}=\frac{m(m-1)}{n(n-1)}
 \max\left\{0,2\left(\frac{m-1}{m}\right)^4-1\right\},
 \qquad
 \widetilde C_{n,k}=\frac{1+\theta_{n,k}}{n(1-\theta_{n,k})}.
\]

Then every measurable relaxed profile has a schedule with at most `k` distinct
activation blocks and one-sided cumulative error at most
`tilde C_{n,k} T`. Consequently its full cumulative error can be bounded by

\[
 \boxed{F_{n,k-1}(T)\le T\max\{1/(k+1),\widetilde C_{n,k}\}.} \tag{1}
\]

This is a strictly smaller one-sided coefficient than the earlier general
coefficient `C_{n,k}` whenever `n>=k+2`. The full bound is strictly better when
its maximum with the omitted-mode lower threshold changes. The coefficient
matches the earlier one at `n=k+1`; both full bounds are then exact.

The four-block input uses the existing exact computer-assisted theorem. This new
transfer does not replace its certificate dependency with an analytic proof.

### Proof

The exact [four-block reach theorem](../results/cia-general-four-block-reach.md)
provides the one-sided coefficient

\[
 L_{m,4}=\frac1{m[(m/(m-1))^4-1]},\qquad m\ge5.
\]

Seed the existing [mode-removal recurrence](../results/cia-arbitrary-block-one-sided-bound.md)
with

\[
 c_m=\max\{1/m,L_{m,4}\}.
\]

The clipping at `1/m` is required by the existing maximum-mass proof: that
version assumes its input coefficient is at least the reciprocal of the input
mode count. A refinement proved at the end of this note removes this restriction
by changing the selected mode below the threshold. For `m=5,6` the exact
four-block coefficient is smaller than `1/m`. Using it without clipping would
invalidate the maximum-terminal-mass step of that proof.

The recurrence is

\[
 c_j=\frac{(j-1)^2c_{j-1}+1}{j(j-1)(1+c_{j-1})}
 \qquad (j=m+1,\ldots,n).
\]

Each step increases both the mode count and allowed block count by one. Thus
`n-m=k-4` steps produce a `k`-block schedule. Under
`eta_j=(j c_j-1)/(j c_j+1)`, direct algebra gives

\[
 \eta_j=\frac{j-2}{j}\eta_{j-1},\qquad
 \eta_m=\max\{0,2((m-1)/m)^4-1\}.
\]

The product telescopes to `theta_{n,k}`. Inverting the transform yields the
claimed coefficient. Since `0<=theta_{n,k}<1`, all denominators are positive
and every recurrence input satisfies its required lower bound. Every induction
step appends a previously unused mode, so distinctness is preserved.

The [universal heavy-mode theorem](../results/cia-universal-heavy-mode-rounding.md)
transfers this one-sided guarantee to (1): at the displayed full threshold,
heavy profiles are rounded by that theorem; otherwise every positive discrepancy
is already bounded by the terminal mass of its mode.

For comparison, the earlier general coefficient is exactly this same recurrence
seeded with its old four-block bound. At `m=5` that seed equals `1/m`. At every
`m>=6`, both `1/m` and `L_{m,4}` are strictly smaller than the old four-block
coefficient. The first inequality follows directly from the old formula; the
second follows from

\[
 C_{m,4}-L_{m,4}
 =\frac{10m^2-5m+1}
 {2(2m-5)(2m-1)(2m^2-2m+1)}>0.
\]

The recurrence is strictly increasing in its input because its derivative is
`(j-2)/[(j-1)(1+c)^2]>0`. Thus improvement propagates to every larger mode and
block count.

## A newly certified four-switch case

At `n=16,k=5` the coefficients are

\[
 \widetilde C_{16,5}=\frac{588449}{3544816}<\frac16,
 \qquad C_{16,5}=\frac{35}{208}>\frac16.
\]

Together with the existing six-pure-mode omitted-mode lower example, (1) gives

\[
 \boxed{F_{16,4}(T)=T/6.}
\]

The earlier general plateau covered only `n=6,...,15` for four switches. The new
bound certifies `n=16` as well. At `n=17` the new coefficient exceeds `1/6`, so
this particular improvement does not certify another plateau dimension there.
This is a modest exact advance; it does not resolve the five-block one-sided law.

## A smaller asymptotic gap

For fixed `k>=4`, as `n` tends to infinity,

\[
 \widetilde C_{n,k}
 =\frac1k-\frac{k+1}{2kn}
 +\left(\frac{k^2-1}{4k}-\frac{10}{k^2}\right)\frac1{n^2}
 +O_k(n^{-3}).
\]

Subtracting the uniform-input lower coefficient gives

\[
 \widetilde C_{n,k}-L_{n,k}
 =\frac{k^3-k-60}{6k^2n^2}+O_k(n^{-3}).
\]

For `k=5` this halves the leading bound gap from `4/(5n^2)` to `2/(5n^2)`.
The leading and first mode-count correction remain unchanged. This is a
quantitative tightening, not a sharp second-order asymptotic theorem.

More generally, any exact `ell`-block one-sided result can seed the same
construction, replacing `4` by `ell`. The expression becomes
`m=n-k+ell` and the exponent becomes `ell`. This observation allows later exact
reach advances to strengthen all larger budgets immediately. Only already proved
seed budgets may be used in a theorem.

## Verification and limits

`python code/cia_reopened/general_reach_research.py` checks 6,786 exact-rational
coefficient cases with `5<=n<=120`, compares direct recurrence evaluation with the
closed form, checks the recurrence hypothesis at every step, compares the old
upper and uniform lower coefficients, and verifies the new `n=16,k=5` plateau.
These checks verify algebraic implementation, not the arbitrary measurable-input
construction: the proof above and its existing dependencies justify that part.

The existing topic literature audit remains the literature basis for the two
inputs. No independent novelty claim is made for a new application of their
recurrence; this is a consequence useful for the eventual paper. The general
weighted three-block exclusion inequality needed for a sharp five-block reach
law remains open. No numerical evidence has been elevated to a theorem.

## Exact negative result for a natural five-block proof relaxation

A direct extension of the earlier pair-event LP is insufficient to establish the
next weighted inequality. This statement is about a proof relaxation, **not** a
counterexample to the CIA conjecture.

Fix `n=6`, `E=1`, and `S={0,1,2,3}`. Introduce first reaches `R_i`; a pair event
`(2,U)` for each available set `U` of size at least three; and a triple event
`(3,U)` for each `U` of size at least four. At each event store a time `t_{h,U}`
and six nonnegative allocations `a_{h,U,i}`. The recorded relaxation imposes:

- `R_i>=1`, `R_0<=R_i`, and `sum_{i!=0} R_i>=6`.
- Mass conservation `sum_i a_{h,U,i}=t_{h,U}`.
- Available-first-root monotonicity `a_{h,U,i}>=R_i-1` for `i in U`.
- Pair endpoint inequalities `t_{2,U}-a_{2,U,i}>=R_j+1` for distinct `i,j in U`.
- Triple endpoint inequalities
  `t_{3,U}-a_{3,U,i}>=t_{2,U\{i}}+1` for `i in U`.
- Allocation monotonicity from `(h,U)` to `(h',U')` whenever `h<=h'` and `U subset U'`.
- All pair events whose available sets contain `{0,1}` equal the global pair
  event; all triple events containing `{0,1,2}` equal the global triple event.
  These express prescribed globally maximizing pair and triple mode sets.

All these constraints are necessary for actual uncapped reach events with those
maximizers. The proposed aggregate objective is

\[
 H_S=\sum_{i\in S}\left(t_{3,[6]\setminus\{i\}}+
          \sum_{j\ne i}t_{3,[6]\setminus\{i,j\}}\right).
\]

The [saved rational witness](../code/cia_reopened/general_reach_relaxation_witness.json)
satisfies all 3,660 inequalities and 64 equalities, with 454 nonnegative variables,
but has

\[
 H_S=\frac{40328}{387}<\frac{13104}{125}=4nB_3.
\]

The standalone standard-library checker is the same command used above:

```
python code/cia_reopened/general_reach_research.py
```

A floating-point LP located the point; the saved fractions satisfy every row
exactly, so numerical optimization is not trusted by the check. No dual optimum
certificate is needed: any feasible point below the target suffices to refute the
implication from this relaxation.

The point is demonstrably not generated by a common cumulative control. Its pair
event for available modes `{0,2,3}` occurs at `1658/645`, and its pair event for
`{2,3,4,5}` occurs later, at `614/215`. Yet mode 2 allocation decreases from
`239/645` to `47/129`. Thus monotonicity between chronologically ordered,
incomparable events is missing. This explicitly identifies additional information
needed by this event-LP approach. It does not show that merely adding these
orders will suffice, and it does not disprove the desired weighted inequality.

## Further transfer improvement: minimum-mass removal below the reciprocal threshold

The clipping used above can be removed by extending the recurrence itself. The
following short argument is independent of the weighted-event investigation.
It is recorded separately so the earlier, more conservative bound remains easy
to audit.

**Unrestricted transfer lemma.** Suppose every `(n-1)`-mode profile admits a
one-sided error bound `C T` with at most `k-1` distinct blocks, where `C>0` and
`n>=3`. Then every `n`-mode profile admits a bound

\[
 E=\frac{(n-1)^2C+1}{n(n-1)(1+C)}T
\]

with at most `k` distinct blocks. No condition `C>=1/(n-1)` is needed.

For `C>=1/(n-1)`, use the established maximum-mass removal proof. For
`0<C<1/(n-1)`, choose instead a mode `q` with **minimum** terminal mass
`a=A_q(T)<=T/n`. The displayed coefficient has

\[
 \frac{T}{n(n-1)}<E<\frac Tn.
\]

Consequently `L=T-a-E>0` and `E'=E-a/(n-1)>0`. Complete the other rates by
`alpha_hat_i=alpha_i+alpha_q/(n-1)` and apply the input guarantee on `[0,L]`.
The required inequality `CL<=E'` is equivalent to

\[
 E\ge\frac{CT+(1/(n-1)-C)a}{1+C}.
\]

Here the right side is increasing in `a`. Its maximum over `a<=T/n` is exactly
the selected `E`. Thus the prefix error against the original rates is at most
`E'+A_q(t)/(n-1)<=E`. Appending mode `q` on `[L,T]` ends with one-sided discrepancy
exactly `E`; this discrepancy is nondecreasing during its block. All other
one-sided discrepancies are nonincreasing after `L`. Distinctness is preserved.
This proves the additional case.

Using the exact four-block input directly therefore gives the same formulas
above with

\[
 \theta^*_{n,k}=\frac{m(m-1)}{n(n-1)}
 \left[2\left(\frac{m-1}{m}\right)^4-1\right],
 \qquad m=n-k+4,
\]

and **no maximum with zero**. Since the seed transform lies strictly between
`-1` and `1` and its multiplicative factor lies in `(0,1]`, all denominator and
positivity conditions hold. Write `C^*_{n,k}=(1+theta^*)/[n(1-theta^*)]`.
This strengthens the clipped coefficient only at `m=5,6` (`n=k+1,k+2`);
there the full two-sided bound is already determined by the plateau. The earlier
new plateau at `(n,k)=(16,5)` and its asymptotic improvement are unchanged.
The unrestricted transfer lemma is useful for applying future seed results even
when their one-sided discrepancy is below reciprocal mode count.
