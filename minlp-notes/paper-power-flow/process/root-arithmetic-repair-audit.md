# Root audit of the stage 3 arithmetic repair

Read the complete new algebraic section and arithmetic appendix before the
correction agent finished validation. This is a proof audit, not the required
five-reviewer round.

- Polynomial circuit coordinates are uniquely determined on the original
  compact basic closed set. Nonnegative output values are imposed globally.
- Scaling a multiplication by epsilon uses w_x*w_y=q and epsilon*w_z=q,
  with q=epsilon^2*z. All intended small coordinates have magnitude at most
  delta, including q, the zero coordinate, and the halving chain.
- The midpoint chain gives Delta=1-delta using bounded additions only;
  A_delta+Delta=2 fixes delta without an unencoded external constant.
- Shifted addition reduces to s+t=u. In the shifted product chain,
  m=1+s+t+st, f=3/2+s+t+st, g=3/4+s+st, h=3/2+s+st;
  B_u+B_s=h gives u=st. J+1/2=A_s imposes s>=0 by J>=1/2.
- The product-from-squares chain yields ab exactly. Every center is
  3/4, 1, or 3/2. The squared inputs tend to 1.
- The reciprocal square chain has h=1/[a(a+1/2)], i=a^2+a/2,
  and final output a^2. Its seven center values lie strictly inside
  the allowed interval, and all reciprocal denominators are nonzero.
- The finite continuity argument legitimately chooses a single dyadic
  delta before epsilon, uniformly across the finite types of gates.
- Reverse recovery does not need an assumption that arbitrary final
  coordinates are small. Bounded equations first recover the exact circuit
  and original set; compactness then gives the intended small bounds.
- Forward coordinates are rational with nonzero denominators on the set;
  every original coordinate has the stated individual affine recovery.
- The denominator-guard proof of basic-closed invariance, the three-quadrant
  local obstruction, and the finite-simplex nonface realization are sound.

No proof issue found in this audit. A quadrant-number wording ambiguity
was sent to the correction agent and fixed before its final delivery.
