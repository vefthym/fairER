import rdflib
import pickle
import random

def generate_rels_and_attrs(data, num):

    g = rdflib.Graph()
    g.parse("" + data + ".nt", format="nt")

    rels = []
    attrs = []
    print("PARSED !")
    for s, p, o in g:
        if isinstance(o, rdflib.Literal):
            attrs.append((s, p, o.rstrip().replace("\t", " ").replace("\"", "").replace("'", " ")))
        else:
            if str(p) == "http://dbkwik.webdatacommons.org/ontology/wikiPageExternalLink":
                attrs.append((s, p, o.rstrip().replace("\t", " ").replace("\"", "").replace("'", " ")))
            elif (str(p) == "http://dbkwik.webdatacommons.org/stexpanded.wikia.com/property/insignia" or str(p) == "http://dbkwik.webdatacommons.org/ontology/wikiPageWikiLink" or str(p) == "http://dbkwik.webdatacommons.org/ontology/wikiPageDisambiguates" or str(p) == "http://dbkwik.webdatacommons.org/memory-alpha.wikia.com/property/combatant" or str(p) == "http://dbkwik.webdatacommons.org/memory-alpha.wikia.com/property/image") and (".jpg" in o or ".png" in o or ".gif" in o or ".jpeg" in o or ".svg" in o or ".JPG" in o):
                attrs.append((s, p, o.rstrip().replace("\t", " ").replace("\"", "").replace("'", " ")))
            elif (str(p) == "http://xmlns.com/foaf/0.1/depiction" or str(p) == "http://dbkwik.webdatacommons.org/ontology/thumbnail") and (".jpg" not in s and ".png" not in s and ".gif" not in s and ".jpeg" not in s and ".svg" not in s and ".JPG" not in s):
                attrs.append((s, p, o.rstrip().replace("\t", " ").replace("\"", "").replace("'", " ")))
            elif ".jpg" not in s and ".png" not in s and ".gif" not in s and ".jpeg" not in s and ".svg" not in s and ".JPG" not in s:
                rels.append((s, p, o.rstrip()))

    # with open('rel_triples_' + num, 'w') as fp:
    #     for rel in rels:
    #         fp.write(rel[0])
    #         fp.write("\t")
    #         fp.write(rel[1])
    #         fp.write("\t")
    #         fp.write(rel[2])
    #         fp.write("\n")

    with open('attr_triples_' + num, 'w') as fp:
        for rel in attrs:
            fp.write(rel[0])
            fp.write("\t")
            fp.write(rel[1])
            fp.write("\t")
            fp.write(rel[2])
            fp.write("\n")


def generate_seed():
    seeds = []
    e1 = ""
    e2 = ""
    with open("reference.xml") as fp:
        for line in fp:

            if 'http://dbkwik.webdatacommons.org/memory-alpha.wikia.com/' in line:
                e1 = line.rstrip()
            if 'http://dbkwik.webdatacommons.org/stexpanded.wikia.com/' in line:
                e2 = line.rstrip()
            
            if e1 != "" and e2 != "":
                seeds.append((e1, e2))
                e1 = ""
                e2 = ""

    with open('ent_links', 'w') as fp:
        for pair in seeds:
            fp.write(pair[0])
            fp.write("\t")
            fp.write(pair[1])
            fp.write("\n")


def get_ents_of_KG(path, num, seeds, seeds_rev):
    ents = set()
    triples = []

    if num == "2":
        with open(path, 'r') as fp:
            for line in fp:
                e1 = line.split("\t")[0]
                p = line.split("\t")[1]
                e2 = line.split("\t")[2].rstrip()
                ents.add(e1)
                ents.add(e2)
                triples.append((e1, p, e2))
        return ents, triples

    with open(path, 'r') as fp:
        for line in fp:
            e1 = line.split("\t")[0]
            p = line.split("\t")[1]
            e2 = line.split("\t")[2].rstrip()
            ents.add(e1)
            ents.add(e2)
            triples.append((e1, p, e2))
    return ents, triples

def get_ents_intersection(ents1, ents2, seeds_rev):

    transl = set()
    for e2 in ents2:
        transl.add(seeds_rev[e2])

    return ents1.intersection(transl)


