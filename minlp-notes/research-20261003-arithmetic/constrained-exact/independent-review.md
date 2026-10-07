# Independent review: exact comparison with few nonlinear directions

Date: 2026-10-03. Reviewer: `constrained_exact/nonlinear_review`,
assigned after the theorem was written. The reviewer did not develop
the submitted proof.

Reviewed note: [theorem.md](theorem.md), initial SHA256
`3fae109fc937fcd7af1319e5149682b59417608e707da0973df133d774f0a7c1`.

**Finding.** Theorem 1 has a valid proof of deterministic ordinary FPT
exact comparison in the nonlinear dimension. The active face is used
to prove a uniform separation bound; neither its enumeration nor a
constraint-rank assumption enters the algorithm. Corollary 2 correctly
composes this theorem with the existing mixed-integer candidate-list
theorem. That composition remains conditional on the imported theorem,
whose lattice-search proof was not re-audited here.

One minor precision convention was requested and incorporated: replace
the approximation error by its minimum with one before invoking a bound stated using
\(\log(1/\varepsilon)\). A large supplied \(\mu\) can otherwise
make that logarithm negative. This does not change the approximation
guarantee or the FPT bound. No substantive correctness defect was found.
This review does not establish publication priority or settle the
unrestricted constrained PosSLP problem.

## 1. Intrinsic dimension and affine elimination

The matrix in Section 1 computes exactly the kernel of the linear map
\(v\mapsto D_vr\). Its entries are rational and its dimensions are
polynomial in the explicit input length because degree is bounded by
four. A rational row basis \(U\) has kernel \(K\); consequently
\(x-VUx\in K\), and integrating the zero directional derivative
along that line proves \(r(x)=r(VUx)\).

Translation does preserve this kernel. Write \(r=r_4+r_3\) in
homogeneous parts. After translation by \(a\), the two higher-degree
parts are \(r_4\) and \(r_3+D_ar_4\). Vanishing of
\(D_vr_4\) makes \(D_vD_ar_4=0\), so the remaining condition is
again \(D_vr_3=0\). This checks both inclusions of the asserted
kernel equality.

At the constrained minimizer, the polyhedral normal-cone formula puts
the negative gradient in the span of the active normals. The gradient
therefore annihilates the direction space of their common affine
equations. Global strong convexity makes this point the unique
unconstrained minimizer on that affine space. Redundant rows, opposite
rows defining an equality, and zero optimal multipliers do not alter
this conclusion.

In the chart \(x=\bar x+ZTt+ZWw\), every higher-degree term is
independent of \(w\). Thus the dependence on \(w\) is exactly a
quadratic with constant Hessian \(H\) and affine linear coefficient
\(Jt+a\). Since \(ZW\) has full column rank, strong convexity
makes \(H\) positive definite. Its unconstrained minimum is exactly
the stated affine map \(w(t)\).

The resulting map \(x=u+Dt\) has full column rank: its image under
\(U\) has derivative \(UZT\), which has rank \(s\). Restricting
the original objective along this affine map therefore gives
\(\nabla^2\phi\succeq\mu D^{\mathsf T}D\succ0\).
In particular, the stationary equation used for separation has one
real solution. Complex stationary components need not be isolated;
the proof correctly avoids that unnecessary assumption.

If \(s=0\), quadratic elimination returns a rational point. If the
active affine space is a point, the same conclusion follows directly.
When the kernel block is empty, no matrix inversion in that block is
needed. These cases preserve the claimed output contract.

## 2. Uniform coefficient bounds and the source theorem

The potentially delicate issue is uniformity over unknown active sets.
An independent subset of at most \(n\) input rows determines the
affine chart. Each relevant minor has polynomial bit length by the
determinant bound, uniformly over every such subset. Nullspace bases,
the complementary columns, and the inverse of \(H\) require a
fixed number of rational linear-algebra operations of polynomial size.
For degree four, affine substitution creates only polynomially many
terms. Clearing their denominators also costs polynomial bit length.
Hence the single polynomial majorant \(T(L)\) can have an absolute
exponent. There is no factor \(L^k\) hidden in this construction.

