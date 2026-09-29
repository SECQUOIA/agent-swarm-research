# Fresh adversarial review of sparse Putinar kernel rounding

Date: 2026-09-28. Reviewed: [sparse-putinar-kernel.md](sparse-putinar-kernel.md),
Sections 1–7, independently of its author. This review also commissioned a
separate proof check of the moment-degree and SDP-duality interface.

## Assessment

No substantive proof defect was found in the finite-order rounding theorem,
the fixed-instance `O(log^3(R)/R^2)` consequence, or the sparse certificate
consequence under the assumptions stated in the draft. The all-input
mathematical argument survives the checks below. The exact computations
are supplemental checks, not the basis for a universal conclusion.

This assessment does not establish priority or significance relative to all
existing sparse-hierarchy results. The kernel construction and dense rate
are already prior. A dedicated sparse prior-work comparison remains necessary.
The result concerns box optimization with a junction-tree polynomial
objective. It does not establish a rate for additional polynomial constraints
or integrality, and gives no computational speedup guarantee.

## Primary-source comparison and degree correction

Examined the primary source
[Gribling, de Klerk and Vera, arXiv:2605.31496v1](https://arxiv.org/html/2605.31496),
especially Sections 2.3 and 3.1–3.5. Its Proposition 4 gives the squared-kernel
identity; Lemmas 1–2 give the geometric SOS approximation and coefficient
bound; Proposition 8 gives the half-maximum lower bound on the mass.
These inputs agree with the draft after setting the final Fejér coefficient
to zero. No source claim of a sparse hierarchy theorem was used.

There is an actual degree issue in the source's proof of Lemma 5: it assigns
degree `(N+2)r` to `p_(r,N) M_r`, although the definitions give degree at most
`2r(N+1)` in general. Its earlier degree count for the kernel uses the latter
quantity. The present draft independently uses
`D=2(s-1)(N+1)`, which is correct for its weights, and bounds the exact residual
`n-1=-z^(N+1)` directly. The draft does not depend on the source's stated
degree in Lemma 5.

Two other source statements should not be imported literally. Proposition 9
selects `N=ceil(3 log_2 r)`, which need not be even, and Propositions 9/11
call images of arbitrary Chebyshev inputs SOS. The latter cannot hold for
odd inputs: with `s=2`, direct integration gives `K T_1=x`, so
`A T_1=p(x)x` is negative at `x=-1`. The present draft explicitly chooses
even `N` and requires SOS of `Q(.,y)`, not of `A T_k`. These repairs retain
the asymptotic construction; this review makes no claim that the dense
rate itself is false.

## Algebra and coefficient estimates

For `x=cos(theta)`, `y=cos(phi)`, the displayed `S_s` is the average of the
two Fejér kernels with arguments `theta-phi` and `theta+phi`. It is therefore
nonnegative. Orthogonality gives the mass in (9). The sum of squared weights
gives exactly `C_s=(2s^2+1)/(3s)`, and the nonnegative composed kernel in (10)
proves `C_s/2<=M_s<=C_s`. This establishes `0<=z_s<=1/2` on the interval.

For even `N`, expanding the right side of (12) verifies the geometric-sum
identity term by term. Every term is a square after substituting `z_s(x)`.
Thus `p` is globally SOS, as is `Q(.,y)=p S_s(.,y)^2` for each fixed output.
Both have explicit finite square representations of their stated degree.
The identity `p M_s=1-z_s^(N+1)` follows by telescoping, including at points
outside the interval; the interval bounds follow from `0<=z_s<=1/2`.
The mass is globally SOS because both `p` and `M_s` are globally SOS.

To check (16), first expand `(T_k(y)-T_k(x))S_s(x,y)` using
`2T_iT_j=T_(i+j)+T_|i-j|`. Multiplication by the second `S_s` and integration
then replaces each `T_m(y)` by `(1-a_m)T_m(x)`, with `a_0=0` and
`a_m=1` for `m>=s`. The three groups give exactly the three negative squared
coefficient differences in (16). The term at `j=s` is zero, so the endpoint
index and the case `k=s` cause no discrepancy. The case `k=0` is zero on
both sides.

Each product of two Chebyshev polynomials has coefficient norm one. The
clipped sequence `a_j=min(j/s,1)` is `1/s`-Lipschitz on its indices. These
facts give the stated error bound, including the last sum with `k-1` terms.
The coefficient expansion of `M_s` gives
`||z_s||_1=(C_s-1)/C_s`; therefore `||p||_1<=(N+1)/C_s`.

The residual `n-1` has degree at most `D`, and its sup norm is at most
`delta`. Chebyshev orthogonality gives
`||q||_1<=sqrt(2(D+1))||q||_infty` for degree at most `D`. Applying that
bound to the residual, and then multiplying by `T_k` in coefficient norm,
proves (15). The tensor-product estimate follows by expanding a product of
factors each of coefficient norm at most `1+eta`, or by telescoping it.

A potentially dangerous truncation step is handled correctly. The two
intermediate terms

```text
p (K T_k - M_s T_k),       (n-1) T_k
```

can have degrees larger than `D`. Their sum is `A T_k-T_k`, whose degree is
at most `D` because the source degree of `Q` is at most `D` and `k<=s<=D`.
The draft uses coefficient-norm inequalities on the intermediate terms but
applies the truncated moment functional only to the combined polynomial.
There is consequently no reliance on undefined high-degree moments.

## Ordinary quadratic-module membership and separator normalization

The interval SOS theorem at even degree `D` gives

```text
n-a = sigma_0 + (1-x^2) sigma_1,
1-n = tau_0 + (1-x^2) tau_1,
```

with the full degree of every summand at most `D`. Non-strict positivity is
allowed in that theorem. The mass is an even polynomial, although the degree
bounded form of the interval theorem would suffice here. Multiplying either
identity by a globally SOS polynomial preserves membership in the ordinary
box quadratic module: products of the SOS coefficients remain SOS, while
each term still has only one box generator.

In the induction (22), every `P_j` is globally SOS. Expanding that induction
therefore introduces no products of distinct generators. Its degree is at
most `jD`; multiplication by `Q_S` raises it to at most `(|S|+j)D<=R`.
This is well within the available ordinary moment and localizer truncations.
It proves the pointwise inequalities in (23) even for moment functionals
that have no representing measure.

Integrating the upper inequality gives `Z_b<=Z_S`. The lower inequality
therefore implies

```text
h_(b,S)/Z_b >= a^|B_b\S| h_S/Z_b
              >= a^|B_b\S| h_S/Z_S.
```

The use of normalization is in the correct direction. Both adjacent
normalized marginals contain the probability measure `eta_S` with weight
at least `a^k_e`. Their common mass is thus at least that value. Under the
declared convention `TV(P,Q)=sup_A|P(A)-Q(A)|`, the resulting bound is
`1-a^k_e`, with no missing factor two. Zero-density sets need no division;
the empty-separator case has TV zero exactly.

## Moment control, objective, repair, and duality

The ordinary-module identity (27) is a telescoping product identity using
`1-T_k(x)^2=(1-x^2)U_(k-1)(x)^2`. Each square multiplying a generator has
degree at most `|alpha|-1`, so the identity is valid under order `R` when
`|alpha|<=R`. It bounds `L(T_alpha^2)<=1`, and the PSD moment matrix gives
`|L(T_alpha)|<=1`. Zero indices contribute no terms. This argument does not
claim such a bound for all tensor polynomials of degree `2R`.

The source degree of each tensor kernel output is at most `v_bD<=R`.
Also `D>=s>=d_infty`, so the original objective in that bag lies within the
same degree limit. Hence every coefficient of `A_b g_b-g_b` can legitimately
be bounded using (26).

The normalization identity is exact:
`Z_b E_(nu_b)g_b=L_b(A_b g_b)`. Rearranging gives (29), with no reciprocal
mass loss and with constants cancelling. Applying `||g_b||_infty<=C_b`
is sufficient; no bound on `L(g_b)` beyond its already established
coefficient control is needed.

For repair, each maximally coupled separator law lifts to a pair of full
bag copies by disintegration. Pair laws on a tree with their shared vertex
marginals glue to a joint law of all bag copies. The event that all edge
separators agree therefore has failure probability at most the sum of the
TV bounds. Running intersection identifies a single global point on the
agreement event. A fixed box point can be used on failure. The objective
changes by at most `W` on failure, proving (31). The full-product box
assumption is essential for this last step. Standard Borel spaces provide
the stated conditional laws and make the agreement event measurable.

For every feasible moment objective `m`, the repaired law gives
`f*<=m+E`. Taking the infimum yields `rho_R>=f*-E`, while point evaluation
gives the reverse relaxation inequality. No attainment of the primal
moment infimum is required.

For Section 6, product-arcsine moments make every moment and single-generator
localizer matrix positive definite: a nonzero polynomial square integrates
strictly positively on the box interior. They also obey all separator
equalities. Thus primal Slater holds on the equality affine space;
redundant equalities only make the multipliers nonunique. The finite
objective lower bound gives an attained dual optimum. Each local dual
identity has the local objective minus its scalar multiplier, plus signed
separator multipliers, equal to a local module element. Summing cancels the
separator polynomials and gives (32). This reasoning was also checked by
the separate reviewer.

## Rate and scope of the conclusion

With the prescribed even `N`, `delta<=1/(2s^3)` and
`D=2(s-1)(N+1)`. The first part of `eta` is bounded by
`3d_infty^2(N+1)/s^2`. For the second part, squaring reduces the claimed
bound to `2(D+1)<=4s^2(N+1)^2`, which holds for `s>=2`, `N>=2`.
When `w eta<=1`, `Gamma_v<=e v eta`. The normalization error contributes
at most `w C_f delta`, and repair contributes at most
`2 C_f(t-1)w delta`, giving exactly (8).

The proposed integer choice `s=floor(R/(8w log_2(R+2)))` has
`wD<=R` for all sufficiently large `R`, since
`N+1<=3 log_2(s)+3`. It also satisfies the fixed objective-degree threshold
eventually. Thus the estimate covers every sufficiently large order, not
just a selected subsequence. The dependence on `t`, `w`, and the chosen
objective decomposition remains material. The claimed asymptotic rate
holds with those quantities fixed.

## Targeted exact computation

Added and ran:

```text
python research-20260928/solver/check_sparse_putinar_fresh_review.py
```

Result:

```text
PASS: 52 exact kernel identities; 24 exact SOS/normalization cases; 156 exact coefficient-error bounds
```

The script uses rational Chebyshev coefficient arithmetic. It constructs
`K T_k` directly by integrating the square of the original kernel, separately
from the displayed coefficient-difference identity. It checks every
`s=2,...,9`, `k=0,...,s`, and `N=2,4,6`, including exact source degrees,
the geometric SOS identity, mass identities, and coefficient bounds.
Interval mass inequalities are additionally checked on 33 rational grid
points per parameter pair. Those grid checks do not prove interval
positivity; the composed-kernel argument above does. These computations do
not verify arbitrary moment SDP feasibility, all truncation orders, general
measure gluing, literature priority, or practical value. No project-wide
checks or CI-status inspections were run.
