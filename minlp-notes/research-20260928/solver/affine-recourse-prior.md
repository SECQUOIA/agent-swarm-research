# Prior-work audit for the affine-recourse rate boundary

Date: 2026-09-28. Independent source and significance audit of
[affine-recourse-rate-boundary.md](affine-recourse-rate-boundary.md).
This audit does not establish publication priority or replace proof review.

The strongest defensible contribution is the sharp `Theta(1/r)` rate for
the stated sparse **full-preordering** hierarchy on a fixed three-variable
problem with affine linear-programming recourse. The qualitative failure
of sparse finite exactness despite a small dense certificate, including
the nonpolynomial separator explanation, already has a very close explicit
precedent. The exact relation between moment matching and uniform
approximation is also established prior work.

## Closest qualitative counterexample

[Nie, Qu, Tang, and Zhang, *A characterization for tightness of the sparse
Moment-SOS hierarchy*](https://link.springer.com/article/10.1007/s10107-025-02223-2),
Example 6.7 (2025 online), considers the same two bags `{x,y}` and `{y,z}`
on `[-1,1]^3`, with

\[
 F=x^2+(xy-1)^2+(yz)^2+(z-1)^2.
\]

The private minima are `1/(1+y^2)` and `y^2/(1+y^2)`, and `F*=1`.
Their argument forces a purported polynomial separator to equal a
nonpolynomial rational function. Meanwhile,

\[
 F-1=(xy+z-1)^2+(x-yz)^2
\]

is a dense degree-four SOS certificate. The full example and its proof
were inspected in publisher HTML and the
[open preprint](https://arxiv.org/html/2406.06882v2).
The paper calls this failure of sparse tightness; its displayed
nonnegative-decomposition obstruction also rules out an exact sparse
preordering representation, independently of the selected local positivity
cone. This last extension is an inference from the proof.

Consequently, neither the two-bag construction nor the qualitative
sparse/dense contrast should carry the novelty claim. The candidate's
addition is quantitative: a nonsmooth recourse value produces an
inverse-degree obstruction, with an explicit certificate proving the
matching upper exponent. The cited example uses smooth rational values
and gives no quantitative lower rate there.

## Exact moment-matching duality and the absolute-value rate

[Han, Jiao, and Weissman, *Local moment matching: A unified methodology for
symmetric functional estimation and distribution estimation under
Wasserstein distance*](https://proceedings.mlr.press/v75/han18b/han18b.pdf),
Lemma 25, pp. 23–24, explicitly identifies twice the best uniform polynomial
approximation error with the maximum expectation difference between two
probability measures matching moments through the polynomial degree.
Its stated interval is positive, but translation gives the candidate's
`[-1,1]` case without changing degree. The same passage applies the result
to a translated absolute value. Thus even the combination of moment
matching, the factor two, and an absolute-value function is established.

[Wu and Yang, *Minimax rates of entropy estimation on large alphabets via
best polynomial approximation*](https://arxiv.org/pdf/1407.0381),
Appendix E, is an earlier direct reference for this duality. The paper's
introduction and Appendix B discussion of equation (34) were inspected;
they explicitly attribute lower-bound constructions to the dual of best
polynomial approximation. This audit does not claim either statistics
paper originated the functional-analytic theorem.

[Bernstein, *Sur la meilleure approximation de |x| par des polynomes de
degrés donnés*](https://history-of-approximation-theory.com/fpapers/acta37.pdf),
*Acta Mathematica* 37, 1–57 (1914), proves the inverse-degree behavior and,
in Section 36, the existence of the positive limit
`beta=lim_(r->infinity) 2r E_(2r)(|x|)`. The introduction and Section 36
were inspected. The issue is sometimes dated 1913 from its printing date;
1914 is the journal metadata used here. Therefore the candidate's exact
local-measure identity yields, as a direct consequence of classical
approximation theory,

\[
 -\eta_{2r}=2E_{2r}(|y|)\sim\beta/r.
\]

This asymptotic is for the **ideal local-measure** relaxation. It does not
identify the leading constant of either finite sparse SDP gap. The
candidate's elementary Fejer witness is useful as a self-contained lower
bound, but inverse-degree approximation of the absolute value is not new.

## Polynomial separator messages and sparse rates

[Fix and Agarwal, *Duality and the Continuous Graphical
Model*](https://www.cs.cornell.edu/~afix/Papers/ECCV14.pdf), ECCV 2014,
already approximates continuous marginal-LP dual messages by polynomial
and piecewise-polynomial functions. Theorem 2 gives an
`O(ML/(dK))` approximation error for Lipschitz potentials, degree `d`, and
`K` pieces, using Jackson approximation of Lipschitz dual variables. The
statement and appendix proof were inspected. Its assumptions concern
finite Lipschitz potentials on product domains; a hard affine recourse
constraint is not directly such a potential. It also does not prove a
matching lower bound for the candidate's finite SOS cones. It is strong
prior for the message-approximation interpretation and the motivation for
piecewise messages.

[Korda, Magron, and Rios-Zertuche, *Convergence rates for sums-of-squares
hierarchies with correlative
sparsity*](https://d-nb.info/1330825241/34), 2024 online/2025 volume,
establishes sparse polynomial convergence rates. Section 3 approximates
separator minimum-value functions by polynomials to construct positive
bag polynomials. Theorem 6 concerns full-box sparse preorderings; Theorem
8 treats more general constrained problems through quadratic modules.
These are upper-error guarantees, with no matching fixed-example
inverse-degree lower bound located in the inspected passages. The
candidate's second bag is a triangle rather than a product box, so its
rate does not contradict a faster box theorem. See also the existing
[kernel audit](kernel-prior.md) for the precise rate and degree comparison.

[Lasserre, *Convergent SDP-Relaxations in Polynomial Optimization with
Sparsity*](https://optimization-online.org/wp-content/uploads/2006/04/1367.pdf),
Theorem 3.6, provides the foundational convergence result under running
intersection and local compactness certificates. The repository's
[source record](../../literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/paper.md)
and relevant local full-text passages were inspected. Two bags with one
shared coordinate satisfy running intersection, so the candidate concerns
the speed and finite-order limitations of an asymptotically convergent
construction.

## Significance and limits

The following is this audit's assessment of the candidate, rather than a
claim made in the cited papers.

The example supplies a useful rate boundary for attempts to extend the
repository's inverse-square partial-rounding theorem to shared-dependent
private feasible sets. Its lower bound survives replacing local SOS tests
by exact local measures. That separates a limitation of finite polynomial
separator information from weakness in local positivity certificates.
The matching upper certificate makes this stronger than a qualitative
counterexample or an approximation-theoretic analogy.

The result is a focused theoretical contribution. By itself it does not
establish a substantial general advance in MINLP solving. It gives no
complexity lower bound for the original optimization problem, which is
elementary, and its dense relaxation is already exact at order two.
There are no integer variables in the stated version. The opposite private
value functions cancel for every separator value; robustness under
perturbation, uniqueness of a minimizer, and general recourse value
functions remain unstudied here. Those properties should not be inferred
from this example.

Splitting at the kink, adding an exact value-function statistic, or merging
bags has a sound explanation in this example. A useful adaptive solver
policy still needs a way to detect the relevant separator obstruction,
account for the cost of a richer representation, and show improved bounds
or useful performance on a broader class. These remain research prospects.

Suggested claim: “We give a fixed three-variable affine-recourse instance
whose sparse full-preordering gap is of exact inverse-order magnitude,
although a dense degree-three certificate is exact. The lower bound
already holds with exact local measures and is obtained by established
moment-matching/approximation duality.” Avoid a claim of first discovery
until a broader citation-descendant search is completed.

## Search and verification record

Searches included `sparse finite convergence counterexample polynomial`,
`sparse Positivstellensatz nonnegative counterexample`, `sparse Moment-SOS
rate lower`, `correlative sparsity absolute value`, `sparse preordering
lower bound approximation`, and `moment matching best polynomial
approximation duality absolute value`. Exact formula and terminology
variants were also searched. They found the close rational-separator
counterexample and the exact moment-matching duality. No identical
three-variable affine-LP example or matching sparse-preordering lower-rate
theorem was located. This negative search result does not establish
novelty.

Local actions were limited to reading the candidate and two existing
prior-work notes, locating source records with `rg --files`, and reading
the local Lasserre source using `sed` and `rg`. Web inspection covered the
primary sources linked above. No project-wide checks, CI inspection,
computational proof verification, or Lean checks were performed in this
literature audit.
