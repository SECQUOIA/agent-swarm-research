# Independent review of rectangular recourse duality and the order unit

Date: 2026-10-05. Reviewed Section 7 and the hierarchy definitions in `paper-sparse-sos/evidence/AUDIT-RECOURSE.md` against `research-20260928/solver/partial-kernel-rounding.md` and `research-20260928/solver/affine-recourse-kernel-upper.md`.

**Verdict: ACCEPT.** The order-unit completion is correct. It proves compactness and attainment of the normalized primal moment optimum, equality of the primal value and certificate supremum, and a finite certificate at every strictly smaller level. It does not prove certificate attainment at the optimal level. No mathematical repair is needed. The theorem must retain its rectangular polynomial space, private quadratic bounds, exact separator equations, running intersection, and disjoint private variables. A short self-contained theorem and degree ledger below make these boundaries explicit.

No literature search, experiment rerun, source-note edit, manuscript edit, project-wide verification, CI inspection, or commit was performed. This reviewer independently reconstructed the proof before accepting its conclusions. This is an analytic review, not a formal proof assistant verification.

## 1. Precise cone and theorem

Take a finite nonempty tree of bags. Bag `b` has shared coordinate set `S_b`, of size `k_b`, and its own disjoint private coordinates `y_b=(y_{b1},...,y_{bp_b})`. Shared sets satisfy running intersection. Put

\[
 V_{b,r}=\mathbb R[u_{S_b}]_{\le2r}\otimes
          \mathbb R[y_b]_{\le2},\qquad r\in\mathbb Z_{\ge0}.
\]

Both bounds are total degrees in their respective groups. They are independent bounds: a polynomial of shared degree `2r` and private degree two has joint total degree `2r+2` and remains in this space. The argument below is not a proof for a joint total-degree-`2r` hierarchy.

For `w_I=prod_{i in I}(1-u_i^2)`, the local cone `C_{b,r}` contains finite sums of

\[
 w_I\left[q_0(u)+\sum_iq_i(u)y_i\right]^2,
       \qquad\deg q_i\le r-|I|,
 \tag{1}
\]

and

\[
 w_Iq(u)^2(1-y_i^2),\qquad\deg q\le r-|I|.
 \tag{2}
\]

All coefficient choices are real. Negative allowances mean absent generators. Additional valid localizers may be included; the audit includes fixed-private affine generators with allowance `r-|I|`, or affine-recourse generators with allowance `r-|I|-1`. Sums of (1), (2), and those additional generators form a convex cone. It is a finite-dimensional Gram image of a product of PSD cones, but its image need not be closed.

Identify the local spaces by addition inside the global polynomial ring:

\[
 W_r=\sum_bV_{b,r},\qquad C_r=\sum_bC_{b,r}\subset W_r.
\]

Assume the cone's additional constraints admit at least one feasible global point, so its evaluation is a positive normalized functional. In the source applications this follows from nonempty independent fixed polytopes, or complete affine recourse. Convexity of the objective, kernel smoothing, and Hoffman repair are not assumptions of this algebraic duality theorem; they are needed separately for the quantitative primal gap bounds.

For any `f in W_r`, define

\[
 \rho_r=\min\{F(f):F\in C_r^*,\ F(1)=1\},\quad
 \lambda_r=\sup\{\lambda:f-\lambda1\in C_r\}.
\]

Then the minimum exists, the values are finite, and

\[
 \lambda_r=\rho_r,\qquad
 f-\lambda1\in C_r\quad\forall\lambda<\rho_r.
 \tag{3}
\]

Section 3 below proves that the normalized global functional formulation is exactly the source's local moment formulation. The theorem remains true at `r=0`; source kernel rate theorems use larger orders for unrelated reasons.

## 2. Independent monomial certificate reconstruction

Every basis monomial of `V_{b,r}` can be written

\[
 e=u^\alpha z_i z_j,\qquad z_0=1,\quad z_i=y_i\ (i>0),
 \quad |\alpha|\le2r.
\]

This notation covers private degrees zero, one, and two. Split the shared exponent into nonnegative integer exponents `alpha=beta+gamma` with `|beta|,|gamma|<=r`. Such a split exists by assigning at most `r` units of the exponent to `beta` and placing the rest in `gamma`; for `|alpha|<=r`, one may take `beta=alpha`, `gamma=0`.

For any `beta` with `|beta|<=r`, direct telescoping gives

\[
 1-u^{2\beta}
 =\sum_{h=1}^{k_b}\sum_{\ell=0}^{\beta_h-1}
 \left(\prod_{j<h}u_j^{\beta_j}u_h^\ell\right)^2(1-u_h^2).
 \tag{4}
\]

Every square polynomial in (4) has shared degree at most `|beta|-1<=r-1`, and the weight is a singleton box generator. Thus (4) belongs to (1)'s scalar subcone with `I={h}` and zero private coefficients. If `beta=0`, both sides are zero and no singleton allowance is used.

