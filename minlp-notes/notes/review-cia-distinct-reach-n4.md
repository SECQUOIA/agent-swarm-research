# Independent review: four-mode, three-distinct-block reach certificate

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: `notes/cia-distinct-reach-investigation.md`,
`code/cia-distinct-reach/verify_n4.py`, and `certificates_n4.json` in that directory.

## Verdict

The computer-assisted proof is valid. It establishes, for every measurable
four-component simplex-valued control on `[0,L]` and every `E>0`,

```
max_(i,j,k distinct) F_k(F_j(F_i(0))) ≥ min(L,148E/27),
F_i(t)=max{s∈[0,L]:s−A_i(s)≤t+E}.
```

The finite LPs encode necessary conditions for arbitrary measurable controls;
they do not assume a temporal grid or rely on approximate optimization results.
All thirty rational dual certificates passed both the supplied checker and an
independent semantic reconstruction described below. This is a proof audit,
not a literature novelty determination.

## Reach operators, saturation, and plateaus

For simplex-valued measurable controls, `A_i` and `H_i(t)=t−A_i(t)` are continuous
and nondecreasing, and `Σ_i H_i(t)=3t`. Their absolute continuity is sufficient;
no strict monotonicity is needed. Since `H_i(0)=0` and thresholds are positive,
each reach set is nonempty and compact, so its maximum exists.

If a reach is strictly below the horizon, continuity forces equality at its
threshold. A strictly smaller value of `H_i` at the maximizing time would permit
a larger feasible time. Flat portions at a threshold are handled by taking the
last feasible time. Thus every unsaturated first reach satisfies
`H_i(R_i)=E`, and every unsaturated two-block reach satisfies its corresponding
threshold equality. Reach operators are nondecreasing in their argument, even
when their inverses have jumps.

Rescale time by `E` to reduce to `E=1`. Restricting the horizon to
`T=min(L,148/27)` can only decrease each reach operator. Monotonicity then implies
that each composed restricted reach is at most its original counterpart. Proving
reach of this restricted horizon is therefore sufficient.

For `M_i` defined as the largest two-block reach using distinct modes other than
`i`, the maximum is over finitely many pairs and is attained. If a first reach or
an `M_i` reaches `T`, a schedule of at most three distinct selections already
reaches the target. Additional distinct modes, if desired, have zero-length
terminal blocks. In the remaining case all first and pair reaches are unsaturated.

For all distinct `i,j,k`, monotonicity gives

```
H_k(M_i) ≥ H_k(F_k(R_j)) = R_j+1.
```

This is a valid necessary inequality even though the pair attaining `M_i` may
differ from `(j,k)`. It is not an equality assumption about every pair.

## Exhaustive event-order coverage

Relabel modes so `R_3≤R_2≤R_1≤R_0`. Since `H_k(s)≤s`, the preceding necessary
inequality implies `M_i≥R_j+1` for every `j≠i`, choosing any third distinct mode
as `k`. Thus `M_1,M_2,M_3` occur strictly after `R_0`, and `M_0` occurs strictly
after `R_1`.

There are therefore exactly two types of compatible order:

1. All four `R` events first, followed by any permutation of the four `M` events:
   24 cases.
2. `M_0` between `R_1` and `R_0`, followed by any permutation of the other three
   `M` events: 6 cases.

Ties between first reaches can be resolved by relabeling. A tie between `M_0`
and `R_0` can be placed in either compatible type, and ties among `M` events can
be ordered arbitrarily. The LP constraints use non-strict monotonicity, so these
representatives retain all tied profiles. No other interleaving is possible.

As an independent finite check, I enumerated all `8!` permutations of the labeled
events, retained the linear extensions of these ordering requirements, and
obtained exactly the same thirty orders as the certificate list.

## Why the LP constraints apply to every control

At each ordered event introduce its time and its four cumulative allocations.
All forty quantities are nonnegative. The eight total-mass equalities are
`Σ_i a_(v,i)=t_v`, and the twenty-eight consecutive monotonicity inequalities
are `a_(v,i)≤a_(v+1,i)`. Summing the latter implies nondecreasing event times.
The total-mass equalities also imply that an individual cumulative increment
cannot exceed the corresponding time increment. Thus omitting explicit time-order
and 1-Lipschitz inequalities does not weaken the necessary-condition argument
in an invalid direction.

The four first-reach equalities are exactly `t_(R_i)−a_(R_i,i)=1`.
The twenty-four other reach inequalities are

```
t_(R_j)−t_(M_i)+a_(M_i,k) ≤ −1,
```

over all distinct triples. They are precisely the valid inequalities derived
above. In total there are twelve equalities and fifty-two inequalities.

No upper horizon bounds are imposed in these programs; dropping them only enlarges
the feasible region and remains legitimate for a lower-bound certificate.
Likewise, the programs do not impose exact maximality of all reaches or equality
among some `M_i` values. Such omissions are relaxations, not unjustified assumptions.
Only the forward implication from an actual control to an LP point is used.

## Matrix-generation and dual-certificate audit

