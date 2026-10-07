# Early independent review: quadratic section and counting interfaces

Date: 2026-10-05. Reviewer: Sol. The reviewed material is the current
`sections/04-quadratic.tex`, together with its interfaces in
`sections/03-counting.tex`, the relevant finite-law/growth proofs in
`appendices/A-finite-noise.tex`, and the model contract. The integration
decisions, independent-review brief, root early counting findings, and
the three requested prior Sol reports were read as context. They are not
substitutes for manuscript proofs.

This is an early review, not full-paper approval. Appendix B appeared
during the review. Its actual 902-line proofs were then read and checked;
the updated findings below supersede the initial missing-appendix status.
The files are being edited, so these references describe the recorded
review snapshots and must be checked again after integration is frozen.

The following hashes identify the last reviewed snapshots. Earlier reads
used older drafts; the review was updated against the versions listed here.

| File | SHA-256 |
| --- | --- |
| `sections/03-counting.tex` | `bf93c06c292064d33074db64a4f843e606342eaa2e3d7dfecfdb78e7b7a5abf7` |
| `sections/04-quadratic.tex` | `64c2376995141057870e7c225f2d5a38e682720ad9b0fd10e803d55010853b0b` |
| `appendices/B-quadratic.tex` | `a6ef088bf073341092b82baced9d9998dfd686da5f135c3e7cc0ab133ab854bf` |

References below use **04**, **03**, **A**, and **B** for the actual
manuscript files, not for historical mathematical notes.

## Decision

The section is not yet submission-ready. Two quantified claims require
correction: the Gaussian-like two-inertia theorem omits a necessary upper
bound on sampling accuracy, and the capped-moment limitation has an
incorrect lower integration limit. Empty mixed feasibility also needs a
consistent contract. Several smaller scope and boundary corrections are
listed below. These defects are repairable; none defeats the main subject.

The central interfaces for nonsmooth witnesses, continuous versus mixed
critical regions, best-competing labels, independent ambient Gaussian
proxies, and supplied versus intrinsic curvature are substantially correct.
Appendix B now supplies substantive proofs of the principal closure
theorems. The current general-k conditioned bound uses a constant c_k
depending on k, so the displayed coordinate-box packing count proves it.
The stronger absolute-c form is also provable by the optional Euclidean
packing argument below. No essential subsection of Appendix B remains
absent in this reviewed snapshot. The remaining scope corrections,
algorithm guards, and explicit real-parameter coverage clarification must
be integrated before approval.

## Required repairs in the actual text

1. **Major: the two-inertia Gaussian-like theorem permits unbounded sampling
   accuracy at fixed base input length.** Theorem `thm:qp:two`(b) at
   **04:251–252** requires only `2^b >= 2n D B`, but retains the
   `poly(I)(1+nu S/sigma)` work bound. With a fixed base instance, b can be
   arbitrarily large. The sampler has work polynomial in b and produces
   rational atoms whose bit length grows with b. This cost cannot be bounded
   by a polynomial in fixed I. Require the least sufficient positive integer
   b, require an explicit `b <= poly(I)`, or state the bound in I+b.
   The proof's claim `L_in <= poly(I)` at **B:254–255** consequently does
   not follow in case (b); its `O(log M)` height sentence must also distinguish
   the Gaussian accuracy b. The principal `thm:qp:gauss` correctly chooses
   `b <= poly(I)` at **04:504–505**. The uniform-grid case already chooses
   the least sufficient M and has no analogous defect.

2. **Major false lower bound: the moment limitation changes the tail variable
   without raising its threshold.** Remark `rem:qp:moments` at
   **04:281–283** claims
   `E min(B,Z^(k/2)) >= a integral_a^B u^(-2/k) du`, where
   `a=nu w_0/sigma`. The tail applies to `Z>t` only for `t>=a`, so the
   moment variable u requires `u>=a^(k/2)`. The displayed inequality can
   exceed B, an absolute upper bound on its left side.

   Take k=3, `X=[-1/2,1/2]^4`,
   `F(x_0,y)=-64 sum_(i=1)^3 y_i^2`, and sigma=1. Then nu=a=128,
   the box has r=8 inequalities, and B=256. The claimed lower bound is
   `128*3*(256^(1/3)-128^(1/3))`, approximately 503. It is strictly above
   480 since `128^(1/3)>5` and `2^(1/3)-1>1/4`, whereas the left side is
   at most 256. This is a symbolic counterexample; no experiment is needed.

   A valid repair is
   `a integral_max(1,a^(k/2))^B u^(-2/k) du` when the lower limit is
   below B. Choosing a=1 in the example is simpler. For fixed positive a
   and sufficiently large B, the order `a B^(1-2/k)` still follows.
   This remains a limitation of integrating the inverse-growth proxy,
   not an algorithmic lower bound.