Put `a=u^beta z_i`. If `i=0`, (4) is already a certificate for `1-a^2`. If `i>0`, use

\[
 1-a^2=(1-u^{2\beta})+u^{2\beta}(1-y_i^2).
 \tag{5}
\]

The second term is (2) with empty `I` and `q=u^beta`, whose degree is at most `r`. Thus `1-a^2 in C_{b,r}`. Repeating the construction for `b=u^gamma z_j` gives `1-b^2 in C_{b,r}`. Finally,

\[
 1\pm e=\frac12\left[(1-a^2)+(1-b^2)+(a\pm b)^2\right]
 \in C_{b,r}.
 \tag{6}
\]

The square `(a plus/minus b)^2` is valid under (1) with empty `I`: it is the square of an affine private form, all of whose shared coefficient polynomials have degree at most `r`. If `i=j`, the two coefficients simply combine; if either index is zero, its term belongs to `q_0`. Nothing requires `a` and `b` to have degree at most `r` in the joint variables. Their shared degrees are at most `r`, their private degrees at most one, and their squared product terms have shared degree at most `2r` and private degree at most two.

This proves the audit's order-unit identity at the most demanding boundary `|alpha|=2r`, including private quadratic cross terms. The identity uses only singleton shared bounds, empty-weight matrix squares, and empty-weight private quadratic bounds. The full shared preordering may remain essential for the kernel rate proof, but the order-unit argument itself does not require products of multiple shared generators. Private affine feasibility inequalities are not used here. Their degree allowance cannot repair omission of (2), because affine localizers do not bound private second moments.

## 3. Exact sparse coefficient quotient

Let `Sigma: direct_sum_b V_{b,r} -> W_r` be coefficient summation in the global polynomial ring. A local functional tuple descends to one global functional precisely if it annihilates `ker Sigma`. The audit correctly identifies this kernel with separator difference relations.

To reconstruct the identification, treat each global monomial separately. A monomial containing any private coordinate can occur only in that coordinate's owning bag, because private coordinate sets are disjoint. Its coefficient therefore contributes no relation between distinct bags. A pure shared monomial of support `J` occurs exactly in the bags containing `J`. Every coordinate's occurrence bags form a connected subtree by running intersection. The intersection of these subtrees is connected whenever nonempty: the unique path between any two common nodes lies in every subtree. Thus the occurrence bags of the monomial form a connected subtree.

A vector of its local coefficients summing to zero can be decomposed into signed edge transfers on that subtree, by peeling off leaves. Each transfer places the monomial at one endpoint and its negative at the other. The monomial is supported in the edge separator and has total shared degree at most `2r`, so the imposed separator equations annihilate every transfer. Conversely an edge transfer is plainly in `ker Sigma`. Summing this argument over finitely many monomials proves the claimed kernel characterization. The constant monomial occurs in every bag and obeys the same proof on the entire tree.

Therefore exact separator equality through degree `2r` makes

\[
 F\left(\sum_bp_b\right)=\sum_bL_b(p_b)
\]

well defined. Conversely, restrictions of a global `F` automatically agree on every separator. The identities `L_b(1)=1` correspond to `F(1)=1`, and positivity on every local cone corresponds to `F in C_r^*`.

There is no quotient by feasibility equalities or by pointwise vanishing on the feasible set in this argument. The quotient is only the kernel of global polynomial summation. Paired private equality localizers remain elements of the cone; no hidden facial reduction is used. No mixed private separator moments are required. With overlapping private variables or without running intersection, the stated kernel proof would need replacement.

## 4. Interior, compactness, and dual value

Choose one occurrence of every distinct global monomial to obtain a basis `{e_l}` of `W_r`. Equation (6) gives `1 plus/minus e_l in C_r` for each basis element. Also `1 in C_r`, by the square of one in any bag. If `g=sum c_l e_l` with `sum |c_l|<=1`, then

\[
 1+g=(1-\sum_l|c_l|)1
        +\sum_l|c_l|(1+\operatorname{sign}(c_l)e_l)\in C_r.
 \tag{7}
\]

Hence a full-dimensional coefficient `ell_1` ball around one lies in `C_r`; one is an interior point relative to `W_r`. The constant basis element itself causes no problem: `1-1=0` and `1+1=2` are in the cone. Positive scalar multiples of the coefficient ball give an interior ball around every `epsilon1` for `epsilon>0`.

For any `F in C_r^*`, (6) yields `|F(e_l)|<=F(1)`. In particular, nonzero positive functionals satisfy `F(1)>0`; if `F(1)=0`, every basis coordinate is zero. The normalized positive functionals thus have all coordinates in `[-1,1]`. Their set is closed because it is an intersection of closed positivity halfspaces and the normalization hyperplane. It is nonempty by feasible evaluation, hence compact. Its objective minimum `rho_r` is finite and attained. This proves compactness for all rectangular moments, including shared degree `2r` times private degree two, rather than only the lower-degree moments used by the rate proofs.

