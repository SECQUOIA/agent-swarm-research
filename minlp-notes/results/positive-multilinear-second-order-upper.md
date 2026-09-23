# A finite harmonic-coupling bound with an optimized cutoff

Date: 2026-09-04. Status: final consolidated proof independently audited; no unresolved mathematical issue identified. This strengthens the finite upper bound in [the sharp leading-order theorem](positive-multilinear-sharp-degree-growth.md). It does not claim a matching second-order lower bound.

## Theorem

Let R(d) be the worst term-by-term gap divided by the convex-hull gap for positive multilinear polynomials of maximum degree at most d≥2, at points with positive hull gap. The bounds below apply to the unit box and every finite box with nonnegative lower bounds.

Choose any real cutoff M≥d−1 and define

    L=1+ln M,       ρ=(d−1)/M,       c=1−exp(−1),
    F_(L,ρ)(v)=1−exp(−(1−ρv)/(Lv)),       0<v≤1,
    J_(L,ρ)(z)=∫_z^1 F_(L,ρ)(v)dv,       0≤z≤1.

Set F_(L,ρ)(0)=1 by continuity. Let ζ be the unique solution of J_(L,ρ)(ζ)=ζ in (0,1). Then

    R(d)≤1/ζ+2/c.                                          (1)

A finite certificate avoids computing the integral. Let w=W(L exp(−ρ)), where W is the positive branch of Lambert W. If w≥1, then

    ζ≥[w−1/(2w)]/L,
    R(d)≤L/[w−1/(2w)]+2/c.                                (2)

Both (1) and (2) permit optimization over the single cutoff parameter M.

For a simple asymptotic choice, put N=1+ln(d−1) and take M=(d−1)N. Then

    L=N+ln N,       ρ=1/N,
    R(d)≤N/[ln N−ln ln N+o(1)]+2/c.                       (3)

In terms of degree, the denominator in (3) is ln ln d−ln ln ln d+o(1). This improves the earlier proof's loss of three times ln ln ln d. The leading constant remains one. Whether the remaining ln ln ln d loss is necessary is open here.

## The common-marginal couplings

Affine terms have zero gap and may be discarded. Use the deficiency representation in the sharp-degree note. For each remaining monomial choose an anchor with smallest mean u and put

    T=min(u, Σ_other coordinates (1−x_j)).

This is its term-by-term gap. For any Bernoulli coupling with the prescribed means, its deficiency is the anchor times the indicator that at least one other coordinate fails. The hull gap is the maximum expected weighted sum of these deficiencies. All deficiencies are nonnegative.

Call coordinates with x_i≤1/2 low and the others high. Independence gives deficiency at least cT/2 for every all-high monomial and every monomial with at least two low coordinates, as proved in the sharp-degree note.

The remaining hard terms have exactly one low anchor u≤1/2 and r≤d−1 high coordinates with failure marginals p_1,...,p_r. Set

    S=Σ_j p_j,       T=min(u,S),       p_max=max_j p_j.

When T=0 no estimate is required. All couplings below apply to the entire vector, regardless of which monomial is being considered.

For harmonic coupling, sample a common uniform t in (0,1). Set every low coordinate to 1[t≤x_i]. Given t, make high-coordinate failures independent, with conditional probability

    q_p(t)=min(1,p/t)/(1+ln min(M,1/p)) if t≤min(Mp,1),
    q_p(t)=0 otherwise.

A coordinate with p=0 never fails. The marginal is exactly p: for h=min(Mp,1),

    ∫_0^h min(1,p/t)dt=p[1+ln(h/p)].

Thus all prescribed coordinate means are preserved. Every positive-p normalizer is at most L.

For threshold coupling, again use a common uniform t and the same low-coordinate rule; a high coordinate fails if and only if t≤p.

## The complete harmonic deficiency curve

Set z=min(p_max/T,1). Threshold deficiency is min(u,p_max), which is at least zT.

If p_max<T, consider p_max≤t≤T. Every p_j≤t. A high coordinate is inactive in the harmonic coupling only if p_j<t/M. The sum of inactive failure marginals is at most rt/M≤ρt. Consequently active marginals sum to at least S−ρt≥T−ρt, and the sum of conditional failure probabilities is at least

    (T−ρt)/(Lt).

The probability of at least one conditional failure is at least one minus the exponential of the negative of that sum. The anchor is active throughout this interval, so harmonic deficiency G_h satisfies

    G_h≥∫_(p_max)^T [1−exp(−(T−ρt)/(Lt))]dt
       =T J_(L,ρ)(z).                                    (4)

If p_max≥T, (4) remains valid with z=1 and J_(L,ρ)(1)=0.

## Optimal mixture for these two scalar guarantees

The function F_(L,ρ) is continuous and strictly decreasing on [0,1]. Its value at zero is one; its value at one is nonnegative and is zero only when ρ=1. Hence J_(L,ρ) is decreasing and strictly convex. The function J_(L,ρ)(z)−z is strictly decreasing, positive at zero, and negative at one. This proves existence and uniqueness of ζ.

