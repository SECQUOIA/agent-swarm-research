# Degree bounds for a unique zero of a rational quartic

Date: 2026-09-28. Status: scoped prior audit, with explicit corollaries of
classical results. The general sharp bound remains unresolved by this audit.

Let \(f\in\mathbb Q[x_1,\ldots,x_n]\) have degree at most four, be
globally nonnegative, and have exactly one real zero \(a\). For the node
arguments assume also \(\det\nabla^2f(a)\ne0\). Global strong convexity
implies this assumption. Write \(D=[\mathbb Q(a):\mathbb Q]\).

The established tools do not support a general \(2^n\) degree bound from
convexity alone. A rational SOS representation gives that bound under
the nondegeneracy assumption. Such a representation is an additional
assumption: explicit rational, strongly convex quartics with a unique
zero can fail even to be SOS over the reals.

## 1. Arithmetic restrictions and a general node bound

The singleton is defined over \(\mathbb Q\), so its coordinates are real
algebraic. Under the Hessian assumption this also follows directly from
the isolated complex solution of \(\nabla f=0\). Every real embedding of
\(K=\mathbb Q(a)\) sends the tuple \(a\) to a real zero of \(f\), hence
to \(a\) itself. Thus \(K\) has exactly one real embedding and \(D\)
is odd. This is a restriction on the whole coordinate field, not just
on each coordinate separately.

Every one of the \(D\) complex conjugate tuples is a zero of \(f\) and
its gradient, with invertible Hessian. They are ordinary double points
of the hypersurface \(f=0\). The standard isolated-solution form of
Bézout immediately gives \(D\le3^n\) from the gradient equations.
The prescribed zero value permits the following elementary refinement:

\[
 D\le 2\,3^{n-1}-1. \tag{1}
\]

Here is a proof that does not require all other singularities to be
isolated. Choose an \((n-1)\times n\) matrix \(A\) generically over
\(\mathbb Q\), and intersect

\[
 f(x)=0,\qquad A\nabla f(x)=0.
\]

At a conjugate node \(b\), put \(H_b=\nabla^2f(b)\). The last
\(n-1\) equations have independent linear parts \(AH_b\), so their
local common zero set is a smooth curve. Its tangent is a line spanned
by some \(v\). The choice of \(A\) can ensure
\(v^{\mathsf T}H_bv\ne0\) at every conjugate: failure is a proper
algebraic condition, and there are finitely many conjugates. On this
curve, \(f\) consequently vanishes to order exactly two. Each node is
an isolated intersection point with multiplicity two. Isolated-solution
Bézout therefore gives

\[
 2D\le4\,3^{n-1}.
\]

Oddness gives (1). For \(n=1\), use the double-root multiplicity in
the univariate polynomial directly. All these assertions also hold
when the actual degree is lower than four.

