# Foundations audit

Scope: the mathematical foundations in §§1–8 of
`research-20260928b/sfree/optimal-intersection-cuts.md`, its two reviews,
`research-20261001/intersection-literature/note.md` §§4–5, and the final
October closeout. This audit re-derived proofs. It did not run experiments,
search the literature, inspect CI, or change the research notes.

The principal theorems survive. Three statements need substantive repairs:
Lemma 13 needs an orientation before asserting a positive pencil multiplier;
the final §6.1 claim that varying the apex makes the point rule reach every
maximal affine set is false; and the efficacy remark needs an actual
separation oracle and a specified metric. The unproved wedge maximality and
neighbourhood claims can be completed. The closed completion has an exact
empty exceptional class, so its admissible nonempty slices can be called
maximal without an unspecified exception.

## Claim inventory

Each numbered item below records the original identifier, final status,
statement, proof dependencies or correction, and manuscript disposition.
Recorded numerical observations belong to the computation author; their
mathematical implications are qualified here.

1. **§1 validity and one-cut value: retain.** For closed convex free (C)
   with the apex in its interior, (a_j=1/\alpha_j\ge0) gives the valid
   inequality (a^T\lambda\ge1). The cut value for nonnegative costs is
   \(\min_{j:a_j>0}\omega_j/a_j\), with value (+\infty) when the cut
   is infeasible. Infinite ray steps are recession directions because a
   closed convex set containing the whole ray from an interior point has
   that direction in its recession cone. Convex combinations with positive
   weight on the apex lie in the interior, proving validity. Explain that
   zero costs on infinite steps do not contribute a term (0\cdot\infty).
   Main text: setting and supporting-simplex interpretation.
2. **Theorem 1(1): retain.** For positive costs, closed (X\ne\varnothing)
   has an attained minimum. Nonnegative coordinates and positive costs make
   every objective sublevel compact. Also (z_K>0), since (X) is closed
   and avoids zero. State finite feasible value separately from (X=\varnothing).
3. **Theorem 1(2): retain as background.** The supremum of single-cut values
   equals (z_K) for every closed (S) and positive costs, including an
   infinite value. Fatten the compact image of the ray-coordinate simplex
   with cost at most (t<z_K), using its positive distance from closed (S).
   This gives coefficients at most \(\omega_j/t\). No full-dimensionality
   or injectivity assumption on (P) is needed. Use the direct proof;
   precise prior-work comparisons come from the sole literature author.
4. **Theorem 1(3): retain.** Extend a full-dimensional free set by Zorn.
   For a nested chain, every interior point of its closed convex union lies
   in some chain member's interior: enclose the point in a finite simplex
   with vertices approximated from the union. Maximal extension preserves
   freeness and improves all ray steps. Main proof can state this argument.
5. **Theorem 1(4): retain, with complete replacement proof below.** For
   (C^1) sublevel (S), if every optimum contact (t) satisfies
   \(\nabla q(t)^T(\bar s-t)>0\), the optimum simplex can be thickened at
   its apex without admitting an interior feasible point. This is a
   sufficient transversality condition, not a necessary characterization.
   The source's language about a physical “far face” needs replacement:
   a noninjective image need not have the advertised physical face, but
   scaling its ray-coordinate representation supplies the contradiction.
6. **Theorem 1(5): retain as background.** The unrestricted closure at one
   fixed corner equals \(\operatorname{cl}(\operatorname{conv}X+\mathbb R_+^N)\).
   Separate a nonnegative point outside this closed dominant by a
   nonnegative normal. Perturb the normal by a small positive multiple of
   the all-ones vector, then apply the approximation theorem. Points
   outside the orthant are already excluded. Do not identify this dominant
   with the hull in the original polytope.
7. **Theorem 1 remarks (i)–(iii): retain/qualify.** Arbitrary (P) is
   allowed. Generic attribution is superseded by the October literature
   audit. A Fritz John system with positive objective multiplier implies
   transversality after multiplication by an optimum ray vector, because
   \(\sigma\nabla q(t)^T(\bar s-t)=\sigma_0 z_K>0\). This is an implication;
   no converse is needed. Move precise cone cases to their own proposition.
