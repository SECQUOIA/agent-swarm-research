# A known global clique cut closes the hard family

Date: 2026-09-05. Status: elementary scope observation; the cut family is
classical and is not claimed as a new result.

The spatial lower bounds restrict the node proof system. One standard global
quadratic inequality immediately closes the single-block family:

```
2 sum_{i<j} X_ij - 2k sum_i x_i + k(k+1) >= 0.             (C)
```

This is a Boolean-quadric clique inequality. In the notation of
[Saito, Fujie, Matsui, and Matuura (2004), Section 4, equation (9)](https://www.keisu.t.u-tokyo.ac.jp/data/2004/METR04-32.pdf),
take the whole coordinate set and `beta=k+1`. That source attributes the
clique family to Padberg. The application below is an elementary consequence.

**Validity on the continuous graph.** With `X_ij=x_i x_j`, the left side is
multiaffine in `x`. Its minimum on `[0,1]^n` is attained at a Boolean vertex.
If that vertex has `s` ones, the expression equals
`(s-k)(s-k-1)>=0`, because `s-k` is an integer. Thus (C) is valid for the
continuous bilinear graph as well as for Boolean points.

**Exact root bound.** The linearized equality products imply
`sum_{i,j}X_ij=K^2`, where `K=k+1/2`. Hence (C) gives

```
trace(X) <= K^2-2kK+k(k+1)=k+1/4,
sum_i (x_i-X_ii) >= K-(k+1/4)=1/4.
```

The true optimum is `1/4`, so adding this single known cut to RLT makes
the root bound exact. PSD is not needed for this deduction.

For a positive ordered linear perturbation, the same cut certifies the base
penalty and the demand-balance LP separately minimizes the linear term at
the unique optimal vertex. Thus it also closes the perturbed single-block
family. For the direct-product construction, one clique inequality per block
makes the summed bound exact.

This observation clarifies what the exponential lower bound means. The
number of spatial leaves remains large even with a stated amount of
moment/preordering information, but a globally valid quadratic inequality
from a known family can avoid the tree. The clique polynomial is not
available from the permitted low-degree box preordering merely because its
own degree is two: deriving its global nonnegativity from local bounds can
require much larger SOS/preordering degree.

In particular, “all valid affine inequalities” in the SDP–RLT closure
remark refers to inequalities in the **original x-space** polytope. It does
not mean all affine inequalities in lifted `(x,X)` variables; that larger
class contains (C).
