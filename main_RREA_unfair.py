from clustering import unique_mapping_clustering as umc
import os
import pickle
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
from matching.KG.KnowledgeGraph import KnowledgeGraph
from matching.Grouping import Grouping

"""
        Run unfair method for RREA (unique mapping clustering)
"""

def run(sample, conf_id):
    """
        Run RREA
    """

    os.chdir("matching/RREA/")
    os.system("python RREA.py " + sample + " " + conf_id + " -1")




def main(dataset, k_results, which_entity, conf_id, sample):
    dest_path = "matching/RREA/exp_results/test_experiments/" + dataset + "/" + conf_id + "/" + dataset + "_sim_lists_NO_CSLS_sampled.pickle"
    isExist = os.path.exists(dest_path)
    
    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, run RREA to produce similarity lists and re-run for unique mapping clustering
    """
    if isExist:
        with (open(dest_path, "rb")) as fp:
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

        results = umc.run(candidates, k_results)
        
        clusters = results

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", conf_id, "RREA")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", conf_id, "RREA")

        g = Grouping(kg1, kg2, dataset, "RREA")
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
        #     if r[0] == r[1]:
        #         tp += 1
        # print(tp/700 * 100)

    # elif not isExist:
    #     run(sample, conf_id)
        

if __name__ == '__main__':

    k_results = 20
    dataset = "D_Y_15K_V1"
    which_entity = 0
    conf_id = "conf_1_only_p"
    sample = "sampled"
    main(dataset, k_results, which_entity, conf_id, sample)