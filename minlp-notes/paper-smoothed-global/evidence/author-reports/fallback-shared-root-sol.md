# Shared-root conversion for the general exact fallback

Date: 2026-10-05. Author: Sol. Scope: reconcile the separate scalar root representations in the current counting fallback with the shared-root algebraic output contract in the model section. No TeX, historical note, literature record, or optimization experiment was changed.

**Conclusion.** The proposed conversion is valid. It has deterministic work polynomial in the product of the scalar defining-polynomial degrees and their coefficient bit lengths. For the canonical two-block fallback, the degrees have a base-only bound, so the product is still \(2^{\operatorname{poly}_d(I)}\). The conversion therefore preserves a bound

\[
B'(I+b+q+1)^{e_d},
\qquad B'=2^{\operatorname{poly}_d(I)},
\]

where \(B'\) is computed before sampling and neither \(B'\) nor the fixed exponent \(e_d\) depends on added noise bits \(b\) or requested precision \(q\). It returns one isolated real root and rational polynomial maps for every continuous coordinate and the optimal value. Native integer coordinates may be listed explicitly.

The conversion does not justify constant-base exponential work for the small-core component solver. Taking a Cartesian product of \(k\) separate degree-\(c_d^k\) representations can cost \(c_d^{k^2}\). The joint critical-limit construction is still needed for that sharper contract. Nor should this generic exponential conversion be applied to all independent component values to claim expected polynomial global algebraic-sum comparisons.

**Lemma: shared-root representation of a specified real tuple.**

Let \(m\ge1\). For each \(i\in[m]\), let \(p_i\in\mathbb Z[T]\) be a nonzero polynomial of positive degree \(\delta_i\), and let \(J_i\) be a rational closed interval, possibly a point, containing a specified real root \(a_i\) of \(p_i\) and no other distinct real root. Let \(H\ge1\) bound the coefficient and endpoint bit lengths. Put

\[
D=\prod_{i=1}^m\delta_i.
\]

There is a deterministic algorithm with the following properties.

1. It returns a nonzero squarefree integer polynomial \(P\), a rational interval isolating one real root \(\theta\) of \(P\), and rational polynomials \(r_i\) of degree less than \(\deg P\), such that \(a_i=r_i(\theta)\) for every \(i\).
2. It has \(\deg P\le D\). All output coefficient and isolating-endpoint bit lengths, and the construction work, are bounded by a polynomial in \(D,m,H+1\) with absolute exponents.
3. For any \(q\ge0\), the stored representation gives rational enclosures of each \(a_i\) of width at most \(2^{-q}\) in work polynomial in \(D,m,H+q+1\), again with absolute exponents. The root \(\theta\) itself can also be refined to \(q\) bits within this bound.
4. Exact signs of explicitly given rational polynomials in the tuple can be decided by univariate algebraic sign determination after substitution. If such a polynomial has fixed degree, an explicit monomial list, and coefficient length \(L\), this costs \(\operatorname{poly}_d(D,m,H+L+1)\).

The lemma asserts a representation of the tuple specified by the scalar isolators. It does not assert that an arbitrary independently specified tuple is feasible or optimal for an optimization problem. That property must already be known. In the intended application, all scalar formulas use the same lexicographically least optimizer, and the value formula gives its objective value.

**Proof: a reduced tensor algebra.**

First replace each \(p_i\) by its primitive squarefree part and choose positive leading coefficient. This preserves all distinct roots and the chosen real root. Rational polynomial gcd and exact division perform this step with work and coefficient heights polynomial in the original degrees and heights. Degrees cannot increase. Write \(d_i\le\delta_i\) for the new degrees and

\[
N=\prod_i d_i\le D.
\]

Work in the rational algebra

\[
\mathcal A=\mathbb Q[X_1,\ldots,X_m]/
               (p_1(X_1),\ldots,p_m(X_m)).
\]

Each polynomial may be divided by its leading coefficient to make it monic over \(\mathbb Q\). A basis is

\[
\left\{X_1^{e_1}\cdots X_m^{e_m}:0\le e_i<d_i\right\},
\]

so \(\dim_{\mathbb Q}\mathcal A=N\). Multiplication by \(X_i\) is the tensor product of its univariate companion matrix with identity matrices for the other factors; call the resulting \(N\times N\) rational matrix \(M_i\).

Over \(\mathbb C\), each squarefree univariate factor has distinct roots. Evaluation gives an isomorphism

\[
\mathcal A\otimes_{\mathbb Q}\mathbb C
\cong
\prod_{\zeta\in\mathcal T}\mathbb C,
\qquad
\mathcal T=\prod_i Z_{\mathbb C}(p_i).
\]

