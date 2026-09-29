# Independent review of the sparse minimal-polynomial output boundary

Date: 2026-09-28. Scope: the
[sparse-output strengthening](sparse-algebraic-output-boundary.md) of
[the short-input QCQP construction](short-input-qcqp-degree-lower-bound.md),
including a read of the complete draft's final theorem and proof.
This reviewer did not develop that construction. The review treats its
established field-degree and input-size conclusions as inputs and checks
the additional translation, coordinate change, and output-size arguments.
A fresh subreviewer separately checked the coordinate change and its
coefficient-size accounting.

**Verdict:** the strengthening is correct for an explicit monomial list of
the minimal polynomial of the requested value or a specified original
optimizer coordinate. No correction to the proposed proof is needed. The
output-format qualification is essential: the argument does not cover an
arbitrary exact algebraic representation.

## 1. Translation makes every coefficient nonzero

Let

\[
 P(X)=\sum_{i=0}^D a_iX^i\in\mathbb Q[X],\qquad a_D\ne0,
\]

and let \(c_j(T)\) be the coefficient of \(X^j\) in \(P(X-T)\).
Direct expansion gives

\[
 c_j(T)=\sum_{i=j}^D a_i\binom ij(-T)^{i-j}.
\]

This polynomial has degree exactly \(D-j\) and leading coefficient
\(a_D\binom Dj(-1)^{D-j}\). In particular it is nonzero, including
the constant polynomial \(c_D=a_D\). The union of all integer roots
of these coefficient polynomials has size at most

\[
 B_D=\sum_{j=0}^D(D-j)=D(D+1)/2.
\]

The \(B_D+1\) integers \(0,\ldots,B_D\) therefore contain a choice
\(t\) for which every coefficient of \(P(X-t)\) is nonzero.
Its binary length is \(O(1+\log D)\).

If \(P\) is a minimal polynomial of \(\alpha\), then
\(P(X-t)\) is a minimal polynomial of \(\alpha+t\): substitution
by an integer translation is an automorphism of \(\mathbb Q[X]\)
and preserves irreducibility and degree. It is also an automorphism of
\(\mathbb Z[X]\), so a primitive integer normalization remains
primitive. Multiplication by a nonzero rational scalar cannot change
which coefficients vanish. Thus the density assertion applies to every
normalization of that minimal polynomial.

Applying this to the degree-\(D\) optimal value requires only adding
the integer \(t\) to the objective constant. The optimizer, constraints,
and every Hessian are unchanged. The translated objective has value
\(v+t\) and a minimal polynomial with exactly \(D+1\) nonzero terms.

The finite-choice argument establishes existence of a short translation.
It does not, by itself, give a procedure polynomial in the QCQP input size
for finding the translation: the search range can be much larger than
that size. This distinction does not weaken the worst-case output lower
bound.

## 2. One optimizer coordinate can generate the entire field

In the block construction, let \(a_i\) be the first optimizer coordinate
of block \(i\). Each \(a_i\) generates its block field, so
\(E=\mathbb Q(a_1,\ldots,a_h)\) has degree \(D\).
Because the characteristic is zero, there are exactly \(D\) distinct
embeddings of \(E\) into \(\mathbb C\). For two distinct embeddings
\(\sigma,\tau\), the polynomial

\[
 \sum_{i=1}^h T^{i-1}\bigl(\sigma(a_i)-\tau(a_i)\bigr)
\]

is nonzero and has degree at most \(h-1\). It excludes at most
\(h-1\) integer choices of \(T\). Counting unordered pairs of
embeddings proves that some integer

\[
 1\le k\le 1+(h-1)D(D-1)/2
\]

makes \(\alpha=\sum_i k^{i-1}a_i\) have \(D\) distinct images.
Since \(\alpha\in E\), its degree is exactly \(D\), and
\(\mathbb Q(\alpha)=E\). This does not assume normality of \(E\).

Reorder the original variables so that the first coordinate of block one
is \(x_1\), and write

\[
 v=\sum_{i=2}^h k^{i-1}e_{j_i},\qquad v_1=0,
 \qquad S=I+e_1v^T,
\]

where \(j_i\) is the index of the first coordinate of block \(i\).
The affine change of variables

\[
 y=Sx+t e_1
\]

has integer matrix of determinant one. Indeed,
\((e_1v^T)^2=0\), so

\[
 U=S^{-1}=I-e_1v^T,
 \qquad x=Uy-t e_1.
\]

All coordinates except the first remain the original coordinates, and
the first new optimizer coordinate is \(\alpha+t\). Choose \(t\)
by Section 1 for the minimal polynomial of \(\alpha\). Then this
specified coordinate has degree \(D\) and a minimal polynomial with
\(D+1\) nonzero coefficients.

An invertible affine change maps the feasible set bijectively onto the
new feasible set. It preserves compactness, strict feasibility, and the
unique optimizer. The Hessian map \(Q\mapsto U^TQU\) preserves
positive definiteness and is an invertible linear map on symmetric
matrices, so the span of the constraint Hessians still has dimension
exactly \(h\). This is a continuous-QCQP construction. Unimodularity
would preserve an all-integer lattice, but mixing continuous and integer
coordinates need not preserve a specified mixed-integer partition; no
such extra assertion is needed here.

