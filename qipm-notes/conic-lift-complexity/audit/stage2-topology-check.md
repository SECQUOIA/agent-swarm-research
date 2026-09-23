# Stage 2 independent support-orbit and real order-three audit

Audited sources: `2026-09-04-symmetric-cone-support-orbit-rigidity.md`, `2026-09-04-psd3-saturation-exclusion.md`, and `2026-09-04-global-smooth-saturation-topology.md`, against the current foundations. No result-invalidating mathematical error found in the support-orbit theorem or the ball-specific order-three exclusion. The full strength below is defensible. The separate arbitrary-cone tangent-bundle theorem needs C2 sheets as stated; it should not be silently conflated with the bi-C1 support-orbit theorem.

## Recommended strongest clean statements

Let C be a compact convex body in R^(n+1), n >= 1, with 0 interior. Suppose both P=boundary C and D=boundary C-polar are strictly convex C1 hypersurfaces. Suppose full slack has globally labelled C1 maps X_i:P -> K_i and Y_i:D -> K_i into finitely many simple symmetric cones, with

    1 - <x,z> = sum_i <X_i(x),Y_i(z)>.

Write c_i=a_i floor(r_i^2/4), with zero for rays. If sum_i c_i=n, then the joint support-idempotent map is a finite covering of the product of balanced support orbits. There is exactly one positive-capacity factor. It is Q_(n+2), except that n=2 allows H_3(R)_+ on purely topological grounds. The H_3(R) possibility is impossible for the round three-ball even in the presence of arbitrarily many finite continuous nonnegative ray factors. Thus for every round ball B_2^s, s>=2, saturation implies the unique positive-capacity factor is Q_(s+1).

No differentiability of the contact correspondence is required in the first statement. At the round-ball specialization the same sphere is used in both arguments, so the local Peirce lemma in the foundations applies directly. For a general body, explicitly use independent local charts and only its rank conclusion; the positivity/symmetry formula from the foundations is not literally a bilinear form on a single tangent space until the contact map is differentiable.

The resulting all-cap frontier for globally bi-C1 symmetric-cone factorizations is valid: if 3 <= d < s+1, then k_+ >= ceil(s/(d-2)), M >= s + 2 ceil(s/(d-2)), and total ambient rank >= 2 ceil(s/(d-2)). Grouped quadratic epigraph lifts attain all three. If d>=s+1, the direct Lorentz cone gives (1,s+1,2). This frontier is for the global selection class, not every exact lift; unrestricted norm trees have the smaller s-1 numerator.

## Proof audit: differential argument

At a contact (x,z), T_x P=z-perp and T_z D=x-perp. The pairing (u,v)-><u,v> between these tangent spaces is nonsingular: u in the first space orthogonal to the second is a multiple of x, and <x,z>=1 kills that multiple. Mixed differentiation yields this full-rank pairing as a sum of negative derivative pairings.

Complementarity and the two-sided cone derivative argument constrain the two derivative images to overlap only in the cross Peirce channels between primal and dual positive supports. Thus rank H_i <= a_i p_i q_i <= c_i even in independent charts. Sum-rank equality forces balanced complementary ranks and rank H_i=c_i for every positive block. Along the contact graph, each rank is lower semicontinuous and their sum is fixed r_i; hence both are locally constant, and then globally constant by connectedness. There is no hidden rank-constancy hypothesis.

The support idempotent e_i of constant-rank X_i is C1 by local spectral functional calculus with the zero cluster separated from the positive spectrum. Differentiate e_i squared=e_i and X_i circle e_i=X_i. The support differential lies in V(e_i,1/2), and if B is the half-Peirce component of dX_i, then L_(X_i) de_i=B/2. On each cross channel L_(X_i) has eigenvalue lambda_j/2>0. Therefore de_i=0 iff B=0. This gives rank H_i <= rank d sigma_i <= c_i and proves submersion.

If every support differential kills u, every H_i(u,v) vanishes, so u=0 by the full mixed pairing. The joint support map therefore has invertible differential because source and target have the same dimension. Compactness gives properness, the image is open and closed, and connectedness of the target gives a finite covering. This is stronger and cleaner than invoking each separate submersion and then a sphere-fibration theorem.

## Proof audit: classification

For n>=2 the source sphere is simply connected, so it is the target's universal cover. A circle factor is impossible because a finite covering by a simply connected compact space would force finite fundamental group, whereas the target product would contain Z. All other factors have compact simply connected covers. The universal cover of the product is the product of these covers. Two positive-dimensional closed-manifold factors give a nonzero intermediate-degree mod-two cohomology class, using one factor's top class and degree zero in the others; hence there is only one. For n=1 the dimension sum already gives a single positive factor.

The remaining table can be proved with little imported topology:

