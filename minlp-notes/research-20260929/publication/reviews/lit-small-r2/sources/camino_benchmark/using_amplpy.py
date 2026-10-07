# This file is part of minlp-toolbox/misc
# Copyright (C) 2026  Andrea Ghezzi
# SPDX-License-Identifier: GPL-3.0-or-later

from amplpy import AMPL
from sys import argv
import os
import json
from time import time
from camino.utils.data import write_json, read_json


def do_write(overview_target, start, i, algorithm, total_stats):
    time_now = time() - start
    total_time = time_now / (i + 1) * total_to_compute
    write_json(
        {
            "time": time_now,
            "total": total_to_compute,
            "done": (i + 1),
            "progress": (i + 1) / total_to_compute,
            "time_remaining_est": total_time - time_now,
            "time_total_est": total_time,
            "algorithm": algorithm,
            "data": total_stats,
        },
        overview_target,
    )


# Convex problems
cvx_problems = ['batch', 'batch0812', 'batchdes', 'batchs101006m', 'batchs121208m', 'batchs151208m', 'batchs201210m', 'clay0203hfsg', 'clay0204hfsg', 'clay0205hfsg', 'clay0303hfsg', 'clay0304hfsg', 'clay0305hfsg', 'cvxnonsep_normcon20', 'cvxnonsep_normcon30', 'cvxnonsep_normcon40', 'cvxnonsep_nsig20', 'cvxnonsep_nsig20r', 'cvxnonsep_nsig30', 'cvxnonsep_nsig30r', 'cvxnonsep_nsig40', 'cvxnonsep_nsig40r', 'cvxnonsep_pcon20', 'cvxnonsep_pcon20r', 'cvxnonsep_pcon30', 'cvxnonsep_pcon30r', 'cvxnonsep_pcon40', 'cvxnonsep_pcon40r', 'cvxnonsep_psig20', 'cvxnonsep_psig20r', 'cvxnonsep_psig30', 'cvxnonsep_psig30r', 'cvxnonsep_psig40', 'cvxnonsep_psig40r', 'enpro48pb', 'enpro56pb', 'ex1223', 'ex1223b', 'fac1', 'fac2', 'flay02h', 'flay02m', 'flay03h', 'flay03m', 'flay04h', 'flay04m', 'flay05h', 'flay05m', 'flay06h', 'flay06m', 'fo7', 'fo7_2', 'fo7_ar25_1', 'fo7_ar2_1', 'fo7_ar3_1', 'fo7_ar4_1', 'fo7_ar5_1', 'fo8', 'fo8_ar25_1', 'fo8_ar2_1', 'fo8_ar3_1', 'fo8_ar4_1', 'fo8_ar5_1', 'fo9', 'fo9_ar25_1', 'fo9_ar2_1', 'fo9_ar3_1', 'fo9_ar4_1', 'fo9_ar5_1', 'gams01', 'ibs2', 'jit1', 'm3', 'm6', 'm7', 'm7_ar25_1', 'm7_ar2_1', 'm7_ar3_1', 'm7_ar4_1', 'm7_ar5_1', 'no7_ar25_1', 'no7_ar2_1', 'no7_ar3_1', 'no7_ar4_1', 'no7_ar5_1', 'o7', 'o7_2', 'o7_ar25_1', 'o7_ar2_1', 'o7_ar3_1', 'o7_ar4_1', 'o7_ar5_1', 'o8_ar4_1', 'o9_ar4_1', 'p_ball_10b_5p_2d_h', 'p_ball_10b_5p_3d_h', 'p_ball_10b_5p_4d_h', 'p_ball_10b_7p_3d_h', 'p_ball_15b_5p_2d_h', 'p_ball_20b_5p_2d_h', 'p_ball_20b_5p_3d_h', 'p_ball_30b_10p_2d_h', 'p_ball_30b_5p_2d_h', 'p_ball_30b_5p_3d_h', 'p_ball_30b_7p_2d_h', 'p_ball_40b_5p_3d_h', 'p_ball_40b_5p_4d_h', 'portfol_buyin', 'portfol_card', 'portfol_roundlot', 'procurement2mot', 'ravempb', 'risk2bpb', 'rsyn0805hfsg', 'rsyn0805m', 'rsyn0805m02hfsg', 'rsyn0805m02m', 'rsyn0805m03hfsg', 'rsyn0805m03m', 'rsyn0805m04hfsg', 'rsyn0805m04m', 'rsyn0810hfsg', 'rsyn0810m', 'rsyn0810m02hfsg', 'rsyn0810m02m', 'rsyn0810m03hfsg', 'rsyn0810m03m', 'rsyn0810m04hfsg', 'rsyn0810m04m', 'rsyn0815hfsg', 'rsyn0815m', 'rsyn0815m02hfsg', 'rsyn0815m02m', 'rsyn0815m03hfsg', 'rsyn0815m03m', 'rsyn0815m04hfsg', 'rsyn0815m04m', 'rsyn0820hfsg', 'rsyn0820m', 'rsyn0820m02hfsg', 'rsyn0820m02m', 'rsyn0820m03hfsg', 'rsyn0820m03m', 'rsyn0820m04hfsg', 'rsyn0820m04m', 'rsyn0830hfsg', 'rsyn0830m', 'rsyn0830m02hfsg', 'rsyn0830m02m', 'rsyn0830m03hfsg', 'rsyn0830m03m', 'rsyn0830m04hfsg', 'rsyn0830m04m', 'rsyn0840hfsg', 'rsyn0840m', 'rsyn0840m02hfsg', 'rsyn0840m02m', 'rsyn0840m03hfsg', 'rsyn0840m03m', 'rsyn0840m04hfsg', 'rsyn0840m04m', 'sssd08-04', 'sssd12-05', 'sssd15-04', 'sssd15-06', 'sssd15-08', 'sssd16-07', 'sssd18-06', 'sssd18-08', 'sssd20-04', 'sssd20-08', 'sssd22-08', 'sssd25-04', 'sssd25-08', 'st_e14', 'stockcycle', 'syn05hfsg', 'syn05m', 'syn05m02hfsg', 'syn05m02m', 'syn05m03hfsg', 'syn05m03m', 'syn05m04hfsg', 'syn05m04m', 'syn10hfsg', 'syn10m', 'syn10m02hfsg', 'syn10m02m', 'syn10m03hfsg', 'syn10m03m', 'syn10m04hfsg', 'syn10m04m', 'syn15hfsg', 'syn15m', 'syn15m02hfsg', 'syn15m02m', 'syn15m03hfsg', 'syn15m03m', 'syn15m04hfsg', 'syn15m04m', 'syn20hfsg', 'syn20m', 'syn20m02hfsg', 'syn20m02m', 'syn20m03hfsg', 'syn20m03m', 'syn20m04hfsg', 'syn20m04m', 'syn30hfsg', 'syn30m', 'syn30m02hfsg', 'syn30m02m', 'syn30m03hfsg', 'syn30m03m', 'syn30m04hfsg', 'syn30m04m', 'syn40hfsg', 'syn40m', 'syn40m02hfsg', 'syn40m02m', 'syn40m03hfsg', 'syn40m03m', 'syn40m04hfsg', 'syn40m04m', 'synthes1', 'synthes2', 'synthes3', 'tls12', 'tls2', 'tls4', 'tls5', 'tls6', 'tls7'] # fmt: skip

