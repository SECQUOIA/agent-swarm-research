# A four-block distinct-mode reach theorem for five modes

Status: developed 2026-09-04 and independently agent-reviewed; see
[the mathematical and certificate audit](../notes/review-cia-five-mode-four-block.md).
This is not external peer review. The result concerns one-sided cumulative discrepancy;
it does not by itself give the exact three-switch two-sided CIA worst case.

For five measurable simplex-valued controls, at most four distinct modes can always reach

\[
 \min\{T,1845E/256\}
\]

at one-sided discrepancy threshold `E>0`. The constant is attained by the uniform
control. The new step is a weighted two-block inequality proved by 360 exact rational
linear-programming certificates. Time is continuous throughout.

## Definitions and the weighted two-block inequality

Let `A_i(t)=integral_0^t alpha_i`, `F_i(t)=t-A_i(t)`, and, on a horizon `[0,L]`,

\[
 \Phi_i(b)=\max\{t\in[0,L]:F_i(t)\le b+E\}.
\]

Use indices `0,...,4`. Let `R_i=Phi_i(0)` and define

\[
 \begin{aligned}
 M&=\max_{j\ne k}\Phi_k(R_j),\\
 P_i&=\max_{j,k\ne i,\ j\ne k}\Phi_k(R_j),\\
 Q_{ij}&=\max_{p,q\notin\{i,j\},\ p\ne q}\Phi_q(R_p).
 \end{aligned}
\]

Here `Q_ij=Q_ji`. Assume `M<L`, so all first and second reach endpoints are uncapped.
For every three-element subset `S` of modes, the following bound holds:

\[
 \boxed{H_S:=\sum_{i\in S}\left(P_i+\sum_{j\ne i}Q_{ij}\right)
       \ge\frac{675}{16}E.} \tag{1}
\]

The proof below gives a finite list of rational linear inequalities whose combination
establishes (1). In particular, numerical solver accuracy is not a premise.

### Necessary linear constraints

Scale time and allocations by `E`, so `E=1`. Relabel modes to make `S={0,1,2}`.
There are 18 named events: `M`, the five `R_i`, the nine `Q_ij` whose excluded pair
intersects `S`, and the three `P_i` for `i in S`. At each named event `v`, introduce
its time `t_v` and the five allocations `a_{v,k}=A_k(t_v)`. These 108 variables are
nonnegative and satisfy

\[
 \sum_k a_{v,k}=t_v.
\]

At each first reach,

\[
 t_{R_i}-a_{R_i,i}=1. \tag{2}
\]

For a pair maximum `v` defined by allowing a set of modes `U`, every ordered pair
`j,k in U`, `j!=k`, satisfies

\[
 t_{R_j}-t_v+a_{v,k}\le-1. \tag{3}
\]

Indeed, `v` is at least that pair's latest feasible endpoint and is uncapped, so
`F_k(t_v)>=R_j+1`. Every first reach of a mode in `U` is at most `t_v`.

For every known order `v<=w`, impose `a_{v,k}<=a_{w,k}` for every `k`. These orders
include the chosen ordering of the five first reaches, all first reaches preceding
their available pair maxima, `Q_ij<=P_i` for `i in S`, and all pair maxima preceding
`M`. An ordering of the first reaches exists even with ties. An ordering of the nine
`Q_ij` is neither chosen nor assumed.

Choose a distinct pair `(p,q)` attaining `M`. It gives additional equalities:

\[
 Q_{ij}=M\quad\text{when }\{i,j\}\cap\{p,q\}=\varnothing,
 \qquad
 P_i=M\quad\text{when }i\notin\{p,q\}. \tag{4}
\]

The code imposes both directions of the associated allocation inequalities; their
mass equalities then also force equal times. All these constraints are necessary for
the original continuous control. They need not characterize every feasible control.

### Exhaustive case coverage and exact certificates

Permutations preserving `S` can map the unordered maximizing pair to one of
`{0,1}`, `{0,3}`, or `{3,4}`. These represent a pair with two, one, or no endpoints
in `S`. Each representative is combined with all `5!=120` first-reach orders.
Thus 360 cases cover every control, including ties and multiple maximizing pairs.

The objective is exactly

\[
 \sum_{i\in S}t_{P_i}
 +\sum_{\{i,j\}:\{i,j\}\cap S\ne\varnothing}
       |\{i,j\}\cap S|\,t_{Q_{ij}}.
\]

