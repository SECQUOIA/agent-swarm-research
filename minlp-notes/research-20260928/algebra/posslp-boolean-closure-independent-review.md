# Independent adversarial review of the PosSLP Boolean compiler

Date: 2026-09-28. Reviewed claim: the compiler in
[posslp-boolean-closure-audit.md](posslp-boolean-closure-audit.md).

## Verdict

The stated compiler is correct under its explicit integer-circuit and
polynomial-size Boolean-circuit assumptions. I found no counterexample or
gap in the magnitude compression, Boolean gate margins, positive-denominator
encoding, or polynomial DAG-size accounting. This is an independent proof
audit and finite computational check, not a novelty certification.

## Proof checks

1. **Initial gap and size bound.** The shift \(x=2a-1\) is nonzero for every
   integer \(a\), and its sign represents \(a>0\), including the important
   case \(a=0\). The bound \(M_{n+2}\) is more than sufficient for circuits
   over constants \(0,1\) with at most \(n\) arithmetic gates. If the result
   is later stated for arbitrary integer literals, their bit lengths must
   enter the input-size parameter. Counting arithmetic gates alone would
   not bound such literals. The shift cannot be applied unchanged to
   arbitrary positive rational inputs: \(a=1/4\) is a counterexample.

2. **Compression.** For \(1\le t\le M\),
   \[
   2Mt-M-t^2=(t-1)(M-t)+t(M-1)\ge0.
   \]
   This proves the lower bound. The upper bound can be checked without
   introducing square roots into the algebra:
   \[
   M(M+t^2)^2-(2Mt)^2=M(t^2-M)^2\ge0.
   \]
   The denominator is positive and the map is odd. Composing the maps in
   descending order of \(M_j\) therefore gives the claimed invariant.
   No approximation or convergence argument is needed.

3. **Boolean gate margins.** For AND, the three intervals are exactly
   \([1,5]\), \([-5,-1]\), and \([-11,-7]\), according to whether
   two, one, or zero inputs are positive. For OR they are exactly
   \([7,11]\), \([1,5]\), and \([-5,-1]\). Consequently neither gate
   can produce zero. Applying \(F_{16}\) and then \(F_4\) restores the
   invariant even at all boundary cases. Negation and Boolean constants
   also preserve it.

4. **Division elimination.** Substitution of \(P/Q\) into the compression
   map gives exactly \((2MPQ,MQ^2+P^2)\). Since \(M>0\) and \(Q>0\),
   the new denominator is strictly positive. The cross-multiplied AND/OR
   numerators and the denominator \(QS\) are correct. No gcd computation
   or fraction reduction is required. Induction gives a final integer
   numerator with the desired strict sign.

5. **Representation size.** Each pair operation uses a constant number of
   new arithmetic gates referencing existing outputs. The constants
   \(M_j\) share one squaring chain. The resulting size is
   \(O(n+kN+s)\). Fanout and shared Boolean subcircuits do not invalidate
   this accounting. Expanding to an arithmetic formula can destroy the
   bound; explicitly evaluating the integers can also require enormous
   bit lengths. Neither operation is needed by the reduction.

For complete precision, Boolean size should mean the encoding size of a
standard Boolean circuit, for example over the binary AND/OR and unary NOT
basis. Arbitrary gates carrying succinct descriptions of much larger truth
tables are outside this statement. Ordinary polynomial-time Boolean
postprocessing can be compiled uniformly to such a circuit.

## Exact finite check

The following targeted command was actually run from the repository root:

```bash
python - <<'PY'
from fractions import Fraction
from itertools import product

def f(x,M):
    return 2*M*x/(M+x*x)
def pair_f(P,Q,M):
    return 2*M*P*Q, M*Q*Q+P*P

def norm(x):
    for M in [256,16,4]:
        x=f(x,M)
    return x

checks=0
for M in [1,2,4,16,256]:
    for numerator in range(1,1001):
        x=1+Fraction(numerator-1,999)*(M-1)
        y=f(x,M)
        assert y>=1 and y*y<=M
        P,Q=pair_f(x.numerator,x.denominator,M)
        assert Q>0 and Fraction(P,Q)==y
        checks+=1
vals=[norm(Fraction(2*a-1)) for a in range(-100,101)]
assert all(1<=abs(v)<=2 for v in vals)
for u,v in product(vals[::10],repeat=2):
    for op,bias in [('and',-3),('or',3)]:
        w=2*(u+v)+bias
        expect=(u>0 and v>0) if op=='and' else (u>0 or v>0)
        assert (w>0)==expect and 1<=abs(w)<=11
        P,Q=u.numerator,u.denominator
        R,S=v.numerator,v.denominator
        A,B=2*P*S+2*R*Q+bias*Q*S,Q*S
        assert Fraction(A,B)==w
        A,B=pair_f(A,B,16)
        A,B=pair_f(A,B,4)
        assert B>0 and 1<=abs(Fraction(A,B))<=2 and (A>0)==expect
        checks+=1
print(f'{checks} exact rational checks passed; 201 shifted integer inputs normalized correctly.')
PY
```

Result: exit code 0, with output:

```text
5882 exact rational checks passed; 201 shifted integer inputs normalized correctly.
```

The checks cover 5,000 rational compression inputs, all 201 integer inputs
from \(-100\) through \(100\), and both gate implementations on 441
normalized input pairs. They check exact fraction identities, denominator
positivity, signs, and output bounds. They do not exhaust arbitrary circuit
depth or input magnitude, verify the implementation of a complete compiler,
or prove the size bound. The analytic induction above supplies the general
argument. No Lean verification, project-wide checks, or CI inspection was
performed.

## Significance and novelty limits

The lemma justifies replacing polynomially many nonadaptive comparisons
and Boolean postprocessing by one PosSLP instance. It does not by itself
give a polynomial-time bit algorithm for evaluating that instance, small
expanded integer witnesses, or a numerical optimization speedup. Adaptive
oracle computations require an additional argument and are not established
by this review.

Focused searches for PosSLP with “truth-table,” “Boolean combination,”
“Boolean operations,” “conjunction,” “intersection,” and reduction closure
did not locate a directly matching primary theorem. That search outcome
does not establish originality. The manuscript's qualification that this
is a self-contained compiler lemma with novelty unresolved is appropriate.
The full literature comparison and any stronger consequences require their
own audits.