Thus \(\mathcal T\) contains exactly \(N\) distinct complex tuples, all \(M_i\) are simultaneously diagonalizable, and their joint eigenvalues are those tuples. This argument uses squarefree preprocessing: without it, multiplicities could make every characteristic polynomial repeated even when its geometric projections separate.

**Proof: find a separating rational linear form.**

For an integer \(t\ge0\), use

\[
\lambda(t)=(1,t,\ldots,t^{m-1}),
\qquad
L_t(X)=\sum_i\lambda_i(t)X_i,
\]

with \(t^0=1\), including at \(t=0\). For two distinct tuples \(\zeta,\eta\in\mathcal T\), equality of their projections is the equation

\[
\sum_{i=1}^m(\zeta_i-\eta_i)t^{i-1}=0.
\]

This is a nonzero complex polynomial in \(t\) of degree at most \(m-1\), because the tuples differ. It excludes at most \(m-1\) integers. There are \(\binom N2\) pairs. Consequently the list

\[
t=0,\ldots,(m-1)\binom N2
\]

contains a form separating every complex tuple in \(\mathcal T\). This includes \(m=1\) and \(N=1\), where the list has one member.

For each listed \(t\), form

\[
M_\lambda=\sum_i\lambda_iM_i,
\qquad
\chi_\lambda(T)=\det(TI-M_\lambda).
\]

Simultaneous diagonalization gives

\[
\chi_\lambda(T)=
\prod_{\zeta\in\mathcal T}
       \bigl(T-\lambda^{\mathsf T}\zeta\bigr).
\]

