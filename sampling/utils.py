from sklearn.model_selection import train_test_split
import os

from matching.KG.KnowledgeGraph import KnowledgeGraph

class Utils:

    @staticmethod
    def check_embedding_constraints(kg1, ents1, ents2):

        seed_pairs = kg1.get_seed_pairs()
        not_included_in_both = 0
        counterparts = set()
        for e in ents1:
            if seed_pairs[e] not in ents2:
                not_included_in_both += 1
                counterparts.add(seed_pairs[e])
        
        assert not_included_in_both == 0

        print(not_included_in_both)

        print(len(ents1))
        print(len(ents2))
        print()

    @staticmethod
    def generate_seeds_and_splittings(dataset, prefix, ents1, ents2, dest_seed_path, method):

        if method == "RREA":
            splittings = {
                "test_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/test_links"},
                "train_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/train_links"},
                "valid_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "_RREA/721_5fold/2/valid_links"}
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
                "test_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "/721_5fold/2/test_links"},
                "train_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "/721_5fold/2/train_links"},
                "valid_pairs": { "src_path": "matching/RREA/RREA_process_datasets/" + dataset + prefix + "/721_5fold/2/valid_links"}
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


    # def convert_sampling(conf_id, dataset):

    #     kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", conf_id)

    #     nodes_1 = kg1.graph.nodes()
    #     ids_to_uris = {}
    #     with open("../RREA_process_datasets/" + dataset + "_RREA/ent_ids_1") as fp:
    #         for line in fp:
    #             ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()

    #     uris_to_ids = {}
    #     with open("../RREA_process_datasets/" + dataset + "_RREA/ent_ids_1") as fp:
    #         for line in fp:
    #             uris_to_ids[line.split("\t")[1].rstrip()] = line.split("\t")[0]

    #     nodes_1_conv = list()
    #     for n in nodes_1:
    #         nodes_1_conv.append(ids_to_uris[n])

    #     attr_1 = {}
    #     with open("../RREA_process_datasets/" + dataset + "/attr_triples_1") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/attr_triples_1", "w") as fp2:
    #             for line in fp:
    #                 ent = line.split("\t")[0]
    #                 if ent in nodes_1_conv:
    #                     fp2.write(ent + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])

    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/rel_triples_1") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/rel_triples_1", "w") as fp2:
    #             for line in fp:
    #                 fp2.write(ids_to_uris[int(line.split("\t")[0])] + "\t" + line.split("\t")[1] + "\t" + ids_to_uris[int(line.split("\t")[2].rstrip())] + "\n")


    #     kg1 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", conf_id)

    #     nodes_1 = kg1.graph.nodes()
    #     with open("../RREA_process_datasets/" + dataset + "_RREA/ent_ids_2") as fp:
    #         for line in fp:
    #             ids_to_uris[int(line.split("\t")[0])] = line.split("\t")[1].rstrip()

    #     uris_to_ids = {}
    #     with open("../RREA_process_datasets/" + dataset + "_RREA/ent_ids_2") as fp:
    #         for line in fp:
    #             uris_to_ids[line.split("\t")[1].rstrip()] = line.split("\t")[0]

    #     nodes_1_conv = list()
    #     for n in nodes_1:
    #         nodes_1_conv.append(ids_to_uris[n])

    #     attr_1 = {}
    #     with open("../RREA_process_datasets/" + dataset + "/attr_triples_2") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/attr_triples_2", "w") as fp2:
    #             for line in fp:
    #                 ent = line.split("\t")[0]
    #                 if ent in nodes_1_conv:
    #                     fp2.write(ent + "\t" + line.split("\t")[1] + "\t" + line.split("\t")[2])

    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/rel_triples_2") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/rel_triples_2", "w") as fp2:
    #             for line in fp:
    #                 fp2.write(ids_to_uris[int(line.split("\t")[0])] + "\t" + line.split("\t")[1] + "\t" + ids_to_uris[int(line.split("\t")[2].rstrip())] + "\n")


    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/ent_links") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/721_5fold/2/ent_links", "w") as fp2:
    #             for line in fp:
    #                 e1 = int(line.split("\t")[0])
    #                 e2 = int(line.split("\t")[1].rstrip())
    #                 fp2.write(ids_to_uris[e1])
    #                 fp2.write("\t")
    #                 fp2.write(ids_to_uris[e2])
    #                 fp2.write("\n")

    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/test_links") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/721_5fold/2/test_links", "w") as fp2:
    #             for line in fp:
    #                 e1 = int(line.split("\t")[0])
    #                 e2 = int(line.split("\t")[1].rstrip())
    #                 fp2.write(ids_to_uris[e1])
    #                 fp2.write("\t")
    #                 fp2.write(ids_to_uris[e2])
    #                 fp2.write("\n")
        
    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/train_links") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/721_5fold/2/train_links", "w") as fp2:
    #             for line in fp:
    #                 e1 = int(line.split("\t")[0])
    #                 e2 = int(line.split("\t")[1].rstrip())
    #                 fp2.write(ids_to_uris[e1])
    #                 fp2.write("\t")
    #                 fp2.write(ids_to_uris[e2])
    #                 fp2.write("\n")

    #     with open("sampled/" + dataset + "_sampled/" + conf_id + "/721_5fold/2/valid_links") as fp:
    #         with open("sampled/" + dataset + "_sampled/" + conf_id + "_RDGCN" + "/721_5fold/2/valid_links", "w") as fp2:
    #             for line in fp:
    #                 e1 = int(line.split("\t")[0])
    #                 e2 = int(line.split("\t")[1].rstrip())
    #                 fp2.write(ids_to_uris[e1])
    #                 fp2.write("\t")
    #                 fp2.write(ids_to_uris[e2])
    #                 fp2.write("\n")