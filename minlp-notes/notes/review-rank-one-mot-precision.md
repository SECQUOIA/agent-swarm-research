# Independent audit: rank-one MOT and the precision question

Date: 2026-09-04. Reviewer: `review_common_factor`.

**Verdict: the reviewed PARTITION reduction gives a negative answer to the proposed precision improvement in the standard polynomial-bit model, unless P=NP.** This holds already for positive rank-one costs with binary uniform marginals. The direct AMIN reduction below independently checks the connection to the exact question; later-literature priority remains unestablished.

## Primary-source scope

I inspected Altschuler and Boix-Adserà, *Polynomial-time algorithms for multimarginal optimal transport problems with structure*, Mathematical Programming 199 (2023), 1107–1178. Definition 3.2 specifies additive approximation of the minimum after subtracting coordinate potentials. Definition 7.2 supplies the low-rank factorization as input. The second remark after Theorem 7.4 asks whether the dependence on inverse accuracy can be made logarithmic for constant rank. Section 2 assumes polynomial entry encoding lengths in the mode size and number of marginals, and reports arithmetic-operation counts. These are the relevant hypotheses, rather than access to an explicitly stored exponential tensor. [Open primary article](https://link.springer.com/article/10.1007/s10107-022-01868-7).

## The reduced tensor fits the input class

Use the integers, even total `A`, and `ε=1/(16A³)` from [the reviewed one-monomial reduction](../results/positive-box-single-monomial-hardness.md). With one binary mode per integer, supply the tensor explicitly in factored form:

```
C = ⊗_i (1,1+εa_i),
C_z = ∏_i(1+εa_i z_i).
```

This tensor is nonzero and has rank exactly one, including nonnegative rank one. There is no sparse component and no cancellation between components. Its factorization has only two rational entries per mode. The same elementary-symmetric majorant used in the reduction gives

```
1 ≤ C_z ≤ ∏_i(1+εa_i) ≤ 1/(1−εA) ≤ 16/15.
```

Give each binary mode marginal `(1/2,1/2)`. The resulting MOT objective is exactly the midpoint convex-envelope LP already reviewed: the feasible objects are joint binary distributions with those means. Thus its YES and NO values lie respectively below `b+ε²/8` and above `b+ε²/2`.

This correspondence proves a high-precision value barrier directly. It applies also to an algorithm returning a sparse feasible solution or another representation from which its objective can be evaluated in polynomial time. An arbitrary implicit object with no efficient objective access is not silently treated as a value oracle.

## Direct reduction to the source's AMIN problem

The more direct argument avoids any possible loss in a reduction between MOT and its dual oracle. For mode `i`, set the potential at zero to zero and the potential at one to

```
π_i = εa_i+(ε²/2)(Aa_i−a_i²).
```

The earlier pointwise expansion now gives exactly

```
C_z−Σ_iπ_i z_i
 = β+(ε²/2)(S(z)−A/2)²+R(z),
β=1−ε²A²/8,
0≤R(z)≤ε²/8.
```

Consequently

```
YES: MIN_C(π) ≤ β+ε²/8,
NO:  MIN_C(π) ≥ β+ε²/2.
```

An additive-error estimate with `δ=ε²/32` distinguishes the cases using threshold `β+ε²/4`: even a two-sided error leaves a strict margin. This is exactly the tilted minimum in the AMIN definition. The cost tensor whose rank is restricted remains `C`; the potentials are separate oracle input. The minimum entry of this positive rank-one tensor with all potentials zero is easy, and no hardness claim for that different problem is made.

Since `Cmax≤16/15` and `log(1/δ)=O(log A)`, an algorithm polynomial in the rational input length and `log(Cmax/δ)` would decide PARTITION in polynomial time. The same conclusion follows for a high-precision MOT value algorithm using the baseline `b`.

## Encoding and arithmetic-model qualifications

An arbitrary PARTITION instance may have integer bit lengths much larger than its number of items. To meet the source's entry-bit assumption literally, let `L` be the original input length and append enough dummy binary modes to make the total number of modes at least `L`. Each dummy factor is `(1,1)` and its marginal is uniform; its potentials are zero. These modes preserve the tensor rank, cost range, AMIN value, and MOT value. Any original feasible law extends by independent dummy bits, and any padded law projects back. The padded factorization and all cost-entry bit lengths are polynomial in the new number of modes, while construction and padding remain polynomial in `L`.

The P≠NP conclusion is a **bit-complexity** barrier, and also excludes arithmetic algorithms whose operations can be implemented with polynomially many bits in polynomial time. A bound solely on unrestricted unit-cost arithmetic operations, allowing enormous intermediate representations or noncomputable real primitives, is not ruled out by an ordinary NP-hardness reduction. The result should not be phrased as that stronger model-independent lower bound.

The proposed logarithmic-precision improvement is therefore impossible in the usual polynomial-time computational interpretation, even at rank one, unless P=NP. The existing polynomial-in-inverse-accuracy guarantee is consistent with this reduction. No strong NP-hardness, fixed-accuracy hardness, or later-literature priority claim follows.

## Independent validation

I extended [the exact reduction verifier](../code/audit_single_monomial_hardness.py) to compute every tilted vertex value and test the `ε²/32` accuracy margin directly. All 120 seeded instances passed again, comprising 28 YES and 92 NO cases and 12,420 binary vertices. These are exact rational computations and supplement the checked identities above.
