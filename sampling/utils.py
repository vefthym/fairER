from sklearn.model_selection import train_test_split
import os
from rdflib import Literal
from rdflib.namespace import XSD, NamespaceManager

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


    def convert_sampling(conf_id, dataset):

        kg1 = KnowledgeGraph("1", dataset, "", "multi_directed", "sampled", conf_id, "RREA")

        RREA_process_RREA = "matching/RREA/RREA_process_datasets/" + dataset + "_RREA/"
        RREA_process_RDGCN = "matching/RREA/RREA_process_datasets/" + dataset
        dest_RREA = "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id
        dest_RDGCN = "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id.replace("RREA", "RDGCN")

        isExist = os.path.exists(dest_RDGCN)
        if isExist:
            if input("are you sure you want to override " + dest_RDGCN + " ? (y/n) ") != "y":
                exit()
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


        kg1 = KnowledgeGraph("2", dataset, "", "multi_directed", "sampled", conf_id, "RREA")

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


    def generate_rels(dataset):

        RREA_process_RREA = "matching/RREA/RREA_process_datasets/" + dataset + "_RREA/"
        RREA_process_RDGCN = "matching/RREA/RREA_process_datasets/" + dataset
        

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

            with open(RREA_process_RREA + "rel_ids_" + str(num), "w") as fp:
                for rel in mapped:
                    fp.write(rel)
                    fp.write("\t")
                    fp.write(mapped[rel])
                    fp.write("\n")


    def convert_to_ttl(conf_id, dataset):

        if conf_id == "original":
            path = "matching/RREA/RREA_process_datasets/" + dataset
            dest_path = "matching/kba/" + dataset + "/" + "original" + "/"
            mapping_path = path + "/ent_links"
        elif "conf" in conf_id:
            path = "matching/RREA/sampled/" + dataset + "_sampled/" + conf_id
            dest_path = "matching/kba/" + dataset + "/" + conf_id + "/"
            mapping_path = path + "/721_5fold/2/ent_links"

        intersection_preds = {
        "http://dbpedia.org/ontology/populationDensity": 'http://yago-knowledge.org/ontology/hasPopulationDensity',
        "http://dbpedia.org/ontology/height": 'http://yago-knowledge.org/ontology/hasHeight',
        # "http://dbpedia.org/ontology/revenue": 'http://yago-knowledge.org/ontology/hasRevenue',
        # "http://dbpedia.org/ontology/area": 'http://yago-knowledge.org/ontology/hasArea',
        "http://dbpedia.org/ontology/influenced": 'http://yago-knowledge.org/ontology/influences',
        "http://dbpedia.org/ontology/language": 'http://yago-knowledge.org/ontology/hasOfficialLanguage',
        # "http://dbpedia.org/ontology/capital": 'http://yago-knowledge.org/ontology/hasCapital',
        "http://dbpedia.org/ontology/doctoralAdvisor": 'http://yago-knowledge.org/ontology/hasAcademicAdvisor',
        "http://xmlns.com/foaf/0.1/name": 'http://yago-knowledge.org/ontology/skos:prefLabel'}

        # with open(path + "/attr_triples_2") as fp:
        #     for line in fp:
                        
        #         s = "<http://yago-knowledge.org/resource/" + line.split("\t")[0] + ">"
        #         p = "<http://yago-knowledge.org/ontology/" + line.split("\t")[1] + ">"
        #         o = line.split("\t")[2].rstrip()
        #         if "^^" not in o and '"@' not in o:
        #             print(Literal(o).n3()) 
        # exit()

        isExist = os.path.exists(dest_path)
        if isExist:
            if input("are you sure you want to override " + dest_path + " ? (y/n) ") != "y":
                exit()
        if not isExist:
            os.makedirs(dest_path)

        with open(path + "/rel_triples_1") as fp:
            with open(dest_path + "/rel_triples_1.ttl", "w") as fp2:
                for line in fp:

                    if line.split("\t")[1] in intersection_preds:
                        p2 = intersection_preds[line.split("\t")[1]]
                    else:
                        p2 = line.split("\t")[1]
                        
                    s = "<" + line.split("\t")[0] + ">"
                    p = "<" + p2 + ">"
                    o = "<" + line.split("\t")[2].rstrip() + ">"

                    fp2.write( s + "\t" + p + "\t" + o + "\t" + ".\n")

        with open(path + "/rel_triples_2") as fp:
            with open(dest_path + "/rel_triples_2.ttl", "w") as fp2:
                for line in fp:
                        
                    s = "<http://yago-knowledge.org/resource/" + line.split("\t")[0] + ">"
                    p = "<http://yago-knowledge.org/ontology/" + line.split("\t")[1] + ">"
                    o = "<http://yago-knowledge.org/resource/" + line.split("\t")[2].rstrip() + ">"

                    fp2.write( s + "\t" + p + "\t" + o + "\t" + ".\n")

        with open(mapping_path) as fp:
            with open(dest_path + "/ent_links.ttl", "w") as fp2:
                for line in fp:

                    s = "<" + line.split("\t")[0] + ">"
                    p = "<http://www.w3.org/2002/07/owl#sameAs>"
                    o = "<http://yago-knowledge.org/resource/" + line.split("\t")[1].rstrip() + ">"

                    fp2.write( s + "\t" + p + "\t" + o + "\t" + ".\n")

        with open(path + "/attr_triples_1") as fp:
            with open(dest_path + "/attr_triples_1.ttl", "w") as fp2:
                for line in fp:

                    if line.split("\t")[1] in intersection_preds:
                        p2 = intersection_preds[line.split("\t")[1]]
                    else:
                        p2 = line.split("\t")[1]

                    s = "<" + line.split("\t")[0] + ">"
                    p = "<" + p2 + ">"
                    o = line.split("\t")[2].rstrip()

                    if "^^" not in o and '"@' not in o:
                        o = Literal(o).n3()
                        
                    fp2.write( s + "\t" + p + "\t" + o + "\t" + ".\n")

        with open(path + "/attr_triples_2") as fp:
            with open(dest_path + "/attr_triples_2.ttl", "w") as fp2:
                for line in fp:
                        
                    s = "<http://yago-knowledge.org/resource/" + line.split("\t")[0] + ">"
                    p = "<http://yago-knowledge.org/ontology/" + line.split("\t")[1] + ">"
                    o = line.split("\t")[2].rstrip()

                    if "^^" not in o and '"@' not in o:
                        o = Literal(o).n3() 

                    fp2.write( s + "\t" + p + "\t" + o + "\t" + ".\n")