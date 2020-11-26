import pandas as pd
import random as rnd
from math import exp, log
import params
import lns
import routes

def random_chance_of_accepting(repaired_routes, tmp_route, SA_Temp):
    prob = exp(-(repaired_routes.total_time - tmp_route.total_time) / SA_Temp)
    if rnd.uniform(0, 1) < prob:
        return True
    return False

def run_vrp_solver(puzzle, init_route):
    record_perf_df = pd.DataFrame()

    sa_iter_count = 0
    best_route = init_route
    tmp_route = init_route
    SA_Temp = (1 - params.sa_control_temp) * tmp_route.total_time / log(0.5)

    while sa_iter_count <= params.sa_max_iter:
        sa_iter_count += 1
        print("Running optimisation of route")
        ### Run lns
        repaired_routes = lns.run(tmp_route)

        ### Reject route if wrong
        if repaired_routes.num_vans != puzzle.max_vans:
            pass
        if repaired_routes.total_time > puzzle.max_duty:
            pass

        ### Simulated Annealing
        if repaired_routes.total_time < best_route.total_time:
            best_route = repaired_routes
            tmp_route = repaired_routes
        elif random_chance_of_accepting(repaired_routes, tmp_route, SA_Temp):
            tmp_route = repaired_routes

        ### Keep track for graphs
        perf_dict = {"iter": sa_iter_count,
                     "SA_temp": SA_Temp,
                     "route_cost": tmp_route.total_time,
                     "best_cost": best_route.total_time}
        record_perf_df = record_perf_df.append(pd.DataFrame(perf_dict, index=[0]))

        ### Updating Simulated Annealing Temperature for next iteration
        SA_Temp = params.sa_cooling_rate * SA_Temp

    record_perf_df = record_perf_df.reset_index(drop=True)

    return best_route, record_perf_df