I directly checked
[Basu, Theorem 2.16, page 12](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf).
Its integer-coefficient clause bounds intermediate and output coefficient
bit sizes by the input bit bound multiplied by a degree factor depending
on the quantifier-block sizes and free-variable count. With one block
of \(s\le k\) variables, one free variable, degree four, and
\(s+1\) input polynomials, this gives \(G(k)T(L)\), rather than
\(T(L)^{O(k)}\). The degree and arithmetic-operation bounds are also
functions of \(k\). This is exactly the coefficient dependence
needed by the submitted proof.

The singleton argument is valid: if every nonzero polynomial in the
quantifier-free formula were nonvanishing at \(\alpha\), their
signs would all be constant on a neighborhood, so the formula could not
define just \(\{\alpha\}\). For \(\alpha\ne0\), removing zero
roots from a vanishing integer polynomial leaves a nonzero integer
constant term. When \(|\alpha|<1\), its remaining terms have
total magnitude at most \(D_0H_0|\alpha|\). This yields the
claimed separation bound. The bound is uniform over active faces;
its calculation uses their coefficient majorant, without finding a face.

## 3. Approximation followed by exact sign recovery

The proposed radius is valid. At a radius \(r\ge R\), the quadratic
lower bound gives
\[
 f(x)-f(x_0)
 \ge (\mu r/2-\|\nabla f(0)\|_1)r
       -|f(x_0)-f(0)|>0.
\]
The feasible rational LP witness has polynomial length, so both \(R\)
and a monomial bound on \(\|\nabla h\|\) have polynomial-length
encodings. This also covers an unbounded input polyhedron.

