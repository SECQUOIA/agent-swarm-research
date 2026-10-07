# Independent review of affine-selector recognition

Date: 2026-10-02. Reviewer: the negative-curvature workstream author,
independent of the adversary who derived the recognition result.
Reviewed source: [affine-selector-recognition.md](../adversary/affine-selector-recognition.md).
This is research-agent review, not external peer review or a priority audit.

**Assessment: no substantive mathematical gap found.** The result gives
a polynomial-bit necessary-and-sufficient test for existence of a globally
affine optimal selector for a rational PSD quadratic on a private product
box, parameterized affinely by a second product box. Singular Hessians and
tied conditional optimizers are included. Both boxes have their fixed
coordinates substituted first.

The central optimal-set identity is exact. The feasible first-order term
and PSD remainder in the quadratic expansion are separately nonnegative;
zero objective gap implies `C(y-yhat)=0` and then the stated linear-objective
equality. Conversely those two equalities give zero gap. This also proves
that every central optimizer has the same gradient.

The simpler final construction partitions coordinates directly by signs
of the common central gradient. Positive gradient forces the lower bound
at every central optimizer; negative gradient forces the upper bound.
A globally affine feasible coordinate attaining a bound at the strict
interior parameter midpoint must equal that bound throughout the
parameter box. For a zero-central-gradient coordinate, an affine optimal
response is either always at a bound, in which case its affine one-signed
gradient has an interior zero and vanishes identically, or is strictly
interior at every interior parameter, where stationarity forces the same
affine identity. This proves the necessary fixed KKT pattern.
The convex KKT conditions give its sufficiency, including zero multipliers
and degeneracy.

This sign partition avoids the originally proposed coordinate LPs over
the central optimizer set: the final recognizer requires one central
convex QP and one affine-map LP. Coordinates forced to a bound in the
central optimal set but having zero central gradient are safely included
in the zero-gradient group. Universal primal feasibility and the zero
gradient identity retain every needed restriction. I checked this
simplification independently after it was suggested in integration review.

The absolute-value auxiliaries correctly express universal affine bounds
on a box. Existence of auxiliaries is equivalent to using the exact
absolute values: any larger auxiliary only strengthens the required
range or sign inequality. There are polynomially many variables and
constraints, with rational data of polynomial length. Standard exact
convex-QP and LP algorithms therefore give the stated rational bit
bound and a polynomial-length rational selector whenever a real one
exists. The theorem does not claim that its diagnostic implements those
general-purpose polynomial-time algorithms.

The singular two-variable squared-residual example correctly distinguishes
the full central optimal face from an arbitrary optimizer's active bounds.
The clipped scalar example correctly lies outside the affine class.
The proof uses the private **box** normal cone and does not assert this
same recognizer for arbitrary private polytopes, variable-dependent
private constraints, or arbitrary piecewise-affine maps.

This review initially checked the complete written proof before the
recognition diagnostic was finalized. Author and independent checker
results are recorded in the recognition note; finite tests supplement
the proof and do not prove its polynomial-time statement. No project-wide
verification or CI inspection was performed for this review.

The final diagnostic record was subsequently checked against this scope:
15 fixtures, 11 accepted affine selectors, four rejected nonaffine
responses, 32 reference active patterns, and 205 exact KKT checks passed.
The checker author and coordinating adversary independently ran it; this
reviewer did not claim an additional execution. Its exact finite
Fourier–Motzkin backend is explicitly a diagnostic, not the polynomial-time
LP implementation assumed by the theorem.