# Nonconvex problems -- removed because breaking "gastrans.mod",
noncvx_problems = ['4stufen', 'autocorr_bern20-05', 'autocorr_bern20-10', 'autocorr_bern20-15', 'autocorr_bern25-06', 'autocorr_bern25-13', 'autocorr_bern25-19', 'autocorr_bern25-25', 'autocorr_bern30-04', 'autocorr_bern30-08', 'autocorr_bern30-15', 'autocorr_bern30-23', 'autocorr_bern30-30', 'autocorr_bern35-04', 'autocorr_bern35-09', 'autocorr_bern35-18', 'autocorr_bern35-26', 'autocorr_bern35-35fix', 'autocorr_bern40-05', 'autocorr_bern40-10', 'autocorr_bern40-20', 'autocorr_bern40-30', 'autocorr_bern40-40', 'autocorr_bern45-05', 'autocorr_bern45-11', 'autocorr_bern45-23', 'autocorr_bern45-34', 'autocorr_bern45-45', 'autocorr_bern50-06', 'autocorr_bern50-13', 'autocorr_bern50-25', 'autocorr_bern50-38', 'autocorr_bern50-50', 'autocorr_bern55-06', 'autocorr_bern55-14', 'autocorr_bern55-28', 'autocorr_bern55-41', 'autocorr_bern55-55', 'autocorr_bern60-08', 'autocorr_bern60-15', 'autocorr_bern60-30', 'autocorr_bern60-45', 'autocorr_bern60-60', 'batch0812_nc', 'batch_nc', 'beuster', 'casctanks', 'case_1scv2', 'cecil_13', 'chp_partload', 'chp_shorttermplan1a', 'chp_shorttermplan1b', 'chp_shorttermplan2a', 'chp_shorttermplan2b', 'chp_shorttermplan2c', 'chp_shorttermplan2d', 'contvar', 'csched1', 'csched1a', 'csched2', 'csched2a', 'deb10', 'deb6', 'deb7', 'deb8', 'deb9', 'eg_all_s', 'eg_disc2_s', 'eg_disc_s', 'eg_int_s', 'eniplac', 'ex1221', 'ex1222', 'ex1224', 'ex1225', 'ex1226', 'ex1233', 'ex1243', 'ex1244', 'ex1252', 'ex1252a', 'ex3pb', 'feedtray', 'fin2bb', 'gams02', 'gams04', 'gasnet', 'gastrans', 'gastrans040', 'gastrans135', 'gastrans582_cold13', 'gastrans582_cold13_95', 'gastrans582_cold17', 'gastrans582_cold17_95', 'gastrans582_cool12', 'gastrans582_cool12_95', 'gastrans582_cool14', 'gastrans582_cool14_95', 'gastrans582_freezing27', 'gastrans582_freezing27_95', 'gastrans582_freezing30', 'gastrans582_freezing30_95', 'gastrans582_mild10', 'gastrans582_mild10_95', 'gastrans582_mild11', 'gastrans582_mild11_95', 'gastrans582_warm15', 'gastrans582_warm15_95', 'gastrans582_warm31', 'gastrans582_warm31_95', 'gear4', 'ghg_1veh', 'ghg_2veh', 'ghg_3veh', 'gkocis', 'hadamard_4', 'hadamard_5', 'hadamard_6', 'hadamard_7', 'hadamard_8', 'hadamard_9', 'hda', 'heatexch_gen1', 'heatexch_gen2', 'heatexch_gen3', 'heatexch_spec1', 'heatexch_spec2', 'heatexch_spec3', 'heatexch_trigen', 'hybriddynamic_var', 'johnall', 'kan_peaks_h1_n2_g24', 'kan_peaks_h1_n2_g3', 'kan_peaks_h1_n5', 'kan_r3_h1_n3', 'kan_r3_h1_n4', 'kan_r3_h1_n5', 'kan_r3_h1_n9', 'kan_r5_h1_n3', 'kan_r5_h1_n5', 'kan_r5_h1_n8', 'kport20', 'kport40', 'lip', 'mbtd', 'milinfract', 'multiplants_mtg1a', 'multiplants_mtg1b', 'multiplants_mtg1c', 'multiplants_mtg2', 'multiplants_mtg5', 'multiplants_mtg6', 'multiplants_stg1', 'multiplants_stg1a', 'multiplants_stg1b', 'multiplants_stg1c', 'multiplants_stg5', 'multiplants_stg6', 'nvs01', 'nvs05', 'nvs08', 'nvs21', 'nvs22', 'oaer', 'oil', 'oil2', 'ortez', 'parallel', 'pooling_epa1', 'pooling_epa2', 'pooling_epa3', 'primary', 'procsel', 'saa_2', 'sepasequ_complex', 'sepasequ_convent', 'sfacloc1_2_80', 'sfacloc1_2_90', 'sfacloc1_2_95', 'sfacloc1_3_80', 'sfacloc1_3_90', 'sfacloc1_3_95', 'sfacloc1_4_80', 'sfacloc1_4_90', 'sfacloc1_4_95', 'sfacloc2_2_80', 'sfacloc2_2_90', 'sfacloc2_2_95', 'sfacloc2_3_80', 'sfacloc2_3_90', 'sfacloc2_3_95', 'sfacloc2_4_80', 'sfacloc2_4_90', 'sfacloc2_4_95', 'spring', 'st_e15', 'st_e29', 'st_e32', 'st_e35', 'st_e36', 'st_e38', 'st_e40', 'super3t', 'supplychainp1_020306', 'supplychainp1_022020', 'supplychainp1_030510', 'supplychainp1_053050', 'supplychainr1_020306', 'supplychainr1_022020', 'supplychainr1_030510', 'supplychainr1_053050', 'synheat', 'tanksize', 'transswitch0009p', 'transswitch0009r', 'transswitch0014p', 'transswitch0014r', 'transswitch0030p', 'transswitch0030r', 'transswitch0039p', 'transswitch0039r', 'transswitch0057p', 'transswitch0057r', 'transswitch0118p', 'transswitch0118r', 'transswitch0300p', 'transswitch0300r', 'transswitch2383wpp', 'transswitch2383wpr', 'transswitch2736spp', 'transswitch2736spr', 'tspn05', 'tspn08', 'tspn10', 'tspn12', 'tspn15', 'unitcommit2', 'uselinear', 'var_con10', 'var_con5', 'wager', 'wastepaper3', 'wastepaper4', 'wastepaper5', 'wastepaper6', 'water4', 'waternd1', 'waternd2', 'waterno2_01', 'waterno2_02', 'waterno2_03', 'waterno2_04', 'waterno2_06', 'waterno2_09', 'waterno2_12', 'waterno2_18', 'waterno2_24', 'watertreatnd_conc', 'watertreatnd_flow', 'waterx', 'waterz', 'windfac'] # fmt: skip

