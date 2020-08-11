from multiprocessing import cpu_count
from collections import deque
import copy
from tools.util import Tree

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
           'CACHE_HIT_RATIO',  # Measure cache hit ratio
           'LATENCY',  # Measure request and response latency (based on static link delays)
           'LINK_LOAD',  # Measure link loads
           'PATH_STRETCH',  # Measure path stretch
                   ]



########################## EXPERIMENTS CONFIGURATION ##########################

# Default experiment values, i.e. values shared by all experiments

# Number of content objects
N_CONTENTS = 7

# Number of content requests generated to pre-populate the caches
# These requests are not logged
N_WARMUP_REQUESTS = 0

# Number of content requests that are measured after warmup
N_MEASURED_REQUESTS = 10 ** 3

# Number of requests per second (over the whole network)
REQ_RATE = 1.0

# Cache eviction policy
CACHE_POLICY = 'LRU'

# Zipf alpha parameter, remove parameters not needed
ALPHA = []

# Total size of network cache as a fraction of content population
# Remove sizes not needed
NETWORK_CACHE = []


# List of topologies tested
# Topology implementations are located in ./icarus/scenarios/topology.py
# Remove topologies not needed
TOPOLOGIES = ['GEANT']

# List of caching and routing strategies
# The code is located in ./icarus/models/strategy/*.py
# Remove strategies not needed
POLICIES = ['FIRST_FIT']

# Instantiate experiment queue
EXPERIMENT_QUEUE = deque()

# Build a default experiment configuration which is going to be used by all
# experiments of the campaign
default = Tree()
default['workload'] = {'name':       'STATIONARY_RANDOM_SFC',
                       'n_contents': N_CONTENTS,
                       'n_warmup':   N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS,
                       'rate':       REQ_RATE}
default['cache_placement']['name'] = 'UNIFORM'
default['content_placement']['name'] = 'UNIFORM'
default['cache_policy']['name'] = CACHE_POLICY

# Create experiments multiplexing all desired parameters
for alpha in ALPHA:
    for strategy in POLICIES:
        for topology in TOPOLOGIES:
            for network_cache in NETWORK_CACHE:
                experiment = copy.deepcopy(default)
                experiment['workload']['alpha'] = alpha
                experiment['strategy']['name'] = strategy
                experiment['topology']['name'] = topology
                experiment['cache_placement']['network_cache'] = network_cache
                experiment['desc'] = "Alpha: %s, strategy: %s, topology: %s, network cache: %s" \
                                     % (str(alpha), strategy, topology, str(network_cache))
                EXPERIMENT_QUEUE.append(experiment)