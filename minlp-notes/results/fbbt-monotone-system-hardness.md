# Constant-error approximation of bilinear FBBT limits is PosSLP-hard

Status: candidate result, passed [independent mathematical review](../notes/review-fbbt.md) (2026-09-04). The hardness source is established; the proposed contribution is its transfer to FBBT and the explicit restrictions on the resulting MINLP instances. Novelty search is incomplete. No NP-hardness claim is made.

## Main statement

Consider exact-real feasibility-based bound tightening (FBBT), initialized with every variable in `[0,1]`, on a feasible system containing only affine equalities and bilinear defining equalities. Every primitive equality must receive its usual forward interval-arithmetic update infinitely often, and every other update must preserve every feasible point in the current box.

Computing a designated limiting lower bound to additive error `1/4`, in the standard binary Turing model, is PosSLP-hard under polynomial-time reductions. Exact-real arithmetic specifies the mathematical FBBT limit; it does not give a unit-cost complexity model for the approximation algorithm. The hardness remains true with all of the following restrictions simultaneously:

- All variables are continuous, and the initial box is the unit cube.
- Every equation has at most three distinct variables.
- Every right-hand-side polynomial has nonnegative coefficients from `{1/2,1}` (and constants from `{0,1/2,1}`).
- Every product has two distinct variable names; square operators are unnecessary.
- Every strongly connected component of the **directed defining-equation dependency graph** has at most four vertices.
- Feasibility is promised. In the reduction, the designated limiting lower bound is either `1` or at most `1/8`.
- The unit-cube feasible set has at most two points, and all feasible coordinates are rational.

The directed graph restriction refers to an edge from a defined variable to each variable in its right-hand side. It does not assert bounded treewidth or small connected components of the undirected constraint graph.

Here PosSLP is the decision problem of whether a circuit over integer constants `0,1` and operations `+,-,*` has strictly positive output. PosSLP is not known to be NP-hard, nor is it known to belong to P. The claim concerns approximation of the **limit**, not the cost of a prescribed finite number of FBBT sweeps or the computation of an approximately stationary box.

## 1. FBBT contains least monotone fixed-point computation

Let `P:R_+^n -> R_+^n` have polynomial coordinates with nonnegative coefficients. Suppose `x=P(x)` has a solution in `[0,1]^n`. Define `s^0=0` and `s^{k+1}=P(s^k)`. These iterates increase coordinatewise and are bounded by every nonnegative fixed point. Consequently they converge to a fixed point `q`, which is the least nonnegative fixed point and belongs to the unit cube.

**Lemma.** For the defining equations `x_i=P_i(x)`, exact FBBT with sound updates and fair forward interval propagation has limiting lower bounds `q`.

**Proof for complete expression updates.** Soundness preserves the feasible point `q`, so every lower vector `l` satisfies `l<=q`. Because coefficients and variables are nonnegative, the natural interval extension of `P_i` has lower endpoint exactly `P_i(l)`. A forward update therefore replaces `l_i` by at least `max(l_i,P_i(l))`. All lower bounds are nondecreasing.

For each integer `k`, there is a finite time after which `l>=s^k`. This is true for `k=0`. Once it holds for `k`, fairness ensures that each defining equation has a subsequent forward update after a finite time. At that time the corresponding bound is at least `P_i(s^k)=s_i^{k+1}`. After all equations have been updated, `l>=s^{k+1}`. Thus the lower limit is at least every `s^k`, hence at least `q`. Combined with soundness, it equals `q`. This argument needs no continuity of inverse contractors and no bounded delay in the fair schedule. □

For a lifted expression graph, apply the same lemma directly to the augmented monotone system. Every variable, including an arithmetic-node auxiliary, has a defining monotone equation. The constructions below ensure that the augmented system has a fixed point in the unit cube. This avoids any assumption that a whole expression is propagated in one step.

**Useful consequence.** On such systems FBBT obtains the exact coordinatewise minimum of the feasible set, since the same feasible point `q` attains every coordinate minimum. This is an exactness statement for the limiting lower bounds; it says nothing comparable about limiting upper bounds for arbitrary nonnegative systems.

## 2. A direct hardness construction

The arithmetic-circuit normalization and amplification idea below are adapted from Etessami and Yannakakis (2009), Theorem 5.2. The construction is written algebraically to establish the FBBT restrictions precisely.

### 2.1 Monotone circuits and their complements

