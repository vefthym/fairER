#import py_entitymatching as em
import sys
import os
import deepmatcher as dm
import pandas as pd
from matching import run_deepmatcher as match


# code from https://colab.research.google.com/drive/1CQFejG3-KeuFmMChsEoOeqypTS7njyJb#scrollTo=qj-AXGxmR_gL
def merge_data(labeled, table_a, table_b, output):
    merged_csv = pd.read_csv(labeled).rename(columns={'ltable_id': 'left_id', 'rtable_id': 'right_id'})
    table_a_csv = pd.read_csv(table_a)
    table_a_csv = table_a_csv.rename(columns={col: 'left_' + col for col in table_a_csv.columns})
    table_b_csv = pd.read_csv(table_b)
    table_b_csv = table_b_csv.rename(columns={col: 'right_' + col for col in table_b_csv.columns})
    merged_csv = pd.merge(merged_csv, table_a_csv, on='left_id')
    merged_csv = pd.merge(merged_csv, table_b_csv, on='right_id')
    merged_csv['id'] = merged_csv[['left_id', 'right_id']].apply(lambda row: '_'.join([str(c) for c in row]), axis=1)
    del merged_csv['left_id']
    del merged_csv['right_id']
    merged_csv.to_csv(output, index=False)


def prepare_deepmatcher_dataset(dataset_path, left='tableA.csv', right='tableB.csv',
                                train='train.csv', valid='valid.csv', test='test.csv'):
    a_path = os.path.join(dataset_path, left)
    b_path = os.path.join(dataset_path, right)
    train_path = os.path.join(dataset_path, train)
    joined_train_path = os.path.join(dataset_path, 'joined_'+train)
    valid_path = os.path.join(dataset_path, valid)
    joined_valid_path = os.path.join(dataset_path, 'joined_'+valid)
    test_path = os.path.join(dataset_path, test)
    joined_test_path = os.path.join(dataset_path, 'joined_'+test)

    merge_data(train_path, a_path, b_path, joined_train_path)
    merge_data(valid_path, a_path, b_path, joined_valid_path)
    merge_data(test_path, a_path, b_path, joined_test_path)



def run(dataset):

    deepmatcher_datasets = os.path.join('..', 'resources', 'Datasets')
    dataset = os.path.join(deepmatcher_datasets, dataset)
    prepare_deepmatcher_dataset(dataset)



if __name__ == '__main__':
    deepmatcher_datasets = os.path.join('..', 'resources', 'Datasets')

    dataset = os.path.join(deepmatcher_datasets, 'Beer')
    prepare_deepmatcher_dataset(dataset)

    # preds = match.run(amazon_google, 'joined_train.csv', 'joined_valid.csv', 'joined_test.csv', epochs=2)
    # print(preds)
