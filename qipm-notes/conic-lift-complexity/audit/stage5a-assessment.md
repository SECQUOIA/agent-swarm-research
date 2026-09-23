# Stage 5A root assessment

All five independent reviewers completed personal reviews of all four new sections. Root read all five reports, previously read all four sections independently, and checked the cited passages. No major issue was identified. Root agrees that the weighted norm-tree coefficient and the other substantive arguments are valid on their stated mathematical models.

Five consolidated minor corrections are accepted:

1. Review 1: require at least one column (`r>=1`) for the PSD compression and a positive optional gradient parameter `vartheta>0` before dividing by its square root. A constant compression otherwise permits zero.
2. Review 3: define `U` in the matrix-ball compression example as the matrix of the selected orthonormal left coordinate vectors.
3. Review 3 and root's consistency check: require `0<R_0<1` in the spectral-profile divided chord bound. Apply the same explicit positive-radius and positive-integer chord-count convention to the other divided bounded-chord formulas in 11a–11c (`m>=1`, `0<R<1`, and `M>=1` where division by M occurs). Zero-radius/no-move cases need not be encoded by division by zero.
4. Reviews 1 and 3: specify `0<epsilon<=k` and `0<R<1` for the central arc/chord formula `A(1-epsilon/k)`. The endpoint epsilon=k gives zero; a larger tolerance is already met at the analytic center.
5. Reviews 4 and 5: replace “equal objective weights” by “unit objective weights” in the entropy specialization. The general formula is correct; equal weights lambda would give `lambda exp(H(p))`.

Review 2 requests no correction. All accepted items are local domain, notation, or normalization clarifications; none alters a substantive proof or requires a second major-issue review cycle. A different correction author must implement every accepted item and verify a clean build before Stage 5B begins.