with open("benchmark/wall_time_noncvx_sbmiqp.json", "r") as file:
    noncvx_problems_time_limit = json.load(file)
    noncvx_problems_time_limit = noncvx_problems_time_limit["noncvx_sbmiqp.calc_time"]

if len(argv) != 5:
    print(
        "Usage: python using_amplpy.py <problem type 'cvx', 'noncvx'> <solver 'gurobi', 'scip', 'xpress'> <root_folder_minlp> <results_folder>"
    )
    exit()

verbosity = 3
problem_type = argv[1]
solver = argv[2]
root_folder_minlp = argv[3]
results_folder = argv[4]
results_folder = os.path.join(results_folder, problem_type + "_" + solver)

if problem_type == "cvx":
    problems = cvx_problems
elif problem_type == "noncvx":
    problems = noncvx_problems
else:
    raise ValueError("problem type must be either 'cvx' or 'noncvx'!")

overview_target = os.path.join(results_folder, "overview.json")
start = time()
total_to_compute = len(problems)
if os.path.exists(overview_target):
    data = read_json(overview_target)
    total_stats = data["data"]
    algorithm = data["algorithm"]
    i_start = data["done"]
    start -= data["time"]
else:
    os.makedirs(results_folder, exist_ok=True)
    total_stats = [
        [
            "id",
            "path",
            "obj",
            "dual_obj",
            "calc_time",
        ]
    ]
    i_start = 0

