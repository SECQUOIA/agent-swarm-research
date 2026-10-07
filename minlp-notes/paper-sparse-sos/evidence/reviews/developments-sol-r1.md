# Independent review of the extension developments

Date: 2026-10-05. Reviewer: Sol, independently of `audit_extensions`.

## Snapshot and verdict

Reviewed `evidence/AUDIT-EXTENSIONS.md`, Sections 4, 6.1–6.4, and 7.6, together with the supporting constructions in Sections 1, 3, 5, and 7.1–7.5. Snapshot metadata recorded during the review:

```text
mtime: 2026-10-05 23:14:29.541619205 -0400
size: 45282 bytes
SHA-256: 4666f3ed32a98012ac9ce844d9c5e934d55b5b57fdc2a168999f7480ef7bef7b
```

Line locators below refer to that snapshot. Supporting source reads included `general-constraints-kernel.md`, Sections 4–5; `rational-sparse-certificates.md`, Sections 4–6; and the ordinary kernel and exact-consistency definitions already reconstructed in this reviewer's earlier `AUDIT-KERNELS.md`.

I accept both new mathematical developments: the labelled ordinary-module exact correction in Section 6 and the constrained density domination in Section 4. Their finite-order estimates and fixed-width rate conclusions follow under the stated hypotheses. The pseudo-label-mass normalization issue is correctly resolved by distinguishing the feasible-point estimate from the data-only maximum budget. No substantive defect was found.

I also accept the rational error majorant and the rate-to-real-membership implication in Section 7.6. The underlying ordinary-module rational theorem already appears in `rational-sparse-certificates.md`, Section 6, and must not be called a new contribution. Polynomial-bit rational witness existence is established by the algebra. The theoretical polynomial-time construction statement still requires the exact external rational strong-feasibility theorem identified by the author; this review does not supply that literature reference.

## Accepted finite-state contract

The Section 6 theorem is accepted with all of the following conditions retained:

- A finite running-intersection tree covers both continuous and finite-state variables. Each finite variable has a specified finite state set. Each bag has an explicit list `A_b` of permitted local labels, and the globally permitted assignment set is nonempty.
- Every label has the same continuous product box. The same univariate source kernel and the same product reference measure are used in every bag and label. This is not a theorem for label-dependent boxes or additional label-dependent continuous constraints.
- Each `L_{b,a}` is defined through total degree `2R`, satisfies the ordinary singleton box module, has mass `tau_{b,a}>=0`, and the masses sum to one in each bag.
- Separator equalities sum the functionals over every fiber of a shared finite-state assignment, for all continuous separator polynomials through degree `2R`. Empty fibers have sum zero. There is one empty finite assignment when the discrete separator is empty.
- For continuous width `w>=1`, choose `s>=max(2,d_infty)`, even `N>=2`, and `R>=wD`, with `D=2(s-1)(N+1)`. The objective degree lies in the moment-bound range; the author's additional explicit `R>=d` is harmless and follows from these choices.
- The common shift is `Delta_w tau_{b,a}`. The scalar `Delta_w` and denominator `1+Delta_w` are common to every bag and label.

Under those conditions, equations (14) and (15) are valid, the constructed law has the specified permitted finite-state support, and the fixed-width rate (18) has no extra label-count, bag-count, or diameter factor outside `C_mix` and the expanded SDP dimensions.

### Mass control and the zero-mass boundary

The ordinary-module identity for `1-T_beta^2` is valid through degree `2|beta|`. Applying an unnormalized positive functional gives

`0<=L(T_beta^2)<=tau` for `|beta|<=R`.

The two-by-two PSD condition on `1,T_beta` then yields

`|L(T_beta)|^2<=L(1)L(T_beta^2)<=tau^2`.

Thus `|L(T_beta)|<=tau`. No normalization by `tau` is used. If `tau=0`, every diagonal of the degree-`R` Chebyshev moment matrix vanishes; PSD forces every entry to vanish. Products of two polynomials of degree at most `R` span all local monomials through degree `2R`: split any exponent of total degree at most `2R` into two exponents of total degree at most `R`. Hence the entire zero-mass functional vanishes, including its highest-degree moments. This proves the author's zero-mass conclusion rather than assuming that an unnormalized functional has a representing measure.