Put `p=f-rho_r1`. A nonzero `F in C_r^*` can be normalized by `F(1)>0`, so

\[
 F(p)=F(1)\left[F(f)/F(1)-\rho_r\right]\ge0.
\]

The zero functional also gives a nonnegative value. Finite-dimensional bipolar separation therefore gives `p in closure(C_r)`. It gives membership in the closure, not in the original cone.

Fix `epsilon>0`. Select `p_n in C_r` converging to `p`; choose one with coefficient norm `||p-p_n||_1<epsilon`. By the scaled version of (7), `epsilon1+(p-p_n) in C_r`. Adding `p_n` gives

\[
 f-(\rho_r-\epsilon)1=p+\epsilon1\in C_r.
\]

Weak duality gives `lambda_r<=rho_r`; the preceding membership for every positive epsilon gives equality of the supremum and minimum. Each element of `C_r` is by definition a finite sum of permitted square forms and localizers, hence a finite real Gram certificate. This completes (3), without assuming closure of a PSD image or primal Slater.

If a quantitative rate proves `f*-rho_r<=E_r`, then

\[
 f^*-E_r-\epsilon\le\rho_r-\epsilon<\rho_r,
\]

so a certificate exists at that level for every `epsilon>0`. Equality of supremal values also transfers the same gap bound to the certificate supremum. The argument does not imply that `f-f*+E_r` itself has a certificate at exactly the error threshold. It does not imply rational Grams, a bound on their norms or bit lengths, or an algorithm for locating them.

## 5. Affine localizer degrees and edge cases

The affine-recourse row has shared degree at most one and private degree at most one. With `deg q<=r-|I|-1`, its displayed localizer has shared degree at most

\[
 2|I|+2(r-|I|-1)+1=2r-1,
\]

and private degree at most one. It therefore belongs to the rectangular domain, with conservative spare shared degree. A row independent of shared variables can use `deg q<=r-|I|`, giving shared degree at most `2r` and private degree at most one. Neither choice changes the order-unit proof. Enlarging a correctly defined cone by these rows preserves (6) and (7); global feasibility preserves a normalized evaluation in its dual.

All small-dimensional cases survive:

- With no private variables, `z=(1)` and (4), (6) reduce to scalar shared certificates; (2) is absent.
- With no shared variables in one bag, the only shared exponent is zero, the rectangle is the private quadratic space, and (5), (6) use constant scalar coefficients. That bag meets neighboring bags only on constant polynomials.
- With no shared variables globally, the tree quotient identifies only constants between otherwise independent private blocks. The proof still applies.
- With `r=0`, all shared exponents are zero and no singleton shared terms are needed. Private quadratic bounds and matrix squares suffice. Affine-recourse rows with allowance minus one are absent, so the hierarchy at this order may ignore those rows, but the duality theorem for the resulting cone remains valid. The source quantitative recourse theorem separately requires `r>=s+1`, so it never uses this weak order.
- For `r=1` or `|alpha|=2r`, the exponent split and certificate degrees above are exact; no extra kernel reserve is required for duality.
- Empty separators carry only constant normalization equations. Lower-dimensional private polytopes, paired equality rows, singular private quadratic Hessians, and zero objectives do not obstruct the cone proof.
- A nonempty bag tree is required to have a constant square and normalize one. The source's finite-tree model convention supplies this; a theorem statement can say it explicitly.

If global feasibility is dropped, interiority of one may still hold but the normalized dual set may be empty; the asserted finite primal optimum then does not follow. Nonempty fixed polytopes or complete recourse are the source conditions discharging this requirement.

## 6. Editorial recommendations and verification record

The audit is ready to use. Retain its statement that no boundary attainment is established. Prefer the phrase “certificates exist at every strict level” to “strict suboptimal levels are attained,” which can be mistaken for an attained dual optimum. The proof needs only objective membership in `W_r`; the stronger `d<=r` and kernel reserve are rate-theorem assumptions and should be stated separately.

For a self-contained manuscript, show the monomial identity (6), give the monomialwise separator-kernel argument, and include the short closure-plus-interior proof in Section 4. These resolve the delicate points without a stronger SDP theorem or an unproved claim that the sparse Gram image is closed. The only external convex-analysis fact used is finite-dimensional separation/bipolarity for a convex cone.

Targeted commands actually used for this review were `cat` and `sed` reads of the two source notes and the current recourse audit, plus a file-presence listing. Document checks `wc -l -w paper-sparse-sos/evidence/reviews/recourse-duality-sol-r1.md` and `rg -n 'Verdict|2r-1|closure|r=0|not imply' paper-sparse-sos/evidence/reviews/recourse-duality-sol-r1.md` both passed: the report was present and all requested proof markers were found. No checker or experiment was run. The relevant verification is the independently reconstructed symbolic identities, total-degree allowances within each tensor factor, the separator relation argument, and the nonclosed-cone proof above. These are distinct from the source notes' historical computational checks and from CI.
