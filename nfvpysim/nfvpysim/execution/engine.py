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
        Strategy definition. It is tree describing the name of the strategyJunto com Stacks 2.0 também v
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
    model_proposal_off = NetworkModelProposalOff(topology, nfv_cache_policy, **netconf)
    model_hod_deg = NetworkModelProposalDegree(topology, nfv_cache_policy, **netconf)
    model_hod_close = NetworkModelProposalCloseness(topology, nfv_cache_policy, **netconf)
    model_hod_page = NetworkModelProposalPageRank(topology, nfv_cache_policy, **netconf)
    model_hod_eigen = NetworkModelProposalEigenVector(topology, nfv_cache_policy, **netconf)
    model_first_fit = NetworkModelFirstFit(topology, nfv_cache_policy, **netconf)

    # view_holu = NetworkViewHolu(model_holu)
    view_markov = NetworkViewMarkov(model_markov)
    view_tap_algo = NetworkViewTapAlgo(model_tap_algo)
    view_first_order = NetworkViewFirstOrder(model_first_order)
    view_baseline = NetworkViewBaseLine(model_baseline)
    view_proposal = NetworkViewProposal(model_proposal)
    view_proposal_off = NetworkViewProposalOff(model_proposal_off)
    view_deg = NetworkViewDeg(model_hod_deg)
    view_close = NetworkViewClose(model_hod_close)
    view_page = NetworkViewPage(model_hod_page)
    view_eigen = NetworkViewEigen(model_hod_eigen)
    view_first_fit = NetworkViewFirstFit(model_first_fit)

    # controller_holu = NetworkController(model_holu)
    controller_markov = NetworkController(model_markov)
    controller_tap_algo = NetworkController(model_tap_algo)
    controller_first_order = NetworkController(model_first_order)
    controller_baseline = NetworkController(model_baseline)
    controller_proposal = NetworkController(model_proposal)
    controller_proposal_off = NetworkController(model_proposal_off)
    controller_deg = NetworkController(model_hod_deg)
    controller_close = NetworkController(model_hod_close)
    controller_page = NetworkController(model_hod_page)
    controller_eigen = NetworkController(model_hod_eigen)
    controller_first_fit = NetworkController(model_first_fit)

    if policy['name'] == 'FIRST_FIT':
        collectors_inst_first_fit = [DATA_COLLECTOR[name](view_first_fit, **params)
                                     for name, params in collectors.items()]
        collector_first_fit = CollectorProxy(view_first_fit, collectors_inst_first_fit)
        controller_first_fit.attach_collector(collector_first_fit)

        policy_name_first_fit = policy['name']
        policy_args_first_fit = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_first_fit = POLICY[policy_name_first_fit](view_first_fit, controller_first_fit,
                                                              **policy_args_first_fit)

        for time, event in workload:
            policy_inst_first_fit.process_event(time, **event)
        return collector_first_fit.results()

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

    if policy['name'] == 'HOD_VNF':
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

    if policy['name'] == 'HOD_VNF_OFF':
        collectors_inst_proposal_off = [DATA_COLLECTOR[name](view_proposal, **params)
                                        for name, params in collectors.items()]
        collector_proposal_off = CollectorProxy(view_proposal_off, collectors_inst_proposal_off)
        controller_proposal_off.attach_collector(collector_proposal_off)

        policy_name_proposal_off = policy['name']
        policy_args_proposal_off = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_proposal_off = POLICY[policy_name_proposal_off](view_proposal_off, controller_proposal_off,
                                                                    **policy_args_proposal_off)

        for time, event in workload:
            policy_inst_proposal_off.process_event(time, **event)
        return collector_proposal_off.results()

    if policy['name'] == 'HOD_DEG':
        collectors_inst_hod_deg = [DATA_COLLECTOR[name](view_deg, **params)
                                   for name, params in collectors.items()]
        collector_hod_deg = CollectorProxy(view_deg, collectors_inst_hod_deg)
        controller_deg.attach_collector(collector_hod_deg)

        policy_name_hod_deg = policy['name']
        policy_args_hod_deg = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_hod_deg = POLICY[policy_name_hod_deg](view_deg, controller_deg, **policy_args_hod_deg)

        for time, event in workload:
            policy_inst_hod_deg.process_event(time, **event)
        return collector_hod_deg.results()

    if policy['name'] == 'HOD_CLOSE':
        collectors_inst_hod_close = [DATA_COLLECTOR[name](view_close, **params)
                                     for name, params in collectors.items()]
        collector_hod_close = CollectorProxy(view_close, collectors_inst_hod_close)
        controller_close.attach_collector(collector_hod_close)

        policy_name_hod_close = policy['name']
        policy_args_hod_close = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_hod_close = POLICY[policy_name_hod_close](view_close, controller_close, **policy_args_hod_close)

        for time, event in workload:
            policy_inst_hod_close.process_event(time, **event)
        return collector_hod_close.results()

    if policy['name'] == 'HOD_PAGE':
        collectors_inst_hod_page = [DATA_COLLECTOR[name](view_page, **params)
                                    for name, params in collectors.items()]
        collector_hod_page = CollectorProxy(view_page, collectors_inst_hod_page)
        controller_page.attach_collector(collector_hod_page)

        policy_name_hod_page = policy['name']
        policy_args_hod_page = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_hod_page = POLICY[policy_name_hod_page](view_page, controller_page, **policy_args_hod_page)

        for time, event in workload:
            policy_inst_hod_page.process_event(time, **event)
        return collector_hod_page.results()

    if policy['name'] == 'HOD_EIGEN':
        collectors_inst_hod_eigen = [DATA_COLLECTOR[name](view_eigen, **params)
                                     for name, params in collectors.items()]
        collector_hod_eigen = CollectorProxy(view_eigen, collectors_inst_hod_eigen)
        controller_eigen.attach_collector(collector_hod_eigen)

        policy_name_hod_eigen = policy['name']
        policy_args_hod_eigen = {k: v for k, v in policy.items() if k != 'name'}
        policy_inst_hod_eigen = POLICY[policy_name_hod_eigen](view_eigen, controller_eigen, **policy_args_hod_eigen)

        for time, event in workload:
            policy_inst_hod_eigen.process_event(time, **event)
        return collector_hod_eigen.results()


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
