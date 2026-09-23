# Independent review: many constraints in a three-dimensional span

Date: 2026-09-22. Reviewed
[the research note](research-20260922-span-three-many.md) independently during
the closeout of existing topics. No new extension was pursued.

## Verdict

The directional bound `2|J_-(D)|`, its conditional consequence `2k-2`,
and the centered-ellipsoid family requiring exactly `k` strict aggregation
rays are correct under the stated hypotheses. They are useful supporting
observations. The note appropriately does not claim an unconditional
improved upper bound, sharpness of either general upper bound, or a major
novelty result.

The proof should explicitly recall why hidden hyperplane convexity (HHC)
holds: choose a basis of the three-dimensional matrix span containing a
positive-definite combination. Since `n>=3`, restrictions to homogenized
hyperplanes have dimension at least three. Calabi's convexity result and
linear images give HHC for the complete original family. This supplies the
hypothesis of the cited strict aggregation results.

## Proof audit

**Coefficient cone.** Fix `x0 in S` and let
`a(M)=(x0,1)^T M (x0,1)`. Every nonzero nonnegative combination of original
generators has negative evaluation. In particular, no nontrivial such
combination is zero, and `K` contains no line. It is a full-dimensional
pointed cone in `L`. A transverse polygon section shows that its number of
facets equals its number `k` of extreme rays. Removing generators that lie
in the cone of the retained generators preserves the strict feasible set.

**Directional exit.** A positive-definite `D` cannot lie in `K`, by
evaluation at `x0`, so at least one inward facet functional is negative on
`D`. For each nontrivial good matrix `M`, the displayed minimum defining
`t_*` is finite and nonnegative. Facets with nonnegative value on `D`
remain satisfied, and the others remain satisfied precisely until their
individual exit times. Consequently `M_*` lies in a selected facet of
`K`. It cannot vanish: for positive `t_*`, that would make `M` negative
definite, inconsistent with its single negative eigenvalue in matrix
dimension at least four; for zero `t_*`, it would make `M` zero.

The coefficient representations cause no hidden difficulty. Choose
nonnegative vectors `lambda,mu` representing `M,M_*`, respectively, and
put `theta=mu-lambda`. Then `Q_theta=t_*D` is PSD and
`lambda+theta=mu` is admissible. This is exactly the PSD-improvement
operation. Thus every original good cut is dominated by a good cut on a
selected facet. The intersection of the selected facet cuts both contains
the hull and is contained in the intersection of all good cuts.

Each facet has two extreme generators. Applying the pair-support endpoint
reduction with goodness defined relative to the original full set reduces
its intersection to at most two cuts. No subsystem convex hull is used.
Empty sets of good facet cuts contribute nothing. Summing the resulting
upper bounds proves `2|J_-(D)|`.

**Conditional improvement.** If a PSD `E` lies outside `-K`, one inward
functional is positive on `E`. For sufficiently small positive `delta`,
`E+delta D0` is positive definite and retains this positive value. At
least one facet is therefore absent from `J_-`, yielding `2k-2`. This
argument does not require closed-set regularity or assumptions at infinity.

**Lower family.** For increasing parameters `a<b<c`, the determinant of
the rows `(a,1-a^2,-1)`, `(b,1-b^2,-1)`, `(c,1-c^2,-1)` is
`(b-a)(c-a)(c-b)`. Hence the span is precisely the displayed diagonal
three-dimensional space and includes a positive-definite homogeneous form.
The witness identity is correct. At `p_i`, every aggregation not supported
solely on index `i` is strictly negative. Since `p_i` is excluded from the
open feasible set, every exact strict aggregation family must contain ray
`i`, even if the family is infinite. The original `m` inequalities give
the matching upper bound. The same witness separates each generator from
the cone of the others, proving `k=m`.

For a finite nonstrict description, strict slack in all cuts omitting ray
`i` persists on a neighborhood of `p_i`. Radially dilating `p_i` slightly
produces a point with `f_i>0`, proving the stated contradiction. The
qualification concerning infinite nonstrict families is necessary.

## Prior work and limits

I opened the [BDS author PDF](https://www2.isye.gatech.edu/~sdey30/HHC.pdf)
and checked its relevant statements and proofs. That PDF identifies itself
as **arXiv:2210.01722v1**, dated October 2022. Its relevant numbering is
Propositions **2.21, 9.1, and 9.6**. The note's numbering is correct for
this version; a reader should not assume identical numbering in every
version. BDS already supplies the facet-based `2m` argument, PSD
improvement, and the two-generator endpoint reduction. The directional
count is a refinement of that existing reasoning.

I also checked [BD arXiv v1, Section 8](https://arxiv.org/html/2405.18282v1),
especially Propositions 8.6 and 8.10. The former provides the antecedent
directional geometry for three generators. The latter treats the
complementary case under its closed-set hypotheses and does not establish
the general-cone strict statement left open in the note. These comparisons
support the note's modest classification; they do not establish novelty.

The statement that a suitable generalization of the complementary theorem
would imply an unconditional strict `2k-2` bound should be read as a
research implication requiring both the general-cone theorem and a valid
transfer from its closed hypotheses. It is not a proved consequence of the
current closed theorem alone.

The three listed failed shortcuts are correctly rejected. In particular,
intersection does not commute with convex hull, goodness is relative to
the full feasible set, and matrices with one negative eigenvalue need not
remain in that inertia class after addition. None closes the remaining
case. That case remains unresolved here.

## Targeted verification

I ran a standalone `python3` heredoc using `fractions.Fraction`, with
parameters `a_i=i/(m+1)` for `m=3,...,30`. It checked:

- all **9,450** boundary identities and their strict sign patterns;
- all **31,465** three-row determinants against the positive Vandermonde
  product.

Both sets passed. These checks verify the listed rational instances;
the algebraic proof covers arbitrary distinct parameters in `(0,1)`.
The directional bound was checked mathematically against its hypotheses
and cited lemmas, not computationally or in Lean. No project-wide checks
or CI inspection were performed. The source note was not edited during
this review.