8. **Proposition 2(a): retain.** For
   \(q=(x+1)y+1\), positive orthant rays and costs ((0,1)), the corner is
   infeasible but every free neighbourhood must have finite first step,
   so every single cut has value zero. The point
   ((2/\delta,-\delta/2)) gives (q=-\delta/2<0) inside a set with an
   infinite first step. Attribute the mechanism, not novelty. An optional
   strengthening uses \(q=(x+1)y+1-y^2\): the corner bound is the finite
   attained golden ratio, while the same argument gives single-cut
   supremum zero. This makes clear that infeasibility is not the cause.
9. **Proposition 2(b): retain.** For
   \(q=x-x^2+(1-y)^2\), costs ((1,1)), the only cost-one feasible point
   is ((0,1)). For (x\ge1), feasible nonnegative coordinates have cost
   at least the golden ratio. If a free neighbourhood contains ((0,1)),
   mixing it with ((-s,0)) from the apex ball creates
   ((-s^2,1-s)) in its interior with (q=-s^4). Hence positive costs do
   not ensure attainment. Treat as a quadratic realization of KY's example.
10. **Lemma 3: retain.** Every fibre \(\{\mu\ge0:P\mu=P\lambda\}\) is a
    pointed polyhedron. Its vertices have independent positive columns,
    and its recession cone is \(\{\delta\ge0:P\delta=0\}\). This proves
    the exact unclosed convex-hull identity and the rank support bound for
    any nonnegative objective. A fibre LP has a vertex optimum whenever
    the objective is bounded below. Include the convex-hull identity in
    the appendix; do not replace it by only an optimization corollary.
11. **Theorem 4: retain.** Independent-support optima use at most
    \(\rho=n_++n_0+1-\mathbf1_{b\notin\operatorname{range}Q}\) rays.
    In the regular case (Q) is nonnegative on a tangent subspace of
    dimension (|J|-1); in the abnormal case it is nonnegative on the
    whole supported subspace. Intersecting the kernel with (b^\perp)
    saves one dimension exactly when (b\notin\operatorname{range}Q).
    Full proof checked, including the abnormal double-cone argument.
12. **Theorem 4 reverse-convex corollary: repair hypothesis.** The source
    says merely that \(\operatorname{cl}(\mathbb R^k\setminus S)\) is
    convex. This alone does not ensure that the closure is (S)-free:
    (S=\{0\}\subset\mathbb R) is a counterexample. The valid assumption
    is that the complement itself is convex, or explicitly that its
    closure is convex and its interior misses (S). Under that assumption
    the closure is the unique maximal full-dimensional free set and its
    cut attains the bound by Theorem 1. Strictly concave (q) separately
    has the one-ray property from Theorem 4. Do not describe the generic
    reverse-convex result as an inertia consequence.
13. **Theorem 4 bilinear and two-variable corollaries: retain corrected
    version.** Bilinear (q=w-xy) has ((n_+,n_0)=(1,1)) and linear term
    outside the quadratic range, hence (ho=2). In two variables only
    \(\min(k,\rho)\le2\) is guaranteed; (ho) can be three. The source
    revised this correctly.
14. **Theorem 5(1): retain with output qualification.** For fixed
    \(r=\min(k,\rho)\), enumerate (O(N^r)) supports and decide an
    existential quadratic formula in at most (r) variables. Fixed-variable
    real-algebraic decision is polynomial in the rational bit size. Relative
    approximation concerns finite positive values; detect infeasibility
    separately, and use algebraic root-size bounds or isolation to obtain
    an initial bracket. Bisection then costs polynomially in
    \(\log(1/\epsilon)\). The generic numerical KKT implementation does
    not replace the exact decision theorem on singular faces.
15. **Theorem 5(2): retain, replace incomplete degeneracy discussion.** A
    sufficiently small generic right-hand-side perturbation of
    (D_\omega=\{y:P^Ty\le\omega\}) makes it simple. Every resulting
    active independent (k)-set limits to an original vertex and its normal
    cone lies in that original normal cone. These cells cover \(\operatorname{cone}P\)
    and preserve the unperturbed fibre cost on each cell. Truncate an
    unbounded pointed polyhedron with one extra facet to invoke the upper
    bound theorem. In dimension three there are at most (2N-4) old
    vertices/cells; the normal-fan edge graph is a simple planar graph on
    at most (N) ray directions, giving at most (3N-6) two-ray edges.
    Remove zero or duplicate directions before counting. Appendix proof.
