from matching import run_deepmatcher as dm
import sys
import pandas as pd
import os
from clustering import unique_mapping_clustering as umc
import evaluation.accuracy as eval
import util


if __name__ == '__main__':
    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    datasets_path = 'resources/DeepMatcherDatasets/'
    dataset_name = 'DBLP-ACM'  #'iTunes-Amazon'
    data_path = sys.argv[1] if args else datasets_path + dataset_name  # the folder containing train,valid,test data
    train_file = sys.argv[2] if args else 'joined_train.csv'
    valid_file = sys.argv[3] if args else 'joined_valid.csv'
    test_file = sys.argv[4] if args else 'joined_test.csv'
    # unlabeled_file = sys.argv[5] if args else data+path+'test_unlabeled.csv'  # unlabeled data for predictions

    ###########
    # Matching
    ###########

    # comment out after the first run (it writes output to file, which does not need to be re-written in every run)
    dm_results = data_path+'/dm_results.csv'
    if not os.path.exists(dm_results):
        preds = dm.run(data_path, train_file, valid_file, test_file, epochs=10)  # , unlabeled_file)
        preds.to_csv(dm_results)
    preds = pd.read_csv(dm_results)  # otherwise throws error: Pandas has no attribute 'id'

    # Ranking of matching results in desc. match score
    preds = preds.sort_values(by='match_score', ascending=False)
    print("Initial Ranking:\n", preds[:20].to_string(index=False))

    initial_pairs = []
    avg_score_protected = 0
    avg_score_nonprotected = 0
    num_protected = 0

    avg_score_protected_matches = 0
    avg_score_nonprotected_matches = 0
    num_protected_matches = 0
    num_nonprotected_matches = 0

    for i in preds.itertuples():
        is_protected = util.tuple_is_protected(i,dataset_name)
        # print(i.id, i.match_score, 'Protected' if is_protected else 'Nonprotected')
        candidate = preds[preds['id'] == i.id][['id', 'match_score']] \
            .to_string(header=None, index=False).split()
        candidate = [int(candidate[0].split('_')[0]), int(candidate[0].split('_')[1]), float(candidate[1]), is_protected]
        initial_pairs.append(candidate)
        is_a_match = i.label == 1
        if is_protected:
            avg_score_protected += i.match_score
            num_protected += 1
            if is_a_match:
                avg_score_protected_matches += i.match_score
                num_protected_matches += 1
        else:
            avg_score_nonprotected += i.match_score
            if is_a_match:
                avg_score_nonprotected_matches += i.match_score
                num_nonprotected_matches += 1

    avg_score_protected /= num_protected
    avg_score_nonprotected /= (len(preds)-num_protected)

    ####################
    # PRINT STATISTICS #
    ####################

    print('\nnum protected matches', num_protected_matches)
    print('num nonprotected matches', num_nonprotected_matches)

    print('\naverage match score of protected: ', avg_score_protected)
    print('average match score of nonprotected: ', avg_score_nonprotected)

    if num_protected_matches > 0:
        avg_score_protected_matches = avg_score_protected_matches / num_protected_matches
        print('\naverage match score of protected matches: ', avg_score_protected_matches)
    if num_nonprotected_matches > 0:
        avg_score_nonprotected_matches /= num_nonprotected_matches
        print('average match score of nonprotected matches: ', avg_score_nonprotected_matches)

