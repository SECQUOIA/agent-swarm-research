# Candidate: a one-bit gap for two convex outputs with box error

Date: 2026-09-05. Status: the final degree-32 construction and exact product
counts passed two independent proof reviews and were promoted to
`results/convex-polynomial-box-error-exact-integer-gap.md`. This file keeps
the earlier hinge and polynomial variants as supporting investigation.
The result does not settle an unbounded gap with one input and growing
output dimension.

The stronger constant choice in the section below gives an exact growing-input
product law: `p_conv=n` and `p_bin=ceil(n log2 3)` for `n` inputs and `2n`
convex degree-32 outputs with unit box error. This does not change the
one-input open boundary.

Use unit componentwise error on the input interval `[0,1]`. Put
`a=1/8`, `A=3/2`, and define the two convex piecewise linear functions

```
F_1(x)=A max(1-x/a,0),
F_2(x)=A max((x-1+a)/a,0).
```

The graph has three affine pieces: a left piece on `[0,a]`, a zero middle
piece on `[a,1-a]`, and a right piece on `[1-a,1]`.

## One unrestricted integer suffices

Let `S_0,S_1,S_2` be these exact graph segments with appended integer
coordinates `z=0,1,2`, respectively. Set `C=conv(S_0 union S_1 union S_2)`.
This is a rational polytope. Impose `z in Z`; its only possible values
are zero, one, and two.

At `z=0` or `z=2`, the corresponding projection is just the exact outer
graph segment. At `z=1`, any convex combination has weights `t,1-2t,t`
on the three segments, with `0<=t<=1/2`. Conditional points within each
segment can be consolidated because those segments are convex. The mean
of an outer pair has input in `[(1-a)/2,(1+a)/2]`, a subset of
`[a,1-a]`. Together with the middle input, the resulting input therefore
lies in `[a,1-a]`, where both components of `F` vanish. The two admitted
outputs lie in `[0,tA]`, hence in `[0,3/4]`. Thus every integer slice has
componentwise error at most `3/4`, and it contains the entire graph.

This is already a rational MILP: one can use convex-combination weights
on the six endpoints of the three labeled graph segments. All endpoint
weights are continuous; only `z` is declared integer.

## Two binaries are necessary and sufficient

Consider exact graph witnesses at inputs `0,1/2,1`. A single convex binary
fiber cannot contain any pair of them. For the pair `0,1/2`, the first
component chord at input `a` is `A(1-2a)=9/8`, while `F_1(a)=0`. The
pair `1/2,1` has the symmetric obstruction in component two. For the pair
`0,1`, the first component chord at `a` has value `A(1-a)=21/16>1`.
Any one-bit formulation has only two fibers, so two of the three exact
witnesses must share a fiber, contradicting one of these tests.

Conversely, a three-way binary disjunction of the exact graph segments
uses two bits. The same chord obstruction rules out a zero-integer convex
lift. Consequently the proposed exact finite counts are

```
p_conv(F,[-1,1]^2)=1,     p_bin(F,[-1,1]^2)=2.
```

## A simple degree-32 rational convex polynomial version

An exact low-degree construction avoids any approximation dependency. Put

```
Q(x)=(A(1-x)^32,A x^32),  A=3/2,
c=1/32,  L=A(1-c)^32,  d=A c^32.
```

Direct rational inequalities give `1/2<L<3/4`, `0<d<1/4`.
Form three rational boxes in `(x,w_1,w_2)`:

```
B_0=[0,c] x [L,A] x [0,d],
B_1=[c,1-c] x [0,L] x [0,L],
B_2=[1-c,1] x [0,d] x [L,A].
```

Each box contains its full portion of the polynomial graph. At `B_0` and
`B_2`, component ranges have width at most `A-L<1`; hence those boxes
already satisfy unit graph error. The middle box has error at most `L<1`.

Append labels `z=0,1,2` and take their convex hull. At integer `z=1`, the
outer weights again equal `t<=1/2`; its input remains in `[c,1-c]` because
`c<=1/3`. Every admitted output coordinate lies between zero and

```
max(L,(A+d)/2)<1.
```

Every true output on that input interval lies between zero and `L<1`.
Thus their absolute difference is strictly below one, including all
convex combinations between the boxes. At integer zero or two only the
corresponding box remains. This gives a rational polyhedral one-integer
outer formulation for the entire polynomial graph.

The same three witnesses `0,1/2,1` require different binary fibers.
For the first pair, the first-component chord error at `x=1/8` is

```
g=(3/4)A+(1/4)A/2^32-A(7/8)^32 > 1.
```

The last pair is symmetric. The outer-pair error in component one is
larger, since its chord value there is `(7/8)A` whereas the displayed
first-pair chord is `(3/4)A+(1/4)A/2^32`. Consequently

```
p_conv(Q,[-1,1]^2)=1,     p_bin(Q,[-1,1]^2)=2.
```

Two binaries suffice by selecting the three boxes. All numerical tests
above are strict rational inequalities. An independent exact-fraction
calculation gave `L=0.5430829338844748...` and `g=1.1040902445307867...`;
the decimal values are explanatory only. Both outputs are convex
polynomials. Adding the affine function `48x` to the first makes both
outputs nondecreasing without changing the graph-error or integer-count
arguments. It does not make their monomial coefficients all nonnegative.

