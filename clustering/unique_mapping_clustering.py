# Unique Mapping Clustering is a clustering method for ER,
# introduced in SiGMa paper.
# Input: a ranking of (left_id, right_id, [score]) candidate matches [scored]
# Output: a list of (left_id, right_id) matching results


# reads a list of 3-item lists, each representing a candiate pair in the form [left_id, right_id, score]
# returns a list of [left_id, right_id] matching results (each corresponding to a cluster for a real-world entity)
def run(candidates):
    matched_ids_left = set()
    matched_ids_right = set()
    matches = []
    for cand in candidates:
        #print(cand)
        if cand[0] in matched_ids_left or cand[1] in matched_ids_right:
            #print('Skipping candidate: ', cand)
            continue
        matches.append([cand[0],cand[1]])
        matched_ids_left.add(cand[0])
        matched_ids_right.add(cand[1])
    return matches

if __name__ == '__main__':
    cand_list = [[-1,1,0.5],[-1,3,0.3],[-2,3,0.2],[-3,3,0.1],[-4,4,0.0]]
    clusters = run(cand_list)
    print(clusters)
