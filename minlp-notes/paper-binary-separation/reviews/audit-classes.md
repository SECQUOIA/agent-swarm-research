# Analytical audit of the inequality-class consequences

Audit date: 2026-10-06. Scope: §5, Corollaries 4–10, their revisions, and the
relevant membership and quantitative claims in the binary-separation note.
This audit independently derives the mathematical transfers. It accepts the
existing computational records and does not rerun them. Literature verification
belongs to the separately assigned literature audit.

## Verdict and required wording corrections

The class reductions, polynomial encodings, distinct-point construction, and
revised maxima are correct. No obstruction to the stated NP-completeness
results was found. Three wording corrections should be made in the paper:

1. Exact lists of the generalized Boolean quadric inequalities must identify
   `(v,s)` with `(-v,-s-1)`. Corollary 8 also has the violated datum
   `(S,T,s)=({g},C,-1)`; Corollary 9 also has
   `(S,T,s)=(∅,C∪{g},-2)`. They reproduce the listed inequalities, but they
   contradict literal claims of a unique data triple. State exactness up to
   this equivalence.
2. Every positive maximum violation is conditional on a cover existing. With
   maximum positive violation defined as `max{0,sup(violation)}`, it is zero
   on a no-instance. The first maximum statements in §9 lack this condition.
3. Pure hypermetric and odd-clique separation require different qualifications
   under switching. Rounded psd, gap-1, and odd-clique families are invariant
   under switching; hypermetric and pure hypermetric families are not. The
   supplied proofs use this distinction correctly. Preserve it in condensed
   statements.

Facet conclusions can be proved directly, removing dependence on the disputed
printed orientation of Padberg's cut-facet condition. The self-contained proof
below also shows that the maximizing pure vectors in Corollary 10 are facets.

## Exact conversion and normalization

For arbitrary coefficients `b=(b₀,z)` with total sum `σ`, substitution of the
covariance map gives

`Q(b,d)=σδᵀz-zᵀMz`.

Consequently, for `σ=1`, `Q=-g_M(z)`. For `σ=0`, `Q=-zᵀMz`, proving the
negative-type/Gram equivalence directly. The latter statement remains true
whether negative-type tests use real or integer vectors, since a strictly
negative quadratic direction can be approximated by rational directions.

The unhalved Boros–Hammer slack is

`h_Y(v,s)=vᵀMv-(2s+1)δᵀv+s(s+1)`.

With `β=(2s+1-Σv,v)`, one has exactly

`h_Y(v,s)=(σ(β)²-1)/4-Q(β,d)`.

This is a bijection between Boros–Hammer data and rounded-psd coefficient
vectors with odd total sum. Global negation of `β` corresponds to
`(v,s)↦(-v,-s-1)` and preserves the inequality. The displayed finite families
(10)–(12) have slack `h_Y/2`; their positive violation is therefore half the
cut-scale rounded-psd violation. In split notation,
`h_Y(v,s)=q_Y(s,-v)`. These identities are valid for every rational input,
without a feasibility or definiteness assumption.

Hypermetric vectors have gap one: the all-positive signing gives value one,
and odd parity excludes zero. Therefore hypermetric ⊂ gap-1 ⊂ rounded psd.
The union of all k-gonal families has the rounded-psd inequalities when the
total sum is odd and the psd inequalities when it is even. The base hard
points are psd and have rounded-psd violators only with total sum ±1, so all
four infinite families have the same yes/no answer there.

## Switching and finite-family hardness

Complementing variable `g` is the congruence `Y↦AYAᵀ`, where row `g` of `A`
is `e₀-e_g` and all other rows are unchanged. Since `A²=I`, positive
definiteness is preserved. Writing `v'` for `v` with entry `g` negated gives

`h_{AYAᵀ}(v,s)=h_Y(v',s-v_g)`.

The shift in `s` is essential. This formula is involutive, so it transfers
the entire exact list of violators, not merely a selected witness. On the
base point the data are `(1_C-e_g,0)` and its equivalent opposite datum.
On the complemented point they are `(1_C+e_g,1)` and its opposite. They
give respectively Padberg cut and clique inequalities, both with positive
violation `1/(4N)`. No other generalized finite-family inequality is
violated, up to the equivalence above.

