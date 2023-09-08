from crypt import methods
from matching import run_deepmatcher as dm
import sys, json
import pandas as pd
import os
from fairsearchcore.models import FairScoreDoc
from fair_ranking import fa_ir as fr
from clustering import unique_mapping_clustering as umc
import evaluation.accuracy as eval
import evaluation.fairness as f_eval
import util
import time
import web.library.methods


def run(data, data_path, train_file, valid_file, test_file, k_results):
    ###########
    # Matching
    ###########

    # comment out after the first run (it writes output to file, which does not need to be re-written in every run)
    if not os.path.exists(data_path + '/dm_results.csv'):
        preds = dm.run(data_path, train_file, valid_file, test_file)  # , unlabeled_file)
        preds.to_csv(data_path + '/dm_results.csv')


    preds = pd.read_csv(data_path + '/dm_results.csv')
    # Ranking of matching results in desc. match score
    preds = preds.sort_values(by='match_score', ascending=False)
    #print("Initial Ranking (top-20):\n", preds[:20].to_string())

    ###########
    # Fairness
    ###########
    start_time = time.time()
    initial_ranking = [FairScoreDoc(a.id, a.match_score, util.tuple_is_protected(a, data)) for a in
                       preds.itertuples()]
    #print("Initial Ranking:", initial_ranking)
    end_init_ranking_time = time.time()
    print('Initial ranking time: %s ', (end_init_ranking_time-start_time))

    k = 2*k_results  # number of topK elements returned (value should be between 10 and 400)
    p = 0.5  # proportion of protected candidates in the topK elements (value should be between 0.02 and 0.98)
    alpha = 0.1  # significance level (value should be between 0.01 and 0.15)

    fair = fr.pre_process_fair(k, p, alpha)
    #print('Fair' if fair.is_fair(initial_ranking[:k]) else 'Unfair', 'ranking!')
    end_prepr_time = time.time()
    print('Preprocessing time: %s ', (end_prepr_time-end_init_ranking_time))

    re_ranked = fair.re_rank(initial_ranking)
    #print("FA*IR Re-Ranking:", re_ranked)
    #print('Fair' if fair.is_fair(re_ranked) else 'Unfair', 'ranking!')
    end_re_ranking_time = time.time()
    print('Re-ranking time: %s ', (end_re_ranking_time-end_prepr_time))

    # [print(i.id, i.score, 'protected' if i.is_protected else 'Nonprotected') for i in re_ranked]

    # re_ranked_pairs = []  # will store the resulting ranking from FA*IR algorithm
    # for i in re_ranked:
    #     #print(i.id, i.score, 'Protected' if i.is_protected else 'Nonprotected')
    #     candidate = preds[preds['id'] == i.id][['id', 'match_score']] \
    #         .to_string(header=None, index=False).split()
    #     candidate = [int(candidate[0].split('_')[0]), int(candidate[0].split('_')[1]), float(candidate[1])]
    #     re_ranked_pairs.append(candidate)

    re_ranked_pairs = [(int(a.id.split('_')[0]), int(a.id.split('_')[1]), float(a.score)) for a in re_ranked]
    end_re_ranking_list = time.time()
    print('Re-ranking list_creation: %s ', (end_re_ranking_list- end_re_ranking_time))

    #############################
    # Unique Mapping Clustering
    #############################

    clusters = umc.run(re_ranked_pairs[:k_results])
    #print("\nclustering results:\n", clusters)


    ####################################################
    # Write clusters to json file
    ####################################################
    data = {'clusters': clusters}
    json_string = json.dumps(data)
    with open('web/data/json_data/clusters_data.json', 'w+') as outfile:
        outfile.write(json_string)

    ###########################
    # Write preds to json file
    ###########################
    web.library.methods.csv_to_json(data_path + '/dm_results.csv',
                      'web/data/json_data/preds_data.json')


    return clusters, preds


if __name__ == '__main__':
    k = 20
    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    datasets_path = 'resources/DeepMatcherDatasets/'
    datasets = ['Beer', 'iTunes-Amazon', 'Fodors-Zagats', 'DBLP-ACM', 'DBLP-GoogleScholar',
                'Amazon-Google', 'Walmart-Amazon']
    # datasets = [datasets[3]]
    for data in datasets:
        print('\n', data, '\n')

        data_path = sys.argv[1] if args else datasets_path + data  # the folder containing train,valid,test data
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

        #############################
        # Evaluation
        #############################

        print("--- %s seconds ---" % (av_time/10.0))

        accuracy = eval.get_accuracy(clusters, preds)
        print("accuracy:", accuracy)

        spd = f_eval.get_spd(clusters, preds, data)
        print("SPD:", spd)

        eod = f_eval.get_eod(clusters, preds, data)
        print("EOD:", eod)
        print()


