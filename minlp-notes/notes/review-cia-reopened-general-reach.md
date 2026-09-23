# Independent review of the four-block-seeded general CIA bound

Date: 2026-09-07. Reviewer: independent `review_seeded` agent.
Status: passed; no mathematical correction required.

The later minimum-mass refinement and exact event-relaxation witness also pass
independent review; their additional audit appears below. The clipping discussion
in the initial audit concerns the earlier maximum-mass proof, not a necessary
limitation of the recurrence itself.

Reviewed [the derivation](cia-reopened-general-reach.md),
[the author checker](../code/cia_reopened/general_reach_research.py), and their
four-block reach, mode-removal, and universal heavy-mode dependencies. The new
coefficient is a valid universal one-sided upper bound, its full-error transfer
is valid, and the newly certified value is `F_(16,4)(T)=T/6`. The result remains
dependent on the existing computer-assisted four-block theorem. This review is
not external peer review and makes no publication-priority determination.

## Seed and inductive construction

For `n>k>=4`, the seed dimension is `m=n-k+4>=5`. Thus the exact four-block
theorem applies to every seed instance, including measurable profiles generated
by completing a removed mode's allocation and restricting to a shorter horizon.
The seed permits at most four distinct modes. Each mode-removal step appends a
mode excluded from the child, so after `n-m=k-4` steps there are at most `k`
distinct activation blocks.

The exact seed `L_(m,4)` falls below `1/m` for `m=5,6`; it exceeds `1/m` for
every `m>=7`. Indeed this comparison is equivalent to comparing
`2(1-1/m)^4` with one, and the expression is strictly increasing in `m`.
Replacing the seed by `max{1/m,L_(m,4)}` weakens an available bound and is valid.
Using the unclipped seed in the published mode-removal argument would be invalid.

To check the recurrence independently, let the child dimension be `j-1`, its
valid coefficient be `c>=1/(j-1)`, and let `a>=T/j` be the largest terminal mass.
Put

```
E/T = [(j-1)^2 c+1]/[j(j-1)(1+c)].
```

This gives `E>=T/j`. If `a>=T-E`, constant use of that mode suffices, including
equality. Otherwise `L=T-a-E>0`, and `E'=E-a/(j-1)>0` because
`a<T-E<=(j-1)E`. Completing the other rates by `alpha_q/(j-1)` produces a valid
simplex profile. Its child schedule has error at most `cL<=E'`: the necessary
inequality has coefficient `1/(j-1)-c<=0` on `a`, so substituting the lower
bound `a>=T/j` has the correct direction. Returning to original rates adds at
most `a/(j-1)`, and appending the removed mode ends at discrepancy exactly `E`.
These arguments preserve both the coefficient hypothesis and distinctness.
The zero-horizon case is trivial.

## Closed form and strict comparison

For `D_j=j c_j`, the recurrence is

```
D_j = [(j-1)D_(j-1)+1]/[j-1+D_(j-1)].
```

Applying `(D-1)/(D+1)` gives the factor `(j-2)/j`. The clipped seed transform
is exactly `max{0,2((m-1)/m)^4-1}`. Multiplication over `j=m+1,...,n` gives
`m(m-1)/[n(n-1)]`, with the empty product equal to one when `k=4`.
Inverting proves the displayed closed formula. Its transform lies in `[0,1)`,
so no denominator vanishes and every resulting coefficient is at least `1/j`.

The old coefficient follows the same recurrence from its old four-block seed.
Direct factorization gives

```
C_(m,4)-1/m = (m-4)(m-5)/[2m(2m-5)],
C_(m,4)-L_(m,4)
  = (10m^2-5m+1)/[2(2m-5)(2m-1)(2m^2-2m+1)].
```

The second difference is strictly positive for every `m>=5`. The first is zero
at `m=5` and strictly positive for every `m>=6`. Thus clipping leaves equality
with the old seed only at `m=5`. The recurrence derivative is
`(j-2)/[(j-1)(1+c)^2]>0`, so strict improvement occurs exactly when
`m>=6`, equivalently `n>=k+2`, throughout the stated domain.
The full-error maximum may remain unchanged at `1/(k+1)`; the note correctly
does not claim a strict full-error improvement everywhere.

## Full-error transfer and the new exact case

Set `E=T max{1/(k+1),tilde C_(n,k)}`. If some terminal mass exceeds `E`, then
`T<=(k+1)E` and the heavy-mode theorem with `s=k-1` supplies the full-error
schedule. Otherwise every positive discrepancy `A_i-W_i` is at most its terminal
mass, hence at most `E`, while the seeded construction controls `W_i-A_i`.
This covers all profiles, including equality at the terminal-mass threshold.

Exact arithmetic gives

```
tilde C_(16,5) = 588449/3544816 < 1/6,
C_(16,5) = 35/208 > 1/6,
tilde C_(17,5) > 1/6.
```

Six successive pure modes of length `T/6` give a lower bound even when a
five-block schedule can repeat modes: it can use at most five of these six
modes, and an omitted mode accumulates mass `T/6`. The other ten relaxed modes
may have zero mass. The matching upper bound therefore proves the claimed
16-mode, four-switch equality. Failure of this upper bound to reach `1/6` at
17 modes makes no assertion about the true value there.

## Asymptotics checked analytically

For fixed `k`, clipping is inactive once `n` is large. With `m=n-k+4`, the
numerator of the transform can be written exactly as

```
m(m-1)[2(1-1/m)^4-1]
  = m^2-9m+20-20/m+10/m^2-2/m^3.
```

Expansion after division by `n(n-1)` gives

```
theta = 1-2k/n+k(k-1)/n^2+(k^2-k-20)/n^3+O_k(n^-4).
```

