# Prior-art and significance audit of the quadratic-path construction

Date: 2026-09-27. Independent review of
[structure-frontier.md](structure-frontier.md), including the revised width-two
repair. This is a focused literature and mathematical audit, not an originality
certificate.

The exact threshold is a useful candidate quantitative result. Its qualitative
message is already known: a path decomposition can lose finite exactness that a
slightly larger bag recovers at order two. The candidate's defensible distinction
is a **constant objective gap until an exponentially large order**, with quadratic
data and coefficients from a fixed finite set. No inspected source states that
particular combination. That search outcome does not establish novelty.

## Closest overlap: a path with no finite sparse exactness

Nie, Qu, Tang and Zhang, *A characterization for tightness of the sparse
Moment-SOS hierarchy*, Mathematical Programming 215 (2026), 369–405, online
2025, [published article](https://link.springer.com/article/10.1007/s10107-025-02223-2),
[arXiv v3](https://arxiv.org/pdf/2406.06882v3), Theorems 3.1–3.2 and Example 6.7,
were inspected in full at those locations.

Their Example 6.7 minimizes

\[
 x_1^2+(x_1x_2-1)^2+(x_2x_3)^2+(x_3-1)^2
\]

on the unit box, using bags `{1,2}` and `{2,3}`. The optimum is one.
The sparse hierarchy is not finitely tight, whereas the dense order-two
certificate is

\[
 f-1=(x_1x_2+x_3-1)^2+(x_1-x_2x_3)^2.
\]

The obstruction is that an exact separator polynomial would have to equal
`−1/(1+x_2^2)` throughout the interval. Thus width one versus width two,
bounded domains, fixed coefficients, and an extreme finite-exactness separation
are already present. The present candidate adds quadratic rather than quartic
input, an exact exponential threshold, and a gap of two below it. It does not
first establish that a wider decomposition can be dramatically stronger.

## The witness is classical Gaussian/Lobatto quadrature

Let `q=N/2`. After repeated cosine values are combined, the candidate's negative
law has nodes

\[
 \cos\frac{(2j+1)\pi}{2q},\quad 0\le j<q,
\]

each with weight `1/q`. Its positive law has nodes `cos(j pi/q)`, `0<=j<=q`,
with endpoint weights `1/(2q)` and interior weights `1/q`. These are precisely
normalized Chebyshev–Gauss and Chebyshev–Gauss–Lobatto quadratures for the
arcsine law. Both have exactness through degree `2q−1=N−1`. The explicit
weights and degrees are recorded, for example, in the numerical-analysis
documentation for [Gauss–Lobatto–Chebyshev quadrature](https://dealii.org/9.7.0/doxygen/deal.II/classQGaussLobattoChebyshev.html)
and the formulas in [NIST DLMF §3.5](https://dlmf.nist.gov/3.5).

The candidate's Fourier proof independently establishes the needed identity,
so it does not depend on a numerical quadrature routine. The embedding of this
pair into two composition chains is the part requiring novelty comparison;
neither the quadrature pair nor its moment matching is new.

Han, Jiao and Weissman, *Local moment matching*, COLT 2018,
[Lemma 25](https://proceedings.mlr.press/v75/han18b/han18b.pdf), equates twice
the best uniform degree-`K` approximation error with the largest difference
of expectations over two probability laws matching moments through `K`.
The stated interval has positive left endpoint; an affine change of variables
gives the version on `[-1,1]`. This supplies the general background mechanism.

## Composition chains and state lifting are established

Balada Gaggioli, Henrion and Korda, *Composition and tensor train structure in
polynomial optimization*, [arXiv:2604.17563v1](https://arxiv.org/pdf/2604.17563v1),
April 2026, was inspected at §§2.1.1, 4–5 and 7.1.

Their state-lifting chordal hierarchy introduces intermediate variables for
polynomial compositions; their push-forward hierarchy moves the composition
into moment consistency constraints. Theorems 4.1 and 5.3 prove asymptotic
convergence. Sections 4.3 and 5.2 count block sizes and coupling equations at
fixed order; they do not provide a uniform bound on the order needed to attain
a given accuracy. Section 2.1.1 explicitly uses repeated squaring. Section 7.1
uses degree-four Chebyshev controls in a Markov-chain example.

The candidate therefore cannot claim the general idea of exploiting low
dimensional compositional states. It may supply a useful worst-case
qualification: fixed local state size, degree and coefficients do not by
themselves bound the useful order of a prescribed sparse decomposition. The
candidate's width-two repair instead retains correlations between the two
synchronized states; the scalar edge decomposition discards them.

## Sparse convergence rates do not give a conflicting uniform bound

Korda, Magron and Ríos-Zertuche, *Convergence rates for sums-of-squares
hierarchies with correlative sparsity*, Mathematical Programming 209 (2025),
435–473, [published full text](https://link.springer.com/article/10.1007/s10107-024-02071-6),
Theorems 6 and 8 and equations (23)–(24), were inspected.

Theorem 6 concerns positivity on the whole box, so it does not directly certify
`F−1` only on the quadratic equality set. Theorem 8 covers general domains
under normalization, sparse Archimedean representations and local error
bounds. Its constants explicitly include

\[
 3^{((16+8\ell)\mathsf L_j+2)/3}
 \quad\text{and}\quad
 3^{\ell(\mathsf L_j+1)+(2\mathsf L_j+|J_j|+2)(1+8\mathsf L_j/3)}.
\]

Consequently their bounds already allow exponential dependence on the number
`ell` of cliques even with fixed local parameters. Clique-size-dependent
accuracy exponents are not uniform complexity bounds over growing families.
The candidate shows that polynomial dependence on chain length cannot simply
replace all such dependence in a theorem for this architecture. It does not
prove those displayed constants, or their exponential bases, optimal.

The unversioned arXiv PDF obtained in this audit was v1, where the corresponding
theorems are numbered 2 and 4. The statements above use the published version.

## Further comparisons

Lasserre, *Convergent SDP-relaxations in polynomial optimization with sparsity*,
[2006 manuscript](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf),
Assumptions 3.1–3.2, Theorems 3.6–3.7 and their proofs, supplies the foundational
running-intersection convergence theorem and an overlap rank-one exactness
test. Theorem 3.6(a) gives asymptotic convergence without a uniform order bound.
Its part (b) has a nonempty-interior assumption for strong duality, which does
not apply directly to the candidate's equality set. The candidate's explicit
primal witnesses and dual certificate avoid relying on that part.

Waki, Kim, Kojima and Muramatsu,
[*Sums of squares and semidefinite program relaxations for polynomial
optimization problems with structured sparsity*](../literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md),
§5.4, already discuss expanding multiplier supports, including unions of small
cliques, to strengthen sparse relaxations. Thus choosing additional
correlations is an established solver design principle. The quantitative
consequence in this candidate is the potential contribution.

Nie and Demmel, [*Sparse SOS relaxations for minimizing functions that are
summations of small polynomials*](https://people.eecs.berkeley.edu/~demmel/Demmel_pubs_07_11_final/J78_Sparse_SOS_Relaxations.pdf),
2009, Remark 3.4 and Example 3.5, already show a numerical sparse/dense gap
on a three-variable path with quartic objective. A caution about the inspected
manuscript's Theorem 3.3: its proof passes from equality of truncated overlap
moments to equality of representing-measure marginals without an explicit
determinacy assumption. That implication is false in general, as the classical
quadrature pair itself shows. This identifies an unjustified proof step; it
does not by itself refute the complete theorem, whose additional optimization
hypotheses would need a separate counterexample. This review does not use it.

Bienstock and Muñoz, [*LP formulations for polynomial optimization
problems*](https://arxiv.org/pdf/1501.00288), Theorems 4 and 15, §2.0.3 and
Appendix A, gives bounded-treewidth LP approximations with coefficient-scaled
constraint violation and objective tolerance. Appendix A uses subset-sum
reductions to explain limitations of stronger tolerance guarantees. Exact
preservation of the candidate's hard quadratic dynamics is not promised.
This is not a stronger or faster algorithm than theirs; it is a lower bound
for a different, fixed relaxation architecture.

Fantuzzi and Fuentes, [*Finite convergence and minimizer extraction in moment
relaxations with correlative sparsity*](https://arxiv.org/pdf/2502.01410v3),
July 2026, Theorem 1.1, Corollary 1.2 and Lemma 3.3, use flatness of both clique
and separator moments to obtain a global representing measure. Actual local
measures alone do not meet those hypotheses. In the candidate, below-threshold
central moments agree while the underlying central laws differ. Thus no
contradiction with sparse extraction follows.

Gribling, Polak and Slot, [*A note on the computational complexity of the
moment-SOS hierarchy for polynomial optimization*](https://arxiv.org/pdf/2305.14944),
studies bit complexity at fixed relaxation order. Its repeated-squaring
examples and conditioning issues are another reason not to identify SDP
matrix size with certified solver running time. It does not supply the
candidate's hierarchy-order threshold.

## Independent assessment of the candidate's scope

Theorem 1's lower witness is feasible for actual local measures, so the
obstruction survives any strengthening that only restricts individual bags
to their exact feasible moment sets. It also survives changing the polynomial
basis while preserving the same degree span. Neither observation rules out
adding nonlocal derived equalities or selected higher-degree observables.

The threshold proof uses only transmission of a terminal *mean*; propagating
a terminal square would double the apparent degree and yield an unnecessary
factor of two. I checked this degree distinction and the quotient bound
`deg q<=2s−2`. The revised three-variable bags transfer the degree-four square
of an equality residual on a paired separator. Their PSD and quadratic-box
arguments stay within order two. This review found no gap in those arguments,
but it is not formal proof checking.

The optimization instance itself is easy: both chains compute the same
polynomial, and common-subexpression elimination or a synchronization proof
removes the difficulty. There is no integer decision or demonstrated hard
application. The result concerns the architecture's information loss, not
intrinsic optimization complexity.

My significance assessment is **a potentially useful sharp limitation theorem
or short theoretical note, with originality still unestablished**. It should
not yet be presented as the substantial solver advance requested by the
research goal. More consequential next steps would need an independently
novel theorem selecting sufficient cross-chain information, or a lower bound
that survives a meaningful class of automatic reformulations. Generic advice
to enlarge bags or propagate states is insufficient, given the sources above.

## Search and verification record

The review searched combinations of “correlative sparsity”, “sparse moment”,
“exponential degree”, “lower bound”, “Chebyshev”, “chain”, “composition”,
“clique merging”, and “finite convergence”, then followed the relevant
references. Search results about sparse random Boolean instances were not
treated as lower bounds for correlative sparse continuous hierarchies.

Downloaded sources and `pdftotext -layout` extracts are retained in
[sources-chebyshev](sources-chebyshev/). The local Waki full text and previous
[separator review](../notes/research-20260922-separator-novelty.md) were also
examined. Some additional retrieved papers were screened without reading all
their proofs; retrieval alone is not recorded as a theorem-level review.

No numerical SDP, project-wide check, CI inspection or Lean check was run for
this literature audit. The verification here consists of reading the stated
proofs, checking exact algebraic degree accounting, identifying an equivalent
quadrature formulation, and comparing specific prior assumptions and
conclusions.
