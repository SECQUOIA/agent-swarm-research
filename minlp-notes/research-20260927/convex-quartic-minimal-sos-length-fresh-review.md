# Fresh review of the convex-quartic SOS-length theorem

Date: 2026-09-28. Reviewer: a separate agent that did not contribute
to the theorem or its proof before this review.

The complete proof in
[the main note](convex-quartic-minimal-sos-length.md) passes this
independent review. I found no mathematical correction needed.
The theorem is a sharp structural restriction, with a useful application
to the cyclic construction's exact SOS length. This review does not
establish priority or an optimization complexity consequence.

The reviewed main-file SHA-256 was
88b6eadd2e7739ed5a0d04fb71f1b064c81e3706997bc2f4e9fb78ad2105a13c.
The main note was not edited by this reviewer.

## Statement and hypotheses

The statement is correctly limited to real polynomial SOS
representations of a globally convex polynomial of degree exactly
four, with a zero at which the Hessian is positive definite.
The lower bound is on the number of polynomial squares, allowing
arbitrary real coefficients. Positive scalar weights do not evade it,
because their square roots can be absorbed in the factors.

The preliminary rank argument is valid. Highest-degree homogeneous
squares cannot cancel over the reals, so each factor has degree at most
two. At a zero, the Hessian is twice the residual Jacobian's Gram
matrix. Thus fewer than \(n\) factors are impossible. Convexity and
positive definite Hessian at one zero imply that this zero is unique:
any other zero would force the intervening segment to be zero, which
contradicts the second directional derivative at the first endpoint.

The remaining proof assumes exactly \(n\) factors, and uses the
resulting square, invertible Jacobian at the zero. No later step
silently assumes global invertibility of this Jacobian.

## Flat directions and their elimination

I independently checked the following points in Sections 2 and 3.

1. The leading quartic \(H=\|q_2\|^2\) is convex as a pointwise
   scaling limit. It is nonnegative and even homogeneous, so its zero
   set \(K\) is a linear subspace. In particular, convexity of the zero
   set alone is supplemented by its invariance under all real scalars.
2. The displayed convexity estimate, followed by
   \(\eta\downarrow0\), proves translation invariance of \(H\) along
   \(K\). Applying the estimate a second time with the opposite
   displacement proves equality. The coefficient of \(t^2\) in
   \(\|q_2(x+tv)\|^2\) then proves invariance of each residual's
   quadratic part. This step does not infer componentwise invariance
   from norm invariance without justification.
3. In coordinates \((w,v)\), the \(ww\) Hessian block is affine in
   the freely signed flat variable \(v\). Positivity for every \(v\)
   forces each coefficient matrix to vanish. Since these coefficients
   are Hessians of homogeneous quadratics, this gives the full
   identity \(B^{\mathsf T}q_2=0\), not just an identity modulo affine
   terms.
4. Full column rank of \(B\) follows from nonsingularity of the
   original residual Jacobian. Thus the least-squares minimizer
   \(v_0(w)\) exists uniquely and is affine. The orthogonal
   decomposition in equation (9) is exact, and \(p_v=v_0(p_w)\).
5. Restriction to this affine graph preserves convexity and gives the
   Hessian \(E^{\mathsf T}\nabla^2F(p)E\). The graph Jacobian \(E\)
   has full column rank, so this Hessian is positive definite.
   Consequently the reduced square map has one regular zero.
6. Orthogonal output projection preserves the norm of \(q_2\)
   because \(q_2\) already lies in \((\operatorname{im}B)^\perp\).
   Its norm on the remaining unit sphere has a positive minimum.
   This is the needed coercive leading term; mere properness of the
   original residual map would not suffice for the later homotopy.

There is no missing case when \(K=\{0\}\), because no elimination is
needed. The case \(K=\mathbb R^n\) is ruled out by degree exactly
four. The remaining dimension is therefore at least one.

## Degree and parity

The bound
\[
\|h_t(w)\|\ge a\|w\|^2-b\|w\|-c
\]
is uniform for \(t\in[0,1]\). It proves the stronger fact needed
here: the entire homotopy is proper. It therefore extends
continuously at infinity to a homotopy on the one-point
compactifications. No smoothness of that extension at infinity is
required for the topological degree argument.

The degree of the reduced map is \(+1\) or \(-1\), because its zero
fiber consists of one regular point. A nonzero regular value of the
leading map has a finite preimage. Sard's theorem allows a regular
value outside the image; the empty fiber then gives degree zero and
does not create an exception.

Every nonempty such fiber is paired by \(w\mapsto-w\).
The two points of a pair have local degrees whose sum is even.
This suffices for the contradiction in all dimensions. The stronger
sign observation is also correct: pair contributions cancel in odd
dimension and agree in even dimension. In particular, dimension one
is covered.

I read the cited primary textbook passages directly:

- [Hatcher, Chapter 2](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf),
  Section 2.2, printed pages 134–136: homotopy invariance and
  Proposition 2.30, the sum of local degrees.
