# Fair Unique Mapping Clustering is a novel method that extends the
# Unique Mapping clustering method for ER introduced in SiGMa paper.
# Input: a ranking of (left_id, right_id, [score]) candidate matches [scored]
# Output: a list of (left_id, right_id) matching results


# reads a list of quadruples, each representing a candiate pair in the form [left_id, right_id, score, protected(t/f)]
# returns a list of [left_id, right_id] matching results (each corresponding to a cluster for a real-world entity)
# at each iteration, the number of returned results for protected and unprotected groups cannot differ by more than 1
def run(candidates, results_limit):
    matched_ids_left = set()
    matched_ids_right = set()
    matches = []

    protected_candidates = [x for x in candidates if x[3]]
    nonprotected_candidates = [x for x in candidates if not x[3]]

    #print(protected_candidates)
    #print(nonprotected_candidates)

    nextProtected = True
    while (protected_candidates or nonprotected_candidates) and (len(matches) < results_limit):
        cand = protected_candidates.pop(0) if nextProtected else nonprotected_candidates.pop(0)
        #print(cand)

        # unique mapping constraint check
        if cand[0] in matched_ids_left or cand[1] in matched_ids_right:
            #print('Skipping candidate: ', cand, 'for violating unique mapping constraint')
            continue

        # add pair to matches
        matches.append([cand[0],cand[1]])
        matched_ids_left.add(cand[0])
        matched_ids_right.add(cand[1])

        if (nextProtected and nonprotected_candidates) or (not nextProtected and protected_candidates):
            nextProtected = not nextProtected  # swap queues
            #print('swapping to ', 'protected' if nextProtected else 'nonprotected', 'queue')

    return matches


if __name__ == '__main__':
    cand_list = [[-1,1,0.5,False],[-1,3,0.3,False],[-2,3,0.2,True],[-3,3,0.1,False],[-4,4,0.0,True]]
    clusters = run(cand_list)
    #print(clusters)
