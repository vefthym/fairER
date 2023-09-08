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
import subprocess
from matching.bert_int.basic_bert_unit import Param_updated
from matching.bert_int.interaction_model import Param_updated_inter

from flask import Flask, render_template, request, json
# from web.run import app

"""
    Run fairER for RREA
"""

def run(conf, dest_path, dataset, file_name, method):
    """
    Purpose: Run RREA
    """

    if method == "BERT_INT":
        if conf == "original":
            dataset_path = "resources/Datasets/" + dataset + "_BERT_INT/"
        else:
            dataset_path = "resources/Datasets/sampled/" + dataset + "_BERT_INT/" + conf + "/"

        with open("matching/bert_int/basic_bert_unit/Param.py", "r") as fp:
            with open("matching/bert_int/basic_bert_unit/Param_updated.py", "w") as fp2:
                for line in fp:
                    if 'DATASET = ""' in line:
                        line = 'DATASET = "' + dataset + '"\n'
                    if 'DATA_PATH = ROOT + "/"' in line:
                        line = 'DATA_PATH = ROOT + "' + '/' + dataset_path + '"\n'
                    if 'MODEL_SAVE_PATH = ROOT + "/"' in line:
                        line = 'MODEL_SAVE_PATH = ROOT + "' + '/' + "resources/exp_results/" + dataset + "_BERT_INT/" + conf + '/"\n'                    
                    if 'TOPK = 0' in line:
                        if conf == "original":
                            line = 'TOPK = 500'
                        else:
                            line = 'TOPK = ' + "50" + "\n" 

                    if 'NEAREST_SAMPLE_NUM = 0' in line:
                        if conf == "original":
                            line = 'NEAREST_SAMPLE_NUM = 500'
                        else:
                            line = 'NEAREST_SAMPLE_NUM = 50' + "\n"

                    if 'CANDIDATE_GENERATOR_BATCH_SIZE = 0' in line:
                        if conf == "original":
                            line = 'CANDIDATE_GENERATOR_BATCH_SIZE = 500'
                        else:
                            line = 'CANDIDATE_GENERATOR_BATCH_SIZE = 50' + "\n"

                    fp2.write(line)


        with open("matching/bert_int/interaction_model/Param.py", "r") as fp:
            with open("matching/bert_int/interaction_model/Param_updated_inter.py", "w") as fp2:
                for line in fp:
                    if 'DATASET = ""' in line:
                        line = 'DATASET = "' + dataset + '"\n'
                    if 'INTERACTION_MODEL_SAVE_PATH = "' in line:
                        line = 'INTERACTION_MODEL_SAVE_PATH = ROOT + "' + '/' + "resources/exp_results/" + dataset + "_BERT_INT/" + conf + "/" + "interaction_model_save" + '"\n'
                    if 'BASIC_BERT_UNIT_MODEL_SAVE_PATH = ""' in line:
                        line = 'BASIC_BERT_UNIT_MODEL_SAVE_PATH = ' + 'ROOT + "' + '/' + "resources/exp_results/" + dataset + "_BERT_INT/" + conf + '/"\n'
                    if 'DATA_PATH = ""' in line:
                        line = 'DATA_PATH = ROOT + "' + '/' + dataset_path + '"\n'

                    fp2.write(line)


        if not os.path.exists(Param_updated.MODEL_SAVE_PATH):
            os.makedirs(Param_updated.MODEL_SAVE_PATH)
        if not os.path.exists(Param_updated.MODEL_SAVE_PATH + "model_epoch_1.p") or not os.path.exists(Param_updated.MODEL_SAVE_PATH + "other_data.pkl"):
            # app.debug = False
            os.system("conda run -n demo_bert_int python matching/bert_int/basic_bert_unit/main.py")

        if not os.path.exists(Param_updated_inter.INTERACTION_MODEL_SAVE_PATH.replace("/interaction_model_save", "")):
            os.makedirs(Param_updated_inter.INTERACTION_MODEL_SAVE_PATH.replace("/interaction_model_save", ""))

        # we need debug mode off    
        if not os.path.exists(Param_updated_inter.INTERACTION_MODEL_SAVE_PATH):
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/clean_attribute_data.py")
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/get_entity_embedding.py")
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/get_attributeValue_embedding.py")
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/get_neighView_and_desView_interaction_feature.py")
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/get_attributeView_interaction_feature.py")
            os.system("conda run -n demo_bert_int python matching/bert_int/interaction_model/interaction_model.py")
    else:
        if conf == "original":
            dataset_path = "resources/Datasets/" + dataset + "_RREA/"
        else:
            dataset_path = "resources/Datasets/sampled/" + dataset + "_RREA/" + conf + "/"
        os.system("python matching/RREA/RREA.py " + dataset_path + " " + dest_path + " " + file_name)

