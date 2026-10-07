# Independent manuscript review: regularity and the recourse appendix

Date: 2026-10-05. Reviewer: Sol. Reviewed the actual proofs in `sections/07-regularity.tex` and `appendices/B-recourse.tex`, including their interfaces with `sections/06-recourse.tex`, `sections/02-setting.tex`, and `sections/03-kernels.tex`. The source `active-region-rates.md` and `AUDIT-RECOURSE.md` were read as comparison materials after reconstructing the principal arguments.

**Verdict: ACCEPT.** No substantive mathematical defect was found. The half-degree certificate covers the commutator frequencies, the projected KKT correction has the correct sign, both regularity estimates are legal under the actual truncated cone, and the Motzkin construction proves all-order unboundedness without private quadratic bounds beginning at order three. The manuscript supplies its own degree and selection arguments rather than relying on the source audit. One optional definition clarification is recorded below; it does not affect either theorem under the stated regularity assumptions.

No authored TeX was edited. No literature research, experiment, numerical solve, historical checker rerun, project-wide verification, CI inspection, or commit was performed. Pending citation locators remain bibliographic dependencies, not mathematical defects in these self-contained arguments.

## Snapshot and scope

The initial review snapshots have the following SHA-256 hashes. Locators below refer to these snapshots.

| File | SHA-256 |
| --- | --- |
| `sections/07-regularity.tex` | `08d83d89615e418b5e547a6a33b75b33cb952d54d0a3815db43a33cd42eb2c93` |
| `appendices/B-recourse.tex` | `19c1deb69b1824bd1a7ed7794c2d8dafd52923e4477bb71d668735916f9c6c9d` |
| `sections/06-recourse.tex` | `9774b27eb05fd579892b2b96b699ba0ac9e65ea79b39c48249012148476ef738` |
| `sections/02-setting.tex` | `6db76f3db9195300a335e61feba66c387692e4e40dc59951fb2b50b020e8936b` |
| `sections/03-kernels.tex` | `aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a` |

The final hash comparison found Section 7, Section 2, and Section 3 unchanged. Appendix B and Section 6 had changed during the review. The entire revised appendix was reread; its only proof change was renaming the separating functional from `lambda` to `mathcal L`. The relevant revised Section 6 interfaces were reread, including its current order-unit certificate proof. That proof now separates a strict-level polynomial directly from the full-dimensional convex cone; weak separation is sufficient because the proposed level is strictly below the primal optimum. It remains valid without cone closedness. New grid comparison material near the end of Section 6 is outside this regularity review. Acceptance includes the reread interfaces and revised appendix at these final hashes:

| Updated file | Final reviewed SHA-256 |
| --- | --- |
| `appendices/B-recourse.tex` | `4c2250b5d513be3f2f0dc8f9019abc05dc1fa27c9cecf55d6586266c9625240f` |
| `sections/06-recourse.tex` | `b8b88edc1f966255db50470c754ff123b43dab7aeb7a54d1c62656a083c31ba6` |

The additional sharpness interface `sections/05-sharpness.tex`, lines 126–191, was inspected to verify that the transferred separator measures have the direction and constant used by the regular affine example. This was not a full review of that section.

## Findings and disposition

| Severity | Locator | Finding | Repair or disposition |
| --- | --- | --- | --- |
| None: correct essential step | Section 7, lines 100–143 and 162–173 | The usual degree-at-most-r Chebyshev moment bound would not cover the commutator; the manuscript proves and uses the stronger half-degree certificate. | Retain this lemma and its frequency ledger. |
| None: correct essential step | Section 7, lines 62–91 | The projected KKT term has sign plus times U-u h. | Identity and source-feasibility derivation are correct. |
| None: correct essential step | Section 7, lines 237–281 | Directional weighted absolute coefficients suffice, including frequencies just outside kernel support. | Termwise integration and the finite resulting source support are justified; no unaccounted tail remains. |
| None: correct essential step | Section 7, lines 284–316 | The Holder proof uses direct displacement and a univariate certificate rather than an approximation polynomial. | Degree 2m-1 for the commutator and degree at most 2m for its interval certificate are correct; no approximation-order or tail assumption is missing. |
| None: correct essential step | Section 7, lines 319–354 | A Borel optimal private policy is constructed independently of any full multiplier selection. | Regularization, minimum-norm convergence, and gluing are correct. |
| None: correct examples | Section 7, lines 367–429 | Sharp regular example and failure of automatic regularity under strict convexity. | Affine scaling, signs, constants, actual-measure transfers, and projected jump all check. |
| None: correct sufficient regime | Section 7, lines 441–483 | LICQ QPs have continuous piecewise-affine primal/full multiplier policies on the closed box. | Finite active-set argument is correct and supplies its own boundary justification. It does not assert general multivariate applicability of the two rate theorems. |
| None: correct essential counterexample | Appendix B, lines 19–89 | Motzkin nonmembership, fixed-order preordering closedness, normalized separation, and unbounded rectangular moments. | All arguments are valid for r at least three. The proof does not require q squared in the domain and does not claim the recourse cone is closed. |
| Minor, optional definition clarification | Section 7, lines 145–149 | The operator is introduced for a “bounded function,” although a completely arbitrary bounded function need not be measurable. | Say “bounded Borel function” or “bounded measurable function.” Both actual theorem hypotheses give a continuous projection, so there is no theorem gap. |