Empty continuous bags present only a scalar label mass. Their tensor source kernel is the empty product one; their signed and corrected densities are both exactly `tau`. All-discrete models have only the consistent finite-state bag probability vectors. Tree gluing makes their hierarchy exact at order zero. No expression involving `r/w` or `R/w` should be used when `w=0`.

### Independent reconstruction of the residual estimate

For a fixed output and a residual subset of size `j` in a continuous bag of size `v`, write `G=prod Q_i` over the complementary coordinates and `H=prod r_i` over the residual coordinates. Since `G` is globally SOS,

`G(delta^{2j}-H^2)`

has an ordinary-module certificate by telescoping the single-coordinate certificates for `delta^2-r_i^2`. All remaining factors are SOS, including previous residual squares. The maximum certificate degree is `(v+j)D<=2R`. Also `G(a+bH)^2` is a sum of permitted squares because each square factor has degree at most `(v+j)D/2<=R`. The resulting weighted PSD matrix gives

`|L(GH)|<=delta^j L(G)`.

The coefficient estimate is applied only to `G`, whose degree is `(v-j)D<=R`, giving

`0<=L(G)<=tau B^{v-j}`.

This proves equation (16) including zero mass. The terms with no residuals and one residual are nonnegative under the ordinary module. Their degree is at most `vD`; multiplying a single interval residual certificate by the other SOS factors does not introduce generator products. Summing only the potentially negative terms with `j>=2` proves

`hbar_{b,a}>=-tau_{b,a} Delta_v>=-tau_{b,a} Delta_w`.

The same degree ledger as the continuous transfer applies. There is no extra localizer degree cost caused by finite labels, since they index separate functional blocks rather than polynomial degrees in a continuous surrogate.

### Reference correction and separator fibers

The exactly normalized kernel has output integral one identically as a source polynomial. Consequently `hbar_{b,a}` has mass `tau_{b,a}` and its continuous marginal deletes precisely the removed source factors. Summing those marginals over a separator-label fiber gives the source polynomial in the required equality constraint.

The corrected density is

`h^+_{b,a}=(hbar_{b,a}+Delta_w tau_{b,a})/(1+Delta_w)`.

It is nonnegative and still has mass `tau_{b,a}`. Marginalizing the added reference term gives `Delta_w tau_{b,a}`, because the reference is a product probability measure. Summing it over a shared label fiber gives `Delta_w tau_{b,S}(s)`. The masses `tau_{b,S}(s)` agree by the separator constraint at polynomial one. Thus the signed part, added part, and denominator all agree at the separator. An absent fiber remains zero.

A concrete boundary check shows why the mass factor is essential. Suppose a parent has two labels for a shared finite variable, while a child has three local labels whose shared-variable fibers have sizes two and one. Assign parent masses `(1/2,1/2)` and child masses `(1/4,1/4,1/2)`. These are consistent. Adding the same bare constant separately to each label changes total masses by different amounts and changes shared fiber masses by different amounts. Even separate bag renormalization does not restore the original shared probabilities. The author's mass-scaled correction avoids this failure.

### Conditional gluing, missing fibers, and support

For each shared label `s` and continuous separator output `y_S`, the corrected separator density is a nonnegative sum of child label densities. Where it is positive, division by that density defines a conditional law on the child's new discrete labels and new continuous coordinates: sum over extending labels and integrate new coordinates. The numerator sums and integrates to the denominator, so the conditional law is normalized. The product box is the same for each label, which is needed for this marginal calculation.

Where the separator density is zero, the conditional law may be chosen arbitrarily. In particular, an empty label fiber need not possess an allowed conditional extension on that null event. Such choices do not affect bag marginals or almost-sure feasibility. Running intersection identifies the child's previously assigned variables with its parent separator. Induction constructs a global law preserving every mixed bag law. Each bag has zero probability for a forbidden local label; a finite union of these null events gives global finite-state support in `mathcal A`.

