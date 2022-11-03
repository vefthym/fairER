import networkx as nx

class Statistics:

    def __init__():
        pass

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
        return df.loc[df['e1'] == ent].count()[0]

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

        print(attr_degree_comp)