# Prewriting audit: algebraic cone thresholds and exact witnesses

Date: 2026-10-05. Scope: the common-field SOCP/MISOCP and algebraic-threshold developments assigned for the new Appendix L. This is an independent analytic source audit. It is not an external peer review or a novelty determination.

## Verdict and required coverage

I found no unresolved mathematical gap in the stated common-field feasibility and witness results after reconstructing their proofs. The source notes contain enough material for a self-contained appendix, provided the manuscript includes the nonconvex perturbation and projection arguments rather than citing repository notes for them. No mathematical experiment, CAS calculation, project-wide check, or CI inspection was run.

The required results belong in the paper. They are not native-PSD quadratic results: squared Lorentz-cone residuals may have indefinite Hessians. The minimum-norm field and recovery conclusions need their own argument. The following statements are supportable.

1. For fixed integer dimension and fixed continuous squared-Hessian span, exact feasibility over one explicitly represented real number field is decidable in polynomial Turing time, without boxes or Slater assumptions. The algorithm first returns an integer assignment whose original exact fiber is nonempty.
2. For rational original cone data and a rational affine objective, one isolated algebraic threshold can be appended with no increase in the original rational Hessian-span parameter. Running time includes the threshold's exact encoding length.
3. For a continuous cone system over the supplied field and fixed span, the unique minimum-norm feasible point has one absolute primitive-element representation of degree and total length \(L^{O(h+1)}\). It is recoverable in \(L^{C_h}\) time. The absolute field must include the input generator.
4. For fixed integer dimension and span, recovering the integer assignment and then applying the continuous witness algorithm to its original exact fiber gives a full mixed-integer algebraic feasible point in polynomial time. Its point is canonical within that fiber.
5. A known finite infimum permits an attainment query by adding its exact affine threshold. This is conditional on the supplied value and its encoding; it does not recover an unknown mixed-integer infimum.
6. For rational original cone data, a known attained affine-fractional optimum with a positive affine denominator admits exact point recovery through an affine optimal-level equation and one reciprocal cone. This adds at most one continuous Hessian direction.

There is no support for unrestricted integer dimension with unbounded integer variables being in NP, a runtime \(F(h)L^C\) with an absolute exponent, a witness restricted to the input field, a sharp \(L^{O(h+1)}\) recovery runtime, or a general optimizer/value theorem for separately encoded algebraic cone data.

## Material inspected and manuscript reuse

Primary repository sources read:

- [algebraic-threshold-misocp.md](../../../research-20260927/algebraic-threshold-misocp.md), including every proof section.
- [algebraic-threshold-misocp-review.md](../../../research-20260927/algebraic-threshold-misocp-review.md).
- [algebraic-socp-witness-recovery.md](../../../research-20260927/algebraic-socp-witness-recovery.md), [its algorithm review](../../../research-20260927/algebraic-socp-witness-recovery-review.md), and [its field review](../../../research-20260927/algebraic-socp-witness-field-review.md).
- [algebraic-coefficient-span-precision.md](../../../research-20260927/algebraic-coefficient-span-precision.md), especially the purely algebraic local-norm lemma.
- [nonconvex-hessian-span-frontier.md](../../../research-20260927/nonconvex-hessian-span-frontier.md), including genericity, the bounded minimizing sequence, common-limit elimination, and the boxed-value argument.
- [unbounded-misocp-frontier.md](../../../research-20260927/unbounded-misocp-frontier.md), including all rank charts, the pointwise uniform perturbation grid, the compressed projection formula, and its integer-witness use.
- [socp-hessian-span-frontier.md](../../../research-20260927/socp-hessian-span-frontier.md), especially the residual-gap and rational cone-lift interfaces.

A delegated independent analytic check examined the witness, field, and constructive reconstruction proofs, including the separate field-independent review. It found no substantive gap. No agent on this audit performed literature discovery or external-source research.

