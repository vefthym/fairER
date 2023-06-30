from clustering import unique_mapping_clustering as umc
import os
import pickle
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
from matching.KG.KnowledgeGraph import KnowledgeGraph
from matching.Grouping import Grouping
import web.library.methods as methods
import json

def run(conf, dest_path, dataset, file_name, method):
    """
    Purpose: Run OpenEA
    """
    if conf == "original":
        with open("matching/OpenEA/run/args/original_" + method.lower() + "_args_15K.json") as fp:
            j = json.load(fp)
        dataset_path = "resources/Datasets/" + dataset + "/"
        j["training_data"] = dataset_path
        j["output"] = dest_path + file_name
        j["dataset"] = dataset
        with open("matching/OpenEA/run/args/original_" + method.lower() + "_args_15K.json", 'w') as outfile:
            json.dump(j, outfile)
        os.system("python matching/OpenEA/run/main_from_args.py matching/OpenEA/run/args/original_" + method.lower() + "_args_15K.json")
    else:
        with open("matching/OpenEA/run/args/sampled_" + method.lower() + "_args_15K.json") as fp:
            j = json.load(fp)
        dataset_path = "resources/Datasets/sampled/" + dataset + "_RDGCN/" + conf + "/"
        j["training_data"] = dataset_path
        j["output"] = dest_path + file_name
        j["dataset"] = dataset
        j["conf_id"] = conf
        with open("matching/OpenEA/run/args/sampled_" + method.lower() + "_args_15K.json", 'w') as outfile:
            json.dump(j, outfile)
        os.system("python matching/OpenEA/run/main_from_args.py matching/OpenEA/run/args/sampled_" + method.lower() + "_args_15K.json")
    
"""
        Run unfair method for OpenEA method (unique mapping clustering)
"""

def main(dataset, conf, which_entity, method_sim_list, k=20):
    
    dest_path = "resources/exp_results/" + dataset + "_" + method_sim_list + "/" + conf + "/"
    file_name =  dataset + "_sim_lists.pickle"
    
    isExist = os.path.exists(dest_path + file_name)

    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, manually run OpenEA method to produce similarity lists and re-run for unique mapping clustering
    """

    if not isExist:
        run(conf, dest_path, dataset, file_name, method_sim_list)
        isExist = True

    if isExist:
        with (open(dest_path + file_name, "rb")) as fp:
            sim_lists_no_csls = pickle.load(fp)

        # Corrects the wrong entity-metric pairs of similarity lists of RDGCN
        # This happens because of manhattan metric used for this method
        if method_sim_list == "RDGCN" or method_sim_list == "MultiKE":
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

        if conf == "original":
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RDGCN")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RDGCN")
        else:
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RDGCN")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RDGCN")

        g = Grouping(kg1, kg2, dataset, "RDGCN")
        g.group_based_on_component(kg1, kg2)

        initial_pairs = [(cand[0], cand[1], int(cand[2]), g.pair_is_protected(cand[:2], which_entity))
                     for cand in candidates]

        k_results = len(sim_lists_no_csls)
        results = umc.run(initial_pairs, k_results)
        
        clusters = results

        if conf == "original":
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RDGCN")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RDGCN")
        else:
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RDGCN")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RDGCN")

        g = Grouping(kg1, kg2, dataset, "RDGCN")
        g.group_based_on_component(kg1, kg2)

        preds = []
        for pair in sim_lists_no_csls:
            preds.append([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]], abs(sim_lists_no_csls[pair][0][1]),
                           g.pair_is_protected([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]]], which_entity)])

        cluster_mapped = []
        for cl in clusters:
            print(cl)
            # cluster_mapped.append([cl[0], kg1.get_seed_pairs()[cl[1]], cl[2], cl[3]])

        #############################
        # Evaluation
        #############################

        accuracy = eval.get_accuracy_KG(clusters, candidates, k)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity, k)
        print("SPD:", spd)

        eod = f_eval.get_eod_KG(cluster_mapped, candidates, g, which_entity, k)
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

        methods.eval_to_json(accuracy, spd, eod)
        methods.clusters_to_json(clusters, ["KG 1", "KG 2"])
        methods.preds_to_json("", preds)

        # measure tp
        # tp = 0
        # for r in results:
        #     print(r)
        #     if r[0] == r[1]:
        #         tp += 1
        # print(tp/len(results) * 100)
        

# if __name__ == '__main__':

#     k_results = 20
#     dataset = "D_W_15K_V1"
#     which_entity = 0
#     conf_id = "conf_3_only_p_RDGCN"
#     sample = "sampled"
#     method_sim_list = "MultiKE"

#     main(dataset, k_results, which_entity, conf_id, sample, method_sim_list)