# Bounded arithmetic circuits: source check

Checked 2026-09-28. These sources establish bounded arithmetic normalizations
and exact simulations using squares. They do not supply the proposed simulation
by positive odd-root gates near 1.

1. Etessami and Yannakakis, *Recursive Markov Chains, Stochastic Grammars,
   and Monotone Systems of Nonlinear Equations*, JACM 56(1), 2009.
   [Author manuscript](https://homepages.inf.ed.ac.uk/kousha/final_rmc_jacm_version.pdf),
   proof of Theorem 5.2, printed pp. 26–27 (PDF pages 26–27).

   The proof converts PosSLP into comparison of two monotone circuits and
   places them at a common depth, with alternating addition and multiplication
   levels. The associated probabilities replace addition by the arithmetic
   mean and preserve multiplication. At level \(r\), the normalized value is
   \(g/2^{a_r}\), where

   \[
   a_0=0,\qquad
   a_r=\begin{cases}
   a_{r-1}+1&\text{at an addition level},\\
   2a_{r-1}&\text{at a multiplication level}.
   \end{cases}
   \]

   **Corollary of the construction, not its stated theorem:** PosSLP reduces
   to comparing two outputs of a polynomial-size circuit with constants 0, 1
   and gates \((x+y)/2\), \(xy\). All values lie in \([0,1]\).
   Replacing the original integer output \(N\) by \(2N-1\) first removes
   equality. The normalized output difference then has magnitude at least
   \(2^{-a_k}>2^{-2^k}\), where \(k\) is the common depth.

2. Etessami and Yannakakis, *On the Complexity of Nash Equilibria and Other
   Fixed Points*, SICOMP 39(6), 2010.
   [Author manuscript](https://homepages.inf.ed.ac.uk/kousha/nash_focs07_full_j_spec_issue_sub.pdf),
   Section 3, Step 1 and Lemma 5, printed pp. 22–23 (PDF pages 22–23).

   This separate construction gives a linear-size circuit over
   \(\{+,\times,/\}\), with input \(1/2\), every value in \((0,1)\), and
   unequal outputs preserving the PosSLP answer. It computes
   \(t=2^{-2^d}\) by repeated squaring, scales every original gate by \(t\),
   and implements multiplication as \((x'y')/t\).
   The division by a circuit-generated tiny value is essential to this
   particular normalization. Lemma 5 therefore does not directly establish
   a division-free or root-only normalization.

3. Doron-Arad and Mossel, *Why ReLU? A Bit-Model Dichotomy for Deep Network
   Training*, [arXiv:2602.19017v1](https://arxiv.org/html/2602.19017v1),
   Lemmas A.4–A.5, Lemma 3.1 and its Appendix B proof, Theorem F.1.

   Independent proof check found no substantive gap in these results.
   Lemma A.5 constructs \(m=O(n^2)\) arithmetic gates from the sole constant
   \(b_0=2^{-m}\), giving output \(2^{-m2^n}N\). The first pass counts gates
   before choosing \(b_0\), avoiding circularity. Exponent alignment skips
   zero exponents; no extra constant 1 is needed. Lemma A.4 bounds every gate
   in \([-1,1]\). The gadget-size expression should read
   \(O(1+\log t)\) at \(t=1\); this does not change the bound.

   Lemma 3.1 provides exact multiplication from shifted evaluations of a
   nonlinear rational polynomial. Its polynomial-time claim is suitable for
   fixed polynomials or dense coefficient input.

   Theorem F.1 rules out the specific finite identity

   \[
   xy=\sum_{j=0}^{m}\lambda_j
   \bigl((x+y+j)^\alpha-(x+j)^\alpha-(y+j)^\alpha\bigr)
   \]

   for \(\alpha\in\mathbb Q\setminus\mathbb Z_{\ge0}\), rational
   \(\lambda_j\), and all sufficiently large positive rational \(x,y\).
   Differentiation and the Vandermonde argument support that scope.
   It does not exclude nested root circuits, quadratic radicands, or
   controlled approximations near 1.

4. Tarasov and Vyalyi, *Semidefinite programming and arithmetic circuit
   evaluation*, [arXiv:cs/0512035v1](https://arxiv.org/pdf/cs/0512035),
   Section 1.2, Theorem 3, p. 5; Lemma 3, pp. 6–7.

   Comparing two circuit outputs over \(\{+,x\mapsto x^2/2\}\) is
   polynomially equivalent to comparison over the arithmetic, division-free,
   and monotone bases. Circuits start from constant 1. Lemma 3 gives exact
   gadgets using a difference of two positive quantities.
   This explicitly supports PosSLP hardness for addition and scaled squaring
   comparisons. The theorem imposes neither bounded values nor root gates.

The missing step remains a reduction into the actual odd-root gate language,
with polynomial encoding size, the required positive interval, and an error
bound smaller than the final sign gap. General arithmetic normalization and
algebraic degree growth do not establish that step.

Verification was limited to reading the cited primary statements and proofs
and checking their algebra and scope. The targeted command
`git diff --no-index --check /dev/null research-20260927/posslp-bounded-circuit-source-check.md`
reported no whitespace diagnostics (exit 1 for the added file). No project-wide
checks or CI inspection were performed. No
learning-theory claims outside the listed lemmas were reviewed.
