import os
from matching.KG.KnowledgeGraph import KnowledgeGraph
from sampling.ResultsStatistics import ResultsStatistics
import pickle

def start_result_analysis(dataset, prefix, measure, sample, conf_id):

    print("-----START RESULTS ANALYSIS-----")

    print(dataset + " " + sample + " " + conf_id)
    if "conf_" in conf_id:
        dest_path = "results_plots/" + dataset + "/" + conf_id + "/"
        isExist = os.path.exists(dest_path)
        if isExist:
            if input("are you sure you want to override " + dest_path + " ? (y/n) ") != "y":
                exit()
        if not isExist:
            os.makedirs(dest_path)

        method = "RREA"

        kg1 = KnowledgeGraph("1", dataset, prefix, "multi_undirected", sample, conf_id, method)
        kg2 = KnowledgeGraph("2", dataset, prefix, "multi_undirected", sample, conf_id, method)
        kg1_mdi = KnowledgeGraph("1", dataset, prefix, "multi_directed", sample, conf_id, method)
        kg2_mdi = KnowledgeGraph("2", dataset, prefix, "multi_directed", sample, conf_id, method)
        
        # with (open("../exp_results/" + measure + "/" + dataset + "/" + conf_id + "/" + dataset + "_sim_lists_" + "WITH_CSLS" + "_" + sample + ".pickle", "rb")) as fp:
        #             sim_lists_with_csls = pickle.load(fp)

        # TO DELETE !!!
        sim_lists_with_csls = []
        with (open("../matching/RREA/exp_results/" + measure + "/" + dataset + "/" + conf_id + "/" + dataset + "_sim_lists_" + "NO_CSLS" + "_" + sample + ".pickle", "rb")) as fp:
                    sim_lists_no_csls = pickle.load(fp)

        # concatenated_df = ResultsStatistics.combine_tp_per_comp_size(kg1, dataset, prefix, sim_lists_no_csls, sim_lists_with_csls, sample, conf_id)
        ResultsStatistics.plot_normalized_tp_per_comp_size(kg1_mdi, kg1, kg2_mdi, kg2, dataset, prefix, sim_lists_no_csls, sample, conf_id)
        # concatenated_df2 = ResultsStatistics.combine_tp_per_comp_size(kg2, dataset, prefix, sim_lists_no_csls, sim_lists_with_csls, sample, conf_id)
        # ResultsStatistics.plot_hits(dataset, measure, sample, conf_id)
        # ResultsStatistics.entropy_diversity(kg1_mdi, kg1, kg2_mdi, kg2, dataset, prefix, sim_lists_no_csls, sample, conf_id)
    else:
        dest_path = "results_matrices/" + dataset + "/"
        isExist = os.path.exists(dest_path)
        if isExist:
            if input("are you sure you want to override " + dest_path + " ? (y/n) ") != "y":
                exit()
        if not isExist:
            os.makedirs(dest_path)
        # ResultsStatistics.scores_matrix(dataset, measure, sample, "NO_CSLS")
        # ResultsStatistics.scores_matrix(dataset, measure, sample, "WITH_CSLS")
        # ResultsStatistics.overall_per_conf(dataset, measure, sample, "NO_CSLS")