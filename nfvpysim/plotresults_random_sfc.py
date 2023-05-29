#!/usr/bin/env python
"""Plot results read from a result set
"""
from __future__ import division
import os
import argparse
import logging

import matplotlib.pyplot as plt

from nfvpysim.util import Settings, config_logging
from nfvpysim.results.plot import plot_lines, plot_bar_chart
from nfvpysim.registry import RESULTS_READER

# Logger object
logger = logging.getLogger('plot')

# These lines prevent insertion of Type 3 fonts in figures
# Publishers don't want them
plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True

# If True text is interpreted as LaTeX, e.g. underscore are interpreted as
# subscript. If False, text is interpreted literally
plt.rcParams['text.usetex'] = False

# Aspect ratio of the output figures
plt.rcParams['figure.figsize'] = 12, 5

# Size of font in legends
LEGEND_SIZE = 5

# Line width in pixels
LINE_WIDTH = 1.5

# Plot
PLOT_EMPTY_GRAPHS = True

# This dict maps strategy names to the style of the line to be used in the plots
# Off-path strategies: solid lines
# On-path strategies: dashed lines
# No-cache: dotted line
POLICY_STYLE = {
    'HOD_VNF': 'k--^',
    'HOD_VNF_OFF': 'b--p',
    'FIRST_FIT': 'r--<',
    'TAP_ALGO': 'g-->',
    'HOD_EIGEN': 'c--s'

    # 'BASELINE': 'r--D',
    # 'HOD': 'k--^',
    # 'FIRST_ORDER': 'm--s',
    # 'TAP_ALGO': 'c-s',
    # 'BCSP':    'g-^',
    # 'HR_HYBRID_AM':    'c-s',
    # 'HR_HYBRID_SM':    'r-v',
    # 'LCE':             'b--p',
    # 'LCD':             'g-->',
    # 'CL4M':            'g-->',
    # 'PROB_CACHE':      'c--<',
    # 'RAND_CHOICE':     'r--<',
    # 'RAND_BERNOULLI':  'g--*',
    # 'NO_CACHE':        'k:o',
    # 'OPTIMAL':         'k-o'
}

# This dict maps name of strategies to names to be displayed in the legend
POLICY_LEGEND = {

    'HOD_VNF': 'NS-HOD',
    'HOD_VNF_OFF': 'HOD_VNF_OFF',
    'BASELINE': 'GREEDY',
    'FIRST_FIT': 'FF',
    'FIRST_ORDER': 'SECOND_ORD',
    'TAP_ALGO': 'TAP_ALGO',
    'MARKOV': 'MARKOV'

    # 'HOD_DEG': 'HOD_DEG',
    # 'HOD_CLOSE': 'HOD_CLOSE',
    # 'HOD_PAGE': 'HOD_PAGE',
    # 'HOD_EIGEN': 'HOD_EIGEN'

    # 'BASELINE': 'BASELINE',
    # 'HOD': 'HOD',
    # 'FIRST_ORDER': 'FIRST_ORD',
    # 'TAP_ALGO': 'TAP_VNF',
    # 'MARKOV': 'MARKOV',
    # 'BCSP':         'BCSP',
    # 'HR_ASYMM':        'HR Asymm',
    # 'HR_MULTICAST':    'HR Multicast',
    # 'HR_HYBRID_AM':    'HR Hybrid AM',
    # 'HR_HYBRID_SM':    'HR Hybrid SM',
    # 'CL4M':            'CL4M',
    # 'PROB_CACHE':      'ProbCache',
    # 'RAND_CHOICE':     'Random (choice)',
    # 'RAND_BERNOULLI':  'Random (Bernoulli)',
    # 'NO_CACHE':        'No caching',
    # 'OPTIMAL':         'Optimal'
}

# Color and hatch styles for bar charts of cache hit ratio and link load vs topology
POLICY_BAR_COLOR_CACHE_SIZE = {

    'HOD_VNF': 'blue',
    'HOD_VNF_OFF': 'navy',
    'BASELINE': 'darkorange',
    'FIRST_FIT': 'darkred',
    'FIRST_ORDER': 'k',
    'TAP_ALGO': 'k',
    'MARKOV': 'pink'

    # 'BASELINE': 'dimgray',
    # 'HOD': 'black',
    # 'FIRST_ORDER': 'lightgray',
    # 'TAP_ALGO': 'grey',
    # 'MARKOV': 'silver',
    # 'BCSP':     'gainsboro',
    # 'HR_ASYMM':     '0.6',
    # 'HR_SYMM':      '0.7'
}

