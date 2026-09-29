# A quartic boundary for the quadratic value-degree theorem

Date: 2026-09-27. Status: an explicit, independently checked boundary
example. This is an application of classical algebraic-degree phenomena,
not a proposed new phenomenon or a complexity lower bound.

The polynomial annihilator-degree conclusion in
[the Hessian-span theorem](hessian-span-reduction.md) cannot extend to
arbitrary convex quartics merely by fixing the number of nonlinear
constraints or the number of distinct polynomial Hessian fields. A single
globally convex quartic epigraph constraint, with a linear objective and
rational boxes, can have an optimal value of algebraic degree \(3^n\).
The example admits strict feasibility and a unique optimizer. Its underlying
quartic is uniformly strongly convex on the box.

## 1. Explicit optimization instance

Let \(p_1,\ldots,p_n\) be distinct positive rational primes and set

\[
 \alpha_i=p_i^{1/3},\qquad
 F(x)=\sum_{i=1}^n(x_i^4-4p_i x_i),\qquad
 M=3\sum_{i=1}^n p_i^2.
\]

Consider the rational convex polynomial program

\[
 \begin{array}{ll}
 \operatorname{minimize}&t\\
 \operatorname{subject\ to}&F(x)-t\leq0,\\
 &1\leq x_i\leq p_i\quad(i=1,\ldots,n),\\
 &-M\leq t\leq0.
 \end{array}                                                     \tag{1}
\]

There is one nonlinear constraint. Its Hessian is
\(\operatorname{diag}(12x_1^2,\ldots,12x_n^2,0)\), so it is convex on
all of \(\mathbb R^{n+1}\). On the displayed \(x\)-box,
\(\nabla^2F(x)\succeq12I\). This last strong-convexity statement concerns
\(F\) in \(x\), not its epigraph polynomial in \((x,t)\).

The identity

\[
 x_i^4-4p_i x_i+3p_i^{4/3}
 =(x_i-\alpha_i)^2
   (x_i^2+2\alpha_i x_i+3\alpha_i^2)                    \tag{2}
\]

shows that the unique global minimizer of \(F\) is \(x=\alpha\).
The second factor equals \((x_i+\alpha_i)^2+2\alpha_i^2>0\).
Since \(1<\alpha_i<p_i\), this point is in the interior of the box.
The optimal value of (1) is

\[
 \theta=-3\sum_{i=1}^n p_i\alpha_i.                    \tag{3}
\]

It satisfies \(-M<\theta<0\), because
\(p_i^{4/3}<p_i^2\). Thus the epigraph bounds do not alter the optimum.
Strict feasibility also holds: take \(x_i=3/2\) and \(t=-1\).
All box inequalities are strict and

\[
 F(x)=\frac{81n}{16}-6\sum_i p_i
 \leq-\frac{111n}{16}<-1=t.
\]

An affine change \(x_i=1+(p_i-1)u_i\) gives the same example on a common
unit box \(u\in[0,1]^n\), if desired. The expanded polynomial still has
only \(O(n)\) nonzero monomials and has Hessian at least \(12I\) on
that box.

## 2. Exact algebraic degree

**Lemma.** For distinct rational primes \(p_i\) and nonzero rational
numbers \(c_i\), the number
\(s=\sum_{i=1}^n c_i p_i^{1/3}\) has degree \(3^n\) over
\(\mathbb Q\).

**Proof.** Let \(\zeta\) be a primitive cube root of unity,
\(K=\mathbb Q(\zeta)\), and
\(L=K(\alpha_1,\ldots,\alpha_n)\). The extension \(L/K\) is the
splitting field of \(\prod_i(X^3-p_i)\). It is Galois, and its group
embeds in the additive group \(\mathbb F_3^n\): an automorphism is
identified with the vector \(b\) for which
\(\sigma_b(\alpha_i)=\zeta^{b_i}\alpha_i\).

Suppose its image \(G\) were a proper subgroup. Since any subgroup of
\(\mathbb F_3^n\) is a vector subspace, there would be a nonzero
\(a\in\mathbb F_3^n\) with \(a\cdot b=0\) for every \(b\in G\).
Choose representatives \(a_i\in\{0,1,2\}\). Then
\(\beta=\prod_i\alpha_i^{a_i}\) is fixed by every automorphism and
therefore belongs to \(K\). Taking the norm from \(K\) to
\(\mathbb Q\) in \(\beta^3=\prod_i p_i^{a_i}\) gives

