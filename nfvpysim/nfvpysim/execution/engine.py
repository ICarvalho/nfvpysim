from nfvpysim.execution.network import NetworkModelBaseLine, NetworkModelProposal, NetworkViewBaseLine, NetworkViewProposal,  NetworkController
from nfvpysim.execution.collectors import CollectorProxy
from nfvpysim.registry import DATA_COLLECTOR, POLICY

__all__ = ['exec_experiment']


def exec_experiment(topology, workload, netconf, policy_baseline, polocy_proposal,  nfv_cache_policy, collectors):
    """Execute the simulation of a specific scenario.
    Parameters
    ----------
    topology : Topology
        The FNSS Topology object modelling the network topology on which
        experiments are run.
    workload : iterable
        An iterable object whose elements are (time, event) tuples, where time
        is a float type indicating the timestamp of the event to be executed
        and event is a dictionary storing all the attributes of the event to
        execute
    netconf : dict
        Dictionary of attributes to initialize the network model
    strategy : tree
        Strategy definition. It is tree describing the name of the strategy
        to use and a list of initialization attributes
    cache_policy : tree
        Cache policy definition. It is tree describing the name of the cache
        policy to use and a list of initialization attributes
    collectors: dict
        The collectors to be used. It is a dictionary in which keys are the
        names of collectors to use and values are dictionaries of attributes

    Returns
    -------
    results : Tree
        A tree with the aggregated simulation results from all collectors
    """
    model_baseline = NetworkModelBaseLine(topology, nfv_cache_policy, **netconf)
    model_proposal = NetworkModelProposal(topology, nfv_cache_policy, **netconf)
    view_baseline = NetworkViewBaseLine(model_baseline)
    view_proposal = NetworkViewProposal(model_proposal)
    controller_baseline = NetworkController(model_baseline)
    controller_proposal = NetworkController(model_proposal)


    collectors_inst_baseline = [DATA_COLLECTOR[name](view_baseline, **params)
                       for name, params in collectors.items()]
    collector_baseline = CollectorProxy(view_baseline, collectors_inst_baseline)
    controller_baseline.attach_collector(collector_baseline)

    policy_name_baseline = policy_baseline['name']
    policy_args_baseline = {k: v for k, v in policy_baseline.items() if k != 'name'}
    policy_inst_baseline = POLICY[policy_name_baseline](view_baseline, controller_baseline, **policy_args_baseline)



    collectors_inst_proposal = [DATA_COLLECTOR[name](view_proposal, **params)
                                for name, params in collectors.items()]
    collector_proposal = CollectorProxy(view_proposal, collectors_inst_proposal)
    controller_proposal.attach_collector(collector_proposal)

    policy_name_proposal = polocy_proposal['name']
    policy_args_proposal = {k: v for k, v in polocy_proposal.items() if k != 'name'}
    policy_inst_proposal = POLICY[policy_name_proposal](view_proposal, controller_proposal, **policy_args_proposal)




    for time, event in workload:
        policy_inst_baseline.process_event(time, **event)
        policy_inst_proposal.process_event(time, **event)
    return collector_baseline.results(), collector_proposal.results()
