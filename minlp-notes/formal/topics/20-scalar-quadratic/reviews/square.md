# Independent review: exact square precision and linear formulations

Date: 2026-09-20. Reviewer: independent source-review agent.
Reviewed modules: `SquarePrefix`, `SquareConstruction`, `SquareSystem`,
`SquareLift`, and `SquareMinimum` in
[Formal/QuadraticPrecision](../../../Formal/QuadraticPrecision).
The review also inspected the invoked interval threshold arithmetic and
minimum-count definitions.

Verdict: **PASS** for S1–S3 and the square hypograph construction in I5.
The upper formulation is an actual finite affine row system, and the
minimum statements concern actual convex integer and binary linear
lifts. There is no assumed formulation, merely dyadic subsequence, or
unattained infimum replacing the claimed exact result.

## Prefix and scalar constraints

The recursive prefix uses weights `1/2, 1/4, ...`, and the residual
width is `h=2^-L`. `exists_squarePrefix` covers every input in the
closed interval `[0,1]`, including one, and includes the empty prefix.
At the right endpoint its recursion repeatedly chooses the one branch
and leaves the positive residual width; it does not require an input
strictly below one. At a dyadic boundary the non-strict left branch is
also valid because the residual interval is closed.

The four binary-product inequalities enforce `v=b*u` for either binary
value. Exact graph feasibility uses the necessary range `0<=u<=U`.
The construction applies them once to `b_i*y` with `U=1`, and once
to `b_i*r` with `U=h`. Both ranges are present in the formulation.
The prefix-linear identities therefore give

```text
w = A*y + A*r + q,   y=A+r,   w-y^2=q-r^2.
```

Thus the residual square is the only approximation. Its triangle
contains `q=r^2` and bounds both signs of `q-r^2` by `h^2/4` over
the whole closed residual interval. All choices of binary code that
satisfy the rows obey this identity and error bound; soundness is not
restricted to the code selected by the containment proof.

`squareRelaxation_attains` supplies a feasible original input `y=h/2`
with every bit zero and `q=w=h^2/2`. Its upper error is exactly
`h^2/4`. The witness is in `[0,1]` at every depth, including zero.
`squareBinaryLift_attains` transfers it into the actual lifted-system
projection.

## Actual affine system and hypograph direction

`SquareSystem` encodes every row as an affine map. Equalities appear
as two opposing rows. The auxiliary indexing allocates disjoint
coordinates to `r`, `q`, `v`, and `t`, and `squareAuxWitness` explicitly
packs arbitrary witnesses into these same positions. The feasibility
and projection equivalences verify both directions of this connection.

The actual system has `L` binary coordinates, `2+2L` continuous
auxiliaries, and **`11+10L` rows**. The row count includes the two
explicit bounds per code coordinate, needed for the shared
`BinaryLinearLift` contract. The underlying `SquareRows` predicate has
`11+8L` rows before those bounds; that intermediate count should not
be confused with the final system count. Both are linear in depth.

For hypographs, the two lower residual-square rows are replaced by
identically zero rows. The upper row `q<=h*r` remains. The same
auxiliary `q` has no other lower bound, and the output equality permits
arbitrarily negative outputs. `squareHypograph_contains` constructs
`q=w-y^2+r^2` for every `w<=y^2`; this can be arbitrarily negative
and satisfies all remaining rows. Thus there is no accidental bound
truncating the hypograph. `squareBinaryLift_hypograph` proves the full
unbounded-hypograph contract in the common model, with error at most
`h^2/4`. Retaining the two zero rows makes its actual recorded row
count the same as the graph system's count.

## Exact minima and thresholds

The lower bound invoked by `SquareMinimum` concerns arbitrary finite
continuous convex lifts with unrestricted signed integer coordinates.
It uses `2^p+1` exact grid contacts and `2^p` parity vectors, so two
distinct contacts have an integer midpoint witness. Their separation
is at least `2^-p`, giving the exact lower error `4^-p/4`. This is a
uniform theorem in `p`, not a finite numerical test.

`squarePrecisionCount` is the natural ceiling of
`(log2(1/eps)-2)/2`. The natural ceiling implements truncation at zero.
For every positive tolerance, `squarePrecisionCount_le_iff` proves its
exact equivalence to `4^-p/4<=eps`; it does not require small error or
exclude equality. Combining the explicit upper lift at every `p` with
this lower bound gives both `square_binary_feasible_iff` and
`square_integer_feasible_iff`.

`IsMinimumCount` requires feasibility at the specified count and a
lower bound against every other feasible count. Both minimum theorems
therefore prove attainment as well as optimality. In particular,
accuracy `1/4` needs zero codes and accuracy `1/16` needs exactly one.
`square_no_exact_integer_lift` separately excludes every finite count
at zero error, using strict positivity of the error threshold.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH"` and
`LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.SquareMinimum
lake env lean /tmp/Topic20SquareReview.lean
```

Both passed. The temporary review client checked actual graph containment
at input one at every depth, arbitrarily negative depth-zero hypograph
outputs at input zero, and the exact counts at tolerances `1/4` and
`1/16`. Initial drafts of that temporary client required an explicit
input function and simplification of `1^2`; no proof-source correction
was needed.

The client printed axioms for `exists_squarePrefix`,
`squareSystem_feasible`, `squareLift_relaxation`,
`squareBinaryLift_graph`, `squareBinaryLift_hypograph`,
`squareBinaryLift_attains`, `square_binary_minimum`,
`square_integer_minimum`, and `square_no_exact_integer_lift`.
Every list was exactly `[propext, Classical.choice, Quot.sound]`.

Reviewed SHA-256 hashes:

- `SquarePrefix.lean`: `c3299bd42d3a765773ceba902cf300afa2cef193580f5bbcb55066b183e187f2`
- `SquareConstruction.lean`: `a7d78e1e546a17b81ef049096194d69c595df613989ebbf13960b447665583cd`
- `SquareSystem.lean`: `9cebf763a9927fb8131048b65e948db01ee51e9c73aa6c2be0a90f93eb57dd71`
- `SquareLift.lean`: `61db59235369375b44c2ce130921f22fd0946cf9effabafaa872ae78dce251a6`
- `SquareMinimum.lean`: `5bbec5e5c7f64b42680ad728b2d20bc8ecf8326a5976f7ff03d21fb6ac974923`

No proof source was changed by this review. No project-wide verification
or CI inspection was performed.