3. **Major model boundary: empty mixed feasible sets are allowed but not
   consistently handled.** `def:qp:instance` at **04:34–47** assumes
   the relaxation is nonempty, yet allows X empty. The relaxation `{1/2}`
   with its variable integer is an allowed example. `thm:qp:gauss` at
   **04:506–507** permits an empty report; `thm:qp:uniform` at
   **04:539–542** promises a minimizer on every draw without that exception.
   The common definitions of f*, growth, and slice minima also need a
   nonempty domain. Appendix B calls a feasibility primitive at
   **B:616–618**, but should explicitly return an infeasibility report
   before using the nonempty-domain definitions and schedules. Either
   promise nonempty X or put the same feasibility branch in every mixed
   theorem. Its cost `f(n_z) poly(I)` fits the bounds. Qualify the final
   sentence of `lem:qp:face` at **04:314–315** by nonempty feasibility too.

4. **Moderate algorithm omission: guard the auxiliary reconstruction by value
   reconstruction.** Step (3) at **B:209–212** compares to hat f even on
   levels where step (2)'s condition is false, so hat f has not yet been
   defined. Attempt step (3) only after the certified value interval has
   yielded hat f. All subsequent correctness and termination arguments
   then apply unchanged. The reconstruction tolerance gives uniqueness:
   distinct rationals with denominator at most R differ by at least
   `1/R^2`, whereas the search radius is `1/(4R^2)`.

5. **Moderate precision needed when removing constant auxiliary ranges.**
   Appendix B now removes singleton ranges at **B:191–200**, fixing the
   positive-width boundary omission in the original section draft. For a
   partial removal, explicitly retain those coordinates' fixed values in
   the full inner problem and retain the full certified PSD matrix P.
   Deleting rows of T and recomputing P may destroy ambient PSD. For example,
   with `A=-I_2`, `T=I_2`, alpha=2, and
   `X={ (x_1,0): |x_1|<=1 }`, the full P is I, but deleting the constant
   second factor row gives `diag(1,-1)`. Embed reduced auxiliary queries
   in the original auxiliary space instead. If all factor ranges are
   constant, one full convex recourse solve at their values is exact.

6. **Moderate scope error in the regret sentence.** The inequality in
   `rem:qp:regret` at **04:575–576** is correct, but **04:577–579**
   gives order sigma S without distinguishing the laws. Deterministic
   uniform ambient regret is at most sigma S. Deterministic Gaussian-like
   regret is at most `sigma(b+20)S`. Aligned regret is at most
   `sigma sum_i range_X(Tx)_i`; `thm:qp:aligned` permits arbitrary T and
   does not imply a bound by original-coordinate sigma S.

   An explicit expected-regret Gaussian statement of order sigma S is
   available. If a standard marginal has support `[-K,K]`, K=b+20, and
   Kolmogorov error delta=2^(-b), integrating absolute-value tails gives
   `E|Z_b| <= sqrt(2/pi)+2K delta = O(1)`. Thus expected ambient regret
   is at most `C sigma S`. Label the expectation and retain the
   law-specific deterministic bounds.

