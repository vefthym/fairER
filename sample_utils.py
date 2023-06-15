from sklearn.model_selection import train_test_split
import os
from rdflib import Literal
from rdflib.namespace import XSD, NamespaceManager

from matching.KG.KnowledgeGraph import KnowledgeGraph

class Utils:

    @staticmethod
    def generate_seeds_and_splittings(dataset, prefix, ents1, ents2, dest_seed_path, method):

        if method == "RREA":
            splittings = {
                "test_pairs": { "src_path": "resources/Datasets/" + dataset + "_RREA/721_5fold/2/test_links"},
                "train_pairs": { "src_path": "resources/Datasets/" + dataset + "_RREA/721_5fold/2/train_links"},
                "valid_pairs": { "src_path": "resources/Datasets/" + dataset + "_RREA/721_5fold/2/valid_links"}
            }

            seed_alignment = {}
            train_ratio = 0.20
            validation_ratio = 0.10
            test_ratio = 0.70
            X = []
            for s in splittings:
                with open(splittings[s]["src_path"]) as fp:
                    for line in fp:
                        if int(line.split("\t")[0]) in ents1 and int(line.split("\t")[1].rstrip()) in ents2:
                            seed_alignment[int(line.split("\t")[0])] = int(line.split("\t")[1].rstrip())
                            X.append(line.rstrip("\n"))
            
            x_train, x_test = train_test_split(X, test_size=1 - train_ratio)
            x_val, x_test = train_test_split(x_test, test_size=test_ratio / (test_ratio + validation_ratio))

        elif method == "RDGCN":

            splittings = {
                "test_pairs": { "src_path": "resources/Datasets/" + dataset + "/721_5fold/2/test_links"},
                "train_pairs": { "src_path": "resources/Datasets/" + dataset + "/721_5fold/2/train_links"},
                "valid_pairs": { "src_path": "resources/Datasets/" + dataset + "/721_5fold/2/valid_links"}
            }

            seed_alignment = {}
            train_ratio = 0.20
            validation_ratio = 0.10
            test_ratio = 0.70
            X = []
            for s in splittings:
                with open(splittings[s]["src_path"]) as fp:
                    for line in fp:
                        if line.split("\t")[0] in ents1 and line.split("\t")[1].rstrip() in ents2:
                            seed_alignment[line.split("\t")[0]] = line.split("\t")[1].rstrip()
                            X.append(line.rstrip("\n"))
            
            x_train, x_test = train_test_split(X, test_size=1 - train_ratio)
            x_val, x_test = train_test_split(x_test, test_size=test_ratio / (test_ratio + validation_ratio))

        

        isExist = os.path.exists(dest_seed_path)
        if not isExist:
            os.makedirs(dest_seed_path)

        with open(dest_seed_path + "ent_links", "w") as fp:
            for s in seed_alignment:
                fp.write(str(s))
                fp.write("\t")
                fp.write(str(seed_alignment[s]))
                fp.write("\n")

        with open(dest_seed_path + "train_links", "w") as fp:
            for x in x_train:
                fp.write(x)
                fp.write("\n")

        with open(dest_seed_path + "valid_links", "w") as fp:
                for x in x_val:
                    fp.write(x)
                    fp.write("\n")

        with open(dest_seed_path + "test_links", "w") as fp:
            for x in x_test:
                fp.write(x)
                fp.write("\n")


    def convert_sampling(conf_id, dataset):

        kg1 = KnowledgeGraph("1", dataset, "multi_directed", "sampled", conf_id, "RREA")

        RREA_process_RREA = "resources/Datasets/" + dataset + "_RREA"
        RREA_process_RDGCN = "resources/Datasets/" + dataset
        dest_RREA = "resources/Datasets/sampled/" + dataset + "_" + "RREA" + "/" + conf_id
        dest_RDGCN = "resources/Datasets/sampled/" + dataset + "_" + "RDGCN" + "/" + conf_id

        isExist = os.path.exists(dest_RDGCN)

        if not isExist:
            os.makedirs(dest_RDGCN)
            os.makedirs(dest_RDGCN + "/721_5fold/2/")

        nodes_1 = kg1.graph.nodes()
        ids_to_uris = {}
        with open(RREA_process_RREA + "/ent_ids_1") as fp:
            for line in fp:
                ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()

        uris_to_ids = {}
        with open(RREA_process_RREA + "/ent_ids_1") as fp:
            for line in fp:
                uris_to_ids[line.split("\t")[1].rstrip()] = line.split("\t")[0]

        rel_ids_to_uris = {}
        with open(RREA_process_RREA + "/rel_ids_1") as fp:
            for line in fp:
                rel_ids_to_uris[line.split("\t")[0]] = line.split("\t")[1].rstrip()

        nodes_1_conv = list()
        for n in nodes_1:
            nodes_1_conv.append(ids_to_uris[n])

        attr_1 = {}
        with open(RREA_process_RDGCN + "/attr_triples_1") as fp:
            with open(dest_RDGCN + "/attr_triples_1", "w") as fp2:
                for line in fp:
                    ent = line.split("\t")[0]
                    if ent in nodes_1_conv:
                        fp2.write(ent + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])

        with open(dest_RREA + "/rel_triples_1") as fp:
            with open(dest_RDGCN + "/rel_triples_1", "w") as fp2:
                for line in fp:
                    fp2.write(ids_to_uris[int(line.split("\t")[0])] + "\t" + rel_ids_to_uris[line.split("\t")[1]] + "\t" + ids_to_uris[int(line.split("\t")[2].rstrip())] + "\n")


        kg1 = KnowledgeGraph("2", dataset, "multi_directed", "sampled", conf_id, "RREA")

        nodes_1 = kg1.graph.nodes()
        with open(RREA_process_RREA + "/ent_ids_2") as fp:
            for line in fp:
                ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()

        uris_to_ids = {}
        with open(RREA_process_RREA + "/ent_ids_2") as fp:
            for line in fp:
                uris_to_ids[line.split("\t")[1].rstrip()] = line.split("\t")[0]

        nodes_1_conv = list()
        for n in nodes_1:
            nodes_1_conv.append(ids_to_uris[n])

        # rel_ids_to_uris = {}
        with open(RREA_process_RREA + "/rel_ids_2") as fp:
            for line in fp:
                rel_ids_to_uris[line.split("\t")[0]] = line.split("\t")[1].rstrip()

        attr_1 = {}
        with open(RREA_process_RDGCN + "/attr_triples_2") as fp:
            with open(dest_RDGCN + "/attr_triples_2", "w") as fp2:
                for line in fp:
                    ent = line.split("\t")[0]
                    if ent in nodes_1_conv:
                        fp2.write(ent + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])

        with open(dest_RREA + "/rel_triples_2") as fp:
            with open(dest_RDGCN + "/rel_triples_2", "w") as fp2:
                for line in fp:
                    fp2.write(ids_to_uris[int(line.split("\t")[0])] + "\t" + rel_ids_to_uris[line.split("\t")[1]] + "\t" + ids_to_uris[int(line.split("\t")[2].rstrip())] + "\n")


        with open(dest_RREA + "/721_5fold/2/ent_links") as fp:
            with open(dest_RDGCN + "/721_5fold/2/ent_links", "w") as fp2:
                for line in fp:
                    e1 = int(line.split("\t")[0])
                    e2 = int(line.split("\t")[1].rstrip())
                    fp2.write(ids_to_uris[e1])
                    fp2.write("\t")
                    fp2.write(ids_to_uris[e2])
                    fp2.write("\n")

        with open(dest_RREA + "/721_5fold/2/test_links") as fp:
            with open(dest_RDGCN + "/721_5fold/2/test_links", "w") as fp2:
                for line in fp:
                    e1 = int(line.split("\t")[0])
                    e2 = int(line.split("\t")[1].rstrip())
                    fp2.write(ids_to_uris[e1])
                    fp2.write("\t")
                    fp2.write(ids_to_uris[e2])
                    fp2.write("\n")
        
        with open(dest_RREA + "/721_5fold/2/train_links") as fp:
            with open(dest_RDGCN + "/721_5fold/2/train_links", "w") as fp2:
                for line in fp:
                    e1 = int(line.split("\t")[0])
                    e2 = int(line.split("\t")[1].rstrip())
                    fp2.write(ids_to_uris[e1])
                    fp2.write("\t")
                    fp2.write(ids_to_uris[e2])
                    fp2.write("\n")

        with open(dest_RREA + "/721_5fold/2/valid_links") as fp:
            with open(dest_RDGCN + "/721_5fold/2/valid_links", "w") as fp2:
                for line in fp:
                    e1 = int(line.split("\t")[0])
                    e2 = int(line.split("\t")[1].rstrip())
                    fp2.write(ids_to_uris[e1])
                    fp2.write("\t")
                    fp2.write(ids_to_uris[e2])
                    fp2.write("\n")


    def convert_attributes(dataset):

        for kg in ["1", "2"]:

            uris_to_ids = {}
            with open("matching/RREA/RREA_process_datasets/" + dataset + "_RREA/ent_ids_" + kg) as fp:
                for line in fp:
                    uris_to_ids[line.split("\t")[1].rstrip()] = line.split("\t")[0]

            with open("matching/RREA/RREA_process_datasets/" + dataset + "/attr_triples_" + kg) as fp:
                with open("matching/RREA/RREA_process_datasets/" + dataset + "_RREA/attr_triples_" + kg, "w") as fp2:
                    for line in fp:
                        ent = uris_to_ids[line.split("\t")[0]]
                        fp2.write(ent + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])


    def generate_rels(conf_id, dataset):

        RREA_process_RREA = "resources/Datasets/sampled/" + dataset + "_RREA/" + conf_id
        RREA_process_RDGCN = "resources/Datasets/" + dataset + "/"
        

        for num in [1, 2]:
            mapped = {}

            rel_ids = list()
            with open(RREA_process_RREA + "/rel_triples_" + str(num), "r") as fp:
                for line in fp:
                    rel_ids.append(line.split("\t")[1])

            rel_uris = list()
            with open(RREA_process_RDGCN + "/rel_triples_" + str(num), "r") as fp:
                for line in fp:
                    rel_uris.append(line.split("\t")[1])

            for i in range(len(rel_ids)):
                mapped[rel_ids[i]] = rel_uris[i]

            with open(RREA_process_RREA + "/rel_ids_" + str(num), "w") as fp:
                for rel in mapped:
                    fp.write(rel)
                    fp.write("\t")
                    fp.write(mapped[rel])
                    fp.write("\n")