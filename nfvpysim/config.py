from multiprocessing import cpu_count
from collections import deque
import copy
from nfvpysim import Tree

############################## GENERAL SETTINGS ##############################

# Level of logging output
# Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# If True, executes simulations in parallel using multiple processes
# to take advantage of multicore CPUs
PARALLEL_EXECUTION = True

# Number of processes used to run simulations in parallel.
# This option is ignored if PARALLEL_EXECUTION = False
N_PROCESSES = cpu_count()

# Format in which results are saved.
# Result readers and writers are located in module ./icarus/results/readwrite.py
# Currently only PICKLE is supported
RESULTS_FORMAT = 'PICKLE'

# Number of times each experiment is replicated
# This is necessary for extracting confidence interval of selected metrics
N_REPLICATIONS = 3

# List of metrics to be measured in the experiments
# The implementation of data collectors are located in ./icarus/execution/collectors.py
# Remove collectors not needed
DATA_COLLECTORS = [
           'ACC_RATIO',  # Measure acceptance hit ratio
           'LATENCY',  # Measure request and response latency (based on static link delays)
           'LINK_LOAD',  # Measure link loads

                   ]



########################## EXPERIMENTS CONFIGURATION ##########################

# Default experiment values, i.e. values shared by all experiments

# Number of vnfs available in the environment
N_VNFS = 8


# Length of sfc
SFC_LENGTH = [2, 3, 4, 5, 6, 7, 8]

# Number of content requests that are measured after warmup
N_REQ = 10 ** 3

# Number of requests per second (over the whole network)
REQ_RATE = 1.0

# vnf allocation policy
VNF_ALLOCATION_POLICY = 'STATIC'

CACHE_POLICY = ''


# Total size for nfv nodes to store vnfs to be used in the sfcs
NFV_NODE_CACHE = 8


# List of topologies tested
# Topology implementations are located in ./icarus/scenarios/topology.py
# Remove topologies not needed
TOPOLOGIES = ['GEANT']

# List of caching and routing strategies
# The code is located in ./icarus/models/strategy/*.py
# Remove strategies not needed
POLICIES = ['GREEDY_WITHOUT_PLACEMENT']

# Instantiate experiment queue
EXPERIMENT_QUEUE = deque()

# Build a default experiment configuration which is going to be used by all
# experiments of the campaign
default = Tree()
default['workload'] = {'name':       'STATIONARY_RANDOM_SFC',
                       'n_vnfs': N_VNFS,
                       'n_measured': N_REQ,
                       'rate':       REQ_RATE}
default['vnf_placement']['name'] = 'RANDOM'
default['vnf_allocation']['name'] = 'STATIC'

# Create experiments multiplexing all desired parameters
for n_req in N_REQ:
    for policy in POLICIES:
        for topology in TOPOLOGIES:
            for nfv_node_cache in NFV_NODE_CACHE:
                experiment = copy.deepcopy(default)
                experiment['workload']['n_req'] = N_REQ
                experiment['policy']['name'] = policy
                experiment['topology']['name'] = topology
                experiment['vnf_policy_allocation']['nfv_node_cache'] = nfv_node_cache
                experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, network cache: %s" \
                                     % (str(n_req), policy, topology, str(nfv_node_cache))
                EXPERIMENT_QUEUE.append(experiment)