idx = i_start
for problem in problems[i_start:]:
    print(f"{problem=}")
    problem_path = os.path.join(root_folder_minlp, problem + ".mod")
    ampl = AMPL()
    ampl.eval(f"model {problem_path};")

    ampl.eval(f"option solver {solver};")
    ampl.eval(f"option solver_msg {verbosity};")
    ampl.eval("option show_stats 1;")

    if problem_type == "noncvx":
        time_limit = str(noncvx_problems_time_limit[problem.split(".")[0]])
        # time_limit = str(noncvx_problems_time_limit[problem.split('.')[0]] + 8)
    else:
        time_limit = str(300)
    print(f"{time_limit=}")

    if (
        solver == "gurobi"
    ):  # TODO gurobi gets slower if setting intfeastol even if the default its 1e-5
        ampl.eval(
            f'option {solver}_options "bestbound=1" "feastol=1e-8" "mipgap=1e-2" "threads=1" "timelimit={time_limit}";'
        )  # "outlev 1"
    elif solver == "scip":
        ampl.eval(
            f'option {solver}_options "bestbound=1" "feastol=1e-8" "mipgap=1e-2" "maxnthreads=1" "timelimit={time_limit}";'
        )  # "outlev 1"
    elif solver == "xpress":
        ampl.eval(
            f'option {solver}_options "bestbound=1" "feastol=1e-8" "mipgap=1e-2" "threads=1" "timelimit={time_limit}";'
        )  # "outlev 1"

    try:

        ampl.eval("solve;")
        ampl.eval("display solve_result_num, solve_result;")

        if ampl.getValue("solve_result") not in ["solved", "limit"]:
            total_stats.append(
                [
                    idx,
                    problem_path,
                    "FAILED",
                    ampl.getValue("solve_result"),
                    ampl.getValue("_solve_elapsed_time"),
                ]
            )
        else:
            result = {}
            result["id"] = idx
            result["path"] = problem_path
            result["obj"] = ampl.getValue("obj")
            result["dual_obj"] = ampl.getValue("obj.bestbound")
            result["calc_time"] = ampl.getValue("_solve_elapsed_time")
            total_stats.append(
                [
                    idx,
                    problem_path,
                    result["obj"],
                    result["dual_obj"],
                    result["calc_time"],
                ]
            )
    except:
        total_stats.append(
            [
                idx,
                problem_path,
                "FAILED",
                ampl.getValue("solve_result"),
                ampl.getValue("_solve_elapsed_time"),
            ]
        )
    do_write(overview_target, start, idx, solver, total_stats)
    idx += 1
