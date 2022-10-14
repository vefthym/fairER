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
    Run fairER for RREA
"""

def run():
    """
    Purpose: Run RREA
    """

    os.chdir("matching/RREA/")
    os.system("python RREA.py sampled conf_1_only_p -1")



def main(k_results, dataset):
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

        # Sort candidates
        candidates = []
        for pair in sim_lists_no_csls:
            for sim_pairs in sim_lists_no_csls[pair]:
                candidates.append([pair[1], index_to_id[sim_pairs[0]], abs(sim_pairs[1])])
        candidates.sort(key=lambda x: x[2], reverse=True)

        #################################
        # Fair Unique Mapping Clustering
        #################################

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", "conf_1_only_p")
        kg2 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", "conf_1_only_p")

        g = Grouping(kg1, kg2, dataset)
        g.group_based_on_component(kg1, kg2)

        initial_pairs = [(int(cand[0]), int(cand[1]), int(cand[2]), g.pair_is_protected(cand[:2], 0))
                     for cand in candidates]

        clusters = fumc.run(initial_pairs, 200)

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

    elif not isExist:
        run()

    

if __name__ == "__main__":
    
    k_results = 20
    dataset = "D_Y_15K_V1"
    
    main(k_results, dataset)
