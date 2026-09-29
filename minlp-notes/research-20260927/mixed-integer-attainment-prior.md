# Prior audit: unbounded mixed-integer convex quadratic optimization

Date: 2026-09-27. Scope: the qualitative attainment and closed-image claims,
and the proposed fixed-parameter exact algorithm in
[the attainment manuscript](mixed-integer-attainment-frontier.md).

**Assessment.** Finite attainment is already a consequence of a directly
accessible Bank–Mandel result from 1987. The same result gives closedness
of rational linear images. These are useful ingredients, not candidate
novel contributions. The possible contribution is the effective exact
algorithm, witness bounds, and algebraic output bounds when the integer
dimension and the continuous Hessian matrix span are fixed. Its priority
remains unestablished.

## 1. A primary source that settles qualitative attainment

Bernd Bank and Reinhard Mandel, *Nonlinear parametric integer programming*,
in *Parametric Optimization and Related Topics*, Mathematical Research 35,
Akademie-Verlag, 1987, pp. 16–48. The
[publisher preview](https://api.pageplace.de/preview/DT0400.9783112720936_A50662169/preview-9783112720936_A50662169.pdf)
contains the relevant statements.

For globally quasiconvex polynomials, write

\[
 M(b)=\{w:f_i(w)\le b_i\},\qquad
 G(b)=M(b)\cap(\mathbb Z^k\times\mathbb R^n).
\]

On p. 20, (MIG) means finite generation by mixed-integer vectors; (IG)
means generation by integer vectors. Theorem 3(iii), p. 24, gives (IG)
for the common recession cone when all coefficients are rational.
The stable subsystem on p. 34 retains polynomials bounded below on
\(M(b)\). Theorem 7(ii) makes \(B=\{b:G(b)\ne\varnothing\}\) closed if
that subsystem's recession cone satisfies (MIG). Rationality ensures
this by Theorem 3(iii) applied to the subfamily. No compact-plus-cone
condition appears in Theorem 7.

Append a rational quasiconvex objective row: closedness gives finite
attainment. Append \(Aw\le b,-Aw\le-b\), for rational \(A\): the inverse
image of \(B\) under \(b\mapsto(\bar b,b,-b)\) is the rational linear
image of the original feasible set, hence closed. Neither conclusion
requires fixed dimensions or Hessian span.

## 2. Relation to the 1988 book citation

Bertsekas and Tseng, *Set intersection theorems and existence of optimal
solutions*, Mathematical Programming 110 (2007), 287–314, explicitly
attribute a mixed-integer quasiconvex-polynomial existence result to
Bank–Mandel, *Parametric Integer Optimization* (1988), Theorem 7.4;
see p. 309, immediately before Proposition 11 in the
[author-hosted published paper](https://www.mit.edu/~dimitrib/Set_Intersections.pdf).
Their Proposition 11 concerns a different general condition on asymptotic
directions; it should not be cited as though it directly supplies the
mixed-integer theorem.

The [1988 publisher record](https://www.degruyterbrill.com/document/doi/10.1515/9783112472668/html)
confirms the book and its chapters on existence, but the original text of
Theorem 7.4 was not obtained in this audit. Its exact wording is therefore
not asserted here. The directly inspected 1987 theorem suffices for the
two qualitative conclusions above. The preview of the 1988 companion paper
*(Mixed-) integer solutions of quasiconvex polynomial inequalities*
contains its introduction, which identifies it as supplying proofs omitted
from the earlier stability treatment, but not the later relevant theorems;
see the [publisher preview](https://api.pageplace.de/preview/DT0400.9783112479926_A46396805/preview-9783112479926_A46396805.pdf).

## 3. What this removes from the novelty claim

For rational native PSD quadratic constraints and objective, global
quasiconvexity is automatic. Thus an elementary recession-elimination proof
is an alternative proof of an old conclusion. Its potential additional
role is algorithmic: it preserves attainable objective values, reduces
dimension, preserves the continuous Hessian span, and controls coefficient
growth when the integer dimension is fixed. Those effective properties
require the new manuscript's proof; the literature comparison does not
verify them.

The proposed advance should be stated as exact Turing tractability for
fixed \((k,h)\), without input bounds and with arbitrary continuous
dimension and arbitrary numbers of affine and quadratic rows. It should
not be stated as a new attainment theorem, a new closed-image theorem,
or a general tractability theorem for mixed-integer convex quadratic
systems. Native positive semidefiniteness is stronger than convexity of
the feasible set defined by indefinite quadratic inequalities.

## 4. Closest exact-complexity comparisons

Alberto Del Pia, *Convex quadratic sets and the complexity of mixed
integer convex quadratic programming*,
[arXiv:2311.00099](https://arxiv.org/abs/2311.00099), Proposition 4 and
Theorem 3 in the inspected version, gives exact feasibility for a
polyhedron intersected with one convex quadratic sublevel, and exact
optimization of a convex quadratic objective over a mixed-integer
polyhedron. Its fixed-parameter tractability in the integer dimension is
stronger than the proposed polynomial-for-fixed-parameters guarantee on
those subclasses. Its stated results do not permit an arbitrary family
of quadratic rows with fixed continuous Hessian span.

There is a useful subsumption at **full** PSD Hessian span one: express
the quadratic parts as nonnegative multiples of one convex quadratic
form, introduce its epigraph variable, and replace the original rows
by affine inequalities. Del Pia's one-quadratic theorem then applies to
feasibility. This observation does not automatically cover span one of
the continuous blocks alone when integer–continuous cross terms vary.

Khachiyan and Porkolab, *Integer optimization on convex semialgebraic
sets*, Discrete & Computational Geometry 23 (2000), 207–224,
[accessible published text](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf),
provides the foundational integer-witness and first-order-description
complexity bounds used by the manuscript. Their bounds depend on the
quantified block dimensions. Applying the theorem to the original
projection formula with all continuous coordinates quantified therefore
does not establish the proposed result when that dimension grows.
The compressed formulas are the claimed additional ingredient.

Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I:
sampling in real algebraic sets*, [arXiv:cs/0403008](https://arxiv.org/pdf/cs/0403008),
Theorem 1.2, computes exact algebraic samples for a polynomial condition on
a fixed number of complete quadratic-map components. Their parameter
counts affine parts as well as quadratic parts. For example,
\(q_i(x)=\|x\|^2+a_i^Tx+b_i\) has Hessian span one but complete-polynomial
span up to \(n+2\). Independent affine rows also count when encoded
directly. Therefore fixed Hessian span is not an immediate specialization
of the quadratic-map theorem.

Bienstock, Del Pia, and Hildebrand, *Complexity, Exactness, and Rationality
in Polynomial Optimization*, Mathematical Programming 197 (2023),
661–692, [full preprint](https://arxiv.org/pdf/2011.08347), p. 3,
explicitly distinguish fixed-number quadratic algorithms from systems
with arbitrarily many linear inequalities and just two quadratic
inequalities. Thus generic few-quadratic results cannot be transferred
without checking their treatment of affine rows. This is a comparison
of theorem scopes, not a declaration that the present convex question
remains open.

Bienstock, *A note on polynomial solvability of the CDT problem*,
[arXiv:1406.6429](https://arxiv.org/abs/1406.6429), treats a fixed total
number of quadratic constraints, including an ellipsoidal constraint,
through weak feasibility and approximate optimization. Its reported
output and boundedness assumptions differ from exact classification
without input bounds. Neither this difference nor the other searches
establishes priority for the new claim.

## 5. Search and verification record

The audit searched the exact Bank–Mandel book title, Theorem 7.4,
quasiconvex polynomial mixed-integer existence, finite quadratic families,
and continuous Hessian span. It examined the author-hosted Bertsekas–Tseng
paper, the two publisher previews above, the 1988 publisher record, and
the exact-complexity sources in Section 4. A separate agent checked the
complexity comparisons.

Targeted source checks downloaded the 1987 preview to a temporary file,
extracted text with pdftotext -layout, and rendered printed pp. 20, 24,
and 34 with pdftoppm. Visual inspection confirmed the definitions,
Theorem 3(iii), and Theorem 7(ii). Another independent agent read the
surrounding assumptions on printed pp. 18, 20, 23–26, and 31–35, and
confirmed the rational-coefficient application and attainment deduction.
The proof of Theorem 7 is not included in
the preview: these checks verify the published statement and its use,
not the omitted proof. They do not verify the new algorithm. No
project-wide verification or CI inspection was performed.