I read the manuscript brief and author conventions, Section 05, the relevant integer-query interface in Appendix D, and the elimination, height, and reconstruction proofs in Appendix J. Precise reuse:

- Appendix J Lemma **lem:qc-heights** gives the needed product-formula and local-height calculus.
- Appendix J Lemma **lem:qc-elimination** is algebraic; convexity does not appear among its hypotheses. It can be used for the nonconvex band KKT equations. A one-parameter application can be embedded in its two-parameter version by taking the second parameter dummy and the same root for every value of it. Alternatively, state its one-parameter specialization directly and refer to its proof.
- Appendix J Theorem **thm:qc-recovery** applies directly to the tuple consisting of the input generator and the canonical cone point. This is the constructive reconstruction interface needed here.
- Appendix J Theorem **thm:qc-kll** gives the paper's recognition contract. Its external-source verification remains Luna's responsibility.
- Appendix J Lemma **lem:qc-sign** supports exact verification at the selected output root.
- Do **not** apply **thm:qc-height**, **thm:qc-degree**, or **cor:qc-feasible-point** directly to squared cone rows: their native convex quadratic hypotheses are stronger than the cone setting.
- Do **not** substitute Appendix D Theorem **thm:constraints-integer-query** for the unbounded projection argument. That theorem assumes a bounded closed convex target and a rational separation oracle. The cone projection may be nonclosed, and the present argument uses a different established witness theorem followed by rational MILP.
- The final cone reduction may cite the same classical fixed-integer-dimension rational MILP algorithm already used elsewhere. It must explicitly allow a growing continuous dimension.

The paper should use \(L\) for total binary input length, \(t\) for integer dimension if Section 05 retains that notation, \(n\) for continuous dimension, \(h\) for squared-Hessian span, and \(\Lambda\) for the relative field-degree bound. Using \(L\) again for quotient dimension would conflict with the manuscript conventions.

## Exact input model and span

Specify
\[
 K=\mathbb Q(\alpha)\subset\mathbb R,\qquad
 p(\alpha)=0,\quad a<\alpha<b,
\]
where \(p\) is dense, primitive and irreducible, and rational nonroot endpoints isolate exactly the chosen real root. All coefficients are explicit rational polynomials in \(\alpha\) of degree below \(D=\deg p\). Count the dense polynomial, isolator, coefficient vectors, matrix dimensions and every listed scalar entry in \(L\). Then \(D\le L\). A succinct high-degree encoding is outside the theorem.

“Real number field” means a selected real embedding. It does not mean that the field has exactly one real embedding. Other embeddings need not preserve signs, convexity or feasibility.

For \(w=(z,x)\), let \(u_i(w)=A_iw+b_i\), \(t_i(w)=c_i^{\mathsf T}w+d_i\), and
\[
 q_i(w)=\|u_i(w)\|^2-t_i(w)^2,\qquad
 h=\dim_K\operatorname{span}_K
 \{2(A_{ix}^{\mathsf T}A_{ix}-c_{ix}c_{ix}^{\mathsf T})\}.
\]
Retain \(t_i\ge0\) everywhere. Flattening the matrices turns this dimension into a matrix rank over \(K\); the nonzero-minor criterion shows that it equals their real span dimension at the chosen embedding. It is not their rational linear-span dimension: \(H\) and \(\sqrt2H\) can have \(K\)-span one and rational span two.

When the original matrices are rational, extending scalars to \(\mathbb Q(\theta)\) preserves their rank. An affine threshold has zero Hessian, so the algebraic-threshold corollary uses the original rational \(h\).

All field linear algebra is polynomial in the explicit input. Multiplication by a field element is a rational \(D\)-dimensional linear map. An invertible \(r\)-by-\(r\) field system can be solved as an \(rD\)-dimensional rational system; reduction modulo \(p\) and determinant bounds control entry and solution bits. This supplies Hessian dependence coefficients and affine charts. It does not assume an algebraic MILP solver.

