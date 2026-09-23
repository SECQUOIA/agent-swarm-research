# Positive multilinear gaps on a fixed strictly positive box

Date: 2026-09-04. Status: question resolved by the independently audited bound in `results/positive-multilinear-positive-box.md`; exploratory history is retained below.

## Question

Is the term-by-term/convex-hull gap ratio for positive multilinear polynomials uniformly bounded on [1,2]^n, across dimension, degree, coefficients, and evaluation points? The unit-cube counterexamples do not settle this. Affine expansion of ∏(1+y_i) introduces positive lower-degree terms, and the original physical monomial's convex envelope is stronger than the sum of the expanded termwise convex envelopes.

## Exact existing product envelopes

For x_i=1+(r−1)u_i, let S=Σu_i, k=⌊S⌋, and θ=S−k. A physical product has convex envelope

V=r^k[1+(r−1)θ].

Its concave envelope is C=∫₀¹ r^{#{i:u_i≥t}}dt. These formulas are classical. Proposition4.1 of Warren Adams, Akshay Gupte and Yibo Xu, *Error bounds for monomial convexification in polynomial optimization*, gives them explicitly and credits Benson2004 and Tawarmalani–Richard–Xiong2013. See [primary manuscript, printed page22](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf). The convex formula uses adjacent-cardinality interpolation; the concave formula uses common-threshold rounding.

## A candidate global mixture

Let P=∏[1+(r−1)u_i] be the physical product under independent rounding. Let O be its expectation under fair endpoint orientations: one common U uniform on [0,1], and each coordinate independently chooses its success interval as [0,u_i] or [1−u_i,1]. Then

O=∫₀¹ ∏ᵢ[1+(r−1)(1[t≤u_i]+1[t≥1−u_i])/2]dt.

Both distributions preserve every coordinate marginal, and the same distribution applies to every monomial in a polynomial. Thus a scalar inequality

C−V≤K[(C−P)+(C−O)]

would imply a global ratio bound 2K by their equal mixture. The exploratory tests suggest K=2 might hold for r=2. This is a conjecture, not a theorem. Tests through degree40 found the worst equal-mixture ratio near4 at extremely unequal bilinear marginals.

Neither component alone works. Independence has arbitrarily small relative deficiency at a bilinear normalized point (ε,1−ε). Endpoint orientation has arbitrarily small relative deficiency at the degree-d normalized point u_i=1−1/d: after dividing product values by2^d, the true termwise gap tends to1/2 whereas the orientation deficiency is O(1/d).

## Useful low/high decomposition for r=2

Classify normalized coordinates as low if u_i≤1/2. Put q_i=u_i for low coordinates and q_i=1−u_i for high coordinates. Divide every product value by2^h, where h is the number of high coordinates. Let L(t),H(t) count low/high q-values at least t, for t∈[0,1/2]. Define

C_L=1+∫(2^L−1), C_H=1+∫(2^(−H)−1),
P_L=∏low(1+q_i), P_H=∏high(1−q_i/2).

Then C=C_L+C_H−1, P=P_LP_H, and

C−P=(C_L−P_L)+(C_H−P_H)+(P_L−1)(1−P_H).

Every term on the right is nonnegative. Also

C−O≥A/2+2∫[(3/2)^L−1][1−(3/4)^H],

where A=C_L−1−Σlow q_i. This follows from the integer inequality

2^L−2(3/2)^L+1≥(2^L−1−L)/2.

The local convex envelope after normalization is φ(Q_L−Q_H), where φ(s)=2^floor(s)[1+s−floor(s)] and Q_L,Q_H are the two sums of q-values.

## A failed simplification

The all-high inequality C_H−V_H≤2(C_H−P_H) is false. Independent reviewer audit_scaling supplied q=(1/2,49/100,1/100), with total failure mean1:

C_H=501/800, V_H=1/2, P_H=90147/160000.

Then C_H−V_H=101/800 while 2(C_H−P_H)=10053/80000, which is strictly smaller. This exact counterexample rules out that intermediate factor-two lemma, not the full mixture conjecture.

## Computation safeguards

`code/multilinear_ratio/positive_box_orientation_search.py` integrates the exact piecewise-constant conditional product formulas in floating arithmetic. The mixture logs are exploratory only. An early large-r run accidentally evaluated integer powers with NumPy integer arithmetic and overflowed; its r=10 and r=100 results in `positive_box_mixture_search.log` are invalid. The r≤2 cases did not overflow. The helper now converts r to float before exponentiation, and the corrected larger-r search is in `positive_box_mixture_large_ratio.log`. Floating near-zero gaps can still magnify cancellation, so no reported sampled maximum is a proof.

## Fixed-box bound completed

The decomposition above yields a global mixture with a uniform bound on every fixed common aspect ratio. Positive affine expansion then transfers it to arbitrary strictly positive boxes: with R=max(4,max_i upper_i/lower_i), the ratio is at most4R+6+2/R. Thus the bound is45/2 on [1,2]^n, independent of degree or dimension. The full proof and fresh independent review are linked in the canonical result. The earlier proposed factor4 bound remains unproved; it is not used. The root agent subsequently obtained a separate family whose ratio tends to the physical aspect ratio, establishing linear worst-case growth in that parameter.

## Sharp leading constant completed

The asymmetric split at normalized value1−ρ^(−1/2) proves the stronger upper bound2+(ρ+1)/(1−3/√ρ) forρ≥64. The proof uses the low independent-deficiency estimate D_IL≥ρ^(−1/2)A and only the endpoint cross deficit; the old symmetric-split inequality D_OL≥A/2 is deliberately not used outside its scope. Two fresh reviewers independently approved every step. Combined with the root agent’s variable-radix lower family, this proves worst-case aspect-ratio growth asymptotic toρ with leading constant one. Canonical statement: `results/positive-multilinear-positive-box-sharp.md`.

The stronger finite scalar inequality T≤ρD_I+2D_O remains a conjecture. A numerical search is retained in `code/multilinear_ratio/positive_box_rho_plus_two_search.py`; neither its success nor failure at floating tolerance is a certificate.


## Final status at orderly shutdown

The earlier conjectured scalar inequality `T≤ρ D_I+2D_O` has been proved by a coefficient induction that spreads only the global minimum and maximum marginal. Its canonical statement and full finite-step proof are in `results/positive-multilinear-positive-box-sharp.md`. It yields `max{2,ρ}≤C_box(ρ)≤ρ+2`, with the lower construction recorded separately. The earlier asymmetric leading-order proof is preserved in `notes/positive-box-asymmetric-upper-predecessor.md`; its old constants are superseded, not invalidated.

Two fresh reviewers checked the coefficient proof independently. Their notes are `notes/review-positive-box-rho-plus-two.md` and `notes/review-positive-box-rho-plus-two-second.md`. The first review includes 1,589 exact rational checks of all coefficients, boundary recurrences, the quadratic identity, and finite spreading. Numerical searches are supporting exploration, not premises of the theorem.

Open: the exact finite-ρ worst-case constant, including whether `C_box(ρ)=max{2,ρ}`, is not proved. The fixed-mixture optimality calculation is verified in [the development note](positive-box-rho-plus-two-proof.md). The already-started balanced-orientation refinement was completed during shutdown and passed the [closing independent audit](review-positive-box-balanced-orientation-closure.md). These narrower results do not determine the true worst-case constant. No new research direction was opened after the requested shutdown.


### Checked limitation of the two-law mixture

The factor `ρ+2` is optimal for a fixed mixture of independent and fair endpoint-orientation rounding when the guarantee must hold separately for every physical monomial. This statement does not establish optimality of the full polynomial gap ratio. The formulas below were independently checked by `audit_scaling`.

Write `w` for the orientation probability. A bilinear monomial with normalized means `(ε,1−ε)` has `D_I/T=ε` and `D_O/T=1/2`. Thus its limiting captured fraction is `w/2`. For the other obstruction, use one anchor of mean `ε` and `k` other coordinates of mean `1−ε/k`. Divide physical values by `ρ^(k+1)` and put `α=1/ρ`, `η=1−α`, `β=(1+α)/2`. For sufficiently small positive `ε`, the sum of means is exactly `k`, and

- `V=α`;
- `C=α+ε[η−α(1−α^k)/k]`;
- `P=α[1+(ρ−1)ε](1−ηε/k)^k`;
- `O=α+ε[η−2β(1−β^k)/k]`.

Taking `ε→0` and then `k→∞` gives `D_I/T→1/ρ` and `D_O/T→0`. Every fixed mixture therefore has uniform fraction at most `min{w/2,(1−w)/ρ}≤1/(ρ+2)`. The proved mixture attains that guarantee. This concerns only fixed mixture weights and uniform individual-term guarantees; coefficient-aware or nontermwise analyses could still improve the actual worst-case ratio.
