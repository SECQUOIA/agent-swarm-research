# Literature status of the irrational-zero convex quartic

Date checked: 2026-09-28. Status: independent primary-source audit of the
explicit example and the stated open question. Publication priority is
not established. This note does not duplicate the
[general realization audit](general-quartic-realization-prior.md) or
recheck the construction's full proof.

The [explicit integer quartic](convex-quartic-irrational-zero.md) has
minimum zero only at $(\sqrt[3]{2},\sqrt[3]{4})$, and its Hessian is
uniformly positive definite on all of $\mathbb R^2$. Subject to its
separate proof verification, it disproves the existence of rational
feasible-point witnesses for every nonempty zero sublevel of a globally
convex rational quartic. The sources inspected here did not supply an
earlier example with these combined properties. That search finding
does not establish priority or that nobody has already resolved the
question.

## The exact question and version status

The [arXiv record of Slot, Steurer, and Wiedmer](https://arxiv.org/abs/2511.03440)
listed only v1, submitted 5 November 2025. In
[Section 1.3 and Table 1](https://arxiv.org/html/2511.03440v1#S1.SS3),
problem (D) asks whether $f(x)\leq0$ for some $x$ in a rational
polyhedron. A compact witness means a rational feasible point of
polynomial bit length. The convex-quartic row lists this witness
question as unknown, separately from the unknown complexity of (D).
[Appendix C](https://arxiv.org/html/2511.03440v1#A3) gives an irrational
quartic minimizer, a convex sextic with an irrational unique zero, and
Lemma C.3 ruling out such a zero for a univariate convex quartic.
The lemma does not cover two variables. Corollary 1.2 concerns
approximation.

The [authors' publication page](https://www.lucasslot.com/publications)
and [Wiedmer's page](https://www.manuelwiedmer.ch/) also list a
[STOC 2026 proceedings version](https://doi.org/10.1145/3798129.3800760).
Its text was not obtained: the independent citation search encountered
an ACM HTTP 403, and the
[ETH repository DOI](https://doi.org/10.3929/ethz-c-000802388)
was inaccessible through the browser and returned HTTP 429 in a direct
request. Therefore this audit does **not** assert that the proceedings
table is identical to arXiv v1. The inspected author lists showed no
separate quartic rational-witness follow-up; author lists need not be
complete or current.

## The closest earlier results

**Bienstock, Del Pia, and Hildebrand (2020), Example 1 and Observation 3.**
Their [primary manuscript](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf),
Section 3, printed page 9, gives

\[
h(x,y)=2x^3+y^3-6xy+4
\]

with its unique zero-level feasible point on the rational rectangle
$R_0=[1.259,1.26]\times[1.587,1.59]$ equal to
$(\sqrt[3]{2},\sqrt[3]{4})$.
This is close prior for both the point and the rational zero level.
Moreover, direct differentiation shows that $h$ is strongly convex
on this rectangle:

\[
\nabla^2h=\begin{pmatrix}12x&-6\\-6&6y\end{pmatrix},\qquad
\det\nabla^2h=72xy-36>0\quad\text{on }R_0.
\]

The last observation is an inference from their displayed polynomial,
checked independently here. Its Hessian at the origin is indefinite.
Thus convexity only on a bounded feasible domain already permits this
arithmetic phenomenon. Global convexity of the polynomial is an
essential qualification of the new example.

**Ahmadi and Parrilo (2013), Theorems 5.1 and 5.6 in the arXiv text.**
The [primary proof](https://arxiv.org/pdf/1111.4587), Section 5.1,
establishes that every convex bivariate quartic polynomial is
SOS-convex, over real coefficients. Theorem 5.6 works directly with the
Hessian biform. Therefore real SOS-convexity of a convex bivariate
quartic is already guaranteed by prior theory. The explicit
[rational Hessian certificate](convex-quartic-rational-sos.md)
adds a concrete exact certificate for this example; the general
equivalence alone does not provide that particular rational certificate
or an irrational-zero construction. Remark 5.1 also warns that
homogenizing a convex polynomial need not preserve convexity.

The newer [Ahmadi, Blekherman, and Parrilo paper](https://arxiv.org/pdf/2404.14440)
proves the corresponding theorem for homogeneous ternary quartics.
Its introduction, main statement, and rational-certificate discussion
were inspected. It does not state an irrational-zero example for a
globally convex rational polynomial. The homogeneous and
nonhomogeneous assertions should not be conflated.

## Later papers and citations inspected

**Ahmadi and Hall, On Approximate Computation of Critical Points (2026).**
The [arXiv record](https://arxiv.org/abs/2601.21917) and
[primary manuscript](https://optimization-online.org/wp-content/uploads/2026/01/Approx_Crit_Point_Ahmadi_Hall.pdf)
were checked. Section 4, printed page 18, cites Slot et al. for efficient
approximate and near critical points of fixed-degree convex
polynomials. Its discussion asks for other tractable function classes.
The inspected citation and surrounding statements do not address exact
rational witnesses. Searches for “rational” and “irrational” were used
to locate potentially relevant passages; absence of a word is not proof
that an equivalent theorem is absent.

**Zhou, Liu, Nie, and Tang, A Tight SDP Relaxation for the Cubic-Quartic
Regularization Problem (published 21 August 2026).**
The [primary article](https://link.springer.com/article/10.1007/s10107-026-02413-6)
studies a quadratic plus multiples of $\|s\|^3$ and $\|s\|^4$.
The introduction and Remark 4.2(iii) cite Slot et al. for convex
polynomial optimization; Reference 45 names the STOC version.
The inspected abstract, model, citation contexts, and Example 3.5 do
not give the desired rational-witness counterexample. Example 3.5
does display $(\sqrt2,\sqrt2)$ as a minimizer with minimum zero, but
also has the rational minimizer zero and infinitely many minimizers.
Its nonzero $\|s\|^3$ term is not polynomial. Neither that example nor
SDP exactness alone yields the present claim.

**Zhu and Cartis, Sufficiently Regularized Nonnegative Quartic
Polynomials are Sum-of-Squares.**
The [current arXiv record](https://arxiv.org/abs/2601.20418) lists v2,
dated 2 April 2026. The [v2 text](https://arxiv.org/html/2601.20418v2),
Section 2.1 and Theorem 2.1, constructs an SOS representation of
$m_3(s^*+v)-m_3(s^*)$ under a matrix positivity condition.
Section 2.3 discusses large regularization and convexification.
The inspected statements do not ensure rationality after subtracting
the minimum or translating by $s^*$, and do not specify an irrational
zero for a rational globally convex quartic. This updates the
previous local audit, which inspected v1.

**Naskar and Singh, Convexity and SOS-Convexity of Sum of Separable and
Biquadratic Quartic Polynomials and Optimization (26 July 2026).**
The [primary v1 text](https://arxiv.org/html/2607.23476v1), abstract,
Section 3, and Theorems 3.1–3.2 concern a homogeneous quartic example
claimed convex but not SOS-convex. Its displayed polynomial vanishes
at the rational point zero. The inspected statements and occurrences
of “rational” do not address irrational zero-level witnesses.
This is a relevance check, not an independent verification of that
paper's mathematical claims.

## Search scope and safe wording

Searches covered the paper's arXiv identifier, title and authors, and
combinations of convex quartic, rational witness, irrational zero,
rational minimum, strong convexity, and SOS-convexity. Both exact
phrase searches and broader unquoted searches were used; some exact
phrase searches returned mostly irrelevant algebraic-geometric or
literary results. Those results were not evidence of novelty.
A separate agent followed citations and checked author lists.
Semantic Scholar was rate-limited; OpenAlex returned no citations for
the arXiv record despite the two later citing papers located directly.
Citation-index counts were therefore not treated as exhaustive.

The supported formulation is:

> The explicit example answers negatively the compact rational
> feasible-point witness question stated in Table 1 of
> Slot–Steurer–Wiedmer, arXiv:2511.03440v1. The inspected literature
> did not reveal an earlier resolution; publication priority remains
> unestablished.

This resolves that mathematical statement regardless of priority.
It supplies no hardness result and no exclusion of NP membership or
short certificates in other representations. It also does not conflict
with rational approximate witnesses. The proof and formal-verification
scope remain those in the linked construction and certificate notes.

## Targeted checks

An inline `python - <<'PY'` SymPy check independently differentiated
the older cubic, verified its Hessian determinant, checked the exact
positive lower determinant bound $13482297/125000$ on $R_0$, and
verified the negative determinant at the origin. It passed.
A separate standard-library Python check on this file verified its
final newline, whitespace, mathematical delimiters, and relative links.
`git diff --check -- research-20260927/quartic-latest-status-prior.md`
also passed; the direct whitespace check covers this newly added file.
No project-wide verification or CI inspection was run.