## Reconstructed nonconvex algebraic radius and boxed gap

The appendix needs a scalar lemma over \(K\) for weak quadratic systems whose Hessians span \(h\), without requiring positive semidefiniteness. It supplies a small feasible point and, on a supplied rational box, an annihilator for the attained minimum of an arbitrary quadratic objective. The objective Hessian is excluded from the constraint span.

Choose a Hessian basis \(B_1,\ldots,B_h\). Introduce \(y_j=x^{\mathsf T}B_jx/2\) and retain every original row in a lifted polyhedron \(\mathcal P\). The only nonlinear equations are
\[
 F_j(x,y)=x^{\mathsf T}B_jx/2-y_j=0,\qquad j\le h.
\]
This lift has polynomial input size over \(K\).

The quantitative genericity lemma in the nonconvex source can be reproduced without changing fields. On a fixed \(d\)-dimensional chart, allow every coefficient of an objective quadratic and \(s\) constraint quadratics to vary independently. The bad loci are:

- a common zero with dependent constraint gradients;
- a KKT solution with singular multiplier Hessian;
- a KKT solution with singular bordered matrix;
- a common zero of more than \(d\) active quadratics.

For the first locus, values and gradients are independently adjustable at fixed \(u\); the incidence dimension is at most one less than the coefficient-space dimension. For the KKT loci, solve value equations for the constraint constants and stationarity equations for objective linear coefficients. This incidence is an affine space. The example \(f_i=u_i^2-1\) and \(r=\sum_j u_j^2+\sum_{i\le s}u_i\) has both nonsingular matrices at \(u_i=\pm1\), \(u_j=0\) for \(j>s\), and \(\lambda_i=-1-1/(2u_i)\). Thus each determinant is nonzero on the incidence, and its zero locus has dimension at most one less. If \(s>d\), the value incidence alone has smaller dimension than coefficient space.

Cumulative affine Bézout degree, projection, and a containing-hypersurface bound give a bad polynomial of degree \(2^{\operatorname{poly}(L)}\). Dependence-vector normalization avoids an exponential list of gradient minors. This is the geometric external contract that must be precisely sourced or proved in the manuscript.

Use integer quadratic perturbations \(P_0,\ldots,P_h\) and bands
\[
 |F_j+\varepsilon^2P_j|\le\varepsilon.
\]
On each chart, restriction of arbitrary ambient quadratics is onto the chart quadratics. Substitution in every bad polynomial and extraction of one nonzero \(\varepsilon\)-coefficient produces a nonzero polynomial in the perturbation coefficients. There are at most exponentially many charts and supports, each of bounded degree. Their product still has single-exponential degree. A nonzero polynomial of degree \(M\) cannot vanish on the whole grid \(\{0,\ldots,M\}^r\). Therefore one perturbation with polynomial-bit integer coefficients is good on all relevant charts for all sufficiently small positive \(\varepsilon\). The argument is existential; the algorithm never builds this product or grid.

For a small feasible point, minimize \(\|(x,y)\|^2+\varepsilon P_0\) on the bands and the unchanged polyhedron. Any original feasible lift stays feasible eventually. Uniform coercivity and comparison with that point give a bounded minimizing sequence. A cluster point is exactly feasible.

For a boxed quadratic minimum, add rational bounds for the lifted \(y\)'s and minimize the original objective plus \(\varepsilon P_0\) on this compact polyhedron and the bands. Uniform convergence and comparison with an original optimizer show that every selected cluster point is an original optimizer.

At selected perturbed minimizers, make all active affine rows equations and choose one chart and one oriented band support along a subsequence. There is at most one active orientation per band, so \(s\le h\). Genericity gives independent gradients, invertible \(M\), and an invertible bordered KKT matrix. All three facts matter: independent gradients and invertibility of an indefinite \(M\) alone would not imply multiplier regularity.

