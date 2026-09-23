# Stage 4: root source reading and proposed extension audit

The root read the complete bounded-rank source proof, including the seven-product
K4 section, and supplied the separate constructive development plan.

## Main proof checks

- A signed fundamental-cycle normal matrix remains TU and includes coordinate
  normals. Minimal nonnegative dependencies have unit nonzero entries, and an
  opposite-normal pair cannot be part of a larger minimal positive dependency.
- Cofactors of r-1 independent TU normals give primitive ternary edge directions.
  Appending any other normal shows its scalar product with such an edge is also
  ternary. This stronger transformed-edge fact is what bounds support-dual
  multipliers after a unimodular change of basis; a naive matrix norm estimate
  would not establish the stated constant.
- A chamber of the central edge-orthogonal arrangement is pointed because the
  coordinate hyperplanes are present. Each support function is linear on its
  closure, including for lower-dimensional state polytopes. Its extreme rays
  therefore suffice to describe every relevant Minkowski sum.
- An optimal support dual has a basic representative even if the primal state
  polytope is degenerate. Independent support rows can be completed to a full
  basis with zero multipliers. Opposite rows cannot both be in that basis.
- The K4 sharpness example has unit capacities but several supply/demand nodes.
  Its first state is fixed to (p,q,p); the other two explicit states have zero
  all-ones support. A residual support bound gives 2p+q >= 0, and the given
  local witnesses establish the complete nearby half-plane, not just necessity.
  A coordinate-section facet restriction is needed to transfer this to actual
  ambient product coefficients and rule out changes by affine-hull equations.

## Candidate constructive recovery

The suffix algorithm uses an intersection with normals M union (-R). The suffix
support inequalities describe the entire remaining sum, so intersection
nonemptiness follows by induction. Every nonempty bounded polyhedron, including
a singleton or a lower-dimensional one, has a vertex whose active normals span
the ambient coordinate dimension. Otherwise an orthogonal line direction would
contradict extremality. Thus full-rank inverse-basis enumeration finds a point.

There are 2^{O(r^2)} candidate normals; enumerating r-row bases and checking all
rows gives the conservative 2^{O(r^3)} per-state bound. The inverse matrices
depend only on the integer normal library. Their entries have parameter-bounded
encoding length. Online recovery uses affine maps with these fixed coefficients,
not products of two recursively generated coordinates; denominator lengths can
grow at most by the sum of per-step increments. This needs to be made explicit
in the final rational-size argument.

This extension remains an author/reviewer candidate until Stage 4 is accepted.
It does not establish the smaller 2^{O(r^2)} construction bound or a runtime
advantage over a compressed LP. The separation theorem keeps its original bound.

## Smaller sharp K4 candidate found during Stage 4

The root found a five-observation example with two explicit states and sent it
to the sole stage author for independent development. In the original source's
arc order (12,13,23,01,02,03), keep C unchanged but take

    v=(1/2,1/2,1/2,1/4,1/2,1/2), u=1,
    b=(-5/4,-3/4,1/2,3/2),
    aggregate theta=(1/6,1/24,1/8),
    aggregate x=(2/3,13/24,5/8,11/24,11/24,1/3).

Both explicit weights and the residual weight are 1/3. Observe (12,1)=U,
(13,1)=V, (02,1)=1/6, (23,2)=1/6, and (01,2)=1/12. Write
p=U-1/6 and q=V-1/6. The first state is (p,q,p), and the second is
s(1,-1,0). Residual bounds give h*theta0 <= 1/3 for h=(1,1,1), while
h*aggregate=1/3 and h*theta2=0. Therefore 2p+q>=0 is necessary.

For |p|,|q|<1/96 and w=2p+q>=0, choose s=q/2 and

    theta0=(1/6-p-q/2, 1/24-q/2, 1/8-p).

Its C values are

    (1/6-w/2, 1/24-q/2, 1/8-p,
     5/24-p-q, -1/24+q/2, -1/6+w/2).

All state intervals are [-1/6,1/6] except the 01 interval [-1/12,1/4].
The first and last expressions satisfy their potentially tight bounds exactly
because w>=0; the others stay strictly inside their bounds in the stated
neighborhood. The other two states are feasible there as well, and their sum
is the prescribed aggregate. Thus the nearby section should be exactly
2U+V>=1/2, proving the same sharp ratio with fewer states and observations.

The independent root script `verification/stage04-root-k4-five.py` builds the
full arc/state system from incidence equations without using repository hull
code. All 289 grid classifications agree with the proposed half-plane; 149
feasible points also have exactly verified rational state decompositions.
The other 140 statuses are numerical infeasibility checks, not exact solver
certificates. The analytical support argument supplies the general necessity.
Output is retained in the adjacent JSON. Author development and the complete
five-reviewer stage are still required before this new example is accepted.