This establishes support in the common continuous box and in the globally permitted finite assignments. It does not establish support in additional label-dependent continuous domains.

### Objective error and a priori normalization

The exactly normalized operator fixes constants and matches the original SOS operator on every positive Chebyshev mode. Tensor expansion therefore gives coefficient error `C_{b,a} Gamma_v`. Both the original and transformed polynomials have degree at most `vD<=R`: for the original objective, `deg f_{b,a}<=v d_infty<=v s<=vD`. Applying mass-scaled moment control yields error at most `tau C_{b,a} Gamma_v`.

The correction identity compares two nonnegative measures of the same mass:

`int f h^+ - int f hbar = Delta_w(tau int f dmu-int f h^+)`.

Their difference is at most `Delta_w tau Omega_{b,a}`. This proof is valid at zero mass without division. Constants depending only on labels cancel exactly because the correction preserves each label mass, rather than just the total bag mass.

Equation (14) is therefore a valid bound for the particular feasible family, weighted by its pseudo-label masses. It is not by itself a data-only coefficient budget. Bag normalization supplies the separate valid inequality

`sum_a tau_{b,a} C_{b,a}<=max_a C_{b,a}`,

and similarly `sum_a tau Omega<=2 max_a C`. Summing proves equation (15) with `C_mix=sum_b max_a C_{b,a}`. The error is now independent of the chosen feasible point, so taking an infimum legitimately yields the unconditional gap and rate conclusions. The author already makes this distinction explicitly at lines 358–371; retain it.

If `C_mix=0`, all labelled objectives depend only on finite labels, and the constructed global law preserves their bag label probabilities exactly. The hierarchy is then exact even if continuous variables are present. A large label-dependent constant does not invalidate the zero coefficient budget.

### Pruning and finite labelled duality

I accept the pruning argument at lines 476–478. The scalar mass equations alone define consistent finite-state bag probabilities and therefore admit discrete tree gluing. Any local label without a global extension has zero mass in every feasible family. The zero-mass result above forces its whole functional to vanish. Deleting these blocks preserves the primal feasible objectives.

Every retained label has at least one global extension. Assign positive probability to every globally permitted finite assignment, independently of a continuous product law of positive interior density. Each retained label then has positive mass; every permitted nonzero square and singleton-box-weighted square has positive expectation in that label. Hence every retained labelled PSD block is positive definite. This proves primal Slater for the pruned finite SDP. The labelled feasible moment set is compact by the mass-scaled monomial moment argument, and the objective is bounded. Standard finite SDP Slater duality gives an attained dual for this pruned formulation.

The resulting dual identity is an identity of labelled local polynomials and labelled separator multipliers, evaluated on the permitted assignment space. It is not automatically an ordinary unlabelled polynomial identity. No unpruned dual-attainment claim or rational size theorem for this labelled cone is accepted without a separate argument.

## Accepted constrained exact-density contract

Section 4, lines 215–270, is accepted with the inherited conditions of Sections 1 and 3 made explicit in the manuscript:

- `K` is the nonempty global intersection of all polynomial inequalities inside the box.
- The global error bound is `dist_2(x,K)<=H V(x)^{alpha/2}` for every box point, with `V=sum(-g_{bj})_+^2`, `0<alpha<=1`, and fixed `H`. Separate local error bounds do not substitute for this assumption.
- `L_f` is a Lipschitz constant for the full objective on the entire box.
- The ordinary moment hierarchy has PSD squares, singleton box localizers, and each supplied `g_{bj}` times squares, through degree `2R`; it has normalized bags and exact separator moments.
- The parameters satisfy even `N>=2`, `s>=max(2,d_infty)`, and the conservative reserve `R>=wD+2d`, where `d>=1` bounds the total degrees of all objectives and constraints. For standalone use, define these two degree parameters explicitly rather than referring to a preceding theorem with possibly different objectives.

### Conditional positivity and displacement certificates

