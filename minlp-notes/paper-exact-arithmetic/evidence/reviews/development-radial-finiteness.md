# Rational radial finiteness: complete sphere-ring deduction

Date: 2026-10-05. This proof is ready for the certificate section or its appendix. It restores the qualitative finiteness theorem needed to define the least rational radial order. It uses the general-ring contracts of Burgdorf, Scheiderer, and Schweighofer (2012) verified by the manuscript's Luna source review. It does not use their real-coefficient geometric Theorem 7.11 as a rational descent theorem.

I read the [saved sphere corollary](../../../research-20260927/rational-denominator-certificate-frontier.md), the [prewriting audit](prewrite-sos-fields.md), and the [vetted source summary](../../../literature/papers/burgdorf2012-pure-states-nonnegative-polynomials-and/paper.md). The root supplied Luna's exact normalization refinement for Corollary 4.12. I performed analytic derivations only. No browsing, source-verification research, mathematical scripts, experiments, project-wide checks, or CI inspection was performed.

## The theorem to restore

**Theorem (rational radial finiteness).** Let \(P\in\mathbb Q[X_1,\ldots,X_n]\) be nonnegative on \(\mathbb R^n\), of even degree \(2d\). Assume its leading homogeneous form is positive definite, its real zero set is finite, and its Hessian is positive definite at every real zero. The empty zero set is allowed. Then there is an integer \(N\ge0\) such that
\[
 (1+\|X\|^2)^N P\in\Sigma\mathbb Q[X]^2.
 \tag{1}
\]
The conclusion also holds for every integer exponent larger than \(N\). In particular \(P\) has an SOS of rational functions with a common polynomial denominator that is nonzero everywhere on \(\mathbb R^n\).

Positive constants are immediate rational sums of squares, so below \(n\ge1\) and \(d\ge1\). The theorem is an existence statement. It supplies neither a uniform exponent in dimension and degree nor an effective bit bound for the certificate.

## Exact imported contracts

For this proof a cone in an additive group is closed under addition and contains zero. A state on a group/cone/order-unit triple \((G,C,u)\) is an additive map \(\psi:G\to\mathbb R\), nonnegative on \(C\), with \(\psi(u)=1\). A pure state is an extreme point of the convex set of normalized states. An order unit means that for every \(g\in G\), some positive integer \(r\) has \(ru+g,ru-g\in C\).

The following are the exact prior-theory interfaces used. Their general-ring scope includes commutative rings containing \(\mathbb Q\).

1. **BSS Theorem 2.5.** If \(u\) is an order unit of \((G,C)\), and every pure state normalized at \(u\) is strictly positive on \(g\in G\), then \(rg\in C\) for some positive integer \(r\). The conclusion is an integer multiple, not directly \(g\in C\).
2. **BSS Corollary 4.12, in the ideal setting used here.** Let \(A\) be a commutative ring, \(S\subseteq A\) an archimedean semiring or a preordering, \(I\) an ideal, and \(C\subseteq I\) an \(S\)-pseudomodule with order unit \(u\). An \(S\)-pseudomodule is an additive cone stable under multiplication by elements of \(S\). Every pure state \(\psi\) of \((I,C,u)\) has one of the following forms:
   - If \(\psi(u^2)\ne0\), there is a unital ring homomorphism \(\lambda:A\to\mathbb R\), nonnegative on \(S\), with \(\lambda(u)\ne0\), and \(\psi(h)=\lambda(h)/\lambda(u)\) for \(h\in I\).
   - If \(\psi(u^2)=0\), there is a unital ring homomorphism \(\lambda:A\to\mathbb R\), nonnegative on \(S+I\), with \(\lambda(I)=0\), and \(\psi(ah)=\lambda(a)\psi(h)\) for \(a\in A,h\in I\).
   In the second case, nonnegativity on \(S+I\) entails annihilation of the additive ideal \(I\), since \(I\) contains both signs. The split concerns \(\psi(u^2)\), not \(\psi(u)\), which is always one.
