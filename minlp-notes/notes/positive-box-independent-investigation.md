# Independent investigation of positive multilinear polynomials on [1,2]

The later [coefficient proof](positive-box-rho-plus-two-proof.md) improves these
coarse bounds to `rho+2`, hence four on `[1,2]^n`. The derivations below remain as
independently useful alternative arguments and records of rejected stronger lemmas.

Date: 2026-09-04. This note concerns the actual monomial envelopes on the
physical box `[1,2]^n`, not the envelopes obtained after separately relaxing an
expanded polynomial. The bound 67 below has passed a fresh independent audit in
[the review record](review-positive-multilinear-fixed-positive-box.md). The later
general-aspect-ratio proof and positive affine transfer are incorporated in
[the canonical result](../results/positive-multilinear-positive-box.md), whose final
text the co-developer checked. The later coefficient proof resolves the factor-four
mixture conjecture and has two independent reviews linked from
[the final result](../results/positive-multilinear-positive-box-sharp.md).

## Two global candidate distributions

Write each physical variable as `1+X_i`, with `E X_i=u_i`. Independent Bernoulli
rounding has monomial expectation `P=∏(1+u_i)`. Fair endpoint orientation gives
coordinate `X_i=1[U≤u_i]` or `X_i=1[U≥1−u_i]`, independently choosing either
orientation with probability one-half and sharing the uniform `U`. Its exact
expectation is

\[
O=\int_0^1\prod_i\left[1+\tfrac12
 (1[t\le u_i]+1[t\ge1-u_i])\right]dt.
\]

Both distributions preserve every marginal and can be used simultaneously for all
monomials of a polynomial. If `C,V` denote the exact monomial concave and convex
envelopes, respectively, a uniform monomial inequality
`C−V≤K[(C−P)+(C−O)]` would give a dimension-independent polynomial gap bound `2K`
by mixing these two distributions equally.

Split coordinates into lows `u_i≤1/2` with `q_i=u_i`, and highs `u_i>1/2` with
`q_i=1−u_i`. Let `h` be the number of highs and divide all monomial values by `2^h`.
Define `L(t),H(t)` as the numbers of low and high deviation probabilities at least
`t`, for `0≤t≤1/2`, and let `Q_L,Q_H` be their total deviations. Then exactly

\[
C=1+\int_0^{1/2}(2^{L(t)}+2^{-H(t)}-2)\,dt,
\]
\[
O=1+2\int_0^{1/2}((3/2)^{L(t)}(3/4)^{H(t)}-1)\,dt,
\]
\[
P=\prod_{\rm low}(1+q_i)\prod_{\rm high}(1-q_i/2),\qquad
V=\phi(Q_L-Q_H),
\quad \phi(s)=2^{\lfloor s\rfloor}(1+s-\lfloor s\rfloor).
\]

The last formula follows because binary monomial values are `2^K`: the minimum
expected value with a specified expected total count is its adjacent-integer convex
interpolation. A distribution with adjacent total counts and any prescribed
coordinate marginals exists by the integrality of the cardinality slab in a cube.

## A tempting all-high factor-two lemma is false

For high-coordinate failure probabilities

\[
q=(1/2,49/100,1/100),\qquad Q=1,
\]

normalized values are

\[
C=\frac{501}{800},\qquad V=\frac12,\qquad
P=\frac{90147}{160000}.
\]

Therefore `C−V=20200/160000`, whereas `2(C−P)=20106/160000` is strictly smaller.
The conjectured estimate `C−V≤2(C−P)` fails even for three coordinates in the upper
half of the physical box. Its failure is small, so generic random checks can miss it.
The exact independent deficiency fraction is `10053/20200<1/2`.

This does not refute the mixture conjecture `C−V≤2[(C−P)+(C−O)]`.

## A rigorous uniform bound for all-high monomials

For all high coordinates, including the boundary probability one-half, independent
rounding satisfies

\[
C-P\ge\frac1{64}(C-V)
\]

in every dimension. This weak constant suffices to show that all-high monomials
alone cannot cause an unbounded physical-box gap. Here all values are divided by
the all-high baseline `2^d`.

Order the failure probabilities as `q_1≥q_2≥…`, with `0≤q_i≤1/2`, and set
`Q=Σq_i`, `b=Σ 2^(−i)q_i`. Then `C=1−b` and `P=∏(1−q_i/2)`.

