from collections import OrderedDict
from operator import itemgetter
import networkx as nx
from nfvpysim.scenarios.topology import *


#HOD_BETW
def get_top_betw_nodes(topology, n_of_nodes):
    dict_nodes_betw = nx.betweenness_centrality(topology)
    ord_dict =  OrderedDict(sorted(dict_nodes_betw.items(), key=itemgetter(1), reverse=True))
    return dict(list(ord_dict.items())[0:n_of_nodes])


#HOD_DEG
def get_top_degree_nodes(topology, n_of_nodes):
    dict_nodes_deg = nx.degree_centrality(topology)
    ord_dict =  OrderedDict(sorted(dict_nodes_deg.items(), key=itemgetter(1), reverse=True))
    return dict(list(ord_dict.items())[0:n_of_nodes])


#HOD_CLOSE
def get_top_close_nodes(topology, n_of_nodes):
    dict_nodes_close = nx.closeness_centrality(topology)
    ord_dict =  OrderedDict(sorted(dict_nodes_close.items(), key=itemgetter(1), reverse=True))
    return dict(list(ord_dict.items())[0:n_of_nodes])


#HOD_PAGE
def get_top_pg_rank_nodes(topology, n_of_nodes):
    dict_nodes_pg_rank = nx.pagerank(topology, alpha=0.9)
    ord_dict =  OrderedDict(sorted(dict_nodes_pg_rank.items(), key=itemgetter(1), reverse=True))
    return dict(list(ord_dict.items())[0:n_of_nodes])


#HOD_EIGEN
def get_top_eigen_nodes(topology, n_of_nodes):
    dict_nodes_eigen = nx.eigenvector_centrality(topology, max_iter=500)
    ord_dict =  OrderedDict(sorted(dict_nodes_eigen.items(), key=itemgetter(1), reverse=True))
    return dict(list(ord_dict.items())[0:n_of_nodes])



topologies = [topology_ion(), topology_bestel(), topology_cogentco(), topology_colt(), topology_geant(),
              topology_tatanld(), topology_interroute(), topology_viatel(), topology_uscarrier()]




top_deg = list(get_top_eigen_nodes(topology_uscarrier(), 10))
print(top_deg)