Stationarity gives \(u=\rho/\det M\). After substituting into active equations and multiplying by \((\det M)^2\), the reduced multiplier system has \(s\le h\) variables, degree \(a_0=L^{O(1)}\), and a nonsingular selected root. Its Jacobian is
\[
 -(\det M)^2GM^{-1}G^{\mathsf T},
\]
which is nonsingular by the bordered-matrix Schur complement. Coordinates and the objective are rational outputs with a nonzero denominator along one common sequence.

Explicit input field elements have polynomial Weil height. Determinant and adjugate bounds at each place give a polynomial joint logarithmic norm \(E\) for all parameterized coefficients: use coefficient sums at archimedean places and coefficient maxima at finite places. The estimate is taken before expanding determinant monomials and includes the formal parameter coefficients. Only a fixed number of elimination and substitution stages occurs.

Lemma **lem:qc-elimination** then gives a nonzero polynomial over \(K\), with
\[
 \deg P\le\Lambda=(a_0+1)^s,\qquad
 \height_{\rm aff}(\operatorname{coeff}P)
 \le W=\Lambda(a_0(s+1)+1)E+\log(\Lambda!)+\Lambda\log3.
\]
Both bounds are \(L^{O(h+1)}\). For any selected scalar output \(\xi\),
\[
 [\mathbb Q(\xi):\mathbb Q]\le D\Lambda,\qquad
 \height(\xi)\le W+\log2,\qquad
 \log\|p_\xi\|_\infty\le D\Lambda(W+2\log2).
\]
The last inequality follows from the Mahler-measure/minimal-polynomial relation and expansion in the roots. A bare field norm proves algebraicity but does not replace this height accounting.

Cauchy's bound gives a feasible-coordinate radius \(2^{L^{O(h+1)}}\). Removing powers of the variable and applying the reciprocal root bound gives a positive-value gap \(2^{-L^{O(h+1)}}\). Zero is a separate exact alternative. These are existence and encoding bounds for arbitrary weak quadratic systems, not nonconvex polynomial-time decision or optimization algorithms.

## Reconstructed integer witness and exact rational reduction

For unbounded integer variables, construct an exact formula for the real projection \(Y\), then use convexity of the original cone set to obtain a bounded integer witness.

After lifting the continuous Hessian span, the affine polyhedron \(\mathcal P_z\) has coefficients polynomial in \(z\), of degree at most one in row normals and at most two in constants. Include every active affine subset and every pivot minor rank chart, with guards ensuring consistency of all nonpivot equations. The zero-rank and zero-dimensional cases must be included. Under a nonzero pivot guard, affine-chart coordinates are rational functions of \(z\) with polynomial degree and individual coefficient bit length.

The perturbation choice can depend on \(z\). A grid of polynomial-bit integer coefficient vectors works pointwise for every real \(z\), because the bad-polynomial degree bound depends only on dimensions and degrees. Put every grid point in the Boolean disjunction. The formula may be exponentially large; it is never constructed by the algorithm.

For each positive-dimensional chart and band support, solve stationarity by an adjugate, require its denominator nonzero, and express all coordinates by this rational function. Include nonnegative multipliers, feasibility of every affine row, all bands, and a norm bound. Clear chart and stationarity denominators by even powers under their guards.

The exact projection prefix is
\[
 \exists R>0\ \forall\delta>0\
 \exists(\varepsilon,\lambda_1,\ldots,\lambda_h).
\]
Forward validity follows from bounded perturbed minimizers. Reverse validity takes \(\delta=1/j\) and a compact subsequence of the encoded points with this one fixed radius \(R\). The finite perturbation grid has bounded coefficients, so its band errors vanish. The limit satisfies every original row at the same fixed \(z\). Keeping \(R\) outside the universal block is necessary; permitting escaping continuous witnesses would describe a larger set than the projection. All rank charts are necessary at exceptional \(z\).

