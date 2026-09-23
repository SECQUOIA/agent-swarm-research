# Joint nomination and resistance uncertainty on bounded-rank blocks

Date: 2026-09-05. Status: archived exploratory route, superseded by the twice-reviewed [joint nomination/resistance theorem](../results/potential-flow-joint-resistance.md). Its separate sign-pattern derivation is not used by that theorem and is not promoted as an independently established result. This builds on the independently checked [bounded-block-cycle-rank candidate](potential-flow-block-cycle-rank-investigation.md), whose own novelty review is separate.

## Candidate claim and scope

Fix a bound `r` on the cycle rank of every biconnected block. Let the physical law be

```
pi_u-pi_v=beta_e x_e|x_e|,
0<beta_lower_e<=beta_e<=beta_upper_e,
l_v<=b_v<=u_v,    sum_v b_v=0,
l_v<=0<=u_v.
```

All bounds are rational; resistance boxes are independent. Optimize `pi_s-pi_t` jointly over both nominations and resistances. The proposed claim is a certified additive optimal-value interval and rational epsilon-optimal nomination/resistance vectors in time polynomial in input bit length and requested precision bits, for fixed `r`.

Unlike the fixed-resistance theorem, this candidate assumes every original nomination interval contains zero. This sign condition is used to control physical flow reversals on long paths. It includes ordinary entry/exit booking intervals and survives off-path aggregation, but it does not include arbitrary shifted original nomination boxes. Local entrance/exit intervals can still become shifted after fixing outside nominations; those two vertices are marked topological core vertices and are excluded from the path sign argument.

No extra pressure, arc-capacity, valve, or compressor constraints are included. Exact threshold comparison and probability distributions are outside the claim.

## The one-active-nomination-block reduction survives joint uncertainty

For each smoothed joint optimum, fix its resistances when applying first-order optimality in the nomination variables. The electrical adjoint still yields one multiplier and ordered block ranges. Thus all nominations before one block are at their aggregated upper bounds, and all after it at their lower bounds. Compactness of the joint nomination/resistance boxes and positive resistance lower bounds permits the smoothing limit. There is therefore an original joint optimum in one of the linearly many selected-nomination-block faces.

Fix such a face. Its active block has a fixed total nomination despite variation of internal nominations. Every other block has fixed effective nominations. The physical solution of a block depends on its own resistances and effective nominations only, so resistance optimization separates by blocks. The global objective is the sum of the separately optimized inactive-block drops and the selected block's joint nomination/resistance optimum.

Internal effective nominations of a block strictly before the active block are nonnegative, because they are upper interval bounds. Those strictly after it are nonpositive. Boundary totals at a block's entrance and exit may have the opposite sign and are treated as terminals.

## Resistance derivatives and few interior resistances

Inside a local block, apply the law smoothing and positive-internal-source objective perturbation from the rank candidate. Let `h` be its adjoint and let

```
j_h,e=(h_u-h_v)/[beta_e(2|x_e|+rho)].
```

Implicit differentiation at fixed nominations gives

```
partial F_delta,rho / partial beta_e
       = j_h,e [x_e|x_e|+rho x_e].           (1)
```

The sign is positive because increasing resistance at fixed potential differences reduces physical flow, so the compensating load-preserving potential derivative has right-hand side `B diag(1/phi') psi(x)`.

At a joint maximum, (1) implies

```
j_h,e x_e>0  -> beta_e=beta_upper_e,
j_h,e x_e<0  -> beta_e=beta_lower_e.
```

An interior resistance therefore requires `x_e=0` or `j_h,e=0`. If `x_e=0`, changing that resistance to its lower endpoint does not change any physical equation or the objective, since the edge's constitutive drop remains zero. Do this for every zero-flow edge. The resulting point is still a perturbed global optimum; its recomputed adjoint and KKT multiplier can be used afresh.

On every maximal degree-two path, the positive adjoint injections imply `j_h,i-j_h,i-1=delta>0`. At most one edge of that path has zero adjoint current. Hence at most one resistance per maximal path must be left free after all zero-flow resistances have been moved to a bound. Since there are `O(r)` paths, at most `O(r)` resistances remain free.

## Only constantly many resistance-bound switches per path

The active block's nomination KKT pattern is lower/free/upper/free/lower along a maximal path, with at most two free pivots. For all non-core internal vertices, original and aggregated bounds satisfy `l_v<=0<=u_v`. Physical conservation in path order is

```
x_i-x_i-1=b_vi.
```

Thus the physical edge-current sequence is nonincreasing on the first lower segment, nondecreasing on the upper segment, and nonincreasing on the final lower segment. Each free pivot adds at most one unrestricted jump. A coarse bound partitions the edge sequence into at most five monotone pieces; each such piece has at most three constant sign runs (`negative`, `zero`, `positive`, in either order). Consequently there are at most 15 constant-sign runs of physical flow.

