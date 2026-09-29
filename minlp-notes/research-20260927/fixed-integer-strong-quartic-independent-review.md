# Independent review of fixed-integer strongly convex quartic optimization

Date: 2026-09-28. Reviewer: a fresh agent that did not contribute to the
proof before receiving its frozen version. Result: no substantive gap
found in the stated fixed-integer-dimension Turing reduction.

The reviewed file was
[fixed-integer-strong-quartic-posslp.md](fixed-integer-strong-quartic-posslp.md),
SHA256
`96bb7fcc5b9156a1d863e31a758d521589eeb5f38fc2c47ed8cc2b81f8d60c32`.
The unbounded integer-polyhedron amendment was then supplied separately
and checked independently below. A final amended-file check is recorded
at the end when complete.

## Scope and conclusion

For fixed integer dimension and variable continuous dimension, the proof
gives an exact optimal integer block in polynomial time with polynomially
many PosSLP queries. It requires a supplied positive rational global
strong-convexity modulus and an explicit rational quartic. Constraints
may restrict only the integer block. Exact continuous coordinates are
specified implicitly; the proof does not print their algebraic
expansions. The Turing-reduction, promise-input, and fixed-dimension
qualifications are necessary and are stated correctly.

I found no reason to weaken the theorem. This is evidence from an
independent proof review, not a formal proof certificate or an exhaustive
novelty determination.

## Main proof checks

**Existence and projection.** The coercive quadratic lower bound gives
attainment on the mixed domain and the stated polynomial-bit radius.
Partial minimization preserves the supplied strong-convexity modulus:
apply the joint inequality at the two unique fiber minimizers and discard
the continuous displacement term. The positive definite fiber Hessian
justifies the implicit-function argument and the projected gradient
formula. No claim that the projected objective is polynomial is needed.

**The lattice cut.** For an integer displacement of norm r at least one,
the gradient error contributes at worst minus nu*r/4. This is at least
minus nu*r^2/4, leaving the claimed quadratic margin. Thus the rational
cut retains every integer point no worse than the query. A zero normal
certifies a unique integer optimum. Ties at other integer points are
retained by a nonzero cut. The argument explicitly does not separate the
entire continuous sublevel set, and the later algorithm never needs that
stronger property.

**Gradient approximation.** I checked the constants in equations
(10)--(11). The coefficient sum bounds the fiber gradient at zero by D;
strong monotonicity bounds the fiber minimizer by D/nu. The cross-Hessian
operator norm is bounded by K on its unit neighborhood. The requested
objective error bounds distance by eta and hence gradient error by
nu/(4d) in each coordinate. All requested accuracies, substituted fiber
coefficients, and output rationals have polynomial encoding length in
the current node's data. The case with no continuous variables is
handled separately.

**Exact comparisons.** The joint objective in equation (12) retains the
supplied curvature modulus. Its unique minimizer is the pair of fiber
minimizers, and the degree-four observable is exactly their value
difference. The now-explicit arbitrary-observable statement of the
[continuous upper bound](strong-convex-quartic-posslp-upper.md) therefore
has the required interface. I checked that interface and its use here;
I did not independently redo that dependency's complete Newton and
quantifier-elimination proof. It has its own
[independent review](strong-convex-quartic-posslp-upper-independent-review.md).
Values are used only to compare candidates, so their expanded algebraic
encodings never become geometric input data.

**Central cuts and flatness.** The central MILP is feasible at lambda
zero. Each feasible positive lambda inserts a translated scaled
difference body in the current polytope. Central symmetry and
Brunn--Minkowski then give the volume bound for every nonzero rational
normal, even a normal pointing away from the true continuous gradient.
This is precisely why the weaker integer-only cut suffices.

If the central MILP optimum is at most Lambda, the inset at Lambda has
integer-free interior. John's ellipsoid inclusions imply that this inset
is full dimensional and that its constant-width bound transfers to the
original polytope. Alternatively, after the prescribed number of cuts,
volume below one gives an integer-free translate and the same type of
flatness bound. Translation preserves lattice width. Inclusive slice
endpoints retain boundary integer points. Deficient-dimensional
polytopes are reduced to their affine lattices before these
full-dimensional arguments are used.

