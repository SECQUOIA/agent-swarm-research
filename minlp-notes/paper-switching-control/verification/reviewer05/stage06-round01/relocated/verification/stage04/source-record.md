# Primary-source verification for stage 4

The final published Sager–Zeile article was downloaded on 2026-09-07 from
https://link.springer.com/content/pdf/10.1007/s10589-020-00244-5.pdf.
SHA-256 of the 6,214,094-byte PDF: `f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`.
An openly indexed institutional copy is available at
https://opendata.uni-halle.de/bitstream/1981185920/64565/1/Sager%20et%20al._On%20mixed-integer_2021.pdf.
The source PDF is not redistributed with this paper.

The author inspected the final published pages 610–612 using `pdftotext -layout`:

- Corollary 4, p.610, equation (6.18), gives the two-mode upper bound and its
  attainment argument restricts N to j(3+2s)+s+2, j a nonnegative integer.
- Corollary 5, p.611, states the many-mode lower bound (N+s+1)/(3+2s) times
  maximum width for n>2 and 1<=s<=N-2, without that congruence restriction.
  Its proof embeds the two-mode example by assigning other modes zero rates.
- Proposition 4, p.612, equation (7.4), gives the continuous lower bound
  T/(s+2) for s<=n-2 and T/(2s+4-n) otherwise. Its construction and the
  displayed hypotheses are distinct from Corollary 5. In particular it supplies
  the already published lower bounds T/5 at n=3,s=2 and T/7 at n=3,s=3.

The manuscript uses these precise locators and qualifies the correction as a
failure of Corollary 5 as written. It does not infer a corrected general
finite-grid lower formula or claim priority for the continuous lower witnesses.

The correction agent independently checked the publisher HTML's Conjecture 1,
equation (7.6), and the corresponding final PDF statement on p.615. It asserts
an equality, subject to n>2 and 1<=s<=N-2. At n=3, N=7, s=3 on unit cells,
its second branch gives 7/(2*3+4-3)+1/2=3/2. The exact seven-cell value 4/3
therefore satisfies that upper-bound inequality but contradicts the stated
equality. This source interpretation is distinct from the Corollary 5
lower-bound correction above. The earlier many-mode examples refute the
conjecture even when weakened to an upper bound.