For each case, the checker constructs integer matrices `A,b,B,d,c` for the necessary
conditions `Ax<=b`, `Bx=d`, `x>=0`. The saved rational vectors `y,z` obey

\[
 y\le0,\qquad c-A^Ty-B^Tz\ge0,\qquad b^Ty+d^Tz=675/16.
\]

Multiplying the feasible constraints by these vectors proves `c^Tx>=675/16` by weak
duality. Every sign, coefficient, case identifier, and resulting bound is checked
using Python's exact `Fraction` arithmetic in
[the standalone checker](../code/cia-distinct-reach/verify_n5_weighted_pairs.py).
The certificates are in
[the adjacent JSON file](../code/cia-distinct-reach/certificates_n5_weighted_pairs.json).
Run:

```
python code/cia-distinct-reach/verify_n5_weighted_pairs.py
```

This proves (1). The stated necessary conditions and their implementation have also
passed independent agent review. HiGHS was used only to propose the rational vectors; it is not
imported or trusted by the checker. Uniform controls have every pair maximum equal
to `B_2=45E/16`, giving `H_S=15B_2=675E/16`, so the bound is sharp.

## From weighted pairs to four blocks

Define

\[
 B_j=5E\left[\left(\frac54\right)^j-1\right].
\]

Then `B_2=45E/16`, `B_3=305E/64`, and `B_4=1845E/256`.
Set `L=min(T,B_4)` and suppose no sequence of at most four distinct modes reaches
`L`. All first, second, and third reach endpoints are then uncapped.

Let `G` be the largest reach of three distinct modes, and let `N_i` be the largest
three-distinct-mode reach excluding `i`. The analytic three-block theorem in
[the exact two-switch result](cia-exact-two-switch-worst-case.md) implies `G>=B_3`:
if `L<=B_3`, that theorem already contradicts the assumed failure.

At time `N_i`, append each possible final mode `k!=i` to a pair attaining `Q_ik`.
Summing the resulting inequalities for the other four allocations gives

\[
 A_i(N_i)\ge4E+\sum_{k\ne i}Q_{ik}-3N_i.
\]

At `G`, append `i` to a pair attaining `P_i` to obtain
`A_i(G)<=G-E-P_i`. Since `N_i<=G` and `A_i` is nondecreasing,

\[
 3N_i\ge5E+P_i+\sum_{k\ne i}Q_{ik}-G. \tag{5}
\]

Choose a maximizing triple, and call its three-mode set `S`. For the two modes outside
`S`, the same triple is available after exclusion, so `N_i=G`. Sum (5) over `i in S`
and then apply (1):

\[
 \sum_iN_i\ge G+\frac{15E+H_S}{3}
 \ge B_3+\frac{15E+675E/16}{3}=5B_3.
\]

Appending mode `i` to a triple attaining `N_i` uses four distinct modes. Its failure
to reach `L` says strictly `F_i(L)>N_i+E`. Summing yields

\[
 4L>\sum_iN_i+5E\ge5B_3+5E=4B_4,
\]

contradicting `L<=B_4`. This proves the four-block reach bound. Flat portions of `F_i`
cause no difficulty: the inverse always means the latest feasible endpoint.

## Exact one-sided minimax and scope

With at most three switches and five modes, the worst optimal one-sided discrepancy is

\[
 \boxed{\sup_\alpha\min_{\omega:\#\mathrm{switches}\le3}
   \max_i\sup_t\int_0^t(\omega_i-\alpha_i)
   =\frac{256}{1845}T.}
\]

The reach theorem gives the upper bound. For uniform controls, every block endpoint
obeys `t_j<=(5/4)(t_{j-1}+E)`, including repeated modes. Four iterations give
`T<=B_4` and hence the matching lower bound. Any positive one-sided error of a selected mode
`integral(omega_i-alpha_i)` is largest at the end of its block; the discrepancy is nonincreasing
outside that block. Unselected modes cannot contribute a positive one-sided error.

A completed [focused literature screen](../notes/cia-novelty.md) found no matching
statement; this does not certify priority. The subsequent
[general four-block theorem](cia-general-four-block-reach.md) proves the reach
formula for every `n>=5` and has passed independent review. The five-mode proof is
retained as a separate check. The [exact three-switch theorem](cia-exact-three-switch-worst-case.md)
now supplies the full two-sided CIA consequence through the independently reviewed
heavy-mode argument. Exact one-sided formulas for more than four blocks remain open.
