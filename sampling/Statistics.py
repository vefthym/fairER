import networkx as nx

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
        sum_ent_names_atrs = kg.attr_df.loc[kg.attr_df["attr"] == 'skos:prefLabel'].count()[0] + kg.attr_df.loc[kg.attr_df["attr"] == 'http://dbpedia.org/ontology/birthName'].count()[0]

        return rel_dens, attr_dens, sum_ent_names_atrs

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