Stream scripts re-run by the reviewer (round 1) from a copy of ../../code in
/tmp/r1run/code, with outputs written to /tmp/r1run/logs (the stream's logs/
directory was not touched). Solver warnings removed from the captured stdout.
sanity.out   python sanity.py
fn.out       python family_neighborhood.py 7 20 2 1
fn2.out      python family_neighborhood.py 8 60 5 2
sc_sub.out   python signclass.py 5 300 sub
sc_sup.out   python signclass.py 6 300 sup
crh.out      python check_rounding_hull.py 9 60
se.out       python stratum_enum.py 0 30 20 20 101 _r1
se_b.out     python stratum_enum.py 0 1 30 60 202 _r1b   (summary: summarize_r1b.txt)