For algebraic coefficients, first perform field arithmetic modulo \(p\). Replace each coefficient by its polynomial in a new real variable \(v\), and conjoin \(p(v)=0\), \(a<v<b\). Clear only the remaining rational coefficient denominators by positive common denominators. Put \(v\) in the outer existential block with \(R\). This gives quantified block dimensions
\[
 2,\quad1,\quad h+1.
\]
The generator has one quantified coordinate, not \(D\) coordinates. \(D\) enters the polynomial degrees, which remain polynomial in \(L\).

The Khachiyan–Porkolab integer-witness theorem then gives an effective integer bit bound polynomial in \(L\) for fixed integer dimension and \(h\), even though \(Y\) is not necessarily closed. Its bound must be independent of the number of atomic predicates. Only that witness bound is used; its formula-size-dependent algorithm would not suffice. The source exponent is of the form \(L^{C(h+1)(t+1)^4}\), after adding a fixed-zero integer coordinate to reduce feasibility to optimization. No sharp overall exponent is needed.

Print an integer box meeting \(Y\cap\mathbb Z^t\) whenever it is nonempty. This preserves existence, not every unbounded feasible assignment. Uniform substitution of polynomial-bit boxed integer points and the algebraic small-point lemma then give one continuous box meeting every nonempty original fiber in that integer box. No fiber or integer assignment is enumerated.

On these rational boxes define
\[
 \gamma_z=\min_x\max\{0,q_i,-t_i,\ell_j,e_j,-e_j\}.
\]
The list ranges over every scalar row. Compactness makes the minimum attained, and zero is equivalent to exact fiber feasibility. Its epigraph variable adds no Hessian direction. A rational upper bound makes that epigraph compact and nonempty. Applying the boxed-value lemma uniformly yields one effective \(\Delta=2^{-B}\le1\) with \(\gamma_z=0\) or \(\gamma_z\ge\Delta\) for every boxed integer \(z\).

For rational original data and one threshold \(\theta\), include the threshold before deriving radius and gap bounds. Refine its isolator to a rational upper endpoint within \(\Delta/4\). Keep other affine rows and cone signs exact. The rational Lorentz lift with \(\epsilon=\Delta/(12T^2)\) gives squared cone violation at most \(\Delta/4\), where \(T\ge1\) bounds absolute cone right sides. Thus every lifted integer assignment has \(\gamma_z\le\Delta/4<\Delta\), and its original exact fiber is feasible.

For all affine cone data in \(K\), approximate all affine maps uniformly within \(\eta\), with vector errors also within \(\eta\), and use
\[
 \eta=\Delta/(256T),\qquad\epsilon=\Delta/(256T^2).
\]
Here \(T\ge1\) bounds both original cone norms and absolute right sides on the boxes. Use rounded affine inequalities \(\widehat\ell\le\eta\), equalities \(|\widehat e|\le\eta\), and lift \((\widehat u,s)\) with \(s=\widehat t+2\eta\). Every original feasible point lifts because \(\|\widehat u\|\le\|u\|+\eta\le s\), including at the apex.

Conversely, the rational lift has \(s\ge0\) and \(\|\widehat u\|\le(1+\epsilon)s\). Original affine residuals are at most \(2\eta\), and \(-t\le3\eta\). Since \(|s-t|\le3\eta\),
\[
 q\le3\epsilon(T+3\eta)^2
       +\eta(2T+\eta)+3\eta(2T+3\eta)
 \le48\epsilon T^2+18T\eta
 =66\Delta/256<\Delta/2.
\]
All exact residuals are below the uniform gap, so a lifted integer assignment has an exact feasible original fiber. This estimate needs no sign for the true rounded-back \(t\); its explicit sign residual is essential.