Put a=F_(L,ρ)(ζ), with 0<a<1. The convex tangent inequality gives

    J_(L,ρ)(z)+az≥J_(L,ρ)(ζ)+aζ=(1+a)ζ.

Mix harmonic and threshold coupling with respective probabilities 1/(1+a) and a/(1+a). Their simultaneous guarantees show that every hard term then has deficiency at least ζT.

This is the optimal mixture when using only the two scalar lower-bound curves J_(L,ρ)(z) and z. For any mixture weight λ, evaluation at z=ζ gives

    λJ_(L,ρ)(ζ)+(1−λ)ζ=ζ.

Thus its minimum guarantee cannot exceed ζ. The tangent mixture attains it. This does not establish optimality among all Bernoulli couplings or show that a polynomial simultaneously attains these scalar lower bounds.

Finally mix that hard-term distribution and independence with probabilities proportional to 1/ζ and 2/c. After normalizing by Z=1/ζ+2/c, every term receives deficiency at least T/Z from its appropriate component. All other deficiencies are nonnegative, so summation with nonnegative coefficients proves (1).

## Finite Lambert-W certificate

The inequalities x−x²/2≤1−exp(−x)≤x hold for x≥0. Also, for 0<z≤1,

    ∫_z^1 (1/v−ρ)²dv
    =1/z−1+2ρ ln z+ρ²(1−z)≤1/z,

because 0<ρ≤1. For 0<A≤L, integrating the quadratic lower bound gives

    L J_(L,ρ)(A/L)
    ≥ln L−ln A−ρ+ρA/L−1/(2A)
    ≥ln L−ln A−ρ−1/(2A).                                 (5)

Let w=W(L exp(−ρ))≥1, so w+ln w=ln L−ρ. Put A=w−1/(2w). Then A≥1/2 and A<L. Moreover,

    A+ln A+1/(2A)−(w+ln w)
    =ln(1−1/(2w²))+1/(4Aw²)
    ≤−1/(2w²)+1/(4Aw²)≤0.

Equation (5) therefore implies J_(L,ρ)(A/L)≥A/L. Strict monotonicity of J_(L,ρ)(z)−z yields ζ≥A/L, proving (2).

## Tuned second-order bound

Choose N=1+ln(d−1), M=(d−1)N, L=N+ln N, and ρ=1/N. Write w=W(L exp(−ρ)). Its defining identity is

    w+ln w=ln L−ρ.

For sufficiently large N, w≤ln L and w≥ln L−ρ−ln ln L. Hence w/ln N→1. Substitution back into the identity gives

    w=ln N−ln ln N+o(1).

Because 1/w→0 and (ln N)²/N→0,

    (N/L)[w−1/(2w)]=ln N−ln ln N+o(1).

Substitute this denominator into the finite bound (2) to prove (3). No uniform expansion of the two-parameter fixed point is needed.

## The simplest cutoff as a special case

With M=d−1, one has ρ=1 and L=1+ln(d−1). Write ζ=z_L. Then the exact fixed point satisfies

    L z_L=ln L−ln ln L−1+o(1).                             (6)

For ln L≥4, a simple finite certificate is

    z_L≥[ln L−ln ln L−2]/L.                               (7)

Indeed, set A=ln L−ln ln L−2. Then A≥1/2, A≤ln L, and (5) gives L J_(L,1)(A/L)≥A.

To verify (6), put α=Lz_L and ℓ=ln L. The lower bound (7) and the integrated linear upper bound imply

    α≥ℓ−ln ℓ−2,
    α≤ℓ−ln α−1+α/L.

Thus α/ℓ→1. The integrated quadratic bounds then yield α=ℓ−ln α−1+o(1), proving (6).

The Lambert certificate in this special case also captures the first reciprocal correction. With w=W(L/e),

    α=w−1/(2w)+O(w^−2).                                  (8)

To see this, the cubic Taylor remainder contributes at most 1/(12α²) to L J_(L,1)(α/L). The other omitted terms in (5) are O(ln L/L), so

    α+ln α=ln L−1−1/(2α)+O(α^−2).

Compare with w+ln w=ln L−1. Since α∼w, the mean value theorem first gives α−w=O(1/w), then gives (8).

## Scope and verification

The finite nonnegative-box extension follows the independently checked positive-expansion argument in the sharp-degree note: coordinatewise affine rescaling preserves the full hull gap, the original term-by-term gap is at most that of the expanded positive polynomial, and expansion does not increase degree.

The root investigation proposed retaining the entire harmonic deficiency curve. This lane derived the fixed-point characterization, mixture optimum for those curves, finite certificates, and cutoff tuning. The earlier leading-order result already proved R(d)∼ln d/ln ln d; the present result improves its finite upper certificate and second-order denominator. It does not prove an exact finite-degree ratio or a matching second-order asymptotic.

Independent review is in [the second-order audit](../notes/review-multilinear-second-order.md). The final consolidated text, including the tuned-cutoff section, passed a full reread. Numerical checks for the ρ=1 case are in [the scalar verification script](../code/verify_multilinear_second_order.py); they supplement the analytic proof. Novelty remains subject to the broader literature review of the positive multilinear result.
