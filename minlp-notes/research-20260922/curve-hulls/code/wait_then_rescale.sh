#!/bin/sh
# wait for the SOC batch and the lnts seed runs, keep the old-scaling results, run the rescaled jobs
cd "$(dirname "$0")"
while kill -0 3103173 2>/dev/null || pgrep -f 'run[.]py lnts' >/dev/null; do sleep 20; done
mkdir -p results_oldscale
for f in gams02_cuts_pb gams02_sub_pb gams02_soc_pb chp_partload_cuts chp_partload_sub chp_partload_soc super3t_cuts super3t_sub super3t_soc ghg_2veh_cuts ghg_2veh_sub ghg_2veh_soc ghg_3veh_cuts ghg_3veh_sub ghg_3veh_soc ex8_4_2_cuts ex8_4_2_sub ex8_4_2_soc ex8_4_7_cuts ex8_4_7_sub ex7_3_5_cuts ex7_3_5_sub; do
  mv results/${f}_1800.out results_oldscale/ 2>/dev/null
done
sh run_batch.sh jobs_rescale.txt 1800 17
