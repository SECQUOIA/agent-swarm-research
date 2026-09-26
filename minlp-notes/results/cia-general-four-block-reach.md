# An exact four-block reach theorem for every number of modes at least five

Status: developed 2026-09-04 and independently agent-reviewed; see
[the mathematical and certificate audit](../notes/review-cia-general-four-block.md).
This is not external peer review. Novelty remains a separate literature question.
The theorem below concerns one-sided cumulative error.

Let `n>=5`, let `alpha:[0,T]->Delta_n` be measurable, and put

\[
 r=\frac n{n-1},\qquad B_k=nE(r^k-1),\qquad E>0.
\]

**Four-block reach theorem.** Some sequence of at most four distinct modes reaches
`min(T,B_4)` while keeping the one-sided cumulative error
`integral_0^t(omega_i-alpha_i)` at most `E` for every mode and time.

Consequently,

\[
 \boxed{\sup_\alpha\min_{\omega:\#\mathrm{switches}\le3}
 \max_i\sup_{t\in[0,T]}\int_0^t(\omega_i-\alpha_i)
 =\frac{T}{n[(n/(n-1))^4-1]},\qquad n\ge5.} \tag{1}
\]

Uniform controls attain the lower bound. The proof uses 179 finite integer
certificates and ten polynomial certificates, with no time discretization or
numerical tolerance in their verification. The earlier
[five-mode certificate result](cia-five-mode-four-block-reach.md) remains a separate
independent check of the smallest case.

## A weighted pair inequality

Let `A_i(t)=integral_0^t alpha_i`, `F_i(t)=t-A_i(t)`, and define the latest feasible
block endpoint on `[0,L]` by

\[
 \Phi_i(b)=\max\{t\in[0,L]:F_i(t)\le b+E\}.
\]

Use `R_i=Phi_i(0)` for the first reaches. Let `M` be the global maximum of two-distinct-
mode reaches, `P_i` their maximum after excluding mode `i`, and `Q_ij=Q_ji` their
maximum after excluding both `i,j`. Assume `M<L`, so these endpoints are uncapped.
For any three-element mode subset `S`, set

\[
 H_S=\sum_{i\in S}\left(P_i+\sum_{j\ne i}Q_{ij}\right).
\]

The key bound is

\[
 \boxed{H_S\ge3nB_2.} \tag{2}
\]

We prove a stronger linear bound valid for any distinguished index `z`:

\[
 H_S\ge\frac{3n^2}{n-1}E+
             \frac{3n^2}{(n-1)^2}\sum_{i\ne z}R_i. \tag{3}
\]

Choose `z` attaining the smallest first reach. Continuity gives
`A_i(R_i)=R_i-E`. Since `R_z<=R_i` and every allocation is nondecreasing,

\[
 R_z=\sum_i A_i(R_z)\le\sum_i(R_i-E),
 \qquad\text{hence}\qquad \sum_{i\ne z}R_i\ge nE.
\]

Substitution in (3) gives exactly (2). The argument treats ties and flat portions
without assuming unique threshold roots.

## Necessary pair constraints

Scale by `E`, so `E=1`, and relabel `S={0,1,2}`. Introduce a nonnegative variable
`R_i` for each mode. Introduce an event time `t_v` and allocations `a_{v,k}` for `M`,
the three `P_i` with `i in S`, and each `Q_ij` whose excluded pair meets `S`.
There are `3n-2` events. Impose nonnegativity and

\[
 \sum_k a_{v,k}=t_v. \tag{4}
\]

At an event defined as the pair maximum over available mode set `U`, impose

\[
 R_j-t_v+a_{v,k}\le-1
 \quad(j,k\in U,\ j\ne k). \tag{5}
\]

For the actual control, (5) follows from `F_k(t_v)>=R_j+1`. Impose allocation
monotonicity for `Q_ij<=P_i` with `i in S` and for every event preceding `M`.

Choose an unordered pair `P={p,q}` attaining `M`. If a deletion avoids `P`, that
same pair remains available, so

\[
 Q_{ij}=M\text{ if }\{i,j\}\cap P=\varnothing,
 \qquad P_i=M\text{ if }i\notin P. \tag{6}
\]

The program imposes both allocation orders for each equality in (6); equation (4)
then forces equal times. These are necessary linear conditions. No first-root
equation, ordering of `R_i`, or total ordering of the pair events beyond the stated
inclusion orders is imposed in this
relaxation. Its lower bound is therefore stronger than what is required of actual
first reaches.

The objective of this auxiliary program is

\[
 C= (n-1)^2 H_S-3n^2\sum_{i\ne z}R_i. \tag{7}
\]

We certify `C>=3n^2(n-1)`, which is equivalent to (3) at `E=1`.

## Symmetry reduction and ten cases

Permutations preserving `S` transform the maximizing pair to `{0,1}`, `{0,3}`, or
`{3,4}`. Permutations also preserving that pair give the following possibilities
for the distinguished index:

| Maximizing pair | Distinguished representatives |
| --- | --- |
| `{0,1}` | `0`, `2`, `3` |
| `{0,3}` | `0`, `1`, `3`, `4` |
| `{3,4}` | `0`, `3`, `5` |

The final type, maximizing pair `{3,4}` with distinguished index `z=5`, exists only for `n>=6`; the other two `{3,4}` types (`z=0`, `z=3`) exist for `n=5`. These ten types cover all choices of `S,P,z`.

Within a type, keep every index in `S union P union {z}` individually labeled.
All other modes can be permuted. The necessary linear system and objective are
invariant under this finite permutation group. Averaging any feasible point over
the group preserves feasibility and objective value. Thus imposing equality of
variables in the same orbit does not change the minimum of the auxiliary LP.

The checker constructs the resulting quotient directly. An orbit label records
each individually labeled index, and records equality or inequality of the remaining
indices. For example, allocation to the unlabeled mode that occurs in an event's
excluded pair and allocation to another unlabeled mode are distinct variables.
This distinction is essential and is retained.

There are at most six individually labeled indices. Each inequality involves at
most three other indices; mass sums have the multiplicities described below.
Thus for `n>=9`, every orbit pattern is already present,
and the quotient has fixed topology. Depending on the case, it has 57 to 162
variables, 151 to 826 inequalities, and 10 to 19 equalities. Its inequality matrix
and right-hand sides are constant in `n`. Only the following coefficients vary:

* In a mass equation, the number of equivalent allocation modes is `n-s` or
  `n-s-1`, where `s` is the number of individually labeled indices. Thus every
  equality-matrix coefficient is affine in `n`.
* An objective orbit has either constant multiplicity or multiplicity `n-s`.
  Multiplying by `(n-1)^2` for time variables and by `-3n^2` for reach variables
  makes every objective coefficient an integer polynomial of degree at most three.

The code reconstructs these symbolic coefficients from the exact orbit counts at
`n=9,10`. This is exact affine reconstruction of known multiplicities, not numerical
interpolation of an unknown function. Row ordering is stable: all individually
labeled indices are at most 5, and additional indices only repeat existing orbit
patterns once three unlabeled indices are present.

## Exact certificates for all dimensions

Write the quotient as `Ax<=b`, `B(n)x=d`, `x>=0`. For each of the 179 cases with
`5<=n<=22`, the saved certificate consists of a positive integer denominator and
integer dual numerators. The checker verifies their signs, every coefficient
identity, and the exact lower bound `3n^2(n-1)` for (7).

For each of the ten types and every `n>=23`, the certificate gives integer
polynomials `D(n),D_0(n),Y(n),Z(n)` satisfying

\[
 \begin{aligned}
 D(n)&=(n-1)^2D_0(n),\\
 D_0(n)c(n)&=A^T Y(n)+B(n)^T Z(n),\\
 b^T Y(n)+d^T Z(n)&=3n^2(n-1)D_0(n),
 \end{aligned} \tag{8}
\]

where `c(n)` is the integer-polynomial objective vector in (7). The checker verifies
these as polynomial identities. It also checks that `D(23+t)` has positive constant
coefficient and nonnegative remaining coefficients, and every entry of
`-Y(23+t)` has nonnegative coefficients. Hence `D(n)>0` and `Y(n)<=0` for every
real `n>=23`, and `D_0(n)>0` there. Dividing (8) by `D_0(n)` gives a valid LP dual
bound `C>=3n^2(n-1)`. Equivalently, division by `D(n)` certifies (3).

The standalone command is

```
python code/cia-distinct-reach/verify_general_four_block.py
```

The [checker](../code/cia-distinct-reach/verify_general_four_block.py) uses only Python's
standard library and integer arithmetic. Its
[certificate file](../code/cia-distinct-reach/certificates_general_four_block.json)
contains no executable expressions. Numerical LP and symbolic linear algebra tools
were used to find the certificates; neither is imported or trusted by the checker.
All finite cases and all ten polynomial identities pass.

## From weighted pairs to four distinct blocks

Set `L=min(T,B_4)` and suppose no sequence of at most four distinct modes reaches
`L`. All first, second, and third reaches are then uncapped. Let `G` be the global
maximum three-distinct-mode reach, and `N_i` the corresponding maximum excluding `i`.
The analytic three-block theorem in
[the exact two-switch result](cia-exact-two-switch-worst-case.md) implies `G>=B_3`:
if `L<=B_3`, that theorem already contradicts the assumed failure.

At `N_i`, append each `k!=i` to a pair attaining `Q_ik`. At `G`, append `i` to a
pair attaining `P_i`. Summing the former endpoint inequalities and using
`A_i(N_i)<=A_i(G)` gives

\[
 (n-2)N_i\ge nE+P_i+\sum_{k\ne i}Q_{ik}-G. \tag{9}
\]

Choose a maximizing triple and let `S` be its three-mode set. Then `N_i=G` for each
mode outside `S`. Summing (9) over `S` yields

\[
 \sum_iN_i\ge
 \left(n-3-\frac3{n-2}\right)G+
 \frac{3nE+H_S}{n-2}.
\]

The coefficient of `G` is positive for `n>=5`. Substitute `G>=B_3` and (2), and
use `(n-1)B_3=n(B_2+E)`, to obtain `sum_i N_i>=nB_3`.

Appending mode `i` to a maximizing triple excluding it uses four distinct modes.
Its failure to reach `L` implies strictly `F_i(L)>N_i+E`. Summing gives

\[
 (n-1)L>\sum_iN_i+nE\ge nB_3+nE=(n-1)B_4,
\]

contradicting `L<=B_4`. The latest-endpoint definition makes the final inequality
strict even with flat portions of `F_i`.

For the schedule so constructed, the one-sided error of a selected mode increases
through its single block and is nonincreasing outside that block. Its block endpoint
constraint therefore controls the entire trajectory. An unselected mode has
nonpositive one-sided error. This proves the reach theorem.

For uniform controls, every block endpoint obeys `t_j<=r(t_{j-1}+E)`, even with
repeated modes: occupation of the current mode is at least its current block length.
Four iterations give `T<=B_4`. This proves the matching lower bound in (1).

## Attribution and limits

The analytic three-block aggregate suggested the recurrence (9). The five-mode
partial-order LP suggested using a global maximizing pair. Inspection of its dual
root multipliers suggested the stronger bound (3), after which removal of first-root
constraints exposed the finite symmetry reduction. These are complementary parts
of the investigation, not independent claims of priority.

The proof establishes the four-block theorem for all `n>=5`; it does not establish
the analogous exact formula for arbitrary numbers of blocks. The independently reviewed
[exact three-switch theorem](cia-exact-three-switch-worst-case.md) now supplies the full
two-sided consequence using a heavy-mode bound. The [completed literature screen](../notes/cia-novelty.md)
found no matching theorem within its documented scope; publication priority remains provisional.
