# Stage 6 primary-source and priority audit

Date: 2026-09-22. This record concerns the four-aggregation PDLC stage.
It is not part of the submission manuscript. No managed literature package
or other repository topic was changed.

## Published four-bound and its precise input

Read the locally downloaded primary PDF and complete text of
[Blekherman–Dunbar, arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1),
including the opening definitions, Theorem 1.4, Proposition 3.15's proof,
and the final proof of Theorem 1.4 in Section 8. The PDF and extraction
are `/tmp/quadratic-paper-literature/bd.pdf` and `bd.txt`.
Fresh online retrieval of that version also succeeded.

The standing setup assumes linearly independent homogeneous matrices.
Theorem 1.4 requires signed PDLC, nonempty interior of the nonstrict set,
equality to the closure of that interior, and no points at infinity.
Permissibility means at most one negative homogeneous eigenvalue.
No smooth spectral curve is assumed in Section 8. The final theorem proof
explicitly uses Proposition 8.7 for n=1,2 and Proposition 8.10 for n>=3;
Proposition 8.6 handles the other hyperbolicity-cone case. The manuscript
therefore applies this input in every positive dimension, rather than
inferring that scope from an omitted restriction.

The journal article is SIAM Journal on Applied Algebra and Geometry 9(2)
(2025), 310–342, DOI 10.1137/24M1668445. A fresh attempted opening of the
[publisher's author eprint](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full)
failed. The earlier repository priority audit successfully inspected the
published version and records the same Theorem 1.4 hypotheses. This stage's
independent primary inspection is of arXiv v1. Its Section 8 locators must
not be described as the journal's Section 7 locators.

Proposition 3.15 already uses limits of oriented negative eigenvectors for
a fixed feasible set. The manuscript credits this antecedent. Its new
argument couples such a limit with compact inward systems that eventually
contain every fixed finite subset of the original strict feasible set.
The topological theorem is credited as an external input, not reproved or
claimed as a new theorem of this paper.

## BDS upper bound, sharpness, and closed-set counterexample

Read the local primary BDS author manuscript as context and the downloaded
[arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2) PDF and extraction
for versioned result statements. Fresh online retrieval of v2 succeeded.
The v2 Corollary 2.20 gives the six-bound, Example 2.21 gives the credited
four-necessary construction, and Conjecture 3.2 asks for a six-necessary
strict PDLC example. The manuscript independently proves that every exact
good family for their example must contain its four rays. Combining this
necessity with the new upper bound supplies the displayed hull description;
no unproved geometric assertion from the example is an input.

The half-ball counterexample is **Example 2.23 in v2**, not Example 2.22
as the canonical repository note currently says. Section 08 uses 2.23 and
adds a redundant negative-definite homogeneous constraint to enforce PDLC.
All numerical locators in the paper remain tied to the cited v2.

## Dissertation priority

Read the complete public reader extraction already saved outside the repo
at `/tmp/dunbar-thesis-priority.txt`, especially Theorem 5.0.5 on printed
page 97, its proof on pages 124–126, and Propositions 5.3.12 and 5.3.13 on
pages 121–122. The official [Emory record](https://etd.library.emory.edu/concern/etds/vq27zq10w)
and search-indexed primary PDF corroborate the title, author, year, and
the stronger theorem statement. Direct fresh openings of the record and
[original PDF](https://etd.library.emory.edu/downloads/2j62s637x?locale=en)
failed; the original PDF was not visually inspected by this stage author.

Theorem 5.0.5 states the regular nonstrict four-bound without the infinity
condition. Its proof invokes Propositions 5.3.12 and 5.3.13, which explicitly
assume that condition in the retrieved complete text. Some mathematical
glyphs in the extraction are damaged. This is a documented discrepancy
in the accessible evidence, not an established author correction or a
definitive allegation about the original PDF. The manuscript acknowledges
the stronger prior statement without relying on it or discussing a
possibly omitted assumption as an established error. Its proof uses the
fully qualified published result only.

Fresh searches included `"four" "strict" "aggregations" "PDLC"` and the
exact dissertation title. These retrieved the primary dissertation and
existing BD material but did not establish a prior universal strict
transfer. Search non-discovery does not establish priority. The qualified
claim is limited to the complete transfer to arbitrary strict systems,
including dependent triples. It does not claim the first four-bound or
the first statement removing an infinity hypothesis.

## Dependent triples and the classical two-bound

Freshly inspected the accepted author text of
[Yildiran (2009)](https://www.researchgate.net/publication/220386378_Convex_hull_of_two_quadratic_constraints_is_an_LMI_set),
Section 3.2, Assumption 1, and Theorem 1. Nonemptiness is the relevant
assumption; the author uses strict positive inequalities and at most one
positive eigenvalue, the negatives of this paper's conventions. His hull
description uses at most two endpoint aggregations when the hull is proper.
The manuscript reproves the finite cone reduction of a dependent triple to
at most two original generators before invoking this theorem. The same
reduction appears in BDS v2 Section 2.5 after Example 2.21 and is explicitly
credited there. The conic representation principle is also recorded in
BDS v2 Remark 2.19 and is credited separately from the new bound of four.
That optional
improvement is not an input to the all-dimensions four-bound.

## Scope of the contribution

The stage supplies a complete transfer: independent positive definite
perturbations, compactness from the absence of a common strictly negative
leading direction, countably many exceptional regular levels, deletion
of globally nonpositive quadratics before strictification, and fixed-size
multiplier limits with controlled negative components. It also gives the
oriented SOC closure formula and rechecks the credited sharpness example.
It makes no general nonstrict-system theorem, multiplier algorithm,
coefficient-size bound, solver performance claim, or optimal bound in
dimensions one and two.
