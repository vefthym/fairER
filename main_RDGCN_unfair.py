from clustering import unique_mapping_clustering as umc
import os
import pickle
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
from matching.KG.KnowledgeGraph import KnowledgeGraph
from matching.Grouping import Grouping

"""
        Run unfair method for OpenEA method (unique mapping clustering)
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

        # Unique mapping clustering
        candidates = []
        for pair in sim_lists_no_csls:
            for sim_pairs in sim_lists_no_csls[pair]:
                candidates.append([pair[1], index_to_id[sim_pairs[0]], abs(sim_pairs[1])])
        candidates.sort(key=lambda x: x[2], reverse=True)

        results = umc.run(candidates, k_results)
        
        clusters = results

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", conf_id ,"RDGCN")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", conf_id,"RDGCN")

        g = Grouping(kg1, kg2, dataset, "RDGCN")
        g.group_based_on_component(kg1, kg2)

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

         #############################
        # End
        #############################

        # Check if 1-to-1
        left = []
        right = []
        for r in results:
            left.append(r[0])
            right.append(r[1])
        assert(len(left) == len(right))

        # measure tp
        # tp = 0
        # for r in results:
        #     print(r)
        #     if r[0] == r[1]:
        #         tp += 1
        # print(tp/len(results) * 100)
        

if __name__ == '__main__':

    k_results = 20
    dataset = "D_Y_15K_V1"
    which_entity = 0
    conf_id = "conf_3_only_p_RDGCN"
    sample = "sampled"
    method_sim_list = "RDGCN"

    main(dataset, k_results, which_entity, conf_id, sample, method_sim_list)