## 1. Rectangular degree interface

The setting, Section 2 lines 441–468 in the reviewed snapshot, defines shared total degree at most `2r` independently of private total degree at most two. Matrix squares have affine private forms whose shared coefficient degrees are at most `r-|I|`. Private quadratic localizers use the same scalar allowance. A fiber row with nonzero shared right-hand-side coefficient reserves one shared degree; fixed rows have the larger allowance.

Section 7's parameters, lines 17–25, give

\[
 m=\lfloor(r-1)/w\rfloor+1=\lceil r/w\rceil,\quad
 r\ge\max(w+1,d),\quad v_b(m-1)\le r-1.
\]

This is exactly the reserve needed by the conditional matrices in Section 6. The kernel certificate has squares of shared degree at most `v_b(m-1)-|I|`. Multiplication by an affine shared form raises that degree by one, staying within the matrix-square allowance. Multiplication by each affine fiber row stays within its scalar localizer allowance. The private degree remains at most two throughout.

The proof of the shared diagonal bounds in Section 6 lines 246–256 handles repeated box generators correctly: an absent coordinate adds a generator; an already-present coordinate is removed from the weight and its generator is absorbed into the square polynomial. This second case costs two square degrees while removal frees one allowance, and the single reserve provides the other. These calculations validate source mean feasibility and the vanishing augmented conditional matrix at zero density, which Section 7 uses.

The ordinary box module is not enough for the tensor half-degree certificate below. The regularity theorems remain restricted to the shared full preordering; the setting does not silently replace it by singleton positivity.

## 2. Projected KKT signs and existence

At each output `u`, private compactness supplies an optimal point. Section 7 lines 42–52 gives a correct direct multiplier argument: the active row cone is finitely generated and closed; separating minus the gradient from it gives a direction with nonpositive active-row derivatives and strictly negative objective derivative. Inactive rows retain their positive slack for sufficiently small steps. This contradicts optimality. Thus minus the gradient is a nonnegative combination of active row normals, including private box rows. No Slater or LICQ assumption is needed for this pointwise existence conclusion.

For the convention `Ahat y <= ahat+D u`, stationarity is `gradient f + Ahat^T pi=0` and complementarity is `pi^T(ahat+D u-Ahat y*)=0`. Expanding the convex quadratic around the optimizer gives exactly

\[
 f(u,y)-F(u)-\pi(u)^T(\widehat a+D u-\widehat A y)
 =(y-y^*)^TQ(u)(y-y^*)\ge0.
\]

This identity holds even for `y` infeasible at output `u`. If `ybar` is feasible at the source mean `xbar`, its output slack is its nonnegative source slack plus `D(u-xbar)`. Dropping the nonnegative multiplier/source-slack product yields

\[
 F(u)\le f(u,ybar)+a^{\rm dual}(u)^T(xbar-u),
 \qquad a^{\rm dual}=D^T\pi.
\]

Multiplying by `h` and using matrix Jensen gives the manuscript's plus correction `a^{dual}(u)^T(U-u h)`. At `h=0`, both conditional matrices and `U` vanish, so no problematic division or hidden multiplier-times-zero convention is needed. The regular projection is finite and bounded under both theorem hypotheses.

The integrated expression contains only the projection. Even if the full multiplier choices are unbounded or nonmeasurable, the assumed projection is continuous under either its absolutely uniform coefficient expansion or its coordinatewise Holder hypothesis. The proof does not integrate the full vector. Optimal private policies are selected by an independent argument; they need not be the same choices used to witness the pointwise KKT assumption.

## 3. Half-degree certificate and commutator legality

For each univariate index `k`, the manuscript produces a certificate for `1 plus/minus T_k` at degree at most `2 ceil(k/2)`. The explicit even identities are immediate from `T_{2j}=2T_j^2-1`. The odd identities

