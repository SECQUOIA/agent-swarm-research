# Distinct-mode reach: four modes and three blocks

Date: 2026-09-04. Status: a computer-assisted proof is complete and its rational certificates
pass an exact verifier. An independent mathematical review and independent semantic
reconstruction of all thirty certificates also passed; see
`notes/review-cia-distinct-reach-n4.md`. No claim is made for arbitrary `n,k` yet.

## The question and the proved candidate

Let `alpha:[0,L]->R_+^4` be measurable with `sum_i alpha_i=1` almost everywhere. Set
`A_i(t)=integral_0^t alpha_i(s)ds` and `H_i(t)=t-A_i(t)`. For `E>0`, define

```
F_i(t)=max { s in [0,L] : H_i(s)<=t+E }.
```

The maximum exists. Each `H_i` is continuous and nondecreasing, and `sum_i H_i(t)=3t`.
The proposed reach lemma is true for four modes and three distinct selections:

```
max_(i,j,k all distinct) F_k(F_j(F_i(0))) >= min{L,148E/27}.       (1)
```

Constant uniform controls attain equality when `L>=148E/27`: `H_i(t)=3t/4`, hence successive
uncapped reaches are `4E/3`, `28E/9`, and `148E/27`.

The proof below establishes a stronger intermediate inequality through thirty small rational
linear programs. The programs are relaxations of all possible measurable profiles, not a
time discretization of the control.

## Reduction to an aggregate two-block inequality

Scaling time by `E` reduces to `E=1`. It suffices to prove reach of
`T=min{L,148/27}` after restricting the control to `[0,T]`. Its truncated reach operators
cannot exceed the original ones.

Write

```
R_i=F_i(0),
M_i=max_(j,k distinct, j!=i, k!=i) F_k(R_j).
```

If any `R_i=T` or `M_i=T`, a sequence of at most three distinct modes reaches `T`, and the
result is immediate. In the remaining case every first and two-block reach is below `T`.
Continuity and the maximal-reach definition then imply

```
R_i-A_i(R_i)=1,                                             (2)
M_i-A_k(M_i)>=R_j+1    for all distinct i,j,k.               (3)
```

Indeed, `M_i>=F_k(R_j)` and `H_k(F_k(R_j))=R_j+1`. The needed aggregate inequality is

```
sum_i M_i >= 112/9.                                        (4)
```

If every three-distinct-mode sequence ended strictly before `T`, then `F_i(M_i)<T` for all
`i`, so `H_i(T)>M_i+1`. Summing would give

```
sum_i M_i < 3T-4 <= 3*(148/27)-4 =112/9,
```

contradicting (4). This argument also covers horizons smaller than `148/27`: failure to reach
the horizon would imply the same impossible inequality.

## Why only thirty event orders are needed

Relabel the modes as `0,1,2,3` so

```
R_3<=R_2<=R_1<=R_0.
```

Since `H_k(s)<=s`, (3) implies `M_i>=R_j+1` whenever `j!=i` (choose a third mode `k`).
Thus `M_1,M_2,M_3` all follow `R_0` strictly, while `M_0` follows `R_1` strictly. There are
only two possibilities, allowing arbitrary tie orders:

1. `R_3,R_2,R_1,R_0` followed by the four `M` events in any order: 24 cases.
2. `R_3,R_2,R_1,M_0,R_0` followed by `M_1,M_2,M_3` in any order: 6 cases.

Ties can be put in either compatible case. No other interleaving can arise. This finite
coverage is independent of the number of pieces of a control or any regularity beyond
measurability and simplex membership.

## The rational LP relaxation for one event order

For each of the eight chronologically ordered events `v`, introduce its time `t_v` and the
four cumulative values `a_(v,i)=A_i(t_v)`. There are forty nonnegative variables. Impose:

```
sum_i a_(v,i)=t_v                         for each event v;
a_(v,i)<=a_(v+1,i)                        for consecutive events and each i;
t_(R_i)-a_(R_i,i)=1                      for i=0,1,2,3;
t_(R_j)-t_(M_i)+a_(M_i,k)<=-1             for distinct i,j,k.
```

Minimize `sum_i t_(M_i)`. There are twelve equalities and fifty-two inequalities.
Every control satisfying the unsaturated case gives a feasible point in the LP for its event
order. The first two groups encode cumulative nonnegativity, monotonicity, and total mass;
they also imply nondecreasing event times. No derivatives, breakpoints, or approximate integral
values are used in this representation.

Conversely, the cumulative data could be interpolated linearly between distinct event times
to give a simplex-valued piecewise-constant control, because the nonnegative allocation
increments sum to each time increment. Exact maximality of the reaches is not imposed by
this interpolation, so the LP is used only in the necessary-condition direction. That is
sufficient for proving a lower bound.

The twenty-four regular-order programs have exact certified lower bound `112/9`; the six
interleaved-order programs have exact certified lower bound `43/3`, which is larger. Thus
all programs imply (4).

## Exact certificates and verification

The complete certificates are stored in
`code/cia-distinct-reach/certificates_n4.json`. The independent-of-solver checker is
`code/cia-distinct-reach/verify_n4.py`; it uses only Python's standard library.

For each program in the form

```
min c^T x  subject to A x<=b, B x=d, x>=0,
```

a certificate consists of rational vectors `y<=0` and unrestricted `z` satisfying

