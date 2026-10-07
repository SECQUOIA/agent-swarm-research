# Verifier verdict on F-referee-1 (W6)

refuted: False; severity: minor

## Reasoning

The finding's facts are correct, and the paper does not handle the issue anywhere else.

Facts checked:
- /tmp/dpaper/out/main.aux gives §7 at p. 30, §8 at p. 43, §9 at p. 51, §11 at p. 64 and §12 at p. 69. pdftotext shows "References" at the top of p. 71, so the main text is pp. 1-70 of 127 pages.
- §§7-9 take 27 pp. and §§3-6 take 21 pp.
- process/w5/CUTPLAN.md sets "Target after W5: main text about 62-65 pages", and R-referee-1 (process/w4/R-referee.md) asked for 50-55 pp.
- The cited proof ranges are exact: recourse-convex.tex:219-261; recourse-cuts.tex:116-133, 203-222, 240-252; constraints.tex:255-296, 328-350, 392-406; optsets.tex:148-186. Together they are 213 lines.
- No moved proof contains a \label, and no text cites the proof of any of these results. The only nearby phrase, "the argument of (a)" at constraints.tex:346, lies inside the moved proof of thm:tu-states.

Measured effect: I applied the moves to private copies (/tmp/f1v-{base,a,ab,abc}; sources untouched) and built each with latexmk. All builds had 0 undefined or multiply defined references.
- base: references start at p. 71.
- (a): references start at p. 68.
- (a)+(b): references start in the middle of p. 67.
- (a)+(b)+(c): §12 starts at p. 65 and references start near the top of p. 66, so the main text is about 65 pp.

So the claim of "about 65-66 pages" holds. Item (c) is needed to reach the 62-65 target, because (a)+(b) alone give about 66.5 pp.

Severity: minor, not major. Nothing here is a correctness or clarity defect. The claimed consequence ("a 127-page manuscript will draw editorial objections") is not cured by the fix, because the PDF stays at 127 pages in every variant. The fix only moves the main/appendix boundary by about 5 pp. MP has no hard page limit, and the same referee report calls the paper "ready for submission after small changes". The fix should still be applied, because it is cheap and meets the binding W5 target.

Defects in the proposed fix:
1. Moving exact-localized.tex:2-135 "unchanged" leaves two problems that I confirmed in the build:
   - Line 122, "The proof is in Appendix~\ref{app:localized}.", now sits inside Appendix B.1 and renders as "The proof is in Appendix B.1" there.
   - appendix-localized.tex:4 still says "We use the notation of Section~\ref{sec:localized}", but that section is now a stub.
2. The summary paragraph is slightly loose in two places:
   - Proposition prop:local imposes sign conditions only on coordinates where the narrowed box has positive length, and none in case (iv).
   - The strict complementarity of cor:local is only needed at A, the continuous coordinates with L_i>0 that are at a bound.
3. The fix does not say where in Appendix D the cut-recourse proofs go, and the appendix intros (appendix-tu.tex:3-6) do not mention the new proofs.
4. Placing tab:chain after the "Exact output" paragraph breaks section order in Appendix H. Section 11.3 comes before 11.4, so the table belongs before that paragraph.

## Corrected fix

Keep every statement and label. Replace each main-text proof block by the sentence given below. Insert the unchanged block in the named appendix as \begin{proof}[Proof of <Theorem|Proposition>~\ref{...}] ... \end{proof}.

(a) Proofs (213 source lines, about 3 pp. measured):
- thm:cv (recourse-convex.tex:219-261)
  - Replace by "The proof is in Appendix~\ref{app:recourse-convex}."
  - Insert the block directly before appendix-recourse-convex.tex:424 ("Proof of the exact-output part of Theorem~\ref{thm:cv}(iii)").
  - In the moved (iii) paragraph, replace "Appendix~\ref{app:recourse-convex} gives the procedure and its analysis." by "The proof below gives the procedure and its analysis."
