# A compact SDP for the missing five-parameter quadratic cuts

Date: 2026-09-25. Status: exact algebra and cone equivalence independently
reviewed; publication priority remains unestablished.

The counterexample family in
[the three-variable note](three-positive-disjoint-counterexample.md) admits an
exact, compact separation formulation. Its infinitely many valid inequalities
are equivalent to one positive semidefinite matrix of order five with six
nonnegative auxiliary variables. The family cuts a rational point that satisfies
both the full disjoint-support SDP and all Anstreicher–Puges SOC strengthenings
of the extended triangle inequalities. This supplies a concrete strengthening;
completeness for the full three-variable hull is not established.

## 1. The valid family has broader parameters than its five-contact subclass

For `h∈R` and `d_1,d_2,d_3,k≥0`, define

\[
L=h-d_1x-d_2y+d_3z,\qquad D=d_1+d_2-h,
\]

\[
q_{h,d,k}=L^2+2d_3kz(1-x-y)+k(2D+k)xy.
\]

The following polynomial identity proves nonnegativity on the entire cube:

\[
\begin{aligned}
q_{h,d,k}={}&(L-kxy)^2
 +2d_3kz(1-x)(1-y)\\
&+k(2d_1+k)xy(1-x)
 +2kd_2xy(1-y)+k^2x^2y(1-y).
\end{aligned}
\]

Every term on the right is nonnegative for the stated parameters. In particular,
`h` is unrestricted in sign. The contact conditions
`0<h<min(d_1,d_2)` and `d_3>d_1+d_2-h+k` are needed for the exposed-ray subclass
studied in the other note, not for validity of this larger family.

Each square coefficient is `d_i²`. Therefore these cuts remain valid for the
joint hull with diagonal epigraph coordinates `Y_ii≥x_i²`; adding diagonal slack
can only increase the cut's left side.

## 2. Exact matrix representation

Let `m=(m_x,m_y,m_z)` and let `Y` denote candidate first and second moments,
with normalization `y_0=1`. Define

\[
b=\begin{pmatrix}-m_x\\-m_y\\m_z\\-Y_{xy}\end{pmatrix},
\qquad
B=\begin{pmatrix}
Y_{xx}&Y_{xy}&-Y_{xz}&Y_{xy}\\
Y_{xy}&Y_{yy}&-Y_{yz}&Y_{xy}\\
-Y_{xz}&-Y_{yz}&Y_{zz}&m_z-Y_{xz}-Y_{yz}\\
Y_{xy}&Y_{xy}&m_z-Y_{xz}-Y_{yz}&Y_{xy}
\end{pmatrix}.
\]

**Theorem.** The following statements are equivalent.

1. `L_y(q_{h,d,k})≥0` for every `h∈R` and every
   `v=(d_1,d_2,d_3,k)∈R_+^4`.
2. `B-bb^T` is copositive.
3. There exists a symmetric entrywise nonnegative `4×4` matrix `N`, with zero
   diagonal, such that

\[
\boxed{\begin{pmatrix}1&b^T\\b&B-N\end{pmatrix}\succeq0.}
\]

Consequently the entire family is enforced by six nonnegative scalar variables
and one affine LMI of order five. It uses only the original quadratic moment
coordinates; it introduces no cubic or quartic moment coordinates.

**Proof.** Direct coefficient comparison gives

\[
L_y(q_{h,d,k})=h^2+2h\,b^Tv+v^TBv.
\]

For a fixed nonnegative `v`, minimize over the unrestricted real scalar `h`.
The minimizer is `h=−b^Tv` and the minimum is `v^T(B-bb^T)v`. This proves the
equivalence of the first two statements, including the case `v=0`.

In order four, the copositive cone equals the sum of the positive semidefinite
cone and the entrywise nonnegative cone. This follows by duality from
`CP_4=DNN_4`; closedness of the dual sum follows, for example, because the PSD
and entrywise nonnegative cones have a common interior point. Thus statement 2
is equivalent to `B-bb^T-N⪰0` for some entrywise nonnegative symmetric `N`.
Any nonnegative diagonal of `N` can be moved into the PSD summand, so its diagonal
may be set to zero. The Schur complement of the top-left entry one gives exactly
statement 3. ∎

This is an SDP **lift**, not a single LMI in the original variables alone.
The auxiliary matrix `N` is part of the formulation; no minimal-lift-size claim
is made. Setting `N=0` would generally impose a stronger condition without
this validity proof. For example, the genuine cube atom `(x,y,z)=(1/2,1/2,0)`
has `(B-bb^T)_{11}=0` but `(B-bb^T)_{14}=1/8`, so `B-bb^T` is not PSD.
The auxiliary matrix is therefore needed to avoid excluding valid cube moments,
even though no lower bound of six on its number of entries is asserted.