POLICY_BAR_COLOR_LATENCY = {

    'HOD_VNF': 'blue',
    'HOD_VNF_OFF': 'navy',
    'BASELINE': 'darkorange',
    'FIRST_FIT': 'darkred',
    'FIRST_ORDER': 'k',
    'TAP_ALGO': 'k',
    'MARKOV': 'pink',

    # 'BASELINE': 'dimgray',
    # 'HOD': 'black',
    # 'FIRST_ORDER': 'lightgray',
    # 'TAP_ALGO': 'grey',
    # 'MARKOV': 'silver',
    # 'BCSP':     'gainsboro',
    # 'NO_CACHE':     '0.5',
    # 'HR_ASYMM':     '0.6',
    # 'HR_SYMM':      '0.7'
}

POLICY_BAR_COLOR_LINK_LOAD = {

    'HOD_VNF': 'blue',
    'HOD_VNF_OFF': 'navy',
    'BASELINE': 'darkorange',
    'FIRST_FIT': 'darkred',
    'FIRST_ORDER': 'k',
    'TAP_ALGO': 'k',
    'MARKOV': 'pink'

}

POLICY_BAR_COLOR_PATH_STRETCH = {

    'HOD_VNF': 'blue',
    'HOD_VNF_OFF': 'navy',
    'BASELINE': 'darkorange',
    'FIRST_FIT': 'darkred',
    'FIRST_ORDER': 'k',
    'TAP_ALGO': 'k',
    'MARKOV': 'pink'

    # 'BASELINE': 'dimgray',
    # 'HOD': 'black',
    # 'FIRST_ORDER': 'lightgray',
    # 'TAP_ALGO': 'grey',
    # 'MARKOV': 'silver',
    # 'BCSP': 'gainsboro',
    # 'NO_CACHE':     '0.5',
    # 'HR_ASYMM':     '0.6',
    # 'HR_SYMM':      '0.7'
}

POLICY_BAR_HATCH = {

    'HOD_VNF': '/',
    'HOD_VNF_OFF': '*',
    'BASELINE': '.',
    'FIRST_FIT': '-',
    'FIRST_ORDER': '\\',
    'TAP_ALGO': 'x',
   # 'MARKOV': 'x',

    # 'BASELINE': '/',
    # 'HOD': 'o',
    # 'FIRST_ORDER': 'x',
    # 'TAP_ALGO': '..',
    # 'MARKOV': '-',
    # 'BCSP':     '++',
    # 'HR_ASYMM':     '+',
    # 'HR_SYMM':      '\\'
}


