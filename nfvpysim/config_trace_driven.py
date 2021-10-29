from multiprocessing import cpu_count
from collections import deque
import copy
from nfvpysim.util import Tree

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
    'ACCEPTANCE_RATIO',  # Measure acceptance hit ratio
    'LATENCY',  # Measure request and response latency (based on static link delays)


]



########################## EXPERIMENTS CONFIGURATION ##########################

# Default experiment values, i.e. values shared by all experiments


# Number of content requests that are measured after warmup
VNF_ALLOCATION_SPACE = [8]


# Number of warmup requests
N_WARMUP_REQUESTS = 0

# Number of measured requests

N_MEASURED_REQUESTS = 1 * 10 ** 4




# Number of requests per second (over the whole network)
SFC_REQ_RATE = 10.0
#SFC_REQ_RATES = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

# vnf allocation policy
VNF_ALLOCATION_POLICY = 'STATIC'

#ALPHA = [0.6, 0.8, 1.0]

# cache size of an nfv_nodes


# NFV cache policy for storing VNFs
NFV_NODE_CACHE_POLICY = 'NFV_CACHE'


# List of topologies tested
# Topology implementations are located in ./icarus/scenarios/topology.py
# Remove topologies not needed
TOPOLOGIES = ['TATANLD', 'ION', 'BESTEL', 'USCARRIER',  'COLT']

# List of caching and routing strategies
# The code is located in ./icarus/models/strategy/*.py
# Remove strategies not needed
POLICIES = ['BASELINE', 'HOD', 'TAP_ALGO']  # 'GREEDY_WITHOUT_PLACEMENT',

# Instantiate experiment queue
EXPERIMENT_QUEUE = deque()

# Create tree of experiment configuration
default = Tree()
default['workload'] = {'name':  'TRACE_DRIVEN',
                       'reqs_file': '/home/igor/PycharmProjects/TESE/nfvpysim/sfc_seq_len_2_test.csv',
                       'n_warmup': N_WARMUP_REQUESTS,
                       'n_measured': N_MEASURED_REQUESTS
                       }

default['vnf_allocation']['name'] = VNF_ALLOCATION_POLICY
default['nfv_cache_policy']['name'] = NFV_NODE_CACHE_POLICY



# Create experiments multiplexing all desired parameters
for policy in POLICIES:
    for topology in TOPOLOGIES:
        for vnf_allocation_space in VNF_ALLOCATION_SPACE:
            experiment = copy.deepcopy(default)
            experiment['policy']['name'] = policy
            experiment['topology']['name'] = topology
            experiment['vnf_allocation']['network_cache'] = vnf_allocation_space
            experiment['desc'] = "policy: %s, topology: %s, network cache: %s" \
                                     % (policy, topology, str(vnf_allocation_space))
            EXPERIMENT_QUEUE.append(experiment)