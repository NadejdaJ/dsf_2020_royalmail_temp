## Sample Variables
depot_name = "EDINBURGH"
sample_name = "sample_050"

## Hard Constraints
max_vans = 5
max_duty = 240
service_time = 5
departure_time = "10:00"

## OR-tools variables
# Options available are: "GREEDY_DESCENT", "TABU_SEARCH", "GUIDED_LOCAL_SEARCH", "SIMULATED_ANNEALING"
search_ortools_options = "SIMULATED_ANNEALING"
num_ortools_iters = 100

## LNS Variable
lns_destroy_frac = 0.4
lns_stop_converge = 100

## Opex Cost Function
pounds_per_min = 0.33
pounds_per_km = 0.25