The adjoint-current sequence is strictly increasing, so it has at most three sign runs, and its zero run has length at most one. Refining these two sign partitions produces at most 17 runs. On each nonzero-product run the resistance is fixed to a particular endpoint by (1). Zero-physical-flow resistances have been set to the lower endpoint. A nonzero-physical-flow, zero-adjoint-current edge is the only possible free resistance on that path. Thus resistance states (`lower`, `upper`, or the one optional `free` edge) have only a constant number of changes, independently of path length. The coarse bound of 17 runs suffices; it is not asserted to be sharp.

Enumerate all path nomination patterns and all resistance-state sequences with at most 17 runs and at most one free edge. This is `n^{O(1)}` per path and `n^{O(r)}` for the block. It is acceptable that many enumerated faces do not arise from any adjoint: each remains a feasible-domain subset, while the argument proves that one contains an optimum.

For inactive blocks, each internal nomination has one fixed sign throughout the block. Physical path currents are monotone, so the resistance-state enumeration is simpler; the same coarse bound remains valid. The positive-internal-source objective perturbation is used independently in each inactive resistance-only block optimization to remove flat adjoint paths.

## Local fixed-dimensional algebraic optimization

On a retained active face, at most `8r-2` nominations, at most `3r-1` resistances, and `r` circulation variables remain. Eliminating one nomination by balance leaves at most `12r-4` variables. For inactive blocks, at most `3r-1` resistances and `r` circulations remain. Bridge blocks and zero-free-coordinate cases bypass these formulas and are handled directly.

Every edge flow is affine in the nomination and circulation variables, independently of resistances. The zero-flow hyperplanes form a polynomial-size arrangement in fixed dimension. On a sign cell, each loop equation and the local objective are polynomials of degree at most three, since the law multiplies a resistance variable by a signed quadratic flow polynomial. Resistance bounds, nomination bounds, and sign constraints are rational polynomial inequalities. All variables have polynomial-size rational bounds: nominations and resistances are boxed, and fundamental-cycle circulation coordinates equal chord flows bounded by total possible injection.

Fixed-dimensional real algebraic decision and sampling therefore yield local value intervals and algebraic near-optimal points in polynomial bit time for fixed `r`. Use uniformly vanishing objective and law perturbations only to prove the existence of an optimal face; the enumerated systems use the original unperturbed law. Summing certified block-value intervals gives the overall value interval.

## Joint Lipschitz bound for rational recovery

Let `B=sum_v max(|l_v|,|u_v|)` on the aggregated core and fix a simple `s-t` path `P`. The fixed-resistance bound can be made uniform over the resistance box:

```
C_b=2B sum_{e in P} beta_upper_e.
```

For the original unperturbed terminal-difference objective, its smoothed adjoint has exactly one unit source and one unit sink. Electrical currents are acyclic and have absolute value at most one. Equation (1) with `delta=0` gives

```
|partial F_0,rho / partial beta_e| <= B^2+rho B.
```

Integrate along resistance-box segments and pass to zero smoothing. Combining this with the nomination bound yields

```
|F(b,beta)-F(c,gamma)|
   <= C_b ||b-c||_1+B^2 ||beta-gamma||_1.    (2)
```

All constants have polynomial rational encoding length. Refine algebraic coordinates into short rational isolating intervals, intersect with original nomination bounds and exact balance, and solve the resulting rational LP. Resistance coordinates can be chosen rationally inside their individual interval intersections. Equation (2), with an explicit per-block error allocation, bounds total objective loss. Off-path resistances can be set to any rational box value because they do not affect the core objective.

## Review targets

The candidate is not yet a theorem. Independent review should check the sign in (1), whether moving all zero-flow resistances preserves the perturbed optimum and its usable KKT structure, the constant sign-run bound with free nomination pivots, the inactive-block separation after fixing the active nomination face, and joint rational recovery. A dedicated novelty search against uncertain-friction robustness literature is also needed.

## Reproducible evidence

[`code/potential_flow_mpd/joint_resistance_checks.py`](../code/potential_flow_mpd/joint_resistance_checks.py) passed 48 independent nonlinear finite-difference checks of the resistance derivative formula (maximum error `7.87e-10`) and 2,000 exact rational long-path checks of physical-sign and resistance-state runs. The largest observed counts were seven physical sign runs and six resistance-state runs, within the coarse proof bounds 15 and 17. It also verifies a zero-flow example in which changing that edge's resistance preserves all physical variables while changing the adjoint; the proof's instruction to recompute KKT data is necessary.

Run with `/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/joint_resistance_checks.py`. These checks establish neither global correctness nor novelty of the unreviewed candidate.
