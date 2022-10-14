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

    def __init__(self, id, dataset, prefix, kg_type, sample, conf_id):

      self.id = id
      self.dataset = dataset
      self.prefix = prefix
      self.sample = sample
      self.conf_id = conf_id
      if sample == "original":
        path =  "matching/RREA/RREA_process_datasets/" + dataset + prefix + "_RREA/rel_triples_" + id
      elif sample == "sampled":
        path =  "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id + "/rel_triples_" + id
      kg = pd.read_csv(path,  sep='\t', names=["e1", "r", "e2"])
      
      self.df = kg
      self.df["(e1,e2)"] = list(zip(self.df.e1, self.df.e2))
      if kg_type == "directed":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.DiGraph())
      elif kg_type == "multi_directed":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.MultiDiGraph())
      elif kg_type == "multi_undirected":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"], create_using=nx.MultiGraph())
      elif kg_type == "undirected":
        self.graph = nx.from_pandas_edgelist(kg, "e1", "e2", ["r"])

    def get_seed_pairs(self, reverse=False):
      if self.sample == "original":
        path = "matching/RREA/RREA_process_datasets/" + self.dataset + self.prefix + "_RREA/721_5fold/2/"
      elif self.sample == "sampled":
        path = "matching/RREA/sampled/" + self.dataset + "_sampled/" + self.conf_id + "/721_5fold/2/"

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