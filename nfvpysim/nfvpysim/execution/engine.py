from nfvpysim.execution.network import *
from nfvpysim.execution.collectors import CollectorProxy
from nfvpysim.registry import DATA_COLLECTOR, POLICY

__all__ = ['exec_experiment']


def exec_experiment(topology, workload, netconf, policy, nfv_cache_policy, collectors):
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
    policy : tree
        Strategy definition. It is tree describing the name of the strategy
        to use and a list of initialization attributes
    nfv_cache_policy : tree
        Cache policy definition. It is tree describing the name of the cache
        policy to use and a list of initialization attributes
    collectors: dict
        The collectors to be used. It is a dictionary in which keys are the
        names of collectors to use and values are dictionaries of attributes

    Returns
    -------
    results : Tree
        A tree with the aggregated simulation results from all collectors
        :param nfv_cache_policy:
    """
    model_holu = NetworkModelHolu(topology, nfv_cache_policy, **netconf)
    model_tap_algo = NetworkModelTapAlgo(topology, nfv_cache_policy, **netconf)
    model_markov = NetworkModelMarkov(topology, nfv_cache_policy, **netconf)
    model_first_order = NetworkModelFirstOrder(topology, nfv_cache_policy, **netconf)
    model_baseline = NetworkModelBaseLine(topology, nfv_cache_policy, **netconf)
    model_proposal = NetworkModelProposal(topology, nfv_cache_policy, **netconf)

    view_holu = NetworkViewHolu(model_holu)
    view_markov = NetworkViewMarkov(model_markov)
    view_tap_algo = NetworkViewTapAlgo(model_tap_algo)
    view_first_order = NetworkViewFirstOrder(model_first_order)
    view_baseline = NetworkViewBaseLine(model_baseline)
    view_proposal = NetworkViewProposal(model_proposal)

    controller_holu = NetworkController(model_holu)
    controller_markov = NetworkController(model_markov)
    controller_tap_algo = NetworkController(model_tap_algo)
    controller_first_order = NetworkController(model_first_order)
    controller_baseline = NetworkController(model_baseline)
    controller_proposal = NetworkController(model_proposal)

    if policy['name'] == 'BCSP':
        collectors_inst_holu = [DATA_COLLECTOR[name](view_holu, **params)
                                for name, params in collectors.items()]
        collector_holu = CollectorProxy(view_holu, collectors_inst_holu)
        controller_holu.attach_collector(collector_holu)

        policy_name_holu = policy['name']
        policy_args_holu = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_holu = POLICY[policy_name_holu](view_holu, controller_holu, **policy_args_holu)

        for time, event in workload:
            policy_inst_holu.process_event(time, **event)
        return collector_holu.results()

    if policy['name'] == 'MARKOV':
        collectors_inst_markov = [DATA_COLLECTOR[name](view_markov, **params)
                                  for name, params in collectors.items()]
        collector_markov = CollectorProxy(view_markov, collectors_inst_markov)
        controller_markov.attach_collector(collector_markov)

        policy_name_markov = policy['name']
        policy_args_markov = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_markov = POLICY[policy_name_markov](view_markov, controller_markov, **policy_args_markov)

        for time, event in workload:
            policy_inst_markov.process_event(time, **event)
        return collector_markov.results()

    if policy['name'] == 'TAP_ALGO':
        collectors_inst_tap_algo = [DATA_COLLECTOR[name](view_tap_algo, **params)
                                    for name, params in collectors.items()]
        collector_tap_algo = CollectorProxy(view_tap_algo, collectors_inst_tap_algo)
        controller_tap_algo.attach_collector(collector_tap_algo)

        policy_name_tap_algo = policy['name']
        policy_args_tap_algo = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_tap_algo = POLICY[policy_name_tap_algo](view_tap_algo, controller_tap_algo, **policy_args_tap_algo)

        for time, event in workload:
            policy_inst_tap_algo.process_event(time, **event)
        return collector_tap_algo.results()

    if policy['name'] == 'FIRST_ORDER':
        collectors_inst_first_order = [DATA_COLLECTOR[name](view_first_order, **params)
                                       for name, params in collectors.items()]
        collector_first_order = CollectorProxy(view_first_order, collectors_inst_first_order)
        controller_first_order.attach_collector(collector_first_order)

        policy_name_first_order = policy['name']
        policy_args_first_order = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_first_order = POLICY[policy_name_first_order](view_first_order, controller_first_order,
                                                                  **policy_args_first_order)

        for time, event in workload:
            policy_inst_first_order.process_event(time, **event)
        return collector_first_order.results()

    if policy['name'] == 'BASELINE':
        collectors_inst_baseline = [DATA_COLLECTOR[name](view_baseline, **params)
                                    for name, params in collectors.items()]
        collector_baseline = CollectorProxy(view_baseline, collectors_inst_baseline)
        controller_baseline.attach_collector(collector_baseline)

        policy_name_baseline = policy['name']
        policy_args_baseline = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_baseline = POLICY[policy_name_baseline](view_baseline, controller_baseline, **policy_args_baseline)

        for time, event in workload:
            policy_inst_baseline.process_event(time, **event)
        return collector_baseline.results()

    if policy['name'] == 'HOD':
        collectors_inst_proposal = [DATA_COLLECTOR[name](view_proposal, **params)
                                    for name, params in collectors.items()]
        collector_proposal = CollectorProxy(view_proposal, collectors_inst_proposal)
        controller_proposal.attach_collector(collector_proposal)

        policy_name_proposal = policy['name']
        policy_args_proposal = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_proposal = POLICY[policy_name_proposal](view_proposal, controller_proposal, **policy_args_proposal)

        for time, event in workload:
            policy_inst_proposal.process_event(time, **event)
        return collector_proposal.results()


"""
    
     model = NetworkModelProposal(topology, nfv_cache_policy, **netconf)
    view = NetworkViewProposal(model)
    controller = NetworkController(model)

    collectors_inst = [DATA_COLLECTOR[name](view, **params)
                       for name, params in collectors.items()]
    collector = CollectorProxy(view, collectors_inst)
    controller.attach_collector(collector)

    policy_name = policy['name']
    policy_args = {k: v for k, v in policy.items() if k != 'name'}
    policy_inst = POLICY[policy_name](view, controller, **policy_args)

    for time, event in workload:
        policy_inst.process_event(time, **event)
    return collector.results()
    
"""