- thm:cr-oracle, thm:cr-search, prop:cr-growth (recourse-cuts.tex:116-133, 203-222, 240-252)
  - Replace each by "The proof is in Appendix~\ref{app:cr-proofs}."
  - Insert the three blocks, in this order, in a new first subsection of Appendix D, before "Exact output with a cut residual": \subsection{Proofs for Section~\ref{sec:cuts}}\label{app:cr-proofs}.
- prop:tu-sound, thm:tu-states, thm:tu-approx (constraints.tex:255-296, 328-350, 392-406)
  - Replace each by "The proof is in Appendix~\ref{app:tu-proofs}."
  - Insert them in a new subsection after E.1, before \subsection{Union versus hull filtering}: \subsection{Proofs for Sections~\ref{sec:tu-filter}--\ref{sec:tu-complexity}}\label{app:tu-proofs}.
  - In appendix-tu.tex:3, change "gives the checks of the model of Section~\ref{sec:tu-model}," to "gives the checks of the model of Section~\ref{sec:tu-model}, the proofs of Proposition~\ref{prop:tu-sound} and Theorems~\ref{thm:tu-states} and~\ref{thm:tu-approx},".
  - Keep the proofs of lem:tu-round and lem:tu-allow in the main text.
- thm:cells (optsets.tex:148-186)
  - Replace by "The proof is in Appendix~\ref{app:cells}."
  - Insert it as the first subsection of Appendix F: \subsection{Uniform cells}\label{app:cells}.

(b) Move the table environment tab:chain (computation.tex:169-187) to appendix-computation.tex, directly before \paragraph{Exact output (Section~\ref{sec:comp-exact}).} so that the appendix follows section order. In computation.tex:155, write "Table~\ref{tab:chain} in Appendix~\ref{app:computation} reports CT on the family".

(c) Move exact-localized.tex:2-135 into appendix-localized.tex.
- Insert it after the subsection heading and before line 4.
- Retitle that subsection \subsection{Localized acceptance}\label{app:localized}.
- In the moved text, replace "The proof is in Appendix~\ref{app:localized}. It also shows" by "The proof below also shows".
- Apply the F-referee-5 wording fix to the moved S1 sentence.
- In appendix-localized.tex:4, replace "We use the notation of Section~\ref{sec:localized} and" by "We use the notation above and of".
- Leave this paragraph under \subsection{Localized acceptance}\label{sec:localized}:

'The acceptance rule of Proposition~\ref{prop:accept} needs a certified gap below $1/(\Omega W)$, as small as about $2^{-315}$ on the instances of Section~\ref{sec:comp-exact}. Appendix~\ref{app:localized} gives a second test that uses the filtering history. On the box retained by a stage of a filtering run, it checks a candidate by sign conditions on the gradient at the coordinates where the narrowed box is not a point, and one exact positive-semidefiniteness test (Proposition~\ref{prop:local}). Its validity needs neither uniqueness nor growth. Assume point growth, and strict complementarity at the continuous coordinates with $L_i>0$ at which $x^*$ is at a bound. Then the face candidate of Definition~\ref{def:facecand} equals $x^*$ and passes this test at every stage that ends by filtering, in a trial of CT with a common mesh and $8\kappa\theta^2\le1$, once the mesh $h_j$ is at most a threshold $h^*$. The least such $j$ is at most $\poly(I)+O(\log\kappa)$ (Corollary~\ref{cor:local}). In experiment S1 (Section~\ref{sec:comp-localized}) the test accepted the face candidate within nine stages on 29 of 30 random mixed-integer instances.'

Measured result (private builds):
- (a)+(b)+(c): references start near the top of p. 66, so the main text is about 65 pp. The total stays 127 pp. There are no undefined references.
- Without (c): about 66.5 pp, which is above the W5 target. Item (c) is therefore needed to meet the target.
