import networkx as nx
import pandas as pd

class KnowledgeGraph:

    graph = None
    dataset = ""
    prefix = ""
    df = None
    id = 0
    sample = ""
    conf_id = ""
    attr_df = ""
    attr_dict = ""
    num_rel_type = 0

    def __init__(self, id, dataset, kg_type, sample, conf_id, method):

      self.id = id
      self.dataset = dataset
      self.prefix = ""
      self.sample = sample
      self.conf_id = conf_id
      self.attr_df = ""
      self.method = method
      self.attr_dict = ""
      self.num_rel_type = 0
      
      KnowledgeGraph.load_rel_graph(self, kg_type, method)
      if method == "RREA" or method == "RDGCN":
        KnowledgeGraph.load_attr_graph(self, method)
     

    def get_seed_pairs(self, reverse=False):

      if self.method == "RDGCN":
        return KnowledgeGraph.get_seed_pairs_RDGCN(self, reverse = reverse)

      if self.method == "BERT_INT":
        return KnowledgeGraph.get_seed_pairs_BERT_INT(self, reverse = reverse)

      if self.sample == "original":
        path = "resources/Datasets/" + self.dataset + self.prefix + "_RREA/721_5fold/2/"
      elif self.sample == "sampled":
        path = "resources/Datasets/sampled/" + self.dataset + "_" + self.method + "/" + self.conf_id + "/721_5fold/2/"

      if reverse == False:
        pairs = {}
        path_test = path + "test_links"
        with open(path_test) as fp:
          for line in fp:
            pairs[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

        path_train = path + "train_links"
        with open(path_train) as fp:
          for line in fp:
            pairs[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

        path_valid = path + "valid_links"
        with open(path_valid) as fp:
          for line in fp:
            pairs[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())
      elif reverse == True:
          pairs = {}
          path_test = path +"test_links"
          with open(path_test) as fp:
            for line in fp:
              pairs[int(line.split("\t")[1].rstrip())] = int(int(line.split("\t")[0]))

          path_train = path + "train_links"
          with open(path_train) as fp:
            for line in fp:
              pairs[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

          path_valid = path + "valid_links"
          with open(path_valid) as fp:
            for line in fp:
              pairs[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

      return pairs


    def get_seed_pairs_RDGCN(self, reverse=False):
      if self.sample == "original":
        path = "resources/Datasets/" + self.dataset + self.prefix + "/721_5fold/2/"
      elif self.sample == "sampled":
        path = "resources/Datasets/sampled/" + self.dataset + "_" + self.method + "/" + self.conf_id + "/721_5fold/2/"

      if reverse == False:
        pairs = {}
        path_test = path + "test_links"
        with open(path_test) as fp:
          for line in fp:
            pairs[line.split("\t")[0]] = line.split("\t")[1].rstrip()

        path_train = path + "train_links"
        with open(path_train) as fp:
          for line in fp:
            pairs[line.split("\t")[0]] = line.split("\t")[1].rstrip()

        path_valid = path + "valid_links"
        with open(path_valid) as fp:
          for line in fp:
            pairs[line.split("\t")[0]] = line.split("\t")[1].rstrip()
      elif reverse == True:
          pairs = {}
          path_test = path +"test_links"
          with open(path_test) as fp:
            for line in fp:
              pairs[line.split("\t")[1].rstrip()] = line.split("\t")[0]

          path_train = path + "train_links"
          with open(path_train) as fp:
            for line in fp:
              pairs[line.split("\t")[1].rstrip()] = line.split("\t")[0]

          path_valid = path + "valid_links"
          with open(path_valid) as fp:
            for line in fp:
              pairs[line.split("\t")[1].rstrip()] = line.split("\t")[0]

      return pairs

    def get_seed_pairs_BERT_INT(self, reverse=False):
      if self.sample == "original":
        path = "resources/Datasets/" + self.dataset + self.prefix + "/721_5fold/2/"
      elif self.sample == "sampled":
        path = "resources/Datasets/sampled/" + self.dataset + "_" + self.method + "/" + self.conf_id + "/"

      if reverse == False:
        pairs = {}
        path_test = path + "ref_pairs"
        with open(path_test) as fp:
          for line in fp:
            pairs[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

        path_train = path + "sup_pairs"
        with open(path_train) as fp:
          for line in fp:
            pairs[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

      elif reverse == True:
          pairs = {}
          path_test = path +"ref_pairs"
          with open(path_test) as fp:
            for line in fp:
              pairs[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

          path_train = path + "sup_pairs"
          with open(path_train) as fp:
            for line in fp:
              pairs[int(line.split("\t")[1].rstrip())] = int(line.split("\t")[0])

      return pairs

    @staticmethod
    def load_rel_graph(self, kg_type, method):

      if self.sample == "original":
        if method == "RREA":
          path =  "resources/Datasets/" + self.dataset + self.prefix + "_RREA/rel_triples_" + self.id
        elif method == "RDGCN":
          path =  "resources/Datasets/" + self.dataset + self.prefix + "/rel_triples_" + self.id
        elif method == "BERT_INT":
          path =  "resources/Datasets/" + self.dataset + self.prefix + "_BERT_INT/rel_triples_" + self.id
      elif self.sample == "sampled":
        if method == "BERT_INT":
          path =  "resources/Datasets/sampled/" + self.dataset + "_" + method + "/" + self.conf_id + "/triples_" + self.id
        else:
          path =  "resources/Datasets/sampled/" + self.dataset + "_" + method + "/" + self.conf_id + "/rel_triples_" + self.id

      kg = pd.read_csv(path,  sep='\t', names=["e1", "r", "e2"])
      self.df = kg

      self.num_rel_type = len(kg["r"].unique())

      # print("Loaded relation types:")
      # print("\t" + str(len(pd.unique(self.df["r"]))))
      
      self.df["(e1,e2)"] = list(zip(self.df.e1, self.df.e2))
      if kg_type == "directed":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.DiGraph())
      elif kg_type == "multi_directed":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.MultiDiGraph())
      elif kg_type == "multi_undirected":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.MultiGraph())
      elif kg_type == "undirected":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"])

    @staticmethod
    def load_attr_graph(self, method):

      if self.sample == "original":
        if method == "RREA":
          path =  "resources/Datasets/" + self.dataset + self.prefix + "_RREA/attr_triples_" + self.id
        elif method == "RDGCN":
          path =  "resources/Datasets/" + self.dataset + self.prefix + "/attr_triples_" + self.id
      elif self.sample == "sampled":
        path =  "resources/Datasets/sampled/" + self.dataset + "_" + method + "/" + self.conf_id + "/attr_triples_" + self.id

      kg = pd.read_csv(path,  sep='\t', names=["e1", "attr", "val"], warn_bad_lines=True, error_bad_lines=False)
      self.attr_df = kg

      attr_dict = {}
      with open(path, "r") as fp:
        for line in fp:
          ent = line.split("\t")[0]
          attr = line.split("\t")[1]

          if ent not in attr_dict.keys():
            attr_dict[ent] = list()

          attr_dict[ent].append(attr)

      self.attr_dict = attr_dict

      # print("Loaded attribute types:")
      # print("\t" + str(len(pd.unique(self.attr_df["attr"]))))

    @staticmethod
    def get_ids_to_uris(dataset, num):
      RREA_process_RREA = "resources/Datasets/" + dataset + "_RREA"
      ids_to_uris = {}
      with open(RREA_process_RREA + "/ent_ids_" + num) as fp:
          for line in fp:
            ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()
      return ids_to_uris

    def get_ids_to_uris_bert_int(self, dataset, num):
      if self.sample == "original":
          path =  "resources/Datasets/" + dataset + self.prefix + "_BERT_INT/ent_ids_" + num
          ids_to_uris = {}
          with open(path) as fp:
              for line in fp:
                ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()
          return ids_to_uris
      elif self.sample == "sampled":
          path =  "resources/Datasets/sampled/" + dataset + "_" + self.method + "/" + self.conf_id + "/ent_ids_" + num
          
          RREA_process_RREA = "resources/Datasets/" + dataset + "_RREA"
          ids_to_uris_RREA = {}
          with open(RREA_process_RREA + "/ent_ids_" + num) as fp:
              for line in fp:
                ids_to_uris_RREA[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()
          
          ids_to_uris = {}
          with open(path) as fp:
              for line in fp:
                ids_to_uris[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())

          ret_ids_to_uris = {}
          for k in ids_to_uris:
            ret_ids_to_uris[k] = ids_to_uris_RREA[ids_to_uris[k]]

          return ret_ids_to_uris