* Spin factor Q_m: primitive orbit S^(m-2), as directly seen from the Jordan product.
* H_r(R), r>=3: balanced orbit Gr_p(R^(p+q)). For r=3 the universal cover is S2 -> RP2. For r>=4, p,q>=2. The oriented Grassmannian SO(p+q)/(SO(p) x SO(q)) is simply connected: the map on pi1 from the isotropy onto SO(p+q) is surjective. Its pi2 is nonzero because the map pi1(SO(p)) x pi1(SO(q)) -> pi1(SO(p+q)) has a nonzero kernel. For p,q>=3 use the diagonal in Z2 x Z2; for either p or q equal to two use a nonzero even winding. Since pq>=4, it cannot be S^(pq). Recall pi1(SO(4))=Z2, not Z2 x Z2.
* H_r(C), r>=3: U(p+q)/(U(p) x U(q)) is simply connected, and pi2 is nonzero because the map Z x Z -> Z on pi1 is addition. Its dimension 2pq>=4 rules out a sphere.
* H_r(H), r>=3: Sp(p+q)/(Sp(p) x Sp(q)) is simply connected, and pi4 is nonzero because the map Z x Z -> Z on pi3 is addition. Its dimension 4pq>=8 rules out a sphere. The facts pi3(Sp(k))=Z and that standard inclusion preserves its generator follow inductively from Sp(k-1)->Sp(k)->S^(4k-1), starting at Sp(1)=S3. This avoids an unexplained cohomology assertion for quaternionic Grassmannians.
* H_3(O): the rank-one and rank-two support orbits are the Cayley plane (complementation identifies them). Its cells have dimensions 0,8,16, hence H8=Z. It cannot be S16.

The homogeneous-space fibrations and their long exact sequences are classical ingredients, not novel claims. No classification of arbitrary submersions from spheres is needed.

## Subsequent simplification developed during this audit

The reusable proof in `stage2-topology-proof.tex` improves on the source proof: all determinantal algebra is unnecessary. If an affine real symmetric pencil X(x) is PSD with nullity one on a sphere and has no common nonzero kernel vector, its kernel-line map is injective. Indeed a shared kernel vector k at two distinct sphere points makes the affine scalar function k^T X(x) k nonnegative on the sphere with two zeros. A nonconstant affine function nonnegative on a sphere has at most one zero, so this function is identically zero. PSD then puts k in every kernel, a contradiction. The projective support covering has two-point fibers and surjective image, contradicting this injectivity.

For H3R, use finite status-pattern elimination and C1 gluing to produce the affine sheet, then apply this lemma. For the Hermitian selected-rank equality analysis, every zero-rank dual block vanishes identically, so the one remaining real factor is affine directly; the same lemma excludes every real order R>=3. Thus the argument does not require the even-quadratic inversion formula, determinant divisibility, a timelike Lorentz normalization, or the special 3-by-3 coefficient computation. The older detailed audit below establishes validity of the source argument but is not the recommended manuscript proof.

## Proof audit: exclusion of H_3(R) for the ball

The source proof is correct. For that determinantal route, all steps below matter; the new affine-kernel argument above bypasses steps 5–8.

1. Saturation gives complementary global ranks 1 and 2 and a support local diffeomorphism S2->RP2. Each open piece maps onto an open projective set.
2. For each finite continuous nonnegative ray factor a_j,b_j, {f>0} union interior{f=0} is dense open. Intersect these sets for all functions and partition by their finite zero/positive patterns. On each pattern set Omega, at least one of a_j or b_j is identically zero, so every cross ray summand a_j(x)b_j(y) is zero for x,y in that same pattern set. Disconnected pattern sets cause no problem.
3. Rank-one PSD matrices with support in a projective open set span S^3: any annihilator would be a quadratic form vanishing on an open set and therefore identically. Choose six rank-one factors at fixed points in Omega. Evaluating the slack against them forces the rank-two sheet to be the restriction of an ambient affine pencil on Omega.
4. A C1 map S2->W that agrees on a finite dense collection of open pieces with affine maps must agree with one global affine map. Distinct affine maps can have coincident first tangential jets at at most one sphere point: their difference then has form M(z dot x - 1), M nonzero. The closures of distinct pieces intersect in at most finitely many points. Removing these points leaves a connected sphere, contradicting a nontrivial finite clopen partition. This argument uses C1 of the matrix sheet and dimension at least two.
5. Write X(x)=C0+sum x_i C_i, PSD rank two everywhere on S2. The support covering makes its kernel lines cover RP2. Therefore C0, the spherical average, is positive definite; a null vector would belong to every boundary kernel.
6. det(t C0+sum x_i C_i) is a cubic vanishing on the sphere quadric, so it equals Q(t,x) ell(t,x), Q=t^2-|x|^2. This polynomial divisibility is elementary: polynomial-divide by |x|^2-1 in one coordinate in the dehomogenized polynomial; the degree-one remainder in that coordinate vanishes at the two sphere roots on an open disk and so both coefficients vanish. Homogenize. It is NOT correct to infer that the determinant vanishes identically on the whole pencil.
7. At each x on S2,

       partial_t det L(1,x) = tr(adj(X(x)) C0) = 2 ell(1,x) > 0.

   Thus ell(t,x)=a t+b dot x with a>|b|. A future Lorentz transformation preserving Q sends ell to a positive multiple of t. Positivity of the pencil persists because the future cone is generated by its boundary rays. Its value at the new center remains positive definite (or use that every interior cone point dominates a positive multiple of the old center). Normalize by congruence to obtain det(tI+A(x))=t(t^2-|x|^2); the multiplier is one by comparing t^3.
