# Stage 5 provisional coordinator proof audit

This is preparation for the independent review gate, not acceptance.

## Signed cubic section

Read the complete first draft of sections/13-xor-quadratic-hulls.tex.
SHA-256: 91a88f8fc6507d6135792437fbcdb12d8c77e7579f74b784eac05c35a7a18741.

Reconstructed the actual-hull versus closed-halfspace distinction, deterministic
substitution (not conditioning), every repeated localizer and local equality,
Boolean idempotence degree 4r, affected-clause bounds, and cover count. The
source distribution is marginalized only for degree-two realization; no
feasible-graph support is assumed. All integer/tolerance/dimension quantifiers
in the occurrence-controlled family are consistent.

Freshly reread Schoenebeck's original printed pages 7–11, Theorems 11/12 and
Lemma 13 construction/proof. The draft directly defines every character
moment through width w by derived sign/zero, including odd top degree, then
proves PSD on squares through floor(w/2) from signed equivalence classes.
This resolves the odd-width Gram-split concern without an unproved moment
extension. The constant vector is normalized. All four needed source facts
(width, clause means, signs, square positivity) are established explicitly.

Checked the elementary Chernoff exponent -2nt+nt^2 and union bound; occurrence
moment derivative and deletion threshold; event intersection; retained
7n<=m<=8n, occurrence<=64 and OPT>=1/8; both tolerance targets and simultaneous
order range; every sensitivity/Hessian factor. No repair found in this draft.

## Candidate order-one upper certificate

Independently proved the full-box quadratic certificate and ran
check_order_one_upper.py. Its exact finite checks include 3,375 boxes and
216,000 vertex identities/inequalities. It reconstructs 250 LP-selected
moment distributions exactly, including 242 with support outside the graph
and 226 below the true node graph optimum. All candidate bounds hold.
The universal proof is the quadratic identity and bounds documented in
process/order-one-monomial-refinement.md, not these finite tests.

## Bounded monomial and finite-certificate sections

Read complete drafts of sections14 and15. The only local clarification sent
to the author was the repeated-factor coordinate index in the localizer
expansion; the author reports it corrected before completing authoring.
The source-to-graph substitution, all degree budgets, signed realization,
actual node support, affected-clause estimate, exact parity count and basis
support union are valid. Checked the order-one lower extension and all
12r, N<=17n, 7n/3072, 7N/52224 and degree-versus-region constants.

Reconstructed both finite upper certificates, their graph equations and
quadratic dual identity. Checked epsilon>0 including M=1; fixed-tolerance
relative implication; no graph support or computational tractability is
silently assumed. Reconstructed both affine obstructions including r=1,
n=1 and arbitrary fixed signs. Fresh primary Stabbing Planes v3 read confirms
intro Theorem1 and detailed Section3/Theorem6, including the degree-dependent
terminal enumeration and quasipolynomial bound in the CNF encoding size.
The manuscript's limited comparison and 1/m-versus1/16 distinction are valid.
No mathematical repair found. Final author package/build/coverage and the
15 independent reviews remain pending.

Current 14-monomial-reformulations.tex SHA-256: e341cb6a1eaedc5934c81261948792b284b509d18cefd94ab143dfc9da8134eb.

Current 15-finite-certificates-affine.tex SHA-256: 751e742ca632da5158ef911f88f0e55ea49147428d4b7bb64970c5b5d16b7c79.


## Completed author package and review freeze

The root read the complete author ledger, source audit JSON, and final build report. All current LaTeX/bibliography inputs and the PDF match the build hashes; the PDF has 91 pages and no reported warnings. The repeated local-generator indices are now explicitly independent of coordinate indices. The root visually inspected pages 67,70,72,74,75: no clipping, overlap, or unreadable mathematics. All three new sections, both verification scripts and results, the full assignment and coverage map were read. No major or minor defect was identified in this preliminary check. This is not stage acceptance; the independent fifteen-reviewer gate follows.