3. **BSS Proposition 5.3(a) and Remark 5.5(1).** For an archimedean quadratic module \(M\) in a ring containing \(1/2\), a finitely generated ideal \(J=(b_1,\ldots,b_s)\) has \(u=\sum_i b_i^2\) as an order unit on \((J^2,M\cap J^2)\). An elementary proof for the present SOS cone is supplied below as well.
4. **BSS Theorem 6.2.** Strict positivity at all real ring homomorphisms nonnegative on an archimedean quadratic module gives \(rH\in M\) for some positive integer \(r\). Rational SOS rescaling gives \(H\in M\) in the setting below.

The distinction between \(\psi\) and \(\lambda\) is maintained throughout. No field-valued PSD factorization, boundary-Gram rounding, or totally real residue-field assumption enters the proof.

## The rational sphere ring is archimedean

Homogenize \(P\) to the rational form
\[
 H(Y_0,\ldots,Y_n)=Y_0^{2d}P(Y_1/Y_0,\ldots,Y_n/Y_0)
\]
of degree \(2d\), and put
\[
 q(Y)=\sum_{i=0}^nY_i^2,\qquad
 A=\mathbb Q[Y_0,\ldots,Y_n]/(q-1),\qquad M=\Sigma A^2.
 \tag{2}
\]
We use the same symbol \(H\) for its class in \(A\). The cone \(M\) is a preordering: sums and products of sums of squares are sums of squares. Every nonnegative rational is a sum of rational squares. For example \(1/r\) is the sum of \(r\) copies of \((1/r)^2\); binary square splitting gives a shorter version when needed. Thus \(M\) is closed under nonnegative rational scaling.

