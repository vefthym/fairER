from matching.KG.KnowledgeGraph import KnowledgeGraph
from sampling.Statistics import *


def start_analysis(dataset, prefix, measure, sample, conf_id, method):

    kg1_mdi = KnowledgeGraph("1", dataset, prefix, "multi_directed", "original", "original", method)
    kg2_mdi = KnowledgeGraph("2", dataset, prefix, "multi_directed", "original", "original", method)

    kg1_mun = KnowledgeGraph("1", dataset, prefix, "multi_undirected", "original", "original", method)
    kg2_mun = KnowledgeGraph("2", dataset, prefix, "multi_undirected", "original", "original", method)

    Statistics.attrs_per_comp(kg1_mun)