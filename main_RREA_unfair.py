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

def run():
    """
        Run RREA
    """

    os.chdir("matching/RREA/")
    os.system("python RREA.py sampled conf_1_only_p -1")




def main(dataset):
    dest_path = "matching/RREA/exp_results/test_experiments/D_Y_15K_V1/conf_1_only_p/D_Y_15K_V1_sim_lists_NO_CSLS_sampled.pickle"
    isExist = os.path.exists(dest_path)
    
    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, run RREA to produce similarity lists and re-run for unique mapping clustering
    """
    if isExist:
        with (open("matching/RREA/exp_results/test_experiments/D_Y_15K_V1/conf_1_only_p/D_Y_15K_V1_sim_lists_NO_CSLS_sampled.pickle", "rb")) as fp:
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
        
        results = umc.run(candidates)
        
        clusters = results

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", "conf_1_only_p")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", "conf_1_only_p")

        g = Grouping(kg1, kg2, dataset)
        g.group_based_on_component(kg1, kg2)

        #############################
        # Evaluation
        #############################

        accuracy = eval.get_accuracy_KG(clusters, candidates)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd_KG(clusters, candidates, g)
        print("SPD:", spd)

        eod = f_eval.get_eod(clusters, candidates, g)
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
        tp = 0
        for r in results:
            if r[0] == r[1]:
                tp += 1
        print(tp/700 * 100)

    elif not isExist:
        run()
        

if __name__ == '__main__':

    dataset = "D_Y_15K_V1"
    main(dataset)