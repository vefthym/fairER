from matching.KG.KnowledgeGraph import KnowledgeGraph
from sampling.Statistics import *


def start_analysis(dataset, prefix, measure, sample, conf_id, method, thres):

    kg1_mdi = KnowledgeGraph("1", dataset, prefix, "multi_directed", sample, conf_id, method)
    kg2_mdi = KnowledgeGraph("2", dataset, prefix, "multi_directed", sample, conf_id, method)

    # kg1_mun = KnowledgeGraph("1", dataset, prefix, "multi_undirected", sample, conf_id, method)
    # kg2_mun = KnowledgeGraph("2", dataset, prefix, "multi_undirected", sample, conf_id, method)

    # print(Statistics.basic_statistics(kg1_mdi))
    # print(Statistics.basic_statistics(kg2_mdi))

    # Statistics.explore("1", method, dataset, prefix, thres)

    Statistics.weakly_conn_comps("1", method, dataset, prefix, thres)
    Statistics.weakly_conn_comps("2", method, dataset, prefix, thres)

    Statistics.avg_rels_per_entity("1", method, dataset, prefix, thres)
    Statistics.avg_rels_per_entity("2", method, dataset, prefix, thres)

    Statistics.max_comp("1", method, dataset, prefix, thres)
    Statistics.max_comp("2", method, dataset, prefix, thres)

    # Statistics.avg_attrs_per_entity("1", method, dataset, prefix, thres)
    # Statistics.avg_attrs_per_entity("2", method, dataset, prefix, thres)

    # # print(Statistics.attrs_per_comp(kg1_mun))