**Exact width and bit bounds.** The vertex-difference inequalities in
(18) give exactly the directional width. Taking the best of the d
MILPs covers every nonzero integer direction, allowing negation.
Full dimensionality ensures attainment. In fixed dimension, vertex
enumeration and these MILPs have polynomial-size input and output.
The polynomial-bit affine lattice parametrization is injective;
its full inverse image preserves all inherited inequalities. The
determinant/trace bound gives a valid curvature modulus under the
nonisometric substitution. A rational left inverse gives the new box.

The most important bit-complexity point is correctly addressed: within
one recursion node, new gradient normals have a uniform polynomial bit
bound determined by the node's fixed polynomial, curvature, and box,
rather than by recursively feeding previous cut sizes into the
approximation oracle. There are polynomially many cuts at that node,
dimension-only branching, and depth at most the fixed integer dimension.
Composing the node bounds therefore stays polynomial. This proves a
fixed-dimension result; it does not prove fixed-parameter tractability.

**Optimization invariant.** Every queried integer point is feasible for
the current branch and is recorded before a cut is made. Every cut
preserves all no-worse points. Consequently an optimum remains in a
descendant polytope or has already been recorded. Comparing all returned
and recorded candidates is sufficient, including at zero-dimensional
leaves. No objective-level bisection or positive inradius of a nonlinear
sublevel is assumed.

## Primary-source and significance checks