## 3. The coordinate change preserves the short-input estimate

For a quadratic in the convention

\[
 q(x)=\tfrac12x^TQx+b^Tx+c,
\]

the transformed coefficients are

\[
 Q'=U^TQU,\qquad b'=U^T(b-tQe_1),
 \qquad c'=c-tb_1+\tfrac12t^2Q_{11}.
\]

More explicitly,

\[
 Q'_{ij}=Q_{ij}-v_jQ_{i1}-v_iQ_{1j}+v_iv_jQ_{11},
\]

\[
 b'_j=b_j-tQ_{j1}-v_j(b_1-tQ_{11}).
\]

Each new coefficient is a sum of at most four products of old coefficients
with the displayed integers. Consequently, if old rational coefficients
have at most \(L\) bits, new coefficients have

\[
 O\bigl(L+\log(1+\|v\|_\infty)+\log(1+|t|)\bigr)
\]

bits, with an absolute implied constant. In particular, rational
denominators do not accumulate across a dimension-dependent sum.

Generally, the primitive choice gives
\(\log k=O(1+\log h+\log D)\) and
\(\log(1+\|v\|_\infty)=O(h(1+\log h+\log D))\).
For the actual family, \(D=\prod_i2(p_i-1)\) and
\(P=\max_i p_i\), so these bounds reduce to

\[
 \log D=O(h\log P),\qquad
 \log(1+\|v\|_\infty)=O(h^2\log P),\qquad
 \log(1+|t|)=O(h\log P).
\]

The original existential weighting and positive-definite constraint
mixing have \(O(h^2\log P)\)-bit coefficients. That bound survives the
shear and translation. For primes in \([R,2R]\), the dense input
length therefore remains \(N=O_h(R^2\log R)\), while
\(D\ge[2(R-1)]^h\).

For any proposed finite function \(f\) and absolute exponent \(C\),
fix an integer \(h>2C\) and let \(R\) tend to infinity along suitable
prime intervals. Then \(D+1>f(h)N^C\) eventually. Constants depending
on the fixed \(h\) cannot absorb the excess power of \(R\).
The same argument applies to the fully computable, larger-weight base
family using its stated \(O_h(R^6\log R)\) input bound and
\(h>6C\); selecting the new primitive shear and translation by the
finite-choice proofs still establishes existence, not an additional
uniform polynomial-time instance generator.

Value density and coordinate density can hold in the same instance by
using separate objective and coordinate translations. If a single common
translation is desired, the union of the two bad sets can contain up to
\(D(D+1)\) integers; use that larger count rather than silently reusing
the bound for one polynomial.

## 4. Precisely what the lower bound excludes

An explicit monomial list for the minimal polynomial of either designated
output contains \(D+1\) nonzero terms, whether the interface is called
dense or sparse. Merely writing these terms requires \(\Omega(D)\)
output symbols and time in the usual bit model. Thus no algorithm can
always produce that required format within \(f(h)N^C\) time.

The argument does not exclude any of the following formats or tasks:

- a polynomial in a shifted basis, or an arithmetic circuit for it;
- an annihilating polynomial that is not required to be minimal;
- another primitive generator together with a map to the requested value;
- a tower of extensions, a sum of block algebraic numbers, or an implicit
  polynomial system;
- feasibility, comparison, approximation, or other decision problems.

In particular, calling the result a lower bound for all sparse algebraic
representations would be too broad. The precise result is about an
explicit sparse **minimal-polynomial** output in the ordinary monomial
basis of the requested scalar or coordinate. The example demonstrates
that good conditioning assumptions such as compactness, Slater's
condition, and positive definite Hessians do not alone remove this output
cost; it makes no quantitative claim about numerical conditioning.

The translation and primitive-element arguments are elementary classical
algebra. This review makes no separate novelty claim for them or for their
combination with the existing QCQP construction. The underlying
arithmetic-family prior comparison remains in the construction and its
[independent review](short-input-degree-adversarial-review.md).

## 5. Targeted verification and limits

An inline command of the form `python - <<'PY'` was run with SymPy. It
checked all 44 coefficient formulas for symbolic degree-one through
degree-eight polynomials, found permitted dense translations for the
12 examples \(X^d-1\), \(1\le d\le12\), and verified the full
symbolic affine-substitution identity for an arbitrary symmetric
four-variable quadratic, including the inverse and determinant of the
shear. All checks passed. The examples are checks on the translation
lemma, not irreducibility tests or proofs of the asymptotic statement.

The general claims rest on the algebraic proofs above. No numerical
optimization experiment, project-wide verification, CI inspection, or
Lean proof was performed. The base construction's arithmetic
irreducibility and field-composition proof was not repeated as part of
this narrowly scoped review.

A second inline Python command checked this review's final newline,
trailing whitespace, control characters, balanced math delimiters, and
three local document links. All checks passed.
