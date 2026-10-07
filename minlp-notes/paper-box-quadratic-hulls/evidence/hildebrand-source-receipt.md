# Supplied-source confirmation: rank-one subtraction

The designated shared literature workflow supplied this confirmation on
6 October 2026. This manuscript session did not run a literature command
or modify the literature KB to obtain it.

The checked original is Roland Hildebrand, *Minimal zeros of copositive
matrices*, arXiv:1401.0134v4. Definition 2.1 is on page 2; Lemma 4.3 is
on page 8. A zero is a nonzero nonnegative vector `u` with `u^T A u=0`.
Irreducibility with respect to a set of copositive matrices means that
no positive multiple of a nonzero matrix in that set can be subtracted
while preserving copositivity.

Lemma 4.3 applies to a copositive matrix `A` and an arbitrary nonzero real
vector `w`, without a sign or support restriction. It says that `A` is
irreducible with respect to `ww^T` if and only if some zero `u` satisfies
`w^T u != 0`. Its complement is exactly the criterion used in Appendix F:
there is an `epsilon>0` with `A-epsilon*ww^T` copositive if and only if
`w^T u=0` for every zero. The choice of epsilon can depend on `(A,w)`;
no uniform bound is used or asserted.

The supplied Crossref DOI check confirms the published citation:
Roland Hildebrand, “Minimal zeros of copositive matrices,” *Linear Algebra
and its Applications* **459** (2014), 154–174,
DOI [10.1016/j.laa.2014.07.004](https://doi.org/10.1016/j.laa.2014.07.004).
The version-of-record text was not separately inspected. The manuscript
therefore explicitly locates the lemma in arXiv version 4 and links that
version in its bibliography.

This receipt resolves the integration gate for Appendix F and the
strengthened theorem `three:edge-classification`. Independent mathematical
review of the transfer and facet proofs is recorded in
[facet-continuation-review.md](reviews/facet-continuation-review.md).
