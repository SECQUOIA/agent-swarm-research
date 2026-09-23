# Stage 1 assessment

All five independent reviewers found no major mathematical issue. Root also
read the fixed-accuracy proofs, checked the implementation contracts and
threshold formula, and independently diagnosed the source's singleton-band
and exact-normalization defects before review. The author corrected both.

Accepted minor findings, consolidated across reports:

1. Explain definite-parity QSVT for a general Hermitian contraction: even
   p(|H|)=p(H), odd sign(H)p(|H|)=p(H), with zero treated explicitly.
2. State that G_r-e is nonnegative on [1,rho], that the auxiliary d(x)
   bound holds on [0,1], and that the pinned-tail estimate has |x|<=1.
3. Describe E_r as approximation errors giving parity lower-bound cutoffs;
   do not imply an optimal even-parity staircase or an equality theorem.
4. Make the nonnegative-integer index convention explicit.
5. Define a positive general normalization before the exact-normalization
   results; retain the exact nu<2 impossibility and formal-bound caveat.

These affect statement precision and exposition, not the proofs on their
actual domains. No major finding requires a second review round. A separate
fixer must address all accepted findings and rebuild before Stage 2 begins.
