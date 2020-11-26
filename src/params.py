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
spancost_coeff = 10

## LNS Variable
lns_destroy_frac = 0.4
lns_stop_converge = 100

## Simulated Annealing Parameters
sa_max_iter = 10
sa_control_temp = 1.33 # Needs to be greater than 1
sa_cooling_rate = 0.81 # Needs to be smaller than 1

## Map Zoom Option
zoom_level = 10