For each coordinate, \(1-Y_i^2=\sum_{j\ne i}Y_j^2\in M\). To verify archimedeanity on all of \(A\), let
\[
 \mathcal B=\{a\in A:\text{some positive integer }R\text{ has }R-a^2\in M\}.
\]
It contains the coordinates and all rational constants. If \(R-a^2,T-b^2\in M\), then
\[
 2R+2T-(a+b)^2
 =2(R-a^2)+2(T-b^2)+(a-b)^2\in M,
\]
and
\[
 RT-a^2b^2=T(R-a^2)+a^2(T-b^2)\in M.
\]
It is also closed under negation. Hence every polynomial class belongs to \(\mathcal B\). For such a class \(a\),
\[
 \frac{R+1}{2}\pm a
 =\frac12\bigl((a\pm1)^2+(R-a^2)\bigr)\in M.
\]
Increasing the rational constant to an integer gives the usual bounds \(R'\pm a\in M\). This proves that \(M\) is archimedean and that \(1\) is an order unit on \((A,M)\).

Every unital real ring homomorphism from \(A\) is evaluation at a point of the real unit sphere; conversely every sphere point gives such a homomorphism and is nonnegative on \(M\). On the equator \(Y_0=0\), \(H\) is the positive definite leading form of \(P\), and is strictly positive. At \(Y_0\ne0\),
\[
 H(Y)=Y_0^{2d}P(Y'/Y_0)\ge0.
 \tag{3}
\]
Consequently \(H\) is nonnegative on the sphere, and its zeros are precisely the finite antipodal lifts
\[
 Z=\left\{\pm\frac{(1,p)}{\sqrt{1+\|p\|^2}}:P(p)=0\right\}.
 \tag{4}
\]
If \(Z\) is empty, Theorem 6.2 gives \(rH\in M\); multiplication by the rational SOS \(1/r\) gives \(H\in M\). The remaining argument treats nonempty \(Z\).

## Algebraicity and exact rational double vanishing

Each affine zero \(p\) is stationary because \(P\ge0\), and its Hessian is invertible by assumption. Its coordinates are algebraic over \(\mathbb Q\). Here is a direct proof that avoids a real-coefficient zero-locus argument.

Let \(K=\mathbb Q(p_1,\ldots,p_n)\). If \(K\) had positive transcendence degree, choose a transcendence basis and a derivation of its rational function field that sends one basis element to one and the others to zero. Characteristic zero permits unique extension of this derivation through the finite separable algebraic extension \(K\). Applying it to \(\nabla P(p)=0\) gives
\[
 \nabla^2P(p)\,Dp=0.
\]
The Hessian is invertible over \(K\), so \(Dp=0\). The coordinates generate \(K\), making the derivation zero on \(K\), a contradiction. Thus \(K/\mathbb Q\) is finite. Formula (4) then shows that every sphere zero has algebraic coordinates.

For \(z\in Z\), let \(\mathfrak m_z\) be the kernel of rational evaluation \(A\to\mathbb R\). Its image is the number field \(\mathbb Q(z)\), so \(\mathfrak m_z\) is maximal. Distinct real zeros can give the same rational maximal ideal; keep each distinct ideal only once, and define
\[
 J=\bigcap_{i=1}^t\mathfrak m_i.
 \tag{5}
\]
This is the rational vanishing ideal of \(Z\). Its finite residue fields need not be totally real. Each rational maximal ideal automatically includes the complete algebraic conjugacy orbit, including nonreal conjugates.

At every \(z\in Z\), the ambient gradient of the homogeneous polynomial \(H\) is zero, not merely its tangent gradient. Indeed, differentiating (3) at an affine zero uses \(P(p)=0,\nabla P(p)=0\), and gives all ambient partial derivatives of \(H\) equal to zero.

The following elementary algebraic fact supplies exact rational membership in the squared maximal ideal.

**Double-vanishing lemma.** Let \(z\) be an algebraic point and \(R\in\mathbb Q[Y]\) satisfy \(R(z)=0,\nabla R(z)=0\). If \(\mathfrak n=\ker(\mathbb Q[Y]\to\mathbb Q(z))\), then \(R\in\mathfrak n^2\).

**Proof.** Choose a primitive element \(\theta\) of \(\mathbb Q(z)\) that is a rational linear combination of the coordinates, \(\theta=\sum a_i z_i\). Such a combination exists by the primitive element theorem in characteristic zero. Let \(f\) be its irreducible polynomial, put \(T=\sum a_iY_i\), and choose rational polynomials \(c_i\) with \(z_i=c_i(\theta)\). The ideal \(\mathfrak n\) is generated by \(f(T)\) and \(e_i=Y_i-c_i(T)\): their quotient identifies every coordinate with \(c_i(T)\) and gives exactly \(\mathbb Q[T]/(f)\). The relation \(T-\sum a_ic_i(T)\) is divisible by \(f(T)\), so the identification is consistent.

Taylor expansion in the \(e_i\), modulo their pair-products, gives
\[
 R(Y)\equiv R(c(T))+\sum_i R_{Y_i}(c(T))e_i\pmod{\mathfrak n^2}.
\]
Each derivative coefficient is divisible by \(f(T)\) because it vanishes at \(\theta\). The polynomial \(h(T)=R(c(T))\) satisfies \(h(\theta)=h'(\theta)=0\); since \(f\) is separable, \(f^2\mid h\). Every displayed term is therefore in \(\mathfrak n^2\). \(\square\)

Apply the lemma to \(H\), then pass to the quotient \(A\). It gives \(H\in\mathfrak m_i^2\) for every \(i\), entirely over \(\mathbb Q\). Distinct maximal ideals are comaximal, as are their squares. For example, if \(a+b=1\), with \(a\in\mathfrak m_i,b\in\mathfrak m_j\), expanding \((a+b)^3\) shows \(1\in\mathfrak m_i^2+\mathfrak m_j^2\). Therefore
\[
 H\in\bigcap_i\mathfrak m_i^2
 =\prod_i\mathfrak m_i^2
 =\left(\prod_i\mathfrak m_i\right)^2
 =J^2.
 \tag{6}
\]
This proves the needed global rational membership, without inferring it from a real SOS or from a boundary rounding argument.

The real zero set of \(J\) on the sphere is exactly \(Z\). One inclusion is its definition. Conversely, any real evaluation annihilating \(J\) factors through
\[
 A/J\cong\prod_i A/\mathfrak m_i
\]
and hence through one residue field. Since \(H\in J\), its value there is zero, so the point belongs to \(Z\). This also proves that every real embedding of every residue field gives a zero already included in the argument.

## Order unit on the squared ideal

The ring \(A\) is noetherian, so choose finite generators \(J=(b_1,\ldots,b_s)\), and put
\[
 I=J^2,\qquad C=M\cap I,\qquad u=\sum_i b_i^2.
 \tag{7}
\]
The cone \(C\) is stable under multiplication by \(S=M\); it is the \(S\)-pseudomodule required by Corollary 4.12. Proposition 5.3(a) and Remark 5.5(1) give the stated order unit. In this specific SOS setting it also follows directly.

Every \(h\in J^2\) is a finite sum of terms \(a b_i b_j\). Archimedeanity gives an integer \(R\ge1\) with \(R-a^2\in M\). Then
\[
 R(b_i^2+b_j^2)\pm2a b_ib_j
 =(ab_i\pm b_j)^2+(R-a^2)b_i^2+(R-1)b_j^2\in C.
\]
Every term on the right belongs to \(J^2\) and is SOS. Multiplying by \(1/2\), summing over a representation of \(h\), and filling unused nonnegative multiples of the \(b_i^2\) gives an integer \(B\) with \(Bu\pm h\in C\). Thus \(u\) is an order unit on \((I,C)\).

The zeros of \(u\) are exactly \(Z\): a sum of real squares is zero exactly when all its generators vanish, which is equivalent to annihilating \(J\).

## Pure states off the zeros

Let \(\psi\) be a pure state of \((I,C,u)\). In type I of Corollary 4.12,
\[
 \psi(h)=\lambda(h)/\lambda(u).
\]
Because \(u\) is a sum of squares, \(\lambda(u)\ge0\), and the type-I nonzero condition gives \(\lambda(u)>0\). Its sphere point is therefore outside \(Z\). Since \(H\ge0\) with zero set exactly \(Z\), \(\lambda(H)>0\), and
\[
 \psi(H)>0.
 \tag{8}
\]
This uses positivity of the associated evaluation \(\lambda(u)\), not any proposed dichotomy in \(\psi(u)\).

## Pure states at the zeros

In type II, \(\lambda(I)=0\). Since \(b^2\in I\) for every \(b\in J\), real evaluation gives \(\lambda(b)^2=0\), hence \(\lambda(J)=0\). Its point \(z\) belongs to \(Z\); its kernel is one of the \(\mathfrak m_i\), with residue field \(K\subseteq\mathbb R\). The relation
\[
 \psi(ah)=\lambda(a)\psi(h)
 \tag{9}
\]
annihilates \(\mathfrak m_i I\). It extends \(\psi\) to a real linear functional on
\[
 (I/\mathfrak m_i I)\otimes_{K,\lambda}\mathbb R.
 \tag{10}
\]
There is an exact identification
\[
 (I/\mathfrak m_i I)\otimes_{K,\lambda}\mathbb R
 \cong (\mathfrak m_i^2/\mathfrak m_i^3)\otimes_{K,\lambda}\mathbb R
 \cong\operatorname{Sym}^2(T_z^*S^n).
 \tag{11}
\]
Here are the algebraic details that justify both isomorphisms.

The module \(I/\mathfrak m_i I\) is killed by \(\mathfrak m_i\), so localization at \(\mathfrak m_i\) changes nothing. All other maximal ideals in (5) become units there, hence \(J_{\mathfrak m_i}=(\mathfrak m_i)_{\mathfrak m_i}\). Thus (10) is the degree-two cotangent quotient \(\mathfrak m_i^2/\mathfrak m_i^3\). Localization changes neither of these finite residue-field modules.

Next extend rational coefficients to \(\mathbb R\). Characteristic zero makes \(K/\mathbb Q\) separable, so \(K\otimes_{\mathbb Q}\mathbb R\) is a finite product of copies of \(\mathbb R\) and \(\mathbb C\). Selecting the real factor specified by \(\lambda\), and localizing at its sphere point, sends the extension of \(\mathfrak m_i\) to the ordinary real point ideal. Flat scalar extension and localization preserve its successive-power quotients. This gives the real point's quotient of the square of its ideal by its cube.

Finally rotate real coordinates so that \(z=(1,0,\ldots,0)\). In its local sphere ring, \(Y_0+1\) is a unit and
\[
 Y_0-1=-\frac{\sum_{j=1}^nY_j^2}{Y_0+1}.
\]
Thus the point ideal is generated by the \(n\) tangent coordinates \(Y_1,\ldots,Y_n\). Their unordered pair-products span its square modulo its cube and are independent: substitution of the formal local parametrization \(Y_0=\sqrt{1-\sum_{j=1}^nY_j^2}\), whose constant term is one, preserves these degree-two products and sends every cube to order at least three. This proves the second isomorphism in (11), and its identification with the genuine tangent quadratic form.

The functional induced by \(\psi\) on this tangent quadratic space is PSD and nonzero. To check positivity over all real tangent vectors without assuming a factorization over a residue field, form the real symmetric matrix
\[
 B_{ij}=\psi(b_i b_j).
\]
For every rational vector \(r\), positivity of \(\psi\) on \((\sum_i r_i b_i)^2\in C\) gives \(r^{\mathsf T}Br\ge0\). Density of rational vectors gives \(B\succeq0\) over \(\mathbb R\). The first-order tangent classes of the generators \(b_i\) span \(T_z^*S^n\), since they generate the localized point ideal. Hence this is positivity on the square of every real tangent linear form. The corresponding dual matrix on a tangent basis is PSD. It is nonzero because
\[
 \psi(u)=\sum_i\psi(b_i^2)=1.
 \tag{12}
\]

The degree-two tangent class of \(H\) is positive definite. The chart \(\pi(Y)=Y'/Y_0\) is a local diffeomorphism of the sphere near \(z\), because \(Y_0\ne0\), with inverse given by the appropriate sign of \((1,X)/\sqrt{1+\|X\|^2}\). Equation (3), together with \(P(p)=0,\nabla P(p)=0\), gives
\[
 \nabla^2_{\mathrm{tan}}H(z)
 =Y_0(z)^{2d}\,D\pi(z)^{\mathsf T}\nabla^2P(p)D\pi(z)\succ0.
 \tag{13}
\]
Its class in (11) is one half of this Hessian. The pairing of a positive definite quadratic matrix with a nonzero PSD dual matrix is strictly positive: after congruence by the positive definite square root, the trace is positive. This square root is used only to establish a real matrix inequality, not to construct a field-valued certificate. Therefore type-II states also satisfy
\[
 \psi(H)>0.
 \tag{14}
\]

## Membership in the rational SOS cone

Equations (8) and (14) cover every normalized pure state of \((I,C,u)\). Since \(H\in I\), BSS Theorem 2.5 gives an integer \(r>0\) with \(rH\in C\subseteq M\). The scalar \(1/r\) is a rational SOS, and the product of rational SOS elements is rational SOS. Thus
\[
 H\in\Sigma A^2.
 \tag{15}
\]
All elements of \(A\), including the resulting square factors, have rational polynomial representatives. The residue fields were used to analyze states and first jets; no coefficients from them were introduced in (15).

## Homogeneous identity and the radial multiplier

Choose rational polynomial representatives \(p_i(Y)\) of the square factors in (15), so on the sphere \(H=\sum_i p_i^2\). Since \(H\) is even under \(Y\mapsto-Y\), antipodal averaging gives
\[
 H=\sum_i\bigl((p_i^+)^2+(p_i^-)^2\bigr)
 \quad\text{in }A,\qquad
 p_i^\pm=\frac{p_i(Y)\pm p_i(-Y)}2.
 \tag{16}
\]
The even representative has only even total-degree components, and the odd one only odd components. Choose a sufficiently large even integer \(L\ge d\), with \(L\) at least every even-component degree and \(L-1\) at least every odd-component degree. For homogeneous components, set
\[
 E_i=\sum_{\substack{j\ge0\\j\ \mathrm{even}}}
 q^{(L-j)/2}(p_i^+)_j,\qquad
 O_i=\sum_{\substack{j\ge1\\j\ \mathrm{odd}}}
 q^{(L-1-j)/2}(p_i^-)_j.
 \tag{17}
\]
Every exponent is a nonnegative integer, so the coefficients remain rational. The forms \(E_i,O_i\) have degrees \(L,L-1\), respectively, and agree with the representatives on the sphere. Consequently the two homogeneous forms of degree \(2L\),
\[
 q^{L-d}H
 \quad\text{and}\quad
 \sum_iE_i^2+q\sum_iO_i^2
 =\sum_iE_i^2+\sum_{i,j=0}^n(Y_jO_i)^2,
\]
agree on the sphere. They agree everywhere: rescale any nonzero real vector to the unit sphere and use homogeneity, then use continuity at zero. A polynomial vanishing at every real vector is identically zero. We have therefore proved the exact rational polynomial identity
\[
 q^{L-d}H=\sum_iE_i^2+\sum_{i,j=0}^n(Y_jO_i)^2.
 \tag{18}
\]
Dehomogenizing at \(Y_0=1\) proves (1), with \(N=L-d\).

Multiplication by \(1+\|X\|^2=1^2+\sum X_j^2\) preserves rational SOS, so every exponent at least \(N\) also works. In particular choose an even exponent \(2a\ge N\). If
\[
 (1+\|X\|^2)^{2a}P=\sum_j f_j^2,
\]
then
\[
 P=\sum_j\left(\frac{f_j}{(1+\|X\|^2)^a}\right)^2.
 \tag{19}
\]
Its common denominator is everywhere positive. This concludes the proof.

## Application to the radial-order family

The rational quartics with a full positive definite rational Hessian Gram satisfy the theorem's hypotheses: they are nonnegative at zero minimum; the minimizer is unique and nondegenerate; and the tensor principal block of the full Hessian Gram gives
\[
 12P_4(X)=(X\otimes X)^{\mathsf T}C(X\otimes X)>0
 \quad(X\ne0).
\]
The rationally scaled family \(f_t(X)=t^{-2}F(tX)\) retains these properties. Hence each individual \(f_t\) has a finite radial SOS order. Its least order is a well-defined finite integer, and the previously proved order lower bound can be stated as growth of that least integer, not merely failure of bounded initial segments.

This theorem does not contradict the unbounded-order construction: the exponent is allowed to depend on the coefficients. Its proof gives no uniform exponent, no uniform bit bound, and no algorithm for finding a useful exponent. The adapted quadratic denominator remains the separate short certificate result.

## Scope of verification

The algebraicity derivation, rational double-vanishing lemma, comaximal square identity, order-unit proof, local tangent quotient, pure-state matrix argument, and parity-correct homogenization were derived here analytically. Imported BSS contracts use the vetted Luna source report and root's exact Corollary 4.12 refinement. Theorem 6.2 is stated with its integer-multiple conclusion. I did not re-verify primary sources or execute mathematical calculations.

A targeted inline Python document check read only this file and checked final newline, whitespace, control characters, paired math delimiters, and its three local Markdown links; all passed. The scoped command below returned no diagnostics. These are document checks, not mathematical experiments or CI checks.

~~~text
git diff --check -- paper-exact-arithmetic/evidence/reviews/development-radial-finiteness.md
~~~
