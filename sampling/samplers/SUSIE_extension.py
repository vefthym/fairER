# import Graph_Sampling
import networkx as nx
import numpy as np
import random
import itertools
import pickle
from copy import copy
from sampling.Statistics import Statistics

class SUSIE_extension:

    attr_thres = None

    def __init__(self, p, attr_thres, sampling_size):

        self.p = p
        self.attr_thres = attr_thres
        self.sampling_size = sampling_size

    @staticmethod
    def get_attr_degree(ent, attr_degree_dict):

        if ent in attr_degree_dict.keys():
            return attr_degree_dict[ent]
        else:
            return 0

    def filter_neighbors(self, cand_neighbors, kg1_mun, kg2_mun, kg_num):

        attr_degree_dict1 = Statistics.generate_attr_degree_dict(kg1_mun.attr_df)
        attr_degree_dict2 = Statistics.generate_attr_degree_dict(kg2_mun.attr_df)

        temp = set()
        for node in cand_neighbors:
            if kg_num == "1":
                node_attr_degree1 = SUSIE_extension.get_attr_degree(node, attr_degree_dict1)
                node_attr_degree2 = SUSIE_extension.get_attr_degree(kg1_mun.get_seed_pairs()[node], attr_degree_dict2)
            elif kg_num == "2":
                node_attr_degree1 = SUSIE_extension.get_attr_degree(kg1_mun.get_seed_pairs(reverse = True)[node], attr_degree_dict1)
                node_attr_degree2 = SUSIE_extension.get_attr_degree(node, attr_degree_dict2)

            if node_attr_degree1 <= self.attr_thres and node_attr_degree2 <= self.attr_thres:
                temp.add(node)

        if len(list(temp)) == 0:
            return cand_neighbors

        return list(temp)



    def filter_nodes(self, comp, kg1_mun, kg2_mun, kg_num):
        attr_degree_dict1 = Statistics.generate_attr_degree_dict(kg1_mun.attr_df)
        attr_degree_dict2 = Statistics.generate_attr_degree_dict(kg2_mun.attr_df)
        filtered = []
        for c in comp:
            temp_set = set()
            for node in c:
                if kg_num == "1":
                    node_attr_degree1 = SUSIE_extension.get_attr_degree(node, attr_degree_dict1)
                    node_attr_degree2 = SUSIE_extension.get_attr_degree(kg1_mun.get_seed_pairs()[node], attr_degree_dict2)
                elif kg_num == "2":
                    node_attr_degree1 = SUSIE_extension.get_attr_degree(kg1_mun.get_seed_pairs(reverse = True)[node], attr_degree_dict1)
                    node_attr_degree2 = SUSIE_extension.get_attr_degree(node, attr_degree_dict2)

                if node_attr_degree1 <= self.attr_thres and node_attr_degree2 <= self.attr_thres:
                    temp_set.add(node)
            filtered.append(temp_set)
                
        return filtered

    @staticmethod
    def get_curr_node(comps_dict, disconnected):
        
        if len(disconnected) != 0:
            curr_node = np.random.choice(disconnected)
            disconnected.remove(curr_node)
        else:
            keys = list(comps_dict.keys())
            curr_key = np.random.choice(keys)
            curr_node = np.random.choice(list(comps_dict[curr_key]))

        return curr_node, disconnected

    @staticmethod
    def my_remove_node(chosen, comps_dict):
        for key, item in comps_dict.items():
            if item is chosen:
                del comps_dict[key]
                break
        return comps_dict

    @staticmethod
    def get_comps_dict(comp):
        comps_dict = {}
        for c in comp:
            if len(c) > 0:
                if len(c) not in comps_dict:
                    comps_dict[len(c)] = set()
                for i in c:
                    comps_dict[len(c)].add(i)
        return comps_dict

    def RJ_only_p(self, kg1_mdi, kg2_mdi, kg1_mun, kg2_mun):

        complete_graph1 = kg1_mun.graph
        complete_graph2 = kg2_mun.graph

        attr_degree_dict1 = Statistics.generate_attr_degree_dict(kg1_mun.attr_df)
        attr_degree_dict2 = Statistics.generate_attr_degree_dict(kg2_mun.attr_df)

        for n, data in complete_graph1.nodes(data=True):
            complete_graph1.nodes[n]['id'] = n

        for n, data in complete_graph2.nodes(data=True):
            complete_graph2.nodes[n]['id'] = n

        comp1 = nx.connected_components(kg1_mun.graph)
        comp2 = nx.connected_components(kg2_mun.graph)

        # comps1 = self.filter_nodes(comp1, kg1_mun, kg2_mun, "1")
        # comps2 = self.filter_nodes(comp2, kg1_mun, kg2_mun, "2")
       
        # comps_dict1 = SUSIE_extension.get_comps_dict(list(comps1))
        # comps_dict2 = SUSIE_extension.get_comps_dict(list(comps2))
        # file_to_write = open("comps_dict1" + ".pickle", "wb")
        # pickle.dump(comps_dict1, file_to_write)
        # file_to_write = open("comps_dict2" + ".pickle", "wb")
        # pickle.dump(comps_dict2, file_to_write)

        file = open("comps_dict1.pickle",'rb')
        comps_dict1 = pickle.load(file)
        file = open("comps_dict2.pickle",'rb')
        comps_dict2 = pickle.load(file)

        seed_pairs = kg1_mun.get_seed_pairs()
        rev_seed_pairs = kg2_mun.get_seed_pairs(reverse=True)

        sampled_graph = nx.MultiDiGraph()
        sampled_graph2 = nx.MultiDiGraph()
        sampled_filtered_kg = nx.MultiDiGraph()
        sampled_filtered_kg2 = nx.MultiDiGraph()
        disconnected1 = []
        disconnected2 = []
        isKG1 = True
        curr_node, disconnected1 = SUSIE_extension.get_curr_node(comps_dict1, [])

        iteration1 = 0
        iteration2 = 0
        nodes_before1 = 0
        nodes_before2 = 0

        while sampled_filtered_kg.number_of_nodes() < self.sampling_size and sampled_filtered_kg2.number_of_nodes() < self.sampling_size:
            print(sampled_filtered_kg.number_of_nodes())
            if isKG1:
                curr_kg, curr_sampled_kg, curr_second_sampled_kg, curr_node, curr_node_match = complete_graph1, sampled_graph, sampled_graph2, curr_node, seed_pairs[curr_node]
            else:
                curr_kg, curr_sampled_kg, curr_second_sampled_kg, curr_node, curr_node_match = complete_graph2, sampled_graph2, sampled_graph, curr_node, rev_seed_pairs[curr_node]
            cand_neighbors = [curr_kg.nodes[n]['id'] for n in curr_kg.neighbors(curr_node)]

            if isKG1:
                cand_neighbors = self.filter_neighbors(cand_neighbors, kg1_mun, kg2_mun, "1")
            elif not isKG1:
                cand_neighbors = self.filter_neighbors(cand_neighbors, kg1_mun, kg2_mun, "2")

            index_of_edge = random.randint(0, len(cand_neighbors) - 1)
            chosen_node = cand_neighbors[index_of_edge]

            if isKG1:
                matched_chosen_node = seed_pairs[chosen_node]
            else:
                matched_chosen_node = rev_seed_pairs[chosen_node]

            curr_sampled_kg.add_node(curr_node)
            curr_second_sampled_kg.add_node(curr_node_match)
            curr_sampled_kg.add_node(chosen_node)
            curr_second_sampled_kg.add_node(matched_chosen_node)

            if isKG1:
                comps_dict1 = SUSIE_extension.my_remove_node(curr_node, comps_dict1)
                comps_dict1 = SUSIE_extension.my_remove_node(chosen_node, comps_dict1)
            else:
                comps_dict2 = SUSIE_extension.my_remove_node(curr_node, comps_dict2)
                comps_dict2 = SUSIE_extension.my_remove_node(chosen_node, comps_dict2)
            
            choice = np.random.choice(['jump', 'random_walk'], 1, p=[self.p, 1 - self.p])
            if isKG1:
                if iteration1 % 100 == 0:
                    if sampled_filtered_kg.number_of_nodes() - nodes_before1 < 2:
                        choice = 'jump'
                        print('jump')
                    nodes_before1 = sampled_filtered_kg.number_of_nodes()
            else:
                if iteration2 % 100 == 0:
                    if sampled_filtered_kg2.number_of_nodes() - nodes_before2 < 2:
                        choice = 'jump'
                        print('jump2')
                    nodes_before2 = sampled_filtered_kg2.number_of_nodes()

            if choice == 'random_walk':
                curr_node = chosen_node
            elif choice == 'jump':
                isKG1 = not isKG1
                if isKG1:
                    curr_node, disconnected1 = SUSIE_extension.get_curr_node(comps_dict1, disconnected1)
                else:
                    curr_node, disconnected2 = SUSIE_extension.get_curr_node(comps_dict2, disconnected2)

            # keeps parallel edges
            filtered_kg1 = kg1_mdi.df.loc[kg1_mdi.df['e1'].isin(sampled_graph.nodes()) & kg1_mdi.df['e2'].isin(sampled_graph.nodes())]
            filtered_kg2 = kg2_mdi.df.loc[kg2_mdi.df['e1'].isin(sampled_graph2.nodes()) & kg2_mdi.df['e2'].isin(sampled_graph2.nodes())]
            sampled_filtered_kg = nx.from_pandas_edgelist(filtered_kg1, source='e1', target='e2', edge_attr=True, create_using=nx.MultiDiGraph())
            sampled_filtered_kg2 = nx.from_pandas_edgelist(filtered_kg2, source='e1', target='e2', edge_attr=True, create_using=nx.MultiDiGraph())
            disconnected1 = [x for x in sampled_graph.nodes() if x not in sampled_filtered_kg.nodes()]
            disconnected2 = [x for x in sampled_graph2.nodes() if x not in sampled_filtered_kg2.nodes()]

            iteration1 += 1
            iteration2 += 1

        sampled_df = nx.to_pandas_edgelist(sampled_filtered_kg)
        sampled_df2 = nx.to_pandas_edgelist(sampled_filtered_kg2)
        node_pairs = list(zip(sampled_df["source"], sampled_df["target"]))
        node_pairs2 = list(zip(sampled_df2["source"], sampled_df2["target"]))

        ents = set()
        for n in node_pairs:
            ents.add(n[0])
            ents.add(n[1])

        ents2 = set()
        for n in node_pairs2:
            ents2.add(n[0])
            ents2.add(n[1])

        print(len(ents))
        print(len(ents2))

        if len(ents) < len(ents2):
            print("den einai idio")
            for e in ents2.copy():
                if rev_seed_pairs[e] in disconnected1:
                    ents2.remove(e)
        elif len(ents) > len(ents2):
            print("den einai idio2")
            for e in ents.copy():
                if seed_pairs[e] in disconnected2:
                    ents.remove(e)
        
        filtered_kg1 = kg1_mdi.df.loc[kg1_mdi.df['e1'].isin(ents) & kg1_mdi.df['e2'].isin(ents)]
        filtered_kg2 = kg2_mdi.df.loc[kg2_mdi.df['e1'].isin(ents2) & kg2_mdi.df['e2'].isin(ents2)]
        sampled_filtered_kg = nx.from_pandas_edgelist(filtered_kg1, source='e1', target='e2', edge_attr=True, create_using=nx.MultiDiGraph())
        sampled_filtered_kg2 = nx.from_pandas_edgelist(filtered_kg2, source='e1', target='e2', edge_attr=True, create_using=nx.MultiDiGraph())

        filtered_attr_kg1 = kg1_mdi.attr_df.loc[kg1_mdi.attr_df['e1'].isin(ents)]
        filtered_attr_kg2 = kg2_mdi.attr_df.loc[kg2_mdi.attr_df['e1'].isin(ents2)]

        return node_pairs, node_pairs2, ents, ents2, sampled_filtered_kg, sampled_filtered_kg2, filtered_kg1, filtered_kg2, filtered_attr_kg1, filtered_attr_kg2