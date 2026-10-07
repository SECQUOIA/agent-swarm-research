"""Write the list of MINLPLib candidate instances for the screening (nonconvex, quadratic problem type,
not a pure binary QP, at most 2000 variables and 4000 constraints) to stdout, one name per line."""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'sources', 'instancedata.csv')), delimiter=';'))
osil = os.path.expanduser('~/.cache/minlplib/minlplib/osil')
for x in rows:
    if 'Q' in x['probtype'] and x['convex'] != 'True' and x['probtype'] != 'BQP' \
            and int(x['nvars']) <= 2000 and int(x['ncons']) <= 4000 \
            and os.path.exists(os.path.join(osil, x['name'] + '.osil')):
        print(x['name'])