The base cut point and its switched image lie in the metric polytope and the
elliptope interior. Switching acts as diagonal-sign congruence on
`Z=J-2D`, and it preserves the support and gonality of rounded-psd vectors.
It also permutes the triangle/perimeter inequalities. However, on the
one-variable switched cut point the rounded-psd violators have total sum
±3, and there is no hypermetric violator. This is a useful check against
an overly broad assertion of hypermetric switching invariance.

The moment entries before and after complementing `g` have common
denominator `4N` and numerators at most `4N`. The finite generalized-family
NP certificate needs only `(S,T)`: if `ℓ=x(S)-x(T)`, its violation as a
function of `s` is `-s²/2+s(ℓ-1/2)+c`, maximized at `s=floor(ℓ)`. When
`ℓ` is integral there is a tied maximizer at `ℓ-1`; the stated choice
still works. This integer has polynomial bit length. The clique family
has finitely many `s∈{0,…,|S|-1}`, and the cut family uses `s=0`.

## A direct proof of the required facets

Let `K` have size `t≥3` and `1≤r≤t-2`. The clique inequality is the
nonnegativity of

`F(x)=Σ_{i<j∈K}x_ix_j-rΣ_{i∈K}x_i+r(r+1)/2`.

Its tight binary points have `|x_K|=r` or `r+1`. Suppose a multilinear
quadratic `p=c+Σa_ix_i+Σa_ijx_ix_j` vanishes on both layers. For distinct
`i,j`, compare `p(1_{R∪{i}})` and `p(1_{R∪{j}})` for `|R|=r-1` and `r`,
where `R⊆K\{i,j}`. Both comparisons give

`a_i-a_j+Σ_{k∈R}(a_ik-a_jk)=0`.

For any `k∉{i,j}`, choose `R⊆K\{i,j,k}` of size `r-1`; the range on `r`
ensures that this is possible. Subtract the comparison for `R` from that
for `R∪{k}`. Thus `a_ik=a_jk`. All pair coefficients equal a common value
`a`, and the first comparison then implies that all linear coefficients
equal a common value `b`. Evaluation on the two layers gives
`b=-ra` and `c=r(r+1)a/2`. Hence `p=aF`.

Unused variables introduce no extra affine equation. Set all unused
variables to zero first. Then set one unused variable to one; the difference
is an affine function on `K` vanishing on both layers. Such a function is
zero, since comparisons show all its linear coefficients equal and the two
layer values then force them and the constant to vanish. Setting two unused
variables to one eliminates their pair coefficient. This proves uniqueness
of the equality hyperplane in the full Boolean quadric space. That space
has full dimension, since the monomials `1,x_i,x_ix_j` are independent on
the Boolean cube. Therefore the clique inequality defines a facet in the
full ambient polytope.

Complementing variables is an affine polytope automorphism. The covariance
map is a linear bijection from the Boolean quadric polytope to the rooted
cut polytope: this follows directly on the vertices and their convex hulls.
Both maps preserve facets. The base cut violators are complements of
clique facets with `t=q+1,r=1`. The all-positive odd-clique inequalities
on `2q-1` points come from `t=2q-1,r=q-1`, which meets the range above.
Their sign switchings also define facets. Every pure/odd-clique violator
in the orthogonal lift has this same odd support size, so all listed
violators, including the maximizing ones, are facets.

This proves the facets needed here. Attribution and the full historical
facet conditions remain questions for the literature audit; no claim about
the disputed orientation of the printed cut-facet condition is required.

## Distinct positive definite points and exact pure-family classification

With `m=q-2` and `τ²=1/(8q)`, let `M̃=M⊕τ²I_m`. The new points have
independent orthogonal directions and positive distances from the root,
from each other, and from every old point. Thus they are distinct, and
`M̃` is positive definite. Its correlation polynomial is

`g_M̃(z,w)=g_M(z)+τ²Σ_jw_j(w_j-1)`.

The added term is nonnegative for integers. Hence all hypermetric violators
come from a cover and have coefficients

`b=(2-q-Σw,1_C,-1,w)`,  `Σ_jw_j(w_j-1)<4q`.