If `Q≤1`, the exact convex envelope is `V=1−Q/2`, so `T=C−V=Q/2−b`.
Let `a=q_1`, `R=Q−a`; because all remaining weights in `b` are at most `1/4`,
`T≥R/4`. The two-term Bonferroni bound for independent failure events gives

\[
C-P\ge T-\frac14\sum_{i<j}q_iq_j
\ge T-\frac{aR+R^2/2}{4}
\ge(1-a-R/2)T\ge\frac14T.
\]

The last inequality uses `R≤1−a` and `a≤1/2`. It also covers `R=0`, when `T=0`.

If `Q≥1`, maximizing the weighted sum `b` at fixed total deviation fills successive
coordinates to their cap one-half. Writing `2Q=r+θ`, with integer `r` and
`0≤θ<1`, the resulting minimum `C` is the linear interpolation of
`1/2+(1/2)2^(−r)` at neighboring integers `r`. Convexity of the exponential gives

\[
C\ge\frac12+\frac12 4^{-Q},\qquad P\le e^{-Q/2}.
\]

Thus `C−P≥g(Q)=1/2+(1/2)4^(−Q)−e^(−Q/2)`. This function is increasing for
`Q≥1`: its derivative is `(1/2)e^(−Q/2)−(log 2)4^(−Q)>0`, since
`exp[(log 4−1/2)Q]≥4/sqrt(e)>2 log 2`. Consequently

\[
C-P\ge g(1)=\frac58-e^{-1/2}>\frac1{64}.
\]

For an elementary exact check of the last strict inequality,
`e^(1/2)>1+1/2+1/8+1/48=79/48>64/39`, so `e^(−1/2)<39/64`.
Since `0≤T=C−V≤C≤1`, the desired estimate follows.

No claim is made that the constant 64 is sharp or new. The mixed low/high case
is handled in the following section.


## Closing the mixed case: the earlier universal bound of 67

The following complete proof passed independent checking, as linked above. Its constant is deliberately coarse. It uses the exact physical monomial
envelopes and therefore does not rely on relaxing the affine expansion term by term.

Continue the low/high normalization above. Set

\[
C_L=1+\int(2^L-1),\quad C_H=1-\int(1-2^{-H}),\quad
P_L=\prod_{\rm low}(1+q_i),\quad P_H=\prod_{\rm high}(1-q_i/2),
\]

where all integrals have interval `[0,1/2]`. Write `D_I=C−P`, `D_O=C−O`, and

\[
A=C_L-1-Q_L,\quad B=Q_H/2-(1-C_H),
\quad D_{I,L}=C_L-P_L,\quad D_{I,H}=C_H-P_H.
\]

All these quantities are nonnegative. In particular, the common threshold
maximizes a product with nonnegative mixed differences, so it dominates independent
rounding within each group. Direct algebra gives

\[
D_I=D_{I,L}+D_{I,H}+J_I,
\qquad J_I=(P_L-1)(1-P_H)\ge0.
\tag{A}
\]

Similarly,

\[
D_O=D_{O,L}+D_{O,H}+J_O,
\]
\[
J_O=2\int((3/2)^L-1)(1-(3/4)^H)\ge0.
\tag{B}
\]

Here the two within-group orientation deficiencies are nonnegative. For the low
part, binomial expansion proves

\[
2^L+1-2(3/2)^L
=\sum_{j=2}^L(1-2^{1-j})\binom Lj
\ge\frac12(2^L-1-L),
\]

so `D_{O,L}≥A/2`. For the high part, nonnegativity follows from
`2(3/4)^H≤1+2^(−H)` by convexity of the integer power.

Let `a` and `b` be the largest low and high deviation probabilities, respectively,
with value zero for an empty group. The elementary integer inequalities

\[
2^L-1-L\ge(L-1)_+,\qquad
H/2-1+2^{-H}\ge\tfrac14(H-1)_+
\]

imply

\[
Q_L\le a+A,\qquad Q_H\le b+4B.
\tag{C}
\]

Whenever both counts are positive, the integrand in `J_O` is at least `1/4`.
Therefore `J_O≥min(a,b)/4`.

The convex function `φ` satisfies
`φ(δ)≥1+δ` for `δ≥0` and `φ(δ)≥1+δ/2` for `δ≤0`.
Substitute `δ=Q_L−Q_H` into `T=C−V` to obtain

