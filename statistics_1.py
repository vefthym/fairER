from matching import run_deepmatcher as dm
import sys
import os
import util
import json
import pandas as pd
from matching.KG.KnowledgeGraph import KnowledgeGraph
import networkx as nx
import pandas as pd


def basic_statistics(kg):
    nodes = kg.graph.number_of_nodes()
    triples = kg.graph.number_of_edges()
    return nodes, triples

def weakly_conn_comps(kg_mdi):
    return nx.number_weakly_connected_components(kg_mdi.graph)/kg_mdi.graph.number_of_nodes()


def avg_rels_per_entity(kg_mdi):

    nodes_deg = kg_mdi.graph.degree()

    counter = 0
    for pair in nodes_deg:
        counter += pair[1]
    avg_node_deg = counter / kg_mdi.graph.number_of_nodes()

    return avg_node_deg

def max_comp(kg_mdi):
    comps = sorted(nx.weakly_connected_components(kg_mdi.graph), key=len)
    max_len = len(comps[-1])/kg_mdi.graph.number_of_nodes()
    return max_len

def main(dataset):
        
        
    kg1_mdi = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RDGCN")
    kg2_mdi = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RDGCN")

    kg1_mun = KnowledgeGraph("1", dataset, "multi_undirected", "original", "original", "RDGCN")
    kg2_mun = KnowledgeGraph("2", dataset, "multi_undirected", "original", "original", "RDGCN")

    nodes1, triples1 = basic_statistics(kg1_mun)
    nodes2, triples2 = basic_statistics(kg2_mun)

    rels1 = kg1_mdi.num_rel_type
    rels2 = kg2_mdi.num_rel_type

    wccR1 = weakly_conn_comps(kg1_mdi)
    wccR2 = weakly_conn_comps(kg2_mdi)

    deg1 = avg_rels_per_entity(kg1_mdi)
    deg2 = avg_rels_per_entity(kg2_mdi)

    maxcs1 = max_comp(kg1_mdi)
    maxcs2 = max_comp(kg2_mdi)   

    #################################
    # Write statistics to json file
    #################################
    data = {'#Nodes KG1': str(nodes1), '#Nodes KG2': str(nodes2),
            '#Relations KG1': str(rels1), '#Relations KG2': str(rels2),
            '#Triples KG1': str(triples1), '#Triples KG2': str(triples2),
            'wccR KG1': str(wccR1), 'wccR KG2': str(wccR2),
            'maxCS KG1': str(maxcs1), 'maxCS KG2': str(maxcs2),
            'deg KG1': str(deg1), 'deg KG2': str(deg2)}
    json_string = json.dumps(data)
    with open('web/data/json_data/statistics_data.json', 'w+') as outfile:
        outfile.write(json_string)