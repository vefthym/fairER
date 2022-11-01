import time
from clustering import unique_mapping_clustering as umc
import os
import pickle
from fairsearchcore.models import FairScoreDoc
from fair_ranking import fa_ir as fr
from matching.Grouping import Grouping
from matching.KG.KnowledgeGraph import KnowledgeGraph
from clustering import fair_unique_mapping_clustering as fumc
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
import web.library.methods as methods

"""
        Run fairER method for OpenEA method (unique mapping clustering)
"""

def main(dataset, k_results, which_entity, conf_id, sample, method_sim_list):
    dest_path = "matching/RREA/exp_results/test_experiments/" + method_sim_list + "/" + dataset + "/" + conf_id + "/" + dataset + "_sim_lists_NO_CSLS_sampled.pickle"
    isExist = os.path.exists(dest_path)

    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, manually run OpenEA method to produce similarity lists and re-run for unique mapping clustering
    """
    if isExist:
        with (open(dest_path, "rb")) as fp:
            sim_lists_no_csls = pickle.load(fp)

        # Corrects the wrong entity-metric pairs of similarity lists of RDGCN
        # This happens because of manhattan metric used for this method
        if method_sim_list == "RDGCN":
            for pair in sim_lists_no_csls:
                temp_measures = list()
                for p in range(len(sim_lists_no_csls[pair])):
                    temp_measures.append(sim_lists_no_csls[pair][p][1])
                temp_measures.sort(reverse=True)
                for p in range(len(sim_lists_no_csls[pair])):
                    sim_lists_no_csls[pair][p] = (sim_lists_no_csls[pair][p][0], temp_measures[p]) 

        index_to_id = {}
        for pair in sim_lists_no_csls:
            index_to_id[pair[0]] = pair[1]

        # Sort candidates
        candidates = []
        for pair in sim_lists_no_csls:
            for sim_pairs in sim_lists_no_csls[pair]:
                candidates.append([pair[1], index_to_id[sim_pairs[0]], abs(sim_pairs[1])])
        candidates.sort(key=lambda x: x[2], reverse=True)

        #################################
        # Fair Unique Mapping Clustering
        #################################

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", sample, conf_id, "RDGCN")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", sample, conf_id, "RDGCN")

        g = Grouping(kg1, kg2, dataset, "RDGCN")
        g.group_based_on_component(kg1, kg2)

        # print("pr1: ")
        # print(len(g.pr_1))
        # print("pr2: ")
        # print(len(g.pr_2))
        # print("n_pr1: ")
        # print(len(g.n_pr_1))
        # print("n_pr2: ")
        # print(len(g.n_pr_2))

        initial_pairs = [(cand[0], cand[1], int(cand[2]), g.pair_is_protected(cand[:2], which_entity))
                     for cand in candidates]
        
        clusters = fumc.run(initial_pairs, k_results)

        #############################
        # Evaluation
        #############################

        accuracy = eval.get_accuracy_KG(clusters, candidates)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity)
        print("SPD:", spd)

        eod = f_eval.get_eod_KG(clusters, candidates, g, which_entity)
        print("EOD:", eod)
        print()

    else:
        print("Printing only the statistics")
        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", sample, conf_id, "RDGCN")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", sample, conf_id, "RDGCN")

        g = Grouping(kg1, kg2, dataset, "RDGCN")
        g.group_based_on_component(kg1, kg2)
        # print("pr1: ")
        # print(len(g.pr_1))
        # print("pr2: ")
        # print(len(g.pr_2))
        # print("n_pr1: ")
        # print(len(g.n_pr_1))
        # print("n_pr2: ")
        # print(len(g.n_pr_2))

if __name__ == "__main__":
    
    
    k_results = 20
    # dataset = "D_W_15K_V1"
    which_entity = 0
    
    # for ORIGINAL datasets 
    # main("D_W_15K_V1", k_results, which_entity, "original", "original", "RDGCN")
    # exit()

    sample = "sampled"

    method_sim_list = ["RDGCN", "MultiKE"]
    for m in method_sim_list:
        print("Method: " + m)
        for d in ["D_Y_15K_V1", "D_W_15K_V1"]:
            dataset = d
            print("\tDataset: " + dataset)
            for c in [1, 3]:
                conf_id = "conf_" + str(c) + "_only_p_RDGCN"
                print("\t\t" + conf_id)
                main(dataset, k_results, which_entity, conf_id, sample, m)