7. **Minor quantifier and proof wording repairs.**

   - `lem:qp:pieces`(b), **04:340–345**, says `R_(z,S)(zeta')`
     contains the query a for variable zeta'. It contains a at
     `zeta'=zeta`, not at every residual parameter. State queried-pair
     inclusion. The proof at **B:315–316** correctly means that pair.
   - A checked supplied frame constant at **04:83–91** must be rational
     and included in I, or be computed as a rational lower frame bound.
     Exact rational elimination does not check an unspecified real input.
   - At **04:215–216**, near-optimal corners lie in the stated ball;
     entire retained cells need not. Each retained cell intersects the
     ball and lies in its enlargement by a cell diameter.
   - At **B:105–106**, the auxiliary concave function is a minimum of
     affine functions indexed by X, which can be infinite. Replace
     "finite minimum" by "infimum of affine functions"; compactness
     separately supplies attainment. Concavity is unchanged.
   - At **B:248**, use `kappa<=2+4Z<=6Z`. The first strict inequality
     is false when `nu/g>=1` because kappa is defined as `2+4nu/g`.
   - At **04:288–290**, the Gaussian variants need not use different
     law families. The two-inertia and closure algorithms can use one
     accuracy budget satisfying both. Their numerical bounds still
     differ. At **04:842**, qualify the nu-based table entry as the
     intrinsically normalized corollary; a supplied factor's general
     bound depends on alpha and c_fr.

## The conditioned exponent and optional stronger packing bound

The actual `thm:qp:conditioned` at **04:186–203** now states a
prefactor c_k depending only on k, rather than an absolute c raised to k.
The coordinate-box count at **B:230–234** proves this current contract:

    4^k(2 sqrt(k kappa)+2)^k
    <= [4(2 sqrt(k)+2)]^k (1+sqrt(kappa))^k.

For k<=2, this is `O(Z^(k/2))` when kappa<=6Z. The exact denominator
bounds, growth transfer `g_W=alpha g/(2g+alpha)`, and rational recovery
at **B:194–198, 223–246** supply `poly(L_in)+O(log Z)` levels and
polynomial work per query. After guarding reconstruction and embedding
removed fixed coordinates, these are sufficient for the absolute
polynomial and log exponent in `thm:qp:conditioned`(c).

If the author restores the stronger absolute-c prefactor, add the
following Euclidean packing proof. Let t<=k coordinates be refined.
Their spacing exceeds h/2, and projections of near-optimal corners lie
in the t-ball of radius `h sqrt(k kappa)/2`. Disjoint cubes of side h/2
centered on those lattice projections lie in the ball enlarged by
`h sqrt(t)/4`. Since the unit t-ball volume is at most
`(C/sqrt(t))^t`, their number is at most

    [C(sqrt(k kappa/t)+1)]^t
    <= C^t(k/t)^(t/2)(1+sqrt(kappa))^t.

For 1<=t<=k, `(k/t)^(t/2)<=exp(k/(2e))`; t=0 contributes one
projection. Unrefined endpoints contribute `2^(k-t)`, and incidence,
children, and queries contribute only further absolute constants raised
to k. This proves `c^k(1+sqrt(kappa))^k`. The current c_k theorem
requires no such extra proof.

The capped-moment upper bound at **B:256–279** is sound once the law's
bit height is bounded. Interleaving uses the same sampled objective and
is capped by the exact fallback, so zero growth and every atom are
included. For p=k/2 in {1/2,1}, the residual beta<=1/B contributes at
most one to the expectation. The integral is bounded by 1 for k=1
and log B for k=2, giving the distinct linear factor
`1+nu S/sigma`. An exact real Gaussian is a continuous probability
proxy, not a Turing input; the finite rational Gaussian-like counterpart
is valid with a least sufficient or polynomially bounded b. The older
result therefore adds a numerical bound and is not completely subsumed
by the degree-k closure bounds.

The current deterministic theorem remains continuous only. The integration
contract asks for the supported mixed deterministic extension with an exact
convex-MIQP oracle factor f(n_z). Its growth transfer, polynomial rational
height and guarded recovery use the same proof, with exact mixed
feasibility/range bounds and polishing. That requested extension is still
an integration/coverage item, not an extra smoothed theorem established
by the current continuous statement.

## Actual Appendix B proofs that pass

**Normalization and bit bounds, `lem:qp:normalize`, B:11–87.** The
characteristic coefficient gives
`mu=q_A^(-d)H^(-(d-1))` for every nonzero absolute eigenvalue. Its
logarithmic height is polynomial. Exact PSD halving gives
`nu<=beta<2nu`. Rational Jacobi rotations are exactly orthogonal;
bisection accuracy, geometric off-diagonal-energy decrease, and adding
rotation-denominator bit lengths give polynomial rational work.
Selecting the k diagonal entries below -mu/2 yields a projector error
bounded by `3n epsilon/mu`. Projection onto range A prevents leakage
into ker A. The perturbation of `A+2beta Pi` is at most 3mu/8,
leaving a PSD correction on range A and exact zero on its kernel.
The frame lower bound 63/64 follows from
`|| (I-R)B ||_F^2<=1/64`. These are actual proofs, not an outline.
The k=0 branch is separate; when n=1 the rotation loop is empty, so its
n(n-1) rotation estimate is not used.

