import os
import sys
import deepmatcher as dm
import pandas as pd
# to install deepmatcher on Windows 10: pip install git+https://github.com/anhaidgroup/deepmatcher#egg=deepmatcher
# also update deepmatcher/data/field.py, and two more files in the same folder to "from torchtext.legacy import data"


def train_or_load_pretrained_model(model, data_path, train_file, valid_file, test_file, model_name='best_model.pth' , epochs=3,left_prefix ='left_', right_prefix='right_'):
    train, validation, test = dm.data.process(path=data_path, train=train_file, validation=valid_file, test=test_file,left_prefix=left_prefix, right_prefix=right_prefix)
    try:
        model.load_state(os.path.join(data_path, model_name))
        print('Using the pre-trained model '+model_name+'. Delete it or rename it to re-train the model.')
    except:
        print('No pre-trained model found stored as ' + model_name +' in the current path.')
        print('Starting training and storing model at current path as '+model_name+ ' ...')
        model.run_train(train, validation, best_save_path=os.path.join(data_path, model_name), epochs=epochs)
        print('Starting evaluation...')
        model.run_eval(test)
    return model


def get_predictions_from_unlabeled_data(model, unlabeled_file):
    print('Starting predictions on unlabeled data stored in ' + unlabeled_file)
    unlabeled = dm.data.process_unlabeled(path=unlabeled_file, trained_model=model)

    predictions = pd.DataFrame(model.run_prediction(unlabeled, output_attributes=True))
    # print(predictions.to_csv(columns=['left_id', 'right_id', 'match_score'], index=False))

    return predictions


def get_predictions_from_labeled_data(model, path, file, left_prefix = 'left_', right_prefix= 'right_'):
    print('Starting predictions on labeled data stored in ' + file)
    processed = dm.data.process(path=path, train=file, left_prefix = left_prefix, right_prefix=right_prefix)
    predictions = pd.DataFrame(model.run_prediction(processed, output_attributes=True))

    return predictions


def run(data_path, train_file, valid_file, test_file, unlabeled_file=None, epochs=2): #TODO: more epochs for testing
    print('Running DeepMatcher with data from folder: ' + str(data_path))

    model = train_or_load_pretrained_model(dm.MatchingModel(), data_path, train_file, valid_file, test_file, epochs=epochs)
    if unlabeled_file:
        return get_predictions_from_unlabeled_data(model, unlabeled_file)
    else:
        return get_predictions_from_labeled_data(model, data_path, test_file)


if __name__ == '__main__':

    args = True if len(sys.argv[1:]) > 4 else False  # checks if user provided runtime arguments or not

    data_path = sys.argv[1] if args else '../resources/datasets/test/'  # the folder containing train,valid,test data
    train_file = sys.argv[2] if args else 'test_train.csv'
    valid_file = sys.argv[3] if args else 'test_valid.csv'
    test_file = sys.argv[4] if args else 'test_test.csv'
    unlabeled_file = sys.argv[5] if args else '../resources/datasets/test/test_unlabeled.csv'  # unlabeled data for predictions

    preds = run(data_path, train_file, valid_file, test_file, unlabeled_file)
    #print(preds)
