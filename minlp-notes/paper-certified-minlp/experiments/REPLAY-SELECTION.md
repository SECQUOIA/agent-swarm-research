# Candidate selection for independent uniform-campaign replay

Recorded while generation is in progress, before independent replay or analysis
of comparative bound quality. This clarifies path handling for the unchanged
producer, which renames failed completed proofs. It changes no search settings.

For each of all 289 attempted models, select `master_complete.vipr` if present;
otherwise select `master_complete_safe_failed.vipr` if present; otherwise select
`master_complete_default_failed.vipr` if present; otherwise report missing proof.
This is fixed attempt order, not bound quality or a separate acceptance screen.
Create a read-only replay view with the selected proof mapped to the conventional
filename, alongside that attempt's common lemma/master. Record the actual source
filename and hash. Keep all other completed failed proof files as attempt evidence;
they do not add instances to the primary replay denominator or count as replayed.

A selected complete proof that survived a generation hard timeout can still pass
independent replay. Such results are reported separately from generation success.
The replay checks nonlinear lemmas and master identity as well as the full proof.
Its optional external corroboration is omitted: the internal exact kernel is
the acceptance boundary. This is a separate execution of the same checker,
implemented separately from the solver and external VIPR checker. This lets replay assess a
candidate even if the legacy external checker refused it. Historical replay used
both checks and remains a separately characterized campaign. External failure
is never silently treated as success during generation.