def plot_cache_hits_vs_n_sfc_requests(resultset, topology, nfv_cache_size, n_measured_range, policies, plotdir):
    if 'NO_CACHE' in policies:
        policies.remove('NO_CACHE')
    desc = {}
    desc['title'] = 'Service Acceptance Ratio - Topology: %s' % topology
    desc['ylabel'] = 'Acceptance Ratio'
    desc['xscale'] = 'log'
    desc['xlabel'] = 'Number of requests'
    desc['xparam'] = ('workload', 'n_measured')
    desc['xvals'] = n_measured_range
    desc['filter'] = {'topology': {'name': topology},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured_range},
                      'vnf_allocation': {'network_cache': nfv_cache_size}}
    desc['ymetrics'] = [('ACCEPTANCE_RATIO', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['line_style'] = POLICY_STYLE
    desc['line_width'] = LINE_WIDTH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_lines(resultset, desc, 'SERVICE_ACCEPTANCE_RATIO_T=%s.pdf'
               % topology, plotdir)


def plot_link_load_vs_n_sfc_requests(resultset, topology, nfv_cache_size, n_measured_range, policies, plotdir):
    desc = {}
    desc['title'] = 'Average Link Load Consumption - Topology: %s' % topology
    desc['xlabel'] = 'Number of requests'
    desc['ylabel'] = 'Link Load (Mbps)'
    desc['xscale'] = 'log'
    desc['xparam'] = ('workload', 'n_measured')
    desc['xvals'] = n_measured_range
    desc['filter'] = {'topology': {'name': topology},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured_range},
                      'vnf_allocation': {'network_cache': nfv_cache_size}}
    desc['ymetrics'] = [('LINK_LOAD', 'MEAN_INTERNAL')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['line_style'] = POLICY_STYLE
    desc['legend'] = POLICY_LEGEND
    desc['legend_size'] = LEGEND_SIZE
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_lines(resultset, desc, 'AVERAGE_LINK_LOAD_T=%s.pdf'
               % topology, plotdir)


def plot_latency_vs_n_requests(resultset, topology, nfv_cache_size, n_measured_range, policies, plotdir):
    desc = {}
    desc['title'] = 'Average End-to-End Delay - Topology: %s' % topology
    desc['xlabel'] = 'Number of requests'
    desc['ylabel'] = 'Delay'
    desc['xscale'] = 'log'
    desc['xparam'] = ('workload', 'n_measured')
    desc['xvals'] = n_measured_range
    desc['filter'] = {'topology': {'name': topology},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured_range},
                      'vnf_allocation': {'network_cache': nfv_cache_size}}
    desc['ymetrics'] = [('LATENCY', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('strategy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['line_style'] = POLICY_STYLE
    desc['legend'] = POLICY_LEGEND
    desc['legend_size'] = LEGEND_SIZE
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_lines(resultset, desc, 'AVERAGE_END_TO_END_DELAY_T=%s.pdf'
               % topology, plotdir)


def plot_cache_hits_vs_topology(resultset, n_measured, nfv_cache_size, topology_range, policies, plotdir):
    desc = {}
    desc['title'] = 'Service Acceptance Ratio - N. of Requests: %s' % n_measured
    desc['ylabel'] = 'Acceptance Ratio'
    desc['xparam'] = ('topology', 'name')
    desc['xvals'] = topology_range
    desc['filter'] = {'vnf_allocation': {'network_cache': nfv_cache_size},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured}}
    desc['ymetrics'] = [('ACCEPTANCE_RATIO', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['bar_color'] = POLICY_BAR_COLOR_CACHE_SIZE
    desc['bar_hatch'] = POLICY_BAR_HATCH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_bar_chart(resultset, desc, 'SFC_HIT_RATIO_N=%s.pdf'
                   % n_measured, plotdir)


def plot_link_load_vs_topology(resultset, n_measured, nfv_cache_size, topology_range, policies, plotdir):
    """
    Plot bar graphs of link load for specific values of alpha and cache
    size for various topologies.
    The objective here is to show that our algorithms works well on all
    topologies considered
    """
    desc = {}
    desc['title'] = 'Average Link Load Consumption: N. of Requests: %s' % n_measured
    desc['ylabel'] = 'Link Load (Mbps)'
    desc['xscale'] = 'log'
    desc['xparam'] = ('topology', 'name')
    desc['xvals'] = topology_range
    desc['filter'] = {'vnf_allocation': {'network_cache': nfv_cache_size},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured}}
    desc['ymetrics'] = [('LINK_LOAD', 'MEAN_INTERNAL')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['bar_color'] = POLICY_BAR_COLOR_LINK_LOAD
    desc['bar_hatch'] = POLICY_BAR_HATCH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_bar_chart(resultset, desc, 'AVERAGE_LINK_LOAD_N=%s.pdf'
                   % n_measured, plotdir)


def plot_latency_vs_topology(resultset, n_measured, nfv_cache_size, topology_range, policies, plotdir):
    """
    Plot bar graphs of link load for specific values of alpha and cache
    size for various topologies.
    The objective here is to show that our algorithms works well on all
    topologies considered
    """
    desc = {}
    desc['title'] = 'Average End-to-End Delay - N. of Requests: %s' % n_measured
    desc['ylabel'] = 'Delay (ms)'
    desc['xlabel'] = 'Topology'
    desc['xscale'] = 'log'
    desc['xparam'] = ('topology', 'name')
    desc['xvals'] = topology_range
    desc['filter'] = {'vnf_allocation': {'network_cache': nfv_cache_size},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured}}
    desc['ymetrics'] = [('LATENCY', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['bar_color'] = POLICY_BAR_COLOR_CACHE_SIZE
    desc['bar_hatch'] = POLICY_BAR_HATCH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_bar_chart(resultset, desc, 'AVERAGE_END_TO_END_DELAY_N=%s.pdf'
                   % n_measured, plotdir)


def plot_path_stretch_vs_n_requests(resultset, topology, nfv_cache_size, n_measured_range, policies, plotdir):
    desc = {}
    desc['title'] = 'Average Path-Stretch Ratio - Topology: %s' % topology
    desc['xlabel'] = 'Number of requests'
    desc['ylabel'] = 'Stretch ratio '
    desc['xscale'] = 'log'
    desc['xparam'] = ('workload', 'n_measured')
    desc['xvals'] = n_measured_range
    desc['filter'] = {'topology': {'name': topology},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured_range},
                      'vnf_allocation': {'network_cache': nfv_cache_size}}
    desc['ymetrics'] = [('PATH_STRETCH', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('strategy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['line_style'] = POLICY_STYLE
    desc['line_width'] = LINE_WIDTH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_lines(resultset, desc, 'AVERAGE_PATH_STRETCH_T=%s.pdf'
               % topology, plotdir)


def plot_path_stretch_vs_topology(resultset, n_measured, nfv_cache_size, topology_range, policies, plotdir):
    desc = {}
    desc['title'] = 'Average Path-Stretch Ratio - N. of Requests: %s' % n_measured
    desc['ylabel'] = 'Stretch ratio'
    desc['xparam'] = ('topology', 'name')
    desc['xvals'] = topology_range
    desc['filter'] = {'vnf_allocation': {'network_cache': nfv_cache_size},
                      'workload': {'name': 'STATIONARY_RANDOM_SFC', 'n_measured': n_measured}}
    desc['ymetrics'] = [('PATH_STRETCH', 'MEAN')] * len(policies)
    desc['ycondnames'] = [('policy', 'name')] * len(policies)
    desc['ycondvals'] = policies
    desc['errorbar'] = True
    desc['legend_loc'] = 'best'
    desc['bar_color'] = POLICY_BAR_COLOR_PATH_STRETCH
    desc['bar_hatch'] = POLICY_BAR_HATCH
    desc['legend'] = POLICY_LEGEND
    desc['plotempty'] = PLOT_EMPTY_GRAPHS
    plot_bar_chart(resultset, desc, 'AVERAGE_PATH_STRETCH_N=%s.pdf'
                   % n_measured, plotdir)


def run(config, results, plotdir):
    """Run the plot script
    Parameters
    ----------
    config : str
        The path of the configuration file
    results : str
        The file storing the experiment results
    plotdir : str
        The directory into which graphs will be saved
    """
    settings = Settings()
    settings.read_from(config)
    config_logging(settings.LOG_LEVEL)
    resultset = RESULTS_READER[settings.RESULTS_FORMAT](results)
    # Create dir if not existing
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    # Parse params from settings
    topologies = settings.TOPOLOGIES
    n_of_sfc_requests = settings.N_MEASURED_REQUESTS
    nfv_cache_sizes = settings.VNF_ALLOCATION_SPACE
    # sfc_lens = settings.SFC_LEN
    policies = settings.POLICIES
    # Plot graphs
    for nfv_cache_size in nfv_cache_sizes:
        for topology in topologies:
            logger.info('Plotting sfc hit ratio for topology %s and cache size %s vs number of sfc requests' % (
                topology, str(nfv_cache_size)))
            plot_cache_hits_vs_n_sfc_requests(resultset, topology, nfv_cache_size, n_of_sfc_requests, policies, plotdir)
            logger.info('Plotting link load for topology %s vs cache size %s' % (topology, str(nfv_cache_size)))
            plot_link_load_vs_n_sfc_requests(resultset, topology, nfv_cache_size, n_of_sfc_requests, policies, plotdir)
            logger.info('Plotting latency considering the number of requests')
            plot_latency_vs_n_requests(resultset, topology, nfv_cache_size, n_of_sfc_requests, policies, plotdir)
            logger.info('Plotting path stretch considering the number of requests')
            plot_path_stretch_vs_n_requests(resultset, topology, nfv_cache_size, n_of_sfc_requests, policies, plotdir)

    for nfv_cache_size in nfv_cache_sizes:
        for n_of_sfc_request in n_of_sfc_requests:
            logger.info('Plotting sfc hit ratio  for all topologies ')
            plot_cache_hits_vs_topology(resultset, n_of_sfc_request, nfv_cache_size, topologies, policies, plotdir)
            logger.info('Plotting latency for all topologies ')
            plot_latency_vs_topology(resultset, n_of_sfc_request, nfv_cache_size, topologies, policies, plotdir)
            logger.info('Plotting link load for all topologies')
            plot_link_load_vs_topology(resultset, n_of_sfc_request, nfv_cache_size, topologies, policies, plotdir)
            logger.info('Plotting path stretch for all topologies')
            plot_path_stretch_vs_topology(resultset, n_of_sfc_request, nfv_cache_size, topologies, policies, plotdir)

    logger.info('Exit. Plots were saved in directory %s' % os.path.abspath(plotdir))


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("-r", "--results", dest="results",
                        help='the results file',
                        required=True)
    parser.add_argument("-o", "--output", dest="output",
                        help='the output directory where plots will be saved',
                        required=True)
    parser.add_argument("config",
                        help="the configuration file")
    args = parser.parse_args()
    run(args.config, args.results, args.output)


if __name__ == '__main__':
    main()