This monic rational polynomial has degree \(N\). Therefore
\(\gcd(\chi_\lambda,\chi_\lambda')=1\) if and only if the form separates all complex tuples. Computing this gcd gives an exact acceptance test. Select the first accepting form in the displayed order.

No optimizer-root pairing problem is solved here: the search separates the entire Cartesian root set, including tuples that have no optimization meaning. It will later use the given scalar isolators to select the one designated tuple.

**Proof: recover coordinates from one scalar root.**

For the selected form, compute its independent coefficient-direction derivatives

\[
q_i(T)=
-\left.\frac{\partial}{\partial u}
\det(TI-M_\lambda-uM_i)\right|_{u=0}.
\]

The independence of the direction variable \(u\) is essential. A derivative only with respect to the moment parameter \(t\) would recover one weighted coordinate combination and would not give all coordinates.

The product formula implies

\[
q_i(T)=
\sum_{\zeta\in\mathcal T}
\zeta_i
\prod_{\eta\ne\zeta}
      \bigl(T-\lambda^{\mathsf T}\eta\bigr).
\]

At the simple root \(\alpha_\zeta=\lambda^{\mathsf T}\zeta\),

\[
q_i(\alpha_\zeta)=
\zeta_i\chi_\lambda'(\alpha_\zeta).
\]

Since the derivative is invertible modulo \(\chi_\lambda\), set

\[
r_i=q_i(\chi_\lambda')^{-1}\pmod{\chi_\lambda}.
\]

Take the polynomial representative of degree less than \(N\). Then
\(r_i(\alpha_\zeta)=\zeta_i\) for every complex tuple. In particular, for

\[
\theta=\sum_i\lambda_i a_i
\]

all desired equalities \(a_i=r_i(\theta)\) hold. Clearing one positive integer coefficient denominator in \(\chi_\lambda\), and removing its content, gives the required squarefree integer \(P\). Scalar multiplication does not change its roots or the coordinate identities.

These identities imply
\(\mathbb Q(a_1,\ldots,a_m)=\mathbb Q(\theta)\), although \(P\) itself need not be irreducible or minimal. It is enough that it isolates the selected root. No factorization into irreducible minimal polynomials is needed.

**Proof: select the designated real root.**

The selected linear form is real. If a nonreal tuple had a real projected value, its distinct conjugate tuple would have the same value, contradicting separation. Hence every real root of \(\chi_\lambda\) corresponds to an all-real Cartesian tuple.

The target tuple is selected by the original scalar isolators. Refine each \(J_i\) by its univariate root representation, preserving the enclosed chosen root. Rational interval summation gives

\[
J_\theta=\sum_i\lambda_iJ_i,
\]

where a negative coefficient would reverse endpoints; the moment forms actually have nonnegative coefficients. This interval contains \(\theta\). If every source interval has width at most \(\varepsilon\), then

\[
\operatorname{width}(J_\theta)
\le\Lambda\varepsilon,
\qquad
\Lambda=\sum_i|\lambda_i|.
\]

Here \(\Lambda\ge1\). Let \(2^{-S}\) be any effective strict lower bound on the distance between distinct roots of the squarefree integer \(P\). Standard integer-polynomial root-separation bounds allow \(S\) polynomial in its degree and coefficient bit length. Refine each source interval to width at most
\(2^{-S-2}/\Lambda\). The resulting \(J_\theta\) has width at most \(2^{-S-2}\), contains the target, and contains no other distinct real root of \(P\). Endpoint root tests and closed-interval Sturm counting verify that its real-root count is exactly one. Rational point intervals are allowed. Alternatively, choose rational endpoints just outside this interval and retain the same separation slack.

This is a quantitatively bounded selection step, not an indefinite refinement loop waiting to distinguish a tie. Separation was already tested in the complex Cartesian root set, and a root-separation bound prescribes sufficient precision. The tuple could be chosen canonically upstream even if the optimization problem has ties or a continuum of minimizers.

**Proof: degrees, coefficient heights, and deterministic work.**

After squarefree preprocessing, the companion entries have heights polynomial in \(D,H\). One common denominator for all entries is the product of the positive leading coefficients of the squarefree \(p_i\). Its bit length is at most \(m\) times the maximum leading-coefficient bit length. Tensoring copies entries but introduces no new field extensions or denominators.

There are at most \(1+(m-1)\binom N2=O(mN^2+1)\) forms. Every tested \(t\) has \(O(\log(m+1)+\log(N+1))\) bits. Each \(\lambda_i=t^{i-1}\) has \(O(m(\log(m+1)+\log(N+1)))\) bits. Matrix entries after summing the forms therefore have polynomial bit length in \(D,m,H\).

For an explicit denominator/height calculation, let \(c>0\) be that common denominator and write \(A_\lambda=cM_\lambda\), \(A_i=cM_i\), with integer entries. The integer polynomial

\[
\widetilde\chi_\lambda(T)
=\det(cTI-A_\lambda)
=c^N\chi_\lambda(T)
\]

has coefficient bit length
\(O(N(H_{\rm mat}+\log(N+1)))\), where \(H_{\rm mat}\) bounds the integer entry and \(c\) bit lengths. The same type of bound holds for

\[
\widetilde q_i(T)
=-[u^1]\det(cTI-A_\lambda-uA_i)
=c^N q_i(T).
\]

Thus \(\widetilde q_i/\widetilde\chi_\lambda'=q_i/\chi_\lambda'\), and the modular construction can use these integer polynomials directly. Bivariate tensor interpolation on \(0,\ldots,N\) in \(T,u\) computes the determinant and its coefficient of \(u\) with polynomially many exact \(N\times N\) determinant calculations. Interpolation uses only two variables. Sample values, interpolation denominators, and intermediate rational heights are polynomial in \(D,m,H\).

Univariate gcds, exact divisions, modular inverses, root isolation, endpoint signs, and root refinement have polynomial degree/height/precision bit bounds with absolute exponents. Subresultant or Sylvester-minor bounds control the coefficient lengths of the modular inverse and all \(r_i\). These lengths are polynomial in \(D,m,H\). Multiplying the numbers of forms, directions, matrix entries, interpolation nodes, and algebraic operations preserves a polynomial in those variables.

The separation exponent \(S\), the source-interval precision needed to identify \(\theta\), and the resulting rational endpoint lengths are also polynomial in \(D,m,H\). For example, the coarser choice
\(S=C N^2(H_P+\log(N+1)+1)\), with a fixed sufficiently large effective integer \(C\), safely dominates usual squarefree integer root-separation estimates; \(H_P\) is the bit length of the coefficients of \(P\). Hence construction has the claimed polynomial work bound.

For later evaluation, a Cauchy root bound gives
\(|\theta|\le 2^{H_P+1}\). On a rational interval containing the relevant root, elementary coefficient bounds give a rational bound \(K_i\ge1\) on \(|r_i'|\). The bit lengths of \(K_i\) are polynomial in \(D,m,H\): there are fewer than \(N\) powers, and their exponents contribute at most \(N\) times the root-bound bit length. Refining \(\theta\) to

\[
q+\left\lceil\log_2\max_i K_i\right\rceil+O(1)
\]

bits and applying exact rational interval polynomial evaluation gives all requested coordinate enclosures. This yields work polynomial in \(D,m,H+q+1\). An extra \(O(\log m)\) precision allowance gives a Euclidean tuple error at most \(2^{-q}\) if desired.

Finally, exact polynomial identities or signs at the chosen tuple reduce to signs of univariate rational polynomials at the isolated \(\theta\). For fixed-degree explicitly encoded polynomials, substitute the \(r_i\), clear positive denominators, and reduce modulo \(P\). Degrees, heights, and arithmetic work remain polynomial in \(D,m,H+L\). A gcd detects exact zeros, and Sturm/subresultant sign determination handles nonzero signs. This proves the lemma.

**Application to the canonical two-block fallback.**

Take the tuple consisting of all optimizer coordinates and the optimal value. Integer coordinates can be listed explicitly after extraction; their maps can then be discarded from the submitted output. The coordinate singleton formulas and the value singleton formula refer to the same lexicographically least optimizer, so the upstream proof already fixes one compatible real tuple. Equivalently, extract the integer labels first, substitute them in the objective, and convert only the continuous coordinates and value.

The block-QE format bound, not merely the fallback's total work bound, supplies the needed degree information. For fixed \(d\), there is a base-computable \(A=2^{\operatorname{poly}_d(I)}\) such that every scalar isolating polynomial has degree at most \(A\), independent of added coefficient length \(b\). Its coefficient and isolating-endpoint lengths are at most \(A(I+b+1)^e\), with \(e\) independent of dimension. This includes forming the product of the nonconstant output atoms, squarefree extraction, singleton-root selection, and univariate isolation.

The tuple length is \(m\le\operatorname{poly}(I)\). Therefore a pre-draw bound on the conversion's product degree is

\[
D\le A^m,\qquad
\log D\le m\log A=\operatorname{poly}_d(I).
\]

Substitute these bounds in the lemma's absolute polynomial degree/height work bound. If that bound is \((D+m+1)^C(H+q+1)^C\), enlarging \(C\) once if needed gives

\[
(D+m+1)^C\bigl(A(I+b+1)^e+q+1\bigr)^C
\le
B'(I+b+q+1)^{e_d},
\]

where \(B'\) absorbs only base quantities such as \(A^{mC}\), \(A^C\), the original QE budget, and polynomial functions of \(I\). Its logarithm is polynomial in \(I\), and its binary encoding is computable from the same pre-draw format bounds. No factor \(b^m\) or \(q^m\) occurs. In particular, neither the degree product nor the exponential multiplier is recomputed from the added bit length.

The degree bound is essential. Knowing only that each polynomial's *total encoded length* is at most \(B(I+b)^e\) would allow degrees depending on \(b\), and multiplying them could create an exponent of \(b\) depending on \(m\). The coefficient-height-independent format-degree estimate rules out that mistake.

Including the value as an additional scalar factor gives a map \(r_f(\theta)\). It equals \(F_\gamma(x^{\rm lex})\) because the selected tuple is the one fixed by the canonical formulas. The characteristic polynomial also represents many other tuples, and the congruence

\[
F_\gamma(r_1(T),\ldots,r_n(T))-r_f(T)
\equiv0\pmod P
\]

need not hold globally: extraneous Cartesian tuples may pair optimizer-coordinate roots with unrelated value roots. What is true, and can be verified within the bound, is

\[
F_\gamma(r_1(\theta),\ldots,r_n(\theta))
-r_f(\theta)=0.
\]

Use exact sign determination at the selected root, not an identity over every root of \(P\). The same procedure can verify original semialgebraic atom signs, coordinate membership in the scalar isolators, and native integer labels. These checks preserve the chosen point and value; they do not replace the canonical global-optimality proof.

For a native integer coordinate, refine its known scalar root to an interval of width less than \(1/2\) and extract the unique possible integer, or use the integer singleton/interval check directly. The domain premise guarantees that such an integer exists. Listing that exact label is within the same bound. For a mixed box, the existing fallback's rational feasible-point construction remains valid: retain these labels and clip continuous approximations to their original bounds, then use an objective derivative bound and the value enclosure to certify the requested gap. No analogous arbitrary-domain rational feasibility claim follows just from this conversion.

**Suggested integration.**

In theorem thm:count:fallback(i), strengthen the output wording to one shared-root algebraic representation for the lexicographically least minimizer and the optimal value; separate scalar root representations may be retained as auxiliary outputs. Leave the lexicographic selector and every-draw correctness intact.

After the existing scalar-QE/root-isolation proof, append the lemma above or its proof as a conversion step. Enlarge the pre-draw factor \(B\) to cover \(A^{O(m)}\) and the absolute polynomial conversion work before choosing rare-event thresholds. Retain a fixed exponent for \(I+b+q\). Replace the statement that no common primitive element is required with the accurate distinction that no *minimal defining polynomial* is required, while the displayed conversion supplies one shared root for the output model.

For theorem (ii), state that refinement of the shared root and its maps gives the coordinate and value enclosures; the scalar representations may alternatively be used. The output length is bounded by \(B\operatorname{poly}_d(I+b)\), not by a base-only \(B\) independent of coefficient length. The base-only factor is what rare-fallback accounting cancels.

**Verification record.** This is an analytical proof and bit-budget development. I read the current model/output definition, fallback theorem, and the saved scalar-QE height/degree derivation. No experiment or literature search was run. The targeted command python3 - <<'PY' read only this report and checked trailing whitespace, paired math delimiters and fences, and absence of escaped control characters. It passed 156 inline math pairs and 25 display pairs. The TeX files were not edited.
