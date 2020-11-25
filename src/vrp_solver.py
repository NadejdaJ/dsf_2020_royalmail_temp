import params
import lns
import routes
import random as rnd
from math import exp, log


def run_vrp_solver(init_route):
    sa_iter_count = 0
    best_route = init_route.deepcopy()
    tmp_route = init_route.deepcopy()
    SA_Temp = (1 - params.sa_control_temp) * tmp_route.cost / log(0.5)

    while sa_iter_count <= params.sa_max_iter:
        sa_iter_count += 1
        print("Running optimisation of route")
        ### Run lns
        #ToDo: Insert Hugos lns
        repaired_routes = lns.run(tmp_route)
        repaired_route_cost = repaired_routes.cost

        ### Reject route if wrong
        #ToDo: reject route if wrong based on to few vans & above 240min

        ### Simulated Annealing
        #Todo: Correct pseudocode below
        flag_accept = False

        prob = exp(-(repaired_routes.opexcost - repaired_routes.opexcost) / SA_Temp)
        if rnd.uniform(0, 1) < prob:
            random_chance_of_accepting = True
        else:
            random_chance_of_accepting = False
            tmp_route = repaired_routes
        if repaired_routes < best_route.cost:
            flag_accept = True
            #ToDo: set best route to temp route

        elif random_chance_of_accepting:
            flag_accept = True
        ### Updating Simulated Annealing Temperature for next iteration
        SA_Temp = params.sa_cooling_rate * SA_Temp

        ### Keep track for graphs

    return best_route