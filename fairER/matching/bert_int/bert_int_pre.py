import os

def preprocess_for_bert_int(dataset_path, save_path):

    isExist = os.path.exists(save_path)

    if not isExist:
        os.makedirs(save_path)
        os.makedirs(save_path + "/temp/")

    ent_ind = 0
    rel_ind = 0
    full_ents = {}

    for i in ["1", "2"]:
        
        ents = {}
        rels = {}

        with open(dataset_path + "/rel_triples_" + i) as fp:
            for line in fp:
                e1 = line.split("\t")[0]
                e2 = line.split("\t")[2].rstrip()
                r = line.split("\t")[1]

                if e1 not in ents:
                    ents[e1] = str(ent_ind)
                    full_ents[e1] = str(ent_ind)
                    ent_ind += 1

                if e2 not in ents:
                    ents[e2] = str(ent_ind)
                    full_ents[e2] = str(ent_ind)
                    ent_ind += 1

                if r not in rels:
                    rels[r] = str(rel_ind)
                    rel_ind += 1


        with open(dataset_path + "/rel_triples_" + i) as fp:
            with open(save_path + "/triples_" + i, "w") as fp2:
                for line in fp:
                    e1 = line.split("\t")[0]
                    e2 = line.split("\t")[2].rstrip()
                    r = line.split("\t")[1]
                    fp2.write(ents[e1])
                    fp2.write("\t")
                    fp2.write(rels[r])
                    fp2.write("\t")
                    fp2.write(ents[e2])
                    fp2.write("\n")

        with open(dataset_path + "/attr_triples_" + i) as fp:
            with open(save_path + "/attr_triples" + i, "w") as fp2:
                for line in fp:
                    fp2.write(line)

        with open(save_path + "/ent_ids_" + i, "w") as fp2:
            for e in ents:
                fp2.write(ents[e])
                fp2.write("\t")
                fp2.write(e)
                fp2.write("\n")

        with open(save_path + "/rel_ids_" + i, "w") as fp2:
            for r in rels:
                fp2.write(rels[r])
                fp2.write("\t")
                fp2.write(r)
                fp2.write("\n")

    with open(dataset_path + "/721_5fold/" + "2" + "/train_links") as fp:
        with open(save_path + "/sup_pairs", "w") as fp2:
            for line in fp:
                e1 = line.split("\t")[0]
                e2 = line.split("\t")[1].rstrip()
                fp2.write(full_ents[e1])
                fp2.write("\t")
                fp2.write(full_ents[e2])
                fp2.write("\n")

    with open(dataset_path + "/721_5fold/" + "2" + "/test_links") as fp:
        with open(save_path + "/ref_pairs", "w") as fp2:
            for line in fp:
                e1 = line.split("\t")[0]
                e2 = line.split("\t")[1].rstrip()
                fp2.write(full_ents[e1])
                fp2.write("\t")
                fp2.write(full_ents[e2])
                fp2.write("\n")