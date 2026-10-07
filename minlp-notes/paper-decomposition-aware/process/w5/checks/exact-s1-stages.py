"""W5 exact: check the S1 numbers quoted in sections/exact-localized.tex.

Claims: the face candidate is accepted within nine stages (stage index <= 8)
on 29 of 30 instances; a single CT run reaches the threshold of
Proposition prop:accept (constants of eq:exact-constants) after at most 72
stages; and this is not "long after" acceptance on every instance.
"""
import csv, os
path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'experiments', 'results', 'S1_localized.csv')
rows = list(csv.DictReader(open(path)))
acc = [r for r in rows if r['status'] == 'accepted']
face = [int(r['face_first_stage']) for r in acc]
single = [int(r['single_run_stages_lemma']) for r in rows]
print('instances', len(rows), 'accepted', len(acc))
print('max face-candidate stage index', max(face))
print('max single-run stages (lemma constant)', max(single))
close = [(r['name'], r['face_first_stage'], r['single_run_stages_lemma'])
         for r in acc if int(r['single_run_stages_lemma']) <= int(r['face_first_stage']) + 3]
print('instances where the threshold is reached within 3 stages of acceptance:', close)
assert len(rows) == 30 and len(acc) == 29 and max(face) <= 8 and max(single) == 72
print('PASS')
