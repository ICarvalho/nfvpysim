"""Registry keeping track of all registered pluggable components"""

CACHE_POLICY = {}

# Dictionary storying all strategy implementations keyed by ID
POLICY = {}

# Dictionary storying all network topologies keyed by ID
TOPOLOGY_FACTORY = {}

# Dictionary storying all cache placement functions keyed by ID
VNF_ALLOCATION = {}

# Dictionary storying all vnf palcement functions keyed by ID
VNF_PLACEMENT = {}

# Dictionary storying all workload generators keyed by ID
WORKLOAD = {}

# Dictionary storying all data collector classes keyed by ID
DATA_COLLECTOR = {}

# Dictionary storying all results reader functions keyed by ID
RESULTS_READER = {}

# Dictionary storying all results writer functions keyed by ID
RESULTS_WRITER = {}


def register_decorator(register):
    """Returns a decorator that register a class or function to a specified
    register
    Parameters
    ----------
    register : dict
        The register to which the class or function is register
    Returns
    -------
    decorator : func
        The decorator
    """
    def decorator(name):
        """Decorator that register a class or a function to a register.
        Parameters
        ----------
        name : str
            The name assigned to the class or function to store in the register
        """
        def _decorator(function):
            register[name] = function
            function.name = name
            return function
        return _decorator
    return decorator


register_cache_policy = register_decorator(CACHE_POLICY)
register_policy = register_decorator(POLICY)
register_topology_factory = register_decorator(TOPOLOGY_FACTORY)
register_vnf_allocation = register_decorator(VNF_ALLOCATION)
register_vnf_placement = register_decorator(VNF_PLACEMENT)
register_workload = register_decorator(WORKLOAD)
register_data_collector = register_decorator(DATA_COLLECTOR)
register_results_reader = register_decorator(RESULTS_READER)
register_results_writer = register_decorator(RESULTS_WRITER)
