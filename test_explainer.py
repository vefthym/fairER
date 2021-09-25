import os
import sys
from matching import run_deepmatcher_w_explainer as dme

if __name__ == '__main__':
    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    datasets_path = 'resources/DeepMatcherDatasets/'
    datasets = [ 'DBLP-ACM']
    # datasets = [datasets[3]]
    for data in datasets:
        print('\n', data, '\n')

        data_path = sys.argv[1] if args else datasets_path + data + '/' # the folder containing train,valid,test data
        train_file = sys.argv[2] if args else 'merged_train.csv'
        valid_file = sys.argv[3] if args else 'merged_valid.csv'
        test_file = sys.argv[4] if args else 'merged_test.csv'
        # unlabeled_file = sys.argv[5] if args else data+path+'test_unlabeled.csv'  # unlabeled data for predictions
        dme.run(data_path,train_file,valid_file,test_file)
