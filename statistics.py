from matching import run_deepmatcher as dm
import sys
import os
import util
import json
import pandas as pd


def main(dataset):
    ###########
    # Matching
    ###########
    train_file = 'joined_train.csv'
    valid_file = 'joined_valid.csv'
    test_file = 'joined_test.csv'
    cur_dir = os.path.abspath(".")
    data_path = os.path.join(cur_dir, '..', 'resources', 'Datasets', dataset)
    # comment out after the first run (it writes output to file, which does not need to be re-written in every run)
    dm_results = data_path+'/dm_results.csv'
    if not os.path.exists(dm_results):
        preds = dm.run(data_path, train_file, valid_file,
                       test_file, epochs=10)  # , unlabeled_file)
        preds.to_csv(dm_results)
    # otherwise throws error: Pandas has no attribute 'id'
    preds = pd.read_csv(dm_results)

    # Ranking of matching results in desc. match score
    preds = preds.sort_values(by='match_score', ascending=False)
    #print("Initial Ranking:\n", preds[:20].to_string(index=False))

    initial_pairs = []
    avg_score_protected = 0
    avg_score_nonprotected = 0
    num_protected = 0

    avg_score_protected_matches = 0
    avg_score_nonprotected_matches = 0
    num_protected_matches = 0
    num_nonprotected_matches = 0

    for i in preds.itertuples():
        is_protected = util.pair_is_protected(i, dataset)
        # print(i.id, i.match_score, 'Protected' if is_protected else 'Nonprotected')
        candidate = preds[preds['id'] == i.id][['id', 'match_score']] \
            .to_string(header=None, index=False).split()
        candidate = [int(candidate[0].split('_')[0]), int(
            candidate[0].split('_')[1]), float(candidate[1]), is_protected]
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


    if num_protected != 0:
        avg_score_protected /= num_protected
    if (len(preds)-num_protected) != 0:
        avg_score_nonprotected /= (len(preds)-num_protected)

    ####################
    # PRINT STATISTICS #
    ####################

    #print('\nnum protected matches', num_protected_matches)
    #print('num nonprotected matches', num_nonprotected_matches)

    #print('\naverage match score of protected: ', avg_score_protected)
    #print('average match score of nonprotected: ', avg_score_nonprotected)

    if num_protected_matches > 0:
        avg_score_protected_matches = avg_score_protected_matches / num_protected_matches
        #print('\naverage match score of protected matches: ', avg_score_protected_matches)
    if num_nonprotected_matches > 0:
        avg_score_nonprotected_matches /= num_nonprotected_matches
        #print('average match score of nonprotected matches: ', avg_score_nonprotected_matches)

        #################################
        # Write statistics to json file
        #################################
        data = {'num_protected_matches': str(num_protected_matches), 'num_nonprotected_matches': str(num_nonprotected_matches),
                'avg_score_protected': str(avg_score_protected), 'avg_score_nonprotected': str(avg_score_nonprotected),
                'avg_score_protected_matches': str(avg_score_protected_matches), 'avg_score_nonprotected_matches': str(avg_score_nonprotected_matches)}
        json_string = json.dumps(data)
        with open('data/json_data/statistics_data.json', 'w+') as outfile:
            outfile.write(json_string)





if __name__ == '__main__':
    dataset = sys.argv[1]
    main(dataset)