# Additional primary-source check during final review

A further targeted search for nonnegative approximation of affine functions
identified Fawzi, Saunderson, and Parrilo, *Equivariant semidefinite lifts of
regular polygons*. This source is worth adding as a close mathematical
antecedent. It does not invalidate the threshold formula or query results.

Primary sources inspected:

- [2014 arXiv manuscript](https://arxiv.org/pdf/1409.4379v1), Definition 4,
  Proposition 7, and Theorem 8: globally nonnegative interpolation of affine
  targets at finite node sets, including Chebyshev constructions.
- [Accepted manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/ccc24100-4e06-460d-b2fb-ccf567a429c3/content),
  Sections 3.1–3.2 and Appendix A, Lemma 1. The section numbering differs
  from arXiv; the accepted version uses Proposition 6 and Theorem 6.
- [Publisher](https://pubsonline.informs.org/doi/10.1287/moor.2016.0813):
  Mathematics of Operations Research 42(2), 472–494; online November 2016,
  issue May 2017. The publisher's generated citation uses the online year.

The tangent inequality has a direct relation to the extremizer. Write
`z=(m_rho-y)/h_rho`, `n=2r`, and let `z_*` be the exterior maximizer.
Since `G_r=h_rho/T_n'(z_*)` and
`z_0=z_*-T_n(z_*)/T_n'(z_*)`, the extremizer equals

`G_r [T_n(z)-T_n(z_*)-T_n'(z_*)(z-z_*)]`.

For even n and z_*>1 their global tangent inequality makes this expression
nonnegative on the entire real line. Our direct positivity proof remains
valid, but the geometric fact should be credited. Their finite-node
interpolation result and supporting-tangent lemma do not state the present
interval minimax value, its query interpretation, or the equality-attaining
coherent construction. The appropriate repair is a concise related-work
comparison and attribution near the positivity argument, with no change
to mathematical claims. I classify this as a minor attribution/completeness
issue. Fresh reviewers 3, 4, and 5 independently located the same antecedent.