Coefficient approximation is polynomial in the requested number of bits. On the original isolator, for \(g(v)=\sum a_jv^j\) and \(H_0=\max(1,|a|,|b|)\), bound its derivative by \(\sum_{j\ge1}j|a_j|H_0^{j-1}\). This magnitude can be exponential, but its bit length is polynomial. Root refinement to the resulting precision is therefore polynomial. Scalar coefficient error \(\eta/((t+n+1)V(d_*+1))\), where \(V\) bounds box coordinates and \(d_*\) bounds cone-vector lengths, suffices for all stated affine and vector errors.

The final polyhedron has rational coefficients and only the original integer variables. Its lift size and coefficient bits are polynomial for fixed parameters. Rational MILP with fixed integer dimension completes the decision and returns \(z\). Rounded Hessians can have a larger span; no span-dependent theorem is applied to them. The gap belongs to the exact system alone. The polyhedron's displayed continuous coordinates can violate the original cones.

## Canonical field bound and constructive exact witness

Let \(C\) be the original nonempty continuous cone set over \(K\). It is closed and convex, so it has a unique minimum-norm point \(p\). A box merely meeting \(C\) need not contain \(p\); use the following direct argument.

Lift \(p\) uniquely to \(w_*\). Choose an unknown integer box strictly containing \(w_*\), and on it minimize \(\|x\|^2+\varepsilon P_0(w)\) subject to the generic outward bands and all original affine rows. The box is used only for compactness. Every cluster point is exactly feasible and has norm no larger than \(p\)'s. Uniqueness of \(p\) and of its lift forces every cluster point to be \(w_*\). Hence, eventually, every artificial box row is inactive. Choose a fixed active chart from the original polyhedron and a fixed oriented support along a subsequence. The unknown box endpoints occur in none of the final KKT coefficients or height bounds.

Every \(K\)-linear form in \(p\) is an output along this same sequence, with relative degree at most \(\Lambda=L^{O(h+1)}\). First obtain coordinate algebraicity; then apply the primitive-element theorem to \(K(p)/K\). A linear combination generating the extension has the same scalar degree bound, so
\[
 [K(p):K]\le\Lambda,\qquad
 [\mathbb Q(\alpha,p):\mathbb Q]\le D\Lambda.
\]
Do not multiply coordinate degrees and do not choose different limiting points for different outputs. The scalar height proof above gives absolute coordinate minimal-polynomial coefficient bits \(L^{O(h+1)}\).

The existential size bound for a primitive element uses bounded integer combinations of the generating tuple \((\alpha,p)\): the at most \(J(J-1)/2\) pairs of embeddings each exclude one hyperplane, with \(J=D\Lambda\). This gives short coefficients, not a polynomial algorithm for exhaustively searching an \((n+1)\)-dimensional grid. Trace pairing after scaling generators and coordinates to algebraic integers gives short rational power-basis coordinate maps. Discriminant separation gives a short isolator. Thus total output length is \(L^{O(h+1)}\).

The algorithm prints a Cauchy-bound box containing \(p\) itself. For a rational scalar \(r\ge0\), use
\[
 \|x\|^2\le r\quad\Longleftrightarrow\quad
 \|(2x,r-1)\|\le r+1.
\]
Its squared Hessian is \(8I\); each feasibility query has span at most \(h+1\) and uses the original input field only.

For requested error \(\tau=2^{-q}\), bisect the squared-norm value to a feasible rational upper threshold \(u\le\|p\|^2+\tau^2/16\). The projection inequality gives \(\|x-p\|\le\tau/4\) for every feasible point of this slice. Bisect closed coordinate intervals while preserving a nonempty slice, until their widths are at most \(\tau\). The box midpoint is within \(3\tau/4\) of \(p\) in each coordinate. It need not be feasible. Restart from the original canonical-point box for each accuracy request; a previously retained narrow box can exclude \(p\).

Approximate \(\alpha\) from its input isolator and apply **thm:qc-recovery** to \((\alpha,p)\). Its moment-curve family of integer combinations has polynomially many candidates. KLL recognition recovers their minimal polynomials; maximum degree identifies a primitive generator. Coordinate recovery interpolates norm polynomials, not bare minimal polynomials: a sample of degree \(e<J_*\) must be raised to the exponent \(J_*/e\), where \(J_*\) is the actual joint degree. The derivative of the interpolated norm polynomial and an inverse modulo the generator polynomial give all coordinate maps.