Replace each gate `g` of a PosSLP circuit by two monotone gates `g+` and `g-` representing `g=g+-g-`. Addition and subtraction use the appropriate sums of positive and negative parts; multiplication uses

`(uv)+ = u+ v+ + u- v-`,

`(uv)- = u+ v- + u- v+`.

This increases circuit size by a constant factor. The question becomes whether two nonnegative integer circuit outputs `U,V` satisfy `U>V`.

Make both monotone circuits have a common depth `L>=1`, with every layer consisting entirely of additions or entirely of multiplications, alternating between the two. Insert identity operations `v+0` and `v*1` to pad edges and layers. Constants zero and one can themselves be carried through these layers. A polynomial increase in size suffices, and all gates have fan-in two.

Let `M_0=1`; at an addition layer put `M_l=2M_{l-1}`, and at a multiplication layer put `M_l=M_{l-1}^2`. These enormous integers are used only in the proof, not encoded in the instance. Each gate at level `l` is represented by two variables `p_g, r_g` whose unique values are

`p_g=value(g)/M_l`, `r_g=1-p_g`.

At input gates these variables are constants zero or one. At an addition gate with predecessor variables `p_j,p_k,r_j,r_k`, impose

`p_g=(p_j+p_k)/2`, `r_g=(r_j+r_k)/2`.

At a multiplication gate impose

`p_g=p_j*p_k`, `v_g=p_j*r_k`, `r_g=r_j+v_g`.

The complement identity follows from `1-p_j*p_k=(1-p_j)+p_j*(1-p_k)`. Every variable has its unique value in `[0,1]`. Every equation has at most three variable names. If a product would repeat the same name, create a fresh copy `h=p_j` and use `p_j*h`. These equations form an acyclic defining-equation graph.

Put `M=M_L`. Induction gives `M<=2^(2^L)`. Let `(p_U,r_U)` and `(p_V,r_V)` be the output pairs, and define

`c=(p_U+r_V)/2`, `d=(r_U+p_V)/2`.

Then `c+d=1` and

`c=1/2+(U-V)/(2M)`, `d=1/2-(U-V)/(2M)`.

### 2.2 One bounded feedback component detects the sign

Introduce the following four variables and equations:

`a'=a`, `t=a*a'`, `v=c*t`, `a=d+v`.

For fixed upstream `c,d`, their nonnegative fixed points correspond to solutions of

`a=d+c*a^2`.

Its least nonnegative root is `a*=1` if `c<=1/2`, and `a*=d/c` if `c>1/2`. This includes `c=0`, where the unique value is `1`, and `c=1`, where the least value is `0`. Thus

- If `U<=V`, then `a*=1`.
- If `U>V`, then, writing the positive integer `Delta=U-V`,

  `1-a*=2*Delta/(M+Delta)>=1/M`,

  since `1<=Delta<=M`.

The four displayed variables form the only feedback component at this stage. Every factor in a product has a distinct variable name, and every row has at most three variable names.

### 2.3 A second bounded component amplifies the gap

Build `b=2^(-2^(L+2))` by starting with `b_0=1/2` and performing `L+2` squarings. Construct a complement `r_b=1-b` using the same acyclic paired-product construction as above. In particular, the very small number `b` is represented by a polynomial number of equations, not by an exponentially long rational constant. The proof bound on `M` gives `b<=1/(8M)`.

Define `e=r_b*a`, and introduce

`w=e*z`, `z=b+w`.

At the least upstream fixed point, `e=(1-b)a*<1`, and this final component has unique solution

`z*=b/[1-(1-b)a*]`.

If `U<=V`, then `a*=1` and `z*=1`. If `U>V`, then

`z*<=b/(1-a*)<=b*M<=1/8`.

For rigor concerning the least fixed point of the full system: the displayed solution is in the unit cube, so it bounds the Kleene iterates and their least nonnegative fixed point `q`. All acyclic variables are uniquely fixed. The first feedback component of `q` must have `a=a*`, because `a*` is its least nonnegative root and the displayed solution bounds `q` from above. The final component then has the unique value `z*`. Thus `q` is precisely the displayed solution.

The final feedback component consists only of `z,w`. Every other new variable depends only on earlier components. The largest directed strongly connected component consequently has four vertices.

By the lemma, FBBT's limiting lower bound for `z` is exactly `z*`. An additive-`1/4` approximation lies at least `3/4` when `U<=V`, and at most `3/8` when `U>V`. Comparing with `1/2` decides PosSLP in polynomial time given such an approximation algorithm. □

