# Root checks for Stage 3

The restricted-barrier frontier is a different theorem from the Stage 1 support-rank minimax. Do not identify the two.

## Proof checks and possible corrections

- The arbitrary-factor wide-cap proof was reconstructed: compact affine homogenization gives the face codimension bound `D(X) >= s`; an order cap with `B=a(R-1)` gives `D(X) <= (B+1) nullity(X)`. Under `s=qB+1` and `B>=q-1`, the hypothesis `nu<q+1` forces nullity exactly `q` everywhere. Compact fibers are then singletons, active full-order corank-one labels cannot switch, and the kernel-line map injects a sphere into an equal-dimensional product of projective spaces. Invariance of domain and intermediate mod-two cohomology give the contradiction. Explain why homogenizing the compact affine slice creates no nonzero zero-height or negative-height cone points.
- The selection-free one-channel note sometimes starts with `nu<=1` although its intended conclusion is `nu>=2`. Start instead with `nu<2`; integer determinant orders then give the same rank-at-most-one argument. A statement that parameter one exists must be an optimum over lifts, not an equality for every lift in the dictionary.
- Convex normalized certificate fibers of total rank at most one are singletons: two different rays have a rank-two midpoint; normalization fixes the scalar on one ray. A fixed Slater point gives uniform upper and positive lower bounds. This compactness yields continuity and fixes the active block globally. Injectivity of the primitive-ray map uses the whole-slice identity, not arbitrary contact selections.
- The seam-incidence note contains a genuine open problem for bounded narrow caps `q>=B+2`. Its product convex fibers are contractible and the incidence projection is compact, so the stated Vietoris–Begle consequence is plausible, but it does not by itself extend the generic channel map or prove a degree theorem. Do not infer such an extension. A compact affine seam example refutes the proposed generic convexity shortcut outside the ball-slack setting.
- Investigated whether the wide-cap codimension argument automatically extends: it does not. With nullity `q-1`, the available upper bound `(q-1)(B+1)` already reaches `qB+1` in the narrow range. Generic nullity `q` only supplies a limiting saturated point in each exceptional fiber; it does not preclude higher-rank points elsewhere in that convex fiber. Thus a proof needs additional ball-slack structure.

## Candidate further reduction for independent verification

The full-certificate range-collapse set in `selection-free-hermitian-standard-barrier-cap` has dimension at most `qB-B` under a hypothetical bounded lift with parameter below `q+1`. For `B>=2`, this seems to rule out generic active-label switching altogether, while still leaving single-pattern channel collapse unresolved:

1. Outside the range-collapse set `Z`, a rank-q convexly averaged certificate forces every primal fiber point to have nullity q. The compact chord argument makes that fiber a singleton.
2. At such a support v, compactness implies that every sequence of generic primal tuples approaching v converges to this unique tuple. Its nullity is q and its generic limiting active pattern is q distinct full-order corank-one blocks. All inactive blocks are strictly positive, so no nearby generic point can introduce a new active label. Since generic tuples have exactly q active labels, their pattern is locally fixed.
3. Thus the boundaries between distinct open generic pattern regions are contained in Z. The closure of semialgebraic Z has the same dimension, at most n-B. For B>=2, its complement in S^n is connected. The generic pattern on that complement is locally constant by step 2, hence constant. Every nonempty generic pattern region meets that complement, so there is only one generic pattern overall.

Check these arguments independently before using them. This would sharpen the open-case description: with B>=2 the remaining mechanism is collapse of a fixed generic pattern over an exceptional set, not a codimension-one switch of block labels. It does not prove the optimal barrier value and must not be presented as doing so. When B=1, the codimension estimate allows label switching and this argument gives no improvement.

The two-parameter recession lemma should extend to all EJA dictionaries: first take t to infinity along a nonzero recession direction, then approach a complementary compressed boundary tuple. The scaled gradient and Hessian converge to the independent logarithmic components of degrees rank(D) and compressed nullity. Provide the derivative-level asymptotics, not merely an O(1) function expansion.

## Literature

See `root-literature.md` for the primary Hildebrand active-facet theorem, projective-self-concordance comparator, and current 2026 geometric-barrier paper. Distinguish arbitrary affine barriers, logarithmically homogeneous cone barriers, and the least parameter of one prescribed standard restriction.

## Existing manuscript overlap

The repository's `central-path-cost/sections/06-formulation.tex` and `appendix-formulations.tex` already contain the exposed-minor metric estimate, grouped/packed constructions, and norm-tree root-slice calculations. These are useful self-contained foundations or consequences, but cannot be advertised as previously absent repository developments. The new formulation-wide rank and restricted-barrier minimization results are the relevant extension. The `formal/` directory concerns a different scalar-dilation certificate and was only read to establish scope; it is not edited or used as a proof of this manuscript's theorems.
