import os.path
from os import path
import os

def check_ids(path):
    print(path)
    with open(path) as fp:
        h_set = set()
        t_set = set()
        r_set = set()
        for line in fp:
            h = line.split("\t")[0]
            t = line.split("\t")[2].rstrip()
            r = line.split("\t")[1]
            h_set.add(int(h))
            t_set.add(int(t))
            r_set.add(int(r))
        print("Heads: ")
        print(min(h_set))
        print(max(h_set))
        print("Relations: ")
        print(min(r_set))
        print(max(r_set))
        print("Tails: ")
        print(min(t_set))
        print(max(t_set))

def generate_ids(paths, attr_paths, dest_path, seed_path):
    e_dict = {}
    r_dict = {}
    num = 0
    for p in paths:
        num += 1
        with open(p) as fp:
            for line in fp:
                h = line.split("\t")[0]
                t = line.split("\t")[2].rstrip()
                r = line.split("\t")[1]
                if h not in e_dict.keys():
                    e_dict[h] = (len(e_dict.keys()), "KG" + str(num))
                if t not in e_dict.keys():
                    e_dict[t] = (len(e_dict.keys()), "KG" + str(num))
                if r not in r_dict.keys():
                    r_dict[r] = (len(r_dict.keys()), "KG" + str(num))

    for num in range(1,3):
        with open(dest_path + "/ent_ids_" + str(num), "w") as fp2:
            for e in e_dict.keys():
                if e_dict[e][1] == "KG" + str(num):
                    fp2.write(str(e_dict[e][0]) + "\t" + e + "\n")

        # ********* Uncomment in order to generate rel_ids files *********
        with open(dest_path + "/rel_ids_" + str(num), "w") as fp3:
            for r in r_dict.keys():
                if r_dict[r][1] == "KG" + str(num):
                    fp3.write(str(r_dict[r][0]) + "\t" + r + "\n")

    dest_seed = os.path.join(dest_path, "721_5fold")
    if not path.exists(dest_seed):
        os.mkdir(os.path.join(dest_path, "721_5fold"))
        os.mkdir(os.path.join(dest_path, "721_5fold", "2"))

    # with open(temp_seed) as fp10:
    #         with open(dest_path + "/ref_ent_ids", "w") as fp11:
    #             for pair in fp10:
    #                 e1 = pair.split("\t")[0]
    #                 e2 = pair.split("\t")[1].rstrip()
    #                 fp11.write(str(e_dict[e1][0]) + "\t" + str(e_dict[e2][0]) + "\n")

    for fold in [2]:
        with open(seed_path + "/" + str(fold) + "/train_links") as fp4:
            with open(dest_path + "/721_5fold/" + str(fold) + "/train_links", "w") as fp5:
                for pair in fp4:
                    e1 = pair.split("\t")[0]
                    e2 = pair.split("\t")[1].rstrip()
                    if e1 in e_dict.keys() and e2 in e_dict.keys():
                        fp5.write(str(e_dict[e1][0]) + "\t" + str(e_dict[e2][0]) + "\n")
        with open(seed_path + "/" + str(fold) + "/test_links") as fp8:
            with open(dest_path + "/721_5fold/" + str(fold) + "/test_links", "w") as fp9:
                for pair in fp8:
                    e1 = pair.split("\t")[0]
                    e2 = pair.split("\t")[1].rstrip()
                    if e1 in e_dict.keys() and e2 in e_dict.keys():
                        fp9.write(str(e_dict[e1][0]) + "\t" + str(e_dict[e2][0]) + "\n")
        with open(seed_path + "/" + str(fold) + "/valid_links") as fp10:
            with open(dest_path + "/721_5fold/" + str(fold) + "/valid_links", "w") as fp11:
                for pair in fp10:
                    e1 = pair.split("\t")[0]
                    e2 = pair.split("\t")[1].rstrip()
                    if e1 in e_dict.keys() and e2 in e_dict.keys():
                        fp11.write(str(e_dict[e1][0]) + "\t" + str(e_dict[e2][0]) + "\n")

    num = 0
    for p in paths:
        num += 1
        with open(p) as fp6:
            with open(dest_path + "/rel_triples_" + str(num), "w") as fp7:
                for line in fp6:
                    h = line.split("\t")[0]
                    t = line.split("\t")[2].rstrip()
                    r = line.split("\t")[1]
                    fp7.write(str(e_dict[h][0]) + "\t" + str(r_dict[r][0]) + "\t" + str(e_dict[t][0]) + "\n")

    num = 0
    for p in attr_paths:
        num += 1
        with open(p) as fp6:
            with open(dest_path + "/attr_triples_" + str(num), "w") as fp7:
                for line in fp6:
                    h = line.split("\t")[0]
                    t = line.split("\t")[2].rstrip()
                    r = line.split("\t")[1]
                    fp7.write(str(e_dict[h][0]) + "\t" + r + "\t" + t + "\n")

# path = "../data/zh_en/triples_1"
# check_ids(path)
# path = "../data/zh_en/triples_2"
# check_ids(path)

def run(dataset, src_path, dest_path):

    if not path.exists(dest_path):
        os.mkdir(dest_path)
    
    paths = [os.path.join(src_path, "rel_triples_1"), os.path.join(src_path, "rel_triples_2")]
    attr_paths = [os.path.join(src_path, "attr_triples_1"), os.path.join(src_path, "attr_triples_2")]
    seed_path = os.path.join(src_path, "721_5fold")
    # temp_seed = dataset + "/ent_links"
    generate_ids(paths, attr_paths, dest_path, seed_path)