**Square completion and every witness, `lem:qp:aux`, B:92–114.**
The equality, whole-space optimal value, and witness primal-gap transfer
are correct. Testing the same attaining witness at every other auxiliary
point gives a global quadratic upper model. Minimizing that model gives
`g^T Lambda^(-1)g<=2(V-V*)` for every witness, including ties.
The descent point may leave the search box: W is defined on all space,
and the box contains a whole-space minimizer. No kernel inclusion,
differentiability, or favorable subgradient selection is required.
Only the word "finite" in the concavity proof needs removal.

**Smallest-face fallback and degenerate active sets, B:117–145.**
A global minimizer on a smallest-dimensional face has positive definite
tangent Hessian, because a null tangent direction would give a smaller
optimal face. An independent active-row basis then gives a nonsingular
stationarity system. Enumeration keeps only feasible candidates;
multiplier signs are unnecessary for this nonconvex fallback. The
same argument slice by slice gives rational MIQP witnesses and values
of polynomial height. Box enumeration costs 3^k; equal fixed bounds
are dealt with by preprocessing or treating that coordinate as fixed.

**Critical bases and boundary derivatives, B:284–337.** The optimal
set of a convex slice is a polytope characterized by
`P_cc(y-x^0)=0` and the zero first-order gap. A vertex of that optimal
set has positive definite tangent curvature. Compressing nonnegative
multipliers to independent support and extending by zero multipliers
gives a full independent active basis. The resulting KKT matrix is
nonsingular, even with redundant constraints or lower-dimensional slices.

The derivative proof at **B:323–328** is the required algebraic one:
`D_(c,S) X_S=0`, and the multiplier contribution cancels identically.
It does not infer ambient derivatives from equality of values on a
region of empty interior. Every chart has
`nabla_a q=alpha(a-Tx_chart)` on the entire parameter space, but
W may remain nonsmooth and overlapping charts need agree only in value.
The Cramer determinant bound at **B:330–335** uses only fixed response
matrices, so Theta is selected before sampling. Pure integer slices
use the empty continuous system and a constant label response.

**Best-competing labels and isolation, B:339–388.** The union of 2n_z
integer exclusions is exactly all different label tuples. Subtracting
the common auxiliary quadratic bounds all slice increments in one
common interval of slopes, giving the whole-cell gap threshold without
an extraneous factor two. Equality is safe. The primal-gap transfer
at **B:360–365** produces two distinct feasible labels of the original
sampled objective when the test fails, with the required h<=1.
The isolation proof compresses each coordinate group into one line,
uses integer slope differences and at most U_i-L_i envelope switches,
and conditions on all other original coefficients. Conditional costs
may contain arbitrary continuous recourse. The original ambient integer
coefficients remain independent; projected aligned coefficients do not.

**All-corner tests and fixed ambient tubes, B:391–455.** Extraction at
every corner ensures the near-optimal corner's test was attempted. An
invertible chart Hessian maps a crossed region boundary to a hyperplane;
a singular Hessian has its entire gradient image in a hyperplane. Zero
region normals cannot fail within a cell containing the query. The
active-witness bound controls distance to either hyperplane. Pullback
normals satisfy `T L=u`, hence `||L||>=1` when `||T||<=1`.
These functionals are a counting device; the algorithm need not construct
irrational normalized normals. Tube probabilities use original
independent coordinates or Gaussian-proxy transfer, never a false
conditional product law for uniform projected noise.

**Section counts, B:460–498.** For continuous/separable pieces, valid
formulas agree on overlaps, so only region endpoints need be counted.
General mixed pieces require pairwise quadratic crossings as well;
P_sec=2R^2 covers both those roots and region endpoints. The 2k+1 local
queries and isolated breakpoint truth values are included. This proves
the advertised interval count once coverage for every real conditioned
parameter and every feasible fixed label is stated explicitly.

