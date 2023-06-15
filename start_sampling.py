from tkinter.font import names
from samplers.SUSIE import *
from matching.KG.KnowledgeGraph import KnowledgeGraph
import sys
import os

from sample_utils import Utils

def start_sampling(dataset, method, p, s, t):

    kg1_mdi = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", method)
    kg2_mdi = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", method)

    kg1_mun = KnowledgeGraph("1", dataset, "multi_undirected", "original", "original", method)
    kg2_mun = KnowledgeGraph("2", dataset, "multi_undirected", "original", "original", method)

    print("\n-----START SAMPLING-----")
    print("It will takes some time ...")
    _, _, ents1, ents2, sampled_graph1, sampled_graph2, sampled_df, sampled_df2, sampled_attr_df1, sampled_attr_df2 = SUSIE.RJ_only_p(kg1_mdi, kg2_mdi, kg1_mun, kg2_mun, int(s), float(p), int(t))    
    
    print("Finished:")
    print(sampled_graph1.number_of_nodes())
    print(sampled_graph2.number_of_nodes())

    dest_path = "resources/Datasets/sampled/" + dataset + "_" + method + "/" + p + "_" + s + "_" + t
    isExist = os.path.exists(dest_path)
    if not isExist:
        os.makedirs(dest_path)

    sampled_df.to_csv(dest_path + "/rel_triples_1", sep="\t", index=False, columns=["e1", "r", "e2"], header=False)  
    sampled_df2.to_csv(dest_path + "/rel_triples_2", sep="\t", index=False, columns=["e1", "r", "e2"], header=False)
    sampled_attr_df1.to_csv(dest_path + "/attr_triples_1", sep="\t", index=False, columns=["e1", "attr", "val"], header=False)  
    sampled_attr_df2.to_csv(dest_path + "/attr_triples_2", sep="\t", index=False, columns=["e1", "attr", "val"], header=False)
    Utils.generate_seeds_and_splittings(dataset, "", ents1, ents2, dest_path +  "/721_5fold/2/", method)
    Utils.generate_rels(p + "_" + s + "_" + t, dataset)
    Utils.convert_sampling(p + "_" + s + "_" + t, dataset)