## 3. Separation and symmetry

At a proposed moment point, let `A=B-bb^T`. Family membership can be checked by
the displayed feasibility SDP. An equivalent normalized separation problem is

\[
\min\{\langle A,W\rangle:W\succeq0,\ W\ge0\text{ entrywise},\
\operatorname{tr}(W)=1\}.
\]

The feasible set is compact and has a strictly feasible point. Its optimum is
negative exactly when a family inequality is violated, because `DNN_4=CP_4`.
To obtain an individual parameter vector from a negative matrix `W`, take a
completely positive decomposition `W=Σ_rv_rv_r^T` with `v_r≥0`. At least one
summand has `v_r^TAv_r<0`; choose that vector and set `h=−b^Tv_r`. A DNN matrix
returned by the SDP is an aggregate certificate. Extracting one vector requires
this additional decomposition step; it should not be claimed to happen
automatically from an arbitrary optimizer.

Coordinate permutations and coordinate complements `x_i↦1−x_i` preserve the
box and induce affine transformations of its first and second moments. Applying
the construction to these transforms gives additional valid family blocks.
Swapping `x` and `y` only swaps `d_1` and `d_2`, so that symmetry gives duplicate
families. No claim is made that all symmetry copies together describe the full
quadratic hull.

For a large sparse problem, a chosen triple can receive such a block when its
three edge moments are present. Introducing missing edge moments is an additional
modeling decision, with associated formulation cost. The present theorem proves
validity and exact enforcement of the family, not a solver-speedup guarantee.

## 4. Exact separation of the known relaxation point

Take the rational moment point tabulated in the counterexample note. With

\[
h=\tfrac12,\qquad(d_1,d_2,d_3,k)=(1,1,3,1),
\]

the family member is

\[
x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+\tfrac14,
\]

and its evaluated value is `−1/40`. Hence this point fails the family LMI.
For the same fixed `v`, the optimizing value of `h` is `2361/5000`, giving the
slightly stronger violation `−644321/25000000`.

The rational point satisfies all 27 matrices in Khajavirad's full three-variable
disjoint-support relaxation strictly. It also satisfies the diagonal upper
bounds required by the compact box moment hull and all the SOC constraints
(15)–(16) of
[Anstreicher and Puges](https://arxiv.org/html/2501.09150v1), including their
coordinate permutations and complements. The exact minimum SOC slacks are
`2831/4000000` for the 24 constraints of type (15), and
`124813/12500000` for the 48 constraints of type (16). Their multilinear
constraints (14) are the eight scalar inequalities already present in the full
disjoint formulation. Their Lemmas 4–5 show that these SOC constraints imply all
ETRI1, ETRI2, and ETRI3 inequalities.

Thus intersecting either of those relaxations with this family LMI is a strict
strengthening. This comparison does not assert that the isolated family LMI
dominates every constraint of either existing relaxation.

## 5. Prior theory, verification, and remaining questions

The cone identity in order four is classical. The exact SDP lift of the complete
three-variable box moment hull via six tetrahedra is also classical; see
[Anstreicher and Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf).
[Burer and Dong, Section 5.3, Corollary 3](https://optimization-online.org/wp-content/uploads/2010/05/2621.pdf)
also give complete separation for the homogeneous three-variable box moment
cone using boundary recursion. Thus the present construction is neither the
first exact lift nor the first separation method for the whole three-variable
hull.
The contribution investigated here is the particular valid parameter family,
its exact compact enforcement, and the proved separation from the newer
disjoint-support and extended-triangle SOC relaxations. The known six-tetrahedron
lift already implies every cut in this family.

Independent reviews cover the
[family identity and LMI equivalence](three-positive-family-lmi-review.md)
and a fresh [publication proof audit](publication-quadratic-proof-audit.md).
The [publication assessment](publication-quadratic-assessment.md) consolidates
the current-source comparisons, exact claim scope, and verification. Its
linked priority audit and the earlier
[priority and significance review](three-positive-family-priority-review.md)
compare the closest inspected families and exact formulations. Publication
priority is not proved by the absence of a matching search result.

Targeted checks actually run include exact symbolic expansion of the family
identity and of `h²+2h b^Tv+v^TBv`, and

```
python research-20260925/checks/three_positive_gap_certificate.py
```

The latter uses rational arithmetic for every disjoint matrix and every
Anstreicher–Puges SOC inequality just described. It does not check the external
cone theorem or establish completeness of the new family. No project-wide or
CI verification was run.

The central next question is whether the disjoint formulation plus the symmetry
copies of this family is complete for three positive variables. Possible routes
include an extreme-ray classification or a further exact counterexample;
randomized numerical success would not be sufficient. Practical assessment also
needs a comparison between adding selected family blocks, generating individual
cuts, and imposing the established six-simplex lift.