The present `lem:qp:pieces` speaks only of rational queries, while the
section lemma fixes arbitrary real values of all other coefficients.
The missing statement is easy to prove: for a fixed feasible label,
the finitely many nonsingular bases have closed polyhedral validity
sets in joint (a,zeta) space. Extraction covers every rational pair,
so their finite closed union covers the entire real parameter space.
Alternatively, optimal-set vertex and multiplier existence give the
same coverage directly for real parameters, with computation required
only at rational queries. Add this existence-versus-computation sentence;
do not condition coverage only on the sampled winning label.

**Dependent uniform volume, B:500–534.** The change of coordinates
`S=[T^T,V_0]`, fiber box volume, projected-zonotope volume, Jacobi
complementary minors, and Cauchy–Binet give the exact minor sum and
sqrt(n) bound. Applying it only to coordinates with factors below one
justifies the product of probability caps. This correctly handles
residual-dependent intervals without claiming projected independence.

**Gaussian proxy and weighted count, B:537–596.** Factor and residual
are independent under the isotropic Gaussian proxy. Principal factor
covariances lie between sigma^2 and sigma^2/c_fr. The product density
majorant is valid. Neighbor comparisons confine the event to both a
short residual-dependent interval and a deterministic location interval;
only their intersection is needed, as **B:562–563** correctly says.
The weighted lattice estimate retains its probability cap on coarse
meshes. Its core contribution is bounded by `C W phi_s(0)+C+2` and
each tail by `1+C/2`, proving the stated `C W phi_s(0)+2C+4`.
Marginalizing away coordinates whose factors exceed one justifies the
product of minima, with c_fr^(-|Q|/2) outside those minima. This gives
the count independent of the enlarged search box.

**Finite budgets, exact completion and expectation, B:604–713.**
The continuous aligned law uses direct finite-grid counts. Uniform and
Gaussian-like laws use the deterministic full grids, not an independence
claim for adaptively selected cells. Product Kolmogorov transfer sums
node errors over all levels; Q_J bounds every deterministic grid node.
The budget sizes have polynomial bit lengths. The mixed schedules at
**B:628–638** enforce h_J<=1, so C_gap is support-independent. In
case (C), `J(t)<=J(0)+t` and `b(t)<=poly(I)+O(k t)` make the support
loop finite with polynomially bounded t,J,b. It is not a circular
post-draw choice. Terminal nonclosure forces one fixed tube or one
label-gap event. The all-draw fallback is the same sampled objective;
its event probability times its cost is polynomial. Queried coefficients,
polished witnesses, critical responses, cell-face solutions, and final
rational outputs have polynomial height. The supplied-frame formula
and intrinsic alpha<4nu corollary remain distinct. Explicit empty
feasibility handling is still required as noted above.

**Uniform count barriers, B:717–792.** The residual-dependent midpoint
example gives the claimed sharp probability. For its n=1 case, the
formula is immediate from a scalar uniform law; the written min/max
joint-density derivation is for n>=2. The quadratic block construction
has one negative eigenvalue, unit frame, projected width 8 and
alpha<4nu. On its constant-probability event, the auxiliary derivative
is smaller than 3/m over the required interval. The mesh choices give
at least m/32 local nodes and sqrt(m)/16 nearly optimal nodes. Products
of independent blocks yield the stated constants. The finite-grid
extreme-value and variance estimates are conservative and valid.
The manuscript correctly describes these as obstructions for its
counts, not lower bounds for closure's total runtime.

**Separable outputs and anisotropic normalization, B:797–901.**
Integer forward differences, curved responses, closed knot states,
endpoint half-lines, and flat-piece endpoint choices cover all scalar
tilts. Rational breakpoints ensure rational continuous responses and
values. Every separable region certifies the global recourse value,
so arbitrary integer dimension needs no competing-label gap test.
The fallback covers every combination of labels and listed continuous
pieces with a rational quadratic box problem.

Rational row rotations and dyadic rescaling preserve
`U^T Lambda U=alpha T^T T` exactly. The frame bounds follow from
rayleigh diagonals and the 1/128 scaled off-diagonal error. Small singular
values change bit heights rather than the numerical count. Balanced
curvature meshes give the safe C_k=1+8k. The witness norm, cell diameter
and rational C_tube at **B:882–888** bound every unresolved tube, and
the final Gaussian support loop at **B:892–900** is finite and has
polynomial sampling precision. The numerical beta parameter is the
supplied concave curvature, as explained at **04:812–815**, and can
exceed the objective's intrinsic negative curvature. Full row rank is
explicit after preprocessing; no dependent-row removal claim is made.