\[
 1+T_{2j+1}=(1+x)(U_j-U_{j-1})^2,\qquad
 1-T_{2j+1}=(1-x)(U_j+U_{j-1})^2
\]

are valid, with `U_{-1}=0`. Replacing `1 plus/minus x` by `((1 plus/minus x)^2+1-x^2)/2` raises the odd degree `2j+1` to at most `2j+2`, as required. The setting's interval theorem also supplies that same padded degree bound. The constant index gives two constant certificates, including zero for the minus sign.

The parity identity at Section 7 lines 126–140 has the correct normalization `2^{1-k}`. Averaging over sign vectors of prescribed product retains only the empty tensor monomial and the full product. Multiplying the univariate certificates concerns distinct coordinates, so its generator products are squarefree and the square multipliers remain sums of squares. The total degree is at most `2 sum_i ceil(alpha_i/2)`, giving membership in the full preordering, not merely pointwise nonnegativity. Both signs then yield `|L(T_alpha)|<=L(1)`. Empty bags give the constant case directly.

The commutator is obtained by applying the finite-dimensional functional to

\[
 R_b(x)=\sum_i\left[x_i\mathcal K_ba_i(x)-\mathcal K_b(u_i a_i)(x)\right].
\]

For a bounded measurable projection the kernel's finite polynomial expansion makes this an ordinary polynomial. Its frequencies have degree at most `2m-2` in every coordinate, except possibly degree `2m-1` in one coordinate. Therefore

\[
 |\alpha|\le2v_b(m-1)+1\le2r-1,\quad
 \sum_i\lceil\alpha_i/2\rceil\le v_b(m-1)+1\le r.
\]

The first inequality validates the functional domain; the second supplies the positivity certificate needed for every coefficient evaluation. The two conditions are distinct. Interchanging integration with `L_b` is a finite coefficient operation with bounded integrands, so neither a representing measure for `L_b` nor an infinite-dimensional continuity estimate is assumed.

## 4. Weighted series, support boundaries, and tails

Section 7 lines 179–203 assumes

\[
 \sum_{b,i,\alpha}|a_{bi\alpha}|\max(1,2\alpha_i)<\infty.
\]

The weight is at least one, so the full tensor series is absolutely and uniformly convergent on the box. Bounded continuous projection functions follow without regularity of the full multiplier vector. It is legitimate to integrate the series against the fixed finite-degree kernel and against `u_i` times that kernel.

The adjacent multiplier bound holds for all indices including indices beyond the kernel support. The cosine difference identity and `|sin(n t)|<=n|sin t|` give

\[
 |g_{j+1}-g_j|\le(2j+1)(1-g_1),\qquad1-g_1=3/D_m.
\]

For an input mode with directional index `k>=1`, the one-coordinate commutator has coefficients `(g_k-g_{k+1})/2` and `(g_k-g_{k-1})/2`; their absolute sum is at most `2k(1-g_1)`. For `k=0`, the coefficient is `1-g_1`. Every other coordinate contributes its multiplier, of magnitude at most one. This explains why directional weights suffice: no frequency weight in unrelated coordinates is needed.

The manuscript explicitly includes input directional index `k=2m-1`, which survives through its `k-1` mode even though `g_k=0`. It must not be discarded with the modes strictly above kernel degree. Modes with `k>2m-1`, or with another coordinate above `2m-2`, vanish. Thus only finitely many input modes can contribute to the source polynomial at each fixed order. One may first integrate rectangular partial sums; their tails vanish uniformly. The coefficient estimate is bounded by the stated summable weighted budget, so the absolute contribution of omitted modes also tends to zero. In fact sufficiently large partial sums contain every surviving mode. There is no hidden polynomial approximation tail or additional order factor.

Applying the half-degree bound coefficientwise gives

\[
 |L_b(R_b)|\le{3\over D_m}
   \sum_{i,\alpha}|a_{bi\alpha}|\max(1,2\alpha_i).
\]

This is the correct finite-order estimate, including zero indices, support edges, and all tensor directions. It does not infer weighted summability from arbitrary multivariate Lipschitz continuity.

## 5. Holder proof and constants

The saved manuscript uses a direct argument instead of a polynomial approximation to the Holder function. No approximation degree choice is missing.

When `a_i(u)=phi_i(u_i)`, normalization of the other kernel coordinates reduces the commutator to a univariate polynomial

\[
 R_i(x)=\int K_m(x,u)\phi_i(u)(x-u)d\mu(u)
\]

