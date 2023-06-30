from clustering import unique_mapping_clustering as umc
import os
import pickle
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
from matching.KG.KnowledgeGraph import KnowledgeGraph
from matching.Grouping import Grouping
import web.library.methods as methods

"""
        Run unfair method for RREA (unique mapping clustering)
"""

def run(conf, dest_path, dataset, file_name):
    """
    Purpose: Run RREA
    """

    if conf == "original":
        dataset_path = "resources/Datasets/" + dataset + "_RREA/"
    else:
        dataset_path = "resources/Datasets/sampled/" + dataset + "_RREA/" + conf + "/"
    # exit()
    os.system("python matching/RREA/RREA.py " + dataset_path + " " + dest_path + " " + file_name)




def main(dataset, conf, which_entity, k=20):

    dest_path = "resources/exp_results/" + dataset + "_RREA/" + conf + "/"
    file_name =  dataset + "_sim_lists.pickle"
    
    isExist = os.path.exists(dest_path + file_name)

    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, run RREA to produce similarity lists and re-run for unique mapping clustering
    """

    if not isExist:
        run(conf, dest_path, dataset, file_name)
        isExist = True

    if isExist:
        with (open(dest_path + file_name, "rb")) as fp:
            sim_lists_no_csls = pickle.load(fp)

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
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RREA")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RREA")
        else:
            kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RREA")
            kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RREA")

        g = Grouping(kg1, kg2, dataset, "RREA")
        g.group_based_on_component(kg1, kg2)

        initial_pairs = [(int(cand[0]), int(cand[1]), float(cand[2]), g.pair_is_protected(cand[:2], which_entity))
                     for cand in candidates]

        k_results = len(sim_lists_no_csls)
        results = umc.run(initial_pairs, k_results)
        
        clusters = results

        preds = []
        for pair in sim_lists_no_csls:
            preds.append([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]], abs(sim_lists_no_csls[pair][0][1]),
                           g.pair_is_protected([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]]], which_entity)])

        #############################
        # Evaluation
        #############################

        cluster_mapped = []
        for cl in clusters:
            cluster_mapped.append([cl[0], kg1.get_seed_pairs()[cl[1]], cl[2], cl[3]])

        accuracy = eval.get_accuracy_KG(clusters, candidates, k)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity, k)
        print("SPD:", spd)

        eod = f_eval.get_eod_KG(clusters, candidates, g, which_entity, k)
        print("EOD:", eod)

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
        methods.clusters_to_json(cluster_mapped, ["KG 1", "KG 2"])
        methods.preds_to_json("", preds)

        # measure tp
        # tp = 0
        # for r in results:
        #     if r[0] == r[1]:
        #         tp += 1
        # print(tp/700 * 100)

    # elif not isExist:
    #     run(sample, conf_id)
        

# if __name__ == '__main__':

#     k_results = 20
#     dataset = "D_W_15K_V1"
#     which_entity = 0
#     conf_id = "conf_3_only_p"
#     sample = "sampled"
#     main(dataset, k_results, which_entity, conf_id, sample)