## Shared interfaces and dependencies still to resolve

The quadratic uses of local intervals, independent tensor counts,
balanced meshes, corrected pruning and deterministic-grid replacement
are sound at **03:59–213, 277–292**. The lower-semicontinuous growth
proof at **A:234–321** is valid and applies to mixed feasible sets via
an infinite-valued extension. The actual finite Gaussian-like law has
bounded support and polynomial production; its coordinates after
projection need not be independent.

The existing early foundations review separately records issues in the
generic fallback output format, arbitrary extra-bit-height dependence,
universal architecture wording, singleton thresholds, and exact Taylor
intermediate heights. This report does not re-approve those interfaces
or their later repairs. The rational quadratic fallback has a simpler
output contract and does not need conversion to a shared algebraic root.

No essential Appendix B subsection is absent in the reviewed 902-line
version. The specific pending proof clarification is real conditioned
fixed-label coverage; the algorithm's reconstruction guard and full-model
embedding also need explicit integration. The mixed deterministic
conditioned extension requested by the integration contract is absent
from the current theorem. Full frozen review must check these changes
and all common output/sampling interfaces again.

No primary-source literature statement was independently checked here.
`prop:qp:primitives` remains a Luna citation dependency, in particular
exact convex-MIQP output and the absolute input-polynomial exponent.
The same applies to normalization attribution and claimed relations to
prior results. Internal proof notes and prior reviews are not citations.

## Checks performed

I used scoped cat, sed, nl, rg, wc and sha256sum reads of the actual
manuscript/interface files, integration documents and relevant early
reviews. I read Appendix B after it materialized and checked its actual
proofs. The analysis supplied a symbolic counterexample to the moment
lower bound, a valid optional Euclidean packing argument, and the real
coverage extension. No TeX, historical note or unrelated file was edited.
No delegation, literature work, optimization experiment, original diagnostic,
project-wide verification or CI inspection was performed. Only this
authorized review was written. The scoped Python format check passed:
final newline, no trailing whitespace, and balanced
code fences. Source hashes were checked separately. These targeted checks
are not CI or project-wide verification.

## Later source movement observed before handoff

The actively edited files changed after the principal proof review. The
following hashes were observed at handoff; they are not a frozen full
re-review of all changes:

| File | Later observed SHA-256 |
| --- | --- |
| `sections/03-counting.tex` | `f54a72dca58da3d71595a1e4159ad9c356555ba5ffa88b670fada18778535f83` |
| `sections/04-quadratic.tex` | `462e049f038ae565ec605cdcc0a7b545964c9f7d6a001731e7f50fb68a7a2c5f` |
| `appendices/B-quadratic.tex` | `140b358d7eb3088bca1e75274e332e3398fa08b77527df0c9b48b96a5cd76693` |

Targeted reads of this later version confirm that the Gaussian accuracy
issue remains at **04:253–254**, the moment-integral issue remains at
**04:283–285**, empty mixed feasibility remains at **04:35–49,
555–557**, and the reconstruction guard remains missing at **B:209–212**.
The later critical-region statement still needs the queried-residual
qualification at **04:343–347**. The factor constant remains unspecified
as rational at **04:85–93**.

The regret remark has been repaired at **04:589–597**: it now states the
Gaussian support radius and the aligned projected widths explicitly.
Required repair 6 above is therefore resolved in this later observed
version. The fiber-sharpness product now consistently uses total dimension
N at **04:635–637** and **B:729–731**.

The uniform count-barrier proof was moved out of Appendix B, which now
references Appendix G at **B:734–735**. Its section statement at
**04:645–659** also strengthens the finite-grid threshold from
M>=64m^2 to M>=32. The earlier proof checked above establishes the former
threshold. The new Appendix G proof and its stronger finite-grid contract
remain pending in this report; no approval is inferred from the reference.
The separable proofs now occupy **B:739–844**, and their narrow reread
confirms the same scalar, anisotropic and finite-budget arguments. A
frozen integrated review must verify the transferred barrier proof,
all resolved items and the latest counting interfaces.