- [Milnor, *Topology from the Differentiable Viewpoint*](https://www.ux1.eiu.edu/~cidelman/Classes/4855%20and%205220/Supplementary%20Texts/MilnorTopDiffVpt.pdf),
  Sections 2, 4, and 5, especially printed pages 27–29:
  regular values, orientation signs, and homotopy invariance.

The main note verifies the extra properness needed to use these
compact-space statements. It does not assume that a homotopy of
individually proper maps is automatically proper.

## Sharpness, boundaries, and significance

The displayed sharp example has exactly \(n+1\) available squares
and Hessian
\[
8xx^{\mathsf T}+(4\|x\|^2+2)I.
\]
Thus the lower bound is attained in every positive dimension.
Applying it to the cyclic family is valid once that family's
independently verified convexity, zero, and \(n+1\)-square
representation are used. The topological argument does not prove
the arithmetic claims about that family by itself.

The examples omitting each hypothesis are correct. A further
boundary makes the restriction to degree four concrete:
\[
G(x)=(x_1+x_1^3)^2+\sum_{j=2}^n x_j^2.
\]
This sextic has \(n\) squares, a unique zero at the origin, and
\[
\nabla^2G(x)=
\operatorname{diag}(2+24x_1^2+30x_1^4,2,\ldots,2)\succeq2I.
\]
The same \(n+1\) lower bound therefore fails already in degree six.
The main note does not claim this extension.

The theorem gives a restriction on exact residual representations,
or equivalently on the rank of any positive semidefinite Gram
matrix representing such a quartic. It supports the optimality of
the cyclic compression. It gives neither a solver speedup nor a
hardness result, and should not be presented as either. Whether
this short structural theorem is independently publishable depends
especially on further literature comparison.

## Literature comparison

I read the introduction and Section 1 of
[Scheiderer, *Sum of squares length of real forms*](https://staff.math.su.se/shapiro/ProblemSolving/Scheiderer!.pdf).
Theorem 1.12 and Corollary 1.13 give upper bounds on SOS length
from the multiplicity of a real zero, after homogenization.
They do not give the present lower bound for every globally convex
quartic with a nondegenerate affine zero. In two affine variables,
the ternary-quartic upper bound complements this theorem to give
length exactly three under its hypotheses. General worst-case
Pythagoras-number bounds have different quantifiers.

The [separate literature audit](convex-quartic-minimal-sos-length-literature-audit.md)
located and examined
[Harrison's full dissertation](https://web.math.ucsb.edu/~martin/dissertation.pdf).
I independently read the statements and arguments around Proposition
2.1.4, Theorem 3.2.10, and Proposition 3.3.1. These concern Gram
rank, convexity of a quadratic map's image, and Pythagoras numbers.
Their convexity hypothesis is different from convexity of the scalar
polynomial in this theorem. They do not supply an evident proof of
the proposed \(n+1\) lower bound.

I also independently read Section 2 of
[Khimshiashvili, *Remarks on Homogeneous Endomorphisms*](https://viam.science.tsu.ge/publishing/proceedings/vol66/Khimshiashvili.pdf),
especially Corollary 1 on page 28 and Proposition 1 on page 29.
These give direct antecedents for the parity and nondegenerate-leading-part
steps. The convex flat-direction reduction is absent from that section.
This source should not replace the main proof or its textbook
references: it also makes incorrect assertions outside the claims used
here. For example, Remark 5 calls
\((x,y)\mapsto(x^2+y,x)\) non-proper, although the displayed map
has polynomial inverse \((u,v)\mapsto(v,u-v^2)\) and is proper.

The audit also compared convex-quartic optimization and convex-form
SOS papers. Its search found no equivalent scalar-convexity
lower bound in the portions examined. Khimshiashvili's 2019
quadratic-mapping paper was available only through its publisher
abstract and references and remains a comparison gap.
The classical degree obstruction is not itself a novelty claim.
The point requiring further comparison is its use after the convex
flat-direction reduction. No unsuccessful search is evidence of
priority.

## Verification actually performed

This review reconstructs the universal argument by hand and checks
its imported topological facts against primary sources.
The existing example checker was read but not rerun: repeating it
would not independently verify the topology or the flat reduction.

One additional exact SymPy check examined the sextic boundary above
in dimensions one through five. The following command passed:

~~~text
python - <<'PY'
import sympy as sp
for n in range(1,6):
    x = sp.symbols(f'x0:{n}', real=True)
    residual = x[0] + x[0]**3
    F = residual**2 + sum(t**2 for t in x[1:])
    target = sp.diag(2 + 24*x[0]**2 + 30*x[0]**4,
                     *([sp.Integer(2)]*(n-1)))
    assert (sp.hessian(F,x)-target).applyfunc(sp.expand) == sp.zeros(n)
    assert sp.degree(F,x[0]) == 6
    assert sp.expand(residual-x[0]*(x[0]**2+1)) == 0
print('Exact sextic boundary: n=1,...,5 passed.')
PY
~~~

An initial version compared unexpanded SymPy expressions by
structural equality and failed. Expanding their difference fixed the
check; no mathematical formula changed. The computation confirms
these finite-dimensional identities, while the displayed formula
and factorization prove the boundary example for every \(n\ge1\).

No Lean verification, project-wide test, or CI inspection was
performed.

A targeted Python check passed for this review and the separate
literature audit: final newlines, trailing whitespace, control
characters, balanced inline/display math delimiters, and both local
links. A second SHA-256 read confirmed that the main note was unchanged.