This is an application of classical intersection theory, not a claimed
new node-count theorem. The multiplicity statement with excess
components is supported by Lazarsfeld's *Excess intersection of
divisors*, §2, Theorem 2.2, Corollary 2.3, and especially the remark on
p. 290: an isolated intersection point retains its local multiplicity
in the limiting intersection cycle. Projective hypersurfaces of fixed
degrees move in base-point-free linear systems, as required there.
[Primary article](https://www.numdam.org/article/CM_1981__43_3_281_0.pdf).
Verschelde's Theorem 2.1 states the isolated-solution Bézout bound
directly. [Author's exposition](https://homepages.math.uic.edu/~jan/srvart/node3.html).

The independent [node-bound audit](quartic-node-bound-prior.md) checked
the local multiplicity calculation and these source hypotheses.

## 2. What a rational SOS representation adds

Suppose explicitly that

\[
 f=\sum_{j=1}^s q_j^2,\qquad q_j\in\mathbb Q[x],\quad\deg q_j\le2.
\]

At the real zero all \(q_j(a)=0\), and

\[
 \nabla^2f(a)=2\sum_j\nabla q_j(a)\nabla q_j(a)^{\mathsf T}.
\]

Nondegeneracy makes the Jacobian of the \(q_j\) have rank \(n\).
Choose \(n\) of the rational quadratics whose Jacobian determinant at
\(a\) is nonzero. Their common zero includes every conjugate of \(a\),
and that same determinant remains nonzero under every embedding. All
these conjugates are isolated complex common zeros. Bézout gives

\[
 D\le2^n,\qquad\text{and hence}\qquad D\le2^n-1. \tag{2}
\]

The rationality of the summands and the nondegeneracy of the zero both
enter this proof. A real SOS decomposition need not descend to a
rational SOS decomposition. An isolated real common zero need not be
isolated over \(\mathbb C\): for example the zero of
\((x^2+y^2)^2\) is real-isolated while the underlying quadratic
vanishes on complex lines. Thus one cannot apply the same Bézout
argument to a degenerate isolated zero without additional work.

## 3. Strong convexity does not supply an SOS representation

Saunderson's Theorem 1.2 gives a convex quartic form \(H\) in
\(272=16\cdot17\) variables that is not SOS over \(\mathbb R\).
Its explicit formula is

\[
 H(x,y)=\|x\|^2\|y\|^2-|\langle x,y\rangle_{\mathbb O}|^2
       +\tfrac14(\|x\|^2+\|y\|^2)^2,
 \qquad x,y\in\mathbb O^{17}.
\]

In real coordinates the octonion multiplication table has integer
entries, so \(H\) has rational coefficients. Convexity and evenness give
\(H(z)\ge H(0)=0\). Define

\[
 F(z)=H(z)+\|z\|^2.
\]

Then \(F\in\mathbb Q[z]\), \(\nabla^2F\succeq2I\), and
\(F^{-1}(0)=\{0\}\). Nevertheless \(F\) is not SOS over
\(\mathbb R\), because the degree-four homogeneous part of any
quartic SOS is itself SOS and equals \(H\). This corollary is inferred
here from the published example; the paper states the homogeneous
example. [Primary text, Theorem 1.2](https://arxiv.org/pdf/2105.08432v2).

The obstruction persists with an irrational zero. If \(G(x)\) is any
rational strongly convex quartic with unique zero \(a\), then

\[
 G(x)+H(z)+\|z\|^2
\]

is strongly convex with unique zero \((a,0)\) and is not even real
SOS. A hypothetical SOS can be restricted to \(x=a\), contradicting
the preceding argument. This rules out automatic SOS as a general
route to (2); it does not disprove a \(2^n\) degree bound by another
argument. The large ambient dimension here is not claimed minimal.

## 4. A precise low-dimensional consequence

There is a stronger conclusion in two affine variables. Scheiderer's
Theorem 4.1 classifies every rational nonnegative ternary quartic form
that is not SOS over \(\mathbb Q\): it must be a product of four
complex linear forms in general position, with Galois action \(A_4\)
or \(S_4\) on the four lines. In particular the six intersection points
form one Galois orbit of size six. [Published primary text](https://ems.press/content/serial-article-files/32129).

Homogenize our bivariate \(f\) to degree four. The result is
nonnegative also at infinity, by continuity. Its real zero
\([1:a_1:a_2]\) is singular. If the homogenization were one of the
exceptional products, this point would have field degree six, since
the lines are in general position and \(A_4\) and \(S_4\) are
transitive on unordered pairs. This contradicts oddness of \(D\).
Thus the homogenization, and therefore \(f\), is rational SOS.
Under the nondegeneracy assumption, (2) now yields

\[
 n=2\quad\Longrightarrow\quad D\le3. \tag{3}
\]

This deduction uses Scheiderer's classification, not Hilbert's theorem
alone. It does not require convexity beyond the assumed properties of
the zero. The bound is attained by the repository's cubic-field
strongly convex examples.

There is also close explicit prior. The published paper's §4.14 gives

\[
 g(x,y)=(x^2-y)^2+(xy+x-1)^2+(y^2-x+y)^2,
\]

whose unique real zero is \((\alpha,\alpha^2)\), where
\(\alpha^3+\alpha-1=0\). Its three complex nodes are conjugate.
This is a prior rational SOS quartic with a unique cubic real zero.
It is not convex: at \((1,-1/2)\) its Hessian is
\(\left[\begin{smallmatrix}33/2&-4\\-4&-1\end{smallmatrix}\right]\).
The exact Hessian substitution was checked independently in SymPy.
The example occurs in the published 2016 text; it is absent from the
2012 arXiv version also examined here.

## 5. Stronger geometric bounds require extra hypotheses

For a degree-four hypersurface in \(\mathbb P^n\) with only isolated
ordinary double points, the Arnold--Varchenko bound is

\[
 A_n(4)=\#\left\{(k_1,\ldots,k_n)\in\{1,2,3\}^n:
                2n-3<\sum_i k_i\le2n\right\}.
\]

For \(n=2,3,4,5,6,7\) this gives
\(6,16,45,126,357,1016\). Goryunov states this bound and its
asymptotic order \(3^n/\sqrt n\), and constructs quartics with
comparable node counts. This is strong evidence that unrestricted
complex node counting alone will not yield a base-two bound.
[Primary text, Theorems 1--2](https://pcwww.liv.ac.uk/~goryunov/quartics.pdf).

The hypotheses do not follow from strong convexity in affine space.
For example, put \(s=\sum_i x_i^2\) and \(f=s+s^2\). Then
\(\nabla^2f\succeq2I\) and the real zero is unique, but the
homogenization \(s^2+x_0^2s\) is singular along
\(\{x_0=0,s=0\}\), of complex dimension \(n-2\). For \(n\ge3\)
this is a positive-dimensional singular set. The inspected modern
statements of the spectral bound require isolated singularities; this
audit does not use them on such a homogenization.

Even where applicable, these bounds count all complex nodes. Real
nonnegative-form results count a different set. For example,
Blekherman--Hauenstein--Ottem--Ranestad--Sturmfels, Proposition 7, gives
at most ten real projective zeros for a nonnegative quaternary quartic
with finitely many real zeros. That does not bound the degree of a
single real zero by ten: the other conjugates need not be real.
[Primary text](https://academicweb.nd.edu/~jhauenst/preprints/bhorsK3Hilbert.pdf).

## 6. Scope, source record, and unresolved question

The main unresolved question is whether the sharper degree bound (2)
holds for all rational strongly convex quartics with minimum zero,
without a rational SOS representation. The sources examined here do
not answer it. Neither unsuccessful searches nor the failure of the
SOS argument establish that this question is new or open in the field.

For ordinary nondegenerate rational quartic zeros the safe general
bound from this audit is (1). For rational SOS quartics it is (2), and
for two affine variables (3) follows from the published classification.
Generic unconstrained optimization degree \(3^n\) is established by
Nie--Ranestad, but rational minimum zero imposes a special singular
fiber; generic critical-point degree does not establish sharpness in
this subclass. [Primary paper, §3.1](https://arxiv.org/pdf/0802.1233).

Sources inspected in addition to those cited above:

- Scheiderer's 2012 arXiv text, §4, and the published 2016 text,
  Theorem 4.1 and §§4.13--4.16, compared directly. Both PDF/text pairs
  are saved in `quartic-degree-prior-sources/`.
- Saunderson's June 2021 v2, Theorem 1.2 and its explicit formula,
  saved in the same directory.
- Choi--Lam--Reznick, *Real zeros of positive semidefinite forms I*,
  located through the [primary scan](https://staff.math.su.se/shapiro/ProblemSolving/ReznickChoiLam.pdf);
  its quaternary real-zero bound is superseded by Proposition 7 above.
- Shapiro's [problem collection](https://staff.math.su.se/shapiro/ProblemSolving/ProblemsWithPolynomials.pdf),
  Problems 2--3 and Conjecture 4, distinguishes isolated real-zero
  counts for nonnegative polynomials and for SOS polynomials. Its 2015
  conjecture statement is not treated as a statement of current status.
- The independent node audit records its full primary-source review
  of Varchenko-type bounds and excess intersection. No project-wide
  verification or CI status was inspected.

Targeted verification actually run: exact SymPy construction of the
published bivariate SOS example, differentiation, and substitution at
\((1,-1/2)\), which returned the Hessian displayed above. This checks
the nonconvexity witness, not the published general classification or
Saunderson's non-SOS theorem. A separate agent independently checked
the polar-intersection deduction and the corollaries in §§3--4 against
the saved primary texts. No correction was required. This is evidence
for the deductions, not a formal verification of the source theorems.