\[
 N_{K/\mathbb Q}(\beta)^3=\prod_i p_i^{2a_i}.
\]

The norm on the left is a rational number. Its prime valuations are
integers, so \(3\mid2a_i\) for every \(i\). Thus every \(a_i=0\),
a contradiction. Hence \(G=\mathbb F_3^n\) and
\([L:K]=3^n\). This argument includes the prime \(3\); no exception
for ramification is needed.

Independent coordinate rotations show that the \(\alpha_i\) are
linearly independent over \(K\). Indeed, in a relation
\(\sum_i d_i\alpha_i=0\), apply the automorphism rotating only
\(\alpha_j\) and subtract the original relation. The result is
\(d_j(\zeta-1)\alpha_j=0\), so \(d_j=0\).

Consequently, if \(\sigma_b(s)=s\), linear independence gives
\(c_i(\zeta^{b_i}-1)=0\) for all \(i\), hence \(b=0\).
The stabilizer of \(s\) is trivial, so \([K(s):K]=3^n\).
On the other hand,

\[
 3^n=[K(s):K]\leq[\mathbb Q(s):\mathbb Q]
 \leq[\mathbb Q(\alpha_1,\ldots,\alpha_n):\mathbb Q]
 \leq3^n.
\]

The first inequality follows because a polynomial over \(\mathbb Q\)
annihilating \(s\) also annihilates it over \(K\). This proves the
lemma. \(\square\)

Apply the lemma with \(c_i=p_i\). Multiplication by a nonzero rational
number and addition of a rational number preserve the generated number
field. Therefore the optimum (3), and more generally the minimum of
\(F(x)+3B\) for every rational \(B\), have degree exactly \(3^n\).
Every nonzero rational or integer polynomial annihilating these values
must have degree at least \(3^n\).

The proof is a short special case of classical Kummer theory; compare
[Milne, *Fields and Galois Theory*, version 5.10, Theorem 5.30,
pp. 75–76](https://www.jmilne.org/math/CourseNotes/FT.pdf).
It uses only the Galois correspondence, finite-dimensional linear algebra,
and rational prime valuations, and does not invoke the full Kummer theorem.

## 3. Input size and the parameter boundary

Choose the first \(n\) primes. The standard bound
\(p_n<n(\log n+\log\log n)\) for \(n\geq6\) implies
\(\log p_i=O(\log(n+1))\). The lower bound \(p_i\geq i+1\)
gives \(\sum_i\log p_i=\Omega(n\log(n+1))\).
The stated upper bound is the corollary (3.13), p. 69, of
[Rosser and Schoenfeld, *Approximate formulas for some functions of prime
numbers*, Illinois Journal of Mathematics 6 (1962), 64–94](https://doi.org/10.1215/ijm/1255631807).
The [original paper scan](https://denisevellachemla.eu/Rosser-Schoenfeld-1962.pdf)
was downloaded and its theorem statement inspected for this note.

In a sparse encoding that records the indices and exponents of the
variables actually occurring in each monomial, (1) has total bit length
\(N=\Theta(n\log(n+1))\). The bounds and the integer \(M\) fit within
this estimate. The optional unit-box expansion changes the constant but
not this order. For this explicit encoding,

\[
 \deg(\theta)=3^n=2^{\Theta(N/\log(N+1))}.
\]

Encoding conventions matter. If each sparse monomial stores a full
\((n+1)\)-entry exponent vector, the size is \(\Theta(n^2)\), and the
same degree is \(2^{\Theta(\sqrt N)}\). A dense list of all quartic
coefficients of the nonlinear row, with the affine boxes stored
separately, has size \(\Theta(n^4)\), giving
\(2^{\Theta(N^{1/4})}\). All these usual encodings give a
superpolynomial degree. The claim is exponential degree in dimension;
it is not exponential degree in the full input length under every
encoding convention.

For general polynomial constraints there are different possible meanings
of a Hessian-span parameter. In (1), the family contains just one nonzero
matrix-valued Hessian polynomial, so the span of that *family of
polynomial matrices* has dimension one. In contrast, the span of its
coefficient matrices, or of all its Hessian values as \(x\) varies,
has dimension \(n\): it contains the independent diagonal matrices
\(E_{11},\ldots,E_{nn}\). Thus this example refutes an extension based
only on the number of constraints or on the first interpretation. It
does not refute a theorem using the second, stronger parameter.

There is also an exact convex quadratic lift of (1): introduce \(y_i\)
and replace the quartic inequality by

\[
 x_i^2-y_i\leq0\quad(i=1,\ldots,n),\qquad
 \sum_i y_i^2-4\sum_i p_i x_i-t\leq0.                 \tag{4}
\]

The first inequalities give \(y_i\geq x_i^2\geq0\), so (4) implies
the original row; conversely choose \(y_i=x_i^2\). Bounds
\(1\leq y_i\leq p_i^2\) can be imposed without changing the projection.
The native Hessian span of this lift has dimension \(n+1\): there are
\(n\) independent coordinate matrices on the \(x\)-block and one
identity matrix on the \(y\)-block. The quadratic theorem therefore
does not predict a polynomial bound independent of \(n\) for this lift.

## 4. Prior interpretation and limitations

[Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*,
Theorem 2.2 and Section 3.1](https://arxiv.org/abs/0802.1233), gives the generic
unconstrained degree \((d-1)^n\), hence \(3^n\) for quartics.
Its formula counts complex critical solutions and concerns generic
polynomial data. The present separable polynomial is special, and each
individual optimizer coordinate has degree only three. The explicit
radical argument above establishes degree \(3^n\) for its *optimal
value* and supplies a convex, strictly feasible example with rational
boxes. This is a concrete boundary illustration consistent with the
classical result, not a new general algebraic-degree theorem.

This example establishes no hardness result for exact feasibility or
optimization, and no lower bound on the precision needed for a sign
decision. Algebraic degree alone gives neither conclusion. The optimum
already has a short expression as a sum of radicals, and its coordinates
can be approximated independently by cube-root computations. In
particular, setting \(B=0\) gives a negative optimum separated from zero
by a large amount. Choosing other rational \(B\) turns feasibility of
\(F(x)+3B\leq0\) into a comparison with the displayed radical sum;
the degree calculation does not establish the complexity of that
comparison.

The precise failed extension is a polynomial bound on annihilator degree
for fixed-count convex quartics. The quadratic proof solves a linear
stationarity system after compressing multipliers. Quartic stationarity
already has \(n\) independent cubic equations with just one nonlinear
shape. That is the structural step which does not carry over.

## 5. Verification record

The primary reviewer derived the quartic optimum, parameter distinction,
and a Kummer-style proof. A separate adversarial reviewer independently
confirmed the degree and supplied the shorter subgroup-and-norm proof
used above. The primary reviewer then checked every step of that proof,
including the prime \(3\), the passage from degree over \(K\) to degree
over \(\mathbb Q\), and the explicit strict-feasibility point.

The sources inspected were Milne's version 5.10, the original
Rosser–Schoenfeld paper, and the locally available Nie–Ranestad theorem
text cited in [the Hessian-span prior-work audit](hessian-span-prior.md).
The separate reviewer also ran the following targeted exact check with
SymPy 1.14.0:

```bash
python - <<'PY'
import sympy as sp
from time import perf_counter

t, u = sp.symbols('t u')
P = sp.Poly(t, t, domain=sp.QQ)
for n, p in enumerate((2, 3, 5), 1):
    start = perf_counter()
    resultant = sp.resultant(P.as_expr().subs(t, u), (t-u)**3-p**4, u)
    P = sp.Poly(resultant, t, domain=sp.QQ)
    degree = P.degree()
    irreducible = P.is_irreducible
    assert degree == 3**n
    assert irreducible
    print(f'n={n}, p={p}, degree={degree}, irreducible={irreducible}, terms={len(P.terms())}, max_coefficient_bits={max(abs(int(c)).bit_length() for c in P.all_coeffs())}, seconds={perf_counter()-start:.3f}')
print('PASS: exact rational resultants have degree 3^n and are irreducible for n=1,2,3.')
print(f'SymPy version: {sp.__version__}')
PY
```

Degrees were \(3,9,27\), and all three polynomials were
irreducible over \(\mathbb Q\). Here the recurrence adds a weighted
cube root \(p_i\alpha_i\), whose cube is \(p_i^4\), to the previous
sum. This checks three finite instances and supports the transcription;
the proof for arbitrary \(n\) is the field-theoretic argument above.
No Lean formalization or project-wide verification was performed.
