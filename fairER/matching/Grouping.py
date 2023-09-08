from typing import Mapping
import networkx as nx
from matching.KG.KnowledgeGraph import KnowledgeGraph
import pickle
import os
import re
class Grouping:

    def __init__(self, kg1, kg2, dataset, method):
        self.kg1 = kg1
        self.kg2 = kg2
        self.pr_1 = set()
        self.n_pr_1 = set()
        self.pr_2 = set()
        self.n_pr_2 = set()
        self.dataset = dataset
        self.comps_1 = set()
        self.comps_2 = set()
        self.mappings = dict()
        self.method = method

    def get_comps(self, kg):
        """
        Purpose: Return th connected components of the given kg
        """

        conn_dict = {}
        for c in nx.weakly_connected_components(kg.graph):
            if len(c) not in conn_dict:
                conn_dict[len(c)] = list()
            for i in c:
                conn_dict[len(c)].append(i)
        
        return conn_dict
        
    # end def

    def is_protected(self, e, kg_num):
        """
        Purpose: Determines if an entity is protected or non-protected
        """

        pickle_path = os.path.join(os.getcwd(), 'web','data', 'pickle_data', 'protected_conditions.pkl')
        if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
            with open(pickle_path, 'rb') as pkl_file:
                data = pickle.load(pkl_file)
        
        key = list(data.keys())[0]
        condition = data[key]
        range_limit = re.findall(r'\d+', condition)[1]

        if kg_num == "1":
            comps = self.comps_1
        elif kg_num == "2":
            comps = self.comps_2

        for key in range(1, int(range_limit)):
            if key in comps.keys():
                if e in comps[key]:
                    return True
        return False

    # end def

    def pair_is_protected(self, pair, which_entity):
        """
        Purpose: Determines if a pair of entities is protected or non-protected based on a condition
        """
        ent = pair[which_entity]
        mapped_ent = self.mappings[ent]

        pickle_path = os.path.join(os.getcwd(), 'web','data', 'pickle_data', 'protected_conditions.pkl')
        if os.path.exists(pickle_path) and os.path.getsize(pickle_path) > 0:
            with open(pickle_path, 'rb') as pkl_file:
                data = pickle.load(pkl_file)
        
        key = list(data.keys())[0]
        condition = data[key]
        if "or" in condition:
            operator = "or"
        elif "and" in condition:
            operator = "and"

        if operator == "or":
            if ent in self.pr_1 or mapped_ent in self.pr_2:
                return True
            else:
                return False
        elif operator == "and":
            if ent in self.pr_1 and mapped_ent in self.pr_2:
                return True
            else:
                return False
        
        
        # if str(which_entity + 1) == "1":
        #     if ent in self.pr_1:
        #         return True
        #     elif ent in self.n_pr_1:
        #         return False
        # elif str(which_entity + 1) == "2":
        #     if self.mappings[ent] in self.pr_2:
        #         return True
        #     elif self.mappings[ent] in self.n_pr_2:
        #         return False
            
        return None

    # end def
    
    def group_based_on_component(self, kg1, kg2):
        """
        Purpose: Group entities of the two kgs based on the connected component the belong
        """

        if self.method == "RREA":
            self.mappings = kg1.get_seed_pairs()
        elif self.method == "RDGCN":
            self.mappings = kg1.get_seed_pairs_RDGCN()
        elif self.method == "BERT_INT":
            self.mappings = kg1.get_seed_pairs_BERT_INT()

        self.comps_1 = self.get_comps(kg1)
        self.comps_2 = self.get_comps(kg2)
        for e1 in self.mappings:
            e2 = self.mappings[e1]

            if self.is_protected(e1, "1"):
                self.pr_1.add(e1)
            elif not self.is_protected(e1, "1"):
                self.n_pr_1.add(e1)

            if self.is_protected(e2, "2"):
                self.pr_2.add(e2)
            elif not self.is_protected(e2, "2"):
                self.n_pr_2.add(e2)

    # end def