16. **Theorem 5(3): retain with exact case distinctions.** The nonsingular
    face formula is generic only; require a nonzero denominator and check
    the positive KKT multiplier and coordinate feasibility. For at most
    two rays, reciprocal radius (u) solves
    (g_0u^2+b(\theta)u+a(\theta)=0). Maximize its positive larger root
    on the discriminant-feasible part of ([0,1]). Candidates are endpoints,
    discriminant roots, and roots of
    (D'^2-4b'^2D=0), with (D'=0) included when appropriate. If the
    stationary polynomial vanishes identically, the square root is affine
    on components and the larger root is piecewise affine, so endpoints
    and discriminant roots suffice. No positive candidate means infeasible.
17. **Theorem 5(4): retain.** Motzkin–Straus gives
    \(z_K=\sqrt{\mu\,\omega(G)/(\omega(G)-1)}\). The rational threshold
    choice \(\mu=\omega_0(\omega_0-1)\) reduces clique decision. With
    (mu=1), adjacent values have ratio at least
    (1+1/(2k^2)), exceeding
    \((1+\delta)/(1-\delta)\) for \(\delta=1/(5k^2)\), (k\ge2).
    Include the adjacency normalization and edgeless case. Both dimension
    and inertia support parameter must be unbounded for this reduction.
18. **Theorem 5 efficacy remark: qualify and complete.** A membership test
    alone does not give the quoted ellipsoid conclusion. Define efficacy
    in the ray-coordinate Euclidean norm, obtain a violated-point
    separation oracle from the same fixed-variable algebraic problem, and
    bound the search region using a positive feasible uniform vector.
    The support-value identity extends to nonnegative weights by positive
    perturbation, so boundary oracle inputs are covered. State weak
    optimization to prescribed accuracy, not an exact efficacy theorem
    for an unspecified original-coordinate metric.
19. **Proposition 6: retain.** The fixed eigen-coordinate point rule has
    steps (x_0+1/x_0) and \(\sqrt{1+x_0^2}\); the strip has value one;
    the corner value is \(\epsilon x_0+\sqrt{1-\epsilon^2}\) under the
    stated feasibility condition. With (epsilon=x_0^{-2}), the rule ratio
    tends to zero. This concerns one fixed coordinate implementation,
    not the full transformed point-rule family. Appendix exact proof.
20. **Remark 7: retain and upgrade limit proof.** With the given perturbation
    (r_2=-r_1+\eta n), (eta=a^{-3}), a boost sends rays to
    ((0,1)) and \((\eta h,-1-\eta c)\), where
    (h=\sqrt{1+2a^2}), (c=2a\sqrt{1+a^2}/h). Thus
    \((1+\eta c)^{-1}\le z_K\le1\), and the oblique split gives the
    lower endpoint. The sum of all constant-direction cut coefficients
    has minimum
    \(L=\sqrt{4(1+a^2)+4\eta a\sqrt{1+a^2}/h-\eta^2/h^2}\).
    The common point ((1/L,1/L)) lies in every such cut, giving closure
    value at most (2/L\to0). This proves the pointed-cone asymptotic
    claim without relying on the three numerical table rows.
21. **Theorem 8(1): retain, supply elementary classification and orbit
    proof.** Separate a full-dimensional free set from each of the two
    convex Lorentz cones. The resulting two timelike-or-null normals can
    be replaced by null nonnegative combinations. Thus every maximal set
    is \(\{\gamma_1^Tx\ge y,\gamma_2^Tx\ge-y\}\), with unit directions
    not opposite. Each is maximal by its two feasible null contacts.
    Explicit Lorentz orthonormal bases send a fixed pair ((\lambda,\pm1))
    to the target pair. For (n\ge2), choose the positive-complement
    extension to have determinant one, obtaining (SO^+(n,1)).
22. **Theorem 8(2): retain.** For signature ((1,m)), the complement has
    two convex components. Connected interiors force a free set into one;
    the only maximal sets are the two closed Lorentz cones.
23. **Theorem 8(3): retain with clarified product-before-slice wording.**
    Cone a full-dimensional free affine slice, classify the resulting
    homogeneous free cone, and slice back. For radical coordinates, every
    maximal full-dimensional free set has the feasible set's lineality.
    If the slicing functional has nonzero radical part (h), the affine
    bijection gives a product with (h^\perp) in the slice; the equivalent
    homogeneous product with all radical coordinates occurs before slicing.
    The old “full-dimensional” repair is necessary. Appendix full proof.
24. **Theorem 8 consequences: retain/qualify.** Every indefinite two-variable
    quadratic has the required homogenized signature, so the full orbit
    supremum equals the corner bound. This is not a universal attainment
    statement: Proposition 2(b) itself is an indefinite two-variable example
    with non-attainment. The SOCP feasibility relaxation with direction
    norms at most one remains free and can be extended to a maximal pair,
    so it gives the same supremum. The point rule and free-direction orbit
    must remain separate.
25. **§6.1 point-rule characterization: retain in homogeneous form.**
    The transformed rule reaches precisely the pairs whose tangency rays
    positively span the homogenized apex: (u=a(\gamma_1,1)+b(\gamma_2,-1)),
    (a,b>0). For signature ((2,1)), the displayed angle formula describes
    a one-parameter family; for general ((n,1)) its parameter dimension
    is (n-1), not one. The full family has dimension (2(n-1)).
26. **§6.1 slice chord/enlargement: retain with dimensions specified.** The
    chord interpretation requires both tangency rays to meet the slice with
    positive scaling. In the ((2,1)) slice, an asymptotic replacement is
    one of at most two null supporting halfspaces at infinity. Homogenize
    the replaced affine inequality before asserting that it vanishes on
    its null ray. Numerical miss counts are 13 of 36 finite corners, with
    four excluded infinite corners; full MS replacement values are numerical.
27. **§6.1 final varying-apex gloss: false, exclude and replace by exact
    asymptotic example.** For (S=\{xy\ge1\}), the quadrant
    (K=\{x\ge0,y\le0\}) is maximal free and has no finite contact with
    (S). Its two homogeneous tangency rays lie in (t=0), so their span
    contains no affine apex. No plain point rule produces it at any apex.
    The two-facet MS enlargement also retains at least one finite contact
    because the positive apex combination has slice coordinate one; thus
    it cannot produce this quadrant either. Theorem 8's unrestricted orbit
    conclusion is unaffected.
28. **§7 nonlocal closure: retain.** For a polytope, intersection over all
    operations \(\operatorname{conv}(P\setminus\operatorname{int}C)\)
    using arbitrary free (C) equals \(\operatorname{conv}(P\cap S)\).
    Separate a point from the compact hull and fatten the compact lower
    objective slice of the polytope. Distinguish this operation from the
    basis-generated rank-one intersection-cut closure.
29. **Proposition 9: retain.** The disk is the unique maximal full-dimensional
    free set, so the two cuts at the lower triangle vertices dominate every
    other first-round basis cut. Exact edge roots give
    (t=(1+2\sqrt{13})/17); cut intersection height is
    ((1+\sqrt{13})/6<2t). The second-round basis at that intersection
    gives the hull chord. Include the finite original basis list and both
    closure definitions to avoid an apparent contradiction with item 28.
30. **§8 rank-two quadratic classification: retain.** A quadratic rank-two
    indefinite part can be written as a product of two linear forms.
    If (b) lies in their span, only two affine coordinates matter and
    the preceding orbit result applies to the supremum. If it does not,
    take the independent linear term as the third coordinate and obtain
    (w-xy) or its negative, with homogenized signature ((2,2)).
    Replace “attains” by “has supremum equal to” in the two-coordinate case.
31. **Lemma 10(1): retain.** Determinant automorphisms preserve or interchange
    the two rulings of maximal rank-one matrix planes, giving (AMB^T)
    or (AM^TB^T), with determinant product one. Give this elementary
    rank-one-plane argument instead of relying solely on a group identity.
32. **Lemma 10(2): retain.** Sylvester map
    (x_1I+x_2J+y_1\operatorname{diag}(1,-1)+y_2\bigl(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\bigr))
    has determinant \(\|x\|^2-\|y\|^2\), and its symmetric part has
    eigenvalues (x_1\pm\|y\|). Images are exactly
    \(\{M:\operatorname{sym}(F^TM)\succeq0\}\), (det F>0), modulo
    positive scaling. Transposition fixes the seed set.
33. **Lemma 10(3): retain with contact domain.** Freeness follows from
    \(\det(S+kJ)=\det S+k^2\). Rank-one membership is precisely
    (F^Ta\in\mathbb R_+b). On the (h=1) slice the Möbius contact graph is
    (y=(F_{11}x+F_{21})/(F_{12}x+F_{22})) on the domain
    (F_{12}x+F_{22}>0), with strictly positive derivative. The positive
    domain must be stated; the full rational graph is not the contact set.
34. **Lemma 10(4): retain with exact exception.** The retained normals satisfy
    (v^TZv\ge0), (Z=\operatorname{sym}(F^TE)). A two-term balanced
    rank-one decomposition proves the dual equality and hence
    \(B_F=\operatorname{cl}(C_F+\mathbb R_+E)\). For (F=\bigl(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\bigr))
    with positive determinant, the exceptional class is exactly (b=0,a<0):
    its completion is ({h\le0}), with empty (h=1) slice. Every other
    completion slice is full dimensional and maximal; complete proof below.
35. **§8.1 point lowering and SCIP Case 4: retain.** On the positive slice,
    the sum is closed and membership is exactly a lowering
    (M(s)-\tau E\in C_F), (0\le\tau\le q(s)). In limits with
    (h\to1), determinant nonnegativity bounds (	au\le\det M/h), proving
    the closure and slice interchange without an unsupported generic
    closure-intersection rule. The cap-support identity of SCIP's formula
    is correct; code comparisons remain saved evidence, not a proof.
36. **Theorem 11(1): retain.** Inertia gives two rays; the exact reciprocal
    formula gives (O(N^2)) algebraic candidates. The 3-D normal-fan version
    uses a convex-hull computation and at most (N+(3N-6)=4N-6) one/two-ray
    problems when rank (P=3); lower-rank cases use their lower-dimensional
    fan or all pairs. State the rank hypothesis for the 3-D hull claim.
37. **Theorem 11(2): retain.** A failed transversality contact has an optimal
    independent-support representation. A regular supported KKT system
    would make transversality positive; hence the supported gradient
    vanishes. The abnormal inertia bound permits only one ray, which is
    tangent at its first contact. This is a sufficient attainment statement,
    not necessity in all tangent cases.
38. **Proposition 12: retain.** For a positive target, ray endpoints in the
    orbit set are (N) affine (2\times2) LMIs in (F), and strict apex
    membership is one further LMI. Strict apex membership forces
    (det F>0), since (q(\bar s)>0). Positive scaling replaces the strict
    LMI by \(\operatorname{sym}(F^TM(\bar s))\succeq I\) without changing
    feasibility. Feasible targets are nested, giving a bisection feasibility
    scheme. Do not call numerical SDP infeasibility an exact certificate.
39. **Lemma 13: correct sign, retain rigidity.** Orient (d_x>0). Then
    (F^T=\theta J\operatorname{adj}(M_0(d)+uM(t))), (	heta>0), has
    constant positive determinant and the required contact. Without this
    orientation the exact sign condition is (	heta d_x>0), so the printed
    universal (	heta>0) was false. Two-sided tangency forces the contact
    null quadratic entry and off-diagonal entry to vanish and makes all
    lowerings zero. For a ruling edge, an invertible (F) is impossible.
    Use (u), not the shared ray condition number symbol (kappa).
40. **Theorem 14(1): retain with direct certificate.** For barycentric
    ((a,b,c,d)) of ((\bar s,v_1,v_2,v_3)), let
    (Q=w(a+b+c+d)-xy). The exact identity is
    \[
    64Q=3[16(b-c)-5a+2d]^2+21a^2+148d^2+1036ad+192ac+1280bd.
    \]
    Nonnegativity and equality cases prove the unique simplex contact
    ((b,c)=(1/2,1/2)) directly. This replaces a repository script dependency.
41. **Theorem 14(2): retain.** The oriented pencil has
    (K_A(\bar s)=[12-8\sqrt2,12+8\sqrt2]),
    (K_A(v_3)=[-13/5-2\sqrt{30}/5,-13/5+2\sqrt{30}/5]), which are disjoint.
    The two printed scalar separating witnesses also exclude lowerings for
    every parameter; their slopes and endpoint signs are exact. Give their
    formulas in the appendix, not only the intervals.
42. **Theorem 14(3): retain with replacement compactness proof.** Normalize
    (F_n), bound all lowerings by the corresponding (q), and pass to a
    limit. Positive determinant contradicts the pencil certificate. In a
    rank-one limit the lowered vertices lie in an affine plane. The contact
    midpoint forces the two edge lowerings to zero. A vertical plane cannot
    contain the full tetrahedron. Otherwise its graph is a plane above
    (xy) over the full projection and equal at an interior projection
    point; the mixed derivative forbids that. Convex combinations of the
    lowered vertices have nonnegative determinant as limits of base-cone
    points, so no unsupported Kuratowski-limit freeness assertion is needed.
43. **Theorem 14(4): complete with a simpler stability proof.** Strict gap
    persists in an open neighbourhood by the same normalized compactness
    argument with perturbed data. The corner value is continuous here:
    compact positive-cost sublevels give lower semicontinuity; a tiny radial
    extension of the optimum has (q<0), giving upper semicontinuity.
    Unrestricted attainment persists because all perturbed optima approach
    the unique original optimum, where the transversality value is (3/2).
    This avoids assuming the whole tangent-edge configuration persists.
44. **Theorem 14 second rational example: retain for A only.** A six-edge
    table and indefinite Hessians on every triangular face prove its unique
    simplex contact. Edge ([v_1,v_2]) has polynomial
    (147t^2/2-21t+3/2), with unique zero at (t=1/7).
    The other five minimum values are (71/288,5/4,5/4,3/2,21/4).
    The two displayed A intervals are disjoint. A normalized rank-one
    matrix would confine the full tetrahedron to a plane, so A's gap is
    strict. B's value remains numerical; do not infer B strictness here.
45. **Remark 15 wedge: complete and retain.** Affinely shear to
    (W=\{x\ge0,y\le0,w\ge0\}), (S=\{w\le xy\}).
    Adding a point beyond either vertical facet creates (q<0) by mixing
    with an interior point far along a ruling. Adding a point below (w=0)
    in the quadrant creates (q<0) after scaling toward the origin and
    mixing with an (O(\epsilon^2)) interior point. Hence W is maximal.
    It has two distinct contacts on one ruling, so the rank-one orbit
    contact identity excludes every invertible (F), including completions.
    Do not rely on an unproved blanket statement about curved boundaries.
46. **Remark 15 ruling ties: retain corrected language.** Two distinct
    optimum contacts on a common ruling force (F^Ta) into two distinct
    positive one-dimensional spans, hence zero, contradicting invertibility.
    This holds for both A and B, because boundary contacts cannot be lowered.
    Replace “only for ties in w” by the precise multiple-contact statement;
    reduced costs themselves need not be equal.
47. **§8.6 adversarial/random observations: qualify.** Preserve saved cohort
    records with the computation author. A gap in one-cut strength does not
    establish a closure gap. Old B local-search values are lower bounds.
    The near-boundary 0.028 value is superseded by the exact binary-float
    bracket [0.03052,0.03056]. General no-angle and depth-order theorems are
    handled by the depth author. Do not retain the stale angle-threshold
    speculation or treat the numerical table as a theorem.
48. **Proposition 16(1): retain with direct certificate.** For the corresponding
    barycentric homogeneous (Q),
    \[
    512Q=(64a-79c-32d)^2+31c^2+512d^2+1280ad+4032cd
       +128b(8a+c+2d).
    \]
    Equality forces (a=c=d=0,b=1), giving unique support one.
    Transversality values (2,1/4,1/2) and KKT inactive multipliers (1/8,1/4)
    are correct. This certificate also accounts for every simplex face.
49. **Proposition 16(2): retain.** The four printed integer positive definite
    matrices have determinants (263,791,224,64), and their matrix products
    sum to zero. Thus every PSD vertex LMI is zero, forcing (F=0) because
    the four affine-independent vertex matrices span all (2\times2)
    matrices. Normalized compactness gives a strict A gap. B strictness at
    this example remains unproved here; the closure author has a separate
    later certificate and will state only the certified result.
50. **Intersection-literature Proposition A: retain with self-contained
    cone proof below.** Full cone span is sufficient for exact attainment
    even with zero costs; the broader containment hypothesis
    (S-\bar s\subseteq\operatorname{cone}P) suffices. Treat (z=0) and
    (z=+\infty) separately rather than using (w/z). Under containment,
    an infinite value forces (S=\varnothing); a zero value makes every
    valid single-cut value zero. The finite positive construction is below.
51. **Intersection-literature §4.3 bilinear cone equivalence: retain.** A
    proper finitely generated cone lies in a homogeneous halfspace, while
    either bilinear sublevel lies in no affine halfspace. Therefore
    (S-\bar s\subseteq\operatorname{cone}P) iff that cone is all of
    (mathbb R^3). Saved 0/120 full-span counts remain numerical.
52. **Intersection-literature Claim 4.4a and corrected KY corollary: record,
    do not use as proof dependency.** The printed KY corollary is refuted
    by the saved exact counterexamples; the ray-avoidance amendment follows
    conditionally from the cited proposition. The direct fattened-simplex
    theorem avoids the unread upstream proof steps. Theorem 14 demonstrates
    a transversality equality case outside that strict criterion. Literature
    discussion should attribute the mechanism with its draft status.
53. **Intersection-literature Proposition B: retain.** BCM's (14a) is exactly
    the rotation part (F^T\in SO(2)). The trace/traceless norm identity
    proves equality. Nonrotation (F) has different one-dimensional
    lineality, so cannot be a rotation member. All positive-determinant
    orbit interiors have (ad-bc>0), whereas (14b) lies on the other side.
    Include the diagonal (F^T=\operatorname{diag}(2,1/2)) illustration or
    the stronger general argument in the appendix. This is a three-parameter
    extension of a known one-parameter family, not an entirely new family.

## Replacement proofs for the main gaps

### Attaining the corner value under transversality

Let (z>0) be finite and (T=\bar s+P\{\lambda\ge0:\omega^T\lambda\le z\}).
Its feasible contacts (M=T\cap S) are compact, and (q=0) on (M): a
point with (q<0) could be scaled toward the apex to give a smaller cost.
Suppose (C_\delta=\operatorname{conv}(T\cup B(\bar s,\delta))) contains a
point of (S\setminus M) for arbitrarily small (delta). Write such points
as (p_n=\theta_n b_n+(1-\theta_n)t_n). Compactness gives a limit in (M).
If the limiting (	heta>0), its ray-coordinate representation has cost at
most ((1-\theta)z<z), a contradiction; hence (	heta_n\to0) and
(t_n\to M). Uniform transversality gives
\(\nabla q(\xi_n)^T(b_n-t_n)>\eta\) near this compact set. For
(	heta_n>0), the mean value theorem makes
\(q(p_n)=q(t_n)+\theta_n\nabla q(\xi_n)^T(b_n-t_n)>0\); for (	heta_n=0),
the point is already in (M). Thus (C_\delta\cap S=M) for small (delta).
A contact interior to (C_\delta) would be an interior local minimum of
(q), forcing zero gradient, contrary to transversality. Therefore the set
is free, contains the optimum simplex, and its cut attains (z).

### Exact domination under the cone containment hypothesis

Work first in (V=\operatorname{span}P). For (omega\ge0), the dual
polyhedron (D_\omega=\{y\in V:P^Ty\le\omega\}) is nonempty and pointed.
It has finitely many vertices (y^1,\ldots,y^m). Fibre LP duality gives,
for (v\in\operatorname{cone}P),
\[
\phi(v)=\min_{\lambda\ge0:P\lambda=v}\omega^T\lambda
       =\max_i (y^i)^Tv.
\]
If (S-\bar s\subseteq\operatorname{cone}P) and (0<z_K<\infty), set
\[
C=\{\bar s+v+u:v\in V, u\in V^\perp, (y^i)^Tv\le z_K\ \forall i\}.
\]
It contains a ball about the apex. A feasible point has (u=0) and
(phi(v)\ge z_K), so cannot be interior to these strict positive-level
halfspaces. Hence C is free. Each original ray remains in C at least up
to (z_K/\omega_j), and forever when (omega_j=0), giving domination of
((\omega/z_K)^T\lambda\ge1) and exact attainment. This proves the cone
case without relying on a repository proof or an unpublished corollary.

### Maximality and the exceptional completion

For (F=\bigl(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\bigr)),
(Z=\bigl(\begin{smallmatrix}a&b/2\\b/2&0\end{smallmatrix}\bigr)).
If (b=0,a<0), retained vectors have (v_1=0), and the completed cone is
({d h\ge0}={h\le0}). Its slice is empty. Otherwise (Z) has positive
directions and its positive set is dense in its nonnegative set. Every
strictly retained normal (N=Fvv^T) has a finite rank-one contact on
(h=1). At that contact, the normal cone of the completion is the single
ray generated by (N): pairing a dual matrix (FY) with the contact gives
(b_0^TYb_0=0), which for PSD (Y) forces (Y\) onto the one-dimensional
orthogonal ray. If a point outside the completion is added, it violates
some retained inequality and, by density, a strictly retained one. Its
addition makes that feasible contact an interior point, contradicting
freeness. Thus every nonempty completed slice is maximal.

### The wedge and a point-rule set with only asymptotic contacts

For the three-dimensional wedge, use the shear stated in item 45. The
interior-point mixtures there prove maximality for every outside point,
including points beyond two facets at once. Two distinct ruling contacts
exclude all orbit completions by the rank-one contact test.

For the two-dimensional point-rule example, (K=\{x\ge0,y\le0\}) misses
(S=\{xy\ge1\}). Adding (p_x<0) and mixing with
((\epsilon,-M)\in\operatorname{int}K) creates a negative-negative point
with product exceeding one; adding (p_y>0) uses ((M,-\epsilon)).
Hence K is maximal. Its two homogenized tangency rays both have (t=0).
A point-rule apex is a positive combination of the two tangency rays, so
cannot have (t=1). In the two-facet affine MS enlargement at least one
ray must have the positive slice sign and its inequality is retained,
giving a finite feasible contact. K has none. This is an exact exclusion,
independent of numerical scans.

## Recommended exposition and dependencies

Start with the ray simplex: the best bound from one cut is the largest
objective simplex that can be placed inside a free neighbourhood. Present
the generic supremum theorem, its cone case, transversality, and the two
boundary failures together. Then state rank and inertia support reduction,
exact two-ray computation, fixed-parameter complexity, and hardness.

Present the Lorentz classification before the determinant orbit. Separate
the free direction from the implemented point rule. Define A and B once,
prove the completion identity and exceptional case, and give the SDP
feasibility formulation. The tangent pencil explains the starting strict
counterexample; the support-one integer dual certificate prevents readers
from inferring that a tangent edge is the only obstruction. Put longer
certificates, the second rational instance, the constant-direction closure
limit, and efficacy qualifications in the foundations appendix.

The depth author's sharp contact theorem and depth bounds, the closure
author's restricted-family results, and the minors/convergence author's
later developments must use these definitions and must not reinterpret
suprema as attained optima. The exact original unrestricted rank-one
triangle example belongs here; restricted corner closures belong to the
closure section.

## Exact targeted checks actually run

- An inline SymPy script expanded all six edge quadratics for the first
  and second rational tetrahedra and the support-one tetrahedron, computed
  their exact stationary minima, and checked each triangular face's
  projected determinant. Result: the minima and determinant values in
  items 40, 44 and 48 agree; all relevant projected determinants are nonzero.
- A second inline SymPy script expanded the two supplied homogeneous
  nonnegative certificates in items 40 and 48. Both residuals were exactly
  zero. These are symbolic proof checks, not experiment reruns.

No project-wide checks were run and CI was not inspected.