The SOS source kernel is `Q_b=sum q_l^2`, with `deg q_l<=vD/2`. Its conditional functional is positive on `(a+b g)^2`, since `deg(q_lg)<=vD/2+d<=R`. Its value at `g` is nonnegative by the additional localizer, because each product `g q_l^2` has degree at most `vD+d<=2R`. Thus the conditional Cauchy–Schwarz argument applies even if `L(Q_b)=0`; it does not require conditional division by that density.

I independently checked the transport certificate used to derive equation (5). For each tensor Chebyshev term, the normalized divided difference `D_k/k^2` has degree `k-1` and modulus at most one on the interval, because `|T'_k|<=k^2`. Multiplying by earlier source factors and constant later output factors gives `r_ell` of degree at most `|beta|-1`. The interval certificate for one minus each factor squared, telescoped with square multipliers, proves `1-r_ell^2` in the ordinary module through degree `2(|beta|-1)`.

The weighted-square identity displayed at lines 169–174 is exact. Multiplying the preceding certificates by `(x_i-y_i)^2` and adding the weighted squares gives

`A(g)sum_i A_i(g)(x_i-y_i)^2-(g(x)-g(y))^2`

in the ordinary module through degree `2deg(g)`. After multiplication by `Q_b`, every complete term has degree at most `vD+2d<=R<=2R`. This proves applicability under the truncated functional; pointwise Lipschitz continuity alone would not.

The squared displacement kernel `j_s=pJ_s` is globally SOS. The circle difference calculation gives `J_s<=2/s`, hence `j_s<=c_s=4/(s C_s)`. Its degree is at most `D+2`, so the interval certificate for `c_s-j_s` has that same cap. Combining it with SOS mass factors and the module certificate for `1-prod n_i` gives the bound for its integrated multivariate version at degree at most `vD+2<=R`. Consequently equation (5), `int(-g)_+^2 h_b<=c_s A(g)^2`, is justified. This is the necessary input to the new domination proof.

### Domination and the positive remainder

The exact signed-density expansion contains `h_b` as its zero-residual term. Singleton residual terms are ordinary-module nonnegative, and all higher residual terms together are at least `-Delta_w`. Therefore

`hbar_b>=h_b-Delta_w`, `h_b^+>=h_b/(1+Delta_w)`.

This is stronger than nonnegativity of `h_b^+`. Let `e_b=h_b^+-h_b/(1+Delta_w)`. It is nonnegative and has exact mass

`int e_b = (1+Delta_w-Z_b)/(1+Delta_w)`.

The original SOS bag density has mass `Z_b` with `a^v<=Z_b<=1`; no sign ambiguity occurs. For `v_g(y)=(-g(y))_+^2`, `0<=v_g<=C(g)^2`. Hence

`int v_g h_b^+ <= [c_s A(g)^2+C(g)^2(1+Delta_w-a^v)]/(1+Delta_w)`.

This recovers exactly Section 4's displayed bound. Summing over all constraints gives `U_exact`. Since exact gluing preserves each corrected bag marginal, the same global law has expected global violation at most `U_exact` and the stated corrected objective error `E_exact`. There is no coupling disagreement event or additional edge-count coefficient.

All terms in `U_exact` are fixed problem data and kernel parameters. Thus the law-to-feasible-point estimate can be taken uniformly over feasible moment collections before taking the hierarchy infimum. The global error bound and Jensen give

`f*-rho_R <= E_exact+L_f H U_exact^{alpha/2}`.

The global repair remains necessary: domination does not imply that a corrected bag law satisfies `g>=0` almost surely. Global geometric assumptions cannot be replaced by local bag repair constants; the author's `y-x^2>=0`, `-y>=0` counterexample is valid.

At fixed width, the selected even `N` gives `delta=O(s^-3)` and `Delta_w=O_w(log^{w-2}(s)/s^3)=o_w(s^-2)` for `w>=2`; width one has zero correction. Thus the positive remainder contribution is lower order than `s^-2`, `U_exact=O(s^-2)`, and `E_exact=O(log(s)/s^2)`. An additive degree reserve `2d` leaves `s=Theta_w(R/log R)` for every sufficiently large order. Raising the squared violation estimate to `alpha/2` gives the accepted rate `O((log R/R)^alpha)`.