def main(dataset, conf, which_entity, k=20, method="RREA"):

    dest_path = "resources/exp_results/" + dataset + "_" + method + "/" + conf + "/"
    file_name =  dataset + "_sim_lists.pickle"

    isExist = os.path.exists(dest_path + file_name)
    """
        If file exists, load similarity lists and perform unique mapping clustering
        otherwise, run RREA to produce similarity lists and re-run for unique mapping clustering
    """
    print(method)
    if not isExist:
        # app.debug = False
        run(conf, dest_path, dataset, file_name, method)
        isExist = True
        # app.debug = True
    

    if isExist:

        with (open(dest_path + file_name, "rb")) as fp:
            sim_lists_no_csls = pickle.load(fp)

        if method == "RREA":
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

            if conf == "original":
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RREA")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RREA")
            else:
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RREA")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RREA")

            g = Grouping(kg1, kg2, dataset, "RREA")
            g.group_based_on_component(kg1, kg2)
            
            # preds = []
            # for pair in sim_lists_no_csls:
            #     preds.append([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]], abs(sim_lists_no_csls[pair][0][1]),
            #                    g.pair_is_protected([pair[1], index_to_id[sim_lists_no_csls[pair][0][0]]], which_entity)])

            initial_pairs = [(int(cand[0]), int(cand[1]), float(cand[2]), g.pair_is_protected(cand[:2], which_entity))
                        for cand in candidates]
            
            k_results = len(sim_lists_no_csls)
            clusters = fumc.run(initial_pairs, k_results)
            
            ids_to_uris_1 = KnowledgeGraph.get_ids_to_uris(dataset, "1")
            ids_to_uris_2 = KnowledgeGraph.get_ids_to_uris(dataset, "2")

            cluster_mapped = []
            i=0
            for cl in clusters:
                cluster_mapped.append([ids_to_uris_1[cl[0]], ids_to_uris_2[kg1.get_seed_pairs()[cl[1]]], cl[2], cl[3]])
                i+=1

            initial_pairs_mapped = []
            for pair in initial_pairs:
                pair = [*pair,]
                if pair in clusters:
                    initial_pairs_mapped.append([ids_to_uris_1[pair[0]], ids_to_uris_2[kg1.get_seed_pairs()[pair[1]]], pair[2], pair[3], True])
                else:
                    initial_pairs_mapped.append([ids_to_uris_1[pair[0]], ids_to_uris_2[kg1.get_seed_pairs()[pair[1]]], pair[2], pair[3], False])
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
        elif method == "BERT_INT":

            if conf == "original":
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "BERT_INT")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "BERT_INT")
            else:
                kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "BERT_INT")
                kg2 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "BERT_INT")

            candidates = []
            for e in sim_lists_no_csls:
                for sim_pairs in sim_lists_no_csls[e]:
                    candidates.append([e, kg1.get_seed_pairs(reverse=True)[sim_pairs[0]], abs(sim_pairs[1])])
           

            g = Grouping(kg1, kg2, dataset, "BERT_INT")
            g.group_based_on_component(kg1, kg2)

            initial_pairs = [(int(cand[0]), int(cand[1]), float(cand[2]), g.pair_is_protected(cand[:2], which_entity))
                        for cand in candidates]
            
            k_results = len(sim_lists_no_csls)
            clusters = fumc.run(initial_pairs, k_results)
            
            ids_to_uris_1 = kg1.get_ids_to_uris_bert_int(dataset, "1")
            ids_to_uris_2 = kg2.get_ids_to_uris_bert_int(dataset, "2")

            if conf == "original":
                kg1_RREA = KnowledgeGraph("1", dataset, "multi_directed", "original", "original", "RREA")
                kg2_RREA = KnowledgeGraph("2", dataset, "multi_directed", "original", "original", "RREA")
            else:
                kg1_RREA = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf, "RREA")
                kg2_RREA = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf, "RREA")

            ids_to_uris_1_RREA = KnowledgeGraph.get_ids_to_uris(dataset, "1")
            ids_to_uris_2_RREA = KnowledgeGraph.get_ids_to_uris(dataset, "2")

            cluster_mapped = []
            i=0 
            for cl in clusters:
                cluster_mapped.append([ids_to_uris_1[cl[0]], ids_to_uris_2[kg1.get_seed_pairs()[cl[1]]], cl[2], cl[3]])
                i+=1

            initial_pairs_mapped = []
            for pair in initial_pairs:
                pair = [*pair,]
                if pair in clusters:
                    initial_pairs_mapped.append([ids_to_uris_1[pair[0]], ids_to_uris_2[kg1.get_seed_pairs()[pair[1]]], pair[2], pair[3], True])
                else:
                    initial_pairs_mapped.append([ids_to_uris_1[pair[0]], ids_to_uris_2[kg1.get_seed_pairs()[pair[1]]], pair[2], pair[3], False])
            

            accuracy = eval.get_accuracy_KG(clusters, candidates, k)
            print("accuracy:", accuracy)
            
            spd = f_eval.get_spd_KG(clusters, candidates, g, which_entity, k)
            print("SPD:", spd)

            eod = f_eval.get_eod_KG(clusters, candidates, g, which_entity, k)
            print("EOD:", eod)
            print()

            methods.eval_to_json(accuracy, spd, eod)
            methods.clusters_to_json(cluster_mapped, ["KG_1 id", "KG_2 id"], initial_pairs_mapped)
    

# if __name__ == "__main__":
    
#     k_results = 20
#     dataset = "D_W_15K_V1"
#     which_entity = 0
#     conf_id = "conf_3_only_p"
#     sample = "sampled"
#     main(dataset, k_results, which_entity, conf_id, sample)