from turtle import color
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import networkx as nx
import pandas as pd
import pickle
import os
import statistics as st

class ResultsStatistics:

    @staticmethod
    def plot_hits(dataset, measure, sample, conf_id):

        names_dict_CSLS = {
            '(iso, iso)': '(iso, iso)\nCSLS',
            '(iso, hubs)': '(iso, hubs)\nCSLS',
            '(hubs, iso)': '(hubs, iso)\nCSLS',
            '(hubs, hubs)': '(hubs, hubs)\nCSLS',
        }

        names_dict_no_CSLS = {
            '(iso, iso)': '(iso, iso)\nno CSLS',
            '(iso, hubs)': '(iso, hubs)\nno CSLS',
            '(hubs, iso)': '(hubs, iso)\nno CSLS',
            '(hubs, hubs)': '(hubs, hubs)\nno CSLS'
        }

        prefix = "hits_hubs_iso"
        with (open("../exp_results/" + measure + "/" + dataset + "/" + conf_id + "/" + dataset + "_hits_hubs_iso_" + "WITH_CSLS" + "_" + sample + ".pickle", "rb")) as fp:
            hits = pickle.load(fp)

        hits_df_CSLS = pd.DataFrame(data=hits, index = ["hits@1", "hits@5", "hits@10"]).rename(columns=names_dict_CSLS).T

        with (open("../exp_results/" + measure + "/" + dataset + "/" + conf_id + "/" + dataset + "_hits_hubs_iso_" + "NO_CSLS" + "_" + sample + ".pickle", "rb")) as fp:
            hits = pickle.load(fp)

        hits_df_NO_CSLS = pd.DataFrame(data=hits, index = ["hits@1", "hits@5", "hits@10"]).rename(columns=names_dict_no_CSLS).T
        
        concatenated_df = pd.concat([hits_df_NO_CSLS, hits_df_CSLS])
        lst = ["(iso, hubs)\nno CSLS", "(iso, hubs)\nCSLS", "(hubs, iso)\nno CSLS", "(hubs, iso)\nCSLS", "(iso, iso)\nno CSLS", "(iso, iso)\nCSLS", "(hubs, hubs)\nno CSLS", "(hubs, hubs)\nCSLS"]
        concatenated_df = concatenated_df.reindex(lst)

        ax = concatenated_df.plot.bar(rot=0, figsize = (20, 15))
        ax.tick_params(axis='both', labelsize=18)
        ax.legend(fontsize=15)
        fig = ax.get_figure()
        ax.set_ylim(0, 100)
        ax.set_xlabel(dataset + " " + measure + " " + sample + " " + conf_id, fontsize=25)
        ax.xaxis.set_label_position('top') 
        fig.savefig("results_plots/" + dataset + "/" + conf_id + "/" + "concatenated_plot" + prefix + dataset + "_" + sample + "_" + conf_id)

    def tp_per_comp(kg, dataset, prefix, sim_lists, mode, sample, conf_id):

        if sample == "original":
            test_links = {}
            with open("../RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

            test_links_rev = {}
            with open("../RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links_rev[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])
        elif sample == "sampled":
            test_links = {}
            with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

            test_links_rev = {}
            with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links_rev[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

        conn_dict = {}

        graph = kg.graph

        sorted_comp = sorted(nx.connected_components(graph), key=len)

        for c in sorted_comp:
            if len(c) not in conn_dict:
                conn_dict[len(c)] = list()
            for i in c:
                conn_dict[len(c)].append(i)

        if kg.id == "1":
            tp_per_group = {}
            for d in conn_dict:
                tp = 0
                counter = 0
                for e in conn_dict[d]:
                    if e in test_links:
                        if test_links[e] == sim_lists[e][0][0]:
                            tp += 1
                        counter += 1
                if counter == 0 and e in conn_dict[1]:
                    tp_per_group[d] = 0
                else:
                    tp_per_group[d] = (tp/counter) * 100
        elif kg.id == "2":
            tp_per_group = {}
            for d in conn_dict:
                tp = 0
                counter = 0
                for e in conn_dict[d]:
                    if e in test_links_rev:
                        if e  == sim_lists[test_links_rev[e]][0][0]:
                            tp += 1
                        counter += 1
                if counter == 0 and e in conn_dict[1]:
                    tp_per_group[d] = 0
                else:
                    tp_per_group[d] = (tp/counter) * 100

        hits_df = pd.DataFrame(data=tp_per_group, index = ["TP " + mode + " (%)"])
        return hits_df

    def combine_tp_per_comp_size(kg, dataset, prefix, sim_lists_no_csls, sim_lists_with_csls, sample, conf_id):

        kg_with_csls = ResultsStatistics.tp_per_comp(kg, dataset, prefix, sim_lists_with_csls, "WITH_CSLS", sample, conf_id)
        kg_no_csls = ResultsStatistics.tp_per_comp(kg, dataset, prefix, sim_lists_no_csls, "NO_CSLS", sample, conf_id)
        concatenated_df = pd.concat([kg_no_csls, kg_with_csls]).T
        ax = concatenated_df.plot.bar(rot=0, figsize = (9,9))
        fig = ax.get_figure()
        ax.set_title(dataset + "_kg" + kg.id + "_" + sample + "_" + conf_id)
        ax.set_xlabel("size of each component")
        ax.set_ylabel("TP (%)")
        ax.set_ylim(0,100)
        fig.savefig("results_plots/" + dataset + "/" + conf_id + "/tp_per_component_" + dataset + "kg" + kg.id + "_" + sample + conf_id + ".png")
        fig.clf()
        return concatenated_df

    def probability_density_function(dataset, kg, concatenated_df):
        ax = concatenated_df.plot(kind = 'density', cumulative=True)
        ax.set_xlim(0,150)
        ax.set_ylim(0,0.03)
        ax.set_title(dataset + "_kg" + kg.id)
        ax.set_xlabel("size of each component")
        fig = ax.get_figure()
        fig.savefig("plots/density_function_" + dataset + "kg" + kg.id + ".png")
        return fig

    def cummulative_distribution_function(dataset, kg, concatenated_df):
        print(concatenated_df)
        count, bins_count = np.histogram(concatenated_df["TP NO_CSLS (%)"], bins=10)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        plt.plot(bins_count[1:], cdf, label="CDF NO CSLS")
        count2, bins_count2 = np.histogram(concatenated_df["TP WITH_CSLS (%)"], bins=10)
        pdf2 = count2 / sum(count2)
        cdf2 = np.cumsum(pdf2)
        plt.plot(bins_count2[1:], cdf2, label="CDF WITH CSLS")
        plt.title(dataset + "_kg" + str(kg.id))
        plt.xlabel("size of each component")
        plt.ylabel("CDF")
        plt.legend()
        plt.savefig("plots/cummulative_function_" + dataset + "kg" + kg.id + ".png")
        return plt


    @staticmethod
    def scores_matrix(dataset, measure, sample, mode):

        df_list = []

        with (open("../exp_results/" + measure + "/" + dataset + "/original/" + dataset + "_hits_hubs_iso_" + mode + "_" + "original" + ".pickle", "rb")) as fp:
                    hits = pickle.load(fp)

        hits_df_NO_CSLS = pd.DataFrame(data=hits, index = ["hits@1", "hits@5", "hits@10"]).rename(columns={
            '(iso, iso)': 'original_' + '(iso, iso) ',
            '(iso, hubs)': 'original_' + ' (iso, hubs) ',
            '(hubs, iso)': 'original_' + ' (hubs, iso) ',
            '(hubs, hubs)': 'original_' + ' (hubs, hubs) '
        }).T

        df_list.append(hits_df_NO_CSLS)
        hits.clear()

        for i in range(1, 9):
            if i != 7 and i != 9:
                with (open("../exp_results/" + measure + "/" + dataset + "/conf_" + str(i) + "/" + dataset + "_hits_hubs_iso_" + mode + "_" + sample + ".pickle", "rb")) as fp:
                    hits = pickle.load(fp)

                hits_df_NO_CSLS = pd.DataFrame(data=hits, index = ["hits@1", "hits@5", "hits@10"]).rename(columns={
                '(iso, iso)': 'conf_' + str(i) + '(iso, iso) ',
                '(iso, hubs)': 'conf_' + str(i) + ' (iso, hubs) ',
                '(hubs, iso)': 'conf_' + str(i) + ' (hubs, iso) ',
                '(hubs, hubs)': 'conf_' + str(i) + ' (hubs, hubs) '
                }).T

                df_list.append(hits_df_NO_CSLS)
                hits.clear()
                    
        concatenated_df = pd.concat(df_list)
        print(concatenated_df)
        concatenated_df.to_csv("results_matrices/" + dataset + "/score_matrix_" + mode + ".tsv", sep="\t", float_format='%.2f')


    @staticmethod
    def overall_per_conf(dataset, measure, sample, csls_mode):
        hits = dict()
        # with open("../exp_results/" + measure + "/RDGCN/" + dataset + "/" + "original" + "/" + dataset + "_acc_" + csls_mode + "_" + "original" + ".pickle", "rb") as fp:
        #     h = pickle.load(fp)
        #     # hits["original"] = h["acc"]
        hits["original"] = [94.15, 97.18, 97.73]
        for i in range(0,5):
            conf_id = "conf" + "_" + str(i) + "_only_p_RDGCN"
            hits[conf_id] = [0, 0, 0]
            dest_path = "../exp_results/" + measure + "/RDGCN/" + dataset + "/" + conf_id + "/" + dataset + "_acc_" + csls_mode + "_" + sample + ".pickle"
            isExist = os.path.exists(dest_path)
            if isExist: 
                with open(dest_path, "rb") as fp:
                    h = pickle.load(fp)
                    hits[conf_id] = h["acc"]

        hits_df = pd.DataFrame(hits, index = ["hits@1", "hits@5", "hits@10"]).rename(columns={
            'conf_0_only_p': '0 ',
            'conf_1_only_p': '0.15 ',
            'conf_2_only_p': '0.50 ',
            'conf_3_only_p': '0.85 ',
            'conf_4_only_p': '1 '
        }).T

        ax = hits_df.plot.bar(rot=0, figsize = (9,9))
        fig = ax.get_figure()
        ax.set_title(dataset + "_" + "with_jump_probability_p")
        ax.set_xlabel("p")
        ax.set_ylim(0,100)
        fig.savefig("results_matrices/" + dataset + "/" + "hits_per_conf" + ".png")

    def norm_tp_per_comp(kg1_mdi, kg, kg2_mdi, kg2, dataset, prefix, sim_lists, mode, sample, conf_id):

        if sample == "original":
            test_links = {}
            with open("../RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

            test_links_rev = {}
            with open("../RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links_rev[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])
        elif sample == "sampled":
            test_links = {}
            with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

            test_links_rev = {}
            with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/test_links") as fp:
                for line in fp:
                    test_links_rev[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

        conn_dict = {}

        graph = kg.graph

        sorted_comp = sorted(nx.connected_components(graph), key=len)

        for c in sorted_comp:
            if len(c) not in conn_dict:
                conn_dict[len(c)] = list()
            conn_dict[len(c)].append(c)

        conn_dict2 = {}

        tp_per_comp = {}
        for d in conn_dict:
            tp_per_comp[d] = list()
            for lst in conn_dict[d]:
                tp = 0
                for e in lst:
                    if e in test_links:
                        for pair in sim_lists:
                            if pair[1] == e:
                                rank_index = np.where(np.array(sim_lists[pair]) == pair[0])[0][0]
                                if rank_index == 0:
                                    tp += 1
                                    if d == 6:
                                        print(e)
                tp_per_comp[d].append(tp/d)


        # gr = dict()
        # for i in range(4):
        #     gr[i] = list()
        #     for j in range(4):
        #         if i != j:
        #             graph_edit_dist = nx.graph_edit_distance(kg1_mdi.graph.subgraph(conn_dict[6][i]), kg1_mdi.graph.subgraph(conn_dict[6][j]))
        #             gr[i].append(graph_edit_dist)
        #             print(graph_edit_dist)
        #     gr[i] = max(gr[i])
        # print(gr)

        final_sum = dict()
        for comp in tp_per_comp:
            final_sum[comp] = sum(tp_per_comp[comp]) / len(tp_per_comp[comp])
            # final_sum[comp] = st.median(tp_per_comp[comp])

        hits_df = pd.DataFrame(data=final_sum, index = ["TP " + mode + " (%)"])
        return hits_df

    def plot_normalized_tp_per_comp_size(kg1_mdi, kg, kg2_mdi, kg2, dataset, prefix, sim_lists_no_csls, sample, conf_id):
        kg_no_csls = ResultsStatistics.norm_tp_per_comp(kg1_mdi, kg, kg2_mdi, kg2, dataset, prefix, sim_lists_no_csls, "NO_CSLS", sample, conf_id)
        df = pd.DataFrame(kg_no_csls).T
        ax = df.plot.bar(rot=0, figsize = (9,9))
        fig = ax.get_figure()
        ax.set_title(dataset + "_kg" + kg.id + "_" + sample + "_" + conf_id)
        ax.set_xlabel("size of each component")
        ax.set_ylabel("TP (%)")
        ax.set_ylim(0,1)
        fig.savefig("results_plots/" + dataset + "/" + conf_id + "/tp_per_component_" + dataset + "kg" + kg.id + "_" + sample + conf_id + ".png")
        fig.clf()

    def entropy_diversity(kg1_mdi, kg1, kg2_mdi, kg2, dataset, prefix, sim_lists_no_csls, sample, conf_id):

        index_to_ent = dict()
        for pair in sim_lists_no_csls:
            index_to_ent[pair[0]] = pair[1]

        sim_lists = dict()
        for pair in sim_lists_no_csls:
            sim_lists[pair[1]] = list()
            for e in sim_lists_no_csls[pair]:
                sim_lists[pair[1]].append(index_to_ent[e])
                if len(sim_lists[pair[1]]) == 10:
                    break

        conn_dict = dict()
        for c in nx.connected_components(kg1.graph):
            if len(c) not in conn_dict:
                conn_dict[len(c)] = list()
            for i in c:
                conn_dict[len(c)].append(i)
        
        k = 10
        
        rec = dict()
        for node in sim_lists:
            rec[node] = 0
            for s in sim_lists:
                if node in sim_lists[s][0:k]:
                    rec[node] += 1
        # for r in rec:
        #     print(r)
        #     print(rec[r])
        #     print("-------------------")
        # exit()

        # c1 = 0
        # c2 = 0
        # for node in sim_lists:
        #     if node in conn_dict[2] or node in conn_dict[1] or node in conn_dict[3] or node in conn_dict[4] or node in conn_dict[5]:
        #         c1 += 1
        #     else:
        #         c2 += 2

        # c1 = len(sim_lists)
        # c2 = len(sim_lists)

        # ed_small = 0
        # ed_big = 0
        
        # for node in sim_lists:
        #     if node in conn_dict[2] or node in conn_dict[3] or node in conn_dict[4]:
        #         if rec[node] != 0:
        #             ed_small += (rec[node]/(k * c1)) * np.log((rec[node]/(k * c1)))
        #         # ed += (rec[node]/(k*700)) * (rec[node]/(k*700))
        #     else:
        #         if rec[node] != 0:
        #             ed_big += (rec[node]/(k * c2)) * np.log((rec[node]/(k * c2)))

        # print("small")
        # print(ed_small*(-1))

        # print("big")
        # print(ed_big*(-1))


          
        c = len(sim_lists)

        ed = 0
        
        for node in sim_lists:
            if rec[node] != 0:
                ed += (rec[node]/(k * c)) * np.log((rec[node]/(k * c)))


        print("ed")
        print(ed*(-1))