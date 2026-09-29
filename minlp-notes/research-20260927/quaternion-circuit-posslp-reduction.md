# PosSLP through signs of rational unit-quaternion circuits

Date: 2026-09-28. Status: passed
[two](quaternion-circuit-posslp-fresh-adversarial-review.md)
[fresh independent adversarial reviews](quaternion-circuit-posslp-reduction-review.md).
Publication priority is unestablished.

A circuit using multiplication and inversion of rational unit
quaternions can encode the sign of an arbitrary integer arithmetic
circuit. Every intermediate quaternion has norm one and rational
coordinates. The reduction uses a fixed finite set of rational unit
constants; its output's selected coordinate is promised nonzero.

Together with the reviewed polynomial-size quartic realization of unit-quaternion
circuits, this gives PosSLP-hard comparison of a coordinate of a
promised rational unique minimizer of a globally strongly SOS-convex
rational quartic. That application concerns optimizer-coordinate
comparison. It does not by itself give a rational-minimizer promise
for the quartic obtained by subsequently perturbing its objective.

## Statement and quaternion notation

Write a quaternion as \(q=(w,v)=(w,x,y,z)\), with multiplication
\[
 (w,v)(s,u)=(ws-v\cdot u,\;wu+sv+v\times u).
 \tag{1}
\]
A unit quaternion has \(w^2+\|v\|^2=1\), inverse
\(\bar q=(w,-v)\), and multiplicative Euclidean norm.
Let \(\mathbf1=(1,0,0,0)\), \(\mathbf i=(0,1,0,0)\),
and
\[
 c=(1,1,1,1)/2,\qquad t=2^{-20},\qquad
 q_0=\left(\frac{1-t^2}{1+t^2},\frac{2t}{1+t^2},0,0\right).
 \tag{2}
\]
These are fixed rational unit quaternions. Define conjugations
\[
 T(q)=\mathbf i q\mathbf i^{-1}=(w,x,-y,-z),\qquad
 R(q)=cqc^{-1}=(w,z,x,y).
 \tag{3}
\]
Thus \(R\) cyclically sends the vector axes
\(\mathbf i\mapsto\mathbf j\mapsto\mathbf k\mapsto\mathbf i\).

**Theorem.** Given an integer straight-line program using
\(0,1,+,-,\times\), one can construct in polynomial time a circuit
with constants only \(\mathbf1,\mathbf i,c,q_0\), and gates
quaternion multiplication and inversion, such that its final
\(\mathbf i\)-coordinate is nonzero and has the sign of
\(2V-1\), where \(V\) is the integer input output. Consequently,
positivity of that coordinate is PosSLP-complete, even with the stated
nonzero promise and the fixed constant set.

All sizes refer to shared directed acyclic circuits. Expanding a
circuit into a word or expanding all rational coordinates is not part
of the reduction.

## Exact projection and commutator identities

Define
\[
 P(q)=qT(q),\qquad
 A(q,r)=P(qr),\qquad
 M(q,r)=P\bigl(R([q,R(r)])\bigr),
 \quad [q,r]=qrq^{-1}r^{-1}.
 \tag{4}
\]
For every unit quaternion,
\[
 P(w,x,y,z)=\bigl(1-2x^2,\;2wx,\;2xz,\;-2xy\bigr).
 \tag{5}
\]
In particular, \(P(q)=\mathbf1\) whenever \(x=0\).
The map preserves the sign of \(x\) when \(w>0\), and
suppresses the transverse vector components near the identity.

For unit \(q=(w,v)\), \(r=(s,u)\),
\[
 [q,r]-\mathbf1=(qr-rq)\bar q\bar r
                    =2(0,v\times u)\bar q\bar r.
 \tag{6}
\]
Hence
\[
 \|[q,r]-\mathbf1\|\leq2\|v\|\|u\|.
 \tag{7}
\]
If \(w,s\geq0\), then
\(\|q-\mathbf1\|\leq2\|v\|\) and
\(\|r-\mathbf1\|\leq2\|u\|\). Subtracting the leading
term from (6) gives
\[
 \|[q,r]-\mathbf1-2(0,v\times u)\|
       \leq4\|v\|\|u\|(\|v\|+\|u\|).
 \tag{8}
\]
The exact vanishing in (6) prevents an error independent of either
input signal. We will nevertheless use absolute leading-term error
bounds, which also cover cancellation to zero in an arithmetic gate.

For a unit quaternion with \(w\geq0\) and \(\|v\|\leq1/2\),
(5) gives the elementary bound
\[
 \|\operatorname{vec}P(q)-2x\mathbf e_1\|
                         \leq4\|v\|^2,
 \tag{9}
\]
since \(|w-1|\leq\|v\|^2\). Here
\(\operatorname{vec}\) denotes the three imaginary coordinates.

## Generating a doubly small rational signal

Suppose a unit quaternion has positive scalar part and
\[
 0<x\leq2^{-16},\qquad \sqrt{y^2+z^2}\leq64x^2.
 \tag{10}
\]
Then \(\|v\|\leq2x\). Let \(U=R([q,R(q)])\).
The selected coordinate of the rotated cross product in (8) is
\(2(x^2-yz)\). Therefore
\[
 |U_x-2x^2|\leq4096x^4+64x^3\leq65x^3,
 \quad x^2\leq U_x\leq3x^2,
 \quad \|\operatorname{vec}U\|\leq8x^2.
 \tag{11}
\]
The scalar part \(U_w\) is at least \(1-8x^2>1/2\), by
(7). Thus the selected coordinate \(x'\) of \(M(q,q)=P(U)\)
satisfies
\[
                        x^2\leq x'\leq6x^2.
 \tag{12}
\]
Its transverse coordinates have norm at most
\[
 2|U_x|\sqrt{U_y^2+U_z^2}
             \leq48x^4\leq64(x')^2.
 \tag{13}
\]
The scalar part of \(P(U)\) is positive by (5). Since
\(6x^2\leq x\), this proves that (10) is preserved.

The fixed \(q_0\) in (2) satisfies (10), with
\(0<x_0<2^{-19}\). Iterate \(q_{j+1}=M(q_j,q_j)\).
By (12),
\[
 0<x_j\leq(6x_0)^{2^j}/6<2^{-16\cdot2^j},
 \qquad
 \|\operatorname{vec}q_j-x_j\mathbf e_1\|\leq64x_j^2.
 \tag{14}
\]
Each iteration uses a fixed number of group operations. It produces a
positive extremely small rational coordinate with a short exact
circuit. The rational coordinate is never expanded.

## A uniform leading-term estimate for arithmetic gates

Fix \(0<\delta<1\). A signal of order \(d\geq1\), coefficient
\(C\in\mathbb Z\), and bound \(B\geq1\) is a unit quaternion
with positive scalar part such that
\[
 |C|\leq B,\qquad
 \|\operatorname{vec}q-C\delta^d\mathbf e_1\|
                            \leq B\delta^{d+1}.
 \tag{15}
\]
In particular, \(\|\operatorname{vec}q\|\leq2B\delta^d\).
The coefficient is allowed to be zero.

If two input signals have bound \(B\) and \(B\delta\leq2^{-30}\),
the following operations give signals with bound
\[
                              B'=2^{20}B^4:
 \tag{16}
\]

- \(q^{-1}\) has coefficient \(-C\) and the same order.
- \(P(q)\) has coefficient \(2C\) and the same order.
- If both inputs have order \(d\), then \(A(q,r)\) has
  coefficient \(2(C+D)\) and order \(d\).
- For orders \(a,b\), \(M(q,r)\) has coefficient \(4CD\)
  and order \(a+b\).

Here are explicit error bounds proving the assertion. Inversion changes
only the sign of the vector. For \(P\), (9) gives an error coefficient
at most \(2B+16B^2\leq18B^2\).

For addition, the vector of \(qr\) differs from
\((C+D)\delta^d\mathbf e_1\) by at most
\[
 (2B+4B^2+16B^3)\delta^{d+1}.
\]
The terms come, respectively, from the inherited vector errors, the
cross product, and the scalar parts minus one. Also
\(\|\operatorname{vec}(qr)\|\leq5B\delta^d\).
After applying (9), the error coefficient is at most
\(4B+108B^2+32B^3\leq144B^3\).

For multiplication, the cross product of the two input vectors, with
the second cyclically rotated, differs from
\(CD\delta^{a+b}\mathbf e_3\) by at most
\(3B^2\delta^{a+b+1}\). Equations (7)--(8), followed by the
cyclic rotation, show that the vector of
\(U=R([q,R(r)])\) differs from
\(2CD\delta^{a+b}\mathbf e_1\) by at most
\[
 (6B^2+64B^3)\delta^{a+b+1},
 \qquad \|\operatorname{vec}U\|\leq8B^2\delta^{a+b}.
\]
After (9), the error coefficient is at most
\(12B^2+128B^3+256B^4\leq396B^4\).
All these bounds and the new leading coefficients fit (16).
The input smallness bound ensures the scalar parts of \(qr\),
\(U\), and the final signals are positive, and ensures all uses
of (9) have vector norm below \(1/2\). Thus the estimates do not
assume positivity that the operations could destroy.

## Homogeneous simulation of integer arithmetic

First append gates to the input integer circuit so its output is
\(W=2V-1\). This is always a nonzero integer and is positive
exactly when \(V>0\).

Represent each integer gate value \(V_i\) by a pair of quaternion
signals \((f_i,g_i)\), of a common order \(d_i\), whose leading
coefficients are \((C_i,D_i)\) with
\[
                D_i\in\mathbb Z_{>0},\qquad C_i=D_iV_i.
 \tag{17}
\]
Once the small signal \(q\) has been chosen, initialize one by
\((q,q)\), and zero by \((\mathbf1,q)\), with order one.
For an integer multiplication gate, use
\[
          f_i=M(f_a,f_b),\qquad g_i=M(g_a,g_b).
 \tag{18}
\]
The leading coefficients become \((4C_aC_b,4D_aD_b)\), and
both orders become \(d_a+d_b\).
For addition or subtraction, use
\[
 \begin{aligned}
 u&=M(f_a,g_b),&v&=M(f_b,g_a),\\
 f_i&=A(u,v)\quad\text{or}\quad A(u,v^{-1}),&
 g_i&=P(M(g_a,g_b)).
 \end{aligned}
 \tag{19}
\]
Both leading coefficients acquire the common factor eight:
\[
       C_i=8(C_aD_b\pm C_bD_a),\qquad D_i=8D_aD_b.
\]
All orders again agree. Thus (17) is preserved, including when an
integer gate value is zero.

Let \(T\) count all signal operations \(M,A,P,\mathrm{inverse}\)
in this compiler, before choosing \(q\). It is polynomial in the
integer input length. Set
\[
 B_0=128,\qquad B_j=2^{20}B_{j-1}^4.
\]
A direct calculation gives
\[
                 \log_2B_j=(41\cdot4^j-20)/3<14\cdot4^j.
 \tag{20}
\]
Now choose the initial signal \(q=q_r\) generated by (14), with
\(r=2T+2\), and define \(\delta=(q_r)_x\). The parameter
is defined by its circuit, not expanded or approximated. By (14),
\[
 0<\delta<2^{-64\cdot4^T}\leq2^{-30}/B_T.
 \tag{21}
\]
Equation (14) verifies the initial signal bound (15) with \(B_0\).
Induction through the compiler using (16) proves (15) at every signal,
with its relevant \(B_j\); previously constructed signals also
satisfy any larger bound. The smallness hypothesis holds throughout
by (21).

At the final numerator signal, \(C=D W\) is a nonzero integer.
Its selected coordinate is
\[
                      x=C\delta^d+e,
                  \qquad |e|\leq B_T\delta^{d+1}
                                 <\tfrac12\delta^d.
 \tag{22}
\]
Therefore \(x\ne0\) and \(\operatorname{sign}x=\operatorname{sign}W\).
This proves the claimed many-one lower reduction. The number of raw
quaternion gates is \(O(T+r)\), since each macro has constant size.
All constants are fixed rational unit quaternions.

## Upper reduction and scope

For the matching upper reduction, maintain the four integer numerators
and a common positive integer denominator at each quaternion gate.
Multiplication multiplies the two positive denominators and forms the
four bilinear integer numerators from (1). Inversion negates the three
vector numerators and leaves the denominator unchanged. The fixed
constant numerators and denominators have constant-size integer
straight-line programs. Thus the selected output coordinate has the
sign of one polynomial-size integer straight-line program. This gives
one PosSLP query, and completes the completeness proof.

The lower reduction uses a nonzero selected output. Other coordinates
and intermediate signals may be zero. Norm one is exact at every raw
gate, not merely an interval promise. The result concerns shared
circuits, not explicitly listed products of polynomially many matrices.
It does not state that equality to the group identity is PosSLP-hard;
compressed group identity and the sign of a coordinate are different
questions.

The commutator mechanism has close prior in Solovay--Kitaev constructions,
and matrix-circuit simulation of arithmetic has substantial older
literature. The [primary comparison](quaternion-circuit-posslp-prior.md)
records those precedents and qualifies novelty. The
[coordinate-comparison consequence](rational-optimizer-posslp-coordinate-comparison.md)
combines this compiler with the independently reviewed quartic
realization. No solver speedup or publication priority follows merely
from the completeness classification.

## Verification

The fresh review independently reconstructed every quaternion identity,
the positive small-signal generator, the uniform bounds, cancellation
handling, the factor-four and factor-eight updates, and both complexity
reductions. It required no mathematical correction. A second independent
reviewer checked the proof and wrote an exact rational stress checker,
which the author also ran:

```text
python research-20260927/check_quaternion_signal_bounds_review.py
```

It passed 36 generator cases, 900 arithmetic-gate cases, 240 cases where
an output remains nonzero after its leading coefficients cancel, and
30 parameter comparisons. A separate narrow symbolic audit verified
the projection, rotation, commutator, and pure-axis product identities;
its scope is recorded in the fresh review. The uniform proof, not the
finite cases, establishes arbitrary circuit size and polynomial output
length. No Lean, project-wide verification, or CI inspection is claimed.
