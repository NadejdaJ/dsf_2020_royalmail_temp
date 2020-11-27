# import pandas as pd
# import random as rnd
# from math import exp, log
# import params
# from lns import lns_class
# import viz
#
# def random_chance_of_accepting(repaired_routes, current_route, SA_Temp):
#     prob = exp(-(repaired_routes.total_time - current_route.total_time) / SA_Temp)
#     if rnd.uniform(0, 1) < prob:
#         return True
#     return False
#
# def simulated_annealing_init_temp(cost):
#     return (1 - params.sa_control_temp) * cost / log(0.5)
#
# def run_vrp_solver(puzzle, init_route):
#
#     rnd.seed(12345)
#
#     record_perf_df = pd.DataFrame()
#
#     best_route = init_route
#     current_route = init_route
#
#     SA_Temp = simulated_annealing_init_temp(current_route.total_time)
#
#     lns_iter_count = 0
#     while lns_iter_count < params.lns_max_iter:
#
#         lns_iter_count += 1
#
#         ### Run lns
#         search = lns_class(puzzle, current_route, params.lns_destroy_frac, lns_iter_count)
#         repaired_routes = search.run()
#
#         # ### Reject route if wrong
#         # if repaired_routes.invalid_routes_max_time() or repaired_routes.invalid_routes_min_time():
#         # 	print('\t ... breaking time constraints ... continue')
#         # 	continue
#         # if repaired_routes.num_vans != puzzle.max_vans:
#         # 	print('\t ... wrong van number ... continue')
#         # 	continue
#
#         ### Simulated Annealing
#         if repaired_routes.total_time < best_route.total_time:
#             best_route = repaired_routes
#             current_route = repaired_routes
#             SA_Temp = simulated_annealing_init_temp(current_route.total_time)
#         elif random_chance_of_accepting(repaired_routes, current_route, SA_Temp):
#             current_route = repaired_routes
#
#         print(" Iter - %d \t\t Driving Time: \t\t Current = %.f \t\t Repaired = %.f \t\t Best = %.f  [min]" %
#               (lns_iter_count, current_route.total_time, repaired_routes.total_time, best_route.total_time))
#
#         ### Keep track for plots
#         perf_dict = {"iter": lns_iter_count,
#                      "SA_temp": SA_Temp,
#                      "route_cost": repaired_routes.total_time,
#                      "best_cost": best_route.total_time,
#                      "route_drive_time": str([round(t[-1], 3) for t in repaired_routes.van_times]),
#                      "best_drive_time": str([round(t[-1], 3) for t in best_route.van_times])
#                      }
#         record_perf_df = record_perf_df.append(pd.DataFrame(perf_dict, index=[0]))
#
#         ### Updating Simulated Annealing Temperature for next iteration
#         SA_Temp = params.sa_cooling_rate * SA_Temp
#
#
#     ### Analysis and Plots
#     record_perf_df = record_perf_df.reset_index(drop=True)
#     record_perf_df.to_csv(puzzle.output_path +"/solutions/vrp_performance.csv")
#
#     # _ = viz.plot_cost_per_van(puzzle, record_perf_df, "cost_per_van.png")
#
#     _ = viz.plot_convergence_cost(puzzle, record_perf_df, "convergence_costs.png")
#
#     return best_route, record_perf_df
