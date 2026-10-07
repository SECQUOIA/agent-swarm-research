Data-semantics audit checks (paper-open-minlplib/development/data-semantics.md).
All scripts are read-only with respect to the repository. The two shell drivers copy the
needed research scripts into a scratch directory and run them there. At most one core is used.

osilx_ro.py          unchanged copy of research-20260929/reviews/open-instances-verification/osilx.py
osilx_b64_wrapper.py replaces osilx.read in a scratch copy: every non-binary64-exact numeric
                     string becomes the exact decimal of its binary64 rounding (reading (c))
rocket_b64.patch.py  same for the first bound-audit verifier's osil.py and rocket_kraw.py

Commands (from this directory; REPO = repository root):
  python3 data_survey.py <instances>        > logs/data_survey.log
  python3 power_survey.py <instances>       > logs/power_survey.log
  python3 enclosure_check.py <instances>    > logs/enclosure_check.log    (10 s)
  python3 misc_checks.py                    > logs/misc_checks.log
  bash pricing050_rerun.sh $REPO /tmp/ds_w2s $PWD/logs                   (20 s)
  python3 zero_bases.py                     > logs/zero_bases.log
  bash run_audit_b64.sh $REPO /tmp/ds_a64 $PWD/logs                      (4.3 min)
  python3 summarize_b64.py $REPO $PWD/logs  > logs/summarize_b64.log
Instances used: ann_cumene_tanh camshape100-800 catmix100-800 chain50-400 dtoc5 eg_int_s
eg_disc_s eg_disc2_s etamac ex6_2_5 ex6_2_7 hvycrash kan_r3_h1_n4/n5/n9 kan_r5_h1_n3/n5/n8
lnts50-400 lukvle10 optcdeg2 pindyck powerflow0030p powerflow0039p powerflow0039r pricing050
waterno2_06/09/12/18/24 rocket100/200/400 (46 cached OSIL files).