Their gonality is at least `2q-1`, by the triangle inequality applied to
the root coefficient and the sum of the new coefficients. The Schur
complement parameter is `s̃=s+mτ²`, so
`εs̃<1/2+1/(8N)<3/4`. The scaled moment point and its subtraction of
`e₀e₀ᵀ/4` are positive definite. This excludes all rounded-psd violations
with `|σ|≥3`. The common denominator `8qN` is polynomial, and all moment
and cut coordinates are in `[0,1]`. The absence of low-gonality violators
gives all metric inequalities for `q≥3`.

For a pure vector, let `a` new coefficients be +1 and `k` be -1. The root
constraint gives `k-a≥q-3=m-1`, while `a+k≤m`. Hence `a=0` and
`k∈{m-1,m}`. The pure vectors are exactly

`b*=(0,1_C,-1,-1_m)` and
`(-1,1_C,-1,-1_m+e_j)` for `1≤j≤m`.

Odd-clique violators are these and their global negatives. Their respective
cut-scale violations are `(q+2)/(4qN)` and `(q+3)/(4qN)`. The latter is
the exact positive maximum when a cover exists. Hypermetric and rounded-psd
maxima are `1/(2N)`, attained when `w∈{0,1}^m`.

Switch on `U={g,o₁,…,o_m}`. An all-positive odd-clique vector can arise only
when `w∈{0,-1}^m` and `2-q-Σw∈{0,1}`. Writing `k` for the number of -1
entries forces `k=m`, and the root coefficient is zero. Therefore the
violated all-positive clique inequalities are exactly the supports `C∪U`,
with size `2q-1` and violation `(q+2)/(4qN)`. Switching preserves the
elliptope interior, metric feasibility, the bounded denominator, and the
absence of rounded-psd inequalities of bounded gonality. Even-support
all-positive clique inequalities, if included in the convention, are psd
inequalities and hold at these points.

## Certificates for infinite families

Gap-1 membership on arbitrary rational inputs does not require computing
the gap. A sign vector `s` witnessing `|sᵀb|=1` switches the violated
inequality to a hypermetric inequality. Conversely, any hypermetric
violation on a switched input gives such a gap-1 violation; the witnessed
value one and odd parity certify the exact gap. A certificate is the sign
set together with a polynomial-length hypermetric witness. Switching
preserves polynomial input length.

Rounded-psd membership can also be proved directly. For rational unit-diagonal
`Z`, the test is `bᵀZb<1`, `Σb` odd. If `Z` is indefinite, a short integral
negative direction `y` obtained by exact symmetric elimination makes
`b=e₀+2ty` a violation for a polynomial-bit integer `t` chosen sufficiently
large. If `Z⪰0`, choose a nonsingular principal block `Z_KK` and set
`P=Z_{K,·}`, `G=Z_KK^{-1}`. Then `Z=PᵀGP`. A violating vector has
`u=Pb` with `uᵀGu<1`, so every coordinate satisfies `|u_i|<1` by
Cauchy–Schwarz and the unit diagonal. Its denominators divide a common
denominator of `P`, so `u` has polynomial bit length. The integral system
`Pb=u`, `Σb-2t=1` has a solution, and Hermite normal form supplies one
of polynomial bit length. It retains the violation and odd parity. This
also supplies a standalone rounded-psd proof instead of referring to the
older split note. The supplied split-witness lemma is sufficient as well.

Pure, odd-clique, and all-positive clique certificates have coefficients
in `{0,±1}` or identify a subset, so their membership is immediate.
The union of all k-gonal families uses the rounded-psd certificate or a
short integral negative direction. All rational hardness encodings here
have a polynomial common denominator as well as polynomial numerators,
so the strong-hardness assertions are unaffected by rational encoding
conventions.

Gap-0's sign-hyperplane criterion and polynomial certificate are consistent
with these transfers. Its reduction stays at indefinite points and cannot
be promoted to solver-relevant positive definite hardness. No transfer
here settles general gap separation at psd points.

## Checks actually performed

Read `AGENTS.md`, the identified sections of the note, review rounds 1–3,
and the referenced split-witness proof with targeted `cat`, `sed`, and `rg`
commands. Derived all displayed conversion identities, the finite-family
facet proof, the pure-vector classification, and the maxima analytically.
No computational experiment, project-wide check, or CI check was run.