def generate_based_on_assumptions():

    seeds = {}
    seeds_rev = {}
    with open('ent_links.txt', 'r') as fp:
        for line in fp:
            e1 = line.split("\t")[0]
            e2 = line.split("\t")[1].rstrip()
            seeds[e1] = e2
            seeds_rev[e2] = e1

    ents1, triples1 = get_ents_of_KG("rel_triples_1.txt", "1", seeds, seeds_rev)
    ents2, triples2 = get_ents_of_KG("rel_triples_2.txt", "2", seeds, seeds_rev)
    print(len(ents1))
    print(len(ents2))

    keep_seed_1 = set()
    for e in ents1:
        if e in seeds:
            keep_seed_1.add(e)

    keep_seed_2 = set()
    for e in ents2:
        if e in seeds_rev:
            keep_seed_2.add(e)

    keep_seed_tr_1 = set()
    for tr in triples1:
        if tr[0] in seeds and tr[2] in seeds:
            keep_seed_tr_1.add(tr)

    keep_seed_tr_2 = set()
    for tr in triples2:
        if tr[0] in seeds_rev and tr[2] in seeds_rev:
            keep_seed_tr_2.add(tr)

    with open('../rel_triples_1_assumpt.txt', 'w') as fp:
        for triple in keep_seed_tr_1:
            fp.write(triple[0])
            fp.write("\t")
            fp.write(triple[1])
            fp.write("\t")
            fp.write(triple[2])
            fp.write("\n")

    with open('../rel_triples_2_assumpt.txt', 'w') as fp:
        for triple in keep_seed_tr_2:
            fp.write(triple[0])
            fp.write("\t")
            fp.write(triple[1])
            fp.write("\t")
            fp.write(triple[2])
            fp.write("\n")
    
    ents1, triples1 = get_ents_of_KG("../rel_triples_1_assumpt.txt", "1", seeds, seeds_rev)
    ents2, triples2 = get_ents_of_KG("../rel_triples_2_assumpt.txt", "2", seeds, seeds_rev)

    common_ents = get_ents_intersection(ents1, ents2, seeds_rev)

    keep_1 = set()
    for tr in triples1:
        if tr[0] in common_ents and tr[2] in common_ents:
            keep_1.add(tr)

    keep_2 = set()
    for tr in triples2:
        if seeds_rev[tr[0]] in common_ents and seeds_rev[tr[2]] in common_ents:
            keep_2.add(tr)

    with open('../rel_triples_1_assumpt2.txt', 'w') as fp:
        for triple in keep_1:
            fp.write(triple[0])
            fp.write("\t")
            fp.write(triple[1])
            fp.write("\t")
            fp.write(triple[2])
            fp.write("\n")

    with open('../rel_triples_2_assumpt2.txt', 'w') as fp:
        for triple in keep_2:
            fp.write(triple[0])
            fp.write("\t")
            fp.write(triple[1])
            fp.write("\t")
            fp.write(triple[2])
            fp.write("\n")

    counter = 0
    with open('../ent_links_assumpt2.txt', 'w') as fp:
        for e in seeds:
            if e in common_ents and seeds_rev[seeds[e]] in common_ents:
                counter += 1
                fp.write(e)
                fp.write("\t")
                fp.write(seeds[e])
                fp.write("\n")

    ents1, triples1 = get_ents_of_KG("../rel_triples_1_assumpt2.txt", "1", seeds, seeds_rev)
    ents2, triples2 = get_ents_of_KG("../rel_triples_2_assumpt2.txt", "2", seeds, seeds_rev)
    print(len(ents1))
    print(len(ents2))
    print(counter)

def split_dataset(dataset, train_ratio=0.2, test_ratio=0.70, validation_ratio=0.10):
    random.shuffle(dataset)
    total_data = len(dataset)
    train_data = int(total_data * train_ratio)
    test_data = int(total_data * test_ratio)
    validation_data = total_data - train_data - test_data

    return dataset[:train_data], dataset[train_data:train_data + test_data], dataset[train_data + test_data:]

def generate_splitting():
    dataset = []
    with open("ent_links", "r") as fp:
        for line in fp:
            dataset.append(line)
    train, test, valid = split_dataset(dataset)
    print(len(train))
    print(len(test))
    print(len(valid))

    with open("../721_5fold/2/train_links","w") as fp:
        for t in train:
            fp.write(t)

    with open("../721_5fold/2/valid_links","w") as fp:
        for t in valid:
            fp.write(t)

    with open("../721_5fold/2/test_links","w") as fp:
        for t in test:
            fp.write(t)
            
def generate_attrs_on_assumptions():
    ents = []
    with open("../ent_links", "r") as fp:
            for line in fp:
                ents.append(line.split("\t")[0])
                ents.append(line.split("\t")[1].rstrip())

    attrs = {}
    for i in [1, 2]:
        attrs[i] = []
        with open("attr_triples_" + str(i) + ".txt", "r") as fp:
            for line in fp:
                ent = line.split("\t")[0]
                if ent in ents:
                    attrs[i].append(line)

    for i in [1, 2]:
        with open("../attr_triples_" + str(i) + ".txt", "w") as fp:
            for attr in attrs[i]:
                fp.write(attr)


# START PREPROCESSING

generate_rels_and_attrs("alpha", "1")
generate_rels_and_attrs("expanded", "2")
# generate_seed()
# generate_splitting()

# generate_based_on_assumptions()
# generate_attrs_on_assumptions()