of degree at most `2m-1`. Adding and subtracting `phi_i(x)` produces a first term `(1-g_1)x phi_i(x)` and a remainder bounded by `H_i int K_m |x-u|^{1+beta}`. The pointwise source/output second-moment identity from Section 6 gives

\[
 \int K_m(x,u)(x-u)^2d\mu(u)
 =V_m+{3-2m\over a_0}x^2\le V_m,
 \quad V_m={3(4m-3)\over2mD_m}.
\]

Its coefficient is nonpositive for `m>=2`. Kernel mass one and Jensen for the exponent `(1+beta)/2` yield the claimed bound for `0<beta<=1`, including equality in Jensen at `beta=1`. Hence

\[
 |R_i(x)|\le\varepsilon_i:={3M_i\over D_m}
                  +H_iV_m^{(1+\beta)/2}.
\]

Although the displayed decomposition contains the nonpolynomial function `phi_i(x)`, the original integrated `R_i` is a polynomial. Only `epsilon_i-R_i` is passed to the interval SOS theorem, so no nonpolynomial certificate is being asserted. The polynomial has degree at most `2m-1`, padded by that theorem to a representation degree at most `2m`. Since `m=ceil(r/w)<=r` for the stated orders and positive width, this univariate certificate embeds in the scalar shared part of (R1). Therefore `L_b(R_i)<=epsilon_i`, without a representing measure or a multivariate sup-norm inference.

This gives the saved Holder theorem exactly. Its parameters obey

\[
 D_m>2r^2/w^2,\qquad V_m<6/D_m<3w^2/r^2.
\]

The matrix-cost term is `3 A/D_m`; the regularity contributions are `3 sum M_i/D_m` and `sum H_i V_m^{(1+beta)/2}`. Thus the displayed `3w^2/(2r^2)` coefficient and `(sqrt(3) w/r)^{1+beta}` coefficient are correct. For fixed data the rate is `r^{-(1+beta)}` because the `r^-2` terms are smaller or equal. Only beta one is asserted sharp. Width, private dimension, and multiplier conditioning enter the fixed-data constants as stated.

## 6. Optimal policies, sharpness, and the scalar QP regime

The Borel-policy completion at Section 7 lines 319–354 is valid. For each positive epsilon, private convexity plus `epsilon ||y||^2` makes the optimizer unique. Fiber Hausdorff continuity and private compactness show that these policies are continuous. Comparison with any unregularized minimizer bounds both their objective error by `epsilon ||z||^2` and their norm by `||z||`. At a fixed parameter their cluster points are optimal minimum-norm points. The optimizer set is compact and convex, so its minimum-norm point is unique and the regularized policies converge pointwise. A sequence epsilon equal to `1/k` gives a Borel policy. Gluing the scalar shared laws and assigning these private policies realizes `sum int h_b F_b` exactly. The full KKT selection need not be the selected Borel policy.

The regular sharp example checks independently. The two local minima are `-x_+^2` and `x_+^2`; both private domains are nonempty for every shared point. Before private affine scaling, multiplier `2x_+` on `-z<=-x` and zero box multipliers satisfy stationarity and complementarity at every point including endpoints. Its projection is `-2x_+`. After scaling `z=(1+zeta)/2`, the row is `-zeta<=1-2x`; dividing the original multiplier by two preserves the projection. The first bag's shared matrix coefficient has entrywise norm two, the second has no shared objective coefficient, so `A=2`. The only nonzero projection has `M=H=2`. The upper error is therefore `12/D_r+2V_r<24/D_r<12/r^2`, as stated.

The lower bound uses the separator measures for `phi=x_+^2` with the larger expectation in the first bag. Both private lifts for this regular example are `x_+`, producing negative expectation difference and the correct constant `2/(27 pi (2r+2)^2)`. The manuscript correctly distinguishes this second lift from the `(-x)_+` lift in the separate quadratic sharpness problem. Actual measures remain feasible for the rectangular localizers after affine scaling; no cone inclusion is used.

The strictly convex example has derivative `2z+1`, optimum `z=|x|`, and a positive definite Hessian. For positive x the active row projection is `-(2x+1)`; for negative x it is `1-2x`. Box rows are inactive in the punctured neighborhood, so no alternative multiplier choices can remove the opposite one-sided limits. A chosen value at zero cannot make the projection continuous. This correctly disproves inference of the stated regularity from strict convexity, complete recourse, or a Lipschitz primal optimizer. It does not claim that this one-bag illustration itself proves the two-bag inverse-order gap.