8. The required real symmetric A:R3->S3 does not exist. Coefficients imply tr A_i=0, tr(A_i A_j)=2 delta_ij, det A(x)=0. Put A1=diag(1,-1,0). For a unit orthogonal B write [[a,d,e],[d,a,f],[e,f,-2a]]. Expanding det(A1+sB) gives a=0, e^2=f^2, def=0, while the norm condition gives d^2+e^2+f^2=1. Therefore (d,e,f) is either (+/-1,0,0) or (0,+/-1/sqrt2,+/-1/sqrt2). Two orthogonal choices for A2,A3 either mix these types, producing a nonzero x2 x3^2 or x2^2 x3 determinant term, or both have the second type, producing a nonzero x1 x2 x3 term. Contradiction.

This establishes the ball result without an external theorem about determinantal representations. Calling the final pencil a 'Clifford pencil' is unnecessary and potentially misleading: the proof does not establish Clifford anticommutation relations.

## Additional general-body consequences

The H3R exception, if realized for a nonquadratic body, requires at least three active ray factors. The two-sheeted support covering has deck involution tau. At the cross pair (tau x,contact(x)), the matrix summand vanishes but strict convexity gives positive slack. Thus U_j={x: b_j(contact(x))>0, a_j(tau x)>0} cover S2. Each U_j is disjoint from tau U_j because diagonal products vanish. Their images give section domains of the double covering. If there were at most two, the mod-two square of the nonzero degree-one class of RP2 would vanish (cup-length bound for sectional category), contradicting H*(RP2;F2)=F2[alpha]/(alpha^3). This is optional once the manuscript specializes its principal global theorem to balls; if retained, cite Schwarz explicitly and do not call it a construction.

The ledger M-total_rank >= n follows pointwise from c_i<=m_i-r_i, equality only for positive factors of rank two. Thus its equality classification needs no H3R exclusion. The all-cap ball frontier also excludes H3R by size when d<s+1; it does not logically depend on the lengthy order-three proof, though the latter supplies the full saturation classification and is relevant to comprehensive coverage.

## Literature checked and citation corrections

* Nomura, *Grassmann manifold of a JH-algebra*, Annals of Global Analysis and Geometry **12** (1994), 237–260. Correct DOI is **10.1007/BF02108300**. The workbench link `10.1007/BF02099191` is incorrect. Confirmed on the primary publisher page: <https://link.springer.com/article/10.1007/BF02108300>. The local metadata already has the correct DOI but marks the article unread. Do not pretend its full proof was consulted; the differential calculation above is self-contained.
* Hatcher, *Algebraic Topology* (Cambridge University Press, 2002), author-hosted Chapter 4: <https://pi.math.cornell.edu/~hatcher/AT/ATch4.pdf>. Example 4.47 (printed pp. 378–379) constructs OP2 by attaching a 16-cell to S8. Examples 4.53–4.55 (printed pp. 381–383) give the Stiefel/Grassmann and classical-group fibrations. The covering and Kunneth steps are standard material in Chapters 1 and 3. These support the elementary computations above.
* Baez, *The Octonions*, Bulletin of the AMS **39** (2002), 145–205, DOI 10.1090/S0273-0979-01-00934-X. Author-hosted Section 3.4, <https://math.ucr.edu/home/baez/octonions/node12.html>, explicitly identifies trace-one projections of H3(O) with Cayley-plane points and trace-two projections via complementation. The local literature note contains the corresponding page locators (preprint pp. 30–34).
* The local Sankaran–Sarkar note for arXiv:0805.0509 gives a usable alternative source for the complex/quaternionic Schubert-cell structure (preprint p.6). This is unnecessary if the fibration proof above is used.
* Faraut–Koranyi remain the source for simple EJA classification and Peirce decomposition. Derive the support differential in the text, so novelty is not implied for Nomura's idempotent geometry.

## Novelty boundary and remaining caveats

Targeted searches identified classical idempotent-orbit geometry, Grassmannian topology, and the standard conic slack framework, but no primary source establishing this particular saturation-to-covering result. A qualified novelty statement may attach to the implication from saturated global slack factorization to the joint covering and the resulting conic resource classification. It should not attach to topology, orbit classification, or the covering theorem themselves. The H3R exclusion is a self-contained further result; do not claim broad minimal determinantal-size novelty without a separate determinantal-representation literature search.

The scalar continuity assumptions, finite factor count, global labels, full (not diagonal-only) slack identity, and distinction between global selection regularity and an arbitrary exact affine lift are material assumptions and should be visible in the theorem statement.
