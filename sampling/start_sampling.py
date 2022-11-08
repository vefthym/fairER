from tkinter.font import names
from sampling.Statistics import Statistics
from sampling.samplers.SUSIE_extension import *
from sampling.samplers.SUSIE import *
from matching.KG.KnowledgeGraph import KnowledgeGraph
import sys
import os

from sampling.utils import Utils


def start_sampling(conf):
    conf_id = conf.id
    measure = conf.measure
    dataset = conf.dataset
    prefix = conf.prefix
    sampling_size = conf.sampling_size
    p = conf.p
    export_sampled = conf.export_sampled
    method = conf.method
    sampling_method = conf.sampling_method

    kg1_mdi = KnowledgeGraph("1", dataset, prefix, "multi_directed", "original", "original", method)
    kg2_mdi = KnowledgeGraph("2", dataset, prefix, "multi_directed", "original", "original", method)

    kg1_mun = KnowledgeGraph("1", dataset, prefix, "multi_undirected", "original", "original", method)
    kg2_mun = KnowledgeGraph("2", dataset, prefix, "multi_undirected", "original", "original", method)

    print("\n-----START SAMPLING WITH ONLY P-----")
    print(Statistics.basic_statistics(kg1_mun))
    print(Statistics.basic_statistics(kg2_mun))

    if sampling_method == "SUSIE_ext":
        attr_thres = conf.attr_thres
        sus = SUSIE_extension(p, attr_thres, sampling_size)
        _, _, ents1, ents2, sampled_graph1, sampled_graph2, sampled_df, sampled_df2, sampled_attr_df1, sampled_attr_df2 = sus.RJ_only_p(kg1_mdi, kg2_mdi, kg1_mun, kg2_mun)
    elif sampling_method == "SUSIE":    
        _, _, ents1, ents2, sampled_graph1, sampled_graph2, sampled_df, sampled_df2 = SUSIE.RJ_only_p(kg1_mdi, kg2_mdi, kg1_mun, kg2_mun, sampling_size, p)
    
    print(sampled_graph1.number_of_nodes())
    print(sampled_graph2.number_of_nodes())

    Utils.check_embedding_constraints(kg1_mdi, ents1, ents2)
    
    if export_sampled:
        Utils.generate_seeds_and_splittings(dataset, prefix, ents1, ents2, "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/721_5fold/2/", method)
        dest_path = "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/"
        isExist = os.path.exists(dest_path)
        if isExist:
            if input("are you sure you want to override " + dest_path + " ? (y/n) ") != "y":
                exit()
        if not isExist:
            os.makedirs(dest_path)
        sampled_df.to_csv("matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/rel_triples_1", sep="\t", index=False, columns=["e1", "r", "e2"], header=False)  
        sampled_df2.to_csv("matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/rel_triples_2", sep="\t", index=False, columns=["e1", "r", "e2"], header=False)

        sampled_attr_df1.to_csv("matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/attr_triples_1", sep="\t", index=False, columns=["e1", "attr", "val"], header=False)  
        sampled_attr_df2.to_csv("matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/attr_triples_2", sep="\t", index=False, columns=["e1", "attr", "val"], header=False)
        conf.export("matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "_" + method + "/" + "configuration.txt")