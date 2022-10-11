from clustering import unique_mapping_clustering as umc
import os
import pickle

def run():
    os.chdir("matching/RREA/")
    os.system("python RREA.py sampled conf_2_only_p -1")

def main():
    dest_path = "matching/RREA/exp_results/test_experiments/D_Y_15K_V1/conf_2_only_p/D_Y_15K_V1_sim_lists_NO_CSLS_sampled.pickle"
    isExist = os.path.exists(dest_path)

    if isExist:
        with (open("matching/RREA/exp_results/test_experiments/D_Y_15K_V1/conf_1_only_p/D_Y_15K_V1_sim_lists_NO_CSLS_sampled.pickle", "rb")) as fp:
            sim_lists_no_csls = pickle.load(fp)

        index_to_id = {}
        for pair in sim_lists_no_csls:
            index_to_id[pair[0]] = pair[1]

        # tp for simple alignemnt results (first match consequencing to not 1-to-1 constraint)
        tp = 0
        for pair in sim_lists_no_csls:
            if pair[0] == sim_lists_no_csls[pair][0][0]:
                tp += 1
        print(tp/700 * 100)

        # unique mapping clustering
        candidates = []
        for pair in sim_lists_no_csls:
            for sim_pairs in sim_lists_no_csls[pair]:
                candidates.append([pair[1], index_to_id[sim_pairs[0]], abs(sim_pairs[1])])
        candidates.sort(key=lambda x: x[2], reverse=True)
        results = umc.run(candidates)

        # check if 1-to-1
        left = []
        right = []
        for r in results:
            left.append(r[0])
            right.append(r[1])
        assert(len(left) == len(right))

        # measure tp
        tp = 0
        for r in results:
            if r[0] == r[1]:
                tp += 1
        print(tp/700 * 100)


    elif not isExist:
        run()
        

if __name__ == '__main__':
    main()