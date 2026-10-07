# Independent review of bit-serial conditioning

Date: 2026-10-02. Verdict: the stated conditioning result is sound.

Reviewed [the proof note](bounded-coefficient-hardness-conditioning.md)
and [its exact checker](check_bit_serial_conditioning.py). This review
concerns that particular reduction and does not establish hardness under
a bounded negative-curvature/growth ratio.

The objective matches equations (20)–(24) of
[Del Pia–Khajavirad, version 1, Section 3](https://arxiv.org/html/2609.35595v1#S3)
with two items. Here the source's total item weight is `U=2B-1`, so its
choice of bit length is exactly `ell=ceil(log2(2B))`. Its variable count
`2n ell+n+ell` becomes `5 ell+2`. The coefficient and treewidth statements
apply to the unweighted construction; arbitrary positive square weights
preserve the proof below, without a claim that they preserve bounded
coefficient magnitudes.

The digit recurrence in (2) is correct with low-to-high bits: multiplying
the state at step `k` by two and subtracting the preceding state leaves
`b_ik u_i`. Both the binary point `(1,0)` and the fractional point
`(1/B,1)` satisfy every affine residual, including the final target
residual. All their coordinates are in the unit box. Since all summands
are nonnegative and the only binary solution is `(1,0)`, zero objective
forces this choice and uniquely determines every remaining coordinate.

For the displacement `d`, let `R=||d||^2` and `q=1-1/B`. The fractional
objective is `cq/B`, whereas `Ad=0` gives
`d^T H d=-2c(q^2+1)`. Thus every positive constant satisfying global
point growth `Psi(v)-Psi(v*) >= g ||v-v*||^2` obeys

\[
 g\leq\frac{cq}{BR},\qquad
 \nu\geq\frac{2c(q^2+1)}R,\qquad
 \frac\nu g\geq2B(q+q^{-1})\geq4B.
\]

The cancellation of `R`, `c`, and all square weights is valid. In
particular, separate positive weights on individual squares do not change
this argument. For `B=2^m`, `ell=m+1` and `N=5m+7`, so the lower bound is
exponential in the number of variables.

The positive-growth argument also holds. In a neighborhood of the unique
optimizer, let `delta_i` be the distance of `x_i1` from its optimizing
endpoint. If `delta_i<=1/2`, its endpoint penalty is
`delta_i(1-delta_i)>=delta_i^2`. Define the linear displacement map

\[
 M h=(h_{x_{11}},h_{x_{21}},Ah).
\]

This map is injective: its zero initial choices and zero copy residuals
force all choice displacements to zero; the digit, running-sum, and
target recurrences then force every state displacement to zero. For
`alpha=min(c,min_j W_jj)>0`, the local objective is consequently at least
`alpha ||M h||^2`, which gives positive local quadratic growth. On the
compact complement of this neighborhood, the continuous ratio
`Psi(v)/||v-v*||^2` has a positive minimum because the optimizer is unique.
Combining the two regions proves existence of a global `g>0` for each
fixed instance and fixed positive weights.

The only executable check run for this review was

```sh
python3 -B research-20261002-decomposition/negative-curvature/adversary/check_bit_serial_conditioning.py
```

It passed with 106 constructions, 954 weight cases, 11,332 zero-residual
checks, and maximum `B` bit length 201. The checker uses exact rational
arithmetic. It varies the common square-penalty scale and the common
endpoint weight; the proof, rather than these finite cases, establishes
the claim for arbitrary separate positive square weights. Its Hessian
check uses the residual representation directly, without an independent
dense Hessian assembly. The universal argument does not require numerical
eigenvalues. No project-wide verification or CI inspection was performed.