The feasible-set restriction follows because the upstream circuit has unique rational values, the detector has only the rational roots `1` and `d/c` when `c>0`, and each admissible root uniquely fixes every remaining variable. There is one unit-cube feasible point when `U<=V`, and exactly two when `U>V`. Thus the hardness does not rely on irrationality of the limiting bounds.

The exact-arithmetic audit script [fbbt-hardness-check.py](../code/fbbt-hardness-check.py) checks the gate/complement identities, promised output gap, unit bounds, row arity, and directed SCC sizes for 50 small randomized layered circuits. These checks supplement the proofs; they do not replace them.

### 2.4 A unique rational feasible point

The same constant-error hardness holds for systems with a **unique rational feasible point** if one additional affine inequality is allowed.

Add a new defining equation `y=c*a` and the inequality `y<=1/2`. When `c<=1/2`, the only unit-cube detector root is `a=1`, and it satisfies the inequality. When `c>1/2`, the smaller root `a=d/c` has `y=d<1/2`, while the other root `a=1` has `y=c>1/2` and is excluded. The double-root case `c=1/2` is also retained. Thus the new feasible set is a singleton with rational coordinates.

The new constraint preserves the original least fixed point. Soundness therefore still bounds all original lower endpoints above by that point, while fair original forward updates bound their limit below by it. The limiting lower endpoint of `z` and its promised gap are unchanged. The new variable is downstream of the detector, so the directed SCC bound is unchanged. The model now consists of the nonnegative defining equations **plus one affine inequality**; the extra inequality is not itself claimed to be a defining monotone equation. This corollary also passed independent mathematical review.

## 3. What this establishes and what it does not

A polynomial-time extension of the known linear FBBT-limit computation to bilinear constraints, even with coarse additive error, would imply `PosSLP in P`. Bounded size of the nonlinear feedback components alone therefore does not bypass this complexity barrier. The difficulty can enter a small feedback component through values represented by a large acyclic arithmetic network.

The source hardness theorem also gives a polynomial reduction from the square-root-sum problem, through two-exit recursive Markov chains whose termination probabilities are least fixed points of nonnegative quadratic systems. The lemma therefore transfers that hardness to bilinear FBBT as well. The direct restricted construction above proves PosSLP hardness; square-root-sum hardness of the same restricted class follows at least under polynomial-time Turing reductions from the standard square-root-sum-to-PosSLP reduction. We do not need a stronger reduction convention here.

These instances do not establish practical difficulty of ordinary tolerance-stopped FBBT on process models. They establish a worst-case barrier for algorithms required to approximate the ultimate bounds with a certified additive error. A small change in successive bounds is not such a certificate.

## Sources and novelty boundary

- Belotti, Cafieri, Lee, and Liberti, *On feasibility based bounds tightening* (2012 preprint): [open paper](https://optimization-online.org/wp-content/uploads/2012/01/3325.pdf). Computes the exact FBBT limit for linear continuous constraints by an LP; discusses non-finite convergence.
- Bordeaux, Katsirelos, Narodytska, and Vardi, *The complexity of integer bound propagation*, JAIR 40, 2011: [author manuscript](https://www.cs.rice.edu/~vardi/papers/jair11.pdf). Section 3.4.1 connects continuous propagation to FBBT and gives LP tractability; Section 4 studies quadratic integer-propagation hardness. The integrality distinction matters here.
- Etessami and Yannakakis, *Recursive Markov chains, stochastic grammars, and monotone systems of nonlinear equations*, JACM 56(1), 2009, Theorem 5.2: [author manuscript](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf), [DOI](https://doi.org/10.1145/1462153.1462154). Established source of the circuit/sign/amplification reduction.
- Etessami, Stewart, and Yannakakis, *A polynomial time algorithm for computing extinction probabilities of multi-type branching processes*, SICOMP 46(5), 2017: [author manuscript](https://www.pure.ed.ac.uk/ws/portalfiles/portal/29051677/revised_sicomp_sub_after_rev_august16_v3_1.pdf). The contrasting normalized subclass `P(1)<=1` admits polynomial-time additive approximation of its least fixed point.

The reduction mechanism and monotone fixed-point theory are not claimed as new. The FBBT transfer and restricted statement are candidates for a new complexity theorem. Initial searches for FBBT/bound propagation together with PosSLP, square-root-sum, and monotone polynomial systems did not locate an earlier statement; this is evidence of a search gap, not a proof of novelty.