Return one irreducible primitive polynomial \(P\), one selected root \(\beta\), and maps \(b_0,b_j\) with
\[
 \alpha=b_0(\beta),\quad p_j=b_j(\beta),\quad
 \mathbb Q(\beta)=K(p).
\]
Verification must check both \(p_{\rm input}(b_0(\beta))=0\) and the input isolator inequalities. Then map every input coefficient through \(b_0\), reduce modulo \(P\), and check every affine row, squared residual, and cone sign exactly. This certifies feasibility and the embedding, not independently the minimum-norm property.

All recognition degree, height and precision bounds are \(L^{O(h+1)}\). Feeding printed radius and precision bits into later feasibility calls can increase the exponent, so claim only \(L^{C_h}\) recovery time. The field degree varies with the input and is never treated as fixed.

A witness can lie in a proper input-field extension. With \(K=\mathbb Q(\sqrt2)\), \(y=\sqrt2\), and
\[
 \|(\sqrt2,1)\|\le x,\qquad \|(x,\sqrt2x)\|\le3,
\]
the unique point has \(x=\sqrt3\) and \(h=1\). The required absolute field is \(\mathbb Q(\sqrt2,\sqrt3)\), of degree four, rather than the quadratic input field or \(\mathbb Q(x)\) alone.

For MISOCP, substitute the returned polynomial-bit integer vector in the original exact system and apply this continuous algorithm. The field and continuous Hessians remain unchanged. Overall time and output length are polynomial for fixed \(t,h\), without the sharper continuous \(L^{O(h+1)}\) exponent in the original mixed-integer input.

## Attainment, strict denominator, and complexity boundaries

For a known finite infimum \(\theta\) of a rational affine objective, existence of a feasible point with \(f\le\theta\) is exactly attainment. The threshold theorem decides it in polynomial time in the original data plus the supplied exact value, for fixed \(t,h\). If feasible, exact witness recovery on the augmented field system gives an optimizer. Alternatively, for rational original data, one can recover the optimizer on the returned rational original fiber by a separately established rational continuous optimization algorithm. Neither route supplies the previously unknown value or a uniform bound for its encoding.

For rational original cone data and a known attained optimum \(\theta\) of a rational affine-fractional objective, impose \(f-\theta d=0\) over \(\mathbb Q(\theta)\). Encode the strict affine domain condition \(d>0\) by a continuous \(s\) and
\[
 \|(2,d-s)\|\le d+s.
\]
This means \(ds\ge1\) and \(d+s\ge0\), which force \(d,s>0\). Conversely \(d>0\) permits \(s=1/d\). The squared residual is \(4-4ds\), giving at most one added Hessian direction. The augmented set is closed; recover a witness and discard \(s\). This special encoding of affine positivity does not justify a theorem for arbitrary strict cone constraints.

Keep these classifications separate:

- Fixed \(h\), no integer variables: common-field cone feasibility is in P, and canonical-point recovery has ordinary polynomial bit cost and polynomial expanded algebraic output.
- Fixed \(t,h\), no supplied integer box: common-field MISOCP decision and full witness recovery are polynomial for those fixed parameters.
- Fixed \(h\), arbitrary integer dimension with supplied finite polynomial-bit bounds: the bounded model has polynomial-size exact algebraic feasibility certificates and a polynomial-size rational MILP reduction. Membership in NP follows, not deterministic polynomial time.
- Arbitrary unbounded integer dimension: the present integer-witness bound is not polynomial in \(L\) uniformly in that dimension. No NP or FP claim follows from this proof.
- Nonconvex quadratic systems of fixed span: the radius and boxed-value lemmas give short encodings only. Feasibility is already NP-hard at span one. Convexity of the actual cone formulation is essential to the polynomial decision reduction.

