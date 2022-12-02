from matching.KG.KnowledgeGraph import KnowledgeGraph
import networkx as nx
import pandas as pd

class Statistics:

    def __init__():
        pass

    @staticmethod
    def basic_statistics(kg):

        # for node in kg.graph.nodes():
        #     print("node" + str(node) + " degree: " + str(Statistics.get_ent_attr_degree(node, kg.attr_df)))
        # exit()
        
        nodes = kg.graph.number_of_nodes()
        edges = kg.graph.number_of_edges()
        attributes = len(kg.attr_df)
        
        rel_dens = edges / nodes
        attr_dens = attributes / nodes
        ents_birth = set(kg.attr_df["e1"][kg.attr_df["attr"] == 'http://dbpedia.org/ontology/birthName'])
        ents_label = set(kg.attr_df["e1"][kg.attr_df["attr"] == 'skos:prefLabel'])

        return nodes, rel_dens, attr_dens, len(ents_birth.union(ents_label))

    @staticmethod
    def get_comps_dict(comp):
        comps_dict = {}
        for c in comp:
            if len(c) not in comps_dict:
                comps_dict[len(c)] = list()
            comps_dict[len(c)].append(c)
        return comps_dict
    
    @staticmethod
    def get_ent_attr_degree(ent, df):
        
        if ent in df['e1'].value_counts().to_dict().keys():
            return df['e1'].value_counts().to_dict()[ent]
        else:
            return 0

    @staticmethod
    def generate_attr_degree_dict(df):
        
        return df['e1'].value_counts().to_dict()

    @staticmethod
    def attrs_per_comp(kg):

        comps = nx.connected_components(kg.graph)
        comps_dict = Statistics.get_comps_dict(list(comps))

        attr_degree_comp = {}
        for comp in comps_dict:

            if comp not in attr_degree_comp:
                attr_degree_comp[comp] = []

            for sub in comps_dict[comp]:
                temp = 0

                for ent in sub:
                    temp += Statistics.get_ent_attr_degree(ent, kg.attr_df)
                attr_degree_comp[comp].append(( sub, (temp / len(sub)) ))

        return attr_degree_comp

    @staticmethod
    def weakly_conn_comps(num_kg, method, dataset, prefix, thres):
        print("wcc_" + "KG" + num_kg)
        wcc_dict = dict()
        kg_mdi = KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "original", "original", method)
        # wcc_dict["original"] = nx.number_weakly_connected_components(kg_mdi.graph)/kg_mdi.graph.number_of_nodes()

        for i in [-3]:
            conf_id = "conf_" + str(i) + "_or_thres_" + str(thres) + "_" + method
            kg_mdi = KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "sampled", conf_id, method)
            wcc_dict[conf_id] = nx.number_weakly_connected_components(kg_mdi.graph)/kg_mdi.graph.number_of_nodes()
        
        wcc_df = pd.DataFrame.from_dict(wcc_dict, orient='index').T

        print(wcc_df.T)
        print("---------------------------------")

    @staticmethod
    def avg_rels_per_entity(num_kg, method, dataset, prefix, thres):
        print("deg_" + "KG" + num_kg)
        kg =  KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "original", "original", method).graph
        nodes_deg = kg.degree()

        counter = 0
        for pair in nodes_deg:
            counter += pair[1]
        avg_node_deg = counter / kg.number_of_nodes()

        b_dict = dict()
        # b_dict["original"] = avg_node_deg

        for i in [-3]:
            conf_id = "conf_" + str(i) + "_or_thres_" + str(thres) + "_" + method
            kg = KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "sampled", conf_id, method).graph
            nodes_deg = kg.degree()

            counter = 0
            for pair in nodes_deg:
                counter += pair[1]
            avg_node_deg = counter / kg.number_of_nodes()
            b_dict[conf_id] = avg_node_deg
        
        df = pd.DataFrame.from_dict(b_dict, orient='index').T

        df = df.T
        print(df)
        print("---------------------------------")

    @staticmethod
    def max_comp(num_kg, method, dataset, prefix, thres):
        print("maxCS_" + "KG" + num_kg)
        kg =  KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "original", "original", method)
        comps = sorted(nx.weakly_connected_components(kg.graph), key=len)

        max_len = len(comps[-1])/kg.graph.number_of_nodes()

        b_dict = dict()
        # b_dict["original"] = max_len

        for i in [-3]:
            conf_id = "conf_" + str(i) + "_or_thres_" + str(thres) + "_" + method
            
            kg = KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "sampled", conf_id, method)
            comps = sorted(nx.weakly_connected_components(kg.graph), key=len)
            max_len = len(comps[-1])/kg.graph.number_of_nodes()
            b_dict[conf_id] = max_len
        
        df = pd.DataFrame.from_dict(b_dict, orient='index').T
        df = df.T
        print(df)
        print("---------------------------------")



    @staticmethod
    def avg_attrs_per_entity(num_kg, method, dataset, prefix, thres):
        print("attr_deg_" + "KG" + num_kg)
        kg =  KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "original", "original", method)
        
        counter = 0
        for n in kg.graph.nodes():

            if str(n) in kg.attr_dict:
                counter += len(kg.attr_dict[str(n)])

        avg_attr_node_deg = counter / kg.graph.number_of_nodes()

        b_dict = dict()
        b_dict["original"] = avg_attr_node_deg

        for i in [-3]:
            conf_id = "conf_" + str(i) + "_or_thres_" + str(thres) + "_" + method
            kg = KnowledgeGraph(num_kg, dataset, prefix, "multi_directed", "sampled", conf_id, method)
            
            counter = 0
            for n in kg.graph.nodes():
                
                if str(n) in kg.attr_dict:
                    counter += len(kg.attr_dict[str(n)])

            avg_attr_node_deg = counter / kg.graph.number_of_nodes()
            b_dict[conf_id] = avg_attr_node_deg
        
        df = pd.DataFrame.from_dict(b_dict, orient='index').T

        df = df.T
        print(df)
        print("---------------------------------")