## Exact product counts with a two-thirds obstruction

Use instead `A=7/4`, `c=1/48`, still with degree 32, and define the same
`Q=(A(1-x)^32,A x^32)`, `L=A(1-c)^32`, and `d=A c^32`.
The exact rational inequalities are

```
A-1<L<1,    (A+d)/2<1.
```

Numerically `L=0.8921747063928608...`, `A-L=0.8578252936071392...`.
Use the same three rational boxes and labels as above. At the outer
integer slices, their error is at most `A-L<1` and `d<1`. At the middle
integer slice the input remains in `[c,1-c]`, every output belongs to
`[0,max(L,(A+d)/2)] subset [0,1)`, and every true component is in `[0,L]`.
The one-integer formulation is therefore valid.

Now the three witnesses have forbidden **thirds** combinations. For
inputs `0,1/2`, give weight `2/3` to zero and `1/3` to one-half. At
`x=1/6` the first-component error is

```
g=(2/3)A+(1/3)A/2^32-A(5/6)^32>1.
```

The rational value is `1.1615470415192186...`. The pair `1/2,1` has the
symmetric obstruction with weight `2/3` on one. For the pair `0,1`, give
weight `2/3` to zero: its first-component error at `1/3` is

```
(2/3)A-A(2/3)^32 > g >1.
```

The first inequality is equivalent to
`(5/6)^32-(2/3)^32 > (1/3)2^(-32)`, another strict rational inequality.
Consequently the one-input exact counts remain `p_conv=1`, `p_bin=2`.

For `n>=1`, take independent inputs `x_i in [0,1]` and output the two
components of `Q(x_i)` for every input. The error body is `[-1,1]^(2n)`.
The product of the one-integer formulations gives `p_conv<=n`.

Choose all `3^n` input vectors in `{0,1/2,1}^n`. Every pair differs in a
coordinate, and the preceding thirds obstruction applies to that input
coordinate and one of its two outputs. Select one exact graph witness for
each input in an arbitrary `p`-integer convex lift. If two integer codes
agree modulo three, both thirds combinations are integral. Choosing the
orientation of the forbidden combination contradicts validity. Thus all
`3^n` codes have different residues modulo three, and `3^p>=3^n`, so
`p>=n`.

For a binary lift, two witnesses with the same binary code admit every
convex weight. Hence every one of the `3^n` witnesses requires its own
binary code, giving `p_bin>=ceil(log2(3^n))`. Conversely select one of the
`3^n` products of the three boxes by a finite binary disjunction. Therefore

```
p_conv=n,    p_bin=ceil(n log2 3),
p_bin-p_conv=ceil(n log2 3)-n.
```

These compare with arbitrary convex lifts of unrestricted continuous size
and integer range, while the general-integer upper construction is a
rational MILP. The binary upper may have exponential continuous size;
only the exact finite binary count is claimed here. All output degrees and
the box tolerance are fixed. This establishes linear additive loss in the
number of inputs for this coupled two-output-per-input class. It does not
amplify the one-input gap by varying only its output dimension.

## Alternative Bernstein transfer for reference

Let `Q_j` be the Bernstein polynomial of `F_j` of degree `n=2^18`:

```
Q_j(x)=sum_(k=0)^n F_j(k/n) binom(n,k) x^k(1-x)^(n-k).
```

All coefficients are rational. The sampled second differences are
nonnegative because `F_j` is convex, and the standard differentiated
Bernstein identity therefore gives `Q_j''>=0` on `[0,1]`. Each `F_j`
is 12-Lipschitz. If `B` is binomial with parameters `n,x`, then

```
|Q_j(x)-F_j(x)| <= 12 E|B/n-x|
                 <= 12 sqrt(x(1-x)/n)
                 <= 6/sqrt(n)=3/256 < delta=1/64.
```

Thicken `C` in the two output coordinates by the rational box
`[-delta,delta]^2`, keeping input and integer coordinates fixed. Every
point of the exact polynomial graph is now admitted. Every integer-slice
output differs from `Q(x)` by at most `3/4+2delta<1`, so the one-integer
upper bound remains valid.

At the three selected inputs, every interpolated chord error changes by
at most `2delta`. The smallest previous strict obstruction was `9/8`,
and `9/8-2delta>1`. Hence the two-bit lower bound remains valid. Two
binaries suffice by using the three individually thickened affine graph
segments; their error against `Q` is at most `2delta`. Thus the same
exact integer counts hold for two rational convex polynomial outputs.

No efficiency claim is needed for this fixed example; the Bernstein
construction is explicit and has finite dense rational encoding. Degree
`2^18` is deliberately conservative and not optimized.

## Open boundary and attribution

Difference between general integer values and binary labels is established;
so are finite polytope disjunctions, Bernstein approximation, and convexity
preservation under Bernstein approximation. The supporting observation is
their use in this restricted convex two-output box-error model. No
publication-priority claim is made.

The construction shows that zero additive overhead is impossible. It does
not disprove a universal additive constant independent of output dimension.
A direct product of copies changes the input dimension, and hence cannot
resolve the one-input question. A naive recursive three-piece construction
also does not work automatically: convex combinations across distant outer
pieces can magnify newly introduced local curvature beyond the unit budget.