Since `tilde C=2/[n(1-theta)]-1/n`, inversion gives

```
tilde C = 1/k-(k+1)/(2kn)
          +[(k^2-1)/(4k)-10/k^2]/n^2+O_k(n^-3).
```

Subtracting the established uniform coefficient's second-order term
`(k^2-1)/(12k)` gives `(k^3-k-60)/(6k^2)`. At `k=4` this is zero, as expected:
the coefficient is the exact four-block seed for all sufficiently large `n`.
At `k=5` the gap coefficient is `2/5`, compared with the old `4/5`.
These are fixed-`k` expansions of explicit bounds, not an assertion that the
unknown minimax has a particular second-order coefficient.

The extension to another proved seed budget `ell` uses the same calculation
with `m=n-k+ell` and exponent `ell`, retaining the clipping and the hypotheses
of whichever seed theorem is used. It does not authorize use of an unproved
uniform-input conjecture as a seed.

## Reproducible checks

The independently written
[checker](../code/cia_reopened/check_seeded_review.py) imports no author code and
uses only standard-library exact rational arithmetic. It clears denominators
in the closed form, evaluates the recurrence through the alternative `D`
transform, and independently expands the original expression as formal power
series. The command

```
python code/cia_reopened/check_seeded_review.py
```

passes 3,900 coefficient cases and 97 formal-series cases, plus exact plateau
and clipping-boundary checks. The finite series checks supplement the all-`k`
analytic expansion above. The checker refuses Python's `-O` mode.

The author checker also passes its 6,786 cases. Finally,
`python code/cia-distinct-reach/verify_general_four_block.py` passes all 179
finite integer certificates and all ten polynomial certificates. The existing
independent reviews of the base theorems cover the underlying measurable-control
and certificate-model arguments; this review checked their hypotheses at each
new use. Numerical checks alone are not the justification of the new universal
bound.

## Additional audit: removing clipping by minimum-mass removal

The appended unrestricted transfer lemma is correct for `n>=3` and `C>0`.
For `C>=1/(n-1)` the preceding maximum-mass argument applies. For
`0<C<1/(n-1)`, normalize `T=1` and select a minimum-mass mode, so `0<=a<=1/n`.
The transfer map is strictly increasing in `C`; its values at `C=0` and
`C=1/(n-1)` are `1/[n(n-1)]` and `1/n`. Therefore the selected coefficient
strictly satisfies

```
1/[n(n-1)] < E < 1/n.
```

It follows that `L=1-a-E>1-2/n>0` and
`E'=E-a/(n-1)>=E-1/[n(n-1)]>0`. Also `L<1`. The condition `CL<=E'` is
equivalent to the same scalar inequality as before; now the coefficient of
`a` is positive, so the upper bound `a<=1/n` gives the needed inequality.
The completed profile, cumulative discrepancy comparison, final appended mode,
and distinctness arguments do not otherwise use maximality. The proof is thus
valid without clipping, including a minimum mode with zero mass.

The unclipped seed transform lies strictly in `(-1,1)`. Multiplication by
`(j-2)/j` preserves this interval, so the resulting coefficient is positive
at every stage and all transfer hypotheses persist. The coefficient can remain
below the reciprocal mode count; this now invokes the valid minimum-mass branch
instead of violating a hypothesis. At equality the maximum-mass proof applies.

Consequently the unclipped coefficient `C*` is a valid stronger one-sided bound.
It is strictly smaller than the clipped bound exactly when `m=5,6`, or
`n=k+1,k+2`. Because the exact four-block seed is strictly below the old seed
even at `m=5`, `C*` is strictly below the old general coefficient for **every**
`n>k>=4`. In those two newly improved dimensions the full-error bound remains
`T/(k+1)`, as the author correctly states. The 16-mode plateau and fixed-`k`
asymptotic coefficients are unchanged.

The independent checker now also evaluates unclipped recurrences on all 3,900
coefficient cases and verifies 768 exact minimum-branch scalar cases, including
zero minimum mass and maximal allowed minimum mass. These computations confirm
the implementation and supplement the universal argument above.

## Additional audit: the nonphysical weighted-event witness

The stated event relaxation is a necessary condition for uncapped physical
reach events with the prescribed maximizers. Available-set and block-count
inclusion imply event-time order, and hence componentwise allocation order.
Each event time is at least each available first reach, giving
`a_(h,U,i)>=R_i-1`. At a maximum pair endpoint, appending an available second
mode gives `t-a_i>=R_j+1`; at a triple endpoint, the corresponding condition
uses the best pair that excludes the appended mode. A maximizing pair or triple
remains available in every set containing it, so its event has the global time
and allocations. The root minimum and root-sum conditions follow from the same
first-reach argument used in the four-block theorem.

I independently parsed the saved rational values and checked these conditions
directly, without importing the author's LP row builder. There are 42 pair
events (available-set sizes 3 through 6) and 22 triple events (sizes 4 through
6), giving 454 variables. All 3,660 stated inequalities, all 64 mass equalities,
and variable nonnegativity pass. The aggregate objective is exactly
`40328/387`, strictly below `4nB_3=13104/125`.

The same independent checker verifies that the `{0,2,3}` pair event occurs at
`1658/645`, before the `{2,3,4,5}` pair event at `614/215`, but their mode-2
allocations are respectively `239/645` and `47/129`, in decreasing order.
This is impossible for one cumulative control. Thus the point refutes the
desired implication from the recorded relaxation, while furnishing no
counterexample to the physical CIA inequality. Additional chronological order
constraints are necessary to exclude this point; their sufficiency is unproved.
The author states this scope correctly.