```
r=c-A^T y-B^T z >=0.
```

For every feasible `x`, the exact identity

```
c^T x = y^T A x+z^T B x+r^T x >= y^T b+z^T d
```

proves the asserted lower bound. The checker reconstructs the integer matrices for all thirty
orders, checks every multiplier sign and every residual coordinate using `Fraction`, and checks
the lower bound exactly. The certificates were proposed by SciPy/HiGHS dual solutions followed
by rational reconstruction; the proof checker does not import or trust SciPy, HiGHS, floating
point arithmetic, or optimization statuses.

Run:

```
python code/cia-distinct-reach/verify_n4.py
```

Verified output:

```
Verified 30 event-order cases using exact rational arithmetic.
24 regular cases: sum M_i >= 112/9.
6 interleaved cases: sum M_i >= 43/3 > 112/9.
No numerical solver, tolerance, or approximate coefficient is used.
```

The independent review checked the reduction from arbitrary measurable controls to these LPs,
the thirty-case coverage, the implication from (4) to (1), and the matrix-generation and
certificate-checking code. It also independently enumerated the event orders and rebuilt all
dual identities using semantic variable names. The exact programmatic inequalities support
a computer-assisted proof; a short symbolic proof of (4) would be preferable if one can be found.

## Useful unsuccessful approaches and further directions

A nine-interval SLSQP search with sixteen random starts found no profile beating uniform
three-block reach; fourteen runs returned `148/27` and two stopped at the capped horizon. This was
only exploratory evidence and is not part of the proof.

The tempting intermediate inequality
`sum_i A_i(M_i)<=sum_i M_i/4` is false: random piecewise-constant controls violate it. It should
not be used to replace the finite LP argument.

A possible generalization retains `R_i` and two-block excluded-mode reaches `M_i` for arbitrary
`n>=3`. The same event-order argument gives `n!+(n-1)!` cases. To prove the three-block reach
bound for general `n`, the corresponding target is

```
sum_i M_i >= n^2 E*((n/(n-1))^2-1).
```

Also, if a pair of modes attains the global maximum two-block reach, then `M_i` equals that
maximum for every mode outside the pair. Hence at least `n-2` of the largest `M_i` are equal.
This extra exact structure was not needed by the thirty LPs and may permit a simpler symbolic
argument or a smaller case analysis. No general-`n` theorem is claimed here.

## Exact counterexample when three modes must supply three distinct blocks

The spare-mode condition cannot be dropped even for `n=3,k=3`. This counterexample was developed
during the investigation and independently checked directly from its rational knot table;
see the additional review in `notes/review-cia-distinct-reach-n4.md`.

Take `E=1` and horizon `L=57/8`, the uniform-control three-block reach. Define the three
cumulative allocations by linear interpolation through the following knots; **every table
entry is divided by 146**:

| Time numerator | A_0 numerator | A_1 numerator | A_2 numerator |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 146 | 98 | 48 | 0 |
| 194 | 110 | 48 | 36 |
| 256 | 110 | 78 | 68 |
| 408 | 224 | 116 | 68 |
| 516 | 224 | 178 | 114 |
| 580 | 240 | 178 | 162 |
| 971 | 417 | 309 | 245 |

After the final knot `t*=971/146`, extend with `alpha_i=1/3` until `L`. Every allocation
increment is nonnegative, the three increments sum to the corresponding time increment,
and every slope is at most `3/4`. Thus this defines a valid piecewise-constant simplex-valued
control, and every `H_i` is strictly increasing. There are no flat-segment ambiguities in
any inverse.

The first reaches are

```
R_0=128/73, R_1=97/73, R_2=1.
```

For each excluded mode `i`, both orders of the other two modes reach the same time:

```
M_0=204/73, M_1=258/73, M_2=290/73.
```

These identities follow by evaluating the appropriate `H_k` at the table's fourth through
seventh knots; for the two modes `j,k` distinct from `i`, both identities
`H_k(M_i)=R_j+1` and `H_j(M_i)=R_k+1` hold. At the final knot,

```
H_i(t*)=M_i+1    for each i.
```

Strict increase proves that **all six distinct three-mode orders end exactly at**

```
t*=971/146 < 57/8 =3*((3/2)^3-1).
```

The exact check `code/cia-distinct-reach/verify_n3_counterexample.py` verifies valid slopes,
first reaches, both-mode reaches, and all six final inverse compositions using rational
arithmetic. This is a counterexample to the reach conjecture with `k=n`; it does not refute
the conjecture with `k<=n-1`, the four-mode theorem above, or any balanced-total CIA result.

## Additional exploratory finite-n LP computations

The same event-order LP relaxation was solved numerically for `n=5` (144 orders) and `n=6`
(840 orders). Its minimum aggregate two-block values were respectively `225/16` and `396/25`,
matching `n²*((n/(n-1))²-1)`. These larger cases are exploratory: rational certificates for them
are not included here and they are not promoted to proved theorems. They support investigating
a symbolic aggregate inequality for all `n>=4`.

That symbolic inequality has now been proved in
[the exact two-switch result](../results/cia-exact-two-switch-worst-case.md), with an
[independent analytic review](review-cia-distinct-reach-general.md). It proves the
three-block reach bound for every `n>=4` and supersedes the computational positive
proof above. The exact four-mode certificates and the three-mode counterexample are
retained as independent checks and evidence for the dimension restriction.