The common-field restriction is sufficient for this argument, not proved necessary for every possible algebraic-input algorithm. Separate coefficient encodings can have an exponentially large compositum, so they are outside the stated polynomial bound. Do not confuse ordinary exact sign tests at an explicitly isolated algebraic root with PosSLP comparisons for compressed circuits.

## External contracts requested through root

The existing literature report available during this audit did not yet contain all cone-specific contracts. I asked root to have the reusable Luna literature agent supply or confirm these contracts; I did not browse or ingest literature.

1. **Khachiyan–Porkolab, Theorem 1.1:** convex first-order sets described by arbitrary Boolean formulas, potentially nonclosed and lower-dimensional; integer-point bit bound independent of atom count and dependent on atomic degree, coefficient bits, free dimension and quantified block dimensions; feasibility reduced to optimization with a fixed-zero extra coordinate.
2. **Lenstra, Section 5:** rational mixed-integer linear feasibility in polynomial time at fixed integer dimension with a growing number of continuous variables; an integer assignment can be returned.
3. **Kocuk rational Lorentz lift:** constructible using rational/integer arithmetic, polynomial size and coefficient bits in cone dimension and \(\log(1/\epsilon)\), with exact inner inclusion and outer inclusion \(\|u\|\le(1+\epsilon)s\), \(s\ge0\), including the apex. A polynomial bound suffices; no sharper size asymptotic should be claimed without its verified contract.
4. **Geometric elimination degree:** cumulative degree of all affine incidence components, Bézout, nonincrease under linear projection, and a proper component's containing hypersurface of bounded degree. The source notes identify Krick–Pardo–Sombra Section 1.2.1 and Heintz via a later primary proof. The appendix must provide a precise imported version or enough elementary derivation.
5. **KLL recognition and standard univariate arithmetic:** use the verified contract already required by Appendix J. Real-root isolation, irreducibility checking when validation is claimed, and exact sign determination have polynomial bit cost in dense degree, coefficient bits and requested precision. Input-field validity may instead be part of the explicitly stated representation promise.

One optional-corollary scope repair is needed. In Section 6 of the witness source, rational \(f,d\) and an algebraic value \(\theta\) alone do not put unrelated original cone coefficients from \(K\) in \(\mathbb Q(\theta)\). The simplest manuscript correction is the rational-original-data restriction stated above. Another valid version assumes \(\theta\) already represented in the original \(K\). A version allowing separately encoded \(\theta\) and original \(K\) must construct and select the common field \(K(\theta)\), for example by applying **thm:qc-recovery** to \((\alpha,\theta)\) with joint-degree bound \(D\deg\theta\) and a certified approximation oracle for those two isolated input numbers. That is a polynomial-size compositum for two explicit fields, but the manuscript must include its construction if it uses that version. This ambiguity does not affect the main common-field threshold or witness theorems.

The remaining required writing repair is to expose the proof chain above, state the exact output and complexity contracts, and avoid borrowing native-PSD theorems for indefinite cone squares.

## Checks actually performed

Read-only targeted source inspection used rg for relevant file and label discovery, and cat/sed for the assigned source and manuscript proofs. No test suite, computation experiment, CAS, mathematical script, project-wide verification, or CI check was run.

Commands actually run for this new evidence file:

    git diff --check -- paper-exact-arithmetic/evidence/reviews/prewrite-algebraic-cones.md
    git status --short -- paper-exact-arithmetic/evidence/reviews/prewrite-algebraic-cones.md
    rg -n '[[:blank:]]+$' paper-exact-arithmetic/evidence/reviews/prewrite-algebraic-cones.md

The diff check reported no errors, but the scoped status showed that the file was untracked, so the diff check supplies no saved-file assurance. The direct rg check returned no trailing-whitespace matches (exit status 1). These are document checks, not mathematical verification or CI results.