I checked the supplied program generator against the preceding semantic constraints.
It assigns five columns per event, with time first and four allocations afterward.
The first eight equality rows are total mass, followed by the four first-reach
rows. Inequality rows consist of the twenty-eight monotonicity rows followed by
all twenty-four ordered distinct-triple reach rows. The objective places a one
on each of the four `M` time columns and zero elsewhere. No row assignment has
an accidental overlapping index or reversed sign.

For a minimization program with `Ax≤b`, `Bx=d`, and `x≥0`, the certificate uses
`y≤0`, arbitrary equality multiplier `z`, and residual
`c−Aᵀy−Bᵀz≥0`. Multiplication reverses the inequality in the correct direction:
`yᵀAx≥yᵀb`. Therefore every feasible point satisfies
`cᵀx≥yᵀb+zᵀd`. All arithmetic in the checker uses exact `Fraction` values.
The certificate data contain rational strings, and the checker verifies every
sign and all forty residual coordinates.

The supplied normal command passed all thirty cases. Independently, I rebuilt
every row using semantic variable keys `(event,coordinate)`, without importing
the supplied generator, and accumulated each stored dual functional directly.
I checked the multiplier signs, every objective coefficient residual, and the
claimed rational constant in all thirty cases. The outcome was:

```
Independent semantic check: exactly 30 linear extensions;
all 30 rational dual identities valid.
```

The twenty-four regular cases certify `Σ_i M_i≥112/9`; the six exceptional cases
certify `Σ_i M_i≥43/3>112/9`. These lower bounds suffice; exact primal attainment
of the LP bounds is not needed for the reach theorem.

I noted that Python's `-O` flag disables assertions. The author added an explicit
runtime guard rejecting optimized Python execution, so the checker cannot now
print successful verification after its assertions have been disabled. The
documented ordinary command already performed all checks correctly.

## The final three-block implication

Suppose every three-distinct-mode reach were below `T`. A pair excluding `i`
attains `M_i`; appending mode `i` therefore shows `F_i(M_i)<T`. Consequently

```
H_i(T)>M_i+1.
```

This inequality is strict: if `H_i(T)≤M_i+1`, the horizon itself would be feasible
in the definition of `F_i(M_i)`. Summing gives

```
Σ_i M_i < 3T−4 ≤ 3(148/27)−4 =112/9,
```

contradicting the certified aggregate lower bound. The proof works unchanged
when the restricted horizon is smaller than `148/27`. Reversing the time scaling
proves the stated result for every `E>0`.

For constant uniform controls, `H_i(t)=3t/4` and the uncapped successive reaches
are exactly `4E/3`, `28E/9`, and `148E/27`. Thus the constant is sharp whenever
the horizon is at least the third value.

This lemma concerns the reach constraints for negative discrepancies of modes
used in distinct blocks. A full CIA error bound must also control positive
cumulative discrepancies; that additional conclusion should not be inferred
from the reach lemma alone. No general-`n` or general-block-count theorem is
proved by these thirty certificates.

## Independent review of the later three-mode boundary counterexample

The subsequently appended `n=3,k=3` counterexample in
`notes/cia-distinct-reach-investigation.md` is correct. I checked its rational
knot table directly, independently of the inverse-composition script.
Every cumulative increment is nonnegative, the increments sum to the elapsed
time, and each individual slope is at most `3/4`. Extending by the uniform
control to `L=57/8` preserves these properties. Thus each `H_i` is strictly
increasing, with slope at least `1/4`, and no plateau ambiguity remains.

In units of `1/146`, the first-reach identities are

```
256−110=146,   194−48=146,   146−0=146.
```

They give `R=(128/73,97/73,1)`. At the three two-block times, the two possible
orders excluding each mode have the required identities:

```
M_0: 408−68=340=146(R_1+1),
     408−116=292=146(R_2+1);
M_1: 516−114=402=146(R_0+1),
     516−224=292=146(R_2+1);
M_2: 580−178=402=146(R_0+1),
     580−240=340=146(R_1+1).
```

Therefore `M=(204/73,258/73,290/73)` exactly. Finally, at `t*=971/146`,

```
971−417=554=146(M_0+1),
971−309=662=146(M_1+1),
971−245=726=146(M_2+1).
```

Strict increase of every `H_i` proves that all six distinct triples end exactly
at this final knot. Since `57/8−971/146=277/584>0`, the example strictly defeats
the uniform three-block reach when three modes must provide all three distinct
blocks.

The standard-library exact script also ran successfully and printed the six
identical final reaches. I requested that it assert the displayed first and
pair identities explicitly, and use equality for each final reach, to match
the stronger verification description in the note; its original inequality
check was already sufficient to establish the counterexample.

This negative result is compatible with the proved four-mode lemma. It does not
refute a conjecture restricted to `k≤n−1`, and it is not a counterexample to an
equal-total CIA theorem. In particular, the valid inverse calculations rely on
the actual strictly increasing cumulative functions supplied by the table,
not merely on a feasible event-data LP.