\[
T\le A+B+\tfrac12\min(Q_L,Q_H).
\tag{D}
\]

If `Q_H≤1`, the all-high proof above gives `B=C_H−V_H≤4D_{I,H}`.
Combining (C), (D), and the lower bound on `J_O` gives

\[
T\le\tfrac32 A+3B+2J_O
\le3D_{O,L}+12D_{I,H}+2J_O
\le3D_O+12D_I.
\tag{E}
\]

This argument also covers an empty low or high group.

If `Q_H≥1`, the stronger absolute conclusion in the all-high proof gives
`D_{I,H}≥1/64`. Moreover,

\[
J_I\ge Q_L(1-e^{-Q_H/2})\ge Q_L/3,
\]

because `P_L≥1+Q_L` and `e^(−1/2)<2/3`. Since `V≥0`,

\[
T\le C\le1+A+Q_L
\le64D_{I,H}+2D_O+3J_I
\le64D_I+2D_O.
\tag{F}
\]

The two cases establish, for every physical monomial in every dimension,

\[
C-V\le64(C-P)+3(C-O).
\tag{G}
\]

Use independent rounding with probability `64/67` and endpoint orientation with
probability `3/67`. Both are defined globally using all coordinate means. Equation
(G) says their combined deficiency from the monomial's true concave envelope is
at least `1/67` of its true physical-box gap. Common-threshold rounding attains
all positive monomial upper envelopes simultaneously. Multiplication by positive
coefficients and summation therefore yield

\[
\operatorname{tbtgap}_{[1,2]^n}f
\le67\operatorname{chgap}_{[1,2]^n}f
\]

for every positive multilinear polynomial, with no degree or dimension dependence.
Affine terms contribute zero and can be removed. The proof applies to arbitrary
individual means, including deterministic coordinates and ties at one-half.

The constant 67 is not claimed sharp. Rational-grid and skewed random experiments
suggest the much stronger monomial inequality `T≤2(D_I+D_O)`, which would give
factor four. The later coefficient proof linked at the beginning of this note
proves that stronger inequality; the experiments themselves were not a proof. The failed all-high factor-two lemma must
not be used to justify that sharper conjecture.


## Extension to every fixed positive aspect ratio

The same argument gives a finite constant for every fixed `ρ>1`; this extension
was incorporated in the separately reviewed coarse result. Put

\[
a=\rho-1,\quad b=1-\rho^{-1},\quad
\eta_\rho=1-b+b^2/2-e^{-b}>0,
\]
\[
K_\rho=\max\{\eta_\rho^{-1},4(1+\rho)\},\qquad
L_\rho=2(1+\rho^{-1}).
\]

The resulting universal constant on `[1,ρ]^n` is `K_ρ+L_ρ`.
The positivity of `η_ρ` follows from the strict second-order Taylor upper bound
`e^(−b)<1−b+b²/2` for `b>0`.

Normalize a physical monomial by `ρ^h`, where `h` is the number of coordinates
whose Bernoulli means exceed one-half. In the preceding notation, replace
`2^L,2^(−H)` by `ρ^L,ρ^(−H)` and replace the orientation factors by
`(1+a/2)^L,(1−b/2)^H`. The independent factors are now
`P_L=∏(1+a q_i)`, `P_H=∏(1−b q_i)`.
Define

\[
A=C_L-1-aQ_L,\qquad B=bQ_H-(1-C_H).
\]

The exact scalar convex envelope is
`φ_ρ(Q_L−Q_H)`, where `φ_ρ(s)=ρ^(floor s)[1+a(s−floor s)]`.
Its supporting slopes at zero are `b` and `a`, giving

\[
T\le A+B+ab\min(Q_L,Q_H).
\]

Integer binomial expansion and telescoping give

\[
A\ge a^2(Q_L-q_{L,\max}),\qquad
B\ge b^2(Q_H-q_{H,\max}),
\]
\[
D_{O,L}\ge A/2,\qquad
J_O\ge(ab/2)\min(q_{L,\max},q_{H,\max}).
\]

For the bound on `B`, the integer sequence
`j b−1+(1−b)^j` starts at zero for `j=1` and every subsequent increment is at
least `b²`. The other two estimates follow directly from the positive binomial
coefficients and the minimum nonzero orientation cross integrand.

