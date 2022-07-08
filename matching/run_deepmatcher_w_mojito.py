import os
import sys
import deepmatcher as dm
import pandas as pd
import numpy as np
import string
import random
import warnings
import contextlib

warnings.simplefilter(action='ignore', category=FutureWarning)

import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from mojito import Mojito, chart
from matching import run_deepmatcher as rdm


# to install deepmatcher on Windows 10: pip install git+https://github.com/anhaidgroup/deepmatcher#egg=deepmatcher
# also update deepmatcher/data/field.py, and two more files in the same folder to "from torchtext.legacy import data"

# to install mojito: git clone https://github.com/0xNaN/mojito.git
# and then to install it's requirments: pip install -r mojito/requirements.txt


def run(data_path, train_file, valid_file, test_file, unlabeled_file=None, epochs=10): #TODO: more epochs for testing
    print('Running DeepMatcher with data from folder: ' + str(data_path))
    
    # Build explainer-ready datasets
    build_dm_dataset(data_path)

    #rd.prepare_deepmatcher_dataset(data_path)

    model = rdm.train_or_load_pretrained_model(dm.MatchingModel(), data_path, train_file, valid_file, test_file, 'best_model_w_explainer.pth',epochs,left_prefix= 'ltable_',right_prefix= 'rtable_')   
    
    if unlabeled_file:
        preds = get_predictions_from_unlabeled_data(model, unlabeled_file)
    else:
        preds = rdm.get_predictions_from_labeled_data(model, data_path, test_file, left_prefix= 'ltable_',right_prefix= 'rtable_')

    
    data = pd.read_csv(os.path.join(data_path,test_file), dtype = str)
    proba = wrap_dm(model)(data)
    tp_group = data[(proba[:, 1] >= 0.5) & (data['label'] == '1')]
    tn_group = data[(proba[:, 0] >= 0.5) & (data['label'] == '0')]

    len(tp_group), len(tn_group)

    mojito = Mojito(data.columns,
                attr_to_copy = 'left',
                split_expression = " ",
                class_names = ['no_match', 'match'],
                feature_selection = "lasso_path")

    tp_result = mojito.drop(wrap_dm(model),
                        tp_group,
                        num_features = 15,
                        num_perturbation = 500)

    tn_result = mojito.copy(wrap_dm(model),
                        tn_group,
                        num_features = 15,
                        num_perturbation = 100)
    chart(tp_result, (1, 1, 1), (-0.6, 0.4), title = "chart_tp", dataset_path = data_path)
    chart(tn_result, (1, 1, 1), (-0.6, 0.4), title = "chart_tn", dataset_path = data_path)
    return preds 

def wrap_dm(model, ignore_columns = ['label', 'id']):

  def wrapper(dataframe):
    data = dataframe.copy().drop([c for c in ignore_columns if c in dataframe.columns], axis = 1)

    data['id'] = np.arange(len(dataframe))

    tmp_name = "./{}.csv".format("".join([random.choice(string.ascii_lowercase) for _ in range(10)]))
    data.to_csv(tmp_name, index = False)

    with open(os.devnull, 'w') as devnull:
      with contextlib.redirect_stdout(devnull):
        data_processed = dm.data.process_unlabeled(tmp_name, trained_model = model)
        out_proba = model.run_prediction(data_processed, output_attributes = True)
        out_proba = out_proba['match_score'].values.reshape(-1)

    multi_proba = np.dstack((1-out_proba, out_proba)).squeeze()

    os.remove(tmp_name)
    return multi_proba
  return wrapper

# Utilities functions to read datasets
#
def merge_sources(table, left_prefix, right_prefix, left_source, right_source, copy_from_table, ignore_from_table):

  dataset = pd.DataFrame(columns = {col:table[col].dtype for col in copy_from_table})
  ignore_column = copy_from_table + ignore_from_table

  for _, row in table.iterrows():
    leftid  = row[left_prefix  + 'id']

    rightid = row[right_prefix + 'id']

    new_row = {column: row[column] for column in copy_from_table}

    for id, source, prefix in [(leftid,  left_source,  left_prefix),
                               (rightid, right_source, right_prefix)]:
      for column in source.keys():
        if column not in ignore_column:
          new_row[prefix + column] = source.loc[id][column]

    new_row['id'] = str(leftid) +'_'+ str(rightid)

    dataset = dataset.append(new_row, ignore_index = True)
  return dataset

def build_dm_dataset(type):
  left  = pd.read_csv(os.path.join(type, "tableA.csv"))
  right = pd.read_csv(os.path.join(type, "tableB.csv"))
  train = pd.read_csv(os.path.join(type, "train.csv"))
  valid = pd.read_csv(os.path.join(type, "valid.csv"))
  test  = pd.read_csv(os.path.join(type, "test.csv"))

  train_name = "merged_train.csv"
  valid_name = "merged_valid.csv"
  test_name  = "merged_test.csv"

  train_path = os.path.join(type, train_name)
  valid_path = os.path.join(type, valid_name)
  test_path  = os.path.join(type,  test_name)

  merge_sources(train, 'ltable_', 'rtable_', left, right, ['label'], ['id']).to_csv(os.path.join(type,train_name), index = False)
  merge_sources(valid, 'ltable_', 'rtable_', left, right, ['label'], ['id']).to_csv(os.path.join(type,valid_name), index = False)
  merge_sources(test,  'ltable_', 'rtable_', left, right, ['label'], ['id']).to_csv(os.path.join(type,test_name), index = False)

  train_d, validation_d, test_d = dm.data.process(
    path = type,
    train = train_name,
    validation = valid_name,
    test = test_name,
    left_prefix = 'ltable_',
    right_prefix = 'rtable_',
   )

  return (train_path, train_d), (test_path, test_d), (valid_path, validation_d)

if __name__ == '__main__':
    
    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    data_path = sys.argv[1] if args else '../resources/datasets/test/'  # the folder containing train,valid,test data
    train_file = sys.argv[2] if args else 'merged_train.csv'
    valid_file = sys.argv[3] if args else 'merged_valid.csv'
    test_file = sys.argv[4] if args else 'merged_test.csv'
    #unlabeled_file = sys.argv[5] if args else '../resources/datasets/test/test_unlabeled.csv'  # unlabeled data for predictions

    preds = run(data_path, train_file, valid_file, test_file)
    #print(preds)

