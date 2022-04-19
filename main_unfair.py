from matching import run_deepmatcher as dm
import sys
import pandas as pd
import os
from clustering import unique_mapping_clustering as umc
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
import util
import time


def run(data, data_path, train, valid, test, k_results):
    ###########
    # Matching
    ###########

    if not os.path.exists(data_path + '/dm_results.csv'):
        preds = dm.run(data_path, train, valid, test)  # , unlabeled_file)
        preds.to_csv(data_path + '/dm_results.csv')

    preds = pd.read_csv(data_path + '/dm_results.csv')

    # Ranking of matching results in desc. match score
    preds = preds.sort_values(by='match_score', ascending=False)
    # print("Initial Ranking:\n", preds[:k].to_string(index=False))

    initial_pairs = [(int(a.id.split('_')[0]), int(a.id.split('_')[1]), a.match_score, util.tuple_is_protected(a, data))
                     for a in preds.itertuples()]

    #############################
    # Unique Mapping Clustering
    #############################

    original_clusters = umc.run(initial_pairs[:k_results])
    # print("\nclustering results:\n", original_clusters)
    return original_clusters, preds


if __name__ == '__main__':
    k = 20
    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    datasets_path = 'resources/DeepMatcherDatasets/'
    datasets = ['Beer', 'iTunes-Amazon', 'Fodors-Zagats', 'DBLP-ACM', 'DBLP-GoogleScholar',
                'Amazon-Google', 'Walmart-Amazon']
    #datasets = [datasets[4]]
    for data in datasets:

        print('\n', data, '\n')

        data_path = sys.argv[1] if args else datasets_path+data  # the folder containing train,valid,test data
        train_file = sys.argv[2] if args else 'joined_train.csv'
        valid_file = sys.argv[3] if args else 'joined_valid.csv'
        test_file = sys.argv[4] if args else 'joined_test.csv'
        # unlabeled_file = sys.argv[5] if args else data+path+'test_unlabeled.csv'  # unlabeled data for predictions

        av_time = 0
        for _ in range(10):
            start_time = time.time()
            clusters, preds = run(data, data_path, train_file, valid_file, test_file, k)
            ex_time = time.time() - start_time
            av_time += ex_time

        ############################
        # Evaluation
        ############################
        print("--- %s seconds ---" % (av_time / 10.0))

        accuracy = eval.get_accuracy(clusters, preds)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd(clusters, preds, data)
        print("SPD:", spd)

        eod = f_eval.get_eod(clusters, preds, data)
        print("EOD:", eod)
        print()