I directly read the theorem, oracle definition, and Sections 3--4 of
[Oertel--Wagner--Weismantel's 2014 author version](https://orca.cardiff.ac.uk/id/eprint/86766/1/IntegerConvexMinRev4.pdf).
Its central-MILP geometry supports the ingredients attributed to it.
The false symmetrized-facet formula and the omitted lower slice endpoint
both occur in that version. The present width MILP and inclusive
enumeration repair those issues without relying on them.

I also directly read the encoding convention and Corollary 1.2 of
[Slot--Steurer--Wiedmer, Hesse's Redemption, version 1](https://arxiv.org/html/2511.03440v1).
The cited ordinary approximation guarantee applies to the unconstrained
strongly convex fibers. The supplied curvature and explicit minimizer
bound would also permit a classical bounded convex-optimization route.

I directly checked the bounded-witness reduction and constructive
integer-feasibility statement in Section 1, and the unimodular affine
lattice reduction in Section 2, of
[Lenstra's 1983 original](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf).
These support the added integer-linear-algebra references and the
unbounded-polyhedron preprocessing.

The meaningful addition is the complete implementation of exact
comparison and sufficiently accurate rational cuts for the implicit
projected quartic objective with arbitrary continuous dimension. The
geometric integer algorithm is prior work. Neither the elementary
lattice-margin inequality nor the absence of equivalent formulations is
claimed here as established publication priority. The source audit is a
useful comparison, but the review does not establish exhaustive novelty.
Practical solver gains remain speculative; the theorem is an oracle
complexity result.

## Independent targeted computations

An independent Python calculation using `fractions.Fraction` checked 24
two-variable quartics of the form

    (x^2+y^2)/2 + a*x + b*y + (x+y-c)^4/8 + e*(2*x-y)^4/16,

where e is zero or one. Their Hessians are globally at least the
identity. On the box [-3,3]^2, the calculation repeatedly computed the
exact central integer query by finite enumeration, obtained exact
polytope vertices by rational linear algebra, and added the proposed
cut with an adversarial gradient error of Euclidean norm exactly 1/4.

All 112 central cuts satisfied the claimed volume decrease and retained
every no-worse integer point. Comparing the recorded points and the
remaining points agreed with exhaustive optimization in all 24 cases.
Additional exact boundary examples checked that an adjacent integer tie
is retained and that an allowed approximate normal can exclude an
improving real point. This last example confirms the necessity of the
integer-only interpretation.

These finite checks challenge the interaction of repeated cuts and
candidate recording. They do not prove polynomial running time, general
flatness, the continuous observable theorem, or the global theorem.
No Lean verification was attempted; the decisive arguments here use
standard geometric and algorithmic results rather than a small isolated
algebraic identity.

Targeted command actually run: an inline `python - <<'PY'` script with
exact rational arithmetic. Output:

    PASS: 24 exact convex-quartic cutting trajectories, 112 central cuts;
    saturated-error ties and real-sublevel failure; 81 radius cases.

The 81 radius cases concern the amendment below. They supplement its
symbolic proof and are not its justification. No project-wide checks or
CI inspection were performed.

## Separately checked unbounded integer-polyhedron amendment

Let P be any rational polyhedron in the fixed-dimensional integer block.
Fixed-dimensional integer linear feasibility either detects that P has
no integer point or returns a polynomial-bit integer point z0 in P.
Put C=f(z0,0), a=grad f(0), f0=f(0), and

    A = ||a||_1 + |C-f0| + 1,
    R = 1 + ceil(2*A/mu).

These data have polynomial bit length. If r=||x|| is at least R, then
mu*r/2>A and r>=1. Therefore

    f(x)-C >= f0-C-||a||_1*r+mu*r^2/2
           > -|C-f0|+(|C-f0|+1)*r >= 1.

Thus every point with f<=C lies inside the radius-R ball. Intersecting
P with [-R,R]^k preserves an optimum; coercivity and closedness ensure
attainment. This validates the amendment for rational constraints on the
integer variables alone. It does not address constraints involving the
continuous block.

## Separately checked full-Gram hardness padding

The author subsequently supplied the padding

    P(X,z) = f(X) + ||z||^2 + t*||z||^4 + ||z||^2*||X||^2,
    t = 1 + 8*n*k/mu0,

starting with a full Hessian Gram M at least mu0*I. I independently
checked every new Hessian term. The two cross tensor blocks have
diagonal coefficient 2; the z-direction quartic block is
4*t*I + 8*t*vec(I_k)*vec(I_k)^T. The remaining cross term is exactly
8*(X dot v_X)*(z dot v_z), represented by the stated off-diagonal
block with coefficient 4.

For arbitrary formal vectors in these blocks, Cauchy--Schwarz and
Young's inequality bound the absolute cross term by

    (mu0/2)*U^2 + (32*n*k/mu0)*V^2.

The remaining z tensor diagonal coefficient is 4. Hence the full
assembled Gram is at least min(mu0/2,2)*I, on its entire formal vector
space. Nonnegative added terms vanish at z=0, so the mixed optimum
equals the original continuous optimum. The certificate and coefficients
have polynomial bit length. The extension of strict and weak order
hardness to every fixed positive integer dimension in the verifiable
full-Gram format is therefore valid. No equality-hardness conclusion
follows or is asserted.

A separate exact SymPy expansion for n=k=2 and mu0=1/7 returned zero
for the difference between the Hessian biform and the claimed Gram
biform, and confirmed the remaining coefficient 4. Command actually
run: another inline `python - <<'PY'` script. This checks one
nontrivial instance of the identity; the displayed general inequalities
justify the dimension-uniform statement.

## Final reconciliation

The amended theorem, radius argument, source links, and full-Gram padding
were read at SHA256
`6936035b38869d4c9e8191b76f15b13df221984ca914d1114bf981c04439b069`.
The new proofs passed. The reviewer requested one scope clarification:
the floor/ceiling argument in the one-integer corollary must explicitly
refer to an unconstrained integer block. It need not hold for a
constrained block; for example, x squared has continuous minimizer zero
but constrained integer minimizer 100 on [100,infinity). This does not
affect the general algorithm or its proof.

The author made that correction and independently checked the example.
I then checked the corrected wording and final main-file SHA256
`efcfd7730430daf3292822e2fc785b88f29d80ec0c16458559b9225e38909129`.
No unresolved substantive issue remains from this review.

Targeted review-file checks passed: local Markdown links, trailing
whitespace, final newline, and
`git diff --check -- research-20260927/fixed-integer-strong-quartic-independent-review.md`.
