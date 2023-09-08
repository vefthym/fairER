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
import json

def run(conf, dest_path, dataset, file_name, method):
    """
    Purpose: Run OpenEA
    """
    if method == "RDGCN" or method == "MultiKE":
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
    else:

        isExist = os.path.exists(os.getcwd() + '/resources/exp_results/' + dataset + "_" + method + "/" + conf + "/" + 'results/')
        if not isExist:
            os.makedirs(os.getcwd() + '/resources/exp_results/' + dataset + "_" + method + "/" + conf + "/" + 'results/')

        if conf == "original":
            os.system('python ' + os.getcwd() + '/matching/PARIS/src/run_experiment.py \
                        --method PARIS\
                        --root_dataset \"' + os.getcwd() + '/resources/Datasets\"\
                        --dataset \"' + dataset + "_RDGCN" + '\"\
                        --dataset_division 721_5fold\
                        --out_folder resources/exp_results/' + dataset + "_" + method + "/" + conf + "/" + 'results/\
                        --use_func')
        else:
            os.system('python ' + os.getcwd() + '/matching/PARIS/src/run_experiment.py \
                        --method PARIS\
                        --root_dataset \"' + os.getcwd() + '/resources/Datasets/sampled\"\
                        --dataset \"' + dataset + "_RDGCN/" + conf + '\"\
                        --dataset_division 721_5fold\
                        --out_folder ' + os.getcwd() + '/resources/exp_results/' + dataset + "_" + method + "/" + conf + "/" + 'results\
                        --use_func')

"""
        Run fairER method for OpenEA method (unique mapping clustering)
"""

def main(dataset, conf, which_entity, method_sim_list, k=20):
    
    if method_sim_list == "RDGCN" or method_sim_list == "MultiKE":
        dest_path = "resources/exp_results/" + dataset + "_" + method_sim_list + "/" + conf + "/"
        file_name =  dataset + "_sim_lists.pickle"
        isExist = os.path.exists(dest_path + file_name)
    elif method_sim_list == "PARIS":
        dest_path = os.getcwd() + "/resources/exp_results/" + dataset + "_" + method_sim_list + "/" + conf + "/results/output/"
        file_name =  "9_eqv_full.tsv"
        isExist = os.path.exists(dest_path + file_name)

    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, manually run OpenEA method to produce similarity lists and re-run for unique mapping clustering
    """ 
    if not isExist:
        run(conf, dest_path, dataset, file_name, method_sim_list)
        isExist = True

    if isExist:

        if method_sim_list == "RDGCN" or method_sim_list == "MultiKE":
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

            # Sort candidates
            candidates = []
            for pair in sim_lists_no_csls:
                for sim_pairs in sim_lists_no_csls[pair]:
                    candidates.append([pair[1], index_to_id[sim_pairs[0]], sim_pairs[1]])
            candidates.sort(key=lambda x: x[2], reverse=True)

            #################################
            # Fair Unique Mapping Clustering
            #################################


            if conf == "original":
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RDGCN")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RDGCN")
            else:
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RDGCN")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RDGCN")

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

            preds = []
            for pair in sim_lists_no_csls:
                preds.append([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]], sim_lists_no_csls[pair][0][1],
                            g.pair_is_protected([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]]], which_entity)])

            initial_pairs = [(cand[0], cand[1], cand[2], g.pair_is_protected(cand[:2], which_entity))
                        for cand in candidates]

            k_results = len(sim_lists_no_csls)
            clusters = fumc.run(initial_pairs, k_results)

            cluster_mapped = []
            for cl in clusters:
                cluster_mapped.append([cl[0], kg1.get_seed_pairs()[cl[1]], cl[2], cl[3]])

            initial_pairs_mapped = []
            for pair in initial_pairs:
                pair = [*pair,]
                if pair in clusters:
                    initial_pairs_mapped.append([pair[0], kg1.get_seed_pairs()[pair[1]], pair[2], pair[3], True])
                else:
                    initial_pairs_mapped.append([pair[0], kg1.get_seed_pairs()[pair[1]], pair[2], pair[3], False])

            #############################
            # Evaluation
            #############################

            accuracy = eval.get_accuracy_KG(clusters, candidates, k)
            print("accuracy:", accuracy)

            spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity, k)
            print("SPD:", spd)

            eod = f_eval.get_eod_KG(clusters, candidates, g, which_entity, k)
            print("EOD:", eod)
            print()

            methods.eval_to_json(accuracy, spd, eod)
            methods.clusters_to_json(cluster_mapped, ["KG_1 id", "KG_2 id"], initial_pairs_mapped)
            methods.preds_to_json("", preds)

        elif method_sim_list == "PARIS":

            if conf == "original":
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RDGCN")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RDGCN")
            else:
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RDGCN")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RDGCN")

            candidates = []
            with (open(dest_path + file_name, "r")) as fp:
                for line in fp:
                    ent1 = line.split("\t")[0].replace("dbp:resource", "http://dbpedia.org/resource")
                    ent2 = line.split("\t")[1]
                    sim_score = line.split("\t")[2].rstrip()
                    candidates.append((ent1, kg1.get_seed_pairs(reverse=True)[ent2], sim_score))
                candidates.sort(key=lambda x: x[2], reverse=True)

            g = Grouping(kg1, kg2, dataset, "RDGCN")
            g.group_based_on_component(kg1, kg2)

            initial_pairs = [(cand[0], cand[1], cand[2], g.pair_is_protected(cand[:2], which_entity))
                        for cand in candidates]

            k_results = len(candidates)
            clusters = fumc.run(initial_pairs, k_results)

            cluster_mapped = []
            for cl in clusters:
                cluster_mapped.append([cl[0], kg1.get_seed_pairs()[cl[1]], cl[2], cl[3]])

            initial_pairs_mapped = []
            for pair in initial_pairs:
                pair = [*pair,]
                if pair in clusters:
                    initial_pairs_mapped.append([pair[0], kg1.get_seed_pairs()[pair[1]], pair[2], pair[3], True])
                else:
                    initial_pairs_mapped.append([pair[0], kg1.get_seed_pairs()[pair[1]], pair[2], pair[3], False])

            #############################
            # Evaluation
            #############################

            accuracy = eval.get_accuracy_KG(clusters, candidates, k)
            print("accuracy:", accuracy)

            spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity, k)
            print("SPD:", spd)

            eod = f_eval.get_eod_KG(clusters, candidates, g, which_entity, k)
            print("EOD:", eod)
            print()

            methods.eval_to_json(accuracy, spd, eod)
            methods.clusters_to_json(cluster_mapped, ["KG_1 id", "KG_2 id"], initial_pairs_mapped)
            # methods.preds_to_json("", preds)

# if __name__ == "__main__":
    
    
    # k_results = 20
    # dataset = "D_W_15K_V1"
    # which_entity = 0
    
    # for ORIGINAL datasets 
    # main("D_W_15K_V1", k_results, which_entity, "original", "original", "RDGCN")
    # exit()

    # sample = "sampled"

    # method_sim_list = ["RDGCN", "MultiKE"]
    # for m in method_sim_list:
    #     print("Method: " + m)
    #     for d in ["D_Y_15K_V1", "D_W_15K_V1"]:
    #         dataset = d
    #         print("\tDataset: " + dataset)
    #         for c in [1, 3]:
    #             conf_id = "conf_" + str(c) + "_only_p_RDGCN"
    #             print("\t\t" + conf_id)
    #             main(dataset, k_results, which_entity, conf_id, sample, m)