I directly checked
[Slot, Steurer, and Wiedmer, Corollary 1.2 and Appendix D](https://arxiv.org/html/2511.03440v1).
The corollary returns a point in the original rational polyhedron;
only its objective value is approximate. Appendix D describes rational
strong-separation queries and an affine-hull reduction, so deficient
dimension is allowed and the point is exactly feasible. Its bit runtime
is polynomial in the data and requested accuracy bits. The present
objective satisfies global convexity and has an attained finite minimum.
Thus this source supplies the contract needed here.

At a feasible approximation, constrained first-order optimality gives
\(\nabla f(p)^{\mathsf T}(\widehat x-p)\ge0\). Combining this
with strong convexity proves the stated distance bound. The segment
between \(p\) and \(\widehat x\) lies in the radius-\(R+1\)
ball, so the gradient bound for \(h\) proves error at most
\(\gamma/8\). Exact zero yields a rational observed magnitude at
most \(\gamma/8\), whereas a nonzero value yields magnitude at least
\(7\gamma/8\) and the correct sign. The threshold \(\gamma/2\)
therefore separates both cases strictly.

The algorithm really prints \(N=G(k)T(L)\) precision bits. This
is affordable under the claimed FPT bound; the proof does not confuse
\(N\) with its binary encoding length. Rational evaluation of a
fixed-degree polynomial has polynomial cost in that printed length.
Applying this sign routine to each slack recovers the full active set
with only a polynomial number of calls. The affine description can
then be constructed from the known set.

## 4. Mixed-integer composition

The imported
[candidate-list theorem](../../research-20260927/mixed-linear-strong-quartic-candidate-list.md)
and its [independent review](../../research-20260927/mixed-linear-strong-quartic-candidate-list-review.md)
state ordinary deterministic FPT construction of all potentially
optimal integer blocks, including feasibility handling and polynomial
exponents independent of integer dimension. I checked those contracts;
this review does not substitute for their earlier source and proof audit.

For a fixed integer block, substituting into
\(g(U_z z+U_y y)\) leaves all terms of degree at least three in
\(y\) dependent on \(U_y y\). The fiber's nonlinear dimension
is therefore at most \(k\). Its continuous Hessian is a principal
block of the original Hessian and retains the supplied \(\mu\).
Product fibers have strong convexity with the same modulus and nonlinear
dimension at most \(2k\). Their difference observable has degree
at most four. Thus Theorem 1 compares their exact minima, including ties.

If a fiber input has length at most \(a(t)L^{C_0}\), applying
Theorem 1 costs at most
\(F(k)a(t)^C L^{C_0C}\). Multiplication by the FPT list size
preserves an absolute polynomial exponent. Parameter functions can be
replaced by nondecreasing majorants and combined into a function of
\(k+t\). There is no constraint-rank dependence in this composition.

## 5. Targeted symbolic challenge and limits

I ran a targeted inline Python/SymPy script with the command form
`python - <<'PY'`. It used the positive definite rational matrix
\[
 Q=\begin{pmatrix}
 4&1&1&0\\1&5&0&1\\1&0&4&1\\0&1&1&5
 \end{pmatrix}
\]
and the objective
\(f(x)=\tfrac12x^{\mathsf T}Qx+(1,-2,3,-1)^{\mathsf T}x
+(x_0+x_1)^4\), restricted to
\(x_2=x_0+2x_1+1\) and \(x_3=2\).
With \(t=x_0+x_1\), exact elimination produced
\[
 \phi(t)=\frac{18t^4+89t^2+184t+221}{18},\qquad
 x(t)=\left(\frac{10t+7}{9},-\frac{t+7}{9},
                 \frac{8t+2}{9},2\right).
\]
The checks passed for the stationary identity, the positive quadratic
remainder after elimination, positive reduced curvature, both affine
equations, nonlinear rank one, and preservation of that rank under a
rational translation. These finite checks challenge the algebra only;
they do not prove the bit bound or implement the general FPT algorithm.

No project-wide checks or CI status/log inspection were performed.

## 6. Final amendment check

I reread the full theorem at SHA256
`2d0d96100ac81ccec2e7614280991d9268d9f045e53c47212f055637719b3a40`.
It incorporates the error cap and replaces the optional full positive
definite Gram with a rational positive semidefinite Gram for
\(v^{\mathsf T}(\nabla^2f(x)-\mu I)v\). Coefficient matching and
rational semidefinite checking certify the promised lower curvature.
This is explicitly a subclass certificate, so no SOS representation for
every strongly convex quartic is asserted. Both amendments are sound.

A targeted inline Python check passed for final newline, trailing
whitespace, balanced Markdown math delimiters, and all local links in
this review. The following targeted command also passed:

```text
git diff --check -- research-20261003-arithmetic/constrained-exact/independent-review.md
```

The review is closed with no remaining correctness objection to the
theorem and its stated composition, subject to the explicit imported
candidate-list dependency and publication-priority limitation.

## 7. Integrated report review

I subsequently read the full integrated
[constrained-comparison section](../document/sections/05-constrained-comparison.tex)
and compared it with the accepted nonlinear-dimension theorem,
[structural Newton note](structural-newton.md),
[network-flow note](network-flow.md), and
[flow source-interface review](network-flow-review.md).
The integrated section's reviewed SHA256 was
`ebf127af06d1f9369cf548dfc5b870065ee1060af1309b0488dc43ced507f8bd`.
**Verdict: no integration blocker found.** This was a comparison of the
integrated claims with their reviewed companions; it did not repeat the
separate audits of the Pang--Han and Végh algorithms.

The condensed nonlinear-dimension proof preserves the essential uniformity
argument: the active affine chart has a coefficient bound with an absolute
polynomial exponent, and quantifier elimination increases that bit bound
by a function of nonlinear dimension. The ordinary approximation therefore
uses \(F(k)L^C\) printed precision bits, rather than expanded data whose
size would introduce an exponent depending on \(k\). Active sets are
recovered after sign decisions, without enumeration.

The mixed-integer paragraph has the scope of the preceding global strong-
convexity promise on all variables. Its imported candidate list preserves
FPT output size; restriction to an integer fiber preserves curvature and
nonlinear dimension at most \(k\). Pairwise comparison doubles only
that parameter. Thus its ordinary FPT statement in \(k+t\) is correctly
distinguished from the separate \(\mathrm P^{\mathrm{PosSLP}}\)
structural subclasses. I suggested making the word "joint" explicit in
the mixed-integer paragraph as an optional clarification.

The transfer interface retains its necessary restriction to rational
arithmetic and comparisons with an operation count independent of expanded
Taylor-coefficient lengths. Shared numerator-denominator circuits describe
the rational Newton iterates. The section does not claim such a circuit
represents a generally irrational optimizer, and it explicitly labels
the nonlinear-dimension optimizer description as implicit. It also keeps
the adaptive Turing reduction distinct from a single-instance reduction.

The Newton rate, absence of a strict-complementarity assumption, structured
box promises, flow capacities, and finite-radius reduction agree with
their companions. The final observable comparison also uses the
polynomial-bit bound on \(\|\nabla h\|\) on the supplied box, as
the full transfer proof states. I suggested mentioning that factor in
the condensed transfer paragraph for clarity; its omission there does not
change the theorem or invalidate the cited full proof.

No additional computational or project-wide verification was required
for this read-only integration review.