The sufficient scalar QP proposition also has a complete proof. Positive definite Q and independent active rows make the KKT matrix nonsingular. Every candidate active-set solution is affine, and feasibility and multiplier nonnegativity define a closed polyhedral region. Finitely many row sets cover the parameter box. LICQ makes the full multiplier unique, including any zero multipliers on active rows; valid affine policies agree on overlaps. A subsequence argument gives continuity at region and box boundaries. Finitely many affine pieces along a line segment give a Lipschitz constant bounded by the largest affine slope. The open-neighborhood assumption is stronger than needed by this algebraic proof on the box but is a valid sufficient assumption and avoids an unqualified boundary sensitivity claim. No strict complementarity is silently assumed. In multivariate bags Lipschitz continuity alone is not promoted to either weighted summability or coordinatewise dependence.

## 7. Appendix: Motzkin nonmembership and unbounded moments

The AM--GM bound proves nonnegativity of the Motzkin form, so `q(x)y^2` has private convexity and true optimum zero. It is in the rectangular objective space for every `r>=3`.

Suppose `q=sum w_I a_{I,l}^2`. At the origin every weight is one and q vanishes, forcing each square polynomial to vanish. Let k be the smallest nonzero homogeneous degree among these polynomials. The degree-2k leading part is the sum of squares of their degree-k parts and cannot cancel. Since q is homogeneous of degree six, k must equal three. Comparing degree-six parts expresses q as a sum of homogeneous cubic squares.

The manuscript's coefficient contradiction is valid in the stated order. Zero x1-sixth and x2-sixth coefficients first remove pure x1-cubed and x2-cubed terms. The x1-fourth x3-squared and x2-fourth x3-squared coefficients then contain only the squares of the x1-squared x3 and x2-squared x3 coefficients, so those vanish. With them removed, x1-squared x3-fourth and x2-squared x3-fourth similarly remove x1 x3-squared and x2 x3-squared. The remaining coefficient of x1-squared x2-squared x3-squared is a sum of squares, contradicting minus three. Cross terms that could contribute to this last monomial involve coefficients already removed. This proves nonmembership at every finite order, not merely at order three.

The fixed-order scalar preordering is closed for the reason given. Uniform cube expectation yields a positive definite matrix for every monomial Gram block, since its weight is positive throughout the open cube. Coefficient convergence bounds integrals, and the positive minimum eigenvalues bound every PSD Gram trace in any representation. Finitely many bounded PSD blocks have a convergent subsequence realizing the limit polynomial. Thus separation is applicable to the actual finite-degree cone. The proof does not assume that every linear image of a closed PSD cone is closed and does not extend this conclusion to the recourse cone with additional signed affine generators.

A separating functional lambda is nonnegative on the preordering and negative on q. Singleton box localizers and moment Cauchy--Schwarz give `|lambda(x^alpha)|<=lambda(1)` for all monomials through degree 2r, so zero mass would force lambda identically zero. It can therefore be normalized to mass one. This does not test q squared and is valid when q squared lies outside the degree-2r domain at r three, four, or five.

Finally,

\[
 L_R(a(x)+b(x)y+c(x)y^2)=a(0)+R\lambda(c),\quad R\ge0,
\]

is normalized and satisfies every matrix-square localizer because its value is the sum of `w_I(0) s_0(0)^2` and `R lambda(w_I s_1^2)`. Mixed private linear terms have value zero. Every scalar affine private localizer for `1 plus/minus y` has value `w_I(0)s(0)^2`. There are no separators in the single-bag construction. Removing private quadratic bounds thus leaves a feasible ray with objective `R lambda(q)` tending to minus infinity. The private second moment is R, precisely the quantity the omitted bounds would control. This proves the manuscript proposition at all its stated orders r at least three.

## 8. Verification and publication dependencies

Actual tool commands were targeted `nl -ba`, `sed`, `rg`, and `cat` reads of the reviewed manuscript files and comparison sources, plus `sha256sum` for the five snapshot files and `wc -l -w` for this review artifact. The conclusions rest on the analytic reconstructions above. No checker or experiment was run. A final hash comparison is recorded in the parent handoff; any changed-file review scope must be identified there.

The arguments needing external source attribution are already presented with their relevant assumptions: even/odd interval SOS, finite-dimensional separation, fixed-matrix Hoffman bounds, and prior multiparametric QP and moment-matching methods. Source locators and pending bibliography keys should be finalized by Luna. The regularity proof, QP sufficient-regime proof, and Motzkin appendix do not need stronger unpublished results to close their mathematical arguments.