No constrained dual-attainment conclusion follows from this primal error estimate alone. Empty interior and equality constraints can defeat the required Slater property. The report explicitly excludes that inference, and I accept the constrained development only as a primal gap and feasible-repair theorem unless further dual hypotheses are supplied.

## Accepted unified rational statement and its boundary

Section 7.6, lines 592–625, is accepted for rational, unlabelled, box-only polynomial data and the full monomial Gram bases of the chosen finite cone. Use the finite-order assumptions of the corresponding kernel theorem. Assume a rational gap upper bound `E_C` and rational positive slack `tau` with

`f*-gamma>=E_C+tau`.

Finite box SDP dual attainment and the gap bound imply

`rho_R>=f*-E_C>=gamma+tau`.

Thus `f-gamma-tau=(f-rho_R)+(rho_R-gamma-tau)` has real membership in the same cone, including at equality of the promise. This is the precise link needed by rational recovery; positive pointwise `f-gamma` at a fixed order alone does not suffice.

I checked that the ordinary restricted block family retains all ingredients of the existing rational theorem: the diagonal complement identities for the constant-one interior direction, positive definite rational product-uniform moment matrices, and the empty-generator monomial coefficient pivots. Restricting to empty and singleton generator sets does not require full-preordering membership and does not require `r>=w` for the rationalization step. This ordinary extension is already proved in the source note's Section 6.

The common constant-one direction supplies margin `tau/D_C`; exact rational rounding and global coefficient correction leave at least `tau/(2D_C)` in each block. The coefficient correction must collect shared monomials globally, and its denominator bound is twice the least common multiple of the rounding-grid denominator and input coefficient denominators. Full monomial bases and the extra factor of two must be retained.

For the ordinary rate, `eta_rat>=eta` follows because `sqrt(2(D+1))<=2(D+1)`. Every quantity in

`E_Q=C_f((1+eta_rat)^w-1+2Delta_w)`

is rational when input coefficients and integer parameters are rational or integral as appropriate. Monotonicity gives a valid upper bound. The replacement term is `O_w(s log(s)*s^-3)=O_w(log(s)/s^2)` under the selected `N`, so it retains the same normalized `log^3(R)/R^2` rate. No accidental square-root input or extra logarithmic rate loss is introduced.

Polynomial-bit witness existence follows independently from this explicit rounding argument and the rational outer bound. The deterministic construction reduction has a valid rational coefficient-space parametrization, a known enclosing ball, an unknown-center ball of known positive radius, and an exact rational PSD separation oracle. The unresolved literature obligation is the rounded rational strong-feasibility theorem that converts those inputs into polynomial-time feasibility. An exact-real volume bound, or a theorem assuming a supplied feasible start, is insufficient. This review accepts the construction claim conditional on that exact external theorem being supplied; if it cannot be supplied, retain the witness-size and checkability theorem and remove only the time claim.

The unified rational theorem does not cover the new labelled cone or constrained extra-generator cones. The manuscript should interpret its brief mention of all-discrete cases as a separate finite-state result, not as an extension of the rational Gram theorem. Constant unlabelled objectives can be handled directly. No new ordinary rational contribution is claimed.

## Verification record

This review used targeted `cat`, `nl -ba`, `sed`, `rg`, `stat`, and `sha256sum` reads. The first requested rational filename was absent; the relevant existing file was located as `rational-sparse-certificates.md` and then read. No experiment or checker was run. No literature research, project-wide verification, CI inspection, commits, source-note edits, or delegation occurred.

The universal claims were checked by the independent derivations above, including the explicit unequal-label-fiber boundary example, zero-mass functional proof, conditional density normalization, and positive-remainder mass calculation. Historical reviewer verdicts and numerical records were not used as mathematical premises. This output is the only file written for the new review task.