For `Q_H≤1`, the all-high convex envelope is `1−bQ_H`. The Bonferroni proof works
with event probabilities `bq_i`, giving `D_{I,H}≥B/4`. The mixed-case estimate is
therefore

\[
T\le(1+b/a)A+(1+a/b)B+2J_O
\le L_\rho D_O+4(1+\rho)D_I.
\]

For `Q_H≥1`, packing deviations to their cap one-half gives

\[
C_H\ge\tfrac12+\tfrac12\rho^{-2Q_H},\qquad
P_H\le e^{-bQ_H}.
\]

The difference `g(Q)=1/2+(1/2)ρ^(−2Q)−e^(−bQ)` increases for `Q≥1`.
Indeed, at `Q=1`,

\[
(\log\rho)\rho^{-2}
\le b(1-b)<b e^{-b},
\]

using `−log(1−b)≤b/(1−b)`; for larger `Q`, the first derivative contribution
decays faster because `2 log ρ>b`. Thus `D_{I,H}≥g(1)=η_ρ`.
Also `J_I≥aQ_L(1−e^(−b))`, whereas `T≤1+A+aQ_L`.
Because `η_ρ≤1−e^(−b)`,

\[
T\le\eta_\rho^{-1}D_I+2D_O.
\]

Combining the cases proves the scalar inequality `T≤K_ρD_I+L_ρD_O`.
The corresponding global mixture, with weights proportional to `K_ρ,L_ρ`, proves

\[
\operatorname{tbtgap}_{[1,\rho]^n}f
\le(K_\rho+L_\rho)\operatorname{chgap}_{[1,\rho]^n}f.
\]

No claim is made that these constants are sharp or behave well as `ρ↓1`.
The box with `ρ=1` is degenerate and has zero gaps directly.

### Nonuniform boxes with bounded aspect ratio

The same constant also applies to a positive box `∏[l_i,r_i]` with `l_i>0` and
`r_i/l_i≤ρ`. Set `s_i=(r_i/l_i−1)/(ρ−1)∈[0,1]` and transform from
`t_i∈[1,ρ]` by

\[
x_i=l_i[(1-s_i)+s_i t_i].
\]

For nondegenerate coordinates this is an invertible affine map onto the given
interval; degenerate coordinates can first be removed. Each original monomial
becomes a positive polynomial in the physical variables `t_i`, so its true hull
gap is at most the sum of the true gaps of its expanded physical monomials.
The full polynomial's hull gap is preserved by the affine map. Applying the
universal `[1,ρ]` estimate to the expanded polynomial therefore bounds the original
termwise gap by the same constant times its full hull gap.

This last expansion step is valid because the bound has already been proved on
`[1,ρ]`; expanding onto the unit cube alone would not establish a degree-independent
constant.


### A simpler explicit bound, including 45/2 on [1,2]

There is no need to use a poorly conditioned exponential constant near `ρ=1`.
Choose an ambient ratio

\[
R=\max\{4,\max_i(r_i/l_i)\}.
\]

The function `η_ρ` increases with `ρ`: as a function of `b`, its derivative is
`−1+b+e^(−b)>0`. At `ρ=4`,

\[
\eta_4=\frac{17}{32}-e^{-3/4}>\frac1{20}.
\]

Indeed, the positive Taylor terms give
`e^(3/4)>1+3/4+9/32+9/128=269/128>160/77`, which is equivalent to the required
strict inequality. Thus for every `R≥4`, `η_R^(−1)<20≤4(1+R)` and the general
constant simplifies to

\[
4R+6+\frac2R.
\]

Combined with the positive affine expansion above, this gives

\[
\operatorname{tbtgap}_{\prod_i[l_i,r_i]}f
\le\left(4R+6+\frac2R\right)
\operatorname{chgap}_{\prod_i[l_i,r_i]}f.
\]

In particular, every positive box of aspect ratio at most four, including
`[1,2]^n`, has uniform gap factor `45/2`. The corresponding mixture on `[1,4]`
uses independent rounding with probability `8/9` and endpoint orientation with
probability `1/9`.

For clarity, the `[1,2]` consequence is not an argument by set inclusion. Under
the affine bijection `x=(2+t)/3`, `t∈[1,4]`, each original monomial becomes a
positive polynomial in `t`; its true hull gap is bounded by the sum of the true
physical `[1,4]` monomial gaps. That inequality is what permits transferring the
universal polynomial bound back to the original box.
