# Independent audit of the sharp positive-box aspect upper bound

Date: 2026-09-04. Reviewer: `review_fbbt`.

Historical scope note: this review audited the superseded asymmetric estimate for `ρ≥64`, now preserved in `notes/positive-box-asymmetric-upper-predecessor.md`. It does not review the current `ρ+2` theorem in `results/positive-multilinear-positive-box-sharp.md`, which has its own two reviews.

Final draft read in full:
[Sharp leading-order gap growth with the box aspect ratio](positive-box-asymmetric-upper-predecessor.md).
Its written upper proof agrees with the argument checked below; no correction
is needed. Conditional end-strip identities are understood almost everywhere,
as interval endpoints do not change expectations.

The proposed common-aspect bound

\[
\operatorname{tbtgap}f(x)\le
\left(\frac{\rho+1}{1-3/\sqrt\rho}+2\right)
\operatorname{chgap}f(x),\qquad \rho\ge64,
\]

passes an independent mathematical audit. This review concerns the upper
bound; the matching lower family and literature novelty require their own
reviews. The proof uses the classical product-envelope identities already
recorded and reviewed in
[the positive-box result](../results/positive-multilinear-positive-box.md).

## Orientation and decomposition

Write `delta=1/sqrt(rho)`, `t=rho-1`, and `eta=1-1/rho`. Declare `u_i<=1-delta`
low, and put `q_i=1-u_i` on the high group. Then low successes under common
threshold rounding lie in `[0,1-delta]`, whereas high failures lie in
`[1-delta,1]`. Endpoint equalities have measure zero. Thus the normalized
concave value is exactly `C_L+C_H-1`, even though low marginals can exceed
one half. Independence gives the nonnegative decomposition

\[
D_I=D_{IL}+D_{IH}+J_I,
\qquad J_I=(P_L-1)(1-P_H).
\]

The old formula for the entire low-group orientation value cannot be reused
at this threshold. The proposed proof correctly uses only its cross term.
Conditional high factors differ from one only on the two end strips of
length `delta`. At an end-strip distance `s`, a low coordinate contributes
`1+(t/2)1[s<=u_i]`, since its success interval cannot cover both ends there.
A high coordinate contributes `1-(eta/2)1[s<=q_i]`. Consequently

\[
D_O=D_{OL}+D_{OH}+J_O\ge J_O
\ge \frac{t\eta}{2}\min(q_L,q_H).
\]

Here `q_L=max_low u_i`, `q_H=max_high q_i`, with empty maxima zero. The
separate-group deficiencies are nonnegative because each orientation law
preserves its marginals and the corresponding concave envelope is maximal.
This establishes the cross bound without an invalid low-group power formula.

## Low and high estimates

Set `A=C_L-1-t Q_L` and `B=C_H-1+eta Q_H`. As in the existing proof,
`A>=t^2(Q_L-q_L)` and `B>=eta^2(Q_H-q_H)`. For each subset of at least two
low coordinates,

\[
\prod_{i\in S}u_i\le(1-\delta)\min_{i\in S}u_i.
\]

Subtracting the independent positive expansion from the common-threshold
expansion and summing gives `D_IL>=delta A`. Singleton and constant terms
cancel exactly, including empty-group cases.

If `Q_H<=4 delta`, let `q=q_H` and `R=Q_H-q`. Bonferroni gives

\[
D_{IH}\ge B-\eta^2\sum_{i<j}q_iq_j
\ge B-\eta^2(qR+R^2/2)
\ge [1-(Q_H+q)/2]B\ge(1-3\delta)B.
\]

The middle inequality uses `B>=eta^2 R`; it involves no division by `R` or
`B` and therefore covers zero values. The actual loss is at most `2.5 delta`.

If `Q_H>=4 delta`, then `C_H>=1-delta` and
`P_H<=exp(-4 eta delta)`. Since `eta>=3/4` and `delta<=1/8`,

\[
e^{-4\eta\delta}\le e^{-3\delta}
\le1-3\delta+\tfrac92\delta^2\le1-2\delta.
\]

Thus `D_IH>=delta` and `J_I>=delta t Q_L`. Together with the low estimate,
`D_I>=delta(1+A+t Q_L)=delta C_L>=delta T`, where `T=C-V`,
`C_H<=1`, and the convex-envelope value `V` is positive.

## Constants and global transfer

The supporting slopes of the interpolated exponential at zero give
`T<=A+B+t eta min(Q_L,Q_H)`. The maximum-versus-sum estimates above imply

\[
T\le(1+1/\rho)A+(1+\rho)B+2J_O.
\]

Let `b=(rho+1)/(1-3 delta)`. In the small-high-mass case,
`b delta >=1+1/rho` because this is equivalent to
`rho delta>=1-3 delta`. Hence `T<=b D_I+2D_O`. In the large case,
`b>=1/delta`, so the same inequality follows from `T<=D_I/delta`.
All denominators are positive for `rho>=64`.

Choose independence with probability `b/(b+2)` and orientation with probability
`2/(b+2)`. Both are defined globally using the given marginals, independently
of the monomial support. Undoing each positive normalization and summing the
local inequalities is therefore legitimate. Common-threshold rounding
simultaneously attains every positive monomial's concave envelope, so the
full graph-hull gap dominates the mixture's summed deficiency.

The previously established positive affine expansion transfers this bound to
any positive box whose coordinate aspect ratios are at most `rho`; it does
not require a box-inclusion argument. Fixed coordinates may first be absorbed
into positive coefficients. The resulting constant is `rho+O(sqrt(rho))`,
which establishes upper leading constant one. No step divides by a gap, so
zero gaps, endpoint marginals, empty groups